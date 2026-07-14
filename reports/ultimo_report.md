# Report — 2026-07-14 — Sfoltita Finding aperti

## DECISIONI UMANE RICHIESTE

- **Merge PR docs/sfoltita-finding → main**: CI verde (run 29315847317, SUCCESS). Merge doc-only da browser o `gh pr merge --merge`.

---

## Scope e esito fette

**Fetta 1 — Spot-check di merito (15 candidati ✅):** `FATTA`
Tutti i 15 candidati verificati da codice/test/commit reale. Nessun RETROCESSO.
Dettaglio per item:
- R-reidx-deps: VERIFICATO — requirements.txt pinnato (openai==2.43.0, requests==2.34.2, numpy==2.4.6, onnxruntime==1.27.0, fastembed==0.8.0)
- R-vec-2: VERIFICATO — gas.py:374,376 legge GAS_VECTORS_DB e GAS_EMBED_MODEL da env
- R-vec-2b: VERIFICATO — test T39b/T39c/T39f/T39g presenti
- R-vec-3: VERIFICATO — testo dice "NON prova qualità semantica"; R-wire-2 residuo 🟡 non toccato
- R-vec-pool: VERIFICATO — test T39h-T39k; fastembed_version nel fingerprint
- WINDOW_CHAR_CAP: VERIFICATO — gas.py:352 env-overridabile min_val=1000
- R-groq-slash: VERIFICATO — commit f028e51 in log; nota lasciata com'è (singola run)
- R-groq-dup: VERIFICATO — merge eb0509f in log
- MEMORY_PIN_SCAN: VERIFICATO — gas.py:351 env-overridabile min_val=10
- CI-4: VERIFICATO — T9a/T9c skip condizionale in test:149,153,159,162
- R-tel-1: VERIFICATO — gas.py:1446 _free_names da FREE_RUNGS
- Riserve #35: VERIFICATO — T39b-reason/T39c-reason/T39f/T39g nei test
- Riserve #44 A e C: VERIFICATO — merge PR #4 hash 3836111 in log
- Riserva #44B: VERIFICATO — brains/model_ids.py:11-16 try/except su float(os.getenv(...))
- Hardening token Claude Code: VERIFICATO — commit 72c2040 in log + curl 404/403 su ruleset

**Fetta 2 — Archiviazione finding verificati:** `FATTA`
15 item spostati (taglia-e-incolla compresso) da stato_progetto.md a finding_archiviati.md.

**Fetta 3 — Riclassifica 🟡 aperti:** `FATTA`
- Restano 🟡 attivi: Esfiltrazione, Degrado solo-testo, R-crm-1b, R-ci-openrouter, Riserve minori
- Nuova subsection DEPLOY VPS: R-reidx-3, R-wire-1, RAM a regime (3 sotto-punti)
- Nuova subsection Limiti noti (non-finding): R-wire-2
- Nuova subsection Debito latente: R-legacy-slice
- TPM burst: degradato da item a nota ℹ️ inline

**Fetta 4 — Riconcilia contatore review:** `FATTA — nessuna modifica necessaria`
Contatore letto da .claude/agents/memoria_revisore.md: ultima review #46 (2026-07-13).
stato_progetto.md già riportava 46 in entrambe le occorrenze. Nessuna modifica.

---

## Anomalie

Nessuna. Il file stato_progetto.md aveva encoding mojibake per le emoji — gestito via Python (edit chirurgico sui byte UTF-8 raw).
