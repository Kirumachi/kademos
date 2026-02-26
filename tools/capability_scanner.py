#!/usr/bin/env python3
"""
Kademos Capability Discovery Engine

Scans package managers (package.json, pom.xml, requirements.txt) to detect
frameworks, databases, and features, then maps them to ASVS chapters.
Per .docs/issues.md: "If the tool detects multer or file upload signatures,
it automatically pulls ASVS Chapter V5 (File Handling). If it doesn't detect
WebSockets, it completely excludes Chapter V17."
"""

import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional


# Capability signatures: (pattern, ASVS chapter_id)
# Pattern matches package names, dependency keys, or file content keywords
CAPABILITY_SIGNATURES = [
    # File upload -> V5
    (r"multer|formidable|express-fileupload|django\.storage|FileField|UploadFile", "V5"),
    (r"file.?upload|upload.?file", "V5"),
    # WebSockets -> V17
    (r"ws|socket\.io|websocket|Socket\.IO", "V17"),
    # Auth (Passport, Auth0, etc.) -> V2
    (r"passport|auth0|okta|keycloak|django\.contrib\.auth|flask-login|PyJWT", "V2"),
    # Session -> V3
    (r"express-session|session|django\.contrib\.sessions|flask.?session", "V3"),
    # Cryptography -> V11
    (r"bcrypt|argon2|cryptography|pyjwt|passlib", "V11"),
    # Database (SQL/NoSQL) -> V6
    (r"pg|postgres|postgresql|mysql|sqlite|mongodb|mongoose|pymongo|django\.db", "V6"),
    # XML parsing -> V1 (injection)
    (r"xml\.etree|lxml|sax|dom\.parse", "V1"),
]

# Always-included baseline chapters (core web security)
BASELINE_CHAPTERS = ["V1", "V2", "V3", "V14"]


@dataclass
class ScanResult:
    """Result of a capability scan."""
    path: Path
    frameworks: list[str] = field(default_factory=list)
    databases: list[str] = field(default_factory=list)
    capabilities: set[str] = field(default_factory=set)
    chapters: set[str] = field(default_factory=set)


def _read_safe(path: Path, encoding: str = "utf-8") -> str:
    """Read file or return empty string on error."""
    try:
        return path.read_text(encoding=encoding)
    except (OSError, UnicodeDecodeError):
        return ""


def _parse_package_json(root: Path) -> Optional[dict]:
    """Parse package.json if it exists."""
    pkg = root / "package.json"
    if not pkg.exists():
        return None
    try:
        return json.loads(pkg.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None


def _parse_pom_xml(root: Path) -> str:
    """Read pom.xml as raw text (simple pattern matching)."""
    pom = root / "pom.xml"
    if not pom.exists():
        return ""
    return _read_safe(pom)


def _parse_requirements_txt(root: Path) -> str:
    """Read requirements.txt."""
    for name in ("requirements.txt", "requirements.in"):
        p = root / name
        if p.exists():
            return _read_safe(p)
    return ""


def scan_repo(repo_path: Path) -> ScanResult:
    """
    Scan repository for capabilities.
    Returns ScanResult with detected frameworks, databases, and ASVS chapters.
    """
    repo_path = Path(repo_path).resolve()
    result = ScanResult(path=repo_path)
    result.chapters.update(BASELINE_CHAPTERS)

    # Collect all searchable content
    content_parts: list[str] = []

    # package.json
    pkg = _parse_package_json(repo_path)
    if pkg:
        deps = {**pkg.get("dependencies", {}), **pkg.get("devDependencies", {})}
        content_parts.append(" ".join(deps.keys()).lower())
        # Framework hints
        if "react" in deps or "next" in deps:
            result.frameworks.append("React")
        if "vue" in deps:
            result.frameworks.append("Vue")
        if "express" in deps:
            result.frameworks.append("Express")
        if "django" in str(pkg).lower():
            result.frameworks.append("Django")

    # pom.xml
    pom_content = _parse_pom_xml(repo_path)
    if pom_content:
        content_parts.append(pom_content.lower())
        if "spring-boot" in pom_content or "springframework" in pom_content:
            result.frameworks.append("Spring")

    # requirements.txt
    req_content = _parse_requirements_txt(repo_path)
    if req_content:
        req_lower = req_content.lower()
        content_parts.append(req_lower)
        if "django" in req_lower:
            result.frameworks.append("Django")
        if "flask" in req_lower:
            result.frameworks.append("Flask")

    combined = " ".join(content_parts)

    # Match capability signatures
    for pattern, chapter in CAPABILITY_SIGNATURES:
        if re.search(pattern, combined, re.IGNORECASE):
            result.capabilities.add(chapter)
            result.chapters.add(chapter)

    return result
