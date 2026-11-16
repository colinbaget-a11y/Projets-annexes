"""Bloc IR-CSG-CRDS : écrit note8p/annexes/annexe_ircsg.tex à partir de sorties/ircsg.json (python3, après
ircsg_proposition.py). Les tableaux sont produits ici pour que chaque chiffre de l'annexe soit reproductible."""
import json
from pathlib import Path

RACINE = Path(__file__).resolve().parents[2]
D = json.loads((RACINE / "note8p/sorties/ircsg.json").read_text(encoding="utf-8"))


def n(v, d=0, signe=False):
    v = round(float(v), d)
    if v == 0:
        v = 0.0
    s = f"{v:+,.{d}f}" if signe and v != 0 else f"{v:,.{d}f}"
    s = s.replace(",", "\\,").replace(".", "{,}").replace("-", "$-$").replace("+", "$+$")
    return s


P, B, E, R = D["perimetre"], D["bareme"], D["efficacite"]["par_jeu_perception"], D["repartition"]
V, C, TM = D["variantes"], D["cas_types"], D["taux_marginaux"]
rc = P["reconciliation_ir"]
r25 = P["recettes_2025"]
cp = B["cout_par_point"]
L = [r"% Annexe du bloc IR-CSG-CRDS (note8p, 17/11/2026). Écrit par note8p/calculs/ircsg_annexe.py à partir de",
     r"% note8p/sorties/ircsg.json ; ne pas modifier à la main.", ""]

# ------------------------------------------------------------------ 1. champ
L += [r"\subsection{Champ, recette et données}", "",
      r"\paragraph{Champ.} Le nouvel impôt remplace l'IR des revenus imposés au barème (salaires, pensions, chômage,"
      r" bénéfices des indépendants, revenus fonciers), la CSG et la CRDS des revenus d'activité et de remplacement, et la"
      r" CEHR due sur ces revenus. Les revenus du capital mobilier et les plus-values (PFU, option pour le barème comprise)"
      r" relèvent du bloc capital. En 2025 : IR " + n(r25["ir_bareme"], 1) + r"~Md€, CSG " + n(r25["csg_activite"] + r25["csg_pensions"] + r25["csg_chomage"], 1)
      + r"~Md€ (activité " + n(r25["csg_activite"], 1) + ", pensions " + n(r25["csg_pensions"], 1) + ", chômage "
      + n(r25["csg_chomage"], 1) + r"), CRDS " + n(r25["crds"], 1) + r"~Md€, soit " + n(r25["total_modele"], 1)
      + r"~Md€ ; s'y ajoutent la CEHR du barème (" + n(P["cehr_bareme"], 2) + r"~Md€ sur " + n(P["cehr_total"], 2)
      + r", au prorata des revenus du barème dans le revenu fiscal des tranches qui la paient, hypothèse) et les avantages"
      r" maintenus pour l'invalidité et la dépendance (" + n(sum(P["avantages_maintenus"].values()), 2)
      + r"~Md€, PLF 2026, Voies et moyens). Recette à tenir : " + n(P["cible"], 1) + r"~Md€.", "",
      r"\paragraph{Réconciliation de l'IR.} Comptes nationaux 2025 : " + n(rc["ir_comptes_nationaux_2025"], 1)
      + r"~Md€ ; IRCOM des revenus 2024 porté en 2025 : " + n(rc["ir_ircom_porte_2025"], 1) + r" ; IR imputé par le modèle"
      r" aux revenus du capital (12,8~\% de 90~Md€, convention de 2024) : " + n(rc["ir_impute_capital_modele"], 1)
      + r" ; IR au PFU mesuré par le bloc capital (revenus 2025) : " + n(rc["ir_pfu_mesure_bloc_capital"], 1)
      + r". L'écart de " + n(rc["ecart_non_attribue"], 1) + r"~Md€ n'est pas attribué : IR des revenus du capital imposés"
      r" au barème par option (hors de notre périmètre), assurance-vie et plus-values immobilières comptées à tort dans les"
      r" 90~Md€, erreur de répartition. S'il s'agissait en entier d'IR sur des revenus du barème, la recette à tenir"
      r" monterait d'autant, soit $+$" + n(rc["ecart_non_attribue"] / cp["tous_taux"], 2) + r"~point sur tous les taux.", "",
      r"\paragraph{Modèle.} Foyers « purs » de \texttt{synthese/modele\_purs.py} : 25 tranches de l'IRCOM des revenus 2024,"
      r" 60 foyers représentatifs par tranche, chacun scindé en foyers d'actifs et de retraités dans la proportion des"
      r" pensions de la tranche ; couples homogènes, quatre partages des revenus (100/0, 88/12, 70/30, 55/45, Insee) ;"
      r" 1,97~M de parents isolés (un enfant chacun) et deux enfants par couple « avec enfants » ; charge actuelle répartie"
      r" entre types par des cas-types OpenFisca sans niche, puis recalée en 2025 composante par composante. Les cas-types"
      r" sont recalculés avec OpenFisca-France 176.1 (droit des revenus 2025 ; IR, CEHR, CDHR, CSG, CRDS ; taux de CSG des"
      r" pensions en régime stable) par \texttt{note8p/calculs/ircsg\_openfisca.py}.", ""]

