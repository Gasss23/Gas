"""Test del CRM clienti (modules/crm): soldi esatti, registro immutabile, motore delle
opportunità, testi WhatsApp, server della dashboard. Zero rete esterna, zero token:
il server gira su 127.0.0.1 con porta scelta dal sistema, l'orologio è finto."""
from __future__ import annotations

import http.client
import json
import os
import plistlib
import shutil
import signal
import subprocess
import sys
import sqlite3
import threading
import time
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import pytest

from modules.crm import analisi, messaggi, motore, server
from modules.crm.store import (CRMStore, ErroreCRM, formatta_euro, formatta_euro_tondo,
                               normalizza_telefono, parse_importo, parse_percentuale_bp)

# ---------------------------------------------------------------------- appoggi


class Orologio:
    """Orologio finto che si può spostare in avanti."""

    def __init__(self, inizio: datetime) -> None:
        self.ora = inizio

    def __call__(self) -> datetime:
        return self.ora

    def avanti(self, giorni: int) -> None:
        self.ora = self.ora + timedelta(days=giorni)


INIZIO = datetime(2026, 6, 20, 10, 0, tzinfo=timezone.utc)
# Ritmo SETTIMANALE esplicito per i test di insistenza e di pausa (scritti col ritmo della
# prima bozza); i default MENSILI decisi dall'operatore il 17-11 hanno i loro test sotto.
REGOLE = motore.Regole(pausa_giorni=7, max_messaggi_30g=4)


@pytest.fixture
def orologio() -> Orologio:
    return Orologio(INIZIO)


@pytest.fixture
def st(tmp_path: Path, orologio: Orologio) -> CRMStore:
    s = CRMStore(tmp_path / "crm.db", orologio=orologio)
    assert s.available
    return s


def servizi_base(st: CRMStore) -> Dict[str, int]:
    return {
        "oro": st.aggiungi_servizio("oro", "Copy Oro", "percentuale_profitto", commissione_bp=2500,
                                    capitale_minimo_cents=100_000, rendimento_stimato_bp=300, priorita=10),
        "gestito": st.aggiungi_servizio("gestito", "Conto Gestito", "percentuale_profitto",
                                        commissione_bp=3000, capitale_minimo_cents=500_000,
                                        rendimento_stimato_bp=250, priorita=20),
        "segnali": st.aggiungi_servizio("segnali", "Segnali VIP", "fisso_mensile",
                                        commissione_fissa_cents=9_900, priorita=30),
    }


def cliente_contento(st: CRMStore, srv: Dict[str, int], nome: str = "Mario Rossi",
                     telefono: str = "+390000000001", profitto_maggio: int = 150_000,
                     consenso: bool = True) -> Tuple[int, int]:
    """Cliente in Copy Oro dal 1° aprile: 20.000 € di capitale, una commissione pagata,
    `profitto_maggio` di profitto nel mese chiuso precedente (maggio 2026)."""
    cid = st.aggiungi_cliente(nome, telefono=telefono, consenso_marketing=consenso)
    pid = st.apri_posizione(cid, srv["oro"], data="2026-04-01")
    st.registra_movimento(pid, "deposito", 2_000_000, data="2026-04-01")
    st.registra_movimento(pid, "profitto", 80_000, data="2026-04-28")
    st.registra_movimento(pid, "commissione", 20_000, data="2026-04-30")
    st.registra_movimento(pid, "profitto", profitto_maggio, data="2026-05-28")
    return cid, pid


def dati(st: CRMStore, giorno: Optional[date] = None) -> analisi.Dati:
    foto = st.fotografia()
    assert foto is not None
    return analisi.costruisci(foto, giorno or st.oggi())


# ---------------------------------------------------------------------- importi e formati


@pytest.mark.parametrize("testo,cents", [
    ("1234", 123_400), ("1234,5", 123_450), ("1.234,56", 123_456), ("1234.56", 123_456),
    ("1,234.56", 123_456), ("€ 1.234", 123_400), ("1.234.567", 123_456_700), ("0,01", 1),
    ("12.5", 1_250), (" 99 ", 9_900), ("1 234,00", 123_400), (1500, 150_000), ("10.000", 1_000_000),
])
def test_parse_importo_valido(testo: Any, cents: int) -> None:
    assert parse_importo(testo) == cents


@pytest.mark.parametrize("testo", ["", "-5", "+5", "1,2,3", "1.2.3", "1,234", "abc", "0", "0,00",
                                   "1,234,567.8.9", "1e5", "1.234,567", True, 1.5, None,
                                   "999999999999"])
def test_parse_importo_rifiuta(testo: Any) -> None:
    # «1,234» è ambiguo (virgola decimale con 3 cifre): rifiutato invece di indovinare
    with pytest.raises(ErroreCRM):
        parse_importo(testo)


def test_parse_percentuale() -> None:
    assert parse_percentuale_bp("25") == 2500
    assert parse_percentuale_bp("2,5%") == 250
    assert parse_percentuale_bp("0.75") == 75
    assert parse_percentuale_bp("") == 0
    for male in ("abc", "1,234", "-3", "100000"):
        with pytest.raises(ErroreCRM):
            parse_percentuale_bp(male)


def test_formati_euro() -> None:
    assert formatta_euro(123_456) == "1.234,56 €"
    assert formatta_euro(-5) == "−0,05 €"
    assert formatta_euro(100, segno=True) == "+1,00 €"
    assert formatta_euro_tondo(123_450) == "1.235 €"
    assert formatta_euro_tondo(99) == "1 €"
    assert analisi.formatta_bp(235) == "2,35%"
    assert analisi.formatta_bp(-50) == "−0,50%"


@pytest.mark.parametrize("ingresso,uscita", [
    ("333 123 4567", "+393331234567"), ("+39 333-123.4567", "+393331234567"),
    ("0039 3331234567", "+393331234567"), ("+44 20 7946 0000", "+442079460000"), ("", None),
])
def test_normalizza_telefono(ingresso: str, uscita: Optional[str]) -> None:
    assert normalizza_telefono(ingresso) == uscita


@pytest.mark.parametrize("male", ["abc", "+12", "+1234567890123456", "33x", "000 000 0001"])
def test_normalizza_telefono_rifiuta(male: str) -> None:
    with pytest.raises(ErroreCRM):
        normalizza_telefono(male)


def test_div_tonda_mezzo_in_su() -> None:
    assert analisi.div_tonda(5, 10) == 1
    assert analisi.div_tonda(4, 10) == 0
    assert analisi.div_tonda(-5, 10) == -1
    with pytest.raises(ValueError):
        analisi.div_tonda(1, 0)


# ---------------------------------------------------------------------- store


def test_registro_movimenti_immutabile_a_livello_db(st: CRMStore) -> None:
    srv = servizi_base(st)
    _, pid = cliente_contento(st, srv)
    con = sqlite3.connect(st.db_path)
    with pytest.raises(sqlite3.DatabaseError, match="immutabile"):
        con.execute("UPDATE crm_movimenti SET importo_cents = 1")
    with pytest.raises(sqlite3.DatabaseError, match="immutabile"):
        con.execute("DELETE FROM crm_movimenti")
    with pytest.raises(sqlite3.DatabaseError, match="immutabile"):
        con.execute("DELETE FROM crm_eventi")
    with pytest.raises(sqlite3.DatabaseError, match="immutabile"):
        con.execute("UPDATE crm_eventi SET descrizione = 'x'")
    con.close()


def test_storno_annulla_e_non_si_ripete(st: CRMStore) -> None:
    srv = servizi_base(st)
    cid, pid = cliente_contento(st, srv)
    sbagliato = st.registra_movimento(pid, "profitto", 999_999, data="2026-05-29")
    assert analisi.metriche_cliente(dati(st), cid).profitto_totale_cents == 80_000 + 150_000 + 999_999
    storno = st.storna_movimento(sbagliato)
    assert analisi.metriche_cliente(dati(st), cid).profitto_totale_cents == 230_000
    with pytest.raises(ErroreCRM, match="già stato stornato"):
        st.storna_movimento(sbagliato)
    with pytest.raises(ErroreCRM, match="già uno storno"):
        st.storna_movimento(storno)
    righe = {m["id"]: m for m in st.movimenti(cid)}
    assert righe[sbagliato]["stornato"] == 1 and righe[storno]["storno_di"] == sbagliato


def test_movimenti_validati(st: CRMStore) -> None:
    srv = servizi_base(st)
    _, pid = cliente_contento(st, srv)
    with pytest.raises(ErroreCRM, match="futuro"):
        st.registra_movimento(pid, "profitto", 100, data="2026-06-21")
    with pytest.raises(ErroreCRM):
        st.registra_movimento(pid, "regalo", 100)
    with pytest.raises(ErroreCRM):
        st.registra_movimento(pid, "profitto", 0)
    with pytest.raises(ErroreCRM, match="inesistente"):
        st.registra_movimento(9999, "profitto", 100)
    with pytest.raises(ErroreCRM, match="inesistente"):
        st.registra_movimento(pid, "profitto", 100, data="2026-02-30")


def test_clienti_unicita_e_validazioni(st: CRMStore) -> None:
    st.aggiungi_cliente("Anna", telefono="333 000 0001")
    with pytest.raises(ErroreCRM, match="stesso numero|già un cliente"):
        st.aggiungi_cliente("Anna bis", telefono="+393330000001")
    with pytest.raises(ErroreCRM):
        st.aggiungi_cliente("  ")
    with pytest.raises(ErroreCRM, match="email"):
        st.aggiungi_cliente("Bea", email="non-una-mail")
    with pytest.raises(ErroreCRM, match="caratteri non ammessi"):
        st.aggiungi_cliente("Ca\x00rlo")


def test_consenso_e_stop_tracciati(st: CRMStore) -> None:
    cid = st.aggiungi_cliente("Anna", telefono="+390000000002")
    st.aggiorna_cliente(cid, consenso_marketing=True)
    c = st.cliente(cid)
    assert c is not None and c["consenso_marketing"] == 1 and c["consenso_il"]
    st.aggiorna_cliente(cid, opt_out=True)
    c = st.cliente(cid)
    assert c is not None and c["opt_out"] == 1 and c["opt_out_il"]
    testi = [e["descrizione"] for e in st.eventi(cid)]
    assert any("STOP" in t for t in testi) and any("consenso marketing DATO" in t for t in testi)
    with pytest.raises(ErroreCRM, match="non modificabile"):
        st.aggiorna_cliente(cid, contatto_id=5)
    with pytest.raises(ErroreCRM, match="se stesso"):
        st.aggiorna_cliente(cid, presentato_da=cid)


def test_posizione_unica_e_riapribile(st: CRMStore) -> None:
    srv = servizi_base(st)
    cid = st.aggiungi_cliente("Anna")
    pid = st.apri_posizione(cid, srv["oro"], data="2026-01-01")
    with pytest.raises(ErroreCRM, match="già in questo servizio"):
        st.apri_posizione(cid, srv["oro"])
    st.cambia_stato_posizione(pid, "chiusa")
    assert st.apri_posizione(cid, srv["oro"]) == pid
    assert st.posizioni(cid)[0]["stato"] == "attiva"


def test_servizio_validazioni(st: CRMStore) -> None:
    servizi_base(st)
    with pytest.raises(ErroreCRM, match="già un servizio"):
        st.aggiungi_servizio("oro", "Altro", "fisso_mensile")
    with pytest.raises(ErroreCRM, match="codice"):
        st.aggiungi_servizio("Con Spazi", "X", "fisso_mensile")
    with pytest.raises(ErroreCRM, match="modello"):
        st.aggiungi_servizio("x", "X", "a_caso")
    sid = st.servizi()[0]["id"]
    st.aggiorna_servizio(sid, attivo=False, commissione_bp=1000)
    assert [s for s in st.servizi() if s["id"] == sid][0]["commissione_bp"] == 1000
    assert sid not in [s["id"] for s in st.servizi(solo_attivi=True)]
    with pytest.raises(ErroreCRM, match="non modificabile"):
        st.aggiorna_servizio(sid, codice="nuovo")


def test_proposte_transizioni_e_doppioni(st: CRMStore) -> None:
    # col consenso: l'invio lo ricontrolla dentro la transazione (V-2 bot #381)
    cid = st.aggiungi_cliente("Anna", telefono="+390000000003", consenso_marketing=True)
    pid = st.crea_proposta(cid, "referral", "cliente:1", "motivo", "messaggio")
    assert pid is not None
    assert st.crea_proposta(cid, "referral", "cliente:1", "motivo", "altro") is None
    with pytest.raises(ErroreCRM, match="non ammesso"):
        st.transiziona_proposta(pid, "accettata")
    p = st.transiziona_proposta(pid, "inviata", messaggio="testo corretto")
    # anche dallo store (non solo dal server) il testo corretto riceve la riga STOP (V-2 bot #381)
    assert p["messaggio"].startswith("testo corretto") and p["messaggio"].endswith(messaggi.RIGA_STOP)
    assert p["inviata_il"] and p["canale"] == "whatsapp"
    with pytest.raises(ErroreCRM, match="prima dell'invio"):
        st.transiziona_proposta(pid, "rifiutata", messaggio="no")
    st.transiziona_proposta(pid, "rifiutata")
    with pytest.raises(ErroreCRM, match="non ammesso"):
        st.transiziona_proposta(pid, "accettata")
    # chiusa la prima, la stessa chiave si può riaprire
    assert st.crea_proposta(cid, "referral", "cliente:1", "motivo", "messaggio") is not None


def test_letture_non_sollevano_su_db_rotto(tmp_path: Path) -> None:
    cartella = tmp_path / "non_un_file.db"
    cartella.mkdir()
    s = CRMStore(cartella)
    assert not s.available
    assert s.fotografia() is None
    assert s.clienti() == [] and s.servizi() == [] and s.eventi() == []
    esito = motore.scansiona(s, regole=REGOLE)
    assert esito.errore == "database non disponibile"
    with pytest.raises(ErroreCRM, match="database non disponibile"):
        s.aggiungi_cliente("Anna")


# ---------------------------------------------------------------------- analisi


def test_conti_esatti_e_movimenti_esclusi(st: CRMStore, orologio: Orologio) -> None:
    srv = servizi_base(st)
    cid, pid = cliente_contento(st, srv)
    st.registra_movimento(pid, "prelievo", 500_000, data="2026-06-01")
    st.registra_movimento(pid, "perdita", 30_000, data="2026-06-10")
    st.registra_movimento(pid, "commissione", 37_500, data="2026-06-01")
    d = dati(st)
    m = analisi.metriche_cliente(d, cid)
    assert m.capitale_cents == 1_500_000
    assert m.profitto_mese_cents == -30_000
    assert m.profitto_mese_prec_cents == 150_000
    assert m.profitto_totale_cents == 200_000
    assert m.commissioni_totali_cents == 57_500 and m.pagamenti == 2
    # un movimento successivo al giorno di analisi non conta
    vecchio = analisi.costruisci(st.fotografia() or {}, date(2026, 5, 1))
    assert analisi.metriche_cliente(vecchio, cid).profitto_totale_cents == 80_000


def test_roi_e_commissioni_stimate(st: CRMStore) -> None:
    srv = servizi_base(st)
    cid, pid = cliente_contento(st, srv)
    d = dati(st)
    pos = d.posizioni[pid]
    # mesi chiusi: mar (niente), apr 800 €, mag 1500 € → 2300 € / (20.000 € × 3) = 383 bp
    assert analisi.roi_posizione_bp(pos, "2026-06") == 383
    assert analisi.roi_servizio_bp(d, srv["oro"]) == 383
    assert analisi.roi_atteso_bp(d, srv["gestito"]) == (250, "stimato")
    s = d.servizi
    assert analisi.commissione_stimata_cents(s[srv["oro"]], 1_000_000, 300) == 7_500
    assert analisi.commissione_stimata_cents(s[srv["oro"]], 1_000_000, -300) == 0
    assert analisi.commissione_stimata_cents(s[srv["segnali"]], 0, 0) == 9_900
    annua = {"modello_commissione": "percentuale_capitale_annua", "commissione_bp": 200,
             "commissione_fissa_cents": 0}
    assert analisi.commissione_stimata_cents(annua, 1_200_000, 0) == 2_000


def test_affinita_tra_servizi(st: CRMStore) -> None:
    srv = servizi_base(st)
    for i in range(4):
        cid = st.aggiungi_cliente(f"C{i}")
        st.apri_posizione(cid, srv["oro"])
        if i < 3:
            st.apri_posizione(cid, srv["segnali"])
    aff = analisi.affinita_bp(dati(st))
    assert aff[(srv["oro"], srv["segnali"])] == 7_500
    assert aff[(srv["segnali"], srv["oro"])] == 10_000


def test_panoramica_numeri(st: CRMStore) -> None:
    srv = servizi_base(st)
    cid, _ = cliente_contento(st, srv)
    altro = st.aggiungi_cliente("Luca", telefono="+390000000009")
    st.apri_posizione(altro, srv["segnali"])
    st.aggiorna_cliente(altro, stato="perso")
    p = analisi.panoramica(dati(st))
    k = p["kpi"]
    assert k["clienti_attivi"] == 1 and k["clienti_totali"] == 2
    assert k["capitale_totale_cents"] == 2_000_000
    assert k["commissioni_totali_cents"] == 20_000
    assert p["serie"]["mesi"][-1] == "2026-06" and len(p["serie"]["mesi"]) == 12
    assert p["serie"]["commissioni_cents"][-3] == 20_000  # aprile
    riga = [c for c in p["clienti"] if c["id"] == cid][0]
    assert riga["celle"][str(srv["oro"])]["capitale_cents"] == 2_000_000
    json.dumps(p)  # serializzabile


# ---------------------------------------------------------------------- motore


def test_motore_propone_nuovo_servizio(st: CRMStore) -> None:
    srv = servizi_base(st)
    cid, _ = cliente_contento(st, srv)
    esito = motore.scansiona(st, regole=REGOLE)
    assert len(esito.create) == 1
    p = st.proposta(esito.create[0])
    assert p is not None and p["tipo"] == "cross_sell" and p["stato"] == "da_approvare"
    assert p["livello"] == 1 and p["chiave"] == f"cliente:{cid}"
    # Conto Gestito: 10.000 € (metà del suo capitale) × 2,5% stimato × 30% = 75 € < 99 € fissi
    assert p["servizio_id"] == srv["segnali"] and p["valore_stimato_cents"] == 9_900
    msg = p["messaggio"]
    assert msg.startswith("Ciao Mario!") and "a maggio con Copy Oro hai chiuso a +1.500 €" in msg
    assert messaggi.RIGA_STOP in msg and messaggi.NOTA_RISCHIO_DEFAULT in msg
    # idempotente: la seconda scansione non crea doppioni
    assert motore.scansiona(st, regole=REGOLE).create == []
    assert len(st.proposte()) == 1


@pytest.mark.parametrize("modifica,motivo", [
    ({"opt_out": True}, "STOP"), ({"consenso_marketing": False}, "consenso"),
    ({"telefono": None}, "numero"), ({"stato": "in_pausa"}, "non attivo"),
])
def test_motore_rispetta_i_divieti(st: CRMStore, modifica: Dict[str, Any], motivo: str) -> None:
    srv = servizi_base(st)
    cid, _ = cliente_contento(st, srv)
    st.aggiorna_cliente(cid, **modifica)
    esito = motore.scansiona(st, regole=REGOLE)
    assert esito.create == [] and motivo in esito.esclusi[cid]


def test_motore_aspetta_il_primo_pagamento_e_la_soglia(st: CRMStore) -> None:
    srv = servizi_base(st)
    nuovo = st.aggiungi_cliente("Nuovo", telefono="+390000000004", consenso_marketing=True)
    pid = st.apri_posizione(nuovo, srv["oro"], data="2026-05-01")
    st.registra_movimento(pid, "deposito", 1_000_000, data="2026-05-01")
    st.registra_movimento(pid, "profitto", 500_000, data="2026-05-28")
    sotto, _ = cliente_contento(st, srv, nome="Sotto", telefono="+390000000005", profitto_maggio=99_999)
    giusto, _ = cliente_contento(st, srv, nome="Giusto", telefono="+390000000006", profitto_maggio=100_000)
    esito = motore.scansiona(st, regole=REGOLE)
    assert "prima commissione" in esito.esclusi[nuovo]
    assert "sotto la soglia" in esito.esclusi[sotto]
    assert len(esito.create) == 1 and st.proposta(esito.create[0])["cliente_id"] == giusto  # type: ignore[index]


def test_dopo_un_no_al_servizio_propone_aumento_di_capitale(st: CRMStore, orologio: Orologio) -> None:
    srv = servizi_base(st)
    cid, pid = cliente_contento(st, srv)
    prima = motore.scansiona(st, regole=REGOLE).create[0]
    st.transiziona_proposta(prima, "inviata")
    orologio.avanti(2)
    st.transiziona_proposta(prima, "rifiutata")
    orologio.avanti(6)  # 8 giorni dall'invio: pausa di 7 superata, sempre giugno
    esito = motore.scansiona(st, regole=REGOLE)
    p = st.proposta(esito.create[0])
    assert p is not None and p["tipo"] == "aumento_capitale" and p["posizione_id"] == pid
    assert p["livello"] == 2  # un no negli ultimi 90 giorni → più diretto
    assert "10.000 €" in p["messaggio"] and "Copy Oro" in p["messaggio"]
    # 50% di 20.000 € = 10.000 € × 3,83% × 25% = 95,75 €
    assert p["valore_stimato_cents"] == 9_575
    assert "ha detto no" in p["motivo"]


def test_pausa_e_tetto_dei_messaggi(st: CRMStore, orologio: Orologio) -> None:
    srv = servizi_base(st)
    cid, _ = cliente_contento(st, srv)
    p1 = motore.scansiona(st, regole=REGOLE).create[0]
    st.transiziona_proposta(p1, "inviata")
    st.transiziona_proposta(p1, "accettata")
    orologio.avanti(3)
    esito = motore.scansiona(st, regole=REGOLE)
    assert esito.create == [] and "pausa minima" in esito.esclusi[cid]
    stretto = motore.Regole(pausa_giorni=1, max_messaggi_30g=1)
    esito = motore.scansiona(st, regole=stretto)
    assert esito.create == [] and "messaggi negli ultimi 30 giorni" in esito.esclusi[cid]


