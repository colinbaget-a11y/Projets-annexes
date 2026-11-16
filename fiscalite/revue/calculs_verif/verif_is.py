"""Recalcul indépendant des chiffres de la partie IS (n'importe pas simulation_is.py).

Sorties : verif_is_sortie.txt dans le même dossier.
Conventions : année 1 = 2027 ; Md€ courants sauf mention ; part imposable s = 75 % au centre.
"""
from pathlib import Path
import numpy as np

OUT = Path(__file__).resolve().parent / "verif_is_sortie.txt"
L = []
p = L.append

# ------------------------------------------------------------------ données sources (relues ici)
I25 = 75.524 + 8.534          # Insee 8.212, flux 2025 : autres machines + TIC, SNF
K25 = 512.115 + 28.802        # Insee 8.212, patrimoine fin 2025, mêmes actifs
K24 = 499.198 + 27.934
CCF25 = 70.475 + 6.789        # consommation de capital fixe 2025
I19 = 61.503 + 5.358
I22 = 68.893 + 7.645
B15, B25, B265, B275 = 27.0, 202.0, 39.0, 10.0   # DGFiP Stat. 21, graphique 2 (xlsx), 2022
BN22 = B25 + B265 + B275                        # 251
PIB25 = 2991.056                                # Insee (donnees/pib_france_cp_meur.json)
# Croissance du bénéfice fiscal (VM tome I PLF 2025 et PLF 2026) : 2023 +1 %, 2024 0 %, 2025 +1 % ;
# 2026 : +2,5 % prévu au PLF 2026, révisé à la baisse au PLF 2027 (chiffre non publié en ligne).
BFI_OFF = {2023: 0.01, 2024: 0.00, 2025: 0.01}
BFI_HYP = {2026: 0.02, 2027: 0.02}             # hypothèse de ce contrôle

TAU, S, G = 0.25, 0.75, 0.03
R_ENT, R_ETAT = 0.05, 0.0325
H = 60


def fac_bfi(a0, a1, hyp=BFI_HYP):
    f = 1.0
    for a in range(a0 + 1, a1 + 1):
        f *= 1 + {**BFI_OFF, **hyp}.get(a, G)
    return f


A22_SCRIPT = 1.03 ** 5
A22_OFF = fac_bfi(2022, 2027)
A25_OFF = fac_bfi(2025, 2027)
p(f"[DONNEES] investissement éligible 2025 {I25:.2f} ; stock fin 2025 {K25:.1f} ; CCF/stock moyen "
  f"{CCF25/((K24+K25)/2):.3f} ; croissance annuelle 2019-2025 {100*((I25/I19)**(1/6)-1):.1f} %, 2022-2025 "
  f"{100*((I25/I22)**(1/3)-1):.1f} %")
p(f"[DONNEES] facteur 2022->2027 : script {A22_SCRIPT:.3f} ; bénéfice fiscal officiel + hyp. 2 %/an en 2026-27 "
  f"{A22_OFF:.3f} (fourchette 0 % à 2,5 % en 2026-27 : {fac_bfi(2022, 2027, {2026: 0, 2027: 0}):.3f} à "
  f"{fac_bfi(2022, 2027, {2026: .025, 2027: .025}):.3f})")


# ------------------------------------------------------------------ plans d'amortissement (écrits à neuf)
def plan_lin(n=7):
    return np.array([0.5 / n] + [1 / n] * (n - 1) + [0.5 / n])


def plan_deg_bofip(n=7, coef=2.25, prorata=0.5):
    """BOI-BIC-AMT-20-20-30 § 260 : l'exercice d'acquisition compte pour une année entière ;
    bascule au linéaire quand VNC / années restantes dépasse l'annuité dégressive ; n exercices."""
    t = coef / n
    v, d = 1.0, []
    for k in range(n):
        reste = n - k
        a_deg = t * v * (prorata if k == 0 else 1)
        a_lin = v / reste
        a = a_deg if (k == 0 or a_deg >= a_lin) else a_lin
        if k == n - 1:
            a = v
        d.append(a)
        v -= a
    return np.array(d)


