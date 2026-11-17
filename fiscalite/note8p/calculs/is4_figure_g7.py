"""Figure g7_tmei (version 4 : déduction portée à 100 % par paliers, financée par la suppression du CIR) : taux marginal effectif d'imposition d'une machine neuve
financée par fonds propres, quatre configurations, et leur coût budgétaire (pic et permanent).
Lancer depuis fiscalite/ après note8p/calculs/is3_reforme.py et is4_reforme.py -> note8p/figures/g7_tmei.pdf, .png, _source.tex
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]           # note8p/
sys.path.insert(0, str(ROOT))
from charte import AUJ, NAIF, PROP, ENCRE, ENCRE2, PLEINE, plt, axes, sauver, pct, _fr  # noqa: E402

J = json.loads((ROOT / "sorties" / "is3.json").read_text(encoding="utf-8"))
T, D, LT = J["taux_effectifs"], J["deduction"], J["long_terme"]
pics = [D["departs"]["2029"]["pic"]]
perm50, perm100 = D["cout_permanent_2027"]["50"] / 1.03, D["cout_permanent_2027"]["100"] / 1.03   # euros de 2026
c225 = J["comparaison_taux_225"]["cout_2027"] / 1.03   # euros de 2026
J4 = json.loads((ROOT / "sorties" / "is4.json").read_text(encoding="utf-8"))
sup = J4["reinvestissement"]["options_exercices"]["b_equipements_75_2033_100_des_2036"]
pic_sup = max(sup.values())

lignes = [  # clé, libellé, couleur, hachure, coût
    ("actuel", "Aujourd'hui (taux de 25 %)", AUJ, None, "référence"),
    ("taux225", "Baisse du taux à 22,5 % (comparaison)", NAIF, None, f"{_fr(c225, 1)} Md€ par an, chaque année"),
    ("ded50", "Déduction immédiate de 50 % (proposition)", PROP, None,
     f"pic {_fr(max(pics), 1)} Md€ (2e année), puis {_fr(perm50, 1)} Md€ par an"),
    ("ded100", "Déduction intégrale (dès 2032)", "white", "////",
     f"jusqu'à {_fr(pic_sup, 1)} Md€ de plus une année, puis {_fr(perm100, 1)} Md€ par an"),
]
fig, ax = plt.subplots(figsize=(PLEINE, 2.0))
n = len(lignes)
for i, (k, lab, col, hat, cout) in enumerate(lignes):
    y = n - 1 - i
    v = 100 * T[k]["fp"]
    ax.barh(y, max(v, 0.12), height=0.62, color=col, edgecolor=(NAIF if hat else col), hatch=hat, lw=0.8, zorder=2)
    ax.text(max(v, 0) + 0.4, y, _fr(v) + " %", va="center", ha="left", fontsize=7.5, color=ENCRE,
            fontweight="bold" if k == "ded50" else "normal")
    ax.text(21.5, y, cout, va="center", ha="left", fontsize=7, color=ENCRE2)
ax.text(21.5, n - 0.4, "Coût brut pour l'État", fontsize=7, color=ENCRE2, va="bottom", fontstyle="italic")
ax.set_yticks(range(n))
ax.set_yticklabels([l[1] for l in lignes][::-1])
ax.set_xlim(0, 20.5)
ax.set_ylim(-0.6, n - 0.35)
ax.set_xticks([0, 5, 10, 15, 20])
ax.xaxis.set_major_formatter(pct)
axes(ax, grille="x")
ax.spines["left"].set_visible(False)
ax.tick_params(axis="y", length=0)
fig.subplots_adjust(right=0.6)
sauver(fig, "g7_tmei",
       "calculs des auteurs, \\texttt{note8p/calculs/is3\\_reforme.py} et \\texttt{is4\\_reforme.py} (convention de Devereux et Griffith).",
       "Machine neuve d'une durée d'usage de 7~ans (plan actuel pour moitié linéaire, pour moitié dégressif), financée "
       "par fonds propres ; rendement réel exigé 5~\\%, inflation 2~\\%, dépréciation 14~\\% par an, sans impôt personnel. "
       "Déduction de 50~\\% : la moitié du prix déduite l'année de l'achat, le reste amorti normalement, au taux de 25~\\% ; "
       "25~\\% pour l'exercice 2029, 50~\\% dès 2030 ; 100~\\% dès 2032, financés par la suppression du "
       "crédit d'impôt recherche. Coûts bruts, hors financement ; coûts permanents en euros de 2026. "
       "Financée par emprunt, la même machine a un taux de $-24$~\\% aujourd'hui, $-37$~\\% avec la déduction de 50~\\% ; "
       "pour un tiers d'emprunt, 7,6~\\% et $-1{,}7$~\\%.")
print("g7_tmei écrite", {k: round(100 * T[k]["fp"], 1) for k, *_ in lignes})
