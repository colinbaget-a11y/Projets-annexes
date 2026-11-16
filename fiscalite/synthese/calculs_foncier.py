"""Calculs de la partie Immobilier de la note fusionnée (refonte du 16/11/2026, CHARTE_NOTE.md, DECISIONS.md).

Reprend le modèle de foncier/simulation.py (importé, non modifié) et ajoute ce que demande la nouvelle architecture :
qui paie aujourd'hui, réforme naïve, proposition à assiette large (tous les terrains privés, d'après les comptes de
patrimoine de l'Insee par secteur), capitalisation et valeur actualisée, report de paiement, arbitrages, cas-types,
transition sur 3, 5 et 10 ans, compensation des collectivités. Les hypothèses fortes sont celles de
revue/hypotheses_foncier.md (H1 à H19) ; les quatre erreurs du texte précédent y sont corrigées (§ 5.2).

Lancer depuis fiscalite/ : python3 synthese/calculs_foncier.py
  -> synthese/sorties/calculs_foncier.txt (journal lisible) et calculs_foncier.json (séries pour les figures)

Conventions : euros de 2024 ; « Md€ » = milliards par an ; σ = baisse des ventes par point de droits (6 = 6 %) ;
r = taux d'actualisation réel (3 %, 4 % en variante) ; perte sèche négative = perte sèche évitée (gain).
"""
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
RACINE = HERE.parent
OUT = HERE / "sorties"
OUT.mkdir(exist_ok=True)
sys.path[:0] = [str(RACINE / "foncier")]
import simulation as sm  # noqa: E402  (modèle de la partie ; son bloc __main__ ne s'exécute pas)

L, c = sm.L, sm.c
W = L.n
NLOG = W.sum()
T = sm.TAUX_DMTO
TF0, D0, VAL, TERRE = sm.TF0, sm.D0, sm.VAL, sm.TERRE
R_ACT = 0.03
J = {}
lignes = []


def p(s=""):
    print(s, flush=True)
    lignes.append(s)


def fr(x, d=0):
    return f"{x:,.{d}f}".replace(",", " ").replace(".", ",")


def quantile_pondere(x, q):
    o = x.sort_values()
    cw = W[o.index].cumsum() / NLOG
    return float(o[cw >= q].iloc[0])


def par_decile(serie):
    return ((W * serie).groupby(L.dec_prix).sum() / W.groupby(L.dec_prix).sum()).values


def ratio_decile(num, den):
    return ((W * num).groupby(L.dec_prix).sum() / (W * den).groupby(L.dec_prix).sum()).values


PARIS = (L.codgeo == "75056")
PARIS_A = PARIS & (L.type == "a")


def idx(code, t):
    return L[(L.codgeo == code) & (L.type == t)].index[0]


# =====================================================================================================================
# 1. SITUATION ACTUELLE
# =====================================================================================================================
p("=" * 100)
p("1. SITUATION ACTUELLE")
p("=" * 100)
p(f"[CHAMP] {NLOG/1e6:.1f} M logements des particuliers (métropole hors Alsace-Moselle) ; valeur {fr(VAL/1e9)} Md€ ;"
  f" terrain {fr(TERRE/1e9)} Md€ ({100*TERRE/VAL:.1f} %) ; taxe foncière {TF0/1e9:.1f} Md€ ({TF0/NLOG:.0f} € par"
  f" logement, {100*TF0/VAL:.3f} % de la valeur) ; droits {D0/1e9:.2f} Md€ (taux {100*T:.2f} %)")
V_VENTES = c.valeur_ventes_an.sum()
N_VENTES = c.ventes_an.sum()
p(f"[DROITS] ventes de logements anciens {V_VENTES/1e9:.0f} Md€ par an, {N_VENTES/1e3:.0f} 000 ventes ; rotation"
  f" {100*N_VENTES/NLOG:.1f} % du parc par an ; droits rapportés au parc : {D0/NLOG:.0f} € par logement et par an,"
  f" soit {100*D0/VAL:.3f} % de la valeur par an (coin implicite sur la détention)")

# Inventaire 2024 (foncier/notes/inventaire.md, valeurs [TEXTE LU] ; successions : clé de 60 % [NON VÉRIFIÉ])
INV = {"Détention": [("Taxe foncière bâtie : logements", 30.5), ("Taxe foncière bâtie : autres locaux", 11.5),
                     ("Ordures ménagères (TEOM)", 9.0), ("Cotisation foncière des entreprises", 8.0),
                     ("Autres (TH résiduelles, IFI, foncier non bâti…)", 10.0)],
       "Ventes": [("Droits de mutation", 14.1), ("TVA du neuf et des terrains", 7.1),
                  ("Plus-values, sécurité immobilière", 3.8)],
       "Transmissions": [("Successions et donations, part immobilière (estimation)", 12.5)],
       "Loyers": [("Impôts sur les revenus locatifs", 8.4)],
       "Construction": [("Taxe d'aménagement", 1.5)]}
tot_inv = sum(v for f in INV.values() for _, v in f)
PIB24 = pd.read_csv(RACINE / "lvt/donnees/patrimoine.csv", index_col=0).loc[2024, "pib"] / 1e3   # Md€ (Insee)
p(f"[INVENTAIRE 2024] total {tot_inv:.1f} Md€ = {100*tot_inv/PIB24:.2f} % du PIB ({fr(PIB24)} Md€, Insee) ; "
  + " ; ".join(f"{k} {sum(v for _, v in f):.1f}" for k, f in INV.items()))
J["inventaire"] = INV

# Qui paie la taxe foncière : statut d'occupation (prorata communal, même taxe par logement dans la commune)
st = pd.DataFrame({"Propriétaires occupants": c.rp_prop, "Logements loués par des particuliers": (c.rp_loc - c.rp_lochlmv).clip(lower=0),
                   "Résidences secondaires": c.rsecocc, "Logements vacants": c.logvac, "Logés gratuitement": c.rp_grat}).fillna(0)
part_st = st.div(st.sum(axis=1).replace(0, np.nan), axis=0).fillna(0)
tf_com = c.n_m * c.tf_m + c.n_a * c.tf_a
qui = {k: float((tf_com * part_st[k]).sum() / 1e9) for k in st}
p("[QUI PAIE] taxe foncière par statut d'occupation (Md€) : " + " ; ".join(f"{k} {v:.1f} ({100*v*1e9/TF0:.0f} %)"
                                                                      for k, v in qui.items()))
J["qui_paie"] = qui

