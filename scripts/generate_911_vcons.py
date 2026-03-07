#!/usr/bin/env python3
"""
Generate synthetic 911 call vCon files for TADHack / vCon 2026 reference use.
Output matches the vCon 0.0.1 structure used in this repo (parties, dialog, analysis).
No audio is generated; dialog.url can point to a placeholder or be left as-is.
"""

import json
import random
import uuid
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Optional

# ---------------------------------------------------------------------------
# 911 call scenarios: (caller_name, caller_tel, dispatcher_name, transcript, summary)
# Transcript uses "Dispatcher:" and "Caller:" for diarization; plain block for transcript body.
# ---------------------------------------------------------------------------

SCENARIOS = [
    {
        "call_type": "medical",
        "caller_name": "Maria Santos",
        "caller_tel": "+15551234001",
        "caller_mailto": "maria.santos@email.com",
        "dispatcher_name": "James Chen",
        "dispatcher_tel": "+15550009111",
        "dispatcher_mailto": "j.chen@psap.gov",
        "transcript": """911, what is your emergency?

I need an ambulance! My husband collapsed and he's not breathing right!

Okay, stay calm. I'm sending help. Is he conscious?

Barely. He's gasping. We're at 4421 Oak Street, apartment 3B.

4421 Oak Street, apartment 3B. Is he on his back? Can you start CPR if you know how?

Yes, I'm doing compressions now!

Help is on the way. Keep doing compressions. Don't hang up. Do you know what might have caused this?

He has heart problems. He takes medication.

Stay on the line. The ambulance is about two minutes out.""",
        "summary": "Caller reports husband collapsed and not breathing properly. Dispatcher confirms address 4421 Oak Street apt 3B, advises CPR, and dispatches ambulance. Caller states husband has heart condition.",
    },
    {
        "call_type": "fire",
        "caller_name": "Robert Miller",
        "caller_tel": "+15551234002",
        "caller_mailto": "r.miller@email.com",
        "dispatcher_name": "Sarah Williams",
        "dispatcher_tel": "+15550009111",
        "dispatcher_mailto": "s.williams@psap.gov",
        "transcript": """911, what is your emergency?

There's a fire in the garage! I can see smoke and flames!

Get everyone out of the house right now. Are you outside?

Yes, we're all out. The garage is attached to the house.

What's your address?

1807 Maple Drive.

1807 Maple Drive. Fire is on the way. Don't go back inside. Is anyone still in the house?

No, just me and my wife. We're in the driveway.

Good. Stay outside. Units are en route.""",
        "summary": "Caller reports fire in attached garage at 1807 Maple Drive. All occupants evacuated. Dispatcher confirms address and advises to stay outside; units dispatched.",
    },
    {
        "call_type": "burglary",
        "caller_name": "David Park",
        "caller_tel": "+15551234003",
        "caller_mailto": "d.park@email.com",
        "dispatcher_name": "Lisa Torres",
        "dispatcher_tel": "+15550009111",
        "dispatcher_mailto": "l.torres@psap.gov",
        "transcript": """911, what is your emergency?

Someone broke into my house. I think they're still inside. I'm in the bedroom with the door locked.

Stay where you are. Don't confront them. What's your address?

5520 Cedar Lane.

5520 Cedar Lane. Are you alone?

My wife is with me. We're both in the bedroom.

Officers are on the way. Can you describe any vehicle or person you saw?

I saw a dark sedan speed off. I didn't get the plate. I heard the back door break.

Stay on the line. Keep the door locked. Police are about four minutes out.""",
        "summary": "Caller reports possible burglary in progress at 5520 Cedar Lane; caller and wife locked in bedroom. Dark sedan seen leaving. Police dispatched.",
    },
    {
        "call_type": "car_accident",
        "caller_name": "Jennifer Walsh",
        "caller_tel": "+15551234004",
        "caller_mailto": "j.walsh@email.com",
        "dispatcher_name": "Michael Brown",
        "dispatcher_tel": "+15550009111",
        "dispatcher_mailto": "m.brown@psap.gov",
        "transcript": """911, what is your emergency?

There's been a bad crash at the intersection of Highway 9 and Riverside. Two cars. One might have people trapped.

Are you at the scene? Are you safe?

Yes, I'm on the shoulder. I didn't hit anyone.

Do you see anyone injured or not moving?

One driver is out and walking. The other car is smashed. I can't tell if someone's inside.

We're sending police and ambulance. Stay back from the vehicles in case of fire. Can you tell me exactly which direction the cars are facing?

One is in the northbound lane, one is in the intersection. There's debris everywhere.

Help is on the way. Don't move anyone. Just stay safe.""",
        "summary": "Caller reports two-vehicle crash at Highway 9 and Riverside; possible entrapment. Caller is safe on shoulder. Police and ambulance dispatched.",
    },
    {
        "call_type": "domestic_disturbance",
        "caller_name": "Anonymous Neighbor",
        "caller_tel": "+15551234005",
        "caller_mailto": "anonymous@email.com",
        "dispatcher_name": "Rachel Kim",
        "dispatcher_tel": "+15550009111",
        "dispatcher_mailto": "r.kim@psap.gov",
        "transcript": """911, what is your emergency?

I'm hearing yelling and things breaking next door. I'm worried someone could get hurt.

What's the address where this is happening?

It's 901 Pine Street. The house next to me.

901 Pine Street. Do you know who lives there or how many people?

I don't know them well. I think a couple. The shouting has been going on for maybe ten minutes.

Have you seen anyone leave or any weapons?

No. I just hear screaming and banging.

We're sending officers. Stay in your home. Don't approach. If you see anyone leave, note what they look like and which way they go.""",
        "summary": "Neighbor reports ongoing yelling and sounds of breaking objects at 901 Pine Street. Dispatcher sends officers and advises caller to stay inside and not approach.",
    },
    {
        "call_type": "medical",
        "caller_name": "Thomas Reed",
        "caller_tel": "+15551234006",
        "caller_mailto": "t.reed@email.com",
        "dispatcher_name": "James Chen",
        "dispatcher_tel": "+15550009111",
        "dispatcher_mailto": "j.chen@psap.gov",
        "transcript": """911, what is your emergency?

My dad fell down the stairs. He's not moving. He's like seventy.

Is he breathing?

I think so. His chest is moving a little.

What's your address?

2240 Birch Road.

2240 Birch Road. Don't move him. Keep him still. Is he on his back or his side?

On his side. There's no blood but he's out of it.

Medics are on the way. Stay with him. If he stops breathing, tell me immediately. Does he have any medical conditions?

He's on blood thinners. He had a stroke a few years ago.

Okay. Help is coming. Keep him still and keep talking to me.""",
        "summary": "Caller reports elderly father fell down stairs at 2240 Birch Road, not moving but breathing. Dispatcher advises not to move him; medics dispatched. Father on blood thinners, history of stroke.",
    },
    {
        "call_type": "suspicious_person",
        "caller_name": "Nancy Foster",
        "caller_tel": "+15551234007",
        "caller_mailto": "n.foster@email.com",
        "dispatcher_name": "Lisa Torres",
        "dispatcher_tel": "+15550009111",
        "dispatcher_mailto": "l.torres@psap.gov",
        "transcript": """911, what is your emergency?

There's someone in my backyard. I'm alone. I don't know if they're trying to get in.

Are you in a safe place? Can you lock the door?

I'm upstairs. The back door is locked. I saw a flashlight.

What's your address?

667 Elm Street.

667 Elm Street. We're sending a unit. Can you describe the person or what they're doing?

I can't see clearly. Maybe one person. They were near the shed.

Stay upstairs. Don't go outside. Keep the line open. Officer is on the way.""",
        "summary": "Caller reports possible intruder in backyard at 667 Elm Street; caller alone and upstairs. Unit dispatched; caller advised to stay inside.",
    },
    {
        "call_type": "roadside_emergency",
        "caller_name": "Chris Morales",
        "caller_tel": "+15551234008",
        "caller_mailto": "c.morales@email.com",
        "dispatcher_name": "Sarah Williams",
        "dispatcher_tel": "+15550009111",
        "dispatcher_mailto": "s.williams@psap.gov",
        "transcript": """911, what is your emergency?

I'm on Route 44 westbound. There's a car on fire on the shoulder. I don't see anyone around.

Are you in a safe location?

Yes, I'm pulled over way back. The car is fully engulfed.

We're sending fire and police. What's the nearest mile marker or landmark?

I think near mile 12. There's a rest area sign about a quarter mile ahead.

Route 44 westbound near mile 12. Don't approach the vehicle. Stay in your car unless you're in danger. Help is on the way.""",
        "summary": "Caller reports vehicle fire on Route 44 westbound near mile 12. No occupants visible. Fire and police dispatched; caller advised to stay back.",
    },
]


