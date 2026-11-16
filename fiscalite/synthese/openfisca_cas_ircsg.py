"""Cas-types OpenFisca (législation des revenus 2025) pour la partie IR-CSG : IR, CSG, CRDS et CASA d'aujourd'hui.

Pourquoi : la partie IR-CSG compare l'impôt d'aujourd'hui et celui de la réforme pour des ménages auxquels un lecteur
peut s'identifier (retraité modeste, couple de retraités, couple avec trois enfants, couple à un seul revenu, parent
isolé, jeune salarié au Smic, cadre, conjoint qui reprend un emploi), et trace les taux marginaux d'aujourd'hui.

Base 2025 (décision 5 du 17/11/2026) : législation des revenus 2025 d'OpenFisca-France 176.1 (barème de l'IR revalorisé
de 0,9 % : 11 600 / 29 579 / 84 577 / 181 917 € ; décote 897 / 1 483 € ; plafond du quotient familial 1 807 € par
demi-part ; seuils de CSG des pensions de 2025 : 12 817 / 16 755 / 26 004 € de revenu fiscal pour une part, demi-part
+3 422 €, valeurs d'OpenFisca non relues sur une source officielle) ; Smic 2025 de 11,88 € de l'heure toute l'année,
soit 21 621,6 € brut par an (151,67 heures).

Conventions :
- salariés du secteur privé nés en 1980, sans autre revenu ni niche ; enfants nés en 2015 ; retraités nés en 1950
  (abattement des plus de 65 ans), pensions de droit direct seulement ;
- couples mariés ou pacsés (imposition commune), revenus partagés 60/40 ou un seul revenu (« mono ») ;
- parents isolés : case T cochée ;
- « conjoint » : le premier conjoint gagne un salaire fixe de 30 000 € brut, le second un salaire g qui varie ;
- taux de CSG des pensions (correction du 17/11/2026, décision 6) : il dépend du revenu fiscal de référence (RFR) de
  l'avant-dernière année, lui-même diminué de la CSG déductible, qui dépend du taux. En régime stable (même pension
  chaque année, seuils revalorisés), on calcule l'année avec chacun des quatre taux (exonération, 3,8, 6,6, 8,3 %) et
  l'on retient le taux le plus élevé dont le seuil est dépassé par le RFR calculé à ce taux. C'est le seul point fixe
  quand il existe ; dans la bande étroite (quelques centaines d'euros de pension) où aucun taux n'est cohérent avec
  son propre RFR, on garde le taux inférieur, comme le fait la règle des deux années consécutives pour le passage aux
  taux médian et plein. L'ancienne méthode (moyenne de deux passages) créait des demi-marches artificielles.
- taux marginaux (fichier courbes_marginales_openfisca.csv) : prélèvement supplémentaire pour 1 000 € de revenu après
  cotisations en plus (salaire net de cotisations, ou pension brute), sur une grille de 100 €, chaque point calculé
  directement (aucune interpolation de l'impôt). Le revenu après cotisations est l'assiette de l'impôt fusionné : le
  mesurer ainsi écarte des courbes les effets propres aux cotisations (par exemple la contribution d'équilibre
  technique, due sur tout le salaire dès qu'il dépasse le plafond de la Sécurité sociale).

Colonnes de cas_types_openfisca.csv : profil, brut (revenu brut du ménage, ou du second conjoint pour « conjoint »),
ir, csg, crds, casa (€ par an, positifs), base_a et base_b (revenu après cotisations de chaque adulte, assiette de
l'impôt fusionné), rfr, taux_csg (retraités : 0 à 3) ; les mêmes avec le suffixe _plus pour brut + 1 000 €.

Lancer avec un Python où openfisca-france est installé, depuis fiscalite/ :
    python3.13 synthese/openfisca_cas_ircsg.py
    ->  synthese/sorties/cas_types_openfisca.csv et synthese/sorties/courbes_marginales_openfisca.csv
"""
import csv
from pathlib import Path

import numpy as np
from openfisca_core.simulation_builder import SimulationBuilder
from openfisca_france import FranceTaxBenefitSystem

TBS = FranceTaxBenefitSystem()
P = "2025"
N2 = "2023"                # avant-dernière année : son RFR fixe le taux de CSG des pensions de 2025
DELTA = 1000.0
SMIC = 11.88 * 151.67 * 12  # 21 621,6 € brut par an
FIXE = 30000.0            # salaire du premier conjoint dans les profils « conjoint »
HERE = Path(__file__).resolve().parent
OUT = HERE / "sorties/cas_types_openfisca.csv"
OUT_MG = HERE / "sorties/courbes_marginales_openfisca.csv"

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


