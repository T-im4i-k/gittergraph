# @generated "partially" Claude-Sonnet-4.5: Code
# @generated "partially" ChatGPT-4.1: Documentation
"""
Reference name resolution.

Provides the RefResolver class for resolving reference names (branches, tags, HEAD, commit IDs) to commit IDs for graph operations.
"""

from gittergraph.models import Branch, Commit, HeadInfo, Tag


class RefResolver:  # pylint: disable=too-few-public-methods
    """
    Helper for resolving reference names to commit IDs.

    Handles resolution of branches, tags, commit IDs, and HEAD.
    """

    def __init__(
        self,
        commits: dict[str, Commit],
        branches: dict[str, Branch],
        tags: dict[str, Tag],
        head_info: HeadInfo,
    ) -> None:
        """
        Initialize reference resolver.

        Stores dictionaries of commits, branches, tags, and HEAD info for resolution.
        """
        self.commits: dict[str, Commit] = commits
        self.branches: dict[str, Branch] = branches
        self.tags: dict[str, Tag] = tags
        self.head_info: HeadInfo = head_info

    def resolve(self, ref: str) -> str | None:
        """
        Resolve a reference name to a commit ID.

        Handles HEAD, commit IDs, branch names, and tag names. Returns None if the reference cannot be resolved.
        """
        match ref:
            case "HEAD":
                return self.head_info.target_id
            case _ if ref in self.commits:
                return ref
            case _ if ref in self.branches:
                return self.branches[ref].target_id
            case _ if ref in self.tags:
                return self.tags[ref].target_id
            case _:
                return None
