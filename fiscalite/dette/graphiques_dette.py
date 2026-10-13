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
from graphiques import (BLEU, GRIS, INK2, MUTED, NU, OCRE, VERT, fin, grille,  # noqa: E402
                        panneau, plt, titre)
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
        "déficits primaires de 1996 à 2025 et des intérêts qu'ils ont générés. Dans la dette totale, "
        "le stock de 1995 et les ajustements stock-flux sont répartis comme la dépense pour les "
        "règles au prorata (M1, M4) et laissés à l'émetteur pour les autres. "
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
          "Stock de 1995 réparti selon la logique de chaque règle")
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


def fig_dynamique():
    t = pd.read_csv(D / "dynamique.csv").set_index("annee").loc[1996:]
    cum = t.drop(columns="dette").cumsum()
    fig, ax = plt.subplots(figsize=(7.5, 4.4))
    x = cum.index.values
    ax.plot(x, t.dette - 57.5, color=INK2, lw=2.4, label="Hausse du ratio de dette depuis 1995")
    for col, lib, coul, ls in (("deficit_primaire", "Déficits primaires", BRIQUE, "-"),
                               ("effet_interets", "Intérêts", OCRE, "--"),
                               ("effet_croissance", "Croissance du PIB nominal", VERT, "--"),
                               ("stock_flux", "Ajustements stock-flux", GRIS, ":")):
        ax.plot(x, cum[col], color=coul, lw=1.8, ls=ls, label=lib)
    ax.axhline(0, color=INK2, lw=0.7)
    ax.set_xlim(1996, 2025)
    ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:+.0f}".replace("-", "−")))
    ax.set_ylabel("Points de PIB, cumulés depuis 1995")
    grille(ax)
    ax.legend(loc="lower left", fontsize=8.5)
    s = t.sum()
    titre(ax, "La hausse de la dette depuis 1995 vient des déficits primaires",
          "Décomposition standard de la dynamique du ratio de dette (FMI, Commission européenne)")
    fin(fig, "dette_dynamique.png", SRC_EUROSTAT + " Calculs de l'auteur (dette/dynamique.py).",
        f"Lecture : le ratio de dette est passé de 57,5 % du PIB en 1995 à {nb(t.dette.iloc[-1], 1)} % "
        f"en 2025. Les déficits primaires cumulés y contribuent pour {nb(s.deficit_primaire, 1)} "
        f"points ; les intérêts ({nb(s.effet_interets, 1)} points) ont été presque entièrement "
        f"compensés par la croissance du PIB nominal ({nb(s.effet_croissance, 1)}) ; les ajustements "
        f"stock-flux font {nb(s.stock_flux, 1)} points.")


fig_dynamique()
fig_fonctions()
fig_evolution()
fig_emetteur()
fig_financement()
fig_methodes()
fig_asso_temps()
fig_decomposition()

# ---------------------------------------------------------------- dynamique : figures annuelles
POSTES = [("vieillesse", "Vieillesse", ["GF1002"], OCRE),
          ("sante", "Santé", ["GF07"], "#a85b00"),
          ("autre_soc", "Autre protection sociale", ["GF10X"], "#e3c27a"),
          ("autres", "Autres fonctions", ["GF01", "GF02", "GF03", "GF04", "GF05", "GF06", "GF08",
                                          "GF09"], BLEU)]
SRC_DYN = SRC_EUROSTAT + " Calculs de l'auteur (dette/dynamique.py)."
PTS = FuncFormatter(lambda v, _: f"{v:+.0f}".replace("-", "−") if v else "0")


def barres_empilees(ax, x, series, couleurs, labels, largeur=0.75):
    """Barres empilées où les valeurs positives et négatives s'empilent séparément."""
    haut, bas = np.zeros(len(x)), np.zeros(len(x))
    for y, c, l in zip(series, couleurs, labels):
        y = np.asarray(y, dtype=float)
        pos, neg = np.where(y > 0, y, 0), np.where(y < 0, y, 0)
        ax.bar(x, pos, bottom=haut, color=c, width=largeur, label=l, lw=0)
        ax.bar(x, neg, bottom=bas, color=c, width=largeur, lw=0)
        haut += pos
        bas += neg


