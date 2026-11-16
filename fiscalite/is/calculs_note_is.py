"""Calculs de la partie IS de la note de synthèse « Taxer mieux plutôt que davantage » (refonte du 16/11/2026).

Lancer depuis fiscalite/ : python3 is/calculs_note_is.py
  -> is/sorties/calculs_note_is.txt   (tous les chiffres cités dans synthese/parties/is.tex et annexe_is.tex)
  -> is/sorties/calculs_note_is.json  (séries pour is/figures_note_is.py)
  -> synthese/parties/tab_is_transition.tex, tab_is_transition_complet.tex, tab_is_options.tex, tab_is_cas.tex

La mécanique (plans d'amortissement, coût annuel d'une déduction immédiate, bénéfices de 2022 portés en 2027)
est celle de is/simulation_is.py, corrigée le 16/11/2026 (revue/hypotheses_is.md), importée telle quelle. Ce
script y ajoute ce que demande la nouvelle architecture de la note :
  1. situation actuelle : recette, qui paie, taux affichés et effectifs, comparaison OCDE ;
  2. réforme naïve : baisse générale du taux, à qui elle profite, effet à coût égal sur la machine marginale ;
  3. proposition sans falaise : calendriers comparés (falaise de 2033, paliers annuels, 100 % sous plafond dès
     2027 sur le modèle britannique, combinaisons, amortissement neutre), dette de transition, baisse finale du taux ;
  4. arbitrages et cas types de sociétés ;
  5. tableau de transition année par année, contribution exceptionnelle comprise.
Conventions : année 1 = 2027 ; Md€ courants (croissance nominale de 3 % par an) sauf mention ; part de
l'investissement éligible faite par des sociétés imposables : 75 % (hypothèse H1, 60 à 90 %).
"""
import json
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import simulation_is as sim  # noqa: E402

OUT = HERE / "sorties"
TAB = HERE.parent / "synthese" / "parties"
L = []
p = L.append
J = {}

TAU, G, R_ENT, R_ETAT = sim.TAU, sim.G, sim.R, sim.R_ETAT
AN1, I1, H = sim.AN1, sim.I1, 70
PART = 0.75
PLANS = {"lin": sim.plan("lineaire"), "deg": sim.plan("degressif")}
E0 = np.eye(1, len(PLANS["lin"]), 0).ravel()
POINT = sim.POINT                                   # un point de taux normal en 2027, taux réduit supprimé (2,99)
POINT_TR = sim.BASE_NORMALE * sim.AB / 100          # un point sur la seule base au taux normal (2,67)
PIB27 = sim.PIB_2027


def fr(x, d=1):
    """Nombre au format français."""
    s = f"{x:,.{d}f}".replace(",", " ").replace(".", ",")
    return s.replace("-", "−")


def z(d, r=R_ENT):
    return float(sum(dk / (1 + r) ** k for k, dk in enumerate(d)))


# ================================================================ 1. situation actuelle (sources : is/donnees)
p("=" * 100)
p("1. SITUATION ACTUELLE")
PIB25 = 2991.056
# Base 2025 (décision 5 du 17/11/2026). Exécution budgétaire : PLF 2027 (tableau des recettes fiscales nettes, colonne
# « Exécution 2025 ») et rapport AN n° 2847 sur le projet de loi relatif aux résultats de la gestion 2025 ; prélèvements
# obligatoires : Insee, comptes de la Nation 2025, tableau 3.217 ; recouvrement : DGFiP Statistiques n° 43 (mars 2026).
REC = {"IS net (budget de l'État)": {2023: 56.8, 2024: 57.4, 2025: 59.9, 2026: 60.3, 2027: 58.5},
       "Contribution exceptionnelle": {2025: 7.52, 2026: 7.0, 2027: 5.0},
       "Contribution sociale (3,3 %), comptabilité nationale": {2024: 1.166, 2025: 1.151},
       "Minimum mondial (pilier 2)": {2026: 0.5}}
PO25 = {"is_avant_credits": 69.473, "credits_deduits": 3.930, "credits_restitues": 6.199, "ce": 7.520, "csb": 1.151}
PO25["is_net"] = PO25["is_avant_credits"] - PO25["credits_deduits"] - PO25["credits_restitues"]
PO25["total"] = PO25["is_net"] + PO25["ce"] + PO25["csb"]
J["po2025"] = PO25
p(f"[RECETTE] IS net 2025 au budget de l'État 59,9 Md€ = {100*59.9/PIB25:.2f} % du PIB (exécution, PLF 2027 et rapport AN "
  f"n° 2847) ; recouvrement DGFiP (IS et contribution sociale) 61,8 Md€ (DGFiP n° 43)")
p(f"[RECETTE PO 2025] Insee 3.217 : IS avant crédits d'impôt {fr(PO25['is_avant_credits'], 1)} Md€, crédits "
  f"{fr(PO25['credits_deduits'] + PO25['credits_restitues'], 1)} (dont restitués {fr(PO25['credits_restitues'], 1)}), IS net "
  f"{fr(PO25['is_net'], 1)} ; contribution exceptionnelle {fr(PO25['ce'], 2)} ; contribution sociale {fr(PO25['csb'], 2)} ; "
  f"total {fr(PO25['total'], 1)} Md€ = {fr(100*PO25['total']/PIB25, 2)} % du PIB ; IS net seul {fr(100*PO25['is_net']/PIB25, 2)} %")
p("[RECETTE] CIR et crédits voisins utilisés en 2025 : 7,69 Md€ (DGFiP n° 51, tableau 3, montants arrêtés au 30 juin) ; "
  "IS brut budgétaire 2026 (avant remboursements et dégrèvements) : 85,0 Md€ ; IS net 2027 (PLF) 58,5 hors contribution "
  "exceptionnelle (5,0 proposés pour 2027 par l'art. 15 du PLF, article supprimé en 1re lecture selon Légifiscal)")
# Qui paie : exercice 2025 (DGFiP Statistiques n° 51, tableau 2 ; données provisoires) : milliers d'entreprises, résultat
# fiscal (bénéfices moins déficits) et IS brut, Md€. Les bénéfices par taille ne sont publiés que jusqu'en 2024.
TAILLE = {"Très petites": (2604.8, 29.40, 14.540), "PME": (220.2, 45.81, 18.940), "ETI": (8.7, 41.41, 16.781),
          "Grandes": (0.371, 59.44, 20.214)}
ISB = sum(v[2] for v in TAILLE.values())
RFT = sum(v[1] for v in TAILLE.values())
for k, (n, b, i) in TAILLE.items():
    p(f"[QUI PAIE 2025] {k:13s} {fr(n*1000,0):>10s} entreprises ; résultat fiscal {b:5.1f} Md€ ({100*b/RFT:.0f} %) ; IS brut "
      f"{i:5.1f} Md€ ({100*i/ISB:.1f} % de l'IS brut)")
p(f"[QUI PAIE 2025] total : {fr(sum(v[0] for v in TAILLE.values())*1000, 0)} entreprises ; IS brut {fr(ISB, 1)} Md€ ; "
  f"résultat fiscal {fr(RFT, 1)} Md€ ; bénéfices à 15 % {fr(sim.BASE_REDUITE, 1)}, à 25 % {fr(sim.BASE_NORMALE, 1)}, déficits "
  "111,3 Md€ (graphique 2)")
