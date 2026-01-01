# @generated "partially" Claude-Sonnet-4.5: Code
# @generated "partially" ChatGPT-4.1: Documentation
"""
TagAccess tests.

Unit tests for the TagAccess class, covering tag lookup, retrieval, and edge cases for various repository structures.
"""

import pygit2
import pytest

from gittergraph.access.tag_access import TagAccess
from gittergraph.models import Tag


class TestToModel:
    """
    Tests for to_model method.

    Covers conversion of repository tag references to Tag model objects.
    """

    def test_converts_lightweight_tag(self, repo_with_lightweight_tag):
        """
        Convert a lightweight tag to model.

        Returns a Tag object for a lightweight tag reference.
        """
        repo_path, commit_ids = repo_with_lightweight_tag
        repo = pygit2.Repository(str(repo_path))

        ref = repo.references["refs/tags/v1.0.0"]
        access = TagAccess(repo_path)
        tag = access.to_model(ref)

        assert isinstance(tag, Tag)
        assert tag.name == "refs/tags/v1.0.0"
        assert tag.target_id == commit_ids[0]
        assert tag.shorthand == "v1.0.0"

    def test_converts_annotated_tag(self, repo_with_annotated_tag):
        """
        Convert an annotated tag to model.

        Returns a Tag object for an annotated tag reference.
        """
        repo_path, commit_ids = repo_with_annotated_tag
        repo = pygit2.Repository(str(repo_path))

        ref = repo.references["refs/tags/v2.0.0"]
        access = TagAccess(repo_path)
        tag = access.to_model(ref)

        assert isinstance(tag, Tag)
        assert tag.name == "refs/tags/v2.0.0"
        assert tag.target_id == commit_ids[0]
        assert tag.shorthand == "v2.0.0"

    def test_raises_valueerror_for_non_tag_reference(self, empty_repo):
        """
        Raise ValueError for non-tag reference.

        Ensures ValueError is raised when converting a non-tag reference.
        """
        repo_path, repo = empty_repo

        # Create a tree object
        tree_id = repo.TreeBuilder().write()

        # Create a reference to the tree (not a valid tag)
        repo.create_reference("refs/tags/invalid", tree_id)

        ref = repo.references["refs/tags/invalid"]
        access = TagAccess(repo_path)

        with pytest.raises(ValueError, match="is not a tag"):
            access.to_model(ref)


class TestGet:
    """
    Tests for get method.

    Covers retrieval of tags by full reference name.
    """

    def test_get_existing_lightweight_tag(self, repo_with_lightweight_tag):
        """
        Get an existing lightweight tag.

        Returns the Tag object for the given lightweight tag reference.
        """
        repo_path, commit_ids = repo_with_lightweight_tag
        access = TagAccess(repo_path)

        tag = access.get("refs/tags/v1.0.0")

        assert tag.name == "refs/tags/v1.0.0"
        assert tag.target_id == commit_ids[0]
        assert tag.shorthand == "v1.0.0"

    def test_get_existing_annotated_tag(self, repo_with_annotated_tag):
        """
        Get an existing annotated tag.

        Returns the Tag object for the given annotated tag reference.
        """
        repo_path, commit_ids = repo_with_annotated_tag
        access = TagAccess(repo_path)

        tag = access.get("refs/tags/v2.0.0")

        assert tag.name == "refs/tags/v2.0.0"
        assert tag.target_id == commit_ids[0]
        assert tag.shorthand == "v2.0.0"

    @pytest.mark.parametrize(
        "tag_name",
        [
            "v1.0.0",
            "v2.0.0-beta",
            "release-2024",
            "stable",
        ],
    )
    def test_get_various_tag_names(self, tmp_path, tag_name):
        """
        Get tags with various naming conventions.

        Returns Tag objects for tags with different naming patterns.
        """
        repo_path = tmp_path / "test_repo"
        repo = pygit2.init_repository(str(repo_path))

        tree = repo.TreeBuilder().write()
        author = pygit2.Signature("Test", "test@example.com")
        id_ = repo.create_commit("refs/heads/main", author, author, "Commit", tree, [])

        repo.create_reference(f"refs/tags/{tag_name}", id_)

        access = TagAccess(repo_path)
        tag = access.get(f"refs/tags/{tag_name}")

        assert tag.name == f"refs/tags/{tag_name}"
        assert tag.shorthand == tag_name
        assert tag.target_id == str(id_)

    def test_get_nonexistent_tag_raises_keyerror(self, simple_repo):
        """
        Get a non-existent tag.

        Ensures KeyError is raised for a tag reference that does not exist.
        """
        repo_path, _ = simple_repo
        access = TagAccess(repo_path)

        with pytest.raises(KeyError):
            access.get("refs/tags/nonexistent")


