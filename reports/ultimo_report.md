# REPORT — Sonda VPS read-only (2026-08-26)

**Data:** 2026-08-26
**Branch:** sonda/vps-stato-2026-08-26

---

## DECISIONI UMANE RICHIESTE

1. **Configurare SSH per la sonda VPS**: l'alias `ssh gas` non è configurato in questo ambiente WSL (`~/.ssh/config` assente). Servono due azioni dall'operatore:

   **Opzione A — setup completo:**
   ```bash
   # Aggiungere l'alias SSH (sostituire <VPS_IP> con l'IP reale del VPS Hetzner)
   cat >> ~/.ssh/config << 'EOF'
   Host gas
       HostName <VPS_IP>
       User gas
       IdentityFile ~/.ssh/id_ed25519
   EOF
   # Avviare ssh-agent e caricare la chiave (R7: la chiave ha passphrase)
   eval "$(ssh-agent -s)" && ssh-add ~/.ssh/id_ed25519
   ```

   **Opzione B — comunicare l'IP/hostname del VPS** a Claude Code, poi eseguire:
   ```bash
   ! eval "$(ssh-agent -s)" && ssh-add ~/.ssh/id_ed25519
   ```
   e rilanciale il task di sonda.

2. **Ri-eseguire il task di sonda** dopo il setup SSH — tutti i comandi della ricognizione sono pronti; unico blocco era la connettività.

---

## ESITO FETTE

**Fetta 1 — Stato servizio systemd gas**: SALTATA — SSH non raggiungibile (alias `gas` non configurato in `~/.ssh/config`)

**Fetta 2 — Stato git sul VPS** (commit, branch, git status): SALTATA — stesso blocco SSH

**Fetta 3 — Verifica .gitignore** (riserva F7: `.venv/` presente?): SALTATA — stesso blocco SSH

**Fetta 4 — Risorse di sistema** (RAM, disco, python3 --version): SALTATA — stesso blocco SSH

**Fetta 5 — Struttura directory e file memoria** (.gas_history.json, diario*): SALTATA — stesso blocco SSH

**Fetta 6 — Log recenti** (journalctl -u gas o gas_debug.log): SALTATA — stesso blocco SSH

---

## CAUSA DEL BLOCCO

Diagnostica eseguita in sequenza:

1. `ssh gas '...'` → `ssh: Could not resolve hostname gas: Name or service not known` (exit 255)
   - Causa: `~/.ssh/config` inesistente (verificato con `cat ~/.ssh/config` → "NESSUN ~/.ssh/config")

2. Ricerca hostname VPS in tutti i report del progetto → IP redatto ovunque come `<VPS_IP>` (sia nel runbook che in stato_storico.md)

3. Controllo `.env` di progetto → nessuna voce VPS/hostname

4. Config Windows-side (`/mnt/c/Users/gqual/.ssh/config`) → file inesistente

5. Chiave presente: `~/.ssh/id_ed25519` + `.pub` esistono. Fingerprint di riferimento WSL: `SHA256:/BJvnyxJIKj00Odj4onGIKszb2W3icqneeLhabKfnoE` (da stato_storico.md R7). Chiave ha passphrase → richiede ssh-agent.

---

## ANOMALIE / NOTE

- Il task è stato avviato su branch `main` (nessun branch di sessione preesistente). Creato `sonda/vps-stato-2026-08-26` al momento del `/fine-task` per rispettare il lucchetto main.
- Nessuna modifica al codice sorgente eseguita. Nessun rischio di regressione.
- La sonda è completamente non-invasiva: tutti i comandi pianificati erano read-only.
