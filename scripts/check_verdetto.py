#!/usr/bin/env python3
"""Verifica che i riferimenti path:riga in §4 VERDETTO DEL REVISORE di
reports/handoff.md siano verificabili: il path esiste nel diff di sessione
e il numero di riga esiste nel file a HEAD.

NOTA IMPORTANTE: questo check prova solo che le citazioni sono verificabili,
NON che il revisore abbia effettivamente letto il codice. Il finding
R-verdetto-evidenza va marcato MITIGATO, NON CHIUSO.

Exit 0: tutte le citazioni verificabili, oppure "non applicabile".
Exit 1: almeno una citazione non verificabile.
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
    r = _git(["git", "diff", "--name-only", f"{base}..HEAD"], repo)
    if r.returncode != 0:
        return set()
    return {l.strip() for l in r.stdout.splitlines() if l.strip()}


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

    if re.search(r"nessun diff motore", sec4, re.IGNORECASE):
        print("check_verdetto: non applicabile (§4 dichiara nessun diff motore).")
        return 0

    base = _get_base(base_override, repo)
    if base is None:
        print("check_verdetto: git merge-base fallito — non applicabile.", file=sys.stderr)
        return 0

    session = _session_files(base, repo)

    if "reports/handoff.md" not in session:
        print("check_verdetto: non applicabile (reports/handoff.md non nel diff di sessione).")
        return 0

    # Filtra i match: tieni solo quelli con estensione sorgente plausibile
    refs = [(p, l) for p, l in _REF_RE.findall(sec4) if _is_valid_path(p)]
    if not refs:
        print("check_verdetto: nessun riferimento path:riga in §4 — OK (nulla da verificare).")
        return 0

    errors: list[str] = []
    for path, lineno_str in refs:
        lineno = int(lineno_str)
        if path not in session:
            errors.append(f"  {path}:{lineno} — path NON nel diff di sessione")
            continue
        nlines = _line_count(path, repo)
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
