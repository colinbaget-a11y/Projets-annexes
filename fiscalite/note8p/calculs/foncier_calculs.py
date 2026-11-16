"""Bloc « fiscalité immobilière » de la note de 8 pages (note8p/CADRE.md, arbitrages de l'auteur du 17/11/2026).

Lancer depuis fiscalite/ : python3 note8p/calculs/foncier_calculs.py
  -> note8p/sorties/foncier.json (tous les chiffres, tables `annuel` 2027-2040) et foncier_journal.txt (journal lisible)

Réutilise le modèle communal de foncier/simulation.py (importé, non modifié : logements des particuliers, métropole hors
Alsace-Moselle, base 2025) et les conventions de synthese/calculs_foncier.py (recopiées ici, ce script n'est pas importé
car il réécrit ses sorties). Ce qui change par rapport à la version de la note fusionnée :
- architecture : UNE taxe foncière, UNE base par bien = valeur du sol + 1/4 de la valeur du bâti (rapport 4 entre le taux
  du sol et celui du bâti), un taux communal voté (recette communale inchangée au départ) + un taux national uniforme ;
- hausse NETTE : enveloppes de recettes nationales nouvelles de 10, 15 et 20 Md€ (et la seule substitution aux droits) ;
- capitalisation : la valeur du sol (donc l'assiette) baisse quand l'impôt sur le sol monte ; le taux national est calé
  après capitalisation ;
- synchronisation : aucune baisse de droits avant la recette ; trois paliers annuels synchronisés (2029, 2030, 2031) ;
- report de paiement ciblé sur les propriétaires occupants modestes, son besoin de financement compté chaque année ;
- droits de mutation chiffrés France entière (l'ancien 7,58 Md€ portait sur le champ du modèle).
Conventions : Md€ de 2025 (assiettes 2025, non indexées, comme synthese/synthese_ensemble.py) ; + = recette publique en
plus par rapport au droit en vigueur (taux permanent des droits, la majoration temporaire tombant le 31/3/2028).
Statuts : [E] empirique publié, [S] simulation, [H] hypothèse, [C] choix de politique.
"""
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ICI = Path(__file__).resolve().parent
N8 = ICI.parent
RACINE = N8.parent
OUT = N8 / "sorties"
OUT.mkdir(exist_ok=True)
sys.path[:0] = [str(RACINE / "foncier")]
import simulation as sm  # noqa: E402

L, c = sm.L, sm.c
W = L.n
NLOG = W.sum()
T = sm.TAUX_DMTO                       # 5,807 % : 4,50 % département + 1,20 % commune + 2,37 % × 4,50 % frais d'assiette
TF0, D0, VAL, TERRE = sm.TF0, sm.D0, sm.VAL, sm.TERRE
PART_CHAMP = sm.part_champ             # logements du modèle / logements des particuliers de métropole
K = 4.0                                # rapport taux du sol / taux du bâti [C]
R = 0.03                               # taux de capitalisation (loyer net / prix) [H] ; 4 % en variante
ANS = list(range(2027, 2041))
J = {"conventions": "Md€ de 2025, assiettes 2025 non indexées ; + = recette publique en plus par rapport au droit en"
                    " vigueur (droits au taux permanent) ; − = coût"}
lignes = []


def p(s=""):
    print(s, flush=True)
    lignes.append(s)


def fr(x, d=0):
    return f"{x:,.{d}f}".replace(",", " ").replace(".", ",")


def qpond(x, q):
    o = x.sort_values()
    cw = W[o.index].cumsum() / NLOG
    return float(o[cw >= q].iloc[0])


def par_decile(s):
    return ((W * s).groupby(L.dec_prix).sum() / W.groupby(L.dec_prix).sum()).values


def ratio_decile(num, den):
    return ((W * num).groupby(L.dec_prix).sum() / (W * den).groupby(L.dec_prix).sum()).values


PARIS = L.codgeo == "75056"
PARIS_A = PARIS & (L.type == "a")


def idx(code, t):
    return L[(L.codgeo == code) & (L.type == t)].index[0]


# =====================================================================================================================
# 1. DROITS DE MUTATION : coût de la division par deux (France entière, taux permanent, ventes 2025)
# =====================================================================================================================
p("=" * 110)
p("1. DROITS DE MUTATION")
p("=" * 110)
CYCLE = {2021: 16.418, 2022: 16.818, 2023: 13.002, 2024: 11.239, 2025: 13.568}   # droits sur les logements, Md€ (CSL 2025)
DMTO_TOT = {2023: 16.311, 2024: 14.093, 2025: 16.703}                              # tous biens, collectivités (OFGL)
F_2324 = T * c.valeur_ventes_an_2324.sum() / 1e9 / np.mean([CYCLE[2023], CYCLE[2024]])   # part du champ, 2023-2024
D_LOG_FR = D0 / 1e9 / F_2324                    # logements, France entière, taux permanent, ventes 2025 [S]
RAP_PERM = D_LOG_FR / CYCLE[2025]               # taux permanent / taux perçu en 2025 (majoration temporaire)
D_AUT_FR = (DMTO_TOT[2025] - CYCLE[2025]) * RAP_PERM   # autres biens (locaux, terrains), même correction [S, non vérifié]
D_FR = D_LOG_FR + D_AUT_FR
DEMI = D_FR / 2
ANCIEN = 0.5 * D0 / 1e9 + 0.5 * (DMTO_TOT[2025] - CYCLE[2025]) * (D0 / 1e9 / CYCLE[2025])
p(f"[DMTO] France entière au taux permanent (ventes 2025) : logements {D_LOG_FR:.2f} Md€, autres biens {D_AUT_FR:.2f},"
  f" total {D_FR:.2f} ; division par deux : {DEMI:.2f} Md€ (ancien calibrage {ANCIEN:.2f}, champ du modèle = métropole"
  f" hors Alsace-Moselle, {100*F_2324:.1f} % des droits sur les logements)")
