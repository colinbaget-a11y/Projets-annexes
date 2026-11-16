"""Réforme naïve de la partie IR-CSG : harmoniser brutalement assiettes et règles en gardant les barèmes.

Version retenue dans le corps (« la plus spontanée ») : on garde l'impôt sur le revenu tel qu'il est (foyer fiscal,
quotient conjugal et familial avec les plafonds actuels, barème des revenus 2024) et la CSG-CRDS comme un taux
proportionnel ; on harmonise seulement l'assiette et les règles : même revenu après cotisations pour tous les
revenus (salaires, pensions, revenus des indépendants, loyers, chômage), ni abattement, ni décote, ni niche, ni taux
réduit de CSG. Le taux proportionnel qui remplace la CSG et la CRDS est calé sur la recette (220,1 Md€).
Version en annexe : le barème de l'IR appliqué à chaque adulte (impôt individuel, comme la CSG), plus un taux
proportionnel (étape 1 de etapes_ircsg.py).

Lancer depuis fiscalite/ : python3 synthese/naive_ircsg.py -> sorties/naive_ircsg.txt et .json
"""
import outils_ircsg as U

M = U.M
L, D = [], {}


def p(s=""):
    print(s, flush=True)
    L.append(s)


def cale_tau(o):
    lo, hi = -0.10, 0.20
    for _ in range(45):
        t = (lo + hi) / 2
        lo, hi = (t, hi) if U.recette(U.empile(t), o) < M.CIBLE else (lo, t)
    return (lo + hi) / 2


for cle, nom, o in (("quotient", "Réforme naïve : IR du foyer (quotient conjugal et familial) + taux proportionnel",
                     U.options(fam="quotient")),
                    ("individuel", "Réforme naïve, variante : barème de l'IR par adulte + taux proportionnel", U.options())):
    r_ir = U.recette(U.empile(0.0), o)
    tau = cale_tau(o)
    s = U.empile(tau)
    r = U.evalue_complet(nom, s, o)
    r.update(tau=tau, recette_bareme_ir=r_ir)
    mg = {}
    for prof, niv in (("seul", (U.SMIC / 2, U.SMIC, 30e3, 50e3, 80e3, 120e3)),
                      ("retraite_seul", (12e3, 16e3, 18e3, 20e3, 25e3, 30e3, 50e3)),
                      ("couple_2enf", (30e3, 50e3, 80e3, 120e3))):
        mg[prof] = {f"{b:.0f}": dict(auj=U.marginal_cas(None, None, prof, round(b / 500) * 500),
                                     naif=U.marginal_cas(s, o, prof, round(b / 500) * 500)) for b in niv}
    r["marginaux"] = mg
    D[cle] = r
    p(f"[{cle}] barème de l'IR seul sur l'assiette large : {r_ir:.1f} Md€ ; taux proportionnel {100 * tau:.2f} %")
    p(U.ligne_resume(r))
    for prof, u in mg.items():
        p(f"    taux marginal {prof} : " + " ; ".join(f"{float(b) / 1e3:.1f} k€ {v['auj']:.0f} → {v['naif']:.0f} %" for b, v in u.items()))
    dd = r["distribution"]
    p(f"    hausses : tous P90 {dd['tous']['p90']:+,.0f} € ; retraités P90 {dd['retraites']['p90']:+,.0f} € ;"
      f" perdants > 500 € {dd['tous']['perd500_M']:.1f} M (dont retraités {dd['retraites']['perd500_M']:.1f} M)\n")
U.ecrire("naive_ircsg", L, D)
