"""
Décomposition standard de la dynamique de la dette (méthode du FMI et de la Commission européenne),
puis ventilation par fonction de la contribution des déficits primaires.

    python dette/dynamique.py

1. Dynamique de la dette en points de PIB. Avec d le ratio dette/PIB, pd le déficit primaire en %
   du PIB, i le taux apparent (intérêts / dette de l'année précédente) et g la croissance du PIB
   nominal :
       d_t - d_{t-1} = pd_t + (i_t - g_t)/(1 + g_t) * d_{t-1} + ajustement stock-flux_t
   Le deuxième terme (« effet boule de neige ») se sépare en un effet des intérêts,
   i_t/(1+g_t)*d_{t-1}, et un effet de la croissance, -g_t/(1+g_t)*d_{t-1}.
2. Ventilation du déficit primaire par fonction (COFOG), de deux façons :
   - au prorata : chaque année, le déficit primaire est réparti selon la part de chaque fonction
     dans la dépense primaire (convention des dépenses fongibles) ;
   - par dérive (Auerbach, 1994 ; OBR) : le déficit primaire de l'année t est égal à celui d'une
     année de référence, plus la hausse de chaque dépense par rapport à cette année, moins la
     hausse des recettes. La ventilation dépend de l'année de référence : on en donne trois.

Sorties dans dette/donnees/ :
  dynamique.csv          contributions annuelles (points de PIB) et ratio de dette, 1995-2025
  dynamique_fonctions.csv  ventilation des déficits primaires cumulés 1996-2025 par fonction
  ../tableau_dynamique.tex tableau de la note
"""
from pathlib import Path

import pandas as pd

D = Path(__file__).resolve().parent / "donnees"
AN0, AN1 = 1995, 2025
ANS = list(range(AN0 + 1, AN1 + 1))
FONCTIONS = ["GF01", "GF02", "GF03", "GF04", "GF05", "GF06", "GF07", "GF08", "GF09", "GF1002", "GF10X"]
SOCIAL = ["GF07", "GF1002", "GF10X"]
REFERENCES = (1995, 1997, 2000)

c = pd.read_csv(D / "comptes.csv")
P = c.pivot_table(index=["na_item", "time"], columns="sector", values="valeur")
pib = pd.read_csv(D / "pib.csv").set_index("time").valeur
dette = pd.read_csv(D / "dette_insee.csv").pivot(index="time", columns="sous_secteur",
                                                  values="valeur").APU * 1000      # M€
TE, TR, B9, I = (P.loc[k]["S13"] for k in ("TE", "TR", "B9", "D41PAY"))

# ---------------------------------------------------------------- 1. dynamique standard
d = 100 * dette / pib
i = I / dette.shift(1)
g = pib / pib.shift(1) - 1
dyn = pd.DataFrame({
    "dette": d,
    "deficit_primaire": 100 * (-B9 - I) / pib,
    "effet_interets": i / (1 + g) * d.shift(1),
    "effet_croissance": -g / (1 + g) * d.shift(1),
}).loc[AN0:AN1]
dyn["stock_flux"] = (dyn.dette.diff() - dyn.deficit_primaire - dyn.effet_interets
                     - dyn.effet_croissance)
dyn.to_csv(D / "dynamique.csv", index_label="annee")

# ---------------------------------------------------------------- 2. ventilation par fonction
f = pd.read_csv(D / "cofog.csv")
f = f[f.sector == "S13"].pivot(index="time", columns="cofog99", values="valeur")
f["GF01"] = f["GF01"] - I.reindex(f.index)           # intérêts retirés des services généraux
f["GF10X"] = f["GF10"] - f["GF1002"]
part = f[FONCTIONS].div(f[FONCTIONS].sum(axis=1), axis=0)
part.loc[2025] = part.loc[2024]                      # 2025 : structure de 2024
# dépense primaire par fonction en % du PIB, cohérente avec le déficit primaire publié
X = part.loc[AN0:AN1].mul(100 * (TE - I).loc[AN0:AN1] / pib.loc[AN0:AN1], axis=0)
tau = 100 * TR.loc[AN0:AN1] / pib.loc[AN0:AN1]
pd_ = X.sum(axis=1) - tau

lignes = {"prorata": part.loc[ANS].mul(pd_.loc[ANS], axis=0).sum()}
for ref in REFERENCES:
    derive = (X.loc[ANS] - X.loc[ref]).sum()
    derive["recettes"] = -(tau.loc[ANS] - tau[ref]).sum()
    derive["deficit_de_reference"] = len(ANS) * pd_[ref]
    lignes[f"derive_{ref}"] = derive
vent = pd.DataFrame(lignes)
vent.to_csv(D / "dynamique_fonctions.csv", index_label="poste")

# Tableau LaTeX de la note : déficits primaires cumulés 1996-2025, en points de PIB
AUTRES = [k for k in FONCTIONS if k not in SOCIAL]
blocs = [("Vieillesse", ["GF1002"]), ("Santé", ["GF07"]), ("Autre protection sociale", ["GF10X"]),
         ("Autres fonctions", AUTRES), ("Recettes (hausse : signe moins)", ["recettes"]),
         ("Déficit primaire de l'année de référence", ["deficit_de_reference"])]


def _n(x):
    return "" if pd.isna(x) else f"{x:+.0f}".replace("-", "$-$")


lignes_tex = []
for lib, cles in blocs:
    vals = [vent.loc[vent.index.intersection(cles), col].sum(min_count=1) for col in vent.columns]
    lignes_tex.append(lib + " & " + " & ".join(_n(v) for v in vals) + r" \\")
tot = [vent[col].sum() for col in vent.columns]
lignes_tex.append(r"\midrule")
lignes_tex.append("Total : déficits primaires cumulés & " + " & ".join(_n(v) for v in tot) + r" \\")
(D.parent / "tableau_dynamique.tex").write_text("\n".join(lignes_tex) + "\n\\bottomrule\n",
                                                encoding="utf-8")

if __name__ == "__main__":
    s = dyn.loc[ANS].sum()
    print(f"Ratio de dette : {d[AN0]:.1f} % du PIB en {AN0}, {d[AN1]:.1f} % en {AN1} "
          f"(+{d[AN1] - d[AN0]:.1f} points)")
    print(f"  déficits primaires cumulés      {s.deficit_primaire:+.1f}")
    print(f"  effet des intérêts              {s.effet_interets:+.1f}")
    print(f"  effet de la croissance du PIB   {s.effet_croissance:+.1f}")
    print(f"  ajustements stock-flux          {s.stock_flux:+.1f}")
    print("\nVentilation des déficits primaires cumulés 1996-2025 (points de PIB)")
    print(vent.round(1).to_string())
    print(f"\nPart sociale au prorata : {vent.prorata[SOCIAL].sum():.1f} points sur "
          f"{vent.prorata.sum():.1f}")
