"""Trois figures « aujourd'hui / réforme naïve / notre réforme » (v6).

g14_menages : impôt mensuel (impôt sur le revenu, CSG, CRDS aujourd'hui ; nouvel impôt demain) de cinq ménages médians.
  - Aujourd'hui : OpenFisca-France 176.1, droit des revenus 2025 (sorties/cas_medians_of.csv, calculs/cas_medians_of.py).
  - Réforme « froide » : fusion et barème lissé, impôt individuel, sans franchise par enfant ; taux des repères 0 à 3,5 Smic
    abaissés uniformément pour que la recette égale celle de notre réforme (même modèle de foyers).
  - Notre réforme : barème final (sorties/ircsg4.json), franchise de 6 000 € par enfant chez le parent qui gagne le plus.
  Forfait de 500 € déduit de chaque salaire dans les deux réformes.
g15_foncier : prélèvements immobiliers, Md€ par an (droits de mutation, taxe foncière sur le bâti, sur le sol, taxe
  nationale sur le sol). Aujourd'hui : taxe foncière répartie entre sol et bâti au prorata de leur valeur (convention :
  taux unique sur la valeur totale) ; réforme naïve : droits divisés par deux, financés par une hausse uniforme de la taxe
  foncière actuelle ; notre réforme : taux communal à deux taux à recette communale inchangée + taxe nationale sur le sol
  (sorties/foncier3.json, montants nationaux du scénario B_E15 ; taxe communale inchangée).
g16_seuil : rendement avant impôt minimal pour qu'une machine neuve financée sur fonds propres soit rentable, quand
  l'actionnaire exige 5 % réels (convention Devereux-Griffith, sorties/is3.json : taux_effectifs).
"""
import csv
import json
import sys
from pathlib import Path

import numpy as np

D = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(D))
sys.path.insert(0, str(D / "calculs"))
from charte import AUJ, NAIF, PROP, HAUSSE, ENCRE, ENCRE2, PLEINE, DEMI, plt, axes, sauver, _fr  # noqa: E402
import ircsg3_modele as N  # noqa: E402

plt.rcParams.update({"font.family": "Liberation Sans", "legend.frameon": False})
S_ = D / "sorties"
J = json.loads((S_ / "ircsg4.json").read_text(encoding="utf-8"))
P0, T = J["bareme"]["points"], J["bareme"]["taux"]
S_FIN = N.continu(P0, T)
O6, O0 = N.options(6000.0), N.options(0.0)
W = np.array([1, 1, 1, 1, 1, 0.0])
cible = N.recette(S_FIN, O6)
lo, hi = -0.05, 0.05
for _ in range(45):
    m = (lo + hi) / 2
    lo, hi = (m, hi) if N.recette(N.continu(P0, list(np.array(T) - m * W)), O0) > cible else (lo, m)
BAISSE_NAIF = (lo + hi) / 2
S_NAIF = N.continu(P0, list(np.array(T) - BAISSE_NAIF * W))
FORFAIT = 500.0

LIB = {"ret_couple": "Couple de retraités,\nchacun la pension médiane",
       "celib": "Célibataire au\nsalaire médian",
       "smic_couple": "Couple de smicards,\nsans enfant",
       "couple_2e": "Couple, deux enfants,\nchacun le salaire médian",
       "mono_2e": "Couple, deux enfants,\nun seul salaire médian"}
rows = {r["cle"]: r for r in csv.DictReader(open(S_ / "cas_medians_of.csv", encoding="utf-8"))}
RES = {}
for k in LIB:
    r = rows[k]
    bases = [float(x) for x in r["bases"].split(";")]
    st = r["statuts"].split(";")
    zs = [max(b - FORFAIT, 0.0) if (s == "sal" and b > 500) else b for b, s in zip(bases, st)]
    kids = int(r["enfants"])
    RES[k] = dict(aujourdhui=float(r["charge"]) / 12, naif=float(N.impot_z(S_NAIF, O0, zs, kids)[0]) / 12,
                  reforme=float(N.impot_z(S_FIN, O6, zs, kids)[0]) / 12)

