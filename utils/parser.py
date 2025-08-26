# utils/parser.py
import pandas as pd
import re
from datetime import datetime

LOG_PATTERN = re.compile(
    r'(?P<Timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\s+'
    r'(?P<Device>\w+)\s+'
    r'(?P<File>\S+)\s+'
    r'(?P<LineNo>\d+)\s+'
    r'(?P<Message>.+?)\s+'
    r'(?P<SystemCode>\d+)\s+'
    r'(?P<Additional>.*)'
)

def parse_log_file(file_path: str) -> pd.DataFrame:
    """
    Parse log file and return structured DataFrame.
    Columns: Timestamp, Device, File, LineNo, Message, SystemCode, Additional, Severity
    """
    records = []
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            match = LOG_PATTERN.match(line)
            if match:
                record = match.groupdict()
                # Convert timestamp
                try:
                    record["Timestamp"] = pd.to_datetime(record["Timestamp"])
                except Exception:
                    continue
                # Extract severity from message (simple rule)
                msg_upper = record["Message"].upper()
                if "ERROR" in msg_upper:
                    record["Severity"] = "Error"
                elif "WARN" in msg_upper:
                    record["Severity"] = "Warning"
                elif "ALARM" in msg_upper:
                    record["Severity"] = "Alarm"
                else:
                    record["Severity"] = "Info"
                
                records.append(record)
    df = pd.DataFrame(records)
    return df

