"""Bloc IR-CSG v4 (révision finale) : recette des niches par dispositif, frais professionnels, barème recalé, gagnants et
perdants nets des niches par catégorie, efficacité, trajectoire. Lancer depuis fiscalite/ :
    python3 note8p/calculs/ircsg4_modele.py
Sorties : note8p/sorties/ircsg4.json (clés listées en fin de script), ircsg4_calculs.txt.

Ce qui change par rapport à la v3 (ircsg3_*.py, réutilisés sans modification) :
1. Le « résidu » de 27,1 Md€ (droit 2025 simulé sans niche − impôt observé) n'est plus assimilé à une recette. Il est
   décomposé point par point du modèle : (a) frais réels au-delà du forfait (modèle de frais, ircsg4_frais) ; (b) niches
   supprimées, réparties selon les données du CPO (répartition du coût de chaque dispositif par groupe de RFR par part et
   entre moins et plus de 65 ans) ; (c) avantages gardés ou non supprimables (revenus de source étrangère, engagements
   Pinel en cours, dépendance, invalidité) ; (d) écart inexpliqué (représentation des ménages, revenus, périmètres).
   Seul (b) finance la réforme ; (c) et (d), s'il est positif, sont retirés de la recette du nouvel impôt simulé.
2. Recettes hors modèle : épargne salariale, indemnités journalières exonérées, impatriés (revenus absents de l'assiette
   du modèle) ; IR non attribué : la moitié des 4,0 Md€ est supposée relever du barème et doit être tenue [H prudente].
3. Frais professionnels : le forfait de 10 % est remplacé par l'option recommandée (forfait fixe, frais réels au-delà),
   avec une estimation de la hausse des frais réels déclarés.
4. Barème : forme continue et repères conservés ; ajustement uniforme des taux aux points 0 à 3,5 Smic.
"""
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import ircsg3_modele as N  # noqa: E402
import ircsg3_droit as DR  # noqa: E402
import ircsg3_cascade as C  # noqa: E402
import ircsg4_donnees as D4  # noqa: E402
import ircsg4_frais as FR4  # noqa: E402

M, R = N.M, N.R
O = N.options()
OUT = N.SORTIES
V3 = json.loads((OUT / "ircsg3.json").read_text(encoding="utf-8"))
P0, T0 = V3["final"]["points"], list(V3["final"]["taux"])
FIN = 5.5
PALIERS = {2032: 1.0, 2033: 2.0, 2034: 3.0, 2035: 4.0, 2036: 5.0}
MONTEE = {2027: 0.25, 2028: 0.5, 2029: 0.75}
IR_NON_ATTRIBUE, PART_PRUDENTE = 4.0, 0.0   # couvert par l'écart inexpliqué retiré (voir en-tête)
L, J = [], {}


def p(s=""):
    print(s, flush=True)
    L.append(s)


TYPES = M.TYPES
NPT = len(M.Q)
WTOT = M.W.sum()


def somme(d, filtre=lambda n, g, f, k: True):
    return sum((w * d[n]).sum() for n, g, f, w, pp, k in TYPES if filtre(n, g, f, k)) / 1e9


# ================================================================== 1. frais professionnels
ADULTES = []           # (type, k, poids, salaire net imposable)
for n, g, f, w, pp, k in TYPES:
    if g != "A":
        continue
    for j, sh in enumerate(pp):
        z = sh * M.SAL_A
        ADULTES.append((n, j, w, z * (1 - 0.068 * 0.9825 / M.R_A)))
PW = np.concatenate([a[2] for a in ADULTES])
PWI = np.concatenate([a[3] for a in ADULTES])
_ok = PWI > 500
err, SIG, GT, ACT = FR4.calage(PW[_ok], PWI[_ok])
p(f"[FRAIS] calage : σ = {SIG:.2f}, seuil de gain {GT:.0f} € ; droit actuel simulé : {ACT['declarants_M']:.2f} M de"
  f" déclarants (cible {FR4.CIBLE_N / 1e6:.2f}), {ACT['frais_reels_Md']:.1f} Md€ de frais réels (cible {FR4.CIBLE_MD:.1f}),"
  f" forfait {ACT['forfait_Md']:.1f} Md€")


def ded_par_adulte(option, tau_new=None):
    """Déduction moyenne par adulte (tableau aligné sur ADULTES) et part de déclarants, pour une option."""
    D, P, F = FR4.profils(option, SIG, GT, tau_new)
    return [np.interp(a[3], FR4.GRID, D) * (a[3] > 500) for a in ADULTES], [np.interp(a[3], FR4.GRID, P) * (a[3] > 500)
                                                                             for a in ADULTES]


def ded_par_point(ded):
    """Déduction moyenne par foyer d'actifs de chaque point (moyenne pondérée sur les types) : le modèle répartit
    ensuite cette déduction entre adultes au prorata de leur revenu (approximation)."""
    num, den = np.zeros(NPT), np.zeros(NPT)
    for (n, j, w, wi), d in zip(ADULTES, ded):
        num += w * d
    for n, g, f, w, pp, k in TYPES:
        if g == "A":
            den += w
    return num / np.maximum(den, 1e-9)


# ================================================================== 2. décomposition du résidu (27,1 Md€)
OBS = {n: M.CURT[n] for n, *_ in TYPES}
SIMF = C.charges({})                                   # droit 2025 sans niche, forfait de 10 % pour tous (v3, étape 1)
ded_act, _ = ded_par_adulte(("actuel",))
DED_ACT = {}
for (n, j, w, wi), d in zip(ADULTES, ded_act):
    DED_ACT.setdefault(n, {})[j] = d
SIMA = {}
for n, g, f, w, pp, k in TYPES:
    ad, fr, per = C._foyer(g, pp, {})
    if g == "A":
        # frais réels attendus sur la part salariale ; forfait de 10 % sur le reste du revenu (comme dans SIMF)
        fr = []
        for j, sh in enumerate(pp):
            x = sh * M.ZNA * (1 - 0.068 * 0.9825 / M.R_A) - (per[j] if per is not None else 0)
            ws = sh * M.SAL_A * (1 - 0.068 * 0.9825 / M.R_A)
            fr.append(DED_ACT[n][j] + np.minimum(np.clip(0.10 * np.clip(x - ws, 0, None), 0, None), 14555.0))
        SIMA[n] = DR.charge(ad, k, n.startswith("parent_isole"), dict(forfait=False), frais_reels=fr, deduc=per)["total"]
    else:
        SIMA[n] = SIMF[n]
