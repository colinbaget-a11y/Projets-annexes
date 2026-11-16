"""Tableaux LaTeX de la partie IR-CSG (corps et annexe), écrits depuis les sorties des programmes (aucune recopie à
la main) : situation_ircsg, naive_ircsg, proposition_ircsg, arbitrages_prop_ircsg, transition_ircsg,
architectures_ircsg, controle_hauts_purs.

Lancer depuis fiscalite/, après ces programmes : python3 synthese/tables_ircsg.py
Fichiers écrits dans synthese/parties/ :
- tab_ircsg_cas.tex     ménages types : aujourd'hui, réforme naïve, proposition (corps, sous-partie 4) ;
- tab_ircsg_arb.tex     arbitrages : gain, financement, qui paie (corps, sous-partie 5) ;
- tab_ircsg_arbcas.tex  arbitrages : ménages types (annexe) ;
- tab_ircsg_trans.tex   transition : hausse annuelle des principaux perdants (annexe) ;
- tab_ircsg_dec.tex     déciles de toutes les variantes (annexe) ;
- tab_ircsg_design.tex  franchise contre taux d'entrée (annexe) ;
- tab_ircsg_sens.tex    sensibilités du gain et du haut de la distribution (annexe) ;
- tab_ircsg_hyp.tex     hypothèses fortes et chiffres non vérifiés (annexe) ;
- tab_ircsg_arch.tex    architectures de la méthode v2 (annexe, architectures_ircsg.json).
"""
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
S = HERE / "sorties"
OUT = HERE / "parties"


def lit(nom):
    return json.loads((S / nom).read_text(encoding="utf-8"))


SIT, NAIF, PROP = lit("situation_ircsg.json"), lit("naive_ircsg.json"), lit("proposition_ircsg.json")
ARB, TR, ARCH = lit("arbitrages_prop_ircsg.json"), lit("transition_ircsg.json"), lit("architectures_ircsg.json")
P = PROP["evaluations"]["proposition"]
NQ = NAIF["quotient"]


def n(x, d=0, signe=True):
    if x is None:
        return "---"
    s = f"{x:+,.{d}f}" if signe else f"{x:,.{d}f}"
    s = s.replace(",", " ").replace(".", ",").replace(" ", "\\,")
    if s.startswith("-"):
        s = "$-$" + s[1:]
    if re.fullmatch(r"[+]?0(,0*)?", s) or re.fullmatch(r"\$-\$0(,0*)?", s):
        s = s.lstrip("+").replace("$-$", "")
    return s


def gain(r):
    return f"{n(r['gain_central'], 1, False)} ({n(r['gain_bas'], 1, False)} à {n(r['gain_haut'], 1, False)})"


def ecrire(nom, lignes):
    (OUT / f"{nom}.tex").write_text("\n".join(lignes) + "\n", encoding="utf-8")


def note(texte):
    return [r"\par\vspace{3pt}\parbox{\linewidth}{\raggedright\scriptsize\color{encre}", texte + "}"]


# ------------------------------------------------------------------ ménages types
CAS_CORPS = ["smic_mi", "smic", "cadre60", "cadre100", "cadre200", "pi_smic", "c0_50", "c0m_80", "c2_50", "c2m_50",
             "c3_60", "c3m_60", "ret12", "ret16", "ret20", "ret25", "ret35", "rc30", "rc45"]
L = [r"\begin{table}[!htbp]\centering\scriptsize\setlength{\tabcolsep}{4pt}",
     r"\caption{Ce que paieraient des ménages types (IR + CSG + CRDS, € par an)}\label{tab:ircsg_cas}",
     r"\begin{tabular}{@{}lrrr@{}}", r"\toprule",
     r"& Aujourd'hui & \multicolumn{2}{c}{Variation} \\ \cmidrule(l){3-4}",
     r"& & Réforme naïve & Proposition \\", r"\midrule"]
for k in CAS_CORPS:
    c = P["cas"][k]
    L.append(f"{c['libelle']} & {n(c['auj'], 0, False)} & {n(NQ['cas'][k]['delta'])} & {n(c['delta'])} \\\\")
