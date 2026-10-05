"""
Données complémentaires pour les figures d'état des lieux : coin fiscal sur le travail et
taux effectif d'imposition des sociétés, depuis l'API SDMX de l'OCDE.

    python extract_situation.py

Sorties dans donnees/ :
  coin_fiscal.csv    décomposition du coin fiscal, célibataire sans enfant au salaire moyen
  eatr_societes.csv  taux effectif moyen d'imposition d'un investissement, méthode Devereux-Griffith
"""
import csv
import json
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


# Taux normal de TVA, janvier 2026. Source : Tax Foundation, VAT Rates in Europe, janvier 2026.
TVA_NORMAL = {"FR": 20.0, "DE": 19.0, "IT": 22.0, "ES": 21.0, "BE": 21.0, "NL": 21.0,
              "SE": 25.0, "DK": 25.0, "PL": 23.0, "AT": 20.0, "IE": 23.0, "PT": 23.0,
              "FI": 25.5, "EL": 24.0, "CZ": 21.0, "HU": 27.0, "EE": 24.0}
NOM2 = {"FR": "France", "DE": "Allemagne", "IT": "Italie", "ES": "Espagne", "BE": "Belgique",
        "NL": "Pays-Bas", "SE": "Suède", "DK": "Danemark", "PL": "Pologne", "AT": "Autriche",
        "IE": "Irlande", "PT": "Portugal", "FI": "Finlande", "EL": "Grèce", "CZ": "Tchéquie",
        "HU": "Hongrie", "EE": "Estonie"}


def eurostat_json(url):
    with tempfile.NamedTemporaryFile(suffix=".json") as t:
        subprocess.run(["curl", "-sS", "--max-time", "180", "-o", t.name, url], check=True)
        with open(t.name, encoding="utf-8") as f:
            return json.load(f)


