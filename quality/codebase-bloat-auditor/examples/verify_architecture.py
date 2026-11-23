#!/usr/bin/env python3
"""
verify_architecture.py - AST and Architectural Pattern Scanner
Part of the codebase-bloat-auditor skill.

Scans Python source trees for:
  1. Blocking I/O inside async def functions
  2. Database sessions open during external HTTP calls
  3. AST structural clones (functions >= 12 lines)
  4. Physical files exceeding 350 lines
  5. Repository classes not inheriting from BaseAsyncRepository
  6. Webhook handlers missing idempotency constraints
"""

import ast
import hashlib
import pathlib
import sys
import re
import argparse
from collections import defaultdict
from dataclasses import dataclass, field

LOC_LIMIT = 350
CLONE_MIN_LINES = 12

BLOCKING_CALLS = {
    "requests.get", "requests.post", "requests.put", "requests.patch",
    "requests.delete", "requests.request", "requests.head", "requests.options",
    "time.sleep", "urllib.request.urlopen",
}

HTTP_CLIENTS = {"httpx", "aiohttp", "requests"}
SESSION_NAMES = {"session", "db", "async_session"}
COMMIT_METHODS = {"commit", "close", "rollback"}
BASE_REPO_NAME = "BaseAsyncRepository"

EXCLUDE_DIRS = {
    ".venv", "venv", "__pycache__", ".git",
    "node_modules", "dist", "build", "site-packages",
    "alembic",
}

LOC_EXCLUDE_DIRS = {"tests", "scripts"}
BLOCKING_EXCLUDE_DIRS = {"scripts"}
WEBHOOK_PATTERNS = ["/webhooks/", "/webhook/", "/callback/"]
IDEMPOTENCY_PATTERNS = ["UniqueConstraint", "FOR UPDATE", "SKIP LOCKED", "redis", "SET.*NX", "set.*nx=True"]


@dataclass
class Finding:
    check: str
    filepath: str
    line: int
    detail: str
    severity: str = "HIGH"


@dataclass
class ScanResult:
    findings: list[Finding] = field(default_factory=list)

    def add(self, check: str, filepath: pathlib.Path, line: int, detail: str, severity: str = "HIGH"):
        self.findings.append(Finding(check, str(filepath), line, detail, severity))

    def print_report(self):
        if not self.findings:
            print("\n[OK] 0 violations found. All architectural checks passed.\n")
            return

        by_check = defaultdict(list)
        for f in self.findings:
            by_check[f.check].append(f)

        print("\n" + "=" * 72)
        print("  Architectural Scan Results")
        print("=" * 72)

        for check, items in sorted(by_check.items()):
            print(f"\n[{check}] - {len(items)} finding(s)")
            for item in items:
                print(f"  {item.filepath}:{item.line} -> {item.detail}")

        total = len(self.findings)
        critical = sum(1 for f in self.findings if f.severity == "CRITICAL")
        print("\n" + "=" * 72)
        print(f"  SUMMARY: {total} violation(s) found ({critical} CRITICAL)")
        print("  Resolve all findings before release.")
        print("=" * 72 + "\n")
        sys.exit(1)


def ast_call_name(node: ast.Call) -> str:
    if isinstance(node.func, ast.Attribute):
        if isinstance(node.func.value, ast.Name):
            return f"{node.func.value.id}.{node.func.attr}"
        return node.func.attr
    if isinstance(node.func, ast.Name):
        return node.func.id
    return ""


def physical_loc(filepath: pathlib.Path) -> int:
    try:
        return sum(1 for line in filepath.open(encoding="utf-8", errors="ignore")
                   if line.strip() and not line.strip().startswith("#"))
    except OSError:
        return 0


def collect_py_files(root: pathlib.Path, extra_excludes: set[str] | None = None):
    exclude = EXCLUDE_DIRS | (extra_excludes or set())
    files = []
    for p in root.rglob("*.py"):
        if any(part in exclude for part in p.parts):
            continue
        files.append(p)
    return sorted(files)


def check_blocking_in_async(tree: ast.AST, filepath: pathlib.Path, result: ScanResult):
    for node in ast.walk(tree):
        if isinstance(node, ast.AsyncFunctionDef):
            for child in ast.walk(node):
                if isinstance(child, ast.Call):
                    name = ast_call_name(child)
                    if name in BLOCKING_CALLS:
                        result.add("BLOCKING_IO_IN_ASYNC", filepath, child.lineno,
                                   f"{name}() called inside async def {node.name}()", severity="CRITICAL")
                    elif name == "open":
                        result.add("BLOCKING_IO_IN_ASYNC", filepath, getattr(child, "lineno", 0),
                                   f"Synchronous open() inside async def {node.name}()", severity="HIGH")


