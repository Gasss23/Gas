# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-10-07 — Bot di verifica: bubblewrap prima di Claude (prima prova reale, PR #142)

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #143 (https://github.com/Gasss23/Gas/pull/143). Numero e URL dall'output del connettore GitHub (`create_pull_request` → `{"id":"4770933069","url":"https://github.com/Gasss23/Gas/pull/143"}`). Tocca la macchina del bot: merge dell'operatore.
2. Dopo il merge: rilanciare la verifica su #142.

---

## §1 SCOPE & ESITO FETTE

- **Prova reale del bot su #142**: `FATTA` — App OK, modelli non partiti (bubblewrap mancante).
- **Fix bubblewrap + m2/m3 legati al sandbox**: `FATTA`.
- **Verifica esterna §4quater**: `SALTATA — la prova reale è il rilancio del bot su #142 dopo il merge (decide l'operatore se lanciarla prima)`.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   3 +++
 .github/workflows/verifica-bot.yml |  29 +++++++++++++++++++++++++++--
 reports/diff_sessione.md           |  11 +++++------
 reports/handoff.md                 | 192 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++---------------------------------------------------------------------------------------------------------------
 reports/stato_progetto.md          |   2 ++
 reports/ultimo_report.md           |  39 +++++++++++++++------------------------
 tests/test_unit_verifica_bot.py    |  20 ++++++++++++++++++++
 7 files changed, 153 insertions(+), 143 deletions(-)
```

## §3 GIT LOG --ONELINE (sessione)

```
d73033f fix(verifica-bot): installa bubblewrap prima di Claude — lo scrub dei segreti lo esige — review #192/#193
b2c92ad chore(revisore): memoria review #193 — APPROVATO CON RISERVE
15670fd chore(revisore): memoria review #192 — APPROVATO CON RISERVE
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione. Il suo hash è stampato al passo 5.

## §4 VERDETTO DEL REVISORE (per commit motore)

Verdetti INTEGRALI. Unica trasformazione meccanica: i path assoluti del worktree (`/home/user/wt-bwrap/`) resi relativi alla radice del repo.

### Review #192 — diff iniziale

## VERDETTO: APPROVATO CON RISERVE

**In breve:** la correzione va nella direzione giusta. Installa bubblewrap (il programma che isola i sottoprocessi) invece di spegnere la pulizia dei segreti, e ferma il job se l'isolamento non parte. Restano due problemi minori: se lo step fallisce, i modelli di riserva partono lo stesso, e il messaggio finale dà la colpa ai modelli invece che all'isolamento.

**Elementi del diff esaminati**

1. `.github/workflows/verifica-bot.yml:158` — nuovo step "Sandbox per lo scrub dei segreti (bubblewrap)", posto dopo i due checkout e prima di m1 (Fable 5.1).
   - Rischi esaminati: ordine degli step, esecuzione di codice della PR, segreti presenti nello step.
   - Esito: **ok**. Lo step non esegue nulla della PR. Nel suo ambiente c'è solo `GH_TOKEN` (il token di sola lettura del job). `CLAUDE_CODE_OAUTH_TOKEN` arriva soltanto nel `with:` di m1/m2/m3. Con la shell predefinita `bash -e`, anche un errore di `apt-get update` o `install` ferma lo step (blocco in caso di errore). Lo scrub resta `"1"` alla riga 102: la protezione non viene indebolita.

2. `.github/workflows/verifica-bot.yml:164-165` — rilassa i sysctl degli user namespace (la restrizione che Ubuntu 24.04 applica via AppArmor), con lo stesso codice dello step "Enable OS sandbox" di `ci.yml`. Questo risponde alla tua domanda (2).
   - Rischio esaminato: una superficie del kernel più ampia su un runner che ha segreti nell'environment.
   - Esito: **ok**. Il runner è usa e getta. Gli unici processi locali sono Claude con Read/Grep/Glob limitati a `./**` e un Bash ristretto ai comandi `gh` di lettura. Il rilassamento è proprio ciò che serve per accendere l'isolamento che riduce il rischio. Non tocca la VPS né `GAS_SANDBOX_MODE`.

