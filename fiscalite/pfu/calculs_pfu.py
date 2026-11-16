"""Calculs de la partie « Revenus du capital » de la note fusionnée (synthese/parties/pfu.tex et annexe_pfu.tex).

Refonte du 16/11/2026 selon synthese/CHARTE_NOTE.md et synthese/DECISIONS.md (décision 3 : fermer l'effacement de
l'impôt sur les plus-values à la donation et au décès ; report d'apport-cession transmis sans effacement).
Reprend, en les recalculant, les chiffres vérifiés de revue/hypotheses_pfu.md (§ 2 à 6) et ajoute :
  - la série des dividendes reçus par les ménages (Insee) et sa réaction aux réformes ;
  - la comparaison européenne recalculée avec un IS à 25,8 % ;
  - la capitalisation dans une holding en valeur actualisée ;
  - l'ordre de grandeur de l'effacement à la transmission (toutes plus-values mobilières) et la recette, année par
    année et en valeur actualisée, d'une reprise du prix d'acquisition par le bénéficiaire ;
  - la valeur actualisée du stock de reports d'apport-cession sous quatre traitements ;
  - les cas types et la charge supplémentaire du haut de la distribution.

Lancer depuis fiscalite/ : python3 pfu/calculs_pfu.py
Sorties : pfu/sorties/calculs_pfu.txt (lisible) et pfu/sorties/calculs_pfu.json (pour pfu/figures_pfu_n.py).
Conventions : Md€ courants ; [H] hypothèse de l'auteur, sans mesure publiée ; [V] chiffre vérifié sur la source
indiquée ; [S] source secondaire ; [C] calcul.
"""
import csv
import json
from math import log
from pathlib import Path

HERE = Path(__file__).resolve().parent
DON, SORT = HERE / "donnees", HERE / "sorties"
SORT.mkdir(exist_ok=True)
L, J = [], {}
p = L.append


def fr(x, d=1):
    """Nombre au format français."""
    s = f"{x:,.{d}f}".replace(",", " ").replace(".", ",")
    return s.replace("-", "−")


# =====================================================================================================================
# 0. Paramètres (droit 2026) et données
# =====================================================================================================================
IR_PFU, PS_HAUT, PS_BAS = 0.128, 0.186, 0.172      # [V] CGI 200 A ; LFSS 2026 art. 12 (CSG 10,6 % ; 9,2 % liste fermée)
PFU = IR_PFU + PS_HAUT                              # 31,4 %
IS_N, CSB = 0.25, 0.033                             # [V] IS normal ; contribution sociale (IS > 763 000 €)
IS_C = IS_N * (1 + CSB)                             # 25,825 %
QPFC = 0.05                                         # [S] quote-part de frais et charges du régime mère-fille (AN 3056)
T_PV_REPORT = 0.30                                  # [H] taux appliqué à une plus-value en report qui expire : IR de
                                                    # l'année d'apport (12,8 %) + PS de 17,2 % (non tranché, registre H10)
# Déclarations 2042, revenus 2024 [V] (donnees/ir_2042_cases_revenus2024.csv, DGFiP)
C2042 = {r[0]: float(r[3]) / 1e9 for r in csv.reader(open(HERE.parent / "donnees" / "ir_2042_cases_revenus2024.csv",
                                                          encoding="utf-8")) if r and r[0] in
         ("2DC", "2TR", "2TS", "3VG", "3AN", "3VH", "3WH", "8UT", "3WA", "2CK")}
B24 = C2042["2DC"] + C2042["2TR"] + C2042["2TS"] + C2042["3VG"] + C2042["3AN"] - C2042["3VH"]
# Insee, comptes nationaux base 2020 (mai 2026) [V] : dividendes reçus par les ménages (D421, tableau 7.401),
# EBE et dividendes versés des SNF (tableau 7.101)
SERIE = [{k: float(v) for k, v in r.items()} for r in csv.DictReader(open(DON / "insee_dividendes_menages.csv"))]
DIVM = {int(r["annee"]): r["dividendes_recus_menages_Md"] for r in SERIE}
EBE = {int(r["annee"]): r["ebe_snf_Md"] for r in SERIE}
K25 = DIVM[2025] / DIVM[2024]                       # dividendes 2025 / 2024
B25 = B24 - C2042["2DC"] * (1 - K25)                # assiette 2025 approchée (dividendes seuls corrigés)
PIB25 = 2991.1                                      # [V] Insee, PIB 2025 (donnees/pib_france_cp_meur.json)
PAT = {r["indicateur"]: (float(r["fin_2024_Md"]), float(r["fin_2025_Md"]))
       for r in csv.DictReader(open(DON / "patrimoine_actions_menages.csv", encoding="utf-8"))}
TF = [dict(r) for r in csv.DictReader(open(DON / "tf_taux_integres_2025.csv", encoding="utf-8"))]

# Reports d'apport-cession [V] : AN n° 3056 (tableau DGFiP) ; EP du PLF 2027, art. 5 (stock 127 Md€ en 2023)
ENTREES = {2020: 10.841, 2021: 16.358, 2022: 18.366, 2023: 33.636, 2024: 22.172}
EXPIRES = {2020: 0.313, 2021: 0.494, 2022: 0.635, 2023: 0.418, 2024: 1.514}
STOCK_8UT = {2023: 152.869, 2024: 173.268}
STOCK_EP23 = 127.0
STOCK_C = STOCK_EP23 / STOCK_8UT[2023] * STOCK_8UT[2024]   # 2024 corrigé du rapport EP/8UT de 2023 : ≈ 144 Md€

R_ACT = (0.025, 0.035, 0.05)                        # [H] taux d'actualisation nominal (taux d'emprunt de l'État ±)


def bloc(titre):
    p("")
    p("=" * 110)
    p(titre)
    p("=" * 110)


