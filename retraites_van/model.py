"""Qui paie une réforme des retraites ? Valeur actualisée, par âge, de trois réformes de même rendement budgétaire.

Réformes (permanentes, à partir de l'année de réforme, Md€ de 2025 à plein effet) :
  A. baisse uniforme de toutes les pensions, liquidées et futures, de delta = budget / pensions totales ;
  B. hausse du taux de cotisation retraite de dtau = budget / assiette (incidence entièrement sur les salariés) ;
  C. recul d'un an de l'âge de départ pour les générations qui n'ont pas atteint l'âge d'ouverture des droits.

Mesure : variation de la valeur actualisée nette des transferts reçus du système de retraite (pensions reçues, autres
prestations de remplacement, moins cotisations versées), espérée (pondérée par la survie) et actualisée à l'année de
réforme, par personne de chaque âge. Le salaire de l'année travaillée en plus n'est pas compté (il rémunère le travail
fourni) ; une variante le compte comme un gain.

Identité de contrôle : la somme, sur toutes les générations présentes et futures, des pertes actualisées est égale à la
valeur actualisée des gains budgétaires (comptabilité générationnelle, sans effet de comportement hors réforme C).

python3 model.py imprime un audit ; export : sorties/resultats.json.
"""
import json
from pathlib import Path

import numpy as np

D = Path(__file__).resolve().parent
P = {k: (v["valeur"] if isinstance(v, dict) and "valeur" in v else v) for k, v in
     json.loads((D / "params.json").read_text(encoding="utf-8")).items() if not k.startswith("_")}
CAL = json.loads((D / "data" / "calage.json").read_text(encoding="utf-8"))      # agrégats observés (OBS) et sources
AMAX = 106                                                                          # âges 0 à 105
AGES = np.arange(AMAX)


