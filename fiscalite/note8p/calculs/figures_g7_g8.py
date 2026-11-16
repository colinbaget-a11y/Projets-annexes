"""Figures g7 (taux marginal effectif de l'investissement, au taux final de 22,5 %) et g8 (bouclage en régime de croisière).

g7 : TMEI calculés par les fonctions de calculs/is_reforme.py (exécuté tel quel : ses sorties sont déterministes) ;
coûts permanents en euros de 2027 (is.json) et, pour le taux, 2,5 points au coût de bouclage.json.
g8 : sorties/bouclage.json (année de caisse 2037, toutes mesures à plein régime) et sorties/ircsg.json, foncier.json.
"""
import json
import runpy
import sys
from pathlib import Path

D = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(D))
from charte import AUJ, NAIF, PROP, HAUSSE, ENCRE, ENCRE2, PLEINE, DEMI, plt, axes, sauver, _fr  # noqa: E402

S = D / "sorties"
IS = json.loads((S / "is.json").read_text(encoding="utf-8"))
B = json.loads((S / "bouclage.json").read_text(encoding="utf-8"))
IR = json.loads((S / "ircsg.json").read_text(encoding="utf-8"))
FO = json.loads((S / "foncier.json").read_text(encoding="utf-8"))
PF = json.loads((S / "pfu.json").read_text(encoding="utf-8"))

# ------------------------------------------------------------------ g7
g = runpy.run_path(str(D / "calculs" / "is_reforme.py"))
tmei = g["tmei"]
C = IS["comparaison"]
an = B["annuel"]["2037"]
point = -an["baisse_taux"] / 2.5                      # coût d'un point en 2037 (euros constants 2027)
lignes = [
    ("Aujourd'hui (25 %)", 0.25, 0.0, AUJ, "référence"),
    ("Taux normal à 22,5 %", 0.225, 0.0, NAIF, f"{_fr(2.5 * point, 1)} Md€ par an"),
    ("Déduction immédiate de 50 %", 0.25, 0.5, NAIF, f"{_fr(C['ded50']['cout_permanent_2027'], 1)} Md€ par an (pic : {_fr(C['ded50']['cout_2028'], 1)})"),
    ("22,5 % + déduction de 50 % (proposition)", 0.225, 0.5, PROP,
     f"{_fr(2.5 * point + C['ded50']['cout_permanent_2027'] * 0.9, 1)} Md€ par an"),
    ("Déduction intégrale (repère)", 0.25, 1.0, NAIF, f"{_fr(C['ded100']['cout_permanent_2027'], 1)} Md€ par an (pic : {_fr(C['ded100']['cout_2027'], 1)})"),
]
vals = {}
fig, ax = plt.subplots(figsize=(PLEINE, 2.2))
n = len(lignes)
for i, (lab, tau, b, col, cout) in enumerate(lignes):
    v = 100 * tmei(tau, b, "fp")[0]
    vals[lab] = v
    y = n - 1 - i
    ax.barh(y, max(v, 0.15), color=col, height=0.62, zorder=2)
    ax.text(max(v, 0) + 0.4, y, f"{_fr(v)} %", va="center", fontsize=7.5, color=ENCRE,
            fontweight="bold" if col == PROP else "normal")
    ax.text(21.5, y, cout, va="center", ha="left", fontsize=7, color=ENCRE2)
ax.text(21.5, n - 0.45, "coût permanent pour l'État", fontsize=7, color=ENCRE2, va="bottom", fontstyle="italic")
ax.set_yticks(range(n))
ax.set_yticklabels([l[0] for l in lignes][::-1])
ax.set_xlim(0, 21)
ax.set_xticks([0, 5, 10, 15, 20])
ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v:.0f} %"))
ax.set_xlabel("Taux marginal effectif d'imposition d'une machine financée par fonds propres", fontsize=7.5)
axes(ax, grille="x")
sauver(fig, "g7_tmei",
       "calculs de l'auteur (note8p/calculs/is_reforme.py, figures_g7_g8.py) : équipement amorti sur 7 ans, dépréciation "
       "économique 14 \\%, rendement réel exigé 5 \\%, inflation 2 \\% ; coûts permanents en euros de 2027.",
       "Le taux marginal effectif mesure l'impôt payé sur l'investissement qui rapporte tout juste ce qu'exigent les "
       "actionnaires. La déduction immédiate n'efface pas l'impôt : elle le décale ; son coût est élevé les premières "
       "années, puis faible.")

