# vCon 2026 - Utility Outage Reports (AI Intake)

This repository contains **utility outage report** conversation data in vCon (Virtual Call Object Notation) format for **vCon 2026**. The scenario: callers report **gas leaks** or **power outages**; an **AI virtual assistant** handles intake, verifies the caller’s address via caller ID, and provides **real-time technician ETA**—no human dispatcher. Conversations span May 18–24, 2025.

> **Disclaimer:** All conversation data in this repository is **synthetic** (generated for demos and reference). It is not from real customers, utilities, or emergency calls. Do not use it for production systems, training on real user data, or any purpose that assumes real identities or events. Use only for vCon format validation, MCP tooling, and hackathon demos.

## TADHack 2026 submission

This repo is a **TADHack 2026** submission: a vCon 2026 reference dataset and tooling for **MCP + vCon** (store, search, tag, analyze conversations with AI).

### What to submit

- **This repository** (GitHub URL) as your submission link.
- **Demo:** Run the viewer and optionally vcon-mcp; show 911 or utility-outage vCons, play TTS audio, and (if you use vcon-mcp) show an AI assistant searching vCons via MCP.

### Quick demo (2–3 minutes)

1. **Clone and run the viewer**
   ```bash
   git clone <your-repo-url> && cd tadhack-2025
   pip install -r requirements.txt
   python3 -m streamlit run vcon_viewer.py
   ```
