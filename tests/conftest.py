# @generated "partially" Claude-Sonnet-4.5: Code
# @generated "partially" ChatGPT-4.1: Documentation
"""
Pytest fixtures for git repository setup.

Provides reusable fixtures for creating temporary git repositories with various commit and branch structures for testing purposes.
"""


import pygit2
import pytest


@pytest.fixture
def empty_repo(tmp_path):
    """
    Create an empty git repository.

    Initializes a new repository in a temporary directory and returns the repository path and pygit2.Repository object.
    """
    repo_path = tmp_path / "test_repo"
    repo = pygit2.init_repository(str(repo_path))
    return repo_path, repo


@pytest.fixture
def simple_repo(empty_repo):
    """
    Create a simple git repository with one commit.

    Initializes a new repository, creates an initial commit, and returns the path and commit id.
    """
    repo_path, repo = empty_repo

    tree = repo.TreeBuilder().write()
    author = pygit2.Signature("Alice", "alice@example.com", 1234567890, 60)
    commit_oid = repo.create_commit(
        "refs/heads/main", author, author, "Initial commit", tree, []
    )

    return repo_path, [str(commit_oid)]


@pytest.fixture
def repo_different_author_and_commiter(empty_repo):
    """
    Create a git repository with a commit having different author and committer.

    Initializes a new repository, creates an initial commit with distinct author and committer, and returns the path and commit id.
    """
    repo_path, repo = empty_repo

    tree = repo.TreeBuilder().write()
    author = pygit2.Signature("Alice", "alice@example.com", 1234567890, 60)
    commiter = pygit2.Signature("Bob", "bob@example.com", 1234567900, -60)
    commit_oid = repo.create_commit(
        "refs/heads/main", author, commiter, "Initial commit", tree, []
    )

    return repo_path, [str(commit_oid)]


@pytest.fixture
def repo_with_history(empty_repo):
    """
    Create a git repository with multiple commits.

    Initializes a repository and creates a linear history of five commits. Returns the path and commit ids.
    """
    repo_path, repo = empty_repo

    commit_ids = []
    for i in range(5):
        tree = repo.TreeBuilder().write()
        author = pygit2.Signature(
            f"Author{i}", f"author{i}@example.com", 1234567890 + i, 60
        )
        parent = [commit_ids[-1]] if commit_ids else []

        oid = repo.create_commit(
            "refs/heads/main", author, author, f"Commit {i}", tree, parent
        )
        commit_ids.append(oid)

    return repo_path, [str(oid) for oid in commit_ids]


@pytest.fixture
def repo_with_branches(empty_repo):
    """
    Create a git repository with multiple branches.

    Initializes a repository, creates commits on main and feature branches, and returns the path and commit ids.
    """
    repo_path, repo = empty_repo

    # Create main branch commits
    tree = repo.TreeBuilder().write()
    author = pygit2.Signature("Test", "test@example.com")
    c1 = repo.create_commit("refs/heads/main", author, author, "First commit", tree, [])

    c2 = repo.create_commit(
        "refs/heads/main", author, author, "Second commit", tree, [c1]
    )

    # Create feature branch
    c3 = repo.create_commit(
        "refs/heads/feature", author, author, "Feature commit", tree, [c2]
    )

    return repo_path, [str(c1), str(c2), str(c3)]


@pytest.fixture
def repo_detached_head(empty_repo):
    """
    Create a repository with detached HEAD.

    Initializes a new repository, creates a commit on main, and detaches HEAD to point directly to the commit. Returns the repository path and commit id.
    """
    repo_path, repo = empty_repo

    tree = repo.TreeBuilder().write()
    author = pygit2.Signature("Test", "test@example.com")
    id_ = repo.create_commit(
        "refs/heads/main", author, author, "First commit", tree, []
    )

    # Detach HEAD
    repo.set_head(id_)

    return repo_path, [str(id_)]
