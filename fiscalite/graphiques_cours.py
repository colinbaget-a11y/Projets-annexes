"""
Figures du cours : les mécanismes de la taxation optimale, et quatre dispositifs empruntés aux
publications de la Tax Foundation, refaits sur données françaises.

    python graphiques_cours.py

c1  la perte sèche croît au carré du taux
c2  le taux supérieur qui maximise les recettes, selon l'élasticité
c3  qui gagne vraiment à un taux réduit de TVA
c4  coin fiscal moyen et marginal en France, selon le niveau de salaire
c5  ce que l'inflation fait à un impôt assis sur le rendement nominal
c6  les cent euros de profit : la cascade jusqu'à l'actionnaire
c7  le pyramidage d'une taxe sur le chiffre d'affaires
c8  la valeur actuelle d'un amortissement
c9  la matrice des rangs de l'indice de compétitivité fiscale
"""
import csv
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

from graphiques import (NU, BLEU, GRIS, HALO, INK, INK2, OCRE, PAL, PCT, SURFACE, VERT,
                        fin, grille, panneau, titre)

HERE = Path(__file__).resolve().parent
BRIQUE = "#993333"


def lire(nom, sep=";"):
    with open(HERE / "donnees" / nom) as f:
        return list(csv.DictReader(f, delimiter=sep))


def fr(v, d=0):
    return f"{v:.{d}f}".replace(".", ",")


# ------------------------------------------- c1 : la perte croît au carré du taux
def c1():
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(12.4, 4.9),
                                 gridspec_kw={"width_ratios": [1.5, 1]})
    taux = [t / 2 for t in range(0, 121)]
    perte = [100 * (t / 20) ** 2 for t in taux]
    a1.plot(taux, perte, color=BLEU, lw=2.3, zorder=3)
    for t in (20, 40, 60):
        v = 100 * (t / 20) ** 2
        a1.plot([t], [v], "o", ms=6, color=BLEU, markeredgecolor=SURFACE, markeredgewidth=1.5,
                zorder=4)
        a1.annotate(f"{t} % → {fr(v)}", (t, v), xytext=(8, -4), textcoords="offset points",
                    fontsize=9.5, color=BLEU, fontweight="bold", path_effects=HALO)
    a1.set_xlim(0, 68)
    a1.set_ylim(0, 1000)
    a1.set_xlabel("taux de l'impôt")
    a1.xaxis.set_major_formatter(PCT)
    grille(a1)
    panneau(a1, "Perte sèche, indice 100 à un taux de 20 %")

    cas = [("Deux taux\n10 % et 30 %", 100 + 900, [100, 900], [BLEU, "#4a7fd4"]),
           ("Un taux unique\n20 % et 20 %", 400 + 400, [400, 400], [VERT, "#4f9e73"])]
    for i, (lab, tot, parts, cou) in enumerate(cas):
        bas = 0
        for p, c in zip(parts, cou):
            a2.bar([i], [p], bottom=[bas], width=0.56, color=c, zorder=2)
            a2.text(i, bas + p / 2, fr(p), ha="center", va="center", fontsize=10,
                    color="white", fontweight="bold")
            bas += p
        a2.text(i, tot + 35, fr(tot), ha="center", fontsize=11.5, fontweight="bold",
                color=BLEU if i == 0 else VERT)
    a2.set_xticks([0, 1], [c[0] for c in cas], fontsize=9.5)
    a2.set_ylim(0, 1180)
    a2.set_xlim(-0.6, 1.6)
    grille(a2)
    a2.annotate("", xy=(1, 870), xytext=(0, 1060),
                arrowprops=dict(arrowstyle="->", color=BRIQUE, lw=1.3,
                                connectionstyle="arc3,rad=-0.25"))
    a2.text(0.5, 1120, "20 % de perte en moins,\nà rendement identique", ha="center",
            fontsize=9.5, color=BRIQUE, fontweight="bold", linespacing=1.4)
    panneau(a2, "Deux assiettes voisines, même rendement")

    fig.subplots_adjust(wspace=0.22)
    if not NU:
        fig.text(0.0, 1.10, "Pourquoi le coût d'un impôt croît avec le carré du taux",
             fontsize=11.5, fontweight="bold", color=INK, transform=a1.transAxes)
    fin(fig, "c1_perte_au_carre.png",
        "Calcul arithmétique. La perte sèche est proportionnelle à l'élasticité de l'assiette et "
        "au carré du taux ; seule la forme est représentée, pas l'unité.",
        "Note : à droite, deux assiettes de même taille rapportant ensemble la même somme. "
        "Taxées à 10 % et 30 %, elles détruisent 10² + 30² = 1 000 ; taxées toutes deux à 20 %, "
        "20² + 20² = 800. L'écart de 20 % est perdu sans contrepartie pour personne.")


