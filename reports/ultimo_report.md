# Report C4b-1 — Notifica Telegram di read-back + anti-doppioni

**Branch:** feat/cancello-c4b1 (nuovo da main aggiornato `4284a9c`; tutta la sessione su questo branch)
**Data:** 2026-10-03
**Review:** #128 — APPROVATO CON RISERVE
**Commit:** `b8bf2ef` (revisore su Opus), `db964b2` (motore), `e3b8459` (memoria revisore)
**PR:** https://github.com/Gasss23/Gas/pull/113 — merge vietato all'agente (lo fa l'operatore con gasmerge)

---

## DECISIONI UMANE RICHIESTE

1. Merge della PR #113 (https://github.com/Gasss23/Gas/pull/113) con gasmerge.
2. Test manuale reale Telegram NON fatto: in `.env` e nell'ambiente non ci sono `TELEGRAM_BOT_TOKEN` né `TELEGRAM_ALLOWED_IDS`. Per farlo vanno aggiunti a `.env`. Prima di aggiungerli va chiusa R-c4b1-1 (vedi sotto): con il token esportato, la suite manda read-back reali.

---

## STATO ONESTO

**C4b-1 fatto, C4b-2 (bottoni + esecuzione) NON fatto, deploy autonomo ancora vietato.**

| Passo | Esito |
|---|---|
| PASSO 0 — revisore su Opus | FATTA — `model: opus` nel frontmatter di `.claude/agents/revisore.md`, commit separato `b8bf2ef` (solo quel file) |
| PASSO 1 — sonda | FATTA — nessun conflitto bloccante (dettaglio sotto) |
| PASSO 2 — anti-doppioni + tetto | FATTA |
| PASSO 3 — read-back (solo invio) | FATTA |
| PASSO 4 — R-c3-3 e R-c3-4 | FATTA — chiuse |
| Test a)–g) | FATTA — T75a-f (51 check) + regressione T74a-g verde |
| Test manuale reale Telegram | NON fatto — token e ID assenti in `.env` e nell'ambiente |
| Bottoni/callback, esecuzione post-approvazione, worker di scadenza, tetto CRM C-d | FUORI SCOPE — non toccati |

---

## PASSO 1 — Sonda (file:riga sul codice di partenza `4284a9c`)

- Design: `reports/design_cancello.md:211` §4b (flusso turno suddiviso, passo 3 = messaggio Telegram), `:259` §4c (read-back integrale, oltre ~4096 → niente invio + diniego "argomenti troppo grandi per un read-back integrale"), `:291` §4e (TELEGRAM_ALLOWED_IDS, token monouso, stato immutabile), `:298` §4f (niente re-invio automatico, contro lo spam).
- Punto di enqueue: `gas.py:1946` (ramo IRREVERSIBLE / UNCERTAIN+contaminata), `gas.py:1952` (`self.memory.enqueue_approval(...)`), `gas.py:1984` (esecuzione normale).
- Bot: `modules/telegram/bot.py:40` `_tg_post` (urllib, non lancia mai, ritorna None in caso di errore), `:62` `_send_text` (TRONCA a 4096 → NON riusabile per il read-back, che non deve mai troncare: ho riusato `_tg_post`).
- Store: `modules/memory/store.py:1430` `enqueue_approval`, `:1505` `resolve_approval`, `:1524` (controllo su 'approved').

Confronto design ↔ prompt — nessuna contraddizione:
- §4b prevede i bottoni nel messaggio; il prompt li esclude in questa fetta. È un taglio dello scope, non un conflitto.
- "Revocata": nello schema non esiste uno stato 'revoked'. Lo stato terminale coerente con §4a è `rejected` con `risolto_da='kernel_revoca'`, già usato da C3 per gli args manomessi.
- Tensione segnalata, non bloccante: il test esistente T73a ("stessa azione accodata due volte → due UUID distinti, §8d") descrive la primitiva C3. §8d vieta di accorpare azioni DIVERSE in una firma; non vieta di deduplicare la STESSA azione ancora pending. Per questo ho lasciato `enqueue_approval` senza dedup e messo la dedup in un metodo nuovo usato dal loop.

---

