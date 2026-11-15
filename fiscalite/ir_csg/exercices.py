"""Les exercices de la note (version finale) : sorties/exercices.txt et sorties/exercices_*.csv.

Lancer depuis fiscalite/ : python3 ir_csg/exercices.py

Cadre commun, à recette égale (IR + CSG + CRDS sur les revenus au barème, 220 Md€) :
- assiette commune : revenu après cotisations sociales, pour tous les revenus (salaires, pensions, revenus des
  indépendants, loyers, allocations chômage) ; aucune réduction, aucun abattement, aucun taux réduit ;
- impôt individuel (comme la CSG) : chaque adulte est imposé sur son propre revenu ; partage des revenus dans
  les couples d'après l'Insee (bareme_v3.PARTAGE) ;
- franchise de FRANCHISE € par enfant à charge, déduite du revenu du parent qui gagne le plus.

Exercice 1, harmonisation brutale : on garde l'empilement des barèmes actuels (tranches de l'IR des revenus 2024,
appliquées à chaque adulte, plus un taux unique de CSG-CRDS sur tous les revenus), ce taux étant calé sur la recette.
Exercice 2, aplanissement : un barème unique dont le taux marginal monte en ligne droite entre quelques seuils
(taux du haut de 50 %), choisi pour s'écarter le moins possible de la charge actuelle de chaque foyer (écart
quadratique moyen en points de revenu), à même recette.
Exercice 3, perte sèche minimale : dans la même famille de barèmes, celui qui minimise la perte sèche, sans aucune
correction sociale. Les pénalités sociales (déciles, haut de la distribution, équité seuls / familles) sont
calculées pour information ; la correction sera décidée ensuite.
"""
import itertools
import sys
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE), str(HERE.parent)]
import bareme_v3 as v  # noqa: E402

FRANCHISE = 6000.0
TOP = 0.50
# barème de l'IR, revenus 2024 (OpenFisca-France, paramètre impot_revenu.bareme_ir_depuis_1945, 2024)
IR_SEUILS = [0.0, 11497.0, 29315.0, 83823.0, 180294.0]
IR_TAUX = [0.0, 0.11, 0.30, 0.41, 0.45]
SIG = dict(dec=1.5, haut=3.0, equite=0.5)

x, W, Z, ZN, Q, DEC = v.x, v.W, v.Z, v.ZN, v.Q, v.DEC
S, NS, NC = v.S_COUPLE, v.N_ENF_S, v.N_ENF_C
R = ZN / Z                                              # assiette nette / brute du foyer représentatif


# ------------------------------------------------------------------ barèmes individuels
def bareme_empile(tau):
    """Exercice 1 : tranches de l'IR + taux unique tau sur tout le revenu."""
    s_, t_ = np.array(IR_SEUILS), np.array(IR_TAUX)
    hauts = np.r_[s_[1:], np.inf]

    def T(z):
        z = np.asarray(z, float)
        return sum(r * np.clip(np.minimum(z, h) - lo, 0, None) for lo, h, r in zip(s_, hauts, t_)) + tau * z

    def tm(z):
        z = np.asarray(z, float)
        return t_[np.searchsorted(s_, z, side="right") - 1] + tau
    return tm, T


def bareme_lineaire(xs, ys):
    """Taux marginal en ligne droite entre les seuils xs (taux ys), constant au-delà du dernier."""
    xs, ys = np.asarray(xs, float), np.asarray(ys, float)
    cum = np.r_[0, np.cumsum(np.diff(xs) * (ys[1:] + ys[:-1]) / 2)]
    k = len(xs)

    def tm(z):
        return np.interp(np.asarray(z, float), xs, ys)

    def T(z):
        z = np.asarray(z, float)
        i = np.clip(np.searchsorted(xs, z, side="right") - 1, 0, k - 1)
        nxt = np.minimum(i + 1, k - 1)
        larg = np.where(i < k - 1, xs[nxt] - xs[i], 1.0)
        pente = np.where(i < k - 1, (ys[nxt] - ys[i]) / larg, 0.0)
        d = z - xs[i]
        return cum[i] + ys[i] * d + pente * d ** 2 / 2
    return tm, T


# ------------------------------------------------------------------ adultes des foyers représentatifs
def adultes():
    """(assiette nette après franchise, assiette brute, poids, type) pour chaque adulte."""
    out = [(np.clip(ZN - FRANCHISE * NS, 0, None), Z, W * (1 - S), "seul")]
    for s_, p in v.PARTAGE:
        out.append((np.clip(s_ * ZN - FRANCHISE * NC, 0, None), s_ * Z, W * S * p, "couple_a"))
        out.append(((1 - s_) * ZN, (1 - s_) * Z, W * S * p, "couple_b"))
    return out


