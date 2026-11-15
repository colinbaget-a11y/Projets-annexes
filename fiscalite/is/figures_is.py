"""Figure de la note IS : coût annuel de la déduction immédiate des équipements et ressources possibles.

Lancer depuis fiscalite/ : python3 is/figures_is.py ; FIG_NU=1 python3 is/figures_is.py
"""
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE), str(HERE.parent)]
import simulation_is as sim  # noqa: E402
from graphiques import INK, fin, grille, plt  # noqa: E402

N = 20
ans = sim.AN1 + np.arange(N)
fig, ax = plt.subplots(figsize=(8.6, 3.9))
for nom, b, col in (("Déduction immédiate de 100 %", 1.0, "#003399"),
                    ("Déduction immédiate de 50 %, reste amorti", 0.5, "#1f7a4d")):
    lin = sim.chemin("lineaire", lambda t, b=b: b, 0.75)[:N]
    deg = sim.chemin("degressif", lambda t, b=b: b, 0.75)[:N]
    ax.fill_between(ans, deg, lin, color=col, alpha=0.25, lw=0)
    ax.plot(ans, (lin + deg) / 2, color=col, lw=2.0, label=nom)
cr = (1 + sim.G) ** np.arange(N)
ax.fill_between(ans, sim.ELARG_PRUDENT * cr, sum(sim.ELARG.values()) * cr, color="#c79100", alpha=0.45, lw=0,
                label="Élargissement de l'assiette (taux réduit, CIR, zones, brevets)")
r3 = [sim.recette_taux(3, e) for e in (1.5, 0)]
ax.fill_between(ans, r3[0] * cr, r3[1] * cr, facecolor="none", edgecolor="#993333", hatch="///", lw=0.8,
                label="Hausse du taux normal de 25 à 28 %")
ax.set_xlim(ans[0], ans[-1])
ax.set_ylim(0, 19.5)
ax.set_xticks(ans[::2])
ax.set_ylabel("Md€ par an")
grille(ax)
ax.legend(fontsize=7.8, loc="upper right", frameon=True)
fin(fig, "is_01_cout_deduction",
    "Insee, comptes nationaux 2025 (tableau 8.212) ; DGFiP Statistiques n° 21 ; CPO (2025) ; calculs de l'auteur "
    "(fiscalite/is/simulation_is.py).",
    "Note : coût pour l'État d'une déduction immédiate des machines, équipements et matériels informatiques des "
    "sociétés non financières (84 Md€ en 2025, hors matériels de transport), à partir de 2027, croissance "
    "nominale de 3 % par an, 75 % de cet investissement fait par des sociétés imposables (hypothèse). Bande : "
    "régime actuel supposé dégressif (bas) ou linéaire sur sept ans (haut). Sans investissement supplémentaire "
    "suscité par la mesure. Élargissement : 3,5 à 4,4 Md€ par an (fin du taux réduit de 15 %, CIR apprécié au "
    "niveau du groupe, fin des exonérations zonées hors outre-mer, avantage de la boîte à brevets réduit de "
    "moitié). Taux à 28 % : 4,4 à 7,5 Md€ selon la réaction des bénéfices déclarés (0 à 1,5 % de base en moins "
    "par point de taux). Le taux réduit et la hausse de taux sont chiffrés sur les bénéfices de 2022, sans croissance jusqu'en 2027 : ils sont plutôt sous-estimés.")
