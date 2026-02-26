#!/usr/bin/env python3
"""
Kademos — Agentic AI Security Requirements Engine

Unified CLI entrypoint.
- kademos scan: Context-aware repo scanning
- kademos interact: Interactive TUI for requirements
- kademos threatmodel: Generate STRIDE prompts
- kademos export: Push requirements to Jira/Azure/Asana
- kademos resources: Manage ASVS reference files
- kademos config: Manage LLM API keys and settings
"""

import argparse
import json
import sys
from pathlib import Path
from typing import List, Optional

from rich.console import Console
from rich.table import Table
from rich.text import Text
from rich import box

from tools.paths import get_source_file


def get_version() -> str:
    """Return package version."""
    try:
        import importlib.metadata
        return importlib.metadata.version("kademos")
    except Exception:
        return "3.0.0"


def show_splash(version: str) -> None:
    """Display splash screen when kademos runs with no args."""
    console = Console()
    ascii_art = """
    __  __        __
   / / / /____ __/ /___  ____ ___  ____  _____
  / /_/ // __ `/ __  / _ \\/ __ `__ \\/ __ \\/ ___/
 / __  // /_/ / /_/ /  __/ / / / / / /_/ (__  )
/_/ /_/ \\__,_/\\__,_/\\___/_/ /_/ /_/\\____/____/
"""
    console.print()
    header_table = Table(box=None, show_header=False, padding=(0, 2))
    ascii_text = Text(ascii_art, style="bold color(43)")
    info_text = Text()
    info_text.append(f"v{version}\n", style="dim")
    info_text.append("Agentic AI Security Requirements Engine\n", style="bold white")
    info_text.append("https://github.com/Kaademos/kademos\n", style="dim blue")
    header_table.add_row(ascii_text, info_text)
    console.print(header_table)

    table = Table(
        box=box.SIMPLE_HEAVY,
        border_style="color(240)",
        header_style="bold color(141)",
        padding=(0, 2),
    )
    table.add_column("Command", style="bold white")
    table.add_column("Description", style="white")
    table.add_row("kademos scan", "Analyze repo to map context to ASVS requirements")
    table.add_row("kademos interact", "Generate requirements via AI-guided developer TUI")
    table.add_row("kademos threatmodel", "Generate scoped LLM prompts for STRIDE modeling")
    table.add_row("kademos export", "Push actionable requirements to Jira, Azure, or Asana")
    table.add_row("kademos resources", "Manage ASVS reference files and AI context blocks")
    table.add_row("kademos config", "Manage LLM API keys and settings")
    console.print(table)

    console.print()
    console.print("  [color(226)]⚡[/] Run [bold white]kademos scan --ai-context[/] to output XML blocks for AI Agents.")
    console.print("  [color(214)]🔐[/] Ensure your LLM API keys are set via [bold white]kademos config set[/].")
    console.print("  [color(43)]🌟[/] Star us on GitHub to support open-source secure development.")
    console.print()


