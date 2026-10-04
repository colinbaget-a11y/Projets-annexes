"""
Les diagnostics chiffrés de la Mirrlees Review (« Tax by Design », IFS, 2011) appliqués
à la France, à partir des données OCDE extraites par extract_mirrlees.py.

    python graphiques_mirrlees.py
"""
import csv
from collections import defaultdict
from pathlib import Path

import matplotlib.pyplot as plt

from graphiques import NU, panneau, GRID, HALO, INK, INK2, MUTED, PAL, PCT, SEQ, SURFACE, etiquette, fin, grille, titre

HERE = Path(__file__).resolve().parent
OUT = HERE / "figures"
NOMS = {"FRA": "France", "DEU": "Allemagne", "GBR": "Royaume-Uni", "DNK": "Danemark", "SWE": "Suède",
        "ITA": "Italie", "ESP": "Espagne", "NLD": "Pays-Bas", "BEL": "Belgique", "AUT": "Autriche",
        "POL": "Pologne", "USA": "États-Unis", "OECD": "moyenne OCDE"}
MEN = {"S_C0": "Célibataire sans enfant", "S_C2": "Célibataire, deux enfants",
       "C_C0": "Couple sans enfant", "C_C2": "Couple, deux enfants"}
SAL = {"MINW": "au salaire minimum", "AW67": "à 67 % du salaire moyen", "AW100": "au salaire moyen"}
ORD_SAL = ["MINW", "AW67", "AW100"]


def lire(nom):
    return list(csv.DictReader(open(HERE / "donnees" / f"{nom}.csv", encoding="utf-8")))


SRC_C = ("Source : OCDE, Effective Carbon Rates (DSD_ECR), part des émissions de CO2 issues de l'énergie tarifées "
         "au-dessus de chaque seuil, 2021. Tarification = taxes sur l'énergie plus prix des quotas.")
SRC_T = ("Source : OCDE, modèle TaxBEN, 2025. Ménage demandant le revenu minimum garanti, sans aide au logement. "
         "Réplique les diagnostics des figures 4.7 et 4.8 de Tax by Design (IFS, 2011).")


# ================================================================ M1 : dispersion du prix du carbone
def m1():
    r = [x for x in lire("carbone_parts")
         if x["REF_AREA"] == "FRA" and x["TIME_PERIOD"] == "2021" and x["EMISSIONS_SOURCE"] == "FFUEL_BIOF"]
    cum = defaultdict(dict)
    for x in r:
        cum[x["SECTOR"]][x["PRICE_LEVEL"]] = float(x["OBS_VALUE"])
    lib = {x["SECTOR"]: x["Economic sector"] for x in r}
    fr_lib = {"ROAD": "Transport routier", "ELEC": "Électricité", "RESCOM": "Bâtiments",
              "INDUSTRY": "Industrie", "OFFROAD": "Transport hors route",
              "AGRIFISH": "Agriculture et pêche", "ENE": "Ensemble des secteurs"}
    bandes = [("non tarifé", "EUR_TCO2E_GT0", None, "#E3E5E8"),
              ("moins de 30 €", "EUR_TCO2E_GT0", "EUR_TCO2E_GT30", SEQ[1]),
              ("30 à 60 €", "EUR_TCO2E_GT30", "EUR_TCO2E_GT60", SEQ[2]),
              ("60 à 120 €", "EUR_TCO2E_GT60", "EUR_TCO2E_GT120", SEQ[4]),
              ("plus de 120 €", "EUR_TCO2E_GT120", None, SEQ[6])]
    secteurs = [s for s in ["ROAD", "ELEC", "ENE", "RESCOM", "INDUSTRY", "OFFROAD", "AGRIFISH"] if s in cum]
    secteurs.sort(key=lambda s: -cum[s].get("EUR_TCO2E_GT60", 0))

    fig, ax = plt.subplots(figsize=(10.4, 5.8))
    gauche = [0.0] * len(secteurs)
    for nom, haut, bas, col in bandes:
        v = []
        for s in secteurs:
            if nom == "non tarifé":
                v.append(100 - cum[s].get(haut, 0))
            elif bas is None:
                v.append(cum[s].get(haut, 0))
            else:
                v.append(cum[s].get(haut, 0) - cum[s].get(bas, 0))
        ax.barh(range(len(secteurs)), v, left=gauche, height=0.72, color=col, label=nom,
                edgecolor=SURFACE, linewidth=1.1, zorder=3)
        for i, (g, x) in enumerate(zip(gauche, v)):
            if x >= 9:
                ax.text(g + x / 2, i, f"{x:.0f}".replace(".", ","), ha="center", va="center", fontsize=9,
                        color="#FFFFFF" if col in (SEQ[4], SEQ[6]) else INK)
        gauche = [g + x for g, x in zip(gauche, v)]
    ax.set_yticks(range(len(secteurs)))
    ax.set_yticklabels([fr_lib.get(s, lib[s]) for s in secteurs], fontsize=10.5)
    for t in ax.get_yticklabels():
        if t.get_text() == "Ensemble des secteurs":
            t.set_fontweight("bold")
    ax.invert_yaxis(); grille(ax, "x")
    ax.set_xlim(0, 100); ax.xaxis.set_major_formatter(PCT)
    ax.set_xlabel("répartition des émissions de CO2 du secteur selon le prix qui leur est appliqué")
    ax.spines["left"].set_visible(False); ax.tick_params(axis="y", length=0)
    ax.legend(frameon=False, fontsize=9.5, ncol=5, loc="upper center", bbox_to_anchor=(0.5, -0.17))
    titre(ax, "Sur la route, plus de 120 € la tonne ; dans l'industrie et les bâtiments, moins de 60 €",
          "France, 2021. Le diagnostic du chapitre 11 de Tax by Design : ce qui compte n'est pas le niveau du prix\ndu carbone mais son uniformité, puisque les abattements les moins chers ne sont pas ceux qu'on déclenche.")
    fig.subplots_adjust(bottom=0.24)
    fin(fig, "m1_prix_carbone_secteurs.png", SRC_C)


