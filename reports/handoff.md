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
- **Riga lunga in setup_notte.md (cosmetica bot #212)**: `FATTA`.
- **Prova con conversazioni reali**: `DEFERITA` — nessun DB né chiave nel container.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   2 ++
 gas.py                             |  52 ++++++++++++++++++++++++++++++++++++++++++----------
 modules/memory/store.py            |  17 +++++++++++++++++
 reports/diff_sessione.md           |  13 +++++++------
 reports/handoff.md                 | 121 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++-----------------------------------------------
 reports/roadmap.md                 |   2 +-
 reports/setup_notte.md             |   5 +++--
 reports/stato_progetto.md          |   4 ++--
 reports/ultimo_report.md           |  17 ++++++++---------
 tests/test_unit_kernel.py          |  71 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 10 files changed, 227 insertions(+), 77 deletions(-)
```

NB: conteggi di `reports/handoff.md` (e totali) presi prima del proprio commit.

## §3 GIT LOG --ONELINE (sessione)

```
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

## §5 DELTA TEST DEL MOTORE

tests/test_unit_kernel.py: 858 → 868 PASS, 0 FAIL (T90a–i, T90c2). Blocco reale: `=== RIEPILOGO: 868 PASS, 0 FAIL ===`.
pytest `tests/`: `1419 passed in 179.12s (0:02:59)` (prima della correzione R-348-1).

## §6 STATO CI

`gh` non disponibile nella sessione cloud: lo stato CI si legge dai check-run della PR via MCP GitHub.

- `5014973`, `f7494b6`, `0e8e29b`: pushati insieme prima dell'apertura della PR #213; run non ancora disponibile alla scrittura dell'handoff.
- Commit di fine-task (questo handoff): run non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- Qualità della scelta su conversazioni reali non verificata (due parole comuni possono ancora vincere).
- Già tracciate: R-345-3, R-bot210-3, R-bot211-2, R-ve211-1, R-ve211-2.
