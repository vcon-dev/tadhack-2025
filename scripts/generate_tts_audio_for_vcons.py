#!/usr/bin/env python3
"""
Generate audible speech from vCon transcripts using TTS (gTTS).
Overwrites or creates .mp3 files so the viewer plays real speech instead of silence.
Requires: pip install gtts pydub
(pydub is used to concatenate chunks; need ffmpeg for mp3, or we use gtts only and save each chunk then merge with pydub - actually gTTS saves directly to mp3, so we can chunk the text, generate multiple mp3s, merge with pydub, or just do one gTTS save if under limit. gTTS limit is 5000 chars. Let me chunk and merge.)
"""

import json
import os
import tempfile
from pathlib import Path

# gTTS has a 5000-character limit per request; chunk and merge with pydub if available
try:
    from gtts import gTTS
except ImportError:
    print("Install gTTS: pip install gtts")
    exit(1)

try:
    from pydub import AudioSegment
except ImportError:
    AudioSegment = None  # optional: for merging long transcripts

MAX_CHARS = 4500  # stay under gTTS limit


def get_transcript(vcon_path: Path) -> str:
    """Extract plain transcript text from vCon (no speaker labels)."""
    with open(vcon_path) as f:
        data = json.load(f)
    for a in data.get("analysis") or []:
        if a.get("type") != "transcript":
            continue
        body = a.get("body")
        if isinstance(body, dict):
            return (body.get("transcript") or body.get("body") or "").strip()
        if isinstance(body, str):
            return body.strip()
    return ""


def text_to_mp3_gtts(text: str, out_path: Path, lang: str = "en") -> bool:
    """Convert text to speech and save as mp3. Chunk if needed."""
    text = (text or "").strip().replace("\n\n", ". ").replace("\n", " ")
    if not text:
        return False
    out_path = Path(out_path).resolve()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    if len(text) <= MAX_CHARS:
        tts = gTTS(text=text, lang=lang, slow=False)
        tts.save(str(out_path))
        return True
    # Chunk and merge
    chunks = []
    start = 0
    while start < len(text):
        end = start + MAX_CHARS
        if end < len(text):
            # break at sentence or space
            last_period = text.rfind(". ", start, end + 1)
            last_space = text.rfind(" ", start, end + 1)
            end = max(last_period + 1, last_space + 1, start + MAX_CHARS) if last_space > start else end
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        start = end
    if not chunks:
        return False
    if AudioSegment is None:
        # No pydub: save first chunk only
        gTTS(text=chunks[0], lang=lang, slow=False).save(str(out_path))
        return True
    tmp_dir = Path(tempfile.mkdtemp())
    try:
        paths = []
        for i, chunk in enumerate(chunks):
            p = tmp_dir / f"chunk_{i}.mp3"
            gTTS(text=chunk, lang=lang, slow=False).save(str(p))
            paths.append(p)
        combined = AudioSegment.empty()
        for p in paths:
            combined += AudioSegment.from_mp3(str(p))
        combined.export(str(out_path), format="mp3")
        return True
    finally:
        for p in tmp_dir.glob("*.mp3"):
            try:
                p.unlink()
            except Exception:
                pass
        try:
            tmp_dir.rmdir()
        except Exception:
            pass
    return False


def main(root_dir: str = ".", dirs: list = None) -> None:
    root = Path(root_dir)
    if dirs is None:
        dirs = ["911_calls"]
        for d in root.iterdir():
            if d.is_dir() and d.name.isdigit():
                dirs.append(d.name)
    done = 0
    for dir_name in dirs:
        folder = root / dir_name
        if not folder.is_dir():
            continue
        for vcon_path in sorted(folder.glob("*.vcon.json")):
            transcript = get_transcript(vcon_path)
            if not transcript:
                print(f"Skip (no transcript): {vcon_path}")
                continue
            # Viewer expects uuid.mp3 (same dir, base name without .vcon.json)
            base_name = vcon_path.stem.replace(".vcon", "")  # "uuid.vcon" -> "uuid"
            mp3_path = vcon_path.parent / (base_name + ".mp3")
            if text_to_mp3_gtts(transcript, mp3_path):
                print(f"Created {mp3_path}")
                done += 1
            else:
                print(f"Failed: {vcon_path}")
    print(f"Done: {done} TTS .mp3 file(s) created. Refresh the viewer to hear them.")


if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser(description="Generate TTS .mp3 from vCon transcripts (audible speech)")
    p.add_argument("--root", "-r", default=".", help="Repo root")
    p.add_argument("--dirs", "-d", nargs="+", default=None, help="Subdirs to scan (default: 911_calls + numbered)")
    args = p.parse_args()
    main(root_dir=args.root, dirs=args.dirs)
