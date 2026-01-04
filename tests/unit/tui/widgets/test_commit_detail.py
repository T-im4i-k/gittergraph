# @generated "all" Claude-Sonnet-4.5
"""
Tests for the CommitDetail widget.

Covers commit detail display, clearing, and text formatting for different commit types.
"""

import pytest
from rich.text import Text
from textual.app import App, ComposeResult

from gittergraph.tui.widgets.commit_detail import CommitDetail
from tests.make_models_helper import make_commit, make_signature


class CommitDetailTestApp(App):
    """
    Minimal test app for CommitDetail widget.

    Provides a simple app context for testing widget behavior.
    """

    def compose(self) -> ComposeResult:
        """Compose the test app with a CommitDetail widget."""
        yield CommitDetail()


def test_commit_detail_initialization():
    """
    Test CommitDetail widget initialization.

    Checks that widget initializes with None commit.
    """
    widget = CommitDetail()
    assert widget.commit is None


def test_commit_detail_get_text_with_commit_same_author_committer():
    """
    Test _get_text method with same author and committer.

    Checks that rich Text object is built correctly when author equals committer.
    """
    widget = CommitDetail()
    sig = make_signature()
    widget.commit = make_commit(author=sig, committer=sig, id="abcdef123456")

    text = widget._get_text()
    assert isinstance(text, Text)
    assert "Commit: abcdef123456" in text.plain
    assert "Author/Committer:" in text.plain
    assert "Alice" in text.plain
    assert "alice@example.com" in text.plain
    assert "Test commit message" in text.plain


def test_commit_detail_get_text_with_commit_different_author_committer():
    """
    Test _get_text method with different author and committer.

    Checks that both author and committer are displayed separately.
    """
    widget = CommitDetail()
    author = make_signature(name="Alice")
    committer = make_signature(name="Bob", email="bob@example.com")
    widget.commit = make_commit(author=author, committer=committer)

    text = widget._get_text()
    assert isinstance(text, Text)
    assert "Author:" in text.plain
    assert "Committer:" in text.plain
    assert "Alice" in text.plain
    assert "Bob" in text.plain


def test_commit_detail_get_text_with_parents():
    """
    Test _get_text method with parent commits.

    Checks that parent commit IDs are displayed.
    """
    widget = CommitDetail()
    parent_ids = ["abc1234567890", "def9876543210"]
    widget.commit = make_commit(parent_ids=parent_ids)

    text = widget._get_text()
    assert isinstance(text, Text)
    assert "Parents:" in text.plain
    assert "abc1234" in text.plain
    assert "def9876" in text.plain


def test_commit_detail_get_text_without_parents():
    """
    Test _get_text method without parent commits.

    Checks that root commits don't display parent information.
    """
    widget = CommitDetail()
    sig = make_signature()
    widget.commit = make_commit(author=sig, committer=sig, parent_ids=[])

    text = widget._get_text()
    assert isinstance(text, Text)
    assert "Parents:" not in text.plain


def test_commit_detail_get_text_without_commit():
    """
    Test _get_text method without a commit.

    Checks that default text is returned when commit is None.
    """
    widget = CommitDetail()
    widget.commit = None

    text = widget._get_text()
    assert isinstance(text, Text)
    assert text.plain == CommitDetail.DEFAULT_TEXT


@pytest.mark.parametrize(
    "message,expected_in_text",
    [
        ("Short message", "Short message"),
        ("Multi\nline\nmessage", "Multi\nline\nmessage"),
        ("Message with special chars: @#$%", "Message with special chars: @#$%"),
    ],
)
def test_commit_detail_get_text_various_messages(message, expected_in_text):
    """
    Test _get_text method with various commit messages.

    Checks that different message formats are displayed correctly.
    """
    widget = CommitDetail()
    sig = make_signature()
    widget.commit = make_commit(message=message, author=sig, committer=sig)

    text = widget._get_text()
    assert expected_in_text in text.plain


@pytest.mark.asyncio
async def test_commit_detail_show_with_app():
    """
    Test show method with a running app.

    Checks that show updates the widget correctly in app context.
    """
    app = CommitDetailTestApp()
    async with app.run_test() as pilot:
        widget = app.query_one(CommitDetail)

        sig = make_signature()
        commit = make_commit(author=sig, committer=sig)
        widget.show(commit)

        assert widget.commit == commit
        await pilot.pause()


@pytest.mark.asyncio
async def test_commit_detail_clear_with_app():
    """
    Test clear method with a running app.

    Checks that clear resets commit and displays default text.
    """
    app = CommitDetailTestApp()
    async with app.run_test() as pilot:
        widget = app.query_one(CommitDetail)

        commit = make_commit()
        widget.show(commit)
        assert widget.commit is not None

        widget.clear()
        assert widget.commit is None
        await pilot.pause()


@pytest.mark.asyncio
async def test_commit_detail_compose_with_app():
    """
    Test compose method with a running app.

    Checks that Static widget is created and initialized with default text.
    """
    from textual.widgets import Static

    app = CommitDetailTestApp()
    async with app.run_test() as pilot:
        widget = app.query_one(CommitDetail)
        static = widget.query_one(Static)

        assert static is not None
        await pilot.pause()


@pytest.mark.parametrize(
    "commit_id,expected_short",
    [
        ("abc1234567890abcdef", "abc1234567890abcdef"),
        ("123456789012345678901234567890", "123456789012345678901234567890"),
    ],
)
def test_commit_detail_get_text_various_commit_ids(commit_id, expected_short):
    """
    Test _get_text method with various commit IDs.

    Checks that commit IDs are displayed correctly.
    """
    widget = CommitDetail()
    sig = make_signature()
    widget.commit = make_commit(id=commit_id, author=sig, committer=sig)

    text = widget._get_text()
    assert f"Commit: {expected_short}" in text.plain
