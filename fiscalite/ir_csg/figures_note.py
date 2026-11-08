"""Figures complémentaires de la note IR + CSG (ircsg_f01 à ircsg_f11).

Lancer depuis fiscalite/ : python3 ir_csg/figures_note.py ; FIG_NU=1 python3 ir_csg/figures_note.py
Format demi-page (environ 7,5 cm imprimés) sauf mention contraire.
"""
import itertools
import sys
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE), str(HERE.parent)]
import ir_csg as m  # noqa: E402
from graphiques import (BLEU, GRIS, INK, INK2, MUTED, OCRE, VERT, PCT, fin, grille, plt,  # noqa: E402
                        titre, etiquette)

BRIQUE = "#993333"
DEMI = (4.7, 3.5)
SRC_IRCOM = "DGFiP, IRCOM et déclarations 2042, revenus 2024 ; CCSS ; calculs de l'auteur."

x, f = m.distribution()
cible, B, sc = m.baremes(x, f)
pop = x.foyers.values
sE, tE = sc["E_franchise_taux_unique"]


def nouv_tranche(xs, fs, s_, t_):
    fs = fs.copy()
    fs["n"] = fs.poids * m.impot(fs.base, s_, t_) / 1e9
    return fs.groupby("tranche", sort=False).n.sum().reindex(xs.tranche).values


def fE(t):
    return [0, 14e3, 120e3, 250e3], [0.0, t, 0.40, 0.49]


def lorenz(v):
    return np.r_[0, np.cumsum(v) / v.sum()]


# ------------------------------------------------------------------ f01 composition
def f01():
    comp = pd.Series({
        "Salaires": m.F_SAL * x.sal.sum(),
        "Pensions": m.F_PENS * x.pens.sum(),
        "Indépendants, foncier": m.F_AUT * x.ind.sum(),
        "Gérants": m.F_GER * x.ger.sum(),
        "Chômage, préretraites": m.F_CHO * x.cho.sum(),
    })
    t_cho = m.CSG_CHO_CCSS / (m.F_CHO * x.cho.sum())
    rec = pd.Series({
        "CSG sur les salaires": m.T_CSG_ACT * m.F_SAL * x.sal.sum(),
        "IR au barème": x.ir_trav.sum(),
        "CSG sur les pensions": (x.t_pens * m.F_PENS * x.pens).sum(),
        "CSG indépendants, foncier, gérants": m.T_CSG_ACT * (m.F_AUT * x.ind.sum() + m.F_GER * x.ger.sum()),
        "CSG chômage": t_cho * m.F_CHO * x.cho.sum(),
    })
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(9.4, 3.2))
    for ax, s_, tot in ((a1, comp, B), (a2, rec, cible)):
        s_ = s_.sort_values()
        ax.barh(range(len(s_)), s_.values, color=BLEU, height=0.62)
        ax.set_yticks(range(len(s_)))
        ax.set_yticklabels(s_.index, fontsize=8.5)
        for i, v in enumerate(s_.values):
            ax.annotate(f"{v:,.0f}".replace(",", " "), (v, i), xytext=(3, 0), textcoords="offset points",
                        va="center", fontsize=8.5, color=INK)
        ax.set_xlim(0, s_.max() * 1.18)
        grille(ax, "x")
        ax.set_xlabel("Md€")
    a1.set_title(f"Assiette brute : {B:,.0f} Md€".replace(",", " "), fontsize=10, color=INK, loc="left")
    a2.set_title(f"Recette à remplacer : {cible:.0f} Md€", fontsize=10, color=INK, loc="left")
    fig.subplots_adjust(wspace=0.75)
    fin(fig, "ircsg_f01_composition", SRC_IRCOM,
        "Note : revenus imposés aujourd'hui au barème de l'IR, foyers déclarants, 2024. Les revenus au PFU "
        "(environ 90 Md€) et l'IR qu'ils paient (11,5 Md€) restent hors champ.")


