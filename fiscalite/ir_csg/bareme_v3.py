"""Version 3 du barème fusionné IR + CSG + CRDS (relecture v2 de l'auteur).

Lancer depuis fiscalite/ : python3 ir_csg/bareme_v3.py  ->  sorties/bareme_v3.txt, sorties/bareme_v3_balayage.csv

Ce qui change par rapport à bareme_lisse.py :
- la CRDS (0,5 %) entre dans la fusion : elle s'ajoute à la charge actuelle et à la recette à remplacer ;
- l'assiette est le revenu après cotisations sociales, avant CSG et CRDS (« même traitement » : un euro de
  pension et un euro de salaire disponibles avant impôt paient le même impôt ; aujourd'hui l'IR est assis
  sur le salaire net de cotisations et la CSG sur 98,25 % du brut) ;
- chaque adulte est imposé séparément (plus de quotient conjugal ni de franchise de couple) ;
- chaque enfant donne un crédit d'impôt forfaitaire C, imputé sur l'impôt des parents (non remboursable) ;
- le taux marginal part de t0 > 0 dès le premier euro (presque tout le monde paie quelque chose) ;
- garde-fous supplémentaires sur des cas-types OpenFisca : les personnes seules actives ne doivent pas
  gagner beaucoup, les familles avec enfants ne doivent pas perdre, les retraités modestes ne doivent pas
  subir de saignée.

Partage des revenus dans les couples : non publié par tranche. Hypothèse (voir PARTAGE) : mélange de
couples à un seul revenu et de couples à deux revenus inégaux.
"""
import itertools
import os
import sys
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE), str(HERE.parent)]
import ir_csg as m  # noqa: E402
import bareme_lisse as bl  # noqa: E402

x, f = bl.x, bl.f
Z, W, Q, DEC = bl.Z, bl.W, bl.Q, bl.DEC
S_COUPLE, N_ENF = bl.S_COUPLE, bl.N_ENF

# ------------------------------------------------------------------ CRDS actuelle (0,5 %)
# Même assiette que la CSG pour les revenus d'activité ; pensions : due dès que la CSG l'est ; chômage :
# proportionnelle à la CSG (0,5 / 6,2).
T_CRDS = 0.005
x["crds"] = (T_CRDS * (m.F_SAL * x.sal + m.F_GER * x.ger + m.F_AUT * x.ind)
             + T_CRDS * m.F_PENS * x.pens * (x.t_pens > 0)
             + (0.5 / 6.2) * m.CSG_CHO_CCSS * x.cho / x.cho.sum())
x["charge3"] = x.charge + x.crds

# ------------------------------------------------------------------ assiette nette de cotisations
# Facteurs net imposable -> revenu après cotisations, avant CSG (OpenFisca 2024 : salaire imposable =
# 82,0 % du brut, revenu après cotisations = 88,7 % : 1,082) ; gérants et indépendants : + CSG
# déductible (6,8 % d'une assiette de 1,35 fois le revenu) : 1,09 ; foncier 1,0 ; mélange 1,06 ;
# chômage : 1,0 ; pensions : brut (1,055 fois l'imposable).
F_SAL_N, F_GER_N, F_AUT_N, F_CHO_N, F_PENS_N = 1.082, 1.09, 1.06, 1.00, m.F_PENS
x["assiette3"] = F_SAL_N * x.sal + F_GER_N * x.ger + F_AUT_N * x.ind + F_CHO_N * x.cho + F_PENS_N * x.pens
R_K = dict(zip(x.tranche, (x.assiette3 / x.assiette).values))
ZN = Z * f.tranche.map(R_K).values                     # assiette nette du foyer représentatif
RATE3 = dict(zip(x.tranche, (x.charge3 / x.assiette).values))
CUR = Z * f.tranche.map(RATE3).values                  # charge actuelle IR + CSG + CRDS
CIBLE = x.charge3.sum()

# part des pensions dans l'assiette nette, par foyer (pour la décomposition et les effets de seuil)
PART_PENS = f.tranche.map(dict(zip(x.tranche, (F_PENS_N * x.pens / x.assiette3).values))).values

# ------------------------------------------------------------------ charge actuelle par type de foyer
# Dans une tranche de RFR, une personne seule paie aujourd'hui plus qu'un couple, et un couple sans enfant
# plus qu'un couple avec enfants (quotient). On répartit la charge de chaque tranche entre ces types selon
# les rapports impôt / RFR des cas-types OpenFisca au même RFR, en gardant le total de la tranche.
_CT0 = pd.read_csv(HERE / "sorties/courbes_openfisca.csv")


