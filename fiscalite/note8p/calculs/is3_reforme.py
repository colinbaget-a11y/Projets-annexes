"""Bloc IS, version 3 (note8p/CONSIGNES_V3.md, 18/11/2026) : taux normal maintenu à 25 %.

Lancer depuis fiscalite/ : python3 note8p/calculs/is3_reforme.py
  -> note8p/sorties/is3.json       (tous les chiffres ; table `annuel` 2027-2040 en exercices, `annuel_caisse`)
  -> note8p/sorties/is3_calculs.txt (journal lisible)

Proposition [C] :
  1. suppression du taux réduit de 15 % : 20 % pour l'exercice 2027, 25 % dès 2028 ;
  2. déduction immédiate de 50 % des équipements neufs éligibles (le reste amorti selon le plan ordinaire), introduite
     à 25 % la première année puis 50 % ; séries pour un départ en 2027, 2028 ou 2029 (choix au bouclage) ;
  3. paquet de rationalisation des niches de l'IS (Voies et moyens, tome II, PLF 2026), dès les exercices 2028.

Parcimonie (ajout du 18/11/2026) : effets mécaniques (statiques) seulement pour les recettes ; aucune fuite ni décote
comportementale ad hoc ; effet réel limité au stock de capital (élasticité au coût d'usage) et au PIB potentiel
Cobb-Douglas ; les effets non calibrables (trésorerie des PME, R&D des grands groupes, relocalisation des brevets) sont
décrits, pas chiffrés.

Mécanique reprise de is/simulation_is.py (importé, non modifié) et de note8p/calculs/is_reforme.py (fonctions recopiées
pour ne pas réécrire is.json). Md€ courants, +3 %/an après 2027 ; part de l'investissement éligible faite par des
sociétés imposables : 75 % [H] ; plan actuel moitié linéaire, moitié dégressif [H].
"""
import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]          # fiscalite/
sys.path.insert(0, str(ROOT / "is"))
import simulation_is as sim  # noqa: E402

OUT = ROOT / "note8p" / "sorties"
L, J = [], {}
p = L.append

TAU, G, R_ENT, R_ETAT, PART = 0.25, sim.G, sim.R, sim.R_ETAT, 0.75
I1 = sim.I1                                          # investissement éligible 2027 (89,1 Md€)
ANS = list(range(2027, 2041))
NA, H = len(ANS), 60
CR = (1 + G) ** np.arange(H)
PLANS = {"lin": sim.plan("lineaire"), "deg": sim.plan("degressif")}
E0 = np.eye(1, len(PLANS["lin"]), 0).ravel()
PIB25, PIB27 = 2991.0, sim.PIB_2027


def fr(x, d=1):
    return f"{x:,.{d}f}".replace(",", " ").replace(".", ",").replace("-", "−")


def z(d, r=R_ENT):
    return float(sum(dk / (1 + r) ** k for k, dk in enumerate(d)))


def zmix(r=R_ENT, b=0.0):
    return b + (1 - b) * (z(PLANS["lin"], r) + z(PLANS["deg"], r)) / 2


# =========================================================================== 0. bases
B_N = sim.BASE_NORMALE * sim.AB
B_R = sim.BASE_REDUITE * sim.AB
POINT = (B_N + B_R) / 100
p("0. BASES : bénéfice 2027 au taux normal %.1f, au taux réduit %.1f Md€ ; un point de taux normal %.2f Md€" % (B_N, B_R, POINT))
J["bases_2027"] = {"benefice_taux_normal": B_N, "benefice_taux_reduit": B_R, "point_base_totale": POINT, "croissance": G}

# =========================================================================== 1. taux réduit
TR_STAT = 0.10 * B_R                                 # mécanique : 10 points sur la base imposée à 15 %
TR_PRUD = sim.REDUIT[0]                              # coût officiel 2019 (2,2 Md€ pour 13 points) ramené à 10 points
CAL_TR = {2027: 0.5}                                 # 20 % en 2027 (5 points sur 10), 25 % dès 2028
tr_prud = np.array([CAL_TR.get(a, 1.0) * TR_PRUD * CR[t] for t, a in enumerate(ANS)])
tr_stat = np.array([CAL_TR.get(a, 1.0) * TR_STAT * CR[t] for t, a in enumerate(ANS)])
p("")
p(f"1. TAUX RÉDUIT (supprimé : 20 % en 2027, 25 % dès 2028) — à plein en 2027 : statique {TR_STAT:.2f} Md€ ; prudent {TR_PRUD:.2f} "
  "(chiffre officiel 2019 actualisé). Série prudente retenue pour le bouclage.")