J["qui_paie"] = {k: {"nombre_milliers": v[0], "resultat_fiscal": v[1], "is_brut": v[2], "part": v[2] / ISB,
                     "part_resultat": v[1] / RFT} for k, v in TAILLE.items()}
# Taux apparent IS brut / bénéfices : 2022 (DGFiP n° 21), année des taux implicites de l'Insee (figure is_n03) ; et 2024
# (DGFiP n° 39), dernière année où les bénéfices par taille sont publiés.
TAILLE22 = {"Très petites": (60.3, 13.1), "PME": (75.9, 18.9), "ETI": (62.2, 15.8), "Grandes": (79.5, 20.6)}
TAILLE24 = {"Très petites": (65.9, 14.0), "PME": (78.5, 19.2), "ETI": (64.5, 16.2), "Grandes": (75.0, 19.6)}
for an_, T_ in ((2022, TAILLE22), (2024, TAILLE24)):
    p(f"[TAUX APPARENT {an_}] IS brut / bénéfices : " + " ; ".join(f"{k} {100*i/b:.1f} %" for k, (b, i) in T_.items()))
J["taux_apparent"] = {"2022": {k: i / b for k, (b, i) in TAILLE22.items()},
                      "2024": {k: i / b for k, (b, i) in TAILLE24.items()}}
IMPLICITE = {"Microentreprises": 19.0, "PME": 21.4, "Grandes": 14.3, "Ensemble": 17.5}   # Insee Analyses n° 112, 2022
J["implicite"] = IMPLICITE
J["taux_legaux"] = {"Taux réduit (jusqu'à 42 500 €)": 15.0, "Taux normal": 25.0,
                    "Avec la contribution sociale": 25.825, "Contribution exceptionnelle, CA ≥ 1 Md€": 30.98,
                    "Contribution exceptionnelle, CA ≥ 3 Md€": 36.13}
p(f"[TAUX] taux affichés : 15 % (≤ 42 500 €), 25 %, 25,825 % (contribution sociale), 30,98 % et 36,13 % (contribution "
  f"exceptionnelle 2025-2026 : 25 × (1 + 3,3 % + 20,6 %) = {25*(1+0.033+0.206):.2f} ; 25 × (1 + 3,3 % + 41,2 %) = {25*(1+0.033+0.412):.3f})")
p("[TAUX] taux implicites 2022 (IS avant crédits / excédent net d'exploitation, Insee) : micro 19,0 ; PME 21,4 ; GE 14,3 ; "
  "ensemble 17,5 % ; OCDE 2025 : taux moyen effectif 23,6 % (moyenne 22,2) ; marginal 15,0 % (16,5) ; équipements 9,8 % (10,4)")
# Comparaison OCDE de la recette (fichier extrait par is/donnees/extraire_ocde_is_pib.py)
oc = {}
for ligne in (HERE / "donnees" / "ocde_is_pib.csv").read_text(encoding="utf-8").splitlines()[1:]:
    c, a, v = ligne.split(",")
    oc.setdefault(int(a), {})[c] = float(v)
for a in (2019, 2022, 2023, 2024):
    d = oc[a]
    rang = sorted(d.values(), reverse=True).index(d["FRA"]) + 1
    p(f"[OCDE] {a} : France {d['FRA']:.2f} % du PIB ; moyenne {np.mean(list(d.values())):.2f} ; médiane "
      f"{np.median(list(d.values())):.2f} ; rang {rang} sur {len(d)} ; Allemagne {d.get('DEU', float('nan')):.1f}, "
      f"Italie {d.get('ITA', float('nan')):.1f}, Espagne {d.get('ESP', float('nan')):.1f}, Royaume-Uni "
      f"{d.get('GBR', float('nan')):.1f}, États-Unis {d.get('USA', float('nan')):.1f}")
J["ocde_2023"] = oc[2023]

# ================================================================ mécanique commune
def chemin(reg, bonus, part=PART, i1=I1, g=G, h=H, tau=TAU, neutre=None):
    """Coût annuel pour l'État (Md€), années 0..h-1 (0 = 2027). bonus(t) : fraction déduite tout de suite des achats
    de l'année t ; neutre : taux de revalorisation des annuités restantes (amortissement neutre) au lieu d'un bonus."""
    anc = PLANS[reg]
    n = len(anc)
    c = np.zeros(h + n)
    for t in range(h):
        I = i1 * (1 + g) ** t
        if neutre is not None:
            nouv = anc * (1 + neutre) ** np.arange(n)
        else:
            b = bonus(t)
            nouv = b * E0 + (1 - b) * anc
        c[t:t + n] += tau * part * I * (nouv - anc)
    return c[:h]


def va_millesime(reg, b=1.0, r=R_ENT, part=PART, neutre=None):
    """Coût actualisé d'une année d'investissement (Md€ de 2027) : tau s I (z nouveau - z ancien)."""
    anc = PLANS[reg]
    nouv = anc * (1 + neutre) ** np.arange(len(anc)) if neutre is not None else b * E0 + (1 - b) * anc
    return TAU * part * I1 * (z(nouv, r) - z(anc, r))


def dette(cout, fin0, r=R_ETAT, g=G, extra=None):
    """Dette cumulée (Md€ courants) : d_t = d_{t-1}(1+r) - (ressources_t - coût_t) ; ressources croissant avec g."""
    h = len(cout)
    res = fin0 * (1 + g) ** np.arange(h)
    if extra is not None:
        res = res + extra[:h]
    solde = res - cout
    D = np.zeros(h)
    d = 0.0
    for t in range(h):
        d = d * (1 + r) - solde[t]
        D[t] = d
    pk = int(np.argmax(D))
    ext = next((t for t in range(pk, h) if D[t] <= 0), None)
    return D, solde, pk, ext


T_PERM = 13      # 2040 : tous les calendriers étudiés sont en régime permanent (dernier changement de taux en 2033)


def baisse_finale(cout, fin0, t):
    """Baisse durable du taux normal (points) que permet l'excédent de régime permanent, en tenant compte de ce que le
    coût de la déduction baisse avec le taux : x = (F - C) / (P - C/25), évalué l'année max(t, 2040)."""
    t = max(t, T_PERM)
    F = fin0 * (1 + G) ** t
    C = cout[t]
    P = POINT * (1 + G) ** t
    return (F - C) / (P - C / (100 * TAU))


