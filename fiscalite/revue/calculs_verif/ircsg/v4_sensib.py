"""Sensibilité des chiffres clés aux hypothèses de construction des foyers purs (barème recalé chaque fois sur
220,1 Md€). Lancer depuis fiscalite/ : python3 -B <ce fichier>"""
import sys
import numpy as np, pandas as pd
sys.path.insert(0, "/tmp/claude-0/-home-user-Projets-annexes/935fc156-45bd-500a-b52a-e7e4ee23abb6/scratchpad/verif_ircsg/hyp")
import v2_independant as V
M = V.M
W, ZN, S = M.W, M.ZN, M.S
W_A, W_R = M.W_A, M.W_R

# ------------------------------------------------------------------ IR actuel recodé (revenus 2024, brochure 2025)
def bar_ir(q):
    return sum(t * np.clip(np.minimum(q, h) - s, 0, None) for s, h, t in zip(V.IRS, V.IRS[1:] + [np.inf], V.IRT))
def ir(r, couple, n, isole=False):
    p0 = 2.0 if couple else 1.0
    if couple:
        p = 2 + 0.5 * min(n, 2) + max(n - 2, 0); cap = 1791 * 2 * (p - p0)
    elif isole and n >= 1:
        p = 2 + 0.5 * min(max(n - 1, 0), 1) + max(n - 2, 0); cap = 4224 + 1791 * 2 * (p - 2)
    else:
        p = 1 + 0.5 * min(n, 2) + max(n - 2, 0); cap = 1791 * 2 * (p - 1)
    i0 = p0 * bar_ir(r / p0); i1 = np.maximum(p * bar_ir(r / p), i0 - cap)
    plaf = (i0 - cap > p * bar_ir(r / p)) & (n > 0)
    d = np.clip((1470 if couple else 889) - 0.4525 * i1, 0, None)
    return np.clip(i1 - d, 0, None), plaf

R = M.RFR_A
g_s = ir(R, False, 0)[0] - ir(R, False, 1, isole=True)[0]
g_c = ir(R, True, 0)[0] - ir(R, True, 2)[0]
w_pi, w_c2 = W_A * (1 - S) * M.NS_A, W_A * S * M.NC_A / 2
qf = ((w_pi * g_s).sum() + (w_c2 * g_c).sum()) / 1e9
print(f"QF des enfants recodé : {qf:.2f} Md€ (modèle 13,36) ; parents isolés {(w_pi*g_s).sum()/1e9:.2f}, couples {(w_c2*g_c).sum()/1e9:.2f}")
pl_c = ir(R, True, 2)[1]; pl_s = ir(R, False, 1, isole=True)[1]
print(f"Part des familles au plafond du QF (modèle) : couples à deux enfants {100*(w_c2*pl_c).sum()/w_c2.sum():.1f} % ;"
      f" parents isolés {100*(w_pi*pl_s).sum()/w_pi.sum():.1f} % ; ensemble {((w_c2*pl_c).sum()+(w_pi*pl_s).sum())/1e6:.2f} M de foyers"
      f" sur {(w_c2.sum()+w_pi.sum())/1e6:.2f} M ; seuil légal 70 829 € (3 parts) et 44 894 € (parent isolé, 2 parts)")
# variantes de représentation des enfants
for nom, n_pi, n_c in (("3 enfants par couple « avec enfants »", 1, 3),):
    nc_c = (18.0e6 - 1965339 * n_pi) / n_c
    print(f"   {nom} : couples avec enfants {nc_c/1e6:.2f} M")
# parents isolés à 1,6 enfant (moyenne approximative des familles monoparentales, non vérifiée) : 1 965 339 × 1,6
gs2 = ir(R, False, 0)[0] - (0.4 * ir(R, False, 2, isole=True)[0] + 0.6 * ir(R, False, 1, isole=True)[0])
n_enf_pi = 1965339 * 1.4
nc2 = (18.0e6 - n_enf_pi) / (W_A * S).sum()
w_c2b = W_A * S * nc2 / 2
qf2 = ((w_pi * gs2).sum() + (w_c2b * g_c).sum()) / 1e9
print(f"   parents isolés à 1,4 enfant en moyenne (60 % un, 40 % deux) : QF {qf2:.2f} Md€")

# ------------------------------------------------------------------ reconstruction des types et de la charge actuelle
def construit(k_couple_R=1.0, partage_R=None, ns_enf=1.0):
    """k_couple_R : multiplie la part des couples chez les retraités (celle des actifs est ajustée pour garder
    13,05 M de couples) ; partage_R : partage des pensions dans les couples de retraités ; ns_enf : sans effet ici."""
    S_R = np.clip(S * k_couple_R, 0, 0.95)
    extra = (W_R * (S_R - S)).sum()
    S_A = np.clip(S - extra / W_A.sum(), 0, 1) if True else S
    # garder le total exactement : ajustement proportionnel
    S_A = S * (1 - extra / (W_A * S).sum())
    NS = 1965339.0 / (W_A * (1 - S_A)).sum()
    NC = (18.0e6 - 1965339.0) / (W_A * S_A).sum()
    PR = partage_R or M.v.PARTAGE
    T = [("seul", "A", "seuls", W_A * (1 - S_A) * (1 - NS), [1.0], 0), ("parent_isole", "A", "parents_isoles", W_A * (1 - S_A) * NS, [1.0], 1)]
    for s_, p_ in M.v.PARTAGE:
        T += [(f"couple0_{s_}", "A", "couples0", W_A * S_A * (1 - NC / 2) * p_, [s_, 1 - s_], 0),
              (f"couple2_{s_}", "A", "couples2", W_A * S_A * NC / 2 * p_, [s_, 1 - s_], 2)]
    T.append(("retraite_seul", "R", "seuls", W_R * (1 - S_R), [1.0], 0))
    for s_, p_ in PR:
        T.append((f"retraite_couple_{s_}", "R", "couples0", W_R * S_R * p_, [s_, 1 - s_], 0))
    U = M._U
    key = lambda n: n if n in U else n.rsplit("_", 1)[0]
    norm = sum(w * U[key(n)] for n, _, _, w, _, _ in T) / W
    cur = {n: M.CUR * U[key(n)] / norm for n, *_ in T}
    return T, cur, NC