# ------------------------------------------------------------------ 2. taux marginaux
rows = []
for b, u in TM["salarie_seul"].items():
    a = u["auj"]
    rows.append(f"{n(float(b))} & {n(a['total'], 1)} & {n(a['ir'], 1)} & {n(a['cehr'], 1)} & {n(a['csg'] + a['crds'], 1)}"
                f" & {n(u['naive'], 1)} & {n(u['proposition'], 0)} \\\\")
th = D["taux_marginaux_theoriques_haut"]
L += [r"\subsection{Taux marginaux d'aujourd'hui sur une assiette comparable}", "",
      r"Le taux marginal est le prélèvement supplémentaire sur 100~€ de revenu après cotisations en plus, calculé point par"
      r" point par OpenFisca sur une grille de 100~€ (salarié seul du privé, sans enfant). Les taux nominaux ne"
      r" s'additionnent pas : la CSG et la CRDS portent sur 98,25~\% du brut (100~\% au-delà de quatre plafonds), donc aussi"
      r" sur les cotisations ; l'IR porte sur le revenu imposable, net de la CSG déductible (6,8 points) et des frais"
      r" professionnels (10~\%, plafonnés). Au sommet, par euro de revenu après cotisations : entre 4 et 8 plafonds, IR "
      + n(th["4_a_8_pass"]["ir"], 1) + " + CSG " + n(th["4_a_8_pass"]["csg"], 1) + " + CRDS " + n(th["4_a_8_pass"]["crds"], 2)
      + " = " + n(th["4_a_8_pass"]["total_sans_cehr"], 1) + r"~\% ; au-delà de 8 plafonds, " + n(th["au_dela_8_pass"]["total_sans_cehr"], 1)
      + r"~\% ; plus " + n(th["4_a_8_pass"]["cehr3"], 1) + " ou " + n(th["4_a_8_pass"]["cehr4"], 1) + r" points de CEHR."
      r" La CDHR ne joue pas pour un salarié (taux moyen supérieur à 20~\%). Médianes sur la grille : "
      + n(TM["max_haut_auj"]["entre_250_450k"], 1) + r"~\% entre 250\,000 et 450\,000~€, " + n(TM["max_haut_auj"]["au_dela_550k"], 1)
      + r"~\% au-delà de 550\,000~€ ; maximum " + n(TM["max_haut_auj"]["max"], 1) + r"~\%.", "",
      r"\begin{table}[h]\centering\footnotesize\setlength{\tabcolsep}{4pt}",
      r"\caption{Taux marginal sur 100~€ de revenu après cotisations, salarié seul (\%)}\label{tab:ircsg8_tm}",
      r"\begin{tabular}{rrrrrrr}\hline",
      r"Revenu (€) & Aujourd'hui & dont IR & dont CEHR & dont CSG-CRDS & Naïve & Proposition \\ \hline",
      *rows, r"\hline\end{tabular}",
      r"\par\footnotesize Fusion naïve : barème de l'IR (sans décote ni abattement) sur le revenu après cotisations, plus "
      + n(100 * V["naive"]["tau"], 1) + r"~\% sur tout le revenu (recette égale). Source : OpenFisca-France 176.1 ; calculs des auteurs.",
      r"\end{table}", ""]

