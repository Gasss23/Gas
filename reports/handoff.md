# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-10-07 — Bot di verifica convalidato (quarta prova su #142) + R-196-1: niente verdetti alla cieca

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #146 (https://github.com/Gasss23/Gas/pull/146). Numero e URL dall'output del connettore GitHub (`create_pull_request` → `{"id":"4772148262","url":"https://github.com/Gasss23/Gas/pull/146"}`). Tocca la macchina del bot: merge dell'operatore.
2. Setup §F: check `verifica-bot` (sorgente App gas-verificatore) obbligatorio nel ruleset main-lock.

---

## §1 SCOPE & ESITO FETTE

- **Merge #145 (socat + ripgrep)**: `FATTA` su richiesta dell'operatore, CI verde.
- **Quarta prova reale su #142**: `FATTA` — verdetto corretto, check success: bot convalidato.
- **Chiusura #142**: `FATTA` su richiesta dell'operatore (senza merge).
- **R-196-1**: `FATTA` (PR #146).
- **Verifica esterna §4quater**: `SALTATA — la prossima PR fuori dalla macchina del bot sarà verificata dal bot stesso; questa tocca la macchina (decide l'operatore)`.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   2 ++
 .github/workflows/verifica-bot.yml |   7 ++++++-
 reports/diff_sessione.md           |  12 +++++++-----
 reports/handoff.md                 | 137 ++++++++++++++++++++++++++++++++++++++++++++++-------------------------------------------------------------------------------------------
 reports/setup_verifica_bot.md      |   3 ++-
 reports/stato_progetto.md          |   2 ++
 reports/ultimo_report.md           |  26 ++++++++++++--------------
 scripts/bot_esito.py               |   8 +++++++-
 tests/test_unit_verifica_bot.py    |  44 ++++++++++++++++++++++++++++++++++++--------
 9 files changed, 120 insertions(+), 121 deletions(-)
```

## §3 GIT LOG --ONELINE (sessione)

```
f5928b4 fix(verifica-bot): niente verdetti alla cieca — strumenti_ok nello schema, senza diff e CI letti RIPROVA — review #198
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione. Il suo hash è stampato al passo 5.

## §4 VERDETTO DEL REVISORE (per commit motore)

Verdetto INTEGRALE. Unica trasformazione meccanica: i path assoluti del worktree (`/home/user/wt-strum/`) resi relativi alla radice del repo.

### Review #198 — diff R-196-1

## VERDETTO: APPROVATO CON RISERVE

**In breve:** la modifica chiude il caso reale della PR #142. Se il bot dice di non aver letto diff e CI, il check finisce `cancelled` e si rilancia: niente più NO definitivi dati alla cieca, e nessuna nuova strada verso un `success`. Resta un limite: il campo `strumenti_ok` lo dichiara il modello stesso, quindi un modello che crede di aver letto (o mente) non viene fermato.

**Elementi del diff esaminati**

1. `scripts/bot_esito.py:243`
   - **Cosa fa:** `if verdetto.get("strumenti_ok") is not True` → RIPROVA. Sta dopo `isinstance(verdetto, dict)` e prima della validazione strutturale.
   - **Rischio esaminato:** valori "quasi veri" (`"true"`, `1`, `"si"`), campo assente, effetto sulla macchina del bot, effetto sul doc-only.
   - **Riprova:** 283 passed. Mutation `is False` → 9 failed. Controllo tolto → 12 failed. File ripristinato, staged intatto.
   - **Percorsi a valle:**
     - `decidi()` trasforma in OPERATORE solo un `APPROVE`, quindi RIPROVA resta RIPROVA.
     - `con_storico()` lascia passare gli eventi diversi da APPROVE/OPERATORE.
     - Il doc-only resta prima e non è toccato.
   - **Esito:** ok.

2. `.github/workflows/verifica-bot.yml:105` e `:107`
   - **Cosa fa:** `strumenti_ok` diventa un campo obbligatorio di tipo booleano nello schema. Il PROMPT (`:133-136`) chiede `true` solo se il bot ha letto davvero sia `gh pr diff` sia `gh pr checks`.
   - **Rischio esaminato:** una risposta senza il campo, o con un valore stringa, passerebbe come `success`?
   - **Esito:** ok. Col campo obbligatorio un output valido lo contiene sempre. Se manca comunque, il codice lo tratta come non-True e dà RIPROVA (difesa doppia). Il test a `tests/test_unit_verifica_bot.py:978-982` controlla schema e prompt.

3. `tests/test_unit_verifica_bot.py:81`
   - **Cosa fa:** il caso `{}` diventa `{"strumenti_ok": True}`.
   - **Rischio esaminato:** si perde copertura?
   - **Esito:** ok. Il `{}` vero ora finisce in RIPROVA ed è coperto da `test_strumenti_assente_si_riprova`. Il caso "struttura incompleta → COMMENT" resta coperto con strumenti dichiarati ok. Con lo schema obbligatorio, `{}` non può uscire da un output valido. Considerarlo "non concluso" è coerente.

**Le tue domande**

- **Ordine dei controlli (strumenti prima della struttura).** L'indebolimento è accettabile. Un verdetto incompleto con `strumenti_ok` false passa da `failure` a `cancelled`. Né `cancelled` né `failure` sono `success`: il check richiesto dal ruleset blocca il merge in entrambi i casi. Si perde solo la regola "il NO è definitivo su quello SHA" (G-2), per un verdetto dato alla cieca, quindi senza valore.
- **PR malevola che fa dire `false` al modello per evitare un NO.** Ottiene solo un altro tentativo. Lo stesso risultato lo ottiene già oggi facendo produrre un output malformato (verdetto assente → RIPROVA), quindi non è una capacità nuova. Per arrivare al merge serve comunque un `success` vero in un'altra run. In più `componi_corpo` (`scripts/bot_esito.py:305-310`) pubblica il testo del verdetto anche con RIPROVA: un NO mascherato resta visibile all'operatore. Il filtro credenziali scatta per ogni esito.
- **Coerenza col protocollo.** `.claude/verifica_esterna.md` non va toccato: lo cambia solo l'operatore, e la clausola è un dettaglio dell'esecuzione automatica, non del metodo. Va bene che stia nel PROMPT.

**Riserve**

- **R-198-1 (BASSA): `strumenti_ok` lo dichiara il modello stesso.** Un modello che crede di aver letto diff e CI, o che mente, mette `true` e si torna esattamente al caso di #142. Il problema è ridotto, non chiuso. Rimedio possibile in una fetta futura: controllare nel file di esecuzione del modello (`execution_file`) che le chiamate `gh pr diff` e `gh pr checks` ci siano davvero e non siano fallite.
- **R-198-2 (COSMETICA): documentazione di `cancelled` incompleta.** `reports/setup_verifica_bot.md:69` elenca i casi di `cancelled` senza "strumenti non disponibili". La docstring a `scripts/bot_esito.py:21` invece è aggiornata. Basta aggiungere il caso a quella riga.

**Cosa non ho verificato:** il comportamento reale del bot su GitHub Actions, cioè se il modello compila `strumenti_ok` con onestà quando Bash o `gh` non funzionano, e se l'azione impone davvero lo schema col nuovo campo obbligatorio. Si vede solo da una run vera, e non si può riprodurre in locale senza i segreti dell'App.

**Memoria:** ho aggiunto la riga #198 e una lezione in `.claude/agents/memoria_revisore.md`. Non ho fatto commit, come richiesto. Il worktree contiene solo questa modifica non in staging, più i tre file già in staging, che sono intatti.

**File rilevanti:**
- `scripts/bot_esito.py`
- `.github/workflows/verifica-bot.yml`
- `tests/test_unit_verifica_bot.py`
- `reports/setup_verifica_bot.md`
- `.claude/agents/memoria_revisore.md`

## §5 DELTA TEST DEL MOTORE

Nessuna modifica a gas.py/brains/modules.

```
python -m pytest -q tests/test_unit_verifica_bot.py → 283 passed
mutation: controllo tolto → 12 failed; `is False` al posto di `is not True` → 9 failed
```

## §6 STATO CI

Bot su #142 dopo #145 (run 37615670460, head ab1093b): gh pr view/diff/checks usati; verdetto APPROVATO CON RISERVE (V-1 BASSA, V-2 COSMETICA), check verifica-bot success, modello claude-opus-5-5 (Fable 5.1 fallito). Run CI di questo branch: non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- **R-198-1** (BASSA): strumenti_ok autodichiarato dal modello.
- **R-194-3** (cosmetica), **R-193-1** (BASSA), **R-193-2** (cosmetica): aperte.
- Fable 5.1 fallisce sempre: motivo da capire.
