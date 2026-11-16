"""Extrait des statistiques de recettes de l'OCDE l'impôt sur les bénéfices des sociétés en % du PIB (38 pays).

Source : OCDE, Revenue Statistics, jeu DSD_REV_COMP_OECD@DF_RSOECD, rubrique 1200 (impôts sur le revenu, les
bénéfices et les gains en capital des sociétés), administrations publiques (S13), en % du PIB. Requête :
https://sdmx.oecd.org/public/rest/data/OECD.CTP.TPS,DSD_REV_COMP_OECD@DF_RSOECD,/.TAX_REV.S13.T_1200._T.PT_B1GQ.A?startPeriod=2018&format=csvfilewithlabels
(téléchargée le 16/11/2026 dans le scratchpad, hors dépôt).

Le fichier téléchargé est une donnée non sûre : lancer avec l'interpréteur isolé, en passant son chemin :
    python3 -I is/donnees/extraire_ocde_is_pib.py <chemin du csv téléchargé>   ->  is/donnees/ocde_is_pib.csv
"""
import csv
import sys
from pathlib import Path

OCDE = ("AUS AUT BEL CAN CHL COL CRI CZE DNK EST FIN FRA DEU GRC HUN ISL IRL ISR ITA JPN KOR LVA LTU LUX MEX NLD "
        "NZL NOR POL PRT SVK SVN ESP SWE CHE TUR GBR USA").split()
SORTIE = Path(__file__).resolve().parent / "ocde_is_pib.csv"

lignes = list(csv.DictReader(open(sys.argv[1], encoding="utf-8")))
garde = []
for r in lignes:
    if r["REF_AREA"] in OCDE and r["OBS_VALUE"] and r["UNIT_MEASURE"] == "PT_B1GQ" and r["STANDARD_REVENUE"] == "T_1200":
        garde.append((r["REF_AREA"], int(r["TIME_PERIOD"]), round(float(r["OBS_VALUE"]), 4)))
garde.sort()
with open(SORTIE, "w", encoding="utf-8", newline="") as f:
    w = csv.writer(f)
    w.writerow(["code", "annee", "is_pct_pib"])
    w.writerows(garde)
print(f"{len(garde)} lignes -> {SORTIE}")
