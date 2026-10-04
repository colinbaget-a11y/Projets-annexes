"""Figures sur données réelles : Tax Foundation et OCDE.

Chaque figure illustre l'argument d'un chapitre du cours avec des chiffres observés, non avec un
calcul illustratif. Les données sont produites par extract_reelles.py dans donnees/.

    python graphiques_reels.py            # PNG et PDF pour la lecture
    FIG_NU=1 python graphiques_reels.py   # PDF nus pour le document LaTeX
"""
import csv
import math
import statistics as st
from pathlib import Path

import matplotlib.pyplot as plt

from graphiques import (NU, BLEU, GRIS, HALO, INK, INK2, OCRE, PCT, SURFACE, VERT,
                        fin, grille, panneau, titre)

HERE = Path(__file__).resolve().parent
BRIQUE = "#993333"
CLAIR = "#C4C8CE"          # pays de contexte
BLEU_CLAIR = "#9fb3d9"
SRC_REV = "Source : OCDE, Revenue Statistics, tableaux comparatifs (DSD_REV_COMP_OECD), données 2023."
SRC_TF = ("Source : Tax Foundation, International Tax Competitiveness Index 2025, données publiées "
          "sur github.com/TaxFoundation.")


def lire(nom):
    with open(HERE / "donnees" / nom, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def fr(v, d=0):
    return f"{v:.{d}f}".replace(".", ",")


REV = lire("recettes_ocde_pct_pib.csv")
NOMS = {x["code"]: x["pays"] for x in REV}


def rev(code, cat, annee="2023"):
    for x in REV:
        if x["code"] == code and x["categorie"] == cat and x["annee"] == annee:
            return float(x["pct_pib"])
    return None


def pays_ocde(annee="2023"):
    return sorted({x["code"] for x in REV if x["annee"] == annee and x["code"] != "OECD_REP"})


IDX = {x["ISO_3"]: x for x in lire("itci_variables_2025.csv")}


def idx(code, var):
    v = IDX[code].get(var, "")
    return float(v) if v not in ("", "NA") else None


# ----------------------------------------------------------------- r1 : la carte des écarts
def r1():
    cats = [("T_2000", "Cotisations sociales"), ("T_3000", "Taxes sur la masse salariale"),
            ("T_1100", "Impôt sur le revenu des personnes"), ("T_4100", "Impôt foncier récurrent"),
            ("T_4300", "Successions et donations"), ("AUTRES_BS", "Taxes sur biens et services hors TVA"),
            ("T_5111", "TVA"), ("T_4400", "Droits sur les transactions"),
            ("T_4200", "Impôt sur la fortune"), ("T_1200", "Impôt sur les sociétés")]

    def val(p, c):
        if c == "AUTRES_BS":
            return rev(p, "T_5000") - rev(p, "T_5111")
        return rev(p, c)

    ecarts = [(lab, val("FRA", c) - val("OECD_REP", c)) for c, lab in cats]
    total = rev("FRA", "_T") - rev("OECD_REP", "_T")
    reste = total - sum(e for _, e in ecarts)
    ecarts.append(("Autres prélèvements", reste))
    ecarts.sort(key=lambda t: t[1])
    fig, ax = plt.subplots(figsize=(10.6, 6.0))
    y = range(len(ecarts))
    ax.barh(list(y), [e for _, e in ecarts], height=0.66, zorder=2,
            color=[BLEU if e > 0 else BLEU_CLAIR for _, e in ecarts])
    for i, (lab, e) in enumerate(ecarts):
        ax.text(e + (0.12 if e >= 0 else -0.12), i, ("+" if e > 0 else "") + fr(e, 1).replace("-", "−"),
                va="center", ha="left" if e >= 0 else "right", fontsize=9.5, color=INK,
                fontweight="bold" if abs(e) > 1 else "normal")
    ax.set_yticks(list(y), [l for l, _ in ecarts], fontsize=9.5)
    ax.axvline(0, color=INK2, lw=0.9, zorder=3)
    ax.set_xlim(-2.4, 7.0)
    ax.set_xlabel("écart France − moyenne OCDE, en points de PIB")
    grille(ax, "x")
    ax.spines["left"].set_visible(False)
    ax.tick_params(left=False)
    titre(ax, "Les dix points d'écart avec l'OCDE viennent d'abord du travail",
          f"Écart de recettes entre la France ({fr(rev('FRA', '_T'), 1)} % du PIB) et la moyenne "
          f"de l'OCDE ({fr(rev('OECD_REP', '_T'), 1)} %), par catégorie, 2023.")
    fin(fig, "r1_carte_des_ecarts.png", SRC_REV,
        f"Note : sur {fr(total, 1)} points d'écart, {fr(ecarts[-1][1], 1)} viennent des seules "
        "cotisations sociales et 1,5 des taxes sur la masse salariale. L'impôt sur les sociétés est "
        "la seule grande catégorie où la France prélève moins que la moyenne. Les autres prélèvements "
        "regroupent les catégories 1300, 4500, 4600 et 6000 de l'OCDE.")


# ------------------------------------------------- r2 : le taux d'IS depuis 1980
def r2():
    d = {x["code"]: x for x in lire("is_taux_1980_2025.csv")}
    ans = list(range(1985, 2026))

    def s(code):
        return [(a, float(d[code][str(a)])) for a in ans if d[code].get(str(a))]

    moy = []
    for a in ans:
        v = [float(x[str(a)]) for x in d.values() if x.get(str(a))]
        if v:
            moy.append((a, st.mean(v), len(v)))
    fig, ax = plt.subplots(figsize=(10.6, 5.4))
    bouts = []
    for code in ("DEU", "GBR", "USA", "IRL"):
        pts = s(code)
        ax.plot([p[0] for p in pts], [p[1] for p in pts], color=CLAIR, lw=1.3, zorder=2)
        bouts.append([pts[-1][1], NOMS.get(code, code), GRIS, False])
    ax.plot([m[0] for m in moy], [m[1] for m in moy], color=GRIS, lw=2.0, zorder=3)
    bouts.append([moy[-1][1], f"moyenne OCDE  {fr(moy[-1][1], 1)}", GRIS, True])
    bouts.sort(key=lambda b: b[0])
    for i in range(1, len(bouts)):
        if bouts[i][0] - bouts[i - 1][0] < 2.4:
            bouts[i][0] = bouts[i - 1][0] + 2.4
    for yy, lab, c, gras in bouts:
        ax.text(2025.6, yy, lab, va="center", fontsize=9.3 if gras else 8.6, color=c,
                fontweight="bold" if gras else "normal")
    f = s("FRA")
    ax.plot([p[0] for p in f[:-1]], [p[1] for p in f[:-1]], color=BLEU, lw=2.7, zorder=4)
    ax.plot([f[-2][0], f[-1][0]], [f[-2][1], f[-1][1]], color=BLEU, lw=2.0, ls=(0, (2, 2)), zorder=4)
    ax.plot([f[-1][0]], [f[-1][1]], "o", ms=6.5, color=BLEU, markeredgecolor=SURFACE,
            markeredgewidth=1.5, zorder=5)
    ax.text(f[-1][0] + 0.6, f[-1][1], f"France  {fr(f[-1][1], 1)}", va="center", fontsize=9.6,
            color=BLEU, fontweight="bold")
    ax.annotate("surtaxe temporaire\ndes grandes entreprises", xy=(2025, f[-1][1]),
                xytext=(2011.5, 43.5), fontsize=9, color=INK2, linespacing=1.4,
                arrowprops=dict(arrowstyle="->", color=GRIS, lw=0.9,
                                connectionstyle="arc3,rad=-0.2"))
    ax.set_xlim(1985, 2034)
    ax.set_ylim(0, 64)
    ax.set_xticks([1985, 1990, 2000, 2010, 2020, 2025])
    ax.yaxis.set_major_formatter(PCT)
    grille(ax)
    titre(ax, "Le taux français a suivi la baisse générale avec une dizaine d'années de retard",
          "Taux statutaire de l'impôt sur les sociétés, contributions additionnelles comprises, "
          "1985-2025.")
    fin(fig, "r2_is_depuis_1985.png",
        "Sources : Tax Foundation, Corporate Tax Rates around the World (1985-2023) et "
        "International Tax Competitiveness Index (2024-2025).",
        f"Note : moyenne simple des pays de l'OCDE disponibles ({moy[0][2]} en 1985, 38 depuis "
        "2000). Le point de 2025, 36,1 %, inclut la contribution exceptionnelle sur les bénéfices "
        "des entreprises dont le chiffre d'affaires dépasse trois milliards d'euros ; le taux "
        "normal est resté à 25 %, 25,8 % avec la contribution sociale.")


# ------------------------------------------- r3 : taux d'IS et recettes d'IS
def r3():
    d = {x["code"]: x for x in lire("is_taux_1980_2025.csv")}
    pts = []
    for p in pays_ocde():
        t = d.get(p, {}).get("2023")
        y = rev(p, "T_1200")
        if t and y is not None:
            pts.append((p, float(t), y))
    fig, ax = plt.subplots(figsize=(10.6, 5.8))
    for p, t, y in pts:
        fr_ = p == "FRA"
        ax.plot([t], [y], "o", ms=8 if fr_ else 6, color=BLEU if fr_ else CLAIR,
                markeredgecolor=SURFACE, markeredgewidth=1.2, zorder=4 if fr_ else 3)
    dec = {"FRA": (-10, 6, "right"), "NOR": (-8, 0, "right"), "COL": (-8, 0, "right"),
           "IRL": (8, 0), "DEU": (8, -3), "LUX": (-8, 2, "right"), "AUS": (8, 0),
           "USA": (8, -9), "HUN": (8, 0), "CHL": (8, 5), "NLD": (-6, 9, "right"),
           "GBR": (-8, -4, "right"),
           "LVA": (8, 0), "EST": (8, 0), "ITA": (8, -3), "JPN": (8, 4), "CZE": (8, -4),
           "PRT": (8, 4)}
    for p, t, y in pts:
        if p in dec:
            o = dec[p]
            ax.annotate(NOMS.get(p, p), (t, y), xytext=o[:2], textcoords="offset points",
                        ha=o[2] if len(o) > 2 else "left", va="center",
                        fontsize=9.6 if p == "FRA" else 8.6,
                        color=BLEU if p == "FRA" else GRIS,
                        fontweight="bold" if p == "FRA" else "normal", path_effects=HALO)
    ax.set_xlim(8, 37)
    ax.set_ylim(0, 13)
    ax.xaxis.set_major_formatter(PCT)
    ax.yaxis.set_major_formatter(PCT)
    ax.set_xlabel("taux statutaire de l'impôt sur les sociétés")
    ax.set_ylabel("recettes d'impôt sur les sociétés, en % du PIB")
    grille(ax)
    ax.grid(axis="x", color="#ECECEC", lw=0.6, zorder=0)
    titre(ax, "Un taux élevé ne fait pas une recette élevée",
          "Taux statutaire et recettes de l'impôt sur les sociétés, pays de l'OCDE, 2023.")
    fin(fig, "r3_is_taux_et_recettes.png",
        "Sources : Tax Foundation pour les taux, OCDE Revenue Statistics (catégorie 1200) pour les "
        "recettes.",
        "Note : la recette dépend de la part des profits dans l'économie, de la taille du secteur "
        "des sociétés et de l'étroitesse de l'assiette autant que du taux ; la Norvège taxe ses "
        "profits pétroliers, l'Irlande héberge les bénéfices de multinationales. Le graphique "
        "n'établit donc aucune relation causale. Il montre seulement qu'en 2023 la France combinait un "
        "taux situé au treizième rang sur trente-huit et une recette au septième rang en partant du "
        "bas.")


# --------------------------------------- r4 : ce que valent les amortissements
def r4():
    actifs = [("machines_cost_recovery", "Machines"), ("buildings_cost_recovery", "Bâtiments"),
              ("intangibles_cost_recovery", "Incorporels")]
    fig, ax = plt.subplots(figsize=(10.6, 4.6))
    for i, (var, lab) in enumerate(actifs):
        y = len(actifs) - 1 - i
        vals = {p: 100 * v for p in IDX if (v := idx(p, var)) is not None}
        ax.plot([min(vals.values()), max(vals.values())], [y, y], color="#E3E5E8", lw=7,
                solid_capstyle="round", zorder=1)
        for p, v in vals.items():
            if p != "FRA":
                ax.plot([v], [y], "o", ms=6, color=CLAIR, markeredgecolor=SURFACE,
                        markeredgewidth=0.8, zorder=2)
        m = st.mean(vals.values())
        ax.plot([m, m], [y - 0.24, y + 0.24], color=INK2, lw=2.2, zorder=3)
        ax.text(m, y - 0.36, f"moyenne {fr(m)}", ha="center", va="top", fontsize=8.6, color=INK2)
        f = vals["FRA"]
        ax.plot([f], [y], "o", ms=10, color=BLEU, markeredgecolor=SURFACE, markeredgewidth=1.6,
                zorder=4)
        ax.text(f, y + 0.3, f"France {fr(f)}", ha="center", va="bottom", fontsize=9.4,
                color=BLEU, fontweight="bold", path_effects=HALO)
        ax.text(-3, y, lab, ha="right", va="center", fontsize=10, color=INK)
    ax.set_xlim(0, 104)
    ax.set_ylim(-0.75, len(actifs) - 0.3)
    ax.set_yticks([])
    ax.set_xticks([0, 20, 40, 60, 80, 100], ["0 €", "20 €", "40 €", "60 €", "80 €", "100 €"])
    ax.spines["left"].set_visible(False)
    grille(ax, "x")
    titre(ax, "Les amortissements français ne sont pas le problème",
          "Valeur actuelle des déductions fiscales pour 100 € investis, 38 pays de l'OCDE, 2025.")
    fin(fig, "r4_amortissements.png", SRC_TF,
        "Lecture : pour 100 € dépensés pour acquérir un actif incorporel, un brevet par exemple, "
        "les déductions fiscales autorisées en France, étalées sur cinq ans, valent 87 € "
        "aujourd'hui ; 100 € correspondrait à une déduction immédiate. Chaque point est un pays ; "
        "les déductions sont actualisées à 7,5 % par an, hypothèse de la Tax Foundation.")


# --------------------------------------- r5 : taxes sur la masse salariale
def r5():
    pts = sorted(((rev(p, "T_3000"), p) for p in pays_ocde() if (rev(p, "T_3000") or 0) > 0.05),
                 reverse=True)
    oe = rev("OECD_REP", "T_3000")
    fig, ax = plt.subplots(figsize=(10.6, 5.0))
    x = range(len(pts))
    ax.bar(list(x), [v for v, _ in pts], width=0.66, zorder=2,
           color=[BLEU if p == "FRA" else CLAIR for _, p in pts])
    for i, (v, p) in enumerate(pts):
        ax.text(i, v + 0.07, fr(v, 1), ha="center", fontsize=8.6, path_effects=HALO, zorder=5,
                color=BLEU if p == "FRA" else INK2, fontweight="bold" if p == "FRA" else "normal")
    ax.axhline(oe, color=GRIS, lw=1.1, ls=(0, (4, 3)), zorder=1)
    ax.text(len(pts) - 0.6, 1.15, f"moyenne OCDE {fr(oe, 2)}", ha="right", fontsize=9,
            color=GRIS)
    ax.annotate("", xy=(len(pts) - 1.2, oe + 0.03), xytext=(len(pts) - 1.2, 1.08),
                arrowprops=dict(arrowstyle="->", color=GRIS, lw=0.8))
    fig.subplots_adjust(bottom=0.24)
    ax.set_xticks(list(x), [NOMS.get(p, p) for _, p in pts], rotation=45, ha="right", fontsize=9)
    for t, (_, p) in zip(ax.get_xticklabels(), pts):
        if p == "FRA":
            t.set_color(BLEU)
            t.set_fontweight("bold")
    ax.set_ylim(0, 6)
    ax.yaxis.set_major_formatter(PCT)
    grille(ax)
    titre(ax, "La France est troisième de l'OCDE pour les taxes sur la masse salariale",
          "Taxes assises sur la masse salariale, hors cotisations sociales, en % du PIB, 2023. "
          "Pays où elles dépassent 0,05 point.")
    fin(fig, "r5_masse_salariale.png", SRC_REV + " Catégorie 3000.",
        "Note : ces prélèvements ne sont pas des cotisations, puisqu'ils n'ouvrent pas de droits "
        "proportionnels aux sommes versées. En France, ce sont pour l'essentiel la taxe sur les "
        "salaires, le versement mobilité et les contributions à la formation professionnelle et à "
        "l'apprentissage. En Suède, c'est la part des prélèvements patronaux qui n'ouvre aucun "
        "droit.")


# ------------------------------------- r6 : taux supérieur de l'IR et seuil
def r6():
    d = [x for x in lire("taux_superieur_et_seuil.csv") if x["annee"] == "2025" and x["taux"]
         and x["seuil_x_salaire_moyen"] and x["code"] != "OECD_REP"]
    fig, ax = plt.subplots(figsize=(10.6, 5.8))
    for x in d:
        t, s = float(x["taux"]), float(x["seuil_x_salaire_moyen"])
        fr_ = x["code"] == "FRA"
        ax.plot([s], [t], "o", ms=8.5 if fr_ else 6, color=BLEU if fr_ else CLAIR,
                markeredgecolor=SURFACE, markeredgewidth=1.2, zorder=4 if fr_ else 3)
    dec = {"FRA": (-10, 0, "right"), "DNK": (8, 4), "BEL": (-8, 0, "right"), "AUT": (8, 3),
           "DEU": (8, -4), "GBR": (8, 0), "USA": (8, 0), "ESP": (8, 4), "PRT": (8, -6),
           "SWE": (8, 5), "JPN": (8, 0), "NLD": (8, 1), "ITA": (8, -6), "EST": (8, 0),
           "IRL": (-8, -2, "right"), "CHL": (8, 0), "CZE": (8, 0)}
    for x in d:
        if x["code"] in dec:
            o = dec[x["code"]]
            ax.annotate(x["pays"], (float(x["seuil_x_salaire_moyen"]), float(x["taux"])), xytext=o[:2],
                        textcoords="offset points", ha=o[2] if len(o) > 2 else "left", va="center",
                        fontsize=9.6 if x["code"] == "FRA" else 8.6,
                        color=BLEU if x["code"] == "FRA" else GRIS,
                        fontweight="bold" if x["code"] == "FRA" else "normal", path_effects=HALO)
    ax.set_xscale("log")
    ax.set_xlim(0.6, 40)
    ax.set_xticks([1, 2, 5, 10, 20], ["1 fois", "2 fois", "5 fois", "10 fois", "20 fois"])
    ax.minorticks_off()
    ax.set_ylim(10, 62)
    ax.yaxis.set_major_formatter(PCT)
    ax.set_xlabel("revenu à partir duquel s'applique le taux supérieur, en multiple du salaire moyen "
                  "(échelle logarithmique)")
    grille(ax)
    titre(ax, "Le taux supérieur français est élevé, mais ne concerne presque personne",
          "Taux marginal supérieur de l'impôt sur le revenu, prélèvements assimilés compris, et "
          "seuil d'application, pays de l'OCDE, 2025.")
    fin(fig, "r6_taux_superieur_et_seuil.png",
        "Source : OCDE, base de données fiscale, taux statutaire supérieur de l'impôt sur le revenu "
        "et seuil d'application (DSD_TAX_PIT, mesures TS_PIT et TS_PIT_TH).",
        "Note : la Belgique et le Danemark appliquent un taux comparable au taux français à partir "
        "d'un revenu proche du salaire moyen ; la France l'applique à partir de treize fois ce "
        "salaire. Le taux marginal "
        "qui pèse sur un grand nombre de salariés français n'est donc pas celui-ci, mais celui du "
        "bas de l'échelle (figure du module sur le travail).")


# ------------------------------------------------ r7 : TVA, taux et assiette
def r7():
    pts = [(p, idx(p, "vat_rate"), 100 * idx(p, "vat_base")) for p in IDX
           if idx(p, "vat_rate") and idx(p, "vat_base")]
    mt = st.mean(t for _, t, _ in pts)
    mb = st.mean(b for _, _, b in pts)
    fig, ax = plt.subplots(figsize=(10.6, 5.8))
    ax.axvline(mt, color="#E3E5E8", lw=1.2, zorder=1)
    ax.axhline(mb, color="#E3E5E8", lw=1.2, zorder=1)
    ax.text(mt + 0.2, 101, f"taux moyen {fr(mt, 1)} %", fontsize=8.6, color=GRIS, va="top")
    ax.text(5.3, mb + 1.2, f"assiette moyenne {fr(mb)} %", fontsize=8.6, color=GRIS)
    for p, t, b in pts:
        fr_ = p == "FRA"
        ax.plot([t], [b], "o", ms=8.5 if fr_ else 6, color=BLEU if fr_ else CLAIR,
                markeredgecolor=SURFACE, markeredgewidth=1.2, zorder=4 if fr_ else 3)
    dec = {"FRA": (9, -2), "NZL": (8, 0), "LUX": (8, 0), "EST": (8, 3), "DNK": (8, 3),
           "ITA": (2, -11, "center"), "GBR": (-8, 0, "right"), "MEX": (8, 0), "CHE": (8, 0),
           "JPN": (8, 3), "DEU": (-8, 0, "right"), "HUN": (8, 0), "POL": (8, 0), "GRC": (8, 0),
           "BEL": (-8, -4, "right"), "AUT": (8, 3), "SWE": (-8, 0, "right"), "CAN": (8, 0)}
    for p, t, b in pts:
        if p in dec:
            o = dec[p]
            ax.annotate(NOMS.get(p, IDX[p]["pays"]), (t, b), xytext=o[:2], textcoords="offset points",
                        ha=o[2] if len(o) > 2 else "left", va="center",
                        fontsize=9.6 if p == "FRA" else 8.6, color=BLEU if p == "FRA" else GRIS,
                        fontweight="bold" if p == "FRA" else "normal", path_effects=HALO)
    ax.set_xlim(4, 29)
    ax.set_ylim(25, 105)
    ax.xaxis.set_major_formatter(PCT)
    ax.yaxis.set_major_formatter(PCT)
    ax.set_xlabel("taux normal de TVA")
    ax.set_ylabel("ratio de recettes de TVA")
    grille(ax)
    titre(ax, "La TVA française a un taux moyen et une assiette plus étroite que la moyenne",
          "Taux normal et ratio de recettes de TVA (part de la consommation effectivement taxée au "
          "taux normal), pays de l'OCDE.")
    fin(fig, "r7_tva_taux_et_assiette.png", SRC_TF + " Ratio de recettes calculé par l'OCDE.",
        "Note : le ratio rapporte les recettes de TVA à ce qu'elles seraient si toute la "
        "consommation finale était taxée au taux normal. Il mesure ensemble les taux réduits, les "
        "exonérations et la fraude. La Nouvelle-Zélande, qui taxe presque tout à 15 %, approche "
        "100 % ; la France est à 51 %, sous la moyenne de 55 %, avec un taux normal de 20 % proche "
        "de la moyenne et inférieur à la médiane de 21 %.")


# --------------------------------- r8 : dividendes et plus-values au sommet
R8_PAYS = {"FRA", "DEU", "AUT", "BEL", "DNK", "ESP", "EST", "USA", "FIN", "IRL", "ITA", "JPN",
           "NOR", "NLD", "POL", "PRT", "GBR", "SWE", "CHE", "CAN", "KOR"}


def r8():
    # Vingt pays de comparaison et la France : les trente-huit pays ne tiennent pas lisiblement
    # à la largeur d'une page ; la moyenne de l'OCDE est donnée en note.
    pts = sorted(((idx(p, "dividends_rate"), idx(p, "capital_gains_rate"), p) for p in IDX
                  if p in R8_PAYS and idx(p, "dividends_rate") is not None
                  and idx(p, "capital_gains_rate") is not None),
                 key=lambda t: (t[0], t[1]))
    fig, ax = plt.subplots(figsize=(10.6, 7.2))
    for i, (dv, pv, p) in enumerate(pts):
        fr_ = p == "FRA"
        c = BLEU if fr_ else "#8C96A6"
        ax.plot([100 * min(dv, pv), 100 * max(dv, pv)], [i, i], color="#D5D9DF" if not fr_ else BLEU_CLAIR,
                lw=2.2, zorder=1)
        ax.plot([100 * pv], [i], "o", ms=9.5 if fr_ else 8, color=SURFACE, zorder=3,
                markeredgecolor=c, markeredgewidth=1.6)
        ax.plot([100 * dv], [i], "o", ms=5.5 if fr_ else 4.5, color=c, zorder=4,
                markeredgecolor=c, markeredgewidth=0)
    ax.set_yticks(range(len(pts)), [NOMS.get(p, IDX[p]["pays"]) for *_, p in pts], fontsize=9)
    for t, (*_, p) in zip(ax.get_yticklabels(), pts):
        if p == "FRA":
            t.set_color(BLEU)
            t.set_fontweight("bold")
    ax.plot([], [], "o", ms=4.5, color="#8C96A6", label="dividendes")
    ax.plot([], [], "o", ms=8, color=SURFACE, markeredgecolor="#8C96A6", markeredgewidth=1.6,
            label="plus-values sur actions")
    leg = ax.legend(loc="lower right", fontsize=9, frameon=False)
    ax.set_xlim(-1, 60)
    ax.set_ylim(-0.8, len(pts) - 0.2)
    ax.xaxis.set_major_formatter(PCT)
    grille(ax, "x")
    ax.spines["left"].set_visible(False)
    ax.tick_params(left=False)
    titre(ax, "Le revenu de l'épargne en actions est taxé en France au-dessus de la moyenne",
          "Taux personnel supérieur sur les dividendes et sur les plus-values de cession d'actions, "
          "pays de l'OCDE.")
    fin(fig, "r8_dividendes_plus_values.png", SRC_TF,
        "Note : vingt pays de comparaison. Un point plein dans un cercle signale deux taux égaux. "
        "Taux au niveau de "
        "l'actionnaire seulement ; l'impôt déjà payé par la société "
        "s'ajoute pour les dividendes (figure de la cascade). Le taux français de 34 % est le "
        "prélèvement forfaitaire unique de 30 % augmenté de la contribution sur les hauts revenus. "
        "Moyenne de l'OCDE : 25 % sur les dividendes, 20 % sur les plus-values.")


# --------------------------- r9 : foncier récurrent contre droits sur les transactions
def r9():
    pts = [(p, rev(p, "T_4100"), rev(p, "T_4400")) for p in pays_ocde()
           if rev(p, "T_4100") is not None and rev(p, "T_4400") is not None]
    o1, o2 = rev("OECD_REP", "T_4100"), rev("OECD_REP", "T_4400")
    fig, ax = plt.subplots(figsize=(10.6, 5.8))
    ax.plot([0, 3.0], [0, 3.0 * o2 / o1], color="#E3E5E8", lw=1.3, zorder=1)
    ax.text(2.95, 3.0 * o2 / o1 + 0.05, "même partage que\nla moyenne OCDE", ha="right",
            va="bottom", fontsize=8.6, color=GRIS, linespacing=1.35)
    for p, a, b in pts:
        fr_ = p == "FRA"
        ax.plot([a], [b], "o", ms=8.5 if fr_ else 6, color=BLEU if fr_ else CLAIR,
                markeredgecolor=SURFACE, markeredgewidth=1.2, zorder=4 if fr_ else 3)
    ax.plot([o1], [o2], "D", ms=7, color=GRIS, zorder=4, markeredgecolor=SURFACE)
    ax.annotate("moyenne OCDE", (o1, o2), xytext=(8, -2), textcoords="offset points",
                fontsize=8.8, color=GRIS, fontweight="bold", va="center", path_effects=HALO)
    dec = {"FRA": (9, 0), "GBR": (8, 0), "USA": (8, 0), "CAN": (8, 0), "KOR": (8, 0),
           "AUS": (8, 0), "ITA": (8, 0), "BEL": (8, 0), "ESP": (8, 4), "PRT": (8, 0),
           "DEU": (8, 0), "TUR": (8, 0), "LUX": (8, 0), "JPN": (8, 0), "DNK": (8, -4),
           "NZL": (8, 0), "GRC": (8, 3), "COL": (8, 0), "IRL": (8, 3), "AUT": (8, 0)}
    for p, a, b in pts:
        if p in dec:
            o = dec[p]
            ax.annotate(NOMS.get(p, p), (a, b), xytext=o[:2], textcoords="offset points",
                        ha="left", va="center", fontsize=9.6 if p == "FRA" else 8.6,
                        color=BLEU if p == "FRA" else GRIS,
                        fontweight="bold" if p == "FRA" else "normal", path_effects=HALO)
    ax.set_xlim(0, 3.1)
    ax.set_ylim(0, 1.75)
    ax.xaxis.set_major_formatter(PCT)
    ax.yaxis.set_major_formatter(PCT)
    ax.set_xlabel("impôts récurrents sur la propriété immobilière, en % du PIB")
    ax.set_ylabel("droits sur les transactions, en % du PIB")
    grille(ax)
    ax.grid(axis="x", color="#ECECEC", lw=0.6, zorder=0)
    titre(ax, "La France taxe deux fois plus que la moyenne la détention et la transaction",
          "Impôts récurrents sur la propriété immobilière et droits sur les transactions "
          "financières et en capital, pays de l'OCDE, 2023.")
    fin(fig, "r9_detention_et_transaction.png", SRC_REV + " Catégories 4100 et 4400.",
        "Note : la France est à 1,9 % du PIB pour la détention et 0,7 % pour les transactions, "
        "contre 0,95 et 0,37 en moyenne ; le partage entre les deux est donc celui de la moyenne. "
        "Ce qui distingue la France est le niveau des droits sur les transactions et l'assiette de "
        "l'impôt récurrent, établie sur des valeurs locatives de 1970.")


# --------------------------------------------- r10 : successions et donations
def r10():
    pts = sorted(((rev(p, "T_4300"), p) for p in pays_ocde() if (rev(p, "T_4300") or 0) >= 0.05),
                 reverse=True)
    oe = rev("OECD_REP", "T_4300")
    fig, ax = plt.subplots(figsize=(10.6, 4.8))
    x = range(len(pts))
    ax.bar(list(x), [v for v, _ in pts], width=0.64, zorder=2,
           color=[BLEU if p == "FRA" else CLAIR for _, p in pts])
    for i, (v, p) in enumerate(pts):
        ax.text(i, v + 0.015, fr(v, 2), ha="center", fontsize=8.4, path_effects=HALO, zorder=5,
                color=BLEU if p == "FRA" else INK2, fontweight="bold" if p == "FRA" else "normal")
    ax.axhline(oe, color=GRIS, lw=1.1, ls=(0, (4, 3)), zorder=1)
    ax.text(len(pts) - 0.6, 0.36, f"moyenne OCDE {fr(oe, 2)}", ha="right", fontsize=9,
            color=GRIS)
    ax.annotate("", xy=(len(pts) - 1.4, oe + 0.01), xytext=(len(pts) - 1.4, 0.34),
                arrowprops=dict(arrowstyle="->", color=GRIS, lw=0.8))
    fig.subplots_adjust(bottom=0.24)
    ax.set_xticks(list(x), [NOMS.get(p, p) for _, p in pts], rotation=45, ha="right", fontsize=9)
    for t, (_, p) in zip(ax.get_xticklabels(), pts):
        if p == "FRA":
            t.set_color(BLEU)
            t.set_fontweight("bold")
    ax.set_ylim(0, 0.9)
    ax.yaxis.set_major_formatter(PCT)
    grille(ax)
    titre(ax, "Aucun pays de l'OCDE ne prélève autant que la France sur les successions",
          "Impôts sur les successions, héritages et donations, en % du PIB, 2023. Pays où ils "
          "atteignent 0,05 point.")
    fin(fig, "r10_successions.png", SRC_REV + " Catégorie 4300.",
        "Note : le rendement français est cinq fois la moyenne de l'OCDE alors que le barème "
        "s'applique à une assiette réduite par plusieurs régimes dérogatoires. Une réforme de "
        "l'impôt sur les transmissions n'a donc pas besoin de rapporter davantage : elle a besoin "
        "d'une assiette plus large et de taux plus bas.")


# ------------------------------------- r11 : le détail des 77 milliards
def r11():
    rows = []
    with open(HERE / "donnees" / "classification_prelevements.csv", encoding="utf-8") as f:
        for x in csv.DictReader(f):
            if x["intrant"] == "oui" and x["correctif"] == "non":
                rows.append((float(x["meur"]) / 1000, x["nom"]))
    rows.sort(reverse=True)
    tot = sum(v for v, _ in rows)
    top = rows[:9]
    autres = sum(v for v, _ in rows[9:])
    court = {
        "Taxes sur les salaires": "Taxe sur les salaires",
        "Versement mobilité": "Versement mobilité",
        "Contributions des entreprises à la formation professionnelle et à l'apprentissage":
            "Formation professionnelle et apprentissage",
        "Cotisation foncière des entreprises": "Cotisation foncière des entreprises",
        "Contribution sociale de solidarité des sociétés": "Contribution sociale de solidarité (C3S)",
        "Cotisation patronale pour le FNAL (Fonds national d'aide au logement)":
            "Contribution au Fonds national d'aide au logement",
        "Part sur les salaires": "Ligne sans libellé, assise sur les salaires",
        "Impositions forfaitaires sur les entreprises de réseaux":
            "Imposition forfaitaire sur les entreprises de réseaux (IFER)",
    }
    lab = [court.get(n, n if len(n) < 52 else n[:50] + "…") for _, n in top] + \
          [f"{len(rows) - 9} autres prélèvements"]
    vals = [v for v, _ in top] + [autres]
    fig, ax = plt.subplots(figsize=(10.6, 5.4))
    y = list(range(len(vals)))[::-1]
    ax.barh(y, vals, height=0.64, color=[BLEU] * len(top) + [CLAIR], zorder=2)
    for yy, v in zip(y, vals):
        ax.text(v + 0.25, yy, fr(v, 1), va="center", fontsize=9.4, color=INK)
    ax.set_yticks(y, lab, fontsize=9.3)
    ax.set_xlim(0, 21)
    ax.set_xticks([0, 5, 10, 15, 20], ["0", "5", "10", "15", "20 Md€"])
    grille(ax, "x")
    ax.spines["left"].set_visible(False)
    ax.tick_params(left=False)
    titre(ax, f"{fr(tot, 0)} milliards prélevés sur ce qui sert à produire, sans rien corriger",
          "Prélèvements français assis sur un facteur de production et sans fonction corrective, "
          "en milliards d'euros, 2024.")
    fin(fig, "r11_77_milliards.png",
        "Source : Eurostat, National Tax List France 2024 ; classement par l'auteur, prélèvement "
        "par prélèvement (fichier donnees/classification_prelevements.csv).",
        "Note : sont retenus les prélèvements dont l'assiette est un intrant — masse salariale, "
        "local, chiffre d'affaires, valeur ajoutée — et qui ne corrigent aucune externalité. Les "
        "taxes sur l'énergie, assises elles aussi sur un intrant mais à visée corrective, en sont "
        "exclues (42 Md€).")


# --------------------- r12 : la structure française rangée selon le classement de l'OCDE
def r12():
    def cat(code):
        g = {
            "immo": rev(code, "T_4100"),
            "conso": rev(code, "T_5000"),
            "autres_patr": rev(code, "T_4000") - rev(code, "T_4100"),
            "revenu": rev(code, "T_1100") + rev(code, "T_2000") + rev(code, "T_3000"),
            "is": rev(code, "T_1200"),
        }
        return g
    lab = [("immo", "immobilier\n(récurrent)"), ("conso", "consommation"),
           ("autres_patr", "autres impôts\nsur le patrimoine"),
           ("revenu", "revenus, cotisations,\nmasse salariale"),
           ("is", "bénéfices\ndes sociétés")]
    f, o = cat("FRA"), cat("OECD_REP")
    fig, ax = plt.subplots(figsize=(10.6, 5.6))
    x = list(range(len(lab)))
    w = 0.36
    ax.bar([i - w / 2 for i in x], [f[k] for k, _ in lab], width=w * 0.94, color=BLEU, zorder=2,
           label="France")
    ax.bar([i + w / 2 for i in x], [o[k] for k, _ in lab], width=w * 0.94, color=CLAIR, zorder=2,
           label="moyenne OCDE")
    for i, (k, _) in enumerate(lab):
        ax.text(i - w / 2, f[k] + 0.35, fr(f[k], 1), ha="center", fontsize=9.6, color=BLEU,
                fontweight="bold")
        ax.text(i + w / 2, o[k] + 0.35, fr(o[k], 1), ha="center", fontsize=9.2, color=INK2)
    ax.set_xticks(x, [l for _, l in lab], fontsize=9.4)
    ax.set_ylim(0, 31)
    ax.yaxis.set_major_formatter(PCT)
    grille(ax)
    ax.annotate("", xy=(4.45, 29.2), xytext=(-0.45, 29.2),
                arrowprops=dict(arrowstyle="->", color=INK2, lw=1.1))
    ax.text(2, 29.8, "classement de l'OCDE : du moins au plus défavorable à la croissance",
            ha="center", fontsize=9.3, color=INK2, style="italic")
    leg = ax.legend(loc="upper left", bbox_to_anchor=(0.0, 0.9), fontsize=9.5, frameon=False)
    titre(ax, "La France s'écarte de la moyenne surtout dans l'avant-dernière catégorie du classement",
          "Recettes en % du PIB, France et moyenne de l'OCDE, 2023, rangées selon le classement "
          "« fiscalité et croissance » de l'OCDE.")
    fin(fig, "r12_classement_ocde.png",
        "Sources : classement de Johansson, Heady, Arnold, Brys et Vartia, OCDE, document de travail "
        "n° 620, 2008 ; recettes OCDE, Revenue Statistics, catégories 1100, 1200, 2000, 3000, 4000, "
        "4100 et 5000.",
        "Note : les catégories 1300 et 6000, non classées, sont omises. Le classement vient de "
        "régressions sur un panel de vingt-et-un pays ; son ordre n'est pas robuste à tous les "
        "changements de spécification (Xing, 2012), et ses auteurs jugent eux-mêmes l'ampleur des "
        "effets estimés plus élevée que ce à quoi on peut raisonnablement s'attendre.")


if __name__ == "__main__":
    for f in (r1, r2, r3, r4, r5, r6, r7, r8, r9, r10, r11, r12):
        f()