3. `.github/workflows/verifica-bot.yml:170-175` — prova minima (`bwrap --unshare-all --ro-bind / / /bin/true`), poi `BWRAP_FAIL` e `exit 1`, senza continue-on-error. Questo risponde alle domande (1) e (3).
   - Esito: **riserva R-192-1**.
   - Domanda (3): `--unshare-all` crea tutti i tipi di namespace, quindi copre almeno quelli che servono a Claude Code. Le opzioni esatte di Claude Code (es. `--proc` in un nuovo namespace dei processi) non le ho verificate, quindi la prova è necessaria ma non dimostrata sufficiente. Lo dirà solo la run reale.
   - Domanda (1), ho tracciato il percorso. Se lo step fallisce, m1 viene saltato (senza `if`, vale `success()`). m2 e m3 invece partono, perché un fallimento non è una cancellazione (`!cancelled()` resta vero). Poi `raccogli` scrive `falliti=claude-fable-5-1, claude-opus-5-5, claude-opus-4-8`. Il verdetto vuoto finisce in `decidi(None)`, che dà RIPROVA e quindi un check `cancelled`.
   - L'esito resta sicuro: mai success, e nessuna quota spesa, perché Claude Code si ferma all'installazione. Ma:
     - (a) il corpo della review dice "Cambio modello: falliti prima …" e dà la colpa ai modelli invece che all'isolamento: diagnosi fuorviante;
     - (b) se una versione futura della CLI passasse da "rifiuto" ad "avviso", m2 lancerebbe il modello su un runner che il job stesso ha dichiarato senza isolamento.
   - Correzione consigliata: dare un `id:` allo step e aggiungere `steps.<id>.outcome == 'success'` all'`if` di m2 e m3 (m1 è già protetto). In alternativa basta dichiararla.

4. `tests/test_unit_verifica_bot.py:882` — `test_bubblewrap_installato_prima_di_claude`.
   - Ho riprodotto la prova a mutazione: con `exit 1` cambiato in `true`, risultato 1 failed / 268 passed (il test se ne accorge). File ripristinato: diff non in staging vuoto, staging invariato. Suite intera: **269 passed** (riprodotto).
   - Esito: **riserva R-192-2 (BASSA)**. Il test controlla che la stringa `"exit 1"` compaia nello step, non che compaia la prova minima `bwrap`. Togliere la prova lasciando un `exit 1` altrove passerebbe.