def fig_contributions():
    t = pd.read_csv(D / "dynamique.csv").set_index("annee").loc[1996:]
    fig, ax = plt.subplots(figsize=(7.8, 4.4))
    x = t.index.values
    barres_empilees(ax, x, [t.deficit_primaire, t.effet_interets, t.effet_croissance, t.stock_flux],
                    [BRIQUE, OCRE, VERT, GRIS],
                    ["Déficit primaire", "Intérêts", "Croissance du PIB nominal",
                     "Ajustements stock-flux"])
    ax.plot(x, t.dette.diff().loc[1996:], color=INK2, lw=0, marker="o", ms=4.5,
            label="Variation du ratio de dette")
    ax.axhline(0, color=INK2, lw=0.7)
    ax.set_xlim(1995.4, 2025.6)
    ax.yaxis.set_major_formatter(PTS)
    ax.set_ylabel("Points de PIB")
    grille(ax)
    ax.set_ylim(-10, 22)
    ax.legend(loc="upper left", fontsize=8.3, ncol=3)
    titre(ax, "Chaque année, la dette varie du déficit primaire et de l'écart entre taux et croissance",
          "Contributions annuelles à la variation du ratio de dette publique")
    fin(fig, "dette_contributions_annuelles.png", SRC_DYN,
        f"Lecture : en 2020, le ratio de dette a augmenté de {nb(t.dette.diff()[2020], 1)} points de "
        f"PIB : {nb(t.deficit_primaire[2020], 1)} de déficit primaire, {nb(t.effet_croissance[2020], 1)} "
        f"dus à la baisse du PIB nominal (l'effet de la croissance devient positif quand le PIB "
        f"recule), {nb(t.effet_interets[2020], 1)} d'intérêts et {nb(t.stock_flux[2020], 1)} "
        "d'ajustements stock-flux (trésorerie constituée par l'État). Les intérêts ajoutent chaque année "
        "de 1 à 4 points ; la croissance en retire en général autant.")


def fig_prorata_annuel():
    a = pd.read_csv(D / "dynamique_annuel.csv").set_index("annee")
    fig, ax = plt.subplots(figsize=(7.8, 4.4))
    x = a.index.values
    series = [a[[f"prorata_{k}" for k in cles]].sum(axis=1) for _, _, cles, _ in POSTES]
    barres_empilees(ax, x, series, [c for *_, c in POSTES], [l for _, l, _, _ in POSTES])
    ax.axhline(0, color=INK2, lw=0.7)
    ax.set_xlim(1995.4, 2025.6)
    ax.yaxis.set_major_formatter(PTS)
    ax.set_ylabel("Points de PIB")
    grille(ax)
    ax.legend(loc="upper left", fontsize=8.5)
    soc = sum(series[:3]).sum()
    titre(ax, "Le déficit primaire de chaque année, réparti au prorata de la dépense",
          "Première convention : dépenses fongibles ; déficit primaire en % du PIB, par fonction")
    fin(fig, "dette_prorata_annuel.png", SRC_DYN,
        f"Lecture : chaque barre est le déficit primaire de l'année (un excédent de 1998 à 2001), "
        f"réparti selon la part de chaque fonction dans la dépense hors intérêts. Cumulés sur "
        f"1996-2025, ces déficits font {nb(a.deficit_primaire.sum(), 1)} points de PIB, dont "
        f"{nb(soc, 1)} pour la santé et la protection sociale. Par construction, la répartition de "
        "chaque barre suit la structure de la dépense de l'année.")


