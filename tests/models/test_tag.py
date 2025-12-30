# @generated "all" ChatGPT-4.1
"""
Tests for the Tag, LightweightTag, and AnnotatedTag models.

Covers tag property logic including shorthand extraction and tag metadata.
"""


import pytest

from gittergraph.models import Tag


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
