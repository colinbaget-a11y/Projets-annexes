"""Écrit annexes/annexe_bouclage.tex (v3) à partir de sorties/bouclage3.json."""
import json
from pathlib import Path
D = Path(__file__).resolve().parent.parent
B = json.loads((D / "sorties" / "bouclage3.json").read_text(encoding="utf-8"))
A, P, F = B["annuel"], B["prudent"], B["financement_ir"]
ans = sorted(A)
f = lambda x: ("$-$" if x < -0.049 else "") + f"{abs(x):.1f}".replace(".", "{,}")
L = [("Taxe nationale sur le sol", "taxe_fonciere"), ("Droits de mutation", "dmto"),
     ("Report, déductibilité, calendrier", "foncier_autres"), ("Fin du taux réduit d'IS", "is_taux_reduit"),
     ("Niches de l'IS", "is_niches"), ("Déduction immédiate de 50~\\%", "is_deduction_50"),
     ("Fusion IR-CSG (montée en charge)", "ircsg_fusion"), ("Baisse supplémentaire de l'impôt sur le travail", "ircsg_financement_externe"),
     ("\\textbf{Solde, scénario central}", "solde"), ("Réserve : plus-values (prudent)", "reserve_plus_values")]
t = ["\\begin{table}[!htbp]\\centering\\scriptsize\\setlength{\\tabcolsep}{2.3pt}",
     "\\caption{Trajectoire complète (Md€ par an, années d'encaissement ; + = recette publique en plus)}",
     "\\begin{tabular}{@{}l" + "r" * len(ans) + "@{}}\\toprule", " & " + " & ".join(a[2:] for a in ans) + " \\\\ \\midrule"]
t += [lab + " & " + " & ".join(f(A[a][k]) for a in ans) + " \\\\" for lab, k in L]
t.append("Solde, scénario prudent (avant clause) & " + " & ".join(f(P[a]["solde"] + F[a]) for a in ans) + " \\\\")
t += ["\\bottomrule\\end{tabular}", "\\end{table}"]
txt = r"""\subsection{Règles, calendrier et scénario prudent}
Règles : aucune année de déficit dans le scénario central ; les recettes de la fin de l'effacement des plus-values ne
financent rien (réserve) ; les évolutions du droit en vigueur (fin de la contribution exceptionnelle sur l'IS, $-7$~Md€ ;
extinction de la CRDS fin 2033) ne sont ni comptées ni utilisées. Calendrier [C] : fusion IR-CSG montée en charge de
2027 à 2030 à recette constante (chaque foyer paie $(1-\lambda)$ ancien impôt $+\ \lambda$ nouvel impôt) ; taxe nationale
sur le sol par tiers en 2029-2031 et droits de mutation baissés au même rythme, avec clause de suspension ; taux réduit
d'IS à 20~\% pour l'exercice 2027, aligné ensuite ; niches de l'IS dès l'exercice 2028 ; déduction de 50~\% dès
l'exercice 2029 (25~\% la première année) ; baisse supplémentaire de l'impôt sur le travail par paliers de 1~Md€ de 2032
à 2036, puis 5,5~Md€. Unités : euros de 2027 environ ; séries d'IS déflatées de leur croissance nominale (3~\% par an).

Scénario prudent [H] : niches de l'IS rapportant 25~\% de moins, déduction plus coûteuse de 20~\% (part imposable de
90~\%), taxe sur le sol plus faible de 10~\% (capitalisation plus forte). Sans les paliers de baisse sur le travail, le
solde serait de $-2{,}9$~Md€ en 2031 et $-1{,}7$~Md€ en 2032, couverts par l'excédent cumulé de 2028-2030 (5,0~Md€) :
la dette ne dépasse jamais celle du droit actuel. La clause qui conditionne chaque palier aux recettes constatées
limiterait alors la baisse supplémentaire à 3,5~Md€. Programme : \texttt{note8p/calculs/bouclage3.py}.

""" + "\n".join(t) + "\n"
(D / "annexes" / "annexe_bouclage.tex").write_text("% Écrit par calculs/annexe_bouclage3.py.\n" + txt, encoding="utf-8")
print("ok")
