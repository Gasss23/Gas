# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-10-07 — R-200-2: run_command conta come input esterno nel cancello

---

## §0 DECISIONI UMANE RICHIESTE

1. PR di questa fetta: merge se il bot dà success (gasmerge --auto equivalente), altrimenti decide l'operatore.
2. R-203-1 (ALTA, preesistente): compressione della cronologia che decontamina — fetta propria del cancello prima dell'autonomia.
3. R-203-2 (decisione umana): dopo un run_command in sandbox, le azioni successive restano in approvazione?

---

## §1 SCOPE & ESITO FETTE

- **R-200-2**: `FATTA` (run_command in UNTRUSTED_INPUT_TOOLS + T72d/e/f, T78e invertito).
- **R-203-1**: `NON FATTA — fetta propria`.
- **Verifica esterna §4quater**: `SALTATA — la verifica esterna la fa il bot V-B sulla PR (etichetta verifica)`.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   2 ++
 modules/gate/gate.py               |   4 +++-
 reports/diff_sessione.md           |  12 +++++-------
 reports/handoff.md                 | 132 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++-----------------------------------------------------------------------
 reports/stato_progetto.md          |   2 ++
 reports/ultimo_report.md           |  35 ++++++++++++++++-------------------
 tests/test_unit_kernel.py          |  46 ++++++++++++++++++++++++++++++++++++++++++++--
 7 files changed, 133 insertions(+), 100 deletions(-)
```

## §3 GIT LOG --ONELINE (sessione)

```
697c770 fix(gate): run_command contamina la finestra come read_file — R-200-2 — review #203
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione. Il suo hash è stampato al passo 5.

## §4 VERDETTO DEL REVISORE (per commit motore)

Verdetto INTEGRALE. Unica trasformazione meccanica: i path assoluti del worktree (`/home/user/wt-r200/`) resi relativi alla radice del repo.

### Review #203 — diff R-200-2

## VERDETTO: APPROVATO CON RISERVE

**In breve:** la correzione funziona e chiude R-200-2. Ho rifatto io le prove: la suite del kernel dà 658 PASS. Ho poi tolto `run_command` dalla lista dei tool che contaminano: falliscono esattamente 4 controlli (T72d, T72e, T72f, T78e). Ho rimesso il file com'era. Il cambio di T78e è corretto. Ci sono due riserve, nessuna blocca il commit. La più importante è un buco preesistente nella compressione della cronologia (R-203-1).

**Elementi del diff esaminati**

1. `modules/gate/gate.py:70` — aggiunge `"run_command"` a `UNTRUSTED_INPUT_TOOLS`.
   - Rischio esaminato: la finestra resta "pulita" anche quando contiene contenuti di file letti con cat/grep/head/tail/ls.
   - Anche l'output di `ls` è testo che un terzo può manipolare: un nome di file può contenere un'istruzione nascosta. Quindi è giusto includere tutto il comando, non solo cat/grep.
   - Gli output di errore (comando rifiutato, sandbox assente, dry-run) contano anch'essi come contaminanti. È prudente: nel dubbio si blocca, mai il contrario.
   - Esito: **ok**.

2. `tests/test_unit_kernel.py` T72f (verso :5103-5133) — giro agentico completo con `GAS_SANDBOX_MODE=os_strict`.
   - Il ricalcolo della contaminazione a ogni iterazione (`gas.py:2119`) fa sì che la `write_file` dell'iterazione 2 veda l'output del `run_command` dell'iterazione 1.
   - Il test controlla tre cose: il file NON viene creato, la controprova senza `ls` lo crea, il ciclo arriva alla risposta finale.
   - Con la mutazione l'output era `['reports\n', 'Successo: File r200.txt aggiornato.']`, cioè il buco riprodotto in modo concreto.
   - Esito: **ok**.

