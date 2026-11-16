"""Vérifications sur une copie du modèle (scratchpad). Lancer depuis verif_foncier/."""
import numpy as np
import pandas as pd
import simulation as sm

L, c = sm.L, sm.c
n = L.n
print("=== agrégats")
print("N logements", n.sum() / 1e6, "M ; VAL", sm.VAL / 1e9, "Md ; TERRE", sm.TERRE / 1e9, "Md ; part", sm.TERRE / sm.VAL)
print("valeur moyenne par logement", sm.VAL / n.sum(), "; terrain moyen", sm.TERRE / n.sum())
print("TF0", sm.TF0 / 1e9, "D0", sm.D0 / 1e9, "TF moy", sm.TF0 / n.sum(), "DMTO moy/logement/an", sm.D0 / n.sum())
print("CIBLE_TF", sm.CIBLE_TF / 1e9, "= 19.2 x", sm.CROISSANCE_TF, "x", sm.part_champ, "; KAPPA", sm.KAPPA)
print("TAUX_DMTO", sm.TAUX_DMTO, "PART_DEP_DMTO", sm.PART_DEP_DMTO, "LAMBDA", sm.LAMBDA_MENAGES, "B_APPART", sm.B_APPART)
cc = c[c.log.fillna(0) > 0]
print("ventes/an (DVF, champ)", cc.ventes_an.sum(), "; valeur ventes/an", cc.valeur_ventes_an.sum() / 1e9, "Md ; prix moyen",
      cc.valeur_ventes_an.sum() / cc.ventes_an.sum())
print("DMTO = taux x valeur ventes", sm.TAUX_DMTO * cc.valeur_ventes_an.sum() / 1e9,
      "; somme m+a", sm.TAUX_DMTO * (cc.valeur_ventes_m_an.sum() + cc.valeur_ventes_a_an.sum()) / 1e9)
print("taux de rotation ventes / parc", cc.ventes_an.sum() / n.sum())
print("parc total (log) champ", cc.log.sum() / 1e6, "maison+appart", (cc.maison + cc.appart).sum() / 1e6, "HLM", cc.rp_lochlmv.sum() / 1e6)
print("valeur par type", (L.n * L.v).groupby(L.type).sum() / 1e9, (L.n).groupby(L.type).sum() / 1e6)

print("=== Paris et 92")
for code in ("75056",):
    m = L.codgeo == code
    print(code, "n", n[m].sum(), "TF0/val", (n * L.tf0)[m].sum() / (n * L.v)[m].sum(),
          "TF0", (n * L.tf0)[m].sum() / 1e6, "M ; val", (n * L.v)[m].sum() / 1e9)
    print("  g_rel Paris", c.loc[code, "g_rel"], "r2017", c.loc[code, "r2017"])
w = n * L.v
for dep in ("75", "92"):
    m = L.dep == dep
    print(dep, "TF0/val", (n * L.tf0)[m].sum() / w[m].sum())

print("=== taux national et contributions nettes par département (N4)")
tn = 0.5 * sm.D0 / sm.TERRE
g = L.assign(terre=n * L.v * L.lam, d=n * L.d0).groupby("dep")
net = (tn * g.terre.sum() - 0.5 * g.d.sum()) / 1e6
print("tn", tn)
print(net.sort_values(ascending=False).head(12).round(0).to_string())
print("somme des contributions positives", net[net > 0].sum(), "M€ ; négatives", net[net < 0].sum())
print("Paris", net.get("75"), "92", net.get("92"))
# avec la variante volumes
c_vol, _ = sm.cout_baisse(0.5)
tnv = c_vol * 1e9 / sm.TERRE
netv = (tnv * g.terre.sum() - (c_vol * 1e9 / sm.D0) * g.d.sum()) / 1e6
print("avec volumes : Paris", netv.get("75"), "92", netv.get("92"))
# part départementale seule
netdep = (tn * sm.PART_DEP_DMTO * g.terre.sum() - 0.5 * sm.PART_DEP_DMTO * g.d.sum()) / 1e6
print("si seule la part départementale compensée : Paris", netdep.get("75"), "92", netdep.get("92"))
print("perte part départementale+frais", 0.5 * sm.D0 * sm.PART_DEP_DMTO / 1e9, "communale", 0.5 * sm.D0 * (1 - sm.PART_DEP_DMTO) / 1e9)

