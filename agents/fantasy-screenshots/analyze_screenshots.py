#!/usr/bin/env python3
"""
Fantasy Screenshot Analyzer
Analyzes uploaded squad screenshots on demand
Run manually when Richard requests analysis
"""

import json
import os
from datetime import datetime
from pathlib import Path

SCREENSHOTS_DIR = Path.home() / '.openclaw/workspace/agents/fantasy-screenshots'

def list_available_screenshots():
    """List all available screenshots"""
    index_file = SCREENSHOTS_DIR / 'screenshots_index.json'
    
    if not index_file.exists():
        return None
    
    with open(index_file, 'r') as f:
        return json.load(f)

def analyze_seriea_squad():
    """Analyze latest Serie A squad"""
    seriea_dir = SCREENSHOTS_DIR / 'seriea'
    
    # Get latest screenshot
    screenshots = sorted(seriea_dir.glob('*.jpg'))
    if not screenshots:
        return "No Serie A screenshots found"
    
    latest = screenshots[-1]
    
    # Load metadata
    index = list_available_screenshots()
    metadata = None
    
    for file_info in index['folders']['seriea']['files']:
        if file_info['filename'] == latest.name:
            metadata = file_info
            break
    
    if not metadata:
        return f"Found screenshot: {latest.name} but no metadata"
    
    # Build analysis request for sub-agent
    content = metadata['content']
    
    analysis_task = f"""Analyze this Serie A fantasy squad for the upcoming gameweek:

SQUAD ({metadata['date']}, {metadata['gameweek']}):
Formation: {content['formation']}

GK: {', '.join(content['gk'])}
DEF: {', '.join(content['def'])}
MID: {', '.join(content['mid'])}
FWD: {', '.join(content['fwd'])}
Bench: {', '.join(content['bench'])}

TASK:
1. Check upcoming fixtures for each player
2. Identify any injury concerns or suspensions
3. Suggest captain pick
4. Recommend any bench vs starting XI changes
5. Note any players with particularly good/bad fixtures

Screenshot file: {latest}
"""
    
    return analysis_task

def analyze_bundesliga_squad():
    """Analyze latest Bundesliga squad"""
    bundesliga_dir = SCREENSHOTS_DIR / 'bundesliga'
    screenshots = sorted(bundesliga_dir.glob('*.jpg'))
    
    if not screenshots:
        return "No Bundesliga screenshots found. Please upload your squad screenshot."
    
    latest = screenshots[-1]
    return f"Found Bundesliga screenshot: {latest.name}\nReady for analysis on request."

def main():
    """Main function"""
    print("=" * 80)
    print("📸 FANTASY SCREENSHOT ANALYZER")
    print("=" * 80)
    print()
    
    # Show available screenshots
    index = list_available_screenshots()
    
    if not index:
        print("❌ No screenshots index found")
        return
    
    print("📁 Available Screenshots:")
    print()
    
    for league, data in index['folders'].items():
        print(f"\n{league.upper()}:")
        print(f"  Platform: {data['platform']}")
        print(f"  Files: {len(data['files'])}")
        
        for file_info in data['files']:
            print(f"    • {file_info['filename']} ({file_info['date']})")
    
    print("\n" + "=" * 80)
    print("USAGE:")
    print("  python3 analyze_fantasy_screenshots.py seriea    # Analyze Serie A")
    print("  python3 analyze_fantasy_screenshots.py bundesliga # Analyze Bundesliga")
    print("  python3 analyze_fantasy_screenshots.py list      # List all screenshots")
    print("=" * 80)

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == 'seriea':
            print(analyze_seriea_squad())
        elif sys.argv[1] == 'bundesliga':
            print(analyze_bundesliga_squad())
        elif sys.argv[1] == 'list':
            main()
        else:
            print(f"Unknown command: {sys.argv[1]}")
    else:
        main()
