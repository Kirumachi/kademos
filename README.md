<div align="center">

# OWASP ASVS Compliance Engine

### Turn Security Requirements into Verifiable Code.

[![PyPI - Version](https://img.shields.io/pypi/v/asvs-compliance-starter-kit?style=flat-square&color=0066FF&labelColor=1c1c1c)](https://pypi.org/project/asvs-compliance-starter-kit/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/asvs-compliance-starter-kit?style=flat-square&color=0066FF&labelColor=1c1c1c)](https://pypi.org/project/asvs-compliance-starter-kit/)
[![License](https://img.shields.io/badge/license-Apache_2.0-0066FF?style=flat-square&labelColor=1c1c1c)](LICENSE)
[![Docker](https://img.shields.io/badge/docker-ready-0066FF?style=flat-square&labelColor=1c1c1c&logo=docker)](Dockerfile)

<br/>

<img src="https://placehold.co/1200x600/1c1c1c/0066FF?text=Does+your+code+actually+meet+security+standards?%0AProove+it+with+one+command.&font=montserrat" alt="ASVS Compliance Engine Hero" width="100%" />

<br/>
<br/>

Move beyond static checklists. The ASVS Compliance Engine is a DevSecOps toolkit that automates the **OWASP Application Security Verification Standard (ASVS) 5.0**. It empowers engineering teams to treat compliance as code, verifying security controls directly in the CI/CD pipeline.

[**Explore the Docs**](docs/) · [**Report a Bug**](https://github.com/kaademos/asvs-compliance-starter-kit/issues) · [**Request Feature**](https://github.com/kaademos/asvs-compliance-starter-kit/issues)

</div>

---

## ⚡ Why Use This?

Most compliance efforts fail because they rely on Word documents that become obsolete the moment they're written. This engine solves the "proof gap" by linking requirements directly to your codebase.

<div align="center">

| ❌ Old Way (Static) | ✅ New Way (Dynamic) |
| :--- | :--- |
| Manual spreadsheet updates | **Automated** evidence collection |
| "Trust me" attestations | **Verifiable** code & config checks |
| Scrambling before an audit | **Continuous** audit-readiness |

</div>

---

## 🚀 Key Features

### 1. Automated Evidence Verification
Don't just claim you use secure libraries—prove it. Map ASVS requirements directly to files in your repository. The engine scans for their existence and content.

<img src="https://placehold.co/1000x400/1c1c1c/0066FF?text=IMAGE+PLACEHOLDER:+Split+screen+showing+evidence.yml+and+terminal+pass+result" alt="Evidence Verification Example" width="100%" />

```yaml
# evidence.yml
requirements:
  V14.4.1: # HTTP Security Headers
    checks:
      - type: content_match
        path: "package.json"
        pattern: "\"helmet\"" # Verify Helmet.js is installed

```

### 2. Infrastructure-as-Code (IaC) Scanning

Shift security left by catching cloud misconfigurations before they are deployed. Our native scanner checks Terraform plans against ASVS V5.3 requirements for storage security.

<img src="https://placehold.co/1000x300/1c1c1c/0066FF%3Ftext%3DIMAGE%2BPLACEHOLDER:%2BTerminal%2Boutput%2Bshowing%2BTerraform%2Bscan%2Bfailure%2Bfor%2Bunencrypted%2BS3%2Bbucket" alt="IaC Scanner Example" width="100%" />

### 3. Auditor-Ready Dashboards

Generate comprehensive HTML reports that combine documentation status, code evidence, and DAST results into a single pane of glass for stakeholders and auditors (SOC2, ISO 27001).

<img src="https://placehold.co/1000x500/1c1c1c/0066FF%3Ftext%3DIMAGE%2BPLACEHOLDER:%2BScreenshot%2Bof%2Bthe%2BHTML%2Bcompliance%2Bdashboard" alt="Compliance Dashboard Example" width="100%" />

---

## 🛠️ Quick Start

Get up and running in minutes.

### Option A: Using Python (Recommended)

1. **Install the toolkit:**
```bash
pip install "asvs-compliance-starter-kit[evidence,verification]"

```

2. **Initialize your project:**
Run the wizard to generate your security architecture documentation based on your risk profile.
```bash
python -m tools.init_project --interactive

```

3. **Verify compliance:**
Run the gate against your docs and the generated sample evidence.
```bash
python -m tools.compliance_gate --level 2 --evidence-manifest evidence.yml

```

### Option B: Using Docker

No Python? No problem. Run the full suite in a container.

```bash
# Build the image
docker build -t asvs-engine .

# Run the init wizard
docker run -it -v $(pwd):/app asvs-engine tools.init_project --interactive

# Run the compliance gate
docker run -v $(pwd):/app asvs-engine tools.compliance_gate --level 2 --evidence-manifest evidence.yml
```

---

## 🗓️ Roadmap & Community

We are actively building the future of open-source compliance. Check out our **[ROADMAP.md](https://www.google.com/search?q=ROADMAP.md)** to see what's coming next, including:

* Two-way sync with Jira/GitHub Issues.
* Pre-built evidence packs for Node.js, Python, and Java frameworks.
* Expanded cloud infrastructure scanning.

**Want to contribute?** We'd love your help! See our [CONTRIBUTING.md](https://www.google.com/search?q=CONTRIBUTING.md) guide to get started.

---

<div align="center">
<p>
Currently maintaining this project in my free time.

If this tool saves your company time and money, please consider supporting its development.
</p>
<a href="https://github.com/sponsors/kaademos">
<img src="=https://img.shields.io/badge/Sponsor-💖-ff69b4?style=for-the-badge" alt="Sponsor">
</a>
</div>

<p align="center">
  <a href="https://owasp.org/www-project-application-security-verification-standard/">OWASP ASVS</a> •
  <a href="https://github.com/kaademos/asvs-compliance-starter-kit/issues">Report Bug</a> •
  <a href="https://github.com/kaademos/asvs-compliance-starter-kit/issues">Request Feature</a>
</p>