5. Domanda (4), coerenza con R-162-1 (riserva della review #162: "bubblewrap e isolamento dei processi NON attivi"). La causa registrata era che l'installazione dentro l'action scatta solo con `allowed_non_write_users`. Ora bwrap lo installa il job e la CLI 2.1.289 lo esige con lo scrub attivo. Quindi R-162-1 è **probabilmente chiusa**, ma solo una run reale riuscita lo dimostra. Va annotata in `stato_progetto.md` come "da confermare dopo il rilancio su #142", non chiusa adesso.

6. `reports/stato_progetto.md:112` — riga di stato coerente con il diff. **ok**.

**Riserve**
- **R-192-1 (BASSA):** se lo step dell'isolamento fallisce, m2 e m3 partono comunque e l'esito attribuisce il fallimento ai tre modelli. Correzione: legare m2 e m3 all'outcome dello step, oppure dichiararla.
- **R-192-2 (BASSA):** il test non vincola la presenza della prova `bwrap` né l'id dello step.
- **R-162-1:** da chiudere solo dopo la run reale.

**Rischi esplicitamente esclusi**
- Comportamento reale sul runner GitHub (installazione apt, sysctl effettivi, prova che passa e Claude Code che accetta il bwrap installato): non riproducibile in locale. Lo confermerà il rilancio della verifica su #142 dopo il merge.
- Le opzioni esatte con cui la CLI 2.1.289 chiama bwrap: non lette nel sorgente della CLI.
- Il bot non può verificare questa PR (tocca la sua stessa macchina, quindi esito neutral): il merge resta all'operatore.

Riga contatore #192 e una lezione nuova scritte in `.claude/agents/memoria_revisore.md` e committate da sole (commit `15670fd`). Il diff in staging non è stato committato, come richiesto.

### Review #193 — dopo R-192-1/2

## VERDETTO: APPROVATO CON RISERVE

**In breve:** R-192-1 (i modelli di riserva partivano anche con l'isolamento rotto) è chiusa sulla parte che conta: senza bubblewrap ora non parte nessun modello. R-192-2 (test troppo debole) è chiusa. Resta un difetto minore: il messaggio finale dà ancora la colpa ai tre modelli quando il problema è l'isolamento.

**Elementi del diff esaminati**

1. `.github/workflows/verifica-bot.yml:160` — `id: sandbox` sullo step che installa bubblewrap. Senza continue-on-error, l'outcome dello step è `failure` quando lui fallisce. **ok**

2. `.github/workflows/verifica-bot.yml:196` e `:212` — l'`if` di m2 (Opus 5.5) e di m3 (Opus 4.8) ora include `steps.sandbox.outcome == 'success'`.
   - Percorso con l'isolamento rotto: m1 viene saltato perché senza `if` vale `success()` implicito; m2 e m3 vengono saltati per la nuova condizione.
   - Percorso normale: la condizione è vera, la cascata dei modelli non cambia.
   - **ok**

3. `tests/test_unit_verifica_bot.py:894-899` — il test ora esige la prova minima `bwrap --unshare-all ...`, l'id `sandbox` e la condizione su m2 e m3.
   - Suite: **269 passed** (riprodotto).
   - Prove a mutazione riprodotte da me, oltre a quella su m2 fatta dall'agente:
     - condizione tolta da **m3** (riga 212): 1 failed;
     - id rinominato `sandbox` → `sbx`: 1 failed.
   - File ripristinato ogni volta: diff non in staging vuoto, staging invariato. **ok**

4. Contesto, file non toccato: `.github/workflows/verifica-bot.yml:226-238`, lo step "Raccogli il verdetto". Ha `if: !cancelled()` e gira anche quando l'isolamento fallisce. Con S1, S2 e S3 vuoti scrive `falliti="claude-fable-5-1, claude-opus-5-5, claude-opus-4-8"`. Il check finale resta `cancelled` ("verifica non conclusa", mai success), ma la review dell'App dice "Cambio modello: falliti prima …" quando non è partito nessun modello. **riserva**

**Riserve**
- **R-193-1 (BASSA, solo diagnosi):** "Raccogli il verdetto" non distingue "isolamento assente" da "tre modelli falliti". Correzione suggerita: passare `steps.sandbox.outcome` a `raccogli` e, se non è `success`, scrivere `falliti="sandbox bubblewrap non disponibile"`. Non blocca: l'esito resta sicuro.
- **R-193-2 (COSMETICA):** nel test, il `for` su m2 e m3 passa senza controllare nulla se quegli id spariscono o cambiano. Basterebbe verificare che entrambi esistano.
- **R-162-1:** l'annotazione "probabilmente chiusa, da confermare con il rilancio su #142" in `stato_progetto.md` è corretta.

**Rischi esplicitamente esclusi**
- Comportamento reale su GitHub Actions: valore effettivo di `steps.sandbox.outcome`, installazione apt, sysctl, Claude Code che accetta il bwrap installato. Non riproducibile in locale: lo confermerà il rilancio della verifica su #142 dopo il merge, che decide l'operatore.
- Le opzioni esatte con cui la CLI 2.1.289 chiama bwrap: non lette nel sorgente.

Riga contatore #193 scritta in `.claude/agents/memoria_revisore.md` e committata da sola (commit `b2c92ad`). Il diff in staging non è stato committato.

## §5 DELTA TEST DEL MOTORE

Nessuna modifica a gas.py/brains/modules.

```
python -m pytest -q tests/test_unit_verifica_bot.py → 269 passed
```

## §6 STATO CI

Run del bot su #142 (run 37603095039): smista success; verifica: claude-code-action fallito x3 ("bubblewrap is required for subprocess env scrubbing"); esito: review dell'App pubblicata, check cancelled. Run CI di questo branch: non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- **R-193-1** (BASSA): con sandbox fallito la review dice "falliti i tre modelli".
- **R-193-2** (cosmetica): il test non esige che m2/m3 esistano.
- **R-162-1**: da confermare chiusa con il rilancio su #142.
