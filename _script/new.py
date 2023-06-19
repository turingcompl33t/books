"""
new.py

Create a new book entry.
"""

import argparse
import logging
import shutil
import sys
from pathlib import Path

EXIT_SUCCESS = 0
EXIT_FAILURE = 1


def parse_arguments() -> Path:
    """Parse commandline arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--books",
        type=Path,
        required=True,
        help="The path to the books directory.",
    )
    parser.add_argument(
        "--templates",
        type=Path,
        required=True,
        help="The path to the templates directory.",
    )
    parser.add_argument("name", type=str, help="The name of the entry.")
    args = parser.parse_args()
    return args.books, args.templates, args.name


def main() -> int:
    books_dir, templates_dir, name = parse_arguments()
    logging.basicConfig(level=logging.ERROR)

    if not books_dir.is_dir():
        logging.error(f"Books directory {books_dir} not found.")
        return EXIT_FAILURE
    if not templates_dir.is_dir():
        logging.error(f"Templates directory {templates_dir} not found.")
        return EXIT_FAILURE

    existing = [path.name for path in books_dir.glob("*") if path.is_dir()]
    if name in existing:
        logging.error(f"Entry with name {name} already exists.")
        return EXIT_FAILURE

    entry_path = books_dir / name
    entry_path.mkdir()

    template_src = templates_dir / "manifest.json"
    assert template_src.is_file(), "Broken invariant."

    shutil.copy(template_src, entry_path / "manifest.json")

    print(f"Initialized new entry at {entry_path}.")
    return EXIT_SUCCESS


if __name__ == "__main__":
    sys.exit(main())
