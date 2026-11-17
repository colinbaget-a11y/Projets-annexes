"""Bloc IR-CSG v5 : réexamen des trois exceptions (frais réels, engagements locatifs en cours, épargne retraite).
Lancer depuis fiscalite/ :  python3 note8p/calculs/ircsg5_exceptions.py
Sorties : note8p/sorties/exceptions5.json, exceptions5.md. Ne modifie ni ircsg4_modele.py ni ses sorties : le modèle v4
est exécuté jusqu'au barème final (sections 1 à 3 bis, sans la section 8 qui écrit les sorties) dans un espace de noms.

1. Frais professionnels. Variantes appliquées au barème final v4 (7,0 Md€) : recette statique de l'impôt du barème
   (N.recette), comparée à l'option du modèle v4 (forfait supprimé, frais réels gardés). La décision de déclarer les
   frais réels dépend du taux marginal du barème final (règle de ircsg4_frais.regle, seuil de gain calé). Baisse
   uniforme des taux à recette constante : points 0 à 3,5 Smic (pondération W_UNI du modèle) et tous les points.
2. Épargne retraite : la déduction du modèle (DED_PER0, 10,58 Md€ en 2024 portés en 2025) comprend les cases 6NS-6NU,
   6RS-6RU (versements individuels déduits du revenu global, 8,09 Md€) mais aussi 6QS-6QU (régimes obligatoires
   d'entreprise, 1,55) et 6OS-6OU (cotisations déduites des revenus d'indépendants, 0,94), qui ne sont déclarées que
   pour le calcul du plafond [à vérifier sur la notice 2042]. La suppression ne porte que sur la part 6NS-6RU.
3. Locatif : hors modèle (avantages gardés « non supprimables ou stock ») ; coûts des Voies et moyens PLF 2026 ;
   calendrier d'extinction [H].
"""
import json
import os
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
SRC = (HERE / "ircsg4_modele.py").read_text(encoding="utf-8")
CUT = SRC.index("# ================================================================== 4. distribution")
ns = {"__file__": str(HERE / "ircsg4_modele.py"), "__name__": "ircsg4_partiel"}
exec(compile(SRC[:CUT], "ircsg4_modele.py[1-3bis]", "exec"), ns)

N, M, O, FR4 = ns["N"], ns["M"], ns["O"], ns["FR4"]
S, TT, P0, W_UNI = ns["S"], ns["TT"], ns["P0"], ns["W_UNI"]
ADULTES, DED_PER0, SIG, GT = ns["ADULTES"], ns["DED_PER0"], ns["SIG"], ns["GT"]
ded_par_point = ns["ded_par_point"]
OUT = HERE.parent / "sorties"
L = []


def p(s=""):
    print(s, flush=True)
    L.append(s)


TAU = lambda w: float(S[0](w))  # noqa: E731  taux marginal du barème final


def ded_option(option):
    """Déduction par adulte et part de déclarants pour une option (barème final)."""
    if option[0] == "aucune":
        return [0 * a[3] for a in ADULTES], [0 * a[3] for a in ADULTES], [0 * a[3] for a in ADULTES]
    if option[0] == "forfait_seul":            # forfait fixe pour tous, pas de frais réels
        d = [np.minimum(option[1], a[3]) * (a[3] > 500) for a in ADULTES]
        return d, [0 * a[3] for a in ADULTES], [0 * a[3] for a in ADULTES]
    if option[0] == "forfait_pct_seul":        # abattement proportionnel plafonné (type CSG : 1,75 % jusqu'à 4 PASS)
        d = [np.minimum(option[1] * a[3], option[2]) * (a[3] > 500) for a in ADULTES]
        return d, [0 * a[3] for a in ADULTES], [0 * a[3] for a in ADULTES]
    D, P, F = FR4.profils(option, SIG, GT, TAU)
    g = lambda arr: [np.interp(a[3], FR4.GRID, arr) * (a[3] > 500) for a in ADULTES]  # noqa: E731
    return g(D), g(P), g(F)


