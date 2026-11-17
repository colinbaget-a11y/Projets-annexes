"""« Pour aller plus loin », piste 3 : revenus irréguliers et progressivité, avec le barème final du nouvel impôt.

A gagne 50 000 € par an pendant 5 ans ; B gagne 10, 20, 30, 70 puis 120 k€ (même cumul : 250 000 €). Revenus après
cotisations sociales, personne seule sans enfant (aucune franchise). Trois régimes :
  - annuel (droit commun) : impôt de l'année = T(revenu de l'année) ;
  - quotient pluriannuel par période de N ans (N = 3 ou 5 ; notre proposition) : dans la k-ième année d'une période,
    l'impôt cumulé dû depuis le début de la période vaut k × T(moyenne des k revenus) ; on paie chaque année la
    différence avec ce qui a déjà été payé (régularisation automatique, éventuellement négative = restitution). À la fin
    de la période, l'impôt total vaut N × T(moyenne). Sur 5 ans, une période de 3 ans puis une de 2 ans (sortie) ;
  - quotient glissant sur 3 ans (variante) : chaque année, l'impôt payé sur les trois dernières années est porté à
    3 × T(moyenne de ces trois revenus) : impôt_t = 3·T(m_t) − impôt_{t−1} − impôt_{t−2} ; avant la 1re année, deux
    années au revenu de la 1re année, imposées au barème annuel ;
  - périodes fixes de 3 ans (1-3 puis 4-5), pour mémoire : le résultat dépend du calage des périodes.
Variante : profil inverse (120, 70, 30, 20, 10 k€), qui fait apparaître des restitutions.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from pal_bareme import Bareme  # noqa: E402

A = [50_000.0] * 5
B = [10_000.0, 20_000.0, 30_000.0, 70_000.0, 120_000.0]


def annuel(b, y):
    return [b.T(v) for v in y]


def quotient(b, y, n):
    """Quotient pluriannuel par périodes successives de n ans (la dernière tronquée à l'horizon = sortie)."""
    out = []
    for d in range(0, len(y), n):
        bloc, deja = y[d:d + n], 0.0
        for k in range(1, len(bloc) + 1):
            du = k * b.T(sum(bloc[:k]) / k)
            out.append(du - deja)
            deja = du
    return out


def glissant(b, y, n=3):
    """Quotient glissant : la somme des impôts de toute fenêtre de n années vaut n × T(moyenne de la fenêtre)."""
    h, imp = [y[0]] * (n - 1), [b.T(y[0])] * (n - 1)
    for v in y:
        h.append(v)
        imp.append(n * b.T(sum(h[-n:]) / n) - sum(imp[-(n - 1):]))
    return imp[n - 1:]


def calcule(b=None):
    b = b or Bareme()
    res = {"bareme": b.decrit(), "profils": {"A": A, "B": B, "B_inverse": B[::-1]}, "regimes": {}}
    for nom, f in (("annuel", annuel), ("glissant_3", glissant), ("quotient_5", lambda b_, y: quotient(b_, y, 5)),
                   ("bloc_3", lambda b_, y: quotient(b_, y, 3))):
        r = {}
        for p, y in res["profils"].items():
            imp = f(b, y)
            r[p] = {"par_annee": imp, "total": sum(imp)}
        r["ecart_B_moins_A"] = r["B"]["total"] - r["A"]["total"]
        r["ecart_pct_impot_A"] = 100 * r["ecart_B_moins_A"] / r["A"]["total"]
        r["taux_moyen_A"] = 100 * r["A"]["total"] / sum(A)
        r["taux_moyen_B"] = 100 * r["B"]["total"] / sum(B)
        res["regimes"][nom] = r
    res["taux_marginaux"] = {str(int(v)): 100 * b.tm(v) for v in sorted(set(A + B))}
    return res


if __name__ == "__main__":
    R = calcule()
    print("Barème :", R["bareme"]["source"])
    for k, r in R["regimes"].items():
        print(f"{k:12s} A {r['A']['total']:9.0f}  B {r['B']['total']:9.0f}  écart {r['ecart_B_moins_A']:+8.0f}"
              f" ({r['ecart_pct_impot_A']:+.1f} %)  B annuel : " + " / ".join(f"{v:.0f}" for v in r["B"]["par_annee"])
              + "  inverse : " + " / ".join(f"{v:.0f}" for v in r["B_inverse"]["par_annee"]))
