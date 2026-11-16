"""Fusion IR-CSG-CRDS, méthode v2 (revue/methode_v2.md) : architectures simples comparées à l'existant.

Principe : l'optimiseur ne choisit pas la réforme. On construit d'abord le barème « neutre », celui qui, à recette
égale et pour la même assiette large et le même barème pour tous, s'écarte le moins de ce que chaque foyer paie
aujourd'hui (écart absolu moyen par foyer). On lui ajoute un à un des dispositifs conventionnels (franchise
d'activité, traitement des enfants, des pensions), la recette étant rétablie par un même nombre de points ajouté
aux taux sous le taux supérieur. On calcule à part, pour mémoire, le barème qui minimise la perte sèche sur
l'activité réelle (« optimum d'efficacité », taux marginaux croissants, 50 % au-delà du dernier seuil), puis le
chemin qui va du barème neutre à cet optimum : quelle part du gain d'efficacité atteignable obtient-on sans
bouleverser la répartition de la charge ?

Perte sèche v2 (modele_purs.evalue, clés v2) : la quantité réagit au taux de l'impôt fusionné (et non au taux net
total : Lehmann, Marical et Rioux, 2013 ; Sicsic, 2022), chaque euro perdu coûte le coin total non contributif
(IR-CSG, cotisations non contributives, retrait de la prime d'activité) ; élasticité du revenu réellement produit
faible (0,05 à 0,10 au centre), marge extensive η = 0,25 sous 2 Smic ; la réaction du revenu déclaré (dixième du
haut) est comptée à part, comme un effet sur la recette, net du déplacement vers l'IS et le PFU.

Lancer depuis fiscalite/ : python3 synthese/architectures_ircsg.py
Sorties : synthese/sorties/architectures_ircsg.txt et .json
"""
import itertools
import json
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE)]
import modele_purs as M  # noqa: E402

ex = M.ex
OUT = HERE / "sorties"
JEUX = ("bas", "central", "haut")
CAS = (("retraité seul 17 000 €", "retraite_seul", 17e3), ("salarié seul au Smic (21 500 € brut)", "seul", 21.5e3),
       ("couple avec deux enfants 50 000 €", "couple_2enf", 50e3))
L = []


def p(s=""):
    print(s, flush=True)
    L.append(s)


def bareme(b, d=0.0, top=0.50):
    t0, tb, z1, t1, z2 = b
    return ex.bareme_lineaire([0, 20e3, z1, z2], [t0 + d, tb + d, t1 + d, top])


def options(**k):
    o = dict(M.OPT0)
    o.update(k)
    return o


def cale_t1(t0, tb, z1, z2, o):
    if M.recette(*bareme((t0, tb, z1, 0.50, z2)), o) < M.CIBLE:
        return None
    lo, hi = 0.0, 0.50
    for _ in range(30):
        t1 = (lo + hi) / 2
        lo, hi = (t1, hi) if M.recette(*bareme((t0, tb, z1, t1, z2)), o) < M.CIBLE else (lo, t1)
    return (lo + hi) / 2


def cale_d(b, o):
    lo, hi = -0.15, 0.30
    for _ in range(34):
        d = (lo + hi) / 2
        lo, hi = (d, hi) if M.recette(*bareme(b, d), o) < M.CIBLE else (lo, d)
    return (lo + hi) / 2


def melange(sa, sb, lam):
    (tma, Ta), (tmb, Tb) = sa, sb
    return (lambda z: (1 - lam) * tma(z) + lam * tmb(z)), (lambda z: (1 - lam) * Ta(z) + lam * Tb(z))


def grille(axes, critere, o):
    rows = []
    for t0, tb, z1, z2 in itertools.product(*axes):
        if tb < t0:
            continue
        t1 = cale_t1(t0, tb, z1, z2, o)
        if t1 is None or t1 < tb:
            continue
        b = (t0, tb, z1, t1, z2)
        rows.append((critere(b), b))
    rows.sort(key=lambda r: r[0])
    return rows


def fb(b):
    return (f"{100*b[0]:.0f} % au premier euro, {100*b[1]:.0f} % à 20 k€, {100*b[3]:.1f} % à {b[2]/1e3:.0f} k€, "
            f"50 % à {b[4]/1e3:.0f} k€")


