# @generated "partially" Claude-Sonnet-4.5: Code
# @generated "partially" ChatGPT-4.1: Documentation
"""
Tests for the BaseAccess class.

Provides pytest-based tests for basic repository access functionality, including initialization and error handling.
"""

from pathlib import Path

import pygit2
import pytest

from gittergraph.data.base_access import BaseAccess


@pytest.fixture
def simple_repo(tmp_path):
    """
    Create a minimal git repository for testing.

    Initializes a new repository, creates an initial commit, and returns the path.
    """
    repo_path = tmp_path / "test_repo"
    repo = pygit2.init_repository(str(repo_path))

    # Create initial commit
    tree = repo.TreeBuilder().write()
    author = pygit2.Signature("Test User", "test@example.com")
    repo.create_commit("refs/heads/main", author, author, "Initial commit", tree, [])

    return repo_path


@pytest.mark.parametrize("path_type", ["str", "Path"])
def test_init_with_valid_repo(simple_repo, path_type):
    """
    Test BaseAccess initialization with valid repository path.

    Checks both string and Path types for repository path argument.
    """
    # Convert to requested type
    path = str(simple_repo) if path_type == "str" else simple_repo

    access = BaseAccess(path)

    assert access.path == Path(simple_repo)
    assert isinstance(access._repo, pygit2.Repository)
    assert not access._repo.is_empty


def test_init_with_nonexistent_path(tmp_path):
    """
    Test error on initialization with non-existent path.

    Verifies that initializing BaseAccess with a missing path raises GitError.
    """
    nonexistent = tmp_path / "does_not_exist"

    with pytest.raises(pygit2.GitError):
        BaseAccess(nonexistent)


def test_init_with_non_git_directory(tmp_path):
    """
    Test error on initialization with non-git directory.

    Verifies that initializing BaseAccess with a non-repo directory raises GitError.
    """
    regular_dir = tmp_path / "not_a_repo"
    regular_dir.mkdir()

    with pytest.raises(pygit2.GitError):
        BaseAccess(regular_dir)
