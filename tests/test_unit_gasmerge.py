"""Tests per scripts/gasmerge.sh — finding R-gasmerge-failopen.

Stub pattern: fake_bin/ preposta al PATH con gh e git fittizi.
GAS_REPO_DIR: punta a repo temporanei reali (nessun side effect su ~/Gas).
"""
import os
import shutil
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
    head_ref: str = "feat",
    on_watch: str = "",
) -> None:
    """Stub gh parametrico — risponde ai comandi usati da gasmerge.

    on_watch: comandi shell eseguiti durante l'attesa CI (`--watch`), prima dell'exit.
    """
    stub = fake_bin / "gh"
    stub.write_text(f"""#!/usr/bin/env bash
case "$*" in
  *"headRefName,title,state"*)
    printf '{{"headRefName":"{head_ref}","title":"Test PR","state":"{state}"}}\\n' > "$GASPR_JSON"
    exit 0 ;;
  *"--watch"*)
    {on_watch}
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
    """Stub git: intercetta 'git grep' con exit rc; delega il resto al git reale.

    Il path del git reale viene risolto QUI (in Python, prima che fake_bin venga
    preposta a PATH), così `exec real_git` nel corpo dello stub non può trovare
    lo stub stesso per ricorsione.
    """
    real_git = shutil.which("git") or "/usr/bin/git"
    stub = fake_bin / "git"
    stub.write_text(f"""#!/usr/bin/env bash
if [ "$1" = "grep" ]; then exit {rc}; fi
exec "{real_git}" "$@"
""")
    stub.chmod(0o755)


def _make_stub_git_diff_name_only_fail(fake_bin: Path, rc: int = 5) -> None:
    """Stub git: intercetta 'git diff --name-only' con exit rc; delega il resto.

    Il path del git reale viene risolto QUI (in Python), prima che fake_bin venga
    preposta a PATH — stessa strategia di _make_stub_git_grep_fail.
    """
    real_git = shutil.which("git") or "/usr/bin/git"
    stub = fake_bin / "git"
    stub.write_text(f"""#!/usr/bin/env bash
if printf '%s\\n' "$@" | grep -qx 'diff' && printf '%s\\n' "$@" | grep -q -- '--name-only'; then
  exit {rc}
fi
exec "{real_git}" "$@"
""")
    stub.chmod(0o755)


# ---------------------------------------------------------------------------
# Runner principale
# ---------------------------------------------------------------------------

def _locale_utf8() -> str | None:
    """V-2 #124/#125: un locale UTF-8 disponibile (dove un byte non UTF-8 attaccato a un IP
    lo nasconde a grep/git grep senza LC_ALL=C). None se il sistema non ne ha."""
    try:
        r = subprocess.run(["locale", "-a"], capture_output=True, text=True)
    except OSError:
        return None
    disponibili = {l.strip().lower().replace("utf8", "utf-8") for l in r.stdout.splitlines()}
    for loc in ("C.UTF-8", "en_US.UTF-8"):
        if loc.lower() in disponibili:
            return loc
    return None


def _run(repo: Path, fake_bin: Path, args: list[str] | None = None) -> subprocess.CompletedProcess:
    env = {
        **os.environ,
        "GAS_REPO_DIR": str(repo),
        "PATH": str(fake_bin) + ":" + os.environ.get("PATH", ""),
    }
    cmd = ["bash", str(GASMERGE)] + (args if args is not None else ["123"])
    # errors="replace": il gate IP stampa le righe bloccate così come sono (anche non UTF-8).
    return subprocess.run(cmd, env=env, capture_output=True, text=True, errors="replace")


def _run_with_stdin(
    repo: Path, fake_bin: Path, args: list[str] | None = None, stdin_data: str = ""
) -> subprocess.CompletedProcess:
    """Come _run, ma inietta stdin_data nel processo (per superare `read -r ANS`)."""
    env = {
        **os.environ,
        "GAS_REPO_DIR": str(repo),
        "PATH": str(fake_bin) + ":" + os.environ.get("PATH", ""),
    }
    cmd = ["bash", str(GASMERGE)] + (args if args is not None else ["123"])
    return subprocess.run(cmd, env=env, capture_output=True, text=True, input=stdin_data)


class TestFileTemporaneo:
    """R-153-2: il JSON della PR va in un file dal nome davvero casuale. Con le X non in
    fondo al template BSD mktemp crea il nome letterale: un file rimasto da un'esecuzione
    interrotta faceva uscire ogni gasmerge successivo con "File exists"."""

    def test_nome_casuale_e_residuo_letterale_non_blocca(self, tmp_path):
        work, _ = _setup_with_origin(tmp_path)
        tmpd = tmp_path / "tmpd"
        tmpd.mkdir()
        (tmpd / "gaspr.XXXXXX.json").write_text("")  # residui col nome letterale
        (tmpd / "gaspr.XXXXXX").write_text("")
        fake_bin = tmp_path / "bin"
        fake_bin.mkdir()
        log = tmp_path / "percorsi.log"
        stub = fake_bin / "gh"
        stub.write_text(f"""#!/usr/bin/env bash
case "$*" in
  *"headRefName,title,state"*)
    printf '%s\\n' "$GASPR_JSON" >> "{log}"
    printf '{{"headRefName":"feat","title":"T","state":"CLOSED"}}\\n' > "$GASPR_JSON"
    exit 0 ;;
  *) exit 0 ;;