L += [r"\bottomrule", r"\end{tabular}"]
L += note(r"Cas-types OpenFisca-France (législation des revenus 2025) : salariés du privé et retraités de plus de 65 ans, "
          r"sans autre revenu ni niche ; revenus bruts ; couples mariés ou pacsés, revenus partagés 60/40 sauf « un seul "
          r"revenu » ; Smic 2025 de 21\,622~€ par an. Réforme naïve : barème de l'IR du foyer (quotient conjugal et familial) "
          r"et taux proportionnel de " + n(100 * NQ["tau"], 2, False) + r"~\% sur l'assiette large. Proposition : sous-partie "
          r"\ref{sec:ircsg}.4. Retraités : leur taux de CSG dépend du revenu fiscal de l'avant-dernière année, pris en régime "
          r"stable (même pension chaque année).")
L.append(r"\end{table}")
ecrire("tab_ircsg_cas", L)

# ------------------------------------------------------------------ arbitrages
A = ARB


def ligne_arb(lib, r, pts=None):
    if r is None:
        return f"{lib} & \\multicolumn{{7}}{{c}}{{aucun barème ne respecte les contraintes}} \\\\"
    dd = r["distribution"]
    pts_s = "---" if pts is None else n(pts, 2)
    return (f"{lib} & {gain(r)} & {n(r['extensif'], 1, False)} & {pts_s} & {n(r['groupes']['retraites']['Md'], 1)} & "
            f"{n(r['top1_Md'], 1)} & {n(r['dec_eur'][9])} & {n(dd['retraites']['p90'])} \\\\")


L = [r"\begin{table}[!htbp]\centering\scriptsize\setlength{\tabcolsep}{3pt}",
     r"\caption{Les arbitrages : ce qu'on gagne, ce que cela coûte, qui paie}\label{tab:ircsg_arb}",
     r"\resizebox{\linewidth}{!}{%", r"\begin{tabular}{@{}lrrrrrrr@{}}", r"\toprule",
     r"& Gain d'efficacité & dont & Points & Retraités & 1~\% & 10\textsuperscript{e} & Retraités, \\",
     r"& Md€ (fourchette) & participation & pour tous & Md€ & du haut & décile & 90\textsuperscript{e} \\",
     r"& & Md€ & & & Md€ & € par foyer & centile (€) \\", r"\midrule",
     ligne_arb(r"\textbf{Proposition}", A["proposition"]),
     r"\multicolumn{8}{@{}l}{\emph{1. Le couple}} \\",
     ligne_arb(r"\quad Quotient conjugal et familial (repli constitutionnel)", A["quotient_c"]),
     r"\multicolumn{8}{@{}l}{\emph{2. Les pensions}} \\",
     ligne_arb(r"\quad Abattement de 5~\%", A["abat5_c"]),
     ligne_arb(r"\quad Abattement de 10~\%", A["abat10_c"]),
     ligne_arb(r"\quad Sortie de l'exonération étalée jusqu'à 37\,500~€", A["sortie_etalee_c"]),
     r"\multicolumn{8}{@{}l}{\emph{3. Les enfants}} \\",
     ligne_arb(r"\quad Chèque de " + n(A["cheque_egal"]["cheque"], 0, False) + r"~€ par enfant (même coût)", A["cheque_egal_c"]),
     ligne_arb(r"\quad Chèque de " + n(A["cheque_qf"]["cheque"], 0, False) + r"~€ (coût du quotient familial)", A["cheque_qf"],
               A["cheque_qf"]["points"]),
     ligne_arb(r"\quad Aucune aide aux enfants dans l'impôt", A["sans_enfant"], A["sans_enfant"]["points"]),
     r"\multicolumn{8}{@{}l}{\emph{4. La franchise d'activité}} \\",
     ligne_arb(r"\quad 4\,000~€ au lieu de 8\,000~€", A["franchise_4000"]),
     ligne_arb(r"\quad Aucune franchise, taux d'entrée bas", A["franchise_0"]),
     r"\multicolumn{8}{@{}l}{\emph{5. Le haut du barème}} \\",
     ligne_arb(r"\quad Le 1~\% le plus aisé peut payer moins", A["haut_baisse"]),
     ligne_arb(r"\quad Idem, et déciles à $\pm$1\,000~€", A["libre_1000"]),
     r"\bottomrule", r"\end{tabular}}"]