# --------------------------------- c2 : le taux supérieur selon l'élasticité
def c2():
    fig, ax = plt.subplots(figsize=(10.6, 5.2))
    xs = [x / 100 for x in range(5, 101)]
    for a, c, lab, xl, dy in ((1.5, "#7fa4e0", "queue plus fine, a = 1,5", 0.66, 7),
                              (2.0, BLEU, "France, a = 2,0", 0.52, -8),
                              (2.5, "#001f5c", "queue plus épaisse, a = 2,5", 0.40, -8)):
        ys = [100 / (1 + a * x) for x in xs]
        ax.plot(xs, ys, color=c, lw=2.5 if a == 2 else 1.6, zorder=3)
        ax.text(xl, 100 / (1 + a * xl) + dy, lab, va="center", ha="left" if a == 1.5 else "center",
                fontsize=9.5, color=c, fontweight="bold" if a == 2 else "normal",
                path_effects=HALO)
    for e in (0.25, 0.5, 1.0):
        v = 100 / (1 + 2 * e)
        ax.plot([e], [v], "o", ms=6.5, color=BLEU, markeredgecolor=SURFACE, markeredgewidth=1.6,
                zorder=4)
        ax.annotate(f"élasticité {fr(e, 2)}\n→ {fr(v)} %", (e, v),
                    xytext=(0, 16) if e < 1 else (-14, 20),
                    textcoords="offset points", ha="center", fontsize=9.5, color=BLEU,
                    fontweight="bold", linespacing=1.4, path_effects=HALO)
    ax.set_xlim(0.05, 1.08)
    ax.set_ylim(0, 92)
    ax.set_xticks([0.1, 0.25, 0.5, 0.75, 1.0], ["0,1", "0,25", "0,5", "0,75", "1,0"])
    ax.set_xlabel("élasticité du revenu imposable")
    ax.yaxis.set_major_formatter(PCT)
    grille(ax)
    titre(ax, "Le taux marginal supérieur qui maximise les recettes",
          "Formule 1 / (1 + a × e), où e est l'élasticité du revenu imposable et a l'épaisseur de "
          "la queue haute de la distribution.")
    fin(fig, "c2_taux_superieur.png",
        "Calcul arithmétique d'après la formule de Saez (2001).",
        "Note : ce taux maximise les recettes ; il n'est le taux optimal que si l'on accorde un "
        "poids strictement nul au bien-être des contribuables concernés. Passer d'une élasticité "
        "de 0,25 à 0,5 fait perdre dix-sept points, ce qui situe l'enjeu du paramètre.")