# Sensibilité au cycle : à la moyenne 2023-2024 des ventes
D_FR_2324 = D_FR * np.mean([CYCLE[2023], CYCLE[2024]]) / CYCLE[2025]
p(f"[DMTO] au niveau moyen de 2023-2024 (creux du marché) : moitié = {D_FR_2324/2:.2f} Md€ ; au niveau de 2022 (pic) :"
  f" {D_FR*CYCLE[2022]/CYCLE[2025]/2:.2f} Md€")
# Réaction durable des ventes (σ % de ventes par point de droits) : coût réduit (bonus, non compté dans la trajectoire)
SIG = {0: 0.0, 3: 0.03, 6: 0.06, 8: 0.08}
cout_sig = {s: D_FR * (1 - 0.5 * (1 + v) ** (100 * T / 2)) for s, v in SIG.items()}
p("[DMTO] coût de la division par deux selon la réaction durable des ventes : " + " ; ".join(
    f"σ = {s} %/pt : {v:.2f} Md€ (ventes +{100*((1+SIG[s])**(100*T/2)-1):.0f} %)" for s, v in cout_sig.items()))
J["dmto"] = dict(logements_fr=D_LOG_FR, autres_fr=D_AUT_FR, total_fr=D_FR, demi=DEMI, ancien_calibrage=ANCIEN,
                 demi_2324=D_FR_2324 / 2, cout_selon_sigma=cout_sig, part_champ_droits=F_2324,
                 cout_par_point=D_FR / (100 * T), taux_avant=100 * T, taux_apres=100 * T / 2)
p(f"[DMTO] coût par point de taux total (statique) : {D_FR/(100*T):.2f} Md€")

# =====================================================================================================================
# 2. ASSIETTE NATIONALE : sol + bâti/4, tous les biens privés (Insee, comptes de patrimoine fin 2025)
# =====================================================================================================================
p()
p("=" * 110)
p("2. ASSIETTE ET TAUX")
p("=" * 110)
ter = pd.read_csv(RACINE / "foncier/donnees/terrains_secteurs_2025.csv", comment="#").set_index("secteur")
PRIV = ["S11", "S12", "S14", "S15"]
SOL = {s: float(ter.loc[s, "N2111"] + ter.loc[s, "N2119"]) for s in PRIV}       # sol bâti + terrains non bâtis
SOL_BATI = {s: float(ter.loc[s, "N2111"]) for s in PRIV}
BATI = {s: float(ter.loc[s, "N111"] + ter.loc[s, "N1121"]) for s in PRIV}       # logements + bâtiments non résidentiels
BW = {s: SOL[s] + BATI[s] / K for s in PRIV}
BW_TOT = sum(BW.values())
SOL_TOT, BATI_TOT = sum(SOL.values()), sum(BATI.values())
NU_TOT = sum(SOL[s] - SOL_BATI[s] for s in PRIV)
# Ménages : la part qui porte sur leurs logements (sol sous bâtiments + bâti) ; leurs terrains nus à part
BW_MEN_LOG = SOL_BATI["S14"] + BATI["S14"] / K
PART_MEN_LOG = BW_MEN_LOG / BW_TOT
# HLM : sol estimé par synthese/calculs_foncier.py (603 Md€, valeur Insee, majorant) ; bâti HLM ≈ logements des sociétés
HLM_SOL, HLM_BATI = 603.0, float(ter.loc["S11", "N111"])
PART_ENTR_IS = (BW["S11"] + BW["S12"] - (HLM_SOL + HLM_BATI / K)) / BW_TOT     # entreprises soumises à l'IS (hors HLM)
p(f"[ASSIETTE] biens privés (S11, S12, S14, S15 ; hors terres agricoles et biens publics) : sol {fr(SOL_TOT)} Md€ dont"
  f" terrains non bâtis {fr(NU_TOT)}, bâti {fr(BATI_TOT)} ; base pondérée sol + bâti/4 = {fr(BW_TOT)} Md€ ;"
  f" logements des ménages {100*PART_MEN_LOG:.1f} %, terrains nus des ménages {100*(SOL['S14']-SOL_BATI['S14'])/BW_TOT:.1f} %,"
  f" sociétés (dont HLM) {100*(BW['S11']+BW['S12'])/BW_TOT:.1f} %, dont soumises à l'IS hors HLM ≈ {100*PART_ENTR_IS:.1f} %")
p(f"[ASSIETTE] part du sol dans la base pondérée : {100*SOL_TOT/BW_TOT:.0f} % ; un euro de recette nationale porte donc à"
  f" {100*(BATI_TOT/K)/BW_TOT:.0f} % sur le bâti")
