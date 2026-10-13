"""
Figures du brief sur la taxe sur la valeur foncière (LVT), sur données françaises.

Données : lvt/donnees/ (voir extract_lvt.py). Charte et sorties : celles de graphiques.py.

    FIG_NU=1 python lvt/graphiques_lvt.py
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from graphiques import (BLEU, GRIS, HALO, INK2, MUTED, NU, OCRE, VERT, fin, grille,  # noqa: E402
                        panneau, plt, titre)
from matplotlib.ticker import FuncFormatter, NullFormatter  # noqa: E402

D = Path(__file__).resolve().parent / "donnees"
BRIQUE = "#993333"
PCT0 = FuncFormatter(lambda v, _: f"{v:.0f} %")
PCT1 = FuncFormatter(lambda v, _: f"{v:.1f} %".replace(".", ","))
EUR = FuncFormatter(lambda v, _: f"{v:,.0f}".replace(",", " "))

pat = pd.read_csv(D / "patrimoine.csv", index_col=0)
dep = pd.read_csv(D / "dep2024.csv", dtype={"dep": str}).set_index("dep")
tvp = pd.read_csv(D / "tf_vs_prix.csv", dtype={"com": str})
bins = pd.read_csv(D / "tf_vs_prix_bins.csv")

def nb(x, d=0):
    """Nombre à la française : espace pour les milliers, virgule décimale."""
    return f"{x:,.{d}f}".replace(",", " ").replace(".", ",")


def sup(fig, t):
    """Titre d'une figure à deux panneaux (non dessiné en mode nu : il devient la légende)."""
    if not NU:
        fig.suptitle(t, x=0.005, ha="left", fontsize=12.5, y=1.07, fontweight="bold")


NOMS = {"19": "Corrèze", "23": "Creuse", "36": "Indre", "58": "Nièvre", "15": "Cantal",
        "74": "Haute-Savoie", "06": "Alpes-Maritimes", "13": "Bouches-du-Rhône",
        "69": "Rhône", "94": "Val-de-Marne", "93": "Seine-Saint-Denis", "33": "Gironde",
        "35": "Ille-et-Vilaine", "59": "Nord", "31": "Haute-Garonne", "78": "Yvelines",
        "62": "Pas-de-Calais", "38": "Isère", "44": "Loire-Atlantique", "95": "Val-d'Oise"}


# ---------------------------------------------------------------- 1. le retour de la terre
def foncier_pib():
    p = pat.copy()
    fig, (a, b) = plt.subplots(1, 2, figsize=(10.5, 4.3), gridspec_kw={"wspace": 0.32})
    x = p.index
    a.plot(x, 100 * p.terrains_batis * 1000 / p.pib, color=BLEU, lw=2.2)
    a.plot(x, 100 * p.logements * 1000 / p.pib, color=GRIS, lw=1.8)
    a.text(1979, 18, "Terrains sous les bâtiments", color=BLEU, fontsize=9.5, path_effects=HALO)
    a.text(1979, 168, "Logements (bâti seul)", color=GRIS, fontsize=9.5, path_effects=HALO)
    a.yaxis.set_major_formatter(PCT0)
    a.set_ylim(0, 300)
    panneau(a, "Valeur de fin d'année, en % du PIB")
    grille(a)
    part = 100 * p.terrains_batis_men / (p.terrains_batis_men + p.logements_men)
    b.plot(x, part, color=OCRE, lw=2.2)
    for an in (1998, 2007, 2024):
        b.annotate(f"{part[an]:.0f} %", (an, part[an]), xytext=(0, 7), textcoords="offset points",
                   ha="center", fontsize=9, color=INK2, path_effects=HALO)
        b.plot(an, part[an], "o", color=OCRE, ms=4)
    b.yaxis.set_major_formatter(PCT0)
    b.set_ylim(0, 65)
    panneau(b, "Part du terrain dans la valeur des logements\ndétenus par les ménages")
    grille(b)
    for ax in (a, b):
        ax.set_xlim(1977, 2025)
    sup(fig, "La valeur du foncier bâti a été multipliée par neuf depuis la fin des années 1990")
    fin(fig, "lvt_foncier_pib.png",
        "Source : Insee, comptes de patrimoine annuels en base 2020 (tableaux 8.201 et 8.210, "
        "lignes « terrains supportant des bâtiments » et « logements », valeurs nettes de fin "
        "d'année), PIB à prix courants ; calculs de l'auteur.",
        "Lecture : fin 2024, les terrains sous les bâtiments valent 229 % du PIB pour l'ensemble de "
        "l'économie ; pour les ménages, le terrain représente 45 % de la valeur cumulée terrain + "
        "logement. La valeur du terrain est un résidu : valeur de marché de l'immobilier moins "
        "valeur de remplacement du bâti, de sorte que toute plus-value immobilière lui est imputée.")


