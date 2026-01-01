# @generated "partially" Claude-Sonnet-4.5: Code
# @generated "partially" ChatGPT-4.1: Documentation
"""
Commit history traversal.

Provides the HistoryWalker class for traversing commit graphs and building history sequences for visualization.
"""

from gittergraph.models import Commit


class HistoryWalker:  # pylint: disable=too-few-public-methods
    """
    Helper for traversing commit history.

    Provides methods for walking first-parent chains and other traversals.
    """

    def __init__(self, commits: dict[str, Commit]) -> None:
        """
        Initialize history walker.

        Stores the commit dictionary for traversal operations.
        """
        self.commits: dict[str, Commit] = commits

    def get_linear_history_from_commit(self, commit_id: str) -> list[Commit]:
        """
        Get linear first-parent history starting from a commit.

        Follows the first parent chain from the given commit, returning commits in newest-first order.
        """
        history: list[Commit] = []
        current_id: str = commit_id

        while current_id in self.commits:
            commit: Commit = self.commits[current_id]
            history.append(commit)

            if commit.parent_ids:
                current_id = commit.parent_ids[0]
            else:
                break

        return history
