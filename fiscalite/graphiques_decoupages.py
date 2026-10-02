"""
Graphiques des découpages analytiques (chapitre 3), à partir de
donnees/classification_prelevements.csv produit par classification.py.

    python graphiques_decoupages.py
"""
import csv
import json
from collections import defaultdict
from pathlib import Path

import matplotlib.pyplot as plt

from graphiques import (BLEU, GRID, HALO, INK, INK2, MUTED, PAL, PCT, SEQ, SURFACE,
                        etiquette, fin, grille, titre)

HERE = Path(__file__).resolve().parent
OUT = HERE / "figures"
SRC = ("Source : classification de l'auteur appliquée à la liste Eurostat des prélèvements français et aux cotisations "
       "effectives, 2024. Détail et motifs dans donnees/classification_prelevements.csv.")

L = list(csv.DictReader(open(HERE / "donnees" / "classification_prelevements.csv", encoding="utf-8")))
for r in L:
    r["meur"] = float(r["meur"])
G = json.loads((HERE / "donnees" / "pib_france_cp_meur.json").read_text())["2024"]
TOT = sum(r["meur"] for r in L)

LIB = {"travail": "Travail : cotisations et taxes sur les salaires", "conso_menages": "Consommation des ménages",
       "revenu_global": "Revenu global : impôt sur le revenu, CSG, CRDS", "profit": "Bénéfice des sociétés",
       "stock_capital": "Détention de patrimoine", "energie": "Énergie",
       "intrant_entreprises": "Intrants et facteurs de production", "transmission": "Transmission",
       "transaction": "Transaction", "revenu_capital": "Revenus du capital des ménages",
       "rente": "Rentes", "autre": "Non classé"}


def barres(ax, libelles, valeurs, couleurs, unite="% du PIB", fmt="{:.2f}", sep=0.015):
    y = list(range(len(valeurs)))
    ax.barh(y, valeurs, height=0.74, color=couleurs, zorder=3)
    for i, v in enumerate(valeurs):
        ax.text(v + max(valeurs) * sep, i, fmt.format(v).replace(".", ","), va="center", fontsize=9.5, color=INK2)
    ax.set_yticks(y); ax.set_yticklabels(libelles, fontsize=10)
    ax.invert_yaxis(); grille(ax, "x")
    ax.set_xlim(0, max(valeurs) * 1.16); ax.set_xlabel(unite)
    ax.spines["left"].set_visible(False); ax.tick_params(axis="y", length=0)


# ================================================================ h1 : ce que l'on taxe
def h1():
    d = defaultdict(float)
    for r in L:
        d[r["assiette"]] += r["meur"]
    s = sorted(d.items(), key=lambda t: -t[1])
    s = [(k, v) for k, v in s if k != "autre"]
    cols = []
    for k, _ in s:
        cols.append(PAL[2] if k == "rente" else (PAL[1] if k in ("transaction", "intrant_entreprises") else SEQ[3]))
    fig, ax = plt.subplots(figsize=(10.0, 6.2))
    barres(ax, [LIB[k] for k, _ in s], [100 * v / G for _, v in s], cols)
    ax.annotate("la meilleure assiette selon la théorie :\nune rente ne réagit pas à l'impôt", (0.06, 10),
                xytext=(40, -4), textcoords="offset points", fontsize=9.5, color=PAL[2], va="center", path_effects=HALO)
    ax.annotate("la pire : taxer l'échange, et non la détention,\nbloque les mutations sans viser la richesse", (0.60, 8),
                xytext=(40, 0), textcoords="offset points", fontsize=9.5, color=PAL[1], va="center", path_effects=HALO)
    titre(ax, "Ce que la France taxe réellement, une fois les étiquettes comptables retirées",
          "1 274,9 Md€ en 2024, soit 43,4 % du PIB : les 121 impôts de la liste nationale plus les cotisations effectives,\nreclassés selon ce qu'ils atteignent en dernier ressort.")
    fin(fig, "h1_ce_que_l_on_taxe.png", SRC)


# ================================================================ h2 : efficience productive
def h2():
    cat = [("ne frappe pas d'intrant", sum(r["meur"] for r in L if r["intrant"] == "non"), "#C9CCD1"),
           ("frappe partiellement un intrant", sum(r["meur"] for r in L if r["intrant"] == "partiel"), SEQ[2]),
           ("frappe un intrant, en corrigeant un dommage",
            sum(r["meur"] for r in L if r["intrant"] == "oui" and r["correctif"] != "non"), PAL[2]),
           ("frappe un intrant sans rien corriger",
            sum(r["meur"] for r in L if r["intrant"] == "oui" and r["correctif"] == "non"), PAL[1])]
    fig, ax = plt.subplots(figsize=(10.6, 3.5))
    gauche, haut = 0.0, 0
    for lib, v, col in cat:
        p = 100 * v / G
        ax.barh([0], [p], left=[gauche], height=0.5, color=col, edgecolor=SURFACE, linewidth=1.6, zorder=3)
        txt = f"{lib}\n{v/1000:.1f} Md€  ·  {p:.2f} % du PIB".replace(".", ",")
        if p >= 5:                                   # segment large : étiquette dessous, centrée
            ax.annotate(txt, (gauche + p / 2, -0.33), ha="center", va="top", fontsize=9.5,
                        color=INK if col != "#C9CCD1" else INK2)
        else:                                        # segment étroit : étiquette au-dessus, décalée
            y = 0.52 + 0.62 * haut
            ax.plot([gauche + p / 2, gauche + p / 2], [0.26, y - 0.04], color=col, lw=0.9, zorder=2)
            ax.annotate(txt, (gauche + p / 2, y), ha="center", va="bottom", fontsize=9.5, color=col)
            haut += 1
        gauche += p
    ax.set_ylim(-1.4, 2.4); ax.set_xlim(0, 44)
    ax.set_yticks([]); ax.xaxis.set_major_formatter(PCT)
    for sp in ("left", "bottom"):
        ax.spines[sp].set_visible(False)
    ax.tick_params(axis="y", length=0)
    grille(ax, "x")
    titre(ax, "Cent dix-neuf milliards frappent directement un facteur de production",
          "Les 1 274,9 Md€ de 2024 selon qu'ils distordent ou non les décisions de production (Diamond-Mirrlees, 1971).\nTaxer un intrant n'est justifié que pour corriger un dommage, puisque celui-ci ne dépend pas de l'identité de l'émetteur.")
    fin(fig, "h2_efficience_productive.png", SRC)


