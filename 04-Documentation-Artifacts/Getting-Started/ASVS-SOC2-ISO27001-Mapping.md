# Mapping ASVS to SOC2 and ISO 27001

A comprehensive guide for organizations seeking to align OWASP ASVS
implementation with SOC2 Trust Service Criteria and ISO 27001 Annex A
controls.

## Overview

Many organizations must demonstrate compliance with multiple frameworks
simultaneously. This guide shows how ASVS requirements map to:

- **SOC2** Trust Service Criteria (TSC)
- **ISO 27001:2022** Annex A Controls

By implementing ASVS, you automatically address significant portions of
these compliance frameworks.

---

## SOC2 Trust Service Criteria Mapping

SOC2 is organized around five Trust Service Criteria. Below is how ASVS
chapters map to each criterion.

### CC6: Logical and Physical Access Controls

| SOC2 Criterion | ASVS Chapter | Key ASVS Requirements |
|----------------|--------------|----------------------|
| CC6.1 - Logical access security | V4 (Access Control) | V4.1.1, V4.1.2, V4.2.1 |
| CC6.2 - Access removal | V4 (Access Control) | V4.1.3, V4.3.1 |
| CC6.3 - Role-based access | V4 (Access Control) | V4.1.1, V4.1.4 |
| CC6.6 - System boundary protection | V9 (API Security) | V9.1.1, V9.2.1 |
| CC6.7 - Transmission protection | V5 (Cryptography) | V5.1.1, V5.2.1 |

**ASVS Coverage:** Implementing ASVS V4 (Access Control) addresses most of
CC6 requirements for application-level access controls.

### CC7: System Operations

| SOC2 Criterion | ASVS Chapter | Key ASVS Requirements |
|----------------|--------------|----------------------|
| CC7.1 - Configuration management | V10 (Configuration) | V10.1.1, V10.2.1 |
| CC7.2 - Change detection | V10 (Configuration) | V10.3.1 |
| CC7.3 - Vulnerability management | V15 (Security Architecture) | V15.1.1, V15.1.2 |
| CC7.4 - Security monitoring | V6 (Error Handling) | V6.1.1, V6.2.1 |

**ASVS Coverage:** ASVS V6 (Error Handling & Logging) and V10 (Configuration)
provide the application-level controls for CC7.

### CC8: Change Management

| SOC2 Criterion | ASVS Chapter | Key ASVS Requirements |
|----------------|--------------|----------------------|
| CC8.1 - Change authorization | V10 (Configuration) | V10.1.1 |
| CC8.2 - Change testing | V15 (Security Architecture) | V15.2.1 |

**ASVS Coverage:** ASVS focuses on secure configuration; change management
processes are typically addressed at the organizational level.

### CC3: Risk Assessment

| SOC2 Criterion | ASVS Chapter | Key ASVS Requirements |
|----------------|--------------|----------------------|
| CC3.1 - Risk identification | V15 (Security Architecture) | V15.1.1, V15.1.2 |
| CC3.2 - Risk analysis | Decision Templates | V11, V15 templates |
| CC3.4 - Risk mitigation | All chapters | Level-based implementation |

**ASVS Coverage:** ASVS Level selection (L1/L2/L3) itself is a risk-based
decision. Decision Templates help document risk mitigation choices.

### CC5: Control Activities

| SOC2 Criterion | ASVS Chapter | Key ASVS Requirements |
|----------------|--------------|----------------------|
| CC5.1 - SDLC security | V15 (Security Architecture) | V15.1.1 |
| CC5.2 - Configuration management | V10 (Configuration) | V10.1.1, V10.2.1 |

---

## ISO 27001:2022 Annex A Mapping

ISO 27001 Annex A contains 93 controls organized into 4 themes. Below is
the mapping to ASVS chapters.

### A.5 - Organizational Controls

