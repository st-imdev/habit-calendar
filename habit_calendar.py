from datetime import datetime, timedelta
from PIL import Image, ImageDraw
import json

# Constants for calendar appearance
SCALE = 2
CELL_SIZE = 12 * SCALE
CELL_PADDING = 2 * SCALE
WEEKS = 53
DAYS = 7
WIDTH = WEEKS * (CELL_SIZE + CELL_PADDING) + CELL_PADDING + 20 * SCALE
HEIGHT = DAYS * (CELL_SIZE + CELL_PADDING) + CELL_PADDING

# Light theme (GitHub green) colors
LIGHT_COLORS = [
    (248, 248, 246),  # 0 habits (very light warm beige)
    (155, 233, 168),  # 1 habit (lightest green)
    (64, 196, 99),    # 2 habits (light green)
    (48, 161, 78),    # 3 habits (medium green)
    (33, 110, 57),    # 4+ habits (dark green)
]

# Dark theme (blue #4a7eff based) colors
DARK_COLORS = [
    (48, 54, 61),     # 0 habits (dark gray)
    (74, 126, 255, 80),   # 1 habit (lightest blue, semi-transparent)
    (74, 126, 255, 120),  # 2 habits (light blue)
    (74, 126, 255, 180),  # 3 habits (medium blue)
    (74, 126, 255, 255),  # 4+ habits (full blue)
]

LIGHT_BORDER_COLOR = (220, 220, 220)
DARK_BORDER_COLOR = (74, 126, 255, 100)  # Semi-transparent blue


def load_habit_data(path="habit_data.json"):
    with open(path, "r") as f:
        return json.load(f)

def get_calendar_matrix(habit_data):
    today = datetime.today().date()
    # Find the most recent Sunday before or on today
    start_of_calendar = today - timedelta(days=today.weekday() + 1 + (WEEKS-1)*7)
    matrix = [[None for _ in range(DAYS)] for _ in range(WEEKS)]
    max_habits = 1
    for week in range(WEEKS):
        for day in range(DAYS):
            date = start_of_calendar + timedelta(weeks=week, days=day)
            if date > today:
                continue  # Don't fill future days
            date_str = date.strftime("%Y-%m-%d")
            habits = habit_data.get(date_str, {})
            count = sum(1 for v in habits.values() if v)
            matrix[week][day] = count
            if count > max_habits:
                max_habits = count
    return matrix, max_habits, start_of_calendar

def get_color(count, max_habits, theme="light"):
    colors = DARK_COLORS if theme == "dark" else LIGHT_COLORS
    
    if count is None:
        return (0, 0, 0, 0)  # Transparent for empty cells
    if count == 0:
        return colors[0]
    # Map count to color index (1-4)
    idx = min(4, int((count / max_habits) * 4))
    idx = max(1, idx)  # Ensure at least 1 for nonzero
    return colors[idx]

def generate_calendar_image(habit_data, theme="light"):
    matrix, max_habits, start_of_calendar = get_calendar_matrix(habit_data)
    # Use RGBA for transparency support
    img = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))  # Transparent background
    draw = ImageDraw.Draw(img)

    # Choose border color based on theme
    border_color = DARK_BORDER_COLOR if theme == "dark" else LIGHT_BORDER_COLOR

    # Draw calendar squares (no title, no border)
    top_offset = 0
    for week in range(WEEKS):
        for day in range(DAYS):
            count = matrix[week][day]
            color = get_color(count, max_habits, theme)
            x = week * (CELL_SIZE + CELL_PADDING) + CELL_PADDING + 10 * SCALE
            y = day * (CELL_SIZE + CELL_PADDING) + CELL_PADDING + top_offset
            if count is not None:
                draw.rounded_rectangle(
                    [x, y, x + CELL_SIZE, y + CELL_SIZE],
                    radius=3 * SCALE,
                    fill=color,
                    outline=border_color
                )
    return img 