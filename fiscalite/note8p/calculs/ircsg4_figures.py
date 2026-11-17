"""Bloc IR-CSG v4 : figures finales g1, g2, g3, g3b, g11 (note8p/charte.py). Lancer après ircsg4_cas.py :
    python3 note8p/calculs/ircsg4_figures.py
Titres et sources dans le LaTeX (fichiers *_source.tex), jamais dans l'image."""
import json
import sys
from pathlib import Path

import numpy as np

RACINE = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(RACINE / "note8p"), str(Path(__file__).resolve().parent)]
from charte import AUJ, NAIF, PROP, HAUSSE, ENCRE2, PLEINE, plt, axes, sauver, _fr  # noqa: E402
from matplotlib.ticker import FuncFormatter  # noqa: E402
import ircsg3_modele as N  # noqa: E402

J = json.loads((RACINE / "note8p/sorties/ircsg4.json").read_text(encoding="utf-8"))
V3 = json.loads((RACINE / "note8p/sorties/ircsg3.json").read_text(encoding="utf-8"))
S = N.continu(J["bareme"]["points"], J["bareme"]["taux"])
O = N.options()
SZ = 19176.48
keur = FuncFormatter(lambda v, _: _fr(v / 1000) + " k€")
pctf = FuncFormatter(lambda v, _: _fr(v) + " %")
eurf = FuncFormatter(lambda v, _: _fr(v) + " €")
CONV = "Repères : 1 Smic = 19 200 € de revenu après cotisations (21 600 € brut par an, 2025)."
SRC_OF = "OpenFisca-France 176.1 (droit des revenus 2025) ; calculs des auteurs (note8p/calculs/ircsg4_*.py)."


def reperes(ax, xmax, haut):
    for m, lab in ((1, "Smic"), (2, "2"), (3, "3 Smic")):
        if m * SZ < xmax:
            ax.axvline(m * SZ, color="#bbbbbb", lw=0.6, ls=":", zorder=0)
            ax.text(m * SZ, haut, lab, fontsize=6.5, color=ENCRE2, ha="center", va="bottom")


T = J["taux"]
z = np.array(T["z"])

# ------------------------------------------------------------------ g1 : taux moyens
fig, ax = plt.subplots(figsize=(PLEINE, 2.4))
ax.plot(z, T["auj_ta"], color=AUJ, lw=1.8, label="Aujourd'hui (IR, CEHR, CSG, CRDS), sans niche")
ax.plot(z, T["final_ta"], color=PROP, lw=2.2, label="Nouvel impôt")
for zz in (SZ, 2 * SZ, 60e3, 100e3, 200e3):
    i = int(np.argmin(np.abs(z - zz)))
    for k, c, dy in (("auj_ta", AUJ, 1.4), ("final_ta", PROP, -3.2)):
        ax.text(zz, T[k][i] + dy, _fr(T[k][i], 1) + " %", color=c, fontsize=6.5, ha="center")
reperes(ax, 250e3, 44)
ax.set_xlim(0, 250e3)
ax.set_ylim(0, 47)
ax.xaxis.set_major_formatter(keur)
ax.yaxis.set_major_formatter(pctf)
ax.set_xlabel("Revenu annuel après cotisations sociales", fontsize=7.5)
ax.legend(loc="lower right", fontsize=7)
axes(ax)
sauver(fig, "g1_taux_moyens", SRC_OF, "Salarié vivant seul, sans enfant, sans niche ni frais réels. " + CONV)

# ------------------------------------------------------------------ g2 : taux marginaux
fig, ax = plt.subplots(figsize=(PLEINE, 2.5))
ax.plot(z, T["auj_tm"], color=AUJ, lw=1.5, label="Aujourd'hui", drawstyle="steps-post")
_irs = np.array([0.0, 11600.0, 29579.0, 84577.0, 181917.0])
_irt = np.array([0.0, 0.11, 0.30, 0.41, 0.45])
ax.plot(z, 100 * (_irt[np.searchsorted(_irs, z, side="right") - 1] + 0.043), color=NAIF, lw=1.5,
        label="Fusion naïve (barème de l'IR + 4,3 points)", drawstyle="steps-post")
ax.plot(z, T["final_tm"], color=PROP, lw=2.3, label="Nouvel impôt")
for zz, tk in zip(J["bareme"]["points"], J["bareme"]["taux"]):
    y = 100 * tk
    ax.plot(zz, y, "o", color=PROP, ms=3.5)
    ax.text(zz + 3000, y - 4.5, _fr(y, 1) + " %", color=PROP, fontsize=7)