class TestGetAll:
    """
    Tests for get_all method.

    Covers retrieval of all tags in the repository.
    """

    def test_get_all_single_lightweight_tag(self, repo_with_lightweight_tag):
        """
        Get all tags with a single lightweight tag.

        Returns a dictionary with one lightweight tag.
        """
        repo_path, commit_ids = repo_with_lightweight_tag
        access = TagAccess(repo_path)

        tags = access.get_all()

        assert len(tags) == 1
        assert "refs/tags/v1.0.0" in tags
        assert tags["refs/tags/v1.0.0"].target_id == commit_ids[0]

    def test_get_all_single_annotated_tag(self, repo_with_annotated_tag):
        """
        Get all tags with a single annotated tag.

        Returns a dictionary with one annotated tag.
        """
        repo_path, commit_ids = repo_with_annotated_tag
        access = TagAccess(repo_path)

        tags = access.get_all()

        assert len(tags) == 1
        assert "refs/tags/v2.0.0" in tags
        assert tags["refs/tags/v2.0.0"].target_id == commit_ids[0]

    def test_get_all_multiple_tags(self, repo_with_multiple_tags):
        """
        Get all tags with multiple tags present.

        Returns a dictionary with all tag references.
        """
        repo_path, commit_ids = repo_with_multiple_tags
        access = TagAccess(repo_path)

        tags = access.get_all()

        assert len(tags) == 3
        assert "refs/tags/v1.0.0" in tags
        assert "refs/tags/v2.0.0" in tags
        assert "refs/tags/latest" in tags

        assert tags["refs/tags/v1.0.0"].target_id == commit_ids[0]
        assert tags["refs/tags/v2.0.0"].target_id == commit_ids[1]
        assert tags["refs/tags/latest"].target_id == commit_ids[1]

    def test_get_all_empty_repo(self, empty_repo):
        """
        Get all tags in an empty repository.

        Returns an empty dictionary when no tags exist.
        """
        repo_path, _ = empty_repo
        access = TagAccess(repo_path)

        tags = access.get_all()

        assert len(tags) == 0

    def test_get_all_returns_dict_keyed_by_full_name(self, repo_with_multiple_tags):
        """
        Get all tags and verify dictionary keys.

        Returns a dictionary keyed by full tag reference names.
        """
        repo_path, _ = repo_with_multiple_tags
        access = TagAccess(repo_path)

        tags = access.get_all()

        # Keys should be full ref names
        for key, tag in tags.items():
            assert key == tag.name
            assert key.startswith("refs/tags/")

    @pytest.mark.parametrize("tag_count", [1, 5, 10])
    def test_get_all_with_multiple_tags_count(self, tmp_path, tag_count):
        """
        Get all tags with varying numbers of tags.

        Returns a dictionary with the expected number of tags.
        """
        repo_path = tmp_path / "test_repo"
        repo = pygit2.init_repository(str(repo_path))

        tree = repo.TreeBuilder().write()
        author = pygit2.Signature("Test", "test@example.com")
        id_ = repo.create_commit("refs/heads/main", author, author, "Commit", tree, [])

        for i in range(tag_count):
            repo.create_reference(f"refs/tags/v{i}.0.0", id_)

        access = TagAccess(repo_path)
        tags = access.get_all()

        assert len(tags) == tag_count


class TestTagProperties:
    """
    Tests for Tag model properties via TagAccess.

    Covers shorthand property and multiple tags on the same commit.
    """

    def test_tag_shorthand_property(self, repo_with_lightweight_tag):
        """
        Test the shorthand property of Tag.

        Returns the shorthand for a lightweight tag.
        """
        repo_path, _ = repo_with_lightweight_tag
        access = TagAccess(repo_path)

        tag = access.get("refs/tags/v1.0.0")

        assert tag.shorthand == "v1.0.0"
        assert tag.name == "refs/tags/v1.0.0"

    def test_tags_on_same_commit(self, tmp_path):
        """
        Test multiple tags pointing to the same commit.

        Returns all tags that reference the same commit.
        """
        repo_path = tmp_path / "test_repo"
        repo = pygit2.init_repository(str(repo_path))

        tree = repo.TreeBuilder().write()
        author = pygit2.Signature("Test", "test@example.com")
        id_ = repo.create_commit("refs/heads/main", author, author, "Commit", tree, [])

        # Create multiple tags on same commit
        repo.create_reference("refs/tags/v1.0.0", id_)
        repo.create_reference("refs/tags/stable", id_)
        repo.create_reference("refs/tags/latest", id_)

        access = TagAccess(repo_path)
        tags = access.get_all()

        assert len(tags) == 3
        # All should point to same commit
        target_ids = [tag.target_id for tag in tags.values()]
        assert all(tid == str(id_) for tid in target_ids)
