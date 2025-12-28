# @generated "partially" ChatGPT-4.1: Documentation
"""
Data models for git objects.

Provides classes for representing signatures, commits, tags, and branches.
"""

from dataclasses import dataclass
from datetime import datetime
from gittergraph.utils.time import unix_timestamp_to_datetime


# @generated "all" ChatGPT-4.1
@dataclass(slots=True)
class Signature:
    """
    Git signature data.

    Represents an author, committer, or tagger with name, email, timestamp, and timezone offset.
    """

    name: str
    email: str
    time: int
    time_offset: int

    @property
    def datetime(self) -> datetime:
        """
        Convert to timezone-aware datetime.

        Returns a datetime object using the stored timestamp and offset.
        """
        return unix_timestamp_to_datetime(self.time, self.time_offset)

    def __str__(self) -> str:
        """
        Format as a git signature string.

        Returns the name and email in standard git format.
        """
        return f"{self.name} <{self.email}>"


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


@dataclass(slots=True)
class Tag:
    """
    Git tag data.

    Represents a tag name and the object it points to.
    """

    target_id: str
    name: str

    @property
    def shorthand(self) -> str:
        """
        Shorthand tag name.

        Returns the tag name without the refs prefix.
        """
        return self.name.removeprefix("refs/tags/")


@dataclass(slots=True)
class LightweightTag(Tag):
    """
    Lightweight git tag.

    Inherits from Tag and does not add extra fields.
    """


@dataclass(slots=True)
class AnnotatedTag(Tag):
    """
    Annotated git tag data.

    Stores tag metadata, message, and tagger info.
    """

    tag_id: str
    message: str
    tagger: Signature


@dataclass(slots=True)
class Branch:
    """
    Git branch data.

    Represents a branch name, the object it points to, and HEAD status.
    """

    target_id: str
    name: str
    is_head: bool

    @property
    def is_remote(self) -> bool:
        """
        Check if branch is remote.

        Returns True if the branch name indicates a remote branch.
        """
        return self.name.startswith("refs/remotes/")

    @property
    def shorthand(self) -> str:
        """
        Shorthand branch name.

        Returns the branch name without the refs prefix.
        """
        if self.is_remote:
            return self.name.removeprefix("refs/remotes/")
        return self.name.removeprefix("refs/heads/")