# =====================================================================================================================
# 1. Situation actuelle
# =====================================================================================================================
bloc("1. SITUATION ACTUELLE")
p("1a. Assiette du PFU (déclarations 2042, revenus 2024) [V]")
for k, lib in (("2DC", "dividendes"), ("2TR", "intérêts"), ("2TS", "autres distributions"),
               ("3VG", "plus-values imposées"), ("3AN", "actifs numériques"), ("3VH", "moins-values (à déduire)"),
               ("3WH", "plus-values placées en report d'apport-cession (non imposées)"), ("8UT", "stock de reports")):
    p(f"   {lib:62s} {fr(C2042[k])} Md€")
p(f"   assiette du PFU : {fr(B24)} Md€ ; base 2025 approchée (dividendes × {fr(K25, 3)}) : {fr(B25)} Md€")
ir_pfu, ps_pfu = IR_PFU * B24, PS_HAUT * B24
A_PS_TOT, A_PS_HAUT = 204.0, 107.0          # [C] 15,305 / 7,5 % (PLF 2027, état A) ; 1,5 / 1,4 pt (LFSS 2026)
ps_tot = PS_HAUT * A_PS_HAUT + PS_BAS * (A_PS_TOT - A_PS_HAUT)
p("1b. Recettes (Md€ par an)")
p(f"   IR au PFU (12,8 % × assiette, majorant : 2,54 M d'optants) : {fr(ir_pfu)} ; acompte prélevé 2CK : {fr(C2042['2CK'])}")
p(f"   prélèvements sociaux sur l'assiette du PFU (18,6 %) : {fr(ps_pfu)}")
p(f"   prélèvements sociaux sur tous les revenus du capital (assiette ≈ {A_PS_TOT:.0f} Md€) : {fr(ps_tot)}")
p("   CEHR 1,41 (revenus 2023, toutes catégories ; part payée sur le capital inconnue, 50-80 % [H] -> 0,7-1,1) [V AN 3056]")
p("   CDHR 0,37 (acompte 2025) ; 0,6 prévus en 2027 (PLF 2027, état A) [V]")
J["recettes"] = dict(ir_pfu=ir_pfu, ps_pfu=ps_pfu, ps_tot=ps_tot, cehr=1.412, cdhr=0.37)
J["assiette"] = dict(dividendes=C2042["2DC"], interets=C2042["2TR"] + C2042["2TS"],
                     pv=C2042["3VG"] + C2042["3AN"] - C2042["3VH"], report=C2042["3WH"],
                     expires=EXPIRES[2024], total=B24)

p("1c. Concentration [V France Stratégie 2023, POTE 2021 ; AN 3056 pour les reports de 2023]")
CONC = {"foyers": 0.01, "dividendes": 33, "pv_droit_commun": 70, "pv_report_2023": 100 * 18.810 / 33.636}
p(f"   part du top 0,01 % (≈ 4 000 foyers) : dividendes 33 % ; plus-values de droit commun 70 % ; "
  f"plus-values mises en report en 2023 {fr(CONC['pv_report_2023'], 0)} % ; 84 foyers : {fr(100 * 23.5 / 33.636, 0)} %")
p("   part du top 1 % des dividendes : 96 % ; du top 0,1 % : 62 %")
J["concentration"] = CONC


def cumule(is_, perso):
    return 100 * (is_ + (1 - is_) * perso)


p("1d. Taux cumulés sur 100 € de bénéfice avant IS [C]")
TAUX = {"distribue": cumule(IS_C, PFU), "cehr": cumule(IS_C, PFU + 0.04), "cdhr": cumule(IS_C, 0.20 + PS_HAUT),
        "holding": cumule(IS_C, QPFC * IS_N), "holding_integre": cumule(IS_C, 0.01 * IS_N),
        "salaire": 100 * (0.097 + 0.49 * (1 - 0.068)), "distribue_is25": cumule(IS_N, PFU),
        "pfu25": cumule(IS_C, 0.25), "pfu33": cumule(IS_C, 0.33)}
for k, v in TAUX.items():
    p(f"   {k:18s} {fr(v, 2)} %")
p("   (salaire : taux marginal supérieur hors cotisations, 9,7 % de CSG-CRDS + 49 % d'IR et CEHR, CSG déductible 6,8 %)")
J["taux"] = TAUX

p("1e. Taux intégrés supérieurs sur les dividendes en Europe, 2025 (Tax Foundation) recalculés pour la France [V+C]")
fr25 = cumule(IS_C, 0.34)          # 2025 : PFU 30 % + CEHR 4 % (taux retenu par la Tax Foundation : 34 %)
fr26 = cumule(IS_C, PFU + 0.04)    # 2026 : PFU 31,4 % + CEHR 4 %
pays = [r for r in TF if r["pays"] not in ("Average", "United States (for comparison)")]
autres = sorted(((r["pays"], float(r["integre_dividendes"])) for r in pays if r["pays"] != "France"),
                key=lambda x: -x[1])
moy_tf = float(next(r for r in TF if r["pays"] == "Average")["integre_dividendes"])
moy_corr = (sum(v for _, v in autres) + fr25) / (len(autres) + 1)
rang25 = 1 + sum(v > fr25 for _, v in autres)
rang26 = 1 + sum(v > fr26 for _, v in autres)
p(f"   France publiée (IS 36,13 %) : 57,85 % ; recalculée IS 25,825 % : 2025 {fr(fr25, 2)} % (rang {rang25}/{len(pays)}) ;"
  f" 2026 {fr(fr26, 2)} % (rang {rang26}) ; sans CEHR 2026 {fr(TAUX['distribue'], 2)} %")
p(f"   moyenne publiée {fr(moy_tf, 2)} % ; recalculée avec la France à {fr(fr25, 1)} % : {fr(moy_corr, 2)} %")
p("   au-dessus de la France 2026 : " + ", ".join(f"{n} {fr(v, 1)}" for n, v in autres if v > fr26))
J["europe"] = dict(autres=autres, france25=fr25, france26=fr26, moyenne=moy_corr, rang25=rang25, rang26=rang26,
                   n=len(pays))

