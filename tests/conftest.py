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
    commit_id = repo.create_commit(
        "refs/heads/main", author, author, "Initial commit", tree, []
    )

    return repo_path, [str(commit_id)]


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
    commit_id = repo.create_commit(
        "refs/heads/main", author, commiter, "Initial commit", tree, []
    )

    return repo_path, [str(commit_id)]


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

        id_ = repo.create_commit(
            "refs/heads/main", author, author, f"Commit {i}", tree, parent
        )
        commit_ids.append(id_)

    return repo_path, [str(id_) for id_ in commit_ids]


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


@pytest.fixture
def repo_with_remote_tracking(tmp_path):
    """
    Fixture for a repository with a local branch and its remote-tracking branch.

    Creates a commit on main and adds a remote-tracking branch (origin/main) pointing to the same commit. Returns the repository path and commit id.
    """
    repo_path = tmp_path / "test_repo"
    repo = pygit2.init_repository(str(repo_path))

    tree = repo.TreeBuilder().write()
    author = pygit2.Signature("Test", "test@example.com")
    id_ = repo.create_commit("refs/heads/main", author, author, "Commit", tree, [])
    repo.create_reference("refs/remotes/origin/main", id_)

    return repo_path, [str(id_)]


@pytest.fixture
def repo_with_remote_branches(tmp_path):
    """
    Fixture for a repository with both local and remote branches.

    Creates commits on local branches (main, develop) and sets up corresponding remote branches (origin/main, origin/develop, upstream/main). Returns the repository path and commit ids.
    """
    repo_path = tmp_path / "test_repo"
    repo = pygit2.init_repository(str(repo_path))

    tree = repo.TreeBuilder().write()
    author = pygit2.Signature("Test", "test@example.com")

    # Create local branches
    c1 = repo.create_commit("refs/heads/main", author, author, "Commit 1", tree, [])
    c2 = repo.create_commit(
        "refs/heads/develop", author, author, "Commit 2", tree, [c1]
    )

    # Create remote branches
    repo.create_reference("refs/remotes/origin/main", c1)
    repo.create_reference("refs/remotes/origin/develop", c2)
    repo.create_reference("refs/remotes/upstream/main", c1)

    return repo_path, [str(c1), str(c2)]


@pytest.fixture
def repo_with_lightweight_tag(empty_repo):
    """Create a repository with a lightweight tag."""
    repo_path, repo = empty_repo

    tree = repo.TreeBuilder().write()
    author = pygit2.Signature("Test", "test@example.com")
    id_ = repo.create_commit("refs/heads/main", author, author, "Commit", tree, [])

    # Create lightweight tag
    repo.create_reference("refs/tags/v1.0.0", id_)

    return repo_path, [str(id_)]


@pytest.fixture
def repo_with_annotated_tag(empty_repo):
    """Create a repository with an annotated tag."""
    repo_path, repo = empty_repo

    tree = repo.TreeBuilder().write()
    author = pygit2.Signature("Test", "test@example.com")
    oid = repo.create_commit("refs/heads/main", author, author, "Commit", tree, [])

    # Create annotated tag
    repo.create_tag("v2.0.0", oid, pygit2.GIT_OBJECT_COMMIT, author, "Release 2.0.0")

    return repo_path, [str(oid)]


@pytest.fixture
def repo_with_multiple_tags(empty_repo):
    """Create a repository with multiple tags on different commits."""
    repo_path, repo = empty_repo

    tree = repo.TreeBuilder().write()
    author = pygit2.Signature("Test", "test@example.com")

    # Create commits
    c1 = repo.create_commit("refs/heads/main", author, author, "Commit 1", tree, [])
    c2 = repo.create_commit("refs/heads/main", author, author, "Commit 2", tree, [c1])

    # Create tags
    repo.create_reference("refs/tags/v1.0.0", c1)
    repo.create_tag("v2.0.0", c2, pygit2.GIT_OBJECT_COMMIT, author, "Release 2.0")
    repo.create_reference("refs/tags/latest", c2)

    return repo_path, [str(c1), str(c2)]


@pytest.fixture
def repo_with_merge(empty_repo):
    """
    Create a repository with a merge commit.

    Creates a base commit, then two branches (main and feature) that diverge and merge back together.
    """

    repo_path, repo = empty_repo
    tree = repo.TreeBuilder().write()
    author = pygit2.Signature("Test", "test@example.com")

    # Create base commit
    base = repo.create_commit(
        "refs/heads/main", author, author, "Base commit", tree, []
    )

    # Create two commits on main
    main1 = repo.create_commit(
        "refs/heads/main", author, author, "Main commit 1", tree, [base]
    )
    main2 = repo.create_commit(
        "refs/heads/main", author, author, "Main commit 2", tree, [main1]
    )

    # Create feature branch with one commit
    feature1 = repo.create_commit(
        "refs/heads/feature", author, author, "Feature commit 1", tree, [base]
    )

    # Create merge commit (first parent: main2, second parent: feature1)
    merge = repo.create_commit(
        "refs/heads/main",
        author,
        author,
        "Merge feature into main",
        tree,
        [main2, feature1],
    )

    return repo_path, {
        "base": str(base),
        "main1": str(main1),
        "main2": str(main2),
        "feature1": str(feature1),
        "merge": str(merge),
    }
