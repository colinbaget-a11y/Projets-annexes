"""Lecture du barème fusionné avec les outils de la taxation optimale.

Lancer depuis fiscalite/ : python3 ir_csg/optimal.py  ->  sorties/optimal.txt, figure ircsg_optimal

1. Paramètre de Pareto de la distribution de l'assiette brute (foyers), local α(z) = z h(z) / (1 − H(z))
   et a(z*) = E[z | z > z*] / (E[z | z > z*] − z*), sur la distribution reconstituée de l'IRCOM 2024.
2. Taux supérieur de Saez (2001) / Piketty-Saez (2013) : τ = (1 − g) / (1 − g + a e) ; taux
   maximisant la recette 1 / (1 + a e) ; poids social implicite g d'un taux donné.
3. Inverse optimum (Saez 2001, Bourguignon-Spadaro 2012, Lockwood-Weinzierl 2016) sans effet revenu :
   poids social moyen au-dessus de z, Ḡ(z) = 1 − e(z) · T'(z) / (1 − T'(z)) · α(z), pour le système
   actuel (taux marginaux OpenFisca des actifs) et pour le barème E.
4. Bien-être à la Atkinson (1970) : à recette égale et revenus avant impôt inchangés, la dominance de
   Lorenz du revenu après impôt équivaut à un bien-être plus élevé pour toute fonction de bien-être
   social utilitariste à utilité concave ; indices d'Atkinson pour ε = 0,5, 1, 2.
"""
import os
import sys
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE), str(HERE.parent)]
import ir_csg as m  # noqa: E402
from graphiques import BLEU, GRIS, INK, OCRE, fin, grille, panneau, plt, titre  # noqa: E402

lignes = []


def p(*a):
    s = " ".join(str(v) for v in a)
    print(s)
    lignes.append(s)


x, f = m.distribution()
cible, B, sc = m.baremes(x, f)
f = f.sort_values("base").reset_index(drop=True)
z, w = f.base.values, f.poids.values
W = w.sum()
lab = np.interp(z, (x.assiette * 1e9 / x.foyers).values, x.part_trav.values)   # part du travail


# ------------------------------------------------------------------ 1. Pareto
def a_seuil(zs):
    sel = z > zs
    zm = np.average(z[sel], weights=w[sel])
    return zm / (zm - zs), w[sel].sum() / W, np.average(lab[sel], weights=w[sel])


grille_z = np.exp(np.linspace(np.log(8e3), np.log(1.2e6), 120))
lz = np.log(z)
bw = 0.25                                                     # lissage en log (noyau gaussien) : la distribution intra-tranche est reconstituée, on ne lit que les grandes tendances
dens_log = np.array([np.sum(w * np.exp(-0.5 * ((lz - np.log(g)) / bw) ** 2)) for g in grille_z])
dens_log /= W * bw * np.sqrt(2 * np.pi)                       # densité de log z
H = np.array([w[z <= g].sum() / W for g in grille_z])
alpha_rec = dens_log / np.clip(1 - H, 1e-6, None)             # z h(z) / (1 − H(z)) = densité de log z / (1 − H)
# Au-delà de 150 k€, la reconstitution comprime la distribution de l'assiette (chaque tranche de RFR
# reçoit la composition moyenne travail / capital de la tranche, alors qu'elle mêle cadres très bien
# payés et rentiers) : α y est surestimé (≈ 4,4 vers 200-300 k€). On y retient a = 2,1, l'estimation
# de Cabannes, Houdré et Landais (2014) pour le haut de la distribution française.
A_HAUT = 2.1
alpha = np.where(grille_z > 150e3, A_HAUT, alpha_rec)

p("=== 1. Paramètre de Pareto de l'assiette brute par foyer (IRCOM 2024 reconstitué)")
for zs in [14e3, 50e3, 90e3, 150e3, 250e3, 500e3]:
    a, part, l = a_seuil(zs)
    p(f"z* = {zs/1e3:5.0f} k€ : a = {a:4.2f} ; foyers au-dessus {100*part:5.2f} % ; part du travail {100*l:3.0f} %")

