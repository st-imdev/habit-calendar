from fastapi import FastAPI, Response, Query
from fastapi.responses import HTMLResponse
from habit_calendar import generate_calendar_image, load_habit_data, WIDTH, HEIGHT
import io

app = FastAPI()

@app.get("/calendar.png")
def calendar_png(theme: str = Query("light", regex="^(light|dark)$")):
    habit_data = load_habit_data()
    img = generate_calendar_image(habit_data, theme=theme)
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return Response(content=buf.getvalue(), media_type="image/png")

@app.get("/", response_class=HTMLResponse)
def index():
    logical_width = WIDTH // 2
    logical_height = HEIGHT // 2
    return f"""
    <html>
      <head>
        <title>Habit Commit Calendar</title>
        <style>
          body {{ font-family: Arial, sans-serif; margin: 40px; }}
          .theme-section {{ margin: 30px 0; }}
          .dark-bg {{ background: #1a1a1a; padding: 20px; border-radius: 8px; }}
          h2 {{ color: #333; }}
          .dark-bg h2 {{ color: #fff; }}
        </style>
      </head>
      <body>
        <h1>Habit Commit Calendar</h1>
        
        <div class="theme-section">
          <h2>Light Theme</h2>
          <img src='/calendar.png?theme=light' alt='Light Habit Calendar' width='{logical_width}' height='{logical_height}' style='image-rendering: crisp-edges;'/>
          <br><small>URL: /calendar.png?theme=light</small>
        </div>
        
        <div class="theme-section dark-bg">
          <h2>Dark Theme</h2>
          <img src='/calendar.png?theme=dark' alt='Dark Habit Calendar' width='{logical_width}' height='{logical_height}' style='image-rendering: crisp-edges;'/>
          <br><small style="color: #ccc;">URL: /calendar.png?theme=dark</small>
        </div>
      </body>
    </html>
    """ 