print("=== scénarios")
scen = {"R50": sm.report_tf(0.5), "K4": sm.deux_taux(0.5, 4), "N4": sm.deux_taux_local_national(0.5, 4)}
for k, (tf1, d1) in scen.items():
    dtf = tf1 - L.tf0
    tot = dtf + d1 - L.d0
    gg = L.assign(a=n * dtf, b=n * tot).groupby("dec_prix")
    print(k, "TF1", (n * tf1).sum() / 1e9, "dTF dec", (gg.a.sum() / gg.n.sum()).round(0).tolist())
    print("   total dec", (gg.b.sum() / gg.n.sum()).round(0).tolist(), "min", (gg.b.sum() / gg.n.sum()).min())
print("K4 taux", sm.TAUX[4], "recette", sm.TAUX[4][0] * sm.TERRE / 1e9 + sm.TAUX[4][1] * (sm.VAL - sm.TERRE) / 1e9)

tf1, d1 = scen["N4"]
dtf = tf1 - L.tf0
dec9 = L.dec_prix == 9
paris = (L.codgeo == "75056")
print("décile 9 : n", n[dec9].sum() / 1e6, "dont Paris", n[dec9 & paris].sum() / 1e6)
print("décile 9 hors Paris : dTF %", 100 * (n * dtf)[dec9 & ~paris].sum() / (n * L.tf0)[dec9 & ~paris].sum(),
      "€", (n * dtf)[dec9 & ~paris].sum() / n[dec9 & ~paris].sum())
print("décile 9 Paris : dTF %", 100 * (n * dtf)[dec9 & paris].sum() / (n * L.tf0)[dec9 & paris].sum())
dbl = dtf > L.tf0
print("TF plus que doublée : part", n[dbl].sum() / n.sum(), "dont Paris", n[dbl & paris].sum() / n[dbl].sum())
top = L[dbl].assign(nn=n[dbl]).groupby("codgeo").nn.sum().sort_values(ascending=False).head(15)
print(top.to_string())
print(c.loc[top.index, "nom"].to_string())
print("hausse > 300 € : part", n[dtf > 300].sum() / n.sum(), "dont Paris", n[(dtf > 300) & paris].sum() / n[dtf > 300].sum())

print("=== durée d'amortissement, actualisée à 3 %")
for code, t, lab in sm.CAS:
    i = L[(L.codgeo == code) & (L.type == t)].index[0]
    eco = sm.TAUX_DMTO * L.v[i] * 0.5
    dt = dtf[i]
    simple = eco / dt if dt > 0 else np.nan
    r = 0.03
    if dt <= 0:
        act = "jamais de perte"
    elif eco * r / dt >= 1:
        act = "jamais (valeur perpétuelle {:,.0f} < économie)".format(dt / r)
    else:
        act = "{:.1f} ans".format(-np.log(1 - eco * r / dt) / np.log(1 + r))
    print(f"{lab}: v {L.v[i]:,.0f} eco {eco:,.0f} dTF {dt:,.0f} simple {simple:.1f} actualisé {act}")

print("=== divers")
print("gain efficacité 5,7 x 0,3-0,9", 5.7 * 0.3, 5.7 * 0.9, "% PIB", 100 * 5.7 * 0.3 / 2935, 100 * 5.7 * 0.9 / 2935)
print("4,6 x 0,3-0,9", 4.6 * 0.3, 4.6 * 0.9)
print("apport", 2.905 / 20, 2.905 / 10)
for s_ in (0.3, 0.5):
    for vol in (0, .03, .06, .08):
        print(s_, vol, sm.cout_baisse(s_, vol))
print("bati", (n * L.tf0 * (1 - L.lam)).sum() / 1e9)
print("hausse TF nécessaire", 0.5 * sm.D0 / sm.TF0, sm.cout_baisse(0.5)[0] * 1e9 / sm.TF0)
