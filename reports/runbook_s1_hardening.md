# RUNBOOK — FASE 5 S1: Hardening SSH + Base VPS
**Target:** Hetzner CX33, Helsinki, Ubuntu 24.04 — `root@204.168.251.92`  
**Revisione:** 2026-07-04 v3  
**Eseguito manualmente dall'umano** in una sessione SSH con console Hetzner aperta.

---

## AVVERTENZE GLOBALI

> **NON eseguire questo runbook come script automatico.**  
> Ogni passo va eseguito, verificato e confermato prima di procedere.  
> Un passo saltato o eseguito fuori ordine può causare **lockout permanente** senza console.

> **Console Hetzner = unica rete di sicurezza contro lockout.**  
> Se la console non è accessibile, **non toccare sshd** — fermati al passo 0.

---

## PASSO 0 — PRE-FLIGHT (BLOCCANTE)

**Obiettivo:** verificare che la console Hetzner sia accessibile e funzionante PRIMA di qualsiasi modifica.

### Azioni (dal browser, non dalla sessione SSH)

1. Vai su **console.hetzner.com** dal browser.
2. Seleziona il server CX33 Helsinki → pulsante **Console** in alto a destra.
3. Nella console VNC che si apre, premi `Invio`.
4. Effettua login come `root` con la password root del VPS.
5. Verifica che il prompt risponda.

### Output atteso

```
Ubuntu 24.04 LTS
<hostname> login: root
Password: ****
root@<hostname>:~#
```

### Verifica prima di procedere

| Esito console VNC | Decisione |
|---|---|
| Accessibile + login root OK | ✅ Procedi al passo 1 |
| Non accessibile / login fallito | 🔴 **STOP — non toccare sshd in nessun caso** |

### Rollback

N/A — nessuna modifica eseguita.

---

## PASSO 1 — unattended-upgrades

**Obiettivo:** aggiornamenti automatici di sicurezza (kernel, librerie).  
**Rischio:** basso. Reversibile. Non tocca sshd.

### 1a. Verifica distro e aggiornamento indice

```bash
lsb_release -cs
# output atteso: noble

apt-get update -qq
# Nota: se dà "Could not get lock /var/lib/dpkg/lock-frontend", unattended-upgrades sta girando in background — attendere 1-2 minuti o fermarlo temporaneamente con `systemctl stop unattended-upgrades`.
```

### 1b. Installazione

```bash
apt-get install -y unattended-upgrades apt-listchanges
```

Output atteso (uno dei due):

```
unattended-upgrades is already the newest version (...)
```

oppure:

```
Setting up unattended-upgrades (2.x) ...
```

### 1c. Configurazione (non interattiva)

```bash
cat > /etc/apt/apt.conf.d/20auto-upgrades << 'EOF'
APT::Periodic::Update-Package-Lists "1";
APT::Periodic::Unattended-Upgrade "1";
APT::Periodic::AutocleanInterval "7";
EOF
```

### 1d. Verifica

```bash
cat /etc/apt/apt.conf.d/20auto-upgrades
# deve mostrare i 3 valori sopra

systemctl status unattended-upgrades | grep -E "Active:"
# atteso: Active: active (running)  oppure  Active: active (exited) — entrambi OK
```

### Rollback

```bash
apt-get remove --purge unattended-upgrades -y
rm -f /etc/apt/apt.conf.d/20auto-upgrades
```

---

## PASSO 2 — fail2ban

**Obiettivo:** bloccare IP che fanno brute-force su SSH.  
**Rischio:** basso. Reversibile. Non tocca sshd_config.

### 2a. Installazione

```bash
apt-get install -y fail2ban
```

### 2b. Jail SSH

> **Nota Ubuntu 24.04:** `/var/log/auth.log` esiste se rsyslog è attivo, ma fail2ban su
> Ubuntu 24.04 preferisce leggere da journald. `backend = auto` sceglie il metodo corretto
> automaticamente (journald se disponibile, file altrimenti).

```bash
cat > /etc/fail2ban/jail.d/sshd-local.conf << 'EOF'
[sshd]
enabled  = true
port     = ssh
filter   = sshd
backend  = auto
maxretry = 5
bantime  = 1h
findtime = 10m
EOF
```

### 2c. Avvio

```bash
systemctl enable fail2ban
systemctl restart fail2ban
```

### 2d. Verifica

```bash
systemctl status fail2ban | grep -E "Active:"
# atteso: Active: active (running)

fail2ban-client status sshd
```

Output atteso:

