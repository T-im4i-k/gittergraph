# @generated "partially" ChatGPT-4.1: Documentation
# @generated "partially" Claude-Sonnet-4.5: Code
"""
Repository access operations.

Provides unified access to all git repository data through specialized access layers.
"""

from pathlib import Path

import pygit2

from gittergraph.access.branch_access import BranchAccess
from gittergraph.access.commit_access import CommitAccess
from gittergraph.access.head_access import HeadAccess
from gittergraph.access.tag_access import TagAccess


class GitRepository:
    """
    Git repository access operations.

    Provides a unified interface to all repository data access operations
    through specialized access layers for commits, branches, tags, and HEAD.
    """

    def __init__(self, path: str | Path) -> None:
        """
        Initialize repository access.

        Sets up repository and access layers for commits, branches, tags, and HEAD.
        """
        self.path: Path = Path(path)
        self._repo: pygit2.Repository = pygit2.Repository(str(self.path))

        # Initialize access components
        self.commits: CommitAccess = CommitAccess(self.path)
        self.branches: BranchAccess = BranchAccess(self.path)
        self.tags: TagAccess = TagAccess(self.path)
        self.head: HeadAccess = HeadAccess(self.path)

    @classmethod
    def discover(cls, start_path: str | Path = ".") -> "GitRepository | None":
        """
        Discover a git repository starting from a directory.

        Searches upward from start_path for a .git directory and returns a GitRepository instance if found.
        """
        repo_path: str | None = pygit2.discover_repository(str(start_path))
        return cls(repo_path) if repo_path is not None else None

    def reload(self):
        """
        Reload repository to detect external changes.

        Reinitializes all access layers with a fresh repository object.
        """
        self._repo = pygit2.Repository(str(self.path))
        self.commits = CommitAccess(self.path)
        self.branches = BranchAccess(self.path)
        self.tags = TagAccess(self.path)
        self.head = HeadAccess(self.path)

    def is_empty(self) -> bool:
        """
        Check if repository has no commits.

        Returns True if the repository is empty, otherwise False.
        """
        return self._repo.is_empty
