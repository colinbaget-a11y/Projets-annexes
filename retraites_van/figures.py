"""Figures de la note (lit sorties/resultats.json, écrit figures/*.png et .pdf)."""
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import matplotlib.ticker  # noqa: E402
import numpy as np  # noqa: E402

D = Path(__file__).resolve().parent
R = json.loads((D / "sorties" / "resultats.json").read_text(encoding="utf-8"))
P = json.loads((D / "params.json").read_text(encoding="utf-8"))
COUL = {"A": "#B8642A", "B": "#173F8A", "C": "#6A8F3C"}
LIB = {"A": "Baisse des pensions", "B": "Hausse des cotisations", "C": "Recul d'un an de l'âge de départ"}
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 8.5, "axes.spines.top": False,
                     "axes.spines.right": False, "axes.titlesize": 9, "axes.titleweight": "bold"})
AG = np.arange(20, 100)


def ex_ante(res, k):
    """Facteur qui ramène une réforme calée sur l'effet public du recul de l'âge à un choc de 6 Md€ ex ante."""
    cle = {"A": "pensions", "B": "cotis_salaries", "B_emp": "cotis_employeurs"}[k]
    return 6.0 / res["calage_reformes"]["X"][cle]


def sauver(fig, nom):
    for ext in ("png", "pdf"):
        fig.savefig(D / "figures" / f"{nom}.{ext}", dpi=200, bbox_inches="tight")
    plt.close(fig)


cle = f"{P['r']['valeur']:.3f}"
res = R[cle]
# 1. même effet sur le solde public (celui d'un an d'âge, moyenne des modèles du COR)
fig, ax = plt.subplots(figsize=(6.6, 3.4))
for k, ls, lab in (("A", "-", LIB["A"]), ("B", "-", "Hausse des cotisations salariales"),
                   ("B_emp", ":", "Hausse des cotisations employeurs (incidence sur les salaires)"), ("C", "-", LIB["C"])):
    v = np.array(res[k]["perte_par_age"])[AG]
    ax.plot(AG, v / 1000, color=COUL[k[0]], lw=2 if ls == "-" else 1.4, ls=ls, label=lab)
ax.set_xlabel("Âge en 2026")
ax.set_ylabel("Perte actualisée, milliers d'euros de 2025")
ax.legend(frameon=False, fontsize=7.5)
ax.grid(axis="y", lw=0.4, alpha=0.5)
sauver(fig, "f1_meme_effet_public")

# 2. même montant ex ante (6 Md€) : baisse des pensions contre hausse des cotisations, selon le taux d'actualisation
fig, axs = plt.subplots(1, 2, figsize=(7.2, 2.8))
cols = ("#999999", "#6b8cc7", "#173F8A", "#0b1f45")
for c, cl in zip(sorted(R), cols):
    rr = R[c]
    a = np.array(rr["A"]["perte_par_age"])[AG] * ex_ante(rr, "A")
    b = np.array(rr["B"]["perte_par_age"])[AG] * ex_ante(rr, "B")
    axs[0].plot(AG, a / 1000, color=cl, lw=1.4, label=f"r = {100 * rr['r']:.1f} %")
    axs[0].plot(AG, b / 1000, color=cl, lw=1.4, ls="--")
    axs[1].plot(AG[:39], (a / b)[:39], color=cl, lw=1.4, label=f"r = {100 * rr['r']:.1f} %")
axs[0].set_title("Perte, milliers d'euros (trait plein : pensions ;\ntirets : cotisations)", loc="left", fontsize=8)
axs[1].set_title("Perte due à la baisse des pensions, en part\nde celle due à la hausse des cotisations", loc="left", fontsize=8)
axs[1].axhline(1, color="k", lw=0.6)
axs[1].set_yscale("log")
axs[1].yaxis.set_minor_formatter(matplotlib.ticker.NullFormatter())
axs[1].set_yticks([0.5, 0.75, 1, 1.5, 2, 3, 5])
axs[1].set_yticklabels(["0,5", "0,75", "1", "1,5", "2", "3", "5"])
for ax in axs:
    ax.set_xlabel("Âge en 2026")
    ax.grid(axis="y", lw=0.4, alpha=0.5)
axs[1].legend(frameon=False, fontsize=7)
sauver(fig, "f2_meme_montant_ex_ante")

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
ax.set_xlabel("Part de la valeur actualisée de l'effort, en % (âge en 2026)")
ax.legend(frameon=False, fontsize=7, ncol=4, loc="upper center", bbox_to_anchor=(0.45, -0.28))
sauver(fig, "f3_qui_paie")
print("figures écrites")
