"""
À quoi a servi la dette publique ? Programme unique : données, calculs, tableau et figures de la
note dette/note-dette.tex.

    python dette/dette.py                 calculs, résumé des résultats, figures (PNG avec titre)
    FIG_NU=1 python dette/dette.py        mêmes figures sans titre, pour la note (figures/nu/)
    python dette/dette.py --telecharger   télécharge d'abord les données (Eurostat, Insee)

Étapes
  1. Données (dette/donnees/) : comptes des administrations publiques (APU) par sous-secteur,
     impôts reçus, dépense par fonction (COFOG), PIB, dette par sous-secteur (Eurostat et Insee,
     base 2020, 1995-2025) ; séries longues de l'Insee en base 2014 (1949-1995).
  2. Dynamique de la dette (méthode du FMI et de la Commission européenne), 1978-2025.
  3. Première convention : dépenses fongibles, dette répartie par fonction au prorata de la dépense.
  4. Seconde convention : dérive de chaque dépense par rapport à une année de référence.
  5. Règles de répartition entre administrations (État, collectivités, sécurité sociale) : tableau.
  6. Figures dette_*.

Sous-secteurs : S13 APU ; S1311 administration centrale (État et ODAC, qu'Eurostat ne sépare pas) ;
S1313 administrations publiques locales (APUL) ; S1314 administrations de sécurité sociale (ASSO).
Montants en millions d'euros sauf mention contraire.
"""
import csv
import json
import re
import sys
import urllib.request
from pathlib import Path

import numpy as np
import pandas as pd

ICI = Path(__file__).resolve().parent
D = ICI / "donnees"
D.mkdir(exist_ok=True)
SECTEURS = ["S13", "S1311", "S1313", "S1314"]
SS = ["S1311", "S1313", "S1314"]
NOM = {"S1311": "ETAT", "S1313": "APUL", "S1314": "ASSO"}
AN0, AN1 = 1995, 2025
ANS = list(range(AN0 + 1, AN1 + 1))


# ================================================================ 1. téléchargement
def jsonstat(dataset, **filtres):
    """Télécharge un jeu Eurostat et le renvoie en lignes {dimension: code, ..., valeur}."""
    api = "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/"
    q = "&".join(f"{k}={v}" for k, vs in filtres.items()
                 for v in (vs if isinstance(vs, list) else [vs]))
    with urllib.request.urlopen(f"{api}{dataset}?{q}", timeout=300) as r:
        d = json.load(r)
    dims, tailles = d["id"], d["size"]
    codes = []
    for dim in dims:
        idx = d["dimension"][dim]["category"]["index"]
        codes.append(sorted(idx, key=idx.get))
    lignes = []
    for cle, val in d["value"].items():
        k, pos = int(cle), []
        for t in reversed(tailles):
            pos.append(k % t)
            k //= t
        pos.reverse()
        lignes.append({**{dim: codes[i][p] for i, (dim, p) in enumerate(zip(dims, pos))},
                       "valeur": val})
    return lignes


def bdm(series, flux=None):
    """Télécharge des séries de la banque de données macroéconomiques de l'Insee, par idbank, ou
    tout un flux dont on garde ces séries : {idbank: (attributs, [(période, valeur)])}."""
    url = "https://bdm.insee.fr/series/sdmx/data/" + (flux or "SERIES_BDM/" + "+".join(series))
    with urllib.request.urlopen(url, timeout=300) as r:
        t = r.read().decode("utf-8")
    out = {}
    for attrs, corps in re.findall(r"<Series ([^>]*)>(.*?)</Series>", t, re.S):
        idb = re.search(r'IDBANK="(\d+)"', attrs).group(1)
        obs = [(p, float(v)) for p, v in re.findall(r'TIME_PERIOD="([^"]+)" OBS_VALUE="([^"]*)"', corps)
               if v not in ("", "NaN")]
        if idb in series:
            out[idb] = (attrs, obs)
    return out


