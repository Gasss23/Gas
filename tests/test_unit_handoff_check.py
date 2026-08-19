"""Tests per scripts/check_handoff.py e scripts/check_verdetto.py.

Usa repo git temporanei reali — nessun mock della logica git.
Stile: test_unit_hooks.py (pytest, tmp_path, subprocess).
"""
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).parent.parent
CHECK_HANDOFF = REPO_ROOT / "scripts" / "check_handoff.py"
CHECK_VERDETTO = REPO_ROOT / "scripts" / "check_verdetto.py"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _init_repo(path: Path) -> None:
    """Init repo git minimale con commit iniziale su main."""
    subprocess.run(["git", "init", str(path)], check=True, capture_output=True)
    subprocess.run(
        ["git", "symbolic-ref", "HEAD", "refs/heads/main"],
        cwd=path, check=True, capture_output=True,
    )
    for cmd in (
        ["git", "config", "user.email", "test@test.invalid"],
        ["git", "config", "user.name", "Test"],
    ):
        subprocess.run(cmd, cwd=path, check=True, capture_output=True)
    (path / "README.md").write_text("init\n")
    subprocess.run(["git", "add", "README.md"], cwd=path, check=True, capture_output=True)
    subprocess.run(["git", "commit", "-m", "init"], cwd=path, check=True, capture_output=True)


def _commit_all(path: Path, msg: str) -> str:
    """Stage tutto e committa. Ritorna lo SHA."""
    subprocess.run(["git", "add", "-A"], cwd=path, check=True, capture_output=True)
    subprocess.run(["git", "commit", "-m", msg], cwd=path, check=True, capture_output=True)
    return subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=path, capture_output=True, text=True, check=True,
    ).stdout.strip()


def _branch(path: Path, name: str) -> None:
    subprocess.run(["git", "checkout", "-b", name], cwd=path, check=True, capture_output=True)


def _fake_origin(work: Path, bare: Path) -> None:
    """Collega bare come origin e pusha main."""
    bare.mkdir()
    subprocess.run(["git", "init", "--bare", str(bare)], check=True, capture_output=True)
    subprocess.run(
        ["git", "remote", "add", "origin", str(bare)],
        cwd=work, check=True, capture_output=True,
    )
    subprocess.run(["git", "push", "origin", "main"], cwd=work, check=True, capture_output=True)


def _run_check_handoff(repo: Path, base: str | None = None) -> subprocess.CompletedProcess:
    args = [sys.executable, str(CHECK_HANDOFF)]
    if base:
        args.append(base)
    return subprocess.run(args, capture_output=True, text=True, cwd=repo)


def _run_check_verdetto(repo: Path, base: str | None = None) -> subprocess.CompletedProcess:
    args = [sys.executable, str(CHECK_VERDETTO)]
    if base:
        args.append(base)
    return subprocess.run(args, capture_output=True, text=True, cwd=repo)


def _write_handoff(repo: Path, stat_block: str, sec4: str = "nessun diff motore, revisore non richiesto.") -> None:
    """Scrive reports/handoff.md con §2 e §4 controllati."""
    (repo / "reports").mkdir(exist_ok=True)
    content = f"""# HANDOFF

**Sessione:** test

## §0 DECISIONI UMANE RICHIESTE

Nessuna.

## §1 SCOPE & ESITO FETTE

test

## §2 GIT DIFF --STAT (sessione)

```
{stat_block}
```

## §3 GIT LOG --ONELINE (sessione)

```
abc1234 test commit
```

## §4 VERDETTO DEL REVISORE (per commit motore)

{sec4}

## §5 DELTA TEST DEL MOTORE

Nessuna modifica a gas.py/tests/.

## §6 STATO CI

CI NON VERIFICATA (gh assente).

## §7 RISERVE APERTE

Nessuna.
"""
    (repo / "reports" / "handoff.md").write_text(content)


# ---------------------------------------------------------------------------
# Tests check_handoff.py
# ---------------------------------------------------------------------------

