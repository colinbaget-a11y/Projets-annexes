"""Bloc IS de la note de 8 pages (note8p/CADRE.md, refonte du 17/11/2026).

Lancer depuis fiscalite/ : python3 note8p/calculs/is_reforme.py
  -> note8p/sorties/is.json  (tous les chiffres, table `annuel` 2027-2040, coûts par point)
  -> note8p/sorties/is_calculs.txt  (journal lisible des calculs)

Trois mesures (arbitrage de l'auteur) :
  1. suppression progressive du taux réduit de 15 % (20 % en 2027, aligné sur le taux normal dès 2028) ;
  2. déduction immédiate de 50 % des équipements neufs éligibles, les 50 % restants amortis selon les règles
     ordinaires (mode linéaire ou dégressif actuel) ; introduction à 25 % en 2027 puis 50 % dès 2028 ;
  3. baisse du taux normal (24, 23 ou 22 %), dont le niveau et le calendrier sont fixés au bouclage.
Pas de dette : la table `annuel` donne des séries séparées (+ = recette publique, − = coût) que le bouclage
combine année par année.

Mécanique reprise de is/simulation_is.py (importé, non modifié : plans d'amortissement, bases de bénéfices 2025
portées en 2027, investissement éligible) et de is/calculs_note_is.py (fonctions recopiées ici, car son import
réécrirait des tableaux de synthese/). Conventions : année = exercice (en caisse, environ un an plus tard, voir
`annuel_caisse`) ; Md€ courants, croissance nominale de 3 % par an après 2027 ; part de l'investissement éligible
faite par des sociétés imposables 75 % (H1) ; plan actuel moitié linéaire, moitié dégressif (H5).
"""
import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]          # fiscalite/
sys.path.insert(0, str(ROOT / "is"))
import simulation_is as sim  # noqa: E402

OUT = ROOT / "note8p" / "sorties"
OUT.mkdir(parents=True, exist_ok=True)
L, J = [], {}
p = L.append

TAU, G, R_ENT, R_ETAT, PART = 0.25, sim.G, sim.R, sim.R_ETAT, 0.75
AN1, I1 = sim.AN1, sim.I1                            # 2027 ; 89,1 Md€ d'investissement éligible
ANS = list(range(2027, 2041))
NA = len(ANS)
H = 60
CR = (1 + G) ** np.arange(H)                         # croissance nominale depuis 2027
PLANS = {"lin": sim.plan("lineaire"), "deg": sim.plan("degressif")}
E0 = np.eye(1, len(PLANS["lin"]), 0).ravel()
PIB25, PIB27 = 2991.0, sim.PIB_2027


def fr(x, d=1):
    s = f"{x:,.{d}f}".replace(",", " ").replace(".", ",")
    return s.replace("-", "−")


def z(d, r=R_ENT):
    return float(sum(dk / (1 + r) ** k for k, dk in enumerate(d)))


def zmix(r=R_ENT, b=0.0):
    """Valeur actuelle des déductions pour 1 € (moyenne linéaire / dégressif), avec une fraction b déduite tout de suite."""
    return b + (1 - b) * (z(PLANS["lin"], r) + z(PLANS["deg"], r)) / 2


# ============================================================================ 0. bases
B_N = sim.BASE_NORMALE * sim.AB                      # bénéfice au taux normal, 2027 (267,1)
B_R = sim.BASE_REDUITE * sim.AB                      # bénéfice au taux réduit, 2027 (31,8)
POINT = (B_N + B_R) / 100                            # un point, taux réduit supprimé (2,99)
POINT_N = B_N / 100                                  # un point sur la seule base au taux normal (2,67)
p("=" * 100)
p("0. BASES (DGFiP Statistiques n° 51, exercice 2025, portées en 2027 par la croissance du bénéfice fiscal x"
  f"{sim.AB:.3f}) ; ensuite +{G:.0%} par an [H]")
p(f"[BASE] bénéfice au taux normal 2027 {B_N:.1f} Md€ ; au taux réduit {B_R:.1f} Md€ ; un point de taux normal "
  f"{POINT:.2f} Md€ (taux réduit supprimé) ; {POINT_N:.2f} Md€ (sur la seule base au taux normal)")
J["bases_2027"] = {"benefice_taux_normal": B_N, "benefice_taux_reduit": B_R, "point_base_totale": POINT,
                   "point_base_normale": POINT_N, "croissance_apres_2027": G}

# ============================================================================ 1. taux réduit
p("")
p("=" * 100)
p("1. SUPPRESSION DU TAUX RÉDUIT DE 15 %")
TR_STAT = 0.10 * B_R                                  # statique, 10 points
TR_BAS = sim.REDUIT[0]                                # coût officiel 2019 ramené à 10 points, porté à 3 %/an
TR_C = (TR_STAT + TR_BAS) / 2                         # central [H] : 84 % du statique
p(f"[TR] rendement à plein (10 points, 2027) : statique {TR_STAT:.2f} Md€ ; prudent {TR_BAS:.2f} (chiffre officiel 2019 "
  f"de 2,2 Md€ pour 13 points, ramené à 10 points et porté à 3 %/an) ; central {TR_C:.2f} ({100*TR_C/TR_STAT:.0f} % du "
  f"statique : passages à l'IR, rémunération en salaire, découpages non chiffrés) [S/H]")
