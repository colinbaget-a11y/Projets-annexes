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
ind = pd.read_csv(D / "indices.csv", index_col=0)
grad = pd.read_csv(D / "gradient_idf.csv")

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


# ---------------------------------------------------------------- 5. ce que mesure le « terrain »
def prix_cout_loyers():
    i = 100 * ind.loc[1998:2025] / ind.loc[1998]
    fig, ax = plt.subplots(figsize=(7.2, 4.3))
    series = (("prix_logements_anciens", BLEU, "Prix des logements anciens"),
              ("cout_construction", OCRE, "Coût de la construction"),
              ("loyers", VERT, "Loyers"),
              ("prix_conso", GRIS, "Prix à la consommation"))
    for col, c, lab in series:
        ax.plot(i.index, i[col], color=c, lw=2.2 if col == "prix_logements_anciens" else 1.8)
        dy = {"loyers": -7, "prix_conso": 7}.get(col, 0)
        ax.annotate(f"{lab} ({nb(i[col].iloc[-1])})", (i.index[-1], i[col].iloc[-1]),
                    xytext=(6, dy), textcoords="offset points", va="center", fontsize=9,
                    color=INK2, path_effects=HALO)
    ax.set_xlim(1997.5, 2025.5)
    ax.set_ylim(80, 320)
    grille(ax)
    titre(ax, "Les prix ont triplé, les loyers ont suivi l'inflation",
          "Indices en moyenne annuelle, base 100 en 1998")
    fin(fig, "lvt_prix_cout_loyers.png",
        "Sources : Insee, indice Notaires-Insee des prix des logements anciens (France "
        "métropolitaine, série brute) ; indice du coût de la construction (ICC) ; indice des prix à "
        "la consommation, base 2015, loyers effectivement payés (04.1.1) et ensemble hors tabac.",
        "Lecture : de 1998 à 2025, le prix des logements anciens a été multiplié par "
        f"{nb(i.prix_logements_anciens.iloc[-1] / 100, 1)}, le coût de la construction par "
        f"{nb(i.cout_construction.iloc[-1] / 100, 1)} et les loyers payés par "
        f"{nb(i.loyers.iloc[-1] / 100, 1)}. L'indice des loyers couvre tout le parc loué, logement "
        "social et baux en cours compris : il progresse moins vite que les loyers de "
        "relocation dans le secteur libre.")


def residu():
    p = pat.loc[1979:2024]
    fig, (a, b) = plt.subplots(1, 2, figsize=(10.5, 4.3), gridspec_kw={"wspace": 0.3})
    a.bar(p.index - 0.2, 100 * p.terrains_batis_men.pct_change().loc[1979:], width=0.4, color=BLEU,
          label="Terrains")
    a.bar(p.index + 0.2, 100 * p.logements_men.pct_change().loc[1979:], width=0.4, color=OCRE,
          label="Logements (bâti)")
    a.axhline(0, color=INK2, lw=0.7)
    a.yaxis.set_major_formatter(PCT0)
    a.legend(loc="upper left")
    panneau(a, "Variation annuelle de la valeur, ménages")
    grille(a)
    tb, lg = pat.terrains_batis_men, pat.logements_men
    tot = tb + lg
    for k, c, ls in ((0.8, VERT, "--"), (1.0, OCRE, "-"), (1.2, BRIQUE, "--")):
        part = 100 * (tot - k * lg) / tot
        b.plot(pat.index, part, color=c, lw=2.0, ls=ls)
        b.annotate(f"bâti × {nb(k, 1)}", (pat.index[-1], part.iloc[-1]), xytext=(6, 0),
                   textcoords="offset points", va="center", fontsize=9, color=INK2,
                   path_effects=HALO)
    b.set_xlim(1977, 2030)
    b.set_ylim(0, 70)
    b.yaxis.set_major_formatter(PCT0)
    panneau(b, "Part du terrain si la valeur du bâti\nest surestimée ou sous-estimée de 20 %")
    grille(b)
    sup(fig, "Le terrain absorbe toutes les fluctuations des prix immobiliers")
    fin(fig, "lvt_residu.png",
        "Source : Insee, comptes de patrimoine annuels en base 2020 (tableau 8.210, ménages) ; "
        "calculs de l'auteur.",
        "Lecture : le terrain étant calculé comme valeur de marché moins valeur du bâti, toute "
        "variation des prix se reporte sur lui : sa valeur a baissé de 8,9 % en 2023 quand celle "
        "du bâti augmentait de 3,0 %. À droite, la valeur totale est tenue pour exacte et seule "
        "l'estimation du bâti varie : une erreur de 20 % sur le bâti déplace la part du terrain "
        "d'environ 10 points.")


