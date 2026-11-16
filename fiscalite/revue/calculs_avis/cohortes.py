import numpy as np
B=0.10; A=1.2227437716464447e-05   # Gompertz calé sur e(65)=21.8 (annuite.py)
gain_actif=15e9/(27.14e6+9.30e6)    # € par adulte actif et par an (modèle : foyers actifs 27,14 M dont 9,30 M couples)
cout_retr=15e9/(14.49e6+3.75e6)     # € par adulte retraité et par an
print(f"par adulte : actif -{gain_actif:.0f} €/an ; retraité +{cout_retr:.0f} €/an")
def va(age,r,retraite=64,dt=0.25):
    xs=np.arange(age,121,dt); mu=A*np.exp(B*xs); S=np.exp(-np.cumsum(mu)*dt); d=np.exp(-r*(xs-age))
    flux=np.where(xs<retraite,gain_actif,-cout_retr)
    return (S*d*flux).sum()*dt
for r in (0.01,0.02,0.03):
    print(f"r={r:.0%} : "+" ; ".join(f"{a} ans {va(a,r):+,.0f} €" for a in (25,30,35,40,45,50,55,60,64,70,80)))
# levée sur la taxe foncière : VA d'un impôt perpétuel de 5,7 Md€ capitalisé à 3 et 4 %
for k in (0.03,0.04): print(f"taxe nationale sur le sol 5,7 Md€/an capitalisée à {k:.0%} : {5.7/k:.0f} Md€")
# étalement linéaire sur 10 ans d'une hausse perpétuelle : part de la VA immédiate
for k in (0.03,):
    t=np.arange(0,400); w=np.minimum((t+1)/10,1); print("étalement 10 ans, part de la VA :", round((w*np.exp(-k*t)).sum()/np.exp(-k*t).sum(),2))
# holding : capitalisation au taux brut contre taux net de PFU
for r,T in ((0.05,25),(0.05,40)):
    print(f"holding r={r:.0%} T={T} : richesse finale relative {((1+r)/(1+r*(1-0.314)))**T:.2f}")
# VA d'un impôt différé sans intérêt
for T in (10,20,30,50): print(f"VA de 1 € d'impôt dû dans {T} ans à 4 % : {1.04**-T:.2f}")
# déduction immédiate : gain d'attendre le palier 50 -> 100 %
z=0.87; z50=0.5+0.5*z; print("gain d'attendre le palier (en % du prix) :", round(0.25*(1-z50)*100,2))
