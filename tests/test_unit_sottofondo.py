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
    monkeypatch.setattr(sf, "_identita", lambda pid, ident: True)
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
    monkeypatch.setattr(sf, "_identita", lambda pid, ident: True)
    inviati, avvisa = _avvisi()
    assert sf.accoda(tmp_path, "due", avvisa=avvisa)[0] is not None
    assert fermati and fermati[0][0] == os.getpid()
    assert json.loads((c / f"{ident}.json").read_text(encoding="utf-8"))["stato"] == "ko"
    assert len(inviati) == 1 and "durata massima, fermato" in inviati[0]


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


# ---- Fetta BASSE del sottofondo (chat M2, 7 nov): bot/ve #345 su e323b60 e 46596b4 ----

def test_pid_riusato_non_blocca_la_coda(tmp_path):
    """Ve #345 V-1: pid vivo ma di un altro processo (riusato dopo un crash): la coda è libera,
    il compito vecchio diventa ko con avviso «si è interrotto»."""
    import subprocess as sp
    import time as _t
    estraneo = sp.Popen(["sleep", "30"], start_new_session=True)
    try:
        ident, _ = sf.accoda(tmp_path, "uno")
        c = tmp_path / sf.CARTELLA
        (c / sf.ATTIVO).write_text(json.dumps({"id": ident, "pid": estraneo.pid,
                                               "creato": _t.time()}))
        assert sf.attivo(tmp_path) is None
        inviati, avvisa = _avvisi()
        assert sf.accoda(tmp_path, "due", avvisa=avvisa)[0] is not None
        assert estraneo.poll() is None
        assert json.loads((c / f"{ident}.json").read_text(encoding="utf-8"))["stato"] == "ko"
        assert len(inviati) == 1 and "si è interrotto" in inviati[0]
    finally:
        estraneo.kill()
        estraneo.wait()


def test_identita_sconosciuta_tiene_il_posto(tmp_path, monkeypatch):
    """Senza `ps` (identità non verificabile) un pid vivo e recente tiene occupata la coda:
    meglio aspettare che far girare due compiti insieme."""
    import time as _t
    c = tmp_path / sf.CARTELLA
    c.mkdir()
    (c / sf.ATTIVO).write_text(json.dumps({"id": "x", "pid": os.getpid(), "creato": _t.time()}))
    monkeypatch.setattr(sf, "_identita", lambda pid, ident: None)
    assert sf.attivo(tmp_path) is not None
    assert sf.accoda(tmp_path, "due", avvisa=lambda t, r: None)[0] is None


def test_identita_senza_ps_e_none(monkeypatch):
    """`ps` in errore → None (non si sa), non False."""
    import subprocess as sp
    monkeypatch.setattr(sf.subprocess, "run",
                        lambda *a, **k: sp.CompletedProcess(a, 1, stdout="", stderr="x"))
    monkeypatch.setattr(sf.os, "getpgid", lambda pid: pid)
    assert sf._identita(12345, "x") is None
    assert sf._e_nostro(12345, "x") is False

    def _rotto(*a, **k):
        raise FileNotFoundError("ps")
    monkeypatch.setattr(sf.subprocess, "run", _rotto)
    assert sf._identita(12345, "x") is None


@pytest.mark.parametrize("pid", ["proprio", None])
@pytest.mark.parametrize("creato", ["abc", "nan", "inf", [1], {"a": 1}, 1e18])
def test_creato_non_numerico_non_blocca(tmp_path, monkeypatch, creato, pid):
    """Bot #345 V-4 / ve V-2, R-701-1/2-M2: «creato» non numerico, non finito o nel futuro →
    posto scaduto e ripulito, sia con pid ancora da scrivere (None) sia con un pid vivo che
    risulta nostro (così l'esito non dipende dal controllo d'identità)."""
    monkeypatch.setattr(sf, "_identita", lambda p, i: True)
    monkeypatch.setattr(sf.os, "killpg", lambda p, s: None)  # mai un segnale a pytest
    c = tmp_path / sf.CARTELLA
    c.mkdir()
    (c / sf.ATTIVO).write_text(json.dumps({"id": "x", "pid": os.getpid() if pid else None,
                                           "creato": creato}))
    if creato == 1e18 and pid:
        # Ve #346 V-1: data nel futuro ma processo vivo e nostro → il posto resta suo
        assert sf.attivo(tmp_path) is not None
        assert sf.accoda(tmp_path, "due", avvisa=lambda t, r: None)[0] is None
        return
    assert sf.attivo(tmp_path) is None
    assert sf.accoda(tmp_path, "due", avvisa=lambda t, r: None)[0] is not None