# Taux rapporté à la valeur, par décile de prix au m² et dans quelques villes
dec_auj = 100 * ratio_decile(L.tf0, L.v)
pm2_dec = L.groupby("dec_prix").pm2.median().values
p("[TAUX] taxe foncière / valeur par décile de prix au m² (%) : " + " ".join(f"{u:.2f}" for u in dec_auj))
p("[TAUX] prix médian au m² par décile : " + " ".join(fr(u) for u in pm2_dec))
J["dec_pm2"] = [float(u) for u in pm2_dec]
J["tfv_auj"] = [float(u) for u in dec_auj]
VILLES = {"75056": "Paris", "69123": "Lyon", "13055": "Marseille", "31555": "Toulouse", "06088": "Nice",
          "44109": "Nantes", "33063": "Bordeaux", "59350": "Lille", "93066": "Saint-Denis", "42218": "Saint-Étienne",
          "87085": "Limoges", "23096": "Guéret", "19272": "Ussel", "74010": "Annecy", "33009": "Arcachon"}
tv = {}
for code, nom in VILLES.items():
    m = L.codgeo == code
    if m.any():
        tv[nom] = float(100 * (W * L.tf0)[m].sum() / (W * L.v)[m].sum())
p("[TAUX] taxe foncière / valeur dans quelques communes (%) : " + " ; ".join(f"{k} {v:.2f}" for k, v in tv.items()))
J["tfv_villes"] = tv
r_log = L.tf0 / L.v
p(f"[TAUX] part des logements dont la taxe dépasse 0,5 % de la valeur : {100*W[r_log > 0.005].sum()/NLOG:.0f} % ;"
  f" sous 0,2 % : {100*W[r_log < 0.002].sum()/NLOG:.0f} %")
# Dispersion à l'intérieur des villes (Insee Analyses n° 91, fig. 3a-3e, IRIS, 2017 : revue/hypotheses_foncier.md H1)
p("[TAUX, H1] à l'intérieur des villes (IA 91, IRIS, 2017) : Paris 0,074 % (1er décile) à 0,121 % (9e) ; agglomération"
  " lyonnaise 0,25 à 0,52 % ; rapport 9e/1er décile : Paris 1,64, Lyon 2,09, Toulouse 1,76, Lille 1,52")
# Par taille de commune
g = L.assign(w=W, tf=W * L.tf0, v=W * L.v, d=W * L.d0).groupby("taille", observed=True).sum(numeric_only=True)
p("[TAILLE] " + " ; ".join(f"{i} : TF {r.tf/r.w:.0f} €/log., {100*r.tf/r.v:.2f} % de la valeur, droits {r.d/r.w:.0f} €/log./an"
                           for i, r in g.iterrows()))

# Droits payés à l'achat du logement médian, et poids dans l'apport
APPORT = 0.153   # 1 − LTV moyenne de 84,7 % (CCSF 2026, d'après foncier/notes/droits_mutation.md ; non relu ici)
p(f"[ACHAT] droits = {100*T:.2f} % du prix, soit {100*T/APPORT:.0f} % d'un apport moyen de {100*APPORT:.0f} % du prix ;"
  f" la baisse de moitié ({100*T/2:.1f} points) représente {100*T/2/0.20:.1f} % d'un apport de 20 % et {100*T/2/0.10:.0f} %"
  f" d'un apport de 10 %")

# Comparaison internationale (OCDE, Revenue Statistics ; vérifiée : revue/verif_litterature_foncier.md n° 1)
oc = pd.read_csv(RACINE / "donnees/recettes_ocde_pct_pib.csv")
PAYS = ["France", "Royaume-Uni", "États-Unis", "Belgique", "Italie", "Espagne", "Danemark", "Pays-Bas", "Allemagne",
        "Moyenne OCDE"]
ocd = {}
for pays in PAYS:
    x = oc[(oc.pays == pays) & (oc.annee == 2023)].set_index("categorie").pct_pib
    ocd[pays] = (float(x["T_4100"]), float(x["T_4400"]))
p("[OCDE 2023] impôts périodiques sur l'immobilier / sur les transactions (% du PIB) : "
  + " ; ".join(f"{k} {a:.2f} / {b:.2f}" for k, (a, b) in ocd.items()))
J["ocde"] = ocd

# Cycle des droits sur les logements (Compte du logement 2025, série T321 [TEXTE LU] : foncier/notes/inventaire.md § 3)
CYCLE = {2021: 16.418, 2022: 16.818, 2023: 13.002, 2024: 11.239, 2025: 13.568}
TF_LOG = {2024: 30.489, 2025: 31.590}
p("[CYCLE] droits sur les logements (Md€) : " + " ; ".join(f"{a} {v:.1f}" for a, v in CYCLE.items())
  + f" ; de 2022 à 2024 : {100*(CYCLE[2024]/CYCLE[2022]-1):+.0f} % ; taxe foncière sur les logements 2024 {TF_LOG[2024]:.1f},"
  f" 2025 {TF_LOG[2025]:.1f}")
J["cycle"] = CYCLE

# Coût marginal d'un euro de droits (réaction exponentielle des ventes, σ par point) : dPS/dR = σ'τ / (1 − σ'τ)
for sig in (3, 6, 8):
    a = sig * 100 * T / 100   # σ' τ, σ' = σ % par point = 100σ par unité
    p(f"[COUT MARGINAL] σ = {sig} : le dernier euro de droits coûte {a/(1-a):.2f} € de perte sèche (contre 0 pour un impôt"
      f" sur le sol)")

# =====================================================================================================================
# 2-3. RÉFORME NAÏVE (droits −50 %, taxe actuelle relevée du même pourcentage partout)
# =====================================================================================================================
p()
p("=" * 100)
p("3. RÉFORME NAÏVE")
p("=" * 100)
S = 0.5
d1 = (1 - S) * L.d0
naif_tf, _ = sm.report_tf(S)
d_naif = naif_tf - L.tf0
hausse_naif = S * D0 / TF0
p(f"[NAÏF] taxe foncière relevée de {100*hausse_naif:.1f} % partout ({S*D0/1e9:.2f} Md€) ; 19,7 % si les ventes"
  f" augmentent de 6 % par point")
