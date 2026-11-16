"""Bloc IR-CSG v3 : candidats, barème recommandé, versions financées, décomposition des recettes, cas-types, familles et
niches, second conjoint, efficacité, trajectoire. Lancer depuis fiscalite/ :  python3 note8p/calculs/ircsg3_proposition.py
Sorties : note8p/sorties/ircsg3.json, ircsg3_calculs.txt.

Barème recommandé (C2) : taux marginal de 2 % au premier euro, 16 % à 1 Smic (19 200 € de revenu après cotisations),
23 % à 1,5 Smic (28 800 €), 29 % à 2 Smic (38 400 €), 36 % à 3,5 Smic (67 100 €), puis montée linéaire jusqu'au
plafond de 48 % atteint au point Zp calé sur la recette (≈ 163 000 €) ; impôt = intégrale du taux marginal.
"""
import json

import numpy as np
import pandas as pd

import ircsg3_modele as N
import ircsg3_droit as DR
import ircsg3_baremes as B
import ircsg3_cascade as C

M, R, U = N.M, N.R, N.U
SZ = N.SMIC_Z
O = N.options()
OUT = N.SORTIES
L, D = [], {}


def p(s=""):
    print(s, flush=True)
    L.append(s)


def pts(zp):
    return [0.0, SZ, 1.5 * SZ, 2 * SZ, 3.5 * SZ, zp]


def cale_zp(t, top, cible, o=O):
    lo, hi = 60e3, 900e3
    for _ in range(45):
        m = (lo + hi) / 2
        lo, hi = (m, hi) if N.recette(N.continu(pts(m), list(t) + [top]), o) > cible else (lo, m)
    return (lo + hi) / 2


W_FIN = (0.5, 1.0, 1.0, 1.0, 0.5, 0.0)        # baisse financée : bas et milieu du barème (points 0 à 3,5 Smic)


def finance(p_, t_, F, o=O):
    def mk(e):
        return N.continu(p_, list(np.maximum(np.array(t_) - e * np.array(W_FIN), 0.0)))
    e = -N.cale(lambda x: mk(-x), o, N.CIBLE - F, lo=-0.12, hi=0.12)
    return mk(e), list(np.maximum(np.array(t_) - e * np.array(W_FIN), 0.0)), e


# ================================================================== 1. candidats
CANDIDATS = {
    "C1_plafond45": ((0.02, 0.16, 0.23, 0.29, 0.37), 0.45),
    "C2_plafond48": ((0.02, 0.16, 0.23, 0.29, 0.36), 0.48),
    "C3_plafond50": ((0.02, 0.16, 0.23, 0.29, 0.37), 0.50),
    "C4_precoce48": ((0.00, 0.16, 0.24, 0.30, 0.38), 0.48),
}
LIB = {"C1_plafond45": "Continu, plafond 45 %", "C2_plafond48": "Continu, plafond 48 % (recommandé)",
       "C3_plafond50": "Continu, plafond 50 %", "C4_precoce48": "Continu, montée précoce, plafond 48 %",
       "T2_tranches": "Tranches rapprochées (3 points)", "ancien": "Ancienne proposition 5/20/28/45",
       "ancien_recale": "Ancienne proposition recalée (frais réels)"}
BAR = {}
for k, (t, top) in CANDIDATS.items():
    zp = cale_zp(t, top, N.CIBLE)
    BAR[k] = dict(points=pts(zp), taux=list(t) + [top])


def tranches(p_, t_, pas=0.03):
    """Barème à tranches rapprochées qui suit le barème continu : un taux tous les `pas` points."""
    tm, _ = N.continu(p_, t_)
    z = np.arange(0, 600e3, 10.0)
    r = tm(z)
    niv = np.floor((r - t_[0]) / pas + 0.5)
    seuils, taux = [0.0], [float(t_[0] + pas * niv[0])]
    for i in range(1, len(z)):
        if niv[i] != niv[i - 1]:
            seuils.append(float(z[i]))
            taux.append(float(min(t_[0] + pas * niv[i], t_[-1])))
    return seuils, taux


