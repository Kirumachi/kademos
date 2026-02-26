"""Unit tests for the tools.config module."""

import json
import os
from pathlib import Path
from unittest.mock import patch

import pytest

from tools.config import (
    KademosConfig,
    VALID_KEYS,
    ENV_OVERRIDES,
    _mask_value,
    _validate_key,
    _validate_value,
)


@pytest.fixture
def config_path(tmp_path):
    """Temporary config file path."""
    return tmp_path / "kademos" / "config.json"


@pytest.fixture
def config(config_path):
    """KademosConfig instance using a temporary path."""
    return KademosConfig(config_path=config_path)


class TestMaskValue:
    """Tests for _mask_value."""

    def test_short_value(self):
        """Values <= 4 chars are fully masked."""
        assert _mask_value("abc") == "****"
        assert _mask_value("abcd") == "****"

    def test_long_value(self):
        """Values > 4 chars show only last 4."""
        assert _mask_value("sk-test12345") == "********2345"

    def test_api_key_like(self):
        """Typical API key masking."""
        assert _mask_value("sk-1234567890abcdef").endswith("cdef")


class TestValidateKey:
    """Tests for _validate_key."""

    def test_valid_keys(self):
        """All valid keys pass validation."""
        for key in VALID_KEYS:
            _validate_key(key)  # Should not raise

    def test_invalid_key(self):
        """Invalid key raises ValueError."""
        with pytest.raises(ValueError, match="Invalid config key"):
            _validate_key("not_a_real_key")


class TestValidateValue:
    """Tests for _validate_value."""

    def test_valid_level(self):
        """Valid levels pass."""
        for v in ("1", "2", "3"):
            _validate_value("default_level", v)  # Should not raise

    def test_invalid_level(self):
        """Invalid level raises ValueError."""
        with pytest.raises(ValueError, match="Invalid level"):
            _validate_value("default_level", "4")

    def test_valid_format(self):
        """Valid formats pass."""
        for v in ("markdown", "json", "csv", "jira-json"):
            _validate_value("output_format", v)  # Should not raise

    def test_invalid_format(self):
        """Invalid format raises ValueError."""
        with pytest.raises(ValueError, match="Invalid format"):
            _validate_value("output_format", "xml")


class TestKademosConfig:
    """Tests for KademosConfig class."""

    def test_set_and_get(self, config):
        """Set and get a config value."""
        config.set("default_level", "1")
        assert config.get("default_level") == "1"

    def test_get_unset_key(self, config):
        """Getting an unset key returns None."""
        assert config.get("default_level") is None

    def test_set_creates_file(self, config, config_path):
        """Setting a value creates the config file on disk."""
        assert not config_path.exists()
        config.set("default_level", "2")
        assert config_path.exists()
        data = json.loads(config_path.read_text())
        assert data["default_level"] == "2"

    def test_set_invalid_key(self, config):
        """Setting an invalid key raises ValueError."""
        with pytest.raises(ValueError, match="Invalid config key"):
            config.set("bad_key", "value")

    def test_set_invalid_value(self, config):
        """Setting an invalid value raises ValueError."""
        with pytest.raises(ValueError, match="Invalid level"):
            config.set("default_level", "99")

    def test_set_api_key(self, config):
        """API keys can be set to any value."""
        config.set("openai_api_key", "sk-test123")
        assert config.get("openai_api_key") == "sk-test123"

    def test_persistence(self, config_path):
        """Config persists across instances."""
        c1 = KademosConfig(config_path=config_path)
        c1.set("default_level", "3")

        c2 = KademosConfig(config_path=config_path)
        assert c2.get("default_level") == "3"

    def test_get_effective_config_value(self, config):
        """get_effective returns config file value when no env override."""
        config.set("default_level", "1")
        assert config.get_effective("default_level") == "1"

    def test_get_effective_env_override(self, config):
        """get_effective returns env var value when set."""
        config.set("openai_api_key", "from-config")
        with patch.dict(os.environ, {"KADEMOS_OPENAI_KEY": "from-env"}):
            assert config.get_effective("openai_api_key") == "from-env"

    def test_get_effective_env_not_set(self, config):
        """get_effective falls back to config when env var is empty."""
        config.set("openai_api_key", "from-config")
        # Ensure env var is not set
        with patch.dict(os.environ, {}, clear=True):
            assert config.get_effective("openai_api_key") == "from-config"

    def test_list_all_structure(self, config):
        """list_all returns entries for all valid keys."""
        entries = config.list_all()
        assert set(entries.keys()) == set(VALID_KEYS.keys())
        for key, entry in entries.items():
            assert "description" in entry
            assert "value" in entry
            assert "source" in entry
            assert "display" in entry

    def test_list_all_masking(self, config):
        """list_all masks sensitive values."""
        config.set("openai_api_key", "sk-1234567890abcdef")
        entries = config.list_all()
        entry = entries["openai_api_key"]
        assert entry["display"] != "sk-1234567890abcdef"
        assert entry["display"].endswith("cdef")

    def test_list_all_non_sensitive_not_masked(self, config):
        """list_all does not mask non-sensitive values."""
        config.set("default_level", "2")
        entries = config.list_all()
        assert entries["default_level"]["display"] == "2"

    def test_reset(self, config, config_path):
        """reset clears config and removes file."""
        config.set("default_level", "1")
        assert config_path.exists()

        config.reset()
        assert not config_path.exists()
        assert config.get("default_level") is None

    def test_corrupt_config_file(self, config_path):
        """Corrupt config file does not crash; starts with empty config."""
        config_path.parent.mkdir(parents=True, exist_ok=True)
        config_path.write_text("not valid json {", encoding="utf-8")
        c = KademosConfig(config_path=config_path)
        assert c.get("default_level") is None
