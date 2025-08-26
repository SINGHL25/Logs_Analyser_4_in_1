
# parser.py
# parser.py
import re
import pandas as pd

LOG_PATTERN = re.compile(
    r'~\|\[\s*'                           # start delimiter
    r'(?P<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d+)\s+'
    r'(?P<level>[A-Z])\s+'
    r'(?P<process>[^\s]+)\s*'
    r'(\((?P<pid>\d+)\))?\s+'             # optional pid
    r'(?P<vdctype>[^\s]+)\s+'
    r'(?P<file>[\w/\.]+)\s+'
    r'L(?P<line>\d+)\s+'
    r'(?P<version>[\w\.]+)\s+'
    r'(?P<message>.+?)\s*'
    r'\]\|~'
)

def parse_logs(log_text):
    matches = LOG_PATTERN.finditer(log_text)
    data = []

    for m in matches:
        data.append({
            "Timestamp": m.group("timestamp"),
            "Level": m.group("level"),
            "Process": m.group("process"),
            "PID": m.group("pid") if m.group("pid") else "",
            "VDC_Type": m.group("vdctype"),
            "File": m.group("file"),
            "Line": m.group("line"),
            "Version": m.group("version"),
            "Message": m.group("message"),
        })

    return pd.DataFrame(data)
