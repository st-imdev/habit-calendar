from fastapi import FastAPI, Response
from fastapi.responses import HTMLResponse
from habit_calendar import generate_calendar_image, load_habit_data, WIDTH, HEIGHT
import io

app = FastAPI()

@app.get("/calendar.png")
def calendar_png():
    habit_data = load_habit_data()
    img = generate_calendar_image(habit_data)
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return Response(content=buf.getvalue(), media_type="image/png")

@app.get("/", response_class=HTMLResponse)
def index():
    logical_width = WIDTH // 2
    logical_height = HEIGHT // 2
    return f"""
    <html>
      <head><title>Habit Commit Calendar</title></head>
      <body>
        <h1>Habit Commit Calendar</h1>
        <img src='/calendar.png' alt='Habit Calendar' width='{logical_width}' height='{logical_height}' style='image-rendering: crisp-edges;'/>
      </body>
    </html>
    """ 