def tot(lst):
    return float(sum((a[2] * x).sum() for a, x in zip(ADULTES, lst)))


def etat(option, per_part=1.0):
    d, q, f = ded_option(option)
    M.DED_PER = per_part * DED_PER0 + ded_par_point(d)
    return dict(recette_Md=N.recette(S, O), deduction_Md=tot(d) / 1e9, declarants_M=tot(q) / 1e6,
                frais_reels_Md=tot(f) / 1e9)


def baisse_uniforme(cible, w):
    """Baisse e (points de taux) aux points pondérés w telle que la recette revienne à la cible."""
    lo, hi = 0.0, 0.05
    for _ in range(45):
        m = (lo + hi) / 2
        lo, hi = (m, hi) if N.recette(N.continu(P0, list(np.array(TT) - m * w)), O) > cible else (lo, m)
    return 100 * (lo + hi) / 2


# ================================================================== 1. frais professionnels
OPTS = {
    "v4_frais_reels_sans_forfait": ("suppression",),
    "aucune_deduction": ("aucune",),
    "forfait_seul_300": ("forfait_seul", 300.0),
    "forfait_seul_500": ("forfait_seul", 500.0),
    "forfait_seul_1000": ("forfait_seul", 1000.0),
    "abattement_1_75_pct_plaf_4pass": ("forfait_pct_seul", 0.0175, 0.0175 * 4 * 47100.0),
    "franchise_1000": ("franchise", 1000.0),
    "franchise_2000": ("franchise", 2000.0),
    "franchise_3000": ("franchise", 3000.0),
    "franchise_5000": ("franchise", 5000.0),
    "forfait_500_ou_reels": ("fixe", 500.0),
}
FR = {k: etat(o) for k, o in OPTS.items()}
BASE = FR["v4_frais_reels_sans_forfait"]["recette_Md"]
W_ALL = np.ones(len(P0))
p("[FRAIS] barème final v4 ; recette statique de l'impôt du barème ; + = recette en plus par rapport au modèle v4")
for k, a in FR.items():
    a["recette_vs_v4_Md"] = a["recette_Md"] - BASE
    a["recette_vs_aucune_Md"] = a["recette_Md"] - FR["aucune_deduction"]["recette_Md"]
    M.DED_PER = DED_PER0 + ded_par_point(ded_option(OPTS[k])[0])
    a["baisse_uniforme_pts_0_3_5_smic"] = baisse_uniforme(BASE, W_UNI) if a["recette_vs_v4_Md"] > 0.05 else None
    a["baisse_uniforme_pts_tous"] = baisse_uniforme(BASE, W_ALL) if a["recette_vs_v4_Md"] > 0.05 else None
    p(f"  {k:30s} déduction {a['deduction_Md']:5.1f} Md€ ; frais réels {a['frais_reels_Md']:5.1f} ; déclarants"
      f" {a['declarants_M']:5.1f} M ; recette vs v4 {a['recette_vs_v4_Md']:+5.2f} ; baisse uniforme"
      f" {a['baisse_uniforme_pts_0_3_5_smic'] or 0:.2f} pt (0-3,5 Smic) / {a['baisse_uniforme_pts_tous'] or 0:.2f} pt (tous)")
# sensibilité : recours moins élastique (seuil de gain doublé) pour l'option v4
_gt = SIG, GT
GT = 2 * GT
d2 = etat(("suppression",))
GT = _gt[1]
FR["sensibilite_v4_seuil_double"] = dict(d2, recette_vs_v4_Md=d2["recette_Md"] - BASE)
p(f"  sensibilité (v4, seuil de gain doublé) : déduction {d2['deduction_Md']:.1f}, déclarants {d2['declarants_M']:.1f} M ;"
  f" recette de « aucune déduction » par rapport à elle : {FR['aucune_deduction']['recette_Md'] - d2['recette_Md']:+.2f} Md€")
