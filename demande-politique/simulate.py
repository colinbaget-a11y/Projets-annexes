"""
Prototype — structure de la demande politique française sur données SIMULÉES.

Tout est fictif. Aucune coordonnée, aucun poids, aucun score ne doit être lu
comme une estimation réelle. L'objet du script est de construire le langage
visuel et les quantités que l'on chercherait ensuite à estimer sur données
réelles.

Organisation :
  1. CONFIG      espace idéologique, dates, clusters d'électeurs, partis
  2. SIMULATION  tirage des électeurs à chaque date (mélange de gaussiennes 2D)
  3. MODÈLE      attraction des partis, probabilités de vote, densité
  4. MÉTRIQUES   potentiels, scores, chevauchements, espace vacant, entrant optimal
  5. FIGURES     neuf graphiques
  6. main
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap, to_rgba
from matplotlib.patches import Ellipse, Rectangle
import matplotlib.patheffects as pe
from scipy.stats import gaussian_kde

# ============================================================================
# 1. CONFIG
# ============================================================================

OUT = Path(__file__).resolve().parent / "figures"
RNG = np.random.default_rng(20250910)

# Espace : E (économie) et C (culture), chacun sur [-3, +3].
#   E < 0 : interventionnisme, redistribution      E > 0 : libéralisme économique
#   C < 0 : progressisme culturel                  C > 0 : conservatisme, autorité
LIM = 3.0
N_VOTERS = 20_000
DATES = [1995, 2000, 2005, 2010, 2015, 2020, 2025]
DATES_CARTE = [1995, 2005, 2015, 2025]

# Clusters d'électeurs. Chaque paramètre est donné en 1995 et en 2025 et
# interpolé linéairement entre les deux. C'est le scénario ILLUSTRATIF :
# contraction du bloc libéral-conservateur, essor du bloc
# national-interventionniste, affaiblissement de la corrélation E/C.
CLUSTERS = {
    "gauche radicale progressiste": dict(
        mu=[(-1.9, -1.2), (-2.0, -1.5)], w=[0.15, 0.17],
        sd=[(0.65, 0.75), (0.65, 0.80)], rho=[0.25, 0.15]),
    "gauche modérée": dict(
        mu=[(-1.0, -0.3), (-0.9, -0.6)], w=[0.23, 0.11],
        sd=[(0.80, 0.85), (0.80, 0.85)], rho=[0.35, 0.05]),
    "centre social-libéral": dict(
        mu=[(0.8, -0.8), (1.0, -1.2)], w=[0.09, 0.17],
        sd=[(0.75, 0.80), (0.75, 0.80)], rho=[0.20, 0.00]),
    "libéral-conservateur": dict(
        mu=[(1.6, 1.0), (1.6, 1.1)], w=[0.30, 0.13],
        sd=[(0.80, 0.75), (0.80, 0.75)], rho=[0.35, 0.05]),
    "national-interventionniste": dict(
        mu=[(0.1, 1.7), (-0.8, 1.8)], w=[0.10, 0.28],
        sd=[(0.85, 0.70), (0.95, 0.70)], rho=[0.10, -0.05]),
    "diffus / peu structuré": dict(
        mu=[(0.0, 0.3), (0.0, 0.2)], w=[0.13, 0.14],
        sd=[(1.30, 1.20), (1.30, 1.20)], rho=[0.15, 0.00]),
}

# Partis (offre 2025, positions ILLUSTRATIVES). Chaque parti = centre mu,
# largeur (sd, rho) de son bassin, valence V (capacité de conversion).
PARTIES = {
    "LFI":         dict(mu=(-2.0, -1.3), sd=(0.75, 0.85), rho=0.10, V=1.00, col="#B4443E"),
    "PS":          dict(mu=(-1.0, -0.9), sd=(0.80, 0.80), rho=0.20, V=0.70, col="#D9679B"),
    "Renaissance": dict(mu=(1.0, -0.5),  sd=(0.90, 0.90), rho=0.00, V=0.95, col="#C48A1C"),
    "LR":          dict(mu=(1.5, 1.0),   sd=(0.80, 0.75), rho=0.20, V=0.65, col="#4E8FD0"),
    "RN":          dict(mu=(-0.4, 1.8),  sd=(1.00, 0.80), rho=-0.10, V=1.20, col="#2A4A9C"),
    "Reconquête":  dict(mu=(0.6, 2.2),   sd=(0.80, 0.70), rho=0.00, V=0.50, col="#8A4FA8"),
}
PARTY_NAMES = list(PARTIES)

# Option extérieure : attraction constante de l'abstention. Un électeur loin de
# tous les partis n'est capté par personne. Indispensable pour que « espace
# vacant » ait un sens.
A_ABST = 0.28

# Familles idéologiques FIXES dans le temps (rectangles de l'espace).
FAMILLES = {
    "gauche interventionniste progressiste":  dict(E=(-3.0, -0.6), C=(-3.0, -0.2), court="gauche interv.\nprogressiste"),
    "social-libéral progressiste":            dict(E=(0.4, 3.0),  C=(-3.0, -0.2), court="social-libéral\nprogressiste"),
    "libéral-conservateur":                   dict(E=(0.6, 3.0),  C=(0.4, 3.0),  court="libéral-\nconservateur"),
    "national-conservateur interventionniste": dict(E=(-3.0, 0.2), C=(0.8, 3.0), court="national-\nconservateur\ninterventionniste"),
}

# Nouvel entrant hypothétique (largeur et valence moyennes)
ENTRANT = dict(sd=(0.8, 0.8), rho=0.0, V=0.8)

# Style
INK, INK2, MUTED, GRID, SURFACE = "#1F2328", "#4B5158", "#8A9099", "#E6E8EA", "#FCFCFB"
DENS_CMAP = LinearSegmentedColormap.from_list("dens", [SURFACE, "#D9DCE1", "#9AA0AA", "#5A6270", "#2E333B"])
TEAL_CMAP = LinearSegmentedColormap.from_list("teal", [SURFACE, "#CFE6E2", "#8CC7BE", "#3E9C8F", "#1B6E64"])

plt.rcParams.update({
    "font.family": "Liberation Sans",
    "font.size": 10,
    "axes.edgecolor": MUTED, "axes.linewidth": 0.6,
    "axes.labelcolor": INK2, "axes.titlecolor": INK,
    "xtick.color": INK2, "ytick.color": INK2,
    "xtick.labelsize": 9, "ytick.labelsize": 9,
    "axes.spines.top": False, "axes.spines.right": False,
    "figure.facecolor": SURFACE, "axes.facecolor": SURFACE, "savefig.facecolor": SURFACE,
    "figure.dpi": 200, "savefig.dpi": 200, "savefig.bbox": "tight", "savefig.pad_inches": 0.25,
})

# ============================================================================
# 2. SIMULATION
# ============================================================================

def lerp(a, b, t):
    return np.asarray(a) + (np.asarray(b) - np.asarray(a)) * t


def cov_matrix(sd, rho):
    sx, sy = sd
    return np.array([[sx * sx, rho * sx * sy], [rho * sx * sy, sy * sy]])


def cluster_params(year):
    """Paramètres de chaque cluster à une date, par interpolation 1995→2025."""
    t = (year - DATES[0]) / (DATES[-1] - DATES[0])
    out = {}
    for name, c in CLUSTERS.items():
        out[name] = dict(
            mu=lerp(c["mu"][0], c["mu"][1], t),
            w=float(lerp(c["w"][0], c["w"][1], t)),
            cov=cov_matrix(lerp(c["sd"][0], c["sd"][1], t), float(lerp(c["rho"][0], c["rho"][1], t))),
        )
    w = np.array([v["w"] for v in out.values()])
    for v in out.values():
        v["w"] /= w.sum()
    return out


def simulate_voters(year, n=N_VOTERS):
    """Électeurs (E_i, C_i) tirés d'un mélange de gaussiennes 2D, bornés à ±3."""
    params = cluster_params(year)
    names = list(params)
    counts = RNG.multinomial(n, [params[k]["w"] for k in names])
    pts = []
    for k, m in zip(names, counts):
        pts.append(RNG.multivariate_normal(params[k]["mu"], params[k]["cov"], size=m))
    Z = np.vstack(pts)
    RNG.shuffle(Z)
    return np.clip(Z, -LIM, LIM)


