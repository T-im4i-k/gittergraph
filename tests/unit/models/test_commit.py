# @generated "all" ChatGPT-4.1
"""
Tests for the Commit model.

Covers commit property logic including merge/root detection and message handling.
"""


import pytest

from gittergraph.models import Commit
from tests.make_models_helper import make_signature


@pytest.mark.parametrize(
    "parent_ids,is_merge,is_root",
    [
        ([], False, True),
        (["a"], False, False),
        (["a", "b"], True, False),
    ],
)
def test_commit_is_merge_and_is_root(parent_ids, is_merge, is_root):
    """
    Test Commit is_merge and is_root properties.

    Checks detection of merge and root commits.
    """
    c = Commit(
        id="abc1234567890",
        message="msg",
        author=make_signature(),
        committer=make_signature(),
        parent_ids=parent_ids,
    )
    assert c.is_merge is is_merge
    assert c.is_root is is_root


@pytest.mark.parametrize(
    "id_,expected_short_id",
    [
        ("abcdef1234567890", "abcdef1"),
        ("1234567", "1234567"),
        ("a", "a"),
    ],
)
def test_commit_short_id(id_, expected_short_id):
    """
    Test Commit short_id property.

    Checks short hash extraction from commit id.
    """
    c = Commit(
        id=id_,
        message="msg",
        author=make_signature(),
        committer=make_signature(),
        parent_ids=[],
    )
    assert c.short_id == expected_short_id


@pytest.mark.parametrize(
    "message,expected_short_message",
    [
        ("Short message", "Short message"),
        (
            "A very long message that exceeds fifty characters in the first line\nsecond line",
            "A very long message that exceeds fifty characte...",
        ),
        ("First\nSecond", "First"),
    ],
)
def test_commit_short_message(message, expected_short_message):
    """
    Test Commit short_message property.

    Checks truncation and extraction of the first line.
    """
    c = Commit(
        id="id",
        message=message,
        author=make_signature(),
        committer=make_signature(),
        parent_ids=[],
    )
    assert c.short_message == expected_short_message


@pytest.mark.parametrize(
    "author,committer,expected",
    [
        (make_signature, make_signature, True),
        (make_signature, lambda: make_signature(name="Other"), False),
    ],
)
def test_commit_author_is_committer(author, committer, expected):
    """
    Test Commit author_is_committer property using parametrize.
    """
    c = Commit(
        id="id",
        message="msg",
        author=author(),
        committer=committer(),
        parent_ids=[],
    )
    assert c.author_is_committer is expected