# ================================================================ 2. paramètres de la proposition
p("")
p("=" * 100)
p("2. PARAMÈTRES ET HYPOTHÈSES PROPRES À LA REFONTE")
# Part de l'investissement éligible couverte par un plafond annuel de 1 M€ par groupe (theta).
# Insee, Les entreprises en France, éd. 2023, fiche 3.3 (Ésane 2021) : 248,7 Md€ d'investissements corporels bruts ;
# 1,2 million d'entreprises ont investi ; 2 % ont investi au moins 500 000 € et font 87 % du total ; 59 % moins de
# 10 000 € (1 % du total). Interpolation de Pareto sur le nombre d'entreprises entre 10 000 et 500 000 € (calcul de
# l'auteur), prolongée jusqu'à 1 M€.
INV21, NINV, S500, N10, N500 = 248.7, 1.2e6, 0.87, 0.41, 0.02
alpha = np.log(N10 / N500) / np.log(50)
n1m = N500 * 2 ** (-alpha)
moy = alpha / (1 - alpha) * (1 - 0.5 ** (1 - alpha)) / (0.5 ** (-alpha) - 1)    # M€, entre 0,5 et 1 M€
inv_05_1 = (N500 - n1m) * NINV * moy / 1000
th500 = (1 - S500) + N500 * NINV * 0.5 / 1000 / INV21
th1m = (1 - S500) + inv_05_1 / INV21 + n1m * NINV * 1.0 / 1000 / INV21
p(f"[PLAFOND] Pareto sur les effectifs : alpha {alpha:.2f} ; entreprises ≥ 1 M€ : {100*n1m:.2f} % des investisseurs "
  f"({n1m*NINV:,.0f}) ; part de l'investissement couverte par un plafond de 0,5 M€ : {100*th500:.1f} % ; de 1 M€ : "
  f"{100*th1m:.1f} %".replace(",", " "))
THETA, THETAS = 0.20, (0.15, 0.20, 0.30)
p(f"[PLAFOND] retenu : theta = {THETA:.0%} (15 à 30 %) ; champ Insee plus large (bâtiments, entreprises individuelles), "
  "composition des investissements par taille inconnue : hypothèse H23 du tableau d'annexe")
J["theta"] = {"pareto_500k": th500, "pareto_1M": th1m, "retenu": THETA}

FIN = {"bas": sim.ELARG_PRUDENT, "haut": sum(sim.ELARG.values())}
FIN["central"] = (FIN["bas"] + FIN["haut"]) / 2
TR = {"bas": sim.REDUIT[0], "haut": sim.REDUIT[1]}
p(f"[FIN] ressources de l'assiette en 2027 : bas {FIN['bas']:.2f} ; central {FIN['central']:.2f} ; haut {FIN['haut']:.2f} Md€ "
  f"(fin du taux réduit {TR['bas']:.2f} à {TR['haut']:.2f} ; CIR au niveau du groupe {0.57*sim.A25:.2f} ; zones IR et IS "
  f"{0.52*sim.A25:.2f} ; brevets {0.2*sim.A25:.2f} à {0.6*sim.A25:.2f}) ; un point de taux = {POINT:.2f} Md€ "
  f"({POINT_TR:.2f} sur la seule base au taux normal)")
J["fin"] = FIN
J["point"] = POINT

# ================================================================ 3. réforme naïve : baisse générale du taux
p("")
p("=" * 100)
p("3. RÉFORME NAÏVE : BAISSE GÉNÉRALE DU TAUX NORMAL (taux réduit gardé)")
naive = {}
for pts in (1, 3, 5):
    stat = pts * POINT_TR
    dyn = [-((TAU - pts / 100) * sim.BASE_NORMALE * sim.AB * (1 + e / 100 * pts) - TAU * sim.BASE_NORMALE * sim.AB)
           for e in (1.0, 1.5)]
    naive[pts] = (stat, dyn[1], dyn[0])
    p(f"[NAIF] −{pts} point(s) (taux {25-pts} %) : coût statique {stat:.1f} Md€ ; avec retour de bénéfices déclarés "
      f"(1 à 1,5 % par point) {dyn[1]:.1f} à {dyn[0]:.1f} Md€")
J["naif"] = naive
# Bénéfices par taille : 2024 (DGFiP n° 39, tableau 2), dernière année publiée ; base à 15 % de 2024 : 30,0 Md€ (n° 51)
ben = {k: v[0] for k, v in TAILLE24.items()}
BR24 = 30.0
qui = {}
for lab, part_tpe in (("haut TPE", 1.0), ("bas TPE", 0.75)):
    bn = dict(ben)
    bn["Très petites"] -= BR24 * part_tpe
    bn["PME"] -= BR24 * (1 - part_tpe)
    tot = sum(bn.values())
    qui[lab] = {k: v / tot for k, v in bn.items()}
    p(f"[NAIF qui] bénéfices de 2024 ; base à 15 % ({'toute' if part_tpe == 1 else 'aux trois quarts'} chez les très petites) : "
      + " ; ".join(f"{k} {100*v/tot:.0f} %" for k, v in bn.items()))
J["naif_qui"] = qui
# Part d'une baisse du taux qui allège l'impôt sur le rendement normal des équipements neufs.
va_lin = va_millesime("lin")
va_deg = va_millesime("deg")
part_norm = (va_lin / 25) / POINT_TR
p(f"[NAIF part] impôt actualisé sur le rendement normal d'une année d'équipements (= coût actualisé de la déduction "
  f"totale) : {va_deg:.2f} à {va_lin:.2f} Md€ ; un point de taux en retire 1/25, soit {va_deg/25:.3f} à {va_lin/25:.3f} "
  f"Md€, pour un coût de {POINT_TR:.2f} Md€ par an : {100*va_deg/25/POINT_TR:.1f} à {100*part_norm:.1f} % du coût")
J["naif_part_equipements"] = (va_deg / 25 / POINT_TR, part_norm)


# ---------------------------------------------------------------- taux effectifs (Devereux et Griffith, 2003)
def dg(tau, zv, p_=0.20, r=0.05, pi=0.02, delta=0.14):
    """Financement par fonds propres, sans impôt personnel ; z actualisé au taux nominal rho = (1+r)(1+pi)-1.
    Renvoie (coût du capital p~, TEMI, TEMA pour un projet de rendement p_)."""
    A = tau * zv
    rho = (1 + r) * (1 + pi) - 1
    pt = (1 - A) * (rho + delta * (1 + pi) - pi) / ((1 - tau) * (1 + pi)) - delta
    temi = (pt - r) / pt
    Rs = (p_ - r) / (1 + r)
    Rn = -(1 - A) + ((1 + pi) * (p_ + delta) * (1 - tau) + (1 + pi) * (1 - delta) * (1 - A)) / (1 + rho)
    tema = (Rs - Rn) / (p_ / (1 + r))
    return pt, temi, tema


RHO = 1.05 * 1.02 - 1
zl_r, zd_r = z(PLANS["lin"], RHO), z(PLANS["deg"], RHO)
zb_r = z(np.array([0.5 / 25] + [1 / 25] * 24 + [0.5 / 25]), RHO)
TEF = {}


def tef(nom, tau, zv, delta=0.14):
    pt, temi, tema = dg(tau, zv, delta=delta)
    coin = tau * (1 - zv) / (1 - tau) if delta == 0.14 else None
    TEF[nom] = {"temi": temi, "tema": tema, "tau": tau, "z": zv}
    p(f"[TEF] {nom:62s} taux {100*tau:5.2f} % z {zv:.3f} : TEMI {100*temi:5.1f} % ; TEMA (projet à 20 %) {100*tema:5.1f} %"
      + (f" ; coin {100*coin:4.2f} %" if coin is not None else ""))


p("")
p("[TEF] convention : fonds propres, r réel 5 %, inflation 2 %, δ 14 % (équipements) ou 3,1 % (bâtiments), z au taux "
  "nominal ; niveaux non comparables à l'OCDE (part de dette non lue), écarts seuls significatifs")
