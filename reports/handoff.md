# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-10-13 — Chiusura dei problemi aperti post #193 (lista #197): A1, A2, B1, C1/C2/C5b, D1, E1

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #198 (https://github.com/Gasss23/Gas/pull/198). Tocca la macchina del bot (`scripts/bot_esito.py`): decide l'operatore. Nessuna fetta ha un APPROVATO secco su tutti i giri: niente merge autonomo.
2. D1 (`modules/gate/gate.py`) è una fetta di sicurezza: secondo passaggio nella chat claude.ai col link della PR #198.
3. E3: sostituire il token `gh` che amministra il repo (`reports/setup_agente_non_admin.md`).
4. E4: confermare che i quattro commit «di autore ignoto» di #193 vengono dalla sessione cloud dell'operatore (trailer `session_01FgYcG4uNEqggobeJsbmE93`, lo stesso di questa sessione).
5. C3: decidere se fare la fetta «lunghezza del record di log capata a monte».
6. C4: decidere se derivare la cartella del log da `handler.baseFilename`.

PR: numero e URL presi dall'output di `mcp__github__create_pull_request` (`{"id":"4849585851","url":"https://github.com/Gasss23/Gas/pull/198"}`); `gh` in questo ambiente non è autenticato (`The token in GH_TOKEN is invalid`).

---

## §1 SCOPE & ESITO FETTE

- **A1 — promemoria_end.sh cieco al worktree**: `FATTA` — repo dal `cwd` del payload, contatore per `session_id` nel git-dir del worktree. Non provato col payload reale di una sessione in worktree.
- **A2 — R-gate-matcher-1, il gate blocca comandi che non committano**: `FATTA` — `gate_matcher.py`, fail-closed; quattro BOCCIATO prima dell'approvazione.
- **B1 — falsi rossi di verifica-bot**: `FATTA` — merge su decisione dell'operatore.
- **C1 — R-297-3 + V-4**: `FATTA` — solo il testo (decisione operatore: il salto dei log resta).
- **C2 — R-301-3 `letti`**: `FATTA` — più R-326-1.
- **C3 — V-2 `_LOG_SFORO_MAX`**: `DEFERITA — fetta a sé (cambia la scrittura del log)`.
- **C4 — V-5 cwd == root**: `DEFERITA — decisione dell'operatore`.
- **C5a/C5c**: `SALTATA — il revisore sconsigliava di toccarle`. **C5b**: `FATTA`.
- **D1 — nove buchi della denylist credenziali**: `FATTA` — fetta di sicurezza.
- **E1 — AGENTS.md**: `FATTA`. **E2**: `CHIUSA senza modifiche (decisione operatore)`. **E3**: `DEFERITA — azione dell'operatore`. **E4**: `DEFERITA — conferma dell'operatore`.
- **Igiene stato_progetto.md**: `FATTA` — lista spostata in `reports/stato_storico.md`.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |  24 ++++++++++++++++++++++++
 .claude/hooks/gate_matcher.py      | 203 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 .claude/hooks/promemoria_end.sh    |  78 +++++++++++++++++++++++++++++++++++++++++++++++++++++-------------------------
 .claude/hooks/review_gate.sh       |   6 ++++++
 .gitignore                         |   3 +++
 gas.py                             |  31 +++++++++++++++++++++++++++----
 modules/gate/gate.py               |  20 ++++++++++++++++----
 reports/diff_sessione.md           |  37 ++++++++++++++++++-------------------
 reports/handoff.md                 | 289 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++-------------------------------------------------------------
 reports/stato_progetto.md          | 189 +++++++++++++++++++++++++++++++--------------------------------------------------------------------------------------------------------------------------------------------------------------
 reports/stato_storico.md           | 159 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 reports/ultimo_report.md           | 100 +++++++++++++++++++++++++++++++++++++++++++++++-----------------------------------------------------
 scripts/bot_esito.py               |  23 ++++++++++++++++++++---
 tests/test_unit_gate.py            |  17 +++++++++++++++--
 tests/test_unit_hooks.py           | 254 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++---
 tests/test_unit_kernel.py          |  26 +++++++++++++++++++++++++-
 tests/test_unit_verifica_bot.py    |  65 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 17 files changed, 1191 insertions(+), 333 deletions(-)
