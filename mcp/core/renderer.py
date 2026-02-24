#!/usr/bin/env python
import subprocess
from pathlib import Path

def render_markdown(
    input_md: Path,
    output_pdf: Path,
    latex_template: Path,
    ):
    cmd = [
        "pandoc",
        str(input_md),
        "-o", str(output_pdf),
        "--from", "markdown",
        "--template", str(latex_template),
        "--pdf-engine", "xelatex",
        "--listings",
        "--toc",
        "--toc-depth=4",
        "--number-sections",
    ]
    print("[...] Rendering PDF with pandoc...")
    try:
        subprocess.run(["pandoc", "--version"], capture_output=True, text=True)
    except FileNotFoundError:
        print("[-] 'pandoc' not found in PATH. Install: sudo apt install pandoc")
        return False
    try:
        subprocess.run(["xelatex", "--version"], capture_output=True, text=True)
    except FileNotFoundError:
        print("[-] 'xelatex' not found in PATH. Install: sudo apt install texlive-xetex")
        return False
    try:
        result = subprocess.run(cmd, cwd=str(input_md.parent))
    except FileNotFoundError as e:
        print(f"[-] Failed to execute: {e}")
        return False
    except Exception as e:
        print(f"[-] Unexpected error while rendering: {e}")
        return False
    if result.returncode != 0:
        print("[-] Pandoc rendering failed.")
        return False
    print(f"[+] PDF generated: {output_pdf}")
    return True
