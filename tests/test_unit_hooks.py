"""Tests per .claude/hooks/session_end.sh e scrivi_rep.sh."""
import json
import os
import subprocess
from pathlib import Path

import pytest

HOOK = Path(__file__).parent.parent / ".claude" / "hooks" / "session_end.sh"
SCRIVI_REP_HOOK = Path(__file__).parent.parent / ".claude" / "hooks" / "scrivi_rep.sh"


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


class TestSessionEndPush:
    """
    T-hook-d/e: verifica che l'hook pushes sul branch corrente (non su main)
    e che un push fallito produca warning su stderr con exit 0.
    """

    def _init_bare_origin(self, bare_path: Path, work_path: Path, branch: str) -> None:
        """Crea un bare repo, collega come origin e prepara il branch dato."""
        bare_path.mkdir()
        subprocess.run(["git", "init", "--bare", str(bare_path)], check=True, capture_output=True)
        subprocess.run(
            ["git", "remote", "add", "origin", str(bare_path)],
            cwd=work_path, check=True, capture_output=True,
        )
        subprocess.run(
            ["git", "push", "origin", "main"],
            cwd=work_path, check=True, capture_output=True,
        )
        subprocess.run(
            ["git", "checkout", "-b", branch],
            cwd=work_path, check=True, capture_output=True,
        )
        subprocess.run(
            ["git", "push", "origin", branch],
            cwd=work_path, check=True, capture_output=True,
        )

    def test_hook_d_push_to_feature_branch_not_main(self, tmp_path):
        """T-hook-d: HEAD su feature/x → commit pushato su origin/feature/x, NON su origin/main."""
        bare = tmp_path / "bare"
        work = tmp_path / "work"
        _init_repo(work)
        self._init_bare_origin(bare, work, "feature/x")
        _add_allowlist_file(work)

        result = _run_hook(work)

        assert result.returncode == 0, f"exit non-zero: {result.stderr!r}"

        # Il commit su origin/feature/x è l'auto-commit dell'hook
        feature_msg = subprocess.run(
            ["git", "--git-dir", str(bare), "log", "--format=%s", "-1", "feature/x"],
            capture_output=True, text=True, check=True,
        ).stdout.strip()
        assert "auto-commit" in feature_msg, (
            f"Messaggio commit atteso 'auto-commit', trovato: {feature_msg!r}"
        )

        # origin/main ha ancora solo il commit init (non l'auto-commit)
        main_log = subprocess.run(
            ["git", "--git-dir", str(bare), "log", "--oneline", "main"],
            capture_output=True, text=True, check=True,
        ).stdout.strip().splitlines()
        assert len(main_log) == 1, (
            f"origin/main non dovrebbe avere nuovi commit: {main_log}"
        )

    def test_hook_e_push_failure_warns_and_exits_zero(self, tmp_path):
        """T-hook-e: origin inesistente → exit 0 + warning su stderr con branch e exit code."""
        _init_repo(tmp_path)
        subprocess.run(
            ["git", "checkout", "-b", "feature/y"],
            cwd=tmp_path, check=True, capture_output=True,
        )
        subprocess.run(
            ["git", "remote", "add", "origin", "/nonexistent/path/repo.git"],
            cwd=tmp_path, check=True, capture_output=True,
        )
        _add_allowlist_file(tmp_path)

        result = _run_hook(tmp_path)

        assert result.returncode == 0, (
            f"Atteso exit 0 anche con push fallito, got {result.returncode}; stderr={result.stderr!r}"
        )
        assert result.stderr.strip(), "Warning atteso su stderr, ma stderr è vuoto"
        assert "push" in result.stderr.lower() and "fallito" in result.stderr.lower(), (
            f"Warning deve menzionare 'push fallito': {result.stderr!r}"
        )
        assert "feature/y" in result.stderr, (
            f"Warning deve nominare il branch 'feature/y': {result.stderr!r}"
        )
        assert "exit code" in result.stderr.lower(), (
            f"Warning deve riportare il codice di uscita: {result.stderr!r}"
        )


