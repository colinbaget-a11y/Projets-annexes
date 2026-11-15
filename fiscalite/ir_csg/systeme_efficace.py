"""Note courte « le système le plus efficace » : impôt proportionnel sur le revenu, favorable au travail et aux
familles, à recette égale (IR + CSG + CRDS sur les revenus au barème, 220 Md€). N'annule rien des exercices.

Lancer depuis fiscalite/ : python3 ir_csg/systeme_efficace.py  ->  sorties/systeme_efficace.txt

Système : taux t_w sur les revenus du travail (salaires, indépendants, gérants, loyers), taux t_p = t_w + ECART sur
les revenus qui ne réagissent pas (pensions, allocations chômage), même assiette (revenu après cotisations), aucun
abattement ; crédit d'impôt de C € par enfant, versé même sans impôt. Avec un taux unique, imposer chaque adulte
séparément ou le couple ensemble revient au même. t_w est calé sur la recette.
"""
import itertools
import sys
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE), str(HERE.parent)]
import exercices as ex  # noqa: E402

v = ex.v
x, W, Z, ZN, S = v.x, v.W, v.Z, v.ZN, v.S_COUPLE
NENF = (1 - S) * v.N_ENF_S + S * v.N_ENF_C                       # enfants par foyer représentatif
# part des revenus « qui ne réagissent pas » (pensions, chômage) dans l'assiette nette, par tranche
NL = v.f.tranche.map(dict(zip(x.tranche, ((v.F_PENS_N * x.pens + v.F_CHO_N * x.cho) / x.assiette3).values))).values
R = ZN / Z


def impot(tw, tp, C):
    return ZN * (tw * (1 - NL) + tp * NL) - C * NENF


def cale(ecart, C):
    lo, hi = 0.0, 0.6
    for _ in range(60):
        tw = (lo + hi) / 2
        lo, hi = (tw, hi) if (W * impot(tw, tw + ecart, C)).sum() / 1e9 < v.CIBLE else (lo, tw)
    return (lo + hi) / 2


def cout(tw, jeu="central"):
    """Perte sèche : seuls les revenus du travail réagissent ; taux marginal tw sur le revenu après cotisations."""
    e = v.elast(jeu)
    tau = tw * R
    return (W * 0.5 * e * Z * tau ** 2 / (1 - tau)).sum() / 1e9


def reaction(tw, jeu="central"):
    e = v.elast(jeu)
    tau = tw * R
    d = e * Z * (np.log(1 - tau) - np.log(1 - v.bl.TAU_CUR))
    return (W * d).sum() / 1e9, (W * tau * d).sum() / 1e9


# ------------------------------------------------------------------ cas-types
CT = ex.CT
ENF = ex.ENF


def cas_types(tw, tp, C, plus=False):
    a = (CT.base_a_plus if plus else CT.base_a).values
    b = (CT.base_b_plus if plus else CT.base_b).values
    taux = np.where(CT.profil == "retraite_seul", tp, tw)
    return taux * (a + b) - C * CT.profil.map(ENF).values


def ecart_ct(tw, tp, C, profil, brut):
    g = CT[(CT.profil == profil) & (CT.brut == brut)]
    return float(cas_types(tw, tp, C)[g.index[0]] - g.actuel.iloc[0])


def bilan(ecart, C):
    tw = cale(ecart, C)
    tp = tw + ecart
    n = impot(tw, tp, C)
    d = v.deciles(n)
    pt = v.par_type(n)
    return dict(ecart=ecart, C=C, tw=tw, tp=tp, cout=cout(tw), cout_bas=cout(tw, "bas"), cout_haut=cout(tw, "haut"),
                reaction=reaction(tw), deciles=d, types=pt, redistribution=ex.redistribution(n),
                credit=C * (W * NENF).sum() / 1e9)


