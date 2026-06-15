# Recruitment sequence

Drafts and runner logic for the 7-transmission onboarding.

Transmissions live in `recruit/transmissions/`.
Public gateway: `recruit/public/index.md`.

## Manual send protocol
1. Copy draft text.
2. Send through the operator's chosen mail client.
3. Log the send record here or in the site ledger.

## Desired receipt loop

Every outbound email gets a desired receipt before it is sent. That desired receipt is a public promise about the evidence we expect, not proof that the human relationship resolved.

States:
- `desired`: expected before send.
- `sent`: send receipt exists.
- `resolved`: reply handled, no-reply closed, or miss logged.

The repo is the artifact: sequence drafts, desired receipts, send receipts, and reply ledger. If a message vanishes into the void, the void gets a row. A depressing but useful improvement over vibes.
