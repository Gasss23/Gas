# Ultimo report

## Task
Doc-only, due fette. Scope chiuso dall'utente: SOLO `reports/stato_progetto.md`,
`reports/roadmap.md`, `reports/ultimo_report.md`. Nessuna modifica a gas.py, brains/, modules/,
tests/. Nessuna review revisore richiesta (policy reports/doc).

## Esito

### Fetta 1 — header reports/stato_progetto.md
✅ Fatta. Riga 4 aggiornata da:
`Ultimo aggiornamento: **2026-07-04** (S1 ✅, S1b ✅)`
a:
`Ultimo aggiornamento: **2026-07-07** (coerenza canonici + item taratura RAM)`
Nessun altro punto del file toccato.

### Fetta 2 — nuovo item aperto in reports/roadmap.md
✅ Fatta. Registrato in FASE 5 (sezione item aperti, NON tra i completati), tra
"Backup OFF-MACHINE" e "Process management + self-healing":

> **Taratura MemoryHigh/MemoryMax di gas.service su misura RAM reale a regime**
> (GAS + embedder singolo modello). Valori attuali 1500M/2000M conservativi, mai
> misurati (vedi nota 9 stato_progetto.md: misura "non registrato"). Da eseguire
> sul VPS insieme a R-wire-1 (VEC_MIN_SIM).

## Stop gate
Rispettato: nessun file toccato oltre `stato_progetto.md`, `roadmap.md` e questo report.

## File toccati
- `reports/stato_progetto.md` (riga 4: data + motivo aggiornati)
- `reports/roadmap.md` (nuovo item aperto FASE 5, taratura RAM systemd)
- `reports/ultimo_report.md` (questo file)
