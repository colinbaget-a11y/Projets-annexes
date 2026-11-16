"""Perte sèche généralisée de la fusion IR-CSG-CRDS, variantes (lecture seule du dépôt).

Lancer : cd fiscalite/ir_csg && python3 -B <ce fichier>
Formule : dPS = - sum_a ( (T0+T1)/2 - s*tau_k ) * dQ_a,  dQ_a = e*z_a*(1+c_er)*[ln(1-tau1-c_ee-c_pa) - ln(1-tau0-c_ee-c_pa)]
avec 1-T = (1-tau-c_ee-c_pa)/(1+c_er) (coin sur le coût du travail).
Marge extensive : dPS_ext = - sum_a PTRbar * eta * g_a * [ln(1-PTR1) - ln(1-PTR0)].
"""
import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path[:0] = [str(ROOT / 'ir_csg'), str(ROOT)]
import proposition as P  # noqa: E402

v, ex = P.v, P.ex
m = v.m
x = v.x
W, Z, ZN, Q, R = P.W, P.Z, P.ZN, P.Q, P.R
TR = v.f.tranche
LAB = v.bl.LAB                                   # part du travail dans l'assiette brute
TAU0 = v.bl.TAU_CUR                              # taux marginal IR+CSG actuel (par euro de Z)
SMIC = 11.88 * 151.67 * 12                       # 21 621,6 euros brut annuel (2025)
PASS = 47100.0
BAR = json.loads((ROOT / 'ir_csg/sorties/proposition_baremes.json').read_text())


def par_tranche(serie):
    return TR.map(dict(zip(x.tranche, serie.values))).values


SALSH = par_tranche(m.F_SAL * x.sal / (m.F_SAL * x.sal + m.F_GER * x.ger + 0.7 * m.F_AUT * x.ind))
PSH = par_tranche(v.F_PENS_N * x.pens / x.assiette3)              # pensions / assiette nette
LAB_SAL = ZN * par_tranche((v.F_SAL_N * x.sal + v.F_GER_N * x.ger) / x.assiette3)


# ------------------------------------------------------------------ coin hors IR-CSG, par euro de brut
def coin(g, single, conv):
    """c_er, c_ee, c_pa par euro de salaire brut. conv = 'tout' (toutes cotisations, OCDE) ou 'nc' (hors
    cotisations contributives : vieillesse plafonnée, Agirc-Arrco hors CEG/CET, chômage). Barèmes 2025 lus dans
    OCDE Taxing Wages 2025 (fichier du dépôt) ; sous le Smic : heures au Smic horaire (4,3 % employeur, Cour des
    comptes 2024 ; prime d'activité 11,2 % = METR TaxBEN 50->100 % moins CSG-CRDS et cotisations salariales)."""
    g = np.asarray(g, float)
    er = np.select([g < SMIC, g < 1.6 * SMIC, g < PASS, g < 2.25 * SMIC, g < 3.3 * SMIC],
                   [0.043, 0.902, 0.3635, 0.3657, 0.4257], 0.4436)
    ee = np.where(g < PASS, 0.1131, 0.10256)
    pa = np.where(g < SMIC, 0.112, np.where(g < 27579.0, 0.316, 0.0)) * single
    if conv == 'nc':
        er = er - np.where(g < PASS, 0.1732, 0.1700)
        ee = ee - np.where(g < PASS, 0.1005, 0.0864)
    return er, ee, pa


# options d'arbitrage sur les pensions (synthese/perte_seche_ircsg.py) : Fp = franchise sur les pensions ;
# Fp_degressif = exonération totale jusqu'à Fp, nulle à 2·Fp ; abat_pens = abattement proportionnel
EXTRA = dict(Fp=0.0, Fp_degressif=False, abat_pens=0.0)


def _pens(p):
    fp = EXTRA["Fp"]
    if EXTRA["Fp_degressif"]:
        a = np.clip(2 * fp - p, 0, p)
    else:
        a = np.minimum(fp, p)
    return a + EXTRA["abat_pens"] * p


