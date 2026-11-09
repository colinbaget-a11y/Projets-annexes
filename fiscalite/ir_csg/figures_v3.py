"""Figures de la note, version 3 (IR + CSG + CRDS, quotient conjugal, crédit par enfant) : ircsg_v01 à ircsg_v08.

Lancer depuis fiscalite/ : python3 ir_csg/figures_v3.py ; FIG_NU=1 python3 ir_csg/figures_v3.py
"""
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE), str(HERE.parent)]
import bareme_v3 as v  # noqa: E402
import ir_csg as m  # noqa: E402
from graphiques import BLEU, GRIS, INK, MUTED, OCRE, PCT, fin, grille, plt  # noqa: E402

BRIQUE = "#993333"
SRC = "DGFiP, IRCOM et déclarations 2042, revenus 2024 ; CCSS ; calculs de l'auteur."
SRC_OF = "OpenFisca-France 176.1 (législation des revenus 2024) ; calculs de l'auteur."
CT = v.CT
T1, TM, T = v.retenu()
C = v.V3["C"]
NEW = v.cas_types(T, C)
NEW_P = v.cas_types(T, C, plus=True)


def fr(u, d=1):
    return f"{u:.{d}f}".replace(".", ",")


def courbe(profil, nouveau=False):
    g = CT[CT.profil == profil].sort_values("brut")
    if nouveau:
        return g.brut.values, NEW[g.index], (NEW_P[g.index] - NEW[g.index]) / 1000
    return g.brut.values, g.actuel.values, (g.actuel_plus - g.actuel).values / 1000


def trace_marginal(ax, z, mg, **kw):
    """Les sauts de plus de 60 % (seuils de CSG des retraités) sont signalés par un triangle."""
    ok = mg <= 0.6
    ax.plot(z / 1e3, np.where(ok, 100 * mg, np.nan), **kw)
    if (~ok).any():
        ax.plot(z[~ok] / 1e3, np.full((~ok).sum(), 58), ls="none", marker="^", color=kw.get("color", INK), ms=5)
        ax.annotate(f"seuils de CSG : +{1000 * mg[~ok].min():.0f} à +{1000 * mg[~ok].max():.0f} €\n"
                    "pour 1 000 € de pension en plus", (z[~ok].max() / 1e3, 58), xytext=(8, -4),
                    textcoords="offset points", fontsize=6.8, color=kw.get("color", INK), va="top")


def axes_taux(a1, a2, xmax=200):
    for ax, t in ((a1, "Taux moyen : part du revenu payée"), (a2, "Taux marginal : impôt sur 1 000 € de plus")):
        ax.set_xlim(0, xmax)
        ax.set_xlabel("Revenu brut annuel du foyer (k€)")
        ax.yaxis.set_major_formatter(PCT)
        ax.set_title(t, fontsize=10, color=INK, loc="left")
        grille(ax)


# ------------------------------------------------------------------ v01 système actuel
def v01():
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(9.4, 3.6))
    for prof, lab, col, ls in (("seul", "Salarié seul", INK, "-"), ("couple_2enf", "Couple, deux enfants", GRIS, "--"),
                               ("retraite_seul", "Retraité seul", OCRE, "-")):
        z, t, mg = courbe(prof)
        a1.plot(z / 1e3, 100 * t / z, color=col, lw=1.6, ls=ls, label=lab)
        trace_marginal(a2, z, mg, color=col, lw=1.3, ls=ls)
    axes_taux(a1, a2)
    a1.set_ylim(0, 42)
    a2.set_ylim(0, 62)
    a1.legend(loc="upper left", fontsize=7.8)
    fig.subplots_adjust(wspace=0.22)
    fin(fig, "ircsg_v01_aujourdhui", SRC_OF,
        "Note : IR, CSG et CRDS en % du revenu brut (salaire brut ou pension brute) ; taux marginal calculé sur "
        "1 000 € de plus. Le couple partage ses revenus 60/40. Triangles : seuils où le taux de CSG d'un retraité "
        "change et s'applique à toute sa pension. Le pic du retraité vers 33 000 € vient de la perte de "
        "l'abattement des plus de 65 ans ; les petits pics, du seuil de 61 € sous lequel l'IR n'est pas "
        "recouvré.")


