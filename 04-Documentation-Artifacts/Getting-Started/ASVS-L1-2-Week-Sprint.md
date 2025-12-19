# How to Adopt ASVS L1 in a 2-Week Sprint

A practical, step-by-step guide for teams looking to achieve ASVS Level 1
compliance within a focused two-week sprint cycle.

## Overview

ASVS Level 1 (L1) represents the minimum baseline security controls that
every application should implement. This guide breaks down the adoption
process into manageable daily tasks across two weeks.

**Prerequisites:**

- Development team with access to source code
- Basic understanding of web application security concepts
- Access to this ASVS Compliance Starter Kit

**Expected Outcomes:**

- All L1 requirements documented and triaged
- Critical security controls implemented
- Verification tests in place for key requirements
- Foundation for continuous compliance monitoring

---

## Week 1: Assessment and Planning

### Day 1-2: Requirement Export and Initial Triage

**Goal:** Create a prioritized backlog of L1 requirements.

**Tasks:**

1. Export L1 requirements to your issue tracker:

   ```bash
   python -m tools.export_requirements --level 1 --format csv > l1-requirements.csv
   # Or for Jira:
   python -m tools.export_requirements --level 1 --format jira-json > l1-requirements.json
   ```

2. Import requirements into your project management system (Jira, GitHub
   Issues, Linear, etc.)

3. Categorize requirements by domain:
   - **V1 - Encoding & Sanitization** (Injection prevention)
   - **V2 - Validation & Business Logic** (Input validation)
   - **V3 - Session Management** (Authentication state)
   - **V4 - Access Control** (Authorization)
   - **V5 - Cryptography** (Data protection)
   - **V6 - Error Handling** (Information disclosure)

4. Mark "Already Implemented" items based on existing controls.

**Deliverable:** Prioritized backlog with ~50-70 L1 items categorized.

### Day 3: Architectural Review

**Goal:** Map existing architecture to ASVS requirements.

**Tasks:**

1. Review Decision Templates in `00-Documentation-Standards/Decision-Templates/`
2. Document your current:
   - Authentication mechanism
   - Session management approach
   - Input validation strategy
   - Error handling policy
3. Identify gaps between current state and L1 requirements.

**Deliverable:** Gap analysis document.

### Day 4-5: High-Priority Implementation (Encoding & Injection)

**Goal:** Address the highest-risk category - V1 Encoding & Sanitization.

**Key L1 Requirements to Address:**

| ID | Requirement | Implementation |
|----|-------------|----------------|
| V1.2.1 | Output encoding for HTTP responses | Use framework auto-escaping |
| V1.2.4 | Parameterized queries | Use ORM or prepared statements |
| V1.2.5 | OS command injection protection | Use subprocess with arrays |
| V1.3.1 | HTML sanitization | Use DOMPurify or Bleach |

**Implementation Guidance:**

- See `02-Implementation-Guidance/` for language-specific patterns
- Focus on data flow from user input to output/storage
- Enable framework security features (auto-escaping, CSRF tokens)

**Deliverable:** PRs for encoding/injection controls.

---

## Week 2: Implementation and Verification

### Day 6-7: Input Validation (V2)

**Goal:** Implement validation controls.

**Key L1 Requirements:**

| ID | Requirement | Implementation |
|----|-------------|----------------|
| V2.2.1 | Input validation against allow-lists | Schema validation |
| V2.2.2 | Server-side validation | Never trust client-only |
| V2.3.1 | HTTP parameter pollution protection | Framework middleware |

**Quick Wins:**

- Enable strict mode in your validation library
- Add request schema validation middleware
- Implement maximum length checks on all inputs

**Deliverable:** Input validation layer implemented.

### Day 8: Session Management (V3)

**Goal:** Secure session handling.

**Key L1 Requirements:**

| ID | Requirement | Implementation |
|----|-------------|----------------|
| V3.2.1 | Generate new session on auth | Regenerate session ID |
| V3.4.1 | Secure cookie attributes | HttpOnly, Secure, SameSite |
| V3.5.1 | CSRF protection | Double-submit or sync token |

