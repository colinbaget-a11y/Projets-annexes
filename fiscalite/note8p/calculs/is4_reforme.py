"""Bloc IS, version 4 (note8p/CONSIGNES_V4.md, section IS et « Ajout de l'auteur : suppression du CIR »).

Lancer depuis fiscalite/ : python3 note8p/calculs/is4_reforme.py   (après is3_reforme.py, dont il lit is3.json)
  -> note8p/sorties/is4.json        (chiffres v4 ; table `annuel_caisse` 2027-2040 pour le bouclage)
  -> note8p/sorties/is4_calculs.txt (journal)

Ce qui change par rapport à is3 :
  1. dette : décomposition du TMEI négatif, corrections possibles (rabot des intérêts, intérêts réels, seuil 212 bis) ;
  2. pertes : valeur de la déduction pour une société déficitaire (l'indexation des déficits est traitée ailleurs) ;
  3. CIR supprimé (décision de l'auteur) : il remplace le « CIR recentré » du paquet (pas de double compte) ;
     recette statique, calendrier d'encaissement des créances (imputation N+1 à N+3, restitution en N+4, remboursement
     immédiat des PME), rendement réalisable, effet attendu sur la R&D ;
  4. niches : rendement statique et rendement prudent réalisable, en caisse.
Années : exercices dans `annuel`, encaissement dans `annuel_caisse` (exercice + 1, sauf calendrier propre du CIR).
Statuts : E empirique publié, S simulation, H hypothèse, C choix.
"""
import json
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "note8p" / "sorties"
I3 = json.loads((OUT / "is3.json").read_text(encoding="utf-8"))
L, J = [], {}
p = L.append
ANS = list(range(2027, 2041))
G, TAU, PI, RR = 0.03, 0.25, 0.02, 0.05
RHO = (1 + RR) * (1 + PI) - 1                      # 7,1 % nominal
DEP = 2029                                          # départ retenu de la déduction (25 % en 2029, 50 % ensuite) [C]
PIB27 = 2991.0 * 1.04                               # PIB 2025 porté en 2027 (ordre de grandeur pour les ratios)


def zplan(d, r):
    return float(sum(dk / (1 + r) ** k for k, dk in enumerate(d)))


import sys
sys.path.insert(0, str(ROOT / "is"))
import simulation_is as sim  # noqa: E402

LIN, DEG = list(sim.plan("lineaire")), list(sim.plan("degressif"))


def zmix(r, b=0.0):
    return b + (1 - b) * (zplan(LIN, r) + zplan(DEG, r)) / 2


def cout_capital(b, rho, tau=TAU, delta=0.14):
    zz = zmix(rho, b)
    return (1 - tau * zz) * (rho - PI + delta * (1 + PI)) / ((1 - tau) * (1 + PI)) - delta


def tm(pc):
    return (pc - RR) / pc


# contrôle : on retrouve les TMEI de is3
T3 = I3["taux_effectifs"]
chk = (tm(cout_capital(0.5, RHO)), tm(cout_capital(0.5, RHO * (1 - TAU))))
p(f"0. CONTRÔLE : TMEI ded50 fp {100*chk[0]:.1f} (is3 {100*T3['ded50']['fp']:.1f}) ; dette {100*chk[1]:.1f} "
  f"(is3 {100*T3['ded50']['dette']:.1f})")

# =========================================================================== 1. dette
p("")
p("1. DETTE : coût du capital (p), TMEI et écart fonds propres / emprunt, selon la fraction b déduite tout de suite")
DET = {}
for b in (0.0, 0.5, 1.0):
    pf, pd = cout_capital(b, RHO), cout_capital(b, RHO * (1 - TAU))
    pm = 2 / 3 * pf + 1 / 3 * pd
    DET[str(b)] = {"p_fp": pf, "p_dette": pd, "p_mixte": pm, "tmei_fp": tm(pf), "tmei_dette": tm(pd),
                   "tmei_mixte": tm(pm), "ecart_points": 100 * (pf - pd)}
    p(f"[b={b:.1f}] p fp {100*pf:.2f} % ; p dette {100*pd:.2f} % ; écart {100*(pf-pd):.2f} pt ; TMEI fp {100*tm(pf):.1f} ; "
      f"dette {100*tm(pd):.1f} ; 1/3 dette {100*tm(pm):.1f}")
