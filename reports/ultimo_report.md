# Report sessione: design/cancello-v2

> Data: 2026-09-30  
> Branch: design/cancello-v2  
> Tipo: doc-only (ZERO codice)

## Obiettivo

Aggiornare `reports/design_cancello.md` con correzioni tecniche e decisioni operatore 2026-09-29 per il Gate Autonomia GAS (Il Cancello). Aprire PR verso main.

## Cosa è stato fatto

### Documento aggiornato: `reports/design_cancello.md` → v2

**Intestazione:** aggiunto `v2 — decisioni operatore 2026-09-29` in cima.

**C-a §3 contaminazione (tre correzioni):**
1. Verificato `_memoria_pin` nel codice (gas.py:1239–1295, gas.py:1753–1824): inietta `prossima_azione` e `descrizione` eventi — campi a testo libero da terze parti. `_sanitize_memory_text` escapa solo `<`/`>`, non limita il contenuto a campi strutturati. **Fatto documentato: oggi ogni turno con pin non vuoto nasce con testo libero di terzi nel system prompt.**
2. Contaminazione riscritta come **per-finestra** (non per-turno): il turno è contaminato se nella finestra inviata al provider c'è un tool result contaminante; torna pulito solo quando quel result esce dalla finestra per scorrimento o compressione.
3. `read_file` contamina **sempre** (rimossa l'eccezione "file non di sistema").

**C-b §4 read-back integrale:**
- Read-back di `tool_args_json` INTEGRALE, senza troncamento. Se troppo grande per Telegram → diniego automatico (no approvazione parziale).
- Approvazione legata a `tool_args_hash` (SHA-256); il kernel esegue gli args salvati, non li rigenera.
- `id` approvazione = UUID casuale monouso (non autoincrement).
- Callback accettate solo da `TELEGRAM_ALLOWED_IDS`.
- Schema tabella `approvals` aggiornato con colonne `tool_args_hash` e `telegram_user_id`.

**C-c §8f + Fetta C4 — turno suddiviso:**
- Architettura: l'azione viene parcheggiata in `approvals`, il turno si chiude con "in attesa di firma"; su Approva il kernel avvia un nuovo turno di sblocco.
- Motivazione documentata: bot Telegram su un singolo thread — polling sincrono in `run_turn` bloccherebbe il thread e la firma non arriverebbe mai; parcheggio in DB sopravvive a crash (M3).
- Fetta C4 riscritta di conseguenza.

**C-d CRM in turno contaminato:**
- `salva_contatto` e `imposta_stato_contatto` restano eseguibili in turno contaminato fino a 5 scritture CRM totali nello stesso turno; dalla sesta → approvazione.
- Tabella §3c aggiornata con riga specifica per UNCERTAIN CRM.
- Test M4 aggiornato: `write_file` / `run_command` → parcheggiato; `salva_contatto` → eseguito fino alla soglia.

**Decisioni §8 chiuse:**
- 8a: `imposta_stato_contatto` UNCERTAIN anche per stati finali, con tetto C-d.
- 8b: solo [Approva]/[Rifiuta]; [Modifica] = fetta C6 futura.
- 8c: timeout 30 min (`GAS_APPROVAL_TIMEOUT_SECS=1800`).
- 8e: `run_command` UNCERTAIN solo se `GAS_SANDBOX_MODE=os_strict`; altrimenti IRREVERSIBLE.
- 8f: turno suddiviso.
- F-diario-eco: Opzione A, fetta autonoma prima di C1; fix vale solo in avanti (diario immutabile).

## Stato post-sessione

- ZERO modifiche al codice.
- `design_cancello.md` è v2 con tutte le decisioni chiuse.
- Prossimo passo: implementare in ordine — F-diario-eco → C1 → C2 → C3 → C4 → C5.
