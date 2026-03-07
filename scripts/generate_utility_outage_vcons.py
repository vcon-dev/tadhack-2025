#!/usr/bin/env python3
"""
Generate synthetic utility outage report vCon files (gas leak, power outage).
AI handles intake, address verification via caller ID, and real-time technician ETA—
no human dispatcher. For TADHack / vCon 2026 reference and MCP demos.
"""

import json
import random
import uuid
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Optional

SCENARIOS = [
    {
        "report_type": "gas_leak",
        "caller_name": "Patricia Moore",
        "caller_tel": "+15559876001",
        "caller_mailto": "p.moore@email.com",
        "address": "2847 Willow Lane, Apt 2B",
        "transcript": """Thank you for calling City Gas & Power. I'm your virtual assistant. How can I help you today?

I smell gas in my building. I'm not sure if it's my unit or the hallway.

I'm sorry to hear that. Your safety is our priority. I'm pulling up your account now. I have your address as 2847 Willow Lane, apartment 2B, from your caller ID. Is that correct?

Yes, that's correct.

Thank you. I've created an urgent gas report for 2847 Willow Lane, Apt 2B. Please avoid flames and don't use any switches if you can. Are you able to leave the building safely?

Yes, I'm going outside now.

A technician is dispatched. Your current ETA is 22 minutes. You'll get a text when they're 5 minutes away. Is there anything else?

No, thank you.

You're welcome. Stay safe.""",
        "summary": "Caller reports gas smell at 2847 Willow Lane Apt 2B. AI verifies address via caller ID, creates urgent ticket, and provides technician ETA of 22 minutes with SMS notification.",
    },
    {
        "report_type": "gas_leak",
        "caller_name": "James Liu",
        "caller_tel": "+15559876002",
        "caller_mailto": "j.liu@email.com",
        "address": "901 Oak Street",
        "transcript": """Thank you for calling City Gas & Power. I'm your virtual assistant. How can I help you today?

I think there might be a gas leak in my backyard. Near the meter.

I'm pulling up your location. I have your address as 901 Oak Street. Is that correct?

Yes.

I've logged a gas leak report for 901 Oak Street. Please keep everyone away from the meter area. A technician is on the way. Your estimated arrival time is 35 minutes. You can also see live ETA in the City Gas & Power app.

Okay. Will they call when they're close?

Yes. You'll get a call and an SMS when the technician is about 5 minutes out. Anything else?

No, that's all.

Thank you for reporting. Stay safe.""",
        "summary": "Caller reports possible gas leak near meter at 901 Oak Street. AI confirms address via caller ID, creates report, and gives technician ETA of 35 minutes with app and SMS updates.",
    },
    {
        "report_type": "power_outage",
        "caller_name": "Susan Davis",
        "caller_tel": "+15559876003",
        "caller_mailto": "s.davis@email.com",
        "address": "4521 Maple Drive",
        "transcript": """Thank you for calling City Gas & Power. I'm your virtual assistant. How can I help you today?

My power just went out. The whole block might be out.

I have your address as 4521 Maple Drive from your caller ID. Is that correct?

Yes.

I've created a power outage report for 4521 Maple Drive. We're seeing an outage in your area. A crew is already assigned. Current ETA to restore service is 1 hour 15 minutes. You can track status and ETA in the app or we'll text you when power is back.

Okay. So about an hour?

Approximately 1 hour 15 minutes. We'll send a notification when it's restored. Anything else?

No, thanks.

You're welcome. Have a good day.""",
        "summary": "Caller reports power outage at 4521 Maple Drive. AI verifies address via caller ID, creates outage ticket, and provides restoration ETA of 1 hour 15 minutes with app and SMS updates.",
    },
    {
        "report_type": "power_outage",
        "caller_name": "Robert Hayes",
        "caller_tel": "+15559876004",
        "caller_mailto": "r.hayes@email.com",
        "address": "1200 Cedar Blvd, Unit 7",
        "transcript": """Thank you for calling City Gas & Power. I'm your virtual assistant. How can I help you today?

The power's been out for over an hour. Just my unit or the building?

I have your address as 1200 Cedar Boulevard, unit 7. Is that correct?

Yes.

Thanks. I've added your location to the outage report. We have a crew in your area. Current technician ETA to your address is 40 minutes. They'll assess whether it's building-wide or your unit. You'll get a text when they're en route.

All right. Thanks.

You're welcome. Is there anything else?

No.

Thank you for calling.""",
        "summary": "Caller reports prolonged power outage at 1200 Cedar Blvd Unit 7. AI confirms address via caller ID and provides technician ETA of 40 minutes with en-route SMS notification.",
    },
    {
        "report_type": "gas_leak",
        "caller_name": "Maria Santos",
        "caller_tel": "+15559876005",
        "caller_mailto": "m.santos@email.com",
        "address": "55 River Road",
        "transcript": """Thank you for calling City Gas & Power. I'm your virtual assistant. How can I help you today?

I smell gas in the kitchen. I turned off the stove.

I have your address as 55 River Road from your caller ID. Can you confirm?

Yes, 55 River Road.

I've created an urgent gas report for 55 River Road. Please open windows if safe and avoid any ignition sources. A technician is dispatched. Your ETA is 18 minutes. We'll text you when they're 5 minutes away.

Thank you.

You're welcome. Stay safe.""",
        "summary": "Caller reports gas smell in kitchen at 55 River Road. AI verifies address via caller ID, creates urgent ticket, and gives technician ETA of 18 minutes with 5-minute-out SMS.",
    },
    {
        "report_type": "power_outage",
        "caller_name": "David Chen",
        "caller_tel": "+15559876006",
        "caller_mailto": "d.chen@email.com",
        "address": "7700 Park Avenue",
        "transcript": """Thank you for calling City Gas & Power. I'm your virtual assistant. How can I help you today?

Power went out about 20 minutes ago. I need to know when it'll be back.

I have your address as 7700 Park Avenue. Is that correct?

Yes.

I've logged your report for 7700 Park Avenue. There's a known outage in your zone. Restoration ETA is 45 minutes. You can see real-time ETA in the app. We'll also send a text when power is restored.

Okay. 45 minutes.

Approximately. Anything else?

No. Thank you.

You're welcome.""",
        "summary": "Caller reports power outage at 7700 Park Avenue. AI confirms address via caller ID, links to known outage, and provides restoration ETA of 45 minutes with app and SMS updates.",
    },
    {
        "report_type": "power_outage",
        "caller_name": "Linda Foster",
        "caller_tel": "+15559876007",
        "caller_mailto": "l.foster@email.com",
        "address": "3300 Elm Street",
        "transcript": """Thank you for calling City Gas & Power. I'm your virtual assistant. How can I help you today?

Our whole street has no power. Can someone come check?

I have your address as 3300 Elm Street from your caller ID. Is that correct?

Yes.

I've created an outage report for 3300 Elm Street. A crew is assigned to your area. Current ETA for assessment is 30 minutes. You'll get an SMS when we have an update. Real-time ETA is also in the app.

Thank you.

You're welcome. Anything else?

No.

Thanks for calling.""",
        "summary": "Caller reports street-wide power outage at 3300 Elm Street. AI verifies address via caller ID and provides crew ETA of 30 minutes with SMS and app updates.",
    },
    {
        "report_type": "gas_leak",
        "caller_name": "Michael Torres",
        "caller_tel": "+15559876008",
        "caller_mailto": "m.torres@email.com",
        "address": "1600 Pine Road",
        "transcript": """Thank you for calling City Gas & Power. I'm your virtual assistant. How can I help you today?

I smell gas near the water heater in the basement.

I have your address as 1600 Pine Road. Can you confirm?

Yes.

I've logged an urgent gas report for 1600 Pine Road. Please avoid the basement and don't use any electrical switches there. A technician is on the way. ETA is 25 minutes. You'll receive a text when they're 5 minutes out.

Okay. Thank you.

You're welcome. Stay safe.""",
        "summary": "Caller reports gas smell near water heater at 1600 Pine Road. AI confirms address via caller ID, creates urgent ticket, and provides technician ETA of 25 minutes.",
    },
    # ---- Additional gas leak examples ----
    {
        "report_type": "gas_leak",
        "caller_name": "Karen Wright",
        "caller_tel": "+15559876009",
        "caller_mailto": "k.wright@email.com",
        "address": "4100 Sunset Blvd, Unit 12",
        "transcript": """Thank you for calling City Gas & Power. I'm your virtual assistant. How can I help you today?

There's a really strong gas smell in the hallway outside my apartment. I'm in 12.

I have your address as 4100 Sunset Boulevard, unit 12, from your caller ID. Is that correct?

Yes, unit 12.

I've created an urgent gas report for 4100 Sunset Blvd, Unit 12. Please don't use elevators or light switches in the hallway. Can you and your household get outside safely?

We're going down the stairs now.

A technician is dispatched. ETA is 20 minutes. You'll get a text when they're 5 minutes away. Stay outside until they clear the building.

Thank you.

You're welcome. Stay safe.""",
        "summary": "Caller reports strong gas smell in hallway at 4100 Sunset Blvd Unit 12. AI verifies address via caller ID, advises evacuation, and provides technician ETA of 20 minutes with SMS.",
    },
    {
        "report_type": "gas_leak",
        "caller_name": "Tom Bradley",
        "caller_tel": "+15559876010",
        "caller_mailto": "t.bradley@email.com",
        "address": "88 Industrial Way",
        "transcript": """Thank you for calling City Gas & Power. I'm your virtual assistant. How can I help you today?

We have a gas leak in the warehouse. Someone hit a line with a forklift.

I have your address as 88 Industrial Way from your caller ID. Is that your location?

Yes, that's our facility. Building B, dock area.

I've logged an urgent gas report for 88 Industrial Way, Building B dock area. Evacuate the area and don't operate equipment. A technician is on the way. ETA is 15 minutes. You'll get a call when they're 5 minutes out.

We're clearing everyone out now.

Thank you for reporting. Stay safe.""",
        "summary": "Caller reports gas line struck by forklift at 88 Industrial Way Building B. AI verifies address via caller ID, creates urgent ticket, and provides technician ETA of 15 minutes.",
    },
    {
        "report_type": "gas_leak",
        "caller_name": "Nancy Choi",
        "caller_tel": "+15559876011",
        "caller_mailto": "n.choi@email.com",
        "address": "2200 Lakeview Drive",
        "transcript": """Thank you for calling City Gas & Power. I'm your virtual assistant. How can I help you today?

I'm calling for my neighbor. She's not home but I smell gas coming from next door. 2202 Lakeview.

I have your address as 2200 Lakeview Drive from your caller ID. Are you reporting for 2202 Lakeview Drive?

Yes. I'm at 2200, the smell is from 2202.

I've created an urgent gas report for 2202 Lakeview Drive. Please stay away from that property. A technician is dispatched. ETA is 28 minutes. We'll attempt to contact the resident. You'll get a text when the technician is 5 minutes out.

Okay. Thank you.

You're welcome. Stay safe.""",
        "summary": "Caller reports gas smell at neighbor's residence 2202 Lakeview Drive; caller at 2200. AI creates report for 2202, dispatches technician ETA 28 minutes, and will contact resident.",
    },
    {
        "report_type": "gas_leak",
        "caller_name": "Derek Evans",
        "caller_tel": "+15559876012",
        "caller_mailto": "d.evans@email.com",
        "address": "515 Hillcrest Ave",
        "transcript": """Thank you for calling City Gas & Power. I'm your virtual assistant. How can I help you today?

I smell gas when I turn on the furnace. I turned it off.

I have your address as 515 Hillcrest Avenue from your caller ID. Is that correct?

Yes.

I've created an urgent gas report for 515 Hillcrest Ave. Don't use the furnace or any gas appliances. A technician is on the way. ETA is 30 minutes. We'll text you when they're 5 minutes out. Do you have heat from another source if needed?

We have space heaters. We're okay.

Good. Stay safe. Anything else?

No. Thank you.""",
        "summary": "Caller reports gas smell when furnace runs at 515 Hillcrest Ave. AI verifies address via caller ID, creates urgent ticket, technician ETA 30 minutes; caller has alternate heat.",
    },
    {
        "report_type": "gas_leak",
        "caller_name": "Rita Patel",
        "caller_tel": "+15559876013",
        "caller_mailto": "r.patel@email.com",
        "address": "700 Grant Street, Apt 4A",
        "transcript": """Thank you for calling City Gas & Power. I'm your virtual assistant. How can I help you today?

There's a gas smell in my bathroom. I think it might be the water heater.

I have your address as 700 Grant Street, apartment 4A, from your caller ID. Can you confirm?

Yes, 4A.

I've created an urgent gas report for 700 Grant Street, Apt 4A. Please avoid the bathroom and don't use any switches or flames there. A technician is dispatched. ETA is 22 minutes. You'll get a text when they're 5 minutes away.

Thank you.

You're welcome. Stay safe.""",
        "summary": "Caller reports gas smell in bathroom, possibly water heater, at 700 Grant St Apt 4A. AI verifies address via caller ID and provides technician ETA of 22 minutes.",
    },
]


