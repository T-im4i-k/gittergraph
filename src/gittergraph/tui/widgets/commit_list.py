# @generated "partially" ChatGPT-4.1: Documentation
"""
Commit list widget for the TUI.

Displays a selectable list of commits in a vertical layout for the TUI, including branch and tag decorations.
"""

from rich.text import Text
from textual.containers import Vertical
from textual.message import Message
from textual.widgets import Label, ListItem, ListView

from gittergraph.models import Branch, Commit, Tag


class CommitList(Vertical):
    """
    Widget for displaying a list of commits in the TUI.

    Shows commit short IDs, messages, and decorations for branches and tags in a selectable list.
    Posts a message when a commit is selected.
    """

    DEFAULT_CSS = """
    CommitList {
        width: 1fr;
        border: solid $primary;
        overflow-y: auto;
        scrollbar-size: 0 0;
    }

    CommitList > ListView {
        height: 100%;
        scrollbar-size: 0 0;
    }

    .commit-item {
        height: auto;
        padding: 0 1;
    }

    .selected-commit {
        background: $boost;
    }
    """

    class CommitSelected(Message):
        """
        Message sent when a commit is selected.

        Contains the ID of the selected commit.
        """

        def __init__(self, commit_id: str) -> None:
            super().__init__()
            self.id: str = commit_id

    def __init__(self, **kwargs) -> None:
        """
        Initialize the CommitList widget.

        Sets up the widget for displaying a list of commits with branch and tag decorations.
        """
        super().__init__(**kwargs)
        self.commits: list[Commit] = []
        self.branches_by_commit: dict[str, list[Branch]] = {}
        self.tags_by_commit: dict[str, list[Tag]] = {}

    def compose(self):
        """
        Yield the ListView widget for displaying commits.

        Called by Textual to build the widget tree.
        """
        yield ListView()

    def show(
        self,
        commits: list[Commit],
        branches_by_commit: dict[str, list[Branch]],
        tags_by_commit: dict[str, list[Tag]],
    ) -> None:
        """
        Display a list of commits with branch and tag decorations.

        Updates the ListView with the provided commits and their associated branches and tags.
        """
        self.commits = commits
        self.branches_by_commit = branches_by_commit
        self.tags_by_commit = tags_by_commit

        list_view: ListView = self.query_one(ListView)
        list_view.clear()

        for commit in self.commits:
            label: Label = self._get_label(commit)
            list_view.append(ListItem(label))

    def _get_label(self, commit: Commit) -> Label:
        """
        Create a label for a commit, including branch and tag decorations.

        Returns a styled Label widget for the given commit.
        """
        header: Text = self._get_header_text(commit)
        body: Text = CommitList._get_body_text(commit)

        label = Label(header + body)
        label.add_class("commit-item")
        return label

    @staticmethod
    def _get_body_text(commit: Commit) -> Text:
        """
        Build the body text for a commit label.

        Returns a rich Text object with the commit message and author.
        """
        text: Text = Text()
        text.append("\n│ ", style="bold yellow")
        text.append(commit.short_message)
        text.append("\n┴ " if commit.is_root else "\n│ ", style="bold yellow")
        text.append(f"\n  {commit.author.name}", style="dim")
        return text

    def _get_header_text(self, commit: Commit) -> Text:
        """
        Build the header text for a commit label, including branch and tag decorations.

        Returns a rich Text object with the commit short ID and decorations.
        """
        text = Text()
        text.append("● ", style="bold yellow")
        text.append(f"{commit.short_id} ", style="cyan")

        if commit.id in self.branches_by_commit:
            branches: list[Branch] = self.branches_by_commit[commit.id]
            for branch in branches:
                text.append(f"[{branch.shorthand}] ", style="bold green")

        if commit.id in self.tags_by_commit:
            tags: list[Tag] = self.tags_by_commit[commit.id]
            for tag in tags:
                text.append(f"<{tag.shorthand}> ", style="bold magenta")

        return text

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        """
        Handle selection of a commit in the list.

        Posts a CommitSelected message with the selected commit ID.
        """
        commit_id: str = self.commits[event.index].id
        self.post_message(self.CommitSelected(commit_id))
