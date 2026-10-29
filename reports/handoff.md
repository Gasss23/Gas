# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-10-29 — Voce V1: cervello forte dalla voce (chat M2, coordinata da M1)

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #304 (https://github.com/Gasss23/Gas/pull/304). Numero e URL dalla risposta JSON dell'integrazione GitHub (`create_pull_request`: `{"id":"5073160064","url":"https://github.com/Gasss23/Gas/pull/304"}`); `gh` nel cloud non è autenticato. Merge da solo SOLO con verdetto del bot APPROVATO pulito; con riserve decide l'operatore (tramite M1).
2. Facoltativo: `GAS_VOCE_FORTE=1` nel `.env` del Mac per mandare tutta la voce al cervello forte (spento di default).

---

## §1 SCOPE & ESITO FETTE

- **V1.1 — verifica del giro vocale e proposta a M1**: `FATTA` — il forte passava solo con «/forte», che a voce non si detta; M1 ha scelto parola chiave + interruttore.
- **V1.2 — parola chiave parlata «forte …» / «Gas forte …»**: `FATTA` — `cervello_voce()` in `modules/voice/server.py`, solo sul testo trascritto, fail-closed («uso» → 400).
- **V1.3 — `GAS_VOCE_FORTE`**: `FATTA` — tutta la voce al forte; forte fermo → errore dichiarato, mai i gratuiti.
- **V1.4 — test di trascrizione e sintesi nei test automatici**: `FATTA` — già in CI dalla PR #229 (riga R8 corretta); chiusa R-384-1 (test indipendenti dal proxy).
- **gas.py / brains/ / doctor**: `SALTATA — fuori dal mandato di M1`.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   1 +
 modules/voice/server.py            |  43 +++++++++++++++++++++++++++++++++++++++----
 reports/diff_sessione.md           |  11 +++++++----
 reports/handoff.md                 | n/d
 reports/roadmap.md                 |   3 ++-
 reports/stato_progetto.md          |   1 +
 reports/ultimo_report.md           |  35 ++++++++++++++---------------------
 tests/test_unit_voice_server.py    | 107 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++---
 tests/test_unit_voice_stt.py       |  38 +++++++++++++++++++++++++++++++++++++-
```

NB: regola «n/d» — il conteggio di `reports/handoff.md` non è misurabile mentre lo si scrive; riga di totale tolta.

## §3 GIT LOG --ONELINE (sessione)

```
aa7c3b1 feat(voce): cervello forte dalla voce — «forte …» parlato e GAS_VOCE_FORTE (V1, chat M2)
f2e68c7 chore(revisore): memoria review #564 — APPROVATO CON RISERVE
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione. Il suo hash è nel `git log` del branch dopo il push.

## §4 VERDETTO DEL REVISORE (per commit motore)

Commit aa7c3b1 — review #564-M2, verdetto integrale:

VERDETTO: APPROVATO CON RISERVE

Review #564-M2 sul diff staged di feat/voce-v1-m2 (4 file, +182/-9). Prima della review ho letto CLAUDE.md (sez. 5, 8, 9 e la regola dei modelli in sez. 2), le voci M2 e R-384-1 di reports/stato_progetto.md e la mia memoria.

**Elementi del diff esaminati**
- `modules/voice/server.py:71` — regex `_PAROLA_FORTE`, ancorata all'inizio, con «gas»/«gus» opzionale seguito da `\b`, e «forte» come parola intera (il controllo `(?!\w)` vieta lettere subito dopo). Rischio esaminato: falsi positivi e negativi. Prove fatte su una copia dell'index:
  - Restano turni normali: «fortemente…», «Fortezza», «Gasforte», «Ok Gas, forte…», «Gas, Gas forte», «forte_x», «fortè», «Fort/Forti…» (forme storpiate da Whisper: vanno ai gratuiti, stesso limite di «/frote» già dichiarato).
  - Vanno al forte: « Forte, …» con spazio iniziale, «Gas. Forte. …», «Gas-forte x», «...forte x», «Gas forte» con spazio non separabile (NBSP).
  - Mutante senza `(?!\w)` → 8 test falliti.
  - Esito: ok, salvo la riserva R-564-1-M2.