def _build_diarized(transcript: str) -> str:
    """Convert plain transcript lines into Dispatcher: / Caller: diarized format."""
    lines = [ln.strip() for ln in transcript.strip().split("\n") if ln.strip()]
    # Alternate: odd-indexed lines often dispatcher (911 first), even caller; adjust if your convention differs
    out = []
    for i, line in enumerate(lines):
        if i % 2 == 0:
            out.append(f"Dispatcher: {line}")
        else:
            out.append(f"Caller: {line}")
    return "\n\n".join(out)


def _parties(scenario: dict) -> List[dict]:
    caller_id = f"{scenario['caller_tel']}_{scenario['caller_mailto']}_1100"
    dispatcher_id = scenario["dispatcher_mailto"]
    return [
        {
            "tel": scenario["dispatcher_tel"],
            "mailto": scenario["dispatcher_mailto"],
            "name": scenario["dispatcher_name"],
            "role": "agent",
            "meta": {"role": "dispatcher", "psap": "PSAP-1"},
            "id": dispatcher_id,
        },
        {
            "tel": scenario["caller_tel"],
            "mailto": scenario["caller_mailto"],
            "name": scenario["caller_name"],
            "role": "customer",
            "meta": {"role": "caller"},
            "id": caller_id,
        },
    ]


