"""Deux figures nouvelles proposées pour la note (v5) :
- g12_travailler_plus : part d'un supplément de revenu prélevée par l'impôt (IR, CSG, CRDS aujourd'hui ; nouvel impôt
  demain), pour une promotion, une progression de carrière et la reprise d'un mi-temps par le second conjoint ;
- g13_machine : économie d'impôt année par année pour une machine de 500 000 € (amortissement linéaire sur 7 ans,
  déduction de 50 %, déduction intégrale ; taux de 25 %, entreprise bénéficiaire chaque année).
Sources : sorties/ircsg4.json (julie.progressions, second_conjoint) ; calcul direct pour la machine.
"""
import json
import sys
from pathlib import Path

import numpy as np

D = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(D))
from charte import AUJ, PROP, NAIF, ENCRE, ENCRE2, PLEINE, plt, axes, sauver, _fr  # noqa: E402

J = json.loads((D / "sorties" / "ircsg4.json").read_text(encoding="utf-8"))
P, SC = J["julie"]["progressions"], J["second_conjoint"]

# ------------------------------------------------------------------ g12
CAS = [("Promotion de 2 à 3 SMIC\n(+1 600 € par mois)", P["2.0_3.0"]["prelevement_aujourdhui_pct"],
        P["2.0_3.0"]["prelevement_demain_pct"]),
       ("Progression de 1,5 à 2 SMIC\n(+800 € par mois)", P["1.5_2.0"]["prelevement_aujourdhui_pct"],
        P["1.5_2.0"]["prelevement_demain_pct"]),
       ("Le conjoint reprend un mi-temps\nau SMIC (+900 € brut par mois)", SC["aujourdhui_pct"], SC["demain_pct"])]
fig, ax = plt.subplots(figsize=(PLEINE, 2.3))
y = np.arange(len(CAS))[::-1]
h = 0.36
for yy, (lab, a, b) in zip(y, CAS):
    ax.barh(yy + h / 2, a, height=h, color=AUJ, zorder=2)
    ax.barh(yy - h / 2, b, height=h, color=PROP, zorder=2)
    ax.text(a + 0.6, yy + h / 2, _fr(a, 0) + " %", va="center", fontsize=7.5, color=ENCRE2)
    ax.text(b + 0.6, yy - h / 2, _fr(b, 0) + " %", va="center", fontsize=7.5, color=PROP, fontweight="bold")
ax.set_yticks(y)
ax.set_yticklabels([c[0] for c in CAS], fontsize=7.4)
ax.set_xlim(0, 42)
ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v:.0f} %"))
ax.set_xlabel("Part du revenu supplémentaire prélevée par l'impôt sur le revenu", fontsize=7.4)
from matplotlib.patches import Patch  # noqa: E402
ax.legend(handles=[Patch(color=AUJ, label="Aujourd'hui (impôt sur le revenu, CSG, CRDS)"),
                   Patch(color=PROP, label="Avec le nouvel impôt")], fontsize=7, loc="lower right")
axes(ax, grille="x")
ax.spines["left"].set_visible(False)
ax.tick_params(axis="y", length=0)
sauver(fig, "g12_travailler_plus",
       "OpenFisca-France 176.1 (droit des revenus 2025) ; calculs des auteurs (note8p/calculs/ircsg4_cas.py).",
       "Salariée seule sans enfant pour les deux progressions (part du revenu supplémentaire après cotisations) ; couple"
       " avec deux enfants dont l'un gagne 45 000 € brut pour la reprise d'activité (part du salaire brut du mi-temps)."
       " Nouvel impôt : barème proposé, forfait de 500 € par salaire, franchise de 6 000 € par enfant.")

# ------------------------------------------------------------------ g13
PRIX, N_ANS, TAUX = 500_000.0, 7, 0.25
lin = np.full(N_ANS, PRIX / N_ANS)
moit = np.r_[PRIX / 2 + PRIX / 2 / N_ANS, np.full(N_ANS - 1, PRIX / 2 / N_ANS)]
tout = np.r_[PRIX, np.zeros(N_ANS - 1)]
REG = [("Aujourd'hui : amortissement sur 7 ans", lin, AUJ), ("Déduction immédiate de 50 %", moit, NAIF),
       ("Déduction immédiate de 100 %", tout, PROP)]
fig, ax = plt.subplots(figsize=(PLEINE, 2.5))
x = np.arange(1, N_ANS + 1)
w = 0.27
for i, (lab, ded, col) in enumerate(REG):
    eco = TAUX * ded / 1000
    ax.bar(x + (i - 1) * w, eco, width=w, color=col, zorder=2, label=f"{lab} (total : {_fr(eco.sum(), 0)} k€)")
    ax.text(1 + (i - 1) * w, eco[0] + 2, _fr(eco[0], 0), ha="center", fontsize=7, color=ENCRE2)
ax.set_xticks(x)
ax.set_xticklabels([f"Année {k}" for k in x], fontsize=7.4)
ax.set_ylabel("Économie d'impôt, k€", fontsize=7.4)
ax.set_ylim(0, 140)
ax.legend(fontsize=7, loc="upper right")
axes(ax)
sauver(fig, "g13_machine", "calculs des auteurs.",
       "Machine de 500 000 € achetée en début d'année 1 par une PME soumise au taux normal de 25 %, bénéficiaire chaque"
       " année ; amortissement linéaire sur 7 ans sans prorata ; déduction de 50 % : la moitié du prix l'année de l'achat,"
       " le reste amorti normalement. L'économie d'impôt totale est la même dans les trois cas (125 000 €) : seule sa"
       " date change.")
print("g12 :", [(c[0].split(chr(10))[0], round(c[1], 1), round(c[2], 1)) for c in CAS], "; g13 total", TAUX * PRIX)
