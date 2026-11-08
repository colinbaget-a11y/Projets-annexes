"""
Fusion de l'IR et de la CSG : état des lieux 2000-2024 et barèmes à rendement constant.

Deux volets, un seul programme :
1. Séries : IR, CSG et CRDS en milliards et en points de PIB (comptabilité nationale,
   donnees/ntl_france.csv ; PIB : donnees/pib_france.json), élasticités apparentes au PIB
   année par année, résumées sur les périodes où les taux légaux n'ont pas changé.
2. Barèmes : distribution des foyers par tranche de revenu fiscal de référence (IRCOM, revenus
   2024, donnees/ircom_national_revenus2024.csv), assiette de type CSG reconstituée par tranche,
   charge actuelle IR + CSG par tranche, puis barèmes fusionnés calibrés pour rapporter autant.
   Effet mécanique, puis correction comportementale simple par l'élasticité du revenu imposable.

    python ir_csg/ir_csg.py        (depuis fiscalite/)

Sorties : ir_csg/sorties/*.csv et figures/ircsg_*.png.
"""
import json
import os
import sys
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
RACINE = HERE.parent
sys.path.insert(0, str(RACINE))
from graphiques import (BLEU, OCRE, VERT, GRIS, INK, MUTED, OUT, fin, grille, plt,  # noqa: E402
                        titre)

SORTIES = HERE / ("sorties_prorata" if os.environ.get("SPLIT") == "prorata" else "sorties")
SORTIES.mkdir(exist_ok=True)

# ------------------------------------------------------------------ 1. séries
# Taux légaux de CSG (revenus d'activité ; pensions de retraite, taux plein ; patrimoine) et part
# de l'assiette retenue sur les revenus d'activité (abattement pour frais professionnels).
# Seules servent ici les dates de changement, pour isoler les périodes à taux constant.
REGIMES_CSG = [
    (1998, 2004, "7,5 % sur 95 % du salaire ; 6,2 % pensions ; 7,5 % patrimoine"),
    (2005, 2011, "7,5 % sur 97 % ; 6,6 % pensions ; 8,2 % patrimoine"),
    (2012, 2017, "7,5 % sur 98,25 % ; 6,6 % pensions ; 8,2 % patrimoine"),
    (2018, 2024, "9,2 % sur 98,25 % ; 8,3 % pensions (taux réduits) ; 9,9 % puis 9,2 % patrimoine"),
]
# Années où le barème ou l'assiette de l'IR a changé au point de fausser l'élasticité apparente.
REFORMES_IR = {
    2006: "réforme du barème (abattement de 20 % intégré, 5 tranches)",
    2007: "première année pleine du barème 2006",
    2012: "gel du barème, tranche à 45 %, contribution sur les hauts revenus",
    2013: "dividendes et intérêts au barème, plafond du quotient abaissé",
    2014: "gel partiel, plafond du quotient abaissé",
    2015: "suppression de la première tranche",
    2017: "réduction d'impôt pour les revenus modestes",
    2018: "prélèvement forfaitaire unique (PFU)",
    2019: "prélèvement à la source",
    2020: "baisse du taux de la première tranche (14 % à 11 %)",
    2023: "fin de la taxe d'habitation sans effet direct ; retour d'une inflation forte",
}