# ------------------------------------------------------------------ 3. barème et variantes
vk = [("proposition", "Proposition"), ("bareme_30_100k", "30~\\% de 44 à 100~k€"),
      ("seuil_exoneration", "Seuil de 10\\,000~€ à 0~\\%"), ("top_40", "Taux supérieur de 40~\\%"),
      ("top_50", "Taux supérieur de 50~\\%"), ("franchise_4000", "Franchise de 4\\,000~€/enfant"),
      ("franchise_8000", "Franchise de 8\\,000~€/enfant"), ("qc_plafond_2000", "Quotient conj. plafonné (2\\,000~€)"),
      ("qc_sans_plafond", "Quotient conj. sans plafond"), ("naive", "Fusion naïve")]
rows = []
for k, lib in vk:
    v = V[k]
    g = v["groupes"]
    rows.append(f"{lib} & {n(v['gain'], 1)} & {n(v['gain_vue05'], 1)} & {n(v['gain_vue0'], 1)} & {n(v['emplois'] / 1e3)}"
                f" & {n(g['retraites']['Md'], 1, True)} & {n(g['couples2']['eur'], 0, True)} & {n(v['top1'], 1, True)}"
                f" & {n(v['cas']['mono2_60'], 0, True)} & {n(v['cas']['couple0m_80'], 0, True)} \\\\")
L += [r"\subsection{Choix du barème et variantes}", "",
      r"\paragraph{Exploration.} 1\,800 barèmes à quatre taux ont été essayés (\texttt{ircsg\_explore.py}, \texttt{ircsg\_affinage.py}),"
      r" chacun calé sur la recette : taux d'entrée de 0 à 10~\% jusqu'à 6\,000 à"
      r" 16\,000~€, deux taux intermédiaires, taux supérieur de 40 à 50~\% au-delà de 80\,000 à 150\,000~€. Le gain"
      r" d'efficacité croît toujours quand le barème s'aplatit (le plus efficace à taux supérieur de 45~\%, 15~\% jusqu'à 100\,000~€ puis 45~\%, gagne"
      r" 5,6~Md€ et rend 21~Md€ au dixième le plus aisé) : sans pondération d'équité, le modèle mène à un impôt"
      r" proportionnel. Le choix est donc un choix de politique, guidé par cinq règles : un taux constant de 0,6 à 1,9 Smic"
      r" (enseignement de Bozio et Wasmer, 2024) ; aucun salarié au Smic perdant ; taux supérieur de 45~\% sur le 1~\% le"
      r" plus aisé ; chiffres ronds ; à progressivité égale, le barème le plus robuste à la perception de la CSG. Le seuil"
      r" de 36\,500~€ est calé sur la recette (" + n(B["recette"], 2) + r"~Md€, écart " + n(B["ecart"], 2, True)
      + r"). Coût d'un point : tous les taux " + n(cp["tous_taux"], 1) + r"~Md€ ; 20 et 28~\% " + n(cp["taux_20_30"], 1)
      + r" ; 45~\% " + n(cp["taux_45"], 2) + r" ; 1\,000~€ de franchise par enfant " + n(cp["franchise_enfant_1000"], 1) + r"~Md€.", "",
      r"\begin{table}[h]\centering\scriptsize\setlength{\tabcolsep}{3pt}",
      r"\caption{Variantes, recette constante (taux intermédiaires recalés)}\label{tab:ircsg8_var}",
      r"\begin{tabular}{lrrrrrrrrr}\hline",
      r" & \multicolumn{3}{c}{Gain (Md€), CSG perçue} & Emplois & Retraités & Couple, 2 enf. & 1~\% & Mono-act. & Couple 1 rev. \\",
      r" & entière & moitié & nulle & (milliers) & (Md€) & (€/foyer) & (Md€) & 60\,k€ (€) & 80\,k€ (€) \\ \hline",
      *rows, r"\hline\end{tabular}",
      r"\par Gain : variation de perte sèche réelle, jeu central ; perception sur les heures et l'effort, la décision de"
      r" travailler se prenant sur le salaire net. Mono-act. : famille à un revenu, deux enfants, 60\,000~€ brut ; couple"
      r" 1 rev. : sans enfant, 80\,000~€ brut.",
      r"\end{table}", ""]

