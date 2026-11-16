"""Bloc IR-CSG-CRDS (note8p) : proposition, variantes, efficacité, répartition, cas-types, bouclage.

Lancer depuis fiscalite/, après python3.13 note8p/calculs/ircsg_openfisca.py :
    python3 note8p/calculs/ircsg_proposition.py   ->  note8p/sorties/ircsg.json et ircsg_calculs.txt

Choix (arbitrages de l'auteur du 17/11/2026 ; exploration : ircsg_explore.py, sorties/ircsg_explore.csv) :
- assiette : revenu après cotisations sociales (salaire net de cotisations avant CSG, pension brute, revenus des
  indépendants et fonciers après cotisations, allocations chômage), de chaque adulte ; versements d'épargne retraite
  déductibles (plafonds actuels) ; aucune autre niche, sauf invalidité et dépendance (maintenues, coût 1,03 Md€) ;
- barème : 5 % jusqu'à 12 000 €, 20 % jusqu'à S1, 30 % jusqu'à 100 000 €, 45 % au-delà ; S1 calé sur la recette du
  périmètre puis arrondi au millier (44 000 €) ;
- enfants : franchise de 6 000 € par enfant, déduite par le parent au revenu le plus élevé (choix des parents) ;
- pensions au droit commun (aucun abattement, aucun taux réduit, aucune exonération propre) ;
- CEHR supprimée sur les revenus du barème (absorbée) ; CEHR et CDHR sur les revenus du capital : bloc capital.
"""
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import ircsg_modele as R  # noqa: E402

M, U = R.M, R.U
OUT = R.SORTIES
L = []
D = {}


def p(s=""):
    print(s, flush=True)
    L.append(s)


def f(v, d=0):
    return f"{v:,.{d}f}".replace(",", " ")


# ================================================================== 1. périmètre et recette
R25 = M.RECETTES["2025"]
NAT25 = dict(ir=103.626, csg=156.583, crds=9.270, pib=2991.056)       # comptes nationaux 2025 (synthese/situation_ircsg.py)
IR_PFU_BLOC = 8.43                                                    # IR au PFU, revenus 2025 (pfu/README.md)
D["perimetre"] = dict(
    definition="IR des revenus imposés au barème (salaires, pensions, chômage, revenus des indépendants, revenus fonciers),"
               " hors revenus du capital mobilier et plus-values (PFU et option pour le barème : bloc capital) ; CSG et CRDS"
               " des revenus d'activité et de remplacement ; CEHR due sur ces revenus",
    recettes_2025=dict(ir_bareme=R25["ir"], csg_activite=R25["csg_activite"], csg_pensions=R25["csg_pensions"],
                       csg_chomage=R25["csg_chomage"], crds=R25["crds"], total_modele=R25["total"]),
    cehr_bareme=R.CEHR_BAR, cehr_total=R.CEHR_TOTAL_2025, cdhr_total=R.CDHR_TOTAL_2025,
    avantages_maintenus=R.GARDES, cible=R.CIBLE,
    reconciliation_ir=dict(ir_comptes_nationaux_2025=NAT25["ir"], ir_ircom_porte_2025=R25["ir_ircom"],
                           ir_impute_capital_modele=R25["ir_pfu"], ir_pfu_mesure_bloc_capital=IR_PFU_BLOC,
                           ecart_non_attribue=R25["ir_pfu"] - IR_PFU_BLOC,
                           ecart_ircom_comptes_nationaux=NAT25["ir"] - R25["ir_ircom"]))
rc = D["perimetre"]["reconciliation_ir"]
p(f"[PÉRIMÈTRE 2025] IR barème {R25['ir']:.1f} + CSG {R25['csg']:.1f} (activité {R25['csg_activite']:.1f}, pensions"
  f" {R25['csg_pensions']:.1f}, chômage {R25['csg_chomage']:.2f}) + CRDS {R25['crds']:.1f} = {R25['total']:.1f} Md€ ;"
  f" + CEHR sur le barème {R.CEHR_BAR:.2f} (sur {R.CEHR_TOTAL_2025}) + avantages maintenus {sum(R.GARDES.values()):.2f}"
  f" -> recette à tenir {R.CIBLE:.2f} Md€")
