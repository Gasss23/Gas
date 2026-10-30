"""Test per scripts/bot_esito.py e .github/workflows/verifica-bot.yml (V-B vera).

Zero rete, zero token: la logica di decisione è pura; i comandi smista/esito girano con
un `gh` finto preposto al PATH; il workflow è controllato staticamente (YAML).
"""
import json
import os
import subprocess
import sys
import unicodedata
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).parent.parent
SCRIPT = ROOT / "scripts" / "bot_esito.py"
WORKFLOW = ROOT / ".github" / "workflows" / "verifica-bot.yml"
sys.path.insert(0, str(ROOT / "scripts"))
import bot_esito as be  # noqa: E402

SHA = "a" * 40
SHA2 = "b" * 40


def _verdetto(esito="APPROVATO", finding=None, testo=None):
    finding = [] if finding is None else finding
    if testo is None:
        righe = [f"VERIFICA ESTERNA #130 — {esito}", "Metodo: lettura", "CLAIM VERIFICATI: ok",
                 "FINDING:"]
        righe += [f"{f['id']} ({f['gravita']}) — {f['descrizione']}" for f in finding] or ["nessuno"]
        righe += ["NON VERIFICATO: test", "RACCOMANDAZIONE: merge"]
        testo = "\n".join(righe)
    return {"strumenti_ok": True, "verdetto": esito, "finding": finding, "testo": testo}


def _f(id_, gravita):
    return {"id": id_, "gravita": gravita, "descrizione": "d"}


# ---------------------------------------------------------------------------
# decidi(): la soglia dell'operatore (2026-10-05) — niente ALTA/MEDIA
# ---------------------------------------------------------------------------

