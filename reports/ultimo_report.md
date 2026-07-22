# Ultimo report — 2026-07-22

## Task

DOC-ONLY. Aggiornamento `reports/stato_progetto.md` con esito sessione 2026-07-22
(sonda VPS, chiusura F7, rettifica diagnosi SSH, gestione chiave gas-vps).

## Branch

`docs/sonda-vps-2026-07-22` (da `origin/main` → 425ba5c)

## File toccati

- `reports/stato_progetto.md` — unica modifica (4 edit descritti sotto)
- `reports/ultimo_report.md` — questo file

## Modifiche apportate

### 1. Header

Aggiornato "Ultimo aggiornamento" da `2026-07-21` a `2026-07-22 (sonda VPS +
rientro accesso SSH)`.

### 2. CI runs — PR #35 aggiunta

Aggiunta in testa alla riga CI:
`PR #35 merge 425ba5c (2026-07-22, CI 29919691907)`

Run ID recuperato live con `gh run list --branch main --limit 5`.
Output verificato: completed / success / 2026-07-22T12:27:28Z.

### 3. Contatore review — verifica e allineamento

**Metodo**: lettura integrale di `.claude/agents/memoria_revisore.md` (100 righe
totali). Ultima riga del file contiene il marcatore `#57` (2026-07-19).
Ultima review = **#57**.

**Risultato**: ENTRAMBE le sezioni di `stato_progetto.md` riportavano già
**57 review / ultima #57** prima di questa sessione — il file era già allineato.
Nessuna modifica al contatore necessaria.
La discrepanza descritta nel brief ("punto C dice 56") era relativa a uno stato
precedente al merge PR #35.

### 4. DA FARE — 3 nuovi item 🟡

Aggiunti dopo R-encoding nella sezione `### DA FARE — sviluppo/processo`:

- 🟡 2FA Hetzner: da attivare; recovery code da salvare OFFLINE prima di confermare.
- 🟡 Ispezionare `/root/.ssh/authorized_keys` sul VPS (residuo gas-vps).
- 🟡 Decidere se rimuovere `gas-vps` da Hetzner Security → SSH Keys.

### 5. Nuovo blocco — Sessione 2026-07-22

Aggiunto in fondo al file (dopo Sessione 2026-07-21). Contenuto (tutti dati
verificati live):

- ✅ F7 CHIUSO: VPS usa `.venv` (con punto), verificato via ssh test -d.
  .gitignore locale ha sia venv/ sia .venv/ → copertura completa.
- ✅ Rilievo FETTA B CHIUSO: fingerprint SHA256:/BJvnyxJIKj00Od...
  verificato presente in authorized_keys del VPS.
- 🔴→✅ RETTIFICA diagnosi SSH: causa reale era BatchMode=yes + chiave con
  passphrase senza ssh-agent, NON chiave mancante. Riga 2026-07-21 conservata.
- ℹ️ Chiave gas-vps identificata (clone Windows deprecato), rimossa da
  authorized_keys del VPS, backup lasciato su VPS.
- ⚠️ Residuo: /root/.ssh/authorized_keys non ispezionato (mitigato da
  PermitRootLogin no). Stato: MITIGATO, non chiuso.
- ⚠️ Residuo: gas-vps ancora in Hetzner SSH Keys.
- ℹ️ Azioni transitorie console Hetzner: PasswordAuth yes/no, passwd lock gas.
- ⚠️ CAMBIO: passwd -l gas blocca sudo con password per utente gas.
- ℹ️ Precisazione §7: push git (HTTPS, no agent) ≠ ssh al VPS (chiave con
  passphrase, agent richiesto a ogni sessione).
- ✅ GAS active a fine sessione, servizio mai interrotto.

## Invarianti rispettate

- Nessun IP VPS in chiaro (grep confermato negativo).
- Nessuna modifica al motore (gas.py, brains/, modules/, tests/).
- Revisore NON invocato (DOC-ONLY).
- PR NON mergiata.
