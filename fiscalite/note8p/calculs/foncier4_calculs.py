"""Bloc « fiscalité immobilière », version 4 (note8p/CONSIGNES_V4.md, section Foncier). Scénario central fixé :
architecture B (part communale à double taux + taxe nationale sur le seul sol), enveloppe nationale de 10 Md€, droits de
mutation divisés par deux par tiers en 2029-2031 (clé B_E10 de foncier3.json, qui reste la source des autres chiffres).

Ce script ne refait que ce qui change :
  1. capitalisation de la baisse des droits selon la fréquence de revente de chaque bien (rotation observée par commune
     et type de logement, DVF 2025), au lieu d'une part capitalisée κ arbitraire ; trois hypothèses d'incidence ;
  2. repère loyers / prix / taux longs pour lire la hausse de la valeur du sol (nuance « rente » contre « actualisation ») ;
  3. IFI : rendement, assiette, ordre de grandeur d'une substitution (hors financement).

Lancer depuis fiscalite/ : python3 note8p/calculs/foncier4_calculs.py   (après foncier3_calculs.py)
  -> note8p/sorties/foncier4.json, foncier4_journal.txt, foncier4_taux_loyers.csv
Réutilise sans les modifier foncier/simulation.py et note8p/calculs/foncier_calculs.py (importé : il réécrit
foncier.json à l'identique). Conventions : Md€ de 2025, r = 3 % (variante 4 %), France entière pour les agrégats.
Statuts : [E] empirique publié, [S] simulation, [H] hypothèse, [C] choix de politique.
"""
import contextlib
import io
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ICI = Path(__file__).resolve().parent
N8 = ICI.parent
RACINE = N8.parent
OUT = N8 / "sorties"
sys.path[:0] = [str(ICI), str(RACINE / "foncier")]
with contextlib.redirect_stdout(io.StringIO()):
    import foncier_calculs as fc  # noqa: E402

J3 = json.loads((OUT / "foncier3.json").read_text(encoding="utf-8"))
REC, E = "B_E10", 10.0
L, W, T, PART_CHAMP = fc.L, fc.W, fc.T, fc.PART_CHAMP
DT = T / 2                                          # baisse du taux des droits : 2,90 points
lignes, J = [], {"scenario": REC}


def p(s=""):
    print(s, flush=True)
    lignes.append(s)


def qpond(x, q, w=W):
    o = x.sort_values()
    cw = w[o.index].cumsum() / w.sum()
    return float(o[cw >= q].iloc[0])


# ---------------------------------------------------------------------------------------------- taxe B_E10 par logement
VS = L.v * L.lam
nat = E * 1e9 * J3["parts_recette_nationale"]["B"]["men_log"] * PART_CHAMP / float((W * VS).sum()) * VS
dtf = fc.COMM + nat - L.tf0                         # hausse annuelle de taxe foncière en régime permanent [S]
chk = float((W * dtf).sum() / W.sum())
assert abs(chk - J3["scenarios"][REC]["logements"]["moyenne"]) < 0.5, chk

# ---------------------------------------------------------------------------------------------- 1. rotation des biens
# d0 = droits annuels moyens par logement du parc de la commune et du type (ventes DVF 2025 / parc) = T × v × ρ
rho = (L.d0 / (T * L.v)).fillna(0.0)                # rotation : part de la valeur vendue chaque année
eco = L.d0 / 2                                      # économie annuelle de droits « par logement du parc »
V_mod = float((W * L.v).sum())
rho_agr = float((W * L.d0).sum() / (T * V_mod))
rot = dict(agregee=rho_agr, intervalle_moyen=1 / rho_agr,
           p10=qpond(rho, .10), p50=qpond(rho, .50), p90=qpond(rho, .90),
           maisons=float((W * L.d0)[L.type == "m"].sum() / (T * (W * L.v)[L.type == "m"].sum())),
           apparts=float((W * L.d0)[L.type == "a"].sum() / (T * (W * L.v)[L.type == "a"].sum())),
           paris=float(rho[fc.PARIS_A].iloc[0]))