class TestDecidi:
    def test_approvato_pulito(self):
        assert be.decidi(_verdetto(), SHA, SHA)[0] == "APPROVE"

    def test_riserve_minori_approvate(self):
        v = _verdetto("APPROVATO CON RISERVE", [_f("V-1", "BASSA"), _f("V-2", "COSMETICA")])
        assert be.decidi(v, SHA, SHA)[0] == "APPROVE"

    @pytest.mark.parametrize("gravita", ["ALTA", "MEDIA"])
    def test_riserva_bloccante(self, gravita):
        v = _verdetto("APPROVATO CON RISERVE", [_f("V-1", "BASSA"), _f("V-2", gravita)])
        evento, motivo = be.decidi(v, SHA, SHA)
        assert evento == "COMMENT" and gravita in motivo

    def test_bocciato(self):
        assert be.decidi(_verdetto("BOCCIATO"), SHA, SHA) == ("COMMENT", "verdetto BOCCIATO")

    # Verifica non conclusa: nessun giudizio, si può rilanciare (non è un NO definitivo, G-2).
    def test_head_cambiata(self):
        evento, motivo = be.decidi(_verdetto(), SHA, SHA2)
        assert evento == "RIPROVA" and "head cambiata" in motivo

    @pytest.mark.parametrize("analizzata,attuale", [("", SHA), (SHA, ""), ("", "")])
    def test_head_vuota(self, analizzata, attuale):
        assert be.decidi(_verdetto(), analizzata, attuale)[0] == "RIPROVA"

    def test_head_cambiata_blocca_anche_doc_only(self):
        assert be.decidi(None, SHA, SHA2, doc_only=True)[0] == "RIPROVA"

    def test_doc_only_senza_verdetto(self):
        assert be.decidi(None, SHA, SHA, doc_only=True)[0] == "APPROVE"

    @pytest.mark.parametrize("verdetto", [None, "APPROVATO", []])
    def test_verifica_non_eseguita_si_riprova(self, verdetto):
        assert be.decidi(verdetto, SHA, SHA)[0] == "RIPROVA"

    @pytest.mark.parametrize("verdetto", [
        {"strumenti_ok": True},
        {"strumenti_ok": True, "verdetto": "APPROVATO", "finding": []},                       # testo mancante
        {"strumenti_ok": True, "verdetto": "APPROVATO", "finding": [], "testo": "   "},        # testo vuoto
        {"strumenti_ok": True, "verdetto": "APPROVATO", "testo": "VERIFICA ESTERNA — APPROVATO"},  # finding mancante
        {"strumenti_ok": True, "verdetto": "OK", "finding": [], "testo": "VERIFICA ESTERNA — OK"},
    ])
    def test_verdetto_illeggibile(self, verdetto):
        assert be.decidi(verdetto, SHA, SHA)[0] == "COMMENT"

    # R-196-1 (terza prova #142): senza diff e CI letti il verdetto è alla cieca → RIPROVA,
    # mai un sì né un NO definitivo; campo assente o non booleano True = alla cieca.
    @pytest.mark.parametrize("valore", [False, None, "true", 1, "si"])
    @pytest.mark.parametrize("esito", ["APPROVATO", "BOCCIATO"])
    def test_strumenti_non_ok_si_riprova(self, valore, esito):
        v = _verdetto(esito)
        v["strumenti_ok"] = valore
        evento, motivo = be.decidi(v, SHA, SHA)
        assert evento == "RIPROVA" and "alla cieca" in motivo

    def test_strumenti_assente_si_riprova(self):
        v = _verdetto("APPROVATO CON RISERVE", [_f("V-1", "MEDIA")])
        del v["strumenti_ok"]
        assert be.decidi(v, SHA, SHA)[0] == "RIPROVA"

    def test_strumenti_non_ok_su_macchina_bot_non_diventa_operatore(self):
        v = _verdetto()
        v["strumenti_ok"] = False
        assert be.decidi(v, SHA, SHA, macchina_bot=True)[0] == "RIPROVA"

    def test_strumenti_non_ok_non_tocca_il_doc_only(self):
        assert be.decidi({"strumenti_ok": False}, SHA, SHA, doc_only=True)[0] == "APPROVE"

    def test_eventi_tutti_mappati_a_una_conclusione(self):
        assert be.CONCLUSIONE == {"APPROVE": "success", "COMMENT": "failure",
                                  "RIPROVA": "cancelled", "OPERATORE": "neutral"}
        assert set(be.ETICHETTE) == set(be.CONCLUSIONE)

    # V-2 seconda verifica #130 + R-161-1: la riga del verdetto è nel formato esatto.
    @pytest.mark.parametrize("riga", [
        "VERIFICA ESTERNA #1 — NON-APPROVATO",
        "VERIFICA ESTERNA #1 — NON È APPROVATO",
        "VERIFICA ESTERNA #1 — NON risulta APPROVATO",
        "VERIFICA ESTERNA #1 — NO APPROVATO",
        "VERIFICA ESTERNA #1 — NEGATO / APPROVATO",
        "VERIFICA ESTERNA #1 — non approvo: APPROVATO",
        "VERIFICA ESTERNA #1 — APPROVATO (ma io lo boccerei)",
        "VERIFICA ESTERNA — metodo seguito",
    ])
    def test_riga_verdetto_fuori_formato(self, riga):
        testo = f"{riga}\nFINDING: nessuno\nNON VERIFICATO: -"
        evento, motivo = be.decidi(_verdetto("APPROVATO", [], testo), SHA, SHA)
        assert evento == "COMMENT" and ("formato" in motivo or "coincide" in motivo), motivo

    @pytest.mark.parametrize("riga", [
        "VERIFICA ESTERNA #130 — APPROVATO", "VERIFICA ESTERNA PR #7 — APPROVATO",
        "VERIFICA ESTERNA 130 – APPROVATO.", "Verifica esterna: approvato",
        "## VERIFICA ESTERNA #1 — APPROVATO", "> **VERIFICA ESTERNA #1 - APPROVATO**",
    ])
    def test_riga_verdetto_nel_formato(self, riga):
        testo = f"{riga}\nFINDING: nessuno\nNON VERIFICATO: -"
        assert be.decidi(_verdetto("APPROVATO", [], testo), SHA, SHA)[0] == "APPROVE"

    @pytest.mark.parametrize("riga", [
        "V-1 (CRITICAL) — x", "F-1 HIGH — x", "V-1 — blocker", "V-1 — importante: x",
        "G-2 (medium) — x", "R-3 — severe", "V-1 (Bloccante) — x", "Nota: resta un HIGH",
    ])
    def test_gravita_fuori_vocabolario(self, riga):
        testo = f"VERIFICA ESTERNA #1 — APPROVATO CON RISERVE\nFINDING:\n{riga}\nNON VERIFICATO: -"
        v = _verdetto("APPROVATO CON RISERVE", [_f("V-1", "BASSA")], testo)
        assert be.decidi(v, SHA, SHA)[0] == "COMMENT"

    @pytest.mark.parametrize("car", ["\u200b", "\u200d", "\u2060", "\ufeff", "\u00ad",
                                     # R-569-2: invisibili che non sono Cf
                                     "\u3164", "\u115f", "\u2800", "\u034f", "\ufe0f"])
    def test_caratteri_invisibili(self, car):
        # V-2 seconda verifica #130: la gravità nascosta da un Cf torna visibile e blocca.
        testo = f"VERIFICA ESTERNA #1 — APPROVATO CON RISERVE\nFINDING:\nV-1 (ME{car}DIA) — x"
        v = _verdetto("APPROVATO CON RISERVE", [_f("V-1", "BASSA")], testo)
        evento, motivo = be.decidi(v, SHA, SHA)
        assert evento == "COMMENT" and "invisibili" in motivo

    # V-1 bot #305 e review #571: un invisibile tra due parole le incollava («BASSA» e
    # «MEDIA»), anche combinato con un secondo invisibile dentro la parola.
    _SEPARATORI = ["\u200b", "\u2800", "\u034f", "\ufe0f", "\u3164", "\U000e0080", "\ue000",
                   "\u2028", "\u2029", "\x0b", "\x0c", "\x1f", "\x85", "\x1b"]

    @pytest.mark.parametrize("sep", _SEPARATORI)
    @pytest.mark.parametrize("dentro", ["", "\u200b", "\u2800"])
    @pytest.mark.parametrize("modello", ["V-1 (BASSA{sep}ME{dentro}DIA) — x", "V-1 — AL{dentro}TA{sep}x — d",
                                         "V-1 — x{sep}gra{dentro}ve: y"])
    def test_invisibili_tra_e_dentro_le_parole(self, sep, dentro, modello):
        riga = modello.format(sep=sep, dentro=dentro)
        testo = f"VERIFICA ESTERNA #1 — APPROVATO CON RISERVE\nFINDING:\n{riga}\nNON VERIFICATO: -"
        evento, motivo = be.decidi(_verdetto("APPROVATO CON RISERVE", [_f("V-1", "BASSA")], testo),
                                   SHA, SHA)
        assert evento == "COMMENT", (riga, motivo)

    @pytest.mark.parametrize("car", ["\u200b", "\u2800", "\x0b"])
    def test_invisibile_che_toglie_un_confine(self, car):
        # V-2 bot #305: «V-1<U+200B>x (alta)» col solo testo ripulito diventava «V-1x (alta)».
        testo = (f"VERIFICA ESTERNA #1 — APPROVATO CON RISERVE\nFINDING:\nV-1{car}x (alta) — bug"
                 "\nNON VERIFICATO: -")
        evento, motivo = be.decidi(_verdetto("APPROVATO CON RISERVE", [_f("V-1", "BASSA")], testo),
                                   SHA, SHA)
        assert evento == "COMMENT" and "MEDIA" in motivo

    def test_credenziale_spezzata_in_un_finding(self):
        f = _f("V-1", "BASSA")
        f["descrizione"] = "x gh\x1bp_Zz9 y"
        assert be.contiene_segreti(_verdetto("APPROVATO CON RISERVE", [f]))

    @pytest.mark.parametrize("car", ["\u200b", "\u2060", "\x1b"])
    def test_credenziale_con_chiave_gemella(self, car):
        # Review #573: con le chiavi ripulite «tes<inv>to» copriva «testo» e la credenziale.
        testo = f"VERIFICA ESTERNA #1 — APPROVATO\nMetodo: gh{car}p_Zz9\nFINDING: nessuno"
        v = _verdetto("APPROVATO", [], testo)
        v[f"tes{car}to"] = "ok"
        assert be.contiene_segreti(v)
        assert be.decidi(v, SHA, SHA)[0] == "COMMENT"
        f = _f("V-1", "BASSA")
        f["descrizione"] = f"x gh{car}p_Zz9"
        f[f"descri{car}zione"] = "ok"
        assert be.contiene_segreti(_verdetto("APPROVATO CON RISERVE", [f]))

    def test_annidamento_profondo(self):
        # R-574-1: oltre il tetto di ricorsione di Python, niente crash: nel dubbio NO.
        v = _verdetto("APPROVATO", [])
        profondo: list = []
        for _ in range(1500):
            profondo = [profondo]
        v["extra"] = profondo
        assert be.contiene_segreti(v)
        assert be.decidi(v, SHA, SHA)[0] == "COMMENT"

    @pytest.mark.parametrize("sep", _SEPARATORI)
    def test_invisibile_che_crea_una_riserva_registrata(self, sep):
        # Bot #305 su d672021: tolto l'invisibile, «R-9-1<inv>V-1 (ALTA)» diventava la
        # citazione di una riserva già registrata e l'ALTA spariva.
        testo = (f"VERIFICA ESTERNA #1 — APPROVATO CON RISERVE\nFINDING:\nR-9-1{sep}V-1 (ALTA) — difetto"
                 "\nNON VERIFICATO: -")
        evento, motivo = be.decidi(_verdetto("APPROVATO CON RISERVE", [_f("V-1", "BASSA")], testo),
                                   SHA, SHA)
        assert evento == "COMMENT" and "ALTA" in motivo

    @pytest.mark.parametrize("segreto", ["gh<U+200B>p_Zz9abc", "sk-<U+2060>ant-oat01", "github<u+feff>_pat_11AA",
                                         "-----BEG<U+E0041>IN RSA"])
    def test_credenziale_spezzata_da_una_citazione(self, segreto):
        # V-1 ve #309: il PROMPT chiede di citare gli invisibili come <U+XXXX>; spezzata
        # così, una credenziale non deve finire nella review pubblica.
        testo = f"VERIFICA ESTERNA #1 — APPROVATO\nMetodo: {segreto}\nFINDING: nessuno"
        v = _verdetto("APPROVATO", [], testo)
        evento, motivo = be.decidi(v, SHA, SHA)
        assert evento == "COMMENT" and "credenziali" in motivo
        f = _f("V-1", "BASSA")
        f["descrizione"] = segreto
        assert be.contiene_segreti(_verdetto("APPROVATO CON RISERVE", [f]))

    def test_credenziale_spezzata_in_una_chiave(self):
        v = _verdetto("APPROVATO", [])
        v["gh\x1bp_Zz9"] = "x"
        assert be.contiene_segreti(v)

    def test_invisibile_lontano_dalle_gravita(self):
        # Un invisibile che non tocca nessuna gravità non cambia l'esito (caso #297).
        testo = ("VERIFICA ESTERNA #1 — APPROVATO CON RISERVE\nCLAIM: «/forte@GasBot\u200b» resta «uso»"
                 "\nFINDING:\nV-1 (BASSA) — x\nNON VERIFICATO: -")
        v = _verdetto("APPROVATO CON RISERVE", [_f("V-1", "BASSA")], testo)
        assert be.decidi(v, SHA, SHA)[0] == "APPROVE"

    @pytest.mark.parametrize("car", ["\U000e0080", "\ue000", "\u2029", "\x1b"])
    def test_altri_invisibili_mostrati(self, car):
        # V-2 bot #305: anche non assegnati, uso privato, separatori e controlli si vedono.
        testo = f"VERIFICA ESTERNA #1 — APPROVATO\nCLAIM: a{car}b\nFINDING: nessuno"
        v = _verdetto("APPROVATO", [], testo)
        evento, motivo = be.decidi(v, SHA, SHA)
        assert evento == "APPROVE", motivo
        assert f"a<U+{ord(car):04X}>b" in be.componi_corpo(evento, motivo, v, "m", "")

    def test_tetto_dopo_escape(self):
        # V-3 bot #305: con molti invisibili il recinto del codice resta chiuso.
        testo = "VERIFICA ESTERNA #1 — APPROVATO\nFINDING: nessuno\n" + "\u200b" * 20000
        v = _verdetto("APPROVATO", [], testo)
        corpo = be.componi_corpo("APPROVE", "m", v, "m", "")
        assert len(corpo) <= 65536 and corpo.endswith("```\n</details>")

    @pytest.mark.parametrize("car", [chr(c) for c in (*range(0x202A, 0x202F), *range(0x2066, 0x206A))])
    def test_controlli_bidi(self, car):
        # R-569-1: «(\u202eATLA\u202c)» si legge «(ALTA)» ma la regex vede «ATLA».
        # V-1 ve #305 (terza): ogni controllo da solo, senza un U+202C che lo copra.
        testo = (f"VERIFICA ESTERNA #1 — APPROVATO CON RISERVE\nFINDING:\n"
                 f"V-1 ({car}ATLA) — x")
        evento, motivo = be.decidi(_verdetto("APPROVATO CON RISERVE", [_f("V-1", "BASSA")], testo),
                                   SHA, SHA)
        assert evento == "COMMENT" and "bidi" in motivo

    @pytest.mark.parametrize("car", ["\u200b", "\u202e", "\u3164"])
    def test_invisibili_nel_titolo(self, car):
        # Un Cf nella riga del verdetto non la rende diversa da quella che si legge.
        titolo = f"VERIFICA ESTERNA #1 — NON{car}-APPROVATO\nFINDING: nessuno"
        assert be.decidi(_verdetto("APPROVATO", [], titolo), SHA, SHA)[0] == "COMMENT"
        titolo = f"VERIFICA ESTERNA #1 — BOCCI{car}ATO\nFINDING: nessuno"
        assert be.decidi(_verdetto("APPROVATO", [], titolo), SHA, SHA)[0] == "COMMENT"

    # R-576-1: niente separatori di riga qui (R-572-1 potrà leggerli come a capo).
    @pytest.mark.parametrize("car", ["\u200b", "\u3164", "\u2060", "\x1b"])
    def test_invisibile_nel_titolo_che_si_legge_uguale(self, car):
        # V-1 ve #305 (terza): il titolo si confronta col campo dopo aver tolto gli
        # invisibili, quindi «APPRO<inv>VATO» vale APPROVATO (come si legge).
        titolo = f"VERIFICA ESTERNA #1 — APPRO{car}VATO\nFINDING: nessuno"
        evento, motivo = be.decidi(_verdetto("APPROVATO", [], titolo), SHA, SHA)
        assert evento == "APPROVE", motivo

    def test_invisibili_come_nel_gate(self):
        # V-3 ve #305 (terza): la copia degli intervalli non deve divergere dal gate.
        from modules.gate import gate
        assert be._INVISIBILI_NON_CF == gate._INVISIBILI_NON_CF

    def test_invisibile_citato_dal_bot(self):
        # Bot #297 (0d45b8b): il bot citava un caso di prova con U+200B e il verdetto pulito
        # finiva in failure definitivo. Ora decide sul testo; nella review il Cf si vede.
        testo = ("VERIFICA ESTERNA #297 — APPROVATO\nCLAIM VERIFICATI:\n- «/forte@GasBot\u200b»"
                 " resta «uso»: VERO\nFINDING: nessuno\nNON VERIFICATO: -")
        v = _verdetto("APPROVATO", [], testo)
        evento, motivo = be.decidi(v, SHA, SHA)
        assert evento == "APPROVE", motivo
        corpo = be.componi_corpo(evento, motivo, v, "m", "")
        assert "«/forte@GasBot<U+200B>»" in corpo
        assert not any(unicodedata.category(c) == "Cf" for c in corpo)

    def test_invisibili_nelle_riserve_pubblicate(self):
        f = _f("V-1", "BASSA")
        f["descrizione"] = "a\u202eb\u3164c"
        # Il testo è pulito: la descrizione strutturata finisce solo tra le riserve pubblicate.
        testo = "VERIFICA ESTERNA #1 — APPROVATO CON RISERVE\nFINDING:\nV-1 (BASSA) — d"
        v = _verdetto("APPROVATO CON RISERVE", [f], testo)
        evento, motivo = be.decidi(v, SHA, SHA)
        corpo = be.componi_corpo(evento, motivo, v, "m", "")
        assert evento == "APPROVE" and "a<U+202E>b<U+3164>c" in corpo
        assert not any(unicodedata.category(c) == "Cf" for c in corpo)

    @pytest.mark.parametrize("segreto", ["gh\u200bp_Zz9", "sk-\u2060ant-oat01", "-----BEG\u00adIN RSA",
                                         # V-1 bot #305: i controlli, che json.dumps scrive come «\u001b»
                                         "gh\x1bp_Zz9", "-----BEG\x0bIN RSA", "github\x1f_pat_Zz9"])
    def test_credenziali_spezzate_da_invisibili(self, segreto):
        testo = f"VERIFICA ESTERNA #1 — APPROVATO\nMetodo: {segreto}\nFINDING: nessuno"
        v = _verdetto("APPROVATO", [], testo)
        evento, motivo = be.decidi(v, SHA, SHA)
        assert evento == "COMMENT" and "credenziali" in motivo
        assert "Zz9" not in be.componi_corpo(evento, motivo, v, "m", "")


