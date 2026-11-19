# Ultimo report — 2026-11-17/19 — CRM clienti: fette 1-3, più fetta 4 (main nel ramo, parole vietate allargate)

## DECISIONI UMANE RICHIESTE
1. Merge della PR #381: decide l'operatore (riserve BASSE e COSMETICHE aperte).
   - Main è ora dentro il ramo, col fix della CI della PR #380: il rosso della CI dovrebbe sparire con questo push (esito nel §6 dell'handoff).
2. Il bot di verifica su GitHub non conclude: due volte di fila tutti i suoi modelli sono falliti. È un problema del bot (quota, chiave o PR troppo grande), non del codice, e il suo check required resta senza esito.
3. Confermare la scelta A su R-810-1: il cervello forte, quando non è Opus, riceve la memoria senza i nomi dei clienti. Alternativa B: Opus a ogni turno del forte, che consuma molto di più.
4. Le 3 domande aperte in `reports/crm/domande.md`.
5. Prima dei dati veri:
   - consenso dei clienti;
   - verifica Consob;
   - decisione GDPR (R-803-9, R-808-6).

## Esito
- **Fetta 1 — CRM clienti, prima bozza**: FATTA.
  - Commit 99d82f3f, review #803 BOCCIATO → #804 APPROVATO CON RISERVE.
  - Poi gate IP (f1c109a7, review #805 APPROVATO) e finding di bot e verifica esterna #381 (c9daf955 e 72dcc9d2, review #806 e #807).
  - Cosa c'è: clienti, servizi, registro movimenti immutabile in centesimi, motore delle opportunità, dashboard in tempo reale su 127.0.0.1, invio WhatsApp con un click dell'operatore.
- **Fetta 2 — risposte dell'operatore** (`reports/crm/decisioni.md`): FATTA. Commit aa4bb422, review #808 BOCCIATO → #809 APPROVATO CON RISERVE.
  - File dedicato `.gas_memory_crm.db`, con una copia di sicurezza al giorno.
  - Follow-up: un messaggio al mese per cliente, spegnibile cliente per cliente. Mai a chi è appena entrato (meno di 30 giorni) né nel mese in perdita. Precedenza ai servizi «da consigliare» (sala segnali, copyflip).
  - Spunte per scegliere i clienti a mano (tutti / alcuni / nessuno), con testi neutri senza numeri.
  - Invio a scaglioni: al massimo 10 ogni 60 minuti, contro il blocco di WhatsApp.
  - «Riscrivi con Opus»: SOLO Claude Opus, con dati minimi. Rientra nello stesso conto e nello stesso tetto di spesa del cervello forte di Gas, e contano anche i tentativi falliti.
  - Privacy (R-803-4 chiusa): se in chat, a voce o su Telegram si nomina un cliente del CRM, il messaggio va SOLO al cervello forte, mai ai modelli gratuiti. Se il file non si legge, tutto va al forte.
  - Primo giro del revisore (#808): il controllo rallentava Gas in proporzione ai clienti (9,4 s a turno con 1500 clienti). Ora c'è una sola regex in cache: 2 ms, con lo stesso identico esito (3000 casi casuali più 8000 casi del revisore).
- **Fetta 3 — dati dei clienti SOLO con Claude Opus** (decisione dell'operatore del 18-11) **e note della verifica esterna #381 (3° giro)**: FATTA.
  - Commit d402a4f6, review #810 APPROVATO CON RISERVE:
    - quando nella conversazione di Gas ci sono dati di un cliente, ogni chiamata del cervello forte usa Opus. Vale anche nei turni /forte, quando i dati arrivano a metà turno e nella riflessione. Se il modello configurato non è Opus, Gas si ferma e lo dice;
    - filtro delle parole vietate che non si aggira più;
    - avviso «⚠ ATTENZIONE» sulle scelte manuali di clienti appena entrati;
    - ID di Opus nel file unico dei modelli;
    - R-809-1 e R-809-2 chiuse.
  - Commit 6ef97624, review #811 APPROVATO (R-810-1, scelta A): il blocco di memoria coi nomi dei lead va solo alle chiamate Opus.
- **Fetta 4 — main nel ramo e note della verifica esterna #381 (4° giro)**: FATTA.
  - Merge 47df3c00 di main (PR #380, #382, #383), review #812 APPROVATO: conflitti solo nei report, fix della CI incluso.
  - Commit 71ccb045, review #813 APPROVATO: parole vietate allargate («ti garantisco», «capitale protetto», «rendimento sicuro», «soldi facili»…).
- **Invio automatico su WhatsApp**: DEFERITA. Decisione dell'operatore: «da sole, ma all'inizio col mio controllo». Oggi ogni invio lo conferma l'operatore. Per l'automatico servono l'API WhatsApp Business e i modelli approvati da Meta.
- **Strumento CRM per il modello di Gas** («chi devo chiamare oggi?»): DEFERITA, prossima fetta.

## Test
- `tests/test_unit_crm.py`: 120 passed. I test nuovi di ogni giro falliscono sul codice di prima:
  - 14 su 48c0f114;
  - 4 sullo staged di #808;
  - 4 su e126c65c.
- Suite del kernel: `=== RIEPILOGO: 1191 PASS, 0 FAIL ===`. Era 1171 sulla base: prima l'handoff diceva 1167 per errore. Fail-before:
  - T117 su e126c65c: 4 FAIL col modello iniettato;
  - T114i e T115d2b su d402a4f6: 2 FAIL.
- Altre suite che costruiscono il kernel: 1490 passed. Sul risultato del merge con main: crm, notte, web_browser (intera, col fix di #380), voice_server, manutenzione e voice_contesto danno 668 passed. mypy: 0 errori in `modules/crm` e `brains/model_ids.py`.

## Riserve aperte
- R-810-2 e R-810-3: COSMETICHE (limiti del filtro delle parole vietate; isolamento dei test legato all'ordine degli import). V-5 della verifica (COSMETICA): il controllo «è Opus» guarda solo il nome.
- R-808-5, R-808-6, R-803-9, R-803-10, R-804-2, R-804-4: vedi `reports/stato_progetto.md`.

## Anomalie
- CI rossa sullo step «Run web suite» (7 test bwrap del browser) fino a cdee8f0d. Il fix era già su main (PR #380): l'handoff lo dava per «fetta separata», un errore segnalato dalla verifica esterna (V-1). Ora main è nel ramo.
- Bot di verifica su e126c65c e su cdee8f0d: check cancelled tutte e due le volte, perché i suoi modelli (claude-opus-5-5, claude-opus-4-8, claude-fable-5-1) sono falliti tutti.
