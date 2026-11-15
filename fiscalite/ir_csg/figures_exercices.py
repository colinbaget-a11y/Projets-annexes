"""Figures des exercices (ircsg_x01 à ircsg_x05).

Lancer depuis fiscalite/ : python3 ir_csg/figures_exercices.py ; FIG_NU=1 python3 ir_csg/figures_exercices.py
"""
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE), str(HERE.parent)]
import exercices as ex  # noqa: E402
from graphiques import BLEU, GRIS, INK, MUTED, OCRE, PCT, fin, grille, plt  # noqa: E402

BRIQUE = "#993333"
SRC = "OpenFisca-France 176.1 (législation des revenus 2024) ; DGFiP, IRCOM revenus 2024 ; calculs de l'auteur."
RES = ex.resultats()
ETAPES = [("Exercice 1 : harmonisation", RES["ex1"], OCRE), ("Exercice 2 : aplanissement", RES["ex2"], BLEU),
          ("Exercice 3 : perte sèche minimale", RES["ex3"], BRIQUE)]
CT = ex.CT
NOTE_COMMUNE = ("Impôt individuel sur le revenu après cotisations, franchise de 6 000 € par enfant déduite du revenu "
                "du parent qui gagne le plus ; même recette qu'aujourd'hui.")


def courbe(profil, T=None):
    g = CT[CT.profil == profil].sort_values("brut")
    if T is None:
        return g.brut.values, g.actuel.values, ((g.actuel_plus - g.actuel) / 1000).values
    n, n1 = ex.cas_types(T)[g.index], ex.cas_types(T, plus=True)[g.index]
    return g.brut.values, n, (n1 - n) / 1000


def axes(a1, a2, xmax=200, ymoy=40, ymarg=55):
    for ax, t in ((a1, "Taux moyen : part du revenu payée"), (a2, "Taux marginal : impôt sur 1 000 € de plus")):
        ax.set_xlim(0, xmax)
        ax.set_xlabel("Revenu brut annuel du foyer (k€)")
        ax.yaxis.set_major_formatter(PCT)
        ax.set_title(t, fontsize=10, color=INK, loc="left")
        grille(ax)
    a1.set_ylim(0, ymoy)
    a2.set_ylim(0, ymarg)


def compare(nom_fig, etape, col, titre_note):
    """Aujourd'hui (gris) et l'exercice (couleur), pour une personne seule et un couple avec deux enfants."""
    nom, (tm, T), _ = etape
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(9.4, 3.8))
    for prof, lab, ls in (("seul", "personne seule", "-"), ("couple_2enf", "couple, deux enfants", "--")):
        z, t, mg = courbe(prof)
        a1.plot(z / 1e3, 100 * t / z, color=GRIS, lw=1.4, ls=ls, label=f"Aujourd'hui, {lab}")
        a2.plot(z / 1e3, np.where(mg < 0.6, 100 * mg, np.nan), color=GRIS, lw=1.2, ls=ls)
        z, t, mg = courbe(prof, T)
        a1.plot(z / 1e3, 100 * t / z, color=col, lw=2.2, ls=ls, label=f"{nom.split(' : ')[0]}, {lab}")
        a2.plot(z / 1e3, 100 * mg, color=col, lw=2.2, ls=ls)
    axes(a1, a2)
    a1.legend(loc="upper left", fontsize=7.2)
    fig.subplots_adjust(wspace=0.22)
    fin(fig, nom_fig, SRC, f"Note : salariés, IR + CSG + CRDS en % du salaire brut ; le couple partage ses revenus "
                           f"60/40. {titre_note} {NOTE_COMMUNE}")


