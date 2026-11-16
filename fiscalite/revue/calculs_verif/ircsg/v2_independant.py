"""Recalcul indépendant des chiffres clés de la partie IR-CSG (foyers purs, méthode v2).
On ne reprend du modèle que ses ENTRÉES (poids, revenus, part des couples, partage, charge actuelle par type, taux
marginal actuel, coins hors IR-CSG) ; barèmes, impôt des types, agrégats, répartition, cas-types et perte sèche sont
recodés ici. Lancer : cd fiscalite && python3 -B <ce fichier>"""
import sys
import numpy as np, pandas as pd
ROOT = "/home/user/Projets-annexes/fiscalite"
sys.path[:0] = [ROOT + "/synthese", ROOT + "/ir_csg", ROOT]
import modele_purs as M  # entrées seulement
import ps_ircsg_methode as ps

W, ZN, Q, DEC, S = M.W, M.ZN, M.Q, M.DEC, M.S
W_A, W_R, Z_A, R_A, LAB_A, ACT = M.W_A, M.W_R, M.Z_A, M.R_A, M.LAB_A, M.ACTIV_A
NS, NC = M.NS_A, M.NC_A
CIBLE = M.CIBLE
TAU0 = M.TAU0

# ------------------------------------------------------------------ barèmes recodés (intégration numérique)
GRID = np.concatenate([np.arange(0, 2e6, 5.0), np.arange(2e6, 6e7, 500.0)])
def lineaire(xs, ys):
    tmg = np.interp(GRID, xs, ys)
    cum = np.concatenate([[0], np.cumsum(np.diff(GRID) * (tmg[1:] + tmg[:-1]) / 2)])
    return (lambda z: np.interp(np.asarray(z, float), xs, ys)), (lambda z: np.interp(np.asarray(z, float), GRID, cum))
IRS, IRT = [0, 11497, 29315, 83823, 180294], [0, .11, .30, .41, .45]
def empile(tau):
    def T(z):
        z = np.asarray(z, float); out = tau * z
        for i, (s, t) in enumerate(zip(IRS, IRT)):
            h = IRS[i + 1] if i + 1 < len(IRS) else np.inf
            out = out + t * np.clip(np.minimum(z, h) - s, 0, None)
        return out
    def tm(z):
        z = np.asarray(z, float)
        return np.select([z < s for s in IRS[1:]], IRT[:-1], IRT[-1]) + tau
    return tm, T
def bar(t0, tb, z1, t1, z2):
    return lineaire([0, 20e3, z1, z2], [t0, tb, t1, .50])

# ------------------------------------------------------------------ types de foyers (recodés)
TYPES = [("seul", "A", "seuls", W_A * (1 - S) * (1 - NS), [1.0], 0), ("parent_isole", "A", "parents_isoles", W_A * (1 - S) * NS, [1.0], 1)]
for s_, p_ in M.v.PARTAGE:
    TYPES += [(f"couple0_{s_}", "A", "couples0", W_A * S * (1 - NC / 2) * p_, [s_, 1 - s_], 0),
              (f"couple2_{s_}", "A", "couples2", W_A * S * NC / 2 * p_, [s_, 1 - s_], 2)]
TYPES.append(("retraite_seul", "R", "seuls", W_R * (1 - S), [1.0], 0))
for s_, p_ in M.v.PARTAGE:
    TYPES.append((f"retraite_couple_{s_}", "R", "couples0", W_R * S * p_, [s_, 1 - s_], 0))
assert abs(sum(t[3].sum() for t in TYPES) - W.sum()) < 1

def impot(tm, T, o, grp, parts, kids, sans=None):
    F, Fp = o.get("F", 0.0), o.get("Fp", 0.0)
    zs = [sh * ZN for sh in parts]
    act = [sh * ACT if grp == "A" else 0 * ZN for sh in parts]
    pen = [sh * ZN if grp == "R" else 0 * ZN for sh in parts]
    if o.get("sur") == "tout":
        act = list(zs)
    if sans is not None:
        zs[sans] = np.clip(zs[sans] - parts[sans] * ACT, 0, None); act[sans] = 0 * ZN
    exo = [np.clip(2 * Fp - p, 0, p) if o.get("deg") else np.minimum(Fp, p) for p in pen]
    exo = [e + o.get("abat", 0.0) * p for e, p in zip(exo, pen)]
    tax = [np.clip(z - np.minimum(F, a) - e, 0, None) for z, a, e in zip(zs, act, exo)]
    if o.get("fam") == "franchise" and kids:
        k_haut = np.argmax(np.vstack(zs), axis=0) if len(zs) == 2 else np.zeros(len(ZN), int)
        tax = [np.where(k_haut == k, np.clip(t - 6000.0 * kids, 0, None), t) for k, t in enumerate(tax)]
    imp = sum(T(t) for t in tax)
    mg = [np.where((a > F) & (t > 0), tm(t), 0.0) for a, t in zip(act, tax)]
    return imp, mg