# ------------------------------------ c3 : qui gagne au taux réduit de TVA
def c3():
    menages = [("Ménage modeste\n1 500 € par mois", 1500, 0.18, VERT),
               ("Ménage aisé\n5 000 € par mois", 5000, 0.09, OCRE)]
    pts = 15
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(11.8, 4.9))
    for i, (lab, rev, part, c) in enumerate(menages):
        depense = rev * part
        gain = depense * pts / 100
        a1.bar([i], [gain], width=0.5, color=c, zorder=2)
        a1.text(i, gain + 2.2, fr(gain) + " €", ha="center", fontsize=12, fontweight="bold",
                color=c)
        a2.bar([i], [100 * gain / rev], width=0.5, color=c, zorder=2)
        a2.text(i, 100 * gain / rev + 0.08, fr(100 * gain / rev, 2) + " %", ha="center",
                fontsize=12, fontweight="bold", color=c)
    for ax, ymax, t in ((a1, 86, "Ce que le taux réduit rapporte, en euros par mois"),
                        (a2, 3.3, "Le même avantage, en % du revenu")):
        ax.set_xticks([0, 1], [m[0] for m in menages], fontsize=9.5)
        ax.set_ylim(0, ymax)
        ax.set_xlim(-0.6, 1.6)
        grille(ax)
        panneau(ax, t)
    a2.yaxis.set_major_formatter(PCT)
    fig.subplots_adjust(wspace=0.24)
    if not NU:
        fig.text(0.0, 1.10, "Un taux réduit donne plus d'euros au ménage aisé qu'au ménage modeste",
             fontsize=11.5, fontweight="bold", color=INK, transform=a1.transAxes)
    fin(fig, "c3_taux_reduit.png",
        "Calcul arithmétique. Parts budgétaires illustratives : 18 % du revenu consacrés à "
        "l'alimentation pour le ménage modeste, 9 % pour le ménage aisé ; écart de taux de TVA de "
        "quinze points.",
        "Note : la mesure est progressive rapportée au revenu et régressive en euros. Or c'est "
        "avec des euros que l'on achète. Verser directement 67 € au ménage modeste coûte moins "
        "cher au budget que d'en distribuer 40 à l'un et 67 à l'autre, et l'aide davantage.")


# --------------------- c4 : coin fiscal moyen et marginal, par niveau de salaire
def c4():
    niveaux = [("67 % du salaire moyen", 41.17, 64.59),
               ("Salaire moyen", 47.18, 58.18),
               ("167 % du salaire moyen", 54.12, 59.97)]
    fig, ax = plt.subplots(figsize=(10.6, 5.4))
    x = range(len(niveaux))
    larg = 0.33
    for j, (cle, lab, c) in enumerate(((1, "Coin fiscal moyen", BLEU),
                                       (2, "Coin fiscal marginal", OCRE))):
        xs = [i + (j - 0.5) * larg for i in x]
        vs = [n[cle] for n in niveaux]
        ax.bar(xs, vs, width=larg * 0.9, color=c, zorder=2, label=lab)
        for xx, v in zip(xs, vs):
            ax.text(xx, v + 0.9, fr(v, 1), ha="center", fontsize=10.5, fontweight="bold",
                    color=c)
    ax.plot([i + 0.5 * larg for i in x], [n[2] for n in niveaux], color=OCRE, lw=1.2,
            ls=(0, (4, 2)), zorder=3)
    ax.set_xticks(list(x), [n[0] for n in niveaux], fontsize=10)
    ax.set_ylim(0, 74)
    ax.yaxis.set_major_formatter(PCT)
    grille(ax)
    leg = ax.legend(loc="upper left", fontsize=9.5, handlelength=1.1)
    for t, c in zip(leg.get_texts(), (BLEU, OCRE)):
        t.set_color(c)
    ax.annotate("Le coin marginal est le plus élevé\nà 67 % du salaire moyen,\npas au sommet",
                xy=(0.17, 64.59), xytext=(0.72, 69), fontsize=9.5, color=BRIQUE,
                fontweight="bold", linespacing=1.45, path_effects=HALO,
                arrowprops=dict(arrowstyle="->", color=BRIQUE, lw=1.1,
                                connectionstyle="arc3,rad=0.2"))
    titre(ax, "Le profil français des prélèvements sur le travail n'est pas monotone",
          "Célibataire sans enfant, en % du coût total du travail, 2025. Le coin moyen est ce qui "
          "est prélevé sur l'ensemble\ndu salaire ; le coin marginal est ce qui est prélevé sur "
          "l'euro suivant.")
    fin(fig, "c4_coin_par_niveau.png",
        "Source : OCDE, Taxing Wages, indicateurs comparatifs, données 2025.",
        "Note : personne n'a décidé que l'euro supplémentaire serait plus taxé à 67 % du salaire "
        "moyen qu'au salaire moyen. Ce creux résulte de la superposition des allègements de "
        "cotisations, de la prime d'activité et des aides sous condition de ressources, dont "
        "chacun est défendable isolément.")


