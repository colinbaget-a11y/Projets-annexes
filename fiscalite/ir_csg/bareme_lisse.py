"""Barème lisse : un taux marginal qui monte en ligne droite, sans marche.

Lancer depuis fiscalite/ : python3 ir_csg/bareme_lisse.py  ->  sorties/bareme_lisse.txt et
sorties/bareme_lisse_balayage.csv

Logique « taxation optimale au premier ordre » : parmi les barèmes de la famille, on cherche celui
qui rapporte la recette actuelle (213 Md€) avec le plus faible coût d'efficacité, sous deux
garde-fous distributifs : aucun décile de foyers ne voit sa charge moyenne varier de plus de 800 €
par an, et les déciles 7 à 10 ne paient pas plus de 0,3 point de revenu de plus qu'aujourd'hui.

Famille : 0 % jusqu'à une franchise F ; au-delà, le taux marginal monte en ligne droite de t0 (en F)
à t1 (en z1), puis de t1 à t2 (en z2), et reste à t2 au-delà. t1 est calé sur la recette.

Coût d'efficacité (approximation de Harberger) : somme sur les foyers de ½ · e · z · τ² / (1 − τ),
avec τ le taux marginal, z l'assiette et e l'élasticité du revenu imposable (Sicsic, 2022 : 0,22 /
0,33 / 0,51 selon le rang) multipliée par la part de l'assiette qui vient du travail (les pensions ne
réagissent pas). C'est un ordre de grandeur de la perte de revenu taxable due aux réactions.

Familles : la répartition des couples et des enfants entre tranches n'est pas publiée. Hypothèse :
part de couples logistique en log du RFR, calée sur les totaux 2042 (13,05 millions de couples
mariés ou pacsés, 17,2 millions d'enfants à charge ou rattachés), enfants répartis comme les couples
plus 0,15 enfant par foyer de personne seule.
"""
import itertools
import sys
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE), str(HERE.parent)]
import ir_csg as m  # noqa: E402

x, f = m.distribution()
CIBLE = x.charge.sum()
_, TAU0 = m.comportement(x, f.copy(), {"A": ([0.0], [0.1])})
f = f.sort_values("base").reset_index(drop=True)
Z, W = f.base.values, f.poids.values
Q = np.cumsum(W) / W.sum()
DEC = np.minimum((Q * 10).astype(int), 9)
LAB = f.part_trav.values
E = np.where(Q < 0.5, 0.22, np.where(Q < 0.9, 0.33, 0.51)) * LAB
RATE_K = dict(zip(x.tranche, (x.charge / x.assiette).values))
CUR = Z * f.tranche.map(RATE_K).values             # charge actuelle, proportionnelle dans la tranche
TAU_CUR = f.tranche.map(TAU0).values
# enfants : mineurs à charge (0CF, 15,15 M) + majeurs rattachés (0DJ, 2,01 M) + moitié des enfants en
# résidence alternée (0CH, 1,69 M / 2)
COUPLES, ENFANTS = 13.05e6, 18.0e6


def cout(tm):
    return (W * 0.5 * E * Z * tm ** 2 / (1 - tm)).sum() / 1e9


def cout_familial(tm_fn, fr_adulte=None, abat_enfant=None):
    """Coût d'efficacité de la version 1 : taux marginal pris sur l'assiette après abattements, séparément
    pour les personnes seules et les couples de chaque tranche."""
    fr_adulte = FR_ADULTE if fr_adulte is None else fr_adulte
    abat_enfant = ABAT_ENFANT if abat_enfant is None else abat_enfant
    zc = np.clip(Z - N_ENF * abat_enfant, 0, None)
    d = lambda tm: 0.5 * E * Z * tm ** 2 / (1 - tm)  # noqa: E731
    return (W * ((1 - S_COUPLE) * d(tm_fn(zc)) + S_COUPLE * d(tm_fn(np.clip(zc - fr_adulte, 0, None))))).sum() / 1e9


def famille(F, t0, z1, t1, z2, t2):
    """Renvoie (taux marginal, impôt) comme fonctions de l'assiette."""
    def tm(v):
        v = np.asarray(v, float)
        return np.where(v < F, 0.0, np.interp(v, [F, z1, z2], [t0, t1, t2]))

    def T(v):
        v = np.asarray(v, float)
        u = np.clip(v - F, 0, None)
        L1 = z1 - F
        a = np.minimum(u, L1)
        b = np.clip(u - L1, 0, z2 - z1)
        return (t0 * a + (t1 - t0) * a ** 2 / (2 * L1) + t1 * b + (t2 - t1) * b ** 2 / (2 * (z2 - z1))
                + t2 * np.clip(v - z2, 0, None))
    return tm, T


