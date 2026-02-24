# MCP Invocado

**MCP Invocado** is a Mini Community Project (MCP) created for the Offensive Security community to help **create, validate, normalize, translate, and render technical reports** from Markdown sources into **submission-ready PDFs**.

The project addresses a common and recurring problem:
turning scattered notes, lab write-ups, and findings into **clean, standardized, and professional reports**, especially for **OffSec practical certifications** (OSWE, OSCP, OSEP), while remaining fully reusable for **professional pentest reports**.

---

## 🎯 What It Does

MCP Invocado provides a terminal-based workflow that allows you to:

- Write reports in **pure Markdown**
- Start from **standardized templates** (OSWE-style by default)
- Import Markdown exported from **Notion, Obsidian, or similar tools**
- Automatically handle `.zip` exports (Markdown + images)
- Normalize Markdown (images, paths, syntax differences)
- Validate content before rendering (code blocks, images, structure)
- Protect critical sections from accidental modification
- Translate reports to **technical English** (optional, AI-assisted)
- Generate **final PDFs using Pandoc + LaTeX**
- Work **offline-first**, with optional AI integration

The Markdown file is always the **single source of truth**.

---

## 👥 Who It Helps

This project is designed for:

- OffSec students (OSWE, OSCP, OSEP, etc.)
- Candidates preparing certification reports
- People writing lab, CTF, or training reports
- Professionals producing repetitive pentest documentation
- International candidates required to submit reports in English

The goal is to **reduce reporting friction**, not to replace technical skill.

---

## 🤖 How AI Is Used

AI assists documentation quality only and operates strictly within formatting and translation boundaries.

It may be used for:
- Translating reports (e.g., PT → EN)
- Improving clarity in narrative sections
- Ensuring language consistency while preserving Markdown structure

AI is **never** used to:
- Generate exploits or payloads
- Perform attacks or interact with targets
- Make technical decisions
- Automate hacking activities

AI assists **documentation quality only**.

Supported engines:
- `none` (default, fully offline)
- `openai` (API-based)
- `llama` (local, via llama-cpp)

---

## 🧱 Core Concepts

### 🔒 Protected Sections

MCP Invocado supports **protected sections** inside Markdown files.

These sections:
- Are excluded from translation
- Are preserved during normalization
- Prevent accidental modification of mandatory report content

They are especially useful for:
- Fixed report structure
- Examiner-required sections
- Boilerplate text

---

### 📝 Markdown as Single Source of Truth

Reports are authored once and can be rendered into:
- PDF (Pandoc + LaTeX)
- HTML
- DOCX (Pandoc)

The tool is editor-agnostic and compatible with:
- Notion
- Obsidian
- VS Code
- Any Markdown editor

---

## 🧪 Validation & Normalization

Before rendering, MCP Invocado can:

- Accept `.md` or `.zip` inputs
- Extract ZIP exports automatically
- Detect and normalize image paths
- Convert Obsidian-style image syntax
- Validate:
  - Balanced code blocks
  - YAML frontmatter
  - Image existence
  - Basic Pandoc compatibility

This reduces last-minute render failures.

---

## 📂 Project Structure

```
MCP_Invocado/
├── mcp/
│ ├── cli.py
│ ├── core/
│ │ ├── checker.py
│ │ ├── normalizer.py
│ │ ├── parser.py
│ │ ├── pipeline.py
│ │ ├── renderer.py
│ │ └── translator.py
│ ├── templates/
│ │ └── oswe.tex
│ ├── assets/
│ │ └── offsec.png
│ └── utils/
│ └── checks.py
├── README.md
├── pyproject.toml
└── Dockerfile
```

---

## ⚙️ Example Usage

### Initialize a new report

```bash
mcp init --template oswe --output report.md

Validate input
mcp check report.md

Render without translation
mcp render report.md

Render ZIP export (Notion)
mcp render export.zip

Render with translation using OpenAI API
mcp render report.md \
  --engine openai \
  --openai-api-key YOUR_API_KEY \
  --lang en

Render with local LLaMA model
mcp render report.md \
  --engine llama \
  --llama-model /path/to/model.gguf \
  --lang en
```

---

## 📌 Ethics & Scope

MCP Invocado follows Offensive Security community guidelines:

- Safe-for-work (SFW) content only
- No automation of exploitation
- No assistance in bypassing exam rules
- Documentation support only

This tool exists to **help you explain what you already know**.

---

## 🌍 Language / Idioma

### 🇺🇸 English
Primary language for reports and documentation.

### 🇧🇷 Português
O MCP Invocado pode ser usado para escrever relatórios em português e traduzi-los para inglês técnico, mantendo estrutura, imagens e formatação.

---

## 🧪 Tested Environments

MCP Invocado has been tested successfully with:

- ✅ VS Code (Markdown + images in directory)
- ✅ Notion Markdown ZIP export
- ✅ Direct `.md` files
- ✅ Translation from Portuguese (BR) to English (EN) using OpenAI API
- ✅ Python virtual environment (`.venv`)
- ✅ Pandoc + XeLaTeX rendering pipeline

The following scenario has been validated:

Notion → Export ZIP → `mcp render export.zip` → PDF generated successfully.

---

## 🐍 Running with Virtual Environment (Recommended for Development)

Using a Python virtual environment keeps dependencies isolated and avoids system-wide conflicts.

### Create and activate virtual environment

```bash
python -m venv .venv
source .venv/bin/activate   # Linux / macOS
# .venv\Scripts\activate    # Windows
Install the project locally
pip install .
```

Optional engine support:
```bash
pip install ".[openai]"
pip install ".[llama]"
Run MCP
mcp render report.md
```

To deactivate the environment:
```bash
deactivate
```

🐳 Running with Docker (Portable & Clean Execution)

Docker allows MCP Invocado to run in a fully isolated environment, without installing dependencies globally.

```bash
Build the image
docker build -t mcp-invocado .
Render a report
docker run --rm -v "$PWD:/work" -w /work \
  mcp-invocado render report.md
Render with OpenAI translation
docker run --rm -v "$PWD:/work" -w /work \
  mcp-invocado render report.md \
  --engine openai \
  --openai-api-key YOUR_API_KEY \
  --lang en
Render a Notion ZIP export
docker run --rm -v "$PWD:/work" -w /work \
  mcp-invocado render export.zip
```

Docker is recommended for:

- Clean execution environments

- CI/CD usage

- Reproducible builds

- Avoiding local Pandoc/LaTeX dependency issues

---

## 🏁 Status

This project is under active development as part of an OffSec MCP community challenge.

Feedback and contributions are welcome.
