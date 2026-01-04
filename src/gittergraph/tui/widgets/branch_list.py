# @generated "partially" ChatGPT-4.1: Documentation
"""
Branch list widget for the TUI.

Displays a selectable list of branches in a vertical layout for the TUI.
"""

from rich.text import Text
from textual.containers import Vertical
from textual.message import Message
from textual.widgets import Label, ListItem, ListView

from gittergraph.models import Branch


class BranchList(Vertical):
    """
    Widget for displaying a list of branches in the TUI.

    Shows branch names in a selectable list and posts a message when a branch is selected.
    """

    # Widgets should use inline TCSS for styling.
    DEFAULT_CSS = """
    BranchList {
        border: solid $primary;
        overflow-y: auto;
        scrollbar-size: 0 0;
    }
    
    BranchList > ListView {
        height: 100%;
        scrollbar-size: 0 0;
    }
    
    .branch-item {
        height: auto;
        padding: 0 1;
        color: $success;
    }
    """

    class BranchSelected(Message):
        """
        Message sent when a branch is selected.

        Contains the name of the selected branch.
        """

        def __init__(self, name: str) -> None:
            super().__init__()
            self.name: str = name

    def __init__(self, **kwargs) -> None:
        """
        Initialize the BranchList widget.

        Sets up the widget for displaying a list of branches.
        """
        super().__init__(**kwargs)
        self.branches: list[Branch] = []
        self.border_title = "Branches"

    def compose(self):
        """
        Yield the ListView widget for displaying branches.

        Called by Textual to build the widget tree.
        """
        yield ListView()

    def show(self, branches: list[Branch]) -> None:
        """
        Display a list of branches.

        Updates the ListView with the provided branches.
        """
        self.branches = branches
        list_view: ListView = self.query_one(ListView)
        list_view.clear()

        for branch in self.branches:
            label: Label = BranchList._get_label(branch)
            list_view.append(ListItem(label))

    @staticmethod
    def _get_label(branch: Branch) -> Label:
        """
        Create a label for a branch.

        Returns a styled Label widget for the given branch.
        """
        text: Text = Text()
        text.append("  ", style="dim")
        text.append(branch.shorthand, style="green")
        label: Label = Label(text)
        label.add_class("branch-item")
        return label

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        """
        Handle selection of a branch in the list.

        Posts a BranchSelected message with the selected branch name.
        """
        branch_name: str = self.branches[event.index].name
        self.post_message(self.BranchSelected(branch_name))
