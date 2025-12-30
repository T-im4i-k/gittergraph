# @generated "all" ChatGPT-4.1
"""
Helpers for model tests.

Provides utility functions for constructing model objects in tests.
"""


from gittergraph.models import Signature


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
