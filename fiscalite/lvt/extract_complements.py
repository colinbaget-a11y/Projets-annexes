"""
Données complémentaires du brief LVT : indices de prix, de coût et de loyers ; gradient du prix
des terrains à bâtir autour de Paris.

    python extract_complements.py BRUT

Fichiers bruts attendus dans BRUT (en plus de ceux d'extract_lvt.py) :
  IPLA-IPLNA-2015.xml   Insee BDM, indices Notaires-Insee des prix des logements anciens
                        https://bdm.insee.fr/series/sdmx/data/IPLA-IPLNA-2015
  ILC-ILAT-ICC.xml      Insee BDM, indice du coût de la construction (ICC)
                        https://bdm.insee.fr/series/sdmx/data/ILC-ILAT-ICC
  s_001764622.xml       Insee BDM, IPC base 2015, loyers effectivement payés (04.1.1), annuel
                        https://bdm.insee.fr/series/sdmx/data/SERIES_BDM/001764622
  s_001763852.xml       Insee BDM, IPC base 2015, ensemble hors tabac, mensuel
                        https://bdm.insee.fr/series/sdmx/data/SERIES_BDM/001763852
  constr.xml            Insee BDM, construction de logements (Sitadel)
                        https://bdm.insee.fr/series/sdmx/data/CONSTRUCTION-LOGEMENTS
  parc.xml              Insee BDM, estimations annuelles du parc de logements
                        https://bdm.insee.fr/series/sdmx/data/PARC-LOGEMENTS
  full2024.csv.gz       DVF géolocalisées 2024 (Etalab)

Sorties dans donnees/ :
  indices.csv           moyennes annuelles 1996-2025 des quatre indices
  gradient_idf.csv      ventes de terrains à bâtir en Île-de-France : prix au m², distance à Paris
  volumes.csv           logements commencés par an (cumul sur 12 mois en décembre), résidences
                        principales, ventes de logements recensées dans DVF en 2024
"""
import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd

BRUT = Path(sys.argv[1])
OUT = Path(__file__).resolve().parent / "donnees"


def serie(fichier, idbank=None):
    t = (BRUT / fichier).read_text(encoding="utf-8")
    for attrs, corps in re.findall(r"<Series ([^>]*)>(.*?)</Series>", t, re.S):
        if idbank is None or f'IDBANK="{idbank}"' in attrs:
            obs = re.findall(r'TIME_PERIOD="([^"]+)" OBS_VALUE="([^"]*)"', corps)
            s = pd.Series({p: float(v) for p, v in obs if v not in ("", "NaN")})
            return s.groupby(s.index.str[:4].astype(int)).mean()   # moyenne annuelle
    raise ValueError(f"{idbank} introuvable dans {fichier}")


ind = pd.DataFrame({
    "prix_logements_anciens": serie("IPLA-IPLNA-2015.xml", "010567058"),   # France métro, brut
    "cout_construction": serie("ILC-ILAT-ICC.xml", "000008630"),
    "loyers": serie("s_001764622.xml"),
    "prix_conso": serie("s_001763852.xml"),
}).loc[1996:2025]
ind.to_csv(OUT / "indices.csv")

# ---------------------------------------------------------------- volumes français
t = (BRUT / "constr.xml").read_text(encoding="utf-8")
for attrs, corps in re.findall(r"<Series ([^>]*)>(.*?)</Series>", t, re.S):
    if 'IDBANK="001718270"' in attrs:   # logements commencés, cumul 12 mois, France hors Mayotte
        obs = dict(re.findall(r'TIME_PERIOD="([^"]+)" OBS_VALUE="([^"]*)"', corps))
vol = pd.DataFrame({"commences": {int(p[:4]): float(v) for p, v in obs.items() if p.endswith("-12")}})
t = (BRUT / "parc.xml").read_text(encoding="utf-8")
for attrs, corps in re.findall(r"<Series ([^>]*)>(.*?)</Series>", t, re.S):
    if 'IDBANK="001791242"' in attrs:   # résidences principales, France hors Mayotte, milliers
        obs = dict(re.findall(r'TIME_PERIOD="([^"]+)" OBS_VALUE="([^"]*)"', corps))
vol = vol.join(pd.Series({int(p): 1000 * float(v) for p, v in obs.items()}, name="residences_principales"),
               how="outer")

# ---------------------------------------------------------------- gradient francilien
cols = ["id_mutation", "nature_mutation", "valeur_fonciere", "code_departement",
        "code_type_local", "code_nature_culture", "surface_terrain", "longitude", "latitude"]
d = pd.read_csv(BRUT / "full2024.csv.gz", usecols=cols, low_memory=False,
                dtype={"code_departement": str, "code_type_local": str})
d = d[d.nature_mutation.isin(["Vente", "Vente terrain à bâtir"])
      & d.code_departement.isin(["75", "77", "78", "91", "92", "93", "94", "95"])]
g = d.groupby("id_mutation").agg(
    val=("valeur_fonciere", "first"), dep=("code_departement", "first"),
    n_local=("code_type_local", lambda s: s.notna().sum()),
    ab=("code_nature_culture", lambda s: (s == "AB").all()),
    surf=("surface_terrain", "sum"), lon=("longitude", "mean"), lat=("latitude", "mean"))
g = g[g.ab & (g.n_local == 0) & g.surf.between(100, 5000) & (g.val > 1000)].dropna(subset=["lon"])
g["pm2"] = g.val / g.surf
# Distance à vol d'oiseau au parvis de Notre-Dame, en km.
lat0, lon0 = np.radians(48.8530), np.radians(2.3499)
la, lo = np.radians(g.lat), np.radians(g.lon)
g["km"] = 6371 * 2 * np.arcsin(np.sqrt(np.sin((la - lat0) / 2) ** 2
                                       + np.cos(la) * np.cos(lat0) * np.sin((lo - lon0) / 2) ** 2))
g[["dep", "val", "surf", "pm2", "km"]].to_csv(OUT / "gradient_idf.csv")

# Ventes de logements en 2024 : mutations « Vente » comportant au moins une maison ou un appartement.
v = pd.read_csv(BRUT / "full2024.csv.gz", usecols=["id_mutation", "nature_mutation", "code_type_local"],
                dtype={"code_type_local": str}, low_memory=False)
v = v[(v.nature_mutation == "Vente") & v.code_type_local.isin(["1", "2"])]
vol["ventes_logements_dvf"] = np.nan
vol.loc[2024, "ventes_logements_dvf"] = v.id_mutation.nunique()
vol.to_csv(OUT / "volumes.csv")
print(ind.round(1).loc[[1998, 2007, 2024]], "\nterrains franciliens :", len(g))
print(vol.tail(3))
