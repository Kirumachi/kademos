# ASVS Level Definitions for [Your Organization's Name]

This document defines the criteria for applying OWASP ASVS Levels 1, 2,
and 3 to applications within our organization. The appropriate level must
be determined early in the SDLC in consultation with the Application
Security team.

---

## Level 1: Low Assurance

**ASVS Level 1** is the baseline for all applications. It represents the
essential security controls required to defend against common, opportunistic
attacks.

- **Applies To:**
  - All new applications by default.
  - Applications that do not handle sensitive data (as defined by our
    Data Classification Policy).
  - Internal tools with limited access to production systems.
- **Goal:** To be fully automated and penetration testable.

---

## Level 2: Standard Assurance

**ASVS Level 2** is the standard for applications that handle sensitive or
business-critical information. It protects against targeted attacks from
skilled adversaries.

- **Applies To:**
  - Applications that process, store, or transmit **Personally Identifiable
    Information (PII)**, **financial data (PCI)**, or other data classified
    as **Confidential** or **Restricted**.
  - Applications critical to business operations.
  - Internet-facing applications that represent the company brand.
- **Goal:** To ensure that security controls are properly designed,
  implemented, and effective.

---

## Level 3: High Assurance

**ASVS Level 3** is reserved for our most critical applications that require
the highest level of security assurance, typically those managing extreme
risk.

- **Applies To:**
  - Applications managing life-safety functions, high-value financial
    transactions, or highly sensitive intellectual property.
  - Systems that, if compromised, would pose a significant, existential
    threat to the business.
- **Goal:** To be resilient against advanced, determined adversaries and to
  have a modular, well-secured architecture.

---

## Finding Requirements

For each of the levels defined above, this starter kit provides two formats
in the `/01-ASVS-Core-Reference/` directory:

- **Verification Checks:** The original ASVS language ("Verify that..."),
  useful for audit and testing checklists.
- **Functional Requirements:** A developer-friendly translation ("The
  application shall..."), ideal for building security into your application
  from the start.
