"""
Les figures d'ensemble sur la situation fiscale française aujourd'hui.

    python graphiques_situation.py

s1  la carte des 1 274,9 Md€, un rectangle par prélèvement
s2  le coin fiscal sur le travail, décomposé
s3  l'entreprise : impôt sur les bénéfices dans la moyenne, prélèvements d'amont hors norme
s4  le taux global de prélèvement depuis 1995
"""
import csv
from pathlib import Path
from textwrap import wrap

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

from graphiques import (ANS, BLEU, GRID, GRIS, HALO, INK, INK2, MUTED, NOMS, OCRE, PAL, PCT,
                        SURFACE, TOTAL, VERT, fin, grille, panneau, pc, titre)

HERE = Path(__file__).resolve().parent
DON = HERE / "donnees"


def lire(nom):
    with open(DON / nom) as f:
        return list(csv.DictReader(f))


# ------------------------------------------------------------------ pavage squarifié
def pavage(valeurs, x, y, dx, dy):
    """Découpe le rectangle (x, y, dx, dy) en sous-rectangles proportionnels aux valeurs.

    Algorithme squarifié : on remplit par rangées en ajoutant une valeur tant que cela
    améliore le rapport d'aspect le plus défavorable de la rangée. On obtient des
    rectangles proches du carré, donc lisibles, plutôt que des lamelles.
    """
    total = sum(valeurs)
    if total <= 0 or dx <= 0 or dy <= 0:
        return []
    aire = dx * dy
    v = [max(val, 1e-9) * aire / total for val in valeurs]
    out, i = [], 0

    def pire(rang, cote):
        s, mn = sum(rang), min(rang)
        if s <= 0 or cote <= 0 or mn <= 0:
            return float("inf")
        return max(cote * cote * max(rang) / (s * s), s * s / (cote * cote * mn))

    while i < len(v):
        cote = min(dx, dy)
        rang, j = [v[i]], i + 1
        while j < len(v) and pire(rang + [v[j]], cote) <= pire(rang, cote):
            rang.append(v[j])
            j += 1
        s = sum(rang)
        if dx >= dy:
            larg, yy = s / dy, y
            for val in rang:
                h = val / larg
                out.append((x, yy, larg, h))
                yy += h
            x, dx = x + larg, dx - larg
        else:
            haut, xx = s / dx, x
            for val in rang:
                w = val / haut
                out.append((xx, y, w, haut))
                xx += w
            y, dy = y + haut, dy - haut
        i = j
    return out


# ---------------------------------------------- s1 : la carte des prélèvements français
ASSIETTES = [
    ("travail", "Le travail", "#003399", None),
    ("conso_menages", "La consommation des ménages", "#1f7a4d", None),
    ("revenu_global", "Le revenu, toutes sources", "#c79100", None),
    ("profit", "Le profit des sociétés", "#1f6b7a", None),
    ("stock_capital", "Le stock de patrimoine", "#5b3f8c", None),
    ("energie", "L'énergie", "#993333", None),
    ("intrant_entreprises", "Les intrants des entreprises", "#a85b00", None),
    ("transmission", "Les transmissions", "#7a63a8", None),
    ("transaction", "Les transactions", "#4a6eb6", None),
    ("revenu_capital", "Les revenus du capital", "#40806a", None),
    ("rente", "Les rentes", "#6b6b6b", None),
    ("autre", "Autre", "#b0b0b0", None),
]


def _eclaircir(hexa, f):
    """Mélange une couleur avec du blanc : f = 0 laisse la couleur, f = 1 donne du blanc."""
    r, g, b = (int(hexa[i:i + 2], 16) for i in (1, 3, 5))
    m = lambda c: int(round(c + (255 - c) * f))
    return f"#{m(r):02x}{m(g):02x}{m(b):02x}"