def synthese():
    """Les quatre étapes pour une personne seule et pour un couple avec deux enfants."""
    fig, axs = plt.subplots(2, 2, figsize=(9.4, 6.6), sharex=True)
    for ligne, (prof, lab) in enumerate((("seul", "Personne seule"), ("couple_2enf", "Couple, deux enfants (60/40)"))):
        a1, a2 = axs[ligne]
        z, t, mg = courbe(prof)
        a1.plot(z / 1e3, 100 * t / z, color=GRIS, lw=1.8, label="Aujourd'hui")
        a2.plot(z / 1e3, np.where(mg < 0.6, 100 * mg, np.nan), color=GRIS, lw=1.6)
        for nom, (tm, T), col in ETAPES:
            z, t, mg = courbe(prof, T)
            a1.plot(z / 1e3, 100 * t / z, color=col, lw=1.8, label=nom)
            a2.plot(z / 1e3, 100 * mg, color=col, lw=1.8)
        for ax, t_ in ((a1, f"{lab} : taux moyen"), (a2, f"{lab} : taux marginal")):
            ax.set_xlim(0, 200)
            ax.yaxis.set_major_formatter(PCT)
            ax.set_title(t_, fontsize=9.5, color=INK, loc="left")
            grille(ax)
        a1.set_ylim(0, 40)
        a2.set_ylim(0, 55)
    for ax in axs[1]:
        ax.set_xlabel("Revenu brut annuel du foyer (k€)")
    axs[0, 0].legend(loc="upper left", fontsize=7)
    fig.subplots_adjust(wspace=0.2, hspace=0.25)
    fin(fig, "ircsg_x04_synthese", SRC, "Note : salariés, IR + CSG + CRDS en % du salaire brut. " + NOTE_COMMUNE)


def deciles():
    fig, ax = plt.subplots(figsize=(9.4, 3.4))
    xs = np.arange(1, 11)
    for k, (nom, (tm, T), col) in enumerate(ETAPES):
        d = ex.v.deciles(ex.impot(T))
        ax.bar(xs + (k - 1) * 0.27, d.delta_eur, width=0.26, color=col, label=nom)
    ax.axhline(0, color=INK, lw=0.7)
    ax.set_xticks(xs)
    ax.set_xticklabels([f"D{i}" for i in xs], fontsize=8)
    ax.set_xlabel("Décile de foyers (revenu brut croissant)")
    ax.set_ylabel("€ par foyer et par an")
    ax.set_title("Variation de la charge moyenne par rapport à aujourd'hui (+ : paie plus)", fontsize=10, color=INK, loc="left")
    grille(ax)
    ax.legend(loc="upper left", fontsize=7.5)
    fin(fig, "ircsg_x05_deciles", "DGFiP, IRCOM et déclarations 2042, revenus 2024 ; CCSS ; calculs de l'auteur.",
        "Note : effet avant réactions, en moyenne par foyer fiscal ; foyers réels, niches comprises dans la charge "
        "actuelle. " + NOTE_COMMUNE)


if __name__ == "__main__":
    tau = RES["tau"]
    b2, b3 = RES["b2"], RES["b3"]
    f = lambda u: f"{100 * u:.1f}".replace(".", ",")  # noqa: E731
    compare("ircsg_x01_harmonisation", ETAPES[0], OCRE,
            f"Exercice 1 : tranches de l'IR des revenus 2024 (0, 11, 30, 41, 45 %) appliquées à chaque adulte, plus un "
            f"taux unique de {f(tau)} % sur tout le revenu.")
    compare("ircsg_x02_aplanissement", ETAPES[1], BLEU,
            f"Exercice 2 : taux marginal de {f(b2.t0)} % au premier euro, {f(b2.tb)} % à 20 000 €, {f(b2.t1)} % à "
            f"{b2.z1/1e3:.0f} 000 €, 50 % à {b2.z2/1e3:.0f} 000 € par adulte, en ligne droite entre ces seuils.")
    compare("ircsg_x03_perte_seche", ETAPES[2], BRIQUE,
            f"Exercice 3 : taux marginal de {f(b3.t0)} % au premier euro, {f(b3.tb)} % à 20 000 €, {f(b3.t1)} % à "
            f"{b3.z1/1e3:.0f} 000 €, 50 % à {b3.z2/1e3:.0f} 000 € par adulte, en ligne droite entre ces seuils.")
    synthese()
    deciles()