class TestSessionEndAddRobust:
    """
    T-hook-f: git add robusto quando .gas_history.json è assente.
    Verifica che l'hook staggi e committi reports/x.md anche senza .gas_history.json.
    """

    def test_hook_f_add_without_gas_history(self, tmp_path):
        """T-hook-f: no .gas_history.json + reports/x.md modificato → commit avviene comunque."""
        # Setup bare origin per evitare interferenza del push fallito
        bare = tmp_path / "bare"
        bare.mkdir()
        subprocess.run(["git", "init", "--bare", str(bare)], check=True, capture_output=True)

        work = tmp_path / "work"
        _init_repo(work)
        subprocess.run(
            ["git", "remote", "add", "origin", str(bare)],
            cwd=work, check=True, capture_output=True,
        )
        subprocess.run(["git", "push", "origin", "main"], cwd=work, check=True, capture_output=True)
        subprocess.run(
            ["git", "checkout", "-b", "feature/f"],
            cwd=work, check=True, capture_output=True,
        )
        subprocess.run(
            ["git", "push", "origin", "feature/f"],
            cwd=work, check=True, capture_output=True,
        )

        # Crea reports/x.md ma NON .gas_history.json (assenza deliberata — il bug
        # precedente avrebbe causato git add di uscire 128 e non staggiare nulla)
        reports = work / "reports"
        reports.mkdir(exist_ok=True)
        (reports / "x.md").write_text("# test fetta 2\n")

        before = _commit_count(work)
        result = _run_hook(work)

        assert result.returncode == 0, (
            f"Atteso exit 0, got {result.returncode}; stderr={result.stderr!r}"
        )
        assert _commit_count(work) == before + 1, (
            f"Atteso 1 commit in più (prima={before}, dopo={_commit_count(work)}); "
            f"stderr={result.stderr!r}"
        )
        # Verifica che reports/x.md sia nel commit HEAD
        committed = subprocess.run(
            ["git", "show", "--name-only", "--format=", "HEAD"],
            cwd=work, capture_output=True, text=True, check=True,
        ).stdout.strip()
        assert "reports/x.md" in committed, (
            f"reports/x.md dovrebbe essere nel commit HEAD: {committed!r}"
        )


class TestScriviRepPush:
    """
    T-hook-g: scrivi_rep.sh pusha sul branch corrente, non su main.
    """

    def _make_transcript(self, path: Path, response_text: str) -> None:
        """Crea un transcript JSONL minimale con trigger 'scrivi rep'.

        L'hook usa jq -rs che fa lo slurp riga per riga: il formato atteso
        è JSONL (un oggetto JSON per riga), non un array JSON.
        """
        lines = [
            {"type": "assistant", "message": {"content": [{"type": "text", "text": response_text}]}},
            {"type": "user", "message": {"content": "scrivi rep"}},
        ]
        path.write_text("\n".join(json.dumps(line) for line in lines))

    def _run_scrivi_rep(self, repo: Path, transcript: Path) -> subprocess.CompletedProcess:
        stdin_data = json.dumps({"transcript_path": str(transcript)})
        env = {
            **os.environ,
            "CLAUDE_PROJECT_DIR": str(repo),
            "GAS_REPO_DIR": str(repo),
        }
        return subprocess.run(
            ["bash", str(SCRIVI_REP_HOOK)],
            input=stdin_data,
            env=env,
            capture_output=True,
            text=True,
        )

    def test_hook_g_push_to_feature_branch_not_main(self, tmp_path):
        """T-hook-g: scrivi_rep.sh su feature/z → push su origin/feature/z, NON origin/main."""
        bare = tmp_path / "bare"
        bare.mkdir()
        subprocess.run(["git", "init", "--bare", str(bare)], check=True, capture_output=True)

        work = tmp_path / "work"
        _init_repo(work)
        subprocess.run(
            ["git", "remote", "add", "origin", str(bare)],
            cwd=work, check=True, capture_output=True,
        )
        subprocess.run(["git", "push", "origin", "main"], cwd=work, check=True, capture_output=True)
        subprocess.run(
            ["git", "checkout", "-b", "feature/z"],
            cwd=work, check=True, capture_output=True,
        )
        subprocess.run(
            ["git", "push", "origin", "feature/z"],
            cwd=work, check=True, capture_output=True,
        )
        (work / "reports").mkdir(exist_ok=True)

        transcript = tmp_path / "transcript.json"
        self._make_transcript(transcript, "Risposta di test hook-g")

        result = self._run_scrivi_rep(work, transcript)

        assert result.returncode == 0, f"exit non-zero: {result.stderr!r}"

        # origin/feature/z deve avere il commit scrivi-rep
        feature_log = subprocess.run(
            ["git", "--git-dir", str(bare), "log", "--format=%s", "feature/z"],
            capture_output=True, text=True, check=True,
        ).stdout.strip()
        assert "scrivi-rep" in feature_log, (
            f"Commit scrivi-rep non trovato su origin/feature/z: {feature_log!r}"
        )

        # origin/main non deve avere commit aggiuntivi
        main_log = subprocess.run(
            ["git", "--git-dir", str(bare), "log", "--oneline", "main"],
            capture_output=True, text=True, check=True,
        ).stdout.strip().splitlines()
        assert len(main_log) == 1, (
            f"origin/main non dovrebbe avere nuovi commit: {main_log}"
        )

    def test_hook_h_main_no_commit(self, tmp_path):
        """T-hook-h: scrivi_rep.sh su main → 0 commit nuovi, exit 0, warning su stderr."""
        work = tmp_path / "work"
        _init_repo(work)  # HEAD su main per default
        (work / "reports").mkdir(exist_ok=True)

        transcript = tmp_path / "transcript.json"
        self._make_transcript(transcript, "Risposta di test hook-h")

        before = _commit_count(work)
        result = self._run_scrivi_rep(work, transcript)

        assert result.returncode == 0, f"exit non-zero: {result.stderr!r}"
        assert _commit_count(work) == before, (
            f"Attesi {before} commit, trovati {_commit_count(work)}; stderr: {result.stderr!r}"
        )
        assert result.stderr.strip(), "Warning atteso su stderr, ma stderr è vuoto"
        assert "main" in result.stderr, (
            f"Warning non menziona 'main': {result.stderr!r}"
        )