# ------------------------------------------------------------------ f02 élasticités annuelles
def f02():
    s, _ = m.series()
    s = s.loc[2001:]
    fig, ax = plt.subplots(figsize=DEMI)
    ref = [a for a in s.index if a in m.REFORMES_IR]
    calme = [a for a in s.index if a not in m.REFORMES_IR]
    clip = lambda v: np.clip(v, -2.5, 4.5)  # noqa: E731
    ax.axhline(1, color=GRIS, lw=0.8, ls="--")
    ax.scatter(calme, clip(s.loc[calme, "elast_ir"]), s=22, color=BLEU, label="IR, année sans réforme", zorder=3)
    ax.scatter(ref, clip(s.loc[ref, "elast_ir"]), s=22, facecolor="white", edgecolor=BLEU, lw=1.1,
               label="IR, année de réforme", zorder=3)
    ax.scatter(s.index, clip(s.elast_csg), s=16, marker="s", color=OCRE, label="CSG", zorder=2)
    for a, col in (("elast_ir", BLEU), ("elast_csg", OCRE)):
        for an in s.index:
            if s.loc[an, a] > 4.5:
                dx = {2012: -6, 2013: 6}.get(an, 0)
                ax.annotate(f"{s.loc[an, a]:.1f}".replace(".", ","), (an, 4.5), xytext=(dx, 5),
                            textcoords="offset points", ha="center", fontsize=7.5, color=col)
    ax.set_ylim(-2.7, 5.2)
    grille(ax)
    ax.legend(loc="lower left", fontsize=7.5)
    ax.set_ylabel("Élasticité apparente au PIB")
    fin(fig, "ircsg_f02_elasticites", "Insee, comptes nationaux ; Eurostat (PIB) ; calculs de l'auteur.",
        "Note : croissance de la recette rapportée à celle du PIB nominal. Valeurs au-delà de 4,5 indiquées en "
        "chiffres (2012 et 2013 pour l'IR, 2018 pour la CSG : hausses de taux). Tiret : élasticité de 1.")


# ------------------------------------------------------------------ f03 concentration
def f03():
    p = np.r_[0, np.cumsum(pop) / pop.sum()]
    fig, ax = plt.subplots(figsize=DEMI)
    ax.plot([0, 1], [0, 1], color=GRIS, lw=0.8, ls=":")
    for v, lab, c, ls in ((x.assiette.values, "Assiette brute", GRIS, "-"), (x.csg.values, "CSG", OCRE, "-"),
                          (x.charge.values, "IR + CSG", INK, "-"), (x.ir_trav.values, "IR", BLEU, "-"),
                          (nouv_tranche(x, f, sE, tE), "Barème E", BLEU, "--")):
        ax.plot(p, lorenz(v), color=c, lw=1.6 if lab != "Barème E" else 1.4, ls=ls, label=lab)
    ax.set_xlabel("Part cumulée des foyers (classés par RFR)")
    ax.set_ylabel("Part cumulée")
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{100*v:.0f} %"))
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{100*v:.0f} %"))
    grille(ax)
    ax.legend(loc="upper left", fontsize=7.5)
    fin(fig, "ircsg_f03_concentration", SRC_IRCOM,
        "Note : courbes de concentration par tranche de RFR. La CSG suit presque l'assiette ; "
        "l'IR est concentré sur le haut de la distribution.")


