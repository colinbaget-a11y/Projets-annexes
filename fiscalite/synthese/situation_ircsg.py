"""Situation actuelle de l'IR, de la CSG et de la CRDS (sous-partie 1 de la partie IR-CSG).

Chiffres produits (sorties/situation_ircsg.txt et .json) :
1. Recettes : dans le champ de la fusion (revenus imposés au barème, modèle calé sur l'IRCOM des revenus 2024 et sur
   les comptes de la Sécurité sociale) et au niveau national (comptes nationaux, ir_csg/sorties/series_ir_csg.csv) ;
   CSG par type de revenu ; foyers imposables à l'IR.
2. Taux moyens et marginaux d'aujourd'hui par cas-type (OpenFisca, revenus 2024, sorties/cas_types_openfisca.csv).
3. Même revenu, actifs contre retraités : charge rapportée au revenu après cotisations (cas-types et agrégats du
   modèle, ces derniers non observables).
4. Ce que vaut le quotient familial : cas-types (couples avec deux ou trois enfants, parents isolés) et coût
   agrégé du modèle ; part des familles au plafond.
5. D'où viennent les marches : seuils de CSG des retraités, entrée dans l'IR.
6. Décomposition approchée du passage de l'IR actuel (80 Md€) au barème de l'IR appliqué à chaque adulte sur
   l'assiette large (197 Md€) (repris de revue/calculs_verif/ircsg/v8_decomp_ir.py ; écart non bouclé).
7. Comparaison internationale : OCDE, Revenue Statistics (impôts sur le revenu des personnes, en % du PIB, dont la
   CSG et la CRDS pour la France) et Taxing Wages 2025 (coin fiscal au salaire moyen) ; fichiers du dépôt.

Lancer depuis fiscalite/ : python3 synthese/situation_ircsg.py
"""
import sys

import numpy as np
import pandas as pd

import outils_ircsg as U

M = U.M
v, m, x = M.v, M.m, M.x
ROOT = U.HERE.parent
L, D = [], {}


def p(s=""):
    print(s, flush=True)
    L.append(s)


# ------------------------------------------------------------------ 1. recettes
ir, csg, crds = x.ir_trav.sum(), x.csg.sum(), x.crds.sum()
csg_pens = (x.t_pens * m.F_PENS * x.pens).sum()
csg_cho = m.CSG_CHO_CCSS
csg_act = csg - csg_pens - csg_cho
crds_pens = (v.T_CRDS * m.F_PENS * x.pens * (x.t_pens > 0)).sum()
nat = pd.read_csv(ROOT / "ir_csg/sorties/series_ir_csg.csv", index_col=0).loc[2024]
D["recettes"] = dict(ir=ir, csg=csg, crds=crds, total=ir + csg + crds, csg_activite=csg_act, csg_pensions=csg_pens,
                     csg_chomage=csg_cho, crds_pensions=crds_pens, ir_ircom=x.ir.sum(), ir_pfu=x.ir.sum() - ir,
                     nat_ir=nat.ir, nat_csg=nat.csg, nat_crds=nat.crds, pib=nat.pib,
                     foyers_M=x.foyers.sum() / 1e6, foyers_imposes_M=x.foyers_imposes.sum() / 1e6,
                     assiette_brute=x.assiette.sum(), assiette_nette=x.assiette3.sum(), pensions=(m.F_PENS * x.pens).sum(),
                     chomage=(m.F_CHO * x.cho).sum())
r = D["recettes"]
p(f"[RECETTES champ] IR {ir:.1f} + CSG {csg:.1f} + CRDS {crds:.1f} = {r['total']:.1f} Md€ ; CSG : activité {csg_act:.1f},"
  f" pensions {csg_pens:.1f}, chômage {csg_cho:.2f} ; CRDS sur les pensions {crds_pens:.2f}")
