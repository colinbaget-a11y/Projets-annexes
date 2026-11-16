"""Bloc IR-CSG v3 : figures de travail (note8p/figures/travail/, A à F) et figures finales (g1, g2, g3, g3b).
python3 note8p/calculs/ircsg3_figures.py, après ircsg3_proposition.py."""
import json
import re
import sys
from pathlib import Path

import numpy as np

RACINE = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RACINE / "note8p"))
from charte import AUJ, NAIF, PROP, HAUSSE, ENCRE2, PLEINE, DEMI, plt, axes, sauver, _fr  # noqa: E402
from matplotlib.ticker import FuncFormatter  # noqa: E402

D = json.loads((RACINE / "note8p/sorties/ircsg3.json").read_text(encoding="utf-8"))
TRAV = RACINE / "note8p/figures/travail"
TRAV.mkdir(exist_ok=True)
SZ = 19176.48
keur = FuncFormatter(lambda v, _: _fr(v / 1000) + " k€")
pctf = FuncFormatter(lambda v, _: _fr(v) + " %")
eurf = FuncFormatter(lambda v, _: _fr(v) + " €")
CONV = "Repères : 1 Smic = 19 200 € de revenu après cotisations (21 600 € brut par an, 2025) ; 1,5, 2 et 3 Smic : 28 800, 38 400 et 57 500 €."
C4C = "#6a9a5b"


def trav(fig, nom, note):
    fig.savefig(TRAV / f"{nom}.pdf")
    fig.savefig(TRAV / f"{nom}.png", dpi=150)
    (TRAV / f"{nom}_note.txt").write_text(note + "\n", encoding="utf-8")
    plt.close(fig)


def reperes(ax, xmax, haut, brut=False):
    k = 12 * 0.0 + (21622.0 / 12 if brut else SZ)
    for m, lab in ((1, "Smic"), (1.5, "1,5"), (2, "2"), (3, "3 Smic")):
        x = m * k
        if x < xmax and not (xmax > 150e3 and m == 1.5):
            ax.axvline(x, color="#bbbbbb", lw=0.6, ls=":", zorder=0)
            ax.text(x, haut, lab, fontsize=6.5, color=ENCRE2, ha="center", va="bottom")


T = D["taux"]
z = np.array(T["z"])
SER = [("auj", "Aujourd'hui", AUJ, 1.4, "-"), ("ancien_recale", "Ancienne proposition (recalée)", NAIF, 1.4, "--"),
       ("C4_precoce48", "Continu, montée précoce", C4C, 1.3, "-"), ("C3_plafond50", "Continu, plafond 50 %", HAUSSE, 1.2, "-"),
       ("C2_plafond48", "Recommandé (plafond 48 %)", PROP, 2.2, "-")]

# ------------------------------------------------------------------ A : taux marginaux (zoom et vue large)
for nom, xmax, ymax in (("A1_taux_marginaux_zoom", 80e3, 50), ("A2_taux_marginaux_large", 400e3, 60)):
    fig, ax = plt.subplots(figsize=(PLEINE, 2.6))
    for k, lab, c, lw, ls in SER:
        ax.plot(z, T[f"{k}_tm"], color=c, lw=lw, ls=ls, label=lab, drawstyle="steps-post" if k in ("auj", "ancien_recale") else "default")
    reperes(ax, xmax, ymax - 3)
    ax.set_xlim(0, xmax)
    ax.set_ylim(0, ymax)
    ax.xaxis.set_major_formatter(keur)
    ax.yaxis.set_major_formatter(pctf)
    ax.set_xlabel("Revenu annuel après cotisations sociales, par adulte", fontsize=7.5)
    ax.legend(fontsize=6.5, loc="lower right", ncol=2)
    axes(ax)
    trav(fig, nom, "Salarié seul ; prélèvement sur 100 € de revenu après cotisations en plus. " + CONV)

