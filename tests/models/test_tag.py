# @generated "all" ChatGPT-4.1
"""
Tests for the Tag, LightweightTag, and AnnotatedTag models.

Covers tag property logic including shorthand extraction and tag metadata.
"""


import pytest
from helper import make_signature

from gittergraph.models import AnnotatedTag, LightweightTag
from gittergraph.models.tag import Tag


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
