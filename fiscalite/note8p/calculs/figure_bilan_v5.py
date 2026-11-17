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


def blocs(an):
    """Lignes du bilan pour une année de caisse (euros de 2027 environ). L'impôt sur le revenu est en régime installé
    dès 2030 (décomposition statique) : mêmes valeurs en 2032 et en 2040."""
    f, c, dd = FA[str(an)], CA[str(an)], (1 + G) ** (an - AREF)
    px = PXA.get(an, PX if an >= 2032 else 0.0)
    return [
        ("Nouvel impôt sur le revenu", [
            ("Suppression des niches", K25 * K["vraies_niches"]),
            ("Pensions imposées comme les salaires", K25 * K["alignement_pensions"]),
            ("Fin du quotient conjugal", K25 * K["unite_fiscale"]),
            ("Fin du quotient familial", K25 * CB["qf"]),
            ("Fin de la CSG déductible", K25 * K["technique_csg_deductible"]),
            ("Forfait de 500 € au lieu du 10 % et des frais réels", K25 * K["technique_frais"]),
            (f"Franchise de {_fr(PAR['franchise_enfant'])} € par enfant", K25 * (K["quotient_familial_vers_franchise"] - CB["qf"])),
            ("Baisse des taux (nouveau barème)", K25 * K["bareme"]),
            ("Minimum vieillesse ; contribution sur les hauts revenus", K25 * (K["aspa_nette"] + K["cehr_absorbee"])),
        ]),
        ("Fiscalité foncière", [
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


BLOCS, B32 = blocs(2040), blocs(2032)
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
assert abs(solde - B["solde"]) < 0.05, (solde, B["solde"])
lignes.append(("solde", "Solde de l'ensemble", solde, y))
# options non retenues (hors solde) : baisse du PFU (sorties/pfu_options.json, après réaction)
PO = L("pfu_options.json")
y -= 1.4
OPTS = []
for k, lib in (("30", "Option : prélèvement forfaitaire unique à 30 %"), ("25", "Option : prélèvement forfaitaire unique à 25 %")):
    OPTS.append((lib, -PO[k]["central"], y))
    V32[lib] = -PO[k]["central"]
    y -= 1


def lab(v):
    r = round(v)
    if r == 0:
        return "≈ 0"
    return ("+" if r > 0 else "−") + _fr(abs(r))


fig, ax = plt.subplots(figsize=(PLEINE, 4.9))
for typ, t, v, yy in lignes:
    if typ == "item":
        ax.barh(yy, v, color=HAUSSE if v > 0 else PROP, height=0.66, zorder=2)
        ax.text(v + (1.2 if v >= 0 else -1.2), yy, lab(v), va="center", ha="left" if v >= 0 else "right", fontsize=7.2,
                color=ENCRE2)
    else:
        ax.barh(yy, v, color=AUJ, height=0.66, zorder=2)
        ax.text(v + (1.2 if v >= 0 else -1.2), yy, lab(v), va="center", ha="left" if v >= 0 else "right", fontsize=7.4,
                color=ENCRE, fontweight="bold")
for typ, t, v, yy in lignes:
    v2 = V32[t]
    diff = abs(round(v2) - round(v)) >= 1
    ax.text(47, yy, lab(v2), va="center", ha="right", fontsize=7.2 if typ == "item" else 7.4,
            color=HAUSSE if diff else ENCRE2, fontweight="bold" if (diff or typ != "item") else "normal")
ax.text(47, lignes[0][3] + 0.9, "En 2032", ha="right", fontsize=7.2, color=ENCRE, fontweight="bold")
ax.text(-110, lignes[0][3] + 0.9, "Réforme installée (2040)", ha="left", fontsize=7.2, color=ENCRE, fontweight="bold")
for lib, v, yy in OPTS:
    ax.barh(yy, v, color="white", edgecolor=HAUSSE, hatch="////", height=0.66, zorder=2, lw=0.8)
    ax.text(v - 1.2, yy, lab(v) + f"  (solde : {lab(solde + v)})", va="center", ha="right", fontsize=7.2, color=HAUSSE)
    ax.text(47, yy, lab(v), va="center", ha="right", fontsize=7.2, color=HAUSSE)
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
ax.set_xlim(-112, 49)
ax.set_xticks([-100, -80, -60, -40, -20, 0, 20])
ax.set_xlabel("Milliards d'euros par an, réforme installée (+ : l'État prélève davantage ; − : il prélève moins)",
              fontsize=7)
axes(ax, grille="x")
ax.spines["left"].set_visible(False)
ax.tick_params(axis="y", length=0)
sauver(fig, "figure_bilan",
       "calculs des auteurs : modèle de foyers calé sur les statistiques de l'impôt sur le revenu 2024 (DGFiP) ; coûts des"
       " niches : Évaluation des voies et moyens PLF 2026, CPO (2026) ; foncier : DVF et comptes de patrimoine (Insee) ;"
       " impôt sur les sociétés : recettes 2025 et coût du crédit d'impôt recherche (PLF 2027) ; annexes B à F.",
       "Barres : recettes de 2040, réforme installée ; colonne de droite : recettes de 2032, en ocre quand elles diffèrent. Euros de 2027 environ, arrondis au milliard. Gris : total de chaque bloc. Impôt sur le revenu :"
       " décomposition séquentielle avant réaction des comportements (l'ordre change la taille de chaque ligne, pas le"
       " total). Taxe foncière communale inchangée. Taxe nationale sur le sol nette de sa déductibilité des bénéfices."
       " Impôt sur les sociétés : rendements prudents, après réaction des entreprises ; en 2040, la déduction immédiate"
       " est à son coût permanent ; en 2032 et surtout en 2033 (près de 12 Md€), l'État rembourse aussi"
       " la transition. Hachures : options non retenues, non comptées dans le solde (coût après réaction des"
       " contribuables ; entre parenthèses, le solde qui en résulterait). Non comptée : fin de l'effacement des plus-values au décès"
       " (environ 1 milliard à terme, gardé en réserve).")
out = dict(blocs=[dict(titre=t, items=[dict(libelle=l, Md=v) for l, v in it], sous_total=sum(v for _, v in it))
                  for t, it in BLOCS], solde=solde, annee=2040, unite="Md€ de 2026")
(S / "bilan_v5.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
print([(t, round(sum(v for _, v in it), 2)) for t, it in BLOCS], round(solde, 2))
