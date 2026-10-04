#!/usr/bin/env python3
"""Verifica che §2 GIT DIFF --STAT di reports/handoff.md dichiari
esattamente i file modificati in questa sessione (BASE..HEAD).

Exit 0: set coerente, oppure "non applicabile" (main / diff vuoto / handoff non scritto
        in una sessione FUORI dal perimetro di review).
Exit 1 SEMPRE (qualunque sessione): merge-base o git diff falliti, perimetro di review
assente o vuoto, handoff nel diff ma file mancante, §2 mancante, set incoerente.
Exit 1 in più se il diff tocca il perimetro (.claude/perimetro_review.txt): handoff non
nel diff di sessione (V-A, verifica esterna PR #119) — il check required non si salta
più non scrivendo l'handoff.
Exit 1: set incoerente — handoff omette o aggiunge file rispetto al diff reale.
"""

import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from check_verdetto import _carica_perimetro, _nel_perimetro, _session_files  # noqa: E402

ALLOWLIST = {
    "reports/ultima_risposta.md",
}


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


def _diff_names(base: str, repo: Path) -> set[str] | None:
    """None se `git diff` fallisce (R-141-1: mai un insieme vuoto travestito da diff vuoto)."""
    r = _git(["git", "-c", "core.quotePath=false", "diff", "--name-only", f"{base}..HEAD"], repo)
    if r.returncode != 0:
        return None
    return {line.strip() for line in r.stdout.splitlines() if line.strip()}


def _declared_set(handoff: Path) -> set[str] | None:
    """Estrae i path dal blocco fence sotto '## §2 GIT DIFF --STAT'.

    Ritorna None se il blocco non è trovato.
    Scarta la riga sommario 'N files changed ...'.
    """
    text = handoff.read_text(encoding="utf-8")
    m = re.search(
        r"##\s*§2\s+GIT DIFF --STAT.*?```(.*?)```",
        text,
        re.DOTALL | re.IGNORECASE,
    )
    if not m:
        return None

    paths: set[str] = set()
    for line in m.group(1).splitlines():
        line = line.strip()
        if not line:
            continue
        if re.match(r"\d+\s+files?\s+changed", line):
            continue
        if "|" in line:
            path = line.split("|")[0].strip()
            if path:
                paths.add(path)
    return paths


def main(argv: list[str]) -> int:
    base_override = argv[1] if len(argv) > 1 else None

    repo = _get_repo()
    handoff = repo / "reports" / "handoff.md"

    branch = _current_branch(repo)
    if branch == "main":
        print("check_handoff: non applicabile (HEAD su main).")
        return 0

    base = _get_base(base_override, repo)
    if base is None:
        # V-A: senza base non si può dire se la sessione tocca il perimetro → fail-closed.
        print("check_handoff: ERRORE — git merge-base fallito: impossibile verificare (fail-closed).",
              file=sys.stderr)
        return 1

    all_changed = _diff_names(base, repo)
    session = _session_files(base, repo)
    if all_changed is None or session is None:
        print(f"check_handoff: ERRORE — git diff {base}..HEAD fallito: impossibile verificare (fail-closed).",
              file=sys.stderr)
        return 1

    # Guard: diff vuoto
    if not all_changed:
        print("check_handoff: non applicabile (diff BASE..HEAD vuoto).")
        return 0

    # V-A: la sessione tocca il perimetro di review? Allora l'handoff è obbligatorio.
    perimetro = _carica_perimetro(repo=repo, base=base)
    if perimetro is None:
        print("check_handoff: ERRORE — perimetro di review assente o vuoto: fail-closed.",
              file=sys.stderr)
        return 1
    nel_perimetro = any(_nel_perimetro(f, perimetro) for f in session)

    # Guard: handoff non scritto in questa sessione
    if "reports/handoff.md" not in all_changed:
        if nel_perimetro:
            print("check_handoff: ERRORE — la sessione tocca il perimetro di review ma "
                  "reports/handoff.md non è nel diff di sessione: handoff obbligatorio (V-A).",
                  file=sys.stderr)
            return 1
        print("check_handoff: non applicabile (reports/handoff.md non nel diff di sessione).")
        return 0

    if not handoff.exists():
        print("check_handoff: reports/handoff.md non trovato sul filesystem.", file=sys.stderr)
        return 1

    # SET REALE: diff meno allowlist
    real = all_changed - ALLOWLIST

    declared = _declared_set(handoff)
    if declared is None:
        print("check_handoff: blocco §2 GIT DIFF --STAT non trovato in reports/handoff.md.",
              file=sys.stderr)
        return 1

    if real == declared:
        print(f"check_handoff: OK — {len(real)} file dichiarati correttamente.")
        return 0

    only_real = real - declared
    only_declared = declared - real

    print("check_handoff: ERRORE — set file incoerente.", file=sys.stderr)
    print(f"\nSET REALE     ({len(real)} file):", file=sys.stderr)
    for f in sorted(real):
        print(f"  {f}", file=sys.stderr)
    print(f"\nSET DICHIARATO ({len(declared)} file):", file=sys.stderr)
    for f in sorted(declared):
        print(f"  {f}", file=sys.stderr)
    if only_real:
        print("\nIn diff ma NON in §2 (omessi dall'handoff):", file=sys.stderr)
        for f in sorted(only_real):
            print(f"  {f}", file=sys.stderr)
    if only_declared:
        print("\nIn §2 ma NON nel diff (fantasmi):", file=sys.stderr)
        for f in sorted(only_declared):
            print(f"  {f}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