p(f"[TR] bénéficiaires : 760 000 en 2019 (CPO 2023, d'après VM PLF 2019) ; base 2025 / plafond = au moins "
  f"{sim.BASE_REDUITE*1e9/42_500:,.0f} sociétés au plafond-équivalent (base 2025) (le nombre réel est plus élevé : beaucoup sont sous le "
  "plafond) ; avantage maximal 4 250 € par société et par an".replace(",", " "))
p(f"[TR] si le taux normal final est x %, l'alignement rapporte (x − 15)/10 du rendement : 24 % {0.9*TR_C:.2f} ; 23 % "
  f"{0.8*TR_C:.2f} ; 22 % {0.7*TR_C:.2f} Md€ (comptabilisé ici à 25 % ; l'écart est dans le coût par point sur la base totale)")
CAL_TR = {2027: 0.5}                                  # 20 % en 2027 (5 points sur 10), aligné dès 2028
tr_serie = np.array([CAL_TR.get(a, 1.0) * TR_C * CR[t] for t, a in enumerate(ANS)])
tr_bas = np.array([CAL_TR.get(a, 1.0) * TR_BAS * CR[t] for t, a in enumerate(ANS)])
tr_haut = np.array([CAL_TR.get(a, 1.0) * TR_STAT * CR[t] for t, a in enumerate(ANS)])
p("[TR] calendrier proposé : 20 % en 2027, aligné sur le taux normal dès 2028 (exercices) ; recette "
  + " ; ".join(f"{a} {v:.2f}" for a, v in zip(ANS[:4], tr_serie[:4])) + f" ... 2040 {tr_serie[-1]:.2f} Md€")
J["taux_reduit"] = {"statique_2027": TR_STAT, "prudent_2027": TR_BAS, "central_2027": TR_C,
                    "beneficiaires_2019": 760000, "cout_officiel_2019": 2.2, "avantage_max_euros": 4250,
                    "calendrier": {"2027": "20 %", "2028+": "taux normal"},
                    "serie_central": dict(zip(ANS, tr_serie.tolist())), "serie_bas": dict(zip(ANS, tr_bas.tolist())),
                    "serie_haut": dict(zip(ANS, tr_haut.tolist()))}


# ============================================================================ 2. déduction immédiate
def chemin(reg, bonus, part=PART, i1=I1, tau=TAU, h=H):
    """Coût annuel pour l'État (Md€, + = coût), années 0..h-1 (0 = 2027) ; bonus(t) = fraction déduite tout de suite
    des achats de l'année t, le reste amorti selon le plan actuel (b E0 + (1 − b) plan)."""
    anc = PLANS[reg]
    n = len(anc)
    c = np.zeros(h + n)
    for t in range(h):
        b = bonus(t)
        c[t:t + n] += tau * part * i1 * CR[t] * ((b * E0 + (1 - b) * anc) - anc)
    return c[:h]


def chemin_mix(bonus, **kw):
    return (chemin("lin", bonus, **kw) + chemin("deg", bonus, **kw)) / 2


def perm(b, reg="mix", part=PART, i1=I1):
    """Coût permanent à l'échelle de 2027 : tau s b I (1 − z(g)), z actualisé au taux de croissance."""
    if reg == "mix":
        return (perm(b, "lin", part, i1) + perm(b, "deg", part, i1)) / 2
    return TAU * part * b * i1 * (1 - z(PLANS[reg], G))


def va(b, r=R_ENT, part=PART, reg="mix"):
    """Coût actualisé d'une année d'achats (Md€ de 2027) : tau s I (z_b − z)."""
    if reg == "mix":
        return (va(b, r, part, "lin") + va(b, r, part, "deg")) / 2
    zz = z(PLANS[reg], r)
    return TAU * part * I1 * b * (1 - zz)


def dette(cout, fin0, r=R_ETAT):
    D, d = np.zeros(len(cout)), 0.0
    for t in range(len(cout)):
        d = d * (1 + r) - (fin0 * CR[t] - cout[t])
        D[t] = d
    return D


p("")
p("=" * 100)
p("2. DÉDUCTION IMMÉDIATE DE 50 % (définition : 50 % du prix déduits l'exercice d'acquisition, les 50 % restants "
  "amortis selon le plan ordinaire ; vérifiée dans is/simulation_is.py plan_bonus et is/calculs_note_is.py chemin)")
d0 = (PLANS["lin"][0] + PLANS["deg"][0]) / 2
p(f"[DEF] déduction de l'exercice d'acquisition pour 100 € (achat au 1er juillet) : aujourd'hui linéaire "
  f"{100*PLANS['lin'][0]:.2f}, dégressif {100*PLANS['deg'][0]:.2f} ; réforme 50 % : linéaire "
  f"{100*(0.5+0.5*PLANS['lin'][0]):.2f}, dégressif {100*(0.5+0.5*PLANS['deg'][0]):.2f}")
for r_ in (R_ENT, R_ETAT, 0.08):
    p(f"[Z r={r_:.2%}] valeur actuelle des déductions pour 100 € : linéaire {100*z(PLANS['lin'], r_):.1f} ; dégressif "
      f"{100*z(PLANS['deg'], r_):.1f} ; moyenne {100*zmix(r_):.1f} ; 50 % + reste ordinaire {100*zmix(r_, 0.5):.1f} ; 100 % 100")
CALS = {"A": ("50 % dès 2027", lambda t: 0.5),
        "B": ("25 % en 2027, 50 % dès 2028 (proposé)", lambda t: 0.25 if t == 0 else 0.5),
        "C": ("25 % en 2027-2028, 50 % dès 2029", lambda t: 0.25 if t < 2 else 0.5),
        "D": ("100 % dès 2027 (référence abandonnée)", lambda t: 1.0)}
