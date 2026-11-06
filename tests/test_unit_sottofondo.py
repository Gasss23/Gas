"""Fetta 3 voce (chat M2, 6 nov 2026): compiti lunghi in sottofondo (modules/sottofondo)."""
from __future__ import annotations

import json
import os
import stat
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from modules import sottofondo as sf  # noqa: E402


class _Kernel:
    def __init__(self, eventi=None, errore=None):
        self.eventi = eventi or [{"type": "final", "content": "Ecco il risultato."}]
        self.errore = errore
        self.chiamate = []

    def run_turn(self, prompt, **kw):
        self.chiamate.append((prompt, kw))
        if self.errore:
            raise self.errore
        yield from self.eventi


def _avvisi():
    inviati = []
    return inviati, lambda testo, root: inviati.append(testo)


def test_accoda_scrive_file_privato_e_un_solo_attivo(tmp_path):
    ident, motivo = sf.accoda(tmp_path, "  cerca i prezzi dei voli per Roma  ")
    assert ident and motivo == ""
    f = tmp_path / sf.CARTELLA / f"{ident}.json"
    dati = json.loads(f.read_text(encoding="utf-8"))
    assert dati["compito"] == "cerca i prezzi dei voli per Roma" and dati["stato"] == "in_coda"
    assert stat.S_IMODE(f.stat().st_mode) == 0o600
    assert stat.S_IMODE((tmp_path / sf.CARTELLA).stat().st_mode) == 0o700
    # un secondo compito mentre il primo è appena accodato: rifiutato
    ident2, motivo2 = sf.accoda(tmp_path, "altro")
    assert ident2 is None and "già un compito" in motivo2


@pytest.mark.parametrize("compito", ["", "   ", None, 12, "x" * (sf.COMPITO_MAX + 1)])
def test_accoda_rifiuta_compiti_non_validi(tmp_path, compito):
    ident, motivo = sf.accoda(tmp_path, compito)
    assert ident is None and motivo.startswith("Operazione negata")


def test_processo_morto_non_blocca_la_coda(tmp_path):
    ident, _ = sf.accoda(tmp_path, "uno")
    (tmp_path / sf.CARTELLA / sf.ATTIVO).write_text(
        json.dumps({"id": ident, "pid": 2 ** 22 + 12345, "creato": 0}), encoding="utf-8")
    assert sf.attivo(tmp_path) is None
    assert sf.accoda(tmp_path, "due")[0] is not None


def test_avvia_lancia_il_processo_separato_senza_compito_negli_argomenti(tmp_path):
    ident, _ = sf.accoda(tmp_path, "COMPITO SEGRETO")
    visti = []
    sf.avvia(tmp_path, ident, popen=lambda cmd, **kw: visti.append((cmd, kw)))
    cmd, kw = visti[0]
    assert cmd[-2:] == ["sottofondo", ident] and cmd[1].endswith("gas.py")
    assert "COMPITO SEGRETO" not in " ".join(cmd)
    assert kw["start_new_session"] is True and kw["cwd"] == str(tmp_path)


def test_esegui_riuscito_solo_forte_avviso_e_coda_libera(tmp_path):
    ident, _ = sf.accoda(tmp_path, "riassumi le mail di oggi")
    k = _Kernel()
    inviati, avvisa = _avvisi()
    assert sf.esegui(tmp_path, ident, lambda: k, avvisa) == 0
    prompt, kw = k.chiamate[0]
    assert kw == {"cervello": "forte"} and prompt.endswith("riassumi le mail di oggi")
    dati = json.loads((tmp_path / sf.CARTELLA / f"{ident}.json").read_text(encoding="utf-8"))
    assert dati["stato"] == "ok" and dati["risposta"] == "Ecco il risultato."
    assert len(inviati) == 1 and "Ho finito" in inviati[0] and "Ecco il risultato." in inviati[0]
    assert sf.attivo(tmp_path) is None
    # rieseguire lo stesso compito non fa nulla
    assert sf.esegui(tmp_path, ident, lambda: k, avvisa) == 1 and len(k.chiamate) == 1


@pytest.mark.parametrize("kernel", [
    _Kernel(eventi=[{"type": "error", "content": "Pipeline esausta: forte fermo"}]),
    _Kernel(eventi=[{"type": "final", "content": "   "}]),
    _Kernel(errore=RuntimeError("boom")),
    _Kernel(eventi=[{"type": "tool_res", "output": "x"}]),
])
def test_esegui_fallito_e_ko_con_avviso_mai_crash(tmp_path, kernel):
    ident, _ = sf.accoda(tmp_path, "compito difficile")
    inviati, avvisa = _avvisi()
    assert sf.esegui(tmp_path, ident, lambda: kernel, avvisa) == 1
    dati = json.loads((tmp_path / sf.CARTELLA / f"{ident}.json").read_text(encoding="utf-8"))
    assert dati["stato"] == "ko" and dati["errore"]
    assert len(inviati) == 1 and "non è riuscito" in inviati[0]
    assert sf.attivo(tmp_path) is None


