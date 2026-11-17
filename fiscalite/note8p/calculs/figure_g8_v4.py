"""Figure g8 v4 : d'où vient l'argent, où va-t-il (recettes de 2040, scénario central, euros de 2027 environ).

Sources : sorties/bouclage4.json, ircsg4.json (annuel_final 2040), is4.json (annuel_caisse 2040, lignes prudentes,
déflatées de 3 %/an), foncier3.json (B_E10). Les lignes de l'impôt sur le revenu sont nettes des niches supprimées.
"""
import json
import sys
from pathlib import Path

D = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(D))
from charte import AUJ, PROP, HAUSSE, ENCRE, ENCRE2, PLEINE, plt, axes, sauver, _fr  # noqa: E402

S = D / "sorties"
L = lambda n: json.loads((S / n).read_text(encoding="utf-8"))
I = L("ircsg4.json")["annuel_final"]["2040"]
C = L("is4.json")["annuel_caisse"]["2040"]
F = L("foncier3.json")["annuel_par_scenario"]["B_E10"]["2040"]
d = 1.03 ** 13
postes = [
    ("Retraités : pensions imposées comme les salaires", I["ircsg_retraites"]),
    ("Actifs : nouvel impôt sur le revenu", I["ircsg_actifs"] + I["ircsg_cehr_bareme_absorbee"]),
    ("Minimum vieillesse calculé sur la pension nette", I["aspa_nette_depense"]),
    ("Taxe nationale sur la valeur du sol", F["taxe_fonciere_nouvelle"]),
    ("Droits de mutation divisés par deux", F["dmto"]),
    ("Report de paiement, déductibilité", F["net"] - F["taxe_fonciere_nouvelle"] - F["dmto"]),
    ("Fin du taux réduit d'IS", C["is_fin_taux_reduit_prudent"] / d),
    ("Fin du crédit d'impôt recherche", C["is_cir_suppression_realisable_prudent"] / d),
    ("Autres niches de l'IS", C["is_niches_rendement_prudent_realisable"] / d),
    ("Déduction immédiate des investissements", (C["is_deduction_50_depart_2029"] + C["is_reinvest_logiciels_acquis"]
                                                + C["is_reinvest_deduction_75_puis_100"]) / d),
]
solde = sum(v for _, v in postes)
fig, ax = plt.subplots(figsize=(PLEINE, 3.0))
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
ax.set_xlim(-24, 17)
ax.set_xlabel("Md€ par an en 2040, euros de 2027 (+ : prélèvement en plus ; − : baisse)", fontsize=7.5)
axes(ax, grille="x")
sauver(fig, "g8_bouclage", "calculs des auteurs, scénario central, recettes de 2040 (rendements prudents pour l'IS).",
       "Les lignes de l'impôt sur le revenu sont nettes des niches supprimées et du nouveau barème. Non comptés : "
       "fin de l'effacement des plus-values (réserve), fin de la contribution exceptionnelle sur l'IS et extinction "
       "de la CRDS (droit en vigueur).")
print([(p, round(v, 2)) for p, v in postes], round(solde, 2))
