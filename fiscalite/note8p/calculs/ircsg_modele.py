"""Bloc IR-CSG-CRDS (note8p) : noyau de calcul du nouvel impôt fusionné.

Réutilise sans les modifier synthese/modele_purs.py (foyers « purs » actifs / retraités calés sur l'IRCOM des revenus
2024 portés en 2025) et synthese/outils_ircsg.py. Ce qui change par rapport à la proposition de synthese/ (arbitrages
de l'auteur du 17/11/2026, note8p/CADRE.md) :
- barème en tranches (taux marginal constant par tranche), commun à tous les revenus, individuel ; aucune franchise
  d'activité, aucune exonération propre aux pensions ; pensions au droit commun ;
- franchise (déduction du revenu imposable) identique pour chaque enfant, imputée sur le parent au revenu le plus élevé
  (ce qui, avec un barème aux taux croissants, est aussi le choix qui minimise l'impôt du couple : règle « au choix ») ;
- étape intermédiaire possible : quotient conjugal plafonné (fam = "qcp") ;
- recette du périmètre : IR des revenus imposés au barème (hors PFU), CSG et CRDS des revenus d'activité et de
  remplacement (229,9 Md€ en 2025, modèle), plus la CEHR acquittée sur ces revenus (absorbée par le nouvel impôt),
  plus le coût des avantages maintenus pour l'invalidité et la dépendance ;
- perte sèche : méthode v2 (revue/methode_v2.md), recopiée ici pour pouvoir faire varier la perception de la CSG
  d'aujourd'hui sur les deux marges (intensive et extensive) ; le nouvel impôt est supposé entièrement perçu.
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

RACINE = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(RACINE / "synthese")]
import modele_purs as M  # noqa: E402
import outils_ircsg as U  # noqa: E402

ps = M.ps
SMIC = U.SMIC
SORTIES = RACINE / "note8p/sorties"
_IMPOT_ORIG = M.impot_adultes

# ------------------------------------------------------------------ périmètre et recette à tenir
R25 = M.RECETTES["2025"]
CIBLE_MODELE = M.CIBLE                                    # IR barème + CSG + CRDS du champ, 2025 (229,9 Md€)
CEHR_TOTAL_2025 = 1.39                                    # CEHR des revenus 2025 (pfu/README.md, DGFiP n° 43)
CDHR_TOTAL_2025 = 0.62                                    # CDHR des revenus 2025 (même source)
# avantages maintenus (invalidité, dépendance), coûts 2025 du PLF 2026, Voies et moyens t. II (fichier du dépôt) :
# demi-part des invalides 0,538 ; part ou demi-part des personnes à charge invalides 0,177 ; réduction pour frais de
# dépendance et d'hébergement en établissement 0,312
GARDES = {"demi_part_invalides": 0.538, "personnes_a_charge_invalides": 0.177, "dependance_etablissement": 0.312}


def cehr_bareme():
    """Part de la CEHR due sur les revenus du barème : CEHR théorique de chaque tranche de l'IRCOM (RFR moyen de la
    tranche, seuils de 250 000 / 500 000 € selon la part de couples du modèle) répartie au prorata de la part des
    revenus du barème dans le RFR (le reste vient des revenus au PFU, convention « mixte » du modèle), puis calée sur
    la recette observée (1,39 Md€). Hypothèse : la répartition des revenus au PFU entre tranches n'est pas publiée."""
    x = M.x
    mo = x.rfr * 1e9 / x.foyers
    s = pd.Series(M.S).groupby(M.TR.values).mean().reindex(x.tranche).values      # part de couples par tranche

    def c(r, seuil):
        return 0.03 * np.clip(np.minimum(r, 2 * seuil) - seuil, 0, None) + 0.04 * np.clip(r - 2 * seuil, 0, None)
    cehr = x.foyers * ((1 - s) * c(mo, 250e3) + s * c(mo, 500e3)) / 1e9
    part_bar = (1 - x.capital / x.rfr).clip(0, 1)
    k = CEHR_TOTAL_2025 / cehr.sum()
    return float((cehr * part_bar).sum() * k), float(cehr.sum())


CEHR_BAR, CEHR_THEO = cehr_bareme()
CIBLE = CIBLE_MODELE + CEHR_BAR + sum(GARDES.values())


# ------------------------------------------------------------------ barème en tranches
def bareme(seuils, taux):
    """Barème en tranches : taux[i] entre seuils[i] et seuils[i+1] (seuils[0] = 0)."""
    s, t = np.asarray(seuils, float), np.asarray(taux, float)
    cum = np.r_[0.0, np.cumsum(np.diff(s) * t[:-1])]

    def tm(z):
        z = np.asarray(z, float)
        return t[np.clip(np.searchsorted(s, z, side="right") - 1, 0, len(t) - 1)]

    def T(z):
        z = np.clip(np.asarray(z, float), 0, None)
        i = np.clip(np.searchsorted(s, z, side="right") - 1, 0, len(t) - 1)
        return cum[i] + t[i] * (z - s[i])
    return tm, T