# ------------------------------------------------------------------ B : taux moyens
fig, ax = plt.subplots(figsize=(PLEINE, 2.6))
for k, lab, c, lw, ls in SER:
    ax.plot(z, T[f"{k}_ta"], color=c, lw=lw, ls=ls, label=lab)
reperes(ax, 200e3, 40)
ax.set_xlim(0, 200e3)
ax.set_ylim(0, 43)
ax.xaxis.set_major_formatter(keur)
ax.yaxis.set_major_formatter(pctf)
ax.legend(fontsize=6.5, loc="lower right", ncol=2)
axes(ax)
trav(fig, "B_taux_moyens", "Salarié seul ; impôt / revenu après cotisations. " + CONV)

# ------------------------------------------------------------------ C : salarié seul selon le brut mensuel
S = D["courbes"]["salarie"]
bm = np.array([r["brut_mensuel"] for r in S])
fig, axs = plt.subplots(1, 2, figsize=(PLEINE, 2.5))
for k, lab, c, lw in (("ancien_recale", "Ancienne proposition (recalée)", NAIF, 1.4), ("C4_precoce48", "Montée précoce", C4C, 1.2),
                      ("C2_plafond48", "Recommandé", PROP, 2.0), ("C2_F6", "Recommandé + 6 Md€", PROP, 1.0)):
    v = np.array([r[k] for r in S])
    axs[0].plot(bm, -v / 12, color=c, lw=lw, label=lab, ls=":" if k == "C2_F6" else "-")
    axs[1].plot(bm, -100 * v / np.array([r["z"] for r in S]), color=c, lw=lw, ls=":" if k == "C2_F6" else "-")
for a, yl in ((axs[0], "Gain, € par mois"), (axs[1], "Gain, % du revenu après cotisations")):
    a.axhline(0, color=ENCRE2, lw=0.6)
    reperes(a, 25000, a.get_ylim()[1], brut=True)
    a.set_xlabel("Salaire brut mensuel", fontsize=7)
    a.set_title(yl, fontsize=7.5, color=ENCRE2)
    a.xaxis.set_major_formatter(eurf)
    a.set_xlim(1000, 25000)
    axes(a)
axs[0].set_xscale("log")
axs[1].set_xscale("log")
for a in axs:
    a.set_xticks([1500, 3000, 5000, 10000, 20000])
    a.xaxis.set_major_formatter(eurf)
    a.tick_params(axis="x", labelsize=6)
axs[0].legend(fontsize=6, loc="upper left")
trav(fig, "C_gains_salarie", "Salarié seul sans enfant ; gain = baisse de l'impôt (IR, CEHR, CSG, CRDS aujourd'hui) ; échelle"
     " logarithmique. Repères en brut mensuel (Smic 1 802 €).")

# ------------------------------------------------------------------ D : retraité seul selon la pension
S = D["courbes"]["retraite"]
pe = np.array([r["pension"] for r in S])
fig, ax = plt.subplots(figsize=(PLEINE, 2.5))
for k, lab, c, lw in (("ancien_recale", "Ancienne proposition (recalée)", NAIF, 1.4), ("C4_precoce48", "Montée précoce", C4C, 1.2),
                      ("C2_plafond48", "Recommandé", PROP, 2.0)):
    ax.plot(pe, [r[k] for r in S], color=c, lw=lw, label=lab)
ax.axhline(0, color=ENCRE2, lw=0.6)
ax.set_xlim(6000, 150000)
ax.xaxis.set_major_formatter(keur)
ax.yaxis.set_major_formatter(eurf)
ax.set_xlabel("Pension annuelle", fontsize=7.5)
ax.set_ylabel("Variation de l'impôt, € par an", fontsize=7)
ax.legend(fontsize=6.5)
axes(ax)
trav(fig, "D_retraite_seul", "Retraité seul de plus de 65 ans ; + = hausse d'impôt.")

