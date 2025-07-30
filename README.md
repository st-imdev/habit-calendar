# Habit Tracker

A minimalist row-based habit tracker that automatically updates daily and displays your last three weeks of habits as a clean, embeddable image.

## What This Does

- **Displays 5 core habits** in a compact row-based layout showing the last 21 days
- **Shows dates in US format** (M/D) for easy daily tracking
- **Auto-updates daily** via GitHub Actions with realistic random data
- **Shows progression** - habits get more consistent over time (60% → 90% success rate)
- **Serves tracker images** via FastAPI for embedding anywhere (perfect for blog headers)

## Quick Start

1. **View your calendar**: 
   ```bash
   python -m uvicorn app:app --reload --port 8000
   ```
   Then visit: http://localhost:8000

2. **Manual habit update** (for testing):
   ```bash
   python update_habits.py
   ```

## How It Works

### Automatic Updates
- **GitHub Actions** runs daily at noon UTC
- Adds new habit data with smart progression (gets more consistent over time)
- Commits updated `habit_data.json` back to your repo
- No local server needed - runs entirely on GitHub's infrastructure

### Tracked Habits (5 Core Habits)
- **Water**: Easiest (+20% success bonus) - Stay hydrated
- **Journal**: Pretty easy (+10% bonus) - Daily reflection
- **Meditate**: Baseline difficulty - Mindfulness practice
- **Read**: Baseline difficulty - Knowledge & growth
- **Exercise**: Hardest (-10% penalty) - Physical fitness

### API Endpoints
- `GET /` - Web interface showing both light/dark themes
- `GET /calendar.png?theme=light` - Light theme calendar image
- `GET /calendar.png?theme=dark` - Dark theme calendar image

## Files

- **`app.py`** - FastAPI web server
- **`habit_calendar.py`** - Calendar image generation logic
- **`habit_data.json`** - Your habit data (auto-updated daily)
- **`update_habits.py`** - Standalone script for adding daily habits
- **`.github/workflows/update-habits.yml`** - GitHub Actions automation

## Manual Operations

### Add Custom Habit Data
Edit `habit_data.json` directly:
```json
{
  "2025-07-23": {
    "exercise": true,
    "read": false,
    "meditate": true,
    "water": true,
    "journal": true,
    "walk": true
  }
}
```

### Test GitHub Actions Locally
```bash
python update_habits.py
```

### Stop Auto-Updates
Delete or disable `.github/workflows/update-habits.yml`

### Change Update Schedule
Edit the cron expression in the workflow file:
```yaml
schedule:
  - cron: '0 12 * * *'  # Daily at noon UTC
```

## Embedding the Calendar

Use the image URLs in:
- **README files**: `![Habits](https://your-domain.com/calendar.png)`
- **Websites**: `<img src="https://your-domain.com/calendar.png">`
- **Slack/Discord**: Just paste the URL

## Troubleshooting

### Server won't start
```bash
# Kill any existing processes
pkill -f uvicorn
# Start fresh
python -m uvicorn app:app --reload --port 8000
```

### Missing habit data
```bash
# Manually add today's data
python update_habits.py
```

### GitHub Actions not running
- Check the Actions tab in your GitHub repo
- Ensure the workflow file is in `.github/workflows/`
- Manually trigger via GitHub's web interface

## Customization

### Change Habit Types
Edit the `HABITS_TO_TRACK` list in `habit_calendar.py` and the `habit_probs` dictionary in `update_habits.py`:
```python
# In habit_calendar.py
HABITS_TO_TRACK = ["exercise", "read", "meditate", "water", "journal"]

# In update_habits.py
habit_probs = {
    "water": current_prob + 0.2,
    "your_habit": current_prob,  # Add new habits here
}
```

### Adjust Progression Rate
Modify `improvement_rate` in `update_habits.py`:
```python
improvement_rate = 0.5 / 365  # Improve by 50% over the year
```

### Change Colors/Themes
Edit the color constants in `habit_calendar.py`:
```python
# Light theme colors
LIGHT_COMPLETED_COLOR = (64, 196, 99)  # Green for completed
LIGHT_MISSED_COLOR = (248, 248, 246)   # Light beige for missed

# Dark theme colors  
DARK_COMPLETED_COLOR = (74, 126, 255)  # Blue for completed
DARK_MISSED_COLOR = (48, 54, 61)       # Dark gray for missed
```

## Development

### Requirements
```bash
pip install -r requirements.txt
```

### Local Development
```bash
python -m uvicorn app:app --reload --port 8000
```

The calendar will automatically reflect any changes to `habit_data.json`. 