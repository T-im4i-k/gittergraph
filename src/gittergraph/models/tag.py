"""
Tag model definition.

Defines the Tag, LightweightTag, and AnnotatedTag dataclasses, representing Git tags and their metadata. Provides properties for tag name normalization and storage of tagger information for annotated tags.
"""

# @generated "partially" ChatGPT-4.1: Documentation

from dataclasses import dataclass

from gittergraph.models.signature import Signature


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
