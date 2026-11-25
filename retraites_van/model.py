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
def calage_cor(horizon=None):
    """Effet moyen des trois modèles du COR sur le solde primaire des APU (pt de PIB) et chocs ex ante (Md€) qui donnent
    à chaque levier le même effet sur le solde public que le recul d'un an de l'âge."""
    c = P["cor_2026"]
    h = c["horizons"].index(P["horizon_calage"] if horizon is None else horizon)
    moy = lambda d: float(np.mean([v[h] for v in d.values() if v[h] is not None]))  # noqa: E731
    E = {k: moy(v) for k, v in c["solde_apu"].items()}
    X = {k: c["choc_ex_ante_Md"] * E["age_un_an"] / E[k] for k in ("pensions", "cotis_salaries", "cotis_employeurs")}
    return dict(E=E, X=X, solde_retraites_age=moy(c["solde_retraites_age"]), emploi_age=moy(c["emploi_age_milliers"]) * 1e3,
                apu_Md=E["age_un_an"] / 100 * P["pib_2025"])


def reformes(pr, N, Q, r, g, horizon=None):
    """Variation, par tête, des transferts nets reçus (perte > 0), par année t (0 = année de base) et âge, pour quatre
    réformes de même effet sur le solde public (celui du recul d'un an de l'âge, moyenne des modèles du COR).
    Renvoie dict réforme -> matrice (T+1, AMAX), en euros de 2025 pour l'économie de l'année t, et le calage."""
    T = N.shape[0] - 1
    G = (1 + g) ** np.arange(T + 1)[:, None]
    Gp = croissance_pensions(T, g)[:, None]                        # pension par tête : COR, puis comme les salaires
    t0 = P["annee_reforme"] - P["annee_base"]
    actif = (np.arange(T + 1) >= t0)[:, None]
    y, p, pens, part = pr["y"], pr["p"], pr["pens"], pr["part"]
    cc = calage_cor(horizon)
    # A et B : chocs ex ante calés sur l'économie de 2025 (droit de référence)
    delta = cc["X"]["pensions"] / ((N[0] * p).sum() / 1e9)
    dts = cc["X"]["cotis_salaries"] / ((N[0] * y).sum() / 1e9)
    dte = cc["X"]["cotis_employeurs"] / ((N[0] * y).sum() / 1e9)   # incidence finale sur les salaires (COR)
    A = actif * delta * p[None, :] * Gp
    Bs = actif * dts * y[None, :] * G
    Be = actif * dte * y[None, :] * G
    # C : la part de retraités est décalée d'un an ; le profil des pensions perdues est mis à l'échelle de l'économie de
    # pensions déduite du COR (solde des retraites moins cotisations sur l'emploi supplémentaire)
    part_c = np.interp(AGES - P["decalage_age"], AGES, part)
    dshare = np.clip(part - part_c, 0, None)
    cotis = cc["emploi_age"] * P["salaire_brut_senior"] * P["taux_cotisation_retraite"] / 1e9
    eco_pensions = cc["solde_retraites_age"] / 100 * P["pib_2025"] - cotis
    lam = eco_pensions * 1e9 / (N[0] * dshare * pens).sum()
    pension_perdue = lam * dshare * pens
    w = P["part_compensee_autres_prestations"]
    perte = pension_perdue * (1 - w)                               # temps libre valant le salaire net
    emp_sup = dshare * cc["emploi_age"] / (N[0] * dshare).sum()    # emploi supplémentaire par tête à chaque âge
    sal_net = emp_sup * P["salaire_brut_senior"] * (1 - CAL["prelevements_salaries"]["valeur"])
    C, Cw = np.zeros_like(A), np.zeros_like(A)
    for t in range(t0, T + 1):
        touche = (AGES - (t - t0)) <= P["age_max_touche"]
        C[t] = touche * perte * Gp[t, 0]
        Cw[t] = touche * (perte * Gp[t, 0] - sal_net * G[t, 0])
    cal = dict(delta=delta, dtau_sal=dts, dtau_emp=dte, cotis_emploi_sup=cotis, eco_pensions=eco_pensions,
               perte_transferts_C=eco_pensions * (1 - w), **cc)
    return dict(A=A, B=Bs, B_emp=Be, C=C, C_salaire=Cw), cal


def croissance_pensions(T, g):
    """Indice de la pension par tête (base 2025) : +gp par an jusqu'à l'année pivot (COR : pension moyenne relative de
    54,6 % en 2025 à 45,3 % en 2070), puis comme le revenu d'activité."""
    gp, fin = P["croissance_pension_reelle"], P["annee_fin_decrochage"] - P["annee_base"]
    k = np.arange(T + 1)
    return np.where(k <= fin, (1 + gp) ** k, (1 + gp) ** fin * (1 + g) ** (k - fin))


