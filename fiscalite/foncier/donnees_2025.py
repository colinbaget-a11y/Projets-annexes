"""Données du millésime 2025 (décision 5 du 17/11/2026 : base 2025 pour tous les chiffrages).

Complète donnees_foncier.py, dont la structure par commune est gardée (prix DVF 2023-2024, recensement 2022, IA 91) :
les agrégats et ce qui a une valeur 2025 sur une source primaire sont recalés sur 2025.

Fichiers bruts attendus dans BRUT (non versionnés) :
  REI_2025.csv            DGFiP, recensement des éléments d'imposition 2025 (zip « REI-2025-fichier-notice-trace »)
                          https://www.data.gouv.fr/datasets/impots-locaux-fichier-de-recensement-des-elements-dimposition-a-la-fiscalite-directe-locale-rei-4
  full2025.csv.gz         DVF géolocalisées 2025 (Etalab) https://files.data.gouv.fr/geo-dvf/latest/csv/2025/full.csv.gz
  T_8200_AAAA_fr.xlsx     Insee, comptes de patrimoine (tableau 8.200), 2020 à 2025, et T_8200_1959_2019_fr.zip,
                          millésime de juin 2026 (comptes de la Nation 2025) https://www.insee.fr/fr/statistiques/8988859
  T_1101_1103_fr.xlsx     Insee, PIB à prix courants (tableau 1.101), même millésime https://www.insee.fr/fr/statistiques/8988797

Lancer depuis fiscalite/foncier/ : python3 donnees_2025.py BRUT
Sorties (donnees/) :
  tfpb2025_communes.csv      taxe foncière bâtie 2025 par commune (métropole ; mêmes parts que tfpb dans communes.csv.gz)
  ventes_logements_2025.csv  ventes de logements anciens de 2025 par commune (même filtre que donnees_foncier.py)
  terrains_secteurs_2025.csv valeur des terrains et des logements par secteur, fin 2025
  patrimoine_2025.csv        terrains bâtis, logements et PIB, 1978-2025 (millésime 2026 ; 2022 à 2024 révisés)
  croissance_tf.json         ajoute la TFPB 2025 de la métropole (tfpb_2025)
Les xlsx de l'Insee ont une feuille de styles que openpyxl refuse : ils sont lus directement en XML.
"""
import glob
import io
import json
import re
import sys
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

import numpy as np
import pandas as pd

BRUT = Path(sys.argv[1])
OUT = Path(__file__).resolve().parent / "donnees"
HORS = {"57", "67", "68"}
NS = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"
PARTS_TFPB = ["E13", "E23", "E33", "E53", "E53A", "E53gGEMAPI", "E53TASA"]


def plm(code):
    code = code.astype(str)
    return code.mask(code.str.match(r"^751\d\d$"), "75056").mask(code.str.match(r"^6938\d$"), "69123") \
               .mask(code.str.match(r"^132\d\d$"), "13055")


def num(s):
    return pd.to_numeric(s.astype(str).str.replace(",", "."), errors="coerce").fillna(0.0)


# ---------------------------------------------------------------- REI 2025 : taxe foncière bâtie par commune
rei = pd.read_csv(BRUT / "REI_2025.csv", sep=";", usecols=["DEP", "COM"] + PARTS_TFPB, dtype=str, encoding="latin-1",
                  low_memory=False)
rei = rei[rei.DEP.str.len() == 2].copy()
rei["codgeo"] = rei.DEP + rei.COM
rei["tfpb_2025"] = sum(num(rei[k]) for k in PARTS_TFPB)
rei[["codgeo", "tfpb_2025"]].round(0).to_csv(OUT / "tfpb2025_communes.csv", index=False)
cr = json.loads((OUT / "croissance_tf.json").read_text())
cr["tfpb_2025"] = float(rei.tfpb_2025.sum())
cr["source"] = ("REI 2017, 2024 et 2025 (DGFiP), sommes des parts commune, syndicats, groupement, département (2017), "
                "TSE, GEMAPI, TASA ; métropole. Logements : recensement 2022, logements moins HLM, métropole.")