p("1f. Capitalisation : 100 € de bénéfice avant IS, rendement R, actualisation à R (valeur actualisée nette) [C]")
p("    A = distribuer tout de suite ; B = garder dans la holding N ans puis distribuer (PFU sur le tout) ;")
p("    C = garder dans la holding puis transmettre (effacement : les héritiers sortent la valeur sans PFU) ;")
p("    D = placer soi-même le dividende net, revenus imposés chaque année au PFU (repère de l'avis Catherine)")


def holding(R=0.05, N=25, tau_h=QPFC * IS_N, k_heritiers=None):
    """Taux d'imposition effectif, en valeur actualisée au taux R, de 100 € de bénéfice avant IS selon la voie."""
    net = 100 * (1 - IS_C)
    rho = (1 + R * (1 - tau_h)) / (1 + R)
    va = {"A": net * (1 - PFU), "B": net * rho ** N * (1 - PFU), "C": net * rho ** N,
          "D": net * (1 - PFU) * ((1 + R * (1 - PFU)) / (1 + R)) ** N}
    if k_heritiers is not None:      # proposition : les héritiers sortent la valeur k ans après la transmission
        va["C_prop"] = net * rho ** (N + k_heritiers) * (1 - PFU)
    return {k: 100 - v for k, v in va.items()}, (1 + R * (1 - tau_h)) ** N / (1 + R * (1 - PFU)) ** N - 1


for R in (0.03, 0.05, 0.07):
    for N in (25, 40):
        t, plus = holding(R, N, k_heritiers=10)
        p(f"   R = {R:.0%}, N = {N} : A {fr(t['A'])} % ; B {fr(t['B'])} % ; C {fr(t['C'])} % ; C proposition "
          f"{fr(t['C_prop'])} % ; D {fr(t['D'])} % ; richesse finale B/D − 1 = {fr(100 * plus, 0)} %")
t, plus = holding()
J["holding"] = dict(t, C_prop=holding(k_heritiers=10)[0]["C_prop"], plus=plus)
t_port, _ = holding(tau_h=IS_N)
p(f"   holding de placement (revenus imposés à l'IS de 25 %) : B {fr(t_port['B'])} % ; C {fr(t_port['C'])} %")

p("1g. Dividendes reçus par les ménages (Insee, D421, Md€) et part de l'EBE des SNF [V+C]")
for a in range(2010, 2026):
    var = "" if a == 2010 else f" ({fr(100 * (DIVM[a] / DIVM[a - 1] - 1), 0)} %)"
    p(f"   {a} : {fr(DIVM[a])}{var} ; {fr(100 * DIVM[a] / EBE[a])} % de l'EBE des SNF")
J["serie"] = dict(annees=list(range(2010, 2026)), div=[DIVM[a] for a in range(2010, 2026)],
                  part_ebe=[100 * DIVM[a] / EBE[a] for a in range(2010, 2026)])

# =====================================================================================================================
# 2. Réforme naïve : changer le taux ou revenir au barème
# =====================================================================================================================
bloc("2. RÉFORME NAÏVE")


def reaction(e, b, t0, t1):
    return e * b * log((1 - t1) / (1 - t0))


def changement(t1, b=B24, e=0.77, t0=PFU):
    """Recette (+) ou coût (−) d'un passage du PFU de t0 à t1. Premières années : toute la réaction rapporte
    (rattrapage compris) ; régime permanent : seule la part pi de la réaction est durable (registre H2)."""
    dq = reaction(e, b, t0, t1)
    meca = (t1 - t0) * b
    prem = t1 * (b + dq) - t0 * b
    perm = {pi: meca + pi * t1 * dq for pi in (0.0, 0.5, 1.0)}
    return meca, prem, perm, dq


NAIF = {}
for nom, t1 in (("PFU 25 %", 0.25), ("PFU 33 %", 0.33), ("PFU 34,4 %", 0.344)):
    for nb, b in (("2024", B24), ("2025", B25)):
        res = [changement(t1, b, e) for e in (0.65, 0.77, 1.0)]
        meca = res[0][0]
        prem = [r[1] for r in res]
        perm = [r[2] for r in res]
        p(f"   {nom}, base {nb} : mécanique {fr(meca, 2)} ; premières années (e = 0,65 / 0,77 / 1) "
          + " / ".join(fr(x, 2) for x in prem) + " ; régime permanent (e = 0,77, π = 0 / 0,5 / 1) "
          + " / ".join(fr(perm[1][pi], 2) for pi in (0.0, 0.5, 1.0)))
        NAIF[f"{nom} {nb}"] = dict(meca=meca, prem=prem, perm_077=[perm[1][pi] for pi in (0.0, 0.5, 1.0)])
J["naif"] = NAIF

p("2b. Taux qui maximise la recette (sans réaction croisée) 1/(1+e) et coût d'un euro levé à 31,4 % [C]")
for e in (0.65, 0.77, 1.0):
    p(f"   e = {e} : {fr(100 / (1 + e))} % ; {fr(1 / (1 - e * PFU / (1 - PFU)), 2)} €")

p("2c. Perte sèche d'un PFU à 25 % (Harberger ; π = part de la réaction qui échappe définitivement à l'impôt ;")
p("    μ − 1 = prix d'un milliard levé ailleurs, 0,04 / 0,08 / 0,17, sorties/architectures_ircsg.txt [PRIX]) [C]")
MU1 = (0.04, 0.08, 0.17)
for pi in (0.0, 0.5, 1.0):
    dq = reaction(0.77, B24, PFU, 0.25)
    perdu = (PFU - 0.25) * B24 - pi * 0.25 * dq
    ps = [-pi * (PFU + 0.25) / 2 * dq + m * perdu for m in MU1]
    p(f"   π = {pi} : " + " / ".join(fr(x, 2) for x in ps) + f" Md€ (recette perdue {fr(perdu, 1)})")
