#!/usr/bin/env python3
"""
Manual send helper for the recruit sequence.

Usage:
  SMTP_HOST=smtp.gmail.com SMTP_PORT=587 \
  SMTP_USER=... SMTP_PASS=... \
  RECRUIT_EMAIL=... \
  python3 recruit/send_transmission.py recruit/transmissions/0.md

Behavior:
- Reads transmission metadata and message body.
- Sends one email to the recruit.
- Prints a receipt with transmission_id, draft_hash, send_timestamp, recipient, and provider.

Security:
- Do not commit secrets.
- Prefer app passwords or an approved mail provider.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import smtplib
import sys
from email.message import EmailMessage
from datetime import datetime, timezone
from pathlib import Path

FRONT_MATTER_RE = re.compile(r"^---\n(.*?)\n---\n(.*)$", re.DOTALL)


def parse_front_matter(text: str):
    m = FRONT_MATTER_RE.match(text)
    if not m:
        raise ValueError("missing yaml-ish front matter block")
    meta = {}
    for line in m.group(1).splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" not in line:
            continue
        k, v = line.split(":", 1)
        meta[k.strip()] = v.strip().strip('"').strip("'")
    body = m.group(2).strip()
    return meta, body


def sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:12]


def build_message(sender: str, recipient: str, meta: dict, body: str) -> EmailMessage:
    msg = EmailMessage()
    msg["Subject"] = meta.get("subject", "Hitchhikers Guide")
    msg["From"] = sender
    msg["To"] = recipient
    msg["X-Transmission-Id"] = meta.get("transmission_id", "")
    msg["X-Sequence-Version"] = meta.get("sequence_version", "")
    msg["X-Draft-Hash"] = meta.get("draft_hash", "")
    msg["X-Reply-Policy"] = meta.get("reply_policy", "")
    msg["X-On-Record-Allowed"] = meta.get("on_record_allowed", "")
    msg.set_content(body)
    return msg


def send_once(msg: EmailMessage, host: str, port: int, username: str, password: str) -> None:
    with smtplib.SMTP(host, port) as smtp:
        smtp.ehlo()
        try:
            smtp.starttls()
        except Exception:
            pass
        smtp.login(username, password)
        smtp.send_message(msg)


def write_receipt(path: Path, meta: dict, recipient: str, timestamp: str, digest: str, provider: str) -> None:
    receipt = {
        "transmission_id": meta.get("transmission_id", ""),
        "subject": meta.get("subject", ""),
        "recipient": recipient,
        "send_timestamp": timestamp,
        "draft_hash": digest,
        "provider": provider,
        "reply_policy": meta.get("reply_policy", ""),
        "on_record_allowed": meta.get("on_record_allowed", ""),
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(receipt, ensure_ascii=False) + "\n")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("transmission")
    parser.add_argument("--to", default=os.getenv("RECRUIT_EMAIL", ""))
    parser.add_argument("--from", default=os.getenv("SMTP_USER", ""), dest="from_")
    parser.add_argument("--host", default=os.getenv("SMTP_HOST", "smtp.gmail.com"))
    parser.add_argument("--port", type=int, default=int(os.getenv("SMTP_PORT", "587")))
    parser.add_argument("--receipt", default="recruit/send-receipts.jsonl")
    args = parser.parse_args()

    path = Path(args.transmission)
    text = path.read_text(encoding="utf-8")
    meta, body = parse_front_matter(text)
    digest = sha256(body)

    if not args.to:
        print("Missing recipient. Set RECRUIT_EMAIL or pass --to.", file=sys.stderr)
        return 2

    msg = build_message(args.from_, args.to, {**meta, "draft_hash": digest}, body)
    timestamp = datetime.now(timezone.utc).isoformat()

    provider = f"smtp:{args.host}:{args.port}"
    send_once(msg, args.host, args.port, os.getenv("SMTP_USER", ""), os.getenv("SMTP_PASS", ""))
    write_receipt(Path(args.receipt), {**meta, "draft_hash": digest}, args.to, timestamp, digest, provider)

    print(f"sent transmission_id={meta.get('transmission_id')} recipient={args.to} ts={timestamp} provider={provider}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