s_, t_ = tranches(BAR["C2_plafond48"]["points"], BAR["C2_plafond48"]["taux"])
dd = N.cale(lambda d: R.bareme(s_, list(np.array(t_) + d)), O, N.CIBLE, lo=-0.03, hi=0.03)
BAR["T2_tranches"] = dict(seuils=s_, taux=list(np.array(t_) + dd), tranches=True)
ANC = ([0.0, 12000.0, 36500.0, 120000.0], [0.05, 0.20, 0.28, 0.45])
s1 = 36500.0
lo, hi = 15e3, 36.5e3
for _ in range(40):
    m = (lo + hi) / 2
    lo, hi = (m, hi) if N.recette(R.bareme([0, 12e3, m, 120e3], ANC[1]), O) > N.CIBLE else (lo, m)
BAR["ancien"] = dict(seuils=ANC[0], taux=ANC[1], tranches=True)
BAR["ancien_recale"] = dict(seuils=[0, 12e3, (lo + hi) / 2, 120e3], taux=ANC[1], tranches=True)


def sched(b):
    return R.bareme(b["seuils"], b["taux"]) if b.get("tranches") else N.continu(b["points"], b["taux"])


def efficacite(s, o=O):
    out = {}
    for j in ("bas", "central", "haut"):
        e = N.evalue(s, o, jeu=j)
        out[j] = dict(gain=e["gain"], intensif=-e["reel"], extensif=-e["ext"], emplois_milliers=e["emplois"] / 1e3,
                      **{k: v for k, v in R.effets_reels(e).items() if k in ("travail_pct", "etp_milliers", "dq_reel_Md",
                                                                               "dq_ext_Md", "salaire_moyen_entrant")},
                      revenu_declare_recette=e["decl"])
    return out


def part_gains(s, o=O):
    """Part des baisses d'impôt (somme des baisses) qui va au dixième et au centième le plus aisé."""
    gains, g10, g1, hausses = 0.0, 0.0, 0.0, 0.0
    for nom, g, f, w, parts, kids in M.TYPES:
        dlt = R.impot_adultes(*s, o, *M.adultes(g, parts, o), kids)[0] - M.CURT[nom]
        neg = np.clip(-dlt, 0, None) * w
        gains += neg.sum()
        g10 += (neg * (M.Q >= 0.9)).sum()
        g1 += (neg * (M.Q >= 0.99)).sum()
        hausses += (np.clip(dlt, 0, None) * w).sum()
    return dict(baisses_Md=gains / 1e9, hausses_Md=hausses / 1e9, part_d10=g10 / gains, part_top1=g1 / gains)


p("[CANDIDATS] recette constante (cible %.2f Md€ : IR barème + CSG + CRDS + CEHR du barème + invalidité)" % N.CIBLE)
RES = {}
for k, b in BAR.items():
    s = sched(b)
    ind = B.indicateurs(s, O)
    ind["efficacite"] = efficacite(s)
    ind["part_gains"] = part_gains(s)
    ind["bareme"] = b
    ind["recette"] = N.recette(s, O)
    RES[k] = ind
    a, e = ind["agregats"], ind["efficacite"]["central"]
    p(f"  {k:14s} {LIB[k]:40s} " + (f"plafond atteint à {b['points'][-1]:,.0f} €" if "points" in b else
                                     f"{len(b['taux'])} taux") +
      f" | Smic {ind['sal_smic']['mois']:+.0f} €/mois, 1,5 S {ind['sal_smic15']['mois']:+.0f}, 2 000 net"
      f" {ind['sal_net2000']['mois']:+.0f}, 3 S {ind['sal_smic3']['mois']:+.0f}, 120 k {ind['sal_cadre120']['mois']:+.0f},"
      f" 250 k {ind['sal_cadre250']['mois']:+.0f} | retraités " + " ".join(
          f"{ind[f'ret_{q}k']['delta']:+.0f}" for q in (12, 16, 20, 30, 60, 100)) +
      f" €/an | gain {e['gain']:.2f} Md€ (bas {ind['efficacite']['bas']['gain']:.2f}, haut"
      f" {ind['efficacite']['haut']['gain']:.2f}), participation {e['emplois_milliers']:+.0f} k, travail"
      f" {e['travail_pct']:+.2f} % | retraités {a['retraites']:+.1f} Md€, 10 % {a['top10']:+.1f}, 1 % {a['top1']:+.2f} ;"
      f" part des baisses au 10 % {100 * ind['part_gains']['part_d10']:.0f} %")
