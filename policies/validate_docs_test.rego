# ASVS Compliance Gate - Document Validation Policy Tests
#
# Run with: opa test policies/ -v

package asvs.compliance_test

import rego.v1

import data.asvs.compliance

# Test: Level 1 has no required documents, always passes
test_level1_always_passes if {
	result := compliance.allow with input as {
		"level": 1,
		"documents": {},
	}
	result == true
}

# Test: Level 2 requires V11 Cryptography Strategy
test_level2_requires_v11 if {
	result := compliance.required_for_level with input as {"level": 2, "documents": {}}
	"V11-Cryptography-Strategy.md" in result
}

# Test: Missing document generates violation
test_missing_document_violation if {
	violations := compliance.violation with input as {
		"level": 2,
		"documents": {},
	}
	count(violations) > 0
	some v in violations
	contains(v, "Missing required document")
}

# Test: Valid document passes
test_valid_document_passes if {
	result := compliance.allow with input as {
		"level": 2,
		"documents": {"V11-Cryptography-Strategy.md": {
			"exists": true,
			"content": "This is a valid cryptography strategy document with enough content to pass the minimum length requirement. It describes our use of AES-256 for encryption.",
			"content_length": 200,
		}},
	}
	result == true
}

# Test: Document with placeholder fails
test_placeholder_document_fails if {
	result := compliance.allow with input as {
		"level": 2,
		"documents": {"V11-Cryptography-Strategy.md": {
			"exists": true,
			"content": "Project: [Project Name] uses encryption. More content here to meet length.",
			"content_length": 200,
		}},
	}
	result == false
}

# Test: Empty document fails
test_empty_document_fails if {
	result := compliance.allow with input as {
		"level": 2,
		"documents": {"V11-Cryptography-Strategy.md": {
			"exists": true,
			"content": "Short",
			"content_length": 5,
		}},
	}
	result == false
}

# Test: Document with YYYY-MM-DD placeholder fails
test_date_placeholder_fails if {
	violations := compliance.violation with input as {
		"level": 2,
		"documents": {"V11-Cryptography-Strategy.md": {
			"exists": true,
			"content": "Date: YYYY-MM-DD - This document needs more content to pass length check.",
			"content_length": 200,
		}},
	}
	count(violations) > 0
}

# Test: Document with [e.g., placeholder fails
test_eg_placeholder_fails if {
	violations := compliance.violation with input as {
		"level": 2,
		"documents": {"V11-Cryptography-Strategy.md": {
			"exists": true,
			"content": "Use [e.g., AES-256] for encryption. More content to meet length requirement.",
			"content_length": 200,
		}},
	}
	count(violations) > 0
}

# Test: Summary contains expected fields
test_summary_structure if {
	s := compliance.summary with input as {
		"level": 2,
		"documents": {},
	}
	s.level == 2
	s.required_documents >= 0
	s.violations_count >= 0
	is_boolean(s.passed)
}

# Test: Level 3 requires same documents as Level 2 (at minimum)
test_level3_includes_v11 if {
	result := compliance.required_for_level with input as {"level": 3, "documents": {}}
	"V11-Cryptography-Strategy.md" in result
}
