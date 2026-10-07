# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-10-07 — Bot di verifica: socat e ripgrep nel sandbox (terza prova reale, PR #142)

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #145 (https://github.com/Gasss23/Gas/pull/145). Numero e URL dall'output del connettore GitHub (`create_pull_request` → `{"id":"4771857391","url":"https://github.com/Gasss23/Gas/pull/145"}`). Tocca la macchina del bot: merge dell'operatore.
2. R-196-3: per rigiudicare #142 serve un commit nuovo su #142 (NO legato allo SHA).
3. R-196-1 (MEDIA): decidere se farla subito, prima di rendere `verifica-bot` obbligatorio nel ruleset (§F).

---

## §1 SCOPE & ESITO FETTE

- **Merge #144 (diagnosi)**: `FATTA` su richiesta dell'operatore. La diagnosi ha mostrato il token con un a capo.
- **Terza prova reale su #142**: `FATTA` — il bot risponde (Opus 5.5), Bash rotta per socat mancante.
- **Fix socat + ripgrep**: `FATTA` (PR #145).
- **R-196-1**: `NON FATTA — fetta separata, decisione dell'operatore`.
- **Verifica esterna §4quater**: `SALTATA — la prova reale è il rilancio del bot su #142 dopo il merge`.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   3 +++
 .github/workflows/verifica-bot.yml |  12 +++++++++++-
 reports/diff_sessione.md           |  10 +++++-----
 reports/handoff.md                 | 147 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++--------------------------------------------------------------------------------
 reports/stato_progetto.md          |   2 ++
 reports/ultimo_report.md           |  26 ++++++++++++++------------
 tests/test_unit_verifica_bot.py    |   3 +++
 7 files changed, 105 insertions(+), 98 deletions(-)
```

## §3 GIT LOG --ONELINE (sessione)

```
5397348 fix(verifica-bot): socat e ripgrep nel sandbox — senza, la Bash del bot non parte — review #196/#197
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione. Il suo hash è stampato al passo 5.

## §4 VERDETTO DEL REVISORE (per commit motore)

Verdetti INTEGRALI. Unica trasformazione meccanica: i path assoluti dei checkout (`/home/user/wt-socat/`, `/home/user/Gas/`) resi relativi alla radice del repo. La memoria #196 era stata committata dal revisore nel checkout sbagliato (HEAD staccato, mai pushato): commit locale annullato e righe spostate in questo branch.

### Review #196 — diff iniziale

## VERDETTO: APPROVATO CON RISERVE

La modifica corregge la causa concreta della terza prova (#142): nel runner mancava socat, quindi la Bash del bot non partiva. Lo fa con la stessa regola già usata per bubblewrap: se il sandbox non è completo, il job si ferma. Resta aperto un problema più generale: quando gli strumenti si rompono, il bot dà comunque un verdetto nel merito.

**Elementi del diff esaminati**

1. `.github/workflows/verifica-bot.yml:166` — `apt-get install -y bubblewrap socat`.
   - Rischio esaminato: socat serve davvero? E basta da solo? Ho guardato il controllo delle dipendenze nel binario locale di Claude Code (`/opt/claude-code/bin/claude`). Su Linux il sandbox richiede tre cose: `bwrap`, `socat` e `ripgrep (rg)`. Seccomp mancante dà solo un avviso. Esiste anche un controllo su euid 0, che non riguarda il runner perché lì non si gira come root.
   - L'errore di #142 era "Sandbox dependencies not available: socat not installed". Gli errori vengono uniti in un unico messaggio, quindi rg e bwrap erano già trovati e socat era l'unico pezzo mancante.
   - Sicurezza: socat fa da proxy di rete al sandbox di Claude Code e il modello non lo può lanciare. `STRUMENTI` (righe 114-116) non cambia: solo Read/Grep/Glob su `./**` e i sottocomandi `gh` in sola lettura.
   - Esito: **ok**.
2. `.github/workflows/verifica-bot.yml:167-170` — se `command -v socat` fallisce, il job esce con 1.
   - Rischio esaminato: m2/m3 partono comunque? No. Restano legati a `steps.sandbox.outcome == 'success'` (righe 203 e 219, R-192-1). Lo step non ha `continue-on-error`.
   - Con la shell `bash -e` di GitHub, se apt-get fallisce il job si ferma già prima: questo controllo è un doppio blocco, utile se un giorno l'installazione cambia.
   - Esito: **ok**.
3. `tests/test_unit_verifica_bot.py:895-897` — controlla che nel testo ci siano l'installazione con socat e `command -v socat`.
   - Rischio esaminato: il test verifica solo stringhe, non che socat funzioni davvero sul runner. È coerente con gli altri test del workflow, e la prova reale resta la prossima esecuzione del bot. `git diff --cached --check` è pulito. Ho rilanciato la suite: 270 passed.
   - Esito: **ok**.

**Riserve**

- **R-196-1 (MEDIA, problema della macchina, da tracciare in `stato_progetto.md`)**: un verdetto alla cieca viene trattato come verdetto nel merito.
  - Il PROMPT (da riga 117) non dice cosa fare se `gh pr diff`/`gh pr checks` o la Bash falliscono. A #142 il bot ha giudicato senza vedere il diff e ha emesso un finding MEDIA sbagliato. Risultato: COMMENT → failure, cioè NO definitivo su quello SHA.
  - Nel verso opposto il rischio è peggiore: con strumenti rotti il bot potrebbe dare APPROVATO senza aver visto il diff.
  - Correzione proposta: il PROMPT deve dire che, se non si riesce a leggere diff e CI, la verifica è "non conclusa". Meglio ancora un campo dello schema (es. `strumenti_ok: false`) che `bot_esito.py` traduca in RIPROVA (check cancelled), mai in COMMENT o APPROVE.
  - Questo diff chiude la causa di #142, non questa categoria di problemi.
- **R-196-2 (BASSA)**: rg oggi viene trovato, ma non è installato in modo esplicito né controllato come socat. Se l'immagine del runner o il ripgrep incluso in Claude Code cambiano, si ripete lo stesso guasto. Rinforzo poco costoso: `apt-get install -y bubblewrap socat ripgrep` più `command -v rg`.
- **R-196-3 (operativa)**: il NO su #142 è registrato come definitivo su quello SHA. Dopo il merge di questo fix serve un nuovo commit su #142 (o un rilancio esplicito) perché il bot rigiudichi. Il finding V-1 di quel verdetto è un falso positivo e va annotato come tale, non chiuso nel merito.

**Rischi esplicitamente esclusi**

- Non ho verificato che sul runner ubuntu-24.04 la Bash del sandbox ora parta davvero, né che non manchino altre dipendenze a runtime (es. permessi di socat dentro bwrap con `--unshare-all`). Non si può riprodurre qui: lo dirà solo la prossima esecuzione reale del bot.
- Non ho verificato perché Fable 5.1 sia fallito: il motivo non è nei log, perché la diagnosi #144 parte solo se nessun modello risponde.

**Memoria**

Ho aggiunto in coda a `.claude/agents/memoria_revisore.md` la riga #196 e una lezione nuova, committate con `bash scripts/commit_memoria_revisore.sh` (commit `0a89644`). La lezione: con strumenti guasti l'esito deve essere RIPROVA, mai un verdetto nel merito; e il controllo nel job deve provare le stesse dipendenze che controlla lo strumento.

Su questo checkout l'ultima riga della memoria era #191. Ho usato #196 come mi hai indicato, perché le review #192-#195 risultano su altri branch: lo conferma il riferimento a R-192-1 nel workflow. Quando i branch si uniranno, controlla che i numeri non si dupliciscano.

File rilevanti:
- `.github/workflows/verifica-bot.yml`
- `tests/test_unit_verifica_bot.py`
- `.claude/agents/memoria_revisore.md`

### Review #197 — dopo R-196-2

## VERDETTO: APPROVATO CON RISERVE

Hai ragione sulla nota (1): avevo committato la memoria nel checkout sbagliato. D'ora in poi lavoro solo in `/home/user/wt-socat`. Ho aggiunto la riga #197 alla memoria lì, senza committare. Nella revisione di conferma la correzione per rg (R-196-2) funziona; resta aperta solo R-196-1, già tracciata come fetta separata.

**Elementi del diff esaminati**

1. `.github/workflows/verifica-bot.yml:166-173` — installa `bubblewrap socat ripgrep`, poi controlla con `command -v` che socat e rg ci siano.
   - Rischio esaminato: il controllo si ferma davvero se manca una delle due? Ho estratto il ciclo e l'ho eseguito con `bash -e` (come la shell degli step) e un PATH ridotto a mano:
     - senza socat: `DIPENDENZA_FAIL: socat assente`, rc=1;
     - senza rg: `DIPENDENZA_FAIL: rg assente`, rc=1;
     - con entrambi: OK, rc=0.
   - Le dipendenze controllate sono quelle che il binario di Claude Code richiede su Linux: bwrap viene già provato più sotto dalla prova reale (`BWRAP_OK`/`BWRAP_FAIL`), socat e rg da questo ciclo.
   - Lo step tiene `id: sandbox` e non ha `continue-on-error`, quindi m2/m3 restano bloccati (R-192-1).
   - Esito: **ok**.
2. `tests/test_unit_verifica_bot.py:896-897` — controlla che nel testo ci siano l'installazione con ripgrep e il ciclo `for dip in socat rg; do` con `command -v "$dip"`.
   - Rischio esaminato: il test guarda solo il testo e non prova che il ciclo esca con 1. Il comportamento l'ho provato io a mano, come descritto sopra. 270 passed (rilanciati), `git diff --cached --check` pulito.
   - Esito: **ok**.

**Riserve**

- R-196-1 (MEDIA) resta aperta: il bot, se gli strumenti sono rotti, giudica alla cieca invece di dare "verifica non conclusa". È fuori da questo diff ed è tracciata come fetta separata. La riserva vale finché quella fetta non arriva.
- Cosmetica: il commento in `.github/workflows/verifica-bot.yml:159-161` parla solo di socat; la riga `:167` già cita rg, quindi è innocuo.

**Rischi esplicitamente esclusi**

- Non ho verificato che il pacchetto `ripgrep` si installi sul runner ubuntu-24.04: è nel repository universe, attivo sulle immagini GitHub, ma qui non si può riprodurre.
- Non ho verificato che il sandbox usi il rg di sistema invece di quello incluso in Claude Code. In entrambi i casi il controllo è solo un doppio blocco e non fa danni.
- La prova vera resta la prossima esecuzione del bot.

**Memoria**

Ho aggiunto la riga #197 in coda a `.claude/agents/memoria_revisore.md`, dopo le righe #196 che hai spostato tu. Non ho committato, come richiesto. Nessuna lezione nuova.

File rilevanti:
- `.github/workflows/verifica-bot.yml`
- `tests/test_unit_verifica_bot.py`
- `.claude/agents/memoria_revisore.md`

## §5 DELTA TEST DEL MOTORE

Nessuna modifica a gas.py/brains/modules.

```
python -m pytest -q tests/test_unit_verifica_bot.py → 270 passed
```

## §6 STATO CI

Run del bot su #142 dopo il token su una riga (check run 112764210917): sandbox success; Fable 5.1 fallito (motivo non visibile); Opus 5.5 verdetto APPROVATO CON RISERVE con V-1 MEDIA (falso positivo: Bash rotta per socat mancante) → check failure. Run precedente (37609672716): DIAGNOSI "Invalid Authorization header value from CLAUDE_CODE_OAUTH_TOKEN: it contains a line break at character 100". Run CI di questo branch: non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- **R-196-1** (MEDIA, aperta): con strumenti rotti il bot dà un verdetto nel merito invece di RIPROVA.
- **R-196-3**: nuovo commit su #142 per rigiudicare.
- **R-194-3** (cosmetica), **R-193-1** (BASSA), **R-193-2** (cosmetica): aperte.
- Fable 5.1: motivo del fallimento da capire.
