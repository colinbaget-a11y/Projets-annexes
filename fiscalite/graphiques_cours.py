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

from graphiques import (NU, BLEU, GRIS, HALO, INK, INK2, MUTED, OCRE, PAL, PCT, SURFACE, VERT,
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
    """Mille échanges possibles, dont le gain va de 100 € à 0 €. Une taxe de t € supprime ceux
    qui rapportent moins de t € : 10 t échanges disparaissent, chacun perdant en moyenne t/2 €.
    La perte vaut donc 5 t² : doubler la taxe quadruple la perte."""
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(12.4, 5.0),
                                 gridspec_kw={"width_ratios": [1.7, 1]})
    a1.plot([0, 1000], [100, 0], color=INK, lw=1.6, zorder=3)
    for t, alpha in ((20, 0.28), (10, 0.85)):
        x0 = 1000 - 10 * t
        a1.fill_between([x0, 1000], [t, 0], 0, color=BRIQUE, alpha=alpha, lw=0, zorder=2)
        a1.plot([620, 1000], [t, t], color=BRIQUE, lw=0.8, ls="--", zorder=2)
        a1.text(612, t, f"taxe {t} €", ha="right", va="center", fontsize=9, color=BRIQUE)
    a1.annotate("taxe de 10 € : perte de 500 €", (960, 3), xytext=(540, 74), fontsize=9.5,
                color=BRIQUE, fontweight="bold",
                arrowprops=dict(arrowstyle="->", color=BRIQUE, lw=1.0), path_effects=HALO)
    a1.annotate("taxe de 20 € : perte de 2 000 €", (870, 7), xytext=(540, 60), fontsize=9.5,
                color=BRIQUE, arrowprops=dict(arrowstyle="->", color=BRIQUE, lw=1.0),
                path_effects=HALO)
    a1.text(420, 97, "chaque point de la droite est un échange possible,\nà la hauteur de ce "
            "qu'il rapporte", fontsize=9, color=INK2, va="top", linespacing=1.35)
    a1.set_xlim(0, 1000)
    a1.set_ylim(0, 100)
    a1.set_xlabel("mille échanges possibles, du plus au moins avantageux")
    a1.set_ylabel("gain de l'échange, en euros")
    grille(a1)
    panneau(a1, "Les échanges que la taxe fait disparaître")

    ts = [10, 20, 30]
    pertes = [5 * t * t / (t * (1000 - 10 * t)) * 100 for t in ts]
    a2.bar(range(3), pertes, width=0.56, color=BRIQUE, zorder=2)
    for i, v in enumerate(pertes):
        a2.text(i, v + 0.6, f"{fr(v, 1)} €", ha="center", fontsize=10, fontweight="bold",
                color=BRIQUE)
    a2.set_xticks(range(3), [f"{t} €" for t in ts])
    a2.set_xlabel("montant de la taxe par échange")
    a2.set_ylim(0, 25)
    a2.set_ylabel("perte pour 100 € prélevés")
    grille(a2)
    panneau(a2, "Ce que coûte l'euro prélevé")
    fig.subplots_adjust(wspace=0.32)
    fin(fig, "c1_perte_au_carre.png",
        "Calcul arithmétique sur un exemple : mille échanges possibles dont le gain s'étage "
        "régulièrement de 100 € à 0 €.",
        "Note : une taxe de t € fait disparaître les échanges qui rapportent moins de t €, soit "
        "10 t échanges qui rapportaient en moyenne t/2 € ; la perte vaut 5 t². Les recettes valent "
        "t × (1 000 − 10 t) : 9 000 € pour une taxe de 10 €, 16 000 € pour 20 €, 21 000 € pour "
        "30 €. La perte, elle, passe de 500 à 2 000 puis 4 500 €.")


