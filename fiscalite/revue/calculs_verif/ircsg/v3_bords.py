"""Bords de grille : barème neutre (t0 = 2 % est le minimum de la grille), gain atteignable et proposition
(z2 = 2 M€ et 1 M€ sont les maxima de leurs grilles). Lancer depuis fiscalite/."""
import itertools, sys
import numpy as np
sys.path.insert(0, "/tmp/claude-0/-home-user-Projets-annexes/935fc156-45bd-500a-b52a-e7e4ee23abb6/scratchpad/verif_ircsg/hyp")
import v2_independant as V

def cale_t1(t0, tb, z1, z2, o):
    if V.recette(*V.lineaire([0, 20e3, z1, z2], [t0, tb, .5, .5]), o) < V.CIBLE:
        return None
    return V.cale(lambda t: V.recette(*V.lineaire([0, 20e3, z1, z2], [t0, tb, t, .5]), o), 0, .5, 30)

def ecart(t0, tb, z1, t1, z2, o):
    tm, T = V.lineaire([0, 20e3, z1, z2], [t0, tb, t1, .5])
    tot = 0.0
    for nom, g, fam, w, parts, k in V.TYPES:
        tot += (w * np.abs(V.impot(tm, T, o, g, parts, k)[0] - V.M.CURT[nom])).sum()
    return tot / V.W.sum()

print("1. Barème neutre : écart absolu moyen à la charge actuelle (€ par foyer), t0 de 0 à 3 %")
rows = []
for t0, tb, z1, z2 in itertools.product([0.0, 0.01, 0.02, 0.03], [0.12, 0.13, 0.14, 0.15, 0.16], [25e3, 30e3, 35e3, 40e3], [200e3, 250e3, 300e3]):
    t1 = cale_t1(t0, tb, z1, z2, {})
    if t1 is None or t1 < tb:
        continue
    rows.append((ecart(t0, tb, z1, t1, z2, {}), t0, tb, z1, t1, z2))
rows.sort()
for r in rows[:6]:
    print(f"   écart {r[0]:.1f} € : {100*r[1]:.0f} % / {100*r[2]:.0f} % à 20 k / {100*r[4]:.1f} % à {r[3]/1e3:.0f} k / 50 % à {r[5]/1e3:.0f} k")
best = rows[0]
tm, T = V.lineaire([0, 20e3, best[3], best[5]], [best[1], best[2], best[4], .5])
print("   perte sèche v2 du meilleur :", round(V.ps_v2(tm, T, {})[0], 2), "(barème neutre publié : -4,02)")

print("2. Gain atteignable avec franchise 4 000 € : prolonger z2 au-delà de 2 M€")
o4 = dict(F=4000.0)
best = []
for t0, tb, z1, z2 in itertools.product([0.14, 0.16, 0.18], [0.14, 0.16, 0.18], [45e3, 60e3, 90e3], [2e6, 3e6, 5e6, 1e7]):
    if tb < t0:
        continue
    t1 = cale_t1(t0, tb, z1, z2, o4)
    if t1 is None or t1 < tb:
        continue
    tm, T = V.lineaire([0, 20e3, z1, z2], [t0, tb, t1, .5])
    best.append((V.ps_v2(tm, T, o4)[0], t0, tb, z1, t1, z2))
best.sort()
for r in best[:5]:
    print(f"   PS {r[0]:+.2f} : {100*r[1]:.0f} / {100*r[2]:.0f} / {100*r[4]:.1f} % à {r[3]/1e3:.0f} k / 50 % à {r[5]/1e6:.0f} M€")
print("   (publié : -7,75 avec z2 = 2 M€)")
print("   taux supérieur 45 % ou 55 % au lieu de 50 % (même famille, z2 = 2 M€) :")
for top in (0.45, 0.55, 0.60):
    t1 = V.cale(lambda t: V.recette(*V.lineaire([0, 20e3, 60e3, 2e6], [.16, .16, t, top]), o4), 0, top, 30)
    tm, T = V.lineaire([0, 20e3, 60e3, 2e6], [.16, .16, t1, top])
    print(f"      top {100*top:.0f} % : t1 {100*t1:.1f} % ; PS {V.ps_v2(tm, T, o4)[0]:+.2f}")

print("3. Proposition : z2 au-delà de 1 M€ (contrainte : aucun décile > 500 €, 1 % du haut ne monte pas)")
oP = dict(F=4000.0, fam="franchise", Fp=12500.0, deg=True)
ok = []
for t0, tb, z1, z2 in itertools.product([0.12, 0.14, 0.16], [0.14, 0.16, 0.18], [30e3, 45e3, 60e3], [6e5, 1e6, 2e6, 4e6]):
    if tb < t0:
        continue
    t1 = cale_t1(t0, tb, z1, z2, oP)
    if t1 is None or t1 < tb:
        continue
    tm, T = V.lineaire([0, 20e3, z1, z2], [t0, tb, t1, .5])
    rp = V.repart(tm, T, oP)
    if max(abs(u) for u in rp["dec"]) <= 500 and rp["top1"] <= 0:
        ok.append((V.ps_v2(tm, T, oP)[0], t0, tb, z1, t1, z2, rp["top1"], rp["perdants"]))
ok.sort()
for r in ok[:5]:
    print(f"   PS {r[0]:+.2f} : {100*r[1]:.0f} / {100*r[2]:.0f} / {100*r[4]:.1f} % à {r[3]/1e3:.0f} k / 50 % à {r[5]/1e6:.1f} M€ ; 1 % {r[6]:+.1f} ; perdants {r[7]} %")
print("   (publié : -4,86 avec 14 / 14 / 30,3 % à 45 k / 50 % à 1 M€)")
