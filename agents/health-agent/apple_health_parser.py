#!/usr/bin/env python3
"""
Apple Health JSON Parser
Parses Apple Health export files and extracts key metrics
"""

import json
from datetime import datetime, timedelta
from pathlib import Path
from collections import defaultdict

class AppleHealthParser:
    def __init__(self, json_path):
        self.json_path = Path(json_path)
        self.data = None
        self.load_data()
        
    def load_data(self):
        """Load and parse Apple Health JSON"""
        with open(self.json_path, 'r') as f:
            self.data = json.load(f)
        print(f"✅ Loaded {len(self.data.get('data', {}).get('metrics', []))} health metrics")
        
    def parse_metric(self, metric_type):
        """Extract specific metric from health data"""
        metrics = self.data.get('data', {}).get('metrics', [])
        
        for metric in metrics:
            if metric.get('name') == metric_type:
                return metric.get('data', [])
        return []
    
    def get_steps(self, days=7):
        """Get daily step counts for last N days"""
        steps_data = self.parse_metric('step_count')
        
        daily_steps = defaultdict(int)
        for entry in steps_data:
            date = entry.get('date', '').split(' ')[0]
            qty = entry.get('qty', 0)
            daily_steps[date] += int(qty)
        
        # Get last N days
        sorted_dates = sorted(daily_steps.keys())[-days:]
        return {date: daily_steps[date] for date in sorted_dates}
    
    def get_heart_rate(self, days=7):
        """Get average heart rate for last N days"""
        hr_data = self.parse_metric('heart_rate')
        
        daily_hr = defaultdict(list)
        for entry in hr_data:
            date = entry.get('date', '').split(' ')[0]
            qty = entry.get('qty', 0)
            daily_hr[date].append(int(qty))
        
        # Calculate daily averages
        daily_avg = {}
        for date, values in daily_hr.items():
            daily_avg[date] = sum(values) / len(values) if values else 0
        
        sorted_dates = sorted(daily_avg.keys())[-days:]
        return {date: daily_avg[date] for date in sorted_dates}
    
    def get_sleep(self, days=7):
        """Get sleep duration for last N days"""
        sleep_data = self.parse_metric('sleep_analysis')
        
        daily_sleep = defaultdict(float)
        for entry in sleep_data:
            date = entry.get('date', '').split(' ')[0]
            # Duration is in format "HH:MM:SS"
            duration = entry.get('duration', '00:00:00')
            parts = duration.split(':')
            hours = int(parts[0]) + int(parts[1])/60 + int(parts[2])/3600
            daily_sleep[date] += hours
        
        sorted_dates = sorted(daily_sleep.keys())[-days:]
        return {date: daily_sleep[date] for date in sorted_dates}
    
    def get_workouts(self, days=30):
        """Get workout summary for last N days"""
        workouts = self.data.get('data', {}).get('workouts', [])
        
        recent_workouts = []
        cutoff = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
        
        for workout in workouts:
            date = workout.get('start', '').split(' ')[0]
            if date >= cutoff:
                recent_workouts.append({
                    'date': date,
                    'type': workout.get('name', 'Unknown'),
                    'duration': workout.get('duration', '00:00:00'),
                    'energy': workout.get('activeEnergyBurned', 0),
                })
        
        return recent_workouts
    
    def get_blood_glucose(self, days=7):
        """Get blood glucose readings if available (from Dexcom)"""
        bg_data = self.parse_metric('blood_glucose')
        
        readings = []
        for entry in bg_data[-days*10:]:  # Last days * ~10 readings/day
            readings.append({
                'date': entry.get('date', ''),
                'value': entry.get('qty', 0),
                'unit': entry.get('unit', 'mg/dL')
            })
        
        return readings
    
    def generate_summary(self):
        """Generate comprehensive health summary"""
        summary = {
            'steps_7d': self.get_steps(7),
            'heart_rate_7d': self.get_heart_rate(7),
            'sleep_7d': self.get_sleep(7),
            'workouts_30d': self.get_workouts(30),
        }
        
        # Calculate averages
        summary['avg_steps_7d'] = sum(summary['steps_7d'].values()) / len(summary['steps_7d']) if summary['steps_7d'] else 0
        summary['avg_sleep_7d'] = sum(summary['sleep_7d'].values()) / len(summary['sleep_7d']) if summary['sleep_7d'] else 0
        summary['avg_hr_7d'] = sum(summary['heart_rate_7d'].values()) / len(summary['heart_rate_7d']) if summary['heart_rate_7d'] else 0
        summary['workout_count_30d'] = len(summary['workouts_30d'])
        
        return summary
    
    def format_report(self):
        """Format health report for Telegram"""
        summary = self.generate_summary()
        
        lines = []
        lines.append("📊 **Apple Health Report - Senaste 7 dagarna**")
        lines.append("")
        
        # Steps
        lines.append("👟 **Steg:**")
        lines.append(f"   Genomsnitt: {int(summary['avg_steps_7d']):,} steg/dag")
        for date, steps in list(summary['steps_7d'].items())[-3:]:
            date_short = date[5:]  # MM-DD
            lines.append(f"   {date_short}: {steps:,} steg")
        lines.append("")
        
        # Heart Rate
        lines.append("❤️ **Puls:**")
        lines.append(f"   Genomsnitt: {int(summary['avg_hr_7d'])} bpm")
        lines.append("")
        
        # Sleep
        lines.append("😴 **Sömn:**")
        lines.append(f"   Genomsnitt: {summary['avg_sleep_7d']:.1f} timmar/natt")
        for date, hours in list(summary['sleep_7d'].items())[-3:]:
            date_short = date[5:]
            lines.append(f"   {date_short}: {hours:.1f}h")
        lines.append("")
        
        # Workouts
        lines.append("💪 **Träning (30 dagar):**")
        lines.append(f"   Totalt pass: {summary['workout_count_30d']}")
        if summary['workouts_30d']:
            recent = summary['workouts_30d'][-3:]
            for w in recent:
                lines.append(f"   {w['date'][5:]}: {w['type']} ({w['duration']})")
        
        return "\n".join(lines)

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python3 apple_health_parser.py <path_to_export.json>")
        sys.exit(1)
    
    parser = AppleHealthParser(sys.argv[1])
    print(parser.format_report())
