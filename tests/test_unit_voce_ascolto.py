"""Voce H24 (R8, chat Mani): clients/voice/ascolto.py con microfono, rilevatore e server
finti (nessun audio vero), più i file di scripts/voce/."""
import http.server
import io
import json
import logging
import os
import plistlib
import stat
import subprocess
import sys
import threading
import time
import wave
from pathlib import Path

import pytest

RADICE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RADICE))
from clients.voice import ascolto as a  # noqa: E402

TOKEN = "tok-SEGRETO-ascolto-123"
SILENZIO = [10] * a.BLOCCO           # rumore di fondo, sotto la soglia della voce
VOCE = [2000] * a.BLOCCO             # voce
PAROLA = "PAROLA"                    # blocco che il rilevatore finto riconosce


def _blocchi(*pezzi):
    """Sequenza di blocchi: (blocco, quante volte) o un blocco singolo."""
    for p in pezzi:
        b, n = p if isinstance(p, tuple) else (p, 1)
        for _ in range(n):
            yield b


def _sec(s):
    return int(round(s / a.SEC_BLOCCO))


class Finti:
    def __init__(self, esito=(True, b"MP3", "")):
        self.inviati, self.riprodotti, self.bip, self.svuotati, self.azzerati = [], [], [], 0, 0
        self.esito = esito

    def rilevatore(self, b):
        return 1.0 if b == PAROLA else 0.0

    def invia(self, wav):
        self.inviati.append(wav)
        return self.esito

    def riproduci(self, audio):
        self.riprodotti.append(audio)

    def suona(self, tipo):
        self.bip.append(tipo)

    def svuota(self):
        self.svuotati += 1

    def azzera(self):
        self.azzerati += 1

    def ascolto(self, blocchi, **k):
        return a.Ascolto(iter(blocchi), self.rilevatore, self.invia, self.riproduci, self.suona,
                         svuota=self.svuota, azzera_rilevatore=self.azzera, **k)


def _campioni(wav):
    with wave.open(io.BytesIO(wav)) as w:
        assert (w.getnchannels(), w.getsampwidth(), w.getframerate()) == (1, 2, a.FREQ)
        return w.getnframes()


# ── privacy: prima della parola niente esce ──

def test_senza_parola_niente_invio():
    f = Finti()
    f.ascolto(_blocchi((VOCE, 500), (SILENZIO, 50))).gira()
    assert f.inviati == [] and f.riprodotti == [] and f.bip == []


def test_parola_bip_registrazione_e_risposta():
    f = Finti()
    f.ascolto(_blocchi(PAROLA, (SILENZIO, 3), (VOCE, 20), (SILENZIO, 30)),
              finestra_s=0).gira()
    assert f.bip == ["ok"] and f.riprodotti == [b"MP3"] and len(f.inviati) == 1
    # niente silenzio prima della voce; dopo, il silenzio che chiude la richiesta (0,8 s)
    assert _campioni(f.inviati[0]) == (20 + _sec(0.8)) * a.BLOCCO
    # svuota dopo bip e risposta; azzera prima della risposta (fetta 41: il rilevatore
    # ascolta mentre Gas parla), prima della finestra (R-680-1) e a fine conversazione
    assert f.svuotati >= 2 and f.azzerati == 3


def test_se_non_parli_dopo_la_parola_non_si_invia():
    f = Finti()
    f.ascolto(_blocchi(PAROLA, (SILENZIO, _sec(a.ATTESA_VOCE_S) + 5), (VOCE, 30))).gira()
    assert f.bip == ["ok"] and f.inviati == []


def test_un_clic_dopo_la_parola_non_apre_una_richiesta():
    """R-615-6: dopo la parola la voce comincia con 3 blocchi di fila, come nella
    finestra: un clic (un blocco) non manda niente."""
    f = Finti()
    f.ascolto(_blocchi(PAROLA, (SILENZIO, 3), VOCE, (SILENZIO, 3), VOCE, VOCE,
                       (SILENZIO, _sec(a.ATTESA_VOCE_S) + 5))).gira()
    assert f.inviati == []


def test_l_attesa_dopo_la_parola_conta_anche_i_rumori():
    """R-616-2: rumori brevi (forte-forte-debole) non allungano l'attesa oltre i 5 s:
    dopo ATTESA_VOCE_S la voce vera non apre più una richiesta."""
    f = Finti()
    rumore = [VOCE, VOCE, SILENZIO]
    n = _sec(a.ATTESA_VOCE_S) // 3 + 2
    f.ascolto(_blocchi(PAROLA, *(rumore * n), (VOCE, 10), (SILENZIO, 10))).gira()
    assert f.inviati == []


def test_l_inizio_della_voce_resta_nella_richiesta():
    f = Finti()
    f.ascolto(_blocchi(PAROLA, VOCE, (SILENZIO, 2), (VOCE, 5), (SILENZIO, 10)),
              finestra_s=0).gira()
    assert _campioni(f.inviati[0]) == (5 + 10) * a.BLOCCO


def test_registrazione_al_massimo_30_secondi():
    f = Finti()
    f.ascolto(_blocchi(PAROLA, (VOCE, _sec(60))), finestra_s=0).gira()
    assert _campioni(f.inviati[0]) == _sec(a.REGISTRAZIONE_MAX_S) * a.BLOCCO


VOCE_PIANA = [300] * a.BLOCCO        # voce bassa, come al microfono del MacBook Air


def test_voce_piana_passa_col_default():
    """Prova del 2026-11-05 sul MacBook Air: con soglia 500 la voce dopo il bip non
    passava («torno ad aspettare»). Col default (200) una voce a RMS 300 apre la richiesta."""
    f = Finti()
    f.ascolto(_blocchi(PAROLA, (VOCE_PIANA, 10), (SILENZIO, 10)), finestra_s=0).gira()
    assert len(f.inviati) == 1 and _campioni(f.inviati[0]) == (10 + 10) * a.BLOCCO


def _main_finto(monkeypatch, tmp_path, ambiente, conferma_cls=None):
    """Fa girare `main` con microfono, rilevatore, download e Ascolto finti e restituisce
    gli argomenti con cui ha costruito Ascolto. R-671-2: il finto usa k.get e il ciclo di
    riprova di main (§9) fa fallire subito il test invece di restare appeso."""
    monkeypatch.setattr(a, "_GAS_ROOT", tmp_path)
    monkeypatch.setenv("GAS_VOICE_TOKEN", TOKEN)
    for k in ("GAS_ASCOLTO_VOCE_RMS", "GAS_ASCOLTO_CONFERMA", "GAS_ASCOLTO_INTERRUZIONE",
              "GAS_VOICE_FINESTRA", "GAS_VOICE_SEGUITO_MAX",
              "GAS_ASCOLTO_SOGLIA_INTERRUZIONE", "GAS_VOICE_URL", "GAS_VOICE_PORT"):
        monkeypatch.delenv(k, raising=False)
    for k, v in ambiente.items():
        monkeypatch.setenv(k, v)
    monkeypatch.setattr(a, "rilevatore_openwakeword", lambda m: (lambda b: 0.0, lambda: None))
    monkeypatch.setattr(a, "scarica_conferma", lambda url, token: b"SI")
    monkeypatch.setattr(a, "Conferma", conferma_cls or (lambda scarica: (lambda: scarica())))
    monkeypatch.setattr(a.time, "sleep",
                        lambda s: pytest.fail("main è finito nel ciclo di riprova"))

    class Mic:
        def blocchi(self):
            return iter(())

        def svuota(self):
            pass

        def chiudi(self):
            pass
    visti = []

    class AscoltoFinto:
        def __init__(self, *args, **k):
            visti.append(k)

        def gira(self):
            raise KeyboardInterrupt
    monkeypatch.setattr(a, "Microfono", Mic)
    monkeypatch.setattr(a, "Ascolto", AscoltoFinto)
    assert a.main() == 0 and len(visti) == 1
    return visti[0]


@pytest.mark.parametrize("valore,atteso", [(None, 200.0), ("350", 350.0), ("abc", 200.0)])
def test_main_passa_la_soglia_della_voce(monkeypatch, tmp_path, valore, atteso):
    """`main` passa ad Ascolto GAS_ASCOLTO_VOCE_RMS, e senza variabile il default 200."""
    k = _main_finto(monkeypatch, tmp_path,
                    {} if valore is None else {"GAS_ASCOLTO_VOCE_RMS": valore})
    assert k.get("voce_rms") == atteso
    assert k.get("finestra_s") == 40.0 and k.get("seguito_max_s") == 15.0
    assert k.get("invia_seguito") is not None
    assert k.get("soglia_interruzione") == a.SOGLIA_INTERRUZIONE_PREDEFINITA


@pytest.mark.parametrize("valore,atteso", [(None, b"SI"), ("1", b"SI"), ("0", None)])
def test_main_passa_la_conferma(monkeypatch, tmp_path, valore, atteso):
    """R-671-1: `main` rispetta GAS_ASCOLTO_CONFERMA (0 = solo il bip)."""
    k = _main_finto(monkeypatch, tmp_path,
                    {} if valore is None else {"GAS_ASCOLTO_CONFERMA": valore})
    conferma = k.get("conferma")
    assert conferma is not None and conferma() == atteso


def test_leggimi_riporta_il_default_della_voce():
    """La tabella di scripts/voce/LEGGIMI.md resta allineata al default del codice."""
    testo = (RADICE / "scripts" / "voce" / "LEGGIMI.md").read_text(encoding="utf-8")
    assert f"| `GAS_ASCOLTO_VOCE_RMS` | {a.VOCE_RMS_PREDEFINITO:g} |" in testo
    assert (f"| `GAS_ASCOLTO_SOGLIA_INTERRUZIONE` | {a.SOGLIA_INTERRUZIONE_PREDEFINITA:g} |"
            in testo)
    assert "| `GAS_ASCOLTO_CONFERMA` | 1 |" in testo


# ── fetta 41: interrompere Gas mentre parla, solo con la parola ──

QUASI = "QUASI"                      # blocco con punteggio 0.6: sopra la soglia normale,
                                     # sotto quella dell'interruzione (0.7)


class Suona:
    """Riproduzione finta: dura `blocchi` letture del microfono, poi finisce."""

    def __init__(self, audio, blocchi, log_):
        self.audio, self.resto, self.fermata, self.log = audio, blocchi, False, log_

    def finita(self):
        if self.resto <= 0:
            return True
        self.resto -= 1
        return False

    def ferma(self):
        self.fermata = True
        self.log.append(("ferma", self.audio, self.resto))


class FintiParlano(Finti):
    def __init__(self, risposte, durata=10):
        super().__init__()
        self.risposte, self.durata, self.eventi = list(risposte), durata, []

    def rilevatore(self, b):
        return {PAROLA: 1.0, QUASI: 0.6}.get(b if isinstance(b, str) else None, 0.0)

    def invia(self, wav):
        self.inviati.append(wav)
        return True, self.risposte.pop(0), ""

    def riproduci(self, audio):
        self.riprodotti.append(audio)
        return Suona(audio, self.durata, self.eventi)


def _frasi_chiuse(*frasi):
    chiuse = []

    def gen():
        try:
            for x in frasi:
                yield x
        finally:
            chiuse.append(True)
    return gen(), chiuse


RICHIESTA = ((VOCE, 10), (SILENZIO, 10))


def test_la_parola_interrompe_gas_e_apre_una_nuova_richiesta():
    frasi, chiuse = _frasi_chiuse(b"A", b"B")
    f = FintiParlano([frasi, b"C"])
    f.ascolto(_blocchi(PAROLA, *RICHIESTA, (SILENZIO, 3), PAROLA, *RICHIESTA, (SILENZIO, 20)),
              finestra_s=0).gira()
    # A fermata a metà, B scartata (risposta chiusa), nuova richiesta inviata e C suonata
    assert f.riprodotti == [b"A", b"C"] and chiuse == [True]
    assert f.eventi[0][:2] == ("ferma", b"A") and f.eventi[0][2] > 0
    assert len(f.inviati) == 2 and f.bip == ["ok", "ok"]


def test_la_voce_senza_parola_non_interrompe():
    """Il microfono sente la voce di Gas dalle casse: il volume da solo non interrompe."""
    frasi, chiuse = _frasi_chiuse(b"A", b"B")
    f = FintiParlano([frasi])
    f.ascolto(_blocchi(PAROLA, *RICHIESTA, (VOCE, 40)), finestra_s=0).gira()
    assert f.riprodotti == [b"A", b"B"] and len(f.inviati) == 1 and f.bip == ["ok"]
    assert all(r == 0 for _, _, r in f.eventi)  # finite da sole, non fermate a metà


def test_mentre_gas_parla_serve_la_soglia_piu_alta():
    f = FintiParlano([b"A"])
    f.ascolto(_blocchi(PAROLA, *RICHIESTA, (QUASI, 20)), finestra_s=0).gira()
    assert f.riprodotti == [b"A"] and len(f.inviati) == 1 and f.eventi[0][2] == 0


def test_interruzione_spenta():
    f = FintiParlano([b"A"])
    f.ascolto(_blocchi(PAROLA, *RICHIESTA, PAROLA, (SILENZIO, 20)), finestra_s=0,
              soglia_interruzione=None).gira()
    assert f.riprodotti == [b"A"] and len(f.inviati) == 1 and f.eventi[0][2] == 0