# ------------------------------------------------------------------ 4. répartition
dec = R["deciles_eur"]
gr = R["groupes"]
pa = R["par_partage_couple"]
cf = D["courbes_familles"]
prof = [("seul", "Salarié seul"), ("couple_0enf", "Couple biactif, sans enfant"), ("couple_0enf_mono", "Couple à un revenu, sans enfant"),
        ("couple_2enf", "Couple biactif, 2 enfants"), ("couple_2enf_mono", "Couple à un revenu, 2 enfants"),
        ("couple_3enf", "Couple biactif, 3 enfants"), ("couple_3enf_mono", "Couple à un revenu, 3 enfants"),
        ("parent_isole_2enf", "Parent isolé, 2 enfants"), ("retraite_seul", "Retraité seul"), ("retraite_couple", "Couple de retraités")]
niv = (20e3, 30e3, 40e3, 60e3, 80e3, 100e3, 150e3)
rows = []
for k, lib in prof:
    d_ = {r["brut"]: r["delta"] for r in cf[k]}
    rows.append(lib + " & " + " & ".join(n(round(d_[x], -1), 0, True) for x in niv) + r" \\")
L += [r"\subsection{Résultats distributifs}", "",
      r"\paragraph{Déciles.} Variation moyenne par foyer fiscal (€ par an), déciles de foyers classés par revenu fiscal"
      r" (IRCOM) : " + " ; ".join(f"D{i + 1} {n(u, 0, True)}" for i, u in enumerate(dec)) + r". Le dixième le plus aisé paie "
      + n(-R["top10_Md"], 1) + r"~Md€ de moins, le 1~\% " + n(-R["top1_Md"], 1) + r"~Md€ de moins. Les déciles 3 et 4, où"
      r" les retraités modestes sont nombreux, paient le plus. Actifs " + n(gr["actifs"]["Md"], 1, True) + r"~Md€ ("
      + n(gr["actifs"]["eur"], 0, True) + r"~€ par foyer) ; retraités " + n(gr["retraites"]["Md"], 1, True) + r"~Md€ ("
      + n(gr["retraites"]["eur"], 0, True) + r"~€) ; " + n(R["perdants500_pct"], 0) + r"~\% des foyers paient plus de 500~€"
      r" de plus.", "",
      r"\paragraph{Couples et impôt individuel.} Variation moyenne selon la part du revenu du couple gagnée par le premier"
      r" conjoint (100/0, 88/12, 70/30, 55/45) : couples d'actifs sans enfant " + " / ".join(
          n(pa[f"couples0_{s}"]["eur"], 0, True) for s in ("1.0", "0.88", "0.7", "0.55")) + r"~€ ; avec enfants "
      + " / ".join(n(pa[f"couples2_{s}"]["eur"], 0, True) for s in ("1.0", "0.88", "0.7", "0.55")) + r"~€ ; couples de retraités "
      + " / ".join(n(pa[f"retraites_{s}"]["eur"], 0, True) for s in ("1.0", "0.88", "0.7", "0.55")) + r"~€. Les perdants de"
      r" l'individualisation sont les couples aux revenus très inégaux.", "",
      r"\begin{table}[h]\centering\footnotesize",
      r"\caption{Variation de l'impôt par configuration familiale, selon le revenu brut du ménage (€ par an)}\label{tab:ircsg8_fam}",
      r"\begin{tabular}{l" + "r" * len(niv) + r"}\hline",
      " & " + " & ".join(n(x / 1e3) + r"\,k€" for x in niv) + r" \\ \hline", *rows, r"\hline\end{tabular}",
      r"\par Cas-types OpenFisca (salariés du privé, couples mariés ou pacsés, biactifs à 60/40 ; retraités de plus de"
      r" 65 ans, pension brute) ; charge d'aujourd'hui : IR, CEHR, CSG, CRDS.", r"\end{table}", ""]

