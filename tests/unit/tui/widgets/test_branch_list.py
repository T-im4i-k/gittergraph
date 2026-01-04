# @generated "all" Claude-Sonnet-4.5
"""
Tests for the BranchList widget.

Covers branch list display, selection, and event handling.
"""

import pytest
from textual.app import App, ComposeResult
from textual.widgets import Label, ListView

from gittergraph.tui.widgets.branch_list import BranchList
from tests.make_models_helper import make_branch


class BranchListTestApp(App):
    """
    Minimal test app for BranchList widget.

    Provides a simple app context for testing widget behavior.
    """

    def compose(self) -> ComposeResult:
        """Compose the test app with a BranchList widget."""
        yield BranchList()


def test_branch_list_initialization():
    """
    Test BranchList widget initialization.

    Checks that widget initializes with empty branch list.
    """
    widget = BranchList()
    assert widget.branches == []
    assert widget.border_title == "Branches"


@pytest.mark.asyncio
async def test_branch_list_compose_with_app():
    """
    Test compose method with a running app.

    Checks that ListView widget is created and initialized.
    """
    app = BranchListTestApp()
    async with app.run_test() as pilot:
        widget = app.query_one(BranchList)
        list_view = widget.query_one(ListView)

        assert list_view is not None
        await pilot.pause()


@pytest.mark.asyncio
async def test_branch_list_show_empty_list():
    """
    Test show method with an empty branch list.

    Checks that ListView is cleared and remains empty.
    """
    app = BranchListTestApp()
    async with app.run_test() as pilot:
        widget = app.query_one(BranchList)
        list_view = widget.query_one(ListView)

        widget.show([])

        assert widget.branches == []
        assert len(list_view) == 0
        await pilot.pause()


@pytest.mark.asyncio
async def test_branch_list_show_single_branch():
    """
    Test show method with a single branch.

    Checks that branch is displayed correctly in the ListView.
    """
    app = BranchListTestApp()
    async with app.run_test() as pilot:
        widget = app.query_one(BranchList)
        list_view = widget.query_one(ListView)

        branch = make_branch(name="refs/heads/main")
        widget.show([branch])

        assert widget.branches == [branch]
        assert len(list_view) == 1
        await pilot.pause()


@pytest.mark.asyncio
async def test_branch_list_show_multiple_branches():
    """
    Test show method with multiple branches.

    Checks that all branches are displayed in the ListView.
    """
    app = BranchListTestApp()
    async with app.run_test() as pilot:
        widget = app.query_one(BranchList)
        list_view = widget.query_one(ListView)

        branches = [
            make_branch(name="refs/heads/main", target_id="abc123"),
            make_branch(name="refs/heads/develop", target_id="def456"),
            make_branch(name="refs/heads/feature", target_id="ghi789"),
        ]
        widget.show(branches)

        assert widget.branches == branches
        assert len(list_view) == 3
        await pilot.pause()


@pytest.mark.asyncio
async def test_branch_list_show_replaces_existing():
    """
    Test show method replaces existing branches.

    Checks that calling show again clears previous branches.
    """
    app = BranchListTestApp()
    async with app.run_test() as pilot:
        widget = app.query_one(BranchList)
        list_view = widget.query_one(ListView)

        # First show
        branches1 = [make_branch(name="refs/heads/main")]
        widget.show(branches1)
        await pilot.pause()
        assert len(list_view) == 1

        # Second show with different branches
        branches2 = [
            make_branch(name="refs/heads/develop"),
            make_branch(name="refs/heads/feature"),
        ]
        widget.show(branches2)
        await pilot.pause()

        assert widget.branches == branches2
        assert len(list_view) == 2
        await pilot.pause()


def test_branch_list_get_label():
    """
    Test _get_label static method.

    Checks that label is created correctly with proper styling.
    """
    branch = make_branch(name="refs/heads/main")
    label = BranchList._get_label(branch)

    assert isinstance(label, Label)
    assert label.has_class("branch-item")


@pytest.mark.parametrize(
    "branch_name,expected_shorthand",
    [
        ("refs/heads/main", "main"),
        ("refs/heads/develop", "develop"),
        ("refs/heads/feature/new-feature", "feature/new-feature"),
        ("refs/remotes/origin/main", "origin/main"),
    ],
)
def test_branch_list_get_label_various_names(branch_name, expected_shorthand):
    """
    Test _get_label with various branch names.

    Checks that labels are created correctly for different branch types.
    """
    branch = make_branch(name=branch_name)
    label = BranchList._get_label(branch)

    assert isinstance(label, Label)
    assert label.has_class("branch-item")


def test_branch_list_on_list_view_selected_handler():
    """
    Test on_list_view_selected event handler.

    Checks that handler extracts correct branch name and posts message.
    """
    widget = BranchList()
    branches = [
        make_branch(name="refs/heads/main"),
        make_branch(name="refs/heads/develop"),
    ]
    widget.branches = branches

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
    assert isinstance(posted_messages[0], BranchList.BranchSelected)
    assert posted_messages[0].name == "refs/heads/main"


def test_branch_list_branch_selected_message():
    """
    Test BranchSelected message initialization.

    Checks that message is created with correct branch name.
    """
    message = BranchList.BranchSelected("refs/heads/main")
    assert message.name == "refs/heads/main"


@pytest.mark.parametrize(
    "index,expected_name",
    [
        (0, "refs/heads/main"),
        (1, "refs/heads/develop"),
        (2, "refs/heads/feature"),
    ],
)
def test_branch_list_on_list_view_selected_indices(index, expected_name):
    """
    Test on_list_view_selected with different indices.

    Checks that correct branch name is extracted for each index.
    """
    widget = BranchList()
    widget.branches = [
        make_branch(name="refs/heads/main"),
        make_branch(name="refs/heads/develop"),
        make_branch(name="refs/heads/feature"),
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
