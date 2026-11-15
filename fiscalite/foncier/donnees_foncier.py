"""Données par commune pour les simulations de la note foncière.

Les fichiers bruts ne sont pas versionnés. Les télécharger dans un répertoire BRUT, puis :

    python3 donnees_foncier.py BRUT          (depuis fiscalite/foncier/)

Fichiers bruts attendus dans BRUT :
  REI_2024.csv                DGFiP, recensement des éléments d'imposition 2024 (fiscalité directe locale)
                              https://www.data.gouv.fr/datasets/impots-locaux-fichier-de-recensement-des-elements-dimposition-a-la-fiscalite-directe-locale-rei-4
  base-cc-logement-2022.CSV   Insee, recensement 2022, logement par commune
                              https://www.insee.fr/fr/statistiques/8581474
  IA91.xlsx                   Insee Analyses n° 91 (André et Meslin, 2023), figure 5a : taxe foncière / valeur
                              des logements par commune, 2017      https://www.insee.fr/fr/statistiques/7735076
  full2023.csv.gz, full2024.csv.gz   DVF géolocalisées (Etalab)
                              https://files.data.gouv.fr/geo-dvf/latest/csv/2024/full.csv.gz (idem 2023)

Sortie : donnees/communes.csv.gz (une ligne par commune de France métropolitaine hors Alsace-Moselle, où DVF
n'existe pas) et donnees/terrains_dep.csv (prix des terrains à bâtir par département).
"""
import sys
from pathlib import Path

import numpy as np
import openpyxl
import pandas as pd

BRUT = Path(sys.argv[1])
OUT = Path(__file__).resolve().parent / "donnees"
OUT.mkdir(exist_ok=True)
HORS = {"57", "67", "68"}                      # Alsace-Moselle : livre foncier, pas de DVF


def plm(code):
    """Arrondissements de Paris, Lyon et Marseille ramenés à la commune (le REI ne connaît que la commune)."""
    code = code.astype(str)
    return code.mask(code.str.match(r"^751\d\d$"), "75056").mask(code.str.match(r"^6938\d$"), "69123") \
               .mask(code.str.match(r"^132\d\d$"), "13055")


def num(s):
    return pd.to_numeric(s.astype(str).str.replace(",", "."), errors="coerce").fillna(0.0)


# ---------------------------------------------------------------- REI 2024 : taxe foncière bâtie par commune
cols = ["DEP", "COM", "LIBCOM", "SIREPCI", "E11", "E12", "E13", "E23", "E33", "E32", "E53", "E53A",
        "E53gGEMAPI", "E53TASA", "H13THS", "H33THS"]
rei = pd.read_csv(BRUT / "REI_2024.csv", sep=";", usecols=cols, dtype=str, encoding="latin-1", low_memory=False)
rei = rei[rei.DEP.str.len() == 2].copy()                       # métropole (DOM exclus : pas de données IA91)
rei["codgeo"] = rei.DEP + rei.COM
for c in cols[4:]:
    rei[c] = num(rei[c])
rei["tfpb"] = rei[["E13", "E23", "E33", "E53", "E53A", "E53gGEMAPI", "E53TASA"]].sum(axis=1)
rei["taux_tfpb"] = rei.E12 + rei.E32                            # commune + groupement, en %
rei["thrs"] = rei.H13THS + rei.H33THS
rei = rei.rename(columns={"DEP": "dep", "SIREPCI": "epci", "LIBCOM": "nom", "E11": "base_tfpb"})[
    ["codgeo", "dep", "epci", "nom", "tfpb", "base_tfpb", "taux_tfpb", "thrs"]].set_index("codgeo")

# ---------------------------------------------------------------- Insee RP 2022 : parc de logements
rp_cols = ["CODGEO", "P22_LOG", "P22_RP", "P22_RSECOCC", "P22_LOGVAC", "P22_MAISON", "P22_APPART", "P22_RP_PROP",
           "P22_RP_LOC", "P22_RP_LOCHLMV", "P22_RP_GRAT", "P22_RPMAISON", "P22_RPAPPART", "P22_PMEN"]
rp = pd.read_csv(BRUT / "base-cc-logement-2022.CSV", sep=";", usecols=rp_cols, dtype={"CODGEO": str})
rp = rp.set_index("CODGEO")
rp.columns = [c.replace("P22_", "").lower() for c in rp.columns]

