"""
Nuages d'électeurs sur données réelles : Baromètre de la confiance politique (CEVIPOF /
Sciences Po, terrain OpinionWay, panel en ligne avec quotas), licence CC-BY 4.0.

Quatre vagues, France uniquement (extraits produits par extract_barometre.py) :
  - vague 9  (décembre 2017, N = 2 084)  : vote déclaré au 1er tour de 2017 ;
  - vague 13 (terrain 23 déc. 2021 - 10 janv. 2022, N = 10 566) : intention de vote au 1er tour de 2022 ;
  - vague 15 (terrain 22-29 janvier 2024, N = 3 514 en France) : vote déclaré au 1er tour de 2022 (souvenir) ;
  - vague 16 (terrain 17 janv. - 5 févr. 2025, N = 3 561 en France) : idem.
Vague 9 : terrain 13-26 décembre 2017. Le jitter (paramètre jit) sert seulement à dé-superposer
les points d'un indice discret ; il est plus fort quand les items sont peu nombreux.

Chaque axe est la moyenne d'items d'opinion standardisés et orientés (voir ITEMS), puis
centrée-réduite. Axe économique orienté libéralisme > 0, axe culturel orienté fermeture > 0.
Un point = un répondant (non pondéré) ; barycentres et parts de voix pondérés (poids politique).
"""
import json
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from nuages_cses import (ABST_COL, AUTRES_COL, GRID, HALO, INK, INK2, MUTED, SURFACE,
                         jitter, nuage, points_barycentres, legende_gris, note_source, r2_vote)

HERE = Path(__file__).resolve().parent
DATA, OUT = HERE / "data" / "barometre", HERE / "figures"
RNG = np.random.default_rng(2022)

