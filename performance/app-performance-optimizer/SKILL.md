---
name: app-performance-optimizer
description: Full-stack application performance engineering skill. Audits, diagnoses, and resolves bottlenecks across frontend rendering, network delivery, API state, backend concurrency, database queries, and observability based on the 31 production-grade performance levers. Use when an app is slow, sluggish, suffering high latency, preparing for high traffic, or when optimizing AI-generated (Vibe Coding) codebases.
license: MIT
metadata:
  author: "Antigravity Engineering / Anthropic Reference Standard"
  version: "1.0.0"
  domain: "performance-engineering"
  triggers: "performance optimization, app is slow, speed up app, vibe coding optimization, database indexing, caching, latency reduction, Core Web Vitals, N+1 queries, load balancing, bundle size"
  role: "Principal Performance Architect"
  scope: "fullstack-optimization"
  output-format: "diagnostic-and-implementation"
---

# App Performance Optimizer (The 31 Production Levers)

An elite, full-stack performance engineering guide designed for AI coding agents and human engineers. It transforms slow, bloated, or raw AI-generated (Vibe Coding) applications into blazing-fast, resilient, production-ready software.

---

## Prime Directive

> **"Never optimize blindly. Measure first, identify the single slowest bottleneck (the critical path), apply surgical fixes, and verify with before/after metrics."**

When tasked with improving application speed or auditing an existing codebase, do NOT apply random micro-optimizations. Follow the **Systematic Optimization Protocol**:

1. **Profile & Trace**: Identify whether the bottleneck is Client Render, Network Latency, API Waterfall, Server Compute, or Database I/O.
2. **Apply the 31 Levers**: Locate the relevant tier below and apply the exact architectural pattern.
3. **Verify the Delta**: Measure before vs. after metrics (Load Time, TTFT, P95 Query Time, Payload Size, Request Count).

---

## Architectural Map: The 6 Tiers of Performance

```
┌─────────────────────────────────────────────────────────────────────────┐
│ Tier 1: Frontend Rendering & DOM (Skeletons, WebP/AVIF, Virtualization) │
├─────────────────────────────────────────────────────────────────────────┤
│ Tier 2: Network Delivery & Edge Caching (CDN, Brotli, Browser Caching) │
├─────────────────────────────────────────────────────────────────────────┤
│ Tier 3: Client State & API Orchestration (Debounce, Dedup, Streaming)   │
├─────────────────────────────────────────────────────────────────────────┤
│ Tier 4: Backend Concurrency & Distributed Systems (Queues, SSR, LB)     │
├─────────────────────────────────────────────────────────────────────────┤
│ Tier 5: Database & Query Performance (Indexes, No SELECT *, N+1, Redis) │
├─────────────────────────────────────────────────────────────────────────┤
│ Tier 6: Observability, Real-World Emulation & Verification (OTel, RUM) │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Tier 1: Frontend Rendering & Asset Optimization

### Lever 01: Skeleton Loading
* **Problem**: Blank screens or abrupt spinners cause high perceived latency and layout shift (CLS).
* **Rule**: For any asynchronous view, render a lightweight CSS animated placeholder matching the exact geometric footprint of incoming data.
* **Pattern (React/Tailwind)**:
```tsx
export function ProductCardSkeleton() {
  return (
    <div className="w-full max-w-sm rounded-2xl p-4 bg-slate-900 border border-slate-800 animate-pulse">
      <div className="w-full h-48 bg-slate-800 rounded-xl mb-4" />
      <div className="h-4 bg-slate-800 rounded w-3/4 mb-2" />
      <div className="h-3 bg-slate-800 rounded w-1/2" />
    </div>
  );
}
```

### Lever 02: Modern Image Formats (WebP / AVIF)
* **Problem**: Legacy PNG/JPEG images waste megabytes of bandwidth and block First Contentful Paint.
* **Rule**: Serve modern compressed formats (AVIF first, WebP fallback), resized to the user's display viewport.
* **Pattern (HTML5 Picture)**:
```html
<picture>
  <source srcset="hero-800.avif 800w, hero-1200.avif 1200w" type="image/avif" />
  <source srcset="hero-800.webp 800w, hero-1200.webp 1200w" type="image/webp" />
  <img src="hero-800.jpg" alt="Hero banner" loading="lazy" decoding="async" width="800" height="450" />