def test_rilevatore_rotto_mentre_gas_parla(caplog):
    """§9: un rilevatore che fallisce durante la risposta non la ferma; una riga sola."""
    f = FintiParlano([b"A"])
    rotto = [False]

    def rilevatore(b):
        if rotto[0]:
            raise RuntimeError("onnx")
        return f.rilevatore(b)
    asc = a.Ascolto(_blocchi(PAROLA, *RICHIESTA, (SILENZIO, 20)), rilevatore, f.invia,
                    lambda audio: (rotto.__setitem__(0, True), f.riproduci(audio))[1],
                    f.suona, finestra_s=0, dorme=lambda s: None)
    with caplog.at_level(logging.WARNING, logger="gas.ascolto"):
        asc.gira()
    assert f.riprodotti == [b"A"] and f.eventi[0][2] == 0
    assert caplog.text.count("rilevatore in errore mentre Gas parla") == 1


def test_frase_fermata_anche_se_il_microfono_finisce():
    f = FintiParlano([b"A"], durata=50)
    f.ascolto(_blocchi(PAROLA, *RICHIESTA, (SILENZIO, 3)), finestra_s=0).gira()
    assert f.eventi and f.eventi[0][0] == "ferma" and f.eventi[0][2] > 0


def test_le_interruzioni_restano_sotto_max_turni():
    """R-668-1: se la voce di Gas facesse scattare la parola, le interruzioni di fila non
    azzerano il tetto: al più max_turni richieste per conversazione."""
    f = FintiParlano([b"A", b"B", b"C", b"D"])
    giro = (*RICHIESTA, (SILENZIO, 2), PAROLA)
    # dopo la seconda interruzione si torna ad aspettare la parola: la voce che segue
    # (senza parola) non apre una terza richiesta
    f.ascolto(_blocchi(PAROLA, *giro, *giro, *RICHIESTA, (SILENZIO, 20)),
              finestra_s=0, max_turni=2).gira()
    assert len(f.inviati) == 2 and f.riprodotti == [b"A", b"B"]


def test_dopo_l_interruzione_il_bip_non_entra_nella_richiesta():
    """R-668-3: dopo il bip dell'interruzione il microfono si svuota (il bip non deve
    finire nella nuova richiesta): uno svuotamento in più di una risposta normale."""
    frasi, _ = _frasi_chiuse(b"A", b"B")
    f = FintiParlano([frasi, b"C"])
    svuotati_al_bip = []
    f.suona = lambda tipo: (f.bip.append(tipo), svuotati_al_bip.append(f.svuotati))
    f.ascolto(_blocchi(PAROLA, *RICHIESTA, (SILENZIO, 3), PAROLA, *RICHIESTA, (SILENZIO, 20)),
              finestra_s=0).gira()
    # bip della parola e bip dell'interruzione: dopo ciascuno uno svuotamento
    assert f.bip == ["ok", "ok"] and len(f.inviati) == 2
    prima_del_secondo = svuotati_al_bip[1]
    assert prima_del_secondo == 2  # bip iniziale + fine del turno interrotto
    assert f.svuotati == prima_del_secondo + 2  # svuota dopo il bip + fine del turno con C


class _Rotta:
    def __init__(self, rompe_finita, rompe_ferma):
        self.rompe_finita, self.rompe_ferma, self.fermata = rompe_finita, rompe_ferma, 0

    def finita(self):
        if self.rompe_finita:
            raise OSError("poll")
        return False

    def ferma(self):
        self.fermata += 1
        if self.rompe_ferma:
            raise OSError("terminate")


@pytest.mark.parametrize("rompe_finita,rompe_ferma", [(True, False), (False, True), (True, True)])
def test_riproduzione_rotta_non_esce_dal_turno(caplog, rompe_finita, rompe_ferma):
    """R-668-2: un errore di finita() o di ferma() resta dentro il turno (§9): la frase si
    ferma, si passa alla successiva e il turno finisce bene."""
    rotte = []

    def riproduci(audio):
        r = _Rotta(rompe_finita, rompe_ferma)
        rotte.append(r)
        return r
    frasi, chiuse = _frasi_chiuse(b"A", b"B")
    f = Finti(esito=(True, frasi, ""))
    asc = a.Ascolto(_blocchi((SILENZIO, 3)) if rompe_finita else iter([]), f.rilevatore,
                    f.invia, riproduci, f.suona, svuota=f.svuota)
    with caplog.at_level(logging.WARNING, logger="gas.ascolto"):
        assert asc.turno([VOCE] * 3) is True
    assert len(rotte) == 2 and all(r.fermata == 1 for r in rotte) and chiuse == [True]
    assert not asc.interrotto
    if rompe_finita:
        assert "riproduzione: stato illeggibile" in caplog.text
    if rompe_ferma:
        assert "arresto della riproduzione fallito" in caplog.text


# ── fetta 42: «Sì, signore?» al posto del bip ──

def test_dopo_la_parola_jarvis_dice_si_signore():
    f = FintiParlano([b"A"], durata=3)
    f.ascolto(_blocchi(PAROLA, (SILENZIO, 5), *RICHIESTA, (SILENZIO, 20)), finestra_s=0,
              conferma=lambda: b"SI-SIGNORE").gira()
    assert f.riprodotti == [b"SI-SIGNORE", b"A"] and f.bip == [] and len(f.inviati) == 1


@pytest.mark.parametrize("conferma", [lambda: None, lambda: b"", lambda: 1 / 0])
def test_senza_conferma_resta_il_bip(conferma):
    """Conferma non pronta, vuota o rotta (§9): il bip di sempre, e si va avanti."""
    f = FintiParlano([b"A"])
    f.ascolto(_blocchi(PAROLA, *RICHIESTA, (SILENZIO, 20)), finestra_s=0,
              conferma=conferma).gira()
    assert f.bip == ["ok"] and f.riprodotti == [b"A"] and len(f.inviati) == 1


def test_conferma_che_non_suona_diventa_bip():
    f = FintiParlano([b"A"])

    def riproduci(audio):
        if audio == b"SI":
            raise OSError("afplay")
        return f.riproduci(audio)
    a.Ascolto(_blocchi(PAROLA, *RICHIESTA, (SILENZIO, 20)), f.rilevatore, f.invia, riproduci,
              f.suona, finestra_s=0, conferma=lambda: b"SI").gira()
    assert f.bip == ["ok"] and f.riprodotti == [b"A"] and len(f.inviati) == 1


def test_la_conferma_non_si_interrompe_e_poi_si_svuota():
    """La parola ripetuta mentre Jarvis dice «Sì, signore?» non apre niente; il microfono
    si svuota dopo la conferma, che quindi non entra nella richiesta."""
    f = FintiParlano([b"A"], durata=5)
    svuotati_al_secondo_audio = []
    riproduci = f.riproduci

    def segna(audio):
        if audio == b"A":
            svuotati_al_secondo_audio.append(f.svuotati)
        return riproduci(audio)
    f.riproduci = segna
    f.ascolto(_blocchi(PAROLA, PAROLA, PAROLA, *RICHIESTA, (SILENZIO, 20)), finestra_s=0,
              conferma=lambda: b"SI").gira()
    assert f.riprodotti == [b"SI", b"A"] and f.eventi[0] == ("ferma", b"SI", 0)
    assert len(f.inviati) == 1 and svuotati_al_secondo_audio == [1]


def test_nella_finestra_e_all_interruzione_niente_conferma():
    """«Sì, signore?» solo alla prima attivazione con la parola: nella finestra dei 12 s
    non serve, e all'interruzione resta il bip (più rapido)."""
    chiamate = []

    def conferma():
        chiamate.append(1)
        return b"SI"
    frasi, _ = _frasi_chiuse(b"A", b"B")
    f = FintiParlano([frasi, b"C", b"D"], durata=3)
    f.ascolto(_blocchi(PAROLA, (SILENZIO, 3), *RICHIESTA, PAROLA, *RICHIESTA, (SILENZIO, 3),
                       *RICHIESTA, (SILENZIO, 20)), finestra_s=12, conferma=conferma).gira()
    assert chiamate == [1] and f.bip == ["ok"] and len(f.inviati) == 3
    assert f.riprodotti[0] == b"SI" and f.riprodotti.count(b"SI") == 1

@pytest.mark.parametrize("acceso,soglia,atteso", [
    (None, None, 0.7), ("1", "0.9", 0.9), ("0", "0.9", None), (None, "abc", 0.7),
    (None, "5", 1.0), (" 0 ", None, None),
])
def test_soglia_interruzione_dall_ambiente(monkeypatch, acceso, soglia, atteso):
    for k, v in (("GAS_ASCOLTO_INTERRUZIONE", acceso), ("GAS_ASCOLTO_SOGLIA_INTERRUZIONE", soglia)):
        if v is None:
            monkeypatch.delenv(k, raising=False)
        else:
            monkeypatch.setenv(k, v)
    assert a.soglia_interruzione() == atteso


# ── fetta 43 parte 2: finestra di 40 s e difese dei turni di seguito ──

class FintiSeguito(Finti):
    """Invio finto che distingue il turno dopo la parola da quello di seguito."""

    def __init__(self, esiti):
        super().__init__()
        self.esiti, self.tipi = list(esiti), []

    def _esito(self, tipo):
        self.tipi.append(tipo)
        return self.esiti.pop(0) if self.esiti else (True, b"MP3", "", "")

    def ascolto(self, blocchi, **k):
        return a.Ascolto(iter(blocchi), self.rilevatore,
                         lambda wav: (self.inviati.append(wav), self._esito("parola"))[1],
                         self.riproduci, self.suona, svuota=self.svuota,
                         azzera_rilevatore=self.azzera,
                         invia_seguito=lambda wav: (self.inviati.append(wav),
                                                    self._esito("seguito"))[1], **k)


SEGUITO = ((VOCE, 10), (SILENZIO, 10))   # una richiesta di seguito da 0,8 s di voce


def test_finestra_predefinita_40_secondi():
    assert a.FINESTRA_PREDEFINITA_S == 40.0 and a.SEGUITO_MAX_PREDEFINITO_S == 15.0
    f = FintiSeguito([])
    asc = f.ascolto(_blocchi(PAROLA, *RICHIESTA, (SILENZIO, _sec(30)), *SEGUITO,
                             (SILENZIO, _sec(45))))
    asc.gira()
    assert asc.finestra_s == 40.0 and f.tipi == ["parola", "seguito"]


def test_il_turno_di_seguito_usa_l_invio_di_seguito():
    f = FintiSeguito([])
    f.ascolto(_blocchi(PAROLA, *RICHIESTA, *SEGUITO, *SEGUITO, (SILENZIO, _sec(50)))).gira()
    assert f.tipi == ["parola", "seguito", "seguito"] and f.bip == ["ok"]


def test_comando_fine_chiude_la_conversazione_senza_bip(caplog):
    f = FintiSeguito([(True, b"A", "", ""), (True, None, "", "fine")])
    with caplog.at_level(logging.INFO, logger="gas.ascolto"):
        f.ascolto(_blocchi(PAROLA, *RICHIESTA, *SEGUITO, *SEGUITO,
                           (SILENZIO, _sec(50)))).gira()
    assert f.tipi == ["parola", "seguito"] and f.riprodotti == [b"A"] and f.bip == ["ok"]
    # chiusa per il comando del server, non come un errore
    assert "non rivolto a Gas" in caplog.text and "non riuscito" not in caplog.text


def test_comando_pausa_suona_va_bene_e_chiude():
    f = FintiSeguito([(True, b"A", "", ""), (True, b"VA-BENE", "", "pausa")])
    f.ascolto(_blocchi(PAROLA, *RICHIESTA, *SEGUITO, *SEGUITO, (SILENZIO, _sec(50)))).gira()
    assert f.tipi == ["parola", "seguito"] and f.riprodotti == [b"A", b"VA-BENE"]
    assert f.bip == ["ok"]


def test_pausa_dopo_la_parola_chiude_anche_senza_audio():
    """«Hey Jarvis, pausa» oltre il tetto orario: 429 col comando, o niente audio: si chiude
    in silenzio, come una pausa riuscita."""
    f = FintiSeguito([(False, None, "HTTP 429", "pausa")])
    f.ascolto(_blocchi(PAROLA, *RICHIESTA, *SEGUITO, (SILENZIO, _sec(50)))).gira()
    assert f.tipi == ["parola"] and f.bip == ["ok"]


@pytest.mark.parametrize("esito", [(False, None, "HTTP 500", ""), (False, None, "HTTP 429"),
                                   (True, iter([]), "", "")])
def test_errore_di_seguito_chiude_senza_bip(esito):
    """R-675-5-M2: col cervello forte spento i turni di seguito ricevono 500. Qualsiasi errore
    (o risposta senza voce) chiude la conversazione, mai bip a ripetizione."""
    f = FintiSeguito([(True, b"A", "", ""), esito])
    f.ascolto(_blocchi(PAROLA, *RICHIESTA, *SEGUITO, *SEGUITO, (SILENZIO, _sec(50)))).gira()
    assert f.tipi == ["parola", "seguito"] and f.bip == ["ok"]


def test_errore_dopo_la_parola_fa_ancora_il_bip():
    f = FintiSeguito([(False, None, "HTTP 500", "")])
    f.ascolto(_blocchi(PAROLA, *RICHIESTA, (SILENZIO, _sec(50)))).gira()
    assert f.bip == ["ok", "errore"]


