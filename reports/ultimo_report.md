# Report — FASE 5 S1: Hardening SSH+Base VPS (v2)

**Data:** 2026-07-04  
**Scope:** FASE 5 S1 — produzione runbook hardening VPS Hetzner CX33 (Helsinki, Ubuntu 24.04).  
**Commit:** solo reports/ → nessun gate revisore.

---

## §1 SCOPE & ESITO FETTE

### FETTA 1 — Runbook `reports/runbook_s1_hardening.md` → FATTA (v2)

Runbook passo-passo per hardening SSH+base, esecuzione manuale umana, console Hetzner come recovery.

**Copertura:**

| Passo | Contenuto | Rischio lockout |
|---|---|---|
| 0 Pre-flight | Verifica console Hetzner (BLOCCANTE prima di tutto) | N/A |
| 1 unattended-upgrades | Install + config non interattiva + verifica + rollback | Nessuno |
| 2 fail2ban | Jail sshd (`backend=auto` per Ubuntu 24.04 journald) + rollback | Nessuno |
| 3 Utente 'gas' | Crea utente (con check uid libero), sposta dir/cache/DB, verifica ownership | Nessuno |
| 4 SSH key-only | Installa pubkey, test su SECONDA sessione, sessione root tenuta aperta | ⚠️ MEDIO |
| 5 sshd_config | Dropin `99-hardening.conf` (override cloud-init), `sshd -t`, reload NON restart | 🔴 ALTO |
| 6 Verifica | `sshd -T` (config effettiva consolidata), lockout test, tabella rollback | Nessuno |

**Correzioni v2 rispetto a v1:**

- **Passo 5**: rimossa la modifica via `sed` sul file principale; aggiunto dropin
  `/etc/ssh/sshd_config.d/99-hardening.conf` — gestisce correttamente Hetzner/cloud-init
  che scrive `50-cloud-init.conf` con `PasswordAuthentication yes`. Il dropin `99-` ha
  precedenza su `50-` nell'ordine alfabetico dei dropin.
- **Passo 5 verifica**: aggiunto `sshd -T` come fonte di verità della config effettiva
  (mostra il consolidato main config + dropin, non solo il file grezzo).
- **Passo 2**: aggiunto `backend = auto` nella jail sshd — su Ubuntu 24.04 fail2ban
  preferisce journald; `auto` sceglie il metodo disponibile senza richiedere `/var/log/auth.log`.
- **Passo 3**: aggiunto check uid libero prima della creazione utente (il bot trading
  coabitante potrebbe occupare `uid=1001`).

**Vincoli rispettati:**
- Nessuna modifica a gas.py, brains/, modules/, tests/ → nessun gate revisore.
- Nessun comando eseguito verso il VPS (nessuna key SSH disponibile).
- Nessun script one-shot: ogni passo ha checkpoint esplicito prima di procedere.
- Passi 4 e 5 marcati "recovery = console Hetzner; non procedere se pre-flight fallito".
- `sshd -t` obbligatorio prima del reload al passo 5.
- `systemctl reload ssh` (NON restart) per preservare le sessioni attive.

**Proposta fette successive (fuori scope, decisione umana):**  
swap file 2–4 GiB, systemd unit con MemoryHigh/MemoryMax, VECTORS_DB path esplicito,
ollama on-demand. Nulla implementato.

---

## §2 ARTEFATTI PRODOTTI

- `reports/runbook_s1_hardening.md` — runbook v2 (passo 0→6 + tabella rollback + proposta FETTE)
- `reports/ultimo_report.md` — questo file

---

## §3 STATO APERTO POST-S1

Motore invariato. VPS invariato (runbook da eseguire a mano dall'umano).

Item pending:
- Esecuzione runbook S1 (hardening SSH + utente gas) — a cura dell'umano
- Decisione su fette successive (swap, systemd unit, VECTORS_DB) — a cura dell'umano