# ------------------------------------------------------------------ g8 : bouclage en régime de croisière (caisse 2037)
ir = IR["annuel"]["2037"]
fo = FO["annuel"]["2037"]
postes = [
    ("Baisse de l'impôt sur les actifs", ir["ircsg_baisse_actifs"] + ir["ircsg_cehr_bareme_absorbee"]
     + ir["ircsg_invalidite_dependance_maintenus"]),
    ("Pensions imposées comme les salaires", ir["ircsg_hausse_retraites"]),
    ("Droits de mutation divisés par deux", fo["dmto"]),
    ("Nouvelle taxe foncière (sol × 4)", fo["taxe_fonciere_nouvelle"]),
    ("Report de paiement, déductibilité", fo["report_paiement"] + fo["deductibilite_is_ir"] + fo["calendrier_ventes"]),
    ("Fin du taux réduit d'IS", an["taux_reduit"]),
    ("Déduction immédiate de 50 %", an["deduction_50"]),
    ("Taux normal de l'IS à 22,5 %", an["baisse_taux"]),
]
solde = sum(v for _, v in postes)
pv = an["pfu_reserve"]
fig, ax = plt.subplots(figsize=(PLEINE, 2.6))
n = len(postes) + 2
for i, (lab, v) in enumerate(postes):
    y = n - 1 - i
    col = PROP if v < 0 else HAUSSE
    ax.barh(y, v, color=col, height=0.62, zorder=2)
    ax.text(v + (0.25 if v >= 0 else -0.25), y, f"{'+' if v > 0 else ''}{_fr(v, 1)}", va="center",
            ha="left" if v >= 0 else "right", fontsize=7.5, color=ENCRE)
y = 1
ax.barh(y, solde, color=AUJ, height=0.62, zorder=2)
ax.text(solde + (0.25 if solde >= 0 else -0.25), y, f"{'+' if solde > 0 else ''}{_fr(solde, 1)} : solde", va="center",
        ha="left" if solde >= 0 else "right", fontsize=7.5, color=ENCRE, fontweight="bold")
ax.barh(0, pv, color="white", edgecolor=HAUSSE, hatch="////", height=0.62, zorder=2)
ax.text(pv + 0.25, 0, f"+{_fr(pv, 1)} : réserve, utilisée une fois constatée", va="center", fontsize=7.5, color=ENCRE)
ax.axvline(0, color=ENCRE2, lw=0.7)
ax.set_yticks(range(n))
ax.set_yticklabels(["Fin de l'effacement des plus-values", "Solde des mesures"] + [p[0] for p in postes][::-1])
ax.set_xlim(-16.5, 19)
ax.set_xlabel("Md€ par an, euros de 2027 (+ : recette publique en plus ; − : baisse d'impôt)", fontsize=7.5)
axes(ax, grille="x")
sauver(fig, "g8_bouclage",
       "calculs de l'auteur (note8p/calculs/bouclage.py, figures_g7_g8.py), régime de croisière (recettes de 2037).",
       "Hausses d'impôt en ocre, baisses en bleu. Les recettes de la fin de l'effacement des plus-values ne financent "
       "aucune baisse tant qu'elles ne sont pas constatées.")
print({k: round(v, 1) for k, v in vals.items()}, round(solde, 2), round(pv, 2), [(p, round(v, 2)) for p, v in postes])