# ------------------------------------------------------------------ v02 recettes et répartition
def v02():
    s_, _ = m.series()
    x = v.x
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(9.4, 3.5), gridspec_kw=dict(width_ratios=[1, 1.1]))
    for c, lab, col, ls in (("pib", "PIB", GRIS, "--"), ("ir", "Impôt sur le revenu", BLEU, "-"), ("csg", "CSG", OCRE, "-")):
        a1.plot(s_.index, 100 * s_[c] / s_[c].iloc[0], color=col, lw=1.8, ls=ls, label=lab)
    a1.annotate("CSG relevée\nde 1,7 point", (2018, 214), xytext=(2016.3, 108), fontsize=7.5, color=INK,
                arrowprops=dict(arrowstyle="-", color=MUTED, lw=0.7))
    a1.set_ylabel("Indice, 2000 = 100")
    a1.set_title("Recettes et PIB, 2000-2024", fontsize=10, color=INK, loc="left")
    grille(a1)
    a1.legend(loc="upper left", fontsize=7.8)
    grp = np.where(x.a < 30e3, 0, np.where(x.a < 100e3, 1, 2))
    d = x.assign(g=grp, cc=x.csg + x.crds).groupby("g")[["foyers", "assiette", "cc", "ir_trav"]].sum()
    d = 100 * d / d.sum()
    mes = [("foyers", "Foyers"), ("assiette", "Revenus"), ("cc", "CSG + CRDS"), ("ir_trav", "IR")]
    labs = ["Revenu fiscal < 30 000 €", "30 000 à 100 000 €", "> 100 000 €"]
    cols = ["#c9d6e3", "#6f8fb0", "#1f3b5a"]
    xs = np.arange(len(mes))
    bas = np.zeros(len(mes))
    for g_, (lab, col) in enumerate(zip(labs, cols)):
        vals = np.array([d.loc[g_, c] for c, _ in mes])
        a2.bar(xs, vals, bottom=bas, color=col, width=0.62, label=lab)
        for xi, (b0, vv) in enumerate(zip(bas, vals)):
            if vv >= 5:
                a2.annotate(f"{vv:.0f} %", (xi, b0 + vv / 2), ha="center", va="center", fontsize=7.5,
                            color="white" if g_ else INK)
        bas += vals
    a2.set_xticks(xs)
    a2.set_xticklabels([lab for _, lab in mes], fontsize=8.5)
    a2.set_ylim(0, 100)
    a2.yaxis.set_major_formatter(PCT)
    a2.set_title("Part de chaque groupe de foyers", fontsize=10, color=INK, loc="left")
    a2.legend(loc="upper center", bbox_to_anchor=(0.5, -0.1), fontsize=7.2, ncol=3, frameon=False)
    fig.subplots_adjust(wspace=0.25)
    fin(fig, "ircsg_v02_recettes", "Insee, comptes nationaux ; Eurostat (PIB) ; DGFiP, IRCOM revenus 2024 ; calculs de l'auteur.",
        "Note : à gauche, euros courants. À droite, trois groupes de foyers selon leur revenu fiscal de référence ; "
        "revenus imposés au barème (activité, pensions, indépendants, foncier). Lecture : les foyers sous 30 000 € "
        f"sont {d.loc[0, 'foyers']:.0f} % des foyers, détiennent {d.loc[0, 'assiette']:.0f} % des revenus, paient "
        f"{d.loc[0, 'cc']:.0f} % de la CSG et de la CRDS et {d.loc[0, 'ir_trav']:.0f} % de l'IR.")


