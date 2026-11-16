"""Foyers purs : chaque foyer représentatif de bareme_v3 est séparé en foyers d'actifs et foyers de retraités.

Pourquoi (revue/verif_ir_csg.md, points graves 1 et 2) : dans le modèle d'origine, chaque foyer d'une tranche a la
même composition de revenus (environ 70 % d'activité, 30 % de pensions et de chômage). La franchise d'activité profite
alors aux retraités, la répartition « qui paie » se fait au prorata du revenu net, la recette n'est pas tenue et la
marge extensive des personnes seules est un artefact.

Construction (lecture seule de ir_csg/ ; rien n'y est modifié) :
- Dans chaque point représentatif (tranche de RFR de l'IRCOM 2024, 60 points par tranche), deux sortes de foyers :
  actifs (salaires, gérants, indépendants et loyers, plus le chômage) et retraités (pensions seules).
- Ils ont le même revenu net (assiette du nouvel impôt, ZN) que le foyer représentatif. Leurs poids respectent les
  masses de la tranche : part des retraités = pensions nettes / assiette nette de la tranche. Les masses brutes et
  la masse du revenu du travail qui réagit (LAB) sont alors respectées elles aussi (contrôlé dans controles()).
  Hypothèse : à revenu net égal, un retraité et un actif ont presque le même RFR (0,85 contre 0,83 à 0,86 fois ZN).
- Couples homogènes (deux actifs ou deux retraités), même part de couples par tranche dans les deux groupes
  (hypothèse ; contrôlée face aux 4,3 M de cases 1BS), même partage des revenus (Insee, bareme_v3.PARTAGE).
- Enfants : seulement chez les actifs. 1 965 339 parents isolés (cases 0BT des déclarations 2042), un enfant chacun
  (hypothèse du modèle d'origine) ; les 16,0 M d'enfants restants vont aux couples d'actifs, deux par couple
  « avec enfants » ; même proportion dans toutes les tranches (hypothèse).
- Charge actuelle (IR + CSG + CRDS) : la charge de chaque point (donc de chaque tranche) est gardée ; elle est
  répartie entre types selon les charges des cas-types OpenFisca au même revenu net (ex.CT, colonne actuel selon
  base_a + base_b) : seul, couple sans enfant, couple avec deux enfants ; parent isolé = seul moins le gain de
  quotient familial (case T) ; retraité seul = cas-type retraite_seul ; couple de retraités = couple d'actifs sans
  enfant × (retraité seul / actif seul) à la moitié du revenu (pas de cas-type de couple retraité : hypothèse).
- Perte sèche : l'élasticité ne porte que sur le revenu du travail des actifs (salaires, gérants, 70 % des revenus
  des indépendants et loyers, comme dans le modèle d'origine) ; les pensions et le chômage ne réagissent pas.

Utilisé par synthese/perte_seche_ircsg_purs.py.
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path[:0] = [str(HERE), str(ROOT / "ir_csg"), str(ROOT)]
import proposition as P  # noqa: E402
import ps_ircsg_methode as ps  # noqa: E402  (coin(), ptr_rest_single(), SMIC, PASS, SALSH)

v, ex = P.v, P.ex
m, x = v.m, v.x
W, Z, ZN, Q, DEC, S = P.W, P.Z, P.ZN, P.Q, P.DEC, P.S
TR = v.f.tranche
CUR = v.CUR                                   # charge actuelle IR + CSG + CRDS du foyer représentatif
CIBLE = v.CIBLE
TAU0 = v.bl.TAU_CUR                           # taux marginal actuel IR-CSG des actifs, par euro brut
CT = ex.CT
ENF_CT = ex.ENF


def par_tranche(serie):
    """Valeur de la tranche, recopiée sur chaque point représentatif."""
    return TR.map(dict(zip(x.tranche, np.asarray(serie)))).values


# ------------------------------------------------------------------ composition des tranches
ACT_B = m.F_SAL * x.sal + m.F_GER * x.ger + m.F_AUT * x.ind + m.F_CHO * x.cho          # actifs, brut (type CSG)
ACT_N = v.F_SAL_N * x.sal + v.F_GER_N * x.ger + v.F_AUT_N * x.ind + v.F_CHO_N * x.cho  # actifs, après cotisations
PEN_N = v.F_PENS_N * x.pens                                                              # pensions (brut = net)
PI = par_tranche(PEN_N / x.assiette3)          # part des foyers de retraités dans le point (masse des pensions)
W_A, W_R = W * (1 - PI), W * PI
Z_A = ZN * par_tranche(ACT_B / ACT_N)          # revenu brut d'un foyer d'actifs
Z_R = ZN.copy()                                # pension : brut = net (assiette du modèle)
R_A = ZN / Z_A                                 # rapport net / brut des actifs (0,90 ; défaut 3 de la vérification)
LAB_A = par_tranche((m.F_SAL * x.sal + m.F_GER * x.ger + 0.7 * m.F_AUT * x.ind) / ACT_B)  # part qui réagit
ACTIV_A = ZN * par_tranche((ACT_N - v.F_CHO_N * x.cho) / ACT_N)   # revenus d'activité nets (sans le chômage)
SAL_A = ZN * par_tranche((v.F_SAL_N * x.sal + v.F_GER_N * x.ger) / ACT_N)  # salaires et gérants seuls
# RFR d'un foyer d'actifs : 90 % des salaires, gérants et chômage (frais professionnels), indépendants et loyers
RFR_A = ZN * par_tranche((0.9 * (x.sal + x.ger + x.cho) + x.ind) / ACT_N)

# ------------------------------------------------------------------ enfants et parents isolés
ENFANTS = v.bl.ENFANTS                         # 18,0 M (0CF + 0DJ + 0CH / 2)
CASES_T = 1965339.0                            # cases 0BT, déclarations 2042 des revenus 2024
NS_A = CASES_T / (W_A * (1 - S)).sum()         # part des actifs seuls qui sont parents isolés (un enfant)
NC_A = (ENFANTS - CASES_T) / (W_A * S).sum()   # enfants par couple d'actifs
assert NC_A <= 2.0, "trop d'enfants pour les couples d'actifs"

# ------------------------------------------------------------------ quotient familial des enfants aujourd'hui
GAIN_S = P.ir_actuel(RFR_A, False, 0) - P.ir_actuel(RFR_A, False, 1)    # parent isolé, case T, un enfant
GAIN_C = P.ir_actuel(RFR_A, True, 0) - P.ir_actuel(RFR_A, True, 2)      # couple, deux enfants
QF_ISOLES = (W_A * (1 - S) * NS_A * GAIN_S).sum() / 1e9
QF_COUPLES = (W_A * S * NC_A / 2 * GAIN_C).sum() / 1e9
QF_COUT = QF_ISOLES + QF_COUPLES
CHEQUE = QF_COUT * 1e9 / ENFANTS               # variante « chèque » : même montant par enfant

# ------------------------------------------------------------------ types de foyers
# (nom, groupe A/R, famille, poids, parts des adultes, enfants)
TYPES = [("seul", "A", "seuls", W_A * (1 - S) * (1 - NS_A), [1.0], 0),
         ("parent_isole", "A", "parents_isoles", W_A * (1 - S) * NS_A, [1.0], 1)]
for _s, _p in v.PARTAGE:
    TYPES.append((f"couple0_{_s}", "A", "couples0", W_A * S * (1 - NC_A / 2) * _p, [_s, 1 - _s], 0))
    TYPES.append((f"couple2_{_s}", "A", "couples2", W_A * S * NC_A / 2 * _p, [_s, 1 - _s], 2))
TYPES.append(("retraite_seul", "R", "seuls", W_R * (1 - S), [1.0], 0))
for _s, _p in v.PARTAGE:
    TYPES.append((f"retraite_couple_{_s}", "R", "couples0", W_R * S * _p, [_s, 1 - _s], 0))


# ------------------------------------------------------------------ charge actuelle par type
def _taux_ct(profil):
    """Charge actuelle / revenu net du cas-type OpenFisca, en fonction du revenu net du foyer (base_a + base_b)."""
    g = CT[CT.profil == profil].sort_values("brut")
    zn = (g.base_a + g.base_b).values
    return lambda z: np.interp(z, zn, g.actuel.values / zn)


r_seul, r_ret = _taux_ct("seul"), _taux_ct("retraite_seul")
r_c0, r_c2 = _taux_ct("couple_0enf"), _taux_ct("couple_2enf")


def rho(z):
    """Charge d'un retraité seul / charge d'un actif seul, au même revenu net z (OpenFisca)."""
    return r_ret(z) / r_seul(z)


_U = {"seul": ZN * r_seul(ZN), "parent_isole": np.maximum(ZN * r_seul(ZN) - GAIN_S, 0.0),
      "couple0": ZN * r_c0(ZN), "couple2": ZN * r_c2(ZN), "retraite_seul": ZN * r_ret(ZN),
      "retraite_couple": ZN * r_c0(ZN) * rho(ZN / 2)}


def _cle(nom):
    return nom if nom in _U else nom.rsplit("_", 1)[0]


_NORM = sum(w * _U[_cle(nom)] for nom, _, _, w, _, _ in TYPES) / W
CURT = {nom: np.where(_NORM > 0, CUR * _U[_cle(nom)] / np.where(_NORM > 0, _NORM, 1), CUR) for nom, *_ in TYPES}

# ------------------------------------------------------------------ options et impôt fusionné
# sur : revenus couverts par la franchise F ("activite" : salaires, gérants, indépendants, loyers ; "salaires" :
# salaires et gérants ; "tout" : tous les revenus, pensions comprises) ; abat_pens : abattement proportionnel sur
# les pensions ; Fp : exonération des pensions jusqu'à Fp par retraité (si Fp_degressif : totale jusqu'à Fp, nulle
# à 2·Fp) ; fam : rien, franchise (6 000 € par enfant, parent qui gagne le plus), cheque, quotient.
OPT0 = dict(F=0.0, sur="activite", abat_pens=0.0, Fp=0.0, Fp_degressif=False, fam="rien")


def impot_adultes(tm, T, o, zs, ls, ps_, kids):
    """Impôt du foyer, taux marginal de chaque adulte sur son activité, assiette taxable de chaque adulte.
    zs : revenu net de chaque adulte ; ls : sa part couverte par la franchise ; ps_ : sa pension."""
    ab = []
    for p in ps_:
        exo = np.clip(2 * o["Fp"] - p, 0, p) if o["Fp_degressif"] else np.minimum(o["Fp"], p)
        ab.append(exo + o["abat_pens"] * p)
    tax = [np.clip(z - np.minimum(o["F"], l) - a, 0, None) for z, l, a in zip(zs, ls, ab)]
    actif = [l > o["F"] for l in ls]                  # le dernier euro d'activité est-il au-delà de la franchise ?
    fam = o["fam"]
    if fam == "quotient":                             # quotient conjugal et familial, plafonds actuels
        y = sum(tax)
        if len(zs) == 2:
            p0, p = 2.0, 2.0 + 0.5 * kids
            cap = 2 * P.PLAF * (p - p0)
        else:
            p0, p = 1.0, 1.0 + (1.0 if kids else 0.0)
            cap = P.PLAF_ISOL if kids else 0.0
        i0, i1 = p0 * T(y / p0), p * T(y / p)
        imp = np.maximum(i1, i0 - cap)
        mg = np.where(i0 - cap > i1, tm(y / p0), tm(y / p))
        return imp, [np.where(a & (y > 0), mg, 0.0) for a in actif], tax
    if fam == "franchise" and kids:
        haut = np.argmax(np.vstack(zs), axis=0) if len(zs) == 2 else np.zeros(len(zs[0]), int)
        tax = [np.where(haut == k, np.clip(t - P.FR_ENF * kids, 0, None), t) for k, t in enumerate(tax)]
    imp = sum(T(t) for t in tax)
    if fam == "cheque":
        imp = imp - CHEQUE * kids
    return imp, [np.where(a & (t > 0), tm(t), 0.0) for a, t in zip(actif, tax)], tax


def adultes(grp, parts, o, sans=None):
    """Revenus des adultes d'un type (listes zs, ls, ps). sans = k : l'adulte k perd son revenu d'activité."""
    if grp == "A":
        lab = {"activite": ACTIV_A, "salaires": SAL_A, "tout": ZN}[o["sur"]]
        pens = 0.0 * ZN
    else:
        lab = ZN if o["sur"] == "tout" else 0.0 * ZN
        pens = ZN
    zs, ls, ps_ = [sh * ZN for sh in parts], [sh * lab for sh in parts], [sh * pens for sh in parts]
    if sans is not None:
        zs[sans] = np.clip(zs[sans] - parts[sans] * ACTIV_A, 0, None)
        ls[sans] = 0.0 * ZN
    return zs, ls, ps_


