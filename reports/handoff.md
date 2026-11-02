# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-11-02 — Cervello forte: difesa contro il futuro default `--bare` di `claude -p` (chat M2, coordinata da M1)

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #321 (https://github.com/Gasss23/Gas/pull/321). Numero e URL dalla risposta JSON dell'integrazione GitHub (`create_pull_request`: `{"id":"5114638285","url":"https://github.com/Gasss23/Gas/pull/321"}`); `gh` nel cloud non è autenticato. Stanotte niente merge (M1): decide l'operatore.
2. Sul Mac: `python3 gas.py doctor` → la riga «Cervello forte · login» deve dire «login dell'abbonamento».

---

## §1 SCOPE & ESITO FETTE

- **1. Figlio `claude -p` senza chiavi API (fail-closed se diventa bare)**: `FATTA` — test che lo fissa.
- **2. Flag o variabile per restare non-bare**: `FATTA (nessuno documentato)` — scritto nel docstring.
- **3. Riga «login» nel doctor, con versione, zero token**: `FATTA` — `stato_abbonamento()` in brains, 3 righe in gas.py autorizzate da M1.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |  3 +++
 brains/claude_cli.py               | 52 ++++++++++++++++++++++++++++++++++++++++++++++++++++
 gas.py                             |  3 +++
 reports/diff_sessione.md           | 16 +++++++---------
 reports/handoff.md                 | n/d
 reports/stato_progetto.md          |  3 ++-
 reports/ultimo_report.md           | 31 +++++++++++++------------------
 tests/test_unit_claude_cli.py      | 90 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 tests/test_unit_dotenv.py          | 20 ++++++++++++++++++++
```

NB: regola «n/d» — il conteggio di `reports/handoff.md` non è misurabile mentre lo si scrive; riga di totale tolta.

## §3 GIT LOG --ONELINE (sessione)

```
2f5d53d fix(forte): difesa contro il futuro default --bare di claude -p; riga «login» nel doctor (chat M2)
26ecd7a chore(revisore): memoria review #632 — BOCCIATO
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione. Il suo hash è nel `git log` del branch dopo il push.

## §4 VERDETTO DEL REVISORE (per commit motore)

Il commit 2f5d53d è stato rivisto in due passaggi sullo stesso diff staged (tra i due cambia solo `stato_abbonamento` e i suoi test). Verdetti integrali:

Review #632-M2 (primo passaggio):

## VERDETTO: BOCCIATO

Diff controllato: diff staged con sha256 009335ee, base b472fe1, branch fix/forte-non-bare-m2, 4 file e 137 righe aggiunte. Ho rilanciato i test: test_unit_claude_cli più test_unit_dotenv danno 57 passed. Non ho rilanciato la suite del kernel.

**Motivo del blocco**
- `brains/claude_cli.py:416` (la riga `versione = (ver.stdout or "").strip().splitlines()[0][:60] ...`): ricava la versione dall'output di `claude --version`. Ho cercato le eccezioni che sfuggono al blocco `except (OSError, subprocess.SubprocessError)`. Esito: **blocco**. Ci sono due casi, entrambi riprodotti.
  1. Se `--version` stampa solo spazi o un a capo, `ver.stdout` non è vuoto, ma dopo `strip()` diventa `""` e `splitlines()[0]` dà IndexError. Ho lanciato `gas.py doctor` con `GAS_CLAUDE_BIN` puntato a una CLI finta che fa solo `echo`: il doctor si ferma con un traceback (`IndexError: list index out of range`).
  2. Se la CLI stampa byte non UTF-8 (prova con `printf "\377\376"` e LANG=C.UTF-8), `subprocess.run(text=True)` alza UnicodeDecodeError. È un ValueError, non un SubprocessError, quindi sfugge allo stesso modo.
  - Il docstring promette «Mai un'eccezione» e il progetto chiede «zero crash»: il doctor è proprio lo strumento di diagnosi e non deve morire per un output strano della CLI.
  - Correzione minima:
    - `errors="replace"` nella `subprocess.run`;
    - versione presa con `next(iter(stdout.strip().splitlines()), "?")`;
    - un `except Exception` finale che ritorna `("WARN", "non verificabile …")`;
    - due casi di test in più (stdout `"\n"` e byte non UTF-8 con il runner vero).

