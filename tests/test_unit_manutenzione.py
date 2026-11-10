"""Terminale, opzione A (chat M2, 9 nov): azioni fisse di manutenzione per Gas.

Modulo (modules/manutenzione), cancello (modules/gate) e collegamento nel kernel (gas.py):
lista chiusa, niente shell, azioni che cambiano Gas solo firmate, mai a voce, in sottofondo
né nel giro notturno. Round-trip §7 col cervello forte finto (come T105 di test_unit_kernel).
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import gas  # noqa: E402
import modules.manutenzione as man  # noqa: E402
from modules.gate import gate as gate_mod  # noqa: E402
from modules.gate.gate import GateClass, gate_classify  # noqa: E402


class _Run:
    """subprocess.run finto: registra argv e risponde con esiti preparati."""

    def __init__(self, esiti=None):
        self.chiamate = []
        self.esiti = list(esiti or [])

    def __call__(self, argv, **kw):
        assert kw.get("shell") is False and "cwd" in kw and kw.get("timeout")
        assert kw["env"]["GIT_TERMINAL_PROMPT"] == "0"
        self.chiamate.append(list(argv))
        codice, out = self.esiti.pop(0) if self.esiti else (0, "")
        return subprocess.CompletedProcess(argv, codice, stdout=out, stderr="")


@pytest.fixture(autouse=True)
def _di_giorno(monkeypatch):
    """I test non dipendono dall'ora reale: di giorno, salvo i test sulla notte."""
    monkeypatch.setattr(man, "e_notte", lambda adesso=None: False)
    monkeypatch.setattr(gas, "_man_e_notte", lambda adesso=None: False)


# ---- modulo ----

def test_liste_uguali_nel_modulo_e_nel_cancello():
    assert set(man.AZIONI_LETTURA) == set(gate_mod._MANUTENZIONE_LETTURA)
    assert set(man.AZIONI_FIRMA) == set(gate_mod._MANUTENZIONE_FIRMA)


@pytest.mark.parametrize("azione", ["rm -rf", "", None, 3, "STATO_GAS", "stato_gas; ls"])
def test_azione_sconosciuta_negata(monkeypatch, tmp_path, azione):
    run = _Run()
    monkeypatch.setattr(man, "_run", run)
    assert man.esegui(azione, tmp_path, firmata=True).startswith("Operazione negata")
    assert run.chiamate == []


@pytest.mark.parametrize("azione", ["aggiorna_gas", "riavvia_voce"])
def test_azioni_che_cambiano_gas_solo_firmate(monkeypatch, tmp_path, azione):
    run = _Run()
    monkeypatch.setattr(man, "_run", run)
    assert "serve la firma" in man.esegui(azione, tmp_path)
    assert run.chiamate == []


def test_stato_gas_lancia_doctor_senza_shell(monkeypatch, tmp_path):
    run = _Run([(0, "\n".join(f"riga {i}" for i in range(100)))])
    monkeypatch.setattr(man, "_run", run)
    out = man.esegui("stato_gas", tmp_path)
    assert run.chiamate == [[sys.executable, str(tmp_path / "gas.py"), "doctor"]]
    assert out.startswith("stato_gas: doctor OK") and "riga 99" in out and "riga 10\n" not in out


def test_stato_gas_tempo_scaduto(monkeypatch, tmp_path):
    def _scade(argv, **kw):
        raise subprocess.TimeoutExpired(argv, kw["timeout"])
    monkeypatch.setattr(man, "_run", _scade)
    assert man.esegui("stato_gas", tmp_path).startswith("[KO] stato_gas: tempo scaduto")


