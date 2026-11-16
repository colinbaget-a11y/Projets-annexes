"""Bloc IR-CSG v3 (note8p, révision du 18/11/2026) : noyau du modèle.

Réutilise ircsg_modele.py (v2, inchangé) et synthese/modele_purs.py (foyers « purs » calés sur l'IRCOM 2024 portés en
2025). Ce que la v3 change :
1. Familles : les enfants des couples d'actifs et des parents isolés sont répartis en familles de 1, 2, 3 et 4 enfants
   selon la répartition des familles avec enfants de moins de 25 ans du recensement 2022 (Insee, « Familles selon le
   nombre d'enfants âgés de moins de 25 ans en 2022 », publié le 26/06/2025 : 1 enfant 21,9 %, 2 : 19,4 %, 3 : 6,6 %,
   4 ou plus 2,4 % des familles, soit 43,5 / 38,6 / 13,1 / 4,8 % des familles avec enfants) [E] ; même répartition pour
   les couples et les parents isolés, quel que soit le revenu, « 4 ou plus » compté 4 [H]. Le total d'enfants (18,0 M)
   et le nombre de parents isolés (1,97 M, cases 0BT) sont gardés ; la part des couples d'actifs avec enfants s'en déduit.
   Charge actuelle des nouveaux types : celle du type d'origine, corrigée de l'écart de quotient familial calculé par
   ircsg3_droit.charge (droit 2025), puis recalée point par point pour garder la charge observée de chaque point.
2. Frais professionnels : le forfait de 10 % disparaît, les frais réels restent déductibles (choix de l'auteur) : 35,2 Md€
   déclarés pour les revenus 2024 (cases 1AK à 1DK, donnees/ir_2042_cases_revenus2024.csv), portés en 2025 (+2,3 %),
   répartis au prorata des revenus d'activité des actifs [H : la répartition n'est pas publiée] ; ajoutés aux versements
   d'épargne retraite déductibles (DED_PER).
3. Barèmes continus : taux marginal affine par morceaux entre des points de référence (revenu après cotisations par
   adulte), impôt = intégrale du taux marginal ; au-delà du dernier point, taux constant (plafond).
4. Perte sèche : cadre standard (décision de l'auteur du 18/11/2026, « parcimonie méthodologique ») : chaque individu
   réagit à sa rémunération nette, tous les prélèvements pleinement pris en compte aujourd'hui comme demain ; un jeu
   d'élasticités central (méthode v2), bornes basse et haute sur les seules élasticités. Plus aucune hypothèse de
   perception partielle.
"""
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import ircsg_modele as R  # noqa: E402
import ircsg3_droit as DR  # noqa: E402

M, U = R.M, R.U
SMIC_BRUT = U.SMIC                                   # 21 622 € brut par an (2025)
SMIC_Z = 19176.48                                    # revenu après cotisations au Smic (OpenFisca, cas jeune_smic)
SORTIES = R.SORTIES

# ------------------------------------------------------------------ 2. frais réels et épargne retraite
DED_PER0 = M.DED_PER.copy()
FR_TOTAL = (26539791171.0 + 8642079803.0) * M.G_ACT  # 1AK + 1BK (déclarants 1 et 2) ; 1CK, 1DK négligeables
FR = M.ACTIV_A * FR_TOTAL / (M.W_A * M.ACTIV_A).sum()
M.DED_PER = DED_PER0 + FR                            # assiette du nouvel impôt : z − épargne retraite − frais réels

# ------------------------------------------------------------------ 1. familles de 1 à 4 enfants
PK = {1: 0.435, 2: 0.386, 3: 0.131, 4: 0.048}
MOY = sum(k * p for k, p in PK.items())
TYPES0, CURT0 = list(M.TYPES), dict(M.CURT)
ENF_PI = M.CASES_T * MOY
F_C = (M.ENFANTS - ENF_PI) / (MOY * (M.W_A * M.S).sum())        # part des couples d'actifs avec enfants


def _u(parts, k, isole):
    zn = M.ZNA
    ad = [("A", sh * zn, M.R_A) for sh in parts]
    return DR.charge(ad, k, isole)["total"]


