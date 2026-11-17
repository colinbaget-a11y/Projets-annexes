"""Bloc IR-CSG v4 : cas-types réalistes au droit actuel AVEC leurs niches (OpenFisca-France 176.1, droit des revenus 2025).
Lancer depuis fiscalite/ :  python3.13 note8p/calculs/ircsg4_openfisca.py   ->  note8p/sorties/ircsg4_of_cas.csv

Pour chaque cas : charge d'aujourd'hui avec niches (IR après réductions et crédits, crédits restitués compris, CEHR,
CSG, CRDS), la même sans niche, et le revenu après cotisations de chaque adulte (assiette du nouvel impôt).
- IR : iai (impôt après décote et réductions, avant seuils de recouvrement) − crédits d'impôt (credits_impot) : un crédit
  supérieur à l'impôt est restitué (montant négatif).
- Heures supplémentaires : OpenFisca 176.1 ne modélise plus leur exonération (variable hsup close en 2013). On simule
  donc l'IR sur le salaire sans les heures supplémentaires et la CSG-CRDS sur le salaire avec (les heures supplémentaires
  restent soumises à la CSG et à la CRDS) ; la réduction de cotisations salariales sur les heures supplémentaires, hors
  périmètre, n'est pas simulée [H].
- Investissement locatif (Pinel) : réduction annuelle de 2 % d'un investissement de 200 000 € (4 000 €), imputée dans
  la limite de l'impôt, hors OpenFisca [H] ; gardée dans la réforme (engagement en cours), sans effet sur le gain net.
- Retraités : taux de CSG de régime stable (méthode de ircsg_openfisca.calcule).
"""
import csv
import sys
from pathlib import Path

import numpy as np
from openfisca_core.simulation_builder import SimulationBuilder

RACINE = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RACINE / "synthese"))
import openfisca_cas_ircsg as OC  # noqa: E402

TBS, P, N2, SMIC = OC.TBS, OC.P, OC.N2, OC.SMIC
OUT = RACINE / "note8p/sorties"


def simule(adultes, enfants=(), foyer=None, isole=False, rfr_n2=None, nbptr_n2=None):
    """adultes : [(nature 'sal'/'ret', brut annuel, année de naissance)] ; enfants : dates de naissance ;
    foyer : variables de déclaration (cases 7xx)."""
    ind = {}
    noms = []
    for j, (nat, mt, an) in enumerate(adultes):
        nom = f"a{j}"
        v = {"date_naissance": {"ETERNITY": f"{an}-01-01"}}
        v["salaire_de_base" if nat == "sal" else "retraite_brute"] = {P: float(mt)}
        ind[nom] = v
        noms.append(nom)
    enf = []
    for j, d in enumerate(enfants):
        e = f"e{j}"
        ind[e] = {"date_naissance": {"ETERNITY": d}}
        enf.append(e)
    foy = {"declarants": noms, "personnes_a_charge": enf, **{k: {P: v} for k, v in (foyer or {}).items()}}
    if isole:
        foy["caseT"] = {P: True}
    if rfr_n2 is not None:
        foy["rfr"] = {N2: float(rfr_n2)}
        foy["nbptr"] = {N2: float(nbptr_n2)}
    men = {"personne_de_reference": [noms[0]], "enfants": enf, **({"conjoint": [noms[1]]} if len(noms) > 1 else {})}
    s = SimulationBuilder().build_from_entities(TBS, {"individus": ind, "foyers_fiscaux": {"f": foy}, "menages": {"m": men},
                                                      "familles": {"fa": {"parents": noms, "enfants": enf}}})
    g = lambda v: float(s.calculate(v, P)[0])  # noqa: E731
    csg = -sum(float(s.calculate_add(v, P)[:len(noms)].sum()) for v in
               ("csg_deductible_salaire", "csg_imposable_salaire", "csg_deductible_retraite", "csg_imposable_retraite"))
    crds = -sum(float(s.calculate_add(v, P)[:len(noms)].sum()) for v in ("crds_salaire", "crds_retraite"))
    base = (s.calculate_add("salaire_de_base", P) + s.calculate_add("cotisations_salariales", P)
            + s.calculate_add("retraite_brute", P))[:len(noms)]
    return dict(iai=max(g("iai"), 0.0), credits=g("credits_impot"), reductions=g("reductions"),
                cehr=g("contribution_exceptionnelle_hauts_revenus_sans_lissage"), csg=csg, crds=crds, rfr=g("rfr"),
                bases=[float(b) for b in base])