D["candidats"] = RES
D["libelles"] = LIB

# ================================================================== 2. recommandé et versions financées
REC = BAR["C2_plafond48"]
S0 = sched(REC)
VERS = {"F0": dict(points=REC["points"], taux=REC["taux"], e=0.0)}
for F in (3.0, 6.0):
    s, tt, e = finance(REC["points"], REC["taux"], F)
    VERS[f"F{int(F)}"] = dict(points=REC["points"], taux=tt, e=e)
p("\n[RECOMMANDÉ] C2 et versions financées (baisse des taux du bas et du milieu)")
for k, v in VERS.items():
    s = N.continu(v["points"], v["taux"])
    ind = B.indicateurs(s, O)
    ind["efficacite"] = efficacite(s)
    ind["part_gains"] = part_gains(s)
    v["ind"] = ind
    v["recette"] = N.recette(s, O)
    p(f"  {k}: taux {[round(100 * x, 2) for x in v['taux']]} aux points {[round(x) for x in v['points']]} ; recette"
      f" {v['recette']:.2f} | Smic {ind['sal_smic']['mois']:+.1f} €/mois, 1,5 S {ind['sal_smic15']['mois']:+.1f}, 2 000 net"
      f" {ind['sal_net2000']['mois']:+.1f}, 2 S {ind['sal_smic2']['mois']:+.1f}, 3 S {ind['sal_smic3']['mois']:+.1f}, 120 k"
      f" {ind['sal_cadre120']['mois']:+.0f}, 250 k {ind['sal_cadre250']['mois']:+.0f} | gain"
      f" {ind['efficacite']['central']['gain']:.2f}, participation {ind['efficacite']['central']['emplois_milliers']:+.0f} k")
D["recommande"] = VERS
# coûts unitaires (Md€) autour du barème recommandé
base = N.recette(S0, O)
cu = {}
cu["un_point_tous_taux"] = N.recette(N.continu(REC["points"], list(np.array(REC["taux"]) + 0.01)), O) - base
cu["un_point_bas_milieu"] = N.recette(N.continu(REC["points"], list(np.array(REC["taux"]) + 0.01 * np.array(W_FIN))), O) - base
cu["un_point_plafond"] = N.recette(N.continu(REC["points"], REC["taux"][:-1] + [REC["taux"][-1] + 0.01]), O) - base
cu["franchise_1000"] = base - N.recette(S0, N.options(fe=7000.0))
cu["smic_euros_mois_par_Md"] = (VERS["F6"]["ind"]["sal_smic"]["mois"] - VERS["F0"]["ind"]["sal_smic"]["mois"]) / 6
cu["adultes_M"] = float(sum((w * len(pp)).sum() for n, g, f, w, pp, k in M.TYPES) / 1e6)
D["couts_unitaires"] = cu
p(f"[COÛTS] un point sur tous les taux {cu['un_point_tous_taux']:.1f} Md€ ; sur le bas et le milieu"
  f" {cu['un_point_bas_milieu']:.1f} ; plafond {cu['un_point_plafond']:.2f} ; 1 000 € de franchise par enfant"
  f" {cu['franchise_1000']:.2f} ; 1 Md€ de baisse financée = {cu['smic_euros_mois_par_Md']:.2f} €/mois au Smic ;"
  f" {cu['adultes_M']:.1f} M d'adultes")