class TestCheckHandoff:

    def test_omits_file_exits_1(self, tmp_path):
        """Handoff che omette un file reale → exit 1."""
        work = tmp_path / "work"
        _init_repo(work)
        _fake_origin(work, tmp_path / "bare")
        _branch(work, "feature/test")

        # Crea due file, mette solo uno nell'handoff
        (work / "reports").mkdir(exist_ok=True)
        (work / "file_a.txt").write_text("a\n")
        _write_handoff(work, " file_a.txt | 1 +\n 1 file changed, 1 insertion(+)")
        (work / "file_b.txt").write_text("b\n")  # file reale omesso dal §2

        base = subprocess.run(
            ["git", "merge-base", "origin/main", "HEAD"],
            cwd=work, capture_output=True, text=True, check=True,
        ).stdout.strip()
        _commit_all(work, "add files")

        result = _run_check_handoff(work, base)

        assert result.returncode == 1, f"Atteso exit 1, got {result.returncode}; stderr={result.stderr!r}"
        assert "file_b.txt" in result.stderr, f"Deve citare il file omesso: {result.stderr!r}"

    def test_correct_handoff_exits_0(self, tmp_path):
        """Handoff corretto (set esatto) → exit 0."""
        work = tmp_path / "work"
        _init_repo(work)
        _fake_origin(work, tmp_path / "bare")
        _branch(work, "feature/test")

        (work / "reports").mkdir(exist_ok=True)
        (work / "file_a.txt").write_text("a\n")
        _write_handoff(
            work,
            " file_a.txt           |  1 +\n"
            " reports/handoff.md   | 40 ++++\n"
            " 2 files changed, 41 insertions(+)",
        )

        base = subprocess.run(
            ["git", "merge-base", "origin/main", "HEAD"],
            cwd=work, capture_output=True, text=True, check=True,
        ).stdout.strip()
        _commit_all(work, "add files")

        result = _run_check_handoff(work, base)

        assert result.returncode == 0, f"Atteso exit 0, got {result.returncode}; out={result.stdout!r} err={result.stderr!r}"

    def test_allowlist_ultima_risposta_exits_0(self, tmp_path):
        """Solo ultima_risposta.md in più rispetto al §2 → exit 0 (allowlist)."""
        work = tmp_path / "work"
        _init_repo(work)
        _fake_origin(work, tmp_path / "bare")
        _branch(work, "feature/test")

        (work / "reports").mkdir(exist_ok=True)
        (work / "file_a.txt").write_text("a\n")
        # ultima_risposta.md è nell'allowlist, non deve comparire nel §2
        (work / "reports" / "ultima_risposta.md").write_text("risposta\n")
        _write_handoff(
            work,
            " file_a.txt           |  1 +\n"
            " reports/handoff.md   | 40 ++++\n"
            " 2 files changed, 41 insertions(+)",
        )

        base = subprocess.run(
            ["git", "merge-base", "origin/main", "HEAD"],
            cwd=work, capture_output=True, text=True, check=True,
        ).stdout.strip()
        _commit_all(work, "add files")

        result = _run_check_handoff(work, base)

        assert result.returncode == 0, (
            f"ultima_risposta.md è in allowlist: atteso exit 0, got {result.returncode}; "
            f"stderr={result.stderr!r}"
        )

    def test_handoff_not_in_diff_exits_0(self, tmp_path):
        """reports/handoff.md non toccato nella sessione → exit 0 'non applicabile'."""
        work = tmp_path / "work"
        _init_repo(work)
        _fake_origin(work, tmp_path / "bare")
        _branch(work, "feature/test")

        # Modifica solo file_a.txt, NON reports/handoff.md
        (work / "file_a.txt").write_text("a\n")

        base = subprocess.run(
            ["git", "merge-base", "origin/main", "HEAD"],
            cwd=work, capture_output=True, text=True, check=True,
        ).stdout.strip()
        _commit_all(work, "add file_a")

        result = _run_check_handoff(work, base)

        assert result.returncode == 0, f"Atteso exit 0 (non applicabile), got {result.returncode}"
        assert "non applicabile" in result.stdout.lower(), (
            f"Deve stampare 'non applicabile': {result.stdout!r}"
        )

    def test_on_main_exits_0(self, tmp_path):
        """Su branch main → exit 0 'non applicabile'."""
        work = tmp_path / "work"
        _init_repo(work)
        # HEAD rimane su main (nessun branch checkout)

        result = _run_check_handoff(work)

        assert result.returncode == 0, f"Atteso exit 0 su main, got {result.returncode}"
        assert "non applicabile" in result.stdout.lower() or "non applicabile" in result.stderr.lower(), (
            f"Deve stampare 'non applicabile': out={result.stdout!r} err={result.stderr!r}"
        )

    def test_nonascii_filename_check_handoff(self, tmp_path):
        """File con nome non-ASCII (caffè.txt) dichiarato correttamente in §2 → exit 0.

        Senza core.quotePath=false, git diff --name-only restituisce
        '"caff\\303\\250.txt"' (quoted) che non corrisponde a 'caffè.txt'
        e il check avrebbe dato exit 1.
        """
        work = tmp_path / "work"
        _init_repo(work)
        _fake_origin(work, tmp_path / "bare")
        _branch(work, "feature/test")

        (work / "reports").mkdir(exist_ok=True)
        (work / "caffè.txt").write_text("contenuto\n", encoding="utf-8")
        _write_handoff(
            work,
            " caffè.txt          |  1 +\n"
            " reports/handoff.md | 40 ++++\n"
            " 2 files changed, 41 insertions(+)",
        )

        base = subprocess.run(
            ["git", "merge-base", "origin/main", "HEAD"],
            cwd=work, capture_output=True, text=True, check=True,
        ).stdout.strip()
        _commit_all(work, "add non-ASCII file")

        result = _run_check_handoff(work, base)

        assert result.returncode == 0, (
            f"File non-ASCII: atteso exit 0 (core.quotePath=false), "
            f"got {result.returncode}; stderr={result.stderr!r}"
        )


# ---------------------------------------------------------------------------
# Tests check_verdetto.py
# ---------------------------------------------------------------------------