x_eq = va_lin / POINT_TR                              # baisse de même coût actualisé que la déduction totale
tef("Équipement, aujourd'hui (25 %, linéaire 7 ans)", 0.25, zl_r)
tef("Équipement, aujourd'hui (25 %, dégressif)", 0.25, zd_r)
tef(f"Équipement, baisse de même coût actualisé ({25-x_eq:.2f} %)", 0.25 - x_eq / 100, zl_r)
tef("Équipement, baisse à 22 %", 0.22, zl_r)
tef("Équipement, baisse à 20 %", 0.20, zl_r)
tef("Équipement, déduction immédiate 50 % (25 %)", 0.25, z(0.5 * E0 + 0.5 * PLANS["lin"], RHO))
tef("Équipement, déduction immédiate 100 % (25 %)", 0.25, 1.0)
tef("Équipement, petite société sous 42 500 € aujourd'hui (15 %)", 0.15, zl_r)
tef("Bâtiment, aujourd'hui (25 %)", 0.25, zb_r, delta=0.031)
tef("Bâtiment, petite société sous 42 500 € aujourd'hui (15 %)", 0.15, zb_r, delta=0.031)
tef("Bâtiment, baisse à 22 %", 0.22, zb_r, delta=0.031)
J["x_eq"] = x_eq
coin = lambda tau, zv: tau * (1 - zv) / (1 - tau)
zl5 = z(PLANS["lin"])
p(f"[NAIF eff] baisse de même coût actualisé que la déduction totale (linéaire, 5 %) : {x_eq:.2f} point ; coin sur le coût "
  f"d'usage des équipements {100*coin(.25, zl5):.2f} % -> {100*coin(.25-x_eq/100, zl5):.2f} % (déduction totale : 0)")
J["coin"] = {"auj": coin(.25, zl5), "naif_eq": coin(.25 - x_eq / 100, zl5)}

# ================================================================ 4. calendriers de la déduction immédiate
p("")
p("=" * 100)
p("4. CALENDRIERS DE LA DÉDUCTION IMMÉDIATE (part imposable 75 %, θ = 20 %)")
pal = lambda t: min(1.0, 0.5 + 0.1 * t)
OPTIONS = {
    "falaise": ("50 % de 2027 à 2032, 100 % en 2033 (ancienne note)", lambda t: 0.5 if t < 6 else 1.0),
    "paliers": ("50 % en 2027, +10 points par an, 100 % en 2032", pal),
    "plafond_paliers": ("100 % sous 1 M€ dès 2027 ; au-delà, paliers 50 → 100 % (2032)",
                        lambda t: THETA + (1 - THETA) * pal(t)),
    "plafond_seul": ("100 % sous 1 M€ par groupe, sans plus (AIA britannique seule)", lambda t: THETA),
    "cent": ("100 % pour tous dès 2027", lambda t: 1.0),
    "cinquante": ("50 % pour tous, sans montée", lambda t: 0.5),
    "neutre": ("Amortissement neutre (annuités revalorisées à 3,25 %)", None),
}


def cout_opt(cle, reg, part=PART, theta=THETA, g=G):
    if cle == "neutre":
        return chemin(reg, None, part=part, g=g, neutre=R_ETAT)
    f = OPTIONS[cle][1]
    if cle == "plafond_paliers":
        f = lambda t: theta + (1 - theta) * pal(t)
    elif cle == "plafond_seul":
        f = lambda t: theta
    return chemin(reg, f, part=part, g=g)


def cout_mix(cle, **kw):
    return (cout_opt(cle, "lin", **kw) + cout_opt(cle, "deg", **kw)) / 2


RES = {}
for cle, (nom, _) in OPTIONS.items():
    c = {reg: cout_opt(cle, reg) for reg in ("lin", "deg")}
    c["mix"] = (c["lin"] + c["deg"]) / 2
    RES[cle] = c
    b_perm = {"plafond_seul": THETA, "cinquante": 0.5}.get(cle, 1.0)
    if cle == "neutre":
        va = (va_millesime("deg", neutre=R_ETAT), va_millesime("lin", neutre=R_ETAT))
        va_e = (va_millesime("deg", r=R_ETAT, neutre=R_ETAT), va_millesime("lin", r=R_ETAT, neutre=R_ETAT))
    else:
        va = (va_millesime("deg", b_perm), va_millesime("lin", b_perm))
        va_e = (va_millesime("deg", b_perm, r=R_ETAT), va_millesime("lin", b_perm, r=R_ETAT))
    marche = max(c["mix"][t] - c["mix"][t - 1] for t in range(1, 15))
    pic_c, an_pic_c = c["mix"][:15].max(), AN1 + int(np.argmax(c["mix"][:15]))
    p(f"[OPT {cle}] {nom}")
    p(f"    coût (dég. – lin., Md€) 2027 {c['deg'][0]:.1f}–{c['lin'][0]:.1f} ; 2028 {c['deg'][1]:.1f}–{c['lin'][1]:.1f} ; "
      f"2030 {c['deg'][3]:.1f}–{c['lin'][3]:.1f} ; 2032 {c['deg'][5]:.1f}–{c['lin'][5]:.1f} ; 2033 {c['deg'][6]:.1f}–{c['lin'][6]:.1f} ; "
      f"2034 {c['deg'][7]:.1f}–{c['lin'][7]:.1f} ; 2040 {c['deg'][13]:.1f}–{c['lin'][13]:.1f} ; pic central (2027-2041) {pic_c:.1f} "
      f"({an_pic_c}) ; plus forte hausse d'une année sur l'autre {marche:+.1f}")
    p(f"    coût actualisé par millésime en régime permanent : {va[0]:.2f}–{va[1]:.2f} Md€ (5 %) ; {va_e[0]:.2f}–{va_e[1]:.2f} "
      f"(3,25 %) ; en points de taux {va[0]/POINT:.2f}–{va[1]/POINT:.2f}")
    RES[cle]["va"] = va
    RES[cle]["va_etat"] = va_e
    for niv in ("bas", "central", "haut"):
        out = []
        for reg in ("deg", "mix", "lin"):
            D, sol, pk, ext = dette(c[reg], FIN[niv])
            bx = baisse_finale(c[reg], FIN[niv], ext + 1) if ext is not None else float("nan")
            out.append(f"{reg} : pic {D[pk]:.1f} ({AN1+pk}), éteinte {AN1+ext if ext is not None else 'non'}"
                       + (f", baisse {bx:.2f} pt dès {AN1+ext+1}" if ext is not None else f", dette 2066 {D[39]:.0f}"))
            RES[cle][(niv, reg)] = (D, sol, pk, ext, bx)
        p(f"    financement {niv} ({FIN[niv]:.2f}) : " + " | ".join(out))
# coût du passage à 100 % sous plafond par rapport aux seuls paliers
d27 = RES["plafond_paliers"]["mix"][0] - RES["paliers"]["mix"][0]
p(f"[OPT] surcoût du plafond à 100 % en 2027 par rapport aux seuls paliers : {d27:.2f} Md€ (central)")
# gain d'attente au passage d'un palier
for nom, db in (("falaise (50 → 100 points)", 0.5), ("palier annuel (10 points)", 0.1)):
    p(f"[ATTENTE] {nom} : acheter juste après le palier fait gagner τ × Δb × (1 − z) = {100*TAU*db*(1-zl5):.2f} % (linéaire) "
      f"/ {100*TAU*db*(1-z(PLANS['deg'])):.2f} % (dégressif) du prix")

