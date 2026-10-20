# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-10-20 (dopo il merge di #226) — catalogo delle fonti alla firma, taglio degli avvisi, lavoro in parallelo

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR: l'agente mergia da solo solo con un APPROVATO pulito del bot (CLAUDE.md §10); altrimenti decide l'operatore.
2. Togliere dal progetto claude.ai le copie di `briefing_architettura_voce.md` e `recinto_autonomia.md` (l'agente non vi ha accesso).

---

## §1 SCOPE & ESITO FETTE

- **R-383-1 (taglio dei valori negli avvisi)**: `FATTA` — review #384 APPROVATO CON RISERVE.
- **Roadmap 5.3 (knowledge/ alla firma) + cosmetiche bot #226**: `FATTA` — review #385 APPROVATO.
- **Regole del lavoro in parallelo** (`reports/lavoro_parallelo.md`): `FATTA` (solo documento).

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   2 ++
 gas.py                             |  14 +++-----------
 modules/gate/gate.py               |   8 ++++++++
 modules/memory/store.py            |   4 ++--
 modules/telegram/bot.py            |  18 ++++++++++++++++--
 reports/diff_sessione.md           |  15 ++++++++-------
 reports/handoff.md                 | 179 +++++++++++++++++++++++++++++++++++++++++++++++++----------------------------------------------------------------------------------------------------------------------------------
 reports/lavoro_parallelo.md        |  24 ++++++++++++++++++++++++
 reports/stato_progetto.md          |   2 ++
 reports/ultimo_report.md           |  14 +++++++-------
 tests/test_unit_gate.py            |   5 ++++-
 tests/test_unit_kernel.py          |  24 ++++++++++++++++++++++++
 12 files changed, 149 insertions(+), 160 deletions(-)
```

---

## §3 GIT LOG --ONELINE (sessione)

```
f4f730e docs(fine-task): report e handoff — knowledge/ alla firma; regole del lavoro in parallelo
48764e0 feat(cancello): il catalogo delle fonti di studio (knowledge/) va alla firma (roadmap 5.3)
f2308de chore(revisore): memoria review #385 — APPROVATO
6e8b0ff Merge remote-tracking branch 'origin/main' into feat/merge-automatico-z1xjx2
71074ca fix(avvisi): taglio dei valori che non nasconde il testo dopo un «<» (R-383-1)
8dc72d5 chore(revisore): memoria review #384 — APPROVATO CON RISERVE
```

---

## §4 VERDETTO DEL REVISORE (per commit motore)

### Review #384

## VERDETTO: APPROVATO CON RISERVE

Review #384. Diff STAGED su feat/merge-automatico-z1xjx2 (PR #226): gas.py, modules/telegram/bot.py, tests/test_unit_kernel.py. Ho letto prima CLAUDE.md (sezioni 5, 8, 9), reports/stato_progetto.md (riga 591, R-383-1) e la memoria del revisore (#381-#383).

**Elementi del diff esaminati**
- `modules/telegram/bot.py:153`: nuova `tronca_visibile(testo, n)`. Fa `rendi_visibili` su una riga, taglia a n e aggiunge «…».
  - Rischio esaminato: una sequenza spezzata, oppure un «<» letterale che cancella il valore.
  - Il «<» si cerca solo negli ultimi 10 caratteri (riga 161). La sequenza più lunga che `rendi_visibili` può produrre è «<U+10FFFF>», 10 caratteri (categorie Cn/Co fino a 0x10FFFF), quindi una parte spezzata ne ha al massimo 9 e la finestra la copre sempre.
  - Sonda eseguita: caratteri U+202E, U+10FFFF, U+E01EF e U+0000, ciascuno in 30 posizioni, con n = 10, 60, 120 e 200. Risultato: 0 sequenze spezzate, lunghezza sempre al massimo n+1.
  - Un «<» letterale in tutte le posizioni da 0 a 204 fa perdere al massimo 9 caratteri: il valore resta visibile. Per questi casi il codice non può più alzare eccezioni.
  - Esito: ok.
- `gas.py:2585`: `_v` dell'avviso lead ora delega a `tronca_visibile(x or "—", 200)`. Comportamento uguale a prima (prima `str(x or "—")`, ora lo `str()` lo fa la funzione nuova). Rischio esaminato: regressione su R-382-2 e R-383-1. Esito: ok.
- `modules/telegram/bot.py:303`: `componi_avviso_scadute` passa da tagli grezzi `[:120]`/`[:60]` a `tronca_visibile`. Rischio esaminato: un messaggio più lungo di prima (al massimo un carattere in più per campo, il «…»), trascurabile rispetto al limite di 4096 con al massimo `MAX_SCADUTE_ELENCATE` righe. Esito: ok.
- `tests/test_unit_kernel.py:6084`: test R-383-1 («<» all'inizio e in mezzo).
- `tests/test_unit_kernel.py:6095`: test V-2 VE #226 (taglio a 120 in ogni punto della sequenza).
  - Mutazioni in un worktree separato, rimosso dopo l'uso; nessun git stash.
  - (a) Ripristinato `rfind("<")` su tutto il taglio: fallisce solo il test R-383-1.
  - (b) Ripristinato il taglio grezzo `[:120]` sull'azione: fallisce solo il test V-2. La lista mostra 9 posizioni su 11 rotte.
  - Esito: ok.

**Riprodotto**: kernel 943 PASS 0 FAIL; `pytest tests/` 1523 passed. Nessuna violazione della sezione 5 di CLAUDE.md: nessuno slicing della history, nessuna simulazione di tool. Le funzioni sono pure, senza I/O.

**Riserve**
- R-384-1 COSMETICA: nessun test dedicato per il taglio del `tool_name` a 60 (`modules/telegram/bot.py:304`). Il codice è lo stesso già coperto, quindi il rischio è minimo.

**Rischio escluso**: non ho verificato la resa reale su Telegram (come il client mostra «<U+…>» e «…»), perché in ambiente di sviluppo non c'è un bot attivo. Non ho controllato nemmeno i chiamanti di `rendi_visibili` fuori dal diff, perché non sono cambiati.

**Memoria**: aggiunta la riga #384 (APPROVATO CON RISERVE, nessuna lezione nuova) in /home/user/Gas/.claude/agents/memoria_revisore.md e committata da sola con lo script (commit 8dc72d5). Il diff staged sotto review resta intatto. R-383-1 e V-2 VE #226 si possono considerare chiuse; R-384-1 va tracciata in /home/user/Gas/reports/stato_progetto.md.

### Review #385

## VERDETTO: APPROVATO

Ho letto CLAUDE.md, la parte di reports/stato_progetto.md che serve e la memoria del revisore. Ho esaminato il diff staged: 5 file, +23 e -4 righe.

**Elementi del diff esaminati**
- `modules/gate/gate.py:455`: ogni percorso il cui primo pezzo (pulito) inizia con «knowledge» ora richiede la firma. Volevo capire se si può aggirare. Ho provato a mano sette varianti, tutte finite alla firma (livello 2): `knowledge\sources.yaml` (barra rovesciata), `KNOWLEDGE /x`, `./knowledge`, `knowledge` da solo, `x/../knowledge/sources.yaml`, `Knowledge%2fsources.yaml` e la «k» a larghezza piena. Il controllo sta dopo quelli di livello 3, quindi non rende più libero nessun percorso che prima era «mai». I collegamenti simbolici sono coperti: l'esecuzione rivaluta il file vero (`gas.py:3736`). — ok
- `modules/gate/gate.py:264`: nuova costante `_LIVELLO2_TOP`, con commento motivato e tipi dichiarati. Vale solo per il primo pezzo, quindi `dati/knowledge/x.md` resta libero (livello 1, sondato): è voluto e coerente con la roadmap 5.3. — ok
- `tests/test_unit_gate.py:485`: sei casi nuovi alla firma. Il caso «knowledge/x.md», che prima era libero, ora è alla firma e al suo posto tra i liberi c'è `dati/knowledge.md`. È un cambio di comportamento voluto, non un test indebolito. Rilanciati: 697 passed. — ok
- `tests/test_unit_kernel.py:5960`: test di round-trip agentico. `write_file knowledge/sources.yaml` senza letture non scrive il file. Il test distingue il vecchio comportamento: prima la cartella knowledge era libera, quindi il file sarebbe stato scritto. Rilanciato: 944 PASS, 0 FAIL, e il caso «roadmap 5.3» è PASS. — ok
- `modules/memory/store.py:1983` e `modules/memory/store.py:1993`: cambia solo il testo dei log (`scadi_approvazioni`), la logica resta uguale e l'errore resta intercettato e loggato con ritorno `[]`. — ok
- `gas.py:4358`: solo il commento passa da «12.» a «11b.». — ok
- Contesto: in `gas.py:1628` la cartella del progetto è montata in sola lettura nella sandbox di `run_command`. Quindi `knowledge/` non si può scrivere nemmeno da shell. — ok

**Coerenza col progetto:** chiude il punto 5.3 della roadmap («da chiudere presto»). Rafforza il guardrail, non lo indebolisce. Non tocca i guardrail su cronologia (`_get_window`), limite di 10 iterazioni e tetto di output, né la gestione degli errori dei provider. Nessun taglio diretto della cronologia e nessun output di tool simulato.

**Rischi esclusi esplicitamente**
- Non ho fatto la prova di mutazione del test kernel, cioè ripristinare temporaneamente il livello 1 e vederlo fallire: il divieto di `git stash` e le modifiche staged la rendevano invasiva. Mi baso sul ragionamento: il vecchio test del gate metteva knowledge tra i liberi.
- Non ho verificato se il database `.gas_knowledge.db`, che non sta nella cartella `knowledge/`, sia scrivibile da Gas tramite una pipeline di ingest. È fuori dal perimetro di questo diff.
- Non ho verificato il comportamento sulla VPS: non è riproducibile in sviluppo.

**Memoria:** riga contatore #385 aggiunta in `/home/user/Gas/.claude/agents/memoria_revisore.md` e committata da sola (commit f2308de, «chore(revisore): memoria review #385 — APPROVATO»). Il diff staged è rimasto intatto (5 file). Nessuna lezione nuova.

---

## §5 DELTA TEST DEL MOTORE

tests/test_unit_kernel.py in locale: 941 → 944 PASS, 0 FAIL. Blocco reale: `=== RIEPILOGO: 944 PASS, 0 FAIL ===`. In CI i conteggi sono +2 (test del profilo sandbox saltati in locale).
pytest `tests/`: `1529 passed in 182.37s (0:03:02)` (+6 gate).

## §6 STATO CI

- Run sui commit di questo handoff: non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- R-384-1 (COSMETICA): nessun test dedicato al taglio del tool_name a 60 negli avvisi delle firme scadute.
- Da #226: R-381-x chiuse; da #225: R-380-1, R-380-2; da #224: R-378-1, R-379-1, R-ve224-2; da #222: vedi stato_progetto.md.
