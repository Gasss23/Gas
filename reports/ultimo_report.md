# Report task — sonda ambiente cloud Claude Code (da telefono)
**Data:** 2026-07-01
**Scope:** Caratterizzazione READ-ONLY di questo ambiente cloud (sandbox Anthropic gestita, NON VPS, NON PC utente) + validazione loop telefono→cloud→CI→review PRIMA di affidargli lavoro reale. Nessun codice, nessuna modifica al motore.

---

## §DECISIONI PER L'UMANO

**Domanda: quali classi di task Gas sono SICURE da telefono (in questa sessione cloud), e qual è il confine?**

Risposta basata sui fatti raccolti in §EVIDENZA:

**SICURE, senza limitazioni:**
- Task doc-only (reports, roadmap, stato_progetto, handoff) — nessun gate richiesto, rischio nullo.
- Probe/analisi read-only del codice (come questo stesso task).

**SICURE, CON il gate attivo (verificato presente):**
- Modifiche a `gas.py`/`modules/`/`tests/` — perché in questo ambiente sono presenti **entrambi** i meccanismi di sicurezza previsti da CLAUDE.md sez. 3:
  1. `.claude/agents/revisore.md` (PRESENTE) — il subagent di review è invocabile.
  2. `.claude/settings.json` ha il gate deterministico `PreToolUse` su Bash che lancia `.claude/hooks/review_gate.sh` (rete di sicurezza), più `SessionStart` che re-inietta le 4 regole critiche dopo un compact, più `SessionEnd`/`Stop` per reporting/backup automatico.
  Quindi un task che tocca il motore da telefono È sicuro, A CONDIZIONE che il gate venga rispettato (mai bypassare con `--no-verify` o auto-commit).

**CONFINE — cose che questo ambiente NON può verificare/eseguire per davvero, da tenere presenti prima di affidargli task reali:**
1. **Sandbox OS (bwrap) ASSENTE.** `command -v bwrap` → non trovato. Qualsiasi comportamento che dipende dal sandbox `run_command` (i 5 test T11c2/T11e/T12a/T12c/T12e, la sicurezza h24 vera) qui **fallisce sempre** per assenza del binario, non per un bug — non è possibile validare qui il comportamento sandbox-dipendente. La verifica reale resta la CI (che installa bwrap esplicitamente) o un ambiente con bwrap preinstallato.
2. **Nessun provider LLM reale configurato.** Le variabili tipo `GITHUB_TOKEN`/`AWS_SECRET_ACCESS_KEY` viste in `env` sono placeholder (`proxy-injected`) del proxy di rete, non credenziali vere; non ci sono chiavi Claude/Gemini/Groq reali. Task che richiedono chiamate LLM vere (`gas doctor` con ping reali, `run_turn` end-to-end, `gas telegram` con bot vero) NON sono eseguibili qui — solo codice/test a zero token.
3. **Dipendenze pesanti assenti di default.** `pytest, fastembed, onnxruntime, openai, numpy` non risultano importabili finché non si installano esplicitamente (`pip install -r requirements.txt`, verificato in una sessione precedente con un venv temporaneo). Non è un blocco, ma un passo manuale necessario prima di eseguire la suite di test — da tenere a mente per non dare per scontato che "il venv sia pronto".
4. **Ambiente effimero, scollegato da VPS/PC.** Nessun task qui può toccare stato reale di produzione (diario/CRM veri, deploy VPS) — solo codice, git, CI.

**Proposta (NON eseguita, solo segnalata):** se si vuole rendere questo ambiente cloud in grado di validare ANCHE il ramo sandbox-dipendente senza aspettare la CI, si potrebbe aggiungere un hook `SessionStart` che installa `bubblewrap` via apt (stesso comando già usato dalla CI in `.github/workflows/ci.yml`), analogamente a come `settings.json` già inietta le regole critiche post-compact. È una scelta di setup ambiente, non di codice motore — decisione umana, non eseguita in questa sonda.

