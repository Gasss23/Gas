# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-10-03 — Test di parità app/terminale + suite ermetica rispetto a Telegram (R-c4b1-1, R-c4b1-2), branch `fix/c4b1-suite-ermetica`

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #115 (https://github.com/Gasss23/Gas/pull/115) — variante A: l'agente lancia `gasmerge 115`, l'operatore conferma digitando `115`.
2. Ora si può mettere il token Telegram in `.env` per il test reale di read-back.
3. F-env-app: dall'app Gas gira senza chiavi API (`.env` lo esporta solo `~/.zshrc`). Decidere se Gas debba caricare `.env` da sé.
4. PR #109 e #87 da chiudere senza merge (spetta all'operatore).

---

## §1 SCOPE & ESITO FETTE

- **Test di parità app ↔ terminale**: `FATTA` — capacità identiche (gate BLOCCATO in entrambi); differenze: chiavi API in env (solo terminale), modello, MCP solo-app, TERM/LANG. Nessun commit.
- **Scelta modalità di merge**: `FATTA` — variante A + massima autonomia (memoria).
- **R-c4b1-1 suite ermetica**: `FATTA` — 40 → 0 chiamate verso Telegram con token esportato.
- **R-c4b1-2 anteprima link**: `FATTA`.
- **Test reale Telegram**: `DEFERITA — token ancora assente in .env (ora sicuro aggiungerlo)`.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   2 +
 modules/telegram/bot.py            |   8 ++-
 reports/diff_sessione.md           |  10 +--
 reports/handoff.md                 | 138 ++++++++-----------------------------
 reports/stato_progetto.md          |  12 +++-
 reports/ultimo_report.md           |  85 +++++++++++++----------
 tests/test_unit_kernel.py          |  68 +++++++++++++++++-
 7 files changed, 167 insertions(+), 156 deletions(-)
