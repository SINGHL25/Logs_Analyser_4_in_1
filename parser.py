
# parser.py
import re
from datetime import datetime

def parse_log_line(line: str) -> dict | None:
    """
    Parse a single log line into structured data.
    Supports both event logs and alarm logs.
    """

    # --- Alarm pattern ---
    alarm_pattern = re.compile(
        r'(?P<site>[A-Za-z\s]+):(?P<system>[A-Za-z0-9\s]+)\s*'
        r'(?P<alarm_desc>.+?)\s*alarm raised at (?P<datetime>[\d/:\s]+)'
        r'(?:; (?P<status>still active|terminated))?',
        re.IGNORECASE
    )

    # --- Event pattern (generic software/system logs) ---
    event_pattern = re.compile(
        r'(?P<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})'
        r'.*?\t(?P<module>\w+)\t(?P<source>[\w\.]+)\t(?P<line>\d+)'
        r'\t(?P<error_msg>.+?)\t(?P<error_code>\d+)'
    )

    # Try Alarm first
    alarm_match = alarm_pattern.search(line)
    if alarm_match:
        dt_str = alarm_match.group("datetime").strip()
        try:
            dt_obj = datetime.strptime(dt_str, "%d/%m/%Y %H:%M;%S")
        except ValueError:
            dt_obj = dt_str  # keep raw if parsing fails

        return {
            "type": "alarm",
            "site": alarm_match.group("site").strip(),
            "system": alarm_match.group("system").strip(),
            "description": alarm_match.group("alarm_desc").strip(),
            "datetime": dt_obj,
            "status": alarm_match.group("status") or "active"
        }

    # Try Event
    event_match = event_pattern.search(line)
    if event_match:
        return {
            "type": "event",
            "timestamp": event_match.group("timestamp"),
            "module": event_match.group("module"),
            "source": event_match.group("source"),
            "line": int(event_match.group("line")),
            "error_msg": event_match.group("error_msg").strip(),
            "error_code": int(event_match.group("error_code")),
        }

    return None


def parse_log_file(file_path: str) -> list[dict]:
    """
    Parse a full log file into structured list of dicts.
    """
    results = []
    with open(file_path, "r") as f:
        for line in f:
            parsed = parse_log_line(line.strip())
            if parsed:
                results.append(parsed)
    return results