# ---------------------------------------------------------------- 2. dispersion géographique
def prix_terrains():
    d = dep.sort_values("pm2_terrain").reset_index()
    fig, (a, b) = plt.subplots(1, 2, figsize=(10.5, 4.5), gridspec_kw={"wspace": 0.3})
    a.scatter(range(len(d)), d.pm2_terrain, s=14, color=BLEU, zorder=3)
    a.set_yscale("log")
    a.set_yticks([10, 20, 50, 100, 200, 500, 1000])
    a.yaxis.set_major_formatter(EUR)
    a.yaxis.set_minor_formatter(NullFormatter())
    a.set_xticks([])
    a.set_xlabel("Départements, du moins cher au plus cher")
    for code in ("19", "36", "35", "33", "74", "13", "94"):
        i = d.index[d.dep == code][0]
        a.annotate(NOMS[code], (i, d.pm2_terrain[i]), xytext=(-6, 4), textcoords="offset points",
                   ha="right", fontsize=8.5, color=INK2, path_effects=HALO)
    panneau(a, "Prix médian d'un terrain à bâtir, en €/m²")
    grille(a)
    b.scatter(d.pm2_terrain, 100 * d.part_terrain, s=14, color=OCRE, zorder=3)
    b.set_xscale("log")
    b.set_xticks([20, 50, 100, 200, 500])
    b.xaxis.set_major_formatter(EUR)
    b.xaxis.set_minor_formatter(NullFormatter())
    b.yaxis.set_major_formatter(PCT0)
    b.set_ylim(0, 80)
    b.set_xlabel("Prix médian d'un terrain à bâtir, en €/m² (échelle log)")
    for code, dx, ha in (("19", 6, "left"), ("74", -6, "right"), ("93", -6, "right"),
                         ("59", 6, "left"), ("06", 6, "left")):
        r = d[d.dep == code].iloc[0]
        b.annotate(NOMS[code], (r.pm2_terrain, 100 * r.part_terrain), xytext=(dx, 0),
                   textcoords="offset points", ha=ha, va="center", fontsize=8.5, color=INK2,
                   path_effects=HALO)
    panneau(b, "Part estimée du terrain dans le prix\nd'une maison médiane")
    grille(b)
    sup(fig, "Le prix du terrain varie d'un facteur 45 entre départements")
    fin(fig, "lvt_prix_terrains.png",
        "Source : DGFiP, Demandes de valeurs foncières (DVF) 2024, version géolocalisée Etalab ; "
        "calculs de l'auteur. Terrains à bâtir : ventes dont toutes les parcelles sont classées "
        "« terrain à bâtir » au cadastre, sans local, de 100 à 5 000 m² (27 353 ventes). Maisons : "
        "ventes d'une seule maison sans autre logement ni local d'activité (304 799 ventes).",
        "Lecture : départements comptant au moins 30 ventes de terrains à bâtir ; l'Alsace-Moselle "
        "(livre foncier) est absente de DVF, Paris et les Hauts-de-Seine n'ont presque pas de "
        "terrains nus vendus. La part du terrain est le prix médian du m² de terrain multiplié par "
        "la surface médiane de parcelle des maisons vendues, rapporté au prix médian de ces "
        "maisons : un ordre de grandeur, pas une mesure.")