def recette(tm, T, o):
    return sum((w * impot_adultes(tm, T, o, *adultes(g, parts, o), kids)[0]).sum()
               for _, g, _, w, parts, kids in TYPES) / 1e9


def elast(jeu="central"):
    """Élasticité du revenu brut d'un foyer d'actifs (barème du modèle × part du travail qui réagit)."""
    a, b, c, d = v.ELAST[jeu]
    return np.select([Q < 0.5, Q < 0.9, Q < 0.99], [a, b, c], d) * LAB_A


QUAD0 = (W_A * 0.5 * elast() * Z_A * TAU0 ** 2 / (1 - TAU0)).sum() / 1e9    # perte quadratique d'aujourd'hui


# ------------------------------------------------------------------ taux de participation d'aujourd'hui (PTR)
def _ptr0():
    """PTR IR-CSG actuel de chaque adulte actif (comme ps_ircsg_methode.evalue, RFR du foyer d'actifs)."""
    out = {}
    for nom, g_, _, w, parts, kids in TYPES:
        if g_ != "A":
            continue
        for k, sh in enumerate(parts):
            g = sh * Z_A * LAB_A
            couple = len(parts) == 2
            d = P.ir_actuel(RFR_A, couple, kids) - P.ir_actuel(np.clip(RFR_A - 0.75 * g, 0, None), couple, kids)
            out[(nom, k)] = np.where(g > 0, d / np.maximum(g, 1.0) + 0.097, 0.0)
    return out


