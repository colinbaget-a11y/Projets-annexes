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

# Bénéfices imposables de l'exercice 2025 (base 2025, décision 5 du 17/11/2026) : DGFiP Statistiques n° 51
# (septembre 2026, données provisoires extrapolées des déclarations connues à mi-2026), graphique 2 et son fichier xlsx.
# Avant le 17/11/2026, le calibrage partait des bénéfices de 2022 (DGFiP n° 21 : 251 Md€ aux taux normaux, 27 à 15 %)
# portés en 2027 par la croissance du bénéfice fiscal (x 1,061) ; les chiffres de 2025 montrent une base au taux normal
# presque identique (256,8 contre 256,0 attendus) mais une base à 15 % plus forte (30,6 contre 27,5 attendus).
BASE_NORMALE = 256.8     # bénéfice imposable à 25 %, exercice 2025 (DGFiP n° 51), Md€ (2022 : 251,0 à 25-27,5 %)
BASE_REDUITE = 30.6      # bénéfice imposable à 15 %, exercice 2025 (DGFiP n° 51), Md€ (2022 : 26,6 ; 2024 : 30,0)
# Croissance du bénéfice fiscal (Évaluation des voies et moyens, tome I, PLF 2025 et PLF 2026) : +1 % en 2023,
# 0 % en 2024, +1 % en 2025 (sert seulement de contrôle : les bases ci-dessus sont celles de 2025) ; +2 % par an en 2026
# et 2027 (hypothèse H7 : le PLF 2026 prévoyait +2,5 % pour 2026, prévision révisée à la baisse par le PLF 2027, dont le
# tome I n'est pas en ligne).
BFI = {2023: 0.01, 2024: 0.00, 2025: 0.01, 2026: 0.02, 2027: 0.02}
A25 = float(np.prod([1 + BFI[a] for a in range(2026, AN1 + 1)]))   # montants de 2025 portés en 2027 (x 1,040)
AB = A25                                                           # bases de bénéfices (2025) portées en 2027
# Élargissement de l'assiette (Md€ par an)
ELARG = {"Fin du taux réduit de 15 % (statique 2025, porté en 2027)": 0.10 * BASE_REDUITE * AB,
         "CIR apprécié au niveau du groupe (CPO, 2025)": 0.57 * A25,
         "Fin des exonérations zonées hors outre-mer, IR et IS (CPO, 2025)": 0.52 * A25,
         "Boîte à brevets : avantage réduit de moitié, taux de 17,5 % (hypothèse : base stable)": 0.6 * A25}
# Version prudente : taux réduit au chiffre officiel de 2019 (2,2 Md€ pour un écart de 13 points, soit
# 1,7 Md€ pour 10 points), porté en 2027 à 3 % par an (2,15 Md€ : 68 % du rendement statique sur la base de 2025,
# 75 % sur l'ancienne base de 2022 ; marge pour les réactions non chiffrées, passage à l'IR ou rémunération en salaire),
# et brevets à 0,2 (fuite de la base)
ELARG_PRUDENT = 1.7 * (1 + G) ** (AN1 - 2019) + (0.57 + 0.52 + 0.2) * A25


def plan(regime):
    """Fractions du coût déduites les années 0, 1, ... (demi-année la première année)."""
    if regime == "lineaire":
        d = [0.5 / DUREE] + [1 / DUREE] * (DUREE - 1) + [0.5 / DUREE]
    elif regime == "degressif":
        # BOI-BIC-AMT-20-20-30, § 260 : l'exercice d'acquisition compte pour une année entière dans le calcul des
        # années restant à courir ; le plan s'achève au 7e exercice (correction du 16/11/2026, l'ancien code
        # l'étalait sur 8 exercices).
        taux = 2.25 / DUREE
        reste, d = 1.0, []
        for k in range(DUREE):
            ann_rest = DUREE - k
            deg = taux * reste * (0.5 if k == 0 else 1.0)
            dk = deg if k == 0 else max(deg, reste / ann_rest)
            dk = reste if k == DUREE - 1 else min(dk, reste)
            d.append(dk)
            reste -= dk
        d.append(0.0)
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


