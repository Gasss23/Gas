"""Scheda clienti da leggere anche SENZA connessione (decisione 22).

Un PDF protetto da password (AES-256) in iCloud Drive, nella stessa cartella delle copie
cifrate: sull'iPhone si apre con l'app File anche senza campo, e iCloud la aggiorna da
sola quando torna la rete. È SOLO DA LEGGERE: le modifiche fatte senza connessione
arriveranno col server di Gas (scelta dell'operatore del 25-11).

Si rifà SOLO quando i dati cambiano (impronta del contenuto), zero token: nessun modello
la scrive. Password: SOLO la sua, `GAS_CRM_SCHEDA_PASSWORD`, di almeno 16 caratteri e
DIVERSA da quella delle copie cifrate (R-864-1: un PDF si prova centinaia di volte più in
fretta di una copia .gascrm, quindi la stessa password esporrebbe le copie complete);
senza password non esce niente (mai in chiaro).
Tutto FAIL-SAFE §9: un errore dà un motivo e un avviso nel registro, mai un crash.
"""
from __future__ import annotations

import hashlib
import hmac
import io
import logging
import os
import re
import sys
import textwrap
import threading
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from modules.crm import analisi, copia_cifrata
from modules.crm.store import CRMStore, formatta_euro

log = logging.getLogger(__name__)

NOME_FILE = "Scheda clienti.pdf"
IMPRONTA_FILE = ".gas_memory_crm_scheda.impronta"  # accanto al DB, mai su iCloud
MOVIMENTI_PER_CLIENTE = 3
LARGHEZZA = 95            # caratteri per riga (Helvetica 9 su A4 con margini di 40 pt)
PASSWORD_MIN = 16         # più lunga delle copie: il PDF si prova in fretta (R-864-1)
RIGHE_PER_PAGINA = 62
_lock = threading.Lock()  # guardiano e riga di comando non scrivono insieme

# caratteri fuori da WinAnsi (la codifica dei font di base del PDF) resi in modo leggibile
_SOSTITUZIONI = {"−": "-", " ": " ", " ": " ", " ": " ", "→": "->"}


_RADICE = Path(__file__).resolve().parents[2]  # la cartella di Gas, dove sta il .env


def _leggi_env_file() -> Optional[Dict[str, str]]:
    """R-865-1: i valori ATTUALI del .env di Gas, riletti ogni volta. Il CRM sotto launchd
    legge il .env solo all'avvio: senza questo, una password cambiata dopo continuerebbe a
    valere la vecchia. Stesse regole del kernel (`gas._carica_dotenv`: `export`, commenti,
    virgolette, vince la prima riga). None se il .env non c'è, non si legge, o è spento
    (`GAS_NO_DOTENV`, come nei test). Mai solleva, mai valori nel registro."""
    try:
        import gas
        if gas._env_flag("GAS_NO_DOTENV"):
            return None
        testo = (_RADICE / ".env").read_text(encoding="utf-8-sig")
    except FileNotFoundError:
        return None
    except Exception as e:
        log.warning("CRM scheda: .env non riletto (%s)", type(e).__name__)
        return None
    valori: Dict[str, str] = {}
    for riga in testo.splitlines():
        riga = riga.strip()
        if not riga or riga.startswith("#"):
            continue
        if riga.startswith("export "):
            riga = riga[len("export "):].lstrip()
        chiave, sep, valore = riga.partition("=")
        chiave = chiave.strip()
        if not sep or not gas._DOTENV_CHIAVE.fullmatch(chiave) or chiave in valori:
            continue
        valore = valore.strip()
        tra = gas._DOTENV_VIRGOLETTE.fullmatch(valore)
        if tra:
            valore = tra.group(2)
        elif valore[:1] in ("'", '"'):
            continue
        else:
            valore = re.split(r"\s+#", valore, maxsplit=1)[0].rstrip()
        valori[chiave] = valore
    return valori


def _valore(chiave: str) -> str:
    """Il valore di adesso: dal .env se c'è (anche se cambiato dopo l'avvio); se una chiave
    era venuta dal .env ed è stata tolta, vale «tolta»; altrimenti l'ambiente."""
    valori = _leggi_env_file()
    if valori is not None:
        if chiave in valori:
            return valori[chiave]
        if chiave in getattr(sys.modules.get("gas"), "_DOTENV_CARICATE", set()):
            return ""
    return os.environ.get(chiave, "")


def _propria() -> str:
    return copia_cifrata._normalizza(_valore("GAS_CRM_SCHEDA_PASSWORD"))