# ------------------------------------------------------------------ v04 coût d'efficacité et déciles
def v04():
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(9.4, 3.4), gridspec_kw=dict(width_ratios=[1, 1.3]))
    jeux = ("bas", "central", "haut")
    act = [v.cout_actuel(j) for j in jeux]
    nv = [v.cout(TM, j) for j in jeux]
    y = np.array([1, 0])
    for yi, vals, col, lab in ((1, act, GRIS, "Aujourd'hui"), (0, nv, BLEU, "Proposé")):
        a1.barh(yi, vals[1], color=col, height=0.5)
        a1.errorbar(vals[1], yi, xerr=[[vals[1] - vals[0]], [vals[2] - vals[1]]], color=INK, capsize=4, lw=1)
        a1.annotate(f"{vals[1]:.0f} Md€\n({vals[0]:.0f} à {vals[2]:.0f})", (vals[2], yi), xytext=(5, 0),
                    textcoords="offset points", va="center", fontsize=7.8)
    a1.set_yticks(y)
    a1.set_yticklabels(["Aujourd'hui", "Proposé"], fontsize=8.5)
    a1.set_xlim(0, 45)
    a1.set_xlabel("Md€ par an")
    a1.set_title("Coût d'efficacité approché", fontsize=10, color=INK, loc="left")
    grille(a1, "x")
    d = v.deciles(v.impot(T, C))
    xs = np.arange(1, 11)
    a2.bar(xs, d.delta_eur, color=[BRIQUE if u > 0 else BLEU for u in d.delta_eur], width=0.6)
    for xi, u in zip(xs, d.delta_eur):
        a2.annotate(f"{u:+.0f}", (xi, u), xytext=(0, 3 if u > 0 else -9), textcoords="offset points", ha="center", fontsize=7)
    a2.axhline(0, color=INK, lw=0.7)
    for u in (800, -800):
        a2.axhline(u, color=MUTED, lw=0.8, ls=":")
    a2.set_xticks(xs)
    a2.set_xticklabels([f"D{i}" for i in xs], fontsize=8)
    a2.set_xlabel("Décile de foyers (revenu brut croissant)")
    a2.set_ylabel("€ par foyer et par an")
    a2.set_ylim(-1000, 1000)
    a2.set_title("Variation de la charge moyenne (+ : paie plus)", fontsize=10, color=INK, loc="left")
    grille(a2)
    fig.subplots_adjust(wspace=0.45)
    fin(fig, "ircsg_v04_resultats", SRC,
        "Note : coût d'efficacité = revenu que les contribuables cessent de gagner ou de déclarer à cause de "
        "l'impôt, approché par ½·e·z·τ²/(1−τ) (Feldstein, 1999), sur les seuls revenus du travail ; barre : jeu "
        "d'élasticités central, trait : jeux bas et haut. Déciles : effet avant réactions, en moyenne par foyer ; "
        "pointillés : garde-fou de ±800 €.")


# ------------------------------------------------------------------ v05 retraités
def v05():
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(9.4, 3.4))
    z, t, _ = courbe("retraite_seul")
    _, tn, _ = courbe("retraite_seul", True)
    k = z <= 60e3
    a1.plot(z[k] / 1e3, t[k], color=GRIS, lw=1.8, label="Aujourd'hui")
    a1.plot(z[k] / 1e3, tn[k], color=BLEU, lw=2.2, label="Proposé")
    zs, ts, _ = courbe("seul")
    # salarié qui a le même revenu après cotisations que le retraité : brut = pension / 0,887
    a1.plot(z[k] / 1e3, np.interp(z[k] / 0.887, zs, ts), color=INK, lw=1, ls=":",
            label="Aujourd'hui, salarié au même revenu\naprès cotisations")
    a1.set_xlabel("Pension brute annuelle (k€)")
    a1.set_ylabel("€ par an")
    a1.set_xlim(5, 60)
    a1.set_ylim(0, 16000)
    a1.set_title("Impôt d'un retraité seul", fontsize=10, color=INK, loc="left")
    grille(a1)
    a1.legend(loc="upper left", fontsize=7.2)
    d = tn - t
    a2.bar(z[k] / 1e3, d[k], width=0.45, color=[BRIQUE if u > 0 else BLEU for u in d[k]])
    a2.axhline(0, color=INK, lw=0.7)
    a2.set_xlabel("Pension brute annuelle (k€)")
    a2.set_ylabel("€ par an")
    a2.set_xlim(5, 60)
    a2.set_title("Écart : proposé − aujourd'hui (+ : paie plus)", fontsize=10, color=INK, loc="left")
    grille(a2)
    fig.subplots_adjust(wspace=0.28)
    fin(fig, "ircsg_v05_retraites", SRC_OF,
        "Note : retraité seul de plus de 65 ans, sans autre revenu ; IR, CSG et CRDS ; CASA (0,3 %) non comprise, "
        "elle est maintenue. Le revenu fiscal de référence de l'année sert aussi de référence pour le taux de CSG.")


