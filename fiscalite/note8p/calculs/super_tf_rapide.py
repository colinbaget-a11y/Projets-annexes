"""Fiche 4 « Super taxe foncière » : chiffrages rapides avec ce qui existe déjà dans le dépôt (17/11/2026).

Lancer depuis fiscalite/ : python3 note8p/calculs/super_tf_rapide.py   (n'écrit rien : tout est imprimé)

Sources (déjà dans le dépôt sauf mention) :
- Insee, comptes de patrimoine fin 2025, tableau 8.200 (foncier/donnees/terrains_secteurs_2025.csv, patrimoine_2025.csv)
- TFPB 2025 : 43,131 Md€ (DGCL-DGFiP, note REI 2025, annexe 1) ; part « ménages » 26,310 (annexe 4, clé conventionnelle
  61 %) ; TFPB sur les logements 31,590 (SDES, Compte du logement 2025) : foncier/notes/inventaire.md
- DMTO : foncier3.json (16,15 Md€ au taux permanent, ventes 2025) ; séries OFGL / Compte du logement / comptabilité
  nationale recopiées de foncier/notes/inventaire.md
- NOUVEAU : BCE Data Portal, BSI.M.FR.N.A.A22.A.1.U2.2250.Z01.E (encours des crédits à l'habitat aux ménages, France,
  M€) et MIR.M.FR.B.A22.A.R.A.2250.EUR.O (taux moyen de l'encours des crédits à l'habitat), téléchargés le 17/11/2026
- Modèle communal foncier/simulation.py (logements des particuliers, métropole hors Alsace-Moselle, base 2025), importé
  sans modification.
Statuts : [E] publié, [S] calcul, [H] hypothèse.
"""
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

RACINE = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(RACINE / "foncier")]
import simulation as sm  # noqa: E402

ter = pd.read_csv(RACINE / "foncier/donnees/terrains_secteurs_2025.csv", comment="#").set_index("secteur")
pat = pd.read_csv(RACINE / "foncier/donnees/patrimoine_2025.csv", comment="#").set_index("annee")
f3 = json.loads((RACINE / "note8p/sorties/foncier3.json").read_text())

PRIV = ["S11", "S12", "S14", "S15"]
SOLB = sum(ter.loc[s, "N2111"] for s in PRIV)
BATI = sum(ter.loc[s, "N111"] + ter.loc[s, "N1121"] for s in PRIV)
BASE_PRIV = SOLB + BATI                                     # immobilier bâti privé, sol compris (Md€, fin 2025)
MEN = ter.loc["S14", "N2111"] + ter.loc["S14", "N111"] + ter.loc["S14", "N1121"]
TFPB, TFPB_MEN, TFPB_LOG = 43.131, 26.310, 31.590           # [E] 2025
DMTO = f3["dmto_total"]                                      # [S] 16,15 Md€, taux permanent, ventes 2025
ENCOURS, TAUX_ENC = 1288.312, 1.94                           # [E] BCE, déc. 2025 (Md€ ; %)


def pct(x):
    return f"{100 * x:.3f} %"


print("== 1. Taux neutres sur la valeur de marché (comptes de patrimoine fin 2025)")
print(f"Base immobilier bâti privé (S11+S12+S14+S15, sol bâti + logements + bâtiments non résidentiels) : {BASE_PRIV:,.0f} Md€")
print(f"  remplace la TFPB ({TFPB}) : {pct(TFPB / BASE_PRIV)} ; TFPB + DMTO ({TFPB + DMTO:.1f}) : "
      f"{pct((TFPB + DMTO) / BASE_PRIV)} ; TFPB + DMTO/2 : {pct((TFPB + DMTO / 2) / BASE_PRIV)}")
print(f"  coût d'un point de base (0,01 %) : {BASE_PRIV * 1e-4:.2f} Md€")
print(f"Ménages seuls (S14 sol bâti + bâti, {MEN:,.0f} Md€) : TFPB 'ménages' {TFPB_MEN} -> {pct(TFPB_MEN / MEN)}")
print(f"Modèle communal (logements des particuliers, métropole hors A-M) : valeur {sm.VAL / 1e9:,.0f} Md€, TF "
      f"{sm.TF0 / 1e9:.1f}, DMTO logements {sm.D0 / 1e9:.1f} -> {pct(sm.TF0 / sm.VAL)} ; avec DMTO {pct((sm.TF0 + sm.D0) / sm.VAL)}")