# ================================================================ 5. sensibilités de la proposition retenue
p("")
p("=" * 100)
p("5. SENSIBILITÉS (proposition : 100 % sous plafond + paliers)")
CLE = "plafond_paliers"
for part in (0.60, 0.75, 0.90):
    out = []
    for reg in ("deg", "mix", "lin"):
        for niv in ("bas", "haut"):
            c = cout_opt(CLE, reg, part=part) if reg != "mix" else cout_mix(CLE, part=part)
            D, sol, pk, ext = dette(c, FIN[niv])
            out.append(f"{reg}-{niv} {D[pk]:.0f} → {AN1+ext if ext is not None else 'jamais'}")
    c = cout_mix(CLE, part=part)
    Dc, _, pkc, extc = dette(c, FIN["central"])
    out.append(f"central {Dc[pkc]:.0f} ({AN1+pkc}) → {AN1+extc if extc is not None else 'jamais'}")
    p(f"[PART {part:.0%}] coût 2027 {c[0]:.1f} ; dette max → année d'extinction : " + " ; ".join(out))
for th in THETAS:
    c = cout_mix(CLE, theta=th)
    D, sol, pk, ext = dette(c, FIN["central"])
    p(f"[THETA {th:.0%}] coût 2027 {c[0]:.1f} ; dette centrale max {D[pk]:.1f} ({AN1+pk}) éteinte {AN1+ext}")
for r in (0.025, 0.0325, 0.05):
    c = cout_mix(CLE)
    D, sol, pk, ext = dette(c, FIN["central"], r=r)
    p(f"[R_ETAT {r:.2%}] dette centrale max {D[pk]:.1f} ({AN1+pk}) éteinte {AN1+ext if ext is not None else 'jamais'}")
for g in (0.02, 0.04):
    c = cout_mix(CLE, g=g)
    D, sol, pk, ext = dette(c, FIN["central"], g=g)
    p(f"[G {g:.0%}] coût permanent 2034 {c[7]:.2f} ; dette centrale max {D[pk]:.1f} ({AN1+pk}) éteinte "
      f"{AN1+ext if ext is not None else 'jamais'}")
# investissement suscité : +10 % d'investissement éligible (ordre de grandeur de Zwick et Mahon), dès 2027
cind = cout_mix(CLE)
p(f"[INDUIT] +10 % d'investissement éligible : coût 2027 +{TAU*PART*0.1*I1*(THETA+(1-THETA)*0.5)*(1-np.mean([PLANS['lin'][0], PLANS['deg'][0]])):.2f} Md€, "
  "récupéré ensuite par l'impôt sur les rendements (non compté)")

# ================================================================ 6. financement : variantes
p("")
p("=" * 100)
p("6. FINANCEMENT : VARIANTES (proposition, régime mixte)")
cP = RES[CLE]["mix"]
NICHES = (FIN["bas"] - TR["bas"], FIN["haut"] - TR["haut"])
VARF = {"assiette (référence)": (FIN["bas"], FIN["haut"]),
        "taux réduit porté à 20 % (moitié de l'avantage)": (NICHES[0] + TR["bas"] / 2, NICHES[1] + TR["haut"] / 2),
        "taux réduit maintenu": NICHES,
        "taux réduit retiré aux seules sociétés immobilières et financières (24 à 31 % du rendement, hypothèse)":
            (NICHES[0] + (4.1 + 12.7) / 70.5 * TR["bas"], NICHES[1] + (631 + 248) / 2834 * TR["haut"]),
        "taux normal à 28 % (taux réduit gardé ; 1,5 à 0 % de base perdue par point)":
            (sim.recette_taux(3, 1.5), sim.recette_taux(3, 0))}
VF = {}
for nom, (fb, fh) in VARF.items():
    out = []
    for f in (fb, fh):
        D, sol, pk, ext = dette(cP, f)
        out.append(f"{f:.2f} Md€ : pic {D[pk]:.0f} ({AN1+pk}), " + (f"éteinte {AN1+ext}" if ext is not None
                                                                     else f"non éteinte, {D[39]:.0f} Md€ en 2066"))
    VF[nom] = (fb, fh)
    p(f"[VARFIN] {nom} : " + " | ".join(out))
# taux réduit réservé : part des sociétés de l'immobilier et de la finance (DGFiP n° 51, tableau 1, exercice 2025 ;
# 2022, DGFiP n° 21 : 28 % du nombre, 23 % de l'IS brut)
n_tot, n_imm, n_fin = 2834.0, 631.0, 248.0
isb_tot, isb_imm, isb_fin = 70.5, 4.1, 12.7
SH_N, SH_I = (n_imm + n_fin) / n_tot, (isb_imm + isb_fin) / isb_tot
p(f"[RÉSERVÉ] sociétés à l'IS des activités immobilières et financières : {100*SH_N:.0f} % du nombre, "
  f"{100*SH_I:.0f} % de l'IS brut (2025) ; si la base à 15 % se répartissait ainsi (invérifiable), les en "
  f"exclure rapporterait {SH_I*TR['bas']:.1f} à {SH_N*TR['haut']:.1f} Md€")
# taux réduit supprimé en deux ans (20 % en 2027, 25 % ensuite)
ext_extra = np.zeros(H)
ext_extra[0] = -(TR["bas"] + TR["haut"]) / 4
D0 = dette(cP, FIN["central"])
D1 = dette(cP, FIN["central"], extra=ext_extra)
p(f"[DEUX ANS] taux réduit à 20 % en 2027 puis supprimé : ressource 2027 {ext_extra[0]:.2f} Md€ ; dette centrale max "
  f"{D0[0][D0[2]]:.1f} → {D1[0][D1[2]]:.1f} ; extinction {AN1+D0[3]} → {AN1+D1[3]}")

# ================================================================ 7. contribution exceptionnelle
p("")
p("=" * 100)
p("7. CONTRIBUTION EXCEPTIONNELLE")
CE = {2025: 7.5, 2026: 7.0}
p("[CE] rendement : 7,5 Md€ (2025), ≈ 7,0 (2026) ; droit en vigueur : rien à partir de l'exercice 2027 ; PLF 2027 art. 15 "
  "(troisième exercice à taux réduits) : 5,0 en 2027 et 0,5 en 2028")
p("[CE] par rapport à 2026, l'extinction est une baisse de 7 Md€ ; par rapport au PLF 2027, de 5 Md€ en 2027")
extra_ce = np.zeros(H)
extra_ce[0], extra_ce[1] = 5.0, 0.5
CE_RES = {}
for niv in ("bas", "central", "haut"):
    for reg in ("deg", "mix", "lin"):
        c = RES[CLE][reg]
        D0, _, pk0, ext0 = dette(c, FIN[niv])
        D1, _, pk1, ext1 = dette(c, FIN[niv], extra=extra_ce)
        CE_RES[(niv, reg)] = (D0[pk0], ext0, D1[pk1], ext1)
        p(f"[CE affectée] {niv} {reg} : sans {D0[pk0]:.1f} (éteinte {AN1+ext0 if ext0 is not None else 'non'}) ; avec une "
          f"dernière année affectée à la transition {max(D1[pk1], 0):.1f} (éteinte {AN1+ext1 if ext1 is not None else 'non'})")

