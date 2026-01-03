# @generated "all" Claude-Sonnet-4.5
"""
Tests for the CommitList widget.

Covers commit list display, selection, decorations, and event handling.
"""

import pytest
from textual.app import App, ComposeResult
from textual.widgets import Label, ListView

from gittergraph.tui.widgets.commit_list import CommitList
from tests.make_models_helper import make_branch, make_commit, make_signature, make_tag


class CommitListTestApp(App):
    """
    Minimal test app for CommitList widget.

    Provides a simple app context for testing widget behavior.
    """

    def compose(self) -> ComposeResult:
        """Compose the test app with a CommitList widget."""
        yield CommitList()


def test_commit_list_initialization():
    """
    Test CommitList widget initialization.

    Checks that widget initializes with empty commit, branch, and tag lists.
    """
    widget = CommitList()
    assert widget.commits == []
    assert widget.branches_by_commit == {}
    assert widget.tags_by_commit == {}


@pytest.mark.asyncio
async def test_commit_list_compose_with_app():
    """
    Test compose method with a running app.

    Checks that ListView widget is created and initialized.
    """
    app = CommitListTestApp()
    async with app.run_test() as pilot:
        widget = app.query_one(CommitList)
        list_view = widget.query_one(ListView)

        assert list_view is not None
        await pilot.pause()


@pytest.mark.asyncio
async def test_commit_list_show_empty_list():
    """
    Test show method with an empty commit list.

    Checks that ListView is cleared and remains empty.
    """
    app = CommitListTestApp()
    async with app.run_test() as pilot:
        widget = app.query_one(CommitList)
        list_view = widget.query_one(ListView)

        widget.show([], {}, {})

        assert widget.commits == []
        assert widget.branches_by_commit == {}
        assert widget.tags_by_commit == {}
        assert len(list_view) == 0
        await pilot.pause()


@pytest.mark.asyncio
async def test_commit_list_show_single_commit():
    """
    Test show method with a single commit.

    Checks that commit is displayed correctly in the ListView.
    """
    app = CommitListTestApp()
    async with app.run_test() as pilot:
        widget = app.query_one(CommitList)
        list_view = widget.query_one(ListView)

        commit = make_commit(id="abc1234567890abcdef", message="Initial commit")
        widget.show([commit], {}, {})

        assert widget.commits == [commit]
        assert len(list_view) == 1
        await pilot.pause()


@pytest.mark.asyncio
async def test_commit_list_show_multiple_commits():
    """
    Test show method with multiple commits.

    Checks that all commits are displayed in the ListView.
    """
    app = CommitListTestApp()
    async with app.run_test() as pilot:
        widget = app.query_one(CommitList)
        list_view = widget.query_one(ListView)

        commits = [
            make_commit(id="abc123", message="First commit"),
            make_commit(id="def456", message="Second commit"),
            make_commit(id="ghi789", message="Third commit"),
        ]
        widget.show(commits, {}, {})

        assert widget.commits == commits
        assert len(list_view) == 3
        await pilot.pause()


@pytest.mark.asyncio
async def test_commit_list_show_with_branches():
    """
    Test show method with commits and branch decorations.

    Checks that branches are associated with their commits.
    """
    app = CommitListTestApp()
    async with app.run_test() as pilot:
        widget = app.query_one(CommitList)
        list_view = widget.query_one(ListView)

        commit = make_commit(id="abc123", message="Commit on main")
        branch = make_branch(name="refs/heads/main", target_id="abc123")
        branches_by_commit = {"abc123": [branch]}

        widget.show([commit], branches_by_commit, {})

        assert widget.commits == [commit]
        assert widget.branches_by_commit == branches_by_commit
        assert len(list_view) == 1
        await pilot.pause()


@pytest.mark.asyncio
async def test_commit_list_show_with_tags():
    """
    Test show method with commits and tag decorations.

    Checks that tags are associated with their commits.
    """
    app = CommitListTestApp()
    async with app.run_test() as pilot:
        widget = app.query_one(CommitList)
        list_view = widget.query_one(ListView)

        commit = make_commit(id="abc123", message="Tagged commit")
        tag = make_tag(name="refs/tags/v1.0.0", target_id="abc123")
        tags_by_commit = {"abc123": [tag]}

        widget.show([commit], {}, tags_by_commit)

        assert widget.commits == [commit]
        assert widget.tags_by_commit == tags_by_commit
        assert len(list_view) == 1
        await pilot.pause()


