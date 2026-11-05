#!/usr/bin/env python3
"""Study Coach harness — SM-2 spaced repetition, Discord-friendly.

Usage:
  coach.py add "topic" "front question" "back answer" [--source notes.md]
  coach.py due [--limit N]          -> cards to review now
  coach.py grade <id> <0-5>         -> reschedule (5=perfect, 0=total blank)
  coach.py stats                    -> workload forecast
  coach.py mine <file>              -> parse Q::A pairs from a notes file
"""
import json, sys, argparse, math, random
from datetime import datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).parent
DB = ROOT / "cards.json"

def load():
    if DB.exists():
        return json.loads(DB.read_text())
    return {"next_id": 1, "cards": []}

def save(db):
    DB.write_text(json.dumps(db, indent=2))

def now():
    return datetime.now()

def sm2(card, q):
    """SM-2: q in [0,5]. q<3 resets streak."""
    if q < 3:
        card["reps"] = 0
        card["interval"] = 1
        card["ease"] = max(1.3, card["ease"] - 0.2)
    else:
        card["reps"] += 1
        if card["reps"] == 1:
            card["interval"] = 1
        elif card["reps"] == 2:
            card["interval"] = 6
        else:
            card["interval"] = round(card["interval"] * card["ease"])
        card["ease"] = max(1.3, card["ease"] + 0.1 - (5 - q) * (0.08 + (5 - q) * 0.02))
    card["due"] = (now() + timedelta(days=card["interval"])).isoformat(timespec="minutes")

def cmd_add(db, topic, front, back, source):
    c = {"id": db["next_id"], "topic": topic, "front": front, "back": back,
         "source": source or "", "ease": 2.5, "interval": 0, "reps": 0,
         "due": now().isoformat(timespec="minutes"), "created": now().isoformat(timespec="minutes")}
    db["next_id"] += 1
    db["cards"].append(c)
    save(db)
    print(f"added #{c['id']} [{topic}] {front}")

def cmd_due(db, limit):
    due = [c for c in db["cards"] if c["due"] <= now().isoformat(timespec="minutes")]
    due.sort(key=lambda c: c["due"])
    if not due:
        print("nothing due — you're clear 🎉")
        return
    print(f"{len(due)} due (showing {min(limit, len(due))}):")
    for c in due[:limit]:
        print(f"  #{c['id']} [{c['topic']}] {c['front']}")

def cmd_grade(db, cid, q):
    c = next((c for c in db["cards"] if c["id"] == cid), None)
    if not c:
        print(f"no card #{cid}"); return
    sm2(c, q)
    save(db)
    print(f"#{cid}: next in {c['interval']}d (ease {c['ease']:.2f})")

def cmd_stats(db):
    total = len(db["cards"])
    due_now = sum(1 for c in db["cards"] if c["due"] <= now().isoformat(timespec="minutes"))
    mature = sum(1 for c in db["cards"] if c["interval"] >= 21)
    print(f"cards: {total} | due now: {due_now} | mature (21d+): {mature}")
    # 7-day forecast
    for d in range(1, 8):
        day = (now() + timedelta(days=d)).date().isoformat()
        n = sum(1 for c in db["cards"] if c["due"][:10] == day)
        if n:
            print(f"  {day}: {n}")

def cmd_mine(db, path):
    """Parse lines like 'Q:: question :: answer' from a notes file."""
    text = Path(path).read_text()
    n = 0
    for line in text.splitlines():
        if "::" in line:
            parts = [p.strip() for p in line.split("::")]
            if len(parts) >= 3 and parts[1] and parts[2]:
                cmd_add(db, parts[0] or "general", parts[1], parts[2], path)
                n += 1
    print(f"mined {n} cards from {path}")

def main():
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("add"); a.add_argument("topic"); a.add_argument("front"); a.add_argument("back"); a.add_argument("--source", default="")
    d = sub.add_parser("due"); d.add_argument("--limit", type=int, default=10)
    g = sub.add_parser("grade"); g.add_argument("id", type=int); g.add_argument("q", type=int)
    sub.add_parser("stats")
    m = sub.add_parser("mine"); m.add_argument("path")
    args = p.parse_args()
    db = load()
    {"add": lambda: cmd_add(db, args.topic, args.front, args.back, args.source),
     "due": lambda: cmd_due(db, args.limit),
     "grade": lambda: cmd_grade(db, args.id, args.q),
     "stats": lambda: cmd_stats(db),
     "mine": lambda: cmd_mine(db, args.path)}[args.cmd]()

if __name__ == "__main__":
    main()
