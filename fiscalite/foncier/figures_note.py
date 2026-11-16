"""Figures de la partie Immobilier de la note fusionnée (préfixe foncier_n, refonte du 16/11/2026).

Chiffres : synthese/sorties/calculs_foncier.json (synthese/calculs_foncier.py) et modèle foncier/simulation.py pour les
variantes de l'annexe. Couleurs : synthese/style_note.py (aujourd'hui en encre grise, réforme naïve en brique,
proposition en bleu, variante en ocre, élément secondaire en gris clair).

Lancer depuis fiscalite/, après synthese/calculs_foncier.py :
    python3 foncier/figures_note.py && FIG_NU=1 python3 foncier/figures_note.py
"""
import json
import sys
from pathlib import Path

import numpy as np
from matplotlib.patches import Patch

HERE = Path(__file__).resolve().parent
RACINE = HERE.parent
sys.path[:0] = [str(HERE), str(RACINE), str(RACINE / "synthese")]
import simulation as sm  # noqa: E402
from graphiques import ECH_TXT, fin, plt  # noqa: E402
from style_note import AUJ, ENCRE, ENCRE2, NAIF, NUANCES_BLEU, PROP, SEC, VAR, axes_propres, euros, _fr  # noqa: E402

J = json.loads((RACINE / "synthese/sorties/calculs_foncier.json").read_text(encoding="utf-8"))
TXT = 10.3                     # taille des textes que graphiques met à l'échelle (≈ 8 pt imprimés en mode nu)
plt.rcParams.update({k: TXT * ECH_TXT for k in ("xtick.labelsize", "ytick.labelsize", "axes.labelsize",
                                                 "legend.fontsize")})
SRC = ("DGFiP, REI 2024 et DVF 2023-2024 ; Insee, recensement 2022, comptes de patrimoine 2024 et Insee Analyses "
       "n° 91 ; calculs de l'auteur (synthese/calculs_foncier.py, foncier/simulation.py).")
XT = [_fr(u / 1e3, 1) for u in J["dec_pm2"]]
XLAB = "Prix médian au m² du dixième de logements (milliers d'euros), du moins cher au plus cher"
X = np.arange(10)


def pct_axe(ax, d=1):
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: _fr(v, d) + " %"))


def axe_deciles(ax, lab=True):
    ax.set_xticks(X)
    ax.set_xticklabels(XT)
    ax.set_xlim(-0.5, 9.5)
    if lab:
        ax.set_xlabel(XLAB, fontsize=TXT, color=ENCRE2)


def ligne(ax, y, col, lab, lw=1.6, ms=4.0, z=3):
    ax.plot(X, y, color=col, lw=lw, marker="o", ms=ms, mec="white", mew=0.7, zorder=z, label=lab,
            solid_capstyle="round")


def etiquette_fin(ax, y, texte, dy=0, dx=7):
    ax.annotate(texte, (9, y), xytext=(dx, dy), textcoords="offset points", va="center", ha="left", fontsize=TXT,
                color=ENCRE, annotation_clip=False)


