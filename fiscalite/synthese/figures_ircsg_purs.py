"""Figures de la partie IR-CSG de la note fusionnée (méthode v2 ; sorties/etapes_ircsg.json, architectures_ircsg.json).

ircsg_p01_marches : taux marginal d'une personne seule salariée et d'un retraité seul (cas-types OpenFisca sans
niche), aujourd'hui, à l'étape 1 (barème de l'IR gardé, CSG-CRDS en taux proportionnel), à l'étape 2 (barème
neutre, sans marche) et avec la proposition.
ircsg_p02_frontiere : gain d'efficacité et part des foyers qui perdent plus de 500 €, étape par étape, et chemin
du barème neutre à l'optimum.
ircsg_p03_qui_paie : variation de l'impôt par type de foyer (€ par an), étapes 1 et 2 et proposition.

Couleurs : palette des figures de la note (bleu #1d4ba6, ocre #c79100, brique #993333, validée) ; aujourd'hui en
encre ; l'optimum, simple étalon, en gris. Lancer depuis fiscalite/ :
python3 synthese/figures_ircsg_purs.py && FIG_NU=1 python3 synthese/figures_ircsg_purs.py
"""
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE), str(HERE.parent)]
import modele_purs as M  # noqa: E402
from graphiques import ECH_TXT, PCT, fin, plt  # noqa: E402

ex = M.ex
E = json.loads((HERE / "sorties/etapes_ircsg.json").read_text(encoding="utf-8"))
J = json.loads((HERE / "sorties/architectures_ircsg.json").read_text(encoding="utf-8"))
INK, INK2, GRIS, GRILLE = "#0b0b0b", "#52514e", "#8a8984", "#e4e3df"
BLEU, ORANGE, AQUA = "#c79100", "#993333", "#1d4ba6"   # étape 2 ocre, étape 1 brique, proposition bleu (palette des autres figures)
SRC = ("OpenFisca-France (législation des revenus 2024) ; DGFiP, IRCOM revenus 2024 ; calculs de l'auteur "
       "(synthese/modele_purs.py, architectures_ircsg.py, etapes_ircsg.py).")


def bareme(b):
    t0, tb, z1, t1, z2 = b
    return ex.bareme_lineaire([0, 20e3, z1, z2], [t0, tb, t1, 0.50])


P4 = J["propositions"]["4000"]
SCH = {"e1": (ex.bareme_empile(E["tau"]), dict(M.OPT0)), "e2": (bareme(J["neutre"]), dict(M.OPT0)),
       "prop": (bareme(P4["bareme"]), P4["options"])}
STYLE = {"auj": dict(color=INK, lw=1.3, ls="-", label="Aujourd'hui"),
         "e1": dict(color=ORANGE, lw=1.6, ls=(0, (4, 2)), label="Étape 1"),
         "e2": dict(color=BLEU, lw=1.8, ls="-", label="Étape 2"),
         "prop": dict(color=AQUA, lw=2.2, ls="-", label="Proposition")}


def style_axes(ax):
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color(GRIS)
    ax.tick_params(colors=INK2, labelsize=9 * ECH_TXT, length=3)
    ax.grid(axis="y", color=GRILLE, lw=0.6, zorder=0)
    ax.set_axisbelow(True)


def lisse(a):
    return pd.Series(a).rolling(5, center=True, min_periods=1).median().values


def marginal(profil, cle):
    g = M.CT[M.CT.profil == profil].sort_values("brut")
    b = g.brut.values
    if cle == "auj":
        return b, lisse(100 * (g.actuel_plus.values - g.actuel.values) / 1000)
    (tm, T), o = SCH[cle]
    t = np.array([M.cas_type(tm, T, o, profil, z) for z in b]) + g.actuel.values
    return b, lisse(100 * np.gradient(t, b))


def marches():
    fig, axs = plt.subplots(1, 2, figsize=(9.2, 4.0), sharey=True)
    for ax, (prof, titre) in zip(axs, (("seul", "Personne seule salariée"), ("retraite_seul", "Retraité seul"))):
        for cle in ("auj", "e1", "e2", "prop"):
            z, mg = marginal(prof, cle)
            ax.plot(z / 1e3, mg, **STYLE[cle], zorder=3 if cle == "prop" else 2)
        ax.set_xlim(0, 120)
        ax.set_ylim(0, 55)
        ax.yaxis.set_major_formatter(PCT)
        ax.set_title(titre, fontsize=10, color=INK, loc="left")
        ax.set_xlabel("Revenu brut annuel (k€)", fontsize=9.5, color=INK2)
        style_axes(ax)
    axs[0].set_ylabel("Taux marginal", fontsize=9.5, color=INK2)
    h, lab = axs[0].get_legend_handles_labels()
    fig.legend(h, lab, loc="upper center", ncol=4, fontsize=9.5 * ECH_TXT, frameon=False, bbox_to_anchor=(0.5, 1.02),
               handlelength=2.4, columnspacing=1.4)
    fig.subplots_adjust(wspace=0.08, top=0.83, bottom=0.15, left=0.09, right=0.98)
    t = f"{100 * E['tau']:.2f}".replace(".", ",")
    fin(fig, "ircsg_p01_marches", SRC,
        f"Note : prélèvement sur 1 000 € de revenu brut en plus (IR + CSG + CRDS, et Casa pour le retraité), cas-types "
        f"sans niche ; lissé sur 2 000 €. Étape 1 : barème de l'IR (0, 11, 30, 41, 45 %) appliqué à chaque adulte sur "
        f"le revenu après cotisations, CSG et CRDS remplacées par un taux unique de {t} %. Étape 2 : taux marginal en "
        f"ligne droite, le barème le plus proche de ce que chacun paie aujourd'hui. Proposition : franchise de 4 000 € "
        f"sur les revenus d'activité, pensions exonérées jusqu'à 12 500 € puis de moins en moins jusqu'à 25 000 € "
        f"(d'où le taux de 28 % du retraité dans cette zone).")


