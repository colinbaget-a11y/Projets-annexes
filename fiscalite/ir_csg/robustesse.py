"""Tests de robustesse du chiffrage IR + CSG et recherche du barème « le plus proportionnel ».

Lancer depuis fiscalite/ : python3 ir_csg/robustesse.py  ->  ir_csg/sorties/robustesse.txt

1. Validation de la reconstitution sur des agrégats indépendants (CCSS, 2042, Eurostat).
2. Sensibilité de la cible, de l'assiette et du barème E aux hypothèses (indépendants, partage de
   l'IR capital/travail, forme intra-tranche, nombre de points).
3. Balayage des barèmes « franchise + taux unique + deux taux supérieurs » : pour chaque scénario,
   celui dont le taux unique s'étend le plus loin sans faire baisser l'indice de Kakwani.
"""
import itertools
import os
import sys
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE), str(HERE.parent)]
import ir_csg as m  # noqa: E402

OUT = HERE / "sorties" / "robustesse.txt"
lignes = []


def p(*a):
    s = " ".join(str(v) for v in a)
    print(s)
    lignes.append(s)


def kak_tranches(x, impot_tranche):
    return m.kakwani(x.assiette.values, impot_tranche, x.foyers.values)


def evalue(x, f, seuils, taux):
    f = f.copy()
    f["n"] = f.poids * m.impot(f.base, seuils, taux) / 1e9
    nouv = f.groupby("tranche", sort=False).n.sum().reindex(x.tranche).values
    return nouv


# ------------------------------------------------------------------ 1. validation
x, f = m.distribution()
p("=== 1. Validation sur agrégats indépendants (revenus 2024)")
csg_sal = m.T_CSG_ACT * m.F_SAL * x.sal.sum()
p(f"CSG reconstituée sur les salaires (hors gérants, chômage, étranger) : {csg_sal:.1f} Md€ ;"
  " CCSS 2024 secteur privé + public : 92,0 Md€ (+ 4,0 « agricoles et autres »)")
p(f"Salaires bruts reconstitués (assiette CSG / 0,9825) : {m.F_SAL * x.sal.sum() / 0.9825:.0f} Md€ ;"
  " Eurostat D11 reçus par les ménages 2024 : 1 137 Md€ (inclut les non-déclarants et les"
  " salaires de source étrangère)")
p(f"Pensions brutes reconstituées : {m.F_PENS * x.pens.sum():.0f} Md€ ; Eurostat ESSPROS 2023,"
  " pensions de vieillesse, de survie et d'invalidité : 412 Md€ (2023)")
p(f"Parts moyennes calées pour la CSG des pensions : {x.attrs['parts']:.2f} (cible CCSS 25,4 Md€)")
p(f"Cible IR + CSG : {x.charge.sum():.1f} Md€ ; assiette {x.assiette.sum():.0f} Md€ ;"
  f" dont revenus au barème hors salaires et pensions (indépendants, foncier) {m.F_AUT * x.ind.sum():.0f} Md€ ;"
  f" revenus au PFU hors champ {x.capital.sum():.0f} Md€, IR imputé {x.ir_autres.sum():.1f} Md€")

# ------------------------------------------------------------------ 2. sensibilité
p("\n=== 2. Sensibilité (barème E : 0 % / 14 k€ / t / 120 k€ / 40 % / 250 k€ / 49 %)")
p("scénario | cible Md€ | assiette Md€ | taux A | taux t de E | Kakwani actuel | Kakwani E | Lorenz E domine (écart min, ‰) | hausse max (pts)")


def fE(t):
    return [0, 14e3, 120e3, 250e3], [0.0, t, 0.40, 0.49]


