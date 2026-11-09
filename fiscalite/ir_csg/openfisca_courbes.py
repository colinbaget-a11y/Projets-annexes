# Courbes fines du système actuel (IR + CSG, revenus 2024), vectorisées : une seule simulation OpenFisca
# par profil, sur une grille de 500 € en 500 € de revenu brut (2 000 € au-delà de 200 000 €) ; taux marginal = impôt supplémentaire
# pour 1 000 € de revenu brut en plus (l'IR est arrondi à l'euro : sur 100 €, cela crée des dents de scie).
# Usage (depuis fiscalite/ir_csg, avec openfisca-france installé) : python openfisca_courbes.py
#   -> sorties/courbes_openfisca.csv : profil, brut, ir, csg, ir_plus, csg_plus (pour brut + 1 000 €), crds, casa (et _plus), rfr
import csv
import numpy as np
from openfisca_france import FranceTaxBenefitSystem
from openfisca_core.simulation_builder import SimulationBuilder

TBS = FranceTaxBenefitSystem()
P = "2024"
DELTA = 1000.0


def simule(revenus, profil, rfr_n2=None):
    ind, foy, men, fam = {}, {}, {}, {}
    for k, g in enumerate(revenus):
        a, b = f"a{k}", f"b{k}"
        retraite = profil == "retraite_seul"
        ind[a] = {"date_naissance": {"ETERNITY": "1950-01-01" if retraite else "1980-01-01"}}
        if retraite:
            ind[a]["retraite_brute"] = {P: g}
        elif profil == "seul":
            ind[a]["salaire_de_base"] = {P: g}
        else:
            part = 1.0 if profil.endswith("mono") else 0.6
            ind[a]["salaire_de_base"] = {P: part * g}
            ind[b] = {"date_naissance": {"ETERNITY": "1980-01-01"}, "salaire_de_base": {P: (1 - part) * g}}
        enf = []
        if profil.startswith("couple_2enf"):
            for j in range(2):
                e = f"e{k}_{j}"
                ind[e] = {"date_naissance": {"ETERNITY": "2015-01-01"}}
                enf.append(e)
        adultes = [a] + ([b] if profil.startswith("couple") else [])
        foy[f"f{k}"] = {"declarants": adultes, "personnes_a_charge": enf}
        if rfr_n2 is not None:
            foy[f"f{k}"]["rfr"] = {"2022": float(rfr_n2[k])}
            foy[f"f{k}"]["nbptr"] = {"2022": 1.0}
        men[f"m{k}"] = {"personne_de_reference": [a], "enfants": enf, **({"conjoint": [b]} if len(adultes) > 1 else {})}
        fam[f"fa{k}"] = {"parents": adultes, "enfants": enf}
    s = SimulationBuilder().build_from_entities(TBS, {"individus": ind, "foyers_fiscaux": foy, "menages": men,
                                                      "familles": fam})
    ir = -s.calculate("impot_revenu_restant_a_payer", P)
    csg_i = -(s.calculate_add("csg_deductible_salaire", P) + s.calculate_add("csg_imposable_salaire", P)
              + s.calculate_add("csg_deductible_retraite", P) + s.calculate_add("csg_imposable_retraite", P))
    csg_f = s.foyer_fiscal.sum(csg_i)
    crds_i = -(s.calculate_add("crds_salaire", P) + s.calculate_add("crds_retraite", P))
    casa_i = -s.calculate_add("casa", P)
    # assiette du nouvel impôt, par adulte : revenu après cotisations sociales, avant CSG et CRDS
    net_i = (s.calculate_add("salaire_de_base", P) + s.calculate_add("cotisations_salariales", P)
             + s.calculate_add("retraite_brute", P))
    ids = list(ind)
    pos = {i: k for k, i in enumerate(ids)}
    base_a = np.array([net_i[pos[f"a{k}"]] for k in range(len(revenus))])
    base_b = np.array([net_i[pos[f"b{k}"]] if f"b{k}" in pos else 0.0 for k in range(len(revenus))])
    return (ir, csg_f, s.foyer_fiscal.sum(crds_i), s.foyer_fiscal.sum(casa_i), s.calculate("rfr", P),
            base_a, base_b)


def main():
    grille = np.arange(5000, 200001, 500.0)
    grille = np.concatenate([grille, np.arange(202000, 400001, 2000.0)])
    rows = []
    for profil in ("seul", "couple_0enf", "couple_2enf", "couple_2enf_mono", "retraite_seul"):
        x = np.concatenate([grille, grille + DELTA])
        ir, csg, crds, casa, rfr, ba, bb = simule(x, profil)
        if profil == "retraite_seul":          # taux de CSG des pensions : RFR N-2 = RFR de l'année
            for _ in range(2):
                ir, csg, crds, casa, rfr, ba, bb = simule(x, profil, rfr_n2=rfr)
        n = len(grille)
        for k, g in enumerate(grille):
            rows.append(dict(profil=profil, brut=g, ir=round(float(ir[k]), 2), csg=round(float(csg[k]), 2),
                             ir_plus=round(float(ir[n + k]), 2), csg_plus=round(float(csg[n + k]), 2),
                             crds=round(float(crds[k]), 2), crds_plus=round(float(crds[n + k]), 2),
                             casa=round(float(casa[k]), 2), casa_plus=round(float(casa[n + k]), 2),
                             base_a=round(float(ba[k]), 2), base_b=round(float(bb[k]), 2),
                             base_a_plus=round(float(ba[n + k]), 2), base_b_plus=round(float(bb[n + k]), 2),
                             rfr=round(float(rfr[k]))))
        print(profil, "ok")
    with open("sorties/courbes_openfisca.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=rows[0].keys())
        w.writeheader()
        w.writerows(rows)


if __name__ == "__main__":
    main()