# --------------------------------- c2 : le taux supérieur selon l'élasticité
def c2():
    fig, ax = plt.subplots(figsize=(10.6, 5.2))
    xs = [x / 100 for x in range(5, 101)]
    for a, c, lab, xl, dy in ((1.5, "#7fa4e0", "queue plus fine, a = 1,5", 0.70, 7),
                              (2.0, BLEU, "France, a = 2,0", 0.64, -11),
                              (2.5, "#001f5c", "queue plus épaisse, a = 2,5", 0.30, -12)):
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
        "Calcul arithmétique. Parts budgétaires illustratives : la dépense alimentaire hors taxe "
        "vaut 18 % du revenu pour le ménage modeste et 9 % pour le ménage aisé ; l'écart de taux "
        "de TVA est de quinze points.",
        "Note : la mesure est progressive rapportée au revenu et régressive en euros. Or c'est "
        "avec des euros que l'on achète. Verser directement 68 € au ménage modeste coûte moins "
        "cher au budget que d'en distribuer 40 à l'un et 68 à l'autre, et l'aide davantage.")


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
    ax.set_ylim(0, 80)
    ax.yaxis.set_major_formatter(PCT)
    grille(ax)
    leg = ax.legend(loc="upper right", fontsize=9.5, handlelength=1.1, ncol=2)
    for t, c in zip(leg.get_texts(), (BLEU, OCRE)):
        t.set_color(c)
    titre(ax, "Le profil français des prélèvements sur le travail n'est pas monotone",
          "Célibataire sans enfant, 2025, en % du coût du travail : prélevé sur tout le salaire "
          "(moyen) et sur l'euro suivant (marginal).")
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
    ax.text(5.9, 25, "taux affiché : 30 %", fontsize=9.5, color=GRIS, ha="right")
    ax.plot([2], [50], "o", ms=7, color=BLEU, markeredgecolor=SURFACE, markeredgewidth=1.6,
            zorder=4)
    ax.annotate("À 2 % d'inflation et 3 % de rendement réel,\nle taux effectif est de 50 %",
                xy=(2, 50), xytext=(0.25, 100), fontsize=9.5, color=BLEU, fontweight="bold",
                linespacing=1.45, path_effects=HALO,
                arrowprops=dict(arrowstyle="-", color=BLEU, lw=0.9,
                                connectionstyle="arc3,rad=-0.2"))
    ax.set_xlim(0, 8.6)
    ax.set_ylim(0, 130)
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
    """Cent euros de bénéfice distribué en dividende à un actionnaire résident, dans trois
    situations françaises de 2025, puis la comparaison internationale de l'OCDE, où la France
    figure au taux normal et avec la contribution exceptionnelle de 2025."""
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(12.6, 5.0),
                                 gridspec_kw={"width_ratios": [1.25, 1]})
    cas = [("Taux normal,\nactionnaire ordinaire", 25.0, 0.30),
           ("Grande entreprise,\nactionnaire au sommet", 25.825, 0.34),
           ("Chiffre d'affaires\nsupérieur à 3 Md€, 2025", 36.13, 0.34)]
    couleurs = [(BLEU, "impôt sur les sociétés"), (OCRE, "impôt sur le dividende"),
                (VERT, "reste à l'actionnaire")]
    for i, (lab, t_is, t_div) in enumerate(cas):
        y = len(cas) - 1 - i
        div = (100 - t_is) * t_div
        net = 100 - t_is - div
        g = 0
        for v, (c, _) in zip((t_is, div, net), couleurs):
            a1.barh(y, v, left=g, height=0.58, color=c, edgecolor=SURFACE, lw=1.2, zorder=2)
            a1.text(g + v / 2, y, fr(v, 1), ha="center", va="center", fontsize=10.5,
                    fontweight="bold", color="white", zorder=3)
            g += v
        a1.text(103, y, f"{fr(100 - net, 1)} %", va="center", fontsize=10, color=INK,
                fontweight="bold")
    a1.text(103, len(cas) - 0.62, "prélevé", va="center", fontsize=8.5, color=INK2)
    a1.legend(handles=[Rectangle((0, 0), 1, 1, color=c) for c, _ in couleurs],
              labels=[nom for _, nom in couleurs], loc="upper left", bbox_to_anchor=(0, 1.02),
              ncol=2, fontsize=8.5, frameon=False, handlelength=0.9, columnspacing=1.0,
              handletextpad=0.4, labelcolor=INK2)
    a1.set_yticks(range(len(cas)), [c[0] for c in reversed(cas)], fontsize=9)
    a1.set_xlim(0, 116)
    a1.set_ylim(-0.45, len(cas) + 0.35)
    a1.set_xticks([0, 25, 50, 75, 100], ["0", "25", "50", "75", "100 €"])
    for s_ in ("left", "top", "right"):
        a1.spines[s_].set_visible(False)
    a1.tick_params(left=False)
    panneau(a1, "Ce que deviennent 100 € de bénéfice distribué")

    d = lire("dividendes_taux_combine.csv")
    lignes = [(x["pays"], float(x["taux_combine"]), "autre") for x in d if x["code"] != "FRA"]
    lignes.append(("France, taux normal", 100 - (100 - 25.825) * 0.66, "fra"))
    lignes.append(("France, surtaxe 2025", 100 - (100 - 36.13) * 0.66, "fra25"))
    lignes.sort(key=lambda x: x[1])
    y = list(range(len(lignes)))
    for i, (nom, v, k) in enumerate(lignes):
        if k == "fra":
            a2.barh(i, v, color=BLEU, height=0.72, zorder=2)
        elif k == "fra25":
            a2.barh(i, v, color="white", edgecolor=BLEU, hatch="////", lw=0.9, height=0.72,
                    zorder=2)
        else:
            a2.barh(i, v, color="#C9CDD2", height=0.72, zorder=2)
        a2.text(v + 0.8, i, fr(v, 1), va="center", fontsize=9,
                color=BLEU if k != "autre" else INK2,
                fontweight="bold" if k != "autre" else "normal")
    a2.set_yticks(y, [x[0] for x in lignes], fontsize=9)
    for t, x in zip(a2.get_yticklabels(), lignes):
        if x[2] != "autre":
            t.set_color(BLEU)
    a2.set_xlim(0, 68)
    a2.xaxis.set_major_formatter(PCT)
    grille(a2, "x")
    a2.spines["left"].set_visible(False)
    a2.tick_params(left=False)
    panneau(a2, "Taux combiné au sommet du barème, 2025")

    fig.subplots_adjust(wspace=0.78)
    if not NU:
        fig.text(0.0, 1.10, "Ce que deux impôts successifs font à cent euros de bénéfice",
                 fontsize=11.5, fontweight="bold", color=INK, transform=a1.transAxes)
    fin(fig, "c6_cascade_profit.png",
        "Sources : OCDE, taux combinés d'imposition des dividendes, données 2025 ; pour la "
        "France au taux normal et pour le graphique de gauche, calcul sur les taux légaux de 2025.",
        "Lecture : au taux normal de 25 %, 100 € de bénéfice deviennent 75 € après impôt sur les "
        "sociétés ; distribués, ils supportent 30 % de prélèvement forfaitaire (22,5 €), et "
        "l'actionnaire garde 52,5 €. La grande entreprise paie en plus la contribution sociale de "
        "3,3 % de l'impôt ; l'actionnaire au sommet paie en plus la contribution sur les hauts "
        "revenus de 4 %. La contribution exceptionnelle de 2025 ne concerne que les groupes dont "
        "le chiffre d'affaires dépasse 1 Md€ (taux porté à 31,0 %) ou 3 Md€ (36,1 %). Les "
        "taux des autres pays sont ceux de l'OCDE, au sommet du barème.")


# ----------------------------- c7 : le pyramidage d'une taxe sur le chiffre d'affaires
def c7():
    """Un produit vendu 100 € au consommateur, fabriqué en quatre étapes qui ajoutent chacune
    25 € de valeur. Chaque entreprise paie la taxe sur tout son chiffre d'affaires, qui contient
    la valeur produite en amont : la taxe porte au total sur 250 €, pas sur 100 €."""
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(12.4, 5.0),
                                 gridspec_kw={"width_ratios": [1.75, 1]})
    teintes = ["#0b2a61", "#1d4ba6", "#7691c8", "#c4d0ea"]
    noms = ["matière", "pièce", "module", "produit fini"]
    for i in range(4):
        bas = 0
        for j in range(i + 1):
            a1.bar(i, 25, bottom=bas, width=0.62, color=teintes[j], edgecolor=SURFACE, lw=1.2,
                   zorder=2)
            bas += 25
        a1.text(i, bas + 3, f"vend {bas} €", ha="center", fontsize=9.5, fontweight="bold",
                color=INK)
    for j, nom in enumerate(noms):
        a1.text(3.42, 12.5 + 25 * j, f"valeur ajoutée\nà l'étape {j + 1}", va="center",
                fontsize=8.5, color=teintes[j] if j < 2 else "#3a5a9e", linespacing=1.2)
    a1.set_xticks(range(4), noms, fontsize=9)
    a1.set_xlabel("ce que vend chaque entreprise de la chaîne")
    a1.set_xlim(-0.5, 4.3)
    a1.set_ylim(0, 112)
    a1.set_ylabel("chiffre d'affaires taxé, en euros")
    a1.text(-0.38, 104, "au total, 25 + 50 + 75 + 100 = 250 € taxés\npour un produit vendu 100 €",
            fontsize=9.5, color=BRIQUE, fontweight="bold", va="top", linespacing=1.35)
    grille(a1)
    panneau(a1, "La même valeur est taxée à chaque vente")

    vals = [0.16, 0.40]
    a2.bar([0, 1], vals, width=0.56, color=[VERT, BRIQUE], zorder=2)
    for i, v in enumerate(vals):
        a2.text(i, v + 0.012, f"{fr(v, 2)} €", ha="center", fontsize=10.5, fontweight="bold",
                color=VERT if i == 0 else BRIQUE)
    a2.set_xticks([0, 1], ["une entreprise\nqui fait tout", "quatre entreprises\nsuccessives"],
                  fontsize=9)
    a2.set_ylim(0, 0.5)
    a2.set_yticks([0, 0.1, 0.2, 0.3, 0.4, 0.5], ["0", "0,10", "0,20", "0,30", "0,40", "0,50"])
    a2.set_ylabel("taxe payée pour 100 € de prix final")
    grille(a2)
    panneau(a2, "Taxe contenue dans le prix final")
    fig.subplots_adjust(wspace=0.34)
    fin(fig, "c7_pyramidage.png",
        "Calcul arithmétique, au taux de la contribution sociale de solidarité des sociétés "
        "(0,16 % du chiffre d'affaires), en supposant que chaque étape ajoute le même montant "
        "et que la taxe est entièrement répercutée dans les prix.",
        "Note : la TVA, elle, n'est payée à chaque étape que sur la valeur ajoutée, puisque "
        "chaque entreprise déduit la taxe payée par son fournisseur ; elle porte au total sur "
        "100 €. Avec la contribution, faire fabriquer une pièce par un sous-traitant coûte plus "
        "cher que la fabriquer soi-même.")


