# Diff della sessione — 2026-11-17/19 — CRM clienti (fette 1-4)

Si riscrive a ogni sessione; la storia completa sta in git.

## Fetta 1 — prima bozza
- `modules/crm/store.py`: tabelle `crm_*`; soldi in centesimi; registro movimenti e diario CRM immutabili (trigger), storno per correggere; una proposta aperta per cliente; orologio iniettabile; `BEGIN IMMEDIATE` in ogni scrittura.
- `modules/crm/analisi.py`: conti puri (capitale, profitto per mese, commissioni, rendimento osservato, affinità, panoramica).
- `modules/crm/motore.py`: il CRM che legge se stesso (nuovo servizio → dopo un no aumento di capitale → presentazione), consenso, STOP, pause, tetti, insistenza crescente.
- `modules/crm/messaggi.py`: testi WhatsApp fissi (senza promesse, nota sul rischio, riga STOP) e link wa.me.
- `modules/crm/server.py`, `modules/crm/web/*`: dashboard in tempo reale (SSE) solo su 127.0.0.1, token, cookie, CSP, anti-CSRF, controllo Host, blocco dei tentativi.
- `modules/crm/__main__.py`, `modules/crm/demo.py`, `modules/crm/__init__.py`: riga di comando e dati dimostrativi.
- `.github/workflows/ci.yml`: step «Run CRM suite».

## Fetta 2 — risposte dell'operatore (`reports/crm/decisioni.md`)
- `gas.py`: `_contatti_per_filtro` unisce ai lead i clienti del CRM (sola lettura, come lapidi): chi nomina un cliente parla solo col cervello forte (R-803-4).
- `modules/crm/store.py`: file dedicato `.gas_memory_crm.db`, `percorso_db`, `identita_clienti`, `backup`; migrazione `followup_attivo` e `consigliato`; tetto degli invii a scaglioni nella transazione; `completa_testo` e saldo minimo dalla data del prelievo; apertura del servizio atomica col deposito.
- `modules/crm/motore.py`: ritmo mensile, anzianità minima, niente proposte nel mese in perdita, servizi da consigliare, selezione manuale (`prepara_selezionati`).
- `modules/crm/scrittore.py` (nuovo): testi riscritti da Claude Opus, mai da modelli gratuiti, con minimizzazione dei dati e tetto giornaliero.
- `modules/crm/messaggi.py`: testi neutri senza numeri per la scelta manuale.
- `modules/crm/server.py`, `modules/crm/web/*`: spunte e «Prepara messaggio», indicatore degli invii, «Riscrivi con Opus», interruttore del follow-up, servizi da consigliare, copia di sicurezza giornaliera, Host vuoto rifiutato.
- `modules/crm/__main__.py`: `.env` letto prima del parser, comando `backup`, import CSV che ferma i file già importati (`--forza`).
- `tests/test_unit_crm.py` (113 test), `tests/test_unit_kernel.py` (blocco T116).
- `.gitignore`: `.gas_memory_crm*`.
- `reports/crm/` (guida, decisioni, domande; la guida viene da `reports/crm.md`), `reports/roadmap.md`, `reports/stato_progetto.md`, report di fine task, `.claude/agents/memoria_revisore.md`.

## Correzioni della review #808
- `gas.py`: il controllo dei dati dei clienti usa una sola regex compilata e in cache invece di una ricerca per identificativo (R-808-1: con 1500 clienti da 9,4 s a 2 ms per finestra, stesso esito); il conto del cervello forte diventa funzioni di modulo (`registra_uso_claude_cli`, `tetto_claude_cli_superato`); i clienti del CRM si leggono anche dalla cartella del repo (R-808-4).
- `modules/crm/scrittore.py`: le riscritture con Opus entrano nel conto e nel tetto del cervello forte del kernel; il tetto del CRM conta i tentativi, segnati prima della chiamata (R-808-2).
- `modules/crm/store.py`: `segna_evento_entro_tetto` (controllo e scrittura insieme); `identita_clienti` ripara un salvataggio interrotto (R-808-3); testo neutro inviato identico resta senza nota (R-808-7).
- `.gitignore`: di nuovo `.gas_crm_demo.db*`. `reports/crm/guida.md`: falsi allarmi, copie di sicurezza, conto di Opus (R-808-5/6).

## Fetta 3 — dati dei clienti SOLO con Opus (decisione del 18-11) e note della verifica esterna #381
- `brains/model_ids.py`: `MODEL_CLAUDE_OPUS`, `MODEL_CLAUDE_CLIENTI` (`GAS_MODEL_CLAUDE_CLIENTI`), `e_modello_opus` (fonte unica dell'ID, V-4).
- `gas.py`: con dati di clienti nella finestra il forte chiama Opus (anche /forte, a metà turno, nella riflessione); modello non Opus → turno fermo; il blocco di memoria pieno solo alle chiamate Opus (R-810-1).
- `modules/crm/scrittore.py`: filtro delle parole vietate su testo normalizzato (V-1); modello dal file unico.
- `modules/crm/motore.py`: «⚠ ATTENZIONE» nel motivo delle scelte manuali (V-2).
- `modules/crm/store.py`: ripiego in lettura solo sul journal rimasto (R-809-1).
- `tests/conftest.py`: le suite pytest non leggono il file vero dei clienti (R-809-2); test nuovi in `tests/test_unit_crm.py`, `tests/test_unit_kernel.py` (T117, T114i/T114i2, T115d2/T115d2b), `tests/test_unit_notte.py`.
- `CLAUDE.md` §2: regola «dati dei clienti SOLO su Claude Opus»; `reports/crm/` (decisioni 10-11, domanda 3 tolta, guida).

## Fetta 4 — main nel ramo e parole vietate
- Merge di origin/main 5cb2d2f8 (PR #380 fix della CI, #382, #383): i file di main arrivano identici; conflitti solo in `reports/` e nella memoria del revisore (unione). Il diff della sessione si misura ora da 5cb2d2f8.
- `modules/crm/scrittore.py`, `tests/test_unit_crm.py`: parole vietate allargate (V-3 verifica esterna #381, 4° giro).