def s1():
    lignes = lire("classification_prelevements.csv")
    par = {}
    for r in lignes:
        if float(r["meur"]) > 0:
            par.setdefault(r["assiette"], []).append((r["nom"], float(r["meur"]) / 1000))
    total = sum(float(r["meur"]) for r in lignes) / 1000

    blocs = [(code, lab, c1, sorted(par.get(code, []), key=lambda t: -t[1]))
             for code, lab, c1, _ in ASSIETTES if par.get(code)]
    blocs.sort(key=lambda b: -sum(m for _, m in b[3]))

    fig, ax = plt.subplots(figsize=(13.6, 7.8))
    W, H = 100.0, 100.0
    rects = pavage([sum(m for _, m in b[3]) for b in blocs], 0, 0, W, H)
    muets = []

    for (code, lab, c1, items), (x, y, dx, dy) in zip(blocs, rects):
        somme = sum(m for _, m in items)
        entete = dx >= 13.5 and dy >= 8
        detail = entete and somme >= 40
        inner = pavage([m for _, m in items], x, y, dx, dy)
        n = max(len(items) - 1, 1)
        for k, ((nom, mnt), (ix, iy, idx, idy)) in enumerate(zip(items, inner)):
            ax.add_patch(Rectangle((ix, iy), idx, idy, zorder=2, lw=0.8, edgecolor=SURFACE,
                                   facecolor=_eclaircir(c1, 0.42 * k / n)))
            if not detail or idx < 9.5 or idy < 6.5:
                continue
            # décaler l'étiquette si elle tomberait sous l'en-tête du bloc
            ly, dec = iy + idy / 2, 0.0
            if ly > y + dy - 8.5 and ix < x + 0.66 * dx:
                if idy < 17:
                    continue
                dec = -5.5
            court = nom.split(" (")[0].split(" y compris")[0]
            lim = max(int(idx * 1.85), 6)
            if len(court) > lim:
                court = court[:lim - 1].rstrip() + "…"
            ax.text(ix + idx / 2, ly + 1.9 + dec, f"{mnt:.0f}", ha="center", va="center",
                    fontsize=10.5, color="white", fontweight="bold", zorder=4)
            ax.text(ix + idx / 2, ly - 1.3 + dec, court, ha="center", va="center",
                    fontsize=7.4, color="white", zorder=4)
        ax.add_patch(Rectangle((x, y), dx, dy, facecolor="none", edgecolor=SURFACE, lw=2.8,
                               zorder=5))
        if entete:
            tete = "\n".join(wrap(lab, max(int(dx / 0.74), 9))) + f"\n{somme:.0f} Md€"
            ax.text(x + 1.1, y + dy - 1.2, tete, ha="left", va="top",
                    fontsize=9.5, color="white", fontweight="bold", zorder=6, linespacing=1.35)
        else:
            muets.append(f"{lab.lower()} {somme:.0f}")

    ax.set_xlim(0, W)
    ax.set_ylim(0, H)
    ax.axis("off")
    fig.subplots_adjust(left=0.02, right=0.98, top=0.90, bottom=0.02)
    reste = (" Faute de place, quatre blocs ne portent pas leur nom : "
             + ", ".join(muets) + " Md€.") if muets else ""
    titre(ax, "Les prélèvements obligatoires français de 2024, un rectangle par prélèvement",
          "Surface proportionnelle au rendement ; montants en milliards d'euros.")
    fin(fig, "s1_carte_des_prelevements.png",
        "Sources : Eurostat, National Tax List France (table 0900 SEC 2010), mise à jour du "
        "21 juillet 2026 ; classement par assiette économique réelle de l'auteur, voir "
        "donnees/classification_prelevements.csv.",
        "Note : chaque prélèvement est rangé selon ce qu'il atteint en dernier ressort et non "
        "selon son étiquette comptable. Les 123 lignes totalisent 1 274,9 Md€ et se "
        "réconcilient exactement avec le total de comptabilité nationale." + reste)


