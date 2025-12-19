<p align="center">
  <h1 align="center">ASVS Compliance Starter Kit</h1>
  <p align="center">
    <strong>Ship secure software faster with OWASP ASVS 5.0</strong>
  </p>
  <p align="center">
    A practical, open-source toolkit that transforms security compliance from a burden into a competitive advantage.
  </p>
</p>

<p align="center">
  <a href="https://github.com/kaademos/asvs-compliance-starter-kit/actions/workflows/ci.yml">
    <img src="https://github.com/kaademos/asvs-compliance-starter-kit/actions/workflows/ci.yml/badge.svg" alt="CI Status">
  </a>
  <a href="https://github.com/kaademos/asvs-compliance-starter-kit/releases">
    <img src="https://img.shields.io/badge/version-2.0.0-blue.svg" alt="Version 2.0.0">
  </a>
  <a href="https://www.python.org/downloads/">
    <img src="https://img.shields.io/badge/python-3.9%20%7C%203.10%20%7C%203.11%20%7C%203.12%20%7C%203.13-blue.svg" alt="Python Versions">
  </a>
  <a href="LICENSE">
    <img src="https://img.shields.io/badge/license-Apache%202.0-green.svg" alt="License">
  </a>
  <a href="https://github.com/kaademos/asvs-compliance-starter-kit/stargazers">
    <img src="https://img.shields.io/github/stars/kaademos/asvs-compliance-starter-kit?style=social" alt="GitHub Stars">
  </a>
</p>

<p align="center">
  <a href="#-quick-start">Quick Start</a> •
  <a href="#-features">Features</a> •
  <a href="#-cli-tools">CLI Tools</a> •
  <a href="#-documentation">Documentation</a> •
  <a href="#-contributing">Contributing</a>
</p>

---

## Why This Kit?

Security compliance shouldn't slow you down. This starter kit gives you:

- **Ready-to-use templates** that pass audits (SOC2, ISO 27001)
- **CLI tools** that automate compliance checks in CI/CD
- **Secure code patterns** for Node.js, Python, Java, and Terraform
- **Machine-readable requirements** for your backlog (JSON/CSV)

> *"Shift left on security without shifting your timeline."*

---

## 🚀 Quick Start

### Option 1: Just the Templates

```bash
git clone https://github.com/kaademos/asvs-compliance-starter-kit.git
cd asvs-compliance-starter-kit

# Copy decision templates to your project
cp -r 00-Documentation-Standards/Decision-Templates ./your-project/docs/
```

### Option 2: Full Tooling

```bash
git clone https://github.com/kaademos/asvs-compliance-starter-kit.git
cd asvs-compliance-starter-kit

# Set up development environment
make build-tools

# Export requirements to your issue tracker
python -m tools.export_requirements --level 2 --format csv > requirements.csv

# Run compliance gate
python -m tools.compliance_gate --docs-path ./docs --level 2
```

### Option 3: CI/CD Integration

```yaml
# .github/workflows/security.yml
- name: ASVS Compliance Gate
  uses: kaademos/asvs-compliance-starter-kit/.github/actions/asvs-compliance-gate@main
  with:
    docs-path: './docs/Decision-Templates'
    level: '2'
```

---

## ✨ Features

### For Engineering Teams

| Feature | Description |
|---------|-------------|
| **Decision Templates** | Pre-built templates for security architecture decisions |
| **Functional Requirements** | ASVS translated into backlog-ready user stories |
| **Implementation Patterns** | Secure coding examples for popular frameworks |
| **Verification Suite** | Light DAST tool to test your security controls |

### For Security Teams

| Feature | Description |
|---------|-------------|
| **Compliance Gate** | Automated validation of security documentation |
| **Policy as Code** | OPA/Rego policies for CI/CD enforcement |
| **Drift Detection** | Track changes against upstream ASVS standard |
| **Audit Evidence** | Generate compliance reports (JSON/CSV) |

### For DevOps

| Feature | Description |
|---------|-------------|
| **GitHub Action** | Drop-in compliance gate for pipelines |
| **Make Targets** | Standardized build commands |
| **Multi-Python Support** | Tested on Python 3.9 - 3.13 |

---

## 🛠 CLI Tools

The starter kit includes four powerful CLI tools:

### Export Requirements

Export ASVS requirements to your issue tracker:

```bash
# Export Level 2 requirements to CSV (Jira/GitHub compatible)
python -m tools.export_requirements --level 2 --format csv > requirements.csv

# Export to Jira JSON format
python -m tools.export_requirements --level 2 --format jira-json > jira-import.json

# Verify source integrity
python -m tools.export_requirements --level 2 --show-hash
```

### Compliance Gate

Validate security documentation exists and is complete:

```bash
# Check your decision templates
python -m tools.compliance_gate \
  --docs-path ./docs/Decision-Templates \
  --level 2 \
  --format text

# Strict mode for CI (fails on any issue)
python -m tools.compliance_gate \
  --docs-path ./docs \
  --level 2 \
  --strict
```

**What it checks:**
- Required documents exist for your ASVS level
- Documents have meaningful content (not empty)
- Placeholder text has been replaced (`[Project Name]`, `YYYY-MM-DD`)

### Verification Suite

Test your application's security controls:

