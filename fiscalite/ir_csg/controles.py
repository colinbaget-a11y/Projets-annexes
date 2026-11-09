"""Recalcule tous les chiffres cités dans la note (barème-fonction) : sorties/controles.txt.

Lancer depuis fiscalite/ : python3 ir_csg/controles.py
Chaque ligne de sortie porte une étiquette [Cn] reprise dans un commentaire du .tex à côté du chiffre.
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE), str(HERE.parent)]
import bareme_lisse as b  # noqa: E402
import ir_csg as m  # noqa: E402

L = []


def p(tag, txt):
    s = f"[{tag}] {txt}"
    print(s)
    L.append(s)


P = b.L0
x = b.x
C = pd.read_csv(HERE / "sorties/courbes_openfisca.csv")


def courbe(profil):
    g = C[C.profil == profil].sort_values("brut")
    return g.brut.values, (g.ir + g.csg).values, (g.ir).values, (g.csg).values


def gini(y, w):
    o = np.argsort(y)
    y, w = y[o], w[o]
    pp = np.r_[0, np.cumsum(w) / w.sum()]
    Lc = np.r_[0, np.cumsum(y * w) / (y * w).sum()]
    return 1 - np.sum((pp[1:] - pp[:-1]) * (Lc[1:] + Lc[:-1]))


# ------------------------------------------------------------------ barème et recette
t2v = b.cale(**P)
t1v = b.cale(**P, impot_foyer=b.impot_familial)
tm2, T2 = b.famille(P["F"], P["t0"], P["z1"], t2v, P["z2"], P["t2"])
tm1, T1 = b.famille(P["F"], P["t0"], P["z1"], t1v, P["z2"], P["t2"])
N1 = b.impot_familial(T1)
p("C1", f"cible {b.CIBLE:.1f} Md€ = IR IRCOM {x.ir.sum():.1f} − IR imputé au PFU {x.ir_autres.sum():.1f}"
        f" + CSG sur revenus au barème {x.csg.sum():.1f} ; assiette {x.assiette.sum():.0f} Md€")
p("C2", f"taux à 30 000 € : version 1 {100*t1v:.2f} %, version 2 {100*t2v:.2f} %")
for a in (10e3, 20e3, 30e3, 50e3, 100e3, 200e3):
    p("C3", f"assiette {a:>9,.0f} € : marginal {100*float(tm1(a)):.1f} %, impôt {float(T1(a)):,.0f} €, moyen {100*float(T1(a))/a:.1f} %")
# crédits et réductions d'impôt conservés : recette supplémentaire à lever
for extra in (5.0, 11.0):
    cible0 = b.CIBLE
    b.CIBLE = cible0 + extra
    t = b.cale(**P, impot_foyer=b.impot_familial)
    b.CIBLE = cible0
    p("C4", f"si l'on garde {extra:.0f} Md€ de crédits et réductions d'IR : taux à 30 000 € {100*t:.1f} %")

# ------------------------------------------------------------------ coût d'efficacité, redistribution
p("C5", f"coût d'efficacité : actuel {b.cout(b.TAU_CUR):.1f} ; version 1 {b.cout_familial(tm1):.1f} ;"
        f" version 2 {b.cout(tm2(b.Z)):.1f} Md€")
g0 = gini(b.Z, b.W)
gc = gini(b.Z - b.CUR, b.W)
g1 = gini(b.Z - N1, b.W)
xa = x.assiette.values
pop = x.foyers.values
fs = b.f.copy()
fs["n"] = N1 * b.W / 1e9
n_k = fs.groupby("tranche", sort=False).n.sum().reindex(x.tranche).values
yb, yc, yn = 1e9 * xa / pop, 1e9 * (xa - x.charge.values) / pop, 1e9 * (xa - n_k) / pop
gb, gcb, gnb = gini(yb, pop), gini(yc, pop), gini(yn, pop)
p("C6", f"effet redistributif (baisse du Gini) : foyers représentatifs {(g0-g1)/(g0-gc):.3f} ;"
        f" tranches groupées {(gb-gnb)/(gb-gcb):.3f}")

# ------------------------------------------------------------------ déciles et dernier décile
d = b.deciles(N1)
p("C7", "déciles version 1, € par foyer : " + ", ".join(f"D{i+1} {v:+.0f}" for i, v in enumerate(d.delta_eur)))
k = x.set_index("tranche")
delta_k = 1e9 * (n_k - x.charge.values) / pop
for t, dv in zip(x.tranche, delta_k):
    if x.set_index("tranche").loc[t, "a"] >= 100e3:
        p("C8", f"RFR {t} : {dv:+,.0f} € par foyer ; total {(dv*k.loc[t,'foyers'])/1e9:+.2f} Md€")

# ------------------------------------------------------------------ par type de revenu
pt = b.par_type(N1)
p("C9", "par type de revenu (Md€) : " + " ; ".join(f"{i} {r.nouveau - r.actuel:+.1f}" for i, r in pt.iterrows()))

# ------------------------------------------------------------------ cas-types : retraités, couple
zr, tr, _, _ = courbe("retraite_seul")
for v in (10e3, 15e3, 16e3, 17e3, 18e3, 20e3, 25e3, 30e3):
    p("C10", f"retraité seul, pension {v:,.0f} € : actuel {np.interp(v, zr, tr):,.0f} €, proposé {float(T1(v)):,.0f} €,"
             f" écart {float(T1(v)) - np.interp(v, zr, tr):+,.0f} €")
zs, ts, irs, csgs = courbe("seul")
i = np.argmin(abs(zs - 30e3))
p("C11", f"personne seule 30 000 € brut : CSG {csgs[i]:,.0f} €, IR {irs[i]:,.0f} €, total {ts[i]:,.0f} €, moyen {100*ts[i]/zs[i]:.1f} %")
zc_, tc, _, _ = courbe("couple_2enf")
ab = b.FR_ADULTE + 2 * b.ABAT_ENFANT
ec = np.array([float(T1(max(0.9825 * v - ab, 0))) for v in zc_]) - tc
for v in (30e3, 40e3, 50e3, 60e3, 70e3, 80e3, 100e3, 150e3):
    j = np.argmin(abs(zc_ - v))
    p("C12", f"couple deux enfants {v:,.0f} € brut : écart proposé − actuel {ec[j]:+,.0f} €")
pos = zc_[ec > 0]
p("C12", f"couple deux enfants : hausse entre {pos.min():,.0f} et {pos.max():,.0f} € ; maximum {ec.max():+,.0f} € à {zc_[ec.argmax()]:,.0f} €")
for v in (20e3, 50e3, 80e3, 150e3):
    j = np.argmin(abs(zs - v))
    p("C13", f"personne seule {v:,.0f} € brut : moyen actuel {100*ts[j]/zs[j]:.1f} %, proposé {100*float(T1(0.9825*v))/v:.1f} %")

# ------------------------------------------------------------------ pensions : foyers concernés
for t in x.tranche[:4]:
    p("C14", f"foyers percevant des pensions, RFR {t} : {k.loc[t, 'foyers_pensions']/1e6:.2f} M")

# ------------------------------------------------------------------ second apporteur (par rapport à la version 1)
def indiv(T, part=0.6):
    zc = np.clip(b.Z - b.N_ENF * b.ABAT_ENFANT, 0, None)
    return (1 - b.S_COUPLE) * T(zc) + b.S_COUPLE * (T(part * zc) + T((1 - part) * zc))


for part in (0.6, 0.5):
    cost = ((b.impot_familial(T1) - indiv(T1, part)) * b.W).sum() / 1e9
    t = b.cale(**P, impot_foyer=lambda T_, part=part: indiv(T_, part))
    p("C15", f"imposition séparée des adultes ({100*part:.0f}/{100*(1-part):.0f}) au lieu de la version 1 : coût"
             f" {cost:.1f} Md€ ; taux à 30 000 € {100*t:.1f} %")

# ------------------------------------------------------------------ option franchise de 10 000 €
OPT = dict(F=10e3, t0=0.10, z1=30e3, z2=400e3, t2=0.45)
to = b.cale(**OPT, impot_foyer=b.impot_familial)
tmo, To = b.famille(OPT["F"], OPT["t0"], OPT["z1"], to, OPT["z2"], OPT["t2"])
do = b.deciles(b.impot_familial(To))
p("C16", f"option franchise 10 000 € (10 % → {100*to:.1f} % à 30 000 € → 45 % à 400 000 €) : déciles "
         + ", ".join(f"D{i+1} {v:+.0f}" for i, v in enumerate(do.delta_eur)))
for v in (15e3, 17e3, 20e3):
    p("C16", f"  retraité seul {v:,.0f} € : écart {float(To(v)) - np.interp(v, zr, tr):+,.0f} €")

# ------------------------------------------------------------------ PFU : sensibilité du taux
import os  # noqa: E402
import subprocess  # noqa: E402
code = ("import sys; sys.path[:0]=['ir_csg','.']\nimport bareme_lisse as b\n"
        "t=b.cale(**b.L0, impot_foyer=b.impot_familial); print(round(b.CIBLE,1), round(100*t,2))")
for cap in ("prorata", "mixte", "haut"):
    for split in ("", "prorata"):
        env = dict(os.environ, CAPITAL=cap, SPLIT=split)
        out = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True, env=env,
                             cwd=HERE.parent).stdout.split()
        p("C17", f"PFU réparti « {cap} », IR partagé « {split or '12,8 %'} » : cible {out[0]} Md€, taux à 30 000 € {out[1]} %")

(HERE / "sorties/controles.txt").write_text("\n".join(L) + "\n", encoding="utf-8")
