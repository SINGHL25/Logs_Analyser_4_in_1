# utils/visuals.py
import plotly.express as px
import pandas as pd

def plot_timeline(df: pd.DataFrame):
    """
    Plot timeline of alarms/events per device over time
    """
    if df.empty:
        return {}
    fig = px.scatter(
        df,
        x="Timestamp",
        y="Device",
        color="Severity",
        hover_data=["Message", "File", "LineNo"],
        title="Device Alarm Timeline"
    )
    fig.update_layout(yaxis={'categoryorder':'total ascending'})
    return fig

def plot_counts(df: pd.DataFrame):
    """
    Plot counts of severity levels
    """
    if df.empty:
        return {}
    counts = df.groupby("Severity").size().reset_index(name="Count")
    fig = px.bar(
        counts,
        x="Severity",
        y="Count",
        color="Severity",
        title="Severity Counts",
        text="Count"
    )
    return fig

def plot_alarm_trends(df: pd.DataFrame, freq="D"):
    """
    Plot alarm trends over time.
    freq: 'D' = daily, 'W' = weekly, 'M' = monthly
    """
    if df.empty:
        return {}
    trend_df = df.set_index("Timestamp").resample(freq).size().reset_index(name="Count")
    fig = px.line(
        trend_df,
        x="Timestamp",
        y="Count",
        title=f"Alarms Trend ({'Daily' if freq=='D' else 'Weekly' if freq=='W' else 'Monthly'})"
    )
    return fig
