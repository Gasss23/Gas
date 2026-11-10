"""V-1 bot #228: tools/ingest_knowledge.py accetta solo fonti di tipo file dentro
knowledge/ (l'unica cartella protetta dalla firma, roadmap 5.3)."""
import importlib.util
import sys
from pathlib import Path

import pytest

_ROOT = Path(__file__).resolve().parent.parent


@pytest.fixture
def ingest(tmp_path, monkeypatch):
    spec = importlib.util.spec_from_file_location(
        "ingest_knowledge_test", _ROOT / "tools" / "ingest_knowledge.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    root = tmp_path / "repo"
    (root / "knowledge").mkdir(parents=True)
    (root / "dati").mkdir()
    (root / "knowledge" / "ok.txt").write_text("testo approvato " * 20, encoding="utf-8")
    (root / "dati" / "fuori.txt").write_text("testo fuori " * 20, encoding="utf-8")
    (root / "knowledge" / "link.txt").symlink_to(root / "dati" / "fuori.txt")
    monkeypatch.setattr(mod, "REPO_ROOT", root)
    conn = mod.open_db(tmp_path / "k.db")
    yield mod, conn
    conn.close()


@pytest.mark.parametrize("uri", ["dati/fuori.txt", "knowledge/../dati/fuori.txt",
                                 "knowledge/link.txt", "/etc/hostname"])
def test_fonte_fuori_da_knowledge_rifiutata(ingest, uri):
    mod, conn = ingest
    esito = mod.ingest_file_source(conn, {"nome": "x", "uri": uri})
    assert esito["error"] == "uri fuori da knowledge/" and esito["ingested"] == 0


def test_fonte_dentro_knowledge_accettata(ingest):
    mod, conn = ingest
    esito = mod.ingest_file_source(conn, {"nome": "ok", "uri": "knowledge/ok.txt"})
    assert "error" not in esito and esito["ingested"] >= 1


def _attivi(conn, nome):
    return [(r["chunk_ref"], r["testo"]) for r in conn.execute(
        "SELECT chunk_ref, testo FROM knowledge WHERE source_name = ? AND stato = 'active' "
        "ORDER BY chunk_ref", (nome,))]


def test_fonte_accorciata_supera_i_chunk_vecchi(ingest, tmp_path):
    """Audit 2026-11-10 B1: una fonte che si accorcia non lascia attivi i pezzi tolti
    (Gas li pescherebbe ancora); restano nel DB come superseded, mai cancellati."""
    mod, conn = ingest
    f = mod.REPO_ROOT / "knowledge" / "corta.txt"
    f.write_text("\n\n".join(f"paragrafo VECCHIO_{i}" for i in range(5)), encoding="utf-8")
    src = {"nome": "corta", "uri": "knowledge/corta.txt", "chunk_chars": 20}
    assert mod.ingest_file_source(conn, src)["ingested"] == 5
    f.write_text("nuovo unico", encoding="utf-8")
    esito = mod.ingest_file_source(conn, src)
    assert _attivi(conn, "corta") == [("chunk_0000", "nuovo unico")]
    assert esito["superseded"] == 5
    totale = conn.execute("SELECT COUNT(*) FROM knowledge WHERE source_name='corta'").fetchone()[0]
    assert totale == 6  # niente cancellato
    # chunk_max più piccolo: anche i pezzi troncati escono dagli attivi
    f.write_text("\n\n".join(f"p{i}" * 8 for i in range(4)), encoding="utf-8")
    mod.ingest_file_source(conn, dict(src, chunk_max=2))
    assert [r for r, _ in _attivi(conn, "corta")] == ["chunk_0000", "chunk_0001"]


def test_chunk_text_spezza_i_paragrafi_lunghi(ingest):
    """Audit 2026-11-10 B2: un capoverso senza righe vuote più lungo del tetto non
    diventa un chunk unico di qualunque lunghezza."""
    mod, _ = ingest
    assert [len(c) for c in mod.chunk_text("x" * 5000, 1800)] == [1800, 1800, 1400]
    parole = " ".join(f"parola{i}" for i in range(600))
    pezzi = mod.chunk_text(parole + "\n\ncorto", 500)
    assert all(len(p) <= 500 for p in pezzi)
    assert " ".join(" ".join(pezzi).split()) == parole + " corto"  # niente perso
    assert all(not p.startswith(" ") and not p.endswith(" ") for p in pezzi)
    assert mod.chunk_text("uno\n\ndue", 1800) == ["uno\n\ndue"]  # invariato sotto il tetto


def test_fonte_rotta_non_ferma_le_altre(ingest):
    """Audit 2026-11-10 B3: file non UTF-8, uri che è una cartella, voce senza uri:
    la fonte si salta con un log e le successive vengono ingerite."""
    mod, conn = ingest
    k = mod.REPO_ROOT / "knowledge"
    (k / "bin.txt").write_bytes(b"\xff\xfe testo rotto \xe8")
    (k / "cartella").mkdir()
    fonti = [{"nome": "bin", "uri": "knowledge/bin.txt"},
             {"nome": "dir", "uri": "knowledge/cartella"},
             {"nome": "nouri"},
             {"nome": "num", "uri": "knowledge/ok.txt", "chunk_max": "tanti"},
             {"nome": "ok", "uri": "knowledge/ok.txt"}]
    totale = mod.ingest_fonti(conn, fonti)
    assert totale["errori"] == 4 and totale["ingested"] >= 1
    assert _attivi(conn, "ok") and not _attivi(conn, "bin") and not _attivi(conn, "num")


@pytest.mark.parametrize("contenuto", ["", "sources:\n", "- a\n- b\n", "sources: 3\n",
                                       "sources:\n  - 7\n  - nome: x\n"])
def test_sources_yaml_vuoto_o_storto(ingest, tmp_path, contenuto):
    """Audit 2026-11-10 B3: sources.yaml vuoto o di forma sbagliata → nessuna fonte,
    mai AttributeError."""
    mod, _ = ingest
    y = tmp_path / "sources.yaml"
    y.write_text(contenuto, encoding="utf-8")
    fonti = mod.carica_fonti(y)
    assert fonti == ([{"nome": "x"}] if "nome: x" in contenuto else [])


@pytest.mark.parametrize("fonti_yaml,codice", [
    ("sources:\n  - nome: ok\n    uri: knowledge/ok.txt\n", None),
    ("sources:\n  - nome: ok\n    uri: knowledge/ok.txt\n  - nome: rotta\n    uri: knowledge/manca/\n", 1),
])
def test_main_exit_code_se_una_fonte_fallisce(ingest, tmp_path, monkeypatch, fonti_yaml, codice):
    """V-3 bot #366: le fonti buone si caricano comunque, ma se una fallisce il comando
    esce con 1 (chi lo lancia da script lo vede); tutto ok → nessun exit."""
    mod, _ = ingest
    (mod.REPO_ROOT / "knowledge" / "manca").mkdir()
    y = mod.REPO_ROOT / "knowledge" / "sources.yaml"
    y.write_text(fonti_yaml, encoding="utf-8")
    monkeypatch.setattr(mod, "SOURCES_YAML", y)
    monkeypatch.setattr(sys, "argv", ["ingest", "--db", str(tmp_path / "m.db")])
    if codice is None:
        mod.main()
    else:
        with pytest.raises(SystemExit) as e:
            mod.main()
        assert e.value.code == codice
