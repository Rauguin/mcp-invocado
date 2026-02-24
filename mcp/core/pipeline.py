#!/usr/bin/env python
from pathlib import Path
import zipfile
import shutil

def ensure_offsec_logo(workdir: Path) -> None:
    template_logo = Path(__file__).parent.parent / "templates" / "images" / "offsec.png"
    if not template_logo.exists():
        raise RuntimeError(f"Template logo not found: {template_logo}")
    shutil.copy(template_logo, workdir / "offsec.png")

def prepare_pipeline_input(input_path: Path) -> Path:
    if input_path.suffix.lower() == ".zip":
        md_path = _extract_zip(input_path)
        ensure_offsec_logo(md_path.parent)
        return md_path
    if input_path.suffix.lower() in {".md", ".markdown"}:
        ensure_offsec_logo(input_path.parent)
        return input_path
    raise RuntimeError("Unsupported input format. Use .md or .zip")

def _extract_zip(zip_path: Path) -> Path:
    extract_dir = zip_path.parent / f".mcp_extract_{zip_path.stem}"
    if extract_dir.exists():
        shutil.rmtree(extract_dir)
    extract_dir.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(zip_path) as z:
        z.extractall(extract_dir)
    md_files = [p for p in extract_dir.rglob("*.md") if p.is_file()]
    if not md_files:
        raise RuntimeError("No Markdown file found in ZIP")
    stem_match = [p for p in md_files if p.stem == zip_path.stem]
    candidates = stem_match if stem_match else md_files
    min_depth = min(len(p.relative_to(extract_dir).parts) for p in candidates)
    shallow = [p for p in candidates if len(p.relative_to(extract_dir).parts) == min_depth]
    md_path = max(shallow, key=lambda p: p.stat().st_size)
    ensure_offsec_logo(md_path.parent)
    return md_path
