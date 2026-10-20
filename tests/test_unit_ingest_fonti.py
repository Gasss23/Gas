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