def frontiere():
    fig, ax = plt.subplots(figsize=(9.2, 4.2))
    ch = J["chemin"]
    ax.plot([c["perdants500"] for c in ch], [-c["v2_central"] for c in ch], color=GRIS, lw=1.2, ls=":", zorder=1)
    pts = [("Étape 1", E["etape1"], ORANGE, "o", "haut"), ("Étape 2", E["etape2"], BLEU, "o", "haut"),
           ("Étape 3", E["etape3"], BLEU, "s", "bas"), ("Proposition", E["proposition"], AQUA, "D", "haut"),
           ("Optimum (étalon)", E["atteignable"], GRIS, "o", "droite")]
    for nom, r, col, mk, pos in pts:
        x, y, lo, hi = r["perdants500"], -r["v2_central"], -r["v2_bas"], -r["v2_haut"]
        ax.errorbar([x], [y], yerr=[[y - lo], [hi - y]], fmt=mk, color=col, ms=5.5, capsize=2.5,
                    lw=1.1, mec="white", mew=0.8, zorder=3)
        if pos == "haut":
            ax.text(x, hi + 0.45, nom, fontsize=9.5, color=INK, ha="center", va="bottom")
        elif pos == "bas":
            ax.text(x, lo - 0.45, nom, fontsize=9.5, color=INK, ha="center", va="top")
        else:
            ax.annotate(nom, (x, y), xytext=(9, 0), textcoords="offset points", fontsize=9.5, color=INK, va="center")
    ax.annotate("barèmes de plus en plus plats", (42, 4.4), fontsize=9, color=INK2, ha="center", rotation=4)
    ax.set_xlim(0, 65)
    ax.set_ylim(0, 20)
    ax.set_xlabel("Foyers dont l'impôt augmente de plus de 500 € par an (%)", fontsize=9.5, color=INK2)
    ax.set_ylabel("Gain d'efficacité (Md€ par an)", fontsize=9.5, color=INK2)
    style_axes(ax)
    fig.subplots_adjust(bottom=0.16)
    fin(fig, "ircsg_p02_frontiere", SRC + " Élasticités : cours/elasticites-france.tex.",
        "Note : gain d'efficacité = baisse de la perte sèche sur l'activité réelle par rapport à aujourd'hui, à recette "
        "égale ; point : hypothèses centrales ; barre : hypothèses basses et hautes. La réaction du revenu déclaré "
        "n'est pas comptée. Pointillé : barèmes intermédiaires entre le barème sans marche et l'optimum, qui est le "
        "barème simple le plus efficace (franchise d'activité comprise).")


def qui_paie():
    types = [("seuls_actifs", "Personne seule active"), ("parents_isoles", "Parent isolé"),
             ("couples0_actifs", "Couple actif sans enfant"), ("couples2", "Couple avec deux enfants"),
             ("seuls_retraites", "Retraité seul"), ("couples0_retraites", "Couple de retraités")]
    series = [("etape1", "Étape 1", ORANGE), ("etape2", "Étape 2", BLEU), ("proposition", "Proposition", AQUA)]
    fig, ax = plt.subplots(figsize=(9.2, 4.2))
    y0 = np.arange(len(types))[::-1]
    h = 0.24
    for k, (cle, nom, col) in enumerate(series):
        v = [E[cle]["groupes"][t]["eur"] for t, _ in types]
        ax.barh(y0 + (1 - k) * (h + 0.03), v, height=h, color=col, label=nom, zorder=2)
    ax.axvline(0, color=INK2, lw=0.8, zorder=3)
    ax.set_yticks(y0)
    ax.set_yticklabels([n for _, n in types], fontsize=9.5 * ECH_TXT, color=INK)
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v:+,.0f}".replace(",", " ").replace("+0", "0")))
    ax.set_xlabel("Variation de l'impôt par foyer (€ par an ; positif : paie plus)", fontsize=9.5, color=INK2)
    style_axes(ax)
    ax.grid(axis="y", visible=False)
    ax.grid(axis="x", color=GRILLE, lw=0.6, zorder=0)
    ax.legend(loc="upper right", fontsize=9.5, frameon=False)
    fig.subplots_adjust(left=0.22, bottom=0.15, right=0.97)
    fin(fig, "ircsg_p03_qui_paie", SRC,
        "Note : moyenne par type de foyer, IR + CSG + CRDS, à recette égale. Étapes 1 et 2 : impôt individuel sans aide "
        "familiale. Proposition : franchise d'activité de 4 000 €, 6 000 € par enfant, petites pensions exonérées.")


if __name__ == "__main__":
    marches()
    frontiere()
    qui_paie()