p("   " + " ; ".join(f"{a} {v:.2f}–{w:.2f}" for a, v, w in zip(ANS, tr_prud, tr_stat) if a in (2027, 2028, 2030, 2035, 2040)))
NB_EQ = sim.BASE_REDUITE * 1e9 / 42_500
cas_tr = {B: 0.10 * min(B, 42_500) for B in (10_000, 20_000, 30_000, 42_500, 60_000, 150_000)}
p("   perte par société = 10 % du bénéfice jusqu'à 42 500 € (au plus 4 250 €/an) : " + " ; ".join(
    f"{fr(b,0)} € → +{fr(v,0)} €" for b, v in cas_tr.items()))
p(f"   bénéficiaires : 760 000 en 2019 (CPO 2023) ; au moins {fr(NB_EQ,0)} sociétés en équivalent plafond (base 2025)")
J["taux_reduit"] = {"statique_2027": TR_STAT, "prudent_2027": TR_PRUD, "calendrier": {"2027": "20 %", "2028+": "25 %"},
                    "serie_prudente": dict(zip(ANS, tr_prud.tolist())), "serie_statique": dict(zip(ANS, tr_stat.tolist())),
                    "beneficiaires_2019": 760000, "societes_equivalent_plafond": NB_EQ,
                    "perte_par_societe": cas_tr, "perte_max": 4250}


# =========================================================================== 2. déduction immédiate
def chemin(reg, bonus, part=PART, tau=TAU, h=H):
    """Coût annuel pour l'État (+ = coût), t = 0 en 2027 ; bonus(t) fraction déduite tout de suite des achats de t."""
    anc = PLANS[reg]
    n = len(anc)
    c = np.zeros(h + n)
    for t in range(h):
        b = bonus(t)
        c[t:t + n] += tau * part * I1 * CR[t] * ((b * E0 + (1 - b) * anc) - anc)
    return c[:h]


def chemin_mix(bonus, **kw):
    return (chemin("lin", bonus, **kw) + chemin("deg", bonus, **kw)) / 2


def perm(b, reg="mix"):
    if reg == "mix":
        return (perm(b, "lin") + perm(b, "deg")) / 2
    return TAU * PART * b * I1 * (1 - z(PLANS[reg], G))


def va(b, r=R_ENT):
    return TAU * PART * I1 * b * (1 - zmix(r))


p("")
p("2. DÉDUCTION IMMÉDIATE DE 50 % (à 25 %) — coûts bruts par exercice, selon l'année de départ (25 % la 1re année)")
DEPARTS = {}
for s in (2027, 2028, 2029):
    t0 = s - 2027
    f_prog = (lambda t, t0=t0: 0.0 if t < t0 else (0.25 if t == t0 else 0.5))
    f_net = (lambda t, t0=t0: 0.0 if t < t0 else 0.5)
    brut = chemin_mix(f_prog)[:NA]
    net = chemin_mix(f_net)[:NA]
    permv = np.array([perm(0.5) * CR[t] if ANS[t] > s else (perm(0.25) * CR[t] if ANS[t] == s else 0.0) for t in range(NA)])
    vav = np.array([va(0.5) * CR[t] if ANS[t] > s else (va(0.25) * CR[t] if ANS[t] == s else 0.0) for t in range(NA)])
    DEPARTS[s] = {"brut": dict(zip(ANS, brut.tolist())), "brut_50_d_emblee": dict(zip(ANS, net.tolist())),
                  "permanent": dict(zip(ANS, permv.tolist())), "actualise_millesime": dict(zip(ANS, vav.tolist())),
                  "pic": float(brut.max()), "annee_pic": ANS[int(brut.argmax())], "cumul_2027_2040": float(brut.sum())}
    p(f"[DEPART {s}] brut " + " ; ".join(f"{a} {v:.2f}" for a, v in zip(ANS, brut) if v > 0.005 and a <= s + 8)
      + f" … 2040 {brut[-1]:.2f} ; pic {brut.max():.2f} ({ANS[int(brut.argmax())]}) ; 50 % d'emblée : pic {net.max():.2f}")