def fig_derive_cumul():
    a = pd.read_csv(D / "dynamique_annuel.csv").set_index("annee")
    fig, ax = plt.subplots(figsize=(7.8, 4.4))
    x = a.index.values
    for _, lib, cles, coul in POSTES:
        ax.plot(x, a[[f"derive1997_{k}" for k in cles]].sum(axis=1).cumsum(), color=coul, lw=2,
                label=lib)
    ax.plot(x, a.derive1997_recettes.cumsum(), color=VERT, lw=2, ls="--",
            label="Recettes (une hausse réduit le déficit)")
    ax.plot(x, a.derive1997_reference.cumsum(), color=GRIS, lw=1.5, ls=":",
            label="Déficit primaire de 1997 répété")
    ax.plot(x, a.deficit_primaire.cumsum(), color=INK2, lw=2.6,
            label="Total : déficits primaires cumulés")
    ax.axhline(0, color=INK2, lw=0.7)
    ax.set_xlim(1996, 2025)
    ax.yaxis.set_major_formatter(PTS)
    ax.set_ylabel("Points de PIB, cumulés depuis 1996")
    grille(ax)
    ax.legend(loc="upper left", fontsize=8.3)
    cum = {lib: a[[f"derive1997_{k}" for k in cles]].sum(axis=1).sum() for _, lib, cles, _ in POSTES}
    titre(ax, "Ce que chaque poste a ajouté au déficit depuis 1997",
          "Seconde convention : dérive de chaque poste par rapport à 1997, cumulée")
    fin(fig, "dette_derive_cumul.png", SRC_DYN,
        f"Lecture : chaque courbe cumule l'écart annuel d'un poste à son niveau de 1997, en points de "
        f"PIB. La hausse de la vieillesse a ajouté {nb(cum['Vieillesse'])} points de déficit cumulé et "
        f"celle de la santé {nb(cum['Santé'])} ; les autres fonctions en ont retiré "
        f"{nb(-cum['Autres fonctions'])}. Les courbes s'additionnent au total. 1997 est retenue parce "
        "que le déficit primaire y était presque nul (0,2 point de PIB).")


def fig_derive_references():
    v = pd.read_csv(D / "dynamique_fonctions.csv").set_index("poste")
    lignes = [(lib, cles) for _, lib, cles, _ in POSTES] + [
        ("Recettes", ["recettes"]), ("Déficit de l'année de référence", ["deficit_de_reference"])]
    cols = [("prorata", "Prorata", GRIS), ("derive_1995", "Dérive depuis 1995", "#aabbdd"),
            ("derive_1997", "Dérive depuis 1997", BLEU), ("derive_2000", "Dérive depuis 2000", "#0b2a61")]
    fig, ax = plt.subplots(figsize=(7.8, 4.8))
    y = np.arange(len(lignes))
    h = 0.2
    for k, (col, lib, coul) in enumerate(cols):
        vals = [v.loc[v.index.intersection(cles), col].sum(min_count=1) for _, cles in lignes]
        vals = [0 if pd.isna(z) else z for z in vals]
        ax.barh(y + (k - 1.5) * h, vals, height=h, color=coul, label=lib)
    ax.axvline(0, color=INK2, lw=0.7)
    ax.set_yticks(y)
    ax.set_yticklabels([l for l, _ in lignes])
    ax.invert_yaxis()
    ax.xaxis.set_major_formatter(PTS)
    ax.set_xlabel("Points de PIB de déficit primaire cumulé, 1996-2025")
    grille(ax, "x")
    ax.legend(loc="center right", fontsize=8.3)
    titre(ax, "Seules la vieillesse et la santé pèsent lourd quelle que soit la convention",
          "Ventilation des 50,5 points de déficits primaires cumulés, selon la convention")
    fin(fig, "dette_derive_references.png", SRC_DYN,
        "Lecture : chaque groupe de barres totalise 50,5 points de PIB. Avec la dérive, la ventilation "
        "dépend de l'année de référence : prendre 1995 (déficit primaire de 1,6 point) ou 2000 (excédent "
        "de 1,6 point) comme norme change le signe des autres fonctions et du déficit de référence. La "
        "vieillesse (+42 à +55) et la santé (+32) restent les deux principaux postes.")


fig_contributions()
fig_prorata_annuel()
fig_derive_cumul()
fig_derive_references()

# ---------------------------------------------------------------- séries longues (Insee base 2014)
SRC_LONG = ("Source : Insee, comptes nationaux annuels base 2014 (séries arrêtées) jusqu'en 1995 ; "
            "Eurostat et Insee base 2020 ensuite. Calculs de l'auteur (dette/dynamique_longue.py).")