def ecrire(nom, lignes, cols):
    with open(D / nom, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        w.writerows(lignes)
    print(f"  {nom} : {len(lignes)} lignes")


def telecharger():
    items = ["TE", "TR", "B9", "D41PAY", "D62PAY", "D632PAY", "D2REC"]
    for s in SS:
        items += [f"D7PAY_{s}", f"D9PAY_{s}"]
    ecrire("comptes.csv", jsonstat("gov_10a_main", geo="FR", unit="MIO_EUR", sector=SECTEURS,
                                   na_item=items), ["sector", "na_item", "time", "valeur"])
    ecrire("cofog.csv", jsonstat("gov_10a_exp", geo="FR", unit="MIO_EUR", sector="S13", na_item="TE",
                                 cofog99=[f"GF{n:02d}" for n in range(1, 11)] + ["GF1002", "TOTAL"]),
           ["sector", "cofog99", "time", "valeur"])
    ecrire("impots.csv", jsonstat("gov_10a_taxag", geo="FR", unit="MIO_EUR", sector=SECTEURS,
                                  na_item=["D2", "D211"]), ["sector", "na_item", "time", "valeur"])
    ecrire("pib.csv", jsonstat("nama_10_gdp", geo="FR", unit="CP_MEUR", na_item="B1GQ"),
           ["time", "valeur"])
    try:
        telecharger_insee()
    except OSError as e:           # la banque de données de l'Insee est parfois indisponible
        print(f"  Insee indisponible ({e}) : fichiers Insee existants conservés")


def telecharger_insee():
    # Insee, dette de Maastricht par sous-secteur (contributions consolidées, Md€), fin d'année
    noms = {"010777610": "Etat", "010777613": "ODAC", "010777626": "APUL", "010777625": "ASSO",
            "010777616": "APU"}
    lignes = [{"sous_secteur": noms[i], "time": p[:4], "valeur": v}
              for i, (_, obs) in bdm(noms, "DETTE-TRIM-APU-2020").items() for p, v in obs
              if p.endswith("Q4")]
    ecrire("dette_insee.csv", lignes, ["sous_secteur", "time", "valeur"])
    # Insee, comptes nationaux annuels base 2014 (séries arrêtées), en Md€ : dette (1978-2022),
    # déficit (1949-2022), intérêts versés D41, prestations en espèces D62 et en nature de produits
    # marchands D632 (1949-2021), PIB (1949-2022)
    noms = {"010562165": "dette", "010562130": "deficit", "010563497": "interets",
            "010563674": "prest_esp", "010563707": "prest_nat", "010548500": "pib"}
    valeurs = {}
    for i, (attrs, obs) in bdm(noms).items():
        mult = 10 ** (int(re.search(r'UNIT_MULT="(\d+)"', attrs).group(1)) - 9)
        for p, v in obs:
            valeurs.setdefault(int(p), {"annee": int(p)})[noms[i]] = v * mult
    ecrire("insee_long.csv", [valeurs[a] for a in sorted(valeurs)], ["annee"] + list(noms.values()))


if "--telecharger" in sys.argv:
    telecharger()

# ================================================================ lecture
P = pd.read_csv(D / "comptes.csv").pivot_table(index=["na_item", "time"], columns="sector",
                                                 values="valeur").fillna(0)
IMP = pd.read_csv(D / "impots.csv").pivot_table(index=["na_item", "time"], columns="sector",
                                                  values="valeur")
COF = pd.read_csv(D / "cofog.csv")
COF = COF[COF.sector == "S13"].pivot(index="time", columns="cofog99", values="valeur")
PIB = pd.read_csv(D / "pib.csv").set_index("time").valeur
DETTE = pd.read_csv(D / "dette_insee.csv").pivot(index="time", columns="sous_secteur",
                                                   values="valeur") * 1000
DETTE["ETAT"] = DETTE.Etat + DETTE.ODAC
LONG = pd.read_csv(D / "insee_long.csv").set_index("annee")
TE, TR, B9, INT = (P.loc[k]["S13"] for k in ("TE", "TR", "B9", "D41PAY"))


def v(item, an, s):
    return P.loc[(item, an), s]


# ================================================================ 2. dynamique de la dette
def contributions(t):
    """d_t - d_{t-1} = pd_t + i_t/(1+g_t) d_{t-1} - g_t/(1+g_t) d_{t-1} + stock-flux_t, en points
    de PIB ; i = intérêts / dette de l'année précédente, g = croissance du PIB nominal."""
    d = 100 * t.dette / t.pib
    i = t.interets / t.dette.shift(1)
    g = t.pib / t.pib.shift(1) - 1
    out = pd.DataFrame({
        "dette": d,
        "deficit_primaire": 100 * (t.deficit - t.interets) / t.pib,
        "effet_interets": i / (1 + g) * d.shift(1),
        "effet_croissance": -g / (1 + g) * d.shift(1),
        "prestations": 100 * t.prestations / t.pib,
    })
    out["stock_flux"] = d.diff() - out.deficit_primaire - out.effet_interets - out.effet_croissance
    return out


# Base 2014 (Insee) jusqu'en 1995 inclus, base 2020 (Eurostat, Insee) ensuite. Chaque variation est
# calculée dans une seule base ; le changement de base relève la dette de 1995 de 1,4 point.
B14 = contributions(pd.DataFrame({"pib": LONG.pib, "dette": LONG.dette, "interets": LONG.interets,
                                  "deficit": -LONG.deficit,
                                  "prestations": LONG.prest_esp + LONG.prest_nat}).loc[:AN0])
B20 = contributions(pd.DataFrame({"pib": PIB, "dette": DETTE.APU, "interets": INT, "deficit": -B9,
                                  "prestations": P.loc["D62PAY"]["S13"] + P.loc["D632PAY"]["S13"]}
                                 ).loc[AN0:AN1] / 1)
DYN = pd.concat([B14.loc[:AN0], B20.loc[AN0 + 1:]])
CHANGEMENT_BASE = B20.dette[AN0] - B14.dette[AN0]
DYN.to_csv(D / "dynamique_longue.csv", index_label="annee")

# ================================================================ 3. par fonction, dépenses fongibles
FONCTIONS = {"GF03": "Ordre et sécurité (police, justice)", "GF02": "Défense",
             "GF01": "Services généraux (hors intérêts)", "GF04": "Affaires économiques",
             "GF05": "Environnement", "GF06": "Logement et équipements collectifs",
             "GF08": "Culture et sport", "GF09": "Enseignement", "GF07": "Santé",
             "GF1002": "Vieillesse", "GF10X": "Autre protection sociale"}
SOCIAL = ["GF07", "GF1002", "GF10X"]
g = COF.copy()
g["GF01"] = g["GF01"] - INT.reindex(g.index)        # COFOG range les intérêts en services généraux
g["GF10X"] = g["GF10"] - g["GF1002"]
g = g[list(FONCTIONS)]
g.loc[AN1] = g.loc[2024]                            # 2025 : structure de 2024, pas encore publiée
PART = g.div(g.sum(axis=1), axis=0)                 # part de chaque fonction dans la dépense primaire

# Chaque année, la hausse de la dette hors intérêts est répartie au prorata de la dépense ; chaque
# fonction porte les intérêts de sa dette au taux apparent ; le stock de 1995 suit la dépense de 1995.
dapu = DETTE.APU
stock_1995 = dapu[AN0] * PART.loc[AN0]
nouveau = pd.Series(0.0, index=PART.columns)
for an in ANS:
    r = INT[an] / dapu[an - 1]
    stock_1995 = stock_1995 * (1 + r)
    nouveau = nouveau * (1 + r) + (dapu[an] - dapu[an - 1] - INT[an]) * PART.loc[an]
total = stock_1995 + nouveau
FONC = pd.DataFrame({"fonction": [FONCTIONS[k] for k in PART.columns], "dette_Mde": total.values,
                     "part_dette": (total / total.sum()).values,
                     "part_dette_depuis_1995": (nouveau / nouveau.sum()).values,
                     "part_depense_2024": PART.loc[2024].values}, index=PART.columns)
FONC.to_csv(D / "fonctions_2025.csv", index_label="cofog")

# dépense primaire par fonction et recettes, en % du PIB (cohérentes avec le déficit publié)
X = PART.loc[AN0:AN1].mul(100 * (TE - INT).loc[AN0:AN1] / PIB.loc[AN0:AN1], axis=0)
TAU = 100 * TR.loc[AN0:AN1] / PIB.loc[AN0:AN1]
PD = X.sum(axis=1) - TAU
PRORATA = PART.loc[ANS].mul(PD.loc[ANS], axis=0).sum()   # déficits primaires cumulés, au prorata


# ================================================================ 4. dérive (Auerbach)
def derive(ref):
    """pd_t = pd_ref + somme_j (x_jt - x_jref) - (tau_t - tau_ref), cumulé sur 1996-2025."""
    s = (X.loc[ANS] - X.loc[ref]).sum()
    s["recettes"] = -(TAU.loc[ANS] - TAU[ref]).sum()
    s["deficit_de_reference"] = len(ANS) * PD[ref]
    return s


DERIVES = {ref: derive(ref) for ref in (1995, 1997, 2000)}

# ================================================================ 5. règles par administration
IMPOTS_2024 = 2024                                   # dernière année publiée des impôts reçus
METHODES = {"M0": "Émetteur", "M2": "Transferts explicites suivis jusqu'au dépensier",
            "M3": "Idem, TVA affectée traitée comme un transfert de l'État",
            "M3+": "Idem, tous impôts indirects affectés à la sécurité sociale",
            "M1": "Prorata de la dépense primaire finale",
            "M4": "Prorata de la dépense par fonction (santé et protection sociale)"}
FONGIBLES = ("M1", "M4")


def deficit_primaire(an):
    return pd.Series({s: -v("B9", an, s) - v("D41PAY", an, s) for s in SS})


def transferts(an, affectes=()):
    """T[i, j] : transferts courants (D7) et en capital (D9) versés par i à j, plus les impôts
    affectés que la règle traite comme versés par l'État."""
    T = pd.DataFrame(0.0, index=SS, columns=SS)
    for i in SS:
        for j in SS:
            if i != j:
                T.loc[i, j] = v(f"D7PAY_{j}", an, i) + v(f"D9PAY_{j}", an, i)
    for j, montant in affectes:
        T.loc["S1311", j] += montant
    return T


def affectes(an, m):
    impot = lambda item, s: IMP.loc[(item, min(an, IMPOTS_2024)), s]     # noqa: E731
    if m == "M3":
        return [("S1314", impot("D211", "S1314")), ("S1313", impot("D211", "S1313"))]
    if m == "M3+":
        return [("S1314", impot("D2", "S1314")), ("S1313", impot("D211", "S1313"))]
    return []


def parts_fongibles(an, m):
    """Parts de la dépense primaire : finale par sous-secteur (M1) ou sociale par fonction (M4)."""
    if m == "M1":
        fe = (pd.Series({s: v("TE", an, s) - v("D41PAY", an, s) for s in SS})
              - transferts(an).sum(axis=1))
        return (fe / fe.sum()).rename(NOM)
    sh = PART.loc[an, SOCIAL].sum()
    return pd.Series({"SOCIAL": sh, "AUTRES": 1 - sh})


def repartit(an, m):
    """Déficit primaire de l'année réparti selon la règle m."""
    dp = deficit_primaire(an)
    if m == "M0":
        return dp.rename(NOM)
    if m in FONGIBLES:
        return dp.sum() * parts_fongibles(an, m)
    # M2, M3, M3+ : chaque sous-secteur finance tous ses emplois avec la même proportion d'emprunt ;
    # l'emprunt dont dispose j vérifie e_j = d_j + somme_i e_i t_ij, et j en garde la part s_j qui
    # finance sa propre dépense.
    aff = affectes(an, m)
    T = transferts(an, aff)
    dep = pd.Series({s: v("TE", an, s) - v("D41PAY", an, s) for s in SS})
    d = dp.copy()
    for j, montant in aff:              # l'État perçoit l'impôt (son déficit baisse) puis le reverse
        d["S1311"] -= montant
        d[j] += montant
        dep["S1311"] += montant
    t = T.div(dep, axis=0)
    s = 1 - t.sum(axis=1)
    e = np.linalg.solve((np.eye(3) - t.values).T, d.values)
    return pd.Series(e * s.values, index=SS).rename(NOM)


def sfa_emetteur(an):
    """Ajustement stock-flux de chaque émetteur ; le résidu (intérêts entre sous-secteurs) à l'État."""
    a = {NOM[s]: DETTE.loc[an, NOM[s]] - DETTE.loc[an - 1, NOM[s]] + v("B9", an, s) for s in SS}
    a["ETAT"] += DETTE.loc[an, "APU"] - DETTE.loc[an - 1, "APU"] + v("B9", an, "S13") - sum(a.values())
    return pd.Series(a)


# Le stock de 1995 et les ajustements stock-flux suivent la logique de chaque règle : répartis comme
# la dépense pour les règles fongibles, laissés à l'émetteur pour les autres. Tout est capitalisé au
# taux apparent des APU.
lignes = []
for m in METHODES:
    h = (dapu[AN0] * parts_fongibles(AN0, m) if m in FONGIBLES
         else DETTE.loc[AN0, ["ETAT", "APUL", "ASSO"]].copy())
    f, n = pd.Series(0.0, index=h.index), pd.Series(0.0, index=h.index)
    for an in ANS:
        # taux apparent cohérent avec les déficits primaires des sous-secteurs (la différence avec
        # INT tient aux intérêts versés entre sous-secteurs)
        r = (-v("B9", an, "S13") - deficit_primaire(an).sum()) / dapu[an - 1]
        sfa = (dapu[an] - dapu[an - 1] + v("B9", an, "S13")) * parts_fongibles(an, m) \
            if m in FONGIBLES else sfa_emetteur(an)
        h, f, n = h * (1 + r), f * (1 + r) + sfa, n * (1 + r) + repartit(an, m)
    lignes.append({"methode": m, **{f"total_{k}": (h + f + n)[k] / dapu[AN1] for k in h.index},
                   **{f"nouveau_{k}": n[k] / n.sum() for k in h.index}})
REGLES = pd.DataFrame(lignes).set_index("methode")
REGLES.to_csv(D / "attribution_2025.csv")


def _pct(x):
    return f"{100 * x:.0f}".replace("-", "$-$")


tex = []
for m, lib in METHODES.items():
    r = REGLES.loc[m]
    if m == "M4":
        cel = [_pct(r.total_SOCIAL), "", _pct(r.total_AUTRES), _pct(r.nouveau_SOCIAL), "",
               _pct(r.nouveau_AUTRES)]
    else:
        cel = [_pct(r[f"{b}_{k}"]) for b in ("total", "nouveau") for k in ("ASSO", "APUL", "ETAT")]
    tex.append(f"{m} & {lib} & " + " & ".join(cel) + r" \\")
(ICI / "tableau_attribution.tex").write_text("\n".join(tex) + "\n\\bottomrule\n", encoding="utf-8")

# ================================================================ résumé
if __name__ == "__main__":
    pd.set_option("display.width", 140)
    print(f"Dette fin {AN1} : {dapu[AN1] / 1000:.0f} Md€, {B20.dette[AN1]:.1f} % du PIB")
    for debut, fin_ in ((1978, AN0), (AN0, AN1)):
        s = DYN.loc[debut + 1:fin_]
        d0 = B20.dette[AN0] if debut == AN0 else DYN.dette[debut]
        print(f"\nDynamique {debut}-{fin_} : {d0:.1f} → {DYN.dette[fin_]:.1f} % du PIB")
        for k in ("deficit_primaire", "effet_interets", "effet_croissance", "stock_flux"):
            print(f"   {k:18s} {s[k].sum():+6.1f}")
    soc = FONC.loc[SOCIAL]
    print(f"\nPar fonction (fongible) : santé et protection sociale {soc.dette_Mde.sum() / 1000:.0f} Md€,"
          f" {100 * soc.part_dette.sum():.1f} % de la dette ({100 * soc.part_dette_depuis_1995.sum():.1f}"
          " % depuis 1995)")
    print(f"Prorata des déficits primaires cumulés : social {PRORATA[SOCIAL].sum():.1f} sur "
          f"{PRORATA.sum():.1f} points de PIB")
    print("\nDérive (points de PIB cumulés 1996-2025) :")
    print(pd.DataFrame(DERIVES).round(1).to_string())
    print("\nRègles par administration, parts fin 2025 :")
    print((100 * REGLES).round(0).to_string())


# ================================================================ 6. figures
sys.path.insert(0, str(ICI.parent))
from graphiques import (BLEU, GRIS, INK2, MUTED, NU, OCRE, VERT, fin, grille,  # noqa: E402
                        panneau, plt, titre)
from matplotlib.ticker import FuncFormatter  # noqa: E402

BRIQUE = "#993333"
COUL = {"ETAT": BLEU, "APUL": VERT, "ASSO": OCRE}
LIB = {"ETAT": "État et ODAC", "APUL": "Collectivités locales", "ASSO": "Sécurité sociale"}
PCT0 = FuncFormatter(lambda x, _: f"{x:.0f} %")
PTS = FuncFormatter(lambda x, _: f"{x:+.0f}".replace("-", "−") if x else "0")
SRC = ("Source : Eurostat, comptes annuels des administrations publiques (gov_10a_main, "
       "gov_10a_taxag, gov_10a_exp), PIB (nama_10_gdp) ; Insee, dette de Maastricht par "
       "sous-secteur. Calculs de l'auteur (dette/dette.py).")
SRC_LONG = ("Source : Insee, comptes nationaux annuels base 2014 (séries arrêtées) jusqu'en 1995 ; "
            "Eurostat et Insee base 2020 ensuite. Calculs de l'auteur (dette/dette.py).")
POSTES = [("Vieillesse", ["GF1002"], OCRE), ("Santé", ["GF07"], "#a85b00"),
          ("Autre protection sociale", ["GF10X"], "#e3c27a"),
          ("Autres fonctions", [k for k in FONCTIONS if k not in SOCIAL], BLEU)]
AX = list(range(AN0, AN1 + 1))


def nb(x, d=0):
    return f"{x:,.{d}f}".replace(",", " ").replace(".", ",")


def sup(fig, t):
    """Titre d'une figure à deux panneaux (non dessiné en mode nu : il devient la légende)."""
    if not NU:
        fig.suptitle(t, x=0.005, ha="left", fontsize=12.5, y=1.07, fontweight="bold")


def fig_emetteur():
    fig, (a, b) = plt.subplots(1, 2, figsize=(10, 4.2), gridspec_kw={"wspace": 0.28})
    x = np.array(AX)
    bas = np.zeros(len(x))
    for k in ("ETAT", "APUL", "ASSO"):
        y = 100 * DETTE.loc[AX, k].values / PIB.loc[AX].values
        a.fill_between(x, bas, bas + y, color=COUL[k], alpha=0.85, lw=0, label=LIB[k])
        bas += y
    a.set_xlim(AN0, AN1)
    a.yaxis.set_major_formatter(PCT0)
    a.legend(loc="upper left")
    grille(a)
    panneau(a, "Dette de Maastricht par émetteur, en % du PIB")
    for s, k in (("S1311", "ETAT"), ("S1313", "APUL"), ("S1314", "ASSO")):
        b.plot(x, 100 * P.loc["B9"][s].loc[AX] / PIB.loc[AX], color=COUL[k], lw=1.8, label=LIB[k])
    b.axhline(0, color=INK2, lw=0.7)
    b.set_xlim(AN0, AN1)
    b.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f"{x:g} %".replace(".", ",")))
    grille(b)
    panneau(b, "Solde (capacité ou besoin de financement), en % du PIB")
    sup(fig, "La dette est émise par l'État, qui porte aussi presque tout le déficit")
    fin(fig, "dette_emetteur.png", SRC,
        f"Lecture : fin 2025, l'État et les organismes divers d'administration centrale portent "
        f"{100 * DETTE.loc[AN1, 'ETAT'] / DETTE.loc[AN1, 'APU']:.0f} % de la dette publique "
        f"({nb(DETTE.loc[AN1, 'APU'] / 1000)} Md€). La sécurité sociale a été excédentaire la "
        "plupart des années hors récessions : la CADES rembourse chaque année une partie de la dette "
        "qu'elle a reprise.")