# ---------------------------------------------------------------------------
# con_storico(): G-2 — un NO su uno SHA resta NO
# ---------------------------------------------------------------------------

class TestStorico:
    @pytest.mark.parametrize("precedenti", [["failure"], ["success", "failure"],
                                            ["failure", "success"], ["cancelled", "failure"]])
    def test_no_precedente_resta_no(self, precedenti):
        evento, motivo = be.con_storico("APPROVE", "ok", precedenti)
        assert evento == "COMMENT" and "già detto NO" in motivo

    @pytest.mark.parametrize("precedenti", [[], ["cancelled"], ["success"], ["neutral"]])
    def test_senza_no_precedente_resta_si(self, precedenti):
        assert be.con_storico("APPROVE", "ok", precedenti) == ("APPROVE", "ok")

    def test_storico_illeggibile_non_e_un_si(self):
        assert be.con_storico("APPROVE", "ok", None)[0] == "RIPROVA"

    # R-163-1: anche il sì sulla macchina del bot cede a un NO precedente sullo SHA.
    def test_operatore_dopo_un_no_resta_no(self):
        assert be.con_storico("OPERATORE", "m", ["failure"])[0] == "COMMENT"

    def test_operatore_storico_illeggibile(self):
        assert be.con_storico("OPERATORE", "m", None)[0] == "RIPROVA"

    def test_operatore_senza_no_resta_operatore(self):
        assert be.con_storico("OPERATORE", "m", ["neutral"]) == ("OPERATORE", "m")

    @pytest.mark.parametrize("evento", ["COMMENT", "RIPROVA"])
    def test_il_no_non_dipende_dallo_storico(self, evento):
        assert be.con_storico(evento, "m", ["success"]) == (evento, "m")

    def test_testo_incoerente_col_campo(self):
        v = _verdetto("APPROVATO", testo="VERIFICA ESTERNA #130 — BOCCIATO\nFINDING: nessuno")
        evento, motivo = be.decidi(v, SHA, SHA)
        assert evento == "COMMENT" and "non coincide" in motivo

    def test_testo_senza_riga_verdetto(self):
        v = _verdetto("APPROVATO", testo="tutto bene, approvo")
        assert be.decidi(v, SHA, SHA)[0] == "COMMENT"

    def test_con_riserve_non_e_approvato_pieno(self):
        # Il campo dice APPROVATO, il testo APPROVATO CON RISERVE: incoerenza → blocco.
        v = _verdetto("APPROVATO", testo="VERIFICA ESTERNA #130 — APPROVATO CON RISERVE\nFINDING: x")
        assert be.decidi(v, SHA, SHA)[0] == "COMMENT"

    @pytest.mark.parametrize("gravita", ["", "alta", "CRITICA", None])
    def test_gravita_non_valida(self, gravita):
        v = _verdetto("APPROVATO CON RISERVE", [{"id": "V-1", "gravita": gravita, "descrizione": "d"}])
        assert be.decidi(v, SHA, SHA)[0] == "COMMENT"

    def test_finding_non_dict(self):
        v = {"strumenti_ok": True, "verdetto": "APPROVATO CON RISERVE", "finding": ["V-1 MEDIA"],
             "testo": "VERIFICA ESTERNA #130 — APPROVATO CON RISERVE"}
        assert be.decidi(v, SHA, SHA)[0] == "COMMENT"

    @pytest.mark.parametrize("riga", [
        "V-1 (MEDIA) — x", "V-2 (MEDIA-BASSA) — x", "V-3 (BASSA/MEDIA) — x",
        "V-4 (ALTA) — x", "  - V-12 (alta) — x",
    ])
    def test_gravita_bloccante_solo_nel_testo(self, riga):
        # Il JSON dice "nessun finding" ma il testo ne riporta uno ALTA/MEDIA: vince il testo.
        testo = f"VERIFICA ESTERNA #130 — APPROVATO CON RISERVE\nFINDING:\n{riga}\nNON VERIFICATO: -"
        v = _verdetto("APPROVATO CON RISERVE", [], testo)
        assert be.decidi(v, SHA, SHA)[0] == "COMMENT"

    def test_gravita_bloccante_solo_nel_json(self):
        # Il testo non scrive la gravità tra parentesi, il JSON sì: vince il JSON.
        testo = "VERIFICA ESTERNA #130 — APPROVATO CON RISERVE\nFINDING:\nV-1 — x\nNON VERIFICATO: -"
        v = _verdetto("APPROVATO CON RISERVE", [_f("V-1", "MEDIA")], testo)
        assert be.decidi(v, SHA, SHA)[0] == "COMMENT"

    # R-158-2: sonde del revisore (#158) che prima davano APPROVE.
    def test_preambolo_non_vale_come_riga_verdetto(self):
        testo = ("Nota: la VERIFICA ESTERNA precedente era APPROVATO\n"
                 "VERIFICA ESTERNA #1 — BOCCIATO\nFINDING: nessuno")
        assert be.decidi(_verdetto("APPROVATO", [], testo), SHA, SHA)[0] == "COMMENT"

    def test_citazione_a_meta_riga_non_e_un_verdetto(self):
        # Una verifica passata citata a metà riga non deve bloccare un verdetto coerente.
        testo = ("VERIFICA ESTERNA #130 — APPROVATO\n"
                 "CLAIM VERIFICATI: la VERIFICA ESTERNA #127 era APPROVATO CON RISERVE — VERO\n"
                 "FINDING: nessuno\nNON VERIFICATO: -")
        assert be.decidi(_verdetto("APPROVATO", [], testo), SHA, SHA)[0] == "APPROVE"

    def test_righe_verdetto_discordi(self):
        testo = "VERIFICA ESTERNA #1 — APPROVATO\nFINDING: nessuno\nVERIFICA ESTERNA #1 — BOCCIATO"
        assert be.decidi(_verdetto("APPROVATO", [], testo), SHA, SHA)[0] == "COMMENT"

    def test_riga_verdetto_in_grassetto(self):
        testo = "**VERIFICA ESTERNA #1 — APPROVATO**\nFINDING: nessuno\nNON VERIFICATO: -"
        assert be.decidi(_verdetto("APPROVATO", [], testo), SHA, SHA)[0] == "APPROVE"

    @pytest.mark.parametrize("riga", [
        "V-1 — MEDIA — x",                 # senza parentesi
        "F-1 (MEDIA) — x",                 # prefisso diverso da V-
        "- R-3 (media) — x",
        "f-2 (alta) — x",                  # prefisso minuscolo
        "Nota: resta un problema MEDIA nel gate",  # parola maiuscola senza formato
    ])
    def test_gravita_senza_formato_canonico(self, riga):
        testo = f"VERIFICA ESTERNA #1 — APPROVATO CON RISERVE\nFINDING:\n{riga}\nNON VERIFICATO: -"
        v = _verdetto("APPROVATO CON RISERVE", [_f("V-1", "BASSA")], testo)
        assert be.decidi(v, SHA, SHA)[0] == "COMMENT"

    def test_media_nella_raccomandazione(self):
        testo = ("VERIFICA ESTERNA #1 — APPROVATO CON RISERVE\nFINDING:\nV-1 (BASSA) — x\n"
                 "NON VERIFICATO: -\nRACCOMANDAZIONE: chiudere V-2 (MEDIA)")
        v = _verdetto("APPROVATO CON RISERVE", [_f("V-1", "BASSA")], testo)
        assert be.decidi(v, SHA, SHA)[0] == "COMMENT"

    def test_con_riserve_senza_finding(self):
        v = _verdetto("APPROVATO CON RISERVE", [])
        evento, motivo = be.decidi(v, SHA, SHA)
        assert evento == "COMMENT" and "senza finding" in motivo

    def test_parola_media_minuscola_fuori_dai_finding_non_blocca(self):
        testo = ("VERIFICA ESTERNA #1 — APPROVATO CON RISERVE\nFINDING:\n"
                 "V-1 (BASSA) — x\nNON VERIFICATO: tempi in media 3 secondi")
        v = _verdetto("APPROVATO CON RISERVE", [_f("V-1", "BASSA")], testo)
        assert be.decidi(v, SHA, SHA)[0] == "APPROVE"

    @pytest.mark.parametrize("riga", [
        "V-1 — grave: un bypass totale del gate",       # V-4 verifica esterna #130
        "V-2 — media — x",
        "- V-3: criticità critica nel gate",
        "V-4 (BASSA) — in media 3 secondi",              # prudenza: su una riga V-N vince il blocco
    ])
    def test_gravita_a_parole_su_riga_di_finding(self, riga):
        testo = f"VERIFICA ESTERNA #1 — APPROVATO CON RISERVE\nFINDING:\n{riga}\nNON VERIFICATO: -"
        v = _verdetto("APPROVATO CON RISERVE", [_f("V-1", "BASSA")], testo)
        assert be.decidi(v, SHA, SHA)[0] == "COMMENT"

    @pytest.mark.parametrize("riga", [
        "VERIFICA ESTERNA #1 — NON APPROVATO",
        "VERIFICA ESTERNA #1 — DISAPPROVATO",
        "Verifica esterna #1: non  approvato",
        "VERIFICA ESTERNA #1 — NON BOCCIATO, APPROVATO",
        "VERIFICA ESTERNA #1 — APPROVATO (non bocciato)",
    ])
    def test_negazione_sulla_riga_del_verdetto(self, riga):
        # V-4 verifica esterna #130: col campo APPROVATO davano APPROVE.
        testo = f"{riga}\nFINDING: nessuno\nNON VERIFICATO: -"
        evento, motivo = be.decidi(_verdetto("APPROVATO", [], testo), SHA, SHA)
        assert evento == "COMMENT"

    # R-159-3: frasi innocue tra parentesi non sono gravità.
    @pytest.mark.parametrize("riga", [
        "CI-1 (test saltati su macOS) — VERO",
        "SHA-256 (in media 3 ms) — VERO",
        "PR-131 (parte multimediale) — VERO",
        "UTF-8 (caratteri ad alta codifica) — VERO",
    ])
    def test_parentesi_innocue_non_bloccano(self, riga):
        testo = f"VERIFICA ESTERNA #1 — APPROVATO\nFINDING: nessuno\n{riga}\nNON VERIFICATO: -"
        assert be.decidi(_verdetto("APPROVATO", [], testo), SHA, SHA)[0] == "APPROVE"

    @pytest.mark.parametrize("riga", ["v-1 (alta) — x", "V-2 ( Media ) — x"])
    def test_gravita_minuscola_tra_parentesi(self, riga):
        testo = f"VERIFICA ESTERNA #1 — APPROVATO CON RISERVE\nFINDING:\n{riga}\nNON VERIFICATO: -"
        v = _verdetto("APPROVATO CON RISERVE", [_f("V-1", "BASSA")], testo)
        assert be.decidi(v, SHA, SHA)[0] == "COMMENT"

    def test_riga_verdetto_minuscola(self):
        # R-159-4: "Verifica esterna: BOCCIATO" non deve essere ignorata.
        testo = "VERIFICA ESTERNA #1 — APPROVATO\nVerifica esterna #1: bocciato\nFINDING: nessuno"
        assert be.decidi(_verdetto("APPROVATO", [], testo), SHA, SHA)[0] == "COMMENT"

    def test_riga_verdetto_minuscola_concorde(self):
        testo = "Verifica esterna #1 — approvato\nFINDING: nessuno\nNON VERIFICATO: -"
        assert be.decidi(_verdetto("APPROVATO", [], testo), SHA, SHA)[0] == "APPROVE"

    @pytest.mark.parametrize("segreto", [
        "sk-ant-oat01-abcdef", "ghs_abc123", "ghp_Zz9", "github_pat_11AA", "-----BEGIN RSA PRIVATE KEY",
    ])
    def test_credenziali_nei_finding(self, segreto):
        # V-2 verifica esterna #130: id e descrizione dei finding finiscono nella review.
        for campo in ("id", "descrizione"):
            f = _f("V-1", "BASSA")
            f[campo] = f"x {segreto} y"
            v = _verdetto("APPROVATO CON RISERVE", [_f("V-2", "BASSA")])
            v["finding"].append(f)
            evento, motivo = be.decidi(v, SHA, SHA)
            assert evento == "COMMENT" and "credenziali" in motivo, campo
            # Anche chiamato con APPROVE, il corpo non pubblica nulla del verdetto.
            assert segreto not in be.componi_corpo("APPROVE", motivo, v, "m", ""), campo

    @pytest.mark.parametrize("segreto", [
        "sk-ant-oat01-abcdef", "ghs_abc123", "ghp_Zz9", "github_pat_11AA", "-----BEGIN RSA PRIVATE KEY",
    ])
    def test_credenziali_nel_testo(self, segreto):
        # R-159-2: repo e review pubblici; un testo con credenziali non si pubblica.
        testo = f"VERIFICA ESTERNA #1 — APPROVATO\nMetodo: {segreto}\nFINDING: nessuno"
        v = _verdetto("APPROVATO", [], testo)
        evento, motivo = be.decidi(v, SHA, SHA)
        assert evento == "COMMENT" and "credenziali" in motivo
        assert segreto not in be.componi_corpo(evento, motivo, v, "m", "")

    # R-158-1: la macchina del bot non si approva mai, nemmeno con verdetto pulito.
    def test_macchina_bot_mai_approvata(self):
        evento, motivo = be.decidi(_verdetto(), SHA, SHA, macchina_bot=True)
        assert evento == "OPERATORE" and "operatore" in motivo

    def test_macchina_bot_vince_su_doc_only(self):
        assert be.decidi(None, SHA, SHA, doc_only=True, macchina_bot=True)[0] == "OPERATORE"

    # R-163-1: prima il verdetto; solo un APPROVE della macchina del bot diventa OPERATORE.
    def test_bocciato_sulla_macchina_resta_no(self):
        assert be.decidi(_verdetto("BOCCIATO"), SHA, SHA, macchina_bot=True) == \
            ("COMMENT", "verdetto BOCCIATO")

    def test_media_sulla_macchina_resta_no(self):
        v = _verdetto("APPROVATO CON RISERVE", [_f("V-1", "MEDIA")])
        assert be.decidi(v, SHA, SHA, macchina_bot=True)[0] == "COMMENT"

    @pytest.mark.parametrize("verdetto", [None, "APPROVATO"])
    def test_verifica_non_eseguita_sulla_macchina_si_riprova(self, verdetto):
        assert be.decidi(verdetto, SHA, SHA, macchina_bot=True)[0] == "RIPROVA"

    def test_head_cambiata_sulla_macchina_si_riprova(self):
        assert be.decidi(_verdetto(), SHA, SHA2, macchina_bot=True)[0] == "RIPROVA"

    def test_riserve_minori_sulla_macchina_all_operatore(self):
        v = _verdetto("APPROVATO CON RISERVE", [_f("V-1", "BASSA")])
        evento, motivo = be.decidi(v, SHA, SHA, macchina_bot=True)
        assert evento == "OPERATORE" and "senza finding ALTA/MEDIA" in motivo

    # R-163-1: "non verificabile" non è mai neutral.
    @pytest.mark.parametrize("macchina", [True, False])
    def test_elenco_troncato_e_un_no(self, macchina):
        evento, motivo = be.decidi(_verdetto(), SHA, SHA, macchina_bot=macchina, elenco="troncato")
        assert evento == "COMMENT" and "troncato" in motivo

    @pytest.mark.parametrize("elenco", ["vuoto", "", "OK", "boh"])
    @pytest.mark.parametrize("macchina", [True, False])
    def test_elenco_non_leggibile_si_riprova(self, elenco, macchina):
        evento, motivo = be.decidi(_verdetto(), SHA, SHA, macchina_bot=macchina, elenco=elenco)
        assert evento == "RIPROVA" and "elenco" in motivo

    def test_elenco_illeggibile_vince_su_doc_only(self):
        assert be.decidi(None, SHA, SHA, doc_only=True, elenco="vuoto")[0] == "RIPROVA"

    def test_macchina_bot_ignota_si_riprova(self):
        evento, motivo = be.decidi(_verdetto(), SHA, SHA, macchina_bot=None)
        assert evento == "RIPROVA" and "macchina del bot" in motivo

    @pytest.mark.parametrize("analizzata,attuale", [("", SHA), (SHA, SHA2)])
    def test_head_prima_di_elenco(self, analizzata, attuale):
        # Senza head, o con la head cambiata (R-164-1), non c'è SHA su cui dire NO
        # definitivo: RIPROVA anche con elenco troncato.
        assert be.decidi(None, analizzata, attuale, elenco="troncato")[0] == "RIPROVA"

    # R-163-4: gravità fuori formato con prefisso fuori da V/F/R/G (solo _APRE_GRAVE la vede).
    @pytest.mark.parametrize("riga", ["C-1 (high) — x", "X-2 (grave) — x", "C-3 (severe) — x"])
    def test_gravita_aperta_in_parentesi_con_prefisso_qualsiasi(self, riga):
        testo = f"VERIFICA ESTERNA #1 — APPROVATO CON RISERVE\nFINDING:\n{riga}\nNON VERIFICATO: -"
        v = _verdetto("APPROVATO CON RISERVE", [_f("V-1", "BASSA")], testo)
        assert be.decidi(v, SHA, SHA)[0] == "COMMENT"

    def test_citazioni_passate_nei_claim_non_bloccano(self):
        testo = ("VERIFICA ESTERNA #130 — APPROVATO\n"
                 "CLAIM VERIFICATI: V-1 (MEDIA) della verifica #127 CHIUSA — VERO\n"
                 "FINDING: nessuno\nNON VERIFICATO: -\nRACCOMANDAZIONE: merge")
        assert be.decidi(_verdetto("APPROVATO", [], testo), SHA, SHA)[0] == "APPROVE"

    def test_senza_sezione_finding_si_analizza_tutto(self):
        testo = "VERIFICA ESTERNA #130 — APPROVATO\nV-1 (MEDIA) — qualcosa"
        assert be.decidi(_verdetto("APPROVATO", [], testo), SHA, SHA)[0] == "COMMENT"

    # R-161-1 (PR #149, due falsi NO reali): una riserva GIÀ registrata citata col suo id
    # R-<n>-<n> e la gravità tra parentesi non è un finding di questa PR.
    @pytest.mark.parametrize("riga", [
        "- Riserve già tracciate: R-203-1 (ALTA, preesistente, fuori da questa PR), R-204-1.",
        "RACCOMANDAZIONE: resta prioritaria R-200-2 (ALTA, preesistente): run_command fuori set.",
        "- R-202-1 (MEDIA, già in stato_progetto.md) e R-199-3 (BASSA).",
    ])
    def test_citazione_di_riserva_registrata_non_blocca(self, riga):
        testo = ("VERIFICA ESTERNA #149 — APPROVATO CON RISERVE\nFINDING:\n"
                 f"V-1 (BASSA) — x\n{riga}\nNON VERIFICATO: -\nRACCOMANDAZIONE: merge")
        v = _verdetto("APPROVATO CON RISERVE", [_f("V-1", "BASSA")], testo)
        assert be.decidi(v, SHA, SHA)[0] == "APPROVE"

    # Il resto della difesa resta intatto: si toglie SOLO "R-<n>-<n> (...)".
    @pytest.mark.parametrize("riga", [
        "V-1 (ALTA) — bug di questa PR",                      # finding del bot
        "R-203-1 (BASSA) ma questa PR introduce un bug ALTA",  # parola fuori dalla citazione
        "R-203-1 ALTA senza parentesi",                        # non è la forma della citazione
        "R-7 (ALTA) — x",                                      # non è un id di riserva R-n-n
        "R-203-1 (BASSA), V-2 (MEDIA) — x",                    # finding sulla stessa riga
        # #205 B-1: gravità minuscole/inglesi/a parole dopo la citazione restano viste.
        "R-203-1 (BASSA) questa PR introduce un bug grave",
        "R-203-1 (BASSA) ma x è high",
        "R-203-1 (BASSA) — critico",
        "R-203-1 (BASSA) e poi x (alta) in questa PR",
        # #205 B-2: parentesi annidate non nascondono un finding V- dentro la citazione.
        "R-203-1 (BASSA, vedi anche V-2 (ALTA) nuovo bug)",
    ])
    def test_gravita_della_pr_blocca_anche_accanto_a_una_riserva(self, riga):
        testo = ("VERIFICA ESTERNA #149 — APPROVATO CON RISERVE\nFINDING:\n"
                 f"{riga}\nNON VERIFICATO: -")
        v = _verdetto("APPROVATO CON RISERVE", [_f("V-9", "BASSA")], testo)
        assert be.decidi(v, SHA, SHA)[0] == "COMMENT"

    # B1: falsi rossi REALI di verifica-bot. Estratti testuali dei verdetti pubblicati
    # (FINDING e coda), con i finding strutturati tutti BASSA/COSMETICA.
    def test_b1_196_alta_nella_raccomandazione_non_blocca(self):
        # PR #196, head 1761eb5: check failure per «ALTA» nella prosa della RACCOMANDAZIONE.
        testo = (
            "VERIFICA ESTERNA #196 — APPROVATO CON RISERVE\nMetodo: lettura statica.\n"
            "CLAIM VERIFICATI:\n- «Motore non toccato»: VERO.\nFINDING:\n"
            "- V-1 (BASSA) — Alcune forme di cambio directory non vengono riconosciute.\n"
            "- V-2 (BASSA) — Claim strutturale sovrastimato.\n"
            "- V-3 (BASSA) — Un worktree creato nello stesso comando.\n"
            "- V-4 (BASSA) — Con `cwd` fuori da un repo git, ogni comando esce 2.\n"
            "Riserve già registrate richiamate, non nate da questa PR come finding V-: R-300-1 "
            "(dichiarata nella PR, cwd che non segue il cd della shell persistente), R-137-3 "
            "(GIT_INDEX_FILE, preesistente).\n\nNON VERIFICATO:\n- Esecuzione locale.\n\n"
            "RACCOMANDAZIONE: il merge è accettabile: il fix chiude il fail-open ALTA documentato "
            "senza indebolire il gate, e la CI reale è verde (138/138 sulla hook suite).")
        v = _verdetto("APPROVATO CON RISERVE", [_f(f"V-{i}", "BASSA") for i in range(1, 5)], testo)
        assert be.decidi(v, SHA, SHA)[0] == "APPROVE"

    @pytest.mark.parametrize("riga", [
        # PR #193, head 7e4609b: in coda alla sezione FINDING.
        "Problemi già registrati, che non nascono da questa PR: R-gate-worktree-1 (ALTA, "
        "preesistente). L'handoff riconosce che i commit del motore sono passati dal gate.",
        # PR #193, head bd3770f: nell'elenco delle riserve dichiarate.
        "Preesistenti, non nate dal codice di questa PR: R-gate-worktree-1 (ALTA, preesistente), "
        "R-291-1 (BASSA, preesistente).",
    ])
    def test_b1_193_riserva_con_id_alfabetico_non_blocca(self, riga):
        testo = ("VERIFICA ESTERNA #193 — APPROVATO CON RISERVE\nFINDING:\n"
                 "V-1 (BASSA) — Descrizione PR e handoff non aggiornati.\n"
                 "V-2 (COSMETICA) — gas.py:1880, commento.\n"
                 f"{riga}\nNON VERIFICATO:\n- niente\nRACCOMANDAZIONE: decide l'operatore.")
        v = _verdetto("APPROVATO CON RISERVE", [_f("V-1", "BASSA"), _f("V-2", "COSMETICA")], testo)
        assert be.decidi(v, SHA, SHA)[0] == "APPROVE"

    # B1, il verso del fail-safe NON si allenta: ogni forma da finding continua a bloccare.
    @pytest.mark.parametrize("testo", [
        # parola maiuscola nuda DENTRO FINDING: blocca come prima
        "FINDING:\nV-1 (BASSA) — x\nNota: resta un problema ALTA nel gate\nNON VERIFICATO: -",
        # id + gravità nella coda: blocca
        "FINDING:\nV-1 (BASSA) — x\nNON VERIFICATO: -\nRACCOMANDAZIONE: chiudere V-2 (ALTA)",
        # riga di finding a parole nella coda: blocca
        "FINDING:\nV-1 (BASSA) — x\nRACCOMANDAZIONE:\nV-3 — grave: bypass",
        # intestazione minuscola: non taglia, la parola nuda resta vista
        "FINDING:\nV-1 (BASSA) — x\nRaccomandazione: fail-open ALTA ancora aperto",
        # senza sezione FINDING: tutto il testo conta
        "V-1 (BASSA) — x\nRACCOMANDAZIONE: un bug ALTA",
        # id alfabetico ma gravità FUORI dalla parentesi della citazione
        "FINDING:\nR-gate-worktree-1 (BASSA) ma questa PR introduce un bug ALTA",
        # id senza cifra finale: non è una riserva registrata
        "FINDING:\nR-gate (ALTA) — x",
        # R-316-1: punto elenco che comincia con NON VERIFICATO dentro FINDING
        "FINDING:\n- NON VERIFICATO il test Y\n- Bypass del gate, gravità ALTA",
        # R-316-1: dopo la coda ricompare un FINDING
        "FINDING: vedi sotto\nRACCOMANDAZIONE: niente\nFINDING:\n- ALTA bypass",
        # R-316-2: id alfabetico, gravità a parole minuscole sulla stessa riga
        "FINDING:\nR-gate-worktree-1 (ALTA, preesistente) — questa PR lo rende grave",
        # R-316-3: finding V- travestito da riserva
        "FINDING:\nR-V-1 (ALTA) bypass",
    ])
    def test_b1_forme_da_finding_restano_bloccanti(self, testo):
        testo = "VERIFICA ESTERNA #1 — APPROVATO CON RISERVE\n" + testo
        v = _verdetto("APPROVATO CON RISERVE", [_f("V-1", "BASSA")], testo)
        assert be.decidi(v, SHA, SHA)[0] == "COMMENT"

    def test_b1_240_grave_negato_non_blocca(self):
        # PR #240, head 4891448: check failure per «non la considero più grave» nella
        # riga di un finding BASSA.
        testo = (
            "VERIFICA ESTERNA #240 — APPROVATO CON RISERVE\nFINDING:\n"
            "V-1 (BASSA) — Regressione di durabilità. I dati dell'altro processo non si "
            "perdono, per questo non la considero più grave. Fix: un file d'appoggio.\n"
            "V-2 (COSMETICA) — descrizione vecchia.\nNON VERIFICATO: -")
        v = _verdetto("APPROVATO CON RISERVE", [_f("V-1", "BASSA"), _f("V-2", "COSMETICA")], testo)
        assert be.decidi(v, SHA, SHA)[0] == "APPROVE"

    @pytest.mark.parametrize("riga", [
        "V-1 (BASSA) — non solo lento ma grave",          # «non» non nega «grave»… resta visto
        "V-1 (BASSA) — non è ALTA a parole ma critica",    # maiuscolo e altra gravità
        "V-1 (BASSA) — NON grave, anzi grave",             # negazione maiuscola: non vale
        "V-1 (BASSA) — non era grave, ora è grave",        # seconda occorrenza non negata
        # review #441: «non» nega il difetto, non la gravità → resta bloccante
        "V-1 — non mitigato: grave",
        "V-1 — il controllo non blocca: rischio grave",
        "V-1 — non autenticato: accesso critico",
        "V-1 — non risolto, grave",
        "V-1 — non escludo un rischio grave",
        "V-1 — non è stato chiuso: grave",
        "V-1 — non verificato grave",
        "V-1 — non ha test, importante",
        "V-1 — non è la più grave ma rompe il merge",       # R-442-1
    ])
    def test_b1_240_negazione_non_nasconde_gravita(self, riga):
        testo = ("VERIFICA ESTERNA #1 — APPROVATO CON RISERVE\nFINDING:\n"
                 f"{riga}\nNON VERIFICATO: -")
        v = _verdetto("APPROVATO CON RISERVE", [_f("V-1", "BASSA")], testo)
        assert be.decidi(v, SHA, SHA)[0] == "COMMENT"

    def test_riserva_registrata_nel_json_resta_bloccante(self):
        # Se il modello mette la riserva nel campo strutturato con gravità ALTA, il campo
        # vince: la nuova regola tocca solo il testo libero.
        testo = ("VERIFICA ESTERNA #149 — APPROVATO CON RISERVE\nFINDING:\n"
                 "R-203-1 (ALTA, preesistente)\nNON VERIFICATO: -")
        v = _verdetto("APPROVATO CON RISERVE", [_f("R-203-1", "ALTA")], testo)
        assert be.decidi(v, SHA, SHA)[0] == "COMMENT"