# lecture : un projet financé par emprunt est entrepris dès que son rendement avant impôt dépasse p_dette < r
# décomposition pour b = 0,5 : effet de la déduction seule (sans intérêts déductibles, rho = i) et effet des intérêts
p_sans_int = cout_capital(0.5, RHO * 1.0)                      # emprunt dont les intérêts ne seraient pas déductibles
DET["decomposition_b05"] = {
    "tmei_fp": tm(cout_capital(0.5, RHO)),
    "subvention_pts_dette_auj": 100 * (RR - DET["0.0"]["p_dette"]),
    "subvention_pts_dette_ded50": 100 * (RR - DET["0.5"]["p_dette"]),
    "subvention_pts_dette_ded100": 100 * (RR - DET["1.0"]["p_dette"]),
}
p(f"[LECTURE] rendement avant impôt minimal d'une machine financée par emprunt : {100*DET['0.0']['p_dette']:.2f} % aujourd'hui, "
  f"{100*DET['0.5']['p_dette']:.2f} % avec b = 0,5, {100*DET['1.0']['p_dette']:.2f} % avec b = 1, pour un rendement exigé de 5 %")
# intuition chiffrée : machine de 100 financée par 100 d'emprunt ; l'État prend tout de suite tau*b*100 à sa charge
# (déduction), mais les intérêts restent déductibles sur 100.
INT = {
    "pret": 100.0, "aide_immediate_b05": TAU * 0.5 * 100, "aide_immediate_b1": TAU * 100,
    "interets_deduits_an1": RHO * 100, "economie_impot_interets_an1": TAU * RHO * 100,
}
p(f"[INTUITION] 100 empruntés : la déduction rend {INT['aide_immediate_b05']:.1f} tout de suite (b = 0,5), "
  f"{INT['aide_immediate_b1']:.0f} (b = 1) ; les intérêts restent déduits sur 100, soit {INT['economie_impot_interets_an1']:.2f} "
  f"d'impôt en moins par an")


def tmei_dette_rabot(b, h, reel=False):
    """Intérêts déductibles à (1 - h), ou seulement leur part réelle (i - pi) si reel."""
    if reel:
        rho_d = RHO - TAU * (RHO - PI)
    else:
        rho_d = RHO * (1 - TAU * (1 - h))
    pd = cout_capital(b, rho_d)
    pf = cout_capital(b, RHO)
    return tm(pd), tm(2 / 3 * pf + 1 / 3 * pd)


def cherche(cible, f):
    lo, hi = 0.0, 1.0
    for _ in range(60):
        m = (lo + hi) / 2
        if f(m) < cible:
            lo = m
        else:
            hi = m
    return (lo + hi) / 2


h_retour = cherche(DET["0.0"]["tmei_dette"], lambda h: tmei_dette_rabot(0.5, h)[0])
h_mixte0 = cherche(0.0, lambda h: tmei_dette_rabot(0.5, h)[1])
h_mixte_auj = cherche(DET["0.0"]["tmei_mixte"], lambda h: tmei_dette_rabot(0.5, h)[1])
reel = tmei_dette_rabot(0.5, 0, reel=True)
CORR = {
    "rabot_general_pour_revenir_au_tmei_dette_actuel": h_retour,
    "rabot_general_pour_tmei_mixte_nul": h_mixte0,
    "rabot_general_pour_tmei_mixte_actuel": h_mixte_auj,
    "interets_reels_seulement_tmei_dette_mixte": reel,
    "au_dela_du_plafond_212bis_tmei_dette": tm(cout_capital(0.5, RHO)),
    "recette_par_10pc_de_rabot": "0,025 x charges financières nettes déduites (montant non vérifié ici)",
}
p(f"[CORRECTIONS] rabot général des intérêts nets nécessaire pour revenir au TMEI-dette actuel ({100*DET['0.0']['tmei_dette']:.0f} %) : "
  f"{100*h_retour:.0f} % ; pour un TMEI mixte nul : {100*h_mixte0:.0f} % ; pour le TMEI mixte actuel (7,6 %) : {100*h_mixte_auj:.0f} %")
p(f"[CORRECTIONS] intérêts réels seulement (i − π) : TMEI dette {100*reel[0]:.1f} %, mixte {100*reel[1]:.1f} % ; "
  f"société au-delà du plafond 212 bis : intérêt marginal non déductible, TMEI dette = fonds propres = {100*CORR['au_dela_du_plafond_212bis_tmei_dette']:.1f} %")
