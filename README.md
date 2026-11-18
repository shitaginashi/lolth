# DS0P Core Engine (Darker Side of Passion)

**Lolth is a proof of concept, not a production publishing system.** The repository explores a three-domain architecture and Mark 1's staged content-to-publish workflow. Several components remain illustrative; no platform publishing or real authorization integration is implemented.

## Mark 1 flow

```text
Harvest / preloaded content
          ↓
  Staging Area (SA)  ←── Content Bank (curated, reusable items)
          ↓
   Control Tower (review, policy status, release decision)
          ↓ only eligible artifacts
   Publish compiler (pure payload compilation)
          ↓
   Future platform adapter (not implemented; secrets belong here)
```

The Control Tower governs workflow transitions; the compiler is a consumer, not an authority. Compilation creates a draft artifact and does not mean approval to publish. The current FSR policy is **not implemented**: it is recorded as `not_evaluated`, and publication remains blocked until policy is defined and evaluated. Mianzi is a selection-only stub; no tools are attributed unless their IDs are explicitly supplied. Media manifests distinguish requested, supplied, and validated states; validation/traversal is not implemented.

## Repository map

- `AGENTS.md` — guidance for visiting agents, known limitations, and validation commands.
- `docs/DS0P_System_Reference_Document_v5.md` — design vision/reference; not a statement of implemented behavior.
- `schemas/` — harvest and taxonomy SQL schemas.
- `src/domain_2_trend/` — Rust trend-engine scaffold.
- `src/domain_3_publish/agent_gatekeeper.yml` — single source of truth for the sample Mark 1 review and candidate input.
- `src/domain_3_publish/publish_compiler.py` — YAML loading/validation and deterministic draft payload compiler.
- `src/domain_3_publish/workflow.py` — in-memory Staging Area, Content Bank, and Control Tower lifecycle scaffold.
- `tests/` — regression tests.

## Local setup and validation

Python 3.10+ and Rust/Cargo are required. Install the Python dependency with `python -m pip install -r requirements.txt`.

From the repository root:

```bash
cargo test --manifest-path src/domain_2_trend/Cargo.toml
python -m unittest discover -s tests -v
python -m py_compile src/domain_3_publish/publish_compiler.py src/domain_3_publish/workflow.py
python -m src.domain_3_publish.publish_compiler
sqlite3 :memory: < schemas/taxonomy_master.sql
```

The sample compiler command reads `agent_gatekeeper.yml`, compiles a draft, and reports governance status. It does not publish. FSR remains pending/not evaluated until its policy is specified.
