"""Calculs transversaux de la synthèse d'ensemble (parties/ensemble.tex, introduction.tex, annexe_methode.tex).

Ce programme ne recalcule aucune réforme : il lit les sorties des quatre parties et appelle, sans les modifier, le
modèle IR-CSG (outils_ircsg.py, modele_purs.py) pour trois questions qui traversent les réformes.

1. Tableau d'ensemble : recette permanente, coût de transition, gain d'efficacité (central et fourchette), effet de
   recette non compté, qui paie ; fin de la contribution exceptionnelle sur l'IS et extinction de la CRDS fin 2033.
2. Trajectoire 2027-2036 des quatre réformes ensemble : solde annuel et dette cumulée de transition (intérêts au taux
   d'emprunt de l'État de la partie IS, 3,25 %).
3. Le haut de la distribution (1 % des foyers) : bilan des quatre réformes et compensation. Le modèle IR-CSG est
   relancé dans un sous-processus pour chaque convention de répartition des revenus au PFU entre tranches
   (CAPITAL = mixte, haut, prorata ; ir_csg/ir_csg.py) et, en sensibilité, avec un autre montant d'IR imputé aux revenus
   du capital (IMPUT_PFU, Md€ ; 11,52 dans le modèle, 10,2 au plus selon la partie PFU). Deux façons de rendre au 1 %
   un montant cible : V1, recette de la fusion constante (taux t1 recalé, seuil du taux de 50 % déplacé, comme
   outils_ircsg.cale_top1) ; V2, barème de la proposition inchangé jusqu'à 150 000 € de revenu imposé, puis pente plus
   douce jusqu'à 50 % (coût porté par le budget).
4. Cas-types cumulés : IR-CSG (cas-types OpenFisca de la partie), taxe foncière et droits de mutation (cas de la partie
   Immobilier), IS (sociétés types), revenus du capital et transmission (partie PFU) ; hypothèses en tête du bloc.
5. Gain d'efficacité total, part permanente, jeu de long terme ; incohérences de chiffres entre parties.

Lancer depuis fiscalite/ : python3 synthese/synthese_ensemble.py  ->  synthese/sorties/synthese_ensemble.{txt,json}
(environ une minute ; quatre sous-processus du modèle IR-CSG).
"""
import json
import os
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
SORT = HERE / "sorties"

# =====================================================================================================================
# Sous-processus : modèle IR-CSG dans une convention donnée (variables d'environnement CAPITAL et IMPUT_PFU)
# =====================================================================================================================
if len(sys.argv) > 1 and sys.argv[1] == "--ircsg":
    sys.path[:0] = [str(HERE), str(ROOT / "ir_csg"), str(ROOT)]
    imput = os.environ.get("IMPUT_PFU")
    if imput:                       # autre IR imputé aux revenus du capital : on réduit ir_autres dans chaque tranche
        import ir_csg as m
        _dist = m.distribution

        def _dist_patch(*a, **k):
            x, f = _dist(*a, **k)
            s = float(imput) / x.ir_autres.sum()
            x["ir_autres"] = x.ir_autres * s
            x["ir_trav"] = x.ir - x.ir_autres
            x["charge"] = x.ir_trav + x.csg
            f["ir_moy"] = f.tranche.map(dict(zip(x.tranche, x.ir_trav * 1e9 / x.foyers))).values
            return x, f
        m.distribution = _dist_patch
    import numpy as np  # noqa: E402
    import outils_ircsg as U  # noqa: E402
    M = U.M
    PJ = json.loads((SORT / "proposition_ircsg.json").read_text(encoding="utf-8"))
    C = PJ["choix"]
    O = U.options(F=C["F"], **PJ["base"])
    B0 = (C["t0"], C["tb"], C["z1"], C["t1"], C["z2"])
    S0 = U.bareme(*B0)
    tm0, _ = S0
    NOEUD = 150e3
    R150 = float(tm0(NOEUD))

    def resume(s, o=O):
        r = M.evalue("x", *s, o, sorties=True)
        g = {j: -M.evalue("x", *s, o, jeu=j, sorties=False)["v2"] for j in ("bas", "haut")}
        return dict(recette=float(r["recette"]), gain=float(-r["v2"]), gain_bas=float(g["bas"]),
                    gain_haut=float(g["haut"]), decl=float(r["v2_decl_recette"]), top1=float(r["top1_Md"]),
                    top10=float(r["top10_Md"]), dec=[float(u) for u in r["dec_eur"]],
                    dec_max=float(max(abs(u) for u in r["dec_eur"])),
                    retraites=float(r["groupes"]["retraites"]["Md"]),
                    cas={k: float(U.impot_cas(s, o, p, b) - U.charge_auj(p, b))
                         for k, p, b in (("cadre100", "seul", 100e3), ("cadre200", "seul", 200e3),
                                         ("cadre150", "seul", 150e3))})

    def v1(cible, top=0.50):
        """Recette constante : seuil z2 du taux de 50 % tel que Δ 1 % = cible, t1 recalé sur la recette."""
        def g(z2):
            t1 = U.cale_t1(C["t0"], C["tb"], C["z1"], z2, O, top)
            if t1 is None:
                return None, None
            return U.top1_md(U.bareme(C["t0"], C["tb"], C["z1"], t1, z2, top), O) - cible, t1
        a, b = np.log(60e3), np.log(5e6)
        ga, _ = g(np.exp(a))
        gb, _ = g(np.exp(b))
        if ga is None or gb is None or ga * gb > 0:
            return None
        for _ in range(40):
            c = (a + b) / 2
            gc, tc = g(np.exp(c))
            if abs(gc) < 0.01:
                break
            if (gc > 0) == (ga > 0):
                a, ga = c, gc
            else:
                b, gb = c, gc
        z2 = float(np.exp(c))
        s = U.bareme(C["t0"], C["tb"], C["z1"], tc, z2, top)
        return dict(z2=z2, t1=float(tc), **resume(s))

    def bar5(z2b):
        return U.ex.bareme_lineaire([0, 20e3, C["z1"], NOEUD, z2b], [C["t0"], C["tb"], C["t1"], R150, 0.50])

    def v2(cible):
        """Barème inchangé jusqu'à 150 000 € de revenu imposé ; seuil z2b du taux de 50 % tel que Δ 1 % = cible."""
        def g(z2b):
            return U.top1_md(bar5(z2b), O) - cible
        a, b = np.log(NOEUD + 5e3), np.log(2e7)
        ga, gb = g(np.exp(a)), g(np.exp(b))
        if ga * gb > 0:
            return dict(hors=True, top1_min=float(min(ga, gb) + cible), top1_max=float(max(ga, gb) + cible))
        for _ in range(50):
            c = (a + b) / 2
            gc = g(np.exp(c))
            if abs(gc) < 0.005:
                break
            if (gc > 0) == (ga > 0):
                a, ga = c, gc
            else:
                b, gb = c, gc
        z2b = float(np.exp(c))
        r = resume(bar5(z2b))
        return dict(z2b=z2b, cout=float(M.CIBLE - r["recette"]), **r)

    out = dict(cible=float(M.CIBLE), r150=R150, proposition=resume(S0))
    for T in (-0.5, -1.1, -1.5, -2.5, -4.0):
        out[f"v1_{T}"] = v1(T)
        out[f"v2_{T}"] = v2(T)
    for T in (0.0,):
        out[f"v1_{T}"] = v1(T)
        out[f"v2_{T}"] = v2(T)
    print("JSON" + json.dumps(out))
    sys.exit()

