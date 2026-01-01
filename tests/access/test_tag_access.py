# tests/access/test_tag_access.py
"""Tests for TagAccess class."""

import pygit2
import pytest

from gittergraph.access.tag_access import TagAccess
from gittergraph.models import Tag


class TestToModel:
    """Tests for to_model method."""

    def test_converts_lightweight_tag(self, repo_with_lightweight_tag):
        """Test converting a lightweight tag to model."""
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
        """Test converting an annotated tag to model."""
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
        """Test that non-tag references raise ValueError."""
        repo_path, repo = empty_repo

        # Create a tree object
        tree_oid = repo.TreeBuilder().write()

        # Create a reference to the tree (not a valid tag)
        repo.create_reference("refs/tags/invalid", tree_oid)

        ref = repo.references["refs/tags/invalid"]
        access = TagAccess(repo_path)

        with pytest.raises(ValueError, match="is not a tag"):
            access.to_model(ref)


class TestGet:
    """Tests for get method."""

    def test_get_existing_lightweight_tag(self, repo_with_lightweight_tag):
        """Test getting an existing lightweight tag."""
        repo_path, commit_ids = repo_with_lightweight_tag
        access = TagAccess(repo_path)

        tag = access.get("refs/tags/v1.0.0")

        assert tag.name == "refs/tags/v1.0.0"
        assert tag.target_id == commit_ids[0]
        assert tag.shorthand == "v1.0.0"

    def test_get_existing_annotated_tag(self, repo_with_annotated_tag):
        """Test getting an existing annotated tag."""
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
        """Test getting tags with various naming conventions."""
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
        """Test that getting non-existent tag raises KeyError."""
        repo_path, _ = simple_repo
        access = TagAccess(repo_path)

        with pytest.raises(KeyError):
            access.get("refs/tags/nonexistent")


class TestGetAll:
    """Tests for get_all method."""

    def test_get_all_single_lightweight_tag(self, repo_with_lightweight_tag):
        """Test get_all with single lightweight tag."""
        repo_path, commit_oids = repo_with_lightweight_tag
        access = TagAccess(repo_path)

        tags = access.get_all()

        assert len(tags) == 1
        assert "refs/tags/v1.0.0" in tags
        assert tags["refs/tags/v1.0.0"].target_id == commit_oids[0]

    def test_get_all_single_annotated_tag(self, repo_with_annotated_tag):
        """Test get_all with single annotated tag."""
        repo_path, commit_oids = repo_with_annotated_tag
        access = TagAccess(repo_path)

        tags = access.get_all()

        assert len(tags) == 1
        assert "refs/tags/v2.0.0" in tags
        assert tags["refs/tags/v2.0.0"].target_id == commit_oids[0]

    def test_get_all_multiple_tags(self, repo_with_multiple_tags):
        """Test get_all with multiple tags."""
        repo_path, commit_oids = repo_with_multiple_tags
        access = TagAccess(repo_path)

        tags = access.get_all()

        assert len(tags) == 3
        assert "refs/tags/v1.0.0" in tags
        assert "refs/tags/v2.0.0" in tags
        assert "refs/tags/latest" in tags

        assert tags["refs/tags/v1.0.0"].target_id == commit_oids[0]
        assert tags["refs/tags/v2.0.0"].target_id == commit_oids[1]
        assert tags["refs/tags/latest"].target_id == commit_oids[1]

    def test_get_all_empty_repo(self, empty_repo):
        """Test get_all with repository without tags."""
        repo_path, _ = empty_repo
        access = TagAccess(repo_path)

        tags = access.get_all()

        assert len(tags) == 0

    def test_get_all_returns_dict_keyed_by_full_name(self, repo_with_multiple_tags):
        """Test that get_all returns dict keyed by full ref names."""
        repo_path, _ = repo_with_multiple_tags
        access = TagAccess(repo_path)

        tags = access.get_all()

        # Keys should be full ref names
        for key, tag in tags.items():
            assert key == tag.name
            assert key.startswith("refs/tags/")

    @pytest.mark.parametrize("tag_count", [1, 5, 10])
    def test_get_all_with_multiple_tags_count(self, tmp_path, tag_count):
        """Test get_all with varying numbers of tags."""
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
    """Tests for Tag model properties via TagAccess."""

    def test_tag_shorthand_property(self, repo_with_lightweight_tag):
        """Test the shorthand property of Tag."""
        repo_path, _ = repo_with_lightweight_tag
        access = TagAccess(repo_path)

        tag = access.get("refs/tags/v1.0.0")

        assert tag.shorthand == "v1.0.0"
        assert tag.name == "refs/tags/v1.0.0"

    def test_tags_on_same_commit(self, tmp_path):
        """Test multiple tags pointing to the same commit."""
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
