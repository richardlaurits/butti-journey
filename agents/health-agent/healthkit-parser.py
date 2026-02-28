#!/usr/bin/env python3
"""
Apple HealthKit Data Parser
Parses exported HealthKit data (XML format from Apple Health app)
Extracts:
- Workouts (type, duration, calories, heart rate)
- Daily steps
- Heart rate variability
- Sleep data
"""

import xml.etree.ElementTree as ET
import json
import os
from datetime import datetime, timedelta
from pathlib import Path

class HealthKitParser:
    def __init__(self, export_file=None):
        self.export_file = export_file
        self.data = {}
    
    def parse_export(self, file_path):
        """Parse HealthKit export XML file"""
        try:
            tree = ET.parse(file_path)
            root = tree.getroot()
            
            # Extract all records
            workouts = []
            steps = {}
            heart_rates = {}
            sleep_data = {}
            
            for record in root.findall(".//Record"):
                record_type = record.get("type", "")
                start_date = record.get("startDate", "")
                end_date = record.get("endDate", "")
                value = record.get("value", "")
                
                # Workouts
                if "HKWorkout" in record_type:
                    workout = self.parse_workout(record)
                    if workout:
                        workouts.append(workout)
                
                # Steps
                elif "HKQuantityTypeIdentifierStepCount" in record_type:
                    steps[start_date] = float(value)
                
                # Heart rate
                elif "HKQuantityTypeIdentifierHeartRate" in record_type:
                    if start_date not in heart_rates:
                        heart_rates[start_date] = []
                    heart_rates[start_date].append(float(value))
                
                # Sleep
                elif "HKCategoryTypeIdentifierSleepAnalysis" in record_type:
                    sleep_data[start_date] = value
            
            self.data = {
                "workouts": workouts,
                "steps": steps,
                "heart_rates": heart_rates,
                "sleep": sleep_data,
                "parsed_at": datetime.now().isoformat()
            }
            
            return True
            
        except Exception as e:
            print(f"❌ Parse error: {e}")
            return False
    
    def parse_workout(self, record):
        """Extract workout details from XML record"""
        try:
            workout_type = record.get("workoutActivityType", "Unknown")
            start_date = record.get("startDate", "")
            end_date = record.get("endDate", "")
            
            # Calculate duration
            start = datetime.fromisoformat(start_date.replace("Z", "+00:00"))
            end = datetime.fromisoformat(end_date.replace("Z", "+00:00"))
            duration_min = (end - start).total_seconds() / 60
            
            # Get calories burned (if available)
            calories = None
            for stat in record.findall(".//FileReference"):
                # FileReference contains calorie data
                pass
            
            return {
                "type": self.normalize_workout_type(workout_type),
                "start": start_date,
                "end": end_date,
                "duration_min": duration_min,
                "calories": calories
            }
        except Exception as e:
            return None
    
    def normalize_workout_type(self, type_str):
        """Normalize Apple's workout type names"""
        mapping = {
            "HKWorkoutActivityTypeStrengthTraining": "strength",
            "HKWorkoutActivityTypeRunning": "running",
            "HKWorkoutActivityTypeCycling": "cycling",
            "HKWorkoutActivityTypeSwimming": "swimming",
            "HKWorkoutActivityTypeWalking": "walking",
            "HKWorkoutActivityTypeYoga": "yoga",
            "HKWorkoutActivityTypeWalking": "walking",
        }
        
        for key, value in mapping.items():
            if key in type_str:
                return value
        
        return "other"
    
    def get_weekly_workouts(self, days_back=7):
        """Get workouts from last N days"""
        if not self.data.get("workouts"):
            return []
        
        cutoff = datetime.now() - timedelta(days=days_back)
        
        recent = []
        for workout in self.data["workouts"]:
            try:
                workout_date = datetime.fromisoformat(
                    workout["start"].replace("Z", "+00:00")
                )
                if workout_date > cutoff:
                    recent.append(workout)
            except:
                pass
        
        return recent
    
    def get_weekly_steps(self, days_back=7):
        """Get daily step counts"""
        steps = self.data.get("steps", {})
        
        total_steps = sum(v for k, v in steps.items())
        avg_steps = total_steps / len(steps) if steps else 0
        
        return {
            "total_steps": total_steps,
            "avg_daily_steps": avg_steps,
            "days_logged": len(steps)
        }
    
    def get_avg_heart_rate(self, days_back=7):
        """Calculate average resting heart rate"""
        hr_data = self.data.get("heart_rates", {})
        
        all_rates = []
        for rates in hr_data.values():
            all_rates.extend(rates)
        
        if not all_rates:
            return None
        
        return {
            "avg_hr": sum(all_rates) / len(all_rates),
            "min_hr": min(all_rates),
            "max_hr": max(all_rates),
            "readings": len(all_rates)
        }
    
    def save_parsed_data(self):
        """Save parsed data to JSON"""
        os.makedirs("agents/health-agent/data", exist_ok=True)
        
        filename = f"agents/health-agent/data/healthkit-{datetime.now().strftime('%Y-%m-%d')}.json"
        with open(filename, 'w') as f:
            json.dump(self.data, f, indent=2)
        
        print(f"✅ Saved HealthKit data: {filename}")
        return filename

if __name__ == "__main__":
    print("🏥 Apple HealthKit Parser\n")
    
    # Find export file
    export_files = list(Path(".").glob("**/apple_health_export/export.xml"))
    
    if export_files:
        parser = HealthKitParser()
        if parser.parse_export(str(export_files[0])):
            print(f"✅ Parsed {len(parser.data.get('workouts', []))} workouts")
            print(f"✅ Parsed {len(parser.data.get('steps', {}))} days of steps")
            parser.save_parsed_data()
    else:
        print("⏳ HealthKit export file not found")
        print("\nTo export your HealthKit data:")
        print("1. Open Health app")
        print("2. Tap your profile (top right)")
        print("3. Export Health Data")
        print("4. Zip file will be ready")
