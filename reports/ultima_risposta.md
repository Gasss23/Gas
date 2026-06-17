Fatto. Tutti e tre i punti completati, gate di scope e di review rispettati.

**Path report:** `reports/ultimo_report.md`
**Hash commit doc:** `becdfd3` · **Hash commit motore:** `cdf764a` (review #16 APPROVATO)
Entrambi pushati su `origin/main`. Il contenuto stampato sopra coincide esattamente col file (nessuna discrepanza).

---

### Recap semplice

Oggi ho sistemato **un solo problema** della memoria di GAS, esattamente come chiesto, senza toccare altro.

1. **Niente più lead doppioni (PUNTO 1).** Prima, se GAS salvava lo stesso contatto scritto in modi diversi — *"Anna"*, *"anna"*, *" ANNA "* — la rubrica li trattava come persone diverse e si riempiva di doppioni silenziosi. Ora una piccola funzione "pulisce" la chiave (toglie spazi di troppo, mette tutto minuscolo) sempre allo stesso modo, sia quando salva sia quando cerca → la stessa persona finisce sempre nella stessa scheda. Niente magie azzardate (nessun "indovinare" se due nomi sono simili): solo una pulizia prevedibile e sicura.

2. **Database vuoto → nessuna migrazione.** Ho controllato: non c'erano vecchi contatti da sistemare, quindi zero rischi. Se in futuro ce ne fossero, ho scritto nel report come gestirli, ma la decisione resta tua.

3. **Due appunti tenuti vivi (PUNTO 2).** Riguardo a due piccole riserve segnalate in passato, ho scoperto che erano già state risolte in un giro precedente. Invece di far finta che fossero aperte, ho annotato con onestà quel poco che resta davvero da rifinire (un numero "fisso" da regolare un domani), senza inventare problemi.

4. **Vector DB messo nero su bianco (PUNTO 3).** Ho registrato che il prossimo grande passo della memoria (i "ricordi intelligenti") è **fermo per scelta**, da progettare con calma prima di buttarcisi. Così non si dimentica.

**Controlli:** tutti i test passano (da 106 a **110**, zero errori), il cuore del sistema (`gas.py`) **non è stato toccato**, e il revisore ha **approvato**. C'è solo un dettaglio estetico segnato per il futuro: il messaggio di conferma mostra il nome come l'hai scritto invece che ripulito — ma nel database il dato è giusto.