# franchise 5 000 / 7 000 € (barème recalé par le point Zp, à défaut par le bas et le milieu)
FRV = {}
for fe in (5000.0, 7000.0):
    o_ = N.options(fe=fe)
    s, tt, e = finance(REC["points"], REC["taux"], 0.0, o_)
    ind = B.indicateurs(s, o_, eff=False)
    FRV[int(fe)] = dict(taux=tt, decalage_points=-100 * e, **{k: ind[k]["delta"] for k in ind if k != "agregats"})
    p(f"[FRANCHISE {fe:,.0f} €] taux du bas et du milieu {100 * -e:+.2f} point ; couple 2 enf. 60 k"
      f" {ind['couple_2enf_60k']['delta']:+.0f}, mono-actif 60 k {ind['couple_2enf_mono_60k']['delta']:+.0f}, 3 enf."
      f" {ind['couple_3enf_60k']['delta']:+.0f} ; Smic {ind['sal_smic']['mois']:+.1f} €/mois")
D["franchise_variantes"] = FRV

# sensibilités de la recette à tenir
SENS = {}
for nom, dc in (("ir_non_attribue_4Md", 4.0), ("ri_source_etrangere_moitie", 1.9), ("frais_reels_plus_10Md", None)):
    if dc is None:
        old = M.DED_PER.copy()
        M.DED_PER = old + N.FR * 10e9 / N.FR_TOTAL
        s, tt, e = finance(REC["points"], REC["taux"], 0.0)
        M.DED_PER = old
    else:
        s, tt, e = finance(REC["points"], REC["taux"], -dc)
    SENS[nom] = dict(points_bas_milieu=-100 * e, smic_mois=B.indicateurs(s, O, eff=False)["sal_smic"]["mois"])
D["sensibilites_recette"] = SENS
p("[SENSIBILITÉS] " + " ; ".join(f"{k} : {v['points_bas_milieu']:+.2f} point, Smic {v['smic_mois']:+.1f} €/mois"
                                   for k, v in SENS.items()))

# ================================================================== 3. décomposition des recettes
for cle, sc in (("recommande", S0), ("ancien", sched(BAR["ancien"]))):
    res, _ = C.cascade(sc, O)
    D[f"cascade_{cle}"] = [dict(etape=a, libelle=b, **{k: v for k, v in c.items()}) for a, b, c in res]
    p(f"\n[CASCADE, {cle}] Md€ (+ = recette) ; actifs / retraités ; 1-5e déciles / 10e décile / 1 %")
    for a, b, c in res:
        dec = c.get("deciles_Md")
        p(f"  {b:52s} {c['Md']:+7.2f}" + (f" | A {c['actifs']:+6.2f} R {c['retraites']:+6.2f} | D1-5 {sum(dec[:5]):+6.2f}"
                                           f" D10 {dec[-1]:+6.2f} 1 % {c['top1_Md']:+5.2f}" if dec else ""))
VM = pd.read_csv(N.R.RACINE / "ir_csg/sorties/depenses_fiscales_ir_plf2026.csv")
cat = VM.groupby(VM.categorie.str[:2]).cout_2025_convention_Meur.sum() / 1e3
top_rici = VM[VM.categorie.str.startswith("A")].sort_values("cout_2025_convention_Meur", ascending=False).head(12)
D["voies_et_moyens"] = dict(par_categorie_Md={k: float(v) for k, v in cat.items()},
                            principales_rici=[dict(code=int(r.code), mesure=r.mesure[:90], Md=r.cout_2025_convention_Meur / 1e3)
                                              for r in top_rici.itertuples()])
p("[VOIES ET MOYENS, PLF 2026, coût 2025, Md€] " + " ; ".join(f"{k} {v:.2f}" for k, v in cat.items()))

