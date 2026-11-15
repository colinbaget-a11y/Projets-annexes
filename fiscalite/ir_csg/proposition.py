"""Proposition de la note (exercice 3 corrigé), quatre façons de traiter la famille, nombre de perdants.

Lancer depuis fiscalite/ : python3 ir_csg/proposition.py  ->  sorties/proposition.txt (étiquettes P0 à P9)

Cadre : celui des exercices (exercices.py) : assiette commune = revenu après cotisations, sans niche ; impôt
individuel ; barème à taux marginal en ligne droite entre 0, 20 000 €, z1 et z2 (50 % au-delà de z2) ; même
recette (220 Md€). Deux corrections de l'exercice 3, décidées avec l'auteur :
- déciles 2 à 4 : une franchise de F € par adulte sur les seuls revenus d'activité (salaires, indépendants,
  gérants, loyers), pas sur les pensions ni le chômage ;
- familles : quatre traitements comparés, à recette égale, le barème étant à chaque fois réoptimisé :
  « rien » (la famille passe par les prestations), « franchise » (6 000 € par enfant déduits du revenu du parent
  qui gagne le plus), « chèque » (le coût actuel du quotient familial des enfants, reversé en un montant égal par
  enfant, versé même sans impôt), « quotient » (quotient conjugal et familial appliqués à l'impôt fusionné, avec
  le plafond actuel de 1 791 € par demi-part et 4 224 € pour le premier enfant d'un parent isolé).

Représentation des foyers : chaque foyer représentatif (bareme_v3) est éclaté en personnes seules sans enfant ou
avec un enfant (part N_ENF_S) et en couples sans enfant ou avec deux enfants (part N_ENF_C / 2), ce qui garde le
nombre total d'enfants ; couples selon les partages de l'Insee. Charge actuelle : couples sans enfant et avec
deux enfants d'après les cas-types OpenFisca ; personnes seules avec enfant : charge des personnes seules moins
le gain de quotient familial calculé ci-dessous.
"""
import itertools
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE), str(HERE.parent)]
import exercices as ex  # noqa: E402
import systeme_efficace as se  # noqa: E402

v = ex.v
W, Z, ZN, S, R, Q, DEC = v.W, v.Z, v.ZN, v.S_COUPLE, ex.R, v.Q, v.DEC
NS, NC = v.N_ENF_S, v.N_ENF_C
LABN = ZN * (1 - se.NL)                      # revenus d'activité et loyers, après cotisations
TOP, FR_ENF = ex.TOP, ex.FRANCHISE

# ------------------------------------------------------------------ IR actuel et quotient familial (revenus 2024)
# Paramètres OpenFisca-France 176.1 (impot_revenu.calcul_impot_revenu.plaf_qf, 2024) : plafond général 1 791 € par
# demi-part, 4 224 € pour les deux demi-parts du premier enfant d'un parent isolé ; décote 889 € (seul), 1 470 €
# (couple), taux 45,25 %.
PLAF, PLAF_ISOL, DEC_S, DEC_C, DEC_T = 1791.0, 4224.0, 889.0, 1470.0, 0.4525
_S, _T = np.array(ex.IR_SEUILS), np.array(ex.IR_TAUX)
_H = np.r_[_S[1:], np.inf]


def _bareme_ir(q):
    return sum(r * np.clip(np.minimum(q, h) - lo, 0, None) for lo, h, r in zip(_S, _H, _T))


def ir_actuel(r, couple, n):
    """IR des revenus 2024 sur le revenu imposable r : quotient, plafonnement, décote (sans niche)."""
    p0 = 2.0 if couple else 1.0
    if couple:
        p = p0 + 0.5 * min(n, 2) + max(n - 2, 0)
        cap = 2 * PLAF * (p - p0)
    else:
        p = p0 + (1.0 if n >= 1 else 0.0) + 0.5 * min(max(n - 1, 0), 1) + max(n - 2, 0)
        cap = (PLAF_ISOL if n >= 1 else 0.0) + 2 * PLAF * (p - p0 - (1.0 if n >= 1 else 0.0))
    i0 = p0 * _bareme_ir(r / p0)
    i = np.maximum(p * _bareme_ir(r / p), i0 - cap)
    return np.clip(i - np.clip((DEC_C if couple else DEC_S) - DEC_T * i, 0, None), 0, None)