3. `tests/test_unit_kernel.py` T78e (verso :6467-6470) — il controllo invertito.
   - Ho verificato che la finestra di `_k78` contiene SOLO il `run_command` firmato (`tests/test_unit_kernel.py:6390`) e il `calcola` di T78b. Il controllo prova davvero `run_command`, non un `read_file` capitato lì per caso.
   - Il vecchio controllo ("NON contaminata, come nel loop") era il buco messo per iscritto nei test. Invertirlo è legittimo.
   - Esito: **ok**.

4. Contesto: `gas.py:938-944` `_finestra_e_contaminata`, `gas.py:545-551` elenco dei tool.
   - `write_file` restituisce solo una conferma; `salva_contatto` e `imposta_stato_contatto` restituiscono ciò che il modello ha appena scritto; `calcola` dà numeri.
   - Nessun altro tool di oggi porta dentro input esterno.
   - Esito: **ok**.

**Riserve (da tracciare in `stato_progetto.md`)**

- **R-203-1 (ALTA, preesistente, riguarda il cancello)** — `gas.py:648-658`.
  - Quando la cronologia viene compressa, l'output dei tool (anche `read_file`, `run_command`, `ricorda`) viene copiato come `"[tool] content[:300]"` dentro un messaggio con **ruolo user**.
  - Il messaggio originale del tool sparisce, quindi `_finestra_e_contaminata` torna False. Ma fino a 300 caratteri di testo di terzi restano visibili al modello, e per di più con l'autorità di un messaggio dell'utente.
  - `reports/design_cancello.md:137` tratta la compressione come una decontaminazione: è sbagliato.
  - Possibili correzioni: escludere gli output dei tool contaminanti dal riassunto, oppure considerare contaminato un riassunto che li contiene.
  - Non blocca questa PR: il buco c'era già prima e non nasce da questo diff. Va però aperto come fetta del cancello prima che Gas lavori in autonomia.

- **R-203-2 (MEDIA, autonomia)** — in modalità `os_strict` lo stesso `run_command` è UNCERTAIN.
  - Ora anche il **secondo** `run_command` della finestra va in approvazione. Un'esplorazione tipo `ls` e poi `cat` non è più autonoma, e lo stesso vale per `write_file`, `salva_contatto` e `imposta_stato_contatto` finché l'output resta nella finestra (anche per più turni).
  - È coerente con il comportamento già in vigore per `read_file`, quindi è accettabile.
  - Va però detto all'operatore. In futuro si può decidere se un `run_command` in sandbox (sola lettura, senza rete) debba andare in approvazione anche con la finestra contaminata: è una decisione umana.

**Rischi NON verificati**
- Non ho verificato come si comporta su un VPS reale con bwrap in esecuzione per più turni, né il click di approvazione reale su Telegram: non si possono riprodurre in sviluppo. T72f regge anche senza bwrap, perché anche un errore conta come contaminante.
- Non ho rieseguito la suite verifica_bot (283): i file che il diff tocca non la riguardano.
- Il pin di memoria (`_memoria_pin`) inietta testo di terzi nel messaggio di sistema. Non l'ho rivalutato: è già tracciato come fetta C-pin (`design_cancello.md:150`).

**Memoria del revisore**
Ho aggiunto in coda a `.claude/agents/memoria_revisore.md` la riga contatore #203 più una lezione: ogni trasformazione della cronologia che sposta del contenuto (compressione, riassunti) può far perdere traccia della sua provenienza. Come richiesto, il file NON è committato. I file staged (`modules/gate/gate.py`, `tests/test_unit_kernel.py`) non sono stati modificati.

## §5 DELTA TEST DEL MOTORE

```
python tests/test_unit_kernel.py → 658 PASS, 0 FAIL (main locale 655)
senza il fix (run_command tolto dal set) → 654 PASS, 4 FAIL (T72d, T72e, T72f, T78e)
python -m pytest tests/test_unit_gate.py tests/test_unit_verifica_bot.py → 357 passed
```

## §6 STATO CI

Run CI di questo branch: non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- **R-203-1** (ALTA, preesistente): compressione della cronologia decontamina.
- **R-203-2** (MEDIA, decisione umana): autonomia ridotta dopo run_command.
