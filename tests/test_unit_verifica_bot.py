"""Test per scripts/bot_esito.py e .github/workflows/verifica-bot.yml (V-B vera).

Zero rete, zero token: la logica di decisione è pura; i comandi smista/esito girano con
un `gh` finto preposto al PATH; il workflow è controllato staticamente (YAML).
"""
import json
import os
import subprocess
import sys
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
    return {"verdetto": esito, "finding": finding, "testo": testo}


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

    def test_head_cambiata(self):
        evento, motivo = be.decidi(_verdetto(), SHA, SHA2)
        assert evento == "COMMENT" and "head cambiata" in motivo

    @pytest.mark.parametrize("analizzata,attuale", [("", SHA), (SHA, ""), ("", "")])
    def test_head_vuota(self, analizzata, attuale):
        assert be.decidi(_verdetto(), analizzata, attuale)[0] == "COMMENT"

    def test_head_cambiata_blocca_anche_doc_only(self):
        assert be.decidi(None, SHA, SHA2, doc_only=True)[0] == "COMMENT"

    def test_doc_only_senza_verdetto(self):
        assert be.decidi(None, SHA, SHA, doc_only=True)[0] == "APPROVE"

    @pytest.mark.parametrize("verdetto", [
        None, "APPROVATO", [], {},
        {"verdetto": "APPROVATO", "finding": []},                       # testo mancante
        {"verdetto": "APPROVATO", "finding": [], "testo": "   "},        # testo vuoto
        {"verdetto": "APPROVATO", "testo": "VERIFICA ESTERNA — APPROVATO"},  # finding mancante
        {"verdetto": "OK", "finding": [], "testo": "VERIFICA ESTERNA — OK"},
    ])
    def test_verdetto_illeggibile(self, verdetto):
        assert be.decidi(verdetto, SHA, SHA)[0] == "COMMENT"

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
        v = {"verdetto": "APPROVATO CON RISERVE", "finding": ["V-1 MEDIA"],
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

    def test_parola_media_minuscola_non_blocca(self):
        testo = ("VERIFICA ESTERNA #1 — APPROVATO CON RISERVE\nFINDING:\n"
                 "V-1 (BASSA) — in media 3 secondi\nNON VERIFICATO: -")
        v = _verdetto("APPROVATO CON RISERVE", [_f("V-1", "BASSA")], testo)
        assert be.decidi(v, SHA, SHA)[0] == "APPROVE"

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
        assert evento == "COMMENT" and "operatore" in motivo

    def test_macchina_bot_vince_su_doc_only(self):
        assert be.decidi(None, SHA, SHA, doc_only=True, macchina_bot=True)[0] == "COMMENT"

    def test_citazioni_passate_nei_claim_non_bloccano(self):
        testo = ("VERIFICA ESTERNA #130 — APPROVATO\n"
                 "CLAIM VERIFICATI: V-1 (MEDIA) della verifica #127 CHIUSA — VERO\n"
                 "FINDING: nessuno\nNON VERIFICATO: -\nRACCOMANDAZIONE: merge")
        assert be.decidi(_verdetto("APPROVATO", [], testo), SHA, SHA)[0] == "APPROVE"

    def test_senza_sezione_finding_si_analizza_tutto(self):
        testo = "VERIFICA ESTERNA #130 — APPROVATO\nV-1 (MEDIA) — qualcosa"
        assert be.decidi(_verdetto("APPROVATO", [], testo), SHA, SHA)[0] == "COMMENT"


# ---------------------------------------------------------------------------
# solo_reports(): il dosaggio non deve diventare una scorciatoia
# ---------------------------------------------------------------------------

class TestSoloReports:
    @pytest.mark.parametrize("files", [
        ["reports/ultimo_report.md"],
        ["reports/handoff.md", "reports/stato_progetto.md"],
    ])
    def test_si(self, files):
        assert be.solo_reports(files)

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
        [".mcp.json"],
        [".claude.json"],
        [],                                              # elenco illeggibile
        ["gas.py"] * be.MAX_FILE_API,                    # elenco troncato
    ])
    def test_si(self, files):
        assert be.tocca_macchina_bot(files)

    @pytest.mark.parametrize("files", [
        ["gas.py", "tests/test_unit_kernel.py"],
        ["scripts/gasmerge.sh", ".claude/agents/memoria_revisore.md"],
        ["reports/handoff.md"],
        ["docs/NOTCLAUDE.md", "CLAUDE.md.bak", "scripts/bot_esito.py.bak", ".githubx/a"],
        [".claude/agents/memoria_revisore.md", ".claude/commands/fine-task.md"],
    ])
    def test_no(self, files):
        assert not be.tocca_macchina_bot(files)