class TestScriviRepJq:
    """
    T-hook-i/j: fail-loud jq in scrivi_rep.sh (riserva #55).
    """

    def _make_transcript(self, path: Path, response_text: str) -> None:
        """Crea un transcript JSONL minimale con trigger 'scrivi rep'."""
        lines = [
            {"type": "assistant", "message": {"content": [{"type": "text", "text": response_text}]}},
            {"type": "user", "message": {"content": "scrivi rep"}},
        ]
        path.write_text("\n".join(json.dumps(line) for line in lines))

    def _run_scrivi_rep(
        self, repo: Path, transcript: Path, extra_env: dict | None = None
    ) -> subprocess.CompletedProcess:
        stdin_data = json.dumps({"transcript_path": str(transcript)})
        env = {
            **os.environ,
            "CLAUDE_PROJECT_DIR": str(repo),
            "GAS_REPO_DIR": str(repo),
        }
        if extra_env:
            env.update(extra_env)
        return subprocess.run(
            ["bash", str(SCRIVI_REP_HOOK)],
            input=stdin_data,
            env=env,
            capture_output=True,
            text=True,
        )

    def test_hook_i_no_jq_warns_and_exits_zero(self, tmp_path):
        """T-hook-i: trigger presente + jq assente → warning su stderr, exit 0, nessun file, nessun commit.

        jq viene "nascosto" con un fake eseguibile che fallisce (exit 1), preposto al PATH reale.
        L'hook usa 'jq --version' come functional check: il fake fa fallire il check.
        """
        work = tmp_path / "work"
        _init_repo(work)
        (work / "reports").mkdir(exist_ok=True)

        transcript = tmp_path / "transcript.json"
        self._make_transcript(transcript, "Risposta di test hook-i")

        # Fake jq: eseguibile che fallisce il functional check (jq --version)
        fake_bin = tmp_path / "fake_bin"
        fake_bin.mkdir()
        fake_jq = fake_bin / "jq"
        fake_jq.write_text("#!/bin/bash\nexit 1\n")
        fake_jq.chmod(0o755)
        broken_jq_path = str(fake_bin) + ":" + os.environ.get("PATH", "")

        before = _commit_count(work)
        result = self._run_scrivi_rep(work, transcript, {"PATH": broken_jq_path})

        assert result.returncode == 0, (
            f"Atteso exit 0 con jq assente, got {result.returncode}; stderr={result.stderr!r}"
        )
        assert result.stderr.strip(), "Warning atteso su stderr con jq assente, ma stderr è vuoto"
        assert "jq" in result.stderr.lower() or "dipendenza" in result.stderr.lower(), (
            f"Warning deve menzionare jq o dipendenza mancante: {result.stderr!r}"
        )
        assert not (work / "reports" / "ultima_risposta.md").exists(), (
            "ultima_risposta.md NON deve essere scritto quando jq è assente"
        )
        assert _commit_count(work) == before, (
            f"Nessun commit atteso con jq assente; prima={before}, dopo={_commit_count(work)}"
        )

    def test_hook_j_detached_head_no_commit(self, tmp_path):
        """T-hook-j: trigger presente, jq disponibile, HEAD detached → warning su stderr, exit 0, nessun commit."""
        work = tmp_path / "work"
        _init_repo(work)
        head_sha = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=work, capture_output=True, text=True, check=True,
        ).stdout.strip()
        subprocess.run(
            ["git", "checkout", "--detach", head_sha],
            cwd=work, check=True, capture_output=True,
        )
        (work / "reports").mkdir(exist_ok=True)

        transcript = tmp_path / "transcript.json"
        self._make_transcript(transcript, "Risposta di test hook-j")

        before = _commit_count(work)
        result = self._run_scrivi_rep(work, transcript)

        assert result.returncode == 0, (
            f"Atteso exit 0 con HEAD detached, got {result.returncode}; stderr={result.stderr!r}"
        )
        assert _commit_count(work) == before, (
            f"Nessun commit atteso con HEAD detached; prima={before}, dopo={_commit_count(work)}"
        )
        assert result.stderr.strip(), "Warning atteso su stderr con HEAD detached, ma stderr è vuoto"
        assert "detach" in result.stderr.lower() or "main-lock" in result.stderr, (
            f"Warning deve menzionare 'detach' o 'main-lock': {result.stderr!r}"
        )
