"""Bloc IR-CSG-CRDS (note8p) : prélèvements d'aujourd'hui calculés avec OpenFisca-France 176.1 (droit des revenus 2025).

Lancer depuis fiscalite/ :  python3.13 note8p/calculs/ircsg_openfisca.py
Sorties (note8p/sorties/) :
- ircsg_of_marges.csv : salarié seul et retraité seul (65 ans et plus), revenu après cotisations de 1 000 à 700 000 €
  (salarié) ou 150 000 € (retraité), pas de 100 € ; pour chaque point, IR (avant crédits, CEHR non comprise), CEHR,
  CDHR, CSG, CRDS au revenu b et au revenu b + 100 € de revenu après cotisations. Le taux marginal se lit
  (charge(b + 100) − charge(b)) / 100 : aucune interpolation de l'impôt, aucun lissage.
  Pour éviter les arrondis à l'euro de l'IR (artefacts de ±1 point par 100 €), l'IR est pris avant arrondi et avant
  seuils de recouvrement : iai (impôt après décote et réductions ; aucun crédit ni réduction dans ces cas-types).
- ircsg_of_cas.csv : cas-types de la note (revenus, charge d'aujourd'hui, revenu après cotisations de chaque adulte).

Conventions (reprises de synthese/openfisca_cas_ircsg.py, qu'on importe sans le modifier) :
- salariés du privé non cadres nés en 1980 ; enfants nés en 2015 ; couples mariés ou pacsés ; parent isolé : case T ;
- retraités nés en 1950 (abattement des plus de 65 ans) ou en 1962 (pour la prolongation d'activité à 63 ans) ;
- taux de CSG des pensions en régime stable (RFR de l'avant-dernière année égal à celui de l'année ; seuils
  revalorisés ; synthese/openfisca_cas_ircsg.py) : pas d'alternance artificielle entre deux taux (« yoyo »).
"""
import csv
import sys
from pathlib import Path

import numpy as np
from openfisca_core.simulation_builder import SimulationBuilder

RACINE = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RACINE / "synthese"))
import openfisca_cas_ircsg as OC  # noqa: E402  (TBS, seuils_csg, SMIC)

TBS, P, N2 = OC.TBS, OC.P, OC.N2
SMIC = OC.SMIC
OUT = RACINE / "note8p/sorties"
D = 100.0


def simule(adultes, enfants=0, isole=False, rfr_n2=None, nbptr_n2=None):
    """adultes : liste de (nature 'sal' ou 'ret', tableau des montants bruts, année de naissance).
    Renvoie IR (iai, non arrondi), CEHR, CDHR, CSG, CRDS, CASA par foyer, revenu après cotisations de chaque adulte."""
    n = len(adultes[0][1])
    ind, foy, men, fam = {}, {}, {}, {}
    for k in range(n):
        noms = [f"a{k}_{j}" for j in range(len(adultes))]
        for nom, (nat, mt, an) in zip(noms, adultes):
            v = {"date_naissance": {"ETERNITY": f"{an}-01-01"}}
            v["salaire_de_base" if nat == "sal" else "retraite_brute"] = {P: float(mt[k])}
            ind[nom] = v
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
        men[f"m{k}"] = {"personne_de_reference": [noms[0]], "enfants": enf,
                        **({"conjoint": [noms[1]]} if len(noms) > 1 else {})}
        fam[f"fa{k}"] = {"parents": noms, "enfants": enf}
    s = SimulationBuilder().build_from_entities(TBS, {"individus": ind, "foyers_fiscaux": foy, "menages": men,
                                                      "familles": fam})
    iai = s.calculate("iai", P)
    cehr = s.calculate("contribution_exceptionnelle_hauts_revenus_sans_lissage", P)
    cdhr = s.calculate("contribution_differentielle_hauts_revenus", P)
    csg_i = -(s.calculate_add("csg_deductible_salaire", P) + s.calculate_add("csg_imposable_salaire", P)
              + s.calculate_add("csg_deductible_retraite", P) + s.calculate_add("csg_imposable_retraite", P))
    crds_i = -(s.calculate_add("crds_salaire", P) + s.calculate_add("crds_retraite", P))
    casa_i = -s.calculate_add("casa", P)
    net_i = (s.calculate_add("salaire_de_base", P) + s.calculate_add("cotisations_salariales", P)
             + s.calculate_add("retraite_brute", P))
    pos = {i: k for k, i in enumerate(ind)}
    bases = [np.array([net_i[pos[f"a{k}_{j}"]] for k in range(n)]) for j in range(len(adultes))]
    return dict(ir=np.maximum(iai, 0.0), cehr=cehr, cdhr=cdhr, csg=s.foyer_fiscal.sum(csg_i),
                crds=s.foyer_fiscal.sum(crds_i), casa=s.foyer_fiscal.sum(casa_i), rfr=s.calculate("rfr", P),
                bases=bases)


