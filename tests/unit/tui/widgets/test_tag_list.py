# @generated "all" Claude-Sonnet-4.5
"""
Tests for the TagList widget.

Covers tag list display, selection, and event handling.
"""

import pytest
from textual.app import App, ComposeResult
from textual.widgets import Label, ListView

from gittergraph.tui.widgets.tag_list import TagList
from tests.make_models_helper import make_tag


class TagListTestApp(App):
    """
    Minimal test app for TagList widget.

    Provides a simple app context for testing widget behavior.
    """

    def compose(self) -> ComposeResult:
        """Compose the test app with a TagList widget."""
        yield TagList()


def test_tag_list_initialization():
    """
    Test TagList widget initialization.

    Checks that widget initializes with empty tag list.
    """
    widget = TagList()
    assert widget.tags == []
    assert widget.border_title == "   Tags   "


@pytest.mark.asyncio
async def test_tag_list_compose_with_app():
    """
    Test compose method with a running app.

    Checks that ListView widget is created and initialized.
    """
    app = TagListTestApp()
    async with app.run_test() as pilot:
        widget = app.query_one(TagList)
        list_view = widget.query_one(ListView)

        assert list_view is not None
        await pilot.pause()


@pytest.mark.asyncio
async def test_tag_list_show_empty_list():
    """
    Test show method with an empty tag list.

    Checks that ListView is cleared and remains empty.
    """
    app = TagListTestApp()
    async with app.run_test() as pilot:
        widget = app.query_one(TagList)
        list_view = widget.query_one(ListView)

        widget.show([])

        assert widget.tags == []
        assert len(list_view) == 0
        await pilot.pause()


@pytest.mark.asyncio
async def test_tag_list_show_single_tag():
    """
    Test show method with a single tag.

    Checks that tag is displayed correctly in the ListView.
    """
    app = TagListTestApp()
    async with app.run_test() as pilot:
        widget = app.query_one(TagList)
        list_view = widget.query_one(ListView)

        tag = make_tag(name="refs/tags/v1.0.0")
        widget.show([tag])

        assert widget.tags == [tag]
        assert len(list_view) == 1
        await pilot.pause()


@pytest.mark.asyncio
async def test_tag_list_show_multiple_tags():
    """
    Test show method with multiple tags.

    Checks that all tags are displayed in the ListView.
    """
    app = TagListTestApp()
    async with app.run_test() as pilot:
        widget = app.query_one(TagList)
        list_view = widget.query_one(ListView)

        tags = [
            make_tag(name="refs/tags/v1.0.0", target_id="abc123"),
            make_tag(name="refs/tags/v1.1.0", target_id="def456"),
            make_tag(name="refs/tags/v2.0.0", target_id="ghi789"),
        ]
        widget.show(tags)

        assert widget.tags == tags
        assert len(list_view) == 3
        await pilot.pause()


@pytest.mark.asyncio
async def test_tag_list_show_replaces_existing():
    """
    Test show method replaces existing tags.

    Checks that calling show again clears previous tags.
    """
    app = TagListTestApp()
    async with app.run_test() as pilot:
        widget = app.query_one(TagList)
        list_view = widget.query_one(ListView)

        # First show
        tags1 = [make_tag(name="refs/tags/v1.0.0")]
        widget.show(tags1)
        await pilot.pause()
        assert len(list_view) == 1

        # Second show with different tags
        tags2 = [
            make_tag(name="refs/tags/v2.0.0"),
            make_tag(name="refs/tags/v3.0.0"),
        ]
        widget.show(tags2)
        await pilot.pause()

        assert widget.tags == tags2
        assert len(list_view) == 2
        await pilot.pause()


def test_tag_list_get_label():
    """
    Test _get_label static method.

    Checks that label is created correctly with proper styling.
    """
    tag = make_tag(name="refs/tags/v1.0.0")
    label = TagList._get_label(tag)

    assert isinstance(label, Label)
    assert label.has_class("tag-item")


@pytest.mark.parametrize(
    "tag_name,expected_shorthand",
    [
        ("refs/tags/v1.0.0", "v1.0.0"),
        ("refs/tags/v2.0.0", "v2.0.0"),
        ("refs/tags/release-1.0", "release-1.0"),
        ("refs/tags/beta/v1.0.0-beta", "beta/v1.0.0-beta"),
    ],
)
def test_tag_list_get_label_various_names(tag_name, expected_shorthand):
    """
    Test _get_label with various tag names.

    Checks that labels are created correctly for different tag types.
    """
    tag = make_tag(name=tag_name)
    label = TagList._get_label(tag)

    assert isinstance(label, Label)
    assert label.has_class("tag-item")


def test_tag_list_on_list_view_selected_handler():
    """
    Test on_list_view_selected event handler.

    Checks that handler extracts correct tag name and posts message.
    """
    widget = TagList()
    tags = [
        make_tag(name="refs/tags/v1.0.0"),
        make_tag(name="refs/tags/v2.0.0"),
    ]
    widget.tags = tags

    # Mock the post_message method to capture the message
    posted_messages = []

    def mock_post_message(message):
        posted_messages.append(message)

    widget.post_message = mock_post_message

    # Create a mock event with the index attribute
    class MockEvent:
        def __init__(self, idx):
            self.index = idx

    # Test with index 0
    event = MockEvent(0)
    widget.on_list_view_selected(event)

    assert len(posted_messages) == 1
    assert isinstance(posted_messages[0], TagList.TagSelected)
    assert posted_messages[0].name == "refs/tags/v1.0.0"


def test_tag_list_tag_selected_message():
    """
    Test TagSelected message initialization.

    Checks that message is created with correct tag name.
    """
    message = TagList.TagSelected("refs/tags/v1.0.0")
    assert message.name == "refs/tags/v1.0.0"


@pytest.mark.parametrize(
    "index,expected_name",
    [
        (0, "refs/tags/v1.0.0"),
        (1, "refs/tags/v2.0.0"),
        (2, "refs/tags/v3.0.0"),
    ],
)
def test_tag_list_on_list_view_selected_indices(index, expected_name):
    """
    Test on_list_view_selected with different indices.

    Checks that correct tag name is extracted for each index.
    """
    widget = TagList()
    widget.tags = [
        make_tag(name="refs/tags/v1.0.0"),
        make_tag(name="refs/tags/v2.0.0"),
        make_tag(name="refs/tags/v3.0.0"),
    ]

    # Mock the post_message method to capture the message
    posted_messages = []

    def mock_post_message(message):
        posted_messages.append(message)

    widget.post_message = mock_post_message

    # Create a mock event with the index attribute
    class MockEvent:
        def __init__(self, idx):
            self.index = idx

    event = MockEvent(index)
    widget.on_list_view_selected(event)

    assert len(posted_messages) == 1
    assert posted_messages[0].name == expected_name