J["assiette"] = dict(sol=SOL_TOT, nu=NU_TOT, bati=BATI_TOT, base_ponderee=BW_TOT, part_men_log=PART_MEN_LOG,
                     part_entr_is=PART_ENTR_IS, par_secteur={s: dict(sol=SOL[s], bati=BATI[s], bw=BW[s]) for s in PRIV})

# Capitalisation : V_sol = rente / (R + τ_sol). Avant : τ0 = taxe actuelle / valeur (0,358 % sur le bâti des ménages,
# appliqué à tous les biens bâtis ; terrains nus : taxe sur le non-bâti, ≈ 0,08 % [H]). Après : τ1 = t_c + t_n sur tout le
# sol, t_c étant le taux communal qui garde la recette communale (τ0 × valeur des biens bâtis) sur la nouvelle base.
TAU0 = TF0 / VAL
TAU0_NU = 0.0008
REC_COMM = TAU0 * (sum(SOL_BATI.values()) + BATI_TOT)


def equilibre(E, r=R, cap=True):
    """Taux national t_n (sur la base sol + bâti/4) qui lève E Md€ ; avec cap=True, une fois la valeur du sol ajustée."""
    vs_b, vs_n = sum(SOL_BATI.values()), NU_TOT
    vs1_b, vs1_n = vs_b, vs_n
    for _ in range(200):
        base = vs1_b + vs1_n + BATI_TOT / K
        tc, tn = REC_COMM / base, E / base
        if not cap:
            break
        tau1 = tc + tn
        vs1_b = vs_b * (r + TAU0) / (r + tau1)
        vs1_n = vs_n * (r + TAU0_NU) / (r + tau1)
    return dict(tn=tn, tc=tc, base=vs1_b + vs1_n + BATI_TOT / K, sol=vs1_b + vs1_n,
                baisse_sol=1 - (vs1_b + vs1_n) / (vs_b + vs_n))


ENV = [round(DEMI, 2), 10.0, 15.0, 20.0]
NOM_ENV = {ENV[0]: "substitution", 10.0: "E10", 15.0: "E15", 20.0: "E20"}
eq = {}
for E in ENV:
    s0, s3, s4 = equilibre(E, cap=False), equilibre(E), equilibre(E, r=0.04)
    rend = s0["tn"] * s3["base"]           # rendement du taux statique une fois les valeurs ajustées
    eq[E] = dict(tn_statique=100 * s0["tn"], tn=100 * s3["tn"], tn_r4=100 * s4["tn"], tc=100 * s3["tc"],
                 tc0=100 * s0["tc"], baisse_sol=100 * s3["baisse_sol"], baisse_sol_r4=100 * s4["baisse_sol"],
                 rendement_taux_statique=rend, perte_rendement=100 * (1 - rend / E))
    p(f"[TAUX {NOM_ENV[E]} = {E:.1f} Md€] taux national {100*s0['tn']:.3f} % du sol ({100*s0['tn']/K:.3f} % du bâti) sans"
      f" capitalisation ; {100*s3['tn']:.3f} % après (r = 4 % : {100*s4['tn']:.3f} %) ; la valeur du sol baisse de"
      f" {100*s3['baisse_sol']:.1f} % (r = 4 % : {100*s4['baisse_sol']:.1f} %), si bien qu'au taux statique la recette ne"
      f" serait que {rend:.1f} Md€ (−{eq[E]['perte_rendement']:.0f} %) ; taux communal moyen sur le sol"
      f" {100*s0['tc']:.2f} % → {100*s3['tc']:.2f} % après capitalisation (recette inchangée)")
p(f"[TAUX] sans les terrains non bâtis (contenu mal connu : terrains à bâtir, jardins, espaces naturels), la base"
  f" pondérée tombe à {fr(BW_TOT-NU_TOT)} Md€ et les taux montent de {100*(BW_TOT/(BW_TOT-NU_TOT)-1):.0f} %")
J["sens_sans_nus"] = 100 * (BW_TOT / (BW_TOT - NU_TOT) - 1)
p(f"[TAUX] aujourd'hui, taxe / valeur ≈ {100*TAU0:.3f} % sur le sol comme sur le bâti des logements ; après passage à la"
  f" base sol + bâti/4 à recette communale constante, le sol paie en moyenne {eq[15.0]['tc0']:.2f} % et le bâti"
  f" {eq[15.0]['tc0']/K:.2f} % avant la part nationale")
J["taux"] = {NOM_ENV[E]: v for E, v in eq.items()}

# =====================================================================================================================
# 3. CE QUE PAIENT LES LOGEMENTS (modèle communal ; valeurs avant capitalisation, montants E levés)
# =====================================================================================================================
p()
p("=" * 110)
p("3. LOGEMENTS DES PARTICULIERS")
p("=" * 110)
B_I = L.v * (L.lam + (1 - L.lam) / K)                      # base pondérée de chaque logement (valeurs du modèle)
TC_COM = (W * L.tf0).groupby(L.codgeo).sum() / (W * B_I).groupby(L.codgeo).sum()
COMM = L.codgeo.map(TC_COM) * B_I                          # part communale sur la nouvelle base, recette constante
REDIS = COMM - L.tf0
SB_MOD = (W * B_I).sum()
st = pd.DataFrame({"po": c.rp_prop, "loc": (c.rp_loc - c.rp_lochlmv).clip(lower=0), "rs": c.rsecocc,
                   "vac": c.logvac, "grat": c.rp_grat}).fillna(0)
