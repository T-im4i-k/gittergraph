# @generated "partially" ChatGPT-4.1: Documentation
"""
Tag list widget for the TUI.

Displays a selectable list of tags in a vertical layout for the TUI.
"""

from rich.text import Text
from textual.containers import Vertical
from textual.message import Message
from textual.widgets import Label, ListItem, ListView

from gittergraph.models import Tag


class TagList(Vertical):
    """
    Widget for displaying a list of tags in the TUI.

    Shows tag names in a selectable list and posts a message when a tag is selected.
    """

    # Widgets should use inline TCSS for styling.
    DEFAULT_CSS = """
    TagList {
        border: solid $primary;
        overflow-y: auto;
        scrollbar-size: 0 0;
    }

    TagList > ListView {
        height: 100%;
        scrollbar-size: 0 0;
    }

    .tag-item {
        height: auto;
        padding: 0 1;
        color: $warning;
    }
    """

    class TagSelected(Message):
        """
        Message sent when a tag is selected.

        Contains the name of the selected tag.
        """

        def __init__(self, name: str) -> None:
            super().__init__()
            self.name: str = name

    def __init__(self, **kwargs) -> None:
        """
        Initialize the TagList widget.

        Sets up the widget for displaying a list of tags.
        """
        super().__init__(**kwargs)
        self.tags: list[Tag] = []
        self.border_title: str = "Tags"

    def compose(self):
        """
        Yield the ListView widget for displaying tags.

        Called by Textual to build the widget tree.
        """
        yield ListView()

    def show(self, tags: list[Tag]) -> None:
        """
        Display a list of tags.

        Updates the ListView with the provided tags.
        """
        self.tags = tags
        list_view: ListView = self.query_one(ListView)
        list_view.clear()

        for tag in self.tags:
            label: Label = TagList._get_label(tag)
            list_view.append(ListItem(label))

    @staticmethod
    def _get_label(tag: Tag) -> Label:
        """
        Create a label for a tag.

        Returns a styled Label widget for the given tag.
        """
        text: Text = Text()
        text.append("  ", style="dim")
        text.append(tag.shorthand, style="magenta")
        label: Label = Label(text)
        label.add_class("tag-item")
        return label

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        """
        Handle selection of a tag in the list.

        Posts a TagSelected message with the selected tag name.
        """
        tag_name: str = self.tags[event.index].name
        self.post_message(self.TagSelected(tag_name))