p(f"[RÉCONCILIATION IR] comptes nationaux 2025 {NAT25['ir']:.1f} ; IRCOM porté en 2025 {R25['ir_ircom']:.1f} (écart"
  f" {rc['ecart_ircom_comptes_nationaux']:.1f} : CEHR, PFU payé hors déclaration, calendrier, non-résidents) ; le modèle"
  f" impute {R25['ir_pfu']:.1f} aux revenus du capital (12,8 % de 90 Md€ en 2024) quand le bloc capital mesure"
  f" {IR_PFU_BLOC} d'IR au PFU : {rc['ecart_non_attribue']:.1f} Md€ restent non attribués (IR sur dividendes et intérêts"
  f" imposés au barème par option, et erreur d'imputation)")


# ================================================================== 2. barème retenu
FE = 6000.0
S0, T0, T1, T2, S2, TOP = 12000.0, 0.05, 0.20, 0.30, 100000.0, 0.45


def sched_S1(S1, fe=FE, s0=S0, t=(T0, T1, T2, TOP), s2=S2):
    return R.bareme([0.0, s0, S1, s2], list(t))


def cale_S1(o, **k):
    lo, hi = 20e3, 99e3
    for _ in range(50):
        m = (lo + hi) / 2
        lo, hi = (lo, m) if R.recette(sched_S1(m, **k), o) < R.CIBLE else (m, hi)
    return (lo + hi) / 2


O = R.options(fe=FE)
S1_EXACT = cale_S1(O)
S1 = round(S1_EXACT / 1000) * 1000
SCHED = sched_S1(S1)
SEUILS, TAUX = [0.0, S0, S1, S2], [T0, T1, T2, TOP]
REC = R.recette(SCHED, O)
d1 = R.recette(R.bareme(SEUILS, [T0 + .01, T1 + .01, T2 + .01, TOP + .01]), O) - REC
d1b = R.recette(R.bareme(SEUILS, [T0, T1 + .01, T2 + .01, TOP]), O) - REC
dtop = R.recette(R.bareme(SEUILS, [T0, T1, T2, TOP + .01]), O) - REC
denf = R.recette(SCHED, R.options(fe=FE + 1000)) - REC
D["bareme"] = dict(seuils=SEUILS, taux=TAUX, S1_exact=S1_EXACT, franchise_enfant=FE, recette=REC, ecart=REC - R.CIBLE,
                   cout_par_point=dict(tous_taux=d1, taux_20_30=d1b, taux_45=dtop, franchise_enfant_1000=-denf))
p(f"\n[BARÈME] 5 % jusqu'à {f(S0)} €, 20 % jusqu'à {f(S1)} € (calage exact {f(S1_EXACT)}), 30 % jusqu'à {f(S2)} €, 45 %"
  f" au-delà ; franchise {f(FE)} € par enfant ; recette {REC:.2f} Md€ (écart {REC - R.CIBLE:+.2f})")
p(f"[POINT DE TAUX] tous les taux +1 point : {d1:.1f} Md€ ; 20 et 30 % : {d1b:.1f} ; 45 % : {dtop:.2f} ; 1 000 € de"
  f" franchise par enfant : {-denf:.2f} Md€")

# ================================================================== 3. efficacité : perte sèche et effets réels
PERC = {"vue_1": (1.0, 1.0), "vue_05": (0.5, 1.0), "vue_0": (0.0, 1.0), "vue_05_deux_marges": (0.5, 0.5),
        "vue_0_deux_marges": (0.0, 0.0)}
JEUX = ("bas", "central", "haut")


def efficacite(sched, o):
    out = {}
    for j in JEUX:
        for k, (v, ve) in PERC.items():
            e = R.evalue(sched, o, jeu=j, vue=v, vue_ext=ve)
            out[f"{j}_{k}"] = dict(gain=e["gain"], intensif=-e["reel"], extensif=-e["ext"], emplois=e["emplois"],
                                   decl=e["decl"], **R.effets_reels(e))
    return out


EFF = efficacite(SCHED, O)
# seuil de perception : part de la CSG perçue qui annule le gain central (marge extensive vue en entier)
lo, hi = 0.0, 1.0
for _ in range(30):
    m = (lo + hi) / 2
    lo, hi = (lo, m) if R.evalue(SCHED, O, vue=m, vue_ext=1.0)["gain"] > 0 else (m, hi)
VUE_SEUIL = (lo + hi) / 2
D["efficacite"] = dict(par_jeu_perception=EFF, perception_seuil=VUE_SEUIL, masse_travail=R.MASSE_TRAVAIL,
                       pib_2025=NAT25["pib"])