part_st = st.div(st.sum(axis=1).replace(0, np.nan), axis=0).fillna(0)
PO = L.codgeo.map(part_st["po"]).fillna(0)
LOC = L.codgeo.map(part_st["loc"]).fillna(0)
d1 = L.d0 / 2
V_VENTES = c.valeur_ventes_an.sum()


def logements(E):
    """Taxe de chaque logement (Md€ E levés France entière ; part des logements des ménages × part du champ)."""
    paye = E * 1e9 * PART_MEN_LOG * PART_CHAMP
    tn_mod = paye / SB_MOD
    nat = tn_mod * B_I
    return COMM + nat, nat, tn_mod


RES = {}
for E in ENV:
    tf1, nat, tn_mod = logements(E)
    dtf = tf1 - L.tf0
    r_ = dict(paye_logements_champ=float((W * nat).sum() / 1e9), paye_logements_fr=E * PART_MEN_LOG,
              tn_modele=100 * tn_mod,
              dtf=[float(u) for u in par_decile(dtf)], dtf_pct=[float(u) for u in 100 * ratio_decile(dtf, L.tf0)],
              net_parc=[float(u) for u in par_decile(dtf + d1 - L.d0)],
              tfv=[float(u) for u in 100 * ratio_decile(tf1, L.v)],
              plus300=float(W[dtf > 300].sum() / NLOG), plus600=float(W[dtf > 600].sum() / NLOG),
              baisse=float(W[dtf < 0].sum() / NLOG), double=float(W[dtf > L.tf0].sum() / NLOG),
              paris_pct=float(100 * (W * dtf)[PARIS].sum() / (W * L.tf0)[PARIS].sum()),
              paris_a=float(dtf[PARIS_A].iloc[0]),
              pctl={q: qpond(dtf, q / 100) for q in (10, 25, 50, 75, 90, 95, 99)},
              moyenne=float((W * dtf).sum() / NLOG), moyenne_pct=float(100 * (W * dtf).sum() / TF0))
    ty = L.assign(a=W * dtf, w=W).groupby("type").sum(numeric_only=True)
    r_["maisons"], r_["apparts"] = float(ty.a["m"] / ty.w["m"]), float(ty.a["a"] / ty.w["a"])
    # report de paiement : somme des hausses positives des propriétaires occupants (champ), France entière
    r_["hausse_po_fr"] = float((W * dtf.clip(lower=0) * PO).sum() / 1e9 / PART_CHAMP)
    r_["hausse_bailleurs_fr"] = float((W * dtf * LOC).sum() / 1e9 / PART_CHAMP)
    # impôt sur le bâti des logements (champ) : part communale (k = 4) + part nationale sur bâti/4
    r_["impot_bati"] = float((W * (L.codgeo.map(TC_COM) + tn_mod) * L.v * (1 - L.lam) / K).sum() / 1e9)
    RES[E] = r_
    p(f"[{NOM_ENV[E]}] logements des particuliers : part nationale {r_['paye_logements_fr']:.2f} Md€ France entière"
      f" ({r_['paye_logements_champ']:.2f} sur le champ) ; hausse moyenne {r_['moyenne']:+.0f} € ({r_['moyenne_pct']:+.0f} %) ;"
      f" par dixième de prix (€) " + " ".join(f"{u:+.0f}" for u in r_["dtf"]) + " ; (%) "
      + " ".join(f"{u:+.0f}" for u in r_["dtf_pct"]))
    p(f"[{NOM_ENV[E]}]   hausse − baisse des droits rapportée au parc (€/an) : " + " ".join(f"{u:+.0f}" for u in r_["net_parc"])
      + f" ; taxe/valeur (%) " + " ".join(f"{u:.2f}" for u in r_["tfv"]))
    p(f"[{NOM_ENV[E]}]   > +300 € : {100*r_['plus300']:.0f} % ; > +600 € : {100*r_['plus600']:.0f} % ; baisse :"
      f" {100*r_['baisse']:.0f} % ; taxe qui double : {100*r_['double']:.1f} % ; Paris {r_['paris_pct']:+.0f} %"
      f" (appartement médian {r_['paris_a']:+.0f} €) ; maisons {r_['maisons']:+.0f} €, appartements {r_['apparts']:+.0f} € ;"
      f" P50 {r_['pctl'][50]:+.0f}, P90 {r_['pctl'][90]:+.0f}, P99 {r_['pctl'][99]:+.0f} € ; impôt sur le bâti"
      f" {r_['impot_bati']:.1f} Md€")
BATI0 = float((W * L.tf0 * (1 - L.lam)).sum() / 1e9)
p(f"[BÂTI] impôt sur le bâti des logements aujourd'hui {BATI0:.1f} Md€ (champ) ; part communale seule à la base sol +"
  f" bâti/4 : {float((W * L.codgeo.map(TC_COM) * L.v * (1 - L.lam) / K).sum() / 1e9):.1f} Md€")
J["dec_pm2"] = [float(u) for u in L.groupby("dec_prix").pm2.median()]
J["tfv_auj"] = [float(u) for u in 100 * ratio_decile(L.tf0, L.v)]
J["logements"] = {NOM_ENV[E]: v for E, v in RES.items()}