class TestCheckVerdetto:

    def _setup_branch_with_handoff(self, work: Path, bare: Path, sec4: str) -> str:
        """Init repo, branch feature, scrive handoff con §4 dato. Ritorna BASE."""
        _init_repo(work)
        _fake_origin(work, bare)
        _branch(work, "feature/test")

        (work / "reports").mkdir(exist_ok=True)
        # Crea un file motore fittizio da citare
        motore = work / "gas_fake.py"
        motore.write_text("line1\nline2\nline3\nline4\nline5\n")

        base = subprocess.run(
            ["git", "merge-base", "origin/main", "HEAD"],
            cwd=work, capture_output=True, text=True, check=True,
        ).stdout.strip()

        _write_handoff(work, " gas_fake.py | 5 +++++\n reports/handoff.md | 40 ++++\n 2 files changed", sec4)
        _commit_all(work, "add engine file and handoff")
        return base

    def test_invalid_path_line_ref_exits_1(self, tmp_path):
        """Citazione path:riga con riga inesistente in §4 → exit 1."""
        work = tmp_path / "work"
        bare = tmp_path / "bare"
        # gas_fake.py ha 5 righe; cito riga 999
        sec4 = "Approvato. Vedi gas_fake.py:999 — tutto ok."
        base = self._setup_branch_with_handoff(work, bare, sec4)

        result = _run_check_verdetto(work, base)

        assert result.returncode == 1, (
            f"Citazione riga inesistente: atteso exit 1, got {result.returncode}; "
            f"out={result.stdout!r} err={result.stderr!r}"
        )
        assert "999" in result.stderr, f"Deve citare la riga errata: {result.stderr!r}"

    def test_valid_ref_exits_0(self, tmp_path):
        """Citazione path:riga valida (riga esiste nel file) → exit 0."""
        work = tmp_path / "work"
        bare = tmp_path / "bare"
        # gas_fake.py ha 5 righe; cito riga 3 (valida)
        sec4 = "Approvato. Vedi gas_fake.py:3 — funzione ok."
        base = self._setup_branch_with_handoff(work, bare, sec4)

        result = _run_check_verdetto(work, base)

        assert result.returncode == 0, (
            f"Citazione valida: atteso exit 0, got {result.returncode}; "
            f"err={result.stderr!r}"
        )

    def test_no_diff_motore_exits_0(self, tmp_path):
        """§4 dichiara nessun diff motore → exit 0 'non applicabile'."""
        work = tmp_path / "work"
        bare = tmp_path / "bare"
        sec4 = "nessun diff motore, revisore non richiesto."
        base = self._setup_branch_with_handoff(work, bare, sec4)

        result = _run_check_verdetto(work, base)

        assert result.returncode == 0, (
            f"nessun diff motore: atteso exit 0, got {result.returncode}; "
            f"err={result.stderr!r}"
        )
        assert "non applicabile" in result.stdout.lower(), (
            f"Deve stampare 'non applicabile': {result.stdout!r}"
        )

    def test_nota_mitigated_not_closed(self, tmp_path):
        """Output di check_verdetto deve dichiarare MITIGATO, non CHIUSO."""
        work = tmp_path / "work"
        bare = tmp_path / "bare"
        sec4 = "Approvato. Vedi gas_fake.py:2."
        base = self._setup_branch_with_handoff(work, bare, sec4)

        result = _run_check_verdetto(work, base)

        combined = result.stdout + result.stderr
        assert "MITIGATO" in combined, (
            f"Output deve contenere 'MITIGATO' (not CHIUSO): {combined!r}"
        )
        assert "CHIUSO" not in combined, (
            f"Output NON deve contenere 'CHIUSO': {combined!r}"
        )

    def test_nonascii_filename_check_verdetto(self, tmp_path):
        """File con nome non-ASCII (caffè.txt) citato in §4 → exit 0.

        Senza core.quotePath=false, _session_files restituisce
        '"caff\\303\\250.txt"' (quoted); il path 'caffè.txt' non verrebbe
        trovato nel diff e il check avrebbe dato exit 1.
        """
        work = tmp_path / "work"
        bare = tmp_path / "bare"
        _init_repo(work)
        _fake_origin(work, bare)
        _branch(work, "feature/test")

        (work / "reports").mkdir(exist_ok=True)
        (work / "caffè.txt").write_text(
            "line1\nline2\nline3\nline4\nline5\n", encoding="utf-8"
        )

        base = subprocess.run(
            ["git", "merge-base", "origin/main", "HEAD"],
            cwd=work, capture_output=True, text=True, check=True,
        ).stdout.strip()

        sec4 = "Approvato. Vedi caffè.txt:3 — test non-ASCII ok."
        _write_handoff(
            work,
            " caffè.txt          | 5 +++++\n"
            " reports/handoff.md | 40 ++++\n"
            " 2 files changed",
            sec4,
        )
        _commit_all(work, "add non-ASCII file")

        result = _run_check_verdetto(work, base)

        assert result.returncode == 0, (
            f"File non-ASCII: atteso exit 0 (core.quotePath=false), "
            f"got {result.returncode}; err={result.stderr!r}"
        )