p("\n[EFFICACITÉ] variation de perte sèche réelle (gain, Md€/an), dont intensif / participation ; emplois (personnes)")
for k in PERC:
    p(f"  {k:20s} " + " | ".join(
        f"{j} {EFF[f'{j}_{k}']['gain']:+.2f} ({EFF[f'{j}_{k}']['intensif']:+.2f} / {EFF[f'{j}_{k}']['extensif']:+.2f} ;"
        f" {EFF[f'{j}_{k}']['emplois'] / 1e3:+.0f} k)" for j in JEUX))
c = EFF["central_vue_1"]
p(f"  seuil : le gain central s'annule si moins de {100 * VUE_SEUIL:.0f} % de la CSG d'aujourd'hui est perçue")
p(f"  effets réels (central, vue 1) : travail {c['travail_pct']:+.2f} % ; équivalents emplois moyens"
  f" {c['etp_milliers']:+.0f} k ; PIB (Cobb-Douglas, travail 2/3) {c['pib_court_pct']:+.2f} % à capital donné,"
  f" {c['pib_long_pct']:+.2f} % capital ajusté, soit {c['pib_long_pct'] / 100 * NAT25['pib']:+.0f} Md€ [H]")
p(f"  revenu déclaré (effet sur la recette, non compté) : {c['decl']:+.2f} Md€ (bas {EFF['bas_vue_1']['decl']:+.2f},"
  f" haut {EFF['haut_vue_1']['decl']:+.2f})")

# anticipation de l'impôt plus lourd sur les pensions futures (régime permanent)
EV = R.evalue(SCHED, O, repart=True)
PENS = float((M.W_R * M.ZNR).sum() / 1e9)
dtau = EV["groupes"]["retraites"]["Md"] / PENS
KAPPA = 0.274 * dtau
D["efficacite"]["pensions_futures"] = dict(dtau=dtau, kappa=KAPPA, **{
    f"theta_{t}": R.evalue(SCHED, O, kappa=KAPPA, theta=t)["gain"] for t in (0.0, 0.5, 1.0)})
pf = D["efficacite"]["pensions_futures"]
p(f"  pensions futures plus taxées : hausse du taux moyen sur les pensions {100 * dtau:.2f} points, κ = 0,274 × Δτ ="
  f" {100 * KAPPA:.2f} point ; gain si non vu {pf['theta_0.0']:.2f}, vu à moitié {pf['theta_0.5']:.2f}, vu {pf['theta_1.0']:.2f}")

# ================================================================== 4. répartition
var = U.variations(SCHED, O)
DIS = U.distribution(SCHED, O)
grp = EV["groupes"]
part = {}
for nom, g_, fam, w, dlt in var:
    if fam in ("couples0", "couples2"):
        s = float(nom.rsplit("_", 1)[1])
        k = f"{'retraites' if g_ == 'R' else fam}_{s}"
        a = part.setdefault(k, [0.0, 0.0])
        a[0] += (w * dlt).sum()
        a[1] += w.sum()
PARTAGE = {k: dict(eur=v[0] / v[1], Md=v[0] / 1e9, foyers_M=v[1] / 1e6) for k, v in part.items()}
D["repartition"] = dict(deciles_eur=EV["dec_eur"], deciles_foyers=EV["dec_foyers"], groupes=grp, distribution=DIS,
                        perdants500_pct=EV["perdants500"], top1_Md=EV["top1_Md"], top10_Md=EV["top10_Md"],
                        par_partage_couple=PARTAGE)
p("\n[RÉPARTITION] déciles (€ par foyer) : " + " ".join(f"{u:+.0f}" for u in EV["dec_eur"])
  + f" ; 10 % du haut {EV['top10_Md']:+.1f} Md€ ; 1 % {EV['top1_Md']:+.2f} Md€")
for k in ("actifs", "retraites", "seuls_actifs", "parents_isoles", "couples0_actifs", "couples2", "seuls_retraites",
          "couples0_retraites"):
    p(f"  {k:20s} {grp[k]['Md']:+6.1f} Md€ ; {grp[k]['eur']:+7,.0f} € par foyer ({grp[k]['foyers_M']:.1f} M)")
p("  couples selon le partage des revenus (part du premier) : " + " ; ".join(
    f"{k} {v['eur']:+,.0f} €" for k, v in sorted(PARTAGE.items())))
for k in ("tous", "actifs", "retraites", "couples2"):
    u = DIS[k]
    p(f"  {k}: P10 {u['p10']:+,.0f} P50 {u['p50']:+,.0f} P90 {u['p90']:+,.0f} € ; perdent > 500 € {u['perd500_M']:.1f} M,"
      f" > 1 000 € {u['perd1000_M']:.1f} M ; gagnent > 500 € {u['gagne500_M']:.1f} M (sur {u['foyers_M']:.1f} M)")

