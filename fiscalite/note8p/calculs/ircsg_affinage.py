"""Bloc IR-CSG-CRDS : affinage autour des barèmes retenus (taux ronds, seuil intermédiaire calé sur la recette),
mesure de la robustesse à la perception de la CSG. python3 note8p/calculs/ircsg_affinage.py -> sorties/ircsg_affinage.csv"""
import sys, itertools; sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
import ircsg_modele as R, numpy as np, pandas as pd
from multiprocessing import Pool
O=R.options()
def cale(S0,t0,t1,t2,S2):
    lo,hi=20e3,99e3
    f=lambda S1: R.recette(R.bareme([0,S0,S1,S2],[t0,t1,t2,.45]),O)-R.CIBLE
    if f(lo)<0 or f(hi)>0: return None
    for _ in range(40):
        m=(lo+hi)/2
        lo,hi=(lo,m) if f(m)<0 else (m,hi)
    return (lo+hi)/2
def go(a):
    S0,t0,t1,t2,S2=a
    S1=cale(S0,t0,t1,t2,S2)
    if S1 is None or S1<S0+10e3: return None
    s=R.bareme([0,S0,S1,S2],[t0,t1,t2,.45])
    r=dict(S0=S0,t0=t0,t1=t1,t2=t2,S1=S1,S2=S2,smic=float(s[1](19176.48))-2060.64, s2000=float(s[1](26889.37))-3714.43)
    for v in (1,.5,0):
        e=R.evalue(s,O,vue=v,vue_ext=1.0,repart=(v==1)); r[f'g{int(10*v)}']=e['gain']
        if v==1: r.update(empl=e['emplois']/1e3, ret=e['groupes']['retraites']['Md'], top1=e['top1_Md'], top10=e['top10_Md'], perd=e['perdants500'], c2=e['groupes']['couples2']['eur'])
    return r
if __name__ == "__main__":
    combos=list(itertools.product((12e3,14e3,16e3),(0.05,0.06,0.08,0.10),(0.17,0.18,0.19,0.20),(0.27,0.28,0.29,0.30,0.32),(100e3,120e3)))
    with Pool(4) as p: res=[r for r in p.map(go,combos,chunksize=8) if r]
    d=pd.DataFrame(res); d.to_csv(str(R.SORTIES / 'ircsg_affinage.csv'),index=False)
    pd.set_option('display.width',250)
    ok=d[(d.smic<=0)]
    print(len(d),len(ok))
    print(ok.sort_values('g5',ascending=False).head(30).round(3).to_string())