PTR0 = _ptr0()
SMIC = ps.SMIC


# ------------------------------------------------------------------ méthode v2 (revue/methode_v2.md)
# Élasticités du revenu réellement produit (marge intensive : heures, effort, carrière), par groupe de revenu
# (moitié du bas, 50-90 %, 90-99 %, 1 % du haut) ; élasticités du revenu déclaré (forme, calendrier, société),
# dixième du haut seulement ; élasticité de participation η (adultes sous 2 Smic). Sources : cours/elasticites-france.tex.
V2 = {"bas": dict(reel=(0.02, 0.05, 0.05, 0.05), decl=(0.10, 0.15), eta=0.10),
      "central": dict(reel=(0.05, 0.10, 0.10, 0.10), decl=(0.20, 0.30), eta=0.25),
      "haut": dict(reel=(0.10, 0.20, 0.25, 0.25), decl=(0.30, 0.45), eta=0.50)}
S_DEPL, TAU_ALT = 0.5, 0.486       # part de la réaction déclarée qui passe vers l'IS puis le PFU, et son taux


def elast_v2(jeu="central"):
    c = V2[jeu]
    a, b, cc, d = c["reel"]
    reel = np.select([Q < 0.5, Q < 0.9, Q < 0.99], [a, b, cc], d)
    decl = np.select([Q < 0.9, Q < 0.99], [0.0, c["decl"][0]], c["decl"][1])
    return reel, decl, c["eta"]


