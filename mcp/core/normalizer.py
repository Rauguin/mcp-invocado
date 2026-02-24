#!/usr/bin/env python3
import re
import zipfile
from pathlib import Path
from typing import Tuple
import urllib.parse
from urllib.parse import unquote

IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".gif", ".webp"}
IMG_MD_PATTERN = re.compile(r'!\[([^\]]*)\]\(([^)]+)\)')
def _clean_img_target(target: str) -> str:
    t = target.strip()
    if t.startswith("<") and t.endswith(">"):
        t = t[1:-1].strip()
    t = urllib.parse.unquote(t)
    t = t.replace("\\", "/")
    return t

def normalize_image_links(md: str) -> str:
    def repl(m):
        alt = m.group(1)
        target = m.group(2)
        fixed = _clean_img_target(target)
        return f"![{alt}]({fixed})"
    return IMG_MD_PATTERN.sub(repl, md)

def normalize_percent_encoded_image_paths(md: str) -> str:
    def repl(match):
        path = match.group(1).strip()
        if path.startswith("http://") or path.startswith("https://"):
            return match.group(0)
        decoded = unquote(path)
        return match.group(0).replace(path, decoded)
    return re.sub(r"!\[.*?\]\((.*?)\)", repl, md)

def extract_zip_if_needed(input_path: Path) -> Path:
    if input_path.suffix.lower() != ".zip":
        return input_path
    extract_dir = input_path.with_suffix("")
    extract_dir.mkdir(exist_ok=True)
    with zipfile.ZipFile(input_path, "r") as z:
        z.extractall(extract_dir)
    md_files = list(extract_dir.glob("*.md"))
    if not md_files:
        raise RuntimeError("ZIP does not contain a markdown file")
    return md_files[0]

def detect_assets_dir(base_dir: Path) -> Path | None:
    for p in base_dir.iterdir():
        if p.is_dir():
            for f in p.iterdir():
                if f.suffix.lower() in IMAGE_EXTENSIONS:
                    return p
    return None

def normalize_obsidian_images(md: str, assets_dir: Path) -> str:
    def repl(match):
        img = match.group(1)
        return f"![{img}]({assets_dir.name}/{img})"
    return re.sub(r"!\[\[(.*?)\]\]", repl, md)

def normalize_notion_frontmatter(md: str) -> str:
    lines = md.splitlines()
    if len(lines) < 6:
        return md
    if not lines[0].startswith("# "):
        return md
    sep_idx = None
    for i in range(1, min(len(lines), 15)):
        if lines[i].strip() == "---":
            sep_idx = i
            break
    if sep_idx is None:
        return md
    fm_lines = []
    i = sep_idx + 1
    while i < len(lines):
        line = lines[i].rstrip()
        if line.strip() == "":
            if i + 1 < len(lines) and lines[i + 1].lstrip().startswith("#"):
                break
            i += 1
            continue
        if line.lstrip().startswith("## "):
            candidate = line.lstrip()[3:]
        else:
            candidate = line
        if ":" in candidate and not candidate.lstrip().startswith("http"):
            fm_lines.append(candidate.strip())
            i += 1
            continue
        break
    if not fm_lines:
        return md
    title_heading = lines[0]
    rest_start = i
    rest = "\n".join([title_heading] + lines[rest_start:]).lstrip("\n")
    frontmatter = "---\n" + "\n".join(fm_lines) + "\n---\n\n"
    return frontmatter + rest

def normalize_image_paths(md: str, base_dir: Path) -> str:
    assets_dir = detect_assets_dir(base_dir)
    if assets_dir:
        md = normalize_obsidian_images(md, assets_dir)
    md = normalize_percent_encoded_image_paths(md)
    return md

def normalize_markdown(input_md: Path) -> Tuple[Path, str]:
    content = input_md.read_text(encoding="utf-8", errors="replace")
    content = normalize_notion_frontmatter(content)
    normalized = normalize_image_links(content)
    normalized = normalize_image_paths(content, input_md.parent)
    return input_md, normalized