# ================================================================== 4. cas-types
CAS = {k: R.cas_type(S0, O, k) for k in R.CAS.cle}
CAS_F = {F: {k: R.cas_type(N.continu(VERS[F]["points"], VERS[F]["taux"]), O, k)["delta"] for k in R.CAS.cle} for F in VERS}
D["cas_types"] = CAS
D["cas_types_finances"] = CAS_F
p("\n[CAS-TYPES, C2] aujourd'hui -> après (€/an ; €/mois)")
for k, v in CAS.items():
    p(f"  {k:12s} {v['libelle'][:62]:62s} {v['auj']:8,.0f} -> {v['apres']:8,.0f} ({v['delta']:+7,.0f} ; {v['delta'] / 12:+6.0f}/mois)"
      f" F3 {CAS_F['F3'][k]:+6.0f} F6 {CAS_F['F6'][k]:+6.0f}")

# courbes : salarié seul selon le brut mensuel, retraité seul selon la pension
g = U.CTN[U.CTN.profil == "seul"].sort_values("brut")
gr = U.CTN[U.CTN.profil == "retraite_seul"].sort_values("brut")
COURBES = {"salarie": [], "retraite": []}
SCH = {k: sched(BAR[k]) for k in ("C1_plafond45", "C2_plafond48", "C3_plafond50", "C4_precoce48", "ancien", "ancien_recale")}
SCH.update({"C2_F3": N.continu(VERS["F3"]["points"], VERS["F3"]["taux"]), "C2_F6": N.continu(VERS["F6"]["points"], VERS["F6"]["taux"])})
for b in np.arange(1000.0, 25001.0, 250.0):
    bb = 12 * b
    z = float(np.interp(bb, g.brut, g.base_a))
    a = float(np.interp(bb, g.brut, g.ir + g.csg + g.crds))
    COURBES["salarie"].append(dict(brut_mensuel=b, z=z, auj=a, **{k: float(N.impot_z(s, O, [z])[0]) - a for k, s in SCH.items()}))
for pe in np.arange(6000.0, 150001.0, 1000.0):
    a = float(np.interp(pe, gr.brut, gr.ir + gr.csg + gr.crds))
    COURBES["retraite"].append(dict(pension=pe, auj=a, **{k: float(N.impot_z(s, O, [pe])[0]) - a for k, s in SCH.items()}))
D["courbes"] = COURBES
for q in (10e3, 12e3, 14e3, 16e3, 18e3, 20e3, 25e3, 30e3, 40e3, 60e3, 80e3, 100e3):
    r_ = [r for r in COURBES["retraite"] if r["pension"] == q][0]
    p(f"  retraité seul {q / 1e3:.0f} k€ : aujourd'hui {r_['auj']:,.0f} ; C2 {r_['C2_plafond48']:+,.0f} ; ancienne {r_['ancien']:+,.0f}")

# ================================================================== 5. familles : configurations et niches
FAM = {}
for prof, kids in (("couple_2enf", 2), ("couple_2enf_mono", 2), ("couple_3enf", 3), ("couple_3enf_mono", 3),
                   ("parent_isole_2enf", 2), ("couple_0enf_mono", 0), ("couple_0enf", 0), ("retraite_couple", 0)):
    gg = U.CTN[U.CTN.profil == prof]
    rows = []
    for bb in (20e3, 30e3, 40e3, 50e3, 60e3, 80e3, 100e3, 150e3):
        r = gg.iloc[np.argmin(np.abs(gg.brut.values - bb))]
        zs = [r.base_a] + ([r.base_b] if prof.startswith(("couple", "retraite_couple")) else [])
        a = r.ir + r.csg + r.crds
        rows.append(dict(brut=bb, auj=a, **{k: float(N.impot_z(SCH[k], O, zs, kids)[0]) - a for k in ("C2_plafond48", "ancien")}))
    FAM[prof] = rows
D["familles_courbes"] = FAM


def foyer_cas(bruts, kids, nat="A", isole=False):
    ad = []
    for b in bruts:
        if nat == "A":
            z = B.z_brut(b) if b > 0 else 0.0
            ad.append(("A", np.array([z]), z / b if b > 0 else 0.885))
        else:
            ad.append(("R", np.array([b]), 1.0))
    return ad


