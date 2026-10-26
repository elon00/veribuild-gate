"""Local byte-for-byte artifact comparison; not a reproducible-build attestation."""
import argparse
from pathlib import Path
import sys


def compare_files(left: Path, right: Path, chunk_size: int = 1024 * 1024) -> bool:
    if chunk_size < 1:
        raise ValueError("chunk_size must be positive")
    with left.open("rb") as source, right.open("rb") as candidate:
        while True:
            a, b = source.read(chunk_size), candidate.read(chunk_size)
            if a != b:
                return False
            if not a:
                return True


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Compare two local artifacts byte-for-byte")
    parser.add_argument("reference", type=Path)
    parser.add_argument("candidate", type=Path)
    args = parser.parse_args(argv)
    try:
        match = compare_files(args.reference, args.candidate)
    except (OSError, ValueError) as exc:
        print(f"INPUT_ERROR: {exc}", file=sys.stderr)
        return 2
    print("REPRODUCIBLE=TRUE" if match else "REPRODUCIBLE=FALSE")
    return 0 if match else 1


if __name__ == "__main__":
    raise SystemExit(main())