if __name__ == "__main__":
    L = []

    def p(tag, txt):
        s = f"[{tag}] {txt}"
        print(s)
        L.append(s)
    p("S0", f"recette {v.CIBLE:.1f} Md€ ; assiette nette {x.assiette3.sum():.0f} Md€ dont pensions et chômage"
            f" {(W * ZN * NL).sum()/1e9:.0f} Md€ ; enfants {(W * NENF).sum()/1e6:.1f} M ; coût actuel {v.cout_actuel():.1f}"
            f" (bas {v.cout_actuel('bas'):.1f}, haut {v.cout_actuel('haut'):.1f})")
    for ecart, C in itertools.product([0.0, 0.03, 0.05, 0.08], [0.0, 1000.0, 1500.0, 2000.0]):
        b = bilan(ecart, C)
        p("S1", f"écart {100*ecart:.0f} pt, crédit {C:.0f} € : travail {100*b['tw']:.1f} %, pensions et chômage"
                f" {100*b['tp']:.1f} % ; coût {b['cout']:.1f} ({b['cout_bas']:.1f} à {b['cout_haut']:.1f}) ; crédit"
                f" {b['credit']:.1f} Md€ ; redistribution {b['redistribution']:.2f} ; D1-D10 € "
                + " ".join(f"{u:+.0f}" for u in b["deciles"].delta_eur))
    # système retenu
    ECART, C = 0.05, 1500.0
    b = bilan(ECART, C)
    tw, tp = b["tw"], b["tp"]
    p("S2", f"retenu : travail {100*tw:.2f} %, pensions et chômage {100*tp:.2f} %, crédit {C:.0f} € par enfant ({b['credit']:.1f} Md€)")
    p("S2", f"coût {b['cout']:.1f} Md€ ({b['cout_bas']:.1f} à {b['cout_haut']:.1f}) contre {v.cout_actuel():.1f} ;"
            f" revenu du travail déclaré {b['reaction'][0]:+.1f} Md€, recette induite {b['reaction'][1]:+.1f} Md€ ;"
            f" redistribution {b['redistribution']:.2f}")
    p("S3", "déciles € " + " ".join(f"{u:+.0f}" for u in b["deciles"].delta_eur) + " | pts "
          + " ".join(f"{u:+.1f}" for u in b["deciles"].delta_pts))
    p("S4", "types (Md€) " + " ; ".join(f"{i} {r.nouveau - r.actuel:+.1f}" for i, r in b["types"].iterrows()))
    tr = v.par_tranche(impot(tw, tp, C))
    p("S5", "tranches RFR ≥ 100 k€ (pts) " + " ".join(f"{u:+.1f}" for u in tr[tr.a >= 100e3].delta_pts)
          + f" ; 100-200k {tr.delta_eur.iloc[7]:+,.0f} € ; 200-300k {tr.delta_eur.iloc[8]:+,.0f} €")
    for prof in ("seul", "couple_0enf", "couple_2enf", "couple_2enf_mono", "retraite_seul"):
        p("S6", f"{prof:17s} " + " ".join(f"{int(br/1e3)}k {ecart_ct(tw, tp, C, prof, br):+,.0f}"
                                         for br in (15e3, 17e3, 21.5e3, 30e3, 50e3, 80e3, 100e3, 150e3)))
    for prof, br in (("seul", 21.5e3), ("seul", 50e3), ("seul", 100e3), ("couple_2enf", 50e3), ("couple_2enf", 80e3),
                     ("retraite_seul", 17e3), ("retraite_seul", 30e3)):
        g = CT[(CT.profil == prof) & (CT.brut == br)]
        i = g.index[0]
        n0, n1 = cas_types(tw, tp, C)[i], cas_types(tw, tp, C, plus=True)[i]
        p("S7", f"{prof} {br/1e3:.1f} k€ : aujourd'hui {g.actuel.iloc[0]:,.0f} € ({100*g.actuel.iloc[0]/br:.1f} %, marginal"
                f" {(g.actuel_plus.iloc[0]-g.actuel.iloc[0])/10:.1f} %) ; proposé {n0:,.0f} € ({100*n0/br:.1f} %, marginal {(n1-n0)/10:.1f} %)")
    (HERE / "sorties/systeme_efficace.txt").write_text("\n".join(L) + "\n", encoding="utf-8")