# ------------------------------- c8 : la valeur actuelle d'un amortissement
def c8():
    """Une machine de 100 € amortie en vingt ans : vingt déductions de 5 €, dont chacune vaut
    moins aujourd'hui qu'elle est lointaine. Leur valeur actuelle totale, à 5 %, est de 62 €."""
    r, n = 0.05, 20
    ans = list(range(1, n + 1))
    nominal = [100 / n] * n
    actuel = [100 / n / (1 + r) ** t for t in ans]
    fig, ax = plt.subplots(figsize=(10.6, 5.0))
    ax.bar(ans, nominal, width=0.72, color="#D5DCEA", zorder=2, label="déduction de l'année : 5 €")
    ax.bar(ans, actuel, width=0.72, color=BLEU, zorder=3,
           label="ce qu'elle vaut aujourd'hui, à 5 % d'intérêt")
    for t in (1, 10, 20):
        ax.text(t, actuel[t - 1] / 2, fr(actuel[t - 1], 2).replace(",00", ""), ha="center",
                va="center", fontsize=8.5, color="white", fontweight="bold", zorder=4)
    ax.text(10.5, 6.6, f"somme des 20 déductions : 100 € ; ce qu'elles valent aujourd'hui : "
            f"{fr(sum(actuel))} €", ha="center", fontsize=10, color=BLEU, fontweight="bold")
    ax.set_xlim(0.3, n + 0.7)
    ax.set_ylim(0, 7.4)
    ax.set_xticks([1, 5, 10, 15, 20])
    ax.set_xlabel("année")
    ax.set_yticks([0, 1, 2, 3, 4, 5], ["0 €", "1 €", "2 €", "3 €", "4 €", "5 €"])
    ax.legend(loc="upper right", bbox_to_anchor=(1.0, 0.86), fontsize=9, frameon=False,
              handlelength=1.0)
    grille(ax)
    titre(ax, "Cent euros déduits sur vingt ans n'en valent que soixante-deux aujourd'hui",
          "Machine de 100 € amortie sur vingt ans : la déduction fiscale de chaque année et sa "
          "valeur actuelle.")
    fin(fig, "c8_amortissement.png",
        "Calcul arithmétique, au taux d'actualisation de 5 %. Dispositif emprunté aux "
        "publications de la Tax Foundation sur la récupération des coûts.",
        "Note : un euro déduit dans dix ans vaut 61 centimes aujourd'hui, parce qu'un euro placé "
        "à 5 % aujourd'hui en vaudrait 1,63 dans dix ans. Amortie sur vingt ans, la machine n'est "
        "donc déduite qu'à hauteur de 62 € en valeur d'aujourd'hui : l'entreprise est imposée "
        "comme si la machine n'avait coûté que 62 €. Sur 40 ans, la valeur tombe à 43 € ; "
        "déduite immédiatement, elle reste à 100 €.")


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


# c10 retirée : ses montants étaient saisis à la main et ne se reconstituaient pas à partir de
# la National Tax List. Elle est remplacée par r12 (graphiques_reels.py), construite sur les
# catégories de recettes de l'OCDE.

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





# ================================================================= second jeu
# ------------------------- c12 : où se trouve le sommet des recettes
def c12():
    fig, ax = plt.subplots(figsize=(10.6, 5.2))
    taux = [t / 200 for t in range(0, 199)]
    series = ((1.0, "#001f5c", "élasticité 1,00"), (0.5, BLEU, "élasticité 0,50"),
              (0.25, "#7fa4e0", "élasticité 0,25"))
    for i, (e, c, lab) in enumerate(series):
        ys = [100 * t * (1 - t) ** e / max(x * (1 - x) ** e for x in taux) for t in taux]
        ax.plot([t * 100 for t in taux], ys, color=c, lw=2.5 if e == 0.5 else 1.7, zorder=3)
        ts = 1 / (1 + e)
        ax.plot([ts * 100], [100], "o", ms=6.5, color=c, markeredgecolor=SURFACE,
                markeredgewidth=1.6, zorder=4)
        ax.annotate(f"sommet\nà {fr(ts * 100)} %", (ts * 100, 100), xytext=(0, 12),
                    textcoords="offset points", ha="center", fontsize=9.5, color=c,
                    fontweight="bold", linespacing=1.4, path_effects=HALO)
        xl = 28.0
        yl = 100 * (xl / 100) * (1 - xl / 100) ** e / max(x * (1 - x) ** e for x in taux)
        ax.annotate(lab, (xl, yl), xytext=(0, 11 if e > 0.3 else -16),
                    textcoords="offset points", ha="center", fontsize=9.5, color=c,
                    fontweight="bold", path_effects=HALO, zorder=5)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 128)
    ax.set_xlabel("taux de l'impôt")
    ax.xaxis.set_major_formatter(PCT)
    ax.set_yticks([0, 25, 50, 75, 100], ["0", "25", "50", "75", "100"])
    grille(ax)
    titre(ax, "Le sommet des recettes ne dépend que de l'élasticité de l'assiette",
          "Recettes d'un impôt proportionnel sur une assiette dont l'élasticité au taux net est "
          "constante, en indice 100 au maximum.")
    fin(fig, "c12_sommet_recettes.png",
        "Calcul arithmétique. L'assiette vaut (1 − t) puissance e ; les recettes valent donc "
        "t (1 − t) puissance e, maximales en t = 1 / (1 + e).",
        "Lecture : ce sont des courbes de Laffer. Avec une élasticité de 0,5, les recettes sont "
        "maximales à un taux de 67 % ; en dessous, monter le taux rapporte toujours quelque chose, "
        "de moins en moins ; au-dessus, il fait baisser les recettes. L'indice 100 marque le "
        "maximum de chaque courbe : la figure situe le sommet, elle ne dit rien du montant des "
        "recettes.")


# -------------- c13 : les huit leçons de Mankiw, théorie et pratique
LECONS = [
    ("Le barème optimal dépend de la distribution des capacités", "fondation"),
    ("Le taux marginal optimal peut décroître en haut de l'échelle", "partielle"),
    ("Un taux unique avec transfert forfaitaire peut être proche de l'optimum", "convergence"),
    ("L'ampleur optimale de la redistribution croît avec l'inégalité", "convergence"),
    ("L'impôt devrait dépendre de caractéristiques personnelles observables", "divergence"),
    ("Seuls les biens finals doivent être taxés, et uniformément", "convergence"),
    ("Le revenu du capital ne devrait pas être taxé, au moins en espérance", "partielle"),
    ("En économie dynamique, l'impôt optimal dépend de l'historique", "divergence"),
]
ETAT = {"convergence": (VERT, "la pratique a suivi"), "partielle": (OCRE, "en partie seulement"),
        "divergence": (BRIQUE, "la pratique n'a pas suivi"),
        "fondation": (GRIS, "résultat de cadrage, non testable")}