# ================================================================== 5. retraités : rendement de l'alignement
CSG_P = R25["csg_pensions"]
csg_plein = 0.083 * PENS                      # toutes les pensions au taux plein de 8,3 % : repère (CRDS non comptée)
csg_act = 0.092 * PENS                        # toutes les pensions au taux des revenus d'activité
DF = dict(abattement_10=5.322, abattement_age_157bis=0.419, demi_part_combattants_74=0.475)
D["retraites"] = dict(
    hausse_Md=grp["retraites"]["Md"], hausse_pct_pensions=100 * grp["retraites"]["Md"] / PENS, pensions_Md=PENS,
    charge_actuelle_Md=float(sum((w * M.CURT[n]).sum() for n, g_, _, w, _, _ in M.TYPES if g_ == "R") / 1e9),
    droit_actuel_reperes=dict(**DF, csg_taux_reduits_vers_taux_plein=csg_plein - CSG_P,
                              csg_vers_taux_activite=csg_act - CSG_P),
    distribution=dict(tous=DIS["retraites"], seuls=DIS["seuls_retraites"], couples=DIS["couples_retraites"]))
p(f"\n[RETRAITÉS] hausse {grp['retraites']['Md']:+.1f} Md€ ({D['retraites']['hausse_pct_pensions']:.1f} % des pensions"
  f" de {PENS:.0f} Md€ ; charge actuelle {D['retraites']['charge_actuelle_Md']:.1f}) ; retraité seul"
  f" {grp['seuls_retraites']['eur']:+,.0f} €, couple {grp['couples0_retraites']['eur']:+,.0f} €")
p(f"  repères en droit actuel (Md€, 2025) : abattement de 10 % {DF['abattement_10']} ; abattement des plus de 65 ans"
  f" {DF['abattement_age_157bis']} ; demi-part des anciens combattants {DF['demi_part_combattants_74']} ; CSG des pensions"
  f" au taux de 8,3 % pour tous : +{csg_plein - CSG_P:.1f} (approximation),"
  f" au taux de 9,2 % : +{csg_act - CSG_P:.1f}")

# ================================================================== 6. cas-types
CLES = [r for r in R.CAS.cle]
CAS = {k: R.cas_type(SCHED, O, k) for k in CLES}
D["cas_types"] = CAS
p("\n[CAS-TYPES] charge aujourd'hui (IR + CEHR + CSG + CRDS, OpenFisca) -> réforme, € par an")
for k, v in CAS.items():
    p(f"  {k:12s} {v['libelle'][:70]:70s} {v['auj']:9,.0f} -> {v['apres']:9,.0f} ({v['delta']:+8,.0f})")


def net(k, sched=SCHED, o=O):
    r = R.CAS[R.CAS.cle == k].iloc[0]
    base = sum(float(b) for b in str(r.bases).split(";"))
    return base - float(r.charge) - float(r.casa), base - R.impot_cas(sched, o, k) - float(r.casa)


# augmentation de 200 € net par mois
a0, a1 = net("sal_2000")
b0, b1 = net("sal_2200")
r0 = R.CAS[R.CAS.cle == "sal_2000"].iloc[0]
r2 = R.CAS[R.CAS.cle == "sal_2200"].iloc[0]
db = float(r2.bases) - float(r0.bases)
D["recit"] = dict(augmentation=dict(brut_avant=float(r0.bruts), brut_apres=float(r2.bruts),
                                    base_avant=float(r0.bases), base_apres=float(r2.bases), hausse_base=db,
                                    gain_net_auj=b0 - a0, gain_net_reforme=b1 - a1,
                                    taux_auj=100 * (1 - (b0 - a0) / db), taux_reforme=100 * (1 - (b1 - a1) / db),
                                    impot_auj=float(r0.charge), impot_reforme=CAS["sal_2000"]["apres"]))
ra = D["recit"]["augmentation"]
p(f"\n[RÉCIT] salarié à 2 000 € net/mois ({f(ra['brut_avant'])} € brut/an) qui passe à 2 200 € net ({f(ra['brut_apres'])} €"
  f" brut) : +{f(db)} € de revenu après cotisations ; il garde {f(ra['gain_net_auj'])} € aujourd'hui"
  f" ({ra['taux_auj']:.1f} % prélevés), {f(ra['gain_net_reforme'])} € après ({ra['taux_reforme']:.1f} %)")