@pytest.mark.parametrize("valore", ["inf", "-inf", "nan", "abc", "", "1e308"])
def test_durata_inf_nan_torna_al_default(monkeypatch, valore):
    """Bot #345 (46596b4) V-3: GAS_SOTTOFONDO_MAX_MIN non finito o non numerico → 60 minuti."""
    monkeypatch.setenv("GAS_SOTTOFONDO_MAX_MIN", valore)
    assert sf._durata_max_s() == sf.DURATA_MAX_S_DEFAULT


def test_oltre_la_durata_non_nostro_non_dice_fermato(tmp_path, monkeypatch):
    """R-699-1-M2: identità non verificabile → non fermato e l'avviso non dice «fermato»;
    killpg fallito → idem."""
    for identita, killpg_rotto, atteso in ((None, False, "forse ancora in esecuzione"),
                                          (True, True, "oltre la durata massima.")):
        root = tmp_path / str(identita)
        root.mkdir()
        ident, _ = sf.accoda(root, "uno")
        c = root / sf.CARTELLA
        (c / sf.ATTIVO).write_text(json.dumps({"id": ident, "pid": os.getpid(), "creato": 0}))
        monkeypatch.setattr(sf, "_identita", lambda pid, i, v=identita: v)

        def _killpg(pid, sig, rotto=killpg_rotto):
            if rotto:
                raise PermissionError("no")
            raise AssertionError("killpg non doveva essere chiamato")
        monkeypatch.setattr(sf.os, "killpg", _killpg)
        inviati, avvisa = _avvisi()
        sf._ripulisci(root, avvisa)
        assert len(inviati) == 1 and atteso in inviati[0] and "fermato" not in inviati[0]


def test_pulizia_dei_compiti_finiti_vecchi(tmp_path, monkeypatch):
    """Bot #345 (46596b4) V-2: compiti finiti più vecchi di GAS_SOTTOFONDO_GIORNI cancellati;
    quelli in corso, recenti o illeggibili restano."""
    import time as _t
    monkeypatch.setenv("GAS_SOTTOFONDO_GIORNI", "7")
    c = tmp_path / sf.CARTELLA
    c.mkdir()
    vecchio = _t.time() - 8 * 86400

    def _job(nome, stato, mtime):
        f = c / nome
        f.write_text(json.dumps({"id": nome, "stato": stato, "compito": "x"}))
        os.utime(f, (mtime, mtime))
        return f
    ok_vecchio = _job("a.json", "ok", vecchio)
    ko_vecchio = _job("b.json", "ko", vecchio)
    in_corso = _job("c.json", "in_corso", vecchio)
    ok_recente = _job("d.json", "ok", _t.time())
    rotto = c / "e.json"
    rotto.write_text("{")
    os.utime(rotto, (vecchio, vecchio))
    tmp = c / ".posto.1.abc"
    tmp.write_text("{}")
    os.utime(tmp, (vecchio, vecchio))
    altro = c / "nota.txt"
    altro.write_text("x")
    os.utime(altro, (vecchio, vecchio))
    assert sf.accoda(tmp_path, "nuovo")[0] is not None
    # bot #349 (a9a17a5) V-1: anche un compito «in_corso» vecchio senza posto si cancella
    assert not ok_vecchio.exists() and not ko_vecchio.exists() and not tmp.exists()
    assert not in_corso.exists()
    assert ok_recente.exists() and rotto.exists() and altro.exists()


def test_giorni_conservazione_non_validi(monkeypatch):
    for v in ("inf", "nan", "abc", "0", "-3", "1e308"):
        monkeypatch.setenv("GAS_SOTTOFONDO_GIORNI", v)
        assert 1.0 <= sf._giorni_conservazione() <= sf.GIORNI_CONSERVAZIONE_DEFAULT