# ------------------------------------------------------------------ E : familles (sans et avec niches)
FAM = D["familles_courbes"]
fig, axs = plt.subplots(1, 2, figsize=(PLEINE, 2.6), gridspec_kw=dict(width_ratios=[1.1, 1]))
for prof, lab, c in (("couple_2enf", "Biactif, 2 enf.", PROP), ("couple_2enf_mono", "Mono-actif, 2 enf.", HAUSSE),
                     ("couple_3enf", "Biactif, 3 enf.", C4C), ("couple_3enf_mono", "Mono-actif, 3 enf.", NAIF),
                     ("parent_isole_2enf", "Parent isolé, 2 enf.", AUJ)):
    r = FAM[prof]
    axs[0].plot([x["brut"] for x in r], [x["C2_plafond48"] / 12 for x in r], color=c, lw=1.6, marker="o", ms=2.5, label=lab)
axs[0].axhline(0, color=ENCRE2, lw=0.6)
axs[0].xaxis.set_major_formatter(keur)
axs[0].yaxis.set_major_formatter(eurf)
axs[0].set_xlabel("Revenu brut du ménage", fontsize=7)
axs[0].set_title("Variation, € par mois (sans niche)", fontsize=7.5, color=ENCRE2)
axs[0].legend(fontsize=5.8, loc="upper left")
axes(axs[0])
NI = D["familles_niches"]
sel = [0, 1, 2, 5, 7, 8]
lab = ["Biactif 2 enf., garde + domicile", "Le même, sans niche", "Cadres 2 enf., domicile + dons",
       "Biactif 4 enf., garde", "Retraité 30 k€, domicile", "Retraité 30 k€, sans niche"]
y = np.arange(len(sel))[::-1]
for yy, i in zip(y, sel):
    r = NI[i]
    for off, v, c in ((0.22, r["perte_avantages"], HAUSSE), (0.0, r["variation_assiette"], NAIF), (-0.22, r["gain_bareme"], PROP)):
        axs[1].barh(yy + off, v / 12, color=c, height=0.2)
    axs[1].plot(r["net"] / 12, yy, "kD", ms=3.5)
    axs[1].text(max(r["perte_avantages"], r["variation_assiette"], 0) / 12 + 15, yy + 0.22,
                f"net {'+' if r['net'] > 0 else ''}{_fr(r['net'] / 12)} €", fontsize=5.8, va="center")
axs[1].set_yticks(y)
axs[1].set_yticklabels(lab, fontsize=6)
axs[1].axvline(0, color=ENCRE2, lw=0.6)
axs[1].set_title("Niches, assiette, barème (losange : net), € par mois", fontsize=7.5, color=ENCRE2)
axs[1].xaxis.set_major_formatter(eurf)
axes(axs[1], grille="x")
trav(fig, "E_familles", "Gauche : couples mariés ou pacsés (biactifs 60/40), sans niche. Droite : barres empilées, ocre = perte"
     " des réductions et crédits, bleu clair = élargissement de l'assiette (quotients, CSG déductible, forfait de 10 %),"
     " bleu foncé = nouveau barème et franchise ; trait = variation nette.")

# ------------------------------------------------------------------ F : cascade
CA = D["cascade_final"]
lab_c = {"observe": "Charge actuelle", "niches": "Réductions, crédits\net exonérations", "abatpen": "Abattement\n10 % pensions",
         "age": "Abattement\npersonnes âgées", "csg_ret": "CSG des\nretraités", "conjugal": "Quotient\nconjugal",
         "qf": "Quotient\nfamilial", "csg_ded": "CSG\ndéductible", "forfait": "Forfait 10 %\n(frais réels gardés)",
         "cehr": "CEHR", "invalidite": "Invalidité", "franchise": "Franchise\nenfants", "bareme": "Nouveau\nbarème"}
