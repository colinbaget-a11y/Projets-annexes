"""
Indice d'évolution du score composite, comparable d'une année à l'autre.

Le score du bulletin est relatif : les bornes min-max sont celles de l'année étudiée. Ici, les bornes
de chaque indicateur sont fixées une fois pour toutes, sur l'ensemble des couples pays-année de la
période. Le score devient alors une fonction linéaire des indicateurs bruts :

    score = somme_k  poids_k * (x_k - min_k) / (max_k - min_k)

Sa variation d'une année à l'autre est la somme des variations des indicateurs du pays, chacune
exprimée en part de l'écart européen observé sur la période. Elle ne dépend pas de ce que font les
autres pays ; les bornes ne fixent que l'unité de chaque indicateur.

Règles :
  - années : éducation, années PISA (2015, 2018, 2022, 2025) ; santé, 2013-2023 ;
  - ruptures de série : signalées par la source (statut Eurostat « b », note « rupture ») ou connues
    (R&D pharmaceutique française en 2021). Si le saut de l'année de rupture est anormal (écart à la
    tendance des années voisines supérieur à 3 écarts-types robustes des variations de l'indicateur),
    la partie antérieure de la série est décalée pour que ce saut soit remplacé par la tendance locale.
    La série est ainsi raccordée sur sa méthodologie la plus récente ;
  - interpolation linéaire entre deux valeurs observées ; au-delà de la première ou de la dernière
    observation, valeur prolongée au plus 3 ans, sinon manquante ;
  - indicateurs relatifs par construction exclus : les indices PISA d'appartenance, de sécurité et de
    harcèlement sont recentrés sur la moyenne OCDE à chaque cycle ; leur niveau ne se compare pas d'un
    cycle à l'autre ;
  - panier : indicateurs disponibles (après interpolation) pour au moins 80 % des couples pays-année ;
  - panier constant par pays : un indicateur manquant une seule année pour un pays est retiré de
    toutes les années pour ce pays, sinon le score bougerait par simple changement de composition ;
  - agrégation identique au bulletin : moyenne des indicateurs disponibles dans chaque objectif
    (imagerie = un bloc d'un tiers en santé O2), quatre objectifs à 25 %.

    python evolution.py      écrit evolution_scores.csv et figures/evolution_*.png
"""
import numpy as np
import pandas as pd
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

import bulletin as bu  # noqa: E402  (données, dictionnaire, pondérations)
from bulletin import be, NOMS, VEDETTES, IMAGERIE, FIG, ICI  # noqa: E402

B = pd.read_csv(ICI / "base_efficience.csv", dtype={"statut": str})
RUPTURES_CONNUES = {("sante_rd_pharma_ratio", "FR", 2021)}
_rupt = B.statut.fillna("").str.contains("b") | B.note.fillna("").str.contains("rupture")
RUPTURES = set(zip(B.indicateur[_rupt], B.pays[_rupt], B.annee[_rupt])) | RUPTURES_CONNUES
SEUIL_RUPTURE = 3
JOURNAL = []                                  # ruptures corrigées : (indicateur, pays, année, décalage)


def raccorder(ind, s):
    """Raccorde chaque série pays (index = années observées) aux ruptures signalées."""
    pas = s.apply(lambda c: c.dropna().diff()).stack()
    et = 1.4826 * (pas - pas.median()).abs().median() or pas.std()
    s = s.copy()
    for p in s.columns:
        x = s[p].dropna()
        for t in sorted((a for (i, q, a) in RUPTURES if i == ind and q == p), reverse=True):
            if t not in x.index or x.index.get_loc(t) == 0:
                continue
            j = x.index.get_loc(t)
            d = x.diff()
            voisins = [d.iloc[k] for k in (j - 1, j + 1) if 1 <= k < len(x) and x.index[k] not in
                       {a for (i, q, a) in RUPTURES if i == ind and q == p}]
            tendance = np.mean(voisins) if voisins else 0.0
            saut = d.iloc[j] - tendance
            if abs(saut) > SEUIL_RUPTURE * et:
                x.iloc[:j] += saut
                JOURNAL.append((ind, p, t, round(float(saut), 3)))
        s[p] = x.reindex(s.index)
    return s

ANNEES = {"education": [2015, 2018, 2022, 2025], "sante": list(range(2013, 2024))}
PAYS = {"education": be.ECHANTILLON_EDU, "sante": be.ECHANTILLON_SANTE}
CODE = {"education": be.E, "sante": be.S}
PROLONGATION = 3
COUVERTURE_MIN = 0.8
RELATIFS = ["pisa_appartenance", "pisa_securite", "pisa_harcelement"]   # indices recentrés à chaque cycle


def panel(ind, pays, annees):
    """Valeurs annuelles interpolées (années x pays), prolongées au plus PROLONGATION ans."""
    t = B[(B.indicateur == ind) & B.pays.isin(pays)]
    if t.empty:
        return pd.DataFrame(index=annees, columns=pays, dtype=float)
    s = raccorder(ind, t.pivot_table(index="annee", columns="pays", values="valeur").reindex(columns=pays))
    tout = range(min(s.index.min(), annees[0]), max(s.index.max(), annees[-1]) + 1)
    s = s.reindex(tout)
    s = s.interpolate(limit_area="inside").ffill(limit=PROLONGATION).bfill(limit=PROLONGATION)
    return s.reindex(annees)