FREX = {n: SIMF[n] - SIMA[n] for n in SIMF}            # frais réels au-delà du forfait (impôt), droit actuel
IRSIM = {}
TAUIR = {}
for n, g, f, w, pp, k in TYPES:
    ad, fr, per = C._foyer(g, pp, {})
    IRSIM[n] = DR.charge(ad, k, n.startswith("parent_isole"), {}, frais_reels=fr, deduc=per)["ir"]
    if g == "A":
        ad2 = [(a[0], a[1] * 1.01, a[2]) for a in ad]
        ir2 = DR.charge(ad2, k, n.startswith("parent_isole"), {}, frais_reels=fr, deduc=per)["ir"]
        TAUIR[n] = np.clip((ir2 - IRSIM[n]) / (0.01 * sum(a[1] for a in ad)), 0, 0.5)
    else:
        TAUIR[n] = 0 * M.Q

POP = D4.population_par_age()
GRP = np.select([M.Q < b[1] for b in D4.BORNES_C[:-1]], range(4), 4)
VM = {r[0]: r[2] for r in D4.TABLEAU}


def repartit(cout, partsC, rho, eligible=lambda n, g, f, k: True, poids=None):
    """Coût (Md€) réparti par groupe C (parts en %) et entre actifs (1 − rho) et retraités (rho), également entre foyers
    éligibles d'une même cellule (ou au prorata de `poids(n)` s'il est donné). Renvoie dict type -> € par foyer."""
    s = np.asarray(partsC, float) / np.sum(partsC)
    out = {n: 0 * M.Q for n, *_ in TYPES}
    for grp, part in (("A", 1 - rho), ("R", rho)):
        if part <= 0:
            continue
        el = [(n, w, (poids(n) if poids else 1.0 + 0 * M.Q)) for n, g, f, w, pp, k in TYPES if g == grp and eligible(n, g, f, k)]
        for c in range(5):
            m = GRP == c
            den = sum((w * pw * m).sum() for n, w, pw in el)
            if den <= 0:
                continue
            for n, w, pw in el:
                out[n] = out[n] + m * pw * cout * 1e9 * part * s[c] / den
    return out


ENF = lambda n, g, f, k: k > 0  # noqa: E731
RI_C, CI_C = D4.CPO_T15["reductions"], D4.CPO_T15["credits"]
NICHES = {   # clé -> (€ par foyer et par type, supprimée ?)
    "emploi_domicile": (repartit(VM["emploi_domicile"], D4.FICHES["emploi_domicile"]["repC"],
                                 D4.part_retraites("emploi_domicile", POP)), True),
    "garde": (repartit(VM["garde"], D4.FICHES["garde"]["repC"], 0.0, ENF), True),
    "dons": (repartit(VM["dons"], D4.FICHES["dons"]["repC"], D4.part_retraites("dons", POP)), True),
    "outre_mer": (repartit(VM["outre_mer"], D4.FICHES["outre_mer"]["repC"], D4.part_retraites("outre_mer", POP)), True),
    "scolarite": (repartit(VM["scolarite"], D4.FICHES["scolarite"]["repC"], 0.0, ENF), True),
    "pme": (repartit(VM["pme"], RI_C, D4.part_retraites("pme", POP)), True),
    "syndicales": (repartit(VM["syndicales"], CI_C, 0.0), True),
    "prestation_comp": (repartit(VM["prestation_comp"], RI_C, 0.3), True),
    "autres_rici_supp": (repartit(0.55 * VM["autres_rici"], RI_C, 0.2), True),
    "dom": (repartit(VM["dom"], D4.CPO_T15["impot_avant_rici"], 0.3), True),
    "locatif_stock": (repartit(VM["locatif_stock"], D4.FICHES["locatif"]["repC"], D4.part_retraites("locatif", POP)), False),
    "autres_rici_garde": (repartit(0.45 * VM["autres_rici"], RI_C, 0.2), False),
    "source_etrangere": (repartit(0.5 * VM["source_etrangere"], D4.CPO_T15["double_imposition"], 0.3), False),
    "dependance": (repartit(VM["dependance"], D4.FICHES["dependance"]["repC"], D4.part_retraites("dependance", POP)), False),
}
# heures supplémentaires : actifs, au prorata des salaires × taux marginal d'IR (HS déclarées 21,8 Md€, 1GH à 1JH) [H]
_hs = {n: (M.SAL_A * TAUIR[n] if g == "A" else 0 * M.Q) for n, g, f, w, pp, k in TYPES}
_k = VM["heures_sup"] * 1e9 / sum((w * _hs[n]).sum() for n, g, f, w, pp, k in TYPES)
NICHES["heures_sup"] = ({n: _k * v for n, v in _hs.items()}, True)
# demi-parts (vivant seul ayant élevé un enfant, anciens combattants, veufs) : retraités seuls, au prorata de min(IR, 1 100 €)
_dp = {n: (np.minimum(IRSIM[n], 1100.0) if n == "retraite_seul" else 0 * M.Q) for n, *_ in TYPES}
_k = VM["demi_parts"] * 1e9 / sum((w * _dp[n]).sum() for n, g, f, w, pp, k in TYPES)
NICHES["demi_parts"] = ({n: _k * v for n, v in _dp.items()}, True)
# demi-parts des invalides (gardées) : tous les foyers, au prorata de min(IR, 1 900 €)
_iv = {n: np.minimum(IRSIM[n], 1900.0) for n, *_ in TYPES}
_k = VM["demi_part_invalides"] * 1e9 / sum((w * _iv[n]).sum() for n, g, f, w, pp, k in TYPES)
NICHES["demi_part_invalides"] = ({n: _k * v for n, v in _iv.items()}, False)
# niches hors modèle (revenus exonérés absents de l'assiette du modèle) : actifs, au prorata des salaires [H] ;
# épargne salariale concentrée sur la moitié haute (grandes entreprises) [H]
_es = {n: (M.SAL_A * (0.5 + M.Q) if g == "A" else 0 * M.Q) for n, g, f, w, pp, k in TYPES}
HORS = {}
for cle in ("epargne_salariale", "ij_ald", "impatries"):
    part = [r for r in D4.TABLEAU if r[0] == cle][0][6]
    base = _es if cle == "epargne_salariale" else ({n: _es[n] * (M.Q >= 0.99) for n in _es} if cle == "impatries" else
                                                    {n: (M.SAL_A if g == "A" else 0 * M.Q) for n, g, *_ in TYPES})
    kk = part * VM[cle] * 1e9 / sum((w * base[n]).sum() for n, g, f, w, pp, k in TYPES)
    HORS[cle] = {n: kk * v for n, v in base.items()}