DED = {}
for k, (nom, f) in CALS.items():
    c = {reg: chemin(reg, f) for reg in ("lin", "deg")}
    c["mix"] = (c["lin"] + c["deg"]) / 2
    DED[k] = c
    p(f"[DED {k}] {nom} : coût (mix ; dég.–lin.) " + " ; ".join(
        f"{a} {c['mix'][t]:.2f} ({c['deg'][t]:.1f}–{c['lin'][t]:.1f})" for t, a in enumerate(ANS) if a in
        (2027, 2028, 2029, 2030, 2032, 2035, 2040)) + f" ; cumul 2027-2040 {c['mix'][:NA].sum():.1f}")
CLE = "B"
b_perm = {"A": 0.5, "B": 0.5, "C": 0.5, "D": 1.0}
for k in ("A", "D"):
    pm = perm(b_perm[k])
    p(f"[PERM {k}] coût permanent (régime établi) : {pm:.2f} Md€ de 2027 ({perm(b_perm[k], 'deg'):.2f}–"
      f"{perm(b_perm[k], 'lin'):.2f}) ; en 2040 (courants) {pm*CR[13]:.2f} ; = {100*pm/PIB27:.3f} % du PIB")
    p(f"[VA {k}] coût actualisé par année d'achats : {va(b_perm[k]):.2f} Md€ à 5 % ({va(b_perm[k], reg='deg'):.2f}–"
      f"{va(b_perm[k], reg='lin'):.2f}) ; {va(b_perm[k], R_ETAT):.2f} à 3,25 % ; en points de taux {va(b_perm[k])/POINT:.2f}")
# l'ancienne variante 50 % : dette transitoire, pas coût permanent
FIN_OLD = (sim.ELARG_PRUDENT + sum(sim.ELARG.values())) / 2
Dold = dette(DED["A"]["mix"], FIN_OLD)
p(f"[ANCIEN] ancienne variante « 50 % dès 2027 » financée par {FIN_OLD:.2f} Md€/an d'assiette (calculs_note_is) : dette "
  f"maximale {Dold.max():.1f} Md€ en {AN1+int(np.argmax(Dold))} = cumul des avances de la transition, remboursé ensuite ; "
  f"ce n'est pas un coût de 5 Md€ par an : le coût permanent est {perm(0.5):.2f} Md€/an (euros de 2027)")
trans = DED[CLE]["mix"][:NA] - np.array([perm(0.5) * CR[t] for t in range(NA)])
trans[0] = DED[CLE]["mix"][0] - perm(0.25)          # 2027 : seul le millésime à 25 %
p(f"[TRANS {CLE}] part transitoire (avance d'impôt remboursée ensuite) du coût : " + " ; ".join(
    f"{a} {v:.2f}" for a, v in zip(ANS, trans) if a in (2027, 2028, 2030, 2033, 2035)))
# assiette élargie : véhicules utilitaires (hypothèse : la moitié des 42,1 Md€ de matériel de transport)
FAC_VU = (sim.I_2025 + 0.5 * 42.1) / sim.I_2025
p(f"[VARIANTE] véhicules utilitaires inclus (moitié du matériel de transport des SNF, 21 Md€ en 2025 [H]) : tous les "
  f"coûts x {FAC_VU:.2f} ; 2028 {DED[CLE]['mix'][1]*FAC_VU:.2f} au lieu de {DED[CLE]['mix'][1]:.2f}")
for s_ in (0.60, 0.90):
    cc = chemin_mix(CALS[CLE][1], part=s_)
    p(f"[PART {s_:.0%}] calendrier {CLE} : 2027 {cc[0]:.2f} ; 2028 {cc[1]:.2f} ; 2040 {cc[13]:.2f} ; permanent "
      f"{perm(0.5, part=s_):.2f}")
J["deduction"] = {
    "definition": "50 % du prix déduits l'exercice d'acquisition + amortissement ordinaire (linéaire ou dégressif) des 50 % restants",
    "investissement_eligible_2027": I1, "part_imposable": PART,
    "calendriers": {k: {"nom": v[0], "mix": dict(zip(ANS, DED[k]["mix"][:NA].tolist())),
                        "lin": dict(zip(ANS, DED[k]["lin"][:NA].tolist())),
                        "deg": dict(zip(ANS, DED[k]["deg"][:NA].tolist()))} for k, v in CALS.items()},
    "calendrier_retenu": CLE,
    "cout_permanent_2027": {"50": perm(0.5), "100": perm(1.0), "50_bornes": [perm(0.5, "deg"), perm(0.5, "lin")],
                            "100_bornes": [perm(1.0, "deg"), perm(1.0, "lin")]},
    "cout_actualise_millesime_5pc": {"50": va(0.5), "100": va(1.0)},
    "cout_actualise_millesime_etat": {"50": va(0.5, R_ETAT), "100": va(1.0, R_ETAT)},
    "ancienne_dette_50pc": {"max": float(Dold.max()), "annee": AN1 + int(np.argmax(Dold)), "financement": FIN_OLD},
    "part_transitoire": dict(zip(ANS, trans.tolist())), "facteur_vehicules_utilitaires": FAC_VU}

