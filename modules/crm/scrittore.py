"""Testi per i clienti riscritti da Claude Opus — mai da un modello gratuito.

Decisione dell'operatore (2026-11-17, `reports/crm/decisioni.md` punto 9): «massima
riservatezza; i dati dei clienti non devono mai finire ai modelli gratuiti; per questa task
solo modelli almeno Opus». Quindi:

- Si usa SOLO il cervello forte (`claude -p` con l'abbonamento, `brains/claude_cli.py`)
  col modello `GAS_CRM_MODELLO` (default Opus). Nessun ripiego su altri provider: se Claude
  non c'è, la proposta resta col testo standard, scritto a regole fisse (nessun modello).
  L'interruttore è lo stesso del kernel: `GAS_CLAUDE_CLI` acceso.
- Minimizzazione dei dati: a Claude vanno solo il nome di battesimo, i nomi dei servizi,
  il risultato del mese se positivo, da quanti mesi è cliente, tipo e livello della proposta
  e la bozza. Mai telefono, email, cognome, note, importi del capitale.
- Il filtro delle parole vietate (promesse, urgenza, perdite) è una rete che si può
  aggirare: la tutela vera è l'approvazione dell'operatore su ogni messaggio.
- Tetto giornaliero di riscritture (`GAS_CRM_OPUS_GIORNO`, default 60): conta i TENTATIVI
  (anche falliti o scartati), segnati sul diario del CRM, che non si può riscrivere, prima
  della chiamata e nella stessa transazione del controllo (R-808-2).
- Stesso conto di spesa del cervello forte del kernel (`.gas_claude_cli_uso.json` e tetto
  `GAS_CLAUDE_CLI_TETTO_USD`): tetto raggiunto o conto illeggibile → niente riscrittura;
  il costo equivalente di ogni chiamata, riuscita o no, entra nel conto (R-808-2).
- Il testo ricevuto si ripulisce e si controlla: niente promesse di guadagno, niente urgenza
  finta, niente perdite; lunghezza massima. Nota sul rischio e riga STOP le rimette sempre
  il sistema (`completa_testo`). La proposta resta «da approvare»: decide l'operatore.
"""
from __future__ import annotations

import logging
import os
import re
import unicodedata
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple

from brains.model_ids import MODEL_CLAUDE_OPUS, e_modello_opus  # fonte unica degli ID (V-4 ve #381)
from modules.crm import analisi
from modules.crm.messaggi import NOTA_RISCHIO_DEFAULT, RIGA_STOP, nome_breve, nota_rischio
from modules.crm.store import CRMStore, ErroreCRM, formatta_euro_tondo

log = logging.getLogger(__name__)

MODELLO_DEFAULT = MODEL_CLAUDE_OPUS
TESTO_MAX_OPUS = 900
OPUS_GIORNO_DEFAULT = 60
NOTA_EVENTO = "testo riscritto da Claude Opus"
TIPO_TENTATIVO = "opus"            # evento del diario: un tentativo di riscrittura
NOTA_TENTATIVO = "tentativo di riscrittura con Claude Opus"
# cartella del conto del cervello forte: la stessa del kernel avviato dal repo
ROOT = Path(__file__).resolve().parents[2]

# (modello, messaggi) → (testo, costo equivalente in USD). Sostituibile nei test.
# Un'eccezione può portare il costo già consumato in `costo_equivalente_usd`.
Chiedi = Callable[[str, List[Dict[str, str]]], Tuple[str, float]]

# un consumo di questo processo che non si è potuto registrare: niente altre riscritture
_senza_conto = False

_VIETATE = ("garantit", "garantisc", "garanzi", "assicurat", "sicuro al 100", "senza rischi",
            "senza rischio", "zero rischi", "rischio zero", "capitale protetto",
            "rendimento sicuro", "guadagno sicuro", "profitto sicuro", "investimento sicuro",
            "rendimento certo", "guadagno certo", "profitto certo", "soldi facili",
            "guadagni facili", "ultimi posti", "solo oggi", "solo per oggi", "affrettati",
            "investi ora", "investi subito", "perdit", "drawdown")

SISTEMA = """Sei il copywriter di un'attività italiana che offre servizi di trading ai propri clienti.
Riscrivi la bozza di un messaggio WhatsApp per UN cliente: deve essere caldo, personale,
naturale, convincente e breve (al massimo 600 caratteri), in italiano, dando del tu.
Regole che non si violano mai:
- non promettere guadagni futuri, non dire che un servizio è sicuro o senza rischi;
- puoi citare solo il risultato GIÀ ottenuto dal cliente che ti viene dato, se c'è;
- non parlare mai di perdite o drawdown;
- niente urgenza finta («ultimi posti», «solo oggi»);
- chiudi con una domanda semplice che inviti a rispondere;
- non aggiungere firme, la riga per dire STOP né avvertenze: le aggiunge il sistema.
Rispondi SOLO con il testo del messaggio, senza virgolette e senza spiegazioni."""