# ---------------------------------------------------------------------------
# solo_reports(): il dosaggio non deve diventare una scorciatoia
# ---------------------------------------------------------------------------

class TestSoloReports:
    @pytest.mark.parametrize("files", [
        ["reports/ultimo_report.md"],
        ["reports/handoff.md", "reports/diff_sessione.md", "reports/ultima_risposta.md"],
    ])
    def test_si(self, files):
        assert be.solo_reports(files)

    @pytest.mark.parametrize("files", [
        # G-4 verifica chat #130: lista BIANCA, criteri e stato passano dal bot.
        ["reports/stato_progetto.md"],
        ["reports/handoff.md", "reports/roadmap.md"],
        ["reports/raccomandazioni_aperte.md"],
        ["reports/handoff.md", "reports/ultimo_report.md", "reports/a.md"],
        ["reports/handoff.md.bak"], ["reports/x/handoff.md"], ["./reports/handoff.md"],
    ])
    def test_lista_bianca(self, files):
        assert not be.solo_reports(files)

    @pytest.mark.parametrize("files", [
        ["reports/sonda_locale_suite.txt"],             # V-5 #130: solo .md
        ["reports/a.md", "reports/e2e_output.json"],
        ["reports/a.md.sh"],
        ["reports/../gas.md"],
        ["reports/setup_verifica_bot.md"],              # V-6 #130 bis: istruzioni operative
        ["reports/a.md", "reports/design_cancello.md"],
    ])
    def test_solo_md(self, files):
        assert not be.solo_reports(files)

    @pytest.mark.parametrize("files", [
        [],                                              # elenco vuoto/illeggibile
        ["reports/a.md", "gas.py"],
        ["reportsX/a.md"],
        ["reports"],
        ["reports/../gas.py"],
        ["docs/reports/a.md"],
        [".github/workflows/ci.yml"],
        ["reports/a.md"] * be.MAX_FILE_API,              # elenco troncato dall'API
    ])
    def test_no(self, files):
        assert not be.solo_reports(files)