**Elementi esaminati che vanno bene**
- `brains/claude_cli.py:406` (`stato_abbonamento`): lancia solo `--version` e `auth status`, mai `-p`. Rischio cercato: spendere token. Esito: ok. Il test parametrico fissa la sequenza esatta dei comandi e la CLI finta del test del doctor esce con 9 su qualunque altro comando. Il timeout di 15 s per comando arriva come TimeoutExpired, che è un SubprocessError, quindi viene preso.
- `brains/claude_cli.py:430`: smista i casi none, rc≠0, api_key e simili. Rischio cercato: dare OK quando il login non è l'abbonamento. Esito: ok. OK arriva solo per claude.ai e oauth_token; JSON illeggibile o metodo mancante danno WARN. Nota cosmetica: con rc≠0 e `api_key` il messaggio dice «nessun login», ma l'esito resta WARN, che è corretto.
- `gas.py:5087`: chiama `stato_abbonamento` solo se `binario` è stato trovato. Rischio cercato: modifiche fuori dal perimetro autorizzato da M1. Esito: ok. In gas.py ci sono 3 righe in tutto (import a `gas.py:35` e la chiamata nel doctor), dentro le 3-4 autorizzate. Il crash descritto sopra, però, si propaga fin qui.
- `brains/claude_cli.py:53` (contesto, `_ENV_PERMESSE`): elenco esatto delle variabili che il figlio riceve. Rischio cercato: il comportamento fail-closed, cioè che una chiave API arrivi al figlio. Esito: ok. Nessuna ANTHROPIC_*, *_API_KEY, CLAUDE_CODE_SIMPLE o BEDROCK passa; CLAUDE_CODE_OAUTH_TOKEN sì. Lo verificano `tests/test_unit_claude_cli.py:398` e, con il runner vero, `tests/test_unit_claude_cli.py:446`.
- `tests/test_unit_dotenv.py:265`: riga «login» del doctor con CLI finta, OK per claude.ai e WARN per api_key, con la versione. Esito: ok.
- Nessuno slicing della history e nessun output dei tool simulato: il diff non tocca `run_turn` né la finestra dei messaggi.

**Riserve da annotare (non bloccanti)**
- BASSA: alla scadenza del timeout, `subprocess.run` uccide solo il processo figlio diretto. Se un processo nipote tiene aperte le pipe, la seconda `communicate()` può restare bloccata, quindi il limite di 15 s non è garantito in assoluto. Caso teorico.
- BASSA: nel caso peggiore il doctor aspetta circa 30 s (due comandi da 15 s).

**Cosa non ho verificato**
Non ho provato il comportamento della CLI `claude` vera: qui non c'è login, e non so se `auth status` stampi davvero il campo `authMethod`, né se in una versione futura possa aprire una sessione. Mi baso sulla documentazione cli-reference citata da M1. Non ho rilanciato la suite del kernel (1063 PASS), che resta un'affermazione della chat.

**Memoria del revisore**
Ho scritto la riga #632-M2 con la lezione nuova in `/home/user/Gas/.claude/agents/memoria_revisore.md` e l'ho committata da sola (commit 26ecd7a, solo quel file). Il diff staged del motore è rimasto com'era. Dopo la correzione serve una nuova review.

Review #633-M2 (diff finale committato in 2f5d53d):

## VERDETTO: APPROVATO CON RISERVE

Ri-review dopo la bocciatura #632-M2. Branch fix/forte-non-bare-m2, diff staged di 4 file. Il motivo del blocco è chiuso: con le uscite strane della CLI che ho provato il doctor non va più in traceback.

**Cosa ho esaminato nel diff**
- `brains/claude_cli.py:409` — `subprocess.run` ora ha `errors="replace"`. Rischio esaminato: `UnicodeDecodeError` con byte non UTF-8. Esito: ok. Anche senza `errors=`, quell'errore è un `ValueError` e verrebbe comunque preso da `except ValueError` (`brains/claude_cli.py:421`): la difesa è doppia.
- `brains/claude_cli.py:414` — `next(iter(righe), "?")[:60]`. Rischio esaminato: `IndexError` con stdout vuoto, di soli spazi o di soli a capo, e con returncode diverso da 0. Esito: ok, la versione diventa «?».
- `brains/claude_cli.py:415-416` — `json.loads` è dentro lo stesso try. Con un runner che restituisce bytes, quelli non UTF-8 danno un `ValueError`, che viene preso. Esito: ok.
- `brains/claude_cli.py:424` — `except Exception` finale, che risponde «non verificabile (Tipo)». Esito: ok. È coerente con «robustezza > potenza» e con la regola della sez. 9 (eccezioni intercettate, fallback, mai crash), applicata qui al doctor. Il codice dopo il try (`brains/claude_cli.py:426-437`) usa `st` solo quando `metodo` è una stringa, quindi `st` esiste sempre.
- `gas.py:5088` — chiamata dal doctor solo se `binario` è valorizzato. Non cambia rispetto a #632. Esito: ok.
- `tests/test_unit_claude_cli.py:61` e `tests/test_unit_claude_cli.py:69` — test nuovi: versione «\n», «   » e «»; CLI finta col runner vero che stampa \377\376; runner che solleva `KeyError`. Esito: ok.