# ================================================================ M2 : comparaison internationale
def m2():
    r = [x for x in lire("carbone_parts")
         if x["TIME_PERIOD"] == "2021" and x["EMISSIONS_SOURCE"] == "FFUEL_BIOF"
         and x["SECTOR"] == "ENE" and x["PRICE_LEVEL"] == "EUR_TCO2E_GT60"]
    d = sorted(((x["REF_AREA"], float(x["OBS_VALUE"])) for x in r), key=lambda t: -t[1])
    fig, ax = plt.subplots(figsize=(9.0, 5.0))
    cols = [PAL[0] if p == "FRA" else SEQ[2] for p, _ in d]
    ax.bar(range(len(d)), [v for _, v in d], width=0.72, color=cols, zorder=3)
    ax.set_xticks(range(len(d)))
    ax.set_xticklabels([NOMS.get(p, p) for p, _ in d], rotation=45, ha="right", fontsize=9.5)
    for t in ax.get_xticklabels():
        if t.get_text() == "France":
            t.set_fontweight("bold"); t.set_color(INK)
    i = [p for p, _ in d].index("FRA")
    ax.annotate(f"{d[i][1]:.0f} %".replace(".", ","), (i, d[i][1]), xytext=(0, 6),
                textcoords="offset points", ha="center", fontsize=10.5, fontweight="bold", color=PAL[0],
                path_effects=HALO)
    grille(ax); ax.yaxis.set_major_formatter(PCT); ax.set_ylim(0, 72)
    titre(ax, "Un tiers des émissions françaises sont tarifées au-dessus de 60 € la tonne",
          "Part des émissions de CO2 issues de l'énergie dont le prix dépasse 60 € par tonne, tous secteurs, 2021.")
    fig.subplots_adjust(bottom=0.22)
    fin(fig, "m2_carbone_comparaison.png", SRC_C)