lab_c = {k: v.replace("\n", " ") for k, v in lab_c.items()}
rows = [r for r in CA if r["etape"] != "net"]
fig, ax = plt.subplots(figsize=(PLEINE, 3.4))
y, cum = len(rows), 0.0
for r in rows:
    v = r["Md"]
    if r["etape"] == "observe":
        ax.barh(y, v, color=AUJ, height=0.7)
        cum = v
        ax.text(v + 2, y, _fr(v), va="center", fontsize=6.5)
    else:
        ax.barh(y, v, left=cum, color=HAUSSE if v > 0 else PROP, height=0.7)
        ax.text(max(cum, cum + v) + 2, y, ("+" if v > 0 else "") + _fr(v, 1 if abs(v) < 1 else 0), va="center", fontsize=6.5)
        cum += v
    y -= 1
ax.barh(y, cum, color=PROP, height=0.7)
ax.text(cum + 2, y, _fr(cum), va="center", fontsize=6.5)
ax.set_yticks(range(len(rows), y - 1, -1))
ax.set_yticklabels([lab_c[r["etape"]] for r in rows] + ["Nouvel impôt"], fontsize=6.8)
ax.set_xlim(150, 370)
ax.set_xlabel("Md€ (2025)", fontsize=7)
axes(ax, grille="x")
trav(fig, "F_cascade_recettes", "Mesures introduites une à une dans cet ordre (statique, avant réaction) ; ocre = recette,"
     " bleu = coût. « Réductions, crédits et exonérations » : écart entre le droit 2025 simulé sans niche et la charge"
     " observée (IRCOM, impôt net).")

# ================================================================== figures finales
# g1 : taux moyens, aujourd'hui et recommandé
fig, ax = plt.subplots(figsize=(PLEINE, 2.4))
ax.plot(z, T["auj_ta"], color=AUJ, lw=1.8, label="Aujourd'hui (IR, CEHR, CSG, CRDS)")
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
sauver(fig, "g1_taux_moyens", "OpenFisca-France 176.1 (droit des revenus 2025) ; calculs des auteurs (note8p/calculs/ircsg3_*.py).",
       "Salarié vivant seul, sans enfant ni niche. " + CONV)

# g2 : taux marginaux
fig, ax = plt.subplots(figsize=(PLEINE, 2.5))
ax.plot(z, T["auj_tm"], color=AUJ, lw=1.5, label="Aujourd'hui", drawstyle="steps-post")
_irs = np.array([0.0, 11600.0, 29579.0, 84577.0, 181917.0]); _irt = np.array([0.0, 0.11, 0.30, 0.41, 0.45])
_naive = 100 * (_irt[np.searchsorted(_irs, np.asarray(z), side="right") - 1] + 0.043)
ax.plot(z, _naive, color=NAIF, lw=1.5, label="Fusion naïve (barème de l'IR + 4,3 points)", drawstyle="steps-post")
ax.plot(z, T["final_tm"], color=PROP, lw=2.3, label="Nouvel impôt")
for zz, tk in zip(D["final"]["points"], D["final"]["taux"]):
    lab = _fr(100 * tk, 1 if abs(100 * tk - round(100 * tk)) > 0.05 else 0) + " %"
    ax.plot(zz, float(np.interp(zz, z, T["final_tm"])) if zz else 2, "o", color=PROP, ms=3.5)
    ax.text(zz + 3000, (float(np.interp(zz, z, T["final_tm"])) if zz else 2) - 4.5, lab, color=PROP, fontsize=7)
reperes(ax, 280e3, 56)
ax.set_xlim(0, 280e3)
ax.set_ylim(0, 60)
ax.xaxis.set_major_formatter(keur)
ax.yaxis.set_major_formatter(pctf)
ax.set_xlabel("Revenu annuel après cotisations sociales", fontsize=7.5)
ax.legend(loc="lower right", fontsize=7)
axes(ax)
sauver(fig, "g2_taux_marginaux", "OpenFisca-France 176.1 (aujourd'hui, droit des revenus 2025) ; calculs des auteurs.",
       "Salarié seul : prélèvement sur 100 € de revenu après cotisations en plus. Points : taux de référence du nouveau"
       " barème, reliés en ligne droite. " + CONV)

