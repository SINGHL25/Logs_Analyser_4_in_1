# charts.py


import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image, ImageDraw, ImageFont

def plot_timeline(df: pd.DataFrame):
    if df.empty or "timestamp" not in df.columns:
        return go.Figure()

    fig = px.scatter(
        df,
        x="timestamp",
        y="Source",
        color="level",
        hover_data=["message", "process", "file"],
        title="Log Timeline"
    )
    fig.update_layout(template="plotly_white", xaxis_rangeslider_visible=True)
    return fig

def plot_counts(df: pd.DataFrame):
    if df.empty or "message" not in df.columns:
        return go.Figure()

    counts = df["message"].value_counts().reset_index()
    counts.columns = ["Message", "Count"]

    fig = px.bar(
        counts.head(20),
        x="Message",
        y="Count",
        title="Top Messages",
        text="Count"
    )
    fig.update_layout(template="plotly_white")
    return fig

def draw_root_cause_diagram(df: pd.DataFrame):
    img = Image.new("RGB", (900, 600), "white")
    draw = ImageDraw.Draw(img)

    try:
        font = ImageFont.truetype("arial.ttf", 14)
    except:
        font = ImageFont.load_default()

    if df.empty:
        draw.text((20, 20), "No events found.", fill="black", font=font)
        return img

    events = df["message"].head(5).tolist()
    draw.text((20, 20), "Root Cause Diagram", fill="black", font=font)

    x, y = 50, 80
    for i, ev in enumerate(events):
        draw.rectangle([(x, y + i*60), (x+300, y+40 + i*60)], outline="black", width=2)
        draw.text((x+5, y+10 + i*60), ev[:40], fill="black", font=font)

    return img
