# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-10-07 — Bot di verifica: diagnosi dell'errore nascosto (seconda prova reale, PR #142)

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #144 (https://github.com/Gasss23/Gas/pull/144). Numero e URL dall'output del connettore GitHub (`create_pull_request` → `{"id":"4771343797","url":"https://github.com/Gasss23/Gas/pull/144"}`). Tocca la macchina del bot: merge dell'operatore.
2. Dopo il merge: rilanciare la verifica su #142 e leggere la riga `DIAGNOSI:`.

---

## §1 SCOPE & ESITO FETTE

- **Merge #143 (bubblewrap)**: `FATTA` su richiesta dell'operatore, CI verde.
- **Seconda prova reale su #142**: `FATTA` x2 — bwrap OK, modelli fermi in ~0,2 s (is_error, costo 0), anche col token rigenerato.
- **Step di diagnosi**: `FATTA` (PR #144).
- **Verifica esterna §4quater**: `SALTATA — fetta di sola diagnosi; la prova reale è il rilancio su #142 dopo il merge (decide l'operatore se lanciarla prima)`.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   3 +++
 .github/workflows/verifica-bot.yml |  26 ++++++++++++++++++++++++++
 reports/diff_sessione.md           |  13 +++++--------
 reports/handoff.md                 | 158 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++----------------------------------------------------------------------------
 reports/stato_progetto.md          |   2 ++
 reports/ultimo_report.md           |  24 ++++++++++++------------
 tests/test_unit_verifica_bot.py    |  16 ++++++++++++++++
 7 files changed, 146 insertions(+), 96 deletions(-)
```

## §3 GIT LOG --ONELINE (sessione)

```
15224c2 fix(verifica-bot): diagnosi dell'errore nascosto quando nessun modello dà il verdetto — review #194/#195
cd78aae chore(revisore): memoria review #195 — APPROVATO
7345499 chore(revisore): memoria review #194 — APPROVATO CON RISERVE
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione. Il suo hash è stampato al passo 5.

## §4 VERDETTO DEL REVISORE (per commit motore)

Verdetti INTEGRALI. Unica trasformazione meccanica: i path assoluti del worktree (`/home/user/wt-diag/`) resi relativi alla radice del repo.

### Review #194 — diff iniziale

## VERDETTO: APPROVATO CON RISERVE

Review #194. Prima della review ho letto CLAUDE.md (sez. 5, 8, 9, 10), le voci V-B e bot in `reports/stato_progetto.md` e la memoria del revisore fino alla #193.

**Elementi del diff esaminati**

1. `.github/workflows/verifica-bot.yml:255` — la condizione `if: ${{ !cancelled() && steps.raccogli.outputs.modello == '' }}`.
   - Rischio: lo step parte quando non deve, oppure cambia l'esito.
   - Esito: **ok**. "Raccogli il verdetto" (:226) lascia `modello` vuoto solo se S1, S2 e S3 sono tutti vuoti. Le uscite del job (:93-96) vengono solo da `raccogli`, che è già stato eseguito, quindi la diagnosi non può alterarle. Se `raccogli` viene saltato, anche `modello` è vuoto e la diagnosi parte lo stesso. Ma a quel punto non ci sono file e lo step stampa "assente": innocuo.

2. `.github/workflows/verifica-bot.yml:261-268` — `${FILE_M3:-${FILE_M2:-$FILE_M1}}`, il test `-f` e jq con fallback `|| echo`.
   - Rischio: lo step si rompe, o perde segreti.
   - Esito: **ok** sulla robustezza. Ho provato tre casi in locale:
     - array vuoto: stampa `subtype=null is_error=null result=`;
     - JSON che non è un array: jq dà errore e scatta il messaggio di fallback, rc 0 (anche con `bash -e`);
     - nell'`env` dello step non c'è nessun `secrets.*`.
   - Esito: **riserva** sul testo stampato, vedi R-194-1.

3. `tests/test_unit_verifica_bot.py:902` — `test_diagnosi_solo_result_e_dopo_i_modelli`.
   - Cosa vincola: l'ordine dopo `raccogli`, la condizione esatta, il troncamento `.[0:400]`, l'assenza di `cat` e di `show_full_output`, nessun segreto nell'env.
   - Esito: **ok**, 270 passed riprodotto.

**Riserve**

- **R-194-1 (BASSA, riprodotta): comandi di GitHub Actions nascosti nel campo `result`.**
  - Cosa succede: `jq -r` stampa i ritorni a capo di `result` così come sono. Se il messaggio contiene una riga che comincia con `::error::...` o `::set-output name=x::y`, GitHub la esegue come comando del workflow. L'ho verificato in locale su un file con quel contenuto.
  - Impatto limitato: lo step non ha `id`, le uscite del job vengono da `raccogli` e `set-env`/`add-path` sono disabilitati. Il danno possibile è un'annotazione falsa nel log o un `stop-commands`.
  - Correzione: `(.result // "") | tostring | gsub("[\r\n]"; " ") | .[0:400]`, oppure `@json`.

- **R-194-2 (BASSA): la stampa salta il filtro credenziali.**
  - Cosa succede: il repo è pubblico, e la diagnosi scrive `result` nel log senza passare dal controllo credenziali V-2/R-159-2 di `scripts/bot_esito.py:192` (citazione di contesto).
  - Attenuanti: quando la CLI esce subito in errore, `result` è un suo messaggio, non testo del modello. Il token OAuth e il GITHUB_TOKEN vengono mascherati dal runner. Il testo è troncato a 400 caratteri.
  - Rischio residuo: se un domani `result` contenesse testo del modello che ha letto la PR, una credenziale non registrata come segreto uscirebbe nel log. In alternativa si può stampare `result` solo con `is_error == true` e ripassarlo dal controllo di `bot_esito`.

- **R-194-3 (COSM.):** viene diagnosticato solo l'ultimo modello partito, di norma m3. Se m1 (Fable) fallisce per un motivo diverso, ad esempio un modello non disponibile, quel motivo resta nascosto. Si possono stampare tutti e tre i file, ciascuno troncato.

**Rischi esclusi esplicitamente**

- Non ho verificato che l'action cab360f imposti davvero `execution_file` anche quando l'esecuzione finisce con `is_error`, né il formato reale del file: lo dichiara chi ha fatto la modifica, l'ho trovato in action.yml ma non è riproducibile in dev. Lo dirà solo la prossima run su #142.
- Non ho verificato se `::set-output` via stdout sia ancora attivo sui runner di oggi: in ogni caso non ha effetto su uno step senza `id`.

Nessun problema dalla sezione 5 di CLAUDE.md (né slicing della history né output dei tool simulati) e nessun guardrail del motore toccato. La modifica serve solo alla diagnosi e non cambia l'esito.

La memoria è aggiornata con la riga #194 e una lezione nuova, già committata da sola (`7345499`) in `.claude/agents/memoria_revisore.md`. Il diff staged è rimasto intatto.

File rilevanti:
- `.github/workflows/verifica-bot.yml`
- `tests/test_unit_verifica_bot.py`
- `.claude/agents/memoria_revisore.md`

### Review #195 — dopo R-194-1/2

## VERDETTO: APPROVATO

Review #195, di conferma sulle riserve della #194. Le correzioni funzionano: le ho provate eseguendo lo step vero, preso dal workflow.

**Elementi del diff esaminati**

1. `.github/workflows/verifica-bot.yml:270-271` — `result` viene stampato solo se `.is_error == true`, e i ritorni a capo diventano spazi (`gsub("[\\r\\n]"; " ")`) prima del taglio a 400 caratteri.
   - Rischio: comandi del runner nascosti nel testo (R-194-1) e testo del modello che finisce nel log (R-194-2).
   - Prova: ho estratto il `run` dal YAML con yaml.safe_load e l'ho eseguito con `bash -e`.
   - Esito: **ok**. Il doppio backslash dentro il blocco YAML e gli apici singoli della shell arriva a jq come la regex `[\r\n]`, quindi funziona. Risultati:

| Caso di prova | Uscita | rc |
|---|---|---|
| `"riga1\n::error::finto\r\nfine"` | una sola riga, `::error::` resta a metà riga e non viene eseguito | 0 |
| `is_error:false` | `(non stampato: non è un errore)` | 0 |
| `error_max_turns` senza `result` | `result=` vuoto | 0 |
| array vuoto | `null`, non stampato | 0 |
| JSON che non è un array | messaggio "illeggibile" | 0 |
| file assente | "assente" | 0 |
| solo `FILE_M1` impostato | ripiega correttamente su m1 | 0 |

2. `.github/workflows/verifica-bot.yml:252-253` — il commento dichiara R-194-3: l'action scrive le tre esecuzioni sullo stesso file.
   - Rischio: una diagnosi che sembra completa e non lo è.
   - Esito: **ok**. La spiegazione regge: con un percorso fisso, un ciclo sui tre file stamperebbe tre volte m3. R-194-3 resta un limite dichiarato, non un difetto.

3. `tests/test_unit_verifica_bot.py:913` — il test ora controlla anche la presenza di `gsub(` e di `.is_error == true`.
   - Esito: **ok**, 270 passed riprodotto. Il controllo è testuale e non esegue lo step; per questo la prova vera l'ho fatta al punto 1.

**Rischi esclusi esplicitamente**

- Non ho verificato che il percorso del file fisso sia quello che dice il coordinatore (`_temp/claude-execution-output.json`): l'ho preso dal suo racconto del log della run, non dal codice dell'action.
- Resta un rischio residuo: se `is_error` è vero ma `result` contiene testo del modello, quel testo esce nel log (troncato e mascherato per i segreti del job). Il caso osservato (uscita in circa 0,2 s, costo 0) è un errore della CLI. Lo vedrà solo la prossima run reale su #142.

La memoria è aggiornata con la riga #195, già committata da sola (`cd78aae`). Il diff staged è rimasto intatto (2 file, +42).

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

Run del bot su #142 dopo #143 (run 37603998259 e 37607359375): smista success; sandbox success; m1/m2/m3 falliti ("--json-schema was provided but Claude did not return structured_output", result is_error, duration 245 ms, costo 0); esito: review dell'App, check cancelled. Run CI di questo branch: non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- **R-194-3** (cosmetica, dichiarata): si vede solo l'ultima esecuzione (file unico).
- **R-193-1** (BASSA), **R-193-2** (cosmetica): aperte.
- **R-162-1**: da confermare con un verdetto reale su #142.