def test_accettato_da_poco_chiede_una_presentazione(st: CRMStore, orologio: Orologio) -> None:
    srv = servizi_base(st)
    cid, _ = cliente_contento(st, srv)
    p1 = motore.scansiona(st, regole=REGOLE).create[0]
    st.transiziona_proposta(p1, "inviata")
    st.transiziona_proposta(p1, "accettata")
    st.apri_posizione(cid, srv["segnali"])
    st.registra_movimento(st.posizioni(cid)[-1]["id"], "commissione", 9_900, data="2026-06-20")
    orologio.avanti(8)
    p = st.proposta(motore.scansiona(st, regole=REGOLE).create[0])
    assert p is not None and p["tipo"] == "referral" and "presenti" in p["messaggio"]


def test_senza_risposta_e_superata(st: CRMStore, orologio: Orologio) -> None:
    srv = servizi_base(st)
    a, _ = cliente_contento(st, srv)
    b, _ = cliente_contento(st, srv, nome="Bea", telefono="+390000000007")
    pa, pb = motore.scansiona(st, regole=REGOLE).create
    st.transiziona_proposta(pa, "inviata")
    st.aggiorna_cliente(b, opt_out=True)
    orologio.avanti(5)
    esito = motore.scansiona(st, regole=REGOLE)
    assert esito.senza_risposta == [pa] and esito.superate == [pb]
    assert st.proposta(pa)["stato"] == "senza_risposta"  # type: ignore[index]
    orologio.avanti(3)
    nuova = st.proposta(motore.scansiona(st, regole=REGOLE).create[0])
    assert nuova is not None and nuova["cliente_id"] == a and nuova["livello"] == 2


def test_una_sola_proposta_aperta_per_cliente_anche_in_concorrenza(st: CRMStore) -> None:
    srv = servizi_base(st)
    cid, _ = cliente_contento(st, srv)
    risultati: List[Optional[int]] = []

    def scan() -> None:
        risultati.extend(motore.scansiona(CRMStore(st.db_path, orologio=st._orologio),
                                          regole=REGOLE).create)
    fili = [threading.Thread(target=scan) for _ in range(4)]
    for f in fili:
        f.start()
    for f in fili:
        f.join()
    aperte = [p for p in st.proposte(cid) if p["stato"] == "da_approvare"]
    assert len(aperte) == 1 and len(risultati) == 1


def test_spiega_a_parole(st: CRMStore) -> None:
    srv = servizi_base(st)
    cid, _ = cliente_contento(st, srv)
    assert motore.spiega(st, cid, regole=REGOLE).startswith("Proposta pronta (cross_sell")
    assert motore.spiega(st, 999, regole=REGOLE) == "cliente inesistente"


def test_regole_da_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("GAS_CRM_SOGLIA_EURO", "2500")
    monkeypatch.setenv("GAS_CRM_PAUSA_GIORNI", "zero")
    monkeypatch.setenv("GAS_CRM_MAX_MESSAGGI_30G", "999")
    r = motore.Regole.da_env()
    # valori sbagliati → i default (mensili, decisione dell'operatore 2026-11-17)
    assert r.soglia_cents == 250_000 and r.pausa_giorni == 30 and r.max_messaggi_30g == 1


# ---------------------------------------------------------------------- messaggi


