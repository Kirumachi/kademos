#!/usr/bin/env python3
"""
Kademos — Shared ASVS data-file resolution.

Single source of truth for locating ASVS JSON reference files.
Resolves bundled package data first, with optional base-path override.
"""

import importlib.resources
from pathlib import Path
from typing import Optional


# Level → filename mapping (shared by all consumers)
LEVEL_FILES = {
    "1": "ASVS-L1-Baseline.json",
    "2": "ASVS-L2-Standard.json",
    "3": "ASVS-5.0-en.json",
}


def _bundled_data_dir() -> Path:
    """Return the path to the bundled data directory inside the package."""
    ref = importlib.resources.files("tools.data")
    # importlib.resources.files() returns a Traversable; for on-disk
    # packages this is a PosixPath already.
    return Path(str(ref))


def get_source_file(level: str, base_path: Optional[Path] = None) -> Path:
    """
    Resolve the ASVS JSON file for the given level.

    Resolution order:
      1. If *base_path* is provided, look under
         ``base_path / 01-ASVS-Core-Reference / <filename>``.
      2. Otherwise fall back to the bundled ``tools/data/<filename>``.

    Args:
        level: ASVS level — must be ``"1"``, ``"2"``, or ``"3"``.
        base_path: Optional explicit base directory (repo root or custom).

    Returns:
        Resolved :class:`~pathlib.Path` to the JSON file.

    Raises:
        ValueError: If *level* is not ``1``, ``2``, or ``3``.
        FileNotFoundError: If the resolved file does not exist.
    """
    if level not in LEVEL_FILES:
        raise ValueError(f"Invalid level: {level}. Must be 1, 2, or 3")

    filename = LEVEL_FILES[level]

    if base_path is not None:
        p = Path(base_path).resolve() / "01-ASVS-Core-Reference" / filename
    else:
        p = _bundled_data_dir() / filename

    if not p.exists():
        raise FileNotFoundError(f"Source file not found: {p}")

    return p