def c13():
    fig, ax = plt.subplots(figsize=(10.4, 5.4))
    for i, (txt, etat) in enumerate(LECONS):
        y = len(LECONS) - 1 - i
        c, lab = ETAT[etat]
        ax.add_patch(Rectangle((0, y - 0.34), 0.42, 0.68, facecolor=c, edgecolor="none"))
        ax.text(0.62, y, f"{i + 1}.", fontsize=11, color=INK2, va="center", ha="right")
        ax.text(0.85, y, txt, fontsize=11, color=INK, va="center")
        ax.text(12.3, y, lab, fontsize=10.5, color=c, va="center", ha="right",
                fontweight="bold" if etat != "fondation" else "normal")
    ax.set_xlim(0, 12.3)
    ax.set_ylim(-0.8, len(LECONS) - 0.2)
    ax.axis("off")
    fig.subplots_adjust(left=0.02, right=0.98, top=0.88, bottom=0.04)
    titre(ax, "Les huit leçons de la théorie, et ce que la pratique en a fait",
          "Synthèse de Mankiw, Weinzierl et Yagan (2009), qui comparent chaque enseignement de la "
          "théorie de la taxation optimale\nà l'évolution observée des systèmes fiscaux de l'OCDE.")
    fin(fig, "c13_lecons_mankiw.png",
        "Source : N. G. Mankiw, M. Weinzierl et D. Yagan, « Optimal Taxation in Theory and "
        "Practice », Journal of Economic Perspectives 23(4), 2009.",
        "Note : les auteurs posent la question dans les deux sens. Là où la pratique n'a pas "
        "suivi, soit les gouvernements tardent à comprendre, soit la théorie omet quelque chose "
        "que la tradition des finances publiques connaît — le principe du bénéfice et l'équité "
        "horizontale, qu'aucun modèle standard ne contient.")


# ------------------- c14 : la mobilité dans la distribution des revenus
# Insee Analyses n° 82 (2023), figure 2a : M[d][o] = % des personnes du cinquième o en 2003
# qui se trouvent dans le cinquième d en 2019 (chaque colonne o totalise 100).
MOBILITE = [[62.2, 22.7, 7.7, 4.0, 3.5], [21.9, 37.5, 25.0, 11.8, 3.9],
            [9.4, 25.0, 35.0, 21.8, 8.8], [4.3, 11.0, 25.0, 39.2, 20.5],
            [2.3, 3.8, 7.4, 23.2, 63.4]]
QUINT = ["20 % les plus modestes", "2e cinquième", "3e cinquième", "4e cinquième",
         "20 % les plus aisés"]
COUL_Q = ["#7a1f1f", "#c97a6b", "#d9d9d9", "#7f9fd1", "#0b2a61"]


def c14():
    """Ce que sont devenus en 2019 les membres de chaque cinquième de revenu de 2003 : une barre
    par cinquième de départ, découpée selon le cinquième d'arrivée."""
    fig, ax = plt.subplots(figsize=(10.2, 4.9))
    for o in range(5):
        g = 0
        for d in range(5):
            v = MOBILITE[d][o]
            ax.barh(o, v, left=g, color=COUL_Q[d], height=0.64, edgecolor=SURFACE, lw=1.0,
                    zorder=2)
            if v >= 7:
                ax.text(g + v / 2, o, fr(v), ha="center", va="center", fontsize=9.5,
                        color="white" if d in (0, 4) else INK,
                        fontweight="bold" if d == o else "normal", zorder=3)
            g += v
    ax.set_yticks(range(5), [f"{q}\nen 2003" for q in QUINT], fontsize=9)
    ax.invert_yaxis()
    ax.set_xlim(0, 100.5)
    ax.xaxis.set_major_formatter(PCT)
    ax.set_xlabel("position des mêmes personnes en 2019")
    for s_ in ("left", "top", "right"):
        ax.spines[s_].set_visible(False)
    ax.tick_params(left=False)
    ax.legend(handles=[Rectangle((0, 0), 1, 1, color=c) for c in COUL_Q],
              labels=["20 % les plus modestes", "2e", "3e", "4e", "20 % les plus aisés"],
              title="cinquième en 2019", ncol=5, loc="upper center", bbox_to_anchor=(0.45, -0.2),
              frameon=False, fontsize=8.5, title_fontsize=8.5, handlelength=1.0,
              columnspacing=1.0)
    titre(ax, "Seize ans plus tard, deux tiers des plus aisés le sont encore",
          "Position en 2019 des personnes classées dans chaque cinquième de revenu en 2003, en %.")
    fin(fig, "c14_mobilite.png",
        "Source : Insee-DGFiP, POTE panélisé 2003-2020 ; T. Loisel et M. Sicsic, « Peu de "
        "mobilité dans l'échelle des revenus entre 2003 et 2019 », Insee Analyses n° 82, 2023, "
        "figure 2a.",
        "Champ : personnes âgées de 25 à 49 ans en 2003, présentes chaque année de 2003 à 2020. "
        "Revenu individuel avant impôt et prestations : revenus d'activité, allocations chômage "
        "et pensions de retraite, nets de cotisations, moyennés sur deux ans. Lecture : parmi "
        "les 20 % les plus aisés de 2003, 63,4 % le sont encore en 2019 et 3,5 % sont parmi les "
        "20 % les plus modestes.")


# ----------------------- c15 : ce que la TVA taxe réellement
def c15():
    d = lire("assiette_tva.csv", ",")
    d.sort(key=lambda x: float(x["taux_de_couverture"]))
    fig, ax = plt.subplots(figsize=(10.8, 6.4))
    y = list(range(len(d)))
    cou = [BLEU if x["code"] == "FR" else "#C9CDD2" for x in d]
    ax.barh(y, [float(x["taux_de_couverture"]) for x in d], color=cou, height=0.72, zorder=2)
    for i, x in enumerate(d):
        v = float(x["taux_de_couverture"])
        ax.text(v + 1.1, i, fr(v, 1) + " %", va="center", fontsize=9,
                color=BLEU if x["code"] == "FR" else INK2,
                fontweight="bold" if x["code"] == "FR" else "normal")
        ax.text(2, i, f"taux normal {fr(float(x['taux_normal']), 1)} %", va="center",
                fontsize=8.2, color="white" if v > 60 else INK2)
    ax.set_yticks(y, [x["pays"] for x in d], fontsize=9.5)
    for t, x in zip(ax.get_yticklabels(), d):
        if x["code"] == "FR":
            t.set_color(BLEU)
            t.set_fontweight("bold")
    ax.set_xlim(0, 100)
    ax.xaxis.set_major_formatter(PCT)
    grille(ax, "x")
    ax.spines["left"].set_visible(False)
    ax.tick_params(left=False)
    titre(ax, "La TVA française ne rapporte que les deux tiers de ce que son taux laisse croire",
          "Recettes de TVA rapportées à ce qu'elles seraient si toute la consommation des ménages "
          "était taxée au taux normal, 2024.")
    fin(fig, "c15_assiette_tva.png",
        "Sources : Eurostat, gov_10a_taxag catégorie D211 et nama_10_gdp poste P31_S14_S15, "
        "données 2024 ; taux normaux de janvier 2026 relevés par la Tax Foundation.",
        "Note : l'écart à 100 % mesure ensemble les taux réduits, les exonérations et ce qui "
        "échappe. Il ne les sépare pas. La comparaison reste significative parce que le "
        "dénominateur est le même pour tous les pays, mais le niveau dépend de la définition "
        "retenue de la consommation : élargie à la consommation publique, le ratio français "
        "tomberait autour de la moitié.")


