"""Addestra la testa di openWakeWord (stessa rete di openwakeword/train.py: Flatten →
Linear → LayerNorm → ReLU → [Linear → LayerNorm → ReLU]×n → Linear → Sigmoid, ingresso
16×96) in JAX su CPU, con la ricetta di openwakeword.train.Model.auto_train: tre sequenze
(lr 1e-4, 1e-5, 1e-6), peso dei negativi che sale da 1 a max_negative_weight, solo esempi
«difficili» nel batch, checkpoint scelti per richiamo con falsi/ora sotto il bersaglio e
mediati. Esporta un .onnx che openwakeword.model.Model carica così com'è.

Uso: python addestra.py <dati> <feat> <uscita.onnx> [--dim 64 --blocchi 1 --passi 30000]"""
from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

import jax
import jax.numpy as jnp
import numpy as np
import optax

jax.config.update("jax_platforms", "cpu")


# ── rete ──
def init(key, dim: int, blocchi: int):
    def lin(k, i, o):
        lim = 1 / np.sqrt(i)   # come nn.Linear di PyTorch
        k1, k2 = jax.random.split(k)
        return {"w": jax.random.uniform(k1, (i, o), minval=-lim, maxval=lim),
                "b": jax.random.uniform(k2, (o,), minval=-lim, maxval=lim)}
    ks = jax.random.split(key, blocchi + 2)
    p = {"l1": lin(ks[0], 16 * 96, dim), "ln1": {"g": jnp.ones(dim), "b": jnp.zeros(dim)},
         "blk": [{"l": lin(ks[1 + i], dim, dim), "ln": {"g": jnp.ones(dim), "b": jnp.zeros(dim)}}
                 for i in range(blocchi)],
         "out": lin(ks[-1], dim, 1)}
    return p


def _ln(x, p):
    m = x.mean(-1, keepdims=True)
    v = ((x - m) ** 2).mean(-1, keepdims=True)
    return (x - m) / jnp.sqrt(v + 1e-5) * p["g"] + p["b"]


def logit(p, x):
    h = x.reshape(x.shape[0], -1)
    h = jax.nn.relu(_ln(h @ p["l1"]["w"] + p["l1"]["b"], p["ln1"]))
    for b in p["blk"]:
        h = jax.nn.relu(_ln(h @ b["l"]["w"] + b["l"]["b"], b["ln"]))
    return (h @ p["out"]["w"] + p["out"]["b"])[:, 0]


prob = jax.jit(lambda p, x: jax.nn.sigmoid(logit(p, x)))


def perdita(p, x, y, wneg):
    z = logit(p, x)
    pr = jax.nn.sigmoid(z)
    # come train.py: contano solo i negativi con p >= 0.001 e i positivi con p < 0.999
    tieni = jnp.where(y > 0.5, pr < 0.999, pr >= 0.001).astype(jnp.float32)
    w = jnp.where(y > 0.5, 1.0, wneg) * jax.lax.stop_gradient(tieni)
    bce = optax.sigmoid_binary_cross_entropy(z, y)
    return (w * bce).sum() / jnp.maximum(jax.lax.stop_gradient(tieni).sum(), 1.0)


