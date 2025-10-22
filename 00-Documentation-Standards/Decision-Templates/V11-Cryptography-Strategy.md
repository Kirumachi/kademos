# Security Decision: Cryptography Strategy

| | |
| :--- | :--- |
| **Project Name:** | `[Project Name]` |
| **Document Owner:** | `[e.g., Cryptography Lead, Architect]` |
| **Date:** | `YYYY-MM-DD` |
| **Status:** | `Draft | In Review | Approved` |

---

## 1. Applicable ASVS Requirements

This document serves as the central inventory for all cryptographic choices within the application, ensuring that only strong, approved algorithms and secure key management practices are used. It addresses requirements from **ASVS Chapter V11 (Cryptography)**.

* **V11.1.2:** Maintain a cryptographic inventory of all keys, algorithms, and certificates.
* **V11.3.2:** Use only approved ciphers and modes, such as AES with GCM.
* **V11.4.2:** Use an approved, computationally intensive key derivation function for password storage.

---

## 2. Cryptographic Use Cases (V11.1.2)

This table documents the specific algorithms chosen for each cryptographic function in the application.

| Use Case | Algorithm Chosen | Key Length / Parameters | Justification |
| :--- | :--- | :--- | :--- |
| **Password Storage** | `e.g., Argon2id` | `e.g., Memory: 64MiB, Iterations: 3` | Industry best practice, resistant to GPU cracking. |
| **Data-at-Rest Encryption** | `e.g., AES-GCM` | `e.g., 256-bit key` | Authenticated encryption, provides both confidentiality and integrity. |
| **Session Token Signing (JWT)**| `e.g., RS256 (RSA with SHA-256)` | `e.g., 2048-bit key` | Asymmetric signature allows stateless verification without sharing the private key. |
| **Data Integrity** | `e.g., HMAC-SHA256` | `e.g., 256-bit key` | Provides strong message authentication codes to prevent tampering. |
| | | | |

---

## 3. Key Management Strategy

This section describes how cryptographic keys are generated, stored, accessed, and rotated.

* **Key Storage Solution:** `[e.g., Azure Key Vault]`
    * *Description: All cryptographic keys (private keys, symmetric keys, HMAC keys) are stored in and managed by Azure Key Vault. The application authenticates via a Managed Identity to access them.*
* **Key Rotation Policy:** `[e.g., Asymmetric signing keys are rotated annually. Symmetric data encryption keys are rotated on-demand following a security incident or policy update.]`