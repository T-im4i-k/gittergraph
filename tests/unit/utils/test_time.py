# @generated "all" ChatGPT-4.1
"""
Tests for time utility functions.

Covers helpers for working with time.
"""

from datetime import datetime, timedelta, timezone

import pytest

from gittergraph.utils.time import unix_timestamp_to_datetime


@pytest.mark.parametrize(
    "timestamp, offset, expected",
    [
        # UTC
        (1609459200, 0, datetime(2021, 1, 1, 0, 0, 0, tzinfo=timezone.utc)),
        # Positive offset (+1 hour)
        (
            1609459200,
            60,
            datetime(2021, 1, 1, 1, 0, 0, tzinfo=timezone(timedelta(minutes=60))),
        ),
        # Negative offset (-2 hours)
        (
            1609459200,
            -120,
            datetime(2020, 12, 31, 22, 0, 0, tzinfo=timezone(timedelta(minutes=-120))),
        ),
        # Default offset (should be UTC)
        (1609459200, None, datetime(2021, 1, 1, 0, 0, 0, tzinfo=timezone.utc)),
    ],
)
def test_unix_timestamp_to_datetime_parametrized(timestamp, offset, expected):
    """
    Convert a Unix timestamp and offset to a timezone-aware datetime.

    Checks that the function returns the correct datetime for various timestamps and offsets, including UTC, positive, negative, and default offsets.
    """
    if offset is None:
        result = unix_timestamp_to_datetime(timestamp)
    else:
        result = unix_timestamp_to_datetime(timestamp, offset)
    assert result == expected
