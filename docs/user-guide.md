# Kademos User Guide

This guide details the usage of every Kademos command.

## 1. Scan (`kademos scan`)

Scans a repository to detect frameworks, databases, and capabilities, then maps them to ASVS requirements.

### Usage

```bash
kademos scan [PATH] [OPTIONS]
```

### Options

* `path`: Repository path (default: current directory)
* `--level {1,2,3}`: ASVS level (default: 2)
* `--format {markdown,json}`: Output format
* `--ai-context`: Output XML for AI agents
* `--base-path PATH`: Base path for ASVS reference files

### Examples

```bash
kademos scan . --level 2 --format markdown > SECURITY_REQUIREMENTS.md
kademos scan ./my-app --ai-context > security_context.xml
```

---

## 2. Interact (`kademos interact`)

Interactive mode for generating security requirements before you write code.

### Usage

```bash
kademos interact [OPTIONS]
```

### Options

* `--output PATH`: Output file (default: SECURITY_REQUIREMENTS.md)
* `--base-path PATH`: Base path for ASVS reference files

---

## 3. Threat Model (`kademos threatmodel`)

Generates an LLM-ready prompt for STRIDE threat modeling.

### Usage

```bash
kademos threatmodel [OPTIONS]
```

### Options

* `--tech-stack TEXT`: Tech stack description
* `--output PATH`: Output file (default: threat_model_prompt.txt)

---

## 4. Export (`kademos export`)

Exports ASVS requirements to CSV or Jira-compatible JSON.

### Usage

```bash
kademos export [OPTIONS]
```

### Options

* `--level {1,2,3}`: ASVS level
* `--format {csv,jira-json}`: Output format
* `--output PATH`: Output file (default: stdout)
* `--base-path PATH`: Base path for ASVS reference files

### Examples

```bash
kademos export --level 2 --format csv > requirements.csv
kademos export --level 2 --format jira-json --output jira-import.json
```

---

## 5. Resources (`kademos resources`)

Lists ASVS reference files and checks drift against upstream.

### Usage

```bash
kademos resources [OPTIONS]
kademos resources --drift [OPTIONS]
```

### Options

* `--drift`: Check drift against upstream OWASP ASVS
* `--format {text,json}`: Output format
* `--offline`: Skip upstream fetch
* `--base-path PATH`: Base path for ASVS reference files

---

## 6. Config (`kademos config`)

Manages LLM API keys and ticketing integrations. Set `KADEMOS_OPENAI_KEY` or `KADEMOS_ANTHROPIC_KEY` for AI features.