# taux marginal moyen apparent
FR["taux_marginal_moyen_apparent_v4"] = (FR["aucune_deduction"]["recette_Md"] - BASE) / FR["v4_frais_reels_sans_forfait"]["deduction_Md"]
# dispersion des frais simulés : part des salariés aux frais > 5 000 € (trajets longs)
grid_f = np.array([np.mean(FR4.frais(w, SIG) > x) for w in FR4.GRID for x in (5000.0,)])
part5000 = float(sum((a[2] * np.interp(a[3], FR4.GRID, grid_f) * (a[3] > 500)).sum() for a in ADULTES) /
                 sum((a[2] * (a[3] > 500)).sum() for a in ADULTES))
FR["part_salaries_frais_sup_5000"] = part5000
p(f"  taux marginal moyen apparent sur la déduction v4 : {100 * FR['taux_marginal_moyen_apparent_v4']:.1f} % ;"
  f" part des salariés aux frais simulés > 5 000 € : {100 * part5000:.1f} %")

# ================================================================== 2. épargne retraite
CASES = dict(c6N=5129128323.0 + 1953442838.0 + 15147340.0, c6R=696647571.0 + 294746473.0 + 3669466.0,
             c6Q=1208420025.0 + 335134904.0 + 3056696.0, c6O=728927959.0 + 210231153.0 + 164357.0)
TOTAL_CASES = sum(CASES.values())
PART_IND = (CASES["c6N"] + CASES["c6R"]) / TOTAL_CASES
base_frais = OPTS["v4_frais_reels_sans_forfait"]
PER = {}
for k, (opt, part) in {"v4": (base_frais, 1.0), "suppression_6NS_6RU": (base_frais, 1 - PART_IND),
                       "suppression_tout_DED_PER": (base_frais, 0.0),
                       "suppression_6NS_6RU_et_frais": (("aucune",), 1 - PART_IND)}.items():
    PER[k] = etat(opt, part)
for k in PER:
    PER[k]["recette_vs_v4_Md"] = PER[k]["recette_Md"] - PER["v4"]["recette_Md"]
DED_IND_MD = float((M.W_A * DED_PER0).sum() / 1e9) * PART_IND
PER["deduction_individuelle_2025_Md"] = DED_IND_MD
PER["taux_marginal_moyen_apparent"] = PER["suppression_6NS_6RU"]["recette_vs_v4_Md"] / DED_IND_MD
PER["part_individuelle_des_cases"] = PART_IND
PER["cases_2024_Md"] = {k: v / 1e9 for k, v in CASES.items()}
M.DED_PER = (1 - PART_IND) * DED_PER0 + ded_par_point(ded_option(base_frais)[0])
PER["baisse_uniforme_pts_0_3_5_smic"] = baisse_uniforme(PER["v4"]["recette_Md"], W_UNI)
# taux marginal du barème final pour un retraité aisé (pension annuelle par adulte)
PER["taux_marginal_bareme_final"] = {str(int(z)): float(S[0](z)) for z in (20e3, 30e3, 40e3, 60e3, 80e3, 120e3)}
tr = float(np.mean([S[0](z) for z in (30e3, 40e3, 60e3)]))
PER["tee_croisiere_Md_indicatif"] = PER["suppression_6NS_6RU"]["recette_vs_v4_Md"] * (1 - tr / PER["taux_marginal_moyen_apparent"])
p(f"\n[PER] déduction individuelle (6NS-6NU, 6RS-6RU) 2025 : {DED_IND_MD:.2f} Md€ ({100 * PART_IND:.0f} % des cases"
  f" du modèle) ; suppression : {PER['suppression_6NS_6RU']['recette_vs_v4_Md']:+.2f} Md€ (taux marginal apparent"
  f" {100 * PER['taux_marginal_moyen_apparent']:.1f} %) ; tout DED_PER : {PER['suppression_tout_DED_PER']['recette_vs_v4_Md']:+.2f} ;"
  f" avec suppression des frais : {PER['suppression_6NS_6RU_et_frais']['recette_vs_v4_Md']:+.2f} ; baisse uniforme"
  f" {PER['baisse_uniforme_pts_0_3_5_smic']:.2f} pt")