| ISO Control | ASVS Chapter | Key ASVS Requirements |
|-------------|--------------|----------------------|
| A.5.1 - Policies | Decision Templates | Policy documentation |
| A.5.10 - Acceptable use | V15 (Architecture) | V15.1.1 |
| A.5.15 - Access control | V4 (Access Control) | V4.1.1, V4.1.2 |
| A.5.16 - Identity management | V3 (Session Mgmt) | V3.1.1, V3.2.1 |
| A.5.17 - Authentication | V3 (Session Mgmt) | V3.3.1, V3.4.1 |
| A.5.18 - Access rights | V4 (Access Control) | V4.1.3, V4.2.1 |

### A.6 - People Controls

| ISO Control | ASVS Chapter | Key ASVS Requirements |
|-------------|--------------|----------------------|
| A.6.3 - Security awareness | Documentation | README, guides |
| A.6.8 - Security event reporting | V6 (Error Handling) | V6.2.1 |

### A.7 - Physical Controls

*Note: ASVS focuses on application security; physical controls are
typically addressed separately.*

### A.8 - Technological Controls

| ISO Control | ASVS Chapter | Key ASVS Requirements |
|-------------|--------------|----------------------|
| A.8.2 - Privileged access | V4 (Access Control) | V4.1.4, V4.3.1 |
| A.8.3 - Information access | V4 (Access Control) | V4.2.1 |
| A.8.5 - Secure authentication | V3 (Session Mgmt) | V3.4.1, V3.5.1 |
| A.8.6 - Capacity management | V10 (Configuration) | V10.2.1 |
| A.8.9 - Configuration management | V10 (Configuration) | V10.1.1, V10.3.1 |
| A.8.10 - Information deletion | V7 (Data Protection) | V7.1.1 |
| A.8.11 - Data masking | V7 (Data Protection) | V7.2.1 |
| A.8.12 - Data leakage prevention | V6, V7 | V6.1.1, V7.1.1 |
| A.8.20 - Network security | V9 (API Security) | V9.1.1 |
| A.8.21 - Web services security | V9 (API Security) | V9.2.1, V9.3.1 |
| A.8.24 - Cryptography | V5 (Cryptography) | V5.1.1, V5.2.1, V5.3.1 |
| A.8.25 - Secure development | V15 (Architecture) | V15.1.1, V15.2.1 |
| A.8.26 - Security requirements | V15 (Architecture) | V15.1.2 |
| A.8.27 - Architecture principles | V15 (Architecture) | V15.1.1 |
| A.8.28 - Secure coding | V1, V2 | V1.2.1, V2.2.1 |
| A.8.29 - Security testing | Verification Suite | tools/verification_suite.py |
| A.8.31 - Dev/test separation | V10 (Configuration) | V10.1.1 |

---

## ASVS Level to Compliance Framework Mapping

### Level 1 (Baseline) Coverage

| Framework | Approximate Coverage | Notes |
|-----------|---------------------|-------|
| SOC2 | ~40% of application controls | Covers essential access controls |
| ISO 27001 A.8 | ~35% of tech controls | Covers authentication, basic crypto |

### Level 2 (Standard) Coverage

| Framework | Approximate Coverage | Notes |
|-----------|---------------------|-------|
| SOC2 | ~70% of application controls | Adds logging, validation |
| ISO 27001 A.8 | ~60% of tech controls | Adds comprehensive input handling |

### Level 3 (Advanced) Coverage

| Framework | Approximate Coverage | Notes |
|-----------|---------------------|-------|
| SOC2 | ~85% of application controls | Full security controls |
| ISO 27001 A.8 | ~80% of tech controls | Defense in depth |

---

## Creating Compliance Evidence

### Using ASVS Tools for Audit Evidence

1. **Requirement Inventory (V15.1.2):**

   ```bash
   python -m tools.export_requirements --level 2 --format csv > evidence/asvs-requirements.csv
   ```

