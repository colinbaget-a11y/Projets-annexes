"""
Nuages d'électeurs sur données réelles : un point par répondant, coloré par son vote.

Source : CSES (Comparative Study of Electoral Systems), vagues françaises
  - 2017, module 5 (enquête post-électorale Kantar Public, face-à-face, N = 1 830) ;
  - 2012, module 4 (N = 2 014).
Entrées : data/fr2017_cses5.csv, data/fr2012_cses4.csv (voir extract_cses.py).
Sorties : figures/r*.png et resultats_cses.json.

Construction des axes
  2017  x : item unique « L'État devrait prendre des mesures pour réduire les écarts
            de revenus » (5 modalités, d'accord = interventionniste, à gauche du graphique) ;
        y : indice culturel = moyenne de 9 items standardisés (5 sur les minorités et
            l'immigration, 4 sur ce qui fait un « vrai » Français), orienté fermeture > 0,
            puis centré-réduit. Alpha de Cronbach 0,83 ; première valeur propre 4,0 sur 9.
  2012  x : indice économique = moyenne de 6 items standardisés (dépenses de santé,
            d'éducation, d'indemnisation du chômage, de retraites, de prestations sociales,
            et réduction des écarts de revenus), orienté libéralisme > 0. Alpha 0,66.
        y : auto-positionnement gauche-droite 0-10 (pas d'items culturels dans cette vague).
Les points sont non pondérés (un point = un répondant). Les barycentres et les parts de
voix affichés utilisent le poids « politique » fourni par l'enquête (calé sur les résultats
officiels du premier tour).
"""
import json
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
from matplotlib.lines import Line2D

HERE = Path(__file__).resolve().parent
DATA, OUT = HERE / "data", HERE / "figures"
OUT.mkdir(exist_ok=True)
RNG = np.random.default_rng(2017)

# ---------------------------------------------------------------- style (identique au prototype simulé)
INK, INK2, MUTED, GRID, SURFACE = "#1F2328", "#4B5158", "#8A9099", "#E6E8EA", "#FCFCFB"
ABST_COL, AUTRES_COL = "#D3D6DA", "#A6ABB3"
plt.rcParams.update({
    "font.family": "Liberation Sans", "font.size": 10,
    "axes.edgecolor": MUTED, "axes.linewidth": 0.6,
    "axes.labelcolor": INK2, "axes.titlecolor": INK,
    "xtick.color": INK2, "ytick.color": INK2, "xtick.labelsize": 9, "ytick.labelsize": 9,
    "axes.spines.top": False, "axes.spines.right": False,
    "figure.facecolor": SURFACE, "axes.facecolor": SURFACE, "savefig.facecolor": SURFACE,
    "figure.dpi": 200, "savefig.dpi": 200, "savefig.bbox": "tight", "savefig.pad_inches": 0.25,
})
HALO = [pe.withStroke(linewidth=2.6, foreground=SURFACE)]

# ---------------------------------------------------------------- codes CSES
# 2017, module 5 : E3013_PR_1 (vote 1er tour). Couleurs = palette du prototype (parti du candidat).
CAND17 = {250001: ("Macron", "#C48A1C"), 250002: ("Le Pen", "#2A4A9C"), 250003: ("Fillon", "#4E8FD0"),
          250004: ("Mélenchon", "#B4443E"), 250005: ("Hamon", "#D9679B"), 250006: ("Dupont-Aignan", "#6E8B3D")}
# 2012, module 4 : D3006_PR_1.
CAND12 = {5: ("Hollande", "#D9679B"), 7: ("Sarkozy", "#4E8FD0"), 9: ("Le Pen", "#2A4A9C"),
          3: ("Mélenchon", "#B4443E"), 6: ("Bayrou", "#C48A1C"), 4: ("Joly", "#3E9C8F")}

# Items culturels 2017 : signe = +1 si un code élevé (désaccord / « pas important ») va vers la fermeture.
# Codes : 1 tout à fait d'accord … 5 pas du tout d'accord (E3005) ; 1 très important … 4 pas du tout (E3006).
CULT17 = {"E3005_1": -1,   # les minorités doivent s'adapter aux coutumes et traditions du pays
          "E3005_2": -1,   # la volonté de la majorité doit prévaloir, même sur les droits des minorités
          "E3005_3": +1,   # les immigrés sont généralement bons pour l'économie
          "E3005_4": -1,   # la culture du pays est généralement abîmée par les immigrés
          "E3005_5": -1,   # les immigrés augmentent la criminalité
          "E3006_1": -1,   # important pour être vraiment français : être né en France
          "E3006_2": -1,   # … avoir des ancêtres français
          "E3006_3": -1,   # … parler français
          "E3006_4": -1}   # … suivre les coutumes et traditions françaises
