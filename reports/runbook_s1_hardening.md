# RUNBOOK — FASE 5 S1: Hardening SSH + Base VPS
**Target:** Hetzner CX33, Helsinki, Ubuntu 24.04 — `root@204.168.251.92`  
**Autore:** Claude Code — 2026-07-04  
**Eseguito manualmente dall'umano** in una sessione SSH con console Hetzner aperta.

---

## AVVERTENZE GLOBALI

> **NON eseguire questo runbook come script automatico.**  
> Ogni passo va eseguito, verificato e confermato prima di procedere.  
> Un passo saltato o eseguito fuori ordine può causare **lockout permanente** senza console.

> **Console Hetzner = unica rete di sicurezza contro lockout.**  
> Se la console non è accessibile, **non toccare sshd né il firewall** — fermati al passo 0.

---

## PASSO 0 — PRE-FLIGHT (BLOCCANTE)

**Obiettivo:** verificare che la console Hetzner sia accessibile e funzionante PRIMA di qualsiasi modifica.

### Azioni

1. Vai su [console.hetzner.com](https://console.hetzner.com) dal browser.
2. Seleziona il server `CX33 Helsinki`.
3. Apri la **Console VNC** (pulsante "Console" in alto a destra nella pagina server).
4. Nella console VNC, premi `Invio` — deve apparire il prompt di login.
5. Effettua login come `root` con la password root.
6. Verifica che il prompt risponda (es. `root@<hostname>:~#`).

### Output atteso

```
Ubuntu 24.04 LTS
<hostname> login: root
Password: ****
root@<hostname>:~#
```

### Verifica prima di procedere

- Console VNC: **accessibile e login root funzionante** → ✅ puoi procedere
- Console VNC: **non accessibile o login fallito** → 🔴 **STOP. Non toccare sshd.**

### Rollback

N/A — nessuna modifica eseguita in questo passo.

---

## PASSO 1 — unattended-upgrades

**Obiettivo:** abilitare gli aggiornamenti automatici di sicurezza (kernel, librerie critiche).  
**Rischio:** basso. Reversibile. Non tocca sshd né la rete.

### Prerequisito

```bash
# Sulla sessione SSH root già aperta
uname -a          # verifica kernel Ubuntu 24.04
lsb_release -a    # verifica distro
```

Output atteso: `Ubuntu 24.04.*`, `Kernel: 6.x.*`

### Installazione

```bash
apt-get update -qq
apt-get install -y unattended-upgrades apt-listchanges
```

Output atteso: `... unattended-upgrades is already the newest version` oppure `Setting up unattended-upgrades...` — entrambi OK.

### Configurazione

```bash
dpkg-reconfigure -plow unattended-upgrades
```

Alla domanda "Automatically download and install stable updates?" → seleziona **Sì**.

Oppure in modo non interattivo:

```bash
echo 'APT::Periodic::Update-Package-Lists "1";
APT::Periodic::Unattended-Upgrade "1";
APT::Periodic::AutocleanInterval "7";' > /etc/apt/apt.conf.d/20auto-upgrades
```

### Verifica

```bash
cat /etc/apt/apt.conf.d/20auto-upgrades
# deve mostrare i valori sopra

systemctl status unattended-upgrades
# deve essere: active (running)  o  active (exited) — entrambi OK
```

### Rollback

```bash
apt-get remove --purge unattended-upgrades -y
rm -f /etc/apt/apt.conf.d/20auto-upgrades
```

---

## PASSO 2 — fail2ban

**Obiettivo:** bloccare IP che fanno brute-force su SSH (protezione passiva, logga in `/var/log/fail2ban.log`).  
**Rischio:** basso. Reversibile. Non tocca sshd.conf.

### Installazione

```bash
apt-get install -y fail2ban
```

### Configurazione jail SSH

```bash
cat > /etc/fail2ban/jail.d/sshd-local.conf << 'EOF'
[sshd]
enabled  = true
port     = ssh
filter   = sshd
logpath  = /var/log/auth.log
maxretry = 5
bantime  = 1h
findtime = 10m
EOF
```

### Avvio e abilitazione

```bash
systemctl enable fail2ban
systemctl restart fail2ban
```

### Verifica

```bash
systemctl status fail2ban
# deve essere: active (running)

fail2ban-client status sshd
# deve mostrare: Currently banned: 0  (a meno che qualcuno non stia già attaccando)
```

Output atteso `fail2ban-client status sshd`:

```
Status for the jail: sshd
|- Filter
|  |- Currently failed: 0
|  `- Total failed: 0
`- Actions
   |- Currently banned: 0
   `- Total banned: 0
```

### Rollback

```bash
systemctl stop fail2ban
systemctl disable fail2ban
apt-get remove --purge fail2ban -y
rm -f /etc/fail2ban/jail.d/sshd-local.conf
```

---

## PASSO 3 — Utente runtime non-root 'gas'

**Obiettivo:** creare l'utente sotto cui girerà GAS in produzione. Spostare working dir, model cache e database fuori da `/root`. NON avviare GAS ora.  
**Rischio:** medio (modifica struttura file). Reversibile. Non tocca sshd.

> **Assunzione:** i file GAS si trovano in `/root/gas/` e i DB in `/root/*.db` o `/root/gas/*.db`.  
> Adatta i path se la struttura reale è diversa — controlla prima con `ls /root/`.

### 3a. Verifica struttura attuale

```bash
ls -la /root/
ls -la /root/gas/ 2>/dev/null || echo "no /root/gas"
ls /root/*.db 2>/dev/null || echo "no db in /root"
ls /root/gas/*.db 2>/dev/null || echo "no db in /root/gas"
# annotati i path reali prima di procedere
```

### 3b. Creazione utente

```bash
useradd --create-home --shell /bin/bash --comment "GAS runtime" gas
# verifica
id gas
# output atteso: uid=1001(gas) gid=1001(gas) groups=1001(gas)
```

### 3c. Spostamento working directory GAS

```bash
# Sostituisci /root/gas con il path reale rilevato al passo 3a
cp -a /root/gas /home/gas/gas
chown -R gas:gas /home/gas/gas
ls -la /home/gas/gas/   # verifica contenuto
```

### 3d. Spostamento model cache fastembed

```bash
# La cache fastembed di default va in ~/.cache/huggingface o ~/.cache/fastembed
# Controlla dove si trova
ls -la /root/.cache/ 2>/dev/null

# Se esiste /root/.cache/fastembed (o /root/.cache/huggingface):
cp -a /root/.cache /home/gas/.cache
chown -R gas:gas /home/gas/.cache
ls /home/gas/.cache/
```

### 3e. Spostamento database SQLite (.gas_*.db)

```bash
# Identifica i DB dal passo 3a — esempio tipico:
# /root/gas/.gas_memory.db, /root/gas/.gas_tokens.jsonl, /root/gas/.gas_history.json

# I DB sono già dentro /root/gas/ e dunque già copiati al passo 3c.
# Se ci sono DB extra in /root/ direttamente:
for f in /root/.gas_*.db /root/.gas_*.jsonl /root/.gas_history.json; do
  [ -e "$f" ] && cp -a "$f" /home/gas/ && chown gas:gas /home/gas/$(basename "$f")
done
ls -la /home/gas/.gas_* 2>/dev/null
```

### 3f. Verifica ownership

```bash
find /home/gas -not -user gas -not -group gas 2>/dev/null | head -20
# output atteso: nessuna riga (tutto owned da gas:gas)
```

### 3g. Verifica struttura home

```bash
ls -la /home/gas/
# atteso: gas/, .cache/ (eventuale), .gas_*.db (eventuali)
```

> **NON avviare GAS come utente gas ora.**  
> I path originali in /root rimangono intatti fino a S1b (rollback sicuro).  
> Non cancellare /root/gas/ finché il deploy non è confermato funzionante.

### Rollback

```bash
# Se qualcosa va storto: l'utente gas si elimina, i dati originali sono intatti in /root
userdel -r gas
# /root/gas/ e /root/*.db rimangono intatti — nessun dato perso
```

---

## PASSO 4 — SSH key-only per l'utente 'gas'

**Obiettivo:** configurare il login via chiave pubblica per l'utente `gas` e verificarlo SU UNA SECONDA SESSIONE SSH prima di procedere.

> 🔴 **RECOVERY = console Hetzner**  
> **Non procedere se il pre-flight (passo 0) è fallito.**

> **REGOLA CRITICA:** Non chiudere la sessione root attiva finché una nuova sessione SSH via chiave per l'utente `gas` non è confermata funzionante.

### 4a. Copia la chiave pubblica

Hai bisogno della tua chiave pubblica SSH (es. `~/.ssh/id_ed25519.pub` o `~/.ssh/id_rsa.pub` sulla tua macchina locale).

**Sulla tua macchina locale** (non sul VPS), copia il contenuto della chiave:

```bash
# macchina locale — mostra la chiave pubblica
cat ~/.ssh/id_ed25519.pub
# oppure
cat ~/.ssh/id_rsa.pub
```

Annota il contenuto (es. `ssh-ed25519 AAAA... commento`).

### 4b. Installa la chiave sul VPS (sulla sessione root già aperta)

```bash
# Sul VPS, nella sessione root
mkdir -p /home/gas/.ssh
chmod 700 /home/gas/.ssh

# Incolla il contenuto della chiave pubblica qui sotto tra le virgolette
echo "ssh-ed25519 AAAA...TUA_CHIAVE_PUBBLICA... commento" >> /home/gas/.ssh/authorized_keys

chmod 600 /home/gas/.ssh/authorized_keys
chown -R gas:gas /home/gas/.ssh

# Verifica
cat /home/gas/.ssh/authorized_keys
# deve mostrare la tua chiave pubblica
```

### 4c. Test login in una NUOVA sessione SSH (tenendo aperta quella root)

**Apri un nuovo terminale sulla tua macchina locale** — NON chiudere la sessione root attiva sul VPS.

```bash
# Nuovo terminale locale — test login via key per utente gas
ssh -i ~/.ssh/id_ed25519 gas@204.168.251.92
# oppure con id_rsa:
ssh -i ~/.ssh/id_rsa gas@204.168.251.92
```

Output atteso:

```
Welcome to Ubuntu 24.04 LTS
gas@<hostname>:~$
```

### 4d. Verifica dalla sessione gas

```bash
# Nella sessione gas appena aperta
whoami    # → gas
id        # → uid=1001(gas) gid=1001(gas) groups=1001(gas)
ls ~      # → vedi gas/, .cache/ (eventuale)
```

### 4e. Verifica esito

- Login via key funzionante → **✅ CONFERMATO. Tieni aperta la sessione root. Procedi al passo 5.**
- Login via key fallito → **🔴 STOP. Diagnosi problema prima di procedere. NON toccare sshd_config.**

**Diagnosi se il login fallisce:**

```bash
# Sulla sessione root
# Controlla permission (devono essere esatte):
ls -la /home/gas/.ssh/
# .ssh: drwx------ (700), authorized_keys: -rw------- (600), owner: gas:gas

# Controlla SELinux/AppArmor (Ubuntu 24.04 usa AppArmor)
aa-status | grep sshd

# Controlla sshd log
journalctl -u ssh --since "5 minutes ago" | tail -30
```

### Rollback

```bash
# Rimuove accesso key per gas — root non è stato toccato
rm -rf /home/gas/.ssh
```

---

## PASSO 5 — sshd_config: key-only, no root login

**Obiettivo:** disabilitare l'autenticazione via password e il login root diretto via SSH.

> 🔴 **RECOVERY = console Hetzner**  
> **Non procedere se il pre-flight (passo 0) è fallito.**  
> **Non procedere se il passo 4 NON è confermato: la sessione gas via key deve essere aperta e funzionante.**

> **REGOLA CRITICA:** La sessione root attiva e la sessione gas via key devono essere entrambe aperte durante questo passo.

### 5a. Backup della configurazione attuale

```bash
# Sulla sessione root
cp /etc/ssh/sshd_config /etc/ssh/sshd_config.bak.$(date +%Y%m%d_%H%M%S)
ls -la /etc/ssh/sshd_config.bak.*
```

### 5b. Modifica sshd_config

```bash
# Mostra le righe rilevanti prima della modifica
grep -E "PasswordAuthentication|PermitRootLogin|PubkeyAuthentication" /etc/ssh/sshd_config
```

Modifica i parametri:

```bash
sed -i 's/^#\?PasswordAuthentication.*/PasswordAuthentication no/' /etc/ssh/sshd_config
sed -i 's/^#\?PermitRootLogin.*/PermitRootLogin no/' /etc/ssh/sshd_config
sed -i 's/^#\?PubkeyAuthentication.*/PubkeyAuthentication yes/' /etc/ssh/sshd_config
```

### 5c. Verifica le modifiche

```bash
grep -E "PasswordAuthentication|PermitRootLogin|PubkeyAuthentication" /etc/ssh/sshd_config
```

Output atteso:

```
PubkeyAuthentication yes
PasswordAuthentication no
PermitRootLogin no
```

### 5d. Validazione sintattica PRIMA del reload

```bash
sshd -t
# output atteso: nessun output = configurazione valida
# se c'è output = errore di sintassi → NON procedere, vedi rollback
```

> **Se `sshd -t` produce output di errore → rollback immediato (vedi sotto). NON eseguire il reload.**

### 5e. Reload (NON restart)

```bash
# reload preserva le sessioni attive; restart le chiude
systemctl reload ssh

# verifica che il servizio sia ancora attivo
systemctl status ssh | head -5
```

Output atteso: `Active: active (running)`

### 5f. Verifica finale su NUOVA sessione (terzo terminale)

**Apri un terzo terminale sulla tua macchina locale.**

```bash
# Test: login via key per gas → deve funzionare
ssh -i ~/.ssh/id_ed25519 gas@204.168.251.92
whoami  # → gas

# Test: login root via SSH → deve fallire (Permission denied)
ssh root@204.168.251.92
# atteso: Permission denied (publickey)

# Test: login con password → deve fallire
ssh -o PreferredAuthentications=password gas@204.168.251.92
# atteso: Permission denied (publickey)
```

### 5g. Verifica esito

- Tutti e tre i test del passo 5f passano → **✅ Configurazione hardening SSH completata.**
- Login gas via key fallisce dopo reload → **🔴 Rollback immediato (sessione root ancora aperta).**

### Rollback

```bash
# Sulla sessione root ancora aperta — ripristina il backup
BACKUP=$(ls /etc/ssh/sshd_config.bak.* | sort | tail -1)
cp "$BACKUP" /etc/ssh/sshd_config

# Valida prima di ricaricare
sshd -t && systemctl reload ssh

# Verifica ripristino
grep -E "PasswordAuthentication|PermitRootLogin" /etc/ssh/sshd_config
systemctl status ssh | head -3
```

Se anche il reload fallisce dopo il ripristino → **usa la console Hetzner** per riavviare il servizio SSH via VNC:

```bash
# Console Hetzner VNC
systemctl restart ssh
```

---

## PASSO 6 — Verifica finale

**Obiettivo:** riepilogo stato post-hardening e check integrale.

### 6a. Checklist verifica

Esegui dalla sessione `gas` (non root):

```bash
# Stato servizi
systemctl status unattended-upgrades | grep -E "Active|Loaded"
systemctl status fail2ban | grep -E "Active|Loaded"
systemctl status ssh | grep -E "Active|Loaded"

# fail2ban jail sshd
fail2ban-client status sshd

# Configurazione SSH
sshd -t && echo "sshd config OK"
grep -E "PasswordAuthentication|PermitRootLogin|PubkeyAuthentication" /etc/ssh/sshd_config

# Utente gas
id gas
ls -la /home/gas/

# Permessi .ssh
ls -la /home/gas/.ssh/
```

### 6b. Test lockout check

```bash
# Da un quarto terminale locale — tenta login root (deve fallire):
ssh root@204.168.251.92
# atteso: Permission denied (publickey).

# Login con password su gas (deve fallire):
ssh -o PreferredAuthentications=password gas@204.168.251.92
# atteso: Permission denied (publickey).
```

### 6c. Stato atteso finale

| Componente | Stato atteso |
|---|---|
| unattended-upgrades | active/enabled |
| fail2ban jail sshd | enabled, 0 banned |
| SSH: PasswordAuthentication | no |
| SSH: PermitRootLogin | no |
| SSH: PubkeyAuthentication | yes |
| Utente gas | uid=1001, home=/home/gas |
| /home/gas/.ssh | 700, authorized_keys 600 |
| /home/gas/gas/ | copia working dir, owned gas:gas |
| /root/gas/ | INTATTO (non cancellare fino a S1b) |

---

## TABELLA ROLLBACK RIEPILOGATIVA

| Passo | Rischio lockout | Rollback rapido | Recovery se lockout |
|---|---|---|---|
| 0 Pre-flight | N/A | N/A | N/A |
| 1 unattended-upgrades | Nessuno | `apt-get remove --purge unattended-upgrades` | N/A |
| 2 fail2ban | Nessuno (non tocca sshd) | `apt-get remove --purge fail2ban; rm /etc/fail2ban/jail.d/sshd-local.conf` | N/A |
| 3 Utente gas | Nessuno | `userdel -r gas` (dati originali in /root intatti) | N/A |
| **4 SSH key** | **⚠️ MEDIO** (se authorized_keys errato) | `rm -rf /home/gas/.ssh` | Console Hetzner VNC |
| **5 sshd_config** | **🔴 ALTO** (lockout se config errata) | `cp sshd_config.bak.* /etc/ssh/sshd_config && sshd -t && systemctl reload ssh` | Console Hetzner VNC → `systemctl restart ssh` |
| 6 Verifica finale | Nessuno | N/A | N/A |

---

## NOTE PER FETTE SUCCESSIVE (FUORI SCOPE S1 — proposta)

Le seguenti attività NON sono in scope di questo runbook. Decisione di includerle spetta all'umano:

**FETTA 2 — proposta (S1b):**

1. **systemd unit GAS** con `MemoryHigh=1500M` / `MemoryMax=2000M` — FINDING no-swap (sonda 2026-07-02): il box non ha swap, un OOM uccide GAS e potenzialmente il bot trading. La unit systemd con limiti di memoria garantisce un degradamento prevedibile (`Restart=always`) invece di un OOM casuale. Parametri da affinare con misura reale dopo il primo avvio.

2. **swap file 2-4 GiB** — opzione cuscinetto (costo: ~2-4 GiB su 70 GiB liberi) per macchina h24 non presidiata. Decisione aperta da sonda S0.

3. **Spostamento VECTORS_DB** — `GAS_VECTORS_DB` configurabile via env (già fatto in review #31). Al deploy va impostato esplicitamente sotto `/home/gas/gas/` e non sotto `/root`. Da fare in concomitanza con la prima run GAS come utente gas.

4. **ollama on-demand vs always-on** — decisione aperta da stato_progetto.md: su 7.6 GiB condivisi, un modello 3B always-on riduce il margine. Valutare spawn on-demand.

**Queste voci NON fanno parte di S1. Includile nel prossimo scope se deciso.**