# ============================================================================
# 3. MODÈLE
# ============================================================================

def mahalanobis2(Z, mu, cov):
    d = Z - np.asarray(mu)
    inv = np.linalg.inv(cov)
    return np.einsum("ij,jk,ik->i", d, inv, d)


def attraction(Z, party):
    """A_p(z) = V_p · exp(-½ (z-μ)' Σ⁻¹ (z-μ)). Sans V : noyau idéologique pur."""
    cov = cov_matrix(party["sd"], party["rho"])
    return party["V"] * np.exp(-0.5 * mahalanobis2(Z, party["mu"], cov))


def kernel(Z, party):
    cov = cov_matrix(party["sd"], party["rho"])
    return np.exp(-0.5 * mahalanobis2(Z, party["mu"], cov))


def attractions(Z, parties=PARTIES):
    return np.column_stack([attraction(Z, p) for p in parties.values()])


def choice_probs(A, a_abst=A_ABST):
    """P(p|z) = A_p / (A_0 + Σ_q A_q). Dernière colonne : abstention.
    C'est un logit multinomial où l'utilité vaut ln V_p − ½ d_p(z)²."""
    denom = a_abst + A.sum(axis=1, keepdims=True)
    P = A / denom
    return np.column_stack([P, a_abst / denom[:, 0]])


def grid(n=141):
    e = np.linspace(-LIM, LIM, n)
    E, C = np.meshgrid(e, e)
    return E, C, np.column_stack([E.ravel(), C.ravel()])


def density_on_grid(Z, Zg, shape):
    kde = gaussian_kde(Z.T, bw_method=0.18)
    return kde(Zg.T).reshape(shape)


# ============================================================================
# 4. MÉTRIQUES
# ============================================================================

def famille_masses(Z):
    """Part des électeurs dans chaque rectangle fixe."""
    out = {}
    for name, f in FAMILLES.items():
        m = (Z[:, 0] >= f["E"][0]) & (Z[:, 0] <= f["E"][1]) & (Z[:, 1] >= f["C"][0]) & (Z[:, 1] <= f["C"][1])
        out[name] = float(m.mean())
    return out


def party_metrics(Z):
    """Pour chaque parti, en % de l'électorat simulé :
       score       part qui vote p en présence de tous les concurrents
       coeur       part située à moins d'un écart-type (d ≤ 1) du centre
       accessible  part qui voterait p s'il était seul face à l'abstention,
                   à valence de référence V = 1 (mesure la position et la largeur, pas la popularité)
       destination répartition du marché accessible de p selon le vote effectif"""
    A = attractions(Z)
    P = choice_probs(A)
    abst = P[:, -1].mean()
    res = {}
    for j, (name, p) in enumerate(PARTIES.items()):
        cov = cov_matrix(p["sd"], p["rho"])
        d2 = mahalanobis2(Z, p["mu"], cov)
        k_ref = A[:, j] / p["V"]                      # noyau à valence de référence V = 1
        alone = k_ref / (A_ABST + k_ref)
        dest = (alone[:, None] * P).sum(axis=0) / alone.sum()
        res[name] = dict(
            score=float(P[:, j].mean()),
            score_exprimes=float(P[:, j].mean() / (1 - abst)),
            coeur=float((d2 <= 1.0).mean()),
            accessible=float(alone.mean()),
            destination={q: float(dest[k]) for k, q in enumerate(PARTY_NAMES + ["abstention"])},
        )
    return res, float(abst)