SUPP = {n: sum(v[n] for v, s in NICHES.values() if s) for n, *_ in TYPES}
GARD = {n: sum(v[n] for c, (v, s) in NICHES.items() if not s and c in ("dependance", "demi_part_invalides")) for n, *_ in TYPES}
KEPT = {n: sum(v[n] for c, (v, s) in NICHES.items() if not s and c not in ("dependance", "demi_part_invalides")) for n, *_ in TYPES}
HSUP = {n: sum(v[n] for v in HORS.values()) for n, *_ in TYPES}
RES = {n: SIMF[n] - OBS[n] for n in SIMF}
UNEX = {n: RES[n] - FREX[n] - SUPP[n] - GARD[n] - KEPT[n] for n in RES}


def par_decile(d):
    tot = sum(w * d[n] for n, g, f, w, pp, k in TYPES)
    return [float(v) for v in (pd.Series(tot).groupby(M.DEC).sum() / 1e9).values]


DECOMP = {}
for cle, d in (("residu", RES), ("frais_reels_au_dela_du_forfait", FREX), ("niches_supprimees", SUPP),
               ("gardees_invalidite_dependance", GARD), ("non_supprimables_ou_stock", KEPT), ("ecart_inexplique", UNEX),
               ("niches_hors_modele", HSUP)):
    DECOMP[cle] = dict(Md=somme(d), actifs=somme(d, lambda n, g, f, k: g == "A"), retraites=somme(d, lambda n, g, f, k: g == "R"),
                       deciles_Md=par_decile(d), top1_Md=sum((w * d[n] * (M.Q >= 0.99)).sum() for n, g, f, w, pp, k in TYPES) / 1e9)
PAR_DISP = {c: dict(Md=somme(v), supprimee=s, actifs=somme(v, lambda n, g, f, k: g == "A"), deciles_Md=par_decile(v))
            for c, (v, s) in NICHES.items()}
for c, v in HORS.items():
    PAR_DISP[c] = dict(Md=somme(v), supprimee=True, hors_modele=True, actifs=somme(v), deciles_Md=par_decile(v))
p("\n[RÉSIDU] décomposition (Md€ 2025) ; part du 10e décile")
for c, d in DECOMP.items():
    p(f"  {c:34s} {d['Md']:+6.2f} | actifs {d['actifs']:+6.2f} retraités {d['retraites']:+6.2f} | D10 {d['deciles_Md'][-1]:+6.2f}"
      f" ({100 * d['deciles_Md'][-1] / d['Md'] if d['Md'] else 0:.0f} %) | D1-5 {sum(d['deciles_Md'][:5]):+5.2f}")
p("  par décile, résidu : " + " ".join(f"{x:.1f}" for x in DECOMP["residu"]["deciles_Md"]))
p("  par décile, niches supprimées : " + " ".join(f"{x:.2f}" for x in DECOMP["niches_supprimees"]["deciles_Md"]))
p("  par décile, écart inexpliqué : " + " ".join(f"{x:.2f}" for x in DECOMP["ecart_inexplique"]["deciles_Md"]))

# ================================================================== 3. recette à tenir et barème recalé
U_TOT = DECOMP["ecart_inexplique"]["Md"]
CORR = DECOMP["non_supprimables_ou_stock"]["Md"] + max(U_TOT, 0.0)
HORS_MD = DECOMP["niches_hors_modele"]["Md"]
PRUD = PART_PRUDENTE * IR_NON_ATTRIBUE
import os
W_UNI = np.array([float(x) for x in os.environ.get("W_AJ", "1,1,1,1,1,0").split(",")])
DED_PER0 = N.DED_PER0


def regle_frais(option, sched):
    ded, part = ded_par_adulte(option, tau_new=lambda w: float(sched[0](w)))
    return ded, part


def applique_frais(ded):
    dp = ded_par_point(ded)
    M.DED_PER = DED_PER0 + dp
    N.FR = dp                         # utilisé par la cascade (étape « forfait »)
    return dp


def bareme(d):
    return N.continu(P0, list(np.array(T0) + d * W_UNI))


def cale(cible, lo=-0.03, hi=0.05):
    for _ in range(40):
        m = (lo + hi) / 2
        lo, hi = (m, hi) if N.recette(bareme(m), O) < cible else (lo, m)
    return (lo + hi) / 2


def cible(F):
    return N.CIBLE + CORR - HORS_MD + PRUD - F


OPTIONS = {"actuel_v3": None, "suppression": ("suppression",), "fixe_500": ("fixe", 500.0), "fixe_1000": ("fixe", 1000.0),
           "pct5_plaf2000": ("pct", 0.05, 2000.0), "franchise_1000": ("franchise", 1000.0)}
S3 = N.continu(P0, T0)
FRAIS = {}
p("\n[FRAIS] options (barème v3 final pour le gain de déclaration) : déduction totale, frais réels déclarés, déclarants ;"
  " point de barème uniforme nécessaire à recette égale")
for k, opt in OPTIONS.items():
    if opt is None:
        M.DED_PER = DED_PER0 + N.FR
        dp = N.FR
        a = dict(deduction_Md=float((M.W_A * N.FR).sum() / 1e9), declarants_M=FR4.CIBLE_N / 1e6, frais_reels_Md=FR4.CIBLE_MD)
    else:
        ded, part = regle_frais(opt, S3)
        dp = applique_frais(ded)
        a = dict(deduction_Md=float(sum((pw * d).sum() for (n, j, pw, wi), d in zip(ADULTES, ded)) / 1e9),
                 declarants_M=float(sum((pw * q).sum() for (n, j, pw, wi), q in zip(ADULTES, part)) / 1e6))
        D_, P_, F_ = FR4.profils(opt, SIG, GT, lambda w: float(S3[0](w)))
        a["frais_reels_Md"] = float(sum((pw * np.interp(wi, FR4.GRID, F_) * (wi > 500)).sum() for (n, j, pw, wi) in ADULTES) / 1e9)
    a["recette_bareme_v3_Md"] = N.recette(S3, O)
    FRAIS[k] = a
    p(f"  {k:14s} déduction {a['deduction_Md']:5.1f} Md€ ; frais réels {a['frais_reels_Md']:5.1f} ; déclarants"
      f" {a['declarants_M']:5.1f} M ; recette au barème v3 {a['recette_bareme_v3_Md']:.2f}")
