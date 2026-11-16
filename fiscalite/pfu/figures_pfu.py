"""Figure de la note PFU : taux cumulé de l'IS et de l'imposition personnelle sur 100 de bénéfice (2026).

Lancer depuis fiscalite/ : python3 pfu/figures_pfu.py ; FIG_NU=1 python3 pfu/figures_pfu.py
Chiffres : pfu/notes/pfu_recherche.md, section 3 (calculs à partir des taux en vigueur en 2026).
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE.parent)]
from graphiques import ECH_TXT, INK, NU, fin, plt  # noqa: E402

# Réglages propres à cette figure (la charte graphiques.py sert aussi au cours et n'est pas modifiée) :
# TXT donne 8 pt imprimés en mode nu. Couleur selon le statut du cas : droit de 2026 en bleu, variante en
# ocre, comparaison en gris (palette validée avec dataviz/validate_palette.js, mode clair).
TXT = 10.3
plt.rcParams.update({k: TXT * ECH_TXT for k in ("xtick.labelsize", "ytick.labelsize")})
BLEU, OCRE, GRIS = "#1d4ba6", "#c79100", "#8c8c8c"

# (libellé, taux cumulé, couleur, position) : un blanc sépare le bénéfice distribué, le bénéfice gardé dans
# une holding et le salaire.
CAS = [("Bénéfice distribué, PFU (31,4 %)", 49.1, BLEU, 0),
       ("Distribué, foyer à la CEHR (35,4 %)", 52.1, BLEU, 1),
       ("Distribué, foyer à la CDHR (38,6 %)", 54.5, BLEU, 2),
       ("Distribué, variante : PFU à 25 %", 44.4, OCRE, 3),
       ("Bénéfice remonté dans une holding et conservé", 26.8, BLEU, 4.45),
       ("Pour comparaison : salaire, taux marginal supérieur", 55.4, GRIS, 5.9)]

fig, ax = plt.subplots(figsize=(8.6, 3.3))
if not NU:   # libellés dans le cadre, alignés avec le bloc des sources
    fig.subplots_adjust(left=0.37)
for lab, v, col, y in CAS:
    ax.barh(y, v, color=col, height=0.66, zorder=3)
    ax.text(v + 0.7, y, f"{v:.1f} %".replace(".", ","), va="center", fontsize=TXT, color=INK)
ax.set_yticks([c[3] for c in CAS])
ax.set_yticklabels([c[0] for c in CAS])
ax.tick_params(axis="y", length=0, pad=5)
ax.set_ylim(6.4, -0.5)
# chaque barre porte sa valeur : pas d'axe horizontal, seulement la ligne de base
ax.set_xlim(0, 61)
ax.set_xticks([])
for c in ("bottom", "left"):
    ax.spines[c].set_visible(False)
ax.axvline(0, color=INK, lw=0.8, zorder=4)
fin(fig, "pfu_01_taux_cumule",
    "Code général des impôts ; LFSS et LF 2026 ; calculs de l'auteur.",
    "Note : impôt total sur 100 de bénéfice avant impôt, droit de 2026 ; entre parenthèses, le taux du prélèvement "
    "personnel sur le dividende. Impôt sur les sociétés de 25 % plus la "
    "contribution sociale de 3,3 % (25,8 %), puis prélèvement personnel sur le dividende : PFU de 31,4 % (12,8 % "
    "d'impôt sur le revenu et 18,6 % de prélèvements sociaux), majoré de la contribution exceptionnelle sur les "
    "hauts revenus (4 %) ou porté au plancher de 20 % de la contribution différentielle. Holding : dividende "
    "exonéré à 95 % (régime mère-fille), soit 1,25 % d'impôt. Salaire : impôt sur le revenu à 45 % et CEHR à 4 %, "
    "plus CSG et CRDS (9,7 %, dont 6,8 points déductibles), hors cotisations sociales. Entreprises de plus de "
    "3 Md€ de chiffre d'affaires (taux le plus élevé de la contribution exceptionnelle, dont les quelque 450 "
    "redevables comprennent aussi des groupes de 1 à 3 Md€) : 56 à 61 % selon la situation de l'actionnaire.")