# Items économiques 2012 : 1 = beaucoup plus de dépenses / tout à fait d'accord pour réduire les écarts
# … 5 = beaucoup moins / pas du tout d'accord ; un code élevé va vers le libéralisme (signe +1).
ECO12 = {"D3001_1": +1, "D3001_2": +1, "D3001_3": +1, "D3001_5": +1, "D3001_8": +1, "D3004": +1}


# ---------------------------------------------------------------- construction des variables
def indice(df, spec, min_items):
    """Moyenne des items standardisés et orientés (score positif = pôle 'fermeture' ou 'libéral'),
    calculée si au moins min_items sont renseignés, puis centrée-réduite."""
    X = df[list(spec)].where(df[list(spec)] < 7)          # 7, 8, 9 = refus, NSP, manquant
    Z = (X - X.mean()) / X.std()
    S = Z * np.array(list(spec.values()))
    idx = S.mean(axis=1).where(S.notna().sum(axis=1) >= min_items)
    return (idx - idx.mean()) / idx.std()


def classes_2017(d):
    cl = pd.Series(np.nan, index=d.index, dtype=object)
    v = d["E3013_PR_1"]
    cl[d["E3012_PR_1"] == 0] = "abstention"
    for code, (nom, _) in CAND17.items():
        cl[v == code] = nom
    autres = v.isin(list(range(250007, 250016)) + [999988, 999989, 999990, 999991, 999992, 999993])
    cl[autres] = "autres"
    return cl                                                # refus / NSP / incohérents restent NaN


def classes_2012(d):
    cl = pd.Series(np.nan, index=d.index, dtype=object)
    v = d["D3006_PR_1"]
    cl[d["D3005_PR_1"] == 5] = "abstention"
    for code, (nom, _) in CAND12.items():
        cl[v == code] = nom
    cl[v.isin([1, 2, 8, 10, 89, 90, 91, 92, 93])] = "autres"
    return cl


def charger_2017():
    d = pd.read_csv(DATA / "fr2017_cses5.csv")
    out = pd.DataFrame({
        "eco": d["E3008"].where(d["E3008"] < 7) - 3,           # -2 (tout à fait d'accord) … +2
        "cult": indice(d, CULT17, min_items=7),
        "gd": d["E3020"].where(d["E3020"] <= 10),
        "classe": classes_2017(d), "w": d["E1010_3"], "vote": d["E3013_PR_1"],
    })
    return out


def charger_2012():
    d = pd.read_csv(DATA / "fr2012_cses4.csv")
    return pd.DataFrame({
        "eco": indice(d, ECO12, min_items=5),
        "gd": d["D3014"].where(d["D3014"] <= 10),
        "classe": classes_2012(d), "w": d["D1010_3"], "vote": d["D3006_PR_1"],
    })


def jitter(x, ampl):
    return x + RNG.uniform(-ampl, ampl, size=len(x))


# ---------------------------------------------------------------- statistiques descriptives
def parts_exprimes(df, cands):
    """Part pondérée de chaque candidat parmi les suffrages exprimés (poids politique)."""
    expr = df["classe"].isin(list(cands) + ["autres"]) & (df["vote"] != 999993) & (df["vote"] != 93)
    tot = df.loc[expr, "w"].sum()
    return {c: float(df.loc[expr & (df["classe"] == c), "w"].sum() / tot) for c in cands}


def barycentres(df, x, y, cands):
    b = {}
    for c in cands:
        m = (df["classe"] == c) & df[x].notna() & df[y].notna()
        b[c] = (float(np.average(df.loc[m, x], weights=df.loc[m, "w"])),
                float(np.average(df.loc[m, y], weights=df.loc[m, "w"])), int(m.sum()))
    return b


def r2_vote(df, var, cands):
    """Part de la variance de `var` expliquée par le vote (ANOVA à un facteur, non pondérée)."""
    m = df["classe"].isin(cands) & df[var].notna()
    g = df.loc[m].groupby("classe")[var]
    sst = ((df.loc[m, var] - df.loc[m, var].mean()) ** 2).sum()
    ssb = sum(len(v) * (v.mean() - df.loc[m, var].mean()) ** 2 for _, v in g)
    return float(ssb / sst)


