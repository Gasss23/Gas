# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-10-20 — Voce, fetta 1: test di trascrizione e sintesi in CI (chat Voce)

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #229 (https://github.com/Gasss23/Gas/pull/229): tocca `.github/workflows/ci.yml` (macchina del bot) → `verifica-bot` neutral, il merge lo decide l'operatore.
2. Etichetta `verifica` sulla PR #229.

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
 .claude/agents/memoria_revisore.md |  1 +
 .github/workflows/ci.yml           |  6 ++++--
 reports/diff_sessione.md           | 12 ++++++++----
 reports/handoff.md                 | 73 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++----------------
 reports/stato_progetto.md          |  2 ++
 reports/ultimo_report.md           | 23 +++++++++++++++--------
 6 files changed, 87 insertions(+), 30 deletions(-)
```

---

## §3 GIT LOG --ONELINE (sessione)

```
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

---

## §5 DELTA TEST DEL MOTORE

Nessuna modifica a gas.py né ai file di test: cambia solo cosa lancia la CI. Voice suite in CI: 24 → 72 test (server + stt + tts). Riepilogo locale reale (rete bloccata, senza chiavi, `test_collection_dell_intero_repo_non_esplode` escluso perché in locale mancava `openai`; poi installato e passato a parte):

```
71 passed, 1 deselected in 17.24s
```

## §6 STATO CI

- `83dd041`: nessuna run su questo SHA (pushato insieme a `312a0e9`; il suo albero è incluso in quello testato da `312a0e9`).
- `312a0e9`: run CI 39494111201 (https://github.com/Gasss23/Gas/actions/runs/39494111201) — in corso alla scrittura dell'handoff; `verifica-bot` 39494131462 skipped (manca l'etichetta `verifica`).
- Commit di fine-task con questo handoff: run non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- R-384-1 BASSA, R-384-2 COSMETICA: dettaglio in §4 e in `reports/stato_progetto.md` (riga «Voce — fetta 1»).
