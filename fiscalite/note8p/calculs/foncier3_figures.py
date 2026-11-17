"""Figures g4, g5, g6 et g10 du bloc « fiscalité immobilière », version 3 (charte de note8p/charte.py).

Lancer depuis fiscalite/ après foncier3_calculs.py : python3 note8p/calculs/foncier3_figures.py [--rec B_E10]
  -> note8p/figures/g4_taxe_valeur, g5_achats, g6_sol_bati, g10_foncier_pib (.pdf, .png, _source.tex)
Le scénario recommandé (architecture × enveloppe) se change avec --rec (ex. --rec A_E15).
"""
import argparse
import json
import sys
from pathlib import Path

ICI = Path(__file__).resolve().parent
sys.path.insert(0, str(ICI.parent))
from charte import *  # noqa: E402,F401,F403
from charte import _fr  # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument("--rec", default="B_E10")
REC = ap.parse_args().rec
ARCHI, ENV = REC.split("_E")
AUTRE = ("A" if ARCHI == "B" else "B") + "_E" + ENV
J = json.loads((ICI.parent / "sorties/foncier3.json").read_text(encoding="utf-8"))
J0 = json.loads((ICI.parent / "sorties/foncier.json").read_text(encoding="utf-8"))
S = J["scenarios"][REC]
LIB = {"A": "base unique sol + bâti/4 pour les parts communale et nationale",
       "B": "part communale à double taux (sol = 4 × bâti) et part nationale sur le seul sol"}

# ---------------------------------------------------------------------------------------------------------- g4
fig, ax = plt.subplots(figsize=(DEMI, 2.35))
x = list(range(1, 11))
auj, apres = J0["tfv_auj"], S["logements"]["tfv"]
ax.plot(x, auj, color=AUJ, marker="o", ms=3.2)
ax.plot(x, apres, color=PROP, marker="o", ms=3.2)
for serie, dy in ((auj, -0.025), (apres, 0.025)):
    ax.text(10.2, serie[-1], _fr(serie[-1], 2) + " %", color=ENCRE2, va="center", fontsize=7)
    ax.text(0.8, serie[0] + dy, _fr(serie[0], 2) + " %", color=ENCRE2, va="center", ha="right", fontsize=7)
ax.text(5.5, auj[4] - 0.06, "aujourd'hui", color=AUJ, fontsize=7.5, ha="center", va="top")
ax.text(5.5, apres[4] + 0.05, "après réforme", color=PROP, fontsize=7.5, ha="center", va="bottom")
ax.set_xticks(x)
ax.set_xticklabels([_fr(v / 1000, 1) for v in J0["dec_pm2"]])
ax.set_xlabel("Prix du m² dans la commune (milliers d'euros)", color=ENCRE2)
ax.set_ylim(0, 0.75)
ax.set_xlim(-0.5, 11.3)
ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: _fr(v, 1) + " %"))
axes(ax)
sauver(fig, "g4_taxe_valeur",
       "modèle communal du bloc (note8p/calculs/foncier3_calculs.py) : DVF 2023-2024 (prix), REI 2025 (taxe foncière),"
       " Insee Analyses n° 91 (taxe / valeur 2017), comptes de patrimoine 2025 (part du sol).",
       "Taxe foncière des logements des particuliers rapportée à leur valeur de marché, par dixième de logements classés"
       " selon le prix au m² de leur commune (métropole hors Alsace-Moselle) ; abscisse : prix médian du dixième."
       f" Après réforme : {LIB[ARCHI]}, recette nationale nouvelle de {ENV} Md€, part communale à recette constante ;"
       " valeurs avant capitalisation ; même taux de la valeur pour tous les logements d'une commune.")

# ---------------------------------------------------------------------------------------------------------- g5
cas = J["cas"][REC]["projets"]
etiq = {"orleans": "Orléans, appartement 65 m²", "lyon": "Lyon, appartement 80 m²",
        "massy": "Massy, appartement 65 m²", "sgdb": "Ste-Geneviève-des-Bois, maison 100 m²"}