</picture>
```

### Lever 15: Lazy Loading Below-the-Fold
* **Problem**: Downloading off-screen images blocks network bandwidth required for critical above-the-fold assets.
* **Rule**: Add native `loading="lazy"` and `decoding="async"` to all images not immediately visible in the initial viewport.
```html
<img src="product-detail.webp" loading="lazy" decoding="async" alt="Product" />
```

### Lever 22: Route-Based Code Splitting
* **Problem**: Monolithic JavaScript bundles force users to download entire application code upfront.
* **Rule**: Split bundles by route and dynamic modals using dynamic `import()`.
* **Pattern (React)**:
```tsx
import { lazy, Suspense } from 'react';
const CheckoutModal = lazy(() => import('./features/checkout/CheckoutModal'));

export function App() {
  return (
    <Suspense fallback={<ProductCardSkeleton />}>
      {isOpen && <CheckoutModal />}
    </Suspense>
  );
}
```

### Lever 23: List Virtualization (Windowing)
* **Problem**: Rendering hundreds or thousands of DOM nodes causes severe memory bloat and scroll stutter.
* **Rule**: Render only elements currently visible inside the viewport, recycling nodes as the user scrolls.
* **Implementation Standard**: Use `@tanstack/react-virtual` or `react-window`.
```tsx
import { useVirtualizer } from '@tanstack/react-virtual';

export function VirtualList({ items }: { items: string[] }) {
  const parentRef = useRef<HTMLDivElement>(null);
  const rowVirtualizer = useVirtualizer({
    count: items.length,
    getScrollElement: () => parentRef.current,
    estimateSize: () => 48,
    overscan: 5,
  });

  return (
    <div ref={parentRef} className="h-96 overflow-auto">
      <div style={{ height: `${rowVirtualizer.getTotalSize()}px`, position: 'relative' }}>
        {rowVirtualizer.getVirtualItems().map((virtualRow) => (
          <div
            key={virtualRow.index}
            style={{
              position: 'absolute',
              top: 0,
              left: 0,
              width: '100%',
              height: `${virtualRow.size}px`,
              transform: `translateY(${virtualRow.start}px)`,
            }}
          >
            {items[virtualRow.index]}
          </div>
        ))}
      </div>
    </div>
  );
}
```

### Lever 26: Prevent Unnecessary Re-renders
* **Problem**: Global state updates trigger waterfall re-renders of heavy pure components.
* **Rule**: Colocate state close to where it is used. Wrap heavy child components in `memo`, and isolate unstable object/callback references with `useCallback` and `useMemo`.

### Lever 29: Self-Hosted Fonts & Minimal Weights
* **Problem**: Third-party fonts (e.g. Google Fonts) create external DNS, TLS, and TCP handshakes, causing FOIT (Flash of Invisible Text).
* **Rule**: Self-host WOFF2 font files on the same domain and subset them to include only required weights (e.g., 400 & 700). Set `font-display: swap`.
```css
@font-face {
  font-family: 'Inter';
  font-style: normal;
  font-weight: 400;
  font-display: swap;
  src: url('/fonts/inter-latin-400.woff2') format('woff2');
}
```

---

## Tier 2: Network Delivery & Edge Caching

### Lever 06: Content Delivery Network (CDN)
* **Problem**: Serving static assets directly from origin server introduces severe latency for geographically distant users.
* **Rule**: Route all static assets, media, and cached responses through an edge CDN (Cloudflare, AWS CloudFront, Fastly).

### Lever 09: Brotli / Gzip Compression
* **Problem**: Uncompressed text files (HTML, JS, CSS, JSON) waste network transfer time.
* **Rule**: Enable Brotli compression (`br`) with fallback to Gzip (`gzip`) on web servers and reverse proxies.
* **Nginx Configuration**:
```nginx
brotli on;
brotli_comp_level 6;
brotli_types text/plain text/css application/javascript application/json image/svg+xml;