# seuil 212 bis : quelle dette faut-il pour atteindre 3 M€ ou 1 M€ de charges nettes ?
for s in (3.0, 1.0):
    p(f"[212 bis] seuil de {s:.0f} M€ de charges nettes = environ {s/0.04:.0f} M€ de dette à 4 % (ou {s/0.06:.0f} M€ à 6 %)")
CORR["dette_equivalente_seuils_MEUR"] = {"3": [3 / 0.06, 3 / 0.04], "1": [1 / 0.06, 1 / 0.04]}
J["dette"] = {"tmei_et_ecart": DET, "intuition_100": INT, "corrections": CORR}

# =========================================================================== 2. pertes
p("")
p("2. PERTES : valeur actualisée (5 %) de la déduction de 50 % pour 100 d'achat, selon le délai avant retour aux bénéfices")
DEP_PLAN = [(a + b_) / 2 for a, b_ in zip(LIN, DEG)]
nouv = [0.5 + 0.5 * DEP_PLAN[0]] + [0.5 * x for x in DEP_PLAN[1:]]


def va_decale(d, n, r=0.05, indexe=False):
    """Déductions inutilisables avant l'année n : reportées (non indexées) et imputées en n (sans plafond)."""
    if indexe:
        return sum(x / (1 + r) ** k for k, x in enumerate(d))
    tot = sum(x for x in d[:n]) / (1 + r) ** n if n > 0 else 0.0
    return tot + sum(x / (1 + r) ** k for k, x in enumerate(d) if k >= n)


PERT = {}
for n in (0, 1, 3, 5, 8):
    v = TAU * 100 * (va_decale(nouv, n) - va_decale(DEP_PLAN, n))
    PERT[n] = v
p("   " + " ; ".join(f"{n} an(s) : {v:.2f}" for n, v in PERT.items()) +
  f" ; avec déficits indexés au taux d'actualisation : {PERT[0]:.2f} quel que soit le délai")
p("   lecture : à 100 d'achat, l'avantage perd un tiers après un an de pertes, les trois quarts après trois ans, et disparaît au-delà de la durée du plan")
D_NOUV = 113.0                                       # déficits de l'exercice 2022 (DGFiP n° 51), Md€
J["pertes"] = {"va_avantage_pour_100_selon_delai": PERT, "deficits_2022": D_NOUV,
               "part_imposable_hypothese": 0.75,
               "part_investissement_deficitaires": "non mesurée ; 25 % implicite dans l'hypothèse de 75 % imposable [H]"}

# =========================================================================== 3. suppression du CIR
p("")
p("3. SUPPRESSION DU CIR (dépenses engagées à compter du 1er janvier 2028)")
CIR27 = 7.4          # coût projeté 2027 (Sénat, NP « Remboursements et dégrèvements », PLF 2027) [E] ; VM PLF 2026 : 8,0 en 2026
CIR27_HAUT = 8.04 * (1 + G)
PME = 0.31           # part des PME dans la créance de CIR-recherche 2023 (MESRE, nov. 2025 : 2,24 sur 7,32 Md€) [E]
# Profil d'encaissement d'un millésime de créances (part du millésime v qui pèse sur le budget en v+k) :
#   2024 : restitué 4,7 / imputé 3,0 sur 7,7 Md€ (CIR + CII ; Sénat, NP PLF 2027, d'après la DGFiP) [E]
#   remboursement immédiat des PME (et JEI, entreprises nouvelles) : ≈ 36 % (31 % de CIR-recherche des PME + CII) [H sur E]
#   restitution du reliquat en N+4 : 61 % − 36 % ≈ 25 % ; imputation 39 %, répartie 80/12/8 % sur N+1 à N+3 [H]
W = {1: 0.36 + 0.39 * 0.80, 2: 0.39 * 0.12, 3: 0.39 * 0.08, 4: 0.61 - 0.36}
assert abs(sum(W.values()) - 1) < 1e-9


def creance(v, base=CIR27):
    # millésime v : coût 2027 ≈ créance 2026 ; +3 %/an
    return base * (1 + G) ** (v - 2026)