p(f"[ROTATION] valeur vendue chaque année / valeur du parc (DVF 2025, modèle) : {100*rho_agr:.2f} % (un logement"
  f" change de main en moyenne tous les {1/rho_agr:.0f} ans) ; maisons {100*rot['maisons']:.2f} %, appartements"
  f" {100*rot['apparts']:.2f} % ; communes P10/P50/P90 {100*rot['p10']:.2f}/{100*rot['p50']:.2f}/{100*rot['p90']:.2f} % ;"
  f" Paris (appartements) {100*rot['paris']:.2f} %")
p("[ROTATION] repère [E] : durée de détention des biens revendus en Île-de-France 13,7 ans (appartements) et 15,8 ans"
  " (maisons) en 2024 (Notaires du Grand Paris) ; l'écart avec l'intervalle moyen du parc vient des logements gardés"
  " jusqu'au décès et transmis sans vente (pas de droits de mutation à titre onéreux).")
J["rotation"] = rot

# ---------------------------------------------------------------------------------------------- 2. capitalisation
# Valeur actuelle, pour le propriétaire en place, d'une économie de droits Δτ·P à chaque vente, les ventes arrivant au
# hasard au taux ρ (temps continu) :
#   (a) prix rigides (la France de 2014 : Bachelet et Poulhès, 2017) : l'acheteur garde l'économie, le prix ne bouge pas
#       → gain du propriétaire en place 0 (il ne gagne qu'en rachetant ailleurs) ;
#   (b) le vendeur capte l'économie de son seul acheteur (prix + Δτ/(1+τ1), acheteurs qui n'anticipent pas la revente)
#       → gain = Δτ/(1+τ1) · P · ρ/(ρ + r) = économie annuelle / (ρ + r) à un facteur près ;
#   (c) capitalisation de toutes les ventes futures (anticipations complètes ; ordre de grandeur cohérent avec Dolls et
#       al., 2025, Allemagne : −3 % de prix par point, davantage là où les biens tournent vite)
#       → gain = Δτ · P · ρ / r = économie annuelle / r.
# La hausse de taxe foncière se capitalise en −ΔTF/r (comme en v3). Le point mort de (c) ne dépend pas de r :
#   un propriétaire gagne si son bien est revendu plus souvent que tous les H* = Δτ · P / ΔTF ans.
CAP = {}
VAL_MEN = float(fc.ter.loc["S14", "N2111"] + fc.ter.loc["S14", "N111"])    # logements des ménages, Insee (Md€)
F_DR = float(fc.D0 / 1e9 / fc.D_LOG_FR)                                     # part du champ dans les droits sur logements
for r in (0.03, 0.04):
    perte = dtf / r
    g = {"a": 0 * eco, "b": eco / (1 + DT) / (rho + r) * np.where(rho > 0, 1, 0), "c": eco / r}
    # Md€ France entière : taxe extrapolée au prorata des logements (PART_CHAMP), droits au prorata des droits (F_DR) ;
    # % de la valeur des logements des ménages (Insee) ; dixièmes de prix : % de la valeur du modèle (prix DVF).
    md = lambda s, f: float((W * s).sum() / 1e9 / f)  # noqa: E731
    out = {"perte_tf_md": md(perte, PART_CHAMP)}
    out["perte_tf_pct"] = 100 * out["perte_tf_md"] / VAL_MEN
    for k, gk in g.items():
        net = gk - perte
        gm = md(gk, F_DR)
        out[k] = dict(gain_md=gm, gain_pct=100 * gm / VAL_MEN, net_md=gm - out["perte_tf_md"],
                      net_pct=100 * (gm - out["perte_tf_md"]) / VAL_MEN,
                      gagnants_pct=100 * float(W[net > 0].sum() / W.sum()),
                      net_decile=[float(u) for u in 100 * (W * net).groupby(L.dec_prix).sum()
                                  / (W * L.v).groupby(L.dec_prix).sum()])
    out["perte_tf_decile"] = [float(u) for u in -100 * (W * perte).groupby(L.dec_prix).sum()
                              / (W * L.v).groupby(L.dec_prix).sum()]
    CAP[f"r{int(100*r)}"] = out
    p(f"[CAP r = {100*r:.0f} %] logements des ménages ({VAL_MEN:.0f} Md€) : taxe foncière −{out['perte_tf_pct']:.2f} %"
      f" (−{out['perte_tf_md']:.0f} Md€) ; droits (a) 0 ; (b) +{out['b']['gain_pct']:.2f} % ; (c)"
      f" +{out['c']['gain_pct']:.2f} % → net (a) {out['a']['net_pct']:+.2f} %, (b) {out['b']['net_pct']:+.2f} % ({out['b']['net_md']:+.0f}"
      f" Md€), (c) {out['c']['net_pct']:+.2f} % ({out['c']['net_md']:+.0f} Md€) ; logements gagnants (b) {out['b']['gagnants_pct']:.0f} %,"
      f" (c) {out['c']['gagnants_pct']:.0f} %")
    p("   net par dixième de prix (c) : " + " ".join(f"{u:+.1f}" for u in out["c"]["net_decile"])
      + " ; (b) : " + " ".join(f"{u:+.1f}" for u in out["b"]["net_decile"]))
