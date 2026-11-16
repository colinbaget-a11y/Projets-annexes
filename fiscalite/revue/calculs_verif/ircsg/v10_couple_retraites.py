"""Hypothèse « couple de retraités = couple d'actifs × (retraité seul / actif seul) à la moitié du revenu » contre la
courbe OpenFisca d'un couple de retraités (of/couple_retraites.csv). Effet sur la charge actuelle des retraités et sur
la répartition du barème neutre et de la proposition. Lancer depuis fiscalite/."""
import sys
import numpy as np, pandas as pd
sys.path.insert(0, "/tmp/claude-0/-home-user-Projets-annexes/935fc156-45bd-500a-b52a-e7e4ee23abb6/scratchpad/verif_ircsg/hyp")
import v2_independant as V
M = V.M
c = pd.read_csv("/tmp/claude-0/-home-user-Projets-annexes/935fc156-45bd-500a-b52a-e7e4ee23abb6/scratchpad/verif_ircsg/hyp/of/couple_retraites.csv")
r_of = lambda z: np.interp(z, c.pension_totale, c.charge / c.pension_totale)
for z in (20e3, 30e3, 40e3, 50e3, 80e3, 150e3):
    a = float(M.r_c0(z) * M.rho(z / 2)); b = float(r_of(z))
    print(f"couple de retraités, pension totale {z/1e3:.0f} k€ : taux du modèle {100*a:.1f} % ; OpenFisca {100*b:.1f} %")
def refait(U):
    key = lambda n: n if n in U else n.rsplit("_", 1)[0]
    norm = sum(w * U[key(n)] for n, _, _, w, _, _ in V.TYPES) / M.W
    return {n: M.CUR * U[key(n)] / norm for n, *_ in V.TYPES}
cur0 = dict(M.CURT)
U1 = dict(M._U); U1["retraite_couple"] = M.ZN * r_of(M.ZN)
cur1 = refait(U1)
for lab, cur in (("modèle", cur0), ("couple de retraités OpenFisca", cur1)):
    M.CURT.clear(); M.CURT.update(cur)
    chR = sum((w * cur[n]).sum() for n, g, f, w, p, k in V.TYPES if g == "R") / 1e9
    out = [f"charge actuelle des retraités {chR:.1f} Md€"]
    for nom, (tm, T), o in (("neutre", V.bar(.02, .14, 30e3, .2302, 250e3), {}),
                            ("proposition", V.lineaire([0, 20e3, 45e3, 1e6], [.14, .14, .3027, .5]), dict(F=4000.0, fam="franchise", Fp=12500.0, deg=True))):
        rp = V.repart(tm, T, o); g = rp["groupes"]
        out.append(f"{nom} : retraités {g['retraites'][0]:+.1f} Md€, couples de retraités {g['couples_retraites'][1]:+,} €, retraités seuls {g['seuls_retraites'][1]:+,} €, actifs {g['actifs'][0]:+.1f} ; déciles max {max(abs(u) for u in rp['dec'])} ; perdants {rp['perdants']} %")
    print(f"[{lab}] " + " | ".join(out))
M.CURT.clear(); M.CURT.update(cur0)