def _tau(profil):
    g = _CT0[_CT0.profil == profil].sort_values("rfr")
    g = g[g.rfr > 0]
    return lambda r: np.interp(r, g.rfr.values, ((g.ir + g.csg + g.crds) / g.rfr).values)


_RFR_F = (Z / f.tranche.map(dict(zip(x.tranche, x.assiette / x.rfr))).values).clip(min=1000)
_ts, _tc0, _tc2 = _tau("seul")(_RFR_F), _tau("couple_0enf")(_RFR_F), _tau("couple_2enf")(_RFR_F)
_scale = bl.ENFANTS / (x.foyers.values * (x.tranche.map(dict(zip(f.tranche, S_COUPLE))).values + 0.15)).sum()
N_ENF_S, N_ENF_C = 0.15 * _scale, 1.15 * _scale          # enfants par foyer : personnes seules, couples
_tc = _tc0 + N_ENF_C * (_tc2 - _tc0) / 2
_mix = (1 - S_COUPLE) * _ts + S_COUPLE * _tc
CUR_S, CUR_C = CUR * _ts / _mix, CUR * _tc / _mix        # charge actuelle : personne seule, couple

# ------------------------------------------------------------------ partage dans les couples (hypothèse)
# (part du premier adulte, poids) ; surchargé par PARTAGE="0.5:1" etc. pour les tests de sensibilité
# Insee Première 1492 (2011) : part de la femme dans les revenus du couple : 0 % pour 12,9 %, 100 % pour 2,2 %,
# 0-20 % pour 10,7 %, 20-40 % pour 27,9 %, 40-60 % pour 38,2 %, 60-100 % pour 8,1 %. En part du premier revenu :
PARTAGE = [(1.0, 0.15), (0.88, 0.12), (0.70, 0.32), (0.55, 0.41)]
if os.environ.get("PARTAGE"):
    PARTAGE = [tuple(float(v) for v in c.split(":")) for c in os.environ["PARTAGE"].split(",")]

# unité d'imposition des couples : "indiv" (chaque adulte séparément) ou "quotient" (deux parts : impôt du
# couple = 2 × impôt sur la moitié de son revenu)
MODE = os.environ.get("MODE", "quotient")

# élasticités du revenu imposable (revenus du travail seulement), par rang du foyer : 50 % du bas, 50-90 %,
# 90-99 %, 1 % du haut. Jeu central proche des médianes de la littérature (Saez, Slemrod et Giertz 2012 :
# 0,12-0,40 ; Neisser 2021 : médiane 0,185 avant déductions) ; « haut » encadre Sicsic (2022).
ELAST = {"bas": (0.05, 0.05, 0.15, 0.20), "central": (0.15, 0.20, 0.30, 0.40), "haut": (0.25, 0.35, 0.50, 0.70)}


def elast(jeu="central"):
    a, b, c, d = ELAST[jeu]
    return np.select([Q < 0.5, Q < 0.9, Q < 0.99], [a, b, c], d) * bl.LAB


def reaction(tm, jeu="central"):
    """Effet des nouveaux taux marginaux sur le revenu imposable du travail (Md€) et sur la recette (Md€) :
    Δz = e · z · Δln(1 − τ), recette induite ≈ τ_nouveau · Δz (premier ordre)."""
    e = elast(jeu)
    r = ZN / Z
    tau_n = (1 - S_COUPLE) * tm(ZN) * r + S_COUPLE * (tm(ZN / 2) if MODE == "quotient" else sum(
        p * (s * tm(s * ZN) + (1 - s) * tm((1 - s) * ZN)) for s, p in PARTAGE)) * r
    dz = e * Z * (np.log(1 - tau_n) - np.log(1 - bl.TAU_CUR))
    return (W * dz).sum() / 1e9, (W * tau_n * dz).sum() / 1e9


ZB = 20e3                                               # nœud bas du barème


