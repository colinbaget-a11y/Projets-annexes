"""Première version de la note fusionnée : extrait le corps des notes foncier, IS et PFU (sections rétrogradées
d'un niveau, introduction gardée comme chapeau) dans des fichiers à inclure, et rassemble leurs références.

Lancer depuis fiscalite/synthese/ : python3 assembler.py  ->  parties/foncier.tex, parties/is.tex, parties/pfu.tex,
parties/references_brutes.txt. Ces fichiers sont ensuite retouchés à la main ; ne pas relancer après retouche.
"""
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / "parties"
OUT.mkdir(exist_ok=True)
NOTES = {"foncier": "../foncier/note-foncier.tex", "is": "../is/note-is.tex", "pfu": "../pfu/note-pfu.tex"}
refs = []
for nom, chemin in NOTES.items():
    s = (HERE / chemin).read_text(encoding="utf-8")
    corps = s[s.index("\\section*{Introduction}") + len("\\section*{Introduction}"):s.index("\\vspace{6pt}\n{\\scriptsize\\textbf{Références.}")]
    r = s[s.index("\\textbf{Références.}") + len("\\textbf{Références.}"):s.index("\\end{document}")]
    refs.append(f"% {nom}\n" + r.strip().rstrip("}").rstrip("\\par").strip())
    corps = re.sub(r"\\subsection\*\{", r"\\subsubsection*{", corps)
    corps = re.sub(r"\\section\{", r"\\subsection{", corps)
    (OUT / f"{nom}.tex").write_text(f"% Partie {nom}, extraite de {chemin} puis retouchée\n" + corps.strip() + "\n",
                                    encoding="utf-8")
(OUT / "references_brutes.txt").write_text("\n\n".join(refs) + "\n", encoding="utf-8")
print("ok")
