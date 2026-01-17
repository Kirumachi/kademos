#!/usr/bin/env python3
"""ASVS Compliance Gate - Policy validation for security decision documents.

This module validates that required security decision documents exist and
contain actual content (not just placeholder text). It supports OPA-compatible
JSON input/output for integration with Policy-as-Code workflows.

ASVS Requirements addressed:
- V11.1.2: Verify cryptographic inventory is performed.
"""

import argparse
import json
import re
import sys
import yaml
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional, Dict, Any, List


@dataclass
class ValidationResult:
    """Result of a single document validation."""

    document: str
    exists: bool
    has_content: bool
    has_placeholders: bool
    placeholder_matches: list[str] = field(default_factory=list)
    error: Optional[str] = None

    @property
    def is_valid(self) -> bool:
        """Document is valid if it exists, has content, and no placeholders."""
        return self.exists and self.has_content and not self.has_placeholders


@dataclass
class GateResult:
    """Overall result of the compliance gate check."""

    passed: bool
    level: int
    documents_checked: int
    documents_valid: int
    results: list[ValidationResult] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return {
            "passed": self.passed,
            "level": self.level,
            "documents_checked": self.documents_checked,
            "documents_valid": self.documents_valid,
            "results": [
                {
                    "document": r.document,
                    "exists": r.exists,
                    "has_content": r.has_content,
                    "has_placeholders": r.has_placeholders,
                    "placeholder_matches": r.placeholder_matches,
                    "is_valid": r.is_valid,
                    "error": r.error,
                }
                for r in self.results
            ],
            "errors": self.errors,
        }

@dataclass
class EvidenceResult:
    """Result of a single evidence check."""
    requirement_id: str
    check_type: str
    target: str
    passed: bool
    details: str = ""

@dataclass
class GateResult:
    """Overall result of the compliance gate check."""
    passed: bool
    level: int
    documents_checked: int
    documents_valid: int
    # Add evidence fields
    evidence_checked: int = 0
    evidence_passed: int = 0
    document_results: list[ValidationResult] = field(default_factory=list) # Renamed from 'results' for clarity
    evidence_results: list[EvidenceResult] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return {
            "passed": self.passed,
            "level": self.level,
            "documents": {
                "checked": self.documents_checked,
                "valid": self.documents_valid,
                "results": [
                    {
                        "document": r.document,
                        "exists": r.exists,
                        "has_content": r.has_content,
                        "is_valid": r.is_valid,
                        "error": r.error,
                    }
                    for r in self.document_results
                ]
            },
            # Add evidence section to JSON output
            "evidence": {
                "checked": self.evidence_checked,
                "passed": self.evidence_passed,
                "results": [
                    {
                        "requirement": r.requirement_id,
                        "type": r.check_type,
                        "target": r.target,
                        "passed": r.passed,
                        "details": r.details
                    }
                    for r in self.evidence_results
                ]
            },
            "errors": self.errors,
        }

# Default placeholder patterns that indicate unmodified template content
DEFAULT_PLACEHOLDER_PATTERNS = [
    r"\[Project Name\]",
    r"\[e\.g\.,",
    r"YYYY-MM-DD",
    r"`\[.*?\]`",  # Backtick-wrapped placeholders like `[Project Name]`
]

# Required documents by ASVS level
# L1: No mandatory decision documents
# L2+: Cryptography strategy required per V11.1.2
REQUIRED_DOCUMENTS_BY_LEVEL = {
    1: [],
    2: ["V11-Cryptography-Strategy.md"],
    3: ["V11-Cryptography-Strategy.md"],
}