def assiette_tva():
    """Recettes de TVA rapportées à la consommation finale des ménages, par pays."""
    base = "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data"
    d = eurostat_json(f"{base}/nama_10_gdp?na_item=P31_S14_S15&unit=CP_MEUR&time=2024&format=JSON")
    ids, size = d["id"], d["size"]
    cats = {i: {v: k for k, v in d["dimension"][i]["category"]["index"].items()} for i in ids}
    conso = {}
    for plat, v in d["value"].items():
        plat, co = int(plat), []
        for s in reversed(size):
            co.append(plat % s)
            plat //= s
        co.reverse()
        conso[dict(zip(ids, (cats[i][c] for i, c in zip(ids, co))))["geo"]] = v
    # recettes de TVA en millions d'euros : gov_10a_taxag, catégorie D211, secteur S13 et UE
    t = eurostat_json(f"{base}/gov_10a_taxag?na_item=D211&unit=MIO_EUR&sector=S13_S212"
                      f"&time=2024&format=JSON")
    ids2, size2 = t["id"], t["size"]
    cats2 = {i: {v: k for k, v in t["dimension"][i]["category"]["index"].items()} for i in ids2}
    tva = {}
    for plat, v in t["value"].items():
        plat, co = int(plat), []
        for s2 in reversed(size2):
            co.append(plat % s2)
            plat //= s2
        co.reverse()
        tva[dict(zip(ids2, (cats2[i][c] for i, c in zip(ids2, co))))["geo"]] = v
    lignes = []
    for code, nom in NOM2.items():
        recettes = tva.get(code)
        c = conso.get(code)
        if None in (recettes, c):
            continue
        lignes.append([nom, code, round(100 * recettes / c, 2), TVA_NORMAL[code],
                       round(100 * recettes / c / TVA_NORMAL[code] * 100, 1)])
    lignes.sort(key=lambda l: -l[4])
    with open(OUT / "assiette_tva.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["pays", "code", "recettes_pct_conso", "taux_normal", "taux_de_couverture"])
        w.writerows(lignes)
    return lignes


def taux_superieurs(debut=2000):
    """Taux statutaire supérieur de l'impôt sur le revenu, OCDE."""
    rows = [x for x in telecharge("DSD_TAX_PIT@DF_PIT_TOP_EARN_THRESH", debut)
            if x["MEASURE"] == "TS_PIT" and x["REF_AREA"] in PAYS]
    d = {}
    for x in rows:
        d.setdefault(x["REF_AREA"], {})[int(x["TIME_PERIOD"])] = float(x["OBS_VALUE"])
    ans = sorted({a for v in d.values() for a in v})
    with open(OUT / "taux_superieur_ir.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["pays", "code"] + [str(a) for a in ans])
        for c, v in sorted(d.items()):
            w.writerow([PAYS[c], c] + [v.get(a, "") for a in ans])
    return d, ans


def coin_par_niveau(annee="2025"):
    """Coin fiscal moyen aux trois niveaux de salaire publiés, célibataire sans enfant."""
    rows = [x for x in telecharge("DSD_TAX_WAGES_COMP@DF_TW_COMP", 2025)
            if x["TIME_PERIOD"] == annee and x["HOUSEHOLD_TYPE"] == "S_C0"
            and x["MEASURE"] == "AV_TW" and x["REF_AREA"] in PAYS]
    d = {}
    for x in rows:
        d.setdefault(x["REF_AREA"], {})[x["INCOME_PRINCIPAL"]] = float(x["OBS_VALUE"])
    lignes = [[PAYS[c], c, v.get("AW67"), v.get("AW100"), v.get("AW167")]
              for c, v in d.items() if {"AW67", "AW100", "AW167"} <= set(v)]
    lignes.sort(key=lambda l: -(l[3] or 0))
    with open(OUT / "coin_par_niveau.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["pays", "code", "aw67", "aw100", "aw167"])
        w.writerows(lignes)
    return lignes


def coin_marginal_par_niveau(annee="2025"):
    """Coin fiscal marginal aux trois niveaux de salaire publiés, célibataire sans enfant.

    Mesure MR_TW_PE : part prélevée sur un euro supplémentaire de coût du travail. À distinguer
    du coin moyen AV_TW, qui porte sur la totalité du salaire."""
    rows = [x for x in telecharge("DSD_TAX_WAGES_COMP@DF_TW_COMP", 2025)
            if x["TIME_PERIOD"] == annee and x["HOUSEHOLD_TYPE"] == "S_C0"
            and x["MEASURE"] == "MR_TW_PE" and x["REF_AREA"] in PAYS]
    d = {}
    for x in rows:
        d.setdefault(x["REF_AREA"], {})[x["INCOME_PRINCIPAL"]] = float(x["OBS_VALUE"])
    lignes = [[PAYS[c], c, v.get("AW67"), v.get("AW100"), v.get("AW167")]
              for c, v in d.items() if {"AW67", "AW100", "AW167"} <= set(v)]
    lignes.sort(key=lambda l: -(l[2] or 0))
    with open(OUT / "coin_marginal_par_niveau.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["pays", "code", "aw67", "aw100", "aw167"])
        w.writerows(lignes)
    return lignes


if __name__ == "__main__":
    c = coin_fiscal()
    print(f"coin fiscal : {len(c)} pays ; France = {[l for l in c if l[1] == 'FRA'][0]}")
    e = eatr()
    print(f"taux effectif sociétés : {len(e)} pays ; France = {[l for l in e if l[1] == 'FRA']}")
    a = assiette_tva()
    print(f"assiette TVA : {len(a)} pays ; France = {[l for l in a if l[1] == 'FR']}")
    t, ans = taux_superieurs()
    print(f"taux supérieur IR : {len(t)} pays, {ans[0]}-{ans[-1]}")
    n = coin_par_niveau()
    print(f"coin par niveau : {len(n)} pays ; France = {[l for l in n if l[1] == 'FRA']}")
    m = coin_marginal_par_niveau()
    print(f"coin marginal : {len(m)} pays ; France = {[l for l in m if l[1] == 'FRA']}")