# ------------------------------------------------------------------ impôt par type (copie de P.impot_type + abattement pensions)
def impot_type(tm, T, F, fam, parts, kids, lab, A0=0.0):
    zs = [sh * ZN for sh in parts]
    ls = [sh * lab for sh in parts]
    ps = [sh * ZN * PSH for sh in parts]
    ab = [np.minimum(p, np.clip(A0 - 0.5 * np.clip(p - A0, 0, None), 0, None)) if A0 else 0.0 for p in ps]
    ab = [a + _pens(p) for a, p in zip(ab, ps)]
    tax = [np.clip(z - np.minimum(F, l) - a, 0, None) for z, l, a in zip(zs, ls, ab)]
    actif = [l > F for l in ls]
    if fam == 'quotient':
        y = sum(tax)
        if len(parts) == 2:
            p0, p = 2.0, 2.0 + 0.5 * kids
            cap = 2 * P.PLAF * (p - p0)
        else:
            p0, p = 1.0, 1.0 + (1.0 if kids else 0.0)
            cap = P.PLAF_ISOL if kids else 0.0
        i0, i1 = p0 * T(y / p0), p * T(y / p)
        borne = i0 - cap > i1
        imp = np.maximum(i1, i0 - cap)
        mg = np.where(borne, tm(y / p0), tm(y / p))
        return imp, [np.where(a, mg, 0.0) for a in actif], tax
    if fam == 'franchise' and kids:
        haut = np.argmax(np.vstack(zs), axis=0) if len(zs) == 2 else np.zeros(len(ZN), int)
        tax = [np.where(haut == k, np.clip(t - P.FR_ENF * kids, 0, None), t) for k, t in enumerate(tax)]
    imp = sum(T(t) for t in tax)
    if fam == 'cheque':
        imp = imp - P.CHEQUE * kids
    mg = [np.where(a & (t > 0), tm(t), 0.0) for a, t in zip(actif, tax)]
    return imp, mg, tax


def recette(tm, T, F, fam, lab, A0):
    return sum((w * impot_type(tm, T, F, fam, parts, kids, lab, A0)[0]).sum() for _, w, parts, kids, _ in P.TYPES) / 1e9


def cale(r, F, fam, lab, A0, top):
    lo, hi = 0.0, top
    for _ in range(40):
        t1 = (lo + hi) / 2
        tm, T = ex.bareme_lineaire([0, 20e3, r['z1'], r['z2']], [r['t0'], r['tb'], t1, top])
        lo, hi = (t1, hi) if recette(tm, T, F, fam, lab, A0) < v.CIBLE else (lo, t1)
    t1 = (lo + hi) / 2
    return t1, ex.bareme_lineaire([0, 20e3, r['z1'], r['z2']], [r['t0'], r['tb'], t1, top])


# ------------------------------------------------------------------ PTR (marge extensive)
def ptr_rest_single(g):
    """Partie du PTR hors IR-CSG, personne seule (base brute) : OCDE TaxBEN 2025 sans aide au logement,
    PTR 54,2 % à 0,5 Smic (calc.), 43,1 % au Smic, 49,1 % à 0,67 SM, 45 % au SM ; au-delà, (cotisations
    salariales + 7 822 euros de minima perdus) / brut. On retire le taux moyen CSG-IR des fichiers OCDE."""
    g = np.maximum(np.asarray(g, float), 1.0)
    hi = (0.1131 * np.minimum(g, PASS) + 0.10256 * np.clip(g - PASS, 0, None) + 7822.0) / g
    lo = np.interp(g, [0.5 * SMIC, SMIC], [0.542 - 0.0953, 0.431 - 0.0953])
    a60 = (0.1131 * 27579.0 + 7822.0) / 27579.0
    mid = np.interp(g, [SMIC, 27579.0], [0.336, a60])
    return np.where(g < SMIC, lo, np.where(g < 27579.0, mid, hi))


