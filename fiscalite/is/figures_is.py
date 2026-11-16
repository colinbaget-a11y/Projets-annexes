"""Figure de la note IS : coût annuel de la déduction immédiate des équipements et ressources possibles.

Lancer depuis fiscalite/ : python3 is/figures_is.py ; FIG_NU=1 python3 is/figures_is.py
"""
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE), str(HERE.parent)]
import simulation_is as sim  # noqa: E402
from graphiques import ECH_TXT, INK, INK2, fin, grille, plt  # noqa: E402

# Réglages propres à cette figure (la charte graphiques.py sert aussi au cours et n'est pas modifiée) :
# TXT donne 8 pt imprimés en mode nu ; palette validée (dataviz/validate_palette.js, mode clair, toutes paires).
TXT = 10.3
plt.rcParams.update({k: TXT * ECH_TXT for k in ("xtick.labelsize", "ytick.labelsize", "axes.labelsize",
                                                 "legend.fontsize")})
BLEU, OCRE, BRIQUE = "#1d4ba6", "#c79100", "#993333"

N = 20
ans = sim.AN1 + np.arange(N)
fig, ax = plt.subplots(figsize=(10.4, 4.1))
# Ressources : deux plages en aplat clair, chacune nommée dans sa bande, à droite.
cr = (1 + sim.G) ** np.arange(N)
for bas, haut, col, a, nom in ((sim.ELARG_PRUDENT, sum(sim.ELARG.values()), OCRE, 0.30,
                                "Financement par l'assiette"),
                               (sim.recette_taux(3, 1.5), sim.recette_taux(3, 0), BRIQUE, 0.17,
                                "Financement par le taux (28 %)")):
    ax.fill_between(ans, bas * cr, haut * cr, color=col, alpha=a, lw=0, zorder=1)
    for v in (bas, haut):
        ax.plot(ans, v * cr, color=col, lw=0.6, alpha=0.8, zorder=1)
    ax.text(ans[-1] - 0.3, (bas + haut) / 2 * cr[-2], nom, ha="right", va="center", fontsize=TXT, color=INK,
            zorder=6)
# Coûts : ligne centrale et bande (régime actuel dégressif ou linéaire) ; la proposition au premier plan.
for nom, f, col, lw, z in (("100", lambda t: 1.0, INK2, 1.5, 3),
                           ("prop", lambda t: 0.5 if t < 6 else 1.0, BLEU, 2.1, 4)):
    lin = sim.chemin("lineaire", f, 0.75)[:N]
    deg = sim.chemin("degressif", f, 0.75)[:N]
    ax.fill_between(ans, deg, lin, color=col, alpha=0.18, lw=0, zorder=z)
    ax.plot(ans, (lin + deg) / 2, color=col, lw=lw, zorder=z + 0.5, solid_capstyle="round")
    if nom == "100":
        ax.annotate("Coût : déduction immédiate de 100 % dès 2027", (ans[0], (lin[0] + deg[0]) / 2), xytext=(9, 12),
                    textcoords="offset points", ha="left", va="bottom", fontsize=TXT, color=INK, zorder=6)
    else:
        ax.annotate("Coût de la proposition :\n50 % de 2027 à 2032, 100 % ensuite", (ans[6], lin[6]), xytext=(0, 9),
                    textcoords="offset points", ha="center", va="bottom", fontsize=TXT, color=INK, zorder=6,
                    linespacing=1.1)
ax.set_xlim(ans[0], ans[-1])
ax.set_ylim(0, 18)
ax.set_yticks(range(0, 17, 4))
ax.set_xticks(ans[::2])
ax.set_ylabel("Md€ par an")
grille(ax)
fin(fig, "is_01_cout_deduction",
    "Insee, comptes nationaux 2025 (tableau 8.212) ; DGFiP Statistiques n° 21 ; CPO (2025) ; calculs de l'auteur "
    "(fiscalite/is/simulation_is.py).",
    "Note : coût annuel pour l'État, hors intérêts, d'une déduction immédiate des machines, équipements et matériels informatiques des "
    "sociétés non financières (84 Md€ en 2025, hors matériels de transport), à partir de 2027, croissance "
    "nominale de 3 % par an, 75 % de cet investissement fait par des sociétés imposables (hypothèse). Bande de "
    "chaque coût : régime actuel supposé dégressif (bas) ou linéaire sur sept ans (haut). Sans investissement "
    "supplémentaire suscité par la mesure. Ressources, en euros de 2027 puis en hausse de 3 % par an : "
    "élargissement de l'assiette, 3,5 à 4,6 Md€ (fin du taux réduit de 15 %, CIR apprécié au niveau du groupe, "
    "fin des exonérations zonées d'IR et d'IS hors outre-mer, avantage de la boîte à brevets réduit de moitié) ; "
    "taux à 28 %, 4,6 à 8,0 Md€ selon la réaction des bénéfices déclarés (0 à 1,5 % de base en moins par point "
    "de taux). Le taux réduit et la hausse de taux sont chiffrés sur les bénéfices de 2022, portés en 2027 par "
    "la croissance du bénéfice fiscal (+1 %, 0 % et +1 % de 2023 à 2025 selon les Voies et moyens ; +2 % par an "
    "en 2026 et 2027, hypothèse).")