# ------------------------------------------------------------------ 2. taux supérieurs
p("\n=== 2. Taux supérieurs (Saez) : τ = (1 − g)/(1 − g + a e) ; e effectif = e × part du travail")
for zs, tau in [(120e3, 0.40), (250e3, 0.49)]:
    a_rec, _, l = a_seuil(zs)
    a = A_HAUT
    p(f"(a reconstitué au-dessus de {zs/1e3:.0f} k€ : {a_rec:.2f} ; retenu : {a})")
    for e in [0.25, 0.51]:
        ee = e * l
        laffer = 1 / (1 + a * ee)
        g = 1 - a * ee * tau / (1 - tau)
        # coin fiscal total : les autres prélèvements non contributifs w s'ajoutent, (1 − τ_tot) = (1 − τ)(1 − w)
        tot = [1 - (1 - tau) * (1 - wv) for wv in (0.10, 0.20)]
        g_tot = [1 - a * ee * t_ / (1 - t_) for t_ in tot]
        p(f"au-dessus de {zs/1e3:.0f} k€, taux {100*tau:.0f} %, e = {e} (effectif {ee:.2f}), a = {a:.2f} :"
          f" taux maximisant la recette {100*laffer:.0f} % ; poids implicite g = {g:.2f}"
          f" (avec 10 / 20 points d'autres prélèvements : coin {100*tot[0]:.0f} / {100*tot[1]:.0f} %, g = {g_tot[0]:.2f} / {g_tot[1]:.2f})")
p("Dans la bande à taux unique t, la formule du taux linéaire t = (1 − ḡ)/(1 − ḡ + e) donne ḡ = 1 − e t/(1 − t) :")
tE = sc["E_franchise_taux_unique"][1][1]
for e in [0.25, 0.33]:
    p(f"  e = {e} : ḡ = {1 - e * tE / (1 - tE):.2f} pour t = {100*tE:.1f} %")

# ------------------------------------------------------------------ 3. inverse optimum
of = pd.read_csv(HERE / "sorties/marges_openfisca.csv")
of = of[~of.profil.str.startswith("retrait")]
tm_act = np.median([np.interp(grille_z, g.assiette, g.taux_marginal.clip(upper=0.6)) for _, g in of.groupby("profil")], axis=0)
sE, tE_ = sc["E_franchise_taux_unique"]
tm_E = m.taux_marginal(grille_z, sE, tE_)
lab_g = np.interp(grille_z, z, lab)
p("\n=== 3. Inverse optimum : Ḡ(z) = 1 − e·part_travail·T'/(1 − T')·α(z)")
G = {}
for e in [0.25, 0.5]:
    for nom, tm in [("actuel", tm_act), ("E", tm_E)]:
        G[(nom, e)] = 1 - e * lab_g * tm / (1 - tm) * alpha
for zs in [20e3, 40e3, 70e3, 100e3, 140e3, 200e3, 300e3, 600e3]:
    i = np.argmin(abs(grille_z - zs))
    p(f"z = {zs/1e3:4.0f} k€ : α = {alpha[i]:4.2f} (reconstitué {alpha_rec[i]:4.2f}) ; T' actuel {100*tm_act[i]:4.1f} %, E {100*tm_E[i]:4.1f} % ;"
      f" Ḡ (e = 0,25) actuel {G[('actuel', .25)][i]:5.2f}, E {G[('E', .25)][i]:5.2f} ;"
      f" Ḡ (e = 0,5) actuel {G[('actuel', .5)][i]:5.2f}, E {G[('E', .5)][i]:5.2f}")
for k, v in G.items():
    sel = grille_z < 1e6
    p(f"{k} : min Ḡ = {v[sel].min():.2f} (à {grille_z[sel][v[sel].argmin()]/1e3:.0f} k€) ;"
      f" Ḡ négatif (barème non parétien) : {'oui' if (v[sel] < 0).any() else 'non'}")

