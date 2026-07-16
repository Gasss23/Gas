"""Tests per .claude/hooks/session_end.sh — guard main-lock / detached HEAD."""
import os
import subprocess
from pathlib import Path

import pytest

HOOK = Path(__file__).parent.parent / ".claude" / "hooks" / "session_end.sh"


def _init_repo(path: Path) -> None:
    """Init un repo git minimale con un commit su main."""
    subprocess.run(["git", "init", str(path)], check=True, capture_output=True)
    # Forza branch "main" anche su git < 2.28
    subprocess.run(
        ["git", "symbolic-ref", "HEAD", "refs/heads/main"],
        cwd=path, check=True, capture_output=True,
    )
    subprocess.run(
        ["git", "config", "user.email", "test@test.invalid"],
        cwd=path, check=True, capture_output=True,
    )
    subprocess.run(
        ["git", "config", "user.name", "Test"],
        cwd=path, check=True, capture_output=True,
    )
    (path / "README.md").write_text("init\n")
    subprocess.run(["git", "add", "README.md"], cwd=path, check=True, capture_output=True)
    subprocess.run(
        ["git", "commit", "-m", "init"],
        cwd=path, check=True, capture_output=True,
    )


def _run_hook(repo: Path) -> subprocess.CompletedProcess:
    env = {**os.environ, "GAS_REPO_DIR": str(repo)}
    env.pop("CLAUDE_PROJECT_DIR", None)
    return subprocess.run(
        ["bash", str(HOOK)],
        env=env,
        capture_output=True,
        text=True,
    )


def _commit_count(repo: Path) -> int:
    r = subprocess.run(
        ["git", "rev-list", "--count", "HEAD"],
        cwd=repo, capture_output=True, text=True, check=True,
    )
    return int(r.stdout.strip())


def _add_allowlist_file(repo: Path) -> None:
    """Crea reports/test_report.md e .gas_history.json (entrambi nell'allowlist dell'hook).

    .gas_history.json deve esistere altrimenti git add fallisce su tutti i path
    (comportamento git: se un pathspec non matcha, l'intera invocazione esce 128
    e non staggia nulla — bug latente in produzione irrelevante perché il file
    esiste sempre a runtime).
    """
    reports = repo / "reports"
    reports.mkdir(exist_ok=True)
    (reports / "test_report.md").write_text("# test\n")
    (repo / ".gas_history.json").write_text("[]")


class TestSessionEndGuard:
    """
    T-hook-a/b/c: verifica il guard main-lock / detached HEAD di session_end.sh.
    Usa repo git temporanei reali — nessun mock del guard.
    """

    def test_hook_a_main_no_commit(self, tmp_path):
        """T-hook-a: HEAD su main + file allowlist modificato → 0 commit nuovi, exit 0, warning su stderr."""
        _init_repo(tmp_path)
        _add_allowlist_file(tmp_path)
        before = _commit_count(tmp_path)

        result = _run_hook(tmp_path)

        assert result.returncode == 0
        assert _commit_count(tmp_path) == before, (
            f"Attesi {before} commit, trovati {_commit_count(tmp_path)}; stderr: {result.stderr!r}"
        )
        assert result.stderr.strip(), "Warning atteso su stderr, ma stderr è vuoto"
        assert "main" in result.stderr or "main-lock" in result.stderr, (
            f"Warning non menziona 'main': {result.stderr!r}"
        )

    def test_hook_b_feature_branch_commits(self, tmp_path):
        """T-hook-b: HEAD su branch normale + file allowlist → commit creato, comportamento invariato."""
        _init_repo(tmp_path)
        subprocess.run(
            ["git", "checkout", "-b", "feature/test-hook"],
            cwd=tmp_path, check=True, capture_output=True,
        )
        _add_allowlist_file(tmp_path)
        before = _commit_count(tmp_path)

        result = _run_hook(tmp_path)

        assert result.returncode == 0
        assert _commit_count(tmp_path) == before + 1, (
            f"Atteso 1 commit in più (prima={before}, dopo={_commit_count(tmp_path)}); "
            f"stdout={result.stdout!r} stderr={result.stderr!r}"
        )

    def test_hook_c_detached_head_no_commit(self, tmp_path):
        """T-hook-c: HEAD detached → 0 commit nuovi, exit 0, warning su stderr."""
        _init_repo(tmp_path)
        head_sha = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=tmp_path, capture_output=True, text=True, check=True,
        ).stdout.strip()
        subprocess.run(
            ["git", "checkout", "--detach", head_sha],
            cwd=tmp_path, check=True, capture_output=True,
        )
        _add_allowlist_file(tmp_path)
        before = _commit_count(tmp_path)

        result = _run_hook(tmp_path)

        assert result.returncode == 0
        assert _commit_count(tmp_path) == before, (
            f"Attesi {before} commit, trovati {_commit_count(tmp_path)}; stderr: {result.stderr!r}"
        )
        assert result.stderr.strip(), "Warning atteso su stderr, ma stderr è vuoto"
        assert "detach" in result.stderr.lower() or "main-lock" in result.stderr, (
            f"Warning non menziona 'detach': {result.stderr!r}"
        )
