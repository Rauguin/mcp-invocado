#!/usr/bin/env python
import re
from pathlib import Path

PROTECTED_BLOCK_PATTERN = re.compile(
    r"```LOCKED(.*?)```",
    re.DOTALL | re.IGNORECASE
)
def extract_protected_blocks(markdown_text: str):
    protected = PROTECTED_BLOCK_PATTERN.findall(markdown_text)
    cleaned = PROTECTED_BLOCK_PATTERN.sub(
        "\n> [*] Protected section removed\n",
        markdown_text
    )
    return protected, cleaned

def parse_markdown(path: Path):
    content = path.read_text(encoding="utf-8")
    protected, cleaned = extract_protected_blocks(content)

    return {
        "raw": content,
        "cleaned": cleaned,
        "protected_blocks": protected
    }
