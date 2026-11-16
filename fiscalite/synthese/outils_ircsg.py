"""Outils communs aux programmes de la partie IR-CSG réécrite (situation_ircsg, naive_ircsg, proposition_ircsg,
arbitrages_prop_ircsg, transition_ircsg, tables_ircsg, figures_ircsg_n).

- Barèmes : celui de la réforme (taux marginal en ligne droite entre 0, 20 000 €, z1 et z2, 50 % au-delà ; la même
  famille que architectures_ircsg.py) et l'empilement « barème de l'IR + taux proportionnel » de la réforme naïve.
- Calage de la recette (220,1 Md€) et de la neutralité du 1 % le plus aisé.
- Évaluation complète d'un système : perte sèche (jeux bas, central, haut et long terme), répartition par décile et
  par type de foyer, distribution des hausses individuelles entre foyers représentatifs.
- Cas-types OpenFisca (sorties/cas_types_openfisca.csv, openfisca_cas_ircsg.py ; législation des revenus 2025) :
  charge d'aujourd'hui, impôt de la réforme, taux moyen et marginal, taux de prélèvement sur un salaire de reprise
  d'emploi.
- Taux marginaux (sorties/courbes_marginales_openfisca.csv) : prélèvement sur 1 000 € de revenu après cotisations en
  plus, grille de 100 €, aujourd'hui (OpenFisca) et pour toute réforme (calcul direct sur le revenu après cotisations,
  sans interpolation ni lissage).
"""
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE)]
import modele_purs as M  # noqa: E402

ex = M.ex
P = M.P
OUT = HERE / "sorties"
JEUX = ("bas", "central", "haut", "long")
SMIC = 11.88 * 151.67 * 12          # Smic 2025 brut annuel, 21 622 € (cas-types, openfisca_cas_ircsg.py)
CTN = pd.read_csv(OUT / "cas_types_openfisca.csv")
MGN = pd.read_csv(OUT / "courbes_marginales_openfisca.csv")
MGN["charge"] = MGN.ir + MGN.csg + MGN.crds
MGN["charge_plus"] = MGN.ir_plus + MGN.csg_plus + MGN.crds_plus
CTN["charge"] = CTN.ir + CTN.csg + CTN.crds
CTN["charge_plus"] = CTN.ir_plus + CTN.csg_plus + CTN.crds_plus
ENF = {"seul": 0, "couple_0enf": 0, "couple_0enf_mono": 0, "couple_2enf": 2, "couple_2enf_mono": 2, "couple_3enf": 3,
       "couple_3enf_mono": 3, "parent_isole_1enf": 1, "parent_isole_2enf": 2, "retraite_seul": 0, "retraite_couple": 0,
       "conjoint": 0, "conjoint_2enf": 2}
RETR = {"retraite_seul", "retraite_couple"}


# ------------------------------------------------------------------ barèmes
def bareme(t0, tb, z1, t1, z2, top=0.50):
    return ex.bareme_lineaire([0, 20e3, z1, z2], [t0, tb, t1, top])


def empile(tau):
    return ex.bareme_empile(tau)


def options(**k):
    o = dict(M.OPT0)
    o.update(k)
    return o


def fb(b):
    t0, tb, z1, t1, z2 = b[:5]
    return (f"{100*t0:.0f} % au premier euro imposé, {100*tb:.0f} % à 20 k€, {100*t1:.1f} % à {z1/1e3:.0f} k€, "
            f"50 % à {z2/1e3:,.0f} k€")


def recette(sched, o):
    return M.recette(*sched, o)


def cale_t1(t0, tb, z1, z2, o, top=0.50):
    """Taux t1 (au nœud z1) qui donne la recette cible. La recette est linéaire en t1 sauf avec le quotient :
    sécante, puis bisection si besoin. None si la recette est hors d'atteinte avec t1 entre 0 et top."""
    f = lambda t1: recette(bareme(t0, tb, z1, t1, z2, top), o) - M.CIBLE  # noqa: E731
    a, b = 0.0, top
    fa, fb_ = f(a), f(b)
    if fa > 0 or fb_ < 0:
        return None
    for _ in range(60):
        t = a - fa * (b - a) / (fb_ - fa) if fb_ != fa else (a + b) / 2
        if not (a < t < b):
            t = (a + b) / 2
        ft = f(t)
        if abs(ft) < 1e-4:
            return t
        if ft < 0:
            a, fa = t, ft
        else:
            b, fb_ = t, ft
    return (a + b) / 2