def evalue(nom, tm, T, F, fam, lab, A0=0.0, jeu='central', eta=0.25, sorties=True):
    e = v.elast(jeu)
    n = np.zeros_like(Z)
    pt = {}
    acc = dict(modele=0.0, c0=0.0, c0_trap=0.0, tout=0.0, nc=0.0, tout_top10=0.0, nc_top10=0.0, nc_s50_486=0.0, nc_s50_25=0.0, nc_s100_486=0.0,
               ext_tout=0.0, ext_nc=0.0, dq_nc=0.0, fe_nc=0.0, fe_nc_s50=0.0)
    for tnom, w, parts, kids, cur in P.TYPES:
        imp, mgs, taxes = impot_type(tm, T, F, fam, parts, kids, lab, A0)
        n += w * imp
        pt[tnom] = (w, imp, cur)
        single = 1.0 if len(parts) == 1 else 0.0
        for k, (sh, mg) in enumerate(zip(parts, mgs)):
            t1 = np.clip(mg * R, 0, 0.95)
            t0 = TAU0
            z = sh * Z
            g = z * LAB                                     # revenu brut du travail de l'adulte
            acc['modele'] += (w * 0.5 * e * z * (t1 ** 2 / (1 - t1))).sum() / 1e9
            # trapèze, coin IR-CSG seul
            acc['c0'] += (w * e * z * (np.log((1 - t0) / (1 - t1)) - (t1 - t0))).sum() / 1e9
            acc['c0_trap'] += (w * -0.5 * (t0 + t1) * e * z * (np.log(1 - t1) - np.log(1 - t0))).sum() / 1e9
            for conv in ('tout', 'nc'):
                er, ee, pa = coin(g, single, conv)
                er, ee, pa = SALSH * er, SALSH * ee, SALSH * pa
                a0 = np.clip(1 - t0 - ee - pa, 0.03, None)
                a1 = np.clip(1 - t1 - ee - pa, 0.03, None)
                T0f, T1f = 1 - a0 / (1 + er), 1 - a1 / (1 + er)
                dq = e * z * (1 + er) * (np.log(a1) - np.log(a0))
                ps = e * z * ((1 + er) * np.log(a0 / a1) + (a1 - a0))
                acc[conv] += (w * ps).sum() / 1e9
                acc[conv + '_top10'] += (w * ps * (Q >= 0.9)).sum() / 1e9
                if conv == 'nc':
                    top = Q >= 0.9
                    for s, tk, cle in ((0.5, 0.486, 'nc_s50_486'), (0.5, 0.25, 'nc_s50_25'), (1.0, 0.486, 'nc_s100_486')):
                        acc[cle] += (w * (ps + np.where(top, s * tk, 0.0) * dq)).sum() / 1e9
                    acc['dq_nc'] += (w * dq).sum() / 1e9
                    acc['fe_nc'] += (w * T1f * dq).sum() / 1e9
                    acc['fe_nc_s50'] += (w * (T1f - np.where(top, 0.5 * 0.486, 0.0)) * dq).sum() / 1e9
            # marge extensive : PTR IR-CSG avant / après pour cet adulte
            lk = sh * lab
            if fam == 'quotient' or len(parts) == 1:
                # impôt du foyer sans le revenu d'activité de l'adulte k
                imp_wo, _, _ = impot_type_sans(tm, T, F, fam, parts, kids, lab, A0, k)
                d1 = (imp - imp_wo)
            else:
                t_with = taxes[k]
                t_wo = np.clip(sh * ZN - lk, 0, None)
                d1 = T(t_with) - T(t_wo)
            ptr1 = np.where(g > 0, d1 / np.maximum(g, 1.0), 0.0)
            rfr = v._RFR_F
            couple = len(parts) == 2
            ir_w = P.ir_actuel(rfr, couple, kids)
            ir_wo = P.ir_actuel(np.clip(rfr - 0.75 * g, 0, None), couple, kids)
            ptr0 = np.where(g > 0, (ir_w - ir_wo) / np.maximum(g, 1.0) + 0.097, 0.0)
            for conv in ('tout', 'nc'):
                if single:
                    rest = ptr_rest_single(g)
                    if conv == 'nc':
                        rest = rest - 0.1005
                else:
                    rest = 0.1131 if conv == 'tout' else 0.0126
                p0 = np.clip(ptr0 + rest, -0.5, 0.97)
                p1 = np.clip(ptr1 + rest, -0.5, 0.97)
                pse = eta * g * (np.log((1 - p0) / (1 - p1)) - (p1 - p0))
                # personnes seules de 0,5 à 2 Smic exclues : artefact des foyers représentatifs, qui mêlent
                # pensions et salaires (revue/methode_perte_seche.md, § 2, limite 5)
                borne = 0.5 * SMIC if single else 2 * SMIC
                acc['ext_' + conv] += (w * pse * (g > 1000) * (g < borne)).sum() / 1e9
    nmean = n / W
    out = dict(nom=nom, recette=(W * nmean).sum() / 1e9, **acc)
    if sorties:
        ty = v.par_type(nmean)
        out['types'] = {i: round(r.nouveau - r.actuel, 1) for i, r in ty.iterrows()}
        d = v.deciles(nmean)
        out['dec_eur'] = [int(round(u)) for u in d.delta_eur]
        out['top1_Md'] = round((W * (nmean - v.CUR) * (Q >= 0.99)).sum() / 1e9, 2)
        out['top10_Md'] = round((W * (nmean - v.CUR) * (Q >= 0.9)).sum() / 1e9, 2)
        per = P.perdants(pt)
        out['perdants500'] = round(per[500][1])
    return out


