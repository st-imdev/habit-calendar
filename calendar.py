from datetime import datetime, timedelta
from PIL import Image, ImageDraw, ImageFont
import json
import os

# Constants for calendar appearance
SCALE = 2
CELL_SIZE = 12 * SCALE
CELL_PADDING = 2 * SCALE
WEEKS = 53
DAYS = 7
WIDTH = WEEKS * (CELL_SIZE + CELL_PADDING) + CELL_PADDING + 20 * SCALE
HEIGHT = DAYS * (CELL_SIZE + CELL_PADDING) + CELL_PADDING + 40  # Extra for title
TITLE = "Habit Commit Calendar"

# GitHub green color palette
COLORS = [
    (235, 237, 240),  # 0 habits (light gray)
    (155, 233, 168),  # 1 habit (lightest green)
    (64, 196, 99),    # 2 habits (light green)
    (48, 161, 78),    # 3 habits (medium green)
    (33, 110, 57),    # 4+ habits (dark green)
]

BG_COLOR = (255, 255, 255)
BORDER_COLOR = (220, 220, 220)
TITLE_COLOR = (36, 41, 46)


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

def get_color(count, max_habits):
    if count is None:
        return BG_COLOR
    if count == 0:
        return COLORS[0]
    # Map count to color index (1-4)
    idx = min(4, int((count / max_habits) * 4))
    idx = max(1, idx)  # Ensure at least 1 for nonzero
    return COLORS[idx]

def generate_calendar_image(habit_data):
    matrix, max_habits, start_of_calendar = get_calendar_matrix(habit_data)
    img = Image.new("RGB", (WIDTH, HEIGHT), BG_COLOR)
    draw = ImageDraw.Draw(img)

    # Draw calendar squares (no title, no border)
    top_offset = 0
    for week in range(WEEKS):
        for day in range(DAYS):
            count = matrix[week][day]
            color = get_color(count, max_habits)
            x = week * (CELL_SIZE + CELL_PADDING) + CELL_PADDING + 10 * SCALE
            y = day * (CELL_SIZE + CELL_PADDING) + CELL_PADDING + top_offset
            if count is not None:
                draw.rounded_rectangle(
                    [x, y, x + CELL_SIZE, y + CELL_SIZE],
                    radius=3 * SCALE,
                    fill=color,
                    outline=BORDER_COLOR
                )
    return img 