def test_avviso_che_fallisce_non_rompe(tmp_path):
    ident, _ = sf.accoda(tmp_path, "compito")

    def avvisa(t, r):
        raise OSError("telegram giù")
    assert sf.esegui(tmp_path, ident, lambda: _Kernel(), avvisa) == 0


def test_id_con_percorso_non_esce_dalla_cartella(tmp_path):
    (tmp_path / "fuori.json").write_text(json.dumps({"stato": "in_coda", "compito": "x"}),
                                         encoding="utf-8")
    assert sf.esegui(tmp_path, "../fuori", lambda: _Kernel(), lambda t, r: None) == 1


# --- review #695-M2 ---

def test_avvia_raccoglie_il_figlio(tmp_path):
    """R-695-2-M2: il figlio viene atteso da un thread (niente zombie che blocca la coda)."""
    import threading
    attese = threading.Event()

    class _Proc:
        def wait(self):
            attese.set()
    ident, _ = sf.accoda(tmp_path, "uno")
    sf.avvia(tmp_path, ident, popen=lambda cmd, **kw: _Proc())
    assert attese.wait(2)


def test_annulla_libera_la_coda(tmp_path):
    """R-695-4-M2: avvio fallito → compito ko e coda libera subito."""
    ident, _ = sf.accoda(tmp_path, "uno")
    sf.annulla(tmp_path, ident, "avvio non riuscito")
    dati = json.loads((tmp_path / sf.CARTELLA / f"{ident}.json").read_text(encoding="utf-8"))
    assert dati["stato"] == "ko" and sf.attivo(tmp_path) is None
    assert sf.accoda(tmp_path, "due")[0] is not None


def test_esegui_chiude_il_turno(tmp_path):
    """R-695-3-M2: il generatore del kernel viene chiuso dopo il final."""
    chiuso = []

    class _K:
        def run_turn(self, prompt, **kw):
            try:
                yield {"type": "final", "content": "fatto"}
                yield {"type": "final", "content": "mai"}
            finally:
                chiuso.append(True)
    ident, _ = sf.accoda(tmp_path, "uno")
    gen_ref = []
    k = _K()
    orig = k.run_turn

    def _rt(prompt, **kw):
        g = orig(prompt, **kw)
        gen_ref.append(g)  # riferimento vivo: senza close() il finally non scatterebbe
        return g
    k.run_turn = _rt
    assert sf.esegui(tmp_path, ident, lambda: k, lambda t, r: None) == 0 and chiuso == [True]


def test_avviso_rifiutato_finisce_nel_log(tmp_path, caplog):
    """R-695-3-M2: un avviso negato (tetto, Telegram non configurato) si vede nel log."""
    import logging
    ident, _ = sf.accoda(tmp_path, "uno")
    with caplog.at_level(logging.WARNING):
        sf.esegui(tmp_path, ident, lambda: _Kernel(),
                  lambda t, r: ("Operazione negata: tetto di 5 notifiche al giorno", False))
    assert "avviso non inviato" in caplog.text


def test_compito_corrotto_non_rompe(tmp_path):
    """R-695-4-M2: un file del compito senza testo non fa uscire eccezioni."""
    c = tmp_path / sf.CARTELLA
    c.mkdir()
    (c / "rotto.json").write_text(json.dumps({"stato": "in_coda", "compito": 5}), encoding="utf-8")
    assert sf.esegui(tmp_path, "rotto", lambda: _Kernel(), lambda t, r: None) == 1


# --- bot e verifica esterna #345 ---

def test_notifica_possibile(tmp_path, monkeypatch):
    """Bot #345 V-1: niente promessa di avviso se Telegram non può avvisare."""
    from modules.telegram import avviso
    monkeypatch.setenv("GAS_NOTIFICHE_GIORNO", "0")
    assert "spente" in sf.notifica_possibile(tmp_path)
    monkeypatch.setenv("GAS_NOTIFICHE_GIORNO", "5")
    monkeypatch.setattr(avviso, "_manca_configurazione", lambda: "TELEGRAM_BOT_TOKEN")
    assert "non configurato" in sf.notifica_possibile(tmp_path)
    monkeypatch.setattr(avviso, "_manca_configurazione", lambda: None)
    monkeypatch.setattr(avviso, "_uso_oggi", lambda p: 5)
    assert "tetto" in sf.notifica_possibile(tmp_path)
    monkeypatch.setattr(avviso, "_uso_oggi", lambda p: 4)
    assert sf.notifica_possibile(tmp_path) is None


