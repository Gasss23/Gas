# Simulazione dell'ascolto vocale — 23 novembre 2026

Prova end-to-end di «Hey Jarvis» con voci sintetiche, fatta per non chiedere all'operatore altre registrazioni alla cieca. Gira il **codice vero** di Gas: `scripts/voce/registra_voce.py` (`main`, `misura`, `addestra`, con un microfono finto) e `clients/voice/ascolto.py` (`Ascolto.gira`, `rilevatore_con_verifica`), su flussi audio lunghi. Da qui escono le correzioni della PR #400.

## Come è fatta
- Voci: espeak-ng (it, en, es, pt; maschili e femminili; velocità e tono diversi). Come «operatore» la voce it+m3 che dice «ehi jarvis» all'italiana. Il modello le dà mediana 0,43 (0,34–0,69), vicino ai numeri veri dell'operatore (0,37–0,54).
- Distanza: −6/−12/−20 dB, riverbero sintetico, rumore rosa (`script/lib_sim.py`).
- Registrazione: `script/sim_registra.py` fa girare `registra_voce.main()` vero (sei registrazioni complete).
- Flussi (`script/gen_flussi.py`):
  - A: 120 chiamate in 30 minuti;
  - B: 30 minuti di parlato dell'operatore, quasi-omofoni compresi;
  - C: 30 minuti di TV;
  - D: 40 «Hey Jarvis» di altre voci;
  - E: 60 chiamate mentre Gas parla.
- Ascolto: `script/sim_ascolto.py` (vero `Ascolto.gira`). Le griglie di soglie si fanno rigiocando i punteggi registrati (`script/traccia*.py`, `script/sweep*.py`), uguali al rilevatore vero (`risultati/val_vero_*.txt` = `risultati/val_tr_*.txt`). Le prove finali sono col rilevatore vero (`risultati/vero4/`).

## Risultati (somma di 3 registrazioni; FP/h = attivazioni sbagliate all'ora)

| Regolazione | vicino | −6 dB | −12 dB | −20 dB | FP/h parlato | FP/h TV | altre voci accettate |
|---|---|---|---|---|---|---|---|
| Senza filtro, 0,7 su 1 blocco | 23% | 33% | 3% | 0% | 34 | 54 | 40% |
| Filtro, 0,5 su 1 blocco (prima della PR) | 89–93% | 71–80% | 28–41% | 23–33% | 2–5 | 6–13 | 16–24% |
| Filtro + 4 fasi, 0,6 su 1 blocco | 96% | 80% | 41% | 27% | 1,3 | 4,7 | 15% |

- 2 blocchi di fila dimezzano sempre le chiamate prese.
- Latenza: 0,2–0,45 s dalla fine della parola.
- **Fasi** (`script/fase.py`): la stessa clip va da 0,06 a 0,48 di punteggio a seconda di dove cade sulla griglia da 80 ms.
- **Interruzione col filtro**: chiamate vicino/−6 dB, 3 filtri addestrati, 180 prove.
  - Una fase (`script/interr.py` → `risultati/interr_1fase.txt`): 0,8 su 3 blocchi 4/180 (2%); soglia della parola 0,5 su 1 blocco 156/180 (87%).
  - **4 fasi, cioè la configurazione predefinita della PR #400** (`script/interr_f4.py` sulle tracce `tracce_f4_ver` di `script/traccia_fasi.py` → `risultati/interr_f4.txt`): 0,8 su 3 blocchi 8/180 (4%); 0,5 su 1 blocco **170/180 (94%)**; 0,5 su 2 blocchi 158/180; 0,5 su 3 blocchi 99/180.
  - Auto-interruzioni dalla voce di Gas simulata (flusso E, Gas che parla di continuo): **0 all'ora** in tutte le regolazioni, con 1 e con 4 fasi.
  - Quando la voce di Gas copre la chiamata (flusso E) le prese sono 0/180 in tutte le regolazioni: funziona solo nelle pause tra le frasi.
- **Griglia in addestramento** (`script/fase2.py`): clip buone scartate 4/74 → 0/74.
- **Pronuncia**: la stessa voce sintetica dà 0,90 a «HEY JARVIS» all'inglese e 0,40 a «ehi jarvis» all'italiana. A −12 dB solo il 27–40% delle chiamate arriva a 0,25 (soglia base del filtro): è il «risponde solo vicino al Mac».
- **Varianti di addestramento del filtro** (`script/train_varianti.py`): nessuna migliore dell'attuale.

## Limiti (da sapere)
- Voce espeak ≠ voce dell'operatore; riverbero e rumore sintetici ≠ microfono del MacBook. Contano le **differenze** tra regolazioni, non i valori assoluti.
- hey_jarvis è addestrato su voci sintetiche: le chiamate sintetiche escono favorite.
- **Non misurati**: l'auto-interruzione con la voce vera di Gas (ElevenLabs) dalle casse del Mac, e la CPU con 4 fasi sul Mac. Vanno provati sul Mac; se l'interruzione scatta da sola, `GAS_ASCOLTO_BLOCCHI_INTERRUZIONE=3` nel `.env` torna al comportamento di prima.

## Rifare la simulazione
Serve un ambiente con openwakeword 0.6.0, onnxruntime, scipy, scikit-learn, espeak-ng e sox o ffmpeg. Metti una **copia** del repo in `sim/`, accanto a `script/` (gli script importano `clients/voice` e `scripts/voce` da lì; `sim/` è nel `.gitignore`, così non finisce in git per sbaglio). Poi, dalla cartella `script/`:

```
python sim_registra.py runs/r0 0
python gen_flussi.py
python traccia.py <flusso> <pkl…>
python sweep2.py ; python sweep5.py
FASI=4 python sim_ascolto.py A_chiamate --modo vero --soglia 0.6 --pkl varianti/d4_orig.pkl
python interr.py ; python traccia_fasi.py E_sopra_gas 4 varianti/d3_orig.pkl varianti/d4_orig.pkl varianti/d5_orig.pkl ; python interr_f4.py
python fase2.py <copia del repo> runs/*
```

Audio generato, cache e registrazioni restano fuori da git (`.gitignore` di questa cartella). In `risultati/` ci sono i numeri delle griglie (`sweep*.txt`), i confronti tracce/rilevatore vero (`val_*.txt`), le prove col rilevatore vero (`vero4/`) e i diff originali (`diff_*.patch`).
