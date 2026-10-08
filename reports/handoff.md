# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-10-08 — Bot di verifica: le riserve già registrate citate nel verdetto non bloccano (R-161-1)

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR di questa fetta (tocca la macchina del bot: il bot darà neutral, decide l'operatore).
2. Dopo il merge: aggiornare la PR #149 da main perché il bot la rigiudichi.

---

## §1 SCOPE & ESITO FETTE

- **Correzione falsi NO (R-161-1)**: `FATTA`.
- **R-205-1 / R-205-2**: `DEFERITE — riserve BASSE registrate`.
- **Verifica esterna §4quater**: `SALTATA — la fa il bot V-B (etichetta verifica); tocca la macchina del bot, merge all'operatore`.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   3 +++
 .github/workflows/verifica-bot.yml |   3 +++
 reports/diff_sessione.md           |  11 ++++++-----
 reports/handoff.md                 | 168 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++-------------------------------------------------------------------
 reports/stato_progetto.md          |   2 ++
 reports/ultimo_report.md           |  27 ++++++++++++++-------------
 scripts/bot_esito.py               |  13 +++++++++++--
 tests/test_unit_verifica_bot.py    |  44 ++++++++++++++++++++++++++++++++++++++++++++
 8 files changed, 184 insertions(+), 87 deletions(-)
```

## §3 GIT LOG --ONELINE (sessione)

```
6ed792f fix(verifica-bot): le riserve già registrate citate nel verdetto non bloccano — R-161-1 — review #205/#206
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione. Il suo hash è stampato al passo 5.

## §4 VERDETTO DEL REVISORE (per commit motore)

Verdetti INTEGRALI. Unica trasformazione meccanica: i path assoluti del worktree (`/home/user/wt-bot161/`) resi relativi alla radice del repo.

### Review #205 — prima versione (BOCCIATO)

## VERDETTO: BOCCIATO

La modifica va nella direzione giusta e funziona sui due casi reali della PR #149 (rifatto da me: entrambi i testi salvati danno ora {BASSA, COSMETICA}). Ma la frase su cui si regge, "tutto il resto della riga conta ancora", è vera solo per ALTA e MEDIA scritte in maiuscolo, cioè l'unico caso che i test provano. Ho trovato tre peggioramenti rispetto a HEAD, tutti rifatti con il vecchio `bot_esito.py` (da `git show HEAD:`) affiancato al nuovo. I 292 test passano.

**Elementi del diff esaminati**

1. `scripts/bot_esito.py:162` — sostituisce la citazione della riserva con la parola `"R-riserva"` prima di cercare le gravità.
   - **Rischio:** la sostituzione modifica anche le righe lette dalle altre due regex. `_FINDING_GRAVE_A_PAROLE` (`scripts/bot_esito.py:105`) e `_FINDING_GRAVITA` (`:97`) cercano un id con numero (`[VFRG]-\d+` e `[A-Za-z]+-\d+`). "R-riserva" non ha numero, quindi quelle regex non vedono più la riga.
   - **Esito: blocco.** Righe che prima davano {MEDIA, BASSA} e ora danno un insieme vuoto:
     - `R-203-1 (BASSA) questa PR introduce un bug grave`
     - `R-203-1 (BASSA) ma x è high`
     - `R-203-1 (BASSA) — critico`
     - `R-203-1 (BASSA) e poi x (alta) in questa PR`
   - Il test `tests/test_unit_verifica_bot.py:445` usa "ALTA" maiuscolo, che viene preso da `_PAROLA_BLOCCANTE` e non da queste regex: per questo non se ne accorge.

2. `scripts/bot_esito.py:155` — la regex `_RISERVA_REGISTRATA = r"\bR-\d+-\d+\b\s*\([^)\n]*\)"`.
   - **Rischio:** con parentesi una dentro l'altra, la regex mangia anche il contenuto della seconda.
   - **Esito: blocco.** `R-203-1 (BASSA, vedi anche V-2 (ALTA) nuovo bug)` dà {} (prima dava {ALTA, MEDIA, BASSA}). Un finding V- vero, scritto dentro la parentesi di una riserva, sparisce. Ho provato `[^()\n]*` e il caso torna {ALTA, MEDIA, BASSA}.

3. `.github/workflows/verifica-bot.yml:142-144` — nuova regola nel prompt del bot (la "R-203-1 (ALTA, preesistente)").
   - **Rischio:** il prompt e il codice potrebbero non coincidere.
   - **Esito: ok.** La forma richiesta dal prompt è quella tolta dalla regex. Riserva sotto: la regex non chiede la parola "preesistente" che il prompt invece impone.

4. `tests/test_unit_verifica_bot.py:441-462` — 5 casi che devono restare COMMENT, più il caso del campo strutturato.
   - **Esito: riserva.** Mancano proprio i casi che fanno fallire il codice: parole minuscole o inglesi fuori dalla parentesi, gravità tra parentesi dopo la citazione, parentesi annidate. Il test sul campo strutturato è giusto: il campo vince sul testo.

**Correzioni richieste (bloccanti)**
- **B-1:** usare un segnaposto con il numero, ad esempio `"R-0"`, così le regex `:97` e `:105` vedono ancora la riga. In alternativa, togliere solo il contenuto della parentesi e lasciare l'id.
- **B-2:** cambiare `[^)\n]*` in `[^()\n]*`.
- **B-3:** aggiungere ai casi COMMENT le quattro righe del punto 1 e quella del punto 2. Poi rifare la prova di mutazione (cioè rompere apposta il fix e controllare che i test falliscano) su ciascuna delle due correzioni.

**Riserve (non bloccanti, da registrare)**
- **R-205-1 (BASSA), forma ostile.** Oggi qualunque `R-n-n (...)` sparisce dal controllo sul testo, compreso un problema nuovo descritto tutto dentro la parentesi, per esempio `R-203-1 (ALTA, preesistente: questa PR toglie il controllo)`. Quanto si indebolisce la difesa secondaria: un contenuto ostile che riesce a far scrivere al modello un problema reale in quella forma riesce anche a farlo togliere dal campo "finding". Quindi la difesa principale cade comunque, e il margine perso è piccolo ma reale. Consiglio di esigere `preesistente` dentro la parentesi: costa poco, coincide con il prompt, ed evita che un finding del bot chiamato "R-…" per abitudine venga cancellato per sbaglio. Il commento a `:103-104` ammette infatti anche id R- per i finding.
- **R-205-2 (BASSA), controllo contro il repo.** Limitare la regola agli id presenti in `reports/stato_progetto.md` di main non lo consiglio come requisito. Un id esistente si può riusare (R-203-1 è pubblico), e il job dell'esito dovrebbe leggere un file di main in più. Il guadagno contro un attacco è circa zero; serve solo contro id inventati per errore.

**Cosa NON ho verificato**
- Il comportamento del modello reale nel workflow con il nuovo prompt: non lo posso riprodurre qui (serve una run di `verifica-bot` con il token del bot). Ho verificato solo la logica deterministica di `bot_esito.py` e i due testi salvati.
- La PR tocca la macchina del bot, quindi il bot darà neutral e il merge resta all'operatore.

La riga contatore #205 e una lezione nuova sono state aggiunte a `.claude/agents/memoria_revisore.md`, senza commit come richiesto. La numerazione salta #204 perché quella sta sul branch della PR #149.

File rilevanti:
- `scripts/bot_esito.py`
- `tests/test_unit_verifica_bot.py`
- `.github/workflows/verifica-bot.yml`
- `.claude/agents/memoria_revisore.md`

### Review #206 — dopo B-1/B-2/B-3

## VERDETTO: APPROVATO CON RISERVE

Le tre correzioni bloccanti di #205 sono a posto e le ho ricontrollate da me sul diff staged in `/home/user/wt-bot161`. I due verdetti reali della PR #149 danno ancora solo {BASSA, COSMETICA}: i due falsi NO non si ripetono.

**Elementi del diff esaminati**

1. `scripts/bot_esito.py:156` — la regex ora è `\b(R-\d+-\d+)\b\s*\([^()\n]*\)`: tiene l'id e non accetta parentesi una dentro l'altra.
   - **Rischio:** il problema di #205, cioè parentesi annidate che nascondono un finding V-.
   - **Esito: ok.** `R-203-1 (BASSA, vedi anche V-2 (ALTA) nuovo bug)` dà {ALTA, MEDIA, BASSA}. Rotto apposta (rimesso `[^)\n]*`) → 1 test fallisce. Ripristinato.

2. `scripts/bot_esito.py:163` — `sub(r"\1", ...)` toglie solo la parentesi e lascia l'id.
   - **Rischio:** il problema di #205, cioè le altre regex che non vedono più il resto della riga perché manca l'id.
   - **Esito: ok.** Le quattro righe di #205 tornano bloccanti: "grave" e "high" danno {MEDIA}, "critico" dà {MEDIA}, "(alta)" dà {ALTA, MEDIA}. Restano senza effetto, come previsto:
     - più citazioni sulla stessa riga;
     - `R-203-1(ALTA)` senza spazio;
     - `R-203-1 (ALTA, gate e compressione): resta prioritaria`.
   - Una seconda parentesi dopo la citazione conta ancora: `R-203-1 (ALTA) (MEDIA)` dà {MEDIA}. Rotto apposta (rimesso "R-riserva") → 4 test falliscono. Ripristinato. Il codice nel worktree è identico a quello staged.

3. `tests/test_unit_verifica_bot.py:451-455` — nuovi casi che devono restare COMMENT: inglese, minuscolo, "critico", parentesi annidate.
   - **Esito: ok.** Ora coprono ogni ramo del controllo, non più solo la parola maiuscola. Risultato: 297 passed.

**Riserve (da registrare in stato_progetto.md)**
- **R-205-1 (BASSA), resta aperta.** Una descrizione messa tutta dentro la parentesi di una riserva sparisce dal controllo sul testo, ad esempio `R-1-1 (ALTA, questa PR toglie il controllo)`. Contro questo caso resta solo il campo strutturato.
  - Accetto la motivazione per non chiedere la parola "preesistente": il secondo verdetto reale di #149 scrive "(ALTA, gate e compressione)" senza quella parola, quindi resterebbe un falso NO.
  - Il margine perso è piccolo: un contenuto ostile che riesce a far scrivere il problema in quella forma riesce anche a farlo togliere dal campo "finding".
- **R-205-2 (BASSA), dichiarata.** Non si controlla che l'id esista davvero nel repo. Il vantaggio contro un attacco è quasi nullo, perché un id vero come R-203-1 è pubblico e si può riusare.

**Cosa NON ho verificato**
- Come si comporta il modello reale con il nuovo prompt nella run di `verifica-bot`: non si può riprodurre qui. Ho verificato solo la logica di `bot_esito.py`, sui testi salvati e su casi costruiti a mano.

**Note**
- La PR tocca la macchina del bot: il bot darà neutral e il merge spetta all'operatore.
- La riga contatore #206 è in `.claude/agents/memoria_revisore.md`, sotto la #205 e la sua lezione, senza commit come richiesto.

File rilevanti:
- `scripts/bot_esito.py`
- `tests/test_unit_verifica_bot.py`
- `.github/workflows/verifica-bot.yml`
- `.claude/agents/memoria_revisore.md`

## §5 DELTA TEST DEL MOTORE

Nessuna modifica a gas.py/brains/modules.

```
python -m pytest -q tests/test_unit_verifica_bot.py → 297 passed
mutation B-1 (segnaposto senza numero) → 4 failed; mutation B-2 (parentesi annidate) → 1 failed
verdetti reali #149 (check run 112915110196, 112989655083) → _gravita_nel_testo = {BASSA, COSMETICA}
```

## §6 STATO CI

Run CI di questo branch: non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- **R-205-1** (BASSA): un problema descritto tutto dentro la parentesi di una citazione R-n-n sfugge al controllo sul testo.
- **R-205-2** (BASSA): l'id della riserva non è verificato contro il repo.
- **R-203-1**: aperta (cancello, compressione).
