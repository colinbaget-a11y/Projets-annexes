"""
Reproduction des calculs et des figures du bulletin « Efficience des dépenses publiques en zone euro »
(C26-096) à partir de la base base_efficience.csv.

    python bulletin.py            scores, classements, frontières, sensibilité, figures/*.png

Chaîne de calcul (annexe méthodologique du bulletin)
  1. Valeurs : PISA 2022 ; TIMSS, dernière valeur entre 2019 et 2023 ; autres indicateurs, dernière
     valeur disponible entre 2019 et 2024 (à défaut, la dernière valeur antérieure).
  2. Normalisation min-max sur l'échantillon, polarité inversée si « plus est moins bien ».
  3. Score d'objectif : moyenne des indicateurs disponibles (pas d'imputation). En santé, objectif 2,
     les six équipements d'imagerie forment un bloc qui vaut un tiers de l'objectif.
  4. Score global : moyenne des quatre objectifs (25 % chacun).
  5. Référence UE : moyenne des valeurs normalisées pondérée par les élèves (primaire et premier cycle
     du secondaire) ou la population, indicateur par indicateur ; contribution d'un indicateur = poids
     × (valeur du pays − référence) ; indicateur manquant : contribution nulle.
  6. Frontière : pays non dominés (aucun autre ne fait mieux en dépensant moins), reliés par une
     interpolation monotone (PCHIP), plate au-delà du dernier ; ratio = score / frontière.
  7. Sensibilité : 20 000 tirages de poids Dirichlet(1,1,1,1), sans poids supérieur à 50 %.

Dépenses : éducation, dépense publique par élève CITE 1-2 (UOE), moyenne 2022-2024 (2022-2023
publiées ; à défaut, dernière valeur disponible, comme la Croatie en 2021) ; santé, dépense courante par habitant en euros, 2022 (Eurostat). La note utilise pour la
santé une série qui n'a pas été identifiée (voir README) : les ratios d'efficience en santé diffèrent.
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.interpolate import PchipInterpolator

ICI = Path(__file__).resolve().parent
sys.path.insert(0, str(ICI))
import base_efficience as be  # noqa: E402

FIG = ICI / "figures"
FIG.mkdir(exist_ok=True)
B = pd.read_csv(ICI / "base_efficience.csv")
W = B.pivot_table(index=["indicateur", "annee"], columns="pays", values="valeur")
NOMS = {"AT": "Autriche", "BE": "Belgique", "BG": "Bulgarie", "HR": "Croatie", "CY": "Chypre",
        "CZ": "Tchéquie", "DK": "Danemark", "EE": "Estonie", "FI": "Finlande", "FR": "France",
        "DE": "Allemagne", "EL": "Grèce", "HU": "Hongrie", "IE": "Irlande", "IT": "Italie",
        "LV": "Lettonie", "LT": "Lituanie", "LU": "Luxembourg", "MT": "Malte", "NL": "Pays-Bas",
        "PL": "Pologne", "PT": "Portugal", "RO": "Roumanie", "SK": "Slovaquie", "SI": "Slovénie",
        "ES": "Espagne", "SE": "Suède"}
VEDETTES = {"FR": "#1f9bd1", "DE": "#d62728", "IT": "#2ca02c", "ES": "#e0a106", "NL": "#ef7d1a"}
IMAGERIE = ["sante_scanners", "sante_irm", "sante_tep", "sante_gamma", "sante_mammographes",
            "sante_radiotherapie"]


def serie(ind):
    return W.loc[ind] if ind in W.index.get_level_values(0) else pd.DataFrame()


def valeur(ind, pays):
    s = serie(ind)
    if ind.startswith("pisa_"):
        return s.loc[2022].reindex(pays)
    if ind.startswith("timss"):
        return s.reindex([2019, 2023]).ffill().iloc[-1].reindex(pays)
    v = s.loc[:2024].ffill().iloc[-1]                 # dernière valeur disponible jusqu'en 2024
    return v.reindex(pays)


def calcul(domaine, pays, poids, poids_objectifs=None):
    inds = [d for d in be.DICO if d[1] == domaine]
    norm = {}
    for ident, _, _, _, pol, _, _ in inds:
        x = valeur(ident, pays)
        n = (x - x.min()) / (x.max() - x.min())
        norm[ident] = 1 - n if pol == "-" else n
    N = pd.DataFrame(norm)
    ref = pd.Series({c: np.average(N[c].dropna(), weights=poids[N[c].dropna().index]) for c in N})
    objectifs = sorted({d[2] for d in inds})
    scores, contrib = {}, {}
    for o in objectifs:
        ids = [d[0] for d in inds if d[2] == o]
        # poids de chaque indicateur dans l'objectif, pays par pays (indicateurs disponibles seulement)
        if domaine == "sante" and o == "S2":
            blocs = {"t": ["sante_mort_traitable"], "i": ["sante_ima30"], "img": IMAGERIE}
        else:
            blocs = {i: [i] for i in ids}
        dispo_bloc = pd.DataFrame({k: N[v].notna().any(axis=1) for k, v in blocs.items()})
        nb_blocs = dispo_bloc.sum(axis=1)
        w = pd.DataFrame(0.0, index=N.index, columns=ids)
        for k, v in blocs.items():
            nb_dans_bloc = N[v].notna().sum(axis=1).replace(0, np.nan)
            for i in v:
                w[i] = (N[i].notna() / nb_dans_bloc / nb_blocs).fillna(0)
        scores[o] = (w * N[ids].fillna(0)).sum(axis=1)
        contrib[o] = (w * (N[ids] - ref[ids]).fillna(0)).sum(axis=1)
    O, C = pd.DataFrame(scores), pd.DataFrame(contrib)
    po = pd.Series(poids_objectifs if poids_objectifs is not None else [0.25] * 4, index=objectifs)
    return N, O, (O * po).sum(axis=1), (C * po).sum(axis=1), C * po


def frontiere(dep, score):
    d = pd.DataFrame({"x": dep, "y": score}).dropna().sort_values("x")
    pts, best = [], -np.inf
    for p, r in d.iterrows():
        if r.y > best:
            pts.append((r.x, r.y))
            best = r.y
    xs, ys = map(np.array, zip(*pts))
    f = PchipInterpolator(xs, ys) if len(xs) > 1 else None

    def front(x):
        x = np.asarray(x, float)
        return np.where(x <= xs[0], ys[0], np.where(x >= xs[-1], ys[-1], f(np.clip(x, xs[0], xs[-1]))))

    def inverse(y):                                   # dépense minimale qui atteint le score y
        grille = np.linspace(xs[0], xs[-1], 20001)
        ok = grille[front(grille) >= y]
        return ok[0] if len(ok) else np.nan
    return front, inverse, xs


def sensibilite(O, n=20000, seed=1):
    rng = np.random.default_rng(seed)
    tirages = []
    while len(tirages) < n:
        w = rng.dirichlet([1, 1, 1, 1], size=n)
        tirages.extend(w[w.max(axis=1) <= 0.5])
    w = np.array(tirages[:n])
    S = O.values @ w.T                                # pays × tirages
    rangs = (-S).argsort(axis=0).argsort(axis=0) + 1
    return pd.DataFrame(S, index=O.index), pd.DataFrame(rangs, index=O.index)


# ================================================================ calculs
PE, PS = be.ECHANTILLON_EDU, be.ECHANTILLON_SANTE
eleves = (W.loc[("edu_eleves_cite1", 2022)] + W.loc[("edu_eleves_cite2", 2022)])
pop = W.loc[("pop_totale", 2022)]
_d = serie("edu_dep_eleve_cite1_2_pub_eur")
dep_edu = _d.loc[2022:2024].mean().fillna(_d.ffill().iloc[-1]).reindex(PE)   # à défaut : dernière valeur
dep_san = serie("sante_dep_hab_eur").loc[2022].reindex(PS)

res = {}
for dom, pays, poids, dep in (("education", PE, eleves.reindex(PE), dep_edu),
                              ("sante", PS, pop.reindex(PS), dep_san)):
    N, O, g, ecart, C = calcul(dom, pays, poids)
    front, inverse, xs = frontiere(dep, g)
    S, R = sensibilite(O)
    res[dom] = dict(N=N, O=O, g=g, ecart=ecart, C=C, dep=dep, front=front, inverse=inverse, S=S, R=R,
                    poids=poids)

tab = []
for dom, r in res.items():
    rang = r["g"].rank(ascending=False).astype(int)
    for p in r["g"].index:
        tab.append({"domaine": dom, "pays": p, "score": r["g"][p], "rang": rang[p],
                    "ecart_ue_points": 100 * r["ecart"][p],
                    **{f"contrib_{o}": 100 * r["C"].loc[p, o] for o in r["C"].columns},
                    "depense": r["dep"][p], "ratio_efficience": r["g"][p] / float(r["front"](r["dep"][p])),
                    "rang_median_sensib": np.median(r["R"].loc[p]),
                    "rang_p5": np.percentile(r["R"].loc[p], 5), "rang_p95": np.percentile(r["R"].loc[p], 95)})
TAB = pd.DataFrame(tab)
TAB.to_csv(ICI / "resultats_bulletin.csv", index=False)

if __name__ == "__main__":
    pd.set_option("display.width", 160)
    for dom in res:
        t = TAB[TAB.domaine == dom].set_index("pays").sort_values("rang")
        print(f"\n{dom} :")
        print(t[["score", "rang", "ecart_ue_points"] + [c for c in t if c.startswith("contrib")]
                + ["ratio_efficience", "rang_median_sensib", "rang_p5", "rang_p95"]].round(3).to_string())
    e = res["education"]
    fr_dep = e["dep"]["FR"]
    gain = 100 * (float(e["front"](fr_dep)) - e["g"]["FR"])
    eco = (fr_dep - e["inverse"](e["g"]["FR"])) * eleves["FR"] / 1e9
    print(f"\nÉducation, France : gain à dépense constante {gain:.0f} points ; équivalent dépense "
          f"{eco:.0f} Md€ par an")

# ================================================================ figures
import matplotlib  # noqa: E402

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10, "axes.spines.top": False,
                     "axes.spines.right": False, "axes.grid": True, "grid.color": "#EEEEEE",
                     "figure.dpi": 150, "savefig.dpi": 150, "savefig.bbox": "tight"})


def nuage(ax, r, xlabel, taille, titre_ax=None, halo=False):
    g, dep = r["g"], r["dep"]
    t = taille.reindex(g.index)
    s = 1400 * t / t.max()
    xx = np.linspace(dep.min() * 0.92, dep.max() * 1.05, 400)
    if halo:
        for p, c in VEDETTES.items():
            if p in g.index:
                v = ax.violinplot(r["S"].loc[p].values, positions=[dep[p]], widths=dep.max() * 0.05,
                                  showextrema=False)
                for b in v["bodies"]:
                    b.set_facecolor(c)
                    b.set_alpha(0.3)
    for p in g.index:
        vedette = p in VEDETTES
        ax.scatter(dep[p], g[p], s=(s[p] if not halo else (90 if vedette else 30)),
                   color=VEDETTES.get(p, "#b8bec4"), edgecolor="#222222" if vedette else "#8a9096",
                   lw=1 if vedette else 0.6, alpha=0.95 if vedette else 0.9, zorder=3)
        taille_pt = (s[p] if not halo else (90 if vedette else 30)) ** 0.5 / 2
        ax.annotate(NOMS[p], (dep[p], g[p]), xytext=(0, taille_pt + 3), textcoords="offset points",
                    ha="center", fontsize=10 if vedette else 8, color=VEDETTES.get(p, "#555555"),
                    fontweight="bold" if vedette else "normal", zorder=4)
    xs0 = xx[xx >= dep[g.idxmin()] * 0 + xx.min()]
    ax.plot(xs0, r["front"](xs0), ls="--", color="#1f4e79" if not halo else "#888888", lw=1.8,
            label="Frontière d'efficience", zorder=2)
    ax.set_xlabel(xlabel)
    ax.set_ylabel("Score composite (0-1)")
    if titre_ax:
        ax.set_title(titre_ax, loc="left", fontweight="bold", color="#1f4e79")


def decomposition(r, nom, libelles, legende_ref):
    C = r["C"] * 100
    ordre = r["g"].sort_values().index
    fig, ax = plt.subplots(figsize=(11, 4.8))
    couleurs = ["#4facde", "#f2b100", "#3aa64c", "#e63946"]
    x = np.arange(len(ordre))
    haut, bas = np.zeros(len(x)), np.zeros(len(x))
    for o, c, lib in zip(C.columns, couleurs, libelles):
        y = C.loc[ordre, o].values
        pos, neg = np.where(y > 0, y, 0), np.where(y < 0, y, 0)
        ax.bar(x, pos, bottom=haut, color=c, width=0.72, label=lib, edgecolor="white", lw=0.5)
        ax.bar(x, neg, bottom=bas, color=c, width=0.72, edgecolor="white", lw=0.5)
        haut += pos
        bas += neg
    ax.scatter(x, 100 * r["ecart"][ordre], color="white", edgecolor="black", zorder=5, s=40,
               label=legende_ref)
    ax.axhline(0, color="black", lw=1)
    ax.set_xticks(x)
    ax.set_xticklabels([NOMS[p] for p in ordre], rotation=45, ha="right")
    for t, p in zip(ax.get_xticklabels(), ordre):
        if p == "FR":
            t.set_color(VEDETTES["FR"])
            t.set_fontweight("bold")
    ax.set_ylabel("Écart au score moyen UE (points)")
    ax.grid(axis="x", visible=False)
    ax.legend(loc="lower center", bbox_to_anchor=(0.5, 1.02), ncol=3, frameon=False, fontsize=9)
    fig.savefig(FIG / nom)
    plt.close(fig)


# figure 1 et figure 3 : nuages
for dom, nom, xl in (("education", "figure1_education.png",
                      "Dépense publique par élève, primaire + 1er cycle secondaire (€, moy. 2022-2024)"),
                     ("sante", "figure3_sante.png", "Dépense de santé par habitant (€, 2022, Eurostat)")):
    fig, ax = plt.subplots(figsize=(10, 6))
    nuage(ax, res[dom], xl, res[dom]["poids"])
    ax.legend(loc="lower right", frameon=False)
    fig.savefig(FIG / nom)
    plt.close(fig)

decomposition(res["education"], "figure2_decomposition_education.png",
              ["Maîtrise des savoirs fondamentaux", "Excellence et dynamisme académique",
               "Équité et climat scolaire", "Insertion dans la vie active"], "Écart total au score moyen UE")
decomposition(res["sante"], "figure4_decomposition_sante.png",
              ["Résultats de santé", "Qualité et efficience des soins", "Accès et protection financière",
               "Prévention et innovation"], "Écart total au score moyen UE")

# encadré : trois parts de la dépense d'éducation, 2024
parts = {"Personnel (rémunérations)": "edu_part_remunerations",
         "Pré-primaire + primaire": "edu_part_preprimaire_primaire", "Services annexes": "edu_part_annexes"}
fig, ax = plt.subplots(figsize=(10, 4.6))
rng = np.random.default_rng(0)
for k, (lib, ind) in enumerate(parts.items()):
    v = serie(ind).loc[:2024].ffill().iloc[-1].reindex(be.UE27).dropna()
    y = 2 - k
    ax.plot([v.min(), v.max()], [y, y], color="#dddddd", lw=3, zorder=1)
    autres = v.drop("FR")
    ax.scatter(autres, y + rng.uniform(-0.12, 0.12, len(autres)), color="#b0b0b0", s=25, zorder=2,
               label="Autres pays de l'UE" if k == 0 else None)
    med = v.median()
    ax.plot([med, med], [y - 0.23, y + 0.23], color="#003399", lw=2.5, zorder=3,
            label="Médiane UE" if k == 0 else None)
    ax.text(med, y - 0.38, f"méd. {med:.0f}", ha="center", color="#003399", fontsize=9)
    ax.scatter(v["FR"], y, s=200, color=VEDETTES["FR"], edgecolor="#0b5a80", lw=1.5, zorder=4,
               label="France" if k == 0 else None)
    ax.text(v["FR"], y + 0.3, f"France {v['FR']:.0f} %", ha="center", color=VEDETTES["FR"],
            fontweight="bold")
    ax.text(-2, y, lib, ha="right", va="center", fontweight="bold", fontsize=11)
ax.set_xlim(0, 80)
ax.set_ylim(-0.6, 2.6)
ax.set_yticks([])
ax.spines["left"].set_visible(False)
ax.grid(axis="y", visible=False)
ax.set_xlabel("Part de la dépense publique d'éducation (%), 2024")
ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.18), ncol=3, frameon=False)
fig.savefig(FIG / "encadre_depense_education.png")
plt.close(fig)

# figure A : sensibilité
fig, axes = plt.subplots(1, 2, figsize=(13, 5.5))
for ax, dom, xl, t in ((axes[0], "education", "Dépense publique par élève (€, moy. 2022-2024)",
                        "Éducation · 24 pays"),
                       (axes[1], "sante", "Dépense de santé par habitant (€, 2022)", "Santé · 24 pays")):
    nuage(ax, res[dom], xl, res[dom]["poids"], titre_ax=t, halo=True)
fig.savefig(FIG / "figureA_sensibilite.png")
plt.close(fig)
print("figures :", ", ".join(sorted(f.name for f in FIG.glob("*.png"))))
