-- =============================================================================
-- Lever 17: High-Performance Composite Indexes
-- =============================================================================
-- Index supporting filtering by tenant and status, and ordered by creation date
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_orders_tenant_status_created 
ON orders (tenant_id, status, created_at DESC);

-- =============================================================================
-- Lever 24: Specific Column Projections (Avoid SELECT *)
-- =============================================================================
-- Inefficient: Reads heavy unused text blobs and JSON metadata into memory
-- SELECT * FROM users WHERE tenant_id = 'org_123' AND is_active = true;

-- Optimized: Explicitly project required fields only
SELECT id, username, email, avatar_url, updated_at 
FROM users 
WHERE tenant_id = 'org_123' AND is_active = true
LIMIT 50;

-- =============================================================================
-- Lever 08: Resolving N+1 Query Antipatterns
-- =============================================================================
-- Antipattern:
-- 1. SELECT * FROM articles WHERE status = 'published' LIMIT 20;
-- 2. Loop 20 times: SELECT * FROM authors WHERE id = article.author_id;

-- Solution: Eager Join or Batched CTE in a single roundtrip
SELECT 
    a.id AS article_id,
    a.title,
    a.slug,
    a.created_at,
    u.id AS author_id,
    u.username AS author_name,
    u.avatar_url AS author_avatar
FROM articles a
INNER JOIN users u ON a.author_id = u.id
WHERE a.status = 'published'
ORDER BY a.created_at DESC
LIMIT 20;

-- =============================================================================
-- Lever 05: Scalable Cursor-Based Pagination
-- =============================================================================
-- Antipattern (Offset Pagination degrades as offset grows):
-- SELECT * FROM audit_logs ORDER BY id DESC LIMIT 50 OFFSET 100000;

-- Solution (Cursor Pagination uses primary key index directly, O(1) performance):
SELECT id, action, actor_id, target_id, created_at
FROM audit_logs
WHERE id < :last_seen_id
ORDER BY id DESC
LIMIT 50;
