"""Figures de la note (lit sorties/resultats.json, écrit figures/*.png et .pdf)."""
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

D = Path(__file__).resolve().parent
R = json.loads((D / "sorties" / "resultats.json").read_text(encoding="utf-8"))
P = json.loads((D / "params.json").read_text(encoding="utf-8"))
COUL = {"A": "#B8642A", "B": "#173F8A", "C": "#6A8F3C"}
LIB = {"A": "Baisse des pensions", "B": "Hausse des cotisations", "C": "Recul d'un an de l'âge de départ"}
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 8.5, "axes.spines.top": False,
                     "axes.spines.right": False, "axes.titlesize": 9, "axes.titleweight": "bold"})
AG = np.arange(20, 100)


def echelle(res, k):
    """Normalise chaque réforme à 10 Md€ de 2025 par an à plein effet (2040)."""
    return P["budget_cible"]["valeur"] / res[k]["flux_2040"]


def sauver(fig, nom):
    for ext in ("png", "pdf"):
        fig.savefig(D / "figures" / f"{nom}.{ext}", dpi=200, bbox_inches="tight")
    plt.close(fig)


# 1. perte par âge, scénario central
cle = f"{P['r']['valeur']:.3f}"
res = R[cle]
fig, ax = plt.subplots(figsize=(6.6, 3.4))
for k in ("A", "B", "C"):
    v = np.array(res[k]["perte_par_age"])[AG] * echelle(res, k)
    ax.plot(AG, v / 1000, color=COUL[k], lw=2, label=LIB[k])
v = np.array(res["C_salaire"]["perte_par_age"])[AG] * echelle(res, "C")
ax.plot(AG, v / 1000, color=COUL["C"], lw=1.2, ls="--", label="Recul de l'âge, salaire de l'année en plus compté comme un gain")
ax.set_xlabel("Âge en 2026")
ax.set_ylabel("Perte actualisée, milliers d'euros de 2025")
ax.legend(frameon=False, fontsize=7.5)
ax.grid(axis="y", lw=0.4, alpha=0.5)
ax.set_title(f"Perte actualisée par personne, à rendement égal (10 Md€ par an), r = {100 * res['r']:.0f} %, g = {100 * res['g']:.1f} %",
             loc="left")
sauver(fig, "f1_perte_par_age")

# 2. sensibilité au taux d'actualisation : rapport baisse des pensions / hausse des cotisations
fig, axs = plt.subplots(1, 3, figsize=(7.2, 2.6), sharey=True)
for ax, k in zip(axs, ("A", "B", "C")):
    for c, cl in zip(sorted(R), ("#999999", "#6b8cc7", "#173F8A", "#0b1f45")):
        rr = R[c]
        v = np.array(rr[k]["perte_par_age"])[AG] * echelle(rr, k)
        ax.plot(AG, v / 1000, color=cl, lw=1.4, label=f"r = {100 * rr['r']:.1f} %")
    ax.set_title(LIB[k], loc="left", fontsize=8)
    ax.grid(axis="y", lw=0.4, alpha=0.5)
    ax.set_xlabel("Âge en 2026")
axs[0].set_ylabel("Milliers d'euros de 2025")
axs[0].legend(frameon=False, fontsize=7)
sauver(fig, "f2_sensibilite_r")

# 3. qui paie : répartition de la valeur actualisée du rendement
fig, ax = plt.subplots(figsize=(6.6, 2.6))
tr = ["0-19", "20-34", "35-49", "50-59", "60-64", "65-74", "75-105"]
nom = ["0-19 ans", "20-34", "35-49", "50-59", "60-64", "65-74", "75 ans et +", "Générations futures"]
cols = ["#d9d9d9", "#9ecae1", "#4292c6", "#08519c", "#fdae6b", "#e6550d", "#a63603", "#6A8F3C"]
for i, k in enumerate(("A", "B", "C")):
    x = res[k]
    parts = [x["va_par_tranche"][t] for t in tr] + [x["va_budget"] - x["va_vivants"]]
    parts = np.array(parts) / x["va_budget"] * 100
    g = 0
    for j, (v, c) in enumerate(zip(parts, cols)):
        ax.barh(i, v, left=g, color=c, label=nom[j] if i == 0 else None)
        if v > 6:
            ax.text(g + v / 2, i, f"{v:.0f}", ha="center", va="center", fontsize=7, color="white" if j in (2, 3, 6, 7) else "black")
        g += v
ax.set_yticks(range(3))
ax.set_yticklabels([LIB[k] for k in ("A", "B", "C")])
ax.invert_yaxis()
ax.set_xlabel("Part de la valeur actualisée du rendement, % (âge en 2026)")
ax.legend(frameon=False, fontsize=7, ncol=4, loc="upper center", bbox_to_anchor=(0.45, -0.28))
sauver(fig, "f3_qui_paie")
print("figures écrites")