PERM50, PERM100 = perm(0.5), perm(1.0)
p(f"[PERMANENT] 50 % : {PERM50:.2f} Md€ de 2027 ({perm(0.5,'deg'):.2f}–{perm(0.5,'lin'):.2f}) ; 100 % : {PERM100:.2f}")
p(f"[ACTUALISÉ] coût d'une année d'achats : 50 % {va(0.5):.2f} Md€ à 5 % ({va(0.5, R_ETAT):.2f} au taux de l'État) ; "
  f"100 % {va(1.0):.2f}")
FAC_VU = (sim.I_2025 + 0.5 * 42.1) / sim.I_2025
J["deduction"] = {"definition": "50 % du prix déduits l'exercice d'acquisition, 50 % amortis selon le plan ordinaire",
                  "investissement_eligible_2027": I1, "part_imposable": PART, "departs": DEPARTS,
                  "calendrier_propose": "25 % la première année, 50 % ensuite ; départ fixé au bouclage",
                  "cout_permanent_2027": {"50": PERM50, "100": PERM100,
                                          "50_bornes_plan": [perm(0.5, "deg"), perm(0.5, "lin")]},
                  "cout_actualise_millesime": {"50_5pc": va(0.5), "50_etat": va(0.5, R_ETAT), "100_5pc": va(1.0)},
                  "facteur_vehicules_utilitaires": FAC_VU}

# =========================================================================== 3. niches (VM II PLF 2026, M€)
# coût 2024 réalisé / 2025 / 2026 prévus ; bénéficiaires ; classement [C]
NICHES = [
    # code, libellé, r2024, p2025, p2026, bénéficiaires, classe, décision
    ("200302", "Crédit d'impôt recherche (CIR)", 7800, 8068, 8041, "17 593 entreprises", "externalité", "recentrer"),
    ("200310", "Crédit d'impôt innovation (CII)", 330, 338, 230, "11 387", "externalité faible", "laisser s'éteindre fin 2027 (droit en vigueur)"),
    ("200311", "Crédit d'impôt recherche collaborative", 13, 13, 14, "308", "externalité", "garder"),
    ("210326", "Boîte à brevets (taux de 10 %)", 1199, 1258, None, "1 065", "convenance (localisation des revenus)", "supprimer"),
    ("210309", "Réduction d'impôt mécénat des entreprises (60 %)", 1635, 1730, 1730, "157 399", "convenance", "remplacer par une déduction"),
    ("320129", "Crédit d'impôt audiovisuel", 224, 223, 263, "396", "convenance sectorielle", "supprimer"),
    ("320121", "Crédit d'impôt cinéma", 152, 164, 156, "169", "convenance sectorielle", "supprimer"),
    ("320140", "Crédit d'impôt international (tournages étrangers)", 212, 117, 125, "81", "convenance sectorielle", "supprimer"),
    ("320135", "Crédit d'impôt jeux vidéo", 66, 75, 78, "108", "convenance sectorielle", "supprimer"),
    ("320142", "Crédit d'impôt spectacle vivant", 41, 47, 47, "612", "convenance sectorielle", "supprimer"),
    ("320128", "Crédit d'impôt production phonographique", 30, 31, 31, "620", "convenance sectorielle", "supprimer"),
    ("320145", "Crédit d'impôt théâtre et cirque", 4, 4, 4, "77", "convenance sectorielle", "supprimer"),
    ("320148", "Crédit d'impôt édition musicale", 1, 2, 2, "53", "convenance sectorielle", "supprimer"),
    ("220104", "Exonération ZRR / France Ruralités Revitalisation", 411, 430, 376, "50 400", "zonage", "fermer aux entrants"),
    ("220109", "Exonération ZFRR (entreprises créées)", 0, 5, 60, "nd", "zonage", "fermer aux entrants"),
    ("220102", "Exonération ZFU-territoires entrepreneurs", 107, 89, 89, "13 200", "zonage", "fermer aux entrants"),
    ("230602", "Entreprises nouvelles en zones (44 sexies)", 48, 42, 42, "9 333", "zonage", "fermer aux entrants"),
    ("230606", "Bassins d'emploi à redynamiser", 5, 4, 4, "564", "zonage", "fermer aux entrants"),
    ("230608", "Bassins urbains à dynamiser", 3, 2, 2, "365", "zonage", "fermer aux entrants"),
    ("230605", "Zones de restructuration de la défense", 2, 1, 1, "190", "zonage", "fermer aux entrants"),
    ("210305", "Crédit d'impôt investissement en Corse", 100, 83, 83, "4 560", "zonage", "fermer aux entrants"),
    ("210308", "Crédit d'impôt famille (crèches d'entreprise)", 209, 223, 223, "19 540", "convenance (utilité sociale)", "supprimer"),
    ("200401", "Suramortissement de 40 % (2015-2017)", 289, 240, 200, "81 900", "investissement", "s'éteint en 2027 (droit en vigueur)"),
    ("320119", "Taxe au tonnage (transport maritime)", 625, 1435, 620, "78", "régime européen, base mobile", "hors paquet"),
    ("210313", "Crédit d'impôt PTZ (banques)", 652, 697, 838, "44 466", "aide au logement", "hors paquet (logement)"),
    ("300206", "SIIC (exonération sous obligation de distribution)", 648, 492, None, "234", "transparence", "hors paquet"),
    ("300210", "SPPICAV", 600, 556, 556, "280", "transparence", "hors paquet"),
    ("300102", "Organismes HLM", 400, 340, 340, "659", "logement social", "hors paquet"),
    ("210325", "Crédit d'impôt investissement outre-mer", 295, 295, None, "3 510", "outre-mer", "hors paquet (politique ultramarine)"),
    ("320136", "Crédit d'impôt logement social outre-mer", 258, 258, 258, "44", "outre-mer", "hors paquet (politique ultramarine)"),
    ("210322", "Abattement bénéfices DOM", 124, 115, 130, "9 200", "outre-mer", "hors paquet (politique ultramarine)"),
    ("210333", "Crédit d'impôt industrie verte (C3IV)", 0, 140, 140, "0", "externalité (mauvais instrument)", "ne pas proroger"),
    ("230604", "JEI, exonération d'IS", 11, 9, 9, "420", "jeunes entreprises", "fermée depuis 2024, s'éteint"),
]
J["niches_liste"] = [dict(zip(("code", "libelle", "r2024", "p2025", "p2026", "beneficiaires", "classe", "decision"), n))
                     for n in NICHES]
