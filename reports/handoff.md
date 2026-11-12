# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-11-12 notte — Voce: perché «Hey Jarvis» non risponde (misura col modello vero) + correzione (M1)

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR di questa sessione (riserve solo BASSE).
2. Compromesso da confermare: con 1 blocco i falsi sui quasi-omofoni («hey Jervis», «hey Chavez») salgono da 3 a 9 su 120 frasi di prova; le frasi comuni restano a ~0. In cambio le chiamate vere prese salgono da 19 a 35 su 81 (prova di 5 chiamate: da 2/5 a 5/5). sì/no
3. Dopo il merge: taratura sulla voce vera (`python3 scripts/voce/taratura_parola.py --chiamate 5`).

---

## §1 SCOPE & ESITO FETTE

- **Fetta 1 — misura col modello vero (hey_jarvis onnx) su voci sintetiche**: FATTA — reports/voce_taratura_2026-11-12.md.
- **Fetta 2 — predefinito 1 blocco (soglia 0,7), «sopra soglia» nella riga quasi, scripts/voce/taratura_parola.py**: FATTA — 0ce03e55, review #795-M1coord e #796-M1coord APPROVATO CON RISERVE.
- **Fetta 3 — R-796-1/2 (avviso «più permissiva», test d'uguaglianza)**: FATTA — 045707c8, review #797-M1coord APPROVATO CON RISERVE.
- **Fetta 4 — R-797-1 (ramo irraggiungibile)**: FATTA — d12e9b67, review #798-M1coord APPROVATO CON RISERVE.
- **Fetta 5 — bot #378 (82eb3bd) V-1 MEDIA: interruzione su 3 blocchi separata; V-2 script della misura; V-3/V-4**: FATTA — review #800-M1coord APPROVATO CON RISERVE (R-800-1 BASSA).

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md      |   7 ++++++
 clients/voice/ascolto.py                |  64 ++++++++++++++++++++++++++++++++++++++-------------
 reports/diff_sessione.md                |  15 ++++++------
 reports/handoff.md                      | n/d
 reports/stato_progetto.md               |   1 +
 reports/ultimo_report.md                |  18 +++++++--------
 reports/voce_taratura_2026-11-12.md     |  39 +++++++++++++++++++++++++++++++
 scripts/voce/LEGGIMI.md                 |  10 +++++---
 scripts/voce/diagnosi_ascolto.py        |  12 ++++++----
 scripts/voce/misura_parola_sintetica.py | 125 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 scripts/voce/taratura_parola.py         | 189 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 tests/test_unit_voce_ascolto.py         | 182 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++------
```

NB: regola «n/d» — il conteggio di reports/handoff.md non è misurabile al momento della scrittura; riga di totale tolta.

## §3 GIT LOG --ONELINE (sessione)

```
0d464e11 docs(fine-task): handoff #378 dopo il fix del bot
3286da4e fix(voce): interruzione su 3 blocchi separata dalla parola, misura riproducibile (bot #378 V-1..V-4) — review #800-M1coord
b6421da1 chore(revisore): memoria review #800 — APPROVATO CON RISERVE
82eb3bd6 docs(fine-task): §2/§3 handoff
5512ede8 docs(fine-task): voce — 1 blocco e taratura (review #795-#798-M1coord)
d12e9b67 refactor(voce): taratura senza il ramo irraggiungibile (R-797-1) — review #798-M1coord
032542c7 chore(revisore): memoria review #798 — APPROVATO CON RISERVE
045707c8 fix(voce): taratura — avviso «più permissiva» in ogni ramo, test d'uguaglianza della soglia (R-796-1/2) — review #797-M1coord
e7a4a42f chore(revisore): memoria review #797 — APPROVATO CON RISERVE
0ce03e55 fix(voce): «Hey Jarvis» su 1 blocco (3 dimezzavano le chiamate), taratura sulla voce vera, «sopra soglia» nella riga quasi — review #795/#796-M1coord
0365386b chore(revisore): memoria review #796 — APPROVATO CON RISERVE
dff590da chore(revisore): memoria review #795 — APPROVATO CON RISERVE
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione.

## §4 VERDETTO DEL REVISORE (per commit motore)

### Review #795-M1coord (commit 0ce03e55, 1° giro)

## VERDETTO: APPROVATO CON RISERVE

Review #795-M1coord, diff staged su fix/voce-blocchi-taratura. Letti prima CLAUDE.md §5, le parti voce di stato_progetto.md e la memoria del revisore. Suite voce_ascolto + voice_server: 568 passed (con `python -B`, `__pycache__` delle verifiche a mano pulito). Nessun antipattern del Wall of Shame.

**Elementi esaminati**
- clients/voice/ascolto.py:134 — `BLOCCHI_PAROLA_PREDEFINITO` da 3 a 1, soglia 0,7. Rischio: attivazione su un picco isolato, contro «zero risposte non richieste». La misura in reports/voce_taratura_2026-11-12.md lo giustifica (3 blocchi 19/81, 1 blocco 35/81; frasi comuni ~0 a ogni regola); costo dichiarato: quasi-omofoni falsi da 3 a 9. Esito: ok, compromesso da scrivere nell'handoff come scelta dell'operatore.
- clients/voice/ascolto.py:480 — `quasi_sopra = max(quasi_sopra, sopra)`, azzerato alle righe 460 e 467, passato a `_segnala_quasi` (riga 491, default 0, chiamante unico). Rischio: valore della salita prima. Esito: ok.
- clients/voice/ascolto.py:1330 — `_scrivi_regolazioni` avvisa ancora su soglia < 0,7 e turni oltre il predefinito; il ramo sui blocchi non scatta più (minimo 1): innocuo. Chi ha `GAS_ASCOLTO_BLOCCHI_PAROLA=3` nel .env non riceve avvisi (più severo): lo dice la riga «regolazioni in uso» e LEGGIMI.md:139. Esito: ok.
- clients/voice/ascolto.py:560 e clients/voice/ascolto.py:815 — finestra dopo un turno e interruzione usano lo stesso `blocchi_parola`: anche lì basta un blocco; si perde «un picco isolato non interrompe» (bot #371 V-1). Restano la soglia d'interruzione 0,8 e la finestra spenta di default (`MAX_TURNI_PREDEFINITO=1`). Esito: riserva R-795-3.
- scripts/voce/diagnosi_ascolto.py:41 — gruppo opzionale «(\d+) di fila sopra soglia», gruppi rinumerati alla riga 144; provato sui 3 formati: `sopra` None, None, 2; taciute e max giusti. Esito: ok.
- scripts/voce/taratura_parola.py:51-77 — `salite()`: sequenza [0,.4,.9,.2,.2,.8,.8,0×5,.35]: le prime due salite vicine si uniscono (massimo 0,9, 2 blocchi di fila sopra ogni soglia); contatore azzerato nella pausa. Esito: ok.
- scripts/voce/taratura_parola.py:86-118 — `consiglio()` chiede che scattino TUTTE le salite, rumore compreso: una salita di rumore a 0,55 porta a consigliare 0,5 senza dirlo; una a 0,35 porta a «Nessuna regolazione le prende tutte». Esito: riserva R-795-1.
- scripts/voce/taratura_parola.py:157-164 — `chiudi()` nel `finally`: microfono chiuso anche con Ctrl-C; `Microfono()` che fallisce → esito 1 e messaggio; errore di lettura → traceback dopo la chiusura (accettabile). Privacy: solo numeri, nessun audio su disco. Esito: ok.

**Riserve**
- **R-795-1 MEDIA**: `consiglio()` tratta ogni salita da 0,3 in su come chiamata voluta: un rumore può far consigliare una soglia sotto 0,7 senza avviso. Correzioni: mai sotto i predefiniti senza scriverlo; con `--chiamate` e più salite, avvisare.
- **R-795-2 BASSA**: docstring in clients/voice/ascolto.py:46 dice ancora «(default 3)».
- **R-795-3 BASSA**: blocchi=1 vale anche per interruzione e finestra dopo un turno: dichiararlo o separare il conteggio in una fetta successiva.

**Rischio escluso**: voce vera e microfono del Mac non verificati; misura del report non riprodotta (niente microfono né modello qui); suite intera del motore non eseguita.

**Memoria**: riga #795-M1coord e una lezione in .claude/agents/memoria_revisore.md (commit dff590da).

### Review #796-M1coord (2° giro, stesso commit 0ce03e55)

## VERDETTO: APPROVATO CON RISERVE

Re-review #796-M1coord, secondo giro di #795, diff staged (7 file). R-795-1 e R-795-2 chiuse; restano due riserve BASSE. Rieseguiti gli 11 test di taratura e della riga «quasi» (passano).

**Elementi esaminati**
- scripts/voce/taratura_parola.py:104 — salite con massimo sotto 0,5 escluse dal consiglio e dichiarate; solo salite deboli → stop alla riga 111 senza consiglio. Esito: ok, R-795-1 chiusa nel caso principale.
- scripts/voce/taratura_parola.py:98 — più salite delle `--chiamate` attese → avviso «probabilmente rumore». Esito: ok.
- scripts/voce/taratura_parola.py:128 — soglia consigliata sotto 0,7 → avviso esplicito. Esito: ok; scoperto il ramo «nessuna regolazione le prende tutte» (scripts/voce/taratura_parola.py:134) → R-796-1.
- scripts/voce/taratura_parola.py:31 — `SOGLIA_PREDEFINITA = 0.7` copiata da clients/voice/ascolto.py:133 senza test d'uguaglianza → R-796-2.
- clients/voice/ascolto.py:46 — docstring «(default 1)». Esito: ok, R-795-2 chiusa.
- R-795-3 e il compromesso (3 → 9 su 120 quasi-omofoni) dichiarati in reports/stato_progetto.md e reports/voce_taratura_2026-11-12.md: ok; il compromesso va riportato nell'handoff come decisione da confermare.

**Riserve aperte**: **R-796-1 BASSA** avviso mancante nel ramo «la migliore» (scripts/voce/taratura_parola.py:134-138); **R-796-2 BASSA** `SOGLIA_PREDEFINITA` duplicata senza test; **R-795-3 BASSA** (dichiarata).

**Rischio escluso**: voce vera e microfono non verificabili; misure del report non riprodotte.

**Memoria**: riga #796-M1coord (commit 0365386b).

### Review #797-M1coord (commit 045707c8)

## VERDETTO: APPROVATO CON RISERVE

Review #797-M1coord: delta su #796, diff staged di 2 file. R-796-1/2 chiuse nel codice, ma il ramo «nessuna regolazione le prende tutte» non è più raggiungibile e il test nuovo non lo prova.

**Elementi esaminati**
- scripts/voce/taratura_parola.py:135 — avviso «più permissiva» dopo i due rami; `t` definito in entrambi; uscite anticipate alle righe 91 e 112 senza salite. Esito: ok, R-796-1 chiusa.
- tests/test_unit_voce_ascolto.py:3178 — `t.SOGLIA_PREDEFINITA == a.SOGLIA_PREDEFINITA`. Esito: ok, R-796-2 chiusa.
- tests/test_unit_voce_ascolto.py:3180-3185 — la sequenza (0,55/0,58/0,65/0,95) passa dal ramo «Consiglio … prende tutte le chiamate», non dal secondo: dopo il filtro (scripts/voce/taratura_parola.py:104) ogni salita ha massimo ≥ 0,5, quindi con 0,5 e 1 blocco scattano tutte e il ramo `else` (scripts/voce/taratura_parola.py:128) è morto. Stesso per test_taratura_senza_regolazione_perfetta_dice_la_migliore (tests/test_unit_voce_ascolto.py:3127). Esito: **R-797-1 BASSA** — togliere il ramo o dichiararlo; rinominare i test.

**Rischio escluso**: suite completa non rilanciata (343 dichiarati); voce vera non verificabile.

**Memoria**: riga #797-M1coord e una lezione (commit e7a4a42f).

### Review #798-M1coord (commit d12e9b67)

## VERDETTO: APPROVATO CON RISERVE

Review #798-M1coord su R-797-1. Diff staged: scripts/voce/taratura_parola.py e tests/test_unit_voce_ascolto.py. R-797-1 chiusa; una riserva BASSA nuova.

**Elementi esaminati**
- scripts/voce/taratura_parola.py:122-129 — ramo `else` tolto, commento col perché, `max(tutte)` diretto. Rischio: `max()` su lista vuota. Invariante: ogni salita rimasta ha `massimo >= 0,5`, che viene da un blocco con `p >= 0,5` (`salite()`, scripts/voce/taratura_parola.py:64-68) → `di_fila[0.5] >= 1` → con 0,5 e 1 blocco scattano tutte, `tutte` mai vuota. Esito: ok, ma l'invariante regge solo finché `BLOCCHI` contiene 1 e il filtro usa `min(SOGLIE)` → R-798-1.
- scripts/voce/taratura_parola.py:130 — avviso «più permissiva» su percorso unico. Esito: ok.
- scripts/voce/taratura_parola.py:88 — docstring coerente. Esito: ok.
- tests/test_unit_voce_ascolto.py:3127 e tests/test_unit_voce_ascolto.py:3177 — nomi e asserzioni coerenti col ramo provato. Esito: ok. 8 test di taratura passano.

**Riserva**: **R-798-1 BASSA** — `max(tutte)` dipende da un invariante non scritto: cambiando `BLOCCHI` o il filtro, `ValueError`. Difesa: `assert tutte` col commento o un test su `1 in BLOCCHI` e `min(SOGLIE)`.

**Rischio escluso**: voce vera e microfono non verificabili; suite completa non rilanciata.

**Memoria**: riga #798-M1coord (commit 032542c7).

### Review #800-M1coord (fix bot #378 V-1..V-4 su 82eb3bd)

## VERDETTO: APPROVATO CON RISERVE

Review #800-M1coord, diff staged nella worktree del branch fix/voce-blocchi-taratura (PR #378). Lette le ultime righe della memoria del revisore e il contesto voce di stato_progetto.md. tests/test_unit_voce_ascolto.py rieseguito: **344 passed**.

**Elementi del diff esaminati**
- `clients/voice/ascolto.py:827` — mentre Gas parla contano i `blocchi_interruzione`, non i `blocchi_parola`. Rischio: la parola su 1 blocco annulla la protezione contro l'eco della #371 (V-1 MEDIA del bot). Il conto `sopra` si azzera sotto soglia e su errore. — **ok**
- `clients/voice/ascolto.py:378` e `clients/voice/ascolto.py:396` — parametro nuovo del costruttore, `Optional[int]`; `None` = come la parola (test esistenti invariati); minimo 1; type hint. — **ok**
- `clients/voice/ascolto.py:1327` — `GAS_ASCOLTO_BLOCCHI_INTERRUZIONE` letta con `_numero`, limiti 1-5, al costruttore via `**regolazioni` (`clients/voice/ascolto.py:1400`); `tests/test_unit_voce_ascolto.py:201` verifica 3; log e avviso sotto 3 coperti da `tests/test_unit_voce_ascolto.py:2927` e `:2938`. — **ok**
- `clients/voice/ascolto.py:490` — `quasi_sopra` aggiornato solo con punteggio >= SOGLIA_QUASI (V-3 BASSA): ramo già irraggiungibile, modifica difensiva senza cambio di comportamento; manca un test, accettabile. — **ok**
- `tests/test_unit_voce_ascolto.py:3195` — il test nuovo verifica solo i due attributi, non che con parola=1 e interruzione=3 uno o due blocchi alti non fermino Gas; il percorso di `_ascolta_mentre_suona` resta coperto dal test della #371 (`tests/test_unit_voce_ascolto.py:2781`) con `blocchi_parola=3`, cioè con i due valori uguali. — **riserva (R-800-1)**
- `scripts/voce/misura_parola_sintetica.py:51` — script di misura fuori dai test; espeak-ng e ffmpeg con elenco di argomenti, senza shell. — **ok**

Nessun problema del Wall of Shame.

**Riserve**
- **R-800-1 BASSA** — manca un test di comportamento con `blocchi_parola=1` e `blocchi_interruzione=3` (1-2 blocchi alti mentre Gas parla non interrompono, 3 di fila sì): una regressione che rimetta `blocchi_parola` alla riga 827 passerebbe i test. Tracciare in stato_progetto.md o chiudere con un test.

**Rischi esclusi**: script di misura non eseguito dal revisore (servono modello onnx ed espeak-ng; numeri presi dall'esecuzione del coordinatore); eco reale sul Mac non verificabile; LEGGIMI e report solo scorsi.

**Memoria**: riga #800-M1coord nella worktree (commit b6421da1).

## §5 DELTA TEST DEL MOTORE

- `python -B -m pytest -q tests/test_unit_voce_ascolto.py` → 332 passed (main 3756c97) → 343 passed (d12e9b67) → 344 passed (fix bot #378).
- `scripts/voce/misura_parola_sintetica.py` eseguito: stessi numeri del report (35/81 contro 19/81; falsi 9 contro 3 su 120).
- `tests/test_unit_voice_server.py` insieme a voce_ascolto: 568 passed dopo 0ce03e55 (prima dei fix di R-795-1).
- Kernel non toccato.

```
343 passed
```

## §6 STATO CI

CI letta con lo strumento GitHub sulla PR #378: 82eb3bd unit-suite e handoff-check success; verifica-bot failure (V-1 MEDIA, V-2/V-3 BASSE, V-4 COSMETICA: corrette nel commit successivo). Run del commit finale non ancora disponibile.

## §7 RISERVE APERTE

- R-795-3 → chiusa (bot #378 V-1): interruzione mentre Gas parla su 3 blocchi (`GAS_ASCOLTO_BLOCCHI_INTERRUZIONE`).
- R-800-1 BASSA — manca un test di comportamento con parola=1 e interruzione=3.
- R-798-1 BASSA — `max(tutte)` in `consiglio()` dipende da un invariante non scritto (1 in BLOCCHI, filtro a min(SOGLIE)).
- Compromesso sui quasi-omofoni (decisione in §0).
- Non provato: voce vera dell'operatore e microfono del Mac (misure su voci sintetiche).
