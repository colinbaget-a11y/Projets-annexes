"""Réplication de la simulation OCDE 2010 (Annexe C, Table C1) et inversion pour une baisse de 37/53 points PISA.
Modèle (Hanushek & Woessmann 2010, Annexe C ; 2011 Economic Policy, sect. 6.2) :
 - réforme démarre en T0, montée linéaire de la qualité des nouvelles cohortes sur D années, puis permanente
 - vie active W=40 ans -> compétence moyenne de la main-d'oeuvre = moyenne des 40 dernières cohortes
 - effet croissance Delta_t = coef (pp par écart-type) x compétence moyenne (en écart-types)
 - PIB sans réforme croît à g ; avec réforme à g + Delta_t (version 'endogène')
 - version 'néoclassique' (HW 2011, sect. 6.4) : Delta_t = coef_nc x skill_t - lambda x (lnGDP_reform - lnGDP_noreform)
 - valeur = somme actualisée (r) des écarts de PIB jusqu'à l'horizon H, rapportée au PIB de T0
"""
import math

def simulate(dpisa, coef=1.736, T0=2010, D=20, H=2090, W=40, g=0.015, r=0.03,
             neoclassical=False, coef_nc=1.718, lam=1.835, phase_in=True):
    # skill of cohort entering labour force in year t (in SD units, 100 pts = 1 SD)
    def cohort_skill(t):
        if t <= T0: return 0.0
        if phase_in and t <= T0 + D: return dpisa/100.0 * (t - T0)/D
        return dpisa/100.0
    gdp_n, gdp_r = 1.0, 1.0
    pv, pv_base = 0.0, 0.0
    path = {}
    for t in range(T0+1, H+1):
        skill = sum(cohort_skill(t-k) for k in range(W))/W
        if neoclassical:
            delta = (coef_nc*skill - lam*(math.log(gdp_r) - math.log(gdp_n)))/100.0
        else:
            delta = coef*skill/100.0
        gdp_n *= (1+g)
        gdp_r *= (1+g+delta)
        disc = (1+r)**(-(t-T0))
        pv += (gdp_r-gdp_n)*disc
        pv_base += gdp_n*disc
        path[t] = (gdp_r/gdp_n-1, delta*100, skill)
    return pv, pv_base, path

def report(label, **kw):
    pv, pvb, path = simulate(**kw)
    yrs = [2030, 2042, 2050, 2070, 2090]
    s = f"{label:60s} | VA/PIB_T0 = {pv*100:7.1f}% | VA/VA(PIB base) = {pv/pvb*100:6.2f}% | "
    s += " ; ".join(f"{y}: {path[y][0]*100:+.1f}%" for y in yrs if y in path)
    s += f" | Delta LT = {path[max(path)][1]:+.3f} pp"
    print(s)

print("### VALIDATION : scénario I OCDE 2010 (+25 pts, coef 1,736, réforme 2010-2030, horizon 2090, r=3%, g=1,5%)")
print("### attendu : +3,0% en 2042, +5,5% en 2050, +14,2% en 2070, +24,3% en 2090, VA = 268% du PIB courant, Delta LT = +0,43 pp")
report("OCDE 2010 +25 pts (endogène)", dpisa=25)
print("### validation HW 2011 EconPol (+25, coef 1,864) : attendu 3,0% en 2041, 5,9% 2050, 15,3% 2070, 26,3% 2090, VA=288%, Delta LT=0,47")
report("HW 2011 +25 pts (endogène, coef 1,864)", dpisa=25, coef=1.864)
print()
print("### INVERSION : baisse permanente de 37 et 53 points (0,37 / 0,53 écart-type élève)")
for d in (-37, -53):
    print(f"--- {d} points ---")
    report(f"A. miroir OCDE 2010 : baisse phasée sur 20 ans dès 2010 (coef 1,736)", dpisa=d)
    report(f"A'. idem, coef borne basse 1,47 (institutions)", dpisa=d, coef=1.47)
    report(f"A''. idem, coef 0,93 (borne inf. IC95%)", dpisa=d, coef=0.93)
    report(f"B. baisse déjà acquise : cohortes entrant dès 2026 à {d} pts, horizon 2105 (80 ans)", dpisa=d, T0=2025, H=2105, phase_in=False)
    report(f"C. néoclassique HW2011 (coef 1,718, lambda 1,835), phasée 20 ans dès 2010", dpisa=d, neoclassical=True)
    report(f"C'. néoclassique, baisse déjà acquise dès 2026, horizon 2105", dpisa=d, T0=2025, H=2105, phase_in=False, neoclassical=True)
    report(f"C''. néoclassique JEG2012 col.9 (coef 1,985, lambda 0,879), phasée dès 2010", dpisa=d, neoclassical=True, coef_nc=1.985, lam=0.879)
print()
print("### Effet de niveau de long terme implicite (état stationnaire néoclassique) = coef_nc/lambda x dSD (en log points)")
for coef_nc, lam, src in ((1.718,1.835,'HW2011 OCDE 24 pays'), (1.985,0.879,'HW2012 JEG col.9, 50 pays')):
    for d in (-25,-37,-53):
        print(f"  {src:28s} dPISA={d:+d}: dlnY = {coef_nc/lam*d/100:+.3f}  -> niveau PIB/tête {100*(math.exp(coef_nc/lam*d/100)-1):+.1f}%")
