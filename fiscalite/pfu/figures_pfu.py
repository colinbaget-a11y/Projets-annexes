"""Figure de la note PFU : taux cumulé de l'IS et de l'imposition personnelle sur 100 de bénéfice (2026).

Lancer depuis fiscalite/ : python3 pfu/figures_pfu.py ; FIG_NU=1 python3 pfu/figures_pfu.py
Chiffres : pfu/notes/pfu_recherche.md, section 3 (calculs à partir des taux en vigueur en 2026).
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE.parent)]
from graphiques import INK, PCT, fin, grille, plt  # noqa: E402

CAS = [("Bénéfice distribué, PFU (31,4 %)", 49.1, "#003399"),
       ("Distribué, foyer à la CEHR (35,4 %)", 52.1, "#003399"),
       ("Distribué, foyer à la CDHR (38,6 %)", 54.5, "#003399"),
       ("Variante PFU à 25 %", 44.4, "#c79100"),
       ("Bénéfice remonté dans une holding et conservé", 26.8, "#993333"),
       ("Pour comparaison : salaire, taux marginal supérieur", 55.4, "#6b6b6b")]

fig, ax = plt.subplots(figsize=(8.6, 3.4))
for i, (lab, v, col) in enumerate(CAS):
    ax.barh(i, v, color=col, height=0.62)
    ax.text(v + 0.8, i, f"{v:.1f} %".replace(".", ","), va="center", fontsize=8.5, color=INK)
ax.set_yticks(range(len(CAS)))
ax.set_yticklabels([c[0] for c in CAS], fontsize=8.5)
ax.invert_yaxis()
ax.set_xlim(0, 62)
ax.xaxis.set_major_formatter(PCT)
grille(ax, "x")
fin(fig, "pfu_01_taux_cumule",
    "Code général des impôts ; LFSS et LF 2026 ; calculs de l'auteur.",
    "Note : impôt total sur 100 de bénéfice avant impôt, droit de 2026. Impôt sur les sociétés de 25 % plus la "
    "contribution sociale de 3,3 % (25,8 %), puis prélèvement personnel sur le dividende : PFU de 31,4 % (12,8 % "
    "d'impôt sur le revenu et 18,6 % de prélèvements sociaux), majoré de la contribution exceptionnelle sur les "
    "hauts revenus (4 %) ou porté au plancher de 20 % de la contribution différentielle. Holding : dividende "
    "exonéré à 95 % (régime mère-fille), soit 1,25 % d'impôt. Salaire : impôt sur le revenu à 45 % et CEHR à 4 %, "
    "plus CSG et CRDS (9,7 %, dont 6,8 points déductibles), hors cotisations sociales. Entreprises de plus de "
    "3 Md€ de chiffre d'affaires (taux le plus élevé de la contribution exceptionnelle, dont les quelque 450 "
    "redevables comprennent aussi des groupes de 1 à 3 Md€) : 56 à 61 % selon la situation de l'actionnaire.")
