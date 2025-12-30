# @generated "partially" Claude-Sonnet-4.5: Code
# @generated "partially" ChatGPT-4.1: Documentation
"""
Tests for the CommitAccess class and related commit conversion logic.

Provides pytest-based tests for commit access, conversion, and error handling.
"""

import pygit2
import pytest

from gittergraph.data.commit_access import CommitAccess
from gittergraph.models import Commit


class TestToModel:
    """
    Tests for the to_model static method.

    Covers conversion of pygit2 commits to Commit model objects, including
    handling of author/committer, message normalization, and parent IDs.
    """

    def test_converts_commit_correctly(self, simple_repo):
        """
        Test that to_model correctly converts a pygit2 commit.

        Verifies all fields are mapped as expected for a simple commit.
        """
        repo_path, commit_ids = simple_repo
        repo = pygit2.Repository(str(repo_path))
        pygit_commit = repo.get(commit_ids[0])

        commit = CommitAccess.to_model(pygit_commit)

        assert isinstance(commit, Commit)
        assert commit.id == commit_ids[0]
        assert commit.message == "Initial commit"
        assert commit.author.name == "Alice"
        assert commit.author.email == "alice@example.com"
        assert commit.author.time == 1234567890
        assert commit.author.time_offset == 60
        assert commit.committer.name == "Alice"
        assert not commit.parent_ids

    def test_converts_author_and_committer_separately(
        self, repo_different_author_and_commiter
    ):
        """
        Test that author and committer are converted correctly when different.

        Ensures both author and committer fields are handled independently.
        """
        repo_path, commit_ids = repo_different_author_and_commiter
        repo = pygit2.Repository(str(repo_path))

        pygit_commit = repo.get(commit_ids[0])
        commit = CommitAccess.to_model(pygit_commit)

        assert commit.author.name == "Alice"
        assert commit.author.email == "alice@example.com"
        assert commit.author.time == 1234567890
        assert commit.author.time_offset == 60

        assert commit.committer.name == "Bob"
        assert commit.committer.email == "bob@example.com"
        assert commit.committer.time == 1234567900
        assert commit.committer.time_offset == -60

    @pytest.mark.parametrize(
        "message,expected",
        [
            ("  Message with whitespace  \n\n", "Message with whitespace"),
            ("\n\nLeading newlines", "Leading newlines"),
            ("Trailing newlines\n\n\n", "Trailing newlines"),
            ("  Both  \n\n", "Both"),
        ],
    )
    def test_strips_commit_message(self, tmp_path, message, expected):
        """
        Test that commit message whitespace is stripped.

        Ensures leading/trailing whitespace and newlines are removed from commit messages.
        """
        repo_path = tmp_path / "test_repo"
        repo = pygit2.init_repository(str(repo_path))

        tree = repo.TreeBuilder().write()
        author = pygit2.Signature("Test", "test@example.com")

        id_ = repo.create_commit("refs/heads/main", author, author, message, tree, [])

        pygit_commit = repo.get(id_)
        commit = CommitAccess.to_model(pygit_commit)

        assert commit.message == expected

    def test_converts_parent_ids(self, repo_with_history):
        """
        Test that parent IDs are converted correctly.

        Verifies that parent commit hashes are properly extracted.
        """
        repo_path, commit_ids = repo_with_history
        repo = pygit2.Repository(str(repo_path))

        # Get the last commit (should have one parent)
        pygit_commit = repo.get(commit_ids[-1])
        commit = CommitAccess.to_model(pygit_commit)

        assert len(commit.parent_ids) == 1
        assert commit.parent_ids[0] == commit_ids[-2]


