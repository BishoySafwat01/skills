# Codebase Bloat Auditor Skill

A production-grade Agent Skill for static analysis, codebase debloating, architectural consistency, and concurrency safety verification. Designed for full-stack monorepos using Python (FastAPI/SQLAlchemy) and TypeScript (React/Node).

## Overview

As projects scale and multiple engineers or AI agents contribute to a codebase, common anti-patterns emerge:
- Unchecked code duplication across service layers and API routes.
- Accumulation of dead functions, stale imports, and unused dependencies.
- Concurrency bugs such as blocking I/O inside asynchronous functions.
- Dangerous database patterns like keeping transactions open during third-party HTTP requests.
- Growing "god files" that exceed healthy cognitive and maintenance limits.

This skill equips AI agents (Claude Code, Antigravity, Cursor, Codex) and engineering teams with an automated, 4-phase audit protocol to detect, catalog, and resolve bloat systematically.

## The 4-Phase Audit Workflow

1. **Tool Installation**: Verifies and installs required static-analysis engines (`vulture`, `radon`, `deptry`, `jscpd`, `knip`).
2. **Static Analysis**: Gathers objective metrics on code duplication, dead code, cyclomatic complexity, and unused dependencies.
3. **Deep AST Scan**: Analyzes Python Abstract Syntax Trees for asynchronous safety, database session boundaries, repository inheritance, and webhook idempotency.
4. **Actionable Reporting**: Produces an executive `AUDIT_REPORT.md` with prioritized remediation steps and a formal Go/No-Go release gate.

## Quick Usage

### For AI Coding Agents
Trigger the skill in Claude Code, Antigravity, or Codex:

```text
Run an audit on this project using the codebase-bloat-auditor skill and produce AUDIT_REPORT.md.
```

Or copy the prompt template from [`references/prompt-template.md`](references/prompt-template.md).

### Acceptance Thresholds

| Metric | Target Standard | Rejection Threshold |
|:-------|:---------------|:--------------------|
| Code Duplication (`jscpd`) | Below 3.0% | Greater than 5.0% |
| Dead Functions (`vulture`, `knip`) | 0 findings | Any unreferenced symbols |
| Cyclomatic Complexity (`radon`) | Grade A or B (average < 8) | Grade D, E, or F functions |
| File Length | Max 350 physical lines | Files exceeding 350 lines |
| Async Safety | 0 blocking calls in `async def` | Any blocking call detected |
| Database Safety | 0 open sessions during external HTTP | Any external HTTP in transaction |

## Directory Structure

```text
codebase-bloat-auditor/
├── SKILL.md                 # Agent instruction specification and executable rules
├── README.md                # Human-readable documentation and quickstart
├── reference.md             # In-depth architectural rules and design patterns
├── references/
│   └── prompt-template.md   # Ready-to-use prompt for auditing any repository
└── examples/
    └── verify_architecture.py # AST architectural verifier script
```