def plan_deg_script(n=7):
    taux = 2.25 / n
    reste, d = 1.0, []
    for k in range(n + 1):
        ar = n - k + 0.5
        lin = reste / ar if ar > 0 else reste
        dk = min((0.5 if k == 0 else 1.0) * max(taux * reste, lin), reste)
        d.append(dk)
        reste -= dk
    d[-1] += reste
    return np.array(d)


def zval(d, r):
    return float(np.sum(d / (1 + r) ** np.arange(len(d))))


PLANS = {"lin": plan_lin(), "deg": plan_deg_script(), "deg_bofip": plan_deg_bofip()}
for k, d in PLANS.items():
    p(f"[Z] {k:9s} annuités {np.round(d, 4).tolist()} ; z(5 %) {zval(d, .05):.4f} ; z(3,25 %) {zval(d, R_ETAT):.4f}"
      f" ; z(3 %) {zval(d, .03):.4f} ; z(8 %) {zval(d, .08):.4f}")


# ------------------------------------------------------------------ coût annuel : formule par millésime
def cout(plan, b, s=S, g=G, i1=None, h=H, tau=TAU):
    """coût(t) = tau s sum_v b_v I_v (1{t=v} - d_{t-v}) ; b : fonction de v (0-indexé)."""
    i1 = I25 * (1 + g) ** 2 if i1 is None else i1
    c = np.zeros(h + len(plan))
    for v in range(h):
        bv = b(v)
        if bv == 0:
            continue
        Iv = i1 * (1 + g) ** v
        c[v] += tau * s * bv * Iv
        c[v:v + len(plan)] -= tau * s * bv * Iv * plan
    return c[:h]


I1 = I25 * (1 + G) ** 2
p(f"[I1] investissement éligible 2027 : {I1:.2f} Md€")
FULL = lambda v: 1.0
HALF = lambda v: 0.5
PAL = lambda v: 0.5 if v < 6 else 1.0
for nom, b in (("100 %", FULL), ("50 %", HALF), ("50 % puis 100 % en an 7", PAL)):
    for k in ("lin", "deg", "deg_bofip"):
        c = cout(PLANS[k], b)
        p(f"[COUT] {nom:24s} {k:9s} an1 {c[0]:5.2f} an2 {c[1]:5.2f} an7 {c[6]:5.2f} an8 {c[7]:5.2f} an10 {c[9]:5.2f}"
          f" an20 {c[19]:5.2f} | an8 en € 2027 {c[7]/1.03**7:4.2f}")
# vérification de la formule fermée en régime permanent
for k in ("lin", "deg"):
    ss = TAU * S * I1 * 1.03 ** 7 * (1 - zval(PLANS[k], G))
    p(f"[COUT] régime permanent an 8, formule fermée tau s I (1 - z(g)) [{k}] : {ss:.2f}")
for s in (0.6, 0.9):
    p(f"[COUT] an 1, part {s:.0%} : lin {cout(PLANS['lin'], FULL, s=s)[0]:.1f} ; deg {cout(PLANS['deg'], FULL, s=s)[0]:.1f}")

# ------------------------------------------------------------------ valeur actualisée par millésime
for k in ("lin", "deg", "deg_bofip"):
    for r in (R_ENT, R_ETAT):
        v = [TAU * s * I1 * (1 - zval(PLANS[k], r)) for s in (0.6, 0.75, 0.9)]
        p(f"[VA] {k:9s} r={r:.4f} : " + " / ".join(f"{x:.2f}" for x in v)
          + f" ; 50 % : {TAU*.75*I1*.5*(1-zval(PLANS[k], r)):.2f}")

# ------------------------------------------------------------------ point de taux et financement
for lab, a22, a25 in (("script (3 %/an)", A22_SCRIPT, 1.03 ** 2), ("corrigé (bénéfice fiscal)", A22_OFF, A25_OFF)):
    point = (BN22 + B15) * a22 / 100
    point_tr = BN22 * a22 / 100
    tr_haut = 0.10 * B15 * a22
    cir, zon, brev = 0.569 * a25, 0.524 * a25, 1.258 / 2 * a25
    haut = tr_haut + cir + zon + brev
    p(f"[FIN] {lab} : point (taux réduit supprimé) {point:.2f} ; point (taux réduit gardé) {point_tr:.2f} ; "
      f"taux réduit {tr_haut:.2f} ; CIR {cir:.2f} ; zones {zon:.2f} ; brevets {brev:.2f} ; total haut {haut:.2f}")
    for e in (0, 1.0, 1.5):
        b0 = BN22 * a22
        rec = 0.28 * b0 * (1 - e / 100 * 3) - 0.25 * b0
        p(f"[FIN]    28 %, semi-élasticité {e} : {rec:.2f}")