def cale_d(sched_de_d, o, lo=-0.15, hi=0.30):
    """Nombre de points d ajoutés aux taux sous le taux supérieur pour retrouver la recette (sched_de_d(d))."""
    for _ in range(40):
        d = (lo + hi) / 2
        lo, hi = (d, hi) if recette(sched_de_d(d), o) < M.CIBLE else (lo, d)
    return (lo + hi) / 2


def variations(sched, o):
    """Pour chaque type de foyer : (nom, groupe, famille, poids, variation de charge par foyer représentatif)."""
    out = []
    for nom, grp, fam, w, parts, kids in M.TYPES:
        imp = M.impot_adultes(*sched, o, *M.adultes(grp, parts, o), kids)[0]
        out.append((nom, grp, fam, w, imp - M.CURT[nom]))
    return out


def top1_md(sched, o):
    return sum((w * d * (M.Q >= 0.99)).sum() for _, _, _, w, d in variations(sched, o)) / 1e9


def cale_top1(t0, tb, z1, o, zlo=60e3, zhi=5e6, top=0.50, tol=0.05):
    """Seuil z2 (taux de 50 %) qui laisse inchangée la charge du 1 % le plus aisé, t1 recalé sur la recette à chaque
    pas. Renvoie (z2, t1, Δ 1 %) ou None si aucune valeur de z2 entre zlo et zhi n'annule l'effet."""
    def g(z2):
        t1 = cale_t1(t0, tb, z1, z2, o, top)
        if t1 is None:
            return None, None
        return top1_md(bareme(t0, tb, z1, t1, z2, top), o), t1
    a, b = np.log(max(zlo, z1 + 5e3)), np.log(zhi)
    ga, ta = g(np.exp(a))
    gb, tb_ = g(np.exp(b))
    if ga is None or gb is None or ga * gb > 0:
        return None
    for _ in range(30):
        c = (a + b) / 2
        gc, tc = g(np.exp(c))
        if gc is None:
            return None
        if abs(gc) < tol:
            return np.exp(c), tc, gc
        if (gc > 0) == (ga > 0):
            a, ga = c, gc
        else:
            b, gb = c, gc
    return np.exp(c), tc, gc


# ------------------------------------------------------------------ distribution des hausses individuelles
def distribution(sched, o):
    """Centiles des variations par foyer (foyers représentatifs) et nombre de foyers qui perdent plus de 500 / 1 000 €,
    pour tous les foyers, les retraités, les couples de retraités, les actifs."""
    var = variations(sched, o)
    out = {}
    for cle, f in (("tous", lambda g, fm: True), ("retraites", lambda g, fm: g == "R"),
                   ("couples_retraites", lambda g, fm: g == "R" and fm == "couples0"),
                   ("seuls_retraites", lambda g, fm: g == "R" and fm == "seuls"), ("actifs", lambda g, fm: g == "A"),
                   ("couples2", lambda g, fm: fm == "couples2")):
        d = np.concatenate([v[4] for v in var if f(v[1], v[2])])
        w = np.concatenate([v[3] for v in var if f(v[1], v[2])])
        k = np.argsort(d)
        d, w = d[k], w[k]
        c = np.cumsum(w) / w.sum()
        q = {f"p{int(100*p)}": float(d[min(np.searchsorted(c, p), len(d) - 1)]) for p in (0.1, 0.25, 0.5, 0.75, 0.9, 0.99)}
        out[cle] = dict(**q, perd500_M=float(w[d > 500].sum() / 1e6), perd1000_M=float(w[d > 1000].sum() / 1e6),
                        gagne500_M=float(w[d < -500].sum() / 1e6), foyers_M=float(w.sum() / 1e6))
    return out