# ============================================================================ 3. taux normal
p("")
p("=" * 100)
p("3. BAISSE DU TAUX NORMAL")
pt_tot = POINT * CR[:NA]
pt_norm = POINT_N * CR[:NA]
p("[POINT] coût d'un point (statique, base totale, taux réduit supprimé) : " + " ; ".join(
    f"{a} {v:.2f}" for a, v in zip(ANS, pt_tot) if a in (2027, 2028, 2030, 2035, 2040)) + " Md€")
for e in (0.5, 1.0):
    x = 2
    retour = (TAU - x / 100) * (e / 100 * x) * (B_N + B_R)
    p(f"[POINT dyn] −{x} points avec une semi-élasticité des bénéfices déclarés de {e} % par point (Beer, de Mooij et Liu, "
      f"2020, mesurée sur les filiales de multinationales : borne haute si appliquée à tous) : coût {x*POINT:.2f} − "
      f"{retour:.2f} = {x*POINT-retour:.2f} Md€ (2027), soit {100*retour/(x*POINT):.0f} % de retour")
inter = DED[CLE]["mix"][:NA] / (100 * TAU)
p("[INTER] chaque point de baisse réduit le coût de la déduction de 1/25 : " + " ; ".join(
    f"{a} +{v:.3f}" for a, v in zip(ANS, inter) if a in (2027, 2028, 2030, 2040)) + " Md€ par point")
CIBLES = {24: 1, 23: 2, 22: 3}
for tx, x in CIBLES.items():
    p(f"[CIBLE {tx} %] coût statique 2028 {x*pt_tot[1]:.2f} ; 2040 {x*pt_tot[13]:.2f} Md€ ; alignement du taux réduit "
      f"(compté à 25 %) {tr_serie[1]:.2f} en 2028")
J["taux_normal"] = {"cout_par_point_base_totale": dict(zip(ANS, pt_tot.tolist())),
                    "cout_par_point_base_normale": dict(zip(ANS, pt_norm.tolist())),
                    "interaction_par_point_deduction": dict(zip(ANS, inter.tolist())),
                    "retour_benefices_declares_part": [0.0, (TAU - .02) * (.01 * 2) * (B_N + B_R) / (2 * POINT)]}

# ============================================================================ 4. taux effectifs (TMEI, TMEA)
p("")
p("=" * 100)
p("4. TAUX MARGINAUX ET MOYENS EFFECTIFS (convention Devereux-Griffith de is/calculs_note_is.py : r réel 5 %, "
  "inflation 2 %, δ 14 % équipements / 3,1 % bâtiments ; pas d'impôt personnel)")
PI, RR = 0.02, 0.05
RHO = (1 + RR) * (1 + PI) - 1                          # 7,1 % nominal (fonds propres)
I_NOM = RHO                                            # taux d'intérêt nominal du prêteur
RHO_D = lambda tau: I_NOM * (1 - tau)                  # coût après impôt de la dette
ZB = np.array([0.5 / 25] + [1 / 25] * 24 + [0.5 / 25])  # bâtiment, linéaire 25 ans


def cout_capital(tau, b, rho, delta=0.14, plan=None):
    """Coût du capital p (rendement réel avant impôt exigé), plan actuel moyen (ou `plan`), fraction b déduite tout de
    suite, actualisation au taux nominal rho : p = (1 − τz)(ρ − π + δ(1+π)) / ((1−τ)(1+π)) − δ."""
    zz = b + (1 - b) * (z(plan, rho) if plan is not None else zmix(rho))
    A = tau * zz
    return (1 - A) * (rho - PI + delta * (1 + PI)) / ((1 - tau) * (1 + PI)) - delta


def tmei(tau, b, fin="fp", delta=0.14, plan=None, dette_part=1 / 3):
    pf = cout_capital(tau, b, RHO, delta, plan)
    pd = cout_capital(tau, b, RHO_D(tau), delta, plan)
    pc = {"fp": pf, "dette": pd, "mixte": (1 - dette_part) * pf + dette_part * pd}[fin]
    return (pc - RR) / pc, pc


def tema(tau, b, p_=0.20, delta=0.14, plan=None):
    zz = b + (1 - b) * (z(plan, RHO) if plan is not None else zmix(RHO))
    A = tau * zz
    Rs = (p_ - RR) / (1 + RR)
    Rn = -(1 - A) + ((1 + PI) * (p_ + delta) * (1 - tau) + (1 + PI) * (1 - delta) * (1 - A)) / (1 + RHO)
    return (Rs - Rn) / (p_ / (1 + RR))


CONF = {"actuel": ("Système actuel (25 %)", 0.25, 0.0),
        "taux23": ("Taux normal à 23 %", 0.23, 0.0),
        "taux24": ("Taux normal à 24 %", 0.24, 0.0),
        "taux22": ("Taux normal à 22 %", 0.22, 0.0),
        "ded50": ("Déduction immédiate de 50 % (25 %)", 0.25, 0.5),
        "combi24": ("24 % + déduction de 50 %", 0.24, 0.5),
        "combi23": ("23 % + déduction de 50 %", 0.23, 0.5),
        "combi22": ("22 % + déduction de 50 %", 0.22, 0.5),
        "ded100": ("Déduction intégrale (25 %)", 0.25, 1.0),
        "pme15": ("Petite société sous le plafond, aujourd'hui (15 %)", 0.15, 0.0)}