cout26 = {n[0]: (n[4] if n[4] is not None else n[3]) / 1000 for n in NICHES}   # Md€ 2026 (2025 si 2026 nc)

CULTURE = ["320129", "320121", "320140", "320135", "320142", "320128", "320145", "320148"]
ZONES = ["220104", "220109", "220102", "230602", "230606", "230608", "230605", "210305"]
CIR_GROUPE, CIR_5PC = 0.569, 0.40                  # CPO (sept. 2025, recomm. 3) ; CAE Focus 90 (2022, données 2019)
MECENAT = cout26["210309"] * (1 - TAU / 0.60)       # réduction de 60 % remplacée par la déduction du don (25 %)
PAQ = {   # mesure: (montant 2026 Md€, profil de montée en charge par exercice à partir de 2028, statut)
    "cir_plafond_groupe_et_fin_tranche_5pc": (CIR_GROUPE + CIR_5PC, {}, "S (chiffres publiés, sans terme croisé)"),
    "mecenat_reduction_vers_deduction": (MECENAT, {}, "S (statique, dons inchangés)"),
    "credits_culture": (sum(cout26[c] for c in CULTURE), {2028: 0.5}, "S (statique)"),
    "zonages_fermes_aux_entrants": (sum(cout26[c] for c in ZONES),
                                    {2028: 1 / 8, 2029: 2 / 8, 2030: 3 / 8, 2031: 4 / 8, 2032: 5 / 8, 2033: 6 / 8, 2034: 7 / 8},
                                    "S/H (extinction linéaire sur 8 ans)"),
    "credit_famille": (cout26["210308"], {}, "S (statique)"),
    "boite_a_brevets": (cout26["210326"], {}, "S statique, borne haute : base mobile, non comptée au bouclage prudent"),
}
p("")
p("3. NICHES : paquet (Md€ 2026, statique) — exercices 2028+ (crédits culture : moitié en 2028 ; zonages : extinction sur 8 ans)")
paq_series = {}
for k, (m, prof, st) in PAQ.items():
    serie = np.array([0.0 if a < 2028 else prof.get(a, 1.0) * m * (1 + G) ** (a - 2026) for a in ANS])
    paq_series[k] = serie
    p(f"[PAQ] {k:40s} {m:.2f} Md€ (2026) [{st}] : 2028 {serie[1]:.2f} ; 2030 {serie[3]:.2f} ; 2035 {serie[8]:.2f}")