def test_parlato_lungo_senza_parola_non_si_invia():
    """(a)+(b): una richiesta di seguito che arriva a 15 s è parlato della stanza: non va al
    server e la conversazione si chiude."""
    f = FintiSeguito([])
    f.ascolto(_blocchi(PAROLA, *RICHIESTA, (VOCE, _sec(20)), (SILENZIO, 10), *SEGUITO,
                       (SILENZIO, _sec(50)))).gira()
    assert f.tipi == ["parola"] and len(f.inviati) == 1


def test_il_parlato_lungo_si_smette_di_registrare_a_15_s():
    """La registrazione di seguito si ferma al tetto (non va avanti fino a 30 s): dopo,
    il microfono torna subito al rilevatore della parola."""
    visti = []
    f = FintiSeguito([])

    def rilevatore(b):
        visti.append(b is VOCE)
        return f.rilevatore(b)
    asc = a.Ascolto(_blocchi(PAROLA, *RICHIESTA, (VOCE, _sec(25)), (SILENZIO, 20)), rilevatore,
                    lambda wav: (f.inviati.append(wav), (True, b"MP3", "", ""))[1],
                    f.riproduci, f.suona, svuota=f.svuota)
    asc.gira()
    assert len(f.inviati) == 1
    assert sum(visti) >= _sec(25) - _sec(a.SEGUITO_MAX_PREDEFINITO_S) - 2


def test_parlato_di_seguito_sotto_il_tetto_si_invia():
    f = FintiSeguito([])
    f.ascolto(_blocchi(PAROLA, *RICHIESTA, (VOCE, _sec(14)), (SILENZIO, 10),
                       (SILENZIO, _sec(50)))).gira()
    assert f.tipi == ["parola", "seguito"]


def test_dopo_la_parola_la_richiesta_lunga_va_ancora_fino_a_30_s():
    f = FintiSeguito([])
    f.ascolto(_blocchi(PAROLA, (VOCE, _sec(20)), (SILENZIO, 10), (SILENZIO, _sec(50)))).gira()
    assert f.tipi == ["parola"] and _campioni(f.inviati[0]) == (_sec(20) + 10) * a.BLOCCO


def test_interrotto_un_turno_di_seguito_il_successivo_non_lo_e():
    frasi, _ = _frasi_chiuse(b"B", b"C")
    f = FintiSeguito([(True, b"A", "", ""), (True, frasi, "", "")])
    f.riproduci = lambda audio: (f.riprodotti.append(audio), Suona(audio, 3, []))[1]
    f.ascolto(_blocchi(PAROLA, *RICHIESTA, *SEGUITO, PAROLA, *RICHIESTA,
                       (SILENZIO, _sec(50)))).gira()
    assert f.tipi == ["parola", "seguito", "parola"]


PAROLA_DETTA = [2100] * a.BLOCCO     # «Hey Jarvis» detto: è voce e il rilevatore la sente


def _finti_con_parola_detta(esiti=()):
    f = FintiSeguito(list(esiti))
    f.rilevatore = lambda b: 1.0 if (b is PAROLA_DETTA or b == PAROLA) else 0.0
    return f


def test_parola_nella_finestra_e_una_richiesta_normale():
    """V-1 bot #341: «Hey Jarvis, …» detto nella finestra non è un turno di seguito: va con
    l'invio normale (gli strumenti, niente «ripetimelo»)."""
    f = _finti_con_parola_detta()
    f.ascolto(_blocchi(PAROLA, *RICHIESTA, (SILENZIO, 5), PAROLA_DETTA, *SEGUITO,
                       (SILENZIO, _sec(50)))).gira()
    assert f.tipi == ["parola", "parola"]


def test_parola_a_meta_della_frase_nella_finestra():
    """Il rilevatore resta acceso anche mentre si registra: la parola sentita dopo l'inizio
    della voce rende normale il turno e alza il tetto a 30 s (si invia anche oltre i 15 s)."""
    f = _finti_con_parola_detta()
    f.ascolto(_blocchi(PAROLA, *RICHIESTA, (VOCE, 5), PAROLA_DETTA, (VOCE, _sec(18)),
                       (SILENZIO, 10), (SILENZIO, _sec(50)))).gira()
    assert f.tipi == ["parola", "parola"]
    assert _campioni(f.inviati[1]) > _sec(15) * a.BLOCCO


def test_dopo_la_parola_nella_finestra_il_turno_dopo_torna_di_seguito():
    f = _finti_con_parola_detta()
    f.ascolto(_blocchi(PAROLA, *RICHIESTA, PAROLA_DETTA, *SEGUITO, *SEGUITO,
                       (SILENZIO, _sec(50)))).gira()
    assert f.tipi == ["parola", "parola", "seguito"]


def test_rilevatore_azzerato_prima_della_finestra():
    """R-680-1: dopo la risposta (il rilevatore ha sentito la voce di Gas) si azzera prima
    della finestra: un residuo fra 0,5 e 0,7 non deve rendere «normale» il turno di seguito."""
    f = FintiSeguito([])
    residuo = [0.0]

    def rilevatore(b):
        if b == PAROLA:
            return 1.0
        return residuo[0]

    def azzera():
        f.azzerati += 1
        residuo[0] = 0.0

    def riproduci(audio):
        f.riprodotti.append(audio)
        residuo[0] = 0.6   # la voce di Gas lascia un punteggio sotto 0,7 ma sopra 0,5
        return None
    a.Ascolto(_blocchi(PAROLA, *RICHIESTA, *SEGUITO, (SILENZIO, _sec(50))), rilevatore,
              lambda wav: (f.inviati.append(wav), f._esito("parola"))[1], riproduci, f.suona,
              svuota=f.svuota, azzera_rilevatore=azzera,
              invia_seguito=lambda wav: (f.inviati.append(wav), f._esito("seguito"))[1]).gira()
    assert f.tipi == ["parola", "seguito"]


def test_senza_parola_la_frase_lunga_resta_scartata():
    f = _finti_con_parola_detta()
    f.ascolto(_blocchi(PAROLA, *RICHIESTA, (VOCE, 5), (VOCE, _sec(18)),
                       (SILENZIO, 10), (SILENZIO, _sec(50)))).gira()
    assert f.tipi == ["parola"]


def test_rilevatore_rotto_nella_finestra_non_ferma_niente():
    f = FintiSeguito([])
    rotto = [False]

    def rilevatore(b):
        if rotto[0]:
            raise RuntimeError("onnx")
        return f.rilevatore(b)
    asc = a.Ascolto(_blocchi(PAROLA, *RICHIESTA, *SEGUITO, (SILENZIO, _sec(50))), rilevatore,
                    lambda wav: (f.inviati.append(wav), f._esito("parola"))[1],
                    lambda audio: (rotto.__setitem__(0, True), f.riproduci(audio))[1],
                    f.suona, svuota=f.svuota, dorme=lambda s: None,
                    invia_seguito=lambda wav: (f.inviati.append(wav), f._esito("seguito"))[1])
    asc.gira()
    assert f.tipi == ["parola", "seguito"]


def test_dopo_l_interruzione_il_turno_non_e_di_seguito():
    frasi, _ = _frasi_chiuse(b"A", b"B")
    f = FintiSeguito([(True, frasi, "", "")])
    f.riproduci = lambda audio: (f.riprodotti.append(audio), Suona(audio, 3, []))[1]
    f.ascolto(_blocchi(PAROLA, *RICHIESTA, PAROLA, *RICHIESTA, *SEGUITO,
                       (SILENZIO, _sec(50)))).gira()
    assert f.tipi == ["parola", "parola", "seguito"]

# ── finestra di 12 s dopo la risposta ──

def test_finestra_continua_senza_parola():
    f = Finti()
    f.ascolto(_blocchi(PAROLA, (VOCE, 10), (SILENZIO, 10),
                       (SILENZIO, _sec(5)), (VOCE, 10), (SILENZIO, 10),
                       (SILENZIO, _sec(20))), finestra_s=12).gira()
    assert len(f.inviati) == 2 and f.bip == ["ok"]
    assert _campioni(f.inviati[1]) == (10 + 10) * a.BLOCCO


def test_finestra_scaduta_torna_alla_parola():
    f = Finti()
    f.ascolto(_blocchi(PAROLA, (VOCE, 10), (SILENZIO, 10),
                       (SILENZIO, _sec(13)), (VOCE, 10), (SILENZIO, 10)),
              finestra_s=12).gira()
    assert len(f.inviati) == 1  # la voce dopo 13 s senza parola non parte


def test_voce_breve_nella_finestra_non_apre_un_turno():
    """Un colpo di tosse (un blocco) non è una richiesta."""
    f = Finti()
    f.ascolto(_blocchi(PAROLA, (VOCE, 10), (SILENZIO, 10),
                       VOCE, (SILENZIO, _sec(13))), finestra_s=12).gira()
    assert len(f.inviati) == 1


def test_massimo_dei_turni_di_fila():
    f = Finti()
    turno = [(VOCE, 10), (SILENZIO, 10), (SILENZIO, 5)]
    f.ascolto(_blocchi(PAROLA, *(turno * 5)), finestra_s=12, max_turni=2).gira()
    assert len(f.inviati) == 2


def test_dopo_la_finestra_la_parola_riattiva():
    f = Finti()
    f.ascolto(_blocchi(PAROLA, (VOCE, 10), (SILENZIO, 10), (SILENZIO, _sec(13)),
                       PAROLA, (VOCE, 10), (SILENZIO, 10)), finestra_s=12).gira()
    assert len(f.inviati) == 2 and f.bip == ["ok", "ok"]


# ── fail-safe ──

def test_invio_fallito_bip_di_errore_e_niente_finestra():
    f = Finti(esito=(False, None, "HTTP 503"))
    f.ascolto(_blocchi(PAROLA, (VOCE, 10), (SILENZIO, 10), (VOCE, 10), (SILENZIO, 10)),
              finestra_s=12).gira()
    assert f.bip == ["ok", "errore"] and f.riprodotti == [] and len(f.inviati) == 1
    assert f.svuotati == 2  # dopo il bip iniziale e dopo il bip di errore (V-3 bot #323)


def test_eccezioni_delle_parti_non_fermano_l_ascolto():
    class Rotti(Finti):
        def __init__(self):
            super().__init__()
            self.chiamate = 0

        def rilevatore(self, b):
            self.chiamate += 1
            if self.chiamate == 1:
                raise RuntimeError("modello")
            return super().rilevatore(b)

        def invia(self, wav):
            self.inviati.append(wav)
            raise OSError("rete")

        def suona(self, tipo):
            self.bip.append(tipo)
            raise OSError("afplay")

    f = Rotti()
    f.ascolto(_blocchi(SILENZIO, PAROLA, (VOCE, 5), (SILENZIO, 10),
                       PAROLA, (VOCE, 5), (SILENZIO, 10))).gira()
    assert len(f.inviati) == 2 and f.bip == ["ok", "errore", "ok", "errore"]


def test_rilevatore_sempre_in_errore_log_limitato_e_pausa_crescente(caplog):
    """V-1 ve #323: un rilevatore rotto non scrive una riga per blocco e non gira a vuoto:
    log al 1°, 2°, 4°, 8°… errore, pausa crescente fino a 60 s, microfono svuotato."""
    pause = []

    class Rotto(Finti):
        def rilevatore(self, b):
            raise RuntimeError("modello")

    f = Rotto()
    with caplog.at_level(logging.WARNING, logger="gas.ascolto"):
        a.Ascolto(iter(_blocchi((SILENZIO, 1000))), f.rilevatore, f.invia, f.riproduci,
                  f.suona, svuota=f.svuota, dorme=pause.append).gira()
    righe = [r for r in caplog.records if "rilevatore: errore" in r.getMessage()]
    assert len(righe) == 10  # 1, 2, 4, …, 512
    assert pause[:4] == [0.5, 1.0, 2.0, 4.0] and max(pause) == a.PAUSA_ERRORI_MAX_S
    assert len(pause) == 998 and f.svuotati == 998 and f.inviati == []


def test_rilevatore_in_errore_per_giorni_resta_a_60_secondi(caplog):
    """R-624-1: oltre i 1027 errori di fila `2 ** (n - 3)` non entra in un float: la
    pausa deve restare 60 s e il log logaritmico, senza «pausa fallita» a ogni blocco."""
    pause = []

    def rotto(b):
        raise RuntimeError("modello")

    f = Finti()
    with caplog.at_level(logging.WARNING, logger="gas.ascolto"):
        a.Ascolto(iter(_blocchi((SILENZIO, 1200))), rotto, f.invia, f.riproduci, f.suona,
                  svuota=f.svuota, dorme=pause.append).gira()
    testo = [r.getMessage() for r in caplog.records]
    assert not any("pausa del rilevatore fallita" in t for t in testo)
    assert len(pause) == 1198 and pause[-1] == a.PAUSA_ERRORI_MAX_S
    assert sum("rilevatore: errore" in t for t in testo) == 11  # 1, 2, 4, …, 1024


