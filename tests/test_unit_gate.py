"""Unit tests for modules/gate/gate.py — C1 scaffolding (zero integration with gas.py).

Tested in isolation: no GasKernel instantiation, no LLM calls, no DB access.

⚠️  CI NOTE (2026-09-30): this file is NOT yet included in ci.yml
    (which only runs test_unit_kernel.py, test_unit_hooks.py,
    test_unit_voice_server.py by explicit name).  Tracked as a finding in
    reports/handoff.md §5 — ci.yml must be updated to add a pytest step for
    this file.  Until then, run locally with:
        python -m pytest tests/test_unit_gate.py -v
"""

import os
import pytest
from modules.gate.gate import (
    GateClass,
    GATE_ALLOWLIST,
    GATE_DENY_TOOLS,
    gate_classify,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _wf(path: str) -> GateClass:
    """Shorthand: gate_classify write_file with given path."""
    return gate_classify("write_file", {"relative_path": path, "content": "x"})


def _rf(path: str) -> GateClass:
    """Shorthand: gate_classify read_file with given path."""
    return gate_classify("read_file", {"relative_path": path})


# ---------------------------------------------------------------------------
# T-gate-kn: known tools → expected GateClass
# ---------------------------------------------------------------------------

class TestKnownTools:
    def test_read_file_safe(self):
        assert _rf("reports/note.md") == GateClass.SAFE

    def test_calcola_safe(self):
        assert gate_classify("calcola", {"expr": "2+2"}) == GateClass.SAFE

    def test_ricorda_safe(self):
        assert gate_classify("ricorda", {"query": "lead"}) == GateClass.SAFE

    def test_notify_telegram_safe(self):
        assert gate_classify("notify_telegram", {"text": "ciao"}) == GateClass.SAFE

    def test_write_file_uncertain(self):
        assert _wf("reports/note.md") == GateClass.UNCERTAIN

    def test_salva_contatto_uncertain(self):
        assert gate_classify("salva_contatto", {"chiave": "mario"}) == GateClass.UNCERTAIN

    def test_imposta_stato_contatto_uncertain(self):
        assert gate_classify(
            "imposta_stato_contatto", {"chiave": "mario", "stato": "interessato"}
        ) == GateClass.UNCERTAIN

    def test_send_email_irreversible(self):
        assert gate_classify(
            "send_email", {"to": "x@x.com", "subject": "s", "body": "b"}
        ) == GateClass.IRREVERSIBLE

    def test_send_dm_irreversible(self):
        assert gate_classify("send_dm", {"to": "user", "text": "msg"}) == GateClass.IRREVERSIBLE

    def test_git_push_irreversible(self):
        assert gate_classify("git_push", {"branch": "main"}) == GateClass.IRREVERSIBLE

    def test_browser_submit_irreversible(self):
        assert gate_classify("browser_submit", {"url": "https://x.com"}) == GateClass.IRREVERSIBLE

    def test_computer_use_irreversible(self):
        assert gate_classify("computer_use", {"action": "click"}) == GateClass.IRREVERSIBLE

    def test_unknown_tool_deny(self):
        assert gate_classify("unknown_tool_xyz", {}) == GateClass.DENY

    def test_ssh_explicit_deny(self):
        assert gate_classify("ssh", {"host": "vps"}) == GateClass.DENY

    def test_modify_gate_explicit_deny(self):
        assert gate_classify("modify_gate", {}) == GateClass.DENY


# ---------------------------------------------------------------------------
# T-gate-nm: invalid tool name
# ---------------------------------------------------------------------------

class TestInvalidToolName:
    def test_empty_name_deny(self):
        assert gate_classify("", {}) == GateClass.DENY

    def test_none_name_deny(self):
        assert gate_classify(None, {}) == GateClass.DENY

    def test_int_name_deny(self):
        assert gate_classify(42, {}) == GateClass.DENY

    def test_list_name_deny(self):
        assert gate_classify(["read_file"], {}) == GateClass.DENY


# ---------------------------------------------------------------------------
# T-gate-wf-deny: write_file denylist paths
# ---------------------------------------------------------------------------

class TestWriteFileDenylist:
    def test_gas_memory_db(self):
        assert _wf(".gas_memory.db") == GateClass.DENY

    def test_gas_memory_db_dotslash(self):
        assert _wf("./.gas_memory.db") == GateClass.DENY

    def test_gas_memory_db_traversal(self):
        assert _wf("x/../.gas_memory.db") == GateClass.DENY

    def test_gas_memory_upper(self):
        assert _wf(".GAS_MEMORY.db") == GateClass.DENY

    def test_env_file(self):
        assert _wf(".env") == GateClass.DENY

    def test_env_prod(self):
        assert _wf(".env.prod") == GateClass.DENY

    def test_gas_py(self):
        # Schema a 3 livelli (1A): codice → firma, non più divieto assoluto.
        assert _wf("gas.py") == GateClass.IRREVERSIBLE

    def test_modules_gate_gate(self):
        assert _wf("modules/gate/gate.py") == GateClass.DENY

    def test_claude_agents_revisore(self):
        assert _wf(".claude/agents/revisore.md") == GateClass.DENY

    def test_absolute_path(self):
        assert _wf("/etc/passwd") == GateClass.DENY

    def test_traversal_relative(self):
        assert _wf("../fuori.txt") == GateClass.DENY

    def test_gas_history(self):
        assert _wf(".gas_history.json") == GateClass.DENY

    def test_brains_model_ids(self):
        assert _wf("brains/model_ids.py") == GateClass.IRREVERSIBLE

    def test_gate_config(self):
        assert _wf("gate_config.py") == GateClass.DENY

    def test_reports_note_uncertain(self):
        assert _wf("reports/note.md") == GateClass.UNCERTAIN


# ---------------------------------------------------------------------------
# T-gate-rf-deny: read_file denylist paths (same denylist applies)
# ---------------------------------------------------------------------------

class TestReadFileDenylist:
    def test_gas_memory_db(self):
        assert _rf(".gas_memory.db") == GateClass.DENY

    def test_gas_memory_db_dotslash(self):
        assert _rf("./.gas_memory.db") == GateClass.DENY

    def test_gas_memory_db_traversal(self):
        assert _rf("x/../.gas_memory.db") == GateClass.DENY

    def test_gas_memory_upper(self):
        assert _rf(".GAS_MEMORY.db") == GateClass.DENY

    def test_env_file(self):
        assert _rf(".env") == GateClass.DENY

    def test_env_prod(self):
        assert _rf(".env.prod") == GateClass.DENY

    def test_gas_py(self):
        # Operatore 2026-10-11: Gas legge il codice (non lo tocca senza firma).
        assert _rf("gas.py") == GateClass.SAFE

    def test_modules_gate_gate(self):
        assert _rf("modules/gate/gate.py") == GateClass.SAFE

    def test_claude_agents_revisore(self):
        assert _rf(".claude/agents/revisore.md") == GateClass.DENY

    def test_absolute_path(self):
        assert _rf("/etc/passwd") == GateClass.DENY

    def test_traversal_relative(self):
        assert _rf("../fuori.txt") == GateClass.DENY

    def test_reports_note_safe(self):
        assert _rf("reports/note.md") == GateClass.SAFE


# ---------------------------------------------------------------------------
# T-gate-ma: malformed args → DENY without exception
# ---------------------------------------------------------------------------

class TestMalformedArgs:
    def test_non_json_string_deny(self):
        # stringa non JSON
        assert gate_classify("read_file", "not json {{{") == GateClass.DENY

    def test_list_args_deny(self):
        # lista invece di dict
        assert gate_classify("read_file", ["path.txt"]) == GateClass.DENY

    def test_missing_path_key_deny(self):
        # chiave path mancante in read_file
        assert gate_classify("read_file", {"content": "x"}) == GateClass.DENY

    def test_missing_path_key_write_file(self):
        # chiave path mancante in write_file
        assert gate_classify("write_file", {"content": "x"}) == GateClass.DENY

    def test_missing_command_key_deny(self):
        # chiave 'command' mancante in run_command
        assert gate_classify("run_command", {"cmd": "ls"}) == GateClass.DENY

    def test_none_args_deny(self):
        # tipo inatteso: None
        assert gate_classify("calcola", None) == GateClass.DENY

    def test_int_args_deny(self):
        # tipo inatteso: int
        assert gate_classify("calcola", 42) == GateClass.DENY

    def test_no_exception_on_bad_args(self):
        # gate_classify must never raise
        for bad in [None, 42, [], object(), "{{{"]:
            result = gate_classify("read_file", bad)
            assert result == GateClass.DENY

    def test_json_string_accepted(self):
        # JSON string form of valid args is accepted
        import json
        args_str = json.dumps({"relative_path": "reports/note.md"})
        assert gate_classify("read_file", args_str) == GateClass.SAFE

    def test_json_string_deny_path(self):
        # JSON string with denied path is still DENY
        import json
        args_str = json.dumps({"relative_path": ".gas_memory.db"})
        assert gate_classify("read_file", args_str) == GateClass.DENY


# ---------------------------------------------------------------------------
# T-gate-rc: run_command sandbox rule + denylist
# ---------------------------------------------------------------------------

class TestRunCommand:
    def test_os_strict_returns_uncertain(self, monkeypatch):
        monkeypatch.setenv("GAS_SANDBOX_MODE", "os_strict")
        assert gate_classify("run_command", {"command": "ls reports/"}) == GateClass.UNCERTAIN

    def test_no_sandbox_env_returns_irreversible(self, monkeypatch):
        monkeypatch.delenv("GAS_SANDBOX_MODE", raising=False)
        assert gate_classify("run_command", {"command": "ls reports/"}) == GateClass.IRREVERSIBLE

    def test_os_with_fallback_returns_irreversible(self, monkeypatch):
        monkeypatch.setenv("GAS_SANDBOX_MODE", "os_with_fallback")
        assert gate_classify("run_command", {"command": "ls reports/"}) == GateClass.IRREVERSIBLE

    def test_unknown_sandbox_mode_returns_irreversible(self, monkeypatch):
        monkeypatch.setenv("GAS_SANDBOX_MODE", "unknown_mode_xyz")
        assert gate_classify("run_command", {"command": "ls reports/"}) == GateClass.IRREVERSIBLE

    def test_env_prod_arg_is_deny(self, monkeypatch):
        # '.env.prod' as a standalone token must be denied regardless of sandbox mode
        monkeypatch.setenv("GAS_SANDBOX_MODE", "os_strict")
        assert gate_classify("run_command", {"command": "cat .env.prod"}) == GateClass.DENY

    def test_env_prod_arg_deny_no_sandbox(self, monkeypatch):
        monkeypatch.delenv("GAS_SANDBOX_MODE", raising=False)
        assert gate_classify("run_command", {"command": "cat .env.prod"}) == GateClass.DENY

    def test_gas_memory_token_deny(self, monkeypatch):
        monkeypatch.setenv("GAS_SANDBOX_MODE", "os_strict")
        assert gate_classify("run_command", {"command": "ls .gas_memory.db"}) == GateClass.DENY

    def test_modules_token_lettura_consentita(self, monkeypatch):
        # Operatore 2026-10-11: lettura del codice aperta; resta la regola §8e.
        monkeypatch.delenv("GAS_SANDBOX_MODE", raising=False)
        assert gate_classify("run_command", {"command": "ls modules/"}) == GateClass.IRREVERSIBLE

    def test_env_sandbox_restored(self, monkeypatch):
        # Monkeypatch must not leak state between tests (pytest guarantees this)
        monkeypatch.setenv("GAS_SANDBOX_MODE", "os_strict")
        r = gate_classify("run_command", {"command": "wc -l reports/note.md"})
        assert r == GateClass.UNCERTAIN
        # After test, monkeypatch fixture undoes the env change automatically.

    # R-gate-2 fix: --flag=value bypass (substring check)
    def test_flag_eq_env_prod_deny(self, monkeypatch):
        monkeypatch.setenv("GAS_SANDBOX_MODE", "os_strict")
        assert gate_classify("run_command", {"command": "grep --file=.env.prod x"}) == GateClass.DENY

    def test_short_flag_env_deny(self, monkeypatch):
        monkeypatch.delenv("GAS_SANDBOX_MODE", raising=False)
        assert gate_classify("run_command", {"command": "grep -f.env x"}) == GateClass.DENY

    def test_traversal_to_env_deny(self, monkeypatch):
        monkeypatch.delenv("GAS_SANDBOX_MODE", raising=False)
        assert gate_classify("run_command", {"command": "cat reports/../.env"}) == GateClass.DENY

    def test_uppercase_gas_memory_deny(self, monkeypatch):
        monkeypatch.setenv("GAS_SANDBOX_MODE", "os_strict")
        assert gate_classify("run_command", {"command": "wc -l .GAS_MEMORY.db"}) == GateClass.DENY

    def test_dotslash_modules_lettura_consentita(self, monkeypatch):
        monkeypatch.setenv("GAS_SANDBOX_MODE", "os_strict")
        assert gate_classify("run_command", {"command": "cat ./modules/gate/gate.py"}) == GateClass.UNCERTAIN

    def test_normal_command_not_denied(self, monkeypatch):
        monkeypatch.delenv("GAS_SANDBOX_MODE", raising=False)
        assert gate_classify("run_command", {"command": "wc -l reports/note.md"}) == GateClass.IRREVERSIBLE


# ---------------------------------------------------------------------------
# T-gate-nfkc: NFKC normalization (R-gate-1 fix)
# ---------------------------------------------------------------------------

class TestNFKC:
    def test_fullwidth_gas_memory_write_deny(self):
        # U+FF0E = FULLWIDTH FULL STOP — NFKC reduces it to ASCII '.'
        # "．" + "gas_memory．db" → ".gas_memory.db" after NFKC
        fullwidth_path = "．gas_memory．db"  # ．gas_memory．db
        assert _wf(fullwidth_path) == GateClass.DENY

    def test_fullwidth_dot_env_write_deny(self):
        fullwidth_path = "．env"  # ．env
        assert _wf(fullwidth_path) == GateClass.DENY

    def test_fullwidth_gas_memory_read_deny(self):
        fullwidth_path = "．gas_memory．db"
        assert _rf(fullwidth_path) == GateClass.DENY


# ---------------------------------------------------------------------------
# Verifica-bot PR #160 (V-1) + R-220-4: catena di avvio fuori dalla sandbox
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("path", [
    "venv/bin/activate", "venv/bin/python3", ".venv/bin/activate",
    "venv/lib/python3.13/site-packages/x.pth",
    ".git/config", ".git/hooks/pre-commit", ".github/workflows/ci.yml",
    ".gas_notte/ultimo_giro.md", ".gas_notte/launchd.log", "./.gas_notte/lock",
    "VENV/bin/activate", "sub/../venv/bin/activate",
])
def test_write_catena_di_avvio_deny(path):
    assert _wf(path) == GateClass.DENY


@pytest.mark.parametrize("path", [
    "yaml.py", "openai.py", "openai/__init__.py", "dati/x.PY", "x.pyc", "x.pyw",
    "evil.pth", "lib.so", "lib.dylib", "x.py/", "x.py.",
])
def test_write_file_di_codice_firma(path):
    assert _wf(path) == GateClass.IRREVERSIBLE


@pytest.mark.parametrize("path", ["note.md", "dati/lead.csv", "copy.txt", "py.txt", "x.pyx.md"])
def test_write_file_non_codice_resta_uncertain(path):
    assert _wf(path) == GateClass.UNCERTAIN


def test_read_file_py_resta_consentita():
    assert gate_classify("read_file", {"relative_path": "README.py"}) == GateClass.SAFE


def test_read_file_venv_e_gas_notte_deny():
    assert gate_classify("read_file", {"relative_path": "venv/bin/activate"}) == GateClass.DENY
    assert gate_classify("read_file", {"relative_path": ".gas_notte/ultimo_giro.md"}) == GateClass.DENY


@pytest.mark.parametrize("path", [
    "scripts/gasmerge.sh", "scripts/hash_diff_staged.sh", "x.sh", "dati/y.ZSH", "a.bash",
    "b.command", "scripts/nuovo.txt", "CLAUDE.md", "./claude.md", ".mcp.json",
    "gas_identity.md", "requirements.txt", "requirements-dev.txt",
])
def test_write_file_eseguiti_fuori_sandbox_firma(path):
    """R-222-1: script e file letti/eseguiti con privilegi fuori dalla sandbox
    (schema 1A: livello 2, firma con diff reale)."""
    assert _wf(path) == GateClass.IRREVERSIBLE


@pytest.mark.parametrize("path", ["note/requirements_cliente.txt", "dati/claude.md.txt", "shell.txt"])
def test_write_prefissi_solo_primo_livello(path):
    assert _wf(path) == GateClass.UNCERTAIN


@pytest.mark.parametrize("path", [
    "CLAUDE.local.md", "claude.local.md", "tests/CLAUDE.md", "dati/claude.md",
    "reports/CLAUDE.local.md", "dati/sotto/AGENTS.md", "AGENTS.md",
    "AGENTS.override.md", "dati/agents.override.md",
    "\uff23\uff2c\uff21\uff35\uff24\uff25.md",          # CLAUDE.md fullwidth (NFKC)
    "dati/\uff23\uff2c\uff21\uff35\uff24\uff25.local.md",
])
def test_write_istruzioni_agenti_a_ogni_livello_firma(path):
    """Verifica-bot #160 V-1: file d'istruzioni degli agenti a qualunque profondità."""
    assert _wf(path) == GateClass.IRREVERSIBLE


@pytest.mark.parametrize("path", [
    "pytest.ini", "tests/pytest.ini", "pyproject.toml", "dati/pyproject.toml",
    "setup.cfg", "tox.ini", "Makefile", "makefile", "dati/GNUmakefile",
    "GEMINI.md", "dati/gemini.md", ".cursorrules", "dati/.cursorrules",
    "tests/.pytest.ini", "tests/pytest.toml", ".pytest.toml",  # R-247-1
    ".vscode/tasks.json", "dati/.vscode/settings.json", ".cursor/rules/x.mdc",
    ".gemini/settings.json", ".idea/workspace.xml", ".devcontainer/devcontainer.json",
    ".pre-commit-config.yaml", ".coveragerc", "mypy.ini", "tests/.mypy.ini", ".flake8",
    "uv.toml", "tests/pytest.cfg", "justfile", "Dockerfile", ".python-version",
    "package.json",  # R-247-2, V-1 verifica esterna #174
    ".devcontainer.json", "dati/.devcontainer.json", "gas.code-workspace",
    "dati/x.CODE-WORKSPACE",  # R-249-1
    "pytest.ini.", "Makefile.", "tests/pyproject.toml ", ".vscode./tasks.json",
    "dati/.vscode /x", "Dockerfile.",  # V-1 bot #174: punti/spazi finali per pezzo
    ".pdbrc", "tests/.pylintrc", "pylintrc", ".husky/pre-commit",  # .npmrc: ora segreto (livello 3)
    ".windsurf/rules/x", ".zed/settings.json",  # V-2 bot #175, verifica esterna #175
    "\uff30\uff59\uff50\uff52\uff4f\uff4a\uff45\uff43\uff54.toml",  # pyproject fullwidth (NFKC)
])
def test_write_config_strumenti_sviluppo_firma(path):
    """Riserva aperta FASE 4.5: file di configurazione degli strumenti di sviluppo
    (pytest, build, make, istruzioni Gemini/Cursor) a qualunque profondità."""
    assert _wf(path) == GateClass.IRREVERSIBLE


@pytest.mark.parametrize("path", [
    "dati/pyproject.toml.txt", "note/makefile_appunti.md", "setup.cfg.bak", "gemini.txt",
    "dati/vscode_note.md", "dati/dockerfile_esempio.txt", "package.json.bak",
])
def test_write_config_strumenti_nomi_simili_restano_uncertain(path):
    assert _wf(path) == GateClass.UNCERTAIN


def test_read_config_strumenti_resta_consentita():
    assert gate_classify("read_file", {"relative_path": "pyproject.toml"}) == GateClass.SAFE


def test_read_claude_md_resta_consentita():
    assert gate_classify("read_file", {"relative_path": "CLAUDE.md"}) == GateClass.SAFE


# ---------------------------------------------------------------------------
# Schema a 3 livelli di write_file (decisione operatore 1A, 2026-10-11)
# ---------------------------------------------------------------------------
from modules.gate.gate import livello_scrittura, LIVELLO_LIBERO, LIVELLO_FIRMA, LIVELLO_MAI


@pytest.mark.parametrize("path", [
    ".env", ".env.prod", "dati/.env", ".envrc", ".git/config", ".github/workflows/ci.yml",
    ".gitignore", ".claude/settings.json", "dati/.claude/x", ".gas_memory.db",
    ".gas_history.json", ".gas_notte/ultimo_giro.md", ".gas_knowledge.db",
    ".gas_vectors.db", ".gas_tokens.jsonl", "gate_config.yaml", "venv/bin/activate",
    ".venv/lib/x.pth",
    "modules/gate/gate.py", "modules/gate/__init__.py", "modules/gate/nuovo.md",
    "modules/gate", "Modules/GATE/gate.py", "modules/./gate/gate.py",
    "modules/x/../gate/gate.py", "modules/gate./gate.py", "modules/gate /gate.py",
    "modules/gate.py", "modules/gate_bis/x.py",
    "\uff4d\uff4f\uff44\uff55\uff4c\uff45\uff53/gate/gate.py",  # fullwidth (NFKC)
    "./.env", "\uff0eenv", "x/../.git/hooks/pre-commit",
    # V-1 verifica esterna #233 (3° giro): invisibili dentro i nomi vietati
    ".e\u200bnv", "modules/ga\u200bte/gate.py", ".gas_\u200bnotte/x", "\u200b.git/config",
])
def test_livello3_mai_nemmeno_con_firma(path):
    assert livello_scrittura(path) == LIVELLO_MAI
    assert _wf(path) == GateClass.DENY


@pytest.mark.parametrize("path", [
    "gas.py", "brains/router.py", "modules/memory/store.py", "modules/notte/notte.py",
    "modules/telegram/bot.py", "modules/nuovo/x.md", "dati/x.py", "scripts/gasmerge.sh",
    "scripts/notte/catalogo_esempio.yaml", "CLAUDE.md", "dati/claude.md", "gas_identity.md",
    "requirements.txt", "requirements-dev.txt", "pytest.ini", ".vscode/tasks.json",
    "tests/test_x.py", "dati/brainstorming.md",  # prefisso "brains": prudente
    # roadmap 5.3: catalogo delle fonti di studio e file delle fonti alla firma
    "knowledge/sources.yaml", "knowledge/x.md", "Knowledge/Sources.YAML",
    "knowledge./sources.yaml", "knowledge_old/sources.yaml", "./knowledge/test_source.txt",
    # V-1 verifica esterna #233 (3° giro): caratteri invisibili (Cf) non aggirano la firma
    "run.sh\u200b", "run.s\u200bh", "run.py\u200b", "x\ufeff.zsh", "g\u200bas.py",
    "scripts\u200b/x.md",
])
def test_livello2_firma(path):
    assert livello_scrittura(path) == LIVELLO_FIRMA
    assert _wf(path) == GateClass.IRREVERSIBLE


@pytest.mark.parametrize("path", [
    "note.md", "reports/nota.md", "dati/lead.csv", "dati/knowledge.md", "dati/gate/x.md",
    "x/modules_note.txt.bak/../note.md",
])
def test_livello1_libero(path):
    assert livello_scrittura(path) == LIVELLO_LIBERO
    assert _wf(path) == GateClass.UNCERTAIN


@pytest.mark.parametrize("path", [None, 3, "", "  ", "/etc/passwd", "../fuori", "..", "."])
def test_livello_percorsi_invalidi_fail_closed(path):
    assert livello_scrittura(path) == LIVELLO_MAI


def test_livello_mai_eccezioni(monkeypatch):
    import modules.gate.gate as g
    monkeypatch.setattr(g, "_normalize_path", lambda p: (_ for _ in ()).throw(RuntimeError()))
    assert livello_scrittura("note.md") == LIVELLO_MAI


def test_lettura_del_codice_aperta_il_livello_3_resta_illeggibile(monkeypatch):
    """Operatore 2026-10-11: Gas legge gas.py, brains/, modules/ (scrittura solo con
    firma). I file «mai» restano illeggibili, con read_file e con run_command."""
    from modules.gate.gate import lettura_consentita
    for p in ("gas.py", "brains/router.py", "modules/memory/store.py",
              "modules/gate/gate.py", "Modules/GATE/gate.py", "note.md"):
        assert gate_classify("read_file", {"relative_path": p}) == GateClass.SAFE, p
        assert lettura_consentita(p), p
    for p in (".env", ".env.prod", ".git/config", ".github/workflows/ci.yml",
              ".claude/settings.json", ".gas_memory.db", ".gas_history.json",
              ".gas_notte/ultimo_giro.md", "venv/bin/activate", "dati/.env",
              "\uff0eenv", "/etc/passwd", "../x", None):
        assert gate_classify("read_file", {"relative_path": p}) == GateClass.DENY, p
        assert not lettura_consentita(p), p
    assert not lettura_consentita("") and not lettura_consentita("  ")
    monkeypatch.setenv("GAS_SANDBOX_MODE", "os_strict")
    assert gate_classify("run_command", {"command": "head -n 50 gas.py"}) == GateClass.UNCERTAIN
    assert gate_classify("run_command", {"command": "grep -n def brains/router.py"}) == GateClass.UNCERTAIN
    for c in ("cat .env", "grep x .git/config", "cat .claude/settings.json",
              "head .gas_memory.db", "grep --file=.env x note.md"):
        assert gate_classify("run_command", {"command": c}) == GateClass.DENY, c


def test_r263_1_read_back_rende_visibili_spazi_e_selettori():
    """R-263-1: NBSP, selettori di variante e riempitivi Hangul non restano invisibili
    nel messaggio di firma; spazio normale, lettere accentate ed emoji restano."""
    from modules.telegram.bot import rendi_visibili
    assert rendi_visibili("a\xa0b️c\U000e0100dㅤe") == \
        "a<U+00A0>b<U+FE0F>c<U+E0100>d<U+3164>e"
    assert rendi_visibili("città ok 🙂\tx\n") == "città ok 🙂\tx\n"
    assert rendi_visibili("a\u034fb\u2800c") == "a<U+034F>b<U+2800>c"  # R-264-2
    assert rendi_visibili("\u17b4\u17b5\u0338\ufffc") == \
        "<U+17B4><U+17B5><U+0338><U+FFFC>"  # V-2 verifica esterna #180


@pytest.mark.parametrize("path", ["modules/prod.env", "brains/x.ENV", "dati/chiavi.env",
                                  "modules/prod.env.", "prod.env", "modules/prod.env.local",
                                  "modules/prod.env.bak", "modules/prod.env~",
                                  "modules/prod.env_old", "modules/prod.env-vecchio",
                                  "modules/prod.env copy", "modules/prod.env(1)",
                                  "modules/prod.env1", "modules/prod.env#", "modules/prod.env,bak",
                                  "modules/PROD.ENV COPY", "modules/prod.envbak",
                                  "modules/prod.envold", "modules/prod.envcopy"])
def test_v2_181_file_che_finiscono_in_env_illeggibili(path):
    """V-2 verifica esterna #181: anche dentro cartelle leggibili."""
    from modules.gate.gate import lettura_consentita
    assert gate_classify("read_file", {"relative_path": path}) == GateClass.DENY
    assert not lettura_consentita(path)


@pytest.mark.parametrize("path", ["modules/envoy.py", "dati/env.txt", "brains/router.py",
                                  "modules/x.environment.py", "dati/a.envelope.md"])
def test_v2_181_nomi_simili_restano_leggibili(path):
    assert gate_classify("read_file", {"relative_path": path}) == GateClass.SAFE


@pytest.mark.parametrize("path", ["id_rsa", "dati/id_ed25519", "dati/id_ecdsa.pub", "id_rsa.", "id_rsa_vecchia",
                                  ".ssh/config", "dati/.ssh/authorized_keys", "chiavi/server.pem",
                                  "dati/X.KEY", "a.p12", "b.pfx", "c.ppk", "d.jks", "e.keystore",
                                  "f.kdbx", "x.pem~", "x.key.bak", "server.pem.old", "y.pfx1", "secrets.yaml",
                                  # varianti (bot e verifica esterna #188)
                                  ".netrc~", ".netrc.bak", ".pgpass.old", ".htpasswd.bak",
                                  ".pypirc~", "secrets~", "backup_id_rsa", "old.id_ed25519",
                                  "credentials_prod.json", "secrets_prod.yaml", ".kube/config",
                                  ".docker/config.json", "service-account.json", "token.json",
                                  "my_credentials.json", "wallet.dat", ".npmrc",
                                  "credentials_guide.md", "dati/secret_sauce.md", "dati/secret.json", "dati/secrets",
                                  "config/credentials.json", ".aws/credentials", ".netrc",
                                  ".pgpass", ".pypirc", ".htpasswd", ".gnupg/pubring.kbx",
                                  # D1: i nove buchi di R-291-1 / bot #188, più varianti
                                  "token_cache.json", "dati/tokens-prod.yaml", "kubeconfig",
                                  "dati/kubeconfig.yaml", "mywallet.dat", "backup-wallet.dat",
                                  ".vault-token", ".dockercfg", "_netrc", "_netrc.bak",
                                  "clientsecret.json", "dati/client_secrets.json",
                                  "chiave.gpg", "dati/pubkey.asc", "x.asc.bak",
                                  # R-324-1/3: token.pickle (OAuth Google), cache MSAL, .pgp,
                                  # pezzo di percorso oltre 255 caratteri
                                  "token.pickle", "msal_token_cache.bin", "token_cache.db",
                                  "chiave.pgp", "token_" * 50 + "x",
                                  # D2 (secondo passaggio claude.ai #198): chiavi API e token
                                  "api_key", "apikey", "api-keys.json", "api_token", "my_api_key.txt",
                                  "access_token", "refresh_token", "gh_token", "github_token",
                                  "hf_token", "openai_key", "openai-api-key", "anthropic_key.txt",
                                  "anthropic-key", "gemini_key", "groq_token", "groq_api_key.txt",
                                  "keys.txt", "key.json", "keys.yaml", "key.yml", "dati/key.txt",
                                  "prod_key.txt", "my_keys.json", "service_keys.yml",
                                  "token", "tokens", "key", "keys", "token~", "key.bak",
                                  ".azure", ".azure/accessTokens.json", "accesstokens.json",
                                  "mykubeconfig", "kubeconfigs",
                                  "password", "passwords", "passwords.txt", "password.md",
                                  "my_passwords.csv", "passwords.txt.bak", "passwd", "shadow",
                                  "passwd-", "shadow.bak",
                                  "cookies.json", "cookie.txt", "cookies.sqlite",
                                  "cookies.sqlite-journal", "storage_state.json", "auth_state.json",
                                  "oauth.json", "oauth2.json", ".auth", ".auth/user.json",
                                  "sessions.json", "session.json", "user_session.json",
                                  "gas.session", "anon.session-journal",
                                  "wallet.json", "wallet.txt", "mywallet.json", "keystore.json",
                                  "seed.txt", "mnemonic.txt", "seed_phrase", "seedphrase.txt",
                                  "recovery-phrase.txt", "recovery_phrase",
                                  "private_key", "private_keys", "privkey", "ssh_key", "ssh-key.txt",
                                  "sshkey", "deploy_key", "deploy-key", "deploy_keys", "id-rsa",
                                  "id-ed25519", "rsa_key", "ssh_host_rsa_key", "AuthKey_ABC.p8",
                                  # D2 BASSA: config con credenziali, stato Terraform, VPN
                                  ".terraformrc", "terraform.tfstate", "terraform.tfstate.backup",
                                  "prod.tfvars", ".boto", ".s3cfg", ".my.cnf", ".yarnrc",
                                  ".yarnrc.yml", ".sentryclirc", "client.ovpn", "wg0.conf",
                                  # R-329-1: nomi scritti da persone, con lo spazio
                                  "Seed Phrase.txt", "recovery phrase.txt", "ssh key", "deploy key",
                                  "access token", "api token", "private key", "gh token",
                                  # D3: altri fornitori senza estensione, separatore ripetuto,
                                  # copie e liste di password, cartella della CLI GitHub
                                  "bot_token", "auth_token", "telegram_token", "slack_token",
                                  "mistral_key", "cohere_key", "oauth_token", "api  key", "api__key",
                                  "seed  phrase", "mnemonic.json", "passwords_backup.txt",
                                  "password_list.txt", "password-prod.csv", "passwords copy.txt",
                                  "password (1).txt", "password_2024.txt", ".config/gh/hosts.yml",
                                  ".config/gh", "dati/keys", "x/shadow-",
                                  "telegram.token", "bot.token", "slack.token", "gh.token",
                                  # bot #202: fornitori usati da Gas, file dentro keys/ e
                                  # tokens/, .config/gh con punti o spazi finali
                                  "openrouter_key", "elevenlabs_key", "voice_token", "claude_key",
                                  "discord_token", "gitlab_token", "npm_token", "pypi_token",
                                  "huggingface_token", "keys/openai", "tokens/github",
                                  "keys/prod.txt", "x/keys/groq.json", "keys/prod.toml", "tokens/a.conf", ".config./gh/hosts.yml",
                                  ".config/gh /hosts.yml", "keys.bak/openai", "keys.old/prod.txt",
                                  "keys~/github", "tokens-/a.conf", "daily_token", "keys/setup.py",
                                  "keys/telegram.py", ".config/gh.bak/hosts.yml",
                                  ".config/gh~/hosts.yml", ".config/gh.old/hosts.yml",
                                  # D5 (secondo passaggio claude.ai su #204, MEDIA): copie con
                                  # altri nomi (Finder «keys copy», «keys (1)», backup, _old…)
                                  "keys copy/openai.txt", "keys (1)/a.txt", "keys.backup/a",
                                  "keys_old/a.json", "old_keys/a", "keys2/a", "tokens copy/x",
                                  "keys.orig/a", "keys copy 2/a", "keys.bak.bak/a",
                                  "Keys Copy/x.yml", ".config/gh copy/hosts.yml",
                                  ".config/gh.orig/hosts.yml", "keys copy", "shadow copy",
                                  "passwd.old", "tokens (2)",
                                  # bot #210 V-1: prefissi new/orig, cifre dopo la parola di copia
                                  "new_keys/a", "orig_keys/a", "keys.bak1/a", "keys_old2/a",
                                  "keys copy2/a", "keys_v2/a", "keys.prev/a", "keys.save/a",
                                  # R-bot210-3: prefisso col punto
                                  "old.keys/a", "backup.keys/a", "copy.tokens/x",
                                  # V-1 verifica esterna #217: prefissi ripetuti, punto iniziale
                                  "old.old.keys/a", "old_old_keys/a", "copy_old.keys/a",
                                  ".old.keys/a", ".keys/a", ".tokens/x", "..keys/a", "._keys/a",
                                  # V-1 verifica esterna #217 su fdf001c: copie di .config
                                  "old.config/gh/hosts.yml", "home/old.config/gh/hosts.yml",
                                  "x/.old.config/gh/hosts.yml", ".config.bak/gh/hosts.yml",
                                  ".config copy/gh.old/hosts.yml"])
def test_chiavi_private_e_credenziali_illeggibili_e_mai_scritte(path):
    """Decisione operatore 2026-10-11: chiavi e credenziali vietate (lettura e scrittura)."""
    from modules.gate.gate import lettura_consentita, livello_scrittura, LIVELLO_MAI
    assert gate_classify("read_file", {"relative_path": path}) == GateClass.DENY
    assert not lettura_consentita(path)
    assert livello_scrittura(path) == LIVELLO_MAI


@pytest.mark.parametrize("path", ["secretary.md", "dati/keys.md", "note/keyboard.txt",
                                  "sshconfig.md", "dati/pemberton.txt", "dati/rsa_id.md",
                                  "dati/x.keyboard", "dati/a.keys.md", "dati/b.pemmican",
                                  "dati/valid_rsa.md", "tokenizer.py", "dati/tokens.md", "kubectl.md",
                                  # D1: nomi simili ai nuovi divieti restano leggibili
                                  "tokenizer.json", "dati/ascii.txt", "dati/x.ascx.md",
                                  "dati/gpgme.md", "wallets.md", "netrc_guida.md",
                                  # D2: falsi positivi da evitare
                                  "keyboard.md", "keynote.md", "monkey.py", "passwordless.md",
                                  "session_notes.md", "seed_data.csv", "auth_flow.md",
                                  "dati/tokenizer.model", ".azure-pipelines/ci.yml",
                                  "dati/sessions.md", "dati/password_reset.md", "a private keynote.md",
                                  # D3: il nome intero vale solo per l'ultimo pezzo (R-bot201-3)
                                  "keys/readme.md", "shadow/readme.md", "tokens/note.md",
                                  "author_key.md", ".config/ghostty/config", ".config/gh_notes.md",
                                  "password_policy.md", "robot.token.md", "gh.keyboard.md",
                                  "voiceover.md", "claudette.md", "keys/notes.rst",
                                  "dailytokenizer.md", "keys.bak/readme.md",
                                  # R-bot210-3: il prefisso col punto non crea falsi positivi
                                  "old.keyboard.md", "dati/old.keys.md", "new.tokenizer.json",
                                  ".keyboard.md", "old.old.keynote.md", ".tokenizer.json",
                                  # #362 COSMETICA: separatori iniziali senza nome protetto
                                  "_keyboard.md", "..keynote.md", "._readme.md",
                                  # «config» nudo non è la cartella della CLI GitHub
                                  "config/gh/readme.md", ".configs/gh/x.md"])
def test_nomi_simili_a_chiavi_restano_leggibili(path):
    from modules.gate.gate import lettura_consentita
    assert gate_classify("read_file", {"relative_path": path}) == GateClass.SAFE
    assert lettura_consentita(path)


@pytest.mark.parametrize("path", ["keys copy/readme.md", "shadow_old/a.md", "passwd (1)/x.md",
                                  "old_keys/readme.md", "old.keys/readme.md",
                                  "keys/readme.md", "keys/notes.rst", "tokens/note.md",
                                  "passwd/x.txt", "shadow/readme.md", "keys.bak/readme.md",
                                  "a/shadow-/b.md", "x/Keys/y.md"])
def test_cartelle_di_chiavi_leggibili_ma_mai_scritte(path):
    """R-bot202-2: dentro keys/, tokens/, passwd/, shadow/ la documentazione si legge
    ma non si scrive mai (come su main prima di D3)."""
    from modules.gate.gate import lettura_consentita, livello_scrittura, LIVELLO_MAI
    assert lettura_consentita(path)
    assert livello_scrittura(path) == LIVELLO_MAI


@pytest.mark.parametrize("path", ["keys.d/x.md", "oldkeys/x.md", "keynote copy.md",
                                  "dati/keys_list.md", "old.keyboard/x.md",
                                  "keyboard/x.md", "monkeys/x.md", "dati/tokens.md",
                                  "shadowing/x.md", "note/keys.md"])
def test_cartelle_simili_a_chiavi_restano_scrivibili(path):
    from modules.gate.gate import livello_scrittura, LIVELLO_LIBERO
    assert livello_scrittura(path) == LIVELLO_LIBERO


@pytest.mark.parametrize("tool, args, atteso", [
    # decisione operatore 2026-10-19: rubrica e livello 1 liberi dopo una lettura
    ("salva_contatto", {"chiave": "a@b.it"}, True),
    ("imposta_stato_contatto", {"chiave": "a@b.it", "stato": "x"}, True),
    ("write_file", {"relative_path": "dati/a.md", "content": "x"}, True),
    ("write_file", '{"relative_path": "dati/note.txt", "content": "x"}', True),
    # restano alla firma: sicurezza del processo, codice, segreti, esterno, args rotti
    ("write_file", {"relative_path": "reports/a.md"}, False),
    ("write_file", {"relative_path": "./Reports/a.md"}, False),
    ("write_file", {"relative_path": "reports_old/a.md"}, False),
    ("write_file", {"relative_path": "reports./a.md"}, False),
    ("write_file", {"relative_path": "knowledge/sources.yaml"}, False),
    ("write_file", {"relative_path": "KNOWLEDGE.bak/x"}, False),
    ("write_file", {"relative_path": "gas.py"}, False),
    ("write_file", {"relative_path": "scripts/a.sh"}, False),
    ("write_file", {"relative_path": ".env"}, False),
    ("write_file", {"relative_path": "../fuori.md"}, False),
    ("write_file", {"content": "senza percorso"}, False),
    ("write_file", "non json", False),
    # V-1 verifica esterna #222: solo documenti (md/txt/csv) liberi dopo una lettura
    ("write_file", {"relative_path": "dati/a.csv"}, True),
    ("write_file", {"relative_path": "dati/a.TXT"}, True),
    ("write_file", {"relative_path": "dati/a.js"}, False),
    ("write_file", {"relative_path": "a.mjs"}, False),
    ("write_file", {"relative_path": "a.ts"}, False),
    ("write_file", {"relative_path": "a.rb"}, False),
    ("write_file", {"relative_path": "a.pl"}, False),
    ("write_file", {"relative_path": "a.ps1"}, False),
    ("write_file", {"relative_path": "a.bat"}, False),
    ("write_file", {"relative_path": "clients/voice/browser_client.html"}, False),
    ("write_file", {"relative_path": "gas.service"}, False),
    ("write_file", {"relative_path": "Library/LaunchAgents/x.plist"}, False),
    ("write_file", {"relative_path": "dati/.bashrc"}, False),
    ("write_file", {"relative_path": ".zshrc"}, False),
    ("write_file", {"relative_path": ".profile"}, False),
    ("write_file", {"relative_path": "dati/authorized_keys"}, False),
    ("write_file", {"relative_path": "dati/a.yml"}, False),
    ("write_file", {"relative_path": "dati/a.toml"}, False),
    ("write_file", {"relative_path": "dati/a.json"}, False),
    ("write_file", {"relative_path": "dati/.nascosto/a.md"}, False),
    ("write_file", {"relative_path": "dati/a.md.sh"}, False),
    ("write_file", {"relative_path": "dati/a"}, False),
    # R-ve222-4: file letti dagli agenti di sviluppo, revisore e bot alla firma
    ("write_file", {"relative_path": "note.txt"}, False),
    ("write_file", {"relative_path": "README.md"}, False),
    ("write_file", {"relative_path": "./Readme.MD"}, False),
    ("write_file", {"relative_path": "tests/x.md"}, False),
    ("write_file", {"relative_path": "Tests./x.md"}, False),
    ("write_file", {"relative_path": "tools/a.txt"}, False),
    ("write_file", {"relative_path": "docs/a.md"}, False),
    ("write_file", {"relative_path": "clients/a.md"}, False),
    ("write_file", {"relative_path": "modules/a.md"}, False),
    ("write_file", {"relative_path": "dati/README.md"}, False),
    ("write_file", {"relative_path": "dati/readme.txt"}, False),
    ("write_file", {"relative_path": "dati/AGENTS.md"}, False),
    ("write_file", {"relative_path": "dati/SKILL.md"}, False),
    ("write_file", {"relative_path": "dati/copilot-instructions.md"}, False),
    ("write_file", {"relative_path": "dati/requirements.txt"}, False),
    ("write_file", {"relative_path": "dati/requirements-dev.txt"}, False),
    ("write_file", {"relative_path": "dati/Contributing.md"}, False),
    ("write_file", {"relative_path": "dati/AGENT.md"}, False),
    ("write_file", {"relative_path": "dati/CONVENTIONS.md"}, False),
    ("write_file", {"relative_path": "dati/clienti/elenco.md"}, True),
    ("write_file", {"relative_path": "memoria/appunti.md"}, True),
    ("write_file", {"relative_path": "dati/agenda.md"}, True),
    # R-398-1: nome grezzo con un carattere invisibile → firma
    ("write_file", {"relative_path": "notes/a.m\u200bd"}, False),
    ("write_file", {"relative_path": "notes/a.t\u200bxt"}, False),
    ("write_file", {"relative_path": "notes\ufeff/a.md"}, False),
    # R-399-1: varianti che NFKC unifica (larghezza piena) → firma
    ("write_file", {"relative_path": "notes/a.\uff4dd"}, False),
    ("write_file", {"relative_path": "notes/a.\uff54xt"}, False),
    ("write_file", {"relative_path": "notes/caff\u00e8.md"}, True),  # accento NFC: resta libero
    ("send_email", {"to": "a@b.it"}, False),
    ("run_command", {"command": "ls"}, False),
    ("browser_scrape", {"url": "x"}, False),
    (None, None, False),
])
def test_libero_dopo_lettura(tool, args, atteso):
    from modules.gate.gate import libero_dopo_lettura
    assert libero_dopo_lettura(tool, args) is atteso


@pytest.mark.parametrize("path, atteso", [
    ("dati/a.md", False), ("dati/note.txt", False), ("lead.csv", False), ("dati/agenda.md", False),
    ("dati/x.json", True), ("dati/X.YAML", True), ("dati/run.html", True), ("dati/a.js", True),
    ("dati/api_key.txt", True), ("dati/Password.md", True), ("dati/config.md", True),
    ("dati/.npmrc", True), ("dati/Makefile", True), ("dati/report", True), ("dati/a.pem", True),
    ("dati/x.json.", True), (None, True), ("", True),
    # R-386-2: parole intere, niente falsi allarmi sui documenti
    ("dati/cronologia.md", False), ("dati/sessione_marketing.md", False),
    ("dati/credito_clienti.csv", False), ("dati/monkey.md", False),
    ("dati/my-secret.md", True), ("dati/aws keys.txt", True),
    # R-387-1 / V-1 verifica esterna #230
    ("dati/x.secret.md", True), ("dati/id_rsa.txt", True), ("dati/accesstoken.md", True),
    ("dati/a.sh.txt", True), ("dati/x.py.md", True), ("dati/q.sql", True),
    ("dati/b.sqlite", True), ("dati/a.terminal", True), ("dati/w.workflow", True),
    ("dati/c.fish", True), ("dati/l.webloc", True), ("dati/m.go", True),
    ("dati/report.2026.md", False), ("dati/v1.2.txt", False), ("dati/note.finali.md", False),
    # R-388-1, V-1/V-2/V-5 verifica esterna e bot #231
    ("dati/github.token", True), ("dati/aws.credentials", True), ("dati/a.secret", True),
    ("dati/a.sh .txt", True), ("dati/verbale.c.rossi.md", False),
    ("dati/f.lli.r.bianchi.txt", False), ("dati/ordine.url.pdf", False),
    ("dati/notes.app.docx", False), ("dati/piano.c.md", False),
    # R-390-1 e verifica esterna #232
    ("dati/server.pem.txt", True), ("dati/dump.sql.txt", True), ("dati/a.p12.md", True),
    ("dati/vault.kdbx.txt", True), ("dati/prod.env.txt", True), ("dati/n.ipynb.txt", True),
    ("dati/customer.service.md", False), ("dati/manuale.html.pdf", False),
    ("dati/node.js.md", False), ("dati/b.ts.txt", False),
    ("dati/a.plist.txt", True), ("dati/a.desktop.txt", True),  # V-3 verifica esterna #233
    ("dati/a.sh\u200b.txt", True), ("dati/x.json\u200b", True), ("dati/a\ufeff.secret", True),
])
def test_sembra_delicato(path, atteso):
    """R-223-2: avviso solo informativo per i file nuovi che sembrano delicati."""
    from modules.gate.gate import sembra_delicato
    assert sembra_delicato(path) is atteso
