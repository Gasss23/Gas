# DA MERGIARE — coda della chat Motore

> Decisione dell'operatore (2026-10-21): la chat Motore lavora di fila sulla roadmap; qui si accumula ciò che è pronto, una voce per fetta, con i pro e i contro del merge. L'operatore passa 1-2 volte al giorno, legge questa pagina e scrive «mergia #N» oppure «no». Le voci mergiate si tolgono.

## PR aperta del ramo `feat/merge-automatico-z1xjx2` (nuova, dopo il merge di #232)

### 1. Avviso sui file delicati: chiavi e database tornano, via le parole ambigue
- **Cosa:** l'avviso «file nuovo che sembra delicato» torna a scattare su `server.pem.txt`, `dump.sql.txt`, `prod.env.txt`, `vault.kdbx.txt`; non scatta più su `customer.service.md`, `manuale.html.pdf`, `node.js.md`; i caratteri invisibili nel nome non lo aggirano più.
- **Pro:** chiude R-390-1 e le note della verifica esterna #232; meno falsi allarmi, nessun trucco con caratteri invisibili.
- **Contro:** `a.html.txt`, `x.js.md`, `a.ts.txt` non vengono più segnalati (R-391-1, bassa, scelta voluta); `dev.env.md` dà un avviso in più (R-391-2, cosmetica). È solo un avviso: non blocca nulla.
- **Controlli:** revisore #391 (chat Motore) APPROVATO CON RISERVE; gate 759, kernel 950 PASS. Verifica esterna e bot: vedi la PR.

### 2. Terza chat «Mani» (solo documento)
- **Cosa:** in `reports/lavoro_parallelo.md` l'area e il compito della chat Mani (R6, leggere il web, modulo `modules/web/` a sé) con il prompt da incollare.
- **Pro:** si lavora in tre senza conflitti (cartelle separate).
- **Contro:** la chat Mani tocca anche un passo di `ci.yml` (solo il suo); l'aggancio a Gas resta alla chat Motore.