# ---------------------------------------------------------------------------
# Comandi con gh finto
# ---------------------------------------------------------------------------

def _gh_finto(tmp_path: Path, head: str, files_out: str = "", fail_head: bool = False) -> dict:
    """gh finto. files_out: righe "nome" o "nuovo<-vecchio" (rename); la risposta
    dell'API è un JSON vero e il filtro --jq dello script gira con jq reale."""
    fake = tmp_path / "bin"
    fake.mkdir()
    log = tmp_path / "gh.log"
    voci = []
    for r in files_out.splitlines():
        nuovo, _, vecchio = r.partition("<-")
        voci.append({"filename": nuovo, **({"previous_filename": vecchio} if vecchio else {})})
    (tmp_path / "files.json").write_text(json.dumps(voci))
    gh = fake / "gh"
    gh.write_text(f"""#!/usr/bin/env bash
printf '%s\\n' "$*" >> {log}
case "$*" in
  *"/reviews"*) cat > {tmp_path}/review.json ;;
  *"/files"*) for a in "$@"; do [ "$prev" = "--jq" ] && expr="$a"; prev="$a"; done
              jq -r "$expr" {tmp_path}/files.json ;;
  *) {"exit 1" if fail_head else f"echo {head}"} ;;
esac
""")
    gh.chmod(0o755)
    env = dict(os.environ, PATH=f"{fake}:{os.environ['PATH']}", REPO="o/r", PR="7",
               GITHUB_OUTPUT=str(tmp_path / "out"), MACCHINA_BOT="false")
    return env


def _run(cmd, env):
    return subprocess.run([sys.executable, str(SCRIPT), cmd], env=env,
                          capture_output=True, text=True)


