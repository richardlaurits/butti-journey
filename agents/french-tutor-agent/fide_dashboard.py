#!/usr/bin/env python3
"""
FIDE A1 Progress Dashboard
Shows exam readiness and tracks all competencies
"""

import json
from datetime import datetime
from pathlib import Path

AGENT_DIR = Path(__file__).parent

def show_dashboard():
    """Display comprehensive progress dashboard."""
    
    # Load data
    with open(AGENT_DIR / "fide_progress.json") as f:
        progress = json.load(f)
    
    with open(AGENT_DIR / "fide_a1_curriculum.json") as f:
        curriculum = json.load(f)
    
    exam_prep = progress["exam_prep"]
    
    print("\n" + "=" * 70)
    print(f"🎯 FIDE A1 EXAM DASHBOARD".center(70))
    print("=" * 70)
    
    # Timeline
    print(f"\n📅 TIMELINE")
    print(f"   Started: {exam_prep['start_date']}")
    print(f"   Goal:    {exam_prep['goal_date']}")
    print(f"   Today:   Day {exam_prep['current_day']} of 90")
    print(f"   Remaining: {exam_prep['days_remaining']} days")
    
    # Progress bar
    pct_complete = (exam_prep['current_day'] / 90) * 100
    bar_length = 40
    filled = int(bar_length * pct_complete / 100)
    bar = "█" * filled + "░" * (bar_length - filled)
    print(f"\n   Progress: [{bar}] {pct_complete:.1f}%")
    
    # Phase info
    print(f"\n📍 CURRENT PHASE: {exam_prep['phase_name']}")
    for phase in curriculum["phases"]:
        if phase["phase"] == exam_prep["phase"]:
            print(f"   Focus: {phase['focus']}")
            print(f"   Daily target: {phase['daily_minutes']} minutes")
            print(f"   Topics: {', '.join(phase['topics'][:3])}...")
    
    # Competency scores
    print(f"\n📊 COMPETENCY SCORES (Target: 60/100 each)")
    for competency, data in progress["competency_scores"].items():
        name = competency.replace("_", " ").title()
        current = data["current"]
        target = data["target"]
        pct = data["progress_pct"]
        bar = "█" * int(pct / 5) + "░" * (20 - int(pct / 5))
        print(f"   {name:20} [{bar}] {current}/{target} ({pct}%)")
    
    # Vocabulary
    vocab = progress["vocabulary"]
    print(f"\n📝 VOCABULARY")
    print(f"   Learned: {vocab['learned']} words")
    print(f"   Phase 1 target: {curriculum['required_vocabulary']['phase_1']}")
    print(f"   Total A1 target: {curriculum['required_vocabulary']['phase_4']}")
    vocab_pct = (vocab['learned'] / curriculum['required_vocabulary']['phase_4']) * 100
    print(f"   Progress: {vocab_pct:.1f}% of total required")
    
    # Practice streak
    streak = progress["streak"]
    print(f"\n🔥 PRACTICE STREAK")
    print(f"   Current: {streak['current']} days")
    print(f"   Best: {streak['best']} days")
    
    # Recent activity
    print(f"\n📈 RECENT ACTIVITY")
    recent = progress["practice_log"][-5:]
    for session in recent:
        print(f"   {session['date']}: {session['type']} ({session['duration_minutes']} min)")
    
    # Next milestone
    milestone = progress["next_milestone"]
    print(f"\n🎯 NEXT MILESTONE: {milestone['name']}")
    print(f"   Due: {milestone['date']} ({milestone['days_away']} days)")
    print(f"   Requirements:")
    for req in milestone["requirements"]:
        print(f"      • {req}")
    
    # Exam readiness
    readiness = progress["exam_readiness"]
    print(f"\n📋 EXAM READINESS")
    print(f"   Overall: {readiness['overall']}%")
    print(f"   Status: {readiness['estimated_pass_probability']}")
    print(f"   Focus areas:")
    for area in readiness["focus_areas"]:
        print(f"      → {area}")
    
    print("\n" + "=" * 70)
    print(f"💪 Keep going! {exam_prep['days_remaining']} days to achieve FIDE A1!")
    print("=" * 70 + "\n")

if __name__ == "__main__":
    show_dashboard()
