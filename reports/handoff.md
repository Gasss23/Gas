# Handoff sessione — 2026-09-01

**Branch**: fix/chiusura-f1-calcola-2026-09-01  
**Tipo**: Certificazione chiusura finding F1 CRITICO (zero modifiche al motore)

---

## §DECISIONI UMANE RICHIESTE

**Nessuna decisione bloccante.** Il finding F1 è chiuso, la suite è verde, il revisore ha approvato.

Suggerimenti non urgenti:
- Valutare aggiornamento VPS a commit attuale (FASE 3 completa mancante, VPS stantio al `f3a8acc` 2026-06-29).
- Prima del deploy VPS: rotare chiave ElevenLabs (ATTESTATO SUP. 2026-08-22, ancora aperto).

---

## §Esito sonda E2E

**Sonda su ENTRAMBI i provider con history temporanea isolata — 4 PASS su 4**

| Provider | Brain effettivo | T1 "sette per otto" | T2 "radice di 144" |
|----------|----------------|---------------------|---------------------|
| Gemini (GEMINI_API_KEY only) | gemini-flash (flash-lite 429 quota) | `calcola("7*8")→56` PASS | `calcola("math.sqrt(144)")→12.0` PASS |
| Groq (GROQ_API_KEY only) | groq (MODEL_GROQ) | `calcola("7*8")→56` PASS | `calcola("math.sqrt(144)")→12.0` PASS |

**Nota Gemini-flash-lite**: 429 RESOURCE_EXHAUSTED (quota gratuita giornaliera 20 RPD esaurita). Il paracadute ha funzionato: fallback su gemini-flash corretto.

---

## §git diff --stat (sessione)

```
 .claude/agents/memoria_revisore.md | 1 +
 1 file changed, 1 insertion(+)
```

(commit `fc211db` — revisore memoria review #95, già pushato)

Report di sessione: `reports/ultimo_report.md`, `reports/stato_progetto.md`, `reports/diff_sessione.md`, `reports/handoff.md` — nel commit successivo.

---

## §git log commits sessione

```
fc211db chore(revisore): memoria review #95 — APPROVATO
```

---

## §Delta test motore

| Suite | Precedente | Questa sessione | Delta |
|-------|-----------|-----------------|-------|
| test_unit_kernel.py | 299 PASS, 0 FAIL | 299 PASS, 0 FAIL | 0 (invariata) |

Nessuna modifica al motore → nessun nuovo test aggiunto. Suite stabile.

---

## §Verdetto revisore INTEGRALE (Review #95 — APPROVATO)

> Commit `fc211db` confermato.
>
> ## VERDETTO FINALE — Review #95
>
> **APPROVATO**
>
> ### Verifica esplicita dei tre punti richiesti
>
> **(a) `_GAS_SYSTEM_PROMPT_BASE` — direttiva calcoli**
> `gas.py:49-50` — ordina esplicitamente `calcola()` per calcoli aritmetici ("Per CALCOLI ARITMETICI usa SEMPRE calcola()"), con esempi `calcola('7*8')` e `calcola('math.sqrt(144)')`. La vecchia direttiva errata che ordinava `run_command` per "conteggi, misure e calcoli esatti" (F1 CRITICO, riga originale 46-48) **non è più presente**. `gas.py:51` delimita run_command a "CONTEGGI E MISURE SU FILE", scope corretto e separato. Nessun'altra riga del prompt risulta anomala: la lista tool a riga 42-44 è completa (7 tool), il contratto anti-simulazione a riga 44-46 è integro.
>
> **(b) `SHELL_ALLOWLIST` — assenza calcolatori**
> `gas.py:992-996` — `SHELL_ALLOWLIST = frozenset({"ls", "cat", "head", "tail", "wc", "grep", "echo", "pwd", "date", "stat", "file", "uniq", "cut", "tr", "nl", "diff", "comm", "true", "false", "basename", "dirname", "printf", "seq", "rev"})`. Nessun calcolatore presente: `bc`, `python`, `expr`, `awk`, `perl` sono assenti. **Nessuna violazione di sicurezza**.
>
> **(c) Guardrail di sicurezza — nessun indebolimento**
> `SHELL_ENV_SENSITIVE_MARKERS` (riga 1001) intatto. Sandbox bwrap (riga 1013+) intatto. Costanti anti-DoS di `calcola()` (`_CALCOLA_MAX_EXP`, `_CALCOLA_MAX_DIGITS`, `_CALCOLA_MAX_FACTORIAL`, righe 70-72) intatte. Schema tool (`tools_schema`, righe 508-514) coerente con system prompt e implementazione.
>
> **Rischio esplicitamente escluso**: comportamento dei provider alternativi (Groq, OpenRouter, Ollama) quando ricevono il system prompt aggiornato in turno reale — non verificabile in questa sessione senza chiavi API attive su quei rung. Il CAVEAT (ii) di stato_progetto.md (comportamento Groq contraddittorio) resta finding aperto distinto.
>
> File rilevanti verificati:
> - `/home/gqual/Gas/gas.py` (righe 40-60 e 992-996)
> - `/home/gqual/Gas/reports/stato_progetto.md`
> - `/home/gqual/Gas/.claude/agents/memoria_revisore.md`

---

## §Stato CI (ultimo run su main)

| Run ID | Branch | Data | Stato |
|--------|--------|------|-------|
| 33541870284 | main | 2026-09-01T18:08:22Z | **SUCCESS** ✅ |
| 33327010358 | main | 2026-08-30T18:04:19Z | SUCCESS ✅ |
| 33262188110 | main | 2026-08-29T16:09:26Z | SUCCESS ✅ |

CI FETTA 1 (`ci.yml`): runner pure-Python, zero token LLM. Ultimo run verde.

---

## §Riepilogo finding F1

**PRIMA** (audit 2026-08-29, sistema prompt pre-`62af5ee`):
- `gas.py:~46-48` (vecchio layout): "Per CONTEGGI, MISURE E CALCOLI ESATTI usa run_command" 
- `SHELL_ALLOWLIST` senza calcolatori → ordine IMPOSSIBILE → bug SEMANTICO F1 CRITICO
- Comportamento osservato: Gemini aggirava (emetteva `calcola()`) — bug mascherato; altri provider potenzialmente bloccati

**DOPO** (commit `62af5ee`, review #93, current state):
- `gas.py:49-50`: "Per CALCOLI ARITMETICI usa SEMPRE calcola()" — ordine POSSIBILE e CORRETTO
- `SHELL_ALLOWLIST` invariata e corretta
- Sonda E2E 2026-09-01: Gemini 2 PASS + Groq 2 PASS → CHIUSO