J["naif_dtf"] = [float(u) for u in par_decile(d_naif)]
J["naif_tot"] = [float(u) for u in par_decile(d_naif + d1 - L.d0)]
J["tfv_naif"] = [float(u) for u in 100 * ratio_decile(naif_tf, L.v)]
p("[NAÏF] variation de taxe foncière par décile (€/an) : " + " ".join(f"{u:+.0f}" for u in J["naif_dtf"]))
p("[NAÏF] taxe foncière moins droits (moyenne du parc, €/an) : " + " ".join(f"{u:+.0f}" for u in J["naif_tot"]))
p("[NAÏF] taxe / valeur par décile (%) : " + " ".join(f"{u:.2f}" for u in J["tfv_naif"]))
p(f"[NAÏF] logements dont la taxe monte de plus de 300 € : {100*W[d_naif > 300].sum()/NLOG:.0f} % ; Paris appartement"
  f" médian {float(d_naif[PARIS_A].iloc[0]):+.0f} €")
gt = L.assign(a=W * (d_naif + d1 - L.d0), w=W).groupby("taille", observed=True).sum(numeric_only=True)
p("[NAÏF] taxe moins droits par taille de commune (€/an) : " + " ; ".join(f"{i} {r.a/r.w:+.0f}" for i, r in gt.iterrows()))

# =====================================================================================================================
# 4. PROPOSITION : deux taux par commune + taux national sur la valeur de TOUS les terrains privés
# =====================================================================================================================
p()
p("=" * 100)
p("4. PROPOSITION")
p("=" * 100)
ter = pd.read_csv(RACINE / "foncier/donnees/terrains_secteurs_2024.csv", comment="#").set_index("secteur")
BATI_MEN = ter.loc["S14", "N2111"]                                   # sol sous les bâtiments des ménages
BATI_AUT = ter.loc[["S11", "S12", "S15"], "N2111"].sum()            # sol des entreprises, sociétés financières, ISBLSM
NU_PRIV = ter.loc[["S11", "S14"], "N2119"].sum()                     # terrains non bâtis privés (à bâtir, naturels)
AGRI = ter.loc["S1", "N2112"]                                        # terres cultivées
PUBLIC = ter.loc["S13", ["N2111", "N2113", "N2119"]].sum()
BASES = {"sol des logements seul": BATI_MEN, "terrains bâtis privés": BATI_MEN + BATI_AUT,
         "tous terrains privés hors terres agricoles": BATI_MEN + BATI_AUT + NU_PRIV,
         "tous terrains privés, terres agricoles comprises": BATI_MEN + BATI_AUT + NU_PRIV + AGRI}
p(f"[INSEE 2024] sol sous les bâtiments des ménages {fr(BATI_MEN)} Md€ ; des entreprises et autres privés {fr(BATI_AUT)} ;"
  f" terrains non bâtis privés {fr(NU_PRIV)} ; terres cultivées {fr(AGRI)} ; terrains publics {fr(PUBLIC)} (exclus)")
# Logements HLM : sol estimé dans le modèle (valeur médiane des logements de la commune : majorant)
hlm = c.rp_lochlmv.fillna(0)
tot_ma = (c.maison + c.appart).replace(0, np.nan)
hlm_terre_mod = ((hlm * c.maison / tot_ma).fillna(0) * c.v_m * c.l_m + (hlm * c.appart / tot_ma).fillna(0) * c.v_a * c.l_a).sum()
RATIO_INSEE = BATI_MEN * sm.part_champ / (TERRE / 1e9)   # valeurs Insee / valeurs du modèle (sol des logements, champ)
hlm_terre = hlm_terre_mod / 1e9 * RATIO_INSEE / sm.part_champ
p(f"[HLM] sol des {hlm.sum()/1e6:.1f} M logements HLM loués, estimé (valeur médiane de la commune, majorant) :"
  f" {fr(hlm_terre)} Md€ en valeurs Insee ; rapport valeurs Insee / modèle : {RATIO_INSEE:.2f}")

# Droits sur les autres biens (locaux, terrains) : total des collectivités (OFGL) − logements (Compte du logement)
DMTO_TOT = {2023: 16.311, 2024: 14.093}
DMTO_AUT = np.mean([DMTO_TOT[a] - CYCLE[a] for a in (2023, 2024)])
F_CHAMP = (D0 / 1e9) / np.mean([CYCLE[2023], CYCLE[2024]])      # droits du modèle / droits France entière (logements)
CUT_LOG = S * D0 / 1e9
CUT_AUT = S * DMTO_AUT * F_CHAMP
p(f"[DROITS AUTRES BIENS] {DMTO_AUT:.2f} Md€ par an en 2023-2024 (différence de deux sources, non vérifiée) ; à l'échelle"
  f" du champ ({F_CHAMP:.3f}) : moitié = {CUT_AUT:.2f} Md€ ; logements : moitié = {CUT_LOG:.2f} Md€")


def part_menages(base):
    return BATI_MEN / base


def proposition(cut, base, k=4, menages_seuls=False):
    """Taxe foncière de chaque logement : part communale à deux taux (terrain = k × bâti, recette constante par commune ;
    k = inf : sol seul) + taux national sur le terrain. Le taux national lève `cut` Md€ sur l'assiette `base` (Md€,
    Insee) ; la part des logements des particuliers est BATI_MEN / base, répartie au prorata de la valeur de leur
    terrain dans le modèle. Rend (taxe, taux national en % de la valeur du terrain dans le modèle)."""
    if np.isfinite(k):
        b = L.v * (L.lam * k + (1 - L.lam))
    else:
        b = L.v * L.lam
    tc = (W * L.tf0).groupby(L.codgeo).sum() / (W * b).groupby(L.codgeo).sum()
    paye_men = cut * 1e9 * (1.0 if menages_seuls else part_menages(base))
    tn = paye_men / TERRE
    return L.codgeo.map(tc) * b + tn * L.v * L.lam, tn, L.codgeo.map(tc) * b - L.tf0