cir_stat, cir_meca, cir_prud, cir_cent = {}, {}, {}, {}
F_PRUD, F_CENT = 0.80, 0.90          # réactions [H] (voir is4.md, § 3)
for a in ANS:
    stat = sum(W[k] * creance(a - k) for k in W) if a >= 2029 else 0.0      # coût total de l'année, perdu dès 2029
    meca = sum(W[k] * creance(a - k) for k in W if a - k >= 2028)           # seuls les millésimes ≥ 2028 disparaissent
    cir_stat[a], cir_meca[a] = stat, meca
    cir_prud[a], cir_cent[a] = F_PRUD * meca, F_CENT * meca
p("[CIR] profil d'un millésime : " + " ; ".join(f"N+{k} {100*w:.0f} %" for k, w in W.items()))
p("[CIR] caisse (Md€) : " + " ; ".join(f"{a} stat {cir_stat[a]:.2f} / méca {cir_meca[a]:.2f} / prudent {cir_prud[a]:.2f}"
                                       for a in ANS if a in (2029, 2030, 2031, 2032, 2033, 2035, 2040)))
# effet sur la R&D et le PIB potentiel (ordre de grandeur, non compté)
CIR_PME = PME * CIR27
RD = {}
for nom, mult in (("bas", 0.9), ("haut", 1.5)):
    dR = mult * CIR_PME
    dS = dR / (0.15 + G)                          # dépréciation de la R&D 15 % [H]
    RD[nom] = {"multiplicateur": mult, "baisse_RD_PME_Md": dR, "baisse_stock_Md": dS,
               "PIB_prive_pct": 100 * (RR + 0.15) * dS / PIB27,
               "PIB_avec_externalites_pct": 100 * 2 * (RR + 0.15) * dS / PIB27}
p(f"[R&D] CIR des PME ≈ {CIR_PME:.2f} Md€ ; multiplicateur 0,9-1,5 (CNEPI, cité par le Sénat) : R&D des PME −{RD['bas']['baisse_RD_PME_Md']:.1f} à "
  f"−{RD['haut']['baisse_RD_PME_Md']:.1f} Md€/an ; stock −{RD['bas']['baisse_stock_Md']:.0f} à −{RD['haut']['baisse_stock_Md']:.0f} Md€ ; "
  f"PIB potentiel −{RD['bas']['PIB_prive_pct']:.2f} à −{RD['haut']['PIB_prive_pct']:.2f} % au rendement privé, "
  f"−{RD['bas']['PIB_avec_externalites_pct']:.2f} à −{RD['haut']['PIB_avec_externalites_pct']:.2f} % si le rendement social est double")
VAR_PME = (1 - PME) * CIR27
p(f"[VARIANTE] garder un crédit réservé aux PME : recette statique {VAR_PME:.1f} Md€ (2027) au lieu de {CIR27:.1f}")
J["cir_suppression"] = {
    "statique_2027": CIR27, "statique_2027_vm_plf2026": CIR27_HAUT, "part_pme_creance": PME,
    "profil_millesime": W, "facteurs_reaction": {"prudent": F_PRUD, "central": F_CENT},
    "caisse_statique": cir_stat, "caisse_mecanique": cir_meca, "caisse_prudent": cir_prud, "caisse_central": cir_cent,
    "effet_RD": RD, "variante_credit_pme_seul_statique_2027": VAR_PME,
    "tmei_RD": {"avec_CIR_30": -0.30 / (1 - TAU - 0.30), "sans_CIR": 0.0},
    "sources": ["Sénat, note de présentation « Remboursements et dégrèvements », PLF 2027 (coût 7,3 Md€ en 2025 exécuté, "
                ">7,4 en 2027 ; 2024 : 4,7 restitués, 3,0 imputés sur 7,7 ; règles art. 199 ter B)",
                "MESRE-DGRI, Le CIR en 2023 (nov. 2025) : créance 7,85 Md€, dont recherche 7,32 ; PME 2,24, ETI 2,10, GE 2,98 ; "
                "33 bénéficiaires au-delà de 100 M€ : 25 % de la créance recherche"],
}