def calcule(adultes, enfants=(), foyer=None, isole=False):
    if all(a[0] == "sal" for a in adultes):
        return simule(adultes, enfants, foyer, isole)
    nb = float(len(adultes)) + 0.5 * len(enfants)
    b = OC.seuils_csg(nb)
    forcer = [0.0, (b[1] + b[2]) / 2, (b[2] + b[3]) / 2, 10 * b[3] + 1e6]
    reg = [simule(adultes, enfants, foyer, isole, r, nb) for r in forcer]
    k = 3 if reg[3]["rfr"] > b[3] else 2 if reg[2]["rfr"] > b[2] else 1 if reg[1]["rfr"] > b[1] else 0
    return reg[k]


def charge(o, ir_override=None, pinel=0.0):
    ir = (o["iai"] if ir_override is None else ir_override)
    red_pinel = min(pinel, ir)
    ir_net = ir - red_pinel - o["credits"]
    return dict(ir_net=ir_net, csg_crds=o["csg"] + o["crds"], cehr=o["cehr"], total=ir_net + o["csg"] + o["crds"] + o["cehr"],
                pinel=red_pinel)


HS = 0.10 * SMIC          # 10 % d'heures supplémentaires au Smic (≈ 2 160 € brut par an)
CAS = [
    # clé, libellé, adultes, enfants, niches (cases), parent isolé, Pinel (€/an), heures sup (brut, adulte 0)
    ("smic_hs", "Salarié au Smic, 10 % d'heures supplémentaires exonérées", [("sal", SMIC + HS, 1995)], (), {}, False, 0.0, HS),
    ("smic", "Salarié au Smic, sans heure supplémentaire", [("sal", SMIC, 1995)], (), {}, False, 0.0, 0.0),
    ("milieu", "Salarié de classe moyenne, 40 000 € brut, sans niche", [("sal", 40000.0, 1980)], (), {}, False, 0.0, 0.0),
    ("julie", "Julie, 2 000 € net par mois", [("sal", 30318.48, 1990)], (), {}, False, 0.0, 0.0),
    ("julie_200", "Julie après +200 € net par mois", [("sal", None, 1990)], (), {}, False, 0.0, 0.0),
    ("garde", "Couple biactif 36 + 24 k€, deux enfants de 1 et 3 ans gardés par une assistante maternelle",
     [("sal", 36000.0, 1990), ("sal", 24000.0, 1990)], ("2024-03-01", "2022-03-01"), {"f7ga": 3500, "f7gb": 3500}, False, 0.0, 0.0),
    ("garde_dom", "Le même, avec en plus 3 000 € d'emploi à domicile (ménage)",
     [("sal", 36000.0, 1990), ("sal", 24000.0, 1990)], ("2024-03-01", "2022-03-01"),
     {"f7ga": 3500, "f7gb": 3500, "f7db": 3000}, False, 0.0, 0.0),
    ("garde_sans", "Le même couple, sans niche", [("sal", 36000.0, 1990), ("sal", 24000.0, 1990)],
     ("2024-03-01", "2022-03-01"), {}, False, 0.0, 0.0),
    ("pi_garde", "Parent isolé au Smic, un enfant de 2 ans gardé (2 500 €)", [("sal", SMIC, 1995)], ("2023-03-01",),
     {"f7ga": 2500}, True, 0.0, 0.0),
    ("nombreuse", "Famille nombreuse biactive 40 + 25 k€, trois enfants (collégien, lycéen, 7 ans)",
     [("sal", 40000.0, 1982), ("sal", 25000.0, 1982)], ("2009-03-01", "2012-03-01", "2018-03-01"),
     {"f7ea": 1, "f7ec": 1}, False, 0.0, 0.0),
    ("mono", "Couple mono-actif, 45 000 € brut, deux enfants de 8 et 11 ans", [("sal", 45000.0, 1985), ("sal", 0.0, 1985)],
     ("2017-03-01", "2014-03-01"), {}, False, 0.0, 0.0),
    ("mono_mi", "Le même, le conjoint reprend un mi-temps au Smic", [("sal", 45000.0, 1985), ("sal", SMIC / 2, 1985)],
     ("2017-03-01", "2014-03-01"), {}, False, 0.0, 0.0),
    ("ret_modeste", "Retraité seul, pension de 14 000 €", [("ret", 14000.0, 1950)], (), {}, False, 0.0, 0.0),
    ("ret_dom", "Retraitée seule, pension de 30 000 €, aide à domicile 4 000 €", [("ret", 30000.0, 1948)], (),
     {"f7db": 4000}, False, 0.0, 0.0),
    ("ret_dom_sans", "La même, sans niche", [("ret", 30000.0, 1948)], (), {}, False, 0.0, 0.0),
    ("cadres", "Couple de cadres 90 + 60 k€, deux enfants ; dons 2 000 €, emploi à domicile 6 000 €, Pinel 4 000 €/an",
     [("sal", 90000.0, 1978), ("sal", 60000.0, 1978)], ("2012-03-01", "2015-03-01"), {"f7uf": 2000, "f7db": 6000, "f7ea": 1},
     False, 4000.0, 0.0),
]