# ------------------------------------------------------------------ v06 par type de revenu
def v06():
    d = v.par_type(v.impot(T, C))
    fig, ax = plt.subplots(figsize=(7.6, 2.7))
    y = np.arange(len(d))[::-1]
    ax.barh(y + 0.18, d.actuel, height=0.34, color=GRIS, label="Aujourd'hui (IR + CSG + CRDS)")
    ax.barh(y - 0.18, d.nouveau, height=0.34, color=BLEU, label="Impôt unique proposé")
    for yi, (a, n_) in zip(y, zip(d.actuel, d.nouveau)):
        ax.annotate(f"{n_ - a:+.1f}".replace(".", ","), (max(a, n_), yi), xytext=(4, 0), textcoords="offset points",
                    va="center", fontsize=8, color=INK)
    ax.set_yticks(y)
    ax.set_yticklabels(d.index, fontsize=8.5)
    ax.set_xlabel("Md€ par an")
    ax.set_xlim(0, 175)
    grille(ax, "x")
    ax.legend(loc="lower right", fontsize=7.5)
    fin(fig, "ircsg_v06_types", SRC,
        "Note : chiffre à droite = variation en Md€, avant réactions. Les retraités paient plus parce que leur CSG "
        "réduite, leur abattement de 10 % et celui des plus de 65 ans disparaissent, et parce que l'impôt porte "
        "désormais sur le revenu après cotisations pour tous.")


# ------------------------------------------------------------------ v07 courbes finales
def v07():
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(9.4, 4.0))
    for prof, lab, ls in (("seul", "personne seule", "-"), ("couple_2enf", "couple, deux enfants", "--")):
        z, t, mg = courbe(prof)
        a1.plot(z / 1e3, 100 * t / z, color=INK, lw=1.3, ls=ls, label=f"Aujourd'hui, {lab}")
        trace_marginal(a2, z, mg, color=INK, lw=1.1, ls=ls)
        z, t, mg = courbe(prof, True)
        a1.plot(z / 1e3, 100 * t / z, color=BLEU, lw=2.2, ls=ls, label=f"Proposé, {lab}")
        a2.plot(z / 1e3, 100 * mg, color=BLEU, lw=2.2, ls=ls)
    axes_taux(a1, a2)
    a1.set_ylim(0, 36)
    a2.set_ylim(0, 50)
    a1.legend(loc="upper left", fontsize=7.2)
    fig.subplots_adjust(wspace=0.22)
    fin(fig, "ircsg_v07_courbes", SRC_OF,
        f"Note : salariés, en % du salaire brut ; IR, CSG et CRDS ; le couple partage ses revenus 60/40. Foyers sans "
        f"aucune niche ni déduction : un foyer réel de même revenu paie souvent moins aujourd'hui. Barème proposé, sur "
        f"le revenu après cotisations, par part : taux marginal de 7 % au premier euro, 14 % à 20 000 €, "
        f"{fr(100 * T1)} % à 30 000 €, 45 % à partir de 120 000 € ; deux parts pour un couple ; crédit de "
        f"{C:.0f} € par enfant.")


# ------------------------------------------------------------------ v08 Pays-Bas
def v08():
    z = np.linspace(5e3, 160e3, 800)
    nl = np.full_like(z, np.nan)
    nl[(z > 24812) & (z <= 39957)] = 36.97 + 6.63
    nl[(z > 39957) & (z <= 75518)] = 36.97 + 6.63 + 6.51
    nl[(z > 75518) & (z <= 124934)] = 49.50 + 6.51
    nl[z > 124934] = 49.50
    fig, ax = plt.subplots(figsize=(6.4, 3.3))
    zz, _, mg = courbe("seul")
    trace_marginal(ax, zz, mg, color=INK, lw=1.3, label="France aujourd'hui (IR, CSG, CRDS)")
    zz, _, mg = courbe("seul", True)
    ax.plot(zz / 1e3, 100 * mg, color=BLEU, lw=2, label="France, impôt unique proposé")
    ax.plot(z / 1e3, nl, color=OCRE, lw=2, label="Pays-Bas 2024 (impôt et cotisations)")
    ax.set_xlabel("Revenu brut annuel d'une personne seule (k€)")
    ax.yaxis.set_major_formatter(PCT)
    ax.set_xlim(0, 160)
    ax.set_ylim(0, 62)
    ax.set_title("Taux marginal d'un salarié seul", fontsize=10, color=INK, loc="left")
    grille(ax)
    ax.legend(loc="lower right", fontsize=7.2)
    fin(fig, "ircsg_v08_paysbas", "Rijksoverheid (2024) ; OpenFisca-France ; calculs de l'auteur.",
        "Note : Pays-Bas, personne d'âge actif : 36,97 % (dont 27,65 points de cotisations) puis 49,50 %, plus le "
        "retrait du crédit général (6,63 %) et du crédit d'emploi (6,51 %) ; montée du crédit d'emploi sous 24 812 € "
        "non représentée. France : hors cotisations sociales.")


if __name__ == "__main__":
    for fn in (v01, v02, v04, v05, v06, v07, v08):
        fn()
