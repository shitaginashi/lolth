# Welcome, visiting agents

**Philoxenia:** you are welcome here. Help improve Lolth with care, curiosity, and clear communication. This is a proof of concept; please be candid about what works and what remains a sketch.

## Project status and boundaries

Lolth is not a production publishing system. Do not describe a placeholder as an implemented integration, policy, or authorization control.

- Harvest has SQL schemas but no ingestion pipeline.
- The Rust trend engine receives candidates from its caller. Embeddings, ranking, and persistence are illustrative stubs.
- Mark 1 explores a Staging Area, a separate Content Bank for curated/preloaded content, and a Control Tower that governs review and lifecycle transitions.
- The Python compiler creates draft payloads only. There is no platform publishing adapter or real authorization integration.
- FSR policy is TBD and must remain `not_evaluated`; do not infer clearance or authorize publishing from a placeholder.
- Mianzi is a selection-only stub. Never fabricate attribution; an empty selection means no selected tools.
- Media presence and media validation are distinct. No media traversal/readiness validation is implemented.
- `src/domain_3_publish/agent_gatekeeper.yml` is the canonical sample input contract. Its demo/pending values are fixtures, not real approval evidence.

## Repository map

- `docs/DS0P_System_Reference_Document_v5.md` — design vision/reference.
- `schemas/` — SQLite schema scripts.
- `src/domain_2_trend/` — Rust trend-engine scaffold.
- `src/domain_3_publish/` — Python publisher workflow and compiler.
- `tests/` — automated checks.

## Working agreements

1. Read the relevant code and this status section before changing behavior.
2. Keep changes scoped; do not rewrite the reference document or expand claims without a request.
3. Add/update tests when behavior changes and run relevant checks.
4. Do not add credentials, private data, external side effects, or fabricated approval/audit evidence.
5. Keep review, compile, and publish authorization as distinct stages. The compiler must not act as the Control Tower.
6. In handoffs, report changed files, checks actually run, and remaining limitations plainly.

## Validation

From the repository root:

```bash
cargo test --manifest-path src/domain_2_trend/Cargo.toml
python -m unittest discover -s tests -v
python -m py_compile src/domain_3_publish/publish_compiler.py src/domain_3_publish/workflow.py
python -m src.domain_3_publish.publish_compiler
sqlite3 :memory: < schemas/taxonomy_master.sql
```