base_v3 = FRAIS["actuel_v3"]["recette_bareme_v3_Md"]
for k in FRAIS:
    FRAIS[k]["cout_vs_v3_Md"] = base_v3 - FRAIS[k]["recette_bareme_v3_Md"]
    FRAIS[k]["cout_vs_suppression_Md"] = FRAIS["suppression"]["recette_bareme_v3_Md"] - FRAIS[k]["recette_bareme_v3_Md"]
# sensibilité : recours deux fois moins élastique (seuil de gain doublé) en cas de suppression du forfait
_gt = GT
GT = 2 * _gt
ded, part = regle_frais(("suppression",), S3)
applique_frais(ded)
FRAIS["suppression_recours_faible"] = dict(deduction_Md=float(sum((pw * d).sum() for (n, j, pw, wi), d in zip(ADULTES, ded)) / 1e9),
                                           declarants_M=float(sum((pw * q).sum() for (n, j, pw, wi), q in zip(ADULTES, part)) / 1e6),
                                           recette_bareme_v3_Md=N.recette(S3, O))
FRAIS["suppression_recours_faible"]["cout_vs_v3_Md"] = base_v3 - FRAIS["suppression_recours_faible"]["recette_bareme_v3_Md"]
p(f"  sensibilité (seuil de gain doublé) : déduction {FRAIS['suppression_recours_faible']['deduction_Md']:.1f} Md€,"
  f" {FRAIS['suppression_recours_faible']['declarants_M']:.1f} M de déclarants, coût {FRAIS['suppression_recours_faible']['cout_vs_v3_Md']:.2f}")
GT = _gt
FRAIS["calage"] = dict(sigma=float(SIG), seuil_gain=float(GT), simule=ACT, cible_declarants_M=FR4.CIBLE_N / 1e6,
                       cible_Md=FR4.CIBLE_MD)
OPTION = os.environ.get("OPTION_FRAIS", "suppression")   # recommandée [C]
# itération : le gain de déclaration dépend du barème final
S = S3
for _ in range(3):
    ded, part = regle_frais(OPTIONS[OPTION], S)
    applique_frais(ded)
    DFIN = cale(cible(FIN))
    S = bareme(DFIN)
D0 = cale(cible(0.0))
S0 = bareme(D0)
TT = list(np.array(T0) + DFIN * W_UNI)
p(f"\n[BARÈME] recette à tenir : cible v3 {N.CIBLE:.2f} + avantages gardés ou non supprimables {DECOMP['non_supprimables_ou_stock']['Md']:.2f}"
  f" + écart inexpliqué {max(U_TOT, 0):.2f} − recettes hors modèle {HORS_MD:.2f} + IR non attribué (moitié) {PRUD:.2f}"
  f" − financement {FIN} = {cible(FIN):.2f} ; frais : {OPTION}")
p(f"  ajustement uniforme {100 * DFIN:+.2f} point (à recette constante, sans financement : {100 * D0:+.2f}) ; taux"
  f" {[round(100 * x, 2) for x in TT]} aux points {[round(x) for x in P0]}")

# ================================================================== 3 bis. version finale : 7,0 Md€ de financement externe
# Décision de l'assembleur (19/11/2026, suppression du CIR) : 1,5 Md€ de 2029 à 2034, 2,5 de 2035 à 2037, 4,5 en 2038,
# 6,0 en 2039, 7,0 dès 2040. Priorités : (1) taux moyens nettement moins progressifs que le droit actuel (écart de taux
# moyen Smic – 200 k€) sans toucher au Smic ni aux taux entre 0,6 et 1,1 Smic ; (2) minimum vieillesse (ASPA calculée
# sur la pension nette du nouvel impôt) ; (3) le reste sur le bas et le milieu. Le moyen le moins coûteux de réduire
# l'écart à 200 k€ est d'atteindre le plafond de 48 % plus haut (exploration : ircsg4_modele, section 3 bis) ; les taux
# aux points 0 à 3,5 Smic de la version à 5,5 Md€ sont gardés.
S5, TT5, DFIN5 = S, TT, DFIN
FIN_TOT = 7.0
PALIERS = {**{a: 1.5 for a in range(2029, 2035)}, **{a: 2.5 for a in range(2035, 2038)}, 2038: 4.5, 2039: 6.0}
ASPA_PLAF, ASPA_ALLOC, ASPA_RECOURS = 12411.44, 752800, 0.5   # plafond 2025 ; allocataires fin 2024 (DREES, MS 2025,
# fiche 28) ; la moitié des personnes seules éligibles le perçoivent (DREES, fin 2016)


def aspa_cout(sched):
    """Coût (Md€) d'une ASPA calculée sur la pension nette du nouvel impôt : (a) allocataires actuels, dont la pension
    propre est supposée uniformément répartie entre 0 et le plafond [H : pension de droit direct moyenne 510 €/mois,
    DREES] : l'ASPA compense leur impôt ; (b) nouveaux éligibles (pension entre le plafond et le plafond + impôt),
    retraités seuls du modèle, avec un recours de 50 % (bas) à 100 % (haut)."""
    ps = np.linspace(0, ASPA_PLAF, 401)
    stock = ASPA_ALLOC * float(np.mean(N.impot_z(sched, O, [ps]))) / 1e9
    w = [t[3] for t in TYPES if t[0] == "retraite_seul"][0]
    pz = M.ZNG["R"]
    t = N.impot_z(sched, O, [pz])
    gain = np.clip(ASPA_PLAF - (pz - t), 0, None) * (pz > ASPA_PLAF)
    ent = float((w * gain).sum()) / 1e9
    return dict(stock=stock, entrants_plein_recours=ent, central=stock + ASPA_RECOURS * ent, bas=0.9 * stock + 0.5 * ent,
                haut=1.1 * stock + ent)


def design(zp):
    return N.continu(P0[:5] + [zp], TT5)