def series():
    d = pd.read_csv(RACINE / "donnees/ntl_france.csv")
    ans = [str(a) for a in range(1999, 2025)]
    lig = d[(d.sto == "D51M") & d.details.isin(["C03", "C04", "C07"])].set_index("details")
    s = lig[ans].T.astype(float) / 1000
    s = s.rename(columns={"C03": "crds", "C04": "csg", "C07": "ir"})
    s.index = s.index.astype(int)
    p = json.load(open(RACINE / "donnees/pib_france.json"))
    idx = p["dimension"]["time"]["category"]["index"]
    pib = {int(a): p["value"][str(i)] / 1000 for a, i in idx.items() if str(i) in p["value"]}
    s["pib"] = [pib[a] for a in s.index]
    for c in ("ir", "csg", "crds"):
        s[f"{c}_pct_pib"] = 100 * s[c] / s.pib
    # élasticité apparente : croissance des recettes / croissance du PIB nominal
    g = np.log(s).diff()
    s["elast_ir"] = g.ir / g.pib
    s["elast_csg"] = g.csg / g.pib
    s["croiss_pib"] = 100 * g.pib
    s = s.loc[2000:]
    s.round(4).to_csv(SORTIES / "series_ir_csg.csv")

    # élasticité moyenne sur les périodes calmes : pente de log(recette) sur log(PIB)
    def pente(y, ans_):
        x = np.log(s.loc[ans_, "pib"]); z = np.log(s.loc[ans_, y])
        return np.polyfit(x, z, 1)[0]
    res = []
    calme_csg = [list(range(2006, 2012)), list(range(2012, 2018)), list(range(2019, 2025))]
    for per in calme_csg:
        res.append(("CSG", f"{per[0]}-{per[-1]}", pente("csg", per), len(per)))
    calme_ir = [a for a in range(2000, 2025) if a not in REFORMES_IR]
    # l'IR suit le revenu de l'année précédente jusqu'en 2018 : on garde des paires d'années
    # consécutives sans réforme
    paires = [a for a in calme_ir if a - 1 in s.index and (a - 1) not in REFORMES_IR and a != 2020]
    e = s.loc[paires, "elast_ir"]
    res.append(("IR (années sans réforme, hors 2020)", ", ".join(map(str, paires)), e.median(), len(paires)))
    res.append(("IR (pente 2000-2024, réformes comprises)", "2000-2024", pente("ir", list(range(2000, 2025))), 25))
    res.append(("CSG (pente 2000-2024, hausses de taux comprises)", "2000-2024", pente("csg", list(range(2000, 2025))), 25))
    el = pd.DataFrame(res, columns=["recette", "periode", "elasticite", "n"])
    el.round(3).to_csv(SORTIES / "elasticites_pib.csv", index=False)
    return s, el


# ------------------------------------------------------------------ 2. distribution IRCOM
def bornes(t):
    t = t.replace(" ", " ").replace(" ", "")
    if t.startswith("Plusde"):
        return float(t[6:]), np.inf
    a, b = t.split("à")
    return float(a), float(b)


# Facteurs de passage du montant déclaré (net imposable) à l'assiette de la CSG :
# salaires : assiette = 98,25 % du brut ; net imposable ≈ brut × (1 − ≈ 11,5 % de cotisations
# salariales − 6,8 % × 98,25 % de CSG déductible) ≈ 0,818 brut, d'où 0,9825 / 0,818 ≈ 1,20.
# pensions : net imposable ≈ brut × (1 − 5,9 % de CSG déductible − ≈ 1 % de cotisation maladie
# complémentaire) ≈ 0,93, d'où ≈ 1,075. Autres revenus (capitaux, fonciers, BIC/BNC) : pris tels
# quels. Ce sont des hypothèses moyennes, pas des données.
F_SAL, F_PENS = 1.20, 1.075
T_CSG_ACT, T_CSG_PAT = 0.092, 0.092
# Taux de CSG sur les pensions selon le RFR du foyer. Seuils légaux pour une part (revenus 2023,
# CSG 2025) : 12 817 €, 16 755 €, 26 004 € ; multipliés par 1,5 part en moyenne (hypothèse).
SEUILS_PENS = [(12817 * 1.5, 0.0), (16755 * 1.5, 0.038), (26004 * 1.5, 0.066), (np.inf, 0.083)]


def taux_pension(rfr_moyen):
    for s, t in SEUILS_PENS:
        if rfr_moyen <= s:
            return t