def calcule(adultes, enfants=0, isole=False):
    """Retraités : taux de CSG de régime stable (méthode de synthese/openfisca_cas_ircsg.calcule)."""
    if all(a[0] == "sal" for a in adultes):
        return simule(adultes, enfants, isole)
    nb = float(len(adultes)) + (0.5 * enfants if enfants else 0.0)
    bornes = OC.seuils_csg(nb)
    forcer = [0.0, (bornes[1] + bornes[2]) / 2, (bornes[2] + bornes[3]) / 2, 10 * bornes[3] + 1e6]
    reg = [simule(adultes, enfants, isole, rfr_n2=r, nbptr_n2=nb) for r in forcer]
    ok = np.vstack([o["rfr"] > b for o, b in zip(reg, bornes)])
    k = np.where(ok[3], 3, np.where(ok[2], 2, np.where(ok[1], 1, 0)))
    out = {c: np.choose(k, [o[c] for o in reg]) for c in reg[0] if c != "bases"}
    out["bases"] = [np.choose(k, [o["bases"][j] for o in reg]) for j in range(len(adultes))]
    out["taux_csg"] = k
    return out


def brut_pour_base(cibles, b_max=820000.0):
    """Salaire brut qui donne chaque revenu après cotisations visé (salarié seul), lu sur une grille de 50 € (le taux marginal est calculé sur les revenus effectivement obtenus)."""
    b = np.arange(0.0, b_max, 50.0)
    base = simule([("sal", b, 1980)])["bases"][0]
    mono = np.maximum.accumulate(base)     # le revenu après cotisations baisse un peu au passage du plafond
    return np.interp(cibles, mono, b)