# =====================================================================================================================
# 4. CAPITALISATION : perte de valeur des propriétaires actuels (hausse de taxe capitalisée ; baisse des droits à
#    l'acheteur, cas central asymétrique de synthese/calculs_foncier.py)
# =====================================================================================================================
p()
p("=" * 110)
p("4. CAPITALISATION")
p("=" * 110)
VAL_INSEE_MEN = float(ter.loc["S14", "N2111"] + ter.loc["S14", "N111"])
CAP = {}
for E in ENV:
    tf1, _, _ = logements(E)
    dv = -(tf1 - L.tf0) / R
    tot_men = E * PART_MEN_LOG / R                         # France entière, logements des ménages
    pct = dv / L.v
    CAP[E] = dict(total_tous=E / R, total_tous_r4=E / 0.04, logements_menages=tot_men,
                  pct_logements=100 * tot_men / VAL_INSEE_MEN, autres=E * (1 - PART_MEN_LOG) / R,
                  paris_a=float(dv[PARIS_A].iloc[0]), paris_a_pct=float(100 * pct[PARIS_A].iloc[0]),
                  p5=float(100 * qpond(pct, 0.05)), plus5=float(W[pct < -0.05].sum() / NLOG),
                  plus10=float(W[pct < -0.10].sum() / NLOG), gagnants=float(W[pct > 0].sum() / NLOG),
                  par_decile_pct=[float(u) for u in 100 * ratio_decile(dv, L.v)],
                  symetrique=(E - DEMI) / R)
    v = CAP[E]
    p(f"[CAP {NOM_ENV[E]}] valeur actuelle de la hausse (r = 3 %) : {v['total_tous']:.0f} Md€ pour tous les propriétaires"
      f" (r = 4 % : {v['total_tous_r4']:.0f}), dont logements des ménages {v['logements_menages']:.0f} Md€"
      f" ({v['pct_logements']:.1f} % de leur valeur, Insee) ; appartement parisien médian {v['paris_a']:+,.0f} €"
      f" ({v['paris_a_pct']:+.1f} %) ; 5e centile {v['p5']:+.1f} % ; logements perdant > 5 % {100*v['plus5']:.0f} %,"
      f" > 10 % {100*v['plus10']:.1f} % ; gagnants {100*v['gagnants']:.0f} % ; par dixième (%) "
      + " ".join(f"{u:+.1f}" for u in v["par_decile_pct"])
      + f" ; si la baisse des droits se capitalise aussi : {v['symetrique']:+.0f} Md€ net")
J["capitalisation"] = {NOM_ENV[E]: v for E, v in CAP.items()}

# =====================================================================================================================
# 5. TRAJECTOIRE 2027-2040
# =====================================================================================================================
p()
p("=" * 110)
p("5. TRAJECTOIRE")
p("=" * 110)
# Calendrier [C] : loi votée en 2027 (valeurs de référence au 1/1/2028), premier avis de la nouvelle taxe à l'automne
# 2029 ; part nationale (et passage de la part communale à la nouvelle base) en trois tiers : 2029, 2030, 2031 ; taux des
# droits baissé au 1er janvier des mêmes années : 5,81 → 4,84 → 3,87 → 2,90 %. Clause : chaque palier de baisse ne
# s'applique que si le palier de taxe correspondant est mis en recouvrement la même année.
PHI = 0.03          # part des ventes annuelles décalée de décembre à janvier par point de baisse annoncée [H]
                    # (Bérard et Trannoy 2018 : +26 % de ventes le mois précédant une hausse de 0,7 point)
I_REP = 0.03        # intérêt du report (taux d'emprunt de l'État, nominal) [C]
H_REP = 1 / 15      # part du stock remboursée chaque année (vente, succession) [H]
ELIG = 0.25         # part des hausses des propriétaires occupants due par des ménages éligibles (revenus modestes) [H]
RECOURS = 0.5       # recours au report parmi les éligibles (report proposé sur l'avis, sur simple acceptation) [H]
DED_IS, DED_BAIL = 0.20, 0.25   # taux effectifs de déduction : IS des entreprises (25 % × ~80 % bénéficiaires) ;
                                # bailleurs au réel (IR + prélèvements sociaux ≈ 40 % × ~60 % au réel) [H]


