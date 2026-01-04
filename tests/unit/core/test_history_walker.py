# @generated "all" Claude-Sonnet-4.5
"""
Tests for HistoryWalker class.

Tests commit history traversal functionality, including linear history walking and first-parent chain following.
"""

import pytest

from tests.unit.core.core_helper import get_history_walker


class TestHistoryWalker:
    """
    Tests for HistoryWalker class.

    Covers commit history traversal, linear walking, and first-parent chain following.
    """

    def test_linear_history_single_commit(self, simple_repo):
        """
        Test linear history with a single commit.

        Ensures that a repository with one commit returns a list containing only that commit.
        """
        repo_path, commit_ids = simple_repo
        walker = get_history_walker(repo_path)
        history = walker.get_linear_history_from_commit(commit_ids[0])

        assert len(history) == 1
        assert history[0].id == commit_ids[0]

    def test_linear_history_multiple_commits(self, repo_with_history):
        """
        Test linear history with multiple commits.

        Ensures that a linear commit chain is traversed correctly in newest-first order.
        """
        repo_path, commit_ids = repo_with_history
        walker = get_history_walker(repo_path)
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
        walker = get_history_walker(repo_path)
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
        walker = get_history_walker(repo_path)
        history = walker.get_linear_history_from_commit("0" * 40)

        assert not history

    def test_linear_history_empty_repository(self, empty_repo):
        """
        Test linear history with an empty repository.

        Ensures that an empty repository returns an empty history.
        """
        repo_path, _ = empty_repo
        walker = get_history_walker(repo_path)
        history = walker.get_linear_history_from_commit("0" * 40)

        assert not history

    def test_linear_history_follows_first_parent(self, repo_with_merge):
        """
        Test that linear history follows first parent in merge commits.

        Ensures that only the first parent chain is followed, ignoring merge parents.
        """
        repo_path, commit_ids = repo_with_merge
        walker = get_history_walker(repo_path)
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
        walker = get_history_walker(repo_path)
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
        walker = get_history_walker(repo_path)
        history = walker.get_linear_history_from_commit(commit_ids[start_index])

        assert len(history) == expected_length
        # First commit in history should be the starting commit
        assert history[0].id == commit_ids[start_index]
