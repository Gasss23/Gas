`scrivi rep` è gestito automaticamente dall'hook `.claude/hooks/scrivi_rep.sh`: salva la **risposta precedente** (il recap della normalizzazione chiavi lead) in `reports/ultima_risposta.md` e committa+pusha da sé con prefisso `chore(scrivi-rep):`. Non scrivo nulla a mano né tocco `ultimo_report.md`.

Recap: hai dato il comando di salvataggio; ci pensa l'hook, io non devo fare altro.