# ---------------------------------------------------------------- dessin
def nuage(ax, x, y, cl, palette, s=15, alpha=0.65):
    abst, autres = (cl == "abstention").values, (cl == "autres").values
    ax.scatter(x[abst], y[abst], s=s - 2, c=ABST_COL, alpha=0.6, lw=0, zorder=1)
    ax.scatter(x[autres], y[autres], s=s - 2, c=AUTRES_COL, alpha=0.55, lw=0, zorder=2)
    k = np.flatnonzero(cl.isin(palette).values)
    RNG.shuffle(k)
    ax.scatter(x[k], y[k], s=s, c=[palette[c] for c in cl.values[k]], alpha=alpha, lw=0, zorder=3)


def points_barycentres(ax, bary, palette, offsets=None, size=64, fs=9):
    offsets = offsets or {}
    for c, (bx, by, _) in bary.items():
        ax.scatter(bx, by, s=size, color=palette[c], ec=SURFACE, lw=1.5, zorder=6)
        dx, dy = offsets.get(c, (0.10, 0.10))
        ax.text(bx + dx, by + dy, c, fontsize=fs, fontweight="bold", color=palette[c], zorder=7,
                ha="left" if dx >= 0 else "right", va="bottom" if dy >= 0 else "top", path_effects=HALO)


def legende_gris(ax, n_abst, loc="lower right"):
    h = [Line2D([], [], marker="o", ls="", ms=6, color=ABST_COL, label=f"abstention (n = {n_abst})"),
         Line2D([], [], marker="o", ls="", ms=6, color=AUTRES_COL, label="autres candidats, blanc ou nul")]
    ax.legend(handles=h, loc=loc, frameon=False, fontsize=8.5, handletextpad=0.4)


def note_source(fig, texte):
    fig.text(0.99, 0.005, texte, fontsize=7.5, color=MUTED, ha="right")


X17_TICKS = ["tout à fait\nd'accord", "plutôt\nd'accord", "ni l'un\nni l'autre", "plutôt pas\nd'accord", "pas du tout\nd'accord"]
X17_LABEL = "« L'État devrait prendre des mesures pour réduire les écarts de revenus »\n←  interventionnisme                                        libéralisme  →"
Y17_LABEL = "Indice culturel : 9 items immigration et identité nationale (écarts-types)\n←  ouverture                                        fermeture  →"
SRC17 = "CSES module 5, vague française 2017 (Kantar Public, face-à-face, N = 1 830) ; points non pondérés, barycentres pondérés"
SRC12 = "CSES module 4, vague française 2012 (N = 2 014) ; points non pondérés, barycentres pondérés"


def fig_r1(d17, pal, bary):
    m = d17["eco"].notna() & d17["cult"].notna() & d17["classe"].notna()
    s = d17[m]
    x, y = jitter(s["eco"].values, 0.42), jitter(s["cult"].values, 0.04)
    fig, ax = plt.subplots(figsize=(7.6, 7.4))
    nuage(ax, x, y, s["classe"], pal)
    points_barycentres(ax, bary, pal, offsets={"Le Pen": (0.10, 0.10), "Dupont-Aignan": (-0.10, 0.10),
                                               "Fillon": (0.10, -0.12), "Macron": (0.10, -0.12),
                                               "Hamon": (0.10, -0.12), "Mélenchon": (-0.10, 0.10)})
    ax.axhline(0, color=GRID, lw=0.6, zorder=0)
    ax.set_xlim(-2.7, 2.7); ax.set_ylim(-3.1, 3.1)
    ax.set_xticks([-2, -1, 0, 1, 2]); ax.set_xticklabels(X17_TICKS)
    ax.set_xlabel(X17_LABEL, labelpad=8); ax.set_ylabel(Y17_LABEL, labelpad=8)
    ax.set_title("France 2017 : un point par répondant, coloré par son vote au premier tour", loc="left", fontsize=11, pad=12)
    legende_gris(ax, int((s["classe"] == "abstention").sum()))
    fig.subplots_adjust(bottom=0.17)
    note_source(fig, SRC17)
    fig.savefig(OUT / "r1_nuage_2017.png"); plt.close(fig)
    return int(m.sum())