# ------------- c16 : le coin fiscal à trois niveaux de salaire
def c16():
    d = lire("coin_par_niveau.csv", ",")
    garde = {"FRA", "DEU", "BEL", "AUT", "ITA", "SWE", "DNK", "NLD", "GBR", "USA",
             "OECD_REP", "HUN"}
    d = [x for x in d if x["code"] in garde]
    fig, ax = plt.subplots(figsize=(10.6, 6.0))
    xs = [0, 1, 2]
    bouts = []
    for x in d:
        vs = [float(x["aw67"]), float(x["aw100"]), float(x["aw167"])]
        fr_ = x["code"] == "FRA"
        oc = x["code"] == "OECD_REP"
        c = BLEU if fr_ else (GRIS if oc else "#C4C8CE")
        ax.plot(xs, vs, color=c, lw=2.6 if fr_ else (1.8 if oc else 1.2),
                marker="o", ms=5.5 if fr_ else 3.5, zorder=4 if fr_ else 2,
                markeredgecolor=SURFACE, markeredgewidth=1.0)
        bouts.append([vs[2], x["pays"], c, fr_ or oc])
        if fr_:
            for xx, v in zip(xs, vs):
                ax.annotate(fr(v, 1), (xx, v), xytext=(0, 10), textcoords="offset points",
                            ha="center", fontsize=9.5, color=BLEU, fontweight="bold",
                            path_effects=HALO)
    bouts.sort(key=lambda b: b[0])
    for i in range(1, len(bouts)):
        if bouts[i][0] - bouts[i - 1][0] < 1.9:
            bouts[i][0] = bouts[i - 1][0] + 1.9
    for yy, nom, c, gras in bouts:
        ax.text(2.06, yy, nom, va="center", fontsize=9 if gras else 8.4,
                color=c if gras else MUTED, fontweight="bold" if gras else "normal")
    ax.set_xticks(xs, ["67 % du salaire moyen", "salaire moyen", "167 % du salaire moyen"],
                  fontsize=9.5)
    ax.set_xlim(-0.12, 2.75)
    ax.set_ylim(20, 64)
    ax.yaxis.set_major_formatter(PCT)
    grille(ax)
    titre(ax, "Le coin fiscal français est élevé dès le bas de l'échelle, et le reste",
          "Coin fiscal moyen d'un célibataire sans enfant, en % du coût du travail, 2025.")
    fin(fig, "c16_coin_trois_niveaux.png",
        "Source : OCDE, Taxing Wages, indicateurs comparatifs, données 2025.",
        "Note : la pente de chaque ligne mesure la progressivité du prélèvement sur le travail. "
        "Celle de la France est modérée, mais elle part d'un niveau que peu de pays atteignent au "
        "salaire moyen : l'écart français tient au niveau de départ plus qu'à la progressivité.")


# ------------- c17 : les impôts sur la production en France depuis 1995
def c17():
    from graphiques import ANS, serie
    fig, ax = plt.subplots(figsize=(10.6, 5.2))
    for code, c, lab in (("D29", BLEU, "Autres impôts sur la production"),
                         ("D51", VERT, "Impôts courants sur le revenu"),
                         ("D21", OCRE, "Impôts sur les produits")):
        ys = serie(code)
        ax.plot(ANS, ys, color=c, lw=2.6 if code == "D29" else 1.5, zorder=3)
        ax.text(ANS[-1] + 0.4, ys[-1], f"{lab}  {fr(ys[-1], 1)}", va="center", fontsize=9.5,
                color=c, fontweight="bold" if code == "D29" else "normal")
    ax.set_xlim(1995, 2037)
    ax.set_ylim(0, 16)
    ax.set_xticks([1995, 2000, 2005, 2010, 2015, 2020, 2024])
    ax.yaxis.set_major_formatter(PCT)
    grille(ax)
    ax.annotate("suppression progressive\nde la CVAE", xy=(2022, 4.7), xytext=(2011.5, 1.7),
                fontsize=9, color=INK2, linespacing=1.45,
                arrowprops=dict(arrowstyle="->", color=GRIS, lw=0.9,
                                connectionstyle="arc3,rad=-0.25"))
    titre(ax, "Les impôts sur la production n'ont pas reculé en trente ans",
          "Trois catégories de prélèvements en % du PIB, France, 1995-2024.")
    fin(fig, "c17_production_depuis_1995.png",
        "Source : Eurostat, National Tax List France, catégories SEC D21, D29 et D51 ; PIB "
        "Eurostat nama_10_gdp.",
        "Note : la catégorie D29 rassemble les prélèvements que l'entreprise acquitte "
        "indépendamment de son résultat. Elle valait 4,1 points de PIB en 1995 et en vaut 4,4 "
        "en 2024, malgré la suppression progressive de la cotisation sur la valeur ajoutée des "
        "entreprises engagée en 2021. Son contenu diffère d'un pays à l'autre, ce qui rend les "
        "comparaisons internationales de cet agrégat fragiles.")


# ------------- c18 : le taux effectif sur l'épargne selon le support
SUPPORTS = [("Livret A, LDDS", 0.0), ("PEA après cinq ans", 17.2),
            ("Assurance vie, dans l'abattement", 17.2), ("Prélèvement forfaitaire unique", 30.0),
            ("Revenu foncier, taux marginal 30 %", 47.2),
            ("Revenu foncier, taux marginal 41 %", 58.2)]


