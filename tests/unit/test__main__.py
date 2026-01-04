# @generated "all" Claude-Sonnet-4.5
"""
Tests for the __main__ entry point.

Covers CLI argument parsing and main function behavior.
"""

import sys
from pathlib import Path

import pytest

from gittergraph import __version__
from gittergraph.__main__ import main


def test_main_with_no_arguments(monkeypatch):
    """
    Test main() with no command-line arguments.

    Checks that run() is called with None (current directory).
    """
    # Mock sys.argv
    monkeypatch.setattr(sys, "argv", ["gittergraph"])

    # Mock the run function
    run_called_with = None

    def mock_run(repo_path=None):
        nonlocal run_called_with
        run_called_with = repo_path

    monkeypatch.setattr("gittergraph.__main__.run", mock_run)

    main()

    assert run_called_with is None


def test_main_with_repo_path_argument(monkeypatch):
    """
    Test main() with repository path argument.

    Checks that run() is called with the provided path.
    """
    test_path = "/some/repo/path"
    monkeypatch.setattr(sys, "argv", ["gittergraph", test_path])

    # Mock the run function
    run_called_with = None

    def mock_run(repo_path=None):
        nonlocal run_called_with
        run_called_with = repo_path

    monkeypatch.setattr("gittergraph.__main__.run", mock_run)

    main()

    assert run_called_with == Path(test_path)


def test_main_with_relative_path(monkeypatch):
    """
    Test main() with relative repository path.

    Checks that run() receives a Path object for relative paths.
    """
    test_path = "./my-repo"
    monkeypatch.setattr(sys, "argv", ["gittergraph", test_path])

    # Mock the run function
    run_called_with = None

    def mock_run(repo_path=None):
        nonlocal run_called_with
        run_called_with = repo_path

    monkeypatch.setattr("gittergraph.__main__.run", mock_run)

    main()

    assert run_called_with == Path(test_path)


def test_main_with_version_flag(monkeypatch, capsys):
    """
    Test main() with --version flag.

    Checks that version is printed and program exits.
    """
    monkeypatch.setattr(sys, "argv", ["gittergraph", "--version"])

    with pytest.raises(SystemExit) as exc_info:
        main()

    # SystemExit code 0 indicates success
    assert exc_info.value.code == 0

    # Check that version was printed
    captured = capsys.readouterr()
    assert __version__ in captured.out


def test_main_version_format(monkeypatch, capsys):
    """
    Test that --version output has correct format.

    Checks that version string includes program name and version.
    """
    monkeypatch.setattr(sys, "argv", ["gittergraph", "--version"])

    with pytest.raises(SystemExit):
        main()

    captured = capsys.readouterr()
    assert "gittergraph" in captured.out
    assert __version__ in captured.out


def test_main_with_help_flag(monkeypatch, capsys):
    """
    Test main() with --help flag.

    Checks that help is printed and program exits.
    """
    monkeypatch.setattr(sys, "argv", ["gittergraph", "--help"])

    with pytest.raises(SystemExit) as exc_info:
        main()

    # SystemExit code 0 indicates success
    assert exc_info.value.code == 0

    # Check that help text was printed
    captured = capsys.readouterr()
    assert "Git graph visualization" in captured.out
    assert "repo_path" in captured.out


def test_main_help_shows_optional_argument(monkeypatch, capsys):
    """
    Test that --help shows repo_path as optional.

    Checks that help indicates default behavior.
    """
    monkeypatch.setattr(sys, "argv", ["gittergraph", "--help"])

    with pytest.raises(SystemExit):
        main()

    captured = capsys.readouterr()
    assert "current directory" in captured.out or "default:" in captured.out


def test_main_calls_run_function(monkeypatch):
    """
    Test that main() actually calls the run function.

    Checks that the TUI run function is invoked.
    """
    monkeypatch.setattr(sys, "argv", ["gittergraph"])

    run_called = False

    def mock_run(repo_path=None):
        nonlocal run_called
        run_called = True

    monkeypatch.setattr("gittergraph.__main__.run", mock_run)

    main()

    assert run_called


def test_main_handles_path_with_spaces(monkeypatch):
    """
    Test main() with path containing spaces.

    Checks that paths with spaces are handled correctly.
    """
    test_path = "/path/with spaces/repo"
    monkeypatch.setattr(sys, "argv", ["gittergraph", test_path])

    run_called_with = None

    def mock_run(repo_path=None):
        nonlocal run_called_with
        run_called_with = repo_path

    monkeypatch.setattr("gittergraph.__main__.run", mock_run)

    main()

    assert run_called_with == Path(test_path)


def test_main_converts_string_to_path(monkeypatch):
    """
    Test that main() converts string argument to Path object.

    Checks that argparse type conversion works correctly.
    """
    test_path = "/some/path"
    monkeypatch.setattr(sys, "argv", ["gittergraph", test_path])

    run_called_with = None

    def mock_run(repo_path=None):
        nonlocal run_called_with
        run_called_with = repo_path

    monkeypatch.setattr("gittergraph.__main__.run", mock_run)

    main()

    assert isinstance(run_called_with, Path)
    assert str(run_called_with) == test_path


def test_main_entry_point_exists():
    """
    Test that main function is importable.

    Checks that entry point is properly defined.
    """
    from gittergraph.__main__ import main

    assert callable(main)


def test_main_if_name_main_block():
    """
    Test that __main__.py can be executed as a module.

    Checks that the if __name__ == "__main__" block exists.
    """
    # Read the __main__.py file to verify it has the if __name__ block
    import inspect

    import gittergraph.__main__ as main_module

    source = inspect.getsource(main_module)
    assert 'if __name__ == "__main__"' in source
    assert "main()" in source