def evalue_tout(nom, sched, o, ref_v2=None):
    """Perte sèche v2 pour les trois jeux, répartition (jeu central), cas-types."""
    r = {j: M.evalue(nom, *sched, o, jeu=j, sorties=(j == "central")) for j in JEUX}
    c = r["central"]
    out = dict(nom=nom, recette=c["recette"], **{f"v2_{j}": r[j]["v2"] for j in JEUX},
               **{f"decl_{j}": r[j]["v2_decl_recette"] for j in JEUX},
               reel=c["v2_reel"], ext=c["v2_ext"], **{k: c[k] for k in c if k.startswith("v2_reel_")},
               perdants500=c["perdants500"], ecart_moyen=c["ecart_moyen"], dec_eur=c["dec_eur"],
               top1_Md=c["top1_Md"], top10_Md=c["top10_Md"], groupes=c["groupes"],
               cas={n: M.cas_type(*sched, o, prof, brut) for n, prof, brut in CAS})
    if ref_v2:
        out["part"] = {j: out[f"v2_{j}"] / ref_v2[j] for j in JEUX}
    return out


def ligne(r, d=None):
    g = r["groupes"]
    part = (" ; part de l'optimum " + " / ".join(f"{100*r['part'][j]:.0f} %" for j in JEUX)) if "part" in r else ""
    p(f"[{r['nom']}]" + (f" points pour tous {100*d:+.2f} ;" if d is not None else "")
      + f" perte sèche réelle {r['v2_central']:+.1f} Md€ (basse {r['v2_bas']:+.1f}, haute {r['v2_haut']:+.1f})"
      + f" dont intensive {r['reel']:+.1f} [moitié du bas {r['v2_reel_q50']:+.1f}, 50-90 {r['v2_reel_q90']:+.1f},"
      + f" 90-99 {r['v2_reel_q99']:+.1f}, 1 % {r['v2_reel_top1']:+.1f}], extensive {r['ext']:+.1f}{part}")
    p(f"    revenu déclaré : recette {r['decl_central']:+.1f} Md€ ({r['decl_bas']:+.1f} à {r['decl_haut']:+.1f}) ;"
      f" écart moyen à aujourd'hui {r['ecart_moyen']:.0f} € par foyer ; perdants > 500 € {r['perdants500']:.0f} %")
    p("    déciles € " + " ".join(f"{u:+.0f}" for u in r["dec_eur"]) + f" ; 1 % du haut {r['top1_Md']:+.1f} Md€ ;"
      f" 10 % du haut {r['top10_Md']:+.1f} Md€")
    p(f"    Md€ : retraités {g['retraites']['Md']:+.1f} ; couples avec deux enfants {g['couples2']['Md']:+.1f} ;"
      f" parents isolés {g['parents_isoles']['Md']:+.1f} | € par foyer : seul actif {g['seuls_actifs']['eur']:+,.0f} ;"
      f" seul retraité {g['seuls_retraites']['eur']:+,.0f} ; parent isolé {g['parents_isoles']['eur']:+,.0f} ;"
      f" couple actif sans enfant {g['couples0_actifs']['eur']:+,.0f} ; couple retraité"
      f" {g['couples0_retraites']['eur']:+,.0f} ; couple avec deux enfants {g['couples2']['eur']:+,.0f}")
    p("    cas-types : " + " ; ".join(f"{n} {u:+,.0f} €" for n, u in r["cas"].items()))


def prix(b, o, d0):
    out = {}
    for j in JEUX:
        r0 = M.evalue("p0", *bareme(b, d0), o, jeu=j, sorties=False)
        r1 = M.evalue("p1", *bareme(b, d0 + 0.002), o, jeu=j, sorties=False)
        out[j] = (r1["v2"] - r0["v2"]) / (r1["recette"] - r0["recette"])
    return out


