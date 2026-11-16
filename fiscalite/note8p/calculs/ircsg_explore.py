"""Bloc IR-CSG-CRDS : exploration de barèmes simples en tranches (python3 note8p/calculs/ircsg_explore.py).

Famille : taux t0 de 0 à S0 (t0 = 0 : seuil d'exonération), t1 de S0 à S1, t2 = t1 + d de S1 à S2, t3 au-delà
(≤ 50 %). t1 et t2 sont calés ensemble sur la recette du périmètre. Franchise de 6 000 € par enfant, impôt individuel.
Sortie : note8p/sorties/ircsg_explore.csv (une ligne par barème, gains de perte sèche selon trois perceptions de la CSG,
répartition) ; aucun barème n'est choisi ici.
"""
import itertools
from multiprocessing import Pool

import numpy as np
import pandas as pd

import ircsg_modele as R

O = R.options(fe=6000.0)


def essai(a):
    S0, t0, S1, S2, t3, d = a
    seuils = [0.0, S0, S1, S2] if S0 > 0 else [0.0, S1, S2]
    base = [t0, 0.15, 0.15 + d, t3] if S0 > 0 else [0.15, 0.15 + d, t3]
    lib = [1, 2] if S0 > 0 else [0, 1]
    tt = R.cale_echelle(seuils, base, lib, O)
    if tt[lib[0]] < t0 or tt[lib[1]] > t3 or tt[lib[0]] < 0.02:
        return None
    s = R.bareme(seuils, tt)
    r = dict(S0=S0, t0=t0, S1=S1, S2=S2, t3=t3, d=d, t1=tt[lib[0]], t2=tt[lib[1]])
    for v in (1.0, 0.5, 0.0):
        e = R.evalue(s, O, vue=v, repart=(v == 1.0))
        r[f"gain_v{int(10*v)}"] = e["gain"]
        r[f"ext_v{int(10*v)}"] = -e["ext"]
        if v == 1.0:
            r.update(emplois=e["emplois"], retraites=e["groupes"]["retraites"]["Md"], actifs=e["groupes"]["actifs"]["Md"],
                     couples2=e["groupes"]["couples2"]["eur"], pi=e["groupes"]["parents_isoles"]["eur"],
                     top1=e["top1_Md"], top10=e["top10_Md"], decmax=max(e["dec_eur"]), decmin=min(e["dec_eur"]),
                     perd500=e["perdants500"], decl=e["decl"])
    for v in (0.5, 0.0):
        r[f"gain_v{int(10*v)}_e10"] = R.evalue(s, O, vue=v, vue_ext=1.0)["gain"]
    for j in ("bas", "haut"):
        r["gain_" + j] = R.evalue(s, O, jeu=j)["gain"]
    return r


if __name__ == "__main__":
    combos = []
    for S0, t0 in [(0.0, 0.0)] + list(itertools.product((6e3, 8e3, 10e3, 12e3), (0.0, 0.05, 0.10))):
        for S1, S2, t3, d in itertools.product((35e3, 40e3, 50e3), (80e3, 100e3, 150e3), (0.40, 0.45, 0.50),
                                               (0.0, 0.05, 0.10, 0.15)):
            combos.append((S0, t0, S1, S2, t3, d))
    with Pool(4) as p:
        res = [r for r in p.map(essai, combos, chunksize=8) if r]
    df = pd.DataFrame(res)
    df.to_csv(R.SORTIES / "ircsg_explore.csv", index=False)
    print(len(combos), len(df))