p(f"  taux marginal du barème final à 30/40/60 k€ : {[round(100 * S[0](z), 1) for z in (30e3, 40e3, 60e3)]} ;"
  f" TEE en croisière (indicatif : recette × (1 − τ retraite / τ actif)) : {PER['tee_croisiere_Md_indicatif']:+.2f} Md€")

# ================================================================== 3. locatif : engagements en cours (Voies et moyens PLF 2026)
VM = {  # code : (libellé, 2024, 2025, 2026 en M€, fin du fait générateur, fin d'incidence)
    "110261": ("Pinel, Duflot", 1469, 1459, 1349, 2024, 2038),
    "110265": ("Denormandie", 5, 5, 7, 2027, 2039),
    "110251": ("Scellier", 34, 30, 38, 2025, 2051),
    "110252": ("Scellier intermédiaire", 189, 169, 176, 2025, 2051),
    "110259": ("Scellier intermédiaire outre-mer", 41, 37, 37, 2025, 2051),
    "110250": ("Censi-Bouvard (LMNP)", 39, 35, 37, 2025, 2035),
    "110210": ("Girardin logement (199 undecies A)", 22, 20, 21, 2029, 2036),
    "110256": ("Girardin logement social (199 undecies C)", 15, 12, 12, 2029, 2030),
    "110224": ("Girardin industriel (199 undecies B)", 775, 825, 831, 2029, 2030),
}
METRO = ["110261", "110265", "110251", "110252", "110259", "110250"]
c26 = sum(VM[c][3] for c in METRO) / 1e3
# calendrier [H] : Pinel linéaire de 2026 à zéro en 2038 (fin d'incidence) ; Scellier et Censi-Bouvard : extinction
# linéaire en 2031 (fin des prorogations ; la fin d'incidence 2051 tient à des reports résiduels) ; Denormandie : 7 M€
CAL = {}
for an in range(2027, 2040):
    pin = 1.349 * max(0.0, (2038 - an) / (2038 - 2026))
    sce = (0.038 + 0.176 + 0.037 + 0.037) * max(0.0, (2031 - an) / (2031 - 2026))
    den = 0.007 if an <= 2039 else 0.0
    CAL[str(an)] = round(pin + sce + den, 3)
LOC = dict(voies_et_moyens_M=VM, stock_metropole_2026_Md=c26, calendrier_suppression_Md=CAL,
           cumul_2027_2038_Md=sum(CAL.values()),
           girardin_industriel_note="réduction imputée l'année de l'investissement, reports sur 5 ans : déjà supprimé dans"
                                    " le modèle v4 (profil « reports » 60/80/90/100 %)")
p(f"\n[LOCATIF] stock métropole (Pinel, Scellier, Censi-Bouvard, Denormandie) 2026 : {c26:.2f} Md€ ; calendrier [H] :"
  + " ".join(f"{a}:{v:.2f}" for a, v in CAL.items()) + f" ; cumul {LOC['cumul_2027_2038_Md']:.1f} Md€")

J = dict(version="v5 exceptions (17/11/2026)", frais=FR, per=PER, locatif=LOC,
         unites="Md€ 2025, recette statique de l'impôt du barème final v4 (7,0 Md€), régime de croisière (λ = 1) ;"
                " + = recette en plus par rapport au modèle v4 ; baisse uniforme en points de taux marginal",
         statuts={"frais": "[H] modèle de frais calé sur 1AK-1DK [E]", "per": "[E] cases 2042 revenus 2024 ; répartition [H]",
                  "locatif": "[E] Voies et moyens PLF 2026 ; calendrier [H]"})
json.dump(J, open(OUT / "exceptions5.json", "w"), ensure_ascii=False, indent=1, default=float)