def cmd_scan(parsed: argparse.Namespace) -> int:
    """Scan repo to map capabilities to ASVS requirements."""
    from tools.capability_scanner import scan_repo

    repo_path = Path(parsed.path).resolve()
    if not repo_path.exists():
        print(f"Error: Path not found: {repo_path}", file=sys.stderr)
        return 1

    result = scan_repo(repo_path)
    base_path = getattr(parsed, "base_path", None)

    try:
        source_path = get_source_file(str(parsed.level), base_path)
    except (ValueError, FileNotFoundError) as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    with open(source_path, encoding="utf-8") as f:
        requirements = json.load(f)

    # Filter by level; optionally narrow by detected chapters
    from tools.capability_scanner import BASELINE_CHAPTERS

    level_hierarchy = {"1": 1, "2": 2, "3": 3}
    max_level = level_hierarchy.get(str(parsed.level), 2)
    level_filtered = [
        r for r in requirements
        if isinstance(r, dict)
        and level_hierarchy.get(str(r.get("L", "2")), 99) <= max_level
    ]
    extra_chapters = result.chapters - set(BASELINE_CHAPTERS)
    if extra_chapters:
        filtered = [r for r in level_filtered if r.get("chapter_id") in result.chapters]
    else:
        filtered = level_filtered

    if getattr(parsed, "ai_context", False):
        # XML output for AI agents
        lines = ['<?xml version="1.0" encoding="UTF-8"?>']
        lines.append("<security_requirements>")
        lines.append(f"  <tech_stack>{', '.join(result.frameworks) or 'Unknown'}</tech_stack>")
        lines.append(f"  <capabilities>{', '.join(sorted(result.capabilities))}</capabilities>")
        lines.append("  <requirements>")
        for r in filtered[:50]:  # Cap for AI context
            rid = r.get("req_id", "")
            desc = (r.get("req_description", "") or "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            lines.append(f'    <requirement id="{rid}">{desc}</requirement>')
        lines.append("  </requirements>")
        lines.append("</security_requirements>")
        print("\n".join(lines))
        return 0

    # Markdown or JSON output
    if parsed.format == "json":
        print(json.dumps({"requirements": filtered, "detected": {"frameworks": result.frameworks, "chapters": list(result.chapters)}}, indent=2))
        return 0

    # Markdown
    md_lines = ["# ASVS Security Requirements (Kademos Scan)", ""]
    md_lines.append(f"**Detected:** {', '.join(result.frameworks) or 'Generic'} | Chapters: {', '.join(sorted(result.chapters))}")
    md_lines.append("")
    current_chapter = None
    for r in filtered:
        ch = r.get("chapter_id", "")
        if ch != current_chapter:
            current_chapter = ch
            md_lines.append(f"## {r.get('chapter_name', ch)}")
            md_lines.append("")
        md_lines.append(f"- **{r.get('req_id', '')}** {r.get('req_description', '')}")
        md_lines.append("")
    print("\n".join(md_lines))
    return 0


def cmd_interact(parsed: argparse.Namespace) -> int:
    """Interactive TUI for generating security requirements."""
    console = Console()
    console.print("[bold]Kademos Interactive - Feature Security Requirements[/bold]")
    console.print()
    prompt = "[bold cyan]Describe your feature (e.g., 'password reset for Django app'):[/bold cyan] "
    feature = console.input(prompt)

    if not feature.strip():
        print("No feature described. Exiting.", file=sys.stderr)
        return 1

    base_path = getattr(parsed, "base_path", None)
    try:
        source_path = get_source_file("2", base_path)
    except (ValueError, FileNotFoundError) as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    with open(source_path, encoding="utf-8") as f:
        requirements = json.load(f)

    # Include V2 (Authentication) and V3 (Session) as default for "password reset" type prompts
    level2_reqs = [r for r in requirements if isinstance(r, dict) and str(r.get("L", "")) in ("1", "2")]
    sample = level2_reqs[:30]

    output_path = Path(parsed.output) if getattr(parsed, "output", None) else Path("SECURITY_REQUIREMENTS.md")
    lines = [
        "# Security Requirements",
        "",
        f"**Feature:** {feature.strip()}",
        "",
        "## Applicable ASVS Requirements (Level 2)",
        "",
    ]
    for r in sample:
        lines.append(f"- **{r.get('req_id', '')}** {r.get('req_description', '')}")
        lines.append("")

    output_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"Generated: {output_path}")
    return 0


def cmd_threatmodel(parsed: argparse.Namespace) -> int:
    """Generate threat model LLM prompt."""
    tech_stack = getattr(parsed, "tech_stack", "Web application")
    output_path = Path(parsed.output) if getattr(parsed, "output", None) else Path("threat_model_prompt.txt")

    prompt = f"""You are an expert security architect. I am building a {tech_stack} application with the following considerations.

I have adopted ASVS 5.0 Level 2 functional requirements for this project.

Based on STRIDE, generate a threat model for this specific feature set and identify any edge-case threats not covered by these baseline requirements.

Provide:
1. Threat actors and attack vectors
2. Mitigations aligned with ASVS controls
3. Residual risks and acceptance criteria
"""

    output_path.write_text(prompt, encoding="utf-8")
    print(f"Generated: {output_path}")
    return 0