def recette(tm, T, o):
    return sum((w * impot(tm, T, o, g, parts, k)[0]).sum() for _, g, _, w, parts, k in TYPES) / 1e9

def cale(f, lo, hi, n=45):
    for _ in range(n):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if f(mid) < CIBLE else (lo, mid)
    return (lo + hi) / 2

# ------------------------------------------------------------------ perte sèche v2 recodée
V2 = {"bas": ((0.02, 0.05, 0.05, 0.05), 0.10), "central": ((0.05, 0.10, 0.10, 0.10), 0.25), "haut": ((0.10, 0.20, 0.25, 0.25), 0.50)}
def ps_v2(tm, T, o, jeu="central", t0_alt=None):
    (a, b, c, d), eta = V2[jeu]
    eR = np.where(Q < .5, a, np.where(Q < .9, b, np.where(Q < .99, c, d)))
    intens = np.zeros(4); ext = 0.0
    bands = [Q < .5, (Q >= .5) & (Q < .9), (Q >= .9) & (Q < .99), Q >= .99]
    for nom, g_, fam, w, parts, kids in TYPES:
        if g_ != "A":
            continue
        imp, mgs = impot(tm, T, o, g_, parts, kids)
        single = 1.0 if len(parts) == 1 else 0.0
        for k, (sh, mg) in enumerate(zip(parts, mgs)):
            t0 = TAU0 if t0_alt is None else t0_alt[fam]
            t1 = np.clip(mg * R_A, 0, .95)
            g = sh * Z_A * LAB_A
            er, ee, pa = ps.coin(g, single, "nc")
            er, ee, pa = ps.SALSH * er, ps.SALSH * ee, ps.SALSH * pa
            coin = er + ee + pa + (t0 + t1) / 2
            dq = eR * g * (np.log(1 - t1) - np.log(1 - t0))
            for i, m_ in enumerate(bands):
                intens[i] += (w * -coin * dq * m_).sum() / 1e9
            imp_wo = impot(tm, T, o, g_, parts, kids, sans=k)[0]
            p1 = np.where(g > 0, (imp - imp_wo) / np.maximum(g, 1.0), 0.0)
            if (nom, k) in M.PTR0:
                p0 = M.PTR0[(nom, k)]
            else:                                   # type absent du modèle (tests) : même formule que modele_purs._ptr0
                gg = sh * Z_A * LAB_A
                d0 = M.P.ir_actuel(M.RFR_A, len(parts) == 2, kids) - M.P.ir_actuel(np.clip(M.RFR_A - 0.75 * gg, 0, None), len(parts) == 2, kids)
                p0 = np.where(gg > 0, d0 / np.maximum(gg, 1.0) + 0.097, 0.0)
            rest = ps.ptr_rest_single(g) - 0.1005 if single else 0.0126
            P0, P1 = np.clip(p0 + rest, -.5, .97), np.clip(p1 + rest, -.5, .97)
            dans = (g > 1000) & (g < 2 * ps.SMIC)
            ext += (w * eta * g * (np.log((1 - P0) / (1 - P1)) - (P1 - P0)) * dans).sum() / 1e9
    return intens.sum() + ext, intens, ext

# ------------------------------------------------------------------ répartition recodée
def repart(tm, T, o):
    rows = []
    for nom, g_, fam, w, parts, kids in TYPES:
        imp = impot(tm, T, o, g_, parts, kids)[0]
        rows.append((nom, g_, fam, w, imp - M.CURT[nom]))
    dn = sum(w * d for *_, w, d in rows)
    dec = pd.DataFrame({"d": DEC, "w": W, "dn": dn}).groupby("d").sum()
    grp = {}
    for cle, f in (("actifs", lambda g, f: g == "A"), ("retraites", lambda g, f: g == "R"),
                   ("couples2", lambda g, f: f == "couples2"), ("parents_isoles", lambda g, f: f == "parents_isoles"),
                   ("seuls_retraites", lambda g, f: g == "R" and f == "seuls"), ("couples_retraites", lambda g, f: g == "R" and f == "couples0")):
        sel = [(w, d) for _, g, fm, w, d in rows if f(g, fm)]
        md = sum((w * d).sum() for w, d in sel) / 1e9; nb = sum(w.sum() for w, _ in sel)
        grp[cle] = (round(md, 1), round(1e9 * md / nb))
    perd = sum((w * (d > 500)).sum() for *_, w, d in rows) / W.sum()
    return dict(dec=[round(u) for u in dec.dn / dec.w], groupes=grp, perdants=round(100 * perd),
                top10=round((dn * (Q >= .9)).sum() / 1e9, 1), top1=round((dn * (Q >= .99)).sum() / 1e9, 1))