def fig_longue_dynamique():
    t = pd.read_csv(D / "dynamique_longue.csv").set_index("annee").loc[1979:]
    cum = t[["deficit_primaire", "effet_interets", "effet_croissance", "stock_flux"]].cumsum()
    d0 = 21.2
    fig, ax = plt.subplots(figsize=(7.8, 4.4))
    x = t.index.values
    ax.plot(x, t.dette - d0, color=INK2, lw=2.4, label="Hausse du ratio de dette depuis 1978")
    for col, lib, coul, ls in (("deficit_primaire", "Déficits primaires", BRIQUE, "-"),
                               ("effet_interets", "Intérêts", OCRE, "--"),
                               ("effet_croissance", "Croissance du PIB nominal", VERT, "--"),
                               ("stock_flux", "Ajustements stock-flux", GRIS, ":")):
        ax.plot(x, cum[col], color=coul, lw=1.8, ls=ls, label=lib)
    ax.axvline(1995, color=MUTED, lw=0.8, ls="-.")
    ax.text(1995.4, 100, "changement de\nbase (+1,4 point)", fontsize=8, color=MUTED, va="top")
    ax.axhline(0, color=INK2, lw=0.7)
    ax.set_xlim(1979, 2025)
    ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:+.0f}".replace("-", "−")))
    ax.set_ylabel("Points de PIB, cumulés depuis 1978")
    grille(ax)
    ax.legend(loc="lower left", fontsize=8.3)
    a = t.loc[:1995].sum()
    titre(ax, "Avant 1995, la dette montait surtout par les taux ; depuis, par les déficits primaires",
          "Décomposition standard de la hausse du ratio de dette publique, 1978-2025")
    fin(fig, "dette_longue_dynamique.png", SRC_LONG,
        f"Lecture : de 1978 à 1995, le ratio de dette passe de 21,2 % à 56,1 % du PIB. Les déficits "
        f"primaires n'y contribuent que pour {nb(a.deficit_primaire, 1)} points ; les intérêts "
        f"({nb(a.effet_interets, 1)}) dépassent nettement la croissance ({nb(a.effet_croissance, 1)}), "
        f"car les taux réels étaient élevés après la désinflation ; les ajustements stock-flux font "
        f"{nb(a.stock_flux, 1)} points. De 1995 à 2025, les intérêts et la croissance se compensent "
        "et la hausse vient des déficits primaires.")


def fig_longue_prestations():
    t = pd.read_csv(D / "dynamique_longue.csv").set_index("annee").loc[1960:]
    fig, (a, b) = plt.subplots(1, 2, figsize=(10, 4.2), gridspec_kw={"wspace": 0.28})
    a.plot(t.index, t.prestations, color=OCRE, lw=2.2)
    a.axvline(1995, color=MUTED, lw=0.8, ls="-.")
    a.set_xlim(1960, 2025)
    a.set_ylim(0, 30)
    a.yaxis.set_major_formatter(PCT0)
    grille(a)
    panneau(a, "Prestations sociales des administrations, en % du PIB")
    b.bar(t.index, t.deficit_primaire, color=[BRIQUE if v > 0 else VERT for v in t.deficit_primaire],
          width=0.8, lw=0)
    b.axhline(0, color=INK2, lw=0.7)
    b.axvline(1995, color=MUTED, lw=0.8, ls="-.")
    b.set_xlim(1959.4, 2025.6)
    b.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:+.0f}".replace("-", "−") if v else "0"))
    grille(b)
    panneau(b, "Déficit primaire (+) ou excédent (−), en % du PIB")
    sup(fig, "Les prestations sociales ont plus que doublé en part du PIB ; les déficits primaires "
             "ne sont devenus importants et permanents qu'après 2008")
    fin(fig, "dette_longue_prestations.png", SRC_LONG,
        f"Lecture : les prestations sociales (en espèces, et en nature de produits marchands comme les "
        f"remboursements de soins) passent de {nb(t.prestations[1960], 1)} % du PIB en 1960 à "
        f"{nb(t.prestations[1978], 1)} % en 1978 et {nb(t.prestations[2025], 1)} % en 2025. Les "
        "administrations ont dégagé des excédents primaires presque chaque année jusqu'au milieu des "
        "années 1970, puis en 1979-1980, 1989-1991 et 1998-2001 : la hausse des prestations a "
        "longtemps été financée par celle des prélèvements. Le trait vertical "
        "marque le passage de la base 2014 à la base 2020.")


fig_longue_dynamique()
fig_longue_prestations()