print("\n== 2. Déductibilité de la dette / des intérêts")
INTERETS = ENCOURS * TAUX_ENC / 100
print(f"Encours crédits habitat des ménages fin 2025 : {ENCOURS:,.0f} Md€ ; taux moyen de l'encours {TAUX_ENC} % "
      f"-> intérêts ≈ {INTERETS:.1f} Md€/an [S]")
for nom, rec in (("TFPB", TFPB), ("TFPB + DMTO", TFPB + DMTO)):
    t = rec / BASE_PRIV
    tn = rec / (BASE_PRIV - ENCOURS)
    print(f"  {nom} : dette déduite de l'assiette -> perte {t * ENCOURS:.1f} Md€ au taux brut ; taux neutre sur base "
          f"nette {pct(tn)} (+{100 * (tn / t - 1):.0f} %)")
print(f"  crédit d'impôt égal aux intérêts : {INTERETS:.0f} Md€, plus que la TFPB des ménages ({TFPB_MEN}) -> "
      f"impraticable sans plafond ; déduction de 1 % des intérêts ≈ {INTERETS / 100:.2f} Md€")

print("\n== 3. Modèle communal : taxe unique sur la valeur de marché (sol + bâti), recette constante")
L, W = sm.L, sm.L.n
for s, nom in ((0, "remplace la TF"), (1, "remplace TF + DMTO logements")):
    tf1, d1 = sm.valeur_unique(s)
    dtf = tf1 - L.tf0
    net = dtf - s * L.d0
    g = pd.DataFrame({"w": W, "dtf": dtf * W, "net": net * W, "tf0": L.tf0 * W, "v": L.v * W, "dec": L.dec_prix})
    by = g.groupby("dec").sum()
    print(f"[{nom}] taux {pct((sm.TF0 + s * sm.D0) / sm.VAL)}")
    print("  dixième de prix au m² : " + " | ".join(
        f"{d + 1}: {by.dtf[d] / by.w[d]:+.0f} € ({100 * by.dtf[d] / by.tf0[d]:+.0f} %)" for d in by.index))
    if s:
        print("  net de l'économie annuelle moyenne de droits : " + " | ".join(
            f"{d + 1}: {by.net[d] / by.w[d]:+.0f} €" for d in by.index))
    hausse = (W * (dtf > 0)).sum() / W.sum()
    p300 = (W * (dtf > 300)).sum() / W.sum()
    paris = L.codgeo == "75056"
    print(f"  logements en hausse {100 * hausse:.0f} % ; > +300 €/an {100 * p300:.0f} % ; Paris "
          f"{100 * ((dtf * W)[paris].sum() / (L.tf0 * W)[paris].sum()):+.0f} %")
    dep = g.assign(dep=L.dep).groupby("dep").sum()
    r = (dep.dtf / dep.tf0).sort_values()
    print("  départements extrêmes (variation de la TF) : " + ", ".join(f"{k} {100 * v:+.0f} %" for k, v in r.head(3).items())
          + " ... " + ", ".join(f"{k} {100 * v:+.0f} %" for k, v in r.tail(3).items()))

print("\n== 4. Volatilité de l'assiette (valeur des logements et du sol bâti des ménages, comptes de patrimoine)")
v = pat.terrains_batis_men + pat.logements_men
gr = v.pct_change().dropna()
lis = v.rolling(3).mean()
grl = lis.pct_change().dropna()
print(f"  variation annuelle 1979-2025 : écart-type {100 * gr.std():.1f} pts ; pire année {100 * gr.min():+.1f} % "
      f"({gr.idxmin()}) ; 2023 {100 * gr[2023]:+.1f} %, 2024 {100 * gr[2024]:+.1f} %, 2025 {100 * gr[2025]:+.1f} %")
print(f"  base lissée sur 3 ans : écart-type {100 * grl.std():.1f} pts ; pire année {100 * grl.min():+.1f} % ({grl.idxmin()})")
DM = {"Compte du logement (logements)": [16.418, 16.818, 13.002, 11.239, 13.568],
      "Comptabilité nationale (droits d'enregistrement)": [21.007, 21.605, 16.843, 14.663, None]}
for k, s in DM.items():
    x = [a for a in s if a]
    print(f"  DMTO {k} 2021-2025 : {x} ; creux/pic {100 * (min(x) / max(x) - 1):.0f} %")