def decompose(lib, bruts, kids, niches, nat="A", isole=False):
    """Perte des avantages / variation d'assiette / gain de barème (franchise comprise) / net, €/an."""
    ad = foyer_cas(bruts, kids, nat, isole)
    c0 = DR.charge(ad, kids, isole)
    ir0 = float(c0["ir"][0])
    # valeur des niches (droit 2025, paramètres OpenFisca 176.1) ; réductions limitées à l'impôt, crédits remboursables
    v_cred, v_red = 0.0, 0.0
    for typ, mt in niches:
        if typ == "emploi_domicile":
            v_cred += 0.5 * min(mt, min(12000 + 1500 * kids, 15000))
        elif typ == "garde":
            v_cred += 0.5 * min(mt, 3500.0)
        elif typ == "dons":
            v_red += 0.66 * mt
    v_red = min(v_red, ir0)
    avec = float(c0["total"][0]) - v_cred - v_red
    sans = float(c0["total"][0])
    fl_all = dict(abatpen=False, age=False, csg_reduit=False, conjugal=False, qf=False, csg_ded=False, forfait=False)
    elargi = float(DR.charge(ad, kids, isole, fl_all, frais_reels=[np.array([0.0])] * len(ad))["total"][0])
    nv = float(N.impot_z(S0, O, [a[1][0] for a in ad], kids)[0])
    return dict(libelle=lib, aujourdhui_avec_niches=avec, valeur_niches=sans - avec, aujourdhui_sans_niches=sans,
                perte_avantages=sans - avec, variation_assiette=elargi - sans, gain_bareme=nv - elargi, apres=nv,
                net=nv - avec, net_mois=(nv - avec) / 12)


NICH = [
    ("Couple biactif, 2 enfants dont 1 de moins de 6 ans, 36 000 + 24 000 € ; garde 3 500 €, emploi à domicile 3 000 €",
     [36000.0, 24000.0], 2, [("garde", 3500.0), ("emploi_domicile", 3000.0)], "A", False),
    ("Le même, sans niche", [36000.0, 24000.0], 2, [], "A", False),
    ("Couple de cadres, 2 enfants, 55 000 + 45 000 € ; emploi à domicile 8 000 €, dons 1 500 €",
     [55000.0, 45000.0], 2, [("emploi_domicile", 8000.0), ("dons", 1500.0)], "A", False),
    ("Famille biactive, 3 enfants, 50 000 + 30 000 € ; dons 1 000 €", [50000.0, 30000.0], 3, [("dons", 1000.0)], "A", False),
    ("Famille mono-active, 3 enfants, 45 000 €, sans niche", [45000.0, 0.0], 3, [], "A", False),
    ("Couple biactif, 4 enfants, 40 000 + 30 000 € ; garde 3 500 €", [40000.0, 30000.0], 4, [("garde", 3500.0)], "A", False),
    ("Parent isolé, 2 enfants, 1,3 Smic ; garde 2 000 €", [1.3 * N.SMIC_BRUT], 2, [("garde", 2000.0)], "A", True),
    ("Retraité seul, 30 000 € ; emploi à domicile 4 000 €", [30000.0], 0, [("emploi_domicile", 4000.0)], "R", False),
    ("Retraité seul, 30 000 €, sans niche", [30000.0], 0, [], "R", False),
    ("Couple de retraités, 60 000 € (36 + 24) ; emploi à domicile 6 000 €, dons 1 000 €", [36000.0, 24000.0], 0,
     [("emploi_domicile", 6000.0), ("dons", 1000.0)], "R", False),
]
D["familles_niches"] = [decompose(*a) for a in NICH]
p("\n[FAMILLES ET NICHES] perte des avantages + variation d'assiette + gain de barème = net (€/an ; €/mois)")
for r in D["familles_niches"]:
    p(f"  {r['libelle'][:95]:95s} | {r['aujourdhui_avec_niches']:7,.0f} : {r['perte_avantages']:+6,.0f} {r['variation_assiette']:+7,.0f}"
      f" {r['gain_bareme']:+7,.0f} = {r['net']:+7,.0f} ({r['net_mois']:+.0f}/mois)")

