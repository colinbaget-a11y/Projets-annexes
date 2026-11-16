"""Faisabilité de calculs manquants : (1) réforme naïve qui garde l'imposition commune (quotient conjugal et familial,
plafonds actuels) ; (2) distribution des hausses individuelles pour la transition (3, 5, 10 ans) ; (3) cas-types
de retraités à plusieurs niveaux de pension. Lancer depuis fiscalite/."""
import sys, json
import numpy as np
sys.path[:0] = ["/home/user/Projets-annexes/fiscalite/synthese"]
import modele_purs as M
import architectures_ircsg as A
ex = M.ex
o0 = A.options()
oq = A.options(fam="quotient")
# (1) étape 1 avec imposition commune
r_ir = M.recette(*ex.bareme_empile(0.0), oq)
lo, hi = -0.1, 0.2
for _ in range(40):
    t = (lo + hi) / 2
    lo, hi = (t, hi) if M.recette(*ex.bareme_empile(t), oq) < M.CIBLE else (lo, t)
tau = (lo + hi) / 2
r = M.evalue("naive quotient", *ex.bareme_empile(tau), oq, sorties=True)
g = r["groupes"]
print(f"(1) Réforme naïve avec quotient conjugal et familial : barème IR seul {r_ir:.1f} Md€ ; taux proportionnel {100*tau:.2f} % ;"
      f" PS v2 {r['v2']:+.2f} ; perdants {r['perdants500']:.0f} % ; déciles " + " ".join(f"{u:+.0f}" for u in r["dec_eur"])
      + f" ; 10 % {r['top10_Md']:+.1f} ; retraités {g['retraites']['Md']:+.1f} Md€ ; couples 2 enf {g['couples2']['eur']:+.0f} €")
print("    cas-types : " + " ; ".join(f"{p} {b/1e3:.0f}k {M.cas_type(*ex.bareme_empile(tau), oq, p, b):+,.0f}" for p, b in (
    ("retraite_seul", 17e3), ("seul", 21.5e3), ("couple_2enf", 50e3), ("couple_2enf_mono", 50e3), ("couple_2enf_mono", 80e3))))
# (2) distribution des hausses, proposition (franchise 4 000 €)
J = json.loads(open("/home/user/Projets-annexes/fiscalite/synthese/sorties/architectures_ircsg.json").read())
P4 = J["propositions"]["4000"]
s = A.bareme(P4["bareme"]); op = P4["options"]
rows = []
for nom, grp, fam, w, parts, kids in M.TYPES:
    imp = M.impot_adultes(*s, op, *M.adultes(grp, parts, op), kids)[0]
    rows.append((grp, fam, w, imp - M.CURT[nom]))
for lab, f in (("tous", lambda g, fm: True), ("retraités", lambda g, fm: g == "R"), ("couples de retraités", lambda g, fm: g == "R" and fm == "couples0"),
               ("actifs", lambda g, fm: g == "A")):
    d = np.concatenate([r[3] for r in rows if f(r[0], r[1])]); w = np.concatenate([r[2] for r in rows if f(r[0], r[1])])
    o = np.argsort(d); d, w = d[o], w[o]; c = np.cumsum(w) / w.sum()
    q = {p: d[np.searchsorted(c, p)] for p in (0.5, 0.75, 0.9, 0.99)}
    perd = w[d > 500].sum() / 1e6
    print(f"(2) {lab:<22} hausse médiane {q[0.5]:+,.0f} € ; P75 {q[0.75]:+,.0f} ; P90 {q[0.9]:+,.0f} ; P99 {q[0.99]:+,.0f} ; perdants > 500 € {perd:.1f} M"
          + " ; hausse annuelle au P90 sur 3 / 5 / 10 ans : " + " / ".join(f"{max(q[0.9],0)/n:,.0f}" for n in (3, 5, 10)))
# (3) retraité seul : pension de 10 000 à 40 000 €, proposition et barème neutre
sN = A.bareme(J["neutre"])
print("(3) retraité seul (OpenFisca 2024 → proposition / neutre) : " + " ; ".join(
    f"{b/1e3:.0f}k auj. {float(M.CT[(M.CT.profil=='retraite_seul')&(M.CT.brut==b)].actuel.iloc[0]):,.0f} → {M.cas_type(*s, op, 'retraite_seul', b):+,.0f} / {M.cas_type(*sN, o0, 'retraite_seul', b):+,.0f}"
    for b in (10e3, 12.5e3, 15e3, 17e3, 20e3, 25e3, 30e3, 40e3)))
