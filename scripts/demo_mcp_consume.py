#!/usr/bin/env python3
"""
Demo: Ingest this repo's vCons into vcon-mcp (REST API), then list/get them
to show the data being consumed by the MCP server.

Prerequisites:
  1. vcon-mcp running in HTTP mode (see README "Using vCon MCP with this repo").
  2. Optional: API_KEY if the server has API_KEYS / API_AUTH_REQUIRED=true.

Usage:
  export MCP_BASE_URL=http://localhost:3000   # optional, default below
  export API_KEY=your-key                     # optional if auth disabled
  python3 scripts/demo_mcp_consume.py
  python3 scripts/demo_mcp_consume.py --dir 911_calls --base-url http://127.0.0.1:3000
"""

import json
import os
import sys
from pathlib import Path

try:
    import requests
except ImportError:
    print("Install requests: pip install requests")
    sys.exit(1)

DEFAULT_BASE = "http://localhost:3000"
API_BASE = "/api/v1"


def main(
    base_url: str = None,
    api_key: str = None,
    data_dir: str = "911_calls",
    dry_run: bool = False,
) -> None:
    base_url = (base_url or os.environ.get("MCP_BASE_URL") or DEFAULT_BASE).rstrip("/")
    api_key = api_key or os.environ.get("API_KEY")
    repo_root = Path(__file__).resolve().parent.parent
    dir_path = repo_root / data_dir

    if not dir_path.is_dir():
        print(f"Data dir not found: {dir_path}")
        sys.exit(1)

    vcon_files = sorted(dir_path.glob("*.vcon.json"))
    if not vcon_files:
        print(f"No .vcon.json files in {dir_path}")
        sys.exit(1)

    headers = {"Content-Type": "application/json"}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"

    # --- 1. Health check ---
    print("1. Checking vcon-mcp server...")
    try:
        r = requests.get(f"{base_url}{API_BASE}/health", timeout=5)
        if r.status_code != 200:
            print(f"   Health check returned {r.status_code}. Is the server running with REST API enabled?")
    except requests.RequestException as e:
        print(f"   Cannot reach {base_url}: {e}")
        print("   Start vcon-mcp in HTTP mode (see README) and set MCP_TRANSPORT=http, MCP_HTTP_PORT=3000")
        sys.exit(1)
    print("   OK")

    # --- 2. Ingest vCons ---
    print(f"\n2. Ingesting {len(vcon_files)} vCon(s) from {data_dir}/...")
    if dry_run:
        for f in vcon_files:
            print(f"   [dry-run] would POST {f.name}")
        print("   (run without --dry-run to actually ingest)")
    else:
        ingested = 0
        for vcon_path in vcon_files:
            with open(vcon_path) as f:
                body = json.load(f)
            r = requests.post(
                f"{base_url}{API_BASE}/vcons",
                headers=headers,
                json=body,
                timeout=30,
            )
            if r.status_code in (200, 201):
                ingested += 1
                print(f"   Ingested {vcon_path.name}")
            else:
                print(f"   Failed {vcon_path.name}: {r.status_code} {r.text[:200]}")
        print(f"   Ingested {ingested}/{len(vcon_files)} vCons.")

    # --- 3. Consume: list and get one ---
    print("\n3. Consuming data from MCP server (list + get one)...")
    if dry_run:
        print("   [dry-run] would GET /vcons and GET /vcons/:uuid")
        return
    r = requests.get(f"{base_url}{API_BASE}/vcons", headers=headers, timeout=10)
    if r.status_code != 200:
        print(f"   List failed: {r.status_code} {r.text[:200]}")
        return
    data = r.json()
    vcons = data if isinstance(data, list) else data.get("vcons", data.get("data", []))
    if not vcons:
        print("   No vCons returned (list may be empty or paginated).")
        return
    # Prefer one we just ingested
    first = vcons[0]
    uuid = first.get("uuid") if isinstance(first, dict) else first
    if isinstance(first, dict) and "uuid" in first:
        uuid = first["uuid"]
    else:
        uuid = first
    print(f"   List returned {len(vcons)} vCon(s). Fetching one: {uuid}")

    r2 = requests.get(f"{base_url}{API_BASE}/vcons/{uuid}", headers=headers, timeout=10)
    if r2.status_code != 200:
        print(f"   Get vCon failed: {r2.status_code}")
        return
    vcon = r2.json()
    parties = vcon.get("parties", [])
    analysis_count = len(vcon.get("analysis", []))
    print(f"   Retrieved vCon: {len(parties)} parties, {analysis_count} analysis entries.")
    for a in vcon.get("analysis") or []:
        if a.get("type") == "summary":
            body = a.get("body", "")
            if isinstance(body, dict):
                body = body.get("body", str(body))
            print(f"   Summary: {str(body)[:120]}...")
            break
    print("\n   Done. Data is being consumed by the MCP server (REST API).")
    print("   AI assistants connected via MCP can search/analyze these vCons with MCP tools.")


if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser(description="Demo: ingest vCons into vcon-mcp and show consumption")
    p.add_argument("--base-url", default=os.environ.get("MCP_BASE_URL", DEFAULT_BASE), help="vcon-mcp base URL")
    p.add_argument("--api-key", default=os.environ.get("API_KEY"), help="API key if required")
    p.add_argument("--dir", default="911_calls", help="Directory with .vcon.json (relative to repo root)")
    p.add_argument("--dry-run", action="store_true", help="Only print what would be done")
    args = p.parse_args()
    main(base_url=args.base_url, api_key=args.api_key, data_dir=args.dir, dry_run=args.dry_run)
