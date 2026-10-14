"""
Évolution de la performance éducative des pays de l'échantillon, 2006-2025, comparable entre pays et
dans le temps.

Méthode :
  1. Panier commun. On ne garde que les indicateurs du bulletin observés pour les 24 pays en début
     (2006) et en fin de fenêtre (2025, ou 2024 pour les séries publiées avec un an de retard), sur une
     échelle comparable dans le temps. Tous les pays sont mesurés sur le même panier, chaque année :
     pas de chaînage, pas de pondération propre à un pays. Entre deux vagues, interpolation linéaire.
     2006 est la première année où les trois domaines PISA sont reliés dans le temps (sciences) et où
     les 24 pays participent.
  2. Standardisation fixe. Chaque indicateur est exprimé en écarts-types de la distribution entre
     pays : z = signe * (x - moyenne des pays en 2006) / écart-type moyen entre pays sur 2006-2025.
     Moyenne et écart-type sont fixés une fois pour toutes : z est une fonction linéaire de x, et sa
     variation ne dépend que du pays lui-même. L'écart-type, calculé sur les 24 pays, est moins
     sensible qu'une étendue min-max aux deux pays extrêmes.
  3. Agrégation du bulletin. Objectif = moyenne de ses indicateurs ; indice = moyenne des quatre
     objectifs, divisée par l'écart-type moyen de l'indice entre pays. Unité : écart-type entre pays ;
     0 = pays européen moyen en 2006.

    python performance_education.py    écrit performance_education.csv et figures/performance_*.png
"""
import numpy as np
import pandas as pd
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.colors import LinearSegmentedColormap  # noqa: E402

import evolution as ev  # noqa: E402  (lecture, raccord des ruptures, échelles PISA)
from bulletin import be, NOMS, FIG, ICI  # noqa: E402

DEBUT, FIN = 2006, 2025
ANNEES = list(range(DEBUT, FIN + 1))
PAYS = be.ECHANTILLON_EDU
VAGUES = [2006, 2009, 2012, 2015, 2018, 2022, 2025]
RETARD_MAX = 1            # dernière valeur observée au plus 1 an avant la fin (délai de publication)
OBJECTIFS = {"E1": "Maîtrise des savoirs fondamentaux", "E2": "Excellence et dynamisme académique",
             "E3": "Équité", "E4": "Insertion dans la vie active"}
# indicateurs PISA par domaine (élèves faibles) : disponibles depuis 2006, contrairement à l'indicateur
# « faibles dans les trois domaines » du bulletin, calculé sur microdonnées depuis 2015 seulement
SUBSTITUTS = [("pisa_faibles_maths", "E1", "-"), ("pisa_faibles_lecture", "E1", "-"),
              ("pisa_faibles_sciences", "E1", "-")]

# charte (palette de référence de la skill dataviz, mode clair)
SURFACE, INK, INK2, MUTED, GRID, AXE = "#fcfcfb", "#0b0b0b", "#52514e", "#898781", "#e1e0d9", "#c3c2b7"
BLEU, BLEU_CLAIR, BLEU_FONCE, ROUGE, NEUTRE = "#2a78d6", "#86b6ef", "#1c5cab", "#e34948", "#f0efec"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9, "axes.facecolor": SURFACE,
                     "figure.facecolor": SURFACE, "axes.edgecolor": AXE, "axes.labelcolor": INK2,
                     "xtick.color": MUTED, "ytick.color": MUTED, "text.color": INK})


def panier():
    """Indicateurs du panier commun, avec objectif et polarité."""
    cand = [(d[0], d[2], d[4]) for d in be.DICO if d[1] == be.E and d[0] not in ev.RELATIFS]
    cand += SUBSTITUTS
    retenus, exclus = [], []
    for ident, obj, pol in cand:
        t = ev.B[(ev.B.indicateur == ident) & ev.B.pays.isin(PAYS)]
        for dom, a0 in ev.DEBUT_TENDANCE_PISA.items():
            if ident.startswith("pisa_") and ident.endswith(dom):
                t = t[t.annee >= a0]
        debut = t[t.annee == DEBUT].pays.nunique()
        fin = t[t.annee >= FIN - RETARD_MAX].groupby("pays").annee.max().index.nunique()
        if debut == len(PAYS) and fin == len(PAYS):
            retenus.append((ident, obj, pol))
        else:
            exclus.append(f"{ident} ({debut} pays en {DEBUT}, {fin} en fin)")
    return retenus, exclus