def resume(nom, tf1, d1_, cle=None):
    dtf = tf1 - L.tf0
    dtot = dtf + d1_ - L.d0
    out = dict(dtf=[float(u) for u in par_decile(dtf)], dtf_pct=[float(u) for u in 100 * ratio_decile(dtf, L.tf0)],
               tot=[float(u) for u in par_decile(dtot)], tfv=[float(u) for u in 100 * ratio_decile(tf1, L.v)])
    out["plus300"] = float(W[dtf > 300].sum() / NLOG)
    out["double"] = float(W[dtf > L.tf0].sum() / NLOG)
    out["baisse"] = float(W[dtf < 0].sum() / NLOG)
    out["paris_pct"] = float(100 * (W * dtf)[PARIS].sum() / (W * L.tf0)[PARIS].sum())
    out["paris_a"] = float(dtf[PARIS_A].iloc[0])
    out["pctl"] = {q: quantile_pondere(dtf, q / 100) for q in (10, 25, 50, 75, 90, 95, 99)}
    dbl = dtf > L.tf0
    out["double_paris"] = float(W[dbl & PARIS].sum() / max(W[dbl].sum(), 1))
    m_hp = (L.dec_prix == 9) & ~PARIS
    out["d10_hors_paris_pct"] = float(100 * (W * dtf)[m_hp].sum() / (W * L.tf0)[m_hp].sum())
    ty = L.assign(a=W * dtf, w=W).groupby("type").sum(numeric_only=True)
    out["maisons"], out["apparts"] = float(ty.a["m"] / ty.w["m"]), float(ty.a["a"] / ty.w["a"])
    p(f"[{nom}] ΔTF par décile (€/an) : " + " ".join(f"{u:+.0f}" for u in out["dtf"]))
    p(f"[{nom}] ΔTF par décile (%) : " + " ".join(f"{u:+.0f}" for u in out["dtf_pct"]))
    p(f"[{nom}] ΔTF − baisse des droits rapportée au parc (€/an) : " + " ".join(f"{u:+.0f}" for u in out["tot"]))
    p(f"[{nom}] taxe / valeur (%) : " + " ".join(f"{u:.2f}" for u in out["tfv"]))
    p(f"[{nom}] hausse > 300 € : {100*out['plus300']:.1f} % des logements ; taxe qui double : {100*out['double']:.1f} %"
      f" (dont Paris {100*out['double_paris']:.0f} %) ; baisse : {100*out['baisse']:.0f} % ; Paris {out['paris_pct']:+.0f} %"
      f" (appartement médian {out['paris_a']:+.0f} €) ; dernier décile hors Paris {out['d10_hors_paris_pct']:+.0f} % ;"
      f" maisons {out['maisons']:+.0f} €, appartements {out['apparts']:+.0f} €")
    p(f"[{nom}] distribution de ΔTF (€/an) : " + " ; ".join(f"P{q} {v:+.0f}" for q, v in out["pctl"].items()))
    for seuil in (500, 660, 760, 1000):
        p(f"[{nom}]   logements à plus de +{seuil} €/an : {100*W[dtf > seuil].sum()/NLOG:.1f} %")
    if cle:
        J[cle] = out
    return dtf


BASE_P = BASES["tous terrains privés hors terres agricoles"]
CUT_P = CUT_LOG + CUT_AUT
prop_tf, TN_P, redis_p = proposition(CUT_P, BASE_P)
nat_p = TN_P * L.v * L.lam
n4_tf, TN_A, redis_a = proposition(CUT_LOG, BATI_MEN, menages_seuls=True)
p(f"[TAUX NATIONAL] proposition (droits divisés par deux sur tous les immeubles, {CUT_P:.2f} Md€, assiette {fr(BASE_P)} Md€) :"
  f" {100*CUT_P/(BASE_P*sm.part_champ):.3f} % en valeurs Insee ; {100*TN_P:.3f} % sur les terrains du modèle ;"
  f" les logements des particuliers paient {100*part_menages(BASE_P):.1f} % = {CUT_P*part_menages(BASE_P):.2f} Md€")
p(f"[TAUX NATIONAL] sol des logements seul (ancienne proposition N4) : {100*TN_A:.3f} % sur les terrains du modèle ;"
  f" {100*CUT_LOG/(BATI_MEN*sm.part_champ):.3f} % en valeurs Insee")
paye_aut = CUT_P * BATI_AUT / BASE_P
paye_nu = CUT_P * NU_PRIV / BASE_P
p(f"[QUI PAIE LE TAUX NATIONAL] logements des particuliers {CUT_P*part_menages(BASE_P):.2f} Md€ (droits en moins"
  f" {CUT_LOG:.2f}) ; sol des entreprises et autres bâtiments privés {paye_aut:.2f} Md€ (droits en moins {CUT_AUT:.2f}) ;"
  f" terrains non bâtis {paye_nu:.2f} Md€")
J["taux_national"] = dict(prop=float(100 * TN_P), n4=float(100 * TN_A),
                          prop_insee=float(100 * CUT_P / (BASE_P * sm.part_champ)),
                          n4_insee=float(100 * CUT_LOG / (BATI_MEN * sm.part_champ)),
                          paye_log=float(CUT_P * part_menages(BASE_P)), paye_aut=float(paye_aut), paye_nu=float(paye_nu),
                          cut_log=float(CUT_LOG), cut_aut=float(CUT_AUT))
# Incitation à laisser un terrain nu quand seul le sol des logements est taxé
p(f"[USAGE] avec le seul sol des logements, construire un logement sur un terrain nu déclenche un impôt dont la valeur"
  f" actuelle vaut {100*TN_A/R_ACT:.1f} % de la valeur du terrain (r = 3 %) ; avec tous les terrains : 0")

d_prop = resume("PROPOSITION", prop_tf, d1, "prop")
d_n4 = resume("SOL DES LOGEMENTS SEUL (N4)", n4_tf, d1, "n4")
p(f"[PROPOSITION] la part nationale représente {100*(W*nat_p)[d_prop > 300].sum()/(W*d_prop)[d_prop > 300].sum():.0f} %"
  f" du montant des hausses de plus de 300 €")
# Plus fortes hausses (cellules d'au moins 1 000 logements)
noms = c.nom
Tt = L.assign(dtf=d_prop, pct=100 * d_prop / L.tf0, nom=L.codgeo.map(noms))
top = Tt[Tt.n >= 1000].sort_values("dtf", ascending=False).head(6)
p("[PROPOSITION] plus fortes hausses (cellules ≥ 1 000 logements) : " + " ; ".join(
    f"{r.nom} ({'maisons' if r.type == 'm' else 'appartements'}) {r.dtf:+,.0f} € ({r.pct:+.0f} %)" for _, r in top.iterrows()))
J["top"] = [(str(r.nom), str(r.type), float(r.dtf), float(r.pct)) for _, r in top.iterrows()]

# Sensibilités de la proposition
sens = {}
for nom_b, base in BASES.items():
    if nom_b == "sol des logements seul":
        continue
    tf_, tn_, _ = proposition(CUT_P, base)
    dd = tf_ - L.tf0
    sens[nom_b] = (100 * tn_, 100 * CUT_P / (base * sm.part_champ), float(100 * (W * dd)[PARIS].sum() / (W * L.tf0)[PARIS].sum()),
                   float(par_decile(dd)[9]), float(W[dd > 300].sum() / NLOG))
