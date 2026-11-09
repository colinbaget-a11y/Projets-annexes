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
    """Revenu brut, charge IR + CSG, et taux marginal sur 1 000 € de plus (calcul OpenFisca exact)."""
    g = C[C.profil == profil].sort_values("brut")
    tot = (g.ir + g.csg).values
    return g.brut.values, tot


def marginal(profil):
    g = C[C.profil == profil].sort_values("brut")
    return g.brut.values, ((g.ir_plus + g.csg_plus) - (g.ir + g.csg)).values / 1000.0


def trace_marginal(ax, profil, **kw):
    """Taux marginal actuel ; les sauts (seuils de CSG des retraités) sont signalés par un triangle et le
    montant de la hausse d'impôt, au lieu d'un pic hors échelle."""
    z, mg = marginal(profil)
    ok = mg <= 0.6
    y = np.where(ok, 100 * mg, np.nan)
    ax.plot(z / 1e3, y, **kw)
    if (~ok).any():
        ax.plot(z[~ok] / 1e3, np.full((~ok).sum(), 58), ls="none", marker="^", color=kw.get("color", INK), ms=5)
        ax.annotate(f"seuils de CSG : +{1000 * mg[~ok].min():.0f} à +{1000 * mg[~ok].max():.0f} € d'impôt\n"
                    "pour 1 000 € de pension en plus", (z[~ok].max() / 1e3, 58), xytext=(8, -4),
                    textcoords="offset points", fontsize=6.8, color=kw.get("color", INK), va="top")


# ------------------------------------------------------------------ l01 système actuel
def l01():
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(9.4, 3.6))
    for prof, lab, col, ls in (("seul", "Salarié seul", INK, "-"), ("couple_2enf", "Couple, deux enfants", GRIS, "--"),
                               ("retraite_seul", "Retraité seul", OCRE, "-")):
        z, tot = actuel(prof)
        a1.plot(z / 1e3, 100 * tot / z, color=col, lw=1.6, ls=ls, label=lab)
        trace_marginal(a2, prof, color=col, lw=1.3, ls=ls, label=lab)
    for ax, t in ((a1, "Taux moyen : part du revenu payée"), (a2, "Taux marginal : impôt sur 1 000 € de plus")):
        ax.set_xlim(0, 200)
        ax.set_xlabel("Revenu brut annuel du foyer (k€)")
        ax.yaxis.set_major_formatter(PCT)
        ax.set_title(t, fontsize=10, color=INK, loc="left")
        grille(ax)
    a1.set_ylim(0, 40)
    a2.set_ylim(0, 62)
    a1.legend(loc="upper left", fontsize=7.8)
    fig.subplots_adjust(wspace=0.22)
    fin(fig, "ircsg_l01_aujourdhui", SRC_OF,
        "Note : IR et CSG en % du revenu brut ; taux marginal calculé sur 1 000 € de revenu en plus. Le couple "
        "partage ses revenus 60/40. Triangles : seuils où le taux de CSG d'un retraité change et s'applique à "
        "toute sa pension (hausse d'impôt indiquée pour 1 000 € de pension en plus). Le pic du retraité vers "
        "33 000 € vient de la perte de l'abattement réservé aux plus de 65 ans ; les petits pics, du seuil de "
        "61 € en dessous duquel l'IR n'est pas recouvré ; la décote crée un palier, non un pic. Le taux du salarié seul "
        "concorde à 0,4 point près avec celui de l'OCDE (Taxing Wages 2026).")