def lire(nom, cx, cy):
    import csv
    xs, ys = [], []
    with open(D / "data" / nom, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            try:
                xs.append(float(r[cx])), ys.append(float(r[cy]))
            except (ValueError, TypeError):
                continue
    return np.array(xs), np.array(ys)


def par_age(x, y, gauche=0.0, droite=None):
    """Série par âge simple à partir de points (âges ou centres de tranches), interpolation linéaire."""
    o = np.argsort(x)
    return np.interp(AGES, x[o], y[o], left=gauche, right=y[o][-1] if droite is None else droite)


# ----------------------------------------------------------------------------------------------- données de base
def donnees():
    a, pop = lire("population_2025.csv", "age", "pop")
    pop0 = np.zeros(AMAX)
    for x, v in zip(a.astype(int), pop):
        pop0[min(x, AMAX - 1)] += v
    a, q = lire("mortalite.csv", "age", "qx")
    qx = par_age(a, q, droite=1.0)
    qx[-1] = 1.0
    a, e = lire("taux_emploi_age.csv", "age", "taux_emploi")
    emp = par_age(a, e / (100 if e.max() > 1.5 else 1), droite=0.0)
    emp[AGES < 15] = 0
    a, w = lire("salaire_age.csv", "age", "salaire_annuel_moyen")
    sal = par_age(a, w)                                           # salaire annuel moyen d'un actif occupé de cet âge
    a, s = lire("pension_age.csv", "age", "share_retired")
    part = par_age(a, s / (100 if s.max() > 1.5 else 1), droite=1.0)
    part[AGES < 50] = 0
    a, m = lire("pension_age.csv", "age", "pension_moyenne_mensuelle")
    pens = par_age(a, 12 * m)                                     # pension annuelle moyenne d'un retraité de cet âge
    return pop0, qx, emp, sal, part, pens


def decaler(f, d, debut=55, plein=58):
    """Décale un profil vers les âges élevés de d années à partir de `plein`, en raccordant progressivement depuis `debut`."""
    dd = np.clip((AGES - debut) / (plein - debut), 0, 1) * d
    return np.interp(AGES - dd, AGES, f)


def profils(pop0, qx, emp, sal, part, pens):
    """Profils par tête en 2025 (euros de 2025), droit de référence : âge légal 64 ans à terme.
    Les profils observés de 2025 (âge légal de 62 ans 9 mois) sont décalés de 1,25 an aux âges de la retraite."""
    d = P["age_legal_reference"] - CAL["age_legal_2025"]["valeur"]
    part_ref, emp_ref = decaler(part, d), decaler(emp, d)
    y = emp_ref * sal                                             # revenu d'activité par tête
    p = part_ref * pens                                           # pension par tête
    # calage sur les agrégats observés de 2025 (avec les profils observés, pas les profils de référence)
    ky = CAL["assiette_cotisations"]["valeur"] * 1e9 / (pop0 * emp * sal).sum()
    kp = CAL["pensions_totales"]["valeur"] * 1e9 / (pop0 * part * pens).sum()
    return dict(y=ky * y, p=kp * p, sal=ky * sal, pens=kp * pens, part=part_ref, emp=emp_ref, ky=ky, kp=kp)


# ----------------------------------------------------------------------------------------------- démographie
def demographie(pop0, qx, T):
    """Population par âge de l'année de base à base + T : mortalité (améliorée de m par an), naissances constantes,
    solde migratoire réparti entre 20 et 34 ans."""
    m = P["amelioration_mortalite"]
    N = np.zeros((T + 1, AMAX))
    N[0] = pop0
    Q = np.array([np.clip(qx * (1 - m) ** t, 0, 1) for t in range(T + 1)])
    Q[:, -1] = 1.0
    nais, mig = CAL["naissances"]["valeur"], CAL["solde_migratoire"]["valeur"]
    for t in range(1, T + 1):
        N[t, 1:] = N[t - 1, :-1] * (1 - Q[t - 1, :-1])
        N[t, 0] = nais
        N[t, 20:35] += mig / 15
    return N, Q


# ----------------------------------------------------------------------------------------------- réformes
def reformes(pr, N, Q, r, g):
    """Variation, par tête, des transferts nets reçus (perte > 0), par année t (0 = année de base) et âge.
    Renvoie dict réforme -> matrice (T+1, AMAX) en euros de 2025 de l'année t, et les paramètres calés."""
    T = N.shape[0] - 1
    G = (1 + g) ** np.arange(T + 1)[:, None]
    t0 = P["annee_reforme"] - P["annee_base"]
    actif = (np.arange(T + 1) >= t0)[:, None]
    y, p, sal, pens, part = pr["y"], pr["p"], pr["sal"], pr["pens"], pr["part"]
    # la cible est un rendement de 10 Md€ dans l'économie de 2025 : delta = 10 / pensions de référence de 2025
    delta = P["budget_cible"] / ((N[0] * p).sum() / 1e9)
    dtau = P["budget_cible"] / ((N[0] * y).sum() / 1e9)
    A = actif * delta * p[None, :] * G
    B = actif * dtau * y[None, :] * G
    # C : part de retraités décalée d'un an pour les générations qui ont au plus `age_max` ans l'année de réforme
    k, rho, tau, gam = P["kappa_emploi"], P["remplacement_autres_prestations"], P["taux_cotisation_retraite"], P["gain_droits_annee_sup"]
    dec = P["decalage_age"]
    part_c = np.interp(AGES - dec, AGES, part)
    dshare = np.clip(part - part_c, 0, None)                      # personnes privées de pension à cet âge
    # perte par tête à chaque âge : pension perdue, cotisations versées par ceux qui travaillent un an de plus, moins
    # les prestations (chômage, invalidité, minima) reçues par ceux qui ne travaillent pas, moins les droits acquis
    perte = (dshare * pens + tau * k * dshare * sal - (1 - k) * rho * dshare * pens
             - gam * k * part_c * pens * (AGES >= P["age_legal_reference"] + dec))
    salaire_net_sup = k * dshare * sal * (1 - CAL["prelevements_salaries"]["valeur"])
    age_max = P["age_max_touche"]                                 # générations touchées : âge l'année de réforme
    C = np.zeros_like(A)
    Cw = np.zeros_like(A)
    for t in range(t0, T + 1):
        nes_age = AGES - (t - t0)                                 # âge l'année de réforme
        touche = nes_age <= age_max
        C[t] = touche * perte * G[t, 0]
        Cw[t] = touche * (perte - salaire_net_sup) * G[t, 0]
    return dict(A=A, B=B, C=C, C_salaire=Cw), dict(delta=delta, dtau=dtau)


def va_individuelle(M, Q, r, t0):
    """Perte actualisée espérée, à l'année t0, d'une personne de chaque âge a vivante en t0 (somme sur sa vie)."""
    T = M.shape[0] - 1
    out = np.zeros(AMAX)
    for a in range(AMAX):
        surv, tot = 1.0, 0.0
        for k in range(0, min(AMAX - a, T - t0 + 1)):
            t, s = t0 + k, a + k
            tot += surv * M[t, s] / (1 + r) ** k
            surv *= 1 - Q[t, s]
        out[a] = tot
    return out


def va_generation_future(M, Q, r, t0, t_entree, age_entree=0):
    """Perte actualisée, ramenée à t0, d'une personne d'âge `age_entree` l'année t_entree (génération future)."""
    T = M.shape[0] - 1
    surv, tot = 1.0, 0.0
    for k in range(0, min(AMAX - age_entree, T - t_entree + 1)):
        t, s = t_entree + k, age_entree + k
        tot += surv * M[t, s] / (1 + r) ** (t - t0)
        surv *= 1 - Q[t, s]
    return tot


def ressources(pr, Q, r, g, t0):
    """Valeur actualisée des ressources restantes (revenus d'activité + pensions) d'une personne de chaque âge."""
    T = Q.shape[0] - 1
    G = (1 + g) ** np.arange(T + 1)[:, None]
    M = (pr["y"] + pr["p"])[None, :] * G
    return va_individuelle(M, Q, r, t0)


def calculer(r=None, g=None, verbeux=False):
    r = P["r"] if r is None else r
    g = P["g"] if g is None else g
    pop0, qx, emp, sal, part, pens = donnees()
    pr = profils(pop0, qx, emp, sal, part, pens)
    T = P["horizon"]
    N, Q = demographie(pop0, qx, T)
    M, cal = reformes(pr, N, Q, r, g)
    t0 = P["annee_reforme"] - P["annee_base"]
    G = (1 + g) ** np.arange(T + 1)
    res = dict(r=r, g=g, delta=cal["delta"], dtau=cal["dtau"], ages=AGES.tolist())
    for k, m in M.items():
        flux = (N * m).sum(axis=1) / 1e9                        # gain budgétaire de chaque année, Md€ courants réels
        va_budget = sum(flux[t] / (1 + r) ** (t - t0) for t in range(t0, T + 1))
        ind = va_individuelle(m, Q, r, t0)
        va_vivants = (N[t0] * ind).sum() / 1e9
        res[k] = dict(perte_par_age=ind.tolist(), flux_2026=flux[t0] / G[t0], flux_2030=flux[t0 + 4] / G[t0 + 4],
                      flux_2040=flux[t0 + 14] / G[t0 + 14], flux_2060=flux[t0 + 34] / G[t0 + 34],
                      va_budget=va_budget, va_vivants=va_vivants, part_vivants=va_vivants / va_budget,
                      va_par_tranche={f"{lo}-{hi}": float((N[t0, lo:hi + 1] * ind[lo:hi + 1]).sum() / 1e9)
                                      for lo, hi in ((0, 19), (20, 34), (35, 49), (50, 59), (60, 64), (65, 74), (75, 105))},
                      future_20_2026=va_generation_future(m, Q, r, t0, t0, 20),
                      future_naissance_2026=va_generation_future(m, Q, r, t0, t0, 0))
    res["ressources_par_age"] = ressources(pr, Q, r, g, t0).tolist()
    res["calage"] = dict(ky=pr["ky"], kp=pr["kp"], pensions_ref_2025=(N[0] * pr["p"]).sum() / 1e9,
                         assiette_ref_2025=(N[0] * pr["y"]).sum() / 1e9)
    if verbeux:
        audit(res)
    return res


def audit(res):
    print(f"r = {res['r']:.3f}, g = {res['g']:.3f} ; delta = {100 * res['delta']:.2f} % des pensions ; "
          f"dtau = {100 * res['dtau']:.2f} point de cotisation")
    print("calage :", {k: round(v, 3) for k, v in res["calage"].items()})
    for k in ("A", "B", "C", "C_salaire"):
        x = res[k]
        print(f"[{k}] flux Md€ 2025 : 2026 {x['flux_2026']:.1f} ; 2030 {x['flux_2030']:.1f} ; 2040 {x['flux_2040']:.1f} ;"
              f" 2060 {x['flux_2060']:.1f} | VA budget {x['va_budget']:.0f} | vivants {x['va_vivants']:.0f}"
              f" ({100 * x['part_vivants']:.0f} %) | futurs nés en 2026 : {x['future_naissance_2026']:.0f} €")
        print("    par tranche (Md€) :", {a: round(v) for a, v in x["va_par_tranche"].items()})
    print("âge  " + "".join(f"{k:>10}" for k in ("A", "B", "C", "C+sal", "ressources")))
    for a in range(20, 100, 5):
        print(f"{a:>3}  " + "".join(f"{res[k]['perte_par_age'][a]:>10.0f}" for k in ("A", "B", "C", "C_salaire"))
              + f"{res['ressources_par_age'][a]:>10.0f}")


if __name__ == "__main__":
    out = {}
    for r in (P["g"], 0.01, 0.02, 0.03):
        out[f"{r:.3f}"] = calculer(r=r, verbeux=(r == P["r"]))
    (D / "sorties" / "resultats.json").write_text(json.dumps(out, ensure_ascii=False), encoding="utf-8")
