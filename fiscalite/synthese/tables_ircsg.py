"""Tableaux LaTeX de la partie IR-CSG, écrits depuis sorties/architectures_ircsg.json (aucune recopie à la main).

Lancer depuis fiscalite/ : python3 synthese/tables_ircsg.py -> synthese/parties/tab_ircsg_arch.tex, tab_ircsg_dec.tex
"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
J = json.loads((HERE / "sorties/architectures_ircsg.json").read_text(encoding="utf-8"))
ATT = J["atteignable"]


def n(x, d=1, signe=True):
    s = f"{x:+,.{d}f}" if signe else f"{x:,.{d}f}"
    s = s.replace(",", " ").replace(".", ",").replace(" ", "\\,")
    if s.startswith("-"):
        s = "$-$" + s[1:]
    if s in ("+0,0", "$-$0,0"):
        s = "0,0"
    return s


def part(r):
    return f"{100 * r['v2_central'] / ATT['v2_central']:.0f}~\\%"


def ligne(nom, r, pts=None):
    g = r["groupes"]
    pts_s = "---" if pts is None else n(100 * pts, 1)
    return (f"{nom} & {pts_s} & {n(-r['v2_central'], 1, False)} ({n(-r['v2_bas'], 1, False)} à "
            f"{n(-r['v2_haut'], 1, False)}) & {part(r)} & {r['perdants500']:.0f}~\\% & {n(g['retraites']['Md'])} & "
            f"{n(g['couples2']['eur'], 0)} & {n(r['top10_Md'])} \\\\")


A = {r["nom"]: r for r in J["architectures"]}
cle = lambda deb: next(r for k, r in A.items() if k.startswith(deb))  # noqa: E731
P4, P8 = J["propositions"]["4000"], J["propositions"]["8000"]
L = [r"\begin{table}[!htbp]\centering\scriptsize\setlength{\tabcolsep}{3pt}",
     r"\caption{Architectures comparées, à recette égale (220~Md€)}\label{tab:ircsg_arch}",
     r"\resizebox{\linewidth}{!}{%", r"\begin{tabular}{@{}lrrrrrrr@{}}", r"\toprule",
     r"& Points & Gain d'efficacité & Part du & Perdants & Retraités & Couple, & 10~\% \\",
     r"& pour tous & Md€ par an & gain & $>$ 500~€ & Md€ & 2 enfants & du haut \\",
     r"& & (fourchette) & atteignable & & & € par foyer & Md€ \\", r"\midrule",
     ligne("Barème neutre", cle("Barème neutre"), 0.0),
     r"\multicolumn{8}{@{}l}{\emph{Un dispositif ajouté au barème neutre}} \\",
     ligne("\\quad Franchise d'activité 4~000~€", cle("Neutre + franchise d'activité 4 000"), cle("Neutre + franchise d'activité 4 000")["d"]),
     ligne("\\quad Franchise d'activité 8~000~€", cle("Neutre + franchise d'activité 8 000 €"), cle("Neutre + franchise d'activité 8 000 €")["d"]),
     ligne("\\quad Franchise de 8~000~€ sur tous les revenus", cle("Neutre + franchise de 8"), cle("Neutre + franchise de 8")["d"]),
     ligne("\\quad Franchise de 6~000~€ par enfant", cle("Neutre + franchise de 6"), cle("Neutre + franchise de 6")["d"]),
     ligne("\\quad Chèque de 742~€ par enfant", cle("Neutre + chèque"), cle("Neutre + chèque")["d"]),
     ligne("\\quad Quotient conjugal et familial", cle("Neutre + quotient"), cle("Neutre + quotient")["d"]),
     ligne("\\quad Abattement de 10~\\% sur les pensions", cle("Neutre + abattement"), cle("Neutre + abattement")["d"]),
     ligne("\\quad Petites pensions exonérées", cle("Neutre + petites"), cle("Neutre + petites")["d"]),
     r"\midrule",
     ligne("\\textbf{Proposition}, franchise d'activité 4~000~€", P4),
     ligne("Proposition, franchise d'activité 8~000~€", P8),
     r"\midrule",
     ligne("Optimum d'efficacité, sans franchise", J["optimum_r"]),
     ligne("Gain atteignable (optimum, franchise 4~000~€)", ATT),
     r"\bottomrule", r"\end{tabular}}",
     r"\par\vspace{3pt}\parbox{\linewidth}{\raggedright\scriptsize\color{encre}",
     r"Gain d'efficacité : baisse de la perte sèche sur l'activité réelle par rapport à aujourd'hui, hypothèses "
     r"centrales (basses et hautes entre parenthèses) ; la réaction du revenu déclaré n'y est pas comptée. Points pour "
     r"tous : hausse des taux du barème neutre qui finance le dispositif. Proposition : franchise d'activité, "
     r"6~000~€ par enfant, pensions exonérées jusqu'à 12~500~€ puis de moins en moins jusqu'à 25~000~€ ; barème "
     r"le plus efficace parmi ceux qui ne changent la charge moyenne d'aucun décile de plus de 500~€ et "
     r"n'alourdissent pas celle du 1~\% le plus aisé. Retraités, couples, 10~\% du haut : variation de leur impôt "
     r"(positif : ils paient plus).}",
     r"\end{table}"]
(HERE / "parties/tab_ircsg_arch.tex").write_text("\n".join(L) + "\n", encoding="utf-8")

N = cle("Barème neutre")
O = J["optimum_r"]
D = [r"\begin{table}[!htbp]\centering\scriptsize\setlength{\tabcolsep}{4pt}",
     r"\caption{Variation de l'impôt par décile de revenu fiscal (€ par foyer et par an)}\label{tab:ircsg_dec}",
     r"\resizebox{\linewidth}{!}{%", r"\begin{tabular}{@{}l" + "r" * 10 + r"r@{}}", r"\toprule",
     "& " + " & ".join(f"D{i}" for i in range(1, 11)) + r" & 1~\% du haut (Md€) \\", r"\midrule"]
for nom, r in (("Barème neutre", N), ("Proposition (franchise 4~000~€)", P4), ("Proposition (franchise 8~000~€)", P8),
               ("Optimum d'efficacité", O)):
    D.append(nom + " & " + " & ".join(n(u, 0) for u in r["dec_eur"]) + f" & {n(r['top1_Md'])} \\\\")
D += [r"\bottomrule", r"\end{tabular}}", r"\end{table}"]
(HERE / "parties/tab_ircsg_dec.tex").write_text("\n".join(D) + "\n", encoding="utf-8")
print("\n".join(L[8:22]))
print("\n".join(D[5:9]))
