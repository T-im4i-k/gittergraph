# @generated "all" Claude-Sonnet-4.5
"""
Tests for the HistoryPanel.

Covers history panel display and child widget composition.
"""

import pytest
from textual.app import App, ComposeResult

from gittergraph.tui.panels.history_panel import HistoryPanel
from gittergraph.tui.widgets import CommitDetail, CommitHistory
from tests.make_models_helper import make_branch, make_commit, make_tag


class HistoryPanelTestApp(App):
    """
    Minimal test app for HistoryPanel.

    Provides a simple app context for testing panel behavior.
    """

    def compose(self) -> ComposeResult:
        """Compose the test app with a HistoryPanel."""
        yield HistoryPanel()


def test_history_panel_initialization():
    """
    Test HistoryPanel initialization.

    Checks that panel initializes correctly.
    """
    panel = HistoryPanel()
    assert panel is not None


@pytest.mark.asyncio
async def test_history_panel_compose_with_app():
    """
    Test compose method with a running app.

    Checks that all child widgets are created in the correct order.
    """
    app = HistoryPanelTestApp()
    async with app.run_test() as pilot:
        panel = app.query_one(HistoryPanel)

        commit_history = panel.query_one("#commit-history", CommitHistory)
        commit_detail = panel.query_one("#commit-detail", CommitDetail)

        assert commit_history is not None
        assert commit_detail is not None
        await pilot.pause()


@pytest.mark.asyncio
async def test_history_panel_show_empty_commits():
    """
    Test show method with empty commit list.

    Checks that panel clears commit detail when no commits are available.
    """
    app = HistoryPanelTestApp()
    async with app.run_test() as pilot:
        panel = app.query_one(HistoryPanel)

        panel.show([], {}, {})

        commit_history = panel.query_one("#commit-history", CommitHistory)
        commit_detail = panel.query_one("#commit-detail", CommitDetail)

        assert commit_history.commits == []
        assert commit_detail.commit is None
        await pilot.pause()


@pytest.mark.asyncio
async def test_history_panel_show_single_commit():
    """
    Test show method with a single commit.

    Checks that panel displays commit in history and shows its details.
    """
    app = HistoryPanelTestApp()
    async with app.run_test() as pilot:
        panel = app.query_one(HistoryPanel)

        commit = make_commit(id="abc1234567890abcdef", message="Initial commit")
        panel.show([commit], {}, {})

        commit_history = panel.query_one("#commit-history", CommitHistory)
        commit_detail = panel.query_one("#commit-detail", CommitDetail)

        assert len(commit_history.commits) == 1
        assert commit_detail.commit == commit
        await pilot.pause()


@pytest.mark.asyncio
async def test_history_panel_show_with_decorations():
    """
    Test show method with commits, branches, and tags.

    Checks that panel passes decorations to commit history widget.
    """
    app = HistoryPanelTestApp()
    async with app.run_test() as pilot:
        panel = app.query_one(HistoryPanel)

        commit1 = make_commit(id="abc1234567890abcdef", message="First commit")
        commit2 = make_commit(id="def4567890abcdef123", message="Second commit")
        commits = [commit1, commit2]

        branch = make_branch(name="refs/heads/main", target_id=commit1.id)
        tag = make_tag(name="refs/tags/v1.0.0", target_id=commit1.id)

        branches_by_commit = {commit1.id: [branch]}
        tags_by_commit = {commit1.id: [tag]}

        panel.show(commits, branches_by_commit, tags_by_commit)

        commit_history = panel.query_one("#commit-history", CommitHistory)
        commit_detail = panel.query_one("#commit-detail", CommitDetail)

        assert len(commit_history.commits) == 2
        assert commit_history.branches_by_commit == branches_by_commit
        assert commit_history.tags_by_commit == tags_by_commit
        assert commit_detail.commit == commit1  # First commit shown in detail
        await pilot.pause()


@pytest.mark.asyncio
async def test_history_panel_show_updates_widgets():
    """
    Test that show method can update widgets multiple times.

    Checks that panel correctly updates when called with different data.
    """
    app = HistoryPanelTestApp()
    async with app.run_test() as pilot:
        panel = app.query_one(HistoryPanel)

        # First update
        commit1 = make_commit(id="abc1234567890abcdef", message="First commit")
        panel.show([commit1], {}, {})

        commit_history = panel.query_one("#commit-history", CommitHistory)
        commit_detail = panel.query_one("#commit-detail", CommitDetail)
        assert len(commit_history.commits) == 1
        assert commit_detail.commit == commit1

        # Second update with more commits
        commit2 = make_commit(id="def4567890abcdef123", message="Second commit")
        commit3 = make_commit(id="ghi7890abcdef123456", message="Third commit")
        panel.show([commit2, commit3], {}, {})

        assert len(commit_history.commits) == 2
        assert commit_detail.commit == commit2  # First of new list
        await pilot.pause()


@pytest.mark.asyncio
async def test_history_panel_clears_detail_on_empty():
    """
    Test that detail view is cleared when transitioning to empty commit list.

    Checks that panel properly clears commit detail after showing commits.
    """
    app = HistoryPanelTestApp()
    async with app.run_test() as pilot:
        panel = app.query_one(HistoryPanel)

        # Show commits first
        commit = make_commit(id="abc1234567890abcdef", message="Initial commit")
        panel.show([commit], {}, {})

        commit_detail = panel.query_one("#commit-detail", CommitDetail)
        assert commit_detail.commit == commit

        # Clear by showing empty list
        panel.show([], {}, {})
        assert commit_detail.commit is None
        await pilot.pause()