# second conjoint
for cle0, cle1, lib in (("conj_0", "conj_mi", "sans enfant"), ("conj2_0", "conj2_mi", "deux enfants")):
    c0, c1 = R.CAS[R.CAS.cle == cle0].iloc[0], R.CAS[R.CAS.cle == cle1].iloc[0]
    sal2 = float(str(c1.bruts).split(";")[1])
    b2 = float(str(c1.bases).split(";")[1])
    t_auj = float(c1.charge) - float(c0.charge)
    t_ref = R.impot_cas(SCHED, O, cle1) - R.impot_cas(SCHED, O, cle0)
    # quotient conjugal plafonné (étape intermédiaire) : taux sur le premier euro et sur le mi-temps
    D["recit"][f"conjoint_{cle1}"] = dict(libelle=lib, salaire_brut_second=sal2, base_second=b2, impot_auj=t_auj,
                                          impot_reforme=t_ref, taux_auj=100 * t_auj / sal2, taux_reforme=100 * t_ref / sal2,
                                          charge_couple_auj=float(c1.charge), charge_couple_reforme=R.impot_cas(SCHED, O, cle1),
                                          charge_seul_salaire_auj=float(c0.charge),
                                          charge_seul_salaire_reforme=R.impot_cas(SCHED, O, cle0),
                                          taux_premier_euro_auj=None, taux_premier_euro_reforme=100 * T0)
    u = D["recit"][f"conjoint_{cle1}"]
    p(f"[RÉCIT] couple {lib}, premier salaire 35 000 € brut ; le second reprend un mi-temps au Smic ({f(sal2)} € brut,"
      f" {f(b2)} € après cotisations) : impôt supplémentaire {f(t_auj)} € aujourd'hui ({u['taux_auj']:.1f} % du brut),"
      f" {f(t_ref)} € après ({u['taux_reforme']:.1f} %) ; charge du couple {f(u['charge_couple_auj'])} -> {f(u['charge_couple_reforme'])} €")
# taux sur le premier euro du second conjoint aujourd'hui (OpenFisca : IR du couple au taux marginal du foyer + CSG-CRDS)
# prolongation d'activité
for s_, r_ in (("sen_sal", "sen_ret"), ("sen_sal2", "sen_ret2")):
    cs, cr = R.CAS[R.CAS.cle == s_].iloc[0], R.CAS[R.CAS.cle == r_].iloc[0]
    ns0, ns1 = net(s_)
    nr0, nr1 = net(r_)
    ecart = float(cs.bases) - float(cr.bases)
    D["recit"][f"prolongation_{s_}"] = dict(salaire_brut=float(cs.bruts), pension=float(cr.bruts), base_salaire=float(cs.bases),
                                            gain_auj=ns0 - nr0, gain_reforme=ns1 - nr1, ecart_avant_impot=ecart,
                                            taux_implicite_auj=100 * (1 - (ns0 - nr0) / ecart),
                                            taux_implicite_reforme=100 * (1 - (ns1 - nr1) / ecart))
    u = D["recit"][f"prolongation_{s_}"]
    p(f"[RÉCIT] 63 ans, salaire {f(float(cs.bruts))} € brut ou pension {f(float(cr.bruts))} € : une année de travail de plus"
      f" rapporte {f(u['gain_auj'])} € aujourd'hui, {f(u['gain_reforme'])} € après (impôt sur l'écart de revenu"
      f" {u['taux_implicite_auj']:.1f} % -> {u['taux_implicite_reforme']:.1f} %) ; pension inchangée par ailleurs")

# taux de prélèvement du premier salaire
PTR = {}
for k, base_k in (("seul_mi", None), ("jeune_smic", None)):
    r = R.CAS[R.CAS.cle == k].iloc[0]
    PTR[k] = dict(auj=100 * float(r.charge) / float(r.bruts), reforme=100 * CAS[k]["apres"] / float(r.bruts))
D["recit"]["premier_salaire"] = PTR
p("[PREMIER SALAIRE] prélèvement / salaire brut : " + " ; ".join(f"{k} {v['auj']:.1f} % -> {v['reforme']:.1f} %"
                                                               for k, v in PTR.items()))

# ================================================================== 7. variantes
VAR = {}


def resume(nom, sched, o, extra=None):
    e = R.evalue(sched, o, repart=True)
    e5 = R.evalue(sched, o, vue=0.5, vue_ext=1.0)
    e0 = R.evalue(sched, o, vue=0.0, vue_ext=1.0)
    g = e["groupes"]
    out = dict(nom=nom, recette=e["recette"], gain=e["gain"], gain_vue05=e5["gain"], gain_vue0=e0["gain"],
               emplois=e["emplois"], intensif=-e["reel"], extensif=-e["ext"], top1=e["top1_Md"], top10=e["top10_Md"],
               deciles=e["dec_eur"], perdants500=e["perdants500"],
               groupes={k: dict(Md=g[k]["Md"], eur=g[k]["eur"]) for k in g},
               cas={k: R.cas_type(sched, o, k)["delta"] for k in CLES}, **(extra or {}))
    return out