def evalue(nom, tm, T, o, jeu="central", eta=0.25, sorties=True):
    """Recette, perte sèche (quadratique, coins IR-CSG, non contributif, toutes cotisations, déplacement s = 0,5,
    marge extensive) et indicateurs de répartition, pour les foyers purs. Variation par rapport à aujourd'hui.
    Méthode v2 (clés v2_*) : réaction au taux de l'impôt fusionné (saillance), coûtée au coin total non contributif ;
    revenu réel et revenu déclaré séparés ; marge extensive avec η du jeu."""
    e = elast(jeu)
    eR, eD, eta2 = elast_v2(jeu)
    top = Q >= 0.9
    acc = dict(modele=0.0, c0=0.0, tout=0.0, nc=0.0, nc_s50_486=0.0, ext_nc=0.0, ext_tout=0.0, ext_nc_seuls_05_2=0.0,
               v2_reel=0.0, v2_ext=0.0, v2_decl_recette=0.0, v2_decl_dq=0.0, v2_reel_dq=0.0)
    res = {}
    for tnom, grp, fam_, w, parts, kids in TYPES:
        imp, mgs, _ = impot_adultes(tm, T, o, *adultes(grp, parts, o), kids)
        res[tnom] = (w, imp, CURT[tnom], grp, fam_)
        if grp == "R":                                        # pensions : pas de réaction
            continue
        single = 1.0 if len(parts) == 1 else 0.0
        for k, (sh, mg) in enumerate(zip(parts, mgs)):
            t1, t0 = np.clip(mg * R_A, 0, 0.95), TAU0
            z = sh * Z_A
            g = z * LAB_A                                     # revenu brut du travail de l'adulte
            acc["modele"] += (w * 0.5 * e * z * t1 ** 2 / (1 - t1)).sum() / 1e9
            acc["c0"] += (w * e * z * (np.log((1 - t0) / (1 - t1)) - (t1 - t0))).sum() / 1e9
            for conv in ("tout", "nc"):
                er, ee, pa = ps.coin(g, single, conv)
                er, ee, pa = ps.SALSH * er, ps.SALSH * ee, ps.SALSH * pa
                a0 = np.clip(1 - t0 - ee - pa, 0.03, None)
                a1 = np.clip(1 - t1 - ee - pa, 0.03, None)
                dq = e * z * (1 + er) * (np.log(a1) - np.log(a0))
                pse = e * z * ((1 + er) * np.log(a0 / a1) + (a1 - a0))
                acc[conv] += (w * pse).sum() / 1e9
                if conv == "nc":                              # déplacement de la moitié de la réaction du haut
                    acc["nc_s50_486"] += (w * (pse + np.where(top, 0.5 * 0.486, 0.0) * dq)).sum() / 1e9
                    # v2 : la quantité réagit au taux net de l'impôt fusionné ; chaque euro perdu coûte le coin total
                    dl = np.log(1 - t1) - np.log(1 - t0)
                    coin_m = er + ee + pa + (t0 + t1) / 2         # coin moyen, par euro de salaire brut
                    dq_r, dq_d = eR * g * dl, eD * g * dl
                    acc["v2_reel"] += (w * -coin_m * dq_r).sum() / 1e9
                    for cle, m_ in (("q50", Q < 0.5), ("q90", (Q >= 0.5) & (Q < 0.9)), ("q99", (Q >= 0.9) & (Q < 0.99)),
                                    ("top1", Q >= 0.99)):
                        acc["v2_reel_" + cle] = acc.get("v2_reel_" + cle, 0.0) + (w * -coin_m * dq_r * m_).sum() / 1e9
                    acc["v2_reel_dq"] += (w * dq_r).sum() / 1e9
                    acc["v2_decl_dq"] += (w * dq_d).sum() / 1e9
                    acc["v2_decl_recette"] += (w * (coin_m - S_DEPL * TAU_ALT) * dq_d).sum() / 1e9
            # marge extensive : impôt du foyer avec et sans le revenu d'activité de l'adulte k
            imp_wo = impot_adultes(tm, T, o, *adultes(grp, parts, o, sans=k), kids)[0]
            ptr1 = np.where(g > 0, (imp - imp_wo) / np.maximum(g, 1.0), 0.0)
            ptr0 = PTR0[(tnom, k)]
            for conv in ("tout", "nc"):
                if single:
                    rest = ps.ptr_rest_single(g) - (0.1005 if conv == "nc" else 0.0)
                else:
                    rest = 0.1131 if conv == "tout" else 0.0126
                p0 = np.clip(ptr0 + rest, -0.5, 0.97)
                p1 = np.clip(ptr1 + rest, -0.5, 0.97)
                pse = eta * g * (np.log((1 - p0) / (1 - p1)) - (p1 - p0))
                dans = (g > 1000) & (g < 2 * SMIC)            # adultes sous 2 Smic, personnes seules comprises
                acc["ext_" + conv] += (w * pse * dans).sum() / 1e9
                if conv == "nc" and single:
                    acc["ext_nc_seuls_05_2"] += (w * pse * dans * (g >= 0.5 * SMIC)).sum() / 1e9
                if conv == "nc":
                    acc["v2_ext"] += (w * pse * dans).sum() / 1e9 * eta2 / eta
    out = dict(nom=nom, recette=sum((w * imp).sum() for w, imp, *_ in res.values()) / 1e9, **acc)
    out["quad"] = acc["modele"] - QUAD0
    out["cen"] = acc["nc_s50_486"] + acc["ext_nc"]           # critère central (revue/methode_perte_seche.md)
    out["v2"] = acc["v2_reel"] + acc["v2_ext"]               # v2 : perte sèche sur l'activité réelle
    out["v2_tout"] = out["v2"] - acc["v2_decl_recette"]      # v2 + revenu déclaré compté comme une perte (Feldstein)
    if sorties:
        out.update(repartition(res))
    return out