# =====================================================================================================================
# Programme principal
# =====================================================================================================================
L = []
J = {}


def p(s=""):
    print(s, flush=True)
    L.append(s)


def fr(x, d=1):
    if abs(x) < 0.5 * 10 ** -d:
        x = 0.0
    s = f"{x:,.{d}f}".replace(",", " ").replace(".", ",")
    return s.replace("-", "−")


def bloc(t):
    p("")
    p("=" * 116)
    p(t)
    p("=" * 116)


def lit(chemin):
    return json.loads(Path(chemin).read_text(encoding="utf-8"))


# ------------------------------------------------------------------ sorties des parties
PJ = lit(SORT / "proposition_ircsg.json")
TRI = lit(SORT / "transition_ircsg.json")
FON = lit(SORT / "calculs_foncier.json")
IS = lit(ROOT / "is/sorties/calculs_note_is.json")
PFU = lit(ROOT / "pfu/sorties/calculs_pfu.json")
PSA = (SORT / "perte_seche_autres.txt").read_text(encoding="utf-8")
PR = PJ["evaluations"]["proposition"]
R_ETAT = 0.0325                         # taux d'emprunt de l'État (partie IS, is/calculs_note_is.py)
ANS = list(range(2027, 2037))
PIB = 2991.1                            # PIB 2025, Md€ (Insee ; pfu/calculs_pfu.py)


def ps_is():
    """Perte sèche évitée sur le capital (IS, déduction totale) : linéaire et dégressif, ε = 0,5 / 1 / 1,6."""
    lin = [float(u) for u in re.search(r"100 %, régime actuel linéaire : ε = [^>]*-> ([-\d.]+) / ([-\d.]+) / ([-\d.]+)",
                                        PSA).groups()]
    deg = [float(u) for u in re.search(r"100 %, dégressif : ε = [^>]*-> ([-\d.]+) / ([-\d.]+) / ([-\d.]+)", PSA).groups()]
    return lin, deg


# ------------------------------------------------------------------ modèle IR-CSG : sous-processus par convention
def ircsg(conv, imput=None):
    env = dict(os.environ, CAPITAL=conv)
    env.pop("IMPUT_PFU", None)
    if imput:
        env["IMPUT_PFU"] = str(imput)
    return subprocess.Popen([sys.executable, __file__, "--ircsg"], env=env, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE, text=True, cwd=ROOT)


IMPUT_CORR = round(PFU["recettes"]["ir_pfu"], 1)       # 10,2 Md€ : IR au PFU, majorant de la partie PFU
procs = {"mixte": ircsg("mixte"), "haut": ircsg("haut"), "prorata": ircsg("prorata"),
         "mixte_imput": ircsg("mixte", IMPUT_CORR)}
IR = {}
for k, pr in procs.items():
    out, err = pr.communicate()
    if pr.returncode:
        raise RuntimeError(f"sous-processus {k} : {err[-2000:]}")
    IR[k] = json.loads(out.split("JSON", 1)[1])
J["ircsg_conventions"] = IR

# =====================================================================================================================
# 0. Repère : prélèvements obligatoires (OCDE, Revenue Statistics ; donnees/recettes_ocde_pct_pib.csv, catégorie _T)
# =====================================================================================================================
import pandas as pd  # noqa: E402
_oc = pd.read_csv(ROOT / "donnees/recettes_ocde_pct_pib.csv")
_oc = _oc[(_oc.categorie == "_T") & (_oc.annee == 2023)].sort_values("pct_pib", ascending=False).reset_index(drop=True)
_rg = int(_oc.index[_oc.code == "FRA"][0]) + 1
bloc("0. REPÈRE")
p(f"[OCDE 2023] prélèvements obligatoires de la France {fr(float(_oc.pct_pib[_rg - 1]), 1)} % du PIB, rang {_rg} sur"
  f" {len(_oc)} pays du fichier ; devant : {', '.join(_oc.pays[:_rg - 1])}")
J["ocde_2023"] = dict(pct=float(_oc.pct_pib[_rg - 1]), rang=_rg, n=len(_oc))

# =====================================================================================================================
# 1. Tableau d'ensemble
# =====================================================================================================================
bloc("1. TABLEAU D'ENSEMBLE (Md€ par an ; + = recette ou gain d'efficacité)")
lin, deg = ps_is()
G = {}
# IR-CSG
G["ircsg"] = dict(central=PR["gain_central"], bas=PR["gain_bas"], haut=PR["gain_haut"], long=PR["gain_long"],
                  perm_05=TRI["permanent"]["gains"]["0.5"]["central"], perm_1=TRI["permanent"]["gains"]["1.0"]["central"],
                  csg0=TRI["saillance"]["0.0"]["gain"]["central"], csg05=TRI["saillance"]["0.5"]["gain"]["central"])
