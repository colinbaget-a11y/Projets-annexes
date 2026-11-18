"""Tableaux de la note (v7, format de la partie III) : écrits en LaTeX dans tableaux/, à partir des seules sorties JSON.
Tableau 1 : recettes 2025 (Insee 3.217), après réforme (régime de croisière), solde 2032 et en régime de croisière.
Tableaux 2 à 5 : composantes de chaque mesure, avec leur statut (OBS, DED, CAL, HYP). Md€ de 2025.
"""
import json
from pathlib import Path

D = Path(__file__).resolve().parent.parent
S, T = D / "sorties", D / "tableaux"
T.mkdir(exist_ok=True)
L = lambda n: json.loads((S / n).read_text(encoding="utf-8"))  # noqa: E731
P = json.loads((D / "parametres.json").read_text(encoding="utf-8"))
I = L("insee_t3217_2025.json")
B = L("bouclage4.json")["annuel"]
BI = L("bilan_v5.json")
IS4 = L("is4.json")["annuel_caisse"]
NP, FP = L("is3.json")["niches_paquet"], P["doublons_partie3"]["facteurs_prudents"]
PART = sum(FP[k] * NP[k]["montant_2026"] for k in P["doublons_partie3"]["niches_is_conservees"]) / sum(FP[k] * NP[k]["montant_2026"] for k in FP)
PO = L("pfu_options.json")
CR = "2040"                                   # régime de croisière : transition de la déduction immédiate achevée
G = P["croissance_nominale"]


def f(v, signe=False, d=1):
    if v is None:
        return ""
    r = round(v, d)
    if r == 0:
        r = 0.0
    s = f"{abs(r):.{d}f}".replace(".", ",")
    if signe:
        return ("+" if r > 0 else ("$-$" if r < 0 else "")) + s
    return ("$-$" if r < 0 else "") + s


def is_lignes(an):
    c, dd = IS4[an], (1 + G) ** (int(an) - 2025)
    pertes = B[an]["is_revalorisation_deficits"]
    return {"taux_reduit": c["is_fin_taux_reduit_prudent"] / dd,
            "culture": PART * c["is_niches_rendement_prudent_realisable"] / dd,
            "deduction": (c["is_deduction_50_depart_2029"] + c["is_reinvest_logiciels_acquis"] + c["is_reinvest_deduction_75_puis_100"]) / dd,
            "pertes": pertes}


IS32, ISC = is_lignes("2032"), is_lignes(CR)
assert abs(sum(IS32.values()) - (B["2032"]["is_net_prudent"] + B["2032"]["is_revalorisation_deficits"])) < 0.01
fon = lambda an: {"sol": B[an]["foncier_taxe_sol"], "dmto": B[an]["foncier_dmto"], "autres": B[an]["foncier_autres"]}  # noqa: E731
F32, FC = fon("2032"), fon(CR)

ir, csg, crds = I["irpp_avant_credits"] + I["irpp_credits_imputes"] + I["irpp_credits_restitues"], I["csg"], I["crds"]
tf, dm = I["taxe_fonciere"], I["dmto_collectivites"]
is_ = I["is_avant_credits"] + I["is_credits_imputes"] + I["is_credits_restitues"]
dm_perm = -2 * FC["dmto"]                       # droits au taux permanent (hors majoration temporaire de 2025-2028)
apres = {"ir": ir + csg + crds, "tf": tf, "sol": FC["sol"], "dm": dm_perm / 2, "is": is_ + sum(ISC.values()) - ISC["pertes"] + ISC["pertes"]}
s32 = {"ir": 0.0, "fon": sum(F32.values()), "is": sum(IS32.values())}
scr = {"ir": 0.0, "fon": sum(FC.values()), "is": sum(ISC.values())}
assert abs(sum(s32.values()) - B["2032"]["solde"]) < 0.01 and abs(sum(scr.values()) - B[CR]["solde"]) < 0.01
rec_tot = ir + csg + crds + tf + dm + is_
apr_tot = apres["ir"] + apres["tf"] + apres["sol"] + apres["dm"] + apres["is"]

