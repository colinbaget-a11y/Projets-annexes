"""Version 3b : optimisation avec les seules contraintes retenues par l'auteur (novembre 2026).

Obligatoires : recette égale ; au moins 80 % des foyers paient ; même barème pour retraités et actifs,
sans marche, CRDS comprise (par construction).
Cibles souples, chacune avec un écart type (pénalité quadratique : une cible manquée d'un écart type coûte
1 Md€ dans le score, deux écarts types 4 Md€) :
- les personnes seules ne gagnent pas : gain du décile le plus favorisé (D3 à D10), écart type 0,5 point ;
- les familles ne sont pas alourdies : hausse maximale d'un couple avec deux enfants (25-150 k€), 300 € ;
- pas d'écart extravagant entre 100 000 € et 1 M€ de RFR : variation par tranche, 3 points.
Score = coût d'efficacité (Md€, jeu central) + pénalités. Libres : déciles, retraités, indépendants, taux du
haut, crédit par enfant, abattement bébé.
Lancer depuis fiscalite/ : MODE=quotient|indiv python3 ir_csg/optim_v3b.py
"""
import itertools
import sys
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE), str(HERE.parent)]
import bareme_v3 as v  # noqa: E402

G = dict(t0=[0.07, 0.08], db=[0.05, 0.06, 0.07], z1=[30e3, 40e3, 50e3], z2=[80e3, 100e3, 120e3],
         t2=[0.38, 0.40, 0.43, 0.45], C=[1000.0, 1500.0, 2000.0], A=[0.0, 12e3])
# seul_ct : gain d'un salarié seul sans niche (cas-type OpenFisca, 20-150 k€ brut) au-delà de 1 point de revenu
SIG = dict(seuls=0.5, fam=300.0, haut=3.0, seul_ct=0.5)
rows = []
for t0, db, z1, z2, t2, C, A in itertools.product(*G.values()):
    v.ABAT_BEBE = A
    r = v.evalue(t0, db, z1, z2, t2, C)
    r["A"] = A
    r["pen_seuls"] = (max(0.0, -r["seuls_dec_min"]) / SIG["seuls"]) ** 2
    r["pen_fam"] = (max(0.0, r["fam_max_eur"]) / SIG["fam"]) ** 2
    r["pen_haut"] = ((r["haut_min"] / SIG["haut"]) ** 2 + (r["haut_max"] / SIG["haut"]) ** 2) / 2
    r["pen_seul_ct"] = (max(0.0, -r["seul_min_pts"] - 1.0) / SIG["seul_ct"]) ** 2
    r["score"] = r["cout"] + r["pen_seuls"] + r["pen_fam"] + r["pen_haut"] + r["pen_seul_ct"]
    r["ok"] = bool(r["paient"] >= 0.8)
    rows.append(r)
R = pd.DataFrame(rows)
R.round(4).to_csv(HERE / f"sorties/optim_v3b_{v.MODE}.csv", index=False)
cols = ["t0", "tb", "z1", "t1", "z2", "t2", "C", "A", "cout", "d_max_eur", "hausse_D7_10", "seuls_dec_min",
        "fam_max_eur", "ret_max_eur", "haut_min", "haut_max", "paient"]
cols += ["seul_min_pts", "pen_seuls", "pen_fam", "pen_haut", "pen_seul_ct", "score"]
print(v.MODE, int(R.ok.sum()), "admissibles sur", len(R))
print(R[R.ok].sort_values("score").head(10)[cols].round(3).to_string(index=False))
