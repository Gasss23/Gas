"""Tests per scripts/gasmerge.sh — finding R-gasmerge-failopen.

Stub pattern: fake_bin/ preposta al PATH con gh e git fittizi.
GAS_REPO_DIR: punta a repo temporanei reali (nessun side effect su ~/Gas).
"""
import os
import subprocess
from pathlib import Path

import pytest

GASMERGE = Path(os.environ.get("GASMERGE_SCRIPT", str(
    Path(__file__).parent.parent / "scripts" / "gasmerge.sh"
)))


# ---------------------------------------------------------------------------
# Helpers repo git
# ---------------------------------------------------------------------------

def _init_repo(path: Path) -> None:
    """Init un repo git minimale con un commit su main."""
    subprocess.run(["git", "init", str(path)], check=True, capture_output=True)
    subprocess.run(["git", "symbolic-ref", "HEAD", "refs/heads/main"],
                   cwd=path, check=True, capture_output=True)
    subprocess.run(["git", "config", "user.email", "test@test.invalid"],
                   cwd=path, check=True, capture_output=True)
    subprocess.run(["git", "config", "user.name", "Test"],
                   cwd=path, check=True, capture_output=True)
    (path / "README.md").write_text("init\n")
    subprocess.run(["git", "add", "README.md"], cwd=path, check=True, capture_output=True)
    subprocess.run(["git", "commit", "-m", "init"], cwd=path, check=True, capture_output=True)


def _setup_with_origin(tmp_path: Path, branch: str = "feat") -> tuple[Path, Path]:
    """Crea work + bare origin con branch pushato, HEAD su main."""
    bare = tmp_path / "bare"
    bare.mkdir()
    subprocess.run(["git", "init", "--bare", str(bare)], check=True, capture_output=True)

    work = tmp_path / "work"
    _init_repo(work)
    subprocess.run(["git", "remote", "add", "origin", str(bare)],
                   cwd=work, check=True, capture_output=True)
    subprocess.run(["git", "push", "origin", "main"], cwd=work, check=True, capture_output=True)
    subprocess.run(["git", "checkout", "-b", branch], cwd=work, check=True, capture_output=True)
    subprocess.run(["git", "push", "origin", branch], cwd=work, check=True, capture_output=True)
    subprocess.run(["git", "checkout", "main"], cwd=work, check=True, capture_output=True)
    return work, bare


# ---------------------------------------------------------------------------
# Helpers stub binari
# ---------------------------------------------------------------------------

def _make_stub_gh(
    fake_bin: Path,
    state: str = "OPEN",
    ci_rc: int = 0,
    checks_json: str = '[{"name":"unit-suite","bucket":"pass"}]',
) -> None:
    """Stub gh parametrico — risponde ai comandi usati da gasmerge."""
    stub = fake_bin / "gh"
    stub.write_text(f"""#!/usr/bin/env bash
case "$*" in
  *"headRefName,title,state"*)
    printf '{{"headRefName":"feat","title":"Test PR","state":"{state}"}}\\n' > /tmp/gaspr.json
    exit 0 ;;
  *"--watch"*)
    exit {ci_rc} ;;
  *"name,bucket"*)
    printf '%s\\n' '{checks_json}'
    exit 0 ;;
  *"headRefOid"*)
    echo "abc1234def5678abc1234def5678abc1234de"
    exit 0 ;;
  *"pr merge"*)
    exit 0 ;;
  *)
    exit 0 ;;
esac
""")
    stub.chmod(0o755)


def _make_stub_jq_broken(fake_bin: Path) -> None:
    """Stub jq: presente in PATH ma fallisce su --version (simula jq rotto)."""
    stub = fake_bin / "jq"
    stub.write_text("#!/usr/bin/env bash\nexit 1\n")
    stub.chmod(0o755)


def _make_stub_git_grep_fail(fake_bin: Path, rc: int = 2) -> None:
    """Stub git: intercetta 'git grep' con exit rc; delega il resto al git reale."""
    stub = fake_bin / "git"
    stub.write_text(f"""#!/usr/bin/env bash
if [ "$1" = "grep" ]; then exit {rc}; fi
exec /usr/bin/git "$@"
""")
    stub.chmod(0o755)