# ------------------------------------------------------------------ l02 croissance
def l02():
    s_, _ = m.series()
    x = m.distribution()[0]
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(9.4, 3.5))
    for c, lab, col, ls in (("pib", "PIB", GRIS, "--"), ("ir", "Impôt sur le revenu", BLEU, "-"), ("csg", "CSG", OCRE, "-")):
        a1.plot(s_.index, 100 * s_[c] / s_[c].iloc[0], color=col, lw=1.8, ls=ls, label=lab)
    a1.annotate("CSG relevée\nde 1,7 point", (2018, 214), xytext=(2016.3, 108), fontsize=7.5, color=INK,
                arrowprops=dict(arrowstyle="-", color=MUTED, lw=0.7))
    a1.set_ylabel("Indice, 2000 = 100")
    a1.set_title("Recettes et PIB, 2000-2024", fontsize=10, color=INK, loc="left")
    grille(a1)
    a1.legend(loc="upper left", fontsize=7.8)
    grp = np.where(x.index <= 4, "< 30 k€", np.where(x.index <= 6, "30 à 100 k€", "> 100 k€"))
    d = x.assign(g=grp).groupby("g", sort=False)[["foyers", "assiette", "csg", "ir_trav"]].sum()
    d = 100 * d / d.sum()
    cols = [("foyers", "Foyers", GRIS), ("assiette", "Revenus", INK), ("csg", "CSG payée", OCRE), ("ir_trav", "IR payé", BLEU)]
    xs = np.arange(len(d))
    for i_, (c, lab, col) in enumerate(cols):
        a2.bar(xs + (i_ - 1.5) * 0.2, d[c], width=0.18, color=col, label=lab)
        for xi, v in zip(xs, d[c]):
            a2.annotate(f"{v:.0f}", (xi + (i_ - 1.5) * 0.2, v), xytext=(0, 2), textcoords="offset points",
                        ha="center", fontsize=7, color=INK)
    a2.set_xticks(xs)
    a2.set_xticklabels(d.index, fontsize=8.5)
    a2.set_ylabel("Part du total (%)")
    a2.set_title("Qui détient les revenus, qui paie (RFR du foyer)", fontsize=10, color=INK, loc="left")
    a2.set_ylim(0, 78)
    grille(a2)
    a2.legend(loc="upper right", fontsize=7.5, ncol=2)
    fig.subplots_adjust(wspace=0.25)
    fin(fig, "ircsg_l02_recettes", "Insee, comptes nationaux ; Eurostat (PIB) ; DGFiP, IRCOM revenus 2024 ; calculs de l'auteur.",
        "Note : à gauche, euros courants. À droite, revenus imposés au barème (activité, pensions, indépendants, "
        "foncier) ; lecture : les foyers sous 30 000 € de RFR sont 63 % des foyers, détiennent 30 % des revenus, "
        "paient 26 % de la CSG et 4 % de l'IR.")


# ------------------------------------------------------------------ l04 coût d'efficacité
def l04():
    x, f = m.distribution()
    sE, tE = m.baremes(x, f)[2]["E_franchise_taux_unique"]
    vals = [("Aujourd'hui", b.cout(b.TAU_CUR), GRIS), ("Franchise + taux unique", b.cout(m.taux_marginal(b.Z, sE, tE)), MUTED),
            ("Fonction, familles\npar l'impôt", b.cout_familial(TM1), BLEU),
            ("Fonction, familles\npar la dépense", b.cout(TM2(b.Z)), OCRE)]
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(9.4, 3.5), gridspec_kw=dict(width_ratios=[1, 1.25]))
    y = np.arange(len(vals))[::-1]
    a1.barh(y, [v for _, v, _ in vals], color=[c for _, _, c in vals], height=0.55)
    for yi, (_, v, _) in zip(y, vals):
        a1.annotate(f"{v:.0f} Md€", (v, yi), xytext=(4, 0), textcoords="offset points", va="center", fontsize=8)
    a1.set_yticks(y)
    a1.set_yticklabels([n for n, _, _ in vals], fontsize=8)
    a1.set_xlabel("Md€ par an")
    a1.set_xlim(0, 34)
    a1.set_title("Coût d'efficacité approché", fontsize=10, color=INK, loc="left")
    grille(a1, "x")
    d1 = b.deciles(b.impot_familial(T1))
    d2 = b.deciles(T2(b.Z))
    xs = np.arange(1, 11)
    a2.bar(xs - 0.2, d1.delta_eur, width=0.38, color=BLEU, label="Familles par l'impôt")
    a2.bar(xs + 0.2, d2.delta_eur, width=0.38, color=OCRE, label="Familles par la dépense")
    a2.axhline(0, color=INK, lw=0.7)
    for v in (800, -800):
        a2.axhline(v, color=MUTED, lw=0.8, ls=":")
    a2.set_xticks(xs)
    a2.set_xticklabels([f"D{i}" for i in xs], fontsize=8)
    a2.set_xlabel("Décile de foyers (revenu brut croissant)")
    a2.set_ylabel("€ par foyer et par an")
    a2.set_ylim(-1000, 1000)
    a2.set_title("Variation de la charge par décile (+ : paie plus)", fontsize=10, color=INK, loc="left")
    grille(a2)
    a2.legend(loc="lower left", fontsize=7.5)
    fig.subplots_adjust(wspace=0.55)
    fin(fig, "ircsg_l04_resultats", SRC,
        "Note : coût d'efficacité = perte de revenu taxable due aux réactions, ½·e·z·τ²/(1−τ), avec τ le taux "
        "marginal et e l'élasticité de Sicsic (2022) appliquée aux seuls revenus du travail ; ordre de grandeur. "
        "Déciles : effet mécanique moyen ; pointillés : garde-fou de ±800 €. La version « familles par la dépense » "
        "suppose versées à part des aides aux familles d'environ 21 Md€.")


