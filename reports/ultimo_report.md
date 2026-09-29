# REPORT: Design del Cancello — Gate Autonomia GAS

**Data:** 2026-09-29  
**Branch:** design/cancello  
**Scope:** Documento di architettura per il meccanismo di controllo delle azioni autonome di GAS (zero codice)

---

## DECISIONI UMANE RICHIESTE

1. **Classificazione CRM:** `imposta_stato_contatto` deve restare UNCERTAIN o scalare a IRREVERSIBLE? (§8a del documento)
2. **Interfaccia Telegram:** solo [Approva]/[Rifiuta] oppure aggiungere [Modifica]? (§8b)
3. **Timeout approvazione:** 1 / 5 / 15 minuti o nessun limite? (§8c)
4. **Batch approvazioni M1:** per-azione o approva-batch oltre N=3? (§8d)
5. **`run_command` nel gate:** UNCERTAIN / IRREVERSIBLE / classe dinamica per argomento? (§8e)
6. **Architettura sospensione turno C4:** sospensione sincrona (polling) vs turno suddiviso vs callback asincrono? (§8f)
7. **F-diario-eco:** aprire finding dedicato e schedulare fix (Opzione A raccomandata)?

---

## ESITO FETTE

### Fetta unica — Documento di design `reports/design_cancello.md`
**FATTA**

Prodotto: `reports/design_cancello.md` (310 righe), con:

1. **§1 Inventario** — 7 tool attuali + 11 azioni future classificati in 4 categorie (reversibile-sicuro / reversibile-incerto / irreversibile / denylist). Inclusa tabella file intoccabili.

2. **§2 Classificatore deterministico** — dizionario hardcoded `GATE_ALLOWLIST` in Python con `GateClass` enum. Default-STOP se tool non in allowlist. Punto di aggancio in `run_turn` (prima di `execute_tool_call`). Invariante: il modello non può ispezionare né modificare il gate.

3. **§3 Regola input non fidato** — flag `_turno_contaminato` per-turno. Tool contaminanti: `ricorda`, `read_file` su file utente, `browser_scrape` (futuro), `fetch_email` (futuro). Effetto: UNCERTAIN in turno contaminato → promossa a IRREVERSIBLE. Tabella 4×2.

4. **§4 Canale firma Telegram** — tabella `approvals` SQLite (8 colonne), flusso completo in 6 passi, read-back verbatim degli argomenti JSON (non parafrasi del modello), timeout 5 min configurabile via env, default-non-eseguire allo scadere.

5. **§5 File intoccabili** — 10 path/prefissi in denylist assoluta per `write_file` e `run_command`.

6. **§6 Piano fette C1–C5** — 5 fette con test unitari per ciascuna. Test di accettazione M2 (mail con firma) e M4 (iniezione durante missione) dettagliati passo-passo.

7. **§7 Finding F-diario-eco** — descritto il meccanismo (output di `ricorda` entra nel diario immutabile via `_esito_sintetico` a riga ~1859-1869), tre effetti negativi (bypass K4.3, amplificazione adversariale, semantica diario compromessa), due opzioni di correzione. Opzione A raccomandata (una riga di modifica). **NON implementato** — proposto come finding autonomo separato.

8. **§8 Domande aperte** — 6 domande per l'operatore con argomenti pro/contro e raccomandazione tecnica dove applicabile.

---

## ANOMALIE E NOTE

- Nessuna modifica a `gas.py`, `brains/`, `modules/`, `tests/`, `gas_identity.md` — STOP gate rispettato.
- Il finding F-diario-eco era citato nel task come da includere nel documento: descritto in §7, non implementato come richiesto.
- Non è stato invocato il revisore (nessun diff motore).
