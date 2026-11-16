"""Bloc IR-CSG v3 : simulateur simplifié du droit actuel (revenus 2025) et de ses variantes « pas à pas ».

But : décomposer séquentiellement le passage du système actuel (IR + CSG + CRDS) au nouvel impôt (graphique F), sur les
foyers « purs » du modèle (synthese/modele_purs.py) et sur les cas-types. Chaque mesure est un drapeau ; on active les
mesures l'une après l'autre dans l'ordre documenté dans ircsg3_cascade.py.

Paramètres : droit des revenus 2025, lus dans OpenFisca-France 176.1 (python3.13, voir l'en-tête de
ircsg_openfisca.py) : barème 11 600 / 29 579 / 84 577 / 181 917 € (11, 30, 41, 45 %) ; plafond de l'avantage par
demi-part 1 807 €, 4 262 € pour la part du premier enfant d'un parent isolé (case T) ; décote 897 / 1 483 € − 45,25 %
de l'impôt ; déduction de 10 % des salaires (min. 509 €, max. 14 555 € par personne) ; abattement de 10 % des pensions
(min. 454 € par pensionné, max. 4 439 € par foyer) ; abattement de l'art. 157 bis : 2 822 € si le revenu net global
≤ 17 670 €, 1 411 € jusqu'à 28 430 € (par personne de 65 ans ou plus) ; CSG des pensions : exonération, 3,8 %, 6,6 %,
8,3 % selon le RFR (seuils 2025 : 12 817 / 16 755 / 26 004 € pour une part, + 3 422 / 4 474 / 6 941 € par demi-part),
déductible 3,8 / 4,2 / 5,9 points ; CRDS 0,5 % (sauf exonération) ; CSG des revenus d'activité 9,2 % (6,8 déductibles)
et CRDS 0,5 % sur 98,25 % du brut. Simplifications : tout revenu d'activité du modèle est traité comme un salaire ; tous
les retraités ont 65 ans ou plus ; taux de CSG des pensions de régime stable (le RFR de l'année fixe le taux) ; pas de
CEHR (traitée à part), pas de seuil de recouvrement. Validation contre OpenFisca : valider() ci-dessous.
"""
import numpy as np

SEUILS_IR = np.array([0.0, 11600.0, 29579.0, 84577.0, 181917.0])
TAUX_IR = np.array([0.0, 0.11, 0.30, 0.41, 0.45])
PLAF_QF, PLAF_ISOL = 1807.0, 4262.0
DEC_S, DEC_C, DEC_T = 897.0, 1483.0, 0.4525
ABATPRO = (0.10, 509.0, 14555.0)
ABATPEN = (0.10, 454.0, 4439.0)
AGE = ((17670.0, 2822.0), (28430.0, 1411.0))
CSG_P = [(0.0, 0.0, 0.0), (0.038, 0.038, 0.005), (0.066, 0.042, 0.005), (0.083, 0.059, 0.005)]   # taux, déductible, CRDS
CSG_S1 = [(12817.0, 3422.0), (16755.0, 4474.0), (26004.0, 6941.0)]
ACT = 0.9825
FLAGS0 = dict(abatpen=True, age=True, csg_reduit=True, conjugal=True, qf=True, csg_ded=True, forfait=True)


def bareme_ir(r):
    r = np.clip(r, 0, None)
    out = 0.0 * r
    for i in range(len(SEUILS_IR)):
        hi = SEUILS_IR[i + 1] if i + 1 < len(SEUILS_IR) else np.inf
        out = out + TAUX_IR[i] * np.clip(np.minimum(r, hi) - SEUILS_IR[i], 0, None)
    return out


def parts_enfants(kids):
    return 0.5 * min(kids, 2) + 1.0 * max(kids - 2, 0)


def ir_foyer(r, couple, kids, isole=False, qf=True):
    """IR d'un foyer sur son revenu imposable r (quotient, plafonnement, décote)."""
    p0 = 2.0 if couple else 1.0
    k = kids if qf else 0
    p = p0 + parts_enfants(k) + (0.5 if (isole and k >= 1 and not couple) else 0.0)
    if isole and k >= 1 and not couple:
        cap = PLAF_ISOL + 2 * PLAF_QF * (p - p0 - 1.0)
    else:
        cap = 2 * PLAF_QF * (p - p0)
    i = np.maximum(p * bareme_ir(r / p), p0 * bareme_ir(r / p0) - cap)
    dec = np.clip((DEC_C if couple else DEC_S) - DEC_T * i, 0, None)
    return np.clip(i - dec, 0, None)


def _abat(x, prm):
    t, lo, hi = prm
    return np.minimum(x, np.clip(t * x, lo, hi))