def c18():
    r, infl = 3.0, 2.0
    k = (r + infl) / r
    fig, ax = plt.subplots(figsize=(11.0, 5.6))
    y = list(range(len(SUPPORTS)))[::-1]
    nom = [s[1] for s in SUPPORTS]
    eff = [min(s[1] * k, 115) for s in SUPPORTS]
    ax.barh(y, eff, color=[BRIQUE if e > 60 else (OCRE if e > 30 else VERT) for e in eff],
            height=0.6, zorder=2)
    ax.barh(y, nom, color="#8C8C8C", height=0.24, zorder=3)
    for yy, n, e in zip(y, nom, eff):
        ax.text(e + 1.4, yy, fr(e, 1) + " %", va="center", fontsize=10.5, fontweight="bold",
                color=BRIQUE if e > 60 else (OCRE if e > 30 else VERT))
        if n > 0:
            ax.text(n - 1.4, yy, fr(n, 1) + " %", va="center", ha="right", fontsize=8.6,
                    color="white" if n > 20 else INK2)
    ax.set_yticks(y, [s[0] for s in SUPPORTS], fontsize=9.5)
    ax.set_xlim(0, 112)
    ax.xaxis.set_major_formatter(PCT)
    grille(ax, "x")
    ax.spines["left"].set_visible(False)
    ax.tick_params(left=False)
    ax.text(70, 4.6, "barre fine : taux affiché\nbarre large : taux effectif\nsur le rendement réel",
            fontsize=9, color=INK2, linespacing=1.5)
    titre(ax, "Le même rendement réel de 3 % supporte de 0 à 97 % d'impôt selon le support",
          "Taux effectif sur le rendement réel, pour un rendement réel de 3 % et une inflation de "
          "2 % par an.")
    fin(fig, "c18_supports_epargne.png",
        "Calcul arithmétique à partir des taux statutaires français. Le taux effectif vaut le "
        "taux affiché multiplié par le rapport du rendement nominal au rendement réel, soit "
        "cinq tiers dans cet exemple.",
        "Note : aucune de ces différences ne correspond à une différence économique entre les "
        "placements. Elles tiennent à l'enveloppe qui les porte. C'est la définition même d'un "
        "système non neutre, et c'est ce que l'exonération du rendement normal supprimerait "
        "d'un coup.")


# ------------- c19 : la capitalisation d'un impôt foncier dans le prix
def c19():
    fig, ax = plt.subplots(figsize=(10.6, 5.2))
    taux = [t / 100 for t in range(0, 301)]
    for d_, c, lab in ((3.0, "#7fa4e0", "taux d'actualisation 3 %"),
                       (4.0, BLEU, "taux d'actualisation 4 %"),
                       (5.0, "#001f5c", "taux d'actualisation 5 %")):
        ys = [100 * (1 - d_ / (d_ + t)) for t in taux]
        ax.plot(taux, ys, color=c, lw=2.5 if d_ == 4 else 1.6, zorder=3)
        ax.text(3.06, ys[-1], lab, va="center", fontsize=9.5, color=c,
                fontweight="bold" if d_ == 4 else "normal")
    for t in (0.5, 1.0, 2.0):
        v = 100 * (1 - 4.0 / (4.0 + t))
        ax.plot([t], [v], "o", ms=6.5, color=BLEU, markeredgecolor=SURFACE, markeredgewidth=1.6,
                zorder=4)
        ax.annotate(f"impôt de {fr(t, 1)} %\n→ valeur −{fr(v)} %", (t, v), xytext=(0, 13),
                    textcoords="offset points", ha="center", fontsize=9.5, color=BLEU,
                    fontweight="bold", linespacing=1.4, path_effects=HALO)
    ax.set_xlim(0, 4.3)
    ax.set_ylim(0, 56)
    ax.set_xticks([0, 0.5, 1, 1.5, 2, 2.5, 3],
                  ["0", "0,5 %", "1 %", "1,5 %", "2 %", "2,5 %", "3 %"])
    ax.set_xlabel("taux de l'impôt annuel sur la valeur du terrain")
    ax.yaxis.set_major_formatter(PCT)
    grille(ax)
    titre(ax, "Un impôt foncier annoncé est payé d'un coup par le propriétaire du jour",
          "Baisse immédiate de la valeur du terrain, en % de sa valeur d'avant l'annonce.")
    fin(fig, "c19_capitalisation.png",
        "Calcul arithmétique. La valeur d'un terrain est le loyer annuel actualisé ; un impôt "
        "annuel au taux t fait passer cette valeur de R/d à R/(d + t).",
        "Note : c'est la propriété qui rend cet impôt efficient — il ne pèse sur aucune décision "
        "future, puisque tous les acquéreurs suivants ont acheté moins cher — et c'est celle qui "
        "le rend politiquement brutal, puisqu'une seule génération de propriétaires acquitte la "
        "totalité. Toute réforme crédible doit traiter cette génération, et c'est pourquoi aucun "
        "gouvernement ne l'a tentée.")


# ------------- c20 : ce que recommandent les cinq revues
REVUES = ["Mirrlees\n2011", "N.-Zélande\n2019", "Irlande\n2022", "Norvège\n2022",
          "Pays-Bas\n2024"]
RECO = [
    ("TVA à base large et taux unique ou resserré", [1, 1, 1, 1, 0]),
    ("Déplacer la charge du travail vers la consommation et le patrimoine", [1, 0, 1, 0, 1]),
    ("Imposer le foncier sur sa valeur réelle, ou la valeur du terrain", [1, 0, 1, 0, 0]),
    ("Supprimer ou réduire les droits de mutation", [1, 0, 0, 0, 0]),
    ("Exonérer le rendement normal de l'épargne", [1, 0, 0, 0, 0]),
    ("Imposer plus uniformément les revenus du capital", [1, 0, 1, 1, 1]),
    ("Rétablir ou élargir l'imposition des transmissions", [1, 0, 0, 1, 1]),
    ("Éteindre l'avantage fiscal du logement occupé par son propriétaire", [1, 0, 0, 0, 1]),
    ("Faire contribuer davantage les retraités", [0, 0, 1, 0, 1]),
    ("Supprimer les effets de seuil des prestations", [1, 0, 1, 0, 0]),
    ("Mieux tarifer les externalités, prix unique du carbone", [1, 0, 0, 0, 1]),
    ("Supprimer les dépenses fiscales mal évaluées", [1, 0, 1, 0, 1]),
]


def c20():
    fig, ax = plt.subplots(figsize=(10.4, 6.4))
    n = len(RECO)
    for i, (txt, marques) in enumerate(RECO):
        y = n - 1 - i
        if i % 2 == 0:
            ax.add_patch(Rectangle((-7.6, y - 0.42), 12.9, 0.84, facecolor="#F2F1EC",
                                   edgecolor="none", zorder=1))
        ax.text(-0.25, y, txt, ha="right", va="center", fontsize=10.4, color=INK, zorder=3)
        for j, m in enumerate(marques):
            if m:
                ax.add_patch(Rectangle((j + 0.14, y - 0.27), 0.72, 0.54, facecolor=VERT,
                                       edgecolor="none", zorder=3))
    for j, r in enumerate(REVUES):
        ax.text(j + 0.5, n - 0.3, r, ha="center", va="bottom", fontsize=10.4, color=INK2,
                linespacing=1.35)
    ax.set_xlim(-7.6, 5.3)
    ax.set_ylim(-0.7, n + 0.9)
    ax.axis("off")
    fig.subplots_adjust(left=0.02, right=0.98, top=0.86, bottom=0.04)
    titre(ax, "Cinq revues indépendantes, et des recommandations qui se recoupent largement",
          "Recommandations retenues par chacune des cinq grandes revues fiscales d'ensemble des "
          "vingt dernières années.")
    fin(fig, "c20_convergence_revues.png",
        "Sources : Tax by Design (2011) ; Tax Working Group néo-zélandais (2019) ; Commission on "
        "Taxation and Welfare, Foundations for the Future (2022) ; NOU 2022:20, comité Torvik ; "
        "Belastingen in maatschappelijk perspectief (2024).",
        "Note : une case vide signifie que la recommandation n'a pas été relevée dans la source "
        "consultée, et non qu'elle a été écartée. Le mandat néo-zélandais excluait explicitement "
        "toute hausse du taux de TVA, ce qui explique la rareté de ses marques. La convergence "
        "sur l'assiette de la consommation et sur l'uniformité de la taxation du capital est le "
        "fait le plus net du tableau.")