def impot_type_sans(tm, T, F, fam, parts, kids, lab, A0, k):
    """Impôt du foyer quand l'adulte k n'a plus de revenu d'activité (approx. : on retire sa part de lab)."""
    # on recalcule en remplaçant, pour l'adulte k, zn par zn - lab et lab par 0
    zs = [sh * ZN for sh in parts]
    ls = [sh * lab for sh in parts]
    zs[k] = np.clip(zs[k] - ls[k], 0, None)
    ls[k] = 0 * ls[k]
    ps = [sh * ZN * PSH for sh in parts]
    ab = [np.minimum(p, np.clip(A0 - 0.5 * np.clip(p - A0, 0, None), 0, None)) if A0 else 0.0 for p in ps]
    ab = [a + _pens(p) for a, p in zip(ab, ps)]
    tax = [np.clip(z - np.minimum(F, l) - a, 0, None) for z, l, a in zip(zs, ls, ab)]
    if fam == 'quotient':
        y = sum(tax)
        if len(parts) == 2:
            p0, p = 2.0, 2.0 + 0.5 * kids
            cap = 2 * P.PLAF * (p - p0)
        else:
            p0, p = 1.0, 1.0 + (1.0 if kids else 0.0)
            cap = P.PLAF_ISOL if kids else 0.0
        return np.maximum(p * T(y / p), p0 * T(y / p0) - cap), None, None
    if fam == 'franchise' and kids:
        haut = np.argmax(np.vstack(zs), axis=0) if len(zs) == 2 else np.zeros(len(ZN), int)
        tax = [np.where(haut == j, np.clip(t - P.FR_ENF * kids, 0, None), t) for j, t in enumerate(tax)]
    imp = sum(T(t) for t in tax)
    if fam == 'cheque':
        imp = imp - P.CHEQUE * kids
    return imp, None, None


def actuel(jeu='central', eta=0.25):
    """Système actuel : coût du modèle et niveaux de référence (pour contrôle)."""
    e = v.elast(jeu)
    return (W * 0.5 * e * Z * TAU0 ** 2 / (1 - TAU0)).sum() / 1e9


if __name__ == '__main__':
    LABN = P.LABN
    print('actuel (modèle)', round(actuel(), 2))
    res = []

    def run(nom, key, F=None, fam=None, lab=LABN, A0=0.0, top=0.50, recale=False):
        r = dict(BAR[key])
        F = r['F'] if F is None else F
        fam = r['fam'] if fam is None else fam
        if recale or top != 0.50:
            t1, (tm, T) = cale(r, F, fam, lab, A0, top)
        else:
            tm, T = ex.bareme_lineaire([0, 20e3, r['z1'], r['z2']], [r['t0'], r['tb'], r['t1'], 0.50])
            t1 = r['t1']
        o = evalue(nom, tm, T, F, fam, lab, A0)
        o['t1'] = round(t1, 4)
        res.append(o)
        print({k: (round(float(u), 2) if isinstance(u, (float, np.floating)) else u) for k, u in o.items()}, flush=True)

    run('proposition', 'franchise')
    for key in ('F0', 'F4000', 'F6000', 'F10000'):
        run(key, key)
    run('franchise salaires seuls', 'franchise', lab=LAB_SAL, recale=True)
    run('franchise tous revenus', 'franchise', lab=ZN, recale=True)
    c0 = v.CIBLE
    v.CIBLE = c0 + 1.0
    run('recette +1 Md€', 'franchise', recale=True)
    v.CIBLE = c0
    for jeu in ('bas', 'haut'):
        r = BAR['franchise']
        tm, T = ex.bareme_lineaire([0, 20e3, r['z1'], r['z2']], [r['t0'], r['tb'], r['t1'], 0.50])
        o = evalue('proposition ' + jeu, tm, T, 8000.0, 'franchise', LABN, jeu=jeu, sorties=False)
        res.append(o)
        print({k: round(u, 2) for k, u in o.items() if isinstance(u, float)}, 'actuel', round(actuel(jeu), 2))
    for key in ('rien', 'cheque', 'quotient'):
        run('famille ' + key, key)
    run('taux sup 45', 'franchise', top=0.45)
    run('taux sup 55', 'franchise', top=0.55)
    out = Path(__file__).with_suffix('.json')
    out.write_text(json.dumps(res, indent=1, ensure_ascii=False))
