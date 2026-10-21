# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-10-20 (dopo il merge di #230) — avviso sui file delicati più preciso

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR: l'agente mergia da solo solo con un APPROVATO pulito del bot (CLAUDE.md §10); altrimenti decide l'operatore.
2. Togliere dal progetto claude.ai le copie di `briefing_architettura_voce.md` e `recinto_autonomia.md` (l'agente non vi ha accesso).

---

## §1 SCOPE & ESITO FETTE

- **R-387-1 + V-1/V-2 verifica esterna e bot #230**: `FATTA` — review #388 (chat Motore) APPROVATO CON RISERVE.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   4 +++-
 gas.py                             |   4 +++-
 modules/gate/gate.py               |  23 ++++++++++++++++++++---
 modules/telegram/bot.py            |  14 ++++++++++++++
 reports/diff_sessione.md           |  18 ++++++++----------
 reports/handoff.md                 | 136 +++++++++++++++++++++++++---------------------------------------------------------------------------------------------------------------
 reports/stato_progetto.md          |   2 ++
 reports/ultimo_report.md           |  34 +++++++---------------------------
 tests/test_unit_gate.py            |   6 ++++++
 tests/test_unit_kernel.py          |  27 +++++++++++++++++++++++++--
 10 files changed, 113 insertions(+), 155 deletions(-)
```

---

## §3 GIT LOG --ONELINE (sessione)

```
8cd30bc Merge origin/main (#229, chat Voce) in feat/merge-automatico-z1xjx2
d0df835 fix(avvisi): file delicati riconosciuti su tutto il nome e nome del file sempre visibile (R-387-1, V-1 bot #230)
e36b46c chore(revisore): memoria review #388 — APPROVATO CON RISERVE
```

---

## §4 VERDETTO DEL REVISORE (per commit motore)

### Review #388 (chat Motore)

## VERDETTO: APPROVATO CON RISERVE

Ho letto CLAUDE.md (sezione 5 e le altre), la parte di reports/stato_progetto.md che riguarda #228 e R-387-1, e la mia memoria (.claude/agents/memoria_revisore.md). Ho riprodotto i risultati dichiarati: kernel 949 PASS 0 FAIL, gate 736 passed, pytest tests/ 1573 passed. Il diff non tocca `_get_window`, il limite di 10 iterazioni, il limite di 8k sull'output né la storia. Non c'è slicing della storia né output simulato dei tool.

**Elementi esaminati**
- `modules/gate/gate.py:541`: un'estensione interna delicata («a.sh.txt», «x.py.md») ora fa scattare l'avviso. Rischio esaminato: falsi positivi sui documenti normali. Ho controllato report.2026.md, v1.2.txt, backup.2026-10.zip, archivio.tar.gz e foto.jpeg.md: tutti restano False. Estensioni corte come «c», «r» e «app» segnalano anche nomi come piano.c.md, ma l'avviso è solo informativo. Esito: ok.
- `modules/gate/gate.py:547`: le parole intere ora si cercano su tutto il nome tranne l'ultima estensione. Il nome arriva già in minuscolo (ID_RSA.TXT, X.SECRET.md → True). Se c'è un errore il risultato è True, quindi non si rompe nulla (regola §9). Esito: riserva R-388-1 (sotto).
- `modules/telegram/bot.py:167` (`tronca_visibile_coda`): taglia il testo tenendo la coda. Rischio esaminato: tagliare a metà una sequenza «<U+XXXX>», oppure che un «>» scritto davvero nel nome cancelli troppo testo. Ho provato 4 caratteri invisibili (anche U+10FFFF e U+E01EF) in 40 posizioni, con lunghezze 10, 50 e 200: nessuna sequenza spezzata. Un «>» vero vicino all'inizio fa perdere al massimo 9 caratteri, perché la ricerca guarda solo i primi 10 (rispetta la lezione #383). Esito: ok, con la nota cosmetica R-388-2.
- `gas.py:2656`: l'avviso dei file usa ora `tronca_visibile_coda(p, 200)`. Il ciclo che accorcia il messaggio sotto `TELEGRAM_MAX_CHARS` resta com'era. Esito: ok.
- `tests/test_unit_kernel.py:6002`: il nuovo test abbassa il limite a 1500 e lo ripristina in un `finally`. Funziona perché `gas.py` legge `_tg_bot.TELEGRAM_MAX_CHARS` dal modulo al momento della chiamata. Esito: ok.
- Prova delle mutazioni, fatta in un worktree temporaneo nella scratchpad (niente git stash, worktree poi rimosso). Ho rimesso il taglio dalla testa al posto della coda e spento il controllo delle estensioni interne: falliscono 2 test T74b5 e 2 casi di test_sembra_delicato. I test colgono davvero i due difetti.

**Riserve**
- **R-388-1 BASSA**: l'ultima estensione non viene confrontata con le parole delicate. Quindi `x.secret`, `github.token` e `aws.credentials` restano False. Non è una regressione: era così anche prima.
- **R-388-2 COSMETICA**: `tronca_visibile_coda(t, 0)` restituisce il testo intero, perché `t[-0:]` prende tutto. Oggi nessun chiamante passa 0, ma conviene una protezione per n<=0.

**Cosa NON ho verificato**: la resa reale su Telegram (come il client mostra «…» seguito dalla coda del percorso). Non si riproduce qui: c'è solo il finto `_TgFinto`, nessun bot vero.

Memoria: ho aggiunto la riga #388 e la lezione (t[-n:] con n=0 prende tutto) in .claude/agents/memoria_revisore.md. Commit e36b46c fatto con scripts/commit_memoria_revisore.sh.

---

## §5 DELTA TEST DEL MOTORE

tests/test_unit_kernel.py in locale: 947 → 949 PASS, 0 FAIL. Blocco reale: `=== RIEPILOGO: 949 PASS, 0 FAIL ===`. In CI i conteggi sono +2 (test del profilo sandbox saltati in locale).
pytest `tests/`: `1573 passed in 175.84s (0:02:55)` (+15 gate).

## §6 STATO CI

- Run sui commit di questo handoff: non ancora disponibile alla scrittura dell'handoff. §2/§3 non possono contenere il commit dell'handoff stesso.

## §7 RISERVE APERTE

- R-388-1 (chat Motore, BASSA): l'ultima estensione non è confrontata con le parole delicate (`github.token`, `aws.credentials`).
- R-388-2 (chat Motore, COSMETICA): `tronca_visibile_coda(t, 0)` restituisce tutto.
- Limite dichiarato: i file creati da `run_command` non fanno scattare l'avviso. Altre riserve: vedi stato_progetto.md.