def distribution(npts=60, split=None):
    x = pd.read_csv(RACINE / "donnees/ircom_national_revenus2024.csv")
    for c in x.columns[1:]:
        x[c] = pd.to_numeric(x[c], errors="coerce")
    x["a"], x["b"] = zip(*x.tranche.map(bornes))
    x["rfr"] = x.rfr_keur / 1e6            # Md€
    x["ir"] = x.impot_net_keur / 1e6
    x["sal"] = x.salaires_keur / 1e6
    x["pens"] = x.pensions_keur / 1e6
    x["autres"] = (x.rfr - 0.9 * (x.sal + x.pens)).clip(lower=0)
    x["moy"] = x.rfr * 1e9 / x.foyers
    x["t_pens"] = x.moy.map(taux_pension)
    # Le barème fusionné porte sur les revenus d'activité et de remplacement ; les autres revenus
    # (capitaux mobiliers au PFU surtout, mais aussi fonciers et BIC/BNC, que l'IRCOM ne sépare
    # pas) restent à leur régime actuel. On leur impute l'IR du PFU (12,8 %) et la CSG du
    # patrimoine (9,2 %), et on les retire de la charge à remplacer.
    x["assiette"] = F_SAL * x.sal + F_PENS * x.pens
    x["csg"] = T_CSG_ACT * F_SAL * x.sal + x.t_pens * F_PENS * x.pens
    # Deux bornes pour l'IR imputé aux autres revenus : 12,8 % (tout au PFU, borne basse) ou
    # prorata du RFR (tout au barème, borne haute). Choix par la variable d'environnement SPLIT.
    if (split or os.environ.get("SPLIT")) == "prorata":
        x["ir_autres"] = x.ir.clip(lower=0) * x.autres / x.rfr
    else:
        x["ir_autres"] = np.minimum(0.128 * x.autres, x.ir.clip(lower=0))
    x["ir_trav"] = x.ir - x.ir_autres
    x["charge"] = x.ir_trav + x.csg
    x["k"] = x.assiette / x.rfr                 # assiette brute (travail et pensions) par euro de RFR

    # foyers représentatifs : densité monotone sur [a, b] ajustée à la moyenne de la tranche
    rows = []
    q = (np.arange(npts) + 0.5) / npts
    for _, r in x.iterrows():
        if np.isinf(r.b):
            pts = np.array([r.moy])
        else:
            mu = np.clip((r.moy - r.a) / (r.b - r.a), 0.02, 0.98)
            if mu >= 0.5:
                p = (2 * mu - 1) / (1 - mu)
                u = q ** (1 / (p + 1))
            else:
                m2 = 1 - mu
                p = (2 * m2 - 1) / (1 - m2)
                u = 1 - q ** (1 / (p + 1))
            pts = r.a + (r.b - r.a) * u
            pts *= r.moy / pts.mean()
        w = r.foyers / len(pts)
        for v in pts:
            rows.append((r.tranche, w, v * r.k, r.ir_trav * 1e9 / r.foyers, r.csg * 1e9 / r.foyers))
    f = pd.DataFrame(rows, columns=["tranche", "poids", "base", "ir_moy", "csg_moy"])
    return x, f


# ------------------------------------------------------------------ 3. barèmes
def impot(base, seuils, taux):
    """Barème par tranches marginales ; seuils[0] = 0."""
    base = np.asarray(base, float)
    t = np.zeros_like(base)
    for i, (s, r) in enumerate(zip(seuils, taux)):
        haut = seuils[i + 1] if i + 1 < len(seuils) else np.inf
        t += r * np.clip(np.minimum(base, haut) - s, 0, None)
    return t


def taux_marginal(base, seuils, taux):
    i = np.searchsorted(seuils, base, side="right") - 1
    return np.asarray(taux)[np.clip(i, 0, len(taux) - 1)]


def calibre(f, cible, fabrique, lo, hi):
    """Trouve le paramètre p tel que le barème fabrique(p) rapporte la cible (bissection)."""
    def rec(p):
        s, t = fabrique(p)
        return (f.poids * impot(f.base, s, t)).sum() / 1e9
    croissant = rec(hi) > rec(lo)
    for _ in range(80):
        m = (lo + hi) / 2
        if (rec(m) < cible) == croissant:
            lo = m
        else:
            hi = m
    return (lo + hi) / 2