R = []
R.append(r"\textbf{1. Nouvel impôt sur le revenu} & \textbf{" + f(ir + csg + crds) + "} & \\textbf{" + f(apres["ir"]) + "} & \\textbf{" + f(s32["ir"], 1) + "} & \\textbf{" + f(scr["ir"], 1) + r"} \\")
R.append(r"\quad Impôt sur le revenu, net des crédits d'impôt & " + f(ir) + r" & fusionnés & & \\")
R.append(r"\quad CSG & " + f(csg) + r" & & & \\")
R.append(r"\quad CRDS & " + f(crds) + r" & & & \\")
R.append(r"\textbf{2. Fiscalité foncière} & \textbf{" + f(tf + dm) + "} & \\textbf{" + f(apres["tf"] + apres["sol"] + apres["dm"]) + "} & \\textbf{" + f(s32["fon"], 1) + "} & \\textbf{" + f(scr["fon"], 1) + r"} \\")
R.append(r"\quad Taxe foncière communale (sol et bâti) & " + f(tf) + " & " + f(apres["tf"]) + r" & 0,0 & 0,0 \\")
R.append(r"\quad Taxe nationale sur la valeur du sol & 0,0 & " + f(apres["sol"]) + " & " + f(F32["sol"], 1) + " & " + f(FC["sol"], 1) + r" \\")
R.append(r"\quad Droits de mutation à titre onéreux & " + f(dm) + " & " + f(apres["dm"]) + " & " + f(F32["dmto"], 1) + " & " + f(FC["dmto"], 1) + r" \\")
R.append(r"\quad Déductibilité de la taxe sur le sol, calendrier & & & " + f(F32["autres"], 1) + " & " + f(FC["autres"], 1) + r" \\")
R.append(r"\textbf{3. Impôt sur les sociétés} & \textbf{" + f(is_) + "} & \\textbf{" + f(apres["is"]) + "} & \\textbf{" + f(s32["is"], 1) + "} & \\textbf{" + f(scr["is"], 1) + r"} \\")
R.append(r"\textbf{4. Prélèvement forfaitaire unique (inchangé)} & & & \textbf{0,0} & \textbf{0,0} \\")
R.append(r"\midrule \textbf{Total} & \textbf{" + f(rec_tot) + "} & \\textbf{" + f(apr_tot) + "} & \\textbf{" + f(sum(s32.values()), 1) + "} & \\textbf{" + f(sum(scr.values()), 1) + r"} \\")


def table(nom, titre, entete, cols, lignes, source, label):
    txt = (r"\begin{table}[!htbp]\small\setlength{\tabcolsep}{4pt}" "\n"
           r"\caption{" + titre + r"}\label{" + label + "}\n"
           r"\begin{tabularx}{\linewidth}{@{}" + cols + "@{}}\n\\toprule\n" + entete + r" \\" "\n\\midrule\n"
           + "\n".join(lignes) + "\n\\bottomrule\n\\end{tabularx}\n"
           r"\par\vspace{2pt}{\raggedright\scriptsize\color{gris}" + source + r"\par}" "\n\\end{table}\n")
    (T / f"{nom}.tex").write_text(txt, encoding="utf-8")


table("tab1", "Recettes des impôts concernés et solde public (Md€ de 2025)",
      r"\textbf{Mesure et impôts concernés} & \textbf{Recettes 2025} & \textbf{Après réforme} & \textbf{Solde 2032} & \textbf{Solde à terme}",
      "Xrrrr", R,
      "Source : Insee, comptes nationaux 2025, tableau 3.217 (recettes 2025) ; calculs des auteurs. Après réforme et solde"
      " à terme : régime de croisière, une fois achevée la transition vers la déduction immédiate des investissements"
      f" (recettes de {CR} rapportées à l'économie de 2025). Les droits de mutation de 2025 comprennent la hausse"
      " temporaire autorisée jusqu'en 2028 ; le solde est calculé par rapport au taux permanent (16,1 Md€). L'effet sur"
      " les prélèvements obligatoires est égal au solde public.", "tab:t1")

