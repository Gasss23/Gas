# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-09-28 — Autonomia K3+K4 (knowledge base in ricorda + 6 protezioni)

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #102 (https://github.com/Gasss23/Gas/pull/102).
2. Riserva R-k4-3 (cosmetica test): T69b check primario vacuosamente True se blocco `<conoscenza_dati>` assente. Il check discriminante è T69b.2. Da correggere in sessione futura se fastidiosa.

---

## §1 SCOPE & ESITO FETTE

- **FETTA 0 — Sonda (sola lettura)**: `FATTA` — K0-K2 confermati su origin/main (`d46868c`). K3/K4 non in contraddizione con le protezioni. `ricorda()` non leggeva `.gas_knowledge.db` prima di questa sessione. Path knowledge DB: costante in `tools/ingest_knowledge.py`, env `GAS_KNOWLEDGE_DB` non esistente in gas.py (aggiunta ora).

- **FETTA 1 — K3+K4**: `FATTA` — `_knowledge_search()` aggiunto, wiring in `_ricorda()`, 6 protezioni K4 implementate, 17 test T69a-T69h, E2E su copia 10/10. Review #108 APPROVATO CON RISERVE. Riserve R-k4-1/R-k4-2 chiuse prima del commit; R-k4-3 aperta.

- **Autonomia #2/#3**: `DEFERITA — STOP BLOCCANTE rispettato` (scope limitato a K3+K4 come da istruzioni; nessun codice fuori dai 6 punti K4).

- **Script CI / fix fuori scope**: `SALTATA — non pertinente a K3+K4 e non in scope` (STOP BLOCCANTE rispettato).

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   1 +
 gas.py                             |  92 +++++++++++++-
 reports/diff_sessione.md           |  34 +++--
 reports/handoff.md                 | 184 +++++++++++++--------------
 reports/stato_progetto.md          |   8 +-
 reports/ultimo_report.md           | 144 +++++++++++++++++----
 tests/test_unit_kernel.py          | 251 +++++++++++++++++++++++++++++++++++++
 7 files changed, 569 insertions(+), 145 deletions(-)