def test_log_voce_solo_righe_dei_tempi(tmp_path):
    (tmp_path / "gas_debug.log").write_text(
        "altro\n" + "".join(f"2026-11-10 10:00:{i:02d},123 - INFO - tempi voce (200): "
                             f"stt=0.{i:02d}s server=1.{i:02d}s\n" for i in range(60))
        + "2026-11-10 10:01:00,000 - WARNING - tempi voce (200): testo libero da una pagina\n"
        # V-3 verifica esterna #363: testo arbitrario che FINISCE col formato dei tempi
        + "2026-11-10 10:01:01,000 - WARNING - segreto tempi voce (200): a=1.0s\n"
        + "segreto 2026-11-10 10:01:02,000 - INFO - tempi voce (200): a=1.0s\n"
        + "segreto non dei tempi\n", encoding="utf-8")
    out = man.esegui("log_voce", tmp_path)
    assert "server=1.59s" in out and "server=1.19s" not in out and "segreto" not in out
    assert "testo libero" not in out  # stesse parole ma non il formato dei tempi
    assert out.count("tempi voce") == man.RIGHE_LOG_VOCE


def test_log_voce_senza_log(tmp_path):
    assert "nessun gas_debug.log" in man.esegui("log_voce", tmp_path)


def test_aggiorna_gas_solo_da_main_pulito(monkeypatch, tmp_path):
    run = _Run([(0, "feat/x\n")])
    monkeypatch.setattr(man, "_run", run)
    assert "non è sul branch main" in man.esegui("aggiorna_gas", tmp_path, firmata=True)
    assert len(run.chiamate) == 1
    run = _Run([(0, "main\n"), (0, " M gas.py\n")])
    monkeypatch.setattr(man, "_run", run)
    assert "modificati a mano" in man.esegui("aggiorna_gas", tmp_path, firmata=True)
    assert all("pull" not in a for a in run.chiamate)


def test_aggiorna_gas_pull_e_pip(monkeypatch, tmp_path):
    (tmp_path / "requirements.txt").write_text("x\n", encoding="utf-8")
    run = _Run([(0, "main\n"), (0, ""), (0, "Fast-forward\n"), (0, "")])
    monkeypatch.setattr(man, "_run", run)
    out = man.esegui("aggiorna_gas", tmp_path, firmata=True)
    assert run.chiamate[2] == ["git", "pull", "--ff-only", "origin", "main"]
    assert run.chiamate[3][:4] == [sys.executable, "-m", "pip", "install"]
    assert "codice aggiornato" in out and "Dipendenze a posto" in out


def test_riavvia_voce_solo_sul_mac(monkeypatch, tmp_path):
    run = _Run()
    monkeypatch.setattr(man, "_run", run)
    monkeypatch.setattr(man.sys, "platform", "linux")
    assert "solo sul Mac" in man.esegui("riavvia_voce", tmp_path, firmata=True)
    monkeypatch.setattr(man.sys, "platform", "darwin")
    monkeypatch.setattr(man.os, "getuid", lambda: 501, raising=False)
    assert man.esegui("riavvia_voce", tmp_path, firmata=True).startswith("riavvia_voce: fatto")
    assert run.chiamate == [["launchctl", "kickstart", "-k", "gui/501/com.gas.voce.server"],
                            ["launchctl", "kickstart", "-k", "gui/501/com.gas.ascolto"]]
    run2 = _Run([(0, ""), (5, "Bootstrap failed: 5: Input/output error")])
    monkeypatch.setattr(man, "_run", run2)
    out = man.esegui("riavvia_voce", tmp_path, firmata=True)
    assert out.startswith("[KO] riavvia_voce: non tutto") and "com.gas.ascolto" in out
    assert len(run2.chiamate) == 2  # il primo riavviato, il secondo provato comunque
    run3 = _Run([(0, ""), (113, 'Could not find service "com.gas.ascolto" in domain')])
    monkeypatch.setattr(man, "_run", run3)
    out = man.esegui("riavvia_voce", tmp_path, firmata=True)
    assert out.startswith("riavvia_voce: fatto") and "in pausa, non riacceso" in out
    assert all("bootstrap" not in a for c in run3.chiamate for a in c)