# Tableau 2 : impôt sur le revenu (décomposition séquentielle, identique en 2032 et à terme)
it = {i["libelle"]: i["Md"] for i in BI["blocs"][0]["items"]}
g = lambda pref: sum(v for k, v in it.items() if k.startswith(pref))  # noqa: E731
L2 = [("Suppression des niches (réductions et crédits, exonérations, demi-parts)", g("Niches"), "DED"),
      ("Pensions imposées comme les salaires (abattement, CSG, âge)", g("Retraités"), "DED"),
      ("Forfait de 500 € au lieu de l'abattement de 10 % et des frais réels", g("Salariés"), "DED"),
      ("Fin de la CSG déductible", g("Fin de la CSG"), "DED"),
      ("Impôt individuel, fin du quotient conjugal", g("Impôt individuel"), "DED"),
      ("Fin du quotient familial", g("Fin du quotient"), "DED"),
      (f"Franchise de {P['franchise_enfant']:,.0f} € par enfant".replace(",", "\\,"), g("Franchise"), "HYP"),
      ("Baisse de tous les taux (nouveau barème)", g("Baisse"), "CAL"),
      ("Minimum vieillesse, contribution sur les hauts revenus", g("Minimum"), "DED")]
R2 = [f"{a} & {f(v, True)} & {s} \\\\" for a, v, s in L2]
R2.append(r"\midrule \textbf{Solde public} & \textbf{" + f(sum(v for _, v, _ in L2), True) + r"} & \\")
table("tab2", "Composantes du nouvel impôt sur le revenu (Md€ de 2025, 2032 et à terme)",
      r"\textbf{Composante} & \textbf{Md€} & \textbf{Statut}", "Xrc", R2,
      "Source : modèle de foyers calé sur les statistiques de l'impôt sur le revenu 2024 (DGFiP) ; OpenFisca-France ;"
      " coûts des niches : Évaluation des voies et moyens (PLF 2026). Décomposition séquentielle avant réaction des"
      " comportements : l'ordre change la taille de chaque ligne, pas le total. Statut : DED, déduit d'une donnée"
      " observée ; CAL, calé (ici sur la neutralité par rapport au droit de 2032) ; HYP, paramètre choisi.", "tab:t2")

R3 = [("Taxe nationale sur la valeur du sol (taux de " + f(100 * L("foncier3.json")["scenarios"][P["scenario_foncier"]]["taux"]["tn_sol"] / 100, d=2) + " %)", F32["sol"], FC["sol"], "HYP"),
      ("Déductibilité de la taxe sur le sol, calendrier de recouvrement", F32["autres"], FC["autres"], "DED"),
      ("Droits de mutation divisés par deux", F32["dmto"], FC["dmto"], "OBS"),
      ("Taxe communale sur la valeur de marché, en deux parts", 0.0, 0.0, "HYP")]
R3 = [f"{a} & {f(x, True)} & {f(y, True)} & {s} \\\\" for a, x, y, s in R3] + [
    r"\midrule \textbf{Solde public} & \textbf{" + f(sum(F32.values()), True) + "} & \\textbf{" + f(sum(FC.values()), True) + r"} & \\"]
table("tab3", "Composantes de la réforme foncière (Md€ de 2025)",
      r"\textbf{Composante} & \textbf{2032} & \textbf{À terme} & \textbf{Statut}", "Xrrc", R3,
      "Source : valeurs foncières des ventes (DVF), comptes de patrimoine de l'Insee ; droits de mutation au taux"
      " permanent, 16,1 Md€ en 2025 (OFGL, DGFiP) ; calculs des auteurs. Assiette du sol : 6\\,156 Md€ après la baisse"
      " de valeur que provoque la taxe (construite, non observée). La taxe communale garde sa recette de 2025.", "tab:t3")

