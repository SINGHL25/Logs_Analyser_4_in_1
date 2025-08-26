# parser.py
import re
import pandas as pd
from datetime import datetime

class LogParser:
    def __init__(self):
        # Regex pattern to extract key fields (adjust as per actual logs)
        self.pattern = re.compile(
            r'(?P<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d+)\s+'
            r'(?P<device>\w+)\s+'
            r'(?P<module>[\w\.]+)\s+'
            r'(?P<line>\d+)\s+'
            r'(?P<message>.+)'
        )

    def parse_line(self, line: str):
        """Parse one log line into structured dict"""
        match = self.pattern.search(line)
        if match:
            return match.groupdict()
        return None

    def parse_file(self, filepath: str) -> pd.DataFrame:
        """Parse a full log file into DataFrame"""
        records = []
        with open(filepath, "r", encoding="utf-8") as f:
            for line in f:
                parsed = self.parse_line(line)
                if parsed:
                    records.append(parsed)
        return pd.DataFrame(records)

    def parse_text(self, text: str) -> pd.DataFrame:
        """Parse multiline log text"""
        records = []
        for line in text.strip().split("\n"):
            parsed = self.parse_line(line)
            if parsed:
                records.append(parsed)
        return pd.DataFrame(records)

