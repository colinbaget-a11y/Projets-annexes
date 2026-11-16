"""Fusion IR-CSG-CRDS : chaque arbitrage chiffré comme une variante d'un système de référence.

Référence (consigne de l'auteur) : assiette large, impôt individuel, même barème pour tous, ni franchise ni aide
familiale dans l'impôt ; barème à taux marginal en ligne droite (nœuds 0, 20 000 €, z1, z2 ; 50 % au-delà de z2)
choisi pour minimiser la perte sèche à recette égale (220 Md€). Chaque variante modifie un seul paramètre ; la
recette est rétablie par un même nombre de points ajouté à tous les taux sous le taux supérieur (« coût en points
de taux pour tous »).

Perte sèche : deux mesures.
- quadratique (celle des notes) : ½·e·z·τ²/(1−τ), τ = taux marginal IR + CSG + CRDS ;
- généralisée (Harberger avec distorsions préexistantes et déplacements d'assiette, voir
  ../revue/methode_perte_seche.md) : e·z·(τg²/2 − σ·t_s·τg)/(1−τg), τg = τ + τ_autres (cotisations non
  contributives, retrait des prestations), σ = part de la réaction qui se déplace vers une assiette taxée à t_s.
  Paramètres dans GEN ci-dessous (par défaut : 0, ce qui redonne la quadratique).

Lancer depuis fiscalite/ : python3 synthese/arbitrages_ircsg.py  ->  synthese/sorties/arbitrages_ircsg.txt
"""
import itertools
import json
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE.parent / "ir_csg"), str(HERE.parent)]
import proposition as pr  # noqa: E402

v, ex = pr.v, pr.ex
W, Z, ZN, R, Q = pr.W, pr.Z, pr.ZN, pr.R, pr.Q
TOP0 = pr.TOP
OUT = HERE / "sorties"
OUT.mkdir(exist_ok=True)

ACT = pr.LABN                    # salaires, indépendants, gérants et loyers (non séparables dans les données)
PENS = ZN * v.PART_PENS          # pensions de retraite (assiette nette)
TOUT = ZN

# paramètres de la perte sèche généralisée (à renseigner d'après revue/methode_perte_seche.md)
GEN = dict(
    tau_autres=lambda z_brut: 0.0 * z_brut,   # coin marginal hors IR-CSG sur les revenus du travail, par € brut
    sigma=lambda q: 0.0 * q,                    # part de la réaction déplacée vers une autre assiette, par rang q
    t_s=0.0,                                    # taux de l'assiette d'accueil (IS + PFU, ou PFU seul)
)


def impot(tm, T, o, parts, kids):
    """Impôt d'un type de foyer et taux marginal de chaque adulte (sur l'assiette nette)."""
    zs = [sh * ZN for sh in parts]
    couv = {"activite": ACT, "tout": TOUT, "aucune": 0 * ZN}[o.get("couv", "aucune")]
    fr = [np.minimum(o.get("F", 0.0), sh * couv) + np.minimum(o.get("Fp", 0.0), sh * PENS) for sh in parts]
    ab = [o.get("abat_pens", 0.0) * sh * PENS for sh in parts]
    tax = [np.clip(z - f - a, 0, None) for z, f, a in zip(zs, fr, ab)]
    fam = o.get("fam", "rien")
    if fam == "quotient":
        y = sum(tax)
        if len(parts) == 2:
            p0, p = 2.0, 2.0 + 0.5 * kids
            cap = 2 * pr.PLAF * (p - p0)
        else:
            p0, p = 1.0, 1.0 + (1.0 if kids else 0.0)
            cap = pr.PLAF_ISOL if kids else 0.0
        i0, i1 = p0 * T(y / p0), p * T(y / p)
        borne = i0 - cap > i1
        imp = np.maximum(i1, i0 - cap)
        mg = np.where(borne, tm(y / p0), tm(y / p))
        return imp, [mg for _ in parts]
    if fam == "franchise" and kids:
        haut = np.argmax(np.vstack(zs), axis=0) if len(zs) == 2 else np.zeros(len(ZN), int)
        tax = [np.where(haut == k, np.clip(t - o.get("FE", pr.FR_ENF) * kids, 0, None), t) for k, t in enumerate(tax)]
    imp = sum(T(t) for t in tax)
    if fam == "cheque":
        imp = imp - pr.CHEQUE * kids
    return imp, [np.where(t > 0, tm(t), 0.0) for t in tax]