L += note(r"Gain d'efficacité : baisse de la perte sèche statique sur l'activité, à court terme, par rapport à aujourd'hui "
          r"(hypothèses centrales ; basses et hautes entre parenthèses). Sauf « points pour tous », chaque variante garde le "
          r"calibrage de la proposition (recette de " + n(PROP["cible"], 1, False) + r"~Md€ ; répartition inchangée : aucun décile au-delà de $\pm$500~€, charge du 1~\% inchangée ; "
          r"rubrique 5 : 1~\% libre de baisser) et le barème est recherché de nouveau ; « points pour tous » : la recette est "
          r"rétablie en ajoutant ce nombre de points à tous les taux sous 50~\%, sans ce calibrage. Optimum "
          r"d'efficacité (sans contrainte de répartition) : " + n(-A["atteignable"]["v2_central"], 1, False) + r"~Md€, le "
          r"dixième le plus aisé payant " + n(-A["atteignable"]["top10_Md"], 0, False) + r"~Md€ de moins.")
L.append(r"\end{table}")
ecrire("tab_ircsg_arb", L)

CAS_ARB = ["smic", "cadre100", "pi_smic", "c0m_80", "c2m_50", "c3_60", "c3m_60", "ret16", "ret20", "ret25", "rc45"]
COLS = [("Proposition", A["proposition"]), ("Quotient", A["quotient_c"]), ("Abatt. 10~\\%", A["abat10_c"]),
        ("Chèque", A["cheque_egal_c"]), ("Franchise 4\\,000~€", A["franchise_4000"])]
L = [r"\begin{table}[!htbp]\centering\scriptsize\setlength{\tabcolsep}{3pt}",
     r"\caption{Les arbitrages pour des ménages types (variation de l'IR + CSG + CRDS, € par an)}\label{tab:ircsg_arbcas}",
     r"\resizebox{\linewidth}{!}{%", r"\begin{tabular}{@{}l" + "r" * len(COLS) + r"@{}}", r"\toprule",
     "& " + " & ".join(c for c, _ in COLS) + r" \\", r"\midrule"]
for k in CAS_ARB:
    L.append(P["cas"][k]["libelle"] + " & " + " & ".join(n(r["cas"][k]["delta"]) if r else "---" for _, r in COLS) + r" \\")
L += [r"\bottomrule", r"\end{tabular}}"]
L += note(r"Mêmes cas-types que le tableau~\ref{tab:ircsg_cas}. Quotient : imposition commune des couples, quotient conjugal "
          r"et familial aux plafonds actuels à la place de la franchise par enfant ; abattement de 10~\% sur les pensions en "
          r"plus de l'exonération des petites pensions ; chèque de " + n(A["cheque_egal"]["cheque"], 0, False) + r"~€ par enfant, "
          r"de même coût que la franchise de 6\,000~€ par enfant ; franchise d'activité de 4\,000~€ par adulte au lieu de "
          r"8\,000~€. Chaque variante a son propre barème, recherché dans le même cadre.")
L.append(r"\end{table}")
ecrire("tab_ircsg_arbcas", L)

# ------------------------------------------------------------------ transition
H = TR["hausses"]
L = [r"\begin{table}[!htbp]\centering\scriptsize\setlength{\tabcolsep}{4pt}",
     r"\caption{Hausse annuelle des principaux perdants selon la durée de la transition (€ par an)}\label{tab:ircsg_trans}",
     r"\begin{tabular}{@{}lrrrr@{}}", r"\toprule",
     r"& Hausse finale & \multicolumn{3}{c}{Hausse chaque année, transition sur} \\ \cmidrule(l){3-5}",
     r"& & 3 ans & 5 ans & 10 ans \\", r"\midrule"]
