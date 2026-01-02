# @generated "partially" ChatGPT-4.1: Documentation
"""
Commit detail view widget for the TUI.

Displays detailed information about a selected commit in a scrollable widget for the TUI.
"""

from rich.text import Text
from textual.containers import VerticalScroll
from textual.widgets import Static

from gittergraph.models import Commit


class CommitDetail(VerticalScroll):
    """
    Scrollable widget for commit details in the TUI.

    Shows commit metadata, author/committer info, dates, message, and parents.
    """

    CSS_PATH: str = ".style/commit_detail.tcss"
    DEFAULT_TEXT: str = "Select a commit to view details"

    def __init__(self, **kwargs) -> None:
        """
        Initialize the CommitDetail widget.

        Sets up the widget for displaying commit details.
        """
        super().__init__(**kwargs)
        self.commit: Commit | None = None
        self._content_widget: Static | None = None

    def on_mount(self) -> None:
        """
        Mount the content widget.

        Prepares the widget for displaying commit details.
        """
        self._content_widget = Static(CommitDetail.DEFAULT_TEXT)
        self.mount(self._content_widget)

    def show(self, commit: Commit) -> None:
        """
        Display details for a commit.

        Updates the widget to show the given commit's details.
        """
        if not self._content_widget:
            return

        self.commit = commit
        content: Text = self._get_text()
        self._content_widget.update(content)

    def _get_text(self) -> Text:
        """
        Build the rich Text object with commit details.

        Returns a rich Text object containing commit metadata and message.
        """
        if not self.commit:
            return Text(CommitDetail.DEFAULT_TEXT)

        content: Text = Text()
        content.append(f"Commit: {self.commit.id}\n", style="bold cyan")

        style: str = "yellow"
        if self.commit.author_is_committer:
            content.append(
                f"Author/Committer: {str(self.commit.author)}\n", style=style
            )
            content.append(f"Date: {self.commit.author.datetime}\n", style=style)
        else:
            content.append(f"Author: {str(self.commit.author)}\n", style=style)
            content.append(f"Author Date: {self.commit.author.datetime}\n", style=style)
            content.append(f"Committer: {str(self.commit.committer)}\n", style=style)
            content.append(
                f"Committer Date: {self.commit.committer.datetime}\n", style=style
            )

        content.append("\n")
        content.append(self.commit.message)

        if self.commit.parent_ids:
            content.append("\n\n")
            content.append(
                f"Parents: {[p[:7] for p in self.commit.parent_ids]}", style="dim"
            )

        return content

    def clear(self) -> None:
        """
        Clear the detail view.

        Resets the widget to its default state.
        """
        self.commit = None
        if self._content_widget:
            self._content_widget.update(CommitDetail.DEFAULT_TEXT)
