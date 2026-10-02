"""
Données permettant de répliquer pour la France les diagnostics chiffrés de la Mirrlees Review
(« Tax by Design », IFS, 2011).

Trois sources OCDE, toutes en accès libre par l'API SDMX :

  TaxBEN, taux marginaux effectifs (DSD_TAXBEN_METR@DF_METR)
      Taux effectif de prélèvement sur une augmentation du temps de travail, par type de
      ménage et niveau de salaire. Équivalent des figures 4.5 et 4.8 de Tax by Design.

  TaxBEN, taux de participation (DSD_TAXBEN_PTR@DF_PTRSA)
      Part du salaire perdue en impôts et en prestations retirées lors d'une reprise d'emploi
      depuis l'aide sociale. Équivalent des figures 4.5 et 4.7.

  Effective Carbon Rates (DSD_ECR@DF_SEP et DF_CPS)
      Part des émissions de CO2 tarifées au-dessus de différents seuils, par secteur.
      Équivalent du diagnostic du chapitre 11 sur l'hétérogénéité du prix implicite du carbone.

    python extract_mirrlees.py
"""
import csv
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
DATA = HERE / "donnees"
BRUT = HERE / "sources"
API = "https://sdmx.oecd.org/public/rest/data/{ag},{df},/all?format=csvfilewithlabels{per}"

PAYS = ["FRA", "DEU", "GBR", "DNK", "SWE", "ITA", "ESP", "NLD", "BEL", "AUT", "POL", "USA", "OECD"]

JEUX = {
    "taxben_metr": ("OECD.ELS.JAI", "DSD_TAXBEN_METR@DF_METR", "&startPeriod=2023",
                    ["REF_AREA", "TIME_PERIOD", "MEASURE", "WORKING_HOURS_INCREASE", "INCOME_CURR",
                     "HOUSEHOLD_TYPE", "INCOME_PART", "SOC_ASS_BENEFIT", "HOUSE_BENEFIT", "OBS_VALUE"]),
    "taxben_ptr": ("OECD.ELS.JAI", "DSD_TAXBEN_PTR@DF_PTRSA", "&startPeriod=2023",
                   ["REF_AREA", "TIME_PERIOD", "MEASURE", "INCOME_CURR", "HOUSEHOLD_TYPE",
                    "INCOME_PART", "HOUSE_BENEFIT", "TEMP_INTOWORK_BENEFIT", "OBS_VALUE"]),
    "carbone_parts": ("OECD.CTP.TPS", "DSD_ECR@DF_SEP", "",
                      ["REF_AREA", "TIME_PERIOD", "SECTOR", "Economic sector", "EMISSIONS_SOURCE",
                       "PRICE_LEVEL", "Carbon price level", "OBS_VALUE"]),
    "carbone_score": ("OECD.CTP.TPS", "DSD_ECR@DF_CPS", "",
                      ["REF_AREA", "TIME_PERIOD", "SECTOR", "Economic sector", "EMISSIONS_SOURCE",
                       "PRICE_LEVEL", "Carbon price level", "OBS_VALUE"]),
}


def telecharger(nom, ag, df, per, cache):
    p = (Path(cache) if cache else BRUT) / f"{nom}.csv"
    if not p.exists():
        p.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(["curl", "-sS", "--max-time", "600", "-o", str(p),
                        API.format(ag=ag, df=df, per=per)], check=True)
    return p


def extraire(nom, cols, src):
    lignes = []
    with open(src, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row.get("REF_AREA") not in PAYS or not row.get("OBS_VALUE"):
                continue
            lignes.append({c: row.get(c, "") for c in cols})
    dst = DATA / f"{nom}.csv"
    with open(dst, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        w.writerows(lignes)
    print(f"{dst.name} : {len(lignes)} lignes, {len({l['REF_AREA'] for l in lignes})} pays")


if __name__ == "__main__":
    import sys
    cache = sys.argv[sys.argv.index("--cache") + 1] if "--cache" in sys.argv else None
    DATA.mkdir(exist_ok=True)
    for nom, (ag, df, per, cols) in JEUX.items():
        extraire(nom, cols, telecharger(nom, ag, df, per, cache))
