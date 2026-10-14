# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-10-14 — D2: nomi di credenziali vietati nel cancello (secondo passaggio claude.ai su PR #198)

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #201 (https://github.com/Gasss23/Gas/pull/201).
2. Fetta di sicurezza (cancello): secondo passaggio nella chat claude.ai col link della PR #201. Verifica esterna (agente) e bot: APPROVATO CON RISERVE senza ALTA/MEDIA; il check `verifica-bot` è neutral, quindi il merge lo decide l'operatore.
3. Decidere se aprire la fetta D3 (nomi ancora leggibili, proposta in `reports/ultimo_report.md`).

---

## §1 SCOPE & ESITO FETTE

- **D2 punti 1–6 (ALTA + MEDIA)**: `FATTA` — `_CHIAVE_PRIVATA_RE` nega in lettura e scrittura (livello 3) tutti i nomi del prompt; falsi positivi del prompt leggibili.
- **D2 BASSA facoltativa**: `FATTA` — nessun falso positivo su file reali.
- **Alternativa `[a-z0-9]+_keys?\.(txt|json|ya?ml)`**: `SALTATA` — ridondante col bordo di `keys?\.(…)` (confermato dal revisore).
- **R-329-1 (MEDIA, review #329)**: `FATTA` — separatore `[-_ ]?` anche con lo spazio.
- **Fetta D3 (nomi ancora leggibili)**: `DEFERITA` — fuori scope di D2, proposta nel report per decisione dell'operatore.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   3 +++
 modules/gate/gate.py               |  37 ++++++++++++++++++++++++++++---------
 reports/diff_sessione.md           |  10 +++++-----
 reports/handoff.md                 | 159 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++--------------------------------------
 reports/stato_progetto.md          |   8 +++++++-
 reports/ultimo_report.md           | 123 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++--------
 tests/test_unit_gate.py            |  41 ++++++++++++++++++++++++++++++++++++++---
 7 files changed, 317 insertions(+), 64 deletions(-)
```

## §3 GIT LOG --ONELINE (sessione)

```
bc7c799 docs(fine-task): report e handoff — fetta D2 nomi di credenziali (PR #201)
21cc202 feat(gate): D2 — nomi di credenziali vietati in lettura e scrittura
e67ef2a chore(revisore): memoria review #330 — APPROVATO CON RISERVE
28a4abb chore(revisore): memoria review #329 — APPROVATO CON RISERVE
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione.

## §4 VERDETTO DEL REVISORE (per commit motore)

### Review #329 (primo giro sul diff D2, prima di R-329-1) — verdetto integrale

## VERDETTO: APPROVATO CON RISERVE

Review #329. Diff staged su feat/gate-d2-credenziali: modules/gate/gate.py e tests/test_unit_gate.py. Ho fatto le tre letture obbligatorie: CLAUDE.md §5, stato_progetto.md (letto in modo mirato: D1, R-324-1, R-324-2) e la memoria del revisore.

**Elementi del diff esaminati**
- `modules/gate/gate.py:291` — nuove voci composte api/access/refresh/gh/github/hf/openai/anthropic/gemini/groq + token/key, con bordo `(?<![a-z])…(?![a-z])`. Rischi esaminati: falsi positivi e scappatoie dal bordo. Risultato misurato: high_key, sigh_token, turkey.json, donkeys.txt, hotkeys.json e keyboard restano leggibili. Il separatore però non ammette lo spazio (R-329-1). Esito: **riserva**.
- `modules/gate/gate.py:298` — seed/recovery phrase, keystore.json, seed.txt/mnemonic.txt. Rischio: nomi scritti da persone. Esito: «Seed Phrase.txt» e «recovery phrase.txt» restano **leggibili** (misurato). **Riserva** (R-329-1).
- `modules/gate/gate.py:299` — `passwords?(\.[a-z0-9]+)*~?$`. Rischi: backtracking e falsi positivi. Il gruppo ripetuto parte sempre da un `.` letterale, quindi non è ambiguo e non diventa esponenziale. Resta quadratico rispetto alle posizioni di partenza: 144µs su `"password."*28+"x!"` (254 caratteri). Il tetto dei 255 caratteri lo limita: un percorso da 102k caratteri con 400 pezzi costa 58 ms. passwordless.md e password_reset.md restano leggibili, passwords.txt.bak è negato. Esito: **ok** (la nota sul tempo è R-329-4).
- `modules/gate/gate.py:305` — `^(tokens?|keys?|passwd|shadow)(-|~|\.bak|\.old)?$`. Rischio: che blocchi anche tokens.md e keys.md. Misurato: tokens.md, keys.md e keys_guide.md leggibili; token, TOKENS, «token » e «token.» negati (casefold e rstrip a monte). Esito: **ok**.
- `modules/gate/gate.py:310` — `^\.azure(?![a-z-])`. Rischio: bloccare la CI. .azure-pipelines/ci.yml resta leggibile; .azure, .azure/accessTokens.json e .azure_x sono negati. Esito: **ok**.
- `modules/gate/gate.py:316` — estensioni .p8, .session, .tfstate, .tfvars, .ovpn. Rischio: blocco in eccesso. Ora sono negati anche notes.session.md, x.p8.md e terraform.tfvars.example (R-329-3). Esito: **riserva BASSA**.
- `tests/test_unit_gate.py:617` e `tests/test_unit_gate.py:637` — i test nuovi e i falsi positivi. Ho rimesso la regex di origin/main con un plugin pytest, senza toccare il working tree: **97 test falliscono**, quindi i test nuovi mordono. Con il diff: **477 passed** (riprodotto). Esito: **ok**.
- Contesto: `gas.py:1725` (cerca_testo) e `modules/gate/gate.py:373` (livello_scrittura) usano la stessa `_nome_da_segreto`, quindi lettura, ricerca e scrittura restano coerenti.

**Fatti dichiarati dall'autore, verificati**
- 477 passed: **confermato**.
- Nessun cambio di esito su git ls-files (98 file) e sull'albero di lavoro: **confermato**. Ho contato 340 voci perché includo le cartelle e .agents/.codex. Su HEAD e sul diff i file tracciati negati sono 15 in entrambi i casi.
- «≤ ~35µs»: **falso**. Ho misurato 144µs (vedi R-329-4).
- Scelte dell'autore:
  - Omettere `[a-z0-9]+_keys?\.(...)`: giusto, il bordo copre già prod_key.txt e my_keys.json.
  - Copie `-`, `~`, `.bak`, `.old`: giusto.
  - `.azure` con `(?![a-z-])`: giusto.
  - dati/key.txt spostato a negato: lo chiede il punto 1, giusto.
  - Il pattern passwords: giusto.

**Finding**
1. **R-329-1 (MEDIA, da chiudere in questa fetta)**: il separatore interno `[-_]?` alle righe 291-298 non ammette lo spazio. Restano leggibili «Seed Phrase.txt», «recovery phrase.txt», «ssh key», «deploy key», «access token», «api token», «private key» e «gh token» senza estensione (misurato). Sono proprio i nomi dei punti 5 e 6 del mandato, nella forma in cui li scrive una persona su macOS. Correzione provata: `[-_ ]?` al posto di `[-_]?` nelle sei composte (api, access/refresh, gruppo gh…groq, private, ssh/deploy, seed/recovery). Risultato: 477 passed, tutti i casi sopra negati, keyboard.md, auth_flow.md, session_notes.md, seed_data.csv e «a private keynote.md» ancora leggibili, tracciati negati sempre 15. Va aggiunto un caso di test con lo spazio.
2. **R-329-2 (BASSA)**: nomi ancora leggibili:
   - «Cookies» senza estensione: è il nome reale del database dei cookie di Chrome.
   - storage-state.json e auth-state.json col trattino.
   - api.token, openai.token, gh.token col punto.
   - token.old~ (copia di una copia).
   - kube_config e kube-config.yaml: R-324-1 resta aperto.
   Da accodare a R-324-1.
3. **R-329-3 (BASSA)**: nomi bloccati in eccesso, anche in scrittura (livello 3): api_key_rotation.md, access_token_docs.md, private_key_howto.md, hfkeys.md, terraform.tfvars.example, notes.session.md, x.p8.md, .boto3. Il mandato lo accetta («anche senza estensione»). Da accodare a R-324-2.
4. **R-329-4 (COSMETICA)**: il tempo dichiarato è smentito dalla misura: 144µs, non 35µs. Non è un rischio, grazie al tetto dei 255 caratteri. Va corretto nel report, e chiamare la regex «lineare» è impreciso: è quadratica ma limitata.

Wall of Shame: nessuno slicing della history, nessuna simulazione di tool, il diff non tocca il kernel. Fail-safe §9 intatto: `lettura_consentita` e `livello_scrittura` restano dentro try/except e chiudono a False / 3.

**Cosa non ho verificato**
- Nomi Unicode che dopo NFKC+casefold non tornano ASCII (es. «İ» turco) su un filesystem che non distingue maiuscole e minuscole. È una classe di problemi già presente prima di questo diff, e servirebbe un volume APFS dedicato.
- Comportamento sulla VPS Linux: non riproducibile in dev, ma la regex non dipende dalla piattaforma.

Commit consentito: sì, dopo aver chiuso R-329-1 (correzione già provata) o averla tracciata in stato_progetto.md. R-329-2, R-329-3 e R-329-4 vanno tracciate.

Memoria: riga #329 e una lezione nuova scritte in /Users/gas/Gas/.claude/agents/memoria_revisore.md, committate da sole (28a4abb). Lo staging del diff è rimasto intatto.

File rilevanti: /Users/gas/Gas/modules/gate/gate.py, /Users/gas/Gas/tests/test_unit_gate.py

### Review #330 (commit 21cc202, diff finale con R-329-1 chiusa) — verdetto integrale

## VERDETTO: APPROVATO CON RISERVE

Review #330, secondo giro sulla fetta D2: ho riverificato il diff staged attuale.

R-329-1 è chiusa. Restano solo riserve basse o cosmetiche (R-329-2, R-329-3, R-329-4), che tracci tu in stato_progetto.md. Il commit è consentito.

**Elementi del diff esaminati**
- `modules/gate/gate.py:291` — `[-_ ]?` dopo api e dopo access/refresh. Ho controllato che lo spazio non apra falsi positivi: «api tokenizer.md» resta leggibile, perché `(?![a-z])` si ferma sulla "i". Esito: **ok**.
- `modules/gate/gate.py:294` — `[-_ ]?` dopo private e dopo ssh/deploy. Stesso controllo sui falsi positivi: «a private keynote.md» e «ssh keyring» restano leggibili (misurato). Esito: **ok**.
- `modules/gate/gate.py:298` — seed/recovery con `[-_ ]?`. Rischio controllato: varianti ancora scoperte. Il plurale «seed phrases.md» / «seed_phrases» resta leggibile, perché la "s" finale viene presa come continuazione della parola. Esito: **riserva BASSA**, da aggiungere a R-329-2.
- `tests/test_unit_gate.py:618` — gli 8 casi nuovi con lo spazio. Rischio controllato: che il test non morda. Ho rimesso `[-_]?` al posto di `[-_ ]?` con un plugin pytest, senza toccare il working tree: **8 failed, 478 passed**. Col diff: **486 passed** (riprodotto). Esito: **ok**.
- `tests/test_unit_gate.py:639` — il falso positivo «a private keynote.md» è tra i leggibili. Esito: **ok**.

**Verificato di nuovo**
- 98 file tracciati e 340 voci dell'albero di lavoro: nessun cambio di esito rispetto a origin/main.
- I tempi sono invariati: la modifica aggiunge solo un carattere alla classe del separatore, che resta opzionale.
- Il working tree non ha modifiche fuori dallo stage su gate.py e test_unit_gate.py.

**Riserve aperte (le traccia l'autore)**
- R-329-2 (BASSA): nomi ancora leggibili.
  - «Cookies» di Chrome, senza estensione.
  - storage-state.json e auth-state.json, col trattino.
  - api.token, openai.token, gh.token, col punto.
  - token.old~.
  - kube_config.
  - Nuovo in questo giro: «seed phrases.md» / «seed_phrases».
- R-329-3 (BASSA): nomi bloccati in eccesso anche in scrittura (stessa linea di R-324-2).
- R-329-4 (COSMETICA): tempo misurato 144µs, non 35µs. La regex è quadratica ma limitata dal tetto dei 255 caratteri, non lineare. La correzione nel report va bene come l'hai proposta.

**Cosa non ho verificato**
- Nomi Unicode che dopo NFKC+casefold non tornano ASCII, su un filesystem che non distingue maiuscole e minuscole. Il problema c'era già prima di questo diff e per provarlo servirebbe un volume APFS dedicato.
- Il comportamento sulla VPS Linux: non riproducibile in dev, ma la regex non dipende dalla piattaforma.

Memoria: ho scritto la riga #330 in /Users/gas/Gas/.claude/agents/memoria_revisore.md e l'ho committata da sola (e67ef2a), senza lezioni nuove. Lo staging è intatto. Prima di committare il diff ricordati `bash scripts/segna_review_ok.sh`, come ultimo passo.

File rilevanti: /Users/gas/Gas/modules/gate/gate.py, /Users/gas/Gas/tests/test_unit_gate.py

## §5 DELTA TEST DEL MOTORE

Nessuna modifica a gas.py (kernel non toccato). Test del cancello: tests/test_unit_gate.py 477 (prima di R-329-1) → 486 passed; con la regex di origin/main i test nuovi falliscono (97 fail, misurato dal revisore #329; 8 fail sui casi con lo spazio, revisore #330).

```
486 passed in 0.19s
```

Suite completa `tests/` (sul diff finale, prima del commit 21cc202):

```
1291 passed, 1 skipped in 200.78s (0:03:20)
```

## §6 STATO CI

```
completed	success	feat(gate): D2 — nomi di credenziali vietati in lettura e scrittura	verifica-bot	feat/gate-d2-credenziali	pull_request_target	38538660297	3m20s	2026-10-14T08:56:02Z
completed	skipped	feat(gate): D2 — nomi di credenziali vietati in lettura e scrittura	verifica-bot	feat/gate-d2-credenziali	pull_request_target	38538646925	10s	2026-10-14T08:55:56Z
completed	success	docs(fine-task): report e handoff — fetta D2 nomi di credenziali (PR …	CI	feat/gate-d2-credenziali	push	38538643894	2m20s	2026-10-14T08:55:54Z
```

Mappatura commit→run:
- `bc7c799` (fine-task precedente, testa del secondo push): run CI 38538643894 **success** (unit-suite, handoff-check); verifica-bot 38538660297 success come workflow, check `verifica-bot` **neutral** (APPROVATO CON RISERVE sulla macchina del bot → decide l'operatore).
- `21cc202` (testa del primo push): run CI 38538493822 **failure** su handoff-check («handoff.md non nel diff di sessione»: atteso, il commit di codice è stato pushato prima di quello dei report; R-ve201-4).
- `e67ef2a`, `28a4abb`: nessuna run su questi SHA (pushati insieme a 21cc202).
- Commit di fine-task attuale (riserve di verifica esterna e bot): run non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- **R-329-2** (BASSA): nomi di credenziali ancora leggibili (Cookies di Chrome, storage-state/auth-state col trattino, api.token col punto, token.old~, kube_config, seed phrases); in più, misura dell'autore: bot_token/auth_token/telegram_token senza estensione e `.config/gh/hosts.yml` (MEDIA proposta per D3).
- **R-329-3** (BASSA): blocco in eccesso anche in scrittura su nomi plausibili (api_key_rotation.md, terraform.tfvars.example, notes.session.md, …).
- **R-329-4** (COSMETICA): regex quadratica ma limitata (144 µs caso peggiore per pezzo), non lineare.
- Tutte tracciate in `reports/stato_progetto.md`; riserve precedenti invariate.
- **Verifica esterna #201** ([commento](https://github.com/Gasss23/Gas/pull/201#issuecomment-6164793654)): R-ve201-1/2/3 (BASSE), R-ve201-4 (COSMETICA). **Bot #201**: R-bot201-1/2 (BASSE), R-bot201-3 (COSMETICA). Tracciate in `reports/stato_progetto.md`.
