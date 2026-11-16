"""Charge actuelle (IR + CSG + CRDS, législation 2024) d'un couple de retraités, pour modele_purs.py.

Pourquoi : modele_purs.py approchait la charge d'un couple de retraités par celle d'un couple d'actifs multipliée par le
rapport retraité seul / actif seul à la moitié du revenu. Cela revient à supposer que les seuils de CSG des pensions
d'un couple valent deux fois ceux d'une personne seule ; or ils valent le seuil d'une part plus deux demi-parts
(revenus 2024 : 12 230 + 2 × 3 265 = 18 760 € de RFR pour l'exonération, au lieu de 24 460 €). La charge des couples
de retraités entre 25 000 et 50 000 € de pension était sous-estimée de 3 à 7 points (revue/hypotheses_ircsg.md).

Cas-type : deux retraités nés en 1950, pensions 60/40 (la charge d'un couple soumis à imposition commune ne dépend
presque pas du partage), sans autre revenu ; même version d'OpenFisca-France (176.1) et même convention que
ir_csg/openfisca_courbes.py pour le taux de CSG (RFR N-2 = RFR de l'année) ; aux seuils, le taux alterne d'un passage
à l'autre : on garde la moyenne des deux derniers passages.

Lancer avec un Python où openfisca-france est installé, depuis fiscalite/ :
    python3.13 synthese/openfisca_couple_retraites.py  ->  synthese/sorties/couple_retraites_openfisca.csv
"""
import csv
from pathlib import Path

import numpy as np
from openfisca_core.simulation_builder import SimulationBuilder
from openfisca_france import FranceTaxBenefitSystem

TBS = FranceTaxBenefitSystem()
P = "2024"
OUT = Path(__file__).resolve().parent / "sorties/couple_retraites_openfisca.csv"


def simule(gs, rfr_n2=None):
    ind, foy, men, fam = {}, {}, {}, {}
    for k, g in enumerate(gs):
        a, b = f"a{k}", f"b{k}"
        ind[a] = {"date_naissance": {"ETERNITY": "1950-01-01"}, "retraite_brute": {P: 0.6 * g}}
        ind[b] = {"date_naissance": {"ETERNITY": "1950-01-01"}, "retraite_brute": {P: 0.4 * g}}
        foy[f"f{k}"] = {"declarants": [a, b]}
        if rfr_n2 is not None:
            foy[f"f{k}"]["rfr"] = {"2022": float(rfr_n2[k])}
            foy[f"f{k}"]["nbptr"] = {"2022": 2.0}
        men[f"m{k}"] = {"personne_de_reference": [a], "conjoint": [b]}
        fam[f"fa{k}"] = {"parents": [a, b]}
    s = SimulationBuilder().build_from_entities(TBS, {"individus": ind, "foyers_fiscaux": foy, "menages": men,
                                                      "familles": fam})
    ir = -s.calculate("impot_revenu_restant_a_payer", P)
    csg = -(s.calculate_add("csg_deductible_retraite", P) + s.calculate_add("csg_imposable_retraite", P))
    crds = -s.calculate_add("crds_retraite", P)
    return ir + s.foyer_fiscal.sum(csg) + s.foyer_fiscal.sum(crds), s.calculate("rfr", P)


if __name__ == "__main__":
    gs = np.concatenate([np.arange(4000, 100001, 1000.0), np.arange(102000, 200001, 4000.0),
                         np.arange(210000, 400001, 10000.0), np.array([600e3, 1e6, 2e6])])
    c, r = simule(gs)
    passes = []
    for _ in range(4):
        c, r = simule(gs, r)
        passes.append(c)
    charge = 0.5 * (passes[-1] + passes[-2])
    with open(OUT, "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["pension_totale", "charge", "charge_passe_a", "charge_passe_b", "rfr"])
        for g, ch, pa, pb, rr in zip(gs, charge, passes[-2], passes[-1], r):
            w.writerow([g, round(float(ch), 2), round(float(pa), 2), round(float(pb), 2), round(float(rr))])
    print(f"{len(gs)} points ; points où le taux de CSG alterne : {int((np.abs(passes[-1] - passes[-2]) > 1).sum())}")
