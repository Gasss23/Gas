# ULTIMO REPORT — 2026-10-03 — C4b-2: bottoni di firma + esecuzione post-approvazione

Branch `feat/cancello-c4b2` · PR #116 · commit motore `3258094` · review #131 + #132 **APPROVATO CON RISERVE**

## DECISIONI UMANE RICHIESTE

1. Merge della PR #116 (variante A: `gasmerge 116`, l'operatore conferma digitando il numero).
2. Prova reale di un click su Telegram: fattibile con il bot vivo (`gas telegram`) e un'azione innocua. Il click reale non è ancora stato provato.

## Esito per step

- **Registrazione C4b-1 verificato dal vivo** in stato_progetto: FATTA (la memoria temporanea è stata cancellata).
- **Bottoni [✅ Approva] [❌ Rifiuta]** sul read-back (`ok:/no:<uuid>`, fullmatch): FATTA.
- **Gestione callback nel bridge**: FATTA. Per essere accettato, il click deve venire da un `from.id` intero e da una chat entrambi in whitelist; altrimenti silenzio. Il bridge prima risponde al click e toglie i bottoni, poi registra la firma con `resolve_approval`. Le approvazioni orfane vengono riprese (R-c4b2-2). `getUpdates` chiede `callback_query`.
- **Esecuzione post-approvazione** (`GasKernel.applica_firma`): FATTA. Non approva mai. Controlla whitelist e hash, prende il reclamo (`approval_esecuzioni`, al massimo una esecuzione), ricontrolla il gate (DENY) ed esegue gli args salvati. Lo stato "eseguita" vale solo se l'esito non è [KO].
- **F-c4a-eco**: CHIUSA. Il diario "approvata id=" per `run_command` contiene solo conteggi (T77b).
- **Esito nel contesto del modello**: DEFERITA a C4b-3 (R-c4b2-1).
- **Notifica passiva di scadenza**: DEFERITA a C5 (design).
- **Click reale su Telegram**: DEFERITO alla decisione dell'operatore (punto 2).

## Test

- `python tests/test_unit_kernel.py`: 558 → **614 PASS / 5 FAIL**. I 5 FAIL sono F-mac-1 (T11c2, T11e, T12a, T12c, T12e: bwrap assente su macOS), invariati.
- `pytest tests --ignore=tests/test_unit_kernel.py`: **232 passed**, invariato.

## Riserve aperte

R-c4b2-1, R-c4b2-6, R-c4b2-7, R-c4b2-8, R-c4b2-9, R-c4b2-10 (dettaglio in `reports/stato_progetto.md`).

## Anomalie

- Il marcatore del gate `.claude/.review_ok` è stato bloccato dal classificatore della modalità automatica (auto-modifica). L'ha creato l'operatore dal pannello terminale.
- Sono state aggiunte due memorie di feedback: stile Jarvis e istruzioni passo-passo all'operatore.