# =========================================================================== 4. niches hors CIR, statique et prudent
p("")
p("4. NICHES HORS CIR (exercices 2028+, caisse 2029+) : statique et prudent réalisable")
NP3 = I3["niches_paquet"]
FACT = {  # mesure : (prudent, central) [H], justification dans is4.md
    "mecenat_reduction_vers_deduction": (0.85, 1.0),
    "credits_culture": (0.75, 0.9),
    "zonages_fermes_aux_entrants": (0.80, 1.0),
    "credit_famille": (0.90, 1.0),
}
nic_stat, nic_prud, nic_cent = {}, {}, {}
for a in ANS:
    ex = str(a - 1)
    s = sum(NP3[k]["serie"].get(ex, 0.0) for k in FACT) if a - 1 >= 2027 else 0.0
    nic_stat[a] = s
    nic_prud[a] = sum(FACT[k][0] * NP3[k]["serie"].get(ex, 0.0) for k in FACT) if a - 1 >= 2027 else 0.0
    nic_cent[a] = sum(FACT[k][1] * NP3[k]["serie"].get(ex, 0.0) for k in FACT) if a - 1 >= 2027 else 0.0
p("[NICHES] caisse : " + " ; ".join(f"{a} {nic_stat[a]:.2f} / prudent {nic_prud[a]:.2f}" for a in ANS if a in (2029, 2030, 2032, 2035, 2040)))
REG26 = sum(NP3[k]["montant_2026"] for k in FACT)
p(f"[NICHES] noyau hors CIR : {REG26:.2f} Md€ de 2026 statiques (l'ancien « CIR recentré », 0,97, est absorbé par la suppression)")

# =========================================================================== 4b. réinvestissement d'une partie de la recette du CIR
p("")
p("4b. RÉINVESTISSEMENT : options générales (coûts bruts par exercice ; caisse = exercice + 1)")
PART_IMP, R_ETAT = 0.75, sim.R_ETAT
I_EQ27 = sim.I1                                     # machines, équipements, TIC des SNF, 2027 (89,1 Md€)
PART_LOG_ACQ = 0.40                                 # part des logiciels acquis (et non produits en interne) [H]
I_LOG27 = PART_LOG_ACQ * 77.5 * (1 + G) ** 2        # FBCF logiciels et bases de données des SNF, 2025 (Insee 8.212) [E]
PLAN_LOG = [0.5 / 3, 1 / 3, 1 / 3, 0.5 / 3]         # logiciel acquis, linéaire 3 ans, prorata [H]
H_ = 60


def chemin_gen(I0, plans, bonus, h=H_):
    out = np.zeros(h + 12)
    for pl in plans:
        pl = np.array(pl)
        e0 = np.zeros(len(pl)); e0[0] = 1.0
        for t in range(h):
            b = bonus(t)
            out[t:t + len(pl)] += TAU * PART_IMP * I0 * (1 + G) ** t * (b * e0 + (1 - b) * pl - pl) / len(plans)
    return out[:h]


def sched(*paliers):
    """paliers : (année d'exercice, fraction) ; avant le premier palier, 0."""
    def f(t):
        a, b = 2027 + t, 0.0
        for an, fr_ in paliers:
            if a >= an:
                b = fr_
        return b
    return f


BASE = sched((2029, 0.25), (2030, 0.5))
P75 = sched((2029, 0.25), (2030, 0.5), (2033, 0.75))
P100 = sched((2029, 0.25), (2030, 0.5), (2033, 0.75), (2036, 1.0))
LOGB = sched((2031, 0.5))                           # logiciels acquis : 50 % dès l'exercice 2031
LOG100 = sched((2031, 0.5), (2033, 0.75), (2036, 1.0))
EQ = [LIN, DEG]
eq_base = chemin_gen(I_EQ27, EQ, BASE)
chk_ = [eq_base[t] for t in range(2, 6)]
p("[CONTRÔLE] équipements, départ 2029 : " + " ; ".join(f"{v:.2f}" for v in chk_) + " (is3 : 3,92 ; 7,16 ; 5,71 ; 4,54)")
OPT = {
    "a_logiciels_acquis_50_des_2031": chemin_gen(I_LOG27, [PLAN_LOG], LOGB),
    "b_equipements_75_des_2033": chemin_gen(I_EQ27, EQ, P75) - eq_base,
    "b_equipements_75_2033_100_des_2036": chemin_gen(I_EQ27, EQ, P100) - eq_base,
    "a_logiciels_acquis_50_2031_75_2033_100_2036": chemin_gen(I_LOG27, [PLAN_LOG], LOG100),
}


def perm_gen(I0, plans, b):
    return TAU * PART_IMP * b * I0 * (1 - np.mean([zplan(pl, G) for pl in plans]))


