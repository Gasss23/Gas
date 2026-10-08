# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-10-08 — R-203-1: la compressione della cronologia non decontamina più la finestra del cancello

---

## §0 DECISIONI UMANE RICHIESTE

1. PR di questa fetta: merge se il bot dà success, altrimenti decide l'operatore.
2. Prova di `gas rifletti` con un modello vero sul Mac (nel container non ci sono chiavi API).

---

## §1 SCOPE & ESITO FETTE

- **R-203-1**: `FATTA` (marcatore sul riepilogo + cancello fail-closed, T72g, design §3a).
- **Prova gas rifletti con modello reale**: `SALTATA — nessuna chiave API nel container cloud; la fa l'operatore sul Mac`.
- **Verifica esterna §4quater**: `SALTATA — la fa il bot V-B (etichetta verifica)`.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   3 +++
 gas.py                             |  29 +++++++++++++++++++++++------
 reports/design_cancello.md         |   2 +-
 reports/diff_sessione.md           |  18 ++++++------------
 reports/handoff.md                 | 341 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
 reports/stato_progetto.md          |   2 +-
 reports/ultimo_report.md           |  93 +++++++++++++++------------------------------------------------------------------------------
 tests/test_unit_kernel.py          |  83 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 8 files changed, 216 insertions(+), 355 deletions(-)
```

## §3 GIT LOG --ONELINE (sessione)

```
32dae5e fix(gate): la compressione della cronologia non decontamina più la finestra — R-203-1 — review #208/#209
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione. Il suo hash è stampato al passo 5.

## §4 VERDETTO DEL REVISORE (per commit motore)

Verdetti INTEGRALI. Unica trasformazione meccanica: i path assoluti del worktree (`/home/user/wt-r203/`) resi relativi alla radice del repo.

### Review #208 — diff iniziale

## VERDETTO: APPROVATO CON RISERVE

La modifica chiude R-203-1 (la compressione nascondeva il testo di terzi al cancello). Il codice è corretto e le mutation provano che i test fermano davvero il bug. Restano due riserve non bloccanti: un test che non verifica nulla e una frase sbagliata nel documento di design.

**Letture fatte:** CLAUDE.md sez. 5, la voce R-203-1 in `stato_progetto.md` (righe 15 e 146), la memoria del revisore fino alla #207.

### Punti del diff esaminati

1. `gas.py:790-794` — la compressione calcola `esterno` con `_finestra_e_contaminata(to_compress)` più i tool senza `name`, e mette il marcatore in fondo alla prima riga del riepilogo.
   - Rischio esaminato: un contenuto esterno che finisce sulla prima riga e falsifica il marcatore. Ogni messaggio compresso va sulle righe successive con il prefisso `[role] `, quindi nessun testo di terzi può iniziare la prima riga.
   - Il marcatore si propaga: il riepilogo precedente è un messaggio `user` che non finisce con SOLO INTERNO e viene ricontato.
   - Il calcolo sta dentro il `try` esistente e `str(... or "")` regge anche contenuti `None` o a lista, quindi non può crashare (§9).
   - **Esito: ok.**

2. `gas.py:1103-1109` — `_finestra_e_contaminata` ora conta anche i messaggi `user` con il prefisso del riepilogo che non finiscono con `[SOLO INTERNO]`.
   - Rischio esaminato: un marcatore falsificato. La regola è un OR: un `[SOLO INTERNO]` falso evita solo che *quel* messaggio contamini, cosa già vera per qualunque messaggio dell'operatore, e non pulisce gli altri. Se l'operatore scrive a mano prefisso più SOLO INTERNO non guadagna niente. Nessun canale esterno scrive messaggi `user`: Telegram accetta solo `TELEGRAM_ALLOWED_IDS`, e la notifica di `gas.py:1512` ha una prima riga fissa del kernel.
   - I riepiloghi vecchi senza marcatore contano come esterni (fail-closed), e va bene così.
   - **Esito: ok.**

3. Contesto, `gas.py:1866-1869` (`rifletti`, FASE 2.6) — considera non fidato ogni riepilogo, anche quelli SOLO INTERNO, guardando tutta la storia.
   - Rischio esaminato: incoerenza tra cancello e riflessione. È voluta e va nella direzione giusta: il recap viene salvato, quindi chiede più garanzie del cancello. Anche la differenza di insiemi è coerente: il cancello usa la lista dei tool non fidati, `rifletti` la lista di quelli fidati.
   - **Esito: ok.**

4. `tests/test_unit_kernel.py`, check T72g "un assistant che scrive il marcatore pulito non conta" — la lista contiene anche un `tool read_file`, che da solo basta a dare True. Il test quindi passa qualunque cosa succeda all'assistant.
   - Non c'è un caso con un messaggio `user` falsificato con `[SOLO INTERNO]` più un `read_file`.
   - Non è coperto il ramo "tool senza name" della compressione.
   - **Esito: riserva R-208-1.**

### Verifiche riprodotte

- **Test del kernel:** 697 PASS / 0 FAIL.
- **Mutation** (su una copia nello scratchpad, poi rimossa):
  - marcatore sempre pulito: 4 FAIL;
  - controllo `endswith` tolto: 2 FAIL (compressione solo interna e controprova del round-trip);
  - ramo `user` disattivato: 4 FAIL.