def cale_zp(F):
    lo, hi = P0[5], 5e6
    for _ in range(50):
        m = (lo + hi) / 2
        lo, hi = (m, hi) if N.recette(design(m), O) > cible(F) else (lo, m)
    return (lo + hi) / 2


def ecart(sched, z=200e3, zs=19176.48):
    return 100 * (float(sched[1](z)) / z - float(sched[1](zs)) / zs)


ASPA_C = aspa_cout(S5)
F_BAR = FIN_TOT - ASPA_C["central"]
ZP = cale_zp(F_BAR)
ZP_TOUT = cale_zp(FIN_TOT)
VARIANTES = {}
for cible_ecart in (24.0, 23.5):
    lo, hi = P0[5], 5e6
    for _ in range(50):
        m = (lo + hi) / 2
        lo, hi = (m, hi) if ecart(design(m)) > cible_ecart else (lo, m)
    VARIANTES[str(cible_ecart)] = dict(zp=(lo + hi) / 2, financement_bareme=cible(0.0) - N.recette(design((lo + hi) / 2), O))
# Arbitrage final de l'assembleur (« bas et milieu ») : coût d'opportunité trop élevé de la progressivité par le haut ;
# point haut gardé à 163 400 € ; le financement restant baisse les taux aux repères 0 à 3,5 Smic (poids 1/1/1/1/0,5) ;
# les autres pondérations essayées (uniforme, sans le premier euro, sans 3,5 Smic) donnent les mêmes résultats à
# 0,1 point près.
W_BM = np.array([1.0, 1.0, 1.0, 1.0, 0.5, 0.0])
ZP_EXPLORE, S_EXPLORE = ZP, design(ZP)


def bm(e):
    return N.continu(P0, list(np.array(TT5) - e * W_BM))


_lo, _hi = 0.0, 0.05
for _ in range(45):
    _m = (_lo + _hi) / 2
    _lo, _hi = (_m, _hi) if N.recette(bm(_m), O) > cible(F_BAR) else (_lo, _m)
E_BM = (_lo + _hi) / 2
S = bm(E_BM)
P_FIN = list(P0)
TT = list(np.array(TT5) - E_BM * W_BM)
ZP = P0[5]
FIN = F_BAR
p(f"  [ARBITRAGE « bas et milieu »] baisse {100 * E_BM:.2f} point (poids 1/1/1/1/0,5) ; taux {[round(100 * x, 2) for x in TT]} ;"
  f" écart Smic–200 k€ {ecart(S):.1f} points (droit actuel 26,8)")
p(f"\n[FINAL 7,0 Md€] ASPA nette : {ASPA_C['central']:.2f} Md€ (fourchette {ASPA_C['bas']:.2f}–{ASPA_C['haut']:.2f} ;"
  f" allocataires {ASPA_C['stock']:.2f}, nouveaux éligibles à plein recours {ASPA_C['entrants_plein_recours']:.2f}) ;"
  f" barème {F_BAR:.2f} Md€ : plafond de 48 % atteint à {ZP:,.0f} € (au lieu de {P0[5]:,.0f}) ; écart de taux moyen"
  f" Smic–200 k€ {ecart(S5):.1f} → {ecart(S):.1f} points (droit actuel 26,8) ; tout sur la progressivité (7,0) :"
  f" plafond à {ZP_TOUT:,.0f} €, écart {ecart(design(ZP_TOUT)):.1f} ; pour 24 points : plafond à"
  f" {VARIANTES['24.0']['zp']:,.0f} €, {VARIANTES['24.0']['financement_bareme']:.1f} Md€ ; pour 23,5 :"
  f" {VARIANTES['23.5']['zp']:,.0f} €, {VARIANTES['23.5']['financement_bareme']:.1f} Md€")

# ================================================================== 4. distribution : nouveau système, niches, net
NEW = {n: R.impot_adultes(*S, O, *M.adultes(g, pp, O), k)[0] for n, g, f, w, pp, k in TYPES}
NEW0 = {n: R.impot_adultes(*S0, O, *M.adultes(g, pp, O), k)[0] for n, g, f, w, pp, k in TYPES}
_c = {n: (0.03 * np.clip(np.minimum(M.ZNG[g], 5e5) - 2.5e5, 0, None) + 0.04 * np.clip(M.ZNG[g] - 5e5, 0, None))
      for n, g, *_ in TYPES}
_k = R.CEHR_BAR * 1e9 / sum((w * _c[n]).sum() for n, g, f, w, pp, k in TYPES)
CEHR_I = {n: _k * v for n, v in _c.items()}                   # CEHR due aujourd'hui sur les revenus du barème (absorbée)
GAIN = {n: NEW[n] - SIMF[n] + FREX[n] - CEHR_I[n] for n in NEW}   # gain du nouveau système (hors niches individuelles)
PERTE = {n: SUPP[n] + HSUP[n] for n in NEW}                  # perte des niches supprimées
NET = {n: GAIN[n] + PERTE[n] for n in NEW}
p(f"\n[CONTRÔLE] Σ net = {somme(NET):+.2f} Md€ (attendu : −financement {FIN} + recettes hors modèle déjà retirées"
  f" ⇒ {-FIN:+.2f} à l'écart de calage près)")


def cat_moy(filtre, d):
    num = sum((w * d[n]).sum() for n, g, f, w, pp, k in TYPES if filtre(n, g, f, k))
    den = sum(w.sum() for n, g, f, w, pp, k in TYPES if filtre(n, g, f, k))
    return num / den if den else float("nan"), den / 1e6


CATS = {"Tous les foyers": lambda n, g, f, k: True, "Actifs": lambda n, g, f, k: g == "A",
        "Retraités": lambda n, g, f, k: g == "R",
        "Actifs seuls sans enfant": lambda n, g, f, k: g == "A" and f == "seuls",
        "Couples d'actifs sans enfant": lambda n, g, f, k: g == "A" and f == "couples0",
        "Couples, 1 enfant": lambda n, g, f, k: f == "couples2" and k == 1,
        "Couples, 2 enfants": lambda n, g, f, k: f == "couples2" and k == 2,
        "Couples, 3 enfants ou plus": lambda n, g, f, k: f == "couples2" and k >= 3,
        "Couples à un seul revenu (avec ou sans enfant)": lambda n, g, f, k: g == "A" and n.endswith("_1.0"),
        "Parents isolés": lambda n, g, f, k: f == "parents_isoles",
        "Retraités seuls": lambda n, g, f, k: g == "R" and f == "seuls",
        "Couples de retraités": lambda n, g, f, k: g == "R" and f == "couples0"}