# ---------------------------------------------------------------- items par vague
# (signe, code valide maximal) ; signe = +1 si un code élevé va vers le pôle positif de l'axe
# (fermeture pour la culture, libéralisme pour l'économie). Codes 1 = tout à fait d'accord …
# 4 = pas du tout d'accord, NSP = 5 (absent en 2024-2025) sauf mention contraire.
ITEMS = {
    "V9_2017": dict(
        culture={"q27_i1": (-1, 4),    # il faudrait rétablir la peine de mort
                 "q27_i2": (-1, 4),    # il y a trop d'immigrés en France
                 "q27_i3": (-1, 4),    # il faudrait supprimer la loi autorisant le mariage homosexuel
                 "q27_i16": (+1, 4),   # il faudrait autoriser la PMA pour les femmes seules ou homosexuelles
                 "q27_i13": (-1, 4),   # de nos jours les parents n'ont plus aucune autorité
                 "n43_i4": (-1, 4),    # l'islam représente une menace pour la République
                 "n43_i5": (-1, 4),    # les enfants d'immigrés nés en France ne sont pas vraiment français
                 "n43_i6": (+1, 4),    # l'immigration est une source d'enrichissement culturel
                 "nou10_i4": (-1, 4),  # en matière d'emploi, priorité à un Français sur un immigré
                 "nou10_i2": (-1, 4)}, # quand l'emploi est en crise, les hommes prioritaires sur les femmes
        economie={"q27_i8": (-1, 4),   # il faudrait réduire le nombre de fonctionnaires
                  "q27_i17": (+1, 4),  # l'économie actuelle profite aux patrons aux dépens de ceux qui travaillent
                  "q27_i14": (-1, 4),  # les chômeurs pourraient trouver du travail s'ils le voulaient vraiment
                  "q31": (+1, 4),      # pour la justice sociale, il faudrait prendre aux riches pour donner aux pauvres
                  "q32": (+1, 3),      # le système capitaliste : 1 réformé en profondeur … 3 pas réformé (NSP = 4)
                  "nou10_i1": (-1, 4), # les patrons devraient avoir le droit de licencier plus facilement
                  "nou7": (-1, 2)},    # priorité : 1 compétitivité de l'économie, 2 situation des salariés (NSP = 3)
        vote="r36ab", abst_codes=(14, 15), blancs=(12, 13), nsp=(16,), poids="Poids1",
        cands={5: "Macron", 9: "Le Pen", 7: "Fillon", 3: "Mélenchon", 4: "Hamon", 8: "Dupont-Aignan"},
        periode="décembre 2017", jit=0.05, vote_txt="vote déclaré au 1er tour de 2017"),
    "V13_2022": dict(
        culture={"Q27_i2": (-1, 4), "q27_i22": (-1, 4),   # trop d'immigrés ; peine de mort
                 "q27_i18": (+1, 4),                       # la PMA est une bonne chose pour les femmes seules ou homosexuelles
                 "n43_i4": (-1, 4), "n43_i6": (+1, 4),     # islam menace ; immigration enrichissement culturel
                 "qcb1_i3": (-1, 4)},                      # plutôt que de nouveaux droits, il faut une bonne dose d'autorité et d'ordre
        economie={"q27_i8": (-1, 4), "q27_i17": (+1, 4), "q27_i14": (-1, 4),
                  "q27_i23": (+1, 4),                      # prendre aux riches pour donner aux pauvres
                  "q32": (+1, 3)},
        vote="ivt1_2", abst_codes=(15,), blancs=(14,), nsp=(16,), poids="Poids1",
        cands={8: "Macron", 12: "Le Pen", 11: "Zemmour", 4: "Mélenchon", 9: "Pécresse", 7: "Jadot", 6: "Hidalgo"},
        periode="janvier 2022", jit=0.09, vote_txt="intention de vote au 1er tour de 2022"),
    "V15_2024": dict(
        culture={"q27_i2": (-1, 4), "q27_i22": (-1, 4),
                 "q27_i31": (-1, 4),                       # l'islam représente une menace pour la République
                 "q27_i32": (+1, 4)},                      # la France devrait évoluer vers un modèle multiculturel
        economie={"q27_i8": (-1, 4), "q27_i14": (-1, 4), "q27_i23": (+1, 4),
                  "q31bv15_i4": (+1, 4)},                  # c'est une société où il y a trop d'inégalités
        vote="t12022", turnout="v0t1", blancs=(13, 14), poids="poids1",
        cands={7: "Macron", 11: "Le Pen", 10: "Zemmour", 4: "Mélenchon", 8: "Pécresse", 6: "Jadot", 5: "Hidalgo"},
        periode="janvier 2024", jit=0.10, vote_txt="vote déclaré au 1er tour de 2022"),
    "V16_2025": dict(
        culture={"q27_i2": (-1, 4), "q27_i22": (-1, 4), "q27_i32": (+1, 4),
                 "q6v16_i4": (-1, 4),                      # on a besoin d'un vrai chef en France pour remettre de l'ordre
                 "q17v16": (-1, 4)},                       # le trafic de stupéfiants est lié à l'immigration (1 oui tout à fait … 4 non pas du tout)
        economie={"q27_i8": (-1, 4), "q27_i14": (-1, 4), "q27_i23": (+1, 4),
                  "q9v16": (-1, 10)},                      # 0 compétitivité de l'économie … 10 situation des salariés (orientation vérifiée par corrélation avec q27_i23)
        vote="t12022", turnout="v0t1", blancs=(13, 14), poids="poids5",
        cands={7: "Macron", 11: "Le Pen", 10: "Zemmour", 4: "Mélenchon", 8: "Pécresse", 6: "Jadot", 5: "Hidalgo"},
        periode="janvier-février 2025", jit=0.10, vote_txt="vote déclaré au 1er tour de 2022"),
}
PAL = {"Macron": "#C48A1C", "Le Pen": "#2A4A9C", "Fillon": "#4E8FD0", "Mélenchon": "#B4443E", "Hamon": "#D9679B",
       "Dupont-Aignan": "#6E8B3D", "Zemmour": "#8A4FA8", "Pécresse": "#4E8FD0", "Jadot": "#3E9C8F", "Hidalgo": "#D9679B"}
SRC = "Baromètre de la confiance politique (CEVIPOF / Sciences Po, OpinionWay, panel en ligne), vague {v} ; points non pondérés, barycentres pondérés"


# ---------------------------------------------------------------- construction
def indice(d, spec, min_share=0.7):
    X = pd.DataFrame({it: d[it].where((d[it] >= 0) & (d[it] <= vmax)) for it, (s, vmax) in spec.items()})
    Z = (X - X.mean()) / X.std()
    S = Z * np.array([s for s, _ in spec.values()])
    ok = S.notna().sum(axis=1) >= np.ceil(min_share * len(spec))
    idx = S.mean(axis=1).where(ok)
    alpha = len(spec) / (len(spec) - 1) * (1 - S.var().sum() / S.dropna().sum(axis=1).var())
    ev = np.linalg.eigvalsh(S.dropna().corr().values)[::-1]
    return (idx - idx.mean()) / idx.std(), float(alpha), float(ev[0] / len(spec))