# ================================================================ 8. cas types
p("")
p("=" * 100)
p("8. CAS TYPES (€ par an ; valeur de la déduction = valeur actualisée à 5 % de l'avance d'impôt, par année d'achats)")
d0 = PLANS["lin"][0]
gain_va = lambda inv: TAU * inv * (1 - zl5)
avance = lambda inv, b: TAU * inv * b * (1 - d0)


def is_actuel(b):
    return 0.15 * min(b, 42_500) + 0.25 * max(b - 42_500, 0)


CAS = {}
# PME industrielle : bénéfice 300 000 €, achète 150 000 € de machines par an (sous le plafond : 100 % dès 2027)
b, inv = 300_000, 150_000
ia = is_actuel(b)
CAS["PME industrielle"] = {"benefice": b, "invest": inv, "is_actuel": ia, "taux_reduit": 4250,
                           "deduction": gain_va(inv), "avance_2027": avance(inv, 1.0)}
# PME de services : bénéfice 40 000 €, 10 000 € d'informatique par an
b, inv = 40_000, 10_000
CAS["PME de services"] = {"benefice": b, "invest": inv, "is_actuel": is_actuel(b), "taux_reduit": 0.10 * b,
                          "deduction": gain_va(inv), "avance_2027": avance(inv, 1.0)}
# Société qui n'investit pas (profession libérale, holding patrimoniale) : bénéfice 42 500 €
b = 42_500
CAS["Société qui n'investit pas"] = {"benefice": b, "invest": 0, "is_actuel": is_actuel(b), "taux_reduit": 4250,
                                    "deduction": 0.0, "avance_2027": 0.0}
# Grand groupe : bénéfice imposable en France 500 M€, chiffre d'affaires ≥ 3 Md€, 300 M€ d'équipements par an
b, inv = 500e6, 300e6
is25 = 0.25 * b
cs = 0.033 * (is25 - 763_000)
ce = 0.412 * is25
CAS["Grand groupe"] = {"benefice": b, "invest": inv, "is_actuel": is25 + cs, "is_2026": is25 + cs + ce, "ce": ce,
                       "taux_reduit": 0.0, "deduction": gain_va(inv),
                       "avance_2027": TAU * ((inv - 1e6) * 0.5 + 1e6) * (1 - d0)}
for k, v in CAS.items():
    net = v["taux_reduit"] - v["deduction"]
    v["net"] = net
    v["net_pct"] = net / v["is_actuel"]
    v["avance_net_2027"] = v["taux_reduit"] - v["avance_2027"]
    extra = (f" ; IS 2026 avec contribution exceptionnelle {fr(v['is_2026']/1e6)} M€, dont contribution {fr(v['ce']/1e6)} M€ "
             f"({100*v['ce']/v['is_2026']:.0f} % de l'impôt 2026)") if "ce" in v else ""
    p(f"[CAS] {k} : bénéfice {fr(v['benefice'],0)} € ; achats {fr(v['invest'],0)} €/an ; IS actuel {fr(v['is_actuel'],0)} € ; "
      f"fin du taux réduit +{fr(v['taux_reduit'],0)} ; valeur de la déduction −{fr(v['deduction'],0)} ; net {fr(net,0)} € "
      f"({100*v['net_pct']:+.1f} % de l'IS) ; trésorerie 2027 {fr(v['avance_net_2027'],0)} €{extra}")
gg = CAS["Grand groupe"]
BX = [RES[CLE][(niv, reg)][4] for niv in ("bas", "haut") for reg in ("deg", "lin")]
bx_lo, bx_hi = round(min(BX), 1), round(max(BX), 1)
p(f"[CAS] grand groupe : baisse finale de {fr(bx_lo)} à {fr(bx_hi)} point → {fr(bx_lo/100*gg['benefice']/1e6)} à "
  f"{fr(bx_hi/100*gg['benefice']/1e6)} M€ "
  f"par an de moins, après extinction de la dette ; fin de la contribution exceptionnelle : {fr(gg['ce']/1e6)} M€ de moins "
  f"dès 2027 ({100*gg['ce']/gg['is_2026']:.0f} % de l'impôt 2026)")
for r in (0.05, 0.08, 0.10):
    zr = z(PLANS["lin"], r)
    zrd = z(PLANS["deg"], r)
    p(f"[SEUIL r={r:.0%}] achats annuels qui compensent la perte maximale de 4 250 € : 100 % linéaire "
      f"{fr(4250/(TAU*(1-zr)),0)} € ; dégressif {fr(4250/(TAU*(1-zrd)),0)} € ; 50 % linéaire "
      f"{fr(4250/(TAU*0.5*(1-zr)),0)} €")
p(f"[CAS] associé d'une petite société qui distribue : IS + PFU sur 42 500 € {100*(0.15+0.85*0.314):.2f} % → "
  f"{100*(0.25+0.75*0.314):.2f} %")
J["cas"] = CAS

# ================================================================ 9. PIB et perte sèche (régime permanent = 100 %)
p("")
p("=" * 100)
p("9. PRODUCTION ET BIEN-ÊTRE (reprise de simulation_is.py et perte_seche_autres.py)")
sk = (0.05 + 0.14) * 541.0 / PIB25
for nom, dc, fac in (("100 % (proposition en régime permanent)", (0.034, 0.048), 1.0),
                     ("100 % sous plafond seulement (marge des seules sociétés sous le plafond)", (0.034, 0.048), THETA)):
    lo, hi = sk * 0.5 * dc[0] * 0.75 * fac, sk * 1.6 * dc[1] * 0.75 * fac
    mid = sk * sum(dc) / 2 * 0.75 * fac
    p(f"[PIB] {nom} : {100*lo:.3f} à {100*hi:.3f} % du PIB à long terme, central {100*mid:.3f} % ({mid*PIB25:.1f} Md€ de 2025)")
p("[PS] triangle évité (perte sèche statique sur le capital) : 0,02 à 0,16 Md€ par an ; IS à 28 % : +0,05 à +0,3 sur le "
  "capital, 0 à +3,2 par le transfert de bénéfices (synthese/sorties/perte_seche_autres.txt)")

# ================================================================ 10. tableau de transition année par année
p("")
p("=" * 100)
p("10. TRANSITION ANNÉE PAR ANNÉE (proposition, régime mixte, financement central, part 75 %)")
c = RES[CLE]["mix"]
D, sol, pk, ext = dette(c, FIN["central"])
bx = baisse_finale(c, FIN["central"], ext + 1)
taux_ded = [min(1.0, 0.5 + 0.1 * t) for t in range(H)]
res_ass = FIN["central"] * (1 + G) ** np.arange(H)
# coût permanent : tau s I_t (1 - z(g)), z actualisé au taux de croissance (formule fermée vérifiée, revue/hypotheses_is.md)
zg = {reg: z(PLANS[reg], G) for reg in PLANS}
perm27 = {reg: TAU * PART * I1 * (1 - zg[reg]) for reg in PLANS}
perm27["mix"] = (perm27["lin"] + perm27["deg"]) / 2
p(f"[PERM] coût permanent à l'échelle de 2027 (euros de 2027, investissement de 2027) : dégressif {perm27['deg']:.2f} ; "
  f"linéaire {perm27['lin']:.2f} ; central {perm27['mix']:.2f} Md€ ; en 2034 (courants) {perm27['deg']*(1+G)**7:.2f} à "
  f"{perm27['lin']*(1+G)**7:.2f} ; en % du PIB {100*perm27['deg']/PIB27:.3f} à {100*perm27['lin']/PIB27:.3f}")
