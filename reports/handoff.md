# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-10-15 — FASE 2.6 fetta 2: riflessione automatica a fine compito notturno e a `clear`

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #211 (https://github.com/Gasss23/Gas/pull/211).

(`gh` non disponibile nella sessione cloud: numero/URL della PR presi dall'esito reale di `create_pull_request` via MCP GitHub.)

---

## §1 SCOPE & ESITO FETTE

- **Riflessione a fine compito notturno**: `FATTA` — `rifletti(iniettabile=False)`, lezioni in quarantena, recap `recap_notte` mai reiniettato, solo il numero delle lezioni su riepilogo/Telegram.
- **Riflessione a `clear`**: `FATTA` — Ctrl-C la salta, pulisce sempre.
- **Spegnimento `GAS_RIFLESSIONE_AUTO=0`**: `FATTA`.
- **Nota bassa bot #210 (`old.keys/`)**: `FATTA` come registrazione (R-bot210-3), codice fuori scope.
- **Prova con provider reali**: `DEFERITA` — nessuna chiave nel container; alla prossima notte sul Mac.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   3 +++
 gas.py                             |  42 +++++++++++++++++++++++++++++++++---------
 modules/notte/notte.py             |  53 +++++++++++++++++++++++++++++++++++++++++++++++++++++
 reports/diff_sessione.md           |  15 ++++++++++-----
 reports/handoff.md                 | 115 +++++++++++++++++++++++++++++++++++++++++++++++++++++--------------------------------------------------------------
 reports/roadmap.md                 |   2 +-
 reports/setup_notte.md             |   6 ++++++
 reports/stato_progetto.md          |   6 ++++--
 reports/ultimo_report.md           |  31 +++++++++++++++----------------
 tests/test_unit_kernel.py          | 100 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 tests/test_unit_notte.py           | 140 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 11 files changed, 418 insertions(+), 95 deletions(-)
```

NB: conteggi di `reports/handoff.md` (e totali) presi prima del proprio commit.

## §3 GIT LOG --ONELINE (sessione)

```
13b03cc feat(rifletti): riflessione automatica a fine compito notturno e a `clear` (FASE 2.6 fetta 2)
e528d4b chore(revisore): memoria review #346 — APPROVATO CON RISERVE
5cd7107 chore(revisore): memoria review #345 — APPROVATO CON RISERVE
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione.

## §4 VERDETTO DEL REVISORE (per commit motore)

### Review #345 — verdetto integrale

## VERDETTO: APPROVATO CON RISERVE

Ho letto CLAUDE.md (sez. 5, 8 e 9), le sezioni di reports/stato_progetto.md che riguardano la FASE 2.6 e la mia memoria (lezioni #199–#213 su rifletti e recap). Il diff staged non contiene slicing della cronologia né output di tool simulati. Il tetto di 10 iterazioni, `_get_window` e il tetto di spesa restano come prima: rifletti ricontrolla il budget prima di ogni rung.

**Test che ho rilanciato io:** tests/test_unit_kernel.py 857 PASS e 0 FAIL (T89a–j tutti PASS); tests/test_unit_notte.py 61 passed.

**Elementi del diff esaminati:**
- gas.py:3000 — con iniettabile=False un recap fidato diventa 'recap_notte'. Se la cronologia è contaminata resta 'recap_non_fidato', anche di notte. Rischio esaminato: un recap notturno che finisce nel prompt. `_recap_pin` (gas.py:2853) pesca solo il tipo 'recap' con fonte 'modello', e T89a lo verifica (pin vuoto). Esito: ok.
- gas.py:537 — 'recap_notte' aggiunto a `_TIPI_DIARIO_KERNEL`. Rischio esaminato: una tool call inventata col nome "recap_notte" che scrive una riga falsa nel diario (la linea R-199-1). Il nome viene rimappato su `_TIPO_TOOL_RISERVATO`. Esito: ok.
- gas.py:1199 — 'recap_notte' aggiunto a `DIARIO_NOISE_TIPI`. Il filtro è applicato a gas.py:2794 prima del tetto degli eventi, quindi il testo del modello non entra in «Ultime azioni» del pin di memoria. Esito: ok.
- gas.py:4701 — `_clear_con_riflessione`: riflette solo se la cronologia non è vuota e la riflessione automatica è accesa; un'eccezione viene loggata e la pulizia avviene comunque (T89i, T89j). Esito: riserva R-345-2.
- modules/notte/notte.py:265 — la riflessione parte solo se il compito non è scaduto, è sotto `max_sec` e ha una cronologia. Ha il suo try/except in `_rifletti_compito` (modules/notte/notte.py:201): un fallimento non cambia l'esito del compito né l'exit code del giro. Esito: ok. Sul tempo: riserva R-345-1.
- modules/notte/notte.py:295 e modules/notte/notte.py:333 — riepilogo e Telegram riportano solo numeri e messaggi fissi; il test controlla che «LEZIONE-SEGRETA» non compaia. L'invariante «testo del modello mai su Telegram» resta intatta. Esito: ok.
- tests/test_unit_notte.py:36 — la fixture `_ermetico` imposta GAS_RIFLESSIONE_AUTO=0. I test nuovi la riaccendono con delenv, e monkeypatch ripristina il valore a fine test. Esito: ok.

**Risposte ai tuoi tre punti:**
1. Sì, è corretto non iniettare il recap notturno. Di notte nessuno legge il recap prima che entri nel prompt di sistema, e notte.py vieta già di mettere la risposta del modello nel diario per lo stesso motivo. Il recap resta consultabile con `ricorda`, che è in UNTRUSTED_INPUT_TOOLS: chi lo legge contamina la finestra, quindi il taint si propaga. Le lezioni restano comunque in quarantena (T89b).
2. Sì, va bene, ma va scritto (R-345-1). È una sola chiamata, con il budget ricontrollato. Però non conta nella «durata» e può sforare il tetto del giro di una cascata intera, con lo stesso caso peggiore «non duro» di R-226-2 (circa 36 minuti). Il docstring del tetto di tempo in notte.py va aggiornato.
3. Sì, è accettabile. La fiducia è valutata fail-closed su tutta la cronologia: un compito KO con input esterno dà 'recap_non_fidato', e le lezioni passano comunque dal tuo sì. Se il compito è KO per budget esaurito, rifletti si ferma da sola sul controllo del budget e il riepilogo dice «Riflessione non riuscita». Riflettere sui fallimenti è anche la parte più utile.

**Riserve (da tracciare in stato_progetto.md):**
- R-345-1 BASSA: il tempo della riflessione è fuori dalla «durata» e dal tetto per compito, e può sforare il tetto del giro di una chiamata in cascata. Oggi non è documentato nel docstring del tetto di tempo.
- R-345-2 BASSA: prima `clear` era istantaneo, ora può durare minuti. Un Ctrl-C durante la riflessione fa uscire dal REPL (gas.py:4800, `except KeyboardInterrupt: break`) senza pulire la cronologia. Inoltre l'import di `modules.notte.notte` sta fuori dal try: oggi il rischio è teorico, ma va messo dentro la cintura.
- R-345-3 COSMETICA: «Lezioni da approvare: N» su Telegram conta solo le proposte di quel giro, non tutte quelle in attesa.

**Rischio escluso:** non ho verificato il comportamento con provider reali e tempi reali (latenza della riflessione sul Mac o su VPS, JSON vero dei modelli free). In questo ambiente non si può riprodurre: ho verificato solo con client finti.

Memoria aggiornata: riga #345 più una lezione (Ctrl-C e passaggi aggiunti prima del try quando un comando istantaneo diventa una chiamata LLM). È committata (5cd7107) in /home/user/Gas/.claude/agents/memoria_revisore.md.

### Review #346 (ri-review dopo R-345-1/2) — verdetto integrale

## VERDETTO: APPROVATO CON RISERVE

Ri-review del diff staged completo dopo le correzioni a R-345-1 e R-345-2. Il resto del diff non è cambiato rispetto alla #345: nessuno slicing della cronologia, nessun output di tool simulato, guardrail invariati.

**Test che ho rilanciato io:** tests/test_unit_kernel.py 858 PASS e 0 FAIL (compreso T89k); tests/test_unit_notte.py 61 passed.

**Elementi del diff esaminati:**
- gas.py:4708 — l'import di `riflessione_auto_attiva` ora sta dentro il try. Rischio esaminato: un errore di import che fa crashare il REPL prima della pulizia. Ora lo cattura `except Exception`, che lo logga in gas_debug.log, e poi `clear_history` viene eseguita. Esito: ok.
- gas.py:4713 — `except KeyboardInterrupt` stampa «Riflessione saltata» e la pulizia avviene comunque; l'interruzione non arriva al `break` del ciclo principale. Rischio esaminato: un Ctrl-C a metà riflessione, dopo il recap e prima delle lezioni. Lascerebbe un recap senza lezioni, che è uno stato coerente: il diario è append-only e le lezioni sono solo proposte. Un secondo Ctrl-C durante `clear_history` esce dal REPL come prima. Esito: ok.
- tests/test_unit_kernel.py:8791 — T89k: un rifletti che solleva KeyboardInterrupt porta a cronologia pulita, al messaggio di riflessione saltata e a nessuna propagazione. Il test morde: senza l'except, KeyboardInterrupt non è sottoclasse di Exception e uscirebbe dal blocco T89. Esito: ok.
- modules/notte/notte.py:47 — il docstring del tetto di tempo ora dice che la riflessione resta fuori dalla «durata» e dal tetto per compito e che il giro può sforare di una cascata (R-345-1). Corrisponde al codice di modules/notte/notte.py:265. Esito: ok.

**Riserve:** R-345-1 e R-345-2 sono chiuse. Resta R-345-3 COSMETICA, già tracciata: «Lezioni da approvare: N» conta solo le proposte del giro.

**Rischio escluso:** non ho provato un Ctrl-C reale dentro una chiamata HTTP del client OpenAI. Il test simula l'interruzione con un rifletti finto, e non ho verificato se l'SDK la rilancia come KeyboardInterrupt o la incapsula. In questo ambiente non si riproduce in modo deterministico. Se la incapsulasse, il ramo `except Exception` pulisce comunque.

Memoria aggiornata: riga #346, nessuna lezione nuova. È committata (e528d4b) in /home/user/Gas/.claude/agents/memoria_revisore.md.

## §5 DELTA TEST DEL MOTORE

tests/test_unit_kernel.py: 847 → 858 PASS, 0 FAIL (T89a–k nuovi). Blocco reale: `=== RIEPILOGO: 858 PASS, 0 FAIL ===`.
tests/test_unit_notte.py: 57 → 61 passed.
pytest `tests/`: `1418 passed in 186.65s (0:03:06)` (prima delle correzioni R-345, che aggiungono T89k).

## §6 STATO CI

`gh` non disponibile nella sessione cloud: lo stato CI si legge dai check-run della PR via MCP GitHub.

- `5cd7107`, `e528d4b`, `13b03cc`: pushati insieme prima dell'apertura della PR #211; run non ancora disponibile alla scrittura dell'handoff.
- Commit di fine-task (questo handoff): run non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- R-345-3 (COSMETICA): «Lezioni da approvare: N» conta solo le proposte del giro.
- R-bot210-3 (BASSA): prefisso di copia senza il punto (`old.keys/` libero).
- Prova con provider reali da fare sul Mac.
