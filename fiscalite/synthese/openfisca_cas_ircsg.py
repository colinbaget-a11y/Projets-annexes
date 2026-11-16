"""Cas-types OpenFisca (législation des revenus 2024) pour la partie IR-CSG : IR, CSG, CRDS et CASA d'aujourd'hui.

Pourquoi : la partie IR-CSG compare l'impôt d'aujourd'hui et celui de la réforme pour des ménages auxquels un lecteur
peut s'identifier (retraité modeste, couple de retraités, couple avec trois enfants, couple à un seul revenu, parent
isolé, jeune salarié au Smic, cadre, conjoint qui reprend un emploi). ir_csg/sorties/courbes_openfisca.csv ne couvre
que cinq profils ; ce programme les recalcule tous avec la même méthode, sur une même grille.

Conventions (comme ir_csg/openfisca_courbes.py et synthese/openfisca_couple_retraites.py) :
- salariés du secteur privé nés en 1980, sans autre revenu ni niche ; enfants nés en 2015 ; retraités nés en 1950
  (abattement des plus de 65 ans), pensions de droit direct seulement ;
- couples mariés ou pacsés (imposition commune), revenus partagés 60/40 ou un seul revenu (« mono ») ;
- parents isolés : case T cochée ;
- « conjoint » : le premier conjoint gagne un salaire fixe de 30 000 € brut, le second un salaire g qui varie :
  sert au taux de prélèvement sur le salaire du conjoint qui reprend un emploi ;
- taux de CSG des pensions : il dépend du revenu fiscal de référence de l'avant-dernière année ; on suppose un
  régime stable (RFR N-2 = RFR de l'année). Aux seuils, le taux alterne d'un passage à l'autre : on garde la
  moyenne des deux derniers passages (comme openfisca_couple_retraites.py) ;
- Smic 2024 : 21 270 € brut par an (11,65 € de janvier à octobre, 11,88 € en novembre et décembre, 151,67 heures).
  Chiffre de sources secondaires, non relu au Journal officiel (revue/hypotheses_ircsg.md, section 4).

Colonnes : profil, brut (revenu brut du ménage, ou du second conjoint pour « conjoint »), ir, csg, crds, casa
(€ par an, positifs), base_a et base_b (revenu après cotisations de chaque adulte, assiette de l'impôt fusionné),
rfr ; les mêmes avec le suffixe _plus pour brut + 1 000 €.

Lancer avec un Python où openfisca-france est installé, depuis fiscalite/ :
    python3.13 synthese/openfisca_cas_ircsg.py  ->  synthese/sorties/cas_types_openfisca.csv
"""
import csv
from pathlib import Path

import numpy as np
from openfisca_core.simulation_builder import SimulationBuilder
from openfisca_france import FranceTaxBenefitSystem

TBS = FranceTaxBenefitSystem()
P = "2024"
DELTA = 1000.0
SMIC = 21270.0
FIXE = 30000.0            # salaire du premier conjoint dans les profils « conjoint »
OUT = Path(__file__).resolve().parent / "sorties/cas_types_openfisca.csv"

# profil : (nature des adultes, part du revenu de chaque adulte, enfants, parent isolé)
PROFILS = {
    "seul": ("sal", [1.0], 0, False),
    "couple_0enf": ("sal", [0.6, 0.4], 0, False),
    "couple_0enf_mono": ("sal", [1.0, 0.0], 0, False),
    "couple_2enf": ("sal", [0.6, 0.4], 2, False),
    "couple_2enf_mono": ("sal", [1.0, 0.0], 2, False),
    "couple_3enf": ("sal", [0.6, 0.4], 3, False),
    "couple_3enf_mono": ("sal", [1.0, 0.0], 3, False),
    "parent_isole_1enf": ("sal", [1.0], 1, True),
    "parent_isole_2enf": ("sal", [1.0], 2, True),
    "retraite_seul": ("ret", [1.0], 0, False),
    "retraite_couple": ("ret", [0.6, 0.4], 0, False),
    "conjoint": ("conj", [None, 1.0], 0, False),
    "conjoint_2enf": ("conj", [None, 1.0], 2, False),
}