TEF = {}
for k, (nom, tau, b) in CONF.items():
    tf, pf = tmei(tau, b, "fp")
    td, pd = tmei(tau, b, "dette")
    tm, pm = tmei(tau, b, "mixte")
    tl = tmei(tau, b, "fp", plan=PLANS["lin"])[0]
    tg = tmei(tau, b, "fp", plan=PLANS["deg"])[0]
    tb = tmei(tau, 0.0, "fp", delta=0.031, plan=ZB)[0]
    ta = tema(tau, b)
    TEF[k] = {"nom": nom, "tau": tau, "b": b, "tmei_fp": tf, "tmei_dette": td, "tmei_mixte": tm, "p_fp": pf,
              "p_dette": pd, "ecart_cout_capital_fp_dette": pf - pd, "tmei_fp_lin": tl, "tmei_fp_deg": tg,
              "tmei_batiment": tb, "tema_20": ta}
    p(f"[TEF] {nom:52s} TMEI fonds propres {100*tf:5.1f} % (lin. {100*tl:4.1f}, dég. {100*tg:4.1f}) ; dette "
      f"{100*td:6.1f} % ; mixte (1/3 dette) {100*tm:5.1f} % ; p fp {100*pf:.2f} / dette {100*pd:.2f} (écart "
      f"{100*(pf-pd):.2f} pt) ; bâtiment {100*tb:4.1f} % ; TMEA projet 20 % {100*ta:4.1f} %")
p("[TEF] lecture : l'écart de coût du capital entre dette et fonds propres (avantage de la dette) ne croît pas avec la "
  "déduction : il vaut ρ − i(1−τ) multiplié par (1 − τz)/(1 − τ), qui baisse quand z monte ; il baisse aussi avec le taux. "
  "Mais le TMEI d'un projet financé par emprunt devient plus négatif (subvention nette).")
J["taux_effectifs"] = TEF
J["taux_effectifs_convention"] = {"r_reel": RR, "inflation": PI, "delta_equipement": 0.14, "delta_batiment": 0.031,
                                  "i_nominal": I_NOM, "part_dette_mixte": 1 / 3, "plan": "moitié linéaire 7 ans, moitié dégressif"}

# ============================================================================ 5. cas types
p("")
p("=" * 100)
p("5. CAS TYPES")
# 5.1 machine de 500 000 € achetée le 1er juillet par une PME industrielle (exercice civil, durée d'usage 7 ans)
M = 500_000.0
cas_m = {}
for reg, nom in (("lin", "linéaire"), ("deg", "dégressif (coef. 2,25)")):
    anc = M * PLANS[reg]
    nouv = M * (0.5 * E0 + 0.5 * PLANS[reg])
    rows = []
    for tau in (0.25, 0.23):
        eco_anc, eco_nouv = tau * anc, tau * nouv
        rows.append({"tau": tau, "economie_an1_actuel": eco_anc[0], "economie_an1_reforme": eco_nouv[0],
                     "tresorerie_an1": eco_nouv[0] - eco_anc[0],
                     "va_5": tau * (z(nouv / M) - z(anc / M)) * M, "va_8": tau * (z(nouv / M, .08) - z(anc / M, .08)) * M})
    cas_m[reg] = {"deduction_an1_actuel": anc[0], "deduction_an1_reforme": nouv[0], "plan_actuel": anc.tolist(),
                  "plan_reforme": nouv.tolist(), "par_taux": rows}
    p(f"[MACHINE {nom}] déductions annuelles actuelles " + " / ".join(fr(v, 0) for v in anc if v > 0)
      + f" € ; avec la réforme " + " / ".join(fr(v, 0) for v in nouv if v > 0) + " €")
    for r_ in rows:
        p(f"   à {100*r_['tau']:.0f} % : impôt économisé la 1re année {fr(r_['economie_an1_actuel'],0)} → "
          f"{fr(r_['economie_an1_reforme'],0)} € (trésorerie +{fr(r_['tresorerie_an1'],0)} €, rendue les années suivantes) ; "
          f"avantage actualisé {fr(r_['va_5'],0)} € à 5 %, {fr(r_['va_8'],0)} € à 8 %")


def gain_baisse(I, dtau, p_reel, rho_nom=R_ENT, plan_mix=True):
    """Gain actualisé, pour la seule machine, d'une baisse de taux dtau : dtau x (VA des recettes brutes − VA des
    déductions). Recettes : (p + δ) I (1−δ)^(t−1) (1+π)^t, t ≥ 1."""
    q = (1 - 0.14) * (1 + PI) / (1 + rho_nom)
    var = (p_reel + 0.14) * (1 + PI) / (1 + rho_nom) / (1 - q) * I
    return dtau * (var - zmix(rho_nom) * I), var


# projet marginal à 25 % : VA(R)(1 − τ) + τ z I = I
zm5 = zmix(R_ENT)
var_marg = M * (1 - TAU * zm5) / (1 - TAU)
g_marg = 0.02 * (var_marg - zm5 * M)
g_rent, var_rent = gain_baisse(M, 0.02, 0.20)
g_ded = TAU * (zmix(R_ENT, 0.5) - zm5) * M
p(f"[MACHINE taux vs déduction] machine marginale (rapporte juste son coût du capital) : −2 points valent "
  f"{fr(g_marg,0)} € actualisés, la déduction de 50 % {fr(g_ded,0)} € ; machine rentable (rendement réel brut 20 %) : "
  f"−2 points valent {fr(g_rent,0)} €, la déduction toujours {fr(g_ded,0)} € (plan moyen, 5 %)")