def fig_financement():
    fig, (a, b) = plt.subplots(1, 2, figsize=(10, 4.2), gridspec_kw={"wspace": 0.28})
    ans24 = list(range(AN0, IMPOTS_2024 + 1))

    def pc(serie, ans=AX):
        return 100 * serie.loc[ans] / PIB.loc[ans]

    for ax, cible, titre_p in ((a, "S1314", "Vers la sécurité sociale"),
                               (b, "S1313", "Vers les collectivités")):
        ax.plot(AX, pc(P.loc[f"D7PAY_{cible}"]["S1311"] + P.loc[f"D9PAY_{cible}"]["S1311"]),
                color=BLEU, lw=1.8, label="Transferts versés par l'État")
        ax.plot(ans24, pc(IMP.loc["D211"][cible], ans24), color=OCRE, lw=1.8, label="TVA affectée")
        if cible == "S1314":
            ax.plot(ans24, pc(IMP.loc["D2"][cible] - IMP.loc["D211"][cible], ans24), color=OCRE,
                    lw=1.4, ls="--", label="Autres impôts sur la production\n(taxe sur les salaires, tabacs…)")
        ax.set_xlim(AN0, AN1)
        ax.set_ylim(0, 2.6 if cible == "S1314" else 4)
        ax.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f"{x:g} %".replace(".", ",")))
        grille(ax)
        ax.legend(loc="upper left", fontsize=8.5)
        panneau(ax, f"{titre_p}, en % du PIB")
    sup(fig, "L'État finance les autres administrations par des transferts et par des impôts qu'il leur cède")
    fin(fig, "dette_financement.png", SRC + " Transferts : courants (D7) et en capital (D9).",
        "Lecture : en comptabilité nationale, un impôt affecté est une recette propre de "
        "l'administration qui le perçoit, pas un transfert de l'État. Les sauts de 2006-2007 et de "
        "2019 pour la sécurité sociale correspondent à la compensation des allègements généraux de "
        "cotisations (panier fiscal, puis TVA lors de la transformation du CICE) ; ceux de 2018, 2021 et "
        "2023 pour les collectivités, au remplacement de la dotation globale de fonctionnement des "
        "régions, de la taxe d'habitation puis de la CVAE par des fractions de TVA.")


