"""
Socle de données du projet « système fiscal français ».

Trois sources, toutes publiques et sans inscription :

1. Eurostat, National Tax Lists (NTL). Liste détaillée, impôt par impôt, transmise chaque
   année par la France à Eurostat avec la table 0900 du programme de transmission SEC 2010.
   C'est la seule source qui donne, dans un même fichier, le rendement de chaque prélèvement,
   son code SEC et sa fonction économique, de 1995 à 2024.
   Fichier : National_tax_lists_2024_2026-07-21.xlsx, onglet FR, mise à jour du 21 juillet 2026.

2. Eurostat, PIB à prix courants (nama_10_gdp, B1GQ, CP_MEUR), pour exprimer les rendements
   en points de PIB.

3. Voies et moyens tome II annexé au PLF 2026 : les dépenses fiscales de l'État.

    python extract_donnees.py
"""
import csv
import json
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
DATA = HERE / "donnees"
SOURCES = HERE / "sources"

NTL = ("https://ec.europa.eu/eurostat/statistics-explained/images/f/f0/"
       "National_tax_lists_2024_2026-07-21.xlsx")
PIB = ("https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/nama_10_gdp"
       "?geo=FR&na_item=B1GQ&unit=CP_MEUR&sinceTimePeriod=1995&format=JSON")
VM2 = ("https://www.assemblee-nationale.fr/dyn/dyn/contenu/visualisation/1087933/file/"
       "Voies_et_moyens_Tome_2_2026.pdf")

# Deux codages parallèles du même impôt coexistent dans la NTL : D51M reprend D51A
# (revenu des personnes physiques) et D51O reprend D51B (bénéfices des sociétés).
# Sommer les deux double-compterait l'intégralité de l'impôt sur le revenu.
DOUBLONS = {"D51M", "D51O"}


def telecharger(url, dst):
    if not dst.exists():
        dst.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(["curl", "-sS", "-L", "--max-time", "300", "-o", str(dst), url], check=True)
    return dst


def extraire_ntl(xlsx, dst):
    import openpyxl
    ws = openpyxl.load_workbook(xlsx, read_only=True, data_only=True)["FR"]
    rows = [list(r) for r in ws.iter_rows(values_only=True)]
    hdr = rows[7]
    annees = {}
    for j, c in enumerate(hdr):
        try:
            a = int(str(c).strip())
            if 1990 <= a <= 2030:
                annees[j] = a
        except (TypeError, ValueError):
            pass

    def txt(c):
        return "" if c is None else str(c).replace("\n", " ").strip()

    cols = ["sto", "details", "nom_fr", "nom_en", "fonction", "tag"] + [str(a) for a in sorted(annees.values())]
    n = 0
    with open(dst, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(cols)
        for r in rows[8:]:
            if not txt(r[0]):
                continue
            vals = {a: (r[j] if j < len(r) and isinstance(r[j], (int, float)) else "") for j, a in annees.items()}
            w.writerow([txt(r[0]), txt(r[1]), txt(r[2]), txt(r[5]), txt(r[9]), txt(r[10])]
                       + [vals[a] for a in sorted(annees.values())])
            n += 1
    print(f"{dst.name} : {n} lignes (unité : millions d'euros)")


def extraire_pib(src, dst):
    d = json.loads(Path(src).read_text())
    inv = {v: k for k, v in d["dimension"]["time"]["category"]["index"].items()}
    pib = {inv[int(k)]: v for k, v in d["value"].items()}
    Path(dst).write_text(json.dumps(pib, indent=1))
    print(f"{Path(dst).name} : PIB {min(pib)}-{max(pib)}, {pib[max(pib)]:,.0f} M€ en {max(pib)}".replace(",", " "))


if __name__ == "__main__":
    DATA.mkdir(exist_ok=True)
    extraire_ntl(telecharger(NTL, SOURCES / "national_tax_lists_2024.xlsx"), DATA / "ntl_france.csv")
    extraire_pib(telecharger(PIB, SOURCES / "pib_france.json"), DATA / "pib_france_cp_meur.json")
    telecharger(VM2, SOURCES / "voies_et_moyens_tome2_plf2026.pdf")
    print("voies_et_moyens_tome2_plf2026.pdf : dépenses fiscales de l'État, chiffres clés p. 13")
