# Security Decision: Authentication Strategy

| Field | Value |
| :--- | :--- |
| **Project Name:** | `[Project Name]` |
| **Document Owner:** | `[e.g., Lead Engineer, Architect]` |
| **Date:** | `YYYY-MM-DD` |
| **Status:** | `Draft / In Review / Approved` |

---

## 1. Applicable ASVS Requirements

This document addresses the high-level design decisions for the following
ASVS 5.0 requirements:

- **V6.1.1:** Document the application's authentication, session management,
  and access control design.
- **V6.1.2:** Document the supported identity verification methods.
- **V6.1.3:** Document all supported authentication factors.

---

## 2. Supported Authentication Factors

Describe all methods a user can use to authenticate.

- [ ] **Passwords / Passphrases:**
  - If checked, the password policy defined in the V2 Authentication
    decision template must be followed.
- [ ] **MFA - One-Time Passwords (OTP):**
  - Method: (e.g., TOTP via Authenticator App, SMS/Email OTP)
  - Justification:
- [ ] **MFA - Cryptographic Device:**
  - Method: (e.g., FIDO2/WebAuthn, Hardware Tokens)
  - Justification:
- [ ] **Single Sign-On (SSO):**
  - Provider: (e.g., Okta, Azure AD, Google Identity)
  - Protocol: (e.g., SAML 2.0, OpenID Connect)
- [ ] **Other (Please Specify):**

---

## 3. Session Management Strategy

Describe the high-level session management design.

- **Session Token Type:** `(e.g., Stateful session identifiers, JWTs)`
- **Token Storage:** `(e.g., Secure, HttpOnly, SameSite cookies; In-memory)`
- **Session Timeout Policy:**
  - Idle Timeout: `(e.g., 15 minutes)`
  - Absolute Timeout: `(e.g., 8 hours)`

---

## 4. Key Decisions & Justifications

Record any significant design choices, trade-offs, or accepted risks here.

- **Decision:**
- **Justification:**
