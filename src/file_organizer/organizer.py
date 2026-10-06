"""Core planning and file movement logic."""

from __future__ import annotations

import shutil
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path


DEFAULT_RULES: dict[str, set[str]] = {
    "images": {".jpg", ".jpeg", ".png", ".gif", ".webp"},
    "documents": {".pdf", ".doc", ".docx", ".txt", ".md"},
    "videos": {".mp4", ".mov", ".avi", ".mkv"},
    "archives": {".zip", ".rar", ".7z", ".tar", ".gz"},
}


class OrganizerError(Exception):
    """Raised when a planning operation cannot be completed."""


@dataclass(frozen=True)
class MovePlanItem:
    """One source-to-destination movement."""

    source: Path
    destination: Path


def plan_moves(
    directory: str | Path,
    rules: Mapping[str, set[str]] | None = None,
) -> tuple[MovePlanItem, ...]:
    """Create a plan without changing the filesystem."""

    source_directory = Path(directory)

    if not source_directory.exists():
        raise OrganizerError(f"Directory does not exist: {source_directory}")

    if not source_directory.is_dir():
        raise OrganizerError(f"Path is not a directory: {source_directory}")

    active_rules = _normalize_rules(DEFAULT_RULES if rules is None else rules)

    try:
        entries = sorted(
            source_directory.iterdir(),
            key=lambda path: path.name.casefold(),
        )
    except OSError as exc:
        raise OrganizerError(f"Unable to read directory: {exc}") from exc

    reserved_destinations: set[Path] = set()
    plan: list[MovePlanItem] = []

    for entry in entries:
        if not entry.is_file():
            continue

        category = _find_category(entry.suffix, active_rules)
        if category is None:
            continue

        destination = _unique_destination(
            source_directory / category / entry.name,
            reserved_destinations,
        )
        reserved_destinations.add(destination)
        plan.append(MovePlanItem(source=entry, destination=destination))

    return tuple(plan)


def apply_moves(
    plan: tuple[MovePlanItem, ...],
) -> tuple[list[MovePlanItem], list[tuple[MovePlanItem, str]]]:
    """Apply a plan and return successful moves and failures."""

    moved: list[MovePlanItem] = []
    failed: list[tuple[MovePlanItem, str]] = []

    for item in plan:
        try:
            if not item.source.is_file():
                raise OrganizerError("Source file does not exist")

            if item.destination.exists():
                raise OrganizerError("Destination already exists")

            item.destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(item.source), str(item.destination))
        except (OSError, OrganizerError) as exc:
            failed.append((item, str(exc)))
        else:
            moved.append(item)

    return moved, failed


def _normalize_rules(
    rules: Mapping[str, set[str]],
) -> dict[str, frozenset[str]]:
    return {
        category: frozenset(
            _normalize_extension(extension)
            for extension in extensions
        )
        for category, extensions in rules.items()
    }


def _normalize_extension(extension: str) -> str:
    normalized = extension.casefold()
    return normalized if normalized.startswith(".") else f".{normalized}"


def _find_category(
    extension: str,
    rules: Mapping[str, frozenset[str]],
) -> str | None:
    normalized_extension = extension.casefold()

    for category, extensions in rules.items():
        if normalized_extension in extensions:
            return category

    return None


def _unique_destination(path: Path, reserved: set[Path]) -> Path:
    candidate = path
    counter = 1

    while candidate.exists() or candidate in reserved:
        candidate = path.with_name(f"{path.stem} ({counter}){path.suffix}")
        counter += 1

    return candidate

