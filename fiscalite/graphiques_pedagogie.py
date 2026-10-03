"""
Figures de la partie III, les trois chapitres pédagogiques : la situation relative des
retraités, le partage des prélèvements sociaux entre salaires et pensions, et l'arithmétique
qui relie un impôt sur le stock à un taux sur le rendement.

    python graphiques_pedagogie.py
"""
import csv
from pathlib import Path

import matplotlib.pyplot as plt

from graphiques import BLEU, GRID, HALO, INK, INK2, MUTED, PAL, PCT, fin, grille, titre

HERE = Path(__file__).resolve().parent
DON = HERE / "donnees"


def lire(nom):
    with open(DON / nom) as f:
        return list(csv.DictReader(f))


# ------------------------------------------------------- p1 : la place des retraités
def p1():
    nv = lire("retraites_niveau_vie.csv")
    pv = {r["code"]: r for r in lire("pauvrete_age.csv")}
    garde = ["ES", "IT", "FR", "AT", "EU27_2020", "PL", "SE", "FI", "DE", "CZ", "DK", "NL", "BE"]
    sel = [r for r in nv if r["code"] in garde]
    sel.sort(key=lambda r: float(r["ratio_65plus_sur_ensemble"]))

    fig, (a1, a2) = plt.subplots(1, 2, figsize=(12.6, 5.4),
                                 gridspec_kw={"width_ratios": [1.15, 1]})

    y = range(len(sel))
    cou = [BLEU if r["code"] == "FR" else (MUTED if r["code"] == "EU27_2020" else "#C9CDD2")
           for r in sel]
    val = [float(r["ratio_65plus_sur_ensemble"]) * 100 for r in sel]
    a1.barh(list(y), val, color=cou, height=0.72, zorder=2)
    a1.set_yticks(list(y), [r["pays"] for r in sel], fontsize=9)
    for t, r in zip(a1.get_yticklabels(), sel):
        if r["code"] == "FR":
            t.set_color(BLEU)
            t.set_fontweight("bold")
    for i, (v, r) in enumerate(zip(val, sel)):
        gras = r["code"] in ("FR", "EU27_2020")
        a1.text(v + 1, i, f"{v:.0f}".replace(".", ","), va="center", fontsize=9,
                color=BLEU if r["code"] == "FR" else INK2,
                fontweight="bold" if gras else "normal")
    a1.axvline(100, color=INK, lw=0.9, ls=(0, (4, 3)), zorder=3)
    a1.text(101, 0, "parité avec l'ensemble\nde la population", fontsize=8.5,
            color=INK2, va="center")
    a1.set_xlim(0, 118)
    a1.set_xticks([0, 25, 50, 75, 100])
    grille(a1, "x")
    a1.spines["left"].set_visible(False)
    a1.tick_params(left=False)
    titre(a1, "Le niveau de vie des retraités français est proche\nde celui du reste du pays",
          "Revenu médian équivalent des 65 ans et plus, en % de celui\nde l'ensemble de la "
          "population, 2024")

    ages = [("moins_18", "Moins de 18 ans"), ("18_64", "18 à 64 ans"), ("65_plus", "65 ans et plus")]
    pays = [("FR", "France", BLEU), ("EU27_2020", "Union européenne", MUTED),
            ("DE", "Allemagne", PAL[1])]
    larg = 0.26
    for j, (code, nom, c) in enumerate(pays):
        xs = [i + (j - 1) * larg for i in range(3)]
        vs = [float(pv[code][a]) for a, _ in ages]
        a2.bar(xs, vs, width=larg * 0.92, color=c, zorder=2)
        for x, v in zip(xs, vs):
            a2.text(x, v + 0.5, f"{v:.1f}".replace(".", ","), ha="center", fontsize=8.5,
                    color=c, fontweight="bold" if code == "FR" else "normal")
        a2.bar([0], [0], color=c, label=nom)
    a2.set_xticks(range(3), [n for _, n in ages], fontsize=9.5)
    a2.set_ylim(0, 28)
    leg = a2.legend(loc="upper center", ncol=3, frameon=False, fontsize=9.5,
                    handlelength=1.1, columnspacing=1.4, borderpad=0.1)
    for t, (_, _, c) in zip(leg.get_texts(), pays):
        t.set_color(c)
        t.set_fontweight("bold")
    a2.yaxis.set_major_formatter(PCT)
    grille(a2)
    titre(a2, "La pauvreté française a changé d'âge",
          "Taux de pauvreté au seuil de 60 % du revenu médian, 2024")

    fig.subplots_adjust(wspace=0.28)
    fin(fig, "p1_retraites_niveau_vie.png",
        "Source : Eurostat, ilc_pnp2 et ilc_li02, données 2024. Calculs de l'auteur.")