## PASSO 2 — Anti-doppioni e tetto

- `modules/memory/store.py:1512` `accoda_approvazione(...)` → `(esito, id)` con esito `nuova` / `doppione` / `tetto` / `errore`. È ATOMICA: `BEGIN IMMEDIATE`, poi query del doppione, COUNT per il tetto e INSERT nella stessa transazione.
- Doppione = 'pending' NON scaduta con stesso `tool_name` e stesso `tool_args_hash`. In quel caso non viene creata nessuna riga, non parte nessun messaggio e al modello torna lo stesso ID ("Azione già in attesa di approvazione umana (ID: …)"). Il doppione si controlla PRIMA del tetto: ripetere un'azione già in coda non viene negato nemmeno a tetto pieno.
- Tetto: 'pending' non scadute >= `GAS_APPROVAL_MAX_PENDING` (default 5; un valore non valido dà WARN e default) → diniego "Operazione negata: troppe azioni in attesa di firma.", senza riga e senza messaggio.
- `enqueue_approval` (primitiva C3) resta invariata, senza dedup. Validazione degli args fattorizzata in `_serializza_args`.

## PASSO 3 — Read-back (solo invio)

- `gas.py:1246` `_parcheggia_e_notifica`: accoda, rilegge la riga dal DB (`get_approval`, args salvati e non quelli del modello), compone il testo, controlla la lunghezza, invia. Il tool non viene mai eseguito.
- `modules/telegram/bot.py:101` `componi_read_back`: testo semplice con azione_leggibile del kernel, Tool, "ARGOMENTI (testo grezzo, può contenere testo di terzi):" + `tool_args_json` integrale, ID approvazione, Scadenza, e una nota che i bottoni non sono ancora attivi.
- `modules/telegram/bot.py:118` `invia_read_back`: `sendMessage` via `_tg_post` con payload `{chat_id, text}`, SENZA parse_mode. L'invio è riuscito se almeno un ID risponde `ok=True`. Lunghezza contata in unità UTF-16 come fa Telegram; il confine 4096 è incluso.
- Oltre 4096, token/ID mancanti, invio fallito o eccezione → `revoca_approval` (`store.py:1686`: solo rejected/kernel_revoca), diniego al modello, WARN in gas_debug.log. Il testo delle eccezioni NON torna al modello, perché potrebbe contenere l'URL col token.
- Scelta: il kernel revoca con un metodo dedicato `revoca_approval` e non con `resolve_approval`. Così l'invariante T73f ("gas.py non invoca resolve_approval") resta vero e non ho modificato T73f.
- Diario: tutti i percorsi del cancello (`pending id=`, `pending-doppione id=`, `revocata id=`, `tetto-pending`, `gate-fail-closed`) scrivono solo nome tool + id, mai args. Prima il ramo fail-closed scriveva il riassunto degli args.
- `parse_allowed_ids` estratto in bot.py e riusato da `run_bot`, con comportamento invariato.

## PASSO 4 — R-c3-3 / R-c3-4

`store.py` `resolve_approval`: 'approved' solo con `risolto_da == "telegram_user"` e `telegram_user_id` int (bool escluso); 'rejected' con `telegram_user_id` int o None. Altrimenti `(False, msg)` prima di aprire il DB, quindi senza scritture. **R-c3-3 e R-c3-4 CHIUSE.**

---

## TEST

Suite `tests/test_unit_kernel.py`: **prima 501 PASS / 5 FAIL → dopo 552 PASS / 5 FAIL**. I 5 FAIL sono gli stessi prima e dopo: F-mac-1 (T11c2, T11e, T12a, T12c, T12e, bwrap assente su macOS).
pytest (escluso test_unit_kernel.py, e2e): **227 passed prima e dopo**.

