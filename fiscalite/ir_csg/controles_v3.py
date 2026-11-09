"""Recalcule tous les chiffres cités dans la note, version 3 : sorties/controles_v3.txt (étiquettes [Vn]).

Lancer depuis fiscalite/ : python3 ir_csg/controles_v3.py
"""
import os
import subprocess
import sys
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE), str(HERE.parent)]
import bareme_v3 as v  # noqa: E402

L = []


def p(tag, txt):
    s = f"[{tag}] {txt}"
    print(s)
    L.append(s)


x = v.x
t1, tm, T = v.retenu()
C = v.V3["C"]
n = v.impot(T, C)
CT = v.CT
NEW, NEW_P = v.cas_types(T, C), v.cas_types(T, C, plus=True)

# ------------------------------------------------------------------ cible, barème
p("V1", f"cible {v.CIBLE:.1f} Md€ = IR {x.ir_trav.sum():.1f} (IR IRCOM {x.ir.sum():.1f} − imputé au PFU {x.ir_autres.sum():.1f})"
        f" + CSG {x.csg.sum():.1f} + CRDS {x.crds.sum():.1f} ; assiette brute {x.assiette.sum():.0f}, nette de cotisations"
        f" {x.assiette3.sum():.0f} Md€")
p("V2", f"barème : 7 % au premier euro, 14 % à 20 000 €, {100*t1:.2f} % à 30 000 €, 45 % à 120 000 € (par part) ; crédit {C:.0f} € par enfant")
for a in (10e3, 20e3, 30e3, 50e3, 80e3, 120e3, 200e3):
    p("V3", f"assiette par part {a:>9,.0f} € : marginal {100*float(tm(a)):.1f} %, impôt {float(T(a)):,.0f} €, moyen {100*float(T(a))/a:.1f} %")
p("V4", f"foyers qui paient quelque chose : {100*(v.W*(n > 0)).sum()/v.W.sum():.1f} % (aujourd'hui IR : 47 %)")

# ------------------------------------------------------------------ efficacité et réactions
for j in ("bas", "central", "haut"):
    dz, dr = v.reaction(tm, j)
    p("V5", f"élasticités {j} {v.ELAST[j]} : coût actuel {v.cout_actuel(j):.1f}, proposé {v.cout(tm, j):.1f} Md€ ;"
            f" revenu du travail déclaré {dz:+.1f} Md€, recette induite {dr:+.1f} Md€")

# ------------------------------------------------------------------ déciles, tranches, types
d = v.deciles(n)
p("V6", "déciles, € par foyer : " + ", ".join(f"D{i+1} {u:+.0f}" for i, u in enumerate(d.delta_eur)))
p("V6", "déciles, points de revenu : " + ", ".join(f"D{i+1} {u:+.2f}" for i, u in enumerate(d.delta_pts)))
tr = v.par_tranche(n)
for _, r in tr[tr.a >= 50e3].iterrows():
    p("V7", f"RFR {r.tranche} : {r.delta_pts:+.1f} pts, {r.delta_eur:+,.0f} € par foyer")
pt = v.par_type(n)
p("V8", "par type de revenu (Md€) : " + " ; ".join(f"{i} {r.nouveau - r.actuel:+.1f} (actuel {r.actuel:.1f})" for i, r in pt.iterrows()))
pf = v.par_famille(T, C)
p("V9", f"personnes seules {pf['seuls_mds']:+.1f} Md€ ({pf['seuls_eur']:+.0f} € par foyer) ; couples {pf['couples_mds']:+.1f} Md€"
        f" ({pf['couples_eur']:+.0f} €)")
sd = v.seuls_deciles(T, C)
p("V9", "personnes seules par décile (points) : " + ", ".join(f"D{i+1} {u:+.1f}" for i, u in enumerate(sd)))


# ------------------------------------------------------------------ cas-types
def ligne(profil, brut):
    g = CT[(CT.profil == profil)]
    i = g.index[np.argmin(abs(g.brut.values - brut))]
    r = CT.loc[i]
    mg_a = (r.actuel_plus - r.actuel) / 10
    mg_n = (NEW_P[i] - NEW[i]) / 10
    return r, NEW[i], mg_a, mg_n


for prof in ("seul", "couple_2enf", "couple_0enf", "couple_2enf_mono", "retraite_seul"):
    for b in (10e3, 15e3, 17e3, 20e3, 30e3, 50e3, 80e3, 100e3, 150e3):
        r, nv, ma, mn = ligne(prof, b)
        p("V10", f"{prof:17s} {b:>8,.0f} € : actuel {r.actuel:7,.0f} € ({100*r.actuel/b:4.1f} %, marginal {ma:4.1f} %) ;"
                 f" proposé {nv:7,.0f} € ({100*nv/b:4.1f} %, marginal {mn:4.1f} %) ; écart {nv - r.actuel:+7,.0f} €")