def test_messaggi_tutti_i_tipi_e_livelli(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("GAS_CRM_NOTA_RISCHIO", raising=False)
    for tipo in ("cross_sell", "aumento_capitale", "referral"):
        for liv in (0, 1, 2, 3, 9):
            t = messaggi.componi(tipo, liv, "Anna Verdi", "ottobre 2026", 123_456,
                                 servizio_nuovo="B", servizio_attuale="A", aumento_cents=500_000)
            assert "{" not in t and "Anna" in t and t.endswith(messaggi.RIGA_STOP)
            minuscolo = t.lower()
            for vietata in ("garantit", "sicuro al 100", "ultimi posti", "solo oggi"):
                if vietata == "garantit":
                    minuscolo = minuscolo.replace(messaggi.NOTA_RISCHIO_DEFAULT.lower(), "")
                assert vietata not in minuscolo
    assert "sei già a +1.235 €" in messaggi.componi("cross_sell", 1, "A", "giugno 2026", 123_456,
                                                    mese_in_corso=True)
    assert "questo mese" in messaggi.componi("referral", 1, "A", "giugno 2026", 1, mese_in_corso=True)
    assert messaggi.periodo("aprile 2026", False) == "ad aprile"
    assert messaggi.periodo("maggio 2026", False) == "a maggio"
    monkeypatch.setenv("GAS_CRM_NOTA_RISCHIO", "")
    assert messaggi.NOTA_RISCHIO_DEFAULT not in messaggi.componi("referral", 1, "A", "maggio", 1)
    with pytest.raises(KeyError):
        messaggi.componi("spam", 1, "A", "maggio", 1)


def test_link_whatsapp() -> None:
    link = messaggi.link_whatsapp("+390000000001", "Ciao & benvenuto\nSTOP?")
    assert link == "https://wa.me/390000000001?text=Ciao%20%26%20benvenuto%0ASTOP%3F"
    assert messaggi.link_whatsapp(None, "x") is None
    assert messaggi.link_whatsapp("3331234567", "x") is None
    assert messaggi.link_whatsapp("+39abc", "x") is None


# ---------------------------------------------------------------------- server

TOKEN = "token-di-prova-lungo-123456"


class Client:
    def __init__(self, porta: int) -> None:
        self.porta = porta
        self.cookie = ""

    def richiesta(self, metodo: str, percorso: str, corpo: Optional[Any] = None,
                  intestazioni: Optional[Dict[str, str]] = None,
                  grezzo: Optional[bytes] = None) -> Tuple[int, Dict[str, str], Any]:
        con = http.client.HTTPConnection("127.0.0.1", self.porta, timeout=10)
        h = {"Host": f"127.0.0.1:{self.porta}"}
        if self.cookie:
            h["Cookie"] = self.cookie
        dati = grezzo
        if corpo is not None:
            dati = json.dumps(corpo).encode()
            h["Content-Type"] = "application/json"
            h["X-Gas-CRM"] = "1"
        h.update(intestazioni or {})
        con.request(metodo, percorso, body=dati, headers=h)
        r = con.getresponse()
        testo = r.read()
        head = {k.lower(): v for k, v in r.getheaders()}
        con.close()
        if "set-cookie" in head:
            self.cookie = head["set-cookie"].split(";", 1)[0]
        try:
            return r.status, head, json.loads(testo.decode())
        except (ValueError, UnicodeDecodeError):
            return r.status, head, testo

    def post(self, percorso: str, corpo: Any, **kw: Any) -> Tuple[int, Dict[str, str], Any]:
        return self.richiesta("POST", percorso, corpo, **kw)

    def get(self, percorso: str, **kw: Any) -> Tuple[int, Dict[str, str], Any]:
        return self.richiesta("GET", percorso, **kw)


@pytest.fixture
def avviato(st: CRMStore):
    inviati: List[str] = []
    stato = server.Stato(st, TOKEN, regole=REGOLE, avvisa=lambda t: (inviati.append(t) or (True, "")))
    srv = server.crea_server(stato, "127.0.0.1", 0)
    filo = threading.Thread(target=srv.serve_forever, kwargs={"poll_interval": 0.05}, daemon=True)
    filo.start()
    yield stato, Client(srv.server_address[1]), inviati
    stato.stop.set()
    with stato.cambio:
        stato.cambio.notify_all()
    srv.shutdown()
    srv.server_close()


def test_bind_solo_locale(st: CRMStore) -> None:
    stato = server.Stato(st, TOKEN, regole=REGOLE)
    for host in ("0.0.0.0", "192.168.1.10", "example.com", "::1", "127.0.0.1.nip.io"):  # gasmerge-ip-ok
        with pytest.raises(ValueError):
            server.crea_server(stato, host, 0)
    assert server.bind_locale("localhost") and server.bind_locale("127.0.0.1")


def test_token_da_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("GAS_CRM_TOKEN", "corto")
    assert server.token_da_env() is None
    monkeypatch.setenv("GAS_CRM_TOKEN", " " + TOKEN + " ")
    assert server.token_da_env() == TOKEN
    assert not server.token_ok("", "") and not server.token_ok("a", "b") and server.token_ok("a", "a")


def test_server_pagine_e_intestazioni(avviato) -> None:
    _, c, _ = avviato
    for percorso in ("/", "/app.js", "/app.css", "/favicon.svg"):
        codice, h, _ = c.get(percorso)
        assert codice == 200
        assert "script-src 'self'" in h["content-security-policy"]
        assert "unsafe-inline" not in h["content-security-policy"]
        assert h["x-content-type-options"] == "nosniff"
    assert c.get("/../store.py")[0] == 404
    assert c.get("/api/stato")[0] == 401
    assert c.get("/api/sessione")[2] == {"autenticato": False, "demo": False}


def test_server_accesso_e_blocco(avviato) -> None:
    stato, c, _ = avviato
    assert c.post("/api/login", {"token": "sbagliato"})[0] == 401
    assert c.post("/api/login", {"token": TOKEN}, intestazioni={"X-Gas-CRM": "0"})[0] == 403
    codice, h, _ = c.post("/api/login", {"token": TOKEN})
    assert codice == 200 and "HttpOnly" in h["set-cookie"] and "SameSite=Strict" in h["set-cookie"]
    assert c.get("/api/stato")[0] == 200
    assert c.get("/api/sessione")[2]["autenticato"] is True
    # bearer per le integrazioni
    b = Client(c.porta)
    assert b.get("/api/stato", intestazioni={"Authorization": f"Bearer {TOKEN}"})[0] == 200
    # dieci tentativi sbagliati: l'IP viene bloccato, anche col token giusto
    x = Client(c.porta)
    for _ in range(server.MAX_FALLITI):
        x.post("/api/login", {"token": "no"})
    assert x.post("/api/login", {"token": TOKEN})[0] == 429
    stato.bloccati.clear()
    assert c.post("/api/logout", {})[0] == 200
    assert c.get("/api/stato")[0] == 401


def test_server_difese_csrf_host_corpo(avviato) -> None:
    _, c, _ = avviato
    c.post("/api/login", {"token": TOKEN})
    assert c.post("/api/clienti", {"nome": "X"}, intestazioni={"Origin": "http://evil.example"})[0] == 403
    assert c.post("/api/clienti", {"nome": "X"}, intestazioni={"Content-Type": "text/plain"})[0] == 403
    assert c.get("/api/stato", intestazioni={"Host": "evil.example:8770"})[0] == 403
    assert c.post("/api/clienti", None, grezzo=b"{rotto", intestazioni={
        "Content-Type": "application/json", "X-Gas-CRM": "1"})[0] == 400
    assert c.post("/api/clienti", None, grezzo=b"[1]", intestazioni={
        "Content-Type": "application/json", "X-Gas-CRM": "1"})[0] == 400
    grande = json.dumps({"nome": "x" * (server.CORPO_MAX + 10)}).encode()
    assert c.post("/api/clienti", None, grezzo=grande, intestazioni={
        "Content-Type": "application/json", "X-Gas-CRM": "1"})[0] == 413
    assert c.post("/api/inesistente", {})[0] == 404


def test_server_flusso_completo(avviato) -> None:
    stato, c, inviati = avviato
    c.post("/api/login", {"token": TOKEN})
    codice, _, r = c.post("/api/servizi", {"codice": "oro", "nome": "Copy Oro",
                                           "modello_commissione": "percentuale_profitto",
                                           "commissione_pct": "25", "capitale_minimo": "1.000"})
    assert codice == 200
    sid = r["risultato"]["id"]
    c.post("/api/servizi", {"codice": "segnali", "nome": "Segnali", "modello_commissione": "fisso_mensile",
                            "commissione_fissa": "99"})
    cid = c.post("/api/clienti", {"nome": "Mario Rossi", "telefono": "+39 000 000 0001",
                                  "consenso_marketing": True})[2]["risultato"]["id"]
    pid = c.post("/api/posizioni", {"cliente_id": cid, "servizio_id": sid,
                                    "capitale_iniziale": "20.000", "data": "2026-04-01"})[2]["risultato"]["id"]
    for tipo, imp, giorno in (("profitto", "800", "2026-04-28"), ("commissione", "200", "2026-04-30"),
                              ("profitto", "1.500,00", "2026-05-28")):
        assert c.post("/api/movimenti", {"posizione_id": pid, "tipo": tipo, "importo": imp,
                                         "data": giorno})[0] == 200
    codice, _, err = c.post("/api/movimenti", {"posizione_id": pid, "tipo": "profitto", "importo": "1,234"})
    assert codice == 400 and "importo" in err["errore"]
    stato_dati = c.get("/api/stato")[2]
    assert stato_dati["kpi"]["capitale_totale_cents"] == 2_000_000
    assert stato_dati["kpi"]["commissioni_totali_cents"] == 20_000
    # scansione a mano → proposta con link wa.me
    esito = c.post("/api/scansiona", {})[2]["risultato"]
    assert len(esito["create"]) == 1
    assert inviati and "1 nuove opportunità" in inviati[0] and "Mario" not in inviati[0]
    prop = c.get("/api/stato")[2]["proposte_aperte"][0]
    assert "link_whatsapp" not in prop  # il link nasce solo da «invia», dopo i controlli
    codice, _, r = c.post("/api/proposte/azione", {"id": prop["id"], "azione": "invia",
                                                  "messaggio": "Ciao Mario, testo mio"})
    assert codice == 200
    link = r["risultato"]["link_whatsapp"]
    assert link.startswith("https://wa.me/390000000001?text=Ciao%20Mario%2C%20testo%20mio")
    from urllib.parse import quote
    assert link.endswith(quote(messaggi.RIGA_STOP, safe=""))  # STOP rimessa (V-1 bot #381)
    assert c.post("/api/proposte/azione", {"id": prop["id"], "azione": "stop"})[0] == 200
    cli = c.get(f"/api/cliente?id={cid}")[2]
    assert cli["cliente"]["opt_out"] == 1
    assert cli["proposte"][0]["stato"] == "rifiutata"
    assert "STOP" in cli["spiegazione"]
    assert c.get("/api/cliente?id=999")[0] == 404
    assert c.get("/api/cliente?id=abc")[0] == 400
    # dopo lo STOP non si può più «inviare» niente a quel cliente
    st = stato.store
    altra = st.crea_proposta(cid, "referral", "manuale:1", "m", "testo")
    codice, _, err = c.post("/api/proposte/azione", {"id": altra, "azione": "invia"})
    assert codice == 400 and "STOP" in err["errore"]
    # storno via API
    mov = [m for m in cli["movimenti"] if m["tipo"] == "profitto"][0]
    assert c.post("/api/movimenti/storno", {"id": mov["id"]})[0] == 200
    assert c.post("/api/movimenti/storno", {"id": mov["id"]})[0] == 400
    assert c.post("/api/note", {"cliente_id": cid, "testo": "chiamato"})[0] == 200
    assert c.post("/api/lead/converti", {"contatto_id": 1})[0] == 400  # senza memoria collegata


def test_server_avviso_telegram_limitato(st: CRMStore) -> None:
    inviati: List[str] = []
    stato = server.Stato(st, TOKEN, regole=REGOLE, avvisa=lambda t: (inviati.append(t) or (True, "")))
    stato._avvisa_operatore(2, 12_345)
    stato._avvisa_operatore(3, 1)
    assert inviati == ["🎯 CRM Gas: 2 nuove opportunità da approvare (valore stimato ~123 €/mese "
                       "di commissioni). Aprile dalla dashboard."]
    demo = server.Stato(st, TOKEN, demo=True, avvisa=lambda t: (inviati.append(t) or (True, "")))
    demo._avvisa_operatore(1, 1)
    assert len(inviati) == 1


def test_server_tempo_reale_sse(avviato) -> None:
    stato, c, _ = avviato
    c.post("/api/login", {"token": TOKEN})
    con = http.client.HTTPConnection("127.0.0.1", c.porta, timeout=10)
    con.request("GET", "/api/stream", headers={"Host": f"127.0.0.1:{c.porta}", "Cookie": c.cookie})
    r = con.getresponse()
    assert r.status == 200 and r.getheader("Content-Type").startswith("text/event-stream")
    assert r.fp.readline().startswith(b"event: pronto")
    r.fp.readline()
    r.fp.readline()
    threading.Timer(0.2, stato.segnala_cambio).start()
    assert r.fp.readline().startswith(b"event: cambio")
    con.close()


def test_guardiano_vede_i_cambi_di_altri_processi(st: CRMStore) -> None:
    stato = server.Stato(st, TOKEN, regole=REGOLE, scan_minuti=60)
    filo = threading.Thread(target=server._guardiano, args=(stato,), daemon=True)
    filo.start()
    try:
        time.sleep(1.3)
        v0 = stato.versione
        CRMStore(st.db_path).aggiungi_cliente("Da un altro processo")
        limite = time.monotonic() + 5
        while stato.versione == v0 and time.monotonic() < limite:
            time.sleep(0.1)
        assert stato.versione > v0
        assert stato.ultima_scansione is not None
    finally:
        stato.stop.set()
        filo.join(timeout=5)


def test_demo_si_popola_e_non_sovrascrive(tmp_path: Path) -> None:
    from modules.crm.demo import popola
    s = CRMStore(tmp_path / "demo.db")
    n = popola(s, oggi=date.today())
    assert n == {"servizi": 5, "clienti": 26}
    assert all(c["telefono"].startswith("+39000000") for c in s.clienti())
    with pytest.raises(RuntimeError):
        popola(s)
    assert motore.scansiona(s, regole=REGOLE).errore is None


# ---------------------------------------------------------------------- review #803 (regressioni)


def _avvia_server(stato: "server.Stato"):
    srv = server.crea_server(stato, "127.0.0.1", 0)
    filo = threading.Thread(target=srv.serve_forever, kwargs={"poll_interval": 0.05}, daemon=True)
    filo.start()
    return srv


def _ferma(stato: "server.Stato", srv) -> None:
    stato.stop.set()
    with stato.cambio:
        stato.cambio.notify_all()
    srv.shutdown()
    srv.server_close()


def test_r803_1_dati_veri_la_dashboard_non_scrive_nel_file(tmp_path: Path) -> None:
    """Con la memoria di Gas collegata, leggere la dashboard non deve scrivere nel file
    (prima ogni GET /api/stato apriva un MemoryStore nuovo → rebuild FTS → scrittura →
    «cambio» → nuovo GET: un ciclo continuo)."""
    from modules.memory.store import MemoryStore
    db = tmp_path / ".gas_memory.db"
    mem = MemoryStore(db)
    lid = mem.upsert_contatto("lead-luigi", nome="Luigi", contatto="+390000000077")
    assert lid is not None and mem.update_stato_contatto(lid, "interessato")
    s = CRMStore(db)
    stato = server.Stato(s, TOKEN, regole=REGOLE, scan_minuti=60, memoria_db=db)
    srv = _avvia_server(stato)
    try:
        c = Client(srv.server_address[1])
        c.post("/api/login", {"token": TOKEN})
        sentinella = sqlite3.connect(db)
        v0 = sentinella.execute("PRAGMA data_version").fetchone()[0]
        for _ in range(3):
            codice, _, corpo = c.get("/api/stato")
            assert codice == 200 and [x["nome"] for x in corpo["lead_pronti"]] == ["Luigi"]
        assert sentinella.execute("PRAGMA data_version").fetchone()[0] == v0
        sentinella.close()
    finally:
        _ferma(stato, srv)


def test_r803_1_conversione_lead_tracciata_e_unica(tmp_path: Path) -> None:
    from modules.memory.store import MemoryStore
    db = tmp_path / ".gas_memory.db"
    mem = MemoryStore(db)
    lid = mem.upsert_contatto("lead-luigi", nome="Luigi", contatto="+39 000 000 0077")
    assert lid is not None and mem.update_stato_contatto(lid, "interessato")
    s = CRMStore(db)
    stato = server.Stato(s, TOKEN, regole=REGOLE, memoria_db=db)
    cid = stato.converti_lead(lid)
    cliente = s.cliente(cid)
    assert cliente is not None and cliente["telefono"] == "+390000000077"
    assert cliente["consenso_marketing"] == 0 and cliente["contatto_id"] == lid
    lead = mem.get_contatto(lid)
    assert lead is not None and lead["stato"] == "chiuso"
    assert any("cliente CRM" in e["descrizione"] for e in mem.diario_di_contatto(lid))
    with pytest.raises(ErroreCRM, match="già un cliente"):
        stato.converti_lead(lid)
    # vincolo nel DB, non solo il controllo prima dell'inserimento (R-803-5)
    with pytest.raises(ErroreCRM, match="già un cliente"):
        s.aggiungi_cliente("Doppione", contatto_id=lid)
    assert stato.lead_pronti() == []


def _codici(risposta: bytes) -> List[bytes]:
    """Codici di stato di tutte le risposte arrivate (anche attaccate al corpo precedente)."""
    import re
    return re.findall(rb"HTTP/1\.[01] (\d{3}) ", risposta)


def _risposte_su_un_socket(porta: int, dati: bytes) -> bytes:
    import socket
    s = socket.create_connection(("127.0.0.1", porta))
    s.sendall(dati)
    s.settimeout(1.5)
    letto = b""
    try:
        while True:
            pezzo = s.recv(65536)
            if not pezzo:
                break
            letto += pezzo
    except OSError:
        pass
    s.close()
    return letto


@pytest.mark.parametrize("caso", ["403_senza_header", "401_senza_accesso", "413_troppo_grande"])
def test_r803_2_corpo_non_letto_non_diventa_una_richiesta(avviato, caso: str) -> None:
    """Una risposta d'errore data SENZA leggere il corpo deve chiudere la connessione:
    altrimenti il corpo (scelto da una pagina estranea) viene eseguito come richiesta."""
    stato, c, _ = avviato
    nascosta = (f"POST /api/login HTTP/1.1\r\nHost: 127.0.0.1:{c.porta}\r\nX-Gas-CRM: 1\r\n"
                "Content-Type: application/json\r\nContent-Length: 15\r\n\r\n"
                '{"token":"bad"}').encode()
    righe = [f"POST /api/clienti HTTP/1.1", f"Host: 127.0.0.1:{c.porta}"]
    lunghezza = len(nascosta)
    if caso == "403_senza_header":
        righe += ["Origin: http://evil.example", "Content-Type: text/plain"]
    else:
        righe += ["Content-Type: application/json", "X-Gas-CRM: 1"]
    if caso == "413_troppo_grande":
        righe.append(f"Authorization: Bearer {TOKEN}")
        lunghezza = server.CORPO_MAX + 1
    righe.append(f"Content-Length: {lunghezza}")
    risposta = _risposte_su_un_socket(c.porta, ("\r\n".join(righe) + "\r\n\r\n").encode() + nascosta)
    stati = _codici(risposta)
    atteso = {"403_senza_header": b"403", "401_senza_accesso": b"401", "413_troppo_grande": b"413"}[caso]
    assert stati == [atteso]
    assert b"Connection: close" in risposta
    assert stato.falliti == {} and not stato.ip_bloccato("127.0.0.1")


def test_r803_2_la_connessione_resta_viva_quando_il_corpo_e_letto(avviato) -> None:
    _, c, _ = avviato
    corpo = b'{"token":"' + TOKEN.encode() + b'"}'
    una = (f"POST /api/login HTTP/1.1\r\nHost: 127.0.0.1:{c.porta}\r\nX-Gas-CRM: 1\r\n"
           f"Content-Type: application/json\r\nContent-Length: {len(corpo)}\r\n\r\n").encode() + corpo
    due = f"GET /api/sessione HTTP/1.1\r\nHost: 127.0.0.1:{c.porta}\r\nConnection: close\r\n\r\n".encode()
    risposta = _risposte_su_un_socket(c.porta, una + due)
    assert _codici(risposta) == [b"200", b"200"]


def test_r803_3_import_csv_tutto_o_niente(tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
                                          capsys: pytest.CaptureFixture) -> None:
    from modules.crm import __main__ as cli
    db = tmp_path / ".gas_memory.db"
    s = CRMStore(db)
    srv = servizi_base(s)
    cid = s.aggiungi_cliente("Anna", telefono="+390000000011")
    s.apri_posizione(cid, srv["oro"], data="2026-01-01")
    monkeypatch.setenv("GAS_CRM_DB", str(db))
    csv_male = tmp_path / "m.csv"
    csv_male.write_text("telefono;servizio;tipo;importo;data;nota\n"
                        "+390000000011;oro;deposito;1.000;2026-01-02;ok\n"
                        "+390000000011;oro;deposit;5;2026-01-03;tipo sbagliato\n"
                        "+390000000011;oro;profitto;5;2099-01-01;nel futuro\n", encoding="utf-8")
    assert cli.main(["import", str(csv_male)]) == 1
    uscita = capsys.readouterr().out
    assert "nessuna riga scritta" in uscita and "riga 3" in uscita and "riga 4" in uscita
    assert s.movimenti(cid) == []
    csv_buono = tmp_path / "b.csv"
    csv_buono.write_text("telefono;servizio;tipo;importo;data;nota\n"
                         "+390000000011;oro;deposito;1.000;2026-01-02;ok\n", encoding="utf-8")
    assert cli.main(["import", str(csv_buono)]) == 0
    assert [m["importo_cents"] for m in s.movimenti(cid)] == [100_000]
    rotto = tmp_path / "rotto.csv"
    rotto.write_bytes(b"\xff\xfe\x00rotto")
    assert cli.main(["import", str(rotto)]) == 1
    assert cli.main(["import", str(tmp_path / "manca.csv")]) == 1


def test_r803_3_lotto_di_movimenti_atomico(st: CRMStore) -> None:
    srv = servizi_base(st)
    cid, pid = cliente_contento(st, srv)
    prima = len(st.movimenti(cid))
    with pytest.raises(ErroreCRM) as err:
        st.registra_movimenti([(pid, "profitto", 100, "2026-06-01", None),
                               (pid, "profitto", 100, "2026-06-30", None)], fonte="import")
    assert "riga 2" in str(err.value)
    assert len(st.movimenti(cid)) == prima
    assert len(st.registra_movimenti([(pid, "profitto", 100, "2026-06-01", "a"),
                                      (pid, "perdita", 50, None, "b")], fonte="import")) == 2
    assert len(st.movimenti(cid)) == prima + 2


def test_r803_6_7_cifre_e_importi_ambigui() -> None:
    for male in ("³³³1234567", "+39٣٣٣1234567", "+3933312345６７"):
        with pytest.raises(ErroreCRM):
            normalizza_telefono(male)
    assert messaggi.link_whatsapp("+39³³³1234567", "x") is None
    for male in ("0.500", "0.050", "000.001", "0,500.25", "٣", "1.²³⁴"):
        with pytest.raises(ErroreCRM):
            parse_importo(male)
    assert parse_importo("0.50") == 50
    assert parse_importo("0,5") == 50
    with pytest.raises(ErroreCRM):
        parse_percentuale_bp("٣")


def test_r803_8_variabili_sbagliate_non_fanno_crashare(monkeypatch: pytest.MonkeyPatch) -> None:
    from modules.crm import __main__ as cli
    monkeypatch.setenv("GAS_CRM_PORT", "abc")
    monkeypatch.setenv("GAS_CRM_SCAN_MINUTI", "dieci")
    a = cli.parser().parse_args(["serve"])
    assert a.porta == 8770
    assert cli._env_int("GAS_CRM_SCAN_MINUTI", 10, 1, 1440) == 10


def test_r803_8_get_con_errore_imprevisto_risponde_500(avviato, monkeypatch: pytest.MonkeyPatch) -> None:
    _, c, _ = avviato
    c.post("/api/login", {"token": TOKEN})

    def rotta(*_a: Any, **_k: Any) -> Any:
        raise RuntimeError("boom")
    monkeypatch.setattr(analisi, "panoramica", rotta)
    codice, _, corpo = c.get("/api/stato")
    assert codice == 500 and "boom" not in json.dumps(corpo)


def test_r803_9_il_diario_del_crm_non_contiene_nomi(st: CRMStore) -> None:
    a = st.aggiungi_cliente("Mario Rossi", telefono="+390000000021")
    st.aggiungi_cliente("Luca Bianchi", telefono="+390000000022", presentato_da=a)
    testi = " ".join(e["descrizione"] for e in st.eventi(n=50))
    assert "Mario" not in testi and "Luca" not in testi and "0000000021" not in testi


def test_r803_11_niente_link_prima_dell_invio_e_stream_chiuso_al_logout(avviato) -> None:
    stato, c, _ = avviato
    st = stato.store
    srv = servizi_base(st)
    cliente_contento(st, srv)
    motore.scansiona(st, regole=REGOLE)
    c.post("/api/login", {"token": TOKEN})
    assert all("link_whatsapp" not in p for p in c.get("/api/stato")[2]["proposte_aperte"])
    con = http.client.HTTPConnection("127.0.0.1", c.porta, timeout=10)
    con.request("GET", "/api/stream", headers={"Host": f"127.0.0.1:{c.porta}", "Cookie": c.cookie})
    r = con.getresponse()
    assert r.fp.readline().startswith(b"event: pronto")
    r.fp.readline()
    r.fp.readline()
    c.post("/api/logout", {})
    resto = r.fp.read()  # il server chiude lo stream: read() torna invece di restare appeso
    assert b"event: cambio" not in resto
    con.close()


# ---------------------------------------------------------------------- verifica esterna PR #381


def test_v1_381_proposta_scartata_non_ricompare(st: CRMStore, orologio: Orologio) -> None:
    """Scartare una proposta deve fermare il motore su quel cliente per la pausa, e sullo
    stesso obiettivo per la pausa dopo un no (prima veniva ricreata alla scansione dopo)."""
    srv = servizi_base(st)
    cid, _ = cliente_contento(st, srv)
    p1 = motore.scansiona(st, regole=REGOLE).create[0]
    assert st.proposta(p1)["servizio_id"] == srv["segnali"]  # type: ignore[index]
    st.transiziona_proposta(p1, "scartata")
    esito = motore.scansiona(st, regole=REGOLE)
    assert esito.create == [] and "scartat" in esito.esclusi[cid]
    orologio.avanti(REGOLE.pausa_giorni + 1)  # sempre giugno: soglia ancora valida
    p2 = st.proposta(motore.scansiona(st, regole=REGOLE).create[0])
    assert p2 is not None and p2["cliente_id"] == cid
    assert p2["servizio_id"] != srv["segnali"]  # l'obiettivo scartato resta in pausa


def test_v2_381_movimenti_incoerenti_rifiutati(st: CRMStore) -> None:
    srv = servizi_base(st)
    cid, pid = cliente_contento(st, srv)  # posizione aperta il 2026-04-01, capitale 20.000 €
    with pytest.raises(ErroreCRM, match="capitale"):
        st.registra_movimento(pid, "prelievo", 2_000_001, data="2026-06-01")
    with pytest.raises(ErroreCRM, match="prima dell'apertura"):
        st.registra_movimento(pid, "deposito", 100, data="2026-03-31")
    with pytest.raises(ErroreCRM, match="prima dell'apertura"):
        st.registra_movimenti([(pid, "profitto", 100, "2026-05-01", None),
                               (pid, "profitto", 100, "0001-01-01", None)])
    st.registra_movimento(pid, "prelievo", 2_000_000, data="2026-06-01")  # tutto il capitale: ok
    primo_deposito = [m for m in st.movimenti(cid) if m["tipo"] == "deposito"][0]["id"]
    with pytest.raises(ErroreCRM, match="capitale"):
        st.storna_movimento(primo_deposito)  # lascerebbe il capitale negativo
    # nel lotto i prelievi vedono i depositi delle righe prima
    st.registra_movimenti([(pid, "deposito", 500, "2026-06-02", None),
                           (pid, "prelievo", 500, "2026-06-02", None)])
    with pytest.raises(ErroreCRM, match="capitale"):
        st.registra_movimenti([(pid, "deposito", 500, "2026-06-02", None),
                               (pid, "prelievo", 501, "2026-06-02", None)])
    assert analisi.metriche_cliente(dati(st), cid).capitale_cents == 0


def test_v1_bot_381_testo_corretto_tiene_stop_e_nota(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("GAS_CRM_NOTA_RISCHIO", raising=False)
    t = messaggi.completa_testo("  Ciao Anna, ti chiamo domani  ")
    assert t == ("Ciao Anna, ti chiamo domani\n\n" + messaggi.NOTA_RISCHIO_DEFAULT
                 + "\n\n" + messaggi.RIGA_STOP)
    assert messaggi.completa_testo(t) == t  # idempotente: niente doppioni
    monkeypatch.setenv("GAS_CRM_NOTA_RISCHIO", "")
    assert messaggi.completa_testo("Ciao") == "Ciao\n\n" + messaggi.RIGA_STOP


def test_v2_bot_381_stop_ricontrollato_nella_transazione_di_invio(st: CRMStore) -> None:
    srv = servizi_base(st)
    cid, _ = cliente_contento(st, srv)
    pid = motore.scansiona(st, regole=REGOLE).create[0]
    # lo STOP arriva DOPO il controllo del server ma prima della transizione: scrittura
    # diretta, come un'altra scheda o la riga di comando
    con = sqlite3.connect(st.db_path)
    con.execute("UPDATE crm_clienti SET opt_out = 1 WHERE id = ?", (cid,))
    con.commit()
    con.close()
    with pytest.raises(ErroreCRM, match="STOP"):
        st.transiziona_proposta(pid, "inviata")
    assert st.proposta(pid)["stato"] == "da_approvare"  # type: ignore[index]


# ---------------------------------------------------------------------- review #806 (riserve)


def _store_con_spia(st: CRMStore, prima_di: str, azione) -> CRMStore:
    """Store le cui connessioni eseguono `azione()` una volta, subito prima del primo
    comando SQL che inizia con `prima_di` (per forzare un intreccio concorrente)."""
    stato = {"fatto": False}

    class Spia(sqlite3.Connection):
        def execute(self, sql, *a):  # type: ignore[override]
            if not stato["fatto"] and sql.lstrip().startswith(prima_di):
                stato["fatto"] = True
                azione()
            return super().execute(sql, *a)

    spiato = CRMStore(st.db_path, orologio=st._orologio)

    def connetti() -> sqlite3.Connection:
        con = sqlite3.connect(str(spiato.db_path), timeout=10, factory=Spia)
        con.row_factory = sqlite3.Row
        con.execute("PRAGMA foreign_keys = ON")
        return con
    spiato._connect = connetti  # type: ignore[method-assign]
    return spiato


def test_r806_1_stop_concorrente_non_passa_tra_controllo_e_invio(st: CRMStore) -> None:
    srv = servizi_base(st)
    cid, _ = cliente_contento(st, srv)
    pid = motore.scansiona(st, regole=REGOLE).create[0]
    esito: Dict[str, Any] = {}

    def stop_da_un_altra_scheda() -> None:
        con = sqlite3.connect(st.db_path, timeout=0.3)
        try:
            con.execute("UPDATE crm_clienti SET opt_out = 1 WHERE id = ?", (cid,))
            con.commit()
            esito["stop"] = "scritto"
        except sqlite3.OperationalError:
            esito["stop"] = "in attesa del lucchetto"
        finally:
            con.close()
    spiato = _store_con_spia(st, "UPDATE crm_proposte", stop_da_un_altra_scheda)
    spiato.transiziona_proposta(pid, "inviata")
    # il controllo e l'invio sono UNA transazione: lo STOP arriva dopo, non in mezzo
    assert esito["stop"] == "in attesa del lucchetto"


def test_r806_1_prelievi_concorrenti_non_superano_il_capitale(st: CRMStore) -> None:
    srv = servizi_base(st)
    cid = st.aggiungi_cliente("Anna", telefono="+390000000031")
    pos = st.apri_posizione(cid, srv["oro"], data="2026-06-01")
    st.registra_movimento(pos, "deposito", 100_000, data="2026-06-01")
    errori: List[str] = []

    def secondo_prelievo() -> None:
        def corri() -> None:
            try:
                CRMStore(st.db_path, orologio=st._orologio).registra_movimento(
                    pos, "prelievo", 100_000, data="2026-06-02")
            except ErroreCRM as e:
                errori.append(str(e))
        filo = threading.Thread(target=corri)
        filo.start()
        secondo_prelievo.filo = filo  # type: ignore[attr-defined]
        time.sleep(0.3)  # il secondo fa in tempo a controllare il capitale, se può
    spiato = _store_con_spia(st, "INSERT INTO crm_movimenti", secondo_prelievo)
    spiato.registra_movimento(pos, "prelievo", 100_000, data="2026-06-02")
    secondo_prelievo.filo.join(timeout=15)  # type: ignore[attr-defined]
    assert errori and "capitale" in errori[0]
    assert analisi.metriche_cliente(dati(st), cid).capitale_cents == 0


def test_r806_2_apertura_anticipabile_per_caricare_lo_storico(st: CRMStore, avviato) -> None:
    srv = servizi_base(st)
    cid = st.aggiungi_cliente("Anna", telefono="+390000000032")
    pos = st.apri_posizione(cid, srv["oro"])  # aperta «oggi» per errore
    with pytest.raises(ErroreCRM, match="prima dell'apertura"):
        st.registra_movimento(pos, "deposito", 100, data="2026-01-02")
    st.anticipa_apertura(pos, "2026-01-01")
    st.registra_movimento(pos, "deposito", 100, data="2026-01-02")
    with pytest.raises(ErroreCRM, match="indietro"):
        st.anticipa_apertura(pos, "2026-02-01")  # in avanti escluderebbe lo storico
    with pytest.raises(ErroreCRM, match="futuro"):
        st.anticipa_apertura(pos, "2099-01-01")
    _, c, _ = avviato
    c.post("/api/login", {"token": TOKEN})
    assert c.post("/api/posizioni/apertura", {"id": pos, "data": "2025-12-01"})[0] == 200
    assert st.posizioni(cid)[0]["aperta_il"] == "2025-12-01"


def test_r806_3_testo_lungo_errore_chiaro(st: CRMStore, avviato) -> None:
    from modules.crm.store import TESTO_MAX
    srv = servizi_base(st)
    cliente_contento(st, srv)
    pid = motore.scansiona(st, regole=REGOLE).create[0]
    _, c, _ = avviato
    c.post("/api/login", {"token": TOKEN})
    codice, _, err = c.post("/api/proposte/azione",
                            {"id": pid, "azione": "invia", "messaggio": "x" * (TESTO_MAX - 20)})
    assert codice == 400 and "accorcialo" in err["errore"]


# ---------------------------------------------------------------------- decisioni del 17-11 (2° giro)


def test_default_mensili_e_follow_up_spegnibile(st: CRMStore, orologio: Orologio) -> None:
    mensili = motore.Regole()  # i default decisi dall'operatore: un messaggio al mese
    assert mensili.pausa_giorni == 30 and mensili.max_messaggi_30g == 1
    srv = servizi_base(st)
    cid, _ = cliente_contento(st, srv)
    p1 = motore.scansiona(st, regole=mensili).create[0]
    st.transiziona_proposta(p1, "inviata")
    st.transiziona_proposta(p1, "accettata")
    orologio.avanti(8)
    esito = motore.scansiona(st, regole=mensili)
    assert esito.create == [] and "pausa minima 30" in esito.esclusi[cid]
    st.aggiorna_cliente(cid, followup_attivo=False)
    orologio.avanti(25)
    esito = motore.scansiona(st, regole=mensili)
    assert esito.create == [] and "follow-up mensile spento" in esito.esclusi[cid]
    # a mano (spunta dell'operatore) si può ancora, perché le regole dure sono rispettate
    assert len(motore.prepara_selezionati(st, [cid], regole=mensili).create) == 1


def test_mai_a_chi_e_appena_entrato_ne_dopo_una_perdita(st: CRMStore) -> None:
    srv = servizi_base(st)
    nuovo = st.aggiungi_cliente("Nuovo", telefono="+390000000041", consenso_marketing=True)
    pid = st.apri_posizione(nuovo, srv["oro"], data="2026-06-05", capitale_iniziale_cents=1_000_000)
    st.registra_movimento(pid, "profitto", 150_000, data="2026-06-15")
    st.registra_movimento(pid, "commissione", 30_000, data="2026-06-16")
    in_perdita, pos = cliente_contento(st, srv, nome="Pina", telefono="+390000000042")
    st.registra_movimento(pos, "perdita", 10_000, data="2026-06-10")
    esito = motore.scansiona(st, regole=REGOLE)
    assert "cliente da 15 giorni" in esito.esclusi[nuovo]
    assert "in perdita" in esito.esclusi[in_perdita]
    assert esito.create == []


def test_servizi_da_consigliare_hanno_la_precedenza(st: CRMStore) -> None:
    srv = servizi_base(st)
    st.aggiorna_servizio(srv["gestito"], consigliato=True)
    cliente_contento(st, srv)
    p = st.proposta(motore.scansiona(st, regole=REGOLE).create[0])
    # senza il segno avrebbe proposto Segnali VIP (99 € fissi): ora solo il servizio consigliato
    assert p is not None and p["servizio_id"] == srv["gestito"]


def test_selezione_manuale_regole_dure_e_testo_neutro(st: CRMStore) -> None:
    srv = servizi_base(st)
    a, _ = cliente_contento(st, srv)
    senza_profitto = st.aggiungi_cliente("Ugo Neri", telefono="+390000000043", consenso_marketing=True)
    st.apri_posizione(senza_profitto, srv["oro"], data="2026-06-01", capitale_iniziale_cents=500_000)
    stop = st.aggiungi_cliente("Lia", telefono="+390000000044", consenso_marketing=True)
    st.aggiorna_cliente(stop, opt_out=True)
    senza_consenso = st.aggiungi_cliente("Teo", telefono="+390000000045")
    esito = motore.prepara_selezionati(st, [a, senza_profitto, stop, senza_consenso, 999, a, True],
                                       regole=REGOLE)
    assert len(esito.create) == 2
    assert "STOP" in esito.esclusi[stop] and "consenso" in esito.esclusi[senza_consenso]
    assert esito.esclusi[999] == "cliente inesistente"
    neutro = [st.proposta(x) for x in esito.create if st.proposta(x)["cliente_id"] == senza_profitto][0]  # type: ignore[index]
    assert neutro is not None and "€" not in neutro["messaggio"]
    assert messaggi.NOTA_RISCHIO_DEFAULT not in neutro["messaggio"]
    assert neutro["messaggio"].endswith(messaggi.RIGA_STOP) and neutro["messaggio"].startswith("Ciao Ugo!")
    # una proposta aperta alla volta anche a mano
    assert motore.prepara_selezionati(st, [a], regole=REGOLE).esclusi[a] == "ha già una proposta aperta"


def test_testo_neutro_inviato_com_e(st: CRMStore, monkeypatch: pytest.MonkeyPatch) -> None:
    """R-808-7: il testo neutro rimandato identico parte com'è (senza la nota sul rischio);
    cambiato dall'operatore, riceve nota e riga STOP (V-1 bot #381)."""
    monkeypatch.delenv("GAS_CRM_NOTA_RISCHIO", raising=False)
    srv = servizi_base(st)
    ids = []
    for i in range(2):
        c = st.aggiungi_cliente(f"Ugo{i} Neri", telefono=f"+39000000005{i}", consenso_marketing=True)
        st.apri_posizione(c, srv["oro"], data="2026-06-01", capitale_iniziale_cents=500_000)
        ids.append(c)
    esito = motore.prepara_selezionati(st, ids, regole=REGOLE)
    p1, p2 = esito.create
    testo1 = st.proposta(p1)["messaggio"]  # type: ignore[index]
    assert messaggi.NOTA_RISCHIO_DEFAULT not in testo1
    inviata = st.transiziona_proposta(p1, "inviata", messaggio="  " + testo1 + "\n")
    assert inviata["messaggio"] == testo1
    cambiato = st.transiziona_proposta(p2, "inviata", messaggio="Ciao Ugo, ti chiamo domani")
    assert cambiato["messaggio"] == ("Ciao Ugo, ti chiamo domani\n\n" + messaggi.NOTA_RISCHIO_DEFAULT
                                     + "\n\n" + messaggi.RIGA_STOP)


def test_identita_dopo_crash_a_meta_scrittura(tmp_path: Path) -> None:
    """R-808-3: journal rimasto dopo un crash del CRM: il kernel legge lo stesso (SQLite
    annulla la scrittura a metà), invece di mandare tutto al forte per sempre."""
    import subprocess
    import sys
    from modules.crm.store import identita_clienti
    db = tmp_path / ".gas_memory_crm.db"
    CRMStore(db).aggiungi_cliente("Marco Bianchi", telefono="+393331234567")
    codice = ("import sqlite3, os; con = sqlite3.connect(%r); con.execute('PRAGMA cache_size=1'); "
              "con.execute('BEGIN IMMEDIATE'); "
              "con.execute(\"UPDATE crm_clienti SET nome = 'X' || hex(randomblob(20000))\"); "
              "con.execute(\"INSERT INTO crm_eventi (ts, tipo, descrizione, autore) SELECT ts, tipo, "
              "descrizione || hex(randomblob(9000)), autore FROM crm_eventi\"); os._exit(0)") % str(db)
    subprocess.run([sys.executable, "-c", codice], check=True)
    assert (tmp_path / ".gas_memory_crm.db-journal").exists()
    letti = identita_clienti(db)
    assert letti is not None and [c["nome"] for c in letti] == ["Marco Bianchi"]


def test_v1_ve381_parole_vietate_non_si_aggirano() -> None:
    """V-1 verifica esterna #381 (3° giro): spazi a larghezza zero, spazi doppi e lettere
    staccate non aggirano più il filtro; le frasi normali passano."""
    from modules.crm import scrittore
    for furbo in ("rendimento garan\u200btito", "zero  rischi", "g a r a n t i t o",
                  "SICURO AL 100 %", "nessun draw-down", "Solo   oggi!",
                  # V-3 verifica esterna #381 (4° giro): altre forme della stessa promessa
                  "ti garantisco un bel mese", "garanzia di rendimento", "capitale protetto",
                  "rendimento sicuro", "profitto assicurato", "soldi facili", "investi ora",
                  "solo per oggi",
                  # V-1 verifica esterna #381 (5° giro) e bot su f537d231: altre forme
                  "Ti garantirò risultati", "Possiamo garantirti un ottimo servizio",
                  "100% sicuro", "senza alcun rischio", "rischio nullo",
                  "Il capitale è al sicuro", "ti assicuro", "non perderai nulla",
                  "ultima occasione", "posti limitati", "affare sicuro"):
        with pytest.raises(ErroreCRM, match="testo scartato"):
            scrittore.pulisci(furbo)
    for buono in ("Ciao Mario, ottimo mese! Ti va di provare Segnali VIP? Ne parliamo?",
                  "Sei sicuro alla fine? Ne parliamo con calma."):
        assert scrittore.pulisci(buono) == buono


def test_v2_ve381_avviso_scelta_manuale_di_chi_e_appena_entrato(st: CRMStore) -> None:
    """V-2 verifica esterna #381 (3° giro): a mano non si blocca, ma il motivo della
    proposta avverte l'operatore (decisione 9: attenzione a chi è appena entrato)."""
    srv = servizi_base(st)
    nuovo = st.aggiungi_cliente("Ada Neri", telefono="+390000000061", consenso_marketing=True)
    st.apri_posizione(nuovo, srv["oro"], data="2026-06-10", capitale_iniziale_cents=500_000)
    st.aggiorna_cliente(nuovo, followup_attivo=False)
    vecchio, _ = cliente_contento(st, srv, nome="Ugo Blu", telefono="+390000000062")
    esito = motore.prepara_selezionati(st, [nuovo, vecchio], regole=REGOLE)
    motivi = {st.proposta(x)["cliente_id"]: st.proposta(x)["motivo"] for x in esito.create}  # type: ignore[index]
    assert motivi[nuovo].startswith("⚠ ATTENZIONE: cliente da soli 10 giorni")
    assert "non ha ancora pagato" in motivi[nuovo] and "follow-up spento" in motivi[nuovo]
    assert "ATTENZIONE" not in motivi[vecchio]


def test_r809_1_file_bloccato_non_riaperto(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """R-809-1: «database is locked» chiude subito (None), senza una seconda apertura che
    raddoppierebbe l'attesa; si riapre solo per il journal rimasto («readonly»)."""
    from modules.crm import store as modulo
    db = tmp_path / ".gas_memory_crm.db"
    CRMStore(db).aggiungi_cliente("Marco Bianchi", telefono="+393331234567")
    aperture: List[str] = []
    vero = modulo.sqlite3.connect

    def finto(dove: Any, *a: Any, **kw: Any) -> Any:
        aperture.append(str(dove))
        if str(dove).endswith("mode=ro"):
            raise sqlite3.OperationalError("database is locked")
        return vero(dove, *a, **kw)

    monkeypatch.setattr(modulo.sqlite3, "connect", finto)
    assert modulo.identita_clienti(db) is None and len(aperture) == 1


def test_v4_ve381_modello_opus_dalla_fonte_unica() -> None:
    from brains import model_ids
    from modules.crm import scrittore
    assert scrittore.MODELLO_DEFAULT == model_ids.MODEL_CLAUDE_OPUS
    assert model_ids.e_modello_opus(model_ids.MODEL_CLAUDE_OPUS)
    assert not model_ids.e_modello_opus("claude-sonnet-5-5")


def test_nota_tolta_senza_doppi_spazi() -> None:
    """Nota minore #813: togliere la nota sul rischio in mezzo al testo non lascia spazi doppi."""
    from modules.crm import scrittore
    assert scrittore.pulisci("Ciao Mario! " + messaggi.NOTA_RISCHIO_DEFAULT + " Ne parliamo?") == \
        "Ciao Mario! Ne parliamo?"


def test_copia_cifrata_fuori_dal_mac(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Decisione dell'operatore 2026-11-19: copia giornaliera anche su iCloud Drive, SOLO
    cifrata; senza password nessuna copia esce; ripristino senza mai sovrascrivere."""
    from modules.crm import copia_cifrata
    from modules.crm import __main__ as cli
    import argparse
    db = tmp_path / ".gas_memory_crm.db"
    s = CRMStore(db)
    s.aggiungi_cliente("Marco Bianchi", telefono="+393331234567", email="marco@esempio.it")
    icloud = tmp_path / "icloud"
    monkeypatch.setenv("GAS_CRM_DB", str(db))
    monkeypatch.setenv("GAS_CRM_BACKUP_CIFRATO_DIR", str(icloud))
    # senza password: spenta, niente esce
    assert "GAS_CRM_BACKUP_PASSWORD" in (copia_cifrata.motivo_spenta() or "")
    assert cli.cmd_backup(argparse.Namespace(demo=False)) == 0
    assert not icloud.exists()
    monkeypatch.setenv("GAS_CRM_BACKUP_PASSWORD", "corta")
    assert copia_cifrata.motivo_spenta() is not None  # troppo corta: spenta
    monkeypatch.setenv("GAS_CRM_BACKUP_PASSWORD", "una-password-lunga-1")
    assert copia_cifrata.motivo_spenta() is None
    assert cli.cmd_backup(argparse.Namespace(demo=False)) == 0
    copie = sorted(icloud.glob("crm-*.gascrm"))
    assert len(copie) == 1
    grezzo = copie[0].read_bytes()
    assert grezzo.startswith(copia_cifrata.MAGIA)
    for in_chiaro in (b"Marco", b"Bianchi", b"3331234567", b"marco@esempio", b"SQLite format"):
        assert in_chiaro not in grezzo
    # ripristino: in un posto nuovo sì, sopra un DB esistente mai
    nuovo = tmp_path / "ripristinato.db"
    assert copia_cifrata.ripristina(copie[0], nuovo, "una-password-lunga-1") == nuovo
    assert CRMStore(nuovo).clienti()[0]["nome"] == "Marco Bianchi"
    with pytest.raises(ErroreCRM, match="esiste già"):
        copia_cifrata.ripristina(copie[0], db, "una-password-lunga-1")
    with pytest.raises(ErroreCRM, match="password sbagliata"):
        copia_cifrata.ripristina(copie[0], tmp_path / "altro.db", "password-sbagliata-123")
    assert not (tmp_path / "altro.db").exists()
    falso = tmp_path / "falso.gascrm"
    falso.write_bytes(b"non sono una copia")
    with pytest.raises(ErroreCRM, match="non è una copia cifrata"):
        copia_cifrata.ripristina(falso, tmp_path / "x.db", "una-password-lunga-1")
    # dalla riga di comando
    assert cli.cmd_ripristina(argparse.Namespace(file=str(copie[0]),
                                                 dest=str(tmp_path / "da_cli.db"))) == 0
    assert cli.cmd_ripristina(argparse.Namespace(file=str(copie[0]), dest=None)) == 1  # DB c'è già
    # tiene le ultime N copie
    for i in range(4):
        finta = tmp_path / f"crm-2026010{i}-000000.db"
        finta.write_bytes(db.read_bytes())
        copia_cifrata.copia_fuori(finta, keep=2)
    # le finte di gennaio ruotano tra loro; la copia di oggi fatta sopra è «nel futuro» per
    # loro e non si tocca (R-858-1)
    assert sorted(p.name for p in icloud.glob("crm-202601*.gascrm")) == [
        "crm-20260102.gascrm", "crm-20260103.gascrm"]


def test_r858_copie_cifrate_orologio_sbagliato(tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
                                              caplog: pytest.LogCaptureFixture) -> None:
    """R-858-1: la copia cifrata appena fatta veniva cancellata se c'erano copie con una data
    più avanti (orologio del Mac andato nel futuro e poi corretto), e la dashboard diceva
    «copia OK» senza nessuna copia di oggi fuori dal Mac."""
    from modules.crm import copia_cifrata
    icloud = tmp_path / "icloud"
    icloud.mkdir()
    monkeypatch.setenv("GAS_CRM_BACKUP_CIFRATO_DIR", str(icloud))
    monkeypatch.setenv("GAS_CRM_BACKUP_PASSWORD", "una-password-lunga-1")
    db = tmp_path / "crm.db"
    CRMStore(db).aggiungi_cliente("Mario Rossi")
    for g in range(1, 31):  # 30 copie fatte con l'orologio nel 2030
        (icloud / f"crm-203001{g:02d}.gascrm").write_bytes(b"x")
    a_mano = icloud / "crm-prima-import.gascrm"
    a_mano.write_bytes(b"copia a mano")
    oggi = tmp_path / "crm-20261124-090000.db"
    oggi.write_bytes(db.read_bytes())
    with caplog.at_level("WARNING"):
        fuori, motivo = copia_cifrata.copia_fuori(oggi, keep=30)
    assert motivo is None and fuori is not None and fuori.exists()
    assert len(list(icloud.glob("crm-2030*.gascrm"))) == 30  # non si toccano
    assert a_mano.read_bytes() == b"copia a mano"
    assert "data nel futuro" in caplog.text
    # orologio tornato indietro di poco: la copia di oggi resta anche se non è l'ultima
    (icloud / "crm-20261125.gascrm").write_bytes(b"x")
    ieri = tmp_path / "crm-20261123-090000.db"
    ieri.write_bytes(db.read_bytes())
    fuori, motivo = copia_cifrata.copia_fuori(ieri, keep=1)
    assert motivo is None and fuori is not None and fuori.exists()


def test_r815_ripristino_sicuro_dopo_un_crash(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """R-815-1: un DB va in crash a metà scrittura, l'operatore lo sposta ma il suo journal
    resta lì: il ripristino rifiuta invece di consegnare un DB rovinato. R-815-2: un DB che
    compare durante il ripristino non viene sovrascritto."""
    import subprocess
    import sys
    from modules.crm import copia_cifrata
    pw = "una-password-lunga-1"
    buono = tmp_path / "buono.db"
    CRMStore(buono).aggiungi_cliente("Anna Verdi", telefono="+393330000001")
    copia = tmp_path / "crm-20260101-000000.gascrm"
    copia.write_bytes(copia_cifrata.cifra(buono.read_bytes(), pw))
    # il DB di lavoro, con altri clienti, va in crash a metà scrittura
    db = tmp_path / ".gas_memory_crm.db"
    st = CRMStore(db)
    for i in range(50):
        st.aggiungi_cliente(f"Cliente {i}", telefono=f"+3933300{i:05d}")
    codice = ("import sqlite3, os; con = sqlite3.connect(%r); con.execute('PRAGMA cache_size=1'); "
              "con.execute('BEGIN IMMEDIATE'); "
              "con.execute(\"UPDATE crm_clienti SET nome = 'X' || hex(randomblob(4000))\"); "
              "os._exit(0)") % str(db)
    subprocess.run([sys.executable, "-c", codice], check=True)
    journal = tmp_path / ".gas_memory_crm.db-journal"
    assert journal.exists()
    db.rename(tmp_path / "rotto.db")  # l'operatore sposta il DB rovinato; il journal resta
    with pytest.raises(ErroreCRM, match="file di lavoro"):
        copia_cifrata.ripristina(copia, db, pw)
    assert not db.exists()
    journal.rename(tmp_path / "rotto.db-journal")  # spostato anche lui: ora si può
    copia_cifrata.ripristina(copia, db, pw)
    assert [c["nome"] for c in CRMStore(db).clienti()] == ["Anna Verdi"]
    # R-815-2: il DB nasce mentre si decifra (es. `serve` avviato nello stesso momento)
    dest = tmp_path / "nuovo.db"
    vero = copia_cifrata.decifra

    def decifra_e_intanto_nasce(blob: bytes, password: str) -> bytes:
        dest.write_bytes(b"DB creato nel frattempo")
        return vero(blob, password)

    monkeypatch.setattr(copia_cifrata, "decifra", decifra_e_intanto_nasce)
    with pytest.raises(ErroreCRM, match="comparso durante il ripristino"):
        copia_cifrata.ripristina(copia, dest, pw)
    assert dest.read_bytes() == b"DB creato nel frattempo"
    assert not list(tmp_path.glob("*.ripristino.tmp"))


def test_ve386_copie_cifrate_rifinite(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Note di bot e verifica esterna #386: password in forme Unicode diverse, una copia al
    giorno, niente .tmp lasciati, file leggibili solo dal proprietario, ripristino che toglie
    il file se il ricontrollo finale fallisce, ripiego senza collegamenti fisici."""
    import stat
    import time as _t
    import unicodedata
    from modules.crm import copia_cifrata
    # V-1 verifica: «Città» scritta in NFC (dal .env) o NFD (digitata altrove) è la stessa password
    nfc = unicodedata.normalize("NFC", "Città-della-pace-2026")
    nfd = unicodedata.normalize("NFD", nfc)
    assert nfc != nfd
    assert copia_cifrata.decifra(copia_cifrata.cifra(b"dati", nfc), nfd) == b"dati"
    db = tmp_path / ".gas_memory_crm.db"
    st = CRMStore(db)
    st.aggiungi_cliente("Anna Verdi", telefono="+393330000001")
    icloud = tmp_path / "icloud"
    monkeypatch.setenv("GAS_CRM_BACKUP_CIFRATO_DIR", str(icloud))
    monkeypatch.setenv("GAS_CRM_BACKUP_PASSWORD", "  una-password-lunga-1  ")
    # V-1 bot: due copie dello stesso giorno → UNA copia esterna (quella del giorno si rinnova)
    for ora in ("080000", "200000"):
        locale = tmp_path / f"crm-20261120-{ora}.db"
        locale.write_bytes(db.read_bytes())
        fuori, motivo = copia_cifrata.copia_fuori(locale)
        assert motivo is None and fuori is not None and fuori.name == "crm-20261120.gascrm"
    assert [f.name for f in icloud.glob("*.gascrm")] == ["crm-20261120.gascrm"]
    # V-4 verifica: solo il proprietario legge (copia esterna e copia locale)
    assert stat.S_IMODE(fuori.stat().st_mode) == 0o600
    locale_vera = st.backup(tmp_path / "locali")
    assert locale_vera is not None and stat.S_IMODE(locale_vera.stat().st_mode) == 0o600
    # V-3: una copia che fallisce non lascia .tmp; i .tmp vecchi di copie interrotte spariscono
    vecchio = icloud / "crm-20261101.gascrm.tmp"
    vecchio.write_bytes(b"resto cifrato")
    os.utime(vecchio, (_t.time() - 7200, _t.time() - 7200))
    vero_replace = os.replace

    def replace_rotto(a: Any, b: Any) -> None:
        raise OSError("disco pieno")

    monkeypatch.setattr(copia_cifrata.os, "replace", replace_rotto)
    fuori2, motivo2 = copia_cifrata.copia_fuori(tmp_path / "crm-20261120-080000.db")
    monkeypatch.setattr(copia_cifrata.os, "replace", vero_replace)
    assert fuori2 is None and "errore durante la copia cifrata" in (motivo2 or "")
    assert not list(icloud.glob("*.tmp"))
    # ripristino: file 0600; senza collegamenti fisici il ripiego crea il file in modo esclusivo
    pw = "una-password-lunga-1"
    rip = copia_cifrata.ripristina(fuori, tmp_path / "ripristinato.db", pw)
    assert stat.S_IMODE(rip.stat().st_mode) == 0o600
    vero_link = os.link

    def link_assente(a: Any, b: Any) -> None:
        raise OSError(1, "collegamenti fisici non supportati")

    monkeypatch.setattr(copia_cifrata.os, "link", link_assente)
    rip2 = copia_cifrata.ripristina(fuori, tmp_path / "senza_link.db", pw)
    assert stat.S_IMODE(rip2.stat().st_mode) == 0o600
    assert CRMStore(rip2).clienti()[0]["nome"] == "Anna Verdi"
    monkeypatch.setattr(copia_cifrata.os, "link", vero_link)
    # V-2 verifica: se il ricontrollo finale fallisce, il file creato da questo ripristino sparisce
    esiti = iter([True, False])
    monkeypatch.setattr(copia_cifrata, "_integro", lambda _p: next(esiti))
    with pytest.raises(ErroreCRM, match="l'ho tolto"):
        copia_cifrata.ripristina(fuori, tmp_path / "rovinato.db", pw)
    assert not (tmp_path / "rovinato.db").exists()
    assert not list(tmp_path.glob("*.ripristino.tmp"))


def test_r817_1_due_copie_dello_stesso_giorno_in_parallelo(tmp_path: Path,
                                                         monkeypatch: pytest.MonkeyPatch) -> None:
    """R-817-1: guardiano e `backup` a mano nello stesso istante, stesso giorno: ognuno scrive
    il SUO temporaneo, e la copia del giorno resta decifrabile."""
    import threading
    from modules.crm import copia_cifrata
    db = tmp_path / ".gas_memory_crm.db"
    CRMStore(db).aggiungi_cliente("Anna Verdi", telefono="+393330000001")
    icloud = tmp_path / "icloud"
    monkeypatch.setenv("GAS_CRM_BACKUP_CIFRATO_DIR", str(icloud))
    monkeypatch.setenv("GAS_CRM_BACKUP_PASSWORD", "una-password-lunga-1")
    copie = []
    for ora in ("080000", "080001"):
        c = tmp_path / f"crm-20261120-{ora}.db"
        c.write_bytes(db.read_bytes())
        copie.append(c)
    tutti_e_due = threading.Barrier(2, timeout=10)
    usati: List[Path] = []
    vero = copia_cifrata._scrivi_privato

    def scrivi_insieme(percorso: Path, dati: bytes, esclusivo: bool = False) -> None:
        if percorso.name.endswith("tmp") and percorso.parent == icloud:
            usati.append(percorso)
            tutti_e_due.wait()  # le due copie scrivono nello stesso momento
        vero(percorso, dati, esclusivo)

    monkeypatch.setattr(copia_cifrata, "_scrivi_privato", scrivi_insieme)
    esiti: List[Any] = []
    fili = [threading.Thread(target=lambda c=c: esiti.append(copia_cifrata.copia_fuori(c)))
            for c in copie]
    for f in fili:
        f.start()
    for f in fili:
        f.join()
    assert len(usati) == 2 and usati[0] != usati[1]
    assert all(fuori is not None for fuori, _ in esiti)
    giorno = icloud / "crm-20261120.gascrm"
    assert copia_cifrata.decifra(giorno.read_bytes(), "una-password-lunga-1").startswith(b"SQLite format")
    assert not list(icloud.glob("*tmp"))


def test_ve386b_ripristino_con_disco_pieno_non_lascia_dati_in_chiaro(
        tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """V-1 verifica esterna #386 (2° giro): disco pieno mentre si scrive il temporaneo in
    chiaro → nessun file con dati parziali dei clienti resta; V-2: un collegamento pendente
    al posto di dest dà «esiste già»."""
    import errno
    from modules.crm import copia_cifrata
    pw = "una-password-lunga-1"
    db = tmp_path / "buono.db"
    CRMStore(db).aggiungi_cliente("Anna Verdi", telefono="+393330000001")
    copia = tmp_path / "crm-20261120.gascrm"
    copia.write_bytes(copia_cifrata.cifra(db.read_bytes(), pw))
    vero = copia_cifrata._scrivi_privato

    def disco_pieno(percorso: Path, dati: bytes, esclusivo: bool = False) -> None:
        vero(percorso, dati[: len(dati) // 2], esclusivo)  # metà scritta, poi pieno
        raise OSError(errno.ENOSPC, "No space left on device")

    monkeypatch.setattr(copia_cifrata, "_scrivi_privato", disco_pieno)
    with pytest.raises(OSError):
        copia_cifrata.ripristina(copia, tmp_path / "nuovo.db", pw)
    assert not list(tmp_path.glob("*.ripristino.tmp")) and not (tmp_path / "nuovo.db").exists()
    monkeypatch.setattr(copia_cifrata, "_scrivi_privato", vero)
    pendente = tmp_path / "pendente.db"
    pendente.symlink_to(tmp_path / "non_esiste")
    with pytest.raises(ErroreCRM, match="esiste già"):
        copia_cifrata.ripristina(copia, pendente, pw)


def test_v1_bot386_copia_esterna_visibile(st: CRMStore, tmp_path: Path,
                                         monkeypatch: pytest.MonkeyPatch) -> None:
    """V-1 bot #386 (MEDIA): una copia esterna che fallisce non resta nascosta nel log. Prova
    vera di scrittura all'avvio, esito dell'ultima copia in /api/stato, avviso all'operatore
    (Telegram, senza dati dei clienti); V-2: ripristino con la password vecchia; V-4: segnaposto
    «.icloud» spiegato."""
    from modules.crm import copia_cifrata
    pw = "una-password-lunga-1"
    buona = tmp_path / "icloud"
    monkeypatch.setenv("GAS_CRM_BACKUP_PASSWORD", pw)
    monkeypatch.setenv("GAS_CRM_BACKUP_CIFRATO_DIR", str(buona))
    assert copia_cifrata.prova_scrittura() is None
    assert buona.is_dir() and not list(buona.iterdir())  # la prova non lascia file
    finta = tmp_path / "non_una_cartella"
    finta.write_bytes(b"sono un file")
    monkeypatch.setenv("GAS_CRM_BACKUP_CIFRATO_DIR", str(finta))
    assert "non si può scrivere" in (copia_cifrata.prova_scrittura() or "")
    # esito nel server: fallita → ok False, motivo, avviso senza nomi; riuscita → ok True
    st.aggiungi_cliente("Marco Bianchi", telefono="+393331234567")
    avvisi: List[str] = []
    stato = server.Stato(st, TOKEN, regole=REGOLE, avvisa=lambda t: (avvisi.append(t) or (True, "")))
    assert stato.copia_esterna["spenta"] is False and stato.copia_esterna["ok"] is None
    copia = st.backup(tmp_path / "locali")
    assert copia is not None
    server._copia_esterna(stato, copia)
    assert stato.copia_esterna["ok"] is False and stato.copia_esterna["motivo"]
    assert len(avvisi) == 1 and "NON è riuscita" in avvisi[0] and "Marco" not in avvisi[0]
    monkeypatch.setenv("GAS_CRM_BACKUP_CIFRATO_DIR", str(buona))
    server._copia_esterna(stato, copia)
    assert stato.copia_esterna["ok"] is True and stato.copia_esterna["quando"]
    assert len(avvisi) == 1  # nessun avviso quando riesce
    # spenta (senza password): niente avviso, segnata come spenta
    monkeypatch.delenv("GAS_CRM_BACKUP_PASSWORD")
    server._copia_esterna(stato, copia)
    assert stato.copia_esterna["spenta"] is True and stato.copia_esterna["ok"] is None
    assert len(avvisi) == 1
    # V-4: segnaposto di iCloud non scaricato
    segnaposto = tmp_path / ".crm-20261120.gascrm.icloud"
    segnaposto.write_bytes(b"bplist00")
    with pytest.raises(ErroreCRM, match="ancora solo su iCloud"):
        copia_cifrata.ripristina(segnaposto, tmp_path / "x.db", pw)


def test_v1_bot386_esito_in_api_stato(avviato) -> None:
    stato, c, _ = avviato
    assert c.post("/api/login", {"token": TOKEN})[0] == 200
    corpo = c.get("/api/stato")[2]
    assert corpo["server"]["copia_esterna"] == stato.copia_esterna


def test_v2_bot386_ripristino_con_la_password_di_prima(tmp_path: Path,
                                                    monkeypatch: pytest.MonkeyPatch) -> None:
    import argparse
    import getpass
    from modules.crm import copia_cifrata
    from modules.crm import __main__ as cli
    db = tmp_path / "vecchio.db"
    CRMStore(db).aggiungi_cliente("Anna Verdi", telefono="+393330000001")
    copia = tmp_path / "crm-20261101.gascrm"
    copia.write_bytes(copia_cifrata.cifra(db.read_bytes(), "password-di-prima-1"))
    monkeypatch.setenv("GAS_CRM_BACKUP_PASSWORD", "password-di-adesso-2")
    monkeypatch.setattr(sys.stdin, "isatty", lambda: True)
    monkeypatch.setattr(getpass, "getpass", lambda _p="": "password-di-prima-1")
    assert cli.cmd_ripristina(argparse.Namespace(file=str(copia), dest=str(tmp_path / "r.db"))) == 0
    assert CRMStore(tmp_path / "r.db").clienti()[0]["nome"] == "Anna Verdi"


def test_ve386c_note_del_terzo_giro(st: CRMStore, tmp_path: Path,
                                   monkeypatch: pytest.MonkeyPatch) -> None:
    """Note di bot e verifica esterna su #386 (3° giro): disco non collegato, copia locale
    rovinata, temporaneo del ripristino unico ed esclusivo, file di lavoro come collegamento
    pendente, prove interrotte ripulite, indicatore se fallisce la copia locale, prova
    all'avvio con un tempo massimo (R-820-1)."""
    import threading
    import time as _t
    from modules.crm import copia_cifrata
    pw = "una-password-lunga-1"
    monkeypatch.setenv("GAS_CRM_BACKUP_PASSWORD", pw)
    # disco esterno non collegato: niente cartella creata sul Mac, nessuna copia «riuscita»
    smontato = tmp_path / "Volumes" / "Disco" / "copie"
    monkeypatch.setenv("GAS_CRM_BACKUP_CIFRATO_DIR", str(smontato))
    assert "non c'è: creala, o collega il disco" in (copia_cifrata.prova_scrittura() or "")
    st.aggiungi_cliente("Anna Verdi", telefono="+393330000001")
    buona = st.backup(tmp_path / "locali")
    assert buona is not None
    fuori, motivo = copia_cifrata.copia_fuori(buona)
    assert fuori is None and "non c'è: creala, o collega il disco" in (motivo or "")
    assert not smontato.exists()
    assert copia_cifrata.esito_all_avvio().startswith("NON FUNZIONA")
    # copia locale rovinata: la copia buona del giorno resta
    icloud = tmp_path / "icloud"
    monkeypatch.setenv("GAS_CRM_BACKUP_CIFRATO_DIR", str(icloud))
    giorno, _ = copia_cifrata.copia_fuori(buona)
    assert giorno is not None
    prima = giorno.read_bytes()
    rotta = tmp_path / (buona.stem[:12] + "-235959.db")
    rotta.write_bytes(b"non sono un database")
    fuori, motivo = copia_cifrata.copia_fuori(rotta)
    assert fuori is None and "non è integra" in (motivo or "") and giorno.read_bytes() == prima
    # prove di scrittura interrotte (processo ucciso) ripulite alla copia dopo
    vecchia_prova = icloud / ".prova-1-2.tmp"
    vecchia_prova.write_bytes(b"x")
    os.utime(vecchia_prova, (_t.time() - 7200, _t.time() - 7200))
    copia_cifrata.copia_fuori(buona)
    assert not vecchia_prova.exists()
    assert copia_cifrata.esito_all_avvio().startswith("ATTIVA")
    # ripristino: un collegamento simbolico al posto del temporaneo non viene seguito
    vittima = tmp_path / "vittima.txt"
    vittima.write_text("intatto")
    dest = tmp_path / "nuovo.db"
    previsto = dest.with_name(f"{dest.name}.{os.getpid()}-{threading.get_ident()}.ripristino.tmp")
    previsto.symlink_to(vittima)
    with pytest.raises(ErroreCRM, match="file .* accanto alla destinazione"):
        copia_cifrata.ripristina(giorno, dest, pw)
    assert vittima.read_text() == "intatto" and previsto.is_symlink() and not dest.exists()
    previsto.unlink()
    # file di lavoro come collegamento pendente: rifiutato
    pendente = tmp_path / "altro.db-journal"
    pendente.symlink_to(tmp_path / "manca")
    with pytest.raises(ErroreCRM, match="file di lavoro"):
        copia_cifrata.ripristina(giorno, tmp_path / "altro.db", pw)
    # R-820-1: una cartella che non risponde non blocca l'avvio
    monkeypatch.setattr(copia_cifrata, "prova_scrittura", lambda: _t.sleep(2) or None)
    inizio = _t.monotonic()
    assert copia_cifrata.esito_all_avvio(attesa_s=0.2).startswith("NON VERIFICATA")
    assert _t.monotonic() - inizio < 1.5


def test_v2_bot386c_copia_locale_fallita_si_vede(st: CRMStore, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("GAS_CRM_BACKUP_PASSWORD", "una-password-lunga-1")
    monkeypatch.setenv("GAS_CRM_BACKUP_CIFRATO_DIR", "/tmp")
    avvisi: List[str] = []
    stato = server.Stato(st, TOKEN, regole=REGOLE, avvisa=lambda t: (avvisi.append(t) or (True, "")))
    stato.copia_esterna = {"spenta": False, "motivo": None, "ok": True, "quando": "ieri"}
    monkeypatch.setattr(st, "backup", lambda *a, **kw: None)
    server._copia_giornaliera(stato)
    assert stato.copia_esterna["ok"] is False and "sul Mac non è riuscita" in stato.copia_esterna["motivo"]
    assert len(avvisi) == 1


def test_r821_1_copia_locale_fallita_in_rosso_anche_a_copia_spenta(
        st: CRMStore, monkeypatch: pytest.MonkeyPatch) -> None:
    """R-821-1: con la copia esterna spenta (senza password) una copia LOCALE fallita è
    comunque rossa e avvisa l'operatore."""
    monkeypatch.delenv("GAS_CRM_BACKUP_PASSWORD", raising=False)
    avvisi: List[str] = []
    stato = server.Stato(st, TOKEN, regole=REGOLE, avvisa=lambda t: (avvisi.append(t) or (True, "")))
    assert stato.copia_esterna["spenta"] is True
    monkeypatch.setattr(st, "backup", lambda *a, **kw: None)
    server._copia_giornaliera(stato)
    assert stato.copia_esterna["ok"] is False and stato.copia_esterna["spenta"] is False
    assert "sul Mac non è riuscita" in stato.copia_esterna["motivo"] and len(avvisi) == 1


def test_r821_disco_esterno_staccato_con_punto_di_mount_vuoto(
        tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Rischio del revisore #821: /Volumes/Disco resta come cartella vuota a disco staccato:
    la copia non deve finire sul disco del Mac."""
    from modules.crm import copia_cifrata
    volumi = tmp_path / "Volumes"
    (volumi / "Disco").mkdir(parents=True)  # cartella rimasta, ma non è un mount
    monkeypatch.setattr(copia_cifrata, "VOLUMI", volumi)
    monkeypatch.setenv("GAS_CRM_BACKUP_PASSWORD", "una-password-lunga-1")
    monkeypatch.setenv("GAS_CRM_BACKUP_CIFRATO_DIR", str(volumi / "Disco" / "copie"))
    assert "non è collegato" in (copia_cifrata.prova_scrittura() or "")
    assert not (volumi / "Disco" / "copie").exists()
    monkeypatch.setattr(copia_cifrata.os.path, "ismount", lambda p: True)  # disco collegato
    assert copia_cifrata.prova_scrittura() is None


def test_v1_bot387_permesso_negato_non_rompe_la_copia(st: CRMStore, tmp_path: Path,
                                                     monkeypatch: pytest.MonkeyPatch) -> None:
    """V-1 bot #387 (MEDIA): un permesso negato sulla cartella che contiene le copie non fa
    sollevare `copia_fuori` (il thread non muore, l'indicatore diventa rosso) e all'avvio non
    dice «ATTIVA». V-2: `_integro` non crea file. Nota #822: collegamento simbolico verso un
    disco staccato riconosciuto."""
    from modules.crm import copia_cifrata
    monkeypatch.setenv("GAS_CRM_BACKUP_PASSWORD", "una-password-lunga-1")
    chiusa = tmp_path / "chiusa"
    monkeypatch.setenv("GAS_CRM_BACKUP_CIFRATO_DIR", str(chiusa / "copie"))
    vero_is_dir = Path.is_dir

    def is_dir_negato(self: Path) -> bool:
        if self == chiusa:
            raise PermissionError(13, "Permission denied")
        return vero_is_dir(self)

    monkeypatch.setattr(Path, "is_dir", is_dir_negato)
    st.aggiungi_cliente("Anna Verdi", telefono="+393330000001")
    copia = st.backup(tmp_path / "locali")
    assert copia is not None
    fuori, motivo = copia_cifrata.copia_fuori(copia)  # non solleva
    assert fuori is None and "non è accessibile" in (motivo or "")
    assert copia_cifrata.esito_all_avvio().startswith("NON FUNZIONA")
    stato = server.Stato(st, TOKEN, regole=REGOLE)
    server._copia_esterna(stato, copia)
    assert stato.copia_esterna["ok"] is False
    monkeypatch.setattr(Path, "is_dir", vero_is_dir)
    # una prova che solleva per un motivo qualsiasi non diventa «ATTIVA»
    def prova_rotta() -> None:
        raise RuntimeError("imprevisto")

    monkeypatch.setattr(copia_cifrata, "prova_scrittura", prova_rotta)
    assert copia_cifrata.esito_all_avvio().startswith("NON FUNZIONA")
    # V-2: il controllo di integrità non crea un file vuoto
    assente = tmp_path / "non_esiste.db"
    assert copia_cifrata._integro(assente) is False and not assente.exists()
    # nota #822: un collegamento simbolico che porta su un disco staccato
    monkeypatch.undo()
    volumi = tmp_path / "Volumes"
    (volumi / "Disco").mkdir(parents=True)
    scorciatoia = tmp_path / "Backup"
    scorciatoia.symlink_to(volumi / "Disco")
    monkeypatch.setattr(copia_cifrata, "VOLUMI", volumi)
    monkeypatch.setenv("GAS_CRM_BACKUP_PASSWORD", "una-password-lunga-1")
    monkeypatch.setenv("GAS_CRM_BACKUP_CIFRATO_DIR", str(scorciatoia / "copie"))
    assert "non è collegato" in (copia_cifrata.prova_scrittura() or "")


def test_v1_bot387b_ripristino_interrotto_non_resta_in_chiaro(
        st: CRMStore, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """V-1 bot #387 (d809f5f1): il temporaneo IN CHIARO di un ripristino ucciso a metà viene
    tolto al ripristino successivo; mai quello di un processo vivo né un collegamento
    simbolico. V-2: motivo giusto anche a copia esterna spenta (verifica esterna #387)."""
    from modules.crm import copia_cifrata
    monkeypatch.setenv("GAS_CRM_BACKUP_PASSWORD", "una-password-lunga-1")
    monkeypatch.setenv("GAS_CRM_BACKUP_CIFRATO_DIR", str(tmp_path / "copie"))
    st.aggiungi_cliente("Anna Verdi", telefono="+393330000001")
    fuori, _ = copia_cifrata.copia_fuori(st.backup(tmp_path / "locali"))
    assert fuori is not None
    dest = tmp_path / "ripristinato.db"
    morto = dest.with_name(f"{dest.name}.999999999-1.ripristino.tmp")
    morto.write_bytes(b"dati in chiaro di un ripristino interrotto")
    vivo = dest.with_name(f"{dest.name}.{os.getppid()}-1.ripristino.tmp")
    vivo.write_bytes(b"ripristino in corso in un altro processo")
    vittima = tmp_path / "vittima.txt"
    vittima.write_text("da non toccare")
    link = dest.with_name(f"{dest.name}.999999998-1.ripristino.tmp")
    link.symlink_to(vittima)
    altro = tmp_path / "altro.db.999999997-1.ripristino.tmp"  # di un'altra destinazione
    altro.write_bytes(b"x")
    # R-824-1/2: PID fuori misura o con cifre non ASCII: non solleva e il file non si tocca
    enorme = dest.with_name(f"{dest.name}.99999999999-1.ripristino.tmp")
    enorme.write_bytes(b"x")
    # R-825-1: nove «٩» = PID 999999999, morto: senza il filtro ASCII verrebbe tolto
    arabo = dest.with_name(f"{dest.name}.{chr(0x669) * 9}-1.ripristino.tmp")
    arabo.write_bytes(b"x")
    assert copia_cifrata.ripristina(fuori, dest, "una-password-lunga-1") == dest
    assert not morto.exists()
    assert vivo.exists() and link.is_symlink() and vittima.read_text() == "da non toccare"
    assert altro.exists() and enorme.exists() and arabo.exists()
    # V-1 bot #388 (7cd7a2f0): dopo un riavvio il PID può essere di un processo vivo (anche
    # di questo): un resto più vecchio di un'ora si toglie lo stesso; uno recente no
    vecchio_vivo = dest.with_name(f"{dest.name}.{os.getppid()}-2.ripristino.tmp")
    vecchio_mio = dest.with_name(f"{dest.name}.{os.getpid()}-2.ripristino.tmp")
    for f in (vecchio_vivo, vecchio_mio):
        f.write_bytes(b"dati in chiaro di prima del riavvio")
        os.utime(f, (time.time() - 2 * copia_cifrata.TMP_VECCHIO_S,) * 2)
    os.unlink(dest)
    assert copia_cifrata.ripristina(fuori, dest, "una-password-lunga-1") == dest
    assert not vecchio_vivo.exists() and not vecchio_mio.exists() and vivo.exists()
    # V-2 bot #388: ripristino ucciso fra os.link e la cancellazione del temporaneo: `dest`
    # esiste, il nuovo ripristino si ferma su «esiste già» ma il temporaneo in chiaro sparisce
    resto_link = dest.with_name(f"{dest.name}.999999996-1.ripristino.tmp")
    os.link(dest, resto_link)
    with pytest.raises(ErroreCRM, match="esiste già"):
        copia_cifrata.ripristina(fuori, dest, "una-password-lunga-1")
    assert not resto_link.exists() and dest.exists()
    assert copia_cifrata._processo_vivo(2 ** 40) is True  # OverflowError: nel dubbio vivo
    # V-2 verifica esterna #387: a copia esterna spenta il motivo non parla di «fuori dal Mac»
    monkeypatch.delenv("GAS_CRM_BACKUP_PASSWORD")
    stato = server.Stato(st, TOKEN, regole=REGOLE)
    monkeypatch.setattr(st, "backup", lambda *a, **kw: None)
    avvisi: List[str] = []
    stato.avvisa = lambda t: (avvisi.append(t) or (True, ""))
    server._copia_giornaliera(stato)
    assert "è spenta" in stato.copia_esterna["motivo"]
    assert "nemmeno" not in stato.copia_esterna["motivo"]
    assert len(avvisi) == 1 and "iCloud" not in avvisi[0]
    assert avvisi[0].lower().count("non è riuscita") == 1


def test_r825_2_cartella_non_valida_o_icloud_negato_il_crm_parte(
        st: CRMStore, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """R-825-2: «~utente» inesistente in GAS_CRM_BACKUP_CIFRATO_DIR, o iCloud Drive che
    macOS non lascia leggere: il CRM parte e la copia si vede in rosso (non «spenta»)."""
    from modules.crm import copia_cifrata
    monkeypatch.setenv("GAS_CRM_BACKUP_PASSWORD", "una-password-lunga-1")
    monkeypatch.setenv("GAS_CRM_BACKUP_CIFRATO_DIR", "~utente_che_non_esiste_r825/copie")
    stato = server.Stato(st, TOKEN, regole=REGOLE)  # prima: RuntimeError
    assert stato.copia_esterna["spenta"] is False
    assert copia_cifrata.esito_all_avvio().startswith("NON FUNZIONA")
    # R-826-1: a un solo componente (manca la «/») o relativo: mai dentro la cartella di lavoro
    lavoro = tmp_path / "lavoro"
    lavoro.mkdir()
    monkeypatch.chdir(lavoro)
    for valore in ("~x_inesistente_r826", "copie"):
        monkeypatch.setenv("GAS_CRM_BACKUP_CIFRATO_DIR", valore)
        esito = copia_cifrata.esito_all_avvio()
        assert esito.startswith("NON FUNZIONA") and "percorso completo" in esito
        fuori, motivo = copia_cifrata.copia_fuori(st.backup(tmp_path / "locali"))
        assert fuori is None and "percorso completo" in (motivo or "")
    assert list(lavoro.iterdir()) == []
    # R-826-2: copia esterna ATTIVA e copia sul Mac fallita: avviso senza «iCloud» fisso né
    # «non è riuscita» ripetuto
    monkeypatch.setenv("GAS_CRM_BACKUP_CIFRATO_DIR", str(tmp_path / "copie"))
    avvisi: List[str] = []
    stato = server.Stato(st, TOKEN, regole=REGOLE, avvisa=lambda t: (avvisi.append(t) or (True, "")))
    with monkeypatch.context() as m:
        m.setattr(st, "backup", lambda *a, **kw: None)
        server._copia_giornaliera(stato)
    assert len(avvisi) == 1 and "iCloud" not in avvisi[0]
    assert avvisi[0].lower().count("non è riuscita") == 1 and "nemmeno" in avvisi[0]
    monkeypatch.delenv("GAS_CRM_BACKUP_CIFRATO_DIR")
    vero_is_dir = Path.is_dir

    def is_dir_negato(self: Path) -> bool:
        if self == copia_cifrata.ICLOUD_DRIVE:
            raise PermissionError(1, "Operation not permitted")
        return vero_is_dir(self)

    monkeypatch.setattr(Path, "is_dir", is_dir_negato)
    assert copia_cifrata.cartella() == copia_cifrata.ICLOUD_DRIVE / copia_cifrata.NOME_CARTELLA
    assert copia_cifrata.motivo_spenta() is None
    esito = copia_cifrata.esito_all_avvio()
    # V-1 bot #388: il motivo dice che è iCloud Drive a non essere leggibile e cosa fare
    assert esito.startswith("NON FUNZIONA") and "iCloud Drive non è leggibile" in esito
    assert "GAS_CRM_BACKUP_CIFRATO_DIR" in esito
    monkeypatch.setattr(Path, "is_dir", vero_is_dir)
    # R-828-1: macOS lascia leggere iCloud Drive ma ne nega la scrittura: stesso consiglio,
    # all'avvio e nella copia. R-828-2: non suggerisce la variabile se è già impostata
    finto_icloud = tmp_path / "icloud"
    finto_icloud.mkdir()
    monkeypatch.setattr(copia_cifrata, "ICLOUD_DRIVE", finto_icloud)
    vero_mkdir = Path.mkdir

    def mkdir_negato(self: Path, *a: Any, **kw: Any) -> None:
        if finto_icloud in self.parents:
            raise PermissionError(1, "Operation not permitted")
        vero_mkdir(self, *a, **kw)

    monkeypatch.setattr(Path, "mkdir", mkdir_negato)
    esito = copia_cifrata.esito_all_avvio()
    assert esito.startswith("NON FUNZIONA") and "iCloud Drive non è leggibile" in esito
    assert "oppure imposta GAS_CRM_BACKUP_CIFRATO_DIR" in esito
    fuori, motivo = copia_cifrata.copia_fuori(st.backup(tmp_path / "locali_icloud"))
    assert fuori is None and "iCloud Drive non è leggibile" in (motivo or "")
    monkeypatch.setenv("GAS_CRM_BACKUP_CIFRATO_DIR", str(finto_icloud / "copie"))
    motivo = copia_cifrata.prova_scrittura() or ""
    assert "iCloud Drive non è leggibile" in motivo and "oppure imposta" not in motivo
    # V-3 bot #388 (R-829-1): un errore diverso dal permesso negato (disco pieno) non dà il
    # consiglio sui permessi, né nella copia né da solo
    import errno

    def mkdir_pieno(self: Path, *a: Any, **kw: Any) -> None:
        if finto_icloud in self.parents:
            raise OSError(errno.ENOSPC, "No space left on device")
        vero_mkdir(self, *a, **kw)

    monkeypatch.setattr(Path, "mkdir", mkdir_pieno)
    fuori, motivo = copia_cifrata.copia_fuori(st.backup(tmp_path / "locali_pieno"))
    assert fuori is None and "iCloud Drive non è leggibile" not in (motivo or "")
    assert "errore durante la copia cifrata" in (motivo or "")
    assert copia_cifrata._consiglio_icloud(finto_icloud / "x", OSError(errno.ENOSPC, "x")) is None
    # V-2 bot #388: collegamento simbolico verso iCloud Drive e maiuscole diverse riconosciuti
    scorciatoia = tmp_path / "scorciatoia"
    scorciatoia.symlink_to(finto_icloud)
    negato = PermissionError(1, "Operation not permitted")
    assert copia_cifrata._consiglio_icloud(scorciatoia / "copie", negato)
    assert copia_cifrata._consiglio_icloud(Path(str(finto_icloud).upper()) / "copie", negato)
    assert copia_cifrata._consiglio_icloud(tmp_path / "altrove", negato) is None
    monkeypatch.setattr(Path, "mkdir", vero_mkdir)
    monkeypatch.delenv("GAS_CRM_BACKUP_CIFRATO_DIR")
    monkeypatch.setattr(Path, "is_dir", is_dir_negato)
    stato = server.Stato(st, TOKEN, regole=REGOLE)
    copia = st.backup()
    assert copia is not None
    server._copia_esterna(stato, copia)
    assert stato.copia_esterna["ok"] is False and stato.copia_esterna["spenta"] is False


def test_note_minori_388(st: CRMStore, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Note minori su #388 (71137d27): R-830-1 (resto di prima dell'ultimo avvio tolto anche
    se il PID è di nuovo vivo), V-2 verifica esterna (sorgente che non c'è: messaggio che dice
    cosa controllare), V-3 bot (avviso senza «non riuscita» doppio)."""
    from modules.crm import copia_cifrata
    avvio_vero = copia_cifrata._avvio_sistema
    monkeypatch.setenv("GAS_CRM_BACKUP_PASSWORD", "una-password-lunga-1")
    monkeypatch.setenv("GAS_CRM_BACKUP_CIFRATO_DIR", str(tmp_path / "copie"))
    st.aggiungi_cliente("Anna Verdi", telefono="+393330000001")
    fuori, _ = copia_cifrata.copia_fuori(st.backup(tmp_path / "locali"))
    assert fuori is not None
    dest = tmp_path / "ripristinato.db"
    # R-830-1: PID vivo (il padre), file di 10 minuti fa, sistema avviato 5 minuti fa
    prima = dest.with_name(f"{dest.name}.{os.getppid()}-3.ripristino.tmp")
    prima.write_bytes(b"dati in chiaro di prima del riavvio")
    os.utime(prima, (time.time() - 600,) * 2)
    dopo = dest.with_name(f"{dest.name}.{os.getppid()}-4.ripristino.tmp")
    dopo.write_bytes(b"ripristino in corso dopo l'avvio")
    # R-834-2b: dentro il margine di 60 s prima dell'avvio il resto resta
    margine = dest.with_name(f"{dest.name}.{os.getppid()}-6.ripristino.tmp")
    margine.write_bytes(b"x")
    avvio_finto = time.time() - 300
    os.utime(margine, (avvio_finto - 30,) * 2)
    monkeypatch.setattr(copia_cifrata, "_avvio_sistema", lambda: avvio_finto)
    assert copia_cifrata.ripristina(fuori, dest, "una-password-lunga-1") == dest
    assert not prima.exists() and dopo.exists() and margine.exists()
    # ora di avvio sconosciuta: si decide come prima (PID vivo e file recente → resta)
    os.unlink(dest)
    ignoto = dest.with_name(f"{dest.name}.{os.getppid()}-5.ripristino.tmp")
    ignoto.write_bytes(b"x")
    os.utime(ignoto, (time.time() - 600,) * 2)
    monkeypatch.setattr(copia_cifrata, "_avvio_sistema", lambda: None)
    assert copia_cifrata.ripristina(fuori, dest, "una-password-lunga-1") == dest
    assert ignoto.exists()
    # lettura dell'ora di avvio di macOS e di questo sistema
    assert copia_cifrata._leggi_boottime(
        "{ sec = 1732000000, usec = 123456 } Wed Nov 20 10:00:00 2026") == 1732000000.0
    assert copia_cifrata._leggi_boottime("{ usec = 5, sec = 7 }") is None
    assert copia_cifrata._leggi_boottime("") is None
    monkeypatch.setattr(copia_cifrata, "_avvio_sistema", avvio_vero)
    # R-834-1: la lettura vera dell'ora di avvio. Su Linux /proc/stat c'è sempre
    avvio = copia_cifrata._avvio_sistema()
    if Path("/proc/stat").exists():
        assert avvio is not None and 0 < avvio <= time.time()
    # ramo di macOS: /proc/stat che non si apre e un sysctl finto (percorso completo)
    def proc_assente(*a: Any, **kw: Any) -> Any:
        raise FileNotFoundError(2, "No such file or directory")

    chiamate: List[List[str]] = []

    def sysctl_finto(argomenti: List[str], **kw: Any) -> Any:
        # R-835-1: anche gli argomenti con nome (uscita catturata come testo, tempo massimo)
        assert kw.get("capture_output") and kw.get("text") and kw.get("timeout") == 2
        chiamate.append(argomenti)
        return copia_cifrata.subprocess.CompletedProcess(
            argomenti, 0, stdout="{ sec = 1732000000, usec = 5 } Wed Nov 20 10:00:00 2026\n")

    with monkeypatch.context() as m:
        m.setattr(copia_cifrata, "open", proc_assente, raising=False)
        m.setattr(copia_cifrata.subprocess, "run", sysctl_finto)
        assert copia_cifrata._avvio_sistema() == 1732000000.0
        assert chiamate == [["/usr/sbin/sysctl", "-n", "kern.boottime"]]

        # nota #834: un'ora di avvio nel futuro non vale
        def sysctl_futuro(argomenti: List[str], **kw: Any) -> Any:
            return copia_cifrata.subprocess.CompletedProcess(
                argomenti, 0, stdout=f"{{ sec = {int(time.time()) + 3600}, usec = 0 }}")

        m.setattr(copia_cifrata.subprocess, "run", sysctl_futuro)
        assert copia_cifrata._avvio_sistema() is None
    # V-2 verifica esterna: sorgente che non c'è
    with pytest.raises(ErroreCRM, match="non riesco a leggere"):
        copia_cifrata.ripristina(tmp_path / "non_esiste.gascrm", tmp_path / "x.db",
                                 "una-password-lunga-1")
    # V-3 bot: copia esterna fallita per un errore qualsiasi, «riuscita» una volta sola
    avvisi: List[str] = []
    stato = server.Stato(st, TOKEN, regole=REGOLE,
                         avvisa=lambda t: (avvisi.append(t) or (True, "")))

    def scrittura_rotta(*a: Any, **kw: Any) -> None:
        raise OSError(5, "Input/output error")

    monkeypatch.setattr(copia_cifrata, "_scrivi_privato", scrittura_rotta)
    server._copia_esterna(stato, st.backup(tmp_path / "locali2"))
    assert stato.copia_esterna["ok"] is False and len(avvisi) == 1
    assert avvisi[0].lower().count("riuscita") == 1


def test_copia_cifrata_mai_in_chiaro_senza_libreria(tmp_path: Path,
                                                   monkeypatch: pytest.MonkeyPatch) -> None:
    import builtins
    from modules.crm import copia_cifrata
    monkeypatch.setenv("GAS_CRM_BACKUP_CIFRATO_DIR", str(tmp_path / "icloud"))
    monkeypatch.setenv("GAS_CRM_BACKUP_PASSWORD", "una-password-lunga-1")
    vero = builtins.__import__

    def senza(nome: str, *a: Any, **kw: Any) -> Any:
        if nome.startswith("cryptography"):
            raise ImportError(nome)
        return vero(nome, *a, **kw)

    monkeypatch.setattr(builtins, "__import__", senza)
    copia = tmp_path / "crm-20260101-000000.db"
    copia.write_bytes(b"dati")
    fuori, motivo = copia_cifrata.copia_fuori(copia)
    assert fuori is None and "cryptography" in (motivo or "")
    assert not (tmp_path / "icloud").exists()


def test_giro_automatico_due_volte_al_giorno() -> None:
    from modules.crm import __main__ as cli
    assert cli.SCAN_MINUTI_DEFAULT == 720


def test_invio_a_scaglioni(st: CRMStore, orologio: Orologio) -> None:
    srv = servizi_base(st)
    ids = [cliente_contento(st, srv, nome=f"C{i}", telefono=f"+3900000001{i:02d}")[0] for i in range(3)]
    proposte = motore.scansiona(st, regole=REGOLE).create
    assert len(proposte) == 3
    st.transiziona_proposta(proposte[0], "inviata", tetto_invii=(2, 60))
    st.transiziona_proposta(proposte[1], "inviata", tetto_invii=(2, 60))
    with pytest.raises(ErroreCRM, match="pausa anti-blocco"):
        st.transiziona_proposta(proposte[2], "inviata", tetto_invii=(2, 60))
    assert st.proposta(proposte[2])["stato"] == "da_approvare"  # type: ignore[index]
    orologio.ora = orologio.ora + timedelta(minutes=61)
    st.transiziona_proposta(proposte[2], "inviata", tetto_invii=(2, 60))
    assert len(st.invii_recenti(60)) == 1 and len(ids) == 3


def test_prelievo_controllato_alla_sua_data(st: CRMStore) -> None:
    srv = servizi_base(st)
    cid = st.aggiungi_cliente("Anna", telefono="+390000000046")
    pos = st.apri_posizione(cid, srv["oro"], data="2026-05-01", capitale_iniziale_cents=100_000)
    st.registra_movimento(pos, "deposito", 50_000, data="2026-05-20")
    with pytest.raises(ErroreCRM, match="capitale"):  # il 10 maggio c'erano solo 1.000 €
        st.registra_movimento(pos, "prelievo", 150_000, data="2026-05-10")
    st.registra_movimento(pos, "prelievo", 100_000, data="2026-05-10")
    st.registra_movimento(pos, "prelievo", 50_000, data="2026-05-25")
    assert analisi.metriche_cliente(dati(st), cid).capitale_cents == 0
    with pytest.raises(ErroreCRM, match="futuro"):
        st.apri_posizione(cid, srv["segnali"], data="2026-07-01")


def test_migrazione_di_un_db_della_prima_bozza(tmp_path: Path) -> None:
    db = tmp_path / ".gas_memory_crm.db"
    con = sqlite3.connect(db)
    con.execute("CREATE TABLE crm_clienti (id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT NOT NULL, "
                "telefono TEXT, email TEXT, stato TEXT NOT NULL DEFAULT 'attivo', "
                "consenso_marketing INTEGER NOT NULL DEFAULT 0, consenso_il TEXT, "
                "opt_out INTEGER NOT NULL DEFAULT 0, opt_out_il TEXT, presentato_da INTEGER, "
                "contatto_id INTEGER, note TEXT, creato_il TEXT NOT NULL, aggiornato_il TEXT NOT NULL)")
    con.execute("INSERT INTO crm_clienti (nome, creato_il, aggiornato_il) VALUES ('Vecchio', 'x', 'x')")
    con.commit()
    con.close()
    s = CRMStore(db)
    assert s.available and s.clienti()[0]["followup_attivo"] == 1
    assert "consigliato" in {r[1] for r in sqlite3.connect(db).execute("PRAGMA table_info(crm_servizi)")}


def test_identita_clienti_e_backup(st: CRMStore, tmp_path: Path) -> None:
    from modules.crm.store import identita_clienti
    st.aggiungi_cliente("Marco Bianchi", telefono="+393331234567", email="m@esempio.it")
    ident = identita_clienti(st.db_path)
    assert ident == [{"nome": "Marco Bianchi", "chiave": "m@esempio.it", "contatto": "+393331234567",
                      "merged_into": "crm", "stato": "chiuso"}]
    assert identita_clienti(tmp_path / "manca.db") == []
    cartella = tmp_path / "cartella.db"
    cartella.mkdir()
    assert identita_clienti(cartella) is None
    copie = tmp_path / "copie"
    # R-853-2: `keep` conta i giorni; `ultime` le copie più recenti dello stesso giorno
    primo = st.backup(copie, keep=2, ultime=2)
    assert primo is not None and CRMStore(primo).clienti()[0]["nome"] == "Marco Bianchi"
    st._orologio = lambda: INIZIO + timedelta(seconds=1)  # type: ignore[assignment]
    st.backup(copie, keep=2, ultime=2)
    st._orologio = lambda: INIZIO + timedelta(seconds=2)  # type: ignore[assignment]
    st.backup(copie, keep=2, ultime=2)
    assert len(list(copie.glob("crm-*.db"))) == 2


class _ClaudeFinto:
    def __init__(self, risposta: str, costo: float = 0.01) -> None:
        self.risposta, self.costo, self.visti = risposta, costo, []

    def __call__(self, modello: str, messaggi_: List[Dict[str, str]]) -> Tuple[str, float]:
        self.visti.append((modello, messaggi_))
        return self.risposta, self.costo


class _ClaudeCheFallisce:
    def __call__(self, modello: str, messaggi_: List[Dict[str, str]]) -> Tuple[str, float]:
        e = RuntimeError("tempo scaduto")
        e.costo_equivalente_usd = 0.2  # type: ignore[attr-defined]
        raise e


def _uso_forte(cartella: Path) -> float:
    return float(json.loads((cartella / ".gas_claude_cli_uso.json").read_text())["usd"])


def test_scrittore_opus(st: CRMStore, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    from modules.crm import scrittore
    monkeypatch.setattr(scrittore, "_senza_conto", False)
    srv = servizi_base(st)
    cliente_contento(st, srv)
    pid = motore.scansiona(st, regole=REGOLE).create[0]
    conto = tmp_path / "conto"
    conto.mkdir()
    finto = _ClaudeFinto("«Ciao Mario, ottimo mese! Ti va di provare Segnali VIP? Ne parliamo?»")
    p = scrittore.riscrivi(st, pid, chiedi=finto, root=conto)
    assert p["messaggio"].startswith("Ciao Mario, ottimo mese!") and p["messaggio"].endswith(messaggi.RIGA_STOP)
    modello, inviati = finto.visti[0]
    tutto = json.dumps(inviati, ensure_ascii=False)
    # minimizzazione: niente telefono, cognome, email
    assert "0000000001" not in tutto and "Rossi" not in tutto and "@" not in tutto and "Mario" in tutto
    assert st.conta_eventi_del_giorno("proposta", scrittore.NOTA_EVENTO) == 1
    # R-808-2: il costo entra nel conto del cervello forte del kernel
    assert _uso_forte(conto) == pytest.approx(0.01)
    with pytest.raises(ErroreCRM, match="contiene «garant»"):
        scrittore.riscrivi(st, pid, chiedi=_ClaudeFinto("Guadagno garantito, fidati!"), root=conto)
    assert st.proposta(pid)["messaggio"] == p["messaggio"]  # type: ignore[index]
    assert _uso_forte(conto) == pytest.approx(0.02)  # anche il testo scartato è consumo
    with pytest.raises(ErroreCRM, match="non ha risposto"):
        scrittore.riscrivi(st, pid, chiedi=_ClaudeCheFallisce(), root=conto)
    assert _uso_forte(conto) == pytest.approx(0.22)  # e la chiamata fallita dopo il consumo
    # R-808-2: il tetto conta i TENTATIVI (riuscito + scartato + fallito = 3)
    assert st.conta_eventi_del_giorno(scrittore.TIPO_TENTATIVO, scrittore.NOTA_TENTATIVO) == 3
    monkeypatch.setenv("GAS_CRM_OPUS_GIORNO", "3")
    with pytest.raises(ErroreCRM, match="tetto di oggi"):
        scrittore.riscrivi(st, pid, chiedi=finto, root=conto)
    assert len(finto.visti) == 1  # Claude non è stato chiamato
    monkeypatch.setenv("GAS_CRM_OPUS_GIORNO", "60")
    # tetto del forte raggiunto o conto illeggibile: niente chiamata
    monkeypatch.setenv("GAS_CLAUDE_CLI_TETTO_USD", "0.2")
    with pytest.raises(ErroreCRM, match="tetto giornaliero del cervello forte"):
        scrittore.riscrivi(st, pid, chiedi=finto, root=conto)
    monkeypatch.delenv("GAS_CLAUDE_CLI_TETTO_USD")
    (conto / ".gas_claude_cli_uso.json").write_text("rovinato")
    with pytest.raises(ErroreCRM, match="illeggibile"):
        scrittore.riscrivi(st, pid, chiedi=finto, root=conto)
    assert len(finto.visti) == 1
    # consumo non registrabile (cartella del conto inesistente): riscritture ferme
    with pytest.raises(ErroreCRM, match="non ha risposto"):
        scrittore.riscrivi(st, pid, chiedi=_ClaudeCheFallisce(), root=tmp_path / "manca")
    assert scrittore._senza_conto is True
    with pytest.raises(ErroreCRM, match="non si è potuto registrare"):
        scrittore.riscrivi(st, pid, chiedi=finto, root=tmp_path / "manca")
    monkeypatch.setattr(scrittore, "_senza_conto", False)
    monkeypatch.delenv("GAS_CLAUDE_CLI", raising=False)
    assert "spento" in (scrittore.disponibile() or "")
    with pytest.raises(ErroreCRM, match="spento"):
        scrittore.riscrivi(st, pid)  # senza Claude acceso: mai un altro modello
    monkeypatch.setenv("GAS_CLAUDE_CLI", "1")
    monkeypatch.setenv("GAS_CRM_MODELLO", "claude-sonnet-5-5")
    assert "non è Opus" in (scrittore.disponibile() or "")


def test_tetto_degli_eventi_atomico(st: CRMStore) -> None:
    import threading
    esiti: List[str] = []

    def prova() -> None:
        try:
            st.segna_evento_entro_tetto("opus", "tentativo", 3, motivo="tetto di oggi")
            esiti.append("ok")
        except ErroreCRM:
            esiti.append("no")

    fili = [threading.Thread(target=prova) for _ in range(8)]
    for f in fili:
        f.start()
    for f in fili:
        f.join()
    assert esiti.count("ok") == 3 and esiti.count("no") == 5
    assert st.conta_eventi_del_giorno("opus", "tentativo") == 3


def test_import_csv_doppio_bloccato(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    from modules.crm import __main__ as cli
    db = tmp_path / ".gas_memory_crm.db"
    s = CRMStore(db)
    srv = servizi_base(s)
    cid = s.aggiungi_cliente("Anna", telefono="+390000000051")
    s.apri_posizione(cid, srv["oro"], data="2026-01-01")
    monkeypatch.setenv("GAS_CRM_DB", str(db))
    f = tmp_path / "estratto.csv"
    f.write_text("telefono;servizio;tipo;importo;data;nota\n"
                 "+390000000051;oro;deposito;1.000;2026-01-02;\n", encoding="utf-8")
    assert cli.main(["import", str(f)]) == 0
    assert cli.main(["import", str(f)]) == 1  # stesso file due volte: fermato
    assert len(s.movimenti(cid)) == 1
    assert cli.main(["import", "--forza", str(f)]) == 0
    assert len(s.movimenti(cid)) == 2


def test_porta_dal_file_delle_chiavi(monkeypatch: pytest.MonkeyPatch) -> None:
    from modules.crm import __main__ as cli
    visto: Dict[str, int] = {}
    monkeypatch.delenv("GAS_CRM_PORT", raising=False)
    monkeypatch.setattr(cli, "_carica_chiavi", lambda: os.environ.__setitem__("GAS_CRM_PORT", "9123"))
    monkeypatch.setattr(cli, "cmd_serve", lambda a: visto.setdefault("porta", a.porta) and 0)
    cli.main(["serve"])
    os.environ.pop("GAS_CRM_PORT", None)
    assert visto["porta"] == 9123  # R-804-1: il .env si legge PRIMA del parser


def test_server_selezione_scaglioni_e_difese_nuove(avviato, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("GAS_CLAUDE_CLI", raising=False)
    stato, c, _ = avviato
    st = stato.store
    srv = servizi_base(st)
    a, _ = cliente_contento(st, srv)
    c.post("/api/login", {"token": TOKEN})
    codice, _, r = c.post("/api/proposte/selezionati", {"clienti": [a]})
    assert codice == 200 and len(r["risultato"]["create"]) == 1
    assert c.post("/api/proposte/selezionati", {"clienti": []})[0] == 400
    stato_d = c.get("/api/stato")[2]["server"]
    assert stato_d["invii"]["max"] == stato.regole.invii_per_lotto and "opus" in stato_d
    assert c.get("/api/stato", intestazioni={"Host": ""})[0] == 403
    assert c.post("/api/clienti", {"nome": "X", "consenso_marketing": "false"})[0] == 400
    cid = c.post("/api/clienti", {"nome": "Y", "telefono": "+390000000052"})[2]["risultato"]["id"]
    assert c.post("/api/posizioni", {"cliente_id": cid, "servizio_id": srv["oro"],
                                     "capitale_iniziale": "1,234"})[0] == 400
    assert st.posizioni(cid) == []  # importo sbagliato: nessuna posizione a metà
    assert c.post("/api/clienti/aggiorna", {"id": cid, "followup_attivo": False})[0] == 200
    assert st.cliente(cid)["followup_attivo"] == 0  # type: ignore[index]
    codice, _, err = c.post("/api/proposte/riscrivi", {"id": r["risultato"]["create"][0]})
    assert codice == 400 and "spento" in err["errore"]  # Claude spento: mai un altro modello


# ---------------------------------------------------------------------- Gas usa il CRM
# Decisione 18 del 23-11 (`reports/crm/decisioni.md`): Gas legge il CRM; scrive solo con
# la firma dell'operatore; gli importi solo se l'operatore li ha detti; niente
# cancellazioni; promemoria su Telegram.
from modules.crm import agente  # noqa: E402


def _conta(st: CRMStore, tabella: str) -> int:
    with sqlite3.connect(st.db_path) as con:
        return int(con.execute(f"SELECT COUNT(*) FROM {tabella}").fetchone()[0])


def test_agente_importi_nel_testo() -> None:
    t = "ha versato 1.500 euro, poi 250,50 e 3 mila; il 23/11 anche 2k. Mille no."
    trovati = agente.importi_nel_testo(t)
    for cents in (150_000, 25_050, 300_000, 200_000):
        assert cents in trovati
    assert 100_000 not in trovati  # «Mille» a parole non conta: il modello chiede la cifra
    # R-839-4: date, ore e #numeri non sono importi
    assert 2_300 not in trovati and 1_100 not in trovati
    assert agente.importi_nel_testo("oggi 20/06 alle 15:30, il #12, il 2026-06-20, "
                                    "il 20-06-2026, alle 9.45") == set()
    assert agente.importi_nel_testo(None) == set()  # type: ignore[arg-type]
    assert agente.importi_nel_testo("nessuna cifra") == set()


def test_agente_movimento_solo_con_importo_detto_e_firma(st: CRMStore) -> None:
    srv = servizi_base(st)
    cid, pid = cliente_contento(st, srv)
    prima = (_conta(st, "crm_movimenti"), _conta(st, "crm_eventi"))
    args = {"azione": "movimento", "cliente": "mario", "tipo": "deposito", "importo": "1.500"}
    with pytest.raises(ErroreCRM, match="non compare nei messaggi"):
        agente.prepara(st, args, "metti un deposito per Mario")
    with pytest.raises(ErroreCRM, match="non compare nei messaggi"):
        agente.prepara(st, args, None)
    can, desc = agente.prepara(st, args, "Mario ha versato 1500 euro")
    # la preparazione NON scrive: si scrive solo dopo la firma
    assert (_conta(st, "crm_movimenti"), _conta(st, "crm_eventi")) == prima
    assert can == {"v": 1, "azione": "movimento", "cliente_id": cid, "posizione_id": pid,
                   "tipo": "deposito", "importo_cents": 150_000, "data": "2026-06-20"}
    assert "«Mario Rossi» (cliente #" in desc and "DEPOSITO" in desc and "1.500,00 €" in desc
    assert agente.applica(st, json.loads(json.dumps(can))).startswith("Movimento registrato")
    assert _conta(st, "crm_movimenti") == prima[0] + 1


def test_agente_il_modello_non_salta_i_controlli(st: CRMStore) -> None:
    srv = servizi_base(st)
    cid, pid = cliente_contento(st, srv)
    # la forma canonica (id, centesimi) la scrive solo `prepara`: il modello non può darla
    with pytest.raises(ErroreCRM, match="non previsti"):
        agente.prepara(st, {"azione": "movimento", "cliente_id": cid, "posizione_id": pid,
                            "tipo": "deposito", "importo_cents": 999}, "999")
    # e `applica` accetta SOLO la forma canonica
    for finto in ({"azione": "movimento", "cliente": "Mario", "tipo": "deposito",
                   "importo": "10"},
                  {"v": 2, "azione": "stato_cliente", "cliente_id": cid, "stato": "perso"},
                  {"v": 1, "azione": "cancella_cliente", "cliente_id": cid},
                  "non un dizionario"):
        with pytest.raises(ErroreCRM):
            agente.applica(st, finto)
    # posizione di un altro cliente: rifiutata anche se la forma è canonica
    altro = st.aggiungi_cliente("Luca Verdi", telefono="+390000000077")
    with pytest.raises(ErroreCRM, match="non è di questo cliente"):
        agente.applica(st, {"v": 1, "azione": "movimento", "cliente_id": altro,
                            "posizione_id": pid, "tipo": "deposito",
                            "importo_cents": 100, "data": "2026-06-20"})
    with pytest.raises(ErroreCRM, match="azione non valida"):
        agente.prepara(st, {"azione": "cancella_cliente", "cliente": "Mario"}, "")


def test_agente_togliere_un_cliente_vuol_dire_archiviarlo(st: CRMStore) -> None:
    srv = servizi_base(st)
    cid, _ = cliente_contento(st, srv)
    assert "cancella" not in " ".join(agente.AZIONI)
    can, desc = agente.prepara(st, {"azione": "stato_cliente", "cliente": f"#{cid}",
                                    "stato": "perso"}, "")
    assert "non si cancella nulla" in desc
    agente.applica(st, can)
    c = st.cliente(cid)
    assert c is not None and c["stato"] == "perso" and _conta(st, "crm_clienti") == 1
    assert _conta(st, "crm_movimenti") > 0  # lo storico resta
    with pytest.raises(ErroreCRM, match="già nello stato"):
        agente.prepara(st, {"azione": "stato_cliente", "cliente": f"#{cid}", "stato": "perso"}, "")


def test_agente_nomi_ambigui_e_servizio_da_scegliere(st: CRMStore) -> None:
    srv = servizi_base(st)
    a, _ = cliente_contento(st, srv, nome="Mario Rossi")
    b, _ = cliente_contento(st, srv, nome="Mario Bianchi", telefono="+390000000002")
    with pytest.raises(ErroreCRM, match="più clienti") as e:
        agente.prepara(st, {"azione": "stato_cliente", "cliente": "mario", "stato": "in_pausa"}, "")
    assert f"#{a}" in str(e.value) and f"#{b}" in str(e.value)
    with pytest.raises(ErroreCRM, match="nessun cliente"):
        agente.prepara(st, {"azione": "stato_cliente", "cliente": "Giulia", "stato": "in_pausa"}, "")
    # il nome uguale vince sul pezzo di nome
    can, _ = agente.prepara(st, {"azione": "stato_cliente", "cliente": " mario  ROSSI ",
                                 "stato": "in_pausa"}, "")
    assert can["cliente_id"] == a
    st.apri_posizione(a, srv["segnali"], data="2026-05-01")
    args = {"azione": "movimento", "cliente": f"#{a}", "tipo": "commissione", "importo": "99"}
    with pytest.raises(ErroreCRM, match="più servizi"):
        agente.prepara(st, args, "99 euro")
    can, desc = agente.prepara(st, dict(args, servizio="segnali"), "99 euro")
    assert "Segnali VIP" in desc and can["importo_cents"] == 9_900
    with pytest.raises(ErroreCRM, match="non è nel servizio"):
        agente.prepara(st, dict(args, cliente=f"#{b}", servizio="segnali"), "99 euro")


def test_agente_errori_detti_prima_della_firma(st: CRMStore) -> None:
    srv = servizi_base(st)
    cid, _ = cliente_contento(st, srv)
    casi = [
        ({"azione": "nuovo_cliente", "nome": "Anna", "telefono": "+390000000001"}, "già del cliente"),
        ({"azione": "nuovo_cliente", "nome": "Anna", "email": "non-una-mail"}, "email non valida"),
        ({"azione": "nuovo_cliente", "nome": "  "}, "nome"),
        ({"azione": "movimento", "cliente": f"#{cid}", "tipo": "deposito", "importo": "10",
          "data": "2026-07-01"}, "futuro"),
        ({"azione": "movimento", "cliente": f"#{cid}", "tipo": "deposito", "importo": "10",
          "data": "2026-03-01"}, "prima dell'apertura"),
        ({"azione": "movimento", "cliente": f"#{cid}", "tipo": "regalo", "importo": "10"}, "tipo"),
        ({"azione": "apri_servizio", "cliente": f"#{cid}", "servizio": "oro"}, "già nel servizio"),
        ({"azione": "apri_servizio", "cliente": f"#{cid}", "servizio": "gestito",
          "data": "2026-12-01"}, "futuro"),
        ({"azione": "promemoria", "testo": "x", "quando": "2026-06-20 09:00"}, "già passata"),
        ({"azione": "promemoria", "testo": "x", "quando": "2029-01-01 09:00"}, "troppo lontano"),
        ({"azione": "promemoria", "testo": "x", "quando": "domani alle 9"}, "AAAA-MM-GG HH:MM"),
        ({"azione": "aggiorna_cliente", "cliente": f"#{cid}"}, "niente da cambiare"),
        ({"azione": "aggiorna_cliente", "cliente": f"#{cid}", "opt_out": "sì"}, "true o false"),
        ({"azione": "annulla_promemoria", "promemoria": "#99"}, "nessun promemoria"),
    ]
    prima = _conta(st, "crm_eventi")
    for args, attesa in casi:
        with pytest.raises(ErroreCRM, match=attesa):
            agente.prepara(st, args, "10")
    assert _conta(st, "crm_eventi") == prima


def test_agente_aggiorna_cliente_e_permessi(st: CRMStore) -> None:
    srv = servizi_base(st)
    cid, _ = cliente_contento(st, srv)
    ref = st.aggiungi_cliente("Luca Verdi", telefono="+390000000077")
    can, desc = agente.prepara(st, {"azione": "aggiorna_cliente", "cliente": "Mario Rossi",
                                    "opt_out": True, "telefono": "333 000 1111",
                                    "presentato_da": "luca"}, "")
    assert can["campi"] == {"telefono": "+393330001111", "opt_out": True, "presentato_da": ref}
    assert "STOP ai messaggi" in desc and "«Luca Verdi»" in desc
    assert "telefono: «+393330001111» (prima: «+390000000001»)" in desc  # R-839-7
    agente.applica(st, can)
    c = st.cliente(cid)
    assert c is not None and c["opt_out"] == 1 and c["telefono"] == "+393330001111"
    assert c["presentato_da"] == ref
    with pytest.raises(ErroreCRM, match="se stesso"):
        agente.applica(st, {"v": 1, "azione": "aggiorna_cliente", "cliente_id": cid,
                            "campi": {"presentato_da": cid}})


def test_promemoria_store_reclamo_unico_e_diario_senza_testo(st: CRMStore,
                                                             orologio: Orologio) -> None:
    cid = st.aggiungi_cliente("Mario Rossi")
    can, desc = agente.prepara(st, {"azione": "promemoria", "testo": "chiamare Mario per il bonifico",
                                    "quando": "2026-06-22 09:30", "cliente": "Mario"}, "")
    assert "lunedì 22-06-2026 alle 09:30" in desc and "«Mario Rossi»" in desc
    assert _conta(st, "crm_promemoria") == 0  # niente scritto prima della firma
    agente.applica(st, can)
    [p] = st.promemoria()
    assert p["cliente_id"] == cid and st.promemoria_scaduti() == []
    # il testo (può contenere nomi) non va nel diario del CRM, che non si anonimizza
    assert all("bonifico" not in e["descrizione"] for e in st.eventi())
    assert "Promemoria in attesa: 1" in agente.consulta(st, "promemoria")
    assert "chiamare Mario" in agente.consulta(st, "cliente", "Mario")
    orologio.avanti(2)  # 22-06 alle 10:00
    [scaduto] = st.promemoria_scaduti()
    assert scaduto["id"] == 1 and st.reclama_promemoria(True) is False  # type: ignore[arg-type]
    assert [r["id"] for r in st.promemoria_scaduti()] == [1]  # True non è l'id 1
    assert st.reclama_promemoria(scaduto["id"]) is True
    assert st.reclama_promemoria(scaduto["id"]) is False  # mai due invii
    assert st.promemoria_scaduti() == []
    st.rilascia_promemoria(scaduto["id"])  # invio fallito: torna in coda
    assert [r["id"] for r in st.promemoria_scaduti()] == [scaduto["id"]]
    assert st.reclama_promemoria(scaduto["id"]) is True
    assert st.promemoria() == [] and len(st.promemoria(solo_in_attesa=False)) == 1
    assert st.reclama_promemoria("x") is False  # type: ignore[arg-type]  # mai solleva


def test_promemoria_firma_in_ritardo_e_annullo(st: CRMStore, orologio: Orologio) -> None:
    can, _ = agente.prepara(st, {"azione": "promemoria", "testo": "fattura",
                                 "quando": "2026-06-20 11:00"}, "")
    orologio.ora = orologio.ora + timedelta(hours=3)  # la firma arriva dopo l'ora scelta
    agente.applica(st, can)  # si salva lo stesso e parte subito
    assert len(st.promemoria_scaduti()) == 1
    pid = st.aggiungi_promemoria("rinnovo", "2026-07-01 09:00")
    can, desc = agente.prepara(st, {"azione": "annulla_promemoria", "promemoria": pid}, "")
    assert "«rinnovo»" in desc
    agente.applica(st, can)
    assert [r["testo"] for r in st.promemoria()] == ["fattura"]
    with pytest.raises(ErroreCRM, match="nessun promemoria"):
        agente.applica(st, can)  # già annullato
    with pytest.raises(ErroreCRM, match="già annullato"):
        st.annulla_promemoria(pid)
    [scaduto] = st.promemoria_scaduti()
    st.reclama_promemoria(scaduto["id"])
    with pytest.raises(ErroreCRM, match="già mandato"):
        st.annulla_promemoria(scaduto["id"])


def test_agente_consulta_mai_solleva_e_resta_corta(st: CRMStore, tmp_path: Path) -> None:
    srv = servizi_base(st)
    cliente_contento(st, srv)
    assert agente.consulta(st, "boh").startswith("Errore: cosa non valida")
    assert agente.consulta(st, "cliente", None).startswith("Errore: cliente")
    assert agente.consulta(st, "cliente", "#999").startswith("Errore:")
    r = agente.consulta(st, "riepilogo")
    assert "Clienti attivi: 1" in r and "Capitale gestito" in r
    assert "#1 Mario Rossi" in agente.consulta(st, "clienti")
    assert "oro" in agente.consulta(st, "servizi")
    assert agente.consulta(st, "proposte").startswith(("Nessuna", "Proposte"))
    for i in range(150):
        st.aggiungi_cliente(f"Cliente {i:03d} " + "x" * 80)
    lungo = agente.consulta(st, "clienti")
    assert len(lungo) <= agente.USCITA_MAX + 60 and "tagliato" in lungo
    rotto = CRMStore(tmp_path / "manca" / "crm.db")
    rotto.db_path = tmp_path  # una cartella al posto del file: ogni lettura fallisce
    assert agente.consulta(rotto, "riepilogo").startswith("Errore:")
    # una lettura fallita non si scambia per «nessun promemoria»
    assert agente.consulta(rotto, "promemoria").startswith("Errore: database")


def test_agente_riserve_839(st: CRMStore) -> None:
    """Riserve della review #839-CRM: ricerca per nome solo a inizio parola (R-839-1),
    controlli prima della firma (R-839-2/3), id enormi (R-839-6), firma che mostra il
    valore sostituito (R-839-7)."""
    srv = servizi_base(st)
    ma, pma = cliente_contento(st, srv, nome="Marianna Verdi", telefono="+390000000011")
    ro, _ = cliente_contento(st, srv, nome="Mario Rossi", telefono="+390000000012")
    ri, _ = cliente_contento(st, srv, nome="Mario Rossini", telefono="+390000000013")
    stato = {"azione": "stato_cliente", "stato": "in_pausa"}
    # R-839-1: «Anna» non trova «Marianna»; il nome uguale vince; la somiglianza si dice
    with pytest.raises(ErroreCRM, match="nessun cliente"):
        agente.prepara(st, dict(stato, cliente="Anna"), "")
    can, desc = agente.prepara(st, dict(stato, cliente="mario rossi"), "")
    assert can["cliente_id"] == ro and "ATTENZIONE" not in desc
    can, desc = agente.prepara(st, dict(stato, cliente="rossin"), "")
    assert can["cliente_id"] == ri and "trovato per somiglianza «Mario Rossini»" in desc
    with pytest.raises(ErroreCRM, match="più clienti"):
        agente.prepara(st, dict(stato, cliente="mario ross"), "")
    can, desc = agente.prepara(st, dict(stato, cliente="MARIANNA"), "")
    assert can["cliente_id"] == ma and "somiglianza" in desc
    # nomi con apostrofo: «amico» trova «D'Amico» (per somiglianza, detto nella firma)
    dam = st.aggiungi_cliente("Gino D'Amico")
    can, desc = agente.prepara(st, dict(stato, cliente="amico"), "")
    assert can["cliente_id"] == dam and "somiglianza" in desc
    can, _ = agente.prepara(st, dict(stato, cliente="d'amico"), "")  # anche la ricerca si divide
    assert can["cliente_id"] == dam
    # omonimi anche con gli accenti
    st.aggiungi_cliente("Nicolò Ferrè")
    _, desc = agente.prepara(st, {"azione": "nuovo_cliente", "nome": "Nicolo Ferre"}, "")
    assert "esiste già un cliente con questo nome" in desc
    # R-839-2: importo detto anche per apri_servizio; telefono già usato in aggiorna
    args = {"azione": "apri_servizio", "cliente": f"#{ro}", "servizio": "gestito",
            "importo": "5.000"}
    with pytest.raises(ErroreCRM, match="non compare"):
        agente.prepara(st, args, "mettilo nel conto gestito")
    assert agente.prepara(st, args, "con 5000 euro")[0]["importo_cents"] == 500_000
    with pytest.raises(ErroreCRM, match="già del cliente"):
        agente.prepara(st, {"azione": "aggiorna_cliente", "cliente": f"#{ro}",
                            "telefono": "+390000000011"}, "")
    can, _ = agente.prepara(st, {"azione": "aggiorna_cliente", "cliente": f"#{ro}",
                                 "telefono": "+390000000012"}, "")  # il suo: va bene
    can, _ = agente.prepara(st, {"azione": "nuovo_cliente", "nome": "Gina Neri",
                                 "consenso_marketing": True}, "")
    nuovo = int(agente.applica(st, can).split("#")[1].rstrip("."))
    assert st.cliente(nuovo)["consenso_marketing"] == 1  # type: ignore[index]
    # R-839-3: prelievo oltre il capitale e riattivazione detti PRIMA della firma
    with pytest.raises(ErroreCRM, match="maggiore del capitale"):
        agente.prepara(st, {"azione": "movimento", "cliente": f"#{ma}", "tipo": "prelievo",
                            "importo": "50.000"}, "preleva 50.000")
    st.cambia_stato_posizione(pma, "chiusa")
    args = {"azione": "apri_servizio", "cliente": f"#{ma}", "servizio": "oro",
            "importo": "200", "data": "2026-03-01"}
    with pytest.raises(ErroreCRM, match="prima dell'apertura"):
        agente.prepara(st, args, "200")
    can, desc = agente.prepara(st, dict(args, data="2026-06-10"), "200")
    assert desc.startswith("Riattiva «Marianna Verdi»") and "aperto dal 2026-04-01" in desc
    agente.applica(st, can)
    # R-839-6: id enormi → ErroreCRM, mai OverflowError
    with pytest.raises(ErroreCRM):
        agente.prepara(st, dict(stato, cliente=2**70), "")
    with pytest.raises(ErroreCRM):
        agente.applica(st, {"v": 1, "azione": "stato_cliente", "cliente_id": 2**70,
                            "stato": "perso"})
    with pytest.raises(ErroreCRM, match="campi"):
        agente.applica(st, {"v": 1, "azione": "aggiorna_cliente", "cliente_id": ro,
                            "campi": "nome"})
    # R-839-7: la firma mostra la nota che viene sostituita
    st.aggiorna_cliente(ro, note="paga sempre puntuale")
    _, desc = agente.prepara(st, {"azione": "aggiorna_cliente", "cliente": f"#{ro}",
                                  "note": "ha chiamato"}, "")
    assert "SOSTITUISCE la nota attuale «paga sempre puntuale» con «ha chiamato»" in desc
    # promemoria annullato: mai reclamato; id non interi rifiutati
    pid = st.aggiungi_promemoria("x", "2020-01-01 09:00", nel_passato=True)
    st.annulla_promemoria(pid)
    assert st.reclama_promemoria(pid) is False and st.reclama_promemoria(True) is False


def test_backup_tiene_i_giorni_anche_con_tanti_riavvii(tmp_path: Path) -> None:
    """R-853-2: un CRM che si riavvia a ripetizione fa una copia per avvio; prima si
    tenevano solo le ultime 30 copie e in pochi minuti sparivano i giorni prima."""
    orologio = Orologio(datetime(2026, 10, 1, 9, 0, tzinfo=timezone.utc))
    st = CRMStore(tmp_path / "crm.db", orologio=orologio)
    st.aggiungi_cliente("Mario Rossi")
    cartella = tmp_path / "copie"
    for _ in range(40):  # una copia al giorno per 40 giorni
        assert st.backup(cartella) is not None
        orologio.avanti(1)
    for i in range(60):  # poi 60 riavvii nello stesso giorno, uno al secondo
        orologio.ora = orologio.ora + timedelta(seconds=1)
        assert st.backup(cartella) is not None
    copie = sorted(p.name for p in cartella.glob("crm-*.db"))
    giorni = sorted({c[4:12] for c in copie})
    assert len(giorni) == 30  # gli ultimi 30 giorni restano tutti
    assert giorni[0] == "20261012" and giorni[-1] == "20261110"  # 41 giorni, restano gli ultimi 30
    oggi = [c for c in copie if c[4:12] == "20261110"]
    assert len(oggi) == 10  # dello stesso giorno solo le ultime 10
    assert len(copie) == 29 + 10


def test_backup_con_orologio_indietro_non_cancella_la_copia_appena_fatta(tmp_path: Path) -> None:
    """V-1 verifica esterna #404: 12 copie nello stesso giorno, poi l'orologio del Mac torna
    indietro di un'ora. La copia nuova ha un nome «più vecchio» delle ultime 10 e veniva
    cancellata subito: backup() restituiva un percorso che non esisteva più."""
    orologio = Orologio(datetime(2026, 11, 24, 9, 0, tzinfo=timezone.utc))
    st = CRMStore(tmp_path / "crm.db", orologio=orologio)
    st.aggiungi_cliente("Mario Rossi")
    cartella = tmp_path / "copie"
    for _ in range(12):
        orologio.ora = orologio.ora + timedelta(seconds=1)
        assert st.backup(cartella) is not None
    orologio.ora = orologio.ora - timedelta(hours=1)
    nuova = st.backup(cartella)
    assert nuova is not None and nuova.exists()
    assert len(list(cartella.glob("crm-*.db"))) == 11  # le ultime 10 più quella appena fatta


def test_backup_copie_nel_futuro_non_accorciano_la_storia(tmp_path: Path,
                                                         caplog: pytest.LogCaptureFixture) -> None:
    """V-3 bot / V-1 verifica esterna #404 (2° giro): con l'orologio andato nel 2030 e poi
    corretto, quelle copie occupavano le «ultime 10» e un giorno dei 30 finché l'orologio non
    le raggiungeva. Ora non contano, non si cancellano e lo si scrive nel registro."""
    orologio = Orologio(datetime(2030, 1, 1, 9, 0, tzinfo=timezone.utc))
    st = CRMStore(tmp_path / "crm.db", orologio=orologio)
    st.aggiungi_cliente("Mario Rossi")
    cartella = tmp_path / "copie"
    for _ in range(12):
        orologio.ora = orologio.ora + timedelta(seconds=1)
        assert st.backup(cartella) is not None
    orologio.ora = datetime(2026, 10, 1, 9, 0, tzinfo=timezone.utc)
    with caplog.at_level("WARNING"):
        for _ in range(40):
            assert st.backup(cartella) is not None
            orologio.avanti(1)
    nomi = sorted(p.name for p in cartella.glob("crm-*.db"))
    # nel 2030 la regola normale ne ha tenute 10; dopo, con l'orologio giusto, non si toccano
    assert len([n for n in nomi if n.startswith("crm-2030")]) == 10
    giorni_veri = sorted({n[4:12] for n in nomi if n.startswith("crm-2026")})
    assert len(giorni_veri) == 30  # i 30 giorni veri restano tutti
    assert "data nel futuro" in caplog.text


def test_backup_margine_del_futuro_e_di_un_giorno(tmp_path: Path,
                                                 caplog: pytest.LogCaptureFixture) -> None:
    """R-858-2: una copia avanti di qualche ora (cambio d'ora, fuso) conta come le altre; una
    avanti di 2 giorni è «nel futuro»: non conta e non si cancella."""
    orologio = Orologio(datetime(2026, 11, 24, 9, 0, tzinfo=timezone.utc))
    st = CRMStore(tmp_path / "crm.db", orologio=orologio)
    st.aggiungi_cliente("Mario Rossi")
    cartella = tmp_path / "copie"
    cartella.mkdir()
    for nome in ("crm-20261123-090000.db", "crm-20261124-200000.db", "crm-20261126-100000.db"):
        (cartella / nome).write_text("copia")
    with caplog.at_level("WARNING"):
        assert st.backup(cartella, keep=1, ultime=1) is not None
    nomi = sorted(p.name for p in cartella.glob("crm-*.db"))
    # quella di stasera conta (è la più recente del giorno) e fa togliere quella di ieri
    assert nomi == ["crm-20261124-090000.db", "crm-20261124-200000.db", "crm-20261126-100000.db"]
    assert "1 copie locali con una data nel futuro" in caplog.text


def test_backup_ignora_le_copie_fatte_a_mano(tmp_path: Path) -> None:
    """V-1 bot #404: «crm-prima-import.db» dava il giorno «prima-im», dopo ogni data: occupava
    per sempre uno dei 30 giorni e ne restavano 29 veri. Ora i nomi fuori formato non contano
    e non si toccano."""
    orologio = Orologio(datetime(2026, 10, 1, 9, 0, tzinfo=timezone.utc))
    st = CRMStore(tmp_path / "crm.db", orologio=orologio)
    st.aggiungi_cliente("Mario Rossi")
    cartella = tmp_path / "copie"
    cartella.mkdir()
    a_mano = cartella / "crm-prima-import.db"
    a_mano.write_text("copia fatta a mano")
    for _ in range(31):
        assert st.backup(cartella) is not None
        orologio.avanti(1)
    giorni = sorted({c.name[4:12] for c in cartella.glob("crm-2*.db")})
    assert len(giorni) == 30 and giorni[0] == "20261002"
    assert a_mano.read_text() == "copia fatta a mano"


# ---------------------------------------------------------------- script del CRM sul Mac
# R-853-3: installa.sh e spegni.sh provati con comandi finti (uname, launchctl, plutil, curl,
# sleep e il python della .venv), come l'installer della voce in test_unit_voce_ascolto.py.

CRM_SCRIPT_DIR = Path(__file__).resolve().parent.parent / "scripts" / "crm"

_FINTI_CRM = {
    "uname": 'echo "${UNAME_FINTO:-Darwin}"',
    "launchctl": ('echo "launchctl $*" >> "$REGISTRO"\n'
                  'case "$1" in\n'
                  '  print) [ -f "$REGISTRO.caricato" ] ;;\n'
                  '  bootout)\n'
                  '    # R-856-1: al bootout il plist deve essere già tolto (si registra com\'è)\n'
                  '    [ -f "$HOME/Library/LaunchAgents/com.gas.crm.plist" ] && echo "bootout-plist si" >> "$REGISTRO" \\\n'
                  '      || echo "bootout-plist no" >> "$REGISTRO"\n'
                  '    # CTRLC2=si: secondo Ctrl+C mentre la pulizia fa il bootout\n'
                  '    if [ "${CTRLC2:-no}" = si ] && [ -f "$REGISTRO.ctrlc" ] && [ ! -f "$REGISTRO.ctrlc2" ]; then\n'
                  '      touch "$REGISTRO.ctrlc2"; kill -INT -- "-$PPID"\n'
                  '    fi\n'
                  '    rm -f "$REGISTRO.caricato" ;;\n'
                  '  bootstrap)\n'
                  '    if [ "${LC_BOOT:-ok}" != ok ]; then echo "Bootstrap failed: 5" >&2; exit 5; fi\n'
                  '    touch "$REGISTRO.caricato"\n'
                  '    [ -n "${RIGA_COPIA:-}" ] && echo "$RIGA_COPIA" >> "$LOG_CRM"\n'
                  '    exit 0 ;;\n'
                  'esac'),
    "plutil": 'echo "plutil $*" >> "$REGISTRO"; [ "${PLUTIL:-ok}" = ok ]',
    # RM_KO=si: il plist non si riesce a togliere (cartella non scrivibile); il resto passa a /bin/rm
    "rm": ('if [ "${RM_KO:-no}" = si ]; then\n'
           '  for a in "$@"; do case "$a" in *com.gas.crm.plist) exit 1 ;; esac; done\n'
           'fi\n'
           'exec /bin/rm "$@"'),
    # la dashboard risponde solo col servizio caricato (DASH=ok) o sempre (DASH=occupata)
    "curl": ('case "${DASH:-ok}" in occupata) exit 0 ;; ok) [ -f "$REGISTRO.caricato" ] ;;'
             ' *) exit 7 ;; esac'),
    # CTRLC=si: al primo sleep col servizio caricato, Ctrl+C a tutto il gruppo (come nel Terminale)
    "sleep": ('echo "sleep $*" >> "$REGISTRO"\n'
              'if [ "${CTRLC:-no}" = si ] && [ -f "$REGISTRO.caricato" ] && [ ! -f "$REGISTRO.ctrlc" ]; then\n'
              '  touch "$REGISTRO.ctrlc"; kill -INT -- "-$PPID"\n'
              'fi\n'
              'exit 0'),
}


def _gas_crm_finto(tmp_path: Path, nome: str = "Gas", esito_python: int = 0) -> Tuple[Path, Path, Path]:
    gas = tmp_path / nome
    (gas / "scripts" / "crm").mkdir(parents=True)
    for f in CRM_SCRIPT_DIR.iterdir():
        shutil.copy2(f, gas / "scripts" / "crm" / f.name)
    casa = tmp_path / "casa"
    (casa / "Desktop").mkdir(parents=True)
    # il controllo del .env gira con `env -i HOME=… PATH=…`: il python finto legge l'esito da HOME
    (casa / "python_esito").write_text(str(esito_python))
    (gas / ".venv" / "bin").mkdir(parents=True)
    py = gas / ".venv/bin/python"
    py.write_text('#!/bin/bash\ncat > /dev/null\ne="$(cat "$HOME/python_esito")"\n'
                  '[ "$e" = 0 ] && echo 8770\nexit "$e"\n')
    py.chmod(0o755)
    finti = tmp_path / "finti"
    finti.mkdir()
    for nome_cmd, corpo in _FINTI_CRM.items():
        p = finti / nome_cmd
        p.write_text("#!/bin/bash\n" + corpo + "\n")
        p.chmod(0o755)
    return gas, finti, casa


def _segnali_normali() -> None:
    """R-855-3: se pytest parte con SIGINT ignorato (nohup, & senza job control) bash non
    potrebbe intercettarlo e i test del Ctrl+C darebbero un rosso falso."""
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    signal.signal(signal.SIGTERM, signal.SIG_DFL)


def _esegui_crm(gas: Path, finti: Path, casa: Path, tmp_path: Path, script: str = "installa.sh",
                **extra: str) -> Tuple[subprocess.CompletedProcess, str]:
    registro = tmp_path / "registro.txt"
    env = {"PATH": f"{finti}:/usr/bin:/bin", "HOME": str(casa), "REGISTRO": str(registro),
           "LOG_CRM": str(gas / ".gas_memory_crm_server.log"), **extra}
    r = subprocess.run(["bash", str(gas / "scripts/crm" / script)], capture_output=True,
                       text=True, timeout=60, env=env, start_new_session=True,
                       preexec_fn=_segnali_normali)
    return r, registro.read_text() if registro.exists() else ""


def _plist_crm(casa: Path) -> Path:
    return casa / "Library/LaunchAgents/com.gas.crm.plist"


def _caricato(tmp_path: Path) -> bool:
    return (tmp_path / "registro.txt.caricato").exists()


def _bootout_col_plist_gia_tolto(registro: str) -> bool:
    """R-856-1: nella pulizia il plist si toglie PRIMA del bootout (se la pulizia si
    interrompe, al login launchd non lo ricarica)."""
    righe = registro.splitlines()
    scritto = next(i for i, x in enumerate(righe) if x.startswith("plutil"))
    dopo = [x for x in righe[scritto:] if x.startswith("bootout-plist")]
    return bool(dopo) and all(x == "bootout-plist no" for x in dopo)


def test_installa_crm_arriva_in_fondo(tmp_path: Path) -> None:
    gas, finti, casa = _gas_crm_finto(tmp_path)
    log = gas / ".gas_memory_crm_server.log"
    log.write_text("Copia cifrata giornaliera fuori dal Mac: RIGA VECCHIA\n")
    r, registro = _esegui_crm(gas, finti, casa, tmp_path,
                              RIGA_COPIA="Copia cifrata giornaliera fuori dal Mac: ATTIVA")
    assert r.returncode == 0, r.stdout + r.stderr
    p = plistlib.loads(_plist_crm(casa).read_bytes())
    assert p["Label"] == "com.gas.crm" and str(gas) in str(p) and "CARTELLA_GAS" not in str(p)
    assert _caricato(tmp_path) and f"launchctl bootstrap gui/{os.getuid()}" in registro
    icona = plistlib.loads((casa / "Desktop/CRM Gas.webloc").read_bytes())
    assert icona == {"URL": "http://127.0.0.1:8770/"}  # solo l'indirizzo, niente token
    assert "Aspetto che la dashboard risponda" in r.stdout
    # si mostra l'esito della copia cifrata di QUESTO avvio, non una riga vecchia del registro
    assert "fuori dal Mac: ATTIVA" in r.stdout and "RIGA VECCHIA" not in r.stdout


@pytest.mark.parametrize("esito, messaggio", [
    (2, "manca GAS_CRM_TOKEN"),
    (3, "GAS_CRM_BIND diverso da 127.0.0.1"),
    (4, "Gas non si avvia con le sue dipendenze"),
    (1, "controllo del CRM non riuscito"),
])
def test_installa_crm_controllo_del_env_si_ferma_prima_del_servizio(
        tmp_path: Path, esito: int, messaggio: str) -> None:
    gas, finti, casa = _gas_crm_finto(tmp_path, esito_python=esito)
    r, registro = _esegui_crm(gas, finti, casa, tmp_path)
    assert r.returncode == 1 and messaggio in r.stderr, r.stdout + r.stderr
    assert not _plist_crm(casa).exists() and "bootstrap" not in registro


def test_installa_crm_solo_sul_mac(tmp_path: Path) -> None:
    gas, finti, casa = _gas_crm_finto(tmp_path)
    r, registro = _esegui_crm(gas, finti, casa, tmp_path, UNAME_FINTO="Linux")
    assert r.returncode == 1 and "per il Mac" in r.stderr and registro == ""


def test_installa_crm_cartella_con_caratteri_non_ammessi(tmp_path: Path) -> None:
    gas, finti, casa = _gas_crm_finto(tmp_path, nome="Gas'x")
    r, registro = _esegui_crm(gas, finti, casa, tmp_path)
    assert r.returncode == 1 and "caratteri non ammessi" in r.stderr and registro == ""


def test_installa_crm_porta_gia_occupata(tmp_path: Path) -> None:
    gas, finti, casa = _gas_crm_finto(tmp_path)
    r, registro = _esegui_crm(gas, finti, casa, tmp_path, DASH="occupata")
    assert r.returncode == 1 and "risponde già qualcosa" in r.stderr
    assert not _plist_crm(casa).exists() and "bootstrap" not in registro


@pytest.mark.parametrize("extra, messaggio", [
    ({"PLUTIL": "ko"}, "plist non valido"),
    ({"LC_BOOT": "ko"}, "3 tentativi"),
    ({"DASH": "muta"}, "la dashboard non risponde"),
])
def test_installa_crm_ogni_stop_dopo_il_plist_toglie_il_servizio(
        tmp_path: Path, extra: Dict[str, str], messaggio: str) -> None:
    """R-853-1: dopo la scrittura del plist ogni STOP lo toglie, se no al login launchd
    ricarica il CRM senza il controllo della dashboard."""
    gas, finti, casa = _gas_crm_finto(tmp_path)
    r, registro = _esegui_crm(gas, finti, casa, tmp_path, **extra)
    assert r.returncode == 1 and messaggio in r.stderr, r.stdout + r.stderr
    assert not _plist_crm(casa).exists() and not _caricato(tmp_path)
    assert not (casa / "Desktop/CRM Gas.webloc").exists()
    assert _bootout_col_plist_gia_tolto(registro)
    if extra.get("LC_BOOT"):
        righe = registro.splitlines()
        assert sum(x.startswith("launchctl bootstrap") for x in righe) == 3
        ultimo = max(i for i, x in enumerate(righe) if x.startswith("launchctl bootstrap"))
        assert any(x.startswith("launchctl bootout") for x in righe[ultimo:])


def test_installa_crm_ctrl_c_mentre_aspetta_toglie_il_servizio(tmp_path: Path) -> None:
    """R-854-1: Ctrl+C durante l'attesa della dashboard lasciava il servizio caricato e il
    plist al suo posto, senza nessun controllo."""
    gas, finti, casa = _gas_crm_finto(tmp_path)
    r, registro = _esegui_crm(gas, finti, casa, tmp_path, DASH="muta", CTRLC="si")
    assert (tmp_path / "registro.txt.ctrlc").exists()
    assert r.returncode == 130 and "interrotto, servizio tolto" in r.stderr, r.stdout + r.stderr
    assert not _plist_crm(casa).exists() and not _caricato(tmp_path)
    assert _bootout_col_plist_gia_tolto(registro)


def test_installa_crm_plist_che_non_si_toglie_lo_dice_e_fa_il_bootout(tmp_path: Path) -> None:
    """R-856-2: con set -e un rm del plist fallito chiudeva la pulizia prima del bootout:
    servizio ancora caricato e nessun messaggio."""
    gas, finti, casa = _gas_crm_finto(tmp_path)
    r, _ = _esegui_crm(gas, finti, casa, tmp_path, DASH="muta", RM_KO="si")
    assert r.returncode == 1, r.stdout + r.stderr
    assert "non riesco a togliere" in r.stderr and "la dashboard non risponde" in r.stderr
    assert not _caricato(tmp_path)


def test_installa_crm_secondo_ctrl_c_non_interrompe_la_pulizia(tmp_path: Path) -> None:
    """R-855-1 / R-856-1: un secondo Ctrl+C mentre la pulizia fa il bootout la interrompeva
    a metà: servizio ancora caricato e «servizio tolto» scritto due volte (falso)."""
    gas, finti, casa = _gas_crm_finto(tmp_path)
    r, _ = _esegui_crm(gas, finti, casa, tmp_path, DASH="muta", CTRLC="si", CTRLC2="si")
    assert (tmp_path / "registro.txt.ctrlc2").exists()
    assert r.returncode == 130, r.stdout + r.stderr
    assert r.stderr.count("servizio tolto") == 1
    assert not _plist_crm(casa).exists() and not _caricato(tmp_path)


def test_installa_crm_ctrl_c_dopo_la_dashboard_lascia_il_servizio(tmp_path: Path) -> None:
    """Con la dashboard che risponde il servizio è provato: un Ctrl+C mentre si aspetta
    l'esito della copia cifrata non lo toglie."""
    gas, finti, casa = _gas_crm_finto(tmp_path)
    r, _ = _esegui_crm(gas, finti, casa, tmp_path, CTRLC="si")
    assert (tmp_path / "registro.txt.ctrlc").exists()
    assert r.returncode in (130, -signal.SIGINT), r.stdout + r.stderr
    assert "servizio tolto" not in r.stderr  # R-855-2: niente messaggio falso
    assert _plist_crm(casa).exists() and _caricato(tmp_path)


def test_installa_crm_seconda_volta_aspetta_lo_spegnimento(tmp_path: Path) -> None:
    gas, finti, casa = _gas_crm_finto(tmp_path)
    (tmp_path / "registro.txt.caricato").touch()  # CRM già acceso da un'installazione prima
    r, registro = _esegui_crm(gas, finti, casa, tmp_path)
    assert r.returncode == 0, r.stdout + r.stderr
    righe = registro.splitlines()
    fuori = righe.index(f"launchctl bootout gui/{os.getuid()}/com.gas.crm")
    dentro = next(i for i, x in enumerate(righe) if x.startswith("launchctl bootstrap"))
    assert fuori < dentro and f"launchctl print gui/{os.getuid()}/com.gas.crm" in righe[fuori:dentro]


def test_spegni_crm_toglie_servizio_e_icona_e_lascia_i_dati(tmp_path: Path) -> None:
    gas, finti, casa = _gas_crm_finto(tmp_path)
    r, _ = _esegui_crm(gas, finti, casa, tmp_path)
    assert r.returncode == 0
    dati = gas / ".gas_memory_crm.db"
    dati.write_text("dati dei clienti")
    r, registro = _esegui_crm(gas, finti, casa, tmp_path, script="spegni.sh")
    assert r.returncode == 0 and "CRM spento" in r.stdout
    assert not _plist_crm(casa).exists() and not _caricato(tmp_path)
    assert not (casa / "Desktop/CRM Gas.webloc").exists() and dati.read_text() == "dati dei clienti"
