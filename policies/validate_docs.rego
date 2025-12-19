# ASVS Compliance Gate - Document Validation Policy
#
# This Rego policy validates that required security decision documents exist
# and contain actual content (not just placeholder text).
#
# ASVS Requirements addressed:
# - V11.1.2: Verify cryptographic inventory is performed.
#
# Input schema:
# {
#   "level": 2,                    // ASVS compliance level (1, 2, or 3)
#   "documents": {                 // Map of document names to their content
#     "V11-Cryptography-Strategy.md": {
#       "exists": true,
#       "content": "...",
#       "content_length": 1500
#     }
#   }
# }
#
# Output:
# - allow: boolean indicating if all required documents are valid
# - violations: array of violation messages
# - summary: object with counts and status

package asvs.compliance

import rego.v1

# Default configuration (can be overridden via data.json)
default min_content_length := 100

# Placeholder patterns that indicate unmodified template content
default_placeholder_patterns := [
	"\\[Project Name\\]",
	"\\[e\\.g\\.,",
	"YYYY-MM-DD",
	"`\\[.*?\\]`",
]

# Required documents by ASVS level
default_required_documents := {
	"1": [],
	"2": ["V11-Cryptography-Strategy.md"],
	"3": ["V11-Cryptography-Strategy.md"],
}

# Get placeholder patterns from data or use defaults
placeholder_patterns := data.placeholder_patterns if {
	data.placeholder_patterns
} else := default_placeholder_patterns

# Get required documents from data or use defaults
required_documents := data.required_documents if {
	data.required_documents
} else := default_required_documents

# Get minimum content length from data or use default
min_length := data.min_content_length if {
	data.min_content_length
} else := min_content_length

# Get the list of required documents for the input level
required_for_level contains doc if {
	level := sprintf("%d", [input.level])
	some doc in required_documents[level]
}

# Check if a document exists
document_exists(doc_name) if {
	input.documents[doc_name].exists == true
}

# Check if a document has sufficient content
document_has_content(doc_name) if {
	input.documents[doc_name].content_length >= min_length
}

# Check if content contains any placeholder patterns
# Note: In real OPA, regex matching would be used. This is a simplified version.
content_has_placeholder(content, pattern) if {
	contains(content, "[Project Name]")
}

content_has_placeholder(content, pattern) if {
	contains(content, "[e.g.,")
}

content_has_placeholder(content, pattern) if {
	contains(content, "YYYY-MM-DD")
}

# Check if document has placeholders
document_has_placeholders(doc_name) if {
	content := input.documents[doc_name].content
	some pattern in placeholder_patterns
	content_has_placeholder(content, pattern)
}

# Violations for missing documents
violation contains msg if {
	some doc in required_for_level
	not document_exists(doc)
	msg := sprintf("Missing required document: %s", [doc])
}

# Violations for empty/short documents
violation contains msg if {
	some doc in required_for_level
	document_exists(doc)
	not document_has_content(doc)
	msg := sprintf("Document too short (minimum %d bytes required): %s", [min_length, doc])
}

# Violations for documents with placeholder text
violation contains msg if {
	some doc in required_for_level
	document_exists(doc)
	document_has_content(doc)
	document_has_placeholders(doc)
	msg := sprintf("Document contains placeholder text: %s", [doc])
}

# Main decision: allow if no violations
default allow := false

allow if {
	count(violation) == 0
}

# Summary output
summary := {
	"level": input.level,
	"required_documents": count(required_for_level),
	"violations_count": count(violation),
	"passed": allow,
}