VAR["proposition"] = resume("Proposition", SCHED, O, dict(seuils=SEUILS, taux=TAUX, fe=FE))
# franchise par enfant : 4 000, 6 000 (retenue), 8 000 € ; S1 recalé
for fe in (4000.0, 8000.0):
    o_ = R.options(fe=fe)
    s1 = cale_S1(o_)
    VAR[f"franchise_{int(fe)}"] = resume(f"Franchise de {f(fe)} € par enfant", sched_S1(s1), o_,
                                         dict(seuils=[0, S0, s1, S2], taux=TAUX, fe=fe))
# seuil d'exonération au lieu du taux d'entrée : 0 % jusqu'à 10 000 €, puis 20/30/45, S1 recalé (si possible)
o_ = R.options(fe=FE)
t_exo = R.cale_echelle([0, 10e3, 44e3, S2], [0.0, T1, T2, TOP], [1, 2], o_)
VAR["seuil_exoneration"] = resume("Seuil d'exonération de 10 000 € (taux 20/30 recalés)", R.bareme([0, 10e3, 44e3, S2], t_exo), o_,
                                  dict(seuils=[0, 10e3, 44e3, S2], taux=list(t_exo), fe=FE))
# taux supérieur : 40 % ou 50 % (taux 20/30 recalés)
for top in (0.40, 0.50):
    t_ = R.cale_echelle(SEUILS, [T0, T1, T2, top], [1, 2], O)
    VAR[f"top_{int(100 * top)}"] = resume(f"Taux supérieur de {int(100 * top)} %", R.bareme(SEUILS, t_), O,
                                          dict(seuils=SEUILS, taux=list(t_), fe=FE))
# étape intermédiaire : quotient conjugal plafonné (2 000 €, 4 000 €, sans plafond), taux 20/30 recalés
for cap in (2000.0, 4000.0, 1e9):
    o_ = R.options(fe=FE, fam="qcp", qc_plafond=cap)
    t_ = R.cale_echelle(SEUILS, TAUX, [1, 2], o_)
    cle = "qc_sans_plafond" if cap > 1e8 else f"qc_plafond_{int(cap)}"
    VAR[cle] = resume(f"Quotient conjugal plafonné à {f(cap)} €" if cap < 1e8 else "Quotient conjugal sans plafond",
                      R.bareme(SEUILS, t_), o_, dict(seuils=SEUILS, taux=list(t_), fe=FE, plafond=cap))
# réforme naïve : IR actuel (barème, quotients, plafonds) sur l'assiette large + taux proportionnel, recette égale
o_n = dict(M.OPT0, fam="quotient", per=True)
lo, hi = -0.10, 0.20
for _ in range(45):
    t = (lo + hi) / 2
    lo, hi = (t, hi) if R.recette(U.empile(t), o_n) < R.CIBLE else (lo, t)
TAU_N = (lo + hi) / 2
VAR["naive"] = resume("Fusion naïve : IR actuel sur l'assiette large + taux proportionnel", U.empile(TAU_N), o_n,
                      dict(tau=TAU_N))
D["variantes"] = VAR
p("\n[VARIANTES] gain central (vue 1 / 0,5 / 0, marge extensive vue en entier) ; emplois ; retraités ; 1 % ; cas")
for k, v in VAR.items():
    g = v["groupes"]
    p(f"  {k:20s} gain {v['gain']:+.2f} / {v['gain_vue05']:+.2f} / {v['gain_vue0']:+.2f} ; emplois {v['emplois'] / 1e3:+.0f} k ;"
      f" retraités {g['retraites']['Md']:+.1f} ; couples avec enfants {g['couples2']['eur']:+,.0f} € ; parents isolés"
      f" {g['parents_isoles']['eur']:+,.0f} € ; 1 % {v['top1']:+.2f} ; {v.get('taux', v.get('tau'))}")
    p("      cas : " + " ; ".join(f"{k2} {d:+,.0f}" for k2, d in v["cas"].items() if k2 in (
        "couple2_60", "mono2_40", "mono2_60", "nomb4m_45", "nomb3m_35", "nomb3_60", "pi2_smic", "pi2_35", "couple0m_80",
        "jeune_smic", "ret_16", "retc_60")))

