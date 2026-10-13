"""
Dynamique de la dette depuis 1978 et dérive des prestations sociales depuis 1960, en raccordant les
séries longues de l'Insee (base 2014, jusqu'en 1994) aux données Eurostat (base 2020, depuis 1995).

    python dette/dynamique_longue.py

Raccord : chaque variation annuelle est calculée dans une seule base (base 2014 jusqu'à 1995
inclus, base 2020 ensuite). Le changement de base relève le ratio de dette de 1995 de 56,1 à 57,5 %
du PIB ; cet écart est isolé dans une ligne « changement de base ». En 1995, les prestations
sociales pèsent 22,3 % du PIB en base 2014 et 22,4 % en base 2020, les intérêts 3,49 et 3,46 %.

Prestations sociales = prestations en espèces (D62 : retraites, chômage, famille, minima sociaux)
+ transferts sociaux en nature de produits marchands (D632 : remboursements de soins et de
médicaments, aides au logement). Les soins produits par l'hôpital public n'y sont pas, faute de
série longue par fonction.

Sorties dans dette/donnees/ :
  dynamique_longue.csv   séries annuelles en % du PIB et contributions à la variation de la dette
"""
from pathlib import Path

import pandas as pd

D = Path(__file__).resolve().parent / "donnees"
L = pd.read_csv(D / "insee_long.csv").set_index("annee")
c = pd.read_csv(D / "comptes.csv")
P = c.pivot_table(index=["na_item", "time"], columns="sector", values="valeur")
pib20 = pd.read_csv(D / "pib.csv").set_index("time").valeur
dette20 = pd.read_csv(D / "dette_insee.csv").pivot(index="time", columns="sous_secteur",
                                                    values="valeur").APU * 1000      # M€


def base2014():
    t = pd.DataFrame({
        "pib": L.pib, "dette": L.dette, "interets": L.interets,
        "deficit": -L.deficit, "prestations": L.prest_esp + L.prest_nat})
    return t.loc[:1995]


def base2020():
    s = lambda k: P.loc[k]["S13"]                                           # noqa: E731
    t = pd.DataFrame({
        "pib": pib20, "dette": dette20, "interets": s("D41PAY"), "deficit": -s("B9"),
        "prestations": s("D62PAY") + s("D632PAY")})
    return t.loc[1995:2025] / 1000                                            # Md€


def contributions(t):
    """Décomposition standard de la variation du ratio de dette, dans une base donnée."""
    d = 100 * t.dette / t.pib
    i = t.interets / t.dette.shift(1)
    g = t.pib / t.pib.shift(1) - 1
    out = pd.DataFrame({
        "dette": d,
        "deficit_primaire": 100 * (t.deficit - t.interets) / t.pib,
        "effet_interets": i / (1 + g) * d.shift(1),
        "effet_croissance": -g / (1 + g) * d.shift(1),
        "prestations": 100 * t.prestations / t.pib,
        "interets": 100 * t.interets / t.pib,
    })
    out["stock_flux"] = (d.diff() - out.deficit_primaire - out.effet_interets
                         - out.effet_croissance)
    return out


a, b = contributions(base2014()), contributions(base2020())
longue = pd.concat([a.loc[:1995], b.loc[1996:]])
changement_base = b.dette[1995] - a.dette[1995]
longue.to_csv(D / "dynamique_longue.csv", index_label="annee")

if __name__ == "__main__":
    pd.set_option("display.width", 140)
    for debut, fin in ((1978, 1995), (1995, 2025), (1978, 2025)):
        s = longue.loc[debut + 1:fin]
        cb = changement_base if debut < 1995 < fin else 0
        d0 = b.dette[1995] if debut == 1995 else longue.dette[debut]
        print(f"\n{debut}-{fin} : ratio {d0:.1f} → {longue.dette[fin]:.1f} % du PIB "
              f"(+{longue.dette[fin] - d0:.1f})")
        for k in ("deficit_primaire", "effet_interets", "effet_croissance", "stock_flux"):
            print(f"   {k:18s} {s[k].sum():+6.1f}")
        if cb:
            print(f"   changement de base {cb:+6.1f}")
    print("\nPrestations sociales et solde primaire, % du PIB")
    print(longue.loc[[1960, 1970, 1974, 1978, 1980, 1985, 1990, 1995, 2000, 2007, 2019, 2024, 2025],
                     ["prestations", "deficit_primaire", "interets", "dette"]].round(1).to_string())
