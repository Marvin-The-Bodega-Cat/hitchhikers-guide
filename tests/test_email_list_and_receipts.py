from __future__ import annotations

import json
import re
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class FormParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.forms = []
        self.inputs = []
        self.buttons = []
        self._current_form = None

    def handle_starttag(self, tag, attrs):
        data = dict(attrs)
        if tag == "form":
            self.forms.append(data)
            self._current_form = data
        elif tag == "input":
            self.inputs.append(data)
        elif tag == "button":
            self.buttons.append(data)

    def handle_endtag(self, tag):
        if tag == "form":
            self._current_form = None


def parse_front_matter(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    assert match, f"{path} missing front matter"
    meta = {}
    for line in match.group(1).splitlines():
        if not line.strip() or ":" not in line:
            continue
        key, value = line.split(":", 1)
        meta[key.strip()] = value.strip().strip('"').strip("'")
    return meta


def test_homepage_has_real_email_list_signup_hook():
    parser = FormParser()
    parser.feed((ROOT / "index.html").read_text(encoding="utf-8"))

    signup_forms = [
        form for form in parser.forms
        if form.get("data-receipt-id") == "hhgttf-email-list-signup-hooked-up"
    ]
    assert len(signup_forms) == 1

    form = signup_forms[0]
    assert form.get("method", "").lower() == "post"
    assert form.get("action", "").startswith("https://")
    assert "TODO" not in form.get("action", "").upper()
    assert "example.com" not in form.get("action", "")

    email_inputs = [field for field in parser.inputs if field.get("type") == "email"]
    assert email_inputs, "signup form needs an email input"
    assert any(field.get("name") == "email" and "required" in field for field in email_inputs)
    assert any(field.get("name") == "source" and field.get("value") == "hhgttf-homepage" for field in parser.inputs)
    assert any(button.get("type") == "submit" for button in parser.buttons)


def test_each_transmission_has_desired_receipt_contract():
    desired_dir = ROOT / "recruit" / "desired-receipts"
    transmissions = sorted((ROOT / "recruit" / "transmissions").glob("*.md"), key=lambda p: p.stem)
    assert len(transmissions) == 7

    for transmission in transmissions:
        meta = parse_front_matter(transmission)
        receipt_path = desired_dir / f"{meta['transmission_id']}.json"
        assert receipt_path.exists(), f"missing desired receipt for {meta['transmission_id']}"
        receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
        assert receipt["receipt_id"] == f"desired-email-{meta['transmission_id'].lower()}"
        assert receipt["transmission_id"] == meta["transmission_id"]
        assert receipt["sequence_version"] == meta["sequence_version"]
        assert receipt["status"] == "desired"
        assert receipt["resolution_status"] == "unresolved"
        assert receipt["expected_evidence"] == ["send_receipt", "reply_receipt"]
        assert receipt["privacy"] == "private_by_default"


def test_public_recruit_gateway_names_receipt_protocol():
    public_gateway = (ROOT / "recruit" / "public" / "index.md").read_text(encoding="utf-8")
    assert "desired receipt" in public_gateway.lower()
    assert "send_receipt" in public_gateway
    assert "reply_receipt" in public_gateway
