# @generated "partially" Claude-Sonnet-4.5: Code
# @generated "partially" ChatGPT-4.1: Documentation
"""
Git graph representation.

Provides the GitGraph class for loading, organizing, and querying git repository data. Includes helper classes for reference resolution, indexing, and history traversal to support efficient lookups and visualization.
"""

from pathlib import Path

from gittergraph.access import GitRepository
from gittergraph.core.graph_data import GitGraphData
from gittergraph.core.history_walker import HistoryWalker
from gittergraph.core.ref_index import RefIndex
from gittergraph.core.ref_resolver import RefResolver
from gittergraph.models import Branch, Commit, Tag


class GitGraph:
    """
    Git graph structure.

    Loads and organizes repository data for efficient access and rendering. Uses helper classes for reference resolution, indexing, and history traversal.
    """

    def __init__(self, repo: GitRepository):
        """
        Initialize graph from repository.

        Loads all commits, branches, tags, and HEAD info, then builds helper indexes for efficient access and visualization.
        """
        self.repo: GitRepository = repo
        self.data: GitGraphData = GitGraphData.load_from(repo)

        # Initialize helpers
        self._ref_index: RefIndex
        self._history_walker: HistoryWalker
        self._ref_resolver: RefResolver
        self._build_helpers()

    @classmethod
    def from_path(cls, path: str | Path) -> "GitGraph":
        """
        Create graph from repository path.

        Opens the repository at the specified path and initializes the graph with its data.
        """
        repo: GitRepository = GitRepository(path)
        return cls(repo)

    @classmethod
    def discover(cls, start_path: str | Path = ".") -> "GitGraph | None":
        """
        Discover and load a git repository from a directory.

        Searches for a repository starting from the given path and moving up the directory tree. Returns None if no repository is found.
        """
        repo: GitRepository | None = GitRepository.discover(start_path)
        return cls(repo) if repo is not None else None

    def get_branches_at_commit(self, commit_id: str) -> list[Branch]:
        """
        Get all branches pointing to a commit.

        Returns an empty list if no branches point to the commit.
        """
        return self._ref_index.get_branches_at_commit(commit_id)

    def get_tags_at_commit(self, commit_id: str) -> list[Tag]:
        """
        Get all tags pointing to a commit.

        Returns an empty list if no tags point to the commit.
        """
        return self._ref_index.get_tags_at_commit(commit_id)

    def get_linear_history(self, start_ref: str = "HEAD") -> list[Commit]:
        """
        Get linear first-parent history from a reference.

        Follows the first parent chain to build linear history for visualization. Returns commits in newest-first order.
        """
        start_id: str | None = self._ref_resolver.resolve(start_ref)
        if start_id is None:
            return []

        return self._history_walker.get_linear_history_from_commit(start_id)

    def reload(self):
        """
        Reload graph data from repository.

        Refreshes all data and rebuilds indexes to reflect external changes in the repository.
        """
        self.repo.reload()

        old_data: GitGraphData = self.data
        self.data = GitGraphData.load_from(self.repo)

        if self.data != old_data:
            # Rebuild helpers with fresh data
            self._build_helpers()

    def _build_helpers(self):
        """
        Build helper indexes with current data.

        Initializes reference index, history walker, and reference resolver using the current graph data.
        """
        self._ref_index = RefIndex(self.data.branches, self.data.tags)
        self._history_walker = HistoryWalker(self.data.commits)
        self._ref_resolver = RefResolver(
            self.data.commits,
            self.data.branches,
            self.data.tags,
            self.data.head_info,
        )

    def is_empty(self) -> bool:
        """
        Check if repository is empty.

        Returns True if the repository is empty, False otherwise.
        """
        return self.repo.is_empty()
