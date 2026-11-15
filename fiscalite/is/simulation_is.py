"""Simulation simple pour la note IS : déduction immédiate des équipements, taux, taux réduit.

Lancer depuis fiscalite/is/ : python3 simulation_is.py  ->  sorties/simulation_is.txt
Chiffres d'entrée : donnees/is_chiffres.csv (sources et statut) ; hypothèses en tête de fichier.

Logique. Un équipement acheté I est aujourd'hui déduit sur sept ans (linéaire, ou dégressif pour les
biens éligibles). Le déduire en une fois ne change pas le total déduit, seulement sa date : l'État perd
de la recette l'année de l'achat et la récupère les années suivantes. Coût de l'année t pour l'État =
taux x part imposable x (déduction nouvelle - déduction ancienne), sommé sur les millésimes achetés depuis
la réforme. Les millésimes antérieurs gardent leur plan d'amortissement.
"""
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
OUT = HERE / "sorties"
OUT.mkdir(exist_ok=True)

# ---------------------------------------------------------------- hypothèses
TAU = 0.25               # taux normal (droit permanent, sans contribution exceptionnelle)
I_2025 = 75.5 + 8.5      # autres machines et équipements + TIC des SNF, 2025 (Insee 8.212), Md€
G = 0.03                 # croissance nominale de l'investissement
AN1 = 2027               # première année de la réforme
I1 = I_2025 * (1 + G) ** (AN1 - 2025)
PARTS = (0.60, 0.75, 0.90)   # part de cet investissement faite par des sociétés imposables (non mesurée)
R = 0.05                 # taux d'actualisation nominal des entreprises et de l'État
DUREE = 7                # durée d'amortissement type des machines
H = 40                   # horizon de simulation (années)

BASE_NORMALE = 251.0     # bénéfice imposé aux taux normaux, 2022 (DGFiP Statistiques n° 21), Md€
BASE_REDUITE = 27.0      # bénéfice imposé à 15 %, 2022, Md€
CROISS_BASE = (1.06) ** 0  # on garde la base 2022, faute de ventilation plus récente (ordre de grandeur)
# Élargissement de l'assiette (Md€ par an)
ELARG = {"Fin du taux réduit de 15 % (statique 2022 ; 2,2 officiel en 2019)": 2.7,
         "CIR apprécié au niveau du groupe (CPO, 2025)": 0.57,
         "Fin des exonérations zonées hors outre-mer (CPO, 2025)": 0.52,
         "Boîte à brevets : avantage réduit de moitié, taux de 17,5 % (hypothèse : base stable)": 0.6}
# Version prudente : taux réduit au chiffre officiel de 2019 (2,2) et brevets à 0,2 (fuite de la base)
ELARG_PRUDENT = 2.2 + 0.57 + 0.52 + 0.2


def plan(regime):
    """Fractions du coût déduites les années 0, 1, ... (demi-année la première année)."""
    if regime == "lineaire":
        d = [0.5 / DUREE] + [1 / DUREE] * (DUREE - 1) + [0.5 / DUREE]
    elif regime == "degressif":
        taux = 2.25 / DUREE
        reste, d = 1.0, []
        for k in range(DUREE + 1):
            ann_rest = DUREE - k + 0.5          # années restantes, demi-année comprise
            lin = reste / ann_rest if ann_rest > 0 else reste
            dk = (0.5 if k == 0 else 1.0) * max(taux * reste, lin)
            dk = min(dk, reste)
            d.append(dk)
            reste -= dk
        d[-1] += reste
    else:
        raise ValueError(regime)
    return np.array(d)


def plan_bonus(regime, b):
    """Déduction immédiate d'une fraction b, le reste amorti selon le régime ancien."""
    return b * np.eye(1, DUREE + 1, 0).ravel() + (1 - b) * plan(regime)


def z(d, r=R):
    """Valeur actuelle des déductions pour 1 € d'investissement."""
    return float(sum(dk / (1 + r) ** k for k, dk in enumerate(d)))


def chemin(regime, bonus_par_annee, part):
    """Coût annuel pour l'État (Md€), années 1..H ; bonus_par_annee(t) = fraction déduite tout de suite."""
    ancien = plan(regime)
    cout = np.zeros(H + DUREE + 2)
    for t in range(H):
        I = I1 * (1 + G) ** t
        nouveau = plan_bonus(regime, bonus_par_annee(t))
        cout[t:t + DUREE + 1] += TAU * part * I * (nouveau - ancien)
    return cout[:H]


def cout_vrai(regime, b, part):
    """Coût actualisé par millésime (Md€ de l'année 1) : taux x part x I x (z nouveau - z ancien)."""
    return TAU * part * I1 * (z(plan_bonus(regime, b)) - z(plan(regime)))


def recette_taux(points, semi_elast):
    """Recette d'une hausse du taux normal de `points`, base 2022 ; semi-élasticité en % de base par point."""
    base = BASE_NORMALE * (1 - semi_elast / 100 * points)
    return (TAU + points / 100) * base - TAU * BASE_NORMALE


def cout_usage(zv, tau=TAU):
    """Coût d'usage relatif (r + delta) x (1 - tau z) / (1 - tau), divisé par (r + delta)."""
    return (1 - tau * zv) / (1 - tau)


def petite_societe(benefice, invest):
    """Perte annuelle due à la fin du taux réduit et gain actualisé de la déduction immédiate (par an)."""
    perte = 0.10 * min(benefice, 42_500)
    gain = TAU * invest * (1 - z(plan("lineaire")))
    return perte, gain