```
Status for the jail: sshd
|- Filter
|  |- Currently failed: 0
|  `- Total failed:     0
`- Actions
   |- Currently banned: 0
   `- Total banned:     0
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

**Obiettivo:** creare l'utente sotto cui girerà GAS. Spostare working dir, cache modelli e DB fuori da `/root`. NON avviare GAS ora.  
**Rischio:** medio (modifica struttura file). Reversibile. Non tocca sshd.

### 3a. Verifica struttura attuale

```bash
ls -la /root/
ls -la /root/gas/ 2>/dev/null || echo "no /root/gas"
find /root -name ".gas_*.db" -o -name ".gas_history.json" -o -name ".gas_*.jsonl" 2>/dev/null
ls -la /root/.cache/ 2>/dev/null || echo "no /root/.cache"

# Annota i path reali prima di procedere al passo 3b
```

### 3b. Verifica UID disponibile

> **Nota:** il bot trading potrebbe già occupare uid/gid 1001.  
> Verifica prima di assegnare l'utente.

```bash
getent passwd | awk -F: '$3 >= 1000 {print $1, $3}' | sort -k2 -n
# mostra gli utenti non-sistema; annota quale uid è il prossimo libero
```

### 3c. Creazione utente

```bash
useradd --create-home --shell /bin/bash --comment "GAS runtime" gas
# verifica
id gas
# output atteso: uid=<N>(gas) gid=<N>(gas) groups=<N>(gas)
```

### 3d-pre. Check: GAS non deve essere in esecuzione durante la copia del DB

> **Copiare `.gas_memory.db` mentre GAS scrive = rischio di DB corrotto o snapshot incoerente.**  
> La memoria non deve mentire. Verificare SEMPRE prima di copiare.  
> (Attualmente GAS NON gira sul VPS, ma il check resta come guardia permanente.)

```bash
pgrep -f gas.py && echo "STOP: GAS in esecuzione, la copia del DB sarebbe inconsistente" \
  || echo "GAS non attivo, copia sicura"
# Se il primo ramo si attiva → fermare GAS prima di procedere:
#   pkill -f gas.py   oppure   systemctl stop gas   (dipende da come è avviato)
```

### 3d. Spostamento working directory GAS

```bash
# Adatta /root/gas al path reale rilevato al passo 3a
cp -a /root/gas /home/gas/gas
chown -R gas:gas /home/gas/gas
ls -la /home/gas/gas/ | head -20
```

### 3e. Spostamento model cache fastembed

```bash
# Verifica cosa c'è in /root/.cache
ls /root/.cache/ 2>/dev/null || echo "cache assente"

# Se esiste (fastembed scarica in ~/.cache/fastembed o ~/.cache/huggingface):
if [ -d /root/.cache ]; then
  cp -a /root/.cache /home/gas/.cache
  chown -R gas:gas /home/gas/.cache
  echo "cache copiata"
fi
ls /home/gas/.cache/ 2>/dev/null
```

### 3f. Spostamento DB extra in /root (se presenti fuori da /root/gas/)

```bash
# I DB dentro /root/gas/ sono già stati copiati al passo 3d.
# Questo loop copia solo eventuali DB direttamente in /root/:
for f in /root/.gas_*.db /root/.gas_*.jsonl /root/.gas_history.json; do
  [ -e "$f" ] || continue
  cp -a "$f" /home/gas/
  chown gas:gas "/home/gas/$(basename "$f")"
  echo "copiato: $f"
done
ls -la /home/gas/.gas_* 2>/dev/null || echo "nessun DB extra in /root"
```

### 3g. Verifica ownership

```bash
find /home/gas -not -user gas -not -group gas 2>/dev/null | head -20
# output atteso: nessuna riga (tutto owned da gas:gas)
```

### 3h. Verifica struttura home

```bash
ls -la /home/gas/
# atteso: gas/ (working dir), .cache/ (eventuale), .gas_* (eventuali)
```

> **NON avviare GAS come utente gas ora.**  
> I path originali in `/root` rimangono intatti (rollback sicuro).  
> Non cancellare `/root/gas/` finché il deploy non è confermato funzionante.

### Rollback

```bash
userdel -r gas
# /root/gas/ e i DB in /root/ rimangono intatti — nessun dato perso
```

---

## PASSO 4 — SSH key-only per l'utente 'gas'

> 🔴 **RECOVERY = console Hetzner**  
> **Non procedere se il pre-flight (passo 0) è fallito.**

> **REGOLA CRITICA:** Non chiudere la sessione root attiva finché una nuova sessione SSH  
> via chiave per l'utente `gas` non è confermata funzionante al passo 4d.