# ------------------------------------------------------------------ 4. Atkinson
p("\n=== 4. Indices d'Atkinson du revenu après IR + CSG (tranches IRCOM, même revenu moyen)")
pop, ass = x.foyers.values, x.assiette.values
y0 = (ass - x.charge.values) * 1e9 / pop
fE = f.copy()
fE["n"] = fE.poids * m.impot(fE.base, sE, tE_) / 1e9
nouv = fE.groupby("tranche", sort=False).n.sum().reindex(x.tranche).values
y1 = (ass - nouv) * 1e9 / pop


def atkinson(y, eps):
    mu = np.average(y, weights=pop)
    if eps == 1:
        return 1 - np.exp(np.average(np.log(y), weights=pop)) / mu
    return 1 - np.average(y ** (1 - eps), weights=pop) ** (1 / (1 - eps)) / mu


for eps in [0.5, 1, 2]:
    p(f"ε = {eps} : actuel {atkinson(y0, eps):.4f} ; E {atkinson(y1, eps):.4f}")

(HERE / "sorties/optimal.txt").write_text("\n".join(lignes) + "\n", encoding="utf-8")

# ------------------------------------------------------------------ figure
fig, (a1, a2) = plt.subplots(1, 2, figsize=(9.2, 3.9))
a1.plot(grille_z / 1e3, 100 * tm_act, color=INK, lw=1.8, label="Actuel (IR + CSG, actifs)")
a1.plot(grille_z / 1e3, 100 * tm_E, color=BLEU, lw=2.2, label="Barème E")
a1.set_xscale("log")
a1.set_xticks([10, 20, 50, 100, 200, 500, 1000])
a1.set_xticklabels(["10", "20", "50", "100", "200", "500", "1 000"])
a1.set_ylabel("Taux marginal (%)")
a1.set_xlabel("Assiette brute du foyer (k€, échelle log)")
grille(a1)
a1.legend(loc="upper left", fontsize=8)
for (nom, e), v in G.items():
    c = INK if nom == "actuel" else BLEU
    a2.plot(grille_z / 1e3, v, color=c, lw=1.8 if e == 0.25 else 1.2, ls="-" if e == 0.25 else "--",
            label=f"{'Actuel' if nom == 'actuel' else 'E'}, e = {str(e).replace('.', ',')}")
a2.axhline(0, color=GRIS, lw=0.8)
a2.set_xscale("log")
a2.set_xticks([10, 20, 50, 100, 200, 500, 1000])
a2.set_xticklabels(["10", "20", "50", "100", "200", "500", "1 000"])
a2.set_ylim(-0.6, 1.1)
a2.set_xlabel("Assiette brute du foyer (k€, échelle log)")
grille(a2)
a2.legend(loc="lower left", fontsize=7.5)
panneau(a2, "Poids social moyen implicite au-dessus de z")
titre(a1, "Ce que les deux barèmes supposent sur les préférences sociales",
      "Inverse optimum à la Saez : Ḡ(z) = 1 − e × part du travail × T'/(1 − T') × α(z)")
fig.subplots_adjust(bottom=0.2, wspace=0.28)
fin(fig, "ircsg_optimal", "DGFiP, IRCOM revenus 2024 ; OpenFisca-France ; calculs des auteurs.",
    "Note : Ḡ(z) est le poids social moyen, rapporté à la valeur d'un euro public, que la société doit"
    " accorder aux foyers dont l'assiette dépasse z pour que le barème soit optimal (Saez, 2001, sans"
    " effet revenu). Un Ḡ négatif signale un taux au-delà du maximum de recette. α(z) = z h(z)/(1 − H(z))"
    " est calculé sur la distribution reconstituée de l'assiette brute jusqu'à 150 000 €, et fixé à 2,1"
    " au-delà (Cabannes, Houdré et Landais, 2014) ; seule la part de l'assiette qui vient du travail"
    " réagit au taux.")