```

## §3 GIT LOG --ONELINE (sessione)

```
9377b4b chore(revisore): memoria review #130 — APPROVATO CON RISERVE
d75acc5 fix(c4b1): suite ermetica rispetto a Telegram (R-c4b1-1) + anteprima link disattivata nel read-back (R-c4b1-2) — review #130 APPROVATO CON RISERVE
```

## §4 VERDETTO DEL REVISORE (per commit motore)

Commit `d75acc5` — review #130 — verdetto INTEGRALE incollato.

Nota (dell'agente principale, fuori dal verdetto): questa è la **riemissione** del revisore, chiesta applicando il precedente scelto dall'operatore per la review #129: la prima versione citava i file col solo nome e un file fuori dal diff, forme che `check_verdetto.py` scarta. Il revisore ha cambiato solo la forma delle citazioni; esito, elementi e riserve sono invariati. Il testo NON è stato ritoccato dall'agente principale.

## Verdetto review #130: APPROVATO CON RISERVE

Le riserve R-c4b1-1 (suite non ermetica) e R-c4b1-2 (anteprima dei link nel read-back) sono chiuse. Il commit è consentito.

**Cosa ho verificato.** Ho fatto girare la suite con `TELEGRAM_BOT_TOKEN=finto TELEGRAM_ALLOWED_IDS=999` esportati:
- risultato: 558 PASS / 5 FAIL, cioè i soliti F-mac-1;
- T76a-d tutti PASS;
- T76c conferma che gli urlopen verso Telegram sono 0.

Nel progetto `dotenv` non compare in gas.py, brains/, modules/ e tests/: nessuna reimportazione di `.env` che possa rimettere le variabili Telegram nell'ambiente dopo il pop.

### Elementi del diff esaminati
1. `tests/test_unit_kernel.py:27-44`: in testa al file toglie TELEGRAM_* dall'ambiente, sostituisce `bot._tg_post` con `_tg_post_vietato` e mette una guardia su `urllib.request.urlopen` che registra solo l'host, mai il token.
   - Rischio esaminato: il blocco si aggira se gas.py o bot.py si legano al trasporto con un `from ... import`.
   - Esito: **ok**. gas.py, riga 23, importa il modulo (`_tg_bot`). `modules/telegram/bot.py:135` risolve `_tg_post` come attributo del modulo e `modules/telegram/bot.py:52` risolve `urllib.request.urlopen` allo stesso modo, quindi le sostituzioni hanno effetto. `_TgFinto` (`tests/test_unit_kernel.py:4824-4828`) salva il trasporto in uso e lo ripristina, quindi si torna a quello che vieta.
2. `tests/test_unit_kernel.py:5887-5919`, test T76a-d.
   - Rischio esaminato: test che passano senza mordere davvero.
   - Esito: **ok**, verificato a ragionamento, non con una mutation eseguita. Se si toglie la riga 36, il trasporto reale chiama la guardia urlopen. Questa lancia un'eccezione che il `except Exception` di `_tg_post` assorbe, quindi `_TG_TENTATIVI` non cresce e T76a e T76b cadono. T76c copre la seconda linea di difesa.
3. `modules/telegram/bot.py:136-140`: aggiunge `"link_preview_options": {"is_disabled": True}` al sendMessage del read-back.
   - Rischio esaminato: la chiamata si rompe oppure finisce fuori dal try fail-safe.
   - Esito: **ok**. Il codice resta dentro il try/except di `invia_read_back` (§9) e `parse_mode` resta assente.

### Giudizio sul test esistente modificato (T75c, `tests/test_unit_kernel.py:5750-5755`)
L'adeguamento è legittimo:
- resta un confronto a **uguaglianza esatta**, non un sottoinsieme: si aggiunge solo la chiave richiesta dalla riserva e l'allowlist anti-`parse_mode` non si indebolisce;
- c'è un check nuovo sul **valore** `{"is_disabled": True}`, quindi un payload con `False` o senza la chiave fa fallire il test.

### Riserve
- **R-erm-1 (minore):** la protezione vale solo dentro `tests/test_unit_kernel.py`. Gli altri file pytest/e2e e i `python -c` lanciati da un terminale con `.env` esportato non sono protetti, se un giorno attraversano il cancello. Va tracciata in stato_progetto.md.
- **R-erm-2 (cosmetica):** la guardia di rete copre solo `urllib.request.urlopen`. Oggi basta perché bot.py usa solo urllib. Un trasporto futuro, per esempio `http.client` o `requests`, non sarebbe intercettato.

### Rischi esplicitamente non verificati
- **Invio reale verso Telegram:** non verificato perché non ci sono credenziali reali, ed è quello che ci si aspetta. Non ho visto l'anteprima effettivamente disattivata su un client Telegram: so solo che il payload è conforme alla Bot API.
- **Suite pytest (232 passed):** non l'ho rilanciata, mi baso sulla tua misura.

### Memoria del revisore
Ho aggiunto la riga contatore #130 e una lezione datata (allowlist esatta adeguata: mantenere l'uguaglianza esatta e aggiungere un check sul valore) in `/Users/gas/Gas/.claude/agents/memoria_revisore.md`. Come richiesto, il file **non è committato**. In questa riemissione non ho toccato nessun file del repo.

Riemissione: solo forma delle citazioni, merito invariato.

## §5 DELTA TEST DEL MOTORE

Suite kernel (macOS): **552 PASS / 5 FAIL → 558 PASS / 5 FAIL** (+6: T76a ×2, T76b, T76c, T76d, T75c anteprima). I 5 FAIL sono F-mac-1 (T11c2, T11e, T12a, T12c, T12e), identici prima e dopo, fuori scope (bwrap assente su macOS).

```
=== RIEPILOGO: 558 PASS, 5 FAIL ===
```

Misura indipendente con `sitecustomize` che conta gli urlopen verso api.telegram.org, con `TELEGRAM_BOT_TOKEN=finto TELEGRAM_ALLOWED_IDS=999` esportati: suite di main → 40; suite corretta → 0.
pytest (escluso kernel/e2e): 232 passed prima e dopo.
Test esistente modificato: T75c (allowlist del payload estesa a `link_preview_options`, uguaglianza esatta mantenuta, più un check sul valore). Il revisore lo giudica legittimo.

## §6 STATO CI

```
completed	success	chore(revisore): memoria review #130 — APPROVATO CON RISERVE	CI	fix/c4b1-suite-ermetica	push	37114537792	49s	2026-10-03T09:53:00Z
completed	success	Merge pull request #114 from Gasss23/fix/gate-review-jq	CI	main	push	37088739700	55s	2026-10-03T02:08:32Z
completed	success	docs(gate-review): report — anomalia check_verdetto e riemissione del…	CI	fix/gate-review-jq	push	37088635501	53s	2026-10-03T02:06:38Z
```

Mappatura commit → run:
- `9377b4b` (testa del push) → run success su headSha `9377b4b9c7fef589158e5afd4c77f73c2e9e02d7`. Log: `=== RIEPILOGO: 567 PASS, 0 FAIL ===`; hook 56, voice 19, gate 74 passed.
- `d75acc5` → nessuna run su questo SHA (pushato insieme a `9377b4b`; il suo albero è incluso in quello testato).
- Commit di fine-task (questo handoff): run non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- **R-erm-1** (minore): l'isolamento da Telegram vale solo in `tests/test_unit_kernel.py`.
- **R-erm-2** (cosmetica): la guardia copre solo urllib.
- **F-env-app**: dall'app le chiavi di `.env` non sono nell'ambiente.
- Ancora aperte: R-c4b1-3, R-c4b1-4, R-gjq-1..3 (vedi stato_progetto.md).
