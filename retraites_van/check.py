"""Contrôles du modèle.
1. Comptabilité générationnelle : la somme des pertes individuelles des personnes vivantes l'année de réforme (pondérée
   par leur nombre) est égale à la valeur actualisée des gains budgétaires que procurent ces mêmes personnes, calculée
   par une autre voie (projection de la seule population vivante, sans naissances ni migrations).
2. Rendement de chaque réforme à plein effet proche de la cible (10 Md€ de 2025).
Tout écart relatif supérieur à 1e-6 (contrôle 1) ou à 5 % (contrôle 2, sauf réforme C) bloque.
"""
import numpy as np

import model as m

pop0, qx, emp, sal, part, pens = m.donnees()
pr = m.profils(pop0, qx, emp, sal, part, pens)
T = m.P["horizon"]
N, Q = m.demographie(pop0, qx, T)
t0 = m.P["annee_reforme"] - m.P["annee_base"]
ok = True
for r in (0.01, 0.02, 0.03):
    M, cal = m.reformes(pr, N, Q, r, m.P["g"])
    # population vivante en t0, projetée sans entrées
    V = np.zeros_like(N)
    V[t0] = N[t0]
    for t in range(t0 + 1, T + 1):
        V[t, 1:] = V[t - 1, :-1] * (1 - Q[t - 1, :-1])
    for k, mat in M.items():
        ind = m.va_individuelle(mat, Q, r, t0)
        a = (N[t0] * ind).sum()
        b = sum((V[t] * mat[t]).sum() / (1 + r) ** (t - t0) for t in range(t0, T + 1))
        e = abs(a - b) / max(abs(b), 1)
        ok &= e < 1e-6
        print(f"r={r:.2f} {k:<10} vivants : somme des pertes {a / 1e9:9.2f} Md€ ; gains budgétaires {b / 1e9:9.2f} Md€ ; écart {e:.1e}")
res = m.calculer()
for k in ("A", "B"):
    e = abs(res[k]["flux_2026"] - m.P["budget_cible"]) / m.P["budget_cible"]
    ok &= e < 0.05
    print(f"rendement {k} en 2026 : {res[k]['flux_2026']:.2f} Md€ de 2025 (cible {m.P['budget_cible']})")
print("rendement C à plein effet (2040) :", round(res["C"]["flux_2040"], 2), "Md€ de 2025")
print("CONTRÔLES", "OK" if ok else "ÉCHEC")
raise SystemExit(0 if ok else 1)