p("2d. Bloc épargne (avis Cochrane) : si l'épargne réagissait au rendement net avec une élasticité réelle ε_s [H],")
p("    la perte sèche sur l'assiette du PFU vaut ½ ε_s t²/(1 − t) B ; gain d'une baisse de 31,4 à 25 % :")
EPARGNE = {}
for es in (0.1, 0.2, 0.5):
    g = 0.5 * es * B24 * (PFU ** 2 / (1 - PFU) - 0.25 ** 2 / 0.75)
    EPARGNE[es] = g
    p(f"   ε_s = {es} : −{fr(g, 2)} Md€ de perte sèche (à comparer au coût du financement : +0,2 à +0,9)")
J["epargne"] = EPARGNE

p("2e. Retour au barème : ordre de grandeur statique [H fortes : 96 % des dividendes au TMI 45 %, 4 % au TMI 30 %,")
p("    intérêts au TMI 30 %, plus-values au TMI 45 %, abattement de 40 %, CSG déductible 6,8 %]")
DIV, INT, PV = C2042["2DC"], C2042["2TR"], C2042["3VG"]
gain = (0.96 * DIV * (0.45 * (0.6 - 0.068) - IR_PFU) + 0.04 * DIV * (0.30 * (0.6 - 0.068) - IR_PFU)
        + INT * (0.30 * (1 - 0.068) - IR_PFU) + PV * (0.45 * (1 - 0.068) - IR_PFU))
p(f"   gain statique ≈ {fr(gain)} Md€ (avant optants déjà au barème, CDHR perdue de 0,4-0,6 et TMI de 41 %)")
BAREME = {"statique": gain}
for e in (0.65, 0.77, 1.0):
    t1 = PFU + gain / B24
    dq = reaction(e, B24, PFU, t1)
    BAREME[e] = t1 * (B24 + dq) - PFU * B24
    p(f"   e = {e} : taux moyen {fr(100 * PFU)} -> {fr(100 * t1)} % ; recette nette {fr(BAREME[e])} Md€")
b40 = gain - 0.40 * DIV * (PFU + 0.96 * (0.45 * 0.532 - IR_PFU))
BAREME["moins40"] = b40
p(f"   si les dividendes baissaient de 40 % comme en 2013 : {fr(b40)} Md€ ; Institut Montaigne via CAE : 3,2 à 3,6"
  " (statique), −0,7 si l'assiette revient à 2017 [S]")
J["bareme"] = BAREME

p("2f. Exil (CAE Focus 118 : 0,02 à 0,23 % du top 1 % par point, long terme) [V+C]")
base_top1 = 0.96 * DIV + 0.8 * PV + 0.3 * INT      # [H] parts du top 1 % dans les plus-values et intérêts
for dp in (0.0002, 0.0023):
    p(f"   PFU à 25 % : {fr(100 * dp * 6.4, 2)} % du top 1 % retenu -> {fr(dp * 6.4 * 0.25 * base_top1, 2)} Md€ gardés")
p(f"   assiette du PFU du top 1 % ≈ {fr(base_top1, 0)} Md€ ; impôt personnel ≈ {fr(PFU * base_top1)} Md€ + CEHR et CDHR")
J["top1"] = dict(base=base_top1, impot=PFU * base_top1)

# =====================================================================================================================
# 3. Proposition : reprise du prix d'acquisition à la donation et au décès ; report transmis sans effacement
# =====================================================================================================================
bloc("3. PROPOSITION : FERMER L'EFFACEMENT À LA TRANSMISSION")
dir_eq = PAT["Actions cotées (BdF)"][1] + PAT["Actions non cotées et autres participations (BdF)"][1]
opc_act = PAT["Actions détenues indirectement (OPC) (BdF)"][1]
p(f"3a. Titres détenus par les ménages fin 2025 [V BdF] : actions cotées {fr(PAT['Actions cotées (BdF)'][1], 0)} ;"
  f" non cotées et autres participations {fr(PAT['Actions non cotées et autres participations (BdF)'][1], 0)} ;"
  f" OPC actions {fr(opc_act, 0)} ; total {fr(dir_eq + opc_act, 0)} Md€ ; patrimoine net {fr(PAT['Valeur nette des ménages (B90)'][1], 0)}")
p("    Assiette couverte E (hors parts de SCI et autres participations hors art. 150-0 A, PEA, épargne salariale) [H]")
# Hypothèses du chiffrage (bas / central / haut), toutes [H] ; voir l'annexe.
JEUX = {
    "bas": dict(E=1200, b=0.017, lam=0.40, a=0.15, h=0.02, S=STOCK_EP23, T=35),
    "central": dict(E=1450, b=0.023, lam=0.55, a=0.30, h=0.04, S=STOCK_C, T=25),
    "haut": dict(E=1700, b=0.030, lam=0.70, a=0.45, h=0.06, S=STOCK_8UT[2024], T=15),
}
p("    jeu : E (Md€) ; b = part transmise par an (décès et donations) ; λ = part de plus-value latente dans la valeur")
p("    transmise ; a = part vendue par les héritiers dans l'année qui suit ; h = probabilité annuelle de vente ensuite ;")
p("    S = stock de reports (Md€) ; T = délai moyen jusqu'à la transmission (ans)")
p("    repères : flux total des transmissions ≈ 300 Md€ (CAE, note 69, 2021), soit 2,0 % du patrimoine net ;")
p("    actions et parts : 13 % du patrimoine net ; 300 × 13 % ≈ 39 Md€ transmis par an")
EFF = {}
for nom, q in JEUX.items():
    G_aut = q["E"] * q["b"] * q["lam"]
    G_rep = q["S"] / q["T"]
    L_aut, L_rep = PFU * G_aut, T_PV_REPORT * G_rep
    EFF[nom] = dict(q, G_aut=G_aut, G_rep=G_rep, L_aut=L_aut, L_rep=L_rep, L=L_aut + L_rep)
    p(f"   {nom:8s} : E {q['E']} b {q['b']:.1%} λ {q['lam']:.0%} -> plus-values effacées {fr(G_aut)} Md€/an"
      f" (impôt {fr(L_aut, 2)}) ; reports {fr(q['S'], 0)}/{q['T']} = {fr(G_rep)} (impôt {fr(L_rep, 2)}) ;"
      f" total effacé {fr(L_aut + L_rep, 2)} Md€/an = {fr(100 * (L_aut + L_rep) / PIB25, 2)} % du PIB")
