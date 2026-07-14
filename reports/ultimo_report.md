# R-crm-1b Fette 0+1 — Sonda CRM + Rilevamento duplicati email

**Data:** 2026-07-14
**Branch:** feature/crm-dup-detect

---

## DECISIONI UMANE RICHIESTE

1. **Merge PR `feature/crm-dup-detect` → main**: CI verde (run 29319472091, SUCCESS). `gh pr merge --merge` o browser GitHub.
2. **Scope fette successive R-crm-1b**: decidere se e quando implementare Fetta 2 (telefono) e/o Fetta 3 (somiglianza nome — fuzzy). Non implementate in questa sessione per rispetto dello STOP GATE.
3. **Fix cosmetic riserva #47**: messaggio CLI stampa `_unisci_contatti` (underscore, convenzione Python per metodo privato) — andrebbe `unisci_contatti`. Banale, 1 riga. Da fare nella prossima fetta o come micro-fix.

---

## Esito fette

- **Fetta 0 — Sonda CRM**: `FATTA`
  Risposto alle 4 domande della sonda leggendo il codice reale (store.py, gas.py). Risultato: lo scope R-crm-1b è valido, il caso "stessa email = due contatti" esiste. Report committato in `b99c1f1`.

- **Fetta 1 — Rilevamento duplicati email**: `FATTA`
  `rileva_duplicati_email()` in `modules/memory/store.py` + CLI `gas check-dups` in `gas.py` + 7 test T57 PASS. Review #47 APPROVATO CON RISERVE. Riserva bloccante (`nota`→`note` in T57b) corretta prima del commit.

- **Fetta 2 — Telefono**: `SALTATA — fuori scope sessione (STOP GATE)`
  Non implementata: le istruzioni prevedono STOP dopo la Fetta 1 email.

- **Fetta 3 — Somiglianza nome**: `SALTATA — fuori scope sessione (STOP GATE)`
  Non implementata: richiede decisione operatore su strategia fuzzy.

---

## Riserve aperte (review #47)

- **Re-entry diario**: invocazioni ripetute di `rileva_duplicati_email()` sulle stesse coppie accumulano righe duplicate nel diario. Accettabile per audit log, documentato ma non bloccante.
- **Messaggio CLI cosmetic**: stampa `_unisci_contatti` (metodo privato per convenzione) invece di `unisci_contatti` (metodo pubblico). Confonde l'operatore. Da correggere in una prossima fetta.
