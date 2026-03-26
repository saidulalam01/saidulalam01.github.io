# Agent Hierarchy — Portfolio Website

## Structure

```
CEO (Saidul Alam Rahat)
  │
  President
  │
  ├── Frontend Lead (3 specialists)
  │   ├── ui-developer
  │   ├── css-theme-engineer
  │   └── case-study-designer
  │
  ├── Content & SEO Lead (2 specialists)
  │   ├── content-editor
  │   └── seo-optimizer
  │
  └── DevOps Lead (2 specialists)
      ├── bot-engineer
      └── deploy-specialist
```

**Total: 1 President + 3 Team Leads + 7 Specialists = 11 agents**

## Communication Rules

| From | To | Allowed |
|------|----|---------|
| CEO | President | Always |
| President | Team Lead | Always |
| Team Lead | Team Lead | Yes (direct coordination) |
| Specialist | Specialist (same team) | Yes |
| Specialist | Specialist (cross-team) | Yes (lead informed) |
| Specialist | President | Only if lead blocked |
| Anyone | CEO | Never (President only) |

## Task Flows

### Simple Task (single domain)
```
CEO → President → Specialist → President → CEO
```

### Complex Task (multi-domain)
```
CEO → President → Lead(s) → Specialists → Lead(s) → President → CEO
```

### Cross-Team Example: New Case Study
```
CEO → President → Frontend Lead + Content & SEO Lead
                       │                    │
              case-study-designer    content-editor
              (slides + document)   (data.json entry)
                       │                    │
                  Frontend Lead + Content & SEO Lead (consolidate)
                                    │
                                President → CEO
```

## Team Responsibilities

| Team | Scope |
|------|-------|
| **Frontend** | HTML structure, CSS design system, JS interactions, case study slides, responsive layout, animations |
| **Content & SEO** | data.json content, AGENT.md prompt, meta tags, OG/Twitter, sitemap, GA, search ranking |
| **DevOps** | Discord bot, Claude CLI integration, git push, GitHub Pages, launchd, backups, .env |
