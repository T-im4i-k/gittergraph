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

    # Widgets should use inline TCSS for styling.
    DEFAULT_CSS = """
    CommitDetail {
        width: 1fr;
        border: solid $primary;
        padding: 1;
        scrollbar-size: 0 0;
    }

    CommitDetail > Static {
        width: 100%;
    }
    """
    DEFAULT_TEXT: str = "Select a commit to view details"

    def __init__(self, **kwargs) -> None:
        """
        Initialize the CommitDetail widget.

        Sets up the widget for displaying commit details. The content widget is created in compose().
        """
        super().__init__(**kwargs)
        self.commit: Commit | None = None
        self.border_title: str = "Commit Details"

    def compose(self):
        """
        Yield the Static widget for displaying commit details.

        This method is called by Textual to build the widget tree.
        """
        yield Static(CommitDetail.DEFAULT_TEXT)

    def show(self, commit: Commit) -> None:
        """
        Display details for a commit.

        Updates the internal commit reference and updates the Static child with commit details.
        """
        self.commit = commit
        text: Text = self._get_text()
        self.query_one(Static).update(text)

    def _get_text(self) -> Text:
        """
        Build the rich Text object with commit details.

        Returns a rich Text object containing commit metadata and message, or the default text if no commit is set.
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

        Resets the internal commit reference and updates the Static child to show the default text.
        """
        self.commit = None
        self.query_one(Static).update(CommitDetail.DEFAULT_TEXT)
