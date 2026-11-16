"""Figures de la note foncière (préfixe fon_).

Lancer depuis fiscalite/ : python3 foncier/figures_foncier.py ; FIG_NU=1 python3 foncier/figures_foncier.py
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from matplotlib.patches import Patch
from matplotlib.ticker import FuncFormatter

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE), str(HERE.parent)]
import simulation as sm  # noqa: E402
from graphiques import ECH_TXT, INK, NU, PCT, fin, grille, plt  # noqa: E402

L = sm.L
SRC = ("DGFiP, REI 2024 et DVF 2023-2024 ; Insee, recensement 2022, comptes de patrimoine et Insee Analyses "
       "n° 91 ; calculs de l'auteur.")

# Réglages propres à ces figures (la charte graphiques.py sert aussi au cours et n'est pas modifiée).
# TXT est la taille passée aux textes que la charte met à l'échelle en mode nu (×0,78) : 8 pt imprimés.
# Les graduations et légendes prennent la même taille imprimée.
TXT = 10.3
plt.rcParams.update({k: TXT * ECH_TXT for k in ("xtick.labelsize", "ytick.labelsize", "axes.labelsize",
                                                 "legend.fontsize")})
# Palette catégorielle validée (dataviz/validate_palette.js, mode clair, toutes paires) : bleu, ocre, brique ;
# « aujourd'hui » et les comparaisons restent en encre ou en gris neutre.
BLEU, OCRE, BRIQUE, CLAIR, GRIS = "#1d4ba6", "#c79100", "#993333", "#aabbdd", "#9a9a9a"
SC = {"auj": ("Aujourd'hui", INK), "R50": ("Taxe actuelle relevée", OCRE),
      "K4": ("Deux taux nationaux", BRIQUE), "N4": ("Proposition", BLEU)}
SCEN = {"R50": sm.report_tf(0.5), "N4": sm.deux_taux_local_national(0.5, 4), "K4": sm.deux_taux(0.5, 4)}
dec = L.groupby("dec_prix").pm2.median()
xt = [f"{u/1e3:.1f}".replace(".", ",") for u in dec]
EUR = FuncFormatter(lambda v, _: f"{v:,.0f}".replace(",", " ").replace("-", "−"))
XLAB = "Prix médian au m² du décile de logements (milliers d'euros)"


def courbe(ax, x, y, cle):
    """Ligne d'un scénario : la proposition plus épaisse, au premier plan ; points cerclés de blanc."""
    p = cle == "N4"
    ax.plot(x, y, color=SC[cle][1], lw=2.1 if p else 1.4, marker="o", ms=4.2 if p else 3.4, mec="white",
            mew=0.7, zorder=5 if p else 4, solid_capstyle="round", label=SC[cle][0])


def etiqueter_fins(ax, x, fins, dx=6):
    """Nom de chaque courbe à droite de son dernier point, en encre ; si deux noms se touchent, on les écarte
    juste assez (au plus quelques points), sans les détacher de leur courbe."""
    ecart = 1.2 * TXT * ECH_TXT
    k = 72 / ax.figure.dpi
    pts = sorted((ax.transData.transform((x, y))[1] * k, y, lab) for lab, y in fins)
    pos = [p for p, _, _ in pts]
    for _ in range(100):
        bouge = False
        for i in range(1, len(pos)):
            if pos[i] - pos[i - 1] < ecart - 1e-6:
                m = (ecart - (pos[i] - pos[i - 1])) / 2
                pos[i] += m
                pos[i - 1] -= m
                bouge = True
        if not bouge:
            break
    for (p0, y, lab), p in zip(pts, pos):
        ax.annotate(lab, (x, y), xytext=(dx, p - p0), textcoords="offset points", va="center", ha="left",
                    fontsize=TXT, color=INK, annotation_clip=False)


def f1():
    """Taxe foncière / valeur des logements, par décile de prix au m²."""
    fig, ax = plt.subplots(figsize=(8.6, 4.15))
    w = L.n * L.v
    x = np.arange(10)
    fins = []
    for cle in ("auj", "R50", "K4", "N4"):
        tf = L.tf0 if cle == "auj" else SCEN[cle][0]
        r = 100 * (L.n * tf).groupby(L.dec_prix).sum() / w.groupby(L.dec_prix).sum()
        courbe(ax, x, r.values, cle)
        fins.append((SC[cle][0], r.values[-1]))
    ax.set_xticks(x)
    ax.set_xticklabels(xt)
    ax.set_xlim(-0.3, 9.3)
    ax.set_xlabel(XLAB)
    ax.set_ylabel("en % de la valeur du logement")
    ax.yaxis.set_major_formatter(PCT)
    ax.set_ylim(0, 0.7)
    ax.set_yticks(np.arange(0, 0.71, 0.1))
    grille(ax)
    etiqueter_fins(ax, 9, fins)
    fin(fig, "fon_01_tf_valeur", SRC,
        "Note : taxe foncière des logements des particuliers rapportée à leur valeur de marché, par décile de "
        "logements classés selon le prix au m² de leur commune (France métropolitaine hors Alsace-Moselle). Les "
        "trois scénarios remplacent la moitié des droits de mutation (5,7 Md€) par de la taxe foncière, à recette "
        "constante, sans réaction des ventes : taxe actuelle relevée du même pourcentage partout ; deux taux "
        "nationaux sur la valeur de marché, le taux sur le terrain égal à quatre fois le taux sur le bâti ; "
        "proposition : chaque commune garde sa recette, répartie selon ces deux taux, et un taux national de "
        "0,19 % sur la valeur des terrains remplace les droits perdus. Aujourd'hui : rapport taxe/valeur de 2017 "
        "vieilli selon la croissance de la taxe foncière de chaque commune de 2017 à 2024.")