# NEW: Evidence Verifier Class
class EvidenceVerifier:
    """Verifies technical evidence against an evidence manifest."""

    def __init__(self, base_path: Path):
        self.base_path = base_path

    def check_file_exists(self, path_str: str) -> tuple[bool, str]:
        """Check if a file exists relative to the base path."""
        target = self.base_path / path_str
        if target.exists() and target.is_file():
            return True, f"File found: {path_str}"
        return False, f"File not found: {path_str}"

    def check_file_contains(self, path_str: str, pattern: str) -> tuple[bool, str]:
        """Check if a file contains a regex pattern."""
        target = self.base_path / path_str
        if not target.exists():
            return False, f"File not found: {path_str}"
        
        try:
            content = target.read_text(encoding="utf-8")
            if re.search(pattern, content, re.MULTILINE):
                return True, f"Pattern '{pattern}' found in {path_str}"
            return False, f"Pattern '{pattern}' NOT found in {path_str}"
        except Exception as e:
            return False, f"Error reading {path_str}: {str(e)}"

    def verify_requirement(self, req_id: str, checks: List[Dict[str, Any]]) -> List[EvidenceResult]:
        """Run all checks for a specific ASVS requirement."""
        results = []
        for check in checks:
            check_type = check.get("type")
            target = check.get("path")
            
            if check_type == "file_exists":
                passed, details = self.check_file_exists(target)
            elif check_type == "content_match":
                pattern = check.get("pattern", "")
                passed, details = self.check_file_contains(target, pattern)
            else:
                passed, details = False, f"Unknown check type: {check_type}"

            results.append(EvidenceResult(
                requirement_id=req_id,
                check_type=check_type,
                target=target,
                passed=passed,
                details=details
            ))
        return results

# Minimum content length (bytes) to be considered non-empty
MIN_CONTENT_LENGTH = 100


class ComplianceGate:
    """Validates security decision documents against ASVS requirements."""

    def __init__(
        self,
        docs_path: Path,
        level: int = 2,
        placeholder_patterns: Optional[list[str]] = None,
        required_documents: Optional[dict[int, list[str]]] = None,
        min_content_length: int = MIN_CONTENT_LENGTH,
    ):
        """Initialize the compliance gate.

        Args:
            docs_path: Path to the decision templates directory.
            level: ASVS compliance level (1, 2, or 3).
            placeholder_patterns: Regex patterns for placeholder detection.
            required_documents: Dict mapping levels to required document lists.
            min_content_length: Minimum content length to be considered valid.
        """
        self.docs_path = Path(docs_path)
        self.level = level
        self.placeholder_patterns = placeholder_patterns or DEFAULT_PLACEHOLDER_PATTERNS
        self.required_documents = required_documents or REQUIRED_DOCUMENTS_BY_LEVEL
        self.min_content_length = min_content_length
        self._compiled_patterns = [
            re.compile(p, re.IGNORECASE) for p in self.placeholder_patterns
        ]

    def get_required_documents(self) -> list[str]:
        """Get list of required documents for the configured level."""
        required = []
        for lvl in range(1, self.level + 1):
            for doc in self.required_documents.get(lvl, []):
                if doc not in required:
                    required.append(doc)
        return required

    def validate_document(self, doc_name: str) -> ValidationResult:
        """Validate a single document.

        Args:
            doc_name: Name of the document file to validate.

        Returns:
            ValidationResult with validation details.
        """
        doc_path = self.docs_path / doc_name
        result = ValidationResult(
            document=doc_name,
            exists=False,
            has_content=False,
            has_placeholders=False,
        )

        if not doc_path.exists():
            result.error = f"Document not found: {doc_path}"
            return result

        result.exists = True

        try:
            content = doc_path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError) as e:
            result.error = f"Failed to read document: {e}"
            return result

        # Check for minimum content length (non-empty check)
        stripped_content = content.strip()
        if len(stripped_content) < self.min_content_length:
            result.error = (
                f"Document too short ({len(stripped_content)} bytes, "
                f"minimum {self.min_content_length} bytes)"
            )
            return result

        result.has_content = True

        # Check for placeholder patterns
        for pattern in self._compiled_patterns:
            matches = pattern.findall(content)
            if matches:
                result.has_placeholders = True
                result.placeholder_matches.extend(matches)

        if result.has_placeholders:
            result.error = (
                f"Document contains placeholder text: {result.placeholder_matches}"
            )

        return result

    def run(self) -> GateResult:
        """Run the compliance gate validation.

        Returns:
            GateResult with overall pass/fail and individual document results.
        """
        required_docs = self.get_required_documents()
        results: list[ValidationResult] = []
        errors: list[str] = []

        if not self.docs_path.exists():
            return GateResult(
                passed=False,
                level=self.level,
                documents_checked=0,
                documents_valid=0,
                results=[],
                errors=[f"Documents path not found: {self.docs_path}"],
            )

        for doc_name in required_docs:
            result = self.validate_document(doc_name)
            results.append(result)
            if not result.is_valid and result.error:
                errors.append(result.error)

        documents_valid = sum(1 for r in results if r.is_valid)
        passed = documents_valid == len(required_docs)

        return GateResult(
            passed=passed,
            level=self.level,
            documents_checked=len(required_docs),
            documents_valid=documents_valid,
            results=results,
            errors=errors,
        )