def charge(adultes, kids=0, isole=False, fl=None, frais_reels=None, deduc=None):
    """Charge IR + CSG + CRDS d'un foyer. adultes : liste de (nature 'A' ou 'R', revenu après cotisations z (tableau),
    rapport z / brut des actifs). frais_reels : liste (par adulte) des frais réels déduits si forfait=False.
    Renvoie dict(ir, csg, total)."""
    fl = dict(FLAGS0, **(fl or {}))
    n = len(adultes)
    csg = 0.0
    ri = []
    pens_ab = []
    for j, (nat, z, ra) in enumerate(adultes):
        z = np.asarray(z, float)
        if nat == "A":
            brut = z / ra
            c = (0.092 + 0.005) * ACT * brut
            ded = 0.068 * ACT * brut if fl["csg_ded"] else 0.0 * z
            x = z - ded
            if deduc is not None:
                x = x - deduc[j]
            if fl["forfait"]:
                x = x - _abat(x, ABATPRO)
            elif frais_reels is not None:
                x = np.clip(x - frais_reels[j], 0, None)
            csg = csg + c
            ri.append(x)
            pens_ab.append(None)
        else:
            ri.append(None)
            pens_ab.append(z)
    # pensions : taux de CSG de régime stable, selon le RFR du foyer
    pens = [p for p in pens_ab if p is not None]
    if pens:
        ptot = sum(pens)
        if fl["csg_reduit"]:
            nb = 1.0 * n
            best = None
            for k in range(3, -1, -1):
                t, d, cr = CSG_P[k]
                rp = [p - d * p for p in pens]
                rp = _abat_pens(rp, fl)
                rfr = sum(rp) + sum(x for x in ri if x is not None)
                ok = rfr > (CSG_S1[k - 1][0] + 2 * (nb - 1) * CSG_S1[k - 1][1]) if k > 0 else np.ones_like(rfr, bool)
                if best is None:
                    best = (ok, (t + cr) * ptot, rp)
                    choix_c, choix_r = np.where(ok, (t + cr) * ptot, np.nan), [np.where(ok, a, np.nan) for a in rp]
                else:
                    pas = np.isnan(choix_c) & ok
                    choix_c = np.where(pas, (t + cr) * ptot, choix_c)
                    choix_r = [np.where(pas, a, b) for a, b in zip(rp, choix_r)]
            csg = csg + choix_c
            rp = choix_r
        else:
            d = 0.068 if fl["csg_ded"] else 0.0
            csg = csg + 0.097 * ptot
            rp = _abat_pens([p - d * p for p in pens], fl)
        it = iter(rp)
        ri = [x if x is not None else next(it) for x in ri]
    # abattement des personnes âgées (157 bis), sur le revenu net global du foyer
    if fl["age"] and pens:
        nret = sum(1 for p in pens_ab if p is not None)
        if fl["conjugal"] or n == 1:
            rng = sum(ri)
            ab = nret * np.where(rng <= AGE[0][0], AGE[0][1], np.where(rng <= AGE[1][0], AGE[1][1], 0.0))
            ri = [x - ab * x / np.where(rng > 0, rng, 1) for x in ri]
        else:
            ri = [x - np.where(x <= AGE[0][0], AGE[0][1], np.where(x <= AGE[1][0], AGE[1][1], 0.0)) if a[0] == "R" else x
                  for x, a in zip(ri, adultes)]
    ri = [np.clip(x, 0, None) for x in ri]
    if n == 2 and fl["conjugal"]:
        ir = ir_foyer(ri[0] + ri[1], True, kids, False, fl["qf"])
    elif n == 2:
        haut = (ri[0] >= ri[1])
        ir = (np.where(haut, ir_foyer(ri[0], False, kids, False, fl["qf"]), ir_foyer(ri[0], False, 0))
              + np.where(haut, ir_foyer(ri[1], False, 0), ir_foyer(ri[1], False, kids, False, fl["qf"])))
    else:
        ir = ir_foyer(ri[0], False, kids, isole, fl["qf"])
    return dict(ir=ir, csg=csg, total=ir + csg)


def _abat_pens(rp, fl):
    if not fl["abatpen"]:
        return rp
    t, lo, hi = ABATPEN
    ab = [np.minimum(p, np.maximum(t * p, lo)) for p in rp]
    tot = sum(ab)
    k = np.where(tot > hi, hi / np.where(tot > 0, tot, 1), 1.0)
    return [p - a * k for p, a in zip(rp, ab)]


def valider():
    """Écarts au cas-type OpenFisca (synthese/sorties/cas_types_openfisca.csv, droit des revenus 2025)."""
    import pandas as pd
    from pathlib import Path
    ct = pd.read_csv(Path(__file__).resolve().parents[2] / "synthese/sorties/cas_types_openfisca.csv")
    out = {}
    for prof, nat, kids, isole in (("seul", "A", 0, False), ("couple_2enf", "A", 2, False), ("couple_0enf_mono", "A", 0, False),
                                   ("couple_3enf", "A", 3, False), ("parent_isole_2enf", "A", 2, True),
                                   ("retraite_seul", "R", 0, False), ("retraite_couple", "R", 0, False)):
        g = ct[(ct.profil == prof) & (ct.brut >= 5000) & (ct.brut <= 250000)]
        b = g.brut.values
        if prof.startswith("couple"):
            ad = [(nat, g.base_a.values, g.base_a.values / (b * (1.0 if "mono" in prof else 0.6))),
                  (nat, g.base_b.values, np.where(g.base_b.values > 0, g.base_b.values / np.maximum(b * 0.4, 1), 0.885))]
        elif prof == "retraite_couple":
            ad = [(nat, g.base_a.values, 1.0), (nat, g.base_b.values, 1.0)]
        else:
            ad = [(nat, g.base_a.values, g.base_a.values / b if nat == "A" else 1.0)]
        c = charge(ad, kids, isole)["total"]
        of = (g.ir + g.csg + g.crds).values
        out[prof] = dict(ecart_moyen_abs=float(np.mean(np.abs(c - of))), ecart_max=float(np.max(np.abs(c - of))),
                         ecart_rel_total=float((c.sum() - of.sum()) / of.sum()))
    return out


if __name__ == "__main__":
    for k, v in valider().items():
        print(k, {a: round(b, 3) for a, b in v.items()})