def famille(t0, tb, z1, t1, z2, t2):
    """Taux marginal en ligne droite par morceaux : t0 au premier euro, tb à 20 000 €, t1 en z1, t2 en z2,
    puis constant. L'impôt est l'intégrale exacte du taux marginal."""
    xs, ys = np.array([0.0, ZB, z1, z2]), np.array([t0, tb, t1, t2])
    cum = np.r_[0, np.cumsum(np.diff(xs) * (ys[1:] + ys[:-1]) / 2)]

    def tm(v):
        return np.interp(np.asarray(v, float), xs, ys)

    def T(v):
        v = np.asarray(v, float)
        i = np.clip(np.searchsorted(xs, v, side="right") - 1, 0, len(xs) - 1)
        x0, y0 = xs[i], ys[i]
        slope = np.where(i < len(xs) - 1, (ys[np.minimum(i + 1, 3)] - y0) / np.where(i < 3, xs[np.minimum(i + 1, 3)] - x0, 1), 0)
        d = v - x0
        return cum[i] + y0 * d + slope * d ** 2 / 2
    return tm, T


# Enfants de moins de 3 ans : naissances 2022-2024 (Insee : 725 997, 677 803, 660 787), soit 11,5 % des
# 18 millions d'enfants à charge ; répartis entre foyers comme l'ensemble des enfants (hypothèse).
PART_BEBES = (725997 + 677803 + 660787) / bl.ENFANTS
ABAT_BEBE = 0.0          # abattement sur l'assiette du foyer par enfant de moins de 3 ans (option nataliste)


def impot_types(T, C, zn=None):
    """Impôt d'une personne seule et d'un couple du foyer représentatif : crédit C par enfant (non
    remboursable) ; abattement ABAT_BEBE par enfant de moins de 3 ans."""
    zn = ZN if zn is None else zn
    zs = np.clip(zn - ABAT_BEBE * PART_BEBES * N_ENF_S, 0, None)
    zc = np.clip(zn - ABAT_BEBE * PART_BEBES * N_ENF_C, 0, None)
    seul = np.clip(T(zs) - C * N_ENF_S, 0, None)
    if MODE == "quotient":
        couple = np.clip(2 * T(zc / 2) - C * N_ENF_C, 0, None)
    else:
        couple = sum(p * np.clip(T(s * zn) + T((1 - s) * zn) - C * N_ENF_C, 0, None) for s, p in PARTAGE)
    return seul, couple


def impot(T, C, zn=None):
    seul, couple = impot_types(T, C, zn)
    return (1 - S_COUPLE) * seul + S_COUPLE * couple


def seuls_deciles(T, C):
    """Variation de charge des personnes seules, en points de leur revenu, par décile de foyers."""
    seul, _ = impot_types(T, C)
    ws = W * (1 - S_COUPLE)
    d = pd.DataFrame({"dec": DEC + 1, "z": Z * ws, "dn": (seul - CUR_S) * ws}).groupby("dec").sum()
    return 100 * d.dn / d.z


def par_famille(T, C):
    """Variation de charge (Md€ et € par foyer) des personnes seules et des couples."""
    seul, couple = impot_types(T, C)
    ws, wc = W * (1 - S_COUPLE), W * S_COUPLE
    return dict(seuls_mds=((seul - CUR_S) * ws).sum() / 1e9, couples_mds=((couple - CUR_C) * wc).sum() / 1e9,
                seuls_eur=((seul - CUR_S) * ws).sum() / ws.sum(), couples_eur=((couple - CUR_C) * wc).sum() / wc.sum())


def cout(tm, jeu="central"):
    """Coût d'efficacité (Harberger-Feldstein) avec les taux marginaux par adulte, exprimés par euro
    d'assiette brute (taux sur l'assiette nette × rapport net / brut)."""
    e = elast(jeu)
    r = ZN / Z
    d = lambda zz, tau: 0.5 * e * zz * tau ** 2 / (1 - tau)  # noqa: E731
    seul = d(Z, tm(ZN) * r)
    if MODE == "quotient":
        couple = d(Z, tm(ZN / 2) * r)
        return (W * ((1 - S_COUPLE) * seul + S_COUPLE * couple)).sum() / 1e9
    couple = sum(p * (d(s * Z, tm(s * ZN) * r) + d((1 - s) * Z, tm((1 - s) * ZN) * r)) for s, p in PARTAGE)
    return (W * ((1 - S_COUPLE) * seul + S_COUPLE * couple)).sum() / 1e9


def cout_actuel(jeu="central"):
    e = elast(jeu)
    t = bl.TAU_CUR
    return (W * 0.5 * e * Z * t ** 2 / (1 - t)).sum() / 1e9


def cale(t0, tb, z1, z2, t2, C):
    lo, hi = 0.0, 0.8
    for _ in range(50):
        t1 = (lo + hi) / 2
        _, T = famille(t0, tb, z1, t1, z2, t2)
        lo, hi = (t1, hi) if (W * impot(T, C)).sum() / 1e9 < CIBLE else (lo, t1)
    return (lo + hi) / 2