gzip on;
gzip_comp_level 6;
gzip_types text/plain text/css application/javascript application/json image/svg+xml;
```

### Lever 21: Defer Third-Party Scripts
* **Problem**: Analytics, tracking pixels, and customer support widgets monopolize the browser's Main Thread.
* **Rule**: Load third-party scripts with `defer` or inject them dynamically on `requestIdleCallback` after first user interaction.
```html
<script src="https://analytics.example.com/script.js" defer></script>
```

### Lever 27: Browser Caching & Immutable Headers
* **Problem**: Returning visitors re-download unchanged static assets on every page visit.
* **Rule**: Use content-hashed filenames (e.g., `app.8f3a9c.js`) and serve with 1-year immutable cache headers.
```http
Cache-Control: public, max-age=31536000, immutable
```

---

## Tier 3: Client State & API Interactions

### Lever 03: Eliminate Duplicate API Calls
* **Problem**: Multiple child components mount simultaneously and fire redundant GET requests for the same dataset.
* **Rule**: Use an in-flight request deduplication layer (TanStack Query, SWR, or module-scoped Promise cache).
```ts
const inFlightRequests = new Map<string, Promise<any>>();

export function fetchDeduplicated<T>(url: string): Promise<T> {
  if (inFlightRequests.has(url)) {
    return inFlightRequests.get(url)!;
  }
  const promise = fetch(url).then(r => r.json()).finally(() => {
    inFlightRequests.delete(url);
  });
  inFlightRequests.set(url, promise);
  return promise;
}
```

### Lever 04: Debounce Search & Autocomplete
* **Problem**: Triggering an API request on every keystroke floods the backend and causes race conditions.
* **Rule**: Debounce search inputs by 250ms–400ms. Cancel pending requests via `AbortController`.
```ts
export function debounce<T extends (...args: any[]) => void>(fn: T, delayMs: number) {
  let timer: NodeJS.Timeout;
  return (...args: Parameters<T>) => {
    clearTimeout(timer);
    timer = setTimeout(() => fn(...args), delayMs);
  };
}
```

### Lever 05: Pagination & Slicing
* **Problem**: Returning unbounded arrays (`SELECT * FROM orders`) degrades server memory and network transfer.
* **Rule**: Enforce pagination on every collection endpoint. Prefer cursor-based pagination over offset-based for large datasets.
```sql
-- Fast Cursor Pagination (uses index directly)
SELECT id, name, created_at FROM items
WHERE id > :last_seen_id
ORDER BY id ASC LIMIT 25;
```

### Lever 12: External API Timeouts
* **Problem**: A hung third-party payment or notification service keeps backend threads hostage, causing server exhaustion.
* **Rule**: Every outbound HTTP call MUST enforce a strict timeout using `AbortSignal.timeout()`.
```ts
async function callExternalService(url: string) {
  const response = await fetch(url, {
    signal: AbortSignal.timeout(3500) // 3.5s timeout
  });
  return response.json();
}
```

### Lever 13: AI Streaming (Server-Sent Events)
* **Problem**: Waiting 15–30 seconds for an LLM to generate a complete response causes high user drop-off.
* **Rule**: Stream tokens incrementally via Server-Sent Events (SSE) or WebSockets to achieve sub-second TTFT (Time to First Token).

### Lever 14: Optimistic UI with Error Rollback
* **Problem**: Waiting for network confirmation before toggling a "like" or "checkbox" feels sluggish and laggy.
* **Rule**: Update client state instantly, persist in the background, and revert gracefully if the request fails.
```tsx
const toggleLike = async () => {
  const previous = isLiked;
  setIsLiked(!previous); // Instant UI update
  try {
    await api.post('/like', { id });
  } catch (err) {
    setIsLiked(previous); // Rollback on failure
    toast.error('Could not save like. Please try again.');
  }
};
```

### Lever 16: Parallel Request Execution
* **Problem**: Await-chains create unnecessary waterfalls:
  `const user = await getUser(); const orders = await getOrders();` (Total: A + B).
* **Rule**: Fire independent promises concurrently with `Promise.all()`.
```ts
const [user, orders, recommendations] = await Promise.all([
  fetchUser(userId),
  fetchOrders(userId),
  fetchRecommendations(userId)
]);
```

---

## Tier 4: Backend Architecture & Concurrency

### Lever 07: Background Job Queues
* **Problem**: Synchronously executing heavy tasks (PDF generation, report export, email sending) during HTTP requests blocks server workers.
* **Rule**: Enqueue slow jobs into a background queue (BullMQ, Celery, SQS) and return `202 Accepted` immediately with a Job ID.

### Lever 11: Prune Unused Dependencies
* **Problem**: Bloated `node_modules` and Python packages slow down cold starts and serverless container boots.
* **Rule**: Audit dependencies using `depcheck` or `npx bundle-analyzer`. Replace oversized libraries with lean alternatives (e.g., date-fns or native Temporal API instead of moment.js).

### Lever 19: Physical Server & Database Proximity
* **Problem**: Hosting API servers in `us-east-1` and database instances in `eu-west-1` adds 80ms–150ms roundtrip latency to every query.
* **Rule**: Colocate backend computing instances and database clusters in the same cloud region and Availability Zone (AZ) within a private VPC.

### Lever 20: Hybrid Rendering (SSR / SSG)
* **Problem**: Client-side rendering (CSR) causes slow initial load, while pure SSR can overload server CPU on high traffic.
* **Rule**: Use Static Site Generation (SSG) / ISR for public, marketing, and catalog pages; reserve Server-Side Rendering (SSR) for dynamic, personalized dashboards.

### Lever 25: Database Connection Pooling
* **Problem**: Creating a new TCP and TLS handshake with PostgreSQL on every serverless or API invocation exhausts database connection limits.
* **Rule**: Implement a connection pooler (PgBouncer, Prisma Accelerate, or HikariCP) to reuse warm persistent connections.

### Lever 28: Horizontal Load Balancing
* **Problem**: Single server instance reaches CPU/memory limits under traffic spikes.
* **Rule**: Deploy stateless app instances behind a reverse proxy/load balancer (Nginx, AWS ALB, Cloudflare Load Balancer) using round-robin or least-connections distribution.

---

## Tier 5: Database & Query Performance

### Lever 08: Resolve N+1 Queries
* **Problem**: Fetching 50 posts and then looping to fetch author details fires 51 separate database queries.
* **Rule**: Batch relationships using `JOIN`, Prisma `include`, Django `select_related` / `prefetch_related`, or GraphQL `DataLoader`.
```sql
-- Bad: N+1
SELECT * FROM posts; -- Returns 50 rows
-- Then 50 separate: SELECT * FROM authors WHERE id = ?;