(OUT / "croissance_tf.json").write_text(json.dumps(cr, indent=1), encoding="utf-8")
print(f"TFPB 2025, métropole : {cr['tfpb_2025']/1e9:.3f} Md€ (2024 : {cr['tfpb_2024']/1e9:.3f})")

# ---------------------------------------------------------------- DVF 2025 : ventes de logements anciens par commune
use = ["id_mutation", "nature_mutation", "valeur_fonciere", "code_commune", "code_departement", "code_type_local"]
d = pd.read_csv(BRUT / "full2025.csv.gz", usecols=use, low_memory=False,
                dtype={"code_commune": str, "code_departement": str, "code_type_local": str})
d["code_commune"] = plm(d.code_commune)
d = d[~d.code_departement.isin(HORS) & (d.code_departement.str.len() == 2) & (d.nature_mutation == "Vente")].copy()
d["maison"] = (d.code_type_local == "1").astype(int)
d["appart"] = (d.code_type_local == "2").astype(int)
d["activite"] = (d.code_type_local == "4").astype(int)
m = d.groupby("id_mutation").agg(val=("valeur_fonciere", "first"), com=("code_commune", "first"), nm=("maison", "sum"),
                                 na=("appart", "sum"), nl=("activite", "sum"))
log = m[(m.nm + m.na >= 1) & (m.nl == 0) & (m.val > 5000)]
log = log.assign(val_m=np.where(log.na == 0, log.val, np.where(log.nm == 0, 0.0, log.val * log.nm / (log.nm + log.na))))
log = log.assign(val_a=log.val - log.val_m)
v = log.groupby("com").agg(ventes=("val", "size"), valeur=("val", "sum"), valeur_m=("val_m", "sum"),
                           valeur_a=("val_a", "sum"))
v.index.name = "codgeo"
v.round(0).to_csv(OUT / "ventes_logements_2025.csv")
print(f"DVF 2025 : {len(log):,} ventes de logements anciens, {log.val.sum()/1e9:.1f} Md€")


# ---------------------------------------------------------------- Insee : comptes de patrimoine et PIB
def lire_xlsx(contenu):
    z = zipfile.ZipFile(contenu)
    ss = [("".join(t.text or "" for t in si.iter(NS + "t")))
          for si in ET.fromstring(z.read("xl/sharedStrings.xml")).findall(NS + "si")]
    feuilles = {}
    wb = ET.fromstring(z.read("xl/workbook.xml"))
    rels = {r.get("Id"): r.get("Target") for r in ET.fromstring(z.read("xl/_rels/workbook.xml.rels"))}
    for sh in wb.find(NS + "sheets"):
        cible = rels[sh.get("{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id")].lstrip("/")
        cible = cible if cible.startswith("xl/") else "xl/" + cible
        cel = {}
        for c in ET.fromstring(z.read(cible)).iter(NS + "c"):
            x = c.find(NS + "v")
            if x is not None:
                cel[c.get("r")] = ss[int(x.text)] if c.get("t") == "s" else x.text
        feuilles[sh.get("name")] = cel
    return feuilles


def table_8200(cel):
    """{(code d'actif, secteur): Md€} ; secteurs en ligne 5, codes d'actifs en colonne A."""
    cols = {re.sub(r"\d", "", k): v.strip() for k, v in cel.items() if re.fullmatch(r"[A-Z]+5", k)}
    out = {}
    for k, code in cel.items():
        if not re.fullmatch(r"A\d+", k):
            continue
        r = k[1:]
        for col, sect in cols.items():
            try:
                out[(code.strip(), sect)] = float(cel.get(f"{col}{r}", ""))
            except ValueError:
                pass
    return out