# ------------------------------------------------------------------ variante : franchise sur les revenus du travail
def impot_franchise(tw, tp, C, F):
    """Chaque adulte ne paie pas d'impôt sur ses F premiers euros de revenu du travail (pas sur les pensions)."""
    lab = ZN * (1 - NL)
    seul = tw * np.clip(lab - F, 0, None)
    couple = sum(p * (tw * np.clip(s_ * lab - F, 0, None) + tw * np.clip((1 - s_) * lab - F, 0, None))
                 for s_, p in v.PARTAGE)
    return (1 - S) * seul + S * couple + tp * ZN * NL - C * NENF


def cale_franchise(ecart, C, F):
    lo, hi = 0.0, 0.8
    for _ in range(60):
        tw = (lo + hi) / 2
        lo, hi = (tw, hi) if (W * impot_franchise(tw, tw + ecart, C, F)).sum() / 1e9 < v.CIBLE else (lo, tw)
    return (lo + hi) / 2


def cout_franchise(tw, F, jeu="central"):
    """Perte sèche : taux marginal nul sous la franchise, tw au-dessus (par adulte)."""
    e = v.elast(jeu)
    lab = ZN * (1 - NL)
    d = lambda zb, zl: 0.5 * e * zb * np.where(zl > F, tw * R, 0) ** 2 / (1 - tw * R)  # noqa: E731
    seul = d(Z, lab)
    couple = sum(p * (d(s_ * Z, s_ * lab) + d((1 - s_) * Z, (1 - s_) * lab)) for s_, p in v.PARTAGE)
    return (W * ((1 - S) * seul + S * couple)).sum() / 1e9


if __name__ == "__main__":
    for F in (0.0, 5000.0, 8000.0, 10000.0):
        tw = cale_franchise(0.05, 1500.0, F)
        n = impot_franchise(tw, tw + 0.05, 1500.0, F)
        d = v.deciles(n)
        g = CT[(CT.profil == "seul") & (CT.brut == 21.5e3)]
        smic = tw * max(g.base_a.iloc[0] - F, 0) - g.actuel.iloc[0]
        g2 = CT[(CT.profil == "seul") & (CT.brut == 50e3)]
        s50 = tw * max(g2.base_a.iloc[0] - F, 0) - g2.actuel.iloc[0]
        p("S8", f"franchise travail {F:,.0f} € : travail {100*tw:.1f} %, pensions {100*(tw+0.05):.1f} % ; coût"
                f" {cout_franchise(tw, F):.1f} ({cout_franchise(tw, F, 'bas'):.1f} à {cout_franchise(tw, F, 'haut'):.1f}) ;"
                f" SMIC seul {smic:+,.0f} € ; seul 50 k€ {s50:+,.0f} € ; redistribution {ex.redistribution(n):.2f} ;"
                f" D1-D10 € " + " ".join(f"{u:+.0f}" for u in d.delta_eur))
    (HERE / "sorties/systeme_efficace.txt").write_text("\n".join(L) + "\n", encoding="utf-8")


# ------------------------------------------------------------------ trois systèmes comparés dans la note courte
def systeme(t, ecart, C, F, univ):
    """Impôt par foyer et perte sèche. t : taux sur le travail ; t + ecart : pensions et chômage ; franchise F par
    adulte, sur le seul revenu du travail (univ=False) ou sur tout son revenu (univ=True) ; crédit C par enfant."""
    lab, nl = ZN * (1 - NL), ZN * NL
    e = v.elast()

    def adulte(sh, zb):
        zl, zp = sh * lab, sh * nl
        if univ:                                   # la franchise s'impute d'abord sur le travail
            fl = np.minimum(zl, F)
            fp = np.minimum(zp, F - fl)
            imp = t * (zl - fl) + (t + ecart) * (zp - fp)
            marg = np.where(zl + zp > F, t, 0.0)
        else:
            imp = t * np.clip(zl - F, 0, None) + (t + ecart) * zp
            marg = np.where(zl > F, t, 0.0)
        tau = marg * R
        return imp, 0.5 * e * sh * zb * tau ** 2 / (1 - tau)
    i_s, c_s = adulte(1.0, Z)
    i_c = c_c = 0.0
    for s_, p in v.PARTAGE:
        ia, ca = adulte(s_, Z)
        ib, cb = adulte(1 - s_, Z)
        i_c, c_c = i_c + p * (ia + ib), c_c + p * (ca + cb)
    n = (1 - S) * i_s + S * i_c - C * NENF
    return n, (W * ((1 - S) * c_s + S * c_c)).sum() / 1e9


