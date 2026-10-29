# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-10-29 — chat M1: ponte voce → sviluppo (PR #307) e coordinamento delle chat

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #307 (https://github.com/Gasss23/Gas/pull/307): review #558-M1 APPROVATO CON RISERVE, quindi decide l'operatore (CLAUDE.md §10). Numero e URL dalla risposta JSON dello strumento GitHub `create_pull_request` (`gh` non autenticato in questo ambiente).
2. Token dedicato per il ponte (solo Issues su `Gas-richieste`) in `~/.config/gas/richieste_token` e `GAS_RICHIESTE_REPO=Gasss23/Gas-richieste` nel `.env` del Mac.
3. `GAS_VOCE_FORTE`: sì o no.
4. Permesso Remote Control per M1 (richiesta in sospeso).

---

## §1 SCOPE & ESITO FETTE

- **Fetta 1 — Ponte voce → sviluppo, strada A**: `FATTA` — `richiedi_sviluppo`, review #557-M1 → #558-M1.
- **Fetta 2 — Coordinamento delle chat**: `FATTA` — regole in `reports/stato_progetto.md`.
- **Fetta 3 — Strada B del ponte**: `DEFERITA — scelta dell'operatore (prima A, poi B)`.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   4 ++++
 .github/workflows/ci.yml           |   7 +++++++
 .gitignore                         |   2 ++
 gas.py                             |  12 ++++++++++--
 gas_identity.md                    |   3 ++-
 modules/gate/gate.py               |   3 +++
 modules/sviluppo/__init__.py       |   5 +++++
 modules/sviluppo/richieste.py      | 176 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 reports/diff_sessione.md           |  19 ++++++++++---------
 reports/roadmap.md                 |   2 +-
 reports/stato_progetto.md          |   6 +++++-
 reports/ultimo_report.md           |  39 +++++++++++++++++----------------------
 tests/test_unit_kernel.py          |  43 +++++++++++++++++++++++++++++++++++++++++++
 tests/test_unit_richieste.py       | 160 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 reports/handoff.md                 | n/d (commit finale)
```

NB: per `reports/handoff.md` il conteggio non è misurabile al momento della scrittura (il file sta nel commit finale), quindi «n/d» e niente riga di totale. Conteggi presi con i report in stage.

## §3 GIT LOG --ONELINE (sessione)

```
3f84962 feat(sviluppo): ponte voce → sviluppo, strumento richiedi_sviluppo (issue in repo privato, R8 strada A)
b8af5d1 chore(revisore): memoria review #558 — APPROVATO CON RISERVE
5935c16 chore(revisore): memoria review #557 — APPROVATO CON RISERVE
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione.

## §4 VERDETTO DEL REVISORE (per commit motore)

### Review #557-M1 — sul diff del ponte (prima delle correzioni)

## VERDETTO: APPROVATO CON RISERVE

Review #557-M1, il 2026-10-29: diff STAGED del branch feat/merge-automatico-z1xjx2 (8 file, 363 righe aggiunte). Prima ho letto CLAUDE.md, reports/stato_progetto.md (solo le parti che servivano), la memoria del revisore e reports/roadmap.md (la voce R8 e il «Ponte» di R10).

**Cosa ho rifatto io:** test del kernel 1065 PASS, 0 FAIL (T100a e T100b passano); pytest delle richieste 21 passed.

**Elementi del diff esaminati**

