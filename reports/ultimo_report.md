# Report — Runbook S1 Hardening v3 (patch chirurgiche)

**Data:** 2026-07-04  
**Scope:** Solo doc — `reports/runbook_s1_hardening.md`. Nessun file motore toccato.  
**Versione prodotta:** v3 (da v2)

---

## §1 SCOPE & ESITO FETTE

### Fetta 1 — Passo 5: socket activation Ubuntu 24.04 ✅

**Dove:** aggiunta sezione `5e-pre` prima del reload (`5e`).

**Cosa aggiunto:**
- Comando `systemctl is-active ssh.socket` per rilevare se Ubuntu 24.04 usa socket activation (default su 24.04).
- Procedura differenziata: se `ssh.socket` è active, il reload della config richiede ANCHE `systemctl restart ssh.socket` (per aggiornare il listener delle nuove connessioni).
- Nota esplicita: `restart ssh.socket` **non chiude** le sessioni SSH già stabilite — root e gas restano connessi.
- 2 righe sul modello service-vs-socket: `ssh.service` gestisce la sessione una volta stabilita; `ssh.socket` ascolta sulla porta 22 e spawna il service on-demand.

### Fetta 2 — Passo 5f e 6b: test password auth de-falsato ✅

**Dove:** `Test 3` in passo 5f e il corrispondente test in passo 6b.

**Bug corretto:** il comando precedente `ssh -o PreferredAuthentications=password gas@...` dà "Permission denied (publickey)" anche se la password fosse ancora abilitata, perché il client tenta prima la chiave pubblica. Il test era **falsato**: superava sempre anche con hardening non applicato.

**Fix:** sostituito con:
```
ssh -o PreferredAuthentications=password -o PubkeyAuthentication=no gas@204.168.251.92
```
Comportamento atteso corretto: "Permission denied (password)." IMMEDIATO.  
Se chiede la password → password auth ancora viva → hardening NON applicato.

La stessa correzione è applicata in entrambe le occorrenze (5f e 6b) per coerenza.

### Fetta 3 — Passo 3: check GAS non in esecuzione prima della copia DB ✅

**Dove:** aggiunta sezione `3d-pre` prima del passo 3d.

**Cosa aggiunto:**
- Comando `pgrep -f gas.py` con output differenziato: STOP esplicito se GAS gira, "copia sicura" se non gira.
- Motivazione: copiare `.gas_memory.db` mentre GAS scrive → DB corrotto o snapshot incoerente. "La memoria non deve mentire."
- Nota: attualmente GAS non gira sul VPS, ma il check resta come guardia permanente.
- Istruzione di fermare GAS se attivo (`pkill -f gas.py` o `systemctl stop gas`) prima di procedere.

### Fetta 4 (minore) — Passo 1a: nota lock apt ✅

**Dove:** in linea nel blocco `apt-get update -qq` del passo 1a.

**Cosa aggiunto:** una riga di nota: se `apt-get update` dà "Could not get lock", unattended-upgrades sta girando — attendere 1-2 minuti o fermarlo temporaneamente con `systemctl stop unattended-upgrades`.

---

## Vincoli rispettati

- Nessun file motore toccato (`gas.py`, `brains/`, `modules/`, `tests/`).
- Nessun gate revisore invocato (modifica solo a `reports/`).
- Sezione PROPOSTA fette successive (S1b) invariata.
- Runbook NON riscritto da zero: 4 patch chirurgiche sui punti indicati.
- Nessuna aggiunta fuori scope.

## File modificati

- `reports/runbook_s1_hardening.md` — v2 → v3 (4 patch)
- `reports/ultimo_report.md` — questo file
