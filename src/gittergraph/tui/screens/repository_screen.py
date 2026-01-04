# @generated "partially" ChatGPT-4.1: Documentation
"""
Repository screen for the TUI.

Defines the main screen for displaying the git repository, including commit history and repository references.
"""

from textual.containers import Horizontal
from textual.screen import Screen
from textual.widgets import ListView

from gittergraph.core import GitGraph
from gittergraph.models import Branch, Commit, HeadInfo, Tag
from gittergraph.tui.panels import HistoryPanel, RefPanel
from gittergraph.tui.widgets import (
    BranchList,
    CommitDetail,
    CommitHistory,
    HeadDetail,
    TagList,
)


class RepositoryScreen(Screen):
    """
    Main screen for displaying git repository.

    Shows commit history and repository references in a horizontal layout.
    Handles user interactions for selecting commits, branches, tags, and HEAD.
    """

    BINDINGS = [
        ("c", "focus_history", "Focus History"),
        ("d", "focus_detail", "Focus Detail"),
        ("h", "focus_head", "Focus HEAD"),
        ("b", "focus_branches", "Focus Branches"),
        ("t", "focus_tags", "Focus Tags"),
    ]

    CSS_PATH = "./style/repository_screen.tcss"

    def __init__(self, **kwargs) -> None:
        """
        Initialize the RepositoryScreen.

        Sets up the screen for displaying git repository data.
        """
        super().__init__(**kwargs)
        self.graph: GitGraph | None = None

    def compose(self):
        """
        Yield panels for displaying git repository.

        Called by Textual to build the widget tree. Composes the HistoryPanel and RefPanel in a horizontal layout.
        """
        with Horizontal():
            yield HistoryPanel(id="history-panel")
            yield RefPanel(id="ref-panel")

    def show(self, graph: GitGraph) -> None:
        """
        Display git graph data.

        Updates both panels with repository data from the graph.
        """
        self.graph = graph
        head: HeadInfo = graph.data.head_info
        branches: list[Branch] = list(graph.data.branches.values())
        tags: list[Tag] = list(graph.data.tags.values())

        self._update_ref_panel(head, branches, tags)
        self._update_history_panel("HEAD")

    def _update_ref_panel(
        self, head: HeadInfo, branches: list[Branch], tags: list[Tag]
    ) -> None:
        """
        Update the reference panel with HEAD, branches, and tags.

        Updates the RefPanel with the provided repository references.
        """
        self.query_one("#ref-panel", RefPanel).show(head, branches, tags)

    def _update_history_panel(self, start_ref: str) -> None:
        """
        Update the history panel with commits from a starting reference.

        Retrieves linear history and decorates commits with branches and tags.
        """
        if not self.graph:
            return

        commits: list[Commit] = self.graph.get_linear_history(start_ref)
        branches_by_commit: dict[str, list[Branch]] = {
            commit.id: self.graph.get_branches_at_commit(commit.id)
            for commit in commits
        }
        tags_by_commit: dict[str, list[Tag]] = {
            commit.id: self.graph.get_tags_at_commit(commit.id) for commit in commits
        }

        self.query_one("#history-panel", HistoryPanel).show(
            commits, branches_by_commit, tags_by_commit
        )

    def on_commit_history_commit_selected(
        self, message: CommitHistory.CommitSelected
    ) -> None:
        """
        Handle commit selection event from CommitHistory widget.

        Updates the commit detail view with the selected commit.
        """
        if not self.graph:
            return

        commit: Commit = self.graph.data.commits[message.id]
        self.query_one("#commit-detail", CommitDetail).show(commit)

    def on_branch_list_branch_selected(
        self, message: BranchList.BranchSelected
    ) -> None:
        """
        Handle branch selection event from BranchList widget.

        Updates the history panel to show commits for the selected branch.
        """
        self._update_history_panel(message.name)

    def on_tag_list_tag_selected(self, message: TagList.TagSelected) -> None:
        """
        Handle tag selection event from TagList widget.

        Updates the history panel to show commits for the selected tag.
        """
        self._update_history_panel(message.name)

    def on_head_detail_head_selected(self, _: HeadDetail.HeadSelected) -> None:
        """
        Handle HEAD selection event from HeadDetail widget.

        Updates the history panel to show commits for HEAD.
        """
        self._update_history_panel("HEAD")

    def action_focus_history(self) -> None:
        """
        Focus the commit history widget.

        Activated by the 'c' key binding.
        """
        commit_history: CommitHistory = self.query_one("#commit-history", CommitHistory)
        commit_history.query_one(ListView).focus()

    def action_focus_detail(self) -> None:
        """
        Focus the commit detail widget.

        Activated by the 'd' key binding.
        """
        self.query_one("#commit-detail", CommitDetail).focus()

    def action_focus_head(self) -> None:
        """
        Focus the HEAD detail widget.

        Activated by the 'h' key binding.
        """
        self.query_one("#head-detail", HeadDetail).focus()

    def action_focus_branches(self) -> None:
        """
        Focus the branch list widget.

        Activated by the 'b' key binding.
        """
        branch_list: BranchList = self.query_one("#branch-list", BranchList)
        branch_list.query_one(ListView).focus()

    def action_focus_tags(self) -> None:
        """
        Focus the tag list widget.

        Activated by the 't' key binding.
        """
        tag_list: TagList = self.query_one("#tag-list", TagList)
        tag_list.query_one(ListView).focus()