```

---

## §3 GIT LOG --ONELINE (sessione)

```
6249e16 feat(autonomia): K3+K4 — ricorda() pesca .gas_knowledge.db + 6 protezioni
6a0a2f7 chore(revisore): memoria review #108 — APPROVATO CON RISERVE
```

---

## §4 VERDETTO DEL REVISORE (per commit motore)

Commit `6249e16` tocca `gas.py` e `tests/test_unit_kernel.py` — review #108 obbligatoria.

**Verdetto integrale review #108:**

> ## VERDETTO REVIEW #108 — K3+K4 (knowledge base in ricorda + 6 protezioni)
>
> **Branch:** feat/autonomia-k3-k4
> **File esaminati:** gas.py, tests/test_unit_kernel.py
>
> ---
>
> ### APPROVATO CON RISERVE
>
> ---
>
> ### Evidenze concrete esaminate
>
> **gas.py:~1467** — `cap_n = min(int(n), self.KNOWLEDGE_MAX_RESULTS)` è posizionata PRIMA del blocco `try/except Exception` che copre la connessione SQLite. Se `n` fosse non-int-convertibile, l'eccezione sfugge a `_knowledge_search` e raggiunge `_ricorda` senza catch (nessun try/except nel call site). Rischio esaminato: propagazione non coperta da fail-safe §9. In pratica `n` è sempre int (schema tool + call in `_ricorda`), ma non è fail-safe per costruzione. Esito: **riserva minore R-k4-1**.
>
> **gas.py:~1638** (hunk @@ -1549) — `_MEM_FILE_PREFIXES` estesa con `.gas_knowledge`. Verifica: `".gas_knowledge.db-wal".lower().replace("-","_").replace(" ","_")` → `".gas_knowledge.db_wal"` contiene `.gas_knowledge` come substring → bloccato correttamente. T69f testa `.gas_knowledge.db`, `.GAS_KNOWLEDGE.db`, `.gas_knowledge.db-wal`. Esito: **ok, K4.4 soddisfatto**.
>
> ### Verifica K4 completa
>
> | # | Requisito | Esito |
> |---|-----------|-------|
> | K4.1 | Contenuto dentro `<conoscenza_dati>`, `_sanitize_memory_text`, "dati non istruzioni" | ✅ gas.py ~1479/1496, T69a/T69b.2 |
> | K4.2 | Cap deterministico env-overridabile (MAX_RESULTS=5, MAX_CHARS=2000) | ✅ gas.py ~536-540/839-840, SQL LIMIT + loop break, T69c/T69d |
> | K4.3 | Solo chunk con fonte in sources.yaml | ✅ gas.py ~1451-1465: carica YAML, filtra `attiva=True`, SQL IN con `approved`, T69e |
> | K4.4 | write_file blocca .gas_knowledge* | ✅ gas.py ~1638, T69f |
> | K4.5 | Nessun tool scrittura knowledge nel loop | ✅ tools_schema senza voci knowledge-write, SQLite `?mode=ro`, T69f2/T69f2b |
> | K4.6 | DB assente/corrotto → ricorda funziona, nessun crash | ✅ gas.py ~1446-1448 (exists check), ~1478-1480 (except), T69g/T69g3 |
>
> ### Antipattern Wall of Shame
> Nessun raw history slicing. Nessuna simulazione tool. T69h usa mock class strutturato. ✅
>
> ### Guardrail integrità
> `_knowledge_search` non tocca `range(10)`, non modifica la finestra, non auto-chiama. ✅
>
> ### Riserve (non bloccanti)
>
> - **R-k4-1** (minore): `gas.py:~1467` — `cap_n = min(int(n), self.KNOWLEDGE_MAX_RESULTS)` fuori dal try/except. Fix: spostare dentro il `try` oppure aggiungere un outer catch nel call site di `_ricorda`.
> - **R-k4-2** (cosmetica): `gas.py:~1477` — `source_name` e `ts` nel header non passano per `_sanitize_memory_text`. Rischio pratico nullo (ts[:10] non abbastanza lungo per un tag completo, source_name operator-controlled), ma non coerente con defense-in-depth applicata a `testo`.
> - **R-k4-3** (cosmetica test): `tests/test_unit_kernel.py:~4380` — T69b check primario con logica chained-split vacuosamente True se il blocco `<conoscenza_dati>` è assente. Il check discriminante reale è T69b.2.
>
> ### Rischio esplicitamente escluso
> `gas doctor` non verificato per il check di PyYAML assente o DB knowledge presente ma non leggibile: il diff non tocca la sezione doctor, fuori scope della fetta K3/K4.

**Azioni post-review**: R-k4-1 (chiusa: `cap_n` spostato dentro `try`), R-k4-2 (chiusa: `source_name`/`ts` sanitizzati), R-k4-3 (aperta, tracciata qui e in `stato_progetto.md`).

---

## §5 DELTA TEST DEL MOTORE

Prima → dopo:

| Metrica | Prima | Dopo |
|---------|-------|------|
| PASS | 366 | 383 |
| FAIL | 5 | 5 |
| Nuovi test | — | +17 (T69a-T69h) |

RIEPILOGO (output reale):

```
=== RIEPILOGO: 383 PASS, 5 FAIL ===
  FAIL: T11c2 snapshot fallito -> run_command (comando lecito) bloccato (fail-closed) — Operazione negata: sandbox OS (bwrap + namespace) non disponibile e GA
  FAIL: T11e run_command fa scattare lo snapshot — refs 1 -> 1
  FAIL: T12a comando in allowlist (wc) eseguito, output reale — Operazione negata: sandbox OS (bwrap + namespace) non dispon
  FAIL: T12c pipe non interpretata (niente shell) — Operazione negata: sandbox OS (bwrap + namespace) non disponibile e GA
  FAIL: T12e command substitution non eseguita (resta letterale) — Operazione negata: sandbox OS (bwrap + namespace) non disponibile e GA
```

I 5 FAIL sono tutti F-mac-1 (bwrap macOS, noti e attesi): `T11c2`, `T11e`, `T12a`, `T12c`, `T12e`. Nessun nuovo FAIL introdotto da questa sessione.

---

## §6 STATO CI

```
in_progress		docs(fine-task): handoff + report K3+K4 autonomia knowledge 2026-09-28	CI	feat/autonomia-k3-k4	push	36477977180	13s	2026-09-28T20:16:05Z
completed	success	Merge pull request #101 from Gasss23/feat/fetta3a-lezioni-quarantena	CI	main	push	36468992436	1m1s	2026-09-28T18:58:43Z
completed	success	fix(ci): handoff §1 — rimuovi citazione inline titolo §2 che ingannav…	CI	feat/fetta3a-lezioni-quarantena	push	36461669985	50s	2026-09-28T17:56:18Z
```

**Mappatura commit→run:**
- `ffb4d81` (docs fine-task reports): run CI `36477977180` — in_progress al momento della scrittura (run non ancora completata).
- `6249e16` (feat K3+K4 codice): incluso nell'albero pushato con `ffb4d81` sulla stessa run `36477977180` — nessuna run autonoma su questo SHA intermedio.
- `6a0a2f7` (chore revisore): incluso nell'albero pushato — nessuna run autonoma su questo SHA intermedio.

---

## §7 RISERVE APERTE

Dalla sessione corrente (review #108):
- **R-k4-3** (cosmetica test): T69b check primario con logica chained-split vacuosamente True quando blocco `<conoscenza_dati>` assente. Il check discriminante è T69b.2. Da correggere in sessione futura.

Ereditate da sessioni precedenti:
- **R-lez-bis-1** (cosmetica, fetta 3a-bis): vedi stato_progetto.md
- **R-lez-2** (ereditata, fetta 3a): vedi stato_progetto.md
- **R-ci-1** (regex check_handoff da ancorare a `^`): vedi stato_progetto.md
