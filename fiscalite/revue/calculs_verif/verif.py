"""Recalcul indépendant des chiffres clés de la partie Immobilier (n'importe pas foncier/simulation.py).

Lit les mêmes données (foncier/donnees/), réimplante la méthode décrite dans foncier/README.md, et ajoute des
contrôles : valeurs vs prix moyens DVF, bornes de la part du terrain, compensation par département, délais de
rattrapage actualisés, perte sèche (réforme naïve vs proposition, coin des droits sur le bâti), transition.
Usage : python3 verif.py /home/user/Projets-annexes/fiscalite/foncier/donnees
"""
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

D = Path(sys.argv[1])
out = []


def p(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    out.append(s)


c = pd.read_csv(D / "communes.csv.gz", dtype={"codgeo": str, "dep": str, "epci": str}).set_index("codgeo")
c = c[c.log.fillna(0) > 0].copy()

# ------------------------------------------------------------------ parc des particuliers
part_hlm = (c.rp_lochlmv.fillna(0) / (c.maison + c.appart)).replace([np.inf], np.nan).fillna(0)
nm = (c.maison * (1 - part_hlm)).clip(lower=0).fillna(0)
na = (c.appart * (1 - part_hlm)).clip(lower=0).fillna(0)
vm, va = c.m_pm2 * c.m_surf, c.a_pm2 * c.a_surf
VAL = (nm * vm + na * va).sum()
p(f"[PARC] {(nm+na).sum()/1e6:.2f} M logements ; valeur {VAL/1e9:,.0f} Md€ ; valeur moyenne {VAL/(nm+na).sum():,.0f} €")

# écart aux comptes de patrimoine (Insee Première 2081 : logements 4 807 + terrains bâtis 4 043, ménages S14+S15)
cr = json.loads((D / "croissance_tf.json").read_text())
lm_metro = cr["logements_metro_particuliers"]
for nom, terr in (("terrains 4 043 (publication)", 4043), ("terrains 3 993 (code)", 3993)):
    tot = 4807 + terr
    p(f"[PARC] Insee {nom} : total {tot} Md€ ; part terrain {terr/tot:.3f} ; au prorata champ/métropole "
      f"{tot*(nm+na).sum()/lm_metro:,.0f} Md€ -> modèle = {VAL/1e9/(tot*(nm+na).sum()/lm_metro):.2f}")

# valeur modélisée vs prix moyen des ventes DVF de la commune (par décile de prix)
w_v = c.valeur_ventes_an
ventes = c.ventes_an

# ------------------------------------------------------------------ part du terrain
dep_pm2m = (c.m_pm2 * nm).groupby(c.dep).sum() / nm.groupby(c.dep).sum()
x = np.log(c.m_pm2 / c.dep.map(dep_pm2m))
y = np.log(c.pm2_tab_com / c.pm2_tab_dep)
ok = (c.n_tab_com.fillna(0) >= 5) & (c.m_n.fillna(0) >= 10) & np.isfinite(x) & np.isfinite(y)
A = np.c_[np.ones(ok.sum()), x[ok]]
(a0, b1), *_ = np.linalg.lstsq(A, y[ok], rcond=None)
p(f"[TERRAIN] élasticité prix terrain / prix maisons {b1:.3f} (const {a0:.3f}, {ok.sum()} communes)")
pm2_tab = np.where(c.n_tab_com.fillna(0) >= 5, c.pm2_tab_com, c.pm2_tab_dep * np.exp(a0 + b1 * x.fillna(0)))
lam_m = pd.Series(pm2_tab * c.m_terrain.clip(upper=1500) / vm, index=c.index).clip(0.1, 0.9)
lam_m = lam_m.fillna(c.dep.map(lam_m.groupby(c.dep).median())).fillna(lam_m.median())
CIBLE_L = 3993 / (3993 + 4807)


def part(B):
    la = (1 - B / c.a_pm2).clip(0.1, 0.9)
    return ((nm * vm * lam_m).sum() + (na * va * la).sum()) / VAL


lo, hi = 100.0, 20000.0
for _ in range(80):
    mid = (lo + hi) / 2
    lo, hi = (mid, hi) if part(mid) > CIBLE_L else (lo, mid)
B = (lo + hi) / 2
lam_a = (1 - B / c.a_pm2).clip(0.1, 0.9)
p(f"[TERRAIN] coût calé appartements {B:,.0f} €/m² ; part terrain {part(B):.4f}")
# avec la cible publiée (4 043)
lo2, hi2 = 100.0, 20000.0
for _ in range(80):
    mid = (lo2 + hi2) / 2
    lo2, hi2 = (mid, hi2) if part(mid) > 4043 / 8850 else (lo2, mid)
p(f"[TERRAIN] avec la cible publiée 45,7 % : coût calé {(lo2+hi2)/2:,.0f} €/m²")
# logements aux bornes
nb_lo = (nm * (lam_m <= 0.1001)).sum() + (na * (lam_a <= 0.1001)).sum()
nb_hi = (nm * (lam_m >= 0.8999)).sum() + (na * (lam_a >= 0.8999)).sum()
p(f"[TERRAIN] logements à la borne de 10 % : {nb_lo/1e6:.2f} M ({100*nb_lo/(nm+na).sum():.0f} %) ; à 90 % : "
  f"{nb_hi/1e6:.2f} M ({100*nb_hi/(nm+na).sum():.0f} %)")

# ------------------------------------------------------------------ taxe foncière actuelle
r = c.tf_valeur_2017 / 100
r = r.fillna(c.epci.map(r.groupby(c.epci).median())).fillna(c.dep.map(r.groupby(c.dep).median()))
G = cr["tfpb_2024"] / cr["tfpb_2017"]
part_champ = (nm + na).sum() / lm_metro
CIBLE_TF = 19.2e9 * G * part_champ
t17 = pd.read_csv(D / "tfpb2017_communes.csv", dtype={"codgeo": str}).set_index("codgeo").tfpb_2017
g = (c.tfpb / t17.reindex(c.index)) / G
g = g.where(np.isfinite(g) & (g > 0), 1.0).clip(0.7, 2.0)
kap = CIBLE_TF / (r * g * (nm * vm + na * va)).sum()
tfm, tfa = kap * r * g * vm, kap * r * g * va
TF0 = (nm * tfm + na * tfa).sum()
p(f"[TF] croissance TFPB 2017-2024 {G:.4f} ; part du champ {part_champ:.4f} ; cible {CIBLE_TF/1e9:.2f} Md€ ;"
  f" TF moyenne {TF0/(nm+na).sum():.0f} € ; TF/valeur {100*TF0/VAL:.3f} %")
p(f"[TF] Paris : croissance relative {g.get('75056'):.3f} ; TF/valeur 2017 {100*r.get('75056'):.3f} %")
# sensibilité : si les 19,2 Md€ couvraient la France entière (≈ 33,3 M logements de particuliers, hypothèse)
p(f"[TF] si 19,2 Md€ = France entière : cible ×{lm_metro/33.3e6:.3f} -> {CIBLE_TF*lm_metro/33.3e6/1e9:.1f} Md€")

# ------------------------------------------------------------------ droits de mutation
T = 0.045 + 0.012 + 0.0237 * 0.045
dm = np.where(nm > 0, T * c.valeur_ventes_m_an / nm.replace(0, np.nan), 0)
da = np.where(na > 0, T * c.valeur_ventes_a_an / na.replace(0, np.nan), 0)
dm, da = np.nan_to_num(dm), np.nan_to_num(da)
D0 = (nm * dm + na * da).sum()
V = c.valeur_ventes_an.sum()
p(f"[DMTO] taux {100*T:.3f} % ; ventes {V/1e9:.1f} Md€/an ; {c.ventes_an.sum()/1e3:.0f} k ventes/an ; "
  f"DMTO {D0/1e9:.2f} Md€ (dont part communale {D0*0.012/T/1e9:.2f}, frais État {D0*0.0237*0.045/T/1e9:.2f})")
p(f"[DMTO] rotation : {c.ventes_an.sum()/(nm+na).sum()*100:.2f} % du parc par an ; ventes / valeur du parc "
  f"{100*V/VAL:.2f} %")
# Ventes de logements perdues (hors champ : VEFA, ventes mixtes logement + local) : non contrôlable ici.

for s in (0.3, 0.5):
    for v in (0.0, 0.03, 0.06, 0.08):
        pts = 100 * s * T
        cout = D0 * (1 - (1 - s) * (1 + v) ** pts)
        p(f"[COUT] baisse {int(100*s)} % ({pts:.2f} pt), +{int(100*v)} %/pt : perte {cout/1e9:.2f} Md€ ; TF +{100*cout/TF0:.1f} %")

# ------------------------------------------------------------------ table longue
L = pd.concat([pd.DataFrame({"codgeo": c.index, "dep": c.dep, "t": t, "n": n, "v": v_, "lam": l_, "tf0": tf_,
                             "d0": d_, "pm2": pm_, "pmen": c.pmen})
               for t, n, v_, l_, tf_, d_, pm_ in (("m", nm, vm, lam_m, tfm, dm, c.m_pm2),
                                                  ("a", na, va, lam_a, tfa, da, c.a_pm2))], ignore_index=True)
L = L[L.n > 0].reset_index(drop=True)
o = L.sort_values("pm2", kind="mergesort")
cum = o.n.cumsum() / o.n.sum()
L.loc[o.index, "dec"] = np.minimum((cum * 10).astype(int), 9)
L["dec"] = L.dec.astype(int)
W = L.n
TERRE = (W * L.v * L.lam).sum()
p(f"[LONG] terrain {TERRE/1e9:,.0f} Md€ ({100*TERRE/VAL:.1f} %) ; taille des déciles (% des logements) : "
  + " ".join(f"{100*u:.1f}" for u in W.groupby(L.dec).sum() / W.sum()))
paris = (L.codgeo == "75056")
p(f"[LONG] Paris : {W[paris].sum()/1e6:.2f} M logements, {100*W[paris].sum()/W[L.dec == 9].sum():.0f} % du dernier décile")

# ------------------------------------------------------------------ scénarios
s = 0.5
d1 = (1 - s) * L.d0
# R50 : TF actuelle relevée uniformément
R50 = L.tf0 * (1 + s * D0 / TF0)


def local_base(k):
    return L.v * (L.lam * k + (1 - L.lam))


def N(k, perte):
    b = local_base(k)
    tc = (W * L.tf0).groupby(L.codgeo).sum() / (W * b).groupby(L.codgeo).sum()
    tn = perte / TERRE
    return L.codgeo.map(tc) * b + tn * L.v * L.lam, tn, L.codgeo.map(tc)


N4, tn4, N4com = N(4, s * D0)
cout6 = D0 * (1 - (1 - s) * 1.06 ** (100 * s * T))
N4v, tn4v, _ = N(4, cout6)
# K4 national
bK = L.v * (4 * L.lam + 1 - L.lam)
tK = (TF0 + s * D0) / (W * bK).sum()
K4 = tK * bK
p(f"[TAUX] national sur le terrain : {100*tn4:.4f} % (sans reprise), {100*tn4v:.4f} % (avec) ; K4 terrain {100*4*tK:.3f} %,"
  f" bâti {100*tK:.3f} %")
# taux sur des valeurs « niveau Insee » : assiette ×1/ratio
ratio = VAL / 1e9 / ((4807 + 4043) * (nm + na).sum() / lm_metro)
p(f"[TAUX] avec des valeurs au niveau des comptes de patrimoine (×{1/ratio:.2f}) : {100*tn4*ratio:.3f} % / {100*tn4v*ratio:.3f} %")


def resume(nom, tf1):
    dtf = tf1 - L.tf0
    g_ = L.assign(a=W * dtf, b=W * (dtf + d1 - L.d0), t0=W * L.tf0).groupby("dec")
    pct = 100 * g_.a.sum() / g_.t0.sum()
    eur = g_.a.sum() / W.groupby(L.dec).sum()
    tot = g_.b.sum() / W.groupby(L.dec).sum()
    p(f"[{nom}] TF {(W*tf1).sum()/1e9:.2f} Md€ ; ΔTF % par décile : " + " ".join(f"{u:+.0f}" for u in pct))
    p(f"[{nom}] ΔTF €/an par décile : " + " ".join(f"{u:+.0f}" for u in eur) + " ; total TF+DMTO : "
      + " ".join(f"{u:+.0f}" for u in tot))
    n = W.sum()
    p(f"[{nom}] logements ΔTF > 300 € : {100*W[dtf > 300].sum()/n:.1f} % ; > +50 % : {100*W[dtf > 0.5*L.tf0].sum()/n:.1f} % ;"
      f" > +100 % : {100*W[dtf > L.tf0].sum()/n:.1f} % ; baisse > 100 € : {100*W[dtf < -100].sum()/n:.1f} %")
    dbl = dtf > L.tf0
    if W[dbl].sum() > 0:
        p(f"[{nom}] parmi les TF qui doublent : Paris {100*W[dbl & paris].sum()/W[dbl].sum():.0f} %, Hauts-de-Seine "
          f"{100*W[dbl & (L.dep == '92')].sum()/W[dbl].sum():.0f} %")
    p(f"[{nom}] Paris ΔTF {100*(W*dtf)[paris].sum()/(W*L.tf0)[paris].sum():+.0f} % ({(W*dtf)[paris].sum()/W[paris].sum():+.0f} €) ;"
      f" dernier décile hors Paris {100*(W*dtf)[(L.dec == 9) & ~paris].sum()/(W*L.tf0)[(L.dec == 9) & ~paris].sum():+.0f} %")
    return dtf


p(f"[AUJ] TF/valeur par décile : " + " ".join(f"{100*u:.2f}" for u in (W*L.tf0).groupby(L.dec).sum()/(W*L.v).groupby(L.dec).sum())
  + f" ; Paris {100*(W*L.tf0)[paris].sum()/(W*L.v)[paris].sum():.3f} %")
resume("R50", R50)
resume("K4", K4)
dN4 = resume("N4", N4)
p(f"[N4] TF/valeur par décile : " + " ".join(f"{100*u:.2f}" for u in (W*N4).groupby(L.dec).sum()/(W*L.v).groupby(L.dec).sum()))
# percentiles des hausses (€/an) pondérés par logement
oo = dN4.sort_values()
cw = W[oo.index].cumsum() / W.sum()
p("[N4] distribution ΔTF €/an (pondérée) : " + " ; ".join(f"P{q} {oo[cw >= q/100].iloc[0]:+.0f}" for q in (10, 25, 50, 75, 90, 95, 99)))

# ------------------------------------------------------------------ bâti et perte sèche
bati0 = (W * L.tf0 * (1 - L.lam)).sum()
bati_N4 = (W * N4com * L.v * (1 - L.lam)).sum()
K = ((W * L.v * (1 - L.lam)).sum())
p(f"[BATI] TF sur le bâti {bati0/1e9:.2f} -> {bati_N4/1e9:.2f} Md€ (N4) ; R50 {bati0*(1+s*D0/TF0)/1e9:.2f} ; K = {K/1e9:,.0f} Md€")
u = 0.045
Kb = K / 1e9
Vb = V / 1e9


def tri_v(t1, sig, t0=T):
    return sig * Vb * (t1 ** 2 - t0 ** 2) / 2


def tri_k(b1, b0=bati0 / 1e9, eps=1.0, uu=u, extra0=0.0, extra1=0.0):
    t0_, t1_ = b0 / Kb + extra0, b1 / Kb + extra1
    return eps * (Kb / uu) * (t1_ ** 2 - t0_ ** 2) / 2


for sig in (3, 6, 8, 15):
    p(f"[PS] droits −50 %, σ = {sig} : {tri_v(T/2, sig):+.2f} Md€ ; −30 % : {tri_v(0.7*T, sig):+.2f}")
# intégrale exacte avec réaction multiplicative (comme cout_baisse) : ∫ t σ Q(t) dt, Q(t) = V e^{σ(t0-t)}
tt = np.linspace(T / 2, T, 2001)
Q = Vb * np.exp(6 * (T - tt))
p(f"[PS] droits −50 %, σ = 6, volume au niveau réformé (intégrale) : {-np.trapezoid(6 * tt * Q, tt):+.2f} Md€")
p(f"[PS] bâti N4 (ε=1, u=4,5 %) : {tri_k(bati_N4/1e9):+.2f} ; ε=0,5 {tri_k(bati_N4/1e9, eps=0.5):+.2f} ; u=3,5 % "
  f"{tri_k(bati_N4/1e9, uu=0.035):+.2f} ; u=6 % {tri_k(bati_N4/1e9, uu=0.06):+.2f}")
for k in (2, 4, np.inf):
    if np.isfinite(k):
        bK_ = L.v * (k * L.lam + 1 - L.lam)
        tK_ = (TF0 + s * D0) / (W * bK_).sum()
        bat = tK_ * K
        bl = local_base(k)
        tc = (W * L.tf0).groupby(L.codgeo).sum() / (W * bl).groupby(L.codgeo).sum()
        bat_loc = (W * L.codgeo.map(tc) * L.v * (1 - L.lam)).sum()
    else:
        bat, bat_loc = 0.0, 0.0
    p(f"[PS] bâti, terrain = {k} × bâti : national {bat/1e9:.2f} Md€ -> {tri_k(bat/1e9):+.2f} ; par commune "
      f"{bat_loc/1e9:.2f} Md€ -> {tri_k(bat_loc/1e9):+.2f}")
r50_bati = bati0 * (1 + s * D0 / TF0) / 1e9
p(f"[PS] réforme naïve R50 : bâti {tri_k(r50_bati):+.2f} ; total σ=6 {tri_v(T/2, 6) + tri_k(r50_bati):+.2f} Md€ ; "
  f"proposition N4 total {tri_v(T/2, 6) + tri_k(bati_N4/1e9):+.2f} Md€")
# coin des droits sur le bâti : droits annuels rapportés à la valeur (rotation × taux)
dmto_coin = D0 / VAL
p(f"[PS] coin des droits sur le capital : {100*dmto_coin:.3f} % de la valeur par an ; avec ce coin (bâti) : N4 "
  f"{tri_k(bati_N4/1e9, extra0=dmto_coin, extra1=dmto_coin/2):+.2f} ; R50 {tri_k(r50_bati, extra0=dmto_coin, extra1=dmto_coin/2):+.2f}")

# ------------------------------------------------------------------ délais de rattrapage actualisés
R = 0.03
CAS = [("75056", "a", "Paris"), ("69123", "a", "Lyon"), ("33063", "a", "Bordeaux"), ("74010", "m", "Annecy"),
       ("44109", "m", "Nantes"), ("87085", "m", "Limoges"), ("42218", "a", "Saint-Étienne"), ("19272", "m", "Ussel"),
       ("23096", "m", "Guéret"), ("33009", "m", "Arcachon")]
for code, t, lab in CAS:
    i = L[(L.codgeo == code) & (L.t == t)].index[0]
    eco = s * T * L.v[i]
    for nom, tf1 in (("R50", R50), ("N4", N4)):
        dt = tf1[i] - L.tf0[i]
        if dt <= 0:
            n_ = "TF en baisse"
        elif R * eco >= dt:
            n_ = "jamais"
        else:
            n_ = f"{-np.log(1 - R*eco/dt)/np.log(1+R):.0f} ans (simple {eco/dt:.0f})"
        p(f"[PRIMO] {lab} {t} {nom} : valeur {L.v[i]:,.0f} ; économie {eco:,.0f} ; TF {L.tf0[i]:,.0f} -> {tf1[i]:,.0f}"
          f" ({dt:+,.0f}) ; rattrapage {n_} ; VA perpétuelle {dt/R:,.0f}")

# ------------------------------------------------------------------ compensation des collectivités
part_dep = (0.045) / T
part_com = 0.012 / T
part_etat = 0.0237 * 0.045 / T
perte = L.assign(x=W * L.d0 * s).groupby("dep").x.sum()
paye = L.assign(x=W * tn4 * L.v * L.lam).groupby("dep").x.sum()
for d_, lab in (("75", "Paris"), ("92", "Hauts-de-Seine"), ("93", "Seine-Saint-Denis"), ("23", "Creuse")):
    p(f"[COMP] {lab} : paie {paye[d_]/1e6:,.0f} M€ ; perd {perte[d_]/1e6:,.0f} M€ (dép. {part_dep*perte[d_]/1e6:,.0f},"
      f" com. {part_com*perte[d_]/1e6:,.0f}) ; net / perte totale {(paye[d_]-perte[d_])/1e6:+,.0f} ; net / part dép."
      f" {(paye[d_]-part_dep*perte[d_])/1e6:+,.0f} M€")
p(f"[COMP] perte totale {perte.sum()/1e9:.2f} Md€ : dép. {part_dep*perte.sum()/1e9:.2f}, com. {part_com*perte.sum()/1e9:.2f},"
  f" État {part_etat*perte.sum()/1e9:.2f}")
net = (paye - part_dep * perte)
p(f"[COMP] départements contributeurs nets (part dép.) : {(net > 0).sum()} ; somme des excédents {net[net > 0].sum()/1e6:,.0f} M€")

# ------------------------------------------------------------------ cohérence valeur modélisée / prix moyen DVF
c["v_mod"] = (nm * vm + na * va) / (nm + na)
c["p_moy"] = c.valeur_ventes_an / c.ventes_an.replace(0, np.nan)
pm2c = (nm * c.m_pm2 + na * c.a_pm2) / (nm + na)
cc = c[(c.ventes_an >= 20)].copy()
cc["dec"] = pd.qcut(pm2c[cc.index].rank(method="first"), 10, labels=False)
rr = cc.groupby("dec").apply(lambda g: (g.p_moy * g.ventes_an).sum() / (g.v_mod * g.ventes_an).sum(), include_groups=False)
p("[VALEUR] prix moyen des ventes / valeur modélisée, par décile de communes (≥ 20 ventes) : "
  + " ".join(f"{u:.2f}" for u in rr))

# ------------------------------------------------------------------ qui paie aujourd'hui : statut d'occupation, taille
st = pd.DataFrame({"prop": c.rp_prop, "loc_priv": (c.rp_loc - c.rp_lochlmv).clip(lower=0), "grat": c.rp_grat,
                   "sec": c.rsecocc, "vac": c.logvac})
tot_ = st.sum(axis=1).replace(0, np.nan)
tfc = nm * tfm + na * tfa
dmc = nm * dm + na * da
p("[QUI] TF par statut (prorata communal, logements des particuliers ≈ parc − HLM loués) : " + " ; ".join(
    f"{k} {(tfc * st[k] / tot_).sum()/1e9:.1f} Md€ ({100*(tfc*st[k]/tot_).sum()/tfc.sum():.0f} %)" for k in st))
taille = pd.cut(c.pmen.fillna(0), [-1, 1000, 5000, 20000, 100000, 1e9], labels=["<1k", "1-5k", "5-20k", "20-100k", ">100k"])
gq = pd.DataFrame({"n": nm + na, "tf": tfc, "dm": dmc, "v": nm * vm + na * va, "t": taille}).groupby("t", observed=True).sum()
p("[QUI] par taille de commune : " + " ; ".join(f"{i} TF {r_.tf/r_.n:,.0f} €/log, TF/valeur {100*r_.tf/r_.v:.2f} %, DMTO/an "
                                                 f"{r_.dm/r_.n:,.0f} €/log" for i, r_ in gq.iterrows()))

# ------------------------------------------------------------------ transition
nat = tn4 * L.v * L.lam                       # taxe nationale sur le terrain, par logement
red = N4com * local_base(4) - L.tf0           # redistribution communale (somme nulle par commune)
surc = L.tf0 * s * D0 / TF0                   # surtaxe uniforme temporaire (R50)
pa = (L.codgeo == "75056") & (L.t == "a")
p(f"[TRANS] Paris appartement médian : taxe nationale {float(nat[pa].iloc[0]):+,.0f} € ; redistribution communale "
  f"{float(red[pa].iloc[0]):+,.0f} € ; surtaxe transitoire R50 {float(surc[pa].iloc[0]):+,.0f} €")
top = dN4 > dN4[W.index].quantile(0.9)
for lab, msk in (("hausses > 300 €", dN4 > 300), ("TF qui doublent", dN4 > L.tf0)):
    p(f"[TRANS] {lab} : part de la hausse venant de la taxe nationale {100*(W*nat)[msk].sum()/(W*dN4)[msk].sum():.0f} %")
# saut de la 1re année de la nouvelle assiette (taux national plein + 1/n de la redistribution) après la surtaxe
for nans in (1, 3, 5, 10):
    saut = nat + red / nans - surc
    oo = saut.sort_values(); cw = W[oo.index].cumsum() / W.sum()
    p(f"[TRANS] calendrier de la note (taux national plein, redistribution sur {nans} an(s)) : saut de la 1re année après la"
      f" surtaxe : P50 {oo[cw >= .5].iloc[0]:+,.0f} €, P90 {oo[cw >= .9].iloc[0]:+,.0f} €, P99 {oo[cw >= .99].iloc[0]:+,.0f} € ;"
      f" Paris {float(saut[pa].iloc[0]):+,.0f} € ; logements à plus de +300 € : {100*W[saut > 300].sum()/W.sum():.1f} %")
for nans in (3, 5, 10):
    pas = dN4.clip(lower=0) / nans
    oo = pas.sort_values()
    cw = W[oo.index].cumsum() / W.sum()
    p(f"[TRANS] {nans} ans : hausse annuelle P90 {oo[cw >= .9].iloc[0]:,.0f} €, P99 {oo[cw >= .99].iloc[0]:,.0f} € ; Paris médian "
      f"{float(pas[(L.codgeo == '75056') & (L.t == 'a')].iloc[0]):,.0f} €/an ; déficit cumulé si droits baissés d'emblée et taux"
      f" national monté linéairement : {s*D0/1e9*(nans-1)/2:.1f} Md€")

Path(__file__).with_suffix(".txt").write_text("\n".join(out) + "\n", encoding="utf-8")

# ------------------------------------------------------------------ vieillissement : ratio 2017 appliqué aux valeurs 2024
# Le modèle prend TF ∝ r2017 × v2024 × g_TF,rel ; le bon vieillissement est r2017 × v2017 × g_TF,rel. L'écart est la
# croissance relative des prix 2017 -> 2023-2024. Correction grossière à trois zones (indices Notaires-Insee, séries
# brutes 010567012, 010567058, 010567072, 010567088 : Paris appartements 1,113 ; métropole 1,239 ; province 1,281 ;
# Île-de-France hors Paris 1,134).
zone = np.where(L.codgeo == "75056", 1.113, np.where(L.dep.isin(["77", "78", "91", "92", "93", "94", "95"]), 1.134, 1.281))
tf0b = L.tf0 / zone
tf0b = tf0b * TF0 / (W * tf0b).sum()
bb = local_base(4)
tcb = (W * tf0b).groupby(L.codgeo).sum() / (W * bb).groupby(L.codgeo).sum()
N4b = L.codgeo.map(tcb) * bb + tn4 * L.v * L.lam
dtfb = N4b - tf0b
g_ = L.assign(a=W * dtfb, t0=W * tf0b).groupby("dec")
p("[VIEIL] TF actuelle corrigée (3 zones) : Paris TF/valeur "
  f"{100*(W*tf0b)[paris].sum()/(W*L.v)[paris].sum():.3f} % ; ΔTF % par décile : "
  + " ".join(f"{u:+.0f}" for u in 100 * g_.a.sum() / g_.t0.sum())
  + f" ; Paris {100*(W*dtfb)[paris].sum()/(W*tf0b)[paris].sum():+.0f} % ; TF qui doublent "
  f"{100*W[dtfb > tf0b].sum()/W.sum():.1f} % ; hausses > 300 € {100*W[dtfb > 300].sum()/W.sum():.1f} %")
Path(__file__).with_suffix(".txt").write_text("\n".join(out) + "\n", encoding="utf-8")

# plus fortes hausses (cellules d'au moins 1 000 logements)
noms = pd.read_csv(D / "communes.csv.gz", usecols=["codgeo", "nom"], dtype={"codgeo": str}).set_index("codgeo").nom
T_ = L.assign(dtf=dN4, pct=100 * dN4 / L.tf0, nat=nat, nom=L.codgeo.map(noms))
big = T_[T_.n >= 1000].sort_values("dtf", ascending=False).head(8)
p("[TOP] plus fortes hausses €/an (cellules ≥ 1 000 logements) : " + " ; ".join(
    f"{r.nom} {r.t} {r.dtf:+,.0f} € ({r.pct:+.0f} %, dont national {r.nat:,.0f})" for _, r in big.iterrows()))
p(f"[TOP] logements à plus de +500 €/an : {100*W[dN4 > 500].sum()/W.sum():.1f} % ; à plus de +1 000 €/an : "
  f"{100*W[dN4 > 1000].sum()/W.sum():.2f} %")
Path(__file__).with_suffix(".txt").write_text("\n".join(out) + "\n", encoding="utf-8")
netT = paye - perte
p(f"[COMP] taux plein 0,185 % : départements qui paient plus qu'ils ne perdent (perte totale) : {(netT > 0).sum()} ; "
  f"transfert entre départements {netT[netT > 0].sum()/1e6:,.0f} M€ ; Paris paie {100*paye['75']/paye.sum():.0f} % du taux national "
  f"pour {100*W[paris].sum()/W.sum():.1f} % des logements ; Paris + Hauts-de-Seine {100*(paye['75']+paye['92'])/paye.sum():.0f} %")
Path(__file__).with_suffix(".txt").write_text("\n".join(out) + "\n", encoding="utf-8")