# ------------------------------------------------------------------ 5. efficacité
jeux = ("bas", "central", "haut")
perc = [("vue_1", "entière"), ("vue_05", "moitié (heures, effort)"), ("vue_0", "nulle (heures, effort)"),
        ("vue_05_deux_marges", "moitié (deux marges)"), ("vue_0_deux_marges", "nulle (deux marges)")]
rows = []
for k, lib in perc:
    rows.append(lib + " & " + " & ".join(n(E[f"{j}_{k}"]["gain"], 1) for j in jeux) + " & "
                + " & ".join(n(E[f"{j}_{k}"]["emplois"] / 1e3) for j in jeux) + " & " + n(E[f"central_{k}"]["pib_long_pct"], 2, True) + r" \\")
pf = D["efficacite"]["pensions_futures"]
L += [r"\subsection{Efficacité et effets réels}", "",
      r"\paragraph{Méthode.} Celle de \texttt{revue/methode\_v2.md}, recopiée dans \texttt{ircsg\_modele.evalue} pour"
      r" appliquer la perception de la CSG aux deux marges. Marge intensive : $\Delta Q = e\,g\,[\ln(1-t_1) - \ln(1-\tilde t_0)]$,"
      r" où $t_1$ est le taux marginal du nouvel impôt (entièrement perçu), $\tilde t_0$ le taux actuel perçu (IR, plus la"
      r" part perçue de la CSG-CRDS) ; chaque euro perdu coûte le coin moyen total non contributif (impôt, cotisations"
      r" non contributives, retrait de la prime d'activité, inchangés). Élasticités du revenu réel 0,02/0,05/0,10 sous la"
      r" médiane, 0,05/0,10/0,20 au-dessus (0,25 au sommet dans le jeu haut). Marge extensive : même formule sur le taux"
      r" de prélèvement du premier salaire, adultes gagnant moins de deux Smic, $\eta$ = 0,10/0,25/0,50. Le revenu déclaré"
      r" du dixième supérieur est un effet sur la recette (non compté).", "",
      r"\begin{table}[h]\centering\footnotesize",
      r"\caption{Gain d'efficacité (Md€ par an), emplois (milliers) et PIB potentiel, selon la perception de la CSG}\label{tab:ircsg8_eff}",
      r"\begin{tabular}{lrrrrrrr}\hline",
      r"CSG d'aujourd'hui perçue & \multicolumn{3}{c}{Gain : bas, central, haut} & \multicolumn{3}{c}{Emplois} & PIB (\%) \\ \hline",
      *rows, r"\hline\end{tabular}",
      r"\par PIB : Cobb-Douglas (part du travail 2/3), capital ajusté, jeu central ; à capital donné, deux tiers de ces chiffres.",
      r"\end{table}", "",
      r"Le gain central s'annule sous " + n(100 * D["efficacite"]["perception_seuil"]) + r"~\% de perception. Pensions"
      r" futures : hausse du taux moyen sur les pensions de " + n(100 * pf["dtau"], 1) + r"~points, soit un prélèvement"
      r" implicite de " + n(100 * pf["kappa"], 2) + r"~point sur le salaire ($\kappa = 0{,}274\,\Delta\tau$, part"
      r" contributive des cotisations) ; gain " + n(pf["theta_0.0"], 1) + " s'il n'est pas vu, " + n(pf["theta_0.5"], 1)
      + " à moitié, " + n(pf["theta_1.0"], 1) + r" en entier.", ""]