J["capitalisation"] = CAP
J["valeur_logements_menages"] = VAL_MEN

# Ce que donnerait une durée de détention de 10 à 15 ans appliquée à tout le parc (erreur à éviter)
fausse = {H: 100 * DT / (0.03 * H) for H in (10, 12, 15, 40)}
p("[H UNIFORME] gain (c) si tout le parc était revendu tous les H ans, en % de la valeur, r = 3 % : "
  + " ; ".join(f"H = {H} : {v:.1f} %" for H, v in fausse.items()))
J["gain_c_si_H_uniforme_pct"] = fausse

# Ensemble des biens (logements + autres, toutes catégories de propriétaires) : flux de droits en moins / r
dmto = J3["dmto_demi"]
J["ensemble_biens"] = {f"r{int(100*r)}": dict(perte_tf=E / r, gain_c=dmto / r, net_c=(E - dmto) / r) for r in (.03, .04)}
p(f"[ENSEMBLE] tous biens privés : taxe −{E/0.03:.0f} Md€ ; droits (c) +{dmto/0.03:.0f} ; net (c) −{(E-dmto)/0.03:.0f}"
  " Md€ (r = 3 %) ; (c) est l'ancien cas κ = 100 %, qui est donc la borne haute, pas une hypothèse arbitraire")

# Cas-types : point mort H* = Δτ P / ΔTF et rotation de leur commune
CAS = []
for x in J3["cas"][REC]["projets"]:
    code, ty = {"orleans": ("45234", "a"), "lyon": ("69123", "a"), "massy": ("91377", "a"),
                "sgdb": ("91549", "m")}[x["cle"]]
    i = fc.idx(code, ty)
    CAS.append(dict(cle=x["cle"], prix=x["prix"], economie=x["economie"], dtf=x["dtf"],
                    point_mort=x["economie"] / x["dtf"], rotation=float(rho[i]), intervalle=float(1 / rho[i])))
p("[CAS] point mort (années entre deux ventes au-delà desquelles le propriétaire perd, cas c) et intervalle moyen de la"
  " commune : " + " ; ".join(f"{c_['cle']} {c_['point_mort']:.0f} ans / {c_['intervalle']:.0f} ans" for c_ in CAS))
J["cas"] = CAS
H_star = (DT * L.v / dtf).where(dtf > 0)
J["point_mort"] = dict(p25=qpond(H_star.fillna(1e3), .25), p50=qpond(H_star.fillna(1e3), .50),
                       p75=qpond(H_star.fillna(1e3), .75))
