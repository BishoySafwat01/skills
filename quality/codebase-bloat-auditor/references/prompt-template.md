# Codebase Bloat and Architecture Audit Prompt

Copy and paste this prompt into Claude Code, Antigravity, Cursor, or Codex to audit any repository:

```markdown
You are a Principal Systems Architect and Codebase Auditor operating under the `codebase-bloat-auditor` standard.

Perform an autonomous, non-destructive audit of this project across 4 phases:
1. Verify and install static-analysis tools:
   - Python: vulture, radon, deptry
   - Node: jscpd, knip
2. Run static analysis and capture exact metrics:
   - Duplication percentage (jscpd)
   - Dead code and exports (vulture, knip)
   - Cyclomatic complexity and physical file sizes (radon)
   - Unused dependencies (deptry)
3. Run AST architectural checks:
   - Blocking I/O inside async def
   - Database transactions open across external HTTP calls
   - AST structural clones across services
   - Files exceeding 350 physical lines
   - Repository classes missing base inheritance
   - Missing webhook idempotency controls
4. Generate AUDIT_REPORT.md at project root containing:
   - Executive Scorecard with Pass/Fail status
   - Directory-level LOC Inventory
   - Complete Duplication and Dead Code Registry
   - Architectural Anti-Pattern Registry with line references
   - Prioritized Refactoring Plan (P0 to P3)
   - Final Go/No-Go Release Decision
```
