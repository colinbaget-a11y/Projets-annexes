"""Sensibilité du coin non contributif au droit 2026 (réduction générale dégressive unique, sortie à 3 Smic, Tmin
0,02, Tdelta 0,378, exposant 1,75 ; formule lue sur des sources secondaires et une FAQ Agirc-Arrco, non vérifiée sur
le décret) au lieu de la réduction générale 2025 (sortie à 1,6 Smic, pente 0,3194 / 0,6 ≈ 0,532). Bandeaux inchangés.
Lancer depuis fiscalite/."""
import sys
import numpy as np
sys.path.insert(0, "/tmp/claude-0/-home-user-Projets-annexes/935fc156-45bd-500a-b52a-e7e4ee23abb6/scratchpad/verif_ircsg/hyp")
import v2_independant as V
ps = V.ps
coin0 = ps.coin
def pente_rgdu(x):
    u = np.clip(0.5 * (3 / x - 1), 0, None)
    C = 0.02 + 0.378 * u ** 1.75
    dC = 0.378 * 1.75 * u ** 0.75 * 0.5 * (-3 / x ** 2)
    return np.where((x >= 1) & (x < 3), -(C + x * dC), 0.0)
def coin26(g, single, conv):
    er, ee, pa = coin0(g, single, conv)
    x = np.asarray(g, float) / ps.SMIC
    er = er - np.where((x >= 1) & (x < 1.6), 0.532, 0.0) + pente_rgdu(np.maximum(x, 1e-9))
    return er, ee, pa
print("pente marginale de la réduction (par € de brut) à 1 / 1,25 / 1,5 / 2 / 2,5 / 2,9 Smic : "
      + " ".join(f"{float(pente_rgdu(np.array(x))):.3f}" for x in (1.0, 1.25, 1.5, 2.0, 2.5, 2.9)) + " (2025 : 0,532 jusqu'à 1,6 Smic)")
cas = {"neutre": (V.bar(.02, .14, 30e3, .2302, 250e3), {}),
       "proposition": (V.lineaire([0, 20e3, 45e3, 1e6], [.14, .14, .3027, .5]), dict(F=4000.0, fam="franchise", Fp=12500.0, deg=True)),
       "atteignable": (V.lineaire([0, 20e3, 60e3, 2e6], [.16, .16, .1637, .5]), dict(F=4000.0))}
for nom, ((tm, T), o) in cas.items():
    ps.coin = coin0
    a = V.ps_v2(tm, T, o)
    ps.coin = coin26
    b = V.ps_v2(tm, T, o)
    print(f"{nom:<12} coin 2025 : {a[0]:+.2f} [intensive par groupe " + " ".join(f"{u:+.2f}" for u in a[1]) + f"] | coin 2026 : {b[0]:+.2f} ["
          + " ".join(f"{u:+.2f}" for u in b[1]) + "]")
ps.coin = coin0