ADULTES = adultes()


def impot_couple(T, s_):
    return T(np.clip(s_ * ZN - FRANCHISE * NC, 0, None)) + T((1 - s_) * ZN)


def impot_types(T):
    seul = T(ADULTES[0][0])
    couple = sum(p * impot_couple(T, s_) for s_, p in v.PARTAGE)
    return seul, couple


def impot(T):
    seul, couple = impot_types(T)
    return (1 - S) * seul + S * couple


def recette(T):
    return (W * impot(T)).sum() / 1e9


def cout(tm, jeu="central"):
    """Perte sèche (Harberger-Feldstein), taux marginal de chaque adulte rapporté à son revenu brut."""
    e = v.elast(jeu)
    tot = 0.0
    for zn, zb, w, _ in ADULTES:
        tau = np.clip(tm(zn) * R, 0, 0.95)
        tot += (w * 0.5 * e * zb * tau ** 2 / (1 - tau)).sum()
    return tot / 1e9


def reaction(tm, jeu="central"):
    """Variation du revenu du travail déclaré et recette induite (Md€), premier ordre."""
    e = v.elast(jeu)
    dz = dr = 0.0
    for zn, zb, w, _ in ADULTES:
        tau = np.clip(tm(zn) * R, 0, 0.95)
        d = e * zb * (np.log(1 - tau) - np.log(1 - v.bl.TAU_CUR))
        dz += (w * d).sum()
        dr += (w * tau * d).sum()
    return dz / 1e9, dr / 1e9


# ------------------------------------------------------------------ cas-types OpenFisca
CT = v.CT
ENF = {"seul": 0, "couple_0enf": 0, "couple_2enf": 2, "couple_2enf_mono": 2, "retraite_seul": 0}


def cas_types(T, plus=False):
    a = (CT.base_a_plus if plus else CT.base_a).values
    b = (CT.base_b_plus if plus else CT.base_b).values
    n = CT.profil.map(ENF).values
    haut, bas = np.maximum(a, b), np.minimum(a, b)
    return T(np.clip(haut - FRANCHISE * n, 0, None)) + T(bas)


def ecart_ct(T, profil, brut):
    g = CT[(CT.profil == profil) & (CT.brut == brut)]
    return float(cas_types(T)[g.index[0]] - g.actuel.iloc[0])


# ------------------------------------------------------------------ indicateurs
def gini(y, w):
    o = np.argsort(y)
    y, w = y[o], w[o]
    p = np.r_[0, np.cumsum(w) / w.sum()]
    L = np.r_[0, np.cumsum(y * w) / (y * w).sum()]
    return 1 - np.sum((p[1:] - p[:-1]) * (L[1:] + L[:-1]))


G0, GC = gini(Z, W), gini(Z - v.CUR, W)


def transferts(T):
    """Écart quadratique moyen, en points de revenu, entre la nouvelle charge et la charge actuelle de chaque
    foyer (personnes seules ; couples selon leur partage des revenus)."""
    tot = (W * (1 - S) * ((T(ADULTES[0][0]) - v.CUR_S) / Z) ** 2).sum()
    for s_, p in v.PARTAGE:
        tot += (W * S * p * ((impot_couple(T, s_) - v.CUR_C) / Z) ** 2).sum()
    return 100 * np.sqrt(tot / W.sum())


def equite(T):
    """Gain d'une personne seule moins gain d'un couple avec deux enfants, au même brut (40-100 k€), en points."""
    n = cas_types(T)
    s_ = CT[(CT.profil == "seul") & CT.brut.between(40e3, 100e3)]
    c = CT[(CT.profil == "couple_2enf") & CT.brut.between(40e3, 100e3)]
    return 100 * (-(n[s_.index] - s_.actuel.values) / s_.brut.values + (n[c.index] - c.actuel.values) / c.brut.values)


def penalites(T):
    n = impot(T)
    d = v.deciles(n)
    tr = v.par_tranche(n)
    haut = tr[(tr.a >= 100e3) & (tr.a < 1e6)].delta_pts.values
    eq = equite(T)
    return dict(pen_dec=float(((d.delta_pts.values / SIG["dec"]) ** 2).sum()),
                pen_haut=float(((haut / SIG["haut"]) ** 2).mean()),
                pen_equite=float((np.clip(eq, 0, None) ** 2).mean() / SIG["equite"] ** 2))