p(f"[PERM] ressources de l'assiette à l'échelle de 2027 : {FIN['bas']:.2f} à {FIN['haut']:.2f} ; excédent permanent "
  f"{FIN['bas']-perm27['lin']:.2f} à {FIN['haut']-perm27['deg']:.2f} Md€")
CE26 = CE[2026]
rows = []
for t in range(0, 30):
    an = AN1 + t
    interets = (D[t - 1] if t > 0 else 0.0) * R_ETAT
    perm = perm27["mix"] * (1 + G) ** t
    rows.append({"an": an, "taux": taux_ded[t], "cout": c[t], "perm": perm, "trans": c[t] - perm, "ress": res_ass[t],
                 "solde": sol[t], "interets": interets, "dette": D[t], "dette_pib": 100 * D[t] / (PIB27 * (1 + G) ** t),
                 "avec_ce": sol[t] - CE26})
    p(f"[TRANS] {an} : déduction au-delà du plafond {100*taux_ded[t]:.0f} % ; coût {c[t]:5.2f} (permanent {perm:4.2f}, "
      f"transition {c[t]-perm:5.2f}) ; ressources {res_ass[t]:5.2f} ; solde {sol[t]:+6.2f} ; intérêts {interets:5.2f} ; "
      f"dette fin d'année {D[t]:6.2f} Md€ ({100*D[t]/(PIB27*(1+G)**t):.2f} % du PIB) ; avec la fin de la contribution "
      f"exceptionnelle, écart à 2026 {sol[t]-CE26:+6.2f}")
p(f"[TRANS] pic de la dette {D[pk]:.1f} Md€ en {AN1+pk} ({D[pk]/(1+G)**pk:.1f} Md€ de 2027 ; "
  f"{100*D[pk]/(PIB27*(1+G)**pk):.2f} % du PIB) ; éteinte en {AN1+ext} ; baisse finale de {bx:.2f} point dès {AN1+ext+1}")
p(f"[TRANS] cumul 2027-2032 du coût : {c[:6].sum():.1f} Md€, dont transition {sum(r_['trans'] for r_ in rows[:6]):.1f} ; "
  f"des ressources : {res_ass[:6].sum():.1f}")
p(f"[TRANS] contribution exceptionnelle : par rapport à 2026, −{CE26:.1f} Md€ chaque année (droit en vigueur, à bénéfices "
  f"de 2026) ; par rapport au PLF 2027, −5,0 en 2027 et −0,5 en 2028 ; écart total à 2026 en 2027 : {sol[0]-CE26:+.1f} "
  f"(réforme {sol[0]:+.1f}) ; par rapport au PLF : {sol[0]-5.0:+.1f}")
J["transition"] = {"rows": rows, "pic": D[pk], "an_pic": AN1 + pk, "extinction": AN1 + ext, "baisse": bx,
                   "perm27": perm27}
# bornes de la transition (quatre combinaisons) et part imposable
BORNES = {}
for reg in ("deg", "lin"):
    for niv in ("bas", "haut"):
        Dx, solx, pkx, extx = dette(RES[CLE][reg], FIN[niv])
        bxx = baisse_finale(RES[CLE][reg], FIN[niv], extx + 1) if extx is not None else float("nan")
        BORNES[(reg, niv)] = (Dx[pkx], AN1 + pkx, AN1 + extx if extx is not None else None, bxx)
        p(f"[BORNES] {reg} {niv} : pic {Dx[pkx]:.1f} ({AN1+pkx}) ; extinction {AN1+extx if extx is not None else 'jamais'} ; "
          f"baisse finale {bxx:.2f} point")
J["bornes"] = {f"{k[0]}_{k[1]}": v for k, v in BORNES.items()}

# ================================================================ 11. séries pour les figures
J["series"] = {cle: {reg: RES[cle][reg][:30].tolist() for reg in ("lin", "deg", "mix")} for cle in OPTIONS}
J["series_fin"] = {niv: (FIN[niv] * (1 + G) ** np.arange(30)).tolist() for niv in FIN}
J["dette_part"] = {}
for part in (0.60, 0.75, 0.90):
    cc = cout_mix(CLE, part=part)
    Dx, _, pkx, extx = dette(cc, FIN["central"])
    J["dette_part"][str(part)] = Dx[:45].tolist()
J["dette_bornes"] = {}
for reg in ("deg", "lin"):
    for niv in ("bas", "haut"):
        J["dette_bornes"][f"{reg}_{niv}"] = dette(RES[CLE][reg], FIN[niv])[0][:45].tolist()
J["tef"] = TEF
J["options_va"] = {k: RES[k]["va"] for k in OPTIONS}

# ================================================================ 12. tables LaTeX
def t(x, d=1):
    return fr(x, d).replace("−", "$-$")


def _ecrire_tab(chemin, lig):
    """Écrit un tableau de la note, sauf s'il a été retouché à la main (première ligne « % table éditée »)."""
    if chemin.exists() and chemin.read_text(encoding="utf-8").startswith("% table éditée"):
        return
    chemin.write_text("\n".join(lig) + "\n", encoding="utf-8")

# Tableau de transition (corps) : 2027-2035, puis années choisies
NUM = r">{\raggedleft\arraybackslash}p{1.5cm}"
lig = [r"\begin{table}[!htbp]\centering\footnotesize", r"\setlength{\tabcolsep}{4pt}",
       r"\caption{La transition année par année : l'État avance l'impôt, l'assiette le rembourse (Md€ courants, cas "
       r"central)}\label{tab:is_transition}",
       r"\begin{tabular}{@{}l" + NUM * 7 + r"@{}}", r"\toprule",
       r"Année & Taux de déduction & Coût & dont permanent & Ressources & Solde & Dette en fin d'année & "
       r"Écart de recette à 2026 \\", r"\midrule"]
for i in list(range(0, 9)) + [11, 14] + ([ext] if ext not in (11, 14) else []):   # sans doublon si l'extinction tombe en 2041
    r_ = rows[i]
    dt = t(r_['dette']) if r_['dette'] > 0 else "éteinte"
    lig.append(f"{r_['an']} & {r_['taux']*100:.0f}~\\% & {t(r_['cout'])} & {t(r_['perm'])} & {t(r_['ress'])} & "
               f"{t(r_['solde'])} & {dt} & {t(r_['avec_ce'])} \\\\")
lig.append(f"\\multicolumn{{8}}{{@{{}}l}}{{À partir de {AN1+ext+1} : baisse du taux normal de {t(bx, 1)} point, qui "
           f"rend l'excédent permanent aux entreprises.}} \\\\")