def test_rilevatore_che_torna_azzera_il_conto(caplog):
    class Ballerino(Finti):
        def __init__(self):
            super().__init__()
            self.n = 0

        def rilevatore(self, b):
            self.n += 1
            if self.n <= 5:
                raise RuntimeError("x")
            return super().rilevatore(b)

    f = Ballerino()
    pause = []
    with caplog.at_level(logging.WARNING, logger="gas.ascolto"):
        a.Ascolto(iter(_blocchi((SILENZIO, 5), (SILENZIO, a.BUONI_PER_AZZERARE), PAROLA,
                                (VOCE, 5), (SILENZIO, 10))),
                  f.rilevatore, f.invia, f.riproduci, f.suona, svuota=f.svuota,
                  dorme=pause.append, finestra_s=0).gira()
    righe = [r.getMessage() for r in caplog.records]
    assert sum("di nuovo a posto" in t for t in righe) == 1  # R-624-2: una volta sola
    assert "di nuovo a posto dopo 5 errori" in " ".join(righe) and len(f.inviati) == 1
    assert pause == [0.5, 1.0, 2.0]


def _pause_con(sequenza):
    errori = iter(sequenza)
    pause = []

    def ballerino(b):
        if next(errori, False):
            raise RuntimeError("x")
        return 0.0

    f = Finti()
    a.Ascolto(iter(_blocchi((SILENZIO, len(sequenza) + 5))), ballerino, f.invia, f.riproduci,
              f.suona, svuota=f.svuota, dorme=pause.append).gira()
    return pause


def test_dopo_il_ritorno_le_pause_ripartono_da_mezzo_secondo():
    """R-624-2: il conto si azzera davvero quando il rilevatore torna (per 10 s di fila)."""
    buoni = [False] * a.BUONI_PER_AZZERARE
    assert _pause_con([True] * 4 + buoni + [True] * 4) == [0.5, 1.0, 0.5, 1.0]


def test_pochi_blocchi_buoni_non_azzerano_il_conto():
    """V-1 ve #328: qualche blocco buono in mezzo agli errori non riazzera il conto."""
    pochi = [False] * (a.BUONI_PER_AZZERARE - 1)
    assert _pause_con([True] * 4 + pochi + [True] * 4) == [0.5, 1.0, 2.0, 4.0, 8.0, 16.0]


def test_rilevatore_a_intermittenza_log_limitato(caplog):
    """V-1 ve #328: errore e blocco buono alternati per 2000 blocchi: poche righe di log
    (non una o due per blocco) e le pause arrivano lo stesso."""
    with caplog.at_level(logging.WARNING, logger="gas.ascolto"):
        pause = _pause_con([True, False] * 1000)
    righe = [r.getMessage() for r in caplog.records if r.getMessage().startswith("rilevatore")]
    assert len(righe) == 10  # 1, 2, 4, …, 512 errori; mai «di nuovo a posto»
    assert len(pause) == 998 and max(pause) == a.PAUSA_ERRORI_MAX_S


def test_avviso_se_il_microfono_e_muto(caplog):
    f = Finti()
    with caplog.at_level(logging.WARNING, logger="gas.ascolto"):
        f.ascolto(_blocchi(([0] * a.BLOCCO, _sec(25)))).gira()
    avvisi = [r for r in caplog.records if "silenzio assoluto" in r.getMessage()]
    assert len(avvisi) == 1


def test_log_senza_audio_ne_token(caplog):
    f = Finti(esito=(False, None, "HTTP 401"))
    with caplog.at_level(logging.DEBUG, logger="gas.ascolto"):
        f.ascolto(_blocchi(PAROLA, (VOCE, 5), (SILENZIO, 10))).gira()
    testo = " ".join(r.getMessage() for r in caplog.records)
    assert TOKEN not in testo and "RIFF" not in testo and "2000" not in testo


# ── parti vere: invio, riproduzione, configurazione ──

class _Server(http.server.BaseHTTPRequestHandler):
    risposta = (200, "audio/mpeg", b"ID3-MP3")
    visti = []

    def do_POST(self):
        n = int(self.headers.get("Content-Length", 0))
        type(self).visti.append((self.path, dict(self.headers), self.rfile.read(n)))
        codice, tipo, corpo = type(self).risposta
        self.send_response(codice)
        if codice == 302:
            self.send_header("Location", f"http://{self.headers['Host']}/rubato")
        self.send_header("Content-Type", tipo)
        self.send_header("Content-Length", str(len(corpo)))
        self.end_headers()
        self.wfile.write(corpo)

    def do_GET(self):  # dove porterebbe il redirect: risponde audio, come un server vero
        type(self).visti.append((self.path, dict(self.headers), b""))
        self.send_response(200)
        self.send_header("Content-Type", "audio/mpeg")
        self.send_header("Content-Length", "3")
        self.end_headers()
        self.wfile.write(b"ID3")

    def log_message(self, *x):
        pass


@pytest.fixture
def server():
    _Server.visti = []
    s = http.server.HTTPServer(("127.0.0.1", 0), _Server)
    t = threading.Thread(target=s.serve_forever, daemon=True)
    t.start()
    yield f"http://127.0.0.1:{s.server_address[1]}"
    s.shutdown()
    s.server_close()


def test_invio_al_server_vero(server):
    _Server.risposta = (200, "audio/mpeg", b"ID3-MP3")
    ok, audio, motivo, _ = a.invia_al_server(server, TOKEN, 5)(b"RIFF-WAV")
    assert (ok, audio, motivo) == (True, b"ID3-MP3", "")
    percorso, intestazioni, corpo = _Server.visti[0]
    assert percorso == "/voice" and corpo == b"RIFF-WAV"
    assert intestazioni["Authorization"] == f"Bearer {TOKEN}"
    assert intestazioni["Content-Type"] == "audio/wav" and intestazioni["Accept"] == "audio/mpeg"


@pytest.mark.parametrize("risposta,atteso", [
    ((401, "application/json", b'{"error": "Unauthorized"}'), "HTTP 401"),
    ((429, "application/json", b'{"error": "troppe"}'), "HTTP 429"),
    ((200, "application/json", b'{"content": "testo"}'), "risposta inattesa"),
])
def test_invio_con_risposte_sbagliate(server, risposta, atteso):
    _Server.risposta = risposta
    ok, audio, motivo, _ = a.invia_al_server(server, TOKEN, 5)(b"x")
    assert not ok and audio is None and atteso in motivo and TOKEN not in motivo


def test_redirect_non_seguito(server):
    """R-615-2: un 302 verso un altro host non si segue (il Bearer non esce)."""
    _Server.risposta = (302, "text/plain", b"")
    ok, audio, motivo, _ = a.invia_al_server(server, TOKEN, 5)(b"x")
    assert not ok and "HTTP 302" in motivo and len(_Server.visti) == 1


def test_proxy_di_sistema_ignorato(monkeypatch):
    """R-615-2: su macOS i proxy di sistema valgono anche per 127.0.0.1. L'opener si
    costruisce all'import: lo si ricostruisce con un proxy nell'ambiente e non deve
    esserci nessun gestore di proxy attivo."""
    import importlib
    import urllib.request
    monkeypatch.setenv("http_proxy", "http://127.0.0.1:9")
    monkeypatch.setenv("https_proxy", "http://127.0.0.1:9")
    try:
        importlib.reload(a)
        attivi = [h for h in a._OPENER.handlers
                  if isinstance(h, urllib.request.ProxyHandler) and h.proxies]
    finally:
        monkeypatch.undo()
        importlib.reload(a)
    assert attivi == []


def test_server_giu():
    ok, audio, motivo, _ = a.invia_al_server("http://127.0.0.1:9", TOKEN, 2)(b"x")
    assert not ok and "non raggiungibile" in motivo and TOKEN not in motivo


# ── fetta 39: risposta a pezzi (NDJSON della V7b), la prima frase suona subito ──

import base64 as _b64  # noqa: E402


def _riga(**campi):
    return (json.dumps(campi) + "\n").encode()


def _mp3(n):
    return _b64.b64encode(f"MP3-{n}".encode()).decode()


class _ServerPezzi(http.server.BaseHTTPRequestHandler):
    """Server voce finto a pezzi: manda la prima riga, poi aspetta che il client l'abbia
    SUONATA (evento) prima di mandare le altre. Se il client leggesse tutto prima di
    suonare, resterebbe fermo fino al timeout dell'evento."""
    protocol_version = "HTTP/1.0"
    righe = []
    suonata = threading.Event()
    atteso = []
    visti = []

    def do_POST(self):
        n = int(self.headers.get("Content-Length", 0))
        type(self).visti.append((dict(self.headers), self.rfile.read(n)))
        self.send_response(200)
        self.send_header("Content-Type", "application/x-ndjson; charset=utf-8")
        self.end_headers()
        for i, r in enumerate(type(self).righe):
            try:
                self.wfile.write(r)
                self.wfile.flush()
            except OSError:
                return
            if i == 0:
                type(self).atteso.append(type(self).suonata.wait(5))

    def log_message(self, *x):
        pass


@pytest.fixture
def server_pezzi():
    _ServerPezzi.visti, _ServerPezzi.atteso = [], []
    _ServerPezzi.suonata = threading.Event()
    s = http.server.HTTPServer(("127.0.0.1", 0), _ServerPezzi)
    th = threading.Thread(target=s.serve_forever, daemon=True)
    th.start()
    yield f"http://127.0.0.1:{s.server_address[1]}"
    s.shutdown()
    s.server_close()


def _turno_vero(url, **k):
    suonati, bip = [], []

    def riproduci(audio):
        suonati.append(audio)
        _ServerPezzi.suonata.set()

    asc = a.Ascolto(iter([]), lambda b: 0.0, a.invia_al_server(url, TOKEN, 5, **k), riproduci,
                    bip.append)
    ok = asc.turno([VOCE] * 3)
    return ok, suonati, bip


def test_pezzi_la_prima_frase_suona_prima_delle_altre(server_pezzi):
    _ServerPezzi.righe = [_riga(content="Ciao. Tutto bene. Ecco.", pezzi=3, audio=_mp3(1)),
                          _riga(audio=_mp3(2)), _riga(audio=_mp3(3)), _riga(fine=True)]
    ok, suonati, bip = _turno_vero(server_pezzi)
    assert ok and suonati == [b"MP3-1", b"MP3-2", b"MP3-3"] and bip == []
    assert _ServerPezzi.atteso == [True]  # la prima è stata suonata mentre il server aspettava
    intestazioni, corpo = _ServerPezzi.visti[0]
    assert intestazioni["X-Gas-Formato"] == a.FORMATO_PEZZI
    assert intestazioni["Accept"] == "audio/mpeg" and corpo.startswith(b"RIFF")


def test_pezzi_errore_voce_a_meta(server_pezzi):
    _ServerPezzi.righe = [_riga(content="x", pezzi=3, audio=_mp3(1)),
                          _riga(errore_voce="Errore TTS ElevenLabs: quota"), _riga(audio=_mp3(3))]
    ok, suonati, bip = _turno_vero(server_pezzi)
    assert ok and suonati == [b"MP3-1"] and bip == []


def test_pezzi_senza_voce_nella_prima_riga(server_pezzi):
    _ServerPezzi.righe = [_riga(content="x", pezzi=2, errore_voce="TTS giù")]
    ok, suonati, bip = _turno_vero(server_pezzi)
    assert not ok and suonati == [] and bip == ["errore"]


@pytest.mark.parametrize("rotta", [b"{non json\n", b'["lista"]\n', _riga(audio="%%%non-base64")])
def test_pezzi_riga_rotta_dopo_la_prima(server_pezzi, rotta, caplog):
    _ServerPezzi.righe = [_riga(content="x", pezzi=3, audio=_mp3(1)), rotta, _riga(audio=_mp3(3))]
    with caplog.at_level(logging.WARNING, logger="gas.ascolto"):
        ok, suonati, bip = _turno_vero(server_pezzi)
    assert ok and suonati == [b"MP3-1"] and bip == []
    assert "risposta interrotta" in caplog.text and TOKEN not in caplog.text


def test_pezzi_riga_troppo_lunga(server_pezzi, monkeypatch):
    monkeypatch.setattr(a, "RIGA_MAX", 64)
    _ServerPezzi.righe = [_riga(content="x", pezzi=2, audio=_mp3(1)),
                          _riga(audio=_b64.b64encode(b"Z" * 200).decode())]
    ok, suonati, bip = _turno_vero(server_pezzi)
    assert ok and suonati == [b"MP3-1"]


def test_pezzi_connessione_chiusa_senza_fine(server_pezzi):
    _ServerPezzi.righe = [_riga(content="x", pezzi=3, audio=_mp3(1)), _riga(audio=_mp3(2))]
    ok, suonati, bip = _turno_vero(server_pezzi)
    assert ok and suonati == [b"MP3-1", b"MP3-2"]



class _ServerConferma(http.server.BaseHTTPRequestHandler):
    risposta = (200, "audio/mpeg", b"ID3-SI")   # o "chiudi" / "dormi"
    visti = []

    def do_GET(self):
        type(self).visti.append((self.path, dict(self.headers)))
        r = type(self).risposta
        if r == "chiudi":   # R-669-1 di M2: in certi errori il server chiude e basta
            self.close_connection = True
            self.wfile.flush()
            self.connection.shutdown(2)
            return
        if r == "dormi":
            time.sleep(2)
            return
        codice, tipo, corpo = r
        self.send_response(codice)
        if codice == 302:
            self.send_header("Location", f"http://{self.headers['Host']}/rubato")
        self.send_header("Content-Type", tipo)
        self.send_header("Content-Length", str(len(corpo)))
        self.end_headers()
        self.wfile.write(corpo)

    def log_message(self, *x):
        pass


@pytest.fixture
def server_conferma():
    _ServerConferma.visti = []
    s = http.server.ThreadingHTTPServer(("127.0.0.1", 0), _ServerConferma)
    t = threading.Thread(target=s.serve_forever, daemon=True)
    t.start()
    yield f"http://127.0.0.1:{s.server_address[1]}"
    s.shutdown()
    s.server_close()


