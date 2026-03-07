#!/usr/bin/env python3
"""
Generate silent audio files for each .vcon.json so the viewer has an audio file
per conversation. Duration from dialog[0].duration.
- Prefers .mp3 (requires ffmpeg: brew install ffmpeg or apt install ffmpeg).
- Fallback: creates .wav with stdlib (no extra deps); viewer also accepts .wav.
"""

import json
import struct
import subprocess
import sys
import wave
from pathlib import Path


def get_duration(vcon_path: Path) -> float:
    """Read duration in seconds from first dialog in vCon JSON."""
    with open(vcon_path) as f:
        data = json.load(f)
    dialogs = data.get("dialog") or []
    if not dialogs:
        return 60.0
    return float(dialogs[0].get("duration", 60))


def generate_silent_wav(output_path: Path, duration_sec: float) -> bool:
    """Create a silent WAV file (stdlib only). Returns True on success."""
    duration_sec = max(0.1, min(7200, duration_sec))
    output_path = output_path.resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    rate = 44100
    nframes = int(rate * duration_sec)
    with wave.open(str(output_path), "wb") as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(rate)
        chunk = 4096
        for i in range(0, nframes, chunk):
            n = min(chunk, nframes - i)
            wav.writeframes(struct.pack("<%dh" % n, *([0] * n)))
    return True


def generate_silent_mp3(output_path: Path, duration_sec: float) -> bool:
    """Create a silent MP3 using ffmpeg. Returns True on success."""
    duration_sec = max(0.1, min(7200, duration_sec))
    output_path = output_path.resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        "ffmpeg", "-y",
        "-f", "lavfi", "-i", "anullsrc=r=44100:cl=mono",
        "-t", str(duration_sec),
        "-acodec", "libmp3lame", "-q:a", "9",
        str(output_path),
    ]
    try:
        subprocess.run(cmd, check=True, capture_output=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        if isinstance(e, FileNotFoundError):
            print("ffmpeg not found; using .wav fallback (no ffmpeg needed).", file=sys.stderr)
        else:
            print(f"ffmpeg failed: {e}; using .wav fallback.", file=sys.stderr)
        return False


def main(root_dir: str = ".", dirs: list = None, prefer_mp3: bool = True, force: bool = False) -> None:
    root = Path(root_dir)
    if dirs is None:
        dirs = ["911_calls"]
        for d in root.iterdir():
            if d.is_dir() and d.name.isdigit():
                dirs.append(d.name)
    created = 0
    skipped = 0
    for dir_name in dirs:
        folder = root / dir_name
        if not folder.is_dir():
            continue
        for vcon_path in sorted(folder.glob("*.vcon.json")):
            base = vcon_path.with_suffix("")
            mp3_path = base.with_suffix(".mp3")
            wav_path = base.with_suffix(".wav")
            if not force and (mp3_path.exists() or wav_path.exists()):
                skipped += 1
                continue
            duration = get_duration(vcon_path)
            if prefer_mp3 and generate_silent_mp3(mp3_path, duration):
                print(f"Created {mp3_path} ({duration:.1f}s)")
                created += 1
            else:
                if generate_silent_wav(wav_path, duration):
                    print(f"Created {wav_path} ({duration:.1f}s)")
                    created += 1
                else:
                    sys.exit(1)
    print(f"Done: {created} created, {skipped} already existed.")


if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser(description="Generate silent .mp3 or .wav for each .vcon.json")
    p.add_argument("--root", "-r", default=".", help="Repo root (default: current dir)")
    p.add_argument("--dirs", "-d", nargs="+", default=None, help="Subdirs to scan (default: 911_calls + numbered)")
    p.add_argument("--wav-only", action="store_true", help="Skip ffmpeg, create .wav only (no deps)")
    p.add_argument("--force", "-f", action="store_true", help="Overwrite existing .mp3/.wav and regenerate")
    args = p.parse_args()
    main(root_dir=args.root, dirs=args.dirs, prefer_mp3=not args.wav_only, force=args.force)
