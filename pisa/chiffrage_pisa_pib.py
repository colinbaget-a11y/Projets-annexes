"""
Effet de long terme d'une baisse durable des scores PISA français sur le PIB par tête.

Un seul choc, trois estimations, un même objet mesuré :
  écart de niveau de PIB réel par tête (≈ productivité du travail à taux d'emploi inchangé)
  une fois la population active entièrement composée de générations ayant subi la baisse.

Toutes les hypothèses sont des constantes nommées ci-dessous. Sources : note_chiffrage.md.
"""
import math

# ---------------------------------------------------------------- le choc
# Moyenne des trois domaines (maths, compréhension de l'écrit, sciences).
# Comparable à partir de 2006 seulement : les sciences ne sont majeures qu'à partir de ce cycle.
FRANCE = {2006: (496, 488, 495), 2009: (497, 496, 498), 2012: (495, 505, 499),
          2015: (493, 499, 495), 2018: (495, 493, 493), 2022: (474, 474, 487),
          2025: (458, 456, 483)}
MOYENNE = {y: sum(v) / 3 for y, v in FRANCE.items()}
SD_ELEVE = 100.0          # écart-type élève, par construction de l'échelle PISA
REFERENCE, COURANT = 2018, 2025

# ------------------------------------------------- PISA 15 ans -> compétences adultes
# Élasticité log(score PIAAC de la cohorte) / log(score PISA de la même cohorte),
# Égert, de la Maisonneuve & Turner (2022, OECD ECO WP 1709), Table 4 : 0,278 avec les
# années d'études en contrôle (valeur retenue par l'OCDE), 0,603 sans.
# On NE suppose JAMAIS qu'un écart-type PISA devient un écart-type PIAAC.
ELAST_PIAAC = {"retenue (années d'études contrôlées)": 0.278, "haute (sans contrôle)": 0.603}
PIAAC_MOYENNE, PIAAC_SD = 262.7, 53.0   # France, numératie (Hanushek et al. 2015, Table 1)

# ------------------------------------------------------------- les trois élasticités
# 1. Cadre macro OCDE : capital humain -> productivité globale des facteurs.
ELAST_PGF = (2.36, 2.84)                 # Égert et al. 2022, panel DOLS, effets fixes pays
OCDE_FRANCE_PAR_POINT = 2.7 / 29.2       # Étude économique France 2024 : +2,7 % pour +29,2 points
PART_CAPITAL = 1 / 3                     # PGF -> PIB par tête : ÷ (1 - part du capital)

# 2. Productivité du travail sectorielle, PIAAC 2023 (OCDE 2024) : élasticité au score adulte.
ELAST_SECTORIELLE = (1.80, 2.29)         # scénario agrégé (18 % pour 10 %) ; Table 1 col. 1

# 3. Rendement individuel des compétences, France (Hanushek et al. 2015, PIAAC).
RENDEMENT = {"à diplôme donné": 0.094, "total": 0.174, "corrigé de l'erreur de mesure": 0.20}

# ------------------------------------------------------------------ diffusion
ENTREE, RENOUVELLEMENT_COMPLET = 2030, 2075

pct = lambda dlog: 100 * (math.exp(dlog) - 1)


def choc(reference=REFERENCE):
    """Baisse en points, en écarts-types élève et en log."""
    d = MOYENNE[COURANT] - MOYENNE[reference]
    return d, d / SD_ELEVE, math.log(MOYENNE[COURANT] / MOYENNE[reference])


def competences_adultes(dlog_pisa, elasticite):
    """Retourne (variation en log du score PIAAC, variation en écarts-types adultes)."""
    dlog = elasticite * dlog_pisa
    return dlog, dlog * PIAAC_MOYENNE / PIAAC_SD


def estimation_1(dlog_pisa, elasticite_piaac):
    """Cadre macro OCDE : PISA -> capital humain -> PGF -> PIB par tête."""
    dlog_ats, _ = competences_adultes(dlog_pisa, elasticite_piaac)
    generique = tuple(pct(e * dlog_ats / (1 - PART_CAPITAL)) for e in ELAST_PGF)
    france = pct(dlog_pisa * MOYENNE[REFERENCE] * OCDE_FRANCE_PAR_POINT / 100 / (1 - PART_CAPITAL))
    return france, generique


def estimation_2(dlog_pisa, elasticite_piaac):
    """Productivité du travail sectorielle : PISA -> PIAAC -> productivité (OCDE 2024)."""
    dlog_ats, _ = competences_adultes(dlog_pisa, elasticite_piaac)
    return tuple(pct(e * dlog_ats) for e in ELAST_SECTORIELLE)


def estimation_3(dlog_pisa, elasticite_piaac):
    """Micro : PISA -> PIAAC -> rendement des compétences, sans externalité."""
    _, dsd = competences_adultes(dlog_pisa, elasticite_piaac)
    return {k: pct(r * dsd) for k, r in RENDEMENT.items()}


def diffusion(effet_complet, annee):
    part = min(1.0, max(0.0, (annee - ENTREE) / (RENOUVELLEMENT_COMPLET - ENTREE)))
    return part, effet_complet * part


if __name__ == "__main__":
    print("=== 1. Le choc (moyenne des trois domaines) ===")
    for y in sorted(MOYENNE):
        print(f"   {y} : {MOYENNE[y]:.1f}")
    for ref in (2018, 2006):
        d, dsd, dlog = choc(ref)
        print(f"   {ref} -> 2025 : {d:+.1f} points = {dsd:+.2f} écart-type élève ({100*dlog:+.2f} % en log)")

    _, _, dlog_pisa = choc()
    print("\n=== 2. Étape commune : PISA à 15 ans -> compétences adultes ===")
    for lab, e in ELAST_PIAAC.items():
        dlog_ats, dsd = competences_adultes(dlog_pisa, e)
        print(f"   élasticité {e} [{lab}] : score PIAAC {100*dlog_ats:+.2f} % = {dsd:+.3f} écart-type adulte"
              f"  (persistance {abs(dsd)/abs(choc()[1]):.2f} SD par SD)")

    e = ELAST_PIAAC["retenue (années d'études contrôlées)"]
    print("\n=== 3. Trois estimations du PIB par tête de long terme ===")
    fr, gen = estimation_1(dlog_pisa, e)
    print(f"   1. Cadre macro OCDE      : {fr:+.1f} %   (calibration France 2024)"
          f" ; élasticités génériques {gen[0]:+.1f} à {gen[1]:+.1f} %")
    s = estimation_2(dlog_pisa, e)
    print(f"   2. Productivité sectorielle : {s[0]:+.1f} à {s[1]:+.1f} %")
    m = estimation_3(dlog_pisa, e)
    print("   3. Micro, rendement      : " + " ; ".join(f"{v:+.1f} % [{k}]" for k, v in m.items()))

    print("\n=== 4. Diffusion dans le temps (effet complet -3 %) ===")
    for t in (2035, 2040, 2050, 2060, 2070, 2075):
        part, v = diffusion(-3.0, t)
        print(f"   {t} : {100*part:3.0f} % de l'effet  ->  {v:+.1f} %")