def modello() -> str:
    v = os.environ.get("GAS_CRM_MODELLO", "").strip()
    return v or MODELLO_DEFAULT


def _tetto_giorno() -> int:
    grezzo = os.environ.get("GAS_CRM_OPUS_GIORNO", "").strip()
    if not grezzo:
        return OPUS_GIORNO_DEFAULT
    try:
        return max(0, int(grezzo))
    except ValueError:
        log.warning("CRM: GAS_CRM_OPUS_GIORNO=%r non è un intero: riscritture spente", grezzo[:20])
        return 0


def disponibile() -> Optional[str]:
    """None se Claude si può usare; altrimenti il motivo (per l'operatore)."""
    if os.environ.get("GAS_CLAUDE_CLI", "").strip().lower() not in ("1", "true", "on", "yes", "si"):
        return "cervello forte spento (GAS_CLAUDE_CLI): resta il testo standard"
    if not e_modello_opus(modello()):
        return f"il modello configurato ({modello()}) non è Opus: riscrittura negata"
    return None


def _chiedi_claude(model: str, messaggi: List[Dict[str, str]]) -> Tuple[str, float]:
    from brains.claude_cli import ClaudeCliClient
    r = ClaudeCliClient(timeout=180).chat.completions.create(model=model, messages=messaggi)
    usage = getattr(r, "usage", None)
    costo = getattr(usage, "costo_equivalente_usd", 0.0) if usage is not None else 0.0
    return str(r.choices[0].message.content or ""), float(costo or 0.0)


def _senza_coda(testo: str) -> str:
    """La bozza senza nota sul rischio e riga STOP (le rimette il sistema)."""
    t = testo.replace(RIGA_STOP, "")
    for nota in {nota_rischio(), NOTA_RISCHIO_DEFAULT}:
        if nota:
            t = t.replace(nota, "")
    return t.strip()


def pulisci(testo: str) -> str:
    """Testo di Claude → testo per il cliente. Solleva ErroreCRM se non è accettabile."""
    t = (testo or "").strip().strip("`").strip()
    if len(t) >= 2 and t[0] in "\"«“" and t[-1] in "\"»”":
        t = t[1:-1].strip()
    t = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]", "", t)
    t = _senza_coda(t)
    if not t:
        raise ErroreCRM("Claude ha risposto un testo vuoto")
    if len(t) > TESTO_MAX_OPUS:
        raise ErroreCRM("il testo di Claude è troppo lungo: resta quello di prima")
    for v in _VIETATE:
        if _contiene_vietata(t, v):
            raise ErroreCRM(f"testo scartato: contiene «{v}» (promesse, urgenza o perdite non ammesse)")
    return t


def _forme_confronto(testo: str) -> Tuple[str, str]:
    """Due forme del testo per il filtro delle parole vietate (V-1 verifica esterna #381,
    3° giro): (1) NFKC, senza caratteri invisibili di formato (spazi a larghezza zero…),
    senza accenti, minuscolo, spazi compressi; (2) la stessa con sole lettere e cifre, così
    anche «g a r a n t i t o» o «garan-tito» vengono visti. È una RETE, non la tutela:
    la tutela è l'approvazione dell'operatore su ogni messaggio. Un falso allarme scarta
    solo la riscrittura (resta il testo di prima). PURA."""
    t = unicodedata.normalize("NFKC", testo or "")
    t = "".join(ch for ch in t if unicodedata.category(ch) != "Cf")
    t = "".join(ch for ch in unicodedata.normalize("NFKD", t) if not unicodedata.combining(ch))
    t = " ".join(t.casefold().split())
    return t, re.sub(r"[^a-z0-9]", "", t)


def _contiene_vietata(testo: str, vietata: str) -> bool:
    spazi, lettere = _forme_confronto(testo)
    return vietata in spazi or re.sub(r"[^a-z0-9]", "", vietata) in lettere


