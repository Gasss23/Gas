r"""A2 (R-gate-matcher-1, alias di R-gjq-1/R-137-2): il comando Bash e' davvero un `git commit`?

review_gate.sh decide con `grep -Eq 'git[[:space:]].*commit'` sul testo GREZZO, quindi
blocca anche la prosa: un `echo "... (committed)"` dopo un `git log`, un `grep` che legge
il gate stesso, un heredoc che scrive un report. Questo helper toglie dal testo SOLO cio'
che di sicuro non viene eseguito, e solo quando ogni comando della riga e' noto e inerte.

Uso: il comando su stdin. Exit 3 = di sicuro NON e' un commit. Qualunque altro esito
(1 per un'eccezione, python assente, 0) = "e' un commit o non si sa": FAIL-CLOSED, il
gate prosegue come prima. Non allarga mai: se il testo grezzo non contiene il pattern,
l'hook esce prima di chiamare questo file.

Regole (nel dubbio si ritorna None = testo grezzo):
- `$(`, backtick, `$'`, `<(`/`>(`: sostituzione di comando o ANSI-C -> None.
- Ogni parola-comando deve stare in INERTI o essere `git`; un comando che comincia con
  `$`, un'interprete (bash, eval, xargs, python, sudo, ...) o una parola ignota -> None.
- `git` vale solo col sottocomando SUBITO dopo (niente -c/-C/--config-env prima) e in
  GIT_LETTURA; se sulla riga c'e' anche una redirezione `>` -> None (R-318-1: scrivere
  .git/config e poi `git <alias>` nello stesso comando crea un commit).
- Un'assegnazione (VAR=...) -> None (GIT_CONFIG_* per la riga, R-318-1).
- Un `#` fuori dagli apici (commento di bash, anche dopo `>`) -> None (R-319-1,
  R-320-2: `echo x #'` a capo `git ...` a capo `#'` sembra una stringa, ma bash
  esegue la riga di mezzo).
- Un `$` fuori dagli apici singoli -> None, anche fra doppi apici e nei corpi di heredoc
  col delimitatore non quotato (R-320-1: `${x@P}` esegue senza `$(`; niente elenco di
  espansioni "pericolose", si rifiutano tutte).
- Un delimitatore di heredoc seguito da altro che non sia spazio/separatore -> None.
- Backslash, `* ? [ ] { } ~` fuori dagli apici -> None (R-321-1: `test -v a[\$\(...\)]`).
- printf non e' inerte (R-320-1: `printf "-v" x '\x24(...)'` costruisce codice).
- Il contenuto fra apici si toglie solo se il comando che lo riceve e' INERTE; per `git`
  (e per gli apici dentro la parola-comando stessa) resta intero.
- Il corpo di un heredoc si toglie solo se il comando che lo apre e' INERTE.
- Apice o heredoc non chiuso -> None.
"""
from __future__ import annotations

import re
import sys

PATTERN = re.compile(r"git[ \t\n\r\f\v].*commit")  # come grep -E, riga per riga

# Comandi che non eseguono i propri argomenti ne' lo stdin. NON ci sono sed/awk (sed
# 's/x/y/e' e system() eseguono), find (-exec), xargs, env, sudo, gli interpreti,
# alias/export/declare (definiscono cio' che si esegue dopo), rg (--pre) e sort
# (--compress-program) che eseguono programmi (R-318-2), ne' chi scrive file
# (tee/cp/mv/ln/chmod/mkdir/touch/rm: R-318-1).
INERTI = frozenset({
    # R-321-1 (taglio radicale, consiglio del revisore dopo quattro bypass): solo i
    # comandi dei tre inneschi reali e pochi altri che non valutano niente. Fuori test/[
    # (test -v valuta indici di array), printf, jq, diff, stat, file, column, ...
    "echo", "cat", "grep", "egrep", "fgrep", "head", "tail", "wc", "ls",
    "cd", "pwd", "true", "false",
})
# Sottocomandi git di sola lettura: sulla riga del gate sono gli unici ammessi.
GIT_LETTURA = frozenset({
    "log", "status", "diff", "show", "rev-parse", "ls-files", "ls-tree", "cat-file",
    "blame", "shortlog", "describe", "rev-list", "merge-base", "grep",
})
CHIAVI = frozenset({"if", "then", "else", "elif", "fi", "do", "done", "while", "until",
                    "!", "{", "}", "time"})
SEPARATORI = ";&|()\n"
_ASSEGNAZIONE = re.compile(r"[A-Za-z_][A-Za-z0-9_]*=")


class _Ignoto(Exception):
    """Costrutto non gestito: si torna al testo grezzo."""


