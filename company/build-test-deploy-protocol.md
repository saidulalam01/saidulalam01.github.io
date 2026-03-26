# Build-Test-Deploy Protocol — Portfolio Website

## Pipeline

```
EDIT → BUILD → QA → DEPLOY → VERIFY
```

## Stage 1: EDIT
**Who:** Relevant specialist (content-editor, ui-developer, css-theme-engineer, etc.)
- Make changes to source files (data.json, build.py, style.css, script.js, case study HTML)
- NEVER edit index.html directly

## Stage 2: BUILD
**Who:** ui-developer or any agent with build access
```bash
cd /Users/saidulalamrahat/work/Claude-Company-Work/github-projects/saidulalam01.github.io
python3 build.py
```
- Verify output: "Built index.html (XXXXX bytes)"
- Confirm no errors or warnings

## Stage 3: QA
**Who:** Responsible lead (per qa-protocol.md)
- Run through QA checklist
- Generate QA report
- **Gate:** Must PASS or PASS WITH WARNINGS before deploy
- **FAIL → fix issues → rebuild → re-QA**

## Stage 4: DEPLOY
**Who:** deploy-specialist
```bash
# Commit changes
git add data.json build.py index.html style.css script.js [other changed files]
git commit -m "Brief description of change"

# Push to origin (private repo)
git push origin main

# Push to public repo (GitHub Pages)
git push public main
```
- Never push: `.env`, `company/`, `agents/`, `sessions/`, `backups/`, `logs/`
- Always verify `.gitignore` is correct before pushing

## Stage 5: VERIFY
**Who:** deploy-specialist
- Check https://saidulalam01.github.io/ loads (allow ~1 min for GitHub Pages)
- Verify changes are visible
- Check browser console for errors
- Confirm on mobile if responsive changes were made

## Hard Stops (CEO Approval Required)
- First deploy after major structural changes
- Case study additions or removals
- Changes affecting SEO (meta, sitemap, robots.txt)
- Any changes to bot.py that affect the live Discord bot
- LaunchAgent service restarts

## Bot-Driven Updates (Automated Pipeline)
When updates come through the Discord bot:
```
Discord message → bot.py → Claude CLI → JSON → data.json mutation
→ build.py → index.html → git commit → dual push → GitHub Pages
```
This pipeline is fully automated. Manual intervention only needed if:
- Build fails
- QA gate fails
- Git push fails
- Bot crashes

## Rollback
```bash
# Via bot
!undo

# Manual
git revert HEAD
python3 build.py
git push origin main
git push public main
```