# ------------------------------------------------------------------ l06 par type de revenu
def l06():
    d = b.par_type(b.impot_familial(T1))
    fig, ax = plt.subplots(figsize=(7.6, 2.7))
    y = np.arange(len(d))[::-1]
    ax.barh(y + 0.18, d.actuel, height=0.34, color=GRIS, label="Aujourd'hui (IR + CSG)")
    ax.barh(y - 0.18, d.nouveau, height=0.34, color=BLEU, label="Barème-fonction")
    for yi, (a, n_) in zip(y, zip(d.actuel, d.nouveau)):
        ax.annotate(f"{n_ - a:+.0f}", (max(a, n_), yi), xytext=(4, 0), textcoords="offset points", va="center",
                    fontsize=8, color=INK)
    ax.set_yticks(y)
    ax.set_yticklabels(d.index, fontsize=8.5)
    ax.set_xlabel("Md€ par an")
    ax.set_xlim(0, 170)
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
        trace_marginal(a2, prof, color=INK, lw=1.2, ls=ls, label=f"Aujourd'hui, {lab}")
        ab = 0.0 if prof == "seul" else b.FR_ADULTE + 2 * b.ABAT_ENFANT
        imp = T1(np.clip(a - ab, 0, None))
        a1.plot(zb / 1e3, 100 * imp / zb, color=BLEU, lw=2.2, ls=ls, label=f"Proposé, {lab}")
        a2.plot(zb / 1e3, 100 * 0.9825 * TM1(np.clip(a - ab, 0, None)) * (a > ab), color=BLEU, lw=2.2, ls=ls,
                label=f"Proposé, {lab}")
    for ax, t in ((a1, "Taux moyen : part du revenu payée"), (a2, "Taux marginal : impôt sur 1 000 € de plus")):
        ax.set_xlim(0, 200)
        ax.set_xlabel("Revenu brut annuel du foyer (k€)")
        ax.yaxis.set_major_formatter(PCT)
        ax.set_title(t, fontsize=10, color=INK, loc="left")
        grille(ax)
    a1.set_ylim(0, 35)
    a2.set_ylim(0, 50)
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
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(9.4, 3.5))
    trace_marginal(a1, "seul", color=INK, lw=1.3, label="France aujourd'hui, salarié seul")
    a1.plot(z / 1e3, 100 * 0.9825 * TM1(0.9825 * z), color=BLEU, lw=2, label="France, barème proposé")
    a1.plot(z / 1e3, nl, color=OCRE, lw=2, label="Pays-Bas 2024")
    a1.set_xlabel("Revenu brut annuel (k€)")
    a1.yaxis.set_major_formatter(PCT)
    a1.set_xlim(0, 160)
    a1.set_ylim(0, 62)
    a1.set_title("Taux marginal : Pays-Bas et France", fontsize=10, color=INK, loc="left")
    grille(a1)
    a1.legend(loc="lower right", fontsize=7.2)
    e = np.linspace(0.02, 0.8, 200)
    for a, c, lab in ((2.1, BLEU, "a = 2,1"), (2.8, VERT, "a = 2,8")):
        a2.plot(e, 100 / (1 + a * e), color=c, lw=1.8, label=f"Taux maximisant la recette, {lab}")
    for v, lab, c in ((45, "Taux du haut proposé : 45 %", GRIS), (58, "Coin marginal total actuel : 58 %", BRIQUE)):
        a2.axhline(v, color=c, lw=1, ls="--")
        a2.annotate(lab, (0.79, v), xytext=(0, 3), textcoords="offset points", ha="right", fontsize=7, color=INK,
                    bbox=dict(boxstyle="square,pad=0.1", fc="white", ec="none"))
    for v, lab in ((0.8 * 0.31, "Cabannes et al."), (0.8 * 0.51, "Sicsic")):
        a2.axvline(v, color=MUTED, lw=0.8, ls=":")
        a2.annotate(lab, (v, 93), xytext=(3, 0), textcoords="offset points", fontsize=7, color=INK, rotation=90, va="top")
    a2.set_xlabel("Élasticité du revenu imposable (part du travail ≈ 80 %)")
    a2.yaxis.set_major_formatter(PCT)
    a2.set_xlim(0, 0.8)
    a2.set_ylim(30, 95)
    a2.set_title("Taux du haut qui rapporte le plus", fontsize=10, color=INK, loc="left")
    grille(a2)
    a2.legend(loc="lower left", fontsize=7)
    fig.subplots_adjust(wspace=0.25)
    fin(fig, "ircsg_l08_etranger_laffer", "Rijksoverheid (2024) ; OpenFisca-France ; OCDE, Taxing Wages 2026 ; Saez (2001) ;"
        " calculs de l'auteur.",
        "Note : à gauche, Pays-Bas, personne d'âge actif : 36,97 % (dont 27,65 points de cotisations) puis 49,50 %, plus "
        "le retrait du crédit général (6,63 %) et du crédit d'emploi (6,51 %) ; montée du crédit d'emploi sous "
        "24 812 € non représentée. À droite : 1/(1 + a·e) ; le coin marginal OCDE inclut IR, CSG, CRDS et toutes les "
        "cotisations salariales et patronales, en % du coût du travail.")


if __name__ == "__main__":
    for fn in (l01, l02, l04, l06, l07, l08):
        fn()