def calcul():
    retenus, exclus = panier()
    Z = {}
    for ident, obj, pol in retenus:
        x, _ = ev.panel(ident, PAYS, ANNEES)
        assert x.notna().all().all(), ident
        signe = -1 if pol == "-" else 1
        Z[ident] = signe * (x - x.loc[DEBUT].mean()) / x.std(axis=1).mean()
    O = {o: sum(Z[i] for i, ob, _ in retenus if ob == o) / sum(ob == o for _, ob, _ in retenus)
         for o in OBJECTIFS}
    brut = sum(O.values()) / 4
    echelle = brut.std(axis=1).mean()
    indice = brut / echelle
    O = {o: v / echelle for o, v in O.items()}          # même unité que l'indice
    return indice, O, retenus, exclus


def style(ax):
    ax.spines[["top", "right"]].set_visible(False)
    ax.spines[["left", "bottom"]].set_color(AXE)
    ax.grid(axis="y", color=GRID, lw=0.6)
    ax.set_axisbelow(True)
    ax.tick_params(length=0)


def petits_multiples(indice, ordre):
    ue = indice.mean(axis=1)
    fig, axes = plt.subplots(4, 6, figsize=(13, 8.6), sharex=True, sharey=True)
    for ax, p in zip(axes.flat, ordre):
        for q in indice.columns:
            if q != p:
                ax.plot(indice.index, indice[q], color="#d9d8d2", lw=0.6, zorder=1)
        ax.plot(indice.index, ue, color=INK2, lw=1.2, ls=(0, (3, 2)), zorder=2)
        ax.plot(indice.index, indice[p], color=BLEU, lw=2, zorder=3)
        ax.plot(VAGUES, indice.loc[VAGUES, p], color=BLEU, lw=0, marker="o", ms=3.5,
                markeredgecolor=SURFACE, markeredgewidth=0.8, zorder=4)
        d = indice.loc[FIN, p] - indice.loc[DEBUT, p]
        ax.set_title(f"{NOMS[p]}", loc="left", fontsize=9.5, color=INK, fontweight="bold", pad=2)
        ax.text(1, 1.02, f"{d:+.2f}", transform=ax.transAxes, ha="right", va="bottom", fontsize=8.5,
                color=INK2)
        style(ax)
        ax.axhline(0, color=AXE, lw=0.8, zorder=0)
        ax.set_xticks([2006, 2015, 2025])
    fig.text(0.01, 0.995, "Performance éducative, 2006-2025 (indice en écarts-types entre pays ; 0 = pays "
             "européen moyen en 2006)", fontsize=11, fontweight="bold", va="top")
    fig.text(0.01, 0.965, "Trait bleu : le pays ; tirets : moyenne des 24 pays ; gris : les autres pays. "
             "Points : années PISA. Chiffre : variation 2006-2025. Pays classés par niveau en 2025.",
             fontsize=8.5, color=INK2, va="top")
    fig.tight_layout(rect=(0, 0, 1, 0.95))
    fig.savefig(FIG / "performance_petits_multiples.png", dpi=160)
    plt.close(fig)


def haltere(indice, ordre):
    a, m, b = DEBUT, 2015, FIN
    fig, ax = plt.subplots(figsize=(8, 8))
    y = np.arange(len(ordre))[::-1]
    for yi, p in zip(y, ordre):
        ax.plot([indice.loc[a, p], indice.loc[b, p]], [yi, yi], color=AXE, lw=2, zorder=1,
                solid_capstyle="round")
        ax.plot(indice.loc[a, p], yi, "o", color=BLEU_CLAIR, ms=7, zorder=2)
        ax.plot(indice.loc[m, p], yi, "o", color=BLEU, ms=4, zorder=3)
        ax.plot(indice.loc[b, p], yi, "o", color=BLEU_FONCE, ms=7, zorder=4)
        ax.text(1.01, yi, f"{indice.loc[b, p] - indice.loc[a, p]:+.2f}", transform=ax.get_yaxis_transform(),
                va="center", fontsize=8.5, color=INK2)
    ax.set_yticks(y, [NOMS[p] for p in ordre], color=INK)
    ax.axvline(0, color=AXE, lw=0.8, zorder=0)
    ax.spines[["top", "right", "left"]].set_visible(False)
    ax.spines["bottom"].set_color(AXE)
    ax.grid(axis="x", color=GRID, lw=0.6)
    ax.set_axisbelow(True)
    ax.tick_params(length=0)
    ax.set_xlabel("Indice de performance éducative (écarts-types entre pays ; 0 = moyenne 2006)")
    h = [plt.Line2D([], [], color=c, marker="o", lw=0, ms=s) for c, s in
         ((BLEU_CLAIR, 7), (BLEU, 4), (BLEU_FONCE, 7))]
    ax.legend(h, [str(a), str(m), str(b)], frameon=False, ncol=3, loc="lower left",
              bbox_to_anchor=(0, 1.0))
    ax.text(1.01, 1.0, "variation\n2006-2025", transform=ax.transAxes, fontsize=8, color=MUTED, va="bottom")
    fig.tight_layout()
    fig.savefig(FIG / "performance_haltere.png", dpi=160)
    plt.close(fig)


