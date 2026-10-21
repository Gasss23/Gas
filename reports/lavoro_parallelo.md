# Lavoro in parallelo — due chat sullo stesso repo

> Deciso dall'operatore il 2026-10-20: una chat lavora sul **motore**, l'altra sulla **voce**.
> Fonte unica di queste regole: questo file. Le due chat lo leggono all'avvio.

## Chi fa cosa

| Chat | Area (può toccare) | NON tocca |
|---|---|---|
| **Motore** | `gas.py`, `modules/gate/`, `modules/memory/`, `modules/notte/`, `modules/telegram/`, `brains/`, i loro test | `modules/voice/`, `clients/voice/`, `tests/test_unit_voice_*`, `modules/web/`, `tests/test_unit_web_*` |
| **Voce** | `modules/voice/`, `clients/voice/`, `tests/test_unit_voice_*`, `reports/briefing_architettura_voce.md` | `gas.py`, `modules/gate/`, `modules/memory/`, `modules/notte/`, `modules/telegram/`, `brains/` |
| **Mani** (dal 2026-10-21) | `modules/web/`, `tests/test_unit_web_*`, e in `.github/workflows/ci.yml` SOLO un passo nuovo «web suite» | tutto il resto: zona Motore, zona Voce, gli altri passi di `ci.yml` |

**Tutto il resto** (`tools/`, `scripts/`, `.claude/`, `knowledge/`, `CLAUDE.md`, CI): nessuna delle due chat lo tocca senza chiedere prima all'operatore, che lo assegna a una sola chat.

Se alla chat Voce serve una modifica nella zona del Motore (per esempio un aggancio in `gas.py` o nel cancello per le firme a voce), **non la fa**: la scrive in fondo al suo `reports/ultimo_report.md` sotto «RICHIESTE ALLA CHAT MOTORE», e l'operatore la passa all'altra chat.

## Regole comuni

1. **Un ramo per chat**, una PR per fetta. Mai lavorare sul ramo dell'altra chat.
2. **Prima di iniziare e dopo ogni merge dell'altra chat**: `git fetch origin main` e merge di `origin/main` nel proprio ramo.
3. **File condivisi che vanno in conflitto** a ogni merge, e come risolverli:
   - `reports/handoff.md`, `reports/ultimo_report.md`, `reports/diff_sessione.md`: tenere la versione del **proprio** ramo (sono i log della propria sessione).
   - `reports/stato_progetto.md`: unire **a mano**, tenendo le righe di entrambi.
   - `.claude/agents/memoria_revisore.md`: tenere **entrambe** le righe nuove, in ordine di numero.
4. **Numeri delle review**: possono sovrapporsi tra le due chat. Nei report si scrive sempre «review #N (chat Motore)» o «review #N (chat Voce)».
5. Tutte le altre regole di `CLAUDE.md` valgono per entrambe: revisore prima di ogni commit nel perimetro, verifica esterna a fine fetta, merge solo con l'ok dell'operatore o con un APPROVATO pulito del bot, risposte brevi.

## Compito della chat Mani (assegnato dall'operatore il 2026-10-21)

Roadmap **R6, primo pezzo: «leggere il web»**, costruito come modulo a sé, senza agganciarlo a Gas.

1. `modules/web/`: una funzione `leggi_pagina(url) -> dict` che scarica UNA pagina e ne restituisce il testo pulito. Regole: solo `http`/`https`; niente indirizzi interni (localhost, 10.x, 192.168.x, 169.254.x, IPv6 locali, anche dopo la risoluzione DNS e dopo ogni redirect); tempo massimo e dimensione massima fissi; niente cookie, niente JavaScript; il testo esce SEMPRE marcato «NON FIDATO» e troncato; mai eccezioni verso chi chiama (errore → dizionario con `ok: False` e motivo).
2. `tests/test_unit_web_*.py`: test con un server finto locale e DNS finto, zero rete vera.
3. In `ci.yml` un solo passo nuovo «web suite» che lancia quei test.
4. Fuori area: l'aggancio come strumento di Gas (lista strumenti in `gas.py`, livello nel cancello, voce nel diario) **non lo fa**: lo scrive in fondo al suo `reports/ultimo_report.md` sotto «RICHIESTE ALLA CHAT MOTORE».
5. Ramo proprio (`feat/mani-web-…`), una PR, revisore prima di ogni commit (sicurezza: anche verifica esterna), numero review con «(chat Mani)».

Prompt da incollare nella chat nuova:

> Chat Mani di Gas. Leggi CLAUDE.md e reports/lavoro_parallelo.md (sezioni «Chi fa cosa» e «Compito della chat Mani»). Crea un ramo tuo da origin/main e fai il compito, di fila, senza chiedere. Tocca SOLO la tua area. Numero review: il più alto in memoria_revisore.md +1, con «(chat Mani)».