def cale_systeme(ecart, C, F, univ):
    lo, hi = 0.0, 0.8
    for _ in range(60):
        t = (lo + hi) / 2
        lo, hi = (t, hi) if (W * systeme(t, ecart, C, F, univ)[0]).sum() / 1e9 < v.CIBLE else (lo, t)
    return (lo + hi) / 2


def ct_systeme(t, ecart, C, F, univ, plus=False):
    a = (CT.base_a_plus if plus else CT.base_a).values
    b = (CT.base_b_plus if plus else CT.base_b).values
    ret = (CT.profil == "retraite_seul").values
    if univ:
        f = lambda z, tx: tx * np.clip(z - F, 0, None)  # noqa: E731
    else:
        f = lambda z, tx: np.where(ret, tx * z, tx * np.clip(z - F, 0, None))  # noqa: E731
    tx = np.where(ret, t + ecart, t)
    return f(a, tx) + np.where(b > 0, f(b, tx), 0) - C * CT.profil.map(ENF).values


SYSTEMES = {"A": dict(ecart=0.05, C=1500.0, F=0.0, univ=False),
            "B": dict(ecart=0.05, C=1500.0, F=10000.0, univ=False),
            "C": dict(ecart=0.0, C=1500.0, F=10000.0, univ=True)}

if __name__ == "__main__":
    for k, par in SYSTEMES.items():
        t = cale_systeme(**par)
        n, c = systeme(t, **par)
        d = v.deciles(n)
        pt = v.par_type(n)
        tr = v.par_tranche(n)
        ct = ct_systeme(t, **par)
        ct1 = ct_systeme(t, **par, plus=True)

        def ec(prof, br):
            g = CT[(CT.profil == prof) & (CT.brut == br)]
            i = g.index[0]
            return ct[i] - g.actuel.iloc[0], ct[i], (ct1[i] - ct[i]) / 10
        p("S9", f"système {k} {par} : travail {100*t:.1f} %, pensions et chômage {100*(t+par['ecart']):.1f} % ; coût {c:.1f} ;"
                f" redistribution {ex.redistribution(n):.2f}")
        p("S9", f"  déciles € " + " ".join(f"{u:+.0f}" for u in d.delta_eur) + " | pts " + " ".join(f"{u:+.1f}" for u in d.delta_pts))
        p("S9", f"  types Md€ " + " ; ".join(f"{i} {r.nouveau - r.actuel:+.1f}" for i, r in pt.iterrows())
              + f" ; RFR 200-300k {tr.delta_eur.iloc[8]:+,.0f} € ; 1-2M {tr[tr.a == 1000001].delta_pts.iloc[0]:+.1f} pts")
        for prof, br in (("seul", 21.5e3), ("seul", 30e3), ("seul", 50e3), ("seul", 100e3), ("couple_2enf", 30e3),
                         ("couple_2enf", 50e3), ("couple_2enf", 80e3), ("couple_0enf", 50e3), ("retraite_seul", 17e3),
                         ("retraite_seul", 30e3)):
            e_, n_, m_ = ec(prof, br)
            p("S9", f"  {prof} {br/1e3:.1f} k€ : {e_:+,.0f} € (proposé {n_:,.0f} €, marginal {m_:.1f} %)")
    (HERE / "sorties/systeme_efficace.txt").write_text("\n".join(L) + "\n", encoding="utf-8")
