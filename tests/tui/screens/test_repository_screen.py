# @generated "all" Claude-Sonnet-4.5
"""
Tests for the RepositoryScreen.

Covers screen composition, display, event handling, and keyboard shortcuts.
"""

import pytest
from textual.app import App, ComposeResult
from textual.widgets import ListView

from gittergraph.core import GitGraph
from gittergraph.tui.panels import HistoryPanel, RefPanel
from gittergraph.tui.screens import RepositoryScreen
from gittergraph.tui.widgets import (
    BranchList,
    CommitDetail,
    CommitHistory,
    HeadDetail,
    TagList,
)


class RepositoryScreenTestApp(App):
    """
    Minimal test app for RepositoryScreen.

    Provides a simple app context for testing screen behavior.
    """

    def compose(self) -> ComposeResult:
        """Compose the test app with a RepositoryScreen."""
        yield RepositoryScreen()


def test_repository_screen_initialization():
    """
    Test RepositoryScreen initialization.

    Checks that screen initializes with None graph.
    """
    screen = RepositoryScreen()
    assert screen.graph is None


@pytest.mark.asyncio
async def test_repository_screen_compose():
    """
    Test compose method creates both panels.

    Checks that HistoryPanel and RefPanel are created in the correct order.
    """
    app = RepositoryScreenTestApp()
    async with app.run_test() as pilot:
        screen = app.query_one(RepositoryScreen)

        history_panel = screen.query_one("#history-panel", HistoryPanel)
        ref_panel = screen.query_one("#ref-panel", RefPanel)

        assert history_panel is not None
        assert ref_panel is not None
        await pilot.pause()


@pytest.mark.asyncio
async def test_repository_screen_compose_creates_all_widgets():
    """
    Test compose method creates all child widgets.

    Checks that all expected widgets are present in the screen.
    """
    app = RepositoryScreenTestApp()
    async with app.run_test() as pilot:
        screen = app.query_one(RepositoryScreen)

        # History panel widgets
        commit_history = screen.query_one("#commit-history", CommitHistory)
        commit_detail = screen.query_one("#commit-detail", CommitDetail)

        # Ref panel widgets
        head_detail = screen.query_one("#head-detail", HeadDetail)
        branch_list = screen.query_one("#branch-list", BranchList)
        tag_list = screen.query_one("#tag-list", TagList)

        assert commit_history is not None
        assert commit_detail is not None
        assert head_detail is not None
        assert branch_list is not None
        assert tag_list is not None
        await pilot.pause()


@pytest.mark.asyncio
async def test_repository_screen_show_with_simple_repo(simple_repo):
    """
    Test show method with a simple repository.

    Checks that screen displays repository data correctly.
    """
    repo_path, _ = simple_repo
    app = RepositoryScreenTestApp()
    async with app.run_test() as pilot:
        screen = app.query_one(RepositoryScreen)
        graph = GitGraph.from_path(repo_path)

        screen.show(graph)

        assert screen.graph is not None
        assert screen.graph == graph
        await pilot.pause()


@pytest.mark.asyncio
async def test_repository_screen_show_updates_history_panel(repo_with_history):
    """
    Test show method updates history panel with commits.

    Checks that commits are displayed in the history panel.
    """
    repo_path, _ = repo_with_history
    app = RepositoryScreenTestApp()
    async with app.run_test() as pilot:
        screen = app.query_one(RepositoryScreen)
        graph = GitGraph.from_path(repo_path)

        screen.show(graph)
        screen._update_history_panel("refs/heads/main")
        await pilot.pause()

        commit_history = screen.query_one("#commit-history", CommitHistory)
        assert len(commit_history.commits) > 0
        await pilot.pause()


@pytest.mark.asyncio
async def test_repository_screen_show_updates_ref_panel(repo_with_branches):
    """
    Test show method updates ref panel with references.

    Checks that HEAD, branches, and tags are displayed.
    """
    repo_path, _ = repo_with_branches
    app = RepositoryScreenTestApp()
    async with app.run_test() as pilot:
        screen = app.query_one(RepositoryScreen)
        graph = GitGraph.from_path(repo_path)

        screen.show(graph)

        head_detail = screen.query_one("#head-detail", HeadDetail)
        branch_list = screen.query_one("#branch-list", BranchList)

        assert head_detail.head is not None
        assert len(branch_list.branches) > 0
        await pilot.pause()


@pytest.mark.asyncio
async def test_repository_screen_action_focus_history(simple_repo):
    """
    Test action_focus_history keyboard shortcut.

    Checks that 'c' key focuses the commit history widget.
    """
    repo_path, _ = simple_repo
    app = RepositoryScreenTestApp()
    async with app.run_test() as pilot:
        screen = app.query_one(RepositoryScreen)
        graph = GitGraph.from_path(repo_path)
        screen.show(graph)

        await pilot.press("c")

        commit_history = screen.query_one("#commit-history", CommitHistory)
        list_view = commit_history.query_one(ListView)
        assert list_view.has_focus
        await pilot.pause()


