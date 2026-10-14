"""
Indice d'évolution du score composite, comparable d'une année à l'autre (indice chaîné).

Le score du bulletin est relatif : les bornes min-max sont celles de l'année étudiée. Ici, les bornes
de chaque indicateur sont fixées une fois pour toutes, sur l'ensemble des couples pays-année de la
période. Chaque indicateur normalisé devient une fonction linéaire de sa valeur brute, et sa variation
s'exprime en part de l'écart européen observé sur la période, sans dépendre des autres pays.

Indice chaîné (méthode des volumes chaînés des comptes nationaux) : la variation du score entre deux
années consécutives est calculée, pays par pays, sur les seuls indicateurs disponibles les deux
années, avec l'agrégation du bulletin (moyenne des indicateurs disponibles dans chaque objectif,
imagerie = un bloc d'un tiers en santé O2, quatre objectifs à 25 %). Le niveau est ancré sur le score
à bornes fixes de l'année de référence (2022, celle du bulletin), puis on cumule les variations vers
l'avant et vers l'arrière. Un indicateur qui n'existe qu'à partir de 2015 compte à partir de 2015 sans
créer de saut : le panier peut s'élargir, chaque variation reste mesurée à panier identique.

Règles :
  - années : éducation 2000-2025, santé 2000-2023, en annuel ;
  - comparabilité PISA : l'OCDE relie les échelles depuis 2000 pour la lecture, 2003 pour les
    mathématiques, 2006 pour les sciences ; les valeurs antérieures de chaque domaine sont écartées ;
  - ruptures de série : signalées par la source (statut Eurostat « b », note « rupture ») ou connues
    (R&D pharmaceutique française en 2021). Si le saut de l'année de rupture est anormal (écart à la
    tendance des années voisines supérieur à 3 écarts-types robustes des variations de l'indicateur),
    la partie antérieure de la série est décalée pour que ce saut soit remplacé par la tendance locale ;
  - interpolation linéaire entre deux valeurs observées ; au-delà de la première ou de la dernière
    observation, valeur prolongée au plus 3 ans, sinon manquante ;
  - chaque variation est décomposée par indicateur, en part observée (indicateur mesuré les deux
    années) et part interpolée (evolution_contributions.csv) ;
  - indicateurs relatifs par construction exclus : les indices PISA d'appartenance, de sécurité et de
    harcèlement sont recentrés sur la moyenne OCDE à chaque cycle ;
  - indicateurs trop peu couverts exclus : moins de 75 % des pays, quelle que soit l'année ;
  - variante à panier constant (2015-2025 en éducation, 2013-2023 en santé) pour contrôle.

    python evolution.py      écrit evolution_scores.csv, evolution_contributions.csv,
                             evolution_ruptures.csv et figures/evolution_*.png
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

ANNEES = {"education": list(range(2000, 2026)), "sante": list(range(2000, 2024))}
REFERENCE = 2022
PANIER_CONSTANT = {"education": 2015, "sante": 2013}       # début de la variante à panier constant
VAGUES = {"education": [2000, 2003, 2006, 2009, 2012, 2015, 2018, 2022, 2025]}
PAYS = {"education": be.ECHANTILLON_EDU, "sante": be.ECHANTILLON_SANTE}
CODE = {"education": be.E, "sante": be.S}
PROLONGATION = 3
COUVERTURE_MIN = 0.75
RELATIFS = ["pisa_appartenance", "pisa_securite", "pisa_harcelement"]   # indices recentrés à chaque cycle
DEBUT_TENDANCE_PISA = {"lecture": 2000, "maths": 2003, "sciences": 2006}


def panel(ind, pays, annees):
    """Valeurs annuelles interpolées (années x pays), prolongées au plus PROLONGATION ans,
    et masque des valeurs effectivement observées."""
    t = B[(B.indicateur == ind) & B.pays.isin(pays)]
    for dom, a0 in DEBUT_TENDANCE_PISA.items():
        if ind.startswith("pisa_") and ind.endswith(dom):
            t = t[t.annee >= a0]
    if t.empty:
        vide = pd.DataFrame(index=annees, columns=pays, dtype=float)
        return vide, vide.notna()
    s = raccorder(ind, t.pivot_table(index="annee", columns="pays", values="valeur").reindex(columns=pays))
    tout = range(min(s.index.min(), annees[0]), max(s.index.max(), annees[-1]) + 1)
    s = s.reindex(tout)
    observe = s.notna().reindex(annees, fill_value=False)
    s = s.interpolate(limit_area="inside").ffill(limit=PROLONGATION).bfill(limit=PROLONGATION)
    return s.reindex(annees), observe


def poids(dispo, domaine, objectif_de):
    """Poids de chaque indicateur disponible dans le score (agrégation du bulletin)."""
    w = {}
    for o in sorted(set(objectif_de.values())):
        ids = [i for i in dispo if objectif_de[i] == o]
        if not ids:
            continue
        if domaine == "sante" and o == "S2":
            blocs = [[i] for i in ids if i not in IMAGERIE] + [[i for i in ids if i in IMAGERIE]]
        else:
            blocs = [[i] for i in ids]
        blocs = [b for b in blocs if b]
        for b in blocs:
            for i in b:
                w[i] = 0.25 / len(blocs) / len(b)
    return w


def indice(domaine):
    pays, annees = PAYS[domaine], ANNEES[domaine]
    X, obs, objectif_de, retenus, exclus = {}, {}, {}, [], []
    for ident, _, obj, _, pol, _, _ in (d for d in be.DICO if d[1] == CODE[domaine]):
        if ident in RELATIFS:
            exclus.append(ident + " (relatif)")
            continue
        p, o = panel(ident, pays, annees)
        if p.notna().mean(axis=1).max() < COUVERTURE_MIN:
            exclus.append(ident)
            continue
        n = (p - np.nanmin(p.values)) / (np.nanmax(p.values) - np.nanmin(p.values))   # bornes fixes
        X[ident] = 1 - n if pol == "-" else n
        obs[ident], objectif_de[ident] = o, obj
        retenus.append(ident)
    objectifs = sorted(set(objectif_de.values()))

    lignes, contrib = [], []
    for p in pays:
        V = pd.DataFrame({i: X[i][p] for i in retenus})          # années x indicateurs
        # niveau de référence : score à bornes fixes de l'année de référence, panier complet
        w_ref = poids([i for i in retenus if pd.notna(V.loc[REFERENCE, i])], domaine, objectif_de)
        niveau = {o: sum(4 * w * V.loc[REFERENCE, i] for i, w in w_ref.items() if objectif_de[i] == o)
                  for o in objectifs}
        # variations chaînées, à panier identique sur chaque couple d'années
        dO = pd.DataFrame(0.0, index=annees, columns=objectifs)
        nb = pd.Series(0, index=annees)
        for a in annees[1:]:
            dispo = [i for i in retenus if pd.notna(V.loc[a - 1, i]) and pd.notna(V.loc[a, i])]
            nb[a] = len(dispo)
            for i, w in poids(dispo, domaine, objectif_de).items():
                d = w * (V.loc[a, i] - V.loc[a - 1, i])
                dO.loc[a, objectif_de[i]] += 4 * d
                contrib.append((domaine, p, a, i, objectif_de[i], 100 * d,
                                bool(obs[i].loc[a, p] and obs[i].loc[a - 1, p])))
        cum = dO.cumsum()
        O = cum - cum.loc[REFERENCE] + pd.Series(niveau)
        score = O.mean(axis=1)
        # variante à panier constant : indicateurs disponibles toutes les années depuis PANIER_CONSTANT
        a0 = PANIER_CONSTANT[domaine]
        fixe = [i for i in retenus if V.loc[a0:, i].notna().all()]
        w_fixe = poids(fixe, domaine, objectif_de)
        constant = sum(w * V[i] for i, w in w_fixe.items()).where(V.index >= a0)
        for a in annees:
            lignes.append({"domaine": domaine, "annee": a, "pays": p, "score": score[a],
                           **{f"objectif_{o}": O.loc[a, o] for o in objectifs},
                           "nb_indicateurs": nb[a] if a > annees[0] else nb[annees[1]],
                           "score_panier_constant": constant[a]})
    C = pd.DataFrame(contrib, columns=["domaine", "pays", "annee", "indicateur", "objectif", "contribution",
                                       "observe"])
    return pd.DataFrame(lignes), C, retenus, exclus


def main():
    tables, contributions = [], []
    for dom in ANNEES:
        T, C, retenus, exclus = indice(dom)
        tables.append(T)
        contributions.append(C)
        print(f"\n{dom} : {len(retenus)} indicateurs ; exclus : {', '.join(exclus) or 'aucun'}")
        sc = T.pivot(index="pays", columns="annee", values="score")
        print(sc[[a for a in sc.columns if a % 5 == 0 or a == sc.columns[-1]]].round(3)
              .sort_values(sc.columns[-1], ascending=False).to_string())
        nb = T.pivot(index="pays", columns="annee", values="nb_indicateurs")
        print("nombre d'indicateurs par pays (médiane) :",
              " ".join(f"{a}:{int(nb[a].median())}" for a in nb.columns if a % 5 == 0))
    T, C = pd.concat(tables), pd.concat(contributions)
    T.to_csv(ICI / "evolution_scores.csv", index=False, float_format="%.4f")
    C.to_csv(ICI / "evolution_contributions.csv", index=False, float_format="%.4f")
    j = pd.DataFrame(sorted(set(JOURNAL)), columns=["indicateur", "pays", "annee", "decalage"])
    j.to_csv(ICI / "evolution_ruptures.csv", index=False)
    print(f"\n{len(j)} ruptures raccordées (evolution_ruptures.csv)")

    poids_ue = {"education": bu.eleves, "sante": bu.pop}       # pondérations fixes (2022)
    for dom in ANNEES:
        sc = T[T.domaine == dom].pivot(index="annee", columns="pays", values="score")
        w = poids_ue[dom].reindex(sc.columns)
        ue = (sc * w).sum(axis=1) / (sc.notna() * w).sum(axis=1)
        fig, ax = plt.subplots(figsize=(10, 5.5))
        for p in sc.columns:
            if p not in VEDETTES:
                ax.plot(sc.index, sc[p], color="#c9cdd1", lw=0.8, zorder=1)
        for p, c in VEDETTES.items():
            ax.plot(sc.index, sc[p], color=c, lw=2.2, label=NOMS[p], zorder=3)
            v = VAGUES.get(dom, [])
            ax.plot(v, sc.loc[v, p], color=c, lw=0, marker="o", ms=4, zorder=4)
        ax.plot(sc.index, ue, color="#222222", lw=2, ls="--", label="Moyenne UE", zorder=2)
        for v in VAGUES.get(dom, []):
            ax.axvline(v, color="#999999", lw=0.6, ls=":", zorder=0)
        # panier réduit : moins des deux tiers des indicateurs (médiane des pays)
        nbm = T[T.domaine == dom].groupby("annee").nb_indicateurs.median()
        mince = nbm[nbm < 2 / 3 * nbm.max()].index
        if len(mince):
            ax.axvspan(sc.index[0] - 0.5, mince.max() + 0.5, color="#eeeeee", zorder=0)
            ax.text(sc.index[0], ax.get_ylim()[1], f" panier réduit (moins de {int(2 / 3 * nbm.max())} "
                    "indicateurs) : à lire avec prudence", fontsize=8, color="#777777", va="top")
        ax.set_ylabel(f"Score composite, bornes fixes, chaîné (niveau {REFERENCE})")
        ax.set_xticks(sc.index[::2])
        ax.spines[["top", "right"]].set_visible(False)
        ax.grid(axis="y", alpha=0.3)
        ax.legend(frameon=False, ncol=3, loc="lower left")
        if dom in VAGUES:
            ax.set_title("Points : années PISA (entre deux vagues, PISA et TIMSS sont interpolés)",
                         fontsize=9, loc="left", color="#555555")
        fig.tight_layout()
        fig.savefig(FIG / f"evolution_{dom}.png", dpi=150)
        plt.close(fig)

        f = C[(C.domaine == dom) & (C.pays == "FR")].groupby(["annee", "observe"]).contribution.sum()
        f = f.unstack().reindex(columns=[True, False]).fillna(0)
        f.columns = ["observé", "interpolé"]
        t = T[(T.domaine == dom) & (T.pays == "FR")].set_index("annee")
        f.insert(0, "variation", f.sum(axis=1))
        f.insert(0, "score", t.score.reindex(f.index))
        f["panier_constant"] = t.score_panier_constant.reindex(f.index)
        f["UE"] = ue.reindex(f.index)
        print(f"\nFrance, {dom} (variations en points de score) :")
        print(f.round(3).to_string())


if __name__ == "__main__":
    main()
