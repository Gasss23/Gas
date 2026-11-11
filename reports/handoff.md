# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-11-11 — voce più veloce: connessione verso ElevenLabs riusata (chat M2)

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #372 (https://github.com/Gasss23/Gas/pull/372): con verdetto del bot APPROVATO pulito e CI verde la mergia la chat (regola notturna di M1); con riserve resta pronta per il «mergia» del mattino.

NB: `gh` nel cloud non è autenticato; numero e URL della PR vengono dalla risposta reale dello strumento GitHub MCP `create_pull_request`.

---

## §1 SCOPE & ESITO FETTE

- **Connessione HTTPS verso ElevenLabs tenuta aperta fra le frasi**: `FATTA` (commit di codice nel §3).
- **R-765-1-M2 MEDIA (doppio addebito), R-765-2-M2 MEDIA (connessione ferma), R-765-3-M2 BASSA (test)**: `FATTA` — chiuse prima del commit, review #768-M2.
- **Misura del guadagno sul Mac**: `DEFERITA` — serve la rete vera.
- **Latenza del cervello (prima frase 5-9 s)**: `DEFERITA` — streaming da `claude -p` in `brains/`/`gas.py`, fetta separata.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   3 +++
 modules/voice/tts.py               |  95 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 reports/diff_sessione.md           |  12 +++++-------
 reports/handoff.md                 | n/d
 reports/stato_progetto.md          |   1 +
 reports/ultimo_report.md           |  16 +++++++---------
 tests/test_unit_voice_tts.py       | 166 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
```

NB: regola «n/d» — il conteggio di `reports/handoff.md` non è misurabile mentre lo si scrive; riga di totale tolta.

## §3 GIT LOG --ONELINE (sessione)

```
4f031dc perf(voce): connessione HTTPS verso ElevenLabs tenuta aperta fra le frasi (una per thread, buttata dopo 20 s ferma, niente doppio addebito) — review #765-M2, #768-M2 (chat M2)
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione.

## §4 VERDETTO DEL REVISORE (per commit motore)

### Review #768-M2 (seguito di #765-M2) — verdetto integrale

VERDETTO: APPROVATO

Review #768-M2, seguito di #765-M2, sul diff STAGED in /home/user/Gas-tts: tutte e tre le riserve sono chiuse. Ho controllato solo il delta, i mutanti e la sonda di #765.

**Cosa ho esaminato nel diff**
- `modules/voice/tts.py:139`: `resp.read()` ora sta in un try separato, dopo quello che può riprovare. Un errore durante la lettura chiude la connessione e risale come OSError (`:140-142`). Rischio esaminato: un secondo POST dopo un 200, cioè il doppio addebito di R-765-1-M2. Ho rilanciato la sonda di #765 (connessione che salta a metà dell'audio su una connessione riusata): ora dà `OSError: risposta rotta (ConnectionResetError)` senza nuova richiesta, mentre prima le richieste erano 3 per 2 frasi. Il mutante «read di nuovo nel try che riprova» viene preso dai test (1 failed). **Esito: ok, R-765-1-M2 chiusa.**
- `modules/voice/tts.py:113`: una connessione inattiva da più di `_KEEPALIVE_INATTIVA_MAX_S` = 20 s (`:87`) viene chiusa e se ne apre una nuova, prima di decidere se la connessione è «riusata». Rischio esaminato: una connessione persa in silenzio che fa aspettare tutto il timeout (R-765-2-M2). Il tempo di ultimo uso (`usata`) si aggiorna solo a risposta letta e senza «Connection: close» (`:149`), e una connessione esiste solo dopo un successo, quindi il valore di partenza 0.0 non entra mai in gioco. I mutanti «soglia tolta», «soglia enorme» e «usata non aggiornato» vengono presi dai test (1, 1 e 6 failed). **Esito: ok, R-765-2-M2 chiusa.**
- `modules/voice/tts.py:121-123`: il timeout viene aggiornato sulla connessione e sul socket riusato. Ora i mutanti «settimeout tolto» e «conn.timeout tolto» vengono presi dai test (1 failed ciascuno). **Esito: ok.**
- `modules/voice/tts.py:135-137`: un'eccezione qualsiasi chiude la connessione. Il mutante che toglie il ramo `except BaseException` viene preso dai test (1 failed). **Esito: ok, R-765-3-M2 chiusa.**