def trajectoire(E, debut=2029, n=3, dmto_en_une_fois=None):
    """Table annuelle {année: {poste: Md€}}. dmto_en_une_fois = année de la baisse unique (variante)."""
    pas = {a: min(max(a - debut + 1, 0), n) / n for a in ANS}
    if dmto_en_une_fois:
        pas_d = {a: 1.0 if a >= dmto_en_une_fois else 0.0 for a in ANS}
    else:
        pas_d = pas
    taux = {a: T * (1 - 0.5 * pas_d[a]) for a in ANS}            # taux total des droits
    taux[ANS[0] - 1] = T
    out, ind = {}, {}
    stock = 0.0
    hausse_po = RES[E]["hausse_po_fr"]
    for a in ANS:
        f = pas[a]
        tf = E * f
        dmto = -DEMI * pas_d[a]
        # décalage des ventes autour de chaque palier (ventes perdues l'année a au taux a, retrouvées l'année a+1)
        d_pts_suiv = 100 * (taux[a] - taux.get(a + 1, taux[a])) if a + 1 in taux else 0.0
        d_pts = 100 * (taux[a - 1] - taux[a])
        perdu = PHI * d_pts_suiv * D_FR * taux[a] / T
        retrouve = PHI * d_pts * D_FR * taux[a] / T
        cal = -perdu + retrouve
        nouveau = ELIG * RECOURS * hausse_po * f
        rembourse = H_REP * stock * (1 + I_REP)
        stock = stock * (1 + I_REP) + nouveau - rembourse
        rep = -(nouveau - rembourse)
        # déductibilité (année suivante) : part des entreprises à l'IS et des bailleurs au réel
        f_prec = pas.get(a - 1, 0.0)
        ded = -f_prec * (DED_IS * E * PART_ENTR_IS + DED_BAIL * max(RES[E]["hausse_bailleurs_fr"], 0))
        net = tf + dmto + cal + rep + ded
        out[a] = dict(taxe_fonciere_nouvelle=round(tf, 3), dmto=round(dmto, 3), calendrier_ventes=round(cal, 3),
                      report_paiement=round(rep, 3), deductibilite_is_ir=round(ded, 3), net=round(net, 3))
        ind[a] = dict(stock_report=round(stock, 3), taux_dmto_pct=round(100 * taux[a], 2), part_taxe=round(f, 3),
                      taux_national_sol_pct=round(eq[E]["tn"] * f, 4) if E in eq else None)
    return out, ind


TRAJ, IND = {}, {}
for E in [10.0, 15.0, 20.0]:
    TRAJ[NOM_ENV[E]], IND[NOM_ENV[E]] = trajectoire(E)
TRAJ["substitution"], IND["substitution"] = trajectoire(ENV[0])
TRAJ["E15_baisse_unique_2030"], IND["E15_baisse_unique_2030"] = trajectoire(15.0, dmto_en_une_fois=2030)
TRAJ["E15_glissement_un_an"], IND["E15_glissement_un_an"] = trajectoire(15.0, debut=2030)
for nom, tab in TRAJ.items():
    p(f"[TRAJ {nom}] " + " ; ".join(f"{a} : TF {v['taxe_fonciere_nouvelle']:+.1f}, droits {v['dmto']:+.1f}, calendrier"
                                    f" {v['calendrier_ventes']:+.2f}, report {v['report_paiement']:+.2f}, déduction"
                                    f" {v['deductibilite_is_ir']:+.2f} → net {v['net']:+.2f}"
                                    for a, v in tab.items() if a in (2028, 2029, 2030, 2031, 2032, 2035, 2040)))
    nets = [v["net"] for v in tab.values()]
    p(f"[TRAJ {nom}]   année la plus basse {min(nets):+.2f} Md€ ; régime permanent (2040) {nets[-1]:+.2f} ; cumul"
      f" 2027-2040 {sum(nets):+.1f} ; stock de report 2040 {IND[nom][2040]['stock_report']:.1f} Md€")
J["annuel"] = TRAJ["E15"]                      # trajectoire recommandée (enveloppe de 15 Md€, trois paliers 2029-2031)
J["annuel_par_scenario"] = TRAJ
J["indicateurs_annuels"] = IND
J["hypotheses_trajectoire"] = dict(phi=PHI, interet_report=I_REP, remboursement=H_REP, eligibles=ELIG, recours=RECOURS,
                                   deduction_is=DED_IS, deduction_bailleurs=DED_BAIL, premier_avis=2029, paliers=3)
# Coûts par point de paramètre pour le bouclage
J["par_point"] = dict(md_par_point_dmto=D_FR / (100 * T),
                      md_par_0_01pt_taux_national=float(0.0001 * equilibre(15.0)["base"]),
                      net_permanent_par_md_enveloppe=(TRAJ["E20"][2040]["net"] - TRAJ["E10"][2040]["net"]) / 10)
p(f"[PAR POINT] 1 point de droits = {D_FR/(100*T):.2f} Md€ ; 0,01 point de taux national sur le sol (bâti 0,0025) ="
  f" {0.0001*equilibre(15.0)['base']:.2f} Md€ (base après capitalisation, E = 15)")

# =====================================================================================================================
# 6. CAS-TYPES : quatre achats, Massy, mobilité professionnelle
# =====================================================================================================================
p()
p("=" * 110)
p("6. CAS-TYPES")
p("=" * 110)
TX_DEP_2026 = {"91": 0.050, "69": 0.050, "45": 0.050}     # tableau DGFiP au 1/6/2026 (majoration, hors primo-accédants)


def taux_2026(dep, primo):
    d = 0.045 if primo else TX_DEP_2026.get(dep, 0.045)
    return d + 0.012 + 0.0237 * d


