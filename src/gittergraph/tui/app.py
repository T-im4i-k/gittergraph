# @generated "all" Claude-Sonnet-4.5
"""
TUI application entry point for gittergraph.

Defines the main application class and run function for launching the Textual UI.
"""

from pathlib import Path
from typing import cast

from textual.app import App

from gittergraph.core import GitGraph
from gittergraph.tui.screens import RepositoryScreen


class GitterGraphApp(App):
    """
    Main Textual application for gittergraph.

    Provides an interactive terminal UI for visualizing git repositories.
    """

    TITLE = "GitterGraph"
    SUB_TITLE = "Git graph in your terminal"

    BINDINGS = [
        ("q", "quit", "Quit"),
        ("r", "reload", "Reload"),
    ]

    SCREENS = {"repository-screen": RepositoryScreen}

    def __init__(self, repo_path: str | Path | None = None, **kwargs) -> None:
        """
        Initialize the TUI application.

        Accepts path to the git repository, or None to auto-discover.
        """
        super().__init__(**kwargs)
        self.repo_path: Path = Path(repo_path or ".")
        self.graph: GitGraph | None = None

    async def on_mount(self) -> None:
        """
        Load the git repository and show the main screen.

        Discovers the repository starting from the provided path or current directory. Exits if no repository is found.
        """
        self.graph = GitGraph.discover(self.repo_path)

        if not self.graph:
            self.exit(message="No git repository found!")
            return

        # Wait for the screen to be ready before proceeding
        await self.push_screen("repository-screen")

        repository_screen: RepositoryScreen = cast(
            RepositoryScreen, self.get_screen("repository-screen")
        )
        repository_screen.show(self.graph)

    def action_reload(self) -> None:
        """
        Reload the git repository and refresh the screen.

        Reloads the graph data and updates the current screen with fresh data.
        """
        if not self.graph:
            return

        self.graph.reload()
        repository_screen: RepositoryScreen = cast(
            RepositoryScreen, self.get_screen("repository-screen")
        )
        repository_screen.show(self.graph)

        self.notify("Graph reloaded", timeout=2)


def run(repo_path: str | Path | None = None) -> None:
    """
    Launch the gittergraph TUI application.

    Accepts path to the git repository, or None to auto-discover.
    """
    app: GitterGraphApp = GitterGraphApp(repo_path=repo_path)
    app.run()