Nuovi test T75 (SQLite vero; per Telegram è sostituito SOLO `bot._tg_post` con un finto trasporto che registra il payload):
- a) doppione identico (iterazioni successive e due chiamate nello stesso messaggio) → 1 riga, 1 invio, stesso ID ×4; a livello store: args o tool diversi → nuova; dopo revoca/scadenza → nuova.
- b) tetto 2 via env → terza richiesta negata, nessuna riga, nessun invio; doppione a tetto pieno → stesso ID; default 5 → la sesta è 'tetto'; le pending risolte non contano; env non valido → 5.
- c) payload: un solo sendMessage al chat_id, chiavi esattamente `{chat_id, text}` (niente parse_mode), args integrali con caratteri Markdown/HTML, etichetta, ID e scadenza presenti; diario senza args.
- d) oltre 4096 → 0 invii, riga rejected/kernel_revoca, diniego "argomenti troppo grandi per un read-back integrale", tool non eseguito; confine 4096 ammesso e 4097 no; emoji = 2 unità.
- e) token mancante, ID mancanti, invio che lancia, risposta ok=False → riga revocata, diniego, tool non eseguito, token mai nell'esito; WARN nel log; con due ID di cui uno fallito → resta pending.
- f) R-c3-3/R-c3-4: casi validi e non validi, con stato del DB invariato nei casi negati.
- g) T74a-g: 21/21 PASS.

Mutazioni (ciascuna applicata e poi ripristinata): dedup disattivato → 6 FAIL (T75a/b); revoca disattivata → 6 FAIL (T75d/e); parse_mode aggiunto → 1 FAIL (T75c).

**Test ESISTENTI modificati** (esaminati dal revisore, giudicati "adeguamento LEGITTIMO, non li indebolisce"):
- T70f, T70g, T72c, T74a, T74b: aggiunto `with _TgFinto():` attorno a `run_turn_scriptato`. Motivo: senza un invio riuscito la richiesta ora viene revocata (comportamento voluto); questi test verificano il percorso "pending" e hanno bisogno di un read-back consegnato. Asserzioni invariate.
- T74e: monkeypatch spostato da `memory.enqueue_approval` a `memory.accoda_approvazione`. Motivo: il kernel ora accoda con quel metodo; lasciato com'era, il test sarebbe diventato vuoto. Asserzioni invariate.

**Test manuale reale:** NON fatto. Motivo: `.env` contiene solo GROQ/ELEVENLABS/GAS_VOICE_TOKEN/GEMINI; né `.env` né l'ambiente hanno `TELEGRAM_BOT_TOKEN` o `TELEGRAM_ALLOWED_IDS`. Nessun messaggio è partito.

---

## RISERVE (review #128)

- **R-c4b1-1** (da chiudere prima del deploy e prima di mettere il token in `.env`): la suite non è ermetica. Con il token reale esportato, circa 40 sendMessage reali partono dai test esistenti che passano dal cancello (run_command T11/T12). Oggi è innocuo perché il token è assente.
- **R-c4b1-2** (minore): anteprima dei link non disabilitata nel read-back.
- **R-c4b1-3** (minore): l'invio è sincrono nel turno, 15 s × N ID nel caso peggiore.
- **R-c4b1-4** (minore, fail-closed): una riga corrotta con ts_expiry TEXT conta nel tetto e nel doppione.

## FINDING REGISTRATI (verifica C4a, in stato_progetto.md)

- **F-c4a-eco**: T70f/T70g riscritti in C4a, quindi il controllo eco del diario per run_command nel giro completo non esiste più → da ripristinare in C4b-2 sul percorso post-approvazione.
- **R-c4a-1 sottostimata**: il limite non è 9 (più chiamate per messaggio e tra turni) → ora coperta da anti-doppioni + tetto.
- **Handoff C4a §6 errato**: "branch non pushato" era falso; la CI gira su ubuntu, non su macOS.
- **R-c3-1b**: controprova più debole del richiesto → "mitigata", non "chiusa".
- **scrivi_rep.sh su main** lascia `reports/ultima_risposta.md` modificato e non committato.
- **Messaggio SessionEnd** che dice ancora "Auto-commit..." (cosmetico).
- **/agents rimosso da Claude Code**: il controllo del revisore ora si fa chiedendo l'elenco dei subagent disponibili.

## ANOMALIE

- Nel corso del lavoro una mia patch ha trasformato i `\n` di `componi_read_back` in a-capo reali (SyntaxError). L'ho corretta prima di qualunque commit; la suite finale gira sul codice corretto.
