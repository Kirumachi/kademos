# Project Roadmap

This document outlines the high-level goals and future direction for the
ASVS Compliance Starter Kit. Our vision is to make this the most practical,
developer-friendly resource for operationalizing the ASVS.

## Short-Term Goals (v1.1) - COMPLETED

Foundation and automation tooling.

- [x] **Expand Implementation Guidance:** Add more secure coding patterns
  to the `/02-Implementation-Guidance/` directory for common vulnerabilities
  (e.g., Secure Password Storage, Input Validation, Secure File Uploads).
- [x] **Add More Decision Templates:** Create new templates in
  `/00-Documentation-Standards/Decision-Templates/` for other key ASVS
  chapters (e.g., V5 File Handling, V11 Cryptography).
- [x] **Provide Verification Examples:** Populate the
  `/02-Implementation-Guidance/Verification-Tests/` directory with examples
  of how to write unit or integration tests for specific ASVS requirements.
- [x] **Improve Automation Scripts:** Develop simple scripts to help users
  generate checklists from the core JSON/CSV files.
  - `tools/export_requirements.py` - Export requirements to CSV/Jira JSON

## Policy Enforcement (v1.2) - COMPLETED

Policy-as-Code enforcement for security decision documents.

- [x] **Compliance Gate Tool:** Validate that required security decision
  documents exist and contain actual content (not placeholder text).
  - `tools/compliance_gate.py` - CLI tool for policy validation
  - `policies/validate_docs.rego` - OPA Rego policy definitions
- [x] **GitHub Action:** Reusable action for CI/CD integration.
  - `.github/actions/asvs-compliance-gate/action.yml`
- [x] **CI Integration:** Automated compliance checks in CI pipeline.
- [x] **Placeholder Detection:** Detect unmodified template placeholders
  like `[Project Name]`, `YYYY-MM-DD`, `[e.g., ...]`.

## Medium-Term Goals (v1.3)

- [ ] **Language-Specific Guidance:** Create dedicated sections for popular
  languages (e.g., Python, Java, Go, C#) with framework-specific advice.
- [ ] **Integration with Tooling:** Provide examples or scripts for
  integrating the machine-readable ASVS files with common security tools
  (e.g., DAST scanners, SAST linters).
- [ ] **Threat Modeling Content:** Add templates and guidance for conducting
  lightweight threat modeling exercises that map to ASVS controls.

## Long-Term Vision (v2.0 and beyond)

- [ ] **Interactive Tooling:** Explore the possibility of a web-based tool
  that allows users to select their project's ASVS level and generate a
  tailored set of documentation and checklists.
- [ ] **Community Case Studies:** Feature case studies or examples from
  users who have successfully implemented the starter kit in their
  organizations.

Want to help us get there? Check out our [open issues][issues], especially
those tagged `help wanted`!

[issues]: https://github.com/kaademos/asvs-compliance-starter-kit/issues
