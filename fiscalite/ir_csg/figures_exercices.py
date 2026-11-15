"""Figures des exercices (ircsg_x01 à ircsg_x05).

Lancer depuis fiscalite/ : python3 ir_csg/figures_exercices.py ; FIG_NU=1 python3 ir_csg/figures_exercices.py

Lisibilité : une palette distinguable par les daltoniens (Okabe et Ito) et un style de trait par étape ; un
profil de foyer par ligne de panneaux ; le taux marginal est lissé par une médiane glissante sur 2 000 € pour
effacer les pointes isolées (seuil de recouvrement de l'IR, arrondis), sans toucher aux marches.
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE), str(HERE.parent)]
import exercices as ex  # noqa: E402
from graphiques import INK, PCT, fin, grille, plt  # noqa: E402

# palette d'Okabe et Ito : noir, orange, bleu, violet-rose
STYLE = {"auj": dict(color="#1a1a1a", lw=1.3, ls="-"),
         "ex1": dict(color="#E69F00", lw=2.2, ls="-."),
         "ex2": dict(color="#0072B2", lw=2.2, ls="-"),
         "ex3": dict(color="#CC79A7", lw=2.2, ls="--")}
NOMS = {"auj": "Aujourd'hui", "ex1": "Exercice 1 : harmonisation", "ex2": "Exercice 2 : aplanissement",
        "ex3": "Exercice 3 : perte sèche minimale"}
SRC = "OpenFisca-France 176.1 (législation des revenus 2024) ; DGFiP, IRCOM revenus 2024 ; calculs de l'auteur."
RES = ex.resultats()
T_EX = {"ex1": RES["ex1"][1], "ex2": RES["ex2"][1], "ex3": RES["ex3"][1]}
CT = ex.CT
PROFILS = [("seul", "Personne seule"), ("couple_2enf", "Couple, deux enfants, revenus partagés 60/40"),
           ("couple_2enf_mono", "Couple, deux enfants, un seul revenu")]
NOTE_COMMUNE = ("Impôt individuel sur le revenu après cotisations, franchise de 6 000 € par enfant déduite du revenu "
                "du parent qui gagne le plus ; même recette qu'aujourd'hui. Salariés, IR + CSG + CRDS en % du salaire "
                "brut ; taux marginal sur 1 000 € de plus, lissé sur 2 000 € (médiane glissante) pour effacer les "
                "pointes isolées. Aujourd'hui, le taux marginal du couple monte à 21 % vers 60 000 € puis retombe à "
                "18 % entre 86 000 et 95 000 € : en dessous, la sortie progressive de la décote alourdit l'IR.")


def lisse(a):
    return pd.Series(a).rolling(5, center=True, min_periods=1).median().values


def courbe(profil, cle):
    g = CT[CT.profil == profil].sort_values("brut")
    if cle == "auj":
        t, t1 = g.actuel.values, g.actuel_plus.values
    else:
        t, t1 = ex.cas_types(T_EX[cle])[g.index], ex.cas_types(T_EX[cle], plus=True)[g.index]
    return g.brut.values, 100 * t / g.brut.values, lisse(100 * (t1 - t) / 1000)


def panneaux(axs, profils, cles, legende=True):
    for ligne, (prof, lab) in enumerate(profils):
        a1, a2 = axs[ligne]
        for cle in cles:
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
    if legende:
        axs[0][0].legend(loc="upper left", fontsize=7.2, frameon=True)


def compare(nom_fig, cle, note):
    fig, axs = plt.subplots(3, 2, figsize=(9.4, 8.4), sharex=True)
    panneaux(axs, PROFILS, ["auj", cle])
    fig.subplots_adjust(wspace=0.18, hspace=0.3)
    fin(fig, nom_fig, SRC, f"Note : {note} {NOTE_COMMUNE}")


def synthese():
    fig, axs = plt.subplots(2, 2, figsize=(9.4, 6.4), sharex=True)
    panneaux(axs, PROFILS[:2], ["auj", "ex1", "ex2", "ex3"], legende=False)
    h, l = axs[0][0].get_legend_handles_labels()
    fig.legend(h, l, loc="upper center", ncol=4, fontsize=7.6, frameon=False, bbox_to_anchor=(0.5, 1.0))
    fig.subplots_adjust(wspace=0.18, hspace=0.3, top=0.9)
    fin(fig, "ircsg_x04_synthese", SRC, "Note : " + NOTE_COMMUNE)


def deciles():
    fig, ax = plt.subplots(figsize=(9.4, 3.6))
    xs = np.arange(1, 11)
    for k, cle in enumerate(("ex1", "ex2", "ex3")):
        d = ex.v.deciles(ex.impot(T_EX[cle]))
        ax.bar(xs + (k - 1) * 0.27, d.delta_eur, width=0.26, color=STYLE[cle]["color"], label=NOMS[cle],
               edgecolor="white", lw=0.3, hatch=["", "", "//"][k])
    ax.axhline(0, color=INK, lw=0.7)
    ax.set_xticks(xs)
    ax.set_xticklabels([f"D{i}" for i in xs], fontsize=8)
    ax.set_xlabel("Décile de foyers (revenu brut croissant)")
    ax.set_ylabel("€ par foyer et par an")
    ax.set_title("Variation de la charge moyenne par rapport à aujourd'hui (+ : paie plus)", fontsize=10, color=INK, loc="left")
    grille(ax)
    ax.legend(loc="lower left", fontsize=7.5)
    fin(fig, "ircsg_x05_deciles", "DGFiP, IRCOM et déclarations 2042, revenus 2024 ; CCSS ; calculs de l'auteur.",
        "Note : effet avant réactions, en moyenne par foyer fiscal ; foyers réels, niches comprises dans la charge "
        "actuelle. Impôt individuel sur le revenu après cotisations, franchise de 6 000 € par enfant ; même recette.")


if __name__ == "__main__":
    tau, b2, b3 = RES["tau"], RES["b2"], RES["b3"]
    f = lambda u: f"{100 * u:.1f}".replace(".", ",")  # noqa: E731
    compare("ircsg_x01_harmonisation", "ex1",
            f"exercice 1 : tranches de l'IR des revenus 2024 (0, 11, 30, 41, 45 %) appliquées à chaque adulte, plus un "
            f"taux unique de {f(tau)} % sur tout le revenu après la franchise pour enfants.")
    compare("ircsg_x02_aplanissement", "ex2",
            f"exercice 2 : taux marginal de {f(b2.t0)} % au premier euro, {f(b2.tb)} % à 20 000 €, {f(b2.t1)} % à "
            f"{b2.z1/1e3:.0f} 000 €, 50 % à {b2.z2/1e3:.0f} 000 € par adulte (revenu après cotisations), en ligne droite "
            f"entre ces seuils.")
    compare("ircsg_x03_perte_seche", "ex3",
            f"exercice 3 : taux marginal de {f(b3.t0)} % au premier euro, {f(b3.tb)} % à 20 000 €, {f(b3.t1)} % à "
            f"{b3.z1/1e3:.0f} 000 €, 50 % à {b3.z2/1e3:.0f} 000 € par adulte (revenu après cotisations), en ligne droite "
            f"entre ces seuils.")
    synthese()
    deciles()