# ---------------------------------------------------- s2 : le coin fiscal sur le travail
def s2():
    r = lire("coin_fiscal.csv")
    r = [x for x in r if x["code"] != "EU22OECD"]
    r.sort(key=lambda x: float(x["coin_total_pct_cout"]))
    y = list(range(len(r)))
    seg = [("impot_revenu_pct_cout", "Impôt sur le revenu", PAL[2]),
           ("cotis_salarie_pct_cout", "Cotisations salariales", PAL[0]),
           ("cotis_employeur_pct_cout", "Cotisations employeur", PAL[1])]

    fig, ax = plt.subplots(figsize=(11.6, 7.4))
    gauche = [0.0] * len(r)
    for cle, lab, c in seg:
        v = [float(x[cle]) for x in r]
        ax.barh(y, v, left=gauche, color=c, height=0.68, zorder=2, label=lab)
        for i, (g, val) in enumerate(zip(gauche, v)):
            if val > 4.2:
                ax.text(g + val / 2, i, f"{val:.0f}".replace(".", ","), ha="center",
                        va="center", fontsize=8.5, color="white", fontweight="bold", zorder=3)
        gauche = [g + val for g, val in zip(gauche, v)]
    for i, (x, t) in enumerate(zip(r, gauche)):
        fr = x["code"] == "FRA"
        ax.text(t + 0.6, i, f"{t:.0f} %".replace(".", ","), va="center", fontsize=9.5,
                color=BLEU if fr else INK, fontweight="bold")
    ax.set_yticks(y, [x["pays"] for x in r], fontsize=9.5)
    for t, x in zip(ax.get_yticklabels(), r):
        if x["code"] == "FRA":
            t.set_color(BLEU)
            t.set_fontweight("bold")
        elif x["code"] == "OECD_REP":
            t.set_style("italic")
        elif x["code"] == "DNK":
            t.set_fontweight("bold")
    ax.set_xlim(0, 60)
    ax.xaxis.set_major_formatter(PCT)
    grille(ax, "x")
    ax.spines["left"].set_visible(False)
    ax.tick_params(left=False)
    leg = ax.legend(loc="lower right", frameon=False, fontsize=9.5, handlelength=1.1)
    for t, (_, _, c) in zip(leg.get_texts(), seg):
        t.set_color(c)

    ax.text(42.5, 7.0, "La France prélève 47 % du coût du travail,\n"
                       "le Danemark 36 %. Mais le Danemark le fait\n"
                       "presque entièrement par l'impôt sur le revenu,\n"
                       "la France surtout par les cotisations employeur.",
            fontsize=9, color=INK2, linespacing=1.6, va="center", path_effects=HALO)
    titre(ax, "Coin fiscal sur le travail et sa composition, 2025",
          "Célibataire sans enfant au salaire moyen, en % du coût total du travail.")
    fin(fig, "s2_coin_fiscal.png",
        "Source : OCDE, Taxing Wages, indicateurs comparatifs, données 2025.",
        "Note : le coin fiscal mesure l'écart entre ce que paie l'employeur et ce que touche le "
        "salarié. L'OCDE publie l'impôt sur le revenu et les cotisations en pourcentage du "
        "salaire brut ; ils sont ici rapportés au coût du travail, afin que les trois "
        "composantes s'additionnent au coin.")


# ------------------------------------- s3 : l'entreprise, le bénéfice et ce qui vient avant
CORR = {"FRA": "FR", "DEU": "DE", "ITA": "IT", "ESP": "ES", "BEL": "BE", "AUT": "AT",
        "NLD": "NL", "SWE": "SE", "DNK": "DK", "POL": "PL", "PRT": "PT", "FIN": "FI",
        "CZE": "CZ", "HUN": "HU", "GRC": "EL", "EST": "EE", "IRL": "IE"}