def va_gen(I0, plans, b, r=0.05):
    return TAU * PART_IMP * b * I0 * (1 - np.mean([zplan(pl, r) for pl in plans]))


PERMS = {"equip_50": perm_gen(I_EQ27, EQ, .5), "equip_75": perm_gen(I_EQ27, EQ, .75), "equip_100": perm_gen(I_EQ27, EQ, 1.),
         "log_50": perm_gen(I_LOG27, [PLAN_LOG], .5), "log_100": perm_gen(I_LOG27, [PLAN_LOG], 1.)}
VAS = {"equip_50": va_gen(I_EQ27, EQ, .5), "equip_100": va_gen(I_EQ27, EQ, 1.), "log_50": va_gen(I_LOG27, [PLAN_LOG], .5),
       "log_100": va_gen(I_LOG27, [PLAN_LOG], 1.)}
for k, v in OPT.items():
    p(f"[{k}] " + " ; ".join(f"{2027+t} {v[t]:.2f}" for t in range(2, 14) if abs(v[t]) > 0.005))
p("[PERMANENT, € 2027] " + " ; ".join(f"{k} {v:.2f}" for k, v in PERMS.items()))
p("[ACTUALISÉ, une année d'achats, 5 %] " + " ; ".join(f"{k} {v:.2f}" for k, v in VAS.items()))
p(f"[LOGICIELS] investissement acquis 2027 : {I_LOG27:.1f} Md€ (40 % de 77,5 Md€ de 2025 [H]) ; 1re année (2031) : {OPT['a_logiciels_acquis_50_des_2031'][4]:.2f}")

# effets réels (même méthode que is3 : stock ∝ coût d'usage^−ε, part imposable 75 %, Cobb-Douglas)
K_EQ_, D_EQ = 541.0, 0.14
D_LOG = 0.33
K_LOG = I_LOG27 / (1 + G) ** 2 / (D_LOG + G)        # stock acquis, régime établi [H]
PIB25 = 2991.0


def dlusage(b, plans, r=0.05):
    zz = np.mean([zplan(pl, r) for pl in plans])
    return np.log((1 - TAU * (b + (1 - b) * zz)) / (1 - TAU * zz))


EFF = {}
for nom, (b_eq, b_log) in {"ded50_equip": (.5, 0), "ded75_equip": (.75, 0), "ded100_equip": (1., 0),
                          "log50": (0, .5), "log100": (0, 1.)}.items():
    res = {}
    for eps_n, eps in (("bas", .5), ("central", 1.), ("haut", 1.6)):
        dke = -eps * dlusage(b_eq, EQ) * PART_IMP * K_EQ_ if b_eq else 0.0
        dkl = -eps * dlusage(b_log, [PLAN_LOG]) * PART_IMP * K_LOG if b_log else 0.0
        dy = (0.05 + D_EQ) * dke / PIB25 + (0.05 + D_LOG) * dkl / PIB25
        res[eps_n] = {"dK": dke + dkl, "dY_pct": 100 * dy}
    res["dln_usage"] = float(dlusage(b_eq, EQ) if b_eq else dlusage(b_log, [PLAN_LOG]))
    EFF[nom] = res
    p(f"[EFFET {nom}] coût d'usage {100*res['dln_usage']:+.2f} % ; ΔK {res['central']['dK']:.1f} Md€ ; PIB {res['central']['dY_pct']:+.3f} % "
      f"({res['bas']['dY_pct']:+.3f} à {res['haut']['dY_pct']:+.3f})")

# carry-back renforcé (option c) : chiffrage simple [H]
CB = {"deficits_reportes_en_arriere_Md": [5.0, 10.0], "creances_annuelles_Md": [TAU * 5, TAU * 10],
      "tresorerie_1re_annee_Md": [TAU * 5, TAU * 10],
      "permanent_Md": [TAU * 5 * (0.0325 * 3 + 0.10), TAU * 10 * (0.0325 * 3 + 0.20)]}
p(f"[CARRY-BACK] 3 exercices, créance remboursable tout de suite : trésorerie 1re année {CB['tresorerie_1re_annee_Md'][0]:.2f}-"
  f"{CB['tresorerie_1re_annee_Md'][1]:.2f} Md€ ; permanent {CB['permanent_Md'][0]:.2f}-{CB['permanent_Md'][1]:.2f} Md€ [H] ; "
  "ne touche pas les jeunes entreprises sans bénéfices passés")

