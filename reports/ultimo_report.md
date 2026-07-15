# Report — docs/header-park-tmux

**Data:** 2026-07-15
**Branch:** docs/header-park-tmux
**Scope:** DOC-ONLY — micro-fix header + item PARK in reports/stato_progetto.md

---

## Esito per fetta

| Fetta | Stato | Note |
|-------|-------|------|
| 1 — pulizia header | **FATTA** | BOM rimosso, " origin/main" spurio rimosso (riga 80), data aggiornata |
| 2 — PARK item tmux | **FATTA** | Item aggiunto dopo riga GDPR nella sezione PARK |

---

## Fetta 1 — dettaglio grep "origin/main"

Grep eseguito prima di qualsiasi modifica: `grep -n "origin/main" reports/stato_progetto.md`

| Riga | Testo | Decisione | Motivo |
|------|-------|-----------|--------|
| 80 | `...lead CRM). origin/main` | **RIMOSSO** | Rumore spurio appiccicato a fine riga — nessun contesto tecnico |
| 140 | `riallineare a origin/main` | **NON TOCCATO** | Frase tecnica legittima (istruzione operativa git) |
| 140 | `merge --ff-only origin/main` | **NON TOCCATO** | Comando git legittimo nella stessa riga |

Nessuna occorrenza ambigua.

### BOM UTF-8

Confermato con `hexdump`: bytes iniziali `ef bb bf` (BOM). Rimosso con `sed -i '1s/^\xEF\xBB\xBF//'`.
Verifica post-modifica: file inizia ora con `23 20` (`# `). OK

### Data header

Riga 4 aggiornata da `**2026-07-14**` a `**2026-07-15**` con causale `header-park-tmux: BOM rimosso + item PARK tmux aggiunto`.

### Mojibake nel corpo

NON toccato — fuori scope deliberato come da istruzioni task.

---

## Fetta 2 — item PARK aggiunto

Aggiunto dopo l'item GDPR nella sezione `### PARK — registrati, nessun impegno`:

```
- SSH + tmux come via di accesso al dev tooling da telefono (item 2 roadmap):
  registrato come alternativa a Dispatch, nessun impegno. Da riprendere SOLO se
  la sonda Dispatch fallisce. Caveat di sicurezza da valutare prima di qualsiasi
  implementazione: esporre una sessione tmux con Claude Code = superficie RCE
  sulla box di sviluppo/repo; richiede design a fiducia mono-direzionale e
  autenticazione separata.
```

Stile adattato: voce puntata singola, sostanza invariata.

---

## git diff --stat REALE

```
reports/stato_progetto.md | 7 ++++---
 1 file changed, 4 insertions(+), 3 deletions(-)
```

---

## Stop gate

- Nessun file di motore toccato (gas.py, brains/, modules/, tests/): OK
- Nessuna review revisore invocata (commit doc-only): OK
- Nessun fix mojibake effettuato (fuori scope): OK
- Nessuna altra modifica oltre a reports/stato_progetto.md e reports/ultimo_report.md: OK