# ---------------------------------------------------------------------------------------------------------- n01
def n01_inventaire():
    inv = J["inventaire"]
    fam = list(inv)
    fig, ax = plt.subplots(figsize=(9.0, 3.3))
    for i, f in enumerate(fam):
        g = 0.0
        for k, (lab, v) in enumerate(inv[f]):
            col = NUANCES_BLEU[min(k + 1, 5)] if len(inv[f]) > 1 else NUANCES_BLEU[1]
            ax.barh(i, v, left=g, height=0.62, color=col, edgecolor="white", lw=1.2, zorder=3)
            court = {"Taxe foncière bâtie : logements": "TF logements", "Taxe foncière bâtie : autres locaux": "TF autres",
                     "Ordures ménagères (TEOM)": "TEOM", "Cotisation foncière des entreprises": "CFE",
                     "Droits de mutation": "droits de mutation", "TVA du neuf et des terrains": "TVA"}.get(lab)
            if court and v >= 6:
                ax.text(g + v / 2, i, court, ha="center", va="center", fontsize=TXT * 0.92,
                        color="white" if k < 3 else ENCRE, zorder=4)
            g += v
        ax.text(g + 0.8, i, _fr(g, 0 if abs(g - round(g)) < 0.05 else 1), va="center", fontsize=TXT, color=ENCRE)
    ax.set_yticks(range(len(fam)))
    ax.set_yticklabels(fam)
    ax.invert_yaxis()
    ax.set_xlim(0, 76)
    ax.set_xlabel("milliards d'euros, 2024", fontsize=TXT, color=ENCRE2)
    axes_propres(ax, grille="x")
    ax.spines["left"].set_visible(False)
    ax.tick_params(axis="y", length=0)
    fin(fig, "foncier_n01_inventaire",
        "DGCL-DGFiP, note REI 2025 ; OFGL ; SDES, Compte du logement 2025 ; DGFiP Statistiques n° 43 ; calculs de "
        "l'auteur (foncier/notes/inventaire.md).",
        "Note : rendements 2024, périmètres hétérogènes. TF : taxe foncière sur les propriétés bâties (42 Md€, dont "
        "30,5 sur les logements selon le Compte du logement ; le reste par différence, non vérifié) ; TEOM : taxe "
        "d'enlèvement des ordures ménagères ; CFE : cotisation foncière des entreprises. Autres de la détention : "
        "taxes d'habitation restantes, IFI, foncier non bâti, taxe sur les bureaux d'Île-de-France, GEMAPI, taxes "
        "spéciales d'équipement. Ventes : droits de mutation, TVA du neuf et des terrains, impôt sur les "
        "plus-values immobilières et contribution de sécurité immobilière. Transmissions : part immobilière des "
        "droits de succession et de donation, estimée à 60 % (clé du CPO, aucune ventilation officielle).")


# ---------------------------------------------------------------------------------------------------------- n02
def n02_ocde():
    o = J["ocde"]
    pays = sorted(o, key=lambda k: o[k][0] + o[k][1])
    fig, ax = plt.subplots(figsize=(9.0, 4.3))
    y = np.arange(len(pays))
    h = 0.38
    det = [o[k][0] for k in pays]
    ven = [o[k][1] for k in pays]
    ax.barh(y + h / 2, det, height=h, color=NUANCES_BLEU[1], zorder=3, label="Impôts annuels sur la détention")
    ax.barh(y - h / 2, ven, height=h, color=NUANCES_BLEU[4], zorder=3, label="Impôts sur les ventes (et les titres)")
    for yi, a, b in zip(y, det, ven):
        ax.text(a + 0.03, yi + h / 2, _fr(a, 2), va="center", fontsize=TXT * 0.9, color=ENCRE)
        ax.text(b + 0.03, yi - h / 2, _fr(b, 2), va="center", fontsize=TXT * 0.9, color=ENCRE2)
    ax.set_yticks(y)
    ax.set_yticklabels(pays)
    for t in ax.get_yticklabels():
        if t.get_text() in ("France", "Moyenne OCDE"):
            t.set_fontweight("bold")
    ax.set_xlim(0, 3.2)
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: _fr(v, 1) + " %"))
    ax.set_xlabel("en % du PIB, 2023", fontsize=TXT, color=ENCRE2)
    axes_propres(ax, grille="x")
    ax.spines["left"].set_visible(False)
    ax.tick_params(axis="y", length=0)
    ax.legend(loc="lower right", frameon=False, handlelength=1.2)
    fin(fig, "foncier_n02_ocde",
        "OCDE, Revenue Statistics (API SDMX, administrations publiques), extraction du 15/11/2026, vérifiée "
        "(revue/verif_litterature_foncier.md).",
        "Note : catégorie 4100 (impôts périodiques sur la propriété immobilière ; en France, taxes foncières, taxe "
        "d'enlèvement des ordures ménagères et taxes d'habitation restantes, mais pas la CFE) et catégorie 4400 "
        "(impôts sur les transactions mobilières et immobilières ; en France, les droits sur l'immobilier en "
        "représentent environ 86 % en 2024). La moyenne de l'OCDE n'est pas encore publiée pour 2024 ; la France "
        "est alors à 1,95 % et 0,62 % du PIB.")


