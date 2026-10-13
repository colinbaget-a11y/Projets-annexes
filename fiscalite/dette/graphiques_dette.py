"""
Figures du projet « à qui attribuer la dette publique ? ».

Données : dette/donnees/ (extract_dette.py, attribution.py). Charte et sorties : graphiques.py.

    python dette/attribution.py && FIG_NU=1 python dette/graphiques_dette.py
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from graphiques import BLEU, GRIS, INK2, NU, OCRE, VERT, fin, grille, panneau, plt, titre  # noqa: E402
from matplotlib.ticker import FuncFormatter  # noqa: E402

D = Path(__file__).resolve().parent / "donnees"
BRIQUE = "#993333"
COUL = {"ETAT": BLEU, "APUL": VERT, "ASSO": OCRE, "SOCIAL": OCRE, "AUTRES": GRIS}
LIB = {"ETAT": "État et ODAC", "APUL": "Collectivités locales", "ASSO": "Sécurité sociale",
       "SOCIAL": "Santé et protection sociale", "AUTRES": "Autres fonctions"}
PCT0 = FuncFormatter(lambda v, _: f"{v:.0f} %")
SRC_EUROSTAT = ("Source : Eurostat, comptes annuels des administrations publiques (gov_10a_main, "
                "gov_10a_taxag, gov_10a_exp), PIB (nama_10_gdp) ; Insee, dette trimestrielle de "
                "Maastricht par sous-secteur (contributions consolidées, 4e trimestre).")

c = pd.read_csv(D / "comptes.csv")
P = c.pivot_table(index=["na_item", "time"], columns="sector", values="valeur")
imp = pd.read_csv(D / "impots.csv").pivot_table(index=["na_item", "time"], columns="sector",
                                                values="valeur")
pib = pd.read_csv(D / "pib.csv").set_index("time").valeur
dette = pd.read_csv(D / "dette_insee.csv").pivot(index="time", columns="sous_secteur",
                                                  values="valeur") * 1000
dette["ETAT"] = dette.Etat + dette.ODAC
R = pd.read_csv(D / "attribution_annuelle.csv")
ANS = list(range(1995, 2026))


def nb(x, d=0):
    return f"{x:,.{d}f}".replace(",", " ").replace(".", ",")


def sup(fig, t):
    """Titre d'une figure à deux panneaux (non dessiné en mode nu : il devient la légende)."""
    if not NU:
        fig.suptitle(t, x=0.005, ha="left", fontsize=12.5, y=1.07, fontweight="bold")


def fig_emetteur():
    fig, (a, b) = plt.subplots(1, 2, figsize=(10, 4.2), gridspec_kw={"wspace": 0.28})
    x = np.array(ANS)
    bas = np.zeros(len(x))
    for k in ("ETAT", "APUL", "ASSO"):
        y = 100 * dette.loc[ANS, k].values / pib.loc[ANS].values
        a.fill_between(x, bas, bas + y, color=COUL[k], alpha=0.85, lw=0, label=LIB[k])
        bas += y
    a.set_xlim(1995, 2025)
    a.yaxis.set_major_formatter(PCT0)
    a.legend(loc="upper left")
    grille(a)
    panneau(a, "Dette de Maastricht par émetteur, en % du PIB")
    for s, k in (("S1311", "ETAT"), ("S1313", "APUL"), ("S1314", "ASSO")):
        b.plot(x, 100 * P.loc["B9"][s].loc[ANS] / pib.loc[ANS], color=COUL[k], lw=1.8, label=LIB[k])
    b.axhline(0, color=INK2, lw=0.7)
    b.set_xlim(1995, 2025)
    b.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:g} %".replace(".", ",")))
    grille(b)
    panneau(b, "Solde (capacité ou besoin de financement), en % du PIB")
    sup(fig, "La dette est émise par l'État, qui porte aussi presque tout le déficit")
    fin(fig, "dette_emetteur.png", SRC_EUROSTAT,
        f"Lecture : fin 2025, l'État et les organismes divers d'administration centrale portent "
        f"{100 * dette.loc[2025, 'ETAT'] / dette.loc[2025, 'APU']:.0f} % de la dette publique "
        f"({nb(dette.loc[2025, 'APU'] / 1000)} Md€). La sécurité sociale a été excédentaire la "
        "plupart des années hors récessions : la caisse d'amortissement de la dette sociale (CADES) "
        "rembourse chaque année une partie de la dette qu'elle a reprise.")