# ------------------------------------------------------------------ cas-types
def _ligne(profil, brut):
    g = CTN[(CTN.profil == profil) & (np.isclose(CTN.brut, brut))]
    if g.empty:
        raise KeyError((profil, brut))
    return g.iloc[0]


def charge_auj(profil, brut, plus=False):
    g = _ligne(profil, brut)
    return float(g.charge_plus if plus else g.charge)


def _quotient_cas(T, tm, y, couple, kids):
    """Quotient conjugal et familial appliqué à l'impôt fusionné, plafonds actuels (cas-types : règle exacte pour
    un parent isolé, première part entière, demi-parts suivantes ; le modèle agrégé n'a qu'un enfant par parent isolé)."""
    if couple:
        p0, p = 2.0, 2.0 + 0.5 * min(kids, 2) + max(kids - 2, 0)
        cap = 2 * P.PLAF * (p - p0)
    elif kids:
        p0, p = 1.0, 2.0 + 0.5 * min(kids - 1, 1) + max(kids - 2, 0)
        cap = P.PLAF_ISOL + 2 * P.PLAF * (p - 2.0)
    else:
        return T(y)
    return np.maximum(p * T(y / p), p0 * T(y / p0) - cap)


def impot_cas(sched, o, profil, brut, plus=False):
    """Impôt fusionné d'un cas-type (mêmes règles que modele_purs.impot_adultes ; pas de versement d'épargne retraite)."""
    g = _ligne(profil, brut)
    a = np.array([g.base_a_plus if plus else g.base_a])
    b = np.array([g.base_b_plus if plus else g.base_b])
    couple = profil.startswith(("couple", "retraite_couple", "conjoint"))
    zs = [a, b] if couple else [a]
    kids = ENF[profil]
    if profil in RETR:
        ps_ = list(zs)
        ls = [z if o["sur"] == "tout" else 0 * z for z in zs]
    else:
        ps_ = [0 * z for z in zs]
        ls = list(zs)
    if o["fam"] == "quotient":
        o2 = dict(o, fam="rien")
        tax = M.impot_adultes(*sched, o2, zs, ls, ps_, 0)[2]
        tm, T = sched
        return float(_quotient_cas(T, tm, sum(tax), couple, kids)[0])
    return float(M.impot_adultes(*sched, o, zs, ls, ps_, kids)[0][0])


def delta_cas(sched, o, profil, brut):
    return impot_cas(sched, o, profil, brut) - charge_auj(profil, brut)


def marginal_cas(sched, o, profil, brut):
    """Prélèvement sur 1 000 € de revenu brut en plus (aujourd'hui si sched est None), en %."""
    if sched is None:
        return 100 * (charge_auj(profil, brut, True) - charge_auj(profil, brut)) / 1000
    return 100 * (impot_cas(sched, o, profil, brut, True) - impot_cas(sched, o, profil, brut)) / 1000


def impot_base(sched, o, profil, base):
    """Impôt fusionné d'une personne seule (salarié « seul » ou « retraite_seul ») dont le revenu après cotisations
    vaut base (tableau)."""
    a = np.asarray(base, float)
    if profil == "retraite_seul":
        zs, ps_, ls = [a], [a], [a if o["sur"] == "tout" else 0 * a]
    else:
        zs, ps_, ls = [a], [0 * a], [a]
    if o["fam"] == "quotient":
        o = dict(o, fam="rien")              # personne seule sans enfant : le quotient ne change rien
    return M.impot_adultes(*sched, o, zs, ls, ps_, 0)[0]


def courbe_marginale(sched, o, profil, bmin=1000.0, bmax=None):
    """(revenus après cotisations, prélèvement en % sur 1 000 € de plus). Aujourd'hui (sched None) : OpenFisca,
    chaque point calculé ; réforme : calcul direct, mêmes revenus que les points d'OpenFisca."""
    g = MGN[MGN.profil == profil].sort_values("base")
    g = g[(g.base >= bmin) & ((g.base <= bmax) if bmax else True)]
    b, bp = g.base_eff.values, g.base_eff_plus.values
    if sched is None:
        return g.base.values, 100 * (g.charge_plus.values - g.charge.values) / (bp - b)
    return g.base.values, 100 * (impot_base(sched, o, profil, bp) - impot_base(sched, o, profil, b)) / (bp - b)


