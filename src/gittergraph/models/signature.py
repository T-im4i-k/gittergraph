# @generated "all" ChatGPT-4.1

"""
Signature model definition.

Defines the Signature dataclass, representing a Git author, committer, or tagger with name, email, timestamp, and timezone offset. Provides conversion to timezone-aware datetime and string formatting.
"""

from dataclasses import dataclass
from datetime import datetime

from gittergraph.utils.time import unix_timestamp_to_datetime


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
