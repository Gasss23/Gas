# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-10-21 (dopo il merge di #234) — tre stati per un comando firmato (R7, R-c4b3-5)

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #236 (https://github.com/Gasss23/Gas/pull/236; numero e URL dall'API GitHub, `gh` non usato): pro e contro in `reports/da_mergiare.md`; l'agente mergia da solo solo con un APPROVATO pulito del bot (CLAUDE.md §10).

---

## §1 SCOPE & ESITO FETTE

- **Merge PR #234**: `FATTA` — su richiesta dell'operatore, merge `35b55be` (prima unito main #235, review #427 APPROVATO).
- **C6**: `FATTA` (decisione) — l'operatore ha scelto (a) «lasciamo così».
- **R7 / R-c4b3-5 — tre stati per un comando firmato**: `FATTA` — review #428 APPROVATO CON RISERVE.
- **R-428-1/2/3/4**: `FATTA` — review #429 APPROVATO CON RISERVE.
- **R7 / R-c4b3-4, R-c4b3-3**: `DEFERITA` — prossime fette.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |    3 ++
 gas.py                             |   52 +++++++++++++++----
 modules/telegram/bot.py            |    4 ++
 reports/da_mergiare.md             |   42 +++------------
 reports/diff_sessione.md           |   15 +++---
 reports/handoff.md                 | 1014 +++++++++++++++++++++-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
 reports/roadmap.md                 |    4 +-
 reports/stato_progetto.md          |    2 +-
 reports/ultimo_report.md           |   39 +++++---------
 tests/test_unit_kernel.py          |   56 ++++++++++++++++++++
 10 files changed, 192 insertions(+), 1039 deletions(-)
```

## §3 GIT LOG --ONELINE (sessione)

```
be72cb5 fix(firma): segno «partito» azzerato a ogni tool call, errore di avvio non incerto, il modello legge «esito INCERTO» (R-428-1/2/3/4)
40da5ce chore(revisore): memoria review #429 — APPROVATO CON RISERVE
c19defc fix(firma): comando firmato partito e interrotto → esito INCERTO, non «NON eseguito» (R7, R-c4b3-5)
b997a5c chore(revisore): memoria review #428 — APPROVATO CON RISERVE
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione.

## §4 VERDETTO DEL REVISORE (per commit motore)

### Review #428 (chat Motore) — commit c19defc

## VERDETTO: APPROVATO CON RISERVE

Review #428 (chat Motore). Il diff staged riguarda R-c4b3-5: un run_command firmato che parte e va in timeout ora viene detto «partito, esito incerto». Ho letto prima, come richiesto: CLAUDE.md sezione 5, la voce R-c4b3-5 in reports/stato_progetto.md e la memoria (#134 e la lezione del 2026-10-03 sui tre stati).

**Prove fatte su una copia dello staged nello scratchpad (poi cancellata).**
- Suite del kernel: 973 PASS, 0 FAIL. T77u passa.
- Sonda diretta, con l'allowlist di test (in produzione `SHELL_ALLOWLIST` è vuota, quindi in produzione tutto questo resta latente).

**Elementi del diff esaminati**
- gas.py:3920 — mette il segno «partito» subito prima di `subprocess.run`, dopo vetting, dry-run, controllo os_strict e snapshot. Rischio: un diniego prima della partenza marcato come «partito». Esito: ok. Ogni `return` di diniego viene prima del segno. Nella sonda, un comando negato al vetting dopo un segno rimasto True lo riporta a False e dà «[KO]».
- gas.py:3869 — azzera il segno all'ingresso di execute_tool_call, accanto a `_esito_contenuto` (dichiarato anche in gas.py:953). Rischio: il segno sopravvive alla chiamata dopo. Esito: ok per ogni chiamata che passa da execute_tool_call (la seconda parte di T77u e la mia sonda lo confermano). Riserva per i rami che non ci passano: vedi R-428-1.
- gas.py:2069 — «[KO] esito incerto: partito ma interrotto» quando meta è None e il segno è True, controllato prima di `negativo`. Rischio: il prefisso «Errore eseguendo» nasconderebbe il caso. Esito: ok, l'ordine è quello giusto.
- gas.py:3106 e gas.py:3110 — in applica_firma: `incerta`, `res["stato"]`, la notizia «PARTITO… Esito INCERTO: verifica prima di ripetere» e la presa d'atto «partita, esito INCERTO». `eseguita` resta False. Rischio: qualcuno tratta «incerta» come successo. Esito: ok. Gli unici consumatori sono modules/telegram/bot.py:694 e modules/telegram/bot.py:751, che passano a componi_esito_firma. Il diario usa «approvata id=… | [KO] esito incerto…».
- modules/telegram/bot.py:667 — nuovo ramo «⚠️ Approvata e PARTITA, ma esito INCERTO». Rischio: ordine dei rami. Esito: ok. Viene dopo `eseguita` e prima del «NON eseguita», e non mostra l'output, che contiene l'argv bwrap.
- tests/test_unit_kernel.py:6874 — il `subprocess.run` finto scade solo per il comando, non per lo snapshot git. Esito: ok, il test esercita il percorso reale fino al punto del timeout.

