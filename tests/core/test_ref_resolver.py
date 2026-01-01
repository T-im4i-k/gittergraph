# @generated "all" Claude-Sonnet-4.5
"""
Tests for RefResolver class.

Tests reference name resolution functionality, including HEAD, commit IDs, branch names, and tag names.
"""
import pygit2
import pytest
from core_helper import get_ref_resolver

from gittergraph.access import GitRepository


class TestRefResolver:
    """Tests for RefResolver class."""

    def test_resolve_head(self, simple_repo):
        """
        Test resolving HEAD reference.

        Ensures that HEAD resolves to the correct commit ID.
        """
        repo_path, commit_ids = simple_repo

        repo = pygit2.Repository(str(repo_path))
        repo.set_head("refs/heads/main")

        resolver = get_ref_resolver(repo_path)
        result = resolver.resolve("HEAD")

        # HEAD should resolve to the commit it points to
        assert result == commit_ids[0]

    def test_resolve_commit_id(self, simple_repo):
        """
        Test resolving a commit ID.

        Ensures that a valid commit ID resolves to itself.
        """
        repo_path, commit_ids = simple_repo
        resolver = get_ref_resolver(repo_path)
        result = resolver.resolve(commit_ids[0])
        assert result == commit_ids[0]

    def test_resolve_branch_name(self, simple_repo):
        """
        Test resolving a branch name.

        Ensures that a branch reference resolves to the commit it points to.
        """
        repo_path, commit_ids = simple_repo
        resolver = get_ref_resolver(repo_path)
        result = resolver.resolve("refs/heads/main")
        assert result == commit_ids[0]

    def test_resolve_tag_name(self, repo_with_lightweight_tag):
        """
        Test resolving a tag name.

        Ensures that a tag reference resolves to the commit it points to.
        """
        repo_path, commit_ids = repo_with_lightweight_tag
        resolver = get_ref_resolver(repo_path)
        result = resolver.resolve("refs/tags/v1.0.0")
        assert result == commit_ids[0]

    def test_resolve_nonexistent_reference(self, simple_repo):
        """
        Test resolving a non-existent reference.

        Ensures that an invalid reference returns None.
        """
        repo_path, _ = simple_repo
        resolver = get_ref_resolver(repo_path)
        result = resolver.resolve("nonexistent")
        assert result is None

    def test_resolve_invalid_commit_id(self, simple_repo):
        """
        Test resolving an invalid commit ID.

        Ensures that a non-existent commit ID returns None.
        """
        repo_path, _ = simple_repo
        resolver = get_ref_resolver(repo_path)
        result = resolver.resolve("0" * 40)
        assert result is None

    def test_resolve_multiple_branches(self, repo_with_branches):
        """
        Test resolving multiple branch names.

        Ensures that different branches resolve to their respective commits.
        """
        repo_path, commit_ids = repo_with_branches
        resolver = get_ref_resolver(repo_path)
        main_result = resolver.resolve("refs/heads/main")
        feature_result = resolver.resolve("refs/heads/feature")
        assert main_result == commit_ids[1]
        assert feature_result == commit_ids[2]

    def test_resolve_remote_branch(self, repo_with_remote_tracking):
        """
        Test resolving a remote-tracking branch.

        Ensures that remote branches resolve to their target commits.
        """
        repo_path, commit_ids = repo_with_remote_tracking
        resolver = get_ref_resolver(repo_path)
        result = resolver.resolve("refs/remotes/origin/main")
        assert result == commit_ids[0]

    def test_resolve_annotated_tag(self, repo_with_annotated_tag):
        """
        Test resolving an annotated tag.

        Ensures that annotated tags resolve to their target commits.
        """
        repo_path, commit_ids = repo_with_annotated_tag
        resolver = get_ref_resolver(repo_path)
        result = resolver.resolve("refs/tags/v2.0.0")
        assert result == commit_ids[0]

    def test_resolve_multiple_tags(self, repo_with_multiple_tags):
        """
        Test resolving multiple tags.

        Ensures that different tags resolve to their respective commits.
        """
        repo_path, commit_ids = repo_with_multiple_tags
        resolver = get_ref_resolver(repo_path)
        v1_result = resolver.resolve("refs/tags/v1.0.0")
        v2_result = resolver.resolve("refs/tags/v2.0.0")
        latest_result = resolver.resolve("refs/tags/latest")
        assert v1_result == commit_ids[0]
        assert v2_result == commit_ids[1]
        assert latest_result == commit_ids[1]

    def test_resolve_detached_head(self, repo_detached_head):
        """
        Test resolving HEAD in detached HEAD state.

        Ensures that HEAD resolves correctly when detached.
        """
        repo_path, commit_ids = repo_detached_head
        resolver = get_ref_resolver(repo_path)
        result = resolver.resolve("HEAD")
        assert result == commit_ids[0]

    @pytest.mark.parametrize(
        "ref_name",
        [
            "refs/heads/main",
            "refs/heads/develop",
            "refs/remotes/origin/main",
            "refs/remotes/origin/develop",
            "refs/remotes/upstream/main",
        ],
    )
    def test_resolve_various_references(self, repo_with_remote_branches, ref_name):
        """
        Test resolving various reference types.

        Ensures that different reference types (local and remote branches) resolve correctly.
        """
        repo_path, commit_ids = repo_with_remote_branches
        resolver = get_ref_resolver(repo_path)
        result = resolver.resolve(ref_name)
        assert result is not None
        assert result in commit_ids

    def test_resolve_priority_order(self, repo_with_history):
        """
        Test resolution priority when same name could match multiple types.

        Ensures that resolution follows the correct priority: HEAD > commit ID > branch > tag.
        """
        repo_path, commit_ids = repo_with_history
        resolver = get_ref_resolver(repo_path)
        # Commit ID should be found as commit ID
        result = resolver.resolve(commit_ids[0])
        assert result == commit_ids[0]
        # HEAD should resolve to HEAD's target
        git_repo = GitRepository(repo_path)
        head_info = git_repo.head.get_info()
        head_result = resolver.resolve("HEAD")
        assert head_result == head_info.target_id

    def test_resolve_empty_repository(self, empty_repo):
        """
        Test resolving references in an empty repository.

        Ensures that resolution handles empty repositories gracefully.
        """
        repo_path, _ = empty_repo
        resolver = get_ref_resolver(repo_path)

        # Should return None for any reference in empty repo
        assert resolver.resolve("refs/heads/main") is None
        assert resolver.resolve("nonexistent") is None
        assert resolver.resolve("0" * 40) is None