noyau = sum(v for k, v in paq_series.items() if k != "boite_a_brevets")
p("[PAQ] noyau (hors brevets) : " + " ; ".join(f"{a} {v:.2f}" for a, v in zip(ANS, noyau) if a in (2028, 2029, 2030, 2032, 2035, 2040)))
p(f"[PAQ] culture : {PAQ['credits_culture'][0]:.2f} ; zonages : {PAQ['zonages_fermes_aux_entrants'][0]:.2f} ; mécénat {MECENAT:.2f} "
  f"(sur {cout26['210309']:.2f})")
J["niches_paquet"] = {k: {"montant_2026": v[0], "statut": v[2], "serie": dict(zip(ANS, paq_series[k].tolist()))}
                      for k, v in PAQ.items()}
J["niches_paquet"]["noyau_hors_brevets"] = dict(zip(ANS, noyau.tolist()))
J["niches_totaux_vm"] = {"is_seul_2024": 3.913, "communes_ir_is_2024": 14.111,
                         "source": "Voies et moyens, tome II, PLF 2026, tableau « Dépenses fiscales par impôt »"}

# =========================================================================== 4. taux effectifs
PI, RR = 0.02, 0.05
RHO = (1 + RR) * (1 + PI) - 1
ZB = np.array([0.5 / 25] + [1 / 25] * 24 + [0.5 / 25])          # bâtiment, linéaire 25 ans
ZLOG = np.array([0.5 / 3, 1 / 3, 1 / 3, 0.5 / 3])               # logiciel acquis, linéaire 3 ans


def cout_capital(tau, b, rho, delta=0.14, plan=None):
    zz = b + (1 - b) * (z(plan, rho) if plan is not None else zmix(rho))
    return (1 - tau * zz) * (rho - PI + delta * (1 + PI)) / ((1 - tau) * (1 + PI)) - delta


def tmei(tau, b, fin="fp", delta=0.14, plan=None):
    pf = cout_capital(tau, b, RHO, delta, plan)
    pd = cout_capital(tau, b, RHO * (1 - tau), delta, plan)
    pc = {"fp": pf, "dette": pd, "mixte": 2 / 3 * pf + 1 / 3 * pd}[fin]
    return (pc - RR) / pc


CONF = {"actuel": ("Aujourd'hui (25 %)", .25, 0.), "taux225": ("Taux normal à 22,5 % (comparaison)", .225, 0.),
        "ded50": ("Déduction de 50 % (25 %)", .25, .5), "ded100": ("Déduction intégrale (long terme)", .25, 1.),
        "pme15": ("Petite société sous 42 500 €, aujourd'hui (15 %)", .15, 0.)}
TEF = {}
p("")
p("4. TMEI (convention Devereux-Griffith : r 5 %, π 2 %, δ 14 % équipements, 33 % logiciels, 3,1 % bâtiments)")
for k, (nom, tau, b) in CONF.items():
    TEF[k] = {"nom": nom, "tau": tau, "b": b, "fp": tmei(tau, b), "dette": tmei(tau, b, "dette"), "mixte": tmei(tau, b, "mixte"),
              "logiciel_fp": tmei(tau, b, delta=0.33, plan=ZLOG), "batiment_fp": tmei(tau, 0., delta=0.031, plan=ZB),
              "batiment_dette": tmei(tau, 0., "dette", delta=0.031, plan=ZB)}
    t = TEF[k]
    p(f"[TEF] {nom:48s} équip. fp {100*t['fp']:5.1f} ; dette {100*t['dette']:6.1f} ; 1/3 dette {100*t['mixte']:5.1f} ; "
      f"logiciel {100*t['logiciel_fp']:5.1f} ; bâtiment {100*t['batiment_fp']:5.1f} (dette {100*t['batiment_dette']:6.1f})")
# dépense de R&D (salaires) : déductible immédiatement → TMEI nul hors CIR ; avec CIR au taux c, subvention
for c in (0.30, 0.05):
    TEF[f"rd_cir_{int(c*100)}"] = {"nom": f"Dépense de R&D, CIR à {int(c*100)} %", "fp": -c / (1 - TAU - c)}
p(f"[TEF] R&D passée en charges : TMEI 0 ; avec CIR à 30 % : TMEI {-100*0.30/0.45:.0f} % ; à 5 % : {-100*0.05/0.70:.0f} % (−c/(1−τ−c), crédit non imposable)")
J["taux_effectifs"] = TEF
J["taux_effectifs_convention"] = {"r_reel": RR, "inflation": PI, "delta": {"equipement": .14, "logiciel": .33, "batiment": .031},
                                  "dette": "intérêt nominal 7,1 % déductible ; mixte : 1/3 d'emprunt"}

