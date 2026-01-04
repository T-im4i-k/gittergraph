# @generated "all" Claude-Sonnet-4.5
"""
Tests for the HeadDetail.

Covers HEAD display, clicking, and event handling.
"""

import pytest
from rich.text import Text
from textual.app import App, ComposeResult
from textual.widgets import Static

from gittergraph.models import HeadState
from gittergraph.tui.widgets.head_detail import HeadDetail
from tests.make_models_helper import make_head


class HeadWidgetTestApp(App):
    """
    Minimal test app for HeadDetail.

    Provides a simple app context for testing widget behavior.
    """

    def compose(self) -> ComposeResult:
        """Compose the test app with a HeadDetail."""
        yield HeadDetail()


def test_head_widget_initialization():
    """
    Test HeadDetail initialization.

    Checks that widget initializes with None head.
    """
    widget = HeadDetail()
    assert widget.head is None
    assert widget.border_title == "   HEAD   "


@pytest.mark.asyncio
async def test_head_widget_compose_with_app():
    """
    Test compose method with a running app.

    Checks that Static widget is created and initialized.
    """
    app = HeadWidgetTestApp()
    async with app.run_test() as pilot:
        widget = app.query_one(HeadDetail)
        static = widget.query_one(Static)

        assert static is not None
        await pilot.pause()


@pytest.mark.asyncio
async def test_head_widget_show_with_app():
    """
    Test show method with a running app.

    Checks that HEAD is displayed correctly.
    """
    app = HeadWidgetTestApp()
    async with app.run_test() as pilot:
        widget = app.query_one(HeadDetail)

        head = make_head(reference="refs/heads/main")
        widget.show(head)

        assert widget.head == head
        await pilot.pause()


def test_head_widget_get_text_with_head():
    """
    Test _get_text method with a HEAD.

    Checks that rich Text object is built correctly.
    """
    widget = HeadDetail()
    head = make_head(reference="refs/heads/main")
    widget.head = head

    text = widget._get_text()
    assert isinstance(text, Text)
    assert "refs/heads/main" in text.plain
    assert "→" in text.plain


def test_head_widget_get_text_without_head():
    """
    Test _get_text method without a HEAD.

    Checks that default text is returned when head is None.
    """
    widget = HeadDetail()
    widget.head = None

    text = widget._get_text()
    assert isinstance(text, Text)
    assert "Not set" in text.plain


@pytest.mark.parametrize(
    "reference",
    [
        "refs/heads/main",
        "refs/heads/develop",
        "refs/heads/feature/new-feature",
    ],
)
def test_head_widget_get_text_various_references(reference):
    """
    Test _get_text with various HEAD references.

    Checks that different reference types are displayed correctly.
    """
    widget = HeadDetail()
    head = make_head(branch_name=reference)
    widget.head = head

    text = widget._get_text()
    assert isinstance(text, Text)
    assert reference in text.plain


def test_head_widget_on_click_handler():
    """
    Test on_click event handler.

    Checks that handler posts HeadSelected message with correct reference.
    """
    widget = HeadDetail()
    head = make_head(reference="refs/heads/main")
    widget.head = head

    # Mock the post_message method to capture the message
    posted_messages = []

    def mock_post_message(message):
        posted_messages.append(message)

    widget.post_message = mock_post_message

    # Trigger the click handler
    widget.on_click()

    assert len(posted_messages) == 1
    assert isinstance(posted_messages[0], HeadDetail.HeadSelected)


def test_head_widget_on_click_without_head():
    """
    Test on_click when no HEAD is set.

    Checks that no message is posted when head is None.
    """
    widget = HeadDetail()
    widget.head = None

    # Mock the post_message method to capture the message
    posted_messages = []

    def mock_post_message(message):
        posted_messages.append(message)

    widget.post_message = mock_post_message

    # Trigger the click handler
    widget.on_click()

    assert len(posted_messages) == 0


def test_head_widget_head_selected_message():
    """
    Test HeadSelected message initialization.

    Checks that message is created without parameters.
    """
    message = HeadDetail.HeadSelected()
    assert isinstance(message, HeadDetail.HeadSelected)


@pytest.mark.parametrize(
    "branch_name",
    [
        "refs/heads/main",
        "refs/heads/develop",
        "refs/heads/feature",
    ],
)
def test_head_widget_on_click_various_references(branch_name):
    """
    Test on_click with different HEAD references.

    Checks that HeadSelected message is posted for each reference.
    """
    widget = HeadDetail()
    head = make_head(branch_name=branch_name)
    widget.head = head

    # Mock the post_message method to capture the message
    posted_messages = []

    def mock_post_message(message):
        posted_messages.append(message)

    widget.post_message = mock_post_message

    # Trigger the click handler
    widget.on_click()

    assert len(posted_messages) == 1
    assert isinstance(posted_messages[0], HeadDetail.HeadSelected)


def test_head_widget_get_text_detached():
    """
    Test _get_text with detached HEAD.

    Checks that detached HEAD shows commit hash.
    """
    widget = HeadDetail()
    head = make_head(
        state=HeadState.DETACHED, branch_name=None, target_id="abc1234567890"
    )
    widget.head = head

    text = widget._get_text()
    assert isinstance(text, Text)
    assert "abc1234" in text.plain
    assert "→" in text.plain


def test_head_widget_get_text_unborn():
    """
    Test _get_text with unborn HEAD.

    Checks that unborn HEAD shows appropriate message.
    """
    widget = HeadDetail()
    head = make_head(state=HeadState.UNBORN, branch_name=None, target_id=None)
    widget.head = head

    text = widget._get_text()
    assert isinstance(text, Text)
    assert "unborn" in text.plain


def test_head_widget_on_click_detached():
    """
    Test on_click with detached HEAD.

    Checks that HeadSelected message is posted for detached HEAD.
    """
    widget = HeadDetail()
    head = make_head(
        state=HeadState.DETACHED, branch_name=None, target_id="abc1234567890"
    )
    widget.head = head

    # Mock the post_message method to capture the message
    posted_messages = []

    def mock_post_message(message):
        posted_messages.append(message)

    widget.post_message = mock_post_message

    # Trigger the click handler
    widget.on_click()

    # Message should be posted for detached HEAD
    assert len(posted_messages) == 1
    assert isinstance(posted_messages[0], HeadDetail.HeadSelected)


def test_head_widget_on_click_unborn():
    """
    Test on_click with unborn HEAD.

    Checks that no message is posted when HEAD is unborn (no commits yet).
    """
    widget = HeadDetail()
    head = make_head(state=HeadState.UNBORN, branch_name=None, target_id=None)
    widget.head = head

    # Mock the post_message method to capture the message
    posted_messages = []

    def mock_post_message(message):
        posted_messages.append(message)

    widget.post_message = mock_post_message

    # Trigger the click handler
    widget.on_click()

    # No message should be posted for unborn HEAD
    assert len(posted_messages) == 0