def password() -> Optional[str]:
    """La password della scheda: solo la sua, abbastanza lunga e diversa da quella delle
    copie cifrate (R-864-1). None se manca o non va bene."""
    propria = _propria()
    if len(propria) < PASSWORD_MIN:
        return None
    copie = copia_cifrata._normalizza(_valore("GAS_CRM_BACKUP_PASSWORD"))
    if copie and hmac.compare_digest(propria.encode("utf-8"), copie.encode("utf-8")):
        return None
    return propria


def motivo_spenta() -> Optional[str]:
    """None se la scheda si può scrivere, altrimenti il motivo (per l'operatore)."""
    propria = _propria()
    if not propria:
        return (f"manca GAS_CRM_SCHEDA_PASSWORD (almeno {PASSWORD_MIN} caratteri, DIVERSA da "
                "quella delle copie cifrate): senza password la scheda non esce dal Mac")
    if len(propria) < PASSWORD_MIN:
        return f"GAS_CRM_SCHEDA_PASSWORD è più corta di {PASSWORD_MIN} caratteri: nessuna scheda"
    if password() is None:
        return ("GAS_CRM_SCHEDA_PASSWORD è uguale a GAS_CRM_BACKUP_PASSWORD: usane una diversa "
                "(la scheda si prova molto più in fretta delle copie cifrate)")
    if copia_cifrata.cartella() is None:
        return "nessuna cartella esterna: iCloud Drive non trovato e GAS_CRM_BACKUP_CIFRATO_DIR non impostata"
    try:
        import pypdf  # noqa: F401
        import cryptography  # noqa: F401
    except ImportError:
        return "mancano le librerie «pypdf»/«cryptography»: pip install -r requirements.txt"
    return None


# ------------------------------------------------------------------ contenuto
def _data_it(giorno: str) -> str:
    """«2026-11-25» → «25/11/2026» (resta com'è se non è una data)."""
    p = str(giorno)[:10].split("-")
    return f"{p[2]}/{p[1]}/{p[0]}" if len(p) == 3 and all(x.isdigit() for x in p) else str(giorno)


def righe_scheda(st: CRMStore) -> Optional[List[Tuple[str, str]]]:
    """Le righe della scheda, senza l'ora di aggiornamento: (stile, testo) con stile «t»
    titolo, «c» cliente, «n» normale. None se il DB non risponde."""
    foto = st.fotografia()
    if foto is None:
        return None
    try:
        promemoria = st.promemoria(solo_in_attesa=True)
    except Exception as e:  # §9: senza promemoria la scheda resta utile
        log.warning("CRM scheda: promemoria non letti: %s", e)
        promemoria = []
    d = analisi.costruisci(foto, oggi=st.oggi())
    limite = d.oggi.isoformat()
    mov_per_pos: Dict[int, List[Dict[str, Any]]] = {}
    for m in foto["movimenti"]:
        # come i saldi (analisi.costruisci): niente stornati né movimenti datati dopo oggi
        if m.get("storno_di") is not None or m.get("stornato") or str(m["data"]) > limite:
            continue
        mov_per_pos.setdefault(int(m["posizione_id"]), []).append(m)
    prom_per_cliente: Dict[Optional[int], List[Dict[str, Any]]] = {}
    for p in sorted(promemoria, key=lambda x: str(x.get("quando") or "")):
        cid = p.get("cliente_id")
        prom_per_cliente.setdefault(int(cid) if cid is not None else None, []).append(p)

    out: List[Tuple[str, str]] = [("t", "Gas CRM - scheda clienti (solo da leggere)")]
    clienti = sorted(d.clienti.values(), key=lambda c: (str(c.get("nome") or "").casefold(), int(c["id"])))
    out.append(("n", f"Clienti: {len(clienti)}. Per i dati aggiornati al minuto apri la dashboard."))
    out.append(("n", ""))
    for c in clienti:
        cid = int(c["id"])
        out.append(("c", f"{c.get('nome') or '(senza nome)'}  [{c.get('stato') or ''}]"))
        contatti = " · ".join(x for x in (c.get("telefono"), c.get("email")) if x)
        if contatti:
            out.append(("n", f"Contatti: {contatti}"))
        metr = analisi.metriche_cliente(d, cid)
        posz = sorted(d.per_cliente.get(cid, []), key=lambda p: p.id)
        for pos in posz:
            servizio = d.servizi.get(pos.servizio_id, {}).get("nome") or f"servizio {pos.servizio_id}"
            out.append(("n", f"Servizio: {servizio} ({pos.stato}, aperto il {_data_it(pos.aperta_il)}) - "
                             f"capitale {formatta_euro(pos.capitale_cents)}"))
        if posz:
            out.append(("n", f"Capitale totale: {formatta_euro(metr.capitale_cents)} · profitto di "
                             f"{analisi.etichetta_mese(d.mese)}: "
                             f"{formatta_euro(metr.profitto_mese_cents, segno=True)}"))
        movimenti = sorted((m for pos in posz for m in mov_per_pos.get(pos.id, [])),
                           key=lambda m: (str(m["data"]), int(m["id"])), reverse=True)
        if movimenti:
            ultimi = "; ".join(f"{_data_it(m['data'])} {m['tipo']} {formatta_euro(int(m['importo_cents']))}"
                               for m in movimenti[:MOVIMENTI_PER_CLIENTE])
            out.append(("n", f"Ultimi movimenti: {ultimi}"))
        for p in prom_per_cliente.get(cid, []):
            out.append(("n", f"Promemoria: {_data_it(str(p['quando']))} {str(p['quando'])[11:16]} - {p['testo']}"))
        out.append(("n", ""))
    senza = prom_per_cliente.get(None, [])
    if senza:
        out.append(("c", "Promemoria senza cliente"))
        for p in senza:
            out.append(("n", f"{_data_it(str(p['quando']))} {str(p['quando'])[11:16]} - {p['testo']}"))
    return out


