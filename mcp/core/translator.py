#!/usr/bin/env python
import os
from typing import Literal, Optional

ENGINE_TYPES = Literal["none", "openai", "llama"]
def translate_markdown(
    markdown_text: str,
    target_language: str = "en",
    engine: ENGINE_TYPES = "none",
) -> str:
    if engine == "none":
        return markdown_text
    if engine == "openai":
        return _translate_openai(markdown_text, target_language)
    if engine == "llama":
        return _translate_llama(markdown_text, target_language)
    raise ValueError(f"Unknown translation engine: {engine}")

def _translate_openai(text: str, lang: str) -> str:
    try:
        from openai import OpenAI
    except ImportError:
        raise RuntimeError("openai package not installed")
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY not set")
    client = OpenAI(api_key=api_key)
    prompt = (
        f"Translate the following Markdown to {lang}. "
        "Preserve all Markdown formatting. "
        "Do not add explanations.\n\n"
        f"{text}"
    )
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
    )
    return response.choices[0].message.content.strip()

def _translate_llama(text: str, lang: str) -> str:
    try:
        from llama_cpp import Llama
    except ImportError:
        raise RuntimeError("llama-cpp-python not installed")
    model_path = os.getenv("LLAMA_MODEL_PATH")
    if not model_path:
        raise RuntimeError("LLAMA_MODEL_PATH not set")
    llm = Llama(
        model_path=model_path,
        n_ctx=4096,
        verbose=False,
    )
    prompt = (
        f"Translate the following Markdown to {lang}. "
        "Preserve formatting.\n\n"
        f"{text}"
    )
    output = llm(prompt, max_tokens=4096)
    return output["choices"][0]["text"].strip()