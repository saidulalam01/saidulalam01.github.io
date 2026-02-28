#!/bin/bash
# Portfolio Website Bot — Setup Script
# Installs dependencies and configures LaunchAgent

set -e

PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
LAUNCH_AGENTS_DIR="$HOME/Library/LaunchAgents"

echo "=== Portfolio Website Bot Setup ==="
echo "Project: $PROJECT_DIR"
echo ""

# 1. Install Python dependencies
echo "[1/4] Installing Python dependencies..."
pip3 install --quiet discord.py
echo "  Done."

# 2. Create directories
echo "[2/4] Creating directories..."
mkdir -p "$PROJECT_DIR/backups"
mkdir -p "$PROJECT_DIR/logs"
echo "  Done."

# 3. Check .env
echo "[3/4] Checking configuration..."
if [ ! -f "$PROJECT_DIR/.env" ]; then
    echo "  WARNING: .env file not found!"
    echo "  Copy .env.example to .env and fill in your tokens:"
    echo "    cp .env.example .env"
    echo ""
fi

# 4. Install LaunchAgent
echo "[4/4] Installing LaunchAgent..."
mkdir -p "$LAUNCH_AGENTS_DIR"

if [ -f "$PROJECT_DIR/.env" ] && grep -q "DISCORD_BOT_TOKEN=." "$PROJECT_DIR/.env"; then
    # Unload if already loaded
    launchctl bootout gui/$(id -u) "$LAUNCH_AGENTS_DIR/com.portfolio.bot.plist" 2>/dev/null || true

    # Copy and load
    cp "$PROJECT_DIR/launchd/com.portfolio.bot.plist" "$LAUNCH_AGENTS_DIR/"
    launchctl bootstrap gui/$(id -u) "$LAUNCH_AGENTS_DIR/com.portfolio.bot.plist"
    echo "  LaunchAgent installed and started."
else
    echo "  Skipped — DISCORD_BOT_TOKEN not configured in .env"
    echo "  After configuring .env, run this script again."
fi

echo ""
echo "=== Setup Complete ==="
echo ""
echo "Status check:"
echo "  launchctl list | grep portfolio"
echo ""
echo "Logs:"
echo "  tail -f $PROJECT_DIR/logs/bot-stderr.log"
echo ""
echo "Manual start:"
echo "  python3 $PROJECT_DIR/bot.py"
