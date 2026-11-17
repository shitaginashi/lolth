# Welcome, visiting agents

Philoxenia: you are welcome here. Help us improve Lolth with care, curiosity, and clear communication. Treat this repository as a work in progress, not as a finished system.

## Project status: proof of concept

Lolth is an early scaffold. Some paths are demonstrations or placeholders, not production behavior. Be explicit about that in code, documentation, and summaries. Do not imply that an unimplemented capability works end to end.

Known limitations:

- Harvest currently has SQL schemas, but no implemented ingestion pipeline.
- The Rust trend engine accepts candidates from its caller; it does not read the harvest database.
- Its embedding is a fixed placeholder vector, its filtering is a simple magnitude threshold, and its trend score is illustrative—not a production model.
- Persistence currently reports a count; it does not write to durable storage.
- The Python publisher builds text and attachment manifests; it does not publish to platform APIs. Character limits may also differ from a platform’s actual counting rules.

## Repository map

- `docs/DS0P_System_Reference_Document_v5.md` — broader system vision and design reference.
- `schemas/` — harvest and attribution-taxonomy SQL schemas.
- `src/domain_2_trend/` — Rust trend-engine proof of concept.
- `src/domain_3_publish/` — Python publish-payload compiler.
- `tests/` — Python regression tests.

## Before changing code

1. Read the relevant code and documentation; preserve the distinction between current behavior and planned design.
2. Keep changes scoped. Don’t rewrite the system reference document or expand the project’s claims unless asked.
3. Prefer small, testable improvements. Add or update tests when behavior changes.
4. Never add credentials, private data, or real external side effects.

## Validate changes

Run the checks relevant to your changes from the repository root:

```bash
cargo test --manifest-path src/domain_2_trend/Cargo.toml
python -m unittest discover -s tests -v
python -m py_compile src/domain_3_publish/publish_compiler.py
sqlite3 :memory: < schemas/taxonomy_master.sql
```

In your handoff, say what changed, which checks you ran, and what remains incomplete. If you could not run a check, say so plainly.