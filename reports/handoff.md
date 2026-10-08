# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-10-08 — FASE 4.5 fetta 1: `gas notte`, giro autonomo dei compiti dal catalogo

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #160 (https://github.com/Gasss23/Gas/pull/160). Tocca motore e CI. Numero e URL presi dalla risposta di GitHub alla creazione: `gh` qui non è autenticato, quindi la PR è stata creata con lo strumento GitHub della sessione.
2. Dopo il merge, sul Mac: seguire `reports/setup_notte.md` (catalogo `~/.gas_notte.yaml` e timer launchd, 5 passi).
3. Ancora aperte dalla sessione precedente:
   - decidere le lezioni #4, #5, #6 (parere dell'agente: approva 6 e 5, rifiuta 4);
   - decidere la firma in attesa `fab385e4…` con il bot Telegram avviato.

---

## §1 SCOPE & ESITO FETTE

- **Fetta 1 FASE 4.5 — comando `gas notte`**: `FATTA`
  - modulo `modules/notte/`, comando `notte_cmd` in `gas.py`;
  - 20 test e passo CI;
  - review #220 APPROVATO CON RISERVE.
- **Template launchd, catalogo di esempio e guida**: `FATTA` — `scripts/notte/`, `reports/setup_notte.md`.
- **Riepilogo su Telegram al mattino**: `DEFERITA` — rimandato alla fetta 2.
- **Orari per singolo compito**: `DEFERITA` — per ora c'è un solo giro a notte, avviato dal timer di sistema.
- **Prova reale con launchd sul Mac**: `DEFERITA` — non si può riprodurre su Linux; la fa l'operatore.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md  |   2 ++
 .github/workflows/ci.yml            |   8 ++++++++
 .gitignore                          |   2 ++
 gas.py                              |   9 +++++++++
 modules/notte/__init__.py           |   4 ++++
 modules/notte/notte.py              | 243 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 reports/diff_sessione.md            |  19 +++++++++++--------
 reports/handoff.md                  |  92 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++----------------
 reports/setup_notte.md              |  42 ++++++++++++++++++++++++++++++++++++++++++
 reports/stato_progetto.md           |   4 ++--
 reports/ultimo_report.md            |  34 +++++++++++++++++++++-------------
 scripts/notte/catalogo_esempio.yaml |  15 +++++++++++++++
 scripts/notte/com.gas.notte.plist   |  27 +++++++++++++++++++++++++++
 tests/test_unit_notte.py            | 282 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 14 files changed, 744 insertions(+), 39 deletions(-)
```

## §3 GIT LOG --ONELINE (sessione)

```
2a2ed0d feat(fase-4.5): gas notte — giro autonomo dei compiti dal catalogo (fetta 1)
365e27d chore(revisore): memoria review #220 — APPROVATO CON RISERVE
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione. Il suo hash è stampato al passo 5.

## §4 VERDETTO DEL REVISORE (per commit motore)

Commit `2a2ed0d` — review #220, verdetto integrale del revisore:

## VERDETTO: APPROVATO CON RISERVE

Il commit si può fare. Nessuna regola del "Wall of Shame" viene violata: non c'è slicing diretto della cronologia e non c'è output dei tool simulato. Il cancello e il cap di 10 iterazioni restano quelli di `run_turn`, che non è stato toccato. Ho trovato quattro riserve di gravità BASSA (sotto); vanno scritte in `reports/stato_progetto.md`.

**Elementi del diff esaminati**

1. `modules/notte/notte.py:135` — ogni compito parte con `kernel.history = []` e a :136 `kernel.db_path` punta a `.gas_notte/storia_<nome>.json`, così la cronologia dell'operatore non entra nella finestra né viene sovrascritta. Il nome non può uscire dalla cartella perché la regex di :47 ammette solo `[a-z0-9_-]{1,40}`. Ho provato a togliere il cambio di `db_path` (mutation): 2 test FAIL, quindi i test lo coprono. Esito: ok.
2. `modules/notte/notte.py:80` — `_dentro` confronta i path dopo `resolve()`, quindi un catalogo dentro la root viene rifiutato anche se ci arriva tramite symlink (testato). Hardlink e parent fuori root non li ho provati. Esito: ok.
3. `modules/notte/notte.py:152` — nel diario va una sola riga di metadati (`fonte="kernel"`). Ho provato ad aggiungere il testo della risposta alla riga (mutation): `test_diario_solo_metadati` FAIL. Le righe di diario delle singole tool call restano quelle di sempre di `run_turn` (riassunto degli argomenti), come di giorno. Esito: ok.
4. `modules/notte/notte.py:202-207` — lock non bloccante: se un altro giro è in corso esce con codice 2 dentro il try, e il `finally` chiude il file. Su Windows (`fcntl` None) gira senza lock, ed è dichiarato. Esito: ok.
5. `gas.py:3583` — `notte_cmd` più il dispatch in `main()` sono l'unica modifica al kernel. L'import è pigro, quindi non ci sono effetti al caricamento. Esito: ok.
6. `tests/test_unit_notte.py:162` — round-trip agentico §7 col kernel vero: read_file, poi calcola, poi la risposta finale. Verifica anche che la storia dell'operatore resti intatta e che "SEGRETO" non arrivi mai al provider. Esito: ok.
7. `.github/workflows/ci.yml:133` — nuovo passo `if: always()` con `pipefail`, e nessun `paths-ignore` aggiunto. Esito: ok.