def seuils_csg(nbptr):
    """Bornes inférieures des quatre taux de CSG des pensions (RFR de l'avant-dernière année), droit de 2025."""
    s = TBS.parameters(f"{P}-01-01").prelevements_sociaux.contributions_sociales.csg.remplacement.seuils
    s1 = s.seuil_rfr1.seuil_rfr1 + (nbptr - 1) * 2 * s.seuil_rfr1.demi_part_suppl_rfr1
    s2 = s.seuil_rfr2.seuil_rfr2 + (nbptr - 1) * 2 * s.seuil_rfr2.demi_part_suppl_rfr2
    s3 = s.seuil_rfr3.seuil_rfr3 + (nbptr - 1) * 2 * s.seuil_rfr3.demi_part_suppl_rfr3
    return np.array([-np.inf, s1, s2, s3])


def simule(revenus, nature, parts, enfants, isole, rfr_n2=None, nbptr_n2=None):
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
            foy[f"f{k}"]["rfr"] = {N2: float(rfr_n2)}
            foy[f"f{k}"]["nbptr"] = {N2: float(nbptr_n2)}
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
    """Résultats de l'année 2025 ; pour les retraités, taux de CSG de régime stable (voir l'en-tête)."""
    nature, parts, enfants, isole = PROFILS[profil]
    if nature != "ret":
        o = simule(revenus, nature, parts, enfants, isole)
        o["taux_csg"] = np.full(len(revenus), np.nan)
        return o
    nb = float(len(parts))
    bornes = seuils_csg(nb)
    forcer = [0.0, (bornes[1] + bornes[2]) / 2, (bornes[2] + bornes[3]) / 2, 10 * bornes[3] + 1e6]
    regimes = [simule(revenus, nature, parts, enfants, isole, rfr_n2=r, nbptr_n2=nb) for r in forcer]
    # taux retenu : le plus élevé dont la borne inférieure est dépassée par le RFR calculé à ce taux
    ok = np.vstack([o["rfr"] > b for o, b in zip(regimes, bornes)])
    k = np.where(ok[3], 3, np.where(ok[2], 2, np.where(ok[1], 1, 0)))
    out = {c: np.choose(k, [o[c] for o in regimes]) for c in regimes[0]}
    out["taux_csg"] = k.astype(float)
    return out


def main_cas():
    grille = np.concatenate([np.arange(0, 200001, 500.0), np.arange(202000, 400001, 2000.0),
                             np.array([500e3, 1e6]), SMIC * np.array([0.25, 0.5, 0.75, 1.0, 1.25, 1.5, 2.0])])
    grille = np.unique(np.round(grille, 2))
    rows = []
    for profil in PROFILS:
        x = np.concatenate([grille, grille + DELTA])
        o = calcule(x, profil)
        n = len(grille)
        for k, g in enumerate(grille):
            r = dict(profil=profil, brut=g)
            for suf, j in (("", k), ("_plus", n + k)):
                for c in ("ir", "csg", "crds", "casa", "base_a", "base_b", "rfr", "taux_csg"):
                    r[c + suf] = round(float(o[c][j]), 2)
            rows.append(r)
        print(profil, "ok", flush=True)
    with open(OUT, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=rows[0].keys())
        w.writeheader()
        w.writerows(rows)
    print(f"{len(rows)} lignes -> {OUT}")


def main_courbes():
    """Taux marginaux d'aujourd'hui, par 1 000 € de revenu après cotisations, grille de 100 €."""
    rows = []
    # salarié seul : salaire brut qui donne chaque revenu après cotisations visé (lu sur une grille de 25 €)
    b_fin = np.arange(0, 230001, 25.0)
    base_fin = simule(b_fin, "sal", [1.0], 0, False)["base_a"]
    mono = np.maximum.accumulate(base_fin)          # le revenu après cotisations baisse d'environ 65 € au plafond
    for profil, nature, cibles in (("seul", "sal", np.arange(1000, 150001, 100.0)),
                                   ("retraite_seul", "ret", np.arange(1000, 80001, 100.0))):
        if nature == "sal":
            br = np.interp(cibles, mono, b_fin)
            br_p = np.interp(cibles + DELTA, mono, b_fin)
        else:
            br, br_p = cibles, cibles + DELTA
        o = calcule(np.concatenate([br, br_p]), profil)
        n = len(cibles)
        for k, c in enumerate(cibles):
            r = dict(profil=profil, base=c)
            for suf, j in (("", k), ("_plus", n + k)):
                r["brut" + suf] = round(float(np.concatenate([br, br_p])[j]), 2)
                r["base_eff" + suf] = round(float(o["base_a"][j]), 2)
                for col in ("ir", "csg", "crds", "rfr", "taux_csg"):
                    r[col + suf] = round(float(o[col][j]), 2)
            rows.append(r)
        print(profil, "courbe ok", flush=True)
    with open(OUT_MG, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=rows[0].keys())
        w.writeheader()
        w.writerows(rows)
    print(f"{len(rows)} lignes -> {OUT_MG}")


if __name__ == "__main__":
    main_cas()
    main_courbes()