# ------------------------------------------------------------------ PDF
def _testo_pdf(s: str) -> bytes:
    for k, v in _SOSTITUZIONI.items():
        s = s.replace(k, v)
    s = "".join(ch if ch >= " " else " " for ch in s)  # niente caratteri di controllo
    b = s.encode("cp1252", errors="replace")
    return b.replace(b"\\", b"\\\\").replace(b"(", b"\\(").replace(b")", b"\\)")


def pdf_in_chiaro(righe: List[Tuple[str, str]], intestazione: str) -> bytes:
    """Un PDF semplice (A4, Helvetica) con le righe date, a capo automatico."""
    linee: List[Tuple[str, str]] = [("n", intestazione), ("n", "")]
    for stile, testo in righe:
        pezzi = textwrap.wrap(testo, LARGHEZZA, break_long_words=True, break_on_hyphens=False) or [""]
        linee.extend((stile, p) for p in pezzi)
    pagine = [linee[i:i + RIGHE_PER_PAGINA] for i in range(0, len(linee), RIGHE_PER_PAGINA)] or [[]]
    oggetti: List[bytes] = []

    def aggiungi(corpo: bytes) -> int:
        oggetti.append(corpo)
        return len(oggetti)

    catalogo = aggiungi(b"")  # riempito dopo
    radice_pagine = aggiungi(b"")
    f1 = aggiungi(b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica /Encoding /WinAnsiEncoding >>")
    f2 = aggiungi(b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold /Encoding /WinAnsiEncoding >>")
    figli: List[int] = []
    for n, pagina in enumerate(pagine, 1):
        flusso = io.BytesIO()
        flusso.write(b"BT\n")
        y = 800
        for stile, testo in pagina:
            font, dim = (b"/F2", 13) if stile == "t" else ((b"/F2", 10) if stile == "c" else (b"/F1", 9))
            flusso.write(b"%s %d Tf 1 0 0 1 40 %d Tm (%s) Tj\n" % (font, dim, y, _testo_pdf(testo)))
            y -= 12
        flusso.write(b"/F1 8 Tf 1 0 0 1 40 30 Tm (%s) Tj\nET\n" % _testo_pdf(f"pagina {n} di {len(pagine)}"))
        dati = flusso.getvalue()
        contenuto = aggiungi(b"<< /Length %d >>\nstream\n%s\nendstream" % (len(dati), dati))
        figli.append(aggiungi(
            b"<< /Type /Page /Parent %d 0 R /MediaBox [0 0 595 842] /Contents %d 0 R "
            b"/Resources << /Font << /F1 %d 0 R /F2 %d 0 R >> >> >>" % (radice_pagine, contenuto, f1, f2)))
    oggetti[catalogo - 1] = b"<< /Type /Catalog /Pages %d 0 R >>" % radice_pagine
    oggetti[radice_pagine - 1] = b"<< /Type /Pages /Kids [%s] /Count %d >>" % (
        b" ".join(b"%d 0 R" % k for k in figli), len(figli))
    out = io.BytesIO()
    out.write(b"%PDF-1.7\n%\xe2\xe3\xcf\xd3\n")
    posizioni: List[int] = []
    for i, corpo in enumerate(oggetti, 1):
        posizioni.append(out.tell())
        out.write(b"%d 0 obj\n%s\nendobj\n" % (i, corpo))
    xref = out.tell()
    out.write(b"xref\n0 %d\n0000000000 65535 f \n" % (len(oggetti) + 1))
    for p in posizioni:
        out.write(b"%010d 00000 n \n" % p)
    out.write(b"trailer\n<< /Size %d /Root %d 0 R >>\nstartxref\n%d\n%%%%EOF\n" % (
        len(oggetti) + 1, catalogo, xref))
    return out.getvalue()


def cifra(pdf: bytes, pw: str) -> bytes:
    """Lo stesso PDF protetto da password (AES-256): senza password non si legge nulla."""
    from pypdf import PdfReader, PdfWriter
    writer = PdfWriter(clone_from=PdfReader(io.BytesIO(pdf)))
    writer.encrypt(user_password=pw, owner_password=None, algorithm="AES-256")
    out = io.BytesIO()
    writer.write(out)
    return out.getvalue()


# ------------------------------------------------------------------ scrittura
def _impronta(righe: List[Tuple[str, str]], pw: str) -> str:
    """Cambia se cambiano i dati o la password (chiave HMAC): così si riscrive solo allora.
    Il file dell'impronta sta accanto al DB, sul Mac, dove c'è già il file delle chiavi."""
    testo = "\n".join(f"{s}\t{t}" for s, t in righe).encode("utf-8")
    return hmac.new(pw.encode("utf-8"), testo, hashlib.sha256).hexdigest()


def _togli_scheda_vecchia() -> None:
    """R-865-2: se la password della scheda è diventata uguale a quella delle copie, la
    scheda già su iCloud si aprirebbe con la password delle copie: si toglie. Mai solleva."""
    dest_dir = copia_cifrata.cartella()
    if dest_dir is None:
        return
    try:
        (dest_dir / NOME_FILE).unlink(missing_ok=True)
        log.warning("CRM: scheda clienti tolta (password uguale a quella delle copie cifrate)")
    except OSError as e:
        log.warning("CRM: scheda clienti da togliere a mano (%s)", type(e).__name__)


def _pulisci_tmp_vecchi(dest_dir: Path) -> None:
    """R-864-6: toglie i temporanei della scheda lasciati da un'interruzione (Mac spento a
    metà) da più di un'ora: cifrati, ma si accumulerebbero su iCloud. Mai solleva."""
    limite = time.time() - copia_cifrata.TMP_VECCHIO_S
    try:
        resti = list(dest_dir.glob(f".{NOME_FILE}.*.tmp"))
    except OSError:
        return
    for resto in resti:
        try:
            if resto.stat().st_mtime < limite:
                resto.unlink(missing_ok=True)
        except OSError:
            pass


def aggiorna(st: CRMStore, forza: bool = False) -> Tuple[str, Optional[Path]]:
    """Riscrive la scheda se i dati sono cambiati (o se manca, o con `forza`).
    Ritorna (esito, percorso): esito «aggiornata», «invariata», «spenta: …» o
    «non riuscita: …». Mai solleva (§9)."""
    with _lock:
        motivo = motivo_spenta()
        if motivo:
            if "uguale a GAS_CRM_BACKUP_PASSWORD" in motivo:
                _togli_scheda_vecchia()
            return f"spenta: {motivo}", None
        dest_dir = copia_cifrata.cartella()
        pw = password()
        if dest_dir is None or pw is None:
            return "spenta: password o cartella non disponibili", None
        tmp: Optional[Path] = None
        try:
            _pulisci_tmp_vecchi(dest_dir)
            assente = copia_cifrata._genitore_assente(dest_dir)
            if assente:
                return f"non riuscita: {assente}", None
            righe = righe_scheda(st)
            if righe is None:
                return "non riuscita: il database del CRM non risponde", None
            impronta = _impronta(righe, pw)
            file_impronta = st.db_path.parent / IMPRONTA_FILE
            dest = dest_dir / NOME_FILE
            try:
                vecchia = file_impronta.read_text(encoding="utf-8").strip()
            except OSError:
                vecchia = ""
            if not forza and vecchia == impronta and dest.exists():
                return "invariata", dest
            ora = st.adesso_minuto()
            intestazione = f"Aggiornata il {_data_it(ora[:10])} alle {ora[11:16]} (dal CRM sul Mac)."
            dati = cifra(pdf_in_chiaro(righe, intestazione), pw)
            dest_dir.mkdir(exist_ok=True)
            tmp = dest_dir / f".{NOME_FILE}.{os.getpid()}-{threading.get_ident()}.tmp"
            copia_cifrata._scrivi_privato(tmp, dati, esclusivo=True)
            os.replace(tmp, dest)
            tmp = None
            copia_cifrata._scrivi_privato(file_impronta, impronta.encode("utf-8"))
            return "aggiornata", dest
        except Exception as e:  # §9: il CRM continua; nel log solo il tipo, mai dati
            log.warning("CRM: scheda clienti non scritta: %s", type(e).__name__)
            consiglio = copia_cifrata._consiglio_icloud(dest_dir, e)
            return f"non riuscita: {consiglio or type(e).__name__}", None
        finally:
            if tmp is not None:
                try:
                    tmp.unlink(missing_ok=True)
                except OSError:
                    pass