def test_conferma_scaricata(server_conferma, caplog):
    _ServerConferma.risposta = (200, "audio/mpeg", b"ID3-SI")
    with caplog.at_level(logging.WARNING, logger="gas.ascolto"):
        assert a.scarica_conferma(server_conferma, TOKEN) == b"ID3-SI"
    percorso, intestazioni = _ServerConferma.visti[0]
    assert percorso == "/voce/conferma" and intestazioni["Authorization"] == f"Bearer {TOKEN}"
    assert TOKEN not in caplog.text


@pytest.mark.parametrize("risposta", [
    (503, "application/json", b'{"error": "TTS non disponibile"}'),
    (502, "application/json", b'{"error": "Errore TTS"}'),
    (401, "application/json", b'{"error": "no"}'),
    (200, "application/json", b'{"audio": "x"}'),
    (200, "audio/mpeg", b""),
    (302, "text/plain", b""),
    "chiudi",
])
def test_conferma_qualsiasi_errore_da_none(server_conferma, risposta, caplog):
    """Su QUALSIASI errore (codici HTTP, tipo sbagliato, vuoto, redirect, connessione
    chiusa dal server) niente eccezioni: None, e l'ascolto userà il bip."""
    _ServerConferma.risposta = risposta
    with caplog.at_level(logging.WARNING, logger="gas.ascolto"):
        assert a.scarica_conferma(server_conferma, TOKEN) is None
    assert [p for p, _ in _ServerConferma.visti] == ["/voce/conferma"]  # niente redirect
    assert TOKEN not in caplog.text



@pytest.fixture
def server_voce_vero(monkeypatch):
    """Il VoiceHandler vero di M2 (GET /voce/conferma, PR #335) con la sintesi finta:
    il contratto si prova dai due lati, non solo col server finto (R-634-3)."""
    from modules.voice.server import VoiceHandler

    class _H(VoiceHandler):
        pass
    _H.kernel = None
    _H.token = TOKEN
    _H.conferma_cache = None
    s = http.server.HTTPServer(("127.0.0.1", 0), _H)
    t = threading.Thread(target=s.serve_forever, daemon=True)
    t.start()
    yield f"http://127.0.0.1:{s.server_address[1]}"
    s.shutdown()
    s.server_close()


def test_conferma_col_server_voce_vero(server_voce_vero, monkeypatch):
    from modules.voice import server as srv
    monkeypatch.setenv("ELEVENLABS_API_KEY", "k")
    monkeypatch.setenv("ELEVENLABS_VOICE_ID", "Brian000000000001")
    # **kw: dalla V15 (chat M2) la conferma passa anche timeout= (autorizzato da M1)
    monkeypatch.setattr(srv, "synthesize_speech", lambda frase, k, voce, **kw: b"ID3-" + frase.encode())
    assert a.scarica_conferma(server_voce_vero, TOKEN) == "ID3-Sì, signore?".encode()
    assert a.scarica_conferma(server_voce_vero, "token-sbagliato") is None   # 401


@pytest.mark.parametrize("caso", ["senza_chiave", "errore_tts", "audio_vuoto"])
def test_conferma_col_server_voce_vero_in_errore(server_voce_vero, monkeypatch, caso):
    from modules.voice import server as srv
    from modules.voice.tts import ElevenLabsTTSError
    monkeypatch.setenv("ELEVENLABS_API_KEY", "" if caso == "senza_chiave" else "k")

    def tts(frase, k, voce, **kw):  # **kw: timeout= della conferma V15 (chat M2)
        if caso == "errore_tts":
            raise ElevenLabsTTSError(429, "quota")
        return b""
    monkeypatch.setattr(srv, "synthesize_speech", tts)
    assert a.scarica_conferma(server_voce_vero, TOKEN) is None

def test_conferma_troppo_grande(server_conferma, monkeypatch):
    monkeypatch.setattr(a, "CONFERMA_MAX_BYTE", 8)
    _ServerConferma.risposta = (200, "audio/mpeg", b"Z" * 20)
    assert a.scarica_conferma(server_conferma, TOKEN) is None


def test_conferma_timeout(server_conferma):
    _ServerConferma.risposta = "dormi"
    assert a.scarica_conferma(server_conferma, TOKEN, timeout=0.3) is None


def test_conferma_server_spento():
    assert a.scarica_conferma("http://127.0.0.1:9", TOKEN, timeout=1) is None


def test_conferma_in_memoria_e_riprova_al_massimo_al_minuto():
    ora = [0.0]
    esiti = [None, b"SI"]
    chiamate = []

    def scarica():
        chiamate.append(ora[0])
        return esiti.pop(0)
    c = a.Conferma(scarica, adesso=lambda: ora[0], in_sottofondo=False)
    assert chiamate == [0.0] and c() is None          # all'avvio fallisce
    ora[0] = 30.0
    assert c() is None and chiamate == [0.0]          # meno di un minuto: non riprova
    ora[0] = a.CONFERMA_RIPROVA_S + 1
    assert c() is None and len(chiamate) == 2         # riprova (in sottofondo nel vero)
    assert c() == b"SI" and c() == b"SI" and len(chiamate) == 2   # poi resta in memoria



def test_conferma_thread_che_non_parte(monkeypatch):
    """R-671-5: se il thread non parte, niente eccezioni e niente blocco: si riprova dopo
    un minuto (la conferma non resta «in corso» per sempre)."""
    ora = [0.0]
    partenze = []

    class ThreadRotto:
        def __init__(self, **k):
            partenze.append(k)

        def start(self):
            raise RuntimeError("can't start new thread")
    monkeypatch.setattr(a.threading, "Thread", ThreadRotto)
    c = a.Conferma(lambda: b"SI", adesso=lambda: ora[0])
    assert c() is None and len(partenze) == 1
    ora[0] = a.CONFERMA_RIPROVA_S + 1
    assert c() is None and len(partenze) == 2


def test_main_con_conferma_che_non_parte(monkeypatch, tmp_path):
    """R-671-5: un errore nel creare la conferma non ferma main: resta il bip."""
    def rotta(scarica):
        raise RuntimeError("x")
    k = _main_finto(monkeypatch, tmp_path, {}, conferma_cls=rotta)
    conferma = k.get("conferma")
    assert conferma is not None and conferma() is None


def test_conferma_tetto_piccolo():
    """R-671-3: «Sì, signore?» non supera qualche secondo di MP3."""
    assert a.CONFERMA_MAX_BYTE <= 200 * 1024

def test_conferma_scarica_che_esplode():
    def esplode():
        raise RuntimeError("x")
    c = a.Conferma(esplode, in_sottofondo=False)
    assert c() is None


def test_conferma_in_sottofondo_non_blocca():
    pronto = threading.Event()

    def lenta():
        pronto.wait(5)
        return b"SI"
    c = a.Conferma(lenta)
    assert c() is None            # l'attivazione non aspetta la rete
    pronto.set()
    for _ in range(100):
        if c():
            break
        time.sleep(0.02)
    assert c() == b"SI"


@pytest.mark.parametrize("valore,atteso", [(None, True), ("1", True), ("0", False), (" 0 ", False)])
def test_conferma_attiva_dall_ambiente(monkeypatch, valore, atteso):
    if valore is None:
        monkeypatch.delenv("GAS_ASCOLTO_CONFERMA", raising=False)
    else:
        monkeypatch.setenv("GAS_ASCOLTO_CONFERMA", valore)
    assert a.conferma_attiva() is atteso


class _ServerComando(http.server.BaseHTTPRequestHandler):
    risposta = (200, "application/json", b'{"content": "", "fine": true}', "fine")
    visti = []

    def do_POST(self):
        n = int(self.headers.get("Content-Length", 0))
        self.rfile.read(n)
        type(self).visti.append(dict(self.headers))
        codice, tipo, corpo, comando = type(self).risposta
        self.send_response(codice)
        self.send_header("Content-Type", tipo)
        self.send_header("Content-Length", str(len(corpo)))
        if comando:
            self.send_header("X-Gas-Comando", comando)
        self.end_headers()
        self.wfile.write(corpo)

    def log_message(self, *x):
        pass


@pytest.fixture
def server_comando():
    _ServerComando.visti = []
    s = http.server.HTTPServer(("127.0.0.1", 0), _ServerComando)
    t = threading.Thread(target=s.serve_forever, daemon=True)
    t.start()
    yield f"http://127.0.0.1:{s.server_address[1]}"
    s.shutdown()
    s.server_close()


@pytest.mark.parametrize("seguito", [False, True])
def test_invio_di_seguito_manda_l_intestazione(server_comando, seguito):
    _ServerComando.risposta = (200, "audio/mpeg", b"ID3", "")
    a.invia_al_server(server_comando, TOKEN, 5, seguito=seguito)(b"x")
    assert (_ServerComando.visti[0].get("X-Gas-Seguito") == "1") is seguito


@pytest.mark.parametrize("risposta,atteso", [
    ((200, "application/json", b'{"content": "", "fine": true}', "fine"),
     (True, None, "", "fine")),
    ((200, "audio/mpeg", b"ID3-VA-BENE", "pausa"), (True, b"ID3-VA-BENE", "", "pausa")),
    ((200, "audio/mpeg", b"ID3", "Pausa "), (True, b"ID3", "", "pausa")),
    ((200, "audio/mpeg", b"ID3", "spegni-tutto"), (True, b"ID3", "", "")),
    ((429, "application/json", b'{"error": "troppe"}', "pausa"),
     (False, None, "HTTP 429", "pausa")),
    ((500, "application/json", b'{"error": "x"}', ""), (False, None, "HTTP 500", "")),
])
def test_comando_del_server(server_comando, risposta, atteso):
    """V15 (PR #339 di M2): X-Gas-Comando «fine» (JSON vuoto) o «pausa», in ogni formato;
    un comando sconosciuto si ignora."""
    _ServerComando.risposta = risposta
    assert a.invia_al_server(server_comando, TOKEN, 5, seguito=True)(b"x") == atteso

def test_json_con_un_solo_audio(server):
    """Il server manda JSON (frase fissa «uso», o niente formato a pezzi): l'audio si suona."""
    _Server.risposta = (200, "application/json", json.dumps(
        {"content": "Non ho capito", "audio": _mp3(9)}).encode())
    ok, audio, motivo, _ = a.invia_al_server(server, TOKEN, 5)(b"x")
    assert (ok, audio, motivo) == (True, b"MP3-9", "")


def test_json_audio_rotto(server):
    _Server.risposta = (200, "application/json", b'{"audio": "%%%"}')
    ok, audio, motivo, _ = a.invia_al_server(server, TOKEN, 5)(b"x")
    assert not ok and audio is None and "risposta inattesa" in motivo


def test_senza_formato_come_prima(server):
    """GAS_ASCOLTO_FORMATO vuoto: niente X-Gas-Formato, e un JSON non vale come risposta."""
    _Server.risposta = (200, "application/json", json.dumps({"audio": _mp3(1)}).encode())
    ok, audio, motivo, _ = a.invia_al_server(server, TOKEN, 5, formato="")(b"x")
    assert not ok and "risposta inattesa" in motivo
    assert "X-Gas-Formato" not in _Server.visti[0][1]


@pytest.mark.parametrize("valore,atteso", [
    (None, a.FORMATO_PEZZI), ("", ""), (" Audio+Testo ", "audio+testo"),
    ("audio+pezzi", "audio+pezzi"), ("audio;rm", a.FORMATO_PEZZI), ("a" * 41, a.FORMATO_PEZZI),
])
def test_formato_dall_ambiente(monkeypatch, valore, atteso):
    if valore is None:
        monkeypatch.delenv("GAS_ASCOLTO_FORMATO", raising=False)
    else:
        monkeypatch.setenv("GAS_ASCOLTO_FORMATO", valore)
    assert a.formato_richiesto() == atteso


def test_turno_chiude_la_risposta_e_svuota(caplog):
    """Le frasi in fila: ognuna suonata, poi la risposta si chiude (il server smette di
    sintetizzare) e il microfono si svuota una volta sola, alla fine."""
    chiuse = []

    def frasi():
        try:
            yield b"A"
            yield b""
            yield b"B"
        finally:
            chiuse.append(True)

    f = Finti(esito=(True, frasi(), ""))
    asc = f.ascolto(iter([]))
    assert asc.turno([VOCE] * 3) is True
    assert f.riprodotti == [b"A", b"B"] and chiuse == [True] and f.svuotati == 1


def test_turno_interrotto_chiude_la_risposta():
    """Ctrl-C (o l'arresto di launchd) durante una frase: la risposta si chiude subito, così
    il server smette di sintetizzare le frasi che nessuno ascolterà."""
    chiuse = []

    def frasi():
        try:
            yield b"A"
            yield b"B"
        finally:
            chiuse.append(True)

    gen = frasi()
    f = Finti(esito=(True, gen, ""))

    def interrotta(audio):
        raise KeyboardInterrupt

    asc = a.Ascolto(iter([]), f.rilevatore, f.invia, interrotta, f.suona, svuota=f.svuota)
    with pytest.raises(KeyboardInterrupt):
        asc.turno([VOCE] * 3)
    assert chiuse == [True] and f.svuotati == 1


