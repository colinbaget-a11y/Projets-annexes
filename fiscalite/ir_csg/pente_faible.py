"""Barème à pente faible (décision de l'auteur, novembre 2026) : taux marginal en une seule ligne droite de t0
au premier euro jusqu'à 45 % en z2, puis 45 % ; z2 calé sur la recette. Deux parts pour un couple, crédit de
750 € par enfant, CRDS comprise, même barème pour tous les revenus après cotisations.
Lancer depuis fiscalite/ : python3 ir_csg/pente_faible.py
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE), str(HERE.parent)]
import bareme_v3 as v  # noqa: E402

T2, C = 0.45, 750.0


def ligne(t0, z2):
    tb = t0 + (T2 - t0) * v.ZB / z2
    z1 = z2 / 2
    t1 = t0 + (T2 - t0) * z1 / z2
    return v.famille(t0, tb, z1, t1, z2, T2)


def cale_z2(t0):
    lo, hi = 30e3, 3e6
    for _ in range(60):
        z2 = (lo * hi) ** 0.5
        _, T = ligne(t0, z2)
        lo, hi = (lo, z2) if (v.W * v.impot(T, C)).sum() / 1e9 < v.CIBLE else (z2, hi)
    return (lo * hi) ** 0.5


if __name__ == "__main__":
    for t0 in (0.07, 0.08, 0.09, 0.10, 0.11):
        z2 = cale_z2(t0)
        tm, T = ligne(t0, z2)
        n = v.impot(T, C)
        d = v.deciles(n)
        ct = v.cas_types(T, C)
        g = v.CT

        def ec(p, b):
            i = g[(g.profil == p) & (g.brut == b)].index[0]
            return ct[i] - g.actuel[i]
        print(f"t0={100*t0:.0f} % -> 45 % atteint à {z2/1e3:,.0f} k€ par part (pente {100*(T2-t0)/(z2/1e4):.2f} pt par 10 k€) ;"
              f" taux à 30 k€ {100*float(tm(30e3)):.1f} %, à 60 k€ {100*float(tm(60e3)):.1f} %, à 100 k€ {100*float(tm(100e3)):.1f} % ;"
              f" coût {v.cout(tm):.1f} Md€")
        print("   déciles € :", " ".join(f"{u:+.0f}" for u in d.delta_eur))
        print(f"   SMIC seul (21 500 €) {ec('seul', 21500):+.0f} ; seul 30k {ec('seul', 30000):+.0f} ; toi (61k) {float(T(54322.15)) - 12556:+.0f} ;"
              f" seul 100k {ec('seul', 100000):+.0f} ; couple 2 enf. 50k {ec('couple_2enf', 50000):+.0f}, 80k {ec('couple_2enf', 80000):+.0f} ;"
              f" retraité 15k {ec('retraite_seul', 15000):+.0f}, 17k {ec('retraite_seul', 17000):+.0f}, 30k {ec('retraite_seul', 30000):+.0f}")
        tr = v.par_tranche(n)
        print("   tranches RFR 100k-1M (pts) :", " ".join(f"{u:+.1f}" for u in tr[(tr.a >= 100e3) & (tr.a < 1e6)].delta_pts))
