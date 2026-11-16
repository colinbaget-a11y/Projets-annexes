"""Hypothèse de saillance : le modèle suppose que la CSG et la CRDS d'aujourd'hui sont perçues comme l'IR (la
quantité réagit à Δln(1 − t) avec t = IR + CSG + CRDS avant comme après). Variante : aujourd'hui, seuls les salariés
« voient » l'IR (la CSG, prélevée sur la fiche de paie avec les cotisations, ne fait pas réagir, comme les
cotisations chez Lehmann, Marical et Rioux, 2013) ; après la fusion, tout l'impôt fusionné est vu. Coin réel
inchangé. Marge extensive inchangée. Lancer depuis fiscalite/ (après la correction de TAU0)."""
import sys
import numpy as np
sys.path.insert(0, "/tmp/claude-0/-home-user-Projets-annexes/935fc156-45bd-500a-b52a-e7e4ee23abb6/scratchpad/verif_ircsg/hyp")
import v2_independant as V
M, ps = V.M, V.ps
print(f"TAU0 moyen pondéré (actifs) : {np.average(M.TAU0, weights=M.W_A*M.Z_A):.3f}")
def ps_saillance(tm, T, o, part_csg_vue=0.0):
    (a, b, c, d), eta = V.V2["central"]
    eR = np.where(V.Q < .5, a, np.where(V.Q < .9, b, np.where(V.Q < .99, c, d)))
    tot = 0.0
    for nom, g_, fam, w, parts, kids in V.TYPES:
        if g_ != "A":
            continue
        imp, mgs = V.impot(tm, T, o, g_, parts, kids)
        single = 1.0 if len(parts) == 1 else 0.0
        for k, (sh, mg) in enumerate(zip(parts, mgs)):
            t0 = M.TAU0
            t0v = np.clip(t0 - (1 - part_csg_vue) * 0.097, 0, None)      # taux perçu aujourd'hui
            t1 = np.clip(mg * V.R_A, 0, .95)
            g = sh * V.Z_A * V.LAB_A
            er, ee, pa = ps.coin(g, single, "nc")
            er, ee, pa = ps.SALSH * er, ps.SALSH * ee, ps.SALSH * pa
            coin = er + ee + pa + (t0 + t1) / 2
            dq = eR * g * (np.log(1 - t1) - np.log(1 - t0v))
            tot += (w * -coin * dq).sum() / 1e9
    return tot
cas = {"étape 1": (V.empile(V.cale(lambda t: V.recette(*V.empile(t), {}), -0.1, 0.2)), {}),
       "neutre": (V.bar(.02, .14, 30e3, .2302, 250e3), {}),
       "proposition": (V.lineaire([0, 20e3, 45e3, 1e6], [.14, .14, .3027, .5]), dict(F=4000.0, fam="franchise", Fp=12500.0, deg=True))}
for nom, ((tm, T), o) in cas.items():
    tot, intens, ext = V.ps_v2(tm, T, o)
    print(f"{nom:<12} modèle (CSG vue) : intensive {intens.sum():+.2f}, extensive {ext:+.2f}, total {tot:+.2f} | CSG non vue aujourd'hui : intensive"
          f" {ps_saillance(tm, T, o, 0.0):+.2f} | à moitié vue : {ps_saillance(tm, T, o, 0.5):+.2f}")
