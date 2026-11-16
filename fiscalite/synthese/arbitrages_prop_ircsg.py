"""Les vrais arbitrages politiques de la fusion IR-CSG-CRDS, chiffrés autour de la proposition (proposition_ircsg.py).

Chaque arbitrage change un paramètre de la proposition. Sauf mention contraire, la recette est rétablie par un même
nombre de points ajouté à tous les taux sous le taux supérieur de 50 % (« points pour tous ») : c'est le coût du
dispositif et son financement. On donne le gain d'efficacité (jeux bas, central, haut, long terme), la participation,
la charge des retraités, les déciles, le 1 % le plus aisé, la distribution des hausses (centiles 90 et 99, foyers qui
perdent plus de 1 000 €) et les cas-types OpenFisca.

1. Le couple : imposition commune (quotient conjugal et familial, plafonds actuels) au lieu de l'impôt individuel.
   C'est la solution de repli si le Conseil constitutionnel censure l'impôt individuel (décision 2012-662 DC).
2. Les pensions : abattement de 5 % ou de 10 % en plus de l'exonération des petites pensions.
3. Les enfants : franchise de 6 000 € par enfant (proposition), chèque de même coût, chèque égal au coût actuel du
   quotient familial (742 € par enfant).
4. La franchise d'activité : 8 000 € (proposition) contre 4 000 € ou 0 € (avec le barème qui maximise la
   participation à franchise donnée, repris de proposition_ircsg.py).
5. Le haut du barème : aller vers l'optimum d'efficacité en relâchant les contraintes de répartition (1 % libre de
   baisser ; déciles à ±1 000 €) ; nouvelle recherche du barème à franchise et taux d'entrée inchangés.

Lancer depuis fiscalite/, après proposition_ircsg.py : python3 synthese/arbitrages_prop_ircsg.py
Sorties : sorties/arbitrages_prop_ircsg.txt et .json
"""
import itertools
import json
from multiprocessing import Pool

import numpy as np

import outils_ircsg as U

M = U.M
PJ = json.loads((U.OUT / "proposition_ircsg.json").read_text(encoding="utf-8"))
C = PJ["choix"]
B0 = (C["t0"], C["tb"], C["z1"], C["t1"], C["z2"])
O0 = U.options(F=C["F"], **PJ["base"])
L, D = [], {}


def p(s=""):
    print(s, flush=True)
    L.append(s)


def sched_d(b, d):
    t0, tb, z1, t1, z2 = b
    return U.bareme(t0 + d, tb + d, z1, t1 + d, z2)


def _essai_c(args):
    o, t0, tb, z1 = args
    c = U.cale_top1(t0, tb, z1, o)
    if c is None:
        return None
    z2, t1, _ = c
    if t1 < tb:
        return None
    rr = M.evalue("c", *U.bareme(t0, tb, z1, t1, z2), o, sorties=True)
    if max(abs(u) for u in rr["dec_eur"]) > 500:
        return None
    return dict(b=(t0, tb, z1, float(t1), float(z2)), part=-rr["v2_ext"], gain=-rr["v2"])


def recherche(o):
    """Barème recherché sous les mêmes contraintes que la proposition (recette, déciles ±500 €, 1 % inchangé), à
    franchise d'activité inchangée, avec la même règle de choix (participation maximale, puis gain total)."""
    grille = [(o, t0, tb, z1) for t0 in (0.10, 0.12, 0.14, 0.16) for tb in np.round(np.arange(0.10, 0.265, 0.01), 2)
              for z1 in (25e3, 30e3, 37.5e3, 45e3, 60e3) if tb >= t0]
    with Pool(4) as pool:
        ok = [r for r in pool.map(_essai_c, grille, chunksize=10) if r is not None]
    if not ok:
        return None
    pm = max(r["part"] for r in ok)
    return max([r for r in ok if r["part"] >= pm - 0.02], key=lambda r: r["gain"])["b"]


def variante(cle, nom, o, b=B0, contraint=False):
    d = U.cale_d(lambda dd: sched_d(b, dd), o)
    r = U.evalue_complet(nom, sched_d(b, d), o)
    r["points"] = 100 * d
    D[cle] = r
    dd = r["distribution"]
    p(U.ligne_resume(r))
    p(f"    points pour tous {100 * d:+.2f} ; hausses : retraités P90 {dd['retraites']['p90']:+,.0f} €, P99"
      f" {dd['retraites']['p99']:+,.0f} € ; tous P99 {dd['tous']['p99']:+,.0f} € ; plus de 1 000 € de hausse"
      f" {dd['tous']['perd1000_M']:.1f} M de foyers\n")
    if contraint:
        bc = recherche(o)
        if bc is None:
            p(f"[{cle} sous contraintes] aucun barème ne respecte les contraintes\n")
            D[cle + "_c"] = None
        else:
            rc = U.evalue_complet(nom + ", barème recherché sous les mêmes contraintes", U.bareme(*bc), o)
            rc["bareme"] = list(bc)
            D[cle + "_c"] = rc
            p(f"[{cle} sous contraintes] {U.fb(bc)}")
            p(U.ligne_resume(rc) + "\n")
    return r