def classes(d, spec):
    cl = pd.Series(np.nan, index=d.index, dtype=object)
    v = d[spec["vote"]]
    if "turnout" in spec:
        cl[d[spec["turnout"]].isin([2, 3])] = "abstention"      # non inscrit ou abstention
        cl[v.notna()] = "autres"
    else:
        cl[v.isin(spec["abst_codes"])] = "abstention"
        cl[v.notna() & ~v.isin(spec["abst_codes"]) & ~v.isin(spec["nsp"])] = "autres"
    cl[v.isin(spec["blancs"])] = "blanc"                        # blanc ou nul : dessiné comme « autres », hors exprimés
    for code, nom in spec["cands"].items():
        cl[v == code] = nom
    return cl


def charger(vague):
    spec = ITEMS[vague]
    d = pd.read_csv(DATA / f"{vague}_fr.csv")
    eco, a_e, ev_e = indice(d, spec["economie"])
    cul, a_c, ev_c = indice(d, spec["culture"])
    df = pd.DataFrame({"eco": eco, "cult": cul, "classe": classes(d, spec), "w": d[spec["poids"]],
                       "gd": d["nou1"].where(d["nou1"] <= 10)})
    return df, dict(alpha_eco=a_e, ev1_eco=ev_e, alpha_cult=a_c, ev1_cult=ev_c)


def parts(df, cands):
    expr = df["classe"].isin(cands + ["autres"])
    tot = df.loc[expr, "w"].sum()
    return {c: float(df.loc[expr & (df["classe"] == c), "w"].sum() / tot) for c in cands}


def barycentres(df, cands):
    b = {}
    for c in cands + ["abstention"]:
        m = (df["classe"] == c) & df["eco"].notna() & df["cult"].notna()
        b[c] = (float(np.average(df.loc[m, "eco"], weights=df.loc[m, "w"])),
                float(np.average(df.loc[m, "cult"], weights=df.loc[m, "w"])), int(m.sum()))
    return b


# ---------------------------------------------------------------- figures
def axes_ec(ax, n_e, n_c, labels=True, court=False):
    ax.set_xlim(-3.1, 3.1); ax.set_ylim(-3.1, 3.1); ax.set_aspect("equal")
    ax.set_xticks([-3, -2, -1, 0, 1, 2, 3]); ax.set_yticks([-3, -2, -1, 0, 1, 2, 3])
    ax.axhline(0, color=GRID, lw=0.6, zorder=0); ax.axvline(0, color=GRID, lw=0.6, zorder=0)
    if labels and not court:
        ax.set_xlabel(f"Indice économique, {n_e} items (écarts-types)\n←  interventionnisme                          libéralisme  →", labelpad=8)
        ax.set_ylabel(f"Indice culturel, {n_c} items (écarts-types)\n←  ouverture                          fermeture  →", labelpad=8)
    elif labels:
        ax.set_xlabel("Économie   ←  interv.        libéral.  →")
        ax.set_ylabel("Culture   ←  ouverture        fermeture  →")


def fig_nuage(vague, df, bary, nom, offsets, s=13, alpha=0.6):
    spec = ITEMS[vague]
    m = df["eco"].notna() & df["cult"].notna() & df["classe"].notna()
    d = df[m]
    x, y = jitter(d["eco"].values, spec["jit"]), jitter(d["cult"].values, spec["jit"])
    fig, ax = plt.subplots(figsize=(7.6, 7.6))
    nuage(ax, x, y, d["classe"].replace("blanc", "autres"), {c: PAL[c] for c in spec["cands"].values()}, s=s, alpha=alpha)
    points_barycentres(ax, {c: bary[c] for c in spec["cands"].values()}, PAL, offsets=offsets)
    axes_ec(ax, len(spec["economie"]), len(spec["culture"]))
    ax.set_title(f"France, {spec['periode']} : un point par répondant, coloré par son {spec['vote_txt']}", loc="left", fontsize=11, pad=12)
    legende_gris(ax, int((d["classe"] == "abstention").sum()), loc="lower right")
    fig.subplots_adjust(bottom=0.15)
    note_source(fig, SRC.format(v=vague.split("_")[0][1:]))
    fig.savefig(OUT / nom); plt.close(fig)
    return int(m.sum())