```

## §3 GIT LOG --ONELINE (sessione)

```
b99cd25 fix(cerca_testo): conteggio dei file letti e consiglio onesto sui file grandi (C1, C2, C5)
3b40597 chore(revisore): memoria review #327 — APPROVATO CON RISERVE
70d79a0 chore(revisore): memoria review #326 — APPROVATO CON RISERVE
d47b048 fix(gate): chiusi i nove buchi della denylist credenziali (D1)
97c5d00 chore(revisore): memoria review #325 — APPROVATO CON RISERVE
156c1bc chore(revisore): memoria review #324 — APPROVATO CON RISERVE
5db02c2 chore: AGENTS.md in .gitignore (E1, decisione operatore 2026-10-13)
bb03a76 fix(hooks): il gate di review riconosce il comando, non la prosa (A2)
e906af3 chore(revisore): memoria review #323 — APPROVATO CON RISERVE
c3c0aa2 chore(revisore): memoria review #322 — APPROVATO CON RISERVE
0fd0c7e chore(revisore): memoria review #321 — BOCCIATO
f015022 chore(revisore): memoria review #320 — BOCCIATO
70a6f5a chore(revisore): memoria review #319 — BOCCIATO
2f6bc1e chore(revisore): memoria review #318 — BOCCIATO
85eba60 fix(bot): niente falsi rossi da gravità fuori dai finding (B1)
7de9175 chore(revisore): memoria review #317 — APPROVATO
cdfc12b chore(revisore): memoria review #316 — APPROVATO CON RISERVE
87f5cda fix(hooks): promemoria_end giudica il worktree del turno (A1)
42c5917 chore(revisore): memoria review #315 — APPROVATO CON RISERVE
c65cff2 chore(revisore): memoria review #314 — APPROVATO CON RISERVE
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione.

## §4 VERDETTO DEL REVISORE (per commit motore)