tf_, tn_, _ = proposition(CUT_LOG, BASE_P)
dd = tf_ - L.tf0
sens["tous terrains privés, droits des seuls logements"] = (100 * tn_, 100 * CUT_LOG / (BASE_P * sm.part_champ),
                                                           float(100 * (W * dd)[PARIS].sum() / (W * L.tf0)[PARIS].sum()),
                                                           float(par_decile(dd)[9]), float(W[dd > 300].sum() / NLOG))
tf_, tn_, _ = proposition(CUT_P, BASE_P - hlm_terre)
dd = tf_ - L.tf0
sens["tous terrains privés, sol des HLM exonéré"] = (100 * tn_, 100 * CUT_P / ((BASE_P - hlm_terre) * sm.part_champ),
                                                     float(100 * (W * dd)[PARIS].sum() / (W * L.tf0)[PARIS].sum()),
                                                     float(par_decile(dd)[9]), float(W[dd > 300].sum() / NLOG))
for k_, v in sens.items():
    p(f"[SENSIBILITÉ ASSIETTE] {k_} : taux {v[0]:.3f} % (modèle), {v[1]:.3f} % (Insee) ; Paris {v[2]:+.0f} % ;"
      f" dernier décile {v[3]:+.0f} €/an ; hausses > 300 € {100*v[4]:.1f} %")
J["sens_assiette"] = sens

# Volumes : si les ventes augmentent de 6 % par point, la baisse coûte moins
c_vol = sm.cout_baisse(S)[0]
F_VOL = c_vol / CUT_LOG
p(f"[VOLUMES] avec +6 % de ventes par point, la baisse des droits des logements coûte {c_vol:.2f} Md€ au lieu de"
  f" {CUT_LOG:.2f} (×{F_VOL:.2f}) ; taux national {100*TN_P*F_VOL:.3f} % (modèle)")

# Impôt sur le bâti et perte sèche
K_BATI = (W * L.v * (1 - L.lam)).sum() / 1e9
bati0 = (W * L.tf0 * (1 - L.lam)).sum() / 1e9
U = 0.045


def bati_apres(k):
    if not np.isfinite(k):
        return 0.0
    b = L.v * (L.lam * k + (1 - L.lam))
    tc = (W * L.tf0).groupby(L.codgeo).sum() / (W * b).groupby(L.codgeo).sum()
    return float((W * L.codgeo.map(tc) * L.v * (1 - L.lam)).sum() / 1e9)


def tri_bati(b1, eps=1.0, u=U, b0=bati0):
    return eps * (K_BATI / u) * ((b1 / K_BATI) ** 2 - (b0 / K_BATI) ** 2) / 2


def tri_ventes(t1, sig, v=V_VENTES / 1e9, t0=T):
    return sig * v * (t1 ** 2 - t0 ** 2) / 2


B4 = bati_apres(4)
B_NAIF = bati0 * (1 + hausse_naif)
ps = {"ventes": tri_ventes(T / 2, 6), "bati_prop": tri_bati(B4), "bati_naif": tri_bati(B_NAIF)}
V_AUT = DMTO_AUT * F_CHAMP / T
ps["ventes_autres"] = tri_ventes(T / 2, 6, v=V_AUT)
p(f"[BÂTI] impôt sur le bâti des logements : {bati0:.1f} Md€ aujourd'hui ; {B4:.1f} avec la proposition ; {B_NAIF:.1f}"
  f" avec la réforme naïve ; valeur du bâti {fr(K_BATI)} Md€")
p(f"[PERTE SÈCHE] ventes de logements (σ = 6) {ps['ventes']:+.2f} Md€ (σ = 3 / 8 / 15 : "
  + " / ".join(f"{tri_ventes(T/2, s_):+.2f}" for s_ in (3, 8, 15)) + ") ; σ = 0 : 0")
p(f"[PERTE SÈCHE] bâti : proposition {ps['bati_prop']:+.2f} (ε = 0,5 : {tri_bati(B4, 0.5):+.2f} ; u = 3,5 % :"
  f" {tri_bati(B4, u=0.035):+.2f} ; u = 6 % : {tri_bati(B4, u=0.06):+.2f}) ; réforme naïve {ps['bati_naif']:+.2f}")
p(f"[PERTE SÈCHE] ventes des autres immeubles (σ = 6 transposé, {V_AUT:.0f} Md€ de ventes, ordre de grandeur) :"
  f" {ps['ventes_autres']:+.2f}")
TOT_NAIF = ps["ventes"] + ps["bati_naif"]
TOT_LOG = ps["ventes"] + ps["bati_prop"]
TOT_PROP = TOT_LOG + ps["ventes_autres"]
p(f"[PERTE SÈCHE] total : réforme naïve {TOT_NAIF:+.2f} ; proposition, logements {TOT_LOG:+.2f} ; avec les autres immeubles"
  f" {TOT_PROP:+.2f} Md€ ({100*-TOT_LOG/PIB24:.3f} % du PIB pour les logements)")
# Määttänen et Terviö : coût d'appariement qui REMPLACE le triangle sur les ventes (H18)
mt = (173 - 64) * NLOG / 1e9
p(f"[PERTE SÈCHE] variante Määttänen-Terviö (remplace le triangle sur les ventes) : environ {mt:.1f} Md€ (euros 2004),"
  f" total {-(mt) + ps['bati_prop']:+.1f} Md€")
# Coin des droits sur le capital (H11) et sol seul / rapport 2
coin = D0 / VAL
p(f"[PERTE SÈCHE] bâti avec le coin des droits sur la détention ({100*coin:.3f} %/an) : proposition"
  f" {(K_BATI/U)*((B4/K_BATI + coin/2)**2 - (bati0/K_BATI + coin)**2)/2:+.2f} ; réforme naïve"
  f" {(K_BATI/U)*((B_NAIF/K_BATI + coin/2)**2 - (bati0/K_BATI + coin)**2)/2:+.2f}")
for k_ in (2, 4, np.inf):
    p(f"[PERTE SÈCHE] rapport terrain/bâti {k_} : impôt sur le bâti {bati_apres(k_):.1f} Md€ -> {tri_bati(bati_apres(k_)):+.2f} Md€")
J["ps"] = {k: float(v) for k, v in ps.items()}
J["ps"].update(total_naif=float(TOT_NAIF), total_log=float(TOT_LOG), total_prop=float(TOT_PROP))