# ------------------------------------------------------------------ f04 cas-types OpenFisca
def f04():
    of = pd.read_csv(HERE / "sorties/marges_openfisca.csv")
    prof = {"seul": ("Salarié seul", BLEU, "-"), "couple_1act": ("Couple, un actif", VERT, "-"),
            "couple_2act_2enf": ("Couple, 2 actifs, 2 enfants", OCRE, "-"),
            "retraites_couple": ("Couple de retraités", MUTED, "-")}
    z = np.linspace(12e3, 450e3, 400)
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(9.4, 3.6))
    for k, (lab, c, ls) in prof.items():
        g = of[of.profil == k]
        a1.plot(g.assiette / 1e3, 100 * g.taux_marginal.clip(upper=0.6), color=c, lw=1.3, ls=ls, label=lab,
                drawstyle="steps-mid")
        a2.plot(g.assiette / 1e3, 100 * g.taux_moyen, color=c, lw=1.4, ls=ls, label=lab, marker="o", ms=2.5)
    a1.plot(z / 1e3, 100 * m.taux_marginal(z, sE, tE), color=INK, lw=2.0, ls="--", label="Barème E")
    a2.plot(z / 1e3, 100 * m.impot(z, sE, tE) / z, color=INK, lw=2.0, ls="--", label="Barème E")
    for ax, t in ((a1, "Taux marginal"), (a2, "Taux moyen")):
        ax.set_xscale("log")
        ax.set_xticks([15, 30, 60, 120, 250])
        ax.set_xticklabels(["15", "30", "60", "120", "250"])
        ax.set_xlabel("Assiette brute du foyer (k€, échelle log)")
        ax.yaxis.set_major_formatter(PCT)
        ax.set_title(t, fontsize=10, color=INK, loc="left")
        grille(ax)
    a1.set_ylim(0, 62)
    a2.legend(loc="upper left", fontsize=7.5)
    fig.subplots_adjust(wspace=0.25)
    fin(fig, "ircsg_f04_cas_types", "OpenFisca-France 176.1 (législation des revenus 2024) ; calculs de l'auteur.",
        "Note : IR et CSG en % de l'assiette brute (98,25 % du salaire brut, pension brute). Taux marginal "
        "tronqué à 60 % (pics de la décote et des seuils de CSG des retraités). Le barème E s'applique au foyer "
        "sans quotient : il ne distingue pas les profils, ce qui est la question de l'unité d'imposition.")


# ------------------------------------------------------------------ f05 gains par tranche
def f05():
    res = []
    for cap, split in itertools.product(["prorata", "mixte", "haut"], [None, "prorata"]):
        xs, fs = m.distribution(indep=cap, split=split)
        t = m.calibre(fs, xs.charge.sum(), fE, 0.05, 0.39)
        n = nouv_tranche(xs, fs, *fE(t))
        res.append(1e9 * (xs.charge.values - n) / xs.foyers.values)
    r = np.array(res)
    cen = 1e9 * (x.charge.values - nouv_tranche(x, f, sE, tE)) / pop
    k = 8
    lab = ["< 10", "10-12", "12-15", "15-20", "20-30", "30-50", "50-100", "100-200"]
    fig, ax = plt.subplots(figsize=DEMI)
    col = [BLEU if v >= 0 else BRIQUE for v in cen[:k]]
    ax.bar(range(k), cen[:k], color=col, width=0.62)
    ax.errorbar(range(k), cen[:k], yerr=[cen[:k] - r.min(0)[:k], r.max(0)[:k] - cen[:k]], fmt="none",
                ecolor=INK, elinewidth=0.8, capsize=2.5)
    ax.axhline(0, color=INK, lw=0.7)
    ax.set_xticks(range(k))
    ax.set_xticklabels(lab, rotation=45, ha="right", fontsize=8)
    ax.set_xlabel("RFR du foyer (k€)")
    ax.set_ylabel("Gain moyen par foyer (€ par an)")
    ax.set_ylim(-1500, 1500)
    grille(ax)
    fig.subplots_adjust(bottom=0.24)
    fin(fig, "ircsg_f05_gains", SRC_IRCOM,
        "Note : effet mécanique du barème E, en moyenne par tranche. Barre : scénario central ; trait : étendue "
        "sur six hypothèses (répartition des revenus au PFU entre tranches, partage de l'IR). Au-delà de "
        "200 000 € (0,3 million de foyers), l'incertitude dépasse l'ordre de grandeur de l'effet.")