# ---------------------------------------------------------------------------------------------------------- n03
def n03_taux_valeur():
    fig, axs = plt.subplots(1, 2, figsize=(9.6, 3.9), gridspec_kw=dict(width_ratios=[1.35, 1], wspace=0.42))
    ax = axs[0]
    ax.bar(X, J["tfv_auj"], width=0.68, color=AUJ, zorder=3)
    for x, v in zip(X, J["tfv_auj"]):
        ax.text(x, v + 0.012, _fr(v, 2), ha="center", va="bottom", fontsize=TXT * 0.85, color=ENCRE)
    axe_deciles(ax, lab=False)
    ax.set_xlabel("Prix médian au m² du dixième de logements\n(milliers d'euros)", fontsize=TXT, color=ENCRE2)
    ax.set_ylim(0, 0.62)
    pct_axe(ax)
    ax.set_title("Par dixième de logements, selon le prix de leur commune", fontsize=TXT, color=ENCRE, loc="left")
    axes_propres(ax)
    ax = axs[1]
    v = J["tfv_villes"]
    noms = [k for k in sorted(v, key=v.get) if k not in ("Saint-Denis",)]
    y = np.arange(len(noms))
    ax.hlines(y, 0, [v[k] for k in noms], color=SEC, lw=1.0, zorder=2)
    ax.plot([v[k] for k in noms], y, "o", color=AUJ, ms=5, mec="white", mew=0.7, zorder=3)
    for yi, k in zip(y, noms):
        ax.text(v[k] + 0.04, yi, _fr(v[k], 2), va="center", fontsize=TXT * 0.85, color=ENCRE)
    ax.set_yticks(y)
    ax.set_yticklabels(noms)
    ax.set_xlim(0, 1.25)
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda u, _: _fr(u, 1) + " %"))
    ax.set_title("Dans quelques communes", fontsize=TXT, color=ENCRE, loc="left")
    axes_propres(ax, grille="x")
    ax.tick_params(axis="y", length=0)
    ax.spines["left"].set_visible(False)
    fig.text(0.07, 0.98, "Taxe foncière en % de la valeur de marché du logement", fontsize=TXT * ECH_TXT, color=ENCRE2,
             va="bottom")
    fig.subplots_adjust(top=0.86, bottom=0.2)
    fin(fig, "foncier_n03_taux_valeur", SRC,
        "Note : logements des particuliers de France métropolitaine hors Alsace-Moselle (30,5 millions). Valeur : prix "
        "médian au m² des ventes 2023-2024 de la commune × surface médiane ; taxe : rapport taxe/valeur de chaque "
        "commune en 2017 (Insee Analyses n° 91) vieilli selon la croissance de sa taxe foncière de 2017 à 2024. Hypothèse "
        "forte : à l'intérieur d'une commune, tous les logements paient le même pourcentage de leur valeur ; en réalité "
        "ce pourcentage varie aussi d'un quartier à l'autre (à Paris, de 0,074 à 0,121 % entre le premier et le "
        "neuvième dixième des quartiers en 2017).")


# ---------------------------------------------------------------------------------------------------------- n04
def n04_qui_paie():
    q = J["qui_paie"]
    noms = list(q)
    tot = sum(q.values())
    fig, ax = plt.subplots(figsize=(9.0, 2.6))
    y = np.arange(len(noms))
    ax.barh(y, [q[k] for k in noms], height=0.6, color=AUJ, zorder=3)
    for yi, k in zip(y, noms):
        ax.text(q[k] + 0.15, yi, f"{_fr(q[k], 1)} Md€ ({_fr(100*q[k]/tot)} %)", va="center", fontsize=TXT, color=ENCRE)
    ax.set_yticks(y)
    ax.set_yticklabels(noms)
    ax.invert_yaxis()
    ax.set_xlim(0, 16)
    ax.set_xlabel("milliards d'euros par an (logements des particuliers, 23,6 Md€ au total)", fontsize=TXT, color=ENCRE2)
    axes_propres(ax, grille="x")
    ax.spines["left"].set_visible(False)
    ax.tick_params(axis="y", length=0)
    fin(fig, "foncier_n04_qui_paie", SRC,
        "Note : la taxe foncière modélisée de chaque commune est répartie entre les statuts d'occupation du "
        "recensement 2022 au prorata du nombre de logements (on suppose la même taxe pour chaque logement de la "
        "commune). Logements loués par des particuliers : logements loués hors HLM.")


