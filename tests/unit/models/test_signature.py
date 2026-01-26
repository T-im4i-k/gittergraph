# @generated "all" ChatGPT-4.1
"""
Tests for the Signature model.

Covers signature formatting and datetime conversion logic.
"""

from datetime import datetime, timedelta, timezone

import pytest

from tests.make_models_helper import make_signature


@pytest.mark.parametrize(
    "sig_args,expected_str",
    [
        ({"name": "Bob", "email": "bob@x.com"}, "Bob <bob@x.com>"),
        ({"name": "Eve", "email": "eve@evil.com"}, "Eve <eve@evil.com>"),
    ],
)
def test_signature_str(sig_args, expected_str):
    """
    Test Signature string formatting.

    Checks __str__ output for various names and emails.
    """
    sig = make_signature(**sig_args)
    assert str(sig) == expected_str


@pytest.mark.parametrize(
    "sig_args,expected_dt",
    [
        (
            {"time": 0, "time_offset": 0},
            datetime(1970, 1, 1, 0, 0, tzinfo=timezone.utc),
        ),
        (
            {"time": 3600, "time_offset": 60},
            datetime(1970, 1, 1, 2, 0, tzinfo=timezone(timedelta(minutes=60))),
        ),
    ],
)
def test_signature_datetime(sig_args, expected_dt):
    """
    Test Signature datetime conversion.

    Checks conversion to timezone-aware datetime.
    """
    sig = make_signature(**sig_args)
    dt = sig.datetime
    assert dt == expected_dt
    assert dt.tzinfo is not None