# ================================================================ M3 : taux marginaux effectifs
def m3():
    r = [x for x in lire("taxben_metr")
         if x["TIME_PERIOD"] == "2025" and x["WORKING_HOURS_INCREASE"] == "PTFTW50T100"
         and x["SOC_ASS_BENEFIT"] == "YES" and x["HOUSE_BENEFIT"] == "NO"
         and x["INCOME_PART"] in ("_Z", "NOEARN_UNEMP_WO_CONBEN")]
    fr = {(x["HOUSEHOLD_TYPE"], x["INCOME_CURR"]): float(x["OBS_VALUE"]) for x in r if x["REF_AREA"] == "FRA"}
    pays = {}
    for x in r:
        if x["HOUSEHOLD_TYPE"] == "S_C0":
            pays.setdefault(x["REF_AREA"], {})[x["INCOME_CURR"]] = float(x["OBS_VALUE"])

    fig, (a1, a2) = plt.subplots(1, 2, figsize=(13.6, 6.0),
                                 gridspec_kw={"width_ratios": [1.25, 1], "wspace": 0.42})
    men = ["S_C0", "S_C2", "C_C0", "C_C2"]
    larg = 0.27
    for k, sal in enumerate(ORD_SAL):
        v = [fr.get((m, sal), float("nan")) for m in men]
        a1.bar([i + (k - 1) * larg for i in range(len(men))], v, width=larg * 0.92,
               color=[SEQ[2], SEQ[4], SEQ[6]][k], label=SAL[sal], zorder=3)
        for i, x in enumerate(v):
            a1.text(i + (k - 1) * larg, x + 1.2, f"{x:.0f}", ha="center", fontsize=8.5, color=INK2)
    court = {"S_C0": "seul", "S_C2": "seul,\n2 enfants", "C_C0": "couple", "C_C2": "couple,\n2 enfants"}
    a1.set_xticks(range(len(men)), [court[m] for m in men], fontsize=9)
    a1.legend(frameon=False, fontsize=8.8, loc="upper center", ncol=3, handlelength=1.0,
              columnspacing=0.8, bbox_to_anchor=(0.5, 1.0))
    grille(a1); a1.set_ylim(0, 80); a1.yaxis.set_major_formatter(PCT)
    panneau(a1, "France, selon le ménage et le salaire")

    d = sorted(((p, v.get("AW67", float("nan"))) for p, v in pays.items() if "AW67" in v),
               key=lambda t: t[1])
    y = range(len(d))
    a2.barh(list(y), [v for _, v in d], height=0.7,
            color=[PAL[0] if p == "FRA" else "#C9CDD2" for p, _ in d], zorder=3)
    for i, (p, v) in enumerate(d):
        a2.text(v + 1, i, f"{v:.0f}", va="center", fontsize=8.5,
                color=PAL[0] if p == "FRA" else INK2, fontweight="bold" if p == "FRA" else "normal")
    a2.set_yticks(list(y), [NOMS.get(p, p) for p, _ in d], fontsize=9)
    for t in a2.get_yticklabels():
        if t.get_text() == "France":
            t.set_fontweight("bold"); t.set_color(PAL[0])
    grille(a2, "x"); a2.set_xlim(0, 75); a2.xaxis.set_major_formatter(PCT)
    a2.spines["left"].set_visible(False); a2.tick_params(left=False)
    panneau(a2, "Personne seule à 67 % du salaire moyen")
    if not NU:
        fig.suptitle("Ce qu'il reste quand on double son temps de travail", x=0.005, ha="left",
                     fontsize=12.5, y=1.08)
    fin(fig, "m3_taux_marginaux_effectifs.png", SRC_T,
        "Lecture : part du salaire supplémentaire absorbée par les cotisations, l'impôt et le "
        "retrait des prestations quand on passe d'un mi-temps à un temps plein. Une personne seule "
        "payée à 67 % du salaire moyen en France perd 51 % de ce que lui rapporte ce passage.")


# ================================================================ M4 : taux de participation
def m4():
    r = [x for x in lire("taxben_ptr")
         if x["TIME_PERIOD"] == "2025" and x["HOUSE_BENEFIT"] == "NO"
         and x["TEMP_INTOWORK_BENEFIT"] == "NO" and x["INCOME_PART"] in ("_Z", "NOEARN_UNEMP_WO_CONBEN")]
    pays = defaultdict(dict)
    for x in r:
        if x["HOUSEHOLD_TYPE"] == "S_C0":
            pays[x["REF_AREA"]][x["INCOME_CURR"]] = float(x["OBS_VALUE"])
    d = sorted(((p, v) for p, v in pays.items() if "MINW" in v), key=lambda t: -t[1]["MINW"])
    fig, ax = plt.subplots(figsize=(9.8, 5.4))
    larg = 0.26
    for k, sal in enumerate(ORD_SAL):
        v = [x.get(sal, float("nan")) for _, x in d]
        ax.bar([i + (k - 1) * larg for i in range(len(d))], v, width=larg * 0.92,
               color=[SEQ[2], SEQ[4], SEQ[6]][k], label=SAL[sal], zorder=3)
    ax.set_xticks(range(len(d)))
    ax.set_xticklabels([NOMS.get(p, p) for p, _ in d], rotation=45, ha="right", fontsize=9.5)
    for t in ax.get_xticklabels():
        if t.get_text() == "France":
            t.set_fontweight("bold"); t.set_color(INK)
    ax.legend(frameon=False, fontsize=9, ncol=3, loc="upper right")
    grille(ax); ax.set_ylim(0, 92); ax.yaxis.set_major_formatter(PCT)
    titre(ax, "Ce que rapporte vraiment une reprise d'emploi",
          "Taux de participation d'un célibataire sans enfant quittant le revenu minimum garanti pour un emploi :\npart du salaire absorbée par les prélèvements et par les prestations perdues, 2025.")
    fig.subplots_adjust(bottom=0.26)
    fin(fig, "m4_taux_participation.png", SRC_T)


if __name__ == "__main__":
    print("figures :")
    for f in (m1, m2, m3, m4):
        f()