class TestMacchinaBot:
    @pytest.mark.parametrize("files", [
        [".github/workflows/verifica-bot.yml"],
        [".github/workflows/nuovo.yml", "reports/a.md"],
        ["gas.py", "scripts/bot_esito.py"],
        [".claude/verifica_esterna.md"],
        [".claude/settings.json"],
        [".claude/settings.local.json"],
        ["CLAUDE.md"],
        ["modules/CLAUDE.md"],                           # CLAUDE.md annidato (R-159-1)
        ["docs/CLAUDE.md"],
        ["CLAUDE.local.md"],
        [".claude/hooks/review_gate.sh"],                # hook = bash arbitrario (R-159-1)
        ["scripts/gasmerge.sh"],                         # macchina dei merge (V-5 #130)
        ["scripts/check_verdetto.py"],
        ["scripts/nuovo_script.sh"],
        [".claude/perimetro_review.txt"],
        [".claude/agents/revisore.md"],
        [".claude/commands/fine-task.md"],
        ["tests/test_unit_verifica_bot.py"],
        ["tests/test_unit_gasmerge.py"],
        ["tests/test_unit_gate.py"],
        ["tests/test_unit_hooks.py"],
        ["tests/test_unit_handoff_check.py"],
        [".mcp.json"],
        [".claude.json"],
        [".gitattributes"],                              # G-5 #130: -diff nasconde file
        ["modules/.gitattributes"],
        [],                                              # elenco illeggibile
        ["gas.py"] * be.MAX_FILE_API,                    # elenco troncato
    ])
    def test_si(self, files):
        assert be.tocca_macchina_bot(files)

    @pytest.mark.parametrize("files", [
        ["gas.py", "tests/test_unit_kernel.py"],
        ["gas.py", ".claude/agents/memoria_revisore.md"],
        ["reports/handoff.md"],
        ["docs/NOTCLAUDE.md", "CLAUDE.md.bak", "scriptsX/a.sh", ".githubx/a"],
        [".claude/agents/memoria_revisore.md", ".claude/commands/altro.md"],
        ["tests/test_unit_voice_tts.py", "modules/memory/db.py"],
        [".mcp.json.bak", ".claude/settings.jsonc", ".claude/verifica_esterna.md.old"],
        [".gitattributes.bak", "docs/gitattributes"],
    ])
    def test_no(self, files):
        assert not be.tocca_macchina_bot(files)


