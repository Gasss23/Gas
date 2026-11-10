# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-11-10 — terminale opzione A: azioni fisse di manutenzione per Gas (chat M2)

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #363 (https://github.com/Gasss23/Gas/pull/363). È un CAMBIO DI SICUREZZA: resta aperta fino al sì esplicito dell'operatore, anche con verdetto pulito del bot. Consigliato il secondo passaggio nella chat claude.ai col link della PR.
2. R-738-2: «mai a voce» deve valere anche per i vocali di Telegram (che oggi arrivano a Gas come turni a testo)? Decide l'operatore.

NB: `gh` nel cloud non è autenticato; numero e URL della PR vengono dalla risposta reale dello strumento GitHub MCP `create_pull_request`.

---

## §1 SCOPE & ESITO FETTE

- **Fetta 1 — terminale opzione A (strumento `manutenzione`, cancello, divieti in run_turn, test, CI)**: `FATTA` (e93bd77).
- **Merge di origin/main (#359 di Mani) nel ramo**: `FATTA` (32619b5), review #743-M2.
- **Riserve del terminale A registrate in stato_progetto (R-743-1)**: `FATTA` (commit di fine task).
- **Prova dal vivo di `riavvia_voce` / launchctl sul Mac**: `DEFERITA` — dopo il merge.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   7 +++++++
 .github/workflows/ci.yml           |   7 +++++++
 gas.py                             |  55 +++++++
 modules/gate/gate.py               |  20 ++++
 modules/manutenzione/__init__.py   | 187 ++++++++++++++
 reports/diff_sessione.md           |  19 ++++++++++---------
 reports/handoff.md                 | n/d
 reports/proposta_terminale_A.md    |  31 +++++++
 reports/stato_progetto.md          |   1 +
 reports/ultimo_report.md           |  18 ++++++++----------
 tests/test_unit_manutenzione.py    | 310 ++++++++++++++++++++++
```

NB: regola «n/d» — il conteggio di `reports/handoff.md` non è misurabile mentre lo si scrive; riga di totale tolta.

## §3 GIT LOG --ONELINE (sessione)

```
32619b5 Merge origin/main (#359 di Mani) nel terminale A — review #743-M2 APPROVATO CON RISERVE (chat M2)
e93bd77 feat(gas): terminale opzione A — azioni fisse di manutenzione (stato_gas, log_voce; aggiorna_gas e riavvia_voce solo con firma), mai a voce né di notte (decisione dell'operatore via M1)
54a6299 chore(revisore): memoria review #739 — APPROVATO CON RISERVE
28c559e chore(revisore): memoria review #738 — APPROVATO CON RISERVE
1ebb897 chore(revisore): memoria review #736 — BOCCIATO
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione.

## §4 VERDETTO DEL REVISORE (per commit motore)

### Review #743-M2 (merge di main, commit 32619b5) — verdetto integrale

VERDETTO: APPROVATO CON RISERVE

Review #743-M2. È il merge in staging di origin/main 695b759 (PR #359, voce Telegram) nel ramo feat/terminale-a-m2 (HEAD e93bd77).

**Il merge non perde nulla**
- Ramo e main hanno toccato file diversi a partire dalla base comune 567beb7. L'unico file in comune è la memoria del revisore.
- I 9 file che vengono da main sono identici, blob per blob, a quelli di 695b759: bot.py, ascolto.py, i test kernel, telegram_voce e voce_ascolto, e i 4 report, stato_progetto compreso.
- I 6 file del terminale A sono identici a HEAD: gas.py, gate.py, manutenzione, il suo test, ci.yml e la proposta.
- `git diff --cached origin/main` mostra solo il contenuto del terminale A più la memoria. `git ls-files -u` è vuoto e non restano marcatori di conflitto.

**Elementi esaminati**
- `.claude/agents/memoria_revisore.md:1410` — il conflitto risolto. Rischio: perdere righe di uno dei due lati. Esito ok: dopo la base ci sono tutte le righe di main (da #722 a #735, chat Mani) seguite da quelle del ramo (da #736-M2 a #739-M2), senza buchi.
- `modules/telegram/bot.py:1002` — `_consegna_voce` manda a un thread separato solo `_invia_risposta_vocale`. Rischio: che un'azione firmata del terminale A (aggiorna_gas, riavvia_voce) finisca nel thread della voce, o che la #359 cambi il contesto voce/sottofondo che il kernel usa per la guardia. Esito ok: le firme restano nel ciclo che legge i messaggi, e bot.py non nomina mai la manutenzione. La guardia T78p del test kernel passa.
- `gas.py:5174` — il divieto della manutenzione a voce e di notte in `run_turn`, prima del cancello. È solo contesto: il merge non lo cambia. Esito ok.
- `modules/manutenzione/__init__.py:167` — `esegui`, anche questo solo contesto: blob identico a HEAD. Esito ok.

**Test sull'albero del merge**
- pytest manutenzione + telegram_voce: 116 passed.
- tests/test_unit_kernel.py: fallisce solo T31g (già noto, GAS_VECTORS); T78p passa.

**Riserva**
- R-743-1 BASSA (di processo, non causata dal merge): le riserve R-738-2, R-738-3, R-739-1 e R-739-2 del terminale A non sono in reports/stato_progetto.md, né sul ramo né su main. Vanno aggiunte a fine task, come chiede la regola sulle riserve tracciate.

**Cosa non ho verificato**
- Non ho rifatto la review del contenuto del terminale A (già coperta da #736, #738 e #739-M2) né della #359 (#722–#735).
- Non ho provato dal vivo le interazioni a runtime (Telegram vero, launchctl): non sono riproducibili qui. La verifica è statica più i test.
- In reports/handoff.md ci sono spazi a fine riga che arrivano da main. Sono innocui.

**Memoria**
- Ho aggiunto in coda a `/home/user/Gas/.claude/agents/memoria_revisore.md` la riga #743-M2 e l'ho messa in staging con `git add`.
- Non ho eseguito `scripts/commit_memoria_revisore.sh`: hai chiesto di non committare e il merge è ancora aperto. In più il primo tentativo è stato bloccato dal gate (il marcatore `.review_ok` non corrisponde al diff in staging) prima di eseguire qualsiasi cosa, quindi la riga l'ho poi aggiunta in un comando separato.
- Ora il diff in staging comprende anche la riga di memoria: prima di committare rigenera il marcatore con `bash scripts/segna_review_ok.sh`.

### Review #736-M2, #738-M2, #739-M2 (commit e93bd77)

I verdetti integrali sono stati emessi prima di un `/clear` di questa chat e non sono più disponibili nel contesto: si riportano alla lettera le righe di memoria del revisore (`.claude/agents/memoria_revisore.md`), non il testo integrale. Il loro contenuto è coperto anche dalla verifica esterna e dal bot su questa PR.

```
#736-M2 — 2026-11-09 — BOCCIATO — terminale opzione A (modules/manutenzione, cancello, kernel), diff STAGED: la guardia del turno sta solo in execute_tool_call (gas.py:4827) ma run_turn manda al cancello prima: aggiorna_gas/riavvia_voce (IRREVERSIBLE, modules/gate/gate.py:777) chiamati da un turno a voce/sottofondo/notte vengono parcheggiati e la richiesta di firma parte lo stesso (riprodotto sulla copia dell'index: test voce → «impossibile notificare la richiesta di firma», cioè accodata). Il fix NON staged (DENY in run_turn prima del cancello) chiude il buco: va messo in staging e ri-revisionato. Riserve: spia del test su enqueue_approval vuota (il parcheggio usa accoda_approvazione), GIT_TERMINAL_PROMPT=0 per git pull, filtro log_voce più stretto.
#738-M2 — 2026-11-09 — APPROVATO CON RISERVE — terminale opzione A, seguito di #736-M2 (diff STAGED, 6 file): _manutenzione_fuori porta a DENY in run_turn PRIMA del cancello (gas.py:5173-5177), test spia accoda_approvazione; mutante senza il DENY → test_a_voce_nessuna_richiesta_di_firma fallisce (provato su copia dell'index), 29 passed. Riserve: R-738-1 MEDIA la proposta (reports/proposta_terminale_A.md:18) promette «azioni con firma negate nelle ore della notte», il codice esclude solo il kernel del giro notturno (carica_storia=False), nessuna finestra oraria; tabella :13 e domanda :24 superate dalla decisione su com.gas.ascolto. R-738-2 BASSA i vocali Telegram (modules/telegram/bot.py:984) sono turni a testo per il kernel (niente voce=True): manutenzione offerta anche lì, da far decidere all'operatore. R-738-3 BASSA l'esecuzione firmata gira nel processo del bot: aggiorna_gas può tenerlo occupato fino a ~19 min (pip 900 s + git), e il bot stesso resta sul codice vecchio senza riavvio.
#739-M2 — 2026-11-09 — APPROVATO CON RISERVE — terminale opzione A, seguito di #738-M2 (diff STAGED, 6 file): R-738-1 chiusa, finestra notte in run_turn prima del cancello (gas.py:5176-5181) e nel modulo anche firmate (modules/manutenzione/__init__.py:176); mutanti provati su copia dell'index: senza controllo del modulo 2 test falliscono, senza quello del kernel 1; 45 passed, gate 823. Riserve: R-739-1 BASSA ora locale della macchina (su VPS in UTC la finestra slitta), R-739-2 BASSA testo «Could not find service» di launchctl non provato dal vivo, R-738-2 (vocali Telegram) resta decisione dell'operatore.
```

## §5 DELTA TEST DEL MOTORE

- `tests/test_unit_manutenzione.py` nuovo (CI: passo «manutenzione suite»).
- `python tests/test_unit_kernel.py` sull'albero del merge:

```
=== RIEPILOGO: 1099 PASS, 1 FAIL ===
  FAIL: T31g gate env GAS_VECTORS=1 costruisce il vector store (lazy, no download) — vectors=VectorStore
```

  T31g è fuori scope: dipende dall'ambiente (GAS_VECTORS), fallisce uguale su main.
- `python -m pytest -q tests/test_unit_manutenzione.py tests/test_unit_gate.py tests/test_unit_notte.py`: 1064 passed.

## §6 STATO CI

CI NON VERIFICATA (gh assente): `gh` nel cloud non è autenticato.
- 32619b5 (merge, pushato da solo prima di aprire la PR #363): run non ancora disponibile alla scrittura dell'handoff.
- e93bd77, 54a6299, 28c559e, 1ebb897: nessuna run su questi SHA (mai pushati da soli; il loro contenuto è nell'albero di 32619b5).
- Commit di fine task: run non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- R-738-2 BASSA — vocali di Telegram = turni a testo: lo strumento è offerto anche lì (decisione dell'operatore, §0 punto 2).
- R-738-3 BASSA — l'esecuzione firmata gira nel processo del bot: `aggiorna_gas` può occuparlo fino a ~19 min; il bot resta sul codice vecchio fino al riavvio.
- R-739-1 BASSA — finestra notte in ora locale della macchina: su un VPS in UTC slitta.
- R-739-2 BASSA — il testo «Could not find service» di launchctl non è stato provato dal vivo.
- R-743-1 BASSA — riserve non registrate in stato_progetto: CHIUSA in questo commit (voce «Terminale opzione A»).
