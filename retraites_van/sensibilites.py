"""Sensibilités : perte actualisée (k€ de 2025) à 25, 40 et 55 ans, réformes de même effet sur le solde public."""
import copy
import json
from pathlib import Path

import model as m

BASE = copy.deepcopy(m.P)
AGES = (25, 40, 55, 70)


def run(nom, actualisation=None, **chg):
    m.P.clear()
    m.P.update(copy.deepcopy(BASE))
    for k, v in chg.items():
        if k == "solde_retraites_age":
            m.P["cor_2026"]["solde_retraites_age"] = {"variante": [v] * 6}
        else:
            m.P[k] = v
    r = m.calculer(actualisation=actualisation)
    ligne = {k: [round(r[k]["perte_par_age"][a] / 1000, 1) for a in AGES] for k in ("A", "B", "C")}
    ligne["part_retraites_A"] = round(sum(r["A"]["va_par_tranche"][t] for t in ("65-74", "75-105")) / r["A"]["va_budget"], 2)
    print(f"{nom:<46}" + " | ".join(f"{k} " + "/".join(f"{x:5.1f}" for x in v) for k, v in ligne.items() if k != "part_retraites_A")
          + f" | retraités {100 * ligne['part_retraites_A']:.0f} %")
    return nom, ligne


print(f"{'':<46}pertes à {'/'.join(map(str, AGES))} ans, k€")
S = [run("central (r 2 %, g 0,7 %, COR à 20 ans)"),
     run("r = 1 %", r=0.01), run("r = 3 %", r=0.03), run("r = g = 0,7 %", r=0.007),
     run("g = 0,4 %", g=0.004), run("g = 1,0 %", g=0.010),
     run("calage COR à 5 ans", horizon_calage=5),
     run("âge : économie de pensions 0,30 pt de PIB (DREES)", solde_retraites_age=0.30 + 0.057),
     run("âge : 20 % compensé par d'autres prestations", part_compensee_autres_prestations=0.2),
     run("âge : 35 % compensé", part_compensee_autres_prestations=0.35),
     run("sans amélioration de la mortalité", amelioration_mortalite=0.0),
     run("pensions qui suivent les salaires (sans décrochage COR)", croissance_pension_reelle=0.007),
     run("courbe des taux réels de marché (OAT indexées)", actualisation="courbe"),
     run("valeur de marché, risque de salaire (CMS)", actualisation="risque"),
     run("jeunes contraints : +2 pts jusqu'à 30 ans", actualisation="liquidite")]
(Path(__file__).parent / "sorties" / "sensibilites.json").write_text(json.dumps(dict(S), ensure_ascii=False, indent=1))
