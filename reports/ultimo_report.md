# Report — Sfoltimento CLAUDE.md + Config frugale Claude Code
Data: 2026-06-24

## DECISIONI UMANE RICHIESTE
Nessuna.

---

## FETTA 1 — Sfoltimento CLAUDE.md (SPOSTA, non cancellare)

**Esito: ✅ COMPLETATA**

- Creato `reports/roadmap.md` con intestazione breve e INTERA sezione §10 originale.
- Rimosso da CLAUDE.md il contenuto verboso di §10 (51 righe, righe 61–111 del file originale).
- Inserito al suo posto un sommario compatto di 12 righe: 5 FASI a una riga + 3 item aperti TOP + puntatore a reports/roadmap.md.
- NON toccate le sezioni 1–9 e §11 DISCIPLINA TOKEN.
- NON toccati reports/stato_progetto.md né reports/stato_storico.md.

**Prova di zero-perdita:**
- Righe spostate da CLAUDE.md: 51 (contenuto §10, righe 61–111)
- Righe in reports/roadmap.md: 51 (contenuto §10 identico + 1 riga intestazione = 52 totali nel file)
- Controllo: ogni paragrafo, voce, item numerato e sotto-sezione (FASE 1, FASE 2, FASE 3, FASE 4, FASE 5, item aperti, idee) è presente integralmente in reports/roadmap.md. Nessun contenuto eliminato, solo spostato.

---

## FETTA 2 — .claude/settings.json (MERGE, preserva l'esistente)

**Esito: ✅ COMPLETATA**

Aggiunti in cima al file (prima di "hooks"):
- `"model": "claude-sonnet-4-6"`
- `"env": { "DISABLE_NON_ESSENTIAL_MODEL_CALLS": "1" }`

Hook esistenti preservati intatti: SessionEnd (session_end.sh), PreToolUse/Bash (review_gate.sh), Stop (scrivi_rep.sh).

---

## FETTA 3 — Hook SessionStart+compact (MERGE negli hook)

**Esito: ✅ COMPLETATA**

Aggiunto hook `SessionStart` con matcher `compact` che emette via stdout le 4 regole critiche:
1. Revisore obbligatorio prima di ogni commit che tocca il motore
2. Fare SOLO lo scope dato — se serve altro, scrivere in DECISIONI UMANE RICHIESTE
3. Reporting canonico obbligatorio (ultimo_report.md + hash + cat + diff --stat)
4. Nessuna operazione irreversibile nel loop

Hook esistenti NON toccati (SessionEnd, PreToolUse, Stop).

---

## FETTA 4 — Custom command /fine-task

**Esito: ✅ COMPLETATA**

Creata directory `.claude/commands/` (non esisteva).
Creato `.claude/commands/fine-task.md` con:
- Istruzioni step-by-step del reporting canonico
- Formato commit corretto (solo doc, no motore)
- Stampa obbligatoria: path + hash + cat integrale + git diff --stat
- Invariante esplicita: nessun riassunto verbale diverso dal file

---

## RIEPILOGO FILE TOCCATI

| File | Operazione |
|------|-----------|
| `CLAUDE.md` | §10 sostituita con sommario compatto (−39 righe nette) |
| `reports/roadmap.md` | CREATO — contiene §10 integrale |
| `.claude/settings.json` | Aggiunti model + env + hook SessionStart/compact |
| `.claude/commands/fine-task.md` | CREATO — comando /fine-task |
| `reports/ultimo_report.md` | QUESTO FILE |

Nessun file del motore (gas.py, brains/, modules/, tests/) toccato → revisore NON invocato (corretto per task doc/.claude/).