# ----------------------- c5 : ce que l'inflation fait à un impôt sur le rendement
def c5():
    fig, ax = plt.subplots(figsize=(10.6, 5.2))
    infl = [i / 10 for i in range(0, 61)]
    for r, c, lab in ((2.0, "#7fa4e0", "rendement réel de 2 %"),
                      (3.0, BLEU, "rendement réel de 3 %"),
                      (5.0, "#001f5c", "rendement réel de 5 %")):
        ys = [30 * (r + p) / r for p in infl]
        ax.plot(infl, ys, color=c, lw=2.5 if r == 3 else 1.6, zorder=3)
        ax.text(6.08, ys[-1], lab, va="center", fontsize=9.5, color=c,
                fontweight="bold" if r == 3 else "normal")
    ax.axhline(30, color=GRIS, lw=1.1, ls=(0, (4, 3)), zorder=2)
    ax.text(0.1, 32, "taux affiché : 30 %", fontsize=9.5, color=GRIS)
    ax.plot([2], [50], "o", ms=7, color=BLEU, markeredgecolor=SURFACE, markeredgewidth=1.6,
            zorder=4)
    ax.annotate("À 2 % d'inflation et 3 % de rendement réel,\nle taux effectif est de 50 %",
                xy=(2, 50), xytext=(2.5, 72), fontsize=9.5, color=BLEU, fontweight="bold",
                linespacing=1.45, path_effects=HALO,
                arrowprops=dict(arrowstyle="-", color=BLEU, lw=0.9,
                                connectionstyle="arc3,rad=-0.2"))
    ax.set_xlim(0, 8.6)
    ax.set_ylim(0, 115)
    ax.set_xticks(range(0, 7), [f"{i} %" for i in range(0, 7)])
    ax.set_xlabel("inflation annuelle")
    ax.yaxis.set_major_formatter(PCT)
    grille(ax)
    titre(ax, "Un impôt assis sur le rendement nominal taxe l'inflation",
          "Taux effectif sur le rendement réel d'un prélèvement forfaitaire de 30 % appliqué au "
          "rendement nominal.")
    fin(fig, "c5_inflation.png",
        "Calcul arithmétique. Taux statutaire français : prélèvement forfaitaire unique de 30 %, "
        "assis sur le rendement nominal et non indexé.",
        "Note : un épargnant dont le placement rapporte exactement l'inflation paie un impôt sur "
        "un gain qui n'existe pas. Le taux effectif monte avec l'inflation sans qu'aucune loi "
        "ait été votée, et d'autant plus vite que le rendement réel est faible.")


