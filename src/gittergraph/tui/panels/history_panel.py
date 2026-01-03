# @generated "all" Claude-Sonnet-4.5
"""
History panel for the TUI.

Displays commit history and detailed commit view in a vertical layout.
"""

from textual.containers import Vertical

from gittergraph.models import Branch, Commit, Tag
from gittergraph.tui.widgets import CommitDetail, CommitHistory


class HistoryPanel(Vertical):
    """
    Panel for displaying commit history.

    Shows commit history list and detailed view in a vertical layout.
    """

    DEFAULT_CSS = """
    HistoryPanel {
        width: 1fr;
    }
    """

    def compose(self):
        """
        Yield widgets for displaying commit history.

        Called by Textual to build the widget tree.
        """
        yield CommitHistory(id="commit-history")
        yield CommitDetail(id="commit-detail")

    def show(
        self,
        commits: list[Commit],
        branches_by_commit: dict[str, list[Branch]],
        tags_by_commit: dict[str, list[Tag]],
    ) -> None:
        """
        Display commit history with decorations.

        Updates the history list and shows details for the first commit if available.
        """
        commit_history = self.query_one("#commit-history", CommitHistory)
        commit_history.show(commits, branches_by_commit, tags_by_commit)

        detail = self.query_one("#commit-detail", CommitDetail)
        if commits:
            detail.show(commits[0])
        else:
            detail.clear()