XM = max(280e3, J["bareme"]["points"][-1] + 30e3)
reperes(ax, XM, 56)
ax.set_xlim(0, XM)
ax.set_ylim(0, 60)
ax.xaxis.set_major_formatter(keur)
ax.yaxis.set_major_formatter(pctf)
ax.set_xlabel("Revenu annuel après cotisations sociales", fontsize=7.5)
ax.legend(loc="lower right", fontsize=7)
axes(ax)
sauver(fig, "g2_taux_marginaux", SRC_OF, "Salarié seul : prélèvement sur 100 € de revenu après cotisations en plus. Points :"
       " taux de référence du nouveau barème, reliés en ligne droite. " + CONV)

# ------------------------------------------------------------------ g3 : cas-types nets des niches (€ par mois, + = gain)
C = J["cas_types_nets"]
LIB = [("smic_hs", "Salarié au Smic avec heures sup."), ("milieu", "Salarié seul, 40 000 € brut"),
       ("garde_sans", "Biactifs 2 enfants, sans niche"), ("garde", "Les mêmes, enfants gardés"),
       ("ret_modeste", "Retraité, 14 000 €"), ("cadres", "Cadres 150 000 €, plusieurs niches")]
fig, ax = plt.subplots(figsize=(PLEINE, 2.2))
y = np.arange(len(LIB))[::-1]
for yy, (k, lab) in zip(y, LIB):
    gs, pn, net = -C[k]["gain_systeme_mois"], -C[k]["perte_niches_mois"], -C[k]["net_mois"]
    ax.barh(yy, gs, color=PROP if gs >= 0 else HAUSSE, height=0.6, zorder=2)
    ax.barh(yy, pn, left=gs if gs * pn > 0 else 0, color=NAIF if False else "#d9a77f", height=0.6, zorder=2)
    ax.plot(net, yy, "D", color="black", ms=3.6, zorder=3)
    ax.text(395, yy, ("+" if net > 0.5 else "−" if net < -0.5 else "") + _fr(abs(round(net))) + " €", va="center",
            ha="right", fontsize=7.2, color=ENCRE2, fontweight="bold")
ax.text(395, len(LIB) - 0.35, "Net", ha="right", fontsize=7, color=ENCRE2)
ax.axvline(0, color=ENCRE2, lw=0.7)
ax.set_yticks(y)
ax.set_yticklabels([l for _, l in LIB], fontsize=7.3)
ax.set_xlim(-430, 400)
ax.xaxis.set_major_formatter(eurf)
from matplotlib.patches import Patch  # noqa: E402
from matplotlib.lines import Line2D  # noqa: E402
ax.legend(handles=[Patch(color=PROP, label="Nouveau système : baisse"), Patch(color=HAUSSE, label="Nouveau système : hausse"),
                   Patch(color="#d9a77f", label="Perte des niches"),
                   Line2D([], [], marker="D", color="black", lw=0, ms=3.6, label="Gain net (valeur affichée)")],
          fontsize=6.5, loc="lower center", bbox_to_anchor=(0.45, 1.0), ncol=4)
axes(ax, grille="x")
ax.spines["left"].set_visible(False)
ax.tick_params(axis="y", length=0)
sauver(fig, "g3_cas_types", "OpenFisca-France 176.1 (droit des revenus 2025, réductions et crédits compris, crédits"
       " restitués compris) ; calculs des auteurs (note8p/calculs/ircsg4_cas.py).",
       "Gain net pour le ménage, € par mois, réforme achevée (+ = il paie moins). Garde : 3 500 € par enfant ; aide à"
       " domicile 3 000 € (4 000 € pour la retraitée) ; cadres : dons 2 000 €, emploi à domicile 6 000 €, Pinel gardé"
       " jusqu'à son terme. Aucun frais réel déclaré.")

# ------------------------------------------------------------------ g3b : gains selon le revenu (€ par mois)
Sal, Ret = V3["courbes"]["salarie"], V3["courbes"]["retraite"]
xs = np.array([r["z"] for r in Sal])
gs = np.array([r["auj"] - float(N.impot_z(S, O, [r["z"]])[0]) for r in Sal]) / 12
pe = np.array([r["pension"] for r in Ret])
gr = np.array([r["auj"] - float(N.impot_z(S, O, [r["pension"]])[0]) for r in Ret]) / 12
fig, ax = plt.subplots(figsize=(PLEINE, 2.4))
ax.plot(xs, gs, color=PROP, lw=2.2, label="Salarié seul")
ax.plot(pe, gr, color=HAUSSE, lw=2.0, label="Retraité seul")
for zz in (SZ, 1.5 * SZ, 2 * SZ, 3 * SZ, 100e3):
    v = float(np.interp(zz, xs, gs))
    ax.text(zz, v + 12, ("+" if v > 0 else "−") + _fr(abs(round(v))), color=PROP, fontsize=6.5, ha="center")