def test_controlla_avvisa_al_crash_senza_nuova_richiesta(tmp_path):
    """Bot #345 (e323b60) V-1: controlla() (chiamata a ogni turno) chiude il compito con pid
    morto e avvisa, senza aspettare il compito successivo; coda vuota → nessun lavoro."""
    import time as _t
    inviati, avvisa = _avvisi()
    sf.controlla(tmp_path, avvisa)  # nemmeno la cartella: niente, nessuna eccezione
    assert inviati == [] and not (tmp_path / sf.CARTELLA).exists()
    ident, _ = sf.accoda(tmp_path, "uno")
    c = tmp_path / sf.CARTELLA
    (c / sf.ATTIVO).write_text(json.dumps({"id": ident, "pid": 2 ** 22 + 12345,
                                           "creato": _t.time()}))
    sf.controlla(tmp_path, avvisa)
    assert len(inviati) == 1 and "non è finito" in inviati[0]
    assert not (c / sf.ATTIVO).exists()
    assert json.loads((c / f"{ident}.json").read_text(encoding="utf-8"))["stato"] == "ko"
    sf.controlla(tmp_path, avvisa)  # una sola volta
    assert len(inviati) == 1


def test_controlla_non_solleva(tmp_path, monkeypatch):
    def _rotto(root, avvisa):
        raise RuntimeError("x")
    monkeypatch.setattr(sf, "_ripulisci", _rotto)
    c = tmp_path / sf.CARTELLA
    c.mkdir()
    (c / sf.ATTIVO).write_text("{}")
    sf.controlla(tmp_path)


def test_orologio_indietro_non_ferma_il_figlio_vero(tmp_path):
    """Ve #346 V-1 / R-702-1-M2: «creato» nel futuro (orologio portato indietro) con il NOSTRO
    figlio vivo: il posto resta occupato, niente killpg, niente secondo compito, niente avviso."""
    import subprocess as sp
    import time as _t
    ident, _ = sf.accoda(tmp_path, "uno")
    figlio = sp.Popen([sys.executable, "-c", "import time; time.sleep(30)", "gas.py",
                       "sottofondo", ident], start_new_session=True)
    try:
        _t.sleep(0.3)
        c = tmp_path / sf.CARTELLA
        (c / sf.ATTIVO).write_text(json.dumps({"id": ident, "pid": figlio.pid,
                                               "creato": _t.time() + 600}))
        assert sf.attivo(tmp_path) is not None
        inviati, avvisa = _avvisi()
        sf.controlla(tmp_path, avvisa)
        assert sf.accoda(tmp_path, "due", avvisa=avvisa)[0] is None
        assert figlio.poll() is None and inviati == []
        assert (c / sf.ATTIVO).exists()
    finally:
        figlio.kill()
        figlio.wait()


def test_orologio_indietro_pid_morto_o_assente_libera(tmp_path):
    """«creato» nel futuro senza processo vivo: la coda si libera (R-701-2-M2 resta chiusa)."""
    import time as _t
    c = tmp_path / sf.CARTELLA
    c.mkdir()
    for pid in (None, 2 ** 22 + 12345):
        (c / sf.ATTIVO).write_text(json.dumps({"id": "x", "pid": pid, "creato": _t.time() + 600}))
        assert sf.attivo(tmp_path) is None


# ---- Fetta BASSE 2 del sottofondo (chat M2, 7 nov): bot #346 e R-703-1-M2 ----

def test_compito_appena_riuscito_non_diventa_ko(tmp_path):
    """Bot #346 (3ee02dd) V-1: se il figlio ha scritto «ok» e tolto il posto mentre un altro
    processo ripulisce, il compito resta «ok» e non parte un avviso «non è finito»."""
    import time as _t
    ident, _ = sf.accoda(tmp_path, "uno")
    c = tmp_path / sf.CARTELLA
    f = c / f"{ident}.json"
    job = json.loads(f.read_text(encoding="utf-8"))
    job.update(stato="ok", risposta="fatto")
    f.write_text(json.dumps(job), encoding="utf-8")
    (c / sf.ATTIVO).write_text(json.dumps({"id": ident, "pid": 2 ** 22 + 12345,
                                           "creato": _t.time()}))
    inviati, avvisa = _avvisi()
    sf._ripulisci(tmp_path, avvisa)
    assert json.loads(f.read_text(encoding="utf-8"))["stato"] == "ok"
    assert inviati == [] and not (c / sf.ATTIVO).exists()
    assert sf.annulla(tmp_path, ident, "x") is False