p("   repères américains : Tax Foundation (2020) 11-12 Md$ par an, 0,05 % du PIB, transposé par le CAE à 1,3 Md€ ;")
p("   Trésor (dépenses fiscales FY2026) 37,8 Md$ en 2025 ; décès seulement, les donations y gardent le prix")
p("   d'acquisition du donateur ; taux de 23,8 % contre 31,4 %")
PIB_US25 = 30000.0      # [H, non vérifié] PIB américain de 2025, en Md$
US = {"TF": 0.0005, "Tresor": 37.8 / PIB_US25}
for k, v in US.items():
    p(f"   transposition {k} : {fr(100 * v, 3)} % du PIB × (31,4 / 23,8) × PIB français = "
      f"{fr(v * PFU / 0.238 * PIB25, 1)} Md€ (décès seuls ; les donations s'y ajoutent en France)")
J["us"] = {k: v * PFU / 0.238 * PIB25 for k, v in US.items()}


def profil(a, h, n=40):
    """Part de l'impôt d'une cohorte de transmissions encaissée k années après la transmission (k = 1..n) :
    a la première année, puis (1 − a)·h·(1 − h)^(k−2). La valeur des titres est supposée constante (prudent)."""
    return [a if k == 1 else (1 - a) * h * (1 - h) ** (k - 2) for k in range(1, n + 1)]


def recette_annee(L, a, h, n=40, debut=1, phi=None):
    """Recette de l'année y (y = 1 = première année d'application), somme des cohortes transmises à partir de 'debut'.
    phi(c) : part de l'impôt latent de la cohorte c soumise à la réforme (1 sans clause de droits acquis)."""
    pr = profil(a, h, n + 1)
    out = []
    for y in range(1, n + 1):
        s = 0.0
        for c in range(debut, y + 1):
            k = y - c + 1
            if 1 <= k <= len(pr):
                s += L * (phi(c) if phi else 1.0) * pr[k - 1] if k > 0 else 0.0
        out.append(s)
    return out


def va_cohorte(a, h, r):
    """Valeur actualisée, au moment de la transmission, de 1 € d'impôt latent transmis (continu pour la vente)."""
    return a / (1 + r) + (1 - a) * h / ((1 + r) * (r + h))


g_prix = 0.04       # [H] croissance nominale des valeurs (pour la clause de droits acquis à la date de la réforme)


def phi_droits_acquis(lam):
    """Clause de droits acquis : seule la plus-value acquise après l'entrée en vigueur est concernée."""
    return lambda c: min(1.0, (1 - (1 + g_prix) ** (-c)) / lam)


p("3b. Recette année par année (Md€) : reprise du prix d'acquisition (toutes plus-values) + report transmis sans")
p("    effacement (a_report = 0,1, même h) ; comparaison : expiration des seuls reports à la transmission (PLF 2027,")
p("    art. 5) et clause de droits acquis (plus-values acquises après la réforme ; reports existants hors champ) [C]")
PROF = {}
for nom, q in EFF.items():
    rec_aut = recette_annee(q["L_aut"], q["a"], q["h"])
    rec_rep = recette_annee(q["L_rep"], 0.10, q["h"])
    rec = [x + y for x, y in zip(rec_aut, rec_rep)]
    art5 = [q["L_rep"]] * 40                       # l'impôt des reports transmis est exigible à la transmission
    da = recette_annee(q["L_aut"], q["a"], q["h"], phi=phi_droits_acquis(q["lam"]))
    PROF[nom] = dict(prop=rec, art5=art5, droits_acquis=da)
    p(f"   {nom:8s} an 1 {fr(rec[0], 2)} ; an 3 {fr(rec[2], 2)} ; an 5 {fr(rec[4], 2)} ; an 10 {fr(rec[9], 2)} ; "
      f"an 20 {fr(rec[19], 2)} ; an 30 {fr(rec[29], 2)} ; moyenne ans 1-10 {fr(sum(rec[:10]) / 10, 2)}")
    p(f"            droits acquis : an 5 {fr(da[4], 2)} ; an 10 {fr(da[9], 2)} ; an 20 {fr(da[19], 2)} ;"
      f" moyenne 1-10 {fr(sum(da[:10]) / 10, 2)} ; art. 5 seul : {fr(art5[0], 2)} par an dès l'an 1")
J["profil"] = PROF

p("3c. Valeur actualisée d'une année de transmissions (Md€), au moment de la transmission [C]")
VA = {}
for nom, q in EFF.items():
    for r in R_ACT:
        v = q["L_aut"] * va_cohorte(q["a"], q["h"], r) + q["L_rep"] * va_cohorte(0.10, q["h"], r)
        VA[(nom, r)] = v
    p(f"   {nom:8s} impôt effacé {fr(q['L'], 2)} ; valeur actualisée (r = 2,5 / 3,5 / 5 %) "
      + " / ".join(fr(VA[(nom, r)], 2) for r in R_ACT)
      + f" ; soit {fr(100 * VA[(nom, 0.035)] / q['L'], 0)} % de l'impôt effacé (r = 3,5 %)")
J["va_cohorte"] = {f"{k[0]}_{k[1]}": v for k, v in VA.items()}