**Altre uscite dopo la partenza (sonda)**
- TimeoutExpired: «incerto». Corretto.
- FileNotFoundError, in fallback senza bwrap e col binario assente: «incerto» anche se il processo non è mai partito (R-428-2).
- KeyboardInterrupt: non è una `Exception`, quindi esce sia da execute_tool_call sia da applica_firma e il segno resta True. Che si propaghi è un comportamento che c'era già. Il reclamo è già avvenuto, quindi l'azione non si riesegue.

**Conteggio della notte:** invariato. modules/notte/notte.py:262-271 conta da `ev["cancello"]`, che a sua volta dipende solo dal testo di `out`.

**Riserve**
- **R-428-1 MEDIA (provata).** Il segno resta True nei rami di run_turn che non chiamano execute_tool_call ma chiamano lo stesso `_esito_diario` (gas.py:4270): il DENY e il cancello. Sequenza della sonda: run_command in timeout, poi un run_command parcheggiato nello stesso turno o in uno successivo → il diario scrive «[KO] esito incerto: partito ma interrotto» (prima «[OK] (non eseguito)»). In più `_turno_tool_ko` sale di 1 e il turno risulta «parziale». Con un run_command negato dal DENY il diario dice «esito incerto» invece di «[KO]». Il segno resta finché un qualsiasi tool non passa da execute_tool_call.
  - Correzione suggerita: in run_turn, per ogni tool call e prima dei rami del cancello, azzerare `self._run_command_meta = None` e `self._run_command_avviato = False`. In alternativa, in `_esito_diario` considerare il segno solo se `s.startswith("Errore eseguendo")`.
  - La stessa correzione chiude un difetto gemello che c'era già: un `_run_command_meta` rimasto da un run_command riuscito fa scrivere «[OK] exit=…» per un run_command parcheggiato dopo.
  - Aggiungere un test: segno True, poi `_esito_diario` di un run_command parcheggiato o negato.
- **R-428-2 BASSA.** FileNotFoundError o PermissionError su `subprocess.run` in os_with_fallback danno «incerto» anche se il processo non è partito. È l'errore prudente (meglio di «non eseguita» su un'azione partita), ma la dicitura è falsa. Si può restringere distinguendo TimeoutExpired dalle altre eccezioni.
- **R-428-3 BASSA.** Nel loop normale, cioè senza firma, il modello legge solo «Errore eseguendo run_command: … timed out after 60 seconds». La dicitura «esito incerto, verifica prima di ripetere» va solo nel diario, non nella storia.
- **R-428-4 COSMETICA.** Il docstring di applica_firma promette `"stato"` nel risultato, ma i ritorni anticipati (rifiutata, firma non valida, hash, già reclamata, eccezione) non lo impostano. Oggi non rompe niente perché bot.py usa `.get`.

**Rischi esclusi (non verificati)**
- Comportamento su VPS reale con bwrap e un vero timeout di 60 s: ho simulato solo con TimeoutExpired finto, non ho atteso un processo reale.
- pytest tests/ completo (1711 / +85) non rieseguito: il diff tocca solo la suite del kernel e bot.py, che il kernel esercita tramite componi_esito_firma.
- Nota di contesto, non introdotta da questo diff: `str(TimeoutExpired)` mette in storia l'argv bwrap con tutte le `--setenv` (già sanificate dei segreti), quindi testo lungo con variabili d'ambiente non segrete.

**Memoria:** riga #428 e una lezione aggiunte a /home/user/Gas/.claude/agents/memoria_revisore.md, committate con scripts/commit_memoria_revisore.sh (commit 2acb83e). Lo staging del motore è intatto: gas.py, modules/telegram/bot.py e tests/test_unit_kernel.py restano staged.

### Review #429 (chat Motore) — commit be72cb5

## VERDETTO: APPROVATO CON RISERVE

Review #429 (chat Motore). Diff in staging: gas.py, tests/test_unit_kernel.py. Ho letto prima CLAUDE.md (sez. 5), la parte di stato_progetto.md che riguarda R-428 e la mia memoria. Tutte le prove le ho fatte su una copia del tree in staging nello scratchpad, poi cancellata. Copia: **kernel 975 PASS, 0 FAIL**, come il tuo risultato.

