# Project Context — Portfolio Website

## CEO
- **Name:** Saidul Alam Rahat
- **Role:** Sr. Executive, Business Intelligence @ FundedNext
- **Location:** Dhaka, Bangladesh
- **Working Style:** Delegates, prefers planning first, short direct communication
- **GitHub:** saidulalam01
- **Site:** https://saidulalam01.github.io/

## Project
- **Type:** Static portfolio website with Discord bot content management
- **Repo (private):** portfolio-website
- **Repo (public):** saidulalam01.github.io (GitHub Pages deployment)
- **URL:** https://saidulalam01.github.io/

## Architecture
```
Discord message → bot.py → Claude CLI (AGENT.md prompt) → JSON response
→ data.json mutation → build.py → index.html → git push → GitHub Pages
```

## Tech Stack
- **Build:** Python 3 (pure, zero dependencies) — `build.py`
- **Bot:** Python 3 + discord.py — `bot.py`
- **Frontend:** HTML5, CSS3 (custom properties, dual dark/light theme), vanilla JS
- **Fonts:** Outfit (300–800), JetBrains Mono (Google Fonts)
- **Analytics:** Google Analytics 4 (G-8CERXVPZXC)
- **Forms:** Formspree
- **Deployment:** GitHub Pages (auto on push to main)
- **Service:** macOS LaunchAgent (com.portfolio.bot.plist)
- **Backups:** Timestamped JSON, auto-prune to last 20

## Key Files
| File | Purpose | Owner |
|------|---------|-------|
| `data.json` | Single source of truth for all content | content-editor |
| `build.py` | Generates index.html from data.json (11 renderers) | ui-developer |
| `bot.py` | Discord bot + Claude CLI integration | bot-engineer |
| `script.js` | Theme toggle, animations, case study switcher, lightbox | ui-developer |
| `style.css` | Full design system, dark/light themes, responsive | css-theme-engineer |
| `index.html` | Generated output — NEVER edit directly | (generated) |
| `AGENT.md` | Bot's Claude CLI prompt template | content-editor |
| `sitemap.xml` | Search engine sitemap | seo-optimizer |
| `robots.txt` | Crawler rules | seo-optimizer |

## Case Studies
- 12 slide designs × 12 color palettes = 144 combinations
- Config: `case-studies/_source/slide-config.md`
- Tools: `design-picker.html`, `theme-picker.html`
- Each case study: slides HTML + full document HTML + PDF

## Content Sections (data.json)
meta, nav, hero, about, experience, projects, achievements, certifications, skills, contact, footer

## Hard Constraints
- No paid APIs or services without CEO approval
- All repos private (public repo is clean output only)
- Never edit index.html directly — always go through data.json + build.py
- Never push secrets, .env, or agent system files to public repo
- READ-ONLY mindset: understand before modifying
- All output files saved inside project folder
- QA artifacts → `qa/`, temp files → `tmp/`
