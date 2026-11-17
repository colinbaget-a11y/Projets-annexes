"""Figure g10b_loyers_taux (annexe du bloc foncier, v4) : prix et loyers des logements, taux long.

Lancer depuis fiscalite/ après foncier4_calculs.py : python3 note8p/calculs/foncier4_figures.py
Deux panneaux (une seule échelle chacun) : indices des prix des logements anciens et des loyers (1998 = 100) ;
taux de l'emprunt d'État à 10 ans. Données : note8p/sorties/foncier4_taux_loyers.csv.
"""
import sys
from pathlib import Path

import pandas as pd

ICI = Path(__file__).resolve().parent
sys.path.insert(0, str(ICI.parent))
from charte import *  # noqa: E402,F401,F403
from charte import _fr  # noqa: E402

t = pd.read_csv(ICI.parent / "sorties/foncier4_taux_loyers.csv", index_col=0).loc[1998:2025]
prix, loy = 100 * t.prix / t.prix[1998], 100 * t.loyers / t.loyers[1998]
fig, (a1, a2) = plt.subplots(1, 2, figsize=(PLEINE, 2.3), gridspec_kw=dict(width_ratios=[1.25, 1], wspace=0.3))
a1.plot(t.index, prix, color=PROP)
a1.plot(t.index, loy, color=AUJ)
a1.text(2025.4, prix[2025], f"prix\n{_fr(prix[2025])}", color=ENCRE2, fontsize=7, va="center")
a1.text(2025.4, loy[2025], f"loyers\n{_fr(loy[2025])}", color=ENCRE2, fontsize=7, va="center")
a1.set_xlim(1997, 2030)
a1.set_xticks([2000, 2005, 2010, 2015, 2020, 2025])
a1.set_ylim(80, 340)
a1.set_ylabel("indice, 1998 = 100", color=ENCRE2)
axes(a1)
a2.plot(t.index, t.oat10, color=HAUSSE)
for y, dx, dy in ((1998, 4, -11), (2020, 0, -11), (2025, 0, 6)):
    a2.annotate(f"{_fr(t.oat10[y], 1)} %", (y, t.oat10[y]), xytext=(dx, dy), textcoords="offset points",
                ha="center", fontsize=7, color=ENCRE2)
a2.axhline(0, color=GRILLE, lw=0.8)
a2.set_xlim(1997, 2027)
a2.set_ylim(-0.8, 6)
a2.yaxis.set_major_formatter(pct)
a2.set_ylabel("taux de l'emprunt d'État à 10 ans", color=ENCRE2)
axes(a2)
sauver(fig, "g10b_loyers_taux",
       "Insee, indices Notaires-Insee des prix des logements anciens (France métropolitaine) et indice des prix à la"
       " consommation, loyers effectivement payés (lvt/donnees/indices.csv) ; BCE, taux long de convergence de la"
       " France (moyenne annuelle) ; note8p/calculs/foncier4_calculs.py.",
       "Le rapport loyers / prix a été divisé par deux entre 1998 et 2025. L'indice des loyers suit des logements"
       " de qualité constante, baux en cours compris : il sous-estime la hausse des loyers de relocation dans les"
       " zones tendues.")
print("figure écrite : g10b_loyers_taux")
