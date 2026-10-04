#!/usr/bin/env python3
"""Verifica che i riferimenti path:riga in §4 VERDETTO DEL REVISORE di
reports/handoff.md siano verificabili: il numero di riga esiste nel file a HEAD.
Il path si risolve, in ordine: (1) file del diff di sessione; (2) file a HEAD
citato per contesto (non toccato nella sessione); (3) nome corto ("bot.py")
che corrisponde a UN SOLO file a HEAD come suffisso di path. Nome corto
ambiguo o file inesistente → citazione non verificabile (F-controlli-auto:
prima ogni file di contesto era un falso positivo).

Le citazioni presenti nel §4 si verificano SEMPRE (V-2 verifica esterna PR #118:
prima, una sessione fuori dal perimetro saltava anche questa verifica).

Se il diff di sessione tocca il PERIMETRO DI REVIEW (.claude/perimetro_review.txt:
motore + macchina di controllo, fonte unica condivisa con review_gate.sh):
- l'esenzione "nessun diff motore" NON vale, qualunque testo ci sia nel §4
  (R-135-4: prima bastava che la frase comparisse, anche dentro un verdetto);
- OGNI verdetto deve citare almeno MIN_CITAZIONI_DIFF `path:riga` di file del
  diff fuori da reports/ e dalla memoria del revisore (R-135-1/R-135-2); se il
  diff contiene codice, le citazioni devono essere di CODICE, non di .md/.txt
  (R-136-5). Un verdetto inizia a ogni riga "VERDETTO: <esito>" e anche a ogni
  riga che apre con un esito (`**Verdetto**: APPROVATO`, `Esito: BOCCIATO`,
  `APPROVATO — …`): un verdetto scritto in un formato diverso non si fonde più
  col precedente (R-136-2). §4 senza alcuna di queste righe → un solo verdetto.
Perimetro assente o vuoto → exit 1 (fail-closed).
V-A (verifica esterna PR #119): con il perimetro toccato, handoff assente dal diff o dal
disco, §4 non trovata o merge-base fallito sono ERRORI (exit 1), non "non applicabile".

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
    r = _git(["git", "merge-base", "refs/remotes/origin/main", "HEAD"], repo)  # R-143-1: ref completo, un tag "origin/main" non vince
    if r.returncode != 0 or not r.stdout.strip():
        return None
    return r.stdout.strip()


def _session_files(base: str, repo: Path) -> set[str] | None:
    """File del diff di sessione. None se `git diff` fallisce (R-141-1: mai un insieme
    vuoto che si travesta da "sessione vuota" → "non applicabile")."""
    # R-138-2: --no-renames (il path di origine di un rename conta) e -z (nomi grezzi).
    r = _git(["git", "diff", "--name-only", "--no-renames", "-z", f"{base}..HEAD"], repo)
    if r.returncode != 0:
        return None
    return {l for l in r.stdout.split("\0") if l.strip()}


MIN_CITAZIONI_DIFF = 2
PERIMETRO_FILE = Path(__file__).resolve().parent.parent / ".claude" / "perimetro_review.txt"
_ESITI = r"(?:APPROVATO|BOCCIATO|RESPINTO|NULLO)"
# R-138-3: apre un verdetto (a) la riga "VERDETTO:" del formato obbligatorio, (b) una
# riga "Verdetto…/Esito…: <ESITO>" (anche "Verdetto finale", "Esito della review"),
# (c) una riga che apre con l'esito IN MAIUSCOLO seguito da separatore o fine riga
# ("APPROVATO — …"). Non aprono: voci di elenco ("- Esito: ok", "- verdetto nullo: «…»",
# forma canonica per riportare un verdetto nullo), prosa ("Approvato il fix …"),
# righe dentro i blocchi di codice.
_VERDETTO_RE = re.compile(
    r"^[ \t#>]*[*_]*\s*(?:(?i:VERDETTO)\s*[*_]*\s*:"
    r"|(?i:verdetto|esito)[\w ]{0,20}?[*_ \t]*[:—–-][*_ \t]*(?i:" + _ESITI + r")"
    r"|" + _ESITI + r"(?:[ \t]+CON[ \t]+RISERVE)?[*_]*[ \t]*(?:[—–:-]|$))",
    re.MULTILINE,
)
_FENCE_RE = re.compile(r"^[ \t]*```.*?^[ \t]*```[ \t]*$", re.MULTILINE | re.DOTALL)
_DOC_SUFFIX = {".md", ".txt"}


_VOCI_CABLATE = [".claude/perimetro_review.txt", ".claude/hooks/"]


def _voci(testo: str) -> list[str]:
    voci = [r.split("#", 1)[0].strip() for r in testo.splitlines()]
    return [v for v in voci if v]


def _carica_perimetro(path: Path = PERIMETRO_FILE, repo: Path | None = None,
                      base: str | None = None) -> list[str] | None:
    """Voci del perimetro (stesso formato letto da review_gate.sh). R-138-1: unione
    del file dello script, delle voci cablate e della versione alla BASE della
    sessione (una PR non può togliersi dal perimetro da sola). None se il file
    dello script è assente o vuoto (fail-closed)."""
    try:
        voci = _voci(path.read_text(encoding="utf-8"))
    except OSError:
        return None
    if not voci:
        return None
    voci += _VOCI_CABLATE
    if repo is not None and base:
        r = _git(["git", "show", f"{base}:.claude/perimetro_review.txt"], repo)
        if r.returncode == 0:
            voci += _voci(r.stdout)
    return voci


def _nel_perimetro(f: str, perimetro: list[str]) -> bool:
    return any(f.startswith(v) if v.endswith("/") else f == v for v in perimetro)


def _contabile(path: str) -> bool:
    """Elemento del codice revisionato: esclusi i report e la memoria del revisore."""
    return not path.startswith("reports/") and path != ".claude/agents/memoria_revisore.md"


def _conta_come_diff(path: str, session: set[str]) -> bool:
    """Citazione valida come 'elemento del diff'. Se il diff contiene codice
    (non .md/.txt), contano solo le citazioni di codice (R-136-5)."""
    if path not in session or not _contabile(path):
        return False
    ha_codice = any(_contabile(f) and Path(f).suffix.lower() not in _DOC_SUFFIX for f in session)
    return not ha_codice or Path(path).suffix.lower() not in _DOC_SUFFIX


def _blocchi_verdetto(sec4: str) -> list[str]:
    """Un blocco per ogni riga che apre un verdetto; nessuna → tutto il §4 è un blocco."""
    # Le righe dentro i blocchi di codice non aprono verdetti (R-138-3).
    mascherato = _FENCE_RE.sub(lambda m: re.sub(r"[^\n]", " ", m.group(0)), sec4)
    starts = [m.start() for m in _VERDETTO_RE.finditer(mascherato)]
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

    base = _get_base(base_override, repo)
    if base is None:
        print("check_verdetto: ERRORE — git merge-base fallito: impossibile verificare (fail-closed).",
              file=sys.stderr)
        return 1

    session = _session_files(base, repo)
    if session is None:
        print(f"check_verdetto: ERRORE — git diff {base}..HEAD fallito: impossibile verificare (fail-closed).",
              file=sys.stderr)
        return 1

    perimetro = _carica_perimetro(repo=repo, base=base)
    if perimetro is None:
        print(f"check_verdetto: ERRORE — perimetro di review assente o vuoto ({PERIMETRO_FILE}): fail-closed.",
              file=sys.stderr)
        return 1
    # R-135-4: l'esenzione dipende dal diff REALE, non da una frase nel §4.
    nel_perimetro = any(_nel_perimetro(f, perimetro) for f in session)

    # V-A: con il perimetro toccato l'handoff (e il suo §4) è obbligatorio.
    def _manca(motivo: str) -> int:
        if nel_perimetro:
            print(f"check_verdetto: ERRORE — la sessione tocca il perimetro di review ma {motivo} (V-A).",
                  file=sys.stderr)
            return 1
        print(f"check_verdetto: non applicabile ({motivo}).")
        return 0

    if "reports/handoff.md" not in session:
        return _manca("reports/handoff.md non è nel diff di sessione")
    if not handoff.exists():
        return _manca("reports/handoff.md non esiste")
    sec4 = _extract_section4(handoff.read_text(encoding="utf-8"))
    if sec4 is None:
        return _manca("§4 VERDETTO DEL REVISORE non trovata in reports/handoff.md")

    head = _head_files(repo)
    errors: list[str] = []

    # R-135-1/R-135-2: ogni verdetto cita almeno MIN_CITAZIONI_DIFF elementi del diff.
    # Fuori dal perimetro il minimo non si applica, ma le citazioni si verificano (V-2).
    for i, blocco in enumerate(_blocchi_verdetto(sec4) if nel_perimetro else [], 1):
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

    if not nel_perimetro and not refs:
        print("check_verdetto: non applicabile (diff fuori dal perimetro di review, nessuna citazione).")
        return 0
    print(f"check_verdetto: OK — {len(refs)} riferimento/i verificato/i"
          f"{'' if nel_perimetro else ' (diff fuori dal perimetro: minimo per verdetto non richiesto)'}.")
    print("NOTA: citazioni verificabili ≠ revisore ha letto il codice. Finding: MITIGATO.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