def marginal_base(sched, o, profil, base):
    """Prélèvement sur 1 000 € de revenu après cotisations en plus, au revenu base (point de la grille de 100 €), en %."""
    xs, ys = courbe_marginale(sched, o, profil)
    return float(ys[np.argmin(np.abs(xs - base))])


def ptr_cas(sched, o, profil, brut):
    """Taux de prélèvement IR-CSG sur un salaire de reprise d'emploi (brut), en % : impôt avec ce salaire moins impôt
    sans, rapporté au salaire. Aujourd'hui si sched est None. Profils « seul » ou « conjoint » (second salaire)."""
    if sched is None:
        return 100 * (charge_auj(profil, brut) - charge_auj(profil, 0.0)) / brut
    return 100 * (impot_cas(sched, o, profil, brut) - impot_cas(sched, o, profil, 0.0)) / brut


CAS = [  # (clé, profil, brut, libellé)
    ("ret12", "retraite_seul", 12000.0, "Retraité seul, pension de 12 000 €"),
    ("ret16", "retraite_seul", 16000.0, "Retraité seul, pension de 16 000 €"),
    ("ret18", "retraite_seul", 18000.0, "Retraité seul, pension de 18 000 €"),
    ("ret20", "retraite_seul", 20000.0, "Retraité seul, pension de 20 000 €"),
    ("ret25", "retraite_seul", 25000.0, "Retraité seul, pension de 25 000 €"),
    ("ret35", "retraite_seul", 35000.0, "Retraité seul, pension de 35 000 €"),
    ("rc30", "retraite_couple", 30000.0, "Couple de retraités, 30 000 € de pensions (60/40)"),
    ("rc45", "retraite_couple", 45000.0, "Couple de retraités, 45 000 € de pensions (60/40)"),
    ("smic_mi", "seul", SMIC / 2, "Jeune salarié à mi-temps au Smic"),
    ("smic", "seul", SMIC, "Jeune salarié au Smic"),
    ("cadre60", "seul", 60000.0, "Cadre seul, 60 000 € brut"),
    ("cadre100", "seul", 100000.0, "Cadre seul, 100 000 € brut"),
    ("cadre200", "seul", 200000.0, "Cadre dirigeant seul, 200 000 € brut"),
    ("pi_smic", "parent_isole_2enf", SMIC, "Parent isolé, deux enfants, au Smic"),
    ("pi35", "parent_isole_2enf", 35000.0, "Parent isolé, deux enfants, 35 000 € brut"),
    ("c0_50", "couple_0enf", 50000.0, "Couple sans enfant, 50 000 € brut (60/40)"),
    ("c0m_50", "couple_0enf_mono", 50000.0, "Couple sans enfant à un seul revenu, 50 000 €"),
    ("c0m_80", "couple_0enf_mono", 80000.0, "Couple sans enfant à un seul revenu, 80 000 €"),
    ("c2_50", "couple_2enf", 50000.0, "Couple avec deux enfants, 50 000 € brut (60/40)"),
    ("c2m_50", "couple_2enf_mono", 50000.0, "Couple avec deux enfants à un seul revenu, 50 000 €"),
    ("c3_40", "couple_3enf", 40000.0, "Couple avec trois enfants, 40 000 € brut (60/40)"),
    ("c3_60", "couple_3enf", 60000.0, "Couple avec trois enfants, 60 000 € brut (60/40)"),
    ("c3_80", "couple_3enf", 80000.0, "Couple avec trois enfants, 80 000 € brut (60/40)"),
    ("c3m_60", "couple_3enf_mono", 60000.0, "Couple avec trois enfants à un seul revenu, 60 000 €"),
]


def cas_types(sched, o):
    out = {}
    for cle, prof, brut, lib in CAS:
        auj = charge_auj(prof, brut)
        nv = impot_cas(sched, o, prof, brut)
        out[cle] = dict(libelle=lib, auj=auj, apres=nv, delta=nv - auj, brut=brut)
    return out


