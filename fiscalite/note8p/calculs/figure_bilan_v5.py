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
G, AREF = PAR["croissance_nominale"], PAR["annee_reference"]
K25 = (1 + G) ** (AREF - 2025)
d = (1 + G) ** (2040 - AREF)

FA = L("foncier3.json")["annuel_par_scenario"][PAR["scenario_foncier"]]
CA = L("is4.json")["annuel_caisse"]
PXA = {int(a): v for a, v in L("pal.json")["pertes"]["national"]["indexation_cout_regime_Md"]["montee_en_charge_indicative"].items()}


# corrections issues de la vérification à la source (sorties/verification_bilan_ir.md) : Girardin éteint avant 2032 en droit
# actuel (0,894) ; abattement des personnes âgées calé sur les Voies et moyens (0,419) ; 1,33 Md€ de CSG induite par la fin de
# l'abattement de 10 % reclassés dans la ligne CSG. Le barème a été recalé d'autant (parametres.json).
GIR, AGE_VM, CSG_ABAT = 0.894, 0.419, 1.33
ND = {k: v["recette_croisiere_Md"] for k, v in IR["recette_niches_par_dispositif"]["par_dispositif"].items()}
PRINC = ("emploi_domicile", "epargne_salariale", "heures_sup", "dons", "garde", "demi_parts")
assert abs(sum(ND.values()) - K["vraies_niches"]) < 0.01
assert abs(CB["abatpen"] + CB["age"] + CB["csg_ret"] - K["alignement_pensions"]) < 0.01


def blocs(an):
    """Lignes du bilan pour une année de caisse (euros de 2027 environ). L'impôt sur le revenu est en régime installé
    dès 2030 (décomposition statique) : mêmes valeurs en 2032 et en 2040."""
    f, c, dd = FA[str(an)], CA[str(an)], (1 + G) ** (an - AREF)
    px = PXA.get(an, PX if an >= 2032 else 0.0)
    return [
        ("Nouvel impôt sur le revenu", [
            ("Niches : crédit pour l'emploi à domicile", K25 * ND["emploi_domicile"]),
            ("Niches : intéressement et participation exonérés", K25 * ND["epargne_salariale"]),
            ("Niches : heures supplémentaires exonérées", K25 * ND["heures_sup"]),
            ("Niches : réduction pour dons", K25 * ND["dons"]),
            ("Niches : crédit pour la garde des jeunes enfants", K25 * ND["garde"]),
            ("Niches : demi-parts dérogatoires", K25 * ND["demi_parts"]),
            ("Niches : autres (Girardin, outre-mer, scolarité…)", K25 * (K["vraies_niches"] - sum(ND[x] for x in PRINC) - GIR)),
            ("Retraités : fin de l'abattement de 10 % sur les pensions", K25 * (CB["abatpen"] - CSG_ABAT)),
            ("Retraités : CSG alignée sur celle des actifs", K25 * (CB["csg_ret"] + CSG_ABAT)),
            ("Retraités : fin de l'abattement des personnes âgées", K25 * AGE_VM),
            ("Salariés : forfait de 500 € au lieu de l'abattement de 10 %", K25 * K["technique_frais"]),
            ("Fin de la CSG déductible", K25 * K["technique_csg_deductible"]),
            ("Impôt individuel : fin du quotient conjugal", K25 * K["unite_fiscale"]),
            ("Fin du quotient familial", K25 * CB["qf"]),
            (f"Franchise de {_fr(PAR['franchise_enfant'])} € par enfant", K25 * (K["quotient_familial_vers_franchise"] - CB["qf"])),
            ("Baisse des taux (nouveau barème)", K25 * K["bareme"]),
            ("Minimum vieillesse ; contribution sur les hauts revenus", K25 * (K["aspa_nette"] + K["cehr_absorbee"])),
        ]),
        ("Fiscalité foncière", [
            ("Taxe communale sur le bâti : valeur de marché, même recette", 0.0),
            ("Taxe communale sur le sol : valeur de marché, même recette", 0.0),
            ("Taxe nationale sur la valeur du sol", K25 * (f["net"] - f["dmto"])),
            ("Droits de mutation divisés par deux", K25 * f["dmto"]),
        ]),
        ("Impôt sur les sociétés", [
            ("Fin du taux réduit", c["is_fin_taux_reduit_prudent"] / dd),
            ("Fin du crédit d'impôt recherche", c["is_cir_suppression_realisable_prudent"] / dd),
            ("Fin des autres niches", c["is_niches_rendement_prudent_realisable"] / dd),
            ("Déduction immédiate des investissements", (c["is_deduction_50_depart_2029"] + c["is_reinvest_logiciels_acquis"]
                                                         + c["is_reinvest_deduction_75_puis_100"]) / dd),
            ("Revalorisation des déficits reportables", -K25 * px),
        ]),
    ]


ANNEE = 2032          # année affichée (transition de la déduction immédiate en cours)
B40, B32 = blocs(2040), blocs(2032)
BLOCS = B32
V32 = {}
for t, it in B32:
    V32[t] = sum(v for _, v in it)
    for l, v in it:
        V32[l] = v