def _build_diarized(transcript: str) -> str:
    """Convert transcript into AI: / Caller: diarized format (alternating)."""
    lines = [ln.strip() for ln in transcript.strip().split("\n") if ln.strip()]
    out = []
    for i, line in enumerate(lines):
        if i % 2 == 0:
            out.append(f"AI: {line}")
        else:
            out.append(f"Caller: {line}")
    return "\n\n".join(out)


def _parties(scenario: dict) -> List[dict]:
    caller_id = f"{scenario['caller_tel']}_{scenario['caller_mailto']}_1100"
    return [
        {
            "tel": "+15550005555",
            "mailto": "assistant@citygaspower.com",
            "name": "City Gas & Power Virtual Assistant",
            "role": "agent",
            "meta": {"role": "ai_assistant", "dispatcher": "none", "caller_id_verification": True},
            "id": "assistant@citygaspower.com",
        },
        {
            "tel": scenario["caller_tel"],
            "mailto": scenario["caller_mailto"],
            "name": scenario["caller_name"],
            "role": "customer",
            "meta": {"role": "caller", "address": scenario["address"]},
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
                "report_type": "utility_outage",
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
        {"type": "transcript", "dialog": 0, "vendor": "deepgram", "body": transcript_body, "encoding": "none"},
        {"type": "summary", "dialog": 0, "vendor": "openai", "body": scenario["summary"].strip(), "encoding": "none"},
        {"type": "diarized", "dialog": 0, "vendor": "openai", "body": diarized_text, "encoding": "none"},
    ]


def generate_one(
    scenario: dict,
    vcon_id: Optional[str] = None,
    start: Optional[datetime] = None,
    duration_sec: Optional[float] = None,
    base_url: str = "",
) -> dict:
    """Build a single vCon document for a utility outage report."""
    vcon_id = vcon_id or str(uuid.uuid4())
    start = start or datetime(2025, 5, 18, 12, 0, 0)
    duration_sec = duration_sec if duration_sec is not None else 50.0 + random.uniform(-10, 20)
    created_at = start + timedelta(seconds=duration_sec)

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
    out_dir: str = ".",
    day_folders: Optional[List[str]] = None,
    count: Optional[int] = None,
    base_url: str = "",
    start_date: str = "2025-05-18",
    seed: Optional[int] = None,
) -> None:
    """Generate vCon files. If day_folders is set (e.g. ['18','19',...,'24']), spread files into those subdirs."""
    out_path = Path(out_dir)
    if seed is not None:
        random.seed(seed)

    start = datetime.strptime(start_date[:10], "%Y-%m-%d")
    count = count or len(SCENARIOS)
    if count <= len(SCENARIOS):
        scenarios_to_use = SCENARIOS[:count]
    else:
        scenarios_to_use = SCENARIOS + random.choices(SCENARIOS, k=count - len(SCENARIOS))

    day_folders = day_folders or []
    for i, scenario in enumerate(scenarios_to_use):
        vcon_id = str(uuid.uuid4())
        day_index = i % len(day_folders) if day_folders else 0
        day_offset = int(day_folders[day_index]) - int(day_folders[0]) if day_folders and day_folders[0].isdigit() else day_index
        call_start = start + timedelta(days=day_offset, hours=(i % 14 + 8), minutes=random.randint(0, 59))
        duration = 45.0 + random.uniform(5, 30)
        vcon = generate_one(scenario, vcon_id=vcon_id, start=call_start, duration_sec=duration, base_url=base_url)
        if day_folders:
            sub = out_path / day_folders[day_index]
            sub.mkdir(parents=True, exist_ok=True)
            file_path = sub / f"{vcon_id}.vcon.json"
        else:
            file_path = out_path / f"{vcon_id}.vcon.json"
        with open(file_path, "w") as f:
            json.dump(vcon, f, indent=2)
        print(f"Wrote {file_path} ({scenario['report_type']})")

    print(f"Generated {len(scenarios_to_use)} vCon file(s) under {out_path.absolute()}")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Generate synthetic utility outage report vCon files")
    parser.add_argument("--out", "-o", default=".", help="Output directory (default: current)")
    parser.add_argument("--day-folders", nargs="+", default=["18", "19", "20", "21", "22", "23", "24"], help="Subdirs to spread vCons into (e.g. 18 19 20 21 22 23 24)")
    parser.add_argument("--count", "-n", type=int, default=None, help="Number of vCons to generate")
    parser.add_argument("--base-url", default="", help="Base URL for dialog audio")
    parser.add_argument("--start-date", default="2025-05-18", help="Start date YYYY-MM-DD")
    parser.add_argument("--seed", type=int, default=None, help="Random seed")
    args = parser.parse_args()
    main(
        out_dir=args.out,
        day_folders=args.day_folders,
        count=args.count,
        base_url=args.base_url,
        start_date=args.start_date,
        seed=args.seed,
    )
