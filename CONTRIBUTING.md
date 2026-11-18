# Contributing to Agent Skills

Thank you for contributing to the Agent Skills collection! High-quality skills empower autonomous AI agents to deliver consistent, production-grade results.

## Skill Package Requirements

Every submitted skill must reside inside an appropriate category directory:

```text
<category>/<skill-name>/
├── SKILL.md                 # Mandatory: Agent instruction specification
├── README.md                # Human overview, motivation, and quick start
├── reference.md             # Deep technical documentation and schemas
├── references/              # Prompt templates and supporting resources
└── examples/                # Working code snippets and configuration files
```

### Frontmatter Schema (`SKILL.md`)

The `SKILL.md` file must begin with valid YAML frontmatter:

```yaml
---
name: your-skill-name
description: Concise one-sentence summary of the skill's capabilities and trigger conditions.
license: MIT
metadata:
  author: "Your Name or Org"
  version: "1.0.0"
  domain: "category-domain"
  triggers: "comma-separated list of trigger keywords and user intents"
  role: "Specialist Persona"
  scope: "domain-scope"
  output-format: "expected-output-structure"
---
```

## Quality Checklist

Before submitting a pull request, ensure your skill meets these criteria:
- [ ] **No Generic Fluff:** Provide concrete code, commands, and actionable rules.
- [ ] **Measurable Success Criteria:** Include a verification table or checklist.
- [ ] **Multi-Stack Awareness:** Mention considerations across web, mobile, and backend where applicable.
- [ ] **Validated Frontmatter:** Ensure YAML frontmatter parses without syntax errors.
