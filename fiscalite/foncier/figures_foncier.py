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
       "N4": dict(color="#0072B2", lw=2.2, ls="-", marker="D", ms=3.5,
                  label="Proposition : DMTO −50 %, deux taux par commune, taux national sur le terrain"),
       "K4": dict(color="#CC79A7", lw=2.0, ls="-.", marker="^", ms=3.5,
                  label="DMTO −50 %, deux taux nationaux en valeur de marché")}
SCEN = {"R50": sm.report_tf(0.5), "N4": sm.deux_taux_local_national(0.5, 4), "K4": sm.deux_taux(0.5, 4)}
dec = L.groupby("dec_prix").pm2.median()
xt = [f"{u/1e3:.1f}".replace(".", ",") for u in dec]


def f1():
    """Taxe foncière / valeur des logements, par décile de prix au m²."""
    fig, ax = plt.subplots(figsize=(8.6, 4.0))
    w = L.n * L.v
    x = np.arange(10)
    for cle in ("auj", "R50", "N4", "K4"):
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
        "constante, sans réaction des ventes. « Deux taux » : taux sur le terrain égal à quatre fois le taux sur le "
        "bâti. Proposition : chaque commune garde sa recette, répartie selon les deux taux, et un taux national de "
        "0,19 % sur la valeur des terrains remplace les droits perdus. Taxe actuelle : rapport taxe/valeur de 2017 "
        "vieilli selon la croissance de la taxe foncière de chaque commune de 2017 à 2024.")


def f2():
    """Variation par logement et par an : taxe foncière seule, et taxe foncière moins la baisse des DMTO."""
    fig, axs = plt.subplots(1, 2, figsize=(9.4, 3.9), sharey=True)
    x = np.arange(10)
    for k, cle in enumerate(("R50", "N4", "K4")):
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


def f3():
    """Inventaire des prélèvements sur l'immobilier (2024) et comparaison OCDE."""
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(9.4, 3.6), gridspec_kw=dict(width_ratios=[1.35, 1]))
    fam = [("Détention", [("Taxe foncière bâtie", 42.0), ("Ordures ménagères", 9.0), ("CFE", 8.0),
                          ("Autres", 3.9 + 2.7 + 1.3 + 1.1 + 1.0)]),
           ("Transactions", [("Droits de mutation", 14.1), ("TVA du neuf", 7.1), ("Plus-values", 2.8),
                             ("Autres", 1.0)]),
           ("Transmissions", [("Successions, part immobilière", 12.5)]),
           ("Revenus locatifs", [("IR, IS, prél. sociaux", 8.4)]),
           ("Construction", [("Taxe d'aménagement", 1.5)])]
    cols = ["#003399", "#5b7fc4", "#9db1dd", "#d4ddf0"]
    for i, (nom, parts) in enumerate(fam):
        g = 0.0
        for j, (lab, v) in enumerate(parts):
            a1.barh(i, v, left=g, color=cols[j], edgecolor="white", lw=0.6)
            court = {"Taxe foncière bâtie": "Taxe foncière bâtie", "Ordures ménagères": "TEOM", "CFE": "CFE",
                     "Droits de mutation": "DMTO", "TVA du neuf": "TVA"}.get(lab)
            if court and len(parts) > 1:
                a1.text(g + v / 2, i, court, ha="center", va="center", fontsize=7,
                        color="white" if j < 2 else INK)
            g += v
        a1.text(g + 0.8, i, f"{g:.0f}".replace(".", ","), va="center", fontsize=8, color=INK)
    a1.set_yticks(range(len(fam)))
    a1.set_yticklabels([f[0] for f in fam], fontsize=8.5)
    a1.invert_yaxis()
    a1.set_xlabel("Md€ (2024)")
    a1.set_title("Prélèvements assis sur l'immobilier, environ 116 Md€", fontsize=9.5, color=INK, loc="left")
    grille(a1, "x")
    x = np.arange(2)
    a2.bar(x - 0.18, [1.90, 0.72], width=0.34, color="#003399", label="France (2023)")
    a2.bar(x + 0.18, [0.95, 0.37], width=0.34, color="#c79100", label="Moyenne OCDE (2023)")
    for xi, (f_, o_) in enumerate([(1.90, 0.95), (0.72, 0.37)]):
        a2.text(xi - 0.18, f_ + 0.04, f"{f_:.2f}".replace(".", ","), ha="center", fontsize=8)
        a2.text(xi + 0.18, o_ + 0.04, f"{o_:.2f}".replace(".", ","), ha="center", fontsize=8)
    a2.set_xticks(x)
    a2.set_xticklabels(["Impôts périodiques\nsur l'immobilier", "Impôts sur les\ntransactions"], fontsize=8.5)
    a2.yaxis.set_major_formatter(PCT)
    a2.set_title("En % du PIB (OCDE, 4100 et 4400)", fontsize=9.5, color=INK, loc="left")
    a2.legend(fontsize=7.6, loc="upper right")
    grille(a2)
    fin(fig, "fon_03_inventaire",
        "DGCL-DGFiP, note REI 2025 ; OFGL ; SDES, compte du logement 2025 ; DGFiP Statistiques n° 43 ; OCDE, "
        "Revenue Statistics ; calculs de l'auteur.",
        "Note : rendements 2024 (OCDE : 2023), périmètres hétérogènes ; part immobilière des droits de succession estimée à 60 % "
        "(clé du CPO, pas de ventilation officielle). Transactions : droits de mutation, TVA du neuf et des terrains, "
        "plus-values immobilières, contribution de sécurité immobilière. « Autres » de la détention : taxes d'habitation restantes, "
        "IFI, taxe sur le foncier non bâti, taxe sur les bureaux d'Île-de-France, GEMAPI et taxes spéciales "
        "d'équipement. La catégorie 4100 de l'OCDE comprend la taxe d'ordures ménagères et exclut la CFE.")


def f4():
    """Primo-accédant : économie de droits à l'achat et coût de la hausse de taxe foncière sur 10 ans."""
    df = sm.primo({"N4": SCEN["N4"]}, lambda *_: None, horizons=(10,))
    df["va10"] = df.eco - df.net10
    fig, ax = plt.subplots(figsize=(9.0, 3.8))
    y = np.arange(len(df))
    ax.barh(y + 0.2, df.eco / 1e3, height=0.38, color="#0072B2", label="Baisse des droits payés à l'achat")
    ax.barh(y - 0.2, -df.va10 / 1e3, height=0.38, color="#E69F00",
            label="Variation de taxe foncière sur 10 ans, valeur actuelle à 3 % (− : hausse)")
    ax.axvline(0, color=INK, lw=0.7)
    ax.set_yticks(y)
    ax.set_yticklabels(df.cas, fontsize=8)
    ax.invert_yaxis()
    ax.set_xlabel("milliers d'euros (+ : gain pour l'acheteur)")
    grille(ax, "x")
    ax.legend(fontsize=7.6, loc="lower center", bbox_to_anchor=(0.5, 1.0), ncol=2, frameon=False)
    fin(fig, "fon_04_primo", SRC,
        "Note : logement médian de la commune (prix médian au m² × surface médiane des ventes 2023-2024). "
        "Proposition : droits de mutation divisés par deux, taxe foncière à deux taux (terrain = 4 × bâti) avec "
        "recette constante par commune et taux national de 0,19 % sur la valeur des terrains (sans réaction des ventes). Sans effet sur les "
        "prix ; si la hausse de taxe foncière est capitalisée, le prix d'achat baisse d'autant.")


if __name__ == "__main__":
    f1()
    f2()
    f3()
    f4()