- `modules/sviluppo/richieste.py:57` — la vera `_http` intercetta HTTPError e ogni altra eccezione, e nel log scrive solo il nome del tipo di errore. Rischio esaminato: il token esce dal log o dal testo restituito. Esito: **ok**. Il token sta solo nell'intestazione Authorization. L'URL e il log contengono solo il nome del repo. Il ramo in `modules/sviluppo/richieste.py:161` scrive anch'esso solo il tipo di errore, e il test che fa sollevare `RuntimeError(TOKEN)` lo conferma.
- `modules/sviluppo/richieste.py:147` — `info.get("private") is not True`, quindi non scrive. Rischio esaminato: valori strani nel campo `private` («"true"», 1, None, campo assente, risposta non dict, codice diverso da 200). Esito: **ok**, è fail-closed. Il caso `{"private": "true"}` ha un test, che controlla anche che non parta nessun POST. Il TOCTOU (repo reso pubblico fra il controllo e la scrittura) resta, ma non si può chiudere lato client: lo accetto.
- `modules/sviluppo/richieste.py:72` — il token per default si legge da `~/.config/gas/agente_token`. Rischio esaminato: privilegio minimo. Esito: **riserva R-557-1 (MEDIA)**, vedi sotto.
- `modules/sviluppo/richieste.py:157` — il conto si aggiorna solo DOPO che la issue è stata creata. Rischio esaminato: race e scrittura fallita. Esito: **riserva R-557-2 (BASSA)**, vedi sotto.
- `modules/sviluppo/richieste.py:58` — `urlopen` con il redirect handler standard. Rischio esaminato: su Python 3.13 l'intestazione Authorization resta nei redirect anche verso un altro host (l'ho verificato nel sorgente di `redirect_request`). Esito: **riserva R-557-3 (BASSA)**. L'API GitHub reindirizza solo dentro api.github.com.
- `modules/gate/gate.py:68` — `richiedi_sviluppo` è UNCERTAIN, non è in `_LIBERI_DOPO_LETTURA` né in `_TOOL_OUTPUT_FIDATO`. Rischio esaminato: un contenuto esterno crea richieste. Esito: **ok**. A finestra contaminata `gas.py:4889` lo manda al cancello (`_finestra_e_contaminata` conta anche i riepiloghi di compressione e il pin non fidato). T100b prova che non parte nessuna chiamata HTTP. Ho controllato per lettura che un mutante con lo strumento aggiunto a `_LIBERI_DOPO_LETTURA` farebbe fallire T100b (la lista delle chiamate non sarebbe vuota). La modifica al cancello, che per Gas è livello 3, è di 3 righe: minima e corretta.
- `gas.py:4623` — il ramo in `execute_tool_call` accetta argomenti non dict (diventano `{}` e quindi un diniego per campi vuoti). Rischio esaminato: crash su argomenti malformati, e il percorso firmato. Esito: **ok**. Dopo la firma `applica_firma` richiama `gate_classify` e poi `execute_tool_call(firmata=True)` (contesto: `gas.py:3557`), quindi l'azione firmata viene eseguita davvero.
- `tests/test_unit_kernel.py:11348` — T100a fa il round-trip §7 completo (tool call, risultato, risposta finale) e verifica GET seguito da POST. Esito: **ok**. Note cosmetiche: T100b accetta anche «negata» oltre a «in_attesa» (in CI senza Telegram esce «negata», quindi il cancello vero non viene provato fino alla notifica), e la scrittura di `pagina100.txt` nel kernel `_k100` è codice morto.

**Riserve**

1. **R-557-1 (MEDIA)** — Il token predefinito è `agente_token`, cioè il token dello sviluppo, che scrive sul repo PUBBLICO del codice. `reports/roadmap.md:281` («Ponte» di R10) mette come vincolo «il server non ha mai le credenziali della macchina di sviluppo». Se su VPS si copia quel file, Gas runtime, che è esposto a prompt injection, avrebbe in mano un token che scrive sul codice.
   - Fix: togliere il default, oppure usare un file dedicato (es. `~/.config/gas/richieste_token`) con un token fine-grained con solo Issues:write su Gas-richieste.
   - Aggiornare la riga 281 della roadmap con la decisione della strada A.
   - Va deciso dall'operatore. Non è bloccante, perché nel codice non ho trovato nessun percorso che faccia uscire il token.
2. **R-557-2 (BASSA)** — Sulla race del conto mi hai chiesto se accettarla come riserva: **sì, la accetto**.
   - Due processi in parallelo possono leggere lo stesso n e scrivere n+1: il conto resta sotto di uno per ogni collisione. È un tetto di consumo, non una barriera di sicurezza, e le issue finiscono in un repo privato.
   - Più rilevante: se `_registra_uso` fallisce sempre (radice non scrivibile), il tetto resta APERTO (fail-open: solo un warning a `modules/sviluppo/richieste.py:158`).
   - Fix proposto: un lucchetto come in `.gas_claude_cli_uso.json.lock`, oppure scrivere il conto prima del POST (prenotazione) e negare se la scrittura fallisce.
3. **R-557-3 (BASSA)** — Un handler che rifiuta i redirect (o che li segue solo su api.github.com) chiuderebbe la possibilità che il token arrivi a un altro host.
4. **COSMETICA** — `_GAS_SYSTEM_PROMPT_BASE` (`gas.py:123`) dice ancora «Hai 11 tool nativi» e non nomina `richiedi_sviluppo`. È solo il prompt di riserva, usato se manca `gas_identity.md`.

**Coerenza col progetto:** va nella direzione di R8/R10. Robustezza §9 rispettata: nessuna eccezione esce e ogni errore produce «Operazione negata». Non tocca il cap di 10 iterazioni, `_get_window`, il tetto di 8k in uscita né i guardrail della memoria. Niente slicing della history, niente output dei tool simulato (Wall of Shame): pulito.

**Cosa NON ho verificato:**
- Le chiamate vere all'API GitHub (`private`, etichetta `da-gas`, permessi del token su Gas-richieste): richiedono rete e credenziali, e i test usano un HTTP finto.
- Il cancello fino alla notifica Telegram: in dev manca `TELEGRAM_BOT_TOKEN`.
- I mutanti: li ho ragionati, non eseguiti su una copia.

Memoria del revisore aggiornata con la riga contatore #557-M1 e una lezione, e committata (5935c16) in /home/user/Gas/.claude/agents/memoria_revisore.md.

### Review #558-M1 — sul diff finale di 3f84962 (riserve di #557-M1 corrette)

## VERDETTO: APPROVATO CON RISERVE

