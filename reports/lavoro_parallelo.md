# Lavoro in parallelo — due chat sullo stesso repo

> Deciso dall'operatore il 2026-10-20: una chat lavora sul **motore**, l'altra sulla **voce**.
> Fonte unica di queste regole: questo file. Le due chat lo leggono all'avvio.

## Chi fa cosa

| Chat | Area (può toccare) | NON tocca |
|---|---|---|
| **Motore** | `gas.py`, `modules/gate/`, `modules/memory/`, `modules/notte/`, `modules/telegram/`, `brains/`, i loro test | `modules/voice/`, `clients/voice/`, `tests/test_unit_voice_*` |
| **Voce** | `modules/voice/`, `clients/voice/`, `tests/test_unit_voice_*`, `reports/briefing_architettura_voce.md` | `gas.py`, `modules/gate/`, `modules/memory/`, `modules/notte/`, `modules/telegram/`, `brains/` |

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
