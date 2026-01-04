# @generated "all" Claude-Sonnet-4.5
"""
Entry point for the gittergraph CLI.

Provides the main function for launching the TUI application.
"""

import argparse
from pathlib import Path

from gittergraph import __version__
from gittergraph.tui import run


def main() -> None:
    """
    Main entry point for gittergraph CLI.

    Launches the TUI application, optionally with a specified repository path.
    """
    parser = argparse.ArgumentParser(
        prog="gittergraph",
        description="Git graph visualization in your terminal",
    )
    parser.add_argument(
        "repo_path",
        nargs="?",
        type=Path,
        default=None,
        help="Path to git repository (default: current directory)",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )

    args = parser.parse_args()
    run(args.repo_path)


if __name__ == "__main__":
    main()