RFR = v._RFR_F
GAIN_C = ir_actuel(RFR, True, 0) - ir_actuel(RFR, True, 2)           # gain de QF, couple avec deux enfants
GAIN_S = ir_actuel(RFR, False, 0) - ir_actuel(RFR, False, 1)         # gain de QF, parent isolé, un enfant
QF_COUPLES = (W * S * NC / 2 * GAIN_C).sum() / 1e9
QF_ISOLES = (W * (1 - S) * NS * GAIN_S).sum() / 1e9
QF_COUT = QF_COUPLES + QF_ISOLES
ENFANTS = (W * ((1 - S) * NS + S * NC)).sum()
CHEQUE = QF_COUT * 1e9 / ENFANTS                                      # montant égal par enfant

# ------------------------------------------------------------------ types de foyers
CUR_C0, CUR_C2 = v.CUR * v._tc0 / v._mix, v.CUR * v._tc2 / v._mix
CUR_S1 = np.maximum(v.CUR_S - GAIN_S, 0.0)
CUR_S0 = (v.CUR_S - NS * CUR_S1) / (1 - NS)                          # garde la charge moyenne des personnes seules
TYPES = [("seul", W * (1 - S) * (1 - NS), [1.0], 0, CUR_S0),
         ("parent_isole", W * (1 - S) * NS, [1.0], 1, CUR_S1)]
for s_, p_ in v.PARTAGE:
    TYPES.append((f"couple0_{s_}", W * S * (1 - NC / 2) * p_, [s_, 1 - s_], 0, CUR_C0))
    TYPES.append((f"couple2_{s_}", W * S * NC / 2 * p_, [s_, 1 - s_], 2, CUR_C2))


def impot_type(tm, T, F, fam, parts, kids, zn=ZN, lab=LABN):
    """Impôt d'un type de foyer et taux marginal de chaque adulte sur ses revenus d'activité."""
    zs = [sh * zn for sh in parts]
    ls = [sh * lab for sh in parts]
    tax = [np.clip(z - np.minimum(F, l), 0, None) for z, l in zip(zs, ls)]    # franchise sur l'activité
    actif = [l > F for l in ls]
    if fam == "quotient":
        y = sum(tax)
        if len(parts) == 2:
            p0, p = 2.0, 2.0 + 0.5 * kids
            cap = 2 * PLAF * (p - p0)
        else:
            p0, p = 1.0, 1.0 + (1.0 if kids else 0.0)
            cap = PLAF_ISOL if kids else 0.0
        i0, i1 = p0 * T(y / p0), p * T(y / p)
        borne = i0 - cap > i1
        imp = np.maximum(i1, i0 - cap)
        mg = np.where(borne, tm(y / p0), tm(y / p))
        return imp, [np.where(a, mg, 0.0) for a in actif]
    if fam == "franchise" and kids:
        haut = np.argmax(np.vstack(zs), axis=0) if len(zs) == 2 else np.zeros(len(zn), int)
        tax = [np.where(haut == k, np.clip(t - FR_ENF * kids, 0, None), t) for k, t in enumerate(tax)]
    imp = sum(T(t) for t in tax)
    if fam == "cheque":
        imp = imp - CHEQUE * kids
    mg = [np.where(a & (t > 0), tm(t), 0.0) for a, t in zip(actif, tax)]
    return imp, mg


def systeme(tm, T, F, fam):
    """Impôt moyen du foyer représentatif, impôts par type et perte sèche (jeu central et variantes)."""
    n = np.zeros_like(Z)
    par_type = {}
    cout = {j: 0.0 for j in ("bas", "central", "haut")}
    e = {j: v.elast(j) for j in cout}
    for nom, w, parts, kids, cur in TYPES:
        imp, mgs = impot_type(tm, T, F, fam, parts, kids)
        n += w * imp
        par_type[nom] = (w, imp, cur)
        for sh, mg in zip(parts, mgs):
            tau = np.clip(mg * R, 0, 0.95)
            for j in cout:
                cout[j] += (w * 0.5 * e[j] * sh * Z * tau ** 2 / (1 - tau)).sum() / 1e9
    return n / W, par_type, cout


def recette(T, tm, F, fam):
    return (W * systeme(tm, T, F, fam)[0]).sum() / 1e9


def cale(t0, tb, z1, z2, F, fam):
    lo, hi = 0.0, TOP
    for _ in range(36):
        t1 = (lo + hi) / 2
        tm, T = ex.bareme_lineaire([0, 20e3, z1, z2], [t0, tb, t1, TOP])
        lo, hi = (t1, hi) if recette(T, tm, F, fam) < v.CIBLE else (lo, t1)
    t1 = (lo + hi) / 2
    return t1, ex.bareme_lineaire([0, 20e3, z1, z2], [t0, tb, t1, TOP])


