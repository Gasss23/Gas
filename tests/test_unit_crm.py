"""Test del CRM clienti (modules/crm): soldi esatti, registro immutabile, motore delle
opportunità, testi WhatsApp, server della dashboard. Zero rete esterna, zero token:
il server gira su 127.0.0.1 con porta scelta dal sistema, l'orologio è finto."""
from __future__ import annotations

import http.client
import json
import os
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
    assert len(list(icloud.glob("crm-*.gascrm"))) == 2


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
    assert fuori2 is None and "non riuscita" in (motivo2 or "")
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
    primo = st.backup(copie, keep=2)
    assert primo is not None and CRMStore(primo).clienti()[0]["nome"] == "Marco Bianchi"
    st._orologio = lambda: INIZIO + timedelta(seconds=1)  # type: ignore[assignment]
    st.backup(copie, keep=2)
    st._orologio = lambda: INIZIO + timedelta(seconds=2)  # type: ignore[assignment]
    st.backup(copie, keep=2)
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