def fig_r2(d17, pal, bary, parts):
    m = d17["eco"].notna() & d17["cult"].notna() & d17["classe"].notna()
    s = d17[m]
    x, y = jitter(s["eco"].values, 0.42), jitter(s["cult"].values, 0.04)
    fig, axes = plt.subplots(2, 3, figsize=(12.6, 8.8), sharex=True, sharey=True)
    for ax, c in zip(axes.ravel(), CAND17_ORDER):
        ax.scatter(x, y, s=9, c="#C9CCD1", alpha=0.3, lw=0, zorder=1)
        k = (s["classe"] == c).values
        ax.scatter(x[k], y[k], s=13, c=pal[c], alpha=0.7, lw=0, zorder=2)
        bx, by, n = bary[c]
        ax.scatter(bx, by, s=70, color=pal[c], ec=SURFACE, lw=1.5, zorder=5)
        ax.axhline(0, color=GRID, lw=0.6, zorder=0)
        ax.set_xlim(-2.7, 2.7); ax.set_ylim(-3.1, 3.1)
        ax.set_xticks([-2, -1, 0, 1, 2]); ax.set_xticklabels(["tout à fait\nd'accord", "plutôt", "ni l'un\nni l'autre", "plutôt pas", "pas du tout\nd'accord"])
        ax.set_title(f"{c}  ·  {100 * parts[c]:.0f} % des exprimés  ·  n = {n}", loc="left", fontsize=10.5, fontweight="bold", color=pal[c], pad=6)
    for ax in axes[1]:
        ax.set_xlabel("« L'État devrait réduire les écarts de revenus »\n←  interv.                    libéral.  →")
    for ax in axes[:, 0]:
        ax.set_ylabel("Indice culturel (é.-t.)\n←  ouverture        fermeture  →")
    fig.suptitle("L'électorat de chaque candidat dans le même plan, France 2017 (fond gris : tous les répondants)",
                 x=0.04, ha="left", fontsize=11.5, y=0.985)
    note_source(fig, SRC17)
    fig.tight_layout(rect=(0, 0.02, 1, 0.97))
    fig.savefig(OUT / "r2_par_candidat_2017.png"); plt.close(fig)


def fig_r3(d17, pal):
    m = d17["gd"].notna() & d17["cult"].notna() & d17["classe"].notna()
    s = d17[m]
    x, y = jitter(s["gd"].values, 0.40), jitter(s["cult"].values, 0.04)
    bary = barycentres(s, "gd", "cult", CAND17_ORDER)
    fig, ax = plt.subplots(figsize=(7.6, 7.4))
    nuage(ax, x, y, s["classe"], pal)
    points_barycentres(ax, bary, pal, offsets={"Le Pen": (0.18, 0.10), "Dupont-Aignan": (-0.18, 0.10),
                                               "Fillon": (0.18, -0.12), "Macron": (0.18, -0.12),
                                               "Hamon": (0.18, -0.12), "Mélenchon": (-0.18, 0.10)})
    ax.axhline(0, color=GRID, lw=0.6, zorder=0)
    ax.set_xlim(-0.8, 10.8); ax.set_ylim(-3.1, 3.1); ax.set_xticks(range(11))
    ax.set_xlabel("Auto-positionnement sur l'échelle gauche (0) – droite (10)", labelpad=8)
    ax.set_ylabel(Y17_LABEL, labelpad=8)
    ax.set_title("France 2017 : gauche-droite déclaré et indice culturel, un point par répondant", loc="left", fontsize=11, pad=12)
    legende_gris(ax, int((s["classe"] == "abstention").sum()))
    fig.subplots_adjust(bottom=0.15)
    note_source(fig, SRC17)
    fig.savefig(OUT / "r3_gauche_droite_culture_2017.png"); plt.close(fig)
    return int(m.sum()), bary


