from pathlib import Path

from file_organizer.cli import main


def touch(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("test", encoding="utf-8")


def test_dry_run_shows_plan_without_moving(
    tmp_path: Path,
    capsys,
) -> None:
    source = tmp_path / "photo.jpg"
    touch(source)

    exit_code = main([str(tmp_path), "--dry-run"])

    captured = capsys.readouterr()
    assert exit_code == 0
    assert "Planned moves:" in captured.out
    assert "photo.jpg" in captured.out
    assert source.exists()


def test_cancel_keeps_files_in_place(
    tmp_path: Path,
    monkeypatch,
    capsys,
) -> None:
    source = tmp_path / "photo.jpg"
    touch(source)
    monkeypatch.setattr("builtins.input", lambda _: "n")

    exit_code = main([str(tmp_path)])

    captured = capsys.readouterr()
    assert exit_code == 0
    assert "Cancelled." in captured.out
    assert source.exists()


def test_confirmation_moves_files(
    tmp_path: Path,
    monkeypatch,
    capsys,
) -> None:
    source = tmp_path / "photo.jpg"
    touch(source)
    monkeypatch.setattr("builtins.input", lambda _: "y")

    exit_code = main([str(tmp_path)])

    captured = capsys.readouterr()
    assert exit_code == 0
    assert "Moved: 1" in captured.out
    assert not source.exists()
    assert (tmp_path / "images" / "photo.jpg").is_file()


def test_yes_applies_without_prompt(
    tmp_path: Path,
    capsys,
) -> None:
    source = tmp_path / "photo.jpg"
    touch(source)

    exit_code = main([str(tmp_path), "--yes"])

    captured = capsys.readouterr()
    assert exit_code == 0
    assert "Moved: 1" in captured.out
    assert not source.exists()


def test_invalid_directory_returns_error(
    tmp_path: Path,
    capsys,
) -> None:
    exit_code = main([str(tmp_path / "missing")])

    captured = capsys.readouterr()
    assert exit_code == 2
    assert "Error:" in captured.err


def test_empty_directory_reports_no_files(
    tmp_path: Path,
    capsys,
) -> None:
    exit_code = main([str(tmp_path)])

    captured = capsys.readouterr()
    assert exit_code == 0
    assert "No files to organize." in captured.out
