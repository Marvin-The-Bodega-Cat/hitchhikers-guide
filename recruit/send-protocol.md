# SEND PROTOCOL

Send path: Leo -> recruit.
Return path: recruit -> Leo + Marvin intake.

Operator identity:
- name: Leo
- role: sender-of-record
- account: [LEO_FILL]

Marvin intake identity:
- role: reply nexus
- account: [MARVIN_FILL]

Per-send check:
- transmission file checksum recorded before send
- transmission id matches repo version
- send timestamp written to transmission YAML front matter

Reply contract:
- reader reply address includes Leo + Marvin
- Marvin receives all replies first
- Leo sees a single trust-preserved summary
- replies never edited for social comfort

Blast radius limit:
- one transmission per action-completed reply only
- nothing is sent by cron without explicit operator approval