def _types_familles():
    T, C = [], {}
    for nom, g, fam, w, parts, kids in TYPES0:
        if g == "R" or kids == 0 and not nom.startswith("couple0"):
            T.append((nom, g, fam, w, parts, kids))
            C[nom] = CURT0[nom]
            continue
        if nom.startswith("couple0"):
            s = float(nom.rsplit("_", 1)[1])
            base = [t for t in TYPES0 if t[0] == f"couple0_{s}"][0][3] + [t for t in TYPES0 if t[0] == f"couple2_{s}"][0][3]
            T.append((nom, g, fam, base * (1 - F_C), parts, 0))
            C[nom] = CURT0[nom]
            continue
        if nom.startswith("couple2"):
            s = float(nom.rsplit("_", 1)[1])
            base = [t for t in TYPES0 if t[0] == f"couple0_{s}"][0][3] + w
            us = {k: _u(parts, k, False) for k in PK}
            ub = sum(PK[k] * us[k] for k in PK)
            for k in PK:
                n_ = f"couple{k}e_{s}"
                T.append((n_, g, "couples2", base * F_C * PK[k], parts, k))
                C[n_] = np.clip(CURT0[nom] + us[k] - ub, 0, None)
        elif nom == "parent_isole":
            us = {k: _u(parts, k, True) for k in PK}
            ub = sum(PK[k] * us[k] for k in PK)
            for k in PK:
                n_ = f"parent_isole_{k}e"
                T.append((n_, g, "parents_isoles", w * PK[k], parts, k))
                C[n_] = np.clip(CURT0[nom] + us[k] - ub, 0, None)
    # recalage : la charge observée de chaque point (actifs) est gardée
    tot0 = sum(w * CURT0[n] for n, g, _, w, _, _ in TYPES0 if g == "A")
    tot1 = sum(w * C[n] for n, g, _, w, _, _ in T if g == "A")
    k_ = np.where(tot1 > 0, tot0 / np.where(tot1 > 0, tot1, 1), 1.0)
    for n, g, *_ in T:
        if g == "A":
            C[n] = C[n] * k_
    return T, C


M.TYPES, M.CURT = _types_familles()
M.PTR0 = M._ptr0()
ENFANTS_MODELE = sum((w * kids).sum() for n, g, f, w, p, kids in M.TYPES)
CIBLE = R.CIBLE                         # IR barème + CSG + CRDS + CEHR du barème + avantages invalidité maintenus


# ------------------------------------------------------------------ 3. barèmes continus
def continu(points, taux):
    """Taux marginal affine par morceaux entre (points[i], taux[i]) ; constant au-delà du dernier point.
    Impôt = intégrale exacte (trapèzes)."""
    xs, ts = np.asarray(points, float), np.asarray(taux, float)
    cum = np.r_[0.0, np.cumsum(np.diff(xs) * (ts[1:] + ts[:-1]) / 2)]

    def tm(z):
        return np.interp(np.asarray(z, float), xs, ts)

    def T(z):
        z = np.clip(np.asarray(z, float), 0, None)
        i = np.clip(np.searchsorted(xs, z, side="right") - 1, 0, len(xs) - 1)
        x0, t0 = xs[i], ts[i]
        t1 = np.where(i + 1 < len(xs), ts[np.minimum(i + 1, len(xs) - 1)], t0)
        x1 = np.where(i + 1 < len(xs), xs[np.minimum(i + 1, len(xs) - 1)], x0 + 1.0)
        pente = (t1 - t0) / np.maximum(x1 - x0, 1e-9)
        d = z - x0
        return cum[i] + t0 * d + 0.5 * pente * np.where(i + 1 < len(xs), d, 0.0) ** 2
    return tm, T


def options(fe=6000.0):
    return R.options(fe=fe)


def recette(sched, o):
    return R.recette(sched, o)


def cale(fabrique, o, cible, lo=-0.15, hi=0.20):
    """fabrique(d) -> barème ; trouve d tel que la recette égale la cible."""
    for _ in range(45):
        m = (lo + hi) / 2
        lo, hi = (m, hi) if recette(fabrique(m), o) < cible else (lo, m)
    return (lo + hi) / 2


def evalue(sched, o, jeu="central", repart=False):
    """Perte sèche (méthode v2) dans le cadre standard : réaction au taux net complet d'aujourd'hui et de demain."""
    return R.evalue(sched, o, jeu=jeu, vue=1.0, vue_ext=1.0, repart=repart)


# ------------------------------------------------------------------ cas-types (bases OpenFisca)
def impot_z(sched, o, zs, kids=0):
    """Nouvel impôt d'un foyer de revenus après cotisations zs (sans frais réels ni épargne retraite)."""
    zs = [np.atleast_1d(np.asarray(z, float)) for z in zs]
    return R.impot_adultes(*sched, o, zs, zs, [0 * z for z in zs], kids)[0]


def cas(sched, o, cle):
    return R.cas_type(sched, o, cle)