for lib in ("Retraités, médiane", "Retraités, 90e centile", "Couples de retraités, 90e centile", "Retraités, 99e centile",
            "Tous les foyers, 90e centile", "Retraité seul, pension de 16 000 €", "Retraité seul, pension de 20 000 €",
            "Retraité seul, pension de 25 000 €", "Couple de retraités, 45 000 € de pensions (60/40)",
            "Couple sans enfant à un seul revenu, 80 000 €"):
    if lib in H:
        u = H[lib]
        lib_t = lib.replace("90e", r"90\textsuperscript{e}").replace("99e", r"99\textsuperscript{e}")
        L.append(f"{lib_t} & {n(u['finale'])} & {n(u['an3'], 0, False)} & {n(u['an5'], 0, False)} & {n(u['an10'], 0, False)} \\\\")
L += [r"\bottomrule", r"\end{tabular}"]
L += note(r"Convergence linéaire : chaque année, chaque foyer paie une part croissante du nouvel impôt et décroissante de "
          r"l'ancien, ce qui tient la recette chaque année. Centiles : foyers représentatifs du modèle (la dispersion réelle "
          r"des hausses est plus forte ; le 99\textsuperscript{e} centile en est un minorant). Cas-types : tableau~\ref{tab:ircsg_cas}.")
L.append(r"\end{table}")
ecrire("tab_ircsg_trans", L)

# ------------------------------------------------------------------ annexe : déciles
E = PROP["evaluations"]
L = [r"\begin{table}[!htbp]\centering\scriptsize\setlength{\tabcolsep}{3pt}",
     r"\caption{Variation de l'impôt par décile de revenu fiscal, toutes variantes (€ par foyer et par an)}\label{tab:ircsg_dec}",
     r"\resizebox{\linewidth}{!}{%", r"\begin{tabular}{@{}l" + "r" * 10 + r"rr@{}}", r"\toprule",
     "& " + " & ".join(f"D{i}" for i in range(1, 11)) + r" & 1~\% (Md€) & Retraités (Md€) \\", r"\midrule"]
for lib, r in (("Réforme naïve (quotient, " + n(100 * NQ["tau"], 2, False) + r"~\%)", NQ),
               (r"Réforme naïve, variante individuelle (" + n(100 * NAIF["individuel"]["tau"], 2, False) + r"~\%)", NAIF["individuel"]),
               (r"\textbf{Proposition}", E["proposition"]), (r"Variante : franchise de 4\,000~€", E["franchise_4000"]),
               ("Variante : sans franchise", E["sans_franchise"]), ("Quotient conjugal et familial", A["quotient_c"]),
               (r"Abattement de 10~\% sur les pensions", A["abat10_c"]), ("Chèque par enfant (même coût)", A["cheque_egal_c"]),
               (r"Le 1~\% peut payer moins", A["haut_baisse"]), ("Barème neutre (méthode v2)", E["neutre"]),
               (r"Ancienne proposition (1~\% en baisse)", E["ancienne"])):
    L.append(lib + " & " + " & ".join(n(u) for u in r["dec_eur"]) + f" & {n(r['top1_Md'], 1)} & {n(r['groupes']['retraites']['Md'], 1)} \\\\")
L += [r"\bottomrule", r"\end{tabular}}"]
L += note(r"Déciles de foyers fiscaux classés par revenu fiscal de référence (IRCOM, revenus 2024 ; montants de 2025). Moyennes de foyers "
          r"représentatifs : elles cachent les écarts à l'intérieur de chaque décile (sous-partie~\ref{sec:ircsg}.4).")
L.append(r"\end{table}")
ecrire("tab_ircsg_dec", L)

# ------------------------------------------------------------------ annexe : franchise contre taux d'entrée
L = [r"\begin{table}[!htbp]\centering\scriptsize\setlength{\tabcolsep}{3pt}",
     r"\caption{Franchise d'activité contre taux d'entrée : le meilleur barème pour chaque combinaison}\label{tab:ircsg_design}",
     r"\resizebox{\linewidth}{!}{%", r"\begin{tabular}{@{}rrrrrrrl@{}}", r"\toprule",
     r"Franchise & Taux & Gain & dont & Retraités & \multicolumn{2}{c}{Premier salaire (\%)} & Barème \\ \cmidrule(lr){6-7}",
     r"(€) & d'entrée & Md€ & participation & Md€ & mi-temps & Smic & \\", r"\midrule"]