@pytest.mark.parametrize("valore,ora,notte", [
    ("", 23, True), ("", 3, True), ("", 6, True), ("", 7, False), ("", 22, False),
    ("22-6", 22, True), ("22-6", 6, False), ("1-5", 0, False), ("1-5", 4, True),
    ("x", 2, True), ("25-3", 12, False), ("7-7", 3, True),  # scritto male → 23-7
])
def test_finestra_della_notte(monkeypatch, valore, ora, notte):
    from datetime import datetime
    monkeypatch.undo()  # la funzione vera, non quella «di giorno» della fixture
    monkeypatch.setenv("GAS_MANUTENZIONE_NOTTE", valore)
    assert man.e_notte(datetime(2026, 11, 9, ora, 30)) is notte


@pytest.mark.parametrize("azione", ["aggiorna_gas", "riavvia_voce"])
def test_di_notte_negate_anche_firmate(monkeypatch, tmp_path, azione):
    run = _Run()
    monkeypatch.setattr(man, "_run", run)
    monkeypatch.setattr(man, "e_notte", lambda adesso=None: True)
    assert man.esegui(azione, tmp_path, firmata=True) == man.NOTTE_NEGATA
    assert run.chiamate == []


def test_di_notte_la_lettura_resta(monkeypatch, tmp_path):
    monkeypatch.setattr(man, "e_notte", lambda adesso=None: True)
    assert "nessun gas_debug.log" in man.esegui("log_voce", tmp_path)


# ---- cancello ----

@pytest.mark.parametrize("args,classe", [
    ({"azione": "stato_gas"}, GateClass.UNCERTAIN),
    ({"azione": "log_voce"}, GateClass.UNCERTAIN),
    ({"azione": "aggiorna_gas"}, GateClass.IRREVERSIBLE),
    ({"azione": "riavvia_voce"}, GateClass.IRREVERSIBLE),
    ({"azione": "sconosciuta"}, GateClass.DENY),
    ({}, GateClass.DENY),
    ({"azione": "stato_gas", "comando": "ls"}, GateClass.DENY),
])
def test_cancello(args, classe):
    assert gate_classify("manutenzione", json.dumps(args)) == classe


# ---- kernel ----

def _kernel(tmp_path) -> "gas.GasKernel":
    subprocess.run(["git", "init", "-q", str(tmp_path)], check=True, capture_output=True)
    return gas.GasKernel(root_dir=str(tmp_path))


def test_offerta_solo_nei_turni_a_testo(tmp_path):
    k = _kernel(tmp_path)
    assert k._manutenzione_offerta(voce=False, effimero=False)
    assert not k._manutenzione_offerta(voce=True, effimero=False)
    assert not k._manutenzione_offerta(voce=False, effimero=True)
    k.nel_sottofondo = True
    assert not k._manutenzione_offerta(voce=False, effimero=False)
    notte = gas.GasKernel(root_dir=str(tmp_path), carica_storia=False)
    assert not notte._manutenzione_offerta(voce=False, effimero=False)


def test_kernel_nega_fuori_dai_turni_a_testo_ma_esegue_la_firma(monkeypatch, tmp_path):
    run = _Run([(0, "main\n"), (0, ""), (0, "ok\n")])
    monkeypatch.setattr(man, "_run", run)
    k = _kernel(tmp_path)
    k._turno_manutenzione = False  # turno a voce / sottofondo / notte
    assert "solo a testo" in k.execute_tool_call("manutenzione", '{"azione": "stato_gas"}')
    assert run.chiamate == []
    out = k.execute_tool_call("manutenzione", '{"azione": "aggiorna_gas"}', firmata=True)
    assert "codice aggiornato" in out and len(run.chiamate) == 3


# ---- round-trip §7 col cervello forte finto ----