# ------------------------------------------------------------------ 6. retraités, trajectoire, limites
rt = D["retraites"]
dr = rt["droit_actuel_reperes"]
an = D["annuel"]
L += [r"\subsection{Retraités, trajectoire et limites}", "",
      r"\paragraph{Retraités.} Hausse de " + n(rt["hausse_Md"], 1) + r"~Md€ (" + n(rt["hausse_pct_pensions"], 1)
      + r"~\% des pensions ; charge actuelle " + n(rt["charge_actuelle_Md"], 1) + r"~Md€). Repères en droit actuel : abattement"
      r" de 10~\% " + n(dr["abattement_10"], 2) + r"~Md€ ; abattement des plus de 65 ans " + n(dr["abattement_age_157bis"], 2)
      + r" ; demi-part des anciens combattants " + n(dr["demi_part_combattants_74"], 2) + r" ; CSG de toutes les pensions"
      r" au taux de 9,2~\% : $+$" + n(dr["csg_vers_taux_activite"], 1) + r"~Md€ (approximation). Le nouveau barème rend une"
      r" partie de ces sommes (taux de 5~\% jusqu'à 12\,000~€, 45~\% au sommet). Variation par retraité seul : P10 "
      + n(rt["distribution"]["seuls"]["p10"], 0, True) + ", médiane " + n(rt["distribution"]["seuls"]["p50"], 0, True)
      + ", P90 " + n(rt["distribution"]["seuls"]["p90"], 0, True) + r"~€ ; par couple : médiane "
      + n(rt["distribution"]["couples"]["p50"], 0, True) + ", P90 " + n(rt["distribution"]["couples"]["p90"], 0, True) + r"~€.", "",
      r"\paragraph{Trajectoire.} Chaque foyer paie $(1-\lambda)$ fois l'ancien impôt et $\lambda$ fois le nouveau,"
      r" $\lambda$ = 0,25 ; 0,5 ; 0,75 ; 1 de 2027 à 2030 : la recette est constante chaque année. En 2030 (Md€, niveau"
      r" 2025) : retraités " + n(an["2030"]["ircsg_hausse_retraites"], 2, True) + r", actifs " + n(an["2030"]["ircsg_baisse_actifs"], 2, True)
      + r", CEHR du barème " + n(an["2030"]["ircsg_cehr_bareme_absorbee"], 2, True) + r", invalidité et dépendance "
      + n(an["2030"]["ircsg_invalidite_dependance_maintenus"], 2, True) + r", total " + n(an["2030"]["ircsg_total"], 2, True)
      + r". L'extinction de la CRDS après 2033 (droit en vigueur) se traduit en 2034 par une baisse de "
      + n(D["crds_2034"]["baisse_points_tous_taux"], 2) + r"~point de tous les taux, hors bilan de la réforme.", "",
      r"\paragraph{Limites.} Foyers synthétiques (pas de ménages mixtes actifs-retraités, pas de familles de trois enfants"
      r" ou plus dans le modèle agrégé, niches réelles réparties au prorata) ; perception de la CSG non mesurée ;"
      r" suppression des crédits d'impôt (emploi à domicile, garde d'enfants : 8,8~Md€) héritée du modèle ; IR non attribué"
      r" de " + n(rc["ecart_non_attribue"], 1) + r"~Md€ ; IR de 2025 peut-être à un point haut ; répartition des revenus au"
      r" PFU entre tranches inconnue ; pas de demande de travail ni de réaction des retraités ; frontaliers et non-résidents"
      r" (CJCE, C-169/98) à expertiser.", ""]
(RACINE / "note8p/annexes/annexe_ircsg.tex").write_text("\n".join(L) + "\n", encoding="utf-8")
print("annexe écrite")
