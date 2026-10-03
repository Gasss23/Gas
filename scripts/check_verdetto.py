#!/usr/bin/env python3
"""Verifica che i riferimenti path:riga in §4 VERDETTO DEL REVISORE di
reports/handoff.md siano verificabili: il numero di riga esiste nel file a HEAD.
Il path si risolve, in ordine: (1) file del diff di sessione; (2) file a HEAD
citato per contesto (non toccato nella sessione); (3) nome corto ("bot.py")
che corrisponde a UN SOLO file a HEAD come suffisso di path. Nome corto
ambiguo o file inesistente → citazione non verificabile (F-controlli-auto:
prima ogni file di contesto era un falso positivo).

Se il diff di sessione tocca il motore (gas.py, brains/, modules/, tests/):
- l'esenzione "nessun diff motore" NON vale, qualunque testo ci sia nel §4
  (R-135-4: prima bastava che la frase comparisse, anche dentro un verdetto);
- OGNI verdetto (blocco che inizia con una riga "VERDETTO:") deve citare almeno
  MIN_CITAZIONI_DIFF `path:riga` di file del diff fuori da reports/ e dalla
  memoria del revisore (R-135-1/R-135-2; regola di .claude/agents/revisore.md).
  §4 senza alcuna riga "VERDETTO:" → l'intero §4 vale come un verdetto.
Se il diff di sessione NON tocca il motore → non applicabile.

NOTA IMPORTANTE: questo check prova solo che le citazioni sono verificabili,
NON che il revisore abbia effettivamente letto il codice. Il finding
R-verdetto-evidenza va marcato MITIGATO, NON CHIUSO.

Exit 0: tutte le citazioni verificabili, oppure "non applicabile".
Exit 1: almeno una citazione non verificabile, oppure un verdetto con meno di
MIN_CITAZIONI_DIFF citazioni di file del diff (diff di sessione col motore).
"""

import re
import subprocess
import sys
from pathlib import Path

_REF_RE = re.compile(r"([\w./\-]+\.\w+):(\d+)")

# Estensioni sorgente attese nei path citati dal revisore.
# I TLD (.com, .io, .org ...) non sono in questa lista — filtro per escludere
# falsi positivi su URL come github.com:443 o //host.ext:port.
_VALID_EXTENSIONS = {
    ".py", ".sh", ".md", ".yaml", ".yml",
    ".json", ".toml", ".ini", ".cfg", ".txt",
    ".js", ".ts", ".go", ".rs", ".c", ".h",
    ".html", ".css", ".sql",
}


def _is_valid_path(path: str) -> bool:
    """Ritorna True se il path ha un'estensione sorgente plausibile."""
    ext = Path(path).suffix.lower()
    return ext in _VALID_EXTENSIONS


def _get_repo() -> Path:
    r = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        capture_output=True, text=True,
    )
    if r.returncode == 0 and r.stdout.strip():
        return Path(r.stdout.strip())
    return Path(__file__).parent.parent


def _git(args: list[str], repo: Path) -> subprocess.CompletedProcess:
    return subprocess.run(args, capture_output=True, text=True, cwd=repo)


def _current_branch(repo: Path) -> str:
    r = _git(["git", "rev-parse", "--abbrev-ref", "HEAD"], repo)
    return r.stdout.strip()


def _get_base(override: str | None, repo: Path) -> str | None:
    if override:
        return override.strip()
    r = _git(["git", "merge-base", "origin/main", "HEAD"], repo)
    if r.returncode != 0 or not r.stdout.strip():
        return None
    return r.stdout.strip()


def _session_files(base: str, repo: Path) -> set[str]:
    r = _git(["git", "-c", "core.quotePath=false", "diff", "--name-only", f"{base}..HEAD"], repo)
    if r.returncode != 0:
        return set()
    return {l.strip() for l in r.stdout.splitlines() if l.strip()}


MIN_CITAZIONI_DIFF = 2
_MOTORE_RE = re.compile(r"^(gas\.py|brains/|modules/|tests/)")
_VERDETTO_RE = re.compile(r"^[ \t#*>]*VERDETTO\s*:", re.IGNORECASE | re.MULTILINE)


def _tocca_motore(session: set[str]) -> bool:
    return any(_MOTORE_RE.match(f) for f in session)


def _conta_come_diff(path: str, session: set[str]) -> bool:
    """Citazione valida come 'elemento del diff': file del diff di sessione,
    esclusi i report e la memoria del revisore (non sono il codice revisionato)."""
    return (path in session and not path.startswith("reports/")
            and path != ".claude/agents/memoria_revisore.md")


def _blocchi_verdetto(sec4: str) -> list[str]:
    """Un blocco per ogni riga 'VERDETTO:'; nessuna → tutto il §4 è un blocco."""
    starts = [m.start() for m in _VERDETTO_RE.finditer(sec4)]
    if not starts:
        return [sec4]
    return [sec4[a:b] for a, b in zip(starts, starts[1:] + [len(sec4)])]