# ================================================================== 6. second conjoint et attribution de la franchise
SC = {}
for cle0, cle1, lib in (("conj_0", "conj_mi", "sans enfant"), ("conj2_0", "conj2_mi", "deux enfants"),
                        ("conj_0", "conj_1k", "premiers 1 000 €"), ("conj2_0", "conj2_1k", "premiers 1 000 €, deux enfants")):
    c0, c1 = R.CAS[R.CAS.cle == cle0].iloc[0], R.CAS[R.CAS.cle == cle1].iloc[0]
    sal2 = float(str(c1.bruts).split(";")[1])
    SC[cle1] = dict(libelle=lib, salaire_brut=sal2, auj=100 * (c1.charge - c0.charge) / sal2,
                    C2=100 * (R.impot_cas(S0, O, cle1) - R.impot_cas(S0, O, cle0)) / sal2,
                    ancien=100 * (R.impot_cas(sched(BAR["ancien"]), O, cle1) - R.impot_cas(sched(BAR["ancien"]), O, cle0)) / sal2,
                    couple_auj=float(c1.charge), couple_C2=R.impot_cas(S0, O, cle1))
D["second_conjoint"] = SC
p("\n[SECOND CONJOINT] prélèvement sur le salaire brut du second : " + " ; ".join(
    f"{v['libelle']} {v['auj']:.1f} % -> {v['C2']:.1f} % (ancienne {v['ancien']:.1f} %)" for v in SC.values()))
tm, T = S0
z1, fe, k = 40000.0, 6000.0, 2
ATT = {}
for z2 in (0.0, 5000.0, 10000.0, 20000.0, 30000.0, 39000.0, 45000.0, 60000.0):
    def imp(z2_, regle):
        if regle == "plus_eleve":
            return min(T(max(z1 - fe * k, 0)) + T(z2_), T(z1) + T(max(z2_ - fe * k, 0))) if True else 0
        if regle == "moitie":
            return T(max(z1 - fe * k / 2, 0)) + T(max(z2_ - fe * k / 2, 0))
        if regle == "second":
            return T(z1) + T(max(z2_ - fe * k, 0))
        if regle == "moitie_transferable":
            h = fe * k / 2
            return T(max(z1 - h - max(h - z2_, 0), 0)) + T(max(z2_ - h, 0))
    ATT[f"{z2:.0f}"] = {rg: dict(impot=float(imp(z2, rg)), tm_second=float(100 * (imp(z2 + 100, rg) - imp(z2, rg)) / 100))
                        for rg in ("plus_eleve", "moitie", "second", "moitie_transferable")}
D["franchise_attribution"] = dict(z1=z1, franchise=fe, enfants=k, par_z2=ATT,
                                  parent_isole_exonere_jusqua={str(kk): fe * kk for kk in (1, 2, 3)})
p("[FRANCHISE, attribution] premier parent 40 000 € ; taux marginal du second (règle « plus élevé » / « moitié » / « au"
  " second ») : " + " ; ".join(f"{z} : {v['plus_eleve']['tm_second']:.1f} / {v['moitie']['tm_second']:.1f} /"
                              f" {v['second']['tm_second']:.1f} / transférable {v['moitie_transferable']['tm_second']:.1f} ; impôt du couple"
                              f" {v['plus_eleve']['impot']:,.0f} / {v['moitie']['impot']:,.0f}" for z, v in ATT.items()))

# ================================================================== 7. taux marginaux et moyens (figures A, B)
grid = np.arange(500.0, 400001.0, 500.0)
MG = pd.read_csv(OUT / "ircsg_of_marges.csv")
ms = MG[MG.profil == "seul"].sort_values("base")
tm_auj = 100 * ((ms.ir_plus + ms.cehr_plus + ms.csg_plus + ms.crds_plus) - (ms.ir + ms.cehr + ms.csg + ms.crds)).values / (
    ms.base_eff_plus - ms.base_eff).values
