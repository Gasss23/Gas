# Proposta — Server voce reso sicuro (R8, chat M2, 9 novembre 2026)

Solo documento. Ordine dell'operatore via M1 (9 nov notte): «prima una proposta breve con opzioni e raccomandazione, poi il codice; la PR resta aperta per l'operatore».

## Oggi
- Il server voce (`python -m modules.voice.server`) ascolta su **127.0.0.1:8765** (si apre all'esterno solo con `GAS_VOICE_BIND`), **HTTP in chiaro**.
- Un **token fisso** (`GAS_VOICE_TOKEN`, obbligatorio, confronto a tempo costante). Non scade mai: chi lo copia lo usa per sempre.
- **Tetto orario** solo sulle richieste parlate e su quelle a testo con voce (`GAS_VOICE_MAX_TURNI_ORA`, default 60). Nessun limite sui tentativi con token sbagliato né sulle richieste a testo senza voce.
- Client: la pagina nel browser (`clients/voice/browser_server.py`, M2) e l'ascolto H24 del Mac (`clients/voice/ascolto.py`, Mani), entrambi in locale.

## Rischi se il server esce dal Mac (VPS, telefono fuori casa)
1. In chiaro: token, audio e risposte (dati dell'operatore) leggibili da chi sta in mezzo.
2. Token eterno: una copia rubata vale per sempre.
3. Indovinare il token o consumare la quota (Groq, ElevenLabs, cervello forte) con richieste a raffica.

## Opzioni

**Connessione cifrata**
- **A1 — TLS nel server Python** (`ssl.SSLContext` su `HTTPServer`, certificato e chiave da file in `.env`). Pro: niente pezzi esterni. Contro: certificati da creare e rinnovare a mano; certificato autofirmato → avvisi sul telefono.
- **A2 — Tunnel privato (Tailscale o WireGuard), server sempre su 127.0.0.1/rete del tunnel**. Pro: cifratura e accesso solo dai dispositivi dell'operatore, zero porte aperte su Internet, niente certificati da gestire. Contro: un'app da installare sul Mac/VPS e sul telefono (configurazione dell'operatore).
- **A3 — Reverse proxy con HTTPS (Caddy/nginx + Let's Encrypt)** sul VPS. Pro: standard, certificato automatico. Contro: serve un dominio e una porta pubblica (superficie d'attacco esposta).

**Token che scadono**
- **B1 — Token di sessione a scadenza**: il token lungo (`GAS_VOICE_TOKEN`) serve solo a `POST /voce/sessione`, che restituisce un token breve (es. 12 ore, casuale, solo in memoria del server). Le richieste normali usano il token breve. Revoca: riavvio del server o `POST /voce/sessione/chiudi`.
- **B2 — Token firmato (HMAC) con scadenza dentro** (`scadenza.firma`). Pro: niente stato nel server. Contro: revoca solo cambiando il segreto.

**Limite di richieste**
- **C1 — Tetto ai tentativi falliti per IP** (es. 10 in 10 minuti → 429 per 15 minuti, nel log solo IP ed esito).
- **C2 — Tetto anche alle richieste a testo** (oltre a quello parlato già presente).

## Raccomandazione
1. **A2 (tunnel privato)** per uscire dal Mac: la cosa più sicura e meno da mantenere; il server resta su 127.0.0.1 o sull'indirizzo del tunnel, mai esposto su Internet. **A1 come opzione nel codice** (attiva solo con `GAS_VOICE_TLS_CERT`/`GAS_VOICE_TLS_KEY`), per quando serve senza tunnel.
2. **B1 (token di sessione a scadenza)**, con il token lungo che resta valido come oggi finché i client non sono aggiornati (`GAS_VOICE_SOLO_SESSIONE=1` per spegnerlo dopo). Così la pagina e l'ascolto H24 non si rompono il giorno del merge.
3. **C1 + C2**: tetto ai tentativi falliti per IP e alle richieste a testo.
4. Avvio rifiutato se `GAS_VOICE_BIND` non è locale e non c'è né TLS né tunnel dichiarato (`GAS_VOICE_RETE_PRIVATA=1`): fail-closed.

## Fette proposte (codice solo nel server voce di M2; client dell'ascolto: Mani)
1. C1 + C2 + avvio rifiutato fuori da 127.0.0.1 senza TLS né rete privata.
2. A1 (TLS opzionale) con test su un certificato generato nel test.
3. B1 (token di sessione) lato server, compatibile; poi i client (pagina: M2; ascolto H24: Mani).

## Stato
- **Fetta 1 FATTA in questa PR** (resta aperta per l'operatore): tetto ai tentativi con token sbagliato per IP (`GAS_VOICE_MAX_FALLITI`, default 10 in 10 minuti → 429 per 15 minuti a quell'IP, anche col token giusto); tetto alle richieste a testo (`GAS_VOICE_MAX_TESTO_ORA`, default 120/ora); avvio rifiutato se `GAS_VOICE_BIND` non è locale senza `GAS_VOICE_RETE_PRIVATA=1`. Su 127.0.0.1 (uso di oggi) nulla cambia per la pagina e l'ascolto H24, salvo i due tetti.
- Fette 2 (TLS) e 3 (token di sessione): dopo il sì dell'operatore su questa proposta.
- Limiti noti della fetta 1 (review #720-M2): (a) sul Mac tutti i client arrivano da 127.0.0.1 (la pagina passa dal suo proxy): un client rimasto con un token vecchio blocca per 15 minuti anche la pagina e l'ascolto H24 — scelta prudente, da confermare (R-720-2-M2); col tunnel ogni dispositivo ha il suo IP. (b) Oltre 1024 IP ricordati, i nuovi non vengono più bloccati (memoria limitata; irrilevante su 127.0.0.1 o tunnel, da rivedere prima di un uso sul VPS, R-720-4-M2). (c) Una riga di log per ogni richiesta bloccata (R-720-5-M2).

## Decisioni per l'operatore
- Sì/no ad A2 (tunnel) come via principale fuori casa, e quale (Tailscale è il più semplice).
- Durata dei token di sessione (proposta: 12 ore).
- Soglie: 10 tentativi falliti in 10 minuti per IP; 120 richieste a testo all'ora.
