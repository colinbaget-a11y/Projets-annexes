"""Figure g7_tmei : taux marginal effectif d'imposition d'un équipement neuf financé par fonds propres, cinq
configurations, avec leur coût budgétaire. Lancer depuis fiscalite/ après note8p/calculs/is_reforme.py.
-> note8p/figures/g7_tmei.pdf, .png, _source.tex
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]           # note8p/
sys.path.insert(0, str(ROOT))
from charte import *  # noqa: E402,F401,F403
from charte import _fr  # noqa: E402

J = json.loads((ROOT / "sorties" / "is.json").read_text(encoding="utf-8"))
T, C = J["taux_effectifs"], J["comparaison"]

lignes = [  # (clé taux effectif, libellé, couleur, hachure, texte de coût)
    ("actuel", "Aujourd'hui (25 %)", AUJ, None, "référence"),
    ("taux23", "Taux normal à 23 %", NAIF, None,
     f"{_fr(C['taux23']['cout_permanent_2027'], 1)} Md€ par an, en permanence"),
    ("ded50", "Déduction immédiate de 50 %", NAIF, None,
     f"au plus {_fr(C['ded50']['cout_2028'], 1)} Md€ (2028), puis {_fr(C['ded50']['cout_permanent_2027'], 1)} Md€ par an"),
    ("combi23", "23 % + déduction de 50 %", PROP, None,
     f"au plus {_fr(C['combi23']['cout_2028'], 1)} Md€ (2028), puis {_fr(C['combi23']['cout_permanent_2027'], 1)} Md€ par an"),
    ("ded100", "Déduction intégrale (repère)", "white", "////",
     f"{_fr(C['ded100']['cout_2027'], 1)} Md€ la 1re année, puis {_fr(C['ded100']['cout_permanent_2027'], 1)} Md€ par an"),
]

fig, ax = plt.subplots(figsize=(PLEINE, 2.2))
n = len(lignes)
for i, (k, lab, col, hat, cout) in enumerate(lignes):
    y = n - 1 - i
    v = 100 * T[k]["tmei_fp"]
    ax.barh(y, v, height=0.62, color=col, edgecolor=(NAIF if hat else col), hatch=hat, lw=0.8, zorder=2)
    ax.text(max(v, 0) + 0.4, y, _fr(v) + " %", va="center", ha="left", fontsize=7.5, color=ENCRE,
            fontweight="bold" if k == "combi23" else "normal")
    ax.text(24.5, y, cout, va="center", ha="left", fontsize=7, color=ENCRE2)
ax.set_yticks(range(n))
ax.set_yticklabels([l[1] for l in lignes][::-1])
ax.set_xlim(0, 23)
ax.set_ylim(-0.6, n - 0.4)
ax.xaxis.set_major_formatter(pct)
ax.set_xticks([0, 5, 10, 15, 20])
axes(ax, grille="x")
ax.spines["left"].set_visible(False)
ax.tick_params(axis="y", length=0)
ax.text(24.5, n - 0.35, "Coût brut pour l'État", fontsize=7, color=ENCRE2, va="bottom", fontstyle="italic")
fig.subplots_adjust(right=0.62)

sauver(fig, "g7_tmei",
       "calculs des auteurs, \\texttt{note8p/calculs/is\\_reforme.py} (convention de Devereux et Griffith).",
       "Équipement neuf d'une durée d'usage de 7~ans (plan actuel pour moitié linéaire, pour moitié dégressif), "
       "financé par fonds propres ; rendement réel exigé 5~\\%, inflation 2~\\%, dépréciation 14~\\% par an, sans impôt "
       "personnel. Déduction de 50~\\% : la moitié du prix déduite l'année de l'achat, le reste amorti normalement. "
       "Coûts bruts, hors fin du taux réduit : 75~\\% de l'investissement éligible fait par des sociétés imposables ; coût permanent une fois la "
       "transition passée, en euros de 2027 (il croît ensuite avec l'investissement). Financé par emprunt, le même "
       "équipement a aujourd'hui un taux de $-24$~\\% ; $-33$~\\% avec la combinaison.")
print("g7_tmei écrite")