def test_annulla_chiude_solo_compiti_aperti(tmp_path):
    ident, _ = sf.accoda(tmp_path, "uno")
    assert sf.annulla(tmp_path, ident, "prova") is True
    f = tmp_path / sf.CARTELLA / f"{ident}.json"
    assert json.loads(f.read_text(encoding="utf-8"))["errore"] == "prova"
    assert sf.annulla(tmp_path, ident, "seconda") is False
    assert json.loads(f.read_text(encoding="utf-8"))["errore"] == "prova"


def test_controlla_pulisce_al_massimo_una_volta_l_ora(tmp_path, monkeypatch):
    """Bot #346 (2d0977e) V-3: la pulizia dei compiti vecchi parte anche da controlla()."""
    chiamate = []
    monkeypatch.setattr(sf, "_pulisci_vecchi", lambda root: chiamate.append(root))
    monkeypatch.setattr(sf, "_ultima_pulizia", None)
    sf.controlla(tmp_path)  # cartella assente: niente
    assert chiamate == []
    (tmp_path / sf.CARTELLA).mkdir()
    sf.controlla(tmp_path)
    sf.controlla(tmp_path)
    assert chiamate == [tmp_path]


def test_data_futura_con_processo_estraneo_libera_il_posto(tmp_path):
    """R-703-1-M2: «creato» nel futuro e pid vivo ma sicuramente estraneo (leader con un altro
    comando): posto libero, il processo estraneo non viene toccato."""
    import subprocess as sp
    import time as _t
    estraneo = sp.Popen(["sleep", "30"], start_new_session=True)
    try:
        ident, _ = sf.accoda(tmp_path, "uno")
        c = tmp_path / sf.CARTELLA
        (c / sf.ATTIVO).write_text(json.dumps({"id": ident, "pid": estraneo.pid,
                                               "creato": _t.time() + 600}))
        assert sf.attivo(tmp_path) is None
        assert sf.accoda(tmp_path, "due", avvisa=lambda t, r: None)[0] is not None
        assert estraneo.poll() is None
    finally:
        estraneo.kill()
        estraneo.wait()


def test_corsa_figlio_finisce_durante_la_pulizia_niente_avviso(tmp_path, monkeypatch):
    """Bot #346 V-1, la corsa vera: _ripulisci legge il compito «in_corso», poi il figlio
    scrive «ok» prima di annulla → annulla non chiude niente e non parte «non è finito»."""
    import time as _t
    ident, _ = sf.accoda(tmp_path, "uno")
    c = tmp_path / sf.CARTELLA
    f = c / f"{ident}.json"
    (c / sf.ATTIVO).write_text(json.dumps({"id": ident, "pid": 2 ** 22 + 12345,
                                           "creato": _t.time()}))
    vero = sf.annulla

    def _figlio_finisce_prima(root, i, motivo):
        job = json.loads(f.read_text(encoding="utf-8"))
        job.update(stato="ok")
        f.write_text(json.dumps(job), encoding="utf-8")
        return vero(root, i, motivo)
    monkeypatch.setattr(sf, "annulla", _figlio_finisce_prima)
    inviati, avvisa = _avvisi()
    sf._ripulisci(tmp_path, avvisa)
    assert inviati == [] and json.loads(f.read_text(encoding="utf-8"))["stato"] == "ok"


