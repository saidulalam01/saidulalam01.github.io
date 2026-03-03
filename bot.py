#!/usr/bin/env python3
"""
Portfolio Website Bot — Discord bot for managing website content.
Receives natural language messages, parses with AI agent CLI,
updates data.json, rebuilds index.html, and pushes to GitHub Pages.
"""

import os
import sys
import json
import re
import shutil
import subprocess
from datetime import datetime
from pathlib import Path

import discord
from discord.ext import commands

ROOT = Path(__file__).parent
DATA_FILE = ROOT / "data.json"
BACKUP_DIR = ROOT / "backups"
AGENT_MD = ROOT / "AGENT.md"
CONVO_LOG = ROOT / "logs" / "conversations.jsonl"

BACKUP_DIR.mkdir(exist_ok=True)
(ROOT / "logs").mkdir(exist_ok=True)


# ── .env loader (works under LaunchAgent, no inherited env) ──────────────────

def load_env():
    """Load .env file into a dict, falling back to os.environ."""
    env = {}
    env_file = ROOT / ".env"
    if env_file.exists():
        for line in env_file.read_text().splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" in line:
                k, v = line.split("=", 1)
                v = v.strip().strip("'\"")
                env[k.strip()] = v
    # Fallback to os.environ for anything not in .env
    for key in ("DISCORD_BOT_TOKEN", "DISCORD_CHANNEL_ID", "AGENT_CLI_PATH"):
        if key not in env:
            env[key] = os.environ.get(key, "")
    return env


ENV = load_env()
BOT_TOKEN = ENV.get("DISCORD_BOT_TOKEN", "")
CHANNEL_ID = int(ENV.get("DISCORD_CHANNEL_ID", "0"))
CLI_PATH = ENV.get("AGENT_CLI_PATH", "")

# Resolve CLI path
if not CLI_PATH:
    for p in ("/Users/saidulalamrahat/.local/bin/claude", "/usr/local/bin/claude"):
        if Path(p).exists():
            CLI_PATH = p
            break


# ── Discord bot setup ────────────────────────────────────────────────────────

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)


async def send_chunked(dest, text):
    """Send message in chunks if it exceeds Discord's 2000 char limit."""
    if len(text) > 1900:
        chunks = [text[i:i + 1900] for i in range(0, len(text), 1900)]
        for chunk in chunks:
            await dest.send(chunk)
    else:
        await dest.send(text)


def is_target_channel(channel_id):
    """Check if message is in our target channel."""
    return channel_id == CHANNEL_ID


# ── AI Agent CLI integration ────────────────────────────────────────────────

def call_agent_cli(prompt):
    """Call the agent CLI subprocess and return parsed JSON response."""
    if not CLI_PATH:
        return None

    # Load AGENT.md context
    agent_context = ""
    if AGENT_MD.exists():
        agent_context = AGENT_MD.read_text()

    # Load current data.json
    current_data = ""
    if DATA_FILE.exists():
        current_data = DATA_FILE.read_text()

    full_prompt = f"""{agent_context}

## Current data.json:
```json
{current_data}
```

## User request:
{prompt}

Respond with ONLY valid JSON. No markdown, no explanation."""

    try:
        modified_env = os.environ.copy()
        modified_env.pop("CLAUDECODE", None)

        result = subprocess.run(
            [CLI_PATH, "-p", full_prompt, "--output-format", "json"],
            capture_output=True,
            text=True,
            timeout=120,
            env=modified_env,
            cwd=str(ROOT),
        )

        if result.returncode != 0:
            print(f"CLI error: {result.stderr}", file=sys.stderr)
            return None

        stdout = result.stdout.strip()
        if not stdout:
            return None

        # --output-format json wraps response in {"result": "..."}
        parsed = extract_json(stdout)
        if parsed and "result" in parsed and isinstance(parsed["result"], str):
            # The actual agent response is inside "result"
            inner = extract_json(parsed["result"])
            if inner:
                return inner
            # Plain text reply from agent
            return {"action": "reply", "text": parsed["result"][:1900]}

        if parsed:
            return parsed

        # Fallback: treat raw output as a text reply
        return {"action": "reply", "text": stdout[:1900]}

    except subprocess.TimeoutExpired:
        print("CLI timeout (120s)", file=sys.stderr)
        return None
    except Exception as e:
        print(f"CLI exception: {e}", file=sys.stderr)
        return None