# g3 : cas-types, € par mois
C = D["final"]["cas_types"]
LIB = [("jeune_smic", "Salarié au Smic"), ("sal_2000", "Salarié à 2 000 € net"), ("couple2_60", "Couple biactif, 2 enfants, 60 k€"),
       ("nomb3_60", "Couple biactif, 3 enfants, 60 k€"), ("pi2_smic", "Parent isolé, 2 enfants, Smic"),
       ("mono2_60", "Couple mono-actif, 2 enfants, 60 k€"), ("cadre120", "Cadre seul, 120 k€ brut"),
       ("ret_16", "Retraité seul, 16 000 €"), ("retc_60", "Couple de retraités, 60 000 €")]
vals = [C[k]["delta"] / 12 for k, _ in LIB]
fig, ax = plt.subplots(figsize=(PLEINE, 2.6))
y = np.arange(len(LIB))[::-1]
ax.barh(y, vals, color=[HAUSSE if v > 0 else PROP for v in vals], height=0.62, zorder=2)
ax.axvline(0, color=ENCRE2, lw=0.7)
for yy, v in zip(y, vals):
    ax.text(v + (6 if v >= 0 else -6), yy, ("+" if v > 0 else "") + _fr(round(v)) + " €", va="center",
            ha="left" if v >= 0 else "right", fontsize=7, color=ENCRE2)
ax.set_yticks(y)
ax.set_yticklabels([l for _, l in LIB], fontsize=7.5)
ax.set_xlim(-300, 160)
ax.xaxis.set_major_formatter(eurf)
axes(ax, grille="x")
ax.spines["left"].set_visible(False)
ax.tick_params(axis="y", length=0)
sauver(fig, "g3_cas_types", "OpenFisca-France 176.1 (charge d'aujourd'hui : IR, CEHR, CSG, CRDS, droit 2025) ; calculs des auteurs.",
       "Variation de l'impôt, € par mois, réforme achevée ; aucune niche ; couples mariés ou pacsés (biactifs 60/40) ;"
       " retraités de plus de 65 ans.")

# g3b : gains selon le revenu, salariés et retraités (€ par mois)
S, Rr = D["courbes"]["salarie"], D["courbes"]["retraite"]
fig, ax = plt.subplots(figsize=(PLEINE, 2.4))
xs = np.array([r["z"] for r in S])
ax.plot(xs, [-r["final"] / 12 for r in S], color=PROP, lw=2.2, label="Salarié seul")
ax.plot([r["pension"] for r in Rr], [-r["final"] / 12 for r in Rr], color=HAUSSE, lw=2.0, label="Retraité seul")
for zz in (SZ, 1.5 * SZ, 2 * SZ, 3 * SZ, 100e3):
    v = -float(np.interp(zz, xs, [r["final"] for r in S])) / 12
    ax.text(zz, v + 12, ("+" if v > 0 else "") + _fr(round(v)), color=PROP, fontsize=6.5, ha="center")
for zz in (12e3, 16e3, 30e3, 60e3, 100e3):
    v = -float(np.interp(zz, [r["pension"] for r in Rr], [r["final"] for r in Rr])) / 12
    ax.text(zz, v - 22, ("+" if v > 0 else "") + _fr(round(v)), color=HAUSSE, fontsize=6.5, ha="center")
ax.axhline(0, color=ENCRE2, lw=0.6)
reperes(ax, 150e3, 285)
ax.set_xlim(5000, 150e3)
ax.set_ylim(-160, 300)
ax.xaxis.set_major_formatter(keur)
ax.yaxis.set_major_formatter(eurf)
ax.set_xlabel("Revenu annuel après cotisations (salaire net de cotisations, pension brute)", fontsize=7.5)
ax.set_ylabel("Gain, € par mois", fontsize=7)
ax.legend(loc="upper left", fontsize=7)
axes(ax)
sauver(fig, "g3b_gains_revenu", "OpenFisca-France 176.1 (droit des revenus 2025) ; calculs des auteurs.",
       "Gain = baisse de l'impôt (IR, CEHR, CSG, CRDS aujourd'hui) ; négatif = hausse. " + CONV)
print("figures écrites")