def overlap_matrix(Z):
    """O[p,q] = Σ min(k_p, k_q) / Σ k_p : part du marché idéologique de p
    (noyau sans valence, pondéré par la densité réelle) que q peut aussi atteindre."""
    K = np.column_stack([kernel(Z, p) for p in PARTIES.values()])
    n = K.shape[1]
    O = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            O[i, j] = np.minimum(K[:, i], K[:, j]).sum() / K[:, i].sum()
    return O


def territories(Zg):
    """Sur la grille : parti dominant, et marge entre les deux premiers."""
    A = attractions(Zg)
    Pi = A / A.sum(axis=1, keepdims=True)          # conditionnel au vote
    order = np.argsort(-Pi, axis=1)
    top = order[:, 0]
    marge = Pi[np.arange(len(Pi)), order[:, 0]] - Pi[np.arange(len(Pi)), order[:, 1]]
    return top, marge


def vacancy(Zg, D):
    """U(z) = D(z) · [1 − max_p P(p|z)], avec l'option extérieure."""
    P = choice_probs(attractions(Zg))[:, :-1]
    return D * (1 - P.max(axis=1))


def entrant_share(Z, positions, A_existing):
    """Part de l'électorat qu'obtiendrait un nouvel entrant à chaque position."""
    cov = cov_matrix(ENTRANT["sd"], ENTRANT["rho"])
    inv = np.linalg.inv(cov)
    base = A_ABST + A_existing.sum(axis=1)
    out = np.empty(len(positions))
    for k in range(0, len(positions), 64):
        pos = positions[k:k + 64]
        d = Z[None, :, :] - pos[:, None, :]
        d2 = np.einsum("pij,jk,pik->pi", d, inv, d)
        An = ENTRANT["V"] * np.exp(-0.5 * d2)
        out[k:k + 64] = (An / (base[None, :] + An)).mean(axis=1)
    return out


def moments(Z):
    return dict(mE=float(Z[:, 0].mean()), mC=float(Z[:, 1].mean()),
                sdE=float(Z[:, 0].std()), sdC=float(Z[:, 1].std()),
                corr=float(np.corrcoef(Z[:, 0], Z[:, 1])[0, 1]))


# ============================================================================
# 5. FIGURES
# ============================================================================

def axes_ideo(ax, labels=True):
    ax.set_xlim(-LIM, LIM); ax.set_ylim(-LIM, LIM)
    ax.set_xticks([-3, -2, -1, 0, 1, 2, 3]); ax.set_yticks([-3, -2, -1, 0, 1, 2, 3])
    ax.axhline(0, color=GRID, lw=0.6, zorder=0); ax.axvline(0, color=GRID, lw=0.6, zorder=0)
    ax.set_aspect("equal")
    if labels:
        ax.set_xlabel("Économie   ←  interventionnisme          libéralisme  →", labelpad=6)
        ax.set_ylabel("Culture   ←  progressisme          conservatisme  →", labelpad=6)


def draw_density(ax, E, C, D, cmap=DENS_CMAP, levels=9, alpha=1.0):
    lv = np.linspace(D.min(), D.max(), levels + 1)[1:]
    cf = ax.contourf(E, C, D, levels=np.concatenate([[D.min()], lv]), cmap=cmap, alpha=alpha, antialiased=True)
    ax.contour(E, C, D, levels=lv, colors=[INK2], linewidths=0.25, alpha=0.35)
    return cf


def party_ellipse(p, k):
    cov = cov_matrix(p["sd"], p["rho"])
    vals, vecs = np.linalg.eigh(cov)
    ang = np.degrees(np.arctan2(vecs[1, 1], vecs[0, 1]))
    return Ellipse(p["mu"], 2 * k * np.sqrt(vals[1]), 2 * k * np.sqrt(vals[0]), angle=ang)


def draw_parties(ax, ellipses=True, label=True, size=42, offsets=None):
    offsets = offsets or {}
    for name, p in PARTIES.items():
        if ellipses:
            e1 = party_ellipse(p, 1.0); e1.set(fill=False, ec=p["col"], lw=1.2, zorder=4)
            ax.add_patch(e1)
        ax.scatter(*p["mu"], s=size, color=p["col"], ec=SURFACE, lw=1.2, zorder=6)
        if label:
            dx, dy = offsets.get(name, (0.13, 0.13))
            ax.annotate(name, p["mu"], xytext=(p["mu"][0] + dx, p["mu"][1] + dy), fontsize=9.5,
                        fontweight="bold", color=p["col"], zorder=7,
                        path_effects=[pe.withStroke(linewidth=2.6, foreground=SURFACE)])


def fig1_carte(Z, E, C, D):
    fig, ax = plt.subplots(figsize=(7.6, 7.2))
    draw_density(ax, E, C, D)
    draw_parties(ax, offsets={"Reconquête": (0.15, 0.2), "RN": (-0.9, -0.05), "LR": (0.18, -0.38), "PS": (0.14, 0.14)})
    axes_ideo(ax)
    ax.set_title("Carte idéologique simulée, « 2025 » : densité d'électeurs et bassins des partis",
                 loc="left", fontsize=11.5, pad=12)
    ax.text(-2.95, 2.78, "gris : densité d'électeurs (KDE)\nellipse : bassin du parti à 1 σ", fontsize=8, color=INK2, va="top",
            bbox=dict(boxstyle="round,pad=0.3", fc=SURFACE, ec="none", alpha=0.85))
    fig.text(0.99, 0.005, "données entièrement simulées", fontsize=7.5, color=MUTED, ha="right")
    fig.savefig(OUT / "fig1_carte_2025.png"); plt.close(fig)


