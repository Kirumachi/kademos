"""Unit tests for the capability scanner."""

import json
from pathlib import Path

import pytest

from tools.capability_scanner import (
    BASELINE_CHAPTERS,
    CAPABILITY_SIGNATURES,
    ScanResult,
    scan_repo,
)


class TestScanResult:
    """Tests for ScanResult dataclass."""

    def test_defaults(self):
        """ScanResult has expected defaults."""
        r = ScanResult(path=Path("/tmp"))
        assert r.frameworks == []
        assert r.databases == []
        assert r.capabilities == set()
        assert r.chapters == set()


class TestScanRepo:
    """Tests for scan_repo function."""

    def test_empty_dir(self, tmp_path):
        """Empty directory returns baseline chapters only."""
        result = scan_repo(tmp_path)
        assert result.path == tmp_path
        assert set(BASELINE_CHAPTERS) <= result.chapters
        assert result.frameworks == []

    def test_package_json_react(self, tmp_path):
        """package.json with React adds framework."""
        pkg = tmp_path / "package.json"
        pkg.write_text(json.dumps({"dependencies": {"react": "^18.0.0"}}))
        result = scan_repo(tmp_path)
        assert "React" in result.frameworks

    def test_package_json_express(self, tmp_path):
        """package.json with Express adds framework."""
        pkg = tmp_path / "package.json"
        pkg.write_text(json.dumps({"dependencies": {"express": "^4.18.0"}}))
        result = scan_repo(tmp_path)
        assert "Express" in result.frameworks

    def test_package_json_multer_adds_v5(self, tmp_path):
        """package.json with multer detects file upload (V5)."""
        pkg = tmp_path / "package.json"
        pkg.write_text(json.dumps({"dependencies": {"multer": "^1.4.0"}}))
        result = scan_repo(tmp_path)
        assert "V5" in result.chapters
        assert "V5" in result.capabilities

    def test_package_json_socket_io_adds_v17(self, tmp_path):
        """package.json with socket.io detects WebSockets (V17)."""
        pkg = tmp_path / "package.json"
        pkg.write_text(json.dumps({"dependencies": {"socket.io": "^4.0.0"}}))
        result = scan_repo(tmp_path)
        assert "V17" in result.chapters

    def test_requirements_txt_django(self, tmp_path):
        """requirements.txt with Django adds framework."""
        req = tmp_path / "requirements.txt"
        req.write_text("Django>=4.0\n")
        result = scan_repo(tmp_path)
        assert "Django" in result.frameworks

    def test_requirements_txt_bcrypt_adds_v11(self, tmp_path):
        """requirements.txt with bcrypt detects cryptography (V11)."""
        req = tmp_path / "requirements.txt"
        req.write_text("bcrypt>=4.0\n")
        result = scan_repo(tmp_path)
        assert "V11" in result.chapters

    def test_pom_xml_spring(self, tmp_path):
        """pom.xml with spring-boot adds framework."""
        pom = tmp_path / "pom.xml"
        pom.write_text("<project><dependencies><artifactId>spring-boot-starter-web</artifactId></dependencies></project>")
        result = scan_repo(tmp_path)
        assert "Spring" in result.frameworks

    def test_invalid_package_json_ignored(self, tmp_path):
        """Invalid package.json does not crash."""
        pkg = tmp_path / "package.json"
        pkg.write_text("not valid json {")
        result = scan_repo(tmp_path)
        assert result.frameworks == []
