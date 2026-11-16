"""Figure de la partie IR-CSG de la note fusionnée : barème de référence et barème progressif (modèle des foyers purs).

ircsg_p01_baremes : taux moyen et taux marginal de trois cas-types OpenFisca (personne seule salariée, couple avec
deux enfants aux revenus partagés 60/40, retraité seul), aujourd'hui, avec le barème de référence (assiette large,
même barème pour tous, ni franchise ni aide familiale) et avec le barème progressif (même assiette, répartition par
décile proche d'aujourd'hui). Barèmes : sorties/perte_seche_ircsg_purs.json.

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
J = json.loads((HERE / "sorties/perte_seche_ircsg_purs.json").read_text(encoding="utf-8"))
REF = J["ref"]
PROG = next(r for r in J["res"] if r["nom"].startswith("Progressivité"))


def bareme(b):
    t0, tb, z1, t1, z2 = b
    return ex.bareme_lineaire([0, 20e3, z1, z2], [t0, tb, t1, 0.50])


def cale_t1(t0, tb, z1, z2, o):
    lo, hi = 0.0, 0.50
    for _ in range(32):
        t1 = (lo + hi) / 2
        lo, hi = (t1, hi) if M.recette(*bareme((t0, tb, z1, t1, z2)), o) < M.CIBLE else (lo, t1)
    return (lo + hi) / 2


O = dict(M.OPT0)
B_PROG = (0.05, 0.13, 30e3, cale_t1(0.05, 0.13, 30e3, 250e3, O), 250e3)
SCH = {"ref": bareme(REF), "prog": bareme(B_PROG)}
STYLE = {"auj": dict(color="#1a1a1a", lw=1.3, ls="-"),
         "ref": dict(color="#CC79A7", lw=2.4, ls="--"),
         "prog": dict(color="#0072B2", lw=2.2, ls="-")}
NOMS = {"auj": "Aujourd'hui", "ref": "Référence (perte sèche minimale)", "prog": "Barème progressif"}
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
        tm, T = SCH[cle]
        t = np.array([M.cas_type(tm, T, O, profil, z) for z in b]) + g.actuel.values
        mg = np.gradient(t, b)
    return b, 100 * t / b, lisse(100 * mg)


def main():
    fig, axs = plt.subplots(3, 2, figsize=(9.4, 8.4), sharex=True)
    for ligne, (prof, lab) in enumerate(PROFILS):
        a1, a2 = axs[ligne]
        for cle in ("auj", "ref", "prog"):
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
    note = (f"Note : impôt individuel sur le revenu après cotisations, même barème pour tous, sans franchise ni aide "
            f"familiale, même recette qu'aujourd'hui (220 Md€). Taux marginal par adulte en ligne droite entre les "
            f"seuils : référence {f(REF[0])} % au premier euro, {f(REF[1])} % à 20 000 €, {f(REF[3])} % à "
            f"{REF[2]/1e3:.0f} 000 €, 50 % à {REF[4]/1e3:.0f} 000 € ; barème progressif {f(B_PROG[0])} %, "
            f"{f(B_PROG[1])} % à 20 000 €, {f(B_PROG[3])} % à {B_PROG[2]/1e3:.0f} 000 €, 50 % à "
            f"{B_PROG[4]/1e3:.0f} 000 €. Cas-types sans niche : IR + CSG + CRDS (et Casa pour le retraité) en % du "
            f"revenu brut ; taux marginal sur 1 000 € de plus, lissé sur 2 000 € (médiane glissante).")
    fin(fig, "ircsg_p01_baremes",
        "OpenFisca-France (législation des revenus 2024) ; DGFiP, IRCOM revenus 2024 ; calculs de l'auteur "
        "(synthese/modele_purs.py).", note)


if __name__ == "__main__":
    main()
