"""Assemble note.tex : corps_v6.tex + paragraphes de l'auteur (comments.json, verbatim) + chapeaux + bilan."""
import json, re, sys
from pathlib import Path
S = Path("/tmp/claude-0/-home-user-Projets-annexes/935fc156-45bd-500a-b52a-e7e4ee23abb6/scratchpad")
N = Path("/home/user/Projets-annexes/fiscalite/note8p")
C = json.loads((S / "relu" / "comments.json").read_text(encoding="utf-8"))
X = json.loads((S / "build" / "extras.json").read_text(encoding="utf-8"))   # chapeaux, exceptions, bilan, titre g11

FN = {"²": r"\footnote{Le taux marginal relie cinq repères : 1,5~\% au premier euro, 15,5~\% au SMIC, 22,5~\% à 1,5 SMIC, "
            r"28,7~\% à 2 SMIC et 36,3~\% à 3,5 SMIC. L'impôt dû est l'aire sous cette courbe ; le calcul figure en annexe B.}",
      "³": r"\footnote{Entre 65\,000 et 101\,500 euros et entre 136\,000 et 157\,000 euros de revenu annuel ; le taux "
            r"marginal monte aussi, plus légèrement, entre 1,6 et 1,8 SMIC.}",
      "⁵": r"\footnote{Zwick et Mahon (2017), \emph{American Economic Review} : +10 à +17~\% d'investissement pour les "
            r"entreprises concernées aux États-Unis ; Maffini, Xing et Devereux (2019), \emph{American Economic Journal: "
            r"Economic Policy} : environ +11~\% au Royaume-Uni.}"}
FIG = {"(figure 2)": r"(figure~\ref{fig:g11})", "(figure 3)": r"(figure~\ref{fig:g3})", "(figure 4)": r"(figure~\ref{fig:g10})",
       "(figure 7)": r"(figure~\ref{fig:g6})", "(figure 8)": r"(figure~\ref{fig:g7})"}
# notes de source ajoutées après un passage précis (le texte de l'auteur n'est pas modifié)
SRC = X["sources"]


def conv(t):
    t = t.replace("&#x20;", "").strip()
    t = t.split("Commentaire pour Claude")[0].strip()
    t = t.replace("absudes", "absurdes").replace("fiscalistes...", "fiscalistes.")
    t = t.replace("XIXᵉ", r"XIX\textsuperscript{e}")
    t = t.replace("%", r"~\%").replace(" ~\\%", r"~\%")
    t = re.sub(r"\*\*(.+?)\*\*", r"\\textbf{\1}", t, flags=re.S)
    t = re.sub(r"\*(.+?)\*", r"\\emph{\1}", t)
    for a, b in FIG.items():
        t = t.replace(a, b)
    for a, b in FN.items():
        t = t.replace(a, b)
    for a, b in X.get("remplacements", []):
        t = t.replace(a, b)
    for a, b in SRC:
        if a in t:
            t = t.replace(a, a + r"\footnote{" + b + "}", 1)
    return t


corps = (S / "corps_v6.tex").read_text(encoding="utf-8")
c22 = conv(C["p2 #2"])
i = c22.index("Les frais réels resteront déductibles")
C["p2 #2"] = None
corps = corps.replace("%%C:p2 #2%%", c22[:i] + X["exceptions"])
G7 = (r"\graphique{g7_tmei}{Pour un coût permanent bien inférieur à celui d'une baisse du taux, la déduction immédiate"
      r" réduit fortement l'impôt sur l'investissement nouveau}{fig:g7}")
for k in re.findall(r"%%C:(p\d #\d)%%", corps):
    t = conv(C[k])
    if k == "p6 #2":
        a, b = t.split("\n\n", 1)
        t = a + "\n\n" + G7 + "\n\n" + b
    corps = corps.replace(f"%%C:{k}%%", t)
for k, v in X["chapeaux"].items():
    corps = corps.replace(r"\CHAPEAU{" + k + "}", r"{\itshape " + v + r"\par}")
corps = corps.replace(r"\TITREGONZE", X["titre_g11"]).replace(r"\BILAN", X["bilan"])
ent = (S / "entete.tex").read_text(encoding="utf-8").replace(r"\input{preambule_v3}", "\\input{preambule_v3}\n\\usepackage{needspace}")
(N / "note.tex").write_text(ent + "\n" + corps + "\n\\end{document}\n", encoding="utf-8")
left = re.findall(r"%%C:[^%]*%%|\\CHAPEAU|\\BILAN|\\TITREGONZE", corps)
print("note.tex écrite ; restes :", left, "; sources non placées :", [a for a, b in SRC if a not in corps.replace(r"\footnote", "")][:5])