def bilan(tm, T):
    n = impot(T)
    seul, couple = impot_types(T)
    ws, wc = W * (1 - S), W * S
    sd = pd.DataFrame({"dec": DEC + 1, "z": Z * ws, "dn": (seul - v.CUR_S) * ws}).groupby("dec").sum()
    return dict(recette=(W * n).sum() / 1e9, cout=cout(tm), cout_bas=cout(tm, "bas"), cout_haut=cout(tm, "haut"),
                reaction=reaction(tm), deciles=v.deciles(n), tranches=v.par_tranche(n), types=v.par_type(n),
                seuls_mds=((seul - v.CUR_S) * ws).sum() / 1e9, couples_mds=((couple - v.CUR_C) * wc).sum() / 1e9,
                seuls_dec=100 * sd.dn / sd.z, redistribution=(G0 - gini(Z - n, W)) / (G0 - GC),
                transferts=transferts(T), paient=(W * (n > 0)).sum() / W.sum())


# ------------------------------------------------------------------ exercice 1
def exercice1():
    lo, hi = -0.2, 0.3
    for _ in range(60):
        tau = (lo + hi) / 2
        lo, hi = (tau, hi) if recette(bareme_empile(tau)[1]) < v.CIBLE else (lo, tau)
    return (lo + hi) / 2


# ------------------------------------------------------------------ exercices 2 et 3 : une même famille
def famille(t0, tb, z1, z2):
    """Taux t0 au premier euro, tb à 20 000 €, t1 (calé sur la recette) en z1, TOP en z2 et au-delà."""
    lo, hi = 0.0, TOP
    for _ in range(50):
        t1 = (lo + hi) / 2
        _, T = bareme_lineaire([0, 20e3, z1, z2], [t0, tb, t1, TOP])
        lo, hi = (t1, hi) if recette(T) < v.CIBLE else (lo, t1)
    t1 = (lo + hi) / 2
    return t1, bareme_lineaire([0, 20e3, z1, z2], [t0, tb, t1, TOP])


def grille():
    rows = []
    for t0, tb, z1, z2 in itertools.product([0.03, 0.05, 0.07, 0.09, 0.11, 0.13, 0.15],
                                            [0.08, 0.10, 0.13, 0.16, 0.19, 0.22],
                                            [30e3, 45e3, 60e3, 80e3], [100e3, 150e3, 250e3, 400e3, 600e3]):
        if tb < t0 or z1 >= z2:
            continue
        t1, (tm, T) = famille(t0, tb, z1, z2)
        if not tb <= t1 <= TOP:
            continue
        rows.append(dict(t0=t0, tb=tb, z1=z1, t1=t1, z2=z2, cout=cout(tm), transferts=transferts(T), **penalites(T)))
    return pd.DataFrame(rows)


def resultats():
    tau = exercice1()
    G = grille()
    b2 = G.sort_values("transferts").iloc[0]
    b3 = G.sort_values("cout").iloc[0]
    return dict(tau=tau, ex1=bareme_empile(tau), grille=G, b2=b2, b3=b3,
                ex2=famille(b2.t0, b2.tb, b2.z1, b2.z2)[1], ex3=famille(b3.t0, b3.tb, b3.z1, b3.z2)[1])