if __name__ == "__main__":
    L = []
    p = L.append
    zl, zd = z(plan("lineaire")), z(plan("degressif"))
    p(f"Investissement éligible année 1 ({AN1}) : {I1:.1f} Md€ (base 2025 {I_2025:.1f}, +{G:.0%}/an)")
    p(f"[Z] Valeur actuelle des déductions pour 100 € (r = {R:.0%}) : linéaire {100*zl:.1f}, "
      f"dégressif {100*zd:.1f}, 50 % immédiat + linéaire {100*z(plan_bonus('lineaire', .5)):.1f}, "
      f"déduction immédiate 100")
    for nom, zv in (("linéaire", zl), ("dégressif", zd)):
        p(f"[USAGE] Coût d'usage relatif {nom} : {cout_usage(zv):.4f} -> 1,0000 avec déduction immédiate "
          f"({100*(1/cout_usage(zv)-1):+.1f} %)")
    p("")
    p("[CHEMIN] Coût annuel pour l'État (Md€), part imposable 60 / 75 / 90 %")
    variantes = {"A : déduction immédiate dès l'année 1": lambda t: 1.0,
                 "B : 50 % immédiat, reste amorti (permanent)": lambda t: 0.5,
                 "C : 50 % les années 1 à 3, 100 % ensuite": lambda t: 0.5 if t < 3 else 1.0,
                 "D : 50 % les années 1 à 6, 100 % ensuite": lambda t: 0.5 if t < 6 else 1.0}
    res = {}
    for nom, f in variantes.items():
        for reg in ("lineaire", "degressif"):
            ch = {s: chemin(reg, f, s) for s in PARTS}
            res[(nom, reg)] = ch
            c = ch[0.75]
            p(f"  {nom} [{reg}] an1 {c[0]:.1f} an2 {c[1]:.1f} an3 {c[2]:.1f} an4 {c[3]:.1f} an5 {c[4]:.1f} "
              f"an10 {c[9]:.1f} an20 {c[19]:.1f} | an1 (60-90 %) {ch[0.6][0]:.1f}-{ch[0.9][0]:.1f} "
              f"| an10 (60-90 %) {ch[0.6][9]:.1f}-{ch[0.9][9]:.1f} | cumul 5 ans {c[:5].sum():.1f}")
    p("")
    for reg in ("lineaire", "degressif"):
        p(f"[VRAI] Coût actualisé par millésime, déduction immédiate [{reg}] : "
          + " / ".join(f"{cout_vrai(reg, 1.0, s):.2f}" for s in PARTS) + " Md€ (parts 60/75/90 %) ; "
          f"en points de taux : {cout_vrai(reg, 1.0, .75)/(BASE_NORMALE/100):.2f}")
    p("")
    p("[TAUX] Recette d'une hausse du taux normal (base 2022 des taux normaux, 251 Md€)")
    for pts in (1, 3):
        p(f"  +{pts} pt : " + " ; ".join(f"semi-élasticité {e} -> {recette_taux(pts, e):.1f}"
                                      for e in (0, 0.5, 1.0, 1.5)) + " Md€")
    p("")
    tot = sum(ELARG.values())
    p("[ELARG] Élargissement de l'assiette (Md€/an, statique)")
    for k, v in ELARG.items():
        p(f"  {k} : {v:.2f}")
    p(f"  Total : {tot:.1f} Md€, soit {tot/(BASE_NORMALE/100):.1f} point de taux normal")
    p("")
    for TOT in (tot, ELARG_PRUDENT):
      p(f"[SOLDE] Solde cumulé (élargissement de {TOT:.1f} Md€ croissant à 3 %/an moins coût), part 75 %, Md€")
      for nom in variantes:
        for reg in ("lineaire", "degressif"):
            c = res[(nom, reg)][0.75]
            e = TOT * (1 + G) ** np.arange(H)
            cum = np.cumsum(e - c)
            bas = cum.min()
            ret = next((t + 1 for t in range(int(np.argmin(cum)), H) if cum[t] >= 0), None)
            p(f"  {nom} [{reg}] : creux {bas:.1f} Md€ (année {int(np.argmin(cum))+1}), "
              f"solde annuel positif dès l'année {next(t+1 for t in range(H) if e[t] >= c[t])}, "
              f"cumul repasse à zéro année {ret}")
    p("")
    p("[PME] Petite société : perte due à la fin du taux réduit / gain actualisé de la déduction immédiate (€/an)")
    for b, i in ((42_500, 0), (42_500, 20_000), (100_000, 50_000), (100_000, 150_000), (30_000, 10_000)):
        perte, gain = petite_societe(b, i)
        p(f"  bénéfice {b:>7,} €, investissement {i:>7,} €/an : perte {perte:>6,.0f} ; gain {gain:>6,.0f} ; "
          f"avance de trésorerie la 1re année {TAU*i*(1-plan('lineaire')[0]):>6,.0f}".replace(",", " "))
    perte, _ = petite_societe(42_500, 0)
    p(f"  investissement annuel qui compense la perte maximale : {perte/(TAU*(1-zl)):,.0f} €".replace(",", " "))
    p(f"  taux cumulé IS + PFU sur un bénéfice distribué de 42 500 € : {100*(0.15+0.85*0.314):.1f} % -> "
      f"{100*(0.25+0.75*0.314):.1f} %")
    (OUT / "simulation_is.txt").write_text("\n".join(L) + "\n")
    print("\n".join(L))