lig += [r"\bottomrule", r"\end{tabular}",
        r"\par\vspace{3pt}\parbox{\linewidth}{\raggedright\scriptsize Proposition : déduction immédiate de 100~\% des "
        r"équipements neufs sous un plafond annuel de 1~M€ par groupe dès 2027 ; au-delà, 50~\% en 2027 puis 10 points de "
        r"plus par an (taux de déduction au-delà du plafond). Coût de la déduction, ressources de l'assiette, solde de "
        r"la réforme. Cas central : régime actuel pour moitié linéaire, pour moitié dégressif ; 75~\% de l'investissement "
        r"éligible fait par des sociétés imposables et plafond couvrant 20~\% de cet investissement (hypothèses) ; "
        r"ressources au milieu de la fourchette, en hausse de 3~\% par an ; intérêts à 3,25~\%. Coût permanent : ce que "
        r"coûterait chaque année la déduction totale une fois la transition passée ; le reste du coût est une avance "
        r"d'impôt, remboursée par les années suivantes. Écart de recette à 2026 : solde de la réforme moins les 7~Md€ de "
        f"la contribution exceptionnelle perçus en 2026, qui s'éteint dans le droit en vigueur. La dette s'éteint en {AN1+ext} ; "
        f"la baisse finale du taux ({t(bx, 1)} point) vient ensuite. Années d'exercice : en caisse, coûts et ressources "
        r"arrivent environ un an plus tard. Source : \texttt{is/calculs\_note\_is.py}.}", r"\end{table}"]
_ecrire_tab(TAB / "tab_is_transition.tex", lig)

# Tableau complet (annexe) : 2027-2056, bornes
NUMS = r">{\raggedleft\arraybackslash}p{1.3cm}"
lig = [r"\begin{table}[!htbp]\centering\scriptsize", r"\setlength{\tabcolsep}{3.5pt}",
       r"\caption{Transition année par année, avec les bornes (Md€ courants)}\label{tab:is_transition_complet}",
       r"\begin{tabular}{@{}l" + NUMS * 8 + r"@{}}", r"\toprule",
       r"& \multicolumn{4}{c}{Cas central} & \multicolumn{2}{c}{Cas favorable} & \multicolumn{2}{c}{Cas défavorable}\\",
       r"\cmidrule(lr){2-5}\cmidrule(lr){6-7}\cmidrule(lr){8-9}",
       r"Année & Coût & Ressources & Solde & Dette & Coût & Dette & Coût & Dette \\", r"\midrule"]
Df = dette(RES[CLE]["deg"], FIN["haut"])[0]
Dd = dette(RES[CLE]["lin"], FIN["bas"])[0]
for i in range(30):
    r_ = rows[i]
    lig.append(f"{r_['an']} & {t(r_['cout'])} & {t(r_['ress'])} & {t(r_['solde'])} & {t(r_['dette'])} & "
               f"{t(RES[CLE]['deg'][i])} & {t(Df[i])} & {t(RES[CLE]['lin'][i])} & {t(Dd[i])} \\\\")
lig += [r"\bottomrule", r"\end{tabular}",
        r"\par\vspace{3pt}\parbox{\linewidth}{\raggedright\scriptsize Cas favorable : régime actuel dégressif, ressources "
        f"hautes ({t(FIN['haut'], 2)}~Md€ en 2027). Cas défavorable : régime actuel linéaire, ressources basses "
        f"({t(FIN['bas'], 2)}~Md€). Cas central : moitié-moitié, ressources au milieu ({t(FIN['central'], 2)}~Md€). Une dette "
        r"négative est un excédent cumulé : dans la proposition, il n'apparaît pas, car l'excédent est rendu par la baisse "
        r"du taux normal dès l'année qui suit l'extinction (le tableau montre ce qui se passerait sans cette baisse). "
        r"Part imposable : 75~\%. Source : \texttt{is/calculs\_note\_is.py}.}", r"\end{table}"]
_ecrire_tab(TAB / "tab_is_transition_complet.tex", lig)

# Tableau des calendriers (annexe)
PCT_TEX = "~" + chr(92) + "%"
lig = [r"\begin{table}[!htbp]\centering\scriptsize",
       r"\caption{Les calendriers de la déduction immédiate comparés (Md€ ; part imposable 75~\%)}\label{tab:is_options}",
       r"\begin{tabularx}{\linewidth}{@{}>{\raggedright\arraybackslash}X" + r">{\raggedleft\arraybackslash}p{1.45cm}" * 5 + "@{}}",
       r"\toprule",
       r"Calendrier & Coût 2027 & Plus forte hausse annuelle & Coût actualisé par année d'achats & Dette maximale "
       r"(cas central) & Extinction (central ; bornes) \\", r"\midrule"]
for cle in ("falaise", "paliers", "plafond_paliers", "plafond_seul", "cent", "cinquante", "neutre"):
    c = RES[cle]
    D, sol, pk, ext = c[("central", "mix")][:4]
    e_f = c[("haut", "deg")][3]
    e_d = c[("bas", "lin")][3]
    marche = max(c["mix"][k] - c["mix"][k - 1] for k in range(1, 15))
    f_e = lambda e: str(AN1 + e) if e is not None else "jamais"
    c27 = f"{t(c['deg'][0])}--{t(c['lin'][0])}" if c['lin'][0] > 0.05 else "0"
    dmax, extx = (t(D[pk]), f"{f_e(ext)} ({f_e(e_f)} à {f_e(e_d)})") if D[pk] > 0 else ("aucune", "---")
    nom_t = OPTIONS[cle][0].replace('→', 'à').replace(' %', PCT_TEX)
    lig.append(f"{nom_t} & {c27} & {t(max(marche, 0))} & "
               f"{t(c['va'][0])}--{t(c['va'][1])} & {dmax} & {extx} \\\\")
lig += [r"\bottomrule", r"\end{tabularx}",
        r"\par\vspace{3pt}\parbox{\linewidth}{\raggedright\scriptsize Coût 2027 : régime actuel dégressif -- linéaire. "
        r"Plus forte hausse annuelle : saut du coût d'une année sur l'autre (cas central) ; la falaise de 2033 en est le "
        r"cas extrême. Coût actualisé à 5~\% (taux des entreprises), en régime permanent. Bornes de l'extinction : cas "
        r"favorable (dégressif, ressources hautes) et défavorable (linéaire, ressources basses). Plafond : 1~M€ par "
        r"groupe, couvrant 20~\% de l'investissement éligible (hypothèse). Amortissement neutre : plans actuels, "
        r"annuités revalorisées au taux d'emprunt de l'État. Source : \texttt{is/calculs\_note\_is.py}.}",
        r"\end{table}"]
_ecrire_tab(TAB / "tab_is_options.tex", lig)

(OUT / "calculs_note_is.txt").write_text("\n".join(L) + "\n", encoding="utf-8")


def _js(o):
    if isinstance(o, (np.floating, np.integer)):
        return o.item()
    if isinstance(o, np.ndarray):
        return o.tolist()
    if isinstance(o, tuple):
        return list(o)
    raise TypeError(type(o))


(OUT / "calculs_note_is.json").write_text(json.dumps(J, default=_js, ensure_ascii=False, indent=1), encoding="utf-8")
print("\n".join(L))
