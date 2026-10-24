# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-10-25 — Turno di notte: `/clear` da Telegram (voce 3 di `reports/coda_notte.md`)

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #263 (https://github.com/Gasss23/Gas/pull/263). Numero e URL dalla risposta JSON di `gh api -X POST repos/Gasss23/Gas/pulls` (GraphQL non disponibile). Il turno di notte non mergia mai.
2. Prova dal vero: bot acceso (`python3 gas.py telegram`), qualche messaggio, poi `/clear`.
3. Testo dell'attività programmata «Turno di notte Gas»: la chat Motore ha chiesto il cambio il 24 ottobre riferendo un'approvazione dell'operatore; non applicato, serve la richiesta dell'operatore in questa sessione.

---

## §1 SCOPE & ESITO FETTE

- **Fetta 1 — Voce 3, `/clear` su Telegram**: `FATTA` — `modules/telegram/bot.py` + 19 test in `tests/test_unit_notte.py`; review #502 e #503 APPROVATO CON RISERVE.
- **Voci 4 e 5**: `SALTATA — toccano il motore: al massimo una voce del motore a notte`.
- **Voci 6–8**: `SALTATA — dopo in ordine; nessuna voce solo-documenti da aggiungere`.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   3 +++
 modules/telegram/bot.py            | 134 +++++++++++++++++++++++++
 reports/coda_notte.md              |   2 +-
 reports/diff_sessione.md           |  17 +++++++++--------
 reports/handoff.md                 | n/d (commit finale)
 reports/report_notte.md            |  31 +++++++++++--------------------
 reports/stato_progetto.md          |   4 +++-
 reports/ultimo_report.md           |  25 +++++++++----------------
 tests/test_unit_notte.py           | 197 +++++++++++++++++++++++++++++
```

NB: per `reports/handoff.md` il conteggio non è misurabile al momento della scrittura (il file sta tutto nel commit finale), quindi «n/d». Gli altri conteggi vengono da `git diff --cached --stat` preso prima del commit finale, con le barre accorciate; il diff reale della PR fa fede.

## §3 GIT LOG --ONELINE (sessione)

```
ceeed81 feat(telegram): /clear da Telegram come il clear del terminale (coda notte voce 3)
c5faa56 chore(revisore): memoria review #503 — APPROVATO CON RISERVE
3ba317f chore(revisore): memoria review #502 — APPROVATO CON RISERVE
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione. Il suo hash è nel `git log` del branch dopo il push.

## §4 VERDETTO DEL REVISORE (per commit motore)

### Review #502 (chat Notte) — sul primo diff staged, poi corretto

## VERDETTO: APPROVATO CON RISERVE

Review #502 (chat Notte), ramo notte/2026-10-25. Ho esaminato il diff STAGED: modules/telegram/bot.py (+109) e tests/test_unit_notte.py (+152). Prima della review ho letto CLAUDE.md, reports/stato_progetto.md (le parti che servivano) e la mia memoria.

