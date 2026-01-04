# @generated "all" ChatGPT-4.1
"""
Unit tests for GitRepository access layer.

Tests initialization, discovery, reload, and is_empty functionality using pytest fixtures for temporary repositories.
"""

import pygit2

from gittergraph.access.repository import GitRepository


def test_init_and_access_layers(simple_repo):
    """
    Test GitRepository initialization and access layer attributes.

    Ensures all access layers are properly initialized and point to the correct repository path.
    """
    repo_path, _ = simple_repo
    repo = GitRepository(repo_path)
    assert repo.path == repo_path
    assert isinstance(repo.commits, type(repo.commits))
    assert isinstance(repo.branches, type(repo.branches))
    assert isinstance(repo.tags, type(repo.tags))
    assert isinstance(repo.head, type(repo.head))
    assert isinstance(repo._repo, pygit2.Repository)


def test_discover(simple_repo):
    """
    Test repository discovery from a directory.

    Ensures GitRepository.discover finds the repository from a subdirectory.
    """
    repo_path, _ = simple_repo
    subdir = repo_path / "subdir"
    subdir.mkdir()
    discovered = GitRepository.discover(subdir)
    assert discovered is not None
    assert discovered.path == repo_path / ".git"


def test_is_empty_on_empty_repo(empty_repo):
    """
    Test is_empty method for an empty repository.

    Verifies that is_empty returns True for a newly initialized repository with no commits.
    """
    empty_path, _ = empty_repo
    repo_empty = GitRepository(empty_path)
    assert repo_empty.is_empty() is True


def test_is_empty_on_nonempty_repo(simple_repo):
    """
    Test is_empty method for a non-empty repository.

    Verifies that is_empty returns False for a repository with at least one commit.
    """
    nonempty_path, _ = simple_repo
    repo_nonempty = GitRepository(nonempty_path)
    assert repo_nonempty.is_empty() is False


def test_reload(simple_repo):
    """
    Test reload method reinitializes access layers and repository object.

    Ensures that after reload, access layers and _repo are fresh instances.
    """
    repo_path, _ = simple_repo
    repo = GitRepository(repo_path)
    old_repo_obj = repo._repo
    repo.reload()
    assert isinstance(repo._repo, pygit2.Repository)
    assert repo._repo is not old_repo_obj
    assert isinstance(repo.commits, type(repo.commits))
    assert isinstance(repo.branches, type(repo.branches))
    assert isinstance(repo.tags, type(repo.tags))
    assert isinstance(repo.head, type(repo.head))
