
# parser.py
# parser.py
import re
import pandas as pd

def parse_logs(text: str) -> pd.DataFrame:
    """
    Parse general tolling logs (timestamps, modules, errors, etc.)
    """
    pattern = re.compile(
        r"(?P<Timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\s+"
        r"(?P<Module>\w+)\s+"
        r"(?P<SourceFile>\w+\.cpp)\s+"
        r"(?P<LineNo>\d+)\s+"
        r"(?P<ErrorMessage>.+?)\s+"
        r"(?P<SystemErrorCode>\d+)\s+"
        r"(?P<AdditionalInfo>.+)"
    )

    entries = [m.groupdict() for m in pattern.finditer(text)]
    return pd.DataFrame(entries)

def parse_alarm_summary(text: str) -> pd.DataFrame:
    """
    Parse alarm events (Device, Alarm, Severity, Status, Dates).
    """
    pattern = re.compile(
        r"(?P<DeviceName>\w+)\s+"
        r"(?P<AlarmName>[\w\s]+)\s+"
        r"(?P<Severity>\w+)\s+"
        r"(?P<Status>\w+)\s+"
        r"(?P<RaiseDate>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\s+"
        r"(?P<TerminatedDate>[\d-:\s]+)?"
    )

    entries = [m.groupdict() for m in pattern.finditer(text)]
    return pd.DataFrame(entries)

