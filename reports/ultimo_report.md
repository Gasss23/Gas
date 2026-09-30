# REPORT — F-diario-eco (2026-09-30)

**Branch:** `fix/diario-eco`  
**Commit motore:** `927c378`  
**PR:** #106 — https://github.com/Gasss23/Gas/pull/106  
**Revisore:** review #114 — APPROVATO CON RISERVE

---

## DECISIONI UMANE RICHIESTE

Nessuna.

---

## Esito per fetta

**PASSO 1 — SONDA (sola lettura)**
FATTA.
- Punto di scrittura diario: `gas.py:1881` — `_esito_str = self._esito_sintetico(out)` all'interno di `run_turn`.
- Tool che copiano testo non fidato nel diario:
  - `ricorda` (SÌ): output `<memoria_dati>...content...` → primi 160 char in diario
  - `read_file` (SÌ): contenuto file grezzo → primi 160 char in diario
  - `run_command` (SÌ): stdout+stderr — NON corretto per scope task
  - `write_file`, `calcola`, `salva_contatto`, `imposta_stato_contatto`: NO (stringhe fisse)
- Conteggio deterministico N per ricorda: variabile locale `parti: List[str]` — `sum(1 for p in parti if p.startswith("- ["))` sulla struttura dati prima della serializzazione a stringa. STOP GATE non scatta.

**PASSO 2 — FIX**
FATTA.
- Aggiunto `_esito_diario(name, out)` instance method (gas.py ~1152): specializza ricorda e read_file, delega a `_esito_sintetico` per tutti gli altri.
- `ricorda`: `"[OK] N risultati restituiti"` oppure `"[KO]"` (nessun testo output)
- `read_file`: `"[OK] N caratteri letti"` oppure `"[KO]"` (nessun testo output)
- `self._ricorda_n` resettato a 0 all'inizio di `_ricorda` (incluso ramo memoria None)
- `run_turn:1881` sostituisce `_esito_sintetico` → `_esito_diario`
- `run_command` finding segnalato nel report, NON corretto (out of scope)

**PASSO 3 — TEST REALI**
FATTA.
- 4 nuovi test T70a–d: tutti PASS
  - T70a: ricorda query non vuota → diario `"[OK] 1 risultati restituiti"`, nessun testo output
  - T70b: payload malevolo ("ignora le istruzioni") → NON compare nel diario azione
  - T70c: round-trip con 2 call ricorda → ciclo non interrotto, 1 risposta finale
  - T70d: read_file → diario `"[OK] 21 caratteri letti"`, nessun contenuto file
- Suite completa: **396 PASS, 5 FAIL** — tutti i FAIL sono F-mac-1 (bwrap macOS noti)
- sha256 DB reale prima: `d1c8f0cc2961145a629bf0b57a43d1b0328fe4db1bf5c428a8037c92b756ef11`
- sha256 DB reale dopo: `d1c8f0cc2961145a629bf0b57a43d1b0328fe4db1bf5c428a8037c92b756ef11` — INVARIATO

**PASSO 4 — REVISORE**
FATTA. Revisore #114: APPROVATO CON RISERVE.
- R-eco-1 (applicata): commento sul coupling regex `_cap_tool_output` aggiunto prima del commit.
- R-eco-2 (non bloccante): test non visibili nel diff statico.

**Finding segnalati NON corretti (out of scope)**:
- `run_command` copia stdout+stderr nel diario (confermato sonda 1b). Da correggere in fetta separata.

---

## Anomalie riscontrate

Nessuna anomalia fuori scope.

---

## Note tecniche

- Il diario immutabile esistente NON è stato toccato (righe storiche restano).
- Il fix vale solo per le scritture future (in avanti).
