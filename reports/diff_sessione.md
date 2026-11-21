# Diff della sessione — 2026-11-20 — Voce: registrazione solo con «Hey Jarvis» veri

Si riscrive a ogni sessione; la storia completa sta in git. Ramo fix/voce-registra-solo-parola da main d03e5bf2.

- `scripts/voce/registra_voce.py`:
  - `Registratore._una_clip`: volume, poi punteggio del modello della parola (`misura`); sotto soglia o picco nei primi 0,5 s → «rifallo»; taglio a 3 s sul picco;
  - `Registratore.positivi`: fino a 3 prove per clip; finestra di 6 s per i gruppi lontani, con istruzione se il bip non si sente;
  - `MotoreOWW.misura`: punteggio massimo e indice, col modello già caricato;
  - `main`: passa `misura` e la soglia base al registratore.
- `scripts/voce/LEGGIMI.md`: come funziona il controllo della parola.
- `tests/test_unit_voce_ascolto.py`: test esistente adeguato; tre test nuovi (rumore scartato, finestra lontana e taglio sul picco, parola tagliata all'inizio).
- `reports/stato_progetto.md`, report di fine task, `.claude/agents/memoria_revisore.md` (commit del revisore).