fig, ax = plt.subplots(figsize=(PLEINE, 2.5))
w = 0.36
for k, r in enumerate(cas):
    a, b = r["dmto_permanent"], r["dmto_apres"]
    ax.bar(k - w / 2 - 0.01, a, w, color=AUJ, zorder=3, label="Droits actuels (5,81 %)" if k == 0 else None)
    ax.bar(k + w / 2 + 0.01, b, w, color=PROP, zorder=3, label="Après réforme (2,90 %)" if k == 0 else None)
    ax.text(k - w / 2 - 0.01, a + 400, _fr(round(a, -2)) + " €", ha="center", va="bottom", fontsize=7, color=ENCRE2)
    ax.text(k + w / 2 + 0.01, b + 400, _fr(round(b, -2)) + " €", ha="center", va="bottom", fontsize=7, color=ENCRE2)
    ax.text(k, a + 3300, "économie " + _fr(round(r["economie"], -2)) + " €", ha="center", va="bottom", fontsize=7.5,
            color=ENCRE, fontweight="bold")
    ax.text(k, -0.37, f"taxe foncière +{_fr(round(r['dtf'], -1))} €/an", transform=ax.get_xaxis_transform(),
            ha="center", va="top", fontsize=7, color=HAUSSE)
ax.set_xticks(range(len(cas)))
ax.set_xticklabels([etiq[r["cle"]].replace(", ", ",\n") + f"\nprix {_fr(r['prix'])} €" for r in cas], fontsize=7)
ax.tick_params(axis="x", length=0, pad=3)
ax.set_ylim(0, 33000)
ax.yaxis.set_major_formatter(euros)
axes(ax)
ax.legend(loc="upper left", ncol=2, bbox_to_anchor=(0.0, 1.06))
fig.subplots_adjust(bottom=0.40)
sauver(fig, "g5_achats",
       "DVF 2023-2024 (prix médian au m² de la commune) ; CGI art. 1594 D, 1584 et 1647 V (droits) ; modèle du bloc"
       " (taxe foncière) ; note8p/calculs/foncier3_calculs.py.",
       "Droits au taux permanent (4,50 % département, 1,20 % commune, frais d'assiette de l'État), payés en 2026 par les"
       " primo-accédants et par tous à partir du 1er avril 2028 ; les autres acheteurs paient 6,32 % jusqu'au 31 mars 2028"
       f" dans ces trois départements. Hausse de taxe foncière : {ENV} Md€ de recette nationale, {LIB[ARCHI]}, en régime"
       " permanent (atteint en trois paliers).")

# ---------------------------------------------------------------------------------------------------------- g6
g = J["g6"]
regs = [("aujourdhui", "Aujourd'hui\n(taux unique)", AUJ), (AUTRE, "Base unique\nsol + bâti/4", NAIF),
        (REC, "Double taux + part\nnationale sur le sol", PROP)]
regs = sorted(regs, key=lambda t: {"aujourdhui": 0, f"A_E{ENV}": 1, f"B_E{ENV}": 2}[t[0]])
fig, ax = plt.subplots(figsize=(DEMI, 2.45))
for j, (k, lab, col) in enumerate(regs):
    v = g[k]
    xn, xb = 2.4 * j, 2.4 * j + 0.85
    ax.bar(xn, v["nu"], 0.7, color=col, zorder=3)
    ax.bar(xb, v["nu"], 0.7, color=col, zorder=3)
    ax.bar(xb, v["construire"], 0.7, bottom=v["nu"], color="white", edgecolor=col, hatch="////", lw=0.8, zorder=3)
    ax.text(xn, v["nu"] + 50, _fr(round(v["nu"], -1)), ha="center", va="bottom", fontsize=6.8, color=ENCRE2)
    ax.text(xb, v["bati"] + 50, "+" + _fr(round(v["construire"], -1)), ha="center", va="bottom", fontsize=7,
            color=ENCRE, fontweight="bold")
    ax.text(xn + 0.42, -0.08, "nu   bâti", transform=ax.get_xaxis_transform(), ha="center", va="top", fontsize=6.5,
            color=ENCRE2)
    ax.text(xn + 0.42, -0.2, lab, transform=ax.get_xaxis_transform(), ha="center", va="top", fontsize=6.8,
            color=col if col != NAIF else "#4a78b5", fontweight="bold")