MOY = {}
for c, flt in CATS.items():
    gnew, nb = cat_moy(flt, GAIN)
    MOY[c] = dict(foyers_M=nb, gain_systeme=gnew, perte_niches=cat_moy(flt, PERTE)[0], net=cat_moy(flt, NET)[0])
DECS = []
for dcl in range(10):
    flt = lambda n, g, f, k, dcl=dcl: True  # noqa: E731
    num = {x: sum((w * d[n] * (M.DEC == dcl)).sum() for n, g, f, w, pp, k in TYPES) for x, d in
           (("gain", GAIN), ("perte", PERTE), ("net", NET))}
    den = sum((w * (M.DEC == dcl)).sum() for n, g, f, w, pp, k in TYPES)
    act = sum((w * (M.DEC == dcl)).sum() for n, g, f, w, pp, k in TYPES if g == "A") / den
    DECS.append(dict(decile=dcl + 1, gain_systeme=num["gain"] / den, perte_niches=num["perte"] / den, net=num["net"] / den,
                     part_actifs=act))
p("\n[MOYENNES] € par foyer et par an : gain du nouveau système (− = baisse) / perte des niches (+) / net")
for c, v in MOY.items():
    p(f"  {c:46s} {v['foyers_M']:5.1f} M : {v['gain_systeme']:+7.0f} / {v['perte_niches']:+6.0f} / {v['net']:+7.0f}")
for v in DECS:
    p(f"  D{v['decile']:<2d} (actifs {100 * v['part_actifs']:.0f} %) : {v['gain_systeme']:+7.0f} / {v['perte_niches']:+6.0f} / {v['net']:+7.0f}")

# sous-groupes : bénéficiaires d'un dispositif, par décile (montant conditionnel = coût de la cellule / bénéficiaires)
BENEF = {"emploi_domicile": D4.FICHES["emploi_domicile"]["benef"], "garde": D4.FICHES["garde"]["benef"],
         "dons": D4.FICHES["dons"]["benef"], "outre_mer": D4.FICHES["outre_mer"]["benef"]}
SOUS = {}
for c, nb in BENEF.items():
    v = NICHES[c][0]
    tot = sum((w * v[n]).sum() for n, g, f, w, pp, k in TYPES)
    # montant moyen par bénéficiaire national (VM 2025 / bénéficiaires 2024) ; croissant avec le groupe C de sorte que
    # la fréquence de recours ne dépasse 60 % dans aucune cellule [H] ; la fréquence s'en déduit
    rows = []
    for dcl in range(10):
        for grp in ("A", "R"):
            cout = sum((w * v[n] * (M.DEC == dcl)).sum() for n, g, f, w, pp, k in TYPES if g == grp)
            fo = sum((w * (M.DEC == dcl)).sum() for n, g, f, w, pp, k in TYPES if g == grp)
            if fo <= 0 or cout <= 0:
                continue
            moy = VM[c] * 1e9 / nb
            m = max(moy, cout / (0.6 * fo))
            sel = [(w, n) for n, g, f, w, pp, k in TYPES if g == grp and (v[n] * (M.DEC == dcl)).sum() > 0]
            gs = sum((w * GAIN[n] * (M.DEC == dcl)).sum() for w, n in sel) / sum((w * (M.DEC == dcl)).sum() for w, n in sel)
            rows.append(dict(decile=dcl + 1, groupe=grp, frequence=cout / m / fo, perte_beneficiaire=m, gain_systeme=gs,
                             net_beneficiaire=gs + m))
    SOUS[c] = rows
p("\n[SOUS-GROUPES] bénéficiaires (fréquence, perte moyenne du seul dispositif, net = gain système + perte ; €/an)")
for c, rows in SOUS.items():
    p(f"  {c}: " + " | ".join(f"D{r['decile']}{r['groupe']} {100 * r['frequence']:.0f} % {r['perte_beneficiaire']:.0f}"
                               f" → {r['net_beneficiaire']:+.0f}" for r in rows if r["decile"] in (2, 5, 8, 10)))

# ================================================================== 5. efficacité et taux
EV = N.evalue(S, O, repart=True)
EFF = {}
for j in ("bas", "central", "haut"):
    e = N.evalue(S, O, jeu=j)
    EFF[j] = dict(gain_Md=e["gain"], intensif=-e["reel"], extensif=-e["ext"], emplois_milliers=e["emplois"] / 1e3,
                  **{kk: vv for kk, vv in R.effets_reels(e).items() if kk in ("travail_pct", "etp_milliers")})
p("\n[EFFICACITÉ] gain d'efficacité statique lié à la modification des incitations fiscales au travail (hors effets"
  " propres aux dispositifs supprimés) : " + " ; ".join(f"{j} {v['gain_Md']:.2f} Md€ (heures {v['intensif']:.2f},"
                                                        f" participation {v['extensif']:.2f}), ETP {v['etp_milliers']:.0f} k"
                                                        for j, v in EFF.items()))
grid = np.array(V3["taux"]["z"])
TAUX = dict(z=list(grid), auj_tm=V3["taux"]["auj_tm"], auj_ta=V3["taux"]["auj_ta"], final_tm=list(100 * S[0](grid)),
            final_ta=list(100 * S[1](grid) / grid), v3_tm=V3["taux"]["final_tm"], v3_ta=V3["taux"]["final_ta"])
ta_a, ta_n = np.array(TAUX["auj_ta"]), np.array(TAUX["final_ta"])
for zz in (19176.0, 38353.0, 60e3, 100e3, 200e3, 400e3):
    i = int(np.argmin(np.abs(grid - zz)))
    p(f"  z {zz:8,.0f} : taux moyen {ta_a[i]:5.1f} → {ta_n[i]:5.1f} % ; marginal {TAUX['auj_tm'][i]:5.1f} → {TAUX['final_tm'][i]:5.1f} %")
i1, i2 = int(np.argmin(np.abs(grid - 19176))), int(np.argmin(np.abs(grid - 200e3)))
PROGR = dict(ecart_ta_smic_200k_auj=float(ta_a[i2] - ta_a[i1]), ecart_ta_smic_200k_nouveau=float(ta_n[i2] - ta_n[i1]),
             tm_max_nouveau=float(max(TAUX["final_tm"])))