PRUD = 1.7 * 1.03 ** 8 + (0.57 + 0.52 + 0.2) * 1.03 ** 2
p(f"[FIN] borne prudente du script : taux réduit {1.7*1.03**8:.2f} + niches {(0.57+0.52+0.2)*1.03**2:.2f} = {PRUD:.2f} ; "
  f"rapport au statique corrigé {1.7*1.03**8/(0.1*B15*A22_OFF):.2f}")
# niveau de recette implicite en 2027
for lab, a22 in (("script", A22_SCRIPT), ("corrigé", A22_OFF)):
    brut = (0.25 * BN22 + 0.15 * B15) * a22
    p(f"[COHERENCE] IS brut liquidé 2027 implicite ({lab}) : {brut:.1f} Md€ ; IS brut 2022 DGFiP 68,4 ; "
      f"IS net 2027 PLF 58,5 (hors contribution exceptionnelle)")


# ------------------------------------------------------------------ dette de transition
def dette(plan, b, fin, r=R_ETAT, g=G, h=H, s=S, extra=None):
    c = cout(plan, b, s=s, g=g, h=h)
    f = fin * (1 + g) ** np.arange(h)
    if extra is not None:
        f = f + extra[:h]
    sol = f - c
    d, D = 0.0, np.zeros(h)
    for t in range(h):
        d = d * (1 + r) - sol[t]
        D[t] = d
    pk = int(np.argmax(D))
    rem = next((t + 1 for t in range(pk, h) if D[t] <= 0), None)
    return D, sol, pk, rem


def ligne(nom, k, b, fin, **kw):
    D, sol, pk, rem = dette(PLANS[k], b, fin, **kw)
    return f"{nom} [{k}] fin {fin:.2f} : max {D[pk]:5.1f} (an {pk+1}), remboursée an {rem}", D, sol


FIN_SCRIPT = (PRUD, 0.1 * B15 * A22_SCRIPT + (0.569 + 0.524 + 0.629) * 1.03 ** 2)
FIN_CORR = (PRUD, 0.1 * B15 * A22_OFF + (0.569 + 0.524 + 0.629) * A25_OFF)
for lab, fins, point in (("script", FIN_SCRIPT, (BN22 + B15) * A22_SCRIPT / 100),
                         ("corrigé", FIN_CORR, (BN22 + B15) * A22_OFF / 100)):
    for k in ("lin", "deg", "deg_bofip"):
        for nom, b in (("S3 calendrier", PAL), ("S4 100 % dès 2027", FULL), ("S1 50 % permanent", HALF)):
            for f in fins:
                txt, D, sol = ligne(f"[DETTE {lab}] {nom}", k, b, f)
                pts = sol[19] / (point * 1.03 ** 19)
                p(txt + f" ; excédent an 20 en points {pts:.2f}")

# niches seules (sans taux réduit) : la dette n'est jamais remboursée ?
for k in ("lin", "deg"):
    for f in ((0.57 + 0.52 + 0.2) * 1.03 ** 2, (0.569 + 0.524 + 0.629) * A25_OFF):
        D, sol, pk, rem = dette(PLANS[k], PAL, f)
        p(f"[DETTE niches seules] S3 [{k}] fin {f:.2f} : dette an 30 {D[29]:.1f}, an 40 {D[39]:.1f} ; remboursée {rem}")

# sensibilité au taux d'intérêt et à la croissance
for r in (0.025, 0.0325, 0.04, 0.05):
    out = []
    for k, f in (("lin", PRUD), ("deg", FIN_CORR[1])):
        D, sol, pk, rem = dette(PLANS[k], PAL, f, r=r)
        out.append(f"{k} {f:.1f}: max {D[pk]:.1f} rembours. an {rem}")
    p(f"[SENS r_etat={r}] S3 : " + " ; ".join(out))
