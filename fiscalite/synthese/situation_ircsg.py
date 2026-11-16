"""Situation actuelle de l'IR, de la CSG et de la CRDS (sous-partie 1 de la partie IR-CSG).

Chiffres produits (sorties/situation_ircsg.txt et .json) :
1. Recettes, base 2025 (décision 5 du 17/11/2026) : dans le champ de la fusion (revenus imposés au barème ; répartition
   de l'IRCOM des revenus 2024, agrégats recalés en 2025, modele_purs.RECETTES) et au niveau national (Insee, comptes
   nationaux 2025 publiés en 2026 : « Impôts, données annuelles de 1995 à 2025 », econ-fin-pub-impots-categ.xlsx,
   28/08/2026 ; PIB : tableau 1.101, 04/06/2026) ; CSG par type de revenu ; foyers imposables à l'IR (IRCOM 2024).
2. Taux moyens et marginaux d'aujourd'hui par cas-type (OpenFisca, revenus 2025, sorties/cas_types_openfisca.csv et
   courbes_marginales_openfisca.csv : taux marginal par 1 000 € de revenu après cotisations, grille de 100 €).
3. Même revenu, actifs contre retraités : charge rapportée au revenu après cotisations (cas-types et agrégats du
   modèle, ces derniers non observables).
4. Ce que vaut le quotient familial : cas-types (couples avec deux ou trois enfants, parents isolés) et coût
   agrégé du modèle ; part des familles au plafond.
5. D'où viennent les marches : seuils de CSG des retraités, entrée dans l'IR.
6. Décomposition approchée du passage de l'IR actuel (80 Md€) au barème de l'IR appliqué à chaque adulte sur
   l'assiette large (197 Md€) (repris de revue/calculs_verif/ircsg/v8_decomp_ir.py ; écart non bouclé).
7. Comparaison internationale : OCDE, Revenue Statistics (impôts sur le revenu des personnes, en % du PIB, dont la
   CSG et la CRDS pour la France) ; fichiers du dépôt.

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
# Comptes nationaux de l'Insee (base 2020), Md€ : IR avant crédits d'impôt, CSG et CRDS (hors jeux), PIB en valeur
# (fichiers lus dans le scratchpad ircsg2025/ ; 2024 semi-définitif, 2025 provisoire)
NAT = {2024: dict(ir=96.018, csg=153.148, crds=9.070, pib=2935.236),
       2025: dict(ir=103.626, csg=156.583, crds=9.270, pib=2991.056)}
R5, R4 = M.RECETTES["2025"], M.RECETTES["2024"]
nat = NAT[2025]
D["recettes"] = dict(**R5, base_2024=R4, nat=NAT[2025], nat_2024=NAT[2024],
                     nat_ir=nat["ir"], nat_csg=nat["csg"], nat_crds=nat["crds"], pib=nat["pib"],
                     facteurs=dict(ir=M.F_IR, csg_activite=M.G_ACT, csg_remplacement=M.G_REMP, crds=M.F_CRDS),
                     foyers_M=x.foyers.sum() / 1e6, foyers_imposes_M=x.foyers_imposes.sum() / 1e6,
                     assiette_nette=float((M.W_A * M.ZNA).sum() + (M.W_R * M.ZNR).sum()) / 1e9,
                     assiette_nette_2024=x.assiette3.sum(), pensions=float((M.W_R * M.ZNR).sum()) / 1e9)
r = D["recettes"]
p(f"[RECETTES champ, base 2025] IR {R5['ir']:.1f} + CSG {R5['csg']:.1f} + CRDS {R5['crds']:.1f} = {R5['total']:.1f} Md€ ;"
  f" CSG : activité {R5['csg_activite']:.1f}, pensions {R5['csg_pensions']:.1f}, chômage {R5['csg_chomage']:.2f}")
p(f"[RECETTES champ, base 2024] IR {R4['ir']:.1f} + CSG {R4['csg']:.1f} + CRDS {R4['crds']:.1f} = {R4['total']:.1f} Md€ ;"
  f" CSG : activité {R4['csg_activite']:.1f}, pensions {R4['csg_pensions']:.1f}, chômage {R4['csg_chomage']:.2f}")
p(f"[RECETTES champ] IR « IRCOM » porté en 2025 {R5['ir_ircom']:.1f} Md€ (2024 : {R4['ir_ircom']:.1f}), dont"
  f" {R5['ir_pfu']:.1f} imputés aux revenus au PFU (12,8 % en 2024, même croissance)")
for an, u in NAT.items():
    p(f"[RECETTES nationales {an}, comptes nationaux] IR {u['ir']:.1f} ; CSG {u['csg']:.1f} ; CRDS {u['crds']:.1f} Md€ ;"
      f" ensemble {u['ir'] + u['csg'] + u['crds']:.1f} Md€, {100 * (u['ir'] + u['csg'] + u['crds']) / u['pib']:.1f} % du PIB")
p(f"[FACTEURS 2025/2024] IR {M.F_IR:.4f} ; CSG d'activité {M.G_ACT} ; CSG de remplacement {M.G_REMP} ; CRDS {M.F_CRDS:.4f}")
p(f"[FOYERS, IRCOM 2024] {r['foyers_M']:.1f} M de foyers fiscaux, dont {r['foyers_imposes_M']:.1f} M imposés à l'IR"
  f" ({100 * r['foyers_imposes_M'] / r['foyers_M']:.0f} %) ; assiette après cotisations {r['assiette_nette']:.0f} Md€"
  f" en 2025 ({r['assiette_nette_2024']:.0f} en 2024) ; pensions {r['pensions']:.0f}")
cur_r = sum((w * M.CURT[nom]).sum() for nom, g_, _, w, _, _ in M.TYPES if g_ == "R") / 1e9
cur_a = sum((w * M.CURT[nom]).sum() for nom, g_, _, w, _, _ in M.TYPES if g_ == "A") / 1e9
pen_n, act_n = (M.W_R * M.ZNR).sum() / 1e9, (M.W_A * M.ZNA).sum() / 1e9
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


def charge_seul_base(prof, base):
    """Charge d'aujourd'hui d'un salarié seul ou d'un retraité seul au revenu après cotisations base (grille de 100 €,
    OpenFisca, sans interpolation)."""
    g = U.MGN[U.MGN.profil == prof]
    i = np.argmin(np.abs(g.base.values - base))
    return float(g.charge.values[i]), float(g.base_eff.values[i])


D["meme_revenu"] = {}
p("\n[MÊME REVENU après cotisations] charge d'aujourd'hui (€ et % du revenu) : salarié seul / retraité seul ;"
  " couple de salariés sans enfant / couple de retraités")
for base in (15e3, 20e3, 25e3, 30e3, 40e3, 60e3):
    a, rr = charge_seul_base("seul", base)[0], charge_seul_base("retraite_seul", base)[0]
    c, rc = charge_par_base("couple_0enf", base), charge_par_base("retraite_couple", base)
    D["meme_revenu"][f"{base:.0f}"] = dict(seul=a, retraite=rr, couple=c, couple_retraites=rc)
    p(f"  {base / 1e3:.0f} k€ : seul {a:,.0f} € ({100 * a / base:.1f} %) / retraité {rr:,.0f} € ({100 * rr / base:.1f} %) ;"
      f" couple {c:,.0f} € ({100 * c / base:.1f} %) / couple de retraités {rc:,.0f} € ({100 * rc / base:.1f} %)")
grille_b = np.arange(8e3, 80001, 100)
D["meme_revenu_courbe"] = dict(base=list(grille_b),
                               seul=[100 * (lambda c, b_: c / b_)(*charge_seul_base("seul", b)) for b in grille_b],
                               retraite=[100 * (lambda c, b_: c / b_)(*charge_seul_base("retraite_seul", b)) for b in grille_b])

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

# ------------------------------------------------------------------ 5. marches (grille de 100 € de revenu après cotisations)
def sauts(prof, seuil=60.0):
    """Hausses de charge de plus de « seuil » euros pour 100 € de revenu en plus : vrais sauts du droit."""
    g = U.MGN[U.MGN.profil == prof].sort_values("base")
    b, c = g.base_eff.values, g.charge.values
    out = []
    for k in range(len(b) - 1):
        d = c[k + 1] - c[k] - 0.25 * (b[k + 1] - b[k])          # au-delà d'un taux marginal ordinaire de 25 %
        if d > seuil:
            out.append(dict(de=float(g.base.values[k]), a=float(g.base.values[k + 1]), hausse=float(c[k + 1] - c[k]),
                            taux_avant=int(g.taux_csg.values[k]) if prof == "retraite_seul" else None,
                            taux_apres=int(g.taux_csg.values[k + 1]) if prof == "retraite_seul" else None,
                            rfr_avant=float(g.rfr.values[k]), rfr_apres=float(g.rfr.values[k + 1])))
    return out


D["marches_retraite"] = sauts("retraite_seul")
p("\n[MARCHES, retraité seul, droit 2025] hausses de charge pour 100 € de pension en plus (taux de CSG 0 à 3 = exonéré,"
  " 3,8, 6,6, 8,3 %) : " + " ; ".join(f"{u['de'] / 1e3:.1f} → {u['a'] / 1e3:.1f} k€ : +{u['hausse']:,.0f} € (CSG {u['taux_avant']}"
                                      f" → {u['taux_apres']}, RFR {u['rfr_avant']:,.0f} → {u['rfr_apres']:,.0f})"
                                      for u in D["marches_retraite"]))
D["marches_salarie"] = sauts("seul", seuil=30.0)
p("[MARCHES, salarié seul, droit 2025] " + " ; ".join(f"{u['de'] / 1e3:.1f} → {u['a'] / 1e3:.1f} k€ : +{u['hausse']:,.0f} €"
                                                       for u in D["marches_salarie"]))
for prof in ("seul", "retraite_seul"):
    xs, ys = U.courbe_marginale(None, None, prof)
    D[f"marginal_{prof}"] = [(float(a), float(b)) for a, b in zip(xs, ys) if a % 500 == 0]
    paliers = []
    for a, b in zip(xs, ys):
        if not paliers or abs(b - paliers[-1][1]) > 2.0:
            paliers.append((a, b))
    p(f"[TAUX MARGINAL {prof}, par 1 000 € de revenu après cotisations] " +
      " ; ".join(f"dès {a / 1e3:.1f} k€ : {b:.1f} %" for a, b in paliers[:30]))

# ------------------------------------------------------------------ 6. décomposition de l'IR (approchée)
IRS, IRT = list(M.ex.IR_SEUILS), [0, .11, .30, .41, .45]          # barème des revenus 2025 (base 2025)
PLAF, PLAF_I, DECS, DECC = M.P.PLAF, M.P.PLAF_ISOL, M.P.DEC_S, M.P.DEC_C
ABP = (2822, 17670, 1411, 28430, 4439) if M.BASE == "2025" else (2796, 17510, 1398, 28170, 4399)


def bar(q):
    return sum(t * np.clip(np.minimum(q, h) - s, 0, None) for s, h, t in zip(IRS, IRS[1:] + [np.inf], IRT))


def ir_regles(r_, couple, n, isole=False, decote=True, qf=True):
    p0 = 2.0 if couple else 1.0
    n = n if qf else 0
    if couple:
        pp = 2 + 0.5 * min(n, 2) + max(n - 2, 0)
        cap = PLAF * 2 * (pp - p0)
    elif isole and n >= 1:
        pp, cap = 2.0, PLAF_I
    else:
        pp, cap = 1.0, 0.0
    i0 = p0 * bar(r_ / p0)
    i1 = np.maximum(pp * bar(r_ / pp), i0 - cap)
    if decote:
        i1 = i1 - np.clip((DECC if couple else DECS) - 0.4525 * i1, 0, None)
    return np.clip(i1, 0, None)


def rfr(g_, parts):
    if g_ == "A":
        return M.RFR_A
    r_ = M.ZNR * 0.95 - np.minimum(0.10 * M.ZNR * 0.95, ABP[4])
    n = len(parts)
    pers = r_ / n
    return np.clip(r_ - n * np.where(pers <= ABP[1], ABP[0], np.where(pers <= ABP[3], ABP[2], 0)), 0, None)


def total(f):
    return sum((w * f(g_, parts, k)).sum() for nom, g_, fam, w, parts, k in M.TYPES) / 1e9


etapes = [("règles actuelles sans niche, sur le revenu imposable, imposition commune",
           lambda g_, parts, k: ir_regles(rfr(g_, parts), len(parts) == 2, k, isole=(k > 0 and len(parts) == 1))),
          ("assiette large (revenu après cotisations, sans abattement)",
           lambda g_, parts, k: ir_regles(M.ZNG[g_], len(parts) == 2, k, isole=(k > 0 and len(parts) == 1))),
          ("sans quotient familial des enfants", lambda g_, parts, k: ir_regles(M.ZNG[g_], len(parts) == 2, k, qf=False)),
          ("sans décote", lambda g_, parts, k: ir_regles(M.ZNG[g_], len(parts) == 2, k, qf=False, decote=False)),
          ("sans quotient conjugal (barème appliqué à chaque adulte)",
           lambda g_, parts, k: sum(bar(sh * M.ZNG[g_]) for sh in parts))]
D["decomposition_ir"] = []
prev = None
p(f"\n[DÉCOMPOSITION approchée] IR des revenus au barème aujourd'hui : {R5['ir']:.1f} Md€ (après niches ; base 2025)")
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

# ------------------------------------------------------------------ premier salaire aujourd'hui
D["ptr_auj"] = U.ptrs(None, None)
p("\n[PREMIER SALAIRE aujourd'hui] taux de prélèvement IR + CSG + CRDS : " + " ; ".join(f"{k} {u:.1f} %" for k, u in D["ptr_auj"].items()))
U.ecrire("situation_ircsg", L, D)