Si incollano integralmente i verdetti che hanno autorizzato ciascun commit motore (l'ultimo giro di ogni fetta). Giri precedenti, superati: #314 APPROVATO CON RISERVE (A1, R-314-1 chiusa nel #315); #316 APPROVATO CON RISERVE (B1, R-316-1 MEDIA chiusa nel #317); #318, #319, #320, #321 BOCCIATO (A2, un bypass reale ciascuno, chiusi); #324 APPROVATO CON RISERVE (D1, R-324-3 chiusa nel #325); #326 APPROVATO CON RISERVE (C, R-326-1 MEDIA chiusa nel #327). Il testo integrale di tutti i giri è nella memoria del revisore e nella trascrizione della sessione.

### Commit 87f5cda (A1) — review #315

VERDETTO: APPROVATO CON RISERVE

Review n. 315, secondo giro sulla voce A1 (`promemoria_end.sh` cieco al worktree), diff staged sul branch feat/merge-automatico-z1xjx2. Sostituisce la #314. Si può committare: resta solo una riserva cosmetica.

**Cosa ho esaminato nel diff**
- `.claude/hooks/promemoria_end.sh:93` e `.claude/hooks/promemoria_end.sh:111`: le due chiamate awk ora ricevono il session_id via ENVIRON invece di `awk -v`, che interpretava i backslash. Rischio cercato: con un backslash nell'id il conto non saliva mai e il blocco diventava perpetuo. Esito: ok, R-314-1 è chiusa.
  - Ho rifatto la prova della mutazione: rimettendo `awk -v` in entrambi i punti, solo wt-6 diventa rosso.
  - Ho rilanciato la sonda con id `a\\tb`: 3 blocchi, poi il fail-open al quarto, e una sola riga `a\\tb:4` (prima erano 4 blocchi e 4 righe `:1`).
- `tests/test_unit_hooks.py:2966` (wt-6): il test colpisce il difetto, perché è rosso con la forma vecchia e verde con la nuova. Esito: ok.
- `.claude/hooks/promemoria_end.sh:43-45`: con CLAUDE_PROJECT_DIR impostato ma non repo, l'hook esce di nuovo con 0; la cartella dello script si usa solo se CLAUDE_PROJECT_DIR manca. È il comportamento di main. Rischio cercato: falsi blocchi giudicati sul repo reale. Esito: ok, la regressione è chiusa.
  - Mutazione riprodotta: sostituendo `|| exit 0` con `|| PROJECT_DIR=""`, il test `tests/test_unit_hooks.py:1315` (T-prom-7) diventa rosso. Il test preesistente quindi protegge davvero.
- `.claude/hooks/promemoria_end.sh:40`: il `cwd` del payload ha sempre la precedenza. Esito: ok. Se `cwd` è un repo valido e CLAUDE_PROJECT_DIR non lo è, si usa `cwd`, che è il comportamento giusto.
- Riprodotti `bash -n` sull'hook e 149 test passati in tests/test_unit_hooks.py. Dopo le mutazioni il working tree è tornato pulito (nessun diff fuori dallo stage).

**Riserva**
- **R-315-1 (COSMETICA).** L'intestazione dell'hook dice ancora «fallback su CLAUDE_PROJECT_DIR, poi sulla dir dello script». Manca il «solo se CLAUDE_PROJECT_DIR manca» che il codice ora applica alle righe 41-46.

R-314-2 (contatore che cresce, nessun lock) e R-314-3 (id non UUID con `:`): mi avete detto che le tracciate in stato_progetto.md. In questo diff non ho visto quel file, quindi non l'ho verificato.

**Cosa NON ho verificato (rischio escluso)**
- Resta non provato con una sessione Claude Code reale che il payload dello Stop hook contenga `cwd` e che questo segua il worktree. Mi fido della documentazione citata, ma non l'ho riprodotto qui, quindi la chiusura di A1 in esercizio non è dimostrata. Suggerisco una prova manuale alla prima sessione in worktree: l'hook deve giudicare l'handoff del worktree.
- Il caso di due sessioni contemporanee sullo stesso checkout non è testato (è R-314-2).

**Memoria aggiornata.** In `.claude/agents/memoria_revisore.md` ho aggiunto la riga contatore #315 e una lezione: un fallback verso la cartella dello script punta a un repo vivo, e un commit della memoria del revisore fatto a metà review può cambiare l'esito di un test che ci ricade. È committata a parte con lo script (commit 42c5917); il diff staged non è stato toccato.

### Commit 85eba60 (B1) — review #317

VERDETTO: APPROVATO

Review #317: secondo giro su B1 (diff STAGED aggiornato dopo la #316). Le tre riserve della #316 sono chiuse e nessuna sonda riapre un modo per far passare un finding ALTA o MEDIA.

**Elementi del diff esaminati**
- scripts/bot_esito.py:168 — `_CODA_NON_FINDING` ora richiede un'intestazione con i due punti, senza trattino davanti. Rischio esaminato: una riga dentro FINDING che inizia con «- NON VERIFICATO il test Y» tagliava il resto della sezione. Esito: ok, la sonda #1 torna {ALTA}.
- scripts/bot_esito.py:178 — se dopo la coda ricompare `^\W*FINDING`, non si taglia niente. Rischio esaminato: un secondo blocco FINDING finiva esente. Esito: ok, la sonda #2 torna {ALTA}. Nel dubbio blocca: basta la parola FINDING, anche senza i due punti.
- scripts/bot_esito.py:105 — in `_FINDING_GRAVE_A_PAROLE` l'id ora accetta `[VFRG]-(?:[A-Za-z0-9]+-)*\d+`. Rischio esaminato: con un id alfabetico, una gravità scritta a parole minuscole passava. Esito: ok, la sonda #3 dà {MEDIA} come l'id numerico. La regola si allarga solo verso il blocco.
- scripts/bot_esito.py:160 — `_RISERVA_REGISTRATA` esclude con `(?![VFGvfg]-)` un primo segmento V/F/G. Rischio esaminato: un finding nuovo scritto come «R-V-1 (ALTA)» veniva esentato. Esito: ok, la sonda #4 dà {ALTA, MEDIA}, perché `_FINDING_GRAVITA` vede «V-1 (ALTA)».
- tests/test_unit_verifica_bot.py:514-521 — i 4 casi bloccanti nuovi sono le sonde #1-#4. Nella versione #316 le avevo misurate a {BASSA}, {}, {}, {}: questi test lì sono rossi, quindi verificano davvero i fix. I due test dei falsi rossi reali (tests/test_unit_verifica_bot.py:465 per #196 e tests/test_unit_verifica_bot.py:490 per #193) restano verdi. Ho rilanciato la suite: 311 passed.

**Sonde avversarie rilanciate** (10, sulla versione nuova)
- Le 4 che passavano ora bloccano.
- Il taglio voluto resta: `**RACCOMANDAZIONE**:` e prosa dopo «NON VERIFICATO:» con una parola maiuscola nuda.
- Le forme da finding nella coda restano bloccanti («V-2 — ALTA —», «V-2 (ALTA)»).

**Finding**
1. COSMETICA: un'intestazione senza due punti («RACCOMANDAZIONE —», «NON VERIFICATO» da sola su una riga) non taglia più. Una parola nuda in quella prosa può tornare a dare un falso rosso. È il verso sicuro voluto dall'operatore; non serve un intervento.
2. Preesistente, non nato qui: l'id della riserva non viene confrontato col repo (R-161-1). Lo tracciate voi in stato_progetto.md.

**Rischio escluso**: non ho rieseguito il workflow `verifica-bot` su GitHub né i verdetti integrali delle PR #193 e #196. Ho lavorato sugli estratti nei test e su sonde sintetiche. Quanto spesso il campo strutturato e il testo divergano davvero non è misurato.

Memoria aggiornata: riga #317 in .claude/agents/memoria_revisore.md, committata da sola (commit 7de9175). Il diff staged non è stato toccato.

Il diff tocca la macchina del bot: il merge lo decide l'operatore.

### Commit bb03a76 (A2) — review #322

VERDETTO: APPROVATO CON RISERVE

Review #322, quinto giro su A2. Ho riletto `git diff --cached`: 3 file, +343 righe. Ho rilanciato tutte le sonde dei giri 1-5 (sonde.py … sonde5.py): 24 forme, 10 delle quali creano un commit reale in un repo usa e getta. L'helper esce 0 su tutte, quindi il gate le blocca. Ho rieseguito i test Match: 63 passed. La suite completa non l'ho rilanciata (tu riporti 211 passed).

**In sintesi:** con il taglio radicale non ho trovato altri modi per far eseguire, nello stesso comando, il testo «git … commit» che l'helper toglie. Restano due riserve basse, nessuna bloccante.

**Elementi del diff esaminati**
- `.claude/hooks/gate_matcher.py:46` — INERTI ridotti a 13 comandi (echo, cat, grep, egrep, fgrep, head, tail, wc, ls, cd, pwd, true, false). Rischio: un comando che esegue o rivaluta i propri argomenti o lo stdin. Esito: ok. Nessuno di questi esegue codice; senza `>` sulla stessa riga di git, il testo tolto può solo finire su stdout o in una pipe verso un altro comando inerte o un git di sola lettura, e nessuno dei due lo esegue.
- `.claude/hooks/gate_matcher.py:112` — backslash, `* ? [ ] { } ~` fuori dagli apici danno `_Ignoto`. Rischio: rivalutazione dopo la quote removal (R-321-1). Esito: ok, `test -v` e `[ -v` ora escono 0.
- `.claude/hooks/gate_matcher.py:116` — `$` e `#` fuori dagli apici singoli danno `_Ignoto`. Esito: ok.
- `.claude/hooks/gate_matcher.py:28` — docstring non raw che contiene `\$`. Esito: **riserva** (R-322-1).
- `.claude/hooks/review_gate.sh:136` — solo exit 3 apre; python assente o in errore porta al blocco. Esito: ok.
- `tests/test_unit_hooks.py:3005` — elenco COMMIT, che ora copre tutte le sonde dei giri 1-5. Esito: ok.

**Finding**
1. **R-322-1 (BASSA) — `\$` nel docstring.** Oggi produce un SyntaxWarning (lo si vede nei test e nelle sonde). In un Python futuro diventerà SyntaxError: l'helper fallirebbe e il gate tornerebbe al blocco per tutti, con i vecchi falsi positivi. È nel verso sicuro, ma va corretto ora: docstring `r"""…"""` oppure `\\$`.
2. **R-322-2 (BASSA, preesistente, da tracciare insieme a R-gjq-1/R-137-2) — GIT_LETTURA non è davvero di sola lettura.** `git log`/`git diff` con `--output=` scrivono file; `git grep -O` esegue un programma. Non è una regressione: gli argomenti di git non vengono mai tolti, quindi questi comandi si comportano come su main. Stessa classe preesistente: scrivere in .git/config col testo letterale (ora passa) e poi fare un `git status` separato. Il commit avviene in un comando separato, che anche main lascia passare.

**Rischi esclusi / non verificati**
- Shell diversa da bash (per esempio zsh come shell dell'operatore): ho controllato solo a ragionamento. Le estensioni zsh pericolose (qualificatori di glob, `=(…)`) cadono già nei divieti; non l'ho misurato.
- Alias e funzioni nel profilo della shell: ambiente considerato fidato.
- Versioni di bash diverse dalla 5.2.21: non verificato.
- Varianti con l'esca (testo «git … commit» accanto a un commit che non contiene quel testo letterale): passano anche su main togliendo l'esca, quindi le considero preesistenti.

**Memoria:** riga #322 e una lezione aggiunte in .claude/agents/memoria_revisore.md, salvate con lo script (c3c0aa2). Il tuo stage è intatto (3 file). Le riserve R-322-1 e R-322-2 vanno tracciate in reports/stato_progetto.md.

### Commit bb03a76 (A2) — review #323 (conferma dopo il fix di R-322-1)

VERDETTO: APPROVATO CON RISERVE

Review #323: confermo il verdetto della #322 sul diff staged attuale (3 file, +343 righe).

**Elementi del diff esaminati**
- `.claude/hooks/gate_matcher.py:1` — la docstring ora è `r"""`. Rischio: SyntaxWarning oggi, SyntaxError in un Python futuro (R-322-1). Esito: ok, chiusa. Con `python3 -W error`, `ast.parse` passa pulito; l'unico ResourceWarning visto veniva dal mio comando di prova, non dal file.
- `.claude/hooks/gate_matcher.py:112` e `.claude/hooks/gate_matcher.py:116` — divieti su backslash, glob, `$` e `#`, invariati rispetto alla #322. Rischio: una regressione introdotta insieme alla modifica della riga 1. Esito: ok. Ho rilanciato le sonde dei giri 1-5: nessun exit 3 e nessun warning.
- `.claude/hooks/review_gate.sh:136` — invariato, fail-closed. Esito: ok.

**Riserve**
- R-322-2 (BASSA, preesistente): GIT_LETTURA non è davvero di sola lettura (`--output=`, `git grep -O`). Non è una regressione: gli argomenti di git non vengono mai tolti. Va tracciata in reports/stato_progetto.md, come hai indicato.

**Rischi esclusi / non verificati**
- La suite completa non l'ho rilanciata a questo giro; mi baso sui tuoi 63 passed Match.
- Shell diversa da bash (per esempio zsh): non misurato.

**Memoria:** riga #323 aggiunta in .claude/agents/memoria_revisore.md, salvata con lo script (e906af3). Il tuo stage è intatto (3 file).

### Commit d47b048 (D1) — review #325

VERDETTO: APPROVATO CON RISERVE

Review #325: nuovo giro sul diff STAGED aggiornato dopo la #324, fetta di sicurezza D1. Restano due riserve BASSE già tracciate (finding 1 e 2); niente blocca il commit.

**Elementi del diff esaminati**
- `modules/gate/gate.py:312` — un pezzo di percorso più lungo di 255 caratteri viene negato prima della regex (R-324-3).
  - Rischio: costo quadratico, e falsi positivi su nomi reali.
  - Esito: ok, misurato. `'token_'*100000+'x'` (600.001 caratteri) impiega 0,005 s. Un percorso con 30.000 cartelle impiega 0,018 s.
  - Il confine è giusto: `'A'*255` resta leggibile, `'A'*256` diventa negato e MAI scrivibile, `dati/` + 200 «é» resta leggibile.
  - Un nome reale ha al massimo 255 byte, quindi al massimo 255 caratteri: nessun file reale viene negato per lunghezza.
  - Lo stesso controllo vale per lettura, scrittura e classificazione, perché tutte passano da `_nome_da_segreto`.
- `modules/gate/gate.py:287` — il ramo token accetta anche le estensioni `pickle|bin|db`.
  - Rischio: buchi residui e falsi positivi.
  - Esito: ok con riserva (finding 2).
  - Negati: token.pickle, token.pickle.bak, msal_token_cache.bin, token_cache.db.
  - Restano leggibili: tokenizer.bin, tokenizer.json.
- `modules/gate/gate.py:297` — aggiunta l'estensione `pgp`.
  - Esito: ok. chiave.pgp è negato; dati/pgpdump.md e x.pgpx restano leggibili.
- `tests/test_unit_gate.py:579` — 5 casi DENY in più, compreso `'token_'*50+'x'`.
  - Esito: ok. Rilanciato: 370 passed.
- `modules/gate/gate.py:293` — invariata rispetto alla #324 (.dockercfg, .vault-token).
  - Esito: ok.

**Controllo `git ls-files` contro `lettura_consentita` (rifatto sul diff attuale)**
- 98 file tracciati: 15 negati con la regex di HEAD e 15 con quella nuova, tutti per i prefissi del livello 3.
- Nessun file cambia esito (0 negati in più, 0 sbloccati).
- Ho passato la regex su tutto il working tree: nessun file corrisponde.

**Finding**
1. **R-324-1 BASSA, aperta in parte** — varianti ancora leggibili: kube_config, kube-config.yaml, mykubeconfig, .vault_token, docker_config.json, wallet_backup.dat, token.cache.json, tokencache.json, access_token (senza estensione). Sono tracciate come riserva per nome.
2. **R-324-2 BASSA, aperta** — blocco in eccesso, nella linea già accettata con R-289-2. Oltre a token_usage.json, max_tokens_config.yaml e tokens_report.txt, ora sono negati e MAI scrivibili anche tokens.bin e token_counts.db. Oggi non tocca nessun file né scrittore del progetto.
3. **R-324-3** — chiusa.

**Rischi esclusi**
- Non ho rilanciato il pytest completo, solo `tests/test_unit_gate.py`.
- Non ho verificato i nomi passati dentro `run_command` (sandbox bwrap): sono fuori perimetro, perché il gate per nomi copre i percorsi passati ai tool, non il testo dei comandi.
- Non ho verificato su VPS né su Windows/WSL.

**Memoria e attenzione al gate**
- Riga #325 aggiunta (nessuna lezione nuova) e committata da sola nel commit `97c5d00`.
- Al primo tentativo l'hook `review_gate.sh` ha bloccato l'intero comando: il marcatore `.claude/.review_ok` non corrisponde più al diff staged cambiato. Il secondo tentativo, con solo lo script di commit, è passato.
- Tu devi rigenerare il marcatore con `bash scripts/segna_review_ok.sh` prima di committare il diff del motore.

- verdetto precedente: #324 APPROVATO CON RISERVE sul diff iniziale, superato da questo.

### Commit b99cd25 (C1/C2/C5b) — review #327

VERDETTO: APPROVATO CON RISERVE

Le due riserve della #326 sono chiuse. Resta una sola riserva: non ho potuto rieseguire la suite del kernel perché il disco della macchina è pieno («No space left on device»).

Elementi del diff esaminati:
1. `gas.py:2243` e `gas.py:2260` — `trovati_prima = len(trovati)`. Nel ramo `_NonTesto`/`_NonRegolare` il file conta fra i letti se ha già aggiunto righe ai risultati. Rischi esaminati:
   - file con righe valide e poi un byte NUL: rilanciata la mia riproduzione della #326 sul diff nuovo. Su cartella (x.txt più vuoto.txt) esce «2 righe trovate in 2 file; 1 file non di testo saltati»; cercato per nome esce «2 righe trovate in 1 file; 1 file non di testo saltati». Prima il conto per nome era «in 0 file». Esito ok, R-326-1 chiusa.
   - file binario senza nessun risultato: conta solo fra i saltati, come voleva C2. Esito ok.
   - lo stesso file contato sia fra i letti sia fra i saltati: avviene solo quando ha prodotto risultati. È documentato nel commento e nel test. Esito ok.
2. `gas.py:2290` (`gas.py:2284-2295`) — testo su cartella «(solo se non supera N byte)» con N uguale a LETTURA_MAX_BYTES. Rischio esaminato: il suggerimento deve essere vero. Per nome `tetto_file = budget_tot`, quindi un file elencato (sopra LETTURA_MAX_BYTES_PER_FILE) si può cercare per intero se non supera LETTURA_MAX_BYTES, e si salta se lo supera. La frase lo dice correttamente. Esito ok, R-326-2 chiusa.
3. `gas.py:2254` e `gas.py:2269` — logica C2 non cambiata dalla #326 (letti dopo il ciclo; in `_TettoByte` solo se il budget è stato consumato). Esito ok.
4. Test T84n R-326-1 aggiunto in tests/test_unit_kernel.py, appena dopo i due casi C2 (vicino a `tests/test_unit_kernel.py:8302`): usa la mia stessa riproduzione e controlla l'intestazione esatta. Esito ok.

Riserva:
- **R-327-1 BASSA (di processo)**: non ho rieseguito la suite del kernel. `python tests/test_unit_kernel.py` si ferma su `git init` in /tmp perché il disco è pieno: `df` dice 100%, circa 324 KB liberi. Il risultato «846 PASS, 0 FAIL» resta una tua affermazione non verificata da me. Prima di committare va liberato spazio e rilanciata la suite. La riproduzione diretta di `_cerca_testo` invece è riuscita, con i risultati qui sopra.

Rischio escluso: non ho verificato con file reali sopra i 5 MB, né su VPS.

Memoria: la riga #327 è scritta in .claude/agents/memoria_revisore.md (riga 559). Non so se `bash scripts/commit_memoria_revisore.sh` abbia committato: l'output è andato perso per il disco pieno, e lo script è fail-safe. Controlla con `git log -1 -- .claude/agents/memoria_revisore.md`. Se manca, rilancia lo script dopo aver liberato spazio.

Attenzione: con il disco pieno anche commit, push e marcatore di review rischiano di fallire. Libera spazio prima di continuare.

(Nota dell'agente, fuori dal verdetto: disco liberato, suite kernel rilanciata → 846 PASS, 0 FAIL; memoria #327 committata con lo script in 3b40597.)

## §5 DELTA TEST DEL MOTORE

- Kernel (`python tests/test_unit_kernel.py`), base `04635d5` misurata in sessione: **843 PASS, 0 FAIL** → dopo la sessione: **846 PASS, 0 FAIL** (+3: due casi C2, uno R-326-1; C1 aggiunge asserzioni a casi esistenti). Con il gas.py di HEAD~1 e i test nuovi: 841 PASS, 4 FAIL (i test colpiscono il difetto).

```
=== RIEPILOGO: 846 PASS, 0 FAIL ===
```

- pytest completo dopo D1: `1171 passed in 163.71s` (base misurata a inizio sessione: `1068 passed`).
- Suite toccate: `tests/test_unit_hooks.py` 211 passed; `tests/test_unit_verifica_bot.py` 311 passed; `tests/test_unit_gate.py` 370 passed.
- Nessun FAIL fuori scope.

## §6 STATO CI

`gh` non autenticato in questo ambiente; dati letti con il connettore GitHub (`actions_list`, workflow `ci.yml`, branch `feat/merge-automatico-z1xjx2`):

| Run | SHA testato | unit-suite | handoff-check |
|---|---|---|---|
| 38462877047 | 87f5cda (A1) | success | failure (handoff non ancora rigenerato) |
| 38463527121 | 85eba60 (B1) | success | failure (idem) |
| 38467113383 | bb03a76 (A2) | success | failure (idem) |
| 38467958846 | d47b048 (D1) | success | failure (idem) |
| 38469244358 | b99cd25 (C) | success | failure (idem) |

Mappatura commit→run: ogni commit di codice è stato pushato da solo, quindi ha la propria run (tabella sopra). Commit della memoria del revisore senza run propria (pushati insieme al commit successivo, testati solo come parte dell'albero di testa): c65cff2, 42c5917 (in 87f5cda); cdfc12b, 7de9175 (in 85eba60); 2f6bc1e, 70a6f5a, f015022, 0fd0c7e, c3c0aa2, e906af3 (in bb03a76); 5db02c2, 156c1bc, 97c5d00 (in d47b048); 70d79a0, 3b40597 (in b99cd25). Il commit di fine-task che contiene questo file: run non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- R-314-2 (BASSA): contatore di `promemoria_end.sh` senza pulizia delle righe vecchie e senza lock.
- R-314-3 (COSMETICA): `session_id` non UUID con `:`.
- R-315-1 (COSMETICA): intestazione di `promemoria_end.sh` non aggiornata sul fallback.
- R-317-1 (COSMETICA): intestazione senza due punti non taglia la coda in `bot_esito.py` (falso rosso residuo, verso sicuro).
- R-161-1 esteso (BASSA, preesistente): id della riserva non confrontato col repo.
- R-322-2 (BASSA, preesistente): GIT_LETTURA non di sola lettura in senso stretto.
- R-gate-matcher-2 (BASSA, preesistente): `"git" commit` sfugge già al grep grezzo su main.
- R-324-1 (BASSA, parziale): varianti per nome ancora leggibili.
- R-324-2 (BASSA): blocco in eccesso su nomi plausibili.
- A1 non provata col payload reale di una sessione in worktree.
- C3, C4 deferite (§0).