# ------------------------------------------------------------------ f06 écart de Lorenz
def f06():
    fig, ax = plt.subplots(figsize=DEMI)
    for cap, c, lab in (("prorata", VERT, "PFU au prorata"), ("mixte", BLEU, "Central"),
                        ("haut", BRIQUE, "PFU en haut")):
        xs, fs = m.distribution(indep=cap)
        t = m.calibre(fs, xs.charge.sum(), fE, 0.05, 0.39)
        n = nouv_tranche(xs, fs, *fE(t))
        d = 1000 * (lorenz(xs.assiette.values - n) - lorenz(xs.assiette.values - xs.charge.values))
        ax.plot(range(len(d) - 1), d[1:], color=c, lw=1.6, marker="o", ms=2.5, label=lab)
    ax.axhline(0, color=INK, lw=0.7)
    pc = np.cumsum(x.foyers.values) / x.foyers.sum()
    ticks = [0, 4, 7, 15, 24]
    ax.set_xticks(ticks)
    ax.set_xticklabels(["10 k€\n19 %", "30 k€\n63 %", "200 k€\n99,4 %", "1 M€", "Tous"], fontsize=7)
    ax.set_xlabel("Foyers jusqu'au plafond de la tranche de RFR (et part cumulée)")
    ax.set_ylabel("Écart de Lorenz, E − actuel (‰)")
    grille(ax)
    ax.legend(loc="upper right", fontsize=7.5)
    fin(fig, "ircsg_f06_lorenz", SRC_IRCOM,
        "Note : différence entre la part du revenu après impôt détenue par les foyers les plus modestes avec le "
        "barème E et aujourd'hui, en pour mille, aux bornes des tranches de RFR. Positive partout : dominance "
        "de Lorenz. Elle échoue de peu entre 100 000 et 300 000 € si les revenus au PFU sont logés aussi haut "
        "que possible.")


# ------------------------------------------------------------------ f07 frontière du balayage
def f07():
    rows = []
    for F, S1, T1 in itertools.product([8e3, 10e3, 12e3, 14e3, 16e3, 18e3, 20e3],
                                       [60e3, 75e3, 90e3, 105e3, 120e3, 150e3, 200e3], [0.40, 0.45]):
        fab = lambda t: ([0, F, S1, 250e3], [0.0, t, T1, 0.49])  # noqa: E731
        t = m.calibre(f, cible, fab, 0.02, 0.34)
        if t >= T1:
            continue
        n = nouv_tranche(x, f, *fab(t))
        gap = (lorenz(x.assiette.values - n) - lorenz(x.assiette.values - x.charge.values))[1:-1].min()
        h = (100 * (n - x.charge.values) / x.assiette.values)[:9].max()
        part = f.poids[(f.base > F) & (f.base <= S1)].sum() / f.poids.sum()
        rows.append((100 * part, 1000 * gap, h, F, S1, T1))
    r = pd.DataFrame(rows, columns=["part", "gap", "h", "F", "S1", "T1"])
    ok = (r.gap >= -0.1) & (r.h <= 2)
    r["gap"] = r.gap.clip(lower=-12)
    fig, ax = plt.subplots(figsize=DEMI)
    ax.scatter(r.part[~ok], r.gap[~ok], s=14, facecolor="white", edgecolor=GRIS, lw=0.8,
               label="Ne remplit pas les deux conditions")
    ax.scatter(r.part[ok], r.gap[ok], s=18, color=BLEU, label="Dominance de Lorenz, hausse ≤ 2 pts")
    e = r[(r.F == 14e3) & (r.S1 == 120e3) & (r.T1 == 0.40)].iloc[0]
    ax.scatter([e.part], [e.gap], s=60, facecolor="none", edgecolor=INK, lw=1.4)
    etiquette(ax, e.part, e.gap, "E", INK, dx=7)
    ax.axhline(0, color=INK, lw=0.7)
    ax.set_xlabel("Part des foyers au taux unique (%)")
    ax.set_ylabel("Pire écart de Lorenz (‰)")
    grille(ax)
    ax.legend(loc="lower left", fontsize=7.2)
    ax.set_ylabel("Pire écart de Lorenz, E − actuel (‰)")
    fin(fig, "ircsg_f07_balayage", SRC_IRCOM,
        "Note : 98 barèmes « franchise (8 à 20 k€), taux unique jusqu'à 60-200 k€, 40 ou 45 %, 49 % au-delà de "
        "250 k€ », tous calés sur la même recette ; scénario central. Ordonnée : plus faible écart de Lorenz aux "
        "bornes des tranches (positif : dominance). Les points bleus remplissent aussi la condition de hausse "
        "limitée à 2 points ; écarts inférieurs à −12 ‰ ramenés à −12.")