p("3d. Stock de reports d'apport-cession : valeur actualisée de l'impôt selon le traitement (Md€) [C]")
p("    hazards annuels : expiration du vivant e = expirés / stock (≈ 0,7 %) ; transmission m = 1/T ; vente des")
p("    héritiers h ; intérêt au taux d'actualisation si prévu")
REP = {}
for nom, q in EFF.items():
    S, T, h = q["S"], q["T"], q["h"]
    imp = T_PV_REPORT * S
    e = EXPIRES[2024] / STOCK_8UT[2024]
    m = 1 / T
    for r in R_ACT:
        den = r + e + m
        REP[(nom, r)] = dict(nominal=imp, actuel=imp * e / den, art5=imp * (e + m) / den,
                             transmis=imp * (e + m * h / (r + h)) / den, interet=imp * (e + m) / den)
    d = REP[(nom, 0.035)]
    p(f"   {nom:8s} impôt nominal {fr(imp, 1)} ; droit actuel {fr(d['actuel'], 1)} ; art. 5 {fr(d['art5'], 1)} ;"
      f" report transmis {fr(d['transmis'], 1)} ; transmis avec intérêt {fr(d['interet'], 1)} (r = 3,5 %)")
J["reports_va"] = {f"{k[0]}_{k[1]}": v for k, v in REP.items()}
for a_ in range(2021, 2025):
    p(f"   contrôle {a_} : entrées − expirés {fr(ENTREES[a_] - EXPIRES[a_], 1)}")
moy = sum(ENTREES[a_] for a_ in (2022, 2023, 2024)) / 3
p(f"   borne de très long terme : entrées moyennes 2022-2024 {fr(moy, 1)} Md€ × 30 % = {fr(0.3 * moy, 1)} Md€ par an")

p("3d bis. Sensibilité de la recette de l'an 10 et de la valeur actualisée d'une année de transmissions (r = 3,5 %)")
p("    à chaque paramètre, les autres au centre (jeux bas et haut) [C]")


def evalue(q):
    L_aut, L_rep = PFU * q["E"] * q["b"] * q["lam"], T_PV_REPORT * q["S"] / q["T"]
    an10 = recette_annee(L_aut, q["a"], q["h"])[9] + recette_annee(L_rep, 0.10, q["h"])[9]
    va = L_aut * va_cohorte(q["a"], q["h"], 0.035) + L_rep * va_cohorte(0.10, q["h"], 0.035)
    return an10, va


SENS = {}
c0 = JEUX["central"]
ref10, refva = evalue(c0)
NOMS_P = {"E": "titres couverts", "b": "part transmise par an", "lam": "part de plus-value latente",
          "a": "ventes la première année", "h": "ventes ensuite (par an)", "S": "stock de reports",
          "T": "délai avant transmission (reports)"}
for k in NOMS_P:
    lo, hi = dict(c0), dict(c0)
    lo[k], hi[k] = JEUX["bas"][k], JEUX["haut"][k]
    SENS[k] = dict(nom=NOMS_P[k], bas=evalue(lo), haut=evalue(hi), v_bas=JEUX["bas"][k], v_haut=JEUX["haut"][k])
    p(f"   {NOMS_P[k]:38s} : an 10 {fr(SENS[k]['bas'][0], 2)} à {fr(SENS[k]['haut'][0], 2)} ; VA "
      f"{fr(SENS[k]['bas'][1], 2)} à {fr(SENS[k]['haut'][1], 2)} (centre {fr(ref10, 2)} ; {fr(refva, 2)})")
J["sensibilite"] = dict(ref=[ref10, refva], par=SENS)

p("3e. Le haut de la distribution [H : 90 % de la recette payée par le top 1 %]")
PART_TOP1 = 0.90
HAUT = {}
for nom in EFF:
    rec = PROF[nom]["prop"]
    HAUT[nom] = dict(an5=PART_TOP1 * rec[4], an10=PART_TOP1 * rec[9], an30=PART_TOP1 * rec[29],
                     moy10=PART_TOP1 * sum(rec[:10]) / 10, va=PART_TOP1 * VA[(nom, 0.035)],
                     da10=PART_TOP1 * PROF[nom]["droits_acquis"][9])
    h = HAUT[nom]
    p(f"   {nom:8s} : an 5 +{fr(h['an5'], 2)} ; an 10 +{fr(h['an10'], 2)} ; an 30 +{fr(h['an30'], 2)} ; moyenne 1-10 "
      f"+{fr(h['moy10'], 2)} Md€ ; en % de l'impôt personnel du top 1 % sur ses revenus du capital (≈ "
      f"{fr(PFU * base_top1 + 1.0 + 0.4, 0)} Md€) : an 10 {fr(100 * h['an10'] / (PFU * base_top1 + 1.4), 0)} %"
      f" ; droits acquis an 10 +{fr(h['da10'], 2)}")
p("   IR-CSG : la charge du 1 % ne bouge pas (décision 3) ; la variation du haut dans cette partie vient donc de la")
p("   seule fermeture de l'effacement (PFU inchangé, CEHR gardée en majoration du PFU).")
J["haut"] = HAUT

# =====================================================================================================================
# 4. Arbitrages
# =====================================================================================================================
bloc("4. ARBITRAGES")
p("4a. Sort de la CEHR sur le capital : la supprimer coûterait 0,7 à 1,1 Md€ [H : 50-80 % de 1,41 Md€], moins la")
p("    part reprise par la CDHR pour les foyers à son plancher ; la garder en majoration du PFU : 0")
p("4b. Alignement des prélèvements sociaux à 18,6 % : " + fr(0.014 * (200 - 107), 2) + " Md€ (assiette restée à 17,2 % :"
  " 200 − 107 = 93 Md€) ; " + fr(0.014 * (A_PS_TOT - A_PS_HAUT), 2) + " avec l'assiette 204 ; alignement vers le bas"
  " (17,2 % pour tous) : −" + fr(0.014 * A_PS_HAUT, 2) + " Md€")