# ------------------------- c6 : les cent euros de profit, cascade et comparaison
def c6():
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(12.6, 5.4),
                                 gridspec_kw={"width_ratios": [1, 1.25]})
    etapes = [("Profit\navant impôt", 100.0, 100.0, GRIS),
              ("Impôt sur\nles sociétés", 63.87, 36.13, BLEU),
              ("Impôt sur\nle dividende", 42.15, 21.72, OCRE),
              ("Net pour\nl'actionnaire", 42.15, 42.15, VERT)]
    for i, (lab, reste, bloc, c) in enumerate(etapes):
        if i == 0 or i == 3:
            a1.bar([i], [reste], width=0.62, color=c, zorder=2)
            a1.text(i, reste + 2.2, fr(reste, 1) + " €", ha="center", fontsize=11,
                    fontweight="bold", color=c)
        else:
            bas = reste
            a1.bar([i], [bloc], bottom=[bas], width=0.62, color=c, zorder=2)
            a1.text(i, bas + bloc / 2, fr(bloc, 1) + " €", ha="center", va="center",
                    fontsize=10.5, fontweight="bold", color="white")
            a1.plot([i - 0.31, i + 0.31], [bas, bas], color=INK2, lw=0.8, zorder=3)
    a1.set_xticks(range(4), [e[0] for e in etapes], fontsize=9)
    a1.set_ylim(0, 118)
    a1.set_xlim(-0.6, 3.6)
    grille(a1)
    a1.text(1.5, 108, "57,9 € prélevés sur 100 € de profit", ha="center", fontsize=10.5,
            fontweight="bold", color=BRIQUE, path_effects=HALO)
    panneau(a1, "Cent euros de profit distribué, en France")

    d = lire("dividendes_taux_combine.csv")
    d.sort(key=lambda x: float(x["taux_combine"]))
    y = list(range(len(d)))
    cou = [BLEU if x["code"] == "FRA" else "#C9CDD2" for x in d]
    a2.barh(y, [float(x["taux_combine"]) for x in d], color=cou, height=0.72, zorder=2)
    for i, x in enumerate(d):
        v = float(x["taux_combine"])
        a2.text(v + 0.8, i, fr(v, 1), va="center", fontsize=9,
                color=BLEU if x["code"] == "FRA" else INK2,
                fontweight="bold" if x["code"] == "FRA" else "normal")
    a2.set_yticks(y, [x["pays"] for x in d], fontsize=9)
    for t, x in zip(a2.get_yticklabels(), d):
        if x["code"] == "FRA":
            t.set_color(BLEU)
            t.set_fontweight("bold")
    a2.set_xlim(0, 68)
    a2.xaxis.set_major_formatter(PCT)
    grille(a2, "x")
    a2.spines["left"].set_visible(False)
    a2.tick_params(left=False)
    panneau(a2, "Taux combiné sur les profits distribués, 2025")

    fig.subplots_adjust(wspace=0.3)
    if not NU:
        fig.text(0.0, 1.10, "Ce que deux impôts successifs font à cent euros de profit",
             fontsize=11.5, fontweight="bold", color=INK, transform=a1.transAxes)
    fin(fig, "c6_cascade_profit.png",
        "Source : OCDE, taux combinés d'imposition des dividendes, données 2025. Dispositif "
        "emprunté aux publications de la Tax Foundation.",
        "Note : taux statutaires au sommet du barème. Le taux français sur les sociétés inclut "
        "les surtaxes applicables en 2025, dont une partie est présentée comme temporaire ; "
        "l'imposition du dividende retient le prélèvement forfaitaire de 30 % majoré de la "
        "contribution sur les hauts revenus. Un actionnaire moyen supporte moins.")


# ----------------------------- c7 : le pyramidage d'une taxe sur le chiffre d'affaires
def c7():
    taux = 0.16
    etapes = list(range(1, 7))
    cumule = [taux * (n + 1) / 2 for n in etapes]
    fig, ax = plt.subplots(figsize=(10.6, 5.2))
    cou = [BLEU if n != 1 else VERT for n in etapes]
    ax.bar(etapes, cumule, width=0.58, color=cou, zorder=2)
    for n, v in zip(etapes, cumule):
        ax.text(n, v + 0.012, fr(v, 2) + " %", ha="center", fontsize=10.5, fontweight="bold",
                color=VERT if n == 1 else BLEU)
    ax.axhline(taux, color=GRIS, lw=1.1, ls=(0, (4, 3)), zorder=3)
    ax.text(6.35, taux, "taux affiché\n0,16 %", va="center", fontsize=9.5, color=GRIS,
            linespacing=1.4)
    ax.annotate("Une chaîne de quatre entreprises\nsupporte 2,5 fois le taux affiché",
                xy=(4, 0.385), xytext=(2.35, 0.085), fontsize=9.5, color=BRIQUE,
                fontweight="bold", linespacing=1.45, va="center",
                arrowprops=dict(arrowstyle="->", color=BRIQUE, lw=1.1,
                                connectionstyle="arc3,rad=-0.3"))
    ax.set_xlim(0.4, 7.9)
    ax.set_ylim(0, 0.64)
    ax.set_xticks(etapes, ["1", "2", "3", "4", "5", "6"], fontsize=10)
    ax.set_xlabel("nombre d'entreprises successives dans la chaîne de production")
    ax.text(1, 0.135, "entreprise intégrée", ha="center", va="top", fontsize=9,
            color=VERT, style="italic")
    ax.set_yticks([0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6],
                  ["0", "0,1 %", "0,2 %", "0,3 %", "0,4 %", "0,5 %", "0,6 %"])
    grille(ax)
    titre(ax, "Une taxe sur le chiffre d'affaires frappe plusieurs fois le même produit",
          "Charge totale incorporée dans le prix final, en % de ce prix, pour une taxe de 0,16 % "
          "appliquée aux ventes de chaque entreprise.")
    fin(fig, "c7_pyramidage.png",
        "Calcul arithmétique. Taux de la contribution sociale de solidarité des sociétés, 0,16 % "
        "du chiffre d'affaires au-dessus d'un abattement. Dispositif emprunté aux publications "
        "de la Tax Foundation.",
        "Note : la valeur ajoutée est supposée répartie également entre les entreprises de la "
        "chaîne. Un produit fabriqué par une entreprise intégrée supporte le taux affiché ; le "
        "même produit fabriqué par quatre entreprises successives en supporte deux fois et demie "
        "autant. La taxe subventionne donc la concentration verticale sans que personne l'ait "
        "décidé. La TVA, qui ouvre droit à déduction à chaque étape, ne produit pas cet effet.")