**Test**
- `tests/test_unit_voice_tts.py`: 37 passed.
- Mutanti: tutti uccisi (7 sul codice nuovo più la variante «read lasciato anche fuori»).

**Cosa non ho verificato**
- Se 20 s bastano a coprire le pause fra le frasi di una risposta lunga sul server voce, e quanto tiene aperta una connessione inattiva ElevenLabs. Serve una prova dal vivo con chiave e rete vere, che qui non ho.
- Non ho rilanciato le suite voice_server, telegram e contesto: il delta tocca solo tts.py e il suo test.

**Memoria del revisore**
- Ho aggiunto la riga #768-M2, senza lezioni nuove, in /home/user/Gas-tts/.claude/agents/memoria_revisore.md e l'ho messa in staging con `git -C /home/user/Gas-tts add`. Nessun commit.

### Review #765-M2 — verdetto integrale

VERDETTO: APPROVATO CON RISERVE

Review #765-M2 sul diff STAGED in /home/user/Gas-tts, branch perf/voce-tts-keepalive-m2: la connessione HTTPS verso ElevenLabs resta aperta e si riusa, una per thread.

Prima della review ho letto CLAUDE.md (sez. 5, 8, 9 e 10), la memoria del revisore e le voci di stato_progetto che riguardano la voce. La modifica non tocca la storia dei messaggi né `_get_window`, non simula i tool e non indebolisce né il tetto di 10 giri né quello di 8k caratteri. Nessuna eccezione arriva a far crashare il programma: i chiamanti gestiscono già OSError ed ElevenLabsTTSError.

**Cosa ho esaminato nel diff**
- `modules/voice/tts.py:75`: `threading.local()` tiene una connessione per thread. Rischio esaminato: stato o chiave condivisi fra thread. La chiave viaggia nell'header di ogni richiesta e non viene salvata. Il server voce gira su un solo thread (`HTTPServer` senza ThreadingMixIn, `modules/voice/server.py:1517`). Il bot Telegram sintetizza da un esecutore suo (`modules/telegram/bot.py:1017`). Il mutante «connessione globale invece che per thread» viene preso dai test. **Esito: ok.**
- `modules/voice/tts.py:117`: nuovo tentativo solo se la connessione era riusata ed è il primo tentativo. Il mutante «riprova anche su una connessione nuova» viene preso dai test. **Esito: ok.**
- `modules/voice/tts.py:114`: `resp.read()` sta dentro lo stesso try che fa ripartire il tentativo, e `ConnectionResetError` è nella lista degli errori «connessione chiusa». **Esito: riserva R-765-1-M2 (MEDIA), possibile doppio addebito.** Una sonda (connessione finta, nessuna chiamata reale) lo conferma: se la connessione salta a metà dell'audio dopo che ElevenLabs ha già risposto 200, parte un secondo POST, che ElevenLabs farebbe pagare di nuovo. Due frasi hanno prodotto 3 richieste. Correzione: riprovare solo se l'errore arriva prima dello status, cioè durante `request`/`getresponse`. Un errore durante `read()` deve risalire come OSError.
- `modules/voice/tts.py:78`: l'elenco degli errori che fanno riprovare non comprende `TimeoutError`, ed è giusto, perché riprovare raddoppierebbe l'attesa. Però il bot Telegram fa una sola sintesi per risposta, a minuti di distanza, quindi riusa sempre una connessione rimasta ferma a lungo. Se il router, il cambio di Wi-Fi o la sospensione del Mac l'hanno persa senza avvisare, la richiesta aspetta tutto il timeout (`VOCE_TIMEOUT_S`) e fallisce, mentre prima funzionava. La stessa cosa vale per la conferma vocale col suo timeout di 5 s (`modules/voice/server.py:232`). **Esito: riserva R-765-2-M2 (MEDIA).** Correzione: buttare la connessione se è inutilizzata da più di circa 15-30 s. Il guadagno di velocità, che sta fra le frasi di una stessa risposta, resta intatto.
- `modules/voice/tts.py:126`: se il server manda «Connection: close» la connessione si chiude. Il mutante viene preso da `tests/test_unit_voice_tts.py:549`. **Esito: ok.**
- `modules/voice/tts.py:167`: il riuso vale solo senza `_conn_factory` e si spegne con `GAS_TTS_KEEPALIVE=0`. Il percorso vecchio è invariato e lo copre `tests/test_unit_voice_tts.py:559`. **Esito: ok.**
- `modules/voice/tts.py:110`: il timeout viene aggiornato anche sul socket riusato. Il codice è corretto, ma sopravvivono i mutanti «settimeout tolto», «conn.timeout tolto» ed «except BaseException non chiude la connessione», perché nella connessione finta dei test `sock` è sempre None. **Esito: riserva R-765-3-M2 (BASSA), mutanti non coperti.**

