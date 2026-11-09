# Test della voce — mattina del 10 novembre 2026

Preparato da M1 nella notte. Si aggiorna con le PR mergiate stanotte (vedi fondo).

## 0. Prima di iniziare (Mac)
```
cd ~/Gas && git pull origin main && bash scripts/voce/installa.sh
python gas.py doctor
```
Il doctor deve dire OK o WARN (niente FAIL).

## 1. Prove base (5 minuti)
| # | Cosa dici / fai | Cosa deve succedere |
|---|---|---|
| 1 | «Hey Jarvis» | «Sì, signore?» |
| 2 | «Che ore sono?» | risposta corta e giusta |
| 3 | domanda di seguito, senza parola, entro 40 s | risponde senza bisogno di «Hey Jarvis» |
| 4 | silenzio per più di 40 s | torna in attesa della parola |
| 5 | «Jarvis, pausa» | «Va bene.» e chiude |
| 6 | parli con qualcuno nella stanza a finestra aperta | Gas NON risponde |
| 7 | «Hey Jarvis» a finestra aperta | non si rompe (V-1 #341) |

## 2. Telegram
| # | Cosa fai | Cosa deve succedere |
|---|---|---|
| 8 | mandi un vocale «che tempo fa a Roma?» | «Ho capito: …» + risposta in testo + risposta in vocale |
| 9 | scrivi un messaggio | risposta solo in testo |
| 10 | vocale che inizia con «forte …» | va al cervello forte |

## 3. Compiti in sottofondo
| # | Cosa dici | Cosa deve succedere |
|---|---|---|
| 11 | «Hey Jarvis, forte, prepara un riassunto della roadmap della voce» | «ci lavoro» e poi avviso su Telegram |
| 12 | dopo l'avviso: «Hey Jarvis, novità?» | ti dice il compito finito |

## 4. Il test vero: un compito intero a voce
Conversazione libera, solo a voce, senza toccare la tastiera. Esempi:
- «Hey Jarvis, quali sono i prossimi passi della roadmap?» → «Spiegami meglio il primo» → «Ok, preparami una bozza e avvisami».
- «Hey Jarvis, salva un contatto: Mario Rossi, interessato al sito, stato nuovo» → «Che contatti ho?»
Annota: risposte sbagliate, tempi lunghi, cose non capite.

## 5. Dopo le prove: incolla a M1
```
grep "tempi voce" ~/Gas/gas_debug.log | tail -20
grep -i "warning\|error" ~/Gas/gas_debug.log | tail -20
```

## Aggiornamenti della notte
(M1 li aggiunge qui man mano.)
- Entrate in main stanotte: #355 (vocali Telegram con risposta a voce). Prova 8 valida.
- In attesa del tuo sì (con riserve, quindi decidi tu): #356 (M2, frasi fisse in cache: «Dimmi.» istantaneo), #357 (Mani, voce Telegram più corta e senza simboli, blocco ~30 s).
- Pronte in locale (pubblicate dopo la #356/#357): sicurezza del server voce (R8 fetta 1, decisione di sicurezza), velocità frasi divise (M2); misura «prima frase dopo X s» (Mani).
- Decisioni di sicurezza per te: thread della voce su Telegram (3 opzioni di Mani, consiglia b); R8 fetta 1; proposta terminale (reports/proposta_terminale_autonomia.md).