fig, ax = plt.subplots(figsize=(PLEINE, 3.3))
ordre = list(LIB)
y = np.arange(len(ordre))[::-1]
h = 0.26
for yy, k in zip(y, ordre):
    v = RES[k]
    for off, key, col in ((h, "aujourdhui", AUJ), (0, "naif", NAIF), (-h, "reforme", PROP)):
        ax.barh(yy + off, v[key], height=h, color=col, zorder=2)
        txt = _fr(v[key]) + " €"
        if key != "aujourdhui":
            dlt = v[key] - v["aujourdhui"]
            txt += f"  ({'+' if dlt > 0 else '−'}{_fr(abs(dlt))})"
        ax.text(v[key] + 8, yy + off, txt, va="center", fontsize=6.8,
                color=PROP if key == "reforme" else ENCRE2, fontweight="bold" if key == "reforme" else "normal")
ax.set_yticks(y)
ax.set_yticklabels([LIB[k] for k in ordre], fontsize=7.2)
ax.set_xlim(0, max(max(v.values()) for v in RES.values()) * 1.32)
ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: _fr(v) + " €"))
ax.set_xlabel("Impôt sur le revenu, CSG et CRDS, € par mois (entre parenthèses : écart avec aujourd'hui)", fontsize=7.2)
from matplotlib.patches import Patch  # noqa: E402
ax.legend(handles=[Patch(color=AUJ, label="Aujourd'hui"), Patch(color=NAIF, label="Fusion et lissage, sans franchise"),
                   Patch(color=PROP, label="Notre réforme, avec la franchise par enfant")],
          loc="lower center", bbox_to_anchor=(0.45, 1.0), ncol=3, fontsize=7)
axes(ax, grille="x")
ax.spines["left"].set_visible(False)
ax.tick_params(axis="y", length=0)
sauver(fig, "g14_menages",
       "OpenFisca-France 176.1 (droit des revenus 2025) ; calculs des auteurs (note8p/calculs/cas_medians_of.py,"
       " figures_v6_trois_etats.py).",
       "Salaire médian : 2 183 € net par mois (secteur privé, 2023, Insee), soit 33 100 € brut par an ; pension médiane :"
       " 1 500 € brut par mois, ordre de grandeur (la DREES publie la moyenne, 1 666 € brut fin 2023, pas la médiane) ;"
       " enfants de 7 et 10 ans ; aucune niche. Fusion et lissage sans franchise : même barème continu, impôt individuel,"
       f" taux abaissés de {_fr(100 * BAISSE_NAIF, 1)} point à recette égale. Forfait de 500 € par salaire dans les deux"
       " réformes.")

# ------------------------------------------------------------------ g15 foncier
F = json.loads((S_ / "foncier3.json").read_text(encoding="utf-8"))
sc = F["scenarios"]["B_E10"]["taux"]
A = F["assiette"]
dmto = F["dmto_total"]
com_sol = sc["tc_sol"] / 100 * sc["sol_apres"]
com_bati = sc["tc_bati"] / 100 * A["bati"]
com = com_sol + com_bati
part_sol = A["sol"] / (A["sol"] + A["bati"])
nat = F["scenarios"]["B_E10"]["E"]
nat = float(json.loads((D / "parametres.json").read_text(encoding="utf-8"))["scenario_foncier"].split("_E")[1])
ETATS = [("Aujourd'hui", dmto, com * (1 - part_sol), com * part_sol, 0.0),
         ("Naïve :\ntaxe\nfoncière\nrelevée", dmto / 2, (com + nat) * (1 - part_sol),
          (com + nat) * part_sol, 0.0),
         ("Notre\nréforme :\ntaxe sur\nle sol", dmto / 2, com * (1 - part_sol), com * part_sol, nat)]
COUL = [("Droits de mutation", "#6b6b6b"), ("Taxe foncière : bâti", NAIF), ("Taxe foncière : sol", HAUSSE),
        ("Taxe nationale sur le sol", "#7a3a12")]
fig, ax = plt.subplots(figsize=(DEMI, 2.9))
x = np.arange(len(ETATS))
for i, (lab, *vals) in enumerate(ETATS):
    bas = 0.0
    for v, (nom, col) in zip(vals, COUL):
        if v <= 0:
            continue
        ax.bar(i, v, bottom=bas, width=0.62, color=col, zorder=2, edgecolor="white", lw=0.6)
        ax.text(i, bas + v / 2, _fr(v), ha="center", va="center", fontsize=7, color="white", fontweight="bold")
        bas += v
    ax.text(i, bas + 1, f"total {_fr(bas)}", ha="center", va="bottom", fontsize=7.2, color=ENCRE)
