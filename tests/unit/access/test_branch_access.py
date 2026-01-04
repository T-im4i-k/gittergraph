# @generated "partially" Claude-Sonnet-4.5: Code
# @generated "partially" ChatGPT-4.1: Documentation
"""
Tests for the BranchAccess class and branch model properties.

Covers conversion of pygit2 branches to model objects, retrieval of local and remote branches, and property logic for branch names and types.
"""

import pygit2
import pytest

from gittergraph.access.branch_access import BranchAccess
from gittergraph.models import Branch


class TestToModel:
    """
    Tests for the to_model static method.

    Covers conversion of pygit2 local and remote branches to Branch model objects and property checks.
    """

    def test_converts_local_branch(self, simple_repo):
        """
        Test converting a local branch to Branch model.

        Verifies correct conversion and property values for a local branch.
        """
        repo_path, _ = simple_repo
        repo = pygit2.Repository(str(repo_path))

        pygit_branch = repo.branches["main"]
        branch = BranchAccess.to_model(pygit_branch)

        assert isinstance(branch, Branch)
        assert branch.name == "refs/heads/main"
        assert branch.target_id == str(pygit_branch.target)
        assert not branch.is_remote
        assert branch.shorthand == "main"

    def test_converts_remote_branch(self, repo_with_remote_tracking):
        """
        Test converting a remote branch to Branch model.

        Verifies correct conversion and property values for a remote branch.
        """
        repo_path, commit_ids = repo_with_remote_tracking
        repo = pygit2.Repository(str(repo_path))

        pygit_branch = repo.branches["origin/main"]
        branch = BranchAccess.to_model(pygit_branch)

        assert branch.name == "refs/remotes/origin/main"
        assert branch.target_id == commit_ids[0]
        assert branch.is_remote
        assert branch.shorthand == "origin/main"


class TestGet:
    """
    Tests for the get method.

    Covers retrieval of local and remote branches by name, error handling, and naming conventions.
    """

    def test_get_existing_local_branch(self, simple_repo):
        """
        Test getting an existing local branch.

        Ensures correct retrieval and property values for a local branch.
        """
        repo_path, commit_ids = simple_repo
        access = BranchAccess(repo_path)

        branch = access.get("refs/heads/main")

        assert branch.name == "refs/heads/main"
        assert branch.target_id == commit_ids[0]
        assert not branch.is_remote

    def test_get_existing_remote_branch(self, repo_with_remote_tracking):
        """
        Test getting an existing remote branch.

        Ensures correct retrieval and property values for a remote branch.
        """
        repo_path, commit_ids = repo_with_remote_tracking

        access = BranchAccess(repo_path)
        branch = access.get("refs/remotes/origin/main")

        assert branch.name == "refs/remotes/origin/main"
        assert branch.target_id == commit_ids[0]
        assert branch.is_remote

    def test_get_nonexistent_branch_raises_keyerror(self, simple_repo):
        """
        Test that getting a non-existent branch raises KeyError.

        Ensures KeyError is raised for missing branch names.
        """
        repo_path, _ = simple_repo
        access = BranchAccess(repo_path)

        with pytest.raises(KeyError, match="Branch 'nonexistent' not found"):
            access.get("nonexistent")

    @pytest.mark.parametrize(
        "branch_name",
        [
            "refs/heads/develop",
            "refs/heads/feature/new-feature",
            "refs/heads/bugfix/fix-123",
            "refs/heads/release/v1.0.0",
        ],
    )
    def test_get_various_branch_names(self, tmp_path, branch_name):
        """
        Test getting branches with various naming conventions.

        Ensures correct retrieval and property values for branches with different naming patterns.
        """
        repo_path = tmp_path / "test_repo"
        repo = pygit2.init_repository(str(repo_path))

        tree = repo.TreeBuilder().write()
        author = pygit2.Signature("Test", "test@example.com")
        id_ = repo.create_commit(branch_name, author, author, "Commit", tree, [])

        access = BranchAccess(repo_path)
        branch = access.get(branch_name)

        assert branch.name == branch_name
        assert branch.shorthand == branch_name.removeprefix("refs/heads/")
        assert branch.target_id == str(id_)


