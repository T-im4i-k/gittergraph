# @generated "partially" ChatGPT-4.1: Documentation
"""
Tag access operations.

Provides access layer for retrieving and converting git tag objects.
"""

import pygit2

from gittergraph.access.base_access import BaseAccess
from gittergraph.models import Tag


class TagAccess(BaseAccess):
    """
    Access layer for tag operations.

    Provides methods for retrieving and converting git tag objects.
    """

    def to_model(self, ref: pygit2.Reference) -> Tag:
        """
        Convert a tag reference to a Tag model.

        Transforms a pygit2.Reference object into a Tag dataclass instance.
        Raises KeyError if the reference target is not found, ValueError if not a tag.
        """
        obj: pygit2.Object | None = self._repo.get(ref.target)

        if obj is None:
            raise KeyError(f"Reference '{ref.name}' not found")

        if not isinstance(obj, pygit2.Commit) and not isinstance(obj, pygit2.Tag):
            raise ValueError(f"Reference '{ref.name}' is not a tag")

        target_id: str = str(obj.target) if isinstance(obj, pygit2.Tag) else str(obj.id)
        return Tag(
            target_id=target_id,
            name=ref.name,
        )

    def get_all(self) -> dict[str, Tag]:
        """
        Get all tags that point directly to commits.

        Walks all references and collects all tags into a dictionary mapping full tag names to Tag objects.
        """
        tags: dict[str, Tag] = {}

        for ref in self._repo.references.objects:
            ref_name: str = ref.name
            if ref_name.startswith("refs/tags/"):
                tags[ref_name] = self.to_model(ref)

        return tags

    def get(self, shorthand: str) -> Tag:
        """
        Get a tag by its shorthand name.

        Retrieves a tag object by its shorthand and converts it to the Tag model.
        """
        ref_name: str = f"refs/tags/{shorthand}"
        ref: pygit2.Reference = self._repo.references[ref_name]
        return self.to_model(ref)