def fig_financement():
    fig, (a, b) = plt.subplots(1, 2, figsize=(10, 4.2), gridspec_kw={"wspace": 0.28})
    x = np.array(ANS)
    ans24 = list(range(1995, 2025))

    def g(serie, ans=ANS):
        return 100 * serie.loc[ans] / pib.loc[ans]

    for ax, cible, lib in ((a, "S1314", "sécurité sociale"), (b, "S1313", "collectivités")):
        tr = g(P.loc[f"D7PAY_{cible}"]["S1311"] + P.loc[f"D9PAY_{cible}"]["S1311"])
        tva = g(imp.loc["D211"][cible], ans24)
        ax.plot(x, tr, color=BLEU, lw=1.8, label="Transferts versés par l'État")
        ax.plot(ans24, tva, color=OCRE, lw=1.8, label="TVA affectée")
        if cible == "S1314":
            autres = g(imp.loc["D2"][cible] - imp.loc["D211"][cible], ans24)
            ax.plot(ans24, autres, color=OCRE, lw=1.4, ls="--",
                    label="Autres impôts sur la production\n(taxe sur les salaires, tabacs…)")
        ax.set_xlim(1995, 2025)
        ax.set_ylim(0, 2.6 if cible == "S1314" else 4)
        ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:g} %".replace(".", ",")))
        grille(ax)
        ax.legend(loc="upper left", fontsize=8.5)
        panneau(ax, f"Vers la {lib}, en % du PIB" if cible == "S1314" else f"Vers les {lib}, en % du PIB")
    sup(fig, "L'État finance les autres administrations par des transferts et par des impôts qu'il leur cède")
    fin(fig, "dette_financement.png", SRC_EUROSTAT + " Transferts : courants (D7) et en capital (D9).",
        "Lecture : en comptabilité nationale, un impôt affecté est une recette propre de "
        "l'administration qui le perçoit, pas un transfert de l'État. Les sauts de 2006-2007 et de "
        "2019 pour la sécurité sociale correspondent à la compensation des allègements généraux de "
        "cotisations (panier fiscal, puis TVA lors de la transformation du CICE) ; ceux de 2018, 2021 et "
        "2023 pour les collectivités, au remplacement de la dotation globale de fonctionnement des "
        "régions, de la taxe d'habitation puis de la CVAE par des fractions de TVA.")


def fig_methodes():
    m = {"M0": "Émetteur (M0)", "M2": "Transferts\nexplicites (M2)",
         "M3": "TVA affectée\ncomme transfert (M3)", "M1": "Dépense finale\n(M1)",
         "M4": "Dépense par\nfonction (M4)"}
    f = R[R.annee == 2025]
    fig, (a, b) = plt.subplots(1, 2, figsize=(10, 4.2), sharey=True, gridspec_kw={"wspace": 0.08})
    for ax, col, pan in ((a, "part", "Dette totale fin 2025"),
                         (b, "part_nouveau", "Dette créée depuis 1995\n(déficits primaires et leurs intérêts)")):
        for i, (code, lib) in enumerate(m.items()):
            g = f[f.methode == code].set_index("sous_secteur")[col]
            ordre = ["SOCIAL", "AUTRES"] if code == "M4" else ["ASSO", "APUL", "ETAT"]
            gauche = 0
            for k in ordre:
                w = 100 * g[k]
                ax.barh(i, w, left=gauche, color=COUL[k], height=0.62,
                        label=LIB[k] if (i == 0 or code == "M4") and ax is a else None)
                if abs(w) >= 6:
                    ax.text(gauche + w / 2, i, f"{w:.0f}", ha="center", va="center", color="white",
                            fontsize=8.5, fontweight="bold")
                gauche += w
        ax.set_yticks(range(len(m)))
        ax.set_yticklabels(m.values())
        ax.invert_yaxis()
        ax.set_xlim(-8, 100)
        ax.axvline(0, color=INK2, lw=0.7)
        ax.xaxis.set_major_formatter(PCT0)
        grille(ax, "x")
        panneau(ax, pan)
    b.tick_params(axis="y", length=0)
    h, l = a.get_legend_handles_labels()
    fig.legend(h, l, loc="lower center", ncol=3, bbox_to_anchor=(0.5, -0.16), fontsize=8.5)
    sup(fig, "Selon la règle d'attribution, la sécurité sociale porte de presque rien à 59 % de la dette créée depuis 1995")
    nouveau = R[(R.annee == 2025) & (R.methode == "M0")].nouveau.sum()
    fin(fig, "dette_methodes.png", SRC_EUROSTAT + " Calculs de l'auteur (dette/attribution.py).",
        f"Lecture : la dette créée depuis 1995 ({nb(nouveau / 1000)} Md€ fin 2025) est la somme des "
        "déficits primaires de 1996 à 2025 et des intérêts qu'ils ont générés ; le reste de la dette "
        "est le stock de 1995, ses intérêts et les ajustements stock-flux, laissés à l'émetteur. "
        "Une barre qui dépasse à gauche de zéro signale une contribution négative (excédents "
        "primaires cumulés). La méthode par fonction répartit la dette entre fonctions et non entre administrations : "
        "elle compte en santé et protection sociale le RSA versé par les départements ou les aides "
        "au logement.")