**Verification:**

```bash
# Test session and cookie security
python -m tools.verification_suite --target-url https://your-app.local
```

**Deliverable:** Session security controls verified.

### Day 9: Access Control (V4)

**Goal:** Verify authorization controls.

**Key L1 Requirements:**

| ID | Requirement | Implementation |
|----|-------------|----------------|
| V4.1.1 | Access control at trusted layer | Server-side checks |
| V4.1.2 | Deny by default | Explicit allow rules |
| V4.2.1 | Direct object reference protection | Authorization checks |

**Implementation Pattern:**

```python
# Deny by default pattern
def get_resource(resource_id, user):
    resource = Resource.get(resource_id)
    if not user.can_access(resource):  # Explicit check
        raise PermissionDenied()
    return resource
```

**Deliverable:** Authorization review complete.

### Day 10: Cryptography & Error Handling (V5, V6)

**Goal:** Data protection and safe error handling.

**Key L1 Requirements:**

| ID | Requirement | Implementation |
|----|-------------|----------------|
| V5.1.1 | No hardcoded secrets | Environment variables |
| V5.2.1 | Strong password hashing | bcrypt/argon2 |
| V6.1.1 | Generic error messages | Hide stack traces |
| V6.1.2 | Consistent error handling | Centralized handler |

**Quick Security Audit:**

```bash
# Search for potential hardcoded secrets
grep -r "password\s*=" --include="*.py" --include="*.js" .
grep -r "api_key\s*=" --include="*.py" --include="*.js" .
```

**Deliverable:** Cryptography and error handling review complete.

---

## Final Verification (Day 10)

### Run Compliance Gate

Verify your documentation is complete:

```bash
python -m tools.compliance_gate \
  --docs-path ./docs/Decision-Templates \
  --level 1 \
  --format text
```

### Run Verification Suite

Test implementation of key controls:

```bash
python -m tools.verification_suite \
  --target-url https://your-staging-app.example.com \
  --format json > verification-report.json
```

### Check for Drift

Ensure you're aligned with latest ASVS:

```bash
python -m tools.drift_detector --offline
```

---

## Sprint Completion Checklist

### Documentation

- [ ] Decision Templates completed for L1 requirements
- [ ] Gap analysis documented
- [ ] Implementation decisions recorded

### Implementation

- [ ] V1: Output encoding and injection prevention
- [ ] V2: Input validation on all endpoints
- [ ] V3: Secure session management
- [ ] V4: Authorization checks on all resources
- [ ] V5: No hardcoded secrets, proper hashing
- [ ] V6: Generic error messages in production

### Verification

- [ ] Verification suite passes on staging
- [ ] Compliance gate passes
- [ ] Security tests added to CI pipeline

---

## Post-Sprint: Continuous Compliance

After completing the sprint:

1. **Add to CI/CD:** Include compliance gate in your pipeline:

   ```yaml
   - name: ASVS Compliance Gate
     uses: ./.github/actions/asvs-compliance-gate
     with:
       docs-path: './docs/Decision-Templates'
       level: '1'
   ```

2. **Schedule Drift Checks:** Run drift detector monthly to catch upstream
   changes.

3. **Plan L2 Adoption:** Once L1 is stable, plan a follow-up sprint for L2
   requirements.

---

## Common Blockers and Solutions

| Blocker | Solution |
|---------|----------|
| Legacy code without validation | Add validation middleware at API gateway |
| Hardcoded credentials | Migrate to secrets manager (Vault, AWS Secrets) |
| No CSRF protection | Add framework CSRF middleware |
| Verbose error messages | Configure production error handler |
| Missing security headers | Add security headers middleware |

---

## Resources

- [OWASP ASVS 5.0 Full Document](https://owasp.org/www-project-application-security-verification-standard/)
- [OWASP Cheat Sheet Series](https://cheatsheetseries.owasp.org/)
- Implementation Guidance: `02-Implementation-Guidance/`
- Verification Tests: `tools/verification_suite.py`

---

*Document Version: 1.0 | Last Updated: 2024*