**Obiettivo:** installare la chiave pubblica per `gas` e verificarne il funzionamento su una seconda sessione SSH indipendente.

### 4a. Ottieni la chiave pubblica (sulla tua macchina locale)

```bash
# Sulla tua macchina LOCALE — mostra la chiave pubblica da copiare
cat ~/.ssh/id_ed25519.pub
# oppure
cat ~/.ssh/id_rsa.pub
```

Copia il contenuto (riga intera: `ssh-ed25519 AAAA... commento`).

### 4b. Installa la chiave sul VPS (sessione root)

```bash
# Sul VPS, nella sessione root
mkdir -p /home/gas/.ssh
chmod 700 /home/gas/.ssh

# Incolla la tua chiave pubblica al posto del placeholder
echo "INCOLLA_QUI_LA_CHIAVE_PUBBLICA_COMPLETA" >> /home/gas/.ssh/authorized_keys

chmod 600 /home/gas/.ssh/authorized_keys
chown -R gas:gas /home/gas/.ssh
```

### 4c. Verifica permessi e contenuto

```bash
ls -la /home/gas/.ssh/
# atteso:
# drwx------  .ssh      (700, owned gas:gas)
# -rw-------  authorized_keys  (600, owned gas:gas)

cat /home/gas/.ssh/authorized_keys
# deve mostrare la tua chiave pubblica
```

### 4d. Test login in una NUOVA sessione SSH

> **Apri un NUOVO terminale sulla tua macchina locale.**  
> NON chiudere la sessione root attiva sul VPS.

```bash
# Nuovo terminale locale
ssh -i ~/.ssh/id_ed25519 gas@204.168.251.92
# oppure
ssh -i ~/.ssh/id_rsa gas@204.168.251.92
```

Output atteso:

```
Welcome to Ubuntu 24.04 LTS (GNU/Linux 6.x.x-xx-generic x86_64)
gas@<hostname>:~$
```

Dalla sessione gas:

```bash
whoami    # → gas
id        # → uid=<N>(gas) gid=<N>(gas) groups=<N>(gas)
ls ~      # → gas/  e altri file copiati
```

### 4e. Esito

| Risultato | Azione |
|---|---|
| Login gas via key ✅ | Tieni aperta la sessione root. Procedi al passo 5. |
| Login fallito 🔴 | STOP. Diagnosi sotto. NON toccare sshd_config. |

**Diagnosi se il login fallisce:**

```bash
# Sulla sessione root
ls -la /home/gas/.ssh/
# .ssh deve essere 700, authorized_keys 600, owner gas:gas

journalctl -u ssh --since "2 minutes ago" | tail -30
# cerca "Authentication refused" o "bad ownership"
```

### Rollback

```bash
rm -rf /home/gas/.ssh
# accesso key rimosso; root è ancora accessibile via password
```

---

## PASSO 5 — sshd_config: key-only, no root login

> 🔴 **RECOVERY = console Hetzner**  
> **Non procedere se il pre-flight (passo 0) è fallito.**  
> **Non procedere se il passo 4 NON è confermato: la sessione gas via key deve essere aperta.**

> **REGOLA CRITICA:** Mantieni aperte ENTRAMBE le sessioni (root + gas via key) durante  
> l'intero passo 5. La sessione root è la rete di rollback manuale; la console Hetzner è  
> la rete finale.

**Obiettivo:** disabilitare autenticazione password e login root diretto via SSH.

### 5a. Controlla i dropin esistenti (specifico Ubuntu 24.04 + Hetzner)

> **Nota:** Hetzner cloud-init può aver scritto `/etc/ssh/sshd_config.d/50-cloud-init.conf`
> con `PasswordAuthentication yes`. Su Ubuntu 24.04 i dropin vengono letti in ordine
> alfabetico; un file con prefisso `99-` sovrascrive `50-cloud-init.conf`.

```bash
ls /etc/ssh/sshd_config.d/ 2>/dev/null || echo "directory dropin assente"
cat /etc/ssh/sshd_config.d/50-cloud-init.conf 2>/dev/null || echo "nessun dropin cloud-init"

# Mostra anche le direttive rilevanti nella config principale
grep -E "PasswordAuthentication|PermitRootLogin|PubkeyAuthentication" /etc/ssh/sshd_config
```

### 5b. Crea il dropin di hardening

> Invece di modificare il file principale (rischio con `sed` su configurazioni multi-riga),
> si aggiunge un dropin `99-hardening.conf` che prende precedenza su tutti i dropin
> precedenti (incluso `50-cloud-init.conf`).

