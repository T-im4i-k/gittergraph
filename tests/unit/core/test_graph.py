# @generated "all" Claude-Sonnet-4.5
"""
GitGraph tests.

Unit tests for the GitGraph class, covering graph initialization, data loading, helper methods, and repository operations.
"""

import pygit2

from gittergraph.core.graph import GitGraph
from tests.unit.core.core_helper import get_git_graph


class TestGitGraph:
    """
    GitGraph test cases.

    Covers graph initialization, data access, helper methods, and reload functionality.
    """

    def test_init_simple_repo(self, simple_repo):
        """
        Initialize graph from a simple repository.

        Returns a GitGraph with commits, branches, and helper indexes.
        """
        repo_path, commit_ids = simple_repo
        repo = pygit2.Repository(str(repo_path))
        repo.set_head("refs/heads/main")
        graph = get_git_graph(repo_path)

        assert len(graph.data.commits) == 1
        assert len(graph.data.branches) == 1
        assert graph.data.head_info is not None
        assert graph.data.head_info.target_id == commit_ids[0]

    def test_init_empty_repo(self, empty_repo):
        """
        Initialize graph from an empty repository.

        Returns a GitGraph with empty collections.
        """
        repo_path, _ = empty_repo
        graph = get_git_graph(repo_path)

        assert len(graph.data.commits) == 0
        assert len(graph.data.branches) == 0
        assert len(graph.data.tags) == 0

    def test_from_path(self, simple_repo):
        """
        Create graph from repository path.

        Returns a GitGraph initialized with repository data.
        """
        repo_path, _ = simple_repo
        graph = GitGraph.from_path(repo_path)

        assert graph.repo is not None
        assert graph.data is not None
        assert len(graph.data.commits) == 1

    def test_discover_from_subdirectory(self, simple_repo):
        """
        Discover repository from a subdirectory.

        Returns a GitGraph when discovering from inside the repository.
        """
        repo_path, _ = simple_repo
        subdir = repo_path / "subdir"
        subdir.mkdir()

        graph = GitGraph.discover(subdir)

        assert graph is not None
        assert graph.repo is not None

    def test_discover_no_repository(self, tmp_path):
        """
        Discover repository from a non-repository directory.

        Returns None when no repository is found.
        """
        non_repo_path = tmp_path / "not_a_repo"
        non_repo_path.mkdir()

        graph = GitGraph.discover(non_repo_path)

        assert graph is None

    def test_get_branches_at_commit_single_branch(self, simple_repo):
        """
        Get branches at a commit with one branch.

        Returns a list containing the single branch.
        """
        repo_path, commit_ids = simple_repo
        graph = get_git_graph(repo_path)

        branches = graph.get_branches_at_commit(commit_ids[0])

        assert len(branches) == 1
        assert branches[0].name == "refs/heads/main"

    def test_get_branches_at_commit_no_branches(self, simple_repo):
        """
        Get branches at a commit with no branches.

        Returns an empty list for a non-existent commit.
        """
        repo_path, _ = simple_repo
        graph = get_git_graph(repo_path)

        branches = graph.get_branches_at_commit("0" * 40)

        assert branches == []

    def test_get_branches_at_commit_multiple_branches(self, repo_with_remote_tracking):
        """
        Get branches at a commit with multiple branches.

        Returns all branches pointing to the commit.
        """
        repo_path, commit_ids = repo_with_remote_tracking
        graph = get_git_graph(repo_path)

        branches = graph.get_branches_at_commit(commit_ids[0])

        assert len(branches) == 2
        branch_names = {b.name for b in branches}
        assert "refs/heads/main" in branch_names
        assert "refs/remotes/origin/main" in branch_names

    def test_get_tags_at_commit_single_tag(self, repo_with_lightweight_tag):
        """
        Get tags at a commit with one tag.

        Returns a list containing the single tag.
        """
        repo_path, commit_ids = repo_with_lightweight_tag
        graph = get_git_graph(repo_path)

        tags = graph.get_tags_at_commit(commit_ids[0])

        assert len(tags) == 1
        assert tags[0].name == "refs/tags/v1.0.0"

    def test_get_tags_at_commit_no_tags(self, simple_repo):
        """
        Get tags at a commit with no tags.

        Returns an empty list for a commit with no tags.
        """
        repo_path, commit_ids = simple_repo
        graph = get_git_graph(repo_path)

        tags = graph.get_tags_at_commit(commit_ids[0])

        assert tags == []

    def test_get_tags_at_commit_multiple_tags(self, repo_with_multiple_tags):
        """
        Get tags at a commit with multiple tags.

        Returns all tags pointing to the commit.
        """
        repo_path, commit_ids = repo_with_multiple_tags
        graph = get_git_graph(repo_path)

        tags = graph.get_tags_at_commit(commit_ids[1])

        assert len(tags) == 2
        tag_names = {t.name for t in tags}
        assert "refs/tags/v2.0.0" in tag_names
        assert "refs/tags/latest" in tag_names

    def test_get_linear_history_from_head(self, repo_with_history):
        """
        Get linear history from HEAD.

        Returns commits in newest-first order following first-parent chain.
        """
        repo_path, commit_ids = repo_with_history
        repo = pygit2.Repository(str(repo_path))
        repo.set_head("refs/heads/main")
        graph = get_git_graph(repo_path)

        history = graph.get_linear_history("HEAD")

        assert len(history) == 5
        for i, commit in enumerate(history):
            assert commit.id == commit_ids[-(i + 1)]

    def test_get_linear_history_from_commit_id(self, repo_with_history):
        """
        Get linear history from a specific commit ID.

        Returns history starting from the given commit.
        """
        repo_path, commit_ids = repo_with_history
        graph = get_git_graph(repo_path)

        history = graph.get_linear_history(commit_ids[2])

        assert len(history) == 3
        assert history[0].id == commit_ids[2]
        assert history[1].id == commit_ids[1]
        assert history[2].id == commit_ids[0]

    def test_get_linear_history_from_branch(self, simple_repo):
        """
        Get linear history from a branch reference.

        Returns history starting from the branch head.
        """
        repo_path, commit_ids = simple_repo
        graph = get_git_graph(repo_path)

        history = graph.get_linear_history("refs/heads/main")

        assert len(history) == 1
        assert history[0].id == commit_ids[0]

    def test_get_linear_history_nonexistent_ref(self, simple_repo):
        """
        Get linear history from a non-existent reference.

        Returns an empty list for invalid references.
        """
        repo_path, _ = simple_repo
        graph = get_git_graph(repo_path)

        history = graph.get_linear_history("nonexistent")

        assert history == []