def f2():
    """Variation par logement et par an : taxe foncière seule, et taxe foncière moins la baisse des DMTO."""
    fig, axs = plt.subplots(1, 2, figsize=(10.4, 4.15), sharey=True, gridspec_kw=dict(wspace=0.1))
    x = np.arange(10)
    for cle in ("R50", "K4", "N4"):
        tf1, d1 = SCEN[cle]
        g = L.assign(w=L.n, a=L.n * (tf1 - L.tf0), b=L.n * (tf1 - L.tf0 + d1 - L.d0)).groupby("dec_prix")
        for ax, col in zip(axs, ("a", "b")):
            courbe(ax, x, (g[col].sum() / g.w.sum()).values, cle)
    for ax, t in zip(axs, ("Taxe foncière seule", "Taxe foncière et droits de mutation")):
        ax.axhline(0, color=INK, lw=0.8, zorder=3)
        ax.set_xticks(x)
        ax.set_xticklabels(xt)
        ax.set_xlim(-0.4, 9.4)
        ax.set_title(t, fontsize=TXT, color=INK, loc="left", pad=4)
        grille(ax)
    axs[1].tick_params(axis="y", length=0)
    axs[0].set_ylabel("€ par logement et par an")
    axs[0].yaxis.set_major_formatter(EUR)
    axs[0].set_ylim(-450, 1900)
    axs[0].set_yticks([0, 500, 1000, 1500])
    # légende sans cadre dans le coin vide, dans l'ordre où les courbes arrivent à droite (haut -> bas)
    h, lab = axs[0].get_legend_handles_labels()
    ordre = [lab.index(SC[c][0]) for c in ("K4", "N4", "R50")]
    axs[0].legend([h[i] for i in ordre], [lab[i] for i in ordre], loc="upper left", frameon=False,
                  handlelength=1.8, borderaxespad=0.2, labelspacing=0.35)
    fig.subplots_adjust(bottom=0.19)
    fig.supxlabel(XLAB, fontsize=TXT * ECH_TXT, color=INK, y=0.035, va="bottom")
    fin(fig, "fon_02_variation", SRC,
        "Note : variation moyenne par logement des particuliers ; scénarios de la figure précédente. À droite, la "
        "baisse des droits de mutation est rapportée à l'ensemble du parc de la commune (droits annuels / nombre "
        "de logements) : c'est ce que paie en moyenne chaque année un logement de la commune au fil des ventes.")