def fig_panneaux(vague, df, bary, prt, nom, ncol=3, abst_panel=False, s=9):
    spec = ITEMS[vague]
    m = df["eco"].notna() & df["cult"].notna() & df["classe"].notna()
    d = df[m]
    x, y = jitter(d["eco"].values, spec["jit"]), jitter(d["cult"].values, spec["jit"])
    cands = list(spec["cands"].values()) + (["abstention"] if abst_panel else [])
    nrow = int(np.ceil(len(cands) / ncol))
    fig, axes = plt.subplots(nrow, ncol, figsize=(4.2 * ncol, 4.3 * nrow), sharex=True, sharey=True)
    for ax, c in zip(axes.ravel(), cands):
        ax.scatter(x, y, s=s - 3, c="#C9CCD1", alpha=0.3, lw=0, zorder=1, rasterized=True)
        k = (d["classe"] == c).values
        col = PAL.get(c, "#7A8088")
        ax.scatter(x[k], y[k], s=s, c=col, alpha=0.65, lw=0, zorder=2, rasterized=True)
        bx, by, n = bary[c]
        ax.scatter(bx, by, s=70, color=col, ec=SURFACE, lw=1.5, zorder=5)
        axes_ec(ax, 0, 0, labels=False)
        titre = f"{c}  ·  {100 * prt[c]:.0f} % des exprimés  ·  n = {n}" if c in prt else f"{c}  ·  n = {n}"
        ax.set_title(titre, loc="left", fontsize=10.5, fontweight="bold", color=col, pad=6)
    for ax in axes.ravel()[len(cands):]:
        ax.axis("off")
    for ax in axes[-1]:
        ax.set_xlabel("Économie   ←  interv.        libéral.  →")
    for ax in axes[:, 0]:
        ax.set_ylabel("Culture   ←  ouverture        fermeture  →")
    fig.suptitle(f"L'électorat de chaque candidat dans le même plan, France {spec['periode']} ({spec['vote_txt']} ; fond gris : tous les répondants)",
                 x=0.04, ha="left", fontsize=11.5, y=0.985)
    note_source(fig, SRC.format(v=vague.split("_")[0][1:]))
    fig.tight_layout(rect=(0, 0.02, 1, 0.97))
    fig.savefig(OUT / nom); plt.close(fig)


def fig_quatre_dates(dfs, nom):
    """Les quatre vagues côte à côte, densité de tous les répondants (sans couleur de vote)."""
    fig, axes = plt.subplots(1, 4, figsize=(16, 4.6), sharex=True, sharey=True)
    for ax, (vague, df) in zip(axes, dfs.items()):
        m = df["eco"].notna() & df["cult"].notna()
        ax.scatter(jitter(df.loc[m, "eco"].values, ITEMS[vague]["jit"]), jitter(df.loc[m, "cult"].values, ITEMS[vague]["jit"]),
                   s=5 if m.sum() > 5000 else 8, c="#5A6270", alpha=0.25 if m.sum() > 5000 else 0.35, lw=0, rasterized=True)  # noqa
        axes_ec(ax, 0, 0, labels=False)
        r = np.corrcoef(df.loc[m, "eco"], df.loc[m, "cult"])[0, 1]
        ax.set_title(f"{ITEMS[vague]['periode']}  ·  n = {m.sum():,}  ·  r = {r:+.2f}".replace(",", " "), loc="left", fontsize=10.5, pad=6)
        ax.set_xlabel("Économie   ←  interv.        libéral.  →")
    axes[0].set_ylabel("Culture   ←  ouverture        fermeture  →")
    fig.suptitle("La forme du nuage à quatre dates (tous les répondants ; les items diffèrent d'une vague à l'autre, voir la note)",
                 x=0.03, ha="left", fontsize=11.5, y=0.99)
    fig.text(0.99, -0.03, "Baromètre de la confiance politique, vagues 9, 13, 15 et 16 ; points non pondérés", fontsize=7.5, color=MUTED, ha="right")
    fig.tight_layout(rect=(0, 0, 1, 0.95))
    fig.savefig(OUT / nom); plt.close(fig)


