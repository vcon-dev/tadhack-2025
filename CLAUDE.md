# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a VCON (Virtual Call Object Notation) data repository for TADHack 2025. VCON is a standardized format for representing conversational data including audio recordings and associated metadata.

## Repository Structure

The repository contains VCON conversation data organized by date:
- Each numbered directory (18/, 19/, 20/, 21/, 22/, 23/, 24/) represents a day
- Each conversation consists of:
  - An `.mp3` audio file containing the recorded conversation
  - A corresponding `.vcon.json` file containing metadata and analysis

## VCON JSON Structure

Each VCON file contains:
- `uuid`: Unique identifier for the conversation
- `vcon`: Version number (currently "0.0.1")
- `created_at`: ISO timestamp of conversation creation
- `parties`: Array of participants with contact info and roles
- `dialog`: Recording metadata including URL, duration, and disposition
- `analysis`: Array containing transcript, summary, and diarized text
- `attachments`: Additional files (currently empty arrays)

## Working with VCON Files

When analyzing or processing VCON files:
1. The audio files are referenced by URL in the `dialog` section
2. Transcripts are available in the `analysis` section under type "transcript"
3. Each conversation has metadata about participants, including roles (customer/agent)
4. File naming follows UUID pattern for both audio and JSON files

## Common Tasks

Since this appears to be a data repository without build scripts:
- To access conversation data: Read the `.vcon.json` files
- To access audio: Use the URL provided in the dialog section or the local `.mp3` file
- To analyze conversations: Parse the transcript, summary, or diarized sections in the analysis array