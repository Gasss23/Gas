# Ultimo report — 2026-11-17 — CRM clienti, fetta 1 (prima bozza) e fetta 2 (risposte dell'operatore)

## DECISIONI UMANE RICHIESTE
1. Merge della PR #381: decide l'operatore (riserve BASSE aperte; la PR tocca la CI, quindi il check del bot è «neutral»). Oggi il merge è bloccato dalla CI rossa per 7 test del sandbox del browser, che falliscono anche su altri rami: è un cambio dei runner GitHub, non il CRM. Serve una fetta separata (già suggerita come task a parte).
2. Le 4 domande aperte in `reports/crm/domande.md`:
   - come guadagniamo su ogni servizio e capitale minimo;
   - WhatsApp Business: app o API;
   - Opus anche per le risposte di Gas in chat sui clienti;
   - collegare le chat tra loro (bacheca comune + avvisi).
3. Prima dei dati veri:
   - consenso dei clienti raccolto davvero;
   - verifica Consob con un consulente;
   - decisione GDPR: anonimizzazione su richiesta (R-803-9), che deve valere anche per le copie di sicurezza (R-808-6).

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
- **Invio automatico su WhatsApp**: DEFERITA. Decisione dell'operatore: «da sole, ma all'inizio col mio controllo». Oggi ogni invio lo conferma l'operatore. Per l'automatico servono l'API WhatsApp Business e i modelli approvati da Meta.
- **Strumento CRM per il modello di Gas** («chi devo chiamare oggi?»): DEFERITA, prossima fetta.

## Test
- `tests/test_unit_crm.py`: 116 passed. I test nuovi di ogni giro falliscono sul codice di prima: 14 su 48c0f114, 4 sullo staged di #808.
- Suite del kernel: `=== RIEPILOGO: 1184 PASS, 0 FAIL ===`. Sul gas.py senza fetta 2 i T116 danno 6 FAIL; su quello di #808, 3 FAIL (T116h a 9,8 s, T116j, blocco T116).
- Suite claude_cli, notte, manutenzione, sottofondo, telegram_voce, voice_server, richieste, gate: 1607 passed. mypy: 0 errori in `modules/crm`. `node --check` ok.

## Riserve aperte
- R-809-1 BASSA: il ripiego in lettura scatta anche su «database is locked», quindi Gas aspetta 10 s prima di chiudere. Nell'uso normale accade di rado.
- R-809-2 BASSA: tre suite di test non isolano un CRM vero nella cartella del repo. Rischio solo sul Mac e sul VPS, non in CI.
- R-808-5 e R-808-6 (dichiarate nella guida), R-803-9, R-803-10, R-804-2, R-804-4: vedi `reports/stato_progetto.md`.

## Anomalie
- CI rossa sullo step «Run web suite» (7 test bwrap del browser) su ogni ramo dal 17 nov: ambientale, dettagli nel §6 dell'handoff. Lo step «Run CRM suite» è verde.