def gradient():
    g = grad[grad.km <= 80].copy()
    fig, ax = plt.subplots(figsize=(7.2, 4.3))
    ax.scatter(g.km, g.pm2, s=5, color=BLEU, alpha=0.18, lw=0, zorder=2)
    bords = np.arange(0, 85, 5)
    g["b"] = pd.cut(g.km, bords)
    m = g.groupby("b", observed=True).agg(km=("km", "median"), pm2=("pm2", "median"), n=("pm2", "size"))
    m = m[m.n >= 15]
    ax.plot(m.km, m.pm2, color=BLEU, lw=2.4, marker="o", ms=4, zorder=3)
    ax.set_yscale("log")
    ax.set_yticks([20, 50, 100, 200, 500, 1000, 2000])
    ax.yaxis.set_major_formatter(EUR)
    ax.yaxis.set_minor_formatter(NullFormatter())
    ax.set_ylim(15, 3000)
    ax.set_xlim(0, 82)
    ax.set_xlabel("Distance à vol d'oiseau à Notre-Dame de Paris, en km")
    grille(ax)
    titre(ax, "Le prix du sol est d'abord le prix de la distance",
          "Prix des terrains à bâtir vendus en Île-de-France en 2024, en €/m² (échelle log)")
    fin(fig, "lvt_gradient_idf.png",
        "Source : DGFiP, DVF 2024 géolocalisées (Etalab) ; calculs de l'auteur sur les "
        + nb(len(g)) + " ventes de terrains à bâtir franciliennes situées à moins de 80 km.",
        "Lecture : chaque point est une vente ; la ligne relie les prix médians par tranche de "
        "5 km comptant au moins 15 ventes. Il ne se vend presque pas de terrain nu à moins de "
        "10 km du centre : la valeur du sol y est la plus élevée et la moins observée.")


# ---------------------------------------------------------------- 6. la transition
R_ACT = 0.03   # taux d'actualisation réel net de croissance (Koster et Pinchbeck : 3 à 4 %)


def chemin_prix(r, t1, n, horizon=400):
    """Prix d'un terrain de loyer net 1 quand une taxe ad valorem passe linéairement de 0 à t1
    en n années à partir de l'annonce (année 0). P(k-1) = (1 + (1 - t(k)) P(k)) / (1 + r)."""
    t = np.array([t1 if n == 0 or k >= n else t1 * k / n for k in range(horizon + 1)])
    t[0] = 0
    p = np.empty(horizon + 1)
    p[-1] = 1 / (r + t1)
    for k in range(horizon, 0, -1):
        p[k - 1] = (1 + (1 - t[k]) * p[k]) / (1 + r)
    return p, t


def trajectoire():
    fig, ax = plt.subplots(figsize=(7.2, 4.3))
    p0 = 1 / R_ACT
    ans = np.arange(-3, 31)
    for n, c in ((0, BRIQUE), (10, BLEU), (20, VERT)):
        p, _ = chemin_prix(R_ACT, 0.01, n)
        y = np.r_[np.full(3, 100.0), 100 * p[:31] / p0]
        ax.step(ans, y, where="post", color=c, lw=2)
        lab = "taxe immédiate" if n == 0 else f"montée en charge sur {n} ans"
        yl = {0: 87, 10: 90.5, 20: 94}[n]
        ax.plot([12, 14], [yl, yl], color=c, lw=2)
        ax.text(14.6, yl, f"{lab} : {nb(y[3] - 100, 0)} % à l'annonce", va="center",
                fontsize=9, color=INK2)
    ax.axvline(0, color=GRIS, lw=0.8, ls=":")
    ax.set_xlim(-3, 30)
    ax.set_ylim(70, 103)
    ax.yaxis.set_major_formatter(PCT0)
    ax.set_xlabel("Années depuis l'annonce")
    grille(ax)
    titre(ax, "Étaler la taxe n'étale pas la perte",
          "Prix d'un terrain, en % de son prix avant l'annonce d'une taxe de 1 % de sa valeur")
    fin(fig, "lvt_trajectoire.png",
        "Calcul de l'auteur : taxe annuelle portée linéairement de 0 à 1 % de la valeur du terrain, "
        "capitalisation complète, taux d'actualisation réel net de croissance de 3 %.",
        "Lecture : avec une montée en charge sur dix ans, le prix baisse de 22 % le jour de "
        "l'annonce, contre 25 % si la taxe s'applique tout de suite ; il continue ensuite de "
        "baisser jusqu'à -25 %, mais ceux qui achètent pendant la transition sont compensés par "
        "une taxe encore réduite. La perte non subie à l'annonce correspond exactement aux "
        "recettes auxquelles l'État renonce pendant la montée en charge.")


