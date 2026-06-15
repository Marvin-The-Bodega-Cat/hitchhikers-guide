# Hitchhikers Guide to the Future

Static site and Time Machine onboarding repo for `hitchhikersguidetothefuture.com`.

The artifact is the repo itself: site copy, onboarding transmissions, desired email receipts, send receipts, reply ledger, and tests.

Core loop:

```text
desired receipt -> send evidence -> reply/no-reply evidence -> resolved or miss
```

The homepage includes an email-list signup hook. The first onboarding sequence lives under `recruit/transmissions/`; each transmission has a matching desired receipt under `recruit/desired-receipts/`.

Analytics:
- Fathom site: `LLFJJYXQ` (`HitchhikersGuideFuture`)
- Pageviews load through `https://cdn.usefathom.com/script.js`
- Signup submit event: `HHGTTF Email Signup Submitted`
- Post-submit confirmation event: `HHGTTF Email Signup Thank You`
