# Veribuild Gate — local artifact comparison (partial implementation)

Canonical QMOOSA-0875, Batch 175, role: tests. This repository contains a **local byte-for-byte comparator** for two existing artifacts, not a deterministic build system or a reproducible-build attestation.

## Run

    python src/compare_artifacts.py path/to/reference.bin path/to/candidate.bin
    python -m compileall -q src tests
    python -m unittest discover -s tests -p 'reality_*.py' -v
    cargo check --all-targets

Exit codes: 0 means both readable artifacts are byte-identical; 1 means different bytes; 2 means an input read error. Missing arguments return a nonzero argparse status. Files are compared in bounded chunks without writing either input.

## Verification scope

Tests invoke the **actual local comparator** with identical, mutated, truncated, empty and missing files. This does not prove independent deterministic builds, supply-chain integrity, trusted provenance, authenticated distribution, cryptographic certification, PQC, network connectivity, or production readiness. No RPC or blockchain deployment occurs.

Status: IMPLEMENTATION_PARTIAL; SECURITY_APPROVED=NO; DEPLOYMENT_READY=NO. Do not infer production acceptance from CI green.