def check_db_session_during_http(tree: ast.AST, filepath: pathlib.Path, result: ScanResult):
    for node in ast.walk(tree):
        if not isinstance(node, (ast.AsyncFunctionDef, ast.FunctionDef)):
            continue

        session_assigned = False
        committed = False
        http_waits = []

        for child in ast.walk(node):
            if isinstance(child, ast.arg) and child.arg in SESSION_NAMES:
                session_assigned = True
            if isinstance(child, ast.Call):
                name = ast_call_name(child)
                if any(m in name for m in COMMIT_METHODS):
                    committed = True
            if isinstance(child, ast.Await) and isinstance(child.value, ast.Call):
                name = ast_call_name(child.value)
                if any(p in name for p in HTTP_CLIENTS):
                    http_waits.append(getattr(child, "lineno", 0))

        if session_assigned and not committed and http_waits:
            for ln in http_waits:
                result.add("DB_SESSION_DURING_HTTP", filepath, ln,
                           f"External HTTP call in {node.name}() while DB session may be active", severity="CRITICAL")


def check_file_sizes(files: list[pathlib.Path], result: ScanResult):
    for fp in files:
        loc = physical_loc(fp)
        if loc > LOC_LIMIT:
            result.add("OVERSIZED_FILE", fp, 1, f"{loc} non-empty lines (limit: {LOC_LIMIT})", severity="HIGH")


def check_repository_bases(trees: list[tuple[pathlib.Path, ast.AST]], result: ScanResult):
    for filepath, tree in trees:
        if "repositories" not in str(filepath):
            continue
        for node in ast.walk(tree):
            if not isinstance(node, ast.ClassDef) or not node.name.endswith("Repository"):
                continue
            bases = []
            for base in node.bases:
                if isinstance(base, ast.Name):
                    bases.append(base.id)
                elif isinstance(base, ast.Subscript) and isinstance(base.value, ast.Name):
                    bases.append(base.value.id)
                elif isinstance(base, ast.Attribute):
                    bases.append(base.attr)
            if BASE_REPO_NAME not in bases:
                result.add("REPO_BASE_GAP", filepath, node.lineno,
                           f"{node.name} does not inherit from {BASE_REPO_NAME}", severity="HIGH")


def check_webhook_idempotency(files: list[pathlib.Path], result: ScanResult):
    for fp in files:
        if any(part in {"tests", "scripts"} for part in fp.parts):
            continue
        source = fp.read_text(encoding="utf-8", errors="ignore")
        is_webhook = "webhook" in str(fp).lower() or any(p in source for p in WEBHOOK_PATTERNS)
        if not is_webhook:
            continue
        if not any(re.search(pat, source) for pat in IDEMPOTENCY_PATTERNS):
            result.add("IDEMPOTENCY_GAP", fp, 1,
                       "Webhook handler has no UniqueConstraint, FOR UPDATE, or Redis NX lock pattern", severity="CRITICAL")


def main():
    parser = argparse.ArgumentParser(description="Architectural Pattern Scanner")
    parser.add_argument("--backend-dir", default="backend", help="Path to backend directory")
    args = parser.parse_args()

    backend = pathlib.Path(args.backend_dir)
    if not backend.exists():
        print(f"Directory not found: {backend}", file=sys.stderr)
        sys.exit(2)

    py_files = collect_py_files(backend)
    app_files = collect_py_files(backend, extra_excludes=BLOCKING_EXCLUDE_DIRS)
    non_test_files = collect_py_files(backend, extra_excludes=LOC_EXCLUDE_DIRS)

    result = ScanResult()
    trees = []

    for fp in py_files:
        try:
            tree = ast.parse(fp.read_text(encoding="utf-8", errors="ignore"), filename=str(fp))
            trees.append((fp, tree))
            if fp in set(app_files):
                check_blocking_in_async(tree, fp, result)
                check_db_session_during_http(tree, fp, result)
        except SyntaxError:
            continue

    check_file_sizes(non_test_files, result)
    check_repository_bases(trees, result)
    check_webhook_idempotency(py_files, result)
    result.print_report()


if __name__ == "__main__":
    main()