def biens_types():
    """Effet à l'annonce d'une bascule taxe foncière -> taxe sur le terrain, à recette constante."""
    def med_pond(g):
        g = g.sort_values("tf")
        c = g.n.cumsum()
        return g.tf[c >= c.iloc[-1] / 2].iloc[0]
    t = tvp.assign(dep=tvp.com.str[:2])
    tf_dep = t.groupby("dep").apply(med_pond, include_groups=False)
    theta = 19.2 / pat.terrains_batis_men[2017]          # taux neutre sur le terrain (ménages)
    biens = []
    for code in ("19", "69", "74"):
        r = dep.loc[code]
        biens.append((f"Maison, {NOMS[code]}", r.prix_maison, r.part_terrain, tf_dep[code] / 100))
    # Appartement parisien : hypothèses. Valeur 500 000 € ; terrain 75 % de la valeur (non
    # observé) ; taxe foncière 0,146 % de la valeur = médiane des IRIS parisiens en 2017 (0,096 %,
    # Insee Analyses n° 91, figure 3a) relevée de 52 % (taux communal de 13,5 % à 20,5 % en 2023).
    biens.append(("Appartement, Paris (hyp.)", 500_000, 0.75, 0.00096 * 1.52))
    fig, ax = plt.subplots(figsize=(7.2, 4.3))
    n = np.arange(0, 31)
    cols = (VERT, GRIS, OCRE, BRIQUE)
    lignes = []
    for (nom, v, s, tf), c in zip(biens, cols):
        dt = theta * s * v - tf * v                       # variation de la facture annuelle
        vt = 1 / (1 + R_ACT)
        phi = np.array([1.0 if k == 0 else
                        R_ACT * (sum((j / k) * vt ** j for j in range(1, k + 1)) + vt ** k / R_ACT)
                        for k in n])
        y = -100 * phi * dt / R_ACT / v
        ax.plot(n, y, color=c, lw=2)
        lignes.append((nom, y, c, dt, tf * v))
    for (nom, y, c, dt, f0), dy in zip(lignes, (1.6, 1.6, 2.3, -2.2)):
        ax.text(1, y[1] + dy, f"{nom} : facture de {nb(round(f0, -1))} € à "
                f"{nb(round(f0 + dt, -1))} € par an", fontsize=8.5, color=INK2, va="center",
                path_effects=HALO)
    ax.axhline(0, color=INK2, lw=0.7)
    ax.yaxis.set_major_formatter(PCT0)
    ax.set_xlabel("Durée de la montée en charge, en années (0 : application immédiate)")
    ax.set_xlim(0, 30)
    ax.set_ylim(-13, 31)
    grille(ax)
    titre(ax, "Une transition longue réduit peu les gains et les pertes en capital",
          "Variation du prix du bien à l'annonce d'une bascule vers une taxe sur le terrain, "
          "à recette constante")
    fin(fig, "lvt_biens_types.png",
        "Calcul de l'auteur. Maisons : prix médian, part du terrain et taxe foncière rapportée à la "
        "valeur dans le département (figures précédentes). Appartement parisien : valeur de "
        "500 000 €, part du terrain de 75 % (hypothèse), taxe foncière de 0,15 % de la valeur "
        "(médiane parisienne de 2017 relevée de la hausse de taux de 2023). Taxe sur le terrain "
        f"au taux neutre de {nb(100 * theta, 2)} % ; capitalisation complète à 3 %.",
        "Lecture : les montants indiquent la facture annuelle avant et après la bascule. Si la "
        "nouvelle taxe s'applique en une fois, le prix de la maison corrézienne monte de "
        f"{nb(lignes[0][1][0])} % et celui de l'appartement parisien baisse de "
        f"{nb(-lignes[3][1][0])} % ; avec une montée en charge sur quinze ans, de "
        f"{nb(lignes[0][1][15])} % et {nb(-lignes[3][1][15])} %.")