# ================================================================== 8. taux marginaux
MG = pd.read_csv(OUT / "ircsg_of_marges.csv") if (OUT / "ircsg_of_marges.csv").exists() else None


def marg_auj(profil, b):
    g = MG[(MG.profil == profil)]
    r = g.iloc[np.argmin(np.abs(g.base.values - b))]
    db_ = r.base_eff_plus - r.base_eff
    comp = {c: 100 * (r[c + "_plus"] - r[c]) / db_ for c in ("ir", "cehr", "cdhr", "csg", "crds")}
    comp["total"] = sum(comp.values())
    return comp


if MG is not None:
    niv = (10e3, 15e3, 19e3, 20.5e3, 25e3, 30e3, 38e3, 45e3, 60e3, 90e3, 110e3, 150e3, 200e3, 250e3, 300e3, 400e3, 600e3)
    TM = {}
    for b in niv:
        a = marg_auj("seul", b)
        TM[f"{b:.0f}"] = dict(auj=a, proposition=100 * float(SCHED[0](b)),
                              naive=100 * float(U.empile(TAU_N)[0](b)))
    TMR = {f"{b:.0f}": dict(auj=marg_auj("retraite_seul", b), proposition=100 * float(SCHED[0](b)))
           for b in (12e3, 15e3, 17.5e3, 20.5e3, 25e3, 32e3, 40e3, 60e3, 100e3)}
    D["taux_marginaux"] = dict(salarie_seul=TM, retraite_seul=TMR,
                               note="prélèvement sur 100 € de revenu après cotisations en plus (OpenFisca, revenus 2025)")
    p("\n[TAUX MARGINAUX, salarié seul, par 100 € de revenu après cotisations] aujourd'hui (IR + CEHR + CSG + CRDS) ->"
      " proposition ; naïve")
    for b, u in TM.items():
        a = u["auj"]
        p(f"  {float(b) / 1e3:6.1f} k€ : {a['total']:5.1f} % (IR {a['ir']:.1f}, CEHR {a['cehr']:.1f}, CDHR {a['cdhr']:.1f},"
          f" CSG {a['csg']:.1f}, CRDS {a['crds']:.2f}) -> {u['proposition']:.0f} % ; naïve {u['naive']:.1f} %")
    p("[TAUX MARGINAUX, retraité seul] " + " ; ".join(f"{float(b) / 1e3:.1f} k€ {u['auj']['total']:.1f} -> {u['proposition']:.0f} %"
                                                     for b, u in TMR.items()))
    # maximum observé aujourd'hui sur la grille, salarié seul
    g = MG[MG.profil == "seul"].copy()
    g["tm"] = 100 * ((g.ir_plus + g.cehr_plus + g.cdhr_plus + g.csg_plus + g.crds_plus)
                     - (g.ir + g.cehr + g.cdhr + g.csg + g.crds)) / (g.base_eff_plus - g.base_eff)
    hi_ = g[g.base >= 120e3]
    D["taux_marginaux"]["max_haut_auj"] = dict(max=float(hi_.tm.max()), base_au_max=float(hi_.base[hi_.tm.idxmax()]),
                                               au_dela_550k=float(g[g.base >= 550e3].tm.median()),
                                               entre_250_450k=float(g[(g.base >= 250e3) & (g.base <= 450e3)].tm.median()),
                                               entre_120_200k=float(g[(g.base >= 120e3) & (g.base <= 200e3)].tm.median()))
    p(f"  haut de la distribution aujourd'hui : médiane 120-200 k€ {D['taux_marginaux']['max_haut_auj']['entre_120_200k']:.1f} % ;"
      f" 250-450 k€ {D['taux_marginaux']['max_haut_auj']['entre_250_450k']:.1f} % ; au-delà de 550 k€"
      f" {D['taux_marginaux']['max_haut_auj']['au_dela_550k']:.1f} % ; maximum {D['taux_marginaux']['max_haut_auj']['max']:.1f} %")

# taux marginal de droit au sommet, par euro de revenu après cotisations (calcul de vérification)
cs_sup8 = 0.004                      # cotisations salariales marginales au-delà de 8 PASS : vieillesse déplafonnée
cs_4_8 = 0.004 + 0.0864 + 0.0108 + 0.0014   # entre 4 et 8 PASS : + Agirc-Arrco T2, CEG T2, CET (taux salariés 2025)
TOPTH = {}
for nom, cs in (("4_a_8_pass", cs_4_8), ("au_dela_8_pass", cs_sup8)):
    k = 1 / (1 - cs)                 # euros de brut par euro de revenu après cotisations
    imp = 1 - 0.068 * k              # revenu imposable par euro (CSG déductible de 6,8 % du brut, frais plafonnés)
    TOPTH[nom] = dict(ir=45 * imp, csg=9.2 * k, crds=0.5 * k, cehr3=3 * imp, cehr4=4 * imp)
    TOPTH[nom]["total_sans_cehr"] = TOPTH[nom]["ir"] + TOPTH[nom]["csg"] + TOPTH[nom]["crds"]
