# @generated "all" Claude-Sonnet-4.5

"""
Test helpers for core tests.

Provides utility functions for constructing test objects, such as RefResolver, to simplify and deduplicate test code in the core test suite.
"""


from gittergraph.access import GitRepository
from gittergraph.core.history_walker import HistoryWalker
from gittergraph.core.ref_index import RefIndex
from gittergraph.core.ref_resolver import RefResolver


def get_history_walker(repo_path: str):
    """
    Create a HistoryWalker for a given repository path.

    Loads all commits from the repository and constructs a HistoryWalker for history traversal tests.
    """
    git_repo = GitRepository(repo_path)
    commits = git_repo.commits.get_all()
    return HistoryWalker(commits)


def get_ref_resolver(
    repo_path: str,
) -> RefResolver:
    """
    Helper to create a RefResolver instance.

    Initializes the RefResolver with commits, branches, tags, and HEAD info from the repository.
    """
    git_repo = GitRepository(repo_path)

    commits = git_repo.commits.get_all()
    branches = git_repo.branches.get_all()
    tags = git_repo.tags.get_all()
    head_info = git_repo.head.get_info()

    resolver = RefResolver(commits, branches, tags, head_info)
    return resolver


def get_ref_index(repo_path: str) -> RefIndex:
    """
    Create a RefIndex for a given repository path.

    Loads branches and tags from the repository and constructs a RefIndex for fast lookups.
    """
    git_repo = GitRepository(repo_path)
    branches = git_repo.branches.get_all()
    tags = git_repo.tags.get_all()
    return RefIndex(branches, tags)
