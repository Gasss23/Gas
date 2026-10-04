"""Tests per .claude/hooks/session_end.sh, scrivi_rep.sh, review_gate.sh e promemoria_end.sh."""
import json
import os
import subprocess
from pathlib import Path

import pytest

HOOK = Path(__file__).parent.parent / ".claude" / "hooks" / "session_end.sh"
SCRIVI_REP_HOOK = Path(__file__).parent.parent / ".claude" / "hooks" / "scrivi_rep.sh"
REVIEW_GATE_HOOK = Path(__file__).parent.parent / ".claude" / "hooks" / "review_gate.sh"
HASH_DIFF_SCRIPT = Path(__file__).parent.parent / "scripts" / "hash_diff_staged.sh"
PROMEMORIA_HOOK = Path(__file__).parent.parent / ".claude" / "hooks" / "promemoria_end.sh"


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

    def test_hook_b_feature_branch_no_commit(self, tmp_path):
        """T-hook-b: HEAD su branch normale + file allowlist non committati → 0 commit nuovi.

        Dal 2026-08-19 l'hook non committa mai: il commit è responsabilità del flusso
        /fine-task. File allowlist presenti ma non committati restano tali.
        """
        _init_repo(tmp_path)
        subprocess.run(
            ["git", "checkout", "-b", "feature/test-hook"],
            cwd=tmp_path, check=True, capture_output=True,
        )
        _add_allowlist_file(tmp_path)
        before = _commit_count(tmp_path)

        result = _run_hook(tmp_path)

        assert result.returncode == 0
        assert _commit_count(tmp_path) == before, (
            f"L'hook non deve creare commit (prima={before}, dopo={_commit_count(tmp_path)}); "
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
        """T-hook-d: commit agente su feature/x non pushato → hook pusha su origin/feature/x, NON su origin/main.

        Simula il caso edge: /fine-task ha committato ma la sessione è terminata prima del push.
        L'hook deve recuperare il push senza creare un nuovo commit.
        """
        bare = tmp_path / "bare"
        work = tmp_path / "work"
        _init_repo(work)
        self._init_bare_origin(bare, work, "feature/x")

        # Simula il commit del flusso /fine-task (già committato, non ancora pushato).
        agent_file = work / "reports"
        agent_file.mkdir(exist_ok=True)
        (agent_file / "ultimo_report.md").write_text("# report\n")
        subprocess.run(["git", "add", "reports/ultimo_report.md"], cwd=work, check=True, capture_output=True)
        subprocess.run(
            ["git", "commit", "-m", "docs(fine-task): report sessione"],
            cwd=work, check=True, capture_output=True,
        )
        before_push_sha = subprocess.run(
            ["git", "rev-parse", "HEAD"], cwd=work, capture_output=True, text=True, check=True,
        ).stdout.strip()

        result = _run_hook(work)

        assert result.returncode == 0, f"exit non-zero: {result.stderr!r}"

        # origin/feature/x ha ricevuto il push del commit dell'agente
        pushed_sha = subprocess.run(
            ["git", "--git-dir", str(bare), "rev-parse", "feature/x"],
            capture_output=True, text=True, check=True,
        ).stdout.strip()
        assert pushed_sha == before_push_sha, (
            f"origin/feature/x deve avere lo SHA del commit agente: "
            f"atteso {before_push_sha!r}, trovato {pushed_sha!r}"
        )

        # origin/main ha ancora solo il commit init
        main_log = subprocess.run(
            ["git", "--git-dir", str(bare), "log", "--oneline", "main"],
            capture_output=True, text=True, check=True,
        ).stdout.strip().splitlines()
        assert len(main_log) == 1, (
            f"origin/main non dovrebbe avere nuovi commit: {main_log}"
        )

    def test_hook_e_push_failure_warns_and_exits_zero(self, tmp_path):
        """T-hook-e: origin inesistente → push tentato (nessuna ref remota nota), warning + exit 0."""
        _init_repo(tmp_path)
        subprocess.run(
            ["git", "checkout", "-b", "feature/y"],
            cwd=tmp_path, check=True, capture_output=True,
        )
        subprocess.run(
            ["git", "remote", "add", "origin", "/nonexistent/path/repo.git"],
            cwd=tmp_path, check=True, capture_output=True,
        )
        # Nessuna ref remota per feature/y → _remote_sha vuoto → push tentato → fallisce.

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


class TestSessionEndPushFallback:
    """
    T-hook-f: push fail-safe: HEAD == origin → nessun push (noop).
    Verifica che l'hook salti il push quando il branch è già sincronizzato con origin.
    """

    def test_hook_f_no_push_when_synced(self, tmp_path):
        """T-hook-f: HEAD == origin/feature/f → push skippato, 0 commit nuovi, exit 0."""
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
        # Push iniziale: HEAD == origin/feature/f dopo questo punto.
        subprocess.run(
            ["git", "push", "origin", "feature/f"],
            cwd=work, check=True, capture_output=True,
        )
        # Aggiorna la ref remota locale con fetch per far sì che il confronto SHA funzioni.
        subprocess.run(["git", "fetch", "origin"], cwd=work, check=True, capture_output=True)

        before_sha = subprocess.run(
            ["git", "rev-parse", "HEAD"], cwd=work, capture_output=True, text=True, check=True,
        ).stdout.strip()
        before = _commit_count(work)

        result = _run_hook(work)

        assert result.returncode == 0, f"exit non-zero: {result.stderr!r}"
        assert _commit_count(work) == before, (
            f"L'hook non deve creare commit (prima={before}, dopo={_commit_count(work)})"
        )
        after_sha = subprocess.run(
            ["git", "--git-dir", str(bare), "rev-parse", "feature/f"],
            capture_output=True, text=True, check=True,
        ).stdout.strip()
        assert after_sha == before_sha, (
            f"origin/feature/f non deve avanzare (già sincronizzato): "
            f"prima={before_sha!r}, dopo={after_sha!r}"
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


# ─────────────────────────────── review_gate.sh ──────────────────────────────
# T-gate-A/B/C/D: check_verdetto fail-closed.
# Tutti i test usano repo git temporanei reali — nessun mock.

class TestReviewGateFailClosed:
    """
    Verifica che review_gate.sh sia fail-closed:
    l'esenzione "nessun diff motore" è consentita SOLO se git diff ha avuto
    successo e il suo output non contiene file motore (gas.py/brains/modules/tests/).
    Un errore di git o di cd deve bloccare il commit, non lasciarlo passare.
    """

    def _stdin_commit(self) -> str:
        """JSON stdin che simula un tool use 'git commit' (forma array)."""
        return json.dumps([{"tool_input": {"command": "git commit -m 'test'"}}])

    def _run(self, repo: Path, *, has_review_ok: bool = False,
             stdin: "str | None" = None) -> subprocess.CompletedProcess:
        env = {**os.environ, "CLAUDE_PROJECT_DIR": str(repo)}
        if has_review_ok:
            # Marcatore legato al diff: SHA-256 del diff staged (scripts/hash_diff_staged.sh).
            (repo / ".claude").mkdir(exist_ok=True)
            h = subprocess.run(["bash", str(HASH_DIFF_SCRIPT)], cwd=repo,
                               capture_output=True, text=True, check=True).stdout.strip()
            (repo / ".claude" / ".review_ok").write_text(h + "\n")
        return subprocess.run(
            ["bash", str(REVIEW_GATE_HOOK)],
            input=self._stdin_commit() if stdin is None else stdin,
            env=env,
            capture_output=True,
            text=True,
        )

    def _stage(self, repo: Path, rel_path: str, content: str = "# test\n") -> None:
        fpath = repo / rel_path
        fpath.parent.mkdir(parents=True, exist_ok=True)
        fpath.write_text(content)
        subprocess.run(["git", "add", str(fpath)], cwd=repo, check=True, capture_output=True)

    def test_gate_a_motor_no_review_blocks(self, tmp_path):
        """T-gate-A: diff motore staged + .review_ok assente → BLOCCA (exit 2)."""
        _init_repo(tmp_path)
        self._stage(tmp_path, "gas.py")
        result = self._run(tmp_path)
        assert result.returncode == 2, (
            f"Atteso exit 2 (blocco), got {result.returncode}; stderr={result.stderr!r}"
        )

    def test_gate_b_motor_with_review_ok_passes(self, tmp_path):
        """T-gate-B: diff motore staged + .review_ok presente → PASSA (exit 0)."""
        _init_repo(tmp_path)
        self._stage(tmp_path, "gas.py")
        result = self._run(tmp_path, has_review_ok=True)
        assert result.returncode == 0, (
            f"Atteso exit 0 (pass), got {result.returncode}; stderr={result.stderr!r}"
        )

    def test_gate_c_doc_only_passes(self, tmp_path):
        """T-gate-C: solo file non-motore staged → esente, PASSA (exit 0)."""
        _init_repo(tmp_path)
        self._stage(tmp_path, "reports/foo.md")
        result = self._run(tmp_path)
        assert result.returncode == 0, (
            f"Atteso exit 0 (esente), got {result.returncode}; stderr={result.stderr!r}"
        )

    def test_gate_b2_stale_marker_blocks(self, tmp_path):
        """T-gate-B2: marcatore residuo (hash di un ALTRO diff) → BLOCCA: un .review_ok
        dimenticato da una sessione precedente non apre il gate."""
        _init_repo(tmp_path)
        self._stage(tmp_path, "gas.py", "# revisionato\n")
        self._run(tmp_path, has_review_ok=True)          # marcatore per QUESTO diff
        self._stage(tmp_path, "gas.py", "# cambiato dopo la review\n")
        result = self._run(tmp_path)                     # marcatore ora residuo
        assert result.returncode == 2 and "non corrisponde" in result.stderr, result.stderr

    def test_gate_b3_empty_marker_blocks(self, tmp_path):
        """T-gate-B3: marcatore vuoto (vecchio `touch .review_ok`) → BLOCCA."""
        _init_repo(tmp_path)
        self._stage(tmp_path, "gas.py")
        (tmp_path / ".claude").mkdir(exist_ok=True)
        (tmp_path / ".claude" / ".review_ok").touch()
        result = self._run(tmp_path)
        assert result.returncode == 2, result.stderr

    def test_gate_b4_unstaged_motor_blocks(self, tmp_path):
        """T-gate-B4 (R-136-1): marcatore valido per l'index, ma una modifica al motore
        NON in stage (entrerebbe con commit -a / pathspec) → BLOCCA."""
        _init_repo(tmp_path)
        self._stage(tmp_path, "gas.py", "# revisionato\n")
        subprocess.run(["git", "commit", "-qm", "base"], cwd=tmp_path, check=True, capture_output=True)
        self._stage(tmp_path, "gas.py", "# revisionato v2\n")
        (tmp_path / "gas.py").write_text("# NON revisionato, solo nel working tree\n")
        result = self._run(tmp_path, has_review_ok=True)
        assert result.returncode == 2 and "NON in stage" in result.stderr, result.stderr

    def test_gate_b5_untracked_motor_blocks(self, tmp_path):
        """T-gate-B5 (R-136-1): file motore non tracciato (entrerebbe con add && commit) → BLOCCA."""
        _init_repo(tmp_path)
        self._stage(tmp_path, "gas.py")
        (tmp_path / "modules").mkdir(exist_ok=True)
        (tmp_path / "modules" / "nuovo.py").write_text("# non tracciato\n")
        result = self._run(tmp_path, has_review_ok=True)
        assert result.returncode == 2 and "NON in stage" in result.stderr, result.stderr

    def test_gate_b6_commit_all_with_nothing_staged_blocks(self, tmp_path):
        """T-gate-B6 (R-136-1): nulla in stage, motore modificato nel working tree → BLOCCA
        (un `commit -a` lo porterebbe dentro senza review)."""
        _init_repo(tmp_path)
        self._stage(tmp_path, "gas.py", "# v1\n")
        subprocess.run(["git", "commit", "-qm", "base"], cwd=tmp_path, check=True, capture_output=True)
        (tmp_path / "gas.py").write_text("# v2 non revisionata\n")
        result = self._run(tmp_path)
        assert result.returncode == 2, result.stderr

    def test_gate_v1_gate_file_staged_blocks(self, tmp_path):
        """T-gate-V1a: SOLO un file della macchina di controllo in stage (hook), senza
        marcatore → BLOCCA: il gate protegge se stesso (V-1 verifica esterna PR #118)."""
        _init_repo(tmp_path)
        self._stage(tmp_path, ".claude/hooks/review_gate.sh", "exit 0\n")
        result = self._run(tmp_path)
        assert result.returncode == 2 and "perimetro" in result.stderr, result.stderr

    def test_gate_v1_revisore_md_staged_blocks(self, tmp_path):
        """T-gate-V1b: le regole del revisore sono nel perimetro → BLOCCA senza marcatore."""
        _init_repo(tmp_path)
        self._stage(tmp_path, ".claude/agents/revisore.md", "regole indebolite\n")
        result = self._run(tmp_path)
        assert result.returncode == 2, result.stderr

    def test_gate_v1_unstaged_hash_script_blocks(self, tmp_path):
        """T-gate-V1c: la sonda della verifica esterna. gas.py in stage con marcatore e
        scripts/hash_diff_staged.sh modificato FUORI dallo stage → BLOCCA."""
        _init_repo(tmp_path)
        (tmp_path / "scripts").mkdir(exist_ok=True)
        self._stage(tmp_path, "scripts/hash_diff_staged.sh", "originale\n")
        subprocess.run(["git", "commit", "-qm", "base"], cwd=tmp_path, check=True, capture_output=True)
        self._stage(tmp_path, "gas.py")
        (tmp_path / "scripts" / "hash_diff_staged.sh").write_text('printf "COSTANTE"\n')
        result = self._run(tmp_path, has_review_ok=True)
        assert result.returncode == 2 and "NON in stage" in result.stderr, result.stderr

    def test_gate_v1_doc_outside_perimeter_passes(self, tmp_path):
        """T-gate-V1d: file fuori dal perimetro (scripts/altro.sh, reports/) → esente."""
        _init_repo(tmp_path)
        self._stage(tmp_path, "scripts/altro.sh", "echo\n")
        self._stage(tmp_path, ".claude/settings.local.json", "{}\n")
        result = self._run(tmp_path)
        assert result.returncode == 0, result.stderr

    def _repo_con_hook_proprio(self, tmp_path: Path) -> Path:
        """Repo temporaneo con COPIA di hook, script dell'hash e perimetro committati:
        così l'hook legge il perimetro di QUESTO repo (necessario per R-138-1)."""
        _init_repo(tmp_path)
        for rel in (".claude/hooks/review_gate.sh", "scripts/hash_diff_staged.sh",
                    ".claude/perimetro_review.txt"):
            dst = tmp_path / rel
            dst.parent.mkdir(parents=True, exist_ok=True)
            dst.write_text((REVIEW_GATE_HOOK.parent.parent.parent / rel).read_text())
        (tmp_path / "gas.py").write_text("# v1\n")
        subprocess.run(["git", "add", "-A"], cwd=tmp_path, check=True, capture_output=True)
        subprocess.run(["git", "commit", "-qm", "base"], cwd=tmp_path, check=True, capture_output=True)
        return tmp_path

    def _run_hook_locale(self, repo: Path) -> subprocess.CompletedProcess:
        env = {**os.environ, "CLAUDE_PROJECT_DIR": str(repo)}
        return subprocess.run(["bash", str(repo / ".claude/hooks/review_gate.sh")],
                              input=self._stdin_commit(), env=env, capture_output=True, text=True)

    def test_gate_r138_1_staged_perimeter_self_removal_blocks(self, tmp_path):
        """R-138-1 (sonda P7): perimetro in stage che toglie sé stesso e gas.py, più gas.py
        modificato in stage, senza marcatore → BLOCCA (le voci di HEAD contano)."""
        repo = self._repo_con_hook_proprio(tmp_path)
        (repo / ".claude/perimetro_review.txt").write_text("brains/\n")
        (repo / "gas.py").write_text("# v2 non revisionata\n")
        subprocess.run(["git", "add", "-A"], cwd=repo, check=True, capture_output=True)
        result = self._run_hook_locale(repo)
        assert result.returncode == 2, result.stderr

    def test_gate_r138_1_unstaged_perimeter_tamper_blocks(self, tmp_path):
        """R-138-1 (sonda P8): perimetro ridotto FUORI stage, gas.py in stage senza
        marcatore → BLOCCA."""
        repo = self._repo_con_hook_proprio(tmp_path)
        (repo / "gas.py").write_text("# v2 non revisionata\n")
        subprocess.run(["git", "add", "gas.py"], cwd=repo, check=True, capture_output=True)
        (repo / ".claude/perimetro_review.txt").write_text("brains/\n")
        result = self._run_hook_locale(repo)
        assert result.returncode == 2, result.stderr

    def test_gate_r138_2_rename_out_of_perimeter_blocks(self, tmp_path):
        """R-138-2 (sonda P1): git mv gas.py → docs/gas.py senza marcatore → BLOCCA."""
        repo = self._repo_con_hook_proprio(tmp_path)
        (repo / "docs").mkdir()
        subprocess.run(["git", "mv", "gas.py", "docs/gas.py"], cwd=repo, check=True, capture_output=True)
        result = self._run_hook_locale(repo)
        assert result.returncode == 2, result.stderr

    def test_gate_r138_2_non_ascii_name_blocks(self, tmp_path):
        """R-138-2 (sonda P2): modules/città.py in stage senza marcatore → BLOCCA."""
        repo = self._repo_con_hook_proprio(tmp_path)
        (repo / "modules").mkdir()
        (repo / "modules" / "città.py").write_text("x\n")
        subprocess.run(["git", "add", "-A"], cwd=repo, check=True, capture_output=True)
        result = self._run_hook_locale(repo)
        assert result.returncode == 2, result.stderr

    def test_gate_r139_git_diff_failure_in_pipeline_blocks(self, tmp_path):
        """R-139 (blocco della review #139): `git diff --cached` fallisce ma `git status`
        riesce (git finto nel PATH) → il gate deve BLOCCARE: l'exit code di git non
        deve perdersi nella pipeline con `tr`."""
        _init_repo(tmp_path)
        self._stage(tmp_path, "gas.py")
        fake = tmp_path / "fakebin"
        fake.mkdir()
        real_git = subprocess.run(["bash", "-c", "command -v git"], capture_output=True,
                                  text=True, check=True).stdout.strip()
        (fake / "git").write_text(
            "#!/usr/bin/env bash\n"
            'for a in "$@"; do [ "$a" = "diff" ] && exit 128; done\n'
            f'exec "{real_git}" "$@"\n')
        (fake / "git").chmod(0o755)
        env = {**os.environ, "CLAUDE_PROJECT_DIR": str(tmp_path),
               "PATH": f"{fake}:{os.environ['PATH']}"}
        result = subprocess.run(["bash", str(REVIEW_GATE_HOOK)], input=self._stdin_commit(),
                                env=env, capture_output=True, text=True)
        assert result.returncode == 2 and "git diff --cached" in result.stderr, result.stderr

    def test_gate_d_git_failure_blocks(self, tmp_path):
        """T-gate-D: CLAUDE_PROJECT_DIR non è un git repo → git diff fallisce → FAIL-CLOSED (exit 2)."""
        # tmp_path esiste ma non ha .git: cd riesce, git diff fallisce → deve bloccare
        result = self._run(tmp_path)
        assert result.returncode == 2, (
            f"Atteso exit 2 (fail-closed), got {result.returncode}; stderr={result.stderr!r}"
        )
        assert result.stderr.strip(), "Messaggio di errore atteso su stderr"


# T-gate-E..I: input OGGETTO (la forma che Claude Code passa davvero all'hook).
# Bug misurato 2026-10-03: con jq presente, `(.[0] // .)` su un oggetto va in
# errore → comando vuoto → exit 0 → gate inerte. I test A-D usavano solo la forma
# array, quindi la CI non lo vedeva.

_STDIN_OBJ_COMMIT = json.dumps({"tool_name": "Bash",
                                "tool_input": {"command": "git commit -m 'test'"}})


class TestReviewGateInputOggetto:
    # Solo gli helper (non l'ereditarieta': A-D girerebbero due volte).
    _stdin_commit = TestReviewGateFailClosed._stdin_commit
    _run = TestReviewGateFailClosed._run
    _stage = TestReviewGateFailClosed._stage

    def test_gate_e_oggetto_motor_no_review_blocks(self, tmp_path):
        """T-gate-E: input oggetto + diff motore + .review_ok assente → BLOCCA."""
        _init_repo(tmp_path)
        self._stage(tmp_path, "gas.py")
        result = self._run(tmp_path, stdin=_STDIN_OBJ_COMMIT)
        assert result.returncode == 2, (
            f"Atteso exit 2 (blocco), got {result.returncode}; stderr={result.stderr!r}"
        )
        assert "BLOCCATO" in result.stderr

    def test_gate_f_oggetto_motor_with_review_ok_passes(self, tmp_path):
        """T-gate-F: input oggetto + diff motore + .review_ok → PASSA."""
        _init_repo(tmp_path)
        self._stage(tmp_path, "modules/x.py")
        result = self._run(tmp_path, has_review_ok=True, stdin=_STDIN_OBJ_COMMIT)
        assert result.returncode == 0, result.stderr

    def test_gate_g_oggetto_doc_only_passes(self, tmp_path):
        """T-gate-G: input oggetto + solo doc staged → esente, PASSA."""
        _init_repo(tmp_path)
        self._stage(tmp_path, "reports/foo.md")
        result = self._run(tmp_path, stdin=_STDIN_OBJ_COMMIT)
        assert result.returncode == 0, result.stderr

    def test_gate_h_oggetto_non_commit_passes(self, tmp_path):
        """T-gate-H: input oggetto, comando NON commit, diff motore staged → non interferisce."""
        _init_repo(tmp_path)
        self._stage(tmp_path, "gas.py")
        stdin = json.dumps({"tool_input": {"command": "git status"}})
        result = self._run(tmp_path, stdin=stdin)
        assert result.returncode == 0, result.stderr

    def test_gate_i_json_illeggibile_con_commit_blocks(self, tmp_path):
        """T-gate-I: JSON illeggibile che contiene un git commit + diff motore → FAIL-CLOSED."""
        _init_repo(tmp_path)
        self._stage(tmp_path, "tests/t.py")
        result = self._run(tmp_path, stdin='{"tool_input": {"command": "git commit -m x"')
        assert result.returncode == 2, (
            f"Atteso exit 2 (fail-closed), got {result.returncode}; stderr={result.stderr!r}"
        )


# R2 — durabilità memoria revisore su interruzione
# ────────────────────────────────────────────────────────────────────────────

COMMIT_MEM_SCRIPT = Path(__file__).parent.parent / "scripts" / "commit_memoria_revisore.sh"
MEM_REL = ".claude/agents/memoria_revisore.md"


def _init_repo_with_mem(path: Path) -> None:
    """Init repo con commit iniziale che include già memoria_revisore.md."""
    _init_repo(path)
    mem = path / MEM_REL
    mem.parent.mkdir(parents=True, exist_ok=True)
    mem.write_text("#1 — 2026-01-01 — APPROVATO — lezione iniziale\n")
    subprocess.run(["git", "add", str(mem)], cwd=path, check=True, capture_output=True)
    subprocess.run(["git", "commit", "-m", "init mem"], cwd=path, check=True, capture_output=True)


def _run_commit_mem(repo: Path, extra_env: dict | None = None) -> subprocess.CompletedProcess:
    env = {**os.environ, "CLAUDE_PROJECT_DIR": str(repo)}
    if extra_env:
        env.update(extra_env)
    return subprocess.run(
        ["bash", str(COMMIT_MEM_SCRIPT)],
        env=env,
        capture_output=True,
        text=True,
    )


class TestCommitMemoriaRevisore:
    """R2 — commit atomico memoria_revisore.md (scripts/commit_memoria_revisore.sh)."""

    def test_r2_only_memoria_committed_and_staging_intact(self, tmp_path):
        """T-R2-a: commit -o committa SOLO memoria_revisore.md; il file motore resta staged.

        Riproduce il bug §6 della sonda R2:
          (a) HEAD contiene SOLO .claude/agents/memoria_revisore.md
          (b) gas.py fittizio (motore) è ancora in staging dopo il commit
          (c) lo script non crasha (exit 0)
        """
        _init_repo_with_mem(tmp_path)

        # Metti in staging un file "motore" fittizio (NON la memoria)
        engine = tmp_path / "gas.py"
        engine.write_text("# motore fittizio staged\n")
        subprocess.run(["git", "add", str(engine)], cwd=tmp_path, check=True, capture_output=True)

        # Scrivi/modifica memoria_revisore.md (non staged, solo working tree)
        mem = tmp_path / MEM_REL
        mem.write_text(
            "#1 — 2026-01-01 — APPROVATO — lezione iniziale\n"
            "#2 — 2026-08-19 — APPROVATO — nessuna lezione nuova\n"
        )

        # Lancia lo script
        result = _run_commit_mem(tmp_path)

        # (c) exit 0 — non crasha
        assert result.returncode == 0, (
            f"T-R2-a(c): atteso exit 0, got {result.returncode}; "
            f"stdout={result.stdout!r} stderr={result.stderr!r}"
        )

        # (a) HEAD contiene SOLO memoria_revisore.md
        head_files = subprocess.run(
            ["git", "diff-tree", "--no-commit-id", "-r", "--name-only", "HEAD"],
            cwd=tmp_path, capture_output=True, text=True, check=True,
        ).stdout.strip().splitlines()
        assert head_files == [MEM_REL], (
            f"T-R2-a(a): HEAD deve contenere SOLO {MEM_REL!r}, trovato: {head_files}"
        )

        # (b) gas.py è ancora in staging
        staged = subprocess.run(
            ["git", "diff", "--cached", "--name-only"],
            cwd=tmp_path, capture_output=True, text=True, check=True,
        ).stdout.strip().splitlines()
        assert "gas.py" in staged, (
            f"T-R2-a(b): gas.py deve restare staged dopo commit -o, staged={staged}"
        )

    def test_r2_add_and_commit_breaks_staging(self, tmp_path):
        """T-R2-b: dimostra che `git add && git commit` NON è sicuro — viola l'asserzione (a).

        Questa è la prova che il bug §6 esiste con l'approccio naive.
        Con `add && commit`, il file motore staged entra nel commit insieme alla memoria
        → HEAD contiene ENTRAMBI i file, violando (a).
        """
        _init_repo_with_mem(tmp_path)

        engine = tmp_path / "gas.py"
        engine.write_text("# motore fittizio staged\n")
        subprocess.run(["git", "add", str(engine)], cwd=tmp_path, check=True, capture_output=True)

        mem = tmp_path / MEM_REL
        mem.write_text(
            "#1 — 2026-01-01 — APPROVATO — lezione iniziale\n"
            "#2 — 2026-08-19 — APPROVATO — nessuna lezione nuova\n"
        )
        subprocess.run(["git", "add", str(mem)], cwd=tmp_path, check=True, capture_output=True)

        subprocess.run(
            ["git", "commit", "-m", "naive add && commit"],
            cwd=tmp_path,
            env={**os.environ, "GIT_AUTHOR_NAME": "T", "GIT_AUTHOR_EMAIL": "t@t",
                 "GIT_COMMITTER_NAME": "T", "GIT_COMMITTER_EMAIL": "t@t"},
            check=True, capture_output=True,
        )

        head_files = subprocess.run(
            ["git", "diff-tree", "--no-commit-id", "-r", "--name-only", "HEAD"],
            cwd=tmp_path, capture_output=True, text=True, check=True,
        ).stdout.strip().splitlines()

        # Con add && commit, gas.py entra nel commit — violazione dell'asserzione (a)
        assert "gas.py" in head_files, (
            "T-R2-b: con add && commit gas.py dovrebbe essere nel commit (dimostra il bug)"
        )
        assert len(head_files) > 1, (
            "T-R2-b: con add && commit HEAD deve contenere più di un file (memoria + motore)"
        )

    def test_r2_noop_idempotent(self, tmp_path):
        """T-R2-c: se memoria_revisore.md non è cambiata, exit 0 (niente da committare).

        Verifica l'idempotenza: dopo /fine-task, una seconda chiamata allo script è innocua.
        """
        _init_repo_with_mem(tmp_path)
        # Non modifichiamo il file — identico a HEAD
        result = _run_commit_mem(tmp_path)
        assert result.returncode == 0, (
            f"T-R2-c: atteso exit 0 su noop, got {result.returncode}; stderr={result.stderr!r}"
        )

    def test_r2_fail_safe_not_a_git_repo(self, tmp_path):
        """T-R2-d: CLAUDE_PROJECT_DIR punta a una dir non-git → exit 0 (fail-safe §9).

        Non crasha; scrive un warning in gas_debug.log dentro CLAUDE_PROJECT_DIR.
        """
        not_a_repo = tmp_path / "not_a_repo"
        not_a_repo.mkdir()
        log_file = not_a_repo / "gas_debug.log"

        result = subprocess.run(
            ["bash", str(COMMIT_MEM_SCRIPT)],
            env={**os.environ, "CLAUDE_PROJECT_DIR": str(not_a_repo)},
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0, (
            f"T-R2-d: atteso exit 0 (fail-safe), got {result.returncode}; stderr={result.stderr!r}"
        )
        assert log_file.exists(), (
            "T-R2-d: gas_debug.log deve essere creato con il warning di fail-safe"
        )
        assert "WARN" in log_file.read_text(), (
            f"T-R2-d: gas_debug.log deve contenere un warning, trovato: {log_file.read_text()!r}"
        )

    def test_r2_review_number_from_highest_not_last_line(self, tmp_path):
        """T-R2-f: quando le ultime righe sono note di lezione, il numero review
        deve venire dalla riga numerata più alta, non dall'ultima riga.

        Riproduce il bug del commit 83354d8 (#12 invece di #116):
        la riga finale contiene '(lezione #12)' → l'old script estraeva #12.
        Il fix usa grep '^#[0-9]+' per trovare solo le righe numerata.
        """
        _init_repo_with_mem(tmp_path)

        mem = tmp_path / MEM_REL
        mem.write_text(
            "#12 — 2026-06-01 — APPROVATO — lezione iniziale\n"
            "#116 — 2026-09-30 — APPROVATO CON RISERVE — Gate C1 scaffolding.\n"
            "- 2026-09-30 — Il vettore --flag=value (lezione #12) rimane aperto.\n"
        )

        result = _run_commit_mem(tmp_path)
        assert result.returncode == 0, (
            f"T-R2-f: exit 0 atteso, got {result.returncode}; stderr={result.stderr!r}"
        )

        # Il subject del commit deve contenere #116, non #12
        log = subprocess.run(
            ["git", "log", "-1", "--format=%s"],
            cwd=tmp_path, capture_output=True, text=True, check=True,
        ).stdout.strip()
        assert "#116" in log, (
            f"T-R2-f: subject deve contenere '#116', trovato: {log!r}"
        )
        assert "#12 " not in log and log.endswith("#116 — APPROVATO CON RISERVE") or "#116" in log, (
            f"T-R2-f: subject non deve estrarre #12 dalla nota di lezione, trovato: {log!r}"
        )
        # Verdetto
        assert "APPROVATO CON RISERVE" in log, (
            f"T-R2-f: verdetto atteso 'APPROVATO CON RISERVE', trovato: {log!r}"
        )

    def test_r2_fail_safe_mem_present_not_git(self, tmp_path):
        """T-R2-e: mem PRESENTE + dir NON-git → git commit fallisce (riga ~75) → WARN + exit 0.

        Esercita il path fail-safe alla riga ~75 dello script: MEM_FILE trovato,
        ma git commit -o fallisce perché la directory non è un repo git.
        A differenza di T-R2-d (file assente → exit precoce riga 64-66), qui il file
        esiste e l'errore emerge solo al git commit, coprendo il ramo finora scoperto.
        """
        not_a_repo = tmp_path / "not_a_repo"
        not_a_repo.mkdir()
        log_file = not_a_repo / "gas_debug.log"

        mem = not_a_repo / MEM_REL
        mem.parent.mkdir(parents=True, exist_ok=True)
        mem.write_text("#1 — 2026-01-01 — APPROVATO — lezione iniziale\n")

        result = subprocess.run(
            ["bash", str(COMMIT_MEM_SCRIPT)],
            env={**os.environ, "CLAUDE_PROJECT_DIR": str(not_a_repo)},
            capture_output=True,
            text=True,
        )

        assert result.returncode == 0, (
            f"T-R2-e: atteso exit 0 (fail-safe), got {result.returncode}; stderr={result.stderr!r}"
        )
        assert log_file.exists(), (
            "T-R2-e: gas_debug.log deve essere creato con il warning di fail-safe"
        )
        assert "WARN" in log_file.read_text(), (
            f"T-R2-e: gas_debug.log deve contenere WARN, trovato: {log_file.read_text()!r}"
        )


# ─── Helpers per TestPromemoriaEnd ───────────────────────────────────────────

def _make_git_commit(repo: Path, rel_path: str, content: str, msg: str) -> None:
    """Aggiunge un commit nel repo di test."""
    f = repo / rel_path
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text(content)
    subprocess.run(["git", "add", rel_path], cwd=repo, check=True, capture_output=True)
    subprocess.run(
        ["git", "commit", "-m", msg],
        cwd=repo,
        check=True,
        capture_output=True,
        env={**os.environ,
             "GIT_AUTHOR_NAME": "T", "GIT_AUTHOR_EMAIL": "t@t.invalid",
             "GIT_COMMITTER_NAME": "T", "GIT_COMMITTER_EMAIL": "t@t.invalid"},
    )


def _init_bare_origin(work: Path, bare: Path) -> None:
    """Crea un bare repo come origin e vi pusha il branch main del repo di lavoro."""
    subprocess.run(["git", "init", "--bare", str(bare)], check=True, capture_output=True)
    subprocess.run(
        ["git", "remote", "add", "origin", str(bare)],
        cwd=work, check=True, capture_output=True,
    )
    subprocess.run(
        ["git", "push", "origin", "main"],
        cwd=work, check=True, capture_output=True,
    )


def _run_promemoria(
    repo: Path, *, stop_hook_active: bool = False, extra_env: dict | None = None,
    session_id: str = "",
) -> subprocess.CompletedProcess:
    """Esegue promemoria_end.sh con CLAUDE_PROJECT_DIR puntato al repo di test.

    Passa il payload JSON Stop hook su stdin (simula il runtime Claude Code).
    """
    payload = json.dumps({"stop_hook_active": stop_hook_active, "transcript_path": "",
                          "session_id": session_id})
    env = {**os.environ, "CLAUDE_PROJECT_DIR": str(repo)}
    if extra_env:
        env.update(extra_env)
    return subprocess.run(
        ["bash", str(PROMEMORIA_HOOK)],
        env=env,
        input=payload,
        capture_output=True,
        text=True,
        cwd=repo,
    )


def _make_broken_python3_path(tmp_path: Path) -> str:
    """PATH prepended with a fake python3 that exits 1 (simulates python3 absent)."""
    fake_bin = tmp_path / "fake_bin_no_py3"
    fake_bin.mkdir()
    fake_py = fake_bin / "python3"
    fake_py.write_text("#!/bin/bash\nexit 1\n")
    fake_py.chmod(0o755)
    return str(fake_bin) + ":" + os.environ.get("PATH", "")


def _is_blocked(result: subprocess.CompletedProcess) -> bool:
    """True se l'hook ha emesso una decisione di blocco JSON su stdout."""
    try:
        data = json.loads(result.stdout.strip())
        return data.get("decision") == "block"
    except (json.JSONDecodeError, AttributeError):
        return False


class TestPromemoriaEnd:
    """T-prom — hook promemoria_end.sh (blocco JSON su stdout, exit 0 in tutti i percorsi)."""

    def test_prom_1_no_commits_since_base_no_block(self, tmp_path):
        """T-prom-1: nessun commit di sessione → nessun blocco, exit 0."""
        work = tmp_path / "work"
        work.mkdir()
        _init_repo(work)
        bare = tmp_path / "origin.git"
        _init_bare_origin(work, bare)

        subprocess.run(
            ["git", "checkout", "-b", "feat/test"],
            cwd=work, check=True, capture_output=True,
        )

        result = _run_promemoria(work)
        assert result.returncode == 0, (
            f"T-prom-1: atteso exit 0, got {result.returncode}; stderr={result.stderr!r}"
        )
        assert not _is_blocked(result), (
            f"T-prom-1: nessun blocco atteso (SESSION_COMMITS=0), stdout={result.stdout!r}"
        )

    def test_prom_2_commits_no_handoff_blocks(self, tmp_path):
        """T-prom-2: commit di sessione senza handoff → blocco JSON su stdout, exit 0."""
        work = tmp_path / "work"
        work.mkdir()
        _init_repo(work)
        bare = tmp_path / "origin.git"
        _init_bare_origin(work, bare)

        subprocess.run(
            ["git", "checkout", "-b", "feat/test"],
            cwd=work, check=True, capture_output=True,
        )
        _make_git_commit(work, "some_file.txt", "contenuto\n", "feat: commit senza handoff")

        result = _run_promemoria(work)
        assert result.returncode == 0, (
            f"T-prom-2: atteso exit 0, got {result.returncode}; stderr={result.stderr!r}"
        )
        assert _is_blocked(result), (
            f"T-prom-2: atteso blocco JSON su stdout, stdout={result.stdout!r}"
        )

    def test_prom_3_handoff_as_last_commit_no_block(self, tmp_path):
        """T-prom-3: handoff come ultimo commit → nessun blocco, exit 0."""
        work = tmp_path / "work"
        work.mkdir()
        _init_repo(work)
        bare = tmp_path / "origin.git"
        _init_bare_origin(work, bare)

        subprocess.run(
            ["git", "checkout", "-b", "feat/test"],
            cwd=work, check=True, capture_output=True,
        )
        _make_git_commit(work, "some_file.txt", "ciao\n", "feat: qualcosa")
        _make_git_commit(work, "reports/handoff.md", "# handoff\n", "docs: aggiorna handoff")

        result = _run_promemoria(work)
        assert result.returncode == 0, (
            f"T-prom-3: atteso exit 0, got {result.returncode}; stderr={result.stderr!r}"
        )
        assert not _is_blocked(result), (
            f"T-prom-3: nessun blocco atteso (handoff è ultimo commit), stdout={result.stdout!r}"
        )

    def test_prom_3b_commits_after_handoff_blocks(self, tmp_path):
        """T-prom-3b: commit DOPO handoff → blocco (handoff non è più l'ultimo)."""
        work = tmp_path / "work"
        work.mkdir()
        _init_repo(work)
        bare = tmp_path / "origin.git"
        _init_bare_origin(work, bare)

        subprocess.run(
            ["git", "checkout", "-b", "feat/test"],
            cwd=work, check=True, capture_output=True,
        )
        _make_git_commit(work, "reports/handoff.md", "# handoff\n", "docs: aggiorna handoff")
        _make_git_commit(work, "extra.txt", "dopo\n", "feat: commit dopo handoff")

        result = _run_promemoria(work)
        assert result.returncode == 0, (
            f"T-prom-3b: atteso exit 0, got {result.returncode}; stderr={result.stderr!r}"
        )
        assert _is_blocked(result), (
            f"T-prom-3b: atteso blocco (commit dopo handoff), stdout={result.stdout!r}"
        )

    def test_prom_3c_only_chore_after_handoff_no_block(self, tmp_path):
        """T-prom-3c: solo chore(scrivi-rep): dopo handoff → nessun blocco."""
        work = tmp_path / "work"
        work.mkdir()
        _init_repo(work)
        bare = tmp_path / "origin.git"
        _init_bare_origin(work, bare)

        subprocess.run(
            ["git", "checkout", "-b", "feat/test"],
            cwd=work, check=True, capture_output=True,
        )
        _make_git_commit(work, "reports/handoff.md", "# handoff\n", "docs: aggiorna handoff")
        _make_git_commit(work, "reports/ultima_risposta.md", "testo\n",
                         "chore(scrivi-rep): ultima risposta salvata")

        result = _run_promemoria(work)
        assert result.returncode == 0, (
            f"T-prom-3c: atteso exit 0, got {result.returncode}; stderr={result.stderr!r}"
        )
        assert not _is_blocked(result), (
            f"T-prom-3c: nessun blocco atteso (solo chore dopo handoff), stdout={result.stdout!r}"
        )

    def test_prom_4_no_origin_warns_log_exit_0(self, tmp_path):
        """T-prom-4: nessun remote origin → WARN in gas_debug.log, exit 0, nessun blocco."""
        work = tmp_path / "work"
        work.mkdir()
        _init_repo(work)
        # Nessun remote: git merge-base origin/main HEAD fallirà

        subprocess.run(
            ["git", "checkout", "-b", "feat/no-origin"],
            cwd=work, check=True, capture_output=True,
        )
        _make_git_commit(work, "file.txt", "ciao\n", "feat: commit senza origin")

        log_file = work / "gas_debug.log"
        result = _run_promemoria(work)

        assert result.returncode == 0, (
            f"T-prom-4: atteso exit 0 (fail-safe), got {result.returncode}; stderr={result.stderr!r}"
        )
        assert log_file.exists(), (
            "T-prom-4: gas_debug.log deve essere creato con il WARN"
        )
        assert "WARN" in log_file.read_text(), (
            f"T-prom-4: gas_debug.log deve contenere WARN, trovato: {log_file.read_text()!r}"
        )
        assert not _is_blocked(result), (
            f"T-prom-4: nessun blocco atteso (fail-open su git error), stdout={result.stdout!r}"
        )

    def test_prom_5_head_on_main_silent_exit_0(self, tmp_path):
        """T-prom-5: HEAD su main → exit 0 silenzioso, nessun blocco."""
        work = tmp_path / "work"
        work.mkdir()
        _init_repo(work)
        # Resta su main (branch di default dopo _init_repo)

        result = _run_promemoria(work)

        assert result.returncode == 0, (
            f"T-prom-5: atteso exit 0 su main, got {result.returncode}; stderr={result.stderr!r}"
        )
        assert not _is_blocked(result), (
            f"T-prom-5: nessun blocco atteso su main, stdout={result.stdout!r}"
        )
        assert result.stdout == "", (
            f"T-prom-5: stdout deve essere vuoto su main, stdout={result.stdout!r}"
        )

    def test_prom_6_stop_hook_active_true_no_block(self, tmp_path):
        """T-prom-6: stop_hook_active=true → exit 0 silenzioso (anti-loop)."""
        work = tmp_path / "work"
        work.mkdir()
        _init_repo(work)
        bare = tmp_path / "origin.git"
        _init_bare_origin(work, bare)

        subprocess.run(
            ["git", "checkout", "-b", "feat/test"],
            cwd=work, check=True, capture_output=True,
        )
        # Commit senza handoff: normalmente bloccherebbe
        _make_git_commit(work, "file.txt", "ciao\n", "feat: commit senza handoff")

        result = _run_promemoria(work, stop_hook_active=True)
        assert result.returncode == 0, (
            f"T-prom-6: atteso exit 0 (anti-loop), got {result.returncode}; stderr={result.stderr!r}"
        )
        assert not _is_blocked(result), (
            f"T-prom-6: nessun blocco con stop_hook_active=true, stdout={result.stdout!r}"
        )
        assert result.stdout == "", (
            f"T-prom-6: stdout deve essere vuoto (anti-loop), stdout={result.stdout!r}"
        )

    def test_prom_7_non_git_dir_exit_0(self, tmp_path):
        """T-prom-7: directory non-git → exit 0 silenzioso (fail-open)."""
        non_git = tmp_path / "not_a_repo"
        non_git.mkdir()

        result = subprocess.run(
            ["bash", str(PROMEMORIA_HOOK)],
            env={**os.environ, "CLAUDE_PROJECT_DIR": str(non_git)},
            input=json.dumps({"stop_hook_active": False}),
            capture_output=True,
            text=True,
            cwd=non_git,
        )
        assert result.returncode == 0, (
            f"T-prom-7: atteso exit 0 su dir non-git, got {result.returncode}; stderr={result.stderr!r}"
        )
        assert not _is_blocked(result), (
            f"T-prom-7: nessun blocco atteso su dir non-git, stdout={result.stdout!r}"
        )

    def test_prom_8_stop_hook_active_no_python3_no_block(self, tmp_path):
        """T-prom-8: stop_hook_active=true + python3 assente → grep fallback → exit 0, nessun blocco."""
        work = tmp_path / "work"
        work.mkdir()
        _init_repo(work)
        bare = tmp_path / "origin.git"
        _init_bare_origin(work, bare)

        subprocess.run(
            ["git", "checkout", "-b", "feat/test"],
            cwd=work, check=True, capture_output=True,
        )
        _make_git_commit(work, "file.txt", "ciao\n", "feat: commit senza handoff")

        broken_path = _make_broken_python3_path(tmp_path)
        result = _run_promemoria(work, stop_hook_active=True, extra_env={"PATH": broken_path})
        assert result.returncode == 0, (
            f"T-prom-8: atteso exit 0 (grep fallback), got {result.returncode}; stderr={result.stderr!r}"
        )
        assert not _is_blocked(result), (
            f"T-prom-8: nessun blocco con stop_hook_active=true (grep fallback), stdout={result.stdout!r}"
        )

    def test_prom_8b_stop_hook_false_no_python3_blocks(self, tmp_path):
        """T-prom-8b: stop_hook_active=false + python3 assente + commit senza handoff → blocco JSON."""
        work = tmp_path / "work"
        work.mkdir()
        _init_repo(work)
        bare = tmp_path / "origin.git"
        _init_bare_origin(work, bare)

        subprocess.run(
            ["git", "checkout", "-b", "feat/test"],
            cwd=work, check=True, capture_output=True,
        )
        _make_git_commit(work, "file.txt", "ciao\n", "feat: commit senza handoff")

        broken_path = _make_broken_python3_path(tmp_path)
        result = _run_promemoria(work, stop_hook_active=False, extra_env={"PATH": broken_path})
        assert result.returncode == 0, (
            f"T-prom-8b: atteso exit 0, got {result.returncode}; stderr={result.stderr!r}"
        )
        assert _is_blocked(result), (
            f"T-prom-8b: atteso blocco JSON (python3 assente, stop_hook_active=false), stdout={result.stdout!r}"
        )


# ─── Helpers per TestCheckLanding ────────────────────────────────────────────

CHECK_LANDING = Path(__file__).parent.parent / "scripts" / "check_landing.sh"


def _run_check_landing(repo: Path, extra_env: dict | None = None) -> subprocess.CompletedProcess:
    """Esegue check_landing.sh con CLAUDE_PROJECT_DIR puntato al repo di test."""
    env = {**os.environ, "CLAUDE_PROJECT_DIR": str(repo)}
    if extra_env:
        env.update(extra_env)
    return subprocess.run(
        ["bash", str(CHECK_LANDING)],
        env=env,
        capture_output=True,
        text=True,
        cwd=repo,
    )


def _write_required_files(repo: Path) -> None:
    """Scrive i tre file di report obbligatori non vuoti."""
    for name in ("ultimo_report.md", "handoff.md", "diff_sessione.md"):
        f = repo / "reports" / name
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_text(f"# {name}\ncontenuto\n")


def _setup_repo_with_origin_and_files(work: Path, bare: Path) -> None:
    """Init repo, crea i file obbligatori, pusha su bare origin."""
    _init_repo(work)
    _write_required_files(work)
    subprocess.run(["git", "add", "-A"], cwd=work, check=True, capture_output=True)
    subprocess.run(
        ["git", "commit", "-m", "add reports"],
        cwd=work, check=True, capture_output=True,
        env={**os.environ,
             "GIT_AUTHOR_NAME": "T", "GIT_AUTHOR_EMAIL": "t@t.invalid",
             "GIT_COMMITTER_NAME": "T", "GIT_COMMITTER_EMAIL": "t@t.invalid"},
    )
    subprocess.run(["git", "init", "--bare", str(bare)], check=True, capture_output=True)
    subprocess.run(
        ["git", "remote", "add", "origin", str(bare)],
        cwd=work, check=True, capture_output=True,
    )
    subprocess.run(["git", "push", "origin", "main"], cwd=work, check=True, capture_output=True)


def _make_fake_gh(tmp_path: Path, script_body: str) -> dict:
    """Crea un fake gh script e restituisce env con PATH aggiornato."""
    bin_dir = tmp_path / "fakebin"
    bin_dir.mkdir(exist_ok=True)
    fake_gh = bin_dir / "gh"
    fake_gh.write_text(f"#!/usr/bin/env bash\n{script_body}\n")
    fake_gh.chmod(0o755)
    return {"PATH": f"{bin_dir}:{os.environ['PATH']}"}


class TestCheckLanding:
    """T-land — scripts/check_landing.sh (Check A file, B pushed, C PR)."""

    def test_land_1_all_ok_no_gh_exit_0(self, tmp_path):
        """T-land-1: file OK, HEAD pushato, gh non in PATH → exit 0 (Check C skip)."""
        work = tmp_path / "work"
        work.mkdir()
        bare = tmp_path / "origin.git"
        _setup_repo_with_origin_and_files(work, bare)

        # Rimuovi gh dal PATH per forzare lo skip del Check C
        env_no_gh = {"PATH": "/usr/bin:/bin"}
        result = _run_check_landing(work, extra_env=env_no_gh)

        assert result.returncode == 0, (
            f"T-land-1: atteso exit 0 (gh assente → skip C), got {result.returncode}; "
            f"stderr={result.stderr!r}"
        )

    def test_land_2_missing_file_exit_1(self, tmp_path):
        """T-land-2: reports/handoff.md assente → exit 1 (Check A bloccante)."""
        work = tmp_path / "work"
        work.mkdir()
        bare = tmp_path / "origin.git"
        _setup_repo_with_origin_and_files(work, bare)

        # Rimuovi handoff.md
        (work / "reports" / "handoff.md").unlink()

        result = _run_check_landing(work, extra_env={"PATH": "/usr/bin:/bin"})

        assert result.returncode == 1, (
            f"T-land-2: atteso exit 1 (file mancante), got {result.returncode}; "
            f"stderr={result.stderr!r}"
        )
        assert "FAIL" in result.stderr, (
            f"T-land-2: atteso FAIL in stderr, stderr={result.stderr!r}"
        )

    def test_land_3_empty_file_exit_1(self, tmp_path):
        """T-land-3: reports/ultimo_report.md presente ma vuoto → exit 1 (Check A bloccante)."""
        work = tmp_path / "work"
        work.mkdir()
        bare = tmp_path / "origin.git"
        _setup_repo_with_origin_and_files(work, bare)

        # Svuota il file
        (work / "reports" / "ultimo_report.md").write_text("")

        result = _run_check_landing(work, extra_env={"PATH": "/usr/bin:/bin"})

        assert result.returncode == 1, (
            f"T-land-3: atteso exit 1 (file vuoto), got {result.returncode}; "
            f"stderr={result.stderr!r}"
        )
        assert "FAIL" in result.stderr, (
            f"T-land-3: atteso FAIL in stderr, stderr={result.stderr!r}"
        )

    def test_land_tag_omonimo_non_maschera_head_non_pushato(self, tmp_path):
        """R-144-1 (verifica esterna #122, V-2): un tag "origin/main" su HEAD non pushato
        non fa passare il Check B: il confronto usa refs/remotes/origin/<branch>."""
        work = tmp_path / "work"
        work.mkdir()
        bare = tmp_path / "origin.git"
        _setup_repo_with_origin_and_files(work, bare)
        (work / "nuovo.txt").write_text("x\n")
        subprocess.run(["git", "add", "nuovo.txt"], cwd=work, check=True, capture_output=True)
        subprocess.run(
            ["git", "commit", "-m", "non pushato"], cwd=work, check=True, capture_output=True,
            env={**os.environ,
                 "GIT_AUTHOR_NAME": "T", "GIT_AUTHOR_EMAIL": "t@t.invalid",
                 "GIT_COMMITTER_NAME": "T", "GIT_COMMITTER_EMAIL": "t@t.invalid"},
        )
        subprocess.run(["git", "tag", "origin/main", "HEAD"], cwd=work,
                       check=True, capture_output=True)
        result = _run_check_landing(work, extra_env={"PATH": "/usr/bin:/bin"})
        assert result.returncode == 1, (
            f"atteso exit 1 (HEAD non pushato), got {result.returncode}; stderr={result.stderr!r}"
        )

    def test_land_4_remote_absent_exit_1(self, tmp_path):
        """T-land-4: nessun remote per il branch → exit 1 (Check B bloccante)."""
        work = tmp_path / "work"
        work.mkdir()
        _init_repo(work)
        _write_required_files(work)
        # Nessun remote: origin non esiste

        result = _run_check_landing(work, extra_env={"PATH": "/usr/bin:/bin"})

        assert result.returncode == 1, (
            f"T-land-4: atteso exit 1 (remote assente), got {result.returncode}; "
            f"stderr={result.stderr!r}"
        )
        assert "FAIL" in result.stderr, (
            f"T-land-4: atteso FAIL in stderr, stderr={result.stderr!r}"
        )

    def test_land_5_head_diverged_exit_1(self, tmp_path):
        """T-land-5: HEAD locale avanti di origin (diverged) → exit 1 (Check B bloccante)."""
        work = tmp_path / "work"
        work.mkdir()
        bare = tmp_path / "origin.git"
        _setup_repo_with_origin_and_files(work, bare)

        # Aggiungi un commit locale senza pushare
        _make_git_commit(work, "extra.txt", "extra\n", "feat: commit non pushato")

        result = _run_check_landing(work, extra_env={"PATH": "/usr/bin:/bin"})

        assert result.returncode == 1, (
            f"T-land-5: atteso exit 1 (HEAD diverged), got {result.returncode}; "
            f"stderr={result.stderr!r}"
        )
        assert "FAIL" in result.stderr, (
            f"T-land-5: atteso FAIL in stderr, stderr={result.stderr!r}"
        )

    def test_land_6_gh_available_no_pr_exit_1(self, tmp_path):
        """T-land-6: A e B OK, gh disponibile + auth OK ma nessuna PR → exit 1 (Check C bloccante)."""
        work = tmp_path / "work"
        work.mkdir()
        bare = tmp_path / "origin.git"
        _setup_repo_with_origin_and_files(work, bare)

        # Fake gh: auth status ok, pr list restituisce array vuoto
        fake_gh_script = (
            'case "$*" in\n'
            '  "auth status") exit 0;;\n'
            '  pr*) echo "[]"; exit 0;;\n'
            '  *) exit 1;;\n'
            'esac\n'
        )
        env_fake = _make_fake_gh(tmp_path, fake_gh_script)

        result = _run_check_landing(work, extra_env=env_fake)

        assert result.returncode == 1, (
            f"T-land-6: atteso exit 1 (nessuna PR), got {result.returncode}; "
            f"stderr={result.stderr!r}"
        )
        assert "FAIL" in result.stderr, (
            f"T-land-6: atteso FAIL in stderr, stderr={result.stderr!r}"
        )


# ─── TestPromemoriaCounter ────────────────────────────────────────────────────
#
# Verifica il nuovo comportamento a contatore di promemoria_end.sh:
#   - 1°/2°/3° invocazione → blocca (JSON su stdout)
#   - 4° invocazione → fail-open + WARNING su stderr (nessun JSON di blocco)
#   - Handoff fresco dopo blocchi → azzera il contatore
#
# Tutti i test usano repo git temporanei reali con un bare origin (per merge-base).

FINE_TASK_FINALE = Path(__file__).parent.parent / "scripts" / "fine_task_finale.sh"


def _run_promemoria_fresh(repo: Path, session_id: str = "") -> subprocess.CompletedProcess:
    """Esegue promemoria_end.sh con stop_hook_active=false (condizione di blocco potenziale)."""
    return _run_promemoria(repo, stop_hook_active=False, session_id=session_id)


def _read_prom_counter(repo: Path) -> int:
    """Legge il contatore da promemoria_block_count (formato 'session_id:count')."""
    raw = (repo / ".git" / "promemoria_block_count").read_text().strip()
    return int(raw.split(":")[-1])


class TestPromemoriaCounter:
    """T-prom-counter — comportamento a contatore (max 3 blocchi, poi fail-open)."""

    def _setup_repo_with_commit_no_handoff(self, tmp_path: Path):
        """Init repo con origin, feature branch, commit senza handoff (blocco atteso)."""
        work = tmp_path / "work"
        work.mkdir()
        _init_repo(work)
        bare = tmp_path / "origin.git"
        _init_bare_origin(work, bare)
        subprocess.run(
            ["git", "checkout", "-b", "feat/test-counter"],
            cwd=work, check=True, capture_output=True,
        )
        _make_git_commit(work, "some_file.txt", "contenuto\n", "feat: commit senza handoff")
        return work

    def test_prom_counter_1st_blocks(self, tmp_path):
        """T-prom-counter-1: 1° invocazione → blocca (JSON su stdout, count=1)."""
        work = self._setup_repo_with_commit_no_handoff(tmp_path)
        result = _run_promemoria_fresh(work)
        assert result.returncode == 0, f"T-prom-counter-1: atteso exit 0, got {result.returncode}"
        assert _is_blocked(result), (
            f"T-prom-counter-1: atteso blocco JSON al 1° tentativo, stdout={result.stdout!r}"
        )
        count = _read_prom_counter(work)
        assert count == 1, f"T-prom-counter-1: contatore atteso 1, trovato {count}"

    def test_prom_counter_2nd_blocks(self, tmp_path):
        """T-prom-counter-2: 2° invocazione → blocca ancora (count=2)."""
        work = self._setup_repo_with_commit_no_handoff(tmp_path)
        _run_promemoria_fresh(work)  # 1° invocazione
        result = _run_promemoria_fresh(work)  # 2° invocazione
        assert result.returncode == 0
        assert _is_blocked(result), (
            f"T-prom-counter-2: atteso blocco JSON al 2° tentativo, stdout={result.stdout!r}"
        )
        count = _read_prom_counter(work)
        assert count == 2, f"T-prom-counter-2: contatore atteso 2, trovato {count}"

    def test_prom_counter_3rd_blocks(self, tmp_path):
        """T-prom-counter-3: 3° invocazione → blocca ancora (count=3)."""
        work = self._setup_repo_with_commit_no_handoff(tmp_path)
        for _ in range(2):
            _run_promemoria_fresh(work)
        result = _run_promemoria_fresh(work)  # 3°
        assert result.returncode == 0
        assert _is_blocked(result), (
            f"T-prom-counter-3: atteso blocco JSON al 3° tentativo, stdout={result.stdout!r}"
        )
        count = _read_prom_counter(work)
        assert count == 3, f"T-prom-counter-3: contatore atteso 3, trovato {count}"

    def test_prom_counter_4th_fail_open(self, tmp_path):
        """T-prom-counter-4: 4° invocazione → fail-open (nessun blocco JSON) + WARNING su stderr."""
        work = self._setup_repo_with_commit_no_handoff(tmp_path)
        for _ in range(3):
            _run_promemoria_fresh(work)
        result = _run_promemoria_fresh(work)  # 4°
        assert result.returncode == 0, f"T-prom-counter-4: atteso exit 0, got {result.returncode}"
        assert not _is_blocked(result), (
            f"T-prom-counter-4: atteso fail-open (nessun blocco JSON) al 4° tentativo, "
            f"stdout={result.stdout!r}"
        )
        assert result.stderr.strip(), (
            "T-prom-counter-4: atteso WARNING su stderr al 4° tentativo"
        )
        assert "WARN" in result.stderr or "warn" in result.stderr.lower(), (
            f"T-prom-counter-4: WARNING deve contenere 'WARN', stderr={result.stderr!r}"
        )

    def test_prom_counter_reason_is_imperative(self, tmp_path):
        """T-prom-counter-reason: il blocco usa la reason imperativa richiesta."""
        work = self._setup_repo_with_commit_no_handoff(tmp_path)
        result = _run_promemoria_fresh(work)
        assert _is_blocked(result), f"T-prom-counter-reason: atteso blocco, stdout={result.stdout!r}"
        data = json.loads(result.stdout.strip())
        reason = data.get("reason", "")
        assert "fine-task" in reason.lower() or "/fine-task" in reason, (
            f"T-prom-counter-reason: reason deve menzionare /fine-task, reason={reason!r}"
        )
        assert "obbligatorio" in reason.lower() or "ORA" in reason, (
            f"T-prom-counter-reason: reason deve essere imperativa ('obbligatorio' o 'ORA'), "
            f"reason={reason!r}"
        )

    def test_prom_counter_fresh_handoff_resets_counter(self, tmp_path):
        """T-prom-counter-reset: handoff fresco azzera il contatore."""
        work = self._setup_repo_with_commit_no_handoff(tmp_path)
        for _ in range(2):
            _run_promemoria_fresh(work)
        count_before = _read_prom_counter(work)
        assert count_before == 2

        # Aggiungi commit con handoff
        _make_git_commit(work, "reports/handoff.md", "# handoff\n", "docs: handoff fresco")
        result = _run_promemoria_fresh(work)
        assert result.returncode == 0
        assert not _is_blocked(result), (
            f"T-prom-counter-reset: nessun blocco atteso con handoff fresco, "
            f"stdout={result.stdout!r}"
        )
        assert not (work / ".git" / "promemoria_block_count").exists(), (
            "T-prom-counter-reset: il file contatore deve essere rimosso dopo handoff fresco"
        )

    def test_prom_counter_session_id_resets_on_new_session(self, tmp_path):
        """T-prom-counter-session: cambio session_id → contatore riparte da 0 (B1)."""
        work = self._setup_repo_with_commit_no_handoff(tmp_path)

        # Sessione A: 4 tentativi → il 4° è fail-open
        for _ in range(3):
            r = _run_promemoria_fresh(work, session_id="session-A")
            assert _is_blocked(r), "sessione-A tentativo 1-3: atteso blocco"
        r4 = _run_promemoria_fresh(work, session_id="session-A")
        assert not _is_blocked(r4), "sessione-A tentativo 4: atteso fail-open"

        # Nuova sessione B: counter deve ripartire da 0 → primo tentativo blocca di nuovo
        r_b1 = _run_promemoria_fresh(work, session_id="session-B")
        assert _is_blocked(r_b1), (
            f"T-prom-counter-session: sessione-B 1° tentativo: atteso blocco (reset), "
            f"stdout={r_b1.stdout!r}"
        )
        count_b = _read_prom_counter(work)
        assert count_b == 1, (
            f"T-prom-counter-session: contatore sessione-B atteso 1, trovato {count_b}"
        )


# ─── TestFinaleScript ────────────────────────────────────────────────────────
#
# Verifica scripts/fine_task_finale.sh su repo git temporanei reali.
#   T-finale-1: branch main → exit 1 (mai push su main)
#   T-finale-2: check_handoff fallisce → exit 1, nessun push
#   T-finale-3: tutto verde → URL_HANDOFF stampato su stdout, exit 0
#   T-finale-4: IP in reports/ → exit 1, nessun push


def _run_finale(
    repo: Path,
    extra_env: dict | None = None,
    cwd: Path | None = None,
) -> subprocess.CompletedProcess:
    """Esegue fine_task_finale.sh con CLAUDE_PROJECT_DIR puntato al repo di test."""
    env = {**os.environ, "CLAUDE_PROJECT_DIR": str(repo)}
    if extra_env:
        env.update(extra_env)
    return subprocess.run(
        ["bash", str(FINE_TASK_FINALE)],
        env=env,
        capture_output=True,
        text=True,
        cwd=cwd or repo,
    )


def _make_git_commit_env(repo: Path, rel_path: str, content: str, msg: str) -> None:
    """Commit con GIT_{AUTHOR,COMMITTER} espliciti (compatibile con repo senza config)."""
    f = repo / rel_path
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text(content)
    subprocess.run(["git", "add", rel_path], cwd=repo, check=True, capture_output=True)
    subprocess.run(
        ["git", "commit", "-m", msg],
        cwd=repo, check=True, capture_output=True,
        env={**os.environ,
             "GIT_AUTHOR_NAME": "T", "GIT_AUTHOR_EMAIL": "t@t.invalid",
             "GIT_COMMITTER_NAME": "T", "GIT_COMMITTER_EMAIL": "t@t.invalid"},
    )


class TestFinaleScript:
    """T-finale — scripts/fine_task_finale.sh."""

    def test_finale_1_main_branch_rejected(self, tmp_path):
        """T-finale-1: HEAD su main → exit 1, messaggio errore su stderr."""
        _init_repo(tmp_path)
        # HEAD su main (default dopo _init_repo)
        result = _run_finale(tmp_path)
        assert result.returncode == 1, (
            f"T-finale-1: atteso exit 1 (main), got {result.returncode}; stderr={result.stderr!r}"
        )
        assert "main" in result.stderr.lower() or "ERRORE" in result.stderr, (
            f"T-finale-1: messaggio deve menzionare 'main', stderr={result.stderr!r}"
        )

    def test_finale_2_check_handoff_fails_exit_1_no_push(self, tmp_path):
        """T-finale-2: check_handoff fallisce → exit 1, nessun push.

        Setup: feature branch con commit che include sia foo.txt sia reports/handoff.md,
        ma §2 di handoff.md dichiara solo foo.txt (mismatch → check_handoff exit 1).
        """
        bare = tmp_path / "bare"
        work = tmp_path / "work"
        _init_repo(work)
        subprocess.run(["git", "init", "--bare", str(bare)], check=True, capture_output=True)
        subprocess.run(
            ["git", "remote", "add", "origin", str(bare)],
            cwd=work, check=True, capture_output=True,
        )
        subprocess.run(["git", "push", "origin", "main"], cwd=work, check=True, capture_output=True)
        subprocess.run(
            ["git", "checkout", "-b", "feat/test-finale"],
            cwd=work, check=True, capture_output=True,
        )

        # §2 dichiara solo foo.txt ma il diff reale è {foo.txt, reports/handoff.md}
        handoff_content = (
            "# HANDOFF\n\n"
            "## §2 GIT DIFF --STAT (sessione)\n\n"
            "```\n"
            " foo.txt | 1 +\n"
            " 1 file changed, 1 insertion(+)\n"
            "```\n\n"
            "## §4 VERDETTO DEL REVISORE (per commit motore)\n\n"
            "nessun diff motore, revisore non richiesto.\n"
        )
        _make_git_commit_env(work, "foo.txt", "bar\n", "feat: foo")
        _make_git_commit_env(work, "reports/handoff.md", handoff_content, "docs: handoff (§2 incompleto)")

        before_sha = subprocess.run(
            ["git", "--git-dir", str(bare), "rev-parse", "refs/heads/main"],
            capture_output=True, text=True, check=True,
        ).stdout.strip()

        result = _run_finale(work, cwd=work)

        assert result.returncode == 1, (
            f"T-finale-2: atteso exit 1 (check_handoff rosso), got {result.returncode}; "
            f"stderr={result.stderr!r}"
        )
        # Nessun push: il branch non deve esistere su origin
        rev = subprocess.run(
            ["git", "--git-dir", str(bare), "rev-parse", "refs/heads/feat/test-finale"],
            capture_output=True, text=True,
        )
        branch_exists_on_origin = rev.returncode == 0
        assert not branch_exists_on_origin, (
            f"T-finale-2: il branch non deve essere pushato dopo check_handoff rosso, "
            f"trovato su origin: {rev.stdout.strip()!r}"
        )

    def test_finale_3_all_green_no_handoff_url_not_available(self, tmp_path):
        """T-finale-3: diff vuoto → handoff.md non rigenerato → URL_HANDOFF: non disponibile (B2)."""
        bare = tmp_path / "bare"
        work = tmp_path / "work"
        _init_repo(work)
        subprocess.run(["git", "init", "--bare", str(bare)], check=True, capture_output=True)
        subprocess.run(
            ["git", "remote", "add", "origin", str(bare)],
            cwd=work, check=True, capture_output=True,
        )
        subprocess.run(["git", "push", "origin", "main"], cwd=work, check=True, capture_output=True)
        subprocess.run(
            ["git", "checkout", "-b", "feat/test-green"],
            cwd=work, check=True, capture_output=True,
        )
        subprocess.run(
            ["git", "push", "-u", "origin", "feat/test-green"],
            cwd=work, check=True, capture_output=True,
        )
        # Nessun commit sul branch → diff BASE..HEAD vuoto → handoff.md non rigenerato
        # Nessun file in reports/ → Gate IP OK

        result = _run_finale(work, cwd=work)

        assert result.returncode == 0, (
            f"T-finale-3: atteso exit 0, got {result.returncode}; "
            f"stderr={result.stderr!r} stdout={result.stdout!r}"
        )
        assert "URL_HANDOFF: non disponibile" in result.stdout, (
            f"T-finale-3: atteso 'URL_HANDOFF: non disponibile' (handoff non rigenerato), "
            f"stdout={result.stdout!r}"
        )
        assert "raw.githubusercontent.com" not in result.stdout, (
            f"T-finale-3: NON atteso URL reale quando handoff non rigenerato, stdout={result.stdout!r}"
        )

    def test_finale_3b_handoff_regenerated_url_printed(self, tmp_path):
        """T-finale-3b: reports/handoff.md nel diff sessione → URL reale con SHA lungo."""
        bare = tmp_path / "bare"
        work = tmp_path / "work"
        _init_repo(work)
        subprocess.run(["git", "init", "--bare", str(bare)], check=True, capture_output=True)
        subprocess.run(
            ["git", "remote", "add", "origin", str(bare)],
            cwd=work, check=True, capture_output=True,
        )
        subprocess.run(["git", "push", "origin", "main"], cwd=work, check=True, capture_output=True)
        subprocess.run(
            ["git", "checkout", "-b", "feat/test-3b"],
            cwd=work, check=True, capture_output=True,
        )
        # Commit reports/handoff.md con §2 valido (solo reports/handoff.md) e §4 OK, nessun IP
        handoff_valid = (
            "# HANDOFF\n\n"
            "## §2 GIT DIFF --STAT (sessione)\n\n"
            "```\n"
            " reports/handoff.md | 10 ++\n"
            " 1 file changed, 10 insertions(+)\n"
            "```\n\n"
            "## §4 VERDETTO DEL REVISORE (per commit motore)\n\n"
            "nessun diff motore, revisore non richiesto.\n"
        )
        _make_git_commit_env(work, "reports/handoff.md", handoff_valid, "docs: handoff rigenerato")
        # Pusha il branch (con tracking) — il push successivo dentro lo script è no-op
        subprocess.run(
            ["git", "push", "-u", "origin", "feat/test-3b"],
            cwd=work, check=True, capture_output=True,
        )
        sha = subprocess.run(
            ["git", "rev-parse", "HEAD"], cwd=work, capture_output=True, text=True, check=True,
        ).stdout.strip()

        result = _run_finale(work, cwd=work)

        assert result.returncode == 0, (
            f"T-finale-3b: atteso exit 0, got {result.returncode}; "
            f"stderr={result.stderr!r} stdout={result.stdout!r}"
        )
        assert "raw.githubusercontent.com" in result.stdout, (
            f"T-finale-3b: URL reale atteso su stdout, stdout={result.stdout!r}"
        )
        assert sha in result.stdout, (
            f"T-finale-3b: URL deve contenere SHA lungo {sha!r}, stdout={result.stdout!r}"
        )

    def test_finale_4_ip_in_reports_exit_1_no_push(self, tmp_path):
        """T-finale-4: IP in reports/ (committed) → exit 1, nessun nuovo push."""
        bare = tmp_path / "bare"
        work = tmp_path / "work"
        _init_repo(work)
        subprocess.run(["git", "init", "--bare", str(bare)], check=True, capture_output=True)
        subprocess.run(
            ["git", "remote", "add", "origin", str(bare)],
            cwd=work, check=True, capture_output=True,
        )
        subprocess.run(["git", "push", "origin", "main"], cwd=work, check=True, capture_output=True)
        subprocess.run(
            ["git", "checkout", "-b", "feat/test-ip"],
            cwd=work, check=True, capture_output=True,
        )

        # §2 vuoto e §4 "nessun diff motore" → check_handoff non applicabile, check_verdetto OK
        # MA ci sono IP nel reports/handoff.md
        handoff_ip = (
            "# HANDOFF\n\n"
            "## §2 GIT DIFF --STAT (sessione)\n\n"
            "```\n"
            " reports/handoff.md | 1 +\n"
            " 1 file changed, 1 insertion(+)\n"
            "```\n\n"
            "## §4 VERDETTO DEL REVISORE (per commit motore)\n\n"
            "nessun diff motore, revisore non richiesto.\n\n"
            "## §6 STATO CI\n\n"
            "Connessione al server 192.168.1.1 riuscita.\n"  # gasmerge-ip-ok
        )
        _make_git_commit_env(work, "reports/handoff.md", handoff_ip, "docs: handoff con IP")

        result = _run_finale(work, cwd=work)

        assert result.returncode == 1, (
            f"T-finale-4: atteso exit 1 (IP trovato), got {result.returncode}; "
            f"stderr={result.stderr!r}"
        )
        assert "IP trovato" in result.stderr, (
            f"T-finale-4: stderr deve contenere 'IP trovato', stderr={result.stderr!r}"
        )

    def test_finale_4b_ip_outside_reports_exit_1(self, tmp_path):
        """T-finale-4b: IP fuori da reports/ senza token → exit 1 (full-tree check)."""
        bare = tmp_path / "bare"
        work = tmp_path / "work"
        _init_repo(work)
        subprocess.run(["git", "init", "--bare", str(bare)], check=True, capture_output=True)
        subprocess.run(
            ["git", "remote", "add", "origin", str(bare)],
            cwd=work, check=True, capture_output=True,
        )
        subprocess.run(["git", "push", "origin", "main"], cwd=work, check=True, capture_output=True)
        subprocess.run(
            ["git", "checkout", "-b", "feat/test-4b"],
            cwd=work, check=True, capture_output=True,
        )

        # File fuori da reports/ con IP non-loopback, senza token
        _make_git_commit_env(work, "scripts/test_ip.sh", "echo 10.0.0.1\n", "chore: script con IP")  # gasmerge-ip-ok

        result = _run_finale(work, cwd=work)

        assert result.returncode == 1, (
            f"T-finale-4b: atteso exit 1 (IP fuori reports/), got {result.returncode}; "
            f"stderr={result.stderr!r}"
        )
        assert "IP trovato" in result.stderr, (
            f"T-finale-4b: stderr deve contenere 'IP trovato', stderr={result.stderr!r}"
        )

    def test_finale_4c_ip_with_token_passes_gate(self, tmp_path):
        """T-finale-4c: IP con token gasmerge-ip-ok sulla stessa riga → Gate IP OK."""
        bare = tmp_path / "bare"
        work = tmp_path / "work"
        _init_repo(work)
        subprocess.run(["git", "init", "--bare", str(bare)], check=True, capture_output=True)
        subprocess.run(
            ["git", "remote", "add", "origin", str(bare)],
            cwd=work, check=True, capture_output=True,
        )
        subprocess.run(["git", "push", "origin", "main"], cwd=work, check=True, capture_output=True)
        subprocess.run(
            ["git", "checkout", "-b", "feat/test-4c"],
            cwd=work, check=True, capture_output=True,
        )

        # IP con token gasmerge-ip-ok sulla stessa riga → allowlistato
        _make_git_commit_env(
            work, "scripts/test_allowed.sh",
            "echo 10.0.0.1  # gasmerge-ip-ok\n",
            "chore: script con IP allowlistato",
        )
        subprocess.run(
            ["git", "push", "-u", "origin", "feat/test-4c"],
            cwd=work, check=True, capture_output=True,
        )

        result = _run_finale(work, cwd=work)

        assert result.returncode == 0, (
            f"T-finale-4c: atteso exit 0 (IP allowlistato), got {result.returncode}; "
            f"stderr={result.stderr!r} stdout={result.stdout!r}"
        )
        assert "IP trovato" not in result.stderr, (
            f"T-finale-4c: nessun blocco IP atteso, stderr={result.stderr!r}"
        )
