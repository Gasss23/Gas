# Handoff sessione 2026-06-27 — probe telemetria + observability doctor

---

## §DECISIONI UMANE RICHIESTE

**D1 — Bug probe vector store in doctor:**  
`gas doctor` usa `default_vectors_path(root)` hardcoded per il probe del vector store (gas.py:1628), ignorando `GAS_VECTORS_DB` env. Se sul VPS si setta un path custom, il probe e il runtime guardano DB diversi → possibile falso OK in doctor mentre il layer è disabilitato a runtime. Richiede modifica a doctor. **Tuo OK per procedere?**

**D2 — Motivo fingerprint-guard non visibile in doctor:**  
Quando il guard disabilita il layer, il WARN di doctor è `"deps assenti o sidecar corrotto"` (generico). Il motivo specifico (mismatch modello, DB legacy, deps) è solo in `gas_debug.log`. Per visibilità h24 unattended servirebbe propagare un `disable_reason` da VectorStore a doctor. Richiede modifica a entrambi i moduli. **Vuoi pianificarlo come item del roadmap?**

**D3 — Degrado solo-testo per-turno (finding R2 #5) resta aperto:**  
Nessun rilevamento runtime. Il commento in gas.py:128 dice "rimandato per falsi positivi". Se si vuole implementare, il punto d'aggancio naturale è nel loop agentico a gas.py:1381-1387 (confronto tra tool_calls attesi e risposta arrivata). **Da pianificare o lasciare aperto?**

---

## Esito sonda

| ID | Domanda | Risposta sintetica |
|----|---------|-------------------|
| A1 | Schema `.gas_tokens.jsonl` | JSONL append-only: ts, provider, model, in, out, event("call"\|"fallthrough"), reason(opt) |
| A2 | Punto unico fallthrough | gas.py:1388-1404 — `except Exception` nel loop provider + `_log_tokens(event="fallthrough")` + `continue` |
| A3 | Conteggio per-provider | ✅ Già implementato (commit 2eb0e30): `gas tokens` tabella + `gas doctor` sezione Telemetria |
| A4 | 429 distinguibile | ✅ Sì — campo `reason` = "429: quota esaurita" vs err_text[:60] per KO generici |
| B1 | Sezioni doctor | 11 sezioni: API keys, Provider, Paracadute, File, Storia, Log, Sandbox OS, Snapshot, Memoria, Config, Telemetria |
| B2 | Motivo disable vector | ⚠️ WARN generico + bug path (D1+D2) |
| B3 | Degrado solo-testo | ⚠️ Non implementato (D3) |

Referto completo: `reports/probe_telemetria.md`

---

## git diff --stat sessione

```
 reports/probe_telemetria.md | 200 +++++++++++++++++++++++++++++++++++++++++++
 1 file changed, 200 insertions(+)
```

---

## git log sessione

```
19e69dd docs(sonda): probe telemetria provider + observability gas doctor 2026-06-27
```

---

## Delta test

N/A — motore non toccato. CI ultimo run: `28292278960` su commit `adc7701` → **SUCCESS** (187 PASS, 0 FAIL).

---

## Verdetto revisore

N/A — nessuna modifica al motore in questa sessione.

---

## Stato CI (FETTA 1 — .github/workflows/ci.yml)

- **Ultimo run:** `28292278960` — `2026-06-27T14:38:45Z`
- **Commit:** `adc7701` (docs(revisore): lezioni sessione 2026-06-27)
- **Esito:** ✅ SUCCESS
- **Suite:** 187 PASS, 0 FAIL
- **Bwrap:** attivo (ubuntu-24.04, AppArmor rilassato nel runner CI)
- **Note:** nessun push di motore in questa sessione → CI non rilanciata; stato valido dal push precedente su `adc7701`