p(f"[RECETTES champ] IR de l'IRCOM {x.ir.sum():.1f} Md€, dont {r['ir_pfu']:.1f} imputés aux revenus au PFU (12,8 %)")
p(f"[RECETTES nationales 2024, comptes nationaux] IR {nat.ir:.1f} ; CSG {nat.csg:.1f} ; CRDS {nat.crds:.1f} Md€ ;"
  f" ensemble {nat.ir + nat.csg + nat.crds:.1f} Md€, {100 * (nat.ir + nat.csg + nat.crds) / nat.pib:.1f} % du PIB")
p(f"[FOYERS] {r['foyers_M']:.1f} M de foyers fiscaux, dont {r['foyers_imposes_M']:.1f} M imposés à l'IR"
  f" ({100 * r['foyers_imposes_M'] / r['foyers_M']:.0f} %) ; assiette brute {r['assiette_brute']:.0f} Md€, après cotisations"
  f" {r['assiette_nette']:.0f} ; pensions {r['pensions']:.0f} ; chômage {r['chomage']:.0f}")
cur_r = sum((w * M.CURT[nom]).sum() for nom, g_, _, w, _, _ in M.TYPES if g_ == "R") / 1e9
cur_a = sum((w * M.CURT[nom]).sum() for nom, g_, _, w, _, _ in M.TYPES if g_ == "A") / 1e9
pen_n, act_n = (M.W_R * M.ZN).sum() / 1e9, (M.W_A * M.ZN).sum() / 1e9
D["charge_groupes"] = dict(retraites=cur_r, actifs=cur_a, taux_retraites=100 * cur_r / pen_n, taux_actifs=100 * cur_a / act_n)
p(f"[MODÈLE, non observable] charge actuelle des retraités {cur_r:.1f} Md€ ({100 * cur_r / pen_n:.1f} % de leurs pensions) ;"
  f" des actifs {cur_a:.1f} Md€ ({100 * cur_a / act_n:.1f} % de leur revenu après cotisations)")

# ------------------------------------------------------------------ 2. taux moyens et marginaux par cas-type
PROF = [("seul", "Salarié seul"), ("couple_0enf", "Couple sans enfant (60/40)"),
        ("couple_2enf", "Couple, deux enfants (60/40)"), ("couple_3enf", "Couple, trois enfants (60/40)"),
        ("couple_2enf_mono", "Couple, deux enfants, un revenu"), ("parent_isole_2enf", "Parent isolé, deux enfants"),
        ("retraite_seul", "Retraité seul"), ("retraite_couple", "Couple de retraités (60/40)")]
NIV = [U.SMIC, 30e3, 50e3, 80e3, 120e3]
D["taux_cas"] = {}
p("\n[TAUX par cas-type, revenu brut du ménage] taux moyen (IR + CSG + CRDS / revenu brut) ; taux marginal (sur 1 000 €)")
for prof, lib in PROF:
    lig = {}
    for b in NIV:
        ch = U.charge_auj(prof, b)
        lig[f"{b:.0f}"] = dict(moyen=100 * ch / b, marginal=U.marginal_cas(None, None, prof, b), charge=ch)
    D["taux_cas"][prof] = dict(libelle=lib, niveaux=lig)
    p(f"  {lib:<34} " + " | ".join(f"{b / 1e3:.0f} k€ : {u['moyen']:.1f} % / {u['marginal']:.0f} % ({u['charge']:,.0f} €)"
                                        for b, u in zip(NIV, lig.values())))

# ------------------------------------------------------------------ 3. même revenu : actifs contre retraités
def charge_par_base(prof, base):
    g = U.CTN[U.CTN.profil == prof].sort_values("brut")
    bz = (g.base_a + g.base_b).values
    return float(np.interp(base, bz, g.charge.values))


D["meme_revenu"] = {}
p("\n[MÊME REVENU après cotisations] charge d'aujourd'hui (€ et % du revenu) : salarié seul / retraité seul ;"
  " couple de salariés sans enfant / couple de retraités")
