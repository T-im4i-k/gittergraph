# @generated "all" ChatGPT-4.1
"""
Helpers for model tests.

Provides utility functions for constructing model objects in tests.
"""

from gittergraph.models import Commit, Signature


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