def indice(domaine):
    pays, annees = PAYS[domaine], ANNEES[domaine]
    inds = [d for d in be.DICO if d[1] == CODE[domaine]]
    X, retenus, exclus = {}, [], []
    for ident, _, obj, _, pol, _, _ in inds:
        if ident in RELATIFS:
            exclus.append(ident + " (relatif)")
            continue
        p = panel(ident, pays, annees)
        if p.notna().values.mean() >= COUVERTURE_MIN:
            X[ident] = (p, pol, obj)
            retenus.append(ident)
        else:
            exclus.append(ident)
    # normalisation à bornes fixes (période entière) et panier constant par pays
    N = {}
    for ident, (p, pol, _) in X.items():
        n = (p - np.nanmin(p.values)) / (np.nanmax(p.values) - np.nanmin(p.values))
        n = 1 - n if pol == "-" else n
        n.loc[:, n.isna().any()] = np.nan          # absent une année -> retiré toutes les années
        N[ident] = n
    objectifs = sorted({X[i][2] for i in retenus})
    O = {}
    for o in objectifs:
        ids = [i for i in retenus if X[i][2] == o]
        if domaine == "sante" and o == "S2":
            blocs = [[i] for i in ids if i not in IMAGERIE] + [[i for i in ids if i in IMAGERIE]]
            blocs = [b for b in blocs if b]
        else:
            blocs = [[i] for i in ids]
        # moyenne des blocs disponibles ; chaque bloc = moyenne de ses indicateurs disponibles
        vals = [pd.concat([N[i] for i in b]).groupby(level=0).mean() for b in blocs]
        O[o] = pd.concat(vals).groupby(level=0).mean()
    score = sum(0.25 * O[o] for o in objectifs)
    return score, O, retenus, exclus


def main():
    lignes = []
    resultats = {}
    for dom in ANNEES:
        score, O, retenus, exclus = indice(dom)
        resultats[dom] = (score, O)
        print(f"\n{dom} : {len(retenus)} indicateurs retenus ; exclus : {', '.join(exclus) or 'aucun'}")
        for a in score.index:
            for p in score.columns:
                lignes.append({"domaine": dom, "annee": a, "pays": p, "score": score.loc[a, p],
                               **{f"objectif_{o}": O[o].loc[a, p] for o in O}})
        print(score.T.round(3).sort_values(score.index[-1], ascending=False).to_string())
    pd.DataFrame(lignes).to_csv(ICI / "evolution_scores.csv", index=False, float_format="%.4f")
    j = pd.DataFrame(sorted(set(JOURNAL)), columns=["indicateur", "pays", "annee", "decalage"])
    j.to_csv(ICI / "evolution_ruptures.csv", index=False)
    print(f"\n{len(j)} ruptures raccordées (evolution_ruptures.csv) ; exemples :")
    print(j.reindex(j.decalage.abs().sort_values(ascending=False).index).head(12).to_string(index=False))

    # moyenne UE à pondérations fixes (2022), pour ne pas mêler effets de composition
    poids = {"education": bu.eleves, "sante": bu.pop}
    for dom, (score, O) in resultats.items():
        w = poids[dom].reindex(score.columns)
        ue = (score * w).sum(axis=1) / (score.notna() * w).sum(axis=1)
        fig, ax = plt.subplots(figsize=(9, 5.5))
        for p in score.columns:
            if p not in VEDETTES:
                ax.plot(score.index, score[p], color="#c9cdd1", lw=0.8, zorder=1)
        for p, c in VEDETTES.items():
            ax.plot(score.index, score[p], color=c, lw=2.2, marker="o", ms=4, label=NOMS[p], zorder=3)
        ax.plot(score.index, ue, color="#222222", lw=2, ls="--", label="Moyenne UE", zorder=2)
        ax.set_ylabel("Score composite, bornes fixes (0-1)")
        ax.set_xticks(score.index if dom == "education" else score.index[::2])
        ax.spines[["top", "right"]].set_visible(False)
        ax.grid(axis="y", alpha=0.3)
        ax.legend(frameon=False, ncol=3, loc="lower left")
        fig.tight_layout()
        fig.savefig(FIG / f"evolution_{dom}.png", dpi=150)
        plt.close(fig)

        # variation de la France par objectif entre la première et la dernière année
        a0, a1 = score.index[0], score.index[-1]
        d = {o: 25 * (O[o].loc[a1, "FR"] - O[o].loc[a0, "FR"]) for o in O}
        print(f"\nFrance, {dom}, {a0}-{a1} : score {score.loc[a0, 'FR']:.3f} -> {score.loc[a1, 'FR']:.3f} "
              f"({100 * (score.loc[a1, 'FR'] - score.loc[a0, 'FR']):+.1f} points) ; par objectif : "
              + ", ".join(f"{o} {v:+.1f}" for o, v in d.items())
              + f" ; moyenne UE {100 * (ue[a1] - ue[a0]):+.1f} points")


if __name__ == "__main__":
    main()