def test_eccezione_dopo_ok_niente_avviso_di_errore(tmp_path, monkeypatch):
    """R-706-2-M2: un'eccezione arrivata dopo che il compito è già «ok» non manda
    «si è interrotto per un errore interno»; prima di «ok» sì."""
    ident, _ = sf.accoda(tmp_path, "uno")
    f = tmp_path / sf.CARTELLA / f"{ident}.json"

    def _gia_ok(root, i, k, a):
        job = json.loads(f.read_text(encoding="utf-8"))
        job.update(stato="ok")
        f.write_text(json.dumps(job), encoding="utf-8")
        raise OSError("dopo ok")
    monkeypatch.setattr(sf, "_esegui", _gia_ok)
    inviati, avvisa = _avvisi()
    assert sf.esegui(tmp_path, ident, lambda: None, avvisa) == 1
    assert inviati == [] and json.loads(f.read_text(encoding="utf-8"))["stato"] == "ok"

    altro = tmp_path / "due"
    altro.mkdir()
    ident2, _ = sf.accoda(altro, "due")

    def _rotto(root, i, k, a):
        raise OSError("prima")
    monkeypatch.setattr(sf, "_esegui", _rotto)
    assert sf.esegui(altro, ident2, lambda: None, avvisa) == 1
    assert len(inviati) == 1 and "errore interno" in inviati[0]
    assert json.loads((altro / sf.CARTELLA / f"{ident2}.json").read_text())["stato"] == "ko"


def test_scrittura_fallita_avvisa_lo_stesso(tmp_path, monkeypatch):
    """Bot #349 V-1: se la riscrittura del compito fallisce (disco pieno), la pulizia
    avvisa comunque l'operatore invece di lasciare il compito «in_corso» in silenzio."""
    import time as _t
    ident, _ = sf.accoda(tmp_path, "uno")
    c = tmp_path / sf.CARTELLA
    (c / sf.ATTIVO).write_text(json.dumps({"id": ident, "pid": 2 ** 22 + 12345,
                                           "creato": _t.time()}))
    vero = sf._scrivi_privato

    def _disco_pieno(percorso, dati):
        if percorso.name == f"{ident}.json":
            raise OSError("disco pieno")
        return vero(percorso, dati)
    monkeypatch.setattr(sf, "_scrivi_privato", _disco_pieno)
    inviati, avvisa = _avvisi()
    sf._ripulisci(tmp_path, avvisa)
    assert len(inviati) == 1 and "non è finito" in inviati[0]


def test_posto_non_tolto_avviso_finale_parte_lo_stesso(tmp_path, monkeypatch):
    """Bot #349 (147d6c8) V-1: se togliere attivo.json fallisce (permessi), il compito resta
    «ok» e l'avviso finale col risultato parte comunque (niente silenzio)."""
    ident, _ = sf.accoda(tmp_path, "uno")
    vero = Path.unlink

    def _unlink(self, *a, **k):
        if self.name == sf.ATTIVO:
            raise PermissionError("no")
        return vero(self, *a, **k)
    monkeypatch.setattr(Path, "unlink", _unlink)
    inviati, avvisa = _avvisi()
    assert sf.esegui(tmp_path, ident, lambda: _Kernel(), avvisa) == 0
    assert len(inviati) == 1 and inviati[0].startswith("Ho finito")
    f = tmp_path / sf.CARTELLA / f"{ident}.json"
    assert json.loads(f.read_text(encoding="utf-8"))["stato"] == "ok"


# ---- Fetta 3.2 (chat M2, 7 nov): compiti finiti da leggere a voce ----

def _finito(root, ident, stato="ok", fine=None, **extra):
    import time as _t
    c = root / sf.CARTELLA
    c.mkdir(exist_ok=True)
    dati = {"id": ident, "compito": f"compito {ident}", "stato": stato, "risposta": "r " * 300,
            "fine": _t.time() - 10 if fine is None else fine, **extra}
    (c / f"{ident}.json").write_text(json.dumps(dati))
    return c / f"{ident}.json"


def test_da_leggere_filtra_e_ordina(tmp_path, monkeypatch):
    import time as _t
    adesso = _t.time()
    _finito(tmp_path, "a", fine=adesso - 300)
    _finito(tmp_path, "b", fine=adesso - 100)
    _finito(tmp_path, "c", fine=adesso - 200, stato="ko")
    _finito(tmp_path, "d", stato="in_corso")
    _finito(tmp_path, "e", letto_a_voce=True)
    _finito(tmp_path, "f", fine=adesso - 3 * 86400)
    _finito(tmp_path, "g", fine="abc")
    (tmp_path / sf.CARTELLA / "h.json").write_text(json.dumps({"id": "altro", "stato": "ok",
                                                               "fine": adesso}))
    assert [j["id"] for j in sf.da_leggere(tmp_path)] == ["a", "c"]  # i più vecchi, max 2
    monkeypatch.setenv("GAS_SOTTOFONDO_LEGGI_ORE", "nan")
    assert sf._ore_lettura() == 24.0
    assert sf.da_leggere(tmp_path / "manca") == []