# =====================================================================================================================
# Capitalisation et valeur actualisée
# =====================================================================================================================
p()
p("-" * 100)
p("CAPITALISATION")
nat_tot = CUT_P
for r in (0.03, 0.04):
    p(f"[VALEUR ACTUELLE r = {100*r:.0f} %] taux national (tous terrains) : {nat_tot/r:.0f} Md€ pour l'ensemble des"
      f" propriétaires de terrains, dont {CUT_P*part_menages(BASE_P)/r:.0f} pour les logements des particuliers ;"
      f" baisse des droits sur les logements : {CUT_LOG/r:.0f} Md€ ; sol des logements seul : {CUT_LOG/r:.0f} Md€")
dTF = d_prop
dD = d1 - L.d0
cas = {"prix figés (pas de capitalisation)": None,
       "symétrique (taxe et droits capitalisés)": -(dTF + dD) / R_ACT,
       "asymétrique (taxe capitalisée, baisse des droits à l'acheteur)": -dTF / R_ACT}
cap = {}
for nom, dv in cas.items():
    if dv is None:
        continue
    tot = (W * dv).sum() / 1e9
    perte = (W * dv.clip(upper=0)).sum() / 1e9
    pct = dv / L.v
    cap[nom] = dict(total=float(tot), pertes=float(perte), pct_total=float(100 * tot * 1e9 / VAL),
                    paris=float(dv[PARIS_A].iloc[0]), paris_pct=float(100 * pct[PARIS_A].iloc[0]),
                    p5=float(100 * quantile_pondere(pct, 0.05)), plus5=float(W[pct < -0.05].sum() / NLOG))
    p(f"[CAPITALISATION, {nom}] variation de la valeur des logements {tot:+.0f} Md€ ({cap[nom]['pct_total']:+.1f} %) ;"
      f" somme des pertes {perte:.0f} Md€ ; appartement parisien médian {cap[nom]['paris']:+,.0f} €"
      f" ({cap[nom]['paris_pct']:+.1f} %) ; 5e centile {cap[nom]['p5']:+.1f} % ; logements perdant plus de 5 % de leur"
      f" valeur {100*cap[nom]['plus5']:.1f} %")
# Naïf, cas asymétrique
dvn = -d_naif / R_ACT
p(f"[CAPITALISATION, réforme naïve, asymétrique] {(W*dvn).sum()/1e9:+.0f} Md€ ; Paris {float(dvn[PARIS_A].iloc[0]):+,.0f} €")
J["cap"] = cap


def part_annonce(n, r=R_ACT, horizon=400):
    t = np.arange(1, horizon + 1)
    return float((np.minimum(t / n, 1) / (1 + r) ** t).sum() / (1 / (1 + r) ** t).sum())


PA = {n: part_annonce(n) for n in (1, 3, 5, 10, 20)}
p("[ÉTALEMENT] part de la perte actualisée supportée à l'annonce si la hausse monte linéairement sur n ans (r = 3 %) : "
  + " ; ".join(f"{n} ans {100*v:.0f} %" for n, v in PA.items()))
J["part_annonce"] = PA

# =====================================================================================================================
# Cas-types
# =====================================================================================================================
p()
p("-" * 100)
p("CAS-TYPES")
CAS = [("75056", "a", "Paris, appartement"), ("69123", "a", "Lyon, appartement"), ("33063", "a", "Bordeaux, appartement"),
       ("44109", "m", "Nantes, maison"), ("87085", "m", "Limoges, maison"), ("42218", "a", "Saint-Étienne, appartement"),
       ("74010", "m", "Annecy, maison"), ("33009", "m", "Arcachon, maison"), ("23096", "m", "Guéret, maison"),
       ("19272", "m", "Ussel, maison")]


def rattrapage(eco, dt, r=R_ACT):
    if dt <= 0:
        return "jamais (taxe en baisse)"
    if r * eco >= dt:
        return "jamais"
    return f"{-np.log(1 - r*eco/dt)/np.log(1+r):.0f} ans"


ct = []
for code, t, lab in CAS:
    i = idx(code, t)
    eco = S * T * L.v[i]
    row = dict(cas=lab, valeur=float(L.v[i]), terrain=float(L.lam[i]), tf0=float(L.tf0[i]), droits=float(T * L.v[i]),
               eco=float(eco), naif=float(d_naif[i]), n4=float(d_n4[i]), prop=float(d_prop[i]),
               nat=float(nat_p[i]), redis=float(redis_p[i]))
    for h in (7, 15):
        row[f"net{h}"] = float(eco - row["prop"] * (1 - (1 + R_ACT) ** -h) / R_ACT)
    row["ratt_prop"], row["ratt_naif"] = rattrapage(eco, row["prop"]), rattrapage(eco, row["naif"])
    ct.append(row)
    p(f"[CAS] {lab} : valeur {fr(row['valeur'])} €, terrain {100*row['terrain']:.0f} %, taxe {fr(row['tf0'])} € ; droits"
      f" à l'achat {fr(row['droits'])} € (économie {fr(eco)} €) ; ΔTF : naïve {row['naif']:+.0f}, sol des logements seul"
      f" {row['n4']:+.0f}, proposition {row['prop']:+.0f} € (part nationale {row['nat']:.0f}, redistribution communale"
      f" {row['redis']:+.0f}) ; acheteur qui revend après 7 ans {row['net7']:+,.0f} €, 15 ans {row['net15']:+,.0f} € ;"
      f" économie rattrapée : proposition {row['ratt_prop']}, naïve {row['ratt_naif']}")
J["cas"] = ct

# Retraité modeste dans une zone chère : report de paiement par défaut
i = idx("75056", "a")
X = float(d_prop[i])
for taux in (0.02, 0.03, 0.04):
    for h in (10, 15, 20):
        dette = X * ((1 + taux) ** h - 1) / taux
        if taux == 0.03 or h == 15:
            p(f"[REPORT] retraité parisien (hausse {X:.0f} €/an reportée), intérêt {100*taux:.0f} %, {h} ans : dette"
              f" {fr(dette)} € = {100*dette/L.v[i]:.1f} % de la valeur actuelle du logement")
# Majorant du coût de trésorerie : toutes les hausses des propriétaires occupants reportées
po = L.codgeo.map(part_st["Propriétaires occupants"]).fillna(0)
hausse_po = (W * d_prop.clip(lower=0) * po).sum() / 1e9
p(f"[REPORT] majorant : si tous les propriétaires occupants reportaient leur hausse, {hausse_po:.2f} Md€ par an"
  f" (somme des hausses positives des propriétaires occupants)")