p("    petit épargnant : 60 000 € d'assurance-vie à 2,5 % -> +" + fr(0.014 * 1500, 0) + " € par an")
p("4c. Intérêt sur l'impôt différé (au taux d'actualisation, à compter de la transmission) : la valeur actualisée")
p("    d'une année de transmissions passe de VA à l'impôt encaissé sans actualisation [C]")
INT_ = {}
for nom, q in EFF.items():
    sans = VA[(nom, 0.035)]
    avec = q["L_aut"] * (q["a"] + (1 - q["a"])) + q["L_rep"]          # tout finit vendu (h > 0)
    INT_[nom] = (sans, avec)
    p(f"   {nom:8s} : {fr(sans, 2)} -> {fr(avec, 2)} Md€ (+{fr(avec - sans, 2)}), si tout finit par être vendu")
J["interet"] = INT_
p("4d. Franchise de 100 000 € de plus-value par transmission [H : 5 à 15 % de l'impôt effacé au-dessous]")
for nom, q in EFF.items():
    p(f"   {nom:8s} : coût {fr(0.05 * q['L'], 2)} à {fr(0.15 * q['L'], 2)} Md€ d'impôt latent par an")
p("4e. Déduire l'impôt latent de l'assiette des droits de succession [H : taux marginal effectif des DMTG sur ces")
p("    biens 10 à 40 %, Dutreil compris] : coût immédiat 10 à 40 % de l'impôt latent transmis")
for nom, q in EFF.items():
    p(f"   {nom:8s} : {fr(0.10 * q['L'], 2)} à {fr(0.40 * q['L'], 2)} Md€ par an")

# =====================================================================================================================
# 5. Cas types (personne seule ; barème de l'IR des revenus 2024, non indexé ; droit 2026)
# =====================================================================================================================
bloc("5. CAS TYPES")
SEUILS, TX = [0, 11497, 29315, 83823, 180294], [0, 0.11, 0.30, 0.41, 0.45]


def bareme(x):
    t = 0.0
    for i, s in enumerate(SEUILS):
        hi = SEUILS[i + 1] if i + 1 < len(SEUILS) else float("inf")
        t += TX[i] * max(0.0, min(x, hi) - s)
    return t


def cehr(r):
    return 0.03 * max(0, min(r, 500e3) - 250e3) + 0.04 * max(0, r - 500e3)


def cdhr(r, impot):
    if r <= 250e3:
        return 0.0
    decote = max(0.0, 0.20 * r - 0.825 * (r - 250e3))
    return max(0.0, 0.20 * r - decote - impot)


def capital(autre, div, inte, pv, ir_part=IR_PFU, ps=PS_HAUT, majoration=True):
    """Impôt sur les revenus du capital (en sus de l'impôt sur 'autre') : PFU, CEHR et CDHR ; puis option barème."""
    cap = div + inte + pv
    base_ir = bareme(autre)
    rfr = autre + cap
    ce_paye = cehr(rfr) if majoration else cehr(autre)      # sans majoration : CEHR sur les seuls autres revenus
    c = ce_paye - cehr(autre)
    d = cdhr(rfr, base_ir + ir_part * cap + ce_paye)          # la CDHR complète jusqu'à 20 % (IR + CEHR payée)
    pfu = ir_part * cap + ps * cap + c + d
    imp = autre + 0.6 * div + inte + pv - 0.068 * cap
    ir_b = bareme(imp)
    bar = ir_b - base_ir + PS_HAUT * cap + c + cdhr(rfr, ir_b + ce_paye)
    return pfu, bar


CAS = {}
# 1. Petit épargnant retraité
pf, ba = capital(19800, 800, 300, 0)
pf25, _ = capital(19800, 800, 300, 0, ir_part=0.064)
CAS["petit"] = dict(auj=min(pf, ba), pfu25=min(pf25, ba), bareme=ba, ps_align=0.014 * 1500,
                    heritiers_auj=0.0, heritiers_prop=PFU * 10000)
p(f"   Petit épargnant (pension 22 000 €, 800 € de dividendes, 300 € d'intérêts ; 30 000 € d'actions dont 10 000 €"
  f" de plus-value latente) : aujourd'hui {fr(min(pf, ba), 0)} € (option barème ; PFU {fr(pf, 0)}) ; PFU 25 % "
  f"{fr(min(pf25, ba), 0)} ; barème {fr(ba, 0)} ; alignement PS +21 € ; héritiers : 0 aujourd'hui, "
  f"{fr(PFU * 10000, 0)} € à la vente avec la proposition (0 avec une franchise)")
# 2. Cadre avec actions
pf, ba = capital(95000, 6000, 0, 4000)
pf25, _ = capital(95000, 6000, 0, 4000, ir_part=0.064)
CAS["cadre"] = dict(auj=pf, pfu25=pf25, bareme=ba, heritiers_prop=PFU * 120000)
p(f"   Cadre (95 000 € nets imposables, 6 000 € de dividendes, 4 000 € de plus-values ; portefeuille de 300 000 €"
  f" dont 120 000 € de plus-value latente) : {fr(pf, 0)} € ; PFU 25 % {fr(pf25, 0)} ({fr(pf25 - pf, 0)}) ; barème"
  f" {fr(ba, 0)} (+{fr(ba - pf, 0)}) ; héritiers : 0 aujourd'hui, {fr(PFU * 120000, 0)} € à la vente")
