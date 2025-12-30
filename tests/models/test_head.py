# @generated "all" ChatGPT-4.1
"""
Tests for the HeadState enum and HeadInfo dataclass.

Covers HEAD state logic, property checks, and edge cases for HEAD status in a Git repository.
"""

import pytest

from gittergraph.models.head import HeadInfo, HeadState


@pytest.mark.parametrize(
    "state,target_id,branch_name,is_detached",
    [
        (HeadState.NORMAL, "abc123", "main", False),
        (HeadState.DETACHED, "def456", None, True),
        (HeadState.UNBORN, None, None, False),
    ],
)
def test_headinfo_is_detached(state, target_id, branch_name, is_detached):
    """
    Test HeadInfo is_detached property.

    Checks correct detection of detached HEAD state for various scenarios.
    """
    info = HeadInfo(state=state, target_id=target_id, branch_name=branch_name)
    assert info.is_detached is is_detached


@pytest.mark.parametrize(
    "state,expected_str",
    [
        (HeadState.NORMAL, "normal"),
        (HeadState.DETACHED, "detached"),
        (HeadState.UNBORN, "unborn"),
    ],
)
def test_headstate_enum_values(state, expected_str):
    """
    Test HeadState enum values.

    Checks that enum values match expected string representations.
    """
    assert state.value == expected_str
