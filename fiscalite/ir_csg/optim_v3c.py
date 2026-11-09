"""Version 3c : démarche en deux temps (novembre 2026).

1. Agnostique : parmi les barèmes sans marche (taux marginal en ligne droite par morceaux, même barème pour
   tous les revenus après cotisations, CRDS comprise, deux parts pour un couple, crédit par enfant), celui qui
   minimise la perte sèche (coût d'efficacité, jeu central d'élasticités) à recette égale.
2. Correction légère, par pénalités souples (une cible manquée d'un écart type coûte 1 Md€ dans le score) :
   - équité entre foyers sans niche : au même salaire brut (40-100 k€), une personne seule ne gagne pas plus
     qu'un couple avec deux enfants (écart de gain en points de revenu, écart type 0,5) ;
   - pas d'écart extravagant entre 100 000 € et 1 M€ de RFR (écart type 3 points) ;
   - dernier décile (écart type 1,5 point de hausse).
Lancer depuis fiscalite/ : python3 ir_csg/optim_v3c.py
"""
import itertools
import sys
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE), str(HERE.parent)]
import bareme_v3 as v  # noqa: E402

v.ABAT_BEBE = 0.0
G = dict(t0=[0.05, 0.07, 0.09], db=[0.03, 0.06, 0.09], z1=[30e3, 50e3], z2=[80e3, 120e3, 250e3],
         t2=[0.30, 0.35, 0.40, 0.45], C=[500.0, 750.0, 1000.0])
SIG = dict(equite=0.5, haut=3.0, d10=1.5)
CT = v.CT


def equite(T, C):
    """Gain d'une personne seule moins gain d'un couple avec deux enfants, au même brut (points de revenu)."""
    n = v.cas_types(T, C)
    s = CT[(CT.profil == "seul") & CT.brut.between(40e3, 100e3)]
    c = CT[(CT.profil == "couple_2enf") & CT.brut.between(40e3, 100e3)]
    gs = -(n[s.index] - s.actuel.values) / s.brut.values
    gc = -(n[c.index] - c.actuel.values) / c.brut.values
    return 100 * (gs - gc)


rows = []
for t0, db, z1, z2, t2, C in itertools.product(*G.values()):
    t1 = v.cale(t0, t0 + db, z1, z2, t2, C)
    tm, T = v.famille(t0, t0 + db, z1, t1, z2, t2)
    n = v.impot(T, C)
    d = v.deciles(n)
    tr = v.par_tranche(n)
    haut = tr[(tr.a >= 100e3) & (tr.a < 1e6)].delta_pts
    eq = equite(T, C)
    r = dict(t0=t0, tb=t0 + db, z1=z1, t1=t1, z2=z2, t2=t2, C=C, cout=v.cout(tm),
             paient=(v.W * (n > 0)).sum() / v.W.sum(), d_min=d.delta_eur.min(), d_max=d.delta_eur.max(),
             d10_pts=d.delta_pts.iloc[9], haut_min=haut.min(), haut_max=haut.max(),
             equite_moy=eq.mean(), equite_max=eq.max(), ret_max=v.ecart_profil(T, C, "retraite_seul", 8e3, 40e3, pct=False).max())
    r["pen_equite"] = float(np.mean(np.clip(eq, 0, None) ** 2)) / SIG["equite"] ** 2
    r["pen_haut"] = ((r["haut_min"] / SIG["haut"]) ** 2 + (r["haut_max"] / SIG["haut"]) ** 2) / 2
    r["pen_d10"] = (max(0.0, r["d10_pts"]) / SIG["d10"]) ** 2
    r["score"] = r["cout"] + r["pen_equite"] + r["pen_haut"] + r["pen_d10"]
    rows.append(r)
R = pd.DataFrame(rows)
R = R[R.paient >= 0.8]
R.round(4).to_csv(HERE / "sorties/optim_v3c.csv", index=False)
pd.set_option("display.width", 300)
print("1. Agnostique : perte sèche minimale")
print(R.sort_values("cout").head(5).round(3).to_string(index=False))
print("2. Corrigé : score")
print(R.sort_values("score").head(8).round(3).to_string(index=False))
