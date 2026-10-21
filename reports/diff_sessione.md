# DIFF SESSIONE — 2026-10-21 (dopo il merge di #234: tre stati per un comando firmato)

> Si riscrive a ogni sessione; la storia completa sta in git.

- `gas.py` — `_run_command_avviato` (True da quando il comando parte, azzerato a ogni tool call e in applica_firma); `_esito_diario` «[KO] esito incerto»; applica_firma con `stato` finita/incerta/non_partita; testo d'errore «PARTITO… esito INCERTO» per il modello.
- `gas.py` (storia) — `_blocca_storia`, `_carica_storia_bloccata`, `_unisci_storia_altrui`, `_storia_sync`, `_salva_storia_su_file` che dice se è riuscita, base riconosciuta dal contenuto (sha256), copie «conflitto» collegate e potate, lock con tetto di tempo (R-c4b3-4, R-430, R-431, V bot #236).
- `modules/telegram/bot.py` — messaggio «⚠️ Approvata e PARTITA, ma esito INCERTO».
- `tests/test_unit_kernel.py` — T77u-z, T77aa-ad, T97a-g.
- `.claude/agents/memoria_revisore.md` — righe #428-#437 (più le righe della chat Mani arrivate con main).
- `reports/ultimo_report.md`, `reports/handoff.md`, `reports/diff_sessione.md`, `reports/stato_progetto.md`, `reports/da_mergiare.md`, `reports/roadmap.md` — report.