def test_frase_finiti_corta_e_segna_letti(tmp_path):
    f = _finito(tmp_path, "a")
    jobs = sf.da_leggere(tmp_path)
    frase = sf.frase_finiti(jobs)
    assert frase.startswith("Ho finito il compito in sottofondo «compito a»: ")
    assert len(frase) < 80 + sf.LETTURA_RISPOSTA_MAX + 60
    sf.segna_letti(tmp_path, jobs)
    assert json.loads(f.read_text())["letto_a_voce"] is True
    assert sf.da_leggere(tmp_path) == []
    sf.segna_letti(tmp_path, [{"id": "../../fuori"}])  # nessuna scrittura fuori, nessuna eccezione
    assert not (tmp_path.parent / "fuori.json").exists()


def test_frase_finiti_risposta_vuota():
    """Ve #350 V-2: compito ok senza risposta → frase chiusa, senza «:» finali."""
    for risposta in ("", None, "   "):
        frase = sf.frase_finiti([{"id": "a", "compito": "t", "stato": "ok", "risposta": risposta}])
        assert frase == "Ho finito il compito in sottofondo «t»."


def test_scrittura_temporanea_con_nome_unico(tmp_path, monkeypatch):
    """Ve #350 V-3: due scritture dello stesso processo usano file temporanei diversi."""
    nomi = []
    vero = sf.os.replace

    def _replace(src, dst):
        nomi.append(Path(src).name)
        return vero(src, dst)
    monkeypatch.setattr(sf.os, "replace", _replace)
    sf._scrivi_privato(tmp_path / "a.json", {"x": 1})
    sf._scrivi_privato(tmp_path / "a.json", {"x": 2})
    assert len(set(nomi)) == 2 and all(".tmp." in n for n in nomi)


@pytest.mark.parametrize("stato", ["in_corso", "in_coda"])
def test_pulizia_non_tocca_il_compito_che_ha_il_posto(tmp_path, monkeypatch, stato):
    """Il compito aperto vecchio che ha ancora il posto in coda non si cancella."""
    import time as _t
    c = tmp_path / sf.CARTELLA
    c.mkdir()
    vecchio = _t.time() - 8 * 86400
    f = c / "x.json"
    f.write_text(json.dumps({"id": "x", "stato": stato, "compito": "t"}))
    os.utime(f, (vecchio, vecchio))
    (c / sf.ATTIVO).write_text(json.dumps({"id": "x", "pid": None, "creato": _t.time()}))
    sf._pulisci_vecchi(tmp_path)
    assert f.exists()


def test_pulizia_oraria_con_orologio_monotono(tmp_path, monkeypatch):
    """Bot #349 (a9a17a5) V-2: il limite orario usa time.monotonic, non l'ora di sistema."""
    chiamate = []
    monkeypatch.setattr(sf, "_pulisci_vecchi", lambda root: chiamate.append(root))
    monkeypatch.setattr(sf, "_ultima_pulizia", None)
    (tmp_path / sf.CARTELLA).mkdir()
    orologio = [1000.0]
    monkeypatch.setattr(sf.time, "monotonic", lambda: orologio[0])
    sf.controlla(tmp_path)
    orologio[0] += 3601
    sf.controlla(tmp_path)
    assert len(chiamate) == 2


@pytest.mark.parametrize("stato", ["in_corso", "in_coda"])
def test_pulizia_compito_aperto_vecchio_senza_posto(tmp_path, stato):
    """Bot #354 V-1: anche «in_coda» vecchio senza posto si cancella, come «in_corso»."""
    import time as _t
    c = tmp_path / sf.CARTELLA
    c.mkdir()
    vecchio = _t.time() - 8 * 86400
    f = c / "y.json"
    f.write_text(json.dumps({"id": "y", "stato": stato, "compito": "t"}))
    os.utime(f, (vecchio, vecchio))
    sf._pulisci_vecchi(tmp_path)
    assert not f.exists()
