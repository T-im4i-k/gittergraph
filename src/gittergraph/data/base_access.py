# @generated "partially" ChatGPT-4.1: Documentation
"""
Base access layer for git repositories.

Provides a base class for interacting with a git repository using pygit2.
"""

from pathlib import Path

import pygit2


class BaseAccess:  # pylint: disable=too-few-public-methods
    """
    Base class for git repository access.

    Wraps pygit2.Repository and provides a common interface for repository operations.
    """

    def __init__(self, path: Path | str) -> None:
        self.path: Path = Path(path)
        self._repo: pygit2.Repository = pygit2.Repository(str(self.path))