# ---------------------------------------------------------------------------------------------------------- n05
def n05_cycle():
    cy = J["cycle"]
    an = list(cy)
    fig, ax = plt.subplots(figsize=(8.0, 3.2))
    ax.bar(range(len(an)), [cy[a] for a in an], width=0.6, color=AUJ, zorder=3)
    for i, a in enumerate(an):
        ax.text(i, cy[a] + 0.3, _fr(cy[a], 1), ha="center", va="bottom", fontsize=TXT, color=ENCRE)
    ax.set_xticks(range(len(an)))
    ax.set_xticklabels(an)
    ax.set_ylim(0, 19.5)
    ax.set_ylabel("milliards d'euros", fontsize=TXT, color=ENCRE2)
    axes_propres(ax)
    fin(fig, "foncier_n05_cycle", "SDES, Compte du logement 2025, série T321 (droits de mutation bruts sur les logements).",
        "Note : France entière, logements seuls. Les droits sur les autres biens (locaux, terrains) ajoutent environ "
        "3 Md€ par an (différence entre le total des collectivités et les logements, non vérifiée). Sur la même "
        "période, la taxe foncière sur les logements rapporte 30,5 Md€ en 2024 et 31,6 Md€ en 2025.")


# ---------------------------------------------------------------------------------------------------------- n06
def n06_naif():
    fig, ax = plt.subplots(figsize=(9.0, 3.9))
    w = 0.38
    ax.bar(X - w / 2, J["naif_dtf"], width=w, color=SEC, zorder=3, label="Hausse de taxe foncière")
    ax.bar(X + w / 2, J["naif_tot"], width=w, color=NAIF, zorder=3,
           label="Hausse de taxe foncière moins baisse des droits")
    ax.axhline(0, color=ENCRE, lw=0.8, zorder=4)
    for x, v in zip(X, J["naif_tot"]):
        ax.text(x + w / 2, v + (6 if v >= 0 else -6), f"{v:+.0f}".replace("-", "−"), ha="center",
                va="bottom" if v >= 0 else "top", fontsize=TXT * 0.85, color=ENCRE)
    axe_deciles(ax)
    ax.set_ylim(-290, 290)
    ax.yaxis.set_major_formatter(euros)
    ax.set_ylabel("€ par logement et par an", fontsize=TXT, color=ENCRE2)
    axes_propres(ax)
    ax.legend(loc="lower left", frameon=False, handlelength=1.2)
    fin(fig, "foncier_n06_naif", SRC,
        "Note : réforme naïve : droits de mutation sur les logements divisés par deux (5,7 Md€), compensés par une "
        "hausse de 24 % de la taxe foncière actuelle dans toutes les communes, sans réaction des ventes. La baisse des "
        "droits est rapportée à l'ensemble des logements de la commune : c'est ce que paie en moyenne chaque année un "
        "logement au fil des ventes. Un ménage qui ne vend ni n'achète paie la seule hausse de taxe foncière (barres "
        "grises).")


# ---------------------------------------------------------------------------------------------------------- n07
def n07_taux_trois():
    fig, ax = plt.subplots(figsize=(9.0, 3.9))
    ligne(ax, J["tfv_auj"], AUJ, "Aujourd'hui", lw=1.4)
    ligne(ax, J["tfv_naif"], NAIF, "Réforme naïve", lw=1.4)
    ligne(ax, J["prop"]["tfv"], PROP, "Proposition", lw=2.2, ms=4.6, z=5)
    etiquette_fin(ax, J["tfv_naif"][-1], "Réforme naïve", dy=2)
    etiquette_fin(ax, J["prop"]["tfv"][-1], "Proposition", dy=5)
    etiquette_fin(ax, J["tfv_auj"][-1], "Aujourd'hui", dy=-7)
    axe_deciles(ax)
    ax.set_ylim(0, 0.72)
    pct_axe(ax)
    ax.set_ylabel("taxe foncière en % de la valeur", fontsize=TXT, color=ENCRE2)
    axes_propres(ax)
    fin(fig, "foncier_n07_taux_trois", SRC,
        "Note : proposition : droits divisés par deux sur toutes les ventes d'immeubles ; chaque commune garde sa "
        "recette de taxe foncière, répartie sur la valeur de marché avec un taux sur le terrain quatre fois plus élevé "
        "que sur le bâti ; un taux national sur la valeur de tous les terrains privés (environ 0,12 % de la valeur "
        "des terrains, 0,15 % sur les valeurs du modèle) remplace les droits perdus. Réforme naïve : figure "
        "précédente. Sans réaction des ventes.")