```bash
cat > /etc/ssh/sshd_config.d/99-hardening.conf << 'EOF'
# Hardening S1 — 2026-07-04
PasswordAuthentication no
PermitRootLogin no
PubkeyAuthentication yes
EOF

chmod 600 /etc/ssh/sshd_config.d/99-hardening.conf
```

### 5c. Verifica il dropin

```bash
cat /etc/ssh/sshd_config.d/99-hardening.conf
# deve mostrare le 3 direttive sopra
```

### 5d. Validazione sintattica PRIMA del reload

```bash
sshd -t
# output atteso: nessun output = configurazione valida
# qualsiasi output = errore → rollback immediato, NON procedere al reload
```

> **Se `sshd -t` produce output di errore → esegui il rollback sotto. NON fare il reload.**

### 5e-pre. Verifica socket activation (Ubuntu 24.04)

> **Ubuntu 24.04 usa per default `ssh.socket` (socket activation systemd):**  
> il demone sshd viene avviato on-demand dal socket, non come servizio permanente.  
> `ssh.service` gestisce la sessione una volta stabilita; `ssh.socket` ascolta sulla porta 22.  
> Ricaricare solo il service lascerebbe il socket col vecchio listener — il reload della  
> config deve coinvolgere anche il socket.
>
> **root e gas restano connessi** durante `restart ssh.socket`: il socket riavvia solo il  
> listener delle nuove connessioni in ingresso, NON chiude le sessioni SSH già stabilite.

```bash
systemctl is-active ssh.socket
# output "active"  → socket activation attiva → vedi procedura sotto
# output "inactive" / "unknown" → procedi con il reload normale al 5e
```

**Se `ssh.socket` è active:**

```bash
# Valida prima
sshd -t
# Se OK:
systemctl reload ssh          # ricarica config nelle sessioni attive
systemctl restart ssh.socket  # riavvia il listener per le nuove connessioni
# root e gas rimangono connessi — solo i nuovi tentativi di login usano la nuova config
```

### 5e. Reload (NON restart)

```bash
# reload: ricarica la config senza interrompere le sessioni attive
# restart: chiude tutte le sessioni — NON usare restart
systemctl reload ssh

systemctl status ssh | grep -E "Active:"
# atteso: Active: active (running)
```

### 5f. Verifica su nuova sessione (terzo terminale)

> **Apri un TERZO terminale sulla tua macchina locale.**

```bash
# Test 1 — login gas via key (deve funzionare)
ssh -i ~/.ssh/id_ed25519 gas@204.168.251.92
whoami   # → gas

# Test 2 — login root via SSH (deve fallire)
ssh root@204.168.251.92
# atteso: Permission denied (publickey).

# Test 3 — login con password (deve fallire)
# IMPORTANTE: aggiungere -o PubkeyAuthentication=no, altrimenti il client tenta
# la key prima della password e il rifiuto riporta "publickey" anche se la password
# fosse ancora abilitata — il test sarebbe falsato.
ssh -o PreferredAuthentications=password -o PubkeyAuthentication=no gas@204.168.251.92
# atteso: "Permission denied (password)." IMMEDIATO (nessuna prompt)
# Se chiede la password → password auth ancora attiva → hardening NON applicato
```

### 5g. Esito

| Risultato | Azione |
|---|---|
| Tutti e 3 i test passano ✅ | Hardening SSH completato. Procedi al passo 6. |
| Test 1 (gas via key) fallisce 🔴 | Rollback immediato (sessione root ancora aperta). |

### Rollback

```bash
# Sulla sessione root ancora aperta
rm /etc/ssh/sshd_config.d/99-hardening.conf

# Valida e ricarica
sshd -t && systemctl reload ssh

# Verifica che il login con password torni a funzionare
grep -E "PasswordAuthentication|PermitRootLogin" /etc/ssh/sshd_config /etc/ssh/sshd_config.d/*.conf 2>/dev/null
```

Se anche il reload fallisce dopo il ripristino → **usa la console Hetzner VNC**:

```bash
# Console Hetzner VNC (ultimo rimedio)
systemctl restart ssh
```

---

## PASSO 6 — Verifica finale

**Obiettivo:** riepilogo stato post-hardening e check integrale.

### 6a. Checklist stato servizi (dalla sessione gas)

