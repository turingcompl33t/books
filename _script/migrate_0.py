"""
migrate_0.py

Migrate 'author' field to support multiple authors.
"""

import argparse
import json
import logging
import sys
from pathlib import Path
from typing import Tuple

EXIT_SUCCESS = 0
EXIT_FAILURE = 1


def parse_arguments() -> Tuple[Path, bool]:
    """Parse commandline arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--path",
        type=Path,
        required=True,
        help="The path to the books directory.",
    )
    parser.add_argument(
        "--verbose", action="store_true", help="Enable verbose output."
    )
    args = parser.parse_args()
    return args.path, args.verbose


def migrate_one(path: Path) -> bool:
    """
    Perform a migration of a single book entry.
    :param path: The path to the book directory
    :return: `True` if the manifest is modified, `False` otherwise
    """
    assert path.is_dir(), "Broken precondition."
    logging.debug(f"Migrating {path}.")

    manifest_path = path / "manifest.json"
    if not manifest_path.is_file():
        raise RuntimeError(f"Book at {path} missing manifest.")

    with manifest_path.open("r") as f:
        manifest = json.load(f)

    if "author" not in manifest:
        logging.debug(f"Book at {path} does not require migration, skipping.")
        return False

    manifest["authors"] = [manifest["author"]]
    del manifest["author"]

    with manifest_path.open("w") as f:
        json.dump(manifest, f, indent=2)

    logging.debug(f"Migrated book at {path}.")
    return True


def migrate(path: Path) -> int:
    """Perform the migration."""
    assert path.is_dir(), "Broken precondition."
    migrated = [migrate_one(p) for p in path.glob("*") if p.is_dir()]
    return sum(1 for m in migrated if m)


def main() -> int:
    path, verbose = parse_arguments()
    logging.basicConfig(level=logging.DEBUG if verbose else logging.ERROR)

    if not path.is_dir():
        logging.error(f"Book directory {path} not found.")
        return EXIT_FAILURE

    migrated = migrate(path)
    print(f"Migrated {migrated} manifests.")

    return EXIT_SUCCESS


if __name__ == "__main__":
    sys.exit(main())
