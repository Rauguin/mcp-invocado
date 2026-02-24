#!/usr/bin/env python3
import os
import shutil
import importlib
from pathlib import Path

def check_xelatex():
    if not shutil.which("xelatex"):
        raise RuntimeError(
            "XeLaTeX not found. Install it:\n"
            "  sudo apt install texlive-xetex"
        )

def check_file_exists(path: Path, label: str = "File"):
    if not path.exists():
        raise RuntimeError(f"{label} not found: {path}")

def check_pandoc():
    if not shutil.which("pandoc"):
        raise RuntimeError(
            "Pandoc not found. Please install it:\n"
            "  sudo apt install pandoc texlive-fonts-extra"
        )

def check_engine_requirements(engine: str):
    if engine == "none":
        return
    if engine == "openai":
        _check_openai()
    elif engine == "llama":
        _check_llama()
    else:
        raise RuntimeError(f"Unknown engine: {engine}")

def _check_openai():
    _check_library("openai")
    _check_env("OPENAI_API_KEY")

def _check_llama():
    _check_library("llama_cpp")
    _check_env("LLAMA_MODEL_PATH")

def _check_library(module_name: str):
    try:
        importlib.import_module(module_name)
    except ImportError:
        raise RuntimeError(
            f"Required library '{module_name}' is not installed.\n"
            f"Install it with: pip install {module_name.replace('_', '-')}"
        )

def _check_env(var_name: str):
    if not os.getenv(var_name):
        raise RuntimeError(
            f"Environment variable '{var_name}' is not set.\n"
            f"Export it before running the command."
        )
