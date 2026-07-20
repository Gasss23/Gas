# Report task — docs(security): scrub IP/SSH + roadmap privatizzazione

**Data:** 2026-07-20  
**Branch:** docs/scrub-ip-ssh  
**Commit:** `683cd08ab5a28aa516d8fa43c43751c9be6393ae`

---

## Esito per sezione

| Sezione | Stato |
|---------|-------|
| §0 Base fresca (fetch + branch da origin/main e7acf75) | FATTA |
| §1 Scrub IP/SSH in stato_progetto.md | FATTA |
| §1 Scrub IP in runbook_s1_hardening.md | FATTA |
| §1 Scrub IP in CLAUDE.md | SALTATA (IP assente) |
| §1 Scrub IP in tutti gli altri file tracciati | FATTA (0 occorrenze residue) |
| §2 Roadmap: item privatizzazione ALTA URGENZA | FATTA |
| §3 Commit + push docs/scrub-ip-ssh | FATTA |

---

## File toccati (verbatim)

- `reports/stato_progetto.md`
- `reports/runbook_s1_hardening.md`
- `reports/roadmap.md`

---

## git diff --stat reale della sessione

```
 reports/roadmap.md              |  2 ++
 reports/runbook_s1_hardening.md | 16 ++++++++--------
 reports/stato_progetto.md       |  7 ++++---
 3 files changed, 14 insertions(+), 11 deletions(-)
```

---

## Dettaglio §1 — Sostituzioni eseguite

**reports/stato_progetto.md §8:**
- Aggiunta riga ⚠️ SCRUB IP/SSH (2026-07-20) in cima all'item 8
- `gas@204.168.251.92` → `<VPS_USER>@<VPS_IP>`
- `via chiave ed25519` → `via chiave <KEY_TYPE>`
- `Utente gas` → `Utente <VPS_USER>`
- `/home/gas/gas/` → `/home/<VPS_USER>/gas/`
- `/home/gas/.cache/` → `/home/<VPS_USER>/.cache/`
- dropin `/etc/ssh/sshd_config.d/99-hardening.conf` → `/etc/ssh/sshd_config.d/<SSH_DROPIN>`

**reports/runbook_s1_hardening.md:**
- 8 occorrenze di `204.168.251.92` → `<VPS_IP>` (replace_all)

**CLAUDE.md:** IP assente — nessuna modifica.

**Verifica post-scrub:** `grep -rn "204\.168\.251\.92"` → 0 risultati.

---

## Dettaglio §2 — Roadmap

Item aggiunto in cima a `### 🟡 PROSSIMI PASSI` come voce 0:

```
0. 🔒 Privatizzare repo — ALTA URGENZA — trigger: prima che entrino dati lead reali /
   maturità GAS. Richiede GitHub Pro ($4/mese): su Free il repo privato SPEGNE il ruleset
   main-lock (rulesets su privati = solo Pro/Team/Enterprise). Quindi Pro + privato è
   UN'unica mossa. Chiude anche l'IP in history. Verificare fork pubblici prima: se
   esistono, l'IP è già uscito e va valutata la rotazione IP su Hetzner.
```

---

## Stato sicurezza

| Aspetto | Stato |
|---------|-------|
| IP nei file HEAD | PULITO (scrubato) |
| IP nella history git pubblica | PRESENTE — MITIGATO, NON chiuso |
| Fork pubblici | DA VERIFICARE prima della privatizzazione |
| Rotazione IP Hetzner | DA VALUTARE se esistono fork |
| Cura vera | Privatizzazione repo (GitHub Pro + privato = unica mossa) |

---

## STOP GATE

Nessuna azione oltre §0/§1/§2 è stata eseguita. Azioni fuori mandato
(rotazione IP, history rewrite, modifiche hook/CI) NON committate —
proposte nella sezione "Stato sicurezza" per decisione umana.
