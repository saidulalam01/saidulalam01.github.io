# Portfolio Website + Management Bot

Personal portfolio website with an automated Discord bot for content management.

## Live Site
https://saidulalam01.github.io/

## Architecture

```
Discord message → bot.py → AI agent CLI → structured JSON
  → updates data.json → build.py regenerates index.html
  → git commit + push → GitHub Pages deploys automatically
```

### Two Repos
- **Private** (`portfolio-website`) — everything: bot code, data, configs, website files
- **Public** (`saidulalam01.github.io`) — website files only, deployed via GitHub Pages

## Files

| File | Purpose |
|------|---------|
| `index.html` | Generated website (do NOT edit manually) |
| `style.css` | Website styles |
| `script.js` | Website interactions (scroll, lightbox, theme toggle) |
| `data.json` | All website content — single source of truth |
| `build.py` | Reads data.json → generates index.html (pure Python, zero deps) |
| `bot.py` | Discord bot — receives messages, calls AI agent CLI, applies updates |
| `AGENT.md` | Prompt instructions for the AI agent CLI subprocess |
| `setup.sh` | Install dependencies + LaunchAgent |
| `requirements.txt` | Python dependencies (discord.py) |
| `.env` | Tokens (DISCORD_BOT_TOKEN, DISCORD_CHANNEL_ID) — never committed |
| `.env.example` | Template for .env |
| `launchd/` | macOS LaunchAgent plist (auto-start, keep-alive) |
| `backups/` | Auto-backups of data.json before every update |
| `logs/` | Bot logs + conversation history |

## Discord Bot Commands

| Command | Description |
|---------|-------------|
| (natural language) | Type any update request — AI parses and applies it |
| `!status` | Show current content summary |
| `!preview <msg>` | Dry-run — show what would change |
| `!push` | Manually push current state |
| `!undo` | Revert last commit |
| `!help` | Show all commands |

**Examples:**
- "add a new skill: Tableau, advanced, in Visualization group"
- "update my title to Lead BI Analyst"
- "add a new certification: AWS Cloud Practitioner, Dec 2025"

## Setup (after restore)

1. Copy `.env.example` to `.env` and fill in tokens
2. Run `bash setup.sh`
3. Verify: `launchctl list | grep portfolio`
4. Check logs: `tail -f logs/bot-stderr.log`

## Manual Operations

```bash
# Rebuild website from data.json
python3 build.py

# Start bot manually (for debugging)
python3 bot.py

# Check bot status
launchctl list | grep portfolio

# Restart bot
launchctl bootout gui/$(id -u) ~/Library/LaunchAgents/com.portfolio.bot.plist
launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/com.portfolio.bot.plist
```

## Auto-Sync
This repo auto-syncs to GitHub every 12 hours via LaunchAgent (`com.agents.sync`).