def recette_taux(points, semi_elast, base0=None):
    """Recette (Md€ de 2027) d'une hausse du taux normal de `points` ; semi-élasticité en % de base par point."""
    b0 = BASE_NORMALE * AB if base0 is None else base0
    base = b0 * (1 - semi_elast / 100 * points)
    return (TAU + points / 100) * base - TAU * b0


def cout_usage(zv, tau=TAU):
    """Coût d'usage relatif (r + delta) x (1 - tau z) / (1 - tau), divisé par (r + delta)."""
    return (1 - tau * zv) / (1 - tau)


def petite_societe(benefice, invest):
    """Perte annuelle due à la fin du taux réduit et gain actualisé de la déduction immédiate (par an)."""
    perte = 0.10 * min(benefice, 42_500)
    gain = TAU * invest * (1 - z(plan("lineaire")))
    return perte, gain


R_ETAT = 0.0325          # taux d'emprunt de l'État (hypothèse, 3 à 3,5 %)
PIB_2027 = 2991.0 * (1 + G) ** 2   # PIB nominal 2027, Md€ (Insee 2025 : 2 991 Md€, porté à 3 % par an)
NICHES = ((0.57 + 0.52 + 0.2) * A25, (0.57 + 0.52 + 0.6) * A25)   # CIR groupe, zones, brevets (bas, haut), 2027
REDUIT = (1.7 * (1 + G) ** (AN1 - 2019), 0.10 * BASE_REDUITE * AB)   # fin du taux réduit (bas, haut), 2027
POINT = (BASE_NORMALE + BASE_REDUITE) * AB / 100                     # un point de taux normal en 2027, taux réduit supprimé


def scenario(regime, bonus, financement, baisse_pts=0.0, baisse_des=None, r=R_ETAT, h=H):
    """Solde budgétaire année par année (Md€) et dette cumulée avec intérêts.
    bonus(t) : fraction déduite tout de suite ; financement : Md€/an en année 1, croissant avec G ;
    baisse_pts : baisse du taux normal (points) à partir de l'année baisse_des (rendue sur la base de 2025 portée en 2027,
    croissant avec G, et le coût de la déduction est réduit dans la proportion (TAU - baisse)/TAU)."""
    cout = chemin(regime, bonus, 0.75)[:h]
    cr = (1 + G) ** np.arange(h)
    rec = financement * cr
    if baisse_des is not None:
        on = np.arange(h) >= baisse_des
        rec = rec - on * baisse_pts * POINT * cr
        cout = np.where(on, cout * (TAU - baisse_pts / 100) / TAU, cout)
    solde = rec - cout
    dette = np.zeros(h)
    d = 0.0
    for t in range(h):
        d = d * (1 + r) - solde[t]
        dette[t] = d
    return solde, dette


def resume_scenario(nom, regime, bonus, fin, **kw):
    solde, dette = scenario(regime, bonus, fin, **kw)
    pib = PIB_2027 * (1 + G) ** np.arange(len(dette))
    pic = dette.max()
    ret = next((t + 1 for t in range(int(np.argmax(dette)), len(dette)) if dette[t] <= 0), None)
    return (f"  {nom} [{regime}] : dette max {pic:.1f} Md€ (an {int(np.argmax(dette))+1}), "
            f"remboursée an {ret} ; solde an 10 {solde[9]:+.1f}, an 20 {solde[19]:+.1f} Md€ ; "
            f"dette an 30 {dette[29]:+.1f} Md€ ({100*dette[29]/pib[29]:+.2f} pt de PIB)")