esac
""")
        stub.chmod(0o755)
        env = {**os.environ, "GAS_REPO_DIR": str(work), "TMPDIR": str(tmpd),
               "PATH": f"{fake_bin}:{os.environ['PATH']}"}
        for _ in range(2):
            r = subprocess.run(["bash", str(GASMERGE), "123"], env=env,
                               capture_output=True, text=True)
            assert "File exists" not in r.stdout + r.stderr, r.stderr
            assert "BLOCCO: PR #123 è CLOSED" in r.stdout, r.stdout + r.stderr
        percorsi = log.read_text().split()
        assert len(percorsi) == 2 and percorsi[0] != percorsi[1], percorsi
        for p in percorsi:
            assert Path(p).parent == tmpd and "XXXXXX" not in Path(p).name, p
            assert not Path(p).exists(), f"il trap EXIT doveva rimuovere {p}"

    def test_mktemp_fallito_ferma_subito(self, tmp_path):
        """mktemp fallito (TMPDIR inesistente) → errore esplicito, gh mai chiamato."""
        work, _ = _setup_with_origin(tmp_path)
        fake_bin = tmp_path / "bin"
        fake_bin.mkdir()
        chiamate = tmp_path / "gh.log"
        stub = fake_bin / "gh"
        stub.write_text(f'#!/usr/bin/env bash\necho "$*" >> "{chiamate}"\nexit 0\n')
        stub.chmod(0o755)
        env = {**os.environ, "GAS_REPO_DIR": str(work), "TMPDIR": str(tmp_path / "manca"),
               "PATH": f"{fake_bin}:{os.environ['PATH']}"}
        r = subprocess.run(["bash", str(GASMERGE), "123"], env=env,
                           capture_output=True, text=True)
        assert r.returncode != 0, r.stdout
        assert "ERRORE: mktemp fallito" in r.stdout, r.stdout + r.stderr
        assert not chiamate.exists(), chiamate.read_text()


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
        # R-151-1: si ferma SUBITO al gate IP (non basta rc≠0: lezione #150).
        assert "--- FILE DI MOTORE ---" not in result.stdout, result.stdout
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
        (work / "README.md").write_text("server: 192.168.1.100\n")  # gasmerge-ip-ok
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
        assert "192.168.1.100" in result.stdout, (  # gasmerge-ip-ok
            f"Match IP deve essere stampato: {result.stdout!r}"
        )
        # V-1 verifica #125: il ramo "IP non allowlistati" deve FERMARE gasmerge,
        # non solo stampare BLOCCO (lezione #150: rc≠0 non basta).
        assert "--- FILE DI MOTORE ---" not in result.stdout, result.stdout


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


# ---------------------------------------------------------------------------
# R-144-1 / V-1 verifica esterna PR #121 — promemoria dal perimetro di review
# ---------------------------------------------------------------------------

class TestPerimetroPromemoria:
    """gasmerge legge .claude/perimetro_review.txt (main ∪ branch), non una regex propria."""

    def _repo(self, tmp_path: Path, perimetro: str | None, files: dict[str, str],
              perimetro_branch: str | None = None) -> Path:
        bare = tmp_path / "bare"
        bare.mkdir()
        subprocess.run(["git", "init", "--bare", str(bare)], check=True, capture_output=True)
        work = tmp_path / "work"
        _init_repo(work)
        if perimetro is not None:
            (work / ".claude").mkdir()
            (work / ".claude" / "perimetro_review.txt").write_text(perimetro)
            subprocess.run(["git", "add", "-A"], cwd=work, check=True, capture_output=True)
            subprocess.run(["git", "commit", "-m", "perimetro"], cwd=work,
                           check=True, capture_output=True)
        subprocess.run(["git", "remote", "add", "origin", str(bare)],
                       cwd=work, check=True, capture_output=True)
        subprocess.run(["git", "push", "origin", "main"], cwd=work, check=True, capture_output=True)
        subprocess.run(["git", "checkout", "-b", "feat"], cwd=work, check=True, capture_output=True)
        for name, content in files.items():
            (work / name).parent.mkdir(parents=True, exist_ok=True)
            (work / name).write_text(content)
        if perimetro_branch is not None:
            (work / ".claude").mkdir(exist_ok=True)
            (work / ".claude" / "perimetro_review.txt").write_text(perimetro_branch)
        subprocess.run(["git", "add", "-A"], cwd=work, check=True, capture_output=True)
        subprocess.run(["git", "commit", "-m", "modifica"], cwd=work, check=True, capture_output=True)
        subprocess.run(["git", "push", "origin", "feat"], cwd=work, check=True, capture_output=True)
        subprocess.run(["git", "checkout", "main"], cwd=work, check=True, capture_output=True)
        return work

    def _sezione(self, tmp_path: Path, work: Path) -> str:
        fake_bin = tmp_path / "bin"
        fake_bin.mkdir()
        _make_stub_gh(fake_bin)
        out = _run_with_stdin(work, fake_bin, stdin_data="\n").stdout
        assert "--- FILE DI MOTORE ---" in out, out
        return out.split("--- FILE DI MOTORE ---", 1)[1].split("--- PROVENIENZA SCRIPT ---", 1)[0]

    def test_voce_esatta_del_perimetro_e_motore(self, tmp_path):
        """gas_identity.md (fuori dalla vecchia regex) è nel perimetro → promemoria."""
        work = self._repo(tmp_path, "gas.py\ngas_identity.md\nclients/\n",
                          {"gas_identity.md": "x\n", "clients/voice/a.py": "y\n"})
        sez = self._sezione(tmp_path, work)
        assert "gas_identity.md" in sez and "clients/voice/a.py" in sez, sez
        assert "PERIMETRO DI REVIEW" in sez and "doc-only" not in sez, sez

    def test_path_non_utf8_non_nasconde_il_motore(self, tmp_path, monkeypatch):
        """R-167-1: in locale UTF-8 un path che finisce con un byte non UTF-8 si mangiava
        il newline in `read` e il file di motore seguente spariva dal promemoria."""
        loc = _locale_utf8()
        if loc is None:
            pytest.skip("nessun locale UTF-8 sul sistema")
        monkeypatch.setenv("LC_ALL", loc)
        # "a\udce9" = byte 0xE9 nel nome (surrogateescape del filesystem POSIX).
        work = self._repo(tmp_path, "gas.py\n", {"a\udce9": "x\n", "gas.py": "y\n"})
        sez = self._sezione(tmp_path, work)
        assert "\ngas.py\n" in sez and "doc-only" not in sez, repr(sez)

    def test_fuori_perimetro_e_doc_only(self, tmp_path):
        work = self._repo(tmp_path, "gas.py  # motore\nclients/\n",
                          {"docs/nota.md": "x\n", "clientsX.md": "y\n"})
        sez = self._sezione(tmp_path, work)
        assert "nessuno (doc-only)" in sez, sez

    def test_branch_che_restringe_non_si_declassa(self, tmp_path):
        """Il branch toglie gas_identity.md dal perimetro: conta ancora la versione di main."""
        work = self._repo(tmp_path, "gas_identity.md\n", {"gas_identity.md": "x\n"},
                          perimetro_branch="gas.py\n")
        sez = self._sezione(tmp_path, work)
        assert "gas_identity.md" in sez and "doc-only" not in sez, sez

    def test_rename_fuori_perimetro_resta_motore(self, tmp_path):
        """R-145-1: git mv gas_identity.md → docs/x.md non diventa 'doc-only'."""
        work = self._repo(tmp_path, "gas_identity.md\n", {"docs/altro.md": "z\n"})
        (work / "gas_identity.md").write_text("a\n" * 20)
        subprocess.run(["git", "add", "gas_identity.md"], cwd=work, check=True, capture_output=True)
        subprocess.run(["git", "commit", "-m", "identity"], cwd=work, check=True, capture_output=True)
        subprocess.run(["git", "push", "origin", "main"], cwd=work, check=True, capture_output=True)
        subprocess.run(["git", "checkout", "feat"], cwd=work, check=True, capture_output=True)
        subprocess.run(["git", "merge", "-q", "main"], cwd=work, check=True, capture_output=True)
        subprocess.run(["git", "mv", "gas_identity.md", "docs/x.md"], cwd=work,
                       check=True, capture_output=True)
        subprocess.run(["git", "commit", "-m", "rename"], cwd=work, check=True, capture_output=True)
        subprocess.run(["git", "push", "origin", "feat"], cwd=work, check=True, capture_output=True)
        subprocess.run(["git", "checkout", "main"], cwd=work, check=True, capture_output=True)
        sez = self._sezione(tmp_path, work)
        assert "gas_identity.md" in sez and "doc-only" not in sez, sez

    def test_nome_non_ascii_nel_perimetro(self, tmp_path):
        """R-145-1: clients/caffè.py non viene quotato e resta nel perimetro."""
        work = self._repo(tmp_path, "clients/\n", {"clients/caffè.py": "x\n"})
        sez = self._sezione(tmp_path, work)
        assert "clients/caffè.py" in sez and "doc-only" not in sez, sez

    def test_tag_origin_main_non_dirotta_il_promemoria(self, tmp_path):
        """R-144-1 (verifica esterna #122): un tag "origin/main" sul branch non svuota il diff."""
        work = self._repo(tmp_path, "gas_identity.md\n", {"gas_identity.md": "x\n"})
        subprocess.run(["git", "tag", "origin/main", "refs/remotes/origin/feat"], cwd=work,
                       check=True, capture_output=True)
        sez = self._sezione(tmp_path, work)
        assert "gas_identity.md" in sez and "doc-only" not in sez, sez

    def test_nome_con_apice_nel_perimetro(self, tmp_path):
        """V-3 verifica esterna #122 bis: git quota i nomi con apice anche con
        quotePath=false; con -z il nome resta grezzo e il prefisso clients/ combacia."""
        work = self._repo(tmp_path, "clients/\n", {'clients/a"b.py': "x\n"})
        sez = self._sezione(tmp_path, work)
        assert 'clients/a"b.py' in sez and "doc-only" not in sez, sez

    def test_tag_origin_main_non_dirotta_il_perimetro(self, tmp_path):
        """R-147-2: il perimetro "di main" si legge da refs/remotes/origin/main. Un tag
        "origin/main" sul branch (che restringe il perimetro) non lo declassa."""
        work = self._repo(tmp_path, "gas_identity.md\n", {"gas_identity.md": "x\n"},
                          perimetro_branch="gas.py\n")
        subprocess.run(["git", "tag", "origin/main", "refs/remotes/origin/feat"], cwd=work,
                       check=True, capture_output=True)
        sez = self._sezione(tmp_path, work)
        assert "gas_identity.md" in sez and "doc-only" not in sez, sez

    def test_perimetro_assente_ogni_file_e_motore(self, tmp_path):
        work = self._repo(tmp_path, None, {"docs/nota.md": "x\n"})
        sez = self._sezione(tmp_path, work)
        assert "illeggibile" in sez and "docs/nota.md" in sez, sez
        assert "doc-only" not in sez, sez


class TestIPRefCompleto:
    """R-144-1 (verifica esterna #122, V-1): il gate IP scansiona refs/remotes/origin/<branch>."""

    def test_tag_omonimo_del_branch_non_aggira_il_gate_ip(self, tmp_path):
        work, _ = _setup_with_origin(tmp_path)
        subprocess.run(["git", "checkout", "feat"], cwd=work, check=True, capture_output=True)
        (work / "x.py").write_text('HOST = "8.8.8.8"\n')  # gasmerge-ip-ok
        subprocess.run(["git", "add", "x.py"], cwd=work, check=True, capture_output=True)
        subprocess.run(["git", "commit", "-m", "ip"], cwd=work, check=True, capture_output=True)
        subprocess.run(["git", "push", "origin", "feat"], cwd=work, check=True, capture_output=True)
        subprocess.run(["git", "checkout", "main"], cwd=work, check=True, capture_output=True)
        # Tag "origin/feat" sul main pulito: col ref abbreviato vincerebbe su refs/remotes/.
        subprocess.run(["git", "tag", "origin/feat", "main"], cwd=work,
                       check=True, capture_output=True)
        fake_bin = tmp_path / "bin"
        fake_bin.mkdir()
        _make_stub_gh(fake_bin)
        result = _run(work, fake_bin)
        assert result.returncode != 0, result.stdout
        assert "BLOCCO: trovati IP non allowlistati" in result.stdout, result.stdout

    def test_branch_locale_pulito_non_maschera_origin_con_ip(self, tmp_path):
        """V-2 verifica #126: si mergia origin/<branch>, quindi il gate IP legge quel tree
        e non refs/heads/<branch> (qui pulito, mentre origin contiene l'IP)."""
        work, _ = _setup_with_origin(tmp_path)
        subprocess.run(["git", "checkout", "feat"], cwd=work, check=True, capture_output=True)
        (work / "x.py").write_text('HOST = "8.8.8.8"\n')  # gasmerge-ip-ok
        subprocess.run(["git", "add", "x.py"], cwd=work, check=True, capture_output=True)
        subprocess.run(["git", "commit", "-m", "ip"], cwd=work, check=True, capture_output=True)
        subprocess.run(["git", "push", "origin", "feat"], cwd=work, check=True, capture_output=True)
        subprocess.run(["git", "reset", "--hard", "HEAD~1"], cwd=work, check=True,
                       capture_output=True)
        subprocess.run(["git", "checkout", "main"], cwd=work, check=True, capture_output=True)
        fake_bin = tmp_path / "bin"
        fake_bin.mkdir()
        _make_stub_gh(fake_bin)
        result = _run(work, fake_bin)
        assert result.returncode != 0, result.stdout
        assert "BLOCCO: trovati IP non allowlistati" in result.stdout, result.stdout
        assert "--- FILE DI MOTORE ---" not in result.stdout, result.stdout

    def test_push_durante_attesa_ci_visto_dal_gate(self, tmp_path):
        """V-3 verifica #126: un push al branch durante l'attesa CI deve arrivare al gate
        IP (secondo `git fetch --prune` dopo il --watch), non lo stato del primo fetch."""
        work, bare = _setup_with_origin(tmp_path)
        altro = tmp_path / "altro"
        subprocess.run(["git", "clone", "-q", "-b", "feat", str(bare), str(altro)],
                       check=True, capture_output=True)
        (altro / "x.py").write_text('HOST = "8.8.8.8"\n')  # gasmerge-ip-ok
        subprocess.run(["git", "add", "x.py"], cwd=altro, check=True, capture_output=True)
        subprocess.run(["git", "-c", "user.email=t@t.invalid", "-c", "user.name=T",
                        "commit", "-m", "ip"], cwd=altro, check=True, capture_output=True)
        fake_bin = tmp_path / "bin"
        fake_bin.mkdir()
        _make_stub_gh(fake_bin, on_watch=f'git -C "{altro}" push -q origin feat >/dev/null 2>&1')
        result = _run(work, fake_bin)
        assert result.returncode != 0, result.stdout
        assert "BLOCCO: trovati IP non allowlistati" in result.stdout, result.stdout
        assert "--- FILE DI MOTORE ---" not in result.stdout, result.stdout


class TestIPAllowlistSoloContenuto:
    """R-147-1 (verifica esterna #122 bis, V-1): il marker gasmerge-ip-ok vale solo nel
    CONTENUTO della riga, non nel prefisso `<ref>:<path>:` stampato da git grep."""

    def _branch_con_ip(self, tmp_path: Path, branch: str, filename: str) -> Path:
        work, _ = _setup_with_origin(tmp_path, branch=branch)
        subprocess.run(["git", "checkout", branch], cwd=work, check=True, capture_output=True)
        (work / filename).parent.mkdir(parents=True, exist_ok=True)
        (work / filename).write_text('HOST = "8.8.8.8"\n')  # gasmerge-ip-ok
        subprocess.run(["git", "add", "-A"], cwd=work, check=True, capture_output=True)
        subprocess.run(["git", "commit", "-m", "ip"], cwd=work, check=True, capture_output=True)
        subprocess.run(["git", "push", "origin", branch], cwd=work, check=True, capture_output=True)
        subprocess.run(["git", "checkout", "main"], cwd=work, check=True, capture_output=True)
        return work

    def _assert_blocca(self, tmp_path: Path, work: Path, branch: str) -> None:
        fake_bin = tmp_path / "bin"
        fake_bin.mkdir()
        _make_stub_gh(fake_bin, head_ref=branch)
        result = _run(work, fake_bin)
        assert result.returncode != 0, result.stdout
        assert "BLOCCO: trovati IP non allowlistati" in result.stdout, result.stdout

    def test_branch_avvelenato_non_allowlista(self, tmp_path):
        work = self._branch_con_ip(tmp_path, "fix/gasmerge-ip-ok", "x.py")
        self._assert_blocca(tmp_path, work, "fix/gasmerge-ip-ok")

    def test_path_avvelenato_non_allowlista(self, tmp_path):
        work = self._branch_con_ip(tmp_path, "feat", "docs/gasmerge-ip-ok.py")
        self._assert_blocca(tmp_path, work, "feat")

    def test_errore_della_grep_allowlist_blocca(self, tmp_path):
        """R-148-1: se la seconda git grep (quella con --and --not) fallisce, il gate
        NON deve concludere "tutti allowlistati": BLOCCO fail-closed."""
        work = self._branch_con_ip(tmp_path, "feat", "x.py")
        fake_bin = tmp_path / "bin"
        fake_bin.mkdir()
        _make_stub_gh(fake_bin)
        real_git = shutil.which("git") or "/usr/bin/git"
        stub = fake_bin / "git"
        stub.write_text(f"""#!/usr/bin/env bash
if [ "$1" = "grep" ] && printf '%s\\n' "$@" | grep -qx -- '--and'; then exit 2; fi
exec "{real_git}" "$@"
""")
        stub.chmod(0o755)
        result = _run(work, fake_bin)
        assert result.returncode != 0, result.stdout
        assert "BLOCCO: git grep (allowlist)" in result.stdout, result.stdout
        assert "allowlistati (gasmerge-ip-ok) — OK" not in result.stdout, result.stdout


class TestIPTreeUnico:
    """R-148-2 (verifica esterna #123, V-1): le due git grep leggono lo stesso tree; se il
    ref si sposta fra l'una e l'altra (IP a un'altra riga) il gate resta chiuso."""

    def test_ref_spostato_fra_le_due_grep_blocca(self, tmp_path):
        work, _ = _setup_with_origin(tmp_path)
        subprocess.run(["git", "checkout", "feat"], cwd=work, check=True, capture_output=True)
        (work / "x.py").write_text('HOST = "8.8.8.8"\n')  # gasmerge-ip-ok
        subprocess.run(["git", "add", "x.py"], cwd=work, check=True, capture_output=True)
        subprocess.run(["git", "commit", "-m", "ip"], cwd=work, check=True, capture_output=True)
        subprocess.run(["git", "push", "origin", "feat"], cwd=work, check=True, capture_output=True)
        (work / "x.py").write_text('\n\nHOST = "8.8.8.8"\n')  # gasmerge-ip-ok
        subprocess.run(["git", "commit", "-qam", "sposta"], cwd=work, check=True, capture_output=True)
        spostato = subprocess.run(["git", "rev-parse", "HEAD"], cwd=work, check=True,
                                  capture_output=True, text=True).stdout.strip()
        subprocess.run(["git", "checkout", "main"], cwd=work, check=True, capture_output=True)
        fake_bin = tmp_path / "bin"
        fake_bin.mkdir()
        _make_stub_gh(fake_bin)
        real_git = shutil.which("git") or "/usr/bin/git"
        stub = fake_bin / "git"
        stub.write_text(f"""#!/usr/bin/env bash
if [ "$1" = "grep" ] && ! printf '%s\\n' "$@" | grep -qx -- '--and'; then
  "{real_git}" "$@"; rc=$?
  "{real_git}" update-ref refs/remotes/origin/feat {spostato}
  exit $rc
fi
exec "{real_git}" "$@"
""")
        stub.chmod(0o755)
        result = _run(work, fake_bin)
        assert result.returncode != 0, result.stdout
        assert "BLOCCO: trovati IP non allowlistati" in result.stdout, result.stdout


class TestIPTreeNonRisolvibile:
    """R-148-2 / G9 review #149: rev-parse del tree fallisce → BLOCCO subito."""

    def test_tree_non_risolvibile_blocca_subito(self, tmp_path):
        work, _ = _setup_with_origin(tmp_path)
        fake_bin = tmp_path / "bin"
        fake_bin.mkdir()
        _make_stub_gh(fake_bin)
        real_git = shutil.which("git") or "/usr/bin/git"
        stub = fake_bin / "git"
        stub.write_text(f"""#!/usr/bin/env bash
if [ "$1" = "rev-parse" ] && printf '%s\\n' "$@" | grep -q '\\^{{tree}}'; then exit 1; fi
exec "{real_git}" "$@"
""")
        stub.chmod(0o755)
        result = _run(work, fake_bin)
        assert result.returncode != 0, result.stdout
        assert "non risolvibile" in result.stdout, result.stdout
        assert "git grep uscito con codice" not in result.stdout, result.stdout


class TestIPErroreFiltro:
    """V-1(c) verifica #124: il filtro `grep -Fx` della allowlist fallisce → BLOCCO
    subito, senza arrivare al promemoria né alla conferma."""

    def test_errore_filtro_allowlist_blocca(self, tmp_path):
        work, _ = _setup_with_origin(tmp_path)
        subprocess.run(["git", "checkout", "feat"], cwd=work, check=True, capture_output=True)
        (work / "x.py").write_text('HOST = "8.8.8.8"\n')  # gasmerge-ip-ok
        subprocess.run(["git", "add", "x.py"], cwd=work, check=True, capture_output=True)
        subprocess.run(["git", "commit", "-m", "ip"], cwd=work, check=True, capture_output=True)
        subprocess.run(["git", "push", "origin", "feat"], cwd=work, check=True, capture_output=True)
        subprocess.run(["git", "checkout", "main"], cwd=work, check=True, capture_output=True)
        fake_bin = tmp_path / "bin"
        fake_bin.mkdir()
        _make_stub_gh(fake_bin)
        real_grep = shutil.which("grep") or "/usr/bin/grep"
        stub = fake_bin / "grep"
        stub.write_text(
            "#!/usr/bin/env bash\n"
            "for a in \"$@\"; do [ \"$a\" = -Fx ] && exit 2; done\n"
            f"exec \"{real_grep}\" \"$@\"\n")
        stub.chmod(0o755)
        result = _run(work, fake_bin)
        assert result.returncode != 0, result.stdout
        assert "BLOCCO: errore nel filtro allowlist (rc=2)" in result.stdout, result.stdout
        assert "--- FILE DI MOTORE ---" not in result.stdout, result.stdout


class TestIPFileBinariENonUtf8:
    """R-148-3: il gate IP vede anche file binari (-a) e righe non UTF-8 (LC_ALL=C)."""

    def _branch_con_bytes(self, tmp_path: Path, data: bytes) -> Path:
        work, _ = _setup_with_origin(tmp_path)
        subprocess.run(["git", "checkout", "feat"], cwd=work, check=True, capture_output=True)
        (work / "a.bin").write_bytes(data)
        subprocess.run(["git", "add", "-A"], cwd=work, check=True, capture_output=True)
        subprocess.run(["git", "commit", "-m", "bytes"], cwd=work, check=True, capture_output=True)
        subprocess.run(["git", "push", "origin", "feat"], cwd=work, check=True, capture_output=True)
        subprocess.run(["git", "checkout", "main"], cwd=work, check=True, capture_output=True)
        return work

    def _assert_blocca(self, tmp_path: Path, work: Path) -> None:
        fake_bin = tmp_path / "bin"
        fake_bin.mkdir()
        _make_stub_gh(fake_bin)
        result = _run(work, fake_bin)
        assert result.returncode != 0, result.stdout
        assert "BLOCCO: trovati IP non allowlistati" in result.stdout, result.stdout

    def test_file_binario_con_ip(self, tmp_path):
        work = self._branch_con_bytes(tmp_path, b"\x00\x01host 8.8.8.8\n")  # gasmerge-ip-ok
        self._assert_blocca(tmp_path, work)

    def test_riga_latin1_con_ip(self, tmp_path):
        work = self._branch_con_bytes(tmp_path, b"caf\xe9 8.8.8.8\n")  # gasmerge-ip-ok
        self._assert_blocca(tmp_path, work)

    @pytest.mark.parametrize("data", [
        b"caf\xe98.8.8.8\n",            # gasmerge-ip-ok
        b"8.8.8.8\xe9\n",               # gasmerge-ip-ok
    ])
    def test_byte_latin1_attaccato_all_ip_in_locale_utf8(self, tmp_path, monkeypatch, data):
        """V-2 #125 (discriminazione su glibc): in locale UTF-8 un byte non UTF-8 ATTACCATO
        all'IP non è un separatore per git grep/grep e l'IP sparisce (fail-open). Solo
        LC_ALL=C nel gate lo vede: togliendolo questo test fallisce."""
        loc = _locale_utf8()
        if loc is None:
            pytest.skip("nessun locale UTF-8 sul sistema")
        monkeypatch.setenv("LC_ALL", loc)
        work = self._branch_con_bytes(tmp_path, data)
        fake_bin = tmp_path / "bin"
        fake_bin.mkdir()
        _make_stub_gh(fake_bin)
        result = _run(work, fake_bin)
        assert result.returncode != 0, result.stdout
        assert "BLOCCO: trovati IP non allowlistati" in result.stdout, result.stdout
        # La riga bloccata va mostrata (grep -Fx in UTF-8 stamperebbe "binary file matches").
        assert "8.8.8.8" in result.stdout, result.stdout  # gasmerge-ip-ok


# ---------------------------------------------------------------------------
# Fette F1/F2 — marker IP allowlist + TOCTOU
# ---------------------------------------------------------------------------

class TestIPAllowlist:
    """Invariante IP con marker gasmerge-ip-ok: deny-by-default, allowlist esplicita."""

    def _make_repo_with_ip_file(
        self, tmp_path: Path, file_content: str, filename: str = "README.md"
    ) -> tuple[Path, Path]:
        """Crea bare+work con un file contenente una riga IP sul branch feat."""
        bare = tmp_path / "bare"
        bare.mkdir()
        subprocess.run(["git", "init", "--bare", str(bare)], check=True, capture_output=True)
        work = tmp_path / "work"
        _init_repo(work)
        subprocess.run(["git", "remote", "add", "origin", str(bare)],
                       cwd=work, check=True, capture_output=True)
        subprocess.run(["git", "push", "origin", "main"], cwd=work, check=True, capture_output=True)
        subprocess.run(["git", "checkout", "-b", "feat"], cwd=work, check=True, capture_output=True)
        target = work / filename
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(file_content)
        subprocess.run(["git", "add", str(filename)], cwd=work, check=True, capture_output=True)
        subprocess.run(["git", "commit", "-m", "add file with ip"],
                       cwd=work, check=True, capture_output=True)
        subprocess.run(["git", "push", "origin", "feat"],
                       cwd=work, check=True, capture_output=True)
        subprocess.run(["git", "checkout", "main"], cwd=work, check=True, capture_output=True)
        return work, bare

    def test_ip_with_marker_passes(self, tmp_path):
        """IP + marker gasmerge-ip-ok sulla stessa riga del file → invariante PASSA.

        La riga nel repo ha '1.0.0.0 # gasmerge-ip-ok': il filtro la riconosce
        come vouch umano e la esclude. Il gate produce il messaggio allowlistat*.
        """
        work, _ = self._make_repo_with_ip_file(
            tmp_path,
            "server: 1.0.0.0 # gasmerge-ip-ok\n",  # gasmerge-ip-ok
            "reports/example.md",
        )
        fake_bin = tmp_path / "bin"
        fake_bin.mkdir()
        _make_stub_gh(fake_bin)
        # Script arriverà al prompt di conferma: stdin EOF → ANNULLATO, ma il gate IP
        # ha già stampato il messaggio di allowlist prima di quel punto.
        result = _run(work, fake_bin)
        assert "Tutti gli IP sono allowlistati" in result.stdout, (
            f"IP marcato deve produrre messaggio allowlist: stdout={result.stdout!r}"
        )
        assert "BLOCCO: trovati IP" not in result.stdout, (
            f"IP marcato non deve bloccare: stdout={result.stdout!r}"
        )

    def test_ip_without_marker_blocks(self, tmp_path):
        """IP senza marker → BLOCCO anche se l'indirizzo è di documentazione."""
        work, _ = self._make_repo_with_ip_file(
            tmp_path,
            "gateway: 1.0.0.0\n",  # gasmerge-ip-ok
        )
        fake_bin = tmp_path / "bin"
        fake_bin.mkdir()
        _make_stub_gh(fake_bin)
        result = _run(work, fake_bin)
        assert result.returncode != 0, (
            f"Atteso exit non-zero con IP non marcato, got 0; stdout={result.stdout!r}"
        )
        assert "BLOCCO" in result.stdout, f"Atteso BLOCCO: {result.stdout!r}"
        assert "1.0.0.0" in result.stdout, (  # gasmerge-ip-ok
            f"Match IP non marcato deve essere stampato: {result.stdout!r}"
        )

    def test_public_ip_without_marker_blocks(self, tmp_path):
        """IP pubblico RFC5737 senza marker → BLOCCO."""
        work, _ = self._make_repo_with_ip_file(
            tmp_path,
            "remote: 203.0.113.9\n",  # gasmerge-ip-ok
        )
        fake_bin = tmp_path / "bin"
        fake_bin.mkdir()
        _make_stub_gh(fake_bin)
        result = _run(work, fake_bin)
        assert result.returncode != 0, (
            f"Atteso exit non-zero con IP pubblico, got 0; stdout={result.stdout!r}"
        )
        assert "BLOCCO" in result.stdout, f"Atteso BLOCCO: {result.stdout!r}"
        assert "203.0.113.9" in result.stdout, (  # gasmerge-ip-ok
            f"Match IP pubblico deve essere stampato: {result.stdout!r}"
        )


# ---------------------------------------------------------------------------
# Loopback exemption (fetta loopback-ok)
# ---------------------------------------------------------------------------

class TestLoopbackExemption:
    """Invariante IP: 127.x.x.x sempre esente; righe miste e altri indirizzi bloccano."""

    def _make_repo_with_ip_file(
        self, tmp_path: Path, file_content: str, filename: str = "README.md"
    ) -> tuple[Path, Path]:
        bare = tmp_path / "bare"
        bare.mkdir()
        subprocess.run(["git", "init", "--bare", str(bare)], check=True, capture_output=True)
        work = tmp_path / "work"
        _init_repo(work)
        subprocess.run(["git", "remote", "add", "origin", str(bare)],
                       cwd=work, check=True, capture_output=True)
        subprocess.run(["git", "push", "origin", "main"], cwd=work, check=True, capture_output=True)
        subprocess.run(["git", "checkout", "-b", "feat"], cwd=work, check=True, capture_output=True)
        target = work / filename
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(file_content)
        subprocess.run(["git", "add", str(filename)], cwd=work, check=True, capture_output=True)
        subprocess.run(["git", "commit", "-m", "add file with ip"],
                       cwd=work, check=True, capture_output=True)
        subprocess.run(["git", "push", "origin", "feat"],
                       cwd=work, check=True, capture_output=True)
        subprocess.run(["git", "checkout", "main"], cwd=work, check=True, capture_output=True)
        return work, bare

    def test_loopback_127_0_0_1_passes(self, tmp_path):
        """Test 1: solo un loopback (127.x) nel branch → invariante IP NON blocca."""
        work, _ = self._make_repo_with_ip_file(tmp_path, "host: 127.0.0.1\n")  # gasmerge-ip-ok
        fake_bin = tmp_path / "bin"
        fake_bin.mkdir()
        _make_stub_gh(fake_bin)
        result = _run(work, fake_bin)
        assert "BLOCCO: trovati IP" not in result.stdout, (
            f"IP loopback non deve bloccare: stdout={result.stdout!r}"
        )
        assert "loopback" in result.stdout, (
            f"Atteso messaggio loopback: stdout={result.stdout!r}"
        )

    def test_due_loopback_sulla_stessa_riga_passa(self, tmp_path):
        """V-2 verifica #125: due 127.x sulla stessa riga → esente (sed con flag g)."""
        work, _ = self._make_repo_with_ip_file(tmp_path, "a: 127.0.0.1 b: 127.0.0.2\n")
        fake_bin = tmp_path / "bin"
        fake_bin.mkdir()
        _make_stub_gh(fake_bin)
        result = _run(work, fake_bin)
        assert "BLOCCO: trovati IP" not in result.stdout, result.stdout
        assert "Tutti gli IP sono loopback" in result.stdout, result.stdout

    @pytest.mark.parametrize("riga", [
        "host: 8.8.8.8 \n",          # spazio finale    # gasmerge-ip-ok
        "host: 8.8.8.8\t\n",        # tab finale       # gasmerge-ip-ok
        "  host: 8.8.8.8\n",         # spazio iniziale  # gasmerge-ip-ok
        "path a\\b host 8.8.8.8\n",  # backslash        # gasmerge-ip-ok
    ])
    def test_riga_con_spazi_o_backslash_blocca(self, tmp_path, riga):
        """R-153-1: la riga confrontata con -Fx deve restare identica a quella di git grep
        (`IFS= read -r`): spazi ai bordi o backslash non devono far passare l'IP."""
        work, _ = self._make_repo_with_ip_file(tmp_path, riga)
        fake_bin = tmp_path / "bin"
        fake_bin.mkdir()
        _make_stub_gh(fake_bin)
        result = _run(work, fake_bin)
        assert "BLOCCO: trovati IP non allowlistati" in result.stdout, result.stdout
        assert "--- FILE DI MOTORE ---" not in result.stdout, result.stdout

    @pytest.mark.parametrize("riga", [
        "connect to 8.8.8.8.\n",              # punto di fine frase  # gasmerge-ip-ok
        "url 8.8.8.8.nip.io\n",               # <IP>.dominio         # gasmerge-ip-ok
        "host.8.8.8.8\n",                     # dominio.<IP>         # gasmerge-ip-ok
        ".8.8.8.8\n",                         # punto a inizio riga  # gasmerge-ip-ok
        "a 127.0.0.1 b 8.8.8.8.\n",           # loopback + IP.       # gasmerge-ip-ok
        "a 127.0.0.1 b host.8.8.8.8\n",       # loopback + .IP       # gasmerge-ip-ok
        "8.8.8.8.nip.io\n",                   # inizio riga + .dom   # gasmerge-ip-ok
    ])
    def test_ip_adiacente_a_un_punto_blocca(self, tmp_path, riga):
        """R-155-1 (review #155, verifica esterna #127 V-1): un IP con un punto subito prima
        o subito dopo (non seguito/preceduto da cifra) è un IP e va bloccato."""
        work, _ = self._make_repo_with_ip_file(tmp_path, riga)
        fake_bin = tmp_path / "bin"
        fake_bin.mkdir()
        _make_stub_gh(fake_bin)
        result = _run(work, fake_bin)
        assert "BLOCCO: trovati IP non allowlistati" in result.stdout, result.stdout
        assert "--- FILE DI MOTORE ---" not in result.stdout, result.stdout

    @pytest.mark.parametrize("riga,atteso", [
        ("versione 1.2.3.4.5\n", "0 IP trovati — OK"),
        ("bind 127.0.0.1 v1.2.3.4.5\n", "Tutti gli IP sono loopback"),
        ("bind 127.0.0.1.\n", "Tutti gli IP sono loopback"),
    ])
    def test_cinque_componenti_non_e_un_ip(self, tmp_path, riga, atteso):
        """R-155-1: le ancore restano: "1.2.3.4.5" non è un IP (punto adiacente a una cifra)."""
        work, _ = self._make_repo_with_ip_file(tmp_path, riga)
        fake_bin = tmp_path / "bin"
        fake_bin.mkdir()
        _make_stub_gh(fake_bin)
        result = _run(work, fake_bin)
        assert "BLOCCO: trovati IP" not in result.stdout, result.stdout
        assert atteso in result.stdout, result.stdout

    def test_loopback_127_0_0_53_passes(self, tmp_path):
        """Test 2: solo un loopback non-canonico nel branch → NON blocca."""
        work, _ = self._make_repo_with_ip_file(tmp_path, "dns: 127.0.0.53\n")  # gasmerge-ip-ok
        fake_bin = tmp_path / "bin"
        fake_bin.mkdir()
        _make_stub_gh(fake_bin)
        result = _run(work, fake_bin)
        assert "BLOCCO: trovati IP" not in result.stdout, (
            f"IP loopback non-canonico non deve bloccare: stdout={result.stdout!r}"
        )
        assert "loopback" in result.stdout, (
            f"Atteso messaggio loopback: stdout={result.stdout!r}"
        )

    def test_0_0_0_0_still_blocks(self, tmp_path):
        """Test 3: zero-route (non loopback) → BLOCCA ancora."""
        work, _ = self._make_repo_with_ip_file(tmp_path, "bind: 0.0.0.0\n")  # gasmerge-ip-ok
        fake_bin = tmp_path / "bin"
        fake_bin.mkdir()
        _make_stub_gh(fake_bin)
        result = _run(work, fake_bin)
        assert result.returncode != 0, (
            f"IP zero-route deve bloccare: stdout={result.stdout!r}"
        )
        assert "BLOCCO" in result.stdout, f"Atteso BLOCCO: {result.stdout!r}"

    def test_public_ip_still_blocks(self, tmp_path):
        """Test 4: IP pubblico senza marker → BLOCCA ancora."""
        work, _ = self._make_repo_with_ip_file(tmp_path, "remote: 93.42.17.8\n")  # gasmerge-ip-ok
        fake_bin = tmp_path / "bin"
        fake_bin.mkdir()
        _make_stub_gh(fake_bin)
        result = _run(work, fake_bin)
        assert result.returncode != 0, (
            f"IP pubblico deve bloccare: stdout={result.stdout!r}"
        )
        assert "BLOCCO" in result.stdout, f"Atteso BLOCCO: {result.stdout!r}"

    def test_mixed_loopback_and_public_blocks(self, tmp_path):
        """Test 5 (CRITICO): riga con loopback E IP pubblico → BLOCCA ancora.

        Il loopback non deve mascherare l'IP non-loopback sulla stessa riga.
        """
        work, _ = self._make_repo_with_ip_file(
            tmp_path, "fallback: 127.0.0.1 remote: 93.42.17.8\n"  # gasmerge-ip-ok
        )
        fake_bin = tmp_path / "bin"
        fake_bin.mkdir()
        _make_stub_gh(fake_bin)
        result = _run(work, fake_bin)
        assert result.returncode != 0, (
            f"Riga mista (loopback + IP pubblico) deve bloccare: stdout={result.stdout!r}"
        )
        assert "BLOCCO" in result.stdout, f"Atteso BLOCCO: {result.stdout!r}"

    def test_public_ip_with_marker_still_passes(self, tmp_path):
        """Test 6: IP pubblico + marker gasmerge-ip-ok → NON blocca (marker ancora valido)."""
        work, _ = self._make_repo_with_ip_file(
            tmp_path, "remote: 93.42.17.8 # gasmerge-ip-ok\n"
        )
        fake_bin = tmp_path / "bin"
        fake_bin.mkdir()
        _make_stub_gh(fake_bin)
        result = _run(work, fake_bin)
        assert "BLOCCO: trovati IP" not in result.stdout, (
            f"IP marcato non deve bloccare: stdout={result.stdout!r}"
        )
        assert "allowlistati" in result.stdout, (
            f"Atteso messaggio allowlist: stdout={result.stdout!r}"
        )

    def test_no_ip_regression_passes(self, tmp_path):
        """Test 7: regressione — branch senza IP continua a passare il gate IP."""
        work, _ = _setup_with_origin(tmp_path)
        fake_bin = tmp_path / "bin"
        fake_bin.mkdir()
        _make_stub_gh(fake_bin)
        result = _run(work, fake_bin)
        assert "BLOCCO: trovati IP" not in result.stdout, (
            f"Branch senza IP non deve bloccare: stdout={result.stdout!r}"
        )
        assert "0 IP trovati" in result.stdout, (
            f"Atteso '0 IP trovati': stdout={result.stdout!r}"
        )


def _make_stub_gh_recording_merge(fake_bin: Path, merge_log: Path, sha: str) -> None:
    """Stub gh: headRefOid sempre identico (head invariata), pr merge registra argomenti.

    Il merge_log viene scritto SOLO quando gh riceve 'pr merge': se il file non esiste
    dopo l'esecuzione, il merge non è stato chiamato. Se esiste, il test può asserire
    che --match-head-commit <sha> compaia come coppia negli argomenti registrati.
    """
    stub = fake_bin / "gh"
    merge_log_path = str(merge_log)
    stub.write_text(f"""#!/usr/bin/env bash
case "$*" in
  *"headRefName,title,state"*)
    printf '{{"headRefName":"feat","title":"Test PR","state":"OPEN"}}\\n' > "$GASPR_JSON"
    exit 0 ;;
  *"--watch"*)
    exit 0 ;;
  *"name,bucket"*)
    printf '%s\\n' '[{{"name":"unit-suite","bucket":"pass"}}]'
    exit 0 ;;
  *"headRefOid"*)
    echo "{sha}"
    exit 0 ;;
  *"pr merge"*)
    echo "$@" >> "{merge_log_path}"
    exit 0 ;;
  *)
    exit 0 ;;
esac
""")
    stub.chmod(0o755)


class TestTOCTOU:
    """TOCTOU: HEAD_SHA cambia tra cattura pre-read e ri-verifica post-read → BLOCCO."""

    def test_head_changed_during_confirm_blocks(self, tmp_path):
        """Stub gh stateful: 1ª headRefOid → SHA_A, 2ª → SHA_B → BLOCCO 'head cambiata'.

        La 1ª chiamata avviene alla cattura HEAD_SHA (dopo i controlli, prima del read).
        La 2ª avviene alla ri-verifica post-read. Stdin alimenta '123' al prompt.
        """
        work, _ = _setup_with_origin(tmp_path)
        fake_bin = tmp_path / "bin"
        fake_bin.mkdir()
        counter_file = tmp_path / "oid_counter"
        counter_file.write_text("0")
        counter_path = str(counter_file)
        stub = fake_bin / "gh"
        stub.write_text(f"""#!/usr/bin/env bash
case "$*" in
  *"headRefName,title,state"*)
    printf '{{"headRefName":"feat","title":"Test PR","state":"OPEN"}}\\n' > "$GASPR_JSON"
    exit 0 ;;
  *"--watch"*)
    exit 0 ;;
  *"name,bucket"*)
    printf '%s\\n' '[{{"name":"unit-suite","bucket":"pass"}}]'
    exit 0 ;;
  *"headRefOid"*)
    COUNT=$(cat "{counter_path}" 2>/dev/null || echo 0)
    if [ "$COUNT" = "0" ]; then
      echo "aaa1111111111111111111111111111111111"
      echo "1" > "{counter_path}"
    else
      echo "bbb2222222222222222222222222222222222"
    fi
    exit 0 ;;
  *"pr merge"*)
    exit 0 ;;
  *)
    exit 0 ;;
esac
""")
        stub.chmod(0o755)
        # Passa "123" allo stdin così `read -r ANS` ottiene il numero PR e procede
        result = _run_with_stdin(work, fake_bin, stdin_data="123\n")
        assert result.returncode != 0, (
            f"Atteso exit non-zero con head cambiata, got 0; stdout={result.stdout!r}"
        )
        assert "BLOCCO" in result.stdout and "head cambiata" in result.stdout, (
            f"Atteso BLOCCO head cambiata: stdout={result.stdout!r}"
        )

    def test_new_head_empty_blocks_with_explicit_message(self, tmp_path):
        """FIX 1 — NEW_HEAD vuoto → BLOCCO esplicito 'vuoto', NON 'head cambiata'.

        Stub stateful: 1ª headRefOid → SHA valido (cattura pre-prompt), 2ª → stringa
        vuota (ri-lettura post-conferma). Senza il nuovo guard il TOCTOU check
        bloccherebbe comunque ma con il messaggio fuorviante 'head cambiata'; con il
        guard il blocco è esplicito prima del confronto TOCTOU.
        """
        work, _ = _setup_with_origin(tmp_path)
        fake_bin = tmp_path / "bin"
        fake_bin.mkdir()
        counter_file = tmp_path / "oid_counter2"
        counter_file.write_text("0")
        counter_path = str(counter_file)
        stub = fake_bin / "gh"
        stub.write_text(f"""#!/usr/bin/env bash
case "$*" in
  *"headRefName,title,state"*)
    printf '{{"headRefName":"feat","title":"Test PR","state":"OPEN"}}\\n' > "$GASPR_JSON"
    exit 0 ;;
  *"--watch"*)
    exit 0 ;;
  *"name,bucket"*)
    printf '%s\\n' '[{{"name":"unit-suite","bucket":"pass"}}]'
    exit 0 ;;
  *"headRefOid"*)
    COUNT=$(cat "{counter_path}" 2>/dev/null || echo 0)
    if [ "$COUNT" = "0" ]; then
      echo "aaa1111111111111111111111111111111111"
      echo "1" > "{counter_path}"
    else
      echo ""
    fi
    exit 0 ;;
  *"pr merge"*)
    exit 0 ;;
  *)
    exit 0 ;;
esac
""")
        stub.chmod(0o755)
        result = _run_with_stdin(work, fake_bin, stdin_data="123\n")
        assert result.returncode != 0, (
            f"Atteso exit non-zero con NEW_HEAD vuoto, got 0; stdout={result.stdout!r}"
        )
        assert "BLOCCO" in result.stdout and "vuoto" in result.stdout, (
            f"Atteso BLOCCO con 'vuoto': stdout={result.stdout!r}"
        )
        assert "head cambiata" not in result.stdout, (
            f"Messaggio 'head cambiata' fuorviante per NEW_HEAD vuoto: {result.stdout!r}"
        )


# ---------------------------------------------------------------------------
# TOCTOU positivo: head invariata → --match-head-commit passato con SHA corretto
# ---------------------------------------------------------------------------

class TestTOCTOUPositive:
    """TOCTOU positivo: HEAD invariata → gh pr merge invocato CON --match-head-commit <SHA>.

    Il difetto che questo test cattura è --match-head-commit assente o SHA sbagliato.
    Un test che asserisce solo 'exit 0' non vale nulla: passerebbe anche se il flag
    sparisse. Il test legge il merge_log scritto dallo stub e verifica la coppia
    '--match-head-commit <SHA_atteso>' negli argomenti reali.
    """

    _SHA = "abc1234def5678abc1234def5678abc1234de"

    def test_head_unchanged_merge_uses_match_head_commit(self, tmp_path):
        """HEAD invariata → gh pr merge include --match-head-commit <SHA_atteso>.

        Lo stub restituisce sempre lo stesso SHA per headRefOid (head non cambia).
        Gli argomenti di pr merge vengono scritti su merge_log. Il test asserisce
        che '--match-head-commit <SHA>' compaia come coppia nel log.
        """
        work, _ = _setup_with_origin(tmp_path)
        fake_bin = tmp_path / "bin"
        fake_bin.mkdir()
        merge_log = tmp_path / "merge_args.log"
        _make_stub_gh_recording_merge(fake_bin, merge_log, self._SHA)

        result = _run_with_stdin(work, fake_bin, stdin_data="123\n")

        assert result.returncode == 0, (
            f"Atteso exit 0 con head invariata, got {result.returncode}; "
            f"stdout={result.stdout!r}; stderr={result.stderr!r}"
        )
        assert merge_log.exists(), (
            f"Stub non ha scritto merge_log — 'pr merge' non è stato chiamato; "
            f"stdout={result.stdout!r}"
        )
        recorded = merge_log.read_text()
        assert f"--match-head-commit {self._SHA}" in recorded, (
            f"'--match-head-commit {self._SHA}' NON trovato negli argomenti di pr merge. "
            f"Registrato: {recorded!r}"
        )