def repartition(res):
    """Déciles (€ par foyer), groupes (Md€ et € par foyer), 1 % du haut, perdants de plus de 500 €."""
    dn = sum(w * (imp - cur) for w, imp, cur, *_ in res.values())             # variation par point (€)
    d = pd.DataFrame({"dec": DEC + 1, "w": W, "dn": dn}).groupby("dec").sum()
    grp = {}
    for cle, filtre in (("actifs", lambda g, f: g == "A"), ("retraites", lambda g, f: g == "R"),
                        ("seuls", lambda g, f: f == "seuls"), ("seuls_actifs", lambda g, f: f == "seuls" and g == "A"),
                        ("seuls_retraites", lambda g, f: f == "seuls" and g == "R"),
                        ("parents_isoles", lambda g, f: f == "parents_isoles"), ("couples0", lambda g, f: f == "couples0"),
                        ("couples0_actifs", lambda g, f: f == "couples0" and g == "A"),
                        ("couples0_retraites", lambda g, f: f == "couples0" and g == "R"),
                        ("couples2", lambda g, f: f == "couples2")):
        sel = [(w, imp, cur) for w, imp, cur, g, f in res.values() if filtre(g, f)]
        md = sum((w * (imp - cur)).sum() for w, imp, cur in sel) / 1e9
        nb = sum(w.sum() for w, _, _ in sel)
        grp[cle] = dict(Md=md, eur=1e9 * md / nb, foyers_M=nb / 1e6)
    perd = sum((w * (imp - cur > 500)).sum() for w, imp, cur, *_ in res.values()) / W.sum()
    ecart = sum((w * np.abs(imp - cur)).sum() for w, imp, cur, *_ in res.values()) / W.sum()
    return dict(dec_eur=list(d.dn / d.w), dec_foyers=list(d.w), groupes=grp, perdants500=100 * perd, ecart_moyen=ecart,
                top1_Md=(dn * (Q >= 0.99)).sum() / 1e9, top10_Md=(dn * (Q >= 0.9)).sum() / 1e9,
                total_Md=dn.sum() / 1e9)


