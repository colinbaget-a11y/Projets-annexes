"""
Récupère deux millésimes d'AMECO et en extrait les séries françaises utiles à la part
de l'industrie dans la valeur ajoutée.

  - millésime courant  : prévisions de printemps 2026, publié le 3 juin 2026, téléchargé
    directement sur le site de la Commission ;
  - millésime précédent : prévisions d'automne 2025 (dernier rafraîchissement 13 décembre
    2025). La Commission n'archive pas ses millésimes ; on le récupère dans le dépôt
    miroir de DBnomics, qui conserve les fichiers bruts AMECO*.TXT commit par commit
    (https://git.nomics.world/dbnomics-source-data/ameco-source-data, projet 36).

    python extract_ameco.py           # télécharge et écrit donnees/ameco_france_*.csv
    python extract_ameco.py --cache D # réutilise des AMECO*.TXT déjà présents dans D
"""
import argparse
import csv
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / "donnees"
CHAPITRES = ["1", "6", "12"]

MILLESIMES = {
    # nom court : (libellé, gabarit d'URL)
    "s2026": ("Prévisions de printemps 2026 (3 juin 2026)",
              "https://ec.europa.eu/economy_finance/db_indicators/ameco/documents/ameco{ch}.zip"),
    "a2025": ("Prévisions d'automne 2025 (13 décembre 2025)",
              "https://git.nomics.world/api/v4/projects/36/repository/files/AMECO{ch}.TXT/raw?ref=1b7562a4"),
}

# Séries retenues (suffixe du code AMECO). U = prix courants, O = prix de 2020 chaînés.
SERIES = {
    "UVGD": "PIB aux prix courants", "OVGD": "PIB aux prix de 2020",
    "UVG0": "VA brute, total des branches, prix courants", "OVG0": "VA brute, total des branches, prix de 2020",
    "UVG1": "VA agriculture, prix courants", "OVG1": "VA agriculture, prix de 2020",
    "UVG2": "VA industrie hors construction (NACE B-E), prix courants",
    "OVG2": "VA industrie hors construction (NACE B-E), prix de 2020",
    "UVGM": "VA industrie manufacturière (NACE C), prix courants",
    "OVGM": "VA industrie manufacturière (NACE C), prix de 2020",
    "UVG4": "VA construction, prix courants", "OVG4": "VA construction, prix de 2020",
    "UVG5": "VA services, prix courants", "OVG5": "VA services, prix de 2020",
    "FETD": "Emploi total, équivalents temps plein", "FET2": "Emploi industrie B-E, ETP",
    "FETM": "Emploi manufacturier C, ETP", "FET4": "Emploi construction, ETP", "FET5": "Emploi services, ETP",
    "NETD": "Emploi total, personnes", "NETM": "Emploi manufacturier C, personnes",
}


def fichier(millesime, ch, cache):
    if cache:
        p = Path(cache) / millesime / f"AMECO{ch}.TXT"
        if p.exists():
            return p
    brut = HERE / "brut" / millesime
    brut.mkdir(parents=True, exist_ok=True)
    url = MILLESIMES[millesime][1].format(ch=ch)
    if url.endswith(".zip"):
        z = brut / f"ameco{ch}.zip"
        subprocess.run(["curl", "-sS", "-L", "--max-time", "300", "-o", str(z), url], check=True)
        subprocess.run(["unzip", "-o", "-q", str(z), "-d", str(brut)], check=True)
    else:
        subprocess.run(["curl", "-sS", "-L", "--max-time", "300", "-o", str(brut / f"AMECO{ch}.TXT"), url], check=True)
    return brut / f"AMECO{ch}.TXT"


def extraire(millesime, cache=None):
    lignes, vues = [], set()
    for ch in CHAPITRES:
        with open(fichier(millesime, ch, cache), encoding="latin-1") as f:
            r = csv.reader(f, delimiter=";")
            hdr = next(r)
            annees = [(i, hdr[i].strip()) for i in range(5, len(hdr)) if hdr[i].strip().isdigit()]
            for row in r:
                code = row[0].strip()
                if not code.startswith("FRA."):
                    continue
                suf = code.split(".")[-1]
                if suf not in SERIES or suf in vues:
                    continue
                vues.add(suf)
                for i, an in annees:
                    v = row[i].strip().replace(",", "")
                    if not v or v.upper() == "NA":
                        continue
                    lignes.append({"millesime": millesime, "code": code, "serie": suf,
                                   "libelle": SERIES[suf], "unite": row[4].strip(),
                                   "annee": int(an), "valeur": float(v)})
    return lignes


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--cache")
    a = ap.parse_args()
    OUT.mkdir(exist_ok=True)
    for m, (lib, _) in MILLESIMES.items():
        lignes = extraire(m, a.cache)
        dst = OUT / f"ameco_france_{m}.csv"
        with open(dst, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=["millesime", "code", "serie", "libelle", "unite", "annee", "valeur"])
            w.writeheader()
            w.writerows(lignes)
        print(f"{dst.name}: {len(lignes)} observations, {len({l['serie'] for l in lignes})} séries — {lib}")