if __name__ == "__main__":
    L = []

    def p(tag, txt):
        s = f"[{tag}] {txt}"
        print(s)
        L.append(s)
    res = resultats()
    p("E0", f"recette cible {v.CIBLE:.1f} Md€ ; franchise {FRANCHISE:,.0f} € par enfant ; coût d'efficacité actuel"
             f" {v.cout_actuel():.1f} Md€ (bas {v.cout_actuel('bas'):.1f}, haut {v.cout_actuel('haut'):.1f})")
    p("E1", f"exercice 1 : tranches de l'IR 2024 + taux unique de {100*res['tau']:.2f} % sur tout le revenu ;"
            f" part « barème de l'IR » {recette(bareme_empile(0.0)[1]):.1f} Md€")
    G = res["grille"]
    G.round(4).to_csv(HERE / "sorties/exercices_grille.csv", index=False)
    for k, nom in (("b2", "exercice 2 (transferts minimaux)"), ("b3", "exercice 3 (perte sèche minimale)")):
        b = res[k]
        p("E2" if k == "b2" else "E3", f"{nom} : {100*b.t0:.0f} % au premier euro, {100*b.tb:.0f} % à 20 000 €,"
              f" {100*b.t1:.1f} % à {b.z1/1e3:.0f} k€, {100*TOP:.0f} % à {b.z2/1e3:.0f} k€ ; coût {b.cout:.1f} ;"
              f" transferts {b.transferts:.2f} pts ; pénalités déciles {b.pen_dec:.2f}, haut {b.pen_haut:.2f},"
              f" équité {b.pen_equite:.2f}")
    # les 5 barèmes les moins coûteux, pour juger de la robustesse de l'exercice 3
    p("E3", "5 barèmes les moins coûteux :\n" + G.sort_values("cout").head(5)[
        ["t0", "tb", "z1", "t1", "z2", "cout", "transferts"]].round(3).to_string(index=False))
    rows = []
    for nom, (tm, T) in (("1 harmonisation", res["ex1"]), ("2 aplanissement", res["ex2"]),
                         ("3 perte sèche minimale", res["ex3"])):
        b = bilan(tm, T)
        p("E4", f"{nom} : recette {b['recette']:.1f} ; coût {b['cout']:.1f} ({b['cout_bas']:.1f} à {b['cout_haut']:.1f}) ;"
                f" réaction revenu {b['reaction'][0]:+.1f}, recette {b['reaction'][1]:+.1f} Md€ ; redistribution"
                f" {b['redistribution']:.2f} ; transferts {b['transferts']:.2f} pts ; foyers qui paient {100*b['paient']:.1f} %")
        p("E5", f"{nom} : déciles € " + " ".join(f"{u:+.0f}" for u in b["deciles"].delta_eur)
              + " | pts " + " ".join(f"{u:+.1f}" for u in b["deciles"].delta_pts))
        tr = b["tranches"]
        p("E6", f"{nom} : tranches RFR ≥ 100 k€ (pts) " + " ".join(f"{u:+.1f}" for u in tr[tr.a >= 100e3].delta_pts))
        p("E6", f"{nom} : RFR 100-200k {tr.delta_eur.iloc[7]:+,.0f} € ; 200-300k {tr.delta_eur.iloc[8]:+,.0f} € ;"
                f" 1-2M {tr[tr.a == 1000001].delta_pts.iloc[0]:+.1f} pts")
        pt = b["types"]
        p("E7", f"{nom} : types (Md€) " + " ; ".join(f"{i} {r.nouveau - r.actuel:+.1f}" for i, r in pt.iterrows()))
        p("E8", f"{nom} : personnes seules {b['seuls_mds']:+.1f} Md€, couples {b['couples_mds']:+.1f} Md€ ; seules par décile "
                + " ".join(f"{u:+.1f}" for u in b["seuls_dec"]))
        for prof in ("seul", "couple_0enf", "couple_2enf", "couple_2enf_mono", "retraite_seul"):
            p("E9", f"{nom} : {prof:17s} " + " ".join(f"{int(br/1e3)}k {ecart_ct(T, prof, br):+,.0f}"
                                                     for br in (15e3, 17e3, 21.5e3, 30e3, 50e3, 80e3, 100e3, 150e3)))
        p("E10", f"{nom} : taux marginal d'un adulte (assiette nette) " + " ".join(
            f"{int(z/1e3)}k {100*float(tm(z)):.1f}" for z in (5e3, 15e3, 25e3, 40e3, 60e3, 100e3, 200e3, 400e3)))
        p("E10", f"{nom} : impôt d'un adulte sans enfant " + " ".join(
            f"{int(z/1e3)}k {float(T(z)):,.0f} ({100*float(T(z))/z:.1f} %)" for z in (10e3, 20e3, 30e3, 50e3, 80e3, 120e3, 200e3)))
        for prof, br in (("seul", 30e3), ("seul", 50e3), ("seul", 80e3), ("couple_2enf", 50e3), ("couple_2enf", 80e3)):
            g = CT[(CT.profil == prof) & (CT.brut == br)]
            i = g.index[0]
            n0, n1 = cas_types(T)[i], cas_types(T, plus=True)[i]
            p("E11", f"{nom} : {prof} {br/1e3:.0f} k€ brut : taux moyen {100*n0/br:.1f} % (auj. {100*g.actuel.iloc[0]/br:.1f}),"
                     f" marginal {(n1-n0)/10:.1f} % (auj. {(g.actuel_plus.iloc[0]-g.actuel.iloc[0])/10:.1f})")
        p("E12", f"{nom} : valeur de la franchise par enfant pour le parent au revenu net de " + " ".join(
            f"{int(z/1e3)}k {float(T(z) - T(z - FRANCHISE)):,.0f} €" for z in (20e3, 30e3, 45e3, 60e3, 100e3, 200e3)))
        rows.append(dict(exercice=nom, cout=b["cout"], redistribution=b["redistribution"], transferts=b["transferts"],
                         **{f"D{i+1}": u for i, u in enumerate(b["deciles"].delta_eur)}))
    pd.DataFrame(rows).round(3).to_csv(HERE / "sorties/exercices_synthese.csv", index=False)
    (HERE / "sorties/exercices.txt").write_text("\n".join(L) + "\n", encoding="utf-8")