def load_policy_config(config_path: Path) -> dict:
    """Load policy configuration from JSON file.

    Args:
        config_path: Path to the policy configuration JSON.

    Returns:
        Configuration dictionary.
    """
    with config_path.open("r", encoding="utf-8") as f:
        return json.load(f)


def main() -> int:
    """Main entry point for CLI usage."""
    parser = argparse.ArgumentParser(
        description="ASVS Compliance Gate - Validate security decision documents",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --docs-path ./Decision-Templates --level 2
  %(prog)s --docs-path ./docs --level 3 --format json
  %(prog)s --config policies/data.json --docs-path ./docs
        """,
    )
    parser.add_argument(
        "--docs-path",
        type=Path,
        required=True,
        help="Path to the decision templates directory",
    )
    parser.add_argument(
        "--level",
        type=int,
        choices=[1, 2, 3],
        default=2,
        help="ASVS compliance level (default: 2)",
    )
    parser.add_argument(
        "--config",
        type=Path,
        help="Path to policy configuration JSON file",
    )
    parser.add_argument(
        "--format",
        choices=["text", "json"],
        default="text",
        help="Output format (default: text)",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Fail on any warning (stricter validation)",
    )
    parser.add_argument(
        "--evidence-manifest",
        type=Path,
        help="Path to evidence.yml configuration file",
    )

    args = parser.parse_args()

    # Load configuration if provided
    placeholder_patterns = None
    required_documents = None
    if args.config and args.config.exists():
        config = load_policy_config(args.config)
        placeholder_patterns = config.get("placeholder_patterns")
        required_documents = {
            int(k): v for k, v in config.get("required_documents", {}).items()
        }

    # Create and run the gate
    gate = ComplianceGate(
        docs_path=args.docs_path,
        level=args.level,
        placeholder_patterns=placeholder_patterns,
        required_documents=required_documents,
    )

    result = gate.run()
    gate_result = gate.run()

    if args.evidence_manifest and args.evidence_manifest.exists():
        try:
            with open(args.evidence_manifest, 'r') as f:
                manifest = yaml.safe_load(f)
            
            verifier = EvidenceVerifier(Path.cwd())
            evidence_results = []
            
            if manifest and "requirements" in manifest:
                for req_id, data in manifest["requirements"].items():
                    checks = data.get("checks", [])
                    evidence_results.extend(verifier.verify_requirement(req_id, checks))
            
            # Update GateResult
            gate_result.evidence_results = evidence_results
            gate_result.evidence_checked = len(evidence_results)
            gate_result.evidence_passed = sum(1 for r in evidence_results if r.passed)
            
            # Fail the gate if evidence fails
            if gate_result.evidence_passed < gate_result.evidence_checked:
                gate_result.passed = False
                
        except Exception as e:
            gate_result.errors.append(f"Evidence verification failed: {str(e)}")
            gate_result.passed = False

    # Output results
    if args.format == "json":
        print(json.dumps(gate_result.to_dict(), indent=2))
    else:
        print(f"ASVS Compliance Gate - Level {result.level}")
        print("=" * 50)
        print(f"Documents checked: {result.documents_checked}")
        print(f"Documents valid: {result.documents_valid}")
        print(f"Status: {'PASSED' if result.passed else 'FAILED'}")
        print()

        for doc_result in result.results:
            status = "✓" if doc_result.is_valid else "✗"
            print(f"  {status} {doc_result.document}")
            if not doc_result.exists:
                print("      - Missing")
            elif not doc_result.has_content:
                print("      - Empty or too short")
            elif doc_result.has_placeholders:
                print(f"      - Contains placeholders: {doc_result.placeholder_matches}")

        if gate_result.evidence_checked > 0:
            print("\nAutomated Evidence Verification")
            print("=" * 30)
            for res in gate_result.evidence_results:
                status = "✓" if res.passed else "✗"
                print(f"  {status} [{res.requirement_id}] {res.check_type}: {res.target}")
                if not res.passed:
                    print(f"      Error: {res.details}")

    return 0 if gate_result.passed else 1

if __name__ == "__main__":
    sys.exit(main())