# ------------------------------- c8 : la valeur actuelle d'un amortissement
def c8():
    def va(n, r):
        return sum((100 / n) / (1 + r) ** t for t in range(1, n + 1))

    fig, ax = plt.subplots(figsize=(10.6, 5.2))
    ns = list(range(1, 41))
    for r, c, lab in ((0.03, "#7fa4e0", "taux d'actualisation 3 %"),
                      (0.05, BLEU, "taux d'actualisation 5 %"),
                      (0.08, "#001f5c", "taux d'actualisation 8 %")):
        ys = [va(n, r) for n in ns]
        ax.plot(ns, ys, color=c, lw=2.5 if r == 0.05 else 1.6, zorder=3)
        ax.text(40.8, ys[-1], lab, va="center", fontsize=9.5, color=c,
                fontweight="bold" if r == 0.05 else "normal")
    for n in (1, 5, 20, 40):
        v = va(n, 0.05)
        ax.plot([n], [v], "o", ms=6, color=BLEU, markeredgecolor=SURFACE, markeredgewidth=1.5,
                zorder=4)
        ax.annotate(f"{n} an{'s' if n > 1 else ''} : {fr(v)} €", (n, v), xytext=(7, 7),
                    textcoords="offset points", fontsize=9.5, color=BLEU, fontweight="bold",
                    path_effects=HALO)
    ax.set_xlim(0, 54)
    ax.set_ylim(0, 108)
    ax.set_xticks([1, 10, 20, 30, 40], ["1", "10", "20", "30", "40"])
    ax.set_xlabel("durée d'amortissement, en années")
    ax.set_yticks([0, 25, 50, 75, 100], ["0 €", "25 €", "50 €", "75 €", "100 €"])
    grille(ax)
    titre(ax, "Cent euros déduits sur vingt ans n'en valent plus que soixante-deux aujourd'hui",
          "Valeur actuelle des déductions fiscales obtenues pour un investissement de 100 €, "
          "selon la durée d'amortissement.")
    fin(fig, "c8_amortissement.png",
        "Calcul arithmétique. Dispositif emprunté aux publications de la Tax Foundation sur la "
        "récupération des coûts.",
        "Note : une entreprise qui investit 100 € ne récupère fiscalement ces 100 € que si elle "
        "les déduit immédiatement. Étalée, la déduction perd de la valeur, et la différence est "
        "un impôt qui pèse sur le rendement normal de l'investissement — exactement ce que la "
        "théorie recommande de ne pas taxer. Plus l'inflation et les taux d'intérêt sont élevés, "
        "plus l'écart se creuse.")