# ================================================================ h3 : le détail des 77 Md€
def h3(n=16):
    s = sorted([r for r in L if r["intrant"] == "oui" and r["correctif"] == "non"], key=lambda r: -r["meur"])
    court = {"Taxes sur les salaires": "Taxe sur les salaires",
             "Contributions des entreprises à la formation professionnelle et à l'apprentissage": "Formation professionnelle et apprentissage",
             "Cotisation foncière des entreprises": "Cotisation foncière des entreprises",
             "Contribution sociale de solidarité des sociétés": "C3S, assise sur le chiffre d'affaires",
             "Cotisation patronale pour le FNAL (Fonds national d'aide au logement)": "Cotisation patronale au FNAL",
             "Contribution de solidarité pour l'autonomie": "Contribution solidarité autonomie",
             "Participation des employeurs à l'effort de construction": "Effort de construction",
             "Taxes au profit de l'Association sur la garantie des salaires": "Garantie des salaires",
             "Impositions forfaitaires sur les entreprises de réseaux": "IFER, entreprises de réseaux",
             "Taxe sur les surfaces commerciales": "Taxe sur les surfaces commerciales",
             "Taxe sur construction de bureaux et sur les locaux à usage de bureaux": "Taxe sur les bureaux",
             "Taxes sur la construction": "Taxes sur la construction",
             "Taxes sur les services professionnels hors droits de mutations": "Taxes sur les services professionnels",
             "Part sur les salaires": "Prélèvement non nommé, assis sur les salaires",
             "Taxe sur les véhicules de tourisme des sociétés": "Véhicules de tourisme des sociétés",
             "Taxe sur les services numériques": "Taxe sur les services numériques"}
    top = s[:n]
    reste = sum(r["meur"] for r in s[n:])
    libs = [court.get(r["nom"], r["nom"][:46]) for r in top] + [f"{len(s)-n} autres prélèvements"]
    vals = [r["meur"] / 1000 for r in top] + [reste / 1000]
    fig, ax = plt.subplots(figsize=(10.0, 6.4))
    barres(ax, libs, vals, [PAL[1]] * n + ["#C9CCD1"], unite="milliards d'euros, 2024", fmt="{:.1f}")
    titre(ax, "Les 77 milliards qui frappent un facteur de production sans corriger quoi que ce soit",
          "Prélèvements assis sur la masse salariale, la valeur locative des locaux ou le chiffre d'affaires.\nIls sont dus que l'entreprise gagne ou perde de l'argent, et se cumulent le long de la chaîne de production.")
    fin(fig, "h3_prelevements_sur_intrants.png", SRC)


# ================================================================ h4 : la lecture par principe
def h4():
    d = defaultdict(float)
    for r in L:
        d[r["verdict"]] += r["meur"]
    lib = {"fusionner_cotisations": "Fusionner dans un prélèvement unique sur le travail",
           "fusionner_impot_revenu": "Fusionner impôt sur le revenu, CSG et CRDS",
           "conserver_base_large": "Conserver : assiette large, taux unique",
           "refondre_rendement_normal": "Refondre pour exonérer le rendement normal",
           "refondre_fonciere": "Refondre le foncier : séparer terrain et bâti",
           "supprimer": "Supprimer", "refondre": "Refondre",
           "refondre_prix_carbone": "Unifier le prix du carbone",
           "conserver_correctif": "Conserver comme correcteur",
           "a_identifier": "À identifier avant de pouvoir juger",
           "refondre_assiette": "Refondre l'assiette des transmissions",
           "supprimer_avec_tva": "Supprimer en élargissant la TVA"}
    s = [(lib[k], d[k]) for k in sorted(d, key=lambda k: -d[k]) if k in lib]
    couleur = {"Conserver : assiette large, taux unique": PAL[2], "Conserver comme correcteur": PAL[2],
               "Supprimer": PAL[1], "Supprimer en élargissant la TVA": PAL[1],
               "À identifier avant de pouvoir juger": "#C9CCD1"}
    fig, ax = plt.subplots(figsize=(10.2, 5.8))
    barres(ax, [k for k, _ in s], [100 * v / G for _, v in s],
           [couleur.get(k, SEQ[3]) for k, _ in s])
    titre(ax, "Ce que les principes impliqueraient, prélèvement par prélèvement",
          "En % du PIB. Lecture de l'auteur, destinée à être contestée : un seul prélèvement, la TVA, passe le test sans\nréserve, et encore à condition d'unifier ses taux et de traiter ses exonérations.")
    fin(fig, "h4_lecture_par_principe.png", SRC)


if __name__ == "__main__":
    print("figures :")
    for f in (h1, h2, h3, h4):
        f()
