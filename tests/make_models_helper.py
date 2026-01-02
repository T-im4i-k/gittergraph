# @generated "all" ChatGPT-4.1
"""
Helpers for model tests.

Provides utility functions for constructing model objects in tests.
"""

from gittergraph.models import Branch, Commit, Signature


def make_branch(**kwargs):
    """
    Create a Branch instance for testing.

    Returns a Branch with default or provided attributes.
    """
    return Branch(
        target_id=kwargs.get("target_id", "abc1234567890"),
        name=kwargs.get("name", "refs/heads/main"),
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


def make_commit(**kwargs):
    """
    Create a Commit instance for testing.

    Returns a Commit with default or provided attributes.
    """
    return Commit(
        id=kwargs.get("id", "abc1234567890abcdef"),
        message=kwargs.get("message", "Test commit message"),
        author=kwargs.get("author", make_signature()),
        committer=kwargs.get("committer", make_signature()),
        parent_ids=kwargs.get("parent_ids", []),
    )