def fig_asso_temps():
    fig, ax = plt.subplots(figsize=(7.5, 4.2))
    lib = {"M0": ("Émetteur", GRIS, "-"), "M2": ("Transferts explicites", BLEU, "-"),
           "M3": ("TVA affectée traitée comme transfert", BRIQUE, "-"),
           "M1": ("Prorata de la dépense finale", OCRE, "-"),
           "M4": ("Fonction : santé et protection sociale", VERT, "--")}
    for code, (l, col, ls) in lib.items():
        k = "SOCIAL" if code == "M4" else "ASSO"
        g = R[(R.methode == code) & (R.sous_secteur == k)].set_index("annee").part
        ax.plot(g.index, 100 * g, color=col, lw=1.8, ls=ls, label=l)
    ax.set_xlim(1996, 2025)
    ax.set_ylim(0, 40)
    ax.yaxis.set_major_formatter(PCT0)
    grille(ax)
    ax.legend(loc="upper left", fontsize=8.5)
    titre(ax, "Part de la dette totale attribuée à la sécurité sociale",
          "Stock de 1995 et ses intérêts laissés à l'émetteur")
    fin(fig, "dette_asso_temps.png", SRC_EUROSTAT + " Calculs de l'auteur (dette/attribution.py).",
        "Lecture : la TVA affectée change peu le résultat avant 2019 ; à partir de 2019, la "
        "compensation des allègements de cotisations par une fraction de TVA fait basculer environ "
        "35 Md€ par an vers la sécurité sociale dans cette méthode.")


def fig_decomposition():
    t = R[(R.annee >= 1996) & (R.methode == "M0")].groupby("annee")[["herite", "sfa", "nouveau"]].sum()
    fig, ax = plt.subplots(figsize=(7.5, 4.2))
    x = t.index.values
    y = [t.herite / pib.loc[x] * 100, t.sfa / pib.loc[x] * 100, t.nouveau / pib.loc[x] * 100]
    ax.stackplot(x, y, colors=[GRIS, "#c9c9c9", BLEU], alpha=0.9,
                 labels=["Stock de 1995 et ses intérêts", "Ajustements stock-flux et leurs intérêts",
                         "Déficits primaires depuis 1996 et leurs intérêts"])
    ax.set_xlim(1996, 2025)
    ax.yaxis.set_major_formatter(PCT0)
    grille(ax)
    ax.legend(loc="upper left", fontsize=8.5)
    titre(ax, "Plus de la moitié de la dette de 2025 est le stock de 1995 et ses intérêts",
          "Dette des APU en % du PIB, intérêts au taux apparent des APU")
    h = t.loc[2025]
    fin(fig, "dette_decomposition.png", SRC_EUROSTAT + " Calculs de l'auteur (dette/attribution.py).",
        f"Lecture : fin 2025, les 702 Md€ de dette de 1995, capitalisés au taux apparent des APU "
        f"(6,5 % en 1996, 1,3 % en 2020), représentent {nb(h.herite / 1000)} Md€ ; les déficits "
        f"primaires de 1996 à 2025 et leurs intérêts, {nb(h.nouveau / 1000)} Md€. C'est une "
        "décomposition comptable, pas causale : sans excédents primaires, les intérêts de la dette "
        "héritée sont payés par de nouveaux emprunts.")


SOC = {"GF07", "GF1002", "GF10X"}