V32["Solde de l'ensemble"] = sum(v for _, it in B32 for _, v in it)
assert abs(V32["Solde de l'ensemble"] - L("bouclage4.json")["annuel"]["2032"]["solde"]) < 0.05
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
assert abs(solde - L("bouclage4.json")["annuel"][str(ANNEE)]["solde"]) < 0.05
lignes.append(("solde", "Solde de l'ensemble", solde, y))
# options non retenues (hors solde) : baisse du PFU (sorties/pfu_options.json, après réaction)
PO = L("pfu_options.json")
y -= 1.4
OPTS = []
for k, lib in (("30", "Option : prélèvement forfaitaire unique à 30 %"), ("25", "Option : prélèvement forfaitaire unique à 25 %")):
    OPTS.append((lib, -PO[k]["central"], y))
    V32[lib] = -PO[k]["central"]
    y -= 1


def lab(v, t=""):
    if "même recette" in t:
        return "0"
    r = round(v)
    if r == 0:
        return "≈ 0"
    return ("+" if r > 0 else "−") + _fr(abs(r))


fig, ax = plt.subplots(figsize=(PLEINE, 6.6))
for typ, t, v, yy in lignes:
    if typ == "item":
        ax.barh(yy, v, color=HAUSSE if v > 0 else PROP, height=0.66, zorder=2)
        ax.text(v + (1.2 if v >= 0 else -1.2), yy, lab(v, t), va="center", ha="left" if v >= 0 else "right", fontsize=7.2,
                color=ENCRE2)
    else:
        ax.barh(yy, v, color=AUJ, height=0.66, zorder=2)
        ax.text(v + (1.2 if v >= 0 else -1.2), yy, lab(v), va="center", ha="left" if v >= 0 else "right", fontsize=7.4,
                color=ENCRE, fontweight="bold")
ax.text(-110, lignes[0][3] + 0.9, f"Recettes de {ANNEE}", ha="left", fontsize=7.2, color=ENCRE, fontweight="bold")
for lib, v, yy in OPTS:
    ax.barh(yy, v, color="white", edgecolor=HAUSSE, hatch="////", height=0.66, zorder=2, lw=0.8)
    ax.text(v - 1.2, yy, lab(v) + f"  (solde : {lab(solde + v)})", va="center", ha="right", fontsize=7.2, color=HAUSSE)
lignes += [("option", lib, v, yy) for lib, v, yy in OPTS]
ax.axvline(0, color=ENCRE2, lw=0.7)
ax.set_yticks([l[3] for l in lignes])
ax.set_yticklabels([l[1] for l in lignes], fontsize=7.2)
for tl, l in zip(ax.get_yticklabels(), lignes):
    if l[0] == "option":
        tl.set_color(HAUSSE)
        tl.set_fontstyle("italic")
    elif l[0] != "item":
        tl.set_fontweight("bold")
        tl.set_color(ENCRE)
ax.set_xlim(-112, 36)
ax.set_xticks([-100, -80, -60, -40, -20, 0, 20])
ax.set_xlabel(f"Milliards d'euros en {ANNEE} (+ : l'État prélève davantage ; − : il prélève moins)",
              fontsize=7)
axes(ax, grille="x")
ax.spines["left"].set_visible(False)
ax.tick_params(axis="y", length=0)
sauver(fig, "figure_bilan",
       "calculs des auteurs : modèle de foyers calé sur les statistiques de l'impôt sur le revenu 2024 (DGFiP) ; coûts des"
       " niches : Évaluation des voies et moyens PLF 2026, CPO (2026) ; foncier : DVF et comptes de patrimoine (Insee) ;"
       " impôt sur les sociétés : recettes 2025 et coût du crédit d'impôt recherche (PLF 2027) ; annexes B à F.",
       "Recettes de 2032, en euros de 2026, arrondies au milliard. Gris : total de chaque bloc. Impôt sur le revenu :"
       " décomposition séquentielle avant réaction des comportements (l'ordre change la taille de chaque ligne, pas le"
       " total). Taxe foncière communale assise sur la valeur de marché, en deux parts (sol et bâti), à recette communale inchangée : le total ne change pas, mais la charge se redistribue entre logements. Taxe nationale sur le sol nette de sa déductibilité des bénéfices."
       " Impôt sur les sociétés : rendements prudents, après réaction des entreprises. En 2032, la déduction immédiate"
       " coûte cher parce que l'État rembourse aussi la transition (près de 12 Md€ en 2033) ; une fois celle-ci passée,"
       " vers 2040, elle ne coûte plus qu'environ 1,5 Md€ par an et la marge de l'ensemble atteint environ 13 Md€. Hachures : options non retenues, non comptées dans le solde (coût après réaction des"
       " contribuables ; entre parenthèses, le solde qui en résulterait). Non comptée : fin de l'effacement des plus-values au décès"
       " (environ 1 milliard à terme, gardé en réserve).")
out = dict(blocs=[dict(titre=t, items=[dict(libelle=l, Md=v) for l, v in it], sous_total=sum(v for _, v in it))
                  for t, it in BLOCS], solde=solde, annee=ANNEE, unite="Md€ de 2026")
(S / "bilan_v5.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
print([(t, round(sum(v for _, v in it), 2)) for t, it in BLOCS], round(solde, 2))
