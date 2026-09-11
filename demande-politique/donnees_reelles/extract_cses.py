"""
Extrait les vagues françaises des fichiers CSES complets (téléchargement libre sur
https://cses.org/data-download/, sans inscription) vers data/.

    python extract_cses.py chemin/vers/cses5.csv chemin/vers/cses4.csv

- cses5.csv  : CSES Module 5 (full release), vague France 2017  -> data/fr2017_cses5.csv
- cses4.csv  : CSES Module 4 (full release), vague France 2012  -> data/fr2012_cses4.csv

Seules les colonnes utilisées par nuages_cses.py sont conservées. Les extraits ne sont
pas versionnés dans le dépôt : les données se récupèrent à la source (cses.org).
"""
import csv
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
DATA = HERE / "data"

COLS_2017 = (
    ["E1004", "E1006_NAM", "E1008", "E1010_1", "E1010_2", "E1010_3"]
    + [f"E3005_{i}" for i in range(1, 6)] + [f"E3006_{i}" for i in range(1, 5)]
    + ["E3008", "E3020", "E3012_PR_1", "E3013_PR_1", "E3013_PR_2", "E2001_Y", "E2002", "E2003", "E2010"]
)
COLS_2012 = (
    ["D1004", "D1006_NAM", "D1008", "D1010_1", "D1010_2", "D1010_3", "D2001_Y", "D2002", "D2003"]
    + [f"D3001_{i}" for i in range(1, 9)]
    + ["D3004", "D3005_PR_1", "D3006_PR_1", "D3014", "D3016", "D3018_3"]
)


def extraire(src, key, value, cols, dst):
    n = 0
    with open(src, newline="") as f, open(dst, "w", newline="") as g:
        r = csv.DictReader(f)
        w = csv.DictWriter(g, fieldnames=cols)
        w.writeheader()
        for row in r:
            if row[key] == value:
                w.writerow({c: row[c] for c in cols})
                n += 1
    print(f"{dst.name}: {n} lignes")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    DATA.mkdir(exist_ok=True)
    extraire(sys.argv[1], "E1004", "FRA_2017", COLS_2017, DATA / "fr2017_cses5.csv")
    extraire(sys.argv[2], "D1004", "FRA_2012", COLS_2012, DATA / "fr2012_cses4.csv")
