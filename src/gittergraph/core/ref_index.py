# @generated "partially" Claude-Sonnet-4.5: Code
# @generated "partially" ChatGPT-4.1: Documentation
"""
Reference indexing for fast lookups.

Provides the RefIndex class for building and maintaining indexes that map commit IDs to their associated branches and tags.
"""

from gittergraph.models import Branch, Tag


class RefIndex:
    """
    Index for fast lookups of references by commit ID.

    Builds and maintains dictionaries mapping commits to their branches and tags.
    """

    def __init__(self, branches: dict[str, Branch], tags: dict[str, Tag]):
        """
        Initialize reference index.

        Builds indexes mapping commit IDs to branches and tags for fast lookups.
        """
        self._branches_by_commit: dict[str, list[Branch]] = {}
        self._tags_by_commit: dict[str, list[Tag]] = {}
        self._build_index_branches(branches)
        self._build_index_tags(tags)

    def _build_index_branches(self, branches: dict[str, Branch]):
        """
        Build index mapping commit IDs to branches.

        Creates a reverse index from commit IDs to lists of branches pointing to them.
        """
        for branch in branches.values():
            target: str = branch.target_id
            if target not in self._branches_by_commit:
                self._branches_by_commit[target] = []
            self._branches_by_commit[target].append(branch)

    def _build_index_tags(self, tags: dict[str, Tag]):
        """
        Build index mapping commit IDs to tags.

        Creates a reverse index from commit IDs to lists of tags pointing to them.
        """
        for tag in tags.values():
            target: str = tag.target_id
            if target not in self._tags_by_commit:
                self._tags_by_commit[target] = []
            self._tags_by_commit[target].append(tag)

    def get_branches_at_commit(self, commit_id: str) -> list[Branch]:
        """
        Get all branches pointing to a commit.

        Returns an empty list if no branches point to the commit.
        """
        return self._branches_by_commit.get(commit_id, [])

    def get_tags_at_commit(self, commit_id: str) -> list[Tag]:
        """
        Get all tags pointing to a commit.

        Returns an empty list if no tags point to the commit.
        """
        return self._tags_by_commit.get(commit_id, [])