class TestGitGraphOperations:
    """
    GitGraph operations tests.

    Covers reload, empty checks, and data integrity operations.
    """

    def test_is_empty_with_empty_repo(self, empty_repo):
        """
        Check if empty repository is empty.

        Returns True for an empty repository.
        """
        repo_path, _ = empty_repo
        graph = get_git_graph(repo_path)

        assert graph.is_empty() is True

    def test_is_empty_with_commits(self, simple_repo):
        """
        Check if non-empty repository is empty.

        Returns False for a repository with commits.
        """
        repo_path, _ = simple_repo
        graph = get_git_graph(repo_path)

        assert graph.is_empty() is False

    def test_reload_updates_data(self, simple_repo):
        """
        Reload graph data after repository changes.

        Updates graph data to reflect new commits.
        """

        repo_path, commit_ids = simple_repo
        graph = get_git_graph(repo_path)

        initial_commit_count = len(graph.data.commits)

        # Add a new commit directly to the repository
        repo = pygit2.Repository(str(repo_path))
        tree = repo.TreeBuilder().write()
        author = pygit2.Signature("Test", "test@example.com")
        new_commit = repo.create_commit(
            "refs/heads/main",
            author,
            author,
            "New commit",
            tree,
            [commit_ids[0]],
        )

        # Reload the graph
        graph.reload()

        assert len(graph.data.commits) == initial_commit_count + 1
        assert str(new_commit) in graph.data.commits

    def test_reload_rebuilds_helpers(self, simple_repo):
        """
        Reload rebuilds helper indexes.

        Ensures helpers are rebuilt after reload.
        """

        repo_path, commit_ids = simple_repo
        repo = pygit2.Repository(str(repo_path))
        repo.set_head("refs/heads/main")
        graph = get_git_graph(repo_path)

        # Add a new commit
        repo = pygit2.Repository(str(repo_path))
        tree = repo.TreeBuilder().write()
        author = pygit2.Signature("Test", "test@example.com")
        new_commit_id = str(
            repo.create_commit(
                "refs/heads/main",
                author,
                author,
                "New commit",
                tree,
                [commit_ids[0]],
            )
        )

        # Reload
        graph.reload()

        # Verify helpers work with new data
        history = graph.get_linear_history("HEAD")
        assert len(history) == 2
        assert history[0].id == new_commit_id

    def test_graph_with_multiple_branches(self, repo_with_branches):
        """
        Initialize graph with multiple branches.

        Returns a GitGraph with all branches indexed.
        """
        repo_path, commit_ids = repo_with_branches
        graph = get_git_graph(repo_path)

        assert len(graph.data.commits) == 3
        assert len(graph.data.branches) == 2

        # Verify branch lookups work
        main_branches = graph.get_branches_at_commit(commit_ids[1])
        assert len(main_branches) == 1
        assert main_branches[0].name == "refs/heads/main"

        feature_branches = graph.get_branches_at_commit(commit_ids[2])
        assert len(feature_branches) == 1
        assert feature_branches[0].name == "refs/heads/feature"

    def test_graph_with_detached_head(self, repo_detached_head):
        """
        Initialize graph with detached HEAD.

        Returns a GitGraph with detached HEAD state.
        """
        repo_path, commit_ids = repo_detached_head
        graph = get_git_graph(repo_path)

        assert graph.data.head_info.is_detached
        assert graph.data.head_info.target_id == commit_ids[0]

    def test_graph_preserves_commit_metadata(self, repo_different_author_and_commiter):
        """
        Verify graph preserves commit metadata.

        Returns commits with complete author and committer information.
        """
        repo_path, commit_ids = repo_different_author_and_commiter
        graph = get_git_graph(repo_path)

        commit = graph.data.commits[commit_ids[0]]
        assert commit.author.name == "Alice"
        assert commit.committer.name == "Bob"
        assert commit.message == "Initial commit"

    def test_helpers_are_private(self, simple_repo):
        """
        Verify helper attributes are private.

        Ensures helpers are prefixed with underscore.
        """
        repo_path, _ = simple_repo
        graph = get_git_graph(repo_path)

        assert hasattr(graph, "_ref_index")
        assert hasattr(graph, "_history_walker")
        assert hasattr(graph, "_ref_resolver")

    def test_data_is_public(self, simple_repo):
        """
        Verify data attribute is public.

        Ensures direct access to graph data is available.
        """
        repo_path, commit_ids = simple_repo
        graph = get_git_graph(repo_path)

        assert hasattr(graph, "data")
        assert commit_ids[0] in graph.data.commits
        assert "refs/heads/main" in graph.data.branches
