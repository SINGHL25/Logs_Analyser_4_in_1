
# app.py
import streamlit as st
from parser import parse_logs

st.title("🚦 Tolling System VDC Log Parser")

option = st.radio("Choose input method:", ["Upload File", "Paste Logs"])

if option == "Upload File":
    uploaded_file = st.file_uploader("Upload log file", type=["txt", "log"])
    if uploaded_file:
        content = uploaded_file.read().decode("utf-8", errors="ignore")
        df = parse_logs(content)
        if df.empty:
            st.warning("⚠️ No matching log entries found.")
        else:
            st.success(f"✅ Parsed {len(df)} log entries")
            st.dataframe(df, use_container_width=True)

elif option == "Paste Logs":
    logs = st.text_area("Paste your logs here")
    if logs:
        df = parse_logs(logs)
        if df.empty:
            st.warning("⚠️ No matching log entries found.")
        else:
            st.success(f"✅ Parsed {len(df)} log entries")
            st.dataframe(df, use_container_width=True)

