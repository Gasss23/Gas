# Proposta — Azioni fisse di manutenzione per Gas (terminale, opzione A) — chat M2, 9 novembre 2026

Base: `reports/proposta_terminale_autonomia.md` (M1). L'operatore ha detto sì all'opzione A il 9/11 (riferito da M1): azioni fisse, quelle che cambiano qualcosa con firma a bottoni su Telegram, mai a voce né di notte. Dettagli decisi da M1 lo stesso giorno: `aggiorna_gas` separata dal riavvio; `riavvia_voce` riavvia server voce e ascolto H24; notte con la finestra prudente. PR di sicurezza: il merge lo decide l'operatore.

## Cosa fa
Un solo strumento nuovo per Gas, `manutenzione`, con un argomento `azione` scelto da una lista chiusa. Non ci sono altri argomenti, e nessun testo del modello diventa un comando.

| azione | cosa fa | firma |
|---|---|---|
| `stato_gas` | `python gas.py doctor` (comando fisso, senza shell, tempo massimo), ultime righe | no (sola lettura) |
| `log_voce` | ultime 40 righe dei tempi della voce in `gas_debug.log`, riconosciute dal loro formato esatto | no (sola lettura) |
| `aggiorna_gas` | `git pull --ff-only origin main`, solo se Gas è sul branch `main` senza modifiche fatte a mano; poi `pip install -r requirements.txt` | sì |
| `riavvia_voce` | `launchctl kickstart -k` del server voce (`com.gas.voce.server`) e poi dell'ascolto (`com.gas.ascolto`), solo sul Mac. Se l'ascolto è in pausa (pausa.sh o standby) resta in pausa: per riprenderlo c'è `riprendi.sh` | sì |

## Come è recintato
1. **Cancello** (`modules/gate`). Un'azione di sola lettura è libera. Un'azione che cambia qualcosa è IRREVERSIBILE: va sempre alla firma su Telegram con i bottoni, lo stesso meccanismo già usato da `write_file` sul codice. Un'azione fuori lista, o con argomenti in più, è negata.
2. **Mai a voce.** Lo strumento non viene offerto nei turni a voce, effimeri o in sottofondo, né al giro notturno. Se il modello lo chiede lo stesso, viene negato prima del cancello, quindi non parte nemmeno una richiesta di firma.
3. **Mai di notte.** Dalle 23 alle 7, ora locale del computer di Gas (si cambia con `GAS_MANUTENZIONE_NOTTE`, per esempio `22-6`), le azioni che cambiano Gas sono negate: non parte la richiesta di firma e, se una firma arriva di notte, l'azione non viene eseguita. Le azioni di sola lettura restano disponibili.
4. **Esecuzione.**
   - I comandi hanno argomenti fissi scritti nel codice e girano senza shell, nella cartella di Gas, con un tempo massimo e l'output tagliato.
   - git non chiede mai credenziali (`GIT_TERMINAL_PROMPT=0`).
   - Nel diario finiscono solo l'azione e l'esito.
5. **Input esterno.** Se nel turno ci sono pagine o mail lette, anche le azioni di sola lettura passano dalla firma, come gli altri strumenti incerti.

## Limiti noti
- I vocali di Telegram arrivano a Gas come turni a testo, quindi lì lo strumento è offerto. Il mittente è comunque l'operatore autenticato, e le azioni che cambiano Gas restano alla firma. Se «mai a voce» deve valere anche per i vocali lo decide l'operatore.
- La firma viene eseguita nel processo del bot Telegram: `aggiorna_gas` può occuparlo per qualche minuto (pip). Dopo l'aggiornamento il bot NON resta sul codice vecchio: i moduli importati dentro le funzioni arrivano nuovi accanto a quelli vecchi già caricati. Gas non sa riavviare il bot da sé, quindi l'esito chiede di riavviarlo SUBITO (V-1 del bot su bae9278).
- `launchctl kickstart` non è ancora stato provato dal vivo sul Mac: va provato dopo il merge.

## Fette
1. Questa proposta più il codice: strumento, cancello, test (M2). I client e il bot Telegram non cambiano, perché la firma usa il meccanismo che c'è già.
