# @generated "partially" ChatGPT-4.1: Documentation
"""
Time utility functions.

Provides helpers for working with time.
"""

from datetime import datetime, timedelta, timezone


def unix_timestamp_to_datetime(timestamp: int, offset: int = 0) -> datetime:
    """
    Convert a Unix timestamp to a timezone-aware datetime.

    Takes a Unix timestamp and an optional timezone offset in minutes, returning a datetime object with the correct timezone applied.
    """
    tz = timezone(timedelta(minutes=offset))
    return datetime.fromtimestamp(timestamp, tz)
