"""
Panorama chiffré des prélèvements obligatoires français, à partir de donnees/ntl_france.csv.

Produit panorama.json et un affichage console : les quatre blocs, les prélèvements classés
par rendement, la concentration du produit fiscal, la déformation de la structure depuis 1995.

    python panorama.py [annee]
"""
import csv
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
DOUBLONS = {"D51M", "D51O"}


def charger(annee):
    rows = list(csv.DictReader(open(HERE / "donnees" / "ntl_france.csv", encoding="utf-8")))
    pib = {int(k): v for k, v in json.loads((HERE / "donnees" / "pib_france_cp_meur.json").read_text()).items()}
    detail = [r for r in rows if r["details"] not in ("_T", "") and r["sto"] not in DOUBLONS and r[str(annee)] != ""]
    agreg = {r["sto"]: {int(y): float(r[y]) for y in r if y.isdigit() and r[y] != ""}
             for r in rows if r["details"] == "_T"}
    return detail, agreg, pib


def concentration(detail, annee):
    s = sorted(detail, key=lambda r: -float(r[str(annee)]))
    total = sum(float(r[str(annee)]) for r in s)
    cum, seuils = 0.0, {}
    for i, r in enumerate(s, 1):
        cum += float(r[str(annee)])
        for q in (50, 75, 90, 95, 99):
            seuils.setdefault(q, None)
            if seuils[q] is None and cum >= q / 100 * total:
                seuils[q] = i
    return s, total, seuils


def main(annee=2024):
    detail, agreg, pib = charger(annee)
    G = pib[annee]
    s, total, seuils = concentration(detail, annee)
    blocs = [("D61", "Cotisations sociales nettes"), ("D2", "Impôts sur la production et les importations"),
             ("D5", "Impôts courants sur le revenu et le patrimoine"), ("D91", "Impôts en capital")]

    print(f"=== Prélèvements obligatoires, France {annee} (PIB = {G:,.0f} M€) ===".replace(",", " "))
    for c, lib in blocs:
        v = agreg[c][annee]
        print(f"  {lib:48s} {v:9,.0f} M€  {100*v/G:5.2f} % PIB  {100*v/agreg['ODB'][annee]:5.1f} % du total".replace(",", " "))
    for c, lib in [("ODA", "Total des recettes fiscales (hors cotisations)"),
                   ("ODB", "Impôts + cotisations, hors cotisations imputées"),
                   ("ODC", "Impôts + cotisations, y compris imputées")]:
        print(f"  {lib:48s} {agreg[c][annee]:9,.0f} M€  {100*agreg[c][annee]/G:5.2f} % PIB".replace(",", " "))

    print(f"\n=== Les {len(s)} impôts recensés, hors cotisations sociales ===")
    for r in s[:25]:
        v = float(r[str(annee)])
        print(f"  {v:8,.0f} M€  {100*v/G:5.2f} % PIB  {r['sto']:6s} {r['fonction']:7s} {r['nom_fr'][:62]}".replace(",", " "))
    print("  concentration : " + ", ".join(f"{q} % du produit en {i} prélèvements" for q, i in sorted(seuils.items())))
    petits = [r for r in s if float(r[str(annee)]) < 150]
    print(f"  longue traîne : {len(petits)} prélèvements sous 150 M€, "
          f"{sum(float(r[str(annee)]) for r in petits):,.0f} M€ cumulés, soit {100*sum(float(r[str(annee)]) for r in petits)/total:.2f} % du produit fiscal".replace(",", " "))

    print("\n=== Déformation de la structure, en % du PIB ===")
    suivi = [("D61", "Cotisations sociales"), ("D211", "TVA"), ("D214", "Autres impôts sur les produits"),
             ("D29", "Autres impôts sur la production"), ("D51A", "Impôts sur le revenu des ménages"),
             ("D51B", "Impôts sur les sociétés"), ("D59", "Autres impôts courants"),
             ("D91", "Impôts en capital"), ("ODB", "TOTAL")]
    print(f"  {'':36s} 1995   2010   {annee}")
    structure = {}
    for c, lib in suivi:
        v = [100 * agreg[c][y] / pib[y] for y in (1995, 2010, annee)]
        structure[lib] = dict(zip(("1995", "2010", str(annee)), v))
        print(f"  {lib:36s} {v[0]:5.2f}  {v[1]:5.2f}  {v[2]:5.2f}   ({v[2]-v[0]:+.2f} pt)")

    res = {"annee": annee, "pib_meur": G,
           "blocs": {c: {"meur": agreg[c][annee], "pct_pib": 100*agreg[c][annee]/G} for c, _ in blocs},
           "agregats": {c: {"meur": agreg[c][annee], "pct_pib": 100*agreg[c][annee]/G} for c in ("ODA", "ODB", "ODC")},
           "n_impots": len(s), "concentration": seuils,
           "longue_traine": {"seuil_meur": 150, "nombre": len(petits),
                             "cumul_meur": sum(float(r[str(annee)]) for r in petits)},
           "classement": [{"nom": r["nom_fr"], "sto": r["sto"], "fonction": r["fonction"],
                           "meur": float(r[str(annee)]), "pct_pib": 100*float(r[str(annee)])/G} for r in s],
           "structure_pct_pib": structure}
    (HERE / "panorama.json").write_text(json.dumps(res, indent=1, ensure_ascii=False))


if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 2024)
