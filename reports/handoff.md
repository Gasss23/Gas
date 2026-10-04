# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-10-04 — Test gemelli del gate IP in fine_task_finale e tree unico, branch `test/gate-ip-gemelli-tree-unico`

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #124 (https://github.com/Gasss23/Gas/pull/124), dopo la verifica esterna. Variante A: l'agente lancia `gasmerge 124`, l'operatore conferma digitando `124`.
2. V-3 (verifica #121): vietare nel ruleset i tag `origin/*`?
3. V-5 (verifica #121): mettere `.gitignore`, `knowledge/` e `CLAUDE.md` nel perimetro di review?
4. Prossima fetta PRIORITARIA, già decisa: V-B "vera" (bot di revisione su GitHub). L'operatore dovrà inserire una chiave API nei segreti di GitHub.

---

## §1 SCOPE & ESITO FETTE

- **Merge PR #123**: `FATTA` (operatore, main `b3c6de3`).
- **V-2 verifica #123 = R-149-1 (7 mutation su 11 superstiti in fine_task_finale.sh)**: `FATTA` — test 4f/4g/4h/4i, 12 mutation su 12 uccise.
- **V-1 verifica #123 = R-148-2 senza test**: `FATTA` — test del ref spostato fra le due git grep in entrambi gli script; G9 coperta anche in gasmerge.
- **V-3 verifica #123 — limite UTF-16 del gate IP**: `FATTA` (annotato in stato_progetto come limite noto).
- **V-4 verifica #123 — nota "gate suite non in ci.yml"**: `FATTA` (corretta).
- **R-150-1 — ramo PUSH_EXIT morto in fine_task_finale.sh**: `DEFERITA — bassa, preesistente, comportamento sicuro`.
- **V-B vera**: `DEFERITA — prossima fetta`.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   2 ++
 reports/diff_sessione.md           |  13 +++++--------
 reports/handoff.md                 | 339 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
 reports/stato_progetto.md          |   8 +++++---
 reports/ultimo_report.md           |  34 ++++++++++++++++------------------
 tests/test_unit_gasmerge.py        |  56 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 tests/test_unit_hooks.py           |  86 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 7 files changed, 302 insertions(+), 236 deletions(-)
```

NB: i conteggi di righe sono quelli dello stage PRIMA di riempire §2/§3/§6 (handoff.md conta se stesso): il set di file è esatto, i conteggi no.

## §3 GIT LOG --ONELINE (sessione)

```
7f03488 test(gate-ip): gemelli per fine_task_finale e tree unico — verifica esterna #123 V-1/V-2, review #150 APPROVATO CON RISERVE
a2679b4 chore(revisore): memoria review #150 — APPROVATO CON RISERVE
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione. Il suo hash è stampato al passo 5.

## §4 VERDETTO DEL REVISORE (per commit motore)

Commit `7f03488` (solo test): review #150, incollata per intero.

### Review 150

## VERDETTO: APPROVATO CON RISERVE

Review #150 sul diff staged del branch `test/gate-ip-gemelli-tree-unico`. Contiene solo test: 2 file, +142 righe, nessuno script modificato. Prima della review ho letto CLAUDE.md sez. 5, reports/stato_progetto.md (in modo selettivo, sezioni R-148/R-149) e la memoria del revisore.

**Elementi del diff esaminati**
- `tests/test_unit_hooks.py:2034` (test 4f): una riga latin1 con un IP deve fermare il gate. Rischio esaminato: che il test non colga la mancanza di LC_ALL=C. Esito **ok**: uccide F3, F4, F5, F6 e F7 (LC_ALL=C tolto dalle due git grep, da sed, da `grep -qE` e da `grep -Fx`). Il test bypassa `_run_finale` per un motivo valido: con `text=True` l'output latin1 farebbe fallire la decodifica.
- `tests/test_unit_hooks.py:2044` (test 4g): uno stub git esce con rc 2 quando trova `--and`. Rischio esaminato: che lo `exit 1` del ramo d'errore della allowlist non sia coperto. Esito **ok**: F10 viene ucciso. A scoprirlo è l'asserzione che "allowlistati" sia assente, non quella sul codice di uscita (vedi sotto).
- `tests/test_unit_hooks.py:2056` (test 4h): il rev-parse di `^{tree}` fallisce. Esito **ok**: F11 viene ucciso, grazie all'asserzione che "git grep uscito con codice" sia assente. Né check_handoff.py né check_verdetto.py usano `^{tree}`, quindi lo stub non colpisce altre chiamate.
- `tests/test_unit_hooks.py:2068` (test 4i): HEAD viene spostato fra le due git grep. Rischio esaminato: che lo spostamento non avvenga dopo la PRIMA git grep, rendendo il test vuoto. Esito **ok**. La condizione `$1 = grep && ! --and` scatta solo sulla prima, perché nello script le git grep sono soltanto due (`fine_task_finale.sh:72` e `:96`). Ho verificato con la mutation F12 (`"$IP_TREE"` sostituito da HEAD in entrambe): il test fallisce, quindi lo spostamento avviene davvero fra le due grep. Il caso è deterministico perché non c'è concorrenza.
- `tests/test_unit_gasmerge.py:525` (TestIPTreeUnico): lo stub esegue `update-ref refs/remotes/origin/feat` (riga 549) dopo la prima grep, cioè dopo i due `git fetch --prune` dello script, che quindi non annullano lo spostamento. La mutation GT (`"$IP_TREE"` sostituito dal ref in entrambe le grep) viene uccisa.
- `tests/test_unit_gasmerge.py:560` (TestIPTreeNonRisolvibile): la mutation G9 (nessun `exit 1` dopo un rev-parse fallito, `gasmerge.sh:96`) viene uccisa. Ho confermato anche G10 (ramo d'errore della allowlist, `gasmerge.sh:129`), coperta dal test esistente.
- Contesto: in `scripts/fine_task_finale.sh` il comando `set -e` viene riattivato alle righe 74, 89, 98 e 106 prima del push (riga 129). Vedi la riserva R-150-1.

**Riprodotto**
- **Suite:** pytest senza kernel ed e2e dà **299 passed**, non 298 (293 + 6 test nuovi). Il "+1 da riverificare" è confermato: il conteggio dichiarato era basso di uno.
- **Mutation su fine_task_finale.sh:** F1-F12 tutte uccise, ciascuna da un test con nome:
  - F1/F2 da 4e;
  - F3-F7 da 4f;
  - F8 da 4c;
  - F9 da 7 test;
  - F10 da 4g, F11 da 4h, F12 da 4i.
- **Mutation su gasmerge.sh:** GT, G9 e G10 uccise, una fallita ciascuna.
- **Ripristino:** gli script sono tornati identici all'originale (`git diff -- scripts/` vuoto).
- **Determinismo e pulizia:** 5 esecuzioni consecutive dei 6 test nuovi, tutte verdi. Nessun file lasciato fuori da tmp_path: zero `/tmp/gaspr.*` residui e configurazione git globale invariata (md5 uguale prima e dopo).
- **Gate IP sul tree staged** (`git write-tree`): 0 residui, perché tutte le righe nuove con IP portano il marker.
- **Wall of Shame:** nessuno slicing della history e nessuna simulazione dei tool, cosa attesa dato che il diff contiene solo test.

**Osservazione sulla robustezza dei test.** Con una mutation attiva lo script non si ferma al gate. Prosegue fino a `git push` senza upstream e, per via del `set -e`, esce con 128, oppure con 0 se il push riesce. Per questo `returncode == 1` da solo non prova che il gate abbia bloccato. Tutti e quattro i test nuovi però hanno un'asserzione testuale che discrimina da sola: ho verificato quali asserzioni falliscono sotto F3, F10, F11 e F12.

**Riserve**
- **R-150-1** (bassa, PREESISTENTE, fuori dal diff): in `scripts/fine_task_finale.sh` il `set -e` riattivato prima del push (righe 74/89/98/106) rende morto il ramo `PUSH_EXIT` (righe 130-133). Un push fallito esce con 128 e con il solo messaggio `fatal` di git, mai con "ERRORE git push fallito" né con exit 1. Il comportamento resta sicuro (nessun push, esce con errore), ma il codice di uscita documentato non vale. Va tracciata in stato_progetto.md.
- Cosmetica: in `tests/test_unit_hooks.py:2024` `_stub_git` dichiara di restituire `dict` invece di `dict[str, str]`.

**Rischio escluso**: non ho verificato l'esecuzione in CI su Linux (GNU grep e sed, git di versione diversa), perché non è riproducibile in questo ambiente macOS. Il caso latin1 dipende dal comportamento della regex di libc in locale UTF-8: su glibc la riga potrebbe già matchare anche senza LC_ALL=C, e in quel caso F3-F7 sopravvivrebbero in CI pur essendo uccise qui. Va controllato nell'esito di `unit-suite` della PR.

**Memoria**: aggiunta la riga #150 più una lezione (l'exit code di uno script a più stadi non prova che il gate si sia fermato). Committata in `a2679b4` con `scripts/commit_memoria_revisore.sh`; l'index del diff sotto review è intatto.

File:
- /Users/gas/Gas/tests/test_unit_hooks.py
- /Users/gas/Gas/tests/test_unit_gasmerge.py
- /Users/gas/Gas/scripts/fine_task_finale.sh
- /Users/gas/Gas/.claude/agents/memoria_revisore.md

## §5 DELTA TEST DEL MOTORE

Nessuna modifica a gas.py/brains/modules/ né agli script. Modifiche solo a tests/ (`tests/test_unit_hooks.py`, `tests/test_unit_gasmerge.py`):
- `pytest tests --ignore=tests/test_unit_kernel.py --ignore=tests/e2e`: 293 → **299 passed** (riprodotto dal revisore #150).
- Mutation su fine_task_finale.sh F1–F12 tutte uccise (`-k finale`: es. F3 `1 failed, 12 passed`; F11 `1 failed, 12 passed` dopo l'asserzione aggiuntiva; F12 `1 failed, 12 passed`). Su gasmerge.sh: tree→ref in entrambe le grep `1 failed, 35 passed`; G9 `1 failed`.
- Kernel non rilanciato: non toccato.

## §6 STATO CI

```
completed	failure	test(gate-ip): gemelli per fine_task_finale e tree unico — verifica e…	CI	test/gate-ip-gemelli-tree-unico	push	37215704534	1m12s	2026-10-04T16:09:10Z
completed	success	Merge pull request #123 from Gasss23/fix/gate-ip-allowlist-ci-gasmerge	CI	main	push	37214792815	1m19s	2026-10-04T15:54:57Z
completed	success	docs(gate-ip): fine-task — allowlist IP sul contenuto, tree unico, bi…	CI	fix/gate-ip-allowlist-ci-gasmerge	push	37213780934	1m34s	2026-10-04T15:38:49Z
```

Mappatura commit→run:
- `a2679b4` (memoria #150): nessuna run su questo SHA (pushato insieme a `7f03488`).
- `7f03488` (test): run `37215704534` — `unit-suite: success` (su ubuntu: hooks `77 passed`, gasmerge `37 passed`; 4f/4g/4h/4i, TestIPTreeUnico e TestIPTreeNonRisolvibile tutti PASSED), `handoff-check: failure` (`check_handoff: ERRORE — la sessione tocca il perimetro di review ma reports/handoff.md non è nel diff di sessione: handoff obbligatorio (V-A).`): atteso, l'handoff arriva col commit di fine-task.
- Commit di fine-task (che contiene questo file): run non ancora disponibile alla scrittura dell'handoff. La copertura pre-merge resta a `gasmerge` (gh pr checks --watch).

## §7 RISERVE APERTE

- **R-150-1 (bassa, preesistente)**: `set -e` riattivato prima del push in fine_task_finale.sh → ramo `PUSH_EXIT` morto (push fallito esce con 128, non con il messaggio/exit 1 documentati; sicuro).
- **Limite noto del gate IP**: grep testuale, cieco a UTF-16 e a IP spezzati o codificati (già su main).
- **Discriminazione del test latin1 su Linux non provata**: il test passa in CI, ma su glibc potrebbe passare anche senza `LC_ALL=C` (le mutation F3–F7 sono state uccise solo su macOS).
- Cosmetica #150: `_stub_git` annotato `-> dict` invece di `dict[str, str]`.
- V-3 / V-5 verifica #121: decisione operatore (§0.2, §0.3). R-143-2 (ci.yml dalla PR) → V-B vera.

### Verdetto INTEGRALE della verifica esterna PR #123 (handoff `2445074`)

Unica aggiunta al testo: il marker `# gasmerge-ip-ok` in fondo alle righe che contengono un IP di esempio, richiesto dal gate IP su reports/.

VERIFICA ESTERNA PR #123 (handoff pinnato 2445074) — APPROVATO CON RISERVE

Metodo: clone usa-e-getta nella scratchpad, checkout di 24450745ef7328ca76f183e020791069e7ad34ed (coincide con headRefOid della PR; merge-base con main ee95197). Ho letto per intero il diff di scripts/, ci.yml e dei report. Interprete: /Users/gas/Gas/.venv (Python 3.14.7, pytest 9.1.1), macOS con grep BSD.
Cosa ho eseguito:
- pytest senza kernel e senza e2e al commit.
- gasmerge+hooks alla base e al commit.
- Controprove con gasmerge.sh preso da main (tramite GASMERGE_SCRIPT) e con fine_task_finale.sh di main (in una copia).
- Mutation su gasmerge.sh (10) e su fine_task_finale.sh (11), più una mutation che rimette il TOCTOU.
- 23 sonde end-to-end su repo git reali con bare remote e stub gh (probe.py, scratchpad).
- gasmerge.sh reale e fine_task_finale.sh reale contro il ref reale del branch.
- API GitHub per run, check e ruleset.
Il repo reale non è stato toccato: `git status` mostra solo .agents/, .codex/ e AGENTS.md, già non tracciati prima.

CLAIM VERIFICATI
- §2, set di file: VERO, 10 file identici a `git diff --stat` reale dalla base. I conteggi di righe del §2 sono 417/237, il reale è 433/232. Il NB del §2 lo dichiara (cosmetico).
- §3, log: VERO. I 3 commit coincidono con `git log ee95197..HEAD` meno 2445074, escluso per costruzione.
- Test 284 → 293: VERO. Ho riprodotto 293 passed (73s). Su gasmerge+hooks sono 99 alla base e 108 al commit (+9).
- Controprove con gli script di main:
  - gasmerge.sh: `-k "avvelenato or apice"` dà 3 failed; `-k Binari` dà 2 failed.
  - fine_task_finale.sh: `finale_4` dà 2 failed, cioè 4d e 4e.
- Mutation su gasmerge.sh uccise da un test:
  - `--and --not` → `--and`;
  - `0|1)` → `0)`;
  - seconda git grep sul ref invece che sul tree (uccisa solo per il prefisso diverso, vedi V-1);
  - senza `-z`; senza `tr`;
  - perimetro di main abbreviato (`git show origin/main:`);
  - togliere `LC_ALL=C` da sed.
- R-147-1 (marker nel prefisso) CHIUSA, con le sonde del bypass originale:
  - branch `fix/gasmerge-ip-ok` e path `docs/gasmerge-ip-ok.py`: BLOCCO, e falliscono con lo script di main;
  - nome di file con a-capo (anche con frammento finto di output git grep): nessun bypass;
  - marker maiuscolo e marker nella riga successiva: BLOCCO.
- R-148-3 CHIUSA su macOS: file binario con NUL e riga latin1 danno BLOCCO. Con lo script di main dànno OK.
- R-148-1 CHIUSA solo su gasmerge.sh: lo stub che fa fallire la grep con `--and` produce "BLOCCO: git grep (allowlist)". Su fine_task_finale.sh no (V-2).
- CI sullo SHA 2445074: run 37213780934 success. unit-suite 73+19+40+74+35 passed, handoff-check success. Il passo "Run gasmerge suite" ha `35 passed in 4.21s` su ubuntu: la V-2 della verifica #122 è davvero chiusa.
- Run sul commit 09d4005 (37213618231): handoff-check failure e unit-suite success, come dichiarato nel §6.
- Ruleset main-lock: VERO. Required check unit-suite e handoff-check, policy strict, 0 approvazioni, nessuna regola sui tag.
- Gate IP sul branch reale:
  - gasmerge.sh reale con stub gh dà "Tutti gli IP sono allowlistati — OK" (nessun falso blocco);
  - il promemoria elenca i 6 file di motore;
  - fine_task_finale.sh reale dà "Gate IP: allowlistati — OK" con check_handoff e check_verdetto OK.
- Correzione dell'affermazione falsa sul test non-ASCII in CI: VERO, il file è ora in ci.yml e gira.

FINDING
- V-1 (BASSA) — R-148-2 "CHIUSA" (tree risolto una volta) non ha alcun test che la protegga.
  - Sonda: rimetto `"refs/remotes/origin/$BRANCH"` al posto di `"$IP_TREE"` in tutte e due le git grep di gasmerge.sh. Risultato: 35 passed su 35. Questo rimette il TOCTOU.
  - La mutation sulla sola seconda grep fallisce per caso, perché cambia il prefisso.
  - Il revisore ha dichiarato la riserva R-148-2 chiusa e il handoff §1 dice FATTA. Nel §7 non è tracciata come "senza test".
  - Fix: uno stub git che sposta il ref fra le due git grep, oppure dichiararla "chiusa per costruzione, non testata".
- V-2 (BASSA) — R-149-1 sottostima i superstiti in fine_task_finale.sh. Dichiara 2 mutation, io ne trovo 7 su 11 che sopravvivono (9 passed su 9 in `-k finale`):
  - `LC_ALL=C` tolto dalla prima git grep (dichiarata);
  - `exit 1` tolto dal ramo d'errore della allowlist (dichiarata);
  - `LC_ALL=C` tolto dalla seconda git grep (non dichiarata);
  - `LC_ALL=C` tolto da sed, da `grep -qE` e da `grep -Fx` (non dichiarate);
  - `exit 1` tolto dopo il rev-parse del tree fallito (non dichiarata; probabilmente ancora fail-closed per rc 128, ma senza test).
  - Sono uccise le altre 4: `-a` sulle due grep, `-Fx`→`-F`, `--and --not`→`--and`.
  - L'effetto pratico è piccolo, perché il codice è identico a quello di gasmerge.sh, che i test coprono. Ma la riserva va riscritta e i test gemelli vanno fatti: oggi il gate di fine_task_finale.sh non ha la copertura che stato_progetto e handoff suggeriscono.
- V-3 (BASSA, limite noto, non una regressione) — il gate IP è una grep testuale. Resta cieco ai file in UTF-16: sonda con `"H=8.8.8.8\n".encode("utf-16")` dà "0 IP trovati — OK". La stessa cosa vale per IP spezzati o codificati. Non è dichiarato nel handoff.  # gasmerge-ip-ok
  - Le righe con più di 64k danno un falso blocco ("errore nel filtro", rc=2): fail-closed, dichiarato dal revisore.
- V-4 (COSMETICA) — nel §6 "run non ancora disponibile" per il commit finale è superato: la run 37213780934 è verde. Gli altri difetti cosmetici:
  - il conteggio righe del §2 (dichiarato);
  - stato_progetto dice ancora "Gate test … non in ci.yml — R-gate-3", ma il gate suite gira in CI (74 passed nel log);
  - dopo il commit finale il `pr checks` era in corso, quindi il handoff non poteva dire altro.
- V-5 (BASSA, nota) — R-143-2, invariata: ci.yml viene preso dalla PR. Il nuovo step `if: always()` è presente nella PR, ma una PR successiva potrebbe rimuoverlo senza che il check required se ne accorga. È già tracciata e demandata alla V-B vera.
- Nessuna regressione trovata rispetto a main: 23 sonde (CRLF, riga senza a-capo finale, marker substring, nomi con `:` o unicode, `.gitattributes binary/-diff`, IPv6-mapped, 999.x, "8.8.8.8.8", loopback+pubblico) danno il comportamento atteso o fail-closed. L'unico fail-open è UTF-16 (V-3), già presente su main.

NON VERIFICATO
- Il passo "Job summary" della CI: non ho potuto leggere il $GITHUB_STEP_SUMMARY, quindi non so se la riga "Gasmerge suite" è popolata. Ho verificato solo che il codice sia presente e che il passo precedente sia verde.
- Comportamento di GNU grep (ubuntu) su latin1 e NUL con `LC_ALL=C`: provato solo dalla CI (35 passed, che include i test su latin1 e binario). Non ho un GNU grep locale per le mutation su Linux.
- Fetch concorrente reale tra le due git grep (TOCTOU): non riproducibile in modo deterministico, ragionato soltanto (vedi V-1).
- Esecuzione reale di gasmerge contro GitHub (merge vero): non lanciata, per non toccare produzione; ho usato stub gh e il ref reale del branch.
- Le review #148/#149 incollate nel §4: non ho l'output originale del revisore; ho riprodotto i numeri (289/293), la maggior parte delle controprove e delle mutation citate.

RACCOMANDAZIONE
La PR #123 è mergiabile: V-1/V-2/V-3 della verifica #122 bis sono chiuse e provate, 293 passed riprodotti, CI verde sullo SHA, ruleset come dichiarato. Prima della V-B vera, in una micro-fetta:
1. Scrivere i due test gemelli per fine_task_finale.sh (latin1 e stub git che fallisce su `--and`, più LC_ALL=C sulla seconda grep e sul filtro) e correggere R-149-1: i superstiti sono 7, non 2.
2. Scrivere un test del tree unico, o declassare R-148-2 a "chiusa per costruzione, non testata" in stato_progetto e nel handoff.
3. Annotare il limite UTF-16 del gate IP nel handoff e in stato_progetto.
V-3/V-5 della #121 restano decisioni dell'operatore.

Esito: PR #123 mergiata (operatore); V-1, V-2, V-3 e la nota R-gate-3 di V-4 chiusi in questa PR #124; V-5 (R-143-2) → V-B vera.