# ---------------------------------------------------------------- Insee IA 91 : TF / valeur des logements, 2017
ws = openpyxl.load_workbook(BRUT / "IA91.xlsx", data_only=True, read_only=True)["Figure 5a"]
ia = pd.DataFrame([r[:2] for r in ws.iter_rows(min_row=4, values_only=True)
                   if r[0] and isinstance(r[1], (int, float))], columns=["codgeo", "tf_valeur_2017"])
ia["codgeo"] = ia.codgeo.astype(str).str.zfill(5)
# Paris, Lyon, Marseille : moyenne des arrondissements pondérée par leur nombre de logements (recensement)
ia["com"] = plm(ia.codgeo)
ia["w"] = ia.codgeo.map(rp.log).fillna(1.0)
ia = ia.groupby("com").apply(lambda g: (g.tf_valeur_2017 * g.w).sum() / g.w.sum(), include_groups=False) \
       .rename("tf_valeur_2017").to_frame()
ia.index.name = "codgeo"

# ---------------------------------------------------------------- DVF 2023 et 2024
use = ["id_mutation", "nature_mutation", "valeur_fonciere", "code_commune", "code_departement", "id_parcelle",
       "code_type_local", "surface_reelle_bati", "code_nature_culture", "surface_terrain"]
parts = []
for an in (2023, 2024):
    d = pd.read_csv(BRUT / f"full{an}.csv.gz", usecols=use, low_memory=False,
                    dtype={"code_commune": str, "code_departement": str, "code_type_local": str})
    d["annee"] = an
    d["id_mutation"] = d.id_mutation.astype(str)
    d["code_commune"] = plm(d.code_commune)
    parts.append(d)
d = pd.concat(parts, ignore_index=True)
del parts
d = d[~d.code_departement.isin(HORS) & (d.code_departement.str.len() == 2)]

# Ventes (hors VEFA, soumises à la TVA et à des droits réduits) contenant au moins un logement et aucun local
# d'activité : assiette des droits de mutation sur les logements anciens.
v = d[d.nature_mutation == "Vente"].copy()
v["maison"] = (v.code_type_local == "1").astype(int)
v["appart"] = (v.code_type_local == "2").astype(int)
v["activite"] = (v.code_type_local == "4").astype(int)
v["sb_m"] = np.where(v.maison == 1, v.surface_reelle_bati, 0.0)
v["sb_a"] = np.where(v.appart == 1, v.surface_reelle_bati, 0.0)
m = v.groupby(["annee", "id_mutation"]).agg(val=("valeur_fonciere", "first"), com=("code_commune", "first"),
                                            dep=("code_departement", "first"), nm=("maison", "sum"),
                                            na=("appart", "sum"), nl=("activite", "sum"),
                                            sbm=("sb_m", "max"), sba=("sb_a", "sum"))
# surface de terrain des maisons : parcelles distinctes de la mutation
t = v[v.maison == 1].drop_duplicates(["annee", "id_mutation", "id_parcelle"]).groupby(
    ["annee", "id_mutation"]).surface_terrain.sum()
m["terrain"] = t.reindex(m.index).fillna(0.0)
m = m.reset_index()
log = m[(m.nm + m.na >= 1) & (m.nl == 0) & (m.val > 5000)]
# assiette des DMTO sur les logements : moyenne annuelle 2023-2024 par commune
log = log.assign(val_m=np.where(log.na == 0, log.val, np.where(log.nm == 0, 0.0, log.val * log.nm / (log.nm + log.na))))
log = log.assign(val_a=log.val - log.val_m)
dmto = log.groupby(["com", "annee"]).agg(n=("val", "size"), valeur=("val", "sum"), valeur_m=("val_m", "sum"),
                                         valeur_a=("val_a", "sum")).groupby("com").mean()
dmto.columns = ["ventes_an", "valeur_ventes_an", "valeur_ventes_m_an", "valeur_ventes_a_an"]

# prix au m² : ventes d'un seul logement
mai = log[(log.nm == 1) & (log.na == 0) & log.sbm.between(30, 400) & log.terrain.between(50, 20000)].copy()
mai["pm2"] = mai.val / mai.sbm
mai = mai[mai.pm2.between(200, 30000)]
app = log[(log.na == 1) & (log.nm == 0) & log.sba.between(10, 300)].copy()
app["pm2"] = app.val / app.sba
app = app[app.pm2.between(300, 40000)]