**Altre note**
- Socket lasciati aperti: quando un thread muore, la sua connessione viene chiusa dal garbage collector. Entrambi i chiamanti hanno thread che durano, quindi non c'è un accumulo.
- Test: `tests/test_unit_voice_tts.py` dà 33 passed. Mutanti: 3 presi, 3 sopravvissuti (elencati sopra).

**Cosa non ho verificato**
- Il comportamento reale di ElevenLabs: quanto tiene aperta una connessione inattiva e se manda «Connection: close». Serve una chiave e una rete vera, che qui non ho.
- La perdita silenziosa della connessione dopo la sospensione del Mac o un cambio di Wi-Fi. Non si riproduce in questo ambiente; R-765-2-M2 è un ragionamento sul codice, non un caso osservato.
- Non ho rilanciato le suite voice_server, stt, prova_voci, telegram_voce e contesto (428 passed secondo chi mi ha invocato), perché il diff tocca solo tts.py e il suo test.

**Memoria del revisore**
- Ho aggiunto la riga #765-M2 e una lezione nuova in /home/user/Gas-tts/.claude/agents/memoria_revisore.md e l'ho messa in staging con `git add`. Nessun commit, come richiesto.
- La sonda è in /tmp/claude-0/-home-user-Gas/62c50102-54a5-5454-8ce4-94a07d021191/scratchpad/sonda.py.

## §5 DELTA TEST DEL MOTORE

- gas.py non toccato. Test nuovi in `tests/test_unit_voice_tts.py` (11).
- `python -m pytest -q tests/test_unit_voice_tts.py`: 37 passed.
- `python -m pytest -q tests/test_unit_voice_server.py tests/test_unit_voice_stt.py tests/test_unit_voice_prova_voci.py tests/test_unit_telegram_voce.py tests/test_unit_voice_contesto.py -k "audit or not browser"` (prima delle correzioni R-765, che toccano solo tts.py): 428 passed.

## §6 STATO CI

CI NON VERIFICATA con `gh` (non autenticato nel cloud).
- Commit di codice: run non ancora disponibile alla scrittura dell'handoff (pushato prima di aprire la PR #372).
- Commit di fine task: run non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- R-765-1-M2 MEDIA, R-765-2-M2 MEDIA, R-765-3-M2 BASSA: CHIUSE (review #768-M2).
- Non verificato: guadagno reale e durata delle connessioni inattive di ElevenLabs (prova sul Mac).