def _dwl(e, z, tau, q):
    tg = np.clip(tau + GEN["tau_autres"](z), 0, 0.95)
    return e * z * (tg ** 2 / 2 - GEN["sigma"](q) * GEN["t_s"] * tg) / (1 - tg)


def systeme(tm, T, o):
    n = np.zeros_like(Z)
    pt, cq, cg = {}, {j: 0.0 for j in ("bas", "central", "haut")}, {j: 0.0 for j in ("bas", "central", "haut")}
    e = {j: v.elast(j) for j in cq}
    for nom, w, parts, kids, cur in pr.TYPES:
        imp, mgs = impot(tm, T, o, parts, kids)
        n += w * imp
        pt[nom] = (w, imp, cur)
        for sh, mg in zip(parts, mgs):
            tau = np.clip(mg * R, 0, 0.95)
            for j in cq:
                cq[j] += (w * 0.5 * e[j] * sh * Z * tau ** 2 / (1 - tau)).sum() / 1e9
                cg[j] += (w * _dwl(e[j], sh * Z, tau, Q)).sum() / 1e9
    return n / W, pt, cq, cg


def dwl_actuel():
    """Perte sèche d'aujourd'hui, quadratique et généralisée, au taux marginal actuel du foyer."""
    t = v.bl.TAU_CUR
    out = {}
    for j in ("bas", "central", "haut"):
        e = v.elast(j)
        out[j] = ((W * 0.5 * e * Z * t ** 2 / (1 - t)).sum() / 1e9, (W * _dwl(e, Z, t, Q)).sum() / 1e9)
    return out


def bareme(t0, tb, z1, t1, z2, d=0.0, top=None):
    top = TOP0 if top is None else top
    return ex.bareme_lineaire([0, 20e3, z1, z2], [t0 + d, tb + d, t1 + d, top])


def recette(tm, T, o):
    return (W * systeme(tm, T, o)[0]).sum() / 1e9


def cale_t1(t0, tb, z1, z2, o):
    lo, hi = 0.0, TOP0
    for _ in range(34):
        t1 = (lo + hi) / 2
        lo, hi = (t1, hi) if recette(*bareme(t0, tb, z1, t1, z2), o) < v.CIBLE else (lo, t1)
    return (lo + hi) / 2


def cale_d(b, o, top=None):
    lo, hi = -0.15, 0.25
    for _ in range(34):
        d = (lo + hi) / 2
        lo, hi = (d, hi) if recette(*bareme(*b, d=d, top=top), o) < v.CIBLE else (lo, d)
    return (lo + hi) / 2


def reference(o, G):
    best = None
    for t0, tb, z1, z2 in itertools.product(*G.values()):
        if tb < t0 or z1 >= z2:
            continue
        t1 = cale_t1(t0, tb, z1, z2, o)
        if not tb <= t1 < TOP0 - 1e-3:
            continue
        c = systeme(*bareme(t0, tb, z1, t1, z2), o)[2]["central"]
        if best is None or c < best[0]:
            best = (c, (t0, tb, z1, t1, z2))
    return best[1]


