# Report — FASE 5 S1: Hardening SSH+Base VPS

**Data:** 2026-07-04  
**Scope:** FASE 5 S1 — produzione runbook hardening VPS Hetzner CX33 (Helsinki, Ubuntu 24.04).  
**Commit unico:** runbook + report (solo reports/ → nessun gate revisore).

---

## §1 SCOPE & ESITO FETTE

### FETTA 1 — Runbook `reports/runbook_s1_hardening.md` → FATTA

Prodotto il runbook passo-passo per hardening SSH+base, progettato per esecuzione manuale umana in sessione SSH con console Hetzner come recovery path.

**Copertura:**

| Passo | Contenuto | Rischio lockout |
|---|---|---|
| 0 Pre-flight | Verifica console Hetzner PRIMA di qualsiasi modifica | N/A — bloccante |
| 1 unattended-upgrades | Installazione + config + verifica + rollback | Nessuno |
| 2 fail2ban | Jail sshd base (maxretry=5, bantime=1h) + rollback | Nessuno |
| 3 Utente 'gas' | Creazione, spostamento working dir + cache + DB, ownership | Nessuno |
| 4 SSH key-only | Copia pubkey, test su SECONDA SESSIONE, sessione root tenuta aperta | ⚠️ MEDIO |
| 5 sshd_config | sshd -t + reload (NON restart), PasswordAuth no, PermitRoot no | 🔴 ALTO |
| 6 Verifica finale | Checklist stato + tabella rollback riepilogativa | Nessuno |

**Vincoli rispettati:**
- Nessuna modifica a gas.py, brains/, modules/, tests/ → nessun gate revisore.
- Nessun comando eseguito verso il VPS (nessuna key SSH disponibile).
- Nessun script one-shot auto-eseguibile: ogni passo ha checkpoint di verifica esplicito.
- Passi 4 e 5 marcati con "recovery = console Hetzner; non procedere se pre-flight fallito".
- `sshd -t` obbligatorio prima del reload al passo 5.
- `systemctl reload ssh` (NON restart) per preservare sessioni attive.

**Proposta FETTA 2 (fuori scope S1, decisione umana):** inclusa in coda al runbook — systemd unit con MemoryHigh/MemoryMax (FINDING no-swap), swap file opzionale, spostamento VECTORS_DB, ollama on-demand. Nulla implementato.

---

## §2 ARTEFATTI PRODOTTI

- `reports/runbook_s1_hardening.md` — runbook completo (passo 0→6 + tabella rollback + proposta FETTA 2)
- `reports/ultimo_report.md` — questo file

---

## §3 STATO APERTO POST-S1

Nessun item risolto nel motore. Stato VPS invariato (runbook non eseguito — lo esegue l'umano).

Item in attesa di esecuzione umana:
- S1 hardening SSH+base (questo runbook)
- S1b sistemd unit + MemoryHigh/MemoryMax (futura, dipende da decisione umana su FETTA 2)