def f3():
    """Inventaire des prélèvements sur l'immobilier (2024)."""
    # Le panneau de comparaison OCDE a été retiré : ses quatre chiffres sont déjà dans le texte, et il
    # écrasait l'inventaire. Les composantes nommées sont en bleu, séparées par un filet blanc ; le reste de
    # chaque famille (« autres ») en bleu clair. Les plus-values et la contribution de sécurité immobilière,
    # trop étroites pour être nommées, rejoignent les « autres » des transactions (détail dans la note).
    fam = [("Détention", [("Taxe foncière bâtie", 42.0), ("TEOM", 9.0), ("CFE", 8.0),
                          (None, 3.9 + 2.7 + 1.3 + 1.1 + 1.0)]),
           ("Transactions", [("DMTO", 14.1), ("TVA", 7.1), (None, 2.8 + 1.0)]),
           ("Transmissions", [("", 12.5)]),
           ("Revenus locatifs", [("", 8.4)]),
           ("Construction", [("", 1.5)])]
    fig, ax = plt.subplots(figsize=(9.3, 3.25))
    if not NU:   # garder axe et étiquettes dans le cadre, au-dessus du bloc des sources
        fig.subplots_adjust(left=0.16, bottom=0.2)
    ax.set_xlim(0, 73)
    ax.set_ylim(len(fam) - 0.45, -0.55)
    etiq = []
    for i, (nom, parts) in enumerate(fam):
        g = 0.0
        for lab, v in parts:
            ax.barh(i, v, left=g, height=0.64, color=BLEU if lab is not None else CLAIR, edgecolor="white",
                    lw=1.0, zorder=3)
            texte = lab if lab is not None else "autres"
            if texte and len(parts) > 1:
                etiq.append((ax.text(g + v / 2, i, texte, ha="center", va="center", fontsize=TXT, zorder=4,
                                     color="white" if lab is not None else INK), g, v))
            g += v
        ax.text(g + 0.7, i, f"{g:.0f}".replace(".", ","), va="center", fontsize=TXT, color=INK)
    ax.set_yticks(range(len(fam)))
    ax.set_yticklabels([f[0] for f in fam])
    ax.tick_params(axis="y", length=0, pad=5)
    ax.spines["left"].set_visible(False)
    ax.set_xlabel("milliards d'euros, 2024 (environ 116 au total)")
    grille(ax, "x")
    # un nom n'est écrit dans son segment que s'il y tient avec de la marge
    fig.canvas.draw()
    r = fig.canvas.get_renderer()
    for t, g, v in etiq:
        x0, x1 = ax.transData.transform([(g, 0), (g + v, 0)])[:, 0]
        if t.get_window_extent(r).width > (x1 - x0) - 8:
            t.remove()
    fin(fig, "fon_03_inventaire",
        "DGCL-DGFiP, note REI 2025 ; OFGL ; SDES, compte du logement 2025 ; DGFiP Statistiques n° 43 ; "
        "calculs de l'auteur.",
        "Note : rendements 2024, périmètres hétérogènes ; part immobilière des droits de succession estimée à 60 % "
        "(clé du CPO, pas de ventilation officielle). TEOM : taxe d'enlèvement des ordures ménagères ; CFE : "
        "cotisation foncière des entreprises ; DMTO : droits de mutation ; TVA du neuf et des terrains. "
        "« Autres » des transactions : plus-values immobilières et contribution de sécurité immobilière ; "
        "« autres » de la détention : taxes d'habitation restantes, IFI, taxe sur le foncier non bâti, taxe sur "
        "les bureaux d'Île-de-France, GEMAPI et taxes spéciales d'équipement.")


def f4():
    """Primo-accédant : économie de droits à l'achat et coût de la hausse de taxe foncière sur 10 ans."""
    df = sm.primo({"N4": SCEN["N4"]}, lambda *_: None, horizons=(10,))
    df["va10"] = df.eco - df.net10
    df = df.sort_values("eco", ascending=False).reset_index(drop=True)
    fig, ax = plt.subplots(figsize=(9.0, 4.15))
    if not NU:
        fig.subplots_adjust(left=0.25)
    y = np.arange(len(df))
    eco, dtf = df.eco / 1e3, -df.va10 / 1e3
    # Une barre par commune : à droite de 0 ce que l'acheteur gagne, à gauche ce qu'il perd. Une baisse de taxe
    # foncière (Annecy, Saint-Étienne) est un gain : elle prolonge la barre des droits, après un filet blanc.
    ax.barh(y, eco, height=0.62, color=BLEU, zorder=3)
    ax.barh(y, dtf, left=np.where(dtf > 0, eco, 0), height=0.62, color=OCRE, edgecolor="white", lw=0.8, zorder=3)
    ax.axvline(0, color=INK, lw=0.8, zorder=4)
    ax.set_yticks(y)
    ax.set_yticklabels(df.cas)
    ax.tick_params(axis="y", length=0)
    ax.spines["left"].set_visible(False)
    ax.invert_yaxis()
    ax.set_xlim(-7, 24)
    ax.xaxis.set_major_formatter(EUR)
    ax.set_xlabel("milliers d'euros : gain (+) ou perte (−) pour l'acheteur")
    grille(ax, "x")
    ax.legend([Patch(color=BLEU), Patch(color=OCRE)],
              ["Baisse des droits payés à l'achat",
               "Variation de taxe foncière sur 10 ans,\nvaleur actuelle à 3 % (à gauche : hausse)"],
              loc="lower right", frameon=False, borderaxespad=0.3, handlelength=1.2, labelspacing=0.6)
    fin(fig, "fon_04_primo", SRC,
        "Note : logement médian de la commune (prix médian au m² × surface médiane des ventes 2023-2024). "
        "Proposition : droits de mutation divisés par deux, taxe foncière à deux taux (terrain = 4 × bâti) avec "
        "recette constante par commune et taux national de 0,19 % sur la valeur des terrains (sans réaction des ventes). Sans effet sur les "
        "prix ; si la hausse de taxe foncière est capitalisée, le prix d'achat baisse d'autant.")


if __name__ == "__main__":
    f1()
    f2()
    f3()
    f4()