# immobilier : convention centrale σ = 6, ε_K = 1 ; bas : ventes qui ne réagissent pas (σ = 0), ε_K = 0,5 ;
# haut : σ = 15 et coût d'usage de 3,5 % (annexe foncier, tableau tab:fon_ps)
ps = FON["ps"]
m_s = re.search(r"σ = 3 / 8 / 15 : ([-\d.]+) / ([-\d.]+) / ([-\d.]+)", (SORT / "calculs_foncier.txt").read_text())
v15 = float(m_s.group(3))
m_b = re.search(r"bâti : proposition ([-\d.]+) \(ε = 0,5 : ([-\d.]+) ; u = 3,5 % : ([-\d.]+)",
                (SORT / "calculs_foncier.txt").read_text())
b_c, b_05, b_35 = (float(u) for u in m_b.groups())
G["foncier"] = dict(central=-ps["total_log"], bas=-b_05, haut=-(v15 + b_35), autres=-ps["ventes_autres"],
                    ventes=-ps["ventes"], bati=-b_c)
G["is"] = dict(central=-(lin[1] + deg[1]) / 2, bas=-deg[0], haut=-lin[2])
G["pfu"] = dict(central=0.0, bas=0.0, haut=0.0)
tot = {k: sum(G[r][k] for r in ("ircsg", "foncier", "is", "pfu")) for k in ("central", "bas", "haut")}
tot["long"] = G["ircsg"]["long"] + G["foncier"]["central"] + G["is"]["central"]
tot["perm_05"] = G["ircsg"]["perm_05"] + G["foncier"]["central"] + G["is"]["central"]
tot["perm_1"] = G["ircsg"]["perm_1"] + G["foncier"]["central"] + G["is"]["central"]
tot["csg0"] = G["ircsg"]["csg0"] + G["foncier"]["central"] + G["is"]["central"]
tot["csg05"] = G["ircsg"]["csg05"] + G["foncier"]["central"] + G["is"]["central"]
G["total"] = tot

# effets de recette non comptés
decl = (PR["decl_bas"], PR["decl_central"], PR["decl_haut"])
tn = FON["taux_national"]
vol = float(re.search(r"coûte ([\d.]+) Md€ au lieu de ([\d.]+) \(×([\d.]+)\)",
                      (SORT / "calculs_foncier.txt").read_text()).group(3))
reprise = (tn["cut_log"] + tn["cut_aut"]) * (1 - vol)       # droits sur les ventes supplémentaires (σ = 6)
NC = dict(ircsg=decl, foncier=reprise, is_induit=0.89)

# IS : transition et contribution exceptionnelle
TRS = IS["transition"]
CE_2026, CE_PLF = 7.0, (5.0, 0.5)
# PFU : recette de la fin de l'effacement
PF = PFU["profil"]
pfu_c, pfu_b, pfu_h = PF["central"]["prop"], PF["bas"]["prop"], PF["haut"]["prop"]
moy10 = {k: sum(PF[k]["prop"][:10]) / 10 for k in ("bas", "central", "haut")}
# CRDS
CRDS_FUS = TRI["crds"]["recette_Md"]
PS_CAP = 204.0          # assiette des prélèvements sociaux du capital, Md€ (annexe PFU, tableau tab:pfu_a_assiette)
CRDS_CAP = 0.005 * PS_CAP

p(f"[IR-CSG] recette 0 par construction (220,1 Md€ avant réaction) ; transition 0 (convergence linéaire sur cinq ans,"
  f" recette constante chaque année) ; gain {fr(G['ircsg']['central'], 2)} ({fr(G['ircsg']['bas'], 2)} à"
  f" {fr(G['ircsg']['haut'], 2)} ; long terme {fr(G['ircsg']['long'], 2)} ; permanent {fr(G['ircsg']['perm_1'], 2)} à"
  f" {fr(G['ircsg']['perm_05'], 2)}) ; revenu déclaré non compté +{fr(decl[1])} ({fr(decl[0])} à {fr(decl[2])}) ;"
  f" retraités +{fr(PR['groupes']['retraites']['Md'])} Md€, actifs {fr(PR['groupes']['actifs']['Md'])}")
p(f"[IMMOBILIER] recette 0 à terme ; transition : déficit cumulé {fr(FON['transition']['5']['deficit'])} Md€ sur cinq ans"
  f" ({fr(FON['transition']['5']['deficit_vol'])} avec la reprise des ventes) ; gain {fr(G['foncier']['central'], 2)}"
  f" ({fr(G['foncier']['bas'], 2)} à {fr(G['foncier']['haut'], 2)} ; +{fr(G['foncier']['autres'], 2)} avec les autres"
  f" immeubles) ; non compté : droits sur les ventes supplémentaires +{fr(reprise)} Md€ ; taux national"
  f" {fr(tn['paye_log'])} logements, {fr(tn['paye_aut'])} entreprises, {fr(tn['paye_nu'])} terrains nus, pour"
  f" {fr(tn['cut_log'])} + {fr(tn['cut_aut'])} de droits en moins")
p(f"[IS] recette 0 à terme (excédent rendu par une baisse de {fr(TRS['baisse'], 2)} point après {TRS['extinction']}) ;"
  f" transition : dette maximale {fr(TRS['pic'])} Md€ en {TRS['an_pic']} ; coût permanent {fr(TRS['perm27']['mix'], 2)}"
  f" ({fr(TRS['perm27']['deg'], 2)} à {fr(TRS['perm27']['lin'], 2)}) ; gain {fr(G['is']['central'], 2)}"
  f" ({fr(G['is']['bas'], 2)} à {fr(G['is']['haut'], 2)}) ; non compté : investissement suscité (+10 % : +0,9 Md€ en"
  f" 2027, récupéré ensuite)")
p(f"[IS, droit en vigueur] fin de la contribution exceptionnelle : −{fr(CE_2026)} Md€ par an par rapport à 2026 ;"
  f" −{fr(CE_PLF[0])} en 2027 et −{fr(CE_PLF[1])} en 2028 par rapport au PLF 2027")