# paquet recommandé : logiciels acquis dans la déduction (2031) + paliers 75 % (2033) et 100 % (2036) pour tous
pkg = OPT["a_logiciels_acquis_50_2031_75_2033_100_2036"] + OPT["b_equipements_75_2033_100_des_2036"]
PKG = {"exercices": {2027 + t: float(pkg[t]) for t in range(14)},
       "permanent_2027": PERMS["equip_100"] - PERMS["equip_50"] + PERMS["log_100"],
       "effet_PIB_pct": {k: EFF["ded100_equip"][k]["dY_pct"] - EFF["ded50_equip"][k]["dY_pct"] + EFF["log100"][k]["dY_pct"]
                         for k in ("bas", "central", "haut")}}
p("[PAQUET] coût en plus (exercices) : " + " ; ".join(f"{a} {v:.2f}" for a, v in PKG["exercices"].items() if v > 0.005)
  + f" ; permanent {PKG['permanent_2027']:.2f} Md€ (2027) ; PIB en plus {PKG['effet_PIB_pct']['central']:+.3f} %")
J["reinvestissement"] = {"options_exercices": {k: {2027 + t: float(v[t]) for t in range(14)} for k, v in OPT.items()},
                         "permanents_2027": PERMS, "actualises_millesime": VAS, "effets": EFF, "carry_back": CB,
                         "paquet_recommande": PKG, "hyp": {"part_logiciels_acquis": PART_LOG_ACQ, "plan_logiciel": PLAN_LOG,
                                                          "I_logiciels_acquis_2027": I_LOG27, "K_logiciels_acquis": K_LOG}}

# =========================================================================== 5. table en caisse
A3 = I3["annuel"]
caisse = {}
for a in ANS:
    ex = str(a - 1)
    d = {
        "is_fin_taux_reduit_prudent": A3[ex]["is_fin_taux_reduit_prudent"] if ex in A3 else 0.0,
        "is_fin_taux_reduit_statique": A3[ex]["is_fin_taux_reduit_statique"] if ex in A3 else 0.0,
        f"is_deduction_50_depart_{DEP}": A3[ex][f"is_deduction_50_depart_{DEP}"] if ex in A3 else 0.0,
        "is_niches_hors_cir_statique": nic_stat[a],
        "is_niches_rendement_prudent_realisable": nic_prud[a],
        "is_niches_hors_cir_central_realisable": nic_cent[a],
        "is_cir_suppression_statique": cir_stat[a],
        "is_cir_suppression_realisable_mecanique": cir_meca[a],
        "is_cir_suppression_realisable_prudent": cir_prud[a],
        "memo_boite_a_brevets_statique_non_comptee": I3["niches_paquet"]["boite_a_brevets"]["serie"].get(ex, 0.0),
    }
    d["is_reinvest_logiciels_acquis"] = -float(pkg[a - 1 - 2027] - OPT["b_equipements_75_2033_100_des_2036"][a - 1 - 2027]) if a - 1 >= 2027 else 0.0
    d["is_reinvest_deduction_75_puis_100"] = -float(OPT["b_equipements_75_2033_100_des_2036"][a - 1 - 2027]) if a - 1 >= 2027 else 0.0
    d["is_solde_bloc_prudent_avant_reinvestissement"] = (d["is_fin_taux_reduit_prudent"] + d[f"is_deduction_50_depart_{DEP}"]
                                  + d["is_niches_rendement_prudent_realisable"] + d["is_cir_suppression_realisable_prudent"])
    d["is_recette_nette_bloc_is_prudent"] = (d["is_solde_bloc_prudent_avant_reinvestissement"]
                                             + d["is_reinvest_logiciels_acquis"] + d["is_reinvest_deduction_75_puis_100"])
    d["is_solde_bloc_statique"] = (d["is_fin_taux_reduit_statique"] + d[f"is_deduction_50_depart_{DEP}"]
                                   + d["is_niches_hors_cir_statique"] + d["is_cir_suppression_statique"])
    caisse[str(a)] = {k: round(float(v), 3) for k, v in d.items()}