def _head_files(repo: Path) -> set[str]:
    r = _git(["git", "-c", "core.quotePath=false", "ls-tree", "-r", "--name-only", "HEAD"], repo)
    if r.returncode != 0:
        return set()
    return {l.strip() for l in r.stdout.splitlines() if l.strip()}


def _resolve_path(path: str, session: set[str], head: set[str]) -> tuple[str | None, str]:
    """Ritorna (path risolto, "") oppure (None, motivo)."""
    if path in session or path in head:
        return path, ""
    cand = sorted(f for f in head if f.endswith("/" + path))
    if len(cand) == 1:
        return cand[0], ""
    if cand:
        return None, f"nome ambiguo a HEAD ({', '.join(cand[:3])})"
    return None, "file non trovato a HEAD (né nel diff né come nome univoco)"


def _line_count(path: str, repo: Path) -> int | None:
    r = _git(["git", "show", f"HEAD:{path}"], repo)
    if r.returncode != 0:
        return None
    return len(r.stdout.splitlines())


def _extract_section4(text: str) -> str | None:
    m = re.search(
        r"##\s*§4\s+VERDETTO DEL REVISORE.*?(?=\n##\s*§|\Z)",
        text,
        re.DOTALL | re.IGNORECASE,
    )
    return m.group(0) if m else None


def main(argv: list[str]) -> int:
    base_override = argv[1] if len(argv) > 1 else None

    repo = _get_repo()
    handoff = repo / "reports" / "handoff.md"

    branch = _current_branch(repo)
    if branch == "main":
        print("check_verdetto: non applicabile (HEAD su main).")
        return 0

    if not handoff.exists():
        print("check_verdetto: reports/handoff.md non trovato — non applicabile.")
        return 0

    text = handoff.read_text(encoding="utf-8")
    sec4 = _extract_section4(text)
    if sec4 is None:
        print("check_verdetto: §4 non trovata in reports/handoff.md — non applicabile.")
        return 0

    base = _get_base(base_override, repo)
    if base is None:
        print("check_verdetto: git merge-base fallito — non applicabile.", file=sys.stderr)
        return 0

    session = _session_files(base, repo)

    if "reports/handoff.md" not in session:
        print("check_verdetto: non applicabile (reports/handoff.md non nel diff di sessione).")
        return 0

    # R-135-4: l'esenzione dipende dal diff REALE, non da una frase nel §4.
    if not _tocca_motore(session):
        print("check_verdetto: non applicabile (il diff di sessione non tocca il motore).")
        return 0

    head = _head_files(repo)
    errors: list[str] = []

    # R-135-1/R-135-2: ogni verdetto cita almeno MIN_CITAZIONI_DIFF elementi del diff.
    for i, blocco in enumerate(_blocchi_verdetto(sec4), 1):
        nel_diff = set()
        for p, l in _REF_RE.findall(blocco):
            if not _is_valid_path(p):
                continue
            resolved, _ = _resolve_path(p, session, head)
            if resolved is not None and _conta_come_diff(resolved, session):
                nel_diff.add((resolved, l))
        if len(nel_diff) < MIN_CITAZIONI_DIFF:
            errors.append(
                f"  verdetto {i}: {len(nel_diff)} citazioni path:riga di file del diff "
                f"(minimo {MIN_CITAZIONI_DIFF}) — verdetto senza evidenza verificabile"
            )

    # Filtra i match: tieni solo quelli con estensione sorgente plausibile
    refs = [(p, l) for p, l in _REF_RE.findall(sec4) if _is_valid_path(p)]
    for path, lineno_str in refs:
        lineno = int(lineno_str)
        resolved, motivo = _resolve_path(path, session, head)
        if resolved is None:
            errors.append(f"  {path}:{lineno} — {motivo}")
            continue
        nlines = _line_count(resolved, repo)
        if nlines is None:
            errors.append(f"  {path}:{lineno} — file non trovato a HEAD")
        elif lineno > nlines:
            errors.append(
                f"  {path}:{lineno} — riga oltre la fine del file ({nlines} righe a HEAD)"
            )

    if errors:
        print("check_verdetto: ERRORE — citazioni non verificabili in §4.", file=sys.stderr)
        print("", file=sys.stderr)
        print("NOTA: questo check prova solo che le citazioni sono verificabili,", file=sys.stderr)
        print("NON che il revisore abbia letto il codice. Finding: MITIGATO, non chiuso.", file=sys.stderr)
        print("", file=sys.stderr)
        for e in errors:
            print(e, file=sys.stderr)
        return 1

    print(f"check_verdetto: OK — {len(refs)} riferimento/i verificato/i.")
    print("NOTA: citazioni verificabili ≠ revisore ha letto il codice. Finding: MITIGATO.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
