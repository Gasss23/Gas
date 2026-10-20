# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-10-20 (dopo il merge di #225) — firme scadute (C5), avvisi dei lead raggruppati

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR: l'agente mergia da solo solo con un APPROVATO pulito del bot (CLAUDE.md §10); altrimenti decide l'operatore.
2. Togliere dal progetto claude.ai le copie di `briefing_architettura_voce.md` e `recinto_autonomia.md` (l'agente non vi ha accesso).

---

## §1 SCOPE & ESITO FETTE

- **C5 — scadenza delle firme (R1)**: `FATTA` — review #381 APPROVATO CON RISERVE.
- **Avvisi dei lead raggruppati (V-1/V-2 bot #225) + riserve #381**: `FATTA` — review #382 BOCCIATO → #383 APPROVATO CON RISERVE.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   3 +++
 gas.py                             | 101 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++---------------
 modules/memory/store.py            |  69 ++++++++++++++++++++++++++++++++++++++++++++++++---------------------
 modules/notte/notte.py             |  22 ++++++++++++++++++++++
 modules/telegram/bot.py            |  43 +++++++++++++++++++++++++++++++++++++++++++
 reports/diff_sessione.md           |  11 +++++++----
 reports/handoff.md                 | 160 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++----------------------------------------
 reports/stato_progetto.md          |   2 ++
 reports/ultimo_report.md           |  11 +++++++----
 tests/test_unit_kernel.py          | 133 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++-----
 tests/test_unit_notte.py           |  53 +++++++++++++++++++++++++++++++++++++++++++++++++++++
 11 files changed, 519 insertions(+), 89 deletions(-)
```

---

## §3 GIT LOG --ONELINE (sessione)

```
1f4442e Merge remote-tracking branch 'origin/main' into feat/merge-automatico-z1xjx2
87c377d fix(avvisi): un solo avviso per turno sotto il limite Telegram; riserve C5 (R-381-1/2/3)
861409f chore(revisore): memoria review #383 — APPROVATO CON RISERVE
c99f1d9 chore(revisore): memoria review #382 — BOCCIATO
214e0da feat(firme): le richieste di firma scadute si chiudono e si avvisano (C5)
4abf095 chore(revisore): memoria review #381 — APPROVATO CON RISERVE
```

---

## §4 VERDETTO DEL REVISORE (per commit motore)

### Review #381

## VERDETTO: APPROVATO CON RISERVE

Review #381, fetta C5 (scadenza firme) sul diff staged del branch feat/merge-automatico-z1xjx2. Prima ho letto CLAUDE.md (sez. 5, 8, 9 e 10), la sezione di stato_progetto.md sulle firme e la memoria del revisore.

**Cosa ho guardato nel diff**
- `modules/memory/store.py:1957` — `scadi_approvazioni`: lettura e UPDATE stanno nella stessa transazione (`BEGIN IMMEDIATE`, store.py:1970), e l'UPDATE filtra `WHERE id = ? AND stato='pending'` (store.py:1983). Rischio esaminato: due chiamanti (bot e giro notturno) che avvisano due volte la stessa richiesta. Il lock è preso prima della SELECT, come dice la lezione #379. Anche il caso R-c3-1b resta coperto: le righe con ts_expiry non numerico (TEXT, BLOB, NULL) vengono comunque scadute, perché il `typeof` sta nella stessa WHERE. Le eccezioni sqlite3/OSError diventano `[]` più un warning. — ok
- `modules/memory/store.py:1997` — `conta_approvazioni`: sola lettura, restituisce None in degrado, con lo stesso criterio di scadenza della SELECT precedente. Rischio esaminato: incoerenza tra il conteggio di doctor e quello che il bot chiude. Le due WHERE coincidono. — ok
- `modules/telegram/bot.py:282` — `componi_avviso_scadute`: i campi passano da `rendi_visibili(a_capo=False)`, sono troncati a 120/60 caratteri, l'elenco si ferma a 10 voci e il messaggio non ha bottoni. Rischio esaminato: iniezione di finti messaggi «SYSTEM» tramite a capo in azione o tool_name. Il test T73d2 lo copre. — ok
- `modules/telegram/bot.py:297` — `avvisa_firme_scadute`: protetto da `except Exception`, un invio fallito produce solo un warning e la riga resta chiusa (scelta dichiarata, il conteggio resta visibile in doctor). — ok
- `modules/telegram/bot.py:370` — timer del loop: `ultimo_controllo_scadute = 0.0` confrontato con `time.monotonic()` (bot.py:374). — riserva (R-381-2)
- `modules/notte/notte.py:399` — `_chiudi_firme_scadute`: protetto, con controllo di `available`. Il numero di firme chiuse finisce in `avvisi` (notte.py:556) dopo che `catalogo_ko` è già stato calcolato, quindi il codice di uscita non cambia. — ok, con riserva R-381-3
- `gas.py:4317` — riga «Firme» di doctor: usa il `mem` già aperto solo se il DB esiste (contesto: gas.py:4216), sola lettura, ha un `except` proprio. Il commento è numerato «12.» ma sta prima del «9.»: solo estetica. — ok
- Wall of Shame: nessuno slicing della cronologia, nessun output di tool simulato, `_get_window` e il tetto di 10 iterazioni non toccati. — ok

**Controprove**
- Riprodotti i risultati: kernel 935 PASS e 0 FAIL, `test_unit_notte` 72 passed.
- Mutazione in un worktree temporaneo (codice di HEAD con i test nuovi, niente stash):
  - kernel: T61b2 fallisce e T73d2 si ferma con `AttributeError: scadi_approvazioni`;
  - notte: 2 FAIL (`test_firme_scadute_chiuse_e_negli_avvisi`, `test_bot_controlla_le_firme_scadute`).
  I test provano davvero il codice nuovo. Worktree rimosso, index intatto.

**Riserve (tutte BASSE, da tracciare in stato_progetto.md)**
- **R-381-1:** `scadi_approvazioni` non controlla `self.available`, mentre le altre scritture sulle firme lo fanno (contesto: modules/memory/store.py:1876). Il bot la chiama anche con memoria degradata, per esempio in caso di collisione chiave_norm. Un DB rotto finisce comunque in un `except`, quindi niente crash: resta un'incoerenza.
- **R-381-2:** con `0.0` come valore iniziale, su una macchina accesa da meno di 60 secondi il primo controllo slitta di un minuto e `test_bot_controlla_le_firme_scadute` fallirebbe (test instabile su runner appena avviati). Correzione: inizializzare a `float("-inf")`.
- **R-381-3:** `_chiudi_firme_scadute` apre `MemoryStore` anche con il catalogo vuoto (nessun kernel creato), quindi crea `.gas_memory.db` come effetto collaterale. Doctor invece evita apposta di farlo.

**Cosa non ho verificato**
- Invio Telegram reale e concorrenza vera tra bot e giro notturno su processi separati: non riproducibili qui. L'esclusione reciproca poggia su `BEGIN IMMEDIATE` più il filtro per stato, verificati sul codice e non con due processi.
- La suite completa `pytest tests/` (1522 passed) non l'ho rilanciata: ho rieseguito solo kernel e notte.

**Memoria:** riga #381 aggiunta in /home/user/Gas/.claude/agents/memoria_revisore.md, insieme alla lezione «un timer su time.monotonic() va inizializzato a -inf, non a 0». Committata da sola con lo script dedicato (commit 4abf095); il diff staged del motore è rimasto intatto.

### Review #382

## VERDETTO: BOCCIATO

Ho letto CLAUDE.md (sezioni 1, 5, 8, 9 e 10), reports/stato_progetto.md (le parti che servivano) e la memoria del revisore (le lezioni e le righe fino alla #381).

**Esiti riprodotti**
- Suite del kernel: 939 PASS, 0 FAIL.
- test_unit_notte: 73 passed.
- Controprova in un worktree temporaneo (codice di HEAD con i test nuovi; il worktree è stato rimosso): kernel 934 PASS / 5 FAIL, notte 1 FAIL. I test nuovi colpiscono davvero il cambiamento: falliscono T73d2 R-381-1, i quattro T74b6 e test_firme_scadute_non_crea_il_db.

**Elementi esaminati**
- `modules/memory/store.py:1968` — se lo store non è disponibile, `scadi_approvazioni` ritorna [] senza toccare il DB. Rischio esaminato: scrittura su memoria degradata. Esito: ok, R-381-1 chiusa, e la controprova conferma che T73d2 morde.
- `modules/telegram/bot.py:370` — il timer del controllo firme parte da `float("-inf")`. Rischio esaminato: primo controllo ritardato su una macchina accesa da poco. Esito: ok, R-381-2 chiusa (non c'è un test dedicato, è una riga ovvia).
- `modules/notte/notte.py:405` — se `.gas_memory.db` manca si esce con 0 prima di aprire `MemoryStore`. Rischio esaminato: creazione del DB come effetto collaterale. Esito: ok, R-381-3 chiusa, il test morde.
- `gas.py:2569` — `_avvisa_lead_dopo_lettura` ora restituisce solo il blocco del lead (None se non c'è nulla da dire) e non solleva eccezioni. Esito: ok.
- `gas.py:2610` — `_invia_avvisi_lead` compone UN solo messaggio con al massimo 10 blocchi più «… e altri K». Rischio esaminato: lunghezza contro il limite Telegram. Esito: **blocco (R-382-1)**, dettagli sotto.
- `gas.py:4079` — l'invio sta nel `finally` di run_turn, dopo `_chiudi_turno`. Rischio esaminato: invio saltato sulle uscite anticipate o in caso di eccezione. Esito: ok. Copre tutte le uscite, `_chiudi_turno` passa solo per `_diario_log`, che non solleva, e l'invio stesso non solleva.
- `gas.py:2587` — taglio a 200 caratteri che non deve spezzare le sequenze `<U+XXXX>`. Esito: riserva R-382-2.
- `tests/test_unit_kernel.py:6045` — test dei 13 lead → 1 messaggio. Copre il conteggio dei lead, non la lunghezza del messaggio.

**Motivo del blocco**

R-382-1 (MEDIA) — un testo esterno può spegnere l'intero avviso.
- `modules/telegram/bot.py:243` (`invia_notifica`) rifiuta in blocco qualsiasi testo oltre 4096 unità («testo oltre il limite Telegram»). Prima di questo diff ogni blocco era un messaggio a sé e stava sempre sotto il limite. Il messaggio unico invece non ha un tetto di lunghezza.
- L'ho provato con uno script: 10 lead con chiave e recapito lunghi, ciascuno creato e poi modificato (un lead nuovo non genera avviso, uno già esistente sì).
  - 6 blocchi = 4147 unità → nessun invio.
  - 7 blocchi = 4813 unità → nessun invio.
  - 10 blocchi = 6811 unità → nessun invio.
  - Nella scatola nera resta solo il warning.
- Quindi il testo letto, che è proprio la minaccia da cui l'avviso deve proteggere, può far creare e poi modificare circa 6 lead lunghi nello stesso turno. Così sopprime anche l'avviso sulle modifiche ai lead legittimi.
- Il segno «non fidato» resta, quindi la difesa principale regge. Ma per chiudere una nota BASSA sul rumore si è introdotto un modo per spegnere il segnale all'operatore.
- Correzione semplice: aggiungere i blocchi finché il testo, con chiusura e «… e altri K», resta sotto `TELEGRAM_MAX_CHARS` (misurato con `lunghezza_telegram`) e contare gli altri. Va aggiunto un test con blocchi lunghi che verifichi che il messaggio parte.

**Riserva non bloccante**

R-382-2 (BASSA) — il taglio a 200 spezza ancora la sequenza quando cade a 1-2 caratteri dentro. `rfind("<U+")` non trova `<` o `<U` rimasti in coda. L'ho provato: con 198 caratteri il recapito finisce in «xxx<U…», con 199 in «xxx<…». Il test copre solo il caso con 197 caratteri. Correzione: cercare l'ultimo `<` e tagliare lì se dopo non c'è `>`.

**Rischi esclusi (non verificati)**
- Consegna reale su Telegram e resa del messaggio sul telefono: non riproducibile in dev (ho usato un token finto, e il controllo sulla lunghezza scatta prima di qualsiasi chiamata di rete).
- La durata del `finally` con Telegram irraggiungibile: resta il problema già noto R-380-2 (invio sincrono, timeout 15 s per destinatario). Ora pesa una volta per turno invece che per ogni lead, quindi è migliorato, ma non l'ho misurato.
- La suite completa `pytest tests/` (1523): non l'ho rieseguita, ho riprodotto solo kernel e notte.

**Wall of Shame**: nessuno slicing della history, nessuna simulazione dell'output dei tool; il tetto di 10 iterazioni e `_get_window` non sono toccati.

**Memoria**: aggiunta la riga #382 in /home/user/Gas/.claude/agents/memoria_revisore.md, con la lezione «quando si accorpano N notifiche in una, rifare il conto del caso peggiore contro il limite del canale». Committata da sola (c99f1d9) con scripts/commit_memoria_revisore.sh; il diff in staging non è stato toccato.

### Review #383

## VERDETTO: APPROVATO CON RISERVE

Review #383, che rifà la review #382 sul diff in staging (`git diff --cached`) del branch feat/merge-automatico-z1xjx2. Prima ho letto CLAUDE.md (sez. 5), reports/stato_progetto.md e la mia memoria (.claude/agents/memoria_revisore.md).

**Riprodotto da me**
- Suite kernel: 941 PASS, 0 FAIL.
- pytest tests/: 1523 passed.
- Mutazione in un worktree temporaneo (codice in staging con i 3 rami nuovi spenti): 938 PASS, 3 FAIL. I 3 FAIL sono esattamente i test T74b6 nuovi (R-382-1, R-382-2, lead nuovi), quindi ogni correzione è coperta dal suo test. Il worktree è stato rimosso e l'index è intatto (niente git stash).

**Elementi esaminati**
- gas.py:2641 — il ciclo `while k > 0 and lunghezza_telegram(_componi(k)) > TELEGRAM_MAX_CHARS: k -= 1`. Rischio esaminato: il messaggio unico supera 4096 unità e Telegram lo rifiuta tutto (R-382-1). Prova fatta: 10 blocchi da circa 630 emoji (2 unità UTF-16 ciascuna) più 7 lead nuovi → parte un solo messaggio da 2852 unità, con «… e altri N lead modificati.», la riga dei lead nuovi e la coda. Con k=0 resta solo un testo breve, sempre sotto il limite. Esito: ok, **R-382-1 chiusa**.
- gas.py:2591 — il taglio a 200 caratteri cerca l'ultimo «<» senza «>» dopo. Rischio esaminato: spezzare a metà una sequenza «<U+XXXX>» (R-382-2), coperta dal test con 197/198/199 caratteri. Esito: **R-382-2 chiusa, ma con una riserva (R-383-1, sotto)**.
- gas.py:4037 — il conteggio di `_lead_nuovi` (`_prima is None` e lead esistente dopo la scrittura). Rischi esaminati:
  - doppio conteggio della stessa chiave nel turno: no, alla seconda scrittura `_prima` non è più None;
  - `imposta_stato_contatto` su una chiave inesistente: dopo resta None, quindi non conta;
  - lettura «prima» fallita in errore: conta in più, ma solo come rumore informativo.

  Esito: ok.
- gas.py:4103 — `_invia_avvisi_lead` dentro il `finally`, dopo `_chiudi_turno`, con try/except interno e warning nella scatola nera (§9). Rischio esaminato: un'eccezione che esce dal `finally`. Esito: ok.
- modules/memory/store.py:1968, modules/telegram/bot.py:370, modules/notte/notte.py:405 — chiusure di R-381-1/2/3, già verificate nella review #382. Esito: ok.
- Wall of Shame: nessuno slicing della history e nessuna simulazione di output dei tool. Il cap di 10 iterazioni e `_get_window` non sono toccati.

**Riserva (da tracciare in stato_progetto.md)**
- **R-383-1 BASSA.** `rendi_visibili` (modules/telegram/bot.py:133) non trasforma il «<» letterale, e gas.py:2591 cerca il «<» nell'intero taglio di 200 caratteri. Così un «<» nel testo esterno cancella tutto quello che segue nel valore mostrato.
  - Sondato: recapito «<» + 250 caratteri → `Recapito cambiato: … (251 caratteri) → … (251 caratteri)`. L'avviso parte, ma l'indirizzo nuovo non si vede.
  - Sondato: `mail@x.it<BBB…` → resta solo `mail@x.it…`.
  - Fail-closed: l'avviso arriva comunque e rimanda alla scheda. Si perde solo informazione.
  - Correzione suggerita: cercare il «<» solo negli ultimi 9 caratteri, es. `t.rfind("<", len(t) - 9)` (una sequenza `<U+10FFFF>` è lunga al massimo 10).

**Rischio escluso**
- Non ho verificato l'invio reale su Telegram (rete, timeout, conteggio UTF-16 lato server): ho usato `invia_notifica` finto con `lunghezza_telegram` come misura. Non è riproducibile in dev senza token del bot.

**Memoria**
- Riga #383 aggiunta in coda a /home/user/Gas/.claude/agents/memoria_revisore.md, con la lezione: un rfind su un delimitatore va limitato alla lunghezza massima della sequenza da proteggere.
- Committata da sola con scripts/commit_memoria_revisore.sh (commit 861409f). Il diff in staging resta intatto: 6 file, +164/-22.

Commit consentito, con R-383-1 tracciata.

---

## §5 DELTA TEST DEL MOTORE

tests/test_unit_kernel.py in locale: 927 → 941 PASS, 0 FAIL (T73d2, T61b2, T74b6). Blocco reale: `=== RIEPILOGO: 941 PASS, 0 FAIL ===`. In CI i conteggi sono +2 (test del profilo sandbox saltati in locale).
pytest `tests/`: `1523 passed in 183.60s (0:03:03)` (+4 notte).

## §6 STATO CI

- Run sui commit di questo handoff: non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- R-383-1 (BASSA): un «<» nel testo letto taglia il valore mostrato nell'avviso dei lead (l'avviso parte comunque).
- R-380-1, R-380-2 (BASSE, da #225); R-378-1, R-379-1, R-ve224-2 (da #224); da #222: R-366-1, R-367-2, R-370-2, R-bot222-2, R-ve222-2, R-373-1, R-375-1, R-372-1 (vedi stato_progetto.md).