class TestGetAll:
    """
    Tests for the get_all method.

    Covers retrieval of all local and remote branches, dictionary keying, and edge cases for empty repositories and multiple branches.
    """

    def test_get_all_single_branch(self, simple_repo):
        """
        Test get_all with a single branch.

        Ensures correct retrieval and dictionary structure for a single branch.
        """
        repo_path, commit_ids = simple_repo
        access = BranchAccess(repo_path)

        branches = access.get_all()

        assert len(branches) == 1
        assert "refs/heads/main" in branches
        assert branches["refs/heads/main"].target_id == commit_ids[0]

    def test_get_all_multiple_local_branches(self, repo_with_branches):
        """
        Test get_all with multiple local branches.

        Ensures correct retrieval and dictionary structure for multiple local branches.
        """
        repo_path, commit_ids = repo_with_branches
        access = BranchAccess(repo_path)

        branches = access.get_all()

        assert len(branches) == 2
        assert "refs/heads/main" in branches
        assert "refs/heads/feature" in branches
        assert branches["refs/heads/main"].target_id == commit_ids[1]
        assert branches["refs/heads/feature"].target_id == commit_ids[2]

    def test_get_all_with_remote_branches(self, repo_with_remote_branches):
        """
        Test get_all includes remote branches.

        Ensures remote branches are included in the result and properties are correct.
        """
        repo_path, _ = repo_with_remote_branches
        access = BranchAccess(repo_path)

        branches = access.get_all()

        # Should have 2 local + 3 remote = 5 total
        assert len(branches) == 5

        # Check local branches
        assert "refs/heads/main" in branches
        assert "refs/heads/develop" in branches

        # Check remote branches
        assert "refs/remotes/origin/main" in branches
        assert "refs/remotes/origin/develop" in branches
        assert "refs/remotes/upstream/main" in branches

        # Verify is_remote property
        assert not branches["refs/heads/main"].is_remote
        assert branches["refs/remotes/origin/main"].is_remote

    def test_get_all_empty_repo(self, empty_repo):
        """
        Test get_all with an empty repository.

        Ensures an empty dictionary is returned when no branches exist.
        """
        repo_path, _ = empty_repo
        access = BranchAccess(repo_path)

        branches = access.get_all()

        assert len(branches) == 0

    def test_get_all_returns_dict_keyed_by_full_name(self, repo_with_branches):
        """
        Test that get_all returns a dictionary keyed by full ref names.

        Ensures dictionary keys match full branch ref names for all branches.
        """
        repo_path, _ = repo_with_branches
        access = BranchAccess(repo_path)

        branches = access.get_all()

        # Keys should be full ref names
        for key, branch in branches.items():
            assert key == branch.name
            assert key.startswith("refs/heads/") or key.startswith("refs/remotes/")

    @pytest.mark.parametrize("branch_count", [1, 5, 10])
    def test_get_all_with_multiple_branches(self, tmp_path, branch_count):
        """
        Test get_all with varying numbers of branches.

        Ensures correct retrieval and dictionary structure for different branch counts.
        """
        repo_path = tmp_path / "test_repo"
        repo = pygit2.init_repository(str(repo_path))

        tree = repo.TreeBuilder().write()
        author = pygit2.Signature("Test", "test@example.com")

        for i in range(branch_count):
            repo.create_commit(
                f"refs/heads/branch{i}", author, author, f"Commit {i}", tree, []
            )

        access = BranchAccess(repo_path)
        branches = access.get_all()

        assert len(branches) == branch_count


class TestBranchProperties:
    """
    Tests for Branch model properties via BranchAccess.

    Covers property logic for local and remote branches, including shorthand extraction and name handling.
    """

    def test_local_branch_properties(self, simple_repo):
        """
        Test properties of a local branch.

        Verifies is_remote, shorthand, and name for a local branch.
        """
        repo_path, _ = simple_repo
        access = BranchAccess(repo_path)

        branch = access.get("refs/heads/main")

        assert not branch.is_remote
        assert branch.shorthand == "main"
        assert branch.name == "refs/heads/main"

    def test_remote_branch_properties(self, repo_with_remote_tracking):
        """
        Test properties of a remote branch.

        Verifies is_remote, shorthand, and name for a remote branch.
        """
        repo_path, _ = repo_with_remote_tracking

        access = BranchAccess(repo_path)
        branch = access.get("refs/remotes/origin/main")

        assert branch.is_remote
        assert branch.shorthand == "origin/main"
        assert branch.name == "refs/remotes/origin/main"

    def test_branch_with_slashes_in_name(self, tmp_path):
        """
        Test branch with slashes in the name.

        Ensures correct shorthand and name for branches with slashes.
        """
        repo_path = tmp_path / "test_repo"
        repo = pygit2.init_repository(str(repo_path))

        tree = repo.TreeBuilder().write()
        author = pygit2.Signature("Test", "test@example.com")
        repo.create_commit(
            "refs/heads/feature/add-login", author, author, "Commit", tree, []
        )

        access = BranchAccess(repo_path)
        branch = access.get("refs/heads/feature/add-login")

        assert branch.shorthand == "feature/add-login"
        assert branch.name == "refs/heads/feature/add-login"
