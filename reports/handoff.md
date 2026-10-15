# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-10-15 — FASE 2.6 fetta 3: il ricordo giusto (recap pertinente e con scadenza)

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #213 (https://github.com/Gasss23/Gas/pull/213).

(`gh` non disponibile nella sessione cloud: numero/URL della PR presi dall'esito reale di `create_pull_request` via MCP GitHub.)

---

## §1 SCOPE & ESITO FETTE

- **Recap pertinente al messaggio**: `FATTA`.
- **Scadenza del recap (R-199-3)**: `FATTA`.
- **Seguito bot #213 (V-1 più recente tra i pertinenti, V-2 intestazione) e verifica esterna #213 (V-1 formato ts)**: `FATTA` — review #350.
- **Riga lunga in setup_notte.md (cosmetica bot #212)**: `FATTA`.
- **Prova con conversazioni reali**: `DEFERITA` — nessun DB né chiave nel container.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   3 +++
 gas.py                             |  55 ++++++++++++++++++++++++++++++++++++++++++++-----------
 modules/memory/store.py            |  17 +++++++++++++++++
 reports/diff_sessione.md           |  13 +++++++------
 reports/handoff.md                 | 152 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++------------------------------------------------
 reports/roadmap.md                 |   2 +-
 reports/setup_notte.md             |   5 +++--
 reports/stato_progetto.md          |   4 ++--
 reports/ultimo_report.md           |  19 ++++++++++---------
 tests/test_unit_kernel.py          |  89 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++-
 10 files changed, 279 insertions(+), 80 deletions(-)
```

NB: conteggi di `reports/handoff.md` (e totali) presi prima del proprio commit.

## §3 GIT LOG --ONELINE (sessione)

```
1574821 fix(recap): tra i recap pertinenti vince il più recente; intestazione «RECAP PERTINENTE» (bot #213)
9918f22 chore(revisore): memoria review #350 — APPROVATO CON RISERVE
d6cc594 docs(fine-task): report e handoff — FASE 2.6 fetta 3 (PR #213)
0e8e29b feat(recap): ricordo giusto — recap pertinente al messaggio e con scadenza (FASE 2.6 fetta 3)
f7494b6 chore(revisore): memoria review #349 — APPROVATO
5014973 chore(revisore): memoria review #348 — APPROVATO CON RISERVE
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione.

## §4 VERDETTO DEL REVISORE (per commit motore)

### Review #348 — verdetto integrale

## VERDETTO: APPROVATO CON RISERVE

Review #348. Fetta: FASE 2.6 fetta 3, il «ricordo giusto». Chiude R-199-3 (il recap che non scadeva mai). Ho letto CLAUDE.md, reports/stato_progetto.md e la mia memoria. Ho rieseguito la suite del kernel: **867 PASS, 0 FAIL**, T90a–i tutti verdi. Le mutazioni dichiarate non le ho rifatte.

**Elementi del diff esaminati**
- `gas.py:2853` — `_recap_pin(user_prompt)`: calcola il limite `dal` in UTC con `isoformat()`, prende fino a 30 recap fidati non scaduti e sceglie per parole in comune. Nel ciclo vince solo un punteggio strettamente maggiore (`p > punti`), quindi a parità resta il più recente (ORDER BY id DESC). Rischi esaminati:
  - errori o memoria assente: sta tutto dentro il try già esistente, che restituisce "";
  - la finestra: `_get_window` e `_cap_window_chars` non sono toccati, il pin resta nel messaggio system e non c'è slicing della history.
  - Esito: ok.
- `gas.py:2875` — punteggio iniziale sul primo candidato. Rischio: niente parole vuote, quindi una parola comune di 4 o più lettere («della», «questo», «anche», «sono») dà un punto e fa vincere un recap più vecchio sul più recente. Esito: riserva **R-348-1 (BASSA)**. Il recap iniettato resta comunque fidato e non scaduto.
- `gas.py:542` — `_parole_recap`: `str(testo or "")` regge None e i tipi strani, la regex è lineare, `\w` riconosce le lettere accentate. Esito: ok. Cosmetico: è inserita tra `_TIPO_TOOL_RISERVATO` e il commento R-200-1, che così resta staccato dalla sua costante.
- `gas.py:832` — `GAS_RECAP_MAX_GIORNI` letto con `_env_int`, minimo 1. Non si può impostare 0 o un valore negativo per svuotare o rompere la finestra. Esito: ok.
- `modules/memory/store.py:958` — `diario_per_tipo_dal`: query parametrizzata in sola lettura, filtra tipo e fonte esatti, `int(n)` dentro il try, `[]` con un warning in caso di degrado (§9). Esito: ok.
- `modules/memory/store.py:386` — contesto: `_now_iso()` è l'unico punto che scrive `ts` nel diario (riga 666), sempre `datetime.now(timezone.utc).isoformat()`. È lo stesso formato del limite calcolato in gas.py. Esito: ok (vedi domanda 3).
- `tests/test_unit_kernel.py:8812` — T90a–i. Coprono pertinenza, ripiego sul più recente, parità, scadenza, la variabile d'ambiente, l'esclusione di recap_notte, recap_non_fidato e fonte diversa da 'modello', e il passaggio attraverso run_turn. Ripristinano l'ambiente e `gas.OpenAI`. Esito: ok.
- `reports/setup_notte.md:58` — solo l'a capo, il contenuto non cambia. Esito: ok.

**Risposte alle tue domande**
1. **Il messaggio dell'utente influenza quale recap viene scelto: non è un problema.** Il messaggio sceglie solo tra recap già fidati (tipo 'recap', fonte 'modello', non scaduti). Non può far entrare testo nuovo, né recap_notte o recap_non_fidato (lo prova T90h). Su Telegram la chat è in whitelist, ed è l'operatore. Al massimo chi scrive può scegliere quale dei suoi recap fidati vedere: è una scelta, non un'iniezione.
2. **Il ripiego sul più recente: sì, va bene.** È il comportamento di prima ristretto alla finestra di validità, e senza recap validi non inietta niente. Unico limite: per via di R-348-1 il ripiego scatta meno spesso del previsto, perché quasi ogni frase ha una parola comune che fa punto.
3. **Il confronto dei timestamp come stringhe: va bene.** Entrambi i lati sono ISO in UTC con `+00:00` e prodotti dallo stesso metodo, quindi l'ordine come stringa coincide con quello cronologico. L'unica eccezione è dentro lo stesso secondo del limite: un `ts` senza microsecondi, ad esempio `…:00+00:00`, si ordina prima di `…:00.5+00:00`. Vuol dire uno scarto di meno di un secondo su una finestra di giorni, irrilevante. Diventerebbe un problema solo se un giorno qualcuno scrivesse `ts` in un altro formato (con `Z` o senza fuso): oggi non succede.

**Riserve**
- **R-348-1 (BASSA)**: mancano le parole vuote. Una parola comune di 4 o più lettere fa vincere un recap più vecchio anche quando non è pertinente. Rimedio possibile: un piccolo elenco di parole vuote italiane, oppure richiedere almeno 2 parole in comune. Va tracciata in stato_progetto.md.
- **R-348-2 (COSMETICA)**: `ultimo_diario_per_tipo` (`modules/memory/store.py:935`) non ha più chiamanti nel kernel. Inoltre `_parole_recap` è inserita in mezzo al blocco di commento R-200-1.

**Cosa NON ho verificato**: il comportamento con un modello reale e un diario vero sul Mac (nel container non ci sono chiavi né il DB dell'operatore). Non ho misurato l'effetto sulla cache dei prompt dei provider: il messaggio system ora può cambiare da un turno all'altro in base al messaggio. Non ho rieseguito `pytest tests/` per intero, ma solo la suite del kernel.

Memoria del revisore aggiornata con la riga #348 e committata (5014973). Nessuna lezione nuova.

File rilevanti:
- /home/user/Gas/gas.py
- /home/user/Gas/modules/memory/store.py
- /home/user/Gas/tests/test_unit_kernel.py
- /home/user/Gas/.claude/agents/memoria_revisore.md

### Review #349 (ri-review dopo R-348-1/2) — verdetto integrale

## VERDETTO: APPROVATO

Ri-review #349 sul diff staged completo (FASE 2.6 fetta 3). R-348-1 è chiusa, e anche la parte cosmetica di R-348-2. Ho rieseguito la suite del kernel: **868 PASS, 0 FAIL**. Ho provato anche una mutazione: con `RECAP_MIN_PAROLE = 1` fallisce solo T90c2 (867/1). Poi ho ripristinato gas.py, che non ha più differenze rispetto allo stage.

**Elementi del diff esaminati**
- `gas.py:782` — nuova costante di modulo `RECAP_MIN_PAROLE = 2`, con un commento che rimanda a R-348-1. Rischio: una costante di modulo non si cambia con una variabile d'ambiente. Non serve: è una soglia di qualità, non un tetto di spesa. Esito: ok.
- `gas.py:2883` — il ciclo parte da `punti = RECAP_MIN_PAROLE - 1` e scorre tutti i candidati dal più recente. Un recap prende il posto del più recente solo se ha almeno 2 parole in comune e supera strettamente il migliore trovato finora. Ho controllato tre casi limite:
  - il più recente ha 1 parola in comune e uno più vecchio ne ha 2: vince il vecchio, ed è corretto;
  - entrambi ne hanno 2: resta il più recente, come prova T90d;
  - nessuno raggiunge la soglia: il ripiego è `candidati[0]`, cioè il più recente.
  Il codice resta dentro il try fail-safe, e `_get_window` non è toccato. Esito: ok.
- `gas.py:774` — `_parole_recap` è stata spostata subito prima di `class GasKernel`, con `str(testo or "")` e una regex lineare. Il commento R-200-1 torna attaccato alla sua costante. Esito: ok.
- `tests/test_unit_kernel.py:8836` — T90c2: con «questo preventivo» c'è una sola parola in comune, quindi resta il recap più recente (Bianchi). La mutazione lo fa fallire, perciò il test morde davvero. Ho anche controllato che T90a («aggiorna il preventivo di Rossi») e T90i («preventivo Rossi?») abbiano esattamente 2 parole in comune: superano la soglia, quindi passano per la ragione giusta e non per caso. Esito: ok.
- `modules/memory/store.py:958` — `diario_per_tipo_dal` invariato rispetto alla #348: query in sola lettura, parametrizzata, restituisce `[]` se la memoria è degradata. Esito: ok.

**Riserve**: nessuna nuova. `ultimo_diario_per_tipo` (`modules/memory/store.py:935`) resta senza chiamanti nel kernel, ma lo usano i test T80/T89: tenerlo è giustificato, e per me la COSMETICA di R-348-2 si può chiudere.

**Cosa NON ho verificato**:
- la qualità della scelta su conversazioni reali in italiano: con 2 parole in comune possono ancora vincere coppie di parole comuni, ad esempio «questo» + «anche». Si vedrà solo usandolo sul Mac, e il danno massimo resta un recap fidato meno adatto;
- un modello reale e il DB vero: nel container non ci sono chiavi;
- `pytest tests/` per intero: ho rieseguito solo la suite del kernel.

Memoria del revisore aggiornata con la riga #349 e committata (f7494b6). Nessuna lezione nuova.

File:
- /home/user/Gas/gas.py
- /home/user/Gas/modules/memory/store.py
- /home/user/Gas/tests/test_unit_kernel.py
- /home/user/Gas/.claude/agents/memoria_revisore.md

### Review #350 (seguito bot #213 e verifica esterna #213) — verdetto integrale

## VERDETTO: APPROVATO CON RISERVE

Ho letto prima, come richiesto, CLAUDE.md (sez. 5, 8 e 9), le voci di reports/stato_progetto.md su R-199-3 e PR #213, e la coda di .claude/agents/memoria_revisore.md (#346–#349).

**Cosa ho controllato nel diff**
1. `gas.py:2886` — `_recap_pin` ora usa `next(...)` sul primo candidato con almeno `RECAP_MIN_PAROLE` parole in comune, altrimenti prende `candidati[0]`. Ho verificato che "primo" vuol dire davvero "più recente": `modules/memory/store.py:967` ordina per `id DESC` (contesto, file non toccato). Il filtro sulla scadenza e quello sulla fonte 'modello' restano a monte. Fail-safe intatto: lista vuota → "", e il try/except è invariato. Non c'è slicing della history e `_get_window` non è toccato. **ok**
2. `gas.py:2894` — l'intestazione del blocco ora è «# RECAP PERTINENTE ({ts})». Ho controllato che questo testo non compaia nel system prompt (REGOLA), così `_BLOCCO80` non può dare falsi positivi. **ok**
3. `tests/test_unit_kernel.py:8835` — T90c3 riproduce il caso del bot: recap vecchio con più parole in comune contro recap nuovo con 2 parole in comune. Prova di mutazione: ho rimesso il vecchio criterio "vince chi ha più parole" → 869 PASS e 1 FAIL, ed è proprio T90c3. Poi ho ripristinato `gas.py`: il diff staged non è cambiato. **ok**
4. `tests/test_unit_kernel.py:8875` — T90j verifica che il ts scritto da `append_diario` sia ISO, con fuso orario e finisca con '+00:00'. È coerente con `modules/memory/store.py:388` (`_now_iso`, contesto). Così si blocca il formato da cui dipende il confronto tra stringhe della scadenza. **ok**
5. `tests/test_unit_kernel.py:7011` — T80x controlla ancora `"RECAP DEL TASK" not in`. Ora è vacuo: quel testo non esiste più da nessuna parte. **riserva cosmetica**

**Riserve**
- **R-350-1 (COSMETICA)**: in `tests/test_unit_kernel.py:7011` sostituire «RECAP DEL TASK» con «RECAP PERTINENTE». La sostituzione è sicura perché il testo non compare nel system prompt. In alternativa si può togliere quella metà della condizione, che è già coperta da `_BLOCCO80`. Non blocca il commit: va tracciata in stato_progetto.md oppure sistemata in questa stessa fetta.

**Prove riprodotte**: kernel 870 PASS / 0 FAIL.

**Rischi esclusi**
- La scelta tra recap con conversazioni reali non è verificata. Preferire il più recente tra quelli pertinenti è una scelta di semantica che segue V-1 del bot. Resta il caso già dichiarato in R-199-3: due parole comuni generiche possono rendere "pertinente" un recap meno adatto.
- Non ho rilanciato `pytest tests/` per intero (1419): mi fido del dato dell'agente, perché il diff tocca solo `gas.py` e il file di test del kernel.
- Il caso limite del confronto tra stringhe quando il ts non ha microsecondi (`isoformat` senza frazione) cade solo sul confine dello stesso secondo, su una finestra di 7 giorni. È trascurabile e non l'ho testato.

**Memoria**: ho aggiunto la riga #350 a /home/user/Gas/.claude/agents/memoria_revisore.md, con questa lezione: quando si rinomina un marcatore testuale, cercare con grep anche le asserzioni «not in» col vecchio testo. L'ho committata con `scripts/commit_memoria_revisore.sh` (commit 9918f22, solo quel file). Il diff staged sotto review è rimasto intatto.

## §5 DELTA TEST DEL MOTORE

tests/test_unit_kernel.py in locale: 858 → 870 PASS, 0 FAIL (T90a–j, T90c2, T90c3). Blocco reale: `=== RIEPILOGO: 870 PASS, 0 FAIL ===`. In CI i conteggi sono +2 (860 su main 2592b61, test del profilo sandbox saltati in locale; V-3 bot #213).
pytest `tests/`: `1419 passed in 174.59s (0:02:54)` (dopo il seguito del bot, prima di T90j che è nel file script del kernel).

## §6 STATO CI

`gh` non disponibile nella sessione cloud: lo stato CI si legge dai check-run della PR via MCP GitHub.

- `5014973`, `f7494b6`, `0e8e29b`: pushati insieme prima dell'apertura della PR #213; nessuna run su questi SHA singolarmente.
- `d6cc594` (primo fine-task): handoff-check success; unit-suite e verifica-bot in corso alla verifica esterna; bot APPROVATO CON RISERVE (V-1 BASSA, V-2/V-3 COSMETICHE).
- `9918f22`, commit del seguito bot #213 e commit di fine-task (questo handoff): run non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- R-350-1 (COSMETICA): asserzione vacua in T80.
- R-ve213-3 (COSMETICA): effetto sulla cache dei prompt non misurato.
- Qualità della scelta su conversazioni reali non verificata (due parole comuni possono ancora rendere pertinente un recap).
- Già tracciate: R-345-3, R-bot210-3, R-bot211-2, R-ve211-1, R-ve211-2.