p(f"[PFU] fin de l'effacement : an 1 +{fr(pfu_c[0], 2)}, an 10 +{fr(pfu_c[9], 2)}, an 30 +{fr(pfu_c[29], 2)} ; moyenne"
  f" ans 1-10 +{fr(moy10['central'], 2)} ({fr(moy10['bas'], 2)} à {fr(moy10['haut'], 2)}) ; pas de transition ; gain"
  f" non chiffré (0 dans la mesure de la note)")
p(f"[CRDS, droit en vigueur] extinction fin 2033 : {fr(CRDS_FUS, 2)} Md€ sur le champ de la fusion (taux fusionné"
  f" {fr(TRI['crds']['points'], 2)} point en 2034 pour rester à recette constante) ; environ {fr(CRDS_CAP, 1)} Md€ sur les"
  f" revenus du capital (0,5 % de {fr(PS_CAP, 0)} Md€) : le PFU passe de 31,4 à 30,9 % si rien ne la remplace")
p(f"[GAIN TOTAL] {fr(tot['central'], 1)} Md€ ({fr(tot['bas'], 1)} à {fr(tot['haut'], 1)}) = {fr(100 * tot['central'] / PIB, 2)} %"
  f" du PIB ; long terme {fr(tot['long'], 1)} ; permanent (retraités actuels exclus) {fr(tot['perm_1'], 1)} à"
  f" {fr(tot['perm_05'], 1)} ; si la CSG n'est pas perçue {fr(tot['csg0'], 1)}, perçue à moitié {fr(tot['csg05'], 1)}")
p(f"   parts du gain central : IR-CSG {fr(100 * G['ircsg']['central'] / tot['central'], 0)} %, immobilier"
  f" {fr(100 * G['foncier']['central'] / tot['central'], 0)} %, IS {fr(100 * G['is']['central'] / tot['central'], 0)} % ;"
  f" gain de transition (retraités actuels) {fr(G['ircsg']['central'] - G['ircsg']['perm_05'], 1)} à"
  f" {fr(G['ircsg']['central'] - G['ircsg']['perm_1'], 1)}")
J["gains"] = G
J["non_comptes"] = NC
J["crds"] = dict(fusion=CRDS_FUS, capital=CRDS_CAP, points=TRI["crds"]["points"])

# =====================================================================================================================
# 2. Le haut de la distribution (calculé avant la trajectoire, qui inclut la compensation)
# =====================================================================================================================
CEHR = PFU["recettes"]["cehr"]                          # 1,41 Md€ (revenus 2023), tous revenus
CEHR_CAP = (0.5 * CEHR, 0.8 * CEHR)                     # part payée sur le capital : 50 à 80 % (hypothèse, partie PFU)
CEHR_BAR = (CEHR - CEHR_CAP[1], CEHR - CEHR_CAP[0])     # part payée sur les revenus du barème : 0,3 à 0,7
cehr_bar_c = sum(CEHR_BAR) / 2
cehr_cap_c = sum(CEHR_CAP) / 2
EFF1 = {k: PFU["haut"][k]["moy10"] for k in ("bas", "central", "haut")}   # fin de l'effacement, charge du 1 %
EFF1_an = {k: PFU["haut"]["central"][k] for k in ("an5", "an10", "an30")}
# immobilier : charge nette du taux national sur le sol des entreprises et les terrains nus (non localisée)
IMMO_NET_ENT = tn["paye_aut"] + tn["paye_nu"] - tn["cut_aut"]
IMMO_1 = (0.0, 0.5)                                      # part du 1 % : ordre de grandeur (hypothèse, voir le texte)
mix, hau, pro, imp = IR["mixte"], IR["haut"], IR["prorata"], IR["mixte_imput"]
TOP_IRCSG = dict(mixte=mix["proposition"]["top1"], haut=-2.8, prorata=3.7, imput=imp["proposition"]["top1"])
# haut et prorata : barème recalé sur la recette dans chaque convention (sorties/controle_hauts_purs.txt)


def bilan(top_ircsg, eff, cehr_bar, immo=0.0):
    return top_ircsg + eff - cehr_bar + immo


B = {}
B["central"] = bilan(TOP_IRCSG["mixte"], EFF1["central"], cehr_bar_c)
B["bas"] = bilan(TOP_IRCSG["mixte"], EFF1["bas"], CEHR_BAR[1], IMMO_1[0])
B["haut_fourchette"] = bilan(TOP_IRCSG["mixte"], EFF1["haut"], CEHR_BAR[0], IMMO_1[1])
B["conv_haut"] = bilan(TOP_IRCSG["haut"], EFF1["central"], cehr_bar_c)
B["conv_prorata"] = bilan(TOP_IRCSG["prorata"], EFF1["central"], cehr_bar_c)
B["imput"] = bilan(TOP_IRCSG["imput"], EFF1["central"], cehr_bar_c)
# compensation : 1) suppression de la majoration ex-CEHR sur le capital (la CEHR disparaît entièrement)
B_maj = {k: v - cehr_cap_c for k, v in B.items()}
# 2) cible pour le barème : ce qui reste dans la convention centrale
cible = round(B_maj["central"], 1)
v2c = mix[f"v2_{-cible}"] if f"v2_{-cible}" in mix else mix["v2_-1.1"]
v1c = mix[f"v1_{-cible}"] if f"v1_{-cible}" in mix else mix["v1_-1.1"]
bloc("2. LE HAUT DE LA DISTRIBUTION (1 % des foyers ; Md€ par an ; + = paie davantage)")
p(f"[FUSION IR-CSG] convention mixte (centrale) {fr(TOP_IRCSG['mixte'], 2)} ; convention haut {fr(TOP_IRCSG['haut'])}"
  f" (barème recalé, controle_hauts_purs.txt) ; prorata +{fr(TOP_IRCSG['prorata'])} ; mixte avec {fr(IMPUT_CORR)} Md€"
  f" d'IR imputé au PFU au lieu de 11,5 : {fr(TOP_IRCSG['imput'], 2)} (à barème inchangé)")
p(f"[CEHR] {fr(CEHR, 2)} Md€ (revenus 2023) ; part capital 50-80 % (hypothèse) : {fr(CEHR_CAP[0], 2)} à {fr(CEHR_CAP[1], 2)}"
  f" ; sa disparition sur les revenus du barème, non comptée dans la fusion, rend {fr(CEHR_BAR[0], 2)} à"
  f" {fr(CEHR_BAR[1], 2)} (centre {fr(cehr_bar_c, 2)}) au 1 %")
