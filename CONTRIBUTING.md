# Contributing to vCon 2026

Thank you for your interest in contributing. This repository contains vCon (Virtual Call Object Notation) conversation data and a Streamlit viewer for **vCon 2026**. The dataset models **utility outage reporting** (gas leak, power outage) with AI intake, caller ID verification, and technician ETA—no human dispatcher. The project centers on an **MCP (Model Context Protocol) server** that exposes vCon data so AI assistants and apps can store, search, tag, analyze, and build tools around conversations.

## Ways to Contribute

### 1. Code & Tooling

- **Improve the vCon viewer** (`vcon_viewer.py`)
  - Add search/filter by transcript content, summary, or conversation type
  - Add export (e.g., CSV/JSON of metadata and transcripts)
  - Improve accessibility and keyboard navigation
  - Add conversation-type tags or categories derived from summaries
- **MCP / API–oriented work**
  - Tools or plugins that consume the MCP server API (search, tag, analyze)
  - Demos that show AI assistants or voice bots using structured vCon data via MCP
  - Small apps that read vCon from the API and visualize or analyze it
- **Scripts and utilities**
  - Validation script to check vCon JSON schema and required fields
  - Batch export or transformation (e.g., all transcripts to a single corpus)
  - Scripts to compute simple analytics (duration distribution, party counts, etc.)

### 2. Data & Documentation

- **Documentation**
  - Expand README with vCon spec links, schema notes, or use cases
  - Add docstrings and type hints to `vcon_viewer.py`
  - Document the exact structure of `analysis[].body` (e.g., when it’s an object with `transcript`, `confidence`, `detected_language`)
- **Data quality**
  - Propose or implement a schema (e.g., JSON Schema) for the vCon files
  - Add a data dictionary or field-level documentation for parties, dialog, analysis

### 3. Analysis & Research

- **Analysis**
  - Summarize conversation types, sentiment, or resolution patterns
  - Contribute notebooks or scripts that analyze the dataset (with outputs documented or excluded per repo policy)
- **Use cases**
  - Document or prototype use cases: training, demos, compliance, QA, etc.

## Development Setup

```bash
# Clone the repository (if you haven’t already)
git clone <repo-url>
cd tadhack-2025   # or your clone path

# Create a virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate   # or .venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt

# Run the viewer
streamlit run vcon_viewer.py
```

## vCon Structure Quick Reference

- **Location**: One `.vcon.json` per conversation under day folders (`18/`, `19/`, … `24/`).
- **Key fields**: `uuid`, `vcon`, `created_at`, `parties`, `dialog`, `analysis`, `attachments`.
- **Analysis**: Array of objects with `type` (e.g. `transcript`, `summary`, `diarized`) and `body`. For `type: "transcript"`, `body` may be a string or an object (e.g. `{"transcript": "...", "confidence": 0.99, "detected_language": "en"}`).
- **Audio**: Referenced in `dialog[].url` and optional local `.mp3` next to the `.vcon.json` (same base name as UUID).

## Submitting Changes

1. Open an issue to discuss larger changes or new features.
2. Fork the repo and create a branch (`git checkout -b feature/your-feature`).
3. Make your changes; keep commits focused and messages clear.
4. Run the viewer and any scripts you add to ensure they work.
5. Push and open a pull request with a short description of what changed and why.

## Code Style

- Prefer clear, readable Python (PEP 8–style).
- Add type hints and docstrings for new or modified functions.
- No formal linter is required; consistency with the existing codebase is preferred.

## Questions

Open an issue for questions about the dataset, vCon format, or how to contribute.