p(f"  progressivité (taux moyen 200 k€ − Smic) : {PROGR['ecart_ta_smic_200k_auj']:.1f} → {PROGR['ecart_ta_smic_200k_nouveau']:.1f}"
  f" points ; taux marginal maximal {PROGR['tm_max_nouveau']:.1f} %")

TDEC = []
for dcl in range(10):
    inc = sum((w * M.ZNG[g] * (M.DEC == dcl)).sum() for n, g, f, w, pp, k in TYPES)
    t0 = sum((w * OBS[n] * (M.DEC == dcl)).sum() for n, g, f, w, pp, k in TYPES)
    t1 = sum((w * (OBS[n] + NET[n]) * (M.DEC == dcl)).sum() for n, g, f, w, pp, k in TYPES)
    TDEC.append(dict(decile=dcl + 1, taux_effectif_auj=100 * t0 / inc, taux_effectif_nouveau=100 * t1 / inc))
PROGR["taux_effectifs_deciles_niches_comprises"] = TDEC
p("  taux effectif moyen par décile, niches comprises (impôt / revenu après cotisations) : " +
  " ; ".join(f"D{r['decile']} {r['taux_effectif_auj']:.1f}→{r['taux_effectif_nouveau']:.1f}" for r in TDEC))

# ================================================================== 6. cascade « où vont les ressources » (statique, croisière)
res, _ = C.cascade(S, O)
CASC = {cle: d for cle, lib, d in res}
SRC = dict(
    vraies_niches=DECOMP["niches_supprimees"]["Md"] + HORS_MD,
    alignement_pensions=CASC["abatpen"]["Md"] + CASC["age"]["Md"] + CASC["csg_ret"]["Md"],
    unite_fiscale=CASC["conjugal"]["Md"],
    technique_csg_deductible=CASC["csg_ded"]["Md"],
    technique_frais=CASC["forfait"]["Md"] + DECOMP["frais_reels_au_dela_du_forfait"]["Md"],
    quotient_familial_vers_franchise=CASC["qf"]["Md"] + CASC["franchise"]["Md"],
    cehr_absorbee=-R.CEHR_BAR,
)
SRC["financement_externe"] = FIN_TOT
SRC["aspa_nette"] = -ASPA_C["central"]
SRC["bareme"] = -sum(SRC.values())                # baisse des taux financée (solde = 0)
SRC["solde"] = sum(SRC.values())
p("\n[CASCADE] ressources (+) et emplois (−), Md€ : " + " ; ".join(f"{k} {v:+.1f}" for k, v in SRC.items()))
p(f"  (barème brut {CASC['bareme']['Md']:+.1f} ; correction des avantages gardés et de l'écart inexpliqué {CORR:.1f}"
  f" et de l'IR non attribué {PRUD:.1f} portée par le barème ; franchise {CASC['franchise']['Md']:+.1f}, QF {CASC['qf']['Md']:+.1f})")

# ================================================================== 7. trajectoire 2027-2040
RECETTE_DISP = {r["cle"]: r for r in D4.tableau()}
ann = {}
NETX0 = {n: NEW0[n] - SIMF[n] + FREX[n] + PERTE[n] for n in NEW0}   # net hors CEHR, sans financement
NETX1 = {n: NET[n] + CEHR_I[n] for n in NEW}
g0 = dict(actifs=somme(NETX0, lambda n, g, f, k: g == "A"), retraites=somme(NETX0, lambda n, g, f, k: g == "R"))
g1 = dict(actifs=somme(NETX1, lambda n, g, f, k: g == "A"), retraites=somme(NETX1, lambda n, g, f, k: g == "R"))

def tm_inter(k):
    """Barème intermédiaire au prorata du financement : impôt = (1 − k) × barème à recette constante + k × barème final
    (taux marginaux interpolés aux points de l'un et de l'autre)."""
    pts = sorted(set(list(P0) + list(P_FIN)))
    return pts, [float((1 - k) * S0[0](z) + k * S[0](z)) for z in pts]


for i, an in enumerate(range(2027, 2041)):
    lam = MONTEE.get(an, 1.0)
    f = PALIERS.get(an, FIN_TOT if an >= 2040 else 0.0)
    asp = lam * ASPA_C["central"] if f > 0 else 0.0
    kf = (f - asp) / (lam * F_BAR)
    manque = sum(r["recette_croisiere_Md"] * (1 - D4.PROFILS[r["profil"]][i]) for r in RECETTE_DISP.values()
                 if r["modele"] in ("residu", "hors"))
    row = dict(lambda_fusion=lam, financement_externe_recu=f,
               ircsg_actifs=lam * ((1 - kf) * g0["actifs"] + kf * g1["actifs"]),
               ircsg_retraites=lam * ((1 - kf) * g0["retraites"] + kf * g1["retraites"]),
               ircsg_cehr_bareme_absorbee=-lam * R.CEHR_BAR, aspa_nette_depense=-asp,
               extinction_progressive_niches=-lam * manque, ajustement_bareme_transitoire=lam * manque)
    row["ircsg_ecart_calage"] = -f - sum(v for kk, v in row.items() if kk not in ("lambda_fusion", "financement_externe_recu"))
    row["ircsg_total"] = sum(v for kk, v in row.items() if kk not in ("lambda_fusion", "financement_externe_recu"))
    row["pour_memoire_recette_niches_supprimees"] = lam * (sum(r["recette_croisiere_Md"] for r in RECETTE_DISP.values()
                                                               if r["modele"] in ("residu", "hors")) - manque)
    row["pour_memoire_dont_hors_modele"] = lam * HORS_MD
    row["part_du_bareme_final_k"] = kf
    row["bareme_points"], row["bareme_taux"] = tm_inter(kf)
    ann[str(an)] = row
p("\n[TRAJECTOIRE] total (= −financement) ; recette des niches supprimées ; manque dû aux reports (couvert par le barème) : "
  + " ; ".join(f"{a} {r['ircsg_total']:+.2f}/{r['pour_memoire_recette_niches_supprimees']:.1f}/{r['ajustement_bareme_transitoire']:.2f}"
               f" (A {r['ircsg_actifs']:+.1f}, R {r['ircsg_retraites']:+.1f}, écart {r['ircsg_ecart_calage']:+.2f})"
               for a, r in ann.items()))

