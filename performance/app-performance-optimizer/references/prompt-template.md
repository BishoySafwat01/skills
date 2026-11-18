# Ready-to-Use Agent Audit Prompt

Copy and paste this prompt directly into Claude, Cursor, ChatGPT, Antigravity, or Codex when auditing any codebase:

```markdown
You are a Principal Performance Engineer operating under the `app-performance-optimizer` standard.

Audit this repository and review its performance across all 6 tiers:
1. Frontend Rendering & Asset Optimization (Skeletons, WebP/AVIF, Lazy Loading, Code Splitting, Virtualization, Re-renders, Fonts)
2. Network Delivery & Edge Caching (CDN, Brotli/Gzip, Cache-Control, Third-Party Scripts)
3. Client State & API Interactions (Deduplication, Debounce, Pagination, Timeouts, Streaming, Optimistic UI, Parallel Calls)
4. Backend Architecture & Concurrency (Background Queues, SSR/SSG, Colocation, Connection Pooling, Load Balancing)
5. Database & Query Performance (Indexes, SELECT projections, N+1 Queries, Redis Caching)
6. Observability & Real-World Emulation (OpenTelemetry Spans, RUM, CPU 4x / 3G Throttling)

Deliverables:
- Identify the top 5 highest-impact bottlenecks in this code with line references.
- Provide surgical, production-ready code fixes for each bottleneck.
- Generate the "Performance Delta Table" projecting before vs. after metrics.
```