-- Good: Eager Join / Batched IN
SELECT p.*, a.name AS author_name 
FROM posts p 
LEFT JOIN authors a ON p.author_id = a.id;
```

### Lever 17: Database Indexes for High-Frequency Queries
* **Problem**: Filtering on non-indexed columns causes full table scans ($O(N)$ disk reads).
* **Rule**: Create composite B-Tree indexes matching filter (`WHERE`), join (`JOIN`), and sort (`ORDER BY`) predicates.
```sql
-- Fast query lookup for user orders by status
CREATE INDEX idx_orders_user_status_created 
ON orders (user_id, status, created_at DESC);
```

### Lever 24: Specific Column Projections (No `SELECT *`)
* **Problem**: `SELECT *` reads heavy unused columns (`description`, `avatar_blob`, `metadata`) into memory and saturates network I/O.
* **Rule**: Explicitly project only the specific columns needed by the calling UI or service.
```sql
-- Bad
SELECT * FROM users WHERE id = :id;

-- Good
SELECT id, username, email FROM users WHERE id = :id;
```

### Lever 10: In-Memory Caching with Redis
* **Problem**: Re-executing identical complex aggregation queries on every page hit.
* **Rule**: Apply the **Cache-Aside Pattern** with explicit TTLs (Time-To-Live).
```ts
async function getPopularItems() {
  const cacheKey = 'items:popular';
  const cached = await redis.get(cacheKey);
  if (cached) return JSON.parse(cached);

  const items = await db.query('SELECT id, name FROM items WHERE views > 1000');
  await redis.set(cacheKey, JSON.stringify(items), 'EX', 300); // 5 min TTL
  return items;
}
```

---

## Tier 6: Observability, Real-World Emulation & Verification

### Lever 18: Distributed Tracing with OpenTelemetry
* **Problem**: Inability to diagnose which microservice, query, or middleware caused a sudden latency spike.
* **Rule**: Instrument every service boundary with OpenTelemetry spans. Inspect flame charts to pinpoint the single "Slowest Span".

### Lever 30: Real User Monitoring (RUM)
* **Problem**: Synthetic local testing on dev laptops hides real-world network and device degradations.
* **Rule**: Capture field metrics directly from real clients (Core Web Vitals: LCP, INP, CLS, TTFB) using tools like Sentry Performance, Vercel Speed Insights, or Datadog RUM.

### Lever 31: Low-End Device & Network Throttling
* **Problem**: Applications tested only on high-end M-series Macs and Gigabit Wi-Fi fail silently for mobile users.
* **Rule**: In Chrome DevTools / Playwright, test critical user journeys under:
  * **CPU Throttling**: 4x to 6x Slowdown.
  * **Network Throttling**: "Slow 3G" or "Fast 3G".

---

## The Verification & Deliverables Contract

Whenever you complete a performance optimization task, produce the **Performance Delta Table**:

| Metric | Before Optimization | After Optimization | Delta / Improvement | Target Threshold |
|---|---|---|---|---|
| **Largest Contentful Paint (LCP)** | `4.2s` | `1.1s` | **-73.8%** | $< 2.5s$ |
| **Time to First Token (TTFT)** | `6.5s` | `0.4s` | **-93.8%** | $< 0.8s$ |
| **Total JavaScript Bundle Size** | `1.8 MB` | `320 KB` | **-82.2%** | $< 400 KB$ |
| **Total HTTP Requests (Initial)** | `48 reqs` | `14 reqs` | **-70.8%** | $< 20 reqs$ |
| **Database Query Count (P95)** | `24 queries` | `2 queries` | **-91.6%** | $\le 3$ per endpoint |
| **P95 API Response Latency** | `1,250ms` | `85ms` | **-93.2%** | $< 200ms$ |

---

## Anti-Patterns: What NOT To Do

1. **Premature Micro-Optimization**: Do not replace clean code with unreadable bitwise hacks or obscure syntax when the real bottleneck is an unindexed database query.
2. **Caching Volatile or Sensitive Data**: Never cache user authentication tokens, private PII, or rapidly changing state without strict invalidation.
3. **Optimistic UI Without Rollback**: Never assume a mutation succeeds without providing an automatic error rollback and user alert.
4. **Unbounded Background Queues**: Always implement concurrency limits and rate-limiting on worker queues to avoid crushing databases under bulk job bursts.