# ------------------------------------------------------------------ cas-types recodés
CT = M.CT
def cas(tm, T, o, prof, brut):
    g = CT[(CT.profil == prof) & (CT.brut == brut)].iloc[0]
    kids = M.ENF_CT[prof]
    if prof == "retraite_seul":
        p = g.base_a; Fp = o.get("Fp", 0.0)
        exo = (np.clip(2 * Fp - p, 0, p) if o.get("deg") else min(Fp, p)) + o.get("abat", 0.0) * p
        act = p if o.get("sur") == "tout" else 0.0
        t = max(p - min(o.get("F", 0.0), act) - exo, 0.0)
        return float(T(t)) - g.actuel
    zs = [g.base_a] + ([g.base_b] if g.base_b > 0 else [])
    tax = [max(z - min(o.get("F", 0.0), z), 0.0) for z in zs]
    if o.get("fam") == "franchise" and kids:
        k = int(np.argmax(zs)); tax[k] = max(tax[k] - 6000.0 * kids, 0.0)
    return float(sum(T(t) for t in tax)) - g.actuel

CAS = (("retraite_seul", 17e3), ("seul", 21.5e3), ("couple_2enf", 50e3), ("couple_2enf_mono", 50e3), ("couple_2enf_mono", 80e3), ("couple_2enf", 80e3))

def bilan(nom, tm, T, o):
    r = {j: ps_v2(tm, T, o, j) for j in V2}
    rp = repart(tm, T, o)
    print(f"[{nom}] recette {recette(tm, T, o):.2f} ; perte sèche v2 central {r['central'][0]:+.2f} (bas {r['bas'][0]:+.2f}, haut {r['haut'][0]:+.2f}) ;"
          f" intensive {r['central'][1].sum():+.2f} [" + " ".join(f"{u:+.2f}" for u in r['central'][1]) + f"] ; extensive {r['central'][2]:+.2f}")
    print(f"    déciles {rp['dec']} ; 10 % {rp['top10']} ; 1 % {rp['top1']} ; perdants>500 {rp['perdants']} % ; groupes (Md€, €) {rp['groupes']}")
    print("    cas-types " + " ; ".join(f"{p} {b/1e3:.1f}k {cas(tm, T, o, p, b):+,.0f}" for p, b in CAS))
    return r

if __name__ == "__main__":
    o0 = {}
    # étape 1
    r_ir = recette(*empile(0.0), o0)
    tau = cale(lambda t: recette(*empile(t), o0), -0.1, 0.2)
    print(f"ÉTAPE 1 : barème IR par adulte sur l'assiette large {r_ir:.2f} Md€ ; taux proportionnel {100*tau:.3f} %")
    bilan("étape 1", *empile(tau), o0)
    # barème neutre
    bN = (0.02, 0.14, 30e3, None, 250e3)
    t1 = cale(lambda t: recette(*bar(.02, .14, 30e3, t, 250e3), o0), 0, .5)
    print(f"NEUTRE : t1 recalé {100*t1:.2f} %")
    bilan("neutre", *bar(.02, .14, 30e3, t1, 250e3), o0)
    # franchise 4 000 € : décalage de tous les taux sous 50 %
    o4 = dict(F=4000.0)
    d = cale(lambda d: recette(*lineaire([0, 20e3, 30e3, 250e3], [.02 + d, .14 + d, t1 + d, .5]), o4), -0.15, 0.3)
    print(f"NEUTRE + franchise 4 000 € : +{100*d:.2f} points")
    bilan("neutre + F4000", *lineaire([0, 20e3, 30e3, 250e3], [.02 + d, .14 + d, t1 + d, .5]), o4)
    # proposition
    oP = dict(F=4000.0, fam="franchise", Fp=12500.0, deg=True)
    tP = cale(lambda t: recette(*lineaire([0, 20e3, 45e3, 1e6], [.14, .14, t, .5]), oP), 0, .5)
    print(f"PROPOSITION : t1 recalé {100*tP:.2f} % (sortie : 30,3 %)")
    bilan("proposition", *lineaire([0, 20e3, 45e3, 1e6], [.14, .14, tP, .5]), oP)
    # gain atteignable
    tA = cale(lambda t: recette(*lineaire([0, 20e3, 60e3, 2e6], [.16, .16, t, .5]), o4), 0, .5)
    print(f"ATTEIGNABLE : t1 recalé {100*tA:.2f} % (sortie : 16,4 %)")
    bilan("atteignable (F 4 000)", *lineaire([0, 20e3, 60e3, 2e6], [.16, .16, tA, .5]), o4)