# ---------------------------------------------------------------------------------------------------------- n08
def n08_variation():
    fig, axs = plt.subplots(1, 2, figsize=(10.2, 4.0), sharey=True, gridspec_kw=dict(wspace=0.08))
    for ax, cle, titre in ((axs[0], "dtf", "Taxe foncière seule"), (axs[1], "tot", "Taxe foncière moins baisse des droits")):
        naif = J["naif_dtf"] if cle == "dtf" else J["naif_tot"]
        ligne(ax, naif, NAIF, "Réforme naïve", lw=1.5)
        ligne(ax, J["prop"][cle], PROP, "Proposition", lw=2.2, ms=4.6, z=5)
        ax.axhline(0, color=ENCRE, lw=0.8, zorder=2)
        axe_deciles(ax, lab=False)
        ax.set_title(titre, fontsize=TXT, color=ENCRE, loc="left")
        axes_propres(ax)
    axs[0].set_ylim(-300, 500)
    axs[0].yaxis.set_major_formatter(euros)
    axs[0].set_ylabel("€ par logement et par an", fontsize=TXT, color=ENCRE2)
    axs[1].tick_params(axis="y", length=0)
    axs[0].legend(loc="upper left", frameon=False, handlelength=1.8)
    fig.subplots_adjust(bottom=0.2)
    fig.supxlabel(XLAB, fontsize=TXT * ECH_TXT, color=ENCRE2, y=0.03, va="bottom")
    fin(fig, "foncier_n08_variation", SRC,
        "Note : variation moyenne par logement des particuliers. À droite, la baisse des droits est rapportée à "
        "l'ensemble des logements de la commune (droits annuels divisés par le nombre de logements). Proposition et "
        "réforme naïve : figures précédentes. Sans réaction des ventes ; avec la reprise des ventes (+6 % par point), "
        "le taux national et les hausses baissent d'environ 18 %.")


# ---------------------------------------------------------------------------------------------------------- n09
def n09_assiette():
    t = J["taux_national"]
    barres = [("Proposition :\ndroits en moins", [("logements", t["cut_log"]), ("autres immeubles", t["cut_aut"])]),
              ("Proposition : taux national\nsur tous les terrains privés",
               [("logements", t["paye_log"]), ("autres immeubles", t["paye_aut"]), ("terrains nus", t["paye_nu"])]),
              ("Variante : droits des logements\net taux sur leur seul sol", [("logements", t["cut_log"])])]
    col = {"logements": NUANCES_BLEU[1], "autres immeubles": NUANCES_BLEU[3], "terrains nus": NUANCES_BLEU[4]}
    fig, ax = plt.subplots(figsize=(9.0, 3.2))
    for i, (nom, parts) in enumerate(barres):
        g = 0.0
        for lab, v in parts:
            ax.barh(i, v, left=g, height=0.58, color=col[lab], edgecolor="white", lw=1.2, zorder=3)
            ax.text(g + v / 2, i, _fr(v, 1), ha="center", va="center", fontsize=TXT,
                    color="white" if lab == "logements" else ENCRE, zorder=4)
            g += v
    ax.set_yticks(range(len(barres)))
    ax.set_yticklabels([b[0] for b in barres])
    ax.invert_yaxis()
    ax.set_xlim(0, 7.6)
    ax.set_xlabel("milliards d'euros par an", fontsize=TXT, color=ENCRE2)
    axes_propres(ax, grille="x")
    ax.spines["left"].set_visible(False)
    ax.tick_params(axis="y", length=0)
    ax.legend([Patch(color=col[k]) for k in col], ["Logements des particuliers", "Locaux d'entreprise et autres "
               "immeubles privés", "Terrains non bâtis"], loc="upper center", bbox_to_anchor=(0.5, -0.32), ncol=3,
              frameon=False, handlelength=1.1, columnspacing=1.2)
    fig.subplots_adjust(bottom=0.33)
    fin(fig, "foncier_n09_assiette",
        "Insee, comptes de patrimoine 2024 (tableau 8.200) ; OFGL ; SDES, Compte du logement 2025 ; calculs de l'auteur.",
        "Note : droits divisés par deux sur toutes les ventes d'immeubles (7,1 Md€ à l'échelle du champ du modèle, "
        "dont 1,45 Md€ sur les biens autres que les logements, montant obtenu par différence entre deux sources et non "
        "vérifié). Assiette de la proposition : sol sous les bâtiments et terrains non bâtis des ménages, des sociétés et "
        "des associations (6 350 Md€ en 2024), hors terres agricoles et terrains publics. La répartition suit les "
        "valeurs de l'Insee par secteur ; la répartition du taux national entre communes ne peut être calculée que pour "
        "les logements. Variante : seuls les droits sur les logements baissent (5,7 Md€), remplacés par un taux national "
        "sur le seul sol des logements des particuliers.")