def baremes(x, f):
    cible = x.charge.sum()
    B = (f.poids * f.base).sum() / 1e9
    sc = {}
    # A. taux unique
    tA = cible / B
    sc["A_taux_unique"] = ([0.0], [tA])
    # B. largement proportionnel : 5 % sur les 10 000 premiers euros, taux principal jusqu'à
    # 100 000 €, puis 30 % et 40 % (assiette brute par foyer)
    def fB(m):
        return [0, 10e3, 100e3, 250e3], [0.05, m, 0.30, 0.40]
    mB = calibre(f, cible, fB, 0.05, 0.40)
    sc["B_proportionnel"] = fB(mB)
    # B'. même structure, haut de barème à 35 % et 45 %
    def fB2(m):
        return [0, 10e3, 100e3, 250e3], [0.05, m, 0.35, 0.45]
    sc["B2_proportionnel_haut_45"] = fB2(calibre(f, cible, fB2, 0.05, 0.40))
    # C. huit tranches de 5 % à 40 % (proposition de travail de Corentin), seuils proportionnels
    # à une grille de référence, facteur d'échelle calibré
    grille_ref = np.array([0, 10e3, 20e3, 30e3, 45e3, 70e3, 120e3, 250e3])
    def fC(lam):
        return list(grille_ref * lam), [0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40]
    sc["C_huit_tranches"] = fC(calibre(f, cible, fC, 0.2, 10.0))
    # D. bas protégé et haut aligné sur le taux marginal supérieur actuel (≈ 49 % de l'assiette
    # brute : 45 % d'IR et 4 % de CEHR sur un net imposable ≈ 82 % du brut, plus 9,2 % de CSG)
    def fD(m):
        return [0, 12e3, 30e3, 120e3, 250e3], [0.04, 0.09, m, 0.40, 0.49]
    sc["D_bas_protege_haut_actuel"] = fD(calibre(f, cible, fD, 0.05, 0.40))
    # E. le plus proportionnel possible sans perdre en progressivité : franchise à 0 % sur les
    # 12 000 premiers euros, un taux unique jusqu'à 90 000 € (trois foyers sur quatre), puis 40 %
    # et 49 %. Paramètres retenus après balayage (franchise, seuil, taux du haut) : c'est la
    # combinaison au seuil le plus haut dont l'indice de Kakwani reste au niveau actuel.
    def fE(m):
        return [0, 12e3, 90e3, 250e3], [0.0, m, 0.40, 0.49]
    sc["E_franchise_taux_unique"] = fE(calibre(f, cible, fE, 0.05, 0.39))
    return cible, B, sc


def concentration(v, pop):
    """Indice de concentration de v, foyers classés par tranche de RFR (données groupées)."""
    p = np.r_[0, np.cumsum(pop) / pop.sum()]
    L = np.r_[0, np.cumsum(v) / v.sum()]
    return 1 - np.sum((p[1:] - p[:-1]) * (L[1:] + L[:-1]))


def kakwani(base, impot_, pop):
    """Kakwani = concentration de l'impôt − Gini de l'assiette (> 0 : impôt progressif)."""
    return concentration(impot_, pop) - concentration(base, pop)


# Élasticités du revenu imposable (Sicsic 2022, Fiscal Studies, tableau 6, déjà vérifiées dans
# donnees/elasticites_france.csv) : 0,22 pour la moitié du bas, 0,33 pour les 40 % du milieu,
# 0,51 pour les 10 % du haut.
def elasticite(rang):
    return np.where(rang < 0.5, 0.22, np.where(rang < 0.9, 0.33, 0.51))


def comportement(x, f, sc):
    """Effet du changement de taux marginal sur l'assiette : ΔB/B = e × Δln(1 − τ)."""
    # taux marginal actuel IR + CSG par foyer : pente de la charge moyenne par foyer entre tranches
    xb = (x.charge * 1e9 / x.foyers).values
    bb = (x.assiette * 1e9 / x.foyers).values
    pente = np.gradient(xb, bb)
    tau0_tr = dict(zip(x.tranche, np.clip(pente, 0, 0.75)))
    f = f.sort_values("base").reset_index(drop=True)
    f["rang"] = f.poids.cumsum() / f.poids.sum()
    tau0 = f.tranche.map(tau0_tr).values
    e = elasticite(f.rang.values)
    out = {}
    for nom, (s, t) in sc.items():
        tau1 = taux_marginal(f.base, s, t)
        b1 = f.base * np.exp(e * (np.log(1 - tau1) - np.log(1 - tau0)))
        r0 = (f.poids * impot(f.base, s, t)).sum() / 1e9
        r1 = (f.poids * impot(b1, s, t)).sum() / 1e9
        # perte d'assiette pour les autres prélèvements (cotisations, TVA…) non comptée ici
        out[nom] = (r0, r1)
    return out, tau0_tr


