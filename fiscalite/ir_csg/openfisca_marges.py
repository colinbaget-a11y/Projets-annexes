# Usage (depuis fiscalite/ir_csg, dans un environnement où openfisca-france est installé) :
#   python openfisca_marges.py  ->  sorties/marges_openfisca.csv
# Taux marginaux et moyens actuels IR + CSG (OpenFisca, revenus 2024) pour des cas-types,
# exprimés en % de l'assiette CSG brute (98,25 % du brut salarial ; pension brute)
import csv, numpy as np
from openfisca_cas import sim, sim2
prof = {
 "seul":            lambda g: dict(sal1=g),
 "couple_2act":     lambda g: dict(sal1=0.6*g, sal2=0.4*g, couple=True),
 "couple_1act":     lambda g: dict(sal1=g, couple=True),
 "couple_2act_2enf":lambda g: dict(sal1=0.6*g, sal2=0.4*g, couple=True, enfants=2),
 "retraite_seul":   lambda g: dict(ret1=g),
 "retraites_couple":lambda g: dict(ret1=0.6*g, ret2=0.4*g, couple=True),
}
def charge(o, kw):
    return o["ir"] + o["csg_sal"] + o["csg_ret"]
def assiette(kw):
    return 0.9825*(kw.get("sal1",0)+kw.get("sal2",0)) + kw.get("ret1",0) + kw.get("ret2",0)
rows=[]
for nom, f in prof.items():
    for g in [12e3,16e3,20e3,25e3,30e3,37e3,45e3,55e3,70e3,90e3,120e3,160e3,220e3,300e3,450e3]:
        k0, k1 = f(g), f(g*1.03)
        run = sim2 if "retrait" in nom else sim
        o0, o1 = run(**k0), run(**k1)
        c0, c1 = charge(o0,k0), charge(o1,k1)
        a0, a1 = assiette(k0), assiette(k1)
        rows.append(dict(profil=nom, brut=g, rfr=round(o0["rfr"]), assiette=round(a0), taux_moyen=round(c0/a0,4), taux_marginal=round((c1-c0)/(a1-a0),4)))
        print(rows[-1])
with open("sorties/marges_openfisca.csv","w",newline="") as fh:
    w=csv.DictWriter(fh, fieldnames=rows[0].keys()); w.writeheader(); w.writerows(rows)
