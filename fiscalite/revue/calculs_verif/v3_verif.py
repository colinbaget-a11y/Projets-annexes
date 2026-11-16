import numpy as np
import simulation as sm

L, c = sm.L, sm.c
n = L.n
tf1, d1 = sm.deux_taux_local_national(0.5, 4)
dtf = tf1 - L.tf0
dbl = dtf > L.tf0
tot = n[dbl].sum()
print("doublement : total", tot, "Paris", n[dbl & (L.dep == "75")].sum() / tot, "92", n[dbl & (L.dep == "92")].sum() / tot,
      "autres", n[dbl & ~L.dep.isin(["75", "92"])].sum() / tot)
autres = L[dbl & ~L.dep.isin(["75", "92"])].assign(nn=n).groupby("dep").nn.sum().sort_values(ascending=False)
print(autres.head(10).to_string())
# Paris : hausse moyenne
p = L.codgeo == "75056"
print("Paris : TF0 moy", (n * L.tf0)[p].sum() / n[p].sum(), "dTF moy", (n * dtf)[p].sum() / n[p].sum(), "%",
      100 * (n * dtf)[p].sum() / (n * L.tf0)[p].sum())
# taux national si la valeur des terrains était celle des comptes de patrimoine (ordre de grandeur)
terre_insee = 4043e9 * 30.46 / 33.2
print("terre champ au prorata Insee", terre_insee / 1e9, "taux", 100 * 0.5 * sm.D0 / terre_insee)
val_insee = 8850e9 * 30.46 / 33.2
print("valeur champ au prorata Insee", val_insee / 1e9, "ratio modèle/Insee", sm.VAL / val_insee, "TF/val", 100 * sm.TF0 / val_insee)
# DMTO par logement et par an, Paris appartements
i = L[(L.codgeo == "75056") & (L.type == "a")].index[0]
print("Paris appart d0", L.d0[i], "lam", L.lam[i], "rotation implicite", L.d0[i] / (sm.TAUX_DMTO * L.v[i]))
print("controle 8252", (dtf[i] - 0.5 * L.d0[i]) / 0.03, "part valeur", (dtf[i] - 0.5 * L.d0[i]) / 0.03 / L.v[i])
# N4v : biais sur le total
c_vol, dp = sm.cout_baisse(0.5)
mult = (1.06) ** dp
print("N4v : DMTO réel après baisse", 0.5 * mult, "x D0 ; écart non compté", (0.5 * mult - 0.5) * sm.D0 / 1e9, "Md€ ;",
      (0.5 * mult - 0.5) * sm.D0 / n.sum(), "€/logement")
# DMTO par logement moyen par décile (pour lecture des totaux)
g = L.assign(a=n * L.d0).groupby("dec_prix")
print("DMTO/logement/an par décile", (g.a.sum() / g.n.sum()).round(0).tolist())
