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
        assert _wf("gas.py") == GateClass.DENY

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
        assert _wf("brains/model_ids.py") == GateClass.DENY

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
        assert _rf("gas.py") == GateClass.DENY

    def test_modules_gate_gate(self):
        assert _rf("modules/gate/gate.py") == GateClass.DENY

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

    def test_modules_token_deny(self, monkeypatch):
        monkeypatch.delenv("GAS_SANDBOX_MODE", raising=False)
        assert gate_classify("run_command", {"command": "ls modules/"}) == GateClass.DENY

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

    def test_dotslash_modules_deny(self, monkeypatch):
        monkeypatch.delenv("GAS_SANDBOX_MODE", raising=False)
        assert gate_classify("run_command", {"command": "cat ./modules/gate/gate.py"}) == GateClass.DENY

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
def test_write_file_di_codice_deny(path):
    assert _wf(path) == GateClass.DENY


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
def test_write_file_eseguiti_fuori_sandbox_deny(path):
    """R-222-1: script e file letti/eseguiti con privilegi fuori dalla sandbox."""
    assert _wf(path) == GateClass.DENY


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
def test_write_istruzioni_agenti_a_ogni_livello_deny(path):
    """Verifica-bot #160 V-1: file d'istruzioni degli agenti a qualunque profondità."""
    assert _wf(path) == GateClass.DENY


def test_read_claude_md_resta_consentita():
    assert gate_classify("read_file", {"relative_path": "CLAUDE.md"}) == GateClass.SAFE