def carte_contributions(O, ordre):
    """Contribution de chaque objectif à la variation 2006-2025 (en unités d'indice)."""
    C = pd.DataFrame({o: (O[o].loc[FIN] - O[o].loc[DEBUT]) / 4 for o in OBJECTIFS}).loc[ordre]
    lim = np.abs(C.values).max()
    cmap = LinearSegmentedColormap.from_list("div", [ROUGE, NEUTRE, BLEU])
    fig, ax = plt.subplots(figsize=(7.2, 8))
    ax.imshow(C.values, cmap=cmap, vmin=-lim, vmax=lim, aspect="auto")
    for i in range(C.shape[0]):
        for j in range(C.shape[1]):
            ax.text(j, i, f"{C.iat[i, j]:+.2f}", ha="center", va="center", fontsize=8, color=INK)
    entetes = {"E1": "Savoirs\nfondamentaux", "E2": "Excellence", "E3": "Équité",
               "E4": "Insertion dans\nla vie active"}
    ax.set_xticks(range(4), [entetes[o] for o in C], fontsize=8.5, color=INK)
    ax.xaxis.tick_top()
    ax.set_yticks(range(len(ordre)), [NOMS[p] for p in ordre], color=INK)
    ax.tick_params(length=0)
    for s in ax.spines.values():
        s.set_visible(False)
    ax.set_xticks(np.arange(-0.5, 4), minor=True)
    ax.set_yticks(np.arange(-0.5, len(ordre)), minor=True)
    ax.grid(False, which="major")
    ax.grid(which="minor", color=SURFACE, lw=2)
    ax.tick_params(which="minor", length=0)
    fig.text(0.01, 0.01, "Contribution de chaque objectif à la variation de l'indice entre 2006 et 2025. "
             "Bleu : amélioration ; rouge : recul.", fontsize=8, color=INK2)
    fig.tight_layout(rect=(0, 0.03, 1, 1))
    fig.savefig(FIG / "performance_contributions.png", dpi=160)
    plt.close(fig)


def main():
    indice, O, retenus, exclus = calcul()
    print(f"Panier commun ({len(retenus)} indicateurs) :")
    for o in OBJECTIFS:
        print(f"  {o} : {', '.join(i for i, ob, _ in retenus if ob == o)}")
    print("Exclus :\n  " + "\n  ".join(exclus))
    ordre = list(indice.loc[FIN].sort_values(ascending=False).index)
    t = pd.DataFrame({"indice": indice.stack(), **{f"objectif_{o}": O[o].stack() for o in O}})
    t.index.names = ["annee", "pays"]
    t.reset_index().to_csv(ICI / "performance_education.csv", index=False, float_format="%.4f")
    r = pd.DataFrame({a: indice.loc[a] for a in (2006, 2015, 2025)})
    r["variation"] = r[2025] - r[2006]
    print(r.loc[ordre].round(2).to_string())
    # contrôle : variations 2015-2025 de cet indice et de l'indice chaîné min-max (evolution.py)
    ch = pd.read_csv(ICI / "evolution_scores.csv")
    ch = ch[ch.domaine == "education"].pivot(index="annee", columns="pays", values="score")
    d1, d2 = indice.loc[2025] - indice.loc[2015], ch.loc[2025] - ch.loc[2015]
    print(f"\nCorrélation des variations 2015-2025 avec l'indice chaîné : {d1.corr(d2):.2f}")
    # variante sans l'insertion (E4), sensible à la conjoncture du marché du travail
    acquis = sum(O[o] for o in ("E1", "E2", "E3")) / 3
    acquis = acquis / acquis.std(axis=1).mean()
    va, vi = acquis.loc[FIN] - acquis.loc[DEBUT], indice.loc[FIN] - indice.loc[DEBUT]
    print(f"Variante sans insertion : corrélation des variations 2006-2025 avec l'indice {va.corr(vi):.2f} ; "
          f"rang de la France en 2025 : {int(acquis.loc[FIN].rank(ascending=False)['FR'])}/24 "
          f"(indice complet : {int(indice.loc[FIN].rank(ascending=False)['FR'])}/24)")
    t2 = pd.DataFrame({"indice_sans_insertion": acquis.stack()})
    t2.index.names = ["annee", "pays"]
    t = t.join(t2)
    t.reset_index().to_csv(ICI / "performance_education.csv", index=False, float_format="%.4f")
    petits_multiples(indice, ordre)
    haltere(indice, ordre)
    carte_contributions(O, ordre)


if __name__ == "__main__":
    main()