for r in sorted(PROP["par_design"], key=lambda r: (r["F"], r["t0"])):
    if round(100 * r["t0"]) % 2:
        continue
    bar = (f"{n(100 * r['tb'], 0, False)}~\\% à 20~k€, {n(100 * r['t1'], 1, False)}~\\% à {n(r['z1'] / 1e3, 1 if r['z1'] % 1000 else 0, False)}~k€, "
           f"50~\\% à {n(r['z2'] / 1e3, 0, False)}~k€")
    L.append(f"{n(r['F'], 0, False)} & {n(100 * r['t0'], 0, False)}~\\% & {n(r['gain'], 2, False)} & {n(r['part'], 2, False)} & "
             f"{n(r['retraites'], 1)} & {n(r['ptr_mi'], 1, False)} & {n(r['ptr_smic'], 1, False)} & {bar} \\\\")
L += [r"\bottomrule", r"\end{tabular}}"]
L += note(r"Pour chaque franchise d'activité (par adulte) et chaque taux d'entrée (taux sur le premier euro imposé après la "
          r"franchise), le barème le plus efficace parmi ceux qui respectent la recette, les déciles à $\pm$500~€ et la "
          r"charge inchangée du 1~\%. Sont aussi fixées : l'exonération des petites pensions, la franchise de 6\,000~€ par enfant, la "
          r"déduction de l'épargne retraite. Premier salaire : taux de prélèvement IR-CSG d'une personne seule qui prend un "
          r"emploi au Smic, à mi-temps ou à temps plein (aujourd'hui : " + n(SIT["ptr_auj"]["seul_mi"], 1, False) + r"~\%). "
          r"Taux d'entrée pairs seulement ; " + str(PROP["n_essais"]) + r" barèmes essayés, " + str(PROP["n_ok"]) +
          r" admissibles. La proposition retient la combinaison qui maximise la participation (franchise de "
          + n(PROP["choix"]["F"], 0, False) + r"~€, taux d'entrée de " + n(100 * PROP["choix"]["t0"], 0, False) + r"~\%).")
L.append(r"\end{table}")
ecrire("tab_ircsg_design", L)

# ------------------------------------------------------------------ annexe : sensibilités
HP = {}
for bloc in (S / "controle_hauts_purs.txt").read_text(encoding="utf-8").split("\n"):
    m = re.match(r"\[(\w+) / proposition_n\] t1 ([\d.]+) % ; perte sèche réelle ([-+\d.]+) Md€ ; 1 % du haut ([-+\d.]+) Md€.*"
                 r"50 % atteint à ([\d,]+) k€", bloc)
    if m:
        HP[m.group(1)] = dict(gain=-float(m.group(3)), top1=float(m.group(4)), z2=float(m.group(5).replace(",", "")))
sal, perm = TR["saillance"], TR["permanent"]["gains"]
L = [r"\begin{table}[!htbp]\centering\scriptsize\setlength{\tabcolsep}{4pt}",
     r"\caption{Ce qui fait varier le gain de la proposition et la charge du 1~\% le plus aisé}\label{tab:ircsg_sens}",
     r"\resizebox{\linewidth}{!}{%", r"\begin{tabular}{@{}lrl@{}}", r"\toprule", r"Hypothèse & Gain (Md€) & Autre effet \\",
     r"\midrule",
     f"Modèle, hypothèses centrales & {n(P['gain_central'], 2, False)} & participation {n(P['extensif'], 2, False)}~Md€ \\\\",
     f"Élasticités basses / hautes & {n(P['gain_bas'], 2, False)} / {n(P['gain_haut'], 2, False)} & \\\\",
     f"Élasticités de long terme (intensif 0,10 à 0,25 ; participation 0,10) & {n(P['gain_long'], 2, False)} & participation "
     f"{n(P['ext_long'], 2, False)}~Md€ \\\\",
     f"CSG perçue à moitié aujourd'hui & {n(sal['0.5']['gain']['central'], 2, False)} & intensif {n(sal['0.5']['intensif'], 2)}~Md€ \\\\",
     f"CSG non perçue aujourd'hui & {n(sal['0.0']['gain']['central'], 2)} & intensif {n(sal['0.0']['intensif'], 2)}~Md€ \\\\",
     f"Régime permanent : impôt futur sur les pensions vu à moitié par les actifs & {n(perm['0.5']['central'], 2, False)} & \\\\",
     f"Régime permanent : vu en entier & {n(perm['1.0']['central'], 2, False)} & prélèvement implicite $+${n(100 * TR['permanent']['kappa'], 2, False)}~point \\\\"]
