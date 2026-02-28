#!/bin/bash
# Watchdog Agent Runner
# Usage: ./run-watchdog.sh [options]
# Options: --quiet (no output unless issues found)

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE_DIR="$(dirname "$(dirname "$SCRIPT_DIR")")"

cd "$WORKSPACE_DIR"

# Run the watchdog
if [ "$1" == "--quiet" ]; then
    python3 agents/watchdog-agent/watchdog.py > /dev/null 2>&1 && exit 0
    # If we get here, there were issues
    python3 agents/watchdog-agent/watchdog.py 2>&1 | tail -20
    exit 1
else
    python3 agents/watchdog-agent/watchdog.py
fi
