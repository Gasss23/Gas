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
) -> None:
    """Stub gh parametrico — risponde ai comandi usati da gasmerge."""
    stub = fake_bin / "gh"
    stub.write_text(f"""#!/usr/bin/env bash
case "$*" in
  *"headRefName,title,state"*)
    printf '{{"headRefName":"feat","title":"Test PR","state":"{state}"}}\\n' > "$GASPR_JSON"
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
if [ "$1" = "diff" ] && printf '%s\\n' "$@" | grep -q -- '--name-only'; then
  exit {rc}
fi
exec "{real_git}" "$@"
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
