# @generated "partially" ChatGPT-4.1: Documentation

"""
Commit model definition.

Defines the Commit dataclass, which represents a Git commit's metadata, author/committer information, and parent relationships. Provides properties for short hash, truncated message, and commit type checks.
"""

from dataclasses import dataclass

from gittergraph.models.signature import Signature


@dataclass(slots=True)
class Commit:
    """
    Git commit data.

    Represents commit metadata, author/committer info, and parent relationships.
    """

    id: str
    message: str
    author: Signature
    committer: Signature
    parent_ids: list[str]

    @property
    def short_id(self) -> str:
        """
        Short commit hash.

        Returns the first 7 characters of the commit id.
        """
        return self.id[:7]

    @property
    def short_message(self) -> str:
        """
        Truncated commit message.

        Returns the first line of the commit message, up to 50 characters.
        """
        max_length: int = 50
        first_line: str = self.message.splitlines()[0]
        if len(first_line) <= max_length:
            return first_line

        return first_line[: max_length - 3] + "..."

    @property
    def is_merge(self) -> bool:
        """
        Check if commit is a merge commit.

        Returns True if the commit has more than one parent.
        """
        return len(self.parent_ids) > 1

    @property
    def is_root(self) -> bool:
        """
        Check if commit is a root commit.

        Returns True if the commit has no parents.
        """
        return len(self.parent_ids) == 0

    @property
    def author_is_committer(self) -> bool:
        """
        Check if author and committer are the same.

        Returns True if the author and committer signatures are identical.
        """
        return self.author == self.committer