def evalue(T, cur, o, xs, ys_fn, lo=0.0, hi=0.5):
    V.TYPES[:] = T
    M.CURT.clear(); M.CURT.update(cur)
    t1 = V.cale(lambda t: V.recette(*V.lineaire(xs, ys_fn(t)), o), lo, hi, 32)
    tm, Tf = V.lineaire(xs, ys_fn(t1))
    ps = V.ps_v2(tm, Tf, o)[0]
    rp = V.repart(tm, Tf, o)
    return t1, ps, rp

T0, CUR0 = list(V.TYPES), dict(M.CURT)
NEUTRE = ([0, 20e3, 30e3, 250e3], lambda t: [.02, .14, t, .5], {})
PROP = ([0, 20e3, 45e3, 1e6], lambda t: [.14, .14, t, .5], dict(F=4000.0, fam="franchise", Fp=12500.0, deg=True))
def ligne(nom, T, cur, t0_alt=None):
    out = []
    for lab, (xs, yf, o) in (("neutre", NEUTRE), ("proposition", PROP)):
        V.TYPES[:] = T; M.CURT.clear(); M.CURT.update(cur)
        t1 = V.cale(lambda t: V.recette(*V.lineaire(xs, yf(t)), o), 0, .5, 32)
        tm, Tf = V.lineaire(xs, yf(t1))
        ps = V.ps_v2(tm, Tf, o, t0_alt=t0_alt)[0]
        rp = V.repart(tm, Tf, o)
        g = rp["groupes"]
        out.append(f"{lab} : t1 {100*t1:.1f} % ; PS {ps:+.2f} ; retraités {g['retraites'][0]:+.1f} Md€ ; couples de retraités {g['couples_retraites'][1]:+,} € ;"
                   f" retraité seul {g['seuls_retraites'][1]:+,} € ; couples 2 enf. {g['couples2'][0]:+.1f} Md€ ({g['couples2'][1]:+,} €) ; perdants {rp['perdants']} % ; déciles max {max(abs(u) for u in rp['dec'])}")
    print(f"[{nom}]\n    " + "\n    ".join(out))

import os
if os.environ.get("SEUL5"):
    M.v.PARTAGE = [(0.60, 1.0)]
    T, cur, _ = construit()
    ligne("S5 couples : 60/40 pour tous", T, cur)
    sys.exit()
ligne("référence (modèle)", T0, CUR0)
# S1 : CRDS dans le taux marginal actuel
# S1 (CRDS dans le taux actuel) : corrigé dans modele_purs.py le 16/11/2026 ; ligne retirée
# S2 : taux marginal actuel propre au type (OpenFisca, cas-types fins lissés), au lieu de la médiane de 4 profils par tranche
CT = M.CT
def tm_prof(prof):
    g = CT[CT.profil == prof].sort_values("brut")
    mg = ((g.actuel_plus - g.actuel) / 1000).rolling(9, center=True, min_periods=1).mean().values / 0.9825
    return lambda z: np.interp(z, g.brut.values * 0.9825, mg)
zA = M.Z_A
t0_type = {"seuls": tm_prof("seul")(zA), "parents_isoles": tm_prof("seul")(zA), "couples0": tm_prof("couple_0enf")(zA), "couples2": tm_prof("couple_2enf")(zA)}
print("   taux actuel par type à 25/40/60/100 k€ (brut) : " + " | ".join(
    f"{k} " + " ".join(f"{100*np.interp(z, zA, v):.0f}" for z in (25e3, 40e3, 60e3, 100e3)) for k, v in t0_type.items())
    + " ; modèle (médiane par tranche) " + " ".join(f"{100*np.interp(z, zA, M.TAU0):.0f}" for z in (25e3, 40e3, 60e3, 100e3)))
ligne("S2 taux marginal actuel par type (OpenFisca)", T0, CUR0, t0_alt=t0_type)
# S3 : plus de couples chez les retraités (4,3 M au lieu de 3,75 M ; 1BS = 4,32 M)
for k in (4.32 / 3.75,):
    T, cur, NC = construit(k_couple_R=k)
    print(f"   S3 : couples de retraités {sum(w.sum() for n,g,f,w,p,kk in T if g=='R' and f=='couples0')/1e6:.2f} M ; couples actifs avec deux enfants {NC/2*100:.0f} %")
    ligne("S3 couples de retraités = 4,32 M (cases 1BS)", T, cur)
# S4 : partage des pensions plus égal dans les couples de retraités
T, cur, _ = construit(partage_R=[(0.62, 1.0)])
ligne("S4 couples de retraités : partage 62/38 pour tous", T, cur)
T, cur, _ = construit(partage_R=[(1.0, 0.30), (0.62, 0.70)])
ligne("S4b couples de retraités : 30 % à une seule pension, 70 % à 62/38", T, cur)
# S5 : partage des couples d'actifs plus égal (part du second revenu 40 % pour tous)
PA0 = M.v.PARTAGE
M.v.PARTAGE = [(0.60, 1.0)]
T, cur, _ = construit()
ligne("S5 couples d'actifs et de retraités : 60/40 pour tous", T, cur)
M.v.PARTAGE = PA0