def simule(revenus, nature, parts, enfants, isole, rfr_n2=None):
    ind, foy, men, fam = {}, {}, {}, {}
    for k, g in enumerate(revenus):
        noms = [f"a{k}", f"b{k}"][:len(parts)]
        for j, (nom, sh) in enumerate(zip(noms, parts)):
            if nature == "ret":
                ind[nom] = {"date_naissance": {"ETERNITY": "1950-01-01"}, "retraite_brute": {P: sh * g}}
            else:
                sal = (FIXE if j == 0 else g) if nature == "conj" else sh * g
                ind[nom] = {"date_naissance": {"ETERNITY": "1980-01-01"}, "salaire_de_base": {P: sal}}
        enf = []
        for j in range(enfants):
            e = f"e{k}_{j}"
            ind[e] = {"date_naissance": {"ETERNITY": "2015-01-01"}}
            enf.append(e)
        foy[f"f{k}"] = {"declarants": noms, "personnes_a_charge": enf}
        if isole:
            foy[f"f{k}"]["caseT"] = {P: True}
        if rfr_n2 is not None:
            foy[f"f{k}"]["rfr"] = {"2022": float(rfr_n2[k])}
            foy[f"f{k}"]["nbptr"] = {"2022": float(len(noms))}
        men[f"m{k}"] = {"personne_de_reference": [noms[0]], "enfants": enf, **({"conjoint": [noms[1]]} if len(noms) > 1 else {})}
        fam[f"fa{k}"] = {"parents": noms, "enfants": enf}
    s = SimulationBuilder().build_from_entities(TBS, {"individus": ind, "foyers_fiscaux": foy, "menages": men,
                                                      "familles": fam})
    ir = -s.calculate("impot_revenu_restant_a_payer", P)
    csg_i = -(s.calculate_add("csg_deductible_salaire", P) + s.calculate_add("csg_imposable_salaire", P)
              + s.calculate_add("csg_deductible_retraite", P) + s.calculate_add("csg_imposable_retraite", P))
    crds_i = -(s.calculate_add("crds_salaire", P) + s.calculate_add("crds_retraite", P))
    casa_i = -s.calculate_add("casa", P)
    net_i = (s.calculate_add("salaire_de_base", P) + s.calculate_add("cotisations_salariales", P)
             + s.calculate_add("retraite_brute", P))
    pos = {i: k for k, i in enumerate(ind)}
    base_a = np.array([net_i[pos[f"a{k}"]] for k in range(len(revenus))])
    base_b = np.array([net_i[pos[f"b{k}"]] if f"b{k}" in pos else 0.0 for k in range(len(revenus))])
    return dict(ir=ir, csg=s.foyer_fiscal.sum(csg_i), crds=s.foyer_fiscal.sum(crds_i), casa=s.foyer_fiscal.sum(casa_i),
                rfr=s.calculate("rfr", P), base_a=base_a, base_b=base_b)


def calcule(revenus, profil):
    nature, parts, enfants, isole = PROFILS[profil]
    o = simule(revenus, nature, parts, enfants, isole)
    if nature != "ret":
        return o
    passes = []
    for _ in range(4):
        o = simule(revenus, nature, parts, enfants, isole, rfr_n2=o["rfr"])
        passes.append(o)
    return {k: 0.5 * (passes[-1][k] + passes[-2][k]) for k in o}


def main():
    grille = np.concatenate([np.arange(0, 200001, 500.0), np.arange(202000, 400001, 2000.0),
                             np.array([500e3, 1e6]), SMIC * np.array([0.25, 0.5, 0.75, 1.0, 1.25, 1.5, 2.0])])
    grille = np.unique(grille)
    rows = []
    for profil in PROFILS:
        x = np.concatenate([grille, grille + DELTA])
        o = calcule(x, profil)
        n = len(grille)
        for k, g in enumerate(grille):
            r = dict(profil=profil, brut=g)
            for suf, j in (("", k), ("_plus", n + k)):
                for c in ("ir", "csg", "crds", "casa", "base_a", "base_b", "rfr"):
                    r[c + suf] = round(float(o[c][j]), 2)
            rows.append(r)
        print(profil, "ok", flush=True)
    with open(OUT, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=rows[0].keys())
        w.writeheader()
        w.writerows(rows)
    print(f"{len(rows)} lignes -> {OUT}")


if __name__ == "__main__":
    main()
