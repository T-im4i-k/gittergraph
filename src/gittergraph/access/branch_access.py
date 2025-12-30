# @generated "partially" Claude-Sonnet-4.5: Code
# @generated "partially" ChatGPT-4.1: Documentation
"""
Branch access operations.

Provides methods for retrieving and converting Git branch objects. Used to access local and remote branches and convert pygit2 branch objects to project models.
"""

import pygit2

from gittergraph.access.base_access import BaseAccess
from gittergraph.models import Branch


class BranchAccess(BaseAccess):
    """
    Branch access layer.

    Methods for retrieving and converting Git branch objects from the repository.
    """

    @staticmethod
    def to_model(branch: pygit2.Branch) -> Branch:
        """
        Convert pygit2.Branch to Branch model.

        Returns a Branch model instance for the given pygit2 branch.
        """
        return Branch(
            target_id=str(branch.target),
            name=branch.name,
        )

    def get_all(self) -> dict[str, Branch]:
        """
        Get all branches (local and remote).

        Returns a dictionary of Branch objects for all branches in the repository.
        """
        branches: dict[str, Branch] = {}

        for shorthand in self._repo.branches:
            branch: Branch = self.get(shorthand)
            branches[branch.name] = branch

        return branches

    def get(self, shorthand: str) -> Branch:
        """
        Get a specific branch by name.

        Returns a Branch model for the given branch shorthand name.
        """
        return BranchAccess.to_model(self._repo.branches[shorthand])