def deciles(nouv):
    d = pd.DataFrame({"dec": DEC + 1, "w": W, "z": Z * W, "c": CUR * W, "n": nouv * W}).groupby("dec").sum()
    return pd.DataFrame({"revenu_moyen": d.z / d.w, "taux_actuel": 100 * d.c / d.z, "taux_nouveau": 100 * d.n / d.z,
                         "delta_pts": 100 * (d.n - d.c) / d.z, "delta_eur": (d.n - d.c) / d.w})


# ------------------------------------------------------------------ cas-types OpenFisca
CT = pd.read_csv(HERE / "sorties/courbes_openfisca.csv")
CT["actuel"] = CT.ir + CT.csg + CT.crds
CT["actuel_plus"] = CT.ir_plus + CT.csg_plus + CT.crds_plus
ENF_CT = {"seul": 0, "couple_0enf": 0, "couple_2enf": 2, "couple_2enf_mono": 2, "retraite_seul": 0}


def cas_types(T, C, plus=False):
    a, b = (CT.base_a_plus.values, CT.base_b_plus.values) if plus else (CT.base_a.values, CT.base_b.values)
    n = (2 * T((a + b) / 2) if MODE == "quotient" else T(a) + T(b)) - C * CT.profil.map(ENF_CT).values
    n = np.where(CT.profil.str.startswith("couple"), n, T(a) - C * CT.profil.map(ENF_CT).values)
    return np.clip(n, 0, None)


def ecart_profil(T, C, profil, lo, hi, pct=True):
    g = CT[(CT.profil == profil) & (CT.brut >= lo) & (CT.brut <= hi)]
    n = cas_types(T, C)[g.index]
    d = n - g.actuel.values
    return 100 * d / g.brut.values if pct else d


def par_tranche(nouv):
    """Variation de charge par tranche de RFR (points d'assiette brute et € par foyer)."""
    fs = pd.DataFrame({"tranche": f.tranche, "n": nouv * W / 1e9})
    n_k = fs.groupby("tranche", sort=False).n.sum().reindex(x.tranche).values
    return pd.DataFrame({"tranche": x.tranche.values, "a": x.a.values,
                         "delta_pts": 100 * (n_k - x.charge3.values) / x.assiette.values,
                         "delta_eur": 1e9 * (n_k - x.charge3.values) / x.foyers.values})


def evalue(t0, db, z1, z2, t2, C):
    tb = t0 + db
    t1 = cale(t0, tb, z1, z2, t2, C)
    tm, T = famille(t0, tb, z1, t1, z2, t2)
    n = impot(T, C)
    d = deciles(n)
    seul = ecart_profil(T, C, "seul", 20e3, 150e3)
    fam = ecart_profil(T, C, "couple_2enf", 25e3, 150e3, pct=False)
    ret = ecart_profil(T, C, "retraite_seul", 8e3, 40e3, pct=False)
    paient = (W * (n > 0)).sum() / W.sum()
    pf = par_famille(T, C)
    sd = seuls_deciles(T, C)
    tr = par_tranche(n)
    haut = tr[(tr.a >= 100e3) & (tr.a < 1e6)].delta_pts     # au-delà d'un million : données trop fragiles
    fm = ecart_profil(T, C, "couple_2enf_mono", 25e3, 150e3, pct=False)
    c0 = ecart_profil(T, C, "couple_0enf", 25e3, 150e3)
    r = dict(t0=t0, tb=tb, z1=z1, t1=t1, z2=z2, t2=t2, C=C, cout=cout(tm), d_max_eur=d.delta_eur.abs().max(),
             hausse_D7_10=d.delta_pts.iloc[6:].max(), seul_min_pts=seul.min(), seul_moy_pts=seul.mean(),
             fam_max_eur=fam.max(), mono_max_eur=fm.max(), c0_moy_pts=c0.mean(), seul_max_pts=seul.max(), ret_max_eur=ret.max(), paient=paient, seuls_dec_min=sd.iloc[2:].min(), seuls_dec_max=sd.iloc[2:].max(), haut_min=haut.min(), haut_max=haut.max(), **pf)
    r["admissible"] = bool(r["d_max_eur"] <= 800 and r["hausse_D7_10"] <= 0.3 and r["seuls_dec_min"] >= -1.25
                           and r["fam_max_eur"] <= -300 and r["ret_max_eur"] <= 1700
                           and r["haut_min"] >= -4.5 and r["haut_max"] <= 3)
    return r