def fig_dynamique():
    t = DYN.loc[1979:]
    cum = t[["deficit_primaire", "effet_interets", "effet_croissance", "stock_flux"]].cumsum()
    fig, ax = plt.subplots(figsize=(7.8, 4.4))
    x = t.index.values
    ax.plot(x, t.dette - DYN.dette[1978], color=INK2, lw=2.4, label="Hausse du ratio de dette depuis 1978")
    for col, lib, coul, ls in (("deficit_primaire", "Déficits primaires", BRIQUE, "-"),
                               ("effet_interets", "Intérêts", OCRE, "--"),
                               ("effet_croissance", "Croissance du PIB nominal", VERT, "--"),
                               ("stock_flux", "Ajustements stock-flux", GRIS, ":")):
        ax.plot(x, cum[col], color=coul, lw=1.8, ls=ls, label=lib)
    ax.axvline(AN0, color=MUTED, lw=0.8, ls="-.")
    ax.text(AN0 + 0.4, 100, f"changement de\nbase (+{nb(CHANGEMENT_BASE, 1)} point)", fontsize=8,
            color=MUTED, va="top")
    ax.axhline(0, color=INK2, lw=0.7)
    ax.set_xlim(1979, AN1)
    ax.yaxis.set_major_formatter(PTS)
    ax.set_ylabel("Points de PIB, cumulés depuis 1978")
    grille(ax)
    ax.legend(loc="lower left", fontsize=8.3)
    a, b = t.loc[:AN0].sum(), t.loc[AN0 + 1:].sum()
    titre(ax, "Avant 1995, la dette montait surtout par les taux ; depuis, par les déficits primaires",
          "Décomposition standard de la hausse du ratio de dette publique, 1978-2025")
    fin(fig, "dette_dynamique.png", SRC_LONG,
        f"Lecture : de 1978 à 1995, le ratio de dette passe de {nb(DYN.dette[1978], 1)} % à "
        f"{nb(DYN.dette[AN0], 1)} % du PIB ; les déficits primaires n'y contribuent que pour "
        f"{nb(a.deficit_primaire, 1)} points, les intérêts ({nb(a.effet_interets, 1)}) dépassant la "
        f"croissance ({nb(a.effet_croissance, 1)}). De 1995 à 2025, il passe de {nb(B20.dette[AN0], 1)} % "
        f"à {nb(DYN.dette[AN1], 1)} % : déficits primaires {nb(b.deficit_primaire, 1)} points, intérêts "
        f"{nb(b.effet_interets, 1)}, croissance {nb(b.effet_croissance, 1)}, ajustements stock-flux "
        f"{nb(b.stock_flux, 1)}.")