# ---------------------------------------------------------------- 7. règles de trois
# Élasticités publiées (voir le texte) appliquées à des grandeurs françaises.
SEMI_HOJ = 4.26     # Høj et al. (2018) : -4,26 % de prix par point pour mille de taxe / valeur
SEMI_KP = 100 / 3.7 / 10   # Koster et Pinchbeck (2022) : capitalisation complète à 3,7 %
SEMI_NWY = 100 / 8 / 10    # Nielsson et al. (2024) : borne de l'IC à 95 % (r = 8 %)
DMTO = 4.5 + 1.2 + 0.0237 * 4.5   # droits sur l'ancien hors hausse de 2025, en points


def biens_bascule():
    """Biens types : nom, valeur, variation de la facture annuelle (€) d'une bascule à recette
    constante vers une taxe sur le terrain (mêmes hypothèses que lvt_biens_types)."""
    def med_pond(g):
        g = g.sort_values("tf")
        c = g.n.cumsum()
        return g.tf[c >= c.iloc[-1] / 2].iloc[0]
    t = tvp.assign(dep=tvp.com.str[:2])
    tf_dep = t.groupby("dep").apply(med_pond, include_groups=False)
    theta = 19.2 / pat.terrains_batis_men[2017]
    out = []
    for code in ("19", "69", "74"):
        r = dep.loc[code]
        v = r.prix_maison
        out.append((f"Maison, {NOMS[code]}", v, theta * r.part_terrain * v - tf_dep[code] / 100 * v))
    v = 500_000
    out.append(("Appartement, Paris (hyp.)", v, theta * 0.75 * v - 0.00096 * 1.52 * v))
    return out


def regles_prix():
    b = biens_bascule()
    fig, (a, c) = plt.subplots(1, 2, figsize=(10.5, 4.4), gridspec_kw={"wspace": 0.08})
    y = np.arange(len(b))[::-1]
    for k, (semi, col, lab) in enumerate(((SEMI_HOJ, BLEU, "Danemark, Høj et al. (2018)"),
                                          (SEMI_KP, OCRE, "Angleterre, Koster et Pinchbeck (2022)"),
                                          (SEMI_NWY, VERT, "Danemark, Nielsson et al. (2024) :\nborne de l'intervalle de confiance"))):
        dp = [-semi * 1000 * dt / v for _, v, dt in b]
        a.barh(y + 0.27 * (1 - k), dp, height=0.25, color=col, label=lab)
    a.axvline(0, color=INK2, lw=0.7)
    a.set_yticks(y)
    a.set_yticklabels([n for n, _, _ in b])
    a.xaxis.set_major_formatter(PCT0)
    a.legend(loc="lower right", fontsize=8)
    panneau(a, "Variation du prix du bien")
    grille(a, "x")
    for k, (pt, col, lab) in enumerate(((0.83, BRIQUE, "Allemagne, Löffler et Siegloch (2024) : 83 %"),
                                        (0.50, GRIS, "Californie, Baker (2025) : 50 à 89 %"))):
        vals = [pt * dt for _, _, dt in b]
        c.barh(y + 0.2 * (0.5 - k) * 2, vals, height=0.36, color=col, label=lab,
               xerr=None if k == 0 else [[0] * len(b), [(0.89 - 0.50) * dt if dt > 0 else 0 for _, _, dt in b]],
               error_kw={"ecolor": INK2, "lw": 0.8, "capsize": 2})
    c.axvline(0, color=INK2, lw=0.7)
    c.set_yticks(y)
    c.set_yticklabels([])
    c.xaxis.set_major_formatter(EUR)
    c.legend(loc="upper right", fontsize=8)
    panneau(c, "Variation du loyer annuel si le bien est loué, en €")
    grille(c, "x")
    sup(fig, "Ce que donneraient en France les élasticités mesurées à l'étranger")
    fin(fig, "lvt_regles_prix.png",
        "Calcul de l'auteur. Variation de la taxe annuelle de chaque bien : bascule à recette "
        "constante vers une taxe sur le terrain (figure précédente). Prix : variation de la taxe "
        "rapportée à la valeur du bien, multipliée par la semi-élasticité estimée (4,26 % de prix "
        "par point pour mille chez Høj et al. ; 2,7 % pour une capitalisation complète au taux de "
        "3,7 % de Koster et Pinchbeck ; 1,25 % au plus chez Nielsson et al., dont l'estimation "
        "centrale est nulle). Loyers : part de la variation de taxe répercutée sur le loyer.",
        "Lecture : si l'élasticité de Høj et al. valait en France, l'appartement parisien perdrait "
        f"{nb(SEMI_HOJ * 1000 * b[3][2] / b[3][1])} % de sa valeur ; avec celle de Nielsson et al., "
        "au plus " + nb(SEMI_NWY * 1000 * b[3][2] / b[3][1]) + " %. Les effets danois et anglais "
        "portent sur des variations de taxe de quelques points pour mille ; la baisse de taxe de la "
        "maison corrézienne (8 ‰ de sa valeur) sort de ce domaine.")


