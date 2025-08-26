import re
import pandas as pd

def parse_log_file(lines):
    """
    Parses log lines into a structured DataFrame.
    Supports TSMC, ALC, VRS style logs.
    """
    records = []
    for line in lines:
        line = line.strip("~|[] \n")
        if not line:
            continue

        # Generic regex for logs
        match = re.match(
            r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d+)\s+"   # Timestamp
            r"([A-Z])\s+"                                       # Severity
            r"(\S+)\s+"                                         # PID/Process
            r"(\S+)\s+"                                         # Device/Module
            r"(\S+)\s+"                                         # File
            r"L(\d+)\s*"                                        # Line
            r"(?:([^\t]+)\t)?"                                  # Optional code/version
            r"(.*)", line)
        if match:
            ts, lvl, pid, device, file, line_no, code, msg = match.groups()
            records.append({
                "Raise Date": pd.to_datetime(ts, errors="coerce"),
                "Severity": lvl,
                "PID": pid,
                "Device Name": device,
                "File": file,
                "Line No": line_no,
                "Code": code if code else "",
                "Message": msg
            })
        else:
            # Fallback for unmatched lines
            records.append({
                "Raise Date": None,
                "Severity": "",
                "PID": "",
                "Device Name": "",
                "File": "",
                "Line No": "",
                "Code": "",
                "Message": line
            })

    df = pd.DataFrame(records)
    return df

def extract_alarm_events(df):
    """
    Filters the logs to extract alarms/events.
    """
    df = df.copy()
    df['is_alarm'] = df['Message'].str.contains(r'Error|Fail|Alarm|CT:', case=False, na=False)
    return df[df['is_alarm']].reset_index(drop=True)
