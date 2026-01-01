# @generated "all" Claude-Sonnet-4.5
"""
Tests for HistoryWalker class.

Tests commit history traversal functionality, including linear history walking and first-parent chain following.
"""

import pygit2
import pytest

from gittergraph.access import GitRepository
from gittergraph.core.history_walker import HistoryWalker


class TestHistoryWalker:
    """Tests for HistoryWalker class."""

    def test_linear_history_single_commit(self, simple_repo):
        """
        Test linear history with a single commit.

        Ensures that a repository with one commit returns a list containing only that commit.
        """
        repo_path, commit_ids = simple_repo
        git_repo = GitRepository(repo_path)
        commits = git_repo.commits.get_all()

        walker = HistoryWalker(commits)
        history = walker.get_linear_history_from_commit(commit_ids[0])

        assert len(history) == 1
        assert history[0].id == commit_ids[0]

    def test_linear_history_multiple_commits(self, repo_with_history):
        """
        Test linear history with multiple commits.

        Ensures that a linear commit chain is traversed correctly in newest-first order.
        """
        repo_path, commit_ids = repo_with_history
        git_repo = GitRepository(repo_path)
        commits = git_repo.commits.get_all()

        walker = HistoryWalker(commits)
        # Start from the last (newest) commit
        history = walker.get_linear_history_from_commit(commit_ids[-1])

        assert len(history) == 5
        # Verify order (newest to oldest)
        for i, commit in enumerate(history):
            assert commit.id == commit_ids[-(i + 1)]

    def test_linear_history_from_middle_commit(self, repo_with_history):
        """
        Test linear history starting from a middle commit.

        Ensures that traversal from a middle commit only includes ancestors.
        """
        repo_path, commit_ids = repo_with_history
        git_repo = GitRepository(repo_path)
        commits = git_repo.commits.get_all()

        walker = HistoryWalker(commits)
        # Start from the 3rd commit (index 2)
        history = walker.get_linear_history_from_commit(commit_ids[2])

        assert len(history) == 3
        assert history[0].id == commit_ids[2]
        assert history[1].id == commit_ids[1]
        assert history[2].id == commit_ids[0]

    def test_linear_history_nonexistent_commit(self, simple_repo):
        """
        Test linear history with non-existent commit ID.

        Ensures that querying a non-existent commit returns an empty list.
        """
        repo_path, _ = simple_repo
        git_repo = GitRepository(repo_path)
        commits = git_repo.commits.get_all()

        walker = HistoryWalker(commits)
        history = walker.get_linear_history_from_commit("0" * 40)

        assert not history

    def test_linear_history_empty_repository(self, empty_repo):
        """
        Test linear history with an empty repository.

        Ensures that an empty repository returns an empty history.
        """
        repo_path, _ = empty_repo
        git_repo = GitRepository(repo_path)
        commits = git_repo.commits.get_all()

        walker = HistoryWalker(commits)
        history = walker.get_linear_history_from_commit("0" * 40)

        assert not history

    def test_linear_history_follows_first_parent(self, repo_with_merge):
        """
        Test that linear history follows first parent in merge commits.

        Ensures that only the first parent chain is followed, ignoring merge parents.
        """
        repo_path, commit_ids = repo_with_merge
        git_repo = GitRepository(repo_path)
        commits = git_repo.commits.get_all()

        walker = HistoryWalker(commits)
        # Start from merge commit
        merge_commit_id = commit_ids["merge"]
        history = walker.get_linear_history_from_commit(merge_commit_id)

        # Should include: merge -> main2 -> main1 -> base
        assert len(history) == 4
        assert history[0].id == commit_ids["merge"]
        assert history[1].id == commit_ids["main2"]
        assert history[2].id == commit_ids["main1"]
        assert history[3].id == commit_ids["base"]

        # Should NOT include feature branch commits
        for commit in history:
            assert commit.id != commit_ids["feature1"]

    def test_linear_history_preserves_commit_objects(self, repo_with_history):
        """
        Test that history contains complete commit objects.

        Ensures that returned commits have all expected attributes (message, author, etc.).
        """
        repo_path, commit_ids = repo_with_history
        git_repo = GitRepository(repo_path)
        commits = git_repo.commits.get_all()

        walker = HistoryWalker(commits)
        history = walker.get_linear_history_from_commit(commit_ids[-1])

        for commit in history:
            assert hasattr(commit, "id")
            assert hasattr(commit, "message")
            assert hasattr(commit, "author")
            assert hasattr(commit, "committer")
            assert hasattr(commit, "parent_ids")
            assert commit.message.startswith("Commit")

    @pytest.mark.parametrize(
        "start_index,expected_length",
        [
            (0, 1),  # First commit
            (1, 2),  # Second commit
            (2, 3),  # Third commit
            (3, 4),  # Fourth commit
            (4, 5),  # Fifth commit
        ],
    )
    def test_linear_history_various_starting_points(
        self, repo_with_history, start_index, expected_length
    ):
        """
        Test linear history from various starting points.

        Ensures correct history length when starting from different commits in the chain.
        """
        repo_path, commit_ids = repo_with_history
        git_repo = GitRepository(repo_path)
        commits = git_repo.commits.get_all()

        walker = HistoryWalker(commits)
        history = walker.get_linear_history_from_commit(commit_ids[start_index])

        assert len(history) == expected_length
        # First commit in history should be the starting commit
        assert history[0].id == commit_ids[start_index]


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
