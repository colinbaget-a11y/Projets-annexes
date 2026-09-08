"""
Une seule métrique : combien de productivité de long terme vaut +10 points de score PISA ?

Unité commune : +10 points sur la MOYENNE DES TROIS DOMAINES (maths, écrit, sciences),
de façon durable, et l'effet sur le niveau de productivité une fois la population active
entièrement renouvelée. Vérification faite pour chaque étude que les points sont bien
définis sur la moyenne des trois domaines et non cumulés ou pris sur un seul domaine.

Sortie : le tableau de note_chiffrage.md, et le calcul France.
"""
import math

# ------------------------------------------------------------------ le choc France
FRANCE = {2006: (496, 488, 495), 2009: (497, 496, 498), 2012: (495, 505, 499),
          2015: (493, 499, 495), 2018: (495, 493, 493), 2022: (474, 474, 487),
          2025: (458, 456, 483)}
MOYENNE = {y: sum(v) / 3 for y, v in FRANCE.items()}
BASE = MOYENNE[2018]                       # 493,7 : niveau de référence pour les logs
CHOC = MOYENNE[2025] - MOYENNE[2018]       # -28,0 points

# --------------------------------------------------- paramètres des chaînes (annexe)
# Passage PISA (15 ans) -> compétences adultes (PIAAC), Égert et al. 2022, Table 4 :
# élasticité log-log de 0,278 avec les années d'études en contrôle (valeur retenue par l'OCDE).
ELAST_PIAAC = 0.278
ELAST_PGF = (2.36, 2.84)        # capital humain -> PGF, Égert et al. 2022, panel DOLS
ELAST_SECTOR = (1.80, 2.29)     # score PIAAC -> productivité du travail, OCDE 2024 (PIAAC 2023)
RENDEMENT_MICRO = 0.174         # salaire horaire par écart-type PIAAC, France (Hanushek et al. 2015)
PIAAC_MOYENNE, PIAAC_SD = 262.7, 53.0

DIX_POINTS = 10 / BASE          # variation en log pour +10 points


def coeff_egert():
    """Cadre macro OCDE : PISA -> capital humain -> PGF. Publié : +25,5 pts -> +3,4 à +4,1 % de PGF."""
    return tuple(100 * (e * ELAST_PIAAC * DIX_POINTS) for e in ELAST_PGF)


def coeff_ocde_france():
    """Étude économique France 2024 : +29,2 pts (écart au top 10 OCDE) -> +2,7 % de productivité."""
    return (2.7 / 29.2 * 10,)


def coeff_piaac_sectoriel():
    """OCDE 2024 : productivité du travail pays x secteur sur les scores PIAAC 2023."""
    return tuple(100 * (e * ELAST_PIAAC * DIX_POINTS) for e in ELAST_SECTOR)


def coeff_cae():
    """CAE Focus 91 : +10 pts (mathématiques) -> +0,6 à +1,4 % de productivité à 15 ans."""
    return (0.6, 1.4)


def coeff_micro():
    """Contrôle : rendement salarial des compétences, sans externalité ni effet d'allocation."""
    dsd = ELAST_PIAAC * DIX_POINTS * PIAAC_MOYENNE / PIAAC_SD
    return (100 * RENDEMENT_MICRO * dsd,)


ETUDES = [
    ("Égert, de la Maisonneuve & Turner 2022", "+25,5 pts (moyenne 3 domaines)",
     "+3,4 à +4,1 % de PGF", coeff_egert(), "long terme"),
    ("OCDE, Étude économique France 2024", "+29,2 pts (moyenne 3 domaines)",
     "+2,7 % de productivité", coeff_ocde_france(), "long terme"),
    ("OCDE, PIAAC 2023 et productivité 2024", "+10 % de score PIAAC",
     "+18 % de productivité du travail", coeff_piaac_sectoriel(), "long terme"),
    ("CAE, Focus 91 (2022)", "+10 pts en mathématiques",
     "+0,6 à +1,4 % de productivité", coeff_cae(), "15 ans, renouvellement partiel"),
    ("Contrôle micro : Hanushek et al. 2015", "+1 écart-type PIAAC",
     "+17,4 % de salaire horaire", coeff_micro(), "long terme, sans externalité"),
]

REGLE = 1.0   # % de productivité de long terme par +10 points, ordre de grandeur retenu

if __name__ == "__main__":
    print("=== Combien vaut +10 points de score PISA moyen ? ===")
    for nom, choc, publie, c, horizon in ETUDES:
        v = f"+{c[0]:.1f} %" if len(c) == 1 else f"+{c[0]:.1f} à +{c[1]:.1f} %"
        print(f"  {nom:42s} | {choc:32s} | {publie:32s} | {v:>16s}  ({horizon})")

    bornes = [v for _, _, _, c, h in ETUDES[:3] for v in c]
    print(f"\n  Estimations macro de long terme : +{min(bornes):.1f} à +{max(bornes):.1f} % par 10 points")
    print(f"  Contrôle micro (plancher, sans externalité) : +{coeff_micro()[0]:.1f} %")
    print(f"  Règle de pouce retenue : +{REGLE:.0f} % de productivité par +10 points durables")

    print("\n=== Le calcul France ===")
    for y in sorted(MOYENNE):
        print(f"  {y} : {MOYENNE[y]:.1f}")
    print(f"  2018 -> 2025 : {CHOC:+.1f} points sur la moyenne des trois domaines")
    print(f"  {CHOC:+.1f} points x {REGLE:.0f} % / 10 points = {CHOC / 10 * REGLE:+.1f} % de productivité de long terme")
    print(f"  fourchette (+0,5 à +1,6 % par 10 points) : "
          f"{CHOC / 10 * 0.5:+.1f} % à {CHOC / 10 * 1.6:+.1f} %")