# ------------------------------------------------------------------ cas-types
def cas_type(tm, T, o, profil, brut):
    """Variation de charge d'un cas-type OpenFisca (€ par an) : impôt fusionné moins IR + CSG + CRDS actuels."""
    g = CT[(CT.profil == profil) & (CT.brut == brut)].iloc[0]
    kids = ENF_CT[profil]
    a = np.array([g.base_a])
    if profil == "retraite_seul":
        zs, ps_ = [a], [a]
        ls = [a if o["sur"] == "tout" else 0 * a]
    else:
        zs = [a] if g.base_b == 0 else [a, np.array([g.base_b])]
        ls, ps_ = list(zs), [0 * u for u in zs]              # salariés : tout leur revenu est d'activité
    imp = impot_adultes(tm, T, o, zs, ls, ps_, kids)[0]
    return float(imp[0] - g.actuel)


# ------------------------------------------------------------------ contrôles de construction
def controles():
    """Lignes de texte : calage, masses, effectifs, quotient familial, charge actuelle des retraités."""
    L = []
    cur_tot = sum((w * CURT[nom]).sum() for nom, _, _, w, _, _ in TYPES) / 1e9
    L.append(f"Calage : charge actuelle des foyers purs {cur_tot:.2f} Md€ ; cible (IR + CSG + CRDS du modèle) "
             f"{CIBLE:.2f} Md€ ; écart {cur_tot - CIBLE:+.3f}")
    L.append(f"Masses : pensions nettes {(W_R * ZN).sum() / 1e9:.1f} Md€ (tranches : {PEN_N.sum():.1f}) ; revenus nets"
             f" des actifs {(W_A * ZN).sum() / 1e9:.1f} (tranches : {ACT_N.sum():.1f}) ; revenu brut total"
             f" {((W_A * Z_A).sum() + (W_R * Z_R).sum()) / 1e9:.1f} (modèle : {(W * Z).sum() / 1e9:.1f}) ; revenu du"
             f" travail qui réagit {(W_A * Z_A * LAB_A).sum() / 1e9:.1f} (modèle : {(W * Z * v.bl.LAB).sum() / 1e9:.1f})")
    L.append(f"Perte sèche quadratique d'aujourd'hui : {QUAD0:.2f} Md€ (modèle d'origine : {v.cout_actuel():.2f})")
    # effectifs
    L.append(f"Foyers de retraités {W_R.sum() / 1e6:.2f} M (IRCOM, foyers déclarant des pensions :"
             f" {x.foyers_pensions.sum() / 1e6:.2f} M ; cases 1AS : 13,15 M) ; foyers d'actifs {W_A.sum() / 1e6:.2f} M"
             f" (IRCOM, foyers déclarant des salaires : {x.foyers_salaires.sum() / 1e6:.2f} M)")
    L.append(f"Couples de retraités {(W_R * S).sum() / 1e6:.2f} M (cases 1BS, pension du déclarant 2 : 4,32 M) ;"
             f" couples d'actifs {(W_A * S).sum() / 1e6:.2f} M ; couples au total {(W * S).sum() / 1e6:.2f} M (2042 : 13,05 M)")
    tab = pd.DataFrame({"tranche": x.tranche, "foyers_M": x.foyers / 1e6,
                        "retraites_masse_%": 100 * PEN_N / x.assiette3,
                        "avec_pensions_IRCOM_%": 100 * x.foyers_pensions / x.foyers,
                        "avec_salaires_IRCOM_%": 100 * x.foyers_salaires / x.foyers,
                        "ni_l_un_ni_l_autre_min_%": 100 * np.clip(x.foyers - x.foyers_pensions - x.foyers_salaires, 0, None) / x.foyers})
    L.append("Part des foyers de retraités par tranche : masse des pensions (modèle) et foyers déclarant des pensions"
             " (IRCOM ; un foyer qui a les deux est compté deux fois) :")
    L.append(tab.head(10).round(1).to_string(index=False))
    n_pi = (W_A * (1 - S) * NS_A).sum()
    n_c2 = (W_A * S * NC_A / 2).sum()
    L.append(f"Parents isolés {n_pi / 1e6:.3f} M (cases 0BT : 1,965 M ; modèle d'origine : "
             f"{(W * (1 - S) * P.NS).sum() / 1e6:.2f} M) ; couples avec deux enfants {n_c2 / 1e6:.2f} M, soit"
             f" {100 * NC_A / 2:.0f} % des couples d'actifs ; enfants {(n_pi + 2 * n_c2) / 1e6:.2f} M (cible 18,0)")
    # quotient familial
    rfr_f = v._RFR_F
    gs_f = P.ir_actuel(rfr_f, False, 0) - P.ir_actuel(rfr_f, False, 1)
    gc_f = P.ir_actuel(rfr_f, True, 0) - P.ir_actuel(rfr_f, True, 2)
    qf_f = ((W_A * (1 - S) * NS_A * gs_f).sum() + (W_A * S * NC_A / 2 * gc_f).sum()) / 1e9
    L.append(f"Quotient familial des enfants : {QF_COUT:.2f} Md€ (couples {QF_COUPLES:.2f}, parents isolés"
             f" {QF_ISOLES:.2f}) ; avec le RFR du foyer représentatif (capital au PFU compris) : {qf_f:.2f} ;"
             f" vérification : 12,9 (9,7 + 3,3) ; modèle d'origine : {P.QF_COUT:.1f} ; chèque {CHEQUE:,.0f} € par enfant")
    # charge actuelle
    k = x.set_index("tranche")
    csg_p = (k.t_pens * m.F_PENS * k.pens).sum()
    crds_p = (v.T_CRDS * m.F_PENS * k.pens * (k.t_pens > 0)).sum()
    ir_p = (k.ir_trav * m.F_PENS * k.pens / k.assiette).sum()
    cur_r = sum((w * CURT[nom]).sum() for nom, g_, _, w, _, _ in TYPES if g_ == "R") / 1e9
    cur_a = sum((w * CURT[nom]).sum() for nom, g_, _, w, _, _ in TYPES if g_ == "A") / 1e9
    L.append(f"Charge actuelle des retraités {cur_r:.1f} Md€ ({100 * cur_r / (W_R * ZN).sum() * 1e9:.1f} % de leurs"
             f" pensions) ; des actifs {cur_a:.1f} Md€ ({100 * cur_a / (W_A * ZN).sum() * 1e9:.1f} % de leur revenu net)")
    L.append(f"   repère, pensions dans le modèle d'origine (par_type) : CSG {csg_p:.1f} + CRDS {crds_p:.1f} + IR au prorata"
             f" de l'assiette {ir_p:.1f} = {csg_p + crds_p + ir_p:.1f} Md€ (vérification : environ 41)")
    for z_ in (20e3, 30e3, 50e3, 100e3):
        L.append(f"   OpenFisca, revenu net {z_ / 1e3:.0f} k€ : charge d'un retraité seul {100 * r_ret(z_):.1f} %, d'un actif seul"
                 f" {100 * r_seul(z_):.1f} % (rapport {rho(z_):.2f})")
    # sensibilité : couple de retraités évalué au revenu / 1,5 au lieu de la moitié (seuils de CSG d'un couple plus bas
    # que deux fois ceux d'une personne seule ; le rapport exact n'est pas vérifié ici)
    u = dict(_U, retraite_couple=ZN * r_c0(ZN) * rho(ZN / 1.5))
    norm = sum(w * u[_cle(nom)] for nom, _, _, w, _, _ in TYPES) / W
    cur_r15 = sum((w * CUR * u[_cle(nom)] / norm).sum() for nom, g_, _, w, _, _ in TYPES if g_ == "R") / 1e9
    L.append(f"   sensibilité : couple de retraités évalué au revenu / 1,5 au lieu de la moitié : charge des retraités"
             f" {cur_r15:.1f} Md€")
    return L
