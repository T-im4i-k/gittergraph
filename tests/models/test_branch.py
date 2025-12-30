# @generated "all" ChatGPT-4.1
"""
Tests for the Branch model.

Covers branch property logic including remote detection and shorthand extraction.
"""


import pytest

from gittergraph.models import Branch


@pytest.mark.parametrize(
    "name,is_remote,expected_shorthand",
    [
        ("refs/remotes/origin/main", True, "origin/main"),
        ("refs/heads/dev", False, "dev"),
        ("refs/heads/feature", False, "feature"),
    ],
)
def test_branch_is_remote_and_shorthand(name, is_remote, expected_shorthand):
    """
    Test Branch is_remote and shorthand properties.

    Checks detection of remote branches and shorthand extraction.
    """
    b = Branch(target_id="id", name=name)
    assert b.is_remote is is_remote
    assert b.shorthand == expected_shorthand
