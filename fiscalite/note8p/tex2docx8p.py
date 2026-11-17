"""Convertit note8p/note.tex en note8p/note.docx (pandoc), en dépliant les commandes de figure de preambule8p.tex.

Lancer depuis fiscalite/note8p : python3 tex2docx8p.py
"""
import re
import subprocess
from pathlib import Path

D = Path(__file__).resolve().parent
src = (D / "note.tex").read_text(encoding="utf-8")
corps = src[src.index("\\begin{document}") + len("\\begin{document}"):src.index("\\end{document}")]


def source(f):
    txt = (D / "figures" / f"{f}_source.tex").read_text(encoding="utf-8").replace("\\par", " ")
    return " ".join(txt.split())


def fig(f, titre, lab):
    return (f"\n\n\\begin{{figure}}\n\\includegraphics{{figures/{f}.png}}\n\\caption{{{titre}}}\\label{{{lab}}}\n"
            f"\\end{{figure}}\n\n{{\\small {source(f)}}}\n\n")


# numéros des figures et tableaux dans l'ordre d'apparition
nums, nf, nt = {}, 0, 0
for m in re.finditer(r"\\(graphique|deuxgraphiques)\{|\\label\{(fig|tab):([^}]*)\}", corps):
    pass
for m in re.finditer(r"\\label\{((fig|tab):[^}]*)\}", corps):
    if m.group(2) == "fig":
        nf += 1
        nums[m.group(1)] = str(nf)
    else:
        nt += 1
        nums[m.group(1)] = str(nt)

corps = re.sub(r"\\deuxgraphiques\{([^}]*)\}\{([^}]*)\}\{([^}]*)\}%?\s*\{([^}]*)\}\{([^}]*)\}\{([^}]*)\}",
               lambda m: fig(m.group(1), m.group(2), m.group(3)) + fig(m.group(4), m.group(5), m.group(6)), corps,
               flags=re.S)
corps = re.sub(r"\\graphique\{([^}]*)\}\{([^}]*)\}\{([^}]*)\}",
               lambda m: fig(m.group(1), m.group(2), m.group(3)), corps, flags=re.S)
# figure 1 + tableau du barème : on garde l'image puis le tableau
corps = re.sub(r"\\begin\{minipage\}\[t\]\{[^}]*\}", "", corps)
corps = corps.replace("\\end{minipage}", "").replace("\\hfill", "")
corps = re.sub(r"\\includegraphics\[width=\\linewidth\]\{figures/([^}]*)\.pdf\}", r"\\includegraphics{figures/\1.png}", corps)
corps = re.sub(r"\\input\{figures/([^}]*)_source\.tex\}", lambda m: source(m.group(1)), corps)
corps = corps.replace("\\captionsetup{type=table}", "")
corps = re.sub(r"\\ref\{([^}]*)\}", lambda m: nums.get(m.group(1), "?"), corps)
corps = re.sub(r"\\graphiqueetroit\{([^}]*)\}\{([^}]*)\}\{([^}]*)\}\{[^}]*\}",
               lambda m: fig(m.group(1), m.group(2), m.group(3)), corps, flags=re.S)
corps = re.sub(r"\\chiffre\{([^}]*)\}\{([^}]*)\}", r"\\textbf{\1} (\2) ; ", corps)
corps = re.sub(r"\\begin\{enbref\}|\\end\{enbref\}|\\par\\vspace\{5pt\}", "\n\n", corps)
corps = re.sub(r"\\begin\{tcolorbox\}\[[^\]]*\]|\\end\{tcolorbox\}", "", corps)
corps = corps.replace("\\color{white}", "")
# en-tête
t = "Taxer mieux plutôt que davantage"
st = "Moins de niches, des assiettes larges, des taux raisonnables : une fiscalité qui récompense le travail, l'investissement et la mobilité, sans un euro de dette en plus"
debut = corps.index("\\textbf{Ce que nous proposons.}") if "Ce que nous proposons" in corps else corps.index("\\section{")
corps = f"\\section*{{{t}}}\n\n\\emph{{{st}}}\n\n" + corps[debut:]
for c in ("\\color{gris}", "\\raggedright", "\\scriptsize", "\\small", "\\vspace{1pt}", "\\vspace{2pt}", "\\vspace{3pt}",
          "\\vspace{4pt}", "\\setlength{\\tabcolsep}{3.2pt}"):
    corps = corps.replace(c, "")
corps = re.sub(r"\\setlength\{\\tabcolsep\}\{[^}]*\}", "", corps)
corps = corps.replace("\\textsuperscript{er}", "er")
doc = "\\documentclass{article}\n\\usepackage{booktabs}\n\\begin{document}\n" + corps + "\n\\end{document}\n"
tmp = D / "note_docx_tmp.tex"
tmp.write_text(doc, encoding="utf-8")
subprocess.run(["pandoc", str(tmp.name), "-f", "latex", "-t", "docx", "-o", "note.docx", "--resource-path", "."],
               cwd=D, check=True)
tmp.unlink()
print("note.docx écrit")