for g in (0.02, 0.03, 0.04):
    out = []
    for k, f in (("lin", PRUD), ("deg", FIN_CORR[1])):
        D, sol, pk, rem = dette(PLANS[k], PAL, f, g=g)
        c = cout(PLANS[k], FULL, g=g)
        out.append(f"{k} {f:.1f}: max {D[pk]:.1f} rembours. an {rem} ; coût permanent an 8 {c[7]:.2f}")
    p(f"[SENS g={g}] S3 : " + " ; ".join(out))
for n in (5, 7, 10):
    pl = plan_lin(n)
    c = cout(pl, FULL)
    p(f"[SENS durée {n} ans, linéaire] an1 {c[0]:.1f} ; an{n+1} {c[n]:.2f} ; VA 5 % {TAU*S*I1*(1-zval(pl, .05)):.2f} ; "
      f"VA 3,25 % {TAU*S*I1*(1-zval(pl, R_ETAT)):.2f} ; coin m {TAU*(1-zval(pl, .05))/(1-TAU):.3f}")
# avec les matériels de transport (126,2 Md€ au lieu de 84,1)
c = cout(PLANS["lin"], FULL, i1=(I25 + 42.094) * 1.03 ** 2)
p(f"[SENS transport inclus] an1 lin {c[0]:.1f} (contre {cout(PLANS['lin'], FULL)[0]:.1f})")

# contribution exceptionnelle prolongée deux ans (5 Md€ en 2027 et 2028) affectée à la transition
extra = np.zeros(H)
extra[0:2] = 5.0
for k, f in (("lin", PRUD), ("lin", FIN_CORR[1]), ("deg", PRUD), ("deg", FIN_CORR[1])):
    for nom, b in (("S3", PAL), ("S4", FULL)):
        D, sol, pk, rem = dette(PLANS[k], b, f, extra=extra)
        D0, _, pk0, rem0 = dette(PLANS[k], b, f)
        p(f"[CE] {nom} [{k}] fin {f:.2f} : sans CE max {D0[pk0]:.1f} rembours. an {rem0} ; avec CE 5+5 max "
          f"{D[pk]:.1f} rembours. an {rem}")

# ------------------------------------------------------------------ petite société
zl5, zl50 = zval(PLANS["lin"], .05), zval(0.5 * np.eye(1, 8, 0).ravel() + 0.5 * PLANS["lin"], .05)
for r in (0.05, 0.08, 0.10):
    zl = zval(PLANS["lin"], r)
    zh = zval(0.5 * np.eye(1, 8, 0).ravel() + 0.5 * PLANS["lin"], r)
    zd = zval(PLANS["deg_bofip"], r)
    zdh = zval(0.5 * np.eye(1, 7, 0).ravel() + 0.5 * PLANS["deg_bofip"], r)
    p(f"[PME r={r}] seuil de compensation de 4 250 € : 50 % lin {4250/(TAU*(zh-zl)):,.0f} ; 100 % lin "
      f"{4250/(TAU*(1-zl)):,.0f} ; 50 % dég {4250/(TAU*(zdh-zd)):,.0f} ; 100 % dég {4250/(TAU*(1-zd)):,.0f}".replace(",", " "))
for i in (20_000, 50_000):
    av50 = TAU * i * (0.5 + 0.5 * PLANS["lin"][0] - PLANS["lin"][0])
    av100 = TAU * i * (1 - PLANS["lin"][0])
    p(f"[PME] avance 1re année pour {i} € : 50 % {av50:,.0f} ; 100 % {av100:,.0f}".replace(",", " "))
p(f"[PME] IS + PFU sur 42 500 € distribués : {100*(0.15+0.85*0.314):.2f} % -> {100*(0.25+0.75*0.314):.2f} %")
p(f"[PME] hausse d'IS pour 30 000 € : {0.25*30000-0.15*30000:.0f} € (+{100*(0.25/0.15-1):.1f} %)")