def fig2_dates(samples, E, C):
    fig, axes = plt.subplots(2, 2, figsize=(9.2, 9.0), sharex=True, sharey=True)
    Ds = {y: density_on_grid(samples[y], np.column_stack([E.ravel(), C.ravel()]), E.shape) for y in DATES_CARTE}
    vmax = max(d.max() for d in Ds.values())
    lv = np.linspace(0, vmax, 10)[1:]
    for ax, y in zip(axes.ravel(), DATES_CARTE):
        ax.contourf(E, C, Ds[y], levels=np.concatenate([[0], lv]), cmap=DENS_CMAP, antialiased=True)
        ax.contour(E, C, Ds[y], levels=lv, colors=[INK2], linewidths=0.25, alpha=0.35)
        axes_ideo(ax, labels=False)
        m = moments(samples[y])
        ax.set_title(f"{y}", loc="left", fontsize=12, fontweight="bold", pad=6)
        ax.text(2.9, 2.75, f"corr(E, C) = {m['corr']:+.2f}", fontsize=8.5, color=INK2, ha="right")
    for ax in axes[1]:
        ax.set_xlabel("Économie   ←  interv.        libéral.  →")
    for ax in axes[:, 0]:
        ax.set_ylabel("Culture   ←  progr.        conserv.  →")
    fig.suptitle("Déformation simulée de la distribution des électeurs, 1995 → 2025 (même échelle de densité)",
                 x=0.06, ha="left", fontsize=11.5, y=0.985)
    fig.text(0.94, 0.012, "données entièrement simulées", fontsize=7.5, color=MUTED, ha="right")
    fig.tight_layout(rect=(0, 0.02, 1, 0.97))
    fig.savefig(OUT / "fig2_cartes_4_dates.png"); plt.close(fig)


FAM_COLS = ["#B4443E", "#C48A1C", "#4E8FD0", "#2A4A9C"]


def fig3_familles(samples, E, C, D2025):
    masses = {y: famille_masses(samples[y]) for y in DATES}
    fig, (ax0, ax1) = plt.subplots(1, 2, figsize=(12.5, 5.6), gridspec_kw=dict(width_ratios=[1, 1.1]))
    ax0.contourf(E, C, D2025, levels=8, cmap=DENS_CMAP, alpha=0.55, antialiased=True)
    axes_ideo(ax0)
    for (name, f), col in zip(FAMILLES.items(), FAM_COLS):
        r = Rectangle((f["E"][0], f["C"][0]), f["E"][1] - f["E"][0], f["C"][1] - f["C"][0],
                      fill=False, ec=col, lw=1.5, zorder=5)
        ax0.add_patch(r)
        # libellé dans le coin du rectangle le plus éloigné du centre de la carte
        x = f["E"][0] + 0.12 if f["E"][0] < 0 else f["E"][1] - 0.12
        y = f["C"][1] - 0.12 if f["C"][1] > 0 else f["C"][0] + 0.12
        ax0.text(x, y, f["court"], ha="left" if f["E"][0] < 0 else "right", va="top" if f["C"][1] > 0 else "bottom",
                 fontsize=7.8, color=col, fontweight="bold", zorder=6, linespacing=1.1,
                 path_effects=[pe.withStroke(linewidth=2.4, foreground=SURFACE)])
    ax0.set_title("Quatre zones FIXES (fond : densité 2025)", loc="left", fontsize=10.5, pad=10)
    for (name, _), col in zip(FAMILLES.items(), FAM_COLS):
        ys = [100 * masses[y][name] for y in DATES]
        ax1.plot(DATES, ys, color=col, lw=2, marker="o", ms=4.5, mec=SURFACE, mew=1)
    # étiquettes de fin de ligne, écartées si nécessaire
    lab = sorted([(100 * masses[DATES[-1]][n], n, c) for (n, _), c in zip(FAMILLES.items(), FAM_COLS)])
    ypos = [v for v, _, _ in lab]
    for i in range(1, len(ypos)):
        if ypos[i] - ypos[i - 1] < 2.2: ypos[i] = ypos[i - 1] + 2.2
    for (v, n, c), yp in zip(lab, ypos):
        ax1.annotate(f"{v:.0f} %  {n}", (DATES[-1], v), xytext=(8, (yp - v) * 9), textcoords="offset points",
                     va="center", fontsize=8.5, color=c, fontweight="bold")
    ax1.set_xlim(1993, 2027); ax1.set_xticks(DATES)
    ax1.set_ylim(0, 40); ax1.set_ylabel("part des électeurs dans la zone (%)")
    ax1.yaxis.grid(True, color=GRID, lw=0.6); ax1.set_axisbelow(True)
    ax1.set_title("Potentiel de chaque famille : masse d'électeurs dans sa zone", loc="left", fontsize=10.5)
    fig.suptitle("Évolution simulée du potentiel électoral de quatre familles idéologiques, 1995-2025",
                 x=0.04, ha="left", fontsize=11.5)
    fig.text(0.98, 0.01, "données entièrement simulées", fontsize=7.5, color=MUTED, ha="right")
    fig.tight_layout(rect=(0, 0.02, 0.84, 0.95))
    fig.savefig(OUT / "fig3_potentiel_familles.png"); plt.close(fig)
    return masses


