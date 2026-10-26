"""Fail-closed source-integrity checks, not protocol or PQC certification."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class SourceIntegrity(unittest.TestCase):
    def test_rust_source_contains_no_fake_verification_claims(self):
        source = (ROOT / "src" / "main.rs").read_text(encoding="utf-8")
        for claim in ("100/100", "FIPS", "CONNECTED", "Treasury Escrows Verified"):
            self.assertNotIn(claim, source)

    def test_comparator_exists(self):
        self.assertTrue((ROOT / "src" / "compare_artifacts.py").is_file())


if __name__ == "__main__":
    unittest.main()
