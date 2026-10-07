"""Gate module: deterministic classifier for GAS tool calls.

C1 scaffolding — zero integration with gas.py (this module is not imported
by any engine file in this fetta).  Only stdlib is used: json, os, shlex,
unicodedata, pathlib.

Design reference: reports/design_cancello.md §2, §5, §6 "Fetta C1", §8e.

Key invariants:
- Never raises: all exceptions caught internally → DENY (fail-closed).
- default-STOP: any tool not in GATE_ALLOWLIST → DENY.
- GATE_ALLOWLIST is hardcoded; no YAML, no env override.
- Path normalization: unicodedata NFKC + os.path.normpath + casefold.
  Absolute paths and paths starting with ".." → DENY.
  NFKC (not NFC) required: FULLWIDTH characters (U+FF0E ．, U+FF0F ／) are
  not reduced to ASCII equivalents by NFC but are by NFKC.
- Path denylist: any path whose normalized form (or any component) starts
  with a denied prefix → DENY for both read_file and write_file.
  Same check for each token of run_command args (conservative).
- run_command sandbox rule (§8e): UNCERTAIN only when
  GAS_SANDBOX_MODE == "os_strict"; IRREVERSIBLE otherwise.
"""

from __future__ import annotations

import json
import os
import shlex
import unicodedata
from enum import Enum
from pathlib import PurePosixPath
from typing import Any


class GateClass(Enum):
    SAFE         = "reversibile-sicuro"
    UNCERTAIN    = "reversibile-incerto"
    IRREVERSIBLE = "irreversibile"
    DENY         = "denylist"


# Allowlist: tool_name → GateClass.
# Any tool NOT listed here → DENY (default-STOP rule).
# run_command entry is overridden by §8e logic inside gate_classify.
GATE_ALLOWLIST: dict[str, GateClass] = {
    "read_file":              GateClass.SAFE,
    "calcola":                GateClass.SAFE,
    "ricorda":                GateClass.SAFE,
    "notify_telegram":        GateClass.SAFE,
    "write_file":             GateClass.UNCERTAIN,
    "salva_contatto":         GateClass.UNCERTAIN,
    "imposta_stato_contatto": GateClass.UNCERTAIN,
    "run_command":            GateClass.UNCERTAIN,   # see §8e override below
    "browser_scrape":         GateClass.UNCERTAIN,
    "send_email":             GateClass.IRREVERSIBLE,
    "send_dm":                GateClass.IRREVERSIBLE,
    "git_push":               GateClass.IRREVERSIBLE,
    "browser_submit":         GateClass.IRREVERSIBLE,
    "computer_use":           GateClass.IRREVERSIBLE,
}

# Explicitly denied tools (belt-and-suspenders on top of "not in allowlist").
GATE_DENY_TOOLS: frozenset[str] = frozenset({"ssh", "modify_gate", "write_env"})

# Tools whose output is untrusted external input (§3b): seeing any of their
# results in the conversation window marks the window as contaminated.
# R-200-2: run_command (cat/grep/head/tail/ls...) porta nella finestra contenuti di
# file come read_file: dopo un suo output i tool UNCERTAIN vanno all'approvazione.
UNTRUSTED_INPUT_TOOLS: frozenset[str] = frozenset({
    "ricorda", "read_file", "run_command", "browser_scrape", "fetch_email",
})

# Denylist path component prefixes — union of design §2b and §5.
# All entries are casefold; no trailing slashes (comparison uses startswith).
# .env covers .env.prod, .env.local, .envrc, etc. (intentional per design).
_DENY_PREFIXES: tuple[str, ...] = (
    ".gas_memory",
    ".gas_history",
    ".gas_knowledge",
    ".gas_vectors",
    ".gas_tokens",
    ".env",
    "gas.py",
    "brains",
    "modules",
    ".claude",
    "gate_config",
)


def _normalize_path(p: str) -> str:
    """Normalize a path string for denylist comparison.

    Steps: unicodedata NFKC → strip leading './' loops → os.path.normpath →
    casefold.  Raises ValueError for absolute paths or traversal (starts with
    '..' after normpath).
    NFKC reduces FULLWIDTH characters (U+FF0E ．, U+FF0F ／) to ASCII '.', '/'.
    """
    p = unicodedata.normalize("NFKC", p)
    # Strip any number of leading "./" sequences.
    while p.startswith("./"):
        p = p[2:]
    p = os.path.normpath(p)
    if os.path.isabs(p):
        raise ValueError(f"absolute path: {p!r}")
    if p == ".." or p.startswith(".." + os.sep):
        raise ValueError(f"path traversal: {p!r}")
    return p.casefold()