def fig_fonctions():
    t = pd.read_csv(D / "fonctions_2025.csv").set_index("cofog").sort_values("dette_Mde")
    fig, ax = plt.subplots(figsize=(7.5, 4.6))
    y = np.arange(len(t))
    coul = [OCRE if k in SOC else BLEU for k in t.index]
    ax.barh(y, t.dette_Mde / 1000, color=coul, height=0.66)
    for i, (k, r) in enumerate(t.iterrows()):
        ax.text(r.dette_Mde / 1000 + 12, i, f"{nb(r.dette_Mde / 1000)} Md€  ({100 * r.part_dette:.0f} %)",
                va="center", fontsize=8.5, color=INK2)
    ax.set_yticks(y)
    ax.set_yticklabels(t.fonction)
    ax.set_xlim(0, 1000)
    ax.xaxis.set_major_formatter(FuncFormatter(lambda v, _: nb(v)))
    ax.set_xlabel("Milliards d'euros")
    grille(ax, "x")
    soc = t.loc[list(SOC)]
    titre(ax, "Dette attribuée à chaque fonction si toutes les dépenses sont fongibles",
          f"Fin 2025 ; santé et protection sociale (en ocre) : {nb(soc.dette_Mde.sum() / 1000)} Md€, "
          f"{100 * soc.part_dette.sum():.0f} % de la dette")
    fin(fig, "dette_fonctions.png", SRC_EUROSTAT + " Calculs de l'auteur (dette/fongible.py).",
        "Lecture : chaque année depuis 1996, la hausse de la dette hors intérêts est répartie au "
        "prorata de la dépense de chaque fonction (COFOG), et chaque fonction porte les intérêts de "
        "la dette qui lui est attribuée ; le stock de 1995 est réparti selon la dépense de 1995. "
        "Les intérêts sont retirés des services généraux. Les pensions des fonctionnaires sont dans "
        "la vieillesse, le RSA et les aides au logement dans l'autre protection sociale.")


def fig_evolution():
    ev = pd.read_csv(D / "fonctions_evolution.csv").set_index("annee")
    t = pd.read_csv(D / "fonctions_2025.csv").set_index("cofog")
    d = (ev.loc[2024] - ev.loc[1995])
    lib = dict(t.fonction)
    lib.update({"interets": "Intérêts de la dette", "recettes": "Recettes publiques"})
    d = d.drop(["recettes"]).sort_values()
    fig, ax = plt.subplots(figsize=(7.5, 4.6))
    y = np.arange(len(d))
    coul = [OCRE if k in SOC else (GRIS if k == "interets" else BLEU) for k in d.index]
    ax.barh(y, d.values, color=coul, height=0.66)
    for i, v in enumerate(d.values):
        ax.text(v + (0.05 if v >= 0 else -0.05), i, f"{v:+.1f}".replace(".", ",").replace("-", "−"),
                va="center", ha="left" if v >= 0 else "right", fontsize=8.5, color=INK2)
    ax.axvline(0, color=INK2, lw=0.7)
    ax.set_yticks(y)
    ax.set_yticklabels([lib[k] for k in d.index])
    ax.set_xlim(-2.2, 3.2)
    ax.xaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:+g}".replace(".", ",").replace("-", "−")))
    ax.set_xlabel("Variation de la dépense entre 1995 et 2024, en points de PIB")
    grille(ax, "x")
    rec = ev.loc[2024, "recettes"] - ev.loc[1995, "recettes"]
    titre(ax, "Depuis 1995, seules la santé et les retraites ont nettement augmenté",
          f"Dépense publique par fonction, variation 1995-2024 ; recettes : {rec:+.1f} point".replace(".", ",")
          .replace("+", "+"))
    fin(fig, "dette_fonctions_evolution.png", SRC_EUROSTAT + " Calculs de l'auteur (dette/fongible.py).",
        f"Lecture : la dépense de vieillesse est passée de {nb(ev.loc[1995, 'GF1002'], 1)} % à "
        f"{nb(ev.loc[2024, 'GF1002'], 1)} % du PIB. Hors intérêts, la dépense publique a augmenté de "
        f"{nb(d.drop('interets').sum(), 1)} points ; la santé et la vieillesse en expliquent "
        f"{nb(d['GF07'] + d['GF1002'], 1)}, les autres fonctions ont baissé ensemble de "
        f"{nb(-(d.drop(['interets', 'GF07', 'GF1002']).sum()), 1)} points.")


fig_fonctions()
fig_evolution()
fig_emetteur()
fig_financement()
fig_methodes()
fig_asso_temps()
fig_decomposition()
