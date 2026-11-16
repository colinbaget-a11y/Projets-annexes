import numpy as np
# Gompertz mu(x)=A exp(Bx), B=0.10, calibrated on e(65)=21.8 (moyenne femmes 23.6 / hommes 20.0, Insee 2025 provisoire)
B=0.10
ages=np.arange(0,121,0.25)
def surv(A,x0):
    xs=np.arange(x0,121,0.25); mu=A*np.exp(B*xs); S=np.exp(-np.cumsum(mu)*0.25); return xs,S
def e(A,x0):
    xs,S=surv(A,x0); return S.sum()*0.25
lo,hi=1e-7,1e-3
for _ in range(100):
    m=(lo*hi)**0.5
    if e(m,65)>21.8: lo=m
    else: hi=m
A=m
print("A",A,"e65",e(A,65),"e74",e(A,74))
# stock of retirees: cohorts of equal size at 62, surviving from 62
xs,S62=surv(A,62)
stock=S62  # density by age 62..120
def annuity(x0,r):
    xs,S=surv(A,x0); t=xs-x0; return (S*np.exp(-r*t)).sum()*0.25
for r in (0.01,0.02,0.03):
    fac=np.array([annuity(x,r) for x in xs])
    w=stock/stock.sum()
    print(f"r={r:.0%} facteur moyen pondéré du stock {np.sum(w*fac):.1f} ; âge moyen du stock {np.sum(w*xs):.1f}")