tm_auj = pd.Series(tm_auj).rolling(21, center=True, min_periods=1).median().values
ta_auj = 100 * (ms.ir + ms.cehr + ms.csg + ms.crds).values / ms.base_eff.values
D["taux"] = dict(z=list(grid), auj_tm=list(np.interp(grid, ms.base.values, tm_auj)),
                 auj_ta=list(np.interp(grid, ms.base.values, ta_auj)),
                 **{f"{k}_tm": list(100 * SCH[k][0](grid)) for k in SCH},
                 **{f"{k}_ta": list(100 * SCH[k][1](grid) / grid) for k in SCH})
for zz in (10e3, 19.2e3, 25e3, 28.8e3, 38.4e3, 50e3, 67e3, 80e3, 100e3, 120e3, 163e3, 200e3, 300e3):
    i = int(np.argmin(np.abs(grid - zz)))
    p(f"  z {zz:8,.0f} : taux marginal aujourd'hui {D['taux']['auj_tm'][i]:5.1f} %, C2 {D['taux']['C2_plafond48_tm'][i]:5.1f} %,"
      f" ancienne {D['taux']['ancien_tm'][i]:4.0f} % ; taux moyen {D['taux']['auj_ta'][i]:5.1f} -> {D['taux']['C2_plafond48_ta'][i]:5.1f} %")

# ================================================================== 8. trajectoire annuelle 2027-2040 (Md€, niveau 2025)
MONTEE = {2027: 0.25, 2028: 0.5, 2029: 0.75}
D["annuel"] = {}
for F, v in VERS.items():
    ag = v["ind"]["agregats"]
    tab = {}
    for an in range(2027, 2041):
        lam = MONTEE.get(an, 1.0)
        tab[str(an)] = dict(ircsg_retraites=lam * ag["retraites"], ircsg_actifs=lam * ag["actifs"],
                            ircsg_cehr_bareme_absorbee=-lam * R.CEHR_BAR,
                            ircsg_invalidite_dependance_maintenus=-lam * sum(R.GARDES.values()),
                            ircsg_ecart_calage=lam * (v["recette"] - N.CIBLE + (0.0 if F == "F0" else float(F[1:]))))
        tab[str(an)]["ircsg_total"] = sum(tab[str(an)].values())
    D["annuel"][F] = tab
    p(f"[ANNUEL {F}] 2027 {tab['2027']['ircsg_total']:+.2f} ; 2028 {tab['2028']['ircsg_total']:+.2f} ; 2029"
      f" {tab['2029']['ircsg_total']:+.2f} ; 2030 et après {tab['2030']['ircsg_total']:+.2f} Md€")
D["annuel_recommande"] = D["annuel"]["F0"]
D["unites"] = ("Md€ au niveau 2025 ; + = recette publique en plus par rapport au droit de 2026 ; chaque foyer paie"
               " (1 − λ) × ancien impôt + λ × nouveau, λ = 0,25 / 0,5 / 0,75 / 1 de 2027 à 2030 ; la CRDS s'éteint"
               " après 2033 (droit en vigueur) : baisse uniforme des taux de 7,6 Md€ en 2034, hors bilan de la réforme")
D["status"] = {"recettes": "[E] IRCOM, comptes nationaux, Voies et moyens ; [S] répartition", "baremes": "[C]",
               "cascade": "[S] droit 2025 simulé (ircsg3_droit, validé sur OpenFisca)", "perte_seche": "[S] élasticités [E]",
               "familles_3_enfants": "[E] Insee RP 2022 + [H] même répartition à tout revenu", "frais_reels": "[E] montant, [H] répartition"}
json.dump(D, open(OUT / "ircsg3.json", "w"), ensure_ascii=False, indent=1, default=float)
(OUT / "ircsg3_calculs.txt").write_text("\n".join(L) + "\n", encoding="utf-8")