ax.set_xticks(x)
ax.set_xticklabels([e[0] for e in ETATS], fontsize=7)
ax.set_ylabel("Md€ par an", fontsize=7.4)
ax.set_ylim(0, 75)
ax.legend(handles=[Patch(color=c, label=n) for n, c in COUL], fontsize=6.8, loc="upper center", bbox_to_anchor=(0.45, -0.42), ncol=2)
axes(ax)
sauver(fig, "g15_foncier",
       "calculs des auteurs (note8p/calculs/foncier3_calculs.py, taxe nationale de 15 Md€) ; DVF ; comptes de patrimoine (Insee).",
       "Droits de mutation à titre onéreux de 2025 ; taxe foncière communale à recette inchangée, répartie aujourd'hui"
       " entre sol et bâti au prorata de leur valeur (convention : taux unique sur la valeur totale du bien). Réforme"
       " naïve : la même hausse porte sur la taxe actuelle, bâti compris. Notre réforme : taxe communale inchangée, plus une"
       " taxe nationale d'environ 0,24 % sur la seule valeur du sol."
       " Montants arrondis au milliard ; hors report de paiement et déductibilité.")

# ------------------------------------------------------------------ g16 seuil de rentabilité
TE = json.loads((S_ / "is3.json").read_text(encoding="utf-8"))["taux_effectifs"]
r = 0.05
seuil = {k: 100 * r / (1 - TE[k]["fp"]) for k in ("actuel", "taux225", "ded50", "ded100")}
BAR = [("Aujourd'hui\n(taux de 25 %)", seuil["actuel"], AUJ, "coût : référence"),
       ("Réforme naïve :\nbaisse du taux à 22,5 %", seuil["taux225"], NAIF, "6,5 Md€ par an, chaque année"),
       ("Notre réforme :\ndéduction immédiate", seuil["ded100"], PROP, "coût surtout transitoire")]
fig, ax = plt.subplots(figsize=(PLEINE, 2.3))
ax.set_xticks([5.0, 5.5, 6.0, 6.5])
yb = np.arange(len(BAR))[::-1]
for yy, (lab, v, col, cout) in zip(yb, BAR):
    ax.barh(yy, v - 5.0, left=5.0, color=col, height=0.55, zorder=2)
    ax.plot(v, yy, "o", color=col if v > 5.001 else PROP, ms=6, zorder=3)
    ax.text(v + 0.04, yy, _fr(v, 1) + " %" + (f"  (l'impôt ajoute {_fr(v - 5.0, 1)} point)" if v > 5.001 else
            "  (l'impôt ne change plus le seuil)"), va="center", fontsize=7.4, color=ENCRE, fontweight="bold")
    ax.text(7.75, yy, cout, va="center", fontsize=6.9, color=ENCRE2)
ax.plot([seuil["ded50"]] * 2, [yb[2] - 0.32, yb[2] + 0.32], color=ENCRE, lw=1.0, ls=":", zorder=3)
ax.text(seuil["ded50"], yb[2] + 0.38, f"50 % dès 2029 : {_fr(seuil['ded50'], 1)} %", ha="center", fontsize=6.5, color=ENCRE2)
ax.axvline(5.0, color=ENCRE2, lw=0.8, ls="--")
ax.text(4.97, yb[0] + 0.3, "rendement exigé\nsans impôt : 5 %", ha="right", fontsize=6.5, color=ENCRE2)
ax.set_yticks(yb)
ax.set_yticklabels([b[0] for b in BAR], fontsize=7.3)
ax.set_xlim(4.7, 9.4)
ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: _fr(v, 1) + " %"))
ax.set_xlabel("Rendement réel avant impôt qu'une machine neuve doit atteindre pour être rentable", fontsize=7.2)
ax.text(7.75, yb[0] + 0.45, "Coût pour l'État", fontsize=6.9, color=ENCRE2, fontweight="bold")
axes(ax, grille="x")
ax.spines["left"].set_visible(False)
ax.tick_params(axis="y", length=0)
sauver(fig, "g16_seuil",
       "calculs des auteurs (note8p/calculs/is3_reforme.py, convention de Devereux et Griffith) ; coûts : annexe D.",
       "Machine neuve financée sur fonds propres, durée d'usage de 7 ans, dépréciation 14 % par an, inflation 2 % ;"
       " l'actionnaire exige 5 % réels. Avec la déduction immédiate, l'impôt ne change plus le seuil de rentabilité :"
       " tout projet rentable sans impôt l'est aussi après impôt. Exemple : une machine qui rapporte 5,8 % avant impôt"
       " est abandonnée aujourd'hui comme avec la baisse du taux ; elle est réalisée avec la déduction immédiate.")
