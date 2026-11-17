"""Figure de bilan (v5) : ce que la réforme prélève et ce qu'elle rend, mesure par mesure, en régime de croisière
(recettes de 2040, euros de 2027 environ, Md€ arrondis).

Sources : sorties/ircsg4.json (cascade_categories et cascade_brute : décomposition séquentielle, statique, du nouvel
impôt sur le revenu) ; foncier3.json (B_E10, 2040) ; is4.json (annuel_caisse 2040, lignes prudentes, déflatées de
3 %/an) ; pal.json (revalorisation des déficits reportables, régime permanent) ; bouclage4.json (solde).
Sortie : figures/figure_bilan.{pdf,png} et figure_bilan_source.tex ; sorties/bilan_v5.json.
"""
import json
import sys
from pathlib import Path

D = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(D))
from charte import AUJ, PROP, HAUSSE, ENCRE, ENCRE2, PLEINE, plt, axes, sauver, _fr  # noqa: E402

S = D / "sorties"
L = lambda n: json.loads((S / n).read_text(encoding="utf-8"))  # noqa: E731
IR = L("ircsg4.json")
K = IR["cascade_categories"]
CB = {c["etape"]: c["Md"] for c in IR["cascade_brute"]}
C = L("is4.json")["annuel_caisse"]["2040"]
F = L("foncier3.json")["annuel_par_scenario"][json.loads((Path(__file__).resolve().parent.parent / "parametres.json").read_text(encoding="utf-8"))["scenario_foncier"]]["2040"]
PX = L("pal.json")["pertes"]["national"]["indexation_cout_regime_Md"]["central"]
B = L("bouclage4.json")["annuel"]["2040"]
PAR = json.loads((Path(__file__).resolve().parent.parent / "parametres.json").read_text(encoding="utf-8"))
F3 = L("foncier3.json")
TX = F3["scenarios"][PAR["scenario_foncier"]]["taux"]
AS = F3["assiette"]
COM_SOL, COM_BATI = TX["tc_sol"] / 100 * TX["sol_apres"], TX["tc_bati"] / 100 * AS["bati"]
PART_SOL = AS["sol"] / (AS["sol"] + AS["bati"])          # convention : aujourd'hui, taux unique sur la valeur totale
TRANSFERT = COM_SOL - (COM_SOL + COM_BATI) * PART_SOL
d = 1.03 ** 13

BLOCS = [
    ("Nouvel impôt sur le revenu", [
        ("Suppression des niches", K["vraies_niches"]),
        ("Pensions imposées comme les salaires", K["alignement_pensions"]),
        ("Fin du quotient conjugal", K["unite_fiscale"]),
        ("Fin du quotient familial", CB["qf"]),
        ("Fin de la CSG déductible", K["technique_csg_deductible"]),
        ("Forfait de 500 € au lieu du 10 % et des frais réels", K["technique_frais"]),
        (f"Franchise de {_fr(PAR['franchise_enfant'])} € par enfant", K["quotient_familial_vers_franchise"] - CB["qf"]),
        ("Baisse des taux (nouveau barème)", K["bareme"]),
        ("Minimum vieillesse ; contribution sur les hauts revenus", K["aspa_nette"] + K["cehr_absorbee"]),
    ]),
    ("Fiscalité foncière", [
        ("Taxe nationale sur la valeur du sol", F["net"] - F["dmto"]),
        ("Taxe foncière communale : le sol paie davantage", TRANSFERT),
        ("Taxe foncière communale : le bâti paie moins", -TRANSFERT),
        ("Droits de mutation divisés par deux", F["dmto"]),
    ]),
    ("Impôt sur les sociétés", [
        ("Fin du taux réduit", C["is_fin_taux_reduit_prudent"] / d),
        ("Fin du crédit d'impôt recherche", C["is_cir_suppression_realisable_prudent"] / d),
        ("Fin des autres niches", C["is_niches_rendement_prudent_realisable"] / d),
        ("Déduction immédiate des investissements", (C["is_deduction_50_depart_2029"] + C["is_reinvest_logiciels_acquis"]
                                                     + C["is_reinvest_deduction_75_puis_100"]) / d),
        ("Revalorisation des déficits reportables", -PX),
    ]),
]
lignes, ytick, y = [], [], 0
for titre, items in BLOCS:
    st = sum(v for _, v in items)
    lignes.append(("titre", titre, st, y))
    y -= 1
    for lab, v in items:
        lignes.append(("item", lab, v, y))
        y -= 1
    y -= 0.4
