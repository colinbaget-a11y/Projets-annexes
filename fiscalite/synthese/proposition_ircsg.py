"""Proposition de fusion IR-CSG-CRDS conforme à synthese/DECISIONS.md (16/11/2026).

Règles fixées d'avance (décisions de l'auteur) :
- impôt individuel sur le revenu après cotisations, sans niche ni taux réduit ; pensions taxées comme les salaires
  (fin de l'abattement de 10 % et des taux réduits de CSG), pensions exonérées jusqu'à 12 500 € par retraité puis de
  moins en moins jusqu'à 25 000 € ; franchise de 6 000 € par enfant, déduite du revenu du parent qui gagne le plus ;
  versements d'épargne retraite toujours déductibles (modele_purs.DED_PER, répartition supposée) ;
- recette inchangée (220,1 Md€ avant réaction) ; aucun décile ne voit sa charge moyenne bouger de plus de 500 € ;
  charge du 1 % le plus aisé inchangée (|Δ| < 0,05 Md€ : le seuil z2 du taux de 50 % est calé pour cela) ;
- aucune prime d'activité ajoutée ni modifiée.
Paramètres cherchés : franchise d'activité F (0 à 8 000 € par adulte) et taux d'entrée t0 (taux au premier euro
imposé, après la franchise), puis la forme du barème (tb à 20 000 €, z1, t1 calé sur la recette, z2 calé sur le 1 %).

Règle de choix (DECISIONS.md, point 4) : parmi tous les barèmes qui respectent les contraintes, celui qui encourage le
plus la reprise d'emploi, mesurée par le gain sur la marge extensive (participation, jeu central) ; à 0,02 Md€ près,
le plus efficace au total. On vérifie qu'il minimise aussi le taux de prélèvement sur un premier salaire à mi-temps
et au Smic (cas-types). Pour chaque couple (F, t0), on garde aussi le barème le plus efficace, pour montrer
l'arbitrage entre franchise et taux d'entrée.

Lancer depuis fiscalite/ : python3 synthese/proposition_ircsg.py (environ 5 minutes sur 4 cœurs)
Sorties : sorties/proposition_ircsg.txt et .json
"""
import itertools
import json
from multiprocessing import Pool

import numpy as np

import outils_ircsg as U

M = U.M
BASE = dict(fam="franchise", Fp=12500.0, Fp_degressif=True, per=True)
FS = (0.0, 2000.0, 4000.0, 6000.0, 7000.0, 8000.0)
T0S = tuple(np.round(np.arange(0.0, 0.165, 0.01), 2))
TBS = tuple(np.round(np.arange(0.08, 0.265, 0.01), 2))
Z1S = (25e3, 30e3, 37.5e3, 45e3, 60e3, 90e3)
TOL_PART = 0.02
L = []


def p(s=""):
    print(s, flush=True)
    L.append(s)


def essai(args):
    F, t0, tb, z1 = args
    o = U.options(F=F, **BASE)
    c = U.cale_top1(t0, tb, z1, o)
    if c is None:
        return None
    z2, t1, d1 = c
    if t1 < tb:
        return None
    s = U.bareme(t0, tb, z1, t1, z2)
    r = M.evalue("p", *s, o, sorties=True)
    return dict(F=F, t0=t0, tb=tb, z1=z1, t1=float(t1), z2=float(z2), top1=float(r["top1_Md"]), gain=-r["v2"],
                part=-r["v2_ext"], intensif=-r["v2_reel"], dec_max=max(abs(u) for u in r["dec_eur"]),
                retraites=r["groupes"]["retraites"]["Md"], perdants=r["perdants500"])


def bar(r):
    return (r["t0"], r["tb"], r["z1"], r["t1"], r["z2"])


