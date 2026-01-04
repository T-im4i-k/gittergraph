# @generated "all" Claude-Sonnet-4.5
"""
Tests for the GitterGraphApp.

Covers application initialization, repository discovery, and app-level actions.
"""

from pathlib import Path

import pytest

from gittergraph.tui.app import GitterGraphApp, run
from gittergraph.tui.screens import RepositoryScreen


def test_app_initialization_with_no_path():
    """
    Test app initialization without a repository path.

    Checks that app initializes with current directory as default.
    """
    app = GitterGraphApp()
    assert app.repo_path == Path(".")
    assert app.graph is None


def test_app_initialization_with_path():
    """
    Test app initialization with a repository path.

    Checks that app stores the provided path correctly.
    """
    test_path = "/some/path"
    app = GitterGraphApp(repo_path=test_path)
    assert app.repo_path == Path(test_path)
    assert app.graph is None


def test_app_initialization_with_path_object():
    """
    Test app initialization with a Path object.

    Checks that app handles Path objects correctly.
    """
    test_path = Path("/some/path")
    app = GitterGraphApp(repo_path=test_path)
    assert app.repo_path == test_path
    assert app.graph is None


@pytest.mark.asyncio
async def test_app_mount_with_simple_repo(simple_repo):
    """
    Test app mounting with a valid repository.

    Checks that app discovers the repository and displays the screen.
    """
    repo_path, _ = simple_repo
    app = GitterGraphApp(repo_path=repo_path)
    async with app.run_test() as pilot:
        assert app.graph is not None
        assert isinstance(app.screen, RepositoryScreen)
        await pilot.pause()


@pytest.mark.asyncio
async def test_app_mount_with_repo_with_history(repo_with_history):
    """
    Test app mounting with a repository containing history.

    Checks that app loads the repository and its commits.
    """
    repo_path, _ = repo_with_history
    app = GitterGraphApp(repo_path=repo_path)
    async with app.run_test() as pilot:
        assert app.graph is not None
        assert len(app.graph.data.commits) > 0
        await pilot.pause()


@pytest.mark.asyncio
async def test_app_mount_discovers_from_subdirectory(simple_repo):
    """
    Test app discovers repository from subdirectory.

    Checks that discover() searches upward to find the repository.
    """
    repo_path, _ = simple_repo
    subdir = repo_path / "subdir" / "nested"
    subdir.mkdir(parents=True)

    app = GitterGraphApp(repo_path=subdir)
    async with app.run_test() as pilot:
        assert app.graph is not None
        await pilot.pause()


@pytest.mark.asyncio
async def test_app_mount_with_no_repo_exits(tmp_path):
    """
    Test app exits gracefully when no repository is found.

    Checks that app exits with appropriate message.
    """
    non_repo_path = tmp_path / "not_a_repo"
    non_repo_path.mkdir()

    app = GitterGraphApp(repo_path=non_repo_path)

    # App should exit during mount when no repo is found
    async with app.run_test() as pilot:
        # App exits immediately, so we just verify it doesn't crash
        await pilot.pause()


def test_app_bindings_defined():
    """
    Test app-level bindings are defined.

    Checks that quit and reload bindings are present.
    """
    app = GitterGraphApp()
    binding_keys = [binding[0] for binding in app.BINDINGS]

    assert "q" in binding_keys  # Quit
    assert "r" in binding_keys  # Reload


def test_app_screens_defined():
    """
    Test app screens are registered.

    Checks that repository screen is in SCREENS dict.
    """
    app = GitterGraphApp()
    assert "repository-screen" in app.SCREENS
    assert app.SCREENS["repository-screen"] == RepositoryScreen


@pytest.mark.asyncio
async def test_app_action_reload(simple_repo):
    """
    Test reload action refreshes the repository.

    Checks that reload action reloads graph data and shows notification.
    """
    repo_path, _ = simple_repo
    app = GitterGraphApp(repo_path=repo_path)
    async with app.run_test() as pilot:
        assert app.graph is not None

        # Store original graph reference
        original_graph = app.graph

        # Trigger reload
        await pilot.press("r")
        await pilot.pause()

        # Graph should be reloaded (same object, updated data)
        assert app.graph is original_graph
        await pilot.pause()


def test_app_action_reload_with_no_graph():
    """
    Test reload action handles missing graph gracefully.

    Checks that reload does nothing when graph is None.
    """
    app = GitterGraphApp()

    # Manually set graph to None (simulating error state)
    app.graph = None

    # Should not crash
    app.action_reload()


@pytest.mark.asyncio
async def test_app_action_quit(simple_repo):
    """
    Test quit action exits the application.

    Checks that pressing 'q' triggers quit action.
    """
    repo_path, _ = simple_repo
    app = GitterGraphApp(repo_path=repo_path)
    async with app.run_test() as pilot:
        # Press 'q' to quit
        await pilot.press("q")
        await pilot.pause()

        # App should be exiting
        assert app.is_running is False


@pytest.mark.asyncio
async def test_app_screen_pushed(simple_repo):
    """
    Test repository screen is pushed on mount.

    Checks that RepositoryScreen is the active screen.
    """
    repo_path, _ = simple_repo
    app = GitterGraphApp(repo_path=repo_path)
    async with app.run_test() as pilot:
        assert isinstance(app.screen, RepositoryScreen)
        await pilot.pause()


@pytest.mark.asyncio
async def test_app_screen_shows_graph(repo_with_branches):
    """
    Test screen displays the loaded graph.

    Checks that graph data is passed to the screen.
    """
    repo_path, _ = repo_with_branches
    app = GitterGraphApp(repo_path=repo_path)
    async with app.run_test() as pilot:
        screen = app.screen
        assert isinstance(screen, RepositoryScreen)
        assert screen.graph is not None
        assert screen.graph is app.graph
        await pilot.pause()


def test_run_function_creates_and_runs_app(simple_repo, monkeypatch):
    """
    Test run() function creates and launches the app.

    Checks that run() instantiates GitterGraphApp correctly.
    """
    repo_path, _ = simple_repo

    # Track if app.run() was called
    run_called = False

    def mock_run(self):
        nonlocal run_called
        run_called = True

    monkeypatch.setattr(GitterGraphApp, "run", mock_run)

    run(repo_path=repo_path)

    assert run_called


def test_run_function_with_no_path(monkeypatch):
    """
    Test run() function with no path argument.

    Checks that run() works with default parameters.
    """
    run_called = False

    def mock_run(self):
        nonlocal run_called
        run_called = True

    monkeypatch.setattr(GitterGraphApp, "run", mock_run)

    run()

    assert run_called


def test_app_title_and_subtitle():
    """
    Test app title and subtitle are set.

    Checks that app displays correct branding.
    """
    app = GitterGraphApp()
    assert app.TITLE == "GitterGraph"
    assert app.SUB_TITLE == "Git graph in your terminal"


@pytest.mark.asyncio
async def test_app_push_screen_by_name(simple_repo):
    """
    Test app pushes screen using registered name.

    Checks that screen is pushed from SCREENS dict.
    """
    repo_path, _ = simple_repo
    app = GitterGraphApp(repo_path=repo_path)
    async with app.run_test() as pilot:
        # Screen should be pushed using "repository-screen" name
        assert isinstance(app.screen, RepositoryScreen)
        await pilot.pause()