cas_m["comparaison"] = {"gain_baisse_2pts_marginale": g_marg, "gain_baisse_2pts_rentable20": g_rent,
                        "gain_deduction_50": g_ded}
# 5.2 petite société de services
def is_actuel(B):
    return 0.15 * min(B, 42_500) + 0.25 * max(B - 42_500, 0)


cas_s = {}
INV_S = 10_000.0                                      # informatique : durée 3 ans, linéaire
plan3 = np.array([0.5 / 3, 1 / 3, 1 / 3, 0.5 / 3])
for B in (30_000, 42_500, 60_000, 100_000, 150_000, 300_000):
    ligne = {"is_actuel": is_actuel(B)}
    for tx in (24, 23, 22):
        ded = (tx / 100) * INV_S * 0.5 * (1 - z(plan3))     # valeur actualisée annuelle de la déduction de 50 %
        ligne[str(tx)] = {"is_reforme": tx / 100 * B, "ecart_is": tx / 100 * B - is_actuel(B), "valeur_deduction": ded}
    cas_s[str(B)] = ligne
    p(f"[SERVICES] bénéfice {fr(B,0)} € : IS actuel {fr(is_actuel(B),0)} € ; écart à 24 % {fr(ligne['24']['ecart_is'],0)} ; "
      f"23 % {fr(ligne['23']['ecart_is'],0)} ; 22 % {fr(ligne['22']['ecart_is'],0)} € par an (+ = perte) ; la déduction de 50 % "
      f"sur 10 000 € d'informatique par an vaut {fr(ligne['23']['valeur_deduction'],0)} €")
SEUIL = {tx: 4250 / (0.25 - tx / 100) for tx in (24, 23, 22)}
p("[SERVICES] bénéfice en dessous duquel la société perd (taux réduit perdu > baisse du taux) : "
  + " ; ".join(f"{tx} % : {fr(s,0)} €" for tx, s in SEUIL.items()))
J["cas"] = {"machine_500k": cas_m, "services": cas_s, "seuil_perdant": SEUIL,
            "hypotheses": "achat au 1er juillet, exercice civil, durée d'usage 7 ans ; informatique 3 ans linéaire"}

# ============================================================================ 6. effets réels
p("")
p("=" * 100)
p("6. EFFETS RÉELS (ordres de grandeur, [S] calibrés sur [E])")
K_EQ, DEP_EQ = 541.0, 0.14                           # machines + TIC des SNF, fin 2025 (Insee 8.212)
K_BAT, DEP_BAT = 399.9, 0.031                        # bâtiments non résidentiels des SNF, fin 2025 (Insee 8.212)
S_EQ = (R_ENT + DEP_EQ) * K_EQ / PIB25               # part du revenu de ce capital = élasticité de la production
S_BAT = (R_ENT + DEP_BAT) * K_BAT / PIB25
EPS = {"bas": 0.5, "central": 1.0, "haut": 1.6}       # élasticité du stock au coût d'usage (MXD 1,6 ; littérature 0,25-1)
EPS_B = {"bas": 0.25, "central": 0.5, "haut": 1.0}    # bâtiments [H]
EI = {"bas": 1.8, "central": 2.4, "haut": 3.1}        # investissement de court terme / terme fiscal (CZZ : 8-14 % pour ~4,5 pt)


def usage(tau, b, zf=None):
    zz = b + (1 - b) * (zmix(R_ENT) if zf is None else zf)
    return (1 - tau * zz) / (1 - tau)


zb5 = z(ZB, R_ENT)
REEL = {}
for k in ("taux24", "taux23", "taux22", "ded50", "combi23", "ded100"):
    _, tau, b = CONF[k]
    dl_eq = np.log(usage(tau, b) / usage(0.25, 0.0))
    dl_b = np.log(usage(tau, 0.0, zb5) / usage(0.25, 0.0, zb5))
    res = {"dln_usage_equipement": dl_eq, "dln_usage_batiment": dl_b}
    for n in ("bas", "central", "haut"):
        dk_eq = -EPS[n] * dl_eq * PART * K_EQ
        dk_b = -EPS_B[n] * dl_b * PART * K_BAT
        dy = S_EQ * (dk_eq / K_EQ) + S_BAT * (dk_b / K_BAT)
        res[n] = {"dK_equipement": dk_eq, "dK_batiment": dk_b, "dY_pct": 100 * dy, "dY_Md25": dy * PIB25,
                  "dI_court_terme": -EI[n] * dl_eq * PART * I1, "dI_regime": (DEP_EQ + 0.01) * dk_eq + (DEP_BAT + 0.01) * dk_b}
    REEL[k] = res
    c = res["central"]
    p(f"[REEL {k}] coût d'usage équipements {100*dl_eq:+.2f} %, bâtiments {100*dl_b:+.2f} % ; capital équipements "
      f"{fr(res['bas']['dK_equipement'])} à {fr(res['haut']['dK_equipement'])} Md€ (central {fr(c['dK_equipement'])}), "
      f"bâtiments {fr(c['dK_batiment'])} ; investissement des premières années {fr(res['bas']['dI_court_terme'])} à "
      f"{fr(res['haut']['dI_court_terme'])} Md€/an ; en régime établi {fr(res['bas']['dI_regime'])} à "
      f"{fr(res['haut']['dI_regime'])} ; PIB de long terme (niveau) {res['bas']['dY_pct']:.3f} à {res['haut']['dY_pct']:.3f} % "
      f"(central {c['dY_pct']:.3f} %, {fr(c['dY_Md25'])} Md€ de 2025)")