def scheletro(cmd: str) -> str | None:
    """Il comando senza le stringhe e gli heredoc inerti; None se non si sa."""
    if any(t in cmd for t in ("$(", "`", "$'", "<(", ">(")):
        return None
    try:
        return _scheletro(cmd)
    except _Ignoto:
        return None


def _scheletro(cmd: str) -> str:
    out: list[str] = []
    comando: str | None = None   # parola-comando del comando semplice corrente
    attesa_sub = False           # la prossima parola e' il sottocomando di git
    ha_git = ha_redirezione = False
    parola: list[str] = []       # parola in costruzione
    heredoc: list[tuple[str, bool, str | None]] = []  # (delimitatore, strip tab, padrone)
    i, n = 0, len(cmd)

    def chiudi_parola() -> None:
        nonlocal comando, attesa_sub, ha_git
        if not parola:
            return
        w = "".join(parola)
        parola.clear()
        if attesa_sub:
            attesa_sub = False
            if w not in GIT_LETTURA:
                raise _Ignoto(f"git {w}")
            return
        if comando is not None:
            return
        if w in CHIAVI:
            return
        if _ASSEGNAZIONE.match(w) or w.startswith(("$", "<", ">")) or \
                (w != "git" and w not in INERTI):
            raise _Ignoto(w)
        comando = w
        if w == "git":
            ha_git = attesa_sub = True

    while i < n:
        c = cmd[i]
        if c == "\\" or c in "*?[]{}~":
            # R-321-1: backslash fuori dagli apici (\$ rivalutato da un builtin) e
            # globbing/brace/tilde: nessuna di queste forme serve agli inneschi reali.
            raise _Ignoto("backslash o espansione di percorso")
        if c in "#$":
            raise _Ignoto("commento o espansione")
        if c in "'\"":
            fine = i + 1
            while True:
                if fine >= n:
                    raise _Ignoto("apice non chiuso")
                if cmd[fine] == c:
                    break
                fine += 2 if (c == '"' and cmd[fine] == "\\") else 1
            testo = cmd[i:fine + 1]
            if c == '"' and "$" in testo:
                raise _Ignoto("espansione fra doppi apici")
            # Dentro la parola-comando (comando ancora ignoto) o per git: intero.
            inerte = comando is not None and comando != "git"
            out.append(c + c if inerte else testo)
            parola.append(testo)
            i = fine + 1
            continue
        if cmd.startswith("<<", i) and not cmd.startswith("<<<", i):
            m = re.compile(r"<<(-?)[ \t]*(['\"]?)([A-Za-z0-9_.-]+)\2").match(cmd, i)
            if not m or (m.end() < n and cmd[m.end()] not in " \t" + SEPARATORI):
                raise _Ignoto("heredoc")
            chiudi_parola()
            heredoc.append((m.group(3), m.group(1) == "-",
                            comando if m.group(2) else None))
            out.append(m.group(0))
            i = m.end()
            continue
        if c == ">":
            ha_redirezione = True
        if c in " \t":
            chiudi_parola()
            out.append(c)
            i += 1
            continue
        if c in SEPARATORI:
            chiudi_parola()
            out.append(c)
            i += 1
            comando = None
            if c == "\n" and heredoc:
                i = _salta_corpi(cmd, i, heredoc, out)
                heredoc.clear()
            continue
        parola.append(c)
        out.append(c)
        i += 1
    chiudi_parola()
    if heredoc:
        raise _Ignoto("heredoc senza corpo")
    if attesa_sub:
        raise _Ignoto("git senza sottocomando")
    if ha_git and ha_redirezione:
        raise _Ignoto("git e redirezione nello stesso comando")
    return "".join(out)


def _salta_corpi(cmd: str, i: int, heredoc: list[tuple[str, bool, str | None]],
                 out: list[str]) -> int:
    """Consuma i corpi degli heredoc aperti sulla riga; li tiene solo se il padrone non e'
    inerte. Ritorna l'indice dopo l'ultimo delimitatore."""
    for delim, strip_tab, padrone in heredoc:
        inerte = padrone is not None and padrone != "git"
        while True:
            if i >= len(cmd):
                raise _Ignoto("heredoc non chiuso")
            fine = cmd.find("\n", i)
            fine = len(cmd) if fine < 0 else fine + 1
            riga = cmd[i:fine]
            i = fine
            if (riga.rstrip("\n").lstrip("\t") if strip_tab else riga.rstrip("\n")) == delim:
                out.append(riga)
                break
            if not inerte:
                out.append(riga)
    return i


def e_commit(cmd: str) -> bool:
    """True se il comando va trattato come commit (o non si sa)."""
    base = scheletro(cmd)
    testo = cmd if base is None else base
    return any(PATTERN.search(riga) for riga in testo.split("\n"))


if __name__ == "__main__":
    sys.exit(0 if e_commit(sys.stdin.read()) else 3)
