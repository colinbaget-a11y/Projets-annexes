"""
D'où vient l'écart entre « 12 % » et « 10 % » pour la part de l'industrie ?

Trois choix de construction séparent les deux graphiques :
  - numérateur   : industrie manufacturière (NACE C) ou industrie hors construction (B-E) ;
  - dénominateur : PIB ou valeur ajoutée totale des branches ;
  - valorisation : prix courants ou volumes chaînés (prix de 2020).

Le script calcule les huit ratios possibles, décompose l'écart entre les deux combinaisons
retenues par une valeur de Shapley (moyenne sur les six ordres de substitution, pour que
l'ordre des étapes ne décide pas du résultat), et compare les deux millésimes d'AMECO.

    python part_industrie.py
"""
import csv
import itertools
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
DATA = HERE / "donnees"

BASE = ("C", "PIB", "valeur")        # le calcul du collègue : b1g_c / pib
CIBLE = ("B-E", "VA", "volume")      # le calcul de la note : VA industrie / VA totale en volume


def charger(millesime):
    d = {}
    with open(DATA / f"ameco_france_{millesime}.csv", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            d.setdefault(r["serie"], {})[int(r["annee"])] = float(r["valeur"])
    return d


def ratio(d, num, den, prix, annee):
    p = "O" if prix == "volume" else "U"
    n = d[p + "VGM" if num == "C" else p + "VG2"]
    q = d[p + "VGD" if den == "PIB" else p + "VG0"]
    return 100 * n[annee] / q[annee]


def shapley(d, annee):
    """Contribution moyenne de chaque choix à l'écart BASE -> CIBLE, sur les 6 ordres."""
    contrib = [0.0, 0.0, 0.0]
    for ordre in itertools.permutations(range(3)):
        etat = list(BASE)
        for f in ordre:
            avant = ratio(d, *etat, annee)
            etat[f] = CIBLE[f]
            contrib[f] += (ratio(d, *etat, annee) - avant) / 6
    return contrib


def main():
    S, A = charger("s2026"), charger("a2025")
    res = {"millesime": "AMECO printemps 2026", "annees": {}}
    noms = ["numerateur_C_vers_BE", "denominateur_PIB_vers_VA", "valeur_vers_volume"]

    for annee in (2019, 2023, 2024, 2025):
        base, cible = ratio(S, *BASE, annee), ratio(S, *CIBLE, annee)
        c = shapley(S, annee)
        print(f"\n===== {annee} =====")
        print(f"  C / PIB en valeur   (collègue) = {base:5.2f} %")
        print(f"  B-E / VA en volume  (note)     = {cible:5.2f} %")
        print(f"  écart                          = {cible - base:+5.2f} pt")
        for nom, v in zip(noms, c):
            print(f"    {nom:26s} {v:+5.2f} pt  ({100 * v / (cible - base):5.1f} % de l'écart net)")
        res["annees"][annee] = {
            "base_C_PIB_valeur": base, "cible_BE_VA_volume": cible, "ecart": cible - base,
            "contributions": dict(zip(noms, c)),
            "tous_ratios": {f"{n}/{d_}/{p}": ratio(S, n, d_, p, annee)
                            for n, d_, p in itertools.product(["C", "B-E"], ["PIB", "VA"], ["valeur", "volume"])},
        }

    print("\n===== révisions entre les deux millésimes =====")
    revisions = {}
    for serie in ["UVGD", "OVGD", "UVG0", "OVG0", "UVG2", "OVG2", "UVGM", "OVGM", "FETD", "FET2", "FETM"]:
        communes = [a for a in S[serie] if a in A[serie] and a <= 2024]
        ecarts = [(a, S[serie][a], A[serie][a]) for a in communes if abs(S[serie][a] - A[serie][a]) > 1e-9]
        revisions[serie] = {"annees_communes": len(communes), "annees_revisees": len(ecarts)}
        print(f"  {serie:5s} : {len(ecarts)} année(s) révisée(s) sur {len(communes)} (1960-2024)")
    res["revisions_1960_2024"] = revisions
    (HERE / "resultats.json").write_text(json.dumps(res, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
