> **Stato al 2026-10-19: APPROVATO da Gas** (chat vocale, decisione R10 della roadmap). Le modifiche decise quel giorno sono in `reports/roadmap.md` e valgono sopra questo testo:
> - Proposte di Gas: idee illimitate in lista ordinata; massimo 10 PR a notte; le proposte "importante" possono superare il limite.
> - Di notte nessun merge: al mattino report breve per PR, decide Gas.
> - Codice di cancello e firma: firma di Gas + doppia verifica bot e chat, solo coi bottoni, mai di notte.
> - §7 superato: il server Hetzner non esiste più; il nuovo server è Netcup (R5).
> Copiato dal documento del progetto su claude.ai `claude/recinto_autonomia.md` (v1 del 2026-09-21), testo originale sotto senza modifiche.

# 🛡️ RECINTO AUTONOMIA GAS — architettura e regole di sicurezza
**v1 — BOZZA, in attesa di approvazione di Gas. 2026-09-21.**

> Definisce il "recinto" dentro cui GAS può diventare autonomo (studiare, autoaggiustarsi, autoprogrammarsi) SENZA violare il principio fondante: robustezza > potenza, zero crash, ogni operazione irreversibile FUORI dalla mano del modello. Finché questo documento non è approvato e implementato, NON si scrive codice di autonomia.

## 1. Le 3 capacità (rischio crescente)
1. **Studiare / comprendere** — legge e arricchisce memoria/conoscenza. Rischio **basso**: non tocca il proprio codice. È il primo mattone.
2. **Autoaggiustarsi** — si accorge di un errore e reagisce (ritenta, fallback provider, segnala). Rischio **medio**: solo azioni reversibili, dentro confini stretti.
3. **Autoprogrammarsi** — propone modifiche al proprio codice. Rischio **massimo**: l'operazione più irreversibile del progetto. Consentita SOLO dentro la catena di cancelli qui sotto.

**Ambito consentito:** codice applicativo (nuovi tool, correzioni di funzioni).
**Escluso SEMPRE:** infrastruttura, deploy, systemd, dipendenze di sistema, operazioni distruttive (merge lossy, gc, restore, cancellazioni) → restano solo mano umana.

## 2. La catena di cancelli (dalla proposta alla produzione)
Ogni auto-modifica passa, in ordine, per QUESTI cancelli. Nessuno saltabile.

1. **GAS propone** — apre una PR su un ramo dedicato. Mai sul tree in esecuzione, mai su `main`.
2. **Primo filtro** — Claude Code + subagent `revisore`: diff reale, edge case, scope, regressioni.
3. **Approvazione umana (Gas + Claude capo-eng)** — è il *check finale*, e sta PRIMA del main. Verdetto sul diff vero, non sul riassunto.
4. **Usciere apre il cancello** — dopo l'approvazione il merge parte da solo (Regola Ferrea #1). GAS non merga: merga l'usciere su ok firmato.
5. **Gemello / staging (soak test)** — la modifica gira su un GAS-copia prima del vero (§3).
6. **Promozione a GAS vero** — solo a criteri verdi.

## 3. Il gemello (staging / shadow) — idea di Gas, affinata
Pattern collaudato (staging + soak test): un GAS-copia dove la modifica "matura" prima di toccare il vero. Tre precisazioni che lo rendono sicuro e non pericoloso:

- **Gira in SANDBOX** (`GAS_SANDBOX_MODE` esiste già): tutte le azioni verso il mondo esterno (DM/mail ai lead veri, scritture su sistemi esterni) sono **disinnescate/finte**. Sennò due GAS scrivono agli stessi clienti = danno reale.
- **Dati e chiavi SEPARATI**: memoria (`.gas_memory.db`) e token (Telegram, provider) del gemello sono COPIE isolate. Il gemello non scrive mai nella memoria del GAS vero né usa il suo canale Telegram.
- **Criterio di promozione = tempo + eventi + zero regressioni**, non solo "5 giorni". Promuovi SOLO se: ≥ 5 giorni in shadow **E** ≥ N eventi/turni gestiti **E** 0 crash **E** suite di test verde **E** nessuna regressione sui casi noti. *(N da fissare insieme.)*

**Costo:** due GAS ≈ doppio consumo runtime. Mitigazione: il gemello può girare su input registrati (replay) invece che h24 live, o essere acceso solo durante il soak.

## 4. Regole FERREE (non negoziabili)
1. **Il merge irreversibile non sta MAI nella mano del modello.** GAS non ha nessun tool di merge. Il merge su `main` lo esegue l'**usciere** (auto-merge di GitHub) SOLO con approvazione firmata + test verdi. Lucchetto vero: il token che GAS usa **non ha permesso di scrivere su `main`** (branch protection senza bypass). *Da implementare e sondare — NON è ancora attivo.*
2. **Infra / deploy / operazioni distruttive = solo mano umana.** Sempre.
3. **Gemello sempre in sandbox, dati e chiavi separati**, azioni verso il mondo disinnescate.
4. **Di notte cancello CHIUSO.** GAS può studiare e preparare proposte (PR in bozza), ma nessuna modifica entra nel main di notte. L'ok lo diamo noi da svegli. Tetti: max N proposte/notte + budget token notturno.
5. **Studio solo da fonti fidate/approvate.** Niente web aperto (rischio prompt injection su agente autonomo).
6. **Report alla fonte.** Verdetti sul `git diff` verbatim, test reali mai simulati, `reports/ultimo_report.md` + hash commit. Vale anche per le proposte di autonomia.

## 5. Trigger (quando GAS agisce)
- **Su richiesta di Gas** — sempre.
- **On-block** — quando sbatte contro un errore/limite reale mentre lavora.
- **Notturno** — studia e prepara SOLO proposte (vedi Regola Ferrea #4).

## 6. Budget (due, mai confusi)
- **Sviluppo** — Claude Code, modelli Anthropic: costruire il recinto e le feature.
- **Runtime GAS** — multi-provider, gratis/economico: GAS che studia/gira + il gemello. Il gemello raddoppia il runtime: tenerne conto.

## 7. Cosa NON è deciso ancora / prossimi passi
- VPS Hetzner **giù** (carta nuova domani): finché non è vivo e finché non c'è Gas a guardare, **niente deploy** di autonomia. Oggi si lavora solo in DEV sul Mac.
- Da fissare insieme: valore di **N** (eventi minimi + proposte/notte), budget token notturno, meccanismo preciso dell'usciere (branch protection, permessi del token di GAS).
- Ordine di costruzione (Pareto): prima **#1 studiare** in DEV (sicura, dà valore subito), poi #2, poi #3 solo a recinto completo.

## 8. Stato
🟡 **BOZZA v1 — in attesa di approvazione di Gas.** Alla conferma diventa fonte di verità della fase Autonomia; da qui nascono i prompt per Claude Code.