def fig_r4(d12, pal, bary, parts):
    m = d12["eco"].notna() & d12["gd"].notna() & d12["classe"].notna()
    s = d12[m]
    x, y = jitter(s["eco"].values, 0.03), jitter(s["gd"].values, 0.40)
    fig, ax = plt.subplots(figsize=(7.6, 7.4))
    nuage(ax, x, y, s["classe"], pal)
    points_barycentres(ax, bary, pal, offsets={"Hollande": (-0.10, 0.18), "Sarkozy": (0.10, 0.18), "Le Pen": (0.10, -0.22),
                                               "Mélenchon": (-0.10, -0.22), "Bayrou": (0.10, 0.18), "Joly": (-0.10, 0.18)})
    ax.axvline(0, color=GRID, lw=0.6, zorder=0)
    ax.set_xlim(-3.1, 3.1); ax.set_ylim(-0.8, 10.8); ax.set_yticks(range(11))
    ax.set_xlabel("Indice économique : 6 items dépenses sociales et redistribution (écarts-types)\n←  interventionnisme                                        libéralisme  →", labelpad=8)
    ax.set_ylabel("Auto-positionnement sur l'échelle gauche (0) – droite (10)", labelpad=8)
    ax.set_title("France 2012 : position économique et gauche-droite déclaré, un point par répondant", loc="left", fontsize=11, pad=12)
    legende_gris(ax, int((s["classe"] == "abstention").sum()), loc="lower right")
    fig.subplots_adjust(bottom=0.17)
    note_source(fig, SRC12)
    fig.savefig(OUT / "r4_nuage_2012.png"); plt.close(fig)
    return int(m.sum())


CAND17_ORDER = ["Macron", "Le Pen", "Fillon", "Mélenchon", "Hamon", "Dupont-Aignan"]
CAND12_ORDER = ["Hollande", "Sarkozy", "Le Pen", "Mélenchon", "Bayrou", "Joly"]


def main():
    d17, d12 = charger_2017(), charger_2012()
    pal17 = {nom: col for nom, col in CAND17.values()}
    pal12 = {nom: col for nom, col in CAND12.values()}

    parts17, parts12 = parts_exprimes(d17, CAND17_ORDER), parts_exprimes(d12, CAND12_ORDER)
    bary17 = barycentres(d17[d17["eco"].notna() & d17["cult"].notna()], "eco", "cult", CAND17_ORDER)
    bary12 = barycentres(d12[d12["eco"].notna() & d12["gd"].notna()], "eco", "gd", CAND12_ORDER)

    n1 = fig_r1(d17, pal17, bary17)
    fig_r2(d17, pal17, bary17, parts17)
    n3, bary17_gd = fig_r3(d17, pal17)
    n4 = fig_r4(d12, pal12, bary12, parts12)

    def corr(df, a, b):
        m = df[a].notna() & df[b].notna()
        return float(np.corrcoef(df.loc[m, a], df.loc[m, b])[0, 1])

    res = {
        "2017": {
            "N_enquete": int(len(d17)), "N_fig_r1": n1, "N_fig_r3": n3,
            "effectifs_classes": d17["classe"].value_counts(dropna=False).rename(index=str).to_dict(),
            "parts_exprimes_ponderees": parts17,
            "corr_eco_culture": corr(d17, "eco", "cult"), "corr_gd_culture": corr(d17, "gd", "cult"), "corr_gd_eco": corr(d17, "gd", "eco"),
            "R2_vote_sur_eco": r2_vote(d17, "eco", CAND17_ORDER), "R2_vote_sur_culture": r2_vote(d17, "cult", CAND17_ORDER),
            "R2_vote_sur_gd": r2_vote(d17, "gd", CAND17_ORDER),
            "barycentres_eco_culture": bary17, "barycentres_gd_culture": bary17_gd,
            "part_culture_positive_ponderee": float(np.average((d17["cult"] > 0)[d17["cult"].notna()], weights=d17.loc[d17["cult"].notna(), "w"])),
            "distribution_eco_ponderee": {str(int(k)): float(v) for k, v in
                                          (d17[d17["eco"].notna()].groupby("eco")["w"].sum() / d17.loc[d17["eco"].notna(), "w"].sum()).items()},
        },
        "2012": {
            "N_enquete": int(len(d12)), "N_fig_r4": n4,
            "effectifs_classes": d12["classe"].value_counts(dropna=False).rename(index=str).to_dict(),
            "parts_exprimes_ponderees": parts12,
            "corr_eco_gd": corr(d12, "eco", "gd"),
            "R2_vote_sur_eco": r2_vote(d12, "eco", CAND12_ORDER), "R2_vote_sur_gd": r2_vote(d12, "gd", CAND12_ORDER),
            "barycentres_eco_gd": bary12,
        },
    }
    (HERE / "resultats_cses.json").write_text(json.dumps(res, indent=2, ensure_ascii=False))
    print(json.dumps(res, indent=1, ensure_ascii=False))


if __name__ == "__main__":
    main()