for conv, lib in (("haut", "revenus au PFU logés en haut (convention « haut »)"), ("prorata", "revenus au PFU au prorata")):
    if conv in HP:
        u = HP[conv]
        L.append(f"Répartition des {lib} & {n(u['gain'], 1, False)} & 1~\\% {n(u['top1'], 1)}~Md€ ; neutre si 50~\\% à "
                 f"{n(u['z2'], 0, False)}~k€ \\\\")
L += [r"\bottomrule", r"\end{tabular}}"]
L += note(r"Gain : baisse de la perte sèche sur l'activité (jeu central sauf mention). CSG non perçue : le revenu d'activité "
          r"ne réagit aujourd'hui qu'à l'IR et réagit après la fusion à tout l'impôt fusionné ; la marge de participation est "
          r"gardée. Régime permanent : la hausse de l'impôt sur les pensions réduit la valeur des droits à pension qu'ouvre "
          r"chaque euro de salaire ; borne haute, ce lien étant faible au bas de l'échelle et nul au-delà de huit fois le "
          r"plafond de la Sécurité sociale. "
          r"Convention centrale de répartition des revenus au PFU : « mixte » (controle\_hauts\_purs.py).")
L.append(r"\end{table}")
ecrire("tab_ircsg_sens", L)

# ------------------------------------------------------------------ annexe : hypothèses fortes et chiffres non vérifiés
s0, s5 = sal["0.0"]["gain"]["central"], sal["0.5"]["gain"]["central"]
HYP = [
    ("Perception de la CSG : la CSG et la CRDS d'aujourd'hui font réagir le revenu d'activité autant que l'IR. Aucune étude ne le mesure.",
     "Tout le gain sur la marge intensive",
     f"Décisif. CSG non perçue : gain {n(s0, 1)}~Md€ au lieu de {n(P['gain_central'], 1, False)} ; perçue à moitié : {n(s5, 1, False)}."),
    ("Élasticités : revenu réel 0,05 (moitié du bas) et 0,10 (au-dessus) ; participation 0,25 sous 2 Smic ; ce sont des choix, pas des estimations françaises.",
     "Tous les gains",
     f"Fourchette {n(P['gain_bas'], 1, False)} à {n(P['gain_haut'], 1, False)}~Md€ ; long terme {n(P['gain_long'], 1, False)}~Md€."),
    ("Les pensions, le chômage et l'épargne ne réagissent pas (âge de départ, surcote, cumul emploi-retraite, sortie en capital).",
     "Mécanisme du financement par les pensions", "Non chiffré ; sens ambigu (une pension nette plus faible pousse à partir plus tard ; un taux marginal élevé dans la zone de sortie de l'exonération pousse en sens inverse)."),
    ("Régime permanent : les actifs ne voient pas que leurs futures pensions seront plus taxées.",
     "Part « permanente » du gain", f"Vu en entier : gain permanent {n(perm['1.0']['central'], 1, False)}~Md€ au lieu de {n(P['gain_central'], 1, False)}."),
    ("Répartition des revenus au PFU entre tranches (non publiée) ; convention « mixte ».",
     "Charge du 1~\\%, forme du haut du barème",
     (f"Convention « haut » (que soutient un calage sur l'IR observé) : 1~\\% {n(HP['haut']['top1'], 1)}~Md€ ; charge inchangée si 50~\\% dès "
      f"{n(HP['haut']['z2'], 0, False)}~k€." if "haut" in HP else "")),
    ("Foyers purs : pas de foyer mixte (couple dont un seul est retraité, retraité bailleur) ; loyers tous chez les actifs.",
     "Coût de la franchise, charge des retraités", "Franchise sous-estimée et hausse des retraités surestimée, jusqu'à 3~Md€ environ (borne grossière)."),
    ("Partage des revenus dans les couples (Insee Première 1492, quatre classes ; le même pour les retraités).",
     "Coût de l'impôt individuel, charge des couples de retraités", "Couples de retraités à 62/38 : charge des retraités plus faible de 2~Md€ environ (registre, H11, ancienne proposition)."),
    ("Enfants : un par parent isolé, deux par couple « avec enfants », aucun chez les retraités et les concubins.",
     "Coût de la franchise par enfant, familles nombreuses", "Familles de trois enfants absentes des agrégats (cas-types seulement)."),
    ("Charge actuelle par type de foyer répartie selon des cas-types sans niche.",
     "Qui paie entre types de foyers", f"Charge actuelle des retraités ({n(SIT['charge_groupes']['retraites'], 1, False)}~Md€) non observable ; niches réparties au prorata."),
    ("Base 2025 : l'IR de 2025 est l'impôt encaissé dans l'année (comptes nationaux), dont la hausse (+7,9~\\%) tient en partie au jeu des acomptes et des soldes du prélèvement à la source ; chaque agrégat de 2024 est porté en 2025 avec la même croissance dans toutes les tranches.",
     "Recette à remplacer, charge actuelle par tranche",
     f"Si cette hausse est passagère, la recette est surestimée d'environ {n(SIT['recettes']['base_2024']['ir'] * (SIT['recettes']['facteurs']['ir'] - SIT['recettes']['facteurs']['csg_activite']), 1, False)}~Md€ (IR porté en 2025 comme les revenus), soit environ 0,4 point de taux."),
    ("Épargne retraite : déduction de 10,6~Md€ (cases 2042) supposée proportionnelle aux revenus d'activité de la moitié haute.",
     "Barème, haut de la distribution", f"Coût de la déduction {n(PROP['cout_per'], 1, False)}~Md€ ({n(100 * PROP['points_per'] if PROP['points_per'] < 0.05 else PROP['points_per'], 2, False)}~point) ; répartition non vérifiée."),
    ("Cas-types : législation des revenus 2025 d'OpenFisca, Smic de 21\\,622~€ (sources secondaires) ; retraités en régime stable (taux de CSG le plus élevé dont le seuil est dépassé par le revenu fiscal calculé à ce taux).",
     "Tous les cas-types, courbes de taux marginaux", "Dans une bande de quelques centaines d'euros autour de chaque seuil de CSG, aucun taux n'est cohérent avec son propre revenu fiscal ; le taux inférieur est retenu, ce qui déplace le saut de moins de 1\\,000~€."),
    ("Valeur actualisée : table de Gompertz calée sur l'espérance de vie à 65 ans (21,8 ans) ; cohortes de retraités de même taille.",
     "Valeur actualisée de la hausse des retraités", "Ordre de grandeur ; 1 à 3~\\% réel donne la fourchette."),
    ("Chiffres non vérifiés sur une source primaire : CSG des pensions de 2024 (CCSS) ; croissance de la CSG par assiette en 2025 (régimes de base et FSV, appliquée à tous les affectataires) ; paramètres 2025 d'OpenFisca (seuils de CSG des pensions, abattement des plus de 65 ans) ; Smic 2025 ; part des familles au plafond du quotient familial ; partage des niches par tranche ; l'IRCOM inclut l'IR au PFU et exclut la CEHR.",
     "Calage, cas-types, récit", "Registre revue/hypotheses\\_ircsg.md, section 4."),
]
L = [r"\begin{table}[!htbp]\centering\scriptsize\setlength{\tabcolsep}{3pt}",
     r"\caption{Hypothèses fortes et chiffres non vérifiés}\label{tab:ircsg_hyp}",
     r"\begin{tabular}{@{}p{0.43\linewidth}p{0.2\linewidth}p{0.33\linewidth}@{}}", r"\toprule",
     r"Hypothèse & Où elle joue & Ce qu'elle change si elle est fausse \\", r"\midrule"]