GRILLE = dict(t0=[0.06, 0.07, 0.08], db=[0.05, 0.06, 0.07, 0.08], z1=[25e3, 30e3, 35e3], z2=[100e3, 120e3, 140e3],
              t2=[0.45, 0.47], C=[500.0, 750.0, 1000.0, 1250.0])

if __name__ == "__main__":
    out = []

    def p(*a):
        s_ = " ".join(str(v) for v in a)
        print(s_)
        out.append(s_)

    p(f"Cible IR + CSG + CRDS : {CIBLE:.1f} Md€ (dont CRDS {x.crds.sum():.1f}) ; assiette nette {x.assiette3.sum():.0f} Md€"
      f" (brute {x.assiette.sum():.0f}) ; coût d'efficacité actuel {cout_actuel():.1f} Md€ (central)")
    rows = [evalue(*c) for c in itertools.product(*GRILLE.values())]
    R = pd.DataFrame(rows)
    R.round(4).to_csv(HERE / f"sorties/bareme_v3_balayage_{MODE}.csv", index=False)
    p(f"{R.admissible.sum()} admissibles sur {len(R)}")
    p(R[R.admissible].sort_values("cout").head(12).round(3).to_string(index=False))
    (HERE / f"sorties/bareme_v3_{MODE}.txt").write_text("\n".join(out) + "\n", encoding="utf-8")


def par_type(nouv):
    """Charge actuelle (IR + CSG + CRDS) et nouvelle par type de revenu (Md€). Actuelle : CSG et CRDS propres
    à chaque revenu, IR au prorata de l'assiette brute dans la tranche ; nouvelle : au prorata de l'assiette
    nette de cotisations dans la tranche."""
    k = x.set_index("tranche")
    fs = pd.DataFrame({"tranche": f.tranche, "n": nouv * W / 1e9})
    n_k = fs.groupby("tranche").n.sum().reindex(k.index)
    t_cho = m.CSG_CHO_CCSS / (m.F_CHO * k.cho.sum())
    brut = {"Salaires": m.F_SAL * k.sal, "Pensions": m.F_PENS * k.pens,
            "Indépendants, foncier, gérants": m.F_AUT * k.ind + m.F_GER * k.ger, "Chômage, préretraites": m.F_CHO * k.cho}
    net = {"Salaires": F_SAL_N * k.sal, "Pensions": F_PENS_N * k.pens,
           "Indépendants, foncier, gérants": F_AUT_N * k.ind + F_GER_N * k.ger, "Chômage, préretraites": F_CHO_N * k.cho}
    csg = {"Salaires": (m.T_CSG_ACT + T_CRDS) * m.F_SAL * k.sal,
           "Pensions": (k.t_pens + T_CRDS * (k.t_pens > 0)) * m.F_PENS * k.pens,
           "Indépendants, foncier, gérants": (m.T_CSG_ACT + T_CRDS) * (m.F_AUT * k.ind + m.F_GER * k.ger),
           "Chômage, préretraites": t_cho * (1 + 0.5 / 6.2) * m.F_CHO * k.cho}
    out = []
    for nom in brut:
        act = (csg[nom] + k.ir_trav * brut[nom] / k.assiette).sum()
        nv = (n_k * net[nom] / k.assiette3).sum()
        out.append((nom, brut[nom].sum(), net[nom].sum(), act, nv))
    return pd.DataFrame(out, columns=["revenu", "assiette_brute", "assiette_nette", "actuel", "nouveau"]).set_index("revenu")


# barème retenu (version 3) : taux marginal 7 % au premier euro, 14 % à 20 000 €, t1 calé à 30 000 €, 43 % à
# 120 000 € par part ; quotient conjugal (deux parts) ; crédit de 600 € par enfant ; abattement bébé
V3 = dict(t0=0.07, tb=0.14, z1=30e3, z2=120e3, t2=0.43, C=600.0)
# orientation « Tax Foundation » (taux du haut 43 % au lieu de 45 %) et nataliste (abattement de 12 000 € par
# enfant de moins de 3 ans, crédit ramené de 750 à 600 €) ; la version sans ces deux choix : V3_BASE
V3_BASE = dict(t0=0.07, tb=0.14, z1=30e3, z2=120e3, t2=0.45, C=750.0)
ABAT_BEBE = 12e3


def retenu():
    t1 = cale(**V3)
    tm, T = famille(V3["t0"], V3["tb"], V3["z1"], t1, V3["z2"], V3["t2"])
    return t1, tm, T
