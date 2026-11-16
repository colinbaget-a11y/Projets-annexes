"""Transition de l'ancien au nouveau système (sous-partie 6 de la partie IR-CSG) et fragilités du gain.

1. Hausse annuelle des principaux perdants pour une convergence linéaire sur 3, 5 ou 10 ans (chaque foyer paie
   chaque année (1 - λ) × l'ancien impôt + λ × le nouveau : la recette est tenue chaque année par construction).
2. Valeur actualisée de la hausse pour les retraités actuels : facteur d'annuité d'une table de Gompertz
   (μ(x) = A·exp(0,10·x), calée sur une espérance de vie à 65 ans de 21,8 ans, moyenne des 23,6 ans des femmes et
   des 20,0 ans des hommes, Insee 2025 provisoire) ; stock de retraités supposé formé de cohortes de même taille
   entrées à 62 ans (hypothèse) ; taux d'actualisation réel de 1, 2 et 3 % ; avec et sans montée en charge.
3. Gain de transition contre gain permanent : en régime permanent, la hausse de l'impôt sur les pensions futures
   réduit la valeur des droits acquis par les cotisations contributives (27,4 % du salaire brut sous le plafond,
   convention de ps_ircsg_methode.coin) ; elle ajoute au coin des actifs κ = 0,274 × (hausse du taux moyen d'impôt
   sur les pensions). On calcule le gain si les actifs ne le voient pas (θ = 0), le voient à moitié ou en entier.
   C'est une borne : le lien entre un euro cotisé et la pension est faible au bas (minimum contributif) et nul
   au-delà de 8 plafonds.
4. Perception de la CSG (hypothèse H1 du registre) : gain si la CSG d'aujourd'hui ne fait pas réagir le revenu
   d'activité, ou à moitié seulement.
5. Extinction de la CRDS avec la CADES fin 2033 : baisse de taux permise si la recette de la CRDS du champ
   (7,4 Md€) n'est plus à lever.
6. Jeu d'élasticités de long terme (avis Cochrane) : déjà dans evalue_complet (gain_long).

Lancer depuis fiscalite/, après proposition_ircsg.py : python3 synthese/transition_ircsg.py
Sorties : sorties/transition_ircsg.txt et .json
"""
import json

import numpy as np

import outils_ircsg as U

M = U.M
PJ = json.loads((U.OUT / "proposition_ircsg.json").read_text(encoding="utf-8"))
C = PJ["choix"]
B0 = (C["t0"], C["tb"], C["z1"], C["t1"], C["z2"])
O0 = U.options(F=C["F"], **PJ["base"])
S0 = U.bareme(*B0)
R0 = PJ["evaluations"]["proposition"]
L, D = [], {}


def p(s=""):
    print(s, flush=True)
    L.append(s)


# ------------------------------------------------------------------ 1. hausses annuelles
dd = R0["distribution"]
D["hausses"] = {}
p("[HAUSSE ANNUELLE] convergence linéaire sur 3 / 5 / 10 ans (€ par an), centiles de la hausse finale entre foyers"
  " représentatifs (la dispersion réelle est plus forte) et cas-types :")
cibles = [("Retraités, médiane", dd["retraites"]["p50"]), ("Retraités, 90e centile", dd["retraites"]["p90"]),
          ("Retraités, 99e centile", dd["retraites"]["p99"]), ("Couples de retraités, 90e centile", dd["couples_retraites"]["p90"]),
          ("Tous les foyers, 90e centile", dd["tous"]["p90"]), ("Tous les foyers, 99e centile", dd["tous"]["p99"])]
cibles += [(v["libelle"], v["delta"]) for k, v in R0["cas"].items() if v["delta"] > 300]
for lib, h in cibles:
    D["hausses"][lib] = dict(finale=h, **{f"an{n}": h / n for n in (3, 5, 10)})
    p(f"  {lib:<58} hausse finale {h:+7,.0f} € : {h / 3:6,.0f} / {h / 5:6,.0f} / {h / 10:6,.0f} € par an")
p(f"  foyers dont la charge monte de plus de 500 € : {dd['tous']['perd500_M']:.1f} M, dont {dd['retraites']['perd500_M']:.1f} M"
  f" de retraités ; plus de 1 000 € : {dd['tous']['perd1000_M']:.1f} M")

# ------------------------------------------------------------------ 2. valeur actualisée pour les retraités actuels
B, PAS = 0.10, 0.25


def survie(A, x0):
    xs = np.arange(x0, 121, PAS)
    return xs, np.exp(-np.cumsum(A * np.exp(B * xs)) * PAS)


def esperance(A, x0):
    return survie(A, x0)[1].sum() * PAS


lo, hi = 1e-7, 1e-3
for _ in range(100):
    A = (lo * hi) ** 0.5
    lo, hi = (A, hi) if esperance(A, 65) > 21.8 else (lo, A)


def annuite(x0, r, montee=0):
    """Valeur actuelle d'un euro par an versé tant que la personne vit, à partir de l'âge x0 ; avec une montée en
    charge linéaire sur « montee » années (λ = t / montee)."""
    xs, S = survie(A, x0)
    t = xs - x0
    lam = np.ones_like(t) if montee == 0 else np.clip((t + PAS) / montee, 0, 1)
    return float((S * np.exp(-r * t) * lam).sum() * PAS)


xs62, S62 = survie(A, 62)
poids = S62 / S62.sum()
age_moyen = float((poids * xs62).sum())
d_ret = R0["groupes"]["retraites"]["Md"]
pens = float((M.W_R * M.ZN).sum() / 1e9)
D["va"] = dict(gompertz_A=A, B=B, e65=esperance(A, 65), e75=esperance(A, 75), age_moyen_stock=age_moyen,
               hausse_Md=d_ret, pensions_Md=pens, hausse_pct_pensions=100 * d_ret / pens, par_taux={})