# ------------- c21 : les taux supérieurs de l'impôt sur le revenu depuis 2000
def c21():
    d = lire("taux_superieur_ir.csv", ",")
    ans = [int(c) for c in d[0] if c.isdigit()]
    garde = {"FRA": BLEU, "DEU": GRIS, "SWE": OCRE, "GBR": VERT, "USA": BRIQUE, "EST": "#7a63a8"}
    # La base de l'OCDE publie 122,8 % pour la France en 2013. C'est un point isolé dans une série
    # qui tient sinon entre 45 et 59 pour ce pays ; on l'écarte du tracé et on le signale en note.
    ECART = {("FRA", "2013")}
    fig, ax = plt.subplots(figsize=(10.6, 5.4))
    bouts = []
    for x in d:
        if x["code"] not in garde:
            continue
        c = garde[x["code"]]
        pts = [(a, float(x[str(a)])) for a in ans
               if x.get(str(a)) and (x["code"], str(a)) not in ECART]
        ax.plot([p[0] for p in pts], [p[1] for p in pts], color=c,
                lw=2.6 if x["code"] == "FRA" else 1.6, zorder=4 if x["code"] == "FRA" else 2)
        bouts.append([pts[-1][0], pts[-1][1], f"{x['pays']}  {fr(pts[-1][1], 1)}", c,
                      x["code"] == "FRA"])
    # écartement vertical minimal des étiquettes de fin de courbe
    bouts.sort(key=lambda b: b[1])
    for i in range(1, len(bouts)):
        if bouts[i][1] - bouts[i - 1][1] < 2.6:
            bouts[i][1] = bouts[i - 1][1] + 2.6
    for xx, yy, lab, c, gras in bouts:
        ax.text(xx + 0.5, yy, lab, va="center", fontsize=9.5, color=c,
                fontweight="bold" if gras else "normal")
    ax.set_xlim(2000, 2036)
    ax.set_ylim(0, 70)
    ax.set_xticks([2000, 2005, 2010, 2015, 2020, 2025])
    ax.yaxis.set_major_formatter(PCT)
    grille(ax)
    titre(ax, "La France a abandonné douze points de taux supérieur, puis les a repris",
          "Taux statutaire supérieur de l'impôt sur le revenu des personnes, prélèvements assimilés "
          "compris, 2000-2025.")
    fin(fig, "c21_taux_superieurs.png",
        "Source : OCDE, base de données fiscale, taux statutaire supérieur de l'impôt sur le "
        "revenu des personnes physiques.",
        "Note : le taux français passe de 58,3 % en 2000 à 46,7 % en 2010, puis remonte à 55,4 % "
        "où il se maintient depuis. La valeur publiée pour la France en 2013, 122,8 %, est "
        "écartée du tracé : c'est un point isolé dans une série qui tient sinon entre 45 et 59 "
        "pour ce pays, et la source ne documente pas ce qui le produit. L'Estonie applique un taux unique depuis sa réforme des "
        "années 1990. Un taux statutaire ne dit rien de l'assiette à laquelle il s'applique, et "
        "c'est précisément l'objet du module 1 : deux pays au même taux affiché peuvent avoir des "
        "élasticités très différentes selon la porosité de leur assiette.")


# ----------------------------- c22 : la TVA sur une vie entière, une personne
VIE = [("jeune actif", 20, 24), ("milieu de carrière", 50, 40), ("retraité", 18, 24)]
TVA_EFF = 0.15   # TVA rapportée à la dépense, compte tenu des taux réduits


def c22():
    """Une même personne à trois âges : elle emprunte jeune, épargne au milieu de sa carrière,
    puise dans son épargne à la retraite. Sur la vie entière, elle consomme ce qu'elle gagne."""
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(12.4, 5.0), gridspec_kw={"width_ratios": [1.25, 1]})
    x = range(3)
    w = 0.36
    a1.bar([i - w / 2 for i in x], [v[1] for v in VIE], width=w * 0.94, color=GRIS, zorder=2,
           label="revenu")
    a1.bar([i + w / 2 for i in x], [v[2] for v in VIE], width=w * 0.94, color=OCRE, zorder=2,
           label="dépense de consommation")
    for i, (_, r, c) in enumerate(VIE):
        a1.text(i - w / 2, r + 1, f"{r}", ha="center", fontsize=9.5, color=INK2)
        a1.text(i + w / 2, c + 1, f"{c}", ha="center", fontsize=9.5, color=OCRE, fontweight="bold")
    for i, txt in enumerate(["emprunte 4", "épargne 10", "puise 6"]):
        a1.text(i, 63, txt, ha="center", va="center", fontsize=8.8, color=INK2)
    a1.set_xticks(list(x), ["jeune actif", "milieu de\ncarrière", "retraité"], fontsize=9.5)
    a1.set_ylim(0, 80)
    a1.set_ylabel("milliers d'euros par an")
    a1.legend(loc="upper center", ncol=2, fontsize=9, frameon=False, handlelength=1.0)
    grille(a1)
    panneau(a1, "Une même personne à trois âges de sa vie")

    taux = [TVA_EFF * c / r * 100 for _, r, c in VIE]
    a2.bar(list(x), taux, width=0.56, color=[BRIQUE, BLEU, BRIQUE], zorder=2)
    for i, t in enumerate(taux):
        a2.text(i, t + 0.5, f"{fr(t)} %", ha="center", fontsize=10.5, fontweight="bold",
                color=BRIQUE if i != 1 else BLEU)
    vie = TVA_EFF * sum(c for *_, c in VIE) / sum(r for _, r, _ in VIE) * 100
    a2.axhline(vie, color=INK, lw=1.0, ls=(0, (4, 3)), zorder=3)
    a2.text(2.36, vie + 0.7, f"sur toute la\nvie : {fr(vie)} %", ha="left", va="bottom",
            fontsize=9, color=INK, linespacing=1.2)
    a2.set_xlim(-0.55, 3.25)
    a2.set_xticks(list(x), ["jeune actif", "milieu de\ncarrière", "retraité"], fontsize=9)
    a2.set_ylim(0, 24)
    a2.yaxis.set_major_formatter(PCT)
    a2.set_ylabel("TVA payée, en % du revenu de l'année")
    grille(a2)
    panneau(a2, "La TVA rapportée au revenu de l'année")
    fig.subplots_adjust(wspace=0.32)
    fin(fig, "c22_tva_cycle_de_vie.png",
        "Exemple numérique : trois périodes de même durée ; la TVA représente 15 % de la dépense "
        "de consommation, compte tenu des taux réduits.",
        "Note : la personne gagne 88 000 € et dépense 88 000 € sur ses trois périodes. Une "
        "photographie prise à une date donnée mêle des jeunes, des actifs et des retraités : les "
        "revenus les plus bas y paient la plus forte part de TVA, et l'impôt paraît régressif. "
        "Sur la vie entière, la même personne paie 15 % de ce qu'elle gagne.")


