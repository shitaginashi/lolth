# DS0P Core Engine (Darker Side of Passion)

3-Domain Architecture Engine.

## Repository status

This repository is an early scaffold for a three-domain architecture:

- Harvest / ingestion schemas
- Trend / Bear Mode Rust state machine
- Publish / sidecar Python compiler

The trend engine currently receives staged candidates as input; database integration, production embeddings, ranking, and persistence are not implemented yet.

## Local validation

From the repository root, run:

```bash
cargo test --manifest-path src/domain_2_trend/Cargo.toml
python -m unittest discover -s tests -v
python -m py_compile src/domain_3_publish/publish_compiler.py
sqlite3 :memory: < schemas/taxonomy_master.sql