# ---------------------------------------------------------------------------
# Comandi con gh finto
# ---------------------------------------------------------------------------

def _gh_finto(tmp_path: Path, head: str, files_out: str = "", fail_head: bool = False,
              precedenti: list | None = None, fail_storico: bool = False) -> dict:
    """gh finto. files_out: righe "nome" o "nuovo<-vecchio" (rename); la risposta
    dell'API è un JSON vero e il filtro --jq dello script gira con jq reale.
    precedenti: check run già presenti sullo SHA, come (slug dell'App, conclusione)."""
    fake = tmp_path / "bin"
    fake.mkdir()
    log = tmp_path / "gh.log"
    voci = []
    for r in files_out.splitlines():
        nuovo, _, vecchio = r.partition("<-")
        voci.append({"filename": nuovo, **({"previous_filename": vecchio} if vecchio else {})})
    (tmp_path / "files.json").write_text(json.dumps(voci))
    (tmp_path / "checks.json").write_text(json.dumps({"check_runs": [
        {"app": {"slug": a}, "conclusion": c} for a, c in (precedenti or [])]}))
    gh = fake / "gh"
    gh.write_text(f"""#!/usr/bin/env bash
printf '%s\\n' "$*" >> {log}
case "$*" in
  *"/reviews"*) cat > {tmp_path}/review.json ;;
  *"/commits/"*"/check-runs"*) {"exit 1" if fail_storico else ""}
              for a in "$@"; do [ "$prev" = "--jq" ] && expr="$a"; prev="$a"; done
              jq -r "$expr" {tmp_path}/checks.json ;;
  *"/check-runs"*) cat > {tmp_path}/check.json ;;
  *"/files"*) for a in "$@"; do [ "$prev" = "--jq" ] && expr="$a"; prev="$a"; done
              jq -r "$expr" {tmp_path}/files.json ;;
  *) {"exit 1" if fail_head else f"echo {head}"} ;;
esac
""")
    gh.chmod(0o755)
    env = dict(os.environ, PATH=f"{fake}:{os.environ['PATH']}", REPO="o/r", PR="7",
               GITHUB_OUTPUT=str(tmp_path / "out"), MACCHINA_BOT="false", ELENCO_FILE="ok",
               APP_SLUG=SLUG)
    return env


SLUG = "gas-verificatore"


def _conclusione(tmp_path: Path) -> str:
    """Conclusione del check run pubblicato; la review è sempre un COMMENTO."""
    review = json.loads((tmp_path / "review.json").read_text())
    assert review["event"] == "COMMENT" and review["commit_id"] == SHA
    check = json.loads((tmp_path / "check.json").read_text())
    assert check["name"] == "verifica-bot" and check["head_sha"] == SHA
    assert check["status"] == "completed" and check["output"]["summary"] == review["body"]
    return check["conclusion"]


def _run(cmd, env):
    return subprocess.run([sys.executable, str(SCRIPT), cmd], env=env,
                          capture_output=True, text=True)