def cmd_export(parsed: argparse.Namespace) -> int:
    """Export requirements (delegate to export_requirements)."""
    from tools import export_requirements

    args = ["--level", str(parsed.level), "--format", parsed.format]
    if getattr(parsed, "base_path", None):
        args.extend(["--base-path", str(parsed.base_path)])
    if getattr(parsed, "output", None):
        args.extend(["--output", str(parsed.output)])
    return export_requirements.main(args)


def cmd_resources(parsed: argparse.Namespace) -> int:
    """Manage ASVS reference files, drift detection, AI context."""
    if getattr(parsed, "drift", False):
        from tools import drift_detector
        args = ["--format", parsed.format]
        if getattr(parsed, "offline", False):
            args.append("--offline")
        if getattr(parsed, "upstream_url", None):
            args.extend(["--upstream-url", parsed.upstream_url])
        if getattr(parsed, "base_path", None):
            args.extend(["--base-path", str(parsed.base_path)])
        return drift_detector.main(args)

    # List resources
    base_path = getattr(parsed, "base_path", None)
    if base_path:
        core = Path(base_path).resolve() / "01-ASVS-Core-Reference"
    else:
        # Use bundled data
        from tools.paths import _bundled_data_dir
        core = _bundled_data_dir()

    if not core.exists():
        print(f"ASVS reference not found at {core}", file=sys.stderr)
        return 1
    for f in sorted(core.glob("*.json")):
        if base_path:
            print(f"  {f.relative_to(Path(base_path).resolve())}")
        else:
            print(f"  {f.name}")
    return 0


def cmd_config(parsed: argparse.Namespace) -> int:
    """Manage LLM API keys and settings."""
    from tools.config import KademosConfig, VALID_KEYS

    console = Console()
    config = KademosConfig()
    action = getattr(parsed, "config_action", None)

    if action == "set":
        try:
            config.set(parsed.key, parsed.value)
            console.print(f"[green]✓[/green] Set [bold]{parsed.key}[/bold]")
            return 0
        except ValueError as e:
            print(f"Error: {e}", file=sys.stderr)
            return 1

    elif action == "get":
        try:
            value = config.get_effective(parsed.key)
            if value is None:
                console.print(f"[dim]{parsed.key}[/dim]: [italic]not set[/italic]")
            else:
                console.print(f"[bold]{parsed.key}[/bold]: {value}")
            return 0
        except ValueError as e:
            print(f"Error: {e}", file=sys.stderr)
            return 1

    elif action == "list":
        entries = config.list_all()
        table = Table(
            title="Kademos Configuration",
            box=box.SIMPLE_HEAVY,
            border_style="color(240)",
            header_style="bold color(141)",
            padding=(0, 2),
        )
        table.add_column("Key", style="bold white")
        table.add_column("Value", style="white")
        table.add_column("Source", style="dim")
        for key, entry in entries.items():
            display = entry["display"] or "[italic]not set[/italic]"
            table.add_row(key, display, entry["source"])
        console.print(table)
        return 0

    elif action == "reset":
        config.reset()
        console.print("[green]✓[/green] Configuration reset.")
        return 0

    else:
        # No subcommand — show help-style overview
        console.print("[bold]Kademos Config[/bold]")
        console.print()
        console.print("  kademos config list              Show all configuration")
        console.print("  kademos config set <key> <value> Set a configuration value")
        console.print("  kademos config get <key>         Get a configuration value")
        console.print("  kademos config reset             Reset all configuration")
        console.print()
        console.print("[dim]Valid keys:[/dim]")
        for key, desc in VALID_KEYS.items():
            console.print(f"  [bold]{key}[/bold]  {desc}")
        console.print()
        console.print("[dim]Environment variable overrides:[/dim]")
        console.print("  KADEMOS_OPENAI_KEY     → openai_api_key")
        console.print("  KADEMOS_ANTHROPIC_KEY  → anthropic_api_key")
        return 0


