"""Fusion IR-CSG-CRDS : référence et arbitrages, perte sèche généralisée (revue/methode_perte_seche.md).

Référence (consigne de l'auteur) : assiette large, impôt individuel, même barème pour tous, ni franchise ni aide
familiale dans l'impôt. Barème à taux marginal en ligne droite (0, 20 000 €, z1, z2 ; 50 % au-delà de z2), choisi
parmi une grille pour minimiser la perte sèche généralisée centrale, à recette égale (220 Md€).

Perte sèche généralisée centrale (variation par rapport à aujourd'hui) = coin total hors cotisations
contributives (cotisations non contributives et prime d'activité comprises), déplacement de la moitié de la
réaction du dixième le plus aisé vers une assiette taxée à 48,6 %, marge extensive (η = 0,25) ; voir
ps_ircsg_methode.py (fonction evalue). La perte quadratique des notes est donnée pour comparaison.

Chaque arbitrage modifie un seul paramètre ; la recette est rétablie par un même nombre de points ajouté à tous
les taux sous le taux supérieur (« points de taux pour tous »).

Lancer depuis fiscalite/ : python3 synthese/perte_seche_ircsg.py  ->  synthese/sorties/perte_seche_ircsg.txt/.json
"""
import itertools
import json
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE)]
import ps_ircsg_methode as ps  # noqa: E402

P, v, ex = ps.P, ps.v, ps.ex
OUT = HERE / "sorties"
OUT.mkdir(exist_ok=True)
LABN, LAB_SAL, ZN = P.LABN, ps.LAB_SAL, ps.ZN
QUAD0 = ps.actuel()


def bareme(b, d=0.0, top=0.50):
    t0, tb, z1, t1, z2 = b
    return ex.bareme_lineaire([0, 20e3, z1, z2], [t0 + d, tb + d, t1 + d, top])


def central(o):
    return o["nc_s50_486"] + o["ext_nc"]


def evalue(nom, b, F, fam, lab, d=0.0, top=0.50, jeu="central", sorties=True):
    tm, T = bareme(b, d, top)
    return ps.evalue(nom, tm, T, F, fam, lab, jeu=jeu, sorties=sorties)


def cale_t1(t0, tb, z1, z2, F, fam, lab):
    lo, hi = 0.0, 0.50
    for _ in range(32):
        t1 = (lo + hi) / 2
        lo, hi = (t1, hi) if ps.recette(*bareme((t0, tb, z1, t1, z2)), F, fam, lab, 0.0) < v.CIBLE else (lo, t1)
    return (lo + hi) / 2


def cale_d(b, F, fam, lab, top=0.50):
    lo, hi = -0.15, 0.30
    for _ in range(32):
        d = (lo + hi) / 2
        lo, hi = (d, hi) if ps.recette(*bareme(b, d, top), F, fam, lab, 0.0) < v.CIBLE else (lo, d)
    return (lo + hi) / 2


def reference(G):
    best = None
    for t0, tb, z1, z2 in itertools.product(*G.values()):
        if tb < t0 or z1 >= z2:
            continue
        t1 = cale_t1(t0, tb, z1, z2, 0.0, "rien", LABN)
        if not tb <= t1 < 0.50 - 1e-3:
            continue
        b = (t0, tb, z1, t1, z2)
        c = central(evalue("grille", b, 0.0, "rien", LABN, sorties=False))
        if best is None or c < best[0]:
            best = (c, b)
    return best[1]


def ligne(o, d, quad0):
    return (f"décalage {100*d:+.2f} pt ; perte sèche, variation : centrale {central(o):+.1f} Md€ (coin IR-CSG seul"
            f" {o['c0']:+.1f} ; coin non contributif {o['nc']:+.1f} ; toutes cotisations {o['tout']:+.1f} ; déplacement"
            f" s=0,5 {o['nc_s50_486'] - o['nc']:+.1f} ; marge extensive {o['ext_nc']:+.1f}) ; quadratique des notes"
            f" {o['modele'] - quad0:+.1f} ; perdants > 500 € {o.get('perdants500', float('nan')):.0f} %")


if __name__ == "__main__":
    L = []

    def p(s):
        print(s, flush=True)
        L.append(s)
    p(f"[AUJ] perte sèche quadratique d'aujourd'hui (modèle des notes) : {QUAD0:.1f} Md€")
    G = dict(t0=[0.06, 0.09, 0.12, 0.15, 0.18], tb=[0.12, 0.15, 0.18, 0.21, 0.24],
             z1=[30e3, 45e3, 60e3, 90e3], z2=[250e3, 400e3, 600e3])
    b = reference(G)
    p(f"[REF] barème de référence : {100*b[0]:.0f} % au premier euro, {100*b[1]:.0f} % à 20 k€, {100*b[3]:.1f} % à "
      f"{b[2]/1e3:.0f} k€, 50 % à {b[4]/1e3:.0f} k€")
    res = []

    def run(nom, F=0.0, fam="rien", lab=LABN, extra=None, top=0.50, recale=True):
        ps.EXTRA.update(dict(Fp=0.0, Fp_degressif=False, abat_pens=0.0))
        if extra:
            ps.EXTRA.update(extra)
        d = cale_d(b, F, fam, lab, top) if recale else 0.0
        o = evalue(nom, b, F, fam, lab, d, top)
        lo = evalue(nom, b, F, fam, lab, d, top, jeu="bas", sorties=False)
        hi = evalue(nom, b, F, fam, lab, d, top, jeu="haut", sorties=False)
        p(f"[{nom}] " + ligne(o, d, QUAD0) + f" ; fourchette élasticités {central(lo):+.1f} à {central(hi):+.1f}")
        p(f"    déciles € " + " ".join(f"{u:+d}" for u in o["dec_eur"]) + f" ; 10 % du haut {o['top10_Md']:+.1f} Md€,"
          f" 1 % du haut {o['top1_Md']:+.1f} Md€")
        p(f"    types Md€ " + " ; ".join(f"{k} {u:+.1f}" for k, u in o["types"].items()))
        o.update(d=d, lo=central(lo), hi=central(hi), cen=central(o))
        res.append({k: (float(u) if isinstance(u, (np.floating, float)) else u) for k, u in o.items()})
        return o

    run("Référence : assiette large, même barème pour tous", recale=False)
    run("Franchise d'activité 4 000 €", F=4000.0)
    run("Franchise d'activité 8 000 €", F=8000.0)
    run("Franchise de 8 000 € sur les seuls salaires", F=8000.0, lab=LAB_SAL)
    run("Franchise de 8 000 € sur tous les revenus", F=8000.0, lab=ZN)
    # petites pensions : non chiffrable avec des foyers représentatifs qui mêlent pensions et salaires
    run("Abattement de 10 % sur les pensions", extra=dict(abat_pens=0.10))
    run("Famille : franchise de 6 000 € par enfant", fam="franchise")
    run("Famille : chèque par enfant", fam="cheque")
    run("Imposition commune : quotient conjugal et familial", fam="quotient")
    run("Taux supérieur 45 %", top=0.45)
    run("Taux supérieur 55 %", top=0.55)
    run("Ancienne proposition : franchise d'activité 8 000 € + 6 000 € par enfant", F=8000.0, fam="franchise")
    (OUT / "perte_seche_ircsg.txt").write_text("\n".join(L) + "\n", encoding="utf-8")
    (OUT / "perte_seche_ircsg.json").write_text(json.dumps(dict(ref=list(b), res=res), default=float, indent=1,
                                                           ensure_ascii=False))
