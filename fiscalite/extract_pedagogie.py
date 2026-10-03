"""
Données des trois chapitres pédagogiques (partie III) : situation relative des retraités,
et taux statutaires de prélèvements sociaux sur les salaires et sur les pensions.

    python extract_pedagogie.py

Sorties dans donnees/ :
  retraites_niveau_vie.csv  Eurostat ilc_pnp2, revenu médian des 65+ / ensemble, 2024
  pauvrete_age.csv          Eurostat ilc_li02, taux de pauvreté à 60 % du médian par âge, 2024
  prelevements_sociaux.csv  taux statutaires 2026, part salariale et pensions
"""
import csv
import json
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / "donnees"
OUT.mkdir(exist_ok=True)
EURO = "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data"

PAYS = {
    "EU27_2020": "Union européenne", "FR": "France", "DE": "Allemagne", "IT": "Italie",
    "ES": "Espagne", "DK": "Danemark", "SE": "Suède", "NL": "Pays-Bas", "BE": "Belgique",
    "PL": "Pologne", "AT": "Autriche", "FI": "Finlande", "PT": "Portugal", "IE": "Irlande",
    "CZ": "Tchéquie", "LU": "Luxembourg", "EE": "Estonie", "LV": "Lettonie", "LT": "Lituanie",
    "EL": "Grèce", "HU": "Hongrie", "SK": "Slovaquie", "SI": "Slovénie", "HR": "Croatie",
    "RO": "Roumanie", "BG": "Bulgarie", "CY": "Chypre", "MT": "Malte",
}


def eurostat(dataset, **filtres):
    """Renvoie {tuple de codes: valeur} et la liste des dimensions, pour un jeu Eurostat."""
    q = "&".join(f"{k}={v}" for k, v in filtres.items())
    url = f"{EURO}/{dataset}?{q}&format=JSON"
    with urllib.request.urlopen(url, timeout=120) as r:
        d = json.load(r)
    ids, size, dim = d["id"], d["size"], d["dimension"]
    codes = {i: {v: k for k, v in dim[i]["category"]["index"].items()} for i in ids}
    out = {}
    for plat, v in d["value"].items():
        plat, co = int(plat), []
        for s in reversed(size):
            co.append(plat % s)
            plat //= s
        co.reverse()
        out[tuple(codes[i][c] for i, c in zip(ids, co))] = v
    return out, ids


def niveau_vie():
    """ilc_pnp2 : revenu médian équivalent des 65 ans et plus, rapporté à l'ensemble."""
    r, ids = eurostat("ilc_pnp2", sex="T", age="Y_GE65", time=2024)
    gi = ids.index("geo")
    lignes = sorted(((PAYS[k[gi]], k[gi], v) for k, v in r.items() if k[gi] in PAYS),
                    key=lambda x: -x[2])
    with open(OUT / "retraites_niveau_vie.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["pays", "code", "ratio_65plus_sur_ensemble"])
        w.writerows(lignes)
    return lignes


def pauvrete():
    """ilc_li02 : taux de pauvreté au seuil de 60 % du revenu médian, par tranche d'âge."""
    r, ids = eurostat("ilc_li02", unit="PC", sex="T", statinfo="MED_EI", rskpovth="B_60",
                      time=2024)
    gi, ai = ids.index("geo"), ids.index("age")
    ages = ["Y_LT18", "Y18-64", "Y_GE65", "TOTAL"]
    lignes = []
    for code, nom in PAYS.items():
        sub = {k[ai]: v for k, v in r.items() if k[gi] == code}
        if all(a in sub for a in ages):
            lignes.append([nom, code] + [sub[a] for a in ages])
    with open(OUT / "pauvrete_age.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["pays", "code", "moins_18", "18_64", "65_plus", "ensemble"])
        w.writerows(lignes)
    return lignes


# Taux statutaires 2026. Salaire : part salariale, secteur privé, rémunération sous le
# plafond de la sécurité sociale. CSG et CRDS assises sur 98,25 % du brut pour les revenus
# d'activité, sur 100 % de la pension pour les retraites.
# Sources : Urssaf, taux de cotisations du secteur privé au 1er janvier 2026 ;
# service-public.gouv.fr, fiche F2971, prélèvements sociaux sur les pensions.
SOCIAL = [
    # catégorie, libellé, taux effectif sur le revenu brut, nature
    ("salaire", "CSG", 9.20 * 0.9825, "non contributif"),
    ("salaire", "CRDS", 0.50 * 0.9825, "non contributif"),
    ("salaire", "Vieillesse plafonnée", 6.90, "contributif"),
    ("salaire", "Vieillesse déplafonnée", 0.40, "contributif"),
    ("salaire", "Retraite complémentaire T1", 3.15, "contributif"),
    ("salaire", "Contribution d'équilibre général T1", 0.86, "contributif"),
    ("pension_normal", "CSG taux normal", 8.30, "non contributif"),
    ("pension_normal", "CRDS", 0.50, "non contributif"),
    ("pension_normal", "CASA", 0.30, "non contributif"),
    ("pension_median", "CSG taux médian", 6.60, "non contributif"),
    ("pension_median", "CRDS", 0.50, "non contributif"),
    ("pension_median", "CASA", 0.30, "non contributif"),
    ("pension_reduit", "CSG taux réduit", 3.80, "non contributif"),
    ("pension_reduit", "CRDS", 0.50, "non contributif"),
    ("pension_exonere", "Aucun prélèvement", 0.00, "non contributif"),
]


def sociaux():
    with open(OUT / "prelevements_sociaux.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["categorie", "libelle", "taux_pct_brut", "nature"])
        for c, l, t, n in SOCIAL:
            w.writerow([c, l, round(t, 4), n])
    return SOCIAL


if __name__ == "__main__":
    nv = niveau_vie()
    pv = pauvrete()
    sociaux()
    print(f"niveau de vie des 65+ : {len(nv)} pays, France = "
          f"{dict((c, v) for _, c, v in nv)['FR']}")
    print(f"pauvreté par âge : {len(pv)} pays")
    print("taux sociaux : ", {
        c: round(sum(t for cc, _, t, _ in SOCIAL if cc == c), 2)
        for c in ("salaire", "pension_normal", "pension_median", "pension_reduit")})