p("")
p(f"5. TABLE EN CAISSE (Md€ courants ; déduction départ {DEP} ; + = recette)")
for a in ANS:
    c = caisse[str(a)]
    p(f"{a} : TR {c['is_fin_taux_reduit_prudent']:+.2f} ; déd. {c[f'is_deduction_50_depart_{DEP}']:+.2f} ; niches prud. "
      f"{c['is_niches_rendement_prudent_realisable']:+.2f} (stat. {c['is_niches_hors_cir_statique']:+.2f}) ; CIR prud. "
      f"{c['is_cir_suppression_realisable_prudent']:+.2f} (stat. {c['is_cir_suppression_statique']:+.2f}) ; solde prudent {c['is_solde_bloc_prudent_avant_reinvestissement']:+.2f} ; réinvesti {c['is_reinvest_logiciels_acquis']+c['is_reinvest_deduction_75_puis_100']:+.2f} ; NET {c['is_recette_nette_bloc_is_prudent']:+.2f}")
J["annuel_caisse"] = caisse
J["annuel_caisse_notes"] = {
    "convention": "années d'encaissement ; exercices + 1 (solde et acomptes), sauf CIR (profil des créances)",
    "is_fin_taux_reduit_prudent": "20 % en 2027, 25 % dès 2028 (exercices) ; coût officiel 2019 actualisé",
    f"is_deduction_50_depart_{DEP}": "coût brut ; 25 % pour l'exercice 2029, 50 % ensuite",
    "is_niches_hors_cir_statique": "mécénat, crédits culture, zonages (extinction sur 8 ans), crédit famille ; Voies et moyens PLF 2026",
    "is_niches_rendement_prudent_realisable": "idem, après réaction : facteurs 0,85 / 0,75 / 0,80 / 0,90 [H] ; LIGNE À RETENIR",
    "is_cir_suppression_statique": "coût total du CIR de l'année (7,4 Md€ en 2027, Sénat), comme si tout disparaissait en 2029",
    "is_cir_suppression_realisable_mecanique": "millésimes de créances ≥ 2028 seulement ; stock ancien imputé ou restitué jusqu'en 2031",
    "is_cir_suppression_realisable_prudent": "mécanique x 0,80 (réactions) ; LIGNE À RETENIR",
    "is_reinvest_logiciels_acquis": "logiciels acquis dans la déduction : 50 % dès l'exercice 2031, 75 % en 2033, 100 % en 2036",
    "is_reinvest_deduction_75_puis_100": "surcoût du relèvement de la déduction des équipements : 75 % dès 2033, 100 % dès 2036",
    "is_solde_bloc_prudent_avant_reinvestissement": "taux réduit + déduction 50 % + niches prudentes + CIR prudent",
    "is_recette_nette_bloc_is_prudent": "solde prudent après réinvestissement : LIGNE À RETENIR AU BOUCLAGE",
    "memo_boite_a_brevets": "statique, base mobile, hors bouclage prudent",
    "hors_table": "fin de la contribution exceptionnelle (−7 Md€/an vs 2026) et extinction du CII : droit en vigueur",
}
# régime permanent (euros 2027)
PERM50 = I3["deduction"]["cout_permanent_2027"]["50"]
TRP = I3["taux_reduit"]["prudent_2027"]
NIC27 = sum(FACT[k][0] * NP3[k]["montant_2026"] for k in FACT) * (1 + G)
CIRP27 = F_PRUD * CIR27
MARGE = {"taux_reduit": TRP, "niches_hors_cir_prudent": NIC27, "cir_prudent": CIRP27, "deduction": -PERM50,
         "total": TRP + NIC27 + CIRP27 - PERM50, "reinvesti": -PKG["permanent_2027"],
         "net_apres_reinvestissement": TRP + NIC27 + CIRP27 - PERM50 - PKG["permanent_2027"]}
p(f"[RÉGIME PERMANENT, € 2027] taux réduit {TRP:.2f} + niches prudentes {NIC27:.2f} + CIR prudent {CIRP27:.2f} − déduction "
  f"{PERM50:.2f} = {MARGE['total']:.2f} Md€/an ; réinvesti {PKG['permanent_2027']:.2f} ; net {MARGE['net_apres_reinvestissement']:.2f}")
J["marge_regime_permanent_2027_prudente"] = MARGE

(OUT / "is4.json").write_text(json.dumps(J, ensure_ascii=False, indent=1, default=float), encoding="utf-8")
(OUT / "is4_calculs.txt").write_text("\n".join(L) + "\n", encoding="utf-8")
print("\n".join(L))