def extract_json(text):
    """3-tier JSON extraction: direct parse → code block → brace scanning."""
    if not text or not text.strip():
        return None

    text = text.strip()

    # Tier 1: Direct parse
    try:
        return json.loads(text)
    except (json.JSONDecodeError, ValueError):
        pass

    # Tier 2: Markdown code block
    match = re.search(r"```(?:json)?\n(.*?)\n```", text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(1))
        except (json.JSONDecodeError, ValueError):
            pass

    # Tier 3: Brace scanning
    brace_start = text.find("{")
    if brace_start >= 0:
        depth = 0
        for i in range(brace_start, len(text)):
            if text[i] == "{":
                depth += 1
            elif text[i] == "}":
                depth -= 1
                if depth == 0:
                    try:
                        return json.loads(text[brace_start:i + 1])
                    except (json.JSONDecodeError, ValueError):
                        pass
                    break

    return None


# ── Data management ──────────────────────────────────────────────────────────

def log_conversation(user_msg, bot_response, action=None):
    """Log every conversation to JSONL for communication history."""
    entry = {
        "ts": datetime.now().isoformat(),
        "user": user_msg,
        "bot": bot_response[:500] if bot_response else None,
        "action": action,
    }
    with open(CONVO_LOG, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


def load_data():
    """Load current data.json."""
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_data(data):
    """Save data.json with backup."""
    backup_data()
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")


def backup_data():
    """Create timestamped backup of data.json."""
    if DATA_FILE.exists():
        ts = datetime.now().strftime("%Y-%m-%d-%H%M%S")
        dst = BACKUP_DIR / f"data-{ts}.json"
        shutil.copy2(DATA_FILE, dst)
        # Keep only last 20 backups
        backups = sorted(BACKUP_DIR.glob("data-*.json"), reverse=True)
        for old in backups[20:]:
            old.unlink()
        return dst
    return None


def apply_update(response):
    """Apply a parsed CLI response to data.json.

    Expected response format:
    {
        "action": "update",
        "section": "skills",
        "operation": "add|remove|modify",
        "data": { ... changes ... },
        "summary": "Human-readable description of what changed"
    }
    """
    if not response or not isinstance(response, dict):
        return False, "Invalid response from agent"

    action = response.get("action")

    if action == "reply":
        # Agent wants to reply with text, no data change
        return True, response.get("text", response.get("summary", "Done"))

    if action == "error":
        return False, response.get("text", response.get("summary", "Unknown error"))

    if action != "update":
        return False, f"Unknown action: {action}"

    section = response.get("section")
    operation = response.get("operation")
    new_data = response.get("data")

    if not section:
        return False, "No section specified"
    if not operation:
        return False, "No operation specified"

    data = load_data()

    if section not in data:
        return False, f"Unknown section: {section}"

    try:
        if operation == "replace_section":
            # Full section replacement
            data[section] = new_data
        elif operation == "add":
            # Add item to a list within the section
            target_key = response.get("target_key", "items")
            if target_key in data[section] and isinstance(data[section][target_key], list):
                if isinstance(new_data, list):
                    data[section][target_key].extend(new_data)
                else:
                    data[section][target_key].append(new_data)
            else:
                return False, f"Cannot add to {section}.{target_key}"
        elif operation == "remove":
            target_key = response.get("target_key", "items")
            item_id = response.get("item_id")
            if target_key in data[section] and isinstance(data[section][target_key], list):
                data[section][target_key] = [
                    item for item in data[section][target_key]
                    if item.get("id") != item_id
                ]
            else:
                return False, f"Cannot remove from {section}.{target_key}"
        elif operation == "modify":
            target_key = response.get("target_key", "items")
            item_id = response.get("item_id")
            if target_key in data[section] and isinstance(data[section][target_key], list):
                for i, item in enumerate(data[section][target_key]):
                    if item.get("id") == item_id:
                        item.update(new_data)
                        break
                else:
                    return False, f"Item {item_id} not found in {section}.{target_key}"
            elif isinstance(data[section], dict) and new_data:
                data[section].update(new_data)
            else:
                return False, f"Cannot modify {section}.{target_key}"
        elif operation == "replace_full":
            # Replace entire data.json
            data = new_data
        else:
            return False, f"Unknown operation: {operation}"

        save_data(data)
        return True, response.get("summary", "Updated successfully")

    except Exception as e:
        return False, f"Apply error: {e}"


# ── Build & Deploy ───────────────────────────────────────────────────────────

def run_build():
    """Run build.py to regenerate index.html."""
    try:
        result = subprocess.run(
            [sys.executable, str(ROOT / "build.py")],
            capture_output=True,
            text=True,
            timeout=30,
            cwd=str(ROOT),
        )
        if result.returncode != 0:
            return False, f"Build failed: {result.stderr}"
        # Verify output exists
        if not (ROOT / "index.html").exists():
            return False, "Build produced no index.html"
        return True, result.stdout.strip()
    except Exception as e:
        return False, f"Build error: {e}"


def git_push(summary):
    """Commit and push changes to both private (origin) and public repos."""
    try:
        # Stage all tracked files (goes to private repo)
        subprocess.run(["git", "add", "-A"], cwd=str(ROOT), check=True)

        # Check if there are changes to commit
        result = subprocess.run(
            ["git", "diff", "--cached", "--quiet"],
            cwd=str(ROOT),
            capture_output=True,
        )
        if result.returncode == 0:
            return True, "No changes to push"

        # Commit
        commit_msg = summary[:72] if len(summary) > 72 else summary
        subprocess.run(
            ["git", "commit", "-m", commit_msg],
            cwd=str(ROOT),
            check=True,
            capture_output=True,
        )

        # Push to private repo (origin — full backup)
        subprocess.run(
            ["git", "push", "origin", "main"],
            cwd=str(ROOT),
            check=True,
            capture_output=True,
            timeout=30,
        )

        # Push to public repo (public — deploys GitHub Pages)
        subprocess.run(
            ["git", "push", "public", "main"],
            cwd=str(ROOT),
            check=True,
            capture_output=True,
            timeout=30,
        )
        return True, f"Pushed: {commit_msg}"
    except subprocess.CalledProcessError as e:
        return False, f"Git error: {e.stderr if e.stderr else str(e)}"
    except Exception as e:
        return False, f"Push error: {e}"


def rollback():
    """Revert the last commit."""
    try:
        subprocess.run(
            ["git", "revert", "HEAD", "--no-edit"],
            cwd=str(ROOT),
            check=True,
            capture_output=True,
        )
        subprocess.run(
            ["git", "push"],
            cwd=str(ROOT),
            check=True,
            capture_output=True,
            timeout=30,
        )
        # Restore data.json from latest backup
        backups = sorted(BACKUP_DIR.glob("data-*.json"), reverse=True)
        if backups:
            shutil.copy2(backups[0], DATA_FILE)
        return True, "Reverted last commit and pushed"
    except Exception as e:
        return False, f"Rollback error: {e}"


# ── Bot commands ─────────────────────────────────────────────────────────────

@bot.event
async def on_ready():
    print(f"Portfolio bot connected as {bot.user}", file=sys.stderr)


@bot.command(name="help")
async def cmd_help(ctx):
    """Show available commands."""
    if not is_target_channel(ctx.channel.id):
        return
    help_text = """**Portfolio Website Bot**

**Natural language** — just type what you want to change
Examples:
- "add a new skill: Tableau, advanced, in Visualization group"
- "update my title to Lead BI Analyst"
- "add a new certification: AWS Cloud Practitioner, Dec 2025"
- "remove the Fun Projects card"

**Commands:**
`!status` — show current content summary
`!preview <message>` — dry-run, show what would change
`!push` — manually push current state to GitHub
`!undo` — revert last commit
`!help` — this message"""
    await ctx.send(help_text)


@bot.command(name="status")
async def cmd_status(ctx):
    """Show current content summary."""
    if not is_target_channel(ctx.channel.id):
        return
    try:
        data = load_data()
        lines = ["**Current Website Content:**"]
        lines.append(f"- **Experience**: {len(data.get('experience', {}).get('items', []))} positions")
        lines.append(f"- **Projects**: 1 featured + {len(data.get('projects', {}).get('cards', []))} cards + {len(data.get('projects', {}).get('portfolio', []))} portfolio")
        lines.append(f"- **Achievements**: {len(data.get('achievements', {}).get('items', []))} items")
        lines.append(f"- **Certifications**: {len(data.get('certifications', {}).get('items', []))} items")
        lines.append(f"- **Skill Groups**: {len(data.get('skills', {}).get('groups', []))} groups")
        total_skills = sum(len(g.get("pills", [])) for g in data.get("skills", {}).get("groups", []))
        lines.append(f"- **Total Skills**: {total_skills}")
        lines.append(f"- **Contact**: {data.get('contact', {}).get('email', 'N/A')}")
        await ctx.send("\n".join(lines))
    except Exception as e:
        await ctx.send(f"Error reading data: {e}")


@bot.command(name="preview")
async def cmd_preview(ctx, *, message: str = ""):
    """Dry-run: show what would change without applying."""
    if not is_target_channel(ctx.channel.id):
        return
    if not message:
        await ctx.send("Usage: `!preview <what you want to change>`")
        return

    async with ctx.typing():
        response = call_agent_cli(message)

    if not response:
        await ctx.send("Could not parse the request. Try rephrasing.")
        return

    preview = f"**Preview (not applied):**\n"
    preview += f"- Action: `{response.get('action', 'unknown')}`\n"
    preview += f"- Section: `{response.get('section', 'N/A')}`\n"
    preview += f"- Operation: `{response.get('operation', 'N/A')}`\n"
    preview += f"- Summary: {response.get('summary', 'N/A')}\n"
    if response.get("data"):
        data_str = json.dumps(response["data"], indent=2, ensure_ascii=False)
        if len(data_str) > 1200:
            data_str = data_str[:1200] + "\n..."
        preview += f"```json\n{data_str}\n```"

    await send_chunked(ctx, preview)


@bot.command(name="push")
async def cmd_push(ctx):
    """Manually push current state to GitHub."""
    if not is_target_channel(ctx.channel.id):
        return
    async with ctx.typing():
        ok, msg = run_build()
        if not ok:
            await ctx.send(f"Build failed: {msg}")
            return
        ok, msg = git_push("Manual push via bot")
    await ctx.send(f"{'Done' if ok else 'Failed'}: {msg}")


@bot.command(name="undo")
async def cmd_undo(ctx):
    """Revert the last commit."""
    if not is_target_channel(ctx.channel.id):
        return
    async with ctx.typing():
        ok, msg = rollback()
    await ctx.send(f"{'Done' if ok else 'Failed'}: {msg}")


# ── Natural language handler ─────────────────────────────────────────────────

@bot.event
async def on_message(message):
    # Ignore bot's own messages
    if message.author == bot.user:
        return

    # Process commands first
    await bot.process_commands(message)

    # Only handle natural language in target channel (not commands)
    if not is_target_channel(message.channel.id):
        return
    if message.content.startswith("!"):
        return

    user_msg = message.content.strip()
    if not user_msg:
        return

    # Natural language update flow
    async with message.channel.typing():
        # 1. Call agent CLI
        response = call_agent_cli(user_msg)

    if not response:
        reply = "Could not understand the request. Try rephrasing or use `!help`."
        log_conversation(user_msg, reply, "no_parse")
        await message.channel.send(reply)
        return

    # If agent just wants to reply (no update needed)
    if response.get("action") == "reply":
        reply = response.get("text", response.get("summary", "Done"))
        log_conversation(user_msg, reply, "reply")
        await send_chunked(message.channel, reply)
        return

    if response.get("action") == "error":
        reply = f"Error: {response.get('text', response.get('summary', 'Unknown'))}"
        log_conversation(user_msg, reply, "error")
        await message.channel.send(reply)
        return

    async with message.channel.typing():
        # 2. Apply update
        ok, summary = apply_update(response)
        if not ok:
            log_conversation(user_msg, f"Update failed: {summary}", "update_failed")
            await message.channel.send(f"Update failed: {summary}")
            return

        # 3. Rebuild HTML
        ok, build_msg = run_build()
        if not ok:
            log_conversation(user_msg, f"Build failed: {build_msg}", "build_failed")
            await message.channel.send(f"Build failed: {build_msg}\nData was saved. Use `!push` after fixing.")
            return

        # 4. Git push
        commit_summary = response.get("summary", summary)
        ok, push_msg = git_push(commit_summary)

    if ok:
        reply = f"Done: {commit_summary}\nSite will update in ~1 min."
        log_conversation(user_msg, reply, "update_pushed")
        await message.channel.send(reply)
    else:
        reply = f"Updated locally but push failed: {push_msg}\nUse `!push` to retry."
        log_conversation(user_msg, reply, "push_failed")
        await message.channel.send(reply)


# ── Main ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    if not BOT_TOKEN:
        print("ERROR: DISCORD_BOT_TOKEN not set in .env", file=sys.stderr)
        sys.exit(1)
    if not CHANNEL_ID:
        print("ERROR: DISCORD_CHANNEL_ID not set in .env", file=sys.stderr)
        sys.exit(1)
    bot.run(BOT_TOKEN)