**Cosa ho controllato nel diff**
1. `modules/telegram/bot.py:707` — il ramo `/clear` in `_handle_update` sta DOPO il controllo `chat_id not in allowed` e dopo `/notte`/`/compito`. Rischio esaminato: una chat non autorizzata che pulisce la cronologia, oppure `/clear` che arriva al modello. Esito: ok. `test_handle_update_clear` (tests/test_unit_notte.py:2077) prova che una chat non autorizzata non provoca né pulizia né invio, e il kernel finto solleva un errore se si arriva a `run_turn`.
2. `modules/telegram/bot.py:652` — `esegui_clear` confrontato riga per riga con `_clear_con_riflessione` (contesto: gas.py:5860). L'ordine è lo stesso: riflessione solo se c'è storia e `riflessione_auto_attiva()`, poi `clear_history()` in ogni caso. Rischi esaminati: pulizia saltata se la riflessione fallisce, eccezione che risale (§9). Esito: ok. Due try separati, `log.warning` in entrambi, la pulizia fallita diventa «✗ Cronologia NON pulita». Ctrl-C qui non serve perché il bot non è interattivo.
3. `modules/telegram/bot.py:580` — la regex segue lo schema di `_COMANDO_GIRO_RE`: destinatario @bot, argomenti separati da spazio o tab, che danno errore. Rischio esaminato: un falso positivo distruttivo. Esito: ok. «/clearx», «ciao /clear» e «/clear<NBSP>x» non attivano il comando. Ho provato a mano «/clear\nora»: ritorna None e quindi va al modello come testo normale (non distruttivo, stesso comportamento di /notte).
4. `modules/telegram/bot.py:618` — `righe_riflessione` passa tutto il testo del modello per `rendi_visibili`/`tronca_visibile`. Le lezioni restano su una riga sola (a_capo=False). Il recap è indentato con «│ » e messo per ultimo. Il cambio di provider viene dichiarato (§8). Rischio esaminato: righe finte che imitano l'esito, caratteri bidi. Esito: ok, coperto da tests/test_unit_notte.py:2060.
5. `tests/test_unit_notte.py:2094` — il round-trip §7 col kernel vero e il client finto fa due tool call, arriva alla risposta finale, poi `/clear` svuota la storia e cancella .gas_history.json, e il turno dopo riparte da user. Esito: ok (con la riserva R-502-2).
6. Wall of Shame: il diff non ha slicing della history (l'unico taglio è sulla stringa del recap, `modules/telegram/bot.py:605`) e non simula output dei tool. Il cap delle 10 iterazioni, `_get_window` e i guardrail non sono toccati.

**Riserve** (vanno messe in stato_progetto.md)
- **R-502-1 MEDIA** — `modules/telegram/bot.py:583`: `_CLEAR_RECAP_MAX = 1200` taglia il recap. Il terminale invece lo mostra INTERO per decisione R-201-2/R-200-3 (gas.py:5838: «l'operatore vede SEMPRE cosa verrà dato come contesto»). Il recap salvato può arrivare a 4000 caratteri, quindi su Telegram l'operatore può non vedere fino a ~2800 caratteri di contesto che verrà iniettato. Non lo blocco: resta leggibile con «ricorda» o dal terminale. Correzione suggerita: mandare il recap intero in uno o più messaggi a parte invece di tagliarlo. Se no, serve una decisione esplicita dell'operatore.
- **R-502-2 BASSA** — `tests/test_unit_notte.py:2094`: il round-trip col kernel vero gira con `GAS_RIFLESSIONE_AUTO=0` (impostato da un fixture, riga 40). Il percorso bot → `kernel.rifletti()` reale non è mai provato insieme: la riflessione è testata solo col kernel finto.
- **R-502-3 BASSA** — `modules/telegram/bot.py:638`: le righe «(scartata: …)» non hanno un tetto e vengono prima dell'avviso «Recap … NON fidato». Se il modello propone molte lezioni scartate, il taglio a 4096 di `_send_text` può togliere quell'avviso, e il commento alla riga 582 promette solo che restano l'esito e le lezioni. Basta mettere un tetto alle scartate (es. 5 + «… e altre N») oppure spostare l'avviso NON fidato prima.

**Misure mie** (venv indicato): `python tests/test_unit_kernel.py` → 1031 PASS, 0 FAIL; `pytest -q tests/` completo, verde fino al 100%; test `-k clear` → 16 passed.

**Cosa NON ho verificato**: il comportamento col Telegram vero (polling reale, indicatore «sta scrivendo» che scade dopo ~5 s durante una riflessione di minuti, update ricevuti durante il blocco). In dev non si riproduce e non ci sono credenziali. Non ho verificato neanche cosa succede se REPL e bot girano in parallelo sullo stesso .gas_history.json: è un problema che c'era già prima, non introdotto da questo diff.

**Memoria**: aggiunta la riga #502 più una lezione (portare un comando del terminale su un altro canale senza perdere le garanzie di visibilità già decise), committate con lo script (3ba317f) in /home/user/Gas/.claude/agents/memoria_revisore.md.

### Review #503 (chat Notte) — sul diff committato in ceeed81

## VERDETTO: APPROVATO CON RISERVE

Review #503 (chat Notte), diff STAGED in /home/user/Gas, ramo notte/2026-10-25: `/clear` da Telegram, secondo giro dopo la #502. File in stage: modules/telegram/bot.py (+134) e tests/test_unit_notte.py (+197). Prima della review ho letto CLAUDE.md, reports/stato_progetto.md (le parti che servono) e la mia memoria.

**Cosa ho guardato nel diff**
1. `modules/telegram/bot.py:612` — `messaggi_recap` manda il recap INTERO, con le righe rientrate da «│ » e diviso in messaggi da al massimo 4000 caratteri. Rischio controllato: un pezzo oltre i 4096, una sequenza «<U+XXXX>» spezzata, testo perso. Prova fatta: 3 righe da più di 3999 caratteri con «<x » e U+200B al punto di taglio danno pezzi di [3997, 4000, 4000, 29], senza sequenze spezzate. Il test ricostruisce il testo visibile senza perdite. Esito: ok, **R-502-1 chiusa** (stessa garanzia del terminale, R-201-2).
2. `modules/telegram/bot.py:606` — `_taglio_sicuro` cerca un «<» solo negli ultimi 10 caratteri e lo scarta se dopo c'è già un «>». Rischio controllato: un ciclo infinito, oppure un «<» scritto nel testo che fa tagliare male. Ogni giro avanza di almeno 3990 caratteri, e un «<» letterale fa solo tagliare un po' prima. Esito: ok.
3. `modules/telegram/bot.py:665` — le righe «scartata» hanno un tetto (5, poi «… e altre N»), e l'avviso «NON fidato» viene prima delle lezioni. Rischio controllato: un primo messaggio troppo lungo. Conto: al massimo 3 lezioni (`RIFLESSIONE_MAX_LEZIONI`) da al massimo 300 caratteri (`LEZIONE_TESTO_MAX` in modules/memory/store.py:75), più 5 scartate da circa 170: circa 2 KB, sotto il limite. Esito: ok, **R-502-3 chiusa**.
4. `modules/telegram/bot.py:694` e `modules/telegram/bot.py:738` — `esegui_clear` ora ritorna una lista: in testa l'esito della pulizia, poi il recap. `_handle_update` manda i messaggi in ordine, dopo il controllo della chat autorizzata. Rischio controllato: la pulizia saltata se la riflessione fallisce, un'eccezione che arriva fino al loop del bot. Ci sono due try separati, il fallimento finisce nel log con `log.warning` e la pulizia avviene sempre (§9). Esito: ok.
5. `tests/test_unit_notte.py:2145` — round-trip bot → `kernel.rifletti()` vero con il client finto `_ClientRifl`: controlla recap nel secondo messaggio, lezioni in quarantena (2 nel DB) e storia vuota. Esito: ok, **R-502-2 chiusa**. Ho girato `pytest -k clear` su tests/test_unit_notte.py: 17 passed.

Wall of Shame: nessuno slicing della cronologia (i tagli sono solo su testo da mostrare) e nessuna simulazione degli strumenti fuori dai test. Il tetto di 10 iterazioni, `_get_window` e i guardrail della memoria non sono toccati.

**Riserve**
- **R-503-1 BASSA**: il pezzo da 4000 è contato in caratteri Python, mentre Telegram conta in unità UTF-16. 4000 caratteri «astrali» (es. emoji) superano 4096 e Telegram rifiuterebbe il messaggio. È lo stesso limite che ha già `_send_text`, e un recap così non è realistico.
- **R-503-2 COSMETICA**: una lezione (al massimo 300 caratteri nello store) piena di caratteri invisibili, una volta resi come «<U+XXXX>», supera 300 e su Telegram viene tagliata con «…». Il testo intero resta in `gas lezioni lista`, ed è lì che si approva.

**Cosa NON ho verificato**: l'invio vero sull'API di Telegram (limite effettivo, limiti di frequenza con molti pezzi), perché in sviluppo il trasporto HTTP è bloccato. Non ho rifatto nemmeno l'intera suite: mi fido delle tue misure (1031 PASS nel kernel, 2159 passed con pytest).

**Memoria**: riga #503 aggiunta in /home/user/Gas/.claude/agents/memoria_revisore.md e committata da sola (c5faa56). Il diff del motore resta in stage. Nessuna lezione nuova.

## §5 DELTA TEST DEL MOTORE

- `python tests/test_unit_kernel.py`: `=== RIEPILOGO: 1031 PASS, 0 FAIL ===` (invariato: gas.py non toccato).
- `python -m pytest -q tests/`: main `2140 passed, 1 skipped` → ramo `2159 passed, 1 skipped` (+19 test di `/clear` in `tests/test_unit_notte.py`). Nessun FAIL.

## §6 STATO CI

```
completed	skipped	Turno di notte 2026-10-25: /clear da Telegram (coda voce 3)	verifica-bot	notte/2026-10-25	pull_request_target	40141304878	7s	2026-10-24T23:05:44Z
in_progress		feat(telegram): /clear da Telegram come il clear del terminale (coda …	CI	notte/2026-10-25	push	40141292710	44s	2026-10-24T23:05:34Z
completed	success	R2 via B fetta 3: costo su ogni errore, conto sotto lucchetto, doctor del cervello forte	verifica-bot	feat/merge-automatico-z1xjx2	pull_request_target	40135227128	3m17s	2026-10-24T21:40:05Z
```

Mappatura commit→run:
- `3ba317f`, `c5faa56`: nessuna run su questo SHA (pushati insieme a `ceeed81`).
- `ceeed81` → run CI 40141292710 (push), in corso alla scrittura dell'handoff.
- commit di fine-task che contiene questo file: run non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- **R-503-1 (chat Notte)** BASSA: pezzo da 4000 contato in caratteri, non in unità UTF-16.
- **R-503-2 (chat Notte)** COSMETICA: lezione piena di invisibili tagliata con «…» su Telegram.
- Non provato col Telegram vero (indicatore «sta scrivendo» durante una riflessione lunga).
