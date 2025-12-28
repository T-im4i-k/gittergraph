# @generated "all" ChatGPT-4.1
"""
Tests for data models for git objects.

Covers all classes and properties in model.py.
"""
from datetime import datetime, timedelta, timezone

import pytest

from gittergraph.data.model import (
    AnnotatedTag,
    Branch,
    Commit,
    LightweightTag,
    Signature,
    Tag,
)


def make_signature(**kwargs):
    """
    Create a Signature instance for testing.

    Returns a Signature with default or provided attributes.
    """
    return Signature(
        name=kwargs.get("name", "Alice"),
        email=kwargs.get("email", "alice@example.com"),
        time=kwargs.get("time", 1700000000),
        time_offset=kwargs.get("time_offset", 60),
    )


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
    "name,expected_shorthand",
    [
        ("refs/tags/v1.0", "v1.0"),
        ("refs/tags/release", "release"),
        ("v2.0", "v2.0"),
    ],
)
def test_tag_shorthand(name, expected_shorthand):
    """
    Test Tag shorthand property.

    Checks removal of refs/tags/ prefix.
    """
    t = Tag(target_id="id", name=name)
    assert t.shorthand == expected_shorthand


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
    b = Branch(target_id="id", name=name, is_head=False)
    assert b.is_remote is is_remote
    assert b.shorthand == expected_shorthand


@pytest.mark.parametrize(
    "target_id,name,expected_shorthand",
    [
        ("id", "refs/tags/v1.0", "v1.0"),
        ("id2", "refs/tags/release", "release"),
    ],
)
def test_lightweight_tag_inheritance(target_id, name, expected_shorthand):
    """
    Test LightweightTag inheritance.

    Checks that LightweightTag is a subclass of Tag and has correct shorthand.
    """
    t = LightweightTag(target_id=target_id, name=name)
    assert isinstance(t, Tag)
    assert t.shorthand == expected_shorthand


@pytest.mark.parametrize(
    "target_id,name,tag_id,message,tagger_args",
    [
        (
            "id",
            "refs/tags/v1.0",
            "tid",
            "msg",
            {"name": "Tagger", "email": "tagger@x.com"},
        ),
        (
            "id2",
            "refs/tags/release",
            "tid2",
            "release message",
            {"name": "Other", "email": "other@x.com"},
        ),
    ],
)
def test_annotated_tag_fields(target_id, name, tag_id, message, tagger_args):
    """
    Test AnnotatedTag fields.

    Checks that AnnotatedTag stores tag_id, message, and tagger.
    """
    tagger = make_signature(**tagger_args)
    t = AnnotatedTag(
        target_id=target_id, name=name, tag_id=tag_id, message=message, tagger=tagger
    )
    assert t.tag_id == tag_id
    assert t.message == message
    assert t.tagger == tagger
