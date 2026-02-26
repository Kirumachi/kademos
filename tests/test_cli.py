"""Unit tests for the Kademos CLI."""

import json
from pathlib import Path
from unittest.mock import patch

import pytest

from tools.cli import (
    create_parser,
    get_version,
    main,
    show_splash,
)


class TestCreateParser:
    """Tests for create_parser."""

    def test_has_subcommands(self):
        """Parser has required subcommands."""
        parser = create_parser()
        action = [a for a in parser._subparsers._group_actions if hasattr(a, "choices")][0]
        choices = list(action.choices.keys())
        assert "scan" in choices
        assert "interact" in choices
        assert "threatmodel" in choices
        assert "export" in choices
        assert "resources" in choices
        assert "config" in choices

    def test_scan_defaults(self):
        """Scan subcommand has correct defaults."""
        parser = create_parser()
        parsed = parser.parse_args(["scan", "."])
        assert parsed.command == "scan"
        assert parsed.path == "."
        assert parsed.level == "2"
        assert parsed.format == "markdown"
        assert parsed.ai_context is False

    def test_scan_ai_context(self):
        """Scan --ai-context flag."""
        parser = create_parser()
        parsed = parser.parse_args(["scan", "/repo", "--ai-context"])
        assert parsed.ai_context is True

    def test_config_set_args(self):
        """Config set subcommand parses key and value."""
        parser = create_parser()
        parsed = parser.parse_args(["config", "set", "default_level", "1"])
        assert parsed.command == "config"
        assert parsed.config_action == "set"
        assert parsed.key == "default_level"
        assert parsed.value == "1"

    def test_config_get_args(self):
        """Config get subcommand parses key."""
        parser = create_parser()
        parsed = parser.parse_args(["config", "get", "default_level"])
        assert parsed.command == "config"
        assert parsed.config_action == "get"
        assert parsed.key == "default_level"

    def test_config_list_args(self):
        """Config list subcommand."""
        parser = create_parser()
        parsed = parser.parse_args(["config", "list"])
        assert parsed.command == "config"
        assert parsed.config_action == "list"

    def test_config_reset_args(self):
        """Config reset subcommand."""
        parser = create_parser()
        parsed = parser.parse_args(["config", "reset"])
        assert parsed.command == "config"
        assert parsed.config_action == "reset"


class TestMain:
    """Tests for main entrypoint."""

    def test_no_args_returns_zero(self):
        """main() with no command returns 0 (splash)."""
        assert main([]) == 0

    def test_version(self):
        """--version prints and exits."""
        parser = create_parser()
        with pytest.raises(SystemExit) as exc:
            parser.parse_args(["--version"])
        assert exc.value.code == 0

    def test_scan_runs(self, project_root):
        """kademos scan . runs successfully with repo."""
        result = main(["scan", str(project_root), "--format", "json"])
        assert result == 0

    def test_scan_nonexistent_path(self):
        """kademos scan on nonexistent path returns 1."""
        result = main(["scan", "/nonexistent/path/xyz"])
        assert result == 1

    def test_scan_without_base_path(self, project_root):
        """kademos scan works without --base-path (uses bundled data)."""
        result = main(["scan", str(project_root), "--format", "json"])
        assert result == 0

    def test_export_runs(self, project_root):
        """kademos export delegates to export_requirements."""
        result = main(["export", "--level", "1", "--format", "csv", "--base-path", str(project_root)])
        assert result == 0

    def test_resources_list(self):
        """kademos resources lists JSON files (from bundled data)."""
        result = main(["resources"])
        assert result == 0

    def test_resources_drift_offline(self, project_root):
        """kademos resources --drift --offline runs."""
        result = main(["resources", "--drift", "--offline", "--base-path", str(project_root)])
        assert result in (0, 1)  # 1 if drift detected

    def test_config_runs(self):
        """kademos config runs without error."""
        assert main(["config"]) == 0

    def test_config_set_and_get(self, tmp_path):
        """kademos config set + get roundtrip."""
        config_path = tmp_path / "kademos" / "config.json"
        with patch("tools.config._config_path", return_value=config_path):
            assert main(["config", "set", "default_level", "1"]) == 0
            assert main(["config", "get", "default_level"]) == 0

    def test_config_list(self, tmp_path):
        """kademos config list shows table."""
        config_path = tmp_path / "kademos" / "config.json"
        with patch("tools.config._config_path", return_value=config_path):
            assert main(["config", "list"]) == 0

    def test_config_reset(self, tmp_path):
        """kademos config reset clears config."""
        config_path = tmp_path / "kademos" / "config.json"
        with patch("tools.config._config_path", return_value=config_path):
            main(["config", "set", "default_level", "1"])
            assert main(["config", "reset"]) == 0

    def test_config_set_invalid_key(self):
        """kademos config set with invalid key returns 1."""
        assert main(["config", "set", "bad_key", "value"]) == 1

    def test_threatmodel_creates_file(self, tmp_path):
        """kademos threatmodel creates output file."""
        out = tmp_path / "prompt.txt"
        result = main(["threatmodel", "--output", str(out)])
        assert result == 0
        assert out.exists()
        assert "STRIDE" in out.read_text()


class TestShowSplash:
    """Tests for splash screen."""

    def test_splash_runs(self):
        """show_splash works with Rich."""
        show_splash("3.0.0")  # Should not raise


@pytest.fixture
def project_root():
    """Project root with ASVS reference files."""
    return Path(__file__).parent.parent
