"""Figure g8 v3 : qui paie quoi en régime de croisière (recettes de 2037), d'après sorties/bouclage3.json et ircsg3.json.

L'impôt sur le revenu est présenté par payeur (retraités, actifs) : chaque ligne est nette des niches supprimées et du
nouveau barème, pour ne rien compter deux fois ; la décomposition interne (niches, quotients, barème) est la figure de
la cascade (figures/travail/F_cascade_recettes).
"""
import json
import sys
from pathlib import Path

D = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(D))
from charte import AUJ, PROP, HAUSSE, ENCRE, ENCRE2, PLEINE, plt, axes, sauver, _fr  # noqa: E402

B = json.loads((D / "sorties" / "bouclage3.json").read_text(encoding="utf-8"))["annuel"]["2037"]
I = json.loads((D / "sorties" / "ircsg3.json").read_text(encoding="utf-8"))["annuel_final"]["2037"]
postes = [
    ("Retraités : pensions imposées comme les salaires", I["ircsg_retraites"]),
    ("Actifs : nouvel impôt sur le revenu", I["ircsg_actifs"] + I["ircsg_cehr_bareme_absorbee"]
     + I["ircsg_invalidite_dependance_maintenus"]),
    ("Taxe nationale sur la valeur du sol", B["taxe_fonciere"]),
    ("Droits de mutation divisés par deux", B["dmto"]),
    ("Report de paiement, déductibilité, calendrier", B["foncier_autres"]),
    ("Fin du taux réduit d'IS", B["is_taux_reduit"]),
    ("Niches de l'IS (CIR recentré, mécénat, crédits sectoriels, zonages)", B["is_niches"]),
    ("Déduction immédiate de 50 % (coût permanent)", B["is_deduction_50"]),
]
solde = sum(v for _, v in postes)
fig, ax = plt.subplots(figsize=(PLEINE, 2.9))
n = len(postes) + 1
for i, (lab, v) in enumerate(postes):
    y = n - 1 - i
    ax.barh(y, v, color=HAUSSE if v > 0 else PROP, height=0.62, zorder=2)
    ax.text(v + (0.3 if v >= 0 else -0.3), y, f"{'+' if v > 0 else ''}{_fr(v, 1)}", va="center",
            ha="left" if v >= 0 else "right", fontsize=7.5, color=ENCRE)
ax.barh(0, solde, color=AUJ, height=0.62, zorder=2)
ax.text(max(solde, 0) + 0.3, 0, f"solde : {'+' if solde > 0 else ''}{_fr(solde, 1)}", va="center", fontsize=7.5,
        color=ENCRE, fontweight="bold")
ax.axvline(0, color=ENCRE2, lw=0.7)
ax.set_yticks(range(n))
ax.set_yticklabels(["Solde"] + [p[0] for p in postes][::-1])
ax.set_xlim(-21, 16)
ax.set_xlabel("Md€ par an en régime de croisière (+ : prélèvement en plus ; − : baisse)", fontsize=7.5)
axes(ax, grille="x")
sauver(fig, "g8_bouclage", "calculs des auteurs, régime de croisière (recettes de 2037), euros de 2027 environ.",
       "Les lignes de l'impôt sur le revenu sont nettes des niches supprimées et du nouveau barème. Non comptées : "
       "recettes de la fin de l'effacement des plus-values (réserve), fin de la contribution exceptionnelle sur l'IS et "
       "extinction de la CRDS (droit en vigueur).")
print([(p, round(v, 2)) for p, v in postes], round(solde, 2))
