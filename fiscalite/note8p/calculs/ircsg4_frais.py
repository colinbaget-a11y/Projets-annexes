"""Bloc IR-CSG v4 : frais professionnels des salariés. Que deviennent les frais réels déclarés si le forfait de 10 %
disparaît, et que coûte un petit forfait de droit commun ?

Modèle de frais [H, calé sur des données publiques] : chaque salarié a des frais F = trajet domicile-travail + repas.
- Distance aller (km) : log-normale de médiane 8 km (Insee Première n° 1948, mai 2023 : « au moins 8 km pour l'ensemble
  des travailleurs » en 2019) [E], croissant modérément avec le salaire (élasticité 0,2 [H] ; les cadres font les plus
  longs trajets, même source), dispersion σ calée ; plafond fiscal de 40 km sauf justification.
- 74 % des actifs vont travailler en voiture (Insee Première n° 1835, janvier 2021, données 2017) [E] ; coût au barème
  kilométrique 5 CV des revenus 2024 (d × 0,636 jusqu'à 5 000 km ; d × 0,357 + 1 395 jusqu'à 20 000 km ; d × 0,427
  au-delà ; legifiscal.fr, reprise de la brochure 2025) [E] ; les autres : 300 € par an (reste à charge de
  l'abonnement après la prise en charge de 50 % par l'employeur) [H].
- 205 jours travaillés par an à temps plein (congés, télétravail partiel) [H], au prorata pour les bas salaires
  (temps partiel : plein temps supposé atteint à 16 000 € net imposable) [H].
- Repas : 25 % des salariés déduisent 5 € par jour (frais supplémentaires de repas : prix payé − 5,35 €, au plus
  15,35 € en 2024) [E pour les paramètres, H pour la part].
- Un salarié déclare ses frais réels si le gain d'impôt dépasse un seuil gt (coût de conformité, justificatifs) [H calé].
Calage : la dispersion σ et le seuil gt sont choisis pour reproduire les frais réels déclarés pour les revenus 2024 :
5,86 M de déclarants (cases 1AK à 1DK), 35,3 Md€ (donnees/ir_2042_cases_revenus2024.csv), portés en 2025 (+2,3 %).
"""
import numpy as np

KM = (0.636, 0.357, 1395.0, 0.427)
CIBLE_N, CIBLE_MD = 4274102 + 1543451 + 42556 + 5048, (26539791171 + 8642079803 + 111571774 + 12513328) * 1.023 / 1e9
FORFAIT = (0.10, 509.0, 14555.0)      # droit des revenus 2025 (ircsg3_droit.ABATPRO)
GRID = np.exp(np.linspace(np.log(500.0), np.log(700000.0), 90))
NDRAW = 6000
_rng = np.random.default_rng(20261119)
_Z, _U1, _U2 = _rng.standard_normal(NDRAW), _rng.random(NDRAW), _rng.random(NDRAW)


def cout_km(km):
    a, b, c, d = KM
    return np.where(km <= 5000, km * a, np.where(km <= 20000, km * b + c, km * d))


def frais(w, sig, med=8.0, beta=0.2, car=0.74, days=205.0, meal_p=0.25, meal=1025.0, wmed=24000.0):
    pt = np.minimum(1.0, w / 16000.0)
    d = np.minimum(med * (w / wmed) ** beta * np.exp(sig * _Z), 40.0)
    return np.where(_U1 < car, cout_km(2 * d * days * pt), 300.0 * pt) + (_U2 < meal_p) * meal * pt


def tau_actuel(r):
    """Taux marginal de l'IR d'une personne seule sur son revenu imposable r (barème 2025, hors décote)."""
    return np.select([r < 11600, r < 29579, r < 84577, r < 181917], [0.0, 0.11, 0.30, 0.41], 0.45)


def regle(w, F, option, sig=None, tau_new=None, gt=120.0):
    """Déduction et décision de déclarer les frais réels pour un salarié de salaire net imposable w.
    option : ("actuel",) ; ("suppression",) ; ("fixe", K) ; ("pct", p, plafond)."""
    nom = option[0]
    if nom == "actuel":
        t, lo, hi = FORFAIT
        fo = min(max(t * w, lo), hi, w)
        tau = tau_actuel(w - fo)
    elif nom == "suppression":
        fo, tau = 0.0, tau_new(w)
    elif nom == "fixe":
        fo, tau = min(option[1], w), tau_new(w)
    elif nom == "franchise":           # pas de forfait ; frais réels déductibles au-delà d'une franchise
        fo, tau = 0.0, tau_new(w)
        dec = (F - option[1]) * tau > gt
        return np.where(dec, F - option[1], 0.0), dec, fo
    else:
        fo, tau = min(option[1] * w, option[2]), tau_new(w)
    dec = (F - fo) * tau > gt
    return np.where(dec, F, fo), dec, fo


def profils(option, sig, gt, tau_new=None):
    """Sur la grille de salaires : déduction moyenne, part de déclarants, frais réels moyens déclarés."""
    D, P, FR = [], [], []
    for w in GRID:
        F = frais(w, sig)
        d, dec, fo = regle(w, F, option, sig, tau_new, gt)
        D.append(d.mean())
        P.append(dec.mean())
        FR.append((F * dec).mean())
    return np.array(D), np.array(P), np.array(FR)


def agrege(poids, w, option, sig, gt, tau_new=None):
    D, P, FR = profils(option, sig, gt, tau_new)
    i = lambda a: np.interp(w, GRID, a)  # noqa: E731
    return dict(deduction_Md=float((poids * i(D)).sum() / 1e9), declarants_M=float((poids * i(P)).sum() / 1e6),
                frais_reels_Md=float((poids * i(FR)).sum() / 1e9), forfait_Md=float((poids * (i(D) - i(FR))).sum() / 1e9))


def calage(poids, w):
    """σ et gt qui reproduisent le nombre de déclarants et le montant des frais réels (droit actuel)."""
    best = None
    for sig in np.arange(0.8, 1.61, 0.05):
        for gt in np.arange(40.0, 241.0, 10.0):
            a = agrege(poids, w, ("actuel",), sig, gt)
            err = ((a["declarants_M"] * 1e6 - CIBLE_N) / CIBLE_N) ** 2 + ((a["frais_reels_Md"] - CIBLE_MD) / CIBLE_MD) ** 2
            if best is None or err < best[0]:
                best = (err, sig, gt, a)
    return best