def facteurs(r, t0, T, variante=None, flux="cotisations"):
    """Facteurs d'actualisation F[a, k] d'un flux reçu k ans après t0 par une personne d'âge a en t0.
    variante : None (taux r constant), "courbe" (taux réels de marché par maturité), "risque" (valeur de marché des flux
    indexés sur les salaires, à la Catherine-Miller-Sarin : prime de risque sur l'exposition aux salaires, jusqu'à la
    liquidation pour les pensions), "liquidite" (taux privé r + prime décroissante avec l'âge)."""
    K = np.arange(T - t0 + 1)
    F = np.empty((AMAX, K.size))
    if variante is None:
        F[:] = (1 + r) ** -K[None, :]
    elif variante == "courbe":
        c = P["courbe_reelle"]
        y = np.interp(K, c["maturites"], c["taux"])
        F[:] = (1 + y[None, :]) ** -K[None, :]
    elif variante == "risque":
        v = P["ajustement_risque"]
        kap, phi, erp = v["kappa"], v["phi"], v["prime_actions"]
        cum = lambda n: (1 - phi / kap) * (n - (1 - np.exp(-kap * n)) / kap)  # noqa: E731  intégrale de beta
        for a in range(AMAX):
            n = K if flux == "cotisations" else np.minimum(K, max(0, v["age_liquidation"] - a))
            F[a] = (1 + r) ** -K * np.exp(-erp * cum(n))
    elif variante == "liquidite":
        v = P["prime_liquidite"]
        for a in range(AMAX):
            ages = a + K
            prime = np.interp(ages, [v["age_debut"], v["age_fin"]], [v["prime"], 0.0])
            F[a] = np.concatenate([[1.0], np.cumprod(1 / (1 + r + prime[:-1]))])
    return F


def va_individuelle(M, Q, r, t0, F=None):
    """Perte actualisée espérée, à l'année t0, d'une personne de chaque âge a vivante en t0 (somme sur sa vie)."""
    T = M.shape[0] - 1
    out = np.zeros(AMAX)
    for a in range(AMAX):
        surv, tot = 1.0, 0.0
        for k in range(0, min(AMAX - a, T - t0 + 1)):
            t, s = t0 + k, a + k
            tot += surv * M[t, s] * (F[a, k] if F is not None else (1 + r) ** -k)
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
    M = pr["y"][None, :] * G + pr["p"][None, :] * croissance_pensions(T, g)[:, None]
    return va_individuelle(M, Q, r, t0)


def calculer(r=None, g=None, verbeux=False, actualisation=None):
    r = P["r"] if r is None else r
    g = P["g"] if g is None else g
    pop0, qx, emp, sal, part, pens = donnees()
    pr = profils(pop0, qx, emp, sal, part, pens)
    T = P["horizon"]
    N, Q = demographie(pop0, qx, T)
    M, cal = reformes(pr, N, Q, r, g)
    t0 = P["annee_reforme"] - P["annee_base"]
    G = (1 + g) ** np.arange(T + 1)
    res = dict(r=r, g=g, ages=AGES.tolist(), calage_reformes={k: v for k, v in cal.items()})
    for k, m in M.items():
        flux = (N * m).sum(axis=1) / 1e9                        # gain budgétaire de chaque année, Md€ courants réels
        va_budget = sum(flux[t] / (1 + r) ** (t - t0) for t in range(t0, T + 1))
        F = None
        if actualisation is not None:
            F = facteurs(r, t0, T, actualisation, "pensions" if k in ("A", "C", "C_salaire") else "cotisations")
        ind = va_individuelle(m, Q, r, t0, F)
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
    c = res["calage_reformes"]
    print(f"r = {res['r']:.3f}, g = {res['g']:.3f} ; effet APU visé {c['E']['age_un_an']:.3f} pt de PIB = {c['apu_Md']:.1f} Md€")
    print("  effets APU par 6 Md€ :", {k: round(v, 3) for k, v in c["E"].items()}, "; chocs ex ante (Md€) :",
          {k: round(v, 1) for k, v in c["X"].items()})
    print(f"  delta = {100 * c['delta']:.2f} % des pensions ; cotisations salariés + {100 * c['dtau_sal']:.2f} pt ;"
          f" employeurs + {100 * c['dtau_emp']:.2f} pt ; âge : économie de pensions {c['eco_pensions']:.1f} Md€,"
          f" cotisations sur l'emploi en plus {c['cotis_emploi_sup']:.1f} Md€, perte de transferts {c['perte_transferts_C']:.1f} Md€")
    print("calage :", {k: round(v, 3) for k, v in res["calage"].items()})
    for k in ("A", "B", "B_emp", "C", "C_salaire"):
        x = res[k]
        print(f"[{k}] flux Md€ 2025 : 2026 {x['flux_2026']:.1f} ; 2030 {x['flux_2030']:.1f} ; 2040 {x['flux_2040']:.1f} ;"
              f" 2060 {x['flux_2060']:.1f} | VA budget {x['va_budget']:.0f} | vivants {x['va_vivants']:.0f}"
              f" ({100 * x['part_vivants']:.0f} %) | futurs nés en 2026 : {x['future_naissance_2026']:.0f} €")
        print("    par tranche (Md€) :", {a: round(v) for a, v in x["va_par_tranche"].items()})
    print("âge  " + "".join(f"{k:>10}" for k in ("A", "B", "B_emp", "C", "C+sal", "ressources")))
    for a in range(20, 100, 5):
        print(f"{a:>3}  " + "".join(f"{res[k]['perte_par_age'][a]:>10.0f}" for k in ("A", "B", "B_emp", "C", "C_salaire"))
              + f"{res['ressources_par_age'][a]:>10.0f}")


if __name__ == "__main__":
    out = {}
    for r in (P["g"], 0.01, 0.02, 0.03):
        out[f"{r:.3f}"] = calculer(r=r, verbeux=(r == P["r"]))
    (D / "sorties" / "resultats.json").write_text(json.dumps(out, ensure_ascii=False), encoding="utf-8")
