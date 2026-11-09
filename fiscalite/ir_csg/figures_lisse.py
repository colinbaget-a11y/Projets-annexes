"""Figures de la note (version « barème-fonction ») : ircsg_l01 à ircsg_l08.

Lancer depuis fiscalite/ : python3 ir_csg/figures_lisse.py ; FIG_NU=1 python3 ir_csg/figures_lisse.py
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE), str(HERE.parent)]
import bareme_lisse as b  # noqa: E402
import ir_csg as m  # noqa: E402
from graphiques import BLEU, GRIS, INK, MUTED, OCRE, VERT, PCT, fin, grille, plt  # noqa: E402

BRIQUE = "#993333"
DEMI = (4.7, 3.5)
SRC = "DGFiP, IRCOM et déclarations 2042, revenus 2024 ; CCSS ; calculs de l'auteur."
SRC_OF = "OpenFisca-France 176.1 (législation des revenus 2024) ; calculs de l'auteur."

P = b.L0
T1_V2 = b.cale(**P)
T1_V1 = b.cale(**P, impot_foyer=b.impot_familial)
TM2, T2 = b.famille(P["F"], P["t0"], P["z1"], T1_V2, P["z2"], P["t2"])
TM1, T1 = b.famille(P["F"], P["t0"], P["z1"], T1_V1, P["z2"], P["t2"])
C = pd.read_csv(HERE / "sorties/courbes_openfisca.csv")


def actuel(profil):
    g = C[C.profil == profil].sort_values("brut")
    tot = (g.ir + g.csg).values
    return g.brut.values, tot


# ------------------------------------------------------------------ l01 système actuel
def l01():
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(9.4, 3.6))
    for prof, lab, col, ls in (("seul", "Salarié seul", INK, "-"), ("couple_2enf", "Couple, deux enfants", GRIS, "--"),
                               ("retraite_seul", "Retraité seul", OCRE, "-")):
        z, tot = actuel(prof)
        a1.plot(z / 1e3, 100 * tot / z, color=col, lw=1.6, ls=ls, label=lab)
        a2.step(z[1:] / 1e3, 100 * np.clip(np.diff(tot) / np.diff(z), 0, 0.6), where="pre", color=col, lw=1.3, ls=ls,
                label=lab)
    for ax, t in ((a1, "Taux moyen : part du revenu payée"), (a2, "Taux marginal : sur 100 € de plus")):
        ax.set_xlim(0, 200)
        ax.set_xlabel("Revenu brut annuel du foyer (k€)")
        ax.yaxis.set_major_formatter(PCT)
        ax.set_title(t, fontsize=10, color=INK, loc="left")
        grille(ax)
    a1.set_ylim(0, 40)
    a2.set_ylim(0, 60)
    a1.legend(loc="upper left", fontsize=7.8)
    fig.subplots_adjust(wspace=0.22)
    fin(fig, "ircsg_l01_aujourdhui", SRC_OF,
        "Note : IR et CSG en % du revenu brut (salaire brut, pension brute). Le couple partage ses revenus 60/40. "
        "Les pics du taux marginal viennent de la décote de l'IR et des seuils de CSG des retraités.")


# ------------------------------------------------------------------ l02 croissance
def l02():
    s, _ = m.series()
    fig, ax = plt.subplots(figsize=DEMI)
    for c, lab, col, ls in (("pib", "PIB", GRIS, "--"), ("ir", "Impôt sur le revenu", BLEU, "-"), ("csg", "CSG", OCRE, "-")):
        ax.plot(s.index, 100 * s[c] / s[c].iloc[0], color=col, lw=1.8, ls=ls, label=lab)
    ax.axvline(2017.5, color=MUTED, lw=0.7, ls=":")
    ax.annotate("CSG +1,7 pt", (2017.6, 245), fontsize=7.5, color=INK)
    ax.set_ylabel("Indice, 2000 = 100")
    grille(ax)
    ax.legend(loc="upper left", fontsize=7.8)
    fin(fig, "ircsg_l02_croissance", "Insee, comptes nationaux ; Eurostat (PIB) ; calculs de l'auteur.",
        "Note : recettes et PIB en euros courants. Hors hausses de taux, la CSG suit le PIB ; l'IR suit le PIB "
        "sur longue période, avec des écarts dus aux réformes.")


# ------------------------------------------------------------------ l03 qui paie
def l03():
    x = m.distribution()[0]
    grp = np.where(x.index <= 4, "Moins de 30 000 €", np.where(x.index <= 6, "30 000 à 100 000 €", "Plus de 100 000 €"))
    d = x.assign(g=grp).groupby("g", sort=False)[["foyers", "assiette", "csg", "ir_trav"]].sum()
    d = 100 * d / d.sum()
    cols = [("foyers", "Foyers", GRIS), ("assiette", "Revenus", INK), ("csg", "CSG payée", OCRE), ("ir_trav", "IR payé", BLEU)]
    fig, ax = plt.subplots(figsize=DEMI)
    xs = np.arange(len(d))
    for i, (c, lab, col) in enumerate(cols):
        ax.bar(xs + (i - 1.5) * 0.2, d[c], width=0.18, color=col, label=lab)
        for xi, v in zip(xs, d[c]):
            ax.annotate(f"{v:.0f}", (xi + (i - 1.5) * 0.2, v), xytext=(0, 2), textcoords="offset points", ha="center",
                        fontsize=6.8, color=INK)
    ax.set_xticks(xs)
    ax.set_xticklabels(d.index, fontsize=8)
    ax.set_ylabel("Part du total (%)")
    ax.set_xlabel("Revenu fiscal de référence du foyer")
    grille(ax)
    ax.legend(loc="upper right", fontsize=7.5, ncol=2)
    ax.set_ylim(0, 75)
    fin(fig, "ircsg_l03_qui_paie", SRC,
        "Note : revenus imposés au barème (activité, pensions, indépendants, foncier). Lecture : les foyers sous "
        "30 000 € de RFR sont 63 % des foyers, détiennent 30 % des revenus, paient 26 % de la CSG et 4 % de l'IR.")


# ------------------------------------------------------------------ l04 coût d'efficacité
def l04():
    x, f = m.distribution()
    sE, tE = m.baremes(x, f)[2]["E_franchise_taux_unique"]
    vals = [("Aujourd'hui", b.cout(b.TAU_CUR)), ("Franchise et taux unique (v1)", b.cout(m.taux_marginal(b.Z, sE, tE))),
            ("Barème-fonction, familles par l'impôt", b.cout(TM1(b.Z))),
            ("Barème-fonction, familles par la dépense", b.cout(TM2(b.Z)))]
    fig, ax = plt.subplots(figsize=DEMI)
    y = np.arange(len(vals))[::-1]
    ax.barh(y, [v for _, v in vals], color=[GRIS, MUTED, BLEU, BLEU], height=0.55)
    for yi, (_, v) in zip(y, vals):
        ax.annotate(f"{v:.0f} Md€", (v, yi), xytext=(4, 0), textcoords="offset points", va="center", fontsize=8)
    ax.set_yticks(y)
    ax.set_yticklabels([n for n, _ in vals], fontsize=8)
    ax.set_xlabel("Coût d'efficacité approché (Md€ par an)")
    ax.set_xlim(0, 34)
    grille(ax, "x")
    fin(fig, "ircsg_l04_cout", SRC,
        "Note : perte de revenu taxable due aux réactions des contribuables, approchée par ½·e·z·τ²/(1−τ), avec τ "
        "le taux marginal et e l'élasticité de Sicsic (2022) appliquée aux seuls revenus du travail. Ordre de grandeur.")


# ------------------------------------------------------------------ l05 déciles
def l05():
    d1 = b.deciles(b.impot_familial(T1))
    d2 = b.deciles(T2(b.Z))
    fig, ax = plt.subplots(figsize=DEMI)
    xs = np.arange(1, 11)
    ax.bar(xs - 0.2, d1.delta_eur, width=0.38, color=BLEU, label="Familles par l'impôt")
    ax.bar(xs + 0.2, d2.delta_eur, width=0.38, color=OCRE, label="Familles par la dépense")
    ax.axhline(0, color=INK, lw=0.7)
    for v in (800, -800):
        ax.axhline(v, color=MUTED, lw=0.8, ls=":")
    ax.set_xticks(xs)
    ax.set_xticklabels([f"D{i}" for i in xs])
    ax.set_xlabel("Décile de foyers (revenu brut croissant)")
    ax.set_ylabel("Variation de la charge (€ par foyer et par an)")
    ax.set_ylim(-1000, 1000)
    grille(ax)
    ax.legend(loc="lower left", fontsize=7.5)
    fin(fig, "ircsg_l05_deciles", SRC,
        "Note : + = le foyer paie plus. Effet mécanique, moyenne par décile ; pointillés : garde-fou de ±800 €. La "
        "version « familles par la dépense » suppose versées à part des aides aux familles d'environ 21 Md€.")


# ------------------------------------------------------------------ l06 par type de revenu
def l06():
    d = b.par_type(b.impot_familial(T1))
    fig, ax = plt.subplots(figsize=DEMI)
    y = np.arange(len(d))[::-1]
    ax.barh(y + 0.18, d.actuel, height=0.34, color=GRIS, label="Aujourd'hui (IR + CSG)")
    ax.barh(y - 0.18, d.nouveau, height=0.34, color=BLEU, label="Barème-fonction")
    for yi, (a, n_) in zip(y, zip(d.actuel, d.nouveau)):
        ax.annotate(f"{n_ - a:+.0f}", (max(a, n_), yi), xytext=(4, 0), textcoords="offset points", va="center",
                    fontsize=8, color=INK)
    ax.set_yticks(y)
    ax.set_yticklabels(d.index, fontsize=8)
    ax.set_xlabel("Md€ par an")
    ax.set_xlim(0, 165)
    grille(ax, "x")
    ax.legend(loc="lower right", fontsize=7.5)
    fin(fig, "ircsg_l06_types", SRC,
        "Note : chiffre à droite = variation en Md€. Version « familles par l'impôt ». Les retraités paient plus "
        "parce que leur CSG réduite et l'abattement de 10 % sur les pensions disparaissent dans l'impôt unique.")


# ------------------------------------------------------------------ l07 courbes finales
def l07():
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(9.4, 4.0))
    zb = np.linspace(2e3, 200e3, 800)
    a = 0.9825 * zb                                   # assiette (base CSG) d'un salarié
    for prof, lab, ls in (("seul", "personne seule", "-"), ("couple_2enf", "couple, deux enfants", "--")):
        z, tot = actuel(prof)
        a1.plot(z / 1e3, 100 * tot / z, color=INK, lw=1.4, ls=ls, label=f"Aujourd'hui, {lab}")
        a2.step(z[1:] / 1e3, 100 * np.clip(np.diff(tot) / np.diff(z), 0, 0.6), where="pre", color=INK, lw=1.2, ls=ls,
                label=f"Aujourd'hui, {lab}")
        ab = 0.0 if prof == "seul" else b.FR_ADULTE + 2 * b.ABAT_ENFANT
        imp = T1(np.clip(a - ab, 0, None))
        a1.plot(zb / 1e3, 100 * imp / zb, color=BLEU, lw=2.2, ls=ls, label=f"Proposé, {lab}")
        a2.plot(zb / 1e3, 100 * 0.9825 * TM1(np.clip(a - ab, 0, None)) * (a > ab), color=BLEU, lw=2.2, ls=ls,
                label=f"Proposé, {lab}")
    for ax, t in ((a1, "Taux moyen : part du revenu payée"), (a2, "Taux marginal : sur 100 € de plus")):
        ax.set_xlim(0, 200)
        ax.set_xlabel("Revenu brut annuel du foyer (k€)")
        ax.yaxis.set_major_formatter(PCT)
        ax.set_title(t, fontsize=10, color=INK, loc="left")
        grille(ax)
    a1.set_ylim(0, 35)
    a2.set_ylim(0, 55)
    a1.legend(loc="upper left", fontsize=7.2)
    fig.subplots_adjust(wspace=0.22)
    fin(fig, "ircsg_l07_courbes", SRC_OF,
        f"Note : salariés, en % du salaire brut ; le couple partage ses revenus 60/40. Barème proposé (familles par "
        f"l'impôt) : taux marginal de 4 % au premier euro, montant en ligne droite jusqu'à {100*T1_V1:.1f} % à 30 000 €, "
        f"puis jusqu'à 45 % à 400 000 € ; seconde franchise de 6 000 € pour le couple et 3 000 € par enfant.")


# ------------------------------------------------------------------ l08 Pays-Bas
def l08():
    z = np.linspace(5e3, 160e3, 800)
    nl = np.full_like(z, np.nan)
    nl[(z > 24812) & (z <= 39957)] = 36.97 + 6.63
    nl[(z > 39957) & (z <= 75518)] = 36.97 + 6.63 + 6.51
    nl[(z > 75518) & (z <= 124934)] = 49.50 + 6.51
    nl[z > 124934] = 49.50
    zs, tot = actuel("seul")
    fig, ax = plt.subplots(figsize=DEMI)
    ax.step(zs[1:] / 1e3, 100 * np.clip(np.diff(tot) / np.diff(zs), 0, 0.6), where="pre", color=INK, lw=1.3,
            label="France aujourd'hui, salarié seul")
    ax.plot(z / 1e3, 100 * 0.9825 * TM1(0.9825 * z), color=BLEU, lw=2, label="France, barème proposé")
    ax.plot(z / 1e3, nl, color=OCRE, lw=2, label="Pays-Bas 2024")
    ax.set_xlabel("Revenu brut annuel (k€)")
    ax.set_ylabel("Taux marginal (%)")
    ax.set_xlim(0, 160)
    ax.set_ylim(0, 62)
    grille(ax)
    ax.legend(loc="lower right", fontsize=7.2)
    fin(fig, "ircsg_l08_pays_bas", "Rijksoverheid, Belangrijkste wijzigingen belastingen 2024 ; OpenFisca-France ;"
        " calculs de l'auteur.",
        "Note : Pays-Bas, personne d'âge actif : 36,97 % (dont 27,65 points de cotisations) puis 49,50 %, plus le "
        "retrait du crédit général (6,63 %) et du crédit d'emploi (6,51 %) ; montée du crédit d'emploi sous "
        "24 812 € non représentée.")


if __name__ == "__main__":
    for fn in (l01, l02, l03, l04, l05, l06, l07, l08):
        fn()