def create_parser() -> argparse.ArgumentParser:
    """Create the main argument parser with subcommands."""
    parser = argparse.ArgumentParser(
        prog="kademos",
        description="Kademos - Agentic AI Security Requirements Engine",
        epilog="Run 'kademos <command> --help' for command-specific help.",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {get_version()}")

    subparsers = parser.add_subparsers(dest="command", title="commands", metavar="<command>")

    # scan
    sp_scan = subparsers.add_parser("scan", help="Scan a repository to map context to ASVS requirements")
    sp_scan.add_argument("path", nargs="?", default=".", help="Repository path (default: current dir)")
    sp_scan.add_argument("--level", choices=["1", "2", "3"], default="2", help="ASVS level (default: 2)")
    sp_scan.add_argument("--format", choices=["markdown", "json"], default="markdown", help="Output format")
    sp_scan.add_argument("--ai-context", action="store_true", help="Output XML for AI agents")
    sp_scan.add_argument("--base-path", type=Path, help="Base path for ASVS reference files")
    sp_scan.set_defaults(func=cmd_scan)

    # interact
    sp_interact = subparsers.add_parser("interact", help="Interactive TUI for generating security requirements")
    sp_interact.add_argument("--output", type=Path, default=Path("SECURITY_REQUIREMENTS.md"), help="Output file")
    sp_interact.add_argument("--base-path", type=Path, help="Base path for ASVS reference files")
    sp_interact.set_defaults(func=cmd_interact)

    # threatmodel
    sp_tm = subparsers.add_parser("threatmodel", help="Generate scoped LLM prompts for STRIDE modeling")
    sp_tm.add_argument("--tech-stack", default="Web application", help="Tech stack description")
    sp_tm.add_argument("--output", type=Path, default=Path("threat_model_prompt.txt"), help="Output file")
    sp_tm.add_argument("--base-path", type=Path, help="Base path for ASVS reference files")
    sp_tm.set_defaults(func=cmd_threatmodel)

    # export
    sp_export = subparsers.add_parser("export", help="Export requirements to CSV/Jira JSON")
    sp_export.add_argument("--level", choices=["1", "2", "3"], default="2", help="ASVS level")
    sp_export.add_argument("--format", choices=["csv", "jira-json"], default="csv", help="Output format")
    sp_export.add_argument("--output", type=Path, help="Output file (default: stdout)")
    sp_export.add_argument("--base-path", type=Path, help="Base path for ASVS reference files")
    sp_export.set_defaults(func=cmd_export)

    # resources
    sp_res = subparsers.add_parser("resources", help="Manage ASVS reference files and drift detection")
    sp_res.add_argument("--drift", action="store_true", help="Check drift against upstream")
    sp_res.add_argument("--format", choices=["text", "json"], default="text", help="Output format")
    sp_res.add_argument("--offline", action="store_true", help="Skip upstream fetch")
    sp_res.add_argument("--upstream-url", type=str, help="URL to fetch upstream ASVS")
    sp_res.add_argument("--base-path", type=Path, help="Base path for ASVS reference files")
    sp_res.set_defaults(func=cmd_resources)

    # config
    sp_config = subparsers.add_parser("config", help="Manage LLM API keys and settings")
    config_sub = sp_config.add_subparsers(dest="config_action")

    sp_config_set = config_sub.add_parser("set", help="Set a configuration value")
    sp_config_set.add_argument("key", help="Configuration key")
    sp_config_set.add_argument("value", help="Value to set")

    sp_config_get = config_sub.add_parser("get", help="Get a configuration value")
    sp_config_get.add_argument("key", help="Configuration key")

    config_sub.add_parser("list", help="List all configuration")
    config_sub.add_parser("reset", help="Reset all configuration")

    sp_config.set_defaults(func=cmd_config)

    return parser


def main(args: Optional[List[str]] = None) -> int:
    """Main entry point for the unified CLI."""
    parser = create_parser()
    parsed = parser.parse_args(args)

    if not parsed.command:
        if args is None or len(sys.argv) == 1:
            show_splash(get_version())
            return 0
        parser.print_help()
        return 0

    try:
        return parsed.func(parsed)
    except KeyboardInterrupt:
        print("\nOperation cancelled.", file=sys.stderr)
        return 130
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