J["report"] = dict(paris_hausse=X, majorant=float(hausse_po))

# Famille qui s'agrandit : vend un appartement à Bordeaux, achète une maison à Nantes (droits payés par l'acheteur)
i_m = idx("44109", "m")
p(f"[FAMILLE] achat d'une maison à Nantes ({fr(L.v[i_m])} €) : droits {fr(T*L.v[i_m])} € -> économie"
  f" {fr(S*T*L.v[i_m])} € ; ΔTF ensuite {float(d_prop[i_m]):+.0f} €/an")

# =====================================================================================================================
# 5. ARBITRAGES
# =====================================================================================================================
p()
p("=" * 100)
p("5. ARBITRAGES")
p("=" * 100)
arb = {}
for s_ in (0.3, 0.5, 1.0):
    cl = s_ * D0 / 1e9
    ca = s_ * DMTO_AUT * F_CHAMP
    tf_, tn_, _ = proposition(cl + ca, BASE_P)
    dd = tf_ - L.tf0
    tri = tri_ventes(T * (1 - s_), 6)
    arb[s_] = dict(cout=float(cl + ca), cout_log=float(cl), taux=float(100 * tn_), ps_ventes=float(tri),
                   paris=float(dd[PARIS_A].iloc[0]), d10=float(par_decile(dd)[9]), plus300=float(W[dd > 300].sum() / NLOG))
    p(f"[BAISSE {int(100*s_)} %] coût {cl+ca:.2f} Md€ (logements {cl:.2f}) ; taux national {100*tn_:.3f} % ; perte sèche"
      f" sur les ventes de logements {tri:+.2f} Md€ ; Paris appartement {arb[s_]['paris']:+.0f} € ; dernier décile"
      f" {arb[s_]['d10']:+.0f} € ; hausses > 300 € {100*arb[s_]['plus300']:.1f} %")
p(f"[BAISSE] 30 % garde {100*arb[0.3]['ps_ventes']/arb[0.5]['ps_ventes']:.0f} % du gain sur les ventes de la baisse de"
  f" 50 % pour {100*arb[0.3]['cout']/arb[0.5]['cout']:.0f} % de son coût")
J["arb_baisse"] = arb

# Sol seul ou deux taux (part communale), avec le taux national de la proposition
arb_k = {}
for k_ in (1, 2, 4, np.inf):
    tf_, tn_, _ = proposition(CUT_P, BASE_P, k=k_)
    dd = tf_ - L.tf0
    ty = L.assign(a=W * dd, w=W).groupby("type").sum(numeric_only=True)
    arb_k[str(k_)] = dict(bati=bati_apres(k_), paris=float(100 * (W * dd)[PARIS].sum() / (W * L.tf0)[PARIS].sum()), d10=float(par_decile(dd)[9]),
        maisons=float(ty.a["m"] / ty.w["m"]), apparts=float(ty.a["a"] / ty.w["a"]), plus300=float(W[dd > 300].sum() / NLOG))
    arb_k[str(k_)]["ps_bati"] = float(tri_bati(arb_k[str(k_)]["bati"]))
    v = arb_k[str(k_)]
    p(f"[RAPPORT {k_}] impôt sur le bâti {v['bati']:.1f} Md€ (perte sèche {v['ps_bati']:+.2f}) ; Paris {v['paris']:+.0f} % ;"
      f" dernier décile {v['d10']:+.0f} € ; maisons {v['maisons']:+.0f} €, appartements {v['apparts']:+.0f} € ;"
      f" hausses > 300 € {100*v['plus300']:.1f} %")
J["arb_k"] = arb_k

# Taux national ou départemental (sur le sol des logements, faute de valeur des terrains d'entreprise par département)
td = sm.deux_taux_local(S, 4)[0]
dd_dep = td - L.tf0
TD = sm.TAUX["dep4"]
p(f"[DÉPARTEMENTAL] taux départemental sur le sol des logements : de {100*TD.min():.2f} à {100*TD.max():.2f} % ; Paris"
  f" {100*TD['75']:.3f} %, Creuse {100*TD['23']:.3f} % ; Paris appartement {float(dd_dep[PARIS_A].iloc[0]):+.0f} € ;"
  f" Guéret maison {float(dd_dep[idx('23096', 'm')]):+.0f} € ; Ussel {float(dd_dep[idx('19272', 'm')]):+.0f} €")

# Compensation des collectivités et péréquation implicite (part des logements)
part_dep = (0.045 + 0.0237 * 0.045) / T
p(f"[COMPENSATION] droits perdus sur les logements {CUT_LOG:.2f} Md€ : départements {CUT_LOG*0.045/T:.2f}, communes"
  f" {CUT_LOG*0.012/T:.2f}, frais de l'État {CUT_LOG*0.0237*0.045/T:.2f} ; autres immeubles {CUT_AUT:.2f}")
perte_dep = L.assign(x=W * L.d0 * S).groupby("dep").x.sum()
for nom, tn_ in (("proposition", TN_P), ("sol des logements seul", TN_A)):
    paye = L.assign(x=W * tn_ * L.v * L.lam).groupby("dep").x.sum()
    net = paye - perte_dep
    p(f"[PÉRÉQUATION, {nom}, logements] Paris paie {paye['75']/1e6:,.0f} M€ et perd {perte_dep['75']/1e6:,.0f} M€ ({net['75']/1e6:+,.0f}) ;"
      f" Hauts-de-Seine {net['92']/1e6:+,.0f} M€ ; Creuse {net['23']/1e6:+,.0f} M€ ; transfert entre départements"
      f" {net[net > 0].sum()/1e6:,.0f} M€ ; départements contributeurs nets {(net > 0).sum()}")
    if nom == "proposition":
        J["perequation"] = dict(paris=float(net["75"] / 1e6), hds=float(net["92"] / 1e6), transfert=float(net[net > 0].sum() / 1e6))