def _make_stub_git_diff_name_only_fail(fake_bin: Path, rc: int = 5) -> None:
    """Stub git: intercetta 'git diff --name-only' con exit rc; delega il resto."""
    stub = fake_bin / "git"
    stub.write_text(f"""#!/usr/bin/env bash
if [ "$1" = "diff" ] && printf '%s\\n' "$@" | grep -q -- '--name-only'; then
  exit {rc}
fi
exec /usr/bin/git "$@"
""")
    stub.chmod(0o755)


# ---------------------------------------------------------------------------
# Runner principale
# ---------------------------------------------------------------------------

def _run(repo: Path, fake_bin: Path, args: list[str] | None = None) -> subprocess.CompletedProcess:
    env = {
        **os.environ,
        "GAS_REPO_DIR": str(repo),
        "PATH": str(fake_bin) + ":" + os.environ.get("PATH", ""),
    }
    cmd = ["bash", str(GASMERGE)] + (args if args is not None else ["123"])
    return subprocess.run(cmd, env=env, capture_output=True, text=True)


# ---------------------------------------------------------------------------
# Fetta 1c — validazione argomento PR
# ---------------------------------------------------------------------------

class TestArgValidation:
    """T-gasmerge-a/b: argomento assente o non numerico → exit 2."""

    def test_no_arg_exits_2(self, tmp_path):
        """Nessun argomento → exit 2, testo d'uso su stderr, nessun numero di parametro."""
        fake_bin = tmp_path / "bin"
        fake_bin.mkdir()
        result = _run(tmp_path, fake_bin, args=[])
        assert result.returncode == 2, (
            f"Atteso exit 2, got {result.returncode}; stderr={result.stderr!r}"
        )
        assert "uso:" in result.stderr, f"Testo d'uso atteso su stderr: {result.stderr!r}"
        # vecchio script stampava "bash: 1: uso:..." con il numero del parametro
        assert result.stderr.strip().startswith("uso:"), (
            f"stderr deve iniziare con 'uso:', non con junk bash: {result.stderr!r}"
        )

    def test_non_numeric_arg_exits_2(self, tmp_path):
        """Argomento non numerico → exit 2, argomento citato nel messaggio."""
        fake_bin = tmp_path / "bin"
        fake_bin.mkdir()
        result = _run(tmp_path, fake_bin, args=["abc"])
        assert result.returncode == 2, (
            f"Atteso exit 2, got {result.returncode}; stderr={result.stderr!r}"
        )
        assert "uso:" in result.stderr, f"Testo d'uso atteso su stderr: {result.stderr!r}"
        assert "abc" in result.stderr, (
            f"L'argomento errato deve essere citato nel messaggio: {result.stderr!r}"
        )


# ---------------------------------------------------------------------------
# Fetta 1b — jq functional check
# ---------------------------------------------------------------------------

class TestJqCheck:
    """T-gasmerge-c: jq presente ma rotto → exit non-zero con messaggio esplicito."""

    def test_broken_jq_exits_with_message(self, tmp_path):
        """jq assente/rotto → exit != 0, messaggio errore che menziona jq.

        Lo stub jq è presente in PATH (command -v passerebbe) ma fallisce su
        jq --version: distingue presence-check da functional-check (fetta 1b).
        """
        fake_bin = tmp_path / "bin"
        fake_bin.mkdir()
        _make_stub_jq_broken(fake_bin)
        result = _run(tmp_path, fake_bin, args=["42"])
        assert result.returncode != 0, (
            f"Atteso exit non-zero con jq rotto, got 0; stdout={result.stdout!r}"
        )
        assert "jq" in result.stdout.lower(), (
            f"Messaggio errore deve menzionare 'jq': stdout={result.stdout!r}"
        )
        assert "ERRORE" in result.stdout, (
            f"Messaggio deve contenere 'ERRORE': {result.stdout!r}"
        )


# ---------------------------------------------------------------------------
# PR state check (presente anche in vecchio script — test di regressione)
# ---------------------------------------------------------------------------

class TestPRState:
    """T-gasmerge-d: PR non OPEN → BLOCCO (guard già in vecchio script)."""

    def test_pr_not_open_blocks(self, tmp_path):
        """PR MERGED → BLOCCO, exit non-zero."""
        work, _ = _setup_with_origin(tmp_path)
        fake_bin = tmp_path / "bin"
        fake_bin.mkdir()
        _make_stub_gh(fake_bin, state="MERGED")
        result = _run(work, fake_bin)
        assert result.returncode != 0, (
            f"Atteso exit non-zero, got 0; stdout={result.stdout!r}"
        )
        assert "BLOCCO" in result.stdout and "MERGED" in result.stdout, (
            f"Output deve contenere BLOCCO e MERGED: {result.stdout!r}"
        )