def marges():
    rows = []
    cs = np.arange(1000.0, 700001.0, 100.0)
    br, brp = brut_pour_base(cs), brut_pour_base(cs + D)
    for prof, adultes, adultes_p, cib in (
            ("seul", [("sal", br, 1980)], [("sal", brp, 1980)], cs),
            ("retraite_seul", [("ret", cs[cs <= 150000], 1950)], [("ret", cs[cs <= 150000] + D, 1950)],
             cs[cs <= 150000])):
        o, op = calcule(adultes), calcule(adultes_p)
        for k, c in enumerate(cib):
            r = dict(profil=prof, base=c, brut=round(float(adultes[0][1][k]), 2))
            for suf, q in (("", o), ("_plus", op)):
                r["base_eff" + suf] = round(float(q["bases"][0][k]), 4)
                for col in ("ir", "cehr", "cdhr", "csg", "crds", "casa", "rfr"):
                    r[col + suf] = round(float(q[col][k]), 4)
            rows.append(r)
        print(prof, "marges ok", flush=True)
    with open(OUT / "ircsg_of_marges.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=rows[0].keys())
        w.writeheader()
        w.writerows(rows)


def brut_net(net_mensuel):
    """Salaire brut annuel d'un salarié seul dont le salaire net (après cotisations, CSG et CRDS, avant impôt sur le
    revenu) vaut net_mensuel par mois."""
    b = np.arange(15000.0, 80000.0, 5.0)
    o = simule([("sal", b, 1980)])
    net = o["bases"][0] - o["csg"] - o["crds"]
    return float(np.interp(12 * net_mensuel, net, b))


# Cas-types : (clé, libellé, adultes [(nature, brut, naissance)], enfants, parent isolé)
B2000 = None


def cas():
    global B2000
    B2000 = brut_net(2000.0)
    b2200 = brut_net(2200.0)
    C = [
        ("jeune_smic", "Jeune salarié au Smic", [("sal", SMIC, 1998)], 0, False),
        ("sal_2000", "Salarié, 2 000 € net par mois", [("sal", B2000, 1985)], 0, False),
        ("sal_2200", "Salarié, 2 200 € net par mois", [("sal", b2200, 1985)], 0, False),
        ("couple2_60", "Couple biactif, deux enfants, 60 000 € brut (36 000 + 24 000)",
         [("sal", 36000.0, 1985), ("sal", 24000.0, 1985)], 2, False),
        ("mono2_40", "Famille mono-active, deux enfants, 40 000 € brut", [("sal", 40000.0, 1985), ("sal", 0.0, 1985)], 2, False),
        ("mono2_60", "Famille mono-active, deux enfants, 60 000 € brut", [("sal", 60000.0, 1985), ("sal", 0.0, 1985)], 2, False),
        ("nomb3_60", "Famille nombreuse biactive, trois enfants, 60 000 € brut (36 000 + 24 000)",
         [("sal", 36000.0, 1985), ("sal", 24000.0, 1985)], 3, False),
        ("nomb4m_45", "Famille nombreuse mono-active, quatre enfants, 45 000 € brut",
         [("sal", 45000.0, 1985), ("sal", 0.0, 1985)], 4, False),
        ("nomb3m_35", "Famille nombreuse mono-active, trois enfants, 35 000 € brut",
         [("sal", 35000.0, 1985), ("sal", 0.0, 1985)], 3, False),
        ("pi2_smic", "Parent isolé, deux enfants, au Smic", [("sal", SMIC, 1985)], 2, True),
        ("pi2_35", "Parent isolé, deux enfants, 35 000 € brut", [("sal", 35000.0, 1985)], 2, True),
        ("cadre120", "Cadre supérieur seul, 120 000 € brut", [("sal", 120000.0, 1975)], 0, False),
        ("cadre250", "Dirigeant salarié seul, 250 000 € brut", [("sal", 250000.0, 1970)], 0, False),
        ("couple0m_80", "Couple sans enfant à un seul revenu, 80 000 € brut", [("sal", 80000.0, 1975), ("sal", 0.0, 1975)], 0, False),
        ("couple0_50", "Couple sans enfant, 50 000 € brut (30 000 + 20 000)", [("sal", 30000.0, 1985), ("sal", 20000.0, 1985)], 0, False),
        ("ret_12", "Retraité seul, pension de 12 000 €", [("ret", 12000.0, 1950)], 0, False),
        ("ret_16", "Retraité seul, pension de 16 000 €", [("ret", 16000.0, 1950)], 0, False),
        ("ret_20", "Retraité seul, pension de 20 000 €", [("ret", 20000.0, 1950)], 0, False),
        ("ret_30", "Retraité seul, pension de 30 000 €", [("ret", 30000.0, 1950)], 0, False),
        ("retc_30", "Couple de retraités, 30 000 € de pensions (18 000 + 12 000)", [("ret", 18000.0, 1950), ("ret", 12000.0, 1950)], 0, False),
        ("retc_60", "Couple de retraités aisé, 60 000 € de pensions (36 000 + 24 000)", [("ret", 36000.0, 1950), ("ret", 24000.0, 1950)], 0, False),
        # second conjoint : premier salaire de 35 000 € brut, le second reprend un mi-temps au Smic (ou rien)
        ("conj_0", "Couple, un seul salaire de 35 000 € brut", [("sal", 35000.0, 1985), ("sal", 0.0, 1985)], 0, False),
        ("conj_mi", "Couple, 35 000 € brut + mi-temps au Smic", [("sal", 35000.0, 1985), ("sal", SMIC / 2, 1985)], 0, False),
        ("conj2_0", "Couple, deux enfants, un seul salaire de 35 000 € brut", [("sal", 35000.0, 1985), ("sal", 0.0, 1985)], 2, False),
        ("conj2_mi", "Couple, deux enfants, 35 000 € brut + mi-temps au Smic", [("sal", 35000.0, 1985), ("sal", SMIC / 2, 1985)], 2, False),
        ("seul_mi", "Personne seule, mi-temps au Smic", [("sal", SMIC / 2, 1985)], 0, False),
        # prolongation d'activité à 63 ans (né en 1962) : salaire de 35 000 € brut, ou pension de 20 000 € brut
        ("sen_sal", "Salarié de 63 ans, 35 000 € brut", [("sal", 35000.0, 1962)], 0, False),
        ("sen_ret", "Retraité de 63 ans, pension de 20 000 €", [("ret", 20000.0, 1962)], 0, False),
        ("sen_sal2", "Salarié de 63 ans, 50 000 € brut", [("sal", 50000.0, 1962)], 0, False),
        ("sen_ret2", "Retraité de 63 ans, pension de 28 000 €", [("ret", 28000.0, 1962)], 0, False),
    ]
    rows = []
    for cle, lib, ad, enf, iso in C:
        o = calcule([(n, np.array([m]), a) for n, m, a in ad], enf, iso)
        r = dict(cle=cle, libelle=lib, enfants=enf, isole=int(iso), nature=ad[0][0],
                 bruts=";".join(f"{m:.2f}" for _, m, _ in ad),
                 bases=";".join(f"{float(b[0]):.2f}" for b in o["bases"]))
        for c in ("ir", "cehr", "cdhr", "csg", "crds", "casa", "rfr"):
            r[c] = round(float(o[c][0]), 2)
        r["charge"] = round(r["ir"] + r["cehr"] + r["cdhr"] + r["csg"] + r["crds"], 2)
        rows.append(r)
        print(cle, r["charge"], flush=True)
    with open(OUT / "ircsg_of_cas.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=rows[0].keys())
        w.writeheader()
        w.writerows(rows)


if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    if "--marges" not in sys.argv:
        cas()
    marges()
