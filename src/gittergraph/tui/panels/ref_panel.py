# @generated "all" Claude-Sonnet-4.5
"""
Reference panel for the TUI.

Displays repository references (HEAD, branches, and tags) in a vertical layout for navigation.
"""

from textual.containers import Vertical

from gittergraph.models import Branch, HeadInfo, Tag
from gittergraph.tui.widgets import BranchList, HeadDetail, TagList


class RefPanel(Vertical):
    """
    Panel for displaying repository references.

    Shows HEAD, branches, and tags in a vertical layout for quick navigation and selection.
    """

    DEFAULT_CSS = """
    RefPanel {
        width: 30;
    }
    """

    def compose(self):
        """
        Yield widgets for displaying repository references.

        Called by Textual to build the widget tree.
        """
        yield HeadDetail(id="head-detail")
        yield BranchList(id="branch-list")
        yield TagList(id="tag-list")

    def show(self, head: HeadInfo, branches: list[Branch], tags: list[Tag]) -> None:
        """
        Display repository references.

        Updates all child widgets with the provided HEAD, branches, and tags.
        """
        self.query_one("#head-detail", HeadDetail).show(head)
        self.query_one("#branch-list", BranchList).show(branches)
        self.query_one("#tag-list", TagList).show(tags)
