# Courbes fines du système actuel (IR + CSG, revenus 2024) pour la note pédagogique.
# Usage (depuis fiscalite/ir_csg, avec openfisca-france installé) : python openfisca_courbes.py
#   -> sorties/courbes_openfisca.csv : profil, brut (revenu brut annuel du foyer), ir, csg, rfr
import csv
import numpy as np
from openfisca_cas import sim, sim2

profils = {
    "seul": lambda g: dict(sal1=g),
    "couple_2enf": lambda g: dict(sal1=0.6 * g, sal2=0.4 * g, couple=True, enfants=2),
    "retraite_seul": lambda g: dict(ret1=g),
}
grille = np.round(np.exp(np.linspace(np.log(6e3), np.log(300e3), 90)), -1)
rows = []
for nom, f in profils.items():
    run = sim2 if "retraite" in nom else sim
    for g in grille:
        o = run(**f(g))
        rows.append(dict(profil=nom, brut=g, ir=round(o["ir"], 2), csg=round(o["csg_sal"] + o["csg_ret"], 2), rfr=round(o["rfr"])))
    print(nom, "ok")
with open("sorties/courbes_openfisca.csv", "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=rows[0].keys())
    w.writeheader()
    w.writerows(rows)
