#!/usr/bin/env python3
import argparse
import sys
from pathlib import Path
import textwrap
import os
from mcp.core.parser import parse_markdown
from mcp.core.translator import translate_markdown
from mcp.core.renderer import render_markdown

def cmd_init(args):
    template_dir = Path(__file__).parent / "templates" / args.template
    output_file = Path(args.output)
    if not template_dir.exists():
        print(f"❌ Template '{args.template}' not found.")
        sys.exit(1)
    template_file = template_dir / "report.md"
    if not template_file.exists():
        print(f"""
    ❌ Template '{args.template}' is incomplete.

    Expected file:
    {template_file}

    Available templates:
    - oswe

    Try:
    mcp init --template oswe
    """)
        sys.exit(1)
    if output_file.exists():
        print(f"❌ File '{output_file}' already exists.")
        sys.exit(1)
    output_file.write_text(template_file.read_text(), encoding="utf-8")
    print(f"✅ Report created: {output_file}")

def cmd_render(args):
    from mcp.core.pipeline import prepare_pipeline_input
    from mcp.core.normalizer import normalize_markdown
    from mcp.core.checker import check_markdown, check_images
    from mcp.utils.checks import check_pandoc, check_engine_requirements
    if not args.input:
        print("❌ Missing input.\n")
        print("Usage:")
        print("  mcp render <report.md|report.zip> [options]\n")
        print("Examples:")
        print("  mcp render report.md")
        print("  mcp render report.zip")
        print("  mcp render report.md --engine llama --lang en")
        print("  mcp render report.zip --strict")
        print("\nTip:")
        print("  Use 'mcp templates' to list available internal templates.")
        sys.exit(1)
    try:
        md_path = prepare_pipeline_input(Path(args.input).resolve())
    except Exception as e:
        print("❌ Input is not valid for MCP render.")
        print(f"   Reason: {e}")
        print("Examples:")
        print("  mcp render report.md --template oswe")
        print("  mcp render report.zip --template oswe")
        sys.exit(1)
    if getattr(args, "openai_api_key", None):
        os.environ["OPENAI_API_KEY"] = args.openai_api_key
    if getattr(args, "llama_model", None):
        os.environ["LLAMA_MODEL_PATH"] = args.llama_model
    if getattr(args, "openai_api_key", None) and args.engine != "openai":
        print("⚠ --openai-api-key provided but engine is not 'openai' (it will be ignored by the translator).")
    if getattr(args, "llama_model", None) and args.engine != "llama":
        print("⚠ --llama-model provided but engine is not 'llama' (it will be ignored by the translator).")
    check_pandoc()
    check_engine_requirements(args.engine)
    if not args.template and not args.template_path:
        print("❌ You must specify --template or --template-path")
        sys.exit(1)
    if args.template and args.template_path:
        print("❌ Use either --template OR --template-path, not both")
        sys.exit(1)
    if args.template_path:
        latex_template = Path(args.template_path).resolve()
    else:
        latex_template = (
            Path(__file__).parent
            / "templates"
            / args.template
            / "offsec.latex"
        )
    if not latex_template.exists():
        print(f"❌ LaTeX template not found: {latex_template}")
        sys.exit(1)
    md_path = prepare_pipeline_input(Path(args.input).resolve())
    output_pdf = Path(args.output).resolve()
    issues = check_markdown(md_path) + check_images(md_path)
    if issues:
        print("⚠ Issues detected:")
        for i in issues:
            print(" ", i)
        if args.strict:
            print("❌ Strict mode enabled. Aborting.")
            sys.exit(1)
    md_path, normalized = normalize_markdown(md_path)
    parsed = parse_markdown(md_path)
    translated = translate_markdown(
        parsed["cleaned"],
        target_language=args.lang,
        engine=args.engine,
    )
    old_cwd = Path.cwd()
    try:
        os.chdir(md_path.parent)
        temp_md = md_path.parent / ".mcp_render.md"
        temp_md.write_text(translated, encoding="utf-8")
        success = render_markdown(
            input_md=temp_md,
            output_pdf=output_pdf,
            latex_template=latex_template,
        )
    finally:
        try:
            temp_md.unlink(missing_ok=True)
        except Exception:
            pass
        os.chdir(old_cwd)
    if not success:
        sys.exit(1)

