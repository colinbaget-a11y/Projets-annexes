"""Faisabilité : caler la part des revenus au PFU par tranche sur l'IR observé (IRCOM), au lieu des conventions
prorata / haut / mixte. IR observé = 12,8 % × PFU + IR du barème (quotient conjugal selon la part de couples du
modèle, sans enfant, sans niche, sans CEHR) sur le reste du RFR. Lancer depuis fiscalite/."""
import sys
import numpy as np, pandas as pd
sys.path[:0] = ["/home/user/Projets-annexes/fiscalite/ir_csg", "/home/user/Projets-annexes/fiscalite"]
import bareme_lisse as bl
x = bl.x
S_k = pd.Series(bl.S_COUPLE).groupby(bl.f.tranche.values).mean().reindex(x.tranche).values
IRS, IRT = [0, 11497, 29315, 83823, 180294], [0, .11, .30, .41, .45]
def bar(q):
    return sum(t * np.clip(np.minimum(q, h) - s, 0, None) for s, h, t in zip(IRS, IRS[1:] + [np.inf], IRT))
def ir_bar(y, s):
    return s * 2 * bar(y / 2) + (1 - s) * bar(y)
print(f"{'tranche':<24} {'IR obs':>7} {'PFU mixte':>9} {'PFU calé':>9} {'autres':>7} {'part calée':>10} {'taux barème mixte':>17} {'calé':>6}")
tot_m = tot_c = 0
for i, r in x.iterrows():
    if r.a < 100e3:
        continue
    n = r.foyers
    def ir_pred(c):
        y = (r.rfr - c) * 1e9 / n
        return 0.128 * c + n * ir_bar(y, S_k[i]) / 1e9
    lo, hi = 0.0, r.autres
    if ir_pred(hi) > r.ir:
        c = hi
    else:
        for _ in range(60):
            mid = (lo + hi) / 2
            lo, hi = (mid, hi) if ir_pred(mid) > r.ir else (lo, mid)
        c = (lo + hi) / 2
    yb_m = r.rfr - r.capital
    tm = (r.ir - min(0.128 * r.capital, r.ir)) / yb_m
    tc = (r.ir - 0.128 * c) / (r.rfr - c)
    tot_m += r.capital; tot_c += c
    print(f"{r.tranche:<24} {r.ir:7.2f} {r.capital:9.2f} {c:9.2f} {r.autres:7.2f} {100*c/r.autres:9.0f} % {100*tm:16.1f} % {100*tc:5.1f} %")
print(f"PFU logé au-delà de 100 k€ : mixte {tot_m:.1f} Md€, calé {tot_c:.1f} Md€ (total national supposé : 90)")