# ── dati ──
class Dati:
    def __init__(self, dati: Path, feat: Path, n_acav: int, n_fette: int = 99,
                 self_veri=("mls_train", "ami_train")):
        self.pos = np.load(feat / "pos_train.npy").astype(np.float32)
        self.neg = np.concatenate([np.load(feat / f"{k}.npy").astype(np.float32)
                                   for k in ("neg_train", "neg2_train") if (feat / f"{k}.npy").exists()])
        # parlato vero (MLS italiano letto + AMI inglese di riunione da lontano), insieme
        vero = [np.load(feat / f"{k}.npy").astype(np.float32) for k in self_veri if (feat / f"{k}.npy").exists()]
        self.mls = np.concatenate(vero) if vero else None
        # fette di openwakeword_features (ACAV100M) lette in memmap: niente copia in RAM
        self.acav = [np.memmap(f, dtype=np.float16, mode="r").reshape(-1, 16, 96)
                     for f in sorted((dati / "feat").glob("acav_*.bin"))[:n_fette]]
        if n_acav:
            self.acav = [m[: n_acav // len(self.acav)] for m in self.acav]
        self.pos_t = np.load(feat / "pos_test.npy").astype(np.float32)
        self.neg_t = np.load(feat / "neg_test.npy").astype(np.float32)
        v = np.load(dati / "feat" / "validation_set_features.npy").astype(np.float32)
        meta = len(v) // 2   # metà A per scegliere i checkpoint, metà B solo per il rapporto
        self.val_a, self.val_b = v[:meta], v[meta:]
        print("dati: pos %d neg %d mls %d acav %d | pos_test %d neg_test %d | val %.1f+%.1f h" % (
            len(self.pos), len(self.neg), 0 if self.mls is None else len(self.mls), sum(map(len, self.acav)),
            len(self.pos_t), len(self.neg_t), len(self.val_a) * 0.08 / 3600, len(self.val_b) * 0.08 / 3600),
            flush=True)

    def batch(self, rng, n):
        parti = [(self.pos, n["pos"], 1.0), (self.neg, n["neg"], 0.0)]
        parti += [(m, n["acav"] // len(self.acav), 0.0) for m in self.acav]
        if self.mls is not None:
            parti.append((self.mls, n["mls"], 0.0))
        xs, ys = [], []
        for arr, k, lab in parti:
            idx = np.sort(rng.integers(0, len(arr), k))
            xs.append(np.asarray(arr[idx], np.float32))
            ys.append(np.full(k, lab, np.float32))
        return np.concatenate(xs), np.concatenate(ys)


def finestre(v: np.ndarray) -> np.ndarray:
    from numpy.lib.stride_tricks import sliding_window_view
    return sliding_window_view(v, (16, 96))[:, 0]


def falsi_ora(p, v: np.ndarray, soglia: float = 0.5) -> float:
    """Attivazioni all'ora sul flusso di caratteristiche: blocchi sopra soglia, contando un
    evento per fronte di salita (una parola = un'attivazione)."""
    w = finestre(v)
    s = np.concatenate([np.asarray(prob(p, jnp.asarray(w[i:i + 65536])))
                        for i in range(0, len(w), 65536)])
    sopra = s >= soglia
    eventi = int((sopra[1:] & ~sopra[:-1]).sum() + sopra[0])
    return eventi / (len(v) * 0.08 / 3600), s


def valuta(p, d: Dati):
    pp = np.asarray(prob(p, jnp.asarray(d.pos_t)))
    pn = np.asarray(prob(p, jnp.asarray(d.neg_t)))
    fa, _ = falsi_ora(p, d.val_a)
    return {"richiamo": float((pp >= 0.5).mean()), "acc_neg": float((pn < 0.5).mean()),
            "fp_ora_valA": fa}


def sequenza(p, d, opt_lr, passi, wmax, rng, n, punti_val, storia, ckpt):
    warm, hold = passi // 5, passi // 3

    def lr_a(s):
        if s < warm:
            return opt_lr * s / max(warm, 1)
        if s < warm + hold:
            return opt_lr
        return 0.5 * opt_lr * (1 + np.cos(np.pi * (s - warm - hold) / max(passi - warm - hold, 1)))
    opt = optax.scale_by_adam()
    st = opt.init(p)

    @jax.jit
    def passo(p, st, x, y, wneg, lr):
        l, g = jax.value_and_grad(perdita)(p, x, y, wneg)
        up, st = opt.update(g, st, p)
        up = jax.tree_util.tree_map(lambda u: -lr * u, up)
        return optax.apply_updates(p, up), st, l
    pesi = np.linspace(1, wmax, passi)
    t0 = time.time()
    for s in range(passi):
        x, y = d.batch(rng, n)
        p, st, l = passo(p, st, jnp.asarray(x), jnp.asarray(y), float(pesi[s]), float(lr_a(s)))
        if s in punti_val:
            v = valuta(p, d)
            v.update(passo=s, perdita=float(l), lr=opt_lr, wneg=float(pesi[s]))
            storia.append(v)
            ckpt.append((v, jax.tree_util.tree_map(np.asarray, p)))
            print(json.dumps(v), "%.0fs" % (time.time() - t0), flush=True)
    return p


def media(ps):
    return jax.tree_util.tree_map(lambda *a: np.mean(np.stack(a), 0), *ps)


def esporta_onnx(p, percorso: Path, nome_uscita: str):
    import onnx
    from onnx import TensorProto, helper, numpy_helper
    nodi, init_ = [], []

    def c(nome, arr):
        init_.append(numpy_helper.from_array(np.asarray(arr, np.float32), nome))
        return nome
    init_.append(numpy_helper.from_array(np.array([1, 16 * 96], np.int64), "forma"))
    nodi.append(helper.make_node("Reshape", ["x", "forma"], ["h0"]))
    h = "h0"
    strati = [(p["l1"], p["ln1"])] + [(b["l"], b["ln"]) for b in p["blk"]]
    for i, (l, ln) in enumerate(strati):
        nodi.append(helper.make_node("Gemm", [h, c(f"w{i}", l["w"]), c(f"b{i}", l["b"])], [f"g{i}"]))
        nodi.append(helper.make_node("LayerNormalization", [f"g{i}", c(f"lg{i}", ln["g"]), c(f"lb{i}", ln["b"])],
                                     [f"n{i}"], axis=-1, epsilon=1e-5))
        nodi.append(helper.make_node("Relu", [f"n{i}"], [f"r{i}"]))
        h = f"r{i}"
    nodi.append(helper.make_node("Gemm", [h, c("wo", p["out"]["w"]), c("bo", p["out"]["b"])], ["z"]))
    nodi.append(helper.make_node("Sigmoid", ["z"], [nome_uscita]))
    g = helper.make_graph(nodi, "ehi_jarvis_it",
                          [helper.make_tensor_value_info("x", TensorProto.FLOAT, [1, 16, 96])],
                          [helper.make_tensor_value_info(nome_uscita, TensorProto.FLOAT, [1, 1])], init_)
    m = helper.make_model(g, opset_imports=[helper.make_opsetid("", 17)], producer_name="gas-oww-it")
    m.ir_version = 8
    onnx.checker.check_model(m)
    onnx.save(m, str(percorso))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("dati")
    ap.add_argument("feat")
    ap.add_argument("uscita")
    ap.add_argument("--dim", type=int, default=64)
    ap.add_argument("--blocchi", type=int, default=1)
    ap.add_argument("--passi", type=int, default=30000)
    ap.add_argument("--wmax", type=float, default=1500)
    ap.add_argument("--fp_bersaglio", type=float, default=0.5)
    ap.add_argument("--n_acav", type=int, default=0)
    ap.add_argument("--fette_acav", type=int, default=99)
    ap.add_argument("--veri", default="mls_train,ami_train", help="negativi di parlato vero")
    ap.add_argument("--seme", type=int, default=0)
    ap.add_argument("--batch", default="128,96,160,1024", help="positivi,avversari,mls,acav per passo")
    a = ap.parse_args()
    d = Dati(Path(a.dati), Path(a.feat), a.n_acav, a.fette_acav, tuple(a.veri.split(",")))
    rng = np.random.default_rng(a.seme)
    n = dict(zip(("pos", "neg", "mls", "acav"), (int(v) for v in a.batch.split(","))))
    p = init(jax.random.PRNGKey(a.seme), a.dim, a.blocchi)
    storia, ckpt = [], []
    passi, lr, wmax = a.passi, 1e-4, a.wmax
    for seq in range(3):
        if seq == 0:
            punti = set(np.linspace(passi - passi // 4, passi - 1, 20).astype(int).tolist())
        else:
            passi = a.passi // 10
            lr /= 10
            if min(c[0]["fp_ora_valA"] for c in ckpt) > a.fp_bersaglio:
                wmax *= 2
            punti = set(np.linspace(1, passi - 1, 20).astype(int).tolist())
        print(f"── sequenza {seq + 1}: passi {passi} lr {lr} wmax {wmax}", flush=True)
        p = sequenza(p, d, lr, passi, wmax, rng, n, punti, storia, ckpt)
    # scelta: checkpoint con falsi/ora (metà A) sotto il bersaglio, i 5 col richiamo migliore, mediati
    buoni = [c for c in ckpt if c[0]["fp_ora_valA"] <= a.fp_bersaglio] or \
        sorted(ckpt, key=lambda c: c[0]["fp_ora_valA"])[:5]
    buoni = sorted(buoni, key=lambda c: -c[0]["richiamo"])[:5]
    cand = [("media", media([c[1] for c in buoni]))] + [("migliore", buoni[0][1])]
    scelto = None
    for nome, pc in cand:
        v = valuta(pc, d)
        print("candidato", nome, json.dumps(v), flush=True)
        if scelto is None and v["fp_ora_valA"] <= max(a.fp_bersaglio, buoni[0][0]["fp_ora_valA"]):
            scelto = (nome, pc, v)
    scelto = scelto or (cand[1][0], cand[1][1], valuta(cand[1][1], d))
    nome, pc, v = scelto
    fb, _ = falsi_ora(pc, d.val_b)
    v["fp_ora_valB_rapporto"] = fb
    for s in (0.3, 0.5, 0.7, 0.9):
        v[f"fp_ora_valB@{s}"] = falsi_ora(pc, d.val_b, s)[0]
        v[f"richiamo_test@{s}"] = float((np.asarray(prob(pc, jnp.asarray(d.pos_t))) >= s).mean())
    print("SCELTO", nome, json.dumps(v), flush=True)
    out = Path(a.uscita)
    esporta_onnx(pc, out, out.stem)
    np.savez(out.with_suffix(".pesi.npz"), **{k: v for k, v in _piatto(pc).items()})
    json.dump({"scelto": nome, "metriche": v, "storia": storia, "argomenti": vars(a)},
              open(out.with_suffix(".json"), "w"), indent=1)
    # controllo: onnx == jax
    import onnxruntime as ort
    s = ort.InferenceSession(str(out))
    x = d.pos_t[:8]
    o = np.array([s.run(None, {"x": x[i:i + 1]})[0][0, 0] for i in range(8)])
    print("controllo onnx-jax: max diff", float(np.abs(o - np.asarray(prob(pc, jnp.asarray(x)))).max()))


def _piatto(p, pre=""):
    out = {}
    if isinstance(p, dict):
        for k, v in p.items():
            out.update(_piatto(v, f"{pre}{k}."))
    elif isinstance(p, list):
        for i, v in enumerate(p):
            out.update(_piatto(v, f"{pre}{i}."))
    else:
        out[pre[:-1]] = np.asarray(p)
    return out


if __name__ == "__main__":
    main()