def ptrs(sched, o):
    """Taux de prélèvement sur le premier salaire : personne seule et conjoint (premier salaire de 30 000 €), à
    mi-temps et à temps plein au Smic."""
    return {f"{p}_{k}": ptr_cas(sched, o, p, f * SMIC) for p in ("seul", "conjoint") for k, f in (("mi", 0.5), ("smic", 1.0))}


# ------------------------------------------------------------------ évaluation complète
def evalue_complet(nom, sched, o, jeux=JEUX):
    r = {j: M.evalue(nom, *sched, o, jeu=j, sorties=(j == "central")) for j in jeux}
    c = r["central"]
    out = dict(nom=nom, recette=c["recette"], options={k: v for k, v in o.items()},
               **{f"gain_{j}": -r[j]["v2"] for j in jeux}, **{f"ext_{j}": -r[j]["v2_ext"] for j in jeux},
               intensif=-c["v2_reel"], extensif=-c["v2_ext"],
               intensif_q50=-c["v2_reel_q50"], intensif_q90=-c["v2_reel_q90"], intensif_q99=-c["v2_reel_q99"],
               intensif_top1=-c["v2_reel_top1"], decl=c["v2_decl_recette"],
               **{f"decl_{j}": r[j]["v2_decl_recette"] for j in jeux},
               perdants500=c["perdants500"], ecart_moyen=c["ecart_moyen"], dec_eur=c["dec_eur"],
               top1_Md=c["top1_Md"], top10_Md=c["top10_Md"], total_Md=c["total_Md"],
               groupes={k: dict(Md=v["Md"], eur=v["eur"], foyers_M=v["foyers_M"]) for k, v in c["groupes"].items()},
               distribution=distribution(sched, o), cas=cas_types(sched, o), ptr=ptrs(sched, o))
    return out


def ligne_resume(r):
    g = r["groupes"]
    return (f"[{r['nom']}] gain {r['gain_central']:.2f} Md€ ({r['gain_bas']:.2f} à {r['gain_haut']:.2f} ; long terme "
            f"{r.get('gain_long', float('nan')):.2f}) dont intensif {r['intensif']:.2f} [bas {r['intensif_q50']:+.2f}, 50-90 "
            f"{r['intensif_q90']:+.2f}, 90-99 {r['intensif_q99']:+.2f}, 1 % {r['intensif_top1']:+.2f}], participation "
            f"{r['extensif']:.2f} ; revenu déclaré {r['decl']:+.1f} ; perdants > 500 € {r['perdants500']:.0f} %\n"
            f"    déciles € " + " ".join(f"{u:+.0f}" for u in r["dec_eur"]) + f" ; 1 % {r['top1_Md']:+.2f} Md€ ; 10 % "
            f"{r['top10_Md']:+.1f} Md€ ; retraités {g['retraites']['Md']:+.1f} Md€ ; actifs {g['actifs']['Md']:+.1f}\n"
            f"    € par foyer : seul actif {g['seuls_actifs']['eur']:+,.0f} ; parent isolé {g['parents_isoles']['eur']:+,.0f} ;"
            f" couple actif sans enfant {g['couples0_actifs']['eur']:+,.0f} ; couple avec enfants {g['couples2']['eur']:+,.0f} ;"
            f" retraité seul {g['seuls_retraites']['eur']:+,.0f} ; couple de retraités {g['couples0_retraites']['eur']:+,.0f}\n"
            f"    premier salaire (taux de prélèvement, %) : seul mi-temps {r['ptr']['seul_mi']:.1f}, seul Smic "
            f"{r['ptr']['seul_smic']:.1f}, conjoint mi-temps {r['ptr']['conjoint_mi']:.1f}, conjoint Smic {r['ptr']['conjoint_smic']:.1f}\n"
            "    cas-types : " + " ; ".join(f"{k} {v['delta']:+,.0f}" for k, v in r["cas"].items()))


def ecrire(nom, lignes, donnees):
    (OUT / f"{nom}.txt").write_text("\n".join(lignes) + "\n", encoding="utf-8")
    json.dump(donnees, open(OUT / f"{nom}.json", "w"), ensure_ascii=False, indent=1, default=float)