for indep, split, forme, npts in [("mixte", None, "puissance", 60), ("prorata", None, "puissance", 60),
                                  ("haut", None, "puissance", 60),
                                  ("mixte", "prorata", "puissance", 60), ("mixte", None, "uniforme", 60),
                                  ("mixte", None, "puissance", 20), ("mixte", None, "puissance", 200)]:
    xs, fs = m.distribution(npts=npts, split=split, forme=forme, indep=indep)
    cible = xs.charge.sum()
    B = (fs.poids * fs.base).sum() / 1e9
    t = m.calibre(fs, cible, fE, 0.05, 0.39)
    nouv = evalue(xs, fs, *fE(t))
    l0 = np.r_[0, np.cumsum(xs.assiette.values - xs.charge.values) / (xs.assiette.values - xs.charge.values).sum()]
    l1 = np.r_[0, np.cumsum(xs.assiette.values - nouv) / (xs.assiette.values - nouv).sum()]
    h = (100 * (nouv - xs.charge.values) / xs.assiette.values)[:9].max()
    p(f"capital={indep:7s} partage={split or 'PFU':7s} forme={forme:9s} n={npts:3d} | {cible:6.1f} | {B:5.0f} |"
      f" {100 * cible / B:5.2f} | {100 * t:5.2f} | {kak_tranches(xs, xs.charge.values):.3f} | {kak_tranches(xs, nouv):.3f} |"
      f" {'oui' if (l1 - l0).min() >= -1e-4 else 'non'} ({1000 * (l1 - l0).min():+.2f}) | {h:.2f}")

# ------------------------------------------------------------------ 3. balayage
# Critère : le revenu après IR + CSG (assiette − charge, foyers classés par tranche de RFR) doit
# dominer au sens de Lorenz celui d'aujourd'hui : alors aucun indice d'inégalité cohérent avec
# Lorenz (Gini, Atkinson, Theil…) ne peut conclure que la réforme redistribue moins.
# Parmi ces barèmes : celui où le taux unique couvre le plus de foyers, puis la perte maximale la
# plus faible pour les tranches de 15 000 à 50 000 € de RFR.
def lorenz(v, pop):
    return np.r_[0, np.cumsum(v) / v.sum()]


def domine(xs, nouv):
    pop = xs.foyers.values
    l0 = lorenz(xs.assiette.values - xs.charge.values, pop)
    l1 = lorenz(xs.assiette.values - nouv, pop)
    return bool(np.all(l1 >= l0 - 1e-4)), float((l1 - l0).min())


p("\n=== 3. Barèmes franchise F + taux unique t jusqu'à S1 + T1 jusqu'à 250 k€ + 49 % : revenu après"
  " impôt dominant au sens de Lorenz, hausse ≤ 2 points de revenu brut dans chaque tranche ; taux unique"
  " pour le plus de foyers")
TABLES = {}
for indep, split in [("mixte", None), ("mixte", "prorata"), ("prorata", None), ("haut", None)]:
    xs, fs = m.distribution(split=split, indep=indep)
    cible, k0 = xs.charge.sum(), kak_tranches(xs, xs.charge.values)
    res = []
    for F, S1, T1 in itertools.product([8e3, 10e3, 12e3, 14e3, 16e3, 18e3, 20e3],
                                       [60e3, 75e3, 90e3, 105e3, 120e3, 150e3, 200e3], [0.40, 0.45]):
        fab = lambda t: ([0, F, S1, 250e3], [0.0, t, T1, 0.49])  # noqa: E731
        t = m.calibre(fs, cible, fab, 0.02, 0.34)
        if t >= T1:
            continue
        nouv = evalue(xs, fs, *fab(t))
        ok, ecart = domine(xs, nouv)
        d = 1e9 * (nouv - xs.charge.values) / xs.foyers.values
        dpct = 100 * (nouv - xs.charge.values) / xs.assiette.values      # en points de revenu brut
        part = fs.poids[(fs.base > F) & (fs.base <= S1)].sum() / fs.poids.sum()
        res.append(dict(F=F / 1e3, S1=S1 / 1e3, T1=T1, t=round(100 * t, 1), K=round(kak_tranches(xs, nouv), 3),
                        lorenz=ok, part=round(100 * part), hausse_max_pts=round(dpct[:9].max(), 2),
                        hausse_max_eur=round(d[:9].max()), perte_15_50k=round(d[3:6].max()),
                        perte_100_250k=round(d[7:9].max())))
    r = pd.DataFrame(res)
    TABLES[(indep, split)] = r
    # « pas massif » : aucune tranche de RFR ne voit sa charge augmenter de plus de 2 points de revenu brut
    ok = r[r.lorenz & (r.hausse_max_pts <= 2.0)].sort_values(["part", "S1", "hausse_max_pts"],
                                                               ascending=[False, False, True])
    p(f"\n-- indépendants={indep}, partage={split or 'PFU'} : Kakwani actuel {k0:.3f} ;"
      f" {len(ok)} barèmes dominants sur {len(r)}")
    p(ok.head(8).to_string(index=False))

OUT.write_text("\n".join(lignes) + "\n", encoding="utf-8")