**Prove che ho rifatto io**
- Test di `claude_cli` e `dotenv`: **61 passed**.
- `GAS_CLAUDE_CLI=1 GAS_CLAUDE_BIN=<CLI finta> python3 gas.py doctor`, con due CLI finte: una che stampa `\377\376` e una che stampa `"   "`. In entrambi i casi esce la riga `[WARN ] Cervello forte login … non verificabile (versione …)` e nessun traceback.
- Mutante: tolto `errors="replace"` e ristretto l'`except` finale a `ZeroDivisionError` → **1 failed** (`test_stato_abbonamento_byte_non_utf8_e_errori_inattesi`). Il file è stato ripristinato; `git diff` non staged è vuoto.
- Antipattern della sez. 5: niente slicing della history (`[:60]` taglia una stringa di versione, non i messaggi) e niente simulazione dell'output dei tool.

**Riserve**
- R-633-1 BASSA (riportata dalla #632): un processo nipote che tiene aperte le pipe e l'attesa massima di circa 30 s (2 × timeout di 15 s). Sono già annotate nei report.
- R-633-2 BASSA: nessun test fissa da solo il ruolo di `errors="replace"`. Il ramo `except ValueError` lo copre comunque, quindi un mutante che toglie solo `errors=` probabilmente sopravvive. Il comportamento resta corretto.

**Cosa non ho verificato**
Non ho provato una CLI `claude` vera con login reale, né il comportamento con `--bare` di default. Qui non c'è un binario `claude` autenticato e quel default è un rilascio futuro, non riproducibile oggi.

**Memoria del revisore**
- Ho scritto la riga contatore `#633-M2 … APPROVATO CON RISERVE … Nessuna lezione nuova` in `/home/user/Gas/.claude/agents/memoria_revisore.md`.
- `scripts/commit_memoria_revisore.sh` **non è partito**: l'hook `review_gate.sh` ha bloccato tutto il comando, perché `.claude/.review_ok` non corrisponde ancora al diff staged. La riga, che contiene anche lo SHA del diff, è stata scritta in un secondo comando senza lo script.
- Il file è modificato ma non in staging e non committato. Va committato dopo aver eseguito `bash scripts/segna_review_ok.sh`, oppure con `/fine-task`.
- Come richiesto, non ho committato nulla.

## §5 DELTA TEST DEL MOTORE

Test di `brains/claude_cli.py` e del doctor: `tests/test_unit_claude_cli.py` 29 → 42 test raccolti, `tests/test_unit_dotenv.py` 17 → 19 (in tutto 61 passed dopo la correzione di #632; conteggi con pytest --collect-only alla base b472fe1 e al commit). Kernel (`tests/test_unit_kernel.py`, che chiama il doctor): RIEPILOGO 1063 PASS, 0 FAIL (prima della correzione di #632, che tocca solo `stato_abbonamento` e i suoi test). Prova a mano: doctor con CLI finta che stampa una riga vuota → «[WARN ] Cervello forte login … non verificabile», nessun traceback.

## §6 STATO CI

`gh` non autenticato nel cloud: check run lette dall'integrazione GitHub.
- 26ecd7a, 2f5d53d: pushati insieme all'apertura della PR #321; run non ancora disponibile alla scrittura dell'handoff.
- Commit di fine-task che contiene questo file: run non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- **R-633-1-M2** BASSA: un processo nipote che tiene aperte le pipe può far durare oltre il timeout; attesa massima normale ~30 s (2 × 15 s).
- **R-633-2-M2** BASSA: `errors="replace"` senza un test dedicato (il ramo `except ValueError` lo copre comunque).
- Non verificato con una CLI `claude` vera e loggata: il campo `authMethod` viene dalla documentazione (cli-reference). Da provare sul Mac.