def cale(F, t0, z1, z2, t2, impot_foyer=None):
    """t1 tel que la recette soit la cible ; impot_foyer(T) permet d'appliquer une règle familiale."""
    lo, hi = 0.0, 0.7
    for _ in range(60):
        t1 = (lo + hi) / 2
        _, T = famille(F, t0, z1, t1, z2, t2)
        n = impot_foyer(T) if impot_foyer else T(Z)
        lo, hi = (t1, hi) if (W * n).sum() / 1e9 < CIBLE else (lo, t1)
    return (lo + hi) / 2


def deciles(nouv):
    d = pd.DataFrame({"dec": DEC + 1, "w": W, "z": Z * W, "c": CUR * W, "n": nouv * W}).groupby("dec").sum()
    return pd.DataFrame({"revenu_moyen": d.z / d.w, "taux_actuel": 100 * d.c / d.z, "taux_nouveau": 100 * d.n / d.z,
                         "delta_pts": 100 * (d.n - d.c) / d.z, "delta_eur": (d.n - d.c) / d.w})


def evalue(F, t0, z1, z2, t2):
    t1 = cale(F, t0, z1, z2, t2)
    tm, T = famille(F, t0, z1, t1, z2, t2)
    d = deciles(T(Z))
    return dict(F=F, t0=t0, z1=z1, t1=t1, z2=z2, t2=t2, cout=cout(tm(Z)),
                hausse_D7_10=d.delta_pts.iloc[6:].max(), ecart_max_eur=d.delta_eur.abs().max(),
                admissible=bool(d.delta_pts.iloc[6:].max() <= 0.3 and d.delta_eur.abs().max() <= 800))


# ------------------------------------------------------------------ familles (hypothèse)
def parts_familles(pente=0.6):
    rfr_moy = (x.rfr * 1e9 / x.foyers).clip(lower=1000).values
    lo, hi = np.log(5e3), np.log(2e5)
    for _ in range(60):
        mid = (lo + hi) / 2
        s = 1 / (1 + np.exp(-(np.log(rfr_moy) - mid) / pente))
        lo, hi = (mid, hi) if (x.foyers.values * s).sum() > COUPLES else (lo, mid)
    s_k = dict(zip(x.tranche, s))
    c_brut = s + 0.15
    c = c_brut * ENFANTS / (x.foyers.values * c_brut).sum()
    return f.tranche.map(s_k).values, f.tranche.map(dict(zip(x.tranche, c))).values


S_COUPLE, N_ENF = parts_familles()


FR_ADULTE, ABAT_ENFANT = 6000.0, 3000.0


def impot_familial(T, fr_adulte=FR_ADULTE, abat_enfant=ABAT_ENFANT):
    """Version 1, « familles par l'impôt » : chaque enfant ajoute un abattement abat_enfant ; les couples
    ont une seconde franchise fr_adulte (le second adulte n'est pas imposé sur ses premiers euros)."""
    zc = np.clip(Z - N_ENF * abat_enfant, 0, None)
    return (1 - S_COUPLE) * T(zc) + S_COUPLE * T(np.clip(zc - fr_adulte, 0, None))


def par_type(nouv):
    """Charge actuelle et nouvelle par type de revenu (Md€). Nouvelle charge : répartie au prorata des
    assiettes dans la tranche ; actuelle : CSG propre à chaque revenu, IR au prorata des assiettes."""
    k = x.set_index("tranche")
    fs = f.copy()
    fs["n"] = nouv * W / 1e9
    n_k = fs.groupby("tranche").n.sum().reindex(k.index)
    t_cho = m.CSG_CHO_CCSS / (m.F_CHO * k.cho.sum())
    ass = {"Salaires": m.F_SAL * k.sal, "Pensions": m.F_PENS * k.pens, "Indépendants, foncier, gérants":
           m.F_AUT * k.ind + m.F_GER * k.ger, "Chômage, préretraites": m.F_CHO * k.cho}
    csg = {"Salaires": m.T_CSG_ACT * m.F_SAL * k.sal, "Pensions": k.t_pens * m.F_PENS * k.pens,
           "Indépendants, foncier, gérants": m.T_CSG_ACT * (m.F_AUT * k.ind + m.F_GER * k.ger),
           "Chômage, préretraites": t_cho * m.F_CHO * k.cho}
    out = []
    for nom in ass:
        part = ass[nom] / k.assiette
        act = (csg[nom] + k.ir_trav * part).sum()
        nv = (n_k * part).sum()
        out.append((nom, ass[nom].sum(), act, nv))
    return pd.DataFrame(out, columns=["revenu", "assiette", "actuel", "nouveau"]).set_index("revenu")