def fig4_potentiel_vs_score(metrics):
    order = sorted(PARTY_NAMES, key=lambda n: metrics[n]["accessible"], reverse=True)
    fig, (ax0, ax1) = plt.subplots(1, 2, figsize=(12, 5.0), gridspec_kw=dict(width_ratios=[1.05, 1]))
    # -- gauche : score / cœur / accessible
    for i, name in enumerate(order):
        m = metrics[name]; col = PARTIES[name]["col"]; y = len(order) - i
        ax0.plot([100 * m["score"], 100 * m["accessible"]], [y, y], color=col, lw=2.2, alpha=0.35, zorder=1)
        ax0.scatter(100 * m["accessible"], y, s=52, marker="s", color=SURFACE, ec=col, lw=1.6, zorder=3)
        ax0.scatter(100 * m["coeur"], y, s=44, marker="D", color=SURFACE, ec=col, lw=1.4, zorder=3)
        ax0.scatter(100 * m["score"], y, s=70, color=col, ec=SURFACE, lw=1.2, zorder=4)
        ax0.text(-1.2, y, name, ha="right", va="center", fontsize=9.5, color=INK, fontweight="bold")
        ax0.text(100 * m["accessible"] + 0.9, y, f"{100*m['accessible']:.0f}", va="center", fontsize=8, color=INK2)
        ax0.text(100 * m["score"], y + 0.32, f"{100*m['score']:.0f}", ha="center", fontsize=8, color=INK2)
    ax0.set_yticks([]); ax0.set_ylim(0.3, len(order) + 0.9)
    ax0.set_xlim(0, 40); ax0.set_xlabel("% de l'électorat simulé")
    ax0.xaxis.grid(True, color=GRID, lw=0.6); ax0.set_axisbelow(True)
    ax0.spines["left"].set_visible(False)
    from matplotlib.lines import Line2D
    handles = [Line2D([], [], marker="o", ls="", ms=8, color=INK2, mec=SURFACE, label="score capté (avec concurrents)"),
               Line2D([], [], marker="D", ls="", ms=7, color=SURFACE, mec=INK2, mew=1.4, label="cœur : électeurs à moins d'1 σ du centre"),
               Line2D([], [], marker="s", ls="", ms=7.5, color=SURFACE, mec=INK2, mew=1.6, label="accessible : s'il était seul, à valence de référence")]
    ax0.legend(handles=handles, loc="lower right", fontsize=8, frameon=False, handletextpad=0.4, borderaxespad=0.2)
    ax0.set_title("Trois tailles pour chaque parti", loc="left", fontsize=10.5)
    # -- droite : où va le marché accessible de chaque parti
    dest_names = PARTY_NAMES + ["abstention"]
    for i, name in enumerate(order):
        y = len(order) - i; left = 0
        for q in dest_names:
            v = 100 * metrics[name]["destination"][q]
            col = PARTIES[q]["col"] if q in PARTIES else "#C9CCD1"
            ax1.barh(y, v, left=left, height=0.62, color=col, ec=SURFACE, lw=1.2, alpha=1.0 if q == name else 0.55)
            if v >= 7:
                ax1.text(left + v / 2, y, f"{v:.0f}", ha="center", va="center", fontsize=7.8,
                         color=SURFACE if q == name else INK, fontweight="bold" if q == name else "normal")
            left += v
        ax1.text(-1.5, y, name, ha="right", va="center", fontsize=9.5, color=INK, fontweight="bold")
    ax1.set_yticks([]); ax1.set_ylim(0.3, len(order) + 0.9); ax1.set_xlim(0, 100)
    ax1.set_xlabel("% du marché accessible du parti (ligne)")
    ax1.spines["left"].set_visible(False)
    ax1.set_title("Où va le marché accessible de chaque parti ?\n(segment plein : capté par lui-même ; autres : par les concurrents ; gris : abstention)",
                  loc="left", fontsize=10.5)
    fig.suptitle("Potentiel idéologique et vote effectivement capté (simulation « 2025 »)",
                 x=0.04, ha="left", fontsize=11.5)
    fig.text(0.98, 0.01, "données entièrement simulées", fontsize=7.5, color=MUTED, ha="right")
    fig.tight_layout(rect=(0, 0.02, 1, 0.94))
    fig.savefig(OUT / "fig4_potentiel_vs_score.png"); plt.close(fig)


def fig5_chevauchement(O):
    n = len(PARTY_NAMES)
    fig, ax = plt.subplots(figsize=(7.4, 6.4))
    im = ax.imshow(O, cmap=TEAL_CMAP, vmin=0, vmax=1)
    for i in range(n):
        for j in range(n):
            v = O[i, j]
            ax.text(j, i, f"{100*v:.0f}", ha="center", va="center", fontsize=9.5,
                    color=SURFACE if v > 0.55 else INK, fontweight="bold" if (i != j and v >= 0.4) else "normal")
    ax.set_xticks(range(n)); ax.set_xticklabels(PARTY_NAMES, rotation=30, ha="right")
    ax.set_yticks(range(n)); ax.set_yticklabels(PARTY_NAMES)
    for t, name in zip(ax.get_xticklabels(), PARTY_NAMES): t.set_color(PARTIES[name]["col"]); t.set_fontweight("bold")
    for t, name in zip(ax.get_yticklabels(), PARTY_NAMES): t.set_color(PARTIES[name]["col"]); t.set_fontweight("bold")
    ax.set_xlabel("… est aussi atteignable par ce parti", labelpad=8)
    ax.set_ylabel("Part du marché idéologique de ce parti …", labelpad=8)
    ax.spines["left"].set_visible(False); ax.spines["bottom"].set_visible(False)
    ax.tick_params(length=0)
    cb = fig.colorbar(im, ax=ax, fraction=0.045, pad=0.03)
    cb.set_label("chevauchement (% du marché de la ligne)")
    cb.outline.set_visible(False)
    ax.set_title("Qui concurrence qui ? Chevauchement des marchés idéologiques (simulation « 2025 »)",
                 loc="left", fontsize=11, pad=12)
    fig.text(0.98, 0.01, "données entièrement simulées", fontsize=7.5, color=MUTED, ha="right")
    fig.savefig(OUT / "fig5_chevauchement.png"); plt.close(fig)