def options(fe=6000.0, fam="franchise", qc_plafond=0.0, per=True):
    o = dict(M.OPT0)
    o.update(F=0.0, abat_pens=0.0, Fp=0.0, Fp_degressif=False, fam=fam, fe=fe, qc_plafond=qc_plafond, per=per)
    return o


def impot_adultes(tm, T, o, zs, ls, ps_, kids):
    """Impôt du foyer, taux marginal de chaque adulte, revenu imposé de chaque adulte (remplace M.impot_adultes).
    fam : "franchise" (impôt individuel, franchise fe par enfant chez le parent au revenu le plus élevé) ; "qcp"
    (même chose, puis quotient conjugal plafonné : l'impôt du couple ne peut pas être inférieur de plus de
    qc_plafond à la somme des impôts individuels... ni à l'impôt du revenu partagé par moitié) ; "quotient" :
    règles de synthese/ (réforme naïve)."""
    fam = o["fam"]
    if fam == "quotient":
        return _IMPOT_ORIG(tm, T, o, zs, ls, ps_, kids)
    tax = [np.clip(z, 0, None) for z in zs]
    if kids and o.get("fe", 0.0):
        haut = np.argmax(np.vstack(zs), axis=0) if len(zs) == 2 else np.zeros(len(np.atleast_1d(zs[0])), int)
        tax = [np.where(haut == k, np.clip(t - o["fe"] * kids, 0, None), t) for k, t in enumerate(tax)]
    ind = sum(T(t) for t in tax)
    mg = [tm(t) for t in tax]
    if fam == "qcp" and len(zs) == 2:
        y = tax[0] + tax[1]
        split = 2 * T(y / 2)
        imp = np.maximum(split, ind - o["qc_plafond"])
        lie = split > ind - o["qc_plafond"]            # le plafond ne mord pas : chacun paie au taux du couple
        mg = [np.where(lie, tm(y / 2), m_) for m_ in mg]
        return imp, mg, tax
    return ind, mg, tax


M.impot_adultes = impot_adultes        # M.recette, U.variations, U.distribution utilisent désormais cette règle


def recette(sched, o):
    return M.recette(*sched, o)


def cale_echelle(seuils, taux_fixes, libres, o, cible=None):
    """Ajoute le même nombre de points d aux taux d'indices `libres` pour tenir la recette ; renvoie les taux."""
    cible = CIBLE if cible is None else cible
    lo, hi = -0.25, 0.30
    t = np.asarray(taux_fixes, float)
    for _ in range(50):
        d = (lo + hi) / 2
        tt = t.copy()
        tt[libres] += d
        lo, hi = (d, hi) if recette(bareme(seuils, tt), o) < cible else (lo, d)
    tt = t.copy()
    tt[libres] += (lo + hi) / 2
    return tt