GRILLE_PROP = dict(t0=[0.05, 0.08, 0.11, 0.14, 0.17, 0.20, 0.23], tb=[0.10, 0.13, 0.16, 0.19, 0.22, 0.25, 0.28],
                   z1=[45e3, 60e3, 80e3, 120e3], z2=[250e3, 400e3, 600e3])
# étapes 2 et 3 : grille des exercices réunie à celle de la proposition (l'étape 3 reste le minimum de perte sèche)
GRILLE_EX = {k: sorted(set(u) | set(GRILLE_PROP[k])) for k, u in dict(
    t0=[0.03, 0.05, 0.07, 0.09, 0.11, 0.13, 0.15], tb=[0.08, 0.10, 0.13, 0.16, 0.19, 0.22],
    z1=[30e3, 45e3, 60e3, 80e3], z2=[100e3, 150e3, 250e3, 400e3, 600e3]).items()}


def transferts(pt):
    """Écart quadratique moyen (points de revenu brut) entre la nouvelle charge et la charge actuelle."""
    num = sum((w * ((imp - cur) / Z) ** 2).sum() for w, imp, cur in pt.values())
    return 100 * np.sqrt(num / W.sum())


def grille(F, fam, G):
    rows = []
    for t0, tb, z1, z2 in itertools.product(*G.values()):
        if tb < t0 or z1 >= z2:
            continue
        t1, (tm, T) = cale(t0, tb, z1, z2, F, fam)
        n, pt, c = systeme(tm, T, F, fam)
        if not tb <= t1 < TOP - 1e-3 or abs((W * n).sum() / 1e9 - v.CIBLE) > 0.05:
            continue
        rows.append(dict(t0=t0, tb=tb, z1=z1, t1=t1, z2=z2, cout=c["central"], transferts=transferts(pt)))
    return pd.DataFrame(rows)


def bareme(r):
    return ex.bareme_lineaire([0, 20e3, r["z1"], r["z2"]], [r["t0"], r["tb"], r["t1"], TOP])


def cale_ex1():
    lo, hi = -0.2, 0.3
    for _ in range(50):
        tau = (lo + hi) / 2
        tm, T = ex.bareme_empile(tau)
        lo, hi = (tau, hi) if recette(T, tm, 0.0, "franchise") < v.CIBLE else (lo, tau)
    return (lo + hi) / 2


# ------------------------------------------------------------------ indicateurs
def perdants(par_type, seuils=(500, 1000)):
    """Foyers (millions) dont la charge augmente de plus de chaque seuil, et part des foyers."""
    out = {}
    for s_ in seuils:
        k = sum((w * (imp - cur > s_)).sum() for w, imp, cur in par_type.values())
        out[s_] = (k / 1e6, 100 * k / W.sum())
    g = sum((w * (imp - cur < -s_)).sum() for w, imp, cur in par_type.values() for s_ in [500])
    out["gagnants500"] = (g / 1e6, 100 * g / W.sum())
    return out


def cas_types(tm, T, F, fam, plus=False):
    """Foyers types OpenFisca (salariés ; retraité : pension, pas d'activité)."""
    ct = ex.CT
    a = (ct.base_a_plus if plus else ct.base_a).values
    b = (ct.base_b_plus if plus else ct.base_b).values
    out = np.zeros(len(ct))
    for prof, kids in ex.ENF.items():
        m = (ct.profil == prof).values
        zn = a[m] + b[m]
        sh = np.where(zn > 0, a[m] / np.where(zn > 0, zn, 1), 1.0)
        lab = zn * (prof != "retraite_seul")
        if prof in ("seul", "retraite_seul"):
            imp, _ = impot_type(tm, T, F, fam, [1.0], kids, zn=zn, lab=lab)
        else:
            # deux adultes : part du premier = sh (vectorisée)
            zs, ls = [sh * zn, (1 - sh) * zn], [sh * lab, (1 - sh) * lab]
            imp = _couple_vect(tm, T, F, fam, zs, ls, kids)
        out[m] = imp
    return out


def _couple_vect(tm, T, F, fam, zs, ls, kids):
    tax = [np.clip(z - np.minimum(F, l), 0, None) for z, l in zip(zs, ls)]
    if fam == "quotient":
        y = sum(tax)
        p = 2.0 + 0.5 * kids
        return np.maximum(p * T(y / p), 2 * T(y / 2) - 2 * PLAF * (p - 2.0))
    if fam == "franchise" and kids:
        haut = np.argmax(np.vstack(zs), axis=0)
        tax = [np.where(haut == k, np.clip(t - FR_ENF * kids, 0, None), t) for k, t in enumerate(tax)]
    imp = sum(T(t) for t in tax)
    return imp - (CHEQUE * kids if fam == "cheque" else 0.0)