# ------------------- c9 : la matrice des rangs de l'indice de compétitivité fiscale
def c9():
    d = lire("itci_2025.csv")
    cats = [("societes", "Sociétés"), ("revenu", "Revenu"), ("consommation", "Consommation"),
            ("foncier", "Foncier"), ("international", "International")]
    fig, ax = plt.subplots(figsize=(9.6, 8.4))
    n = len(d)
    for i, x in enumerate(d):
        y = n - 1 - i
        for j, (cle, _) in enumerate(cats):
            rang = int(x[cle])
            f = (rang - 1) / 37
            coul = f"#{int(255 - 160 * (1 - f)):02x}{int(255 - 150 * (1 - f)):02x}" \
                   f"{int(255 - 60 * (1 - f)):02x}" if f > 0.5 else None
            # bleu clair pour les bons rangs, brique clair pour les mauvais
            if rang <= 19:
                t = 1 - (rang - 1) / 18
                c = f"#{int(255 - 120 * t):02x}{int(255 - 80 * t):02x}{int(255 - 20 * t):02x}"
            else:
                t = (rang - 19) / 19
                c = f"#{int(255 - 10 * t):02x}{int(255 - 110 * t):02x}{int(255 - 110 * t):02x}"
            ax.add_patch(Rectangle((j, y), 0.94, 0.9, facecolor=c, edgecolor=SURFACE, lw=1.2))
            ax.text(j + 0.47, y + 0.45, str(rang), ha="center", va="center", fontsize=9.5,
                    color=INK, fontweight="bold" if x["code"] == "FRA" else "normal")
        ax.text(-0.3, y + 0.45, f"{x['pays']}", ha="right", va="center", fontsize=9.5,
                color=BLEU if x["code"] == "FRA" else INK,
                fontweight="bold" if x["code"] == "FRA" else "normal")
        ax.text(5.3, y + 0.45, f"{x['rang']}", ha="center", va="center", fontsize=9.5,
                color=BLEU if x["code"] == "FRA" else INK2,
                fontweight="bold" if x["code"] == "FRA" else "normal")
        ax.text(6.3, y + 0.45, fr(float(x["score"]), 1), ha="right", va="center", fontsize=9.5,
                color=BLEU if x["code"] == "FRA" else INK2,
                fontweight="bold" if x["code"] == "FRA" else "normal")
    for j, (_, lab) in enumerate(cats):
        ax.text(j + 0.47, n + 0.15, lab, ha="center", va="bottom", fontsize=9.5, color=INK2,
                rotation=0)
    ax.text(5.3, n + 0.15, "Rang", ha="center", va="bottom", fontsize=9.5, color=INK2)
    ax.text(6.3, n + 0.15, "Score", ha="right", va="bottom", fontsize=9.5, color=INK2)
    ax.set_xlim(-3.4, 6.6)
    ax.set_ylim(-0.3, n + 1.5)
    ax.axis("off")
    fig.subplots_adjust(left=0.02, right=0.98, top=0.90, bottom=0.03)
    titre(ax, "La France dernière de l'OCDE, mais pas sur tous les tableaux",
          "Rang de chaque pays dans l'indice de compétitivité fiscale internationale 2025, sur "
          "trente-huit pays. Plus le rang est\nélevé, plus la case est rouge.")
    fin(fig, "c9_matrice_indice.png",
        "Source : Tax Foundation, International Tax Competitiveness Index 2025, tableau 1. "
        "Dix-neuf des trente-huit pays sont représentés.",
        "Note : l'indice agrège plus de quarante variables selon une pondération choisie par ses "
        "auteurs, qui encode une préférence pour la neutralité à l'égard de l'investissement et "
        "pour une charge faible sur le capital. Il est utile là où il rejoint la théorie — les "
        "impôts sur la production, l'étroitesse de l'assiette de TVA — et constitue une prise de "
        "position là où il va au-delà.")