if __name__ == "__main__":
    combos = [c for c in itertools.product(FS, T0S, TBS, Z1S) if c[2] >= c[1]]
    with Pool(4) as pool:
        tous = [r for r in pool.map(essai, combos, chunksize=20) if r is not None]
    ok = [r for r in tous if r["dec_max"] <= 500]
    p(f"{len(combos)} barèmes essayés ; {len(tous)} tiennent la recette et la neutralité du 1 % ; {len(ok)} respectent"
      " aussi la contrainte des déciles (±500 €)")
    # meilleur barème (gain total) pour chaque couple (F, t0)
    par_design = {}
    for r in ok:
        k = (r["F"], r["t0"])
        if k not in par_design or r["gain"] > par_design[k]["gain"]:
            par_design[k] = r
    p("\n[ARBITRAGE franchise / taux d'entrée] meilleur barème (gain total) pour chaque franchise F et taux d'entrée t0 :")
    for (F, t0), r in sorted(par_design.items()):
        o = U.options(F=F, **BASE)
        pt = U.ptrs(U.bareme(*bar(r)), o)
        r.update(ptr_mi=pt["seul_mi"], ptr_smic=pt["seul_smic"], ptr_conj_smic=pt["conjoint_smic"])
        p(f"  F {F:5.0f} t0 {100*t0:4.1f} % | gain {r['gain']:.2f} dont participation {r['part']:.2f} | retraités"
          f" {r['retraites']:+.1f} Md€ | premier salaire mi-temps {pt['seul_mi']:.1f} %, Smic {pt['seul_smic']:.1f} % | {U.fb(bar(r))}")
    # règle de choix : participation maximale, puis gain total
    pmax = max(r["part"] for r in ok)
    cands = [r for r in ok if r["part"] >= pmax - TOL_PART]
    choix = max(cands, key=lambda r: r["gain"])
    best_gain = max(ok, key=lambda r: r["gain"])
    p(f"\n[CHOIX] participation maximale {pmax:.2f} Md€ ; {len(cands)} barèmes à 0,02 près ; retenu : F {choix['F']:.0f} €,"
      f" {U.fb(bar(choix))} ; gain {choix['gain']:.2f}")
    p(f"[POUR MÉMOIRE] barème le plus efficace sous les mêmes contraintes : F {best_gain['F']:.0f} €, {U.fb(bar(best_gain))} ;"
      f" gain {best_gain['gain']:.2f} dont participation {best_gain['part']:.2f}")
    # franchise par franchise : barème qui maximise la participation (variante prudente : F = 4 000 €)
    par_F = {}
    for F in FS:
        cF = [r for r in ok if r["F"] == F]
        if cF:
            pm = max(r["part"] for r in cF)
            par_F[F] = max([r for r in cF if r["part"] >= pm - TOL_PART], key=lambda r: r["gain"])
    p("\n[PAR FRANCHISE] barème qui maximise la participation à franchise donnée :")
    for F, r in par_F.items():
        p(f"  F {F:5.0f} : participation {r['part']:.2f} ; gain {r['gain']:.2f} ; retraités {r['retraites']:+.1f} Md€ ; {U.fb(bar(r))}")
    # évaluations complètes
    J = json.loads((U.OUT / "architectures_ircsg.json").read_text(encoding="utf-8"))
    o_c = U.options(F=choix["F"], **BASE)
    s_c = U.bareme(*bar(choix))
    res = {}
    res["proposition"] = U.evalue_complet("Proposition", s_c, o_c)
    res["meilleur_gain"] = U.evalue_complet("Barème le plus efficace sous les mêmes contraintes",
                                            U.bareme(*bar(best_gain)), U.options(F=best_gain["F"], **BASE))
    if 4000.0 in par_F and choix["F"] != 4000.0:
        r4 = par_F[4000.0]
        res["franchise_4000"] = U.evalue_complet("Variante : franchise de 4 000 €", U.bareme(*bar(r4)),
                                                 U.options(F=4000.0, **BASE))
    if 0.0 in par_F:
        r0 = par_F[0.0]
        res["sans_franchise"] = U.evalue_complet("Variante : taux d'entrée bas, sans franchise", U.bareme(*bar(r0)),
                                                 U.options(F=0.0, **BASE))
    P4 = J["propositions"]["4000"]
    res["ancienne"] = U.evalue_complet("Ancienne proposition (1 % en baisse, sans déduction de l'épargne retraite)",
                                       U.bareme(*P4["bareme"]), P4["options"])
    res["neutre"] = U.evalue_complet("Barème neutre (architectures_ircsg.py)", U.bareme(*J["neutre"]), U.options())
    for k, r in res.items():
        p("\n" + U.ligne_resume(r))
    # coût de la déduction de l'épargne retraite et marges de calage
    o_sans = dict(o_c, per=False)
    cout_per = U.recette(s_c, o_sans) - U.recette(s_c, o_c)
    d_per = U.cale_d(lambda d: U.bareme(choix["t0"] + d, choix["tb"] + d, choix["z1"], choix["t1"] + d, choix["z2"]), o_sans)
    p(f"\n[ÉPARGNE RETRAITE] garder la déduction des versements coûte {cout_per:.2f} Md€ au barème retenu, soit"
      f" {-100 * d_per:.2f} point de taux pour tous (sous le taux de 50 %)")
    # taux marginaux de la proposition (cas-types)
    mg = {}
    for prof, niv in (("seul", (U.SMIC / 2, U.SMIC, 30e3, 50e3, 80e3, 120e3, 200e3, 300e3)),
                      ("retraite_seul", (12e3, 15e3, 18e3, 20e3, 24e3, 30e3, 50e3))):
        mg[prof] = {f"{b:.0f}": dict(auj=U.marginal_cas(None, None, prof, round(b / 500) * 500),
                                     prop=U.marginal_cas(s_c, o_c, prof, round(b / 500) * 500)) for b in niv}
        p(f"[TAUX MARGINAL {prof}] " + " ; ".join(f"{float(b) / 1e3:.1f} k€ : {u['auj']:.0f} → {u['prop']:.0f} %"
                                                  for b, u in mg[prof].items()))
    # taux marginal du barème sur le revenu imposé, aux revenus repères
    tm, T = s_c
    reperes = {f"{z:.0f}": float(100 * tm(z)) for z in (0, 10e3, 20e3, 30e3, 45e3, 60e3, 100e3, 150e3, 250e3)}
    p("[BARÈME] taux marginal sur le revenu imposé (après franchise) : "
      + " ; ".join(f"{float(z) / 1e3:.0f} k€ {t:.1f} %" for z, t in reperes.items()))
    out = dict(choix=choix, meilleur_gain=best_gain, par_design=[dict(r) for r in par_design.values()],
               par_franchise={str(int(F)): r for F, r in par_F.items()}, evaluations=res, cout_per=cout_per,
               points_per=-d_per, marginaux=mg, bareme_reperes=reperes, base=BASE, n_essais=len(combos), n_ok=len(ok),
               admissibles=ok)
    U.ecrire("proposition_ircsg", L, out)
