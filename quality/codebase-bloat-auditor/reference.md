# Architectural Rules and Debloating Reference

This document details the architectural standards and verification rules enforced by the `codebase-bloat-auditor` skill.

---

## 1. Code Volume and Duplication Limits

### 1.1 Physical Line Budgets
- **Monorepo Target**: Total active code lines across backend, frontend, and tests should remain strictly budgeted per milestone.
- **File Length Limit**: No single `.py`, `.ts`, or `.tsx` file may exceed **350 physical lines** (excluding blank lines and comments).
- **Decomposition Principle**: Split large files by domain responsibility, never by mechanical line cutting.

### 1.2 Duplication Ceiling
- Overall duplication percentage reported by `jscpd` must stay below **3.0%**.
- Duplication above 5.0% indicates systemic copy-pasting across routes, adapters, or services.

### 1.3 Dead Code Elimination
- Zero dead symbols: every public function, class, and export must have an active caller or test anchor.
- Stale utility modules and deprecated endpoints must be deleted, not commented out.

---

## 2. Asynchronous Concurrency and Database Safety

### 2.1 Zero Blocking I/O in Async Routes
Asynchronous event loops must never be blocked by synchronous calls.

```python
# Forbidden in async functions
import time
import requests

async def handle_request():
    time.sleep(1)            # Blocks the event loop
    res = requests.get(url)  # Synchronous socket I/O

# Required pattern
import asyncio
import httpx

async def handle_request():
    await asyncio.sleep(1)
    async with httpx.AsyncClient() as client:
        res = await client.get(url)
```

### 2.2 Short Database Transactions
Never hold an active database session or transaction open across external network calls.

```python
# Forbidden pattern: DB transaction open during external HTTP
async def send_notification(session: AsyncSession, user_id: str):
    user = await session.get(User, user_id)
    # Network latency holds DB connection hostage:
    response = await external_client.post("/notify", json={"phone": user.phone})
    user.notified = True
    await session.commit()

# Required pattern: commit state first, then call external APIs
async def send_notification(session: AsyncSession, user_id: str):
    user = await session.get(User, user_id)
    phone = user.phone
    await session.commit()  # Session released
    
    response = await external_client.post("/notify", json={"phone": phone})
```

### 2.3 Atomic Claiming and Locking
When multiple workers or operators interact with shared resources, use explicit concurrency controls:
- PostgreSQL: `SELECT ... FOR UPDATE SKIP LOCKED`
- Redis: `SET key value NX EX seconds`

---

## 3. Structural Abstractions

### 3.1 Generic Repository Pattern
Avoid repeating CRUD boilerplate across database entities. Model repositories should inherit from a generic base repository and implement only domain-specific queries:

```python
class BaseAsyncRepository(Generic[ModelType, CreateSchema, UpdateSchema]):
    async def get(self, id: UUID) -> ModelType | None: ...
    async def list(self, limit: int = 50, offset: int = 0) -> list[ModelType]: ...
    async def create(self, obj_in: CreateSchema) -> ModelType: ...
    async def update(self, id: UUID, obj_in: UpdateSchema) -> ModelType: ...
    async def delete(self, id: UUID) -> bool: ...
```

### 3.2 Channel Adapter Protocol
When integrating multiple external messaging or payment providers, normalize interfaces through a shared abstract base adapter:
- Signature validation
- Inbound payload normalization
- Outbound delivery with backoff and retry policy

### 3.3 Idempotent Webhook Processing
Every webhook ingestion pipeline must enforce uniqueness on `(provider, external_event_id)` to ensure repeated deliveries produce identical system state without duplicate processing.
