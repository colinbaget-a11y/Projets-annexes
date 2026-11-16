"""Écrit annexes/annexe_bouclage.tex (trajectoire complète, années de caisse) à partir de sorties/bouclage.json."""
import json
from pathlib import Path

D = Path(__file__).resolve().parent.parent
B = json.loads((D / "sorties" / "bouclage.json").read_text(encoding="utf-8"))
A = B["annuel"]


def f(x, d=1):
    s = f"{x:.{d}f}".replace(".", "{,}")
    return s.replace("-", "$-$") if not s.startswith("-0{,}0") or abs(x) >= 0.05 else "0{,}0"


ans = sorted(A)
lignes = [
    ("Nouvel impôt sur le revenu (net)", "ircsg"),
    ("Foncier net (taxe, droits, report, déductibilité)", "foncier_net"),
    ("Fin du taux réduit d'IS", "taux_reduit"),
    ("Déduction immédiate de 50~\\%", "deduction_50"),
    ("Baisse du taux normal", "baisse_taux"),
    ("\\textbf{Solde}", "solde_sans_pfu"),
    ("Réserve : fin de l'effacement (central)", "pfu_reserve"),
    ("Étape conditionnelle : baisse financée par la réserve", "baisse_taux_pv"),
    ("Solde avec la réserve et l'étape conditionnelle", "solde_avec_pfu_et_baisse"),
]
t = ["\\begin{table}[!htbp]\\centering\\scriptsize\\setlength{\\tabcolsep}{2.4pt}",
     "\\caption{Trajectoire complète (Md€ de 2027, années d'encaissement ; + = recette publique en plus)}\\label{tab:traj_complete}",
     "\\begin{tabular}{@{}l" + "r" * len(ans) + "@{}}\\toprule",
     " & " + " & ".join(a[2:] for a in ans) + " \\\\ \\midrule"]
for lab, k in lignes:
    t.append(lab + " & " + " & ".join(f(A[a][k]) for a in ans) + " \\\\")
t.append("Taux normal de l'IS (exercice précédent, \\%) & " + " & ".join(f(A[a]["taux_normal"], 1) for a in ans) + " \\\\")
t.append("Idem avec l'étape conditionnelle (\\%) & " + " & ".join(f(A[a]["taux_normal_avec_pv"], 1) for a in ans) + " \\\\")
t += ["\\bottomrule\\end{tabular}", "\\end{table}"]

texte = r"""\subsection{Règles et calendrier}

Le bouclage tient trois règles. Aucune année de déficit organisée : le solde des quatre réformes reste compris entre
$-0{,}3$ et $+1{,}1$~Md€ chaque année. Les recettes de la fin de l'effacement des plus-values ne financent rien avant
d'être constatées ; elles forment une réserve. Les évolutions du droit en vigueur (fin de la contribution exceptionnelle
sur les bénéfices des grandes entreprises, $-7$~Md€ par an après l'exercice 2026 ; extinction de la CRDS fin 2033, qui
permet de baisser tous les taux du nouvel impôt de 0{,}54 point à recette constante) ne sont ni comptées ni utilisées.

Unités : euros constants de 2027. Les séries de l'IS, nominales (+3~\% par an), sont déflatées par leur propre
croissance ; les séries foncières et des plus-values sont au niveau de l'activité de 2025. L'écart de convention
(environ 4~\%) est sans effet sur les conclusions. L'IS d'un exercice est encaissé l'année suivante.

Calendrier [C] : nouvel impôt sur le revenu monté en charge sur quatre ans (2027-2030), chaque foyer payant
$(1-\lambda)\times$ ancien impôt $+\ \lambda\times$ nouvel impôt, $\lambda = 0{,}25$ à 1, ce qui garde la recette chaque
année ; taxe foncière nationale par tiers en 2029, 2030 et 2031, droits de mutation baissés le 1\textsuperscript{er}
janvier des mêmes années, avec clause de suspension ; taux réduit d'IS à 20~\% pour l'exercice 2027, aligné dès 2028 ;
déduction immédiate à 25~\% pour l'exercice 2028, 50~\% dès 2029 ; taux normal baissé par demi-points, au plus fort
possible sans qu'aucune année ultérieure passe sous $-0{,}3$~Md€ : 24~\% (exercice 2030), 23{,}5~\% (2032), 23~\%
(2033), 22{,}5~\% (2035). Étape conditionnelle : un point de plus dès l'exercice 2035 si la réserve atteint son niveau
central. Programme : \texttt{note8p/calculs/bouclage.py}.

""" + "\n".join(t) + r"""

\subsection{Sensibilités}

\textbf{Plus-values.} Au bas de la fourchette (1{,}0~Md€ en 2040 au lieu de 3{,}7), l'étape conditionnelle n'a pas
lieu ; rien d'autre ne change, puisque la réserve ne finance rien d'autre. \textbf{Foncier.} Avec une enveloppe de 10~Md€ au lieu de 15 (excédent net d'environ 1~Md€ par an), la baisse du
taux normal se limite à un point, et le calendrier de la déduction immédiate n'est plus finançable : le solde tombe à
$-3{,}2$~Md€ l'année du pic, sauf à retarder la déduction. Avec 20~Md€ (excédent de 10~Md€), le taux normal
descendrait à 21~\% dès 2035. Si l'évaluation des terrains prend un an de retard, la clause de suspension décale la
taxe et la baisse des droits, mais pas les mesures d'IS : sans autre précaution, le solde tomberait à $-1{,}8$~Md€ une
année. La déduction immédiate et chaque palier de baisse du taux doivent donc être soumis à la même clause que les
droits de mutation (programme : \texttt{FONCIER\_SCEN=E10|E20|E15\_glissement\_un\_an python3 calculs/bouclage.py}).
\textbf{IS.} La part imposable de l'investissement (75~\%, hypothèse) fait varier le coût de la déduction
dans la même proportion (pic de 5{,}4 à 8{,}1~Md€ pour 60 à 90~\%) ; inclure les véhicules utilitaires le multiplie
par 1{,}25. Le rendement de la fin du taux réduit va de 2{,}15 à 3{,}18~Md€. Dans le cas défavorable, la baisse du
taux normal doit attendre ; le calendrier par paliers le permet.
"""
(D / "annexes" / "annexe_bouclage.tex").write_text(
    "% Écrit par note8p/calculs/annexe_bouclage.py ; ne pas modifier à la main.\n" + texte, encoding="utf-8")
print("ok")