2. **Show the data:** Open the viewer → select a conversation from **911_calls** → show metadata, transcript, diarization (Dispatcher / Caller), and **play the TTS audio**.
3. **Show data consumed by MCP server:** With [vcon-mcp](https://github.com/vcon-dev/vcon-mcp) running in HTTP mode, run `python3 scripts/demo_mcp_consume.py` from this repo. The script ingests 911_calls vCons into the MCP server via the REST API, then lists and fetches one vCon to show the data being consumed. Optionally connect Cursor/Claude to vcon-mcp and ask the AI to search or get a vCon.

### Pitch angles for judges

- **vCon as “PDF for conversations”:** Standard format for voice, transcripts, and AI analysis; this repo provides a reference dataset (911 + utility outage scenarios) for vCon 2026.
- **MCP + vCon:** AI assistants can plug into conversation data via the vcon-mcp server—search, tag, add analysis—without custom integrations.
- **Use case:** Utility outage reporting (gas leak, power outage) with AI intake, caller ID verification, and technician ETA; plus 911-style calls. All synthetic for safe demos.

See **[SUBMISSION.md](SUBMISSION.md)** for a submission checklist and detailed demo script.

## Hackathon context: MCP + vCon

This hackathon revolves around a **server using MCP (Model Context Protocol)** — a way for AI assistants and developers to plug into structured conversation data stored in vCon format. You can:

- **Store** conversations (vCon)
- **Search** them
- **Tag** them
- **Analyze** them
- **Build tools** around them (apps, plugins, AI helpers)

Think of it as a standardized API + conversation storage layer so different services (and AI) can work with human conversations the same way. This repo provides the **vCon dataset**; the hackathon focus is building on top of the MCP server (voice bots, analytics, tools that consume the API).

## Using vCon MCP with this repo

The **[vcon-mcp](https://github.com/vcon-dev/vcon-mcp)** server is an MCP server for storing, searching, tagging, and analyzing vCon data. AI assistants (e.g. Claude, Cursor) can use it to work with your conversations via tools like `create_vcon`, `search_vcons`, `add_analysis`, and semantic search.

### 1. Set up vcon-mcp

```bash
# Clone and install (Node.js 18+)
git clone https://github.com/vcon-dev/vcon-mcp.git
cd vcon-mcp
npm install

# Copy env and add your Supabase credentials (sign up free at supabase.com)
cp .env.example .env
# Edit .env: SUPABASE_URL, SUPABASE_ANON_KEY, (optional) SUPABASE_SERVICE_ROLE_KEY

# Build and run
npm run build
npm run dev
```

### 2. Load this repo’s vCons into vcon-mcp (show data being consumed)

**Option A – Demo script from this repo (recommended for hackathon):**

With vcon-mcp running in **HTTP mode** (see vcon-mcp docs: `MCP_TRANSPORT=http`, `MCP_HTTP_PORT=3000`), run:

```bash
# From this repo (tadhack-2025). Install requests if needed: pip install requests
export MCP_BASE_URL=http://localhost:3000
export API_KEY=your-api-key   # only if vcon-mcp has API_KEYS set
python3 scripts/demo_mcp_consume.py
```

This script (1) health-checks the MCP server, (2) **ingests** all vCons from `911_calls/` via the REST API, and (3) **consumes** the data by listing and fetching one vCon to show it in the MCP server. Use this to demonstrate “this data being consumed in the MCP server” during your demo.

**Option B – From the vcon-mcp project:**

```bash
cd vcon-mcp
npm run load:local -- --path /path/to/tadhack-2025/911_calls
```

**Option C – curl (single vCon):**

```bash
curl -X POST http://localhost:3000/api/v1/vcons \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d @911_calls/4f22a08c-7e3b-4a65-8a73-d2677aadd8d3.vcon.json
```

### 3. Connect an AI assistant to vcon-mcp

**Claude Desktop** – add to `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS):

```json
{
  "mcpServers": {
    "vcon": {
      "command": "node",
      "args": ["/path/to/vcon-mcp/dist/index.js"],
      "env": {
        "SUPABASE_URL": "your-project-url",
        "SUPABASE_ANON_KEY": "your-anon-key"
      }
    }
  }
}
```

**Cursor** – add the vcon-mcp server in Cursor settings (MCP) with the same `command`/`args`/`env`. Then you can ask the AI to “search vCons for gas leak reports” or “get the transcript for vCon …” and it will use the MCP tools.

### 4. What you can do with MCP tools

Once connected, the AI can use vcon-mcp tools to:

- **create_vcon** / **add_dialog** / **add_analysis** – store or enrich vCons
- **search_vcons** – filter by subject, party, date
- **search_vcons_content** – full-text search in transcripts
- **search_vcons_semantic** – meaning-based search (with embeddings)
- **get_vcon** – fetch a vCon by UUID
- **get_database_analytics** – size, growth, content stats

For full tool list, transport options (stdio vs HTTP), and Docker deployment, see the [vcon-mcp README](https://github.com/vcon-dev/vcon-mcp).

## Reference for vCon 2026

This repository is maintained as a **reference dataset for vCon 2026** (spec, tooling, MCP, demos). Use it to validate vCon implementations, test MCP servers, or build search/tag/analyze tools against a known structure.

- **[REFERENCE.md](REFERENCE.md)** — Purpose, usage, and citation.
- **[reference/vcon-2026-reference.json](reference/vcon-2026-reference.json)** — Machine-readable manifest (counts, date range, layout, vCon structure) for automation and catalogs.

## Scenario: Utility Outages (AI intake, no human dispatcher)

The dataset models **utility outage reporting** where:

- **Caller** reports a gas leak or power outage.
- **AI virtual assistant** (no human dispatcher) handles the call:
  - Intake of the report
  - **Address verification via caller ID** (“I have your address as … from your caller ID. Is that correct?”)
  - **Real-time technician ETA** and optional SMS/app updates when the technician is en route or when power is restored

Use cases: demos for AI-powered utility intake, MCP tooling over vCon, and reference payloads for address verification + ETA flows.

## Overview

The dataset includes **42** synthetic utility outage report calls between callers and the **City Gas & Power Virtual Assistant**, covering:

- **Gas leak reports** (smell in building, near meter, kitchen, water heater)
- **Power outage reports** (single unit, building, street; restoration ETA)

Calls are organized by day in folders `18/`–`24/` (May 18–24, 2025).

## Report types

### Gas leak
- Caller reports gas smell (building, kitchen, meter, basement).
- AI verifies address via caller ID, creates urgent ticket, gives technician ETA (e.g. 18–35 minutes) and SMS when technician is ~5 minutes out.
- Safety guidance (avoid flames, open windows if safe).

### Power outage
- Caller reports power out (unit, building, or street).
- AI verifies address via caller ID, creates outage ticket, gives restoration or technician ETA (e.g. 30–75 minutes) and app/SMS updates.

## Call characteristics

- **Average duration**: ~45–75 seconds
- **Parties**: AI assistant (agent), caller (customer)
- **No human dispatcher**: All intake and ETA provided by the virtual assistant
- **Language**: English
- **Transcription confidence**: 99%
- **Meta**: `report_type: utility_outage`; parties include `caller_id_verification: true` for the AI agent

## Data format

Each conversation includes:
- Dialog metadata (recording type, start, duration; audio URL optional)
- Full transcript with speaker diarization (AI / Caller)
- AI-generated summary
- Participant metadata (caller and virtual assistant, with address in meta where relevant)

## Regenerating or adding utility outage vCons

Synthetic utility outage vCons are generated by **`scripts/generate_utility_outage_vcons.py`**. To regenerate or add more:

```bash
# Regenerate 42 vCons into day folders 18–24 (from repo root)
python3 scripts/generate_utility_outage_vcons.py --out . --count 42 --seed 42

# Custom count and output
python3 scripts/generate_utility_outage_vcons.py --out . --count 20
```

See **[scripts/README.md](scripts/README.md)** for full options (day folders, base URL, start date, seed).

## Synthetic 911 call data (optional)

You can also generate **synthetic** 911 emergency call vCons (dispatcher + caller) for separate demos or MCP testing. *That data is scripted and not from real 911 calls.* See **[scripts/README.md](scripts/README.md)**. From the repo root:

```bash
python3 scripts/generate_911_vcons.py          # 8 scenarios → 911_calls/
```

## Audio files (.mp3 or .wav)

The viewer plays audio when a file with the same base name as the vCon exists (e.g. `uuid.mp3` or `uuid.wav`).

**Option A – Audible speech (recommended):** Generate speech from the transcripts with TTS so you can hear the conversation:

```bash
pip install gtts
python3 scripts/generate_tts_audio_for_vcons.py --root .
```

This creates `.mp3` files with spoken transcript content. Refresh the viewer and press play to hear them.

**Option B – Silent placeholders:** Generate silent audio (for duration only):

```bash
python3 scripts/generate_mp3_for_vcons.py --root .
```

- With **ffmpeg**: creates `.mp3`. Without ffmpeg: creates `.wav`.  
Use `--wav-only` to always create `.wav`. See [scripts/README.md](scripts/README.md).

## Running the viewer

1. Install dependencies:
```bash
pip install streamlit pandas
```

2. Run the viewer:
```bash
streamlit run vcon_viewer.py
```
If `streamlit` is not found:
```bash
python3 -m streamlit run vcon_viewer.py
```

The viewer lets you browse conversations by day, view metadata and transcripts, and inspect analysis and diarization (AI / Caller).

## Typical interaction flow (utility outage)

1. AI greeting: “Thank you for calling City Gas & Power. I’m your virtual assistant. How can I help you today?”
2. Caller describes issue (gas smell or power out).
3. AI verifies address via caller ID and confirms with caller.
4. AI creates report and gives technician or restoration ETA; optionally SMS/app updates.
5. Closing (anything else? / stay safe / thank you for calling).

This dataset supports demos and tooling for **AI-handled utility outage intake, caller ID address verification, and real-time technician ETA** in a vCon + MCP context.