# ------------------------------- p2 : prélèvements sociaux, salaires contre pensions
def p2():
    r = lire("prelevements_sociaux.csv")
    def part(cat, nature):
        return sum(float(x["taux_pct_brut"]) for x in r
                   if x["categorie"] == cat and x["nature"] == nature)

    cas = [
        ("Salaire", "salaire"),
        ("Pension, taux normal", "pension_normal"),
        ("Pension, taux médian", "pension_median"),
        ("Pension, taux réduit", "pension_reduit"),
        ("Pension exonérée", "pension_exonere"),
    ]
    nc = [part(c, "non contributif") for _, c in cas]
    co = [part(c, "contributif") for _, c in cas]

    fig, ax = plt.subplots(figsize=(11.4, 5.2))
    y = list(range(len(cas)))[::-1]
    ax.barh(y, nc, color=BLEU, height=0.6, zorder=2, label="CSG, CRDS, CASA")
    ax.barh(y, co, left=nc, color="#C9CDD2", height=0.6, zorder=2,
            label="cotisations ouvrant des droits")
    for yy, a, b, (nom, _) in zip(y, nc, co, cas):
        if a > 1:
            ax.text(a / 2, yy, f"{a:.1f}".replace(".", ","), ha="center", va="center",
                    fontsize=9.5, color="white", fontweight="bold")
        if b > 1:
            ax.text(a + b / 2, yy, f"{b:.1f}".replace(".", ","), ha="center", va="center",
                    fontsize=9.5, color=INK, fontweight="bold")
        ax.text(a + b + 0.35, yy, f"{a + b:.1f} %".replace(".", ","), va="center",
                fontsize=10, color=INK, fontweight="bold")
    ax.set_yticks(y, [n for n, _ in cas], fontsize=10)
    ax.set_xlim(0, 24)
    ax.xaxis.set_major_formatter(PCT)
    grille(ax, "x")
    ax.spines["left"].set_visible(False)
    ax.tick_params(left=False)
    ax.legend(loc="lower right", frameon=False, fontsize=9.5, labelcolor=INK2,
              handlelength=1.1)

    note = ("Convention retenue par le rapport : toute cotisation est un impôt.\n"
            "L'écart entre un salaire et une pension au taux normal est alors de 11,7 points.")
    ax.text(11.6, 2.25, note, fontsize=9.5, color=PAL[1], va="center", linespacing=1.5)
    note2 = ("Si l'on ne retient que la part non contributive, soit la CSG, la CRDS\n"
             "et la CASA, le même écart tombe à 0,4 point.")
    ax.text(11.6, 1.25, note2, fontsize=9.5, color=PAL[2], va="center", linespacing=1.5)

    titre(ax, "Entre un salaire et une pension, l'écart dépend presque entièrement\n"
              "d'une convention comptable",
          "Prélèvements sociaux sur 100 € de revenu brut, part supportée par le titulaire du "
          "revenu, taux au 1er janvier 2026.\nLes cotisations employeur, qui n'ont pas "
          "d'équivalent sur les pensions, ajoutent environ 30 à 45 points sur un salaire.")
    fin(fig, "p2_salaire_pension.png",
        "Sources : Urssaf, taux de cotisations du secteur privé au 1er janvier 2026 ; "
        "service-public.gouv.fr, fiche F2971. Salarié du privé sous le plafond de la sécurité "
        "sociale.")


