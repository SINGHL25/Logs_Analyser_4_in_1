
# parser.py
# parser.py
import re
import pandas as pd

# VDC log pattern
VDC_PATTERN = re.compile(
    r'~\|\[\s*'
    r'(?P<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d+)\s+'
    r'(?P<level>[A-Z])\s+'
    r'(?P<process>[^\s]+)?\s*'
    r'(\((?P<pid>\d+)\))?\s+'
    r'(?P<vdctype>[^\s]+)\s+'
    r'(?P<file>[\w\/\.@]+)\s+'
    r'L(?P<line>\d+)\s+'
    r'(?P<version>[\w\.x]+)?\s*'
    r'(?P<message>.+?)\s*'
    r'\]\|~'
)

# VR log pattern
VR_PATTERN = re.compile(
    r'~\|\[\s*'
    r'(?P<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d+)\s+'
    r'(?P<level>[A-Z])\s+'
    r'(?P<pid>\d+)\s+'
    r'(?P<process>[A-Za-z0-9\.\-]+)\s+'
    r'(?P<file>[\w\/\.]+)\s+'
    r'L(?P<line>\d+)\s+'
    r'(?P<message>.+?)\s*'
    r'\]\|~'
)

# ALC log pattern
ALC_PATTERN = re.compile(
    r'~\|\[\s*'
    r'(?P<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d+)\s+'
    r'(?P<level>[A-Z])\s+'
    r'(?P<pid>\d+)\s+'
    r'ALC\s+'
    r'(?P<file>[\w\/\.@]+)\s+'
    r'L(?P<line>\d+)\s+'
    r'(?P<code>0x[0-9A-Fa-f]+)\s+'
    r'(?P<message>.+?)\s*'
    r'\]\|~'
)

def parse_logs(log_text: str) -> pd.DataFrame:
    rows = []

    for line in log_text.splitlines():
        line = line.strip()
        if not line:
            continue

        match = VDC_PATTERN.match(line)
        if match:
            rows.append({**match.groupdict(), "Source": "VDC"})
            continue

        match = VR_PATTERN.match(line)
        if match:
            rows.append({**match.groupdict(), "Source": "VR"})
            continue

        match = ALC_PATTERN.match(line)
        if match:
            rows.append({**match.groupdict(), "Source": "ALC"})
            continue

    return pd.DataFrame(rows)

