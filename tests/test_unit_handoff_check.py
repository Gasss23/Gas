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
        motore = work / "modules" / "gas_fake.py"
        motore.parent.mkdir(parents=True, exist_ok=True)
        motore.write_text("line1\nline2\nline3\nline4\nline5\n")

        base = subprocess.run(
            ["git", "merge-base", "origin/main", "HEAD"],
            cwd=work, capture_output=True, text=True, check=True,
        ).stdout.strip()

        _write_handoff(work, " modules/gas_fake.py | 5 +++++\n reports/handoff.md | 40 ++++\n 2 files changed", sec4)
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
        sec4 = "Approvato. Vedi gas_fake.py:3 — funzione ok; gas_fake.py:4 — ok."
        base = self._setup_branch_with_handoff(work, bare, sec4)

        result = _run_check_verdetto(work, base)

        assert result.returncode == 0, (
            f"Citazione valida: atteso exit 0, got {result.returncode}; "
            f"err={result.stderr!r}"
        )


    def test_nota_mitigated_not_closed(self, tmp_path):
        """Output di check_verdetto deve dichiarare MITIGATO, non CHIUSO."""
        work = tmp_path / "work"
        bare = tmp_path / "bare"
        sec4 = "Approvato. Vedi gas_fake.py:2 e gas_fake.py:3."
        base = self._setup_branch_with_handoff(work, bare, sec4)

        result = _run_check_verdetto(work, base)

        combined = result.stdout + result.stderr
        assert "MITIGATO" in combined, (
            f"Output deve contenere 'MITIGATO' (not CHIUSO): {combined!r}"
        )
        assert "CHIUSO" not in combined, (
            f"Output NON deve contenere 'CHIUSO': {combined!r}"
        )

    def _setup_with_context(self, work: Path, bare: Path, sec4: str) -> str:
        """Come _setup_branch_with_handoff, ma su main ci sono già file di
        CONTESTO (non toccati dal branch): modules/telegram/bot.py (4 righe) e
        due util.py omonimi in cartelle diverse."""
        _init_repo(work)
        (work / "modules" / "telegram").mkdir(parents=True)
        (work / "modules" / "telegram" / "bot.py").write_text("a\nb\nc\nd\n")
        for d in ("pkg_a", "pkg_b"):
            (work / d).mkdir()
            (work / d / "util.py").write_text("x\n")
        _commit_all(work, "contesto su main")
        _fake_origin(work, bare)
        _branch(work, "feature/test")
        (work / "modules" / "gas_fake.py").write_text("line1\nline2\nline3\n")
        base = subprocess.run(
            ["git", "merge-base", "origin/main", "HEAD"],
            cwd=work, capture_output=True, text=True, check=True,
        ).stdout.strip()
        _write_handoff(work, " modules/gas_fake.py | 3 +++\n reports/handoff.md | 40 ++++\n 2 files changed", sec4)
        _commit_all(work, "engine + handoff")
        return base

    def test_context_file_full_path_exits_0(self, tmp_path):
        """F-controlli-auto: file di contesto citato col path completo, non nel diff → OK."""
        sec4 = "Approvato. Vedi gas_fake.py:2, gas_fake.py:3 e modules/telegram/bot.py:3."
        base = self._setup_with_context(tmp_path / "work", tmp_path / "bare", sec4)
        result = _run_check_verdetto(tmp_path / "work", base)
        assert result.returncode == 0, f"err={result.stderr!r}"

    def test_context_short_name_unique_exits_0(self, tmp_path):
        """Nome corto (bot.py) che corrisponde a un solo file a HEAD → OK."""
        sec4 = "Approvato. gas_fake.py:1, gas_fake.py:2; bot.py:4 gira nello stesso thread."
        base = self._setup_with_context(tmp_path / "work", tmp_path / "bare", sec4)
        result = _run_check_verdetto(tmp_path / "work", base)
        assert result.returncode == 0, f"err={result.stderr!r}"

    def test_context_short_name_line_out_of_range_exits_1(self, tmp_path):
        """Nome corto risolto ma riga oltre la fine del file → exit 1."""
        sec4 = "Approvato. gas_fake.py:1, gas_fake.py:2, bot.py:99."
        base = self._setup_with_context(tmp_path / "work", tmp_path / "bare", sec4)
        result = _run_check_verdetto(tmp_path / "work", base)
        assert result.returncode == 1 and "99" in result.stderr, result.stderr

    def test_context_short_name_ambiguous_exits_1(self, tmp_path):
        """Nome corto che corrisponde a più file a HEAD → non verificabile, exit 1."""
        sec4 = "Approvato. gas_fake.py:1, gas_fake.py:2, util.py:1."
        base = self._setup_with_context(tmp_path / "work", tmp_path / "bare", sec4)
        result = _run_check_verdetto(tmp_path / "work", base)
        assert result.returncode == 1 and "ambiguo" in result.stderr, result.stderr

    def test_context_missing_file_exits_1(self, tmp_path):
        """File citato inesistente a HEAD (né nel diff né come nome) → exit 1."""
        sec4 = "Approvato. gas_fake.py:1, gas_fake.py:2, fantasma.py:1."
        base = self._setup_with_context(tmp_path / "work", tmp_path / "bare", sec4)
        result = _run_check_verdetto(tmp_path / "work", base)
        assert result.returncode == 1 and "fantasma.py" in result.stderr, result.stderr

    def test_r135_1_only_context_exits_1(self, tmp_path):
        """R-135-1: verdetto che cita SOLO file di contesto (nessun file del diff) → exit 1."""
        sec4 = "## VERDETTO: APPROVATO\nmodules/telegram/bot.py:3 e bot.py:4 ok."
        base = self._setup_with_context(tmp_path / "work", tmp_path / "bare", sec4)
        result = _run_check_verdetto(tmp_path / "work", base)
        assert result.returncode == 1 and "minimo 2" in result.stderr, result.stderr

    def test_r135_2_no_citations_exits_1(self, tmp_path):
        """R-135-2: verdetto senza alcun path:riga con diff motore → exit 1 (non 'nulla da verificare')."""
        sec4 = "APPROVATO — nessuna lezione nuova."
        base = self._setup_with_context(tmp_path / "work", tmp_path / "bare", sec4)
        result = _run_check_verdetto(tmp_path / "work", base)
        assert result.returncode == 1, f"out={result.stdout!r} err={result.stderr!r}"

    def test_r135_2_one_empty_verdict_among_many_exits_1(self, tmp_path):
        """R-135-2: con più verdetti nel §4, UNO vuoto basta a bocciare."""
        sec4 = ("### #1\n## VERDETTO: APPROVATO\ngas_fake.py:1 e gas_fake.py:2 ok.\n"
                "### #2\n## VERDETTO: APPROVATO\nnessuna lezione nuova.")
        base = self._setup_with_context(tmp_path / "work", tmp_path / "bare", sec4)
        result = _run_check_verdetto(tmp_path / "work", base)
        assert result.returncode == 1 and "verdetto 2" in result.stderr, result.stderr

    def test_r135_3_report_citations_do_not_count(self, tmp_path):
        """Le citazioni di reports/ (nel diff) non contano come elementi del codice revisionato."""
        sec4 = "## VERDETTO: APPROVATO\nreports/handoff.md:1, reports/handoff.md:2, gas_fake.py:1."
        base = self._setup_with_context(tmp_path / "work", tmp_path / "bare", sec4)
        result = _run_check_verdetto(tmp_path / "work", base)
        assert result.returncode == 1 and "minimo 2" in result.stderr, result.stderr

    def test_r135_4_phrase_does_not_exempt_motor_diff(self, tmp_path):
        """R-135-4: la frase 'nessun diff motore' nel §4 NON esenta se il diff tocca il motore.
        Sostituisce il vecchio test_no_diff_motore_exits_0, che codificava il by-pass."""
        sec4 = "nessun diff motore, revisore non richiesto."
        base = self._setup_with_context(tmp_path / "work", tmp_path / "bare", sec4)
        result = _run_check_verdetto(tmp_path / "work", base)
        assert result.returncode == 1, f"out={result.stdout!r} err={result.stderr!r}"

    def test_r135_4_no_motor_diff_not_applicable(self, tmp_path):
        """Diff di sessione senza motore → non applicabile, qualunque cosa dica il §4."""
        work, bare = tmp_path / "work", tmp_path / "bare"
        _init_repo(work)
        _fake_origin(work, bare)
        _branch(work, "feature/doc")
        base = subprocess.run(["git", "merge-base", "origin/main", "HEAD"], cwd=work,
                              capture_output=True, text=True, check=True).stdout.strip()
        (work / "docs.md").write_text("x\n")
        _write_handoff(work, " docs.md | 1 +\n reports/handoff.md | 40 ++++\n 2 files changed",
                       "APPROVATO senza citazioni")
        _commit_all(work, "doc only")
        result = _run_check_verdetto(work, base)
        assert result.returncode == 0 and "fuori dal perimetro" in result.stdout, result.stdout

    def _setup_doc_session(self, work: Path, bare: Path, sec4: str, extra: "dict | None" = None) -> str:
        """Sessione con file scelti (default: solo docs.md), handoff con §4 dato."""
        _init_repo(work)
        (work / "scripts").mkdir(exist_ok=True)
        (work / "scripts" / "esistente.py").write_text("a\nb\nc\n")
        _commit_all(work, "contesto")
        _fake_origin(work, bare)
        _branch(work, "feature/x")
        base = subprocess.run(["git", "merge-base", "origin/main", "HEAD"], cwd=work,
                              capture_output=True, text=True, check=True).stdout.strip()
        files = extra or {"docs.md": "x\n"}
        for rel, content in files.items():
            (work / rel).parent.mkdir(parents=True, exist_ok=True)
            (work / rel).write_text(content)
        stat = "".join(f" {rel} | 1 +\n" for rel in files) + " reports/handoff.md | 40 ++++\n"
        _write_handoff(work, stat, sec4)
        _commit_all(work, "sessione")
        return base

    def test_v2_citations_verified_outside_perimeter(self, tmp_path):
        """V-2: sessione fuori dal perimetro con citazioni inesistenti → exit 1 (prima: rc=0)."""
        sec4 = "Vedi scripts/file_che_non_esiste.py:999 e scripts/esistente.py:99999."
        base = self._setup_doc_session(tmp_path / "work", tmp_path / "bare", sec4)
        result = _run_check_verdetto(tmp_path / "work", base)
        assert result.returncode == 1, f"out={result.stdout!r} err={result.stderr!r}"
        assert "file_che_non_esiste.py" in result.stderr and "99999" in result.stderr

    def test_v2_valid_citations_outside_perimeter_exits_0(self, tmp_path):
        """V-2: fuori dal perimetro, citazioni valide → OK senza minimo per verdetto."""
        sec4 = "Vedi scripts/esistente.py:2."
        base = self._setup_doc_session(tmp_path / "work", tmp_path / "bare", sec4)
        result = _run_check_verdetto(tmp_path / "work", base)
        assert result.returncode == 0 and "fuori dal perimetro" in result.stdout, result.stdout

    def test_v1_gate_file_session_requires_verdict(self, tmp_path):
        """V-1: sessione che tocca SOLO un file del gate (scripts/check_verdetto.py) è nel
        perimetro → verdetto senza citazioni → exit 1."""
        sec4 = "APPROVATO — nessuna lezione nuova."
        base = self._setup_doc_session(tmp_path / "work", tmp_path / "bare", sec4,
                                       {"scripts/check_verdetto.py": "x = 1\ny = 2\n"})
        result = _run_check_verdetto(tmp_path / "work", base)
        assert result.returncode == 1 and "minimo 2" in result.stderr, result.stderr

    def test_v1_gate_file_session_with_citations_exits_0(self, tmp_path):
        """V-1: stessa sessione, verdetto con 2 citazioni del file del gate → OK."""
        sec4 = "## VERDETTO: APPROVATO\ncheck_verdetto.py:1 e scripts/check_verdetto.py:2 ok."
        base = self._setup_doc_session(tmp_path / "work", tmp_path / "bare", sec4,
                                       {"scripts/check_verdetto.py": "x = 1\ny = 2\n"})
        result = _run_check_verdetto(tmp_path / "work", base)
        assert result.returncode == 0, result.stderr

    def test_r136_2_markdown_variant_opens_new_verdict(self, tmp_path):
        """R-136-2: un secondo verdetto scritto `**Verdetto**: APPROVATO` senza citazioni
        non si fonde più col primo → exit 1."""
        sec4 = ("## VERDETTO: APPROVATO\ngas_fake.py:1 e gas_fake.py:2 ok.\n"
                "**Verdetto**: APPROVATO — nessuna lezione nuova.")
        base = self._setup_with_context(tmp_path / "work", tmp_path / "bare", sec4)
        result = _run_check_verdetto(tmp_path / "work", base)
        assert result.returncode == 1 and "verdetto 2" in result.stderr, result.stderr

    def test_r136_2_bare_esito_line_opens_new_verdict(self, tmp_path):
        """R-136-2: riga che apre con l'esito (`APPROVATO — …`) dopo un verdetto pieno → exit 1."""
        sec4 = ("## VERDETTO: APPROVATO\ngas_fake.py:1 e gas_fake.py:2 ok.\n"
                "APPROVATO — nessuna lezione nuova.")
        base = self._setup_with_context(tmp_path / "work", tmp_path / "bare", sec4)
        result = _run_check_verdetto(tmp_path / "work", base)
        assert result.returncode == 1 and "verdetto 2" in result.stderr, result.stderr

    def test_r136_2_list_item_esito_does_not_split(self, tmp_path):
        """Le righe di analisi `- Esito: **ok**` non aprono un verdetto (niente falsi positivi)."""
        sec4 = ("## VERDETTO: APPROVATO\n1. gas_fake.py:1 — ok\n   - Esito: **ok**.\n"
                "2. gas_fake.py:2 — ok\n   - Esito: **ok**.")
        base = self._setup_with_context(tmp_path / "work", tmp_path / "bare", sec4)
        result = _run_check_verdetto(tmp_path / "work", base)
        assert result.returncode == 0, result.stderr

    def test_r138_3_variants_open_and_prose_does_not(self, tmp_path):
        """R-138-3: 'Verdetto finale: APPROVATO' e 'Esito della review: BOCCIATO' aprono un
        verdetto; prosa ('Approvato il fix …'), voce di elenco 'verdetto nullo' e righe in
        un blocco di codice NO."""
        import importlib.util
        spec = importlib.util.spec_from_file_location("cv", CHECK_VERDETTO)
        cv = importlib.util.module_from_spec(spec); spec.loader.exec_module(cv)
        apre = ["## VERDETTO: APPROVATO", "Verdetto finale: APPROVATO",
                "Esito della review: BOCCIATO", "**Verdetto**: APPROVATO CON RISERVE",
                "APPROVATO — nessuna lezione nuova", "**APPROVATO CON RISERVE**"]
        non_apre = ["Approvato il fix precedente, ma resta un dubbio.",
                    "- verdetto nullo: «APPROVATO — nessuna lezione nuova»",
                    "   - Esito: **ok**.", "La review è APPROVATO? no"]
        for riga in apre:
            assert len(cv._blocchi_verdetto("intro\n" + riga + "\nx")) == 1 and \
                cv._blocchi_verdetto("intro\n" + riga + "\nx")[0].lstrip().startswith(riga.lstrip()[:3]), riga
        for riga in non_apre:
            assert cv._blocchi_verdetto(riga + "\nx") == [riga + "\nx"], riga
        fence = "## VERDETTO: APPROVATO\na.py:1\n```\nAPPROVATO — dentro il codice\n```\nb.py:2"
        assert len(cv._blocchi_verdetto(fence)) == 1

    def test_r138_2_rename_out_of_perimeter_counts_origin(self, tmp_path):
        """R-138-2: rename modules/x.py → docs/x.py: il path di origine è nel diff di sessione
        (prima --name-only mostrava solo la destinazione)."""
        import importlib.util
        spec = importlib.util.spec_from_file_location("cv", CHECK_VERDETTO)
        cv = importlib.util.module_from_spec(spec); spec.loader.exec_module(cv)
        work = tmp_path / "w"
        _init_repo(work)
        (work / "modules").mkdir()
        (work / "modules" / "x.py").write_text("a\nb\nc\nd\ne\n")
        (work / "modules" / "città.py").write_text("x\n")
        base = _commit_all(work, "base")
        (work / "docs").mkdir()
        subprocess.run(["git", "mv", "modules/x.py", "docs/x.py"], cwd=work, check=True)
        (work / "modules" / "città.py").write_text("y\n")
        _commit_all(work, "rename")
        files = cv._session_files(base, work)
        assert "modules/x.py" in files and "docs/x.py" in files, files
        assert "modules/città.py" in files, files

    def test_r136_5_doc_citations_do_not_count_when_code_in_diff(self, tmp_path):
        """R-136-5: diff con codice, verdetto che cita solo .md del diff → exit 1."""
        sec4 = "## VERDETTO: APPROVATO\nnote.md:1 e note.md:2 ok."
        base = self._setup_doc_session(tmp_path / "work", tmp_path / "bare", sec4,
                                       {"modules/codice.py": "a\nb\n", "note.md": "x\ny\n"})
        result = _run_check_verdetto(tmp_path / "work", base)
        assert result.returncode == 1 and "minimo 2" in result.stderr, result.stderr

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