p(f"[EFFACEMENT] charge du 1 % (90 % de la recette) : moyenne ans 1-10 +{fr(EFF1['central'], 2)} ({fr(EFF1['bas'], 2)} à"
  f" {fr(EFF1['haut'], 2)}) ; an 5 +{fr(EFF1_an['an5'], 2)} ; an 10 +{fr(EFF1_an['an10'], 2)} ; an 30 +{fr(EFF1_an['an30'], 2)}")
p(f"[IMMOBILIER] logements du dixième de prix le plus cher : taxe moins droits +{fr(FON['prop']['tot'][9], 0)}"
  f" € par logement et par an (quasi neutre) ; sol des entreprises et terrains nus : +{fr(IMMO_NET_ENT, 2)} Md€ nets, non"
  f" localisés ; part du 1 % supposée de {fr(IMMO_1[0])} à {fr(IMMO_1[1])} Md€ (ordre de grandeur, hypothèse)")
p(f"[BILAN] central +{fr(B['central'], 2)} (de {fr(B['bas'], 2)} à {fr(B['haut_fourchette'], 2)}) ; convention haut"
  f" {fr(B['conv_haut'], 2)} ; prorata +{fr(B['conv_prorata'], 2)} ; IR imputé corrigé +{fr(B['imput'], 2)}")
p(f"[COMPENSATION 1 : suppression de la majoration ex-CEHR sur le capital, −{fr(cehr_cap_c, 2)}] central"
  f" +{fr(B_maj['central'], 2)} (de {fr(B_maj['bas'], 2)} à {fr(B_maj['haut_fourchette'], 2)}) ; convention haut"
  f" {fr(B_maj['conv_haut'], 2)} ; IR imputé corrigé {fr(B_maj['imput'], 2)}")
p(f"[COMPENSATION 2, convention centrale : rendre {fr(cible)} Md€ au 1 % par le barème]")
p(f"   V2 (si le calage confirme la convention centrale) : barème inchangé jusqu'à 150 000 € de revenu imposé ({fr(100 * mix['r150'], 1)} %), puis 50 % atteint à"
  f" {fr(v2c['z2b'] / 1e3, 0)} k€ au lieu de 265 k€ ; coût budgétaire {fr(v2c['cout'], 2)} Md€ ; Δ 1 % {fr(v2c['top1'], 2)} ;"
  f" dixième du haut {fr(v2c['top10'], 2)} ; gain {fr(v2c['gain'], 2)} ({fr(v2c['gain_bas'], 2)} à {fr(v2c['gain_haut'], 2)})"
  f" au lieu de {fr(mix['proposition']['gain'], 2)} ; revenu déclaré +{fr(v2c['decl'], 1)} ; décile le plus touché"
  f" {fr(v2c['dec_max'], 0)} € ; cadre à 200 000 € brut {fr(v2c['cas']['cadre200'], 0)} € (proposition"
  f" {fr(mix['proposition']['cas']['cadre200'], 0)})")
p(f"   V1 (pour mémoire) : recette de la fusion constante ; 50 % à {fr(v1c['z2'] / 1e3, 0)} k€ et taux à 25 k€ de"
  f" {fr(100 * v1c['t1'], 1)} % au lieu de 27,4 % : les autres foyers paient {fr(-v1c['top1'], 1)} Md€ de plus ; retraités"
  f" +{fr(v1c['retraites'], 1)} ; décile le plus touché {fr(v1c['dec_max'], 0)} €")
for conv, d in (("haut", hau), ("prorata", pro), ("mixte, IR imputé corrigé", imp)):
    z = d.get("v1_0.0") or {}
    p(f"   convention {conv} : neutralité du 1 % à recette constante → 50 % à {fr(z.get('z2', float('nan')) / 1e3, 0)} k€,"
      f" taux à 25 k€ {fr(100 * z.get('t1', float('nan')), 1)} %, décile le plus touché {fr(z.get('dec_max', float('nan')), 0)} € ;"
      f" recette à remplacer {fr(d['cible'], 1)} Md€")
COMP = dict(cehr_total=CEHR, cehr_bar=cehr_bar_c, cehr_cap=cehr_cap_c, bareme=v2c["cout"], total=CEHR,
            total_v2=CEHR + v2c["cout"])
p(f"[COMPENSATION RETENUE] la CEHR disparaît entièrement : coût {fr(CEHR, 2)} Md€ par an (dont {fr(cehr_bar_c, 2)} déjà"
  f" impliqués par la fusion) ; avec la pente plus douce du barème (V2), {fr(COMP['total_v2'], 2)} ; à comparer à la"
  f" recette de la fin de l'effacement : {fr(moy10['central'], 2)} en moyenne sur dix ans, dont {fr(EFF1['central'], 2)}"
  f" payés par le 1 %")
J["haut"] = dict(top_ircsg=TOP_IRCSG, cehr=dict(total=CEHR, cap=CEHR_CAP, bar=CEHR_BAR), effacement=EFF1,
                 effacement_an=EFF1_an, immo_ent=IMMO_NET_ENT, immo_1=IMMO_1, bilan=B, bilan_majoration=B_maj,
                 cible=cible, v2=v2c, v1=v1c, compensation=COMP)

# =====================================================================================================================
# 3. Trajectoire 2027-2036
# =====================================================================================================================
bloc("3. TRAJECTOIRE 2027-2036 (Md€ ; solde des réformes par rapport au droit en vigueur ; + = recette)")
cal = FON["calendrier5"]
traj = []
fon = [-cal[i]["deficit"] if i < 5 else 0.0 for i in range(10)]
fon_vol = [u * FON["transition"]["5"]["deficit_vol"] / FON["transition"]["5"]["deficit"] for u in fon]
is_c = [r["solde"] for r in TRS["rows"][:10]]


def soldes_de(dettes):
    out, prev = [], 0.0
    for d in dettes[:10]:
        out.append(prev * (1 + R_ETAT) - d)
        prev = d
    return out