Risultati riprodotti da me: `test_unit_notte.py` 20 passed; `tests/test_unit_kernel.py` 707 PASS, 0 FAIL. Dopo le mutation il file è stato ripristinato e confrontato con l'index (nessuna differenza).

**Riserve**

- **R-220-1 (BASSA)**: l'isolamento della cronologia regge fino alla firma, non oltre.
  - Un'azione notturna messa in attesa e poi firmata su Telegram viene eseguita dal kernel del bot (`modules/telegram/bot.py:225`, che usa `.gas_history.json`).
  - `_storia_esito_firma` (`gas.py:1553`) scrive la notifica e l'output del tool nella conversazione dell'operatore.
  - L'output finisce nel ruolo tool, quindi la contaminazione viene comunque calcolata. Va però corretta la frase "non sporca la conversazione dell'operatore" nel docstring di `notte.py` e in `reports/setup_notte.md`, oppure in una fetta futura va legato l'esito della firma alla storia del compito.
- **R-220-2 (BASSA)**: `GasKernel.__init__` (`gas.py:659`) legge comunque `.gas_history.json` prima che `notte` azzeri la cronologia. Se il file è corrotto lo rinomina in `.corrupt.*` anche durante il giro notturno. Questo contraddice "non viene letta". Rimedio possibile: un parametro del kernel che salta il caricamento della storia.
- **R-220-3 (BASSA)**: non c'è un tetto di tempo né per compito né per giro. Un provider bloccato, tra timeout e retry del client, può allungare il giro di ore. È limitato (10 iterazioni per 4 provider), ma non dichiarato.
- **R-220-4 (BASSA, coincide col rischio (a) che hai dichiarato)**: `.gas_notte/` non è tra i prefissi vietati di `modules/gate/gate.py:76` (`_DENY_PREFIXES`). Il problema riguarda anche `launchd.log`, che sta in quella cartella secondo il plist: di giorno Gas può scriverlo (quindi falsificarlo) e leggerlo. Rimedio: aggiungere `.gas_notte` ai prefissi vietati. È una modifica al cancello, quindi va revisionata.

**Rischi esclusi (non verificati)**

- Comportamento reale di launchd sul Mac (risveglio dallo stop, creazione del log, caricamento di `.env` con zsh): non riproducibile in questo ambiente Linux.
- Corsa tra un giro notturno e una sessione diurna o il bot attivi in contemporanea sullo stesso `.gas_memory.db`: non l'ho testata. Mi affido al WAL di SQLite già in uso.

Ho aggiunto in memoria la riga #220 e la lezione: l'isolamento di un'esecuzione autonoma va seguito anche lungo il percorso della firma, cioè chi esegue l'azione approvata e in quale cronologia scrive l'esito. Le ho committate col commit `365e27d`, che contiene solo quel file; il diff staged sotto review è rimasto com'era.

## §5 DELTA TEST DEL MOTORE

- Suite kernel (`python tests/test_unit_kernel.py`): 707 PASS prima, 707 PASS dopo. Nessun test kernel aggiunto e nessuno rotto. Output reale: `=== RIEPILOGO: 707 PASS, 0 FAIL ===`.
- Nuova suite `tests/test_unit_notte.py`: da 0 a 20 test. Output reale: `20 passed in 1.91s`.
- Mutation provate a mano, tutte colte:
  - rimozione del reset della cronologia: 1 FAIL;
  - disattivazione del controllo "catalogo dentro la root": 2 FAIL;
  - testo della risposta inserito nella riga di diario: 1 FAIL.
- Una mutation (lock condiviso al posto di esclusivo) è risultata equivalente nel test.

## §6 STATO CI

`gh` non è autenticato (`Failed to log in to github.com using token (GH_TOKEN)`), quindi le run sono state lette con lo strumento GitHub Actions della sessione.

| Commit | Run CI | Stato alla scrittura dell'handoff |
|---|---|---|
| `2a2ed0d` (feat, testa del push) | CI run 37800758579 (#765), evento push | in_progress |
| `365e27d` (memoria del revisore) | nessuna run su questo SHA | pushato insieme a `2a2ed0d`: è testato solo come parte dell'albero di `2a2ed0d` |
| commit di fine-task che contiene questo file | — | run non ancora disponibile alla scrittura dell'handoff |

Run precedente sul branch: `5d759ff`, CI run 37798972499 → success. Quel commit è della sessione precedente.

## §7 RISERVE APERTE

Nuove, dalla review #220, tutte BASSE e tracciate in `reports/stato_progetto.md` alla voce 6:

- **R-220-1** — l'esito di un'azione firmata finisce nella cronologia dell'operatore.
  - Già corretto: `reports/setup_notte.md`.
  - Da correggere: il docstring di `notte.py`.
- **R-220-2** — `__init__` del kernel legge comunque `.gas_history.json`.
- **R-220-3** — nessun tetto di tempo, né per singolo compito né per l'intero giro.
- **R-220-4** — `.gas_notte/` non è tra i prefissi vietati dal cancello.

Restano aperti dalle sessioni precedenti (non sono riserve): lo scarto intermittente di Gemini su `rifletti` e il bottone Rifiuta di Telegram (voce 9).
