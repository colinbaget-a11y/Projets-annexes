"""Figure de la note courte « système efficace » : ircsg_e01_systeme.

Lancer depuis fiscalite/ : python3 ir_csg/figures_efficace.py ; FIG_NU=1 python3 ir_csg/figures_efficace.py
"""
import sys
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE), str(HERE.parent)]
import systeme_efficace as se  # noqa: E402
from graphiques import INK, PCT, fin, grille, plt  # noqa: E402

STYLE = {"auj": dict(color="#1a1a1a", lw=1.3, ls="-", label="Aujourd'hui"),
         "B": dict(color="#0072B2", lw=2.3, ls="-", label="Système proposé"),
         "A": dict(color="#E69F00", lw=1.6, ls="--", label="Variante sans franchise (taux unique de 15 %)")}
PROFILS = [("seul", "Salarié seul"), ("couple_2enf", "Couple salarié, deux enfants"), ("retraite_seul", "Retraité seul")]
CT = se.CT
PAR = {k: dict(t=se.cale_systeme(**se.SYSTEMES[k]), **se.SYSTEMES[k]) for k in ("A", "B")}


def lisse(a):
    return pd.Series(a).rolling(5, center=True, min_periods=1).median().values


def courbe(profil, cle):
    g = CT[CT.profil == profil].sort_values("brut")
    if cle == "auj":
        t, t1 = g.actuel.values, g.actuel_plus.values
    else:
        t, t1 = se.ct_systeme(**PAR[cle])[g.index], se.ct_systeme(**PAR[cle], plus=True)[g.index]
    mg = 100 * (t1 - t) / 1000
    return g.brut.values, 100 * t / g.brut.values, lisse(mg)


fig, axs = plt.subplots(3, 2, figsize=(9.4, 7.0), sharex=True)
for ligne, (prof, lab) in enumerate(PROFILS):
    a1, a2 = axs[ligne]
    for cle in ("auj", "A", "B"):
        z, moy, mg = courbe(prof, cle)
        a1.plot(z / 1e3, moy, **STYLE[cle])
        a2.plot(z / 1e3, mg if prof != "retraite_seul" or cle != "auj" else
                [m if m < 60 else float("nan") for m in mg], **{k: v for k, v in STYLE[cle].items() if k != "label"})
    for ax, t in ((a1, f"{lab} : taux moyen"), (a2, f"{lab} : taux marginal")):
        ax.set_xlim(0, 150)
        ax.yaxis.set_major_formatter(PCT)
        ax.set_title(t, fontsize=9, color=INK, loc="left")
        grille(ax)
    a1.set_ylim(-12, 40)
    a2.set_ylim(0, 50)
for ax in axs[-1]:
    ax.set_xlabel("Revenu brut annuel du foyer (k€)")
axs[0][0].legend(loc="lower right", fontsize=7, frameon=True)
fig.subplots_adjust(wspace=0.18, hspace=0.32)
tb = PAR["B"]["t"]
f = lambda u: f"{100 * u:.1f}".replace(".", ",")  # noqa: E731
fin(fig, "ircsg_e01_systeme", "OpenFisca-France 176.1 (législation des revenus 2024) ; calculs de l'auteur.",
    f"Note : IR + CSG + CRDS en % du revenu brut. Système proposé : {f(tb)} % sur les revenus du travail au-delà de "
    f"10 000 € par actif, {f(tb + 0.05)} % sur les pensions et les allocations chômage dès le premier euro, crédit de "
    f"1 500 € par enfant versé même sans impôt (taux moyen négatif quand le crédit dépasse l'impôt) ; revenu après "
    f"cotisations, sans niche ; même recette qu'aujourd'hui. Couple : revenus partagés 60/40. Taux marginal lissé "
    f"sur 2 000 € ; les sauts de CSG des retraités d'aujourd'hui (plus de 60 %) ne sont pas tracés.")
