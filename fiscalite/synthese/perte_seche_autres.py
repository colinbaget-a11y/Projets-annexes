"""Perte sèche du foncier, de l'IS et du PFU : même formule (Harberger généralisé), voir revue/methode_perte_seche.md.

Variation de perte sèche = − Σ_j (coin moyen sur la marge j) × (variation de la quantité taxée j) ; pour une marge
où le coin passe de t0 à t1 avec une réaction linéaire, cela donne (t1² − t0²)/2 × pente. Les revenus déplacés
vers une autre assiette taxée ne comptent que pour l'écart de taux ; une réponse de calendrier ne compte pas.
Le « prix d'un milliard » (μ − 1) sert à comparer des variantes qui ne lèvent pas la même recette.

Lancer depuis fiscalite/ : python3 synthese/perte_seche_autres.py  ->  synthese/sorties/perte_seche_autres.txt
"""
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
OUT = HERE / "sorties"
OUT.mkdir(exist_ok=True)
MU1 = (0.16, 0.38, 0.60)    # prix d'un milliard levé par le barème fusionné (coin IR-CSG seul, non contributif, total)

# ---------------------------------------------------------------- foncier (foncier/sorties/simulation.txt)
V = 11.4 / 0.0581           # ventes de logements anciens, Md€ par an (2023-2024)
T0, T50, T30 = 0.0581, 0.0581 / 2, 0.0581 * 0.7
K_BATI = 6762 - 3068        # valeur du bâti des logements des particuliers, Md€
TB0, TB1 = 14.1 / K_BATI, 7.3 / K_BATI   # taxe foncière sur le bâti / valeur du bâti, avant et après
U = 0.045                   # coût d'usage du logement (part de la valeur), convention


def dmto(t1, sigma):
    """Triangle sur les ventes : sigma = baisse des ventes par point de droits (6 = 6 % par point)."""
    return sigma * V * (t1 ** 2 - T0 ** 2) / 2


def bati(eps, tb0=TB0, tb1=TB1):
    """Triangle sur le capital logement : coin = taxe sur le bâti / coût d'usage."""
    return eps * (K_BATI / U) * (tb1 ** 2 - tb0 ** 2) / 2


# ---------------------------------------------------------------- IS (is/sorties/simulation_is.txt)
K_EQ = 0.75 * 541.0         # équipements des sociétés imposables, Md€ (Insee 8.212, fin 2025 ; part imposable)
RD = 0.19                   # r + δ des équipements


def capital(m0, m1, eps):
    return RD * K_EQ * eps * (m1 ** 2 - m0 ** 2) / 2


# ---------------------------------------------------------------- PFU (pfu/notes/pfu_recherche.md)
B_PFU = 79.6                # assiette du PFU, Md€


def pfu(t1, e, pi, mu1, t0=0.314, cout_net=None):
    """Baisse du taux : réaction ΔQ = e·B·Δln(1−t) ; seule la part pi qui échappe définitivement à l'impôt est une
    perte sèche évitée ; la recette perdue doit être levée ailleurs au prix mu1."""
    dq = e * B_PFU * np.log((1 - t1) / (1 - t0))
    tbar = (t0 + t1) / 2
    perte_recette = (t0 * B_PFU - t1 * (B_PFU + dq)) if cout_net is None else cout_net
    return -pi * tbar * dq + mu1 * perte_recette, perte_recette, dq


if __name__ == "__main__":
    L = []
    p = L.append
    p(f"[FONCIER] ventes {V:.0f} Md€ ; bâti {K_BATI} Md€ ; taxe sur le bâti {100*TB0:.2f} % -> {100*TB1:.2f} % de la valeur")
    for nom, t1 in (("DMTO −50 %", T50), ("DMTO −30 %", T30)):
        p(f"  {nom} : σ = 3 / 6 / 8 / 15 -> " + " / ".join(f"{dmto(t1, s):+.2f}" for s in (3, 6, 8, 15)) + " Md€")
    p(f"  bâti (terrain = 4 × bâti, recette constante par commune) : ε_K = 0,5 / 1 -> {bati(0.5):+.2f} / {bati(1):+.2f} Md€")
    p(f"  central (DMTO −50 %, σ = 6, ε_K = 1) : {dmto(T50, 6) + bati(1):+.2f} Md€")
    p("  coût d'appariement (Määttänen et Terviö, interpolé, non calibré sur la France) : de l'ordre de −3,5 Md€")
    p("")
    p("[IS] triangle sur les équipements imposables ; m = coin sur le coût d'usage")
    for nom, m0, m1 in (("100 %, régime actuel linéaire", 0.051, 0.0), ("100 %, dégressif", 0.035, 0.0),
                        ("50 %, linéaire", 0.051, 0.025), ("IS à 28 %, linéaire", 0.051, 0.060)):
        p(f"  {nom} : ε = 0,5 / 1 / 1,6 -> " + " / ".join(f"{capital(m0, m1, e):+.3f}" for e in (0.5, 1, 1.6)) + " Md€")
    for kappa in (0.0, 0.5, 1.0):
        # IS à 28 % : base déclarée perdue 1 à 1,5 % par point × 3 points × 322 Md€ (2027)
        db = np.array([0.03, 0.045]) * 322.0
        p(f"  IS à 28 %, coût réel du transfert de bénéfices κ = {kappa} : +{kappa*0.265*db[0]:.1f} à +{kappa*0.265*db[1]:.1f} Md€")
    p("")
    p("[PFU] baisse à 25 % ; π = part de la réaction qui échappe définitivement à l'impôt")
    for e in (0.65, 0.77, 1.0):
        for pi in (0.0, 0.5, 1.0):
            r = [pfu(0.25, e, pi, m) for m in MU1]
            p(f"  e = {e} ; π = {pi} : ΔPS = " + " / ".join(f"{u[0]:+.2f}" for u in r)
              + f" Md€ (μ−1 = 0,16 / 0,38 / 0,60) ; recette perdue {r[0][1]:.1f} Md€ ; réaction {r[0][2]:+.1f} Md€")
    (OUT / "perte_seche_autres.txt").write_text("\n".join(L) + "\n", encoding="utf-8")
    print("\n".join(L))