L0 = dict(F=0.0, t0=0.04, z1=30e3, z2=400e3, t2=0.45)         # barème retenu : taux bas dès le premier euro
L = dict(F=6e3, t0=0.10, z1=80e3, z2=400e3, t2=0.45)          # variante avec franchise

if __name__ == "__main__":
    lignes = []

    def p(*a):
        s_ = " ".join(str(v) for v in a)
        print(s_)
        lignes.append(s_)

    rows = [evalue(*c) for c in itertools.product([0.0, 4e3, 6e3, 8e3, 12e3], [0.0, 0.04, 0.08, 0.10, 0.12],
                                                  [30e3, 50e3, 80e3], [250e3, 400e3, 600e3], [0.40, 0.45, 0.49])]
    R = pd.DataFrame(rows)
    R.round(4).to_csv(HERE / "sorties/bareme_lisse_balayage.csv", index=False)
    p(f"Recette cible {CIBLE:.1f} Md€ ; coût d'efficacité du système actuel (approx.) {cout(TAU_CUR):.1f} Md€")
    p(f"{R.admissible.sum()} barèmes admissibles sur {len(R)} ; les 8 moins coûteux :")
    p(R[R.admissible].sort_values("cout").head(8).round(3).to_string(index=False))
    p("Sans garde-fou, le moins coûteux :")
    p(R.sort_values("cout").head(1).round(3).to_string(index=False))
    for nom, par in (("L0 (retenu, taux dès le premier euro)", L0), ("L (variante avec franchise)", L)):
        t1 = cale(**par)
        tm, T = famille(par["F"], par["t0"], par["z1"], t1, par["z2"], par["t2"])
        d = deciles(T(Z))
        p(f"\n{nom} : franchise {par['F']/1e3:.0f} k€, taux marginal {100*par['t0']:.0f} % → {100*t1:.1f} % à "
          f"{par['z1']/1e3:.0f} k€ → {100*par['t2']:.0f} % à {par['z2']/1e3:.0f} k€ ; coût {cout(tm(Z)):.1f} Md€")
        p(d.round(1).to_string())
        top1 = Q > 0.99
        p(f"1 % le plus aisé : {100*((T(Z)-CUR)*W)[top1].sum()/(Z*W)[top1].sum():+.2f} pt")
        p("Par type de revenu (version 2, sans règle familiale), Md€ :")
        p(par_type(T(Z)).round(1).to_string())
        # familles
        t1v = cale(**par, impot_foyer=impot_familial)
        tmv, Tv = famille(par["F"], par["t0"], par["z1"], t1v, par["z2"], par["t2"])
        nv = impot_familial(Tv)
        dv = deciles(nv)
        trans = ((T(Z) - impot_familial(T)) * W).sum() / 1e9
        p(f"  Version 1, familles par l'impôt (seconde franchise de {FR_ADULTE:.0f} € pour les couples,"
          f" {ABAT_ENFANT:.0f} € par enfant) : taux en z1 = {100*t1v:.1f} % au lieu de {100*t1:.1f} % ;"
          f" coût {cout(tmv(Z)):.1f} Md€")
        p(dv.round(1).to_string())
        p(f"  Version 2, familles par la dépense : la règle familiale de la version 1 vaut {trans:.1f} Md€ à"
          f" barème inchangé ; c'est le montant d'aides aux familles à prévoir côté dépenses.")
        for pente in (0.4, 0.9):
            sc_, nc_ = parts_familles(pente)
            S0, N0 = S_COUPLE.copy(), N_ENF.copy()
            globals()["S_COUPLE"], globals()["N_ENF"] = sc_, nc_
            t1s = cale(**par, impot_foyer=impot_familial)
            tr_s = ((T(Z) - impot_familial(T)) * W).sum() / 1e9
            p(f"    sensibilité à la répartition des couples (pente {pente}) : taux V1 {100*t1s:.1f} % ; coût {tr_s:.1f} Md€")
            globals()["S_COUPLE"], globals()["N_ENF"] = S0, N0
    (HERE / "sorties/bareme_lisse.txt").write_text("\n".join(lignes) + "\n", encoding="utf-8")