# --------------------------------------- p3 : un impôt sur le stock, en taux sur le flux
def p3():
    inflation, pfu = 2.0, 0.30
    r = [x / 10 for x in range(10, 81)]
    taux = [(0.0, "Aucun impôt sur le stock"), (0.5, "0,5 % du stock"),
            (1.0, "1 % du stock"), (2.0, "2 % du stock")]
    cou = [MUTED, "#9ec5f4", "#3987e5", PAL[1]]

    fig, ax = plt.subplots(figsize=(11.2, 6.0))
    for (t, lab), c in zip(taux, cou):
        y = [(t + pfu * (x + inflation)) / x * 100 for x in r]
        ax.plot(r, y, color=c, lw=2.4 if t == 2 else 1.7, zorder=3)
        yb = (t + pfu * (8 + inflation)) / 8 * 100
        ax.text(8.12, yb, lab, va="center", fontsize=9.5, color=c,
                fontweight="bold" if t == 2 else "normal")

    ax.axhline(100, color=INK, lw=1.0, ls=(0, (4, 3)), zorder=4)
    ax.text(6.0, 104, "au-dessus de cette ligne,\nl'impôt dépasse la totalité\ndu rendement réel",
            fontsize=9, color=INK, va="bottom", path_effects=HALO)
    ax.plot([3], [(2 + pfu * 5) / 3 * 100], "o", ms=7, color=PAL[1], zorder=5,
            markeredgecolor="white", markeredgewidth=1.2)
    ax.annotate("Un rendement réel de 3 % et un impôt de 2 % sur le stock :\n"
                "117 % du rendement réel est prélevé",
                xy=(3, 116.7), xytext=(3.45, 158), fontsize=9.5, color=PAL[1],
                fontweight="bold", path_effects=HALO,
                arrowprops=dict(arrowstyle="-", color=PAL[1], lw=0.9,
                                connectionstyle="arc3,rad=-0.2"))

    ax.set_xlim(1, 9.9)
    ax.set_ylim(0, 200)
    ax.set_xticks(range(1, 9))
    ax.xaxis.set_major_formatter(PCT)
    ax.yaxis.set_major_formatter(PCT)
    ax.set_xlabel("rendement réel annuel du placement")
    grille(ax)
    titre(ax, "Deux pour cent du stock, c'est davantage que la totalité d'un rendement réel de 3 %",
          "Part du rendement réel absorbée par l'impôt. Le prélèvement forfaitaire unique de "
          "30 % sur le rendement nominal est inclus\ndans tous les cas ; l'inflation est "
          "supposée de 2 % par an.")
    fin(fig, "p3_stock_contre_flux.png",
        "Calcul arithmétique. Taux statutaires français : prélèvement forfaitaire unique de "
        "30 %, soit 12,8 % d'impôt sur le revenu et 17,2 % de prélèvements sociaux, assis sur "
        "le rendement nominal.")


# ------------------------------- p4 : l'impôt sur le rendement est un impôt sur l'attente
def p4():
    r = 0.03
    cas = [(0.172, "17,2 %\nprélèvements sociaux seuls", "#9ec5f4"),
           (0.300, "30 %\nprélèvement forfaitaire unique", PAL[0]),
           (0.472, "47,2 %\nrevenu foncier au taux marginal de 30 %", PAL[1])]
    ans = list(range(0, 41))

    fig, ax = plt.subplots(figsize=(11.2, 6.0))
    for tau, lab, c in cas:
        y = [(1 - ((1 + r * (1 - tau)) / (1 + r)) ** t) * 100 for t in ans]
        ax.plot(ans, y, color=c, lw=2.3, zorder=3)
        ax.text(40.6, y[-1], lab, va="center", fontsize=9.5, color=c, fontweight="bold",
                linespacing=1.4)
        ax.plot([30], [y[30]], "o", ms=5.5, color=c, zorder=4,
                markeredgecolor="white", markeredgewidth=1.1)
        ax.text(29.4, y[30] + 1.6, f"{y[30]:.0f} %".replace(".", ","), ha="right",
                fontsize=9.5, color=c, fontweight="bold", path_effects=HALO)
    ax.axvline(30, color=MUTED, lw=0.8, ls=(0, (3, 3)), zorder=1)
    ax.text(29.4, 2, "après trente ans\nd'épargne", ha="right", fontsize=9, color=INK2,
            linespacing=1.4)

    ax.set_xlim(0, 52)
    ax.set_ylim(0, 48)
    ax.set_xticks(range(0, 41, 10), ["0", "10 ans", "20 ans", "30 ans", "40 ans"])
    ax.yaxis.set_major_formatter(PCT)
    ax.set_xlabel("durée pendant laquelle l'épargne est conservée")
    grille(ax)
    titre(ax, "Un impôt sur le rendement est un impôt sur la durée de l'attente",
          "Taux d'imposition implicite de la consommation différée, pour un rendement réel de "
          "3 % par an. Lire : trente ans d'épargne\ntaxée au prélèvement forfaitaire unique "
          "reviennent à taxer la consommation à 23 %, contre zéro pour la consommation "
          "immédiate.")
    fin(fig, "p4_impot_sur_l_attente.png",
        "Calcul arithmétique. Trois régimes français : 17,2 % de prélèvements sociaux seuls, "
        "30 % pour le prélèvement forfaitaire unique, 47,2 % pour un revenu foncier taxé au "
        "taux marginal de 30 %.")


if __name__ == "__main__":
    p1(); p2(); p3(); p4()
    print("p1 à p4 écrits dans figures/")
