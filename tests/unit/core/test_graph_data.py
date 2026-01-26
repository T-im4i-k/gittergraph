# @generated "all" Claude-Sonnet-4.5
"""
GitGraphData tests.

Unit tests for the GitGraphData dataclass, covering data loading, immutability, and snapshot functionality.
"""

import pygit2
import pytest

from gittergraph.access import GitRepository
from gittergraph.core.graph_data import GitGraphData
from tests.unit.core.core_helper import get_graph_data


class TestGitGraphData:
    """
    GitGraphData test cases.

    Covers data loading, immutability, and snapshot functionality.
    """

    def test_load_from_simple_repo(self, simple_repo):
        """
        Load data from a simple repository.

        Returns a GitGraphData with commits, branches, tags, and HEAD info.
        """
        repo_path, commit_ids = simple_repo
        data = get_graph_data(repo_path)

        assert len(data.commits) == 1
        assert commit_ids[0] in data.commits
        assert len(data.branches) == 1
        assert "refs/heads/main" in data.branches
        assert len(data.tags) == 0
        assert data.head_info is not None

    def test_load_from_empty_repo(self, empty_repo):
        """
        Load data from an empty repository.

        Returns a GitGraphData with empty collections.
        """
        repo_path, _ = empty_repo
        data = get_graph_data(repo_path)

        assert len(data.commits) == 0
        assert len(data.branches) == 0
        assert len(data.tags) == 0
        assert data.head_info is not None

    def test_load_from_repo_with_history(self, repo_with_history):
        """
        Load data from a repository with commit history.

        Returns a GitGraphData with all commits in the history.
        """
        repo_path, commit_ids = repo_with_history
        data = get_graph_data(repo_path)

        assert len(data.commits) == 5
        for commit_id in commit_ids:
            assert commit_id in data.commits
        assert len(data.branches) == 1
        assert "refs/heads/main" in data.branches

    def test_load_from_repo_with_branches(self, repo_with_branches):
        """
        Load data from a repository with multiple branches.

        Returns a GitGraphData with all branches indexed.
        """
        repo_path, _ = repo_with_branches
        data = get_graph_data(repo_path)

        assert len(data.commits) == 3
        assert len(data.branches) == 2
        assert "refs/heads/main" in data.branches
        assert "refs/heads/feature" in data.branches

    def test_load_from_repo_with_tags(self, repo_with_multiple_tags):
        """
        Load data from a repository with tags.

        Returns a GitGraphData with all tags indexed.
        """
        repo_path, _ = repo_with_multiple_tags
        data = get_graph_data(repo_path)

        assert len(data.commits) == 2
        assert len(data.tags) == 3
        assert "refs/tags/v1.0.0" in data.tags
        assert "refs/tags/v2.0.0" in data.tags
        assert "refs/tags/latest" in data.tags

    def test_load_from_repo_with_remote_branches(self, repo_with_remote_tracking):
        """
        Load data from a repository with remote branches.

        Returns a GitGraphData with both local and remote branches.
        """
        repo_path, _ = repo_with_remote_tracking
        data = get_graph_data(repo_path)

        assert len(data.commits) == 1
        assert len(data.branches) == 2
        assert "refs/heads/main" in data.branches
        assert "refs/remotes/origin/main" in data.branches

    def test_commits_dictionary_structure(self, repo_with_history):
        """
        Verify commits dictionary structure.

        Returns commits keyed by commit ID with Commit objects as values.
        """
        repo_path, _ = repo_with_history
        data = get_graph_data(repo_path)

        for commit_id, commit in data.commits.items():
            assert commit_id == commit.id
            assert hasattr(commit, "message")
            assert hasattr(commit, "author")
            assert hasattr(commit, "committer")
            assert hasattr(commit, "parent_ids")

    def test_branches_dictionary_structure(self, repo_with_branches):
        """
        Verify branches dictionary structure.

        Returns branches keyed by full reference name with Branch objects as values.
        """
        repo_path, _ = repo_with_branches
        data = get_graph_data(repo_path)

        for branch_name, branch in data.branches.items():
            assert branch_name == branch.name
            assert hasattr(branch, "target_id")
            assert hasattr(branch, "is_remote")

    def test_tags_dictionary_structure(self, repo_with_multiple_tags):
        """
        Verify tags dictionary structure.

        Returns tags keyed by full reference name with Tag objects as values.
        """
        repo_path, _ = repo_with_multiple_tags
        data = get_graph_data(repo_path)

        for tag_name, tag in data.tags.items():
            assert tag_name == tag.name
            assert hasattr(tag, "target_id")

    def test_head_info_structure(self, simple_repo):
        """
        Verify HEAD info structure.

        Returns HEAD info with state and target information.
        """
        repo_path, commit_ids = simple_repo

        repo = pygit2.Repository(str(repo_path))
        repo.set_head("refs/heads/main")

        data = get_graph_data(repo_path)

        assert data.head_info is not None
        assert hasattr(data.head_info, "state")
        assert hasattr(data.head_info, "target_id")
        assert hasattr(data.head_info, "branch_name")
        assert data.head_info.target_id == commit_ids[0]

    def test_head_info_detached(self, repo_detached_head):
        """
        Verify HEAD info in detached state.

        Returns HEAD info with detached state.
        """
        repo_path, commit_ids = repo_detached_head
        data = get_graph_data(repo_path)

        assert data.head_info is not None
        assert data.head_info.is_detached
        assert data.head_info.target_id == commit_ids[0]

    def test_load_from_multiple_calls(self, simple_repo):
        """
        Load data multiple times from the same repository.

        Returns consistent data across multiple loads.
        """
        repo_path, _ = simple_repo
        data1 = get_graph_data(repo_path)
        data2 = get_graph_data(repo_path)

        assert len(data1.commits) == len(data2.commits)
        assert len(data1.branches) == len(data2.branches)
        assert len(data1.tags) == len(data2.tags)
        assert data1.head_info.target_id == data2.head_info.target_id

    def test_load_from_with_annotated_tags(self, repo_with_annotated_tag):
        """
        Load data from repository with annotated tags.

        Returns GitGraphData with annotated tags properly loaded.
        """
        repo_path, commit_ids = repo_with_annotated_tag
        data = get_graph_data(repo_path)

        assert len(data.tags) == 1
        assert "refs/tags/v2.0.0" in data.tags
        tag = data.tags["refs/tags/v2.0.0"]
        assert tag.target_id == commit_ids[0]

    def test_load_from_with_lightweight_tags(self, repo_with_lightweight_tag):
        """
        Load data from repository with lightweight tags.

        Returns GitGraphData with lightweight tags properly loaded.
        """
        repo_path, commit_ids = repo_with_lightweight_tag
        data = get_graph_data(repo_path)

        assert len(data.tags) == 1
        assert "refs/tags/v1.0.0" in data.tags
        tag = data.tags["refs/tags/v1.0.0"]
        assert tag.target_id == commit_ids[0]

    def test_load_from_with_merge_commit(self, repo_with_merge):
        """
        Load data from repository with merge commits.

        Returns GitGraphData with merge commits and their parents.
        """
        repo_path, commit_ids = repo_with_merge
        data = get_graph_data(repo_path)

        merge_commit = data.commits[commit_ids["merge"]]
        assert len(merge_commit.parent_ids) == 2
        assert commit_ids["main2"] in merge_commit.parent_ids
        assert commit_ids["feature1"] in merge_commit.parent_ids

    def test_commits_contain_all_metadata(self, repo_different_author_and_commiter):
        """
        Verify commits contain complete metadata.

        Returns commits with author, committer, and message information.
        """
        repo_path, commit_ids = repo_different_author_and_commiter
        data = get_graph_data(repo_path)

        commit = data.commits[commit_ids[0]]
        assert commit.author.name == "Alice"
        assert commit.committer.name == "Bob"
        assert commit.message == "Initial commit"

    @pytest.mark.parametrize(
        "fixture_name,expected_commits,expected_branches",
        [
            ("simple_repo", 1, 1),
            ("repo_with_history", 5, 1),
            ("repo_with_branches", 3, 2),
        ],
    )
    def test_load_various_repositories(
        self, request, fixture_name, expected_commits, expected_branches
    ):
        """
        Load data from various repository structures.

        Returns correct counts for different repository configurations.
        """
        fixture = request.getfixturevalue(fixture_name)
        repo_path, _ = fixture
        data = get_graph_data(repo_path)

        assert len(data.commits) == expected_commits
        assert len(data.branches) == expected_branches

    def test_load_from_creates_new_instance(self, simple_repo):
        """
        Verify load_from creates new instances.

        Returns different instances for each load_from call.
        """
        repo_path, _ = simple_repo
        git_repo = GitRepository(repo_path)

        data1 = GitGraphData.load_from(git_repo)
        data2 = GitGraphData.load_from(git_repo)

        assert data1 is not data2
        assert data1.commits is not data2.commits
