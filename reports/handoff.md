# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-10-04 — Promemoria di gasmerge dal perimetro, ref completi, .gitignore audio, branch `fix/gasmerge-perimetro-gitignore`

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #122 (https://github.com/Gasss23/Gas/pull/122), dopo la verifica esterna. Variante A: l'agente lancia `gasmerge 122`, l'operatore conferma digitando `122`.
2. V-3 (verifica #121): vietare nel ruleset i tag `origin/*`? Oggi la difesa sono i ref completi negli script.
3. V-5 (verifica #121): mettere `.gitignore`, `knowledge/` e `CLAUDE.md` nel perimetro di review?
4. Prossima fetta PRIORITARIA, già decisa: V-B "vera" (bot di revisione su GitHub). L'operatore dovrà inserire una chiave API nei segreti di GitHub.

---

## §1 SCOPE & ESITO FETTE

- **V-1 verifica #121 — gasmerge legge il perimetro di review**: `FATTA`.
- **R-144-1 — ref abbreviato in gasmerge.sh / promemoria_end.sh / fine-task.md**: `FATTA`.
- **V-2 verifica #121 — .gitignore audio e output dei client (R-143-4 parziale)**: `FATTA`.
- **R-145-1 — rename e nomi non-ASCII nel promemoria**: `FATTA` (stessa fetta, review #146).
- **R-145-2 — `*_output.*` nascondeva i sorgenti**: `FATTA` (stessa fetta, review #146).
- **Correzioni stato_progetto (R-143-4 PARZIALE, R-143-1 chiusa dopo il merge di #121)**: `FATTA`.
- **Tracciamento V-3 / V-5 della verifica #121**: `FATTA` (aperte, decisione operatore).
- **V-B vera**: `DEFERITA — prossima fetta`.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   3 +++
 .claude/commands/fine-task.md      |   2 +-
 .claude/hooks/promemoria_end.sh    |   2 +-
 .gitignore                         |   9 +++++++++
 reports/diff_sessione.md           |  19 ++++++++-----------
 reports/handoff.md                 | 261 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++-------------------------------------------------------------------------------------------------------------------------------------------------------------------------
 reports/stato_progetto.md          |   6 ++++--
 reports/ultimo_report.md           |  38 ++++++++++++++++++++------------------
 scripts/gasmerge.sh                |  56 ++++++++++++++++++++++++++++++++++++++++----------------
 tests/test_unit_gasmerge.py        |  97 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++-
 10 files changed, 274 insertions(+), 219 deletions(-)
```

## §3 GIT LOG --ONELINE (sessione)

```
03e01f8 fix(gasmerge): promemoria dal perimetro di review, ref completi, .gitignore audio — review #145/#146 APPROVATO CON RISERVE
2ffa88c chore(revisore): memoria review #146 — APPROVATO CON RISERVE
30ba09f chore(revisore): memoria review #145 — APPROVATO CON RISERVE
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione. Il suo hash è stampato al passo 5.

## §4 VERDETTO DEL REVISORE (per commit motore)

Commit `03e01f8`: la #145 sul diff iniziale e la #146 sul delta che chiude R-145-1 e R-145-2. Entrambe sono incollate per intero.

### Review 145

## VERDETTO: APPROVATO CON RISERVE

**Letture preliminari fatte:** CLAUDE.md (sez. 5, 8, 10), reports/stato_progetto.md (solo le voci R-144-1, R-143-4, V-1 e V-2) e .claude/agents/memoria_revisore.md (contatori #137–#144 e lezioni del 2026-10). Il Wall of Shame non c'entra con questo diff: non tocca codice Python del motore, né history né tool. Guardrail del motore (cap a 10 iterazioni, `_get_window`, cap sull'output) non toccati.

**Riproduzioni**
- test_unit_hooks + test_unit_gasmerge + test_unit_gate: **168 passed**, numero confermato.
- Controprova sul gasmerge.sh di `refs/remotes/origin/main`: `-k TestPerimetroPromemoria` dà **3 failed, 1 passed**. Il test doc-only passa per costruzione, come dichiarato.

**Elementi del diff esaminati**
- `scripts/gasmerge.sh:153` — costruisce PERIM_VOCI come unione del perimetro di main, del perimetro del branch e delle voci `scripts/` e `.claude/`; poi toglie commenti e spazi, scarta le righe vuote e ordina con `sort -u`. Rischio esaminato: con `set -euo pipefail` (riga 2) un `grep -v` senza output darebbe rc 1 e farebbe uscire lo script. Non succede: il `printf` garantisce sempre almeno 2 righe, e i `git show … || true` dentro il gruppo neutralizzano il ref mancante — **ok**.
- `scripts/gasmerge.sh:162` — doppio ciclo: una voce che finisce con `/` vale come prefisso, le altre come path esatto, e `"$v"` è quotato quindi niente glob. Se il perimetro è illeggibile su tutti e due i lati (PERIM_LETTO=0, righe 157-160), ogni file conta come motore. Rischio esaminato: falsi "doc-only". Sonde: tag `origin/main` puntato sul branch → promemoria corretto (P3); cancellazione di `gas_identity.md` → promemoria corretto (P4) — **ok**.
- `scripts/gasmerge.sh:141` — `git diff --name-only` senza `--no-renames` e senza `core.quotePath=false`. Rischio: un file del perimetro rinominato o con nome non-ASCII sparisce dal confronto (lezione del 2026-10-04 in memoria). Le sonde lo confermano. **P1**: `git mv gas_identity.md docs/x.md` → "nessuno (doc-only)". **P2**: `clients/caffè.py` → "nessuno (doc-only)". Il problema c'era già con la vecchia regex, quindi non è una regressione; e lo script è un promemoria, non un gate (hook e check_handoff usano già `--no-renames -z`) — **riserva R-145-1**.
- `.claude/hooks/promemoria_end.sh:45` — merge-base con il ref completo `refs/remotes/origin/main`. Rischio: rottura del ramo di fallback. È invariato: WARN nel log ed exit 0 — **ok**.
- `.claude/commands/fine-task.md:21` — solo il testo del messaggio d'errore, allineato al ref completo. È la riserva estetica della #144, chiusa — **ok**.
- `.gitignore:41` — `clients/**/*_output.*`. Rischio: il pattern prende anche i sorgenti. `git check-ignore -v --no-index` conferma che `clients/voice/tts_output.py` verrebbe ignorato. L'hook (`--untracked-files=all`) non vede i file ignorati, quindi un sorgente con quel nome sparirebbe senza avviso: non arriverebbe mai alla review né al repo. Nessun file tracciato è colpito oggi: l'unico `*_output.*` tracciato è `reports/e2e_k3bis_output.txt`, fuori da `clients/` — **riserva R-145-2**.
- `tests/test_unit_gasmerge.py:337` — la fixture `_repo` costruisce un bare repo reale con perimetro opzionale su main e sul branch. I 4 test coprono: voce esatta, prefisso con quasi-omonimo `clientsX.md`, branch che restringe il perimetro, perimetro assente. Le asserzioni sono specifiche ("PERIMETRO DI REVIEW", "illeggibile", assenza di "doc-only") — **ok**.

**Riserve**
- **R-145-1** (media, c'era già prima di questa fetta). Fix verificato su una copia: `ENGINE_DIFF=$(git -c core.quotePath=false diff --no-renames --name-only "refs/remotes/origin/main...refs/remotes/origin/$BRANCH")`. Con questa modifica P1 e P2 elencano correttamente `gas_identity.md` e `clients/caffè.py`. Fa però fallire `test_git_diff_name_only_error_blocks`, perché lo stub `_make_stub_git_diff_name_only_fail` (tests/test_unit_gasmerge.py:119) controlla `$1 = diff`, e con `-c` davanti `$1` cambia. Va adeguato anche lo stub. Consiglio di chiuderla in questa stessa fetta: costa due flag e un test.
- **R-145-2** (minore). Restringere `.gitignore:41` alle estensioni degli artefatti (es. `clients/**/*_output.wav`, `.mp3`, `.txt`, `.json`), oppure chiarire nel commento che i sorgenti `*_output.py` vanno aggiunti con `-f`. Nota a margine: `*.wav` globale ignorerebbe anche futuri fixture audio in `tests/`.

**Rischi esplicitamente esclusi**
- Esecuzione reale di `gasmerge` contro GitHub (gh vero, PR reale): non riprodotta. Uso solo gli stub gh dei test e i bare repo locali, perché lanciare lo script vero farebbe un fetch e un merge sul repo di produzione.
- Nomi di file contenenti un a-capo: non provati. Il ciclo `read -r` riga per riga non li gestirebbe; è un caso marginale per un promemoria.
- Comportamento con il perimetro presente ma vuoto (solo commenti) su main: non sondato. Restano attive solo `scripts/` e `.claude/`, scelta coerente con la "fonte unica".

**Memoria:** riga #145 e una lezione nuova aggiunte e salvate nel repo con lo script dedicato: commit `30ba09f` su `/Users/gas/Gas/.claude/agents/memoria_revisore.md`.

**File rilevanti**
- `/Users/gas/Gas/scripts/gasmerge.sh`
- `/Users/gas/Gas/.gitignore`
- `/Users/gas/Gas/tests/test_unit_gasmerge.py`
- `/Users/gas/Gas/.claude/hooks/promemoria_end.sh`
- `/Users/gas/Gas/.claude/commands/fine-task.md`
- Sonda: `/private/tmp/claude-501/-Users-gas-Gas/91091029-3df7-47ca-a712-d6baf2fbda65/scratchpad/sonda.py`

### Review 146

## VERDETTO: APPROVATO CON RISERVE

Review #146 sul diff staged aggiornato del branch `fix/gasmerge-perimetro-gitignore`. R-145-1 e R-145-2 sono chiuse. Restano solo due riserve di poco conto, che non bloccano il commit.

**Esiti rifatti da me**
- `test_unit_gasmerge` + `test_unit_hooks` + `test_unit_gate`: **170 passed**, coincide con il vostro 26 + 144.
- Stessi test contro il `gasmerge.sh` di `refs/remotes/origin/main`, con `-k "Perimetro or DiffGuard"`: **5 failed, 2 passed**, come dichiarato. Passano il test doc-only e DiffGuard, ed è atteso.
- Ho tolto un solo flag alla volta:
  - senza `--no-renames` fallisce solo `test_rename_fuori_perimetro_resta_motore`;
  - senza `core.quotePath=false` fallisce solo `test_nome_non_ascii_nel_perimetro`.
  Ogni flag ha quindi un test suo che fallisce se lo si toglie.
- Ho rilanciato le sonde della #145 sul diff nuovo:
  - P1 (rename `gas_identity.md` → `docs/x.md`): ora mostra `gas_identity.md`;
  - P2 (`clients/caffè.py`): ora mostra il nome in chiaro, non quotato;
  - P3 (tag `origin/main` che punta al branch) e P4 (cancellazione): promemoria corretto.

**Elementi del diff esaminati**
- `scripts/gasmerge.sh:144` — `git -c core.quotePath=false diff --no-renames --name-only "refs/remotes/origin/main...refs/remotes/origin/$BRANCH"`. Rischio esaminato: un file del perimetro rinominato verso fuori, o con nome non-ASCII, che sparisce dal promemoria. Ora compare anche il vecchio path e i nomi non sono più tra virgolette. Il ramo d'errore `DIFF_RC` è invariato — **ok**.
- `tests/test_unit_gasmerge.py:119` — lo stub riconosce `diff` in qualunque posizione (`grep -qx 'diff'`) insieme a `--name-only`. Rischio esaminato: uno stub che non intercetta più la chiamata e lascia passare il test del ramo d'errore senza verificarlo davvero. `test_git_diff_name_only_error_blocks` resta verde, quindi lo stub intercetta il `git -c … diff`. `git diff --stat` (riga 42) e `git show` non lo attivano — **ok**.
- `tests/test_unit_gasmerge.py:395` — rename test: `gas_identity.md` (20 righe identiche) viene committato su main, il branch lo integra e poi fa `git mv` puro. Rischio: che git non riconosca il rename e il test passi anche senza il fix. La copia è identica al 100%, quindi il rename scatta, e la mutation qui sopra lo conferma — **ok**.
- `tests/test_unit_gasmerge.py:412` — `clients/caffè.py` con perimetro `clients/`. Rischio: differenze NFC/NFD tra macOS e Linux. In locale passa; il comportamento in CI Linux è indicato tra i rischi non verificati — **ok**.
- `.gitignore:41` — ora `clients/**/*_output.{wav,mp3,txt,json}`, su righe separate. Rischio: sorgenti ignorati senza che l'hook se ne accorga. `git check-ignore -v --no-index`: `clients/voice/tts_output.py` **non** è più ignorato; `a_output.wav`, `a_output.json` e `c_output.txt` (anche annidato) sì — **ok**.

**Riserve (di poco conto)**
- Cosmetica: le righe `clients/**/*_output.wav` e `*_output.mp3` non servono, perché `*.wav` e `*.mp3` sono già ignorati ovunque.
- Dichiarata: `*.wav` ignorato in tutto il repo è una scelta dell'operatore (V-2). Eventuali file audio di prova futuri in `tests/` andranno aggiunti con `git add -f`.

**Rischi esplicitamente esclusi**
- Non ho eseguito il test non-ASCII su Linux, dove gira la CI. Sono in dev su macOS con `precomposeunicode`. Python scrive NFC e git su Linux restituisce i byte tali e quali, quindi mi aspetto che passi, ma lo confermerà la run `unit-suite`.
- Non ho eseguito `gasmerge` reale contro GitHub, per lo stesso motivo della #145: farebbe fetch e merge sul repo di produzione.
- Non ho provato nomi di file che contengono un a-capo: il ciclo che li legge va riga per riga e non li gestirebbe. È un caso marginale per un promemoria.

**Memoria:** ho aggiunto la riga #146, senza lezioni nuove, in `/Users/gas/Gas/.claude/agents/memoria_revisore.md` e l'ho committata (`2ffa88c`). La riga #145 era già in `30ba09f`.

**File rilevanti**
- `/Users/gas/Gas/scripts/gasmerge.sh`
- `/Users/gas/Gas/tests/test_unit_gasmerge.py`
- `/Users/gas/Gas/.gitignore`
- `/Users/gas/Gas/.claude/hooks/promemoria_end.sh`
- `/Users/gas/Gas/.claude/commands/fine-task.md`

## §5 DELTA TEST DEL MOTORE

Nessuna modifica a gas.py/brains/modules/. Modifiche a tests/ (solo `tests/test_unit_gasmerge.py`):
- `pytest tests --ignore=tests/test_unit_kernel.py --ignore=tests/e2e`: 275 → **281 passed** (+6 `TestPerimetroPromemoria`).
- Riepilogo reale: `281 passed in 65.88s (0:01:05)`.
- Controprova sul gasmerge.sh di main, `-k "Perimetro or DiffGuard"`: `5 failed, 2 passed`.
- Kernel non rilanciato: non toccato.

## §6 STATO CI

```
completed	failure	fix(gasmerge): promemoria dal perimetro di review, ref completi, .git…	CI	fix/gasmerge-perimetro-gitignore	push	37210021530	1m3s	2026-10-04T14:38:46Z
completed	success	Merge pull request #121 from Gasss23/fix/gate-rename-perimetro-ci	CI	main	push	37206707321	1m4s	2026-10-04T13:44:41Z
completed	success	docs(gate-rename): fine-task — correzione §6 (mappatura commit→run re…	CI	fix/gate-rename-perimetro-ci	push	37206249513	1m13s	2026-10-04T13:37:00Z
```

Mappatura commit→run:
- `30ba09f` (memoria #145): nessuna run su questo SHA (pushato insieme a `03e01f8`, la run testa solo il commit di testa).
- `2ffa88c` (memoria #146): nessuna run su questo SHA (stesso push).
- `03e01f8` (fix): run `37210021530` — `unit-suite: success`, `handoff-check: failure`. Causa reale dal log: `check_handoff: ERRORE — la sessione tocca il perimetro di review ma reports/handoff.md non è nel diff di sessione: handoff obbligatorio (V-A).` Atteso: a quel push l'handoff di sessione non esisteva ancora; lo aggiunge il commit di fine-task.
- Commit di fine-task (che contiene questo file): run non ancora disponibile alla scrittura dell'handoff. La copertura pre-merge resta a `gasmerge` (gh pr checks --watch).

## §7 RISERVE APERTE

- Riserve minori #146: righe `clients/**/*_output.{wav,mp3}` ridondanti con `*.wav`/`*.mp3`; fixture audio future in tests/ vanno aggiunte con `git add -f`.
- Test non-ASCII verificato solo su macOS (conferma attesa dalla run `unit-suite` su Linux).
- V-3 verifica #121 (tag `origin/*` non vietati dal ruleset) e V-5 verifica #121 (`.gitignore`, `knowledge/`, `CLAUDE.md` fuori dal perimetro): aperte, decisione operatore.
- R-143-2 (ci.yml dalla PR) e R-143-3 (stallo con falso blocco su main): invariate, R-143-2 → V-B vera.