ax.set_xticks([])
ax.set_xlim(-0.6, 2.4 * 2 + 1.5)
ax.set_ylim(0, 3200)
ax.yaxis.set_major_formatter(euros)
ax.set_ylabel("Impôt annuel", color=ENCRE2)
axes(ax)
fig.subplots_adjust(bottom=0.36)
sauver(fig, "g6_sol_bati",
       "calcul illustratif (note8p/calculs/foncier3_calculs.py).",
       f"Terrain de {_fr(g['sol'])} €, nu ou portant un immeuble de {_fr(g['bati'])} € ; chiffre en gras : impôt dû"
       f" à cause de l'immeuble (hachures). Aujourd'hui : {_fr(g['aujourdhui']['t_sol'], 2)} % de la valeur totale"
       f" (taxe foncière / valeur des logements, 2025). Réforme ({ENV} Md€ de recette nationale) : taux communal moyen"
       f" sur la nouvelle base plus part nationale ; sol {_fr(g[REC]['t_sol'], 2)} % et bâti {_fr(g[REC]['t_bati'], 2)} %"
       f" (base unique : {_fr(g[AUTRE]['t_sol'], 2)} % et {_fr(g[AUTRE]['t_bati'], 2)} %). Un terrain nu paie aujourd'hui"
       " la taxe sur le non-bâti, souvent plus basse : l'écart actuel entre nu et bâti est plus grand que figuré.")

# ---------------------------------------------------------------------------------------------------------- g10
h = J["g10"]
an, ens, men = h["annees"], h["ensemble"], h["menages"]
fig, ax = plt.subplots(figsize=(PLEINE, 2.4))
ax.plot(an, ens, color=PROP, lw=2.0, zorder=4)
ax.plot(an, men, color=NAIF, lw=1.6, zorder=3)
for a_, dy in ((1998, 10), (2007, 8), (2022, 8), (2025, -16)):
    i = an.index(a_)
    ax.plot([a_], [ens[i]], "o", color=PROP, ms=4, mec="white", mew=0.8, zorder=5)
    ax.annotate(f"{_fr(ens[i])} %", (a_, ens[i]), xytext=(0, dy), textcoords="offset points", ha="center",
                fontsize=7.5, color=ENCRE, fontweight="bold")
i98, i25 = an.index(1998), an.index(2025)
ax.annotate(f"{_fr(men[i98])} %", (1998, men[i98]), xytext=(0, -12), textcoords="offset points", ha="center",
            fontsize=7, color=ENCRE2)
ax.annotate(f"{_fr(men[i25])} %", (2025, men[i25]), xytext=(4, -10), textcoords="offset points", ha="left",
            fontsize=7, color=ENCRE2)
ax.text(1988, 92, "toute l'économie", color=PROP, fontsize=7.5, ha="center")
ax.text(1988, 20, "ménages", color="#4a78b5", fontsize=7.5, ha="center")
ax.set_xlim(1977, 2027.5)
ax.set_ylim(0, 340)
ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: _fr(v) + " %"))
ax.set_ylabel("en % du PIB", color=ENCRE2)
axes(ax)
sauver(fig, "g10_foncier_pib",
       "Insee, comptes de patrimoine (base 2020, tableau 8.200) et PIB à prix courants (tableau 1.101), millésime 2026 ;"
       " foncier/donnees/patrimoine_2025.csv.",
       "Valeur de fin d'année des terrains supportant des bâtiments (sol bâti, hors terres agricoles et terrains nus),"
       " toute l'économie et ménages. La valeur du sol est un résidu (valeur de marché moins coût de remplacement du"
       f" bâti) : toute variation des prix lui est imputée. De fin 2022 à fin 2025, elle a baissé de"
       f" {_fr(h['sol_2022'] - h['sol_2025'])} Md€.")
print("figures écrites :", REC)
