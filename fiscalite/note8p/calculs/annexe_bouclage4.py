"""Écrit annexes/annexe_bouclage.tex (scénario central unique) à partir de sorties/bouclage4.json et is4.json."""
import json
from pathlib import Path

D = Path(__file__).resolve().parent.parent
S = D / "sorties"
A = json.loads((S / "bouclage4.json").read_text(encoding="utf-8"))["annuel"]
IS = json.loads((S / "is4.json").read_text(encoding="utf-8"))["annuel_caisse"]
ans = sorted(A)
f = lambda x: ("$-$" if x < -0.049 else "") + f"{abs(x):.1f}".replace(".", "{,}")
dfl = lambda a: 1.03 ** (int(a) - 2026)
isl = [("\\quad dont fin du taux réduit", ["is_fin_taux_reduit_prudent"]),
       ("\\quad dont fin du CIR (prudent)", ["is_cir_suppression_realisable_prudent"]),
       ("\\quad dont autres niches de l'IS (prudent)", ["is_niches_rendement_prudent_realisable"]),
       ("\\quad dont déduction immédiate", ["is_deduction_50_depart_2029", "is_reinvest_logiciels_acquis",
                                           "is_reinvest_deduction_75_puis_100"])]
L = [("Taxe nationale sur le sol", "foncier_taxe_sol"), ("Droits de mutation", "foncier_dmto"),
     ("Report, déductibilité, calendrier", "foncier_autres"), ("Impôt sur les sociétés, solde prudent", "is_net_prudent")]
t = ["\\begin{table}[!htbp]\\centering\\scriptsize\\setlength{\\tabcolsep}{2.1pt}",
     "\\caption{Trajectoire complète du scénario central (Md€ par an, années d'encaissement, euros de 2026 ;"
     " + = recette publique en plus)}",
     "\\begin{tabular}{@{}l" + "r" * len(ans) + "@{}}\\toprule", " & " + " & ".join(a[2:] for a in ans) + " \\\\ \\midrule"]
for lab, k in L:
    t.append(lab + " & " + " & ".join(f(A[a][k]) for a in ans) + " \\\\")
    if k == "is_net_prudent":
        for lab2, ks in isl:
            t.append(lab2 + " & " + " & ".join(f(sum(IS[a].get(x, 0) for x in ks) / dfl(a)) for a in ans) + " \\\\")
t.append("Revalorisation des déficits reportables & " + " & ".join(f(A[a]["is_revalorisation_deficits"]) for a in ans) + " \\\\")
t.append("Baisse supplémentaire de l'impôt sur le travail & " + " & ".join(f(A[a]["ir_financement_externe"]) for a in ans) + " \\\\")
t.append("\\textbf{Solde} & " + " & ".join("\\textbf{" + f(A[a]["solde"]) + "}" for a in ans) + " \\\\")
t.append("\\emph{Réserve : plus-values (prudent)} & " + " & ".join(f(A[a]["reserve_plus_values"]) for a in ans) + " \\\\")
t += ["\\bottomrule\\end{tabular}", "\\end{table}"]
txt = r"""\subsection{Un seul scénario central, des recettes prudentes}
Règles [C] : aucune année de déficit ; chaque baisse n'entre en vigueur qu'avec la recette qui la finance ; les recettes
incertaines (niches de l'IS, crédit d'impôt recherche) sont comptées à leur rendement prudent, après réaction des
entreprises et extinction des créances existantes ; les recettes de la fin de l'effacement des plus-values ne financent
rien (réserve) ; les évolutions du droit en vigueur (fin de la contribution exceptionnelle sur l'IS ; extinction de la
CRDS fin 2033) ne sont ni comptées ni utilisées. La fusion de l'IR et de la CSG monte en charge de 2027 à 2030 à recette
constante chaque année (les niches supprimées financent la baisse du barème au rythme de leur extinction) ; la ligne
« baisse supplémentaire » est le financement externe qu'elle reçoit, minimum vieillesse corrigé compris, et net du coût de la revalorisation des déficits reportables de l'impôt sur les sociétés, qu'il finance. Taxe
nationale sur le sol par tiers en 2029-2031, droits de mutation baissés au même rythme. Déduction immédiate de 50~\% dès
2029, 75~\% en 2033, 100~\% en 2036, logiciels acquis inclus dès 2031. Montants en euros de 2026 : séries d'IS déflatées de 3~\% par an, niveaux 2025 (foncier, impôt sur le revenu) majorés de 3~\%. Les
excédents des premières années, qui viennent de l'IS encaissé avant la montée en charge de la déduction, sont gardés
comme marge ; le solde est d'au moins 0,58~Md€ chaque année à partir de 2028 (programme
\texttt{calculs/bouclage4.py}).

"""
(D / "annexes" / "annexe_bouclage.tex").write_text(txt + "\n".join(t) + "\n", encoding="utf-8")
print("annexe_bouclage.tex écrit")
