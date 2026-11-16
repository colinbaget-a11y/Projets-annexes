"""Bloc IR-CSG-CRDS (note8p) : figures g1 à g3 (python3 note8p/calculs/ircsg_figures.py, après ircsg_proposition.py).

g1_taux_moyens : taux moyens d'aujourd'hui d'un salarié seul (IR et CEHR, CSG-CRDS, ensemble), en fonction du revenu
                 après cotisations (OpenFisca 176.1, droit des revenus 2025) ;
g2_taux_marginaux : taux marginal sur 100 € de revenu après cotisations, salarié seul : aujourd'hui (IR + CEHR + CSG +
                 CRDS, OpenFisca), fusion naïve (barème actuel de l'IR sur l'assiette large + taux proportionnel calé
                 sur la recette), proposition ;
g3_cas_types : variation de l'impôt de huit ménages types (€ par an).
"""
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

RACINE = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RACINE / "note8p"))
from charte import AUJ, NAIF, PROP, HAUSSE, ENCRE2, PLEINE, DEMI, plt, axes, sauver, _fr  # noqa: E402
from matplotlib.ticker import FuncFormatter  # noqa: E402

S = RACINE / "note8p/sorties"
D = json.loads((S / "ircsg.json").read_text(encoding="utf-8"))
MG = pd.read_csv(S / "ircsg_of_marges.csv")
g = MG[MG.profil == "seul"].sort_values("base")
keur = FuncFormatter(lambda v, _: _fr(v / 1000) + " k€")
pctf = FuncFormatter(lambda v, _: _fr(v) + " %")

# ------------------------------------------------------------------ g1 : taux moyens d'aujourd'hui
h = g[g.base <= 250000]
b = h.base_eff.values
ir = 100 * (h.ir + h.cehr + h.cdhr).values / b
cs = 100 * (h.csg + h.crds).values / b
fig, ax = plt.subplots(figsize=(DEMI, 2.3))
ax.plot(h.base, ir + cs, color=AUJ, lw=2.0)
ax.plot(h.base, ir, color=AUJ, lw=1.2, ls="--")
ax.plot(h.base, cs, color=AUJ, lw=1.2, ls=":")
ax.text(250000, (ir + cs)[-1] + 1.2, "Ensemble", ha="right", va="bottom", color=ENCRE2, fontsize=7)
ax.text(250000, 21.5, "IR (et CEHR)", ha="right", va="top", color=ENCRE2, fontsize=7)
ax.text(250000, cs[-1] - 1.0, "CSG et CRDS", ha="right", va="top", color=ENCRE2, fontsize=7)
ax.set_xlim(0, 250000)
ax.set_ylim(0, 45)
ax.xaxis.set_major_formatter(keur)
ax.yaxis.set_major_formatter(pctf)
ax.set_xticks([0, 50e3, 100e3, 150e3, 200e3, 250e3])
ax.set_xlabel("Revenu annuel après cotisations sociales", fontsize=7.5)
axes(ax)
sauver(fig, "g1_taux_moyens",
       "OpenFisca-France 176.1, droit des revenus 2025 ; calculs des auteurs (note8p/calculs/ircsg_openfisca.py).",
       "Salarié du privé vivant seul, sans enfant ni autre revenu ; taux moyens rapportés au revenu après cotisations"
       " sociales (salaire brut moins cotisations salariales, avant CSG).")

# ------------------------------------------------------------------ g2 : taux marginaux
h = g[g.base <= 300000]
tm = 100 * ((h.ir_plus + h.cehr_plus + h.cdhr_plus + h.csg_plus + h.crds_plus)
            - (h.ir + h.cehr + h.cdhr + h.csg + h.crds)).values / (h.base_eff_plus - h.base_eff).values
