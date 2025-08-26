# app.py
import streamlit as st
import pandas as pd
from utils.parser import parse_log_file
from utils.visuals import plot_timeline, plot_counts, plot_alarm_trends

st.set_page_config(page_title="Toll/ITS Log Analyzer", layout="wide")

st.title("🚦 Toll/ITS Log Analyzer")
st.markdown("Upload a log file to visualize alarms, severity, and trends.")

# File upload
uploaded_file = st.file_uploader("Choose a log file", type=["txt", "log"])

if uploaded_file:
    # Save uploaded file temporarily
    with open("temp_log.txt", "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    # Parse log file
    df = parse_log_file("temp_log.txt")
    
    if df.empty:
        st.warning("No valid log lines found in the file.")
    else:
        st.success(f"Parsed {len(df)} log entries successfully!")
        
        # Show raw DataFrame
        with st.expander("📄 Raw Data"):
            st.dataframe(df)
        
        # Sidebar filters
        st.sidebar.header("Filter Logs")
        devices = df["Device"].unique()
        selected_devices = st.sidebar.multiselect("Select Devices", devices, default=devices)
        
        severities = df["Severity"].unique()
        selected_severities = st.sidebar.multiselect("Select Severity", severities, default=severities)
        
        filtered_df = df[df["Device"].isin(selected_devices) & df["Severity"].isin(selected_severities)]
        
        st.subheader("📊 Alarm Timeline")
        timeline_fig = plot_timeline(filtered_df)
        st.plotly_chart(timeline_fig, use_container_width=True)
        
        st.subheader("📊 Severity Counts")
        counts_fig = plot_counts(filtered_df)
        st.plotly_chart(counts_fig, use_container_width=True)
        
        st.subheader("📈 Alarm Trends Over Time")
        freq_option = st.selectbox("Trend Frequency", options=["Daily", "Weekly", "Monthly"])
        freq_map = {"Daily": "D", "Weekly": "W", "Monthly": "M"}
        trend_fig = plot_alarm_trends(filtered_df, freq=freq_map[freq_option])
        st.plotly_chart(trend_fig, use_container_width=True)
        try:
    import plotly.express as px
except ModuleNotFoundError:
    import streamlit as st
    st.error("Plotly is missing. Add `plotly` to requirements.txt and redeploy.")




