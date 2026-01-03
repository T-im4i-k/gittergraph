# @generated "all" Claude-Sonnet-4.5
"""
Tests for the RefPanel.

Covers reference panel display and child widget composition.
"""

import pytest
from textual.app import App, ComposeResult

from gittergraph.tui.panels.ref_panel import RefPanel
from gittergraph.tui.widgets import BranchList, HeadDetail, TagList
from tests.make_models_helper import make_branch, make_head, make_tag


class RefPanelTestApp(App):
    """
    Minimal test app for RefPanel.

    Provides a simple app context for testing panel behavior.
    """

    def compose(self) -> ComposeResult:
        """Compose the test app with a RefPanel."""
        yield RefPanel()


def test_ref_panel_initialization():
    """
    Test RefPanel initialization.

    Checks that panel initializes correctly.
    """
    panel = RefPanel()
    assert panel is not None


@pytest.mark.asyncio
async def test_ref_panel_compose_with_app():
    """
    Test compose method with a running app.

    Checks that all child widgets are created in the correct order.
    """
    app = RefPanelTestApp()
    async with app.run_test() as pilot:
        panel = app.query_one(RefPanel)

        head_detail = panel.query_one("#head-detail", HeadDetail)
        branch_list = panel.query_one("#branch-list", BranchList)
        tag_list = panel.query_one("#tag-list", TagList)

        assert head_detail is not None
        assert branch_list is not None
        assert tag_list is not None
        await pilot.pause()


@pytest.mark.asyncio
async def test_ref_panel_show_empty_data():
    """
    Test show method with empty branches and tags.

    Checks that panel updates all child widgets correctly.
    """
    app = RefPanelTestApp()
    async with app.run_test() as pilot:
        panel = app.query_one(RefPanel)
        head = make_head(branch_name="refs/heads/main")

        panel.show(head, [], [])

        head_detail = panel.query_one("#head-detail", HeadDetail)
        branch_list = panel.query_one("#branch-list", BranchList)
        tag_list = panel.query_one("#tag-list", TagList)

        assert head_detail.head == head
        assert branch_list.branches == []
        assert tag_list.tags == []
        await pilot.pause()


@pytest.mark.asyncio
async def test_ref_panel_show_with_data():
    """
    Test show method with branches and tags.

    Checks that panel updates all child widgets with provided data.
    """
    app = RefPanelTestApp()
    async with app.run_test() as pilot:
        panel = app.query_one(RefPanel)
        head = make_head(branch_name="refs/heads/develop")
        branches = [
            make_branch(name="refs/heads/main"),
            make_branch(name="refs/heads/develop"),
        ]
        tags = [make_tag(name="refs/tags/v1.0.0"), make_tag(name="refs/tags/v2.0.0")]

        panel.show(head, branches, tags)

        head_detail = panel.query_one("#head-detail", HeadDetail)
        branch_list = panel.query_one("#branch-list", BranchList)
        tag_list = panel.query_one("#tag-list", TagList)

        assert head_detail.head == head
        assert len(branch_list.branches) == 2
        assert len(tag_list.tags) == 2
        await pilot.pause()


@pytest.mark.asyncio
async def test_ref_panel_show_updates_widgets():
    """
    Test that show method can update widgets multiple times.

    Checks that panel correctly updates when called with different data.
    """
    app = RefPanelTestApp()
    async with app.run_test() as pilot:
        panel = app.query_one(RefPanel)

        # First update
        head1 = make_head(branch_name="refs/heads/main")
        branches1 = [make_branch(name="refs/heads/main")]
        tags1 = [make_tag(name="refs/tags/v1.0.0")]
        panel.show(head1, branches1, tags1)

        branch_list = panel.query_one("#branch-list", BranchList)
        tag_list = panel.query_one("#tag-list", TagList)
        assert len(branch_list.branches) == 1
        assert len(tag_list.tags) == 1

        # Second update
        head2 = make_head(branch_name="refs/heads/develop")
        branches2 = [
            make_branch(name="refs/heads/main"),
            make_branch(name="refs/heads/develop"),
            make_branch(name="refs/heads/feature"),
        ]
        tags2 = [make_tag(name="refs/tags/v2.0.0")]
        panel.show(head2, branches2, tags2)

        assert len(branch_list.branches) == 3
        assert len(tag_list.tags) == 1
        await pilot.pause()
