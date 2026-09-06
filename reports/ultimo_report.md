# Ricognizione READ-ONLY deploy VPS S2 — 2026-09-07

**Branch:** `docs/ricognizione-deploy-s2-2026-09-07`  
**Data:** 2026-09-07  
**Tipo:** Analisi read-only. Zero modifiche a codice o VPS. Solo report.

---

## §0 DECISIONI UMANE RICHIESTE

1. **Ruotare `ELEVENLABS_API_KEY` prima del deploy S2** (🔴 OBBLIGATORIO): la chiave attuale è stata usata in sessioni di sviluppo WSL — rischio leak in log di sessione. Ruotarla su elevenlabs.io e aggiornare `.env.prod` sul VPS.
2. **Merge della PR** (vedere §0 handoff.md per numero e URL da `gh`).
3. **Timing e modalità S2**: decidere quando eseguire il deploy (18 passi in checklist §DEPLOY VPS — Checklist S2 in `stato_progetto.md`).
4. **Voice server su VPS**: opzionale — decidere se avviare `gas voice` come servizio systemd separato.

---

## §1 SCOPE & ESITO FETTE

- **Fetta 1 — git fetch + baseline**: `FATTA` — fetch OK, baseline VPS = `f3a8acc` (2026-06-29), HEAD origin/main = `939effd` (2026-09-07).
- **Fetta 2 — commit motore nel range**: `FATTA` — `git log --oneline f3a8acc..origin/main -- gas.py brains/ modules/ tests/` → **45 commit motore** (2026-07-01 → 2026-09-02).
- **Fetta 3a — nuove dipendenze**: `FATTA` — `requirements.txt` IDENTICO tra baseline e main (openai==2.43.0, requests==2.34.2, numpy==2.4.6, onnxruntime==1.27.0, fastembed==0.8.0). Nessun nuovo `pip install` necessario per il core telegram. Il modulo voice usa solo stdlib (`http.client`).
- **Fetta 3b — nuove variabili d'ambiente**: `FATTA` — Identificate 11 nuove variabili (vedere tabella in stato_progetto.md). Obbligatorie solo per voice server: `ELEVENLABS_API_KEY`, `GAS_VOICE_TOKEN`. Tutte le altre hanno default ragionevoli. Variabili core telegram già in `.env.prod` del VPS invariate.
- **Fetta 3c — cambi schema DB / history**: `FATTA` — Nessun rischio. `.gas_history.json`: formato invariato, solo atomicità migliorata. `.gas_memory.db`: nuove tabelle `vettori`/`metadata` create con `CREATE TABLE IF NOT EXISTS` al primo avvio (additive, no ALTER TABLE).
- **Fetta 3d — cambi entrypoint / systemd**: `FATTA` — `gas.service` non è nel repo, invariato. Entrypoint VPS (`gas.py telegram`) invariato. Il voice server (`gas.py voice`) è un sotto-comando separato, non avviato automaticamente.
- **Fetta 3e — operazioni irreversibili / passi manuali**: `FATTA` — Nessuna operazione irreversibile su dati. Unico rischio medio: cambio modello Groq da `llama-3.3-70b-versatile` a `openai/gpt-oss-120b` (comportamento potenzialmente diverso). Rischio alto: `ELEVENLABS_API_KEY` da ruotare prima del deploy.
- **Fetta 4 — ricerca piano deploy pregresso**: `FATTA` — Nessun file `reports/deploy_vps*.txt` o simile trovato. La checklist S2 è stata costruita ex novo da questa ricognizione.
- **Fetta 5 — scrittura checklist in stato_progetto.md**: `FATTA` — Sezione "DEPLOY VPS — Checklist S2" aggiunta con tabella delta strutturale, tabella env vars, tabella rischi, 18 passi ordinati.

---

## Riepilogo delta strutturale (f3a8acc → origin/main)

| Area | Cambiamento |
|---|---|
| **45 commit motore** | Range 2026-07-01 → 2026-09-02 |
| **brains/model_ids.py** | NUOVO — fonte unica 5 ID modello, importato da gas.py |
| **brains/{4 file}** | ELIMINATI (dead code, non importati) |
| **modules/voice/** | NUOVO package completo (server/stt/tts) — FASE 3 |
| **modules/marketing/** | ELIMINATI 6 file (dead code) |
| **gas.py** | calcola() AST, prompt hardening, atomicità history, nuovi comandi CLI |
| **Modello Groq** | llama-3.3-70b-versatile → openai/gpt-oss-120b |
| **requirements.txt** | IDENTICO — nessun pip install aggiuntivo |
| **gas.service** | NON nel repo, invariato |
| **Rischio dati** | ZERO — formati compatibili, schema additive |

---

## Anomalie / note

- Il VPS al 2026-08-26 (ultima sonda) era fermo a `f3a8acc` con 391 commit totali dietro, ora 45 commit motore da portare (la sonda citava 17 ma era relativa a origin/main del 2026-08-26 — il contatore è cresciuto).
- `modules/voice/__init__.py` è vuoto (0 byte) — nessun import automatico al boot del kernel telegram.
- `.venv/` non è nel `.gitignore` VPS (fix in commit `1b03adc` non deployata) — dopo `git pull` sarà gitignorato correttamente.