# ------------- c10 : le classement de l'OCDE appliqué à la structure française
def c10():
    blocs = [("Impôts récurrents\nsur l'immobilier", 48.0, VERT),
             ("Taxes sur la\nconsommation", 304.3, VERT),
             ("Autres impôts\nsur le patrimoine", 53.6, OCRE),
             ("Prélèvements sur\nle revenu du travail", 748.8, OCRE),
             ("Impôts sur\nles sociétés", 90.0, BRIQUE)]
    fig, ax = plt.subplots(figsize=(11.2, 5.4))
    x = range(len(blocs))
    ax.bar(x, [b[1] for b in blocs], width=0.56, color=[b[2] for b in blocs], zorder=2)
    for i, b in enumerate(blocs):
        ax.text(i, b[1] + 16, fr(b[1], 0) + " Md€", ha="center", fontsize=11,
                fontweight="bold", color=b[2])
    ax.set_xticks(list(x), [b[0] for b in blocs], fontsize=9.5)
    ax.set_ylim(0, 960)
    ax.set_yticks([0, 200, 400, 600, 800], ["0", "200", "400", "600", "800 Md€"])
    grille(ax)
    ax.annotate("", xy=(4.35, 862), xytext=(-0.35, 862),
                arrowprops=dict(arrowstyle="->", color=INK2, lw=1.2))
    ax.text(2, 886, "classement de l'OCDE : du moins au plus défavorable à la croissance",
            ha="center", fontsize=9.5, color=INK2, style="italic")
    titre(ax, "La France lève le plus là où le classement de l'OCDE place le plus de dommage",
          "Prélèvements obligatoires français de 2024 rangés selon le classement « fiscalité et "
          "croissance » de l'OCDE.")
    fin(fig, "c10_classement_ocde.png",
        "Sources : classement de Johansson, Heady, Arnold, Brys et Vartia, OCDE, document de "
        "travail n° 620, 2008 ; montants Eurostat, National Tax List France, 2024.",
        "Note de prudence : ce classement vient de régressions de croissance sur panel de pays, "
        "pas d'un théorème. Xing (2012) montre que l'ordre n'est pas robuste, et notamment que "
        "l'avantage attribué aux impôts récurrents sur l'immobilier ne résiste pas au changement "
        "de spécification. Ce qui subsiste est l'accord entre cet ordre et ce que la théorie "
        "prédit pour des raisons indépendantes : une assiette immobile se taxe sans dommage, un "
        "prélèvement sur un facteur de production en fait le plus.")


# --------- c11 : un taux unique avec abattement est déjà progressif
def c11():
    A, t = 12000, 0.30
    ys = list(range(0, 100001, 500))
    moy = [0 if y <= A else 100 * t * (1 - A / y) for y in ys]
    fig, ax = plt.subplots(figsize=(11.2, 5.4))
    ax.plot([0, A, A, 100000], [0, 0, 30, 30], color=OCRE, lw=2.2, zorder=3)
    ax.plot(ys, moy, color=BLEU, lw=2.6, zorder=4)
    ax.text(101500, 30, "taux marginal\nconstant à 30 %", va="center", fontsize=9.5,
            color=OCRE, fontweight="bold", linespacing=1.4)
    ax.text(101500, moy[-1], "taux moyen,\nqui monte sans cesse", va="center", fontsize=9.5,
            color=BLEU, fontweight="bold", linespacing=1.4)
    for y in (20000, 50000, 100000):
        v = 100 * t * (1 - A / y)
        ax.plot([y], [v], "o", ms=6, color=BLEU, markeredgecolor=SURFACE, markeredgewidth=1.5,
                zorder=5)
        ax.annotate(fr(v, 1) + " %", (y, v),
                    xytext=(0, 11) if y < 100000 else (0, -20), textcoords="offset points",
                    ha="center", fontsize=9.5, color=BLEU, fontweight="bold",
                    path_effects=HALO)
    ax.axvspan(0, A, color=GRIS, alpha=0.1, zorder=1)
    ax.text(A / 2, 27, "abattement", ha="center", fontsize=9, color=GRIS, rotation=90)
    ax.set_xlim(0, 139000)
    ax.set_ylim(0, 35)
    ax.set_xticks([0, 20000, 40000, 60000, 80000, 100000],
                  ["0", "20 000", "40 000", "60 000", "80 000", "100 000 €"])
    ax.set_xlabel("revenu annuel")
    ax.yaxis.set_major_formatter(PCT)
    grille(ax)
    titre(ax, "Un taux unique assorti d'un abattement est déjà un impôt progressif",
          "Taux marginal et taux moyen d'un impôt à taux unique de 30 % au-delà d'un abattement "
          "de 12 000 €.")
    fin(fig, "c11_flat_tax_progressive.png",
        "Calcul arithmétique. Définition de la progressivité reprise de l'encadré 2.1 de Tax by "
        "Design : un impôt est progressif lorsque le taux moyen augmente avec l'assiette.",
        "Note : la progressivité ne demande pas que le taux marginal augmente. Trois leviers la "
        "renforcent : relever l'abattement, relever le taux unique, ou ajouter une tranche "
        "supérieure. Le premier est le plus efficient, puisqu'il ne change le taux marginal de "
        "personne au-dessus du seuil.")


if __name__ == "__main__":
    c1(); c2(); c3(); c4(); c5(); c6(); c7(); c8(); c9(); c10(); c11()