def regles_dmto():
    vol = pd.read_csv(D / "volumes.csv", index_col=0)
    n0 = vol.ventes_logements_dvf.dropna().iloc[-1]
    fig, (a, c) = plt.subplots(1, 2, figsize=(10.5, 4.2), gridspec_kw={"wspace": 0.75})
    etudes = (("Allemagne, Fritzsche\net Vandrei (2019)", 7.0, BLEU),
              ("Toronto, Dachis\net al. (2012)", 15 / 1.1, OCRE),
              ("Royaume-Uni, Hilber et\nLyytikäinen (2017), mobilité", 37 / 2, VERT),
              ("France, Bérard et\nTrannoy (2018), après 3 mois", 0.0, BRIQUE))
    y = np.arange(len(etudes))[::-1]
    for yi, (nom, e, col) in zip(y, etudes):
        a.barh(yi, e / 100 * n0 / 1000, color=col, height=0.55)
        a.text(e / 100 * n0 / 1000, yi, f"  +{nb(e, 1)} %" if e else "  aucun effet durable",
               va="center", fontsize=9, color=INK2)
    a.set_yticks(y)
    a.set_yticklabels([e[0] for e in etudes], fontsize=8.5)
    a.set_xlim(0, 1.35 * max(e[1] for e in etudes) / 100 * n0 / 1000)
    a.set_xlabel("milliers de ventes supplémentaires par an")
    panneau(a, "Baisse d'un point des droits de mutation")
    grille(a, "x")
    lin = [(nom.replace("\n", " "), e * DMTO) for nom, e, _ in etudes[:2]]
    noms = ["Fritzsche et Vandrei,\nextrapolation linéaire", "Dachis et al.,\nextrapolation linéaire",
            "Bontemps et al. (2023),\nmodèle estimé sur la France"]
    vals = [lin[0][1], lin[1][1], 21.0]
    cols = (BLEU, OCRE, BRIQUE)
    y2 = np.arange(3)[::-1]
    for yi, v, col, k in zip(y2, vals, cols, range(3)):
        c.barh(yi, v, color=col, height=0.55, hatch="///" if k < 2 else None, edgecolor="white",
               lw=0)
        c.text(v, yi, f"  +{nb(v)} %", va="center", fontsize=9, color=INK2)
    c.set_yticks(y2)
    c.set_yticklabels(noms, fontsize=8.5)
    c.set_xlim(0, 105)
    c.xaxis.set_major_formatter(PCT0)
    panneau(c, "Suppression des droits de mutation :\nvariation du nombre de ventes")
    grille(c, "x")
    sup(fig, "Les droits de mutation : les élasticités les mieux établies, transposées à la France")
    fin(fig, "lvt_regles_dmto.png",
        "Calcul de l'auteur. Base : " + nb(n0) + " ventes comportant au moins un logement recensées "
        "dans DVF en 2024 (hors Alsace-Moselle et Mayotte). Élasticités : -7 % de transactions par "
        "point de droit (Fritzsche et Vandrei) ; -15 % pour un droit de 1,1 % (Dachis et al.) ; "
        "-37 % de déménagements pour 2 points (Hilber et Lyytikäinen, effet sur la mobilité et non "
        "sur les ventes) ; hausse de 0,7 point en 2014 en France : ventes +26 % le mois précédent, "
        "-14 % par mois les trois mois suivants, puis aucun effet (Bérard et Trannoy). Droits sur "
        "l'ancien : " + nb(DMTO, 1) + " points avant la hausse de 2025.",
        "Lecture : à gauche, effet d'une baisse d'un point, proche des variations observées dans les "
        "études ; la seule estimation française ne trouve pas d'effet durable. À droite, les barres hachurées prolongent ces élasticités jusqu'à la suppression des "
        "droits, très au-delà de ce qui a été observé ; le modèle de Bontemps et al. simule le passage "
        "de 14 % à 6 % de coûts de transaction (droits, frais et commissions) compensé par un impôt "
        "sur la propriété.")