---

## §SCOPE & ESITO

| Fetta | Esito |
|---|---|
| Fetta 1 — Sonda ambiente (read-only) | `FATTA` |
| Fetta 2 — Report (ultimo_report.md + handoff.md) | `FATTA` |
| Fetta 3 — Commit + push (solo reports/) | `FATTA` |
| Esecuzione suite di test / installazione pacchetti | `SALTATA — vietato esplicitamente dallo scope (VIETATO: lanciare la suite, installare pacchetti)` |
| Modifiche a gas.py/brains/modules/tests | `SALTATA — fuori scope per design (sonda read-only)` |

---

## §EVIDENZA

### Ambiente

```
=== uname -a ===
Linux vm 6.18.5 #1 SMP PREEMPT_DYNAMIC @0 x86_64 x86_64 x86_64 GNU/Linux

=== nproc ===
4

=== free -h ===
               total        used        free      shared  buff/cache   available
Mem:            15Gi       521Mi        14Gi       4.2Mi       475Mi        15Gi
Swap:             0B          0B          0B

=== df -h . ===
Filesystem      Size  Used Avail Use% Mounted on
/dev/vda        252G  7.2G   30G  20% /

=== /etc/os-release ===
PRETTY_NAME="Ubuntu 24.04.4 LTS"
NAME="Ubuntu"
VERSION_ID="24.04"
VERSION="24.04.4 LTS (Noble Numbat)"
VERSION_CODENAME=noble
ID=ubuntu
ID_LIKE=debian
HOME_URL="https://www.ubuntu.com/"
SUPPORT_URL="https://help.ubuntu.com/"
BUG_REPORT_URL="https://bugs.launchpad.net/ubuntu/"
PRIVACY_POLICY_URL="https://www.ubuntu.com/legal/terms-and-policies/privacy-policy"
UBUNTU_CODENAME=noble
LOGO=ubuntu-logo
```

```
=== python3 --version ===
Python 3.11.15

=== pip --version ===
pip 24.0 from /usr/lib/python3/dist-packages/pip (python 3.11)

=== node --version ===
v22.22.2

=== git --version ===
git version 2.43.0
```

