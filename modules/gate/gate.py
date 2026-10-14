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
  with a denied prefix → DENY for read_file (dal 2026-10-11 solo i prefissi
  del livello 3: gas.py, brains/, modules/ si possono LEGGERE).
- write_file: schema a 3 livelli (livello_scrittura, decisione operatore 1A del
  2026-10-11): 3 = mai → DENY; 2 = codice → IRREVERSIBLE (firma con diff reale e
  pro e contro); 1 = libero → UNCERTAIN.
  Same check for each token of run_command args (conservative).
- run_command sandbox rule (§8e): UNCERTAIN only when
  GAS_SANDBOX_MODE == "os_strict"; IRREVERSIBLE otherwise.
"""

from __future__ import annotations

import json
import os
import re
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
    # Strumenti nativi di sola lettura (FETTA 1, PR A, 2026-10-11): in-process, niente
    # subprocess né shell, stesso controllo dei percorsi di read_file. SAFE in ogni
    # modalità del recinto (funzionano anche senza bwrap).
    "elenca_cartella":        GateClass.SAFE,
    "leggi_righe":            GateClass.SAFE,
    "cerca_testo":            GateClass.SAFE,
    "conta_file":             GateClass.SAFE,
    "data_ora":               GateClass.SAFE,
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
    # FETTA 1 PR A: portano nella finestra contenuti e nomi di file come read_file.
    "elenca_cartella", "leggi_righe", "cerca_testo", "conta_file",
})

# Tool che leggono un percorso: stesso controllo per NOME di read_file (_check_path_arg).
# elenca_cartella/cerca_testo senza percorso lavorano sulla root (".").
TOOL_LETTURA_PERCORSO: frozenset[str] = frozenset({
    "read_file", "elenca_cartella", "leggi_righe", "cerca_testo", "conta_file",
})
_TOOL_PERCORSO_DEFAULT_ROOT: frozenset[str] = frozenset({"elenca_cartella", "cerca_testo"})

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
    # Verifica-bot PR #160 (V-1): catena di avvio eseguita FUORI dalla sandbox
    # (giro notturno launchd, git dello snapshot, hook di git). Una scrittura qui
    # diventerebbe codice eseguito senza cancello al giro/avvio successivo.
    # ".git" copre anche .github/ (CI), .gitattributes, .gitignore.
    "venv",
    ".venv",
    ".git",
    ".gas_notte",   # R-220-4: stato del giro notturno (riepilogo, storie, lock, log)
)

# Verifica-bot PR #160 (V-1): estensioni che Python carica/esegue all'avvio di
# `python3 gas.py` (sys.path[0] = root: un yaml.py o openai.py nella root oscura il
# modulo vero; un .pth in site-packages esegue codice). write_file verso questi file
# è DENY ovunque nella root; la lettura resta consentita.
_DENY_WRITE_SUFFIXES: tuple[str, ...] = (
    ".py", ".pyc", ".pyw", ".pth", ".so", ".dylib",
    # R-222-1: script di shell eseguiti fuori sandbox (hook, gasmerge, fine-task, launchd)
    ".sh", ".zsh", ".bash", ".command",
    ".code-workspace",  # R-249-1: workspace di VS Code, può contenere task eseguiti
)

# R-222-1: file di PRIMO livello letti/eseguiti fuori dalla sandbox con privilegi
# (agente di sviluppo con shell, prompt di sistema, pip, script dell'operatore).
# Solo scrittura: Gas li legge on-demand (es. CLAUDE.md, sez. 6).
_DENY_WRITE_TOP_PREFIXES: tuple[str, ...] = (
    "scripts", "claude.md", ".mcp", "gas_identity", "requirements",
)

# Verifica-bot PR #160 (V-1, d3a593d): file d'istruzioni caricati dagli agenti di
# sviluppo a QUALSIASI livello (CLAUDE.local.md all'avvio, i CLAUDE.md delle
# sottocartelle quando ci si lavora, AGENTS.md). Confronto esatto su ogni pezzo del
# percorso dopo NFKC+casefold (_normalize_path): "dati/claude.md.txt" resta fuori.
_DENY_WRITE_ANY_PART_NAMES: frozenset[str] = frozenset({
    "claude.md", "claude.local.md", "agents.md",
    "agents.override.md",  # R-224-1: Codex lo carica con precedenza su AGENTS.md
    "gemini.md", ".cursorrules",  # istruzioni di Gemini CLI e Cursor
    # Configurazione degli strumenti di sviluppo (riserva aperta FASE 4.5): pytest
    # cerca l'ini anche nelle cartelle dei test lanciati (tests/pytest.ini vince
    # sulla root), quindi il divieto vale a ogni livello, non solo in cima.
    # addopts/plugin lì dentro diventano codice eseguito dall'agente di sviluppo e
    # dalla CI fuori dalla sandbox. conftest.py/noxfile.py: già coperti da ".py".
    "pytest.ini", "pyproject.toml", "setup.cfg", "tox.ini",
    ".pytest.ini", "pytest.toml", ".pytest.toml",  # R-247-1: pytest 9 li carica tutti
    "makefile", "gnumakefile",
    # R-247-2 + V-1 verifica esterna #174: cartelle di editor/agenti che eseguono o
    # caricano istruzioni all'apertura (il confronto vale anche sulle cartelle, quindi
    # tutto .vscode/… è vietato), più la config di altri strumenti di sviluppo. Resta
    # un divieto per nomi (R-223-2): uno strumento nuovo con un altro file non è coperto.
    ".vscode", ".cursor", ".gemini", ".idea", ".devcontainer",
    ".devcontainer.json",  # R-249-1: forma a file singolo della cartella sopra
    ".pre-commit-config.yaml", ".coveragerc", "mypy.ini", ".mypy.ini", ".flake8",
    "uv.toml", "pytest.cfg", "justfile", "dockerfile", ".python-version", "package.json",
    # V-2 bot #175: pdb e pylint eseguono codice dalla config; V-1 verifica esterna
    # (agente) #175: hook git di husky, npm, altri editor/agenti.
    ".pdbrc", ".pylintrc", "pylintrc", ".husky", ".npmrc", ".windsurf", ".zed",
})


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


def _in_denylist(normalized: str, prefissi: "tuple[str, ...] | None" = None) -> bool:
    """Return True if the normalized path (or any of its components) is denied.
    `prefissi` None = _DENY_PREFIXES; la LETTURA usa _LETTURA_NEGATA (operatore
    2026-10-11: Gas legge gas.py, brains/, modules/ ma non li tocca senza firma)."""
    if prefissi is None:
        prefissi = _DENY_PREFIXES
    # Check full path starts with any denied prefix.
    for prefix in prefissi:
        if normalized.startswith(prefix):
            return True
    # Check individual path components.
    try:
        parts = PurePosixPath(normalized).parts
    except Exception:
        return True  # Fail-closed on unparsable path.
    for part in parts:
        for prefix in prefissi:
            if part.startswith(prefix):
                return True
    return False


def _check_path_arg(args: dict[str, Any], write: bool = False) -> "GateClass | None":
    """Validate the 'relative_path' key in args for read_file.

    Returns DENY if missing, wrong type, absolute, traversal, or in denylist.
    Returns None if the path is clean (caller continues to allowlist lookup).
    write=True (vecchio divieto unico di scrittura) non è più usato da
    gate_classify: write_file passa da livello_scrittura (schema a 3 livelli).
    """
    raw = args.get("relative_path")
    if raw is None or not isinstance(raw, str):
        return GateClass.DENY
    try:
        norm = _normalize_path(raw)
    except ValueError:
        return GateClass.DENY
    if _in_denylist(norm, None if write else _LETTURA_NEGATA):
        return GateClass.DENY
    if not write and _nome_da_segreto(norm):
        return GateClass.DENY
    if write and norm.rstrip("/. ").endswith(_DENY_WRITE_SUFFIXES):
        return GateClass.DENY
    if write and PurePosixPath(norm).parts[:1] and \
            PurePosixPath(norm).parts[0].startswith(_DENY_WRITE_TOP_PREFIXES):
        return GateClass.DENY
    # V-1 bot #174: punti/spazi finali tolti da OGNI pezzo, non solo dalla fine del
    # percorso ("pytest.ini.", ".vscode./tasks.json"): su Windows sono lo stesso file.
    if write and any(p.rstrip(". ") in _DENY_WRITE_ANY_PART_NAMES
                     for p in PurePosixPath(norm).parts):
        return GateClass.DENY
    return None


# --- Schema a 3 livelli per write_file (decisione operatore 1A, 2026-10-11) ---
# Livello 3 — MAI, nemmeno con firma: segreti, git/CI, il cancello stesso, la
# macchina di controllo dell'agente di sviluppo, memoria/cronologia/stato del giro,
# ambienti Python. Confronto per prefisso su OGNI pezzo del percorso (come
# _in_denylist), più il percorso del cancello.
_LIVELLO3_PREFISSI: tuple[str, ...] = (
    ".env", ".git", ".claude",
    ".gas_memory", ".gas_history", ".gas_knowledge", ".gas_vectors", ".gas_tokens",
    ".gas_notte", "gate_config", "venv", ".venv",
)
# Il cancello: "modules/gate" come prefisso (copre anche modules/gate.py e simili).
_LIVELLO3_CANCELLO: tuple[str, str] = ("modules", "gate")

# Livello 2 — FIRMA su Telegram con diff reale + pro e contro: il codice e ciò che
# viene eseguito o caricato fuori dalla sandbox. È ESATTAMENTE il vecchio insieme
# negato in scrittura meno il livello 3: nessun file diventa più libero di "firma".
_LIVELLO2_PREFISSI: tuple[str, ...] = ("gas.py", "brains", "modules")

LIVELLO_LIBERO, LIVELLO_FIRMA, LIVELLO_MAI = 1, 2, 3

# Lettura (decisione operatore 2026-10-11, «Gas può leggere i file ma non toccarli»):
# read_file e run_command possono leggere gas.py, brains/, modules/ (livello 2 in
# scrittura). Restano illeggibili SOLO i file del livello 3: segreti, git/CI,
# .claude, memoria/cronologia/stato, venv.
_LETTURA_NEGATA: tuple[str, ...] = _LIVELLO3_PREFISSI


# R-275-1 + V-2 verifica esterna #182: `.env` seguito da QUALSIASI cosa è un segreto,
# salvo le parole note che iniziano così (environment, envelope, envoy).
_SEGRETO_RE = re.compile(r"\.env(?!ironment|elope|oy)")


# Decisione operatore 2026-10-11 («vietale»): chiavi private e file di credenziali
# illeggibili ovunque nella root (prima Gas li leggeva e cerca_testo li trovava).
# Confronto su OGNI pezzo del percorso (casefold, punti/spazi finali tolti).
# Divieto per nomi (come R-223-2): un file di segreti con un nome qualsiasi non è coperto.
_CHIAVE_PRIVATA_RE = re.compile(
    # Varianti (bot e verifica esterna #188, V-1/V-2): copie (~, .bak, .old) e nomi
    # con prefisso/suffisso (backup_id_rsa, my_credentials.json, secrets_prod.yaml).
    # Bordo = niente lettera prima/dopo: secretary.md, keyboard, valid_rsa restano fuori;
    # credentials_guide.md e secret_sauce.md sono bloccati per eccesso (R-289-2).
    r"(?<![a-z])(id[-_](rsa|dsa|ecdsa|ed25519)"  # chiavi ssh, anche backup_id_rsa, id-rsa
    r"|secrets?|credentials?"                  # secrets.yaml, my_credentials.json
    # D1 (R-291-1, bot #188): token_cache.json / tokens-prod.yaml (separatore dopo
    # token, così tokenizer.json resta fuori), clientsecret.json.
    r"|service[-_]?account|tokens?([-_][a-z0-9_-]*)?\.(json|txt|ya?ml|pickle|bin|db)"
    r"|client[-_]?secrets?"
    # D2 (secondo passaggio claude.ai #198): chiavi API e token con nome parlante,
    # anche senza estensione e con lo spazio («Seed Phrase.txt», R-329-1); key.txt / prod_keys.yaml (il bordo copre il prefisso_).
    # D3: separatore ripetibile (`api  key`, `api__key`: R-ve201-2) e altri fornitori
    # senza estensione (bot_token, telegram_token, slack_token, mistral_key: R-329-2).
    r"|api[-_ ]*(key|token)s?|(access|refresh)[-_ ]*tokens?"
    # Bot #202 V-1: anche i fornitori che Gas usa (openrouter, elevenlabs, voice, claude)
    # e altri comuni (discord, gitlab, npm, pypi, huggingface).
    r"|(gh|github|hf|openai|anthropic|gemini|groq|mistral|cohere|slack|telegram|bot|o?auth"
    r"|openrouter|elevenlabs|voice|claude|discord|gitlab|npm|pypi|huggingface)"
    r"[-_. ]*(token|key)s?"  # verifica esterna #202 V-1: anche bot.token, telegram.token
    r"|keys?\.(txt|json|ya?ml)"
    r"|private[-_ ]*keys?|privkeys?|(ssh|deploy)[-_ ]*keys?|rsa_keys?"
    # D2: sessioni del browser (Playwright storage_state), OAuth, cookie
    r"|cookies?\.(json|txt|sqlite)|(storage|auth)_state\.json|oauth2?\.json|sessions?\.json"
    # D2: portafogli e frasi di recupero (seed_data.csv resta fuori)
    r"|keystore\.json|(seed|mnemonic)\.(txt|json)|(seed|recovery)[-_ ]*phrase"
    # D3 (R-ve201-1, R-bot201-1): anche le copie e le liste (passwords_backup.txt,
    # password_list.txt, password-prod.csv, «passwords copy.txt», «password (1).txt»,
    # password_2024.txt); passwordless.md e password_reset.md restano fuori.
    r"|passwords?([-_ ]+(backup|bak|old|new|copy|list|prod|dev|[0-9]+)| ?\([0-9]+\))*"
    r"(\.[a-z0-9]+)*~?$"
    r"|wg[0-9]+\.conf"
    r")(?![a-z])"
    # D1/D2: anche con prefisso (mywallet.dat, mykubeconfig, kubeconfigs)
    r"|wallet\.(dat|json|txt)(?![a-z])|kubeconfig"
    # D1: .dockercfg, .vault-token, _netrc (nome Windows di .netrc); D2: .azure, .auth
    # e le config con credenziali (BASSA): .terraformrc .boto .s3cfg .my.cnf .yarnrc
    r"|^\.(ssh|gnupg|aws|kube|docker|dockercfg|vault-token|netrc|pgpass|pypirc|htpasswd|npmrc"
    r"|auth|terraformrc|boto|s3cfg|my\.cnf|yarnrc|sentryclirc)(?![a-z])"
    r"|^\.azure(?![a-z-])"                     # .azure-pipelines (CI) resta fuori
    r"|^_netrc(?![a-z])"
    # chiavi/certificati/portachiavi, anche copie (x.pem~, x.key.bak: R-289-1);
    # D1: chiavi GPG/PGP (.gpg binarie, .asc armored); D2: .p8 (chiavi Apple/Snowflake),
    # sessioni Telethon/Pyrogram (.session, .session-journal), stato e variabili
    # Terraform, profili VPN.
    r"|\.(pem|key|p12|pfx|ppk|jks|keystore|kdbx|gpg|pgp|asc|p8|session|tfstate|tfvars|ovpn)(?![a-z])"
)


# Nome intero dell'ULTIMO pezzo (+ copie ~ .bak .old e il «-» di /etc/shadow-):
# tokens.md, keys.md e session_notes.md restano leggibili. D3 (R-bot201-3): solo
# l'ultimo pezzo, così una cartella keys/ o shadow/ non rende illeggibile il contenuto.
_NOME_INTERO_RE = re.compile(r"^(tokens?|keys?|passwd|shadow)(-|~|\.bak|\.old)?$")

# Bot #202 V-2 + R-333-1: dentro una cartella keys/ o tokens/ è negato tutto
# (keys/openai, tokens/github, keys/prod.toml) tranne documentazione e codice:
# keys/readme.md, keys/setup.py restano leggibili.
_NOME_CARTELLA_CHIAVI_RE = re.compile(r"^(tokens?|keys?)$")
_DOC_IN_CARTELLA_CHIAVI_RE = re.compile(r"\.(md|rst|py)$")


def _nome_da_segreto(normalized: str) -> bool:
    """V-2 verifica esterna #181 + R-274-1 + R-275-1: un pezzo del percorso con `.env`
    NON seguito da una lettera (prod.env, prod.env.local, prod.env~, «prod.env copy»,
    prod.env(1), prod.env1, prod.envbak) è un file di segreti anche dentro cartelle
    leggibili; `x.environment.py`, `a.envelope.md`, `envoy.py` no (percorso casefold).
    Lo stesso per chiavi private e credenziali (_CHIAVE_PRIVATA_RE).
    Punti/spazi finali tolti."""
    parti = PurePosixPath(normalized).parts
    puliti = [p.rstrip(". ") for p in parti]
    if puliti and _NOME_INTERO_RE.search(puliti[-1]):
        return True
    if (len(puliti) > 1 and not _DOC_IN_CARTELLA_CHIAVI_RE.search(puliti[-1])
            and any(_NOME_CARTELLA_CHIAVI_RE.search(c) for c in puliti[:-1])):
        return True
    # D3 (R-329-2): la cartella della CLI GitHub (.config/gh/hosts.yml contiene il
    # token), confrontata sui pezzi puliti (bot #202 V-3: «.config./gh», «gh /»).
    if any(a == ".config" and b == "gh" for a, b in zip(puliti, puliti[1:])):
        return True
    for pulito in puliti:
        # R-324-3: un pezzo oltre 255 caratteri non è un nome di file reale; negarlo
        # subito tiene lineare il costo della regex (fail-closed).
        if len(pulito) > 255:
            return True
        if _SEGRETO_RE.search(pulito) or _CHIAVE_PRIVATA_RE.search(pulito):
            return True
    return False


def lettura_consentita(relative_path: Any) -> bool:
    """True se read_file può leggere il percorso (relativo alla root). Usata anche
    dal kernel sul percorso RISOLTO (symlink). Mai eccezioni: errore → False."""
    try:
        if not isinstance(relative_path, str) or not relative_path.strip():
            return False
        norm = _normalize_path(relative_path)
        return not (_in_denylist(norm, _LETTURA_NEGATA) or _nome_da_segreto(norm))
    except Exception:
        return False


def livello_scrittura(relative_path: Any) -> int:
    """Livello di write_file per un percorso relativo alla root di Gas.

    1 = libero (snapshot preventivo, cancello solo se la finestra è contaminata);
    2 = firma umana su Telegram con diff reale generato dal kernel + pro e contro;
    3 = mai. Percorso non stringa, assoluto, con traversal o non normalizzabile → 3.
    Mai eccezioni (fail-closed su 3)."""
    try:
        if not isinstance(relative_path, str) or not relative_path.strip():
            return LIVELLO_MAI
        norm = _normalize_path(relative_path)
        parts = PurePosixPath(norm).parts
        if not parts or norm in (".", ""):
            return LIVELLO_MAI
        # Punti/spazi finali tolti da ogni pezzo (V-1 bot #174: su Windows
        # "gate." e "gate" sono la stessa cartella).
        puliti = tuple(p.rstrip(". ") for p in parts)
        for part in parts + puliti:
            if part.startswith(_LIVELLO3_PREFISSI):
                return LIVELLO_MAI
        if len(puliti) >= 2 and puliti[0] == _LIVELLO3_CANCELLO[0] and \
                puliti[1].startswith(_LIVELLO3_CANCELLO[1]):
            return LIVELLO_MAI
        if _nome_da_segreto(norm):  # segreti illeggibili: mai scritti né sovrascritti
            return LIVELLO_MAI
        for part in parts + puliti:
            if part.startswith(_LIVELLO2_PREFISSI):
                return LIVELLO_FIRMA
        if norm.rstrip("/. ").endswith(_DENY_WRITE_SUFFIXES):
            return LIVELLO_FIRMA
        if parts[0].startswith(_DENY_WRITE_TOP_PREFIXES):
            return LIVELLO_FIRMA
        if any(p in _DENY_WRITE_ANY_PART_NAMES for p in puliti):
            return LIVELLO_FIRMA
        return LIVELLO_LIBERO
    except Exception:
        return LIVELLO_MAI


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
    3. read_file (e i tool di TOOL_LETTURA_PERCORSO) / write_file: normalize 'relative_path'; absolute/traversal/
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
        if tool_name == "write_file":
            # Schema a 3 livelli (1A): mai → DENY, codice → firma (IRREVERSIBLE:
            # sempre al cancello), il resto → UNCERTAIN come prima.
            livello = livello_scrittura(parsed.get("relative_path"))
            if livello == LIVELLO_MAI:
                return GateClass.DENY
            if livello == LIVELLO_FIRMA:
                return GateClass.IRREVERSIBLE
        elif tool_name in TOOL_LETTURA_PERCORSO:
            if tool_name in _TOOL_PERCORSO_DEFAULT_ROOT and "relative_path" not in parsed:
                parsed = {**parsed, "relative_path": "."}
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
                if _in_denylist(norm, _LETTURA_NEGATA):
                    return GateClass.DENY
            # Belt-and-suspenders: whole-command substring check (NFKC + casefold).
            # Catches --flag=.env.prod and -f.env patterns where the token itself
            # is not a normalizable path but embeds a denied name as a value.
            cmd_norm = unicodedata.normalize("NFKC", command).casefold()
            for prefix in _LETTURA_NEGATA:  # run_command è in sola lettura (allowlist)
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
