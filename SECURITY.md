# Security status — Veribuild Gate

This is a **partial local artifact comparison tool**. It checks byte equality of two caller-supplied files, not how those files were built or whether they came from trusted sources.

No independent security audit, NIST FIPS certification, PQC implementation, verified build provenance, production deployment readiness, or bug-bounty commitment is asserted.

Known limitations: local files only; filesystem race and symlink behavior are not hardened for untrusted multi-tenant use; no signed attestations, reproducible build orchestration, hermetic environment enforcement or trust roots. Treat it as a development diagnostic.

Report security findings through the repository's GitHub issue/security-reporting mechanism. Do not include credentials or private keys.