@pytest.mark.asyncio
async def test_commit_list_show_with_multiple_branches_and_tags():
    """
    Test show method with commits having multiple branches and tags.

    Checks that multiple decorations are handled correctly.
    """
    app = CommitListTestApp()
    async with app.run_test() as pilot:
        widget = app.query_one(CommitList)
        list_view = widget.query_one(ListView)

        commit = make_commit(id="abc123", message="Release commit")
        branches = [
            make_branch(name="refs/heads/main", target_id="abc123"),
            make_branch(name="refs/heads/develop", target_id="abc123"),
        ]
        tags = [
            make_tag(name="refs/tags/v1.0.0", target_id="abc123"),
            make_tag(name="refs/tags/latest", target_id="abc123"),
        ]
        branches_by_commit = {"abc123": branches}
        tags_by_commit = {"abc123": tags}

        widget.show([commit], branches_by_commit, tags_by_commit)

        assert widget.commits == [commit]
        assert widget.branches_by_commit == branches_by_commit
        assert widget.tags_by_commit == tags_by_commit
        assert len(list_view) == 1
        await pilot.pause()


@pytest.mark.asyncio
async def test_commit_list_show_replaces_existing():
    """
    Test show method replaces existing commits.

    Checks that calling show again clears previous commits and decorations.
    """
    app = CommitListTestApp()
    async with app.run_test() as pilot:
        widget = app.query_one(CommitList)
        list_view = widget.query_one(ListView)

        # First show
        commits1 = [make_commit(id="abc123", message="First")]
        widget.show(commits1, {}, {})
        await pilot.pause()
        assert len(list_view) == 1

        # Second show with different commits
        commits2 = [
            make_commit(id="def456", message="Second"),
            make_commit(id="ghi789", message="Third"),
        ]
        widget.show(commits2, {}, {})
        await pilot.pause()

        assert widget.commits == commits2
        assert len(list_view) == 2
        await pilot.pause()


def test_commit_list_get_label():
    """
    Test _get_label method.

    Checks that label is created correctly with proper styling.
    """
    widget = CommitList()
    commit = make_commit(id="abc1234567890abcdef", message="Test commit")
    label = widget._get_label(commit)

    assert isinstance(label, Label)
    assert label.has_class("commit-item")


def test_commit_list_get_label_with_branches():
    """
    Test _get_label method with branch decorations.

    Checks that branch decorations are included in the label.
    """
    widget = CommitList()
    commit = make_commit(id="abc123", message="Commit on main")
    branch = make_branch(name="refs/heads/main", target_id="abc123")
    widget.branches_by_commit = {"abc123": [branch]}

    label = widget._get_label(commit)

    assert isinstance(label, Label)
    assert label.has_class("commit-item")


def test_commit_list_get_label_with_tags():
    """
    Test _get_label method with tag decorations.

    Checks that tag decorations are included in the label.
    """
    widget = CommitList()
    commit = make_commit(id="abc123", message="Tagged commit")
    tag = make_tag(name="refs/tags/v1.0.0", target_id="abc123")
    widget.tags_by_commit = {"abc123": [tag]}

    label = widget._get_label(commit)

    assert isinstance(label, Label)
    assert label.has_class("commit-item")


def test_commit_list_get_body_text():
    """
    Test _get_body_text static method.

    Checks that commit body text is formatted correctly.
    """
    commit = make_commit(
        message="Test commit message", author=make_signature(name="Alice")
    )
    text = CommitList._get_body_text(commit)

    assert text is not None
    # Check that text contains the message and author
    text_str = str(text)
    assert "Test commit message" in text_str
    assert "Alice" in text_str


def test_commit_list_get_body_text_root_commit():
    """
    Test _get_body_text with a root commit.

    Checks that root commits are formatted differently.
    """
    commit = make_commit(
        message="Initial commit", parent_ids=[], author=make_signature(name="Bob")
    )
    text = CommitList._get_body_text(commit)

    assert text is not None
    text_str = str(text)
    assert "Initial commit" in text_str
    assert "Bob" in text_str