# ================================================================== 8. sorties
J.update(
    version="v4 final, 7,0 Md€ (19/11/2026)",
    sources=dict(cpo="CPO, L'impôt sur le revenu, ses réductions et crédits d'impôt depuis 2017, septembre 2026 (vie-publique.fr/files/rapport/pdf/304837.pdf)",
                 dgfip="DGFiP Statistiques n° 41, novembre 2025 (impots.gouv.fr, classeur dgfip_stat_41.xlsx)",
                 vm="Voies et moyens, t. II, PLF 2026, coût 2025 (copie assemblee-nationale.fr)"),
    donnees_niches=dict(ensemble=D4.ENSEMBLE, cpo_t15=D4.CPO_T15, cpo_t17=D4.CPO_T17, cpo_t21=D4.CPO_T21,
                        dgfip_t4_rici_par_decile=D4.DGFIP_T4_RICI_DECILE, fiches=D4.FICHES,
                        population_par_age_M=POP, part_retraites={c: D4.part_retraites(c, POP) for c in D4.FICHES}),
    tableau_dispositifs=D4.tableau(),
    recette_niches_par_dispositif=dict(
        par_dispositif={r["cle"]: dict(libelle=r["libelle"], cout_vm_2025_Md=r["cout_vm_2025_Md"], classement=r["classement"],
                                       traitement_modele=r["modele"], part_supprimable=r["part_supprimable"],
                                       recette_croisiere_Md=r["recette_croisiere_Md"] if r["modele"] in ("residu", "hors") else 0.0,
                                       profil=r["profil"], reparti_modele_Md=PAR_DISP.get(r["cle"], {}).get("Md"))
                        for r in D4.tableau()},
        total_dans_le_residu_Md=DECOMP["niches_supprimees"]["Md"], total_hors_modele_Md=HORS_MD,
        total_Md=DECOMP["niches_supprimees"]["Md"] + HORS_MD, par_annee_avant_lambda=D4.recette_par_profil(D4.tableau()),
        residu_v3_Md=DECOMP["residu"]["Md"]),
    decomposition_residu=DECOMP, niches_reparties=PAR_DISP,
    recette_a_tenir=dict(cible_v3=N.CIBLE, gardes_non_supprimables=DECOMP["non_supprimables_ou_stock"]["Md"],
                         ecart_inexplique=U_TOT, ecart_retenu=max(U_TOT, 0.0), recettes_hors_modele=HORS_MD,
                         ir_non_attribue_prudence=PRUD, financement=FIN, cible_finale=cible(FIN), cible_sans_financement=cible(0.0)),
    frais=dict(options=FRAIS, recommandee=OPTION),
    final=dict(description="Version finale « bas et milieu » : financement externe de 7,0 Md€ en croisière (paliers"
                           " 2029-2040) ; ASPA calculée sur la pension nette du nouvel impôt (0,3 Md€) ; le reste baisse les"
                           " taux aux repères 0 à 3,5 Smic (poids 1/1/1/1/0,5) ; plafond de 48 % à 163 400 €",
               points=P_FIN, taux=TT, financement=FIN_TOT, baisse_points=100 * E_BM,
               variante_ecartee_plafond_recule=dict(zp=ZP_EXPLORE, ecart=ecart(S_EXPLORE)),
               aspa_cout_Md=ASPA_C, financement_bareme=F_BAR, ecart_taux_moyen_smic_200k=ecart(S),
               ecart_v4_5_5=ecart(S5), ecart_droit_actuel=26.78, tout_sur_progressivite=dict(zp=ZP_TOUT, ecart=ecart(design(ZP_TOUT))),
               pour_atteindre=VARIANTES, paliers=PALIERS, recette_modele=N.recette(S, O)),
    bareme=dict(points=P_FIN, taux=TT, taux_v3=T0, ajustement_points=100 * DFIN, ajustement_sans_financement=100 * D0,
                recette_modele=N.recette(S, O), taux_sans_financement=list(np.array(T0) + D0 * W_UNI)),
    moyennes_categories=MOY, deciles=DECS, sous_groupes=SOUS,
    gagnants_perdants=dict(publie=False, raison=(
        "Non estimable sérieusement : on ne connaît pas la distribution jointe des niches, du revenu et de la configuration"
        " familiale ; le modèle représente chaque tranche par des foyers types ; seules des moyennes par catégorie et des"
        " moyennes de bénéficiaires sont produites.")),
    efficacite=dict(libelle="gain d'efficacité statique lié à la modification des incitations fiscales au travail, hors effets"
                            " comportementaux propres aux dispositifs supprimés", jeux=EFF),
    taux=TAUX, progressivite=PROGR, cascade_categories=SRC,
    cascade_brute=[dict(etape=a, libelle=b, Md=c["Md"]) for a, b, c in res],
    annuel_final=ann,
    unites=("Md€ niveau 2025 ; + = recette publique en plus ; ircsg_total = −financement externe de l'année ; fusion"
            " λ = 0,25/0,5/0,75/1 en 2027-2030 ; financement 1,5 Md€ de 2029 à 2034, 2,5 de 2035 à 2037, 4,5 en 2038, 6,0 en"
            " 2039, 7,0 dès 2040 (dont ASPA nette, dépense hors impôt, à partir de 2029) ; barème de l'année : impôt ="
            " (1 − k) × barème à recette constante + k × barème final ; niches à reports"
            " (Girardin, PME) 60/80/90/100 % ; engagements Pinel gardés jusqu'à extinction (aucune recette) ; actifs et"
            " retraités : variation réelle (nette des niches, hors écart inexpliqué du modèle), CEHR à part ; les avantages"
            " d'invalidité et de dépendance, gardés, sont neutres"),
    statuts={"donnees_niches": "[E] CPO 2026, DGFiP n° 41, Voies et moyens PLF 2026",
             "repartition_niches": "[S] coût par groupe de RFR par part (CPO) appliqué aux quantiles de RFR du modèle [H]",
             "frais": "[H] modèle de frais calé sur les déclarations [E]", "bareme": "[C]", "efficacite": "[S]"},
)
json.dump(J, open(OUT / "ircsg4.json", "w"), ensure_ascii=False, indent=1, default=float)
(OUT / "ircsg4_calculs.txt").write_text("\n".join(L) + "\n", encoding="utf-8")
