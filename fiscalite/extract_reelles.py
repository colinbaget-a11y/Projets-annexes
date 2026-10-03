"""Données réelles pour la refonte du cours : Tax Foundation et OCDE.

Sources téléchargées, dans l'ordre :
- Tax Foundation, Corporate Tax Rates around the World (github.com/TaxFoundation/
  worldwide-corporate-tax-rates), taux statutaires d'IS 1980-2023 ;
- Tax Foundation, International Tax Competitiveness Index 2025 (github.com/TaxFoundation/
  international-tax-competitiveness-index), 46 variables pour les 38 pays de l'OCDE, dont le
  taux d'IS 2024 et 2025, la valeur actuelle des amortissements, le ratio de recettes de TVA,
  les taux sur dividendes et plus-values et l'existence des impôts sur le patrimoine ;
- OCDE, Revenue Statistics (DSD_REV_COMP_OECD@DF_RSOECD), recettes par catégorie en % du PIB ;
- OCDE, taux supérieur de l'impôt sur le revenu et seuil d'application
  (DSD_TAX_PIT@DF_PIT_TOP_EARN_THRESH).

Usage : python extract_reelles.py   (écrit dans donnees/)
"""
import csv
import io
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / "donnees"
OUT.mkdir(exist_ok=True)

TF = "https://raw.githubusercontent.com/TaxFoundation"
OCDE = "https://sdmx.oecd.org/public/rest/data/OECD.CTP.TPS,{flow},/{cle}?{q}&format=csvfilewithlabels"

NOMS = {
    "AUS": "Australie", "AUT": "Autriche", "BEL": "Belgique", "CAN": "Canada", "CHE": "Suisse",
    "CHL": "Chili", "COL": "Colombie", "CRI": "Costa Rica", "CZE": "Tchéquie", "DEU": "Allemagne",
    "DNK": "Danemark", "ESP": "Espagne", "EST": "Estonie", "FIN": "Finlande", "FRA": "France",
    "GBR": "Royaume-Uni", "GRC": "Grèce", "HUN": "Hongrie", "IRL": "Irlande", "ISL": "Islande",
    "ISR": "Israël", "ITA": "Italie", "JPN": "Japon", "KOR": "Corée", "LTU": "Lituanie",
    "LUX": "Luxembourg", "LVA": "Lettonie", "MEX": "Mexique", "NLD": "Pays-Bas", "NOR": "Norvège",
    "NZL": "Nouvelle-Zélande", "POL": "Pologne", "PRT": "Portugal", "SVK": "Slovaquie",
    "SVN": "Slovénie", "SWE": "Suède", "TUR": "Turquie", "USA": "États-Unis",
    "OECD_REP": "Moyenne OCDE",
}


def get(url):
    """Le service de l'OCDE refuse urllib ; curl passe, avec le proxy de l'environnement."""
    r = subprocess.run(["curl", "-sS", "--fail", "--max-time", "300", url],
                       check=True, capture_output=True)
    return r.stdout.decode("utf-8-sig")


def ecrit(nom, entete, lignes):
    with open(OUT / nom, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(entete)
        w.writerows(lignes)
    print(f"  {nom} : {len(lignes)} lignes")


def itci(annee):
    txt = get(f"{TF}/international-tax-competitiveness-index/master/final_data/"
              f"final_index_data_{annee}.csv")
    return list(csv.DictReader(io.StringIO(txt)))


def taux_is():
    """IS statutaire 1980-2023 (Tax Foundation), complété par l'indice pour 2024 et 2025."""
    txt = get(f"{TF}/worldwide-corporate-tax-rates/master/final_data/final_data_long.csv")
    r = list(csv.DictReader(io.StringIO(txt)))
    d = {}
    for x in r:
        if x["oecd"] in ("1", "TRUE") and x["rate"] not in ("", "NA") and int(x["year"]) >= 1980:
            d.setdefault(x["iso_3"], {})[int(x["year"])] = float(x["rate"])
    for a in (2024, 2025):
        for x in itci(a):
            d.setdefault(x["ISO_3"], {})[a] = 100 * float(x["corporate_rate"])
    ans = list(range(1980, 2026))
    lignes = [[NOMS.get(p, p), p] + [d[p].get(a, "") for a in ans] for p in sorted(d)]
    ecrit("is_taux_1980_2025.csv", ["pays", "code"] + ans, lignes)


def indice_2025():
    """Les 46 variables de l'indice 2025, telles quelles, avec le nom français du pays."""
    r = itci(2025)
    cles = [k for k in r[0] if k not in ("ISO_2", "country", "year")]
    ecrit("itci_variables_2025.csv", ["pays"] + cles,
          [[NOMS.get(x["ISO_3"], x["country"])] + [x[k] for k in cles] for x in r])


def recettes():
    """Recettes publiques par catégorie OCDE, en % du PIB, 1995-2024."""
    cats = "T_1100+T_1200+T_2000+T_3000+T_4000+T_4100+T_4200+T_4300+T_4400+T_5000+T_5111+_T"
    txt = get(OCDE.format(flow="DSD_REV_COMP_OECD@DF_RSOECD", cle=f"..S13.{cats}..PT_B1GQ.A",
                          q="startPeriod=1995&endPeriod=2024"))
    r = list(csv.DictReader(io.StringIO(txt)))
    lignes = sorted([NOMS.get(x["REF_AREA"], x["REF_AREA"]), x["REF_AREA"], x["STANDARD_REVENUE"],
                     x["TIME_PERIOD"], x["OBS_VALUE"]] for x in r if x["OBS_VALUE"])
    ecrit("recettes_ocde_pct_pib.csv", ["pays", "code", "categorie", "annee", "pct_pib"], lignes)


def taux_superieur_et_seuil():
    """Taux supérieur de l'IR et seuil d'application en multiple du salaire moyen."""
    txt = get(OCDE.format(flow="DSD_TAX_PIT@DF_PIT_TOP_EARN_THRESH", cle="all",
                          q="startPeriod=2020"))
    r = list(csv.DictReader(io.StringIO(txt)))
    d = {}
    for x in r:
        if x["MEASURE"] in ("TS_PIT", "TS_PIT_TH") and x["OBS_VALUE"]:
            d.setdefault((x["REF_AREA"], x["TIME_PERIOD"]), {})[x["MEASURE"]] = x["OBS_VALUE"]
    lignes = [[NOMS.get(p, p), p, a, v.get("TS_PIT", ""), v.get("TS_PIT_TH", "")]
              for (p, a), v in sorted(d.items()) if p in NOMS]
    ecrit("taux_superieur_et_seuil.csv", ["pays", "code", "annee", "taux", "seuil_x_salaire_moyen"],
          lignes)


if __name__ == "__main__":
    taux_is()
    indice_2025()
    recettes()
    taux_superieur_et_seuil()
