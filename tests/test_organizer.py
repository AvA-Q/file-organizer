from pathlib import Path

import pytest

from file_organizer import (
    MovePlanItem,
    OrganizerError,
    apply_moves,
    plan_moves,
)


def touch(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("test", encoding="utf-8")


def test_plan_moves_classifies_known_files(tmp_path: Path) -> None:
    touch(tmp_path / "photo.JPG")
    touch(tmp_path / "report.pdf")
    touch(tmp_path / "movie.mp4")
    touch(tmp_path / "archive.zip")

    plan = plan_moves(tmp_path)
    planned = {
        item.source.name: item.destination.relative_to(tmp_path)
        for item in plan
    }

    assert planned == {
        "photo.JPG": Path("images/photo.JPG"),
        "report.pdf": Path("documents/report.pdf"),
        "movie.mp4": Path("videos/movie.mp4"),
        "archive.zip": Path("archives/archive.zip"),
    }


def test_plan_moves_ignores_unknown_files(tmp_path: Path) -> None:
    touch(tmp_path / "notes.unknown")

    assert plan_moves(tmp_path) == ()


def test_plan_moves_avoids_name_conflict(tmp_path: Path) -> None:
    touch(tmp_path / "photo.jpg")
    touch(tmp_path / "images/photo.jpg")

    plan = plan_moves(tmp_path)

    assert plan[0].destination.name == "photo (1).jpg"


def test_plan_moves_rejects_missing_directory(tmp_path: Path) -> None:
    with pytest.raises(OrganizerError, match="does not exist"):
        plan_moves(tmp_path / "missing")


def test_apply_moves_moves_files(tmp_path: Path) -> None:
    touch(tmp_path / "photo.jpg")
    plan = plan_moves(tmp_path)

    moved, failed = apply_moves(plan)

    assert len(moved) == 1
    assert failed == []
    assert (tmp_path / "images/photo.jpg").is_file()


def test_apply_moves_does_not_overwrite(tmp_path: Path) -> None:
    source = tmp_path / "photo.jpg"
    destination = tmp_path / "images/photo.jpg"
    touch(source)
    touch(destination)

    moved, failed = apply_moves((MovePlanItem(source, destination),))

    assert moved == []
    assert len(failed) == 1
    assert failed[0][1] == "Destination already exists"
    assert source.exists()
    assert destination.exists()