def ecart(n_ct, prof, brut):
    ct = ex.CT
    i = ct[(ct.profil == prof) & (ct.brut == brut)].index[0]
    return float(n_ct[i] - ct.actuel[i])


F_RET = 8000.0                               # franchise d'activité retenue (voir P2)
FAM_RET = "franchise"                        # traitement de la famille retenu (voir P3, P4)


def aide_familiale(tm, T, F, fam):
    """Aide aux familles contenue dans l'impôt (Md€) : impôt des foyers avec enfants s'ils n'en avaient pas,
    moins leur impôt réel ; pour comparaison, le quotient familial des enfants coûte QF_COUT aujourd'hui."""
    tot = 0.0
    for nom, w, parts, kids, cur in TYPES:
        if kids:
            tot += (w * (impot_type(tm, T, F, fam, parts, 0)[0] - impot_type(tm, T, F, fam, parts, kids)[0])).sum()
    return tot / 1e9


def _txt(r):
    return (f"{100*r['t0']:.0f} % au premier euro, {100*r['tb']:.0f} % à 20 k€, {100*r['t1']:.1f} % à {r['z1']/1e3:.0f} k€,"
            f" 50 % à {r['z2']/1e3:.0f} k€ ; perte sèche {r['cout']:.1f} ; transferts {r['transferts']:.2f} pts")


def bilan(nom, tm, T, F, fam, p):
    n, pt, c = systeme(tm, T, F, fam)
    d = v.deciles(n)
    per = perdants(pt)
    ty = v.par_type(n)
    n_ct = cas_types(tm, T, F, fam)
    p("P5", f"{nom} : recette {(W*n).sum()/1e9:.1f} Md€ ; perte sèche {c['central']:.1f} ({c['bas']:.1f} à {c['haut']:.1f}) ;"
            f" redistribution {ex.redistribution(n):.2f} ; perdants > 500 € {per[500][0]:.1f} M ({per[500][1]:.0f} %),"
            f" > 1 000 € {per[1000][0]:.1f} M ({per[1000][1]:.0f} %) ; gagnants > 500 € {per['gagnants500'][0]:.1f} M"
            f" ({per['gagnants500'][1]:.0f} %)")
    p("P6", f"{nom} : déciles € " + " ".join(f"{u:+.0f}" for u in d.delta_eur) + " | pts "
          + " ".join(f"{u:+.1f}" for u in d.delta_pts))
    p("P6", f"{nom} : types Md€ " + " ; ".join(f"{i} {r.nouveau - r.actuel:+.1f}" for i, r in ty.iterrows()))
    agg = {}
    for k, (w, imp, cur) in pt.items():
        g = k.split("_")[0] if k.startswith("couple") else k
        a = agg.setdefault(g, [0.0, 0.0])
        a[0] += (w * (imp - cur)).sum()
        a[1] += w.sum()
    p("P6", f"{nom} : par type de foyer, € par foyer " + " ; ".join(
        f"{g} {a[0]/a[1]:+,.0f} ({a[0]/1e9:+.1f} Md€)" for g, a in agg.items()))
    p("P7", f"{nom} : cas-types " + " ; ".join(
        f"{pr} {int(b/1e3)}k {ecart(n_ct, pr, b):+,.0f}" for pr, b in (
            ("seul", 21.5e3), ("seul", 30e3), ("seul", 50e3), ("seul", 80e3), ("seul", 150e3), ("couple_0enf", 50e3),
            ("couple_2enf", 30e3), ("couple_2enf", 50e3), ("couple_2enf", 80e3), ("couple_2enf_mono", 80e3),
            ("retraite_seul", 17e3), ("retraite_seul", 30e3))))
    eq = [ecart(n_ct, "seul", b) / b - ecart(n_ct, "couple_2enf", b) / b for b in (40e3, 60e3, 80e3, 100e3)]
    p("P7", f"{nom} : gain d'une personne seule moins gain d'un couple avec deux enfants (pts de brut) à 40/60/80/100 k€ "
            + " ".join(f"{-100*u:+.1f}" for u in eq))
    return dict(n=n, pt=pt, cout=c, deciles=d, perdants=per, ct=n_ct)