def cmd_check(args):
    from mcp.core.pipeline import prepare_pipeline_input
    from mcp.core.checker import check_markdown, check_images
    if not args.input:
        print("❌ Missing input.\n")
        print("Usage:")
        print("  mcp check <report.md|report.zip> [--strict]\n")
        print("Examples:")
        print("  mcp check report.md")
        print("  mcp check report.zip")
        print("  mcp check report.zip --strict")
        sys.exit(1)
    input_path = Path(args.input).resolve()
    try:
        md_path = prepare_pipeline_input(input_path)
    except Exception as e:
        print("❌ Input is not valid for MCP check.")
        print(f"   Reason: {e}")
        print("")
        print("Expected:")
        print("  - A Markdown file:  report.md")
        print("  - A ZIP export:     report.zip (must contain a .md + images folder)")
        print("")
        print("Examples:")
        print("  mcp check report.md")
        print("  mcp check report.zip")
        sys.exit(1)
    issues = check_markdown(md_path) + check_images(md_path)
    if not issues:
        print("✅ No issues found. Markdown is safe for rendering.")
        return
    print(f"⚠ Issues detected ({len(issues)}):")
    for i in issues:
        print(" ", i)
    if issues and not args.strict:
        print("\nℹ Continuing (not strict). Pandoc will replace missing images with descriptions.\n")
    print("")
    print("ℹ Tip: Fix the issues above. If you want MCP to fail on warnings, use --strict.")
    if args.strict:
        print("❌ Strict mode enabled. Validation failed.")
        sys.exit(1)

def cmd_templates(args):
    templates_dir = Path(__file__).parent / "templates"
    names = sorted([p.name for p in templates_dir.iterdir() if p.is_dir()])
    print("Available templates:")
    for n in names:
        print(f"  - {n}")
    print("\nUse:")
    print("  mcp render report.md --template <name>")
    print("Or external LaTeX template:")
    print("  mcp render report.md --template-path /path/custom.latex")

def main():
    parser = argparse.ArgumentParser(
        prog="mcp",
        description="MCP Invocado - Markdown-based reporting toolkit",
        epilog = textwrap.dedent("""\
            Examples:
            mcp init
            mcp templates
            mcp check report.zip
            mcp render report.md
            mcp render report.md --engine llama --lang en
            mcp check report.zip --strict

            Translation engines:
            none   (default)
            llama  (local, requires LLAMA_MODEL_PATH or --llama-model)
            openai (requires OPENAI_API_KEY or --openai-api-key)

            Strict mode:
            --strict  Fail if issues are detected (missing images, broken fences, etc.)
            """),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    subparsers = parser.add_subparsers(dest="command")
    init_parser = subparsers.add_parser(
        "init", help="Create a new report from a template"
    )
    init_parser.add_argument(
        "--template",
        default="oswe",
        help="Template name (default: oswe)"
    )
    init_parser.add_argument(
        "--output",
        default="report.md",
        help="Output markdown file"
    )
    init_parser.set_defaults(func=cmd_init)
    render_parser = subparsers.add_parser(
        "render", help="Render Markdown report to PDF"
    )
    render_parser.add_argument(
        "input",
        nargs="?",
        help="Markdown (.md) or Notion export (.zip)"
    )
    render_parser.add_argument(
        "--output",
        default="report.pdf",
        help="Output PDF file"
    )
    render_parser.add_argument(
        "--engine",
        choices=["none", "openai", "llama"],
        default="none",
        help="Translation engine (default: none)"
    )
    render_parser.add_argument(
        "--openai-api-key",
        dest="openai_api_key",
        help="OpenAI API key (only used when --engine openai). Overrides OPENAI_API_KEY."
    )
    render_parser.add_argument(
        "--llama-model",
        dest="llama_model",
        help="Path to local GGUF model (only used when --engine llama). Overrides LLAMA_MODEL_PATH."
    )
    render_parser.add_argument(
        "--lang",
        default="en",
        help="Target language (default: en)"
    )
    render_parser.add_argument(
        "--strict",
        action="store_true",
        help="Abort rendering if issues are detected (recommended for final PDF)"
    )
    render_parser.add_argument(
        "--template",
        default="oswe",
        help="Internal template name (default: oswe)"
    )
    render_parser.add_argument(
        "--template-path",
        help="Path to external LaTeX template"
    )
    render_parser.set_defaults(func=cmd_render)
    check_parser = subparsers.add_parser(
    "check", help="Validate markdown or zip input"
    )
    check_parser.add_argument(
        "input",
        nargs="?",
        help="Markdown or ZIP file to validate"
    )

    check_parser.add_argument(
        "--strict",
        action="store_true",
        help="Fail if issues are found (recommended for final submission)"
    )
    check_parser.set_defaults(func=cmd_check)
    templates_parser = subparsers.add_parser(
        "templates", help="List available internal templates"
    )
    templates_parser.set_defaults(func=cmd_templates)
    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(1)
    args.func(args)

if __name__ == "__main__":
    main()
