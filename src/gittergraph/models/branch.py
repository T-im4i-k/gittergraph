# @generated "partially" ChatGPT-4.1: Documentation

"""
Branch model definition.

Defines the Branch dataclass, representing a Git branch's name, target object, and HEAD status. Provides properties for remote branch detection and shorthand naming.
"""

from dataclasses import dataclass


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