def test_compito_con_processo_morto_diventa_ko_con_avviso(tmp_path):
    """Bot #345 V-3: processo ucciso → compito ko e avviso, coda libera."""
    ident, _ = sf.accoda(tmp_path, "uno")
    c = tmp_path / sf.CARTELLA
    job = json.loads((c / f"{ident}.json").read_text(encoding="utf-8"))
    job["stato"] = "in_corso"
    (c / f"{ident}.json").write_text(json.dumps(job), encoding="utf-8")
    (c / sf.ATTIVO).write_text(json.dumps({"id": ident, "pid": 2 ** 22 + 12345,
                                           "creato": job["creato"]}), encoding="utf-8")
    inviati, avvisa = _avvisi()
    nuovo, _ = sf.accoda(tmp_path, "due", avvisa=avvisa)
    assert nuovo is not None and len(inviati) == 1 and "non è finito" in inviati[0]
    assert json.loads((c / f"{ident}.json").read_text(encoding="utf-8"))["stato"] == "ko"


def test_oltre_la_durata_massima_non_blocca(tmp_path, monkeypatch):
    """Ve #345 V-1/V-2: pid riusato o figlio appeso: oltre la durata massima la coda si libera."""
    monkeypatch.setenv("GAS_SOTTOFONDO_MAX_MIN", "1")
    c = tmp_path / sf.CARTELLA
    c.mkdir()
    (c / sf.ATTIVO).write_text(json.dumps({"id": "x", "pid": os.getpid(),
                                           "creato": 0}), encoding="utf-8")
    assert sf.attivo(tmp_path) is None
    (c / sf.ATTIVO).write_text(json.dumps({"id": "x", "pid": os.getpid(),
                                           "creato": __import__("time").time()}), encoding="utf-8")
    assert sf.attivo(tmp_path) is not None


def test_posto_preso_in_modo_atomico(tmp_path, monkeypatch):
    """Bot #345 V-4: se attivo.json compare fra il controllo e la scrittura, niente secondo compito."""
    c = tmp_path / sf.CARTELLA
    c.mkdir()
    orig = sf.attivo
    chiamate = []

    def _attivo(root):
        r = orig(root)
        if not chiamate:  # dopo il primo controllo un altro processo prende il posto
            (c / sf.ATTIVO).write_text(json.dumps({"id": "altro", "pid": None,
                                                   "creato": __import__("time").time()}))
        chiamate.append(1)
        return r
    monkeypatch.setattr(sf, "attivo", _attivo)
    monkeypatch.setattr(sf, "_ripulisci", lambda root, avvisa: None)
    ident, motivo = sf.accoda(tmp_path, "uno")
    assert ident is None and "già un compito" in motivo


def test_eccezione_interna_avvisa(tmp_path, monkeypatch):
    """R-696-2-M2: anche un'eccezione nel processo separato produce l'avviso."""
    def _rotto(*a, **k):
        raise OSError("disco pieno")
    monkeypatch.setattr(sf, "_esegui", _rotto)
    inviati, avvisa = _avvisi()
    assert sf.esegui(tmp_path, "x", lambda: _Kernel(), avvisa) == 1
    assert len(inviati) == 1 and "interrotto" in inviati[0]


def test_comando_gas_sottofondo(tmp_path):
    """Bot #345 V-2: il comando vero `gas.py sottofondo <id>` esce pulito su un id assente."""
    import subprocess
    gas_py = Path(__file__).resolve().parents[1] / "gas.py"
    r = subprocess.run([sys.executable, str(gas_py), "sottofondo", "inesistente"],
                       cwd=tmp_path, capture_output=True, text=True, timeout=120)
    assert r.returncode == 1 and "Traceback" not in r.stderr


# --- review #697-M2 ---

def test_posto_vuoto_vecchio_non_blocca(tmp_path):
    """R-697-1-M2: un attivo.json vuoto (crash) non blocca la coda per sempre."""
    c = tmp_path / sf.CARTELLA
    c.mkdir()
    p = c / sf.ATTIVO
    p.write_text("")
    os.utime(p, (0, 0))
    assert sf.accoda(tmp_path, "uno", avvisa=lambda t, r: None)[0] is not None


def test_posto_vuoto_recente_aspetta(tmp_path):
    c = tmp_path / sf.CARTELLA
    c.mkdir()
    (c / sf.ATTIVO).write_text("")
    assert sf.accoda(tmp_path, "uno", avvisa=lambda t, r: None)[0] is None


