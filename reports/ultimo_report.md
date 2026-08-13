# Ultimo Report — FASE 3 Fetta 1: endpoint HTTP voice

**Data:** 2026-08-13
**Branch:** fase3/voice-endpoint
**Task:** Scrivere l'endpoint HTTP locale in WSL che avvolge GasKernel (FASE 3, Fetta 1)

---

## §SCOPE & ESITO

**Scope:** endpoint HTTP `POST /voice` con autenticazione bearer, zero nuove dipendenze, kernel istanziato una volta, suite di test reali (18 test), aggiunta alla CI.

**Esito:** ✅ COMPLETATO. Fetta 1 chiusa su tutti i requisiti.

---

## File creati / modificati

| File | Azione |
|---|---|
| `modules/voice/__init__.py` | NUOVO — package marker |
| `modules/voice/server.py` | NUOVO — endpoint HTTP (172 righe) |
| `tests/test_unit_voice_server.py` | NUOVO — suite pytest (18 test) |
| `.github/workflows/ci.yml` | MODIFICATO — aggiunto step voice suite |

**File NON toccati:** `gas.py`, `brains/`, `modules/memory/`, `modules/telegram/` — stop gate rispettati.

---

## Requisiti coperti

| Requisito | Esito |
|---|---|
| Bind 127.0.0.1 di default, apribile via GAS_VOICE_BIND | ✅ |
| GAS_VOICE_TOKEN obbligatorio, fail-closed all'avvio | ✅ |
| Confronto token `hmac.compare_digest` (tempo costante) | ✅ |
| Log AUTH FAIL con IP, MAI il token nei log | ✅ |
| Kernel istanziato una volta all'avvio | ✅ |
| Single-thread stdlib `http.server.HTTPServer` | ✅ |
| Zero nuove dipendenze | ✅ |
| Fail-safe §9: eccezione run_turn → 500, server vivo | ✅ |
| Zero valori inchiodati nel codice | ✅ |
| Solo `POST /voice` funzionale, altri verbi 405 | ✅ |

---

## Suite di test reali — 18 PASS, 0 FAIL

```
TV1: avvio senza token → exit 1         PASS
TV2a: no auth header → 401              PASS
TV2b: no auth → kernel non invocato     PASS
TV3a: token errato → 401               PASS
TV3b: token errato loggato, niente segreto nei log  PASS
TV4a: token corretto → 200 + content   PASS
TV4b: tool_res silenti nella risposta  PASS
TV5a: eccezione run_turn → 500         PASS
TV5b: server vivo dopo eccezione       PASS
TV6: kernel stesso oggetto per N req   PASS
TVExtra ×4 (400/405/error-event)       PASS
unit _token_ok ×4                      PASS
```

Suite kernel: **276 PASS, 0 FAIL** (invariata, nessuna regressione).

---

## Diff reale (stat)

```
.github/workflows/ci.yml              | +30
modules/voice/__init__.py             | +0 (file vuoto)
modules/voice/server.py               | +172
tests/test_unit_voice_server.py       | +323
```

---

## Verdetto revisore #74 (APPROVATO CON RISERVE) — integrale

> Il diff di FASE 3 Fetta 1 (endpoint HTTP voice) è approvato con due riserve non bloccanti:
>
> **R1 (minore)** — `modules/voice/server.py:85`: `int(self.headers.get("Content-Length", 0) or 0)` non cattura `ValueError` per header non numerici (es. `Content-Length: abc`). Il server sopravvive ma il client riceve EOF invece di un 400 controllato. Fix raccomandato prima del deploy su VPS: avvolgere in `try/except ValueError` con risposta 400 esplicita.
>
> **R2 (cosmetica)** — `tests/test_unit_voice_server.py:81–83`: variabili `rc` e `result` assegnate e mai usate; `monkeypatch.delenv` + `os.environ.pop` ridondanti. Il test è corretto e passa, ma il codice è disordinato.
>
> Nessuna violazione dei guardrail critici: nessun slicing history, nessuna simulazione tool, §9 rispettato (except+log in do_POST), cap 10 iter delegato correttamente al kernel, stop gate rispettati (gas.py/brains/modules esistenti non toccati). Le riserve R1 e R2 vanno tracciate in `reports/stato_progetto.md`.

---

## Verdetto revisore #75 (APPROVATO) — integrale

> **Oggetto:** ri-review post-fix delle riserve R1 e R2 di review #74 (FASE 3 Fetta 1, `modules/voice/server.py` + `tests/test_unit_voice_server.py`).
>
> **`modules/voice/server.py:85-89`** — try/except ValueError attorno a `int(...)` — rischio: Content-Length non numerico provocava EOF al client senza risposta HTTP controllata (violazione fail-safe §9) — esito: **CHIUSA R1**. Il blocco è corretto: la guard `or 0` gestisce già il caso di header vuoto/None prima della conversione; il ValueError su valori tipo "abc" ora produce `_send_json(400, {"error": "Content-Length non valido"})` seguito da `return`, lasciando il server in piedi.
>
> **`tests/test_unit_voice_server.py:79-84`** — `test_tv1_no_token_refuses_start` riscritto con `monkeypatch.delenv` + `capsys` — rischio: dead code e assenza di asserzione su stdout — esito: **CHIUSA R2**. Il test usa correttamente le fixture pytest, asserisce `code == 1` e verifica che `"GAS_VOICE_TOKEN"` compaia in `captured.out`.
>
> Entrambe le riserve sono chiuse. La suite a 18 PASS confermata è coerente con le modifiche. Il commit può procedere.

---

## Proposte fuori scope (da decidere come prossime fette)

1. **`gas voice` CLI entry in gas.py** — integrazione del comando `gas voice` nella CLI principale (analogia: `gas telegram`). Richiede toccare gas.py → fuori scope Fetta 1, proposta per Fetta 2.
2. **Test Content-Length non numerico** — TVExtra potrebbe coprire il caso `Content-Length: abc` ora che R1 è chiusa. Piccola aggiunta ai test, nessun blocco.
3. **TLS / esposizione pubblica VPS** — esplicitamente fuori scope per questa fetta.
4. **Client Windows / STT / TTS / wake word** — fette successive.