def test_turno_riproduzione_rotta_va_avanti():
    f = Finti(esito=(True, iter([b"A", b"B"]), ""))

    def rotta(audio):
        f.riprodotti.append(audio)
        raise OSError("afplay")

    asc = a.Ascolto(iter([]), f.rilevatore, f.invia, rotta, f.suona, svuota=f.svuota)
    assert asc.turno([VOCE] * 3) is True and f.riprodotti == [b"A", b"B"] and f.bip == []


class _Popen:
    """afplay finto: «suona» finché il test non lo fa finire (o non lo si ferma)."""
    ultimi: list = []

    def __init__(self, argv, **k):
        p = Path(argv[1])
        self.visto = (argv[0], p.read_bytes(), stat.S_IMODE(p.stat().st_mode))
        self.codice = None
        self.terminato = False
        _Popen.ultimi.append(self)

    def poll(self):
        return self.codice

    def terminate(self):
        self.terminato = True
        self.codice = -15

    def kill(self):
        self.codice = -9

    def wait(self, timeout=None):
        return self.codice


@pytest.fixture
def popen_finto(monkeypatch, tmp_path):
    monkeypatch.setattr(a.tempfile, "tempdir", str(tmp_path))
    _Popen.ultimi = []
    monkeypatch.setattr(a.subprocess, "Popen", _Popen)
    return tmp_path


def test_riproduzione_da_file_0600_cancellato(popen_finto):
    r = a.riproduci_afplay(b"ID3-MP3")
    p = _Popen.ultimi[0]
    assert p.visto == ("afplay", b"ID3-MP3", 0o600)
    assert not r.finita() and list(popen_finto.iterdir()) != []  # suona: il file c'è
    p.codice = 0
    assert r.finita() and list(popen_finto.iterdir()) == [] and not p.terminato


def test_riproduzione_fermata_cancella_il_file(popen_finto):
    """Fetta 41: `ferma()` spegne afplay e cancella il file; chiamarla due volte va bene."""
    r = a.riproduci_afplay(b"x")
    r.ferma()
    r.ferma()
    assert _Popen.ultimi[0].terminato and list(popen_finto.iterdir()) == []


def test_riproduzione_troppo_lunga_si_ferma(popen_finto):
    ora = [0.0]
    r = a.RiproduzioneAfplay(b"x", adesso=lambda: ora[0])
    assert not r.finita()
    ora[0] = a.RIPRODUZIONE_MAX_S
    assert r.finita() and _Popen.ultimi[0].terminato and list(popen_finto.iterdir()) == []


def test_riproduzione_fallita_cancella_comunque(monkeypatch, tmp_path):
    monkeypatch.setattr(a.tempfile, "tempdir", str(tmp_path))

    def esplode(argv, **k):
        raise OSError("afplay assente")

    monkeypatch.setattr(a.subprocess, "Popen", esplode)
    with pytest.raises(OSError):
        a.riproduci_afplay(b"x")
    assert list(tmp_path.iterdir()) == []


def test_wav_in_memoria():
    wav = a.in_wav([VOCE, SILENZIO])
    assert wav[:4] == b"RIFF" and _campioni(wav) == 2 * a.BLOCCO


@pytest.mark.parametrize("url,ok", [
    ("http://127.0.0.1:8765", True), ("http://localhost:8765", True),
    ("https://gas.example.org", True), ("http://gas.example.org", False),
    ("ftp://127.0.0.1", False), ("127.0.0.1:8765", False), ("http://", False),
])
def test_url_del_server(url, ok):
    assert (a.url_valido(url) is None) is ok


def test_senza_token_non_parte(monkeypatch, tmp_path, caplog):
    monkeypatch.setattr(a, "_GAS_ROOT", tmp_path)
    monkeypatch.delenv("GAS_VOICE_TOKEN", raising=False)
    monkeypatch.setattr(a, "Microfono", lambda: pytest.fail("microfono aperto senza token"))
    assert a.main() == 1


def test_url_in_chiaro_fuori_dal_mac_non_parte(monkeypatch, tmp_path):
    monkeypatch.setattr(a, "_GAS_ROOT", tmp_path)
    monkeypatch.setenv("GAS_VOICE_TOKEN", TOKEN)
    monkeypatch.setenv("GAS_VOICE_URL", "http://gas.example.org:8765")
    monkeypatch.setattr(a, "Microfono", lambda: pytest.fail("microfono aperto"))
    assert a.main() == 1


@pytest.mark.parametrize("url,porta,atteso", [
    (None, None, "http://127.0.0.1:8765"),
    (None, "9001", "http://127.0.0.1:9001"),
    ("https://gas.example.org/", "9001", "https://gas.example.org"),
])
def test_url_del_server_segue_la_porta(monkeypatch, url, porta, atteso):
    """R-616-1: senza GAS_VOICE_URL il client usa la porta del server voce."""
    for k, v in (("GAS_VOICE_URL", url), ("GAS_VOICE_PORT", porta)):
        if v is None:
            monkeypatch.delenv(k, raising=False)
        else:
            monkeypatch.setenv(k, v)
    assert a.url_del_server() == atteso


def test_main_usa_la_porta_del_server(monkeypatch, tmp_path):
    """R-618-1: `main` costruisce l'invio con url_del_server() (porta del server voce)."""
    monkeypatch.setattr(a, "_GAS_ROOT", tmp_path)
    monkeypatch.setenv("GAS_VOICE_TOKEN", TOKEN)
    monkeypatch.delenv("GAS_VOICE_URL", raising=False)
    monkeypatch.setenv("GAS_VOICE_PORT", "9001")
    visti = []
    monkeypatch.setattr(a, "rilevatore_openwakeword", lambda m: (lambda b: 0.0, lambda: None))
    monkeypatch.setattr(a, "invia_al_server",
                        lambda url, token, timeout, seguito=False:
                        (visti.append((url, seguito)), lambda wav: (False, None, ""))[1])

    def fermati():
        raise KeyboardInterrupt
    monkeypatch.setattr(a, "Microfono", fermati)
    # fetta 43 parte 2: un invio normale e uno «di seguito», tutti e due sulla porta giusta
    assert a.main() == 0 and visti == [("http://127.0.0.1:9001", False),
                                       ("http://127.0.0.1:9001", True)]


@pytest.mark.parametrize("ripiego", [False, True])
def test_dotenv_non_sovrascrive(monkeypatch, tmp_path, ripiego):
    (tmp_path / ".env").write_text('GAS_VOICE_TOKEN="dal-file"\nexport GAS_PROVA_ASCOLTO=x\n',
                                   encoding="utf-8")
    monkeypatch.delenv("GAS_NO_DOTENV", raising=False)  # conftest lo accende per la suite
    if ripiego:
        _senza_gas(monkeypatch)
    monkeypatch.setenv("GAS_VOICE_TOKEN", "dall-ambiente")
    monkeypatch.delenv("GAS_PROVA_ASCOLTO", raising=False)
    a._carica_dotenv(tmp_path)
    assert os.environ["GAS_VOICE_TOKEN"] == "dall-ambiente"
    assert os.environ["GAS_PROVA_ASCOLTO"] == "x"


def _senza_gas(monkeypatch):
    """gas.py non importabile: il client usa il ripiego."""
    import builtins
    vero_import = builtins.__import__

    def finto(nome, *args, **kw):
        if nome == "gas":
            raise ImportError("gas assente")
        return vero_import(nome, *args, **kw)
    monkeypatch.setattr(builtins, "__import__", finto)


@pytest.mark.parametrize("ripiego", [False, True])
def test_dotenv_come_il_server(monkeypatch, tmp_path, ripiego):
    """V-1 bot #323: commento in linea, virgolette con commento e BOM letti come li legge
    il server voce (gas._carica_dotenv), così il token del client è lo stesso."""
    (tmp_path / ".env").write_bytes(
        "\ufeffGAS_VOICE_TOKEN=abc # voce\nGAS_VOICE_PORT=\"9001\" # porta\n".encode())
    monkeypatch.delenv("GAS_NO_DOTENV", raising=False)
    monkeypatch.delenv("GAS_VOICE_TOKEN", raising=False)
    monkeypatch.delenv("GAS_VOICE_PORT", raising=False)
    if ripiego:
        _senza_gas(monkeypatch)
    a._carica_dotenv(tmp_path)
    assert os.environ["GAS_VOICE_TOKEN"] == "abc" and os.environ["GAS_VOICE_PORT"] == "9001"


def test_dotenv_usa_il_caricatore_di_gas(monkeypatch, tmp_path):
    """V-1 bot #323: la strada principale è proprio gas._carica_dotenv (lo stesso del
    server voce), con il .env della cartella di Gas."""
    import gas
    visti = []
    monkeypatch.setattr(gas, "_carica_dotenv", lambda path=None: visti.append(path) or [])
    a._carica_dotenv(tmp_path)
    assert visti == [tmp_path / ".env"]


def test_dotenv_spento_dalla_suite(monkeypatch, tmp_path):
    """GAS_NO_DOTENV=1 vale anche per il client (come per server e CLI)."""
    (tmp_path / ".env").write_text("GAS_PROVA_SPENTO=1\n", encoding="utf-8")
    monkeypatch.setenv("GAS_NO_DOTENV", "1")
    monkeypatch.delenv("GAS_PROVA_SPENTO", raising=False)
    a._carica_dotenv(tmp_path)
    a._carica_dotenv_ripiego(tmp_path)
    assert "GAS_PROVA_SPENTO" not in os.environ


@pytest.mark.parametrize("valore,atteso", [("abc", 12.0), ("nan", 12.0), ("inf", 12.0),
                                           ("-5", 0.0), ("999", 120.0), ("7", 7.0)])
def test_numeri_dall_ambiente(monkeypatch, valore, atteso):
    monkeypatch.setenv("GAS_VOICE_FINESTRA", valore)
    assert a._numero("GAS_VOICE_FINESTRA", 12, 0, 120) == atteso


# ── scripts/voce ──

VOCE_DIR = RADICE / "scripts" / "voce"


@pytest.mark.parametrize("nome,comando", [
    ("com.gas.voce.server", "exec python -m modules.voice.server"),
    ("com.gas.ascolto", "exec python clients/voice/ascolto.py"),
])
def test_plist(nome, comando):
    p = plistlib.loads((VOCE_DIR / f"{nome}.plist").read_bytes())
    assert p["Label"] == nome and p["RunAtLoad"] is True and p["KeepAlive"] is True
    assert p["ThrottleInterval"] >= 10
    assert p["ProgramArguments"][:2] == ["/bin/zsh", "-c"]
    assert comando in p["ProgramArguments"][2] and "CARTELLA_GAS" in p["ProgramArguments"][2]
    assert p["StandardOutPath"].startswith("CARTELLA_GAS/.gas_voce/")


@pytest.mark.parametrize("script", ["installa.sh", "spegni.sh", "pausa.sh", "riprendi.sh"])
def test_script_sintassi_e_solo_mac(script):
    percorso = VOCE_DIR / script
    assert subprocess.run(["bash", "-n", str(percorso)]).returncode == 0
    if sys.platform != "darwin":
        r = subprocess.run(["bash", str(percorso)], capture_output=True, text=True, timeout=30)
        assert r.returncode == 1 and "solo per il Mac" in r.stderr


def test_installa_non_stampa_il_token():
    testo = (VOCE_DIR / "installa.sh").read_text(encoding="utf-8")
    assert 'TOKEN_VOCE="$(valore_env GAS_VOICE_TOKEN' in testo  # letto senza stamparlo
    assert "cat .env" not in testo and "echo $GAS_VOICE_TOKEN" not in testo
    assert "$TOKEN_VOCE" not in testo.replace('[ -n "$TOKEN_VOCE" ]', "").replace(
        '[[ "$TOKEN_VOCE" != \\#* ]]', "")


def test_dipendenze_del_mac_fissate():
    righe = [r for r in (RADICE / "clients/voice/requirements-ascolto.txt").read_text()
             .splitlines() if r.strip() and not r.startswith("#")]
    assert righe and all("==" in r for r in righe)
    assert any(r.startswith("openwakeword==") for r in righe)


# ── installa.sh fino in fondo, con i comandi del Mac finti (R-615-1) ──

