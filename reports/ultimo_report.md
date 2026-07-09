# REPORT — 2026-07-09 — TASK DOC-ONLY: registrazione decisioni 2026-07-07 (verifica re-esecuzione)

## DECISIONI UMANE RICHIESTE

Nessuna bloccante. Tre incoerenze residue (stale) segnalate come proposte —
stesse proposte già individuate dalla sessione precedente (08:00). Decisione
umana se completare in un task futuro.

---

## Contesto re-esecuzione

Al momento dell'avvio, il working tree locale aveva:
- `reports/stato_progetto.md` modificato (solo header) — cambio da una sessione
  parziale precedente, NON committato.
- `reports/verifica_fase25.md` untracked (irrilevante al task).
- Local branch dietro origin/main di **3 commit**.

Una sessione precedente (2026-07-09 ~08:00, CI run `29003285932` SUCCESS) aveva
già completato l'intero task e pushato. Azione eseguita in questa sessione:
`git restore reports/stato_progetto.md` (scarta modifica locale stale) +
`git pull --ff-only` (fast-forward a `d7e4d89`).

---

## Verifica per punto (tutti FATTA dalla sessione precedente)

### 1) reports/stato_progetto.md

- **1a ✅** — Merge `refactor/model-ids-fonte-unica` (merge `eb0509f`, commit `160543a`)
  registrato: item "config-drift stringhe modello" **CHIUSO**. `brains/model_ids.py`
  = fonte unica dei 5 ID cascata, env-overridabili (`GAS_MODEL_*`). Suite 217 PASS
  incluso T56. Contatore review corretto a **44** (da `memoria_revisore.md`, ultima
  #44, 2026-07-08 — era stale a 42 nella sezione Stato motore).
- **1b ✅** — Finding 🟡 **R-legacy-slice** aggiunto (riserva #1 revisore, review
  #43): `brains/claude_brain.py:38` — `for m in messages[-8:]`, slicing raw,
  violazione sez. 5 CLAUDE.md. INERTE oggi (legacy non wired); bloccante se
  ri-agganciato. Debito tecnico latente, nessuna azione ora.
- **1c ✅** — Caveat suite registrato: i 217 PASS sono da Codespace dove bwrap NON
  è validabile; verifica bwrap demandata a CI/WSL locale.
- **1d ✅** — CI run merge: **ID 28874912495**, evento push su `eb0509f`
  ("Merge branch 'refactor/model-ids-fonte-unica'"), 2026-07-07T14:41:10Z —
  **SUCCESS ✅**.

### 2) reports/roadmap.md

- **2a ✅** — Sezione "🧭 DECISIONI CASCATA PROVIDER" aggiunta: rung 4 Cerebras
  `zai-glm-4.7` (5 RPM, 30K TPM, 1M token/giorno, doc ufficiale 2026-07-07);
  Gate 1 (sonda contesto, possibile cap 8.192 token) e Gate 2 (tool-call
  `disable_reasoning: true`, parsing id duplicati) bloccanti pre-wiring.
- **2b ✅** — Mistral API (free "Experiment", ~1B token/mese) aggiunto come
  CANDIDATO fetta separata post-Cerebras, stessi gate. TRIGGER DATI registrato
  (evento, non data): prima di lead reali → policy dati tutti i provider free.
- **2c ✅** — Decisioni registrate 2026-07-07: (i) NO cascata oltre ~6 rung;
  (ii) NO GitHub Models runtime; (iii) OpenRouter sblocco $10 RINVIATO;
  (iv) rung premium futuro = Claude API budget-cappata (Haiku 4.5 rif. 2026-07-07).
- **2d ✅** — "🌉 Ponte GAS↔Claude Code human-gated (Telegram)" aggiunto integrale:
  flusso proposta-file → Telegram → `/approva <id>` → listener lato DEV →
  branch mai main. 8 vincoli sicurezza non negoziabili. Prerequisito FASE 5.

### 3) Sezione "Pipeline provider"

**NON toccata** — la migrazione Groq era già mergiata su main (commit `f028e51`,
review #44, 2026-07-08) e la sezione riflette già lo stato reale.

---

## Proposte (fuori scope — decisione umana)

Tre incoerenze residue non toccate per rispettare "Fai SOLO quanto elencato":

1. `reports/roadmap.md` §PROSSIMI PASSI item 8 "Config-drift stringhe modello"
   risulta ancora "Stato: APERTO" — ora chiuso (merge `eb0509f`).
2. `reports/roadmap.md` §PROSSIMI PASSI item 1 "Migrazione rung Groq —
   validazione live: PENDING" e §Deprecazioni primo bullet sono stale —
   migrazione completata 2026-07-08 (commit `f028e51`, review #44).
3. `reports/stato_progetto.md` §Stato motore riga CI ("run #28665577327 su
   `51f9e1e`") è il run pre-sonda; l'ultimo su main è `28967120717` su
   `9187804` (SUCCESS, 2026-07-08).

---

## Scope e note operative

- Tocati in questa sessione: SOLO `reports/ultimo_report.md` (questo file).
- Zero file di motore.
- `git pull --ff-only` eseguito per allineare local a remote (`d7e4d89`).
- CI sulla sessione precedente: run `29003285932` — SUCCESS ✅.