p(f"[POINT MORT] parc : quartiles {J['point_mort']['p25']:.0f} / {J['point_mort']['p50']:.0f} /"
  f" {J['point_mort']['p75']:.0f} ans")

# ---------------------------------------------------------------------------------------------- 3. loyers, prix, taux
ind = pd.read_csv(RACINE / "lvt/donnees/indices.csv", index_col=0)
ecb = Path(__file__).resolve().parent / "donnees_oat10_bce.csv"
oat = pd.read_csv(ecb, index_col=0, comment="#")["oat10"] if ecb.exists() else None
pt = pd.read_csv(RACINE / "foncier/donnees/patrimoine_2025.csv", comment="#", index_col=0)
tab = pd.DataFrame({"prix": ind.prix_logements_anciens, "loyers": ind.loyers})
tab["loyers_sur_prix"] = 100 * (tab.loyers / tab.prix) / (tab.loyers / tab.prix)[1998]
if oat is not None:
    tab["oat10"] = oat
tab["sol_pib"] = 100 * pt.terrains_batis / pt.pib
tab = tab.loc[1996:2025]
tab.round(3).to_csv(OUT / "foncier4_taux_loyers.csv")
a, b = 1998, 2025
J["loyers_prix"] = dict(prix=float(tab.prix[b] / tab.prix[a]), loyers=float(tab.loyers[b] / tab.loyers[a]),
                        loyers_sur_prix_2025=float(tab.loyers_sur_prix[b]),
                        loyers_sur_prix_min=float(tab.loyers_sur_prix.min()),
                        annee_min=int(tab.loyers_sur_prix.idxmin()),
                        oat={int(y): float(tab.oat10[y]) for y in (1998, 2007, 2015, 2020, 2022, 2025)} if oat is not None
                        else None)
p(f"[LOYERS] 1998-2025 : prix des logements anciens ×{J['loyers_prix']['prix']:.2f}, loyers (IPC) ×"
  f"{J['loyers_prix']['loyers']:.2f} ; rapport loyers/prix 2025 = {tab.loyers_sur_prix[b]:.0f} (1998 = 100), minimum"
  f" {tab.loyers_sur_prix.min():.0f} en {J['loyers_prix']['annee_min']}"
  + (" ; OAT 10 ans " + ", ".join(f"{y} {v:.1f} %" for y, v in J['loyers_prix']['oat'].items()) if oat is not None else ""))

# ---------------------------------------------------------------------------------------------- 4. IFI
TN = J3["scenarios"][REC]["taux"]
IFI = dict(recette_2024=2.2, foyers_2024=186_000, patrimoine_net_2024=467.0, recette_2025=2.3, foyers_2025=193_600,
           assiette_sol_apres=TN["sol_apres"])
IFI["points_taux_sol_equivalents"] = 100 * IFI["recette_2025"] / TN["sol_apres"]
IFI["taux_moyen_ifi"] = 100 * IFI["recette_2024"] / IFI["patrimoine_net_2024"]
J["ifi"] = IFI
p(f"[IFI] 2024 : {IFI['recette_2024']} Md€, {IFI['foyers_2024']} foyers, patrimoine net taxable {IFI['patrimoine_net_2024']:.0f}"
  f" Md€ (taux moyen {IFI['taux_moyen_ifi']:.2f} %) ; 2025 : {IFI['recette_2025']} Md€, {IFI['foyers_2025']} foyers"
  f" [E, DGFiP via sources secondaires]. Le remplacer à recette égale : +{IFI['points_taux_sol_equivalents']:.3f} point"
  f" sur le sol privé (hors financement central)")

(OUT / "foncier4_journal.txt").write_text("\n".join(lignes) + "\n", encoding="utf-8")
(OUT / "foncier4.json").write_text(json.dumps(J, ensure_ascii=False, indent=1, default=float), encoding="utf-8")