is_60, is_90 = soldes_de(IS["dette_part"]["0.6"]), soldes_de(IS["dette_part"]["0.9"])
haut_l = [-COMP["total"]] * 10
haut_v2 = [-COMP["total_v2"]] * 10


def dette(soldes):
    d, out = 0.0, []
    for s in soldes:
        d = d * (1 + R_ETAT) - s
        out.append(d)
    return out


tot_c = [a + b + c + h for a, b, c, h in zip(fon, is_c, pfu_c[:10], haut_l)]
tot_sans = [a + b + c for a, b, c in zip(fon, is_c, pfu_c[:10])]
tot_v2 = [a + b + c + h for a, b, c, h in zip(fon, is_c, pfu_c[:10], haut_v2)]
tot_def = [a + b + c + h for a, b, c, h in zip(fon, is_90, pfu_b[:10], haut_l)]
tot_fav = [a + b + c + h for a, b, c, h in zip(fon_vol, is_60, pfu_h[:10], haut_l)]
d_c, d_sans, d_def, d_fav, d_v2 = dette(tot_c), dette(tot_sans), dette(tot_def), dette(tot_fav), dette(tot_v2)
report = [2.38 * min((i + 1) / 5, 1.0) for i in range(10)]          # avances du report, majorant (tous occupants)
report_cum = [sum(report[:i + 1]) for i in range(10)]
p("année : IR-CSG | fin de la CEHR | immobilier | IS | fin de l'effacement | total | dette (3,25 %) | sans"
  " compensation du haut : total, dette")
for i, a in enumerate(ANS):
    traj.append(dict(an=a, ircsg=0.0, haut=haut_l[i], foncier=fon[i], is_=is_c[i], pfu=pfu_c[i], total=tot_c[i],
                     dette=d_c[i], total_sans=tot_sans[i], dette_sans=d_sans[i], dette_def=d_def[i],
                     dette_fav=d_fav[i], total_v2=tot_v2[i], dette_v2=d_v2[i], ce=-CE_2026, report_cum=report_cum[i],
                     crds=-CRDS_FUS if a >= 2034 else 0.0))
    p(f"  {a} : 0 | {fr(haut_l[i], 2)} | {fr(fon[i], 2)} | {fr(is_c[i], 2)} | +{fr(pfu_c[i], 2)} | {fr(tot_c[i], 2)} |"
      f" {fr(d_c[i], 1)} | {fr(tot_sans[i], 2)}, {fr(d_sans[i], 1)}")
# au-delà de 2036 : IS (tableau de transition jusqu'en 2056) et effacement (profil sur 40 ans), compensation constante
_n = min(len(TRS["rows"]), 30)
_long = [(-cal[i]["deficit"] if i < 5 else 0.0) + TRS["rows"][i]["solde"] + pfu_c[i] - COMP["total"] for i in range(_n)]
_dl = dette(_long)
ext_c = next((2027 + i for i in range(_n) if _dl[i] <= 0), None)
_long_s = [u + COMP["total"] for u in _long]
_dls = dette(_long_s)
ext_s = next((2027 + i for i in range(_n) if _dls[i] <= 0), None)
imax = max(range(10), key=lambda i: d_c[i])
imax_s = max(range(10), key=lambda i: d_sans[i])
imax_v2 = max(range(10), key=lambda i: d_v2[i])
p(f"[DETTE, avec le barème V2 en plus] pic {fr(d_v2[imax_v2], 1)} en {ANS[imax_v2]}, {fr(d_v2[9], 1)} fin 2036")
p(f"[DETTE] avec la fin de la CEHR : pic {fr(d_c[imax], 1)} Md€ en {ANS[imax]} ({fr(100 * d_c[imax] / PIB, 2)} % du"
  f" PIB de 2025), {fr(d_c[9], 1)} fin 2036 ; sans : pic {fr(d_sans[imax_s], 1)} en {ANS[imax_s]}, {fr(d_sans[9], 1)} fin"
  f" 2036 ; défavorable (IS 90 % imposable, effacement bas) : pic {fr(max(d_def), 1)}, {fr(d_def[9], 1)} fin 2036 ;"
  f" favorable (IS 60 %, effacement haut, reprise des ventes) : pic {fr(max(d_fav), 1)}, {fr(d_fav[9], 1)} fin 2036")
p(f"[EXTINCTION] dette éteinte en {ext_c} avec la fin de la CEHR, en {ext_s} sans compensation (IS : baisse finale du"
  f" taux non comptée, elle n'intervient qu'après l'extinction de sa propre dette)")
p(f"[SOLDE] 2027 {fr(tot_c[0], 1)} ; 2031 {fr(tot_c[4], 1)} ; 2036 {fr(tot_c[9], 1)} ; premier excédent :"
  f" {next((ANS[i] for i in range(10) if tot_c[i] > 0), 'après 2036')} (sans compensation :"
  f" {next((ANS[i] for i in range(10) if tot_sans[i] > 0), 'après 2036')})")
p(f"[POUR MÉMOIRE, droit en vigueur] fin de la contribution exceptionnelle : −{fr(CE_2026)} Md€ chaque année par rapport à"
  f" 2026 (cumul 2027-2036 {fr(10 * CE_2026, 0)} Md€) ; CRDS : −{fr(CRDS_FUS, 1)} sur le champ de la fusion et −{fr(CRDS_CAP, 1)}"
  f" sur le capital à partir de 2034 par rapport à 2033")
p(f"[REPORT DE TAXE FONCIÈRE] avances (hors solde, dans la dette brute), majorant si tous les propriétaires occupants"
  f" reportent : {fr(report[4], 1)} Md€ par an en régime, {fr(report_cum[9], 1)} Md€ cumulés fin 2036 ; moitié environ"
  f" si le report est réservé aux 65 ans et plus (ordre de grandeur non vérifié)")
J["trajectoire"] = traj
J["dette"] = dict(extinction=ext_c, extinction_sans=ext_s, pic=d_c[imax], an_pic=ANS[imax], fin=d_c[9], pic_sans=d_sans[imax_s], an_pic_sans=ANS[imax_s],
                  fin_sans=d_sans[9], pic_v2=d_v2[imax_v2], an_pic_v2=ANS[imax_v2], fin_v2=d_v2[9],
                  pic_def=max(d_def), fin_def=d_def[9], pic_fav=max(d_fav), fin_fav=d_fav[9])