def par_tranche(x, f, sc):
    g = x[["tranche", "foyers", "rfr", "assiette", "autres", "ir", "ir_trav", "csg", "charge"]].copy()
    g["taux_actuel_pct"] = 100 * g.charge / g.assiette
    for nom, (s, t) in sc.items():
        f[nom] = f.poids * impot(f.base, s, t) / 1e9
        r = f.groupby("tranche", sort=False)[nom].sum()
        g[nom] = g.tranche.map(r)
        g[nom + "_pct"] = 100 * g[nom] / g.assiette
        g[nom + "_gain_par_foyer"] = 1e9 * (g.charge - g[nom]) / g.foyers
    return g


# ------------------------------------------------------------------ figures
def figures(s, g, sc, haut=None):
    fig, ax = plt.subplots(figsize=(7.2, 3.8))
    ax.plot(s.index, s.ir_pct_pib, color=BLEU, lw=2, label="Impôt sur le revenu")
    ax.plot(s.index, s.csg_pct_pib, color=VERT, lw=2, label="CSG")
    ax.plot(s.index, s.ir_pct_pib + s.csg_pct_pib, color=INK, lw=1.2, ls="--", label="IR + CSG")
    for a in (2005, 2012, 2018):
        ax.axvline(a - 0.5, color=GRIS, lw=0.6, ls=":")
    grille(ax)
    ax.set_ylim(0, None)
    ax.legend(loc="upper left")
    titre(ax, "Recettes de l'IR et de la CSG, en % du PIB, 2000-2024",
          "Pointillés verticaux : changements des taux légaux de CSG (2005, 2012, 2018)")
    fin(fig, "ircsg_series", "Insee, comptes nationaux (recettes par impôt) ; Eurostat (PIB).",
        "Note : CSG sur tous les revenus (activité, remplacement, patrimoine et placements), hors CRDS.")

    lab = [t.replace(" à ", "–").replace("Plus de ", "> ") for t in g.tranche]
    # tranches regroupées pour la lisibilité : on garde jusqu'à 1 M€ puis « > 1 M€ »
    keep = g.index[:16]
    fig, ax = plt.subplots(figsize=(8.2, 4.2))
    xs = np.arange(len(keep))
    ax.plot(xs, g.loc[keep, "taux_actuel_pct"], color=INK, lw=2, marker="o", ms=3, label="Actuel (IR + CSG)")
    if haut is not None:
        a, b = g.loc[keep, "taux_actuel_pct"].values, haut[keep]
        ax.fill_between(xs, np.minimum(a, b), np.maximum(a, b), color=GRIS, alpha=0.25, lw=0,
                        label="Actuel : incertitude sur l'IR des autres revenus")
    noms = {"A_taux_unique": "A : taux unique", "B_proportionnel": "B : largement proportionnel",
            "C_huit_tranches": "C : huit tranches de 5 % à 40 %", "D_bas_protege_haut_actuel": "D : bas protégé, haut à 49 %",
            "E_franchise_taux_unique": "E : franchise, taux unique, 40 % et 49 % en haut"}
    # B et D figurent dans le tableau de la note ; la figure se limite aux trois barèmes discutés
    for nom, c, ls, lw in (("A_taux_unique", GRIS, "-", 1.2), ("C_huit_tranches", OCRE, "-", 1.4),
                           ("E_franchise_taux_unique", BLEU, "-", 2.4)):
        ax.plot(xs, g.loc[keep, nom + "_pct"], color=c, lw=lw, ls=ls, marker="o", ms=3, label=noms[nom])
    ax.set_xticks(xs)
    ax.set_xticklabels([lab[i] for i in keep], rotation=60, ha="right", fontsize=7.5)
    grille(ax)
    ax.legend(loc="upper left", fontsize=8)
    ax.set_ylabel("% de l'assiette brute (travail et pensions)")
    ax.set_xlabel("Tranche de revenu fiscal de référence du foyer (euros)", labelpad=8)
    titre(ax, "Taux moyen IR + CSG par tranche de revenu fiscal de référence, 2024",
          "Actuel et barèmes fusionnés à rendement égal (effet mécanique)")
    fig.subplots_adjust(bottom=0.32)
    fin(fig, "ircsg_taux_moyens", "DGFiP, IRCOM revenus 2024 ; calculs des auteurs.",
        "Note : taux moyen = IR et CSG payés sur les revenus d'activité et les pensions, rapportés à "
        "leur montant brut (assiette de type CSG), par foyer fiscal. La bande grise encadre le taux "
        "actuel selon la part de l'IR attribuée aux revenus du capital (au plus 12,8 % de ces revenus, "
        "ou au prorata). Barèmes : A, 12,5 % dès le premier euro ; C, huit tranches de 5 % à 40 % ; "
        "E, 0 % jusqu'à 12 000 €, 15,5 % jusqu'à 90 000 €, 40 % jusqu'à 250 000 €, 49 % au-delà.")