def _in_denylist(normalized: str) -> bool:
    """Return True if the normalized path (or any of its components) is denied."""
    # Check full path starts with any denied prefix.
    for prefix in _DENY_PREFIXES:
        if normalized.startswith(prefix):
            return True
    # Check individual path components.
    try:
        parts = PurePosixPath(normalized).parts
    except Exception:
        return True  # Fail-closed on unparsable path.
    for part in parts:
        for prefix in _DENY_PREFIXES:
            if part.startswith(prefix):
                return True
    return False


def _check_path_arg(args: dict[str, Any]) -> "GateClass | None":
    """Validate the 'relative_path' key in args for read_file / write_file.

    Returns DENY if missing, wrong type, absolute, traversal, or in denylist.
    Returns None if the path is clean (caller continues to allowlist lookup).
    """
    raw = args.get("relative_path")
    if raw is None or not isinstance(raw, str):
        return GateClass.DENY
    try:
        norm = _normalize_path(raw)
    except ValueError:
        return GateClass.DENY
    if _in_denylist(norm):
        return GateClass.DENY
    return None


def _parse_args(args: Any) -> "dict[str, Any] | None":
    """Parse args to a dict.  Accepts dict or JSON string.  Returns None on failure."""
    if isinstance(args, dict):
        return args
    if isinstance(args, str):
        try:
            parsed = json.loads(args)
            if isinstance(parsed, dict):
                return parsed
        except (json.JSONDecodeError, ValueError):
            pass
    return None


def gate_classify(tool_name: Any, args: Any) -> GateClass:
    """Classify a tool call and return its GateClass.

    Rules applied in order:
    1. Invalid tool_name (not str / empty) or unparsable args → DENY.
    2. tool_name in GATE_DENY_TOOLS or not in GATE_ALLOWLIST → DENY.
    3. read_file / write_file: normalize 'relative_path'; absolute/traversal/
       denylist match → DENY.
    4. run_command: check each command token against denylist → DENY on match;
       then apply §8e: UNCERTAIN if GAS_SANDBOX_MODE == 'os_strict', else
       IRREVERSIBLE.
    5. Fallback: return GATE_ALLOWLIST[tool_name].

    Never raises: all internal exceptions are caught and mapped to DENY.
    """
    try:
        # Rule 1 — validate tool_name type.
        if not isinstance(tool_name, str) or not tool_name:
            return GateClass.DENY

        # Rule 2 — explicit deny + allowlist gate.
        if tool_name in GATE_DENY_TOOLS or tool_name not in GATE_ALLOWLIST:
            return GateClass.DENY

        # Parse args (dict or JSON string).
        parsed = _parse_args(args)
        if parsed is None:
            return GateClass.DENY

        # Rule 3 — path-sensitive tools.
        if tool_name in ("read_file", "write_file"):
            result = _check_path_arg(parsed)
            if result is not None:
                return result
            # Path is clean → fall through to allowlist lookup.

        # Rule 4 — run_command: token denylist check + §8e sandbox rule.
        elif tool_name == "run_command":
            command = parsed.get("command")
            if command is None or not isinstance(command, str):
                return GateClass.DENY
            try:
                tokens = shlex.split(command)
            except ValueError:
                return GateClass.DENY
            for token in tokens:
                try:
                    norm = _normalize_path(token)
                except ValueError:
                    # Absolute path or traversal as a command argument → DENY.
                    return GateClass.DENY
                if _in_denylist(norm):
                    return GateClass.DENY
            # Belt-and-suspenders: whole-command substring check (NFKC + casefold).
            # Catches --flag=.env.prod and -f.env patterns where the token itself
            # is not a normalizable path but embeds a denied name as a value.
            cmd_norm = unicodedata.normalize("NFKC", command).casefold()
            for prefix in _DENY_PREFIXES:
                if prefix in cmd_norm:
                    return GateClass.DENY
            # All checks clean → apply §8e sandbox mode rule.
            sandbox_mode = os.environ.get("GAS_SANDBOX_MODE", "")
            if sandbox_mode == "os_strict":
                return GateClass.UNCERTAIN
            return GateClass.IRREVERSIBLE

        # Rule 5 — allowlist lookup.
        return GATE_ALLOWLIST[tool_name]

    except Exception:
        # Rule 1 catch-all: any unexpected error → DENY (fail-closed).
        return GateClass.DENY