def test_commit_list_get_header_text_plain():
    """
    Test _get_header_text method without decorations.

    Checks that header text contains commit short ID.
    """
    widget = CommitList()
    commit = make_commit(id="abc1234567890abcdef")
    text = widget._get_header_text(commit)

    assert text is not None
    text_str = str(text)
    # Should contain the short ID
    assert commit.short_id in text_str


def test_commit_list_get_header_text_with_branch():
    """
    Test _get_header_text method with branch decoration.

    Checks that branch shorthand is included in header text.
    """
    widget = CommitList()
    commit = make_commit(id="abc123")
    branch = make_branch(name="refs/heads/main", target_id="abc123")
    widget.branches_by_commit = {"abc123": [branch]}

    text = widget._get_header_text(commit)

    assert text is not None
    text_str = str(text)
    assert commit.short_id in text_str
    assert "main" in text_str


def test_commit_list_get_header_text_with_tag():
    """
    Test _get_header_text method with tag decoration.

    Checks that tag shorthand is included in header text.
    """
    widget = CommitList()
    commit = make_commit(id="abc123")
    tag = make_tag(name="refs/tags/v1.0.0", target_id="abc123")
    widget.tags_by_commit = {"abc123": [tag]}

    text = widget._get_header_text(commit)

    assert text is not None
    text_str = str(text)
    assert commit.short_id in text_str
    assert "v1.0.0" in text_str


def test_commit_list_get_header_text_with_multiple_decorations():
    """
    Test _get_header_text method with multiple branches and tags.

    Checks that all decorations are included in header text.
    """
    widget = CommitList()
    commit = make_commit(id="abc123")
    branches = [
        make_branch(name="refs/heads/main", target_id="abc123"),
        make_branch(name="refs/heads/develop", target_id="abc123"),
    ]
    tags = [
        make_tag(name="refs/tags/v1.0.0", target_id="abc123"),
    ]
    widget.branches_by_commit = {"abc123": branches}
    widget.tags_by_commit = {"abc123": tags}

    text = widget._get_header_text(commit)

    assert text is not None
    text_str = str(text)
    assert commit.short_id in text_str
    assert "main" in text_str
    assert "develop" in text_str
    assert "v1.0.0" in text_str


def test_commit_list_on_list_view_selected_handler():
    """
    Test on_list_view_selected event handler.

    Checks that handler extracts correct commit ID and posts message.
    """
    widget = CommitList()
    commits = [
        make_commit(id="abc123", message="First"),
        make_commit(id="def456", message="Second"),
    ]
    widget.commits = commits

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
    assert isinstance(posted_messages[0], CommitList.CommitSelected)
    assert posted_messages[0].id == "abc123"


def test_commit_list_commit_selected_message():
    """
    Test CommitSelected message initialization.

    Checks that message is created with correct commit ID.
    """
    message = CommitList.CommitSelected("abc1234567890abcdef")
    assert message.id == "abc1234567890abcdef"


@pytest.mark.parametrize(
    "index,expected_id",
    [
        (0, "abc123"),
        (1, "def456"),
        (2, "ghi789"),
    ],
)
def test_commit_list_on_list_view_selected_indices(index, expected_id):
    """
    Test on_list_view_selected with different indices.

    Checks that correct commit ID is extracted for each index.
    """
    widget = CommitList()
    widget.commits = [
        make_commit(id="abc123", message="First"),
        make_commit(id="def456", message="Second"),
        make_commit(id="ghi789", message="Third"),
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
    assert posted_messages[0].id == expected_id


@pytest.mark.parametrize(
    "commit_message,author_name",
    [
        ("Initial commit", "Alice"),
        ("Add feature X", "Bob"),
        ("Fix bug in module Y", "Charlie"),
        ("Merge branch 'develop'", "Dave"),
    ],
)
def test_commit_list_get_label_various_messages(commit_message, author_name):
    """
    Test _get_label with various commit messages and authors.

    Checks that labels are created correctly for different commits.
    """
    widget = CommitList()
    commit = make_commit(
        message=commit_message, author=make_signature(name=author_name)
    )
    label = widget._get_label(commit)

    assert isinstance(label, Label)
    assert label.has_class("commit-item")
