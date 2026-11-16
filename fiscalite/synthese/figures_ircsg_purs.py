"""Figures de la partie IR-CSG de la note fusionnée (méthode v2, sorties/architectures_ircsg.json).

ircsg_p01_baremes : taux moyen et taux marginal de trois cas-types OpenFisca (personne seule salariée, couple avec
deux enfants aux revenus partagés 60/40, retraité seul), aujourd'hui, avec le barème neutre (assiette large, même
barème pour tous, le plus proche de la charge d'aujourd'hui) et avec la proposition (franchise d'activité de
4 000 €, 6 000 € par enfant, petites pensions exonérées).
ircsg_p02_frontiere : gain d'efficacité réel et part des foyers qui perdent plus de 500 €, pour chaque architecture
et le long du chemin du barème neutre à l'optimum.

Lancer depuis fiscalite/ : FIG_NU=1 python3 synthese/figures_ircsg_purs.py
"""
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE), str(HERE.parent)]
import modele_purs as M  # noqa: E402
from graphiques import INK, PCT, fin, grille, plt  # noqa: E402

ex = M.ex
J = json.loads((HERE / "sorties/architectures_ircsg.json").read_text(encoding="utf-8"))
BN = J["neutre"]
PROP = J["propositions"]["4000"]
BP, OP = PROP["bareme"], PROP["options"]


def bareme(b):
    t0, tb, z1, t1, z2 = b
    return ex.bareme_lineaire([0, 20e3, z1, z2], [t0, tb, t1, 0.50])


SCH = {"neutre": (bareme(BN), dict(M.OPT0)), "prop": (bareme(BP), OP)}
STYLE = {"auj": dict(color="#1a1a1a", lw=1.3, ls="-"),
         "neutre": dict(color="#0072B2", lw=2.2, ls="--"),
         "prop": dict(color="#009E73", lw=2.6, ls="-")}
NOMS = {"auj": "Aujourd'hui", "neutre": "Barème neutre", "prop": "Proposition"}
PROFILS = [("seul", "Personne seule salariée"), ("couple_2enf", "Couple, deux enfants, revenus partagés 60/40"),
           ("retraite_seul", "Retraité seul")]
CT = M.CT


def lisse(a):
    return pd.Series(a).rolling(5, center=True, min_periods=1).median().values


def courbe(profil, cle):
    g = CT[CT.profil == profil].sort_values("brut")
    b = g.brut.values
    if cle == "auj":
        t, t1 = g.actuel.values, g.actuel_plus.values
        mg = (t1 - t) / 1000
    else:
        (tm, T), o = SCH[cle]
        t = np.array([M.cas_type(tm, T, o, profil, z) for z in b]) + g.actuel.values
        mg = np.gradient(t, b)
    return b, 100 * t / b, lisse(100 * mg)


def main():
    fig, axs = plt.subplots(3, 2, figsize=(9.4, 8.4), sharex=True)
    for ligne, (prof, lab) in enumerate(PROFILS):
        a1, a2 = axs[ligne]
        for cle in ("auj", "neutre", "prop"):
            z, moy, mg = courbe(prof, cle)
            a1.plot(z / 1e3, moy, label=NOMS[cle], **STYLE[cle])
            a2.plot(z / 1e3, mg, **STYLE[cle])
        for ax, t in ((a1, f"{lab} : taux moyen"), (a2, f"{lab} : taux marginal")):
            ax.set_xlim(0, 200)
            ax.yaxis.set_major_formatter(PCT)
            ax.set_title(t, fontsize=9, color=INK, loc="left")
            grille(ax)
        a1.set_ylim(0, 40)
        a2.set_ylim(0, 55)
    for ax in axs[-1]:
        ax.set_xlabel("Revenu brut annuel du foyer (k€)")
    axs[0][0].legend(loc="upper left", fontsize=7.2, frameon=True)
    fig.subplots_adjust(wspace=0.18, hspace=0.3)
    f = lambda u: f"{100 * u:.1f}".replace(".", ",").replace(",0", "")  # noqa: E731
    note = (f"Note : impôt individuel sur le revenu après cotisations, même barème pour tous, même recette qu'aujourd'hui "
            f"(220 Md€). Taux marginal par adulte en ligne droite entre les seuils. Barème neutre (le plus proche de ce "
            f"que chaque foyer paie aujourd'hui) : {f(BN[0])} % au premier euro, {f(BN[1])} % à 20 000 €, {f(BN[3])} % à "
            f"{BN[2]/1e3:.0f} 000 €, 50 % à {BN[4]/1e3:.0f} 000 €. Proposition : franchise de 4 000 € par adulte sur les "
            f"revenus d'activité, 6 000 € par enfant, pensions exonérées jusqu'à 12 500 € (puis de moins en moins jusqu'à "
            f"25 000 €) ; {f(BP[0])} % au premier euro imposé, {f(BP[1])} % à 20 000 €, {f(BP[3])} % à "
            f"{BP[2]/1e3:.0f} 000 €, 50 % à {BP[4]/1e3:.0f} 000 €. Cas-types sans niche : IR + CSG + CRDS (et Casa "
            f"pour le retraité) en % du revenu brut ; taux marginal sur 1 000 € de plus, lissé sur 2 000 €.")
    fin(fig, "ircsg_p01_baremes",
        "OpenFisca-France (législation des revenus 2024) ; DGFiP, IRCOM revenus 2024 ; calculs de l'auteur "
        "(synthese/modele_purs.py, architectures_ircsg.py).", note)


