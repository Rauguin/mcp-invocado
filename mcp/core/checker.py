#!/usr/bin/env python3
from typing import List
from pathlib import Path
from urllib.parse import unquote
import re

def check_markdown(md_path: Path) -> List[str]:
    issues = []
    content = md_path.read_text(encoding="utf-8")
    if content.count("```") % 2 != 0:
        issues.append("❌ Unbalanced code blocks (``` mismatch)")
    if content.startswith("---") and content.count("---") < 2:
        issues.append("❌ YAML frontmatter not properly closed")
    return issues

def check_images(md_path: Path, base_dir: Path | None = None) -> List[str]:
    issues: List[str] = []
    content = md_path.read_text(encoding="utf-8")
    base_dir = base_dir or md_path.parent
    images = re.findall(r"!\[.*?\]\((.*?)\)", content)
    for img in images:
        img_ref = img.strip()
        img_ref = img_ref.strip("<>").strip()
        img_ref = unquote(img_ref)
        if img_ref.startswith(("http://", "https://")):
            continue
        img_path = (base_dir / img_ref).resolve()
        if not img_path.exists():
            issues.append(f"⚠ Image not found: {img_ref}")
    return issues
