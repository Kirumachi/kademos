"""Pytest fixtures for ASVS Compliance Tools tests."""

import json
from pathlib import Path

import pytest


@pytest.fixture
def sample_requirements_data():
    """Sample ASVS requirements data for testing."""
    return [
        {
            "chapter_id": "V1",
            "chapter_name": "Encoding and Sanitization",
            "section_id": "V1.1",
            "section_name": "Encoding Architecture",
            "req_id": "V1.1.1",
            "req_description": "Test requirement for L1",
            "L": "1",
        },
        {
            "chapter_id": "V1",
            "chapter_name": "Encoding and Sanitization",
            "section_id": "V1.2",
            "section_name": "Injection Prevention",
            "req_id": "V1.2.1",
            "req_description": "Test requirement for L2",
            "L": "2",
        },
        {
            "chapter_id": "V2",
            "chapter_name": "Validation",
            "section_id": "V2.1",
            "section_name": "Input Validation",
            "req_id": "V2.1.1",
            "req_description": "Test requirement for L3",
            "L": "3",
        },
    ]


@pytest.fixture
def sample_json_file(tmp_path, sample_requirements_data):
    """Create a temporary JSON file with sample data."""
    json_path = tmp_path / "requirements.json"
    json_path.write_text(json.dumps(sample_requirements_data), encoding="utf-8")
    return json_path


@pytest.fixture
def invalid_json_file(tmp_path):
    """Create a temporary file with invalid JSON."""
    json_path = tmp_path / "invalid.json"
    json_path.write_text("{ invalid json }", encoding="utf-8")
    return json_path


@pytest.fixture
def project_root():
    """Return the project root directory."""
    return Path(__file__).parent.parent
