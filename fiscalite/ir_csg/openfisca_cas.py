# Cas-types OpenFisca-France (législation revenus 2024) : facteurs brut -> imposable, CSG, IR, taux marginaux
import numpy as np
from openfisca_france import FranceTaxBenefitSystem
from openfisca_core.simulation_builder import SimulationBuilder
tbs = FranceTaxBenefitSystem()
P = "2024"
def sim(sal1=0, sal2=0, ret1=0, ret2=0, couple=False, enfants=0, rfr_n2=None):
    ind = {"d1": {}}
    if couple: ind["d2"] = {}
    for k in range(enfants): ind[f"e{k}"] = {"date_naissance": {"ETERNITY": "2015-01-01"}}
    def put(p, v, var):
        if v: ind[p].setdefault(var, {})[P] = v
    put("d1", sal1, "salaire_de_base"); put("d1", ret1, "retraite_brute")
    if couple: put("d2", sal2, "salaire_de_base"); put("d2", ret2, "retraite_brute")
    ind["d1"]["date_naissance"] = {"ETERNITY": "1950-01-01" if ret1 else "1980-01-01"}
    if couple: ind["d2"]["date_naissance"] = {"ETERNITY": "1950-01-01" if ret2 else "1980-01-01"}
    adultes = ["d1"] + (["d2"] if couple else [])
    enf = [f"e{k}" for k in range(enfants)]
    case = {"individus": ind,
            "foyers_fiscaux": {"f": {"declarants": adultes, "personnes_a_charge": enf, **({"rfr": {"2022": rfr_n2}, "nbptr": {"2022": (2 if couple else 1) + 0.5*min(enfants,2) + max(enfants-2,0)}} if rfr_n2 is not None else {})}},
            "menages": {"m": {"personne_de_reference": ["d1"], **({"conjoint": ["d2"]} if couple else {}), "enfants": enf}},
            "familles": {"fa": {"parents": adultes, "enfants": enf}}}
    s = SimulationBuilder().build_from_entities(tbs, case)
    g = lambda v: float(np.sum(s.calculate_add(v, P)))
    out = dict(
        sal_imp=g("salaire_imposable"), ret_imp=g("retraite_imposable"),
        csg_sal=-(g("csg_deductible_salaire") + g("csg_imposable_salaire")),
        csg_ret=-(g("csg_deductible_retraite") + g("csg_imposable_retraite")),
        ir=-float(s.calculate("impot_revenu_restant_a_payer", P).sum()), rfr=float(s.calculate("rfr", P).sum()))
    return out
def sim2(**kw):
    """Régime stationnaire : le RFR N-2 (qui fixe le taux de CSG des pensions) = RFR de l'année."""
    o = sim(**kw)
    for _ in range(2):
        o = sim(rfr_n2=o["rfr"], **kw)
    return o
if __name__ == "__main__":
    import sys
    print("salarié seul : brut annuel -> imposable, facteur brut/imposable, CSG/brut, IR")
    for b in [21000, 30000, 45000, 70000, 120000, 250000]:
        o = sim(sal1=b)
        print(b, round(o["sal_imp"]), round(b / o["sal_imp"], 3), round(o["csg_sal"] / b, 4), round(o["ir"]))
    print("retraité seul : brut -> imposable, facteur, CSG/brut, IR")
    for b in [12000, 18000, 24000, 30000, 45000, 80000]:
        o = sim2(ret1=b)
        print(b, round(o["ret_imp"]), round(b / max(o["ret_imp"],1), 3), round(o["csg_ret"] / b, 4), round(o["ir"]), round(o["rfr"]))
    print("couple retraités (deux pensions égales) : brut total, facteur, CSG/brut")
    for b in [24000, 36000, 50000, 70000]:
        o = sim2(ret1=b/2, ret2=b/2, couple=True)
        print(b, round(b / max(o["ret_imp"],1), 3), round(o["csg_ret"] / b, 4), round(o["ir"]), round(o["rfr"]))
