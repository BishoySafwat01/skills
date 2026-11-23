import React, { useState, useRef, useTransition } from 'react';

// -----------------------------------------------------------------------------
// Lever 01: Skeleton Loading Pattern
// -----------------------------------------------------------------------------
export function CardSkeleton() {
  return (
    <div className="w-full max-w-sm rounded-2xl p-4 bg-slate-900 border border-slate-800 animate-pulse">
      <div className="w-full h-48 bg-slate-800 rounded-xl mb-4" />
      <div className="h-4 bg-slate-800 rounded w-3/4 mb-2" />
      <div className="h-3 bg-slate-800 rounded w-1/2" />
    </div>
  );
}

// -----------------------------------------------------------------------------
// Lever 04: Debounce with Request Cancellation
// -----------------------------------------------------------------------------
export function useDebouncedSearch(delay = 300) {
  const [searchTerm, setSearchTerm] = useState('');
  const abortControllerRef = useRef<AbortController | null>(null);

  const handleSearchChange = (value: string, onFetch: (signal: AbortSignal, term: string) => void) => {
    setSearchTerm(value);

    // Cancel in-flight requests from prior keystrokes
    if (abortControllerRef.current) {
      abortControllerRef.current.abort();
    }

    const controller = new AbortController();
    abortControllerRef.current = controller;

    setTimeout(() => {
      if (!controller.signal.aborted && value.trim()) {
        onFetch(controller.signal, value.trim());
      }
    }, delay);
  };

  return { searchTerm, handleSearchChange };
}

// -----------------------------------------------------------------------------
// Lever 14: Optimistic UI with Rollback
// -----------------------------------------------------------------------------
interface LikeButtonProps {
  itemId: string;
  initialLiked: boolean;
  initialCount: number;
  onPersist: (id: string, liked: boolean) => Promise<void>;
}

export function OptimisticLikeButton({ itemId, initialLiked, initialCount, onPersist }: LikeButtonProps) {
  const [isLiked, setIsLiked] = useState(initialLiked);
  const [count, setCount] = useState(initialCount);
  const [isPending, startTransition] = useTransition();

  const handleToggle = () => {
    // 1. Snapshot previous state
    const prevLiked = isLiked;
    const prevCount = count;

    // 2. Optimistic update
    const nextLiked = !prevLiked;
    setIsLiked(nextLiked);
    setCount(prevCount + (nextLiked ? 1 : -1));

    // 3. Persist asynchronously
    startTransition(async () => {
      try {
        await onPersist(itemId, nextLiked);
      } catch (error) {
        // 4. Rollback on failure
        setIsLiked(prevLiked);
        setCount(prevCount);
        console.error('Optimistic update failed, reverted state:', error);
      }
    });
  };

  return (
    <button
      onClick={handleToggle}
      className={`px-3 py-1.5 rounded-full text-sm font-medium transition-colors ${
        isLiked ? 'bg-rose-600 text-white' : 'bg-slate-800 text-slate-300 hover:bg-slate-700'
      }`}
    >
      <span>{isLiked ? '[x]' : '[ ]'}</span> {count}
    </button>
  );
}
