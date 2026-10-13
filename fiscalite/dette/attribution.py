"""
Attribution de la dette publique aux sous-secteurs des administrations publiques (APU).

    python dette/attribution.py

Cadre commun à toutes les méthodes. Chaque année de 1996 à 2025, la dette des APU augmente du
déficit des APU et des ajustements stock-flux (achats d'actifs financiers, primes d'émission…).
Le déficit se décompose en un déficit primaire (avant intérêts) et des intérêts. Les méthodes ne
diffèrent que par la règle qui répartit le déficit primaire ; le reste est traité de la même façon :
  - les intérêts suivent la dette : chaque bloc de dette attribué est capitalisé au taux apparent
    des APU (une dette attribuée à la sécurité sociale porte ses intérêts, même si c'est l'État
    qui les paie) ;
  - les ajustements stock-flux restent à l'émetteur (ils traduisent sa gestion financière : les
    réserves des régimes de retraite complémentaire gonflent la dette brute des ASSO) ;
  - le stock de fin 1995 (702 Md€) et ses intérêts sont répartis selon l'émetteur de 1995, faute
    de données antérieures dans la même base. Capitalisé, ce bloc pèse plus de la moitié de la
    dette de 2025 : les résultats sont donnés pour la dette totale et pour la seule dette créée
    depuis 1995.

Sous-secteurs : ETAT = administration centrale (État et ODAC, S1311) ; APUL (S1313) ; ASSO (S1314).

Règles de répartition du déficit primaire
  M0  émetteur      chaque sous-secteur garde son propre déficit primaire.
  M1  dépense       déficit primaire des APU au prorata de la dépense primaire finale de chaque
      finale        sous-secteur (dépense hors intérêts et hors transferts versés aux autres APU).
  M2  transferts    chaque sous-secteur finance tous ses emplois (dépense finale et transferts
      explicites    aux autres APU) avec la même proportion d'emprunt ; la part de son déficit qui
                    finance des transferts courants (D7) ou en capital (D9) suit l'argent jusqu'à
                    celui qui le dépense.
  M3  TVA affectée  M2, en traitant la TVA perçue par la sécurité sociale et par les collectivités
                    comme un transfert de l'État et non comme une ressource propre.
  M3+ impôts        M3, en traitant aussi comme transferts de l'État tous les autres impôts sur la
      affectés      production perçus par la sécurité sociale (taxe sur les salaires, droits sur
                    les tabacs et alcools…). La CSG reste une ressource propre des ASSO.
  M4  fonction      déficit primaire des APU au prorata de la dépense primaire par fonction
                    (COFOG) : santé (GF07) et protection sociale (GF10) d'un côté, le reste de
                    l'autre, quel que soit le sous-secteur qui dépense.

Sorties dans dette/donnees/ :
  attribution_annuelle.csv  dette attribuée par bloc (héritée, ajustements, nouvelle) et part,
                            par méthode, sous-secteur et année
  attribution_deficits.csv  déficits primaires attribués, par méthode, sous-secteur et année
  attribution_2025.csv      parts de la dette totale et de la dette nouvelle fin 2025, par méthode
"""
from pathlib import Path

import numpy as np
import pandas as pd

D = Path(__file__).resolve().parent / "donnees"
SS = ["S1311", "S1313", "S1314"]
NOM = {"S1311": "ETAT", "S1313": "APUL", "S1314": "ASSO"}
AN0, AN1 = 1995, 2025
METHODES = ["M0", "M1", "M2", "M3", "M3+", "M4"]

c = pd.read_csv(D / "comptes.csv")
P = c.pivot_table(index=["na_item", "time"], columns="sector", values="valeur").fillna(0)
imp = pd.read_csv(D / "impots.csv").pivot_table(index=["na_item", "time"], columns="sector",
                                                values="valeur")
cof = pd.read_csv(D / "cofog.csv")
cof = cof[cof.sector == "S13"].pivot(index="time", columns="cofog99", values="valeur")
dette = pd.read_csv(D / "dette_insee.csv").pivot(index="time", columns="sous_secteur",
                                                  values="valeur") * 1000      # M€
dette["ETAT"] = dette.Etat + dette.ODAC


def v(item, an, s):
    return P.loc[(item, an), s]


def impot(item, an, s):
    """Impôt reçu ; la dernière année publiée (2024) sert pour 2025."""
    return imp.loc[(item, min(an, 2024)), s]