# =====================================================================================================================
# 4. Cas-types cumulés
# =====================================================================================================================
bloc("4. CAS-TYPES CUMULÉS (€ par an en régime permanent, après la transition ; + = paie davantage)")
R_ACT, N_DET = 0.03, 10                       # droits de mutation annualisés : sur dix ans de détention, à 3 %
ANN = R_ACT / (1 - (1 + R_ACT) ** -N_DET)
CASI = PR["cas"]
CASF = {c["cas"]: c for c in FON["cas"]}
PFU_T = 0.314
pme = IS["cas"]["PME industrielle"]
paris = CASF["Paris, appartement"]
st_tropez = next(t for t in FON["top"] if t[0] == "SAINT TROPEZ")
tf_paris_2m = paris["prop"] / paris["valeur"] * 2e6
v2_cad200 = v2c["cas"]["cadre200"] - mix["proposition"]["cas"]["cadre200"]
CEHR_RENT = 0.03 * (500e3 - 250e3) + 0.04 * (3e6 - 500e3)       # CEHR d'un rentier seul à 3 M€ de dividendes
va_cession = PFU["va_cohorte"]["central_0.035"] / (PFU_T * 1450 * 0.023 * 0.55 + 0.30 * 144 / 25)  # VA / impôt latent


def cas(cle, nom, revenu, ircsg, tf=0.0, droits=0.0, is_=0.0, pfu=0.0, transm=0.0, hyp="", notes=""):
    an = ircsg + tf - abs(droits) * ANN + is_ + pfu
    return dict(cle=cle, nom=nom, revenu=revenu, ircsg=ircsg, tf=tf, droits=-abs(droits), droits_an=-abs(droits) * ANN,
                is_=is_, pfu=pfu, total_an=an, pct=100 * an / revenu if revenu else None, transm=transm, hyp=hyp,
                notes=notes)


CT = [
    cas("retraite_province", "Retraité modeste propriétaire en province", 16000, CASI["ret16"]["delta"],
        tf=CASF["Limoges, maison"]["prop"],
        hyp="seul, 75 ans, pension de 16 000 € ; maison médiane de Limoges (171 800 €, taxe foncière 1 209 €) ; ne"
            " déménage pas ; épargne sur livrets",
        notes="hausse de taxe foncière reportable sur la succession ; Guéret : +26 € au lieu de +248 €"),
    cas("retraites_paris", "Couple de retraités propriétaire à Paris", 45000, CASI["rc45"]["delta"], tf=paris["prop"],
        transm=PFU_T * 80e3,
        hyp="pensions de 45 000 € (60/40) ; appartement parisien médian (416 200 €, taxe foncière 518 €) ; portefeuille"
            " de 200 000 € dont 80 000 € de plus-value latente",
        notes="hausse de taxe foncière reportable ; transmission : impôt dû par les héritiers quand ils vendent"),
    cas("primo_lyon", "Jeune couple primo-accédant, deux enfants, à Lyon", 50000, CASI["c2_50"]["delta"],
        tf=CASF["Lyon, appartement"]["prop"], droits=CASF["Lyon, appartement"]["eco"],
        hyp="salaires de 50 000 € brut (60/40) ; achète l'appartement lyonnais médian (279 200 €)",
        notes="si la hausse de taxe passe dans les prix (cas central), l'achat coûte environ 9 500 € de moins"),
    cas("monoactif_3enf", "Couple à un seul revenu, trois enfants, locataire", 60000, CASI["c3m_60"]["delta"],
        hyp="un salaire de 60 000 € brut ; locataire",
        notes="hypothèse : la taxe sur le sol ne passe pas dans les loyers (théorie) ; avec le quotient conjugal"
              " (repli, barème recalculé), +102 € au lieu de −1 003 €"),
    cas("cadre_paris", "Cadre parisien qui achète", 100000, CASI["cadre100"]["delta"], tf=paris["prop"],
        droits=paris["eco"], pfu=0.0, transm=PFU_T * 120e3,
        hyp="seul, 100 000 € brut ; achète l'appartement parisien médian ; 10 000 € de dividendes et plus-values"
            " par an (PFU inchangé) ; portefeuille de 300 000 € dont 120 000 € de plus-value latente",
        notes=""),
    cas("dirigeant", "Dirigeant de PME, holding transmise", 200000, CASI["cadre200"]["delta"], is_=pme["net"],
        transm=PFU_T * 5e6,
        hyp="seul, salaire de 200 000 € brut ; PME industrielle (bénéfice 300 000 €, 150 000 € de machines par an) ;"
            " holding de 6 M€ dont 5 M€ de plus-value latente à son décès",
        notes=f"impôt de sa société ; trésorerie 2027 : {fr(-pme['avance_net_2027'], 0)} € ; barème V2 :"
              f" {fr(v2_cad200, 0)} € de plus ; transmission : rien si les héritiers ne vendent ni ne liquident"),
    cas("rentier", "Rentier", 3e6, 0.0, tf=tf_paris_2m + st_tropez[2], transm=PFU_T * 40e6,
        hyp="3 M€ de dividendes par an (38,6 %, CDHR) ; portefeuille de 60 M€ dont 40 M€ de plus-value latente ;"
            " appartement parisien de 2 M€ et maison à Saint-Tropez",
        notes=f"suppression de la majoration : 0 tant que la CDHR existe, puis −{fr(CEHR_RENT, 0)} € par an"),
]
for c in CT:
    p(f"[{c['cle']}] {c['nom']} : IR-CSG {fr(c['ircsg'], 0)} ; taxe foncière {fr(c['tf'], 0)} ; droits {fr(c['droits'], 0)}"
      f" à l'achat ({fr(c['droits_an'], 0)} par an) ; IS {fr(c['is_'], 0)} ; PFU {fr(c['pfu'], 0)} ; total"
      f" {fr(c['total_an'], 0)} € par an ({fr(c['pct'], 1)} % du revenu) ; transmission : impôt latent"
      f" {fr(c['transm'], 0)} € (0 aujourd'hui)")
    p(f"      hypothèses : {c['hyp']}" + (f" ; {c['notes']}" if c["notes"] else ""))
