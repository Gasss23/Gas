# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-11-17 — Voce: filtro sulla voce dell'operatore per «Hey Jarvis» + guida in giro (M1)

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR di questa sessione (nessuna riserva aperta oltre a R-804-3 COSMETICA).
2. Dopo il merge: registrare la voce sul Mac (`scripts/voce/registra_voce.py`, circa 5 minuti) e riprovare Jarvis.

---

## §1 SCOPE & ESITO FETTE

- **Fetta 1 — verificatore della voce** (taratura del 17/11 sul Mac: la voce normale dell'operatore arriva solo a 0,37-0,43 col modello hey_jarvis): FATTA — 3c25eeee, review #804-M1coord APPROVATO CON RISERVE; R-804-1/2 chiuse in 6219b621, review #805-M1coord APPROVATO.
- **Fetta 2 — guida «Gas in giro»** (`reports/guida_voce_in_giro.md`, solo documento): FATTA — 53cb2a12.
- **Fetta scartata — data e ora nel prompt a voce**: review #803-M1coord BOCCIATO (c'erano già dal V13, `modules/voice/server.py` `ora_per_voce`); codice non committato, resta solo la riga di memoria (0e85b335). Causa del giro in più del 17/11 16:28: da trovare con il diario.
- **Porting del fix bwrap (dalla PR #380, commit 605e154c)** per la CI su Ubuntu 26.04: FATTO — review #808-M1coord APPROVATO CON RISERVE (R-808-1 BASSA: meglio mergiare prima la #380). La #380 è stata mergiata il 18/11 e main è entrato nel branch: browser.py e il suo test ora coincidono con main e non sono più nel diff (R-808-1 chiusa).

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   5 ++
 clients/voice/ascolto.py           | 207 ++++++++++++++++++++++++++++++++++++++++++++++++++++-----
 reports/diff_sessione.md           |  22 +++---
 reports/guida_voce_in_giro.md      |  32 +++++++++
 reports/handoff.md                 | n/d
 reports/stato_progetto.md          |   1 +
 reports/ultimo_report.md           |  24 +++----
 scripts/voce/LEGGIMI.md            |  65 +++++++++++++++++-
 scripts/voce/registra_voce.py      | 573 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 scripts/voce/taratura_parola.py    |  65 ++++++++++++------
 tests/test_unit_voce_ascolto.py    | 568 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++-
```

NB: regola «n/d» — il conteggio di reports/handoff.md non è misurabile al momento della scrittura; riga di totale tolta.

## §3 GIT LOG --ONELINE (sessione)

```
2fe61b78 docs(fine-task): handoff col porting del fix bwrap (#808-M1coord)
ba62b507 fix(web): sandbox del browser su Ubuntu 26.04 (porting di 605e154c dalla PR #380) — review #808-M1coord
84d1b770 docs(fine-task): §2/§3 handoff
9ee2da5f docs(fine-task): riferimenti esterni nel verdetto #804 in forma leggibile da check_verdetto
02ec8635 docs(fine-task): §2/§3 handoff
176ef263 docs(fine-task): voce — filtro sulla voce dell'operatore (review #804/#805-M1coord)
53cb2a12 docs(voce): guida per usare Gas in giro (Telegram vocali, Comando Rapido iPhone)
0e85b335 chore(revisore): memoria review #803 — BOCCIATO
6219b621 fix(voce): verifica della voce mai ferma all'avvio con cartella illeggibile; test su proprietario e cartella (R-804-1/2) — review #805-M1coord
2a32f67a chore(revisore): memoria review #805 — APPROVATO
3c25eeee feat(voce): filtro sulla voce dell'operatore per «Hey Jarvis» (verificatore openWakeWord) + registrazione guidata — review #804-M1coord
1473e9c9 chore(revisore): memoria review #804 — APPROVATO CON RISERVE
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione.

## §4 VERDETTO DEL REVISORE (per commit motore)

### Review #804-M1coord (commit 3c25eeee)

## VERDETTO: APPROVATO CON RISERVE

Review #804-M1coord. Diff staged nella worktree del branch feat/voce-verifica-parlante (5 file). Letti prima CLAUDE.md, reports/stato_progetto.md (parti utili) e la memoria. Confronto col sorgente di openWakeWord 0.6.0 installato nell'area temporanea.

**Punti del diff esaminati**
- `clients/voice/ascolto.py:1370` — `_file_fidato` controlla file e cartella prima del caricamento con pickle. Rischi: symlink, proprietario diverso, file scrivibile da altri, TOCTOU. Percorso fisso (`percorso_verificatore`: radice + `.gas_voce/verifica` + nome `[a-z0-9_]{1,40}`): nessun path traversal. TOCTOU solo per chi può scrivere in `verifica`, che il controllo esclude: accettabile su un Mac a un utente. Esito: ok con riserva R-804-1. Mutanti: tolto il controllo symlink → 1 rosso; tolto il controllo permessi → 1 rosso; il controllo del proprietario (`if False`) e quello della cartella madre (`for q in (p,)`) **sopravvivono** (26 verdi).
- `clients/voice/ascolto.py:1432` — `custom_verifier_models` e `custom_verifier_threshold=soglia_base` a `Model`. Rischio: punteggio non verificato che attiva. openwakeword/model.py (righe 320-327): il verificatore sostituisce il punteggio solo dalla soglia base in su; con `clients/voice/ascolto.py:1470` (soglia della verifica mai sotto la base) un blocco non verificato non attiva. Esito: ok. Mutante `max(...,0.0)` → 1 rosso.
- `clients/voice/ascolto.py:1473` — anche la soglia dell'interruzione non scende sotto la base. Rischio: risposte non richieste mentre Gas parla. Con la verifica attiva l'eco di Gas viene scartata dal filtro; prezzo: l'operatore interrompe più a fatica (rischio dichiarato). Esito: ok. Mutante → 1 rosso.
- `clients/voice/ascolto.py:1441` — `rilevatore_con_verifica`: pkl che non si carica → fallback senza verifica (§9); numpy/openwakeword mancanti rilanciati come prima. In `main` lo stato passa a «non caricata» PRIMA di `_regolazioni` (soglia di nuovo 0,7). Un errore di `predict_proba` durante l'ascolto è catturato dal ciclo (`clients/voice/ascolto.py:490`): niente crash, ma Jarvis diventa sordo (direzione sicura), segnalato nel log. Esito: ok.
- Senza pkl comportamento identico a oggi: stato «assente» → stessa `Model(wakeword_models=[modello], inference_framework="onnx")`, stessa `GAS_ASCOLTO_SOGLIA` 0,7, stessa interruzione; cambia solo la riga di log. Esito: ok.
- `scripts/voce/registra_voce.py:306` — `MotoreOWW.blocchi` contro `get_reference_clip_features` (custom_verifier_model.py (righe 30-86)): stesso passo di 1280 campioni, stesso spostamento casuale 0-1280 con 5 ripetizioni, stesse feature `preprocessor.get_features(...)` che `predict` passa al verificatore. Negativi su tutti i blocchi (come `threshold=0.0`), positivi dalla soglia base invece che da 0,5; 1 s di silenzio in testa per i primi 5 blocchi azzerati; classificatore `train_verifier_model` della libreria. Esito: ok.
- `scripts/voce/registra_voce.py:104` e `scripts/voce/registra_voce.py:118` — privacy: cartelle 0700, file 0600 scritti in modo atomico (mkstemp + replace); clip di `say` a 0600 in cartella 0700; `.gas_voce/` in `.gitignore` (riga 23) con test. Esito: ok.
- Test: `tests/test_unit_voce_ascolto.py:3282` (file non fidato) e `tests/test_unit_voce_ascolto.py:3407` (verifica rotta/spenta/assente). Suite voce_ascolto rieseguita: 371 passed.

**Riserve**
- **R-804-1 BASSA**: proprietario (`st_uid`) e cartella madre (`clients/voice/ascolto.py:1377`) senza test (spegnerli lascia la suite verde).
- **R-804-2 BASSA**: `verifica_della_voce` chiamata fuori dal try in `main` (`clients/voice/ascolto.py:1544`): su Python 3.11/3.12 `Path.exists()`/`is_symlink()` rilanciano PermissionError; con `.gas_voce` non attraversabile l'ascolto crasha all'avvio.
- **R-804-3 COSMETICA**: la soglia base dell'addestramento è nel .json ma non confrontata a runtime.

**Non verificato**: Mac reale (microfono, `say`, launchd); qualità reale del filtro sulla voce dell'operatore; pkl fra versioni di scikit-learn; LEGGIMI letto in parte.

Wall of Shame: nessuna violazione; guardrail del kernel non toccati. Memoria: riga #804-M1coord e una lezione (commit 1473e9c9).

### Review #805-M1coord (commit 6219b621)

## VERDETTO: APPROVATO

Review #805-M1coord: R-804-1 e R-804-2 chiuse, nessuna riserva nuova. Diff staged nella worktree (2 file, da 3c25eeee).

- `clients/voice/ascolto.py:1408` — `exists()`/`is_symlink()` dentro `try/except OSError` → «non caricata» con avviso (`gas.ascolto`, riga 1414); il pkl non viene mai caricato in quel percorso; soglia di nuovo 0,7; solo OSError intercettato. Esito: ok, R-804-2 chiusa.
- `tests/test_unit_voce_ascolto.py:3304` — test su proprietario diverso (`os.getuid` monkeypatchato) e cartella `verifica` 0o777; permessi ripristinati nel `finally`. Mutanti: `if False` → 1 failed; `for q in (p,)` → 1 failed. Esito: ok, R-804-1 chiusa.
- `tests/test_unit_voce_ascolto.py:3323` — `Path.exists` che solleva PermissionError: stato, motivo e log controllati; mutante `except ZeroDivisionError` → 1 failed. Esito: ok.
- Suite voce_ascolto: 373 passed (rieseguita).

Non verificato: cartella davvero senza permessi su Mac con Python 3.11/3.12 (qui 3.13; test con monkeypatch). R-804-3 COSMETICA resta aperta. Memoria: riga #805-M1coord (commit 2a32f67a).

NB: nel verdetto #804 i due riferimenti alla libreria esterna openWakeWord (non nel repo) sono scritti come «(righe N-M)» invece di «file:N-M», perché check_verdetto accetta solo file del repo; il testo è altrimenti integrale.

### Review #808-M1coord (porting del fix bwrap di #380, commit 605e154c)

## §4bis VERDETTO DEL REVISORE SUL PORTING ORA IN MAIN (#808-M1coord)

Il codice di questo verdetto (modules/web/browser.py e il suo test) è arrivato in main con la #380, mergiata il 18/11: dopo il merge di main nel branch non è più nel diff di questa PR, quindi il verdetto sta fuori dal §4 (che check_verdetto confronta col diff). Testo integrale, invariato:

## VERDETTO: APPROVATO CON RISERVE

Review #808-M1coord. Porting del commit 605e154c (PR #380) in due branch: fix/voce-togli-parola e feat/voce-verifica-parlante. Letti prima CLAUDE.md, reports/stato_progetto.md e la memoria.

**Porting identico nei due posti.** Tolte le righe index, i due diff staged e `git show 605e154c` hanno lo stesso SHA-256 (5969695a…); i file interi in staging coincidono con `605e154c:file` (browser.py dfeae8f8…, test f4bbae85…). Staged solo i 2 file (+177/-5).

**Elementi esaminati**
- modules/web/browser.py:283 — `_programmi_fuori` segue i collegamenti di /usr/bin al massimo 16 volte e monta in sola lettura solo il file vero, più un `--symlink` per ogni collegamento intermedio. Rischio: allargare il sandbox. Si blocca se il genitore è un collegamento, se il percorso è fuori dalle radici ammesse, dentro /usr/local, dentro Gas o la home (anche col percorso vero); collegamento rotto, ciclo o catena troppo lunga non espongono niente. — ok
- modules/web/browser.py:278 — radici ammesse solo `/usr` e `/etc/alternatives`; /usr/local escluso; si espone file per file, mai cartelle. — ok
- modules/web/browser.py:325 — solo un file vero ed eseguibile; una modifica a metà lettura finisce in `except OSError` e il programma viene saltato senza crash. — ok
- modules/web/browser.py:397 — il controllo parte dopo i montaggi esposti e prima del tmpfs su Gas e home: i protetti restano coperti. — ok
- tests/test_unit_web_browser.py:477 — `test_programmi_fuori_espone_solo_catene_ammesse`: 8 casi negativi più la catena buona; eseguito qui: PASS. — ok
- tests/test_unit_web_browser.py:395 — `_catene_di_usr_bin` amplia l'elenco dei file permessi nel test, calcolato dall'host: allentamento voluto e proporzionato (solo /usr/ e /etc/alternatives/ fuori da /usr/local/). — ok

**Test nel container (bwrap assente):** a HEAD 33 failed, 11 passed; col porting 34 failed, 12 passed (+1 test nuovo con bwrap, +1 senza). Gli altri fallimenti dipendono da bwrap assente.

**Wall of Shame:** nessuna violazione; kernel non toccato.

**Riserve:** R-808-1 BASSA — le due PR voce portano un fix del browser estraneo al loro tema: meglio mergiare prima la #380, poi riportare main (modifica identica, niente conflitti); nel report va detto che il fix arriva da #380.

**Rischio escluso:** comportamento reale nel sandbox su Ubuntu 26.04 non verificato (bwrap assente): fa fede la CI di #380 (unit-suite success); merito del fix già revisionato nell'altra chat.

**Memoria:** riga #808-M1coord e una lezione (commit 50fade22 su fix/voce-togli-parola).

## §5 DELTA TEST DEL MOTORE

- `python -B -m pytest -q tests/test_unit_voce_ascolto.py` → 346 passed (main 01eb9f5) → 371 (3c25eeee) → 373 passed (6219b621).
- `tests/test_unit_voice_server.py`: 236 passed (agente, dopo 3c25eeee).
- Resto di `tests/` (agente): 3812 passed, 33 failed tutti in `test_unit_web_browser.py` (bwrap assente nel container, identico su main).
- Prova reale del verificatore (agente, modello vero, voci espeak): voce addestrata non vista 0,70-0,96; voci femminili/inglesi 0,19-0,34; 3 maschili italiane su 4 passano (0,83-0,93).

```
373 passed
```

## §6 STATO CI

CI NON VERIFICATA (gh assente): run della PR non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- R-808-1 BASSA — il fix bwrap della #380 viaggia anche qui: meglio mergiare prima la #380.
- R-804-3 COSMETICA — la soglia base dell'addestramento non è confrontata a runtime.
- Limiti dichiarati: voci maschili simili all'operatore passano; una registrazione dell'operatore riprodotta passa; pkl legato alla versione di scikit-learn (ritorna senza verifica, si rifà con `--solo-addestra`); `say` del Mac non provato su Mac reale; interruzione (0,8 × 3 blocchi) raggiunta di rado col verificatore.
- Licenza CC BY-NC-SA di hey_jarvis: decisione dell'operatore ancora aperta.