for zz in (12e3, 16e3, 30e3, 60e3, 130e3):
    v = float(np.interp(zz, pe, gr))
    ax.text(zz, v - 22, ("+" if v > 0 else "−") + _fr(abs(round(v))), color=HAUSSE, fontsize=6.5, ha="center")
ax.axhline(0, color=ENCRE2, lw=0.6)
reperes(ax, 150e3, 230)
ax.set_xlim(5000, 150e3)
ax.set_ylim(-170, 250)
ax.xaxis.set_major_formatter(keur)
ax.yaxis.set_major_formatter(eurf)
ax.set_xlabel("Revenu annuel après cotisations (salaire net de cotisations, pension brute)", fontsize=7.5)
ax.set_ylabel("Gain, € par mois", fontsize=7)
ax.legend(loc="lower center", bbox_to_anchor=(0.55, 0.02), fontsize=7)
axes(ax)
sauver(fig, "g3b_gains_revenu", SRC_OF, "Hors niches : ni réduction, ni crédit, ni frais réels. Gain = baisse de l'impôt"
       " (IR, CEHR, CSG, CRDS aujourd'hui) ; négatif = hausse. " + CONV)

# ------------------------------------------------------------------ g11 : où vont les ressources
K = J["cascade_categories"]
CB = {c["etape"]: c["Md"] for c in J["cascade_brute"]}
ITEMS = [("Suppression des vraies niches", K["vraies_niches"], "src"),
         ("Pensions imposées comme les salaires", K["alignement_pensions"], "src"),
         ("Impôt individuel : fin du quotient conjugal", K["unite_fiscale"], "src"),
         ("Fin du quotient familial", CB["qf"], "src"),
         ("Assiette avant CSG (fin de la CSG déductible)", K["technique_csg_deductible"], "tec"),
         ("Fin du forfait de 10 % pour frais", K["technique_frais"], "tec"),
         ("Apport des autres réformes (IS, foncier)", K["financement_externe"], "src"),
         ("Franchise de 6 000 € par enfant", K["quotient_familial_vers_franchise"] - CB["qf"], "use"),
         ("Minimum vieillesse sur la pension nette", K["aspa_nette"], "use"),
         ("Contribution sur les hauts revenus intégrée", K["cehr_absorbee"], "use"),
         ("Baisse des taux (nouveau barème)", K["bareme"], "use")]
fig, ax = plt.subplots(figsize=(PLEINE, 2.9))
y = np.arange(len(ITEMS))[::-1]
for yy, (lab, v, t) in zip(y, ITEMS):
    col = {"src": HAUSSE, "tec": "#d9a77f", "use": PROP}[t]
    ax.barh(yy, v, color=col, height=0.62, zorder=2)
    ax.text(v + (1.5 if v >= 0 else -1.5), yy, ("+" if v > 0 else "−") + _fr(abs(v), 1 if abs(v) < 10 else 0), va="center",
            ha="left" if v >= 0 else "right", fontsize=7, color=ENCRE2)
ax.axvline(0, color=ENCRE2, lw=0.7)
ax.set_yticks(y)
ax.set_yticklabels([i[0] for i in ITEMS], fontsize=7.3)
ax.set_xlim(-110, 40)
ax.set_xlabel("Md€ par an (niveau 2025, réforme achevée, avant réaction des comportements)", fontsize=7)
axes(ax, grille="x")
ax.spines["left"].set_visible(False)
ax.tick_params(axis="y", length=0)
sauver(fig, "g11_cascade", "calculs des auteurs (modèle de foyers calé sur l'IRCOM des revenus 2024 porté en 2025 ; CPO 2026 ;"
       " DGFiP Statistiques n° 41 ; Voies et moyens PLF 2026).",
       "Ocre : ressources ; ocre clair : ajustements techniques de la fusion ; bleu : emplois. Le solde est nul : la fusion est à recette constante. Décomposition séquentielle, avant réaction des comportements (l'ordre change la taille de chaque ligne, pas le total). Vraies niches : coût des"
       " réductions, crédits et exonérations supprimés (dont 3,3 Md€ de revenus aujourd'hui exonérés, comme l'épargne"
       " salariale) ; les avantages gardés (engagements Pinel, revenus de source étrangère, invalidité, dépendance) et"
       " l'écart inexpliqué du modèle ne sont pas comptés. Forfait : frais réels gardés, en hausse.")
print("figures écrites")