2. **Compliance Gate Reports:**

   ```bash
   python -m tools.compliance_gate \
     --docs-path ./docs/Decision-Templates \
     --level 2 \
     --format json > evidence/compliance-gate-report.json
   ```

3. **Verification Test Results:**

   ```bash
   python -m tools.verification_suite \
     --target-url https://app.example.com \
     --format json > evidence/security-verification.json
   ```

4. **Drift Detection (Version Control):**

   ```bash
   python -m tools.drift_detector --format json > evidence/asvs-drift-report.json
   ```

### Evidence Mapping Table

| Evidence Type | SOC2 Criterion | ISO 27001 Control |
|--------------|----------------|-------------------|
| Compliance Gate Report | CC3.2, CC5.1 | A.5.1, A.8.25 |
| Verification Suite Output | CC7.1, CC7.4 | A.8.29 |
| Decision Templates | CC3.4, CC6.1 | A.5.1, A.8.27 |
| Export Requirements CSV | CC3.1, CC7.3 | A.8.26 |

---

## Gap Analysis: What ASVS Does NOT Cover

While ASVS provides excellent application security coverage, these areas
require additional controls:

### For SOC2

- **CC1 (Control Environment):** Organizational governance
- **CC2 (Communication):** Security awareness programs
- **CC4 (Monitoring):** Management oversight
- **CC9 (Risk Mitigation):** Vendor management

### For ISO 27001

- **A.5.1-A.5.9:** Policy and organizational controls
- **A.6 (People):** HR security, training
- **A.7 (Physical):** Physical and environmental security
- **A.5.19-A.5.23:** Supplier relationships

---

## Implementation Workflow for Dual Compliance

### Step 1: Establish Baseline

1. Determine ASVS Level based on application risk
2. Map to SOC2/ISO requirements using this guide
3. Identify gaps requiring additional controls

### Step 2: Document Controls

Use the starter kit templates:

```plaintext
00-Documentation-Standards/
├── Decision-Templates/
│   ├── V11-Cryptography-Strategy.md    → A.8.24, CC6.7
│   └── V15-Security-Architecture.md    → A.8.25, CC5.1
```

### Step 3: Implement and Verify

1. Implement ASVS requirements per level
2. Run verification suite regularly
3. Generate compliance evidence (JSON/CSV exports)

### Step 4: Continuous Monitoring

```bash
# Add to CI/CD pipeline
python -m tools.compliance_gate --level 2 --format json
python -m tools.drift_detector --format json
```

---

## Quick Reference: Control Families

| ASVS Chapter | Primary SOC2 | Primary ISO 27001 |
|-------------|--------------|-------------------|
| V1 - Encoding | CC6.1 | A.8.28 |
| V2 - Validation | CC6.1 | A.8.28 |
| V3 - Session | CC6.1, CC6.3 | A.5.16, A.5.17 |
| V4 - Access Control | CC6.1-CC6.3 | A.5.15, A.8.2 |
| V5 - Cryptography | CC6.7 | A.8.24 |
| V6 - Error Handling | CC7.4 | A.6.8, A.8.12 |
| V7 - Data Protection | CC6.7 | A.8.10, A.8.11 |
| V9 - API Security | CC6.6 | A.8.20, A.8.21 |
| V10 - Configuration | CC7.1, CC8.1 | A.8.9 |
| V15 - Architecture | CC3.1, CC5.1 | A.8.25-A.8.27 |

---

## Resources

- [AICPA SOC2 Guide](https://www.aicpa.org/soc)
- [ISO 27001:2022 Standard](https://www.iso.org/standard/27001)
- [OWASP ASVS Mapping Project](https://owasp.org/www-project-application-security-verification-standard/)
- Starter Kit Tools: `tools/export_requirements.py`, `tools/compliance_gate.py`

---

*Document Version: 1.0 | Last Updated: 2024*
*Mapping based on ASVS 5.0, SOC2 2017, ISO 27001:2022*