def main():
    s, el = series()
    x, f = distribution()
    cible, B, sc = baremes(x, f)
    beh, tau0 = comportement(x, f.copy(), sc)
    g = par_tranche(x, f, sc)
    g.round(4).to_csv(SORTIES / "par_tranche.csv", index=False)
    with open(SORTIES / "baremes.txt", "w") as fh:
        fh.write(f"Cible IR (IRCOM) + CSG (reconstituée) : {cible:.1f} Md€ ; assiette brute {B:.0f} Md€\n")
        fh.write(f"IR IRCOM {x.ir.sum():.1f} dont imputé aux autres revenus {x.ir_autres.sum():.1f} ; CSG reconstituée sur travail et pensions {x.csg.sum():.1f} (CSG totale, comptes nationaux 2024 : {s.loc[2024, 'csg']:.1f}) ; autres revenus hors barème {x.autres.sum():.0f} Md€\n\n")
        pop, ass = x.foyers.values, x.assiette.values
        fh.write(f"Kakwani actuel (IR + CSG sur travail et pensions) : {kakwani(ass, x.charge.values, pop):.3f}\n\n")
        for nom, (st, t) in sc.items():
            tm = taux_marginal(f.base, st, t)
            modal = pd.Series(f.poids.values).groupby(tm).sum()
            fh.write(f"Kakwani {kakwani(ass, g[nom].values, pop):.3f} ; taux marginal le plus fréquent "
                     f"{100*modal.idxmax():.1f} %, pour {100*modal.max()/modal.sum():.0f} % des foyers\n")
            seuils = " | ".join(f"{a/1000:,.0f} k€ : {100*r:.1f} %" for a, r in zip(st, t))
            r0, r1 = beh[nom]
            fh.write(f"{nom}\n  {seuils}\n  rendement mécanique {r0:.1f} Md€ ; après réaction (élasticités Sicsic) {r1:.1f} Md€ ; écart {r1-cible:+.1f}\n")
    xp, fp = distribution(split="prorata" if os.environ.get("SPLIT") != "prorata" else "pfu")
    haut = (100 * xp.charge / xp.assiette).values
    figures(s, g, sc, haut)
    print(open(SORTIES / "baremes.txt").read())
    print(el.to_string())
    cols = ["tranche", "foyers", "taux_actuel_pct", "A_taux_unique_pct", "B_proportionnel_pct", "C_huit_tranches_pct", "D_bas_protege_haut_actuel_pct", "E_franchise_taux_unique_pct", "E_franchise_taux_unique_gain_par_foyer"]
    print(g[cols].round(1).to_string())


if __name__ == "__main__":
    main()