def fig6_territoires(E, C, D, top, marge):
    rgba = np.zeros(E.shape + (4,))
    cols = [to_rgba(PARTIES[n]["col"]) for n in PARTY_NAMES]
    T = top.reshape(E.shape); M = marge.reshape(E.shape)
    for j in range(len(PARTY_NAMES)):
        mask = T == j
        for k in range(3):
            rgba[..., k][mask] = cols[j][k]
    rgba[..., 3] = 0.12 + 0.78 * np.clip(M / 0.6, 0, 1)
    fig, ax = plt.subplots(figsize=(7.6, 7.2))
    ax.imshow(rgba, origin="lower", extent=(-LIM, LIM, -LIM, LIM), interpolation="bilinear", zorder=1)
    lv = np.linspace(D.min(), D.max(), 8)[1:]
    ax.contour(E, C, D, levels=lv, colors=[INK], linewidths=0.5, alpha=0.5, zorder=3)
    draw_parties(ax, ellipses=False, size=40, offsets={"Reconquête": (0.15, 0.2), "RN": (-0.55, -0.6), "LR": (0.18, -0.35)})
    axes_ideo(ax)
    ax.set_title("Territoires politiques : parti le plus attractif en chaque point (simulation « 2025 »)",
                 loc="left", fontsize=11, pad=12)
    ax.text(-2.95, 2.78, "couleur : parti dominant\nopacité : marge sur le second\ncontours : densité d'électeurs",
            fontsize=8, color=INK2, va="top", bbox=dict(boxstyle="round,pad=0.3", fc=SURFACE, ec="none", alpha=0.85))
    fig.text(0.99, 0.005, "données entièrement simulées", fontsize=7.5, color=MUTED, ha="right")
    fig.savefig(OUT / "fig6_territoires.png"); plt.close(fig)


def fig7_vacant(E, C, D, U):
    fig, ax = plt.subplots(figsize=(7.6, 7.2))
    lv = np.linspace(0, U.max(), 10)[1:]
    ax.contourf(E, C, U, levels=np.concatenate([[0], lv]), cmap=TEAL_CMAP, antialiased=True)
    ax.contour(E, C, D, levels=np.linspace(D.min(), D.max(), 8)[1:], colors=[INK2], linewidths=0.3, alpha=0.35)
    draw_parties(ax, ellipses=False, size=40, offsets={"Reconquête": (0.15, 0.2), "RN": (-0.55, -0.6), "LR": (0.18, -0.35)})
    k = np.unravel_index(np.argmax(U), U.shape)
    ax.scatter(E[k], C[k], s=160, marker="*", color="#1B6E64", ec=SURFACE, lw=1.2, zorder=8)
    ax.annotate(f"maximum : E = {E[k]:+.1f}, C = {C[k]:+.1f}", (E[k], C[k]), xytext=(E[k] + 0.25, C[k] - 0.45),
                fontsize=8.5, color="#1B6E64", fontweight="bold")
    axes_ideo(ax)
    ax.set_title("Espace politique mal représenté : U = densité × (1 − max probabilité de capture)",
                 loc="left", fontsize=11, pad=12)
    ax.text(-2.95, 2.78, "vert : beaucoup d'électeurs\nqu'aucun parti ne capte avec une forte probabilité",
            fontsize=8, color=INK2, va="top", bbox=dict(boxstyle="round,pad=0.3", fc=SURFACE, ec="none", alpha=0.85))
    fig.text(0.99, 0.005, "données entièrement simulées", fontsize=7.5, color=MUTED, ha="right")
    fig.savefig(OUT / "fig7_espace_vacant.png"); plt.close(fig)


def fig8_entrant(E, C, D, share_grid, Eg, Cg, best_by_year):
    fig, ax = plt.subplots(figsize=(7.6, 7.2))
    lv = np.linspace(share_grid.min(), share_grid.max(), 10)[1:]
    ax.contourf(Eg, Cg, share_grid, levels=np.concatenate([[share_grid.min()], lv]), cmap=TEAL_CMAP, antialiased=True)
    ax.contour(E, C, D, levels=np.linspace(D.min(), D.max(), 8)[1:], colors=[INK2], linewidths=0.3, alpha=0.35)
    draw_parties(ax, ellipses=False, size=40, offsets={"Reconquête": (0.15, 0.2), "RN": (0.16, 0.16), "LR": (0.18, -0.35)})
    # optimum de chaque date-carte : marqueurs séparés, sans trait (la surface est
    # plate et multimodale, un trait suggérerait une trajectoire continue qui n'existe pas)
    for y in DATES_CARTE:
        pos = best_by_year[y]["pos"]; sh = 100 * best_by_year[y]["share"]
        if y == DATES_CARTE[-1]:
            ax.scatter(*pos, s=200, marker="*", color="#1B6E64", ec=SURFACE, lw=1.2, zorder=9)
            ax.annotate(f"optimum {y} : {sh:.0f} % de l'électorat", pos, xytext=(pos[0] - 1.55, pos[1] - 0.42),
                        fontsize=8.5, color="#1B6E64", fontweight="bold",
                        path_effects=[pe.withStroke(linewidth=2.6, foreground=SURFACE)])
        else:
            ax.scatter(*pos, s=34, color=SURFACE, ec="#1B6E64", lw=1.4, zorder=8)
            ax.annotate(f"{y}", pos, xytext=(pos[0] - 0.62, pos[1] - 0.06), fontsize=8, color="#1B6E64",
                        path_effects=[pe.withStroke(linewidth=2.4, foreground=SURFACE)])
    axes_ideo(ax)
    ax.set_title("Position optimale d'un nouvel entrant (offre 2025 fixée, demande de chaque date)",
                 loc="left", fontsize=11, pad=12)
    ax.text(-2.95, 2.78, "vert : part de l'électorat qu'obtiendrait un nouvel entrant\nplacé en ce point (demande 2025)\n"
            "cercles : optimum pour la demande de 1995, 2005, 2015", fontsize=8, color=INK2, va="top",
            bbox=dict(boxstyle="round,pad=0.3", fc=SURFACE, ec="none", alpha=0.85))
    fig.text(0.99, 0.005, "données entièrement simulées", fontsize=7.5, color=MUTED, ha="right")
    fig.savefig(OUT / "fig8_entrant_optimal.png"); plt.close(fig)


