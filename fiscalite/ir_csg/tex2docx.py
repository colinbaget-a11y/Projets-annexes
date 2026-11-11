"""Convertit note-ir-csg.tex en note-ir-csg.docx (pandoc), en dépliant les commandes propres à la note.

Lancer depuis fiscalite/ir_csg/ : python3 tex2docx.py
- \\figbloc{nom}{légende}{label} -> image PNG (source et note de lecture comprises dans l'image) + légende ;
- \\partie{...} -> titre de niveau 1, \\section -> niveau 2 ;
- encadré -> titre en gras suivi du texte ;
- \\ref{...} -> numéro de figure ou de tableau, calculé dans l'ordre du document.
"""
import re
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
src = (HERE / "note-ir-csg.tex").read_text(encoding="utf-8")
corps = src[src.index("\\begin{document}") + len("\\begin{document}"):src.index("\\end{document}")]

# numéros des figures et tableaux, dans l'ordre d'apparition
nums, nf, nt = {}, 0, 0
for m in re.finditer(r"\\figbloc\{[^}]*\}\{[^}]*\}\{([^}]*)\}|\\caption\{[^}]*\}\\label\{([^}]*)\}", corps):
    if m.group(1):
        nf += 1
        nums[m.group(1)] = str(nf)
    else:
        nt += 1
        nums[m.group(2)] = str(nt)
sec = 0
for m in re.finditer(r"\\section\{[^}]*\}(?:\\label\{([^}]*)\})?", corps):
    sec += 1
    if m.group(1):
        nums[m.group(1)] = str(sec)

# page de titre : on garde titre, sous-titre et auteur
corps = re.sub(r"\\renewcommand\{\\figurename\}.*?\n", "", corps)
t = re.search(r"\\selectfont\\bfseries\\color\{bleu\}(.*?)\\par\}", corps, re.S).group(1)
st = re.search(r"\{\\large (.*?)\\par\}", corps, re.S).group(1)
au = re.search(r"\{\\small (Colin Baget.*?)\\par\}", corps, re.S).group(1)
debut = corps.index("\\section*{L'essentiel}")
corps = (f"\\textbf{{NOTE DE TRAVAIL · NOVEMBRE 2026}}\n\n\\section*{{{t}}}\n\n\\textit{{{st}}}\n\n{au}\n\n"
         + corps[debut:])


def fig(m):
    nom, leg, lab = m.group(1), m.group(2), m.group(3)
    return (f"\n\n\\begin{{figure}}\n\\centering\n\\includegraphics[width=\\linewidth]{{../figures/{nom}.png}}\n"
            f"\\caption{{Figure {nums[lab]}. {leg}}}\n\\end{{figure}}\n\n")


corps = re.sub(r"\\figbloc\{([^}]*)\}\{([^}]*)\}\{([^}]*)\}", fig, corps)
corps = re.sub(r"\\partie\{([^}]*)\}", r"\\section*{\1}", corps)
corps = re.sub(r"\\section\{([^}]*)\}(\\label\{[^}]*\})?", lambda m: f"\\subsection*{{{nums.get((m.group(2) or '')[7:-1], '')} {m.group(1)}}}" if m.group(2) else f"\\subsection*{{{m.group(1)}}}", corps)
corps = re.sub(r"\\begin\{encadre\}\{([^}]*)\}", r"\\textbf{\1}\n\n", corps)
corps = corps.replace("\\end{encadre}", "")
corps = re.sub(r"\\caption\{([^}]*)\}\\label\{([^}]*)\}", lambda m: f"\\caption{{Tableau {nums[m.group(2)]}. {m.group(1)}}}", corps)
corps = re.sub(r"(?:figure|tableau|section)~\\ref\{([^}]*)\}",
               lambda m: {"f": "figure", "t": "tableau", "s": "section"}[m.group(0)[0]] + " " + nums.get(m.group(1), "?"), corps)
corps = re.sub(r"\\ref\{([^}]*)\}", lambda m: nums.get(m.group(1), "?"), corps)
corps = re.sub(r"\\(clearpage|vspace\*?\{[^}]*\}|thispagestyle\{[^}]*\}|scriptsize|footnotesize|small|setlength\{[^}]*\}\{[^}]*\})", "", corps)
corps = re.sub(r"\\parbox\{[^}]*\}\{(.*?)\}\n\\end\{table\}", r"\\end{table}\n\n\1", corps, flags=re.S)
corps = re.sub(r"\\color\{[^}]*\}", "", corps)
corps = corps.replace("tabularx}{\\linewidth}", "tabular}").replace("\\end{tabularx}", "\\end{tabular}")
corps = re.sub(r">\{\\raggedright\\arraybackslash\}p\{[^}]*\}", "l", corps)
corps = re.sub(r"\\par\s*\\end\{table\}", r"\\end{table}", corps)
corps = re.sub(r"\\cmidrule(\([a-z]*\))?\{[^}]*\}", "", corps)
corps = corps.replace("@{}", "")                       # pandoc ne lit pas les tableaux avec @{}
corps = corps.replace(">{\\raggedright\\arraybackslash}X", "l")

tex = ("\\documentclass{article}\n\\usepackage{graphicx}\n\\usepackage{booktabs}\n\\begin{document}\n"
       + corps + "\n\\end{document}\n")
tmp = HERE / "_note_pandoc.tex"
tmp.write_text(tex, encoding="utf-8")
subprocess.run(["pandoc", str(tmp), "-f", "latex", "-t", "docx", "-o", str(HERE / "note-ir-csg.docx"),
                "--resource-path", str(HERE)], check=True)
tmp.unlink()
print("note-ir-csg.docx écrit")