def frontiere():
    fig, ax = plt.subplots(figsize=(8.6, 4.6))
    ch = J["chemin"]
    x = [c["perdants500"] for c in ch]
    ax.plot(x, [-c["v2_central"] for c in ch], color="#999999", lw=1.4, ls=":", zorder=1)
    ax.fill_between(x, [-c["v2_bas"] for c in ch], [-c["v2_haut"] for c in ch], color="#DDDDDD", alpha=0.5, zorder=0)
    pts = [("Aujourd'hui", 0.0, (0.0, 0.0, 0.0), "#1a1a1a"),
           ("Barème neutre", J["architectures"][0]["perdants500"], J["architectures"][0], "#0072B2"),
           ("+ franchise d'activité 4 000 €", J["architectures"][6]["perdants500"], J["architectures"][6], "#56B4E9"),
           ("+ franchise d'activité 8 000 €", J["architectures"][7]["perdants500"], J["architectures"][7], "#56B4E9"),
           ("Proposition (franchise 4 000 €)", PROP["perdants500"], PROP, "#009E73"),
           ("Optimum d'efficacité", J["optimum_r"]["perdants500"], J["optimum_r"], "#CC79A7"),
           ("Gain atteignable", J["atteignable"]["perdants500"], J["atteignable"], "#CC79A7")]
    for nom, xx, r, col in pts:
        if isinstance(r, tuple):
            y, lo, hi = r
        else:
            y, lo, hi = -r["v2_central"], -r["v2_bas"], -r["v2_haut"]
        ax.errorbar([xx], [y], yerr=[[y - lo], [hi - y]], fmt="o", color=col, ms=6, capsize=3, lw=1.2, zorder=3)
        off = {"Aujourd'hui": (8, 6, "left"), "Barème neutre": (-8, -4, "right"),
               "+ franchise d'activité 4 000 €": (8, -9, "left"), "+ franchise d'activité 8 000 €": (8, 7, "left"),
               "Proposition (franchise 4 000 €)": (-8, 12, "right"), "Gain atteignable": (-8, 8, "right"),
               "Optimum d'efficacité": (8, 0, "left")}[nom]
        ax.annotate(nom, (xx, y), xytext=off[:2], textcoords="offset points", fontsize=7.6, color=col,
                    va="center", ha=off[2])
    ax.set_xlabel("Foyers dont l'impôt augmente de plus de 500 € par an (%)")
    ax.set_ylabel("Gain d'efficacité (Md€ par an)")
    ax.set_xlim(-2, 70)
    ax.set_ylim(0, 19)
    grille(ax)
    note = ("Note : gain d'efficacité = baisse de la perte sèche sur l'activité réelle par rapport à aujourd'hui "
            "(heures, effort, reprise d'emploi), à recette égale ; point : hypothèses centrales ; barre et zone grise : "
            "hypothèses basses et hautes. La réaction du revenu déclaré (forme, date, société) n'y est pas comptée. "
            "Ligne pointillée : barèmes intermédiaires entre le barème neutre et l'optimum. Gain atteignable : meilleur "
            "barème simple, franchise d'activité comprise.")
    fin(fig, "ircsg_p02_frontiere", "Calculs de l'auteur (synthese/architectures_ircsg.py) ; élasticités : "
        "cours/elasticites-france.tex.", note)


if __name__ == "__main__":
    main()
    frontiere()