```bash
systemctl status unattended-upgrades | grep -E "Active:"
systemctl status fail2ban | grep -E "Active:"
systemctl status ssh | grep -E "Active:"

fail2ban-client status sshd

sshd -t && echo "sshd config: OK"

# Direttive hardening attive (inclusi dropin)
sshd -T | grep -E "passwordauthentication|permitrootlogin|pubkeyauthentication"
# atteso:
# passwordauthentication no
# permitrootlogin no
# pubkeyauthentication yes
```

> **Nota:** `sshd -T` mostra la configurazione effettiva consolidata (main config + dropin),
> non solo quello che è scritto nel file. È la fonte di verità per la config attiva.

### 6b. Test lockout (da un quarto terminale locale)

```bash
# Login root via SSH — deve fallire
ssh root@204.168.251.92
# atteso: Permission denied (publickey).

# Login gas con password — deve fallire
# IMPORTANTE: -o PubkeyAuthentication=no obbliga il client a usare solo password;
# senza questo flag il test è falsato (vedi nota passo 5f).
ssh -o PreferredAuthentications=password -o PubkeyAuthentication=no gas@204.168.251.92
# atteso: "Permission denied (password)." IMMEDIATO (nessuna prompt)
# Se chiede la password → password auth ancora attiva → hardening NON applicato
```

### 6c. Stato finale atteso

| Componente | Stato atteso |
|---|---|
| unattended-upgrades | active (running o exited) |
| fail2ban jail sshd | enabled, 0 banned |
| `sshd -T` passwordauthentication | no |
| `sshd -T` permitrootlogin | no |
| `sshd -T` pubkeyauthentication | yes |
| `/etc/ssh/sshd_config.d/99-hardening.conf` | presente, chmod 600 |
| Utente gas | creato, home=/home/gas |
| `/home/gas/.ssh` | 700, authorized_keys 600 |
| `/home/gas/gas/` | copia working dir, owner gas:gas |
| `/root/gas/` | INTATTO (non cancellare fino a S1b) |

---

## TABELLA ROLLBACK RIEPILOGATIVA

| Passo | Rischio lockout | Rollback | Recovery se lockout |
|---|---|---|---|
| 0 Pre-flight | N/A | N/A | N/A |
| 1 unattended-upgrades | Nessuno | `apt-get remove --purge unattended-upgrades; rm /etc/apt/apt.conf.d/20auto-upgrades` | N/A |
| 2 fail2ban | Nessuno | `systemctl stop fail2ban; apt-get remove --purge fail2ban; rm /etc/fail2ban/jail.d/sshd-local.conf` | N/A |
| 3 Utente gas | Nessuno | `userdel -r gas` (dati originali in /root intatti) | N/A |
| **4 SSH key** | **⚠️ MEDIO** | `rm -rf /home/gas/.ssh` | Console Hetzner VNC |
| **5 sshd_config** | **🔴 ALTO** | `rm /etc/ssh/sshd_config.d/99-hardening.conf && sshd -t && systemctl reload ssh` | Console Hetzner VNC → `systemctl restart ssh` |
| 6 Verifica finale | Nessuno | N/A | N/A |

---

## PROPOSTA FETTE SUCCESSIVE (FUORI SCOPE S1 — decisione umana)

Le seguenti attività NON sono in scope di questo runbook:

**Candidati per S1b:**

1. **swap file 2–4 GiB** — il box non ha swap (FINDING no-swap, sonda 2026-07-02). Su 7.6 GiB
   condivisi con bot trading e GAS, un picco = OOM killer senza cuscinetto. Costo: 2–4 GiB su
   70 GiB liberi. Comando: `fallocate -l 2G /swapfile && chmod 600 /swapfile && mkswap /swapfile && swapon /swapfile` + riga in `/etc/fstab`.

2. **systemd unit GAS** con `MemoryHigh=1500M` / `MemoryMax=2000M` — limita il blast radius di
   GAS in caso di picco (embedder + reindex), garantisce `Restart=always` prevedibile invece di
   OOM casuale. Parametri da affinare con misura reale dopo il primo avvio.

3. **Spostamento VECTORS_DB** — al primo avvio GAS come utente `gas`, impostare
   `GAS_VECTORS_DB=/home/gas/gas/.gas_vectors.db` via env/systemd unit, altrimenti il layer
   vettoriale usa il path di default che potrebbe puntare a `/root`.

4. **ollama on-demand** — 3B always-on su 7.6 GiB condivisi lascia poco margine. Valutare
   spawn on-demand (avvio al primo turno ollama, unload dopo). Decisione aperta.

**Queste voci NON fanno parte di S1. Includile nel prossimo scope se deciso dall'umano.**