_FINTI = {
    "uname": 'echo Darwin',
    "plutil": 'exit 0',
    # launchctl con lo stato dei servizi (prova dal vero di M1): «$REGISTRO.su.<servizio>»
    # = caricato. Dopo bootout il servizio resta visibile per BOOTOUT_LENTO letture di
    # print (bootout asincrono) e in quel tempo bootstrap fallisce con l'errore 5 vero;
    # BOOTSTRAP_FALLISCE = quanti bootstrap falliscono comunque prima di riuscire.
    "launchctl": ('echo "launchctl $*" >> "$REGISTRO"\n'
                  'case "$1" in\n'
                  '  print) s="${2##*/}"\n'
                  '    if [ -f "$REGISTRO.su.$s" ]; then echo "	state = running"; exit 0; fi\n'
                  '    n=$(cat "$REGISTRO.giu.$s" 2>/dev/null || echo 0)\n'
                  '    if [ "$n" -gt 0 ]; then echo $((n-1)) > "$REGISTRO.giu.$s"\n'
                  '      echo "	state = running"; exit 0; fi\n'
                  '    echo "Could not find service" >&2; exit 113;;\n'
                  '  bootout) s="${2##*/}"; [ -f "$REGISTRO.su.$s" ] || exit 3\n'
                  '    rm -f "$REGISTRO.su.$s"; echo "${BOOTOUT_LENTO:-0}" > "$REGISTRO.giu.$s";;\n'
                  '  bootstrap) s="$(basename "$3" .plist)"\n'
                  '    n=$(cat "$REGISTRO.giu.$s" 2>/dev/null || echo 0)\n'
                  '    f=$(cat "$REGISTRO.bs" 2>/dev/null || echo 0); echo $((f+1)) > "$REGISTRO.bs"\n'
                  '    if [ -f "$REGISTRO.su.$s" ] || [ "$n" -gt 0 ] \\\n'
                  '       || [ "$f" -lt "${BOOTSTRAP_FALLISCE:-0}" ]; then\n'
                  '      echo "Bootstrap failed: 5: Input/output error" >&2; exit 5; fi\n'
                  '    touch "$REGISTRO.su.$s";;\n'
                  'esac\nexit 0'),
    "nc": ('echo "nc $*" >> "$REGISTRO"\n'
           'n=$(cat "$REGISTRO.nc" 2>/dev/null || echo 0); echo $((n+1)) > "$REGISTRO.nc"\n'
           '[ "$((n+1))" -gt "${NC_FALLISCE:-0}" ]'),
    "sleep": 'echo "sleep $*" >> "$REGISTRO"; exit 0',  # R-629-1: le attese si contano
    "python": ('echo "python $*" >> "$REGISTRO"\n'
               'case "$*" in *version_info*) [ -z "$PYTHON_VECCHIO" ];; *) cat > /dev/null;; esac'),
    "python3": 'echo "python3 $*" >> "$REGISTRO"; exit 0',
}


def _gas_finto(tmp_path, nome="Gas", env="GAS_VOICE_TOKEN=segreto-di-prova\n"):
    gas = tmp_path / nome
    (gas / "scripts" / "voce").mkdir(parents=True)
    for f in VOCE_DIR.iterdir():
        (gas / "scripts" / "voce" / f.name).write_bytes(f.read_bytes())
    (gas / "clients" / "voice").mkdir(parents=True)
    (gas / "clients/voice/requirements-ascolto.txt").write_text("")
    (gas / "requirements.txt").write_text("")
    (gas / "gas.py").write_text("")
    (gas / ".env").write_text(env)
    finti = tmp_path / "finti"
    finti.mkdir(exist_ok=True)
    for nome_cmd, corpo in _FINTI.items():
        p = finti / nome_cmd
        p.write_text("#!/bin/bash\n" + corpo + "\n")
        p.chmod(0o755)
    (gas / ".venv" / "bin").mkdir(parents=True)
    (gas / ".venv/bin/activate").write_text(f'export PATH="{finti}:$PATH"\n')
    casa = tmp_path / "casa"
    casa.mkdir(exist_ok=True)
    return gas, finti, casa


def _installa(gas, finti, casa, tmp_path, **extra):
    registro = tmp_path / "registro.txt"
    env = {"PATH": f"{finti}:/usr/bin:/bin", "HOME": str(casa), "REGISTRO": str(registro),
           **extra}
    r = subprocess.run(["bash", str(gas / "scripts/voce/installa.sh")], capture_output=True,
                       text=True, timeout=60, env=env)
    return r, registro.read_text() if registro.exists() else ""


def test_installa_arriva_in_fondo_senza_porta_nel_env(tmp_path):
    """R-615-1: senza GAS_VOICE_PORT nel .env (il caso normale) lo script non deve
    fermarsi in silenzio dopo il passo 5."""
    gas, finti, casa = _gas_finto(tmp_path)
    r, registro = _installa(gas, finti, casa, tmp_path)
    assert r.returncode == 0, r.stdout + r.stderr
    assert "6/6 tutto acceso" in r.stdout and "nc -z 127.0.0.1 8765" in registro
    assert "segreto-di-prova" not in r.stdout + r.stderr + registro
    for s in ("com.gas.voce.server", "com.gas.ascolto"):
        p = plistlib.loads((casa / "Library/LaunchAgents" / f"{s}.plist").read_bytes())
        assert str(gas) in p["ProgramArguments"][2] and "CARTELLA_GAS" not in str(p)
        assert f"launchctl bootstrap gui/" in registro


def test_installa_usa_la_porta_del_env(tmp_path):
    gas, finti, casa = _gas_finto(tmp_path, env="GAS_VOICE_TOKEN=x\nGAS_VOICE_PORT=9001\n")
    r, registro = _installa(gas, finti, casa, tmp_path)
    assert r.returncode == 0 and "nc -z 127.0.0.1 9001" in registro.splitlines()


def test_installa_porta_ripetuta_vale_la_prima(tmp_path):
    """V-2 bot #323: come server e ascolto, vale la PRIMA GAS_VOICE_PORT del .env."""
    gas, finti, casa = _gas_finto(
        tmp_path, env="GAS_VOICE_TOKEN=x\nGAS_VOICE_PORT=9001\nGAS_VOICE_PORT=9002\n")
    r, registro = _installa(gas, finti, casa, tmp_path)
    assert r.returncode == 0 and "nc -z 127.0.0.1 9001" in registro.splitlines()


def test_installa_avvisa_se_c_e_un_url_remoto(tmp_path):
    gas, finti, casa = _gas_finto(
        tmp_path, env="GAS_VOICE_TOKEN=x\nGAS_VOICE_URL=https://gas.example.org\n")
    r, _ = _installa(gas, finti, casa, tmp_path)
    assert r.returncode == 0 and "AVVISO: nel .env c'è GAS_VOICE_URL" in r.stdout


def test_installa_porta_con_commento_in_linea(tmp_path):
    """R-622-1: le cifre di un commento in linea non finiscono nella porta."""
    gas, finti, casa = _gas_finto(tmp_path, env="GAS_VOICE_TOKEN=x\nGAS_VOICE_PORT=9001 # era 8765\n")
    r, registro = _installa(gas, finti, casa, tmp_path)
    assert r.returncode == 0 and "nc -z 127.0.0.1 9001" in registro.splitlines()


def _gia_caricati(tmp_path):
    for s in ("com.gas.voce.server", "com.gas.ascolto"):
        (tmp_path / f"registro.txt.su.{s}").touch()


def test_installa_seconda_volta_aspetta_che_il_vecchio_sparisca(tmp_path):
    """Prova dal vero di M1: alla seconda esecuzione bootout è asincrono e un bootstrap
    subito dopo dà «Bootstrap failed: 5». Lo script aspetta che print fallisca."""
    gas, finti, casa = _gas_finto(tmp_path)
    _gia_caricati(tmp_path)
    r, registro = _installa(gas, finti, casa, tmp_path, BOOTOUT_LENTO="4")
    assert r.returncode == 0, r.stdout + r.stderr
    assert "Bootstrap failed" not in r.stderr
    righe = registro.splitlines()
    for s in ("com.gas.voce.server", "com.gas.ascolto"):
        fuori = righe.index(f"launchctl bootout gui/{os.getuid()}/{s}")
        dentro = next(i for i, x in enumerate(righe) if x.startswith("launchctl bootstrap")
                      and x.endswith(f"/{s}.plist"))
        letture = [x for x in righe[fuori:dentro] if x == f"launchctl print gui/{os.getuid()}/{s}"]
        assert len(letture) == 5  # 4 ancora visibile + 1 sparito


def test_installa_servizio_che_non_si_spegne_si_ferma(tmp_path):
    gas, finti, casa = _gas_finto(tmp_path)
    _gia_caricati(tmp_path)
    r, registro = _installa(gas, finti, casa, tmp_path, BOOTOUT_LENTO="999")
    assert r.returncode == 1 and "non si spegne" in r.stderr
    assert "launchctl bootstrap" not in registro
    assert registro.count("launchctl print gui/") == 50  # al massimo 5 s (50 × 0,1 s)


def test_installa_bootstrap_riprova(tmp_path):
    gas, finti, casa = _gas_finto(tmp_path)
    r, registro = _installa(gas, finti, casa, tmp_path, BOOTSTRAP_FALLISCE="2")
    assert r.returncode == 0, r.stdout + r.stderr
    assert registro.count("launchctl bootstrap") == 4  # 2 falliti + 2 servizi
    assert r.stdout.count("riprovo tra 1 s") == 2  # R-628-3: si dice che riprova


def test_installa_bootstrap_sempre_rotto_si_ferma(tmp_path):
    gas, finti, casa = _gas_finto(tmp_path)
    r, registro = _installa(gas, finti, casa, tmp_path, BOOTSTRAP_FALLISCE="99")
    assert r.returncode == 1 and "3 tentativi" in r.stderr
    assert registro.count("launchctl bootstrap") == 3 and "nc -z" not in registro
    assert r.stdout.count("riprovo tra 1 s") == 2
    assert registro.splitlines().count("sleep 1") == 2  # R-629-1: niente attesa dopo il terzo


# ── V-1/V-2 bot #328: installa.sh legge il .env come gas._carica_dotenv ──

_CASI_ENV = [
    "K=abc\n",
    "K = abc\n",                         # spazi intorno a «=»
    "K= abc\n",
    "export K=abc\n",
    "  export   K=abc  \n",
    "K=abc # commento\n",
    "K=#abc\n",                          # «#» senza spazio prima: fa parte del valore
    "K=a#b\n",
    'K="abc" # commento\n',
    "K='a b'\n",
    'K="a" # "b"\n',
    'K="abc\nK=dopo\n',                 # virgolette non chiuse: riga ignorata, vale la dopo
    "K=\nK=abc\n",                       # vale la PRIMA, anche vuota
    "K= # solo commento\n",
    "# K=abc\nK=vero\n",
    "\ufeffK=bom\n",
    "K=crlf\r\nALTRA=1\r\n",
    "ALTRA=1\n",                          # chiave assente
    "K=senza-a-capo-finale",
    "KK=no\nK=si\n",
]


def _valore_env_bash(tmp_path, contenuto):
    f = tmp_path / ".env"
    f.write_bytes(contenuto.encode("utf-8"))
    script = (VOCE_DIR / "installa.sh").read_text(encoding="utf-8")
    inizio = script.index("_spazi_via() {")
    fine = script.index("\n}\n", script.index("valore_env() {")) + 3
    r = subprocess.run(["bash", "-c", script[inizio:fine] + '\nvalore_env K "$1"', "x", str(f)],
                       capture_output=True, text=True, timeout=10)
    return r.stdout if r.returncode == 0 else None


@pytest.mark.parametrize("contenuto", _CASI_ENV)
def test_installa_legge_il_env_come_gas(tmp_path, monkeypatch, contenuto):
    import gas
    monkeypatch.delenv("GAS_NO_DOTENV", raising=False)
    monkeypatch.delenv("K", raising=False)
    (tmp_path / "g").mkdir()
    (tmp_path / "g" / ".env").write_bytes(contenuto.encode("utf-8"))
    gas._carica_dotenv(tmp_path / "g" / ".env")
    atteso = os.environ.get("K")
    monkeypatch.delenv("K", raising=False)
    assert _valore_env_bash(tmp_path, contenuto) == atteso


@pytest.mark.parametrize("env", [
    "GAS_VOICE_TOKEN=\nGAS_VOICE_TOKEN=segreto\n",   # la prima è vuota: il server non avrebbe token
    "GAS_VOICE_TOKEN=''\nGAS_VOICE_TOKEN=segreto\n",
])
def test_installa_token_vuoto_nella_prima_riga_si_ferma(tmp_path, env):
    gas, finti, casa = _gas_finto(tmp_path, env=env)
    r, registro = _installa(gas, finti, casa, tmp_path)
    assert r.returncode == 1 and "GAS_VOICE_TOKEN non è nel .env" in r.stderr
    assert "launchctl" not in registro and "segreto" not in r.stdout + r.stderr


@pytest.mark.parametrize("env", ["GAS_VOICE_TOKEN = abc\n", "export GAS_VOICE_TOKEN='a b'\n"])
def test_installa_token_scritto_come_lo_accetta_gas(tmp_path, env):
    gas, finti, casa = _gas_finto(tmp_path, env=env)
    r, _ = _installa(gas, finti, casa, tmp_path)
    assert r.returncode == 0, r.stdout + r.stderr


@pytest.mark.parametrize("env", ["GAS_VOICE_TOKEN=#abc\n", "GAS_VOICE_TOKEN= # da mettere\n"])
def test_installa_token_che_comincia_con_cancelletto_si_ferma(tmp_path, env):
    """Gas prende «# da mettere» come token: lo script si ferma e dice perché."""
    gas, finti, casa = _gas_finto(tmp_path, env=env)
    r, registro = _installa(gas, finti, casa, tmp_path)
    assert r.returncode == 1 and "comincia con #" in r.stderr and registro == ""


def test_installa_claude_vuoto_nella_prima_riga_avvisa(tmp_path):
    gas, finti, casa = _gas_finto(
        tmp_path, env="GAS_VOICE_TOKEN=t\nGAS_CLAUDE_BIN=\nGAS_CLAUDE_BIN=/x/claude\n")
    r, _ = _installa(gas, finti, casa, tmp_path)
    assert r.returncode == 0 and "GAS_CLAUDE_BIN è vuoto" in r.stdout
    assert (gas / ".env").read_text().count("GAS_CLAUDE_BIN") == 2  # niente riga aggiunta


def test_installa_claude_non_assoluto_avvisa(tmp_path):
    gas, finti, casa = _gas_finto(tmp_path, env="GAS_VOICE_TOKEN=t\nGAS_CLAUDE_BIN=claude\n")
    r, _ = _installa(gas, finti, casa, tmp_path)
    assert r.returncode == 0 and "non è un percorso assoluto" in r.stdout


