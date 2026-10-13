"""
Attribution de la dette publique aux sous-secteurs des administrations publiques.

    python dette/attribution.py

Toutes les méthodes répartissent le même besoin de financement annuel des APU (−B9), de 1996 à
2025 ; elles ne diffèrent que par la règle qui dit « à qui » revient chaque euro emprunté. La
dette de fin 2025 est ensuite reconstituée comme : stock de fin 1995 (réparti selon l'émetteur,
faute de mieux) + déficits attribués de 1996 à 2025 + écart entre variation de dette et déficit
(ajustements stock-flux), réparti au prorata des déficits attribués de l'année.

Sous-secteurs : ETAT = administration centrale (État et ODAC, S1311) ; APUL (S1313) ; ASSO (S1314).

Méthodes
  M0 émetteur     dette telle qu'enregistrée (Insee), État et ODAC réunis.
  M1 dépense      déficit des APU réparti au prorata de la dépense finale de chaque sous-secteur
                  (dépense totale moins transferts versés aux autres APU) : la règle simple.
  M2 dépensier    chaque sous-secteur finance tous ses emplois, dépense finale et transferts aux
     final        autres APU, avec la même proportion d'emprunt ; la part de son déficit qui a
                  financé des transferts suit l'argent jusqu'au sous-secteur qui le dépense.
  M3 ressources   variante de M2 où les impôts sur la production et les importations perçus par
     propres      la sécurité sociale (TVA affectée, droits sur les tabacs…), votés par l'État,
                  sont traités comme des transferts de l'État et non comme des ressources propres.
  M4 fonction     déficit des APU réparti au prorata de la dépense par fonction (COFOG) :
                  protection sociale et santé d'un côté, le reste de l'autre.

Sorties : dette/donnees/attribution_annuelle.csv, dette/donnees/attribution_2025.csv
"""
from pathlib import Path

import numpy as np
import pandas as pd

D = Path(__file__).resolve().parent / "donnees"
SS = ["S1311", "S1313", "S1314"]
NOM = {"S1311": "ETAT", "S1313": "APUL", "S1314": "ASSO"}
AN0, AN1 = 1995, 2025

c = pd.read_csv(D / "comptes.csv")
P = c.pivot_table(index=["na_item", "time"], columns="sector", values="valeur").fillna(0)
dette = pd.read_csv(D / "dette_insee.csv").pivot(index="time", columns="sous_secteur",
                                                  values="valeur") * 1000      # M€
dette["ETAT"] = dette.Etat + dette.ODAC


def transferts(an, d2_asso=False):
    """Matrice T[i, j] des transferts versés par i à j (courants D7 et en capital D9), M€."""
    T = pd.DataFrame(0.0, index=SS, columns=SS)
    for i in SS:
        for j in SS:
            if i != j:
                T.loc[i, j] = (P.loc[(f"D7PAY_{j}", an), i] + P.loc[(f"D9PAY_{j}", an), i])
    if d2_asso:
        T.loc["S1311", "S1314"] += P.loc[("D2REC", an), "S1314"]
    return T


def attribue(an, methode):
    b9 = P.loc[("B9", an), SS].copy()
    te = P.loc[("TE", an), SS].copy()
    deficit_apu = -P.loc[("B9", an), "S13"]
    if methode == "M1":
        T = transferts(an)
        fe = te - T.sum(axis=1)
        return deficit_apu * fe / fe.sum()
    if methode in ("M2", "M3"):
        T = transferts(an, d2_asso=(methode == "M3"))
        d = -b9
        if methode == "M3":
            # Les impôts affectés passent du compte de la sécurité sociale à celui de l'État :
            # l'État les perçoit (son déficit baisse) puis les verse (sa dépense augmente).
            g = P.loc[("D2REC", an), "S1314"]
            d["S1311"] -= g
            d["S1314"] += g
            te["S1311"] += g
        t = T.div(te, axis=0)                     # part de chaque emploi dans la dépense
        s = 1 - t.sum(axis=1)                     # part de la dépense finale
        # L'argent emprunté circule le long des transferts : e = d + e·t, puis reste chez le
        # dépensier final à hauteur de sa part de dépense finale.
        e = np.linalg.solve((np.eye(3) - t.values).T, d.values)
        return pd.Series(e * s.values, index=SS)
    raise ValueError(methode)


def cofog(an):
    f = pd.read_csv(D / "cofog.csv")
    f = f[(f.sector == "S13") & (f.time == min(an, f.time.max()))].set_index("cofog99").valeur
    return (f["GF07"] + f["GF10"]) / f["TOTAL"]


lignes = []
for an in range(AN0 + 1, AN1 + 1):
    deficit_apu = -P.loc[("B9", an), "S13"]
    for m in ("M1", "M2", "M3"):
        a = attribue(an, m)
        for s in SS:
            lignes.append({"annee": an, "methode": m, "sous_secteur": NOM[s], "deficit": a[s]})
    sh = cofog(an)
    lignes.append({"annee": an, "methode": "M4", "sous_secteur": "SOCIAL", "deficit": deficit_apu * sh})
    lignes.append({"annee": an, "methode": "M4", "sous_secteur": "AUTRES",
                   "deficit": deficit_apu * (1 - sh)})
    for s in SS:
        lignes.append({"annee": an, "methode": "M0", "sous_secteur": NOM[s], "deficit": -P.loc[("B9", an), s]})
A = pd.DataFrame(lignes)

# Reconstitution des stocks : stock 1995 par émetteur + déficits attribués + ajustements
# stock-flux de l'année répartis au prorata de la valeur absolue des déficits attribués.
stock0 = {"ETAT": dette.loc[AN0, "ETAT"], "APUL": dette.loc[AN0, "APUL"], "ASSO": dette.loc[AN0, "ASSO"]}
res = []
for m, g in A.groupby("methode"):
    secteurs = sorted(g.sous_secteur.unique())
    if m == "M4":
        st = {"SOCIAL": stock0["ASSO"], "AUTRES": stock0["ETAT"] + stock0["APUL"]}
    else:
        st = dict(stock0)
    for an in range(AN0 + 1, AN1 + 1):
        ga = g[g.annee == an].set_index("sous_secteur").deficit
        sfa = (dette.loc[an, "APU"] - dette.loc[an - 1, "APU"]) - ga.sum()
        poids = ga.abs() / ga.abs().sum()
        for s in secteurs:
            st[s] += ga[s] + sfa * poids[s]
        for s in secteurs:
            res.append({"annee": an, "methode": m, "sous_secteur": s, "dette": st[s],
                        "part": st[s] / dette.loc[an, "APU"]})
R = pd.DataFrame(res)
# M0 : la dette publiée, pour contrôle
for an in range(AN0, AN1 + 1):
    for s in ("ETAT", "APUL", "ASSO"):
        R = pd.concat([R, pd.DataFrame([{"annee": an, "methode": "M0pub", "sous_secteur": s,
                                         "dette": dette.loc[an, s],
                                         "part": dette.loc[an, s] / dette.loc[an, "APU"]}])])
R.to_csv(D / "attribution_annuelle.csv", index=False)
fin = R[R.annee == AN1].pivot(index="methode", columns="sous_secteur", values="part")
fin.to_csv(D / "attribution_2025.csv")
cum = A.groupby(["methode", "sous_secteur"]).deficit.sum().unstack() / 1000
print("Déficits cumulés 1996-2025, Md€\n", cum.round(0))
print("\nPart de la dette fin 2025\n", (100 * fin).round(1))