# ---------------------------------------------------------------------------------------------------------- n10
def n10_primo():
    noms = ["Paris, appartement", "Lyon, appartement", "Bordeaux, appartement", "Nantes, maison", "Limoges, maison",
            "Saint-Étienne, appartement", "Guéret, maison"]
    cas = {c["cas"]: c for c in J["cas"]}
    a10 = (1 - 1.03 ** -10) / 0.03
    eco = np.array([cas[n]["eco"] for n in noms]) / 1e3
    va = -np.array([cas[n]["prop"] for n in noms]) * a10 / 1e3
    fig, ax = plt.subplots(figsize=(9.0, 3.9))
    y = np.arange(len(noms))
    ax.barh(y, eco, height=0.6, color=PROP, zorder=3)
    ax.barh(y, va, left=np.where(va > 0, eco, 0), height=0.6, color=SEC, edgecolor="white", lw=0.8, zorder=3)
    for yi, e, v in zip(y, eco, va):
        net = e + v
        ax.text(max(e, e + v) + 0.3, yi, f"net {_fr(net, 1)} k€", va="center", fontsize=TXT * 0.9, color=ENCRE)
    ax.axvline(0, color=ENCRE, lw=0.8, zorder=4)
    ax.set_yticks(y)
    ax.set_yticklabels(noms)
    ax.invert_yaxis()
    ax.set_xlim(-6, 17.5)
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda u, _: _fr(u)))
    ax.set_xlabel("milliers d'euros : gain (+) ou perte (−) pour l'acheteur", fontsize=TXT, color=ENCRE2)
    axes_propres(ax, grille="x")
    ax.spines["left"].set_visible(False)
    ax.tick_params(axis="y", length=0)
    ax.legend([Patch(color=PROP), Patch(color=SEC)],
              ["Droits en moins à l'achat", "Taxe foncière sur dix ans, valeur actuelle à 3 % (à gauche : hausse)"],
              loc="upper center", bbox_to_anchor=(0.45, -0.2), ncol=2, frameon=False, handlelength=1.2)
    fig.subplots_adjust(bottom=0.25)
    fin(fig, "foncier_n10_primo", SRC,
        "Note : logement médian de la commune (prix médian au m² × surface médiane des ventes 2023-2024). Proposition, "
        "sans effet sur les prix ni reprise des ventes. Si la hausse de taxe foncière se capitalise dans les prix, "
        "l'acheteur paie le logement moins cher d'autant et la barre grise disparaît ; si la baisse des droits se "
        "capitalise aussi, la barre bleue disparaît.")


# ---------------------------------------------------------------------------------------------------------- n11
def n11_transition():
    tr = J["transition"]
    ns = ["3", "5", "10"]
    fig, axs = plt.subplots(1, 2, figsize=(9.6, 3.8), gridspec_kw=dict(width_ratios=[1.5, 1], wspace=0.35))
    ax = axs[0]
    series = [("p90", "9 logements sur 10 en dessous", NUANCES_BLEU[4]), ("paris", "Appartement parisien médian",
              NUANCES_BLEU[2]), ("p99", "99 logements sur 100 en dessous", NUANCES_BLEU[0])]
    w = 0.26
    for k, (cle, lab, col) in enumerate(series):
        v = [tr[n][cle] for n in ns]
        ax.bar(np.arange(3) + (k - 1) * w, v, width=w, color=col, zorder=3, label=lab)
        for x, u in zip(np.arange(3) + (k - 1) * w, v):
            ax.text(x, u + 3, _fr(u), ha="center", va="bottom", fontsize=TXT * 0.8, color=ENCRE)
    ax.set_xticks(range(3))
    ax.set_xticklabels([f"sur {n} ans" for n in ns])
    ax.set_ylim(0, 240)
    ax.yaxis.set_major_formatter(euros)
    ax.set_title("Hausse annuelle de taxe foncière", fontsize=TXT, color=ENCRE, loc="left")
    ax.legend(loc="upper right", frameon=False, handlelength=1.1, fontsize=TXT * ECH_TXT * 0.9)
    axes_propres(ax)
    ax = axs[1]
    v = [tr[n]["deficit"] for n in ns]
    vv = [tr[n]["deficit_vol"] for n in ns]
    ax.bar(np.arange(3), v, width=0.55, color=PROP, zorder=3)
    for x, u, uu in zip(range(3), v, vv):
        ax.text(x, u + 0.6, f"{_fr(u, 0)}", ha="center", va="bottom", fontsize=TXT * 0.9, color=ENCRE)
    ax.set_xticks(range(3))
    ax.set_xticklabels([f"{n} ans" for n in ns])
    ax.set_ylim(0, 37)
    ax.set_title("Déficit transitoire cumulé (Md€)", fontsize=TXT, color=ENCRE, loc="left")
    axes_propres(ax)
    fin(fig, "foncier_n11_transition", SRC,
        "Note : proposition, toutes les composantes (taux national et nouvelle répartition communale) montant en ligne "
        "droite à partir de la première année, les droits étant divisés par deux dès l'annonce. Hausse annuelle : "
        "90e et 99e centiles des logements classés selon leur hausse. Déficit : droits "
        "perdus non encore remplacés, sans reprise des ventes (avec une reprise de 6 % par point : 18 % de moins). "
        "Si les valeurs provisoires du sol n'existaient qu'au bout de trois ans, il faudrait ajouter 21 Md€.")