def main():
    res, dfs = {}, {}
    for vague, spec in ITEMS.items():
        df, qual = charger(vague)
        dfs[vague] = df
        cands = list(spec["cands"].values())
        prt, bary = parts(df, cands), barycentres(df, cands)
        m = df["eco"].notna() & df["cult"].notna()
        w = df.loc[m, "w"]
        quad = {"interv_ouvert": float(np.average((df.loc[m, "eco"] < 0) & (df.loc[m, "cult"] < 0), weights=w)),
                "interv_ferme": float(np.average((df.loc[m, "eco"] < 0) & (df.loc[m, "cult"] >= 0), weights=w)),
                "liberal_ouvert": float(np.average((df.loc[m, "eco"] >= 0) & (df.loc[m, "cult"] < 0), weights=w)),
                "liberal_ferme": float(np.average((df.loc[m, "eco"] >= 0) & (df.loc[m, "cult"] >= 0), weights=w))}
        res[vague] = dict(N=int(len(df)), N_axes=int(m.sum()), **qual,
                          corr_eco_culture=float(np.corrcoef(df.loc[m, "eco"], df.loc[m, "cult"])[0, 1]),
                          corr_gd_eco=float(df[["gd", "eco"]].corr().iloc[0, 1]), corr_gd_culture=float(df[["gd", "cult"]].corr().iloc[0, 1]),
                          R2_vote_sur_eco=r2_vote(df, "eco", cands), R2_vote_sur_culture=r2_vote(df, "cult", cands),
                          R2_vote_sur_gd=r2_vote(df, "gd", cands),
                          effectifs=df["classe"].value_counts(dropna=False).rename(index=str).to_dict(),
                          parts_exprimes=prt, barycentres=bary, quadrants_ponderes=quad)
    o17 = {"Le Pen": (0.10, 0.10), "Fillon": (0.10, -0.12), "Dupont-Aignan": (-0.10, 0.10), "Macron": (0.10, -0.12), "Hamon": (-0.10, -0.12), "Mélenchon": (-0.10, 0.10)}
    o22 = {"Le Pen": (0.10, 0.10), "Zemmour": (0.10, 0.10), "Pécresse": (0.10, -0.12), "Macron": (0.10, -0.12), "Hidalgo": (-0.10, -0.14), "Mélenchon": (-0.10, 0.10), "Jadot": (0.10, -0.14)}
    o25 = {"Le Pen": (0.10, 0.10), "Zemmour": (0.10, 0.10), "Pécresse": (0.10, -0.12), "Macron": (0.10, -0.12), "Hidalgo": (0.10, -0.14), "Mélenchon": (-0.10, -0.14), "Jadot": (-0.10, 0.10)}
    res["V9_2017"]["N_fig"] = fig_nuage("V9_2017", dfs["V9_2017"], res["V9_2017"]["barycentres"], "b1_nuage_2017.png", o17)
    fig_panneaux("V9_2017", dfs["V9_2017"], res["V9_2017"]["barycentres"], res["V9_2017"]["parts_exprimes"], "b2_par_candidat_2017.png")
    res["V13_2022"]["N_fig"] = fig_nuage("V13_2022", dfs["V13_2022"], res["V13_2022"]["barycentres"], "b3_nuage_2022_intentions.png", o22, s=6, alpha=0.45)
    fig_panneaux("V13_2022", dfs["V13_2022"], res["V13_2022"]["barycentres"], res["V13_2022"]["parts_exprimes"], "b4_par_candidat_2022_intentions.png", ncol=4, abst_panel=True, s=6)
    res["V16_2025"]["N_fig"] = fig_nuage("V16_2025", dfs["V16_2025"], res["V16_2025"]["barycentres"], "b5_nuage_2025_vote2022.png", o25, s=11, alpha=0.6)
    fig_quatre_dates(dfs, "b6_quatre_dates.png")
    (HERE / "resultats_barometre.json").write_text(json.dumps(res, indent=2, ensure_ascii=False))
    for v, r in res.items():
        print(f"{v}: N={r['N']} axes={r['N_axes']} alpha_eco={r['alpha_eco']:.2f} ev1_eco={r['ev1_eco']:.2f} alpha_cult={r['alpha_cult']:.2f} ev1_cult={r['ev1_cult']:.2f} "
              f"r(E,C)={r['corr_eco_culture']:+.3f} R2 eco={r['R2_vote_sur_eco']:.2f} cult={r['R2_vote_sur_culture']:.2f} gd={r['R2_vote_sur_gd']:.2f} quad={ {k: round(v_, 2) for k, v_ in r['quadrants_ponderes'].items()} }")
        print("   parts:", {k: round(100 * v_, 1) for k, v_ in r["parts_exprimes"].items()})
        print("   bary :", {k: (round(a, 2), round(b, 2), n) for k, (a, b, n) in r["barycentres"].items()})


if __name__ == "__main__":
    main()