class TestComandi:
    def test_uso(self):
        r = subprocess.run([sys.executable, str(SCRIPT)], capture_output=True, text=True)
        assert r.returncode == 2

    def test_smista_doc_only(self, tmp_path):
        env = _gh_finto(tmp_path, SHA, "reports/a.md\nreports/b.md\n")
        assert _run("smista", env).returncode == 0
        out = (tmp_path / "out").read_text()
        assert f"head={SHA}" in out and "solo_reports=true" in out and "macchina_bot=false" in out

    def test_smista_rename_da_fuori(self, tmp_path):
        # Rename gas.py → reports/x.md: il vecchio nome conta.
        env = _gh_finto(tmp_path, SHA, "reports/x.md<-gas.py\n")
        _run("smista", env)
        assert "solo_reports=false" in (tmp_path / "out").read_text()

    def test_smista_rename_dalla_macchina_bot(self, tmp_path):
        env = _gh_finto(tmp_path, SHA, "scripts/altro.py<-scripts/bot_esito.py\n")
        _run("smista", env)
        assert "macchina_bot=true" in (tmp_path / "out").read_text()

    @pytest.mark.parametrize("valore", [None, "", "true", "False", "no"])
    def test_esito_macchina_bot_prudente(self, tmp_path, valore):
        # Solo "false" esatto lascia approvare: variabile assente o strana = macchina del bot.
        env = _gh_finto(tmp_path, SHA)
        env.update(HEAD_ANALIZZATA=SHA, VERDETTO_JSON=json.dumps(_verdetto()))
        if valore is None:
            env.pop("MACCHINA_BOT")
        else:
            env["MACCHINA_BOT"] = valore
        _run("esito", env)
        assert json.loads((tmp_path / "review.json").read_text())["event"] == "COMMENT"

    def test_esito_approva_legato_allo_sha(self, tmp_path):
        env = _gh_finto(tmp_path, SHA)
        env.update(HEAD_ANALIZZATA=SHA, VERDETTO_JSON=json.dumps(_verdetto()),
                   MODELLO="claude-fable-5-1")
        assert _run("esito", env).returncode == 0
        review = json.loads((tmp_path / "review.json").read_text())
        assert review["event"] == "APPROVE" and review["commit_id"] == SHA
        assert "claude-fable-5-1" in review["body"] and "VERIFICA ESTERNA #130" in review["body"]

    def test_esito_media_non_approva(self, tmp_path):
        env = _gh_finto(tmp_path, SHA)
        v = _verdetto("APPROVATO CON RISERVE", [_f("V-1", "MEDIA")])
        env.update(HEAD_ANALIZZATA=SHA, VERDETTO_JSON=json.dumps(v))
        _run("esito", env)
        assert json.loads((tmp_path / "review.json").read_text())["event"] == "COMMENT"

    def test_esito_json_rotto(self, tmp_path):
        env = _gh_finto(tmp_path, SHA)
        env.update(HEAD_ANALIZZATA=SHA, VERDETTO_JSON="{non json")
        _run("esito", env)
        assert json.loads((tmp_path / "review.json").read_text())["event"] == "COMMENT"

    def test_esito_verifica_fallita_dichiara_cascata(self, tmp_path):
        env = _gh_finto(tmp_path, SHA)
        env.update(HEAD_ANALIZZATA=SHA, VERDETTO_JSON="",
                   MODELLI_FALLITI="claude-fable-5-1, claude-opus-5-5, claude-opus-4-8")
        _run("esito", env)
        review = json.loads((tmp_path / "review.json").read_text())
        assert review["event"] == "COMMENT" and "claude-opus-4-8" in review["body"]

    def test_esito_head_illeggibile(self, tmp_path):
        env = _gh_finto(tmp_path, SHA, fail_head=True)
        env.update(HEAD_ANALIZZATA=SHA, VERDETTO_JSON=json.dumps(_verdetto()))
        _run("esito", env)
        assert json.loads((tmp_path / "review.json").read_text())["event"] == "COMMENT"

    def test_esito_doc_only(self, tmp_path):
        env = _gh_finto(tmp_path, SHA)
        env.update(HEAD_ANALIZZATA=SHA, SOLO_REPORTS="true")
        _run("esito", env)
        assert json.loads((tmp_path / "review.json").read_text())["event"] == "APPROVE"

    def test_corpo_troncato_sotto_il_limite(self):
        v = _verdetto(testo="VERIFICA ESTERNA #1 — APPROVATO\n" + "x" * 100000)
        assert len(be.componi_corpo("APPROVE", "m", v, "m", "")) < 65536

    def test_testo_lungo_resta_ben_chiuso(self):
        v = _verdetto(testo="VERIFICA ESTERNA #1 — APPROVATO\n" + "x" * 100000)
        assert be.componi_corpo("APPROVE", "m", v, "m", "").endswith("</details>")

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
    def test_concurrency_solo_sui_job_che_lavorano(self, wf):
        # R-158-3: a livello di workflow cancellerebbe verifiche buone su eventi irrilevanti.
        assert "concurrency" not in wf
        assert "concurrency" not in wf["jobs"]["smista"]
        for nome in ("verifica", "esito"):
            assert wf["jobs"][nome]["concurrency"]["cancel-in-progress"] is True

    def test_macchina_bot_passata_a_esito(self, wf):
        env = wf["jobs"]["esito"]["steps"][-1]["env"]
        assert env["MACCHINA_BOT"] == "${{ needs.smista.outputs.macchina_bot }}"

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
        strumenti = [t.strip() for t in wf["jobs"]["verifica"]["env"]["STRUMENTI"].split(",")]
        assert "Read(./**)" in strumenti and "Read" not in strumenti

    def test_cascata_modelli(self, wf):
        args = [s["with"]["claude_args"] for s in wf["jobs"]["verifica"]["steps"]
                if "claude-code-action" in s.get("uses", "")]
        modelli = [a.split("--model ", 1)[1].split()[0] for a in args]
        assert modelli == ["claude-fable-5-1", "claude-opus-5-5", "claude-opus-4-8"]
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