- `modules/voice/server.py:82` — `cervello_voce`. Ordine: prima `prefisso_forte` (invariato), poi la parola «forte» solo se `parlato`; se manca la richiesta → «uso»; `GAS_VOCE_FORTE` vale solo se il cervello è ancora None. Rischio esaminato: un ramo che porti un lavoro «forte» ai gratuiti. Non ce n'è nessuno: «uso» esce sempre con 400 e nessun turno, «forte» passa sempre `cervello="forte"` al kernel, e l'interruttore non trasforma mai «uso» in un turno. `_voce_tutta_forte` usa gli stessi valori di `_env_flag` in gas.py:573. Esito: ok.
- `modules/voice/server.py:185` — il gestore chiama `cervello_voce(prompt, parlato=is_audio)`: la parola parlata vale solo per l'audio; il testo JSON richiede ancora «/forte», coperto da `test_v1_parola_forte_solo_nel_parlato`. Esito: ok.
- `tests/test_unit_voice_server.py:29` e `tests/test_unit_voice_stt.py:68` — client urllib senza proxy (opener con `ProxyHandler({})`). Rischio esaminato: la chiusura di R-384-1 (chat Voce) è reale? Sì. Con il vecchio test stt, `http_proxy` impostato e `no_proxy` vuoto → 11 test falliti. Con il diff: 104 passed sia senza proxy sia con `http_proxy=http://127.0.0.1:9` e `no_proxy` vuoto. Esito: ok.
- `tests/test_unit_voice_server.py:476` — test con forte fermo: il kernel finto emette un errore, il server risponde 500 con il messaggio dichiarato e c'è una sola chiamata, con `cervello="forte"`. Esito: ok.
- Contesto, non nel diff: `gas.py:4703` — con `cervello == "forte"` il compito è forzato a «forte». È l'invariante R2 esistente; gas.py e brains/ non sono toccati, come deciso da M1.

**Riserve**
- **R-564-1-M2 BASSA**: in italiano «Forte!» a inizio frase è anche un'interiezione («che bello!»).
  - «Forte! Che bello.» → turno al forte con richiesta «Che bello.».
  - «Forte e chiaro, ti sento» → al forte.
  - «Forte.» da solo → 400 con l'istruzione d'uso.

  La direzione è sicura (mai ai gratuiti, rispetta la regola dei modelli), ma consuma il budget del forte e dà una risposta d'uso inattesa. Il limite non è dichiarato né nella docstring né in reports/roadmap.md, che cita solo «Ok Gas, forte…». Da dichiarare, oppure da gestire in seguito.

**Rischi esplicitamente esclusi**
- Trascrizioni reali di Whisper non verificate: nessun audio vero né chiave Groq in dev; ho usato solo stringhe simulate al posto di `transcribe_audio`.
- Il comportamento del kernel con il forte fermo (tetto, CLI assente) non è stato riverificato: è codice di gas.py fuori dal diff, coperto dalle sue review.
- La correttezza della riga della roadmap sulla PR #229 non è stata verificata su GitHub; si appoggia alla review #384 (chat Voce) in memoria.

**Test**: `python -m pytest tests/test_unit_voice_server.py tests/test_unit_voice_stt.py tests/test_unit_voice_tts.py -q` → 104 passed, sia senza proxy sia con un proxy finto nell'ambiente.

**Memoria**: riga contatore #564-M2 aggiunta in coda a /home/user/Gas/.claude/agents/memoria_revisore.md, con la lezione: per una parola chiave parlata, provare anche gli usi comuni della parola come interiezione, non solo i composti. Già committata con lo script di memoria (commit f2e68c7, solo quel file); l'index staged del diff è rimasto invariato (4 file). Nota: il messaggio di commit generato dallo script dice «#564» senza il suffisso -M2.

## §5 DELTA TEST DEL MOTORE

gas.py non toccato. Voice suite (pytest, servizi finti): 73 → 104 test (+31, tutti V1), `104 passed in 21.06s`, sia senza proxy sia con `http_proxy=http://127.0.0.1:9` e `no_proxy` vuoto. Prima del diff, con quel proxy: `26 failed, 47 passed` (R-384-1). Nessun FAIL.

## §6 STATO CI

`gh` non autenticato nel cloud (CI NON VERIFICATA con gh).
- f2e68c7: nessuna run su questo SHA (pushato insieme ad aa7c3b1).
- aa7c3b1: pushato prima dell'apertura della PR #304; run non ancora disponibile alla scrittura dell'handoff.
- Commit di fine-task che contiene questo file: run non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- **R-564-1-M2** BASSA — «Forte!» esclamazione a inizio frase va al forte (direzione sicura, consuma budget): dichiarata in `reports/roadmap.md` (R8) e in stato_progetto; non gestita nel codice.
- **R-384-2 (chat Voce)** COSMETICA — commento in `ci.yml` «sempre servizi finti»: fuori da questa fetta, resta aperta.
- Prova dal vero col microfono sul Mac non fatta (nessun audio nel cloud).