# ------------------------------------------------------------------ coût d'usage, taux effectifs (Devereux-Griffith)
def dg(tau, A, p_=None, r=0.05, pi=0.02, delta=0.14):
    """Devereux-Griffith (2003), financement par fonds propres, sans impôt personnel.
    A = tau * z (z actualisé au taux nominal rho). Renvoie (p_tilde, EMTR, EATR(p_))."""
    rho = (1 + r) * (1 + pi) - 1
    ptil = (1 - A) * (rho + delta * (1 + pi) - pi) / ((1 - tau) * (1 + pi)) - delta
    emtr = (ptil - r) / ptil
    eatr = None
    if p_ is not None:
        Rstar = (p_ - r) / (1 + r)
        R = -(1 - A) + ((1 + pi) * (p_ + delta) * (1 - tau) + (1 + pi) * (1 - delta) * (1 - A)) / (1 + rho)
        eatr = (Rstar - R) / (p_ / (1 + r))
    return ptil, emtr, eatr


rho = 1.05 * 1.02 - 1
cases = [("aujourd'hui, linéaire 7 ans, 25 %", .25, zval(PLANS["lin"], rho)),
         ("aujourd'hui, dégressif, 25 %", .25, zval(PLANS["deg_bofip"], rho)),
         ("50 % immédiat + linéaire, 25 %", .25, zval(0.5 * np.eye(1, 8, 0).ravel() + 0.5 * PLANS["lin"], rho)),
         ("100 % immédiat, 25 %", .25, 1.0),
         ("baisse du taux à 24 %, linéaire", .24, zval(PLANS["lin"], rho)),
         ("baisse du taux à 20 %, linéaire", .20, zval(PLANS["lin"], rho)),
         ("hausse à 28 %, linéaire", .28, zval(PLANS["lin"], rho)),
         ("hausse à 28 %, 100 % immédiat", .28, 1.0),
         ("petite société sous le plafond aujourd'hui (15 %), linéaire", .15, zval(PLANS["lin"], rho)),
         ("petite société après réforme (25 %), 50 %", .25, zval(0.5 * np.eye(1, 8, 0).ravel() + 0.5 * PLANS["lin"], rho)),
         ("petite société après réforme (25 %), 100 %", .25, 1.0)]
for nom, tau, z in cases:
    pt, emtr, eatr = dg(tau, tau * z, p_=0.20)
    m = tau * (1 - z) / (1 - tau)
    p(f"[TEF équipements] {nom:58s} z {z:.3f} coin m {100*m:5.2f} % ; TEMI {100*emtr:5.1f} % ; TEMA (20 %) {100*eatr:5.1f} %")
# bâtiments (non éligibles) : 25 ans linéaire, delta 3 % économique (convention OCDE 3,1 %)
zb = zval(plan_lin(25), rho)
for nom, tau in (("bâtiment, 25 %", .25), ("bâtiment, 28 %", .28), ("bâtiment, 24 %", .24),
                 ("bâtiment, petite société 15 %", .15)):
    pt, emtr, eatr = dg(tau, tau * zb, p_=0.20, delta=0.031)
    p(f"[TEF bâtiments] {nom:30s} z {zb:.3f} ; TEMI {100*emtr:5.1f} % ; TEMA {100*eatr:5.1f} %")

# ------------------------------------------------------------------ réforme naïve : baisse générale du taux
POINT_TR = BN22 * A22_OFF / 100       # taux réduit maintenu
for pts in (1, 3, 5):
    stat = pts * POINT_TR
    dyn = [(0.25 - pts / 100) * BN22 * A22_OFF * (1 + e / 100 * pts) - 0.25 * BN22 * A22_OFF for e in (1.0, 1.5)]
    p(f"[NAIVE] baisse de {pts} pt : coût statique {stat:.1f} Md€ ; avec retour de bénéfices (1 à 1,5 %/pt) "
      f"{-dyn[0]:.1f} à {-dyn[1]:.1f}")
