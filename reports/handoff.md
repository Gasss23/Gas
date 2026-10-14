# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-10-14 — D5: copie di cartelle e file di chiavi

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #210 (https://github.com/Gasss23/Gas/pull/210): tocca il cancello, decide l'operatore.
2. Secondo passaggio claude.ai facoltativo (D5 nasce già da quello su #204).

(`gh` non disponibile nella sessione cloud: numero/URL della PR presi dall'esito reale di `create_pull_request` via MCP GitHub.)

---

## §1 SCOPE & ESITO FETTE

- **Copie di cartella con altri nomi** (MEDIA claude.ai #204): `FATTA`.
- **Tetto 255 prima delle regex**: `FATTA`.
- **Bot #210 V-1/V-2**: `FATTA` — review #344.
- **Verifica esterna #210 V-1/V-2** (lista chiusa, coerenza): `SALTATA` — tracciate come R-ve210-1/2.
- **Backslash su Windows** (BASSA): `SALTATA` — Gas gira su Linux/Mac; tracciata.
- **Cartelle innocue key/, token/, shadow/** (BASSA): `SALTATA` — nessuna nel repo; tracciata.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |  2 ++
 modules/gate/gate.py               | 27 ++++++++++++++++++++++++---
 reports/diff_sessione.md           |  8 +++++---
 reports/handoff.md                 | 84 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++----------------------
 reports/stato_progetto.md          |  3 ++-
 reports/ultimo_report.md           | 22 +++++++++++++++-------
 tests/test_unit_gate.py            | 21 ++++++++++++++++++---
 7 files changed, 128 insertions(+), 39 deletions(-)
```

NB: conteggi di `reports/handoff.md` (e totali) presi prima del proprio commit.

## §3 GIT LOG --ONELINE (sessione)

```
d05cadf Merge origin/main in feat/gate-d5-copie-cartelle (conflitti sui report dopo #209)
854347b docs(fine-task): report e handoff — bot e verifica esterna #210
4816117 fix(gate): parole di copia uguali in prefisso e suffisso, cifre attaccate (bot #210)
9f255ba chore(revisore): memoria review #344 — APPROVATO
31ffae0 docs(fine-task): report e handoff — D5 (PR #210)
0b03da5 feat(gate): D5 — copie di cartelle e file di chiavi con qualsiasi nome comune
590eaaa chore(revisore): memoria review #343 — APPROVATO
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione.

## §4 VERDETTO DEL REVISORE (per commit motore)

### Review #343 (commit D5) — verdetto integrale

## VERDETTO: APPROVATO

Ho letto CLAUDE.md, le sezioni di reports/stato_progetto.md (solo i titoli, con Grep) e la memoria del revisore. Ho esaminato il diff staged e ho scritto sonde con Write, eseguite sia su Python 3.11.17 (versione minima del progetto, usata dalla CI) sia su 3.13.

Elementi del diff esaminati:
- `modules/gate/gate.py:331-345` — `_COPIA_SUFFISSI` e `_nome_con_copie` usano un gruppo atomico `(?>…)*+` con quantificatore possessivo. Rischio esaminato: backtracking esponenziale e supporto del `re` alla versione minima. Il codice compila e gira su 3.11.17 (le costruzioni atomiche esistono dalla 3.11, e la CI usa 3.11). Con 8 input ostili da circa 255 caratteri (`keys` seguito da ` copy` ripetuto, `(1)`, `-_`, spazi, `.1`, cifre, `old-` ripetuto) ogni ricerca dura al massimo 0,03 ms. Esito: ok.
- `modules/gate/gate.py:367-369` — il tetto dei 255 caratteri viene controllato prima di tutte le regex. Rischio esaminato: cambio di esito per un pezzo lungo in ultima posizione. Non cambia nulla, perché il ciclo a `modules/gate/gate.py:383` negava già ogni pezzo con più di 255 caratteri. Sulla nuova versione sia `keys` + 300 spazi sia `a/` + 300 `z` danno True. Esito: ok. Riserva cosmetica: ora ci sono due controlli identici, e quello del ciclo (`modules/gate/gate.py:383`) è codice morto. Si può togliere in una fetta successiva.
- `modules/gate/gate.py:331-345` (falsi positivi) — risultati della sonda. Restano liberi: `keys.d/x`, `oldkeys/x`, `keynote copy.md`, `key-value/x`, `keys.md`, `tokens.md`, `keys-2024.md`, `keys_`, `keys1.md`. Sono bloccate le varianti volute: `keys copy`, `keys (1)`, `keys 2`, `backup keys`, `copy_tokens (3)~`, `keys.new`, `passwd.bak.old`, `shadow2`. Esito: ok. Nota: `keys.json`, `keys.txt` e `keys.env` risultano bloccati. Non è un effetto di D5 (nessun suffisso di D5 vi corrisponde): dipende da regole preesistenti che non ho tracciato.
- `tests/test_unit_gate.py:635-646` e `tests/test_unit_gate.py:679-697` — nuovi casi: copie negate (lettura e scrittura), cartelle copia con documentazione leggibili ma mai scrivibili, e nomi simili che restano scrivibili. I casi coprono sia i blocchi sia i falsi positivi. Esito: ok. `pytest tests/test_unit_gate.py` dà 590 passed, come dichiarato.

Rischio escluso, non verificato:
- Non ho rieseguito il confronto sulle 180 voci reali contro origin/main: mi fido della misura dichiarata, ma non l'ho riprodotta.
- Non ho eseguito `pytest tests/` completo (1406 passed dichiarati). Su Python 3.11 non c'è pytest installato, quindi la suite gate l'ho eseguita solo su 3.13. Su 3.11 ho verificato solo che il modulo compili e che le sonde diano gli stessi risultati.
- Non ho verificato il comportamento su VPS.

Memoria aggiornata con la riga #343 (il massimo precedente era #342).

### Review #344 (fix bot #210) — verdetto integrale

## VERDETTO: APPROVATO

Ho letto CLAUDE.md, la memoria del revisore e lo stato del progetto. Ho riprodotto la suite del gate: 598 passed.

Elementi del diff esaminati:
- `modules/gate/gate.py:337` — `_PAROLE_COPIA` è una lista chiusa (copy, copia, backup, bak, old, orig, new, prev, save) con `[0-9]*+` possessivo. Rischio: backtracking e cifre attaccate alla parola. Esito: ok. Il possessivo non lascia nulla da riprovare e non c'è nidificazione di quantificatori ambigui.
- `modules/gate/gate.py:338` — i suffissi usano `_PAROLE_COPIA` oppure `v?[0-9]+` dentro `(?>...)*+`. Rischio: ReDoS e falsi positivi. Esito: ok. Su input ostili da 205-256 caratteri il tempo è ≤0,07 ms. L'unica eccezione è `keys` seguito da 250 trattini, che ha richiesto 1,7 ms: è lineare, non esponenziale.
- `modules/gate/gate.py:340` — il prefisso ora usa la stessa lista e richiede un separatore. Rischio: falsi positivi nuovi. Esito: ok. `oldkeys/`, `newkeys/`, `savekeys/`, `previous_keys/`, `saved_keys/` e `keys_new_item/` restano leggibili.
- `tests/test_unit_gate.py:646` — otto nuovi casi negati: `new_keys`, `orig_keys`, `keys.bak1`, `keys_old2`, `keys copy2`, `keys_v2`, `keys.prev`, `keys.save`. Rischio: copertura. Esito: ok. Tutti negati anche nella mia sonda.
- `modules/gate/gate.py:333` — commento corretto: lista chiusa, diversa da D3. Chiude la V-2 del bot. Esito: ok.

Sonda mia, con uno script scritto con Write:
- Negati come atteso (16): anche `keys.v2`, `keys-old-2`, `prev keys`, `save2_keys`, `tokens.bak2`, `shadow.orig3`, `passwd.new1` e `keys_copy2_v3`.
- Liberi come atteso (16): `keys.d`, `oldkeys`, `newkeys`, `savekeys`, `keys_vault`, `keynote copy.md`, `keys.save.md`, `dati/keys_list.md`, `keys_final`, `keys.vx`, `keys_v`, `tokens.md`, `keys.md`.

Non verificato: i 183 percorsi reali confrontati con origin/main. Mi fido della tua misura, non l'ho rieseguita. Non ho nemmeno provato Python 3.13: la sintassi possessiva/atomica è la stessa già approvata in #343.

Guardrail (cap 10 iterazioni, `_get_window`, tool simulati): non toccati dal diff. Il comportamento resta fail-closed.

Memoria aggiornata: riga #344 (massimo precedente #343) e commit eseguito con `commit_memoria_revisore.sh`.

## §5 DELTA TEST DEL MOTORE

tests/test_unit_gate.py: 565 → 590 → 598 passed (bot #210). Mutazione: con `modules/gate/gate.py` di origin/main `20 failed, 570 passed`.

pytest `tests/`: `1406 passed in 180.35s (0:03:00)`.

## §6 STATO CI

`gh` non disponibile nella sessione cloud: lo stato CI si legge dai check-run della PR via MCP GitHub.

- `0b03da5`: run 38654132272 failure (handoff-check rosso atteso: il commit di codice precede quello dei report), unit-suite success.
- `854347b`: unit-suite e handoff-check success; bot APPROVATO CON RISERVE (neutral).
- Merge di main (dopo #209) per risolvere i conflitti sui report: nessuna run al momento della scrittura.
- `31ffae0`: unit-suite e handoff-check success, verifica-bot neutral (bot APPROVATO CON RISERVE).
- `9f255ba` e il fix del bot: nessuna run su questi SHA (pushati col fine-task).
- Commit `chore(revisore): memoria review #343` e `feat(gate): D5`: nessuna run su questi SHA (pushati prima dell'apertura della PR #210).
- Commit di fine-task (questo handoff): run non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- R-claude204-2 (BASSA, backslash su Windows), R-claude204-3 (BASSA, cartelle innocue key/token/shadow), cosmetica review #343 (tetto 255 doppio), R-ve210-1/2 (BASSA), R-bot210-2 (BASSA, costo quadratico limitato): in `reports/stato_progetto.md`.
