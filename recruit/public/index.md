# Boarding the Time Machine

This is the public gateway for the onboarding sequence. The sequence is not just copy; it is a small receipt machine.

## Receipt protocol

For each transmission, the repo carries a desired receipt in `recruit/desired-receipts/`.

A desired receipt starts unresolved and expects two evidence classes:

- `send_receipt`: the transmission was sent, with recipient, timestamp, provider, and draft hash.
- `reply_receipt`: the reply was answered, closed as no-reply, or logged as a miss with reason.

Replies are private by default. The repo should track metadata and resolution, not leak people.