for h, o, e in HYP:
    L.append(f"{h} & {o} & {e} \\\\[2pt]")
L += [r"\bottomrule", r"\end{tabular}"]
L += note(r"Source : registre revue/hypotheses\_ircsg.md (hypothèses H1 à H20), chiffres recalculés pour la proposition par "
          r"transition\_ircsg.py, controle\_hauts\_purs.py et proposition\_ircsg.py.")
L.append(r"\end{table}")
ecrire("tab_ircsg_hyp", L)

# ------------------------------------------------------------------ annexe : architectures (méthode v2)
AT = ARCH["atteignable"]


def ligne_v2(nom, r, pts=None):
    g = r["groupes"]
    pts_s = "---" if pts is None else n(100 * pts, 1)
    return (f"{nom} & {pts_s} & {n(-r['v2_central'], 1, False)} ({n(-r['v2_bas'], 1, False)} à {n(-r['v2_haut'], 1, False)}) & "
            f"{100 * r['v2_central'] / AT['v2_central']:.0f}~\\% & {r['perdants500']:.0f}~\\% & {n(g['retraites']['Md'], 1)} & "
            f"{n(r['top10_Md'], 1)} \\\\")


AA = {r["nom"]: r for r in ARCH["architectures"]}
cle = lambda deb: next(r for k, r in AA.items() if k.startswith(deb))  # noqa: E731
L = [r"\begin{table}[!htbp]\centering\scriptsize\setlength{\tabcolsep}{3pt}",
     r"\caption{Un dispositif à la fois : architectures simples comparées au barème neutre}\label{tab:ircsg_arch}",
     r"\resizebox{\linewidth}{!}{%", r"\begin{tabular}{@{}lrrrrrr@{}}", r"\toprule",
     r"& Points & Gain d'efficacité & Part du gain & Perdants & Retraités & 10~\% du \\",
     r"& pour tous & Md€ (fourchette) & atteignable & $>$ 500~€ & Md€ & haut, Md€ \\", r"\midrule",
     ligne_v2("Barème neutre", cle("Barème neutre"), 0.0)]
