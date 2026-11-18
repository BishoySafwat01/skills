# App Performance Optimizer Skill

A production-grade Agent Skill for full-stack web and mobile application performance engineering. Designed to diagnose, audit, and systematically resolve bottlenecks across frontend rendering, network delivery, client state, backend concurrency, database queries, and observability.

## Overview

Modern software development—especially with AI-assisted or rapid prototyping—often introduces subtle performance bottlenecks: unindexed queries, duplicate API calls, cascading re-renders, and unbounded network payloads.

This skill equips AI agents (Claude Code, Antigravity, Cursor, Codex) and human engineers with **31 battle-tested performance levers** organized into 6 architectural tiers.

## The 6 Performance Tiers

| Tier | Focus Area | Core Levers |
|---|---|---|
| **Tier 1** | **Frontend & DOM** | Skeleton Loading, Modern Formats (WebP/AVIF), Lazy Loading, Code Splitting, List Virtualization, Re-render Prevention, Self-hosted Fonts |
| **Tier 2** | **Network & Edge** | Global CDN, Brotli/Gzip Compression, Deferring Third-Party Scripts, Immutable Browser Caching |
| **Tier 3** | **API & Client State** | Request Deduplication, Debounce & Throttle, Cursor Pagination, External API Timeouts, AI Streaming (SSE), Optimistic UI, Parallel Execution |
| **Tier 4** | **Backend Concurrency**| Background Job Queues, Dependency Pruning, Server & DB Colocation, SSR/SSG Selection, Connection Pooling, Horizontal Load Balancing |
| **Tier 5** | **Database & Storage** | B-Tree Indexing, Explicit Projections (No `SELECT *`), Resolving N+1 Queries, In-Memory Caching (Redis) |
| **Tier 6** | **Observability & Testing**| Distributed Tracing (OpenTelemetry), Real User Monitoring (RUM), Low-end Device & 3G Simulation |

## Quick Usage

### For AI Coding Agents (Claude, Cursor, Antigravity)
Point your agent to this skill or copy the prompt from [`references/prompt-template.md`](references/prompt-template.md):

```markdown
Audit this codebase using the `app-performance-optimizer` skill. Identify the top 5 highest-impact bottlenecks, provide surgical code fixes, and generate a Before/After metrics delta table.
```

### Verification Criteria
Every optimization must be validated against measurable benchmarks:
- **Load Time & Core Web Vitals** (LCP, FID/INP, CLS)
- **Time to First Token (TTFT)** for LLM/AI streaming
- **Database Query Count & P95 Execution Time**
- **Transferred Payload Size & HTTP Request Count**

## Directory Structure

```text
app-performance-optimizer/
├── SKILL.md                 # Agent instruction specification and executable rules
├── README.md                # Human-readable documentation and quickstart
├── reference.md             # In-depth architectural breakdown of all 31 levers
├── references/
│   └── prompt-template.md   # Ready-to-use prompt for auditing any repository
└── examples/
    ├── react-optimizations.tsx    # Concrete React/TypeScript implementation examples
    ├── database-queries.sql       # High-performance SQL queries, indexes, and anti-pattern fixes
    └── server-nginx.conf          # Optimized Nginx configuration for compression and caching
```