# ---------------------------------------------------------------------------------------------------------- annexe
def n12_variantes():
    """Annexe : taxe / valeur par décile pour toutes les variantes de répartition."""
    L, W = sm.L, sm.L.n
    w = W * L.v

    def r(tf):
        return (100 * (W * tf).groupby(L.dec_prix).sum() / w.groupby(L.dec_prix).sum()).values
    K4 = sm.deux_taux(0.5, 4)[0]
    Kinf = sm.deux_taux(0.5, np.inf)[0]
    L4 = sm.deux_taux_local(0.5, 4)[0]
    sc = [("Aujourd'hui", J["tfv_auj"], AUJ, "-"), ("Réforme naïve", J["tfv_naif"], NAIF, "-"),
          ("Deux taux nationaux (terrain = 4 × bâti)", r(K4), VAR, "--"), ("Sol seul, taux national unique", r(Kinf), VAR, ":"),
          ("Deux taux par commune, taux départemental sur le sol", r(L4), SEC, "-"),
          ("Deux taux par commune, taux national sur le sol des logements", J["n4"]["tfv"], NUANCES_BLEU[3], "--"),
          ("Proposition (taux national sur tous les terrains)", J["prop"]["tfv"], PROP, "-")]
    fig, ax = plt.subplots(figsize=(9.0, 4.2))
    for lab, y, col, ls in sc:
        ax.plot(X, y, color=col, ls=ls, lw=2.0 if lab.startswith("Proposition") else 1.3, marker="o", ms=3.2,
                mec="white", mew=0.5, label=lab, zorder=5 if lab.startswith("Proposition") else 3)
    axe_deciles(ax)
    ax.set_ylim(0, 0.95)
    pct_axe(ax)
    ax.set_ylabel("taxe foncière en % de la valeur", fontsize=TXT, color=ENCRE2)
    axes_propres(ax)
    ax.legend(loc="upper left", frameon=False, fontsize=TXT * ECH_TXT * 0.85, ncol=2, handlelength=2.2)
    fin(fig, "foncier_n12_variantes", SRC,
        "Note : toutes les variantes remplacent la moitié des droits de mutation par de la taxe foncière, à recette "
        "constante et sans réaction des ventes ; la proposition remplace aussi la moitié des droits sur les autres "
        "immeubles, et son taux national porte sur tous les terrains privés. Taux départemental : chaque département "
        "remplace ses propres droits par un taux sur le sol des logements de son territoire (de 0,11 % à Paris à "
        "0,85 % dans la Creuse).")


