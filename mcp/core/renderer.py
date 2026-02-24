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
    result = subprocess.run(
        cmd,
        cwd=str(input_md.parent)
    )
    if result.returncode != 0:
        print("[-] Pandoc rendering failed.")
        return False
    print(f"[+] PDF generated: {output_pdf}")
    return True