# =====================================================================================================================
# 6. TRANSITION
# =====================================================================================================================
p()
p("=" * 100)
p("6. TRANSITION")
p("=" * 100)
trans = {}
for n in (3, 5, 10):
    pas = d_prop.clip(lower=0) / n
    deficit = CUT_P * (n - 1) / 2
    trans[n] = dict(p90=quantile_pondere(pas, 0.9), p99=quantile_pondere(pas, 0.99), paris=float(pas[PARIS_A].iloc[0]),
                    deficit=float(deficit), deficit_vol=float(deficit * F_VOL), annonce=part_annonce(n))
    p(f"[{n} ANS] hausse annuelle (toutes composantes linéaires) : P90 {trans[n]['p90']:.0f} €, P99 {trans[n]['p99']:.0f} €,"
      f" Paris appartement {trans[n]['paris']:.0f} € ; déficit cumulé si les droits baissent dès l'annonce {deficit:.1f} Md€"
      f" ({deficit*F_VOL:.1f} avec la reprise des ventes) ; perte actualisée supportée à l'annonce {100*part_annonce(n):.0f} %")
J["transition"] = trans
# Calendrier détaillé sur 5 ans : année par année
N5 = 5
cal = []
for a in range(1, N5 + 1):
    f = min(a / N5, 1.0)
    rec = CUT_P * f
    cal.append(dict(annee=a, taux=float(100 * TN_P * f), recette=float(rec), deficit=float(CUT_P - rec),
                    paris=float(L.tf0[PARIS_A].iloc[0] + f * d_prop[PARIS_A].iloc[0])))
p("[CALENDRIER 5 ANS] " + " ; ".join(f"année {r['annee']} : taux {r['taux']:.3f} %, recette {r['recette']:.1f}, manque"
                                      f" {r['deficit']:.1f} Md€, taxe parisienne {r['paris']:.0f} €" for r in cal))
J["calendrier5"] = cal
# Si les valeurs provisoires ne sont pas prêtes : la montée du taux commence après D années de droits déjà baissés
for n in (3, 5, 10):
    p(f"[RETARD] montée sur {n} ans commençant après 3 années sans nouvelle recette : déficit cumulé"
      f" {CUT_P*3 + CUT_P*(n-1)/2:.1f} Md€ ; baisse des droits en deux temps (25 % à l'annonce, 25 % au démarrage) :"
      f" {CUT_P/2*3 + CUT_P*(n-1)/2:.1f} Md€")
# Ancien calendrier (taux national plein la 1re année) : saut parisien
p(f"[ANCIEN CALENDRIER] taux national plein dès la 1re année : saut parisien {float(nat_p[PARIS_A].iloc[0]):+.0f} €"
  f" (sol des logements seul : {float((TN_A*L.v*L.lam)[PARIS_A].iloc[0]):+.0f} €)")
# Surtaxe transitoire sur les valeurs de 1970 (financement rejeté)
p(f"[SURTAXE 1970] relever la taxe actuelle de {100*CUT_P*1e9/TF0:.0f} % pour financer la transition : taxe / valeur"
  f" {100*ratio_decile(L.tf0*(1+CUT_P*1e9/TF0), L.v)[0]:.2f} % dans le décile le moins cher, "
  f"{100*ratio_decile(L.tf0*(1+CUT_P*1e9/TF0), L.v)[9]:.2f} % dans le plus cher")

# Sensibilité au vieillissement de la taxe actuelle (H6, correction à trois zones, indices Notaires-Insee)
zone = np.where(PARIS, 1.113, np.where(L.dep.isin(["77", "78", "91", "92", "93", "94", "95"]), 1.134, 1.281))
tf0b = L.tf0 / zone
tf0b = tf0b * TF0 / (W * tf0b).sum()
b4 = L.v * (L.lam * 4 + (1 - L.lam))
tcb = (W * tf0b).groupby(L.codgeo).sum() / (W * b4).groupby(L.codgeo).sum()
propb = L.codgeo.map(tcb) * b4 + nat_p
ddb = propb - tf0b
p(f"[H6] taxe actuelle corrigée du double vieillissement : Paris {100*(W*ddb)[PARIS].sum()/(W*tf0b)[PARIS].sum():+.0f} %"
  f" (au lieu de {J['prop']['paris_pct']:+.0f} %) ; ΔTF % par décile : "
  + " ".join(f"{u:+.0f}" for u in 100 * ((W * ddb).groupby(L.dec_prix).sum() / (W * tf0b).groupby(L.dec_prix).sum()))
  + f" ; hausses > 300 € {100*W[ddb > 300].sum()/NLOG:.1f} %")

# Variante de mesure du terrain (H5) : résidu pour les maisons aussi, coût recalé sur 45,4 % de terrain
lam0, terre0 = L.lam.copy(), TERRE


def part_tot(B):
    lm_ = (1 - B / sm.RATIO_COUT_APPART / L.pm2).clip(sm.LMIN, sm.LMAX)
    la_ = (1 - B / L.pm2).clip(sm.LMIN, sm.LMAX)
    lam_ = np.where(L.type == "m", lm_, la_)
    return lam_, (W * L.v * lam_).sum() / (W * L.v).sum()


lo, hi = 100.0, 6000.0
for _ in range(40):
    Bv = (lo + hi) / 2
    lo, hi = (Bv, hi) if part_tot(Bv)[1] > sm.LAMBDA_MENAGES else (lo, Bv)
L["lam"] = part_tot(Bv)[0]
TERRE = (W * L.v * L.lam).sum()
tfv_, _, _ = proposition(CUT_P, BASE_P)
dv_ = tfv_ - L.tf0
ty = L.assign(a=W * dv_, w=W).groupby("type").sum(numeric_only=True)
p(f"[H5] terrain des maisons mesuré par résidu (coût recalé {Bv:,.0f} €/m²) : maisons {ty.a['m']/ty.w['m']:+.0f} €,"
  f" appartements {ty.a['a']/ty.w['a']:+.0f} € (mesure centrale : maisons {J['prop']['maisons']:+.0f}, appartements"
  f" {J['prop']['apparts']:+.0f}) ; par décile : " + " ".join(f"{u:+.0f}" for u in par_decile(dv_))
  + f" ; Paris {100*(W*dv_)[PARIS].sum()/(W*L.tf0)[PARIS].sum():+.0f} %")
J["h5"] = dict(maisons=float(ty.a["m"] / ty.w["m"]), apparts=float(ty.a["a"] / ty.w["a"]))
L["lam"] = lam0
TERRE = terre0

(OUT / "calculs_foncier.txt").write_text("\n".join(lignes) + "\n", encoding="utf-8")


def _js(o):
    if isinstance(o, dict):
        return {str(k): _js(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [_js(v) for v in o]
    if isinstance(o, (np.floating, np.integer)):
        return float(o)
    return o


(OUT / "calculs_foncier.json").write_text(json.dumps(_js(J), ensure_ascii=False, indent=1), encoding="utf-8")
