"""
Données du projet « à qui attribuer la dette publique ? », par sous-secteur des administrations
publiques (APU). Source : Eurostat, API de diffusion (JSON-stat).

    python dette/extract_dette.py

Sous-secteurs (SEC 2010) : S13 APU ; S1311 administration centrale (État et organismes divers
d'administration centrale, ODAC) ; S1313 administrations publiques locales (APUL) ; S1314
administrations de sécurité sociale (ASSO). Eurostat ne sépare pas l'État des ODAC.

Sorties dans dette/donnees/ :
  comptes.csv  gov_10a_main : dépenses (TE), recettes (TR), solde (B9), intérêts, transferts
               courants (D7) et en capital (D9) versés à chaque autre sous-secteur, revenus de la
               propriété versés aux autres sous-secteurs (D4), en millions d'euros, 1995-2025
  dette.csv    gov_10dd_edpt1 : dette de Maastricht (GD) par sous-secteur, en millions d'euros
  cofog.csv    gov_10a_exp : dépense totale par fonction (COFOG, 1er niveau, et vieillesse GF1002),
               APU et sous-secteurs
  impots.csv   gov_10a_taxag : impôts et cotisations reçus par sous-secteur (TVA D211, autres impôts
               sur les produits D214, impôts sur la production D29, impôts sur le revenu D5/D51,
               cotisations sociales D61), en millions d'euros
  pib.csv      PIB à prix courants (nama_10_gdp)
  dette_insee.csv  Insee, dette trimestrielle de Maastricht par sous-secteur (contributions
               consolidées, en milliards d'euros), valeur du 4e trimestre, 1995-2025 :
               État, ODAC, APUL, ASSO (flux DETTE-TRIM-APU-2020 de la BDM)
"""
import csv
import json
import re
import urllib.request
from pathlib import Path

OUT = Path(__file__).resolve().parent / "donnees"
OUT.mkdir(exist_ok=True)
API = "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/"
SECTEURS = ["S13", "S1311", "S1313", "S1314"]


def jsonstat(dataset, **filtres):
    """Télécharge un jeu Eurostat et le renvoie en lignes {dimension: code, ..., valeur}."""
    q = "&".join(f"{k}={v}" for k, vs in filtres.items()
                 for v in (vs if isinstance(vs, list) else [vs]))
    with urllib.request.urlopen(f"{API}{dataset}?{q}", timeout=300) as r:
        d = json.load(r)
    dims, tailles = d["id"], d["size"]
    codes = []
    for dim in dims:
        idx = d["dimension"][dim]["category"]["index"]
        codes.append(sorted(idx, key=idx.get))
    lignes = []
    for cle, val in d["value"].items():
        k, pos = int(cle), []
        for t in reversed(tailles):
            pos.append(k % t)
            k //= t
        pos.reverse()
        lignes.append({**{dim: codes[i][p] for i, (dim, p) in enumerate(zip(dims, pos))},
                       "valeur": val})
    return lignes


def ecrire(nom, lignes, cols):
    with open(OUT / nom, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols + ["valeur"], extrasaction="ignore")
        w.writeheader()
        w.writerows(sorted(lignes, key=lambda l: tuple(l[c] for c in cols)))
    print(f"  {nom} : {len(lignes)} valeurs")


ITEMS = ["TE", "TR", "B9", "D41PAY", "D41REC", "P5", "D1PAY", "D62PAY", "D632PAY",
         "D7PAY", "D7REC", "D73PAY", "D73REC", "D9PAY", "D9REC", "D92PAY", "D92REC", "D99PAY",
         "D99REC", "D2REC", "D5REC", "D61REC", "D91REC"]
for s in ("S1311", "S1313", "S1314"):
    ITEMS += [f"D7PAY_{s}", f"D9PAY_{s}", f"D4PAY_{s}"]

comptes = jsonstat("gov_10a_main", geo="FR", unit="MIO_EUR", sector=SECTEURS, na_item=ITEMS)
ecrire("comptes.csv", comptes, ["sector", "na_item", "time"])
dette = jsonstat("gov_10dd_edpt1", geo="FR", unit="MIO_EUR", sector=SECTEURS, na_item="GD")
ecrire("dette.csv", dette, ["sector", "na_item", "time"])
cofog = jsonstat("gov_10a_exp", geo="FR", unit="MIO_EUR", sector=SECTEURS, na_item="TE",
                 cofog99=[f"GF{n:02d}" for n in range(1, 11)] + ["GF1002", "TOTAL"])
ecrire("cofog.csv", cofog, ["sector", "cofog99", "time"])
impots = jsonstat("gov_10a_taxag", geo="FR", unit="MIO_EUR", sector=SECTEURS,
                  na_item=["D2", "D211", "D214", "D214A", "D29", "D29C", "D5", "D51", "D51A",
                           "D51B", "D61", "D611", "D613"])
ecrire("impots.csv", impots, ["sector", "na_item", "time"])
pib = jsonstat("nama_10_gdp", geo="FR", unit="CP_MEUR", na_item="B1GQ")
ecrire("pib.csv", pib, ["time"])

# ---------------------------------------------------------------- Insee : dette par sous-secteur
SERIES = {"010777610": "Etat", "010777613": "ODAC", "010777626": "APUL", "010777625": "ASSO",
          "010777616": "APU"}
with urllib.request.urlopen("https://bdm.insee.fr/series/sdmx/data/DETTE-TRIM-APU-2020",
                            timeout=300) as r:
    t = r.read().decode("utf-8")
lignes = []
for attrs, corps in re.findall(r"<Series ([^>]*)>(.*?)</Series>", t, re.S):
    idb = re.search(r'IDBANK="(\d+)"', attrs).group(1)
    if idb in SERIES:
        for per, val in re.findall(r'TIME_PERIOD="([^"]+)" OBS_VALUE="([^"]*)"', corps):
            if per.endswith("Q4") and val not in ("", "NaN"):
                lignes.append({"sous_secteur": SERIES[idb], "time": per[:4], "valeur": float(val)})
ecrire("dette_insee.csv", lignes, ["sous_secteur", "time"])