def n13_distribution():
    """Annexe : distribution des variations de taxe foncière (centiles)."""
    L, W = sm.L, sm.L.n
    d_naif = sm.report_tf(0.5)[0] - L.tf0
    o = d_naif.sort_values()
    cw = W[o.index].cumsum() / W.sum()
    qs = [10, 25, 50, 75, 90, 95, 99]
    naif = [float(o[cw >= q / 100].iloc[0]) for q in qs]
    n4 = [J["n4"]["pctl"][str(q)] for q in qs]
    pr = [J["prop"]["pctl"][str(q)] for q in qs]
    fig, ax = plt.subplots(figsize=(9.0, 3.6))
    x = np.arange(len(qs))
    w = 0.26
    trio = ((naif, NAIF, "Réforme naïve"), (n4, NUANCES_BLEU[3], "Taux national sur le sol des logements seul"),
            (pr, PROP, "Proposition"))
    for k, (v, col, lab) in enumerate(trio):
        ax.bar(x + (k - 1) * w, v, width=w, color=col, zorder=3, label=lab)
    ax.axhline(0, color=ENCRE, lw=0.8)
    ax.set_xticks(x)
    ax.set_xticklabels([f"{q}e" if q != 50 else "médiane" for q in qs])
    ax.set_xlabel("centile des logements classés selon la variation de leur taxe foncière", fontsize=TXT, color=ENCRE2)
    ax.yaxis.set_major_formatter(euros)
    ax.set_ylabel("€ par an", fontsize=TXT, color=ENCRE2)
    axes_propres(ax)
    ax.legend(loc="upper left", frameon=False, handlelength=1.2)
    fin(fig, "foncier_n13_distribution", SRC,
        "Note : variation de taxe foncière par logement des particuliers (cellules commune × type de logement, tous les "
        "logements d'une cellule étant supposés identiques). Les écarts à l'intérieur d'une commune, que le modèle ne "
        "voit pas, élargiraient la distribution.")


def n14_sol_pib():
    """Valeur du sol sous les bâtiments et des logements (bâti), en % du PIB, 1978-2024 (Insee)."""
    import pandas as pd
    pt = pd.read_csv(RACINE / "lvt/donnees/patrimoine.csv", index_col=0)
    sol = 100 * pt.terrains_batis * 1e3 / pt.pib
    bati = 100 * pt.logements * 1e3 / pt.pib
    fig, ax = plt.subplots(figsize=(9.0, 3.6))
    ax.plot(pt.index, sol, color=NUANCES_BLEU[1], lw=2.2, zorder=4)
    ax.plot(pt.index, bati, color=AUJ, lw=1.5, zorder=3)
    ax.annotate(f"Sol sous les bâtiments : {_fr(sol[2024])} %", (2024, sol[2024]), xytext=(6, 0), textcoords="offset points",
                va="center", fontsize=TXT, color=ENCRE, annotation_clip=False)
    ax.annotate(f"Logements, bâti seul : {_fr(bati[2024])} %", (2024, bati[2024]), xytext=(6, 0), textcoords="offset points",
                va="center", fontsize=TXT, color=ENCRE, annotation_clip=False)
    for a_, dxy, ha in ((1998, (0, 8), "center"),):
        ax.plot([a_], [sol[a_]], "o", color=NUANCES_BLEU[1], ms=5, mec="white", mew=0.8, zorder=5)
        ax.annotate(_fr(sol[a_]) + " %", (a_, sol[a_]), xytext=dxy, textcoords="offset points", ha=ha,
                    fontsize=TXT, color=ENCRE)
    ax.set_xlim(1978, 2024)
    ax.set_ylim(0, 320)
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: _fr(v) + " %"))
    ax.set_ylabel("en % du PIB", fontsize=TXT, color=ENCRE2)
    axes_propres(ax)
    fin(fig, "foncier_n14_sol_pib",
        "Insee, comptes de patrimoine (base 2020, tableau 8.201) et PIB à prix courants ; lvt/donnees/patrimoine.csv.",
        "Note : valeur de fin d'année, toute l'économie. La valeur du sol est un résidu (valeur de marché des biens "
        "moins valeur du bâti à son coût de remplacement) : l'Insee ne publie pas de marge d'incertitude, et le niveau "
        "de 2023 a été révisé de 9 % entre deux publications. Pour les seuls logements des ménages, la part du sol dans "
        "la valeur est passée de 22 % en 1998 à 45 % en 2024.")


if __name__ == "__main__":
    n14_sol_pib()
    n01_inventaire()
    n02_ocde()
    n03_taux_valeur()
    n04_qui_paie()
    n05_cycle()
    n06_naif()
    n07_taux_trois()
    n08_variation()
    n09_assiette()
    n10_primo()
    n11_transition()
    n12_variantes()
    n13_distribution()
