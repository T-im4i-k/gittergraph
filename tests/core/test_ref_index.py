# @generated "all" Claude-Sonnet-4.5
"""
RefIndex tests.

Unit tests for the RefIndex class, covering branch and tag indexing, lookup, and edge cases for various repository structures.
"""

import pytest

from tests.core.core_helper import get_ref_index


class TestRefIndex:
    """
    RefIndex test cases.

    Covers branch and tag indexing, lookup, and edge cases for various repository structures.
    """

    def test_get_branches_at_commit_single_branch(self, simple_repo):
        """
        Branch lookup for a commit with one branch.

        Returns a single branch for a commit pointed to by one branch.
        """
        repo_path, commit_ids = simple_repo
        index = get_ref_index(repo_path)
        result = index.get_branches_at_commit(commit_ids[0])
        assert len(result) == 1
        assert result[0].name == "refs/heads/main"
        assert result[0].target_id == commit_ids[0]

    def test_get_branches_at_commit_multiple_branches(self, repo_with_branches):
        """
        Branch lookup for a commit with multiple branches.

        Returns all branches pointing to a commit.
        """
        repo_path, commit_ids = repo_with_branches
        index = get_ref_index(repo_path)
        result = index.get_branches_at_commit(commit_ids[1])
        assert len(result) == 1
        assert result[0].name == "refs/heads/main"

    def test_get_branches_at_commit_no_branches(self, simple_repo):
        """
        Branch lookup for a commit with no branches.

        Returns an empty list for a commit with no branches.
        """
        repo_path, _ = simple_repo
        index = get_ref_index(repo_path)
        result = index.get_branches_at_commit("0" * 40)
        assert result == []

    def test_get_tags_at_commit_single_tag(self, repo_with_lightweight_tag):
        """
        Tag lookup for a commit with one tag.

        Returns a single tag for a commit pointed to by one tag.
        """
        repo_path, commit_ids = repo_with_lightweight_tag
        index = get_ref_index(repo_path)
        result = index.get_tags_at_commit(commit_ids[0])
        assert len(result) == 1
        assert result[0].name == "refs/tags/v1.0.0"
        assert result[0].target_id == commit_ids[0]

    def test_get_tags_at_commit_multiple_tags(self, repo_with_multiple_tags):
        """
        Tag lookup for a commit with multiple tags.

        Returns all tags pointing to a commit.
        """
        repo_path, commit_ids = repo_with_multiple_tags
        index = get_ref_index(repo_path)
        result = index.get_tags_at_commit(commit_ids[1])
        assert len(result) == 2
        tag_names = {tag.name for tag in result}
        assert "refs/tags/v2.0.0" in tag_names
        assert "refs/tags/latest" in tag_names

    def test_get_tags_at_commit_no_tags(self, simple_repo):
        """
        Tag lookup for a commit with no tags.

        Returns an empty list for a commit with no tags.
        """
        repo_path, commit_ids = simple_repo
        index = get_ref_index(repo_path)
        result = index.get_tags_at_commit(commit_ids[0])
        assert result == []

    def test_get_tags_at_commit_nonexistent(self, repo_with_lightweight_tag):
        """
        Tag lookup for a non-existent commit.

        Returns an empty list for a non-existent commit ID.
        """
        repo_path, _ = repo_with_lightweight_tag
        index = get_ref_index(repo_path)
        result = index.get_tags_at_commit("0" * 40)
        assert result == []

    def test_index_with_remote_branches(self, repo_with_remote_tracking):
        """
        Branch indexing with remote-tracking branches.

        Returns both local and remote branches for a commit.
        """
        repo_path, commit_ids = repo_with_remote_tracking
        index = get_ref_index(repo_path)
        result = index.get_branches_at_commit(commit_ids[0])
        assert len(result) == 2
        branch_names = {branch.name for branch in result}
        assert "refs/heads/main" in branch_names
        assert "refs/remotes/origin/main" in branch_names

    def test_index_with_mixed_references(self, repo_with_multiple_tags):
        """
        Indexing with both branches and tags.

        Returns correct results for commits with both branch and tag references.
        """
        repo_path, commit_ids = repo_with_multiple_tags
        index = get_ref_index(repo_path)
        tags_c1 = index.get_tags_at_commit(commit_ids[0])
        assert len(tags_c1) == 1
        assert tags_c1[0].name == "refs/tags/v1.0.0"
        branches_c2 = index.get_branches_at_commit(commit_ids[1])
        tags_c2 = index.get_tags_at_commit(commit_ids[1])
        assert len(branches_c2) == 1
        assert branches_c2[0].name == "refs/heads/main"
        assert len(tags_c2) == 2

    def test_index_with_empty_repository(self, empty_repo):
        """
        Indexing in an empty repository.

        Returns empty lists for any commit ID in an empty repo.
        """
        repo_path, _ = empty_repo
        index = get_ref_index(repo_path)
        assert index.get_branches_at_commit("0" * 40) == []
        assert index.get_tags_at_commit("0" * 40) == []

    def test_index_with_history(self, repo_with_history):
        """
        Branch indexing in a commit history.

        Returns only the latest commit with a branch pointing to it.
        """
        repo_path, commit_ids = repo_with_history
        index = get_ref_index(repo_path)
        for i, commit_id in enumerate(commit_ids):
            result = index.get_branches_at_commit(commit_id)
            if i == len(commit_ids) - 1:
                assert len(result) == 1
                assert result[0].name == "refs/heads/main"
            else:
                assert result == []

    @pytest.mark.parametrize("commit_index", [0, 1, 2])
    def test_get_branches_various_commits(self, repo_with_branches, commit_index):
        """
        Branch lookup for various commits in a multi-branch repo.

        Returns the correct branch for each commit index.
        """
        repo_path, commit_ids = repo_with_branches
        index = get_ref_index(repo_path)
        result = index.get_branches_at_commit(commit_ids[commit_index])
        if commit_index == 0:
            assert result == []
        elif commit_index == 1:
            assert len(result) == 1
            assert result[0].name == "refs/heads/main"
        elif commit_index == 2:
            assert len(result) == 1
            assert result[0].name == "refs/heads/feature"

    def test_annotated_tag_in_index(self, repo_with_annotated_tag):
        """
        Indexing of annotated tags.

        Returns annotated tags for their commit.
        """
        repo_path, commit_ids = repo_with_annotated_tag
        index = get_ref_index(repo_path)
        result = index.get_tags_at_commit(commit_ids[0])
        assert len(result) == 1
        assert result[0].name == "refs/tags/v2.0.0"
        assert result[0].target_id == commit_ids[0]

    def test_multiple_remote_branches(self, repo_with_remote_branches):
        """
        Indexing with multiple remote branches.

        Returns all remote-tracking branches for their commits.
        """
        repo_path, commit_ids = repo_with_remote_branches
        index = get_ref_index(repo_path)
        result_c1 = index.get_branches_at_commit(commit_ids[0])
        branch_names_c1 = {branch.name for branch in result_c1}
        assert "refs/heads/main" in branch_names_c1
        assert "refs/remotes/origin/main" in branch_names_c1
        assert "refs/remotes/upstream/main" in branch_names_c1
        result_c2 = index.get_branches_at_commit(commit_ids[1])
        branch_names_c2 = {branch.name for branch in result_c2}
        assert "refs/heads/develop" in branch_names_c2
        assert "refs/remotes/origin/develop" in branch_names_c2
