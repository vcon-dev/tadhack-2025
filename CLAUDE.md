# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a vCon (Virtual Call Object Notation) data repository for **vCon 2026**. The dataset models **utility outage reporting**: callers report gas leaks or power outages; an **AI virtual assistant** handles intake, verifies address via caller ID, and provides real-time technician ETA—no human dispatcher. vCon is a standardized format for representing conversational data including audio recordings and associated metadata.

## Repository Structure

The repository contains vCon conversation data organized by date:
- Each numbered directory (18/, 19/, 20/, 21/, 22/, 23/, 24/) represents a day (May 18–24, 2025)
- Each conversation consists of:
  - A `.vcon.json` file containing metadata and analysis (transcript, summary, diarized)
  - Optional corresponding `.mp3` or audio referenced by URL in the dialog section

## vCon JSON Structure

Each vCon file contains:
- `uuid`: Unique identifier for the conversation
- `vcon`: Version number (currently "0.0.1")
- `created_at`: ISO timestamp of conversation creation
- `parties`: Array of participants—AI virtual assistant (agent) and caller (customer); agent meta includes `role: ai_assistant`, `caller_id_verification: true`
- `dialog`: Recording metadata including URL, duration; meta includes `report_type: utility_outage`
- `analysis`: Array containing transcript, summary, and diarized text (AI: / Caller:)
- `attachments`: Additional files (currently empty arrays)

## Working with vCon Files

When analyzing or processing vCon files:
1. The audio files are referenced by URL in the `dialog` section (optional local `.mp3`)
2. Transcripts are available in the `analysis` section under type "transcript"; body may be an object with `transcript`, `confidence`, `detected_language`
3. Diarized analysis uses "AI:" and "Caller:" speaker labels
4. File naming follows UUID pattern for both audio and JSON files

## Common Tasks

- To access conversation data: Read the `.vcon.json` files from day folders 18/–24/
- To regenerate utility outage vCons: Run `python3 scripts/generate_utility_outage_vcons.py --out . --count 42 --seed 42`
- To analyze conversations: Parse the transcript, summary, or diarized sections in the analysis array
