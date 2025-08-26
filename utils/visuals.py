import plotly.express as px
import pandas as pd

def plot_timeline(df, time_col="Raise Date", severity_col="Severity"):
    """
    Creates a timeline chart of log events by severity.
    """
    df = df.dropna(subset=[time_col])
    fig = px.scatter(df, x=time_col, y=severity_col, color=severity_col,
                     title="Timeline of Events", hover_data=["Message", "Device Name", "File"])
    fig.update_traces(marker=dict(size=10))
    fig.update_layout(height=400)
    return fig

def plot_counts(df, severity_col="Severity"):
    """
    Creates a bar chart of counts per severity.
    """
    count_df = df.groupby(severity_col).size().reset_index(name="Count")
    fig = px.bar(count_df, x=severity_col, y="Count", color=severity_col,
                 title="Count of Events by Severity", text="Count")
    fig.update_layout(height=400)
    return fig

def draw_root_cause_diagram(df, msg_col="Message"):
    """
    Creates a simple root cause diagram (top 10 recurring messages).
    """
    top_msgs = df[msg_col].value_counts().nlargest(10).reset_index()
    top_msgs.columns = ["Root Cause", "Count"]
    fig = px.bar(top_msgs, x="Root Cause", y="Count", color="Count",
                 title="Top 10 Root Causes", text="Count")
    fig.update_layout(height=400, xaxis_tickangle=-45)
    return fig
