# @generated "all" Claude-Sonnet-4.5
"""
Repository data snapshot.

Provides the GitGraphData dataclass for representing an immutable snapshot of repository data loaded from a Git repository.
"""

from dataclasses import dataclass

from gittergraph.access import GitRepository
from gittergraph.models import Branch, Commit, HeadInfo, Tag


@dataclass(slots=True, frozen=True)
class GitGraphData:
    """
    Repository data snapshot.

    Immutable snapshot of commits, branches, tags, and HEAD info loaded from a repository.
    """

    commits: dict[str, Commit]
    branches: dict[str, Branch]
    tags: dict[str, Tag]
    head_info: HeadInfo

    @classmethod
    def load_from(cls, repo: GitRepository) -> "GitGraphData":
        """
        Load repository data.

        Retrieves all commits, branches, tags, and HEAD info from the repository.
        """
        return cls(
            commits=repo.commits.get_all(),
            branches=repo.branches.get_all(),
            tags=repo.tags.get_all(),
            head_info=repo.head.get_info(),
        )