p(f"\n[VALEUR ACTUALISÉE] Gompertz : e(65) {esperance(A, 65):.1f} ans, e(75) {esperance(A, 75):.1f} ans ; âge moyen du stock"
  f" de retraités {age_moyen:.1f} ans (cohortes égales dès 62 ans, hypothèse)")
p(f"  hausse annuelle des retraités : {d_ret:+.1f} Md€, soit {100 * d_ret / pens:.1f} % de leurs pensions ({pens:.0f} Md€)")
for r in (0.01, 0.02, 0.03):
    fac = float(sum(w * annuite(x, r) for w, x in zip(poids, xs62)))
    fac5 = float(sum(w * annuite(x, r, 5) for w, x in zip(poids, xs62)))
    D["va"]["par_taux"][f"{r:.2f}"] = dict(facteur=fac, facteur_5ans=fac5, va_Md=d_ret * fac, va_5ans_Md=d_ret * fac5,
                                           age65=annuite(65, r), age75=annuite(75, r), age85=annuite(85, r))
    p(f"  taux réel {100 * r:.0f} % : facteur moyen {fac:.1f} (montée sur 5 ans : {fac5:.1f}) → valeur actualisée"
      f" {d_ret * fac:.0f} Md€ ({d_ret * fac5:.0f} Md€ avec la montée sur 5 ans) ; un euro par an vaut {annuite(65, r):.1f} €"
      f" à 65 ans, {annuite(75, r):.1f} € à 75 ans, {annuite(85, r):.1f} € à 85 ans")
D["va_cas"] = {}
for k in ("ret20", "ret25", "rc45"):
    h = R0["cas"][k]["delta"]
    D["va_cas"][k] = {f"age{a}": h * annuite(a, 0.02, 5) for a in (65, 75, 85)}
    p(f"  {R0['cas'][k]['libelle']} : hausse finale {h:+,.0f} € par an ; valeur actualisée à 2 %, montée sur 5 ans :"
      + " ; ".join(f" {a} ans {h * annuite(a, 0.02, 5):,.0f} €" for a in (65, 75, 85)))

# ------------------------------------------------------------------ 3. gain de transition contre gain permanent
C_CONTRIB = 0.1732 + 0.1005          # cotisations contributives sous le plafond, par euro brut (ps_ircsg_methode.coin)
dtau = d_ret / pens
kappa = C_CONTRIB * dtau
D["permanent"] = dict(dtau=dtau, kappa=kappa, c_contrib=C_CONTRIB, gains={})
p(f"\n[GAIN PERMANENT] hausse du taux moyen d'impôt sur les pensions {100 * dtau:.2f} points ; coin ajouté au salaire"
  f" des actifs en régime permanent κ = {C_CONTRIB:.3f} × {dtau:.4f} = {100 * kappa:.2f} point")
for theta in (0.0, 0.5, 1.0):
    o = dict(O0, kappa_reel=kappa, kappa_vu=theta * kappa)
    g = {j: -M.evalue("perm", *S0, o, jeu=j, sorties=False)["v2"] for j in ("bas", "central", "haut")}
    D["permanent"]["gains"][f"{theta:.1f}"] = g
    p(f"  θ = {theta:.1f} : gain permanent {g['central']:.2f} Md€ ({g['bas']:.2f} à {g['haut']:.2f}) contre"
      f" {R0['gain_central']:.2f} dans le modèle")

# ------------------------------------------------------------------ 4. perception de la CSG
D["saillance"] = {}
for vue in (1.0, 0.5, 0.0):
    o = dict(O0, csg_vue=vue)
    r = {j: M.evalue("sal", *S0, o, jeu=j, sorties=False) for j in ("bas", "central", "haut")}
    D["saillance"][f"{vue:.1f}"] = dict(gain={j: -r[j]["v2"] for j in r}, intensif=-r["central"]["v2_reel"],
                                        extensif=-r["central"]["v2_ext"])
    p(f"[CSG PERÇUE à {100 * vue:.0f} %] gain {-r['central']['v2']:.2f} Md€ ({-r['bas']['v2']:.2f} à {-r['haut']['v2']:.2f})"
      f" dont intensif {-r['central']['v2_reel']:+.2f}, participation {-r['central']['v2_ext']:+.2f}")

# ------------------------------------------------------------------ 5. extinction de la CRDS fin 2033
crds = float(M.x.crds.sum())
lo, hi = -0.10, 0.05
for _ in range(40):
    d = (lo + hi) / 2
    t0, tb, z1, t1, z2 = B0
    rec = U.recette(U.bareme(t0 + d, tb + d, z1, t1 + d, z2), O0)
    lo, hi = (d, hi) if rec < M.CIBLE - crds else (lo, d)
D["crds"] = dict(recette_Md=crds, points=100 * (lo + hi) / 2, part_recette=100 * crds / M.CIBLE)
p(f"\n[CRDS] recette de la CRDS dans le champ {crds:.2f} Md€ ({100 * crds / M.CIBLE:.1f} % de la recette fusionnée) :"
  f" si elle disparaît en 2034, les taux sous 50 % peuvent baisser de {-100 * (lo + hi) / 2:.2f} point")

# ------------------------------------------------------------------ 6. long terme
D["long"] = dict(gain=R0["gain_long"], ext=R0["ext_long"])
p(f"[LONG TERME] jeu de l'avis Cochrane (intensif 0,10 à 0,25, participation 0,10) : gain {R0['gain_long']:.2f} Md€ dont"
  f" participation {R0['ext_long']:.2f}")
U.ecrire("transition_ircsg", L, D)