# =========================================================================== 5. effets réels
K_EQ, DEP_EQ, K_BAT, DEP_BAT = 541.0, 0.14, 399.9, 0.031
S_EQ = (R_ENT + DEP_EQ) * K_EQ / PIB25
S_BAT = (R_ENT + DEP_BAT) * K_BAT / PIB25
EPS = {"bas": 0.5, "central": 1.0, "haut": 1.6}       # équipements (Maffini-Xing-Devereux 1,6 ; littérature 0,5-1)
EPS_B = {"bas": 0.25, "central": 0.5, "haut": 1.0}


def usage(tau, b, zf=None):
    zz = b + (1 - b) * (zmix(R_ENT) if zf is None else zf)
    return (1 - tau * zz) / (1 - tau)


zb5 = z(ZB, R_ENT)
REEL = {}
p("")
p("5. EFFETS RÉELS DE LONG TERME (stock de capital, PIB potentiel Cobb-Douglas, niveau)")
for k in ("ded50", "taux225", "ded100"):
    _, tau, b = CONF[k]
    dl_eq = np.log(usage(tau, b) / usage(.25, 0.))
    dl_b = np.log(usage(tau, 0., zb5) / usage(.25, 0., zb5))
    res = {"dln_usage_eq": dl_eq, "dln_usage_bat": dl_b}
    for n in EPS:
        dk_eq = -EPS[n] * dl_eq * PART * K_EQ
        dk_b = -EPS_B[n] * dl_b * PART * K_BAT
        dy = S_EQ * dk_eq / K_EQ + S_BAT * dk_b / K_BAT
        res[n] = {"dK": dk_eq + dk_b, "dK_eq": dk_eq, "dK_bat": dk_b, "dI_regime": (DEP_EQ + G) * dk_eq + (DEP_BAT + G) * dk_b,
                  "dY_pct": 100 * dy, "dY_Md": dy * PIB25}
    REEL[k] = res
    c = res["central"]
    p(f"[REEL {k}] coût d'usage équip. {100*dl_eq:+.2f} %, bât. {100*dl_b:+.2f} % ; ΔK {c['dK']:.1f} ({res['bas']['dK']:.1f}–"
      f"{res['haut']['dK']:.1f}) Md€ ; investissement en régime établi +{c['dI_regime']:.1f} Md€/an ; PIB {c['dY_pct']:.3f} % "
      f"({res['bas']['dY_pct']:.3f}–{res['haut']['dY_pct']:.3f}), {c['dY_Md']:.1f} Md€")
# petites sociétés qui perdent le taux réduit : variation du coût d'usage à la marge (pas de part du capital connue)
dl_p_eq = np.log(usage(.25, .5) / usage(.15, 0.))
dl_p_b = np.log(usage(.25, 0., zb5) / usage(.15, 0., zb5))
p(f"[PME sous 42 500 €] coût d'usage : équipements {100*dl_p_eq:+.1f} % (taux réduit perdu, déduction gagnée), bâtiments "
  f"{100*dl_p_b:+.1f} % ; non agrégé (part du capital de ces sociétés inconnue) ; effet de trésorerie non chiffré")
REEL["pme_sous_plafond"] = {"dln_usage_eq": dl_p_eq, "dln_usage_bat": dl_p_b}
# coût et rendement
COUT_225 = 2.5 * POINT
REEL["ded50"]["cout_permanent"] = PERM50
REEL["ded100"]["cout_permanent"] = PERM100
REEL["taux225"]["cout_permanent"] = COUT_225
REEL["ded50"]["cout_economique"] = va(0.5)            # coût actualisé d'une année d'achats (avance comprise)
REEL["ded100"]["cout_economique"] = va(1.0)
REEL["taux225"]["cout_economique"] = COUT_225
for k in ("ded50", "taux225", "ded100"):
    REEL[k]["dK_par_Md_cout_economique"] = REEL[k]["central"]["dK"] / REEL[k]["cout_economique"]
    p(f"[RENDEMENT {k}] coût économique annuel {REEL[k]['cout_economique']:.2f} Md€ (actualisé, avance de trésorerie "
      f"comprise) ; {REEL[k]['dK_par_Md_cout_economique']:.1f} Md€ de capital par Md€")