class TestGet:
    """
    Tests for the get method.

    Covers retrieval of commits by hash, error handling, and type validation.
    """

    def test_get_existing_commit(self, simple_repo):
        """
        Test getting a commit that exists.

        Ensures correct commit is returned for a valid hash.
        """
        repo_path, commit_ids = simple_repo
        access = CommitAccess(repo_path)

        commit = access.get(commit_ids[0])

        assert commit.id == commit_ids[0]
        assert commit.message == "Initial commit"

    def test_get_with_short_hash(self, simple_repo):
        """
        Test getting a commit with short hash.

        Ensures short hashes are resolved to full commit IDs.
        """
        repo_path, commit_ids = simple_repo
        access = CommitAccess(repo_path)

        short_hash = commit_ids[0][:7]
        commit = access.get(short_hash)

        assert commit.id == commit_ids[0]

    @pytest.mark.parametrize(
        "invalid_id",
        [
            "0" * 40,  # Non-existent full hash
            "abc123",  # Non-existent short hash
        ],
    )
    def test_get_nonexistent_commit_raises_keyerror(self, simple_repo, invalid_id):
        """
        Test that getting non-existent commit raises KeyError.

        Ensures KeyError is raised for missing commit hashes.
        """
        repo_path, _ = simple_repo
        access = CommitAccess(repo_path)

        with pytest.raises(KeyError, match="not found"):
            access.get(invalid_id)

    def test_get_non_commit_object_raises_valueerror(self, tmp_path):
        """
        Test that getting a non-commit object raises ValueError.

        Ensures ValueError is raised if the object is not a commit.
        """
        repo_path = tmp_path / "test_repo"
        repo = pygit2.init_repository(str(repo_path))

        # Create a tree object (not a commit)
        tree_id = repo.TreeBuilder().write()

        access = CommitAccess(repo_path)

        with pytest.raises(ValueError, match="is not a commit"):
            access.get(str(tree_id))


class TestGetAll:
    """
    Tests for the get_all method.

    Covers retrieval of all commits, deduplication, and edge cases (empty repo, tags, branches).
    """

    def test_get_all_single_commit(self, simple_repo):
        """
        Test get_all with single commit.

        Ensures the only commit is returned in the result.
        """
        repo_path, commit_ids = simple_repo
        access = CommitAccess(repo_path)

        commits = access.get_all()

        assert len(commits) == 1
        assert commit_ids[0] in commits
        assert commits[commit_ids[0]].message == "Initial commit"

    def test_get_all_linear_history(self, repo_with_history):
        """
        Test get_all with linear history.

        Ensures all commits in a linear history are returned.
        """
        repo_path, commit_ids = repo_with_history
        access = CommitAccess(repo_path)

        commits = access.get_all()

        assert len(commits) == len(commit_ids)
        for id_ in commit_ids:
            assert id_ in commits

    def test_get_all_with_branches(self, repo_with_branches):
        """
        Test get_all includes commits from all branches.

        Ensures commits from all branches are included in the result.
        """
        repo_path, commit_ids = repo_with_branches
        access = CommitAccess(repo_path)

        commits = access.get_all()

        assert len(commits) == len(commit_ids)
        for id_ in commit_ids:
            assert id_ in commits

    def test_get_all_empty_repo(self, tmp_path):
        """
        Test get_all with empty repository.

        Ensures an empty dict is returned for an empty repo.
        """
        repo_path = tmp_path / "test_repo"
        pygit2.init_repository(str(repo_path))

        access = CommitAccess(repo_path)
        commits = access.get_all()

        assert len(commits) == 0

    def test_get_all_with_tags(self, tmp_path):
        """
        Test get_all includes commits reachable from tags.

        Ensures commits pointed to by tags are included in the result.
        """
        repo_path = tmp_path / "test_repo"
        repo = pygit2.init_repository(str(repo_path))

        tree = repo.TreeBuilder().write()
        author = pygit2.Signature("Test", "test@example.com")

        id_ = repo.create_commit(
            "refs/heads/main", author, author, "Tagged commit", tree, []
        )

        # Create a tag
        repo.create_reference("refs/tags/v1.0", id_)

        access = CommitAccess(repo_path)
        commits = access.get_all()

        assert len(commits) == 1
        assert str(id_) in commits

    def test_get_all_deduplicates_commits(self, tmp_path):
        """
        Test that get_all doesn't duplicate commits in multiple branches.

        Ensures commits reachable from multiple refs are not duplicated.
        """
        repo_path = tmp_path / "test_repo"
        repo = pygit2.init_repository(str(repo_path))

        tree = repo.TreeBuilder().write()
        author = pygit2.Signature("Test", "test@example.com")

        # Create shared commit
        id_ = repo.create_commit(
            "refs/heads/main", author, author, "Shared commit", tree, []
        )

        # Point another branch to the same commit
        repo.create_reference("refs/heads/other", id_)

        access = CommitAccess(repo_path)
        commits = access.get_all()

        # Should only have one commit, not duplicated
        assert len(commits) == 1
        assert str(id_) in commits