def bilan(nom, b, o, p, d=0.0, top=None):
    tm, T = bareme(*b, d=d, top=top)
    n, pt, cq, cg = systeme(tm, T, o)
    per = pr.perdants(pt)
    dec = v.deciles(n)
    ty = v.par_type(n)
    agg = {}
    for k, (w, imp, cur) in pt.items():
        g = k.split("_")[0] if k.startswith("couple") else k
        a = agg.setdefault(g, [0.0, 0.0])
        a[0] += (w * (imp - cur)).sum()
        a[1] += w.sum()
    p(f"[{nom}] décalage {100*d:+.2f} pt ; recette {(W*n).sum()/1e9:.1f} ; perte sèche quadratique {cq['central']:.1f}"
      f" ({cq['bas']:.1f}-{cq['haut']:.1f}) ; généralisée {cg['central']:.1f} ({cg['bas']:.1f}-{cg['haut']:.1f}) ;"
      f" perdants >500 € {per[500][1]:.0f} %, >1000 € {per[1000][1]:.0f} %")
    p(f"    déciles € " + " ".join(f"{u:+.0f}" for u in dec.delta_eur))
    p(f"    types Md€ " + " ; ".join(f"{i} {r.nouveau - r.actuel:+.1f}" for i, r in ty.iterrows()))
    p(f"    foyers € " + " ; ".join(f"{g} {a[0]/a[1]:+,.0f}" for g, a in agg.items()))
    return dict(nom=nom, d=d, cq=cq, cg=cg, per=per, dec=list(dec.delta_eur), agg={g: a[0] / a[1] for g, a in agg.items()})


if __name__ == "__main__":
    L = []

    def p(s):
        print(s, flush=True)
        L.append(s)
    act = dwl_actuel()
    p(f"[AUJ] perte sèche aujourd'hui : quadratique {act['central'][0]:.1f} ({act['bas'][0]:.1f}-{act['haut'][0]:.1f}),"
      f" généralisée {act['central'][1]:.1f} ({act['bas'][1]:.1f}-{act['haut'][1]:.1f}) Md€")
    ref_o = dict(couv="aucune", F=0.0, fam="rien")
    G = dict(t0=[0.10, 0.12, 0.14, 0.16, 0.18], tb=[0.14, 0.16, 0.18, 0.20, 0.22],
             z1=[45e3, 60e3, 80e3, 120e3], z2=[250e3, 400e3, 600e3])
    b = reference(ref_o, G)
    p(f"[REF] barème de référence : {100*b[0]:.0f} % au premier euro, {100*b[1]:.0f} % à 20 k€, {100*b[3]:.1f} % à "
      f"{b[2]/1e3:.0f} k€, 50 % à {b[4]/1e3:.0f} k€")
    res = [bilan("REF assiette large, même barème pour tous", b, ref_o, p)]
    variantes = [
        ("Franchise d'activité 4 000 €", dict(ref_o, couv="activite", F=4000.0)),
        ("Franchise d'activité 8 000 €", dict(ref_o, couv="activite", F=8000.0)),
        ("Franchise de 8 000 € sur tous les revenus", dict(ref_o, couv="tout", F=8000.0)),
        ("Pensions exonérées jusqu'à 12 500 €", dict(ref_o, Fp=12500.0)),
        ("Abattement de 10 % sur les pensions", dict(ref_o, abat_pens=0.10)),
        ("Famille : franchise de 6 000 € par enfant", dict(ref_o, fam="franchise")),
        ("Famille : chèque par enfant", dict(ref_o, fam="cheque")),
        ("Imposition commune : quotient conjugal et familial", dict(ref_o, fam="quotient")),
        ("Ancienne proposition : franchise d'activité 8 000 € + 6 000 € par enfant",
         dict(ref_o, couv="activite", F=8000.0, fam="franchise")),
    ]
    for nom, o in variantes:
        d = cale_d(b, o)
        res.append(bilan(nom, b, o, p, d=d))
    for top in (0.45, 0.55):
        d = cale_d(b, ref_o, top=top)
        res.append(bilan(f"Taux supérieur {100*top:.0f} %", b, ref_o, p, d=d, top=top))
    (OUT / "arbitrages_ircsg.txt").write_text("\n".join(L) + "\n", encoding="utf-8")
    (OUT / "arbitrages_ircsg.json").write_text(json.dumps(dict(ref=b, res=res), default=float, indent=1))
