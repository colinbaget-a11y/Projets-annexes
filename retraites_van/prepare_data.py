"""Prépare les séries par âge du modèle (data/*.csv) à partir des extractions propres (Insee, Eurostat, DREES).
Usage : python3 -I prepare_data.py <dossier des extractions>   (les extractions ne sont jamais exécutées, seulement lues)
"""
import csv
import json
import sys
from pathlib import Path

import numpy as np

SRC = Path(sys.argv[1])
D = Path(__file__).resolve().parent / "data"
AMAX = 106


def lire(nom):
    with open(SRC / nom, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def age_num(s):
    s = s.strip().replace("+", "")
    return int(s) if s.isdigit() else None


def ecrire(nom, entete, lignes):
    with open(D / nom, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(entete)
        w.writerows(lignes)


# population au 1er janvier 2025 (Insee, bilan démographique 2025), 105 ans et plus regroupés à 105
pop = np.zeros(AMAX)
for r in lire("population_2025.csv"):
    a = age_num(r["age"])
    if a is not None:
        pop[min(a, AMAX - 1)] += float(r["pop"])
ecrire("population_2025.csv", ["age", "pop"], [(a, int(pop[a])) for a in range(AMAX)])

# mortalité : Eurostat 2024 (0-94), puis quotients Insee 2025 tous sexes (95-100), puis prolongement de Gompertz
q = {}
for r in lire("mortalite.csv"):
    a = age_num(r["age"])
    if a is None:
        continue
    if a <= 94 and r["qx"] and not r["age"].endswith("+"):
        q[a] = float(r["qx"])
    elif a >= 95 and r.get("qx_insee2025_age_atteint_both_sexes_derived"):
        q[a] = float(r["qx_insee2025_age_atteint_both_sexes_derived"])
pente = np.log(q[100] / q[95]) / 5
for a in range(101, AMAX):
    q[a] = min(1.0, q[100] * np.exp(pente * (a - 100)))
q[AMAX - 1] = 1.0
ecrire("mortalite.csv", ["age", "qx"], [(a, round(q[a], 6)) for a in range(AMAX)])

# pensions et part de retraités par âge (DREES, EACR-Ancetre, fin 2024)
part, pens = np.zeros(AMAX), np.zeros(AMAX)
for r in lire("pension_age.csv"):
    a = age_num(r["age_band"])
    if a is None or not r["share_retired"]:
        continue
    rng = range(a, AMAX) if r["age_band"].endswith("+") else [a]
    for x in rng:
        part[x], pens[x] = float(r["share_retired"]), float(r["pension_moyenne_mensuelle"])
pens[:50] = pens[50]
ecrire("pension_age.csv", ["age", "share_retired", "pension_moyenne_mensuelle"],
       [(a, round(part[a], 4), round(pens[a], 1)) for a in range(AMAX)])

# emploi : tranches quinquennales (Insee, enquête Emploi 2025). Avant 55 ans, interpolation entre centres de tranches ;
# de 55 à 74 ans, emploi = k × (1 − part de retraités), k constant par tranche et calé sur le taux de la tranche
emp = np.zeros(AMAX)
bandes = {}
for r in lire("taux_emploi_age.csv"):
    lo, _, hi = r["age"].partition("-")
    if lo.isdigit() and hi.isdigit() and int(hi) - int(lo) == 4:
        bandes[(int(lo), int(hi))] = float(r["taux_emploi"]) / 100
cent = sorted(((lo + hi) / 2, v) for (lo, hi), v in bandes.items())
emp[:] = np.interp(np.arange(AMAX), [c for c, _ in cent], [v for _, v in cent], left=0, right=0)
emp[:15] = 0
for (lo, hi), v in bandes.items():
    if lo >= 55:
        a = np.arange(lo, hi + 1)
        w = pop[a]
        k = v * w.sum() / (w * (1 - part[a])).sum()
        emp[a] = k * (1 - part[a])
emp[75:] = 0
ecrire("taux_emploi_age.csv", ["age", "taux_emploi"], [(a, round(emp[a], 4)) for a in range(AMAX)])

# salaires : revenu salarial net annuel moyen par tranche (Insee, ECRT 2026, 2023) ; profil relatif seulement
centres = {"<25": 21.5, "25-39": 32, "40-49": 45, "50-54": 52, "55+": 59}
pts = [(centres[r["age_band"]], float(r["salaire_annuel_moyen"])) for r in lire("salaire_age.csv") if r["age_band"] in centres]
ecrire("salaire_age.csv", ["age", "salaire_annuel_moyen"], sorted(pts))

# contrôles imprimés
e64 = 0
s = 1.0
for a in range(64, AMAX):
    s *= 1 - q[a]
    e64 += s
print(f"population totale {pop.sum() / 1e6:.2f} M ; e64 période ≈ {e64 + 0.5:.1f} ans ; part de retraités à 62/64/66 :"
      f" {part[62]:.2f}/{part[64]:.2f}/{part[66]:.2f} ; emploi 55/60/62/64/66 : "
      + "/".join(f"{emp[a]:.2f}" for a in (55, 60, 62, 64, 66)))
# vérification : moyenne pondérée par tranche = taux publié
for (lo, hi), v in sorted(bandes.items()):
    a = np.arange(lo, hi + 1)
    print(f"  {lo}-{hi} : publié {v:.3f} ; modèle {(pop[a] * emp[a]).sum() / pop[a].sum():.3f}")
(D / "SOURCES.csv").write_bytes((SRC / "SOURCES.csv").read_bytes())
json.dump({"esperance_vie_cohorte": list(lire("esperance_vie_cohorte_derivee.csv"))},
          open(D / "esperance_vie_cohorte.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
