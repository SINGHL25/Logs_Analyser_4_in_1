# app.py
# app.py
import streamlit as st

# Safe imports with error handling
try:
    import pandas as pd
    import numpy as np
except ModuleNotFoundError as e:
    st.error(f"Missing package: {e.name}. Please add it to requirements.txt")
    raise

try:
    from utils.parser import parse_logs
except ModuleNotFoundError:
    st.error("utils.parser module not found")
    raise

try:
    from utils.visuals import plot_timeline, plot_counts, plot_alarm_trends
except ModuleNotFoundError:
    st.warning("utils.visuals module missing or Plotly not installed")
    plot_timeline = plot_counts = plot_alarm_trends = None

st.set_page_config(page_title="Logs Analyser 4-in-1", layout="wide")

st.title("📊 Logs Analyser 4-in-1")

uploaded_file = st.file_uploader("Upload log file", type=["log", "txt", "csv"])

if uploaded_file:
    try:
        raw_text = uploaded_file.read().decode("utf-8")
        logs_df = parse_logs(raw_text)
        st.success("✅ Logs parsed successfully!")
        
        st.subheader("Preview of logs")
        st.dataframe(logs_df.head(10))

        if plot_timeline:
            st.subheader("Timeline plot")
            st.plotly_chart(plot_timeline(logs_df), use_container_width=True)

        if plot_counts:
            st.subheader("Counts plot")
            st.plotly_chart(plot_counts(logs_df), use_container_width=True)

        if plot_alarm_trends:
            st.subheader("Alarm trends")
            st.plotly_chart(plot_alarm_trends(logs_df), use_container_width=True)
    except Exception as e:
        st.error(f"Error parsing file: {str(e)}")
else:
    st.info("Upload a log file to get started.")