def contesto(store: CRMStore, proposta: Dict[str, Any]) -> Dict[str, Any]:
    """I SOLI dati che vanno a Claude (minimizzazione)."""
    foto = store.fotografia()
    if foto is None:
        raise ErroreCRM("database non disponibile")
    d = analisi.costruisci(foto, store.oggi())
    cid = int(proposta["cliente_id"])
    cliente = d.clienti.get(cid)
    if cliente is None:
        raise ErroreCRM("cliente inesistente")
    m = analisi.metriche_cliente(d, cid)
    attivi = [str(d.servizi[s]["nome"]) for s in m.servizi_attivi if s in d.servizi]
    risultato = None
    if m.profitto_mese_prec_cents > 0:
        risultato = f"+{formatta_euro_tondo(m.profitto_mese_prec_cents)} il mese scorso"
    elif m.profitto_mese_cents > 0:
        risultato = f"+{formatta_euro_tondo(m.profitto_mese_cents)} questo mese"
    aperture = [p.aperta_il for p in m.posizioni if p.aperta_il]
    mesi = None
    if aperture:
        primo = min(aperture)
        mesi = max(0, (store.oggi().year - int(primo[:4])) * 12 + store.oggi().month - int(primo[5:7]))
    proposto = None
    if proposta.get("servizio_id"):
        s = d.servizi.get(int(proposta["servizio_id"]))
        if s is not None:
            proposto = {"nome": s["nome"], "descrizione": s.get("descrizione") or ""}
    return {
        "nome": nome_breve(str(cliente.get("nome") or "")),
        "mesi_da_cliente": mesi,
        "servizi_attuali": attivi,
        "risultato_recente": risultato,
        "tipo_proposta": {"cross_sell": "consigliare un nuovo servizio",
                          "aumento_capitale": "proporre di aumentare il capitale nel servizio attuale",
                          "referral": "chiedere di presentare un amico"}.get(str(proposta["tipo"]),
                                                                           str(proposta["tipo"])),
        "servizio_proposto": proposto,
        "insistenza": f"{proposta['livello']} su 3 (1 = gentile, 3 = più diretto, mai insistente)",
    }


def riscrivi(store: CRMStore, proposta_id: int, chiedi: Optional[Chiedi] = None,
             root: Optional[Path] = None) -> Dict[str, Any]:
    """Fa riscrivere a Claude Opus il testo di una proposta da approvare e lo salva.
    Ritorna la proposta aggiornata. Solleva ErroreCRM con un motivo leggibile. `root` è
    la cartella del conto del cervello forte (default: il repo, come il kernel)."""
    global _senza_conto
    motivo = disponibile() if chiedi is None else None
    if motivo:
        raise ErroreCRM(motivo)
    p = store.proposta(proposta_id)
    if p is None:
        raise ErroreCRM("proposta inesistente")
    if p["stato"] != "da_approvare":
        raise ErroreCRM("si può riscrivere solo una proposta ancora da approvare")
    from gas import registra_uso_claude_cli, tetto_claude_cli_superato  # lo stesso conto del kernel
    radice = ROOT if root is None else Path(root)
    if _senza_conto:
        raise ErroreCRM("un consumo del cervello forte non si è potuto registrare: "
                        "riscritture ferme fino al riavvio del CRM")
    fermo = tetto_claude_cli_superato(radice)
    if fermo is not None:
        usato, limite = fermo
        raise ErroreCRM("conto del cervello forte illeggibile: riscrittura negata" if usato is None
                        else f"tetto giornaliero del cervello forte raggiunto "
                             f"({usato:.2f}/{limite:.2f} USD equivalenti)")
    dati = contesto(store, p)
    tetto = _tetto_giorno()
    # il tentativo si segna PRIMA della chiamata, nella transazione del controllo: conta
    # anche se poi Claude fallisce o il testo viene scartato
    store.segna_evento_entro_tetto(TIPO_TENTATIVO, f"{NOTA_TENTATIVO} (proposta #{int(proposta_id)})",
                                   tetto, cliente_id=int(p["cliente_id"]),
                                   motivo=f"tetto di oggi raggiunto ({tetto} riscritture con Opus)")
    messaggi = [
        {"role": "system", "content": SISTEMA},
        {"role": "user", "content": (
            "Dati del cliente (solo questi):\n"
            + "\n".join(f"- {k}: {v}" for k, v in dati.items() if v not in (None, [], ""))
            + "\n\nBozza da riscrivere:\n" + _senza_coda(str(p["messaggio"])))},
    ]
    costo: Any = 0.0
    try:
        grezzo, costo = (chiedi or _chiedi_claude)(modello(), messaggi)
    except ErroreCRM:
        raise
    except Exception as e:  # §9: il motivo nel log, mai il testo di Claude né i dati
        costo = getattr(e, "costo_equivalente_usd", 0.0)
        log.warning("CRM: riscrittura con Claude non riuscita: %s", type(e).__name__)
        raise ErroreCRM("Claude non ha risposto: resta il testo di prima") from None
    finally:
        if not registra_uso_claude_cli(radice, costo):
            _senza_conto = True
    testo = pulisci(grezzo)
    return store.aggiorna_messaggio(proposta_id, testo, autore="motore", nota=NOTA_EVENTO)
