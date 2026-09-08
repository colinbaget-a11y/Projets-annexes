"""
Chiffrages simples : baisse des scores PISA de la France
  1) équivalent en années de scolarité perdues
  2) équivalent en PIB de long terme (deux cadres : effet de niveau vs effet de croissance)

Toutes les hypothèses sont des paramètres explicites ci-dessous.
"""
import numpy as np

# ---------- Scores France (moyennes OCDE publiées) ----------
# Seules les comparaisons depuis l'année où le domaine était majeur sont valides :
# lecture depuis 2000, maths depuis 2003, sciences depuis 2006.
FRANCE = {
    "maths":   {2003: 511, 2006: 496, 2009: 497, 2012: 495, 2015: 493, 2018: 495, 2022: 474, 2025: 458},
    "lecture": {2000: 505, 2003: 496, 2006: 488, 2009: 496, 2012: 505, 2015: 499, 2018: 493, 2022: 474, 2025: 456},
    "sciences":{2006: 495, 2009: 498, 2012: 499, 2015: 495, 2018: 493, 2022: 487, 2025: 483},
}
SD_PISA = 100.0   # écart-type élève OCDE à la base de l'échelle (Hanushek-Woessmann raisonnent dans cette unité)

# ---------- Paramètre 1 : points PISA par année de scolarité ----------
POINTS_PAR_ANNEE = {
    "Avvisati-Givord 2021, moyenne 31 pays (~1/5 SD)": 20,
    "Avvisati-Givord 2021, pays riches européens (>=25)": 25,
    "Hanushek-Woessmann 2020, règle 1 an = 1/3 SD": 33.3,
    "Ancienne règle OCDE (rapports PISA <=2012)": 40,
}

# ---------- Paramètre 2a : effet de niveau via rendement des compétences (PIAAC) ----------
RENDEMENT_PAR_SD = {"France (HSWW 2015, Table 2)": 0.174, "Pooled 23 pays (HSWW 2015)": 0.178}
# ---------- Paramètre 2b : effet de croissance (Hanushek-Woessmann 2012/2020) ----------
CROISSANCE_PAR_SD = 1.98  # points de % de croissance annuelle du PIB/tête par SD de compétences de la main-d'oeuvre
ANNEES_VIE_ACTIVE = 45    # durée pour que toute la main-d'oeuvre soit composée des cohortes touchées
BASE_YEAR = 2025

def baisse(domaine, depuis):
    s = FRANCE[domaine]; return s[depuis] - s[2025]

def annees_perdues(delta_pts):
    return {k: delta_pts / v for k, v in POINTS_PAR_ANNEE.items()}

def pib_niveau(delta_pts, rendement):
    """Effet de long terme sur log PIB/tête une fois toutes les cohortes remplacées."""
    return -rendement * delta_pts / SD_PISA

def pib_croissance(delta_pts, horizon):
    """Cadre H&W : la croissance annuelle baisse de 1.98 pp x SD x (part de la main-d'oeuvre touchée).
    Baisse permanente pour toutes les cohortes à partir de BASE_YEAR ; la part touchée monte linéairement
    de 0 à 1 sur ANNEES_VIE_ACTIVE. Retourne l'écart de log PIB à l'horizon."""
    dS = delta_pts / SD_PISA
    T = horizon - BASE_YEAR
    ramp = min(T, ANNEES_VIE_ACTIVE)
    integ = ramp**2 / (2 * ANNEES_VIE_ACTIVE) + max(0, T - ANNEES_VIE_ACTIVE)   # ∫ part(t) dt
    return -(CROISSANCE_PAR_SD / 100) * dS * integ

if __name__ == "__main__":
    scen = [("maths", 2003), ("maths", 2018), ("maths", 2022), ("lecture", 2000), ("lecture", 2018), ("sciences", 2006)]
    print("=== 1) Années de scolarité perdues (par élève de 15 ans, 2025 vs année de référence) ===")
    for d, y in scen:
        dp = baisse(d, y)
        print(f"\n{d} : {FRANCE[d][y]} ({y}) -> {FRANCE[d][2025]} (2025) = {dp:+d} pts = {dp/SD_PISA:.2f} SD")
        for k, v in annees_perdues(dp).items(): print(f"   {v:4.1f} an(s)  [{k}]")
    print("\n=== 2a) PIB de long terme, effet de niveau (log-points, toutes cohortes remplacées) ===")
    for d, y in scen:
        dp = baisse(d, y)
        vals = "  ".join(f"{100*pib_niveau(dp, r):+.1f}% [{k.split(' (')[0]}]" for k, r in RENDEMENT_PAR_SD.items())
        print(f"{d} depuis {y} ({dp:+d} pts) : {vals}")
    print("\n=== 2b) PIB, cadre 'effet de croissance' H&W (écart de log PIB à l'horizon) ===")
    for d, y in scen:
        dp = baisse(d, y)
        print(f"{d} depuis {y} ({dp:+d} pts) : croissance -{CROISSANCE_PAR_SD*dp/SD_PISA:.2f} pp/an à terme ; "
              + "  ".join(f"{h}: {100*pib_croissance(dp,h):+.0f}%" for h in (2040, 2050, 2075, 2100)))
