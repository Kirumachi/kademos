<div align="center">

# Kademos

### Agentic AI Security Requirements Engine

[![PyPI - Version](https://img.shields.io/pypi/v/kademos?style=flat-square&color=0066FF&labelColor=1c1c1c)](https://pypi.org/project/kademos/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/kademos?style=flat-square&color=0066FF&labelColor=1c1c1c)](https://pypi.org/project/kademos/)
[![License](https://img.shields.io/badge/license-MIT-0066FF?style=flat-square&labelColor=1c1c1c)](LICENSE)
[![Docker](https://img.shields.io/badge/docker-ready-0066FF?style=flat-square&labelColor=1c1c1c&logo=docker)](Dockerfile)

<br/>

Kademos analyzes your codebase, detects capabilities (frameworks, databases, file uploads, WebSockets), and generates exact ASVS 5.0 functional requirements—perfect for developers, security architects, and AI coding agents.

[**Explore the Docs**](docs/) · [**Report a Bug**](https://github.com/kaademos/asvs-compliance-starter-kit/issues) · [**Request Feature**](https://github.com/kaademos/asvs-compliance-starter-kit/issues)

</div>

---

## ⚡ Why Kademos?

- **Context-aware:** Scans package.json, requirements.txt, pom.xml to map your stack to ASVS chapters
- **AI-ready:** `--ai-context` outputs XML blocks for Claude, Devin, and other agents
- **Interactive:** `kademos interact` guides you to generate SECURITY_REQUIREMENTS.md before you code
- **Ticketing:** Export to Jira, Azure DevOps, or Asana as Epics/Stories

---

## 🛠️ Quick Start

### Install

```bash
pip install kademos[cli]
```

### Scan your repo

```bash
kademos scan ./path/to/repo --level 2 --format markdown > SECURITY_REQUIREMENTS.md
```

### AI agent context

```bash
kademos scan ./my-feature --ai-context > security_context.xml
```

### Interactive mode

```bash
kademos interact
```

---

## 📋 Commands

| Command | Description |
|---------|-------------|
| `kademos scan` | Analyze repo to map context to ASVS requirements |
| `kademos interact` | Generate requirements via guided TUI |
| `kademos threatmodel` | Generate STRIDE threat model prompts |
| `kademos export` | Export requirements to CSV or Jira JSON |
| `kademos resources` | List ASVS reference files, check drift |
| `kademos config` | Manage LLM API keys and integrations |

---

## 🐳 Docker

```bash
docker build -t kademos .
docker run -v $(pwd):/app kademos scan /app --level 2
```

---

<p align="center">
  <a href="https://owasp.org/www-project-application-security-verification-standard/">OWASP ASVS</a> •
  <a href="https://github.com/kaademos/asvs-compliance-starter-kit/issues">Report Bug</a> •
  <a href="https://github.com/kaademos/asvs-compliance-starter-kit/issues">Request Feature</a>
</p>
