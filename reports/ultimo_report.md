# Report — Test di parità app/terminale + suite ermetica rispetto a Telegram (R-c4b1-1, R-c4b1-2)

**Branch:** fix/c4b1-suite-ermetica (nuovo da main `b2a7b34`; tutta la fetta su questo branch)
**Data:** 2026-10-03
**Review:** #130 — APPROVATO CON RISERVE
**Commit:** `d75acc5` (fix), `9377b4b` (memoria revisore)
**PR:** https://github.com/Gasss23/Gas/pull/115 — merge con la variante A: l'agente lancia gasmerge, l'operatore conferma digitando il numero

---

## DECISIONI UMANE RICHIESTE

1. Conferma del merge della PR #115 (https://github.com/Gasss23/Gas/pull/115): l'agente lancia `gasmerge 115` nel pannello terminale, l'operatore digita `115` (oppure INVIO per annullare).
2. Ora si può mettere `TELEGRAM_BOT_TOKEN` e `TELEGRAM_ALLOWED_IDS` in `.env` per il test reale di read-back: la suite non manda più messaggi veri.
3. Da decidere (F-env-app): dall'app Gas gira senza chiavi API, perché `.env` lo esporta solo `~/.zshrc`. Le strade sono due: Gas legge `.env` da sé, oppure i test reali coi provider si fanno sempre da terminale.
4. PR aperte da chiudere senza merge (spetta all'operatore): #109 (superata da #110) e #87 (vecchia certificazione della migrazione al Mac).

---

## STATO ONESTO

| Passo | Esito |
|---|---|
| Test di parità app ↔ terminale | FATTA — capacità identiche; differenze nelle chiavi d'ambiente, nel modello e negli strumenti MCP solo-app (dettaglio sotto). Nessun commit. |
| Scelta della modalità di merge | FATTA — variante A, con "il più autonomamente possibile" per il resto (salvato in memoria) |
| R-c4b1-1 suite ermetica | FATTA — chiusa |
| R-c4b1-2 anteprima link | FATTA — chiusa |
| Test reale Telegram | NON fatto — token ancora assente; ora si può fare in sicurezza |

---

## TEST DI PARITÀ (sonda `sonda_parita.sh` nella scratchpad, sola lettura)

Identico tra app e terminale:
- macchina, utente e cwd;
- PATH, strumenti e versioni: python 3.14.7, git 2.55.0, gh 2.100.0, jq 1.7.1-apple, claude 2.1.288;
- repo, `import gas`, lettura di `.env`;
- rete e autenticazione: ls-remote, push --dry-run, gh keyring, api.github.com 200, api.telegram.org 302;
- suite: 552/5 e 232;
- **gate di review**: commit senza marcatore BLOCCATO in entrambi;
- subagent (incluso revisore), skill `/fine-task`, MEMORY.md, CLAUDE.md.

Diverso:
1. **Chiavi API nell'ambiente.** Le chiavi API (GEMINI, GROQ, ELEVENLABS, GAS_VOICE_TOKEN) sono presenti da terminale e assenti dall'app. Il motivo è `~/.zshrc` riga 4: `set -a; source ~/Gas/.env`, che vale solo per le zsh interattive. `gas.py` non carica `.env` da solo.
2. **Modello.** Da terminale vale Sonnet 4.6, il pin di `.claude/settings.json`; l'operatore l'ha cambiato con `/model`. Nell'app gira Opus 5.5.
3. **Strumenti solo nell'app:** browser pane, pannello terminale, simulatore iOS, Chrome, computer-use, `ccd_*`.
4. TERM/LANG: `dumb`/non impostata nell'app, `xterm-256color`/`C.UTF-8` da terminale.

Nota: l'agente da terminale ha eseguito il prompt due volte, con risultati identici.

## FIX

- `tests/test_unit_kernel.py`, in testa al file:
  - pop di `TELEGRAM_BOT_TOKEN`/`TELEGRAM_ALLOWED_IDS`;
  - `bot._tg_post` sostituito da `_tg_post_vietato`, che registra la chiamata e lancia;
  - guardia su `urllib.request.urlopen` verso api.telegram.org, che blocca e conta senza mai registrare il token.

  I test che vogliono un invio riuscito installano `_TgFinto`, che poi ripristina il trasporto che vieta.
- `modules/telegram/bot.py` `invia_read_back`: aggiunto `"link_preview_options": {"is_disabled": True}` al payload. `parse_mode` resta assente.

## TEST

- Suite kernel: **552 → 558 PASS / 5 FAIL** (F-mac-1 invariati). Nuovi T76a-d, più un check nuovo in T75c.
- pytest (escluso kernel/e2e): 232 passed.
- **Misura indipendente** con un `sitecustomize` che conta gli urlopen verso api.telegram.org, e `TELEGRAM_BOT_TOKEN=finto TELEGRAM_ALLOWED_IDS=999` esportati:
  - suite di main → **40** chiamate;
  - suite corretta → **0**.
- CI sul commit `9377b4b`: success (561+6 = 567 PASS, 0 FAIL su ubuntu; hook 56, voice 19, gate 74).
- **Test esistente modificato:** T75c. Prima `set(payload) == {"chat_id","text"}`, ora `== {"chat_id","text","link_preview_options"}`, più un check sul valore `{"is_disabled": True}`. Motivo: R-c4b1-2. Il revisore lo giudica legittimo: l'uguaglianza resta esatta.

## RISERVE (review #130)

- **R-erm-1** (minore): l'isolamento vale solo in `tests/test_unit_kernel.py`.
- **R-erm-2** (cosmetica): la guardia copre solo urllib.

## ANOMALIE

- Il verdetto #130 citava `bot.py:135`/`:52` col nome corto e `gas.py:23`, un file fuori dal diff: `check_verdetto.py` li avrebbe scartati. Applicando il precedente scelto dall'operatore per la review #129, ho chiesto subito al revisore una riemissione: solo la forma delle citazioni, merito invariato. L'handoff §4 contiene la riemissione verbatim.
- Nella sonda di parità il primo lancio è fallito per un apostrofo nel messaggio d'errore della riga 7 (errore di sintassi bash). L'ho corretto e rilanciato prima di qualunque confronto.