```
=== bwrap/socat ===
bwrap: ASSENTE
socat: ASSENTE

=== proxy env ===
CCR_AGENT_PROXY_ENABLED=1
no_proxy=localhost,127.0.0.1,::1,127.0.0.0/8,0.0.0.0/8,::,169.254.0.0/16,anthropic.com,.anthropic.com,*.anthropic.com,registry.npmjs.org,jsr.io,npm.jsr.io,pypi.org,files.pythonhosted.org,index.crates.io,proxy.golang.org,host.docker.internal,10.0.0.0/8,172.16.0.0/12,192.168.0.0/16,100.64.0.0/10,.svc.cluster.local,*.svc.cluster.local
GH_TOKEN=proxy-injected
CCR_UPSTREAM_PROXY_ENABLED=1
CLOUDSDK_PROXY_TYPE=http
GITHUB_TOKEN=proxy-injected
CLOUDSDK_AUTH_ACCESS_TOKEN=proxy-injected
CLOUDSDK_PROXY_PORT=33447
CLAUDE_CODE_PROXY_RESOLVES_HOSTS=true
CCR_TEST_GITPROXY=1
AWS_SECRET_ACCESS_KEY=proxy-injected
https_proxy=http://127.0.0.1:33447
GLOBAL_AGENT_NO_PROXY=localhost,127.0.0.1,::1,127.0.0.0/8,0.0.0.0/8,::,169.254.0.0/16,anthropic.com,.anthropic.com,*.anthropic.com,registry.npmjs.org,jsr.io,npm.jsr.io,pypi.org,files.pythonhosted.org,index.crates.io,proxy.golang.org,host.docker.internal,10.0.0.0/8,172.16.0.0/12,192.168.0.0/16,100.64.0.0/10,.svc.cluster.local,*.svc.cluster.local
ELECTRON_GET_USE_PROXY=1
JAVA_TOOL_OPTIONS=-Djavax.net.ssl.trustStore=/root/.ccr/java-truststore.p12 -Djavax.net.ssl.trustStorePassword=changeit -Djavax.net.ssl.trustStoreType=PKCS12 -Dhttps.proxyHost=127.0.0.1 -Dhttps.proxyPort=33447 -Dhttp.nonProxyHosts=localhost|127.0.0.1|::1|127.*|0.*|::|169.254.*|anthropic.com|*.anthropic.com|*.anthropic.com|registry.npmjs.org|jsr.io|npm.jsr.io|pypi.org|files.pythonhosted.org|index.crates.io|proxy.golang.org|host.docker.internal|10.*|172.16.*|172.17.*|172.18.*|172.19.*|172.20.*|172.21.*|172.22.*|172.23.*|172.24.*|172.25.*|172.26.*|172.27.*|172.28.*|172.29.*|172.30.*|172.31.*|192.168.*|100.64.0.0/10|*.svc.cluster.local|*.svc.cluster.local -Djdk.http.auth.tunneling.disabledSchemes= -Djdk.http.auth.proxying.disabledSchemes=
NO_PROXY=localhost,127.0.0.1,::1,127.0.0.0/8,0.0.0.0/8,::,169.254.0.0/16,anthropic.com,.anthropic.com,*.anthropic.com,registry.npmjs.org,jsr.io,npm.jsr.io,pypi.org,files.pythonhosted.org,index.crates.io,proxy.golang.org,host.docker.internal,10.0.0.0/8,172.16.0.0/12,192.168.0.0/16,100.64.0.0/10,.svc.cluster.local,*.svc.cluster.local
AWS_ACCESS_KEY_ID=proxy-injected
HTTPS_PROXY=http://127.0.0.1:33447
npm_config_noproxy=localhost,127.0.0.1,::1,127.0.0.0/8,0.0.0.0/8,::,169.254.0.0/16,anthropic.com,.anthropic.com,*.anthropic.com,registry.npmjs.org,jsr.io,npm.jsr.io,pypi.org,files.pythonhosted.org,index.crates.io,proxy.golang.org,host.docker.internal,10.0.0.0/8,172.16.0.0/12,192.168.0.0/16,100.64.0.0/10,.svc.cluster.local,*.svc.cluster.local
YARN_HTTPS_PROXY=http://127.0.0.1:33447
CLOUDSDK_PROXY_ADDRESS=127.0.0.1
npm_config_https_proxy=http://127.0.0.1:33447
DOCKER_HTTPS_PROXY=http://127.0.0.1:33447
GLOBAL_AGENT_HTTPS_PROXY=http://127.0.0.1:33447
```

### Repo + macchina di sicurezza (inventario)

```
=== git rev-parse --abbrev-ref HEAD ===
claude/phone-gas-development-10svqc

=== git remote -v ===
origin	http://local_proxy@127.0.0.1:41729/git/Gasss23/Gas (fetch)
origin	http://local_proxy@127.0.0.1:41729/git/Gasss23/Gas (push)

=== git log --oneline -5 ===
c728b01 docs(report): fine task prova sviluppo da telefono — gas version, CI green
d992c47 feat(gas): aggiungi comando `gas version`
f3a8acc docs(stato): sonda doctor sez.8 — confermata copertura completa memoria SQLite a freddo
4ac00e8 docs(report): sonda doctor memoria SQLite — già coperto, niente da fare
eebde1a docs(roadmap): chiudi R-reidx-deps, riduci R-vec-3 (2026-06-29)
```

