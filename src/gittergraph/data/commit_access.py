# @generated "partially" ChatGPT-4.1: Documentation
"""
Commit access operations.

Provides access layer for retrieving and converting git commit objects.
"""

import pygit2

from gittergraph.data.base_access import BaseAccess
from gittergraph.models import Commit, Signature


class CommitAccess(BaseAccess):
    """
    Access layer for commit operations.

    Provides methods for retrieving and converting git commit objects.
    """

    @staticmethod
    def to_model(commit: pygit2.Commit) -> Commit:
        """
        Convert pygit2.Commit to Commit model.

        Transforms a pygit2.Commit object into a Commit dataclass instance.
        """
        author: Signature = Signature(
            name=commit.author.name,
            email=commit.author.email,
            time=commit.author.time,
            time_offset=commit.author.offset,
        )
        committer: Signature = Signature(
            name=commit.committer.name,
            email=commit.committer.email,
            time=commit.committer.time,
            time_offset=commit.committer.offset,
        )
        return Commit(
            id=str(commit.id),
            message=commit.message.strip(),
            author=author,
            committer=committer,
            parent_ids=[str(p) for p in commit.parent_ids],
        )

    def get(self, commit_id: str) -> Commit:
        """
        Get a commit by its ID.

        Retrieves a commit object by its hash and converts it to the Commit model.
        Raises KeyError if not found, ValueError if not a commit.
        """
        obj: pygit2.Object | None = self._repo.get(commit_id)
        if obj is None:
            raise KeyError(f"Object '{commit_id}' not found")

        if not isinstance(obj, pygit2.Commit):
            raise ValueError(f"Object '{commit_id}' is not a commit")

        return CommitAccess.to_model(obj)

    def get_all(self) -> dict[str, Commit]:
        """
        Get all commits reachable from any reference.

        Walks all references and collects all reachable commits into a dictionary.
        """
        commits: dict[str, Commit] = {}

        for ref in self._repo.references.objects:
            try:
                start_id: str = str(ref.peel(pygit2.Commit).id)

            # Refs that do not point to commits are skipped
            except pygit2.InvalidSpecError:
                pass
            else:
                for commit in self._repo.walk(start_id, pygit2.enums.SortMode.NONE):
                    commit_id: str = str(commit.id)
                    if commit_id not in commits:
                        commits[commit_id] = CommitAccess.to_model(commit)

        return commits