r, nv, _, _ = ligne("seul", 30e3)
p("V11", f"personne seule 30 000 € : IR {r.ir:,.0f}, CSG {r.csg:,.0f}, CRDS {r.crds:,.0f}, total {r.actuel:,.0f} € ;"
         f" proposé {nv:,.0f} €")
r, nv, _, _ = ligne("couple_2enf", 50e3)
p("V11", f"couple deux enfants 50 000 € : IR {r.ir:,.0f}, CSG {r.csg:,.0f}, CRDS {r.crds:,.0f}, total {r.actuel:,.0f} € ;"
         f" proposé {nv:,.0f} €")
g = CT[CT.profil == "retraite_seul"]
dd = NEW[g.index] - g.actuel.values
p("V12", f"retraité seul : hausse maximale {dd.max():+,.0f} € à {g.brut.values[dd.argmax()]:,.0f} € ; hausse jusqu'à"
         f" {g.brut.values[dd > 0].max():,.0f} € de pension ; à 60 000 € {dd[np.argmin(abs(g.brut.values-60e3))]:+,.0f} €")
for prof in ("couple_2enf", "couple_2enf_mono", "couple_0enf", "seul"):
    g = CT[(CT.profil == prof) & (CT.brut >= 20e3) & (CT.brut <= 150e3)]
    dd = NEW[g.index] - g.actuel.values
    p("V13", f"{prof} 20-150 k€ : écart de {dd.min():+,.0f} à {dd.max():+,.0f} € ; moyen {dd.mean():+,.0f} €")
# personnes seules : où le gain du cas-type est-il le plus fort
g = CT[(CT.profil == "seul") & (CT.brut <= 200e3)]
dd = 100 * (NEW[g.index] - g.actuel.values) / g.brut.values
p("V13", f"personne seule : écart de {dd.min():+.1f} pts (à {g.brut.values[dd.argmin()]:,.0f} €) à {dd.max():+.1f} pts")

# ------------------------------------------------------------------ variante : imposition individuelle
code = ("import sys; sys.path[:0]=['ir_csg','.']\nimport bareme_v3 as v\nr=v.evalue(0.07,0.07,30e3,120e3,0.45,750)\n"
        "print(round(r['t1'],4), round(r['cout'],1), round(r['mono_max_eur']), round(r['fam_max_eur']), round(r['couples_mds'],1))")
out = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True, cwd=HERE.parent,
                     env=dict(os.environ, MODE="indiv")).stdout.split()
p("V14", f"variante imposition individuelle (même barème, recalé) : taux à 30 000 € {100*float(out[0]):.1f} %, coût {out[1]} Md€,"
         f" couple deux enfants à un revenu : jusqu'à {int(out[2]):+,} € ; à deux revenus 60/40 : jusqu'à {int(out[3]):+,} € ;"
         f" couples {out[4]} Md€")

# ------------------------------------------------------------------ sensibilités
for env, lab in ((dict(CAPITAL="prorata"), "PFU au prorata"), (dict(CAPITAL="haut"), "PFU en haut"),
                 (dict(PARTAGE="0.6:1"), "partage 60/40 pour tous")):
    code = ("import sys; sys.path[:0]=['ir_csg','.']\nimport bareme_v3 as v\nt1,tm,T=v.retenu()\n"
            "d=v.deciles(v.impot(T,v.V3['C']))\nprint(round(100*t1,2), round(v.CIBLE,1), round(d.delta_eur.abs().max()))")
    out = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True, cwd=HERE.parent,
                         env=dict(os.environ, **env)).stdout.split()
    p("V15", f"sensibilité « {lab} » : taux à 30 000 € {out[0]} %, cible {out[1]} Md€, écart maximal par décile {out[2]} €")

# ------------------------------------------------------------------ arbitrage petites retraites
for tb in (0.10, 0.12, 0.14):
    r = v.evalue(0.07, tb - 0.07, 30e3, 120e3, 0.45, C)
    p("V16", f"taux à 20 000 € de {100*tb:.0f} % : retraité seul hausse max {r['ret_max_eur']:+,.0f} € ;"
             f" écart max par décile {r['d_max_eur']:,.0f} € ; D7-D10 {r['hausse_D7_10']:+.2f} pt ; taux à 30 000 € {100*r['t1']:.1f} %")

(HERE / "sorties/controles_v3.txt").write_text("\n".join(L) + "\n", encoding="utf-8")