J["effets_reels"] = REEL
J["effets_reels_hyp"] = {"K_eq": K_EQ, "K_bat": K_BAT, "s_eq": S_EQ, "s_bat": S_BAT, "eps_eq": EPS, "eps_bat": EPS_B}

# =========================================================================== 6. long terme : déduction intégrale
f_50_puis_100 = lambda t: 0.5 if t < 8 else 1.0      # 50 % dès 2027, 100 % dès 2035
f_50 = lambda t: 0.5
sup = chemin_mix(f_50_puis_100)[:NA + 5] - chemin_mix(f_50)[:NA + 5]
p("")
p(f"6. LONG TERME : passer de 50 à 100 % en 2035 coûte en plus {sup[8]:.2f} Md€ la 1re année (2035), {sup[9]:.2f} en 2036, "
  f"puis {PERM100 - PERM50:.2f} Md€ de 2027 par an ; d'un coup en 2027 : {chemin_mix(lambda t: 1.0)[0]:.1f} Md€")
J["long_terme"] = {"surcout_passage_100_en_2035": dict(zip(range(2027, 2027 + NA + 5), sup.tolist())),
                   "surcout_permanent_2027": PERM100 - PERM50, "deduction_integrale_1re_annee_2027": float(chemin_mix(lambda t: 1.0)[0]),
                   "ace": "non chiffrée : fonds propres fiscaux des sociétés imposables non disponibles dans une source vérifiée"}

# =========================================================================== 7. cas types
M = 500_000.0
cas = {}
for reg in ("lin", "deg"):
    anc, nouv = M * PLANS[reg], M * (0.5 * E0 + 0.5 * PLANS[reg])
    cas[reg] = {"ded_an1_actuel": anc[0], "ded_an1_reforme": nouv[0], "tresorerie_an1": TAU * (nouv[0] - anc[0]),
                "va_5": TAU * (z(nouv / M) - z(anc / M)) * M, "va_8": TAU * (z(nouv / M, .08) - z(anc / M, .08)) * M}
# niche : suramortissement « industrie 4.0 » (PLF 2027, art. 9, proposé) : 80 % (petites entreprises), 120 % en zone AFR
zm = zmix(R_ENT)
for s_ in (0.40, 0.80, 1.20):
    cas[f"suramort_{int(s_*100)}"] = TAU * s_ * zm * M
cas["ded50_va"] = TAU * (zmix(R_ENT, .5) - zm) * M
p("")
p("7. CAS TYPES")
for reg in ("lin", "deg"):
    c = cas[reg]
    p(f"[MACHINE {reg}] déduction an 1 {fr(c['ded_an1_actuel'],0)} → {fr(c['ded_an1_reforme'],0)} € ; trésorerie +{fr(c['tresorerie_an1'],0)} ; "
      f"avantage actualisé {fr(c['va_5'],0)} € (5 %), {fr(c['va_8'],0)} € (8 %)")
p(f"[NICHE] machine de 500 000 € : déduction de 50 % = {fr(cas['ded50_va'],0)} € actualisés ; suramortissement 40 % = "
  f"{fr(cas['suramort_40'],0)} ; 80 % = {fr(cas['suramort_80'],0)} ; 120 % = {fr(cas['suramort_120'],0)} €")
# projet non rentable rendu rentable : VAN avant niche = −40 000 € après impôt (droit actuel)
J["cas"] = {"machine_500k": cas, "taux_reduit": cas_tr}

# =========================================================================== 8. table annuelle
p("")
p("8. TABLE ANNUELLE (exercices, Md€ courants, + = recette)")
annuel = {}
for t, a in enumerate(ANS):
    d = {"is_fin_taux_reduit_prudent": float(tr_prud[t]), "is_fin_taux_reduit_statique": float(tr_stat[t])}
    for s in (2027, 2028, 2029):
        d[f"is_deduction_50_depart_{s}"] = -DEPARTS[s]["brut"][a]
        d[f"is_deduction_50_depart_{s}_permanent"] = -DEPARTS[s]["permanent"][a]
    d["is_niches_noyau"] = float(noyau[t])
    for k in PAQ:
        d[f"is_niches_{k}"] = float(paq_series[k][t])
    d["memo_fin_contribution_exceptionnelle_droit_en_vigueur_non_comptee"] = -7.0
    d["memo_extinction_cii_suramortissement_droit_en_vigueur_non_comptee"] = round(
        (0.23 if a >= 2028 else 0.0) + 0.2 * (1 if a >= 2028 else 0), 3)
    annuel[str(a)] = {k: round(v, 3) for k, v in d.items()}
    p(f"{a} : taux réduit {tr_prud[t]:+.2f} (stat. {tr_stat[t]:+.2f}) ; déduction départ 27/28/29 "
      f"{d['is_deduction_50_depart_2027']:+.2f}/{d['is_deduction_50_depart_2028']:+.2f}/{d['is_deduction_50_depart_2029']:+.2f} ; "
      f"niches noyau {noyau[t]:+.2f} (+ brevets {paq_series['boite_a_brevets'][t]:.2f})")