def stats(df, cle, pref, surf):
    g = df.groupby(cle).agg(n=("pm2", "size"), pm2=("pm2", "median"), surf=(surf, "median"))
    g.columns = [f"{pref}_{c}" for c in g.columns]
    return g


com_m, com_a = stats(mai, "com", "m", "sbm"), stats(app, "com", "a", "sba")
dep_m, dep_a = stats(mai, "dep", "m", "sbm"), stats(app, "dep", "a", "sba")
terr = mai.groupby("com").terrain.median().rename("m_terrain")
terr_dep = mai.groupby("dep").terrain.median().rename("m_terrain")

# terrains à bâtir : mutations dont toutes les lignes sont « AB », sans local, 100 à 5 000 m²
tb = d[d.nature_mutation.isin(["Vente", "Vente terrain à bâtir"])].copy()
tb["ab"] = (tb.code_nature_culture == "AB").astype(int)
tb["loc"] = tb.code_type_local.notna().astype(int)
g = tb.groupby(["annee", "id_mutation"]).agg(val=("valeur_fonciere", "first"), dep=("code_departement", "first"),
                                             com=("code_commune", "first"), ab=("ab", "min"), nloc=("loc", "sum"),
                                             surf=("surface_terrain", "sum"))
g = g[(g.ab == 1) & (g.nloc == 0) & g.surf.between(100, 5000) & (g.val > 1000)].copy()
g["pm2"] = g.val / g.surf
g = g[g.pm2.between(1, 3000)]
terrains_dep = g.groupby("dep").agg(n_tab=("pm2", "size"), pm2_tab=("pm2", "median"), surf_tab=("surf", "median"))
terrains_com = g.groupby("com").agg(n_tab_com=("pm2", "size"), pm2_tab_com=("pm2", "median"))
terrains_dep.join(dep_m).join(terr_dep).to_csv(OUT / "terrains_dep.csv")

# ---------------------------------------------------------------- assemblage
c = rei.join(rp, how="left").join(ia, how="left").join(dmto, how="left").join(com_m).join(com_a).join(terr) \
       .join(terrains_com)
c = c[~c.dep.isin(HORS)]
for col in ("ventes_an", "valeur_ventes_an", "valeur_ventes_m_an", "valeur_ventes_a_an"):
    c[col] = c[col].fillna(0.0)
# replis : commune (au moins 10 ventes), sinon intercommunalité, sinon département
for pref, mm in (("m", mai), ("a", app)):
    mm = mm.merge(c[["epci"]], left_on="com", right_index=True, how="left")
    ep = mm.groupby("epci").agg(n=("pm2", "size"), pm2=("pm2", "median"))
    dp = mm.groupby("dep").agg(pm2=("pm2", "median"), surf=("sbm" if pref == "m" else "sba", "median"))
    ok = c[f"{pref}_n"].fillna(0) >= 10
    via_epci = c.epci.map(ep.pm2.where(ep.n >= 10))
    c[f"{pref}_pm2_src"] = np.where(ok, "commune", np.where(via_epci.notna(), "epci", "departement"))
    c[f"{pref}_pm2"] = np.where(ok, c[f"{pref}_pm2"], via_epci.fillna(c.dep.map(dp.pm2)))
    c[f"{pref}_surf"] = np.where(ok, c[f"{pref}_surf"], c.dep.map(dp.surf))
c["m_terrain"] = c.m_terrain.where(c.m_n.fillna(0) >= 10, c.dep.map(terr_dep))
c["pm2_tab_dep"] = c.dep.map(terrains_dep.pm2_tab)
c.index.name = "codgeo"
c.round(4).to_csv(OUT / "communes.csv.gz")
print("communes :", len(c), "| avec IA91 :", c.tf_valeur_2017.notna().sum(), "| logements :", c.log.sum() / 1e6,
      "M | ventes de logements par an :", round(c.ventes_an.sum() / 1e3), "k, valeur", round(c.valeur_ventes_an.sum() / 1e9, 1),
      "Md€ | TFPB", round(c.tfpb.sum() / 1e9, 1), "Md€")
print("source du prix au m² (maisons) :", c.m_pm2_src.value_counts().to_dict())
print("source du prix au m² (appartements) :", c.a_pm2_src.value_counts().to_dict())
