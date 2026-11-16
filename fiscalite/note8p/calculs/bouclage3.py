"""Bouclage v3 (CONSIGNES_V3.md) : solde ≥ 0 chaque année de 2027 à 2040, sans dette.

Entrées (années de caisse) : sorties/ircsg3.json (annuel_final, sinon F0), foncier3.json (B_E10), is3.json (annuel_caisse :
fin du taux réduit prudente, noyau de niches, déduction de 50 % départ exercice 2029), pfu3.json (fin de l'effacement,
scénario prudent : réserve, ne finance rien). Unités : Md€ constants de 2027 environ ; les séries IS, nominales (+3 %/an),
sont déflatées par leur croissance. Choix [C] : enveloppe foncière de 10 Md€ ; financement externe de l'impôt sur le
revenu par paliers (FIN). Scénario prudent : noyau de niches IS −25 %, coût de la déduction +20 % (part imposable 90 %),
taxe foncière nouvelle −10 % (capitalisation plus forte) ; les paliers de baisse de l'impôt sur le revenu ne sont
accordés qu'au vu des recettes constatées (même clause que les droits de mutation).
Sorties : sorties/bouclage3.json, bouclage3.txt.
"""
import json
from pathlib import Path

S = Path(__file__).resolve().parent.parent / "sorties"
Y = [str(a) for a in range(2027, 2041)]
L = lambda n: json.loads((S / n).read_text(encoding="utf-8"))
IR, FO, IS, PF = L("ircsg3.json"), L("foncier3.json"), L("is3.json"), L("pfu3.json")
E = "B_E10"
FIN = {"2032": 1.0, "2033": 2.0, "2034": 3.0, "2035": 4.0, "2036": 5.0}
DEF = lambda y: 1.03 ** (int(y) - 2027)


def fin(y):
    v = 0.0
    for k in sorted(FIN):
        if y >= k:
            v = FIN[k]
    return 5.5 if y >= "2037" else v


def ligne(y, prudent=False):
    c = IS["annuel_caisse"][y]
    f = FO["annuel_par_scenario"][E][y]
    ir_fin = IR.get("annuel_final", {}).get(y)
    ir = ir_fin["ircsg_total"] if ir_fin else IR["annuel"]["F0"][y]["ircsg_total"] - fin(y)
    tr = c.get("is_fin_taux_reduit_prudent", 0) / DEF(y)
    ni = c.get("is_niches_noyau", 0) / DEF(y)
    de = c.get("is_deduction_50_depart_2029", 0) / DEF(y)
    tf, dm = f["taxe_fonciere_nouvelle"], f["dmto"]
    autres = f["net"] - tf - dm
    if prudent:
        ni, de, tf = 0.75 * ni, 1.2 * de, 0.9 * tf
    r = {"ircsg_fusion": ir + fin(y), "ircsg_financement_externe": -fin(y), "taxe_fonciere": tf, "dmto": dm,
         "foncier_autres": autres, "is_taux_reduit": tr, "is_niches": ni, "is_deduction_50": de,
         "reserve_plus_values": PF["annuel"][y]["fin_effacement_prudent"]}
    r["solde"] = sum(v for k, v in r.items() if k != "reserve_plus_values")
    return r


res = {y: ligne(y) for y in Y}
pru = {y: ligne(y, True) for y in Y}
out = {"annuel": res, "prudent": pru, "financement_ir": {y: fin(y) for y in Y}, "enveloppe": E, "notes": __doc__}
(S / "bouclage3.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
txt = [f"{y} | " + " | ".join(f"{k} {v:+.2f}" for k, v in res[y].items()) + f" || prudent {pru[y]['solde']:+.2f}" for y in Y]
(S / "bouclage3.txt").write_text("\n".join(txt) + "\n", encoding="utf-8")
print("\n".join(f"{y} solde {res[y]['solde']:+.2f}  prudent {pru[y]['solde']:+.2f}  fin IR {fin(y)}" for y in Y))