# ------------------------------------------------------------------ f08 sensibilité du taux unique
def f08():
    base_vals = dict(F_SAL=m.F_SAL, F_PENS=m.F_PENS, F_AUT=m.F_AUT, CAP_PFU_TOT=m.CAP_PFU_TOT)
    cas = [("Central", {}, {}),
           ("PFU : prorata", {}, dict(indep="prorata")),
           ("PFU : en haut", {}, dict(indep="haut")),
           ("IR : prorata", {}, dict(split="prorata")),
           ("PFU : 75 Md€", dict(CAP_PFU_TOT=75.0), {}),
           ("PFU : 105 Md€", dict(CAP_PFU_TOT=105.0), {}),
           ("Salaires ×1,15", dict(F_SAL=1.15), {}),
           ("Salaires ×1,25", dict(F_SAL=1.25), {}),
           ("Pensions ×1,04", dict(F_PENS=1.04), {}),
           ("Pensions ×1,07", dict(F_PENS=1.07), {}),
           ("Indép., foncier ×1,0", dict(F_AUT=1.0), {}),
           ("Indép., foncier ×1,3", dict(F_AUT=1.3), {}),
           ("Densité uniforme", {}, dict(forme="uniforme"))]
    out = []
    for lab, const, kw in cas:
        for k_, v in const.items():
            setattr(m, k_, v)
        xs, fs = m.distribution(**kw)
        out.append((lab, 100 * m.calibre(fs, xs.charge.sum(), fE, 0.05, 0.39)))
        for k_, v in base_vals.items():
            setattr(m, k_, v)
    fig, ax = plt.subplots(figsize=(4.7, 3.9))
    y = np.arange(len(out))[::-1]
    c0 = out[0][1]
    ax.axvline(c0, color=GRIS, lw=0.8, ls="--")
    for yi, (lab, v) in zip(y, out):
        ax.plot([c0, v], [yi, yi], color=GRIS, lw=1)
        ax.scatter([v], [yi], s=22, color=BLEU if lab != "Central" else INK, zorder=3)
        ax.annotate(f"{v:.1f}".replace(".", ","), (v, yi), xytext=(5 if v >= c0 else -5, 0),
                    textcoords="offset points", ha="left" if v >= c0 else "right", va="center", fontsize=7.5)
    ax.set_yticks(y)
    ax.set_yticklabels([o[0] for o in out], fontsize=8.5)
    ax.set_xlabel("Taux unique du barème E (%)")
    ax.set_xlim(c0 - 1.6, c0 + 1.6)
    grille(ax, "x")
    fin(fig, "ircsg_f08_sensibilite", SRC_IRCOM,
        "Note : taux unique qui redonne la recette, la franchise (14 000 €) et les taux supérieurs (40 % de 120 000 "
        "à 250 000 €, 49 % au-delà) restant fixes. Une hypothèse change à la fois : répartition des revenus "
        "au PFU entre tranches et leur montant, partage de l'IR, rapports brut / net imposable, forme de la "
        "densité intra-tranche.")