# rendement par euro : capital supplémentaire par Md€ de coût permanent annuel (2040, régime établi, euros de 2027)
cp = {"taux24": 1 * POINT, "taux23": 2 * POINT, "taux22": 3 * POINT, "ded50": perm(0.5), "ded100": perm(1.0),
      "combi23": 2 * POINT + perm(0.5) * 23 / 25}
for k in cp:
    dk = REEL[k]["central"]["dK_equipement"] + REEL[k]["central"]["dK_batiment"]
    REEL[k]["cout_permanent_2027"] = cp[k]
    REEL[k]["dK_par_Md_cout"] = dk / cp[k]
    p(f"[RENDEMENT {k}] coût permanent {cp[k]:.2f} Md€/an (euros de 2027) ; capital en plus {dk:.1f} Md€ ; "
      f"{dk/cp[k]:.1f} Md€ de capital par Md€ de coût annuel")
# perte sèche (triangle sur les équipements) : indicateur d'efficacité, pas un supplément de PIB
coin = lambda tau, b: tau * (1 - (b + (1 - b) * zmix(R_ENT))) / (1 - tau)
for k in ("ded50", "taux23", "combi23"):
    _, tau, b = CONF[k]
    ps = [(R_ENT + DEP_EQ) * PART * K_EQ * EPS[n] * (coin(.25, 0) ** 2 - coin(tau, b) ** 2) / 2 for n in ("bas", "haut")]
    REEL[k]["perte_seche_evitee"] = ps
    p(f"[PS {k}] triangle évité sur les équipements : {ps[0]:.3f} à {ps[1]:.3f} Md€/an (indicateur, pas du PIB)")
# contre-effet : petites sociétés qui perdent le taux réduit (taux marginal 15 % → taux normal)
for tx in (23,):
    dl_eq_p = np.log(usage(tx / 100, 0.5) / usage(0.15, 0.0))
    dl_b_p = np.log(usage(tx / 100, 0.0, zb5) / usage(0.15, 0.0, zb5))
    p(f"[PME15 → {tx} % + 50 %] coût d'usage pour une société dont le bénéfice reste sous 42 500 € : équipements "
      f"{100*dl_eq_p:+.1f} %, bâtiments {100*dl_b_p:+.1f} %")
    REEL["pme15"] = {"dln_usage_equipement": dl_eq_p, "dln_usage_batiment": dl_b_p}
perte_tr = TR_C
p(f"[PME15 trésorerie] les sociétés qui perdent le taux réduit perdent {TR_C:.2f} Md€/an de trésorerie ; avec une "
  f"sensibilité de l'investissement à la trésorerie de 0,1 à 0,3 [H], −{0.1*TR_C:.2f} à −{0.3*TR_C:.2f} Md€/an "
  "d'investissement chez elles, à comparer à l'investissement suscité par la déduction")
REEL["pme15"]["investissement_tresorerie"] = [-0.1 * TR_C, -0.3 * TR_C]
J["effets_reels"] = REEL
J["effets_reels_hyp"] = {"K_equipement": K_EQ, "K_batiment": K_BAT, "part_revenu_equipement": S_EQ,
                         "part_revenu_batiment": S_BAT, "elasticite_stock_equipement": EPS,
                         "elasticite_stock_batiment": EPS_B, "elasticite_investissement_court_terme": EI}

# comparaison des configurations (euros courants sauf mention)
p("")
p("[COMPARAISON] coût brut 2028 ; coût permanent (euros de 2027) ; coût actualisé par année d'achats (5 %) ; cumul 2027-2036 ; "
  "capital en plus (central) ; capital par Md€ cumulé sur dix ans")
CMP = {}
cum = lambda serie: float(np.sum(serie[:10]))
for k, nom, serie, perm_, va_ in (
        ("ded50", "Déduction de 50 % (calendrier B)", DED[CLE]["mix"], perm(0.5), va(0.5)),
        ("ded100", "Déduction de 100 % dès 2027", DED["D"]["mix"], perm(1.0), va(1.0)),
        ("taux24", "Taux à 24 % dès 2027", 1 * POINT * CR, POINT, POINT),
        ("taux23", "Taux à 23 % dès 2027", 2 * POINT * CR, 2 * POINT, 2 * POINT),
        ("taux22", "Taux à 22 % dès 2027", 3 * POINT * CR, 3 * POINT, 3 * POINT),
        ("combi23", "23 % + déduction de 50 %", 2 * POINT * CR + DED[CLE]["mix"] * 23 / 25, 2 * POINT + perm(.5) * .92,
         2 * POINT + va(.5) * .92)):
    dk = REEL[k]["central"]["dK_equipement"] + REEL[k]["central"]["dK_batiment"]
    CMP[k] = {"nom": nom, "cout_2027": float(serie[0]), "cout_2028": float(serie[1]), "cout_permanent_2027": perm_,
              "cout_actualise_millesime": va_, "cumul_2027_2036": cum(serie), "dK_central": dk,
              "dK_bas": REEL[k]["bas"]["dK_equipement"] + REEL[k]["bas"]["dK_batiment"],
              "dK_haut": REEL[k]["haut"]["dK_equipement"] + REEL[k]["haut"]["dK_batiment"],
              "dK_par_Md_cumul10": dk / cum(serie), "dY_pct": [REEL[k][n]["dY_pct"] for n in ("bas", "central", "haut")],
              "tmei_fp": TEF[k]["tmei_fp"], "tmei_dette": TEF[k]["tmei_dette"]}
    c = CMP[k]
    p(f"[CMP] {nom:34s} 2027 {c['cout_2027']:5.2f} ; 2028 {c['cout_2028']:5.2f} ; permanent {perm_:5.2f} ; actualisé {va_:5.2f} ; "
      f"cumul 10 ans {c['cumul_2027_2036']:5.1f} ; ΔK {dk:4.1f} ({c['dK_bas']:.1f}–{c['dK_haut']:.1f}) Md€ ; "
      f"{c['dK_par_Md_cumul10']:.2f} Md€ de capital par Md€ cumulé ; TMEI {100*c['tmei_fp']:.1f} %")
