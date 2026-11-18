"""Assemble note.tex (v7, format de la partie III) : corps_v7.tex + paragraphes de l'auteur (comments.json) + chapeaux,
tableaux générés (note8p/tableaux), troisième personne. Les paragraphes de l'auteur ne sont modifiés que pour
(1) les montants passés en Md€ de 2025, (2) les doublons avec la partie III (CIR), (3) la troisième personne."""
import json, re
from pathlib import Path
S = Path("/tmp/claude-0/-home-user-Projets-annexes/935fc156-45bd-500a-b52a-e7e4ee23abb6/scratchpad")
N = Path("/home/user/Projets-annexes/fiscalite/note8p")
C = json.loads((S / "relu" / "comments.json").read_text(encoding="utf-8"))
X = json.loads((S / "build" / "extras_v7.json").read_text(encoding="utf-8"))
FN = {"²": r"\footnote{Le taux marginal relie cinq repères : 1,5~\% au premier euro, 15,5~\% au SMIC, 22,5~\% à 1,5 SMIC, "
            r"28,7~\% à 2 SMIC et 36,3~\% à 3,5 SMIC. L'impôt dû est l'aire sous cette courbe ; le calcul figure en annexe B.}",
      "³": r"\footnote{Entre 65\,000 et 101\,500 euros et entre 136\,000 et 157\,000 euros de revenu annuel ; le taux "
            r"marginal monte aussi, plus légèrement, entre 1,6 et 1,8 SMIC.}",
      "⁵": r"\footnote{Zwick et Mahon (2017), \emph{American Economic Review} : +10 à +17~\% d'investissement pour les "
            r"entreprises concernées aux États-Unis ; Maffini, Xing et Devereux (2019), \emph{American Economic Journal: "
            r"Economic Policy} : environ +11~\% au Royaume-Uni.}"}
FIG = {"(figure 2)": r"(figure~\ref{fig:g11})", "(figure 3)": r"(figure~\ref{fig:g3})", "(figure 4)": r"(figure~\ref{fig:g10})",
       "(figure 7)": r"(figure~\ref{fig:g6})", "(figure 8)": r"(figure~\ref{fig:g7})"}
CIR = X["is_cir"]
CIR[0][1] = CIR[0][1] + r"\footnote{" + X["cir_note"][1] + "}"
REMPL = X["remplacements"] + CIR

