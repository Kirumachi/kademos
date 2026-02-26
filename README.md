<div align="center">

<img src="docs/assets/kademos-logo.png" alt="Kademos Logo" width="250" />

### The Context-Aware Security Requirements Engine for Devs and Agentic AI

![PyPI - Version](https://img.shields.io/pypi/v/kademos)
[![Python Version](https://img.shields.io/pypi/pyversions/kademos?style=flat-square&color=8A2BE2&labelColor=1c1c1c)](https://pypi.org/project/kademos/)
[![License](https://img.shields.io/badge/license-MIT-00FF66?style=flat-square&labelColor=1c1c1c)](LICENSE)

<br/>

<img src="docs/assets/demo.gif" alt="Kademos Demo" width="100%" />

<br/>
<br/>

**Security compliance shouldn't rely on guesswork, and AI agents shouldn't write code without guardrails.**

Kademos is a modern DevSecOps engine that bridges the gap between the **OWASP ASVS 5.0** standard and actionable developer workflows. It analyzes your codebase, understands your application's capabilities, and generates exact, machine-readable security requirements.

[**Quick Start**](#-quick-start) · [**For AI Agents**](#-agentic-ai-integration) · [**Documentation**](docs/) · [**Report Bug**](https://github.com/kaademos/kademos/issues)

</div>

---

## ✨ Why Kademos?

The era of static, Excel-based security checklists is over. Whether you are a developer building a new feature or an Agentic AI (like Devin or Claude) writing code autonomously, you need exact security requirements *before* the code is written.

* **🧠 Context-Aware Scanning:** Kademos parses your AST and package managers (React, Django, PostgreSQL) to detect features and map them automatically to ASVS Level 1 & 2 requirements.
* **🤖 Native Agentic AI Support:** Export tightly structured XML context blocks designed specifically for LLM context windows. 
* **💬 Beautiful Interactive TUI:** Use `kademos interact` to walk through a guided, rich terminal interface when planning new features.
* **🛡️ Threat Model Ready:** Generates perfectly scoped STRIDE prompts based on your tech stack to kickstart LLM-assisted threat modeling.

---

## 🚀 Quick Start

### Installation
```bash
pip install kademos

```

### 1. Scan your Repository

Let Kademos figure out what your app does and generate the security baseline:

```bash
kademos scan ./my-project --level 2 --format markdown > SECURITY_REQUIREMENTS.md

```

### 2. Interactive Feature Planning (TUI)

Planning a new password reset flow? Generate the exact ASVS requirements interactively:

```bash
kademos interact

```

---

## 🤖 Agentic AI Integration

Kademos is built to be the "Security Brain" for AI coding agents. If you are using Claude, Devin, or a custom GPT, inject Kademos into your pipeline.

Use the `--ai-context` flag to output pure, structured XML that LLMs understand perfectly:

```bash
kademos scan ./backend --ai-context > ai_security_guardrails.xml

```

**Example Agent Prompt:**

> *"Read `ai_security_guardrails.xml`. You are tasked with writing the new File Upload module. Ensure your generated code strictly adheres to the ASVS V5 requirements outlined in the context block."*

---

## 🛠️ CLI Reference

Simply type `kademos` to see the splash screen and available commands.

| Command | Description |
| --- | --- |
| `kademos scan` | Analyze repo AST/packages to map context to ASVS requirements |
| `kademos interact` | Generate requirements via AI-guided developer TUI |
| `kademos threatmodel` | Generate scoped LLM prompts for STRIDE modeling |
| `kademos export` | Push actionable requirements to Jira, Azure, or Asana |
| `kademos resources` | Manage ASVS reference files and local cache |

---

## 🤝 Contributing

We welcome contributions from the community! Check out our [Contributing Guide](https://www.google.com/search?q=CONTRIBUTING.md) to see how you can add framework adapters, improve the TUI, or expand AI prompt generation.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](https://www.google.com/search?q=LICENSE) file for details.

<p align="center">
  <a href="https://owasp.org/www-project-application-security-verification-standard/">OWASP ASVS</a> •
  <a href="https://github.com/kaademos/asvs-compliance-starter-kit/issues">Report Bug</a> •
  <a href="https://github.com/kaademos/asvs-compliance-starter-kit/issues">Request Feature</a>
</p>
