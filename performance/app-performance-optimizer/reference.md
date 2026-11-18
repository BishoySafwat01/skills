# Complete Technical Reference: The 31 Performance Levers

This document provides in-depth architectural guidance for each of the 31 production levers defined in the `app-performance-optimizer` skill.

---

### Tier 1: Frontend Rendering & DOM (Client-Side)

1. **Skeleton Loading (01/31)**
   - *Goal*: Eliminate layout shifts (CLS) and reduce perceived latency.
   - *Implementation*: Render CSS pulse containers that mirror exact dimensions of incoming cards/tables. Never show a blank container or generic spinner that shifts content upon resolution.

2. **Modern Image Formats: WebP & AVIF (02/31)**
   - *Goal*: Reduce image payload by 60%–80% without perceptual quality loss.
   - *Implementation*: Serve AVIF with WebP fallback via `<picture>`. Resize dynamically to client viewport.

3. **Lazy Loading Below-the-Fold (15/31)**
   - *Goal*: Reserve initial bandwidth for Critical Rendering Path assets.
   - *Implementation*: Add native `loading="lazy"` and `decoding="async"` to all images and iframes below initial viewport.

4. **Route-Based Code Splitting (22/31)**
   - *Goal*: Avoid sending the entire multi-route JavaScript bundle to users viewing a single page.
   - *Implementation*: Use dynamic imports (`React.lazy`, Vite manual chunks, Next.js dynamic) to separate admin, dashboard, and public bundles.

5. **List Virtualization / Windowing (23/31)**
   - *Goal*: Maintain smooth 60fps scrolling and bounded RAM consumption on large datasets.
   - *Implementation*: Render only visible items inside scroll container using TanStack Virtual or react-window.

6. **Re-render Prevention (26/31)**
   - *Goal*: Prevent deep DOM tree re-render cycles on parent state changes.
   - *Implementation*: Colocate state locally. Use memoization (`React.memo`, `useCallback`, `useMemo`) on expensive components.

7. **Self-Hosted Fonts & Minimal Weights (29/31)**
   - *Goal*: Eliminate external DNS/TLS handshakes and Flash of Invisible Text (FOIT).
   - *Implementation*: Self-host WOFF2 font files on domain. Subset fonts to required characters and load only necessary weights (e.g., 400 and 700).

---

### Tier 2: Network Delivery & Transport (Edge Layer)

8. **Content Delivery Network (CDN) (06/31)**
   - *Goal*: Minimize geographic roundtrip latency.
   - *Implementation*: Cache and serve static assets and immutable media from edge nodes (Cloudflare, CloudFront, Fastly).

9. **Brotli & Gzip HTTP Compression (09/31)**
   - *Goal*: Minimize wire transfer size for text payloads (HTML, CSS, JS, JSON).
   - *Implementation*: Enable Brotli compression level 5–6 with Gzip fallback on reverse proxies and servers.

10. **Immutable Browser Caching (27/31)**
    - *Goal*: Eliminate redundant downloads for returning users.
    - *Implementation*: Serve asset files with content hashes and `Cache-Control: public, max-age=31536000, immutable`.

11. **Deferred Third-Party Scripts (21/31)**
    - *Goal*: Prevent non-critical analytics and widgets from blocking main thread execution.
    - *Implementation*: Mark external tags with `defer` or inject them on `requestIdleCallback` after interactive readiness.

---

### Tier 3: Client State & API Interactions (Data Layer)

12. **In-Flight Request Deduplication (03/31)**
    - *Goal*: Prevent duplicate HTTP requests when multiple components mount concurrently.
    - *Implementation*: Use SWR/TanStack Query or an in-flight Promise cache map.

13. **Input Debounce & Throttle (04/31)**
    - *Goal*: Prevent backend flooding on rapid typing and avoid UI race conditions.
    - *Implementation*: Debounce search/autocomplete inputs by 250ms–350ms and cancel previous requests using `AbortController`.

14. **Cursor-Based API Pagination (05/31)**
    - *Goal*: Prevent database performance degradation on large offsets ($O(1)$ vs $O(N)$).
    - *Implementation*: Slice queries using indexed sequential columns (`WHERE id > :cursor LIMIT :size`).