```
=== ls -la .claude .claude/agents .claude/hooks .claude/commands ===
total 24
drwxr-xr-x  5 root root 4096 Jul  1 18:47 .
drwxr-xr-x 11 root root 4096 Jul  1 16:02 ..
drwxr-xr-x  2 root root 4096 Jul  1 11:12 agents
drwxr-xr-x  2 root root 4096 Jul  1 11:12 commands
drwxr-xr-x  2 root root 4096 Jul  1 11:12 hooks
-rw-r--r--  1 root root 1860 Jul  1 11:12 settings.json
--- .claude/agents ---
total 64
drwxr-xr-x 2 root root  4096 Jul  1 11:12 .
drwxr-xr-x 5 root root  4096 Jul  1 18:47 ..
-rw-r--r-- 1 root root 49491 Jul  1 11:12 memoria_revisore.md
-rw-r--r-- 1 root root  2740 Jul  1 11:12 revisore.md
--- .claude/hooks ---
total 20
drwxr-xr-x 2 root root 4096 Jul  1 11:12 .
drwxr-xr-x 5 root root 4096 Jul  1 18:47 ..
-rwxr-xr-x 1 root root 2567 Jul  1 11:12 review_gate.sh
-rwxr-xr-x 1 root root 2149 Jul  1 11:12 scrivi_rep.sh
-rwxr-xr-x 1 root root 2287 Jul  1 11:12 session_end.sh
--- .claude/commands ---
total 16
drwxr-xr-x 2 root root 4096 Jul  1 11:12 .
drwxr-xr-x 5 root root 4096 Jul  1 18:47 ..
-rw-r--r-- 1 root root 4378 Jul  1 11:12 fine-task.md
```

```
=== revisore.md presence ===
revisore: PRESENTE
```

```
== .claude/settings.json ==
{
  "model": "claude-sonnet-4-6",
  "env": {
    "DISABLE_NON_ESSENTIAL_MODEL_CALLS": "1"
  },
  "hooks": {
    "SessionStart": [
      {
        "matcher": "compact",
        "hooks": [
          {
            "type": "command",
            "command": "echo '=== REGOLE CRITICHE GAS (post-compact) === (1) REVISORE OBBLIGATORIO: prima di ogni commit che tocca gas.py/brains/modules/tests/, invocare il subagent revisore e attendere il verdetto APPROVATO. (2) SCOPE: fare SOLO lo scope dato — se serve altro, fermati e scrivilo in DECISIONI UMANE RICHIESTE nel report. (3) REPORTING CANONICO: a fine task scrivere reports/ultimo_report.md, committare+pushare, poi stampare: path report + hash commit + cat integrale + git diff --stat. (4) NO OPERAZIONI IRREVERSIBILI nel loop (niente merge/gc/restore/delete non autorizzati).'"
          }
        ]
      }
    ],
    "SessionEnd": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "bash $CLAUDE_PROJECT_DIR/.claude/hooks/session_end.sh",
            "timeout": 60,
            "statusMessage": "Auto-commit selettivo (reports/doc/history, motore MAI)..."
          }
        ]
      }
    ],
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "bash $CLAUDE_PROJECT_DIR/.claude/hooks/review_gate.sh",
            "timeout": 15,
            "statusMessage": "Gate review: il commit del motore richiede il revisore..."
          }
        ]
      }
    ],
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "bash $CLAUDE_PROJECT_DIR/.claude/hooks/scrivi_rep.sh",
            "timeout": 30,
            "statusMessage": "scrivi rep: controllo trigger e salvataggio risposta..."
          }
        ]
      }
    ]
  }
}
== .claude/settings.local.json ==
(assente)
```

```
=== deps presenti ===
deps presenti: ['requests']
```

---

## §NOTE PIPELINE

- Branch corrente: `claude/phone-gas-development-10svqc` (NOTA: non `main` — questo branch ha già una PR #1 mergiata in una sessione precedente della stessa conversazione telefono; il checkout locale di questa sonda non è stato aggiornato dal merge, che è avvenuto via API GitHub, non via `git pull`. Nessuna azione correttiva presa: la sonda è read-only per design).
- CI GitHub Actions parte sul push, esito da verificare da PC (o da questa stessa sessione via l'integrazione GitHub, come già fatto nel task precedente).