```bash
# Run security verification against your app
python -m tools.verification_suite \
  --target-url https://staging.yourapp.com \
  --format text

# JSON output for CI integration
python -m tools.verification_suite \
  --target-url https://staging.yourapp.com \
  --format json \
  --fail-on-issues
```

**Tests included:**
- Security headers (HSTS, CSP, X-Frame-Options, etc.)
- Cookie attributes (HttpOnly, Secure, SameSite)
- CSRF protection detection
- Password field security

### Drift Detector

Track your ASVS implementation against the upstream standard:

```bash
# Check for drift against OWASP ASVS
python -m tools.drift_detector

# Offline mode (no network)
python -m tools.drift_detector --offline

# JSON output
python -m tools.drift_detector --format json
```

---

## 📚 Documentation

### Getting Started Guides

New to ASVS? Start here:

| Guide | Description |
|-------|-------------|
| [ASVS L1 in 2 Weeks](04-Documentation-Artifacts/Getting-Started/ASVS-L1-2-Week-Sprint.md) | Sprint plan to achieve Level 1 compliance |
| [SOC2/ISO 27001 Mapping](04-Documentation-Artifacts/Getting-Started/ASVS-SOC2-ISO27001-Mapping.md) | Map ASVS to compliance frameworks |

### Implementation Guidance

Secure coding patterns by language:

| Language | Patterns Available |
|----------|-------------------|
| **Node.js** | Secure File Upload, Anti-CSRF (Double Submit Cookie) |
| **Python** | Input Validation (Pydantic), Secure Headers (FastAPI) |
| **Java** | Coming soon |
| **Terraform** | Secure S3 Bucket, Secure Azure Blob |

Browse all patterns: [`02-Implementation-Guidance/`](02-Implementation-Guidance/)

### Reference Material

| Resource | Description |
|----------|-------------|
| [Level Definitions](00-Documentation-Standards/Level-Definitions.md) | Choose the right ASVS level |
| [Decision Templates](00-Documentation-Standards/Decision-Templates/) | Security architecture templates |
| [ASVS Core Reference](01-ASVS-Core-Reference/) | Machine-readable ASVS (JSON/CSV) |

---

## 📁 Repository Structure

```
├── 00-Documentation-Standards/    # Templates for security decisions
│   ├── Decision-Templates/        # Fill these out for your project
│   └── Level-Definitions.md       # L1/L2/L3 explained
├── 01-ASVS-Core-Reference/        # ASVS 5.0 in JSON/CSV
│   └── Functional-Requirements/   # Backlog-ready requirements
├── 02-Implementation-Guidance/    # Secure coding patterns
│   ├── Languages/                 # Node.js, Python, Java, Terraform
│   ├── Patterns/                  # Reusable security patterns
│   └── Verification-Tests/        # Test templates
├── 03-Product-Specific-Files/     # Your project's ASVS docs
├── 04-Documentation-Artifacts/    # Getting started guides
│   └── Getting-Started/           # L1 sprint guide, compliance mapping
├── tools/                         # CLI tools
│   ├── export_requirements.py     # Export to CSV/Jira
│   ├── compliance_gate.py         # Validate documentation
│   ├── verification_suite.py      # Security testing
│   └── drift_detector.py          # Track ASVS drift
├── policies/                      # OPA/Rego policies
└── tests/                         # 143 unit tests
```

---

## ⚡ Make Targets

```bash
make help              # Show all available targets
make check             # Run JSON validation + Markdown linting
make test              # Run Python unit tests (143 tests)
make build-tools       # Set up development environment
make validate-policies # Run ASVS compliance gate
make validate-terraform # Validate Terraform formatting
make verify-security TARGET_URL=https://example.com  # Run verification suite
make check-drift       # Check for ASVS drift
make clean             # Remove generated files
```

---

## 🤝 Contributing

We welcome contributions of all kinds! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Ways to Contribute

- 🐛 Report bugs or request features via [Issues](https://github.com/kaademos/asvs-compliance-starter-kit/issues)
- 📝 Improve documentation or add implementation patterns
- 🔧 Submit pull requests for bug fixes or new features
- ⭐ Star the repo to show support

### Community

- **[ADOPTERS.md](ADOPTERS.md)** - Organizations using this kit
- **Ambassador Program** - Become a recognized contributor

---

## 📊 Project Status

| Milestone | Status | Description |
|-----------|--------|-------------|
| v1.1 - Foundation | ✅ Complete | CLI tools, Makefile, CI |
| v1.2 - Policy as Code | ✅ Complete | Compliance gate, OPA policies |
| v1.3 - Polyglot Support | ✅ Complete | Node.js, Python, Terraform patterns |
| v2.0 - Community | ✅ Complete | Getting started guides, drift detection |

See [ROADMAP.md](ROADMAP.md) for future plans.

---

## 📜 License

This project is licensed under the **Apache License 2.0**. See [LICENSE](LICENSE) for details.

---

<p align="center">
  <sub>Built with ❤️ by the security community</sub>
</p>

<p align="center">
  <a href="https://owasp.org/www-project-application-security-verification-standard/">OWASP ASVS</a> •
  <a href="https://github.com/kaademos/asvs-compliance-starter-kit/issues">Report Bug</a> •
  <a href="https://github.com/kaademos/asvs-compliance-starter-kit/issues">Request Feature</a>
</p>
