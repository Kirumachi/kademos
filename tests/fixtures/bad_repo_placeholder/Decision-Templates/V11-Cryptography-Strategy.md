# Security Decision: Cryptography Strategy

| Field | Value |
| :--- | :--- |
| **Project Name:** | `[Project Name]` |
| **Document Owner:** | `[e.g., Cryptography Lead, Architect]` |
| **Date:** | `YYYY-MM-DD` |
| **Status:** | `Draft / In Review / Approved` |

---

## 1. Applicable ASVS Requirements

This document serves as the central inventory for all cryptographic choices
within the application, ensuring that only strong, approved algorithms and
secure key management practices are used. It addresses requirements from
**ASVS Chapter V11 (Cryptography)**.

- **V11.1.2:** Maintain a cryptographic inventory of all keys, algorithms,
  and certificates.
- **V11.3.2:** Use only approved ciphers and modes, such as AES with GCM.
- **V11.4.2:** Use an approved, computationally intensive key derivation
  function for password storage.

---

## 2. Cryptographic Use Cases (V11.1.2)

This table documents the specific algorithms chosen for each cryptographic
function in the application.

| Use Case | Algorithm | Key Length | Justification |
| :--- | :--- | :--- | :--- |
| **Password Storage** | Argon2id | 64MiB mem, 3 iter | GPU-resistant |
| **Data-at-Rest** | AES-GCM | 256-bit key | Authenticated encryption |
| **JWT Signing** | RS256 | 2048-bit key | Asymmetric, stateless verify |
| **Data Integrity** | HMAC-SHA256 | 256-bit key | Strong MAC, tamper-proof |

---

## 3. Key Management Strategy

This section describes how cryptographic keys are generated, stored,
accessed, and rotated.

- **Key Storage Solution:** `[e.g., Azure Key Vault]`
  - Description: All cryptographic keys (private keys, symmetric keys,
    HMAC keys) are stored in and managed by Azure Key Vault. The
    application authenticates via a Managed Identity to access them.
- **Key Rotation Policy:** `[e.g., Annual rotation for asymmetric keys]`
  - Asymmetric signing keys are rotated annually.
  - Symmetric data encryption keys are rotated on-demand following a
    security incident or policy update.