tab = {}
with zipfile.ZipFile(BRUT / "T_8200_1959_2019_fr.zip") as zz:
    for n in zz.namelist():
        a = int(re.search(r"T_8200_(\d{4})", n).group(1))
        if a >= 1978:
            with zz.open(n) as f:
                tab[a] = table_8200(next(iter(lire_xlsx(io.BytesIO(f.read())).values())))
for f in sorted(glob.glob(str(BRUT / "T_8200_20*_fr.xlsx"))):
    a = int(re.search(r"T_8200_(\d{4})_fr", f).group(1))
    tab[a] = table_8200(next(iter(lire_xlsx(f).values())))
pib_cel = lire_xlsx(BRUT / "T_1101_1103_fr.xlsx")["T_1101 en niveau"]
annees = {re.sub(r"\d", "", k): int(v) for k, v in pib_cel.items() if re.fullmatch(r"[A-Z]+4", k)}
ligne = next(k[1:] for k, v in pib_cel.items() if re.fullmatch(r"A\d+", k) and v == "B1GQ")
pib = {a: float(pib_cel[f"{col}{ligne}"]) for col, a in annees.items() if f"{col}{ligne}" in pib_cel}
serie = pd.DataFrame({a: {"pib": pib[a], "terrains_batis": t[("N2111", "S1")], "logements": t[("N111", "S1")],
                          "terrains_batis_men": t[("N2111", "S14")], "logements_men": t[("N111", "S14")],
                          "terrains_cultives": t[("N2112", "S1")], "autres_terrains": t[("N2119", "S1")]}
                      for a, t in sorted(tab.items())}).T
serie.index.name = "annee"
entete = ("# Insee, comptes nationaux annuels base 2020, millésime des comptes de la Nation 2025 (juin 2026) : tableau 8.200\n"
          "# (Md€, fin d'année ; https://www.insee.fr/fr/statistiques/8988859) et PIB à prix courants, tableau 1.101\n"
          "# (Md€ ; https://www.insee.fr/fr/statistiques/8988797). Terrains bâtis = N2111 ; logements = N111 ; men = S14.\n")
(OUT / "patrimoine_2025.csv").write_text(entete + serie.round(3).to_csv(), encoding="utf-8")
t25 = tab[2025]
sect = [("S11", "Sociétés non financières"), ("S12", "Sociétés financières"), ("S13", "Administrations publiques"),
        ("S14", "Ménages"), ("S15", "ISBLSM"), ("S1", "Économie totale")]
codes = ["N2111", "N2112", "N2113", "N2119", "N111", "N1121"]
lignes = ["# Insee, comptes nationaux annuels base 2020, tableau 8.200 « Comptes de patrimoine des secteurs institutionnels "
          "de l'année 2025 » (Md€, fin 2025)",
          "# https://www.insee.fr/fr/statistiques/fichier/8988859/T_8200_2025_fr.xlsx (page https://www.insee.fr/fr/statistiques/8988859), "
          "lu le 16/11/2026 ; actifs non financiers identiques à ceux de l'Insee Première n° 2135 (12/11/2026)",
          "# N2111 terrains supportant des bâtiments et des ouvrages de génie civil ; N2112 terrains cultivés ; N2119 autres "
          "terrains et plans d'eau ; N2113 terrains de loisirs ; N111 logements ; N1121 bâtiments non résidentiels",
          "secteur,libelle," + ",".join(codes)]
for s, lib in sect:
    lignes.append(f"{s},{lib}," + ",".join(f"{t25.get((k, s), 0.0):.3f}" for k in codes))
(OUT / "terrains_secteurs_2025.csv").write_text("\n".join(lignes) + "\n", encoding="utf-8")
print(f"Insee 2025 : terrains bâtis {t25[('N2111', 'S1')]:,.0f} Md€ (ménages {t25[('N2111', 'S14')]:,.0f}) ;"
      f" logements des ménages {t25[('N111', 'S14')]:,.0f} ; PIB 2025 {pib[2025]:,.1f} Md€")