def test_installa_claude_con_spazi_non_si_raddoppia(tmp_path):
    gas, finti, casa = _gas_finto(tmp_path, env="GAS_VOICE_TOKEN=t\nGAS_CLAUDE_BIN = /x/claude\n")
    r, _ = _installa(gas, finti, casa, tmp_path)
    assert r.returncode == 0 and "aggiunto" not in r.stdout and "vuoto" not in r.stdout
    assert (gas / ".env").read_text().count("GAS_CLAUDE_BIN") == 1


def _claude_finto(tmp_path, cartella):
    d = tmp_path / cartella
    d.mkdir(parents=True)
    c = d / "claude"
    c.write_text("#!/bin/bash\nexit 0\n")
    c.chmod(0o755)
    return d


@pytest.mark.parametrize("cartella", ["bin$(touch PWNED)", "bin;x", "bin`id`", "a\\b"])
def test_installa_claude_in_cartella_pericolosa_non_scrive_il_env(tmp_path, cartella):
    """R-625-1: la lista bianca tiene fuori dal .env un percorso con caratteri pericolosi."""
    gas, finti, casa = _gas_finto(tmp_path, env="GAS_VOICE_TOKEN=t\n")
    d = _claude_finto(tmp_path, cartella)
    r, _ = _installa(gas, finti, casa, tmp_path, PATH=f"{finti}:{d}:/usr/bin:/bin")
    assert r.returncode == 0, r.stdout + r.stderr
    assert "caratteri non ammessi" in r.stdout
    assert "GAS_CLAUDE_BIN" not in (gas / ".env").read_text()
    assert not (tmp_path / "PWNED").exists() and not (gas / "PWNED").exists()


def test_installa_claude_in_cartella_buona_scrive_il_env(tmp_path):
    gas, finti, casa = _gas_finto(tmp_path, env="GAS_VOICE_TOKEN=t\n")
    d = _claude_finto(tmp_path, "strumenti buoni/bin")
    r, _ = _installa(gas, finti, casa, tmp_path, PATH=f"{finti}:{d}:/usr/bin:/bin")
    assert r.returncode == 0 and f"GAS_CLAUDE_BIN={d}/claude aggiunto" in r.stdout
    assert f"\nGAS_CLAUDE_BIN={d}/claude\n" in (gas / ".env").read_text()


def test_installa_aspetta_il_server_lento(tmp_path):
    """V-3 ve #323: il server che ci mette qualche secondo non dà un falso STOP."""
    gas, finti, casa = _gas_finto(tmp_path)
    r, registro = _installa(gas, finti, casa, tmp_path, NC_FALLISCE="3")
    assert r.returncode == 0 and registro.count("nc -z") == 4
    assert registro.splitlines().count("sleep 1") == 3  # R-631-1 (= R-623-2): si aspetta davvero


def test_installa_server_che_non_risponde_si_ferma(tmp_path):
    gas, finti, casa = _gas_finto(tmp_path)
    r, registro = _installa(gas, finti, casa, tmp_path, NC_FALLISCE="999")
    assert r.returncode == 1 and "non risponde" in r.stderr and registro.count("nc -z") == 30


def test_installa_python_vecchio_si_ferma_prima_delle_dipendenze(tmp_path):
    """V-3 ve #323: con Python < 3.11 nel .venv lo dice, invece di un pip che fallisce."""
    gas, finti, casa = _gas_finto(tmp_path)
    r, registro = _installa(gas, finti, casa, tmp_path, PYTHON_VECCHIO="1")
    assert r.returncode == 1 and "Python 3.11" in r.stderr and "pip install" not in registro


def test_installa_scrive_gas_claude_bin(tmp_path):
    """V-1 bot #323: con `claude` nel PATH e senza GAS_CLAUDE_BIN nel .env, installa.sh
    lo aggiunge col percorso assoluto (sotto launchd il PATH non lo troverebbe)."""
    gas, finti, casa = _gas_finto(tmp_path)
    (finti / "claude").write_text("#!/bin/bash\nexit 0\n")
    (finti / "claude").chmod(0o755)
    r, _ = _installa(gas, finti, casa, tmp_path)
    env = (gas / ".env").read_text()
    assert r.returncode == 0 and f"GAS_CLAUDE_BIN={finti}/claude" in env.splitlines()
    assert env.startswith("GAS_VOICE_TOKEN=segreto-di-prova\n")


def test_installa_non_tocca_un_gas_claude_bin_esistente(tmp_path):
    gas, finti, casa = _gas_finto(tmp_path, env="GAS_VOICE_TOKEN=x\nGAS_CLAUDE_BIN=/opt/c\n")
    (finti / "claude").write_text("#!/bin/bash\nexit 0\n")
    (finti / "claude").chmod(0o755)
    r, _ = _installa(gas, finti, casa, tmp_path)
    assert r.returncode == 0 and (gas / ".env").read_text() == "GAS_VOICE_TOKEN=x\nGAS_CLAUDE_BIN=/opt/c\n"


@pytest.mark.parametrize("riga", ["GAS_CLAUDE_BIN=", "GAS_CLAUDE_BIN= # da mettere"])
def test_installa_gas_claude_bin_vuoto_avvisa_e_non_raddoppia(tmp_path, riga):
    """R-624-3: una riga vuota non si raddoppia (vale la prima) e si avvisa."""
    gas, finti, casa = _gas_finto(tmp_path, env="GAS_VOICE_TOKEN=x\n" + riga + "\n")
    (finti / "claude").write_text("#!/bin/bash\nexit 0\n")
    (finti / "claude").chmod(0o755)
    r, _ = _installa(gas, finti, casa, tmp_path)
    assert r.returncode == 0 and "GAS_CLAUDE_BIN è vuoto" in r.stdout
    assert (gas / ".env").read_text() == "GAS_VOICE_TOKEN=x\n" + riga + "\n"


def test_installa_avvisa_se_claude_manca(tmp_path):
    gas, finti, casa = _gas_finto(tmp_path)
    r, _ = _installa(gas, finti, casa, tmp_path)
    assert r.returncode == 0 and "claude` non trovato" in r.stdout
    assert "GAS_CLAUDE_BIN" not in (gas / ".env").read_text()


@pytest.mark.parametrize("riga", ["GAS_VOICE_TOKEN=", "GAS_VOICE_TOKEN= # da mettere",
                                  "GAS_VOICE_TOKEN=\"\"", "GAS_VOICE_TOKEN=   "])
def test_installa_token_vuoto_si_ferma(tmp_path, riga):
    """V-4 bot #323: un token vuoto o col solo commento non passa il controllo."""
    gas, finti, casa = _gas_finto(tmp_path, env=riga + "\n")
    r, registro = _installa(gas, finti, casa, tmp_path)
    assert r.returncode == 1 and "GAS_VOICE_TOKEN" in r.stderr and registro == ""


@pytest.mark.parametrize("riga", ["GAS_VOICE_TOKEN=abc", "export GAS_VOICE_TOKEN=\"abc\"",
                                  "GAS_VOICE_TOKEN='abc' # x"])
def test_installa_token_buono_passa(tmp_path, riga):
    gas, finti, casa = _gas_finto(tmp_path, env=riga + "\n")
    r, _ = _installa(gas, finti, casa, tmp_path)
    assert r.returncode == 0, r.stderr


def test_installa_senza_token_si_ferma_prima_di_tutto(tmp_path):
    gas, finti, casa = _gas_finto(tmp_path, env="ALTRO=1\n")
    r, registro = _installa(gas, finti, casa, tmp_path)
    assert r.returncode == 1 and "GAS_VOICE_TOKEN" in r.stderr
    assert registro == "" and not (casa / "Library").exists()


@pytest.mark.parametrize("nome", ["Gas$(touch PWNED)", "Gas`touch PWNED`", "Ga\\s", "Ga&s",
                                  'Ga"s', "Ga#s", "Ga;s"])
def test_installa_rifiuta_cartelle_con_caratteri_pericolosi(tmp_path, nome):
    """R-615-3: lista bianca dei caratteri della cartella di Gas (finisce nel sed e
    nella shell del plist)."""
    gas, finti, casa = _gas_finto(tmp_path, nome=nome)
    r, registro = _installa(gas, finti, casa, tmp_path)
    assert r.returncode == 1 and "caratteri" in r.stderr
    assert registro == "" and not (tmp_path / "PWNED").exists()


# ── fetta 43: pausa.sh e riprendi.sh (solo l'ascolto, il server resta) ──

def _voce_cmd(tmp_path, script, acceso=True, plist=True, **extra):
    gas, finti, casa = _gas_finto(tmp_path)
    registro = tmp_path / "registro.txt"
    if acceso:
        (tmp_path / "registro.txt.su.com.gas.ascolto").touch()
    (tmp_path / "registro.txt.su.com.gas.voce.server").touch()
    agenti = casa / "Library" / "LaunchAgents"
    agenti.mkdir(parents=True, exist_ok=True)
    if plist:
        (agenti / "com.gas.ascolto.plist").write_text("<plist/>")
    env = {"PATH": f"{finti}:/usr/bin:/bin", "HOME": str(casa), "REGISTRO": str(registro),
           **extra}
    r = subprocess.run(["bash", str(gas / "scripts/voce" / script)], capture_output=True,
                       text=True, timeout=60, env=env)
    log_ = registro.read_text() if registro.exists() else ""
    return r, log_, tmp_path / "registro.txt.su.com.gas.ascolto", agenti


def test_pausa_ferma_solo_l_ascolto(tmp_path):
    r, log_, su, agenti = _voce_cmd(tmp_path, "pausa.sh")
    assert r.returncode == 0 and "PAUSA" in r.stdout and "riprendi.sh" in r.stdout
    assert not su.exists()                                  # l'ascolto è giù
    assert (tmp_path / "registro.txt.su.com.gas.voce.server").exists()   # il server no
    assert "com.gas.voce.server" not in log_ and "bootstrap" not in log_
    assert (agenti / "com.gas.ascolto.plist").exists()      # il plist resta


def test_pausa_quando_e_gia_in_pausa(tmp_path):
    r, log_, _, _ = _voce_cmd(tmp_path, "pausa.sh", acceso=False)
    assert r.returncode == 0 and "già in pausa" in r.stdout and "bootout" not in log_


def test_pausa_aspetta_il_bootout_lento(tmp_path):
    r, log_, _, _ = _voce_cmd(tmp_path, "pausa.sh", BOOTOUT_LENTO="4")
    assert r.returncode == 0 and "PAUSA" in r.stdout and log_.count("sleep 0.1") == 4


def test_pausa_che_non_si_ferma_lo_dice(tmp_path):
    r, _, _, _ = _voce_cmd(tmp_path, "pausa.sh", BOOTOUT_LENTO="999")
    assert r.returncode == 1 and "non si è fermato" in r.stderr and "PAUSA" not in r.stdout


def test_riprendi_riaccende_l_ascolto(tmp_path):
    r, log_, su, _ = _voce_cmd(tmp_path, "riprendi.sh", acceso=False)
    assert r.returncode == 0 and "RIPRESO" in r.stdout and su.exists()
    assert "com.gas.voce.server" not in log_


def test_riprendi_quando_ascolta_gia(tmp_path):
    r, log_, _, _ = _voce_cmd(tmp_path, "riprendi.sh")
    assert r.returncode == 0 and "già ascoltando" in r.stdout and "bootstrap" not in log_


def test_riprendi_senza_installazione(tmp_path):
    r, log_, _, _ = _voce_cmd(tmp_path, "riprendi.sh", acceso=False, plist=False)
    assert r.returncode == 1 and "installa.sh" in r.stderr and "bootstrap" not in log_


@pytest.mark.parametrize("falliti,ok", [(2, True), (3, False)])
def test_riprendi_riprova_il_bootstrap(tmp_path, falliti, ok):
    r, log_, su, _ = _voce_cmd(tmp_path, "riprendi.sh", acceso=False,
                               BOOTSTRAP_FALLISCE=str(falliti))
    assert log_.count("launchctl bootstrap") == min(falliti + 1, 3)
    assert (r.returncode == 0) is ok and su.exists() is ok
    if not ok:
        assert "non è ripartito" in r.stderr


def test_pausa_e_riprendi_nel_leggimi():
    testo = (VOCE_DIR / "LEGGIMI.md").read_text(encoding="utf-8")
    assert "bash scripts/voce/pausa.sh" in testo and "bash scripts/voce/riprendi.sh" in testo


@pytest.mark.parametrize("valore,atteso", [("20", 20.0), ("1", 3.0), ("99", 30.0), ("x", 15.0)])
def test_main_tetto_di_seguito_dall_ambiente(monkeypatch, tmp_path, valore, atteso):
    k = _main_finto(monkeypatch, tmp_path, {"GAS_VOICE_SEGUITO_MAX": valore})
    assert k.get("seguito_max_s") == atteso


def test_leggimi_finestra_e_seguito():
    testo = (VOCE_DIR / "LEGGIMI.md").read_text(encoding="utf-8")
    assert f"| `GAS_VOICE_FINESTRA` | {a.FINESTRA_PREDEFINITA_S:g} |" in testo
    assert f"| `GAS_VOICE_SEGUITO_MAX` | {a.SEGUITO_MAX_PREDEFINITO_S:g} |" in testo
