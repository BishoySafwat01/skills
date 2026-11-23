# Agent Skills Collection

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Standard: Agent Skills Spec](https://img.shields.io/badge/Standard-Agent%20Skills%20Spec-purple.svg)](https://agentskills.io)
[![Compatible With: Claude Code, Antigravity, Cursor, Codex](https://img.shields.io/badge/Compatible%20With-Claude%20%7C%20Antigravity%20%7C%20Cursor%20%7C%20Codex-emerald.svg)](#)

A curated, enterprise-grade collection of **Agent Skills** designed for autonomous AI agents, coding assistants, and engineering teams. Engineered to adhere strictly to the open **Agent Skills Specification** (`agentskills.io`) popularized by Anthropic's Claude ecosystem.

---

## Repository Architecture

This repository organizes skills hierarchically by **Category / Domain**, housing self-contained skill packages:

```text
skills/
├── .github/
│   └── workflows/
│       └── validate-skills.yml         # CI workflow ensuring compliance with Agent Skills spec
├── LICENSE                             # MIT License
├── README.md                           # Repository index and usage guide
├── CONTRIBUTING.md                     # Skill authoring and submission standards
│
└── <category>/                         # Skill domain category (e.g., performance, architecture)
    └── <skill-name>/                   # Dedicated, self-contained skill package
        ├── SKILL.md                    # [Mandatory] YAML frontmatter + imperative agent instructions
        ├── README.md                   # Human-readable documentation, motivation & benchmarks
        ├── reference.md                # In-depth architectural references & schema definitions
        ├── references/                 # Supporting prompt templates, rubrics & schemas
        │   └── prompt-template.md
        └── examples/                   # Production-tested code implementations across stacks
            ├── react-optimizations.tsx
            ├── database-queries.sql
            └── server-nginx.conf
```

---

## Skills Catalog

| Category | Skill Name | Description | Key Capabilities |
|---|---|---|---|
| **`performance/`** | [`app-performance-optimizer`](performance/app-performance-optimizer) | Full-stack performance engineering covering the **31 production levers**. | WebP/AVIF, Skeletons, Virtualization, Dedup, Debounce, Redis, Indexes, N+1 fixes, OTel, RUM |
| **`quality/`** | [`codebase-bloat-auditor`](quality/codebase-bloat-auditor) | Codebase bloat detection, architectural safety verification, and static analysis. | Duplication check, dead code removal, cyclomatic complexity, AST safety scan, Go/No-Go gates |

---

## How to Use These Skills

### 1. In Claude Code
Clone or link the repository to your skills directory:
```bash
git clone git@github.com:BishoySafwat01/skills.git ~/.claude/skills
```
Or reference a specific skill in your prompt:
```text
Review my app against the `app-performance-optimizer` skill from @BishoySafwat01/skills.
```

### 2. In Google Antigravity & Codex
Copy the skill folder directly into your skills directory:
```bash
cp -r performance/app-performance-optimizer ~/.gemini/skills/
# or for Codex:
cp -r performance/app-performance-optimizer ~/.codex/skills/
```

### 3. In Cursor / Windsurf / ChatGPT
Use the pre-built prompt template from [`references/prompt-template.md`](performance/app-performance-optimizer/references/prompt-template.md):
```markdown
Audit this codebase using the `app-performance-optimizer` standard across all 6 tiers:
1. Frontend Rendering & Asset Optimization
2. Network Delivery & Edge Caching
3. Client State & API Interactions
4. Backend Architecture & Concurrency
5. Database & Query Performance
6. Observability & Real-World Emulation

Deliverables:
- Top 5 bottlenecks with file/line references.
- Production-ready code fixes.
- Before/After Performance Delta Table.
```

---

## The Anatomy of a High-Quality Skill

Every skill in this collection adheres to strict design criteria:
1. **Lightweight Discovery:** Clean YAML frontmatter (`name`, `description`, `triggers`, `metadata`) for token-efficient agent loading.
2. **Progressive Disclosure:** High-level instructions live in `SKILL.md`; deep architectural details reside in `reference.md` and are loaded only when triggered.
3. **Executable Examples:** Concrete code snippets in TypeScript, SQL, Python, and system configurations rather than generic advice.
4. **Verifiable Success Criteria:** Clear deliverables and measurable benchmark rubrics.

---

## Contributing

We welcome additions of new skills adhering to our standards! Please consult [`CONTRIBUTING.md`](CONTRIBUTING.md) for details on the validation schema, directory layout, and review guidelines.

---

## License

This repository is licensed under the [MIT License](LICENSE).