Review #558-M1. Riguarda il diff STAGED del ponte voce → sviluppo (`richiedi_sviluppo`), cioè il delta che chiude le riserve di #557-M1.

**Elementi del diff esaminati**
- `modules/sviluppo/richieste.py:43`: il token predefinito ora è `~/.config/gas/richieste_token`. Ho controllato se si potesse ricadere sul token di sviluppo: la riga 84 usa solo l'env oppure questo default, e `agente_token` non compare da nessuna parte. La docstring cita roadmap R10. Esito: ok, **R-557-1 chiusa**.
- `modules/sviluppo/richieste.py:163`: il posto nel tetto si prenota dopo il controllo `private` e prima del POST. Ho cercato un'apertura del tetto in caso di errore. Se il conto non si scrive, niente POST (`test_conto_non_scrivibile_niente_richiesta`). Un POST fallito consuma il posto, nel verso prudente. Un GET fallito non prenota nulla. Esito: ok, la parte "fail-open" di R-557-2 è chiusa. Resta la race senza lucchetto: vedi R-558-1.
- `modules/sviluppo/richieste.py:49-55`: `_NoRedirect` è montato in `_OPENER`. Ho controllato che il token non segua un redirect, provandolo davvero con un server locale che risponde 302. `_http` restituisce `(302, None)`, l'host di destinazione non riceve nessuna richiesta, e tra gli handler dell'opener c'è `_NoRedirect` al posto di quello di default. Esito: ok, **R-557-3 chiusa**. Il test però verifica solo la classe: vedi R-558-2.
- `gas_identity.md:19`: c'è una riga nuova, il conteggio passa a 12 e il file cresce di 151 byte (da 1689 a 1840). Ho verificato che resti coerente e breve. Ricorda i paletti (solo su richiesta dell'operatore, dopo aver chiarito) ed è allineato a `gas.py:124`. Esito: ok.
- `modules/gate/gate.py:68`: `richiedi_sviluppo` è UNCERTAIN e non è tra quelli liberi dopo una lettura. Ho cercato se una pagina esterna potesse avviare la richiesta. T100b lo esclude: con la finestra contaminata si passa dal cancello e non parte nessuna chiamata HTTP. Esito: ok.
- `gas.py:4624`: il dispatch passa `args`, che deve essere un dict. Altrimenti diventa un dict vuoto e la funzione risponde «Operazione negata». Nessuna eccezione esce. Esito: ok.

**Esiti eseguiti da me**
- pytest richieste: 24 passed.
- Kernel: 1065 PASS, 0 FAIL (T100a e T100b PASS).
- pytest completo su questo diff: **2577 passed**, 114 skipped, nessuna regressione.
- Nessun test cerca la stringa «11 tool».
- Antipattern (CLAUDE.md sez. 5): nessuno slicing della history, nessuna simulazione dell'output dei tool. Il cap delle iterazioni non è toccato.

**Riserve**
- R-558-1 BASSA (residuo di R-557-2): il conto non ha lucchetto. Due chiamate concorrenti possono leggere lo stesso `n` e contare una richiesta in meno. È accettabile con un solo processo; da chiudere se il runtime diventa concorrente.
- R-558-2 COSMETICA: `test_redirect_non_seguiti` prova solo `_NoRedirect.redirect_request`. Non prova che `_OPENER` monti quella classe. L'ho verificato a mano, ma un test con un 302 locale lo renderebbe permanente.

**Rischio escluso**: non ho verificato il comportamento verso la vera API di GitHub (repo `Gas-richieste`, permessi effettivi del token dedicato, etichetta `da-gas` già esistente). Serve un token reale e la rete verso GitHub, che non sono disponibili in dev. Va provato una volta sul VPS. Non ho verificato neanche come il proxy dell'ambiente tratta i redirect HTTPS.

Riga contatore #558-M1 e una lezione aggiunte a /home/user/Gas/.claude/agents/memoria_revisore.md e committate (b8af5d1, solo quel file: l'index staged non è toccato). Il marcatore review va creato da te con `bash scripts/segna_review_ok.sh`.

## §5 DELTA TEST DEL MOTORE

Suite kernel: 1063 → 1065 PASS (T100a, T100b nuovi), 0 FAIL.

```
=== RIEPILOGO: 1065 PASS, 0 FAIL ===
```

pytest: `tests/test_unit_richieste.py` 24 passed (nuovo); pytest completo sul diff 2577 passed, 114 skipped (misura del revisore #558-M1).

## §6 STATO CI

CI letta con lo strumento GitHub della sessione (`gh` non autenticato).

Mappatura commit→run:
- `5935c16`, `b8af5d1`, `3f84962`: pushati prima dell'apertura della PR #307; run non letta alla scrittura dell'handoff.
- commit di fine-task che contiene questo file: run non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- R-558-1 BASSA: il conto delle richieste non ha lucchetto (race fra processi concorrenti).
- R-558-2 COSMETICA: il test del redirect prova la classe, non l'opener montato.
- Le chiamate vere a GitHub vanno provate una volta col token dedicato.