# ---------------------------------------------------------------- 3. la taxe foncière actuelle
def tf_regressive():
    lo, hi = bins.iloc[0], bins.iloc[-1]
    fig, ax = plt.subplots(figsize=(7.2, 4.3))
    ax.fill_between(bins.pm2, bins.tf25, bins.tf75, color=BLEU, alpha=0.13, lw=0)
    ax.plot(bins.pm2, bins.tf, color=BLEU, lw=2.2, marker="o", ms=3.5)
    ax.set_xscale("log")
    ax.set_xticks([1000, 1500, 2000, 3000, 4000, 6000])
    ax.xaxis.set_major_formatter(EUR)
    ax.xaxis.set_minor_formatter(NullFormatter())
    ax.yaxis.set_major_formatter(PCT1)
    ax.set_ylim(0, 0.75)
    ax.set_xlabel("Prix médian au m² des logements vendus dans la commune en 2024, en € (échelle log)")
    grille(ax)
    titre(ax, "Plus le logement est cher, plus la taxe foncière pèse peu sur sa valeur",
          "Taxe foncière sur les logements rapportée à leur valeur de marché, médiane par "
          "vingtième de communes")
    fin(fig, "lvt_tf_regressive.png",
        "Sources : Insee, André et Meslin (2023), Insee Analyses n° 91, données de la figure 5a "
        "(taxe foncière 2017 / valeur de marché estimée, par commune) ; DGFiP, DVF 2024 (prix médian "
        "au m² des ventes d'un seul logement) ; calculs de l'auteur sur les "
        + nb(len(tvp)) + " communes comptant au moins 20 ventes.",
        f"Lecture : dans les 5 % de communes les moins chères (prix médian {nb(lo.pm2)} €/m²), la "
        f"taxe foncière représente en médiane {nb(lo.tf, 2)} % de la valeur des logements chaque "
        f"année ; dans les 5 % les plus chères ({nb(round(hi.pm2, -2))} €/m²), {nb(hi.tf, 2)} %."
        " Dans chaque vingtième, la moitié des communes se "
        "situe dans la bande claire. La taxe date de 2017 et les prix de 2024 : on suppose que le "
        "classement des communes par prix a peu changé entre les deux dates.")


# ---------------------------------------------------------------- 4. capitalisation
def capitalisation():
    t = np.linspace(0, 3, 301)
    fig, ax = plt.subplots(figsize=(7.2, 4.3))
    for r, c in ((2, BRIQUE), (3, BLEU), (5, VERT)):
        y = 100 * r / (r + t)
        ax.plot(t, y, color=c, lw=2)
        ax.text(3.03, y[-1], f"r = {r} %", color=c, fontsize=9, va="center", path_effects=HALO)
    for tx, lab in ((0.7, "0,7 %"), (1.0, "1 %")):
        ax.axvline(tx, color=GRIS, lw=0.8, ls="--")
        ax.text(tx + 0.03, 101, lab, fontsize=8.5, color=MUTED, va="bottom")
    ax.set_xlim(0, 3.4)
    ax.set_ylim(35, 105)
    ax.set_xticks([0, 0.5, 1, 1.5, 2, 2.5, 3])
    ax.xaxis.set_major_formatter(PCT1)
    ax.yaxis.set_major_formatter(PCT0)
    ax.set_xlabel("Taux annuel de la taxe, en % de la valeur du terrain")
    grille(ax)
    titre(ax, "Une taxe annuelle sur le terrain se lit d'abord dans son prix",
          "Prix du terrain taxé, en % du prix sans taxe, si la taxe est perpétuelle et "
          "entièrement capitalisée")
    fin(fig, "lvt_capitalisation.png",
        "Calcul de l'auteur : un terrain qui rapporte un loyer net R vaut R/r sans taxe et R/(r+t) "
        "avec une taxe annuelle au taux t de sa valeur ; r est le taux d'actualisation réel net de "
        "la croissance attendue des loyers.",
        "Lecture : les deux repères sont les taux qui, appliqués à la valeur des terrains bâtis hors "
        "administrations fin 2024, rapporteraient autant que la taxe foncière sur les propriétés "
        "bâties (0,7 %) ou que celle-ci et les droits de mutation réunis (1 %). Les prix actuels "
        "intègrent déjà ces impôts : une bascule à recette constante ne ferait pas baisser le prix "
        "moyen du terrain de l'ampleur lue sur les courbes, elle déplacerait la charge d'un bien à "
        "l'autre. La capitalisation complète est une hypothèse, que la section 4 confronte aux "
        "données.")


if __name__ == "__main__":
    foncier_pib()
    prix_terrains()
    tf_regressive()
    capitalisation()
