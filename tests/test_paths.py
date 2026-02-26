"""Unit tests for the tools.paths module."""

from pathlib import Path

import pytest

from tools.paths import get_source_file, _bundled_data_dir, LEVEL_FILES


class TestBundledDataDir:
    """Tests for bundled data directory resolution."""

    def test_bundled_dir_exists(self):
        """Bundled data directory exists and contains JSON files."""
        d = _bundled_data_dir()
        assert d.exists()
        assert d.is_dir()

    def test_bundled_dir_has_json_files(self):
        """Bundled data directory contains the expected JSON files."""
        d = _bundled_data_dir()
        for filename in LEVEL_FILES.values():
            assert (d / filename).exists(), f"Missing bundled file: {filename}"


class TestGetSourceFile:
    """Tests for get_source_file resolution."""

    def test_bundled_l1(self):
        """Level 1 resolves to bundled ASVS-L1-Baseline.json."""
        p = get_source_file("1")
        assert p.name == "ASVS-L1-Baseline.json"
        assert p.exists()

    def test_bundled_l2(self):
        """Level 2 resolves to bundled ASVS-L2-Standard.json."""
        p = get_source_file("2")
        assert p.name == "ASVS-L2-Standard.json"
        assert p.exists()

    def test_bundled_l3(self):
        """Level 3 resolves to bundled ASVS-5.0-en.json."""
        p = get_source_file("3")
        assert p.name == "ASVS-5.0-en.json"
        assert p.exists()

    def test_base_path_override(self, project_root):
        """Custom base_path resolves under 01-ASVS-Core-Reference."""
        p = get_source_file("2", base_path=project_root)
        assert p.name == "ASVS-L2-Standard.json"
        assert "01-ASVS-Core-Reference" in str(p)
        assert p.exists()

    def test_invalid_level(self):
        """Invalid level raises ValueError."""
        with pytest.raises(ValueError, match="Invalid level"):
            get_source_file("4")

    def test_missing_file_with_base_path(self, tmp_path):
        """Non-existent base_path raises FileNotFoundError."""
        with pytest.raises(FileNotFoundError, match="Source file not found"):
            get_source_file("1", base_path=tmp_path)


@pytest.fixture
def project_root():
    """Project root with ASVS reference files."""
    return Path(__file__).parent.parent
