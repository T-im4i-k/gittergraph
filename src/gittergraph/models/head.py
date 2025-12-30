# @generated "partially" Claude-Sonnet-4.5: Code
# @generated "partially" ChatGPT-4.1: Documentation
"""
HEAD model definition.

Defines the HeadState enum and HeadInfo dataclass for representing the state of Git HEAD. Used to track whether HEAD is attached to a branch, detached, or unborn, and to provide related metadata.
"""

from dataclasses import dataclass
from enum import Enum


class HeadState(Enum):
    """
    Git HEAD state.

    Represents possible HEAD states: normal (attached to branch), detached (points directly to commit), and unborn (no commits yet).
    """

    NORMAL = "normal"  # HEAD -> branch -> commit
    DETACHED = "detached"  # HEAD -> commit directly
    UNBORN = "unborn"  # New repo, no commits yet


@dataclass(slots=True)
class HeadInfo:
    """
    Information about the current HEAD state.

    Stores HEAD state, target object id, and branch name if available.
    """

    state: HeadState
    target_id: str | None
    branch_name: str | None

    @property
    def is_detached(self) -> bool:
        """
        Check if HEAD is in detached state.

        Returns True if HEAD points directly to a commit, not a branch.
        """

        return self.state == HeadState.DETACHED