# ------------------------------------------------------------------ f09 Pareto
def f09():
    fs = f.sort_values("base")
    z, w = fs.base.values, fs.poids.values
    zs = np.exp(np.linspace(np.log(12e3), np.log(600e3), 60))
    a = []
    for s_ in zs:
        sel = z > s_
        zm = np.average(z[sel], weights=w[sel])
        a.append(zm / (zm - s_))
    fig, ax = plt.subplots(figsize=DEMI)
    ax.plot(zs / 1e3, a, color=BLEU, lw=1.8, label="a(z*) reconstitué, assiette brute")
    ax.axhline(2.1, color=OCRE, lw=1.4, ls="--", label="a ≈ 2,1 (Cabannes, Houdré, Landais)")
    for s_ in (120, 250):
        ax.axvline(s_, color=GRIS, lw=0.7, ls=":")
    ax.set_xscale("log")
    ax.set_xticks([15, 30, 60, 120, 250, 500])
    ax.set_xticklabels(["15", "30", "60", "120", "250", "500"])
    ax.set_xlabel("Seuil z* (k€, échelle log)")
    ax.set_ylabel("a = E[z | z > z*] / (E[z | z > z*] − z*)")
    ax.set_ylim(1, 4)
    grille(ax)
    ax.legend(loc="upper left", fontsize=7.5)
    fin(fig, "ircsg_f09_pareto", SRC_IRCOM,
        "Note : plus a est faible, plus le haut de la distribution est épais et plus le taux optimal au-delà du "
        "seuil est élevé. Pointillés : seuils des tranches à 40 % et 49 % du barème E.")


# ------------------------------------------------------------------ f10 taux maximisant la recette
def f10():
    e = np.linspace(0.02, 0.8, 200)
    # étiquettes des horizontales à droite, là où les courbes sont passées sous 45 %
    fig, ax = plt.subplots(figsize=DEMI)
    for a, c, lab in ((2.1, BLEU, "a = 2,1"), (2.8, VERT, "a = 2,8")):
        ax.plot(e, 100 / (1 + a * e), color=c, lw=1.8, label=f"Taux maximisant la recette, {lab}")
    for v, lab in ((49, "Taux supérieur de E : 49 %"), (54, "Coin avec 10 pts d'autres prélèvements : 54 %")):
        ax.axhline(v, color=GRIS if v == 49 else BRIQUE, lw=1, ls="--")
        ax.annotate(lab, (0.8, v), xytext=(0, 3), textcoords="offset points", ha="right",
                    fontsize=7.2, color=INK2)
    for v, lab in ((0.8 * 0.31, "Cabannes et al."), (0.8 * 0.51, "Sicsic")):
        ax.axvline(v, color=MUTED, lw=0.8, ls=":")
        ax.annotate(lab, (v, 93), xytext=(3, 0), textcoords="offset points", fontsize=7.2, color=INK2, rotation=90,
                    va="top")
    ax.set_xlabel("Élasticité du revenu imposable (effective, part du travail ≈ 80 %)")
    ax.set_xlim(0, 0.8)
    ax.set_ylabel("Taux (%)")
    ax.set_ylim(30, 95)
    grille(ax)
    ax.legend(loc="lower left", fontsize=7.2)
    fin(fig, "ircsg_f10_laffer", "Saez (2001) ; Piketty et Saez (2013) ; calculs de l'auteur.",
        "Note : taux maximisant la recette au-delà d'un seuil, 1 / (1 + a·e). Verticales : élasticités du décile "
        "supérieur estimées en France (0,31 et 0,51), multipliées par la part du travail dans l'assiette.")