# ---------------- c23 : les taux d'impôt sur les sociétés ont baissé, les recettes ont monté
def c23():
    """Moyenne simple de dix-huit pays de l'OCDE observés sans interruption de 1981 à 2023
    (la Norvège est exclue : ses recettes contiennent l'imposition du pétrole). À gauche le taux
    légal, à droite la recette en % du PIB, avec la France."""
    taux = {x["code"]: {int(k): float(v) for k, v in x.items() if k.isdigit() and v}
            for x in lire("is_taux_1980_2025.csv", ",")}
    rec = {x["code"]: {int(k): float(v) for k, v in x.items() if k.isdigit() and v}
           for x in lire("is_recettes_1965_2024.csv")}
    ans = list(range(1981, 2024))
    pan = sorted(c for c in rec if c in taux and c not in ("NOR", "OECD_REP")
                 and all(a in rec[c] and a in taux[c] for a in ans))
    moy_t = [sum(taux[c][a] for c in pan) / len(pan) for a in ans]
    moy_r = [sum(rec[c][a] for c in pan) / len(pan) for a in ans]
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(12.4, 4.8))
    for ax, moy, fra, lim in ((a1, moy_t, [taux["FRA"][a] for a in ans], 60),
                              (a2, moy_r, [rec["FRA"][a] for a in ans], 4.8)):
        ax.plot(ans, moy, color=BLEU, lw=2.4, zorder=3)
        ax.plot(ans, fra, color=GRIS, lw=1.4, zorder=2)
        ax.set_xlim(1980, 2024)
        ax.set_ylim(0, lim)
        grille(ax)
    a1.yaxis.set_major_formatter(PCT)
    a1.text(1981, moy_t[0] + 5, f"{fr(moy_t[0])} %", fontsize=10, color=BLEU,
            fontweight="bold")
    a1.text(2023, moy_t[-1] - 4.5, f"{fr(moy_t[-1])} %", fontsize=10, color=BLEU,
            fontweight="bold", ha="right")
    a1.text(2002, 20.5, "moyenne de 18 pays", fontsize=9, color=BLEU)
    a1.text(2005, 39.5, "France", fontsize=9, color=INK2)
    panneau(a1, "Taux légal de l'impôt sur les sociétés")
    a2.set_yticks([0, 1, 2, 3, 4], ["0 %", "1 %", "2 %", "3 %", "4 %"])
    a2.text(1982, moy_r[0] - 0.42, f"{fr(moy_r[0], 1)} %", fontsize=10, color=BLEU,
            fontweight="bold")
    a2.text(2023, moy_r[-1] + 0.2, f"{fr(moy_r[-1], 1)} %", fontsize=10, color=BLEU,
            fontweight="bold", ha="right")
    a2.text(1984, 3.3, "moyenne de 18 pays", fontsize=9, color=BLEU)
    a2.text(2011.5, 1.55, "France", fontsize=9, color=INK2)
    panneau(a2, "Recettes de l'impôt sur les sociétés, en % du PIB")
    fig.subplots_adjust(wspace=0.25)
    fin(fig, "c23_taux_et_recettes_is.png",
        "Sources : Tax Foundation, taux d'impôt sur les sociétés 1980-2025 ; OCDE, Revenue "
        "Statistics, catégorie 1200, en % du PIB.",
        "Note : moyenne simple des dix-huit pays de l'OCDE pour lesquels les deux séries sont "
        "complètes de 1981 à 2023 : " + ", ".join(pan) + ". La Norvège est exclue, ses recettes "
        "comprenant l'imposition des bénéfices pétroliers. La hausse des recettes ne mesure pas "
        "le seul effet de l'élargissement des assiettes : elle reflète aussi la part croissante "
        "des bénéfices dans l'économie et des activités exercées en société.")


# ------------- c24 : Carey et Rabesona, le taux implicite d'imposition du capital, 1975-2000
def c24():
    """Impôts sur les revenus du capital rapportés à l'excédent net d'exploitation, seize pays de
    l'OCDE aux données complètes (Carey et Rabesona, 2002, tableau A2)."""
    d = lire("carey_rabesona_2002_capital.csv")
    per = ["net_1975_1980", "net_1980_1990", "net_1990_2000"]
    x = [0, 1, 2]
    fig, ax = plt.subplots(figsize=(8.2, 5.2))
    for r in d:
        v = [float(r[k]) for k in per]
        if r["code"] == "FRA":
            continue
        ax.plot(x, v, color="#C9CDD2", lw=1.1, zorder=1)
        if r["code"] in ("SWE", "KOR", "DEU"):
            ax.text(2.06, v[2], r["pays"], va="center", fontsize=8.5, color=INK2)
    moy = [sum(float(r[k]) for r in d) / len(d) for k in per]
    fra = [float(next(r for r in d if r["code"] == "FRA")[k]) for k in per]
    ax.plot(x, moy, color=INK, lw=2.4, ls=(0, (5, 3)), zorder=3, marker="o", ms=5)
    ax.plot(x, fra, color=BLEU, lw=2.8, zorder=4, marker="o", ms=6)
    for i in (0, 1):
        ax.text(i, moy[i] - 4.2, fr(moy[i], 1), ha="center", fontsize=9.5, color=INK,
                fontweight="bold")
        ax.text(i, fra[i] + 2.4, fr(fra[i], 1), ha="center", fontsize=9.5, color=BLEU,
                fontweight="bold")
    ax.text(2.07, fra[2], f"France {fr(fra[2], 1)}", va="center", fontsize=9.5, color=BLEU,
            fontweight="bold")
    ax.text(2.07, moy[2], f"moyenne {fr(moy[2], 1)}", va="center", fontsize=9.5, color=INK,
            fontweight="bold")
    ax.set_xticks(x, ["1975-1980", "1980-1990", "1990-2000"])
    ax.set_xlim(-0.15, 2.62)
    ax.set_ylim(0, 80)
    ax.yaxis.set_major_formatter(PCT)
    grille(ax)
    titre(ax, "La charge effective sur le capital a augmenté pendant que les taux baissaient",
          "Impôts sur les revenus du capital, en % de l'excédent net d'exploitation, seize pays "
          "de l'OCDE.")
    fin(fig, "c24_carey_rabesona.png",
        "Source : D. Carey et J. Rabesona, « Tax Ratios on Labour and Capital Income and on "
        "Consumption », OECD Economic Studies n° 35, 2002, tableau A2 (méthode révisée).",
        "Note : moyennes par période des pays dont les données sont complètes depuis 1975. Le "
        "ratio rapporte tous les impôts sur les revenus du capital, y compris ceux des ménages, "
        "au revenu du capital mesuré par la comptabilité nationale. Il dépend de conventions : "
        "si l'on attribue au travail une partie du revenu des indépendants, la hausse moyenne "
        "est réduite d'environ deux points, et celle de la France presque entièrement.")


if __name__ == "__main__":
    for f in (c1, c2, c3, c4, c5, c6, c7, c8, c9, c11,
              c12, c13, c14, c15, c16, c17, c18, c19, c20, c21, c22, c23, c24):
        f()
