# ULTIMO REPORT — 2026-10-29 — Mani: chiusura fetta 26, note cosmetiche della verifica esterna #298, ripartenza (R6, chat Mani)

## DECISIONI UMANE RICHIESTE
1. Merge della PR di questa sessione (numero nell'handoff §0): solo report; lo faccio io con verdetto del bot APPROVATO pulito, con riserve aspetto il tuo OK.
2. Due decisioni rimaste della chat Mani, una alla volta: «tempo di rete 12 s» (oggi la rete si ferma a 12 s e 3 s restano per la pulizia, stima e non tetto rigido) e R-ve235-7 (il DNS di sistema non si interrompe; proposta: chiuderla come accettata).
3. Accensione della lettura con lexbor: serve la chat Motore (`selectolax==1.0.2` in `requirements-dev.txt` e `requirements.txt`), poi `GAS_WEB_LEXBOR=1` sul VPS (Linux).

## Esito
- **PR #298 (fetta 26)**: MERGIATA su richiesta dell'operatore («mergia 298», 7cc2112). Bot su d3b489f APPROVATO CON RISERVE (V-1 COSMETICA: descrizione della PR vecchia → FATTA, descrizione aggiornata). Verifica esterna su d3b489f APPROVATO CON RISERVE (https://github.com/Gasss23/Gas/pull/298#issuecomment-6499903630):
  - V-1 COSMETICA: FATTA — correzione: i casi nuovi che passano anche sulla base f8b35ae sono SEI, non tre: nbsp/eacute ridichiarati, `[%q;]` con DOCTYPE SYSTEM, nvlt con «<», AMP con «&», entità PUBLIC XHTML con `&e;`, `<p a="&e;">` (più il test R-553-1 riscritto); nbsp, nvlt e AMP sono guardie contro regressioni nate dentro la PR (nbsp falliva a 6512576).
  - V-2 COSMETICA: FATTA — correzione: il mutante «`valore is not None` tolto» NON è equivalente (TypeError sulle entità esterne, preso dai test); l'unico equivalente è «la pagina non vince».
  - V-3 informativa (7f571ee committato prima della fine della #562, numero #561 usato due volte): SALTATA — già dichiarato; diff revisionato = diff committato (sha f1cd8f63).
- **Ripartenza della chat Mani**: FATTA — `reports/ripartenza_mani.md` con #296 e #298 mergiate e le due decisioni rimaste.
- **Codice**: nessuna modifica in questa sessione.

## RICHIESTE ALLA CHAT MOTORE
1. `selectolax==1.0.2` in `requirements-dev.txt` e `requirements.txt` (R-ve280-1), poi `GAS_WEB_LEXBOR=1` sul VPS.
2. R-546-1: numeri delle review doppi tra le chat.
3. `scripts/bot_esito.py` boccia il verdetto quando il bot stesso scrive un carattere Cf citando il codice.
4. Sul VPS serve libexpat ≥ 2.4 perché il taglio dell'XHTML sia attivo; un controllo nel doctor.

## Anomalie
- `gh` non autenticato nel cloud: PR, etichetta e stato CI passano dall'integrazione GitHub.