# ---------------------------------------------------------------------------
# Fetta 2a — git grep fail-closed
# ---------------------------------------------------------------------------

class TestIPGuard:
    """T-gasmerge-e/f: invariante IP fail-closed su tutto l'albero."""

    def test_git_grep_error_blocks(self, tmp_path):
        """git grep esce rc=2 (errore reale) → BLOCCO, non '0 match OK'.

        Vecchio script: git grep dentro un `if` — rc=2 trattato come nessun match.
        """
        work, _ = _setup_with_origin(tmp_path)
        fake_bin = tmp_path / "bin"
        fake_bin.mkdir()
        _make_stub_gh(fake_bin)
        _make_stub_git_grep_fail(fake_bin, rc=2)
        result = _run(work, fake_bin)
        assert result.returncode != 0, (
            f"Atteso exit non-zero con git grep rc=2, got 0; stdout={result.stdout!r}"
        )
        assert "BLOCCO" in result.stdout, f"Atteso BLOCCO: {result.stdout!r}"
        assert "0 match OK" not in result.stdout, (
            f"'0 match OK' non deve apparire quando git grep fallisce: {result.stdout!r}"
        )

    def test_ip_outside_reports_blocks(self, tmp_path):
        """IP in README.md (fuori da reports/) → BLOCCO con match stampato.

        Vecchio script: git grep limitato a -- reports/ → 0 match → '0 match OK'.
        """
        bare = tmp_path / "bare"
        bare.mkdir()
        subprocess.run(["git", "init", "--bare", str(bare)], check=True, capture_output=True)

        work = tmp_path / "work"
        _init_repo(work)
        subprocess.run(["git", "remote", "add", "origin", str(bare)],
                       cwd=work, check=True, capture_output=True)
        subprocess.run(["git", "push", "origin", "main"], cwd=work, check=True, capture_output=True)
        subprocess.run(["git", "checkout", "-b", "feat"], cwd=work, check=True, capture_output=True)

        # IP in README.md — fuori da reports/
        (work / "README.md").write_text("server: 192.168.1.100\n")
        subprocess.run(["git", "add", "README.md"], cwd=work, check=True, capture_output=True)
        subprocess.run(["git", "commit", "-m", "add ip"], cwd=work, check=True, capture_output=True)
        subprocess.run(["git", "push", "origin", "feat"], cwd=work, check=True, capture_output=True)
        subprocess.run(["git", "checkout", "main"], cwd=work, check=True, capture_output=True)

        fake_bin = tmp_path / "bin"
        fake_bin.mkdir()
        _make_stub_gh(fake_bin)
        result = _run(work, fake_bin)
        assert result.returncode != 0, (
            f"Atteso exit non-zero con IP nel branch, got 0; stdout={result.stdout!r}"
        )
        assert "BLOCCO" in result.stdout and "IP" in result.stdout, (
            f"Output deve contenere BLOCCO e IP: {result.stdout!r}"
        )
        assert "192.168.1.100" in result.stdout, (
            f"Match IP deve essere stampato: {result.stdout!r}"
        )


# ---------------------------------------------------------------------------
# Fetta 2c — git diff fail-closed
# ---------------------------------------------------------------------------

class TestDiffGuard:
    """T-gasmerge-g: git diff --name-only fail-closed."""

    def test_git_diff_name_only_error_blocks(self, tmp_path):
        """git diff --name-only esce rc=5 → BLOCCA, non 'nessuno (doc-only)'.

        Vecchio script: '|| true' maschera l'errore di git diff.
        """
        work, _ = _setup_with_origin(tmp_path)
        fake_bin = tmp_path / "bin"
        fake_bin.mkdir()
        _make_stub_gh(fake_bin)
        _make_stub_git_diff_name_only_fail(fake_bin, rc=5)
        result = _run(work, fake_bin)
        assert result.returncode != 0, (
            f"Atteso exit non-zero con git diff rc=5, got 0; stdout={result.stdout!r}"
        )
        assert "BLOCCO" in result.stdout, f"Atteso BLOCCO: {result.stdout!r}"
        assert "nessuno (doc-only)" not in result.stdout, (
            f"'nessuno (doc-only)' non deve apparire quando git diff fallisce: {result.stdout!r}"
        )
