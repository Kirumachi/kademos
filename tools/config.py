#!/usr/bin/env python3
"""
Kademos — Configuration management.

Stores user configuration in ``~/.config/kademos/config.json``
(or ``$XDG_CONFIG_HOME/kademos/config.json``).

Environment variables override config-file values at runtime:
  KADEMOS_OPENAI_KEY      → openai_api_key
  KADEMOS_ANTHROPIC_KEY   → anthropic_api_key
"""

import json
import os
from pathlib import Path
from typing import Any, Optional


# Valid configuration keys and their descriptions
VALID_KEYS: dict[str, str] = {
    "openai_api_key": "OpenAI API key for AI-powered features",
    "anthropic_api_key": "Anthropic API key for AI-powered features",
    "default_level": "Default ASVS level (1, 2, or 3)",
    "output_format": "Default output format (markdown, json, csv, jira-json)",
}

# Env-var overrides: env-var name → config key
ENV_OVERRIDES: dict[str, str] = {
    "KADEMOS_OPENAI_KEY": "openai_api_key",
    "KADEMOS_ANTHROPIC_KEY": "anthropic_api_key",
}

# Keys whose values should be masked in list output
_SENSITIVE_KEYS = {"openai_api_key", "anthropic_api_key"}

# Validation constraints
_VALID_LEVELS = {"1", "2", "3"}
_VALID_FORMATS = {"markdown", "json", "csv", "jira-json"}


def _config_dir() -> Path:
    """Return the configuration directory, respecting XDG_CONFIG_HOME."""
    xdg = os.environ.get("XDG_CONFIG_HOME")
    if xdg:
        return Path(xdg) / "kademos"
    return Path.home() / ".config" / "kademos"


def _config_path() -> Path:
    """Return the path to the configuration file."""
    return _config_dir() / "config.json"


def _mask_value(value: str) -> str:
    """Mask a sensitive value, showing only the last 4 characters."""
    if len(value) <= 4:
        return "****"
    return "*" * (len(value) - 4) + value[-4:]


def _validate_key(key: str) -> None:
    """Raise ValueError if key is not a valid configuration key."""
    if key not in VALID_KEYS:
        valid = ", ".join(sorted(VALID_KEYS))
        raise ValueError(f"Invalid config key: '{key}'. Valid keys: {valid}")


def _validate_value(key: str, value: str) -> None:
    """Raise ValueError if value is invalid for the given key."""
    if key == "default_level" and value not in _VALID_LEVELS:
        raise ValueError(f"Invalid level: '{value}'. Must be one of: {', '.join(sorted(_VALID_LEVELS))}")
    if key == "output_format" and value not in _VALID_FORMATS:
        raise ValueError(f"Invalid format: '{value}'. Must be one of: {', '.join(sorted(_VALID_FORMATS))}")


class KademosConfig:
    """Manages Kademos configuration stored as JSON on disk."""

    def __init__(self, config_path: Optional[Path] = None):
        self._path = config_path or _config_path()
        self._data: dict[str, str] = {}
        self._load()

    def _load(self) -> None:
        """Load configuration from disk. Creates empty config if missing."""
        if self._path.exists():
            try:
                self._data = json.loads(self._path.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, OSError):
                self._data = {}
        else:
            self._data = {}

    def _save(self) -> None:
        """Persist configuration to disk."""
        self._path.parent.mkdir(parents=True, exist_ok=True)
        self._path.write_text(
            json.dumps(self._data, indent=2) + "\n",
            encoding="utf-8",
        )

    def get(self, key: str) -> Optional[str]:
        """Get a config value by key (file only, no env override)."""
        _validate_key(key)
        return self._data.get(key)

    def get_effective(self, key: str) -> Optional[str]:
        """
        Get the effective value for a key.

        Checks environment variable overrides first, then the config file.
        """
        _validate_key(key)
        # Check env overrides
        for env_var, config_key in ENV_OVERRIDES.items():
            if config_key == key:
                env_val = os.environ.get(env_var)
                if env_val:
                    return env_val
        return self._data.get(key)

    def set(self, key: str, value: str) -> None:
        """Set a config value and persist to disk."""
        _validate_key(key)
        _validate_value(key, value)
        self._data[key] = value
        self._save()

    def list_all(self) -> dict[str, Any]:
        """
        Return all config entries for display.

        Returns a dict of ``{key: {"value": str | None, "source": str, "masked": str | None}}``.
        Sensitive values are masked. Environment overrides are indicated.
        """
        result: dict[str, Any] = {}
        for key, desc in VALID_KEYS.items():
            entry: dict[str, Any] = {"description": desc, "value": None, "source": "not set"}

            # Check env override first
            env_val = None
            for env_var, config_key in ENV_OVERRIDES.items():
                if config_key == key:
                    env_val = os.environ.get(env_var)
                    if env_val:
                        entry["value"] = env_val
                        entry["source"] = f"env ({env_var})"
                    break

            # Fall back to config file
            if entry["value"] is None and key in self._data:
                entry["value"] = self._data[key]
                entry["source"] = "config file"

            # Mask sensitive values
            if entry["value"] and key in _SENSITIVE_KEYS:
                entry["display"] = _mask_value(entry["value"])
            elif entry["value"]:
                entry["display"] = entry["value"]
            else:
                entry["display"] = None

            result[key] = entry
        return result

    def reset(self) -> None:
        """Remove all configuration values and delete the config file."""
        self._data = {}
        if self._path.exists():
            self._path.unlink()
