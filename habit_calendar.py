from datetime import datetime, timedelta
from PIL import Image, ImageDraw, ImageFont
import json
import random
import os

# Constants for minimalist row-based tracker
SCALE = 2
CELL_SIZE = 20 * SCALE  # Slightly larger cells for better visibility
CELL_PADDING = 3 * SCALE
DAYS_TO_SHOW = 21  # Show last three weeks
HABIT_LABEL_WIDTH = 90 * SCALE  # Width for habit names
FONT_SIZE = 11 * SCALE

# Calculate dimensions
WIDTH = HABIT_LABEL_WIDTH + (DAYS_TO_SHOW * (CELL_SIZE + CELL_PADDING)) + CELL_PADDING * 2
HEIGHT = 0  # Will be calculated based on number of habits

# Define the 5 core habits to track
HABITS_TO_TRACK = ["exercise", "read", "meditate", "water", "journal"]

# Light theme colors - using existing green palette
LIGHT_COMPLETED_COLOR = (64, 196, 99)  # Medium green for completed
LIGHT_MISSED_COLOR = (248, 248, 246)  # Very light beige for missed
LIGHT_TEXT_COLOR = (51, 51, 51)
LIGHT_BG_COLOR = (255, 255, 255, 0)  # Transparent background

# Dark theme colors - using existing blue palette  
DARK_COMPLETED_COLOR = (74, 126, 255)  # Blue for completed
DARK_MISSED_COLOR = (48, 54, 61)  # Dark gray for missed
DARK_TEXT_COLOR = (200, 200, 200)
DARK_BG_COLOR = (0, 0, 0, 0)  # Transparent background

LIGHT_BORDER_COLOR = (220, 220, 220)
DARK_BORDER_COLOR = (74, 126, 255, 100)  # Semi-transparent blue


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
    
    return habit_data

def load_habit_data(path="habit_data.json"):
    with open(path, "r") as f:
        return json.load(f)

def get_last_days_data(habit_data):
    """Get habit data for the last 21 days"""
    today = datetime.today().date()
    days_data = []
    
    for i in range(DAYS_TO_SHOW - 1, -1, -1):  # Start from 20 days ago to today
        date = today - timedelta(days=i)
        date_str = date.strftime("%Y-%m-%d")
        day_habits = habit_data.get(date_str, {})
        days_data.append({
            'date': date,
            'habits': day_habits
        })
    
    return days_data

def get_font(size):
    """Try to get a nice font, fallback to default if not available"""
    try:
        # Try different font options
        font_paths = [
            "/System/Library/Fonts/Helvetica.ttc",  # macOS
            "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",  # Linux
            "C:\\Windows\\Fonts\\Arial.ttf",  # Windows
        ]
        for path in font_paths:
            if os.path.exists(path):
                return ImageFont.truetype(path, size)
    except:
        pass
    # Fallback to default PIL font
    return ImageFont.load_default()

def generate_calendar_image(habit_data, theme="light"):
    """Generate a minimalist row-based habit tracker"""
    # Calculate height based on number of habits
    num_habits = len(HABITS_TO_TRACK)
    row_height = CELL_SIZE + CELL_PADDING
    total_height = (num_habits * row_height) + CELL_PADDING * 3 + FONT_SIZE + CELL_PADDING
    
    # Set colors based on theme
    if theme == "dark":
        bg_color = DARK_BG_COLOR
        text_color = DARK_TEXT_COLOR
        completed_color = DARK_COMPLETED_COLOR
        missed_color = DARK_MISSED_COLOR
        border_color = DARK_BORDER_COLOR
    else:
        bg_color = LIGHT_BG_COLOR
        text_color = LIGHT_TEXT_COLOR
        completed_color = LIGHT_COMPLETED_COLOR
        missed_color = LIGHT_MISSED_COLOR
        border_color = LIGHT_BORDER_COLOR
    
    # Create image with transparent background
    img = Image.new("RGBA", (WIDTH, total_height), bg_color)
    draw = ImageDraw.Draw(img)
    
    # Get font
    font = get_font(FONT_SIZE)
    small_font = get_font(int(FONT_SIZE * 0.65))  # Even smaller for date headers
    
    # Get last days data
    days_data = get_last_days_data(habit_data)
    
    # Draw day headers (US format M/D)
    header_y = CELL_PADDING
    for i, day_data in enumerate(days_data):
        x = HABIT_LABEL_WIDTH + (i * (CELL_SIZE + CELL_PADDING))
        # US format M/D without leading zeros (platform-safe)
        month = day_data['date'].month
        day = day_data['date'].day
        date_text = f"{month}/{day}"
        # Center the text in the cell
        text_bbox = draw.textbbox((0, 0), date_text, font=small_font)
        text_width = text_bbox[2] - text_bbox[0]
        text_x = x + (CELL_SIZE - text_width) // 2
        draw.text((text_x, header_y), date_text, fill=text_color, font=small_font)
    
    # Draw habits
    start_y = header_y + FONT_SIZE + CELL_PADDING
    
    for habit_idx, habit in enumerate(HABITS_TO_TRACK):
        y = start_y + (habit_idx * row_height)
        
        # Draw habit name
        habit_display = habit.capitalize()
        draw.text((CELL_PADDING, y + 2), habit_display, fill=text_color, font=font)
        
        # Draw completion squares for each day
        for day_idx, day_data in enumerate(days_data):
            x = HABIT_LABEL_WIDTH + (day_idx * (CELL_SIZE + CELL_PADDING))
            
            # Check if habit was completed that day
            completed = day_data['habits'].get(habit, False)
            fill_color = completed_color if completed else missed_color
            
            # Draw rounded rectangle
            draw.rounded_rectangle(
                [x, y, x + CELL_SIZE, y + CELL_SIZE],
                radius=4 * SCALE,
                fill=fill_color,
                outline=border_color
            )
    
    return img 