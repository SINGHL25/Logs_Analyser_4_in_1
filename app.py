
# app.py
# app.py
# import streamlit as st
# from parser import parse_logs
# from charts import plot_timeline, plot_counts, draw_root_cause_diagram

# st.title("🚦 Tolling System Unified Log Parser")

# option = st.radio("Choose input method:", ["Upload File", "Paste Logs"])

# logs = ""
# if option == "Upload File":
#     uploaded_file = st.file_uploader("Upload log file", type=["txt", "log"])
#     if uploaded_file:
#         logs = uploaded_file.read().decode("utf-8", errors="ignore")
# elif option == "Paste Logs":
#     logs = st.text_area("Paste your logs here")

# if logs:
#     df = parse_logs(logs)

#     if df.empty:
#         st.warning("⚠️ No matching log entries found.")
#     else:
#         st.success(f"✅ Parsed {len(df)} log entries")
#         st.dataframe(df, use_container_width=True)

#         # Charts
#         st.plotly_chart(plot_timeline(df), use_container_width=True)
#         st.plotly_chart(plot_counts(df), use_container_width=True)

#         # Root Cause
#         st.image(draw_root_cause_diagram(df), caption="Root Cause Diagram")