for base in (15e3, 20e3, 25e3, 30e3, 40e3, 60e3):
    a, rr = charge_par_base("seul", base), charge_par_base("retraite_seul", base)
    c, rc = charge_par_base("couple_0enf", base), charge_par_base("retraite_couple", base)
    D["meme_revenu"][f"{base:.0f}"] = dict(seul=a, retraite=rr, couple=c, couple_retraites=rc)
    p(f"  {base / 1e3:.0f} k€ : seul {a:,.0f} € ({100 * a / base:.1f} %) / retraité {rr:,.0f} € ({100 * rr / base:.1f} %) ;"
      f" couple {c:,.0f} € ({100 * c / base:.1f} %) / couple de retraités {rc:,.0f} € ({100 * rc / base:.1f} %)")
grille_b = np.arange(8e3, 80001, 500)
D["meme_revenu_courbe"] = dict(base=list(grille_b),
                               seul=[100 * charge_par_base("seul", b) / b for b in grille_b],
                               retraite=[100 * charge_par_base("retraite_seul", b) / b for b in grille_b])

# ------------------------------------------------------------------ 4. quotient familial
D["qf_cas"] = {}
p("\n[QUOTIENT FAMILIAL, cas-types] baisse de charge due aux enfants (couple 60/40, même revenu brut) :"
  " deux enfants / trois enfants ; parent isolé avec deux enfants contre salarié seul")
for b in (30e3, 40e3, 50e3, 60e3, 80e3, 100e3, 150e3):
    c0 = U.charge_auj("couple_0enf", b)
    d2, d3 = c0 - U.charge_auj("couple_2enf", b), c0 - U.charge_auj("couple_3enf", b)
    dpi = U.charge_auj("seul", b) - U.charge_auj("parent_isole_2enf", b)
    D["qf_cas"][f"{b:.0f}"] = dict(deux=d2, trois=d3, parent_isole=dpi)
    p(f"  {b / 1e3:.0f} k€ : deux enfants {d2:,.0f} € ; trois enfants {d3:,.0f} € ; parent isolé (deux enfants) {dpi:,.0f} €")
grille_q = np.arange(20e3, 200001, 1000)
D["qf_courbe"] = dict(brut=list(grille_q),
                      deux=[U.charge_auj("couple_0enf", b) - U.charge_auj("couple_2enf", b) for b in grille_q],
                      trois=[U.charge_auj("couple_0enf", b) - U.charge_auj("couple_3enf", b) for b in grille_q])
cap2 = 2 * M.P.PLAF * 1.0
n_c2 = (M.W_A * M.S * M.NC_A / 2)
au_plafond = (n_c2 * (M.GAIN_C >= cap2 - 1)).sum()
n_pi = (M.W_A * (1 - M.S) * M.NS_A)
pi_plafond = (n_pi * (M.GAIN_S >= M.P.PLAF_ISOL - 1)).sum()
D["qf_agregat"] = dict(cout=M.QF_COUT, couples=M.QF_COUPLES, isoles=M.QF_ISOLES, cheque=M.CHEQUE,
                       couples2_M=n_c2.sum() / 1e6, plafond_couples_M=au_plafond / 1e6,
                       parents_isoles_M=n_pi.sum() / 1e6, plafond_isoles_M=pi_plafond / 1e6)
p(f"[QUOTIENT FAMILIAL, modèle] coût {M.QF_COUT:.2f} Md€ (couples {M.QF_COUPLES:.2f}, parents isolés {M.QF_ISOLES:.2f}) ;"
  f" {M.CHEQUE:,.0f} € par enfant ; couples avec deux enfants au plafond : {au_plafond / 1e6:.2f} M sur {n_c2.sum() / 1e6:.2f} M ;"
  f" parents isolés au plafond {pi_plafond / 1e6:.2f} M sur {n_pi.sum() / 1e6:.2f} M (hypothèses H13 du registre)")

# ------------------------------------------------------------------ 5. marches
g = U.CTN[U.CTN.profil == "retraite_seul"].sort_values("brut")
g = g[(g.brut >= 5e3) & (g.brut <= 60e3) & (g.brut % 500 == 0)]
sauts = []
for b0, b1, c0, c1 in zip(g.brut.values[:-1], g.brut.values[1:], g.charge.values[:-1], g.charge.values[1:]):
    if c1 - c0 > 250 and b1 - b0 == 500:
        sauts.append(dict(de=b0, a=b1, hausse=c1 - c0))