def _cli(registro, risposte):
    from brains.claude_cli import ClaudeCliClient
    it = iter(risposte)

    def _run(cmd, stdin, cwd, env, timeout):
        f = cmd[cmd.index("--system-prompt-file") + 1]
        registro.append(Path(f).read_text(encoding="utf-8"))
        return subprocess.CompletedProcess(cmd, 0, stdout=json.dumps({
            "type": "result", "subtype": "success", "is_error": False,
            "structured_output": next(it),
            "usage": {"input_tokens": 10, "output_tokens": 3}}), stderr="")
    return lambda timeout=None, **kw: ClaudeCliClient(timeout=timeout, binario="claude",
                                                      runner=_run, **kw)


@pytest.mark.parametrize("voce", [False, True])
def test_round_trip_stato_gas(monkeypatch, tmp_path, voce):
    """A testo: offerto, eseguito, poi la risposta finale (il ciclo continua dopo il tool).
    A voce: non offerto e, chiesto lo stesso, negato senza eseguire nulla."""
    run = _Run([(0, "OK tutto\n")])
    monkeypatch.setattr(man, "_run", run)
    monkeypatch.setenv("GAS_CLAUDE_CLI", "1")
    registro = []
    monkeypatch.setattr(gas, "ClaudeCliClient", _cli(registro, [
        {"testo": "", "chiamate": [{"nome": "manutenzione", "argomenti": {"azione": "stato_gas"}}]},
        {"testo": "Gas sta bene.", "chiamate": []}]))
    k = _kernel(tmp_path)
    ev = list(k.run_turn("come stai?", cervello="forte", voce=voce))
    res = [e["output"] for e in ev if e["type"] == "tool_res"]
    finale = [e["content"] for e in ev if e["type"] == "final"]
    assert finale == ["Gas sta bene."] and len(res) == 1
    if voce:
        assert "manutenzione" not in registro[0] and "solo a testo" in res[0]
        assert run.chiamate == []
    else:
        assert "manutenzione" in registro[0] and res[0].startswith("stato_gas: doctor OK")
        assert len(run.chiamate) == 1


def test_a_voce_nessuna_richiesta_di_firma(monkeypatch, tmp_path):
    """Da un turno a voce aggiorna_gas è negata al cancello: nessun parcheggio per la firma."""
    run = _Run()
    monkeypatch.setattr(man, "_run", run)
    monkeypatch.setenv("GAS_CLAUDE_CLI", "1")
    registro = []
    monkeypatch.setattr(gas, "ClaudeCliClient", _cli(registro, [
        {"testo": "", "chiamate": [{"nome": "manutenzione", "argomenti": {"azione": "aggiorna_gas"}}]},
        {"testo": "Non posso a voce.", "chiamate": []}]))
    k = _kernel(tmp_path)
    parcheggi = []
    monkeypatch.setattr(k.memory, "accoda_approvazione",
                        lambda *a, **kw: parcheggi.append(a) or "id")
    ev = list(k.run_turn("aggiorna gas", cervello="forte", voce=True))
    res = [e for e in ev if e["type"] == "tool_res"]
    assert len(res) == 1 and "solo a testo" in res[0]["output"]
    assert res[0].get("cancello") == "negata" and parcheggi == [] and run.chiamate == []


def test_di_notte_nessuna_richiesta_di_firma(monkeypatch, tmp_path):
    """A testo ma di notte: aggiorna_gas negata al cancello, nessuna firma chiesta."""
    run = _Run()
    monkeypatch.setattr(man, "_run", run)
    monkeypatch.setattr(gas, "_man_e_notte", lambda adesso=None: True)
    monkeypatch.setenv("GAS_CLAUDE_CLI", "1")
    monkeypatch.setattr(gas, "ClaudeCliClient", _cli([], [
        {"testo": "", "chiamate": [{"nome": "manutenzione", "argomenti": {"azione": "aggiorna_gas"}}]},
        {"testo": "Domattina.", "chiamate": []}]))
    k = _kernel(tmp_path)
    parcheggi = []
    monkeypatch.setattr(k.memory, "accoda_approvazione",
                        lambda *a, **kw: parcheggi.append(a) or "id")
    ev = list(k.run_turn("aggiorna gas", cervello="forte"))
    res = [e for e in ev if e["type"] == "tool_res"]
    assert len(res) == 1 and res[0]["output"] == man.NOTTE_NEGATA
    assert parcheggi == [] and run.chiamate == []