r_ = CMP["ded50"]["dK_par_Md_cumul10"] / CMP["taux23"]["dK_par_Md_cumul10"]
p(f"[CMP] par euro dépensé sur dix ans, la déduction de 50 % accumule {r_:.1f} fois plus de capital (équipements et bâtiments) "
  "que la baisse de deux points ; Chodorow-Reich, Zidar et Zwick (2024) trouvent 1,5 fois dans un modèle complet "
  "(tous actifs, toutes les sociétés de capitaux)")
J["comparaison"] = CMP

# ============================================================================ 7. table annuelle pour le bouclage
p("")
p("=" * 100)
p("7. TABLE ANNUELLE (exercices ; + = recette publique, − = coût ; Md€ courants)")
ded = DED[CLE]["mix"][:NA]
annuel = {}
for t, a in enumerate(ANS):
    annuel[str(a)] = {
        "is_fin_taux_reduit": round(float(tr_serie[t]), 3),
        "is_deduction_50": round(float(-ded[t]), 3),
        "is_point_taux_normal_base_totale": round(float(-pt_tot[t]), 3),
        "is_point_taux_normal_base_normale": round(float(-pt_norm[t]), 3),
        "is_point_interaction_deduction": round(float(inter[t]), 3),
        "memo_fin_contribution_exceptionnelle": -7.0,
    }
    p(f"[ANNUEL] {a} : taux réduit {tr_serie[t]:+.2f} ; déduction 50 % {-ded[t]:+.2f} ; un point de taux normal "
      f"{-pt_tot[t]:+.2f} (base normale seule {-pt_norm[t]:+.2f}) ; interaction par point {inter[t]:+.3f} ; "
      f"[mémoire] contribution exceptionnelle −7,0")
J["annuel"] = annuel
J["annuel_caisse"] = {str(a): {k: (annuel[str(a - 1)][k] if str(a - 1) in annuel else 0.0)
                               for k in annuel[str(a)] if k.startswith("is_")} for a in ANS}
J["annuel_notes"] = {
    "convention": "années d'exercice ; en caisse, l'essentiel arrive l'année suivante (solde et acomptes) : annuel_caisse = décalage d'un an",
    "is_fin_taux_reduit": "taux réduit à 20 % en 2027, aligné sur le taux normal dès 2028, compté jusqu'à 25 % ; central (84 % du statique), bornes dans taux_reduit",
    "is_deduction_50": "25 % en 2027, 50 % dès 2028 ; au taux de 25 % ; part imposable 75 % ; plan actuel moitié linéaire moitié dégressif",
    "is_point_taux_normal_base_totale": "coût statique d'un point de baisse du taux normal, une fois le taux réduit aligné (dès 2028)",
    "is_point_taux_normal_base_normale": "coût d'un point si la baisse s'appliquait en 2027, quand le taux réduit n'est pas encore aligné",
    "is_point_interaction_deduction": "recette par point de baisse : la déduction coûte moins quand le taux baisse (coût x taux/25)",
    "memo_fin_contribution_exceptionnelle": "droit en vigueur (fin après l'exercice 2026), écart au niveau de 2026, NON compté dans nos réformes",
}
# scénarios indicatifs du solde IS (le taux et son calendrier sont choisis au bouclage)
SCEN = {}
for tx, x in CIBLES.items():
    for nom, cal in (("2028", lambda a: x if a >= 2028 else 0),
                     ("progressif", lambda a: min(x, max(0, (a - 2027) // 2)))):
        sol = []
        for t, a in enumerate(ANS):
            pts = cal(a)
            sol.append(tr_serie[t] - ded[t] * (TAU - pts / 100) / TAU - pts * pt_tot[t])
        SCEN[f"{tx}_{nom}"] = dict(zip(ANS, [round(float(v), 3) for v in sol]))
        p(f"[SOLDE IS {tx} % {nom}] " + " ; ".join(f"{a} {v:+.2f}" for a, v in zip(ANS, sol)
                                                if a in (2027, 2028, 2029, 2030, 2031, 2033, 2035, 2040)))
J["scenarios_solde_is"] = SCEN
J["scenarios_notes"] = ("solde IS = fin du taux réduit − déduction (au taux final) − points x coût du point ; "
                        "« 2028 » : baisse entière en 2028 ; « progressif » : un point en 2029, deux en 2031, trois en 2033 ; "
                        "le reste à financer (solde négatif) vient des recettes foncières au bouclage")

(OUT / "is.json").write_text(json.dumps(J, ensure_ascii=False, indent=1,
                                        default=lambda o: o.item() if hasattr(o, "item") else list(o)), encoding="utf-8")
(OUT / "is_calculs.txt").write_text("\n".join(L) + "\n", encoding="utf-8")
print("\n".join(L))
