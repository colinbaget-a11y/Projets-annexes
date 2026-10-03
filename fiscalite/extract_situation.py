"""
Données complémentaires pour les figures d'état des lieux : coin fiscal sur le travail et
taux effectif d'imposition des sociétés, depuis l'API SDMX de l'OCDE.

    python extract_situation.py

Sorties dans donnees/ :
  coin_fiscal.csv    décomposition du coin fiscal, célibataire sans enfant au salaire moyen
  eatr_societes.csv  taux effectif moyen d'imposition d'un investissement, méthode Devereux-Griffith
"""
import csv
import subprocess
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / "donnees"
OUT.mkdir(exist_ok=True)
SDMX = "https://sdmx.oecd.org/public/rest/data/OECD.CTP.TPS,{flow},/all?format=csvfilewithlabels"

PAYS = {
    "FRA": "France", "DEU": "Allemagne", "ITA": "Italie", "ESP": "Espagne", "BEL": "Belgique",
    "AUT": "Autriche", "NLD": "Pays-Bas", "SWE": "Suède", "DNK": "Danemark", "POL": "Pologne",
    "GBR": "Royaume-Uni", "USA": "États-Unis", "IRL": "Irlande", "PRT": "Portugal",
    "FIN": "Finlande", "CZE": "Tchéquie", "HUN": "Hongrie", "GRC": "Grèce", "EST": "Estonie",
    "OECD_REP": "Moyenne OCDE", "EU22OECD": "Moyenne UE de l'OCDE",
}


def telecharge(flow, debut):
    """Le service de l'OCDE refuse les requêtes de urllib ; on passe par curl."""
    url = SDMX.format(flow=flow) + f"&startPeriod={debut}"
    with tempfile.NamedTemporaryFile(suffix=".csv") as t:
        subprocess.run(["curl", "-sS", "--max-time", "600", "-o", t.name, url], check=True)
        with open(t.name, encoding="utf-8") as f:
            return list(csv.DictReader(f))


def coin_fiscal(annee="2025"):
    """Décomposition du coin fiscal en points de coût du travail.

    L'OCDE publie l'impôt sur le revenu et les cotisations salariales en % du salaire brut,
    les cotisations patronales en % du salaire brut, et le coin en % du coût du travail. Le
    coût du travail valant le brut augmenté des cotisations patronales, on divise les trois
    premières par (1 + taux patronal) pour les exprimer dans la même unité que le coin.
    """
    rows = [x for x in telecharge("DSD_TAX_WAGES_COMP@DF_TW_COMP", 2025)
            if x["TIME_PERIOD"] == annee and x["HOUSEHOLD_TYPE"] == "S_C0"
            and x["INCOME_PRINCIPAL"] == "AW100" and x["REF_AREA"] in PAYS]
    d = {}
    for x in rows:
        d.setdefault(x["REF_AREA"], {})[x["MEASURE"]] = float(x["OBS_VALUE"])
    lignes = []
    for code, v in d.items():
        ir, ee = v.get("AV_ITR"), v.get("AV_R_EMPEE_SSC")
        er, coin = v.get("AV_R_EMPER_SSC"), v.get("AV_TW")
        if None in (ir, ee, er, coin):
            continue
        k = 1 + er / 100
        lignes.append([PAYS[code], code, round(ir / k, 2), round(ee / k, 2),
                       round(er / k, 2), round(coin, 2), round(ir + ee + er, 2)])
    lignes.sort(key=lambda l: -l[5])
    with open(OUT / "coin_fiscal.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["pays", "code", "impot_revenu_pct_cout", "cotis_salarie_pct_cout",
                    "cotis_employeur_pct_cout", "coin_total_pct_cout", "total_pct_brut"])
        w.writerows(lignes)
    return lignes


def eatr(annee="2025"):
    """Taux effectif moyen et marginal sur un investissement composite, scénario propre au pays."""
    rows = [x for x in telecharge("DSD_ETR@DF_ETR_BASELINE", 2025)
            if x["TIME_PERIOD"] == annee and x["ETR_TAX_TYPE"] == "COMPOSITE"
            and x["ETR_SCENARIO"] == "CS" and x["REF_AREA"] in PAYS]
    d = {}
    for x in rows:
        d.setdefault(x["REF_AREA"], {})[x["MEASURE"]] = float(x["OBS_VALUE"])
    lignes = sorted(([PAYS[c], c, round(v.get("EATR", float("nan")), 2),
                      round(v.get("EMTR", float("nan")), 2)] for c, v in d.items()),
                    key=lambda l: -l[2])
    with open(OUT / "eatr_societes.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["pays", "code", "eatr_pct", "emtr_pct"])
        w.writerows(lignes)
    return lignes


if __name__ == "__main__":
    c = coin_fiscal()
    print(f"coin fiscal : {len(c)} pays ; France = {[l for l in c if l[1] == 'FRA'][0]}")
    e = eatr()
    print(f"taux effectif sociétés : {len(e)} pays ; France = {[l for l in e if l[1] == 'FRA']}")