# ------------------------------------------------------------------ perte sèche (méthode v2) et effets réels
def evalue(sched, o, jeu="central", vue=1.0, kappa=0.0, theta=0.0, repart=False):
    """Variation par rapport à aujourd'hui (Md€ par an ; positif = perte sèche en plus) et effets réels.
    vue : part de la CSG-CRDS d'aujourd'hui (9,7 points) perçue comme l'IR, sur les deux marges ; le nouvel impôt est
    entièrement perçu. kappa : hausse du prélèvement implicite sur le salaire due à l'impôt plus lourd sur les
    pensions futures (par euro brut), theta : part perçue de kappa."""
    tm, T = sched
    eR, eD, eta = M.elast_v2(jeu)
    acc = dict(reel=0.0, ext=0.0, decl=0.0, dq_reel=0.0, dq_ext=0.0, emplois=0.0, dq_decl=0.0, ext_seuls=0.0,
               ext_couples=0.0, emplois_seuls=0.0, emplois_conjoints=0.0)
    res = {}
    for tnom, grp, fam_, w, parts, kids in M.TYPES:
        imp, mgs, _ = impot_adultes(tm, T, o, *M.adultes(grp, parts, o), kids)
        res[tnom] = (w, imp, M.CURT[tnom], grp, fam_)
        if grp == "R":
            continue
        single = len(parts) == 1
        for k, (sh, mg) in enumerate(zip(parts, mgs)):
            t1, t0 = np.clip(mg * M.R_A, 0, 0.95), M.TAU0
            t0v = np.clip(t0 - (1 - vue) * 0.097, 0, None)
            g = sh * M.Z_A * M.LAB_A
            er, ee, pa = ps.coin(g, 1.0 if single else 0.0, "nc")
            er, ee, pa = ps.SALSH * er, ps.SALSH * ee, ps.SALSH * pa
            dl = np.log(1 - np.clip(t1 + theta * kappa, 0, 0.95)) - np.log(1 - t0v)
            coin_m = er + ee + pa + (t0 + t1 + kappa) / 2
            dq_r, dq_d = eR * g * dl, eD * g * dl
            acc["reel"] += (w * -coin_m * dq_r).sum() / 1e9
            acc["dq_reel"] += (w * dq_r).sum() / 1e9
            acc["dq_decl"] += (w * dq_d).sum() / 1e9
            acc["decl"] += (w * (coin_m - M.S_DEPL * M.TAU_ALT) * dq_d).sum() / 1e9
            # marge extensive : prélèvement sur le revenu d'activité de l'adulte k (adultes sous 2 Smic)
            imp_wo = impot_adultes(tm, T, o, *M.adultes(grp, parts, o, sans=k), kids)[0]
            ptr1 = np.where(g > 0, (imp - imp_wo) / np.maximum(g, 1.0), 0.0) + theta * kappa
            ptr0 = M.PTR0[(tnom, k)]
            rest = ps.ptr_rest_single(g) - 0.1005 if single else 0.0126
            p0 = np.clip(ptr0 + rest, -0.5, 0.97)
            p0v = np.clip(ptr0 - (1 - vue) * 0.097 + rest, -0.5, 0.97)
            p1 = np.clip(ptr1 + rest, -0.5, 0.97)
            dans = (g > 1000) & (g < 2 * SMIC)
            dlp = np.log(1 - p1) - np.log(1 - p0v)
            dq = eta * g * dlp * dans
            pse = -((p0 + p1) / 2 + (kappa if False else 0.0)) * dq
            acc["ext"] += (w * pse).sum() / 1e9
            acc["dq_ext"] += (w * dq).sum() / 1e9
            acc["emplois"] += (w * eta * dlp * dans).sum()
            acc["ext_seuls" if single else "ext_couples"] += (w * pse).sum() / 1e9
            acc["emplois_seuls" if single else "emplois_conjoints"] += (w * eta * dlp * dans).sum()
    out = dict(recette=sum((w * imp).sum() for w, imp, *_ in res.values()) / 1e9, **acc)
    out["ps"] = acc["reel"] + acc["ext"]            # variation de perte sèche réelle (négatif = gain)
    out["gain"] = -out["ps"]
    if repart:
        out.update(M.repartition(res))
    return out


MASSE_TRAVAIL = float((M.W_A * M.Z_A * M.LAB_A).sum() / 1e9)   # revenu brut du travail qui réagit (Md€)


def effets_reels(ev):
    """Effets réels en ordres de grandeur [S] : emplois (personnes), ETP, revenu d'activité réel, et équivalent en
    PIB potentiel par une fonction de production Cobb-Douglas (part du travail 2/3) [H] : à capital donné
    (court terme), ΔY/Y = 2/3 × ΔL/L ; capital ajusté à rendement inchangé (long terme), ΔY/Y = ΔL/L."""
    dl = (ev["dq_reel"] + ev["dq_ext"]) / MASSE_TRAVAIL
    salaire_moyen_etp = MASSE_TRAVAIL * 1e9 / 26.0e6           # repère : environ 26 M d'ETP salariés et non salariés [H]
    return dict(emplois_milliers=ev["emplois"] / 1e3, travail_pct=100 * dl,
                etp_milliers=(ev["dq_reel"] + ev["dq_ext"]) * 1e9 / salaire_moyen_etp / 1e3,
                pib_court_pct=100 * 2 / 3 * dl, pib_long_pct=100 * dl)


# ------------------------------------------------------------------ cas-types (OpenFisca aujourd'hui, réforme)
CAS = pd.read_csv(SORTIES / "ircsg_of_cas.csv")


def impot_cas(sched, o, cle):
    """Impôt fusionné d'un cas-type, à partir des revenus après cotisations calculés par OpenFisca."""
    r = CAS[CAS.cle == cle].iloc[0]
    zs = [np.array([float(b)]) for b in str(r.bases).split(";")]
    kids = int(r.enfants)
    if o["fam"] == "quotient":
        return float(U._quotient_cas(sched[1], sched[0], sum(zs)[0:1], len(zs) == 2, kids)[0])
    return float(impot_adultes(*sched, o, zs, zs, [0 * z for z in zs], kids)[0][0])


def cas_type(sched, o, cle):
    r = CAS[CAS.cle == cle].iloc[0]
    nv = impot_cas(sched, o, cle)
    return dict(libelle=r.libelle, bruts=r.bruts, bases=r.bases, auj=float(r.charge), apres=nv, delta=nv - float(r.charge),
                ir=float(r.ir), cehr=float(r.cehr), csg_crds=float(r.csg + r.crds), casa=float(r.casa))