out = dict(menages=RES, baisse_naif_points=100 * BAISSE_NAIF,
           foncier=[dict(etat=e[0], dmto=e[1], bati=e[2], sol=e[3], national=e[4]) for e in ETATS],
           seuils=seuil)
(S_ / "trois_etats_v6.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
print(json.dumps(out, ensure_ascii=False, indent=1)[:1500])

# ------------------------------------------------------------------ g17 : terrain nu ou bâti (remplace g6)
G6 = F["g6"]
SOL, BATI = G6["sol"], G6["bati"]
t0 = G6["aujourdhui"]["t_sol"] / 100                       # taxe actuelle, taux unique sur la valeur totale (convention)
k_naif = (com + nat) / com
tn = F["scenarios"][json.loads((D / "parametres.json").read_text(encoding="utf-8"))["scenario_foncier"]]["taux"]["tn_sol"] / 100
CASG = [("Aujourd'hui", t0 * SOL, t0 * (SOL + BATI)),
        ("Naïve :\ntaxe foncière\nrelevée", k_naif * t0 * SOL, k_naif * t0 * (SOL + BATI)),
        ("Notre réforme :\ntaxe sur\nle sol", t0 * SOL + tn * SOL, t0 * (SOL + BATI) + tn * SOL)]
fig, ax = plt.subplots(figsize=(DEMI, 2.9))
for i, (lab, nu, ba) in enumerate(CASG):
    ax.bar(i - 0.2, nu, width=0.38, color=HAUSSE, zorder=2)
    ax.bar(i + 0.2, ba, width=0.38, color=NAIF, zorder=2)
    ax.text(i - 0.2, nu + 60, _fr(round(nu, -1)), ha="center", fontsize=6.6, color=ENCRE2)
    ax.text(i + 0.2, ba + 60, _fr(round(ba, -1)), ha="center", fontsize=6.6, color=ENCRE2)
    ax.annotate("", xy=(i + 0.2, ba), xytext=(i + 0.2, nu), arrowprops=dict(arrowstyle="<->", color=PROP, lw=0.9))
    ax.text(i + 0.45, (nu + ba) / 2, f"+{_fr(round(ba - nu, -1))}", rotation=90, va="center", ha="center", fontsize=6.6,
            color=PROP, fontweight="bold")
ax.set_xticks(range(3))
ax.set_xticklabels([c[0] for c in CASG], fontsize=7)

ax.set_ylim(0, 4300)
ax.set_ylabel("Impôt foncier annuel, €", fontsize=7)
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: _fr(v)))
ax.legend(handles=[Patch(color=HAUSSE, label="Terrain de 200 000 € vide"),
                   Patch(color=NAIF, label="Avec un immeuble de 600 000 €"),
                   plt.Line2D([], [], color=PROP, lw=0.9, label="Impôt dû pour avoir construit")], fontsize=6.6,
          loc="upper center", bbox_to_anchor=(0.45, -0.42), ncol=1)
axes(ax)
sauver(fig, "g17_construire", "calcul illustratif des auteurs (note8p/calculs/figures_v6_trois_etats.py).",
       f"Aujourd'hui : {_fr(100 * t0, 2)} % de la valeur totale du bien (taxe foncière rapportée à la valeur des logements,"
       f" 2025 ; un terrain nu paie aujourd'hui la taxe sur le non-bâti, souvent plus basse). Réforme naïve : la même recette"
       f" de 15 Md€ obtenue en relevant la taxe actuelle (+{_fr(100 * (k_naif - 1))} %). Notre réforme : taxe nationale de"
       f" {_fr(100 * tn, 2)} % sur la seule valeur du sol.")
print("g17", [(c[0].split(chr(10))[0], round(c[1]), round(c[2]), round(c[2] - c[1])) for c in CASG])
