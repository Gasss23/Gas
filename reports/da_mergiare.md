# DA MERGIARE — coda della chat Motore

> Decisione dell'operatore (2026-10-21): la chat Motore lavora di fila sulla roadmap; qui si accumula ciò che è pronto, una voce per fetta, con i pro e i contro del merge. L'operatore passa 1-2 volte al giorno, legge questa pagina e scrive «mergia #N» oppure «no». Le voci mergiate si tolgono.

## PR aperta del ramo `feat/merge-automatico-z1xjx2`

### 1. Avviso sui file delicati più preciso (note di #231)
- **Cosa:** l'avviso «file nuovo che sembra delicato» non scatta più su documenti con iniziali nel nome (`verbale.c.rossi.md`), riconosce `github.token` e `aws.credentials`, regge gli spazi nel nome.
- **Pro:** meno falsi allarmi su Telegram, più casi veri presi.
- **Contro:** chiavi e database con doppia estensione (`server.pem.txt`, `dump.sql.txt`) non vengono più segnalati (riserva R-390-1, bassa: è solo un avviso, non blocca nulla); si sistema nella fetta successiva.
- **Controlli:** revisore #390 APPROVATO CON RISERVE; test 1582 passati; bot e verifica esterna: vedi la PR.