def fig9_correlation(moms):
    fig, (ax0, ax1) = plt.subplots(1, 2, figsize=(11, 4.2))
    mE = [moms[y]["mE"] for y in DATES]; mC = [moms[y]["mC"] for y in DATES]; r = [moms[y]["corr"] for y in DATES]
    ax0.plot(DATES, mE, color="#4E8FD0", lw=2, marker="o", ms=4, mec=SURFACE)
    ax0.plot(DATES, mC, color="#8A4FA8", lw=2, marker="o", ms=4, mec=SURFACE)
    ax0.annotate("moyenne de E (économie)", (DATES[-1], mE[-1]), xytext=(6, 0), textcoords="offset points", va="center", fontsize=8.5, color="#4E8FD0", fontweight="bold")
    ax0.annotate("moyenne de C (culture)", (DATES[-1], mC[-1]), xytext=(6, 0), textcoords="offset points", va="center", fontsize=8.5, color="#8A4FA8", fontweight="bold")
    ax0.axhline(0, color=MUTED, lw=0.6); ax0.set_ylim(-1, 1); ax0.set_xlim(1993, 2027); ax0.set_xticks(DATES)
    ax0.yaxis.grid(True, color=GRID, lw=0.6); ax0.set_axisbelow(True)
    ax0.set_title("Les moyennes bougent peu", loc="left", fontsize=10.5)
    ax1.plot(DATES, r, color=INK, lw=2.2, marker="o", ms=4.5, mec=SURFACE)
    ax1.axhline(0, color=MUTED, lw=0.6); ax1.set_ylim(-0.4, 0.8); ax1.set_xlim(1993, 2027); ax1.set_xticks(DATES)
    ax1.yaxis.grid(True, color=GRID, lw=0.6); ax1.set_axisbelow(True)
    ax1.annotate(f"{r[0]:+.2f}", (DATES[0], r[0]), xytext=(0, 8), textcoords="offset points", ha="center", fontsize=8.5, color=INK)
    ax1.annotate(f"{r[-1]:+.2f}", (DATES[-1], r[-1]), xytext=(0, 8), textcoords="offset points", ha="center", fontsize=8.5, color=INK)
    ax1.set_title("… mais la corrélation entre E et C s'effondre", loc="left", fontsize=10.5)
    ax1.set_ylabel("corr(E, C)")
    fig.suptitle("Position moyenne et corrélation économie / culture dans l'électorat simulé, 1995-2025",
                 x=0.04, ha="left", fontsize=11.5)
    fig.text(0.98, 0.01, "données entièrement simulées", fontsize=7.5, color=MUTED, ha="right")
    fig.tight_layout(rect=(0, 0.02, 0.9, 0.93))
    fig.savefig(OUT / "fig9_correlation.png"); plt.close(fig)



def sample_votes(P):
    """Un vote par électeur, tiré selon ses probabilités (dernière colonne : abstention)."""
    cum = np.cumsum(P, axis=1)
    u = RNG.random(len(P))[:, None]
    return (u > cum).sum(axis=1)


ABST_COL = "#D3D6DA"


def fig10_nuage(Z, votes):
    """Un point par électeur, coloré par son vote ; la superposition fait la saillance."""
    fig, ax = plt.subplots(figsize=(7.6, 7.2))
    cols = [PARTIES[n]["col"] for n in PARTY_NAMES] + [ABST_COL]
    abst = votes == len(PARTY_NAMES)
    ax.scatter(Z[abst, 0], Z[abst, 1], s=4, c=ABST_COL, alpha=0.35, lw=0, zorder=1, rasterized=True)
    idx = np.flatnonzero(~abst); RNG.shuffle(idx)
    ax.scatter(Z[idx, 0], Z[idx, 1], s=5, c=[cols[v] for v in votes[idx]], alpha=0.38, lw=0, zorder=2, rasterized=True)
    draw_parties(ax, ellipses=False, size=46, offsets={"Reconquête": (0.15, 0.2), "RN": (-0.9, -0.05), "LR": (0.18, -0.38), "PS": (0.14, 0.14)})
    axes_ideo(ax)
    ax.set_title("Où sont les électeurs de chaque parti ? Un point par électeur, coloré par son vote (« 2025 »)",
                 loc="left", fontsize=11, pad=12)
    ax.text(-2.95, 2.78, f"{len(Z):,} électeurs simulés\ngris : abstention ({100*abst.mean():.0f} %)".replace(",", " "),
            fontsize=8, color=INK2, va="top", bbox=dict(boxstyle="round,pad=0.3", fc=SURFACE, ec="none", alpha=0.85))
    fig.text(0.99, 0.005, "données entièrement simulées", fontsize=7.5, color=MUTED, ha="right")
    fig.savefig(OUT / "fig10_nuage_electeurs.png"); plt.close(fig)


def fig11_nuage_par_parti(Z, votes, metrics):
    fig, axes = plt.subplots(2, 3, figsize=(12.6, 8.6), sharex=True, sharey=True)
    for ax, (j, name) in zip(axes.ravel(), enumerate(PARTY_NAMES)):
        ax.scatter(Z[:, 0], Z[:, 1], s=3, c="#C9CCD1", alpha=0.25, lw=0, zorder=1, rasterized=True)
        m = votes == j
        ax.scatter(Z[m, 0], Z[m, 1], s=5, c=PARTIES[name]["col"], alpha=0.5, lw=0, zorder=2, rasterized=True)
        ax.scatter(*PARTIES[name]["mu"], s=60, color=PARTIES[name]["col"], ec=SURFACE, lw=1.4, zorder=5)
        axes_ideo(ax, labels=False)
        ax.set_title(f"{name}  ·  {100*metrics[name]['score_exprimes']:.0f} % des exprimés", loc="left",
                     fontsize=10.5, fontweight="bold", color=PARTIES[name]["col"], pad=6)
    for ax in axes[1]:
        ax.set_xlabel("Économie   ←  interv.        libéral.  →")
    for ax in axes[:, 0]:
        ax.set_ylabel("Culture   ←  progr.        conserv.  →")
    fig.suptitle("L'électorat de chaque parti dans le même plan (fond gris : tous les électeurs)",
                 x=0.04, ha="left", fontsize=11.5, y=0.985)
    fig.text(0.99, 0.008, "données entièrement simulées", fontsize=7.5, color=MUTED, ha="right")
    fig.tight_layout(rect=(0, 0.02, 1, 0.97))
    fig.savefig(OUT / "fig11_nuage_par_parti.png"); plt.close(fig)