if __name__ == "__main__":
    variante("proposition", "Proposition", O0)
    # 1. le couple
    variante("quotient", "Imposition commune : quotient conjugal et familial (plafonds actuels)", dict(O0, fam="quotient"),
             contraint=True)
    # 2. les pensions
    variante("abat5", "Abattement de 5 % sur les pensions", dict(O0, abat_pens=0.05), contraint=True)
    variante("abat10", "Abattement de 10 % sur les pensions", dict(O0, abat_pens=0.10), contraint=True)
    variante("sortie_etalee", "Sortie de l'exonération des petites pensions étalée jusqu'à 37 500 €", dict(O0, Fp_pente=0.5),
             contraint=True)
    # 3. les enfants : chèque de même coût que la franchise par enfant, chèque égal au coût du quotient familial
    r_rien = U.recette(U.bareme(*B0), dict(O0, fam="rien"))
    r_fr = U.recette(U.bareme(*B0), O0)
    enfants = sum((w * kids).sum() for _, _, _, w, _, kids in M.TYPES)
    cheque_egal = (r_rien - r_fr) * 1e9 / enfants
    D["cout_franchise_enfants"] = r_rien - r_fr
    p(f"[ENFANTS] la franchise de 6 000 € par enfant coûte {r_rien - r_fr:.2f} Md€ au barème de la proposition ; chèque de"
      f" même coût : {cheque_egal:,.0f} € par enfant ({enfants / 1e6:.1f} M d'enfants) ; coût actuel du quotient familial"
      f" {M.QF_COUT:.2f} Md€, soit {M.CHEQUE:,.0f} € par enfant")
    ancien = M.CHEQUE
    M.CHEQUE = cheque_egal
    r = variante("cheque_egal", f"Chèque de {cheque_egal:,.0f} € par enfant (même coût que la franchise)", dict(O0, fam="cheque"),
                 contraint=True)
    r["cheque"] = cheque_egal
    M.CHEQUE = ancien
    r = variante("cheque_qf", f"Chèque de {ancien:,.0f} € par enfant (coût actuel du quotient familial)", dict(O0, fam="cheque"))
    r["cheque"] = ancien
    variante("sans_enfant", "Aucune aide aux enfants dans l'impôt", dict(O0, fam="rien"))
    # 4. la franchise d'activité
    for F, rr in PJ["par_franchise"].items():
        if float(F) == C["F"]:
            continue
        o = dict(O0, F=float(F))
        b = (rr["t0"], rr["tb"], rr["z1"], rr["t1"], rr["z2"])
        r = U.evalue_complet(f"Franchise d'activité de {float(F):,.0f} € (barème qui maximise la participation)",
                             U.bareme(*b), o)
        r["bareme"] = list(b)
        D[f"franchise_{F}"] = r
        p(U.ligne_resume(r) + "\n")
    # 5. le haut du barème : nouvelle recherche, franchise et taux d'entrée inchangés
    def essai(args):
        tb, z1, z2 = args
        t1 = U.cale_t1(C["t0"], tb, z1, z2, O0)
        if t1 is None or t1 < tb:
            return None
        s = U.bareme(C["t0"], tb, z1, t1, z2)
        rr = M.evalue("h", *s, O0, sorties=True)
        return dict(tb=tb, z1=z1, z2=z2, t1=float(t1), gain=-rr["v2"], dec_max=max(abs(u) for u in rr["dec_eur"]),
                    top1=rr["top1_Md"], top10=rr["top10_Md"])
    grille = list(itertools.product(np.round(np.arange(0.08, 0.265, 0.01), 2), (25e3, 30e3, 37.5e3, 45e3, 60e3, 90e3),
                                    (150e3, 200e3, 250e3, 300e3, 400e3, 600e3, 1e6, 1.5e6, 2e6, 3e6)))
    with Pool(4) as pool:
        tous = [r for r in pool.map(essai, grille, chunksize=20) if r is not None]
    for cle, nom, f in (("haut_baisse", "Le 1 % peut baisser (déciles ±500 €)", lambda r: r["dec_max"] <= 500 and r["top1"] <= 0.05),
                        ("deciles_1000", "Déciles à ±1 000 €, 1 % neutre", lambda r: r["dec_max"] <= 1000 and abs(r["top1"]) <= 0.3),
                        ("libre_1000", "Déciles à ±1 000 €, 1 % libre de baisser", lambda r: r["dec_max"] <= 1000 and r["top1"] <= 0.05)):
        ok = [r for r in tous if f(r)]
        if not ok:
            p(f"[{cle}] aucun barème")
            continue
        bst = max(ok, key=lambda r: r["gain"])
        b = (C["t0"], bst["tb"], bst["z1"], bst["t1"], bst["z2"])
        r = U.evalue_complet(nom, U.bareme(*b), O0)
        r["bareme"] = list(b)
        D[cle] = r
        p(f"[{cle}] {U.fb(b)}")
        p(U.ligne_resume(r) + "\n")
    A = json.loads((U.OUT / "architectures_ircsg.json").read_text(encoding="utf-8"))["atteignable"]
    D["atteignable"] = {k: A[k] for k in ("v2_bas", "v2_central", "v2_haut", "top1_Md", "top10_Md", "dec_eur", "perdants500")}
    p(f"[ATTEIGNABLE] optimum d'efficacité (architectures_ircsg.py, sans déduction d'épargne retraite) : gain"
      f" {-A['v2_central']:.1f} Md€ ; 10 % du haut {A['top10_Md']:+.1f} Md€ ; 1 % {A['top1_Md']:+.1f} Md€")
    U.ecrire("arbitrages_prop_ircsg", L, D)