# troisième personne (consignes de chiffrage, § 6) : remplacements exacts, vérifiés un par un
TP = [
 ("Notre système fiscal procède", "Le système fiscal français procède"),
 (r"\textbf{Nous voulons que les décisions économiques dépendent de leur rentabilité réelle plutôt que de leur traitement" + "\nfiscal.}",
  r"\textbf{Les décisions économiques devraient dépendre de leur rentabilité réelle plutôt que de leur traitement" + "\nfiscal.}"),
 ("Nos\npropositions découlent de ce principe.", "Les\npropositions qui suivent découlent de ce principe."),
 ("application froide de nos réformes", "application froide de ces réformes"),
 (", nous ajoutons un étage de complexité", ", la réforme ajoute un étage de complexité"),
 ("Nous ne construisons pas la fiscalité idéale des\nmanuels, qui taxerait la consommation plutôt que le revenu. Nous proposons une étape crédible dans cette direction.",
  "La réforme ne construit pas la fiscalité idéale des\nmanuels, qui taxerait la consommation plutôt que le revenu. Elle propose une étape crédible dans cette direction."),
 ("que notre système fiscal renchérit", "que le système fiscal renchérit"),
 (r"\textbf{Nous proposons donc un impôt qui emprunte", r"\textbf{La réforme crée donc un impôt qui emprunte"),
 ("Notre réforme réduit les taux marginaux", "La réforme réduit les taux marginaux"),
 ("nous continuons donc de privilégier", "la réforme continue donc de privilégier"),
 ("nous faisons le choix d’abaisser", "elle fait le choix d’abaisser"),
 ("Nos simulations suggèrent", "Les simulations suggèrent"),
 ("il nous paraît dès lors difficilement justifiable", "il paraît dès lors difficilement justifiable"),
 ("Il revient naturellement à notre système de protection sociale", "Il revient naturellement au système de protection sociale"),
 ("Nous illustrons ici l’un des principes", "Ce choix illustre l’un des principes"),
 ("avec notre impôt individuel", "avec le nouvel impôt individuel"),
 ("il nous paraîtrait donc particulièrement malvenu", "il serait donc particulièrement malvenu"),
 ("entorse assumée à notre objectif", "entorse assumée à l’objectif"),
 ("sans que nous puissions établir", "sans qu’il soit possible d’établir"),
 ("Or, notre taxe foncière frappe", "Or, la taxe foncière actuelle frappe"),
 ("que nous n'abordons pas ici", "que cette note n'aborde pas"),
 ("elles nous invitent à en modérer", "elles invitent à en modérer"),
 ("Pour financer cette réforme, nous proposons de réorienter", "Pour financer cette réforme, il est proposé de réorienter"),
 ("Il nous paraît préférable", "Il paraît préférable"),
 (r"\textbf{Notre fiscalité décourage également", r"\textbf{La fiscalité actuelle décourage également"),
 ("cohérence avec notre réforme de l’imposition des revenus", "cohérence avec la réforme de l’imposition des revenus"),
 ("de notre nouvel impôt sur le revenu", "du nouvel impôt sur le revenu"),
 ("il nous paraît économiquement souhaitable", "il paraît économiquement souhaitable"),
 ("conformément à notre objectif général", "conformément à l’objectif général de la réforme"),
 (r"\textbf{Notre réforme doit inciter", r"\textbf{La réforme doit inciter"),
 ("Notre réforme aggrave ce déséquilibre", "La réforme aggrave ce déséquilibre"),
 ("Nous n'en\nchiffrons donc aucun.", "Aucun effet n'en\nest donc chiffré."),
 ("notre fiscalité pénalise celui", "la fiscalité pénalise celui"),
 ("Avec notre barème, Antoine", "Avec le barème proposé, Antoine"),
 ("Nous proposons", "La réforme propose"), ("nous proposons", "la réforme propose"),
]


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
    for a, b in REMPL:
        t = t.replace(a, b)
    for a, b in X["sources"]:
        if a in t:
            t = t.replace(a, a + r"\footnote{" + b + "}", 1)
    return t


corps = (S / "corps_v7.tex").read_text(encoding="utf-8")
c22 = conv(C["p2 #2"])
i = c22.index("Les frais réels resteront déductibles")
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
    corps = corps.replace(r"\CHAPEAU{" + k + "}", v)
corps = corps.replace(r"\BILANIR", X["bilan_ir"]).replace(r"\PFUFIN", X["pfu_fin"])
manque = []
for a, b in TP:
    if a not in corps and a not in ("Nous proposons", "nous proposons"):
        manque.append(a[:60])
    corps = corps.replace(a, b)
ent = (S / "entete.tex").read_text(encoding="utf-8").replace(r"\input{preambule_v3}", "\\input{preambule_v3}\n\\usepackage{needspace}\n\\addto\\captionsfrench{\\renewcommand{\\tablename}{Tableau}}")
ent = ent[:ent.index(r"\begin{enbref}")]
ent = ent.replace("NOTE DE POLITIQUE ÉCONOMIQUE\\quad·\\quad NOVEMBRE 2026", "NOTE DE CHIFFRAGE\\quad·\\quad DOCUMENT DE TRAVAIL DU 18 NOVEMBRE 2026")
ent = re.sub(r"\{\\large\\color\{white\}.*?\\par\}", lambda m: r"{\large\color{white} Impôt sur le revenu, fiscalité foncière, impôt sur les sociétés et prélèvement forfaitaire unique. Montants en Md€ de 2025.\par}", ent, flags=re.S)
(N / "note.tex").write_text(ent + "\n" + corps + "\n\\end{document}\n", encoding="utf-8")
left = re.findall(r"%%C:[^%]*%%|\\CHAPEAU|\\BILAN\w*|\\PFUFIN", corps)
pers = re.findall(r".{40}\b(?:[Nn]ous|[Nn]otre|[Nn]os)\b.{30}", corps.replace("\n", " "))
print("restes :", left, "\nTP non trouvés :", manque, "\npremière personne restante :", len(pers))
for p in pers: print("  ·", p)
print("sources non placées :", [a for a, b in X["sources"] if a not in corps][:6])
print("remplacements non appliqués :", [a[:50] for a, b in REMPL if a in corps][:6])
