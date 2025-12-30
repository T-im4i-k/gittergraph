# @generated "partially" ChatGPT-4.1: Documentation
"""
Tag model definition.

Defines the Tag, LightweightTag, and AnnotatedTag dataclasses, representing Git tags and their metadata. Provides properties for tag name normalization and storage of tagger information for annotated tags.
"""

from dataclasses import dataclass


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