15. **External API Timeouts (12/31)**
    - *Goal*: Prevent slow third-party services from locking server worker threads.
    - *Implementation*: Enforce strict timeouts on every outbound fetch using `AbortSignal.timeout(ms)`.

16. **AI Streaming via Server-Sent Events (13/31)**
    - *Goal*: Reduce Time to First Token (TTFT) from 10–20 seconds to sub-second.
    - *Implementation*: Stream token chunks incrementally over SSE or WebSockets.

17. **Optimistic UI with Rollback (14/31)**
    - *Goal*: Provide immediate visual feedback for user actions.
    - *Implementation*: Mutate UI state immediately, dispatch network request in background, and revert gracefully on error.

18. **Parallel Request Orchestration (16/31)**
    - *Goal*: Eliminate waterfall request chains.
    - *Implementation*: Execute independent network requests concurrently using `Promise.all()`.

---

### Tier 4: Backend Architecture & Concurrency (Server Layer)

19. **Background Job Queues (07/31)**
    - *Goal*: Keep HTTP request-response cycles sub-100ms.
    - *Implementation*: Enqueue CPU-heavy or I/O-heavy jobs (PDF generation, emails) into BullMQ/Celery workers and return `202 Accepted`.

20. **Dependency Tree Pruning (11/31)**
    - *Goal*: Reduce bundle sizes and server container boot times.
    - *Implementation*: Audit dependencies with `depcheck` and replace heavy legacy libraries with modular alternatives.

21. **Physical Colocation of Server & Database (19/31)**
    - *Goal*: Eliminate cross-region network latency on database roundtrips.
    - *Implementation*: Deploy backend compute and database clusters within the same cloud region and Availability Zone.

22. **Hybrid Rendering Strategy (SSR / SSG) (20/31)**
    - *Goal*: Balance instant initial paint with server load.
    - *Implementation*: Pre-render static pages at build time (SSG/ISR) and reserve dynamic SSR for authenticated or frequently modified dashboards.

23. **Database Connection Pooling (25/31)**
    - *Goal*: Avoid socket and TLS handshake exhaustion under concurrent traffic.
    - *Implementation*: Route queries through connection poolers (PgBouncer, Prisma Accelerate) with persistent socket pools.

24. **Horizontal Load Balancing (28/31)**
    - *Goal*: Eliminate single-instance resource exhaustion.
    - *Implementation*: Place stateless application instances behind an Nginx or cloud load balancer with health checks.

---

### Tier 5: Database & Query Performance (Storage Layer)

25. **Targeted Database Indexing (17/31)**
    - *Goal*: Eliminate full table scans on read queries.
    - *Implementation*: Add composite B-tree indexes matching filter (`WHERE`), join (`ON`), and sort (`ORDER BY`) columns.

26. **Explicit Column Projections (24/31)**
    - *Goal*: Reduce memory consumption and wire payload.
    - *Implementation*: Never use `SELECT *`; specify only the exact columns needed by the view.

27. **Resolving N+1 Queries (08/31)**
    - *Goal*: Replace multiple sequential child queries with a single batched query.
    - *Implementation*: Use SQL `JOIN`, Prisma `include`, or DataLoader patterns.

28. **In-Memory Caching with Redis (10/31)**
    - *Goal*: Relieve database load for high-read datasets.
    - *Implementation*: Store pre-computed query results in Redis with deterministic cache keys and TTLs.

---

### Tier 6: Observability & Field Verification (Testing Layer)

29. **Distributed Tracing with OpenTelemetry (18/31)**
    - *Goal*: Pinpoint exact bottlenecks across services and middlewares.
    - *Implementation*: Instrument services with OpenTelemetry traces to identify the slowest span.

30. **Real User Monitoring (RUM) (30/31)**
    - *Goal*: Monitor user experience under real-world device and network conditions.
    - *Implementation*: Collect Core Web Vitals (LCP, INP, CLS) from field sessions via RUM instrumentation.

31. **Device & Network Throttling Emulation (31/31)**
    - *Goal*: Verify acceptable performance on low-end hardware and degraded connectivity.
    - *Implementation*: Test critical user paths under 4x CPU slowdown and Slow 3G network profiles.