D["marches_retraite"] = sauts
p("\n[MARCHES, retraité seul] hausse de charge pour 500 € de pension en plus aux seuils de CSG : "
  + " ; ".join(f"{s['de'] / 1e3:.1f} → {s['a'] / 1e3:.1f} k€ : +{s['hausse']:,.0f} €" for s in sauts))
mg_seul = [(b, U.marginal_cas(None, None, "seul", b)) for b in np.arange(5e3, 150001, 500)]
D["marginal_seul"] = mg_seul
paliers = []
for b, t in mg_seul:
    if not paliers or abs(t - paliers[-1][1]) > 2.0:
        paliers.append((b, t))
p("[MARCHES, salarié seul] taux marginal (IR + CSG + CRDS, sur 1 000 € brut) : "
  + " ; ".join(f"dès {b / 1e3:.1f} k€ : {t:.1f} %" for b, t in paliers[:14]))

# ------------------------------------------------------------------ 6. décomposition de l'IR (approchée)
IRS, IRT = [0, 11497, 29315, 83823, 180294], [0, .11, .30, .41, .45]


def bar(q):
    return sum(t * np.clip(np.minimum(q, h) - s, 0, None) for s, h, t in zip(IRS, IRS[1:] + [np.inf], IRT))


def ir_regles(r_, couple, n, isole=False, decote=True, qf=True):
    p0 = 2.0 if couple else 1.0
    n = n if qf else 0
    if couple:
        pp = 2 + 0.5 * min(n, 2) + max(n - 2, 0)
        cap = 1791 * 2 * (pp - p0)
    elif isole and n >= 1:
        pp, cap = 2.0, 4224.0
    else:
        pp, cap = 1.0, 0.0
    i0 = p0 * bar(r_ / p0)
    i1 = np.maximum(pp * bar(r_ / pp), i0 - cap)
    if decote:
        i1 = i1 - np.clip((1470 if couple else 889) - 0.4525 * i1, 0, None)
    return np.clip(i1, 0, None)


def rfr(g_, parts):
    if g_ == "A":
        return M.RFR_A
    r_ = M.ZN * 0.95 - np.minimum(0.10 * M.ZN * 0.95, 4399)
    n = len(parts)
    pers = r_ / n
    return np.clip(r_ - n * np.where(pers <= 17510, 2796, np.where(pers <= 28170, 1398, 0)), 0, None)


def total(f):
    return sum((w * f(g_, parts, k)).sum() for nom, g_, fam, w, parts, k in M.TYPES) / 1e9


etapes = [("règles actuelles sans niche, sur le revenu imposable, imposition commune",
           lambda g_, parts, k: ir_regles(rfr(g_, parts), len(parts) == 2, k, isole=(k > 0 and len(parts) == 1))),
          ("assiette large (revenu après cotisations, sans abattement)",
           lambda g_, parts, k: ir_regles(M.ZN, len(parts) == 2, k, isole=(k > 0 and len(parts) == 1))),
          ("sans quotient familial des enfants", lambda g_, parts, k: ir_regles(M.ZN, len(parts) == 2, k, qf=False)),
          ("sans décote", lambda g_, parts, k: ir_regles(M.ZN, len(parts) == 2, k, qf=False, decote=False)),
          ("sans quotient conjugal (barème appliqué à chaque adulte)",
           lambda g_, parts, k: sum(bar(sh * M.ZN) for sh in parts))]
D["decomposition_ir"] = []
prev = None
p(f"\n[DÉCOMPOSITION approchée] IR des revenus au barème aujourd'hui : {ir:.1f} Md€ (après niches)")
for lab, f in etapes:
    t = total(f)
    D["decomposition_ir"].append(dict(etape=lab, Md=t, ecart=None if prev is None else t - prev))
    p(f"  {lab:<72} {t:6.1f} Md€" + (f" ({t - prev:+.1f})" if prev is not None else ""))
    prev = t