def test_oltre_la_durata_il_processo_vivo_viene_fermato(tmp_path, monkeypatch):
    """R-697-2-M2: oltre la durata massima il gruppo del figlio riceve SIGTERM, compito ko."""
    ident, _ = sf.accoda(tmp_path, "uno")
    c = tmp_path / sf.CARTELLA
    (c / sf.ATTIVO).write_text(json.dumps({"id": ident, "pid": os.getpid(), "creato": 0}))
    fermati = []
    monkeypatch.setattr(sf.os, "killpg", lambda pid, sig: fermati.append((pid, sig)))
    monkeypatch.setattr(sf, "_e_nostro", lambda pid, ident: True)
    inviati, avvisa = _avvisi()
    assert sf.accoda(tmp_path, "due", avvisa=avvisa)[0] is not None
    assert fermati and fermati[0][0] == os.getpid()
    assert json.loads((c / f"{ident}.json").read_text(encoding="utf-8"))["stato"] == "ko"
    assert len(inviati) == 1 and "durata massima" in inviati[0]


def test_esito_tardivo_non_sovrascrive_ko(tmp_path):
    """R-697-2-M2: un compito già chiuso ko non diventa ok né manda un secondo avviso."""
    ident, _ = sf.accoda(tmp_path, "uno")
    c = tmp_path / sf.CARTELLA

    class _K:
        def run_turn(self, prompt, **kw):
            sf.annulla(tmp_path, ident, "oltre la durata massima, fermato")
            yield {"type": "final", "content": "fatto"}
    inviati, avvisa = _avvisi()
    assert sf.esegui(tmp_path, ident, lambda: _K(), avvisa) == 1
    assert json.loads((c / f"{ident}.json").read_text(encoding="utf-8"))["stato"] == "ko"
    assert inviati == []


def test_figlio_senza_posto_non_ruba(tmp_path):
    """R-697-3-M2: un figlio il cui posto è ora di un altro compito non parte."""
    ident, _ = sf.accoda(tmp_path, "uno")
    c = tmp_path / sf.CARTELLA
    (c / sf.ATTIVO).write_text(json.dumps({"id": "altro", "pid": None,
                                           "creato": __import__("time").time()}))
    k = _Kernel()
    assert sf.esegui(tmp_path, ident, lambda: k, lambda t, r: None) == 1 and k.chiamate == []
    assert json.loads((c / sf.ATTIVO).read_text())["id"] == "altro"


# --- review #698-M2 ---

def test_pid_estraneo_non_viene_mai_fermato(tmp_path, monkeypatch):
    """R-698-1-M2: un pid riusato da un processo estraneo (comando diverso) non riceve
    SIGTERM; il compito diventa ko e la coda si libera lo stesso."""
    import subprocess as sp
    estraneo = sp.Popen(["sleep", "30"], start_new_session=True)
    try:
        ident, _ = sf.accoda(tmp_path, "uno")
        c = tmp_path / sf.CARTELLA
        (c / sf.ATTIVO).write_text(json.dumps({"id": ident, "pid": estraneo.pid, "creato": 0}))
        assert sf._e_nostro(estraneo.pid, ident) is False
        fermati = []
        monkeypatch.setattr(sf.os, "killpg", lambda pid, sig: fermati.append(pid))
        assert sf.accoda(tmp_path, "due", avvisa=lambda t, r: None)[0] is not None
        assert fermati == [] and estraneo.poll() is None
        assert json.loads((c / f"{ident}.json").read_text(encoding="utf-8"))["stato"] == "ko"
    finally:
        estraneo.kill()
        estraneo.wait()


def test_e_nostro_riconosce_il_figlio(tmp_path):
    """Il figlio vero (`... gas.py sottofondo <id>`, leader del gruppo) è riconosciuto."""
    import subprocess as sp
    figlio = sp.Popen([sys.executable, "-c", "import time; time.sleep(30)", "gas.py",
                       "sottofondo", "abc123"], start_new_session=True)
    try:
        __import__("time").sleep(0.3)
        assert sf._e_nostro(figlio.pid, "abc123") is True
        assert sf._e_nostro(figlio.pid, "altro") is False
    finally:
        figlio.kill()
        figlio.wait()


def test_e_nostro_con_colonne_strette(tmp_path, monkeypatch):
    """CI #345: con COLUMNS piccolo `ps` troncava il comando e il figlio vero non era
    riconosciuto (oltre la durata non veniva fermato). Con `-ww` la riga è intera."""
    import subprocess as sp
    monkeypatch.setenv("COLUMNS", "20")
    figlio = sp.Popen([sys.executable, "-c", "import time; time.sleep(30)", "gas.py",
                       "sottofondo", "abc123"], start_new_session=True)
    try:
        __import__("time").sleep(0.3)
        assert sf._e_nostro(figlio.pid, "abc123") is True
    finally:
        figlio.kill()
        figlio.wait()