if __name__ == "__main__":
    L = []

    def p(tag, txt):
        s = f"[{tag}] {txt}"
        print(s, flush=True)
        L.append(s)
    p("P0", f"quotient familial des enfants aujourd'hui (IR 2024 sans niche, foyers représentatifs) : {QF_COUT:.1f} Md€"
            f" (couples {QF_COUPLES:.1f}, parents isolés {QF_ISOLES:.1f}) ; {ENFANTS/1e6:.1f} M d'enfants ; chèque égal"
            f" {CHEQUE:,.0f} € par enfant. Repère : Insee (André et Sireyjol 2021, Ines 2017) 16,6 Md€ pour l'ensemble des"
            f" dispositifs familiaux, dont 11,3 couples avec enfants et 2,0 familles monoparentales.")
    p("P0", "gain de QF d'un couple avec deux enfants, RFR " + " ".join(
        f"{int(r/1e3)}k {float(ir_actuel(np.array([r]), True, 0)[0] - ir_actuel(np.array([r]), True, 2)[0]):,.0f}"
        for r in (30e3, 40e3, 50e3, 60e3, 80e3, 120e3)))
    # étapes 1 à 3 (franchise de 6 000 € par enfant, pas de franchise d'activité), recalées dans cette représentation
    tau = cale_ex1()
    G = grille(0.0, "franchise", GRILLE_EX)
    r2, r3 = G.sort_values("transferts").iloc[0].to_dict(), G.sort_values("cout").iloc[0].to_dict()
    BAR = dict(ex1=dict(tau=tau), ex2=r2, ex3=r3)
    p("P1", f"exercice 1 : tranches de l'IR + {100*tau:.2f} % ; exercice 2 : " + _txt(r2) + " ; exercice 3 : " + _txt(r3))
    p("P1", "exercice 3, 5 barèmes les moins coûteux :\n" + G.sort_values("cout").head(5).round(3).to_string(index=False))
    for nom, (tm, T) in (("ex1", ex.bareme_empile(tau)), ("ex2", bareme(r2)), ("ex3", bareme(r3))):
        bilan(nom, tm, T, 0.0, "franchise", p)
    # correction 1 (déciles 2 à 4) : franchise sur les revenus d'activité, enfants traités par la franchise
    for F in (0.0, 4000.0, 6000.0, 8000.0, 10000.0):
        Gf = grille(F, "franchise", GRILLE_PROP)
        r = Gf.sort_values("cout").iloc[0].to_dict()
        BAR[f"F{int(F)}"] = dict(F=F, fam="franchise", **r)
        p("P2", f"franchise d'activité {F:,.0f} € : " + _txt(r))
        bilan(f"F{int(F/1e3)}k", *bareme(r), F, "franchise", p)
    # correction 2 (familles) : quatre traitements, franchise d'activité retenue
    for fam in ("rien", "franchise", "cheque", "quotient"):
        Gf = grille(F_RET, fam, GRILLE_PROP)
        r = Gf.sort_values("cout").iloc[0].to_dict()
        BAR[fam] = dict(F=F_RET, fam=fam, **r)
        p("P3", f"famille « {fam} », franchise d'activité {F_RET:,.0f} € : " + _txt(r))
        b = bilan(fam, *bareme(r), F_RET, fam, p)
        tm, T = bareme(r)
        seul = b["pt"]["seul"]
        p("P4", f"famille « {fam} » : aide aux familles dans l'impôt {aide_familiale(tm, T, F_RET, fam):.1f} Md€ (quotient"
                f" familial des enfants aujourd'hui {QF_COUT:.1f}) ; impôt brut avant chèques"
                f" {(W * b['n']).sum()/1e9 + (CHEQUE * ENFANTS / 1e9 if fam == 'cheque' else 0):.1f} Md€ ; personnes seules"
                f" sans enfant : {(seul[0] * (seul[1] - seul[2])).sum() / seul[0].sum():+,.0f} € par foyer par rapport à"
                f" aujourd'hui ; impôt d'un adulte sans enfant à 30/50/80 k€ nets "
                + " ".join(f"{float(T(np.clip(z - F_RET, 0, None))):,.0f}" for z in (30e3, 50e3, 80e3)))
    BAR["proposition"] = BAR[FAM_RET]
    (HERE / "sorties/proposition_baremes.json").write_text(json.dumps(BAR, indent=1), encoding="utf-8")
    (HERE / "sorties/proposition.txt").write_text("\n".join(L) + "\n", encoding="utf-8")