E_REC = 15.0
tf_rec, nat_rec, _ = logements(E_REC)
tf_10, _, _ = logements(10.0)
PROJETS = [  # (clé, libellé, commune, type, surface m², primo-accédant)
    ("orleans", "Appartement 3 pièces, Orléans (ville moyenne)", "45234", "a", 65, True),
    ("lyon", "Appartement familial 4 pièces, Lyon (métropole régionale)", "69123", "a", 80, False),
    ("massy", "Appartement 3 pièces, Massy (couronne parisienne)", "91377", "a", 65, True),
    ("sgdb", "Maison familiale 5 pièces, Sainte-Geneviève-des-Bois (Essonne)", "91549", "m", 100, False),
]
CAS = []
for cle, lab, code, t, surf, primo in PROJETS:
    i = idx(code, t)
    pm2 = float(c.loc[code, f"{t}_pm2"])
    prix = round(pm2 * surf, -3)
    k = prix / L.v[i]
    dep = code[:2]
    d26 = taux_2026(dep, primo) * prix
    dperm = T * prix
    dapres = T / 2 * prix
    row = dict(cle=cle, cas=lab, commune=code, prix=prix, prix_m2=pm2, surface=surf, primo=primo,
               taux_2026=100 * taux_2026(dep, primo), dmto_2026=d26, dmto_permanent=dperm, dmto_apres=dapres,
               economie=dperm - dapres, economie_vs_2026=d26 - dapres,
               tf_actuelle=float(L.tf0[i] * k), dtf=float((tf_rec[i] - L.tf0[i]) * k),
               dtf_nat=float(nat_rec[i] * k), dtf_10=float((tf_10[i] - L.tf0[i]) * k), terrain=float(L.lam[i]))
    row["annees_equivalentes"] = row["economie"] / row["dtf"] if row["dtf"] > 0 else None
    row["net_7ans"] = row["economie"] - row["dtf"] * (1 - (1 + R) ** -7) / R
    row["perte_valeur_proprietaire"] = -row["dtf"] / R
    CAS.append(row)
    p(f"[CAS] {lab} : {surf} m² à {fr(pm2)} €/m² (DVF 2023-2024) = {fr(prix)} € ; droits 2026"
      f" {fr(d26)} € ({100*taux_2026(dep, primo):.2f} %{', primo-accédant' if primo else ''}) ; taux permanent {fr(dperm)} € ;"
      f" après réforme {fr(dapres)} € ; économie {fr(row['economie'])} € ; taxe foncière {fr(row['tf_actuelle'])} € →"
      f" {row['dtf']:+.0f} €/an (E = 15 ; E = 10 : {row['dtf_10']:+.0f}) ; l'économie vaut"
      f" {row['annees_equivalentes'] or 0:.0f} ans de hausse ; bilan actualisé après 7 ans {row['net_7ans']:+,.0f} € ;"
      f" perte de valeur d'un propriétaire en place {row['perte_valeur_proprietaire']:+,.0f} €")
J["cas"] = CAS
# Mobilité professionnelle : famille propriétaire à Orléans (maison 100 m²) qui accepte un poste mieux payé en Essonne et
# achète la maison de Sainte-Geneviève-des-Bois ; les droits sont dus sur l'achat.
i_o = idx("45234", "m")
prix_o = round(float(c.loc["45234", "m_pm2"]) * 100, -3)
mais = CAS[3]
mob = dict(vend=prix_o, achete=mais["prix"], droits_2026=taux_2026("91", False) * mais["prix"],
           droits_permanent=mais["dmto_permanent"], droits_apres=mais["dmto_apres"])
mob["economie"] = mob["droits_permanent"] - mob["droits_apres"]
mob["hausse_mensuelle_equiv_6ans_avant"] = mob["droits_permanent"] / 72
mob["hausse_mensuelle_equiv_6ans_apres"] = mob["droits_apres"] / 72
mob["dtf_orleans_quittee"] = float((tf_rec[i_o] - L.tf0[i_o]) * prix_o / L.v[i_o])
p(f"[MOBILITÉ] famille qui vend sa maison d'Orléans ({fr(prix_o)} €) pour un poste en Essonne et achète {fr(mais['prix'])} € :"
  f" droits {fr(mob['droits_2026'])} € en 2026 (6,32 %), {fr(mob['droits_permanent'])} € au taux permanent,"
  f" {fr(mob['droits_apres'])} € après réforme ; il faut aujourd'hui {fr(mob['hausse_mensuelle_equiv_6ans_avant'])} € de"
  f" hausse de salaire net par mois pendant six ans pour payer les seuls droits, {fr(mob['hausse_mensuelle_equiv_6ans_apres'])}"
  f" € après réforme")
J["mobilite"] = mob

# =====================================================================================================================
# 7. GAINS : ventes, mobilité, perte sèche (indicateurs d'efficacité, pas de PIB)
# =====================================================================================================================
p()
p("=" * 110)
p("7. GAINS")
p("=" * 110)
N_VENTES_FR = c.ventes_an.sum() / F_2324                  # ventes de logements anciens, France entière (ordre de grandeur)
V_VENTES_FR = V_VENTES / F_2324 / 1e9
gain = {}
for s, v in SIG.items():
    if s == 0:
        continue
    dv = (1 + v) ** (100 * T / 2) - 1
    tri = s * V_VENTES_FR * ((T / 2) ** 2 - T ** 2) / 2      # σ % par point = σ par unité de taux (triangle)
    gain[s] = dict(ventes_pct=100 * dv, ventes_sup=dv * N_VENTES_FR, perte_seche_ventes=tri)
    p(f"[VENTES σ = {s} %/pt] ventes durablement +{100*dv:.0f} % (≈ {dv*N_VENTES_FR/1e3:.0f} 000 par an, France entière) ;"
      f" perte sèche sur les ventes de logements {tri:+.2f} Md€")
