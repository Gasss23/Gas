# Ultimo report — doc-only: swap riconciliazione + branch orfano

**Branch**: `docs/swap-e-branch-orfano`
**Data**: 2026-07-29
**Scope**: solo `reports/stato_progetto.md` e questo file. Nessun altro file toccato.

## DECISIONI UMANE RICHIESTE

1. Merge della PR #52 (docs(riconciliazione): swap (c)→✅ S1b + micro-finding branch orfano).

---

## Esito fette

- **EDIT 1 — punto (c) swap**: `FATTA` — riga riconciliata da "Non decisa" a ✅ ESEGUITA a S1b.
- **EDIT 2 — micro-finding branch orfano**: `FATTA` — voce aggiunta in fondo a "### DA FARE".
- **Riga Ultimo aggiornamento**: `FATTA` — aggiornata a 2026-07-29.

---

## Cosa è cambiato

### EDIT 1 — punto (c) swap (riga 151 → riscritta)

Il punto (c) della sezione "Note operative VPS" recitava:
> `(c) OPZIONE S1a da valutare: aggiungere swap file 2-4Gi … Non decisa, messa sul tavolo.`

Era un **detrito**: lo swap file 2GiB era stato attivato il 2026-07-04 (punto 9 della stessa sezione, S1b ✅). La riga era rimasta "Non decisa" per 24 giorni dopo l'esecuzione.

**Riscritta come**:
> `(c) ✅ SUPERATA — ESEGUITA a S1b (2026-07-04): swap file 2GiB attivo sul VPS …`

Non toccato: punto (a) (ancora aperto), punto (b) Ollama always-on (ancora aperto, decisione a S3), finding 🔴 no-swap (storia, resta).

### EDIT 2 — nuova voce in "### DA FARE — sviluppo/processo"

Aggiunta in fondo alla sezione (prima di "### Sessione 2026-07-21") la registrazione del micro-finding di processo sul branch `docs/stato-roadmap-hygiene` (`409ad54`): lavoro completo ma mai promosso a PR, canonici che descrivevano uno stato post-merge inesistente per giorni. Classe nuova ("lavoro che non atterra e sparisce dal radar"), contromisura minima e fix strutturale possibile (non impegnato).

### Riga "Ultimo aggiornamento"

Aggiornata da `2026-07-28` a `2026-07-29` con descrizione dei due edit.

---

## git diff REALE

```diff
diff --git a/reports/stato_progetto.md b/reports/stato_progetto.md
index 0cb451b..4f4f8c4 100644
--- a/reports/stato_progetto.md
+++ b/reports/stato_progetto.md
@@ -1,7 +1,7 @@
 # STATO PROGETTO GAS
 
 > Fotografia viva dello stato. Aggiornata a fine di ogni task.
-> Ultimo aggiornamento: **2026-07-28** (doc-only: bonifica branch remoti A1+A2,
+> Ultimo aggiornamento: **2026-07-29** (doc-only: riconciliazione swap (c)→✅
 > Storico sessioni, dettaglio componenti, finding chiusi: `reports/stato_storico.md`
 
@@ -148,7 +148,10 @@
 - (b) Ollama "3B always-on" da RIVALUTARE …
-- (c) OPZIONE S1a da valutare: aggiungere swap file 2-4Gi … Non decisa, messa sul tavolo.
+- (c) ✅ **SUPERATA — ESEGUITA a S1b (2026-07-04)**: swap file **2GiB** attivo sul VPS
+  (vedi punto 9 di questa sezione). L'opzione era "da valutare" al 2026-07-02; la
+  decisione è stata presa e applicata. Riga riconciliata il 2026-07-28 (era rimasta
+  "Non decisa" per 24 giorni dopo l'esecuzione).
 
@@ -246,6 +246,18 @@
 - ✅ **R-crm-1b fetta 3 (telefono) — CHIUSA su main** …
+- ℹ️ **Micro-finding di processo — branch di sessione mai promosso a PR** (rilevato
+  2026-07-28): il branch `docs/stato-roadmap-hygiene` (`409ad54`) è rimasto **2 commit
+  avanti su main, 0 indietro, senza PR aperta** dalla sessione hygiene. Lavoro completo
+  (`/fine-task` eseguito, handoff presente, hook che ha pushato il branch) ma **mai
+  atterrato su main**, e **non registrato in nessun canonico**: per giorni i canonici
+  hanno descritto uno stato "post-merge hygiene" che non esisteva. Classe NUOVA: non è
+  gate saltato né scope creep, è **lavoro fatto che non atterra e sparisce dal radar**.
+  La memoria ha mentito per OMISSIONE. Recuperato con PR dedicata il 2026-07-28.
+  **Contromisura minima (disciplinare, non strutturale)**: a fine di ogni giro,
+  `git ls-remote --heads origin` e confronto col numero di head atteso; ogni head in
+  più va spiegata o chiusa. Fix strutturale possibile, NON impegnato: uno step in
+  `/fine-task` che stampi `gh pr list --head <branch>` e FERMI se è vuoto.
 
 ### Sessione 2026-07-21 — chiusura giro item fuori-roadmap
```

---

## Dichiarazione scope

**Nessun altro file è stato toccato.** I due edit riguardano esclusivamente `reports/stato_progetto.md`. Nessuna modifica a gas.py, brains/, modules/, tests/, .claude/, .github/ o altri file. Nessun revisore invocato (doc-only per regola di progetto).

Incoerenze aggiuntive rilevate durante la lettura (fuori scope, proposte per task separati):
- La riga `### DA FARE — sviluppo/processo (aperti dal 2026-07-09)` riporta ancora "aperti dal 2026-07-09" nell'intestazione ma molti item sono ormai ✅ chiusi. Non toccata: riordinare intestazioni = rischio riformattazione fuori mandato.
- La sezione "Istituzioni di processo" conta "68 review" — non verificato se aggiornato, fuori scope.