def _dialog(vcon_id: str, start: datetime, duration_sec: float, base_url: str) -> List[dict]:
    date_path = start.strftime("%Y/%m/%d")
    filename = f"{vcon_id}.mp3"
    url = f"{base_url.rstrip('/')}/{date_path}/{filename}" if base_url else ""
    start_iso = start.strftime("%Y-%m-%dT%H:%M:%S-04:00")
    return [
        {
            "type": "recording",
            "start": start_iso,
            "parties": [1, 0],
            "mimetype": "audio/x-wav",
            "filename": filename,
            "url": url,
            "alg": "SHA-512",
            "signature": "",
            "duration": round(duration_sec, 3),
            "meta": {
                "disposition": "ANSWERED",
                "direction": "in",
                "emergency_type": "911",
            },
        }
    ]


def _analysis(scenario: dict) -> List[dict]:
    transcript_body = {
        "transcript": scenario["transcript"].strip(),
        "confidence": 0.99,
        "detected_language": "en",
    }
    diarized_text = _build_diarized(scenario["transcript"])
    return [
        {
            "type": "transcript",
            "dialog": 0,
            "vendor": "deepgram",
            "body": transcript_body,
            "encoding": "none",
        },
        {
            "type": "summary",
            "dialog": 0,
            "vendor": "openai",
            "body": scenario["summary"].strip(),
            "encoding": "none",
        },
        {
            "type": "diarized",
            "dialog": 0,
            "vendor": "openai",
            "body": diarized_text,
            "encoding": "none",
        },
    ]


def generate_one(
    scenario: dict,
    vcon_id: Optional[str] = None,
    start: Optional[datetime] = None,
    duration_sec: Optional[float] = None,
    base_url: str = "",
) -> dict:
    """Build a single vCon document for a 911 call scenario."""
    vcon_id = vcon_id or str(uuid.uuid4())
    start = start or datetime(2025, 6, 1, 12, 0, 0)
    duration_sec = duration_sec if duration_sec is not None else 45.0 + random.uniform(-10, 25)
    created_at = start + timedelta(seconds=duration_sec)
    # ISO format with -04:00 style offset for compatibility
    def _iso_ts(dt: datetime) -> str:
        return dt.strftime("%Y-%m-%dT%H:%M:%S-04:00")

    return {
        "uuid": vcon_id,
        "vcon": "0.0.1",
        "created_at": _iso_ts(created_at),
        "redacted": {},
        "group": [],
        "parties": _parties(scenario),
        "dialog": _dialog(vcon_id, start, duration_sec, base_url),
        "attachments": [],
        "analysis": _analysis(scenario),
    }


def main(
    out_dir: str = "911_calls",
    count: Optional[int] = None,
    base_url: str = "",
    start_date: str = "2025-06-01",
    seed: Optional[int] = None,
) -> None:
    out_path = Path(out_dir)
    out_path.mkdir(parents=True, exist_ok=True)
    if seed is not None:
        random.seed(seed)

    start = datetime.strptime(start_date[:10], "%Y-%m-%d")
    count = count or len(SCENARIOS)
    if count <= len(SCENARIOS):
        scenarios_to_use = SCENARIOS[:count]
    else:
        scenarios_to_use = SCENARIOS + random.choices(SCENARIOS, k=count - len(SCENARIOS))

    for i, scenario in enumerate(scenarios_to_use):
        vcon_id = str(uuid.uuid4())
        call_start = start + timedelta(days=i // 10, hours=(i % 10) * 2, minutes=random.randint(0, 59))
        duration = 35.0 + random.uniform(5, 40)
        vcon = generate_one(scenario, vcon_id=vcon_id, start=call_start, duration_sec=duration, base_url=base_url)
        file_path = out_path / f"{vcon_id}.vcon.json"
        with open(file_path, "w") as f:
            json.dump(vcon, f, indent=2)
        print(f"Wrote {file_path} ({scenario['call_type']})")

    print(f"Generated {len(scenarios_to_use)} vCon file(s) under {out_path.absolute()}")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Generate synthetic 911 call vCon files")
    parser.add_argument("--out", "-o", default="911_calls", help="Output directory (default: 911_calls)")
    parser.add_argument("--count", "-n", type=int, default=None, help="Number of vCons to generate (default: one per scenario)")
    parser.add_argument("--base-url", default="", help="Base URL for dialog audio (e.g. https://example.com/audio)")
    parser.add_argument("--start-date", default="2025-06-01", help="Start date for generated calls (YYYY-MM-DD)")
    parser.add_argument("--seed", type=int, default=None, help="Random seed for reproducibility")
    args = parser.parse_args()
    main(out_dir=args.out, count=args.count, base_url=args.base_url, start_date=args.start_date, seed=args.seed)
