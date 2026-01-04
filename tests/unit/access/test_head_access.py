# @generated "partially" Claude-Sonnet-4.5: Code
# @generated "partially" ChatGPT-4.1: Documentation
"""
Tests for the HeadAccess class and HEAD state logic.

Covers detection of HEAD state (normal, detached, unborn), correct reporting of HEAD target and branch, and property checks for various repository scenarios.
"""

import pygit2
import pytest

from gittergraph.access.head_access import HeadAccess
from gittergraph.models import HeadState


class TestGetInfo:
    """
    Tests for the get_info method of HeadAccess.

    Covers HEAD state detection and info extraction for normal, detached, and unborn HEAD states, as well as branch switching and edge cases.
    """

    def test_normal_head_on_main_branch(self, simple_repo):
        """
        Test HEAD in normal state pointing to main branch.

        Ensures correct state, target, and branch name for HEAD on main.
        """
        repo_path, commit_ids = simple_repo

        # Ensure HEAD is set to main branch
        repo = pygit2.Repository(str(repo_path))
        repo.set_head("refs/heads/main")

        access = HeadAccess(repo_path)
        info = access.get_info()

        assert info.state == HeadState.NORMAL
        assert info.target_id == commit_ids[0]
        assert info.branch_name == "refs/heads/main"
        assert not info.is_detached

    def test_normal_head_on_feature_branch(self, repo_with_branches):
        """
        Test HEAD in normal state pointing to feature branch.

        Ensures correct state, target, and branch name for HEAD on feature.
        """
        repo_path, commit_ids = repo_with_branches

        # Switch to feature branch
        repo = pygit2.Repository(str(repo_path))
        repo.set_head("refs/heads/feature")

        access = HeadAccess(repo_path)
        info = access.get_info()

        assert info.state == HeadState.NORMAL
        assert info.target_id == commit_ids[2]  # feature branch commit
        assert info.branch_name == "refs/heads/feature"
        assert not info.is_detached

    def test_detached_head(self, repo_with_history):
        """
        Test HEAD in detached state.

        Ensures correct state, target, and branch name for detached HEAD.
        """
        repo_path, commit_ids = repo_with_history

        # Detach HEAD to specific commit
        repo = pygit2.Repository(str(repo_path))
        commit = repo.get(commit_ids[2])
        repo.set_head(commit.id)

        access = HeadAccess(repo_path)
        info = access.get_info()

        assert info.state == HeadState.DETACHED
        assert info.target_id == commit_ids[2]
        assert info.branch_name is None
        assert info.is_detached

    def test_unborn_head(self, empty_repo):
        """
        Test HEAD in unborn state (empty repository).

        Ensures correct state and None values for target and branch name.
        """
        repo_path, _ = empty_repo

        access = HeadAccess(repo_path)
        info = access.get_info()

        assert info.state == HeadState.UNBORN
        assert info.target_id is None
        assert info.branch_name is None
        assert not info.is_detached

    @pytest.mark.parametrize(
        "branch_name",
        [
            "main",
            "develop",
            "feature/new-feature",
            "bugfix/fix-123",
        ],
    )
    def test_normal_head_on_different_branches(self, empty_repo, branch_name):
        """
        Test HEAD pointing to various branch names.

        Ensures correct state, target, and branch name for HEAD on different branches.
        """
        repo_path, repo = empty_repo

        # Create commit on specific branch
        tree = repo.TreeBuilder().write()
        author = pygit2.Signature("Test", "test@example.com")
        id_ = repo.create_commit(
            f"refs/heads/{branch_name}", author, author, "Test commit", tree, []
        )

        # Set HEAD to the branch
        repo.set_head(f"refs/heads/{branch_name}")

        access = HeadAccess(repo_path)
        info = access.get_info()

        assert info.state == HeadState.NORMAL
        assert info.target_id == str(id_)
        assert info.branch_name == f"refs/heads/{branch_name}"

    def test_detached_head_at_different_commits(self, repo_with_history):
        """
        Test detached HEAD at various commits in history.

        Ensures correct state, target, and branch name for HEAD detached at each commit.
        """
        repo_path, commit_ids = repo_with_history
        repo = pygit2.Repository(str(repo_path))

        # Test detached HEAD at each commit
        for _, commit_id in enumerate(commit_ids):
            commit = repo.get(commit_id)
            repo.set_head(commit.id)

            access = HeadAccess(repo_path)
            info = access.get_info()

            assert info.state == HeadState.DETACHED
            assert info.target_id == commit_id
            assert info.branch_name is None
            assert info.is_detached

    def test_head_after_switching_branches(self, repo_with_branches):
        """
        Test HEAD info updates correctly when switching branches.

        Ensures state and branch name are updated after branch switches and detaching.
        """
        repo_path, commit_ids = repo_with_branches
        repo = pygit2.Repository(str(repo_path))

        # Set HEAD to main first
        repo.set_head("refs/heads/main")

        access = HeadAccess(repo_path)

        # Initially on main
        info = access.get_info()
        assert info.state == HeadState.NORMAL
        assert info.branch_name == "refs/heads/main"

        # Switch to feature
        repo.set_head("refs/heads/feature")
        info = access.get_info()
        assert info.state == HeadState.NORMAL
        assert info.branch_name == "refs/heads/feature"
        assert info.target_id == commit_ids[2]

        # Detach HEAD
        commit = repo.get(commit_ids[0])
        repo.set_head(commit.id)
        info = access.get_info()
        assert info.state == HeadState.DETACHED
        assert info.branch_name is None
        assert info.target_id == commit_ids[0]


def test_head_info_properties(repo_detached_head):
    """
    Test HeadInfo helper properties.

    Checks is_detached property for detached HEAD state.
    """
    repo_path, _ = repo_detached_head
    access = HeadAccess(repo_path)

    info = access.get_info()

    # is_detached should return True for detached HEAD
    assert info.is_detached
    assert info.state == HeadState.DETACHED


def test_head_info_not_detached(simple_repo):
    """
    Test HeadInfo.is_detached returns False for normal HEAD.

    Checks is_detached property for normal HEAD state.
    """
    repo_path, _ = simple_repo

    # Ensure HEAD is set to main branch
    repo = pygit2.Repository(str(repo_path))
    repo.set_head("refs/heads/main")

    access = HeadAccess(repo_path)
    info = access.get_info()

    assert not info.is_detached
    assert info.state == HeadState.NORMAL
