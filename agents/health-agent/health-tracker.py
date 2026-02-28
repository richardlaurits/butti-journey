#!/usr/bin/env python3
"""
Health Tracking System for Richard
Aggregates data from multiple sources:
- Apple Watch (workouts, HR, calories)
- Dexcom (blood sugar, TIR)
- Smart scale (weight, body fat %)
- Manual input (workouts, nutrition)
"""

import json
import os
from datetime import datetime, timedelta
from pathlib import Path

DATA_DIR = "agents/health-agent/data"
MEMORY_FILE = "agents/health-agent/MEMORY.md"

os.makedirs(DATA_DIR, exist_ok=True)

# Richard's baseline (2026-02-14)
BASELINE = {
    "weight_kg": 85.0,
    "height_cm": 190,
    "body_fat_target": 5,  # lose 5% body fat
    "timeline_weeks": 16,  # 4 months
    "goal_date": "2026-06-14"
}

def calculate_tdee(weight_kg, height_cm, activity_level="moderate"):
    """Estimate TDEE (Total Daily Energy Expenditure)"""
    # Mifflin-St Jeor equation (men)
    bmr = 10 * weight_kg + 6.25 * height_cm - 5 * 40 + 5  # Assuming age ~40
    
    activity_multipliers = {
        "sedentary": 1.2,
        "light": 1.375,
        "moderate": 1.55,
        "very_active": 1.725,
        "extremely_active": 1.9
    }
    
    tdee = bmr * activity_multipliers.get(activity_level, 1.55)
    return {"bmr": bmr, "tdee": tdee}

def calculate_progress(current_weight, current_bf=None):
    """Calculate progress toward 5% body fat loss goal"""
    weight_loss = BASELINE["weight_kg"] - current_weight
    
    progress = {
        "weight_loss_kg": weight_loss,
        "weight_loss_pct": (weight_loss / BASELINE["weight_kg"]) * 100,
        "weeks_elapsed": None,
        "target_completion": BASELINE["goal_date"],
        "pace_on_track": False
    }
    
    if current_bf:
        progress["body_fat_loss_pct"] = current_bf  # Will update when we have baseline
    
    return progress

class HealthTracker:
    def __init__(self):
        self.data_dir = DATA_DIR
        self.weekly_data = self.load_weekly_data()
    
    def load_weekly_data(self):
        """Load existing weekly data"""
        latest_file = None
        for f in sorted(Path(self.data_dir).glob("weekly-*.json"), reverse=True):
            latest_file = f
            break
        
        if latest_file:
            with open(latest_file, 'r') as f:
                return json.load(f)
        
        return self.create_empty_week()
    
    def create_empty_week(self):
        """Create empty weekly template"""
        today = datetime.now()
        week_start = today - timedelta(days=today.weekday())
        
        return {
            "week_start": week_start.strftime("%Y-%m-%d"),
            "week_end": (week_start + timedelta(days=6)).strftime("%Y-%m-%d"),
            "daily": {},
            "summary": {}
        }
    
    def add_daily_entry(self, date, data):
        """Add daily health data"""
        date_str = datetime.strptime(date, "%Y-%m-%d").strftime("%Y-%m-%d")
        
        self.weekly_data["daily"][date_str] = {
            "weight_kg": data.get("weight"),
            "body_fat_pct": data.get("body_fat"),
            "calories_consumed": data.get("calories_consumed"),
            "calories_burned": data.get("calories_burned"),
            "workouts": data.get("workouts", []),
            "tir_pct": data.get("tir"),  # Time in range (Dexcom)
            "avg_glucose": data.get("avg_glucose"),
            "notes": data.get("notes", "")
        }
    
    def calculate_weekly_summary(self):
        """Calculate weekly statistics"""
        daily = self.weekly_data["daily"]
        
        if not daily:
            return None
        
        weights = [d.get("weight_kg") for d in daily.values() if d.get("weight_kg")]
        calories_consumed = [d.get("calories_consumed") for d in daily.values() if d.get("calories_consumed")]
        calories_burned = [d.get("calories_burned") for d in daily.values() if d.get("calories_burned")]
        tir_values = [d.get("tir_pct") for d in daily.values() if d.get("tir_pct")]
        
        summary = {
            "days_logged": len(daily),
            "weight_start": weights[0] if weights else None,
            "weight_end": weights[-1] if weights else None,
            "weight_change": (weights[-1] - weights[0]) if len(weights) > 1 else 0,
            "avg_calories_consumed": sum(calories_consumed) / len(calories_consumed) if calories_consumed else 0,
            "avg_calories_burned": sum(calories_burned) / len(calories_burned) if calories_burned else 0,
            "avg_deficit": (sum(calories_burned) - sum(calories_consumed)) / len(calories_consumed) if calories_consumed else 0,
            "avg_tir": sum(tir_values) / len(tir_values) if tir_values else 0,
            "workouts_completed": sum([len(d.get("workouts", [])) for d in daily.values()]),
        }
        
        # Progress check
        if weights:
            progress = calculate_progress(weights[-1])
            summary["progress"] = progress
        
        self.weekly_data["summary"] = summary
        return summary
    
    def save_week(self):
        """Save weekly data"""
        summary = self.calculate_weekly_summary()
        
        filename = f"{self.data_dir}/weekly-{datetime.now().strftime('%Y-%m-%d')}.json"
        with open(filename, 'w') as f:
            json.dump(self.weekly_data, f, indent=2)
        
        print(f"✅ Saved weekly data: {filename}")
        return filename

def generate_weekly_summary(tracker):
    """Generate human-readable weekly summary"""
    summary = tracker.weekly_data.get("summary", {})
    
    if not summary:
        return "No data logged yet"
    
    report = f"""
📊 **WEEKLY HEALTH SUMMARY**

**Weight & Body:**
- Start: {summary.get('weight_start', 'N/A')} kg
- End: {summary.get('weight_end', 'N/A')} kg
- Change: {summary.get('weight_change', 0):.1f} kg

**Calories:**
- Consumed: {summary.get('avg_calories_consumed', 0):.0f} kcal/day avg
- Burned: {summary.get('avg_calories_burned', 0):.0f} kcal/day avg
- Deficit: {summary.get('avg_deficit', 0):.0f} kcal/day avg

**Diabetes (Dexcom):**
- Avg TIR: {summary.get('avg_tir', 0):.0f}%

**Training:**
- Workouts: {summary.get('workouts_completed', 0)} sessions

**Progress:**
{json.dumps(summary.get('progress', {}), indent=2) if summary.get('progress') else 'N/A'}

**Target:** Best shape in 4 months (by June 14, 2026)
"""
    
    return report

if __name__ == "__main__":
    # Example usage
    tracker = HealthTracker()
    
    # Add sample data
    today = datetime.now().strftime("%Y-%m-%d")
    tracker.add_daily_entry(today, {
        "weight": 85.0,
        "body_fat": 20,  # Will refine
        "calories_consumed": 2500,
        "calories_burned": 2800,
        "workouts": [{"type": "strength", "duration_min": 60, "intensity": "high"}],
        "tir": 95
    })
    
    tracker.save_week()
    print(generate_weekly_summary(tracker))
