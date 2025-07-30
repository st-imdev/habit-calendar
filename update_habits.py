#!/usr/bin/env python3
"""
Standalone script to update habit data - designed for GitHub Actions
"""

from datetime import datetime, timedelta
import json
import random
import os

def auto_update_habits(path="habit_data.json"):
    """Automatically update habit data with random but improving consistency"""
    
    # Load existing data
    if os.path.exists(path):
        with open(path, "r") as f:
            habit_data = json.load(f)
    else:
        habit_data = {}
    
    today = datetime.today().date()
    today_str = today.strftime("%Y-%m-%d")
    
    # If today's data already exists, don't overwrite
    if today_str in habit_data:
        print(f"Habit data for {today_str} already exists, skipping update")
        return habit_data
    
    # Calculate days since start of year to show progression
    start_of_year = datetime(today.year, 1, 1).date()
    days_passed = (today - start_of_year).days
    
    # Base probabilities that increase over time
    base_prob = 0.6  # Starting probability
    improvement_rate = 0.3 / 365  # Improve by 30% over the year
    current_prob = min(0.95, base_prob + (days_passed * improvement_rate))
    
    # Habit-specific modifiers (some habits are easier to maintain)
    habit_probs = {
        "water": current_prob + 0.2,      # Easiest habit
        "journal": current_prob + 0.1,    # Pretty easy
        "meditate": current_prob,         # Baseline
        "read": current_prob,             # Baseline  
        "exercise": current_prob - 0.1,   # Slightly harder
    }
    
    # Generate today's habits
    today_habits = {}
    for habit, prob in habit_probs.items():
        # Add some randomness but bias toward consistency
        today_habits[habit] = random.random() < min(0.98, max(0.1, prob))
    
    # Save updated data
    habit_data[today_str] = today_habits
    
    with open(path, "w") as f:
        json.dump(habit_data, f, indent=2)
    
    print(f"Updated habit data for {today_str}: {today_habits}")
    return habit_data

if __name__ == "__main__":
    auto_update_habits() 