@pytest.mark.asyncio
async def test_repository_screen_action_focus_detail(simple_repo):
    """
    Test action_focus_detail keyboard shortcut.

    Checks that 'd' key focuses the commit detail widget.
    """
    repo_path, _ = simple_repo
    app = RepositoryScreenTestApp()
    async with app.run_test() as pilot:
        screen = app.query_one(RepositoryScreen)
        graph = GitGraph.from_path(repo_path)
        screen.show(graph)

        await pilot.press("d")

        commit_detail = screen.query_one("#commit-detail", CommitDetail)
        assert commit_detail.has_focus
        await pilot.pause()


@pytest.mark.asyncio
async def test_repository_screen_action_focus_head(simple_repo):
    """
    Test action_focus_head keyboard shortcut.

    Checks that the focus action can be called on HEAD detail widget.
    """
    repo_path, _ = simple_repo
    app = RepositoryScreenTestApp()
    async with app.run_test() as pilot:
        screen = app.query_one(RepositoryScreen)
        graph = GitGraph.from_path(repo_path)
        screen.show(graph)
        await pilot.pause()

        # Call action - HeadDetail focus behavior to be fully tested when implemented
        screen.action_focus_head()
        await pilot.pause()

        head_detail = screen.query_one("#head-detail", HeadDetail)
        assert head_detail is not None
        await pilot.pause()


@pytest.mark.asyncio
async def test_repository_screen_action_focus_branches(repo_with_branches):
    """
    Test action_focus_branches keyboard shortcut.

    Checks that 'b' key focuses the branch list widget.
    """
    repo_path, _ = repo_with_branches
    app = RepositoryScreenTestApp()
    async with app.run_test() as pilot:
        screen = app.query_one(RepositoryScreen)
        graph = GitGraph.from_path(repo_path)
        screen.show(graph)

        await pilot.press("b")

        branch_list = screen.query_one("#branch-list", BranchList)
        list_view = branch_list.query_one(ListView)
        assert list_view.has_focus
        await pilot.pause()


@pytest.mark.asyncio
async def test_repository_screen_action_focus_tags(simple_repo):
    """
    Test action_focus_tags keyboard shortcut.

    Checks that 't' key focuses the tag list widget.
    """
    repo_path, _ = simple_repo
    app = RepositoryScreenTestApp()
    async with app.run_test() as pilot:
        screen = app.query_one(RepositoryScreen)
        graph = GitGraph.from_path(repo_path)
        screen.show(graph)

        await pilot.press("t")

        tag_list = screen.query_one("#tag-list", TagList)
        list_view = tag_list.query_one(ListView)
        assert list_view.has_focus
        await pilot.pause()


@pytest.mark.asyncio
async def test_repository_screen_commit_selection_updates_detail(repo_with_history):
    """
    Test that selecting a commit updates the detail view.

    Checks that commit selection event triggers detail update.
    """
    repo_path, _ = repo_with_history

    app = RepositoryScreenTestApp()
    async with app.run_test() as pilot:
        screen = app.query_one(RepositoryScreen)
        graph = GitGraph.from_path(repo_path)
        screen.show(graph)
        await pilot.pause()

        # Verify graph and commits are loaded
        assert screen.graph is not None
        assert len(screen.graph.data.commits) > 1

        # Explicitly update with main branch since HEAD is unborn in fixture
        screen._update_history_panel("refs/heads/main")
        await pilot.pause()

        commit_history = screen.query_one("#commit-history", CommitHistory)
        commit_detail = screen.query_one("#commit-detail", CommitDetail)

        # Verify we have commits
        assert len(commit_history.commits) > 1

        # Simulate selecting the second commit
        second_commit = commit_history.commits[1]
        screen.on_commit_history_commit_selected(
            CommitHistory.CommitSelected(second_commit.id)
        )
        await pilot.pause()

        # Verify detail updated to show second commit
        assert commit_detail.commit is not None
        assert commit_detail.commit.id == second_commit.id
        await pilot.pause()


def test_repository_screen_bindings_defined():
    """
    Test that keyboard bindings are properly defined.

    Checks that all expected bindings are present.
    """
    screen = RepositoryScreen()
    binding_keys = [binding[0] for binding in screen.BINDINGS]

    assert "c" in binding_keys  # Focus history
    assert "d" in binding_keys  # Focus detail
    assert "h" in binding_keys  # Focus HEAD
    assert "b" in binding_keys  # Focus branches
    assert "t" in binding_keys  # Focus tags
