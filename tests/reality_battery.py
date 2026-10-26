"""Real subprocess regression tests for the local artifact comparator."""
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "src" / "compare_artifacts.py"


class ArtifactComparatorIntegration(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.a = Path(self.tmp.name) / "reference.bin"
        self.b = Path(self.tmp.name) / "candidate.bin"

    def run_cli(self, *paths):
        return subprocess.run([sys.executable, str(SCRIPT), *map(str, paths)],
                              capture_output=True, text=True, timeout=10, check=False)

    def test_identical_binary_artifacts(self):
        data = bytes(range(256)) * 4097
        self.a.write_bytes(data)
        self.b.write_bytes(data)
        proc = self.run_cli(self.a, self.b)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertIn("REPRODUCIBLE=TRUE", proc.stdout)

    def test_one_byte_mutation_rejected(self):
        self.a.write_bytes(b"abc")
        self.b.write_bytes(b"abd")
        proc = self.run_cli(self.a, self.b)
        self.assertEqual(proc.returncode, 1)
        self.assertIn("REPRODUCIBLE=FALSE", proc.stdout)

    def test_truncation_rejected(self):
        self.a.write_bytes(b"abc")
        self.b.write_bytes(b"ab")
        self.assertEqual(self.run_cli(self.a, self.b).returncode, 1)

    def test_empty_artifacts_equal(self):
        self.a.write_bytes(b"")
        self.b.write_bytes(b"")
        self.assertEqual(self.run_cli(self.a, self.b).returncode, 0)

    def test_missing_artifact_fails_closed(self):
        self.a.write_bytes(b"abc")
        proc = self.run_cli(self.a, self.b)
        self.assertEqual(proc.returncode, 2)
        self.assertIn("INPUT_ERROR", proc.stderr)

    def test_missing_arguments_fails_closed(self):
        self.assertNotEqual(self.run_cli().returncode, 0)


if __name__ == "__main__":
    unittest.main()
