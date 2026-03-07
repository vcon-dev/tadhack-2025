# TADHack 2026 submission guide

Use this repo as your **TADHack 2026** submission. Below: what you have, what to submit, how to demo, and a short pitch.

---

## What you have

| Item | Description |
|------|-------------|
| **vCon dataset** | 911 calls (3 vCons in `911_calls/`) and scripts to generate utility outage vCons (gas leak, power outage, AI intake). All synthetic. |
| **Viewer** | Streamlit app to browse vCons, read transcripts/summaries, and **play TTS audio** (audible speech from transcripts). |
| **Scripts** | Generate more 911 or utility outage vCons; generate silent or TTS `.mp3`; load into vcon-mcp. |
| **MCP integration** | README explains how to use [vcon-mcp](https://github.com/vcon-dev/vcon-mcp) with this data. **Demo script** `scripts/demo_mcp_consume.py` ingests this repo’s vCons into vcon-mcp (REST API) and then lists/gets a vCon to show the data being consumed. |
| **Reference docs** | REFERENCE.md, reference/vcon-2026-reference.json for vCon 2026 and citation. |

---

## Submission checklist

- [ ] **Repo is public** (or shared with TADHack / judges if required).
- [ ] **README** is clear: project name, TADHack 2026, what it does, how to run the viewer (see “Quick demo” in README).
- [ ] **Demo works:** `pip install -r requirements.txt` and `python3 -m streamlit run vcon_viewer.py` run without errors; at least one folder (e.g. `911_calls/`) has `.vcon.json` and optionally `.mp3` so the viewer and audio work.
- [ ] **Submission form:** Enter your **repository URL** (and any other links—e.g. short video—if the hackathon asks).
- [ ] **Optional:** Show **data consumed by MCP server**: run vcon-mcp in HTTP mode, then `python3 scripts/demo_mcp_consume.py` to ingest and consume vCons (see README).
- [ ] **Optional:** Record a 1–2 minute screen demo (viewer + play audio + MCP consume script or AI search) and add the link in the README or submission form.

---

## Demo script (for live or video)

**0:00–0:20** – “This is a TADHack 2026 submission: a vCon 2026 reference dataset and viewer for MCP + vCon. vCon is a standard for conversation data; MCP lets AI assistants work with that data.”

**0:20–0:50** – Open the viewer. “Here are 911-style and utility-outage vCons. I’ll pick one.” Open a conversation, scroll to the transcript and diarization (Dispatcher / Caller or AI / Caller). “I’ll play the audio.” Click play on the TTS audio. “The audio is generated from the transcript with TTS so we can demo without real recordings.”

**0:50–1:25** – “To show this data being consumed by the MCP server, we run vcon-mcp in HTTP mode and then a demo script from this repo.” Run: `python3 scripts/demo_mcp_consume.py`. “It posts our 911 vCons to the MCP server’s REST API, then lists and fetches one vCon—so you see the same data now stored and served by the MCP server. An AI assistant connected via MCP can then search or analyze these vCons.”

**1:25–1:40** – “So we’re showing: vCon as a portable format, a reference dataset, a viewer with TTS audio, and this data being consumed by the vcon-mcp MCP server—ingest via REST, then list/get so the MCP server is the source of truth for AI tools.” End with repo link and thank you.

---

## One-line pitch

**“A vCon 2026 reference dataset (911 + utility outage scenarios) with a Streamlit viewer and TTS audio, ready to use with the vcon-mcp MCP server for AI-powered search and analysis.”**

---

## If judges ask

- **Where is the MCP server?** We use the existing [vcon-mcp](https://github.com/vcon-dev/vcon-mcp) server; this repo provides the **data and viewer**. You can load our vCons into vcon-mcp via `load:local` or the REST API (see README).
- **Why synthetic data?** Safe for demos and sharing; no real PII or emergency calls. Same vCon structure as production.
- **What’s the utility outage scenario?** Callers report gas leak or power outage; an AI virtual assistant does intake, verifies address via caller ID, and gives technician ETA—no human dispatcher. Scripts in `scripts/generate_utility_outage_vcons.py` and README.

Good luck at TADHack 2026.