def test_round_trip_aggiorna_gas_va_alla_firma(monkeypatch, tmp_path):
    """A testo, aggiorna_gas non parte: va alla firma (qui Telegram non c'è, quindi negata),
    nessun comando eseguito, e il turno arriva comunque alla risposta finale."""
    run = _Run()
    monkeypatch.setattr(man, "_run", run)
    monkeypatch.setenv("GAS_CLAUDE_CLI", "1")
    for chiave in ("TELEGRAM_BOT_TOKEN", "TELEGRAM_ALLOWED_IDS"):
        monkeypatch.delenv(chiave, raising=False)
    registro = []
    monkeypatch.setattr(gas, "ClaudeCliClient", _cli(registro, [
        {"testo": "", "chiamate": [{"nome": "manutenzione", "argomenti": {"azione": "aggiorna_gas"}}]},
        {"testo": "Serve la tua firma.", "chiamate": []}]))
    k = _kernel(tmp_path)
    ev = list(k.run_turn("aggiorna gas", cervello="forte"))
    assert [e["content"] for e in ev if e["type"] == "final"] == ["Serve la tua firma."]
    assert run.chiamate == []


# ---- V-1/V-2 bot #363: esito di una manutenzione firmata ----

def _firma(monkeypatch, k, azione):
    """Una richiesta di manutenzione approvata dall'operatore su Telegram, poi applicata."""
    monkeypatch.setenv("TELEGRAM_ALLOWED_IDS", "4242")
    esito, aid = k.memory.accoda_approvazione("manutenzione", {"azione": azione})
    assert aid, esito
    ok, msg = k.memory.resolve_approval(aid, "approved", telegram_user_id=4242)
    assert ok, msg
    return k.applica_firma(aid)


@pytest.mark.parametrize("esiti, pezzo", [
    ([(0, "main\n"), (0, ""), (1, "fatal: rete giù\n")], "git pull non riuscito"),
    ([(0, "main\n"), (0, ""), (0, "ok\n"), (1, "ERROR: pip\n")], "dipendenze NON installate"),
])
def test_aggiorna_gas_firmata_ma_fallita_non_e_eseguita(monkeypatch, tmp_path, esiti, pezzo):
    """V-1 bot #363: git pull o pip falliti dopo la firma → mai «eseguita»: esito incerto."""
    run = _Run(list(esiti))
    monkeypatch.setattr(man, "_run", run)
    k = _kernel(tmp_path)
    (tmp_path / "requirements.txt").write_text("x\n", encoding="utf-8")
    res = _firma(monkeypatch, k, "aggiorna_gas")
    assert res["eseguita"] is False and res["stato"] == "incerta", res
    assert res["output"].startswith("[KO]") and pezzo in res["output"]


def test_aggiorna_gas_firmata_riuscita_e_eseguita(monkeypatch, tmp_path):
    run = _Run([(0, "main\n"), (0, ""), (0, "ok\n")])
    monkeypatch.setattr(man, "_run", run)
    k = _kernel(tmp_path)
    res = _firma(monkeypatch, k, "aggiorna_gas")
    assert res["eseguita"] is True and res["stato"] == "finita", res


def test_diario_della_manutenzione_solo_esito(tmp_path):
    """V-2 bot #363: nel diario solo [OK]/[KO], mai l'output (doctor, log, git, pip)."""
    k = _kernel(tmp_path)
    assert k._esito_diario("manutenzione", "stato_gas: doctor OK.\nsegreto") == "[OK]"
    assert k._esito_diario("manutenzione", "[KO] aggiorna_gas: git pull non riuscito.\nx") == "[KO]"
    assert k._esito_diario("manutenzione", "Operazione negata: di notte no.") == "[KO]"
