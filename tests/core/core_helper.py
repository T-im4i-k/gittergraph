# @generated "all" Claude-Sonnet-4.5

"""
Test helpers for core tests.

Provides utility functions for constructing test objects, such as RefResolver, to simplify and deduplicate test code in the core test suite.
"""


from gittergraph.access import GitRepository
from gittergraph.core.ref_resolver import RefResolver


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
