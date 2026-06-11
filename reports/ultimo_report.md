# Report sessione 2026-06-11 — Le tre istituzioni di processo (A, B, C)

Ripresa dopo limite. CHECK iniziale: working tree pulito sull'auto-commit
`4c6fc3d`, ma **nessuna delle tre istituzioni esisteva** (niente
stato_progetto.md, niente diff_sessione.md, niente .claude/agents/).
Create tutte e tre da zero, con l'upgrade "memoria del revisore".

## Cosa è stato fatto

1. **Validazione preliminare** (inizio sessione): eseguita
   `tests/test_unit_kernel.py` rimasta non verificata nell'auto-commit di
   ieri → **20 PASS, 0 FAIL**. Fix `_get_window` validato. Confermato il
   finding T10 (path traversal in write_file, escape riuscito).

2. **Istituzione A — `reports/stato_progetto.md`**: fotografia viva dello
   stato (motore validato, pipeline provider, finding aperti, prossimi
   passi). Da aggiornare a fine di ogni task.

3. **Istituzione B — `reports/diff_sessione.md`**: riepilogo del diff a
   fine sessione (file toccati, cosa e perché). Scritto per la sessione
   odierna; si riscrive a ogni sessione.

4. **Istituzione C — subagent revisore** (`.claude/agents/revisore.md`)
   con MEMORIA DEL REVISORE:
   - PRIMA di ogni review legge obbligatoriamente CLAUDE.md (sez. 5 Wall
     of Shame in primis), reports/stato_progetto.md e
     .claude/agents/memoria_revisore.md; giudica anche la coerenza col
     progetto e la roadmap, non solo la correttezza tecnica.
   - DOPO ogni review aggiunge a memoria_revisore.md le eventuali lezioni
     nuove (1-3 righe, datate, niente prolissità).
   - Creata `.claude/agents/memoria_revisore.md` vuota con intestazione.

5. **CLAUDE.md sezione 3** aggiornata: le tre istituzioni sono ora nel
   canone permanente.

## Stato finale

- Tre istituzioni operative, canone aggiornato, stato_progetto.md
  allineato allo stato reale.
- Nessuna modifica al codice del motore (gas.py intatto in questa
  sessione).
- Tutto committato e pushato (hash nel messaggio a terminale, regola
  anti-discrepanza rispettata con cat integrale di stato_progetto.md e di
  questo report).

## Prossimi candidati (invariati, da stato_progetto.md)

1. Fix path traversal in write_file (T10) + promozione del test a check
   bloccante.
2. Snapshot preventivo dei file (anti-autodistruzione).
3. Modalità dry-run.
4. Cap dedicato per pipeline Whisper.
