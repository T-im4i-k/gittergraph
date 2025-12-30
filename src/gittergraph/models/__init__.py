# @generated "partially" ChatGPT-4.1: Documentation
"""
Git object data models.

Provides dataclasses for representing core Git objects and metadata, including branches, commits, signatures, and tags. These models are used throughout the project for type-safe access to repository data and for building higher-level features.
"""

from .branch import Branch
from .commit import Commit
from .head import HeadInfo, HeadState
from .signature import Signature
from .tag import AnnotatedTag, LightweightTag