def regles_construction():
    vol = pd.read_csv(D / "volumes.csv", index_col=0)
    an = int(vol.commences.dropna().index.max())
    c0 = vol.commences[an]
    rp = vol.residences_principales
    croiss = 100 * (rp[an - 1] / rp[an - 11] - 1)          # croissance du parc sur dix ans, en %
    rp0 = rp[an - 1]
    fig, ax = plt.subplots(figsize=(7.2, 3.6))
    lignes = (("Plassmann et Tideman (2000) :\n+3 à 4 % de construction", 0.03 * c0, 0.04 * c0, BLEU),
              ("Banzhaf et Lavery (2010) :\n+0,6 à 2 points de croissance\ndu parc par décennie",
               0.006 * rp0 / 10, 0.02 * rp0 / 10, OCRE))
    y = np.arange(len(lignes))[::-1]
    for yi, (nom, lo, hi, col) in zip(y, lignes):
        ax.barh(yi, hi - lo, left=lo, height=0.5, color=col)
        ax.text(hi, yi, f"  {nb(lo / 1000)} à {nb(hi / 1000)} milliers", va="center", fontsize=9,
                color=INK2)
    ax.set_yticks(y)
    ax.set_yticklabels([l[0] for l in lignes], fontsize=8.5)
    ax.set_xlim(0, 90_000)
    ax.xaxis.set_major_formatter(FuncFormatter(lambda v, _: nb(v / 1000)))
    ax.set_xlabel(f"milliers de logements commencés en plus par an (pour mémoire : {nb(c0 / 1000)} "
                  f"milliers en {an})")
    grille(ax, "x")
    titre(ax, "Les effets pennsylvaniens rapportés à la construction française",
          "Logements supplémentaires par an si l'effet mesuré se reproduisait en France")
    fin(fig, "lvt_regles_construction.png",
        f"Calcul de l'auteur. Logements commencés en {an} : {nb(c0)} (Insee, Sitadel, cumul sur douze "
        f"mois, France hors Mayotte). Résidences principales : {nb(rp0 / 1e6, 1)} millions, en hausse "
        f"de {nb(croiss, 1)} % en dix ans (Insee, estimations annuelles du parc). Effets : "
        "Plassmann et Tideman d'après la synthèse de Dye et England (2010) ; Banzhaf et Lavery, "
        "modèles fondés sur le rapport des taux, pour un taux sur le terrain double ou quadruple de "
        "celui sur le bâti.",
        "Lecture : l'effet de Banzhaf et Lavery est mesuré à l'échelle de quartiers et inclut des "
        "logements qui se seraient construits ailleurs ; il majore donc l'effet national. Les deux "
        "études portent sur des écarts de taux modestes ; une bascule française complète déplacerait "
        "davantage la charge, sans qu'on sache si l'effet croîtrait en proportion.")


if __name__ == "__main__":
    foncier_pib()
    prix_terrains()
    tf_regressive()
    capitalisation()
    prix_cout_loyers()
    residu()
    gradient()
    trajectoire()
    biens_types()
    regles_prix()
    regles_dmto()
    regles_construction()