def deficit_primaire(an):
    return pd.Series({s: -v("B9", an, s) - v("D41PAY", an, s) for s in SS})


def transferts(an, affectes=()):
    """Matrice T[i, j] des transferts versés par i à j (D7 et D9), plus les impôts affectés que
    la méthode traite comme versés par l'État, en M€."""
    T = pd.DataFrame(0.0, index=SS, columns=SS)
    for i in SS:
        for j in SS:
            if i != j:
                T.loc[i, j] = v(f"D7PAY_{j}", an, i) + v(f"D9PAY_{j}", an, i)
    for j, montant in affectes:
        T.loc["S1311", j] += montant
    return T


def affectes(an, methode):
    if methode == "M3":
        return [("S1314", impot("D211", an, "S1314")), ("S1313", impot("D211", an, "S1313"))]
    if methode == "M3+":
        return [("S1314", impot("D2", an, "S1314")), ("S1313", impot("D211", an, "S1313"))]
    return []


def repartit(an, methode):
    """Déficit primaire de l'année réparti selon la méthode, en M€."""
    dp = deficit_primaire(an)
    if methode == "M0":
        return dp.rename(NOM)
    if methode == "M1":
        T = transferts(an)
        fe = pd.Series({s: v("TE", an, s) - v("D41PAY", an, s) for s in SS}) - T.sum(axis=1)
        return (dp.sum() * fe / fe.sum()).rename(NOM)
    if methode == "M4":
        f = cof.loc[min(an, cof.index.max())]
        prim = f["TOTAL"] - v("D41PAY", min(an, cof.index.max()), "S13")
        sh = (f["GF07"] + f["GF10"]) / prim
        return pd.Series({"SOCIAL": dp.sum() * sh, "AUTRES": dp.sum() * (1 - sh)})
    # M2, M3, M3+ : l'emprunt suit les transferts
    aff = affectes(an, methode)
    T = transferts(an, aff)
    dep = pd.Series({s: v("TE", an, s) - v("D41PAY", an, s) for s in SS})
    d = dp.copy()
    for j, m in aff:          # l'État perçoit l'impôt (son déficit baisse) puis le reverse
        d["S1311"] -= m
        d[j] += m
        dep["S1311"] += m
    t = T.div(dep, axis=0)                        # part de chaque transfert dans les emplois
    s = 1 - t.sum(axis=1)                         # part de la dépense finale
    # e_j = d_j + somme_i e_i t_ij : emprunt dont dispose j, le sien et celui reçu par transferts ;
    # il en garde la part s_j qui finance sa dépense finale.
    e = np.linalg.solve((np.eye(3) - t.values).T, d.values)
    return pd.Series(e * s.values, index=SS).rename(NOM)


def sfa_emetteur(an):
    """Ajustement stock-flux de chaque émetteur : variation de sa dette moins son déficit."""
    a = {NOM[s]: (dette.loc[an, NOM[s]] - dette.loc[an - 1, NOM[s]]) + v("B9", an, s) for s in SS}
    # écart résiduel (intérêts versés entre sous-secteurs, arrondis) : à l'État
    total = dette.loc[an, "APU"] - dette.loc[an - 1, "APU"] + v("B9", an, "S13")
    a["ETAT"] += total - sum(a.values())
    return pd.Series(a)


def taux(an):
    """Taux apparent des APU : intérêts de l'année rapportés à la dette de fin d'année précédente."""
    interets = -v("B9", an, "S13") - deficit_primaire(an).sum()
    return interets / dette.loc[an - 1, "APU"]


