---
name: codebase-bloat-auditor
description: Audits codebases for architectural anti-patterns, dead code, bloat, async and database safety violations, and code duplication. Runs static-analysis tooling, executes an AST scanner, and produces a structured AUDIT_REPORT.md with a Go/No-Go release verdict. Use when checking code quality before release, enforcing file-size limits, detecting bloat, or auditing monorepos.
license: MIT
metadata:
  author: "BishoySafwat01"
  version: "1.0.0"
  domain: "code-quality"
  triggers: "audit the codebase, check for bloat, run code quality, code quality audit, run audit, bloat check"
  role: "Principal Systems Architect and Codebase Auditor"
  scope: "fullstack-monorepo"
  output-format: "AUDIT_REPORT.md"
---

# Codebase Bloat Auditor

An automated, 4-phase codebase quality enforcement system. It installs static analysis tools, runs duplication and dead-code scans, executes a deep AST architectural scan, and produces a structured `AUDIT_REPORT.md` with an actionable refactoring plan and a Go/No-Go release verdict.

---

## Prime Directive

> **"Measure first. Never guess. Report exact file paths and line numbers."**

This skill is non-destructive by default. Do not modify, patch, or delete application code during a scan run. Every finding must be backed by tool output, file path, or AST node evidence.

---

## Phase 1: Tool Installation

Install static analysis tools before running any check. Skip tools already present in the environment.

### Backend (Python)
```bash
pip install --quiet vulture radon deptry
```

### Frontend (Node.js)
```bash
npm install --save-dev jscpd knip 2>/dev/null || npx --yes jscpd --version
```

If a tool fails to install, log the warning and continue with the remaining tools.

---

## Phase 2: Static Analysis Runs

Execute each check and capture numeric metrics. Save all reports to `./audit_reports/`.

```bash
mkdir -p ./audit_reports
```

### 2a. Cross-Stack Duplication (Backend + Frontend)
```bash
npx --yes jscpd backend/ frontend/src/ \
  --min-lines 10 --min-tokens 50 \
  --reporters consoleFull,json \
  --output ./audit_reports
```
Record: Duplication percentage, duplicate blocks, line ranges.

### 2b. Dead Python Code
```bash
vulture backend/ --min-confidence 80
```
Record: Unused functions, classes, imports, and variables with file and line references.

### 2c. Cyclomatic Complexity and Maintainability
```bash
radon cc backend/ -a -nc   # Cyclomatic complexity: flag grades D, E, and F
radon raw backend/ -s       # Physical LOC per file: flag files > 350 lines
```
Record: Average complexity grade, list of files exceeding 350 LOC.

### 2d. Unused Python Dependencies
```bash
deptry backend/
```
Record: Obsolete, missing, or misclassified dependencies.

### 2e. Dead Frontend Code and Exports
```bash
cd frontend && npx --yes knip --reporter compact
```
Record: Unused exports, files, and types with file paths.

---

## Phase 3: Deep AST and Architectural Pattern Scan

Execute the architectural verifier `scripts/verify_architecture.py` (see reference: `references/verify_architecture.md`) against the backend codebase:

| Check | Target Pattern | Threshold |
|:------|:---------------|:----------|
| **Blocking I/O in Async** | `requests.*`, `time.sleep`, sync file I/O inside `async def` | 0 violations |
| **Open DB Session During HTTP** | External HTTP calls (`httpx`, `aiohttp`) inside open transactions | 0 violations |
| **AST Structural Clones** | Functions >= 12 lines with identical AST node type sequences | 0 duplicate pairs |
| **Oversized Files** | Files exceeding 350 physical lines | <= 350 LOC per file |
| **Repository Base Inheritance** | Repository classes not inheriting from `BaseAsyncRepository` | 0 uninherited classes |
| **Webhook Idempotency** | Webhook handlers lacking unique constraints or atomic lock patterns | 0 unprotected endpoints |

Run command:
```bash
python3 scripts/verify_architecture.py 2>&1 | tee audit_reports/architecture_scan.txt
```

---

## Phase 4: Generate AUDIT_REPORT.md

Produce `AUDIT_REPORT.md` at the project root following this exact structure:

```markdown
# Monorepo Codebase Audit Report
**Date:** <ISO-8601 timestamp>
**Auditor:** Automated Codebase Bloat Auditor Skill

---

## 1. Executive Scorecard

| Metric | Actual | Target | Status |
|:-------|:------:|:------:|:------:|
| Copy-Paste Duplication | X.X% | < 3.0% | PASS / FAIL |
| Dead Python Functions | N | 0 | PASS / FAIL |
| Dead Frontend Exports | N | 0 | PASS / FAIL |
| Avg Cyclomatic Complexity | Grade X | A or B | PASS / FAIL |
| Files > 350 LOC | N | 0 | PASS / FAIL |
| Blocking Calls in async def | N | 0 | PASS / FAIL |
| DB Sessions During HTTP Calls | N | 0 | PASS / FAIL |

**Overall Verdict:** PASS / NEEDS WORK / CRITICAL -- DO NOT MERGE

---

## 2. Code Volume vs. Target Budget

| Directory | Current LOC | Target Budget | Delta |
|:----------|------------:|:-------------:|:-----:|
| Backend APIs | | Within target | |
| Backend Services | | Within target | |
| Backend Repositories | | Within target | |
| Backend Models | | Within target | |
| Frontend Source | | Within target | |

---

## 3. Duplication and Dead Code Registry

### 3a. Duplicated Blocks (jscpd)
| File A | Range A | File B | Range B | Duplicate Lines |
|:-------|:-------:|:-------|:-------:|:---------------:|

### 3b. Dead Python Symbols (vulture)
| File | Line | Symbol | Confidence |
|:-----|:----:|:-------|:----------:|

### 3c. Dead Frontend Exports (knip)
| File | Symbol | Type |
|:-----|:-------|:----:|

---

## 4. Architectural Anti-Pattern Registry

### 4a. Async and Database Safety Violations
| File | Line | Violation Description | Severity |
|:-----|:----:|:---------------------|:--------:|

### 4b. Oversized Files (> 350 LOC)
| File | Actual LOC | Recommended Split Strategy |
|:-----|:----------:|:---------------------------|

### 4c. Repository Pattern and Idempotency Gaps
| Target Component | Issue | Severity |
|:-----------------|:------|:--------:|

---

## 5. Refactoring Execution Plan

Ordered by impact-to-effort ratio. Resolve P0 and P1 before proceeding to lower priorities:

| Priority | Action | Target Files | Expected LOC Reduction |
|:--------:|:-------|:-------------|:----------------------:|
| P0 -- Critical | | | |
| P1 -- High | | | |
| P2 -- Medium | | | |
| P3 -- Low | | | |

---

## 6. Acceptance Gate Summary

| Gate | Tool | Threshold | Result |
|:-----|:-----|:----------|:------:|
| Duplication | jscpd | < 3.0% | |
| Dead Python | vulture | 0 findings | |
| Dead Frontend | knip | 0 findings | |
| Complexity | radon cc | Grade A/B avg | |
| Max File Size | radon raw | <= 350 LOC | |
| Async Safety | verify_architecture.py | 0 violations | |
| DB Safety | verify_architecture.py | 0 violations | |

**Release Decision:** GO / NO-GO
```

---

## Architectural Rules Reference

For full architectural contracts, design patterns, and code examples, consult:
- `reference.md`
- `references/prompt-template.md`