def cout_vrai_r(regime, b, part, r):
    return TAU * part * I1 * (z(plan_bonus(regime, b), r) - z(plan(regime), r))


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
          f"en points de taux : {cout_vrai(reg, 1.0, .75)/POINT:.2f}")
    p("")
    p(f"[TAUX] Recette d'une hausse du taux normal (base 2025 au taux normal, {BASE_NORMALE:.1f} Md€, portée en 2027)")
    for pts in (1, 3):
        p(f"  +{pts} pt : " + " ; ".join(f"semi-élasticité {e} -> {recette_taux(pts, e):.1f}"
                                      for e in (0, 0.5, 1.0, 1.5)) + " Md€")
    p("")
    tot = sum(ELARG.values())
    p("[ELARG] Élargissement de l'assiette (Md€/an, statique)")
    for k, v in ELARG.items():
        p(f"  {k} : {v:.2f}")
    p(f"  Total : {tot:.1f} Md€ (prudent {ELARG_PRUDENT:.1f}), soit {tot/POINT:.1f} point de taux normal ; un point = {POINT:.2f} Md€ en 2027")
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
    p(f"  taux cumulé IS + PFU sur un bénéfice distribué de 42 500 € : {100*(0.15+0.85*0.314):.2f} % -> "
      f"{100*(0.25+0.75*0.314):.2f} %")

    p("")
    p(f"[VRAI_ETAT] Coût par millésime actualisé au taux de l'État ({R_ETAT:.2%}), déduction totale : "
      + " ; ".join(f"{reg} " + " / ".join(f"{cout_vrai_r(reg, 1.0, s_, R_ETAT):.2f}" for s_ in PARTS)
                   for reg in ("lineaire", "degressif")) + " Md€ (parts 60/75/90 %)")
    p(f"[SCEN] Dette cumulée avec intérêts à {R_ETAT:.2%} (part imposable 75 %, horizon 30 ans)")
    pal = lambda t: 0.5 if t < 6 else 1.0
    for reg in ("lineaire", "degressif"):
        for nom, bonus, fin, kw in (
                ("S1 50 % permanent, niches", lambda t: 0.5, NICHES, {}),
                ("S2 50 % puis 100 % en an 7, niches", pal, NICHES, {}),
                ("S3 50 % puis 100 % en an 7, niches + taux réduit", pal, tuple(a + b for a, b in zip(NICHES, REDUIT)), {}),
                ("S4 100 % dès l'an 1, niches + taux réduit", lambda t: 1.0, tuple(a + b for a, b in zip(NICHES, REDUIT)), {})):
            for f in fin:
                p(resume_scenario(f"{nom} ({f:.1f})", reg, bonus, f, **kw))
    # baisse de taux que l'excédent permet une fois la dette remboursée (scénario S3)
    for reg in ("lineaire", "degressif"):
        for f in tuple(a + b for a, b in zip(NICHES, REDUIT)):
            solde, dette = scenario(reg, pal, f)
            cr_ = (1 + G) ** np.arange(len(solde))
            pts = solde / (POINT * cr_)
            p(f"[POINTS] S3 [{reg}] financement {f:.1f} : excédent en points de taux normal, an 15 {pts[14]:.2f},"
              f" an 20 {pts[19]:.2f}, an 30 {pts[29]:.2f}")
    # petite société pendant la phase à 50 % (2027-2032)
    perte = 4250.0
    for i in (20_000, 50_000):
        av = TAU * i * (plan_bonus("lineaire", 0.5)[0] - plan("lineaire")[0])
        p(f"[PME50] déduction de 50 % : avance la 1re année pour {i:,} € d'équipements {av:,.0f} € ;".replace(",", " ")
          + f" investissement annuel qui compense la perte maximale {perte/(TAU*(z(plan_bonus('lineaire', .5))-z(plan('lineaire')))):,.0f} €".replace(",", " "))
    # gain de PIB de long terme (ordre de grandeur)
    K, DEP, PIB25 = 541.0, 0.14, 2991.0      # stock éligible fin 2025 (Insee 8.212 : 512,1 + 28,8), dépréciation ; PIB Insee
    sk = (0.05 + DEP) * K / PIB25
    for nom, dc in (("100 %", (0.034, 0.048)), ("50 %", (0.017, 0.024))):
        lo = sk * 0.5 * dc[0] * 0.75
        hi = sk * 1.6 * dc[1] * 0.75
        mid = sk * 1.0 * sum(dc) / 2 * 0.75
        p(f"[PIB] {nom} : part du revenu de ce capital {100*sk:.1f} % du PIB ; gain de long terme "
          f"{100*lo:.2f} à {100*hi:.2f} % du PIB (central {100*mid:.2f} %, soit {mid*PIB25:.1f} Md€)")
    (OUT / "simulation_is.txt").write_text("\n".join(L) + "\n")
    print("\n".join(L))