p(f"[CONVENTIONS] droits annualisés sur {N_DET} ans à {fr(100 * R_ACT, 0)} % (facteur {fr(ANN, 4)}) ; IR-CSG au terme de la"
  f" transition de cinq ans (un cinquième par an), avant l'extinction de la CRDS en 2034 ; impôt latent transmis payé"
  f" par les héritiers à la vente ({fr(100 * va_cession, 0)} % en valeur actualisée à 3,5 % avec le rythme de ventes de la"
  f" partie PFU) ; Paris 2 M€ : hausse de l'appartement médian au prorata de la valeur ({fr(tf_paris_2m, 0)} €) ;"
  f" Saint-Tropez : maisons, +{fr(st_tropez[2], 0)} €")
J["cas_types"] = dict(cas=CT, annualisation=dict(r=R_ACT, n=N_DET, facteur=ANN), va_cession=va_cession)

# =====================================================================================================================
# 5. Incohérences entre parties
# =====================================================================================================================
bloc("5. INCOHÉRENCES ENTRE PARTIES")
import csv  # noqa: E402
C42 = {r["case"]: float(r["montant_eur"]) / 1e9 for r in csv.DictReader(open(ROOT / "donnees/ir_2042_cases_revenus2024.csv",
                                                                               encoding="utf-8"))}
av = C42["2CH"] + C42["2DH"] + C42["2ZZ"] + C42["2UU"]
mod90 = C42["2DC"] + C42["2TR"] + av + C42["2EE"] + C42["2TS"] + C42["3VG"] + C42["3VZ"]
pfu80 = PFU["assiette"]["total"]
p(f"[IR IMPUTÉ AU PFU] modèle IR-CSG : 12,8 % × 90 = 11,52 Md€ ; partie PFU : 12,8 % × {fr(pfu80, 1)} = "
  f"{fr(PFU['recettes']['ir_pfu'], 2)} (majorant, foyers au barème compris) ; acompte prélevé (2CK) 7,7 sur les seuls"
  f" dividendes et intérêts")
p(f"   les « 90 Md€ » = dividendes {fr(C42['2DC'], 1)} + intérêts {fr(C42['2TR'], 1)} + assurance-vie {fr(av, 1)} + autres"
  f" ({fr(C42['2EE'] + C42['2TS'], 1)}) + plus-values mobilières {fr(C42['3VG'], 1)} + plus-values immobilières"
  f" {fr(C42['3VZ'], 1)} = {fr(mod90, 1)} ; l'assiette du PFU retire l'assurance-vie, les plus-values immobilières et les"
  f" moins-values ({fr(C42['3VH'], 1)}) : écart d'IR {fr(0.128 * (mod90 - pfu80), 1)} Md€ ; l'assurance-vie paie 7,5 ou"
  f" 12,8 % après abattement, les plus-values immobilières 19 % chez le notaire (hors IRCOM : point non vérifié)")
p(f"   effet (convention mixte, IR imputé {fr(IMPUT_CORR)}) : recette à remplacer {fr(imp['cible'], 2)} au lieu de"
  f" {fr(mix['cible'], 2)} ; au barème proposé, la fusion rend {fr(imp['cible'] - imp['proposition']['recette'], 2)} Md€,"
  f" dont {fr(-imp['proposition']['top1'], 2)} au 1 % ; neutralité du 1 % à recette constante : 50 % à"
  f" {fr(imp['v1_0.0']['z2'] / 1e3, 0)} k€, taux à 25 k€ {fr(100 * imp['v1_0.0']['t1'], 1)} %, décile le plus touché"
  f" {fr(imp['v1_0.0']['dec_max'], 0)} €, gain {fr(imp['v1_0.0']['gain'], 2)}")
p(f"[CEHR] la fusion la supprime sur les revenus du barème sans le compter : {fr(CEHR_BAR[0], 2)} à {fr(CEHR_BAR[1], 2)} Md€"
  f" de recette et de baisse pour le 1 % (partie IR-CSG : « n'est comptée dans aucun cas »)")
p(f"[CRDS DU CAPITAL] la CRDS (0,5 %) fait partie des 18,6 % de prélèvements sociaux du PFU : son extinction fin 2033 fait"
  f" passer le PFU à 30,9 % et retire environ {fr(CRDS_CAP, 1)} Md€ ; la partie PFU dit que le taux « ne doit pas bouger »"
  f" sans le mentionner")
p("[PLUS-VALUES IMMOBILIÈRES] la partie PFU renvoie leur effacement à la transmission à la partie Immobilier, qui n'en"
  " traite pas")
p("[ZONES] la partie IS compte 0,54 Md€ pour la fin des exonérations zonées « d'IR et d'IS » ; la part d'IR (bénéfices"
  " des entreprises individuelles) relève aussi de l'assiette large de la fusion : double compte possible, de moins de"
  " 0,5 Md€ (part non publiée ; inclusion de ces bénéfices dans le revenu fiscal non vérifiée)")
p(f"[DATES] IR-CSG : revenus 2024 ; immobilier : ventes 2023-2024 et fiscalité locale 2024 ; IS : euros courants 2027 et"
  f" suivants ; PFU : revenus 2024, patrimoine fin 2025 ; la trajectoire additionne ces montants sans les indexer")
J["incoherences"] = dict(ir_pfu=dict(modele=11.52, pfu=PFU["recettes"]["ir_pfu"], acompte=7.67, mod90=mod90, av=av,
                                     pvi=C42["3VZ"], mv=C42["3VH"], cible_corr=imp["cible"],
                                     rend=imp["cible"] - imp["proposition"]["recette"],
                                     top1=imp["proposition"]["top1"], neutre=imp["v1_0.0"]),
                         cehr_bar=CEHR_BAR, crds_cap=CRDS_CAP)

# =====================================================================================================================
# Écriture
# =====================================================================================================================
(SORT / "synthese_ensemble.txt").write_text("\n".join(L).lstrip("\n") + "\n", encoding="utf-8")
(SORT / "synthese_ensemble.json").write_text(json.dumps(J, ensure_ascii=False, indent=1, default=float),
                                             encoding="utf-8")