# Trois blocs de dette, capitalisés chaque année au taux apparent des APU :
#   HERITE  stock de fin 1995 et intérêts sur ce stock, réparti selon l'émetteur de 1995 ;
#   SFA     ajustements stock-flux et leurs intérêts, réparti selon l'émetteur ;
#   NOUVEAU déficits primaires 1996-2025 et leurs intérêts, réparti selon la méthode.
herite0 = dette.loc[AN0, ["ETAT", "APUL", "ASSO"]]
res, defs = [], []
for m in METHODES:
    h, f, n = herite0.copy(), pd.Series(0.0, index=herite0.index), None
    for an in range(AN0 + 1, AN1 + 1):
        r = taux(an)
        dp = repartit(an, m)
        n = dp if n is None else n * (1 + r) + dp
        h = h * (1 + r)
        f = f * (1 + r) + sfa_emetteur(an)
        for k in dp.index:
            defs.append({"annee": an, "methode": m, "sous_secteur": k, "deficit_primaire": dp[k]})
        if m == "M4":   # fonctions : héritage et ajustements des ASSO au social, le reste aux autres
            hh = pd.Series({"SOCIAL": h["ASSO"], "AUTRES": h["ETAT"] + h["APUL"]})
            ff = pd.Series({"SOCIAL": f["ASSO"], "AUTRES": f["ETAT"] + f["APUL"]})
        else:
            hh, ff = h, f
        for k in n.index:
            res.append({"annee": an, "methode": m, "sous_secteur": k, "herite": hh[k], "sfa": ff[k],
                        "nouveau": n[k], "dette": hh[k] + ff[k] + n[k]})
R = pd.DataFrame(res)
R["part"] = R.dette / R.annee.map(dette.APU)
R["part_nouveau"] = R.nouveau / R.groupby(["annee", "methode"]).nouveau.transform("sum")
A = pd.DataFrame(defs)
R.to_csv(D / "attribution_annuelle.csv", index=False)
A.to_csv(D / "attribution_deficits.csv", index=False)
fin = R[R.annee == AN1].pivot(index="methode", columns="sous_secteur", values="part")
fin_nouveau = R[R.annee == AN1].pivot(index="methode", columns="sous_secteur", values="part_nouveau")
pd.concat({"dette_totale": fin, "dette_nouvelle": fin_nouveau}).to_csv(D / "attribution_2025.csv")

# Tableau LaTeX de la note (dette/note-dette.tex) : parts de la sécurité sociale, des collectivités
# et de l'État, dans la dette totale et dans la dette créée depuis 1995.
LIBELLES = {"M0": "Émetteur", "M2": "Transferts explicites suivis jusqu'au dépensier",
            "M3": "Idem, TVA affectée traitée comme un transfert de l'État",
            "M3+": "Idem, tous impôts indirects affectés à la sécurité sociale",
            "M1": "Prorata de la dépense primaire finale",
            "M4": "Prorata de la dépense par fonction (santé et protection sociale)"}


def _f(x):
    return f"{100 * x:.0f}".replace("-", "$-$")


lignes = []
for m, lib in LIBELLES.items():
    t, n = fin.loc[m], fin_nouveau.loc[m]
    if m == "M4":
        cel = [_f(t["SOCIAL"]), "", _f(t["AUTRES"]), _f(n["SOCIAL"]), "", _f(n["AUTRES"])]
    else:
        cel = [_f(t["ASSO"]), _f(t["APUL"]), _f(t["ETAT"]), _f(n["ASSO"]), _f(n["APUL"]), _f(n["ETAT"])]
    lignes.append(f"{m} & {lib} & " + " & ".join(cel) + r" \\")
(D.parent / "tableau_attribution.tex").write_text("\n".join(lignes) + "\n\\bottomrule\n",
                                                      encoding="utf-8")

if __name__ == "__main__":
    pd.set_option("display.width", 120)
    tot = R[(R.annee == AN1) & (R.methode == "M0")][["herite", "sfa", "nouveau", "dette"]].sum()
    print(f"Dette fin 2025 : {tot.dette / 1000:.0f} Md€ (publiée {dette.loc[AN1, 'APU'] / 1000:.0f}),"
          f" dont héritée de 1995 et ses intérêts {tot.herite / 1000:.0f}, ajustements stock-flux "
          f"{tot.sfa / 1000:.0f}, déficits primaires 1996-2025 et leurs intérêts {tot.nouveau / 1000:.0f}")
    pub = dette.loc[AN1, ["ETAT", "APUL", "ASSO"]] / dette.loc[AN1, "APU"]
    print("Parts publiées (émetteur), % :", (100 * pub).round(1).to_dict())
    cum = A.groupby(["methode", "sous_secteur"]).deficit_primaire.sum().unstack() / 1000
    print("\nDéficits primaires cumulés 1996-2025, Md€\n", cum.round(0).to_string())
    print("\nPart de la dette fin 2025, %\n", (100 * fin).round(1).to_string())
    print("\nPart de la dette nouvelle (déficits primaires 1996-2025 et leurs intérêts), %\n",
          (100 * fin_nouveau).round(1).to_string())