solde = sum(v for _, it in BLOCS for _, v in it)
assert abs(solde - B["solde"]) < 0.05, (solde, B["solde"])
lignes.append(("solde", "Solde de l'ensemble", solde, y))


def lab(v):
    r = round(v)
    if r == 0:
        return "≈ 0"
    return ("+" if r > 0 else "−") + _fr(abs(r))


fig, ax = plt.subplots(figsize=(PLEINE, 5.0))
for typ, t, v, yy in lignes:
    if typ == "item":
        ax.barh(yy, v, color=HAUSSE if v > 0 else PROP, height=0.66, zorder=2)
        ax.text(v + (1.2 if v >= 0 else -1.2), yy, lab(v), va="center", ha="left" if v >= 0 else "right", fontsize=7.2,
                color=ENCRE2)
    else:
        ax.barh(yy, v, color=AUJ, height=0.66, zorder=2)
        ax.text(v + (1.2 if v >= 0 else -1.2), yy, lab(v), va="center", ha="left" if v >= 0 else "right", fontsize=7.4,
                color=ENCRE, fontweight="bold")
ax.axvline(0, color=ENCRE2, lw=0.7)
ax.set_yticks([l[3] for l in lignes])
ax.set_yticklabels([l[1] for l in lignes], fontsize=7.2)
for tl, l in zip(ax.get_yticklabels(), lignes):
    if l[0] != "item":
        tl.set_fontweight("bold")
        tl.set_color(ENCRE)
ax.set_xlim(-112, 36)
ax.set_xlabel("Milliards d'euros par an, réforme installée (+ : l'État prélève davantage ; − : il prélève moins)",
              fontsize=7)
axes(ax, grille="x")
ax.spines["left"].set_visible(False)
ax.tick_params(axis="y", length=0)
sauver(fig, "figure_bilan",
       "calculs des auteurs : modèle de foyers calé sur les statistiques de l'impôt sur le revenu 2024 (DGFiP) ; coûts des"
       " niches : Évaluation des voies et moyens PLF 2026, CPO (2026) ; foncier : DVF et comptes de patrimoine (Insee) ;"
       " impôt sur les sociétés : recettes 2025 et coût du crédit d'impôt recherche (PLF 2027) ; annexes B à F.",
       "Recettes de 2040 en euros de 2027 environ, arrondies au milliard. Gris : total de chaque bloc. Impôt sur le revenu :"
       " décomposition séquentielle avant réaction des comportements (l'ordre change la taille de chaque ligne, pas le"
       " total). Taxe foncière communale à deux taux, à recette inchangée : aujourd'hui répartie entre sol et bâti au"
       " prorata de leur valeur (convention). Taxe nationale sur le sol nette de sa déductibilité des bénéfices."
       " Impôt sur les sociétés : rendements prudents, après réaction des entreprises. Non comptée : fin de l'effacement des plus-values au décès"
       " (environ 1 milliard à terme, gardé en réserve).")
out = dict(blocs=[dict(titre=t, items=[dict(libelle=l, Md=v) for l, v in it], sous_total=sum(v for _, v in it))
                  for t, it in BLOCS], solde=solde, annee=2040, unite="Md€ de 2027 environ")
(S / "bilan_v5.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
print([(t, round(sum(v for _, v in it), 2)) for t, it in BLOCS], round(solde, 2))