# 3. Dirigeant de PME : 400 000 € de bénéfice par an
BEN = 400e3
is_pme = 0.15 * 42500 + 0.25 * (BEN - 42500)
is_pme_c = is_pme   # contribution sociale non due (IS < 763 000 €)
dist = BEN - is_pme
ir_d = IR_PFU * dist
c = cehr(dist)
d = cdhr(dist, ir_d + c)
tot_d = is_pme + ir_d + c + d + PS_HAUT * dist
tot_h = is_pme + QPFC * IS_N * dist
CAS["dirigeant"] = dict(distribue=tot_d, holding=tot_h, taux_d=100 * tot_d / BEN, taux_h=100 * tot_h / BEN)
p(f"   Dirigeant de PME (bénéfice 400 000 €/an, IS {fr(is_pme, 0)} €) : tout distribué {fr(tot_d, 0)} € "
  f"({fr(100 * tot_d / BEN)} %, dont CDHR {fr(d, 0)}) ; gardé en holding {fr(tot_h, 0)} € ({fr(100 * tot_h / BEN)} %)")
th, _ = holding(R=0.05, N=25, k_heritiers=10)
p(f"     sur 25 ans à 5 % (valeur actualisée) : distribué {fr(th['A'])} % ; holding puis distribution {fr(th['B'])} % ;"
  f" holding transmise aujourd'hui {fr(th['C'])} % ; avec la proposition (héritiers sortent 10 ans après) "
  f"{fr(th['C_prop'])} %")
# 4. Entrepreneur qui cède : plus-value de 7,5 M€, apport-cession ; décès dans D ans ; héritiers h
G = 7.5e6
ENT = {}
for r in R_ACT:
    for D in (15, 20, 30):
        h = 0.04
        imp = PFU * G
        ENT[(r, D)] = dict(directe=imp, actuel=0.0, art5=imp / (1 + r) ** D,
                           transmis=imp / (1 + r) ** D * h / (r + h), interet=imp / (1 + r) ** D)
e0 = ENT[(0.035, 20)]
CAS["entrepreneur"] = e0
p(f"   Entrepreneur qui cède (plus-value 7,5 M€, décès dans 20 ans, r = 3,5 %, héritiers h = 4 %) : cession directe"
  f" {fr(e0['directe'] / 1e6, 2)} M€ ; apport-cession, droit actuel 0 (effacement au décès) ; art. 5 "
  f"{fr(e0['art5'] / 1e6, 2)} M€ en valeur actualisée ({fr(PFU * G / 1e6, 2)} M€ payés au décès) ; report transmis "
  f"{fr(e0['transmis'] / 1e6, 2)} M€ ; transmis avec intérêt {fr(e0['interet'] / 1e6, 2)} M€")
p("     variantes (r, D) : " + " ; ".join(f"r={r:.1%} D={D}: art5 {fr(v['art5'] / 1e6, 2)} transmis "
                                         f"{fr(v['transmis'] / 1e6, 2)}" for (r, D), v in ENT.items()))
p(f"     plus gros apporteurs (84 foyers, 280 M€ de plus-value chacun) : art. 5 = {fr(280 * 0.30, 0)} à "
  f"{fr(280 * 0.354, 0)} M€ chacun à la transmission")
J["entrepreneur"] = {f"{k[0]}_{k[1]}": v for k, v in ENT.items()}
# 5. Héritier : portefeuille coté de 2 M€, prix d'acquisition du défunt 0,8 M€, vendu 3 ans après à 2,1 M€
CAS["heritier"] = dict(auj=PFU * 0.1e6, prop=PFU * 1.3e6)
p(f"   Héritier (titres cotés de 2 M€ acquis 0,8 M€ par le défunt, vendus 2,1 M€ trois ans après) : aujourd'hui"
  f" {fr(PFU * 0.1e6, 0)} € ; proposition {fr(PFU * 1.3e6, 0)} € ; droits de succession inchangés")
# 6. Rentier
RENT = {}
for D_ in (400e3, 3e6):
    pf, ba = capital(0, D_, 0, 0)
    pf25, _ = capital(0, D_, 0, 0, ir_part=0.064)
    pf25ps, _ = capital(0, D_, 0, 0, ps=0.122)
    sans_cehr, _ = capital(0, D_, 0, 0, majoration=False)
    RENT[D_] = dict(auj=pf, pfu25_ir=pf25, pfu25_ps=pf25ps, bareme=ba, sans_cehr=sans_cehr)
    p(f"   Rentier, {fr(D_ / 1e3, 0)} k€ de dividendes : {fr(pf, 0)} € ({fr(100 * pf / D_)} %) ; PFU 25 % par l'IR "
      f"{fr(100 * pf25 / D_)} % ; par les PS {fr(100 * pf25ps / D_)} % ; barème {fr(100 * ba / D_)} % ; sans CEHR "
      f"{fr(100 * sans_cehr / D_)} %")
CAS["rentier"] = {str(int(k)): v for k, v in RENT.items()}
p(f"     à son décès, un portefeuille de 60 M€ dont 40 M€ de plus-value latente : impôt latent transmis "
  f"{fr(PFU * 40, 1)} M€ (0 aujourd'hui)")
J["cas"] = CAS

# =====================================================================================================================
# 6. Transition : droits acquis ou application immédiate
# =====================================================================================================================
bloc("6. TRANSITION")
for nom in EFF:
    pr, da = PROF[nom]["prop"], PROF[nom]["droits_acquis"]
    p(f"   {nom:8s} : cumul ans 1-10, application aux transmissions futures {fr(sum(pr[:10]), 1)} Md€ ; avec clause de"
      f" droits acquis {fr(sum(da[:10]), 1)} Md€ ({fr(100 * sum(da[:10]) / sum(pr[:10]), 0)} %)")
p("   Exit tax : plus-values en sursis déclarées (3WA, revenus 2024) " + fr(C2042["3WA"], 2) + " Md€ pour 358 foyers [V]")

(SORT / "calculs_pfu.txt").write_text("\n".join(L) + "\n", encoding="utf-8")
(SORT / "calculs_pfu.json").write_text(json.dumps(J, ensure_ascii=False, indent=1, default=float), encoding="utf-8")
print("\n".join(L))