if __name__ == "__main__":
    o0 = options()
    p("Méthode v2 : perte sèche sur l'activité réelle, variation par rapport à aujourd'hui (Md€ par an ; négatif ="
      " gain) ; jeux bas / central / haut (modele_purs.V2) ; recette 220,1 Md€ dans tous les cas.")
    p(f"Élasticités : {json.dumps(M.V2)} ; déplacement s = {M.S_DEPL} vers {M.TAU_ALT}")
    p()

    def ecart(b):
        return M.evalue("n", *bareme(b), o0, sorties=True)["ecart_moyen"]

    neutres = grille(([0.02, 0.04, 0.06, 0.08, 0.10, 0.12], [0.08, 0.10, 0.12, 0.14, 0.16, 0.18],
                      [25e3, 30e3, 40e3, 50e3, 60e3], [150e3, 200e3, 250e3, 400e3, 600e3]), ecart, o0)
    bN = neutres[0][1]
    p(f"[NEUTRE] barème qui s'écarte le moins de la charge d'aujourd'hui : {fb(bN)} (écart moyen"
      f" {neutres[0][0]:.0f} € par foyer ; {len(neutres)} barèmes essayés)")
    p("[NEUTRE] suivants : " + " | ".join(f"{fb(b)} : {c:.0f} €" for c, b in neutres[1:5]))

    def eff(b):
        return M.evalue("o", *bareme(b), o0, sorties=False)["v2"]

    opt = grille(([0.04, 0.06, 0.08, 0.10, 0.12, 0.14, 0.16, 0.18], [0.10, 0.12, 0.14, 0.16, 0.18, 0.20, 0.22, 0.24],
                  [30e3, 45e3, 60e3, 90e3], [250e3, 400e3, 600e3, 1e6, 2e6]), eff, o0)
    bO = opt[0][1]
    p(f"[OPTIMUM] barème qui minimise la perte sèche réelle (jeu central) : {fb(bO)} ({opt[0][0]:+.2f} Md€)")
    p("[OPTIMUM] suivants : " + " | ".join(f"{fb(b)} : {c:+.2f}" for c, b in opt[1:5]))
    p()
    sN, sO = bareme(bN), bareme(bO)
    rO = evalue_tout("Optimum d'efficacité (pour mémoire)", sO, o0)
    # gain atteignable : meilleur des optimums sans franchise et avec franchise d'activité de 4 000 ou 8 000 €
    att = {0.0: (rO["v2_central"], bO, o0)}
    for F in (4000.0, 8000.0):
        oF = options(F=F)
        g_ = grille(([0.10, 0.12, 0.14, 0.16, 0.18, 0.20], [0.12, 0.14, 0.16, 0.18, 0.20, 0.22],
                     [30e3, 45e3, 60e3], [600e3, 1e6, 2e6]),
                    lambda b, oF=oF: M.evalue("o", *bareme(b), oF, sorties=False)["v2"], oF)
        att[F] = (g_[0][0], g_[0][1], oF)
        p(f"[OPTIMUM franchise {F:.0f} €] {fb(g_[0][1])} ({g_[0][0]:+.2f} Md€)")
    Fb = min(att, key=lambda k: att[k][0])
    rB = evalue_tout(f"Gain atteignable : optimum avec franchise d'activité de {Fb:.0f} €", bareme(att[Fb][1]), att[Fb][2])
    refv2 = {j: rB[f"v2_{j}"] for j in JEUX}
    p(f"[ATTEIGNABLE] franchise {Fb:.0f} € : " + " / ".join(f"{j} {refv2[j]:+.2f}" for j in JEUX)
      + " Md€ (barème optimisé pour le jeu central, évalué avec chaque jeu)")
    rO["part"] = {j: rO[f"v2_{j}"] / refv2[j] for j in JEUX}
    rB["part"] = {j: 1.0 for j in JEUX}
    res = []
    for nom, k in (("Barème neutre : assiette large, même barème pour tous, impôt individuel", {}),
                   ("Neutre + quotient conjugal et familial", dict(fam="quotient")),
                   ("Neutre + franchise de 6 000 € par enfant", dict(fam="franchise")),
                   ("Neutre + chèque par enfant", dict(fam="cheque")),
                   ("Neutre + abattement de 10 % sur les pensions", dict(abat_pens=0.10)),
                   ("Neutre + petites pensions exonérées (jusqu'à 12 500 €, dégressif jusqu'à 25 000 €)",
                    dict(Fp=12500.0, Fp_degressif=True)),
                   ("Neutre + franchise d'activité 4 000 €", dict(F=4000.0)),
                   ("Neutre + franchise d'activité 8 000 €", dict(F=8000.0)),
                   ("Neutre + franchise de 8 000 € sur tous les revenus", dict(F=8000.0, sur="tout")),
                   ("Neutre + franchise d'activité 4 000 € + 6 000 € par enfant + petites pensions",
                    dict(F=4000.0, fam="franchise", Fp=12500.0, Fp_degressif=True)),
                   ("Neutre + franchise d'activité 8 000 € + 6 000 € par enfant + petites pensions",
                    dict(F=8000.0, fam="franchise", Fp=12500.0, Fp_degressif=True))):
        o = options(**k)
        d = cale_d(bN, o) if k else 0.0
        r = evalue_tout(nom, bareme(bN, d), o, refv2)
        r["d"], r["options"] = d, o
        ligne(r, d)
        res.append(r)
    p()
    ligne(rB)
    ligne(rO)
    oc = options(F=8000.0, fam="franchise", Fp=12500.0, Fp_degressif=True)
    dc = cale_d(bO, oc)
    rOc = evalue_tout("Optimum + franchise d'activité 8 000 € + 6 000 € par enfant + petites pensions",
                      bareme(bO, dc), oc, refv2)
    rOc["d"] = dc
    ligne(rOc, dc)
    p()
    # chemin du barème neutre vers l'optimum (recette constante par construction : la recette est linéaire en T)
    chemin = []
    for lam in np.linspace(0, 1, 11):
        s = melange(sN, sO, lam)
        r = {j: M.evalue("chemin", *s, o0, jeu=j, sorties=(j == "central")) for j in JEUX}
        c = r["central"]
        chemin.append(dict(lam=float(lam), recette=c["recette"], **{f"v2_{j}": r[j]["v2"] for j in JEUX},
                           ecart_moyen=c["ecart_moyen"], perdants500=c["perdants500"], top10_Md=c["top10_Md"],
                           top1_Md=c["top1_Md"], retraites_Md=c["groupes"]["retraites"]["Md"],
                           decl=c["v2_decl_recette"]))
        p(f"[CHEMIN λ={lam:.1f}] recette {c['recette']:.1f} ; perte sèche réelle {r['central']['v2']:+.2f}"
          f" ({r['bas']['v2']:+.2f} à {r['haut']['v2']:+.2f}) ; part de l'optimum "
          + " / ".join(f"{100*r[j]['v2']/refv2[j]:.0f} %" for j in JEUX)
          + f" ; écart moyen {c['ecart_moyen']:.0f} € ; perdants {c['perdants500']:.0f} % ; 10 % du haut"
          f" {c['top10_Md']:+.1f} Md€ ; retraités {c['groupes']['retraites']['Md']:+.1f} ; revenu déclaré"
          f" {c['v2_decl_recette']:+.1f}")
    p()
    # proposition : parmi les barèmes simples, avec franchise d'activité, aide aux enfants et petites pensions, le plus
    # efficace de ceux qui ne changent la charge moyenne d'aucun décile de plus de 500 € par foyer et n'alourdissent
    # pas celle du 1 % le plus aisé (contrainte de répartition fixée d'avance ; l'optimiseur ne choisit que le barème)
    props = {}
    for F in (4000.0, 8000.0):
        op = options(F=F, fam="franchise", Fp=12500.0, Fp_degressif=True)
        ok = []
        for t0, tb, z1, z2 in itertools.product([0.06, 0.08, 0.10, 0.12, 0.14, 0.16], [0.14, 0.16, 0.18, 0.20, 0.22],
                                                [30e3, 45e3, 60e3], [150e3, 250e3, 400e3, 600e3, 1e6]):
            if tb < t0:
                continue
            t1 = cale_t1(t0, tb, z1, z2, op)
            if t1 is None or t1 < tb:
                continue
            b = (t0, tb, z1, t1, z2)
            c = M.evalue("prop", *bareme(b), op, sorties=True)
            if max(abs(u) for u in c["dec_eur"]) <= 500 and c["top1_Md"] <= 0:
                ok.append((c["v2"], b))
        ok.sort(key=lambda r: r[0])
        bP = ok[0][1]
        p(f"[PROPOSITION franchise {F:.0f} €] {len(ok)} barèmes respectent la contrainte ; retenu : {fb(bP)}")
        r = evalue_tout(f"Proposition : franchise d'activité {F:.0f} € + 6 000 € par enfant + petites pensions, barème"
                        f" {fb(bP)}", bareme(bP), op, refv2)
        r["bareme"], r["options"] = list(bP), op
        ligne(r)
        props[F] = r
    p()
    pr = {"neutre": prix(bN, o0, 0.0), "neutre + franchise 8 000 € + enfants + petites pensions": prix(bN, oc, cale_d(bN, oc)),
          "optimum": prix(bO, o0, 0.0)}
    for k, u in pr.items():
        p(f"[PRIX] {k} : perte sèche réelle par milliard levé (un point de taux pour tous) "
          + " / ".join(f"{j} {u[j]:.2f}" for j in JEUX))
    json.dump(dict(neutre=list(bN), optimum=list(bO), architectures=res, optimum_r=rO, optimum_comb=rOc,
                   propositions={str(int(k)): v for k, v in props.items()},
                   chemin=chemin, prix=pr, V2=M.V2, atteignable=rB),
              open(OUT / "architectures_ircsg.json", "w"), ensure_ascii=False, indent=1, default=float)
    (OUT / "architectures_ircsg.txt").write_text("\n".join(L) + "\n", encoding="utf-8")
