# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-10-20 — Voce, fetta 1: test di trascrizione e sintesi in CI (chat Voce)

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #229 (https://github.com/Gasss23/Gas/pull/229): tocca `.github/workflows/ci.yml` (macchina del bot) → `verifica-bot` neutral, il merge lo decide l'operatore. Deciso dall'operatore in chat il 2026-10-20 («ok merge 229»): merge automatico attivato dopo il merge di main nel ramo (`5b90d69`, review #388).
2. Etichetta `verifica` sulla PR #229: presente.

(`gh` non autenticato nella sessione cloud: numero/URL della PR presi dall'esito reale di `create_pull_request` via MCP GitHub.)

---

## §1 SCOPE & ESITO FETTE

- **Fetta 1 — test stt/tts nei test automatici**: `FATTA` — `ci.yml` lancia anche `test_unit_voice_stt.py` e `test_unit_voice_tts.py` (52 test, servizi finti). Modifica a `ci.yml` autorizzata dall'operatore in sessione.
- **Fetta 2 — token a scadenza e limite richieste**: `DEFERITA` — dopo il merge della fetta 1.
- **Fetta 3 — timer due secondi e frase di attesa**: `DEFERITA` — dopo la fetta 2.
- **Fetta 4 — revisione del client nel browser**: `DEFERITA` — dopo la fetta 3.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   2 ++
 .github/workflows/ci.yml           |   6 ++++--
 reports/diff_sessione.md           |  18 +++++++++---------
 reports/handoff.md                 | 188 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++---------------------------------------------------------------------------------
 reports/stato_progetto.md          |   4 +++-
 reports/ultimo_report.md           |  34 ++++++++++++++++++++++++++--------
 6 files changed, 151 insertions(+), 101 deletions(-)
```

---

## §3 GIT LOG --ONELINE (sessione)

```
5b90d69 Merge origin/main (#227, #228) in claude/peaceful-lovelace-0w2b7q
1aa2921 docs(fine-task): correzioni della verifica esterna #229 (voice suite 20 → 72)
7515eae docs(fine-task): correzioni V-1/V-2 del bot #229 (voice suite 72 test, frase del report)
c1e2f33 docs(fine-task): report e handoff — voce fetta 1, test stt/tts in CI (chat Voce)
312a0e9 ci(voce): la voice suite lancia anche i test di trascrizione e sintesi (R8)
83dd041 chore(revisore): memoria review #384 — APPROVATO CON RISERVE
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione.

---

## §4 VERDETTO DEL REVISORE (per commit motore)

Review #384 (chat Voce), sul commit `312a0e9` — verdetto integrale:

## VERDETTO: APPROVATO CON RISERVE

Review #384 (chat Voce). Diff staged: solo `.github/workflows/ci.yml`, +4 −2. Prima della review ho letto CLAUDE.md (sez. 5, 8, 10), le voci voce di reports/stato_progetto.md, la memoria del revisore e le regole di lavoro parallelo prese da origin/feat/merge-automatico-z1xjx2.

**Elementi del diff esaminati**
1. `.github/workflows/ci.yml:111` — la voice suite ora gira in un solo `python -m pytest` su server + stt + tts. Ho controllato tre rischi:
   - rete reale e chiavi;
   - interferenze tra i file nello stesso processo;
   - flakiness.

   Esito: **ok**. Ho bloccato la rete con un sitecustomize (connect e DNS verso host non locali sollevano errore) e ottenuto 72 passed in 3 ordini diversi (server/stt/tts, tts/stt/server, stt/server/tts). Ho rifatto la prova sia senza GROQ_API_KEY/ELEVENLABS_API_KEY sia con chiavi finte presenti, e ho lanciato stt+tts 3 volte di fila: sempre 52/52.
   - Nessun test modifica `os.environ` a livello globale: si usano solo `patch.dict` e `monkeypatch`.
   - Ogni test ha un server proprio su porta 0 (`tests/test_unit_voice_stt.py:53`, `tests/test_unit_voice_tts.py:52`) con shutdown nel teardown.
   - Ogni server usa una sottoclasse `_H` locale, quindi `kernel` e `token` non si sporcano tra un file e l'altro.
   - I tempi di 0,5 s nel teardown sono l'intervallo di attesa di `serve_forever`, non timeout.
   - Dopo le esecuzioni il working tree è pulito.
2. `.github/workflows/ci.yml:190` (contesto, non toccato) — il riepilogo «Voice suite» legge `voice_output.txt`. Rischio: che con tre file la riga si rompa. Esito: **ok**. Ho simulato il flusso (tee + grep + sed) sull'output combinato: viene fuori «72 passed in 17.39s», con 52 righe stt/tts nel `-v`. La lista FAILED (`.github/workflows/ci.yml:238`) e il codice di uscita con pipefail (rc=0) funzionano. Una sola chiamata a pytest produce una sola riga di riepilogo.
3. `.github/workflows/ci.yml:105` — cambia il nome dello step. Rischio: qualcosa che lo cerca per nome. Esito: **ok**. Il grep su scripts/, tests/, .github/, .claude/ non trova riferimenti al vecchio nome. Il check obbligatorio del ruleset è il job `unit-suite`, non lo step. Il riepilogo usa il nome del file, non quello dello step.
4. `.github/workflows/ci.yml:106` — il commento dice «sempre servizi finti iniettati». Esito: **riserva cosmetica (R-384-2)**: è impreciso. I test 503/400 senza patch (per esempio quelli di `tests/test_unit_voice_tts.py:181` e `tests/test_unit_voice_stt.py:312`) non iniettano nulla. Reggono perché il server esce prima della chiamata (`modules/voice/server.py:177`, `modules/voice/server.py:204`, `modules/voice/server.py:208`). Se quell'ordine cambiasse, in CI partirebbe una chiamata vera con chiave finta e il test fallirebbe (nessun segreto esposto). Oggi la rete non viene mai raggiunta.

**Riserve**
- **R-384-1 BASSA** — `tests/test_unit_voice_stt.py:67` usa `urllib.request.urlopen` verso 127.0.0.1, come già faceva `tests/test_unit_voice_server.py:71`. urllib segue `http_proxy` anche per il localhost. Prova: con `http_proxy` finto e senza `no_proxy` ottengo 24 FAIL su stt+server. Sui runner GitHub non c'è proxy, quindi la CI non è toccata. Il difetto c'era già; questa modifica porta in CI altri test dello stesso tipo. Rimedio (area Voce): `urllib.request.build_opener(urllib.request.ProxyHandler({}))` oppure `http.client` diretto, come già fa tts.
- **R-384-2 COSMETICA** — il commento di `.github/workflows/ci.yml:106`, vedi punto 4.

**Note (non riserve)**
- `ci.yml` rientra nella macchina del bot (`bot_esito.tocca_macchina_bot` dà True): `verifica-bot` riporterà neutral e il merge lo decide l'operatore.
- Ci sono due dati vecchi fuori dal diff, da sistemare con l'aggiornamento di stato:
  - `reports/stato_progetto.md:268` riporta ancora «Voice suite: 24 PASS»;
  - la docstring di `tests/test_unit_gate.py:7` dice che in CI gira solo voice_server (fuori dall'area Voce).

**Cosa non ho verificato**
- Non ho visto una run CI reale su ubuntu-latest con Python 3.11 (locale ho python3 di sistema), quindi non ho escluso differenze di versione. Le dipendenze di stt/tts sono solo stdlib + pytest, quindi il rischio è basso; la conferma arriverà dalla prima run della PR.
- Non ho misurato la flakiness sotto il carico di un runner condiviso: in locale ho fatto solo 3+3 esecuzioni.

Riga contatore scritta in `/home/user/Gas/.claude/agents/memoria_revisore.md` come «#384 (chat Voce)» e committata (83dd041, solo quel file). Il diff staged di ci.yml è rimasto intatto nell'index.

### Review #388 — merge di origin/main nel ramo della PR #229 (verdetto integrale, incollato)

## VERDETTO: APPROVATO CON RISERVE

Review #388: merge di origin/main (e6e69b5, PR #227/#228) nel ramo `claude/peaceful-lovelace-0w2b7q` (HEAD 1aa2921, PR #229 della chat Voce). Prima della review ho letto CLAUDE.md (sez. 5, 8, 10), `reports/stato_progetto.md` (solo le righe 593 e 599 e il diff contro main), `reports/lavoro_parallelo.md` (regole 3-4) e la mia memoria.

**Cosa ho controllato nel diff**
1. `.github/workflows/ci.yml:105` — lo step della voce della PR (server + stt + tts, nome «Run voice suite»). Rischio esaminato: che la risoluzione del merge abbia perso o alterato la modifica della PR. `git diff --cached origin/main -- .github/workflows/ci.yml` mostra SOLO la modifica della PR (+4 −2). Esito: ok.
2. `.github/workflows/ci.yml:159` — lo step «Ingest delle fonti di studio» arrivato da main (#228). Rischio: che il ci.yml della PR abbia cancellato lo step di main. `git diff --cached 1aa2921` mostra SOLO questo blocco di +7 righe, uguale al delta di main dalla merge-base 9b8526b (cambia solo l'offset dell'hunk). Il ci.yml risultante è quindi quello della PR più lo step ingest di main, e non soltanto quello della PR: è il risultato giusto. YAML valido. Esito: ok.
3. `.claude/agents/memoria_revisore.md:624` — la riga «#384 (chat Voce)» dopo #384–#387 di main. Rischio: una riga persa o alterata. Contro origin/main la differenza è solo +1 riga, identica byte per byte a quella di HEAD. Esito: riserva (vedi R-388-1 e la lezione).
4. `reports/stato_progetto.md:599` — riga «Voce — fetta 1», fusa da sola insieme a «Stato motore» (24 PASS → 72 test). `reports/stato_progetto.md:593` (main) usa lo stesso id R-384-1 con un altro significato. Esito: riserva R-388-1.
5. Perimetro (gas.py, modules/, tests/, scripts/, .claude/, tools/, knowledge/, brains/): `git diff --cached origin/main --stat` riporta solo ci.yml e la riga di memoria. Tutto il resto è identico a main. Esito: ok.
6. `reports/diff_sessione.md`, `reports/handoff.md`, `reports/ultimo_report.md`: nessuna differenza contro HEAD, quindi la parte della PR (--ours) è confermata. Nessun marcatore di conflitto nei 14 file del merge. Il working tree coincide con l'indice. Ho eseguito voce + ingest sull'albero fuso: 77 passed (72 + 5).

**Riserve**
- **R-388-1 BASSA — due significati per #384 e R-384-1.**
  - Su main, la review #384 riguarda la chiusura di R-383-1 e R-384-1 è COSMETICA (taglio del tool_name senza test), in `reports/stato_progetto.md:593`.
  - Nella chat Voce, R-384-1 è BASSA (urllib verso 127.0.0.1 segue `http_proxy`), in `reports/stato_progetto.md:599` e nel §4 dell'handoff della PR.
  - La regola 4 di `reports/lavoro_parallelo.md` qualifica i numeri delle review ma non gli id dei finding.
  - Proposta, senza rinumerare nulla:
    - (a) in stato_progetto riga 593 scrivere «review #384 (chat Motore)» e «R-384-1 (chat Motore)»; in riga 599 scrivere «R-384-1 (chat Voce)» e «R-384-2 (chat Voce)»;
    - (b) estendere la regola 4 di lavoro_parallelo.md: «anche gli id dei finding R-N-k portano il suffisso della chat quando il numero collide»;
    - (c) NON toccare il §4 dell'handoff, che è il verdetto integrale e non si riscrive. Il suffisso nella riga 599 basta a disambiguare il rimando dell'handoff («riga Voce — fetta 1»);
    - (d) le prossime review ripartono da #388 (massimo del file + 1).
- **R-388-2 COSMETICA — citazioni spostate nell'handoff.** Le citazioni `ci.yml:190` e `ci.yml:238` del §4 dell'handoff della PR ora puntano 7 righe sopra il contenuto citato, perché lo step ingest di main sposta il summary (:190 → :197, :238 → :245). Il gate B verifica solo che la riga esista e passa; il testo integrale non va toccato.

**Cosa NON ho verificato (rischio escluso)**
- La suite kernel e la pytest completa sull'albero fuso. Il perimetro è identico a origin/main, già revisionato e verde in CI. L'unico file diverso, ci.yml, l'ho verificato con le suite che lancia (voce + ingest).
- L'esito reale della CI e del check verifica-bot sul commit di merge: non è riproducibile prima del push.
- La resa del job summary in CI: lo step ingest di main non compare nel summary, ma è una scelta di #228 e non riguarda questo merge.

**Memoria**
- Ho scritto la riga contatore #388 in coda a `/home/user/Gas/.claude/agents/memoria_revisore.md`, con questa lezione: con chat parallele il numero si prende dal MASSIMO del file, non dall'ultima riga. Prima della mia riga, l'ultima era «#384 (chat Voce)»: chi incrementava dall'ultima riga avrebbe creato un altro #385.
- La riga è nel working tree e NON è nello staging.
- NON ho eseguito `scripts/commit_memoria_revisore.sh`, per due motivi: lo hai chiesto tu, e durante un merge in corso `git commit -o` fallisce comunque («partial commit during a merge»).
- Cosa devi fare tu: `git add .claude/agents/memoria_revisore.md` PRIMA di `bash scripts/segna_review_ok.sh`, così l'hash del marcatore copre anche questa riga; poi il commit del merge.


---

## §5 DELTA TEST DEL MOTORE

Nessuna modifica a gas.py né ai file di test: cambia solo cosa lancia la CI. Voice suite in CI: 20 → 72 test (20 server + 28 stt + 24 tts). Riepilogo locale reale (rete bloccata, senza chiavi, `test_collection_dell_intero_repo_non_esplode` escluso perché in locale mancava `openai`; poi installato e passato a parte):

```
71 passed, 1 deselected in 17.24s
```

## §6 STATO CI

- `83dd041`: nessuna run su questo SHA (pushato insieme a `312a0e9`).
- `312a0e9`: run CI 39494111201 — unit-suite success; handoff-check failure (atteso: l'handoff di quel commit era ancora quello della sessione precedente).
- `c1e2f33`: run CI 39494258815 — unit-suite success (step «Run voice suite» success), handoff-check success. Bot `gas-verificatore`: APPROVATO CON RISERVE, check verifica-bot neutral (la PR tocca `ci.yml`, macchina del bot).
- `7515eae` (correzioni V-1/V-2 del bot): run non ancora disponibile alla scrittura dell'handoff.
- `1aa2921` (correzioni della verifica esterna #229): run CI 39495199446 — unit-suite success, handoff-check success; verifica-bot neutral (APPROVATO CON RISERVE, nessuna ALTA/MEDIA). Merge rifiutato da GitHub per conflitto con main (#227/#228 mergiate nel frattempo).
- `5b90d69` (merge di origin/main, review #388): run non ancora disponibile alla scrittura dell'handoff.
- Commit di fine-task con questo handoff: run non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- Review #388 (merge di main): R-388-1 BASSA (numero #384 e id R-384-1 usati da due chat; disambiguati in `reports/stato_progetto.md` con «chat Motore»/«chat Voce»; regola 4 di `reports/lavoro_parallelo.md` da estendere agli id dei finding), R-388-2 COSMETICA (citazioni `ci.yml:190`/`:238` del verdetto #384 spostate di 7 righe).
- Le altre riserve aperte del progetto sono in `reports/stato_progetto.md`.

- R-384-1 BASSA, R-384-2 COSMETICA: dettaglio in §4 e in `reports/stato_progetto.md` (riga «Voce — fetta 1»).
- Bot #229: V-1 BASSA («Voice suite: 24 PASS» vecchio in `stato_progetto.md`) e V-2 COSMETICA (frase «72/72» di `ultimo_report.md` non allineata a §5): CHIUSE in questo commit.
- Verifica esterna #229 (commento sulla PR): APPROVATO CON RISERVE. V-1 BASSA («24 → 72» in §5, il reale è 20 → 72) e V-2 BASSA (riga «Stato motore» di `stato_progetto.md`): CHIUSE in questo commit. V-3 COSMETICA (conteggi del §2 presi prima del commit di fine-task): limite noto del flusso, come R-bot221-2. V-4 COSMETICA (docstring di `tests/test_unit_gate.py`, fuori area Voce): richiesta alla chat Motore in `ultimo_report.md`.
