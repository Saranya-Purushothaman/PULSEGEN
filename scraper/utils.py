from dateutil import parser
from datetime import date

def parse_date_safe(date_str):
    try:
        return parser.parse(date_str).date()
    except Exception:
        return None

def validate_date_range(start, end):
    if start > end:
        raise ValueError("Start date cannot be after end date")

def safe_text(element):
    return element.get_text(strip=True) if element else ""