def fig12_nuage_enquete(Z, votes, n=3000, niveaux=11):
    """Ce que donnerait une vraie enquête : n répondants, positions sur une échelle
    discrète à `niveaux` modalités par axe, jitter pour dé-superposer."""
    idx = RNG.choice(len(Z), n, replace=False)
    pas = 2 * LIM / (niveaux - 1)
    Zd = np.round(Z[idx] / pas) * pas + RNG.uniform(-0.42 * pas, 0.42 * pas, size=(n, 2))
    v = votes[idx]
    cols = [PARTIES[nm]["col"] for nm in PARTY_NAMES] + [ABST_COL]
    fig, ax = plt.subplots(figsize=(7.6, 7.2))
    abst = v == len(PARTY_NAMES)
    ax.scatter(Zd[abst, 0], Zd[abst, 1], s=13, c=ABST_COL, alpha=0.6, lw=0, zorder=1)
    k = np.flatnonzero(~abst); RNG.shuffle(k)
    ax.scatter(Zd[k, 0], Zd[k, 1], s=15, c=[cols[t] for t in v[k]], alpha=0.65, lw=0, zorder=2)
    draw_parties(ax, ellipses=False, size=46, offsets={"Reconquête": (0.15, 0.2), "RN": (-0.9, -0.05), "LR": (0.18, -0.38), "PS": (0.14, 0.14)})
    axes_ideo(ax)
    n_txt = f"{n:,}".replace(",", " ")
    ax.set_title(f"À quoi ressemblerait une enquête réelle : {n_txt} répondants, échelles à {niveaux} points",
                 loc="left", fontsize=11, pad=12)
    ax.text(-2.95, 2.78, "chaque point : un répondant, auto-positionné sur deux\néchelles discrètes (jitter), coloré par son vote déclaré",
            fontsize=8, color=INK2, va="top", bbox=dict(boxstyle="round,pad=0.3", fc=SURFACE, ec="none", alpha=0.85))
    fig.text(0.99, 0.005, "données entièrement simulées", fontsize=7.5, color=MUTED, ha="right")
    fig.savefig(OUT / "fig12_nuage_enquete.png"); plt.close(fig)


# ============================================================================
# 6. MAIN
# ============================================================================

def main():
    OUT.mkdir(exist_ok=True)
    samples = {y: simulate_voters(y) for y in DATES}
    Z25 = samples[2025]
    E, C, Zg = grid(141)
    D25 = density_on_grid(Z25, Zg, E.shape)

    metrics, abst = party_metrics(Z25)
    O = overlap_matrix(Z25)
    top, marge = territories(Zg)
    U = vacancy(Zg, D25.ravel()).reshape(E.shape)
    moms = {y: moments(samples[y]) for y in DATES}

    # entrant : carte 2025 sur grille 81×81, optimum par date sur grille 41×41
    Eg, Cg, Zg8 = grid(81)
    share25 = entrant_share(Z25, Zg8, attractions(Z25)).reshape(Eg.shape)
    _, _, Zsmall = grid(41)
    best = {}
    for y in DATES:
        s = entrant_share(samples[y], Zsmall, attractions(samples[y]))
        k = int(np.argmax(s)); best[y] = dict(pos=Zsmall[k].tolist(), share=float(s[k]))

    fig1_carte(Z25, E, C, D25)
    fig2_dates(samples, E, C)
    masses = fig3_familles(samples, E, C, D25)
    fig4_potentiel_vs_score(metrics)
    fig5_chevauchement(O)
    fig6_territoires(E, C, D25, top, marge)
    fig7_vacant(E, C, D25, U)
    fig8_entrant(E, C, D25, share25, Eg, Cg, best)
    fig9_correlation(moms)
    votes = sample_votes(choice_probs(attractions(Z25)))
    fig10_nuage(Z25, votes)
    fig11_nuage_par_parti(Z25, votes, metrics)
    fig12_nuage_enquete(Z25, votes)

    kU = np.unravel_index(np.argmax(U), U.shape)
    resume = dict(
        abstention_2025=abst,
        partis=metrics,
        familles={str(y): masses[y] for y in DATES},
        chevauchement={p: {q: float(O[i, j]) for j, q in enumerate(PARTY_NAMES)} for i, p in enumerate(PARTY_NAMES)},
        moments={str(y): moms[y] for y in DATES},
        vacant_max=dict(E=float(E[kU]), C=float(C[kU])),
        entrant_optimal={str(y): best[y] for y in DATES},
    )
    (OUT.parent / "resultats_simules.json").write_text(json.dumps(resume, indent=2, ensure_ascii=False))
    print(f"abstention simulée 2025 : {100*abst:.1f} %")
    for n in PARTY_NAMES:
        m = metrics[n]
        print(f"  {n:12s} score {100*m['score']:5.1f} % élect. ({100*m['score_exprimes']:5.1f} % exprimés) | "
              f"cœur {100*m['coeur']:5.1f} | accessible {100*m['accessible']:5.1f}")
    print("corr(E,C) :", {y: round(moms[y]["corr"], 2) for y in DATES})
    print("familles 1995 → 2025 :", {k: (round(100*masses[1995][k]), round(100*masses[2025][k])) for k in FAMILLES})
    print("entrant optimal :", {y: (np.round(best[y]['pos'], 2).tolist(), round(100*best[y]['share'], 1)) for y in DATES})


if __name__ == "__main__":
    main()