D["taux_marginaux_theoriques_haut"] = TOPTH
p("[TAUX DE DROIT AU SOMMET] par euro de revenu après cotisations : " + " ; ".join(
    f"{k} : IR {v['ir']:.1f} + CSG {v['csg']:.1f} + CRDS {v['crds']:.2f} = {v['total_sans_cehr']:.1f} %, + CEHR"
    f" {v['cehr3']:.1f} ou {v['cehr4']:.1f}" for k, v in TOPTH.items()))

# ================================================================== 9. bouclage annuel 2027-2040
MONTEE = {2027: 0.25, 2028: 0.5, 2029: 0.75}
DR, DA = grp["retraites"]["Md"], grp["actifs"]["Md"]
GARD = sum(R.GARDES.values())
ann = {}
for an in range(2027, 2041):
    lam = MONTEE.get(an, 1.0)
    ann[str(an)] = dict(ircsg_hausse_retraites=lam * DR, ircsg_baisse_actifs=lam * DA,
                        ircsg_cehr_bareme_absorbee=-lam * R.CEHR_BAR, ircsg_invalidite_dependance_maintenus=-lam * GARD,
                        ircsg_ecart_calage=lam * (REC - R.CIBLE), ircsg_crds_extinction_2034_droit_en_vigueur=0.0)
    ann[str(an)]["ircsg_total"] = sum(v for k, v in ann[str(an)].items())
CRDS_PTS = R25["crds"] / d1
D["annuel"] = ann
D["unites"] = ("Md€ au niveau 2025 (pas de croissance) ; + = recette en plus par rapport au droit de 2026 ; chaque foyer"
               " paie (1 − λ) × ancien impôt + λ × nouveau, λ = 0,25 / 0,5 / 0,75 / 1 de 2027 à 2030")
D["crds_2034"] = dict(recette_crds_perimetre=R25["crds"], baisse_points_tous_taux=CRDS_PTS,
                      note="extinction de la CRDS après 2033 (droit en vigueur) : la recette du nouvel impôt baisse"
                           " d'autant, par une baisse uniforme des taux ; ce n'est ni un coût ni une recette de la réforme")
D["cehr_cdhr"] = dict(cehr_bareme_absorbee=R.CEHR_BAR, cehr_capital=R.CEHR_TOTAL_2025 - R.CEHR_BAR,
                      cdhr="inchangée (capital, bloc PFU) ; supposée calculée en comptant comme « impôt sur le revenu » le"
                           " nouvel impôt diminué de 9,7 % des revenus du barème, ce qui laisse son produit inchangé",
                      fin_cdhr="droit en vigueur : jusqu'à l'imposition des revenus de l'année dont la loi de règlement constate"
                               " un déficit du budget général inférieur à 3 % du PIB (LF 2026) ; CEHR : jusqu'à un déficit"
                               " public nul (art. 223 sexies CGI)")
p(f"\n[BOUCLAGE] 2030 : retraités {DR:+.2f}, actifs {DA:+.2f}, CEHR {-R.CEHR_BAR:+.2f}, invalidité-dépendance {-GARD:+.2f},"
  f" écart de calage {REC - R.CIBLE:+.2f} -> total {ann['2030']['ircsg_total']:+.2f} Md€ ; CRDS 2034 : baisse de"
  f" {CRDS_PTS:.2f} point de tous les taux ({R25['crds']:.1f} Md€)")

D["status"] = {"recettes": "[E] comptes nationaux, CCSS, IRCOM ; [S] répartition du modèle", "bareme": "[C]",
               "perte_seche": "[S] sur élasticités [E] et hypothèses [H]", "perception_csg": "[H]",
               "effets_reels": "[S]/[H]", "cas_types": "[S] OpenFisca 176.1 (droit des revenus 2025)"}
json.dump(D, open(OUT / "ircsg.json", "w"), ensure_ascii=False, indent=1, default=float)
(OUT / "ircsg_calculs.txt").write_text("\n".join(L) + "\n", encoding="utf-8")
