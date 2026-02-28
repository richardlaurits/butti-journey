#!/usr/bin/env python3
"""
Watchdog Agent Self-Test
Validates that the watchdog is functioning correctly
"""

import json
import subprocess
import sys
from pathlib import Path

WATCHDOG_DIR = Path(__file__).parent
STATUS_FILE = WATCHDOG_DIR / "status.json"
RULES_FILE = WATCHDOG_DIR / "rules.json"

def test_files_exist():
    """Test 1: All required files exist."""
    print("Test 1: Required files exist...")
    required = ["watchdog.py", "rules.json", "README.md", "run-watchdog.sh", "demo.sh"]
    for f in required:
        path = WATCHDOG_DIR / f
        assert path.exists(), f"Missing: {f}"
        print(f"  ✅ {f}")
    print("  PASSED\n")

def test_rules_valid():
    """Test 2: Rules JSON is valid."""
    print("Test 2: Rules JSON is valid...")
    with open(RULES_FILE) as f:
        rules = json.load(f)
    assert "auto_remediate" in rules
    assert "alert_escalation" in rules
    print(f"  ✅ Rules version: {rules.get('version', 'unknown')}")
    print(f"  ✅ Auto-remediation: {'enabled' if rules['auto_remediate'].get('enabled') else 'disabled'}")
    print("  PASSED\n")

def test_watchdog_executable():
    """Test 3: Watchdog can run and produce output."""
    print("Test 3: Watchdog execution...")
    result = subprocess.run(
        [sys.executable, str(WATCHDOG_DIR / "watchdog.py")],
        capture_output=True,
        text=True,
        cwd=WATCHDOG_DIR.parent.parent  # Run from workspace
    )
    assert result.returncode in [0, 1], f"Unexpected exit code: {result.returncode}"
    assert STATUS_FILE.exists(), "Status file not created"
    print(f"  ✅ Exit code: {result.returncode}")
    print(f"  ✅ Status file created")
    print("  PASSED\n")

def test_status_structure():
    """Test 4: Status JSON has expected structure."""
    print("Test 4: Status JSON structure...")
    with open(STATUS_FILE) as f:
        status = json.load(f)
    
    required_keys = ["last_check", "agents", "cron_jobs", "environment", "alerts", "auto_fixed"]
    for key in required_keys:
        assert key in status, f"Missing key: {key}"
        print(f"  ✅ {key}")
    
    # Validate environment has required fields
    env = status.get("environment", {})
    assert "node_available" in env
    assert "nvm_available" in env
    assert "npm_healthy" in env
    print("  ✅ Environment fields complete")
    print("  PASSED\n")

def test_environment_health():
    """Test 5: Current environment passes health checks."""
    print("Test 5: Environment health...")
    with open(STATUS_FILE) as f:
        status = json.load(f)
    
    env = status.get("environment", {})
    assert env.get("node_available") == True, "Node not available"
    assert env.get("nvm_available") == True, "NVM not available"
    assert env.get("npm_healthy") == True, "NPM prefix not healthy"
    
    print(f"  ✅ Node: {env.get('node_version')}")
    print(f"  ✅ NVM: {env.get('nvm_current')}")
    print(f"  ✅ NPM prefix: healthy")
    print("  PASSED\n")

def main():
    print("=" * 50)
    print("  WATCHDOG AGENT SELF-TEST")
    print("=" * 50)
    print()
    
    try:
        test_files_exist()
        test_rules_valid()
        test_watchdog_executable()
        test_status_structure()
        test_environment_health()
        
        print("=" * 50)
        print("  ✅ ALL TESTS PASSED")
        print("=" * 50)
        print()
        print("The watchdog agent is functioning correctly.")
        print("Integration with heartbeat is ready.")
        return 0
        
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
        return 1
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