def fig_fonctions():
    t = FONC.sort_values("dette_Mde")
    fig, ax = plt.subplots(figsize=(7.5, 4.6))
    y = np.arange(len(t))
    ax.barh(y, t.dette_Mde / 1000, color=[OCRE if k in SOCIAL else BLEU for k in t.index], height=0.66)
    for i, (_, r) in enumerate(t.iterrows()):
        ax.text(r.dette_Mde / 1000 + 12, i, f"{nb(r.dette_Mde / 1000)} Md€  ({100 * r.part_dette:.0f} %)",
                va="center", fontsize=8.5, color=INK2)
    ax.set_yticks(y)
    ax.set_yticklabels(t.fonction)
    ax.set_xlim(0, 1000)
    ax.xaxis.set_major_formatter(FuncFormatter(lambda x, _: nb(x)))
    ax.set_xlabel("Milliards d'euros")
    grille(ax, "x")
    soc = t.loc[SOCIAL]
    titre(ax, "Dette attribuée à chaque fonction si toutes les dépenses sont fongibles",
          f"Fin 2025 ; santé et protection sociale (en ocre) : {nb(soc.dette_Mde.sum() / 1000)} Md€, "
          f"{100 * soc.part_dette.sum():.0f} % de la dette")
    fin(fig, "dette_fonctions.png", SRC,
        "Lecture : chaque année depuis 1996, la hausse de la dette hors intérêts est répartie au "
        "prorata de la dépense de chaque fonction (COFOG), et chaque fonction porte les intérêts de "
        "la dette qui lui est attribuée ; le stock de 1995 est réparti selon la dépense de 1995. "
        "Les pensions des fonctionnaires sont dans la vieillesse, le RSA et les aides au logement "
        "dans l'autre protection sociale.")


