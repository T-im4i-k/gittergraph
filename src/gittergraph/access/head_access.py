# @generated "all" Claude-Sonnet-4.5
"""
HEAD access operations.

Provides access layer for retrieving git HEAD state and information.
"""

import pygit2

from gittergraph.access.base_access import BaseAccess
from gittergraph.models.head import HeadInfo, HeadState


class HeadAccess(BaseAccess):  # pylint: disable=too-few-public-methods
    """
    Access layer for HEAD operations.

    Provides methods for retrieving HEAD state and target commit.
    """

    def get_info(self) -> HeadInfo:
        """
        Get information about the current HEAD state.

        Returns HeadInfo describing whether HEAD is normal, detached, or unborn.
        """
        if self._repo.head_is_unborn:
            return HeadInfo(state=HeadState.UNBORN, target_id=None, branch_name=None)

        commit: pygit2.Commit = self._repo.head.peel(pygit2.Commit)
        if self._repo.head_is_detached:
            return HeadInfo(
                state=HeadState.DETACHED,
                target_id=str(commit.id),
                branch_name=None,
            )

        # Normal state - HEAD points to a branch
        branch_name: str = self._repo.head.name
        return HeadInfo(
            state=HeadState.NORMAL,
            target_id=str(commit.id),
            branch_name=branch_name,
        )
