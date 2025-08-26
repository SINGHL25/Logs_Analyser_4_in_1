
# app.py
import streamlit as st
import pandas as pd
from parser import LogParser

st.set_page_config(page_title="Tolling Log Parser", layout="wide")

st.title("🚦 Tolling System Log Parser")
parser = LogParser()

# Option to upload file or paste logs
mode = st.radio("Choose input method:", ["Upload File", "Paste Logs"])

df = pd.DataFrame()

if mode == "Upload File":
    uploaded = st.file_uploader("Upload log file", type=["txt", "log"])
    if uploaded is not None:
        text = uploaded.read().decode("utf-8")
        df = parser.parse_text(text)

elif mode == "Paste Logs":
    text = st.text_area("Paste raw log text here")
    if st.button("Parse Logs") and text.strip():
        df = parser.parse_text(text)

if not df.empty:
    st.success(f"Parsed {len(df)} log entries ✅")
    st.dataframe(df, use_container_width=True)

    # Download option
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Download CSV",
        data=csv,
        file_name="parsed_logs.csv",
        mime="text/csv"
    )