def fig_evolution():
    ev = X.loc[:2024].copy()
    ev["interets"] = 100 * INT.loc[AN0:2024] / PIB.loc[AN0:2024]
    d = (ev.loc[2024] - ev.loc[AN0]).sort_values()
    lib = {**FONCTIONS, "interets": "Intérêts de la dette"}
    fig, ax = plt.subplots(figsize=(7.5, 4.6))
    y = np.arange(len(d))
    ax.barh(y, d.values, color=[OCRE if k in SOCIAL else (GRIS if k == "interets" else BLEU)
                                for k in d.index], height=0.66)
    for i, x in enumerate(d.values):
        ax.text(x + (0.05 if x >= 0 else -0.05), i, f"{x:+.1f}".replace(".", ",").replace("-", "−"),
                va="center", ha="left" if x >= 0 else "right", fontsize=8.5, color=INK2)
    ax.axvline(0, color=INK2, lw=0.7)
    ax.set_yticks(y)
    ax.set_yticklabels([lib[k] for k in d.index])
    ax.set_xlim(-2.2, 3.2)
    ax.xaxis.set_major_formatter(FuncFormatter(lambda x, _: f"{x:+g}".replace(".", ",").replace("-", "−")))
    ax.set_xlabel("Variation de la dépense entre 1995 et 2024, en points de PIB")
    grille(ax, "x")
    rec = TAU[2024] - TAU[AN0]
    titre(ax, "Depuis 1995, seules la santé et les retraites ont nettement augmenté",
          f"Dépense publique par fonction, variation 1995-2024 ; recettes : {rec:+.1f} point".replace(".", ","))
    autres = -d.drop(["interets", "GF07", "GF1002"]).sum()
    fin(fig, "dette_fonctions_evolution.png", SRC,
        f"Lecture : la dépense de vieillesse est passée de {nb(ev.loc[AN0, 'GF1002'], 1)} % à "
        f"{nb(ev.loc[2024, 'GF1002'], 1)} % du PIB. Hors intérêts, la dépense publique a augmenté de "
        f"{nb(d.drop('interets').sum(), 1)} points ; la santé et la vieillesse en expliquent "
        f"{nb(d['GF07'] + d['GF1002'], 1)}, les autres fonctions ont baissé ensemble de "
        f"{nb(autres, 1)} points.")