# à qui profite un point (répartition des bénéfices 2022 au taux normal, hypothèse sur la base à 15 %)
ben = {"TPE": 60.3, "PME": 75.9, "ETI": 62.2, "GE": 79.5}
isb = {"TPE": 13.1, "PME": 18.9, "ETI": 15.8, "GE": 20.6}
for lab, part_tpe in (("base à 15 % toute en TPE", 1.0), ("base à 15 % : 3/4 TPE, 1/4 PME", 0.75)):
    bn = dict(ben)
    bn["TPE"] -= B15 * part_tpe
    bn["PME"] -= B15 * (1 - part_tpe)
    tot = sum(bn.values())
    p(f"[NAIVE qui] {lab} : " + " ; ".join(f"{k} {100*v/tot:.0f} %" for k, v in bn.items())
      + f" (base normale {tot:.1f})")
p("[ACTUEL] part de l'IS brut 2022 : " + " ; ".join(f"{k} {100*v/68.4:.0f} %" for k, v in isb.items())
  + " ; IS brut / bénéfices : " + " ; ".join(f"{k} {100*isb[k]/ben[k]:.1f} %" for k in ben))
p(f"[ACTUEL] IS net 2025 59,9 Md€ = {100*59.9/PIB25:.1f} % du PIB ; contribution exceptionnelle 7,5 Md€ (2025)")
# efficacité comparée à coût actualisé égal (équipements seulement)
va100 = TAU * S * I1 * (1 - zval(PLANS["lin"], .05))
pts_eq = va100 / ((BN22 + B15) * A22_OFF / 100)
z = zval(PLANS["lin"], .05)
m0 = .25 * (1 - z) / .75
m_cut = (.25 - pts_eq / 100) * (1 - z) / (1 - .25 + pts_eq / 100)
p(f"[NAIVE eff] VA de la déduction totale (lin, 5 %) {va100:.2f} Md€ = {pts_eq:.2f} pt de taux ; à ce coût, la "
  f"baisse du taux ramène le coin des équipements de {100*m0:.2f} % à {100*m_cut:.2f} % ; la déduction totale à 0")

# ------------------------------------------------------------------ PIB et triangle
sk = (0.05 + 0.14) * 541 / 2950
sk2 = (0.05 + 0.14) * K25 / PIB25
for nom, dc in (("100 %", (0.034, 0.048)), ("50 %", (0.017, 0.024))):
    p(f"[PIB] {nom} : part {100*sk:.2f} % (avec PIB Insee {100*sk2:.2f} %) ; gain {100*sk*.5*dc[0]*.75:.3f} à "
      f"{100*sk*1.6*dc[1]*.75:.3f} % ; central {100*sk*sum(dc)/2*.75:.3f} %")
KEQ = 0.75 * 541
for nom, m0_, m1_ in (("100 % lin", .051, 0), ("100 % deg", .035, 0), ("50 % lin", .051, .025), ("28 % lin sans déduction", .051, .060)):
    p(f"[TRIANGLE] {nom} : " + " / ".join(f"{0.19*KEQ*e*(m1_**2-m0_**2)/2:+.3f}" for e in (.5, 1, 1.6)))
# 28 % dans le paquet : les équipements sont déduits (coin nul), le coin monte sur les bâtiments non résidentiels
KB = 0.75 * 399.869
zb5 = zval(plan_lin(25), .05)
mb0, mb1 = .25 * (1 - zb5) / .75, .28 * (1 - zb5) / .72
db = 49.19 / 399.869
p(f"[TRIANGLE] 28 % avec déduction des équipements : bâtiments non résidentiels imposables ({KB:.0f} Md€, coin "
  f"{100*mb0:.1f} -> {100*mb1:.1f} %) : " + " / ".join(f"{(0.05+db)*KB*e*(mb1**2-mb0**2)/2:+.3f}" for e in (.5, 1, 1.6)))
for base, lab in ((322.0, "script (322, base totale)"), (BN22 * A22_SCRIPT, "base au taux normal, script"),
                  (BN22 * A22_OFF, "base au taux normal, corrigée")):
    p(f"[KAPPA=1] {lab} : {0.265*0.03*base:.2f} à {0.265*0.045*base:.2f}")

OUT.write_text("\n".join(L) + "\n", encoding="utf-8")
print("\n".join(L))