tm = pd.Series(tm).rolling(21, center=True, min_periods=1).median().values   # neutralise les arrondis à l'euro de l'IR
x = h.base.values
bar = D["bareme"]
sx, st = np.array(bar["seuils"]), np.array(bar["taux"])
prop = 100 * st[np.clip(np.searchsorted(sx, x, side="right") - 1, 0, len(st) - 1)]
tau = D["variantes"]["naive"]["tau"]
irs = np.array([0.0, 11600.0, 29579.0, 84577.0, 181917.0])
irt = np.array([0.0, 0.11, 0.30, 0.41, 0.45])
naive = 100 * (irt[np.searchsorted(irs, x, side="right") - 1] + tau)
fig, ax = plt.subplots(figsize=(PLEINE, 2.5))
ax.axhline(50, color=HAUSSE, lw=0.8, ls="--")
ax.text(125000, 50.8, "plafond de 50 %", ha="left", va="bottom", color=HAUSSE, fontsize=7)
ax.plot(x, tm, color=AUJ, lw=1.4, label="Aujourd'hui (IR, CEHR, CSG, CRDS)", drawstyle="steps-post")
ax.plot(x, naive, color=NAIF, lw=1.6, label=f"Fusion naïve (barème de l'IR + {_fr(100 * tau, 1)} %)", drawstyle="steps-post")
ax.plot(x, prop, color=PROP, lw=2.0, label="Proposition", drawstyle="steps-post")
ax.set_xlim(0, 280000)
ax.set_ylim(0, 60)
ax.set_xticks(np.arange(0, 280001, 40000))
ax.xaxis.set_major_formatter(keur)
ax.yaxis.set_major_formatter(pctf)
ax.set_xlabel("Revenu annuel après cotisations sociales", fontsize=7.5)
ax.legend(loc="lower right", ncol=1, fontsize=7)
axes(ax)
sauver(fig, "g2_taux_marginaux",
       "OpenFisca-France 176.1 (aujourd'hui, droit des revenus 2025) ; calculs des auteurs (note8p/calculs/ircsg_*.py).",
       "Salarié vivant seul, sans enfant : prélèvement sur 100 € de revenu après cotisations en plus. Fusion naïve :"
       " barème actuel de l'IR (sans décote ni abattement) appliqué au revenu après cotisations, plus un taux"
       " proportionnel qui donne la même recette. La CEHR (3 %, puis 4 % au-delà de 500 000 € de revenu fiscal) s'ajoute"
       " aujourd'hui au-delà d'environ 270 000 €. Courbe d'aujourd'hui : médiane glissante sur ± 1 000 €, qui neutralise"
       " les arrondis à l'euro du calcul de l'IR.")

# ------------------------------------------------------------------ g3 : cas-types
C = D["cas_types"]
LIB = [("jeune_smic", "Jeune salarié au Smic"),
       ("sal_2000", "Salarié à 2 000 € net par mois"),
       ("couple2_60", "Couple biactif, 2 enfants, 60 000 € brut"),
       ("mono2_60", "Famille mono-active, 2 enfants, 60 000 € brut"),
       ("nomb3_60", "Famille nombreuse, 3 enfants, 60 000 € brut"),
       ("cadre120", "Cadre supérieur seul, 120 000 € brut"),
       ("ret_16", "Retraité seul, pension de 16 000 €"),
       ("retc_60", "Couple de retraités, 60 000 € de pensions")]
vals = [C[k]["delta"] for k, _ in LIB]
fig, ax = plt.subplots(figsize=(PLEINE, 2.6))
y = np.arange(len(LIB))[::-1]
ax.barh(y, vals, color=[HAUSSE if v > 0 else PROP for v in vals], height=0.62, zorder=2)
ax.axvline(0, color=ENCRE2, lw=0.7)
for yy, v in zip(y, vals):
    r_ = round(v, -1)
    ax.text(v + (120 if v >= 0 else -120), yy, ("+" if r_ > 0 else "") + _fr(r_ if r_ != 0 else 0) + " €", va="center",
            ha="left" if v >= 0 else "right", fontsize=7, color=ENCRE2)
ax.set_yticks(y)
ax.set_yticklabels([l for _, l in LIB], fontsize=7.5)
ax.set_xlim(-8500, 3000)
ax.xaxis.set_major_formatter(FuncFormatter(lambda v, _: _fr(v) + " €"))
ax.text(-8400, -0.9, "baisse d'impôt", color=PROP, fontsize=7, va="center")
ax.text(2900, -0.9, "hausse d'impôt", color=HAUSSE, fontsize=7, va="center", ha="right")
ax.set_ylim(-1.3, len(LIB) - 0.5)
axes(ax, grille="x")
for s_ in ("left",):
    ax.spines[s_].set_visible(False)
ax.tick_params(axis="y", length=0)
sauver(fig, "g3_cas_types",
       "OpenFisca-France 176.1 (charge d'aujourd'hui : IR, CEHR, CSG et CRDS, droit des revenus 2025) ; calculs des"
       " auteurs (note8p/calculs/ircsg_proposition.py).",
       "Variation de l'impôt annuel, réforme achevée. Salariés du privé ; couples mariés ou pacsés (biactifs : 60/40) ;"
       " retraités de plus de 65 ans ; aucune niche. Smic 2025 : 21 622 € brut par an.")
print("figures écrites")
