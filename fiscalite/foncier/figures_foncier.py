"""Figures de la note foncière (préfixe fon_).

Lancer depuis fiscalite/ : python3 foncier/figures_foncier.py ; FIG_NU=1 python3 foncier/figures_foncier.py
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE), str(HERE.parent)]
import simulation as sm  # noqa: E402
from graphiques import INK, PCT, fin, grille, plt  # noqa: E402

L = sm.L
SRC = ("DGFiP, REI 2024 et DVF 2023-2024 ; Insee, recensement 2022, comptes de patrimoine et Insee Analyses "
       "n° 91 ; calculs de l'auteur.")
STY = {"auj": dict(color="#1a1a1a", lw=1.6, ls="-", marker="o", ms=3.5, label="Aujourd'hui"),
       "R50": dict(color="#E69F00", lw=2.0, ls="--", marker="s", ms=3.5,
                   label="DMTO −50 %, taxe foncière actuelle relevée"),
       "L4": dict(color="#0072B2", lw=2.2, ls="-", marker="D", ms=3.5,
                  label="DMTO −50 %, deux taux, recette constante par commune"),
       "K4": dict(color="#CC79A7", lw=2.0, ls="-.", marker="^", ms=3.5,
                  label="DMTO −50 %, deux taux nationaux en valeur de marché")}
SCEN = {"R50": sm.report_tf(0.5), "L4": sm.deux_taux_local(0.5, 4), "K4": sm.deux_taux(0.5, 4)}
dec = L.groupby("dec_prix").pm2.median()
xt = [f"{u/1e3:.1f}".replace(".", ",") for u in dec]


def f1():
    """Taxe foncière / valeur des logements, par décile de prix au m²."""
    fig, ax = plt.subplots(figsize=(8.6, 4.0))
    w = L.n * L.v
    x = np.arange(10)
    for cle in ("auj", "R50", "L4", "K4"):
        tf = L.tf0 if cle == "auj" else SCEN[cle][0]
        r = 100 * (L.n * tf).groupby(L.dec_prix).sum() / w.groupby(L.dec_prix).sum()
        ax.plot(x, r.values, **STY[cle])
    ax.set_xticks(x)
    ax.set_xticklabels(xt, fontsize=8)
    ax.set_xlabel("Prix médian au m² du décile de logements (milliers d'euros)")
    ax.yaxis.set_major_formatter(PCT)
    ax.set_ylim(0, 0.75)
    grille(ax)
    ax.legend(loc="upper right", fontsize=7.6)
    fin(fig, "fon_01_tf_valeur", SRC,
        "Note : taxe foncière des logements des particuliers rapportée à leur valeur de marché, par décile de "
        "logements classés selon le prix au m² de leur commune (France métropolitaine hors Alsace-Moselle). Les "
        "trois scénarios remplacent la moitié des droits de mutation (5,7 Md€) par de la taxe foncière, à recette "
        "constante. « Deux taux » : taux sur le terrain égal à quatre fois le taux sur le bâti.")


def f2():
    """Variation par logement et par an : taxe foncière seule, et taxe foncière moins la baisse des DMTO."""
    fig, axs = plt.subplots(1, 2, figsize=(9.4, 3.9), sharey=True)
    x = np.arange(10)
    for k, cle in enumerate(("R50", "L4", "K4")):
        tf1, d1 = SCEN[cle]
        g = L.assign(w=L.n, a=L.n * (tf1 - L.tf0), b=L.n * (tf1 - L.tf0 + d1 - L.d0)).groupby("dec_prix")
        for ax, col in zip(axs, ("a", "b")):
            ax.bar(x + (k - 1) * 0.27, g[col].sum() / g.w.sum(), width=0.26, color=STY[cle]["color"],
                   label=STY[cle]["label"], edgecolor="white", lw=0.3, hatch=["", "", "//"][k])
    for ax, t in zip(axs, ("Taxe foncière", "Taxe foncière et droits de mutation")):
        ax.axhline(0, color=INK, lw=0.7)
        ax.set_xticks(x)
        ax.set_xticklabels(xt, fontsize=7.5)
        ax.set_title(t, fontsize=9.5, color=INK, loc="left")
        ax.set_xlabel("Prix médian au m² du décile (k€)")
        grille(ax)
    axs[0].set_ylabel("€ par logement et par an")
    axs[0].set_ylim(-500, 1900)
    h, lab = axs[0].get_legend_handles_labels()
    fig.legend(h, lab, loc="upper center", ncol=1, fontsize=7.4, frameon=False, bbox_to_anchor=(0.5, 1.13))
    fin(fig, "fon_02_variation", SRC,
        "Note : variation moyenne par logement des particuliers. À droite, la baisse des droits de mutation est "
        "rapportée à l'ensemble du parc de la commune (droits annuels / nombre de logements) : c'est ce que paie "
        "en moyenne chaque année un logement de la commune au fil des ventes.")


if __name__ == "__main__":
    f1()
    f2()