- **Round-trip §7:** T72g scrittura in attesa di approvazione dopo una compressione esterna, eseguita dopo una compressione interna. Arriva alla risposta finale in entrambi i casi.

### Autonomia

L'effetto è limitato. Con le impostazioni normali (10 messaggi nella finestra, 20 tenuti) il riepilogo resta fuori dalla finestra. Entra solo quando la parte recente è corta. I riepiloghi scritti prima di questa modifica contano come esterni finché restano nella finestra: è un costo accettabile e transitorio.

### Riserve

- **R-208-1 (BASSA, test):** rendere significativo il check T72g sull'assistant isolando il messaggio sotto prova. Aggiungere il caso `user` falsificato `[SOLO INTERNO]` più `read_file` (deve risultare contaminato) e il caso "tool senza name nella compressione" (deve dare INPUT ESTERNO).
- **R-208-2 (DOC):** `reports/design_cancello.md:137` dice ancora che il turno torna pulito "per scorrimento o per compressione della storia". Va corretto: la compressione mantiene la contaminazione finché il riepilogo marcato INPUT ESTERNO resta nella finestra. Meglio farlo in questa stessa PR.

### Cosa non ho verificato

- Il comportamento con una storia `.gas_history.json` reale di VPS: non è disponibile in dev, ho usato solo storie sintetiche.
- La suite gate+bot (371 passed): non l'ho rieseguita perché il diff non tocca `modules/gate` né `scripts/`.

La riga #208 e una lezione nuova sono state aggiunte, non committate come richiesto, in `.claude/agents/memoria_revisore.md`.

File rilevanti:
- `gas.py`
- `tests/test_unit_kernel.py`
- `reports/design_cancello.md`

### Review #209 — dopo R-208-1/2

## VERDETTO: APPROVATO

Le due riserve della review #208 sono chiuse: i test ora controllano davvero quello che dichiarano e il documento di design non dice più che la compressione pulisce la finestra. `gas.py` non è cambiato rispetto alla #208.

### Punti del diff esaminati

1. `tests/test_unit_kernel.py:5180` — il check sull'assistant ora usa solo un messaggio user "ciao" più un assistant col prefisso del riepilogo, senza nessun `read_file`.
   - Rischio esaminato: un test vacuo come in R-208-1. Ora risulta "non contaminata" solo perché i messaggi assistant non contano come riepilogo, quindi il test controlla davvero quella proprietà.
   - **Esito: ok.**

2. `tests/test_unit_kernel.py:5184` — un messaggio user con prefisso del riepilogo e `[SOLO INTERNO]`, nella stessa lista di un `read_file`, deve risultare contaminato.
   - Rischio esaminato: un marcatore falso che "lava" la finestra. Il test fissa che la regola resta un OR: il marcatore pulito non toglie la contaminazione portata da un altro messaggio.
   - **Esito: ok.**

3. `tests/test_unit_kernel.py:5192` — una compressione con un messaggio tool senza `name` deve produrre `[CONTIENE INPUT ESTERNO]`.
   - Rischio esaminato: un ramo del codice senza test. Ho disattivato il ramo "tool senza name" in `gas.py:790` su una copia nello scratchpad (poi rimossa): 698 PASS / 1 FAIL, e il FAIL è proprio questo check. Il ramo è quindi coperto.
   - **Esito: ok.**

4. `reports/design_cancello.md:137` — la frase sulla contaminazione dice ora che il turno torna pulito solo per scorrimento della finestra. Spiega anche che la compressione non decontamina, cita i due marcatori e la regola che anche un riepilogo vecchio senza marcatore conta come esterno.
   - Rischio esaminato: un documento che contraddice il codice. È ora allineato a `gas.py:1103-1109`.
   - **Esito: ok.**

### Verifiche riprodotte

- **Test del kernel:** 699 PASS / 0 FAIL.

### Cosa non ho verificato

- Non ho rieseguito la suite gate+bot né le mutation della #208. `gas.py` è identico a quello revisionato nella #208 (stessa statistica, 29 righe) e il nuovo diff tocca solo test e documento.
- Il comportamento su VPS con una storia reale resta non verificato, come nella #208: in sviluppo non è riproducibile.

Ho aggiunto la riga #209 in `.claude/agents/memoria_revisore.md`, senza commit come richiesto.

File rilevanti:
- `tests/test_unit_kernel.py`
- `reports/design_cancello.md`
- `gas.py`

## §5 DELTA TEST DEL MOTORE

```
python tests/test_unit_kernel.py → 699 PASS, 0 FAIL (main locale 689)
mutation: ramo user disattivato → 4 FAIL; tool senza name → 1 FAIL; marcatore sempre pulito → 4 FAIL (revisore)
python -m pytest tests/test_unit_gate.py tests/test_unit_verifica_bot.py → 371 passed
```

## §6 STATO CI

Run CI di questo branch: non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- Nessuna riserva nuova aperta (R-208-1/2 chiuse nella stessa PR).
- Note: i riepiloghi scritti prima di questa regola contano come esterni finché restano nella finestra (fail-closed, transitorio).