**Elementi del diff esaminati**
- `gas.py:4220` — azzera `_run_command_meta` e `_run_command_avviato` all'inizio di ogni tool call di run_turn, prima di gate_classify. Rischio: che l'azzeramento cancelli il meta prima che il diario della stessa chiamata lo legga. La lettura avviene dopo, a `gas.py:4284`, nella stessa iterazione, quindi non succede. Esito: ok. Mutazione (tolte le due righe): T77v FAIL. Sonda sul gemello col solo meta residuo e chiamata parcheggiata: con lo staging il diario dice «[OK] (non eseguito)», con la riga del meta tolta dice «[OK] exit=0 stdout=3 char…». Il gemello è chiuso.
- `gas.py:4033` — nuovo testo d'errore per un run_command partito e poi interrotto. Rischi: conteggi di notte e cancello, il diario, argv in storia. Il testo inizia con «Errore eseguendo» e non con «Operazione negata»: per `gas.py:2050` resta negativo, i rami di `gas.py:4260` e `gas.py:4269` non lo contano come diniego. `_esito_diario` restituisce comunque «[KO] esito incerto: partito ma interrotto» a `gas.py:2068`, perché quel controllo viene prima del controllo «negativo». Non contiene più str(e), quindi niente argv di bwrap. Esito: ok. Mutazione (`if False:`): T77w FAIL, e la storia torna a contenere l'argv di bwrap.
- `gas.py:3926` — FileNotFoundError/PermissionError: il segno torna a False e l'eccezione viene rilanciata. Rischio: un errore di avvio scambiato per «incerto». Sonda con FileNotFoundError: il modello legge «Errore eseguendo run_command: [Errno 2]…», il diario «[KO]», avviato False. Esito: ok, ma la mutazione sopravvive (vedi R-429-1).
- `gas.py:3038` — il dizionario res di applica_firma nasce con "stato": "non_partita". Rischio: un ritorno anticipato senza la chiave. Ok.
- `tests/test_unit_kernel.py:6896` (T77v) e `tests/test_unit_kernel.py:6912` (T77w) — sono test veri: uccidono le mutazioni di R-428-1 (sul segno avviato) e di R-428-3.

**Altri punti che leggono `_run_command_meta`**: fuori da gas.py nessuno (grep su tutto il repo esclusi i test). In gas.py ci sono solo `_esito_diario` e applica_firma, che ha già il suo azzeramento dopo il reclamo a `gas.py:3082`.

**Riserve**
- R-429-1 BASSA: due rami corretti ma senza test.
  - Il rilancio di R-428-2: tolto il `False`, la suite resta 975/0.
  - Il meta residuo su una chiamata parcheggiata: tolto il solo azzeramento del meta, nessun test fallisce, perché T77v passa dal DENY, che è già negativo da sé.
  - Basta un test per ciascuno (FileNotFoundError → diario «[KO]» senza «incerto»; meta residuo + parcheggio → «[OK] (non eseguito)»).
- R-429-2 COSMETICA: il ramo except di `gas.py:4033` guarda solo `_run_command_avviato` e non anche `meta is None`. Un'eccezione arrivata dopo che il meta è stato valorizzato farebbe leggere al modello «INCERTO» mentre il diario dice «[OK] exit=…». In pratica non si raggiunge: dopo il meta c'è solo la concatenazione dell'output.

**Rischio escluso**: non ho verificato il comportamento dentro bwrap reale né su VPS/macOS. Nella copia il sandbox OS mancava e i test giravano in os_with_fallback; inoltre il PermissionError di un exec negato dentro bwrap non si riproduce in dev. In produzione la allowlist è vuota, quindi tutti questi rami restano latenti.

Memoria aggiornata con la riga #429 (nessuna lezione nuova) e committata da sola: 0f458fa, sopra 52b8e00, nessuno dei due pushato. Lo staging di gas.py e tests/test_unit_kernel.py è intatto. File: /home/user/Gas/.claude/agents/memoria_revisore.md

---

## §5 DELTA TEST DEL MOTORE

tests/test_unit_kernel.py: 971 → 975 PASS, 0 FAIL (T77u, T77v, T77w). Blocco reale: `=== RIEPILOGO: 975 PASS, 0 FAIL ===`.
pytest `tests/` (prima di #429): 1711 passed; dopo il merge di main si aggiungono i 85 test web.

## §6 STATO CI

- 521b018 (testa della PR #234, mergiata): unit-suite, handoff-check success; verifica-bot neutral (APPROVATO CON RISERVE).
- b997a5c, c19defc, 40da5ce, be72cb5: run non ancora disponibile alla scrittura dell'handoff (commit nuovi sopra main, non ancora pushati).

## §7 RISERVE APERTE

- R-428-1/2/3/4: chiuse in #429.
- R-429-1 (BASSA): mancano i test dell'errore di avvio (FileNotFoundError) e del meta residuo su un'azione parcheggiata.
- R-429-2 (COSMETICA): il ramo d'errore guarda solo il segno «partito», non anche il meta.
- Riserve precedenti: vedi `reports/stato_progetto.md`.