c32 = IS4["2032"]["is_cir_suppression_statique"] / (1 + G) ** 7
R4 = [("Fin du taux réduit de 15 % des petites entreprises", IS32["taux_reduit"], ISC["taux_reduit"], "DED"),
      ("Fin des crédits d'impôt culture (cinéma, jeux vidéo, spectacle)", IS32["culture"], ISC["culture"], "DED"),
      ("Déduction immédiate des investissements (25 % en 2029, 50 % en 2030, 100 % en 2032)", IS32["deduction"], ISC["deduction"], "DED"),
      ("Revalorisation des déficits reportables au taux de l'État", IS32["pertes"], ISC["pertes"], "HYP")]
R4 = [f"{a} & {f(x, True)} & {f(y, True)} & {s} \\\\" for a, x, y, s in R4] + [
    r"\midrule \textbf{Solde public} & \textbf{" + f(sum(IS32.values()), True) + "} & \\textbf{" + f(sum(ISC.values()), True) + r"} & \\",
    r"\midrule \emph{Pour mémoire, compté en partie III : recentrage du crédit d'impôt recherche} & \emph{+5,2} & \emph{+5,2} & \\",
    r"\emph{Pour mémoire, compté en partie III : mécénat, zonages, crédit famille} & & & \\",
    r"\emph{Variante : suppression du tiers restant du crédit d'impôt recherche} & \emph{" + f(B["2032"]["variante_cir_tiers_restant"], True) + "} & \\emph{" + f(B[CR]["variante_cir_tiers_restant"], True) + r"} & HYP \\"]
table("tab4", "Composantes de la réforme de l'impôt sur les sociétés (Md€ de 2025)",
      r"\textbf{Composante} & \textbf{2032} & \textbf{À terme} & \textbf{Statut}", "Xrrc", R4,
      "Source : Insee (recettes 2025) ; DGFiP, \\emph{Statistiques} n\\textsuperscript{o}~51 ; Évaluation des voies et moyens"
      " (PLF 2026) ; calculs des auteurs. Rendements après une décote de 10 à 25~\\% pour la réaction des entreprises."
      " La déduction immédiate coûte davantage en 2032 qu'à terme parce que l'État rembourse encore les amortissements des"
      " investissements passés. Variante : 2,6 Md€ après recentrage, décote de 20~\\%.", "tab:t4")

R5 = []
for k, taux in (("30", "47,5"), ("25", "44")):
    o = PO[k]
    R5.append(f"Prélèvement forfaitaire unique à {k}~\\% & {f(-o['statique'], True)} & {f(-o['central'], True)} & {f(-o['bas'], True)} à {f(-o['haut'], True)} & {taux}~\\% \\\\")
table("tab5", "Coût d'une baisse du prélèvement forfaitaire unique (Md€ de 2025, option non retenue)",
      r"\textbf{Option} & \textbf{Statique} & \textbf{Après réaction} & \textbf{Fourchette} & \textbf{Taux cumulé}", "Xrrrr", R5,
      "Source : DGFiP (dividendes, intérêts et plus-values déclarés au titre de 2024, 80 Md€) ; élasticité du revenu"
      " déclaré de 0,22 à 0,96 (Lefebvre, Lehmann et Sicsic) ; Sénat pour le rendement constaté de la hausse de 2026."
      " Taux cumulé : impôt sur les sociétés à 25~\\% puis prélèvement sur le dividende, à comparer aux 48~\\% du haut du"
      " nouvel impôt sur le revenu.", "tab:t5")

out = dict(recettes_2025=dict(ir=ir, csg=csg, crds=crds, tf=tf, dmto=dm, is_=is_, total=rec_tot), apres=apres, apres_total=apr_tot,
           solde_2032=s32, solde_terme=scr, is_2032=IS32, is_terme=ISC, foncier_2032=F32, foncier_terme=FC,
           po_terme_points=100 * sum(scr.values()) / I["pib_2025"], cir_statique_modele=c32)
(S / "tableaux_v7.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
print(json.dumps(out, ensure_ascii=False, indent=0)[:1500])
