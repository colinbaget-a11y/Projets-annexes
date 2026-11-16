"""Sensibilités complémentaires, sur le script corrigé (copie importée depuis le dépôt)."""
import sys, importlib.util
import numpy as np
spec = importlib.util.spec_from_file_location("sim", "/home/user/Projets-annexes/fiscalite/is/simulation_is.py")
sim = importlib.util.module_from_spec(spec); spec.loader.exec_module(sim)
pal = lambda t: 0.5 if t < 6 else 1.0
fin_bas = sim.ELARG_PRUDENT; fin_haut = sum(sim.ELARG.values())
print(f"A22 {sim.A22:.4f} A25 {sim.A25:.4f} POINT {sim.POINT:.3f} ; fin {fin_bas:.2f} / {fin_haut:.2f}")
def dette(reg, bonus, fin, part=0.75, r=sim.R_ETAT, h=40):
    c = sim.chemin(reg, bonus, part)[:h]; f = fin * (1 + sim.G) ** np.arange(h)
    d, D = 0.0, np.zeros(h)
    for t in range(h):
        d = d * (1 + r) - (f[t] - c[t]); D[t] = d
    pk = int(np.argmax(D)); rem = next((t + 1 for t in range(pk, h) if D[t] <= 0), None)
    return D[pk], pk + 1, rem, D
for part in (0.6, 0.75, 0.9):
    out = []
    for reg in ("lineaire", "degressif"):
        for nom, b in (("S3", pal), ("S4", lambda t: 1.0)):
            for f in (fin_bas, fin_haut):
                m, a, rem, _ = dette(reg, b, f, part=part)
                out.append(f"{nom}-{reg[:3]}-{f:.1f}: {m:.0f} (an {a}) -> {rem}")
    print(f"[PART {part}] " + " ; ".join(out))
# dette au pic en % du PIB et en euros de 2027
for reg, b, f, nom in (("lineaire", lambda t: 1.0, fin_bas, "S4 lin bas"), ("lineaire", pal, fin_bas, "S3 lin bas")):
    m, a, rem, D = dette(reg, b, f)
    pib = sim.PIB_2027 * (1 + sim.G) ** (a - 1)
    print(f"[PIC] {nom}: {m:.1f} Md€ an {a} ({2026+a}) = {100*m/pib:.2f} % du PIB ; {m/(1+sim.G)**(a-1):.1f} Md€ de 2027 ; remboursée an {rem} ({2026+rem})")
# coût de la marche de 2033
for reg in ("lineaire", "degressif"):
    c = sim.chemin(reg, pal, 0.75)
    print(f"[2033] {reg}: an6 {c[5]:.1f} an7 {c[6]:.1f} an8 {c[7]:.1f}")
# investissement induit : +10 % d'investissement éligible (ordre de Zwick et Mahon)
dI = 0.10 * sim.I1
print(f"[INDUIT] +10 % d'investissement la 1re année : coût supplémentaire an 1 = {sim.TAU*0.75*dI:.2f} Md€ (100 %), "
      f"{sim.TAU*0.75*dI*0.5:.2f} (50 %) ; recouvré ensuite par l'impôt sur le rendement")
# point de taux selon l'hypothèse 2026-27
for g26 in (0.0, 0.02, 0.025):
    f = 1.01 * 1.00 * 1.01 * (1 + g26) ** 2
    print(f"[BFI 2026-27 = {g26}] facteur {f:.3f} ; point {278*f/100:.2f} ; taux réduit {2.7*f:.2f} ; 28 % statique {0.03*251*f:.2f}")
# année de la baisse finale
for reg, f in (("lineaire", fin_bas), ("lineaire", fin_haut), ("degressif", fin_bas), ("degressif", fin_haut)):
    m, a, rem, D = dette(reg, pal, f)
    print(f"[BAISSE] S3 {reg} {f:.1f}: dette éteinte an {rem} ({2026+rem}) -> baisse possible dès {2027+rem}")
