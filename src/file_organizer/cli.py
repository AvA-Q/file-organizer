"""Command-line interface for the file organizer."""

from __future__ import annotations

import argparse
import sys
from collections.abc import Sequence

from .organizer import MovePlanItem, OrganizerError, apply_moves, plan_moves


def build_parser() -> argparse.ArgumentParser:
    """Create the command-line argument parser."""

    parser = argparse.ArgumentParser(
        prog="file-organizer",
        description="Safely organize files by extension.",
    )
    parser.add_argument(
        "directory",
        help="Directory whose files should be organized.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show the plan without changing files.",
    )
    parser.add_argument(
        "--yes",
        action="store_true",
        help="Apply the plan without asking for confirmation.",
    )
    return parser


def format_plan(plan: Sequence[MovePlanItem]) -> str:
    """Format a movement plan for terminal output."""

    lines = ["Planned moves:"]
    lines.extend(
        f"  {item.source} -> {item.destination}"
        for item in plan
    )
    return "\n".join(lines)


def main(argv: Sequence[str] | None = None) -> int:
    """Run the command-line program and return an exit status."""

    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        plan = plan_moves(args.directory)
    except OrganizerError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2

    if not plan:
        print("No files to organize.")
        return 0

    print(format_plan(plan))

    if args.dry_run:
        return 0

    if not args.yes:
        try:
            answer = input("Proceed with these moves? [y/N] ")
        except EOFError:
            answer = ""

        if answer.strip().casefold() not in {"y", "yes"}:
            print("Cancelled.")
            return 0

    moved, failed = apply_moves(plan)

    print(f"Moved: {len(moved)}")
    print(f"Failed: {len(failed)}")

    for item, reason in failed:
        print(
            f"  {item.source} -> {item.destination}: {reason}",
            file=sys.stderr,
        )

    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())

