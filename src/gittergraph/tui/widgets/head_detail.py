# @generated "all" Claude-Sonnet-4.5
"""
HEAD widget for the TUI.

Displays the current HEAD reference as a clickable element in a vertical layout for the TUI.
"""

from rich.text import Text
from textual.containers import Vertical
from textual.message import Message
from textual.widgets import Static

from gittergraph.models import HeadInfo


class HeadDetail(Vertical):
    """
    Widget for displaying HEAD in the TUI.

    Shows the HEAD reference as a clickable element and posts a message when clicked.
    """

    # Widgets should use inline TCSS for styling.
    DEFAULT_CSS = """
    HeadDetail {
        width: 30;
        border: solid $primary;
        height: auto;
    }
    
    HeadDetail > Static {
        height: auto;
        padding: 0 1;
        color: $accent;
    }
    
    HeadDetail > Static:hover {
        background: $boost;
    }
    """
    DEFAULT_TEXT: str = "Not set"

    class HeadSelected(Message):
        """
        Message sent when HEAD is clicked.

        Contains the HEAD reference.
        """

    def __init__(self, **kwargs) -> None:
        """
        Initialize the HeadDetail.

        Sets up the widget for displaying HEAD.
        """
        super().__init__(**kwargs)
        self.head: HeadInfo | None = None
        self.border_title: str = "HEAD"

    def compose(self):
        """
        Yield the Static widget for displaying HEAD.

        Called by Textual to build the widget tree.
        """
        yield Static(HeadDetail.DEFAULT_TEXT)

    def show(self, head: HeadInfo) -> None:
        """
        Display HEAD information.

        Updates the Static widget with the provided HEAD reference.
        """
        self.head = head
        text: Text = self._get_text()
        self.query_one(Static).update(text)

    def _get_text(self) -> Text:
        """
        Build the rich Text object with HEAD information.

        Returns a rich Text object containing HEAD reference or default text if not set.
        """
        if not self.head:
            return Text(HeadDetail.DEFAULT_TEXT, style="dim")

        text: Text = Text()
        text.append("  ", style="dim")
        text.append("→ ", style="cyan bold")

        if self.head.branch_name:
            text.append(self.head.branch_name, style="cyan")
        elif self.head.target_id:
            text.append(self.head.target_id[:7], style="yellow")
        else:
            text.append("unborn", style="dim")

        return text

    def on_click(self) -> None:
        """
        Handle click on HEAD widget.

        Posts a HeadSelected message with the HEAD reference.
        """
        if self.head and self.head.target_id:
            self.post_message(self.HeadSelected())