for lib, deb in (("\\quad + franchise d'activité 4\\,000~€", "Neutre + franchise d'activité 4 000 €"),
                 ("\\quad + franchise d'activité 8\\,000~€", "Neutre + franchise d'activité 8 000 €"),
                 ("\\quad + franchise de 8\\,000~€ sur tous les revenus", "Neutre + franchise de 8"),
                 ("\\quad + franchise de 6\\,000~€ par enfant", "Neutre + franchise de 6"),
                 ("\\quad + chèque de " + n(SIT["qf_agregat"]["cheque"], 0, False) + "~€ par enfant", "Neutre + chèque"),
                 ("\\quad + quotient conjugal et familial", "Neutre + quotient"),
                 ("\\quad + abattement de 10~\\% sur les pensions", "Neutre + abattement"),
                 ("\\quad + petites pensions exonérées", "Neutre + petites")):
    r = cle(deb)
    L.append(ligne_v2(lib, r, r["d"]))
L += [ligne_v2("Optimum d'efficacité, sans franchise", ARCH["optimum_r"]),
      ligne_v2("Gain atteignable (optimum, franchise de 4\\,000~€)", AT), r"\bottomrule", r"\end{tabular}}"]
_bn = ARCH["neutre"]
L += note(r"Barème neutre : " + n(100 * _bn[0], 0, False) + r"~\% au premier euro, " + n(100 * _bn[1], 0, False) + r"~\% à 20\,000~€, "
          + n(100 * _bn[3], 1, False) + r"~\% à " + n(_bn[2] / 1e3, 0, False) + r"\,000~€, 50~\% à " + n(_bn[4] / 1e3, 0, False)
          + r"\,000~€, le plus proche de "
          r"ce que chaque foyer paie aujourd'hui ; sans déduction de l'épargne retraite. Chaque dispositif est financé par des "
          r"points ajoutés à tous les taux sous 50~\% (architectures\_ircsg.py).")
L.append(r"\end{table}")
ecrire("tab_ircsg_arch", L)
print("tableaux écrits :", ", ".join(sorted(p.name for p in OUT.glob("tab_ircsg_*.tex"))))