class TestComandi:
    def test_uso(self):
        r = subprocess.run([sys.executable, str(SCRIPT)], capture_output=True, text=True)
        assert r.returncode == 2

    def test_smista_doc_only(self, tmp_path):
        env = _gh_finto(tmp_path, SHA, "reports/handoff.md\nreports/ultimo_report.md\n")
        assert _run("smista", env).returncode == 0
        out = (tmp_path / "out").read_text()
        assert f"head={SHA}" in out and "solo_reports=true" in out and "macchina_bot=false" in out
        assert "elenco=ok" in out

    def test_smista_elenco_vuoto(self, tmp_path):
        env = _gh_finto(tmp_path, SHA, "")
        assert _run("smista", env).returncode == 0
        assert "elenco=vuoto" in (tmp_path / "out").read_text()

    def test_smista_elenco_troncato(self, tmp_path):
        env = _gh_finto(tmp_path, SHA, "gas.py\n" * be.MAX_FILE_API)
        assert _run("smista", env).returncode == 0
        assert "elenco=troncato" in (tmp_path / "out").read_text()

    def test_smista_rename_da_fuori(self, tmp_path):
        # Rename gas.py → reports/x.md: il vecchio nome conta.
        env = _gh_finto(tmp_path, SHA, "reports/x.md<-gas.py\n")
        _run("smista", env)
        assert "solo_reports=false" in (tmp_path / "out").read_text()

    def test_smista_rename_dalla_macchina_bot(self, tmp_path):
        env = _gh_finto(tmp_path, SHA, "scripts/altro.py<-scripts/bot_esito.py\n")
        _run("smista", env)
        assert "macchina_bot=true" in (tmp_path / "out").read_text()

    @pytest.mark.parametrize("valore,attesa", [
        (None, "cancelled"), ("", "cancelled"), ("False", "cancelled"), ("no", "cancelled"),
        ("true", "neutral"), ("false", "success")])
    def test_esito_macchina_bot_prudente(self, tmp_path, valore, attesa):
        # R-163-1: solo "true"/"false" esatti; variabile assente o strana = non verificabile.
        env = _gh_finto(tmp_path, SHA)
        env.update(HEAD_ANALIZZATA=SHA, VERDETTO_JSON=json.dumps(_verdetto()))
        if valore is None:
            env.pop("MACCHINA_BOT")
        else:
            env["MACCHINA_BOT"] = valore
        assert _run("esito", env).returncode == 0
        assert _conclusione(tmp_path) == attesa

    def test_esito_bocciato_sulla_macchina_e_failure(self, tmp_path):
        env = _gh_finto(tmp_path, SHA)
        env.update(HEAD_ANALIZZATA=SHA, VERDETTO_JSON=json.dumps(_verdetto("BOCCIATO")),
                   MACCHINA_BOT="true")
        assert _run("esito", env).returncode == 0
        assert _conclusione(tmp_path) == "failure"

    def test_esito_macchina_dopo_un_no_resta_failure(self, tmp_path):
        env = _gh_finto(tmp_path, SHA, precedenti=[(SLUG, "failure")])
        env.update(HEAD_ANALIZZATA=SHA, VERDETTO_JSON=json.dumps(_verdetto()), MACCHINA_BOT="true")
        assert _run("esito", env).returncode == 0
        assert _conclusione(tmp_path) == "failure"

    @pytest.mark.parametrize("elenco,attesa", [
        (None, "cancelled"), ("vuoto", "cancelled"), ("troncato", "failure")])
    def test_esito_elenco_non_verificabile(self, tmp_path, elenco, attesa):
        env = _gh_finto(tmp_path, SHA)
        env.update(HEAD_ANALIZZATA=SHA, VERDETTO_JSON=json.dumps(_verdetto()), MACCHINA_BOT="true")
        if elenco is None:
            env.pop("ELENCO_FILE")
        else:
            env["ELENCO_FILE"] = elenco
        assert _run("esito", env).returncode == 0
        assert _conclusione(tmp_path) == attesa

    def test_esito_approva_legato_allo_sha(self, tmp_path):
        env = _gh_finto(tmp_path, SHA)
        env.update(HEAD_ANALIZZATA=SHA, VERDETTO_JSON=json.dumps(_verdetto()),
                   MODELLO="claude-fable-5-1")
        assert _run("esito", env).returncode == 0
        assert _conclusione(tmp_path) == "success"
        body = json.loads((tmp_path / "review.json").read_text())["body"]
        assert "claude-fable-5-1" in body and "VERIFICA ESTERNA #130" in body
        # Il check si pubblica PRIMA della review (G-1: il gate c'è anche se la review fallisce).
        log = (tmp_path / "gh.log").read_text()
        assert log.index("/check-runs --input") < log.index("/reviews")

    def test_esito_media_non_approva(self, tmp_path):
        env = _gh_finto(tmp_path, SHA)
        v = _verdetto("APPROVATO CON RISERVE", [_f("V-1", "MEDIA")])
        env.update(HEAD_ANALIZZATA=SHA, VERDETTO_JSON=json.dumps(v))
        _run("esito", env)
        assert _conclusione(tmp_path) == "failure"

    def test_esito_json_rotto(self, tmp_path):
        env = _gh_finto(tmp_path, SHA)
        env.update(HEAD_ANALIZZATA=SHA, VERDETTO_JSON="{non json")
        _run("esito", env)
        assert _conclusione(tmp_path) == "cancelled"

    def test_esito_verifica_fallita_dichiara_cascata(self, tmp_path):
        env = _gh_finto(tmp_path, SHA)
        env.update(HEAD_ANALIZZATA=SHA, VERDETTO_JSON="",
                   MODELLI_FALLITI="claude-fable-5-1, claude-opus-5-5, claude-opus-4-8")
        _run("esito", env)
        assert _conclusione(tmp_path) == "cancelled"
        assert "claude-opus-4-8" in json.loads((tmp_path / "review.json").read_text())["body"]

    def test_esito_head_illeggibile(self, tmp_path):
        env = _gh_finto(tmp_path, SHA, fail_head=True)
        env.update(HEAD_ANALIZZATA=SHA, VERDETTO_JSON=json.dumps(_verdetto()))
        _run("esito", env)
        assert _conclusione(tmp_path) == "cancelled"

    def test_esito_doc_only(self, tmp_path):
        env = _gh_finto(tmp_path, SHA)
        env.update(HEAD_ANALIZZATA=SHA, SOLO_REPORTS="true")
        _run("esito", env)
        assert _conclusione(tmp_path) == "success"

    # G-2: un NO precedente della NOSTRA App sullo stesso SHA non si ritira con un rilancio.
    @pytest.mark.parametrize("doc_only", [False, True])
    def test_esito_no_precedente_resta_no(self, tmp_path, doc_only):
        env = _gh_finto(tmp_path, SHA, precedenti=[(SLUG, "failure")])
        env.update(HEAD_ANALIZZATA=SHA, VERDETTO_JSON=json.dumps(_verdetto()),
                   SOLO_REPORTS="true" if doc_only else "false")
        _run("esito", env)
        assert _conclusione(tmp_path) == "failure"
        log = (tmp_path / "gh.log").read_text()
        assert f"commits/{SHA}/check-runs?check_name=verifica-bot&filter=all" in log

    def test_esito_no_di_un_altra_app_non_conta(self, tmp_path):
        env = _gh_finto(tmp_path, SHA, precedenti=[("altra-app", "failure"), (SLUG, "cancelled")])
        env.update(HEAD_ANALIZZATA=SHA, VERDETTO_JSON=json.dumps(_verdetto()))
        _run("esito", env)
        assert _conclusione(tmp_path) == "success"

    def test_esito_storico_illeggibile(self, tmp_path):
        env = _gh_finto(tmp_path, SHA, fail_storico=True)
        env.update(HEAD_ANALIZZATA=SHA, VERDETTO_JSON=json.dumps(_verdetto()))
        _run("esito", env)
        assert _conclusione(tmp_path) == "cancelled"

    @pytest.mark.parametrize("slug", ["", "Gas Bot", 'x") | .conclusion = ("success', "a" * 101])
    def test_esito_slug_non_valido(self, tmp_path, slug):
        env = _gh_finto(tmp_path, SHA)
        env.update(HEAD_ANALIZZATA=SHA, VERDETTO_JSON=json.dumps(_verdetto()), APP_SLUG=slug)
        _run("esito", env)
        assert _conclusione(tmp_path) == "cancelled"

    def test_esito_senza_sha_non_pubblica(self, tmp_path):
        env = _gh_finto(tmp_path, SHA)
        env.update(HEAD_ANALIZZATA="", VERDETTO_JSON=json.dumps(_verdetto()))
        assert _run("esito", env).returncode == 1
        assert not (tmp_path / "check.json").exists()

    def test_corpo_troncato_sotto_il_limite(self):
        v = _verdetto(testo="VERIFICA ESTERNA #1 — APPROVATO\n" + "x" * 100000)
        assert len(be.componi_corpo("APPROVE", "m", v, "m", "")) < 65536

    def test_testo_lungo_resta_ben_chiuso(self):
        v = _verdetto(testo="VERIFICA ESTERNA #1 — APPROVATO\n" + "x" * 100000)
        assert be.componi_corpo("APPROVE", "m", v, "m", "").endswith("</details>")

    @pytest.mark.parametrize("finding", [5, True, "x", None, {"a": 1}])
    def test_corpo_con_finding_non_lista(self, finding):
        # V-4 verifica esterna #130 bis: prima TypeError → nessuna review pubblicata.
        v = {"strumenti_ok": True, "verdetto": "APPROVATO", "finding": finding, "testo": "VERIFICA ESTERNA #1 — APPROVATO"}
        evento, motivo = be.decidi(v, SHA, SHA)
        assert evento == "COMMENT"
        assert "VERIFICA ESTERNA #1" in be.componi_corpo("APPROVE", motivo, v, "m", "")

    def test_segreti_verdetto_non_serializzabile(self):
        assert be.contiene_segreti({"x": object()})

    def test_corpo_troncato_con_riserve_lunghe(self):
        lunghe = [{"id": f"V-{i}", "gravita": "BASSA", "descrizione": "y" * 5000} for i in range(30)]
        v = _verdetto("APPROVATO CON RISERVE", lunghe)
        assert len(be.componi_corpo("APPROVE", "m", v, "m", "")) < 65536


# ---------------------------------------------------------------------------
# Workflow: le proprietà di sicurezza dichiarate restano vere
# ---------------------------------------------------------------------------

@pytest.fixture(scope="module")
def wf():
    return yaml.safe_load(WORKFLOW.read_text())


def _on(wf):
    return wf.get("on", wf.get(True))  # PyYAML legge la chiave `on` come True


