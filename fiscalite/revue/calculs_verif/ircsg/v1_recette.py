"""Vérification indépendante de la recette de 220 Md€ (IR + CSG + CRDS des revenus au barème), depuis le CSV IRCOM,
sans importer le modèle. Paramètres recopiés de ir_csg/ir_csg.py (ce sont des hypothèses du modèle, contrôlées ici
pour l'arithmétique et les ordres de grandeur)."""
import numpy as np, pandas as pd, sys
R = "/home/user/Projets-annexes/fiscalite/"
x = pd.read_csv(R + "donnees/ircom_national_revenus2024.csv")
for c in x.columns[1:]:
    x[c] = pd.to_numeric(x[c], errors="coerce")
rfr, ir = x.rfr_keur / 1e6, x.impot_net_keur / 1e6
sal_i, pen_i = x.salaires_keur / 1e6, x.pensions_keur / 1e6
print(f"IRCOM : foyers {x.foyers.sum()/1e6:.2f} M ; RFR {rfr.sum():.1f} ; IR net {ir.sum():.2f} ; salaires {sal_i.sum():.1f} ; pensions {pen_i.sum():.1f} Md€")
TOT = 925.4
sal, ger, cho = 823.9 / TOT * sal_i, 30.7 / TOT * sal_i, 37.0 / TOT * sal_i
pen = 383.9 / 391.5 * pen_i
autres = (rfr - 0.9 * (sal_i + pen_i)).clip(lower=0)
pro = 90.0 * autres / autres.sum()
haut = np.zeros(len(x)); reste = 90.0
for i in reversed(range(len(x))):
    haut[i] = min(0.9 * autres.iloc[i], reste); reste -= haut[i]
cap = 0.5 * (pro + haut)
ind = autres - cap
print(f"autres revenus {autres.sum():.1f} ; dont PFU 90 ; au barème (indépendants, foncier) {ind.sum():.1f}")
ir_aut = np.minimum(0.128 * cap, ir.clip(lower=0))
ir_trav = ir - ir_aut
print(f"IR imputé au PFU {ir_aut.sum():.2f} ; IR des revenus au barème {ir_trav.sum():.2f} Md€")
# CSG des pensions : taux par tranche selon le RFR moyen et un nombre de parts calé sur 25,4 Md€
moy = rfr * 1e9 / x.foyers
S1 = [(12817, 0.0), (16755, 0.038), (26004, 0.066), (np.inf, 0.083)]
def tp(v, parts):
    for s, t in S1:
        if v <= s * parts:
            return t
lo, hi = 0.8, 3.0
for _ in range(60):
    mm = (lo + hi) / 2
    r = sum(1.055 * p * tp(v, mm) for p, v in zip(pen, moy))
    lo, hi = (mm, hi) if r > 25.4 else (lo, mm)
parts = (lo + hi) / 2
t_p = np.array([tp(v, parts) for v in moy])
t_cho = 0.561 / (1.04 * cho.sum())
csg_act = 0.092 * (1.20 * sal + 1.35 * ger + 1.15 * ind)
csg = csg_act + t_cho * 1.04 * cho + t_p * 1.055 * pen
crds = 0.005 * (1.20 * sal + 1.35 * ger + 1.15 * ind) + 0.005 * 1.055 * pen * (t_p > 0) + (0.5 / 6.2) * 0.561 * cho / cho.sum()
print(f"parts calées {parts:.3f} ; CSG {csg.sum():.2f} (activité {csg_act.sum():.2f}, dont salaires {(0.092*1.2*sal).sum():.2f} ; pensions {(t_p*1.055*pen).sum():.2f} ; chômage 0,56) ; CRDS {crds.sum():.2f}")
print(f"TOTAL IR + CSG + CRDS = {ir_trav.sum() + csg.sum() + crds.sum():.2f} Md€")
# assiettes
brut = 1.20 * sal + 1.35 * ger + 1.04 * cho + 1.055 * pen + 1.15 * ind
net = 1.082 * sal + 1.09 * ger + 1.0 * cho + 1.055 * pen + 1.06 * ind
print(f"assiette brute {brut.sum():.1f} ; nette (après cotisations) {net.sum():.1f} ; salaires bruts {(1.2*sal).sum():.1f} ; pensions {(1.055*pen).sum():.1f} ; chômage net {cho.sum():.1f} ; indép.+foncier net {(1.06*ind).sum():.1f}")
print(f"taux moyen actuel sur l'assiette nette {100*(ir_trav.sum()+csg.sum()+crds.sum())/net.sum():.1f} %")
# variantes de convention
for nom, c in (("prorata", pro), ("haut", haut)):
    ia = np.minimum(0.128 * c, ir.clip(lower=0)); i2 = autres - c
    cs = 0.092 * (1.20 * sal + 1.35 * ger + 1.15 * i2) + t_cho * 1.04 * cho + t_p * 1.055 * pen
    cr = 0.005 * (1.20 * sal + 1.35 * ger + 1.15 * i2) + 0.005 * 1.055 * pen * (t_p > 0) + (0.5 / 6.2) * 0.561 * cho / cho.sum()
    print(f"  convention {nom} : IR barème {(ir-ia).sum():.2f} ; total {(ir-ia).sum()+cs.sum()+cr.sum():.2f}")
# IR au prorata du RFR (SPLIT=prorata)
ia = (ir.clip(lower=0) * cap / rfr)
print(f"  partage de l'IR au prorata du RFR : IR imputé au PFU {ia.sum():.2f}, IR barème {(ir-ia).sum():.2f}")
# tranches du haut : taux actuel attribué
k = x.tranche.str.contains("Plus de 9") | x.tranche.str.startswith("3 000") 
for i in range(len(x) - 9, len(x)):
    print(f"   {x.tranche[i]:<25} PFU {cap[i]:.2f} ({100*cap[i]/autres[i]:.0f} % des autres) ; IR/RFR {100*ir[i]/rfr[i]:.1f} % ; IR barème / (sal+ind) {100*ir_trav[i]/(sal_i[i]+pen_i[i]+ind[i]):.1f} %")