def fig_derive():
    ref = 1997
    fig, ax = plt.subplots(figsize=(7.8, 4.4))
    x = np.array(ANS)
    ecart = X.loc[ANS] - X.loc[ref]
    cum = {}
    for lib, cles, coul in POSTES:
        s = ecart[cles].sum(axis=1).cumsum()
        cum[lib] = s.iloc[-1]
        ax.plot(x, s, color=coul, lw=2, label=lib)
    ax.plot(x, -(TAU.loc[ANS] - TAU[ref]).cumsum(), color=VERT, lw=2, ls="--",
            label="Recettes (une hausse réduit le déficit)")
    ax.plot(x, PD[ref] * np.arange(1, len(ANS) + 1), color=GRIS, lw=1.5, ls=":",
            label=f"Déficit primaire de {ref} répété")
    ax.plot(x, PD.loc[ANS].cumsum(), color=INK2, lw=2.6, label="Total : déficits primaires cumulés")
    ax.axhline(0, color=INK2, lw=0.7)
    ax.set_xlim(ANS[0], AN1)
    ax.yaxis.set_major_formatter(PTS)
    ax.set_ylabel("Points de PIB, cumulés depuis 1996")
    grille(ax)
    ax.legend(loc="upper left", fontsize=8.3)
    titre(ax, f"Ce que chaque poste a ajouté au déficit depuis {ref}",
          f"Seconde convention : dérive de chaque poste par rapport à {ref}, cumulée")
    fin(fig, "dette_derive.png", SRC,
        f"Lecture : chaque courbe cumule l'écart annuel d'un poste à son niveau de {ref}, en points de "
        f"PIB. La hausse de la vieillesse a ajouté {nb(cum['Vieillesse'])} points de déficit cumulé et "
        f"celle de la santé {nb(cum['Santé'])} ; les autres fonctions en ont retiré "
        f"{nb(-cum['Autres fonctions'])}. Les courbes s'additionnent au total. {ref} est retenue parce "
        f"que le déficit primaire y était presque nul ({nb(PD[ref], 1)} point de PIB).")