def s3():
    e = [x for x in lire("eatr_societes.csv") if x["code"] in CORR]
    d29 = {x["code"]: pc(CORR[x["code"]], "D29", 2024) for x in e}
    e = [x for x in e if d29.get(x["code"]) is not None]

    fig, (a1, a2) = plt.subplots(1, 2, figsize=(12.8, 5.8))
    for ax, cle, src, tit, sous in (
        (a1, lambda x: float(x["eatr_pct"]), None,
         "Taux effectif moyen sur un investissement, 2025", None),
        (a2, lambda x: d29[x["code"]], None,
         "Autres impôts sur la production, en % du PIB, 2024", None),
    ):
        s = sorted(e, key=cle)
        y = list(range(len(s)))
        cou = [BLEU if x["code"] == "FRA" else "#C9CDD2" for x in s]
        ax.barh(y, [cle(x) for x in s], color=cou, height=0.72, zorder=2)
        for i, x in enumerate(s):
            v = cle(x)
            ax.text(v + max(cle(z) for z in s) * 0.015, i, f"{v:.1f}".replace(".", ","),
                    va="center", fontsize=8.8,
                    color=BLEU if x["code"] == "FRA" else INK2,
                    fontweight="bold" if x["code"] == "FRA" else "normal")
        ax.set_yticks(y, [x["pays"] for x in s], fontsize=9)
        for t, x in zip(ax.get_yticklabels(), s):
            if x["code"] == "FRA":
                t.set_color(BLEU)
                t.set_fontweight("bold")
        ax.set_xlim(0, max(cle(z) for z in s) * 1.16)
        ax.xaxis.set_major_formatter(PCT)
        grille(ax, "x")
        ax.spines["left"].set_visible(False)
        ax.tick_params(left=False)
        titre(ax, tit, sous)
    a2.text(0.98, 0.955, "La Suède classe ses cotisations patronales\nen impôts sur la "
            "production : son niveau n'est pas\ncomparable à celui des autres.",
            transform=a2.transAxes, ha="right", va="top", fontsize=8.5, color=MUTED,
            linespacing=1.5)
    fig.subplots_adjust(wspace=0.34)
    fin(fig, "s3_entreprises.png",
        "Sources : OCDE, Corporate Tax Statistics, taux effectifs d'imposition, scénario aux "
        "taux d'intérêt et d'inflation propres à chaque pays ; Eurostat gov_10a_taxag, "
        "catégorie D29.",
        "Note : à gauche, taux effectif moyen calculé selon la méthode Devereux-Griffith sur un "
        "investissement composite. À droite, impôts sur la production hors TVA et hors droits "
        "sur les importations. La Suède classe ses cotisations patronales dans cette catégorie, "
        "ce qui explique son niveau.")


# ------------------------------------------------- s4 : le taux global de prélèvement
def s4():
    choix = [("FR", BLEU), ("DK", VERT), ("SE", OCRE), ("DE", GRIS),
             ("IT", PAL[6]), ("NL", PAL[4]), ("IE", "#b0b0b0")]
    fig, ax = plt.subplots(figsize=(11.4, 6.2))
    fins = []
    for p, c in choix:
        xs = [a for a in ANS if pc(p, TOTAL, a) is not None]
        ys = [pc(p, TOTAL, a) for a in xs]
        if not xs:
            continue
        ax.plot(xs, ys, color=c, lw=2.4 if p == "FR" else 1.5, zorder=3 if p == "FR" else 2,
                ls=(0, (5, 2)) if p == "IE" else "-")
        fins.append((ys[-1], NOMS[p], c, xs[-1]))
    fins.sort(reverse=True)
    pos, prec = [], None
    for v, nom, c, x in fins:
        yy = v if prec is None else min(v, prec - 1.15)
        pos.append((yy, nom, c, v))
        prec = yy
    for yy, nom, c, v in pos:
        ax.text(x + 0.45, yy, f"{nom}  {v:.1f}".replace(".", ","), va="center", fontsize=9.5,
                color=c, fontweight="bold" if nom == "France" else "normal")
    ax.set_xlim(1995, x + 6.2)
    ax.set_xticks([1995, 2000, 2005, 2010, 2015, 2020, 2024])
    ax.set_ylim(18, 50)
    ax.yaxis.set_major_formatter(PCT)
    grille(ax)
    titre(ax, "Impôts et cotisations sociales en % du PIB, 1995-2024",
          "Sept pays, hors cotisations imputées.")
    fin(fig, "s4_taux_global.png",
        "Source : Eurostat, gov_10a_taxag, secteur S13 et institutions européennes.",
        "Note : le niveau français monte de quatre points entre 2009 et 2017, puis revient à "
        "son point de départ. L'Irlande est en tireté parce que son ratio est perturbé par le "
        "dénominateur : le PIB bondit en 2015 sous l'effet de réimplantations d'actifs "
        "incorporels, sans qu'aucun impôt ait baissé.")


if __name__ == "__main__":
    s1(); s2(); s3(); s4()