J["annuel"] = annuel
J["annuel_caisse"] = {str(a): {k: (annuel[str(a - 1)][k] if str(a - 1) in annuel else 0.0) for k in annuel[str(a)]
                               if k.startswith("is_")} for a in ANS}
J["annuel_notes"] = {
    "convention": "exercices ; en caisse, solde et acomptes : environ un an plus tard (annuel_caisse = décalage d'un an)",
    "is_fin_taux_reduit_prudent": "20 % pour l'exercice 2027, 25 % ensuite ; coût officiel 2019 actualisé (retenu au bouclage)",
    "is_fin_taux_reduit_statique": "10 points sur la base imposée à 15 % (borne haute mécanique)",
    "is_deduction_50_depart_XXXX": "coût brut, 25 % l'année de départ puis 50 % ; _permanent : coût de régime établi (repère)",
    "is_niches_noyau": "CIR recentré + mécénat + crédits culture + zonages + crédit famille, dès les exercices 2028, statique",
    "is_niches_boite_a_brevets": "suppression du taux de 10 %, statique : base mobile, borne haute, hors bouclage prudent",
    "memo_fin_contribution_exceptionnelle": "droit en vigueur (fin après l'exercice 2026), écart au niveau 2026, non compté",
    "memo_extinction_cii_suramortissement": "CII (fin 2027) et suramortissement 2015-2017 (fin d'incidence 2027) : droit en vigueur, non comptés",
}
# solde du bloc (prudent, noyau) pour chaque départ
SOLDE = {}
for s in (2027, 2028, 2029):
    sol = [annuel[str(a)]["is_fin_taux_reduit_prudent"] + annuel[str(a)][f"is_deduction_50_depart_{s}"] + annuel[str(a)]["is_niches_noyau"]
           for a in ANS]
    SOLDE[s] = dict(zip(ANS, [round(v, 3) for v in sol]))
    p(f"[SOLDE IS, départ {s}] " + " ; ".join(f"{a} {v:+.2f}" for a, v in zip(ANS, sol) if a in (2027, 2028, 2029, 2030, 2031, 2033, 2035, 2040)))
REG = TR_PRUD + sum(v[0] * (1 + G) for k, v in PAQ.items() if k != "boite_a_brevets") - PERM50
p(f"[MARGE] régime permanent (euros 2027) : taux réduit {TR_PRUD:.2f} + niches noyau "
  f"{sum(v[0] for k, v in PAQ.items() if k != 'boite_a_brevets')*(1+G):.2f} − déduction {PERM50:.2f} = {REG:.2f} Md€/an "
  f"(+{PAQ['boite_a_brevets'][0]*(1+G):.2f} si brevets ; +{TR_STAT-TR_PRUD:.2f} si taux réduit statique)")
J["solde_bloc_is"] = SOLDE
J["marge_regime_permanent_2027"] = {"prudent": REG, "avec_brevets": REG + PAQ["boite_a_brevets"][0] * (1 + G),
                                   "avec_taux_reduit_statique": REG + TR_STAT - TR_PRUD,
                                   "point_de_taux_equivalent": REG / POINT}
p(f"[MARGE] soit {REG/POINT:.1f} point de taux normal ; une baisse à 22,5 % coûterait {COUT_225:.2f} Md€/an (2027)")
J["comparaison_taux_225"] = {"cout_2027": COUT_225, "point": POINT}

(OUT / "is3.json").write_text(json.dumps(J, ensure_ascii=False, indent=1,
                                         default=lambda o: o.item() if hasattr(o, "item") else list(o)), encoding="utf-8")
(OUT / "is3_calculs.txt").write_text("\n".join(L) + "\n", encoding="utf-8")
print("\n".join(L))