class TestWorkflow:
    def test_permessi_esatti_del_token_app(self, wf):
        # V-3 verifica esterna #130: nessun permesso sul contenuto. G-1: checks write per
        # pubblicare il check verifica-bot, pull-requests write per la review di commento.
        app = [s for s in wf["jobs"]["esito"]["steps"]
               if "create-github-app-token" in s.get("uses", "")][0]
        permessi = {k: v for k, v in app["with"].items() if k.startswith("permission-")}
        assert permessi == {"permission-pull-requests": "write", "permission-checks": "write"}

    def test_slug_dell_app_passato_a_esito(self, wf):
        # G-2: lo storico dei NO si legge solo sui check della NOSTRA App.
        passi = wf["jobs"]["esito"]["steps"]
        app = [s for s in passi if "create-github-app-token" in s.get("uses", "")][0]
        assert passi[-1]["env"]["APP_SLUG"] == "${{ steps.%s.outputs.app-slug }}" % app["id"]

    def test_prompt_fissa_il_formato_del_verdetto(self, wf):
        assert "ESATTAMENTE \"VERIFICA ESTERNA #" in wf["jobs"]["verifica"]["env"]["PROMPT"]

    def test_esito_dipende_dalla_verifica(self, wf):
        assert set(wf["jobs"]["esito"]["needs"]) == {"smista", "verifica"}
        assert wf["jobs"]["verifica"]["needs"] == "smista"

    def test_niente_git_fra_gli_strumenti(self, wf):
        # V-1 verifica esterna #130: `git log/show/diff --output=FILE` scrive file.
        strumenti = wf["jobs"]["verifica"]["env"]["STRUMENTI"]
        assert "Bash(git" not in strumenti and "git " not in strumenti

    def test_solo_comandi_gh_in_lettura(self, wf):
        strumenti = [t.strip() for t in wf["jobs"]["verifica"]["env"]["STRUMENTI"].split(",")]
        bash = sorted(t for t in strumenti if t.startswith("Bash("))
        assert bash == sorted(["Bash(gh pr view:*)", "Bash(gh pr diff:*)", "Bash(gh pr checks:*)",
                               "Bash(gh run view:*)", "Bash(gh run list:*)"])

    def test_concurrency_solo_sui_job_che_lavorano(self, wf):
        # R-158-3: a livello di workflow cancellerebbe verifiche buone su eventi irrilevanti.
        assert "concurrency" not in wf
        assert "concurrency" not in wf["jobs"]["smista"]
        for nome in ("verifica", "esito"):
            assert wf["jobs"][nome]["concurrency"]["cancel-in-progress"] is True

    def test_macchina_bot_passata_a_esito(self, wf):
        env = wf["jobs"]["esito"]["steps"][-1]["env"]
        assert env["MACCHINA_BOT"] == "${{ needs.smista.outputs.macchina_bot }}"
        # R-163-1: lo stato dell'elenco viaggia separato dalla macchina del bot.
        assert env["ELENCO_FILE"] == "${{ needs.smista.outputs.elenco }}"
        assert wf["jobs"]["smista"]["outputs"]["elenco"] == "${{ steps.smista.outputs.elenco }}"

    def test_trigger_solo_pull_request_target(self, wf):
        assert list(_on(wf)) == ["pull_request_target"]

    def test_permessi_globali_vuoti(self, wf):
        assert wf["permissions"] == {}

    def test_nessun_job_con_id_token(self, wf):
        for job in wf["jobs"].values():
            assert "id-token" not in (job.get("permissions") or {})

    def test_job_claude_sola_lettura(self, wf):
        perms = wf["jobs"]["verifica"]["permissions"]
        assert set(perms.values()) == {"read"}

    def test_scrive_solo_l_app(self, wf):
        for nome, job in wf["jobs"].items():
            assert "write" not in (job.get("permissions") or {}).values(), nome
        esito = wf["jobs"]["esito"]
        app = [s for s in esito["steps"] if "create-github-app-token" in s.get("uses", "")]
        assert len(app) == 1
        pubblica = esito["steps"][-1]
        assert pubblica["env"]["GH_TOKEN"] == "${{ steps.app.outputs.token }}"

    def test_segreti_solo_nell_environment(self, wf):
        testo = WORKFLOW.read_text()
        for nome, job in wf["jobs"].items():
            if "secrets." in yaml.safe_dump(job):
                assert job.get("environment") == "verifica-bot", nome
        assert "secrets.GITHUB_TOKEN" not in testo

    def test_filtro_fork_e_autore(self, wf):
        cond = wf["jobs"]["smista"]["if"]
        assert "head.repo.full_name == github.repository" in cond
        assert "user.login == github.repository_owner" in cond
        assert "'verifica'" in cond

    def test_azioni_pinnate_a_sha(self, wf):
        for job in wf["jobs"].values():
            for s in job["steps"]:
                if "uses" in s:
                    ref = s["uses"].split("@", 1)[1]
                    assert len(ref) == 40 and all(c in "0123456789abcdef" for c in ref), s["uses"]

    def test_checkout_senza_credenziali(self, wf):
        # NB (review #158): nella root claude-code-action riscrive poi .git/config col
        # github_token del job verifica, che è di sola lettura (test_job_claude_sola_lettura).
        for job in wf["jobs"].values():
            for s in job["steps"]:
                if s.get("uses", "").startswith("actions/checkout@"):
                    assert s["with"]["persist-credentials"] is False

    def test_codice_pr_mai_eseguito(self, wf):
        for job in wf["jobs"].values():
            for s in job["steps"]:
                run = s.get("run", "")
                assert "pr/" not in run and "./pr" not in run
                assert "scripts/" not in run or "python3 scripts/bot_esito.py" in run

    def test_nessun_testo_della_pr_interpolato(self, wf):
        # Titolo, corpo e nome del branch sono testo dell'autore: mai dentro ${{ }}.
        testo = WORKFLOW.read_text()
        for campo in ("pull_request.title", "pull_request.body", "head.ref", "head_ref",
                      "event.comment", "event.review"):
            assert campo not in testo, campo

    def test_nessun_file_del_repo_caricato_dal_bot(self, wf):
        # R-159-1: con le impostazioni di progetto il bot caricherebbe gli hook del repo
        # (bash col token nell'env) e i CLAUDE.md annidati della PR come istruzioni.
        args = [s["with"]["claude_args"] for s in wf["jobs"]["verifica"]["steps"]
                if "claude-code-action" in s.get("uses", "")]
        assert len(args) == 3
        assert all("--setting-sources user" in a for a in args)

    def test_lettura_limitata_alla_cartella(self, wf):
        # V-1 verifica esterna #130 bis: Grep/Glob nudi leggevano fuori cartella.
        strumenti = [t.strip() for t in wf["jobs"]["verifica"]["env"]["STRUMENTI"].split(",")]
        for t in ("Read", "Grep", "Glob"):
            assert f"{t}(./**)" in strumenti and t not in strumenti, t
        assert not [x for x in strumenti if not x.startswith(("Read(", "Grep(", "Glob(", "Bash("))]

    def test_ambiente_dei_sottoprocessi_ripulito(self, wf):
        assert wf["jobs"]["verifica"]["env"]["CLAUDE_CODE_SUBPROCESS_ENV_SCRUB"] == "1"

    def test_bubblewrap_installato_prima_di_claude(self, wf):
        """Prova reale PR #142: lo scrub (=1) esige bubblewrap. Lo step che lo installa deve
        venire PRIMA del primo modello e fermare il job se il sandbox non parte."""
        passi = wf["jobs"]["verifica"]["steps"]
        nomi = [p.get("name", "") for p in passi]
        i_bwrap = next(i for i, p in enumerate(passi) if "bubblewrap" in p.get("run", ""))
        i_claude = next(i for i, p in enumerate(passi)
                        if "claude-code-action" in p.get("uses", ""))
        assert i_bwrap < i_claude, nomi
        run = passi[i_bwrap]["run"]
        assert "apt-get install -y bubblewrap" in run and "exit 1" in run, run
        # R-192-2: la prova reale di bwrap deve esserci (non basta un exit 1 qualsiasi).
        assert "bwrap --unshare-all --ro-bind / / /bin/true" in run, run
        # Terza prova reale #142: senza socat la Bash del bot non parte → verdetto alla cieca.
        assert "apt-get install -y bubblewrap socat ripgrep" in run, run
        assert "for dip in socat rg; do" in run and 'command -v "$dip"' in run, run
        assert "continue-on-error" not in passi[i_bwrap], passi[i_bwrap]
        # R-192-1: senza sandbox nemmeno i modelli di riserva partono.
        assert passi[i_bwrap].get("id") == "sandbox"
        for p in passi:
            if p.get("id") in ("m2", "m3"):
                assert "steps.sandbox.outcome == 'success'" in p["if"], p["if"]

    def test_diagnosi_solo_result_e_dopo_i_modelli(self, wf):
        """Seconda prova reale #142: errore nascosto dall'action. La diagnosi stampa solo il
        campo result (troncato), viene dopo il raccogli e parte solo senza verdetto."""
        passi = wf["jobs"]["verifica"]["steps"]
        i_racc = next(i for i, p in enumerate(passi) if p.get("id") == "raccogli")
        i_diag = next(i for i, p in enumerate(passi) if "DIAGNOSI" in p.get("run", ""))
        assert i_diag > i_racc
        diag = passi[i_diag]
        assert diag["if"] == "${{ !cancelled() && steps.raccogli.outputs.modello == '' }}"
        assert ".result" in diag["run"] and ".[0:400]" in diag["run"], diag["run"]
        # R-194-1/2: una sola riga, e solo se is_error.
        assert "gsub(" in diag["run"] and ".is_error == true" in diag["run"], diag["run"]
        # Mai la trascrizione intera né i segreti nell'ambiente dello step.
        assert "cat " not in diag["run"] and "show_full_output" not in str(passi)
        assert not any("secrets." in str(v) for v in diag.get("env", {}).values())

    def test_condizioni_dei_job(self, wf):
        # V-3 verifica esterna #130 bis: un `if: always()` farebbe partire Claude e l'App
        # anche su PR escluse da smista (fork, autore estraneo, senza etichetta, draft).
        assert wf["jobs"]["verifica"]["if"] == ("needs.smista.outputs.solo_reports == 'false'"
                                                " && needs.smista.outputs.elenco == 'ok'")
        assert wf["jobs"]["esito"]["if"] == "${{ !cancelled() && needs.smista.result == 'success' }}"

    def test_sha_verificato_e_quello_di_smista(self, wf):
        # La review si lega allo SHA che il bot ha davvero letto (checkout di ./pr).
        checkout_pr = [s for s in wf["jobs"]["verifica"]["steps"] if s.get("with", {}).get("path") == "pr"]
        assert checkout_pr[0]["with"]["ref"] == "${{ needs.smista.outputs.head }}"
        env = wf["jobs"]["esito"]["steps"][-1]["env"]
        assert env["HEAD_ANALIZZATA"] == "${{ needs.smista.outputs.head }}"

    def test_cascata_modelli(self, wf):
        args = [s["with"]["claude_args"] for s in wf["jobs"]["verifica"]["steps"]
                if "claude-code-action" in s.get("uses", "")]
        modelli = [a.split("--model ", 1)[1].split()[0] for a in args]
        # Scelta dell'operatore 2026-10-11: Opus 5.5 per primo, Fable ultima riserva.
        assert modelli == ["claude-opus-5-5", "claude-opus-4-8", "claude-fable-5-1"]
        assert all("--json-schema" in a and "--allowedTools" in a for a in args)

    def test_strumenti_senza_scrittura(self, wf):
        strumenti = wf["jobs"]["verifica"]["env"]["STRUMENTI"]
        for vietato in ("Edit", "Write", "Bash(python", "Bash(bash", "Bash(sh",
                        "Bash(pytest", "Bash(git push", "Bash(gh pr review", "Bash(gh pr merge",
                        "Bash(*", "Bash(git -C pr checkout", "Bash(gh api", "Bash(curl",
                        "WebFetch", "WebSearch"):
            assert vietato not in strumenti, vietato

    def test_schema_coerente_con_lo_script(self, wf):
        schema = json.loads(wf["jobs"]["verifica"]["env"]["SCHEMA"])
        assert tuple(schema["properties"]["verdetto"]["enum"]) == be.VERDETTI
        gravita = schema["properties"]["finding"]["items"]["properties"]["gravita"]["enum"]
        assert tuple(gravita) == be.GRAVITA
        # R-196-1: il modello deve dichiarare se ha letto diff e CI (campo obbligatorio).
        assert schema["properties"]["strumenti_ok"] == {"type": "boolean"}
        assert "strumenti_ok" in schema["required"]
        prompt = wf["jobs"]["verifica"]["env"]["PROMPT"]
        assert '"strumenti_ok": true SOLO se' in prompt and "gh pr diff" in prompt
        # R-161-1: le riserve già registrate si citano come "R-203-1 (ALTA, preesistente)".
        assert '"R-203-1 (ALTA,' in prompt and "non blocca" in prompt
        # R-580-1: gli invisibili citati si scrivono come <U+XXXX>, mai col carattere vero.
        assert "SEMPRE come" in prompt and "<U+XXXX>" in prompt and "mai il carattere vero" in prompt
        assert "in qualunque campo" in prompt and "a capo e tab restano normali" in prompt  # V-1/V-2 bot #309
