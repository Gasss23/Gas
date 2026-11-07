# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-11-07 — Sottofondo: seconda fetta di riserve BASSE (bot #346) (chat M2, coordinata da M1)

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR di questa fetta: per decisione dell'operatore (via M1, 7 nov, operatore assente ~4 ore) le PR nuove si mergiano da sole solo con verdetto APPROVATO pulito; con riserve restano aperte e le decide l'operatore al rientro.
2. Prova sul Mac (dalla #345): a voce un compito lungo → «ci lavoro» e poi avviso su Telegram.

---

## §1 SCOPE & ESITO FETTE

- **PR #346** (prima fetta BASSE del sottofondo): `MERGIATA` (c523a04) col sì dell'operatore via M1, dopo due merge di main nel branch (#341 e #347 di Mani, conflitti solo in report e memoria; review #704-M2 e #705-M2 APPROVATO).
- **Seconda fetta BASSE del sottofondo**: `FATTA` — compito appena riuscito non riscritto «ko» e niente avviso «non è finito» (bot #346 V-1 su 3ee02dd e 0c836f9); riga nel prompt del processo in sottofondo «avvisa_operatore qui non esiste» (bot #346 V-1 su 2d0977e, V-4 su 0c836f9); pulizia dei compiti vecchi anche da `controlla()`, al massimo una volta l'ora (bot #346 V-3 su 2d0977e); test «data futura + processo estraneo» (R-703-1-M2). Review #706-M2 APPROVATO CON RISERVE (R-706-1/2-M2 BASSE).
- **Prossimo passo della roadmap voce** (ordine di M1 dopo questa fetta): `DA FARE`.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |  2 +
 gas.py                             |  4 ++
 modules/sottofondo/__init__.py     | 27 +++++++++---
 reports/diff_sessione.md                        | n/d
 reports/handoff.md                              | n/d
 reports/ripartenza_m2.md                        | n/d
 reports/stato_progetto.md                       | n/d
 reports/ultimo_report.md                        | n/d
 tests/test_unit_kernel.py          |  4 +-
 tests/test_unit_sottofondo.py      | 84 ++++++++++++++++++++++++++++++++++++++
```

NB: regola «n/d» — i report si scrivono in questo stesso commit di fine task; riga di totale tolta. Base: origin/main c523a04 (merge della #346).

## §3 GIT LOG --ONELINE (sessione)

```
135535e fix(sottofondo): compito riuscito non diventa «ko», prompt del figlio senza avvisa_operatore, pulizia anche da controlla(), test R-703-1 (bot #346 V-1/V-3) (sì dell'operatore via M1)
0898dd1 chore(revisore): memoria review #706 — APPROVATO CON RISERVE
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione.

## §4 VERDETTO DEL REVISORE (per commit motore)

Review #706-M2 sul commit 135535e (verdetto integrale):

## VERDETTO: APPROVATO CON RISERVE

Review #706-M2: diff in staging (`git diff --cached`) su feat/voce-v12-m2, HEAD 0c836f9, 4 file, +112/−7. Ho letto CLAUDE.md (già nel contesto), le voci del sottofondo in `reports/stato_progetto.md` e le lezioni recenti della mia memoria. Niente git stash: per i mutanti ho usato un worktree nello scratchpad, poi rimosso.

**Cosa ho guardato nel diff:**
- `modules/sottofondo/__init__.py:345`: ora `annulla` mette «ko» solo ai compiti ancora in_coda o in_corso e ritorna True se li ha chiusi. Il posto in coda si libera comunque se è dello stesso id. Rischio esaminato: un compito «ok» che resta con la coda bloccata. Non succede, lo sblocco del posto non dipende dallo stato. Esito: ok.
- `modules/sottofondo/__init__.py:190`: `_ripulisci` avvisa solo se `annulla` ha chiuso il compito. Rischio esaminato: avvisi persi quando il file del compito manca. Il comportamento è lo stesso di prima: niente file del compito, niente avviso. Esito: ok.
- `modules/sottofondo/__init__.py:269`: `controlla` lancia `_pulisci_vecchi` al massimo una volta l'ora per processo, solo se la cartella esiste, dentro il try/except già presente (§9 rispettato). La prima chiamata pulisce subito: costa un solo elenco della cartella. Esito: ok.
- `gas.py:4582`: la riga «SEI UN COMPITO IN SOTTOFONDO» viene aggiunta a `system_prompt`. Rischio esaminato: che il prompt venga ricostruito e la riga si perda. Non succede: `system_prompt` si assegna solo in `__init__` (gas.py:1120) e si usa a gas.py:5036. Non tocca `_get_window` né la finestra della storia. Esito: ok.
- `tests/test_unit_kernel.py:11934` e `tests/test_unit_kernel.py:11948`: T106a controlla che la riga ci sia nel processo in sottofondo, T106c che manchi nei turni normali. Esito: ok.
- `tests/test_unit_sottofondo.py:640`: la corsa è simulata col monkeypatch su `sf.annulla`. Funziona perché `_ripulisci` cerca `annulla` nel modulo a ogni chiamata. Esito: ok.

**Contesto (file non toccati):** gli altri chiamanti di `annulla` sono `modules/sottofondo/__init__.py:394`, `modules/sottofondo/__init__.py:413` e `gas.py:4619`. Ignorano il valore di ritorno, ed è corretto.

**Prove eseguite:**
- `tests/test_unit_sottofondo.py`: 67 passed.
- Mutante «annulla senza il controllo sullo stato»: 3 test falliti, preso.
- Mutante «pulizia a ogni chiamata, senza il limite di un'ora»: 1 test fallito, preso.
- Wall of Shame: nessun taglio diretto della storia, nessuna simulazione di tool. Cap 10 iterazioni e cap 8k non toccati.

**Riserve:**
- R-706-1-M2 BASSA: la corsa in `annulla` è ridotta ma non chiusa. Il file viene letto e poi riscritto senza lock: se il figlio scrive «ok» fra `_leggi` e `_scrivi_privato`, viene ancora sovrascritto con «ko». Basta dichiararlo; un lock su file sarebbe sproporzionato per una riserva BASSA.
- R-706-2-M2 BASSA: in `esegui` (`modules/sottofondo/__init__.py:394`), un'eccezione arrivata dopo che `_esegui` ha già scritto «ok» (per esempio un OSError diverso da FileNotFoundError durante l'unlink) ora lascia il compito «ok». Però all'operatore parte lo stesso «si è interrotto per un errore interno», in contraddizione con lo stato. Rimedio possibile: in quel ramo avvisare solo se `annulla` ha ritornato True.

**Non verificato:**
- La corsa vera fra due processi (figlio reale contro `controlla` del kernel): l'ho controllata solo con la simulazione via monkeypatch, perché una corsa fra processi in dev non si riproduce in modo deterministico.
- La suite completa del kernel (1100 PASS dichiarati): non l'ho rilanciata, ho letto solo T106a/c.
- Il comportamento sul Mac o sulla VPS.

**Memoria:** ho aggiunto in coda a `/home/user/Gas/.claude/agents/memoria_revisore.md` la riga contatore #706-M2 e una lezione (un «controlla lo stato prima di sovrascrivere» senza lock restringe la corsa ma non la chiude; verificare i chiamanti che ignorano il nuovo valore di ritorno). Commit 0774cd7 fatto con `commit_memoria_revisore.sh`; il diff in staging è rimasto com'era (4 file, +112/−7).

## §5 DELTA TEST DEL MOTORE

`tests/test_unit_kernel.py` T106a ora controlla anche la riga «SEI UN COMPITO IN SOTTOFONDO» nel prompt del processo in sottofondo (round-trip §7: chiamata negata, risposta finale), T106c che manchi nei turni normali. Suite kernel `=== RIEPILOGO: 1100 PASS, 0 FAIL ===`. `tests/test_unit_sottofondo.py`: 67 passed (prima 62): compito appena riuscito resta «ok» senza avviso, `annulla` chiude solo compiti aperti, corsa simulata (figlio che finisce durante la pulizia), pulizia da `controlla` una volta l'ora, data futura + processo estraneo. Con il modulo di prima i test nuovi danno 3 failed; mutante «avviso sul compito letto prima» → 1 failed.

## §6 STATO CI

`gh` non autenticato nel cloud. I commit sono pushati insieme a questo report: run non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- R-706-1-M2 BASSA: la corsa in `annulla` è ristretta ma non chiusa (lettura e riscrittura senza lock).
- R-706-2-M2 BASSA: in `esegui`, un'eccezione dopo che il compito è già «ok» manda comunque «si è interrotto per un errore interno».
- R-701-3-M2 BASSA / bot #346 V-3 (0c836f9): con un compito in corso ogni turno lancia `ps`; due processi che controllano insieme un figlio morto possono mandare due avvisi.
- R-703-2-M2 / bot #346 V-2 (0c836f9) BASSA: con «creato» nel futuro e identità ignota la durata massima non vale finché l'orologio non raggiunge quella data.
- R-696-1-M2, ve #345 V-2, bot #345 V-3: BASSE, invariate.
- Non verificato in dev: processo vero con `claude -p`, avviso Telegram vero, `ps -ww` su macOS.