# ------------------------------------------------------------------ f11 Pays-Bas
def f11():
    z = np.linspace(5e3, 160e3, 800)
    nl = np.full_like(z, np.nan)
    nl[(z > 24812) & (z <= 39957)] = 36.97 + 6.63
    nl[(z > 39957) & (z <= 75518)] = 36.97 + 6.63 + 6.51
    nl[(z > 75518) & (z <= 124934)] = 49.50 + 6.51
    nl[z > 124934] = 49.50
    of = pd.read_csv(HERE / "sorties/marges_openfisca.csv")
    g = of[of.profil == "seul"]
    fig, ax = plt.subplots(figsize=DEMI)
    ax.plot(g.assiette / 1e3, 100 * g.taux_marginal, color=MUTED, lw=1.4, drawstyle="steps-mid",
            label="France, IR + CSG, salarié seul")
    ax.plot(z / 1e3, 100 * m.taux_marginal(z, sE, tE), color=BLEU, lw=2, label="France, barème E")
    ax.plot(z / 1e3, nl, color=OCRE, lw=2, label="Pays-Bas 2024, impôt + cotisations")
    ax.set_xlabel("Revenu brut annuel (k€)")
    ax.set_ylabel("Taux marginal (%)")
    ax.set_xlim(0, 160)
    ax.set_ylim(0, 62)
    grille(ax)
    ax.legend(loc="lower right", fontsize=7.2)
    fin(fig, "ircsg_f11_pays_bas", "Rijksoverheid, Belangrijkste wijzigingen belastingen 2024 ; OpenFisca-France ;"
        " calculs de l'auteur.",
        "Note : Pays-Bas, personne de moins de l'âge de la retraite : tranche à 36,97 % (dont 27,65 points de "
        "cotisations) puis 49,50 %, plus le retrait du crédit général (6,63 %) et du crédit d'emploi (6,51 %). "
        "La montée du crédit d'emploi sous 24 812 € n'est pas représentée. Les assiettes ne sont pas "
        "strictement identiques entre les deux pays.")


# ------------------------------------------------------------------ f12 courbes finales
def f12():
    c = pd.read_csv(HERE / "sorties/courbes_openfisca.csv")
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(9.4, 3.9))
    zb = np.linspace(5e3, 250e3, 600)
    # barème E : assiette = 98,25 % du salaire brut (base de la CSG) ; taux exprimés en % du brut
    tE_moy = 100 * m.impot(0.9825 * zb, sE, tE) / zb
    tE_marg = 100 * 0.9825 * m.taux_marginal(0.9825 * zb, sE, tE)
    for prof, lab, col, ls in (("seul", "Aujourd'hui : personne seule", INK, "-"),
                               ("couple_2enf", "Aujourd'hui : couple, deux enfants", GRIS, "--")):
        g = c[c.profil == prof].sort_values("brut")
        tot = g.ir + g.csg
        a1.plot(g.brut / 1e3, 100 * tot / g.brut, color=col, lw=1.6, ls=ls, label=lab)
        mg = np.diff(tot) / np.diff(g.brut)
        a2.step(g.brut.values[1:] / 1e3, 100 * np.clip(mg, 0, 0.6), where="pre", color=col, lw=1.4, ls=ls, label=lab)
    a1.plot(zb / 1e3, tE_moy, color=BLEU, lw=2.4, label="Proposé (tous les foyers)")
    a2.plot(zb / 1e3, tE_marg, color=BLEU, lw=2.4, label="Proposé (tous les foyers)")
    for ax, t in ((a1, "Taux moyen : part du revenu payée en impôt"),
                  (a2, "Taux marginal : impôt sur 100 € de plus")):
        ax.set_xlim(0, 250)
        ax.set_xlabel("Revenu brut annuel du foyer (k€)")
        ax.yaxis.set_major_formatter(PCT)
        ax.set_title(t, fontsize=10, color=INK, loc="left")
        grille(ax)
    a1.set_ylim(0, 40)
    a2.set_ylim(0, 55)
    a1.legend(loc="upper left", fontsize=7.8)
    fig.subplots_adjust(wspace=0.22)
    fin(fig, "ircsg_f12_courbes", "OpenFisca-France 176.1 (législation des revenus 2024) ; calculs de l'auteur.",
        "Note : IR et CSG en % du salaire brut, salariés ; le couple partage ses revenus 60/40. Barème proposé : "
        "0 % jusqu'à 14 000 €, 17,2 % jusqu'à 120 000 €, 40 % jusqu'à 250 000 €, 49 % au-delà, appliqué au revenu "
        "du foyer sans quotient familial. Les pics du taux marginal actuel viennent de la décote de l'IR.")


if __name__ == "__main__":
    for fn in (f01, f02, f03, f04, f05, f06, f07, f08, f09, f10, f11, f12):
        fn()