# ------------------------------------------------------------------ 7. comparaison internationale
rev = pd.read_csv(ROOT / "donnees/recettes_ocde_pct_pib.csv")
pays = ["Danemark", "Belgique", "Suède", "Italie", "Royaume-Uni", "États-Unis", "Allemagne", "France", "Pays-Bas",
        "Espagne", "Moyenne OCDE", "Japon"]
t11 = rev[(rev.categorie == "T_1100") & (rev.pays.isin(pays))]
an = int(min(t11[t11.pays == "France"].annee.max(), t11[t11.pays == "Moyenne OCDE"].annee.max()))
t11 = t11[t11.annee == an].set_index("pays").pct_pib
D["ocde_1100"] = dict(annee=an, valeurs={k: float(t11[k]) for k in pays if k in t11})
natp = pd.read_csv(ROOT / "ir_csg/sorties/series_ir_csg.csv", index_col=0).loc[an]
D["ocde_1100"]["france_ir_pct"] = float(natp.ir_pct_pib)
D["ocde_1100"]["france_csg_crds_pct"] = float(natp.csg_pct_pib + natp.crds_pct_pib)
p(f"\n[OCDE, Revenue Statistics {an}] impôts sur le revenu des personnes (1100), % du PIB : "
  + " ; ".join(f"{k} {t11[k]:.1f}" for k in pays if k in t11)
  + f" | France : IR seul {natp.ir_pct_pib:.1f} %, CSG + CRDS {natp.csg_pct_pib + natp.crds_pct_pib:.1f} % (comptes nationaux)")
cf = pd.read_csv(ROOT / "donnees/coin_fiscal.csv").set_index("pays")
D["ocde_coin"] = {k: dict(impot=float(cf.loc[k, "impot_revenu_pct_cout"]), total=float(cf.loc[k, "coin_total_pct_cout"]))
                  for k in ("France", "Allemagne", "Royaume-Uni", "Moyenne OCDE", "Moyenne UE de l'OCDE") if k in cf.index}
p("[OCDE, Taxing Wages 2025] personne seule au salaire moyen, % du coût du travail : impôt sur le revenu (CSG et CRDS"
  " comprises pour la France) / coin total : " + " ; ".join(f"{k} {u['impot']:.1f} / {u['total']:.1f}" for k, u in D["ocde_coin"].items()))

# ------------------------------------------------------------------ premier salaire aujourd'hui
D["ptr_auj"] = U.ptrs(None, None)
p("\n[PREMIER SALAIRE aujourd'hui] taux de prélèvement IR + CSG + CRDS : " + " ; ".join(f"{k} {u:.1f} %" for k, u in D["ptr_auj"].items()))
coin = {}
for f in (0.5, 1.0, 1.25, 1.5, 2.0, 2.5, 3.0):
    gg = f * M.ps.SMIC
    er, ee, pa = M.ps.coin(np.array([gg]), 1.0, "nc")
    er_tout = M.ps.coin(np.array([gg]), 1.0, "tout")[0]
    tau = U.marginal_cas(None, None, "seul", round(f * U.SMIC / 500) * 500) / 100
    cout = 1 + float(er_tout[0])            # coût marginal du travail par euro brut
    coin[f] = dict(cotis_nc=float(er[0] + ee[0]) / cout, prime=float(pa[0]) / cout, ircsg=tau / cout,
                   total=float(er[0] + ee[0] + pa[0] + tau) / cout)
D["coin_marginal"] = coin
p("[COIN MARGINAL, personne seule, droit 2025] en % d'un euro de coût du travail en plus : cotisations non"
  " contributives + retrait de la prime d'activité + IR-CSG = total : "
  + " ; ".join(f"{f:g} Smic : {100 * u['cotis_nc']:.0f} + {100 * u['prime']:.0f} + {100 * u['ircsg']:.0f} = {100 * u['total']:.0f}"
               for f, u in coin.items()))

U.ecrire("situation_ircsg", L, D)
