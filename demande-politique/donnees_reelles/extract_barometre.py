"""
Télécharge les vagues utiles du Baromètre de la confiance politique (CEVIPOF / Sciences Po,
terrain OpinionWay) depuis le Dataverse de Sciences Po (licence CC-BY 4.0, aucun compte
nécessaire) et en extrait, pour la France, les colonnes utilisées par nuages_barometre.py.

    python extract_barometre.py            # télécharge puis extrait
    python extract_barometre.py --cache D  # utilise des fichiers .tab déjà téléchargés dans D

Jeu de données : doi:10.21410/7E4/9K3VGR (« Baromètre de la confiance politique », CDSP).
Les fichiers sont accessibles à https://data.sciencespo.fr/api/access/datafile/<id>.
"""
import subprocess
import sys
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
OUT = HERE / "data" / "barometre"
API = "https://data.sciencespo.fr/api/access/datafile/{id}"

# id Dataverse du fichier, colonnes conservées
VAGUES = {
    "V9_2017": dict(id=5885, cols=["Poids", "Poids1", "nou1", "r36a", "r36ab", "r36",
                                   "q27_i1", "q27_i2", "q27_i3", "q27_i16", "q27_i13", "n43_i4", "n43_i5", "n43_i6", "nou10_i4", "nou10_i2",
                                   "q27_i8", "q27_i17", "q27_i14", "q31", "q32", "nou10_i1", "nou7"]),
    "V13_2022": dict(id=3959, cols=["Poids", "Poids1", "nou1", "r36a", "r36ab", "ivt1_2",
                                    "Q27_i2", "q27_i22", "q27_i18", "n43_i4", "n43_i6", "qcb1_i3",
                                    "q27_i8", "q27_i17", "q27_i14", "q27_i23", "q32"]),
    "V15_2024": dict(id=8753, pays=1, cols=["pays", "poids1", "nou1", "v0t1", "t12022", "r36b",
                                            "q27_i2", "q27_i22", "q27_i31", "q27_i32",
                                            "q27_i8", "q27_i14", "q27_i23", "q31bv15_i4"]),
    "V16_2025": dict(id=10529, pays=1, cols=["pays", "poids1", "poids5", "nou1", "v0t1", "t12022",
                                             "q27_i2", "q27_i22", "q27_i32", "q6v16_i4", "q17v16",
                                             "q27_i8", "q27_i14", "q27_i23", "q9v16"]),
}


def fichier(vague, cache):
    p = (Path(cache) if cache else OUT / "brut") / f"{vague}.tab"
    if not p.exists():
        p.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(["curl", "-sS", "-L", "--max-time", "300", "-o", str(p), API.format(id=VAGUES[vague]["id"])], check=True)
    return p


if __name__ == "__main__":
    cache = sys.argv[sys.argv.index("--cache") + 1] if "--cache" in sys.argv else None
    OUT.mkdir(parents=True, exist_ok=True)
    for vague, spec in VAGUES.items():
        d = pd.read_csv(fichier(vague, cache), sep="\t", low_memory=False)
        if "pays" in spec:
            d = d[d["pays"] == spec["pays"]]
        d = d[[c for c in spec["cols"] if c in d.columns]]
        d.to_csv(OUT / f"{vague}_fr.csv", index=False)
        print(f"{vague}: {len(d)} répondants, {d.shape[1]} colonnes")
