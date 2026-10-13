"""
Attribution de la dette publique par fonction, en supposant toutes les dépenses fongibles.

    python dette/fongible.py

Principe (la « méthode simple ») : les impôts ne sont affectés à aucune dépense ; chaque année, le
déficit des administrations publiques finance donc chaque euro de dépense dans la même proportion.
La dette de l'année se répartit entre fonctions (classification COFOG : justice et police, défense,
enseignement, santé, vieillesse…) au prorata de leur dépense, hors intérêts.

Mise en œuvre, année par année de 1996 à 2025 :
  - la hausse de la dette hors intérêts (déficit primaire et ajustements stock-flux) est répartie
    au prorata de la dépense primaire de chaque fonction de l'année ;
  - les intérêts suivent la dette : chaque fonction paie les intérêts de la dette qui lui est
    attribuée, au taux apparent des administrations publiques ;
  - le stock de fin 1995 est réparti selon la dépense par fonction de 1995 (la fongibilité est
    supposée valoir aussi avant 1995) ; variante : seule la dette créée depuis 1995.
Les intérêts sont retirés de la fonction « services généraux », où COFOG les classe.
La dépense par fonction de 2025, pas encore publiée, est celle de 2024.

Sorties dans dette/donnees/ :
  fonctions_2025.csv           dette attribuée fin 2025 par fonction, part, part de la dépense
  fonctions_evolution.csv      dépense par fonction en % du PIB, 1995-2024
"""
from pathlib import Path

import pandas as pd

D = Path(__file__).resolve().parent / "donnees"
LIB = {"GF03": "Ordre et sécurité (police, justice)", "GF02": "Défense",
       "GF01": "Services généraux (hors intérêts)", "GF04": "Affaires économiques",
       "GF05": "Environnement", "GF06": "Logement et équipements collectifs",
       "GF08": "Culture et sport", "GF09": "Enseignement", "GF07": "Santé",
       "GF1002": "Vieillesse", "GF10X": "Autre protection sociale"}
SOCIAL = ["GF07", "GF1002", "GF10X"]

f = pd.read_csv(D / "cofog.csv")
f = f[f.sector == "S13"].pivot(index="time", columns="cofog99", values="valeur")
c = pd.read_csv(D / "comptes.csv")
P = c.pivot_table(index=["na_item", "time"], columns="sector", values="valeur")
pib = pd.read_csv(D / "pib.csv").set_index("time").valeur
dette = pd.read_csv(D / "dette_insee.csv").pivot(index="time", columns="sous_secteur",
                                                  values="valeur").APU * 1000      # M€
interets = P.loc["D41PAY"]["S13"]

g = f.copy()
g["GF01"] = g["GF01"] - interets.reindex(g.index)
g["GF10X"] = g["GF10"] - g["GF1002"]
g = g[list(LIB)]
g.loc[2025] = g.loc[2024]
part = g.div(g.sum(axis=1), axis=0)

stock_1995 = dette[1995] * part.loc[1995]
nouveau = pd.Series(0.0, index=part.columns)
for an in range(1996, 2026):
    r = interets[an] / dette[an - 1]
    hors_interets = dette[an] - dette[an - 1] - interets[an]
    stock_1995 = stock_1995 * (1 + r)
    nouveau = nouveau * (1 + r) + hors_interets * part.loc[an]
total = stock_1995 + nouveau

res = pd.DataFrame({
    "fonction": [LIB[k] for k in part.columns],
    "dette_Mde": total.values,
    "part_dette": (total / total.sum()).values,
    "dette_depuis_1995_Mde": nouveau.values,
    "part_dette_depuis_1995": (nouveau / nouveau.sum()).values,
    "part_depense_2024": part.loc[2024].values,
}, index=part.columns)
res.to_csv(D / "fonctions_2025.csv", index_label="cofog")

ev = 100 * g.loc[:2024].div(pib.reindex(g.loc[:2024].index), axis=0)
ev["interets"] = 100 * interets.loc[1995:2024] / pib.loc[1995:2024]
ev["recettes"] = 100 * P.loc["TR"]["S13"].loc[1995:2024] / pib.loc[1995:2024]
ev.to_csv(D / "fonctions_evolution.csv", index_label="annee")

if __name__ == "__main__":
    pd.set_option("display.width", 140)
    t = res.sort_values("part_dette", ascending=False).copy()
    t[["dette_Mde", "dette_depuis_1995_Mde"]] /= 1000
    for k in ("part_dette", "part_dette_depuis_1995", "part_depense_2024"):
        t[k] *= 100
    print(t.set_index("fonction").round(1).to_string())
    s = res.loc[SOCIAL]
    print(f"\nSanté et protection sociale : {s.dette_Mde.sum() / 1000:.0f} Md€, "
          f"{100 * s.part_dette.sum():.1f} % de la dette ({100 * s.part_dette_depuis_1995.sum():.1f} % "
          "de la dette créée depuis 1995)")
    d = ev.loc[2024] - ev.loc[1995]
    print("\nVariation 1995-2024, points de PIB :\n", d.round(1).to_string())
