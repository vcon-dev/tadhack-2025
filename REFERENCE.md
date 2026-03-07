# Reference Dataset for vCon 2026

This repository is published as a **reference dataset** for the vCon ecosystem and for **vCon 2026** (specification, tooling, MCP servers, and events). Use it to validate implementations, build demos, or develop search/tag/analyze tools against a known vCon structure.

**Disclaimer:** The data in this repository is **synthetic** (generated for reference and demos). It does not represent real customers, utilities, or emergency calls. Use only for format validation, tooling, and demonstrations.

## Purpose

- **Spec & tooling**: Example vCon 0.0.1 payloads for **utility outage reports** (gas leak, power outage) with AI intake, address verification via caller ID, and technician ETA—no human dispatcher.
- **MCP / APIs**: Reference data for servers that expose vCon via MCP; use this dataset to test store/search/tag/analyze flows.
- **Demos & docs**: Ready-made conversations for AI-handled utility intake, caller ID verification, and ETA flows for tutorials, hackathons, and MCP demos.

## Dataset summary

| Field | Value |
|-------|--------|
| **Name** | vCon 2026 – Utility Outage Reports (AI intake) |
| **vCon version** | 0.0.1 |
| **Conversation count** | 42 |
| **Date range** | 2025-05-18 to 2025-05-24 (days 18–24 in folder names) |
| **Domain** | Utility outage reporting (gas leak, power outage); AI virtual assistant, no human dispatcher |
| **Structure** | One `.vcon.json` per conversation; audio referenced by URL (optional local `.mp3`) |

## How to use as reference

1. **Clone or link this repo** when documenting vCon 2026, building MCP servers, or writing tutorials.
2. **Point tooling at the layout**: day folders `18/`–`24/`, each containing `*.vcon.json` (and optionally same-named `.mp3`).
3. **Use the manifest**: Machine-readable metadata is in `reference/vcon-2026-reference.json` for automation or catalogs.
4. **Run the viewer**: `streamlit run vcon_viewer.py` to inspect conversations and confirm structure.

## Citation / attribution

When referencing this dataset (e.g. in vCon 2026 docs, tools, or papers):

- **Title**: vCon 2026 – Utility outage report conversations (AI intake, caller ID verification, technician ETA)  
- **Role**: Reference vCon dataset for vCon 2026  
- **Repo**: (use this repository URL)  
- **vCon version**: 0.0.1  

## Manifest

See **`reference/vcon-2026-reference.json`** for a machine-readable manifest (name, version, counts, date range, layout, vCon structure, citation). Tooling and catalogs can consume this file to discover and validate the reference dataset.
