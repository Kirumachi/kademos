# Security Decision: Data Classification & Protection

| Field | Value |
| :--- | :--- |
| **Project Name:** | `[Project Name]` |
| **Document Owner:** | `[e.g., Data Protection Officer, Architect]` |
| **Date:** | `YYYY-MM-DD` |
| **Status:** | `Draft / In Review / Approved` |

---

## 1. Applicable ASVS Requirements

This document addresses the high-level design decisions for the following
ASVS 5.0 requirements:

- **V14.1.1:** Identify and classify all sensitive data into protection
  levels.
- **V14.1.2:** Document the protection requirements for each classification
  level.

---

## 2. Data Classification Levels

This organization defines the following levels of data sensitivity:

- **Public:** Information intended for public consumption. Its disclosure
  would cause no harm.
- **Internal:** Information for internal employees and authorized
  contractors. Unauthorized disclosure would have a minimal negative impact.
- **Confidential:** Sensitive business or personal data. Unauthorized
  disclosure could have a significant negative impact on the company, its
  partners, or its users.
- **Restricted:** The most sensitive data, including trade secrets,
  authentication secrets, and highly regulated data. Unauthorized disclosure
  could have a critical or catastrophic impact.

---

## 3. Data Inventory & Classification (V14.1.1)

This table serves as the inventory of all sensitive data elements handled
by the application.

| Data Element | Description | Storage | Level |
| :--- | :--- | :--- | :--- |
| User Password | Authentication credential | Database | Restricted |
| Session Token | Maintains user session | Cookie, Cache | Restricted |
| User Email | Contact and login ID | Database, Logs | Confidential |
| Credit Card PAN | Payment account number | Processor only | Restricted |
| User Profile Bio | Publicly viewable bio | Database | Public |
| Feature Flag | Configuration for features | Config, DB | Internal |
| API Keys | Backend service comms | Secrets Manager | Restricted |

---

## 4. Protection Requirements per Level (V14.1.2)

This matrix defines the minimum security controls required for each data
classification level.

| Control | Public | Internal | Confidential | Restricted |
| :--- | :--- | :--- | :--- | :--- |
| **Encryption Transit** | Recommended | Required | Required | Required |
| **Encryption Rest** | N/A | Recommended | Required | Required |
| **Logging Policy** | Log access | Log access | Mask/redact | No values |
| **Data Retention** | Indefinite | Indefinite | 7 years | 30 days |
| **Access Control** | Anonymous | Authenticated | Authorized | Strict |
| **Other** | - | - | Data Masking | HSM/Vault |
