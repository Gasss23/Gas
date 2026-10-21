# DA MERGIARE — coda della chat Motore

> Decisione dell'operatore (2026-10-21): la chat Motore lavora di fila sulla roadmap; qui si accumula ciò che è pronto, una voce per fetta, con i pro e i contro del merge. L'operatore passa 1-2 volte al giorno, legge questa pagina e scrive «mergia #N» oppure «no». Le voci mergiate si tolgono.

> **C6 deciso (2026-10-21):** l'operatore ha scelto (a) «lasciamo così»: una firma per ogni azione, niente «Modifica» né firme a gruppi.

## PR aperta del ramo `feat/merge-automatico-z1xjx2` (nuova, dopo il merge di #234)

### 1. Tre stati per un comando firmato (roadmap R7, R-c4b3-5)
- **Cosa:** se un comando approvato su Telegram parte ma si interrompe (es. tempo scaduto dopo 60 s), Gas ora dice «PARTITO, esito INCERTO: può aver fatto solo una parte del lavoro, controlla prima di ripetere», nella storia, nel diario e nel messaggio Telegram. Prima diceva «NON eseguito», che era falso.
- **Pro:** niente più informazione sbagliata all'operatore e al modello; il diario delle azioni successive non viene più sporcato (R-428-1).
- **Contro:** oggi i comandi di sistema sono spenti (allowlist vuota), quindi è un caso latente; due rami senza test (R-429-1, bassa).
- **Controlli:** revisori #428, #429 (chat Motore) APPROVATO CON RISERVE; kernel 975 PASS. Bot V-B: success con 3 riserve BASSE (prossima fetta).

### 2. Bot e terminale non si cancellano più la storia (roadmap R7, R-c4b3-4)
- **Cosa:** se Gas su Telegram e Gas da terminale lavorano sulla stessa cartella, l'ultimo che salvava cancellava i messaggi dell'altro (anche l'esito di una firma). Ora c'è un lock sul file: chi salva rilegge e accoda i propri turni completi; se uno dei due è a metà turno, la versione dell'altro va in una copia «conflitto» accanto alla storia, nulla si perde.
- **Pro:** niente più conversazioni perse quando si usano insieme bot e terminale.
- **Contro:** le copie «conflitto» si accumulano senza pulizia né avviso (R-430-3, bassa); provato con due kernel nello stesso processo, non con due processi veri su VPS.
- **Controlli:** revisori #430 (R-430-1 MEDIA) e #431 (la chiude) APPROVATO CON RISERVE; kernel 981 PASS, pytest 1796 passed.
