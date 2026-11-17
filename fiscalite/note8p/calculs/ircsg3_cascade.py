"""Bloc IR-CSG v3 : décomposition séquentielle « où vont les recettes » (graphique F).

Ordre retenu (chaque étape s'ajoute aux précédentes ; statique, avant réaction ; Md€ de 2025, + = recette en plus) :
 0. charge observée du périmètre : IR des revenus du barème (net des réductions et crédits : IRCOM « impôt net »), CSG,
    CRDS (229,9 Md€) ;
 1. niches non simulées : réductions et crédits d'impôt, exonérations (heures supplémentaires, épargne salariale…),
    demi-parts spéciales, frais réels au-delà du forfait : écart entre le droit 2025 simulé sans niche (ircsg3_droit)
    et la charge observée, point par point ; comparé aux Voies et moyens (PLF 2026, t. II) ;
 2. fin de l'abattement de 10 % sur les pensions ;
 3. fin de l'abattement des personnes âgées (art. 157 bis) ;
 4. alignement de la CSG des pensions (9,2 % + CRDS 0,5 % sur toute pension, 6,8 points déductibles) ;
 5. individualisation (fin du quotient conjugal ; les enfants restent au quotient familial du parent qui gagne le plus) ;
 6. fin du quotient familial (et de la demi-part des parents isolés) ;
 7. fin de la déductibilité partielle de la CSG ;
 8. frais professionnels : fin du forfait de 10 %, frais réels déductibles ;
 coûts : 9. CEHR des revenus du barème absorbée ; 10. avantages maintenus (invalidité, dépendance) ;
 11. franchise par enfant (sur le système de l'étape 8) ; 12. passage au nouveau barème (taux) ; = variation nette.
L'épargne retraite déductible est gardée à chaque étape (même déduction avant et après : elle ne crée ni recette ni coût).
"""
import numpy as np
import pandas as pd

import ircsg3_modele as N
import ircsg3_droit as DR

M, R = N.M, N.R
ETAPES = [("niches", "Réductions, crédits, exonérations et autres niches", {}),
          ("abatpen", "Abattement de 10 % sur les pensions", dict(abatpen=False)),
          ("age", "Abattement des personnes âgées", dict(age=False)),
          ("csg_ret", "Alignement de la CSG des retraités", dict(csg_reduit=False)),
          ("conjugal", "Fin du quotient conjugal", dict(conjugal=False)),
          ("qf", "Fin du quotient familial", dict(qf=False)),
          ("csg_ded", "Fin de la CSG déductible", dict(csg_ded=False)),
          ("forfait", "Forfait de 10 % (frais réels gardés)", dict(forfait=False))]


def _foyer(g, parts, fl, fe=0.0, kids=0):
    zn = M.ZNG[g]
    if g == "A":
        ad = [("A", sh * zn, M.R_A) for sh in parts]
        fr = [sh * N.FR for sh in parts]
        per = [sh * N.DED_PER0 for sh in parts]       # épargne retraite déductible, avant et après
    else:
        ad = [("R", sh * zn, 1.0) for sh in parts]
        fr = [0 * zn for _ in parts]
        per = None
    if fe and kids:
        zs = np.vstack([a[1] for a in ad])
        haut = np.argmax(zs, axis=0) if len(ad) == 2 else np.zeros(zs.shape[1], int)
        fr = [f + np.where(haut == k, fe * kids, 0.0) for k, f in enumerate(fr)]
    return ad, fr, per


def charges(fl, fe=0.0):
    """Charge simulée de chaque type (dict nom -> tableau)."""
    out = {}
    for nom, g, fam, w, parts, kids in M.TYPES:
        ad, fr, per = _foyer(g, parts, fl, fe, kids)
        isole = nom.startswith("parent_isole")
        out[nom] = DR.charge(ad, kids, isole, fl, frais_reels=fr, deduc=per)["total"]
    return out


def resume(delta):
    """delta : dict nom -> variation par foyer (€). Md€ total, actifs, retraités, par décile, 1 % du haut."""
    tot = sum(w * delta[n] for n, g, f, w, p, k in M.TYPES)
    act = sum((w * delta[n]).sum() for n, g, f, w, p, k in M.TYPES if g == "A") / 1e9
    ret = sum((w * delta[n]).sum() for n, g, f, w, p, k in M.TYPES if g == "R") / 1e9
    dec = pd.Series(tot).groupby(M.DEC).sum() / 1e9
    return dict(Md=float(tot.sum() / 1e9), actifs=act, retraites=ret, deciles_Md=[float(v) for v in dec.values],
                top1_Md=float((tot * (M.Q >= 0.99)).sum() / 1e9),
                couples_enfants=sum((w * delta[n]).sum() for n, g, f, w, p, k in M.TYPES if f == "couples2") / 1e9,
                couples_un_revenu=sum((w * delta[n]).sum() for n, g, f, w, p, k in M.TYPES
                                      if g == "A" and n.endswith("_1.0")) / 1e9)


def cascade(sched, o, fe=None):
    fe = N.FE_DEFAUT if fe is None else fe
    obs = {n: M.CURT[n] for n, *_ in M.TYPES}
    fl = {}
    prev = charges(fl)
    res = [("observe", "Charge observée", dict(Md=float(sum((w * obs[n]).sum() for n, g, f, w, p, k in M.TYPES) / 1e9)))]
    res.append(("niches", ETAPES[0][1], resume({n: prev[n] - obs[n] for n in prev})))
    for cle, lib, f_ in ETAPES[1:]:
        fl = dict(fl, **f_)
        cur = charges(fl)
        res.append((cle, lib, resume({n: cur[n] - prev[n] for n in cur})))
        prev = cur
    sys8 = prev
    # coûts
    res.append(("cehr", "CEHR des revenus du barème absorbée", dict(Md=-R.CEHR_BAR)))
    res.append(("invalidite", "Avantages invalidité-dépendance gardés", dict(Md=-sum(R.GARDES.values()))))
    cur = charges(fl, fe=fe)
    res.append(("franchise", f"Franchise de {fe:,.0f} € par enfant".replace(",", " "),
                resume({n: cur[n] - prev[n] for n in cur})))
    # passage au nouveau barème
    nv = {}
    for nom, g, fam, w, parts, kids in M.TYPES:
        nv[nom] = R.impot_adultes(*sched, o, *M.adultes(g, parts, o), kids)[0]
    r = resume({n: nv[n] - cur[n] for n in nv})
    r["Md"] -= 0.0
    res.append(("bareme", "Passage au nouveau barème", r))
    tot = resume({n: nv[n] - obs[n] for n in nv})
    res.append(("net", "Variation nette (hors CEHR et invalidité)", tot))
    return res, sys8


def tableau(res):
    rows = []
    for cle, lib, d in res:
        rows.append(dict(etape=cle, libelle=lib, Md=d["Md"], actifs=d.get("actifs"), retraites=d.get("retraites"),
                         top1=d.get("top1_Md"), d10=(d.get("deciles_Md") or [None] * 10)[-1],
                         d1_5=sum((d.get("deciles_Md") or [0] * 10)[:5]) if d.get("deciles_Md") else None))
    return pd.DataFrame(rows)


if __name__ == "__main__":
    o = N.options()
    old = R.bareme([0, 12000, 36500, 120000], [0.05, 0.20, 0.28, 0.45])
    res, _ = cascade(old, o)
    pd.set_option("display.width", 200)
    print(tableau(res).round(2).to_string())