def main():
    rows = []
    b2000 = 30318.48
    for cle, lib, ad, enf, niches, iso, pinel, hs in CAS:
        if cle == "julie_200":
            # salaire brut qui donne 200 € de plus par mois de salaire net (après cotisations, CSG et CRDS)
            o0 = simule([("sal", b2000, 1990)])
            net0 = o0["bases"][0] - o0["csg"] - o0["crds"]
            lo, hi = b2000, b2000 + 6000
            for _ in range(40):
                m = (lo + hi) / 2
                o = simule([("sal", m, 1990)])
                lo, hi = (m, hi) if o["bases"][0] - o["csg"] - o["crds"] - net0 < 2400 else (lo, m)
            ad = [("sal", (lo + hi) / 2, 1990)]
        avec = calcule(ad, enf, niches, iso)
        sans = calcule(ad, enf, {}, iso)
        ir_hs = None
        if hs:
            ir_hs = calcule([(ad[0][0], ad[0][1] - hs, ad[0][2])] + ad[1:], enf, niches, iso)["iai"]
        ca = charge(avec, ir_hs, pinel)
        cs = charge(sans)                 # sans niche : HS imposées, pas de Pinel, pas de crédit
        r = dict(cle=cle, libelle=lib, enfants=len(enf), isole=int(iso), bruts=";".join(f"{a[1]:.2f}" for a in ad),
                 bases=";".join(f"{b:.2f}" for b in avec["bases"]), charge_avec=round(ca["total"], 2),
                 charge_sans=round(cs["total"], 2), ir_avec=round(ca["ir_net"], 2), ir_sans=round(cs["ir_net"], 2),
                 credits=round(avec["credits"], 2), reductions=round(avec["reductions"], 2), pinel_garde=round(ca["pinel"], 2),
                 csg_crds=round(ca["csg_crds"], 2), cehr=round(ca["cehr"], 2), naissances=";".join(enf))
        rows.append(r)
        print(cle, r["charge_avec"], r["charge_sans"], r["bases"], flush=True)
    with open(OUT / "ircsg4_of_cas.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=rows[0].keys())
        w.writeheader()
        w.writerows(rows)


if __name__ == "__main__":
    main()