# autres immeubles (σ = 6 transposé)
V_AUT = D_AUT_FR / T
tri_aut = 6 * V_AUT * ((T / 2) ** 2 - T ** 2) / 2
p(f"[VENTES] autres immeubles (σ = 6 transposé, {V_AUT:.0f} Md€ de ventes) : {tri_aut:+.2f} Md€ (ordre de grandeur)")
# Bâti : triangle de Harberger sur l'impôt sur le bâti des logements (méthode de synthese/calculs_foncier.py)
K_BATI = float((W * L.v * (1 - L.lam)).sum() / 1e9)
U = 0.045


def tri_bati(b1, eps=1.0, u=U, b0=BATI0):
    return eps * (K_BATI / u) * ((b1 / K_BATI) ** 2 - (b0 / K_BATI) ** 2) / 2


for E in ENV:
    gain.setdefault("bati", {})[NOM_ENV[E]] = tri_bati(RES[E]["impot_bati"]) / PART_CHAMP
    p(f"[BÂTI {NOM_ENV[E]}] impôt sur le bâti des logements {BATI0:.1f} → {RES[E]['impot_bati']:.1f} Md€ (champ) ;"
      f" perte sèche {tri_bati(RES[E]['impot_bati'])/PART_CHAMP:+.2f} Md€ France entière (ε = 1, u = 4,5 %)")
gain["autres_immeubles"] = tri_aut
# Mobilité des propriétaires [E, transposé] : Eerola et al. (2021) −5,6 % pour +0,5 point ; van Ommeren et van
# Leuvensteijn (2005) −8 à −13 % par point de coûts de transaction : extrapolation à −2,9 points non établie
mob_g = {"bas": 0.0, "pays_bas_bas": (1.08 ** (100 * T / 2) - 1), "pays_bas_haut": (1.13 ** (100 * T / 2) - 1)}
p(f"[MOBILITÉ] mobilité des propriétaires : de 0 (aucun effet durable, lecture de Bérard et Trannoy) à"
  f" +{100*mob_g['pays_bas_bas']:.0f} / +{100*mob_g['pays_bas_haut']:.0f} % si elle réagit comme aux Pays-Bas"
  f" (8 à 13 % par point, extrapolé à 2,9 points)")
gain["mobilite_proprietaires_pct"] = {k: 100 * v for k, v in mob_g.items()}
# Calendrier : effets temporaires à chaque palier
p(f"[TEMPORAIRE] chaque palier de 0,97 point décale ≈ {100*PHI*100*T/6:.1f} % des ventes annuelles de décembre à janvier"
  f" ({PHI*100*T/6*N_VENTES_FR/1e3:.0f} 000 ventes) ; une baisse unique de 2,9 points en décalerait ≈"
  f" {100*PHI*100*T/2:.0f} % ({PHI*100*T/2*N_VENTES_FR/1e3:.0f} 000), sur une attente plus longue : pas un gain")
J["gains"] = gain

# Coût d'un déménagement (indicateur concret) : droits sur l'achat du logement médian des ventes
PRIX_MED = float(np.average(L.v, weights=W))
p(f"[DÉMÉNAGEMENT] droits sur l'achat d'un logement de {fr(round(PRIX_MED,-3))} € (valeur moyenne du parc du modèle) :"
  f" {fr(T*PRIX_MED)} € → {fr(T/2*PRIX_MED)} €")
J["demenagement"] = dict(prix=PRIX_MED, avant=T * PRIX_MED, apres=T / 2 * PRIX_MED)

# Schéma g6 : deux terrains de même valeur, l'un nu, l'autre bâti (valeurs illustratives)
SOL_G6, BATI_G6 = 200_000, 600_000
t_uni = TAU0                                       # taux unique sur la valeur totale (≈ taxe actuelle / valeur)
tot = t_uni * (2 * SOL_G6 + BATI_G6)
t_sol = tot / (2 * SOL_G6 + BATI_G6 / K)
g6 = dict(sol=SOL_G6, bati=BATI_G6, taux_unique=100 * t_uni, taux_sol=100 * t_sol, taux_bati=100 * t_sol / K,
          unique_nu=t_uni * SOL_G6, unique_bati=t_uni * (SOL_G6 + BATI_G6),
          double_nu=t_sol * SOL_G6, double_bati=t_sol * SOL_G6 + t_sol / K * BATI_G6)
p(f"[G6] terrain de {fr(SOL_G6)} € nu ou portant un immeuble de {fr(BATI_G6)} € : taux unique {100*t_uni:.3f} % → nu"
  f" {g6['unique_nu']:.0f} €, bâti {g6['unique_bati']:.0f} € (écart {g6['unique_bati']-g6['unique_nu']:.0f}) ; double taux"
  f" (sol {100*t_sol:.3f} %, bâti {100*t_sol/K:.3f} %, même recette) → nu {g6['double_nu']:.0f} €, bâti"
  f" {g6['double_bati']:.0f} € (écart {g6['double_bati']-g6['double_nu']:.0f})")
J["g6"] = g6

(OUT / "foncier_journal.txt").write_text("\n".join(lignes) + "\n", encoding="utf-8")


def _js(o):
    if isinstance(o, dict):
        return {str(k): _js(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [_js(v) for v in o]
    if isinstance(o, (np.floating, np.integer)):
        return float(o)
    if isinstance(o, np.bool_):
        return bool(o)
    return o


(OUT / "foncier.json").write_text(json.dumps(_js(J), ensure_ascii=False, indent=1), encoding="utf-8")
