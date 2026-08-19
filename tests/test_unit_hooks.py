"""Tests per .claude/hooks/session_end.sh, scrivi_rep.sh e review_gate.sh."""
import json
import os
import subprocess
from pathlib import Path

import pytest

HOOK = Path(__file__).parent.parent / ".claude" / "hooks" / "session_end.sh"
SCRIVI_REP_HOOK = Path(__file__).parent.parent / ".claude" / "hooks" / "scrivi_rep.sh"
REVIEW_GATE_HOOK = Path(__file__).parent.parent / ".claude" / "hooks" / "review_gate.sh"


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
        """JSON stdin che simula un tool use 'git commit'."""
        return json.dumps([{"tool_input": {"command": "git commit -m 'test'"}}])

    def _run(self, repo: Path, *, has_review_ok: bool = False) -> subprocess.CompletedProcess:
        env = {**os.environ, "CLAUDE_PROJECT_DIR": str(repo)}
        if has_review_ok:
            (repo / ".claude").mkdir(exist_ok=True)
            (repo / ".claude" / ".review_ok").touch()
        return subprocess.run(
            ["bash", str(REVIEW_GATE_HOOK)],
            input=self._stdin_commit(),
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

    def test_gate_d_git_failure_blocks(self, tmp_path):
        """T-gate-D: CLAUDE_PROJECT_DIR non è un git repo → git diff fallisce → FAIL-CLOSED (exit 2)."""
        # tmp_path esiste ma non ha .git: cd riesce, git diff fallisce → deve bloccare
        result = self._run(tmp_path)
        assert result.returncode == 2, (
            f"Atteso exit 2 (fail-closed), got {result.returncode}; stderr={result.stderr!r}"
        )
        assert result.stderr.strip(), "Messaggio di errore atteso su stderr"

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
