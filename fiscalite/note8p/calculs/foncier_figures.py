"""Figures g4, g5 et g6 du bloc « fiscalité immobilière » (charte de note8p/charte.py).

Lancer depuis fiscalite/ après foncier_calculs.py : python3 note8p/calculs/foncier_figures.py
  -> note8p/figures/g4_taxe_valeur, g5_achats, g6_sol_bati (.pdf, .png, _source.tex)
"""
import json
import sys
from pathlib import Path

ICI = Path(__file__).resolve().parent
sys.path.insert(0, str(ICI.parent))
from charte import *  # noqa: E402,F401,F403
from charte import _fr  # noqa: E402

J = json.loads((ICI.parent / "sorties/foncier.json").read_text(encoding="utf-8"))
REC = J["logements"]["E15"]

# ---------------------------------------------------------------------------------------------------------- g4
fig, ax = plt.subplots(figsize=(DEMI, 2.35))
x = list(range(1, 11))
auj, apres = J["tfv_auj"], REC["tfv"]
ax.plot(x, auj, color=AUJ, marker="o", ms=3.2, label="Aujourd'hui")
ax.plot(x, apres, color=PROP, marker="o", ms=3.2, label="Après réforme")
ax.text(10.15, auj[-1], _fr(auj[-1], 2) + " %", color=ENCRE2, va="center", fontsize=7)
ax.text(10.15, apres[-1], _fr(apres[-1], 2) + " %", color=ENCRE2, va="center", fontsize=7)
ax.text(0.8, auj[0], _fr(auj[0], 2) + " %", color=ENCRE2, va="center", ha="right", fontsize=7)
ax.text(0.8, apres[0], _fr(apres[0], 2) + " %", color=ENCRE2, va="center", ha="right", fontsize=7)
ax.text(5.5, 0.30, "aujourd'hui", color=AUJ, fontsize=7.5, ha="center", va="top")
ax.text(4.0, 0.60, "après réforme", color=PROP, fontsize=7.5, ha="center", va="bottom")
ax.set_xticks(x)
ax.set_xticklabels([_fr(v / 1000, 1) for v in J["dec_pm2"]])
ax.set_xlabel("Prix du m² dans la commune (milliers d'euros)", color=ENCRE2)
ax.set_ylim(0, 0.75)
ax.set_xlim(-0.5, 11.2)
ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: _fr(v, 1) + " %"))
axes(ax)
sauver(fig, "g4_taxe_valeur",
       "modèle communal du bloc (note8p/calculs/foncier_calculs.py) : DVF 2023-2024 (prix), REI 2025 (taxe foncière),"
       " Insee Analyses n° 91 (taxe / valeur 2017), comptes de patrimoine 2025 (part du sol).",
       "Taxe foncière bâtie des logements des particuliers rapportée à leur valeur de marché, par dixième de logements"
       " classés selon le prix au m² de leur commune (métropole hors Alsace-Moselle) ; abscisse : prix médian du dixième."
       " Après réforme : base sol + bâti/4, part communale à recette constante, part nationale de 15 Md€ ; valeurs avant"
       " capitalisation. Même taux de la valeur pour tous les logements d'une commune.")

# ---------------------------------------------------------------------------------------------------------- g5
cas = J["cas"]
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
       "DVF 2023-2024 (prix médian au m² de la commune) ; CGI art. 1594 D et 1584 (droits) ; modèle du bloc (taxe"
       " foncière) ; note8p/calculs/foncier_calculs.py.",
       "Droits de mutation au taux permanent (4,50 % département, 1,20 % commune, frais d'assiette de l'État), ceux que"
       " paient en 2026 les primo-accédants et tous les acheteurs à partir du 1er avril 2028 ; les autres acheteurs paient"
       " 6,32 % jusqu'au 31 mars 2028 dans ces trois départements. Hausse de taxe foncière : enveloppe de 15 Md€, en régime"
       " permanent (atteinte en trois paliers), proportionnelle à la valeur dans la commune.")

# ---------------------------------------------------------------------------------------------------------- g6
g = J["g6"]
fig, ax = plt.subplots(figsize=(DEMI, 2.4))
pos = {"unique": (0.0, 0.9), "double": (2.6, 3.5)}
col = {"unique": AUJ, "double": PROP}
for s, (xn, xb) in pos.items():
    nu, bati = g[f"{s}_nu"], g[f"{s}_bati"]
    ax.bar(xn, nu, 0.7, color=col[s], zorder=3)
    ax.bar(xb, nu, 0.7, color=col[s], zorder=3)
    ax.bar(xb, bati - nu, 0.7, bottom=nu, color="white", edgecolor=col[s], hatch="////", lw=0.8, zorder=3)
    ax.text(xn, nu + 60, _fr(round(nu, -1)) + " €", ha="center", va="bottom", fontsize=7, color=ENCRE2)
    ax.text(xb, bati + 60, _fr(round(bati, -1)) + " €", ha="center", va="bottom", fontsize=7, color=ENCRE2)
    ax.text(xb + 0.42, nu + (bati - nu) / 2, "+" + _fr(round(bati - nu, -1)) + " €\nsi l'on\nconstruit",
            ha="left", va="center", fontsize=6.8, color=ENCRE)
ax.set_xticks([0, 0.9, 2.6, 3.5])
ax.set_xticklabels(["terrain\nnu", "terrain\n+ immeuble", "terrain\nnu", "terrain\n+ immeuble"], fontsize=7)
ax.text(0.45, -0.30, "Taux unique\n(≈ aujourd'hui)", transform=ax.get_xaxis_transform(), ha="center", va="top",
        fontsize=7.5, color=AUJ, fontweight="bold")
ax.text(3.05, -0.30, "Sol taxé 4 fois\nplus que le bâti", transform=ax.get_xaxis_transform(), ha="center", va="top",
        fontsize=7.5, color=PROP, fontweight="bold")
ax.tick_params(axis="x", length=0)
ax.set_xlim(-0.6, 4.6)
ax.set_ylim(0, 3300)
ax.yaxis.set_major_formatter(euros)
ax.set_ylabel("Impôt annuel", color=ENCRE2)
axes(ax)
fig.subplots_adjust(bottom=0.33)
sauver(fig, "g6_sol_bati",
       "calcul illustratif (note8p/calculs/foncier_calculs.py).",
       f"Deux terrains de même valeur ({_fr(g['sol'])} €), l'un nu, l'autre portant un immeuble de {_fr(g['bati'])} €."
       f" Taux unique : {_fr(g['taux_unique'], 2)} % de la valeur totale (taxe foncière / valeur des logements en 2025)."
       f" Double taux : {_fr(g['taux_sol'], 2)} % sur le sol et {_fr(g['taux_bati'], 2)} % sur le bâti, pour la même"
       " recette sur les deux terrains. Hachures : impôt dû à cause de l'immeuble. En France, un terrain nu paie aujourd'hui"
       " la taxe sur le non-bâti, assise sur des valeurs cadastrales souvent plus basses : l'écart actuel est plus grand.")
print("figures écrites")