def fig_prestations():
    t = DYN.loc[1960:]
    fig, (a, b) = plt.subplots(1, 2, figsize=(10, 4.2), gridspec_kw={"wspace": 0.28})
    a.plot(t.index, t.prestations, color=OCRE, lw=2.2)
    b.bar(t.index, t.deficit_primaire, color=[BRIQUE if x > 0 else VERT for x in t.deficit_primaire],
          width=0.8, lw=0)
    b.axhline(0, color=INK2, lw=0.7)
    for ax in (a, b):
        ax.axvline(AN0, color=MUTED, lw=0.8, ls="-.")
        grille(ax)
    a.set_xlim(1960, AN1)
    a.set_ylim(0, 30)
    a.yaxis.set_major_formatter(PCT0)
    b.set_xlim(1959.4, AN1 + 0.6)
    b.yaxis.set_major_formatter(PTS)
    panneau(a, "Prestations sociales des administrations, en % du PIB")
    panneau(b, "Déficit primaire (+) ou excédent (−), en % du PIB")
    sup(fig, "Les prestations sociales ont plus que doublé en part du PIB ; les déficits primaires "
             "ne sont devenus importants et permanents qu'après 2008")
    fin(fig, "dette_prestations.png", SRC_LONG,
        f"Lecture : les prestations sociales (en espèces, et en nature de produits marchands comme les "
        f"remboursements de soins) passent de {nb(t.prestations[1960], 1)} % du PIB en 1960 à "
        f"{nb(t.prestations[1978], 1)} % en 1978 et {nb(t.prestations[AN1], 1)} % en 2025. Les "
        "administrations ont dégagé des excédents primaires presque chaque année jusqu'au milieu des "
        "années 1970, puis en 1979-1980, 1989-1991 et 1998-2001. Le trait vertical marque le passage "
        "de la base 2014 à la base 2020.")


for figure in (fig_emetteur, fig_financement, fig_dynamique, fig_fonctions, fig_evolution,
               fig_derive, fig_prestations):
    figure()
