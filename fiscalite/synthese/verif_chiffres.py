"""Contrôle de la coupe : aucun chiffre ne doit apparaître qui n'existait pas avant.

Usage (depuis fiscalite/) : python3 synthese/verif_chiffres.py synthese/parties/ircsg.tex [autres fichiers]
Compare chaque fichier à sa version du commit de référence (REF, par défaut e7232a5) et liste les nombres présents
après la coupe mais absents avant ; « NOUVEAU » signale ceux qui n'existaient nulle part dans la note de référence
(parties et notes de figure), les seuls qui demandent vraiment une vérification.
"""
import re
import subprocess
import sys
from pathlib import Path

REF = "e7232a5"
RACINE = Path(subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True).stdout.strip())


def nombres(texte):
    texte = re.sub(r"(?m)(?<!\\)%.*$", "", texte)              # commentaires LaTeX
    texte = re.sub(r"(?<=\d)\\,(?=\d)", "", texte)             # 3\,000 -> 3000
    texte = re.sub(r"(?<=\d)\{,\}(?=\d)", ",", texte)          # 0{,}5 -> 0,5
    texte = re.sub(r"\\(label|ref|eqref|figbloc|input|cite\w*|includegraphics)(\[[^]]*\])?\{[^}]*\}", " ", texte)
    texte = re.sub(r"\\[a-zA-Z]+", " ", texte)                  # commandes
    return set(re.findall(r"(?<![\w.,])\d+(?:,\d+)?", texte))


def ancien(chemin):
    rel = Path(chemin).resolve().relative_to(RACINE)
    r = subprocess.run(["git", "show", f"{REF}:{rel}"], capture_output=True, text=True, cwd=RACINE)
    return r.stdout if r.returncode == 0 else ""


def global_ancien():
    r = subprocess.run(["git", "ls-tree", "-r", "--name-only", REF], capture_output=True, text=True, cwd=RACINE)
    tous = set()
    for f in r.stdout.split():
        if (f.startswith("fiscalite/synthese/parties/") or (f.startswith("fiscalite/figures/nu/") and f.endswith("_note.tex"))):
            tous |= nombres(subprocess.run(["git", "show", f"{REF}:{f}"], capture_output=True, text=True, cwd=RACINE).stdout)
    return tous


if __name__ == "__main__":
    glob = global_ancien()
    for chemin in sys.argv[1:]:
        neufs = sorted(nombres(Path(chemin).read_text(encoding="utf-8")) - nombres(ancien(chemin)),
                       key=lambda x: float(x.replace(",", ".")))
        nouveaux = [x for x in neufs if x not in glob]
        print(f"{chemin} : {len(neufs)} nombre(s) absent(s) de la version de référence du fichier"
              + (f" : {', '.join(neufs)}" if neufs else ""))
        if nouveaux:
            print(f"   NOUVEAU (absent de toute la note de référence) : {', '.join(nouveaux)}")
