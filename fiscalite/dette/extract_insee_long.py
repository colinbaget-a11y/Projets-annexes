"""
Séries longues de l'Insee sur les administrations publiques (comptes nationaux annuels, base 2014,
séries arrêtées), pour prolonger avant 1995 les données Eurostat en base 2020.

    python dette/extract_insee_long.py

La dépense par fonction (COFOG) n'existe à l'Insee qu'à partir de 1995, dans toutes les bases ; les
séries longues sont donc par nature d'opération.

Sortie : dette/donnees/insee_long.csv (milliards d'euros courants), colonnes :
  dette        dette de Maastricht des APU, fin d'année (1978-2022)
  deficit      déficit de Maastricht des APU, signe négatif = déficit (1949-2022)
  interets     intérêts versés par les APU, D41 emplois (1949-2021)
  prest_esp    prestations sociales en espèces, D62 (1949-2021)
  prest_nat    transferts sociaux en nature de produits marchands, D632 : remboursements de soins,
               de médicaments, aides au logement… (1949-2021)
  pib          PIB en valeur (1949-2022)
"""
import csv
import re
import urllib.request
from pathlib import Path

OUT = Path(__file__).resolve().parent / "donnees"
SERIES = {"010562165": "dette", "010562130": "deficit", "010563497": "interets",
          "010563674": "prest_esp", "010563707": "prest_nat", "010548500": "pib"}

url = "https://bdm.insee.fr/series/sdmx/data/SERIES_BDM/" + "+".join(SERIES)
with urllib.request.urlopen(url, timeout=300) as r:
    t = r.read().decode("utf-8")
valeurs = {}
for attrs, corps in re.findall(r"<Series ([^>]*)>(.*?)</Series>", t, re.S):
    nom = SERIES[re.search(r'IDBANK="(\d+)"', attrs).group(1)]
    mult = 10 ** (int(re.search(r'UNIT_MULT="(\d+)"', attrs).group(1)) - 9)   # en milliards
    for an, v in re.findall(r'TIME_PERIOD="(\d{4})" OBS_VALUE="([^"]*)"', corps):
        if v not in ("", "NaN"):
            valeurs.setdefault(int(an), {})[nom] = float(v) * mult
cols = list(SERIES.values())
with open(OUT / "insee_long.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["annee"] + cols)
    for an in sorted(valeurs):
        w.writerow([an] + [valeurs[an].get(c, "") for c in cols])
print(f"  insee_long.csv : {len(valeurs)} années, {min(valeurs)}-{max(valeurs)}")
