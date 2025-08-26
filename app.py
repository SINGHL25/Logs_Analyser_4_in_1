
# app.py
# app.py
import streamlit as st
import pandas as pd
from parser import parse_logs, parse_alarm_summary

st.set_page_config(page_title="🚦 Tolling System Log Parser", layout="wide")

st.title("🚦 Tolling System Log Parser")

# Input choice
choice = st.radio("Choose input method:", ["Upload File", "Paste Logs"])

logs = ""

if choice == "Upload File":
    uploaded_file = st.file_uploader("Upload log file", type=["txt", "log"])
    if uploaded_file is not None:
        # Read full file content
        logs = uploaded_file.read().decode("utf-8", errors="ignore")
elif choice == "Paste Logs":
    logs = st.text_area("Paste logs here:")

# Process logs if provided
if logs.strip():
    with st.spinner("Parsing logs..."):
        df_logs = parse_logs(logs)
        df_alarms = parse_alarm_summary(logs)

    if not df_logs.empty:
        st.subheader("📜 Parsed Log Entries")
        st.dataframe(df_logs, use_container_width=True)
        st.download_button("📥 Download Logs CSV", df_logs.to_csv(index=False), "parsed_logs.csv")

    if not df_alarms.empty:
        st.subheader("🚨 Alarm Summary")
        st.dataframe(df_alarms, use_container_width=True)
        st.download_button("📥 Download Alarm CSV", df_alarms.to_csv(index=False), "alarms.csv")

    if df_logs.empty and df_alarms.empty:
        st.warning("No recognizable log entries found.")
