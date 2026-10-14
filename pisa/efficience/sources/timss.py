"""TIMSS, 4e année (CM1) : indicateurs par pays de l'UE, cycles 1995 à 2023.

Indicateurs produits (format long : pays, indicateur, annee, valeur, source, note) :
    timss4_maths, timss4_sciences                 score moyen
    timss4_avance_maths, timss4_avance_sciences   % d'élèves au niveau avancé (>= 625)
    timss4_bas_maths, timss4_bas_sciences         % d'élèves sous le niveau bas (< 400),
                                                  = 100 - % atteignant 400 (pourcentages publiés arrondis)

Sources : tableaux « International Results » du TIMSS & PIRLS International Study Center
(Excel pour 2015, 2019 et 2023, PDF pour 2003, 2007 et 2011). Les valeurs 1995 viennent des
tableaux de tendance des rapports ultérieurs (échelle 1995 réétalonnée pour les tendances, voir
timss_notes.md) ; à défaut, de l'API Banque mondiale (EdStats), signalé dans `source` et `note`.

Usage :
    python3 -I timss.py [dossier_brut]    # télécharge si besoin, extrait, contrôle, écrit timss.csv

Dépendances : pandas, openpyxl, xlrd (fichiers .xls de 2015), pymupdf ; téléchargement par urllib.
Les fichiers téléchargés sont traités comme des données : aucun code n'en est exécuté.
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
from datetime import date
from pathlib import Path

import pandas as pd

DOSSIER_BRUT_DEFAUT = Path(
    "/tmp/claude-0/-home-user-Projets-annexes/935fc156-45bd-500a-b52a-e7e4ee23abb6"
    "/scratchpad/efficience/timss_raw"
)
SORTIE_CSV = Path(__file__).resolve().with_name("timss.csv")
COLONNES = ["pays", "indicateur", "annee", "valeur", "source", "note"]

# --------------------------------------------------------------------------------------------
# Pays : nom TIMSS -> code ISO2 Eurostat. La Belgique n'est jamais couverte en entier :
# "Belgium (Flemish)" sert de ligne BE (communauté flamande) ; "Belgium (French)" (2023 seulement)
# n'est exportée que sur demande, sous le code BE_FR (hors nomenclature UE27).
# --------------------------------------------------------------------------------------------
PAYS = {
    "Austria": "AT", "Belgium (Flemish)": "BE", "Bulgaria": "BG", "Croatia": "HR",
    "Cyprus": "CY", "Czech Republic": "CZ", "Denmark": "DK", "Estonia": "EE", "Finland": "FI",
    "France": "FR", "Germany": "DE", "Greece": "EL", "Hungary": "HU", "Ireland": "IE",
    "Italy": "IT", "Latvia": "LV", "Lithuania": "LT", "Luxembourg": "LU", "Malta": "MT",
    "Netherlands": "NL", "Poland": "PL", "Portugal": "PT", "Romania": "RO",
    "Slovak Republic": "SK", "Slovenia": "SI", "Spain": "ES", "Sweden": "SE",
}
SOUS_NATIONAUX = {"Belgium (French)": "BE_FR"}
UE27 = sorted(PAYS.values())

# Notes de couverture vérifiées dans les rapports (annexes « population » et notes des tableaux).
NOTES_COUVERTURE = {
    ("BE", None): "Belgique : Communauté flamande uniquement (pas de valeur nationale)",
    ("BE_FR", None): "Belgique : Fédération Wallonie-Bruxelles (Communauté française) uniquement",
    ("LT", 2003): "élèves scolarisés en lituanien uniquement (renvoi 1)",
    ("LT", 2007): "élèves scolarisés en lituanien uniquement, 93 % de la population (renvoi 1)",
    ("LT", 2011): "élèves scolarisés en lituanien uniquement, 93 % de la population (renvoi 1)",
    ("LV", 2007): "élèves scolarisés en letton uniquement, 72 % de la population (renvoi 1) ; "
                  "non repris dans les tendances TIMSS ultérieures",
    ("LV", 1995): "écoles de langue lettone uniquement (Latvia LSS)",
    ("SI", 2003): "élèves ayant 3 ou 4 années de scolarité selon les écoles (transition vers le primaire "
                  "en 9 ans), âge moyen 9,8 ans",
    ("SI", 1995): "la série de tendance retient la classe inférieure de 1995 (3e année, âge moyen 9,9 ans, "
                  "comme la population 2003) : 488 en maths sur l'échelle d'origine 1995, contre 552 pour la "
                  "4e année ; rupture de population cible",
    ("PL", 2011): "classe nationale « Grade 3 » (4e année de scolarité formelle), âge moyen 9,9 ans ; "
                  "non reprise dans les tendances TIMSS ultérieures",
    ("LV", 2003): "toutes écoles (la série de tendance 1995-2003 du rapport 2003 porte sur les seules écoles "
                  "de langue lettone : 533 en maths)",
}

# --------------------------------------------------------------------------------------------
# Fichiers sources. `cle` identifie le fichier dans le code ; `fichier` est le chemin local
# relatif à dossier_brut.
# --------------------------------------------------------------------------------------------
_T23 = "https://timss2023.org/wp-content/uploads/2024/11/"
_T19 = "https://timss2019.org/reports/wp-content/uploads/download/achievement/"
_T15 = "https://timssandpirls.bc.edu/timss2015/international-results/wp-content/uploads/filebase/"
_T11 = "https://timssandpirls.bc.edu/timss2011/downloads/"
_T07 = "https://timssandpirls.bc.edu/TIMSS2007/PDF/"
_T03 = "https://timssandpirls.bc.edu/PDF/t03_download/"
_WB = ("https://api.worldbank.org/v2/country/{pays}/indicator/{ind}"
       "?format=json&per_page=2000&source=12")

FICHIERS = {
    # 2023 (Excel)
    "23_m_moy": (_T23 + "1-1-1_ach-g4m-dist.xlsx", "2023/1-1-1_ach-g4m-dist.xlsx", "Exhibit 1.1.1"),
    "23_s_moy": (_T23 + "2-1-1_ach-g4s-dist.xlsx", "2023/2-1-1_ach-g4s-dist.xlsx", "Exhibit 2.1.1"),
    "23_m_niv": (_T23 + "1-1-4_ach-g4m-bmk-dist.xlsx", "2023/1-1-4_ach-g4m-bmk-dist.xlsx", "Exhibit 1.1.4"),
    "23_s_niv": (_T23 + "2-1-4_ach-g4s-bmk-dist.xlsx", "2023/2-1-4_ach-g4s-bmk-dist.xlsx", "Exhibit 2.1.4"),
    "23_m_moy_tend": (_T23 + "1-1-10_ach-g4m-trend-table.xlsx", "2023/1-1-10_ach-g4m-trend-table.xlsx", "Exhibit 1.1.10"),
    "23_s_moy_tend": (_T23 + "2-1-10_ach-g4s-trend-table.xlsx", "2023/2-1-10_ach-g4s-trend-table.xlsx", "Exhibit 2.1.10"),
    "23_m_niv_tend": (_T23 + "1-1-12_ach-g4m-bmk-trend.xlsx", "2023/1-1-12_ach-g4m-bmk-trend.xlsx", "Exhibit 1.1.12"),
    "23_s_niv_tend": (_T23 + "2-1-12_ach-g4s-bmk-trend.xlsx", "2023/2-1-12_ach-g4s-bmk-trend.xlsx", "Exhibit 2.1.12"),
    # 2019 (Excel)
    "19_m_moy": (_T19 + "1_1-2_achievement-results-M4.xlsx", "2019/1_1-2_achievement-results-M4.xlsx", "Exhibit 1.1"),
    "19_s_moy": (_T19 + "2_1-2_achievement-results-S4.xlsx", "2019/2_1-2_achievement-results-S4.xlsx", "Exhibit 2.1"),
    "19_m_niv": (_T19 + "1-8_benchmarks-results-M4.xlsx", "2019/1-8_benchmarks-results-M4.xlsx", "Exhibit 1.8"),
    "19_s_niv": (_T19 + "2-8_benchmarks-results-S4.xlsx", "2019/2-8_benchmarks-results-S4.xlsx", "Exhibit 2.8"),
    "19_m_moy_tend": (_T19 + "1_3-4_achievement-trends-M4.xlsx", "2019/1_3-4_achievement-trends-M4.xlsx", "Exhibit 1.4"),
    "19_s_moy_tend": (_T19 + "2_3-4_achievement-trends-S4.xlsx", "2019/2_3-4_achievement-trends-S4.xlsx", "Exhibit 2.4"),
    "19_m_niv_tend": (_T19 + "1-9_benchmarks-trends-M4.xlsx", "2019/1-9_benchmarks-trends-M4.xlsx", "Exhibit 1.9"),
    "19_s_niv_tend": (_T19 + "2-9_benchmarks-trends-S4.xlsx", "2019/2-9_benchmarks-trends-S4.xlsx", "Exhibit 2.9"),
    # 2015 (Excel 97)
    "15_m_moy": (_T15 + "mathematics/1.-student-achievement/1_1_math-distribution-of-mathematics-achievement-grade-4.xls",
                 "2015/1_1_math-distribution-of-mathematics-achievement-grade-4.xls", "Exhibit 1.1 (math.)"),
    "15_s_moy": (_T15 + "science/1.-student-achievement/1_1_science-distribution-of-science-achievement-grade-4.xls",
                 "2015/1_1_science-distribution-of-science-achievement-grade-4.xls", "Exhibit 1.1 (sciences)"),
    "15_m_niv": (_T15 + "mathematics/2.-performance-at-international-benchmarks/"
                 "2_2_math-performance-at-the-international-benchmarks-of-mathematics-achievement-grade-4.xls",
                 "2015/2_2_math-performance-at-the-international-benchmarks-of-mathematics-achievement-grade-4.xls",
                 "Exhibit 2.2 (math.)"),
    "15_s_niv": (_T15 + "science/2.-performance-at-international-benchmarks/"
                 "2_2_science-performance-at-the-international-benchmarks-of-science-achievement-grade-4.xls",
                 "2015/2_2_science-performance-at-the-international-benchmarks-of-science-achievement-grade-4.xls",
                 "Exhibit 2.2 (sciences)"),
    # 2011, 2007, 2003 (PDF, chapitres des rapports internationaux)
    "11_m_ch1": (_T11 + "T11_IR_M_Chapter1.pdf", "2011/T11_IR_M_Chapter1.pdf", ""),
    "11_m_ch2": (_T11 + "T11_IR_M_Chapter2.pdf", "2011/T11_IR_M_Chapter2.pdf", ""),
    "11_s_ch1": (_T11 + "T11_IR_S_Chapter1.pdf", "2011/T11_IR_S_Chapter1.pdf", ""),
    "11_s_ch2": (_T11 + "T11_IR_S_Chapter2.pdf", "2011/T11_IR_S_Chapter2.pdf", ""),
    "07_m_ch1": (_T07 + "T07_M_IR_Chapter1.pdf", "2007/T07_M_IR_Chapter1.pdf", ""),
    "07_m_ch2": (_T07 + "T07_M_IR_Chapter2.pdf", "2007/T07_M_IR_Chapter2.pdf", ""),
    "07_s_ch1": (_T07 + "T07_S_IR_Chapter1.pdf", "2007/T07_S_IR_Chapter1.pdf", ""),
    "07_s_ch2": (_T07 + "T07_S_IR_Chapter2.pdf", "2007/T07_S_IR_Chapter2.pdf", ""),
    "03_m_ch1": (_T03 + "T03_M_Chap1.pdf", "2003/T03_M_Chap1.pdf", ""),
    "03_m_ch2": (_T03 + "T03_M_Chap2.pdf", "2003/T03_M_Chap2.pdf", ""),
    "03_s_ch1": (_T03 + "T03_S_Chap1.pdf", "2003/T03_S_Chap1.pdf", ""),
    "03_s_ch2": (_T03 + "T03_S_Chap2.pdf", "2003/T03_S_Chap2.pdf", ""),
    # Annexes consultées pour les notes de couverture (non lues par le code)
    "doc_07_annexeA": (_T07 + "T07_M_IR_AppendixA.pdf", "annexes/T07_M_IR_AppendixA.pdf", ""),
    "doc_11_annexeC": (_T11 + "T11_IR_M_AppendixC.pdf", "annexes/T11_IR_M_AppendixC.pdf", ""),
    "doc_03_annexeA": (_T03 + "T03_M_AppA.pdf", "annexes/T03_M_AppA.pdf", ""),
    "doc_19_annexeB": ("https://timss2019.org/reports/wp-content/themes/timssandpirls/download-center/"
                       "appendices/T19_AppB_population-samples.pdf", "annexes/T19_AppB_population-samples.pdf", ""),
    "doc_95_maths_ch1": ("https://timssandpirls.bc.edu/timss1995i/TIMSSPDF/am1chap.pdf", "1995/am1chap.pdf",
                         "échelle d'origine 1995, contrôle seulement"),
}
_ISO3 = "AUT;BEL;BGR;HRV;CYP;CZE;DNK;EST;FIN;FRA;DEU;GRC;HUN;IRL;ITA;LVA;LTU;LUX;MLT;NLD;POL;PRT;ROU;SVK;SVN;ESP;SWE"
_WB_IND = {
    "LO.TIMSS.MAT4": "timss4_maths", "LO.TIMSS.SCI4": "timss4_sciences",
    "LO.TIMSS.MAT4.ADV": "timss4_avance_maths", "LO.TIMSS.SCI4.ADV": "timss4_avance_sciences",
    "LO.TIMSS.MAT4.BL": "timss4_bas_maths", "LO.TIMSS.SCI4.BL": "timss4_bas_sciences",
}
for _ind in _WB_IND:
    FICHIERS["wb_" + _ind] = (_WB.format(pays=_ISO3, ind=_ind), f"worldbank/{_ind}.json", "API Banque mondiale")

# Pages des PDF (index à partir de 0) et chaîne témoin qui doit y figurer (valeur de la 1re ligne
# du tableau 4e année) : si le PDF change, l'extraction s'arrête au lieu de lire la mauvaise page.
PAGES_PDF = {
    # (cycle, matière, type): (clé fichier, page, témoin, libellé exhibit)
    (2011, "maths", "moy"): ("11_m_ch1", 5, "606 (3.2)", "Exhibit 1.1"),
    (2011, "sciences", "moy"): ("11_s_ch1", 5, "587 (2.0)", "Exhibit 1.1"),
    (2011, "maths", "niv"): ("11_m_ch2", 5, "43 (2.0)", "Exhibit 2.2"),
    (2011, "sciences", "niv"): ("11_s_ch2", 5, "33 (1.7)", "Exhibit 2.2"),
    (2007, "maths", "moy"): ("07_m_ch1", 3, "607 (3.6)", "Exhibit 1.1"),
    (2007, "sciences", "moy"): ("07_s_ch1", 3, "587 (4.1)", "Exhibit 1.1"),
    (2007, "maths", "niv"): ("07_m_ch2", 5, "41 (2.1)", "Exhibit 2.2"),
    (2007, "sciences", "niv"): ("07_s_ch2", 5, "36 (1.9)", "Exhibit 2.2"),
    (2003, "maths", "moy"): ("03_m_ch1", 5, "594 (5.6)", "Exhibit 1.1"),
    (2003, "sciences", "moy"): ("03_s_ch1", 4, "565 (5.5)", "Exhibit 1.1"),
    (2003, "maths", "niv"): ("03_m_ch2", 10, "38 (2.9)", "Exhibit 2.2"),
    (2003, "sciences", "niv"): ("03_s_ch2", 10, "25 (2.4)", "Exhibit 2.2"),
    # tendances 1995-2003 de 4e année dans le rapport 2003 (Lettonie LSS)
    (2003, "maths", "moy_tend"): ("03_m_ch1", 15, "Latvia (LSS)", "Exhibit 1.3"),
    (2003, "sciences", "moy_tend"): ("03_s_ch1", 14, "Latvia (LSS)", "Exhibit 1.3"),
    (2003, "maths", "niv_tend"): ("03_m_ch2", 13, "Latvia (LSS)", "Exhibit 2.4"),
    (2003, "sciences", "niv_tend"): ("03_s_ch2", 13, "Latvia (LSS)", "Exhibit 2.4"),
}

MATIERES = ("maths", "sciences")
_FIN_TABLEAU = re.compile(r"Benchmarking Participants|Sixth Grade Participants", re.I)
_RENVOIS = "0-9†‡≡¿ψΨЖø¶§"


# ============================================================================================
# Téléchargement
# ============================================================================================
def _get(url: str, timeout: int = 300) -> bytes:
    """GET HTTPS via urllib (proxy de l'environnement, vérification TLS par défaut)."""
    import urllib.request

    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (compatible; extraction-timss/1.0)"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def telecharger(dossier_brut=DOSSIER_BRUT_DEFAUT, forcer: bool = False) -> pd.DataFrame:
    """Télécharge les fichiers sources dans `dossier_brut` (TLS vérifié) et écrit manifeste.csv.

    Les fichiers déjà présents ne sont pas retéléchargés (sauf forcer=True).
    """
    dossier_brut = Path(dossier_brut)
    lignes = []
    for cle, (url, rel, _) in FICHIERS.items():
        chemin = dossier_brut / rel
        chemin.parent.mkdir(parents=True, exist_ok=True)
        if forcer or not chemin.exists() or chemin.stat().st_size == 0:
            if cle.startswith("wb_"):
                # l'API pagine : on fusionne toutes les pages dans un seul JSON
                pages, p, n = [], 1, 1
                while p <= n:
                    meta, data = json.loads(_get(url + f"&page={p}", 120))
                    n = meta["pages"]
                    pages.extend(data or [])
                    p += 1
                chemin.write_text(json.dumps([meta, pages]), encoding="utf-8")
            else:
                chemin.write_bytes(_get(url))
        contenu = chemin.read_bytes()
        lignes.append({"cle": cle, "url": url, "fichier": rel, "octets": len(contenu),
                       "sha256": hashlib.sha256(contenu).hexdigest()})
    man = pd.DataFrame(lignes)
    man["verifie_le"] = date.today().isoformat()
    man.to_csv(dossier_brut / "manifeste.csv", index=False)
    return man


# ============================================================================================
# Lecture des tableurs
# ============================================================================================
def _lire_tableur(chemin: Path) -> list[list[list]]:
    """Renvoie, pour chaque feuille, la liste des lignes (valeurs brutes)."""
    if chemin.suffix == ".xls":
        import xlrd
        wb = xlrd.open_workbook(str(chemin))
        return [[ws.row_values(i) for i in range(ws.nrows)] for ws in wb.sheets()]
    import openpyxl
    wb = openpyxl.load_workbook(chemin, data_only=True, read_only=True)
    return [[list(r) for r in ws.iter_rows(values_only=True)] for ws in wb.worksheets]


def _txt(v) -> str:
    return "" if v is None else str(v).strip()


def _num(v):
    if isinstance(v, (int, float)) and not isinstance(v, bool):
        return float(v)
    return None


def _code_pays(nom: str, sous_nationaux: bool):
    nom = re.sub(r"\s+", " ", nom).strip()
    if nom in PAYS:
        return PAYS[nom]
    if sous_nationaux and nom in SOUS_NATIONAUX:
        return SOUS_NATIONAUX[nom]
    return None


def _renvois(v) -> str:
    s = _txt(v)
    if isinstance(v, float) and v.is_integer():
        s = str(int(v))
    return re.sub(r"\s+", " ", s)


def _tableur_transversal(lignes: list[list], genre: str, sous_nationaux: bool):
    """Tableau d'un cycle (une ligne par pays). genre = 'moy' ou 'niv'.

    Renvoie {code: dict(moy=..., moy_se=..., avance=..., avance_se=..., bas_atteint=..., renvois=...)}.
    """
    h = next(i for i, r in enumerate(lignes) if any(_txt(c) == "Country" for c in r))
    c_pays = next(j for j, c in enumerate(lignes[h]) if _txt(c) == "Country")
    entete = lignes[h:h + 3]

    def colonne(motif):
        for r in entete:
            for j, c in enumerate(r):
                if re.match(motif, _txt(c), re.I):
                    return j
        raise ValueError(f"colonne {motif!r} introuvable")

    cols = ({"moy": colonne(r"Average")} if genre == "moy"
            else {"avance": colonne(r"Advanced"), "bas_atteint": colonne(r"Low")})
    res = {}
    for r in lignes[h + 1:]:
        if any(_FIN_TABLEAU.search(_txt(c)) for c in r):
            break
        if len(r) <= c_pays:
            continue
        code = _code_pays(_txt(r[c_pays]), sous_nationaux)
        if not code:
            continue
        d = {"renvois": _renvois(r[c_pays - 1]) if c_pays else ""}
        for k, j in cols.items():
            d[k], d[k + "_se"] = _num(r[j]), _num(r[j + 1])
        res[code] = d
    return res


def _tableur_tendance_moy(feuilles, sous_nationaux: bool):
    """Tableau de tendance des moyennes : ligne pays puis une ligne par année. -> {(code, an): (val, renvois)}"""
    res = {}
    for lignes in feuilles:
        courant = None
        for r in lignes:
            if len(r) < 5:
                continue
            if any(_FIN_TABLEAU.search(_txt(c)) for c in r):
                courant = None
                continue
            nom = r[2]
            if isinstance(nom, str) and nom.strip() and not nom.strip().isdigit():
                courant = _code_pays(nom, sous_nationaux)
                continue
            an = int(nom) if _num(nom) is not None or (isinstance(nom, str) and nom.strip().isdigit()) else None
            if courant and an and _num(r[4]) is not None:
                res.setdefault((courant, an), (_num(r[4]), _renvois(r[1])))
        if res:
            return res
    return res


def _tableur_tendance_niv(feuilles, sous_nationaux: bool):
    """Tableau de tendance des niveaux : colonnes (niveau, année). -> {(code, an): {avance, bas_atteint}}"""
    for lignes in feuilles:
        iy = next((i for i, r in enumerate(lignes)
                   if sum(1 for c in r if _num(c) is not None and 1995 <= _num(c) <= 2023
                          or (isinstance(c, str) and re.fullmatch(r"(1995|20[0-2]\d)", c.strip()))) >= 3), None)
        if iy is None:
            continue
        annees, niveaux = {}, {}
        dernier = None
        for j, c in enumerate(lignes[iy]):
            t = _txt(c)
            if re.fullmatch(r"(1995|20[0-2]\d)(\.0)?", t):
                dernier = int(float(t))
            annees[j] = dernier
        for i in range(max(0, iy - 3), min(len(lignes), iy + 2)):
            if i == iy:
                continue
            if any(re.match(r"(Advanced|Low)", _txt(c)) for c in lignes[i]):
                dernier = None
                for j, c in enumerate(lignes[i]):
                    t = _txt(c)
                    m = re.match(r"(Advanced|High|Intermediate|Low)", t)
                    if m:
                        dernier = m.group(1)
                    niveaux[j] = dernier
                break
        res = {}
        for r in lignes[iy + 1:]:
            if any(_FIN_TABLEAU.search(_txt(c)) for c in r):
                break
            if len(r) < 3:
                continue
            code = _code_pays(_txt(r[2]), sous_nationaux)
            if not code:
                continue
            for j, c in enumerate(r):
                v = _num(c)
                if v is None or j < 4:
                    continue
                niv, an = niveaux.get(j), annees.get(j)
                cle = {"Advanced": "avance", "Low": "bas_atteint"}.get(niv)
                if cle and an:
                    res.setdefault((code, an), {})[cle] = v
        return res
    return {}


# ============================================================================================
# Lecture des PDF (reconstitution des lignes par la position verticale des mots)
# ============================================================================================
def _lignes_pdf(chemin: Path, page: int, temoin: str) -> list[str]:
    import pymupdf

    with pymupdf.open(chemin) as doc:
        pg = doc[page]
        texte = pg.get_text()
        if temoin not in texte:
            raise ValueError(f"{chemin.name} p.{page}: témoin {temoin!r} absent (mise en page modifiée ?)")
        mots = pg.get_text("words")
    mots.sort(key=lambda w: ((w[1] + w[3]) / 2, w[0]))
    groupes: list[list] = []
    for w in mots:
        yc = (w[1] + w[3]) / 2
        if groupes and abs(groupes[-1][0] - yc) <= 3.0:
            groupes[-1][1].append(w)
        else:
            groupes.append([yc, [w]])
    return [" ".join(w[4] for w in sorted(ws, key=lambda w: w[0])) for _, ws in groupes]


_PAIRE = re.compile(r"(?<![\d.])(\d{1,3}) \((\d+\.\d)\)")


def _cherche_ligne(ligne: str, nom: str):
    """Si `ligne` commence (après les renvois) par le pays `nom`, renvoie (renvois, reste)."""
    m = re.match(rf"^(?P<renv>[{_RENVOIS}\s]*?)\s*{re.escape(nom)}(?P<reste>(\s.*)?)$", ligne)
    if not m:
        return None
    reste = m.group("reste") or ""
    if re.match(r"\s*\([A-Za-z]", reste):  # ex. « Latvia (LSS) » quand on cherche « Latvia »
        return None
    return re.sub(r"\s+", " ", m.group("renv")).strip(), reste


def _pdf_transversal(lignes: list[str], genre: str, sous_nationaux: bool):
    noms = dict(PAYS, **(SOUS_NATIONAUX if sous_nationaux else {}))
    res = {}
    for ligne in lignes:
        if _FIN_TABLEAU.search(ligne):
            break
        for nom, code in noms.items():
            t = _cherche_ligne(ligne, nom)
            if not t:
                continue
            paires = [(float(a), float(b)) for a, b in _PAIRE.findall(t[1])]
            if genre == "moy" and paires:
                res[code] = {"renvois": t[0], "moy": paires[0][0], "moy_se": paires[0][1]}
            elif genre == "niv" and len(paires) >= 4:
                res[code] = {"renvois": t[0], "avance": paires[0][0], "avance_se": paires[0][1],
                             "bas_atteint": paires[3][0], "bas_atteint_se": paires[3][1]}
            break
    return res


def _pdf_tendance_2003_lettonie(lignes: list[str], genre: str):
    """Valeurs 1995 de « Latvia (LSS) » dans les tableaux de tendance 4e année du rapport 2003."""
    for k, ligne in enumerate(lignes):
        if not ligne.startswith("Latvia (LSS)"):
            continue
        if genre == "moy":
            for suite in lignes[k + 1:k + 4]:
                m = re.match(r"^(?:##\s*)?1995\s+(\d{3}) \((\d+\.\d)\)", suite)
                if m:
                    return {"moy": float(m.group(1)), "moy_se": float(m.group(2))}
        else:
            p = _PAIRE.findall(ligne)
            if len(p) == 8:  # 2003/1995 pour avancé, élevé, intermédiaire, bas
                return {"avance": float(p[1][0]), "avance_se": float(p[1][1]),
                        "bas_atteint": float(p[7][0]), "bas_atteint_se": float(p[7][1])}
    raise ValueError("Latvia (LSS) introuvable dans le tableau de tendance 2003")


# ============================================================================================
# Extraction
# ============================================================================================
def _ref(cle: str, exhibit: str = "") -> str:
    url, _, ex = FICHIERS[cle]
    return f"{exhibit or ex} – {url}".strip(" –")


def _note(code: str, annee: int, renvois: str = "", extra: str = "") -> str:
    morceaux = []
    for k in ((code, None), (code, annee)):
        if k in NOTES_COUVERTURE:
            morceaux.append(NOTES_COUVERTURE[k])
    if renvois:
        morceaux.append(f"renvois TIMSS : {renvois}")
    if extra:
        morceaux.append(extra)
    return " ; ".join(morceaux)


def _lignes_sortie(code, annee, matiere, d, source, renvois="", extra=""):
    """Transforme un dict extrait en lignes du format long."""
    out = []
    if d.get("moy") is not None:
        se = f"e.-t. {d['moy_se']:g}" if d.get("moy_se") is not None else ""
        out.append((code, f"timss4_{matiere}", annee, d["moy"], source,
                    _note(code, annee, renvois, "; ".join(x for x in (se, extra) if x))))
    if d.get("avance") is not None:
        se = f"e.-t. {d['avance_se']:g}" if d.get("avance_se") is not None else ""
        out.append((code, f"timss4_avance_{matiere}", annee, d["avance"], source,
                    _note(code, annee, renvois, "; ".join(x for x in (se, extra) if x))))
    if d.get("bas_atteint") is not None:
        txt = "100 - % atteignant 400 (pourcentage publié arrondi)"
        out.append((code, f"timss4_bas_{matiere}", annee, round(100 - d["bas_atteint"], 6), source,
                    _note(code, annee, renvois, "; ".join(x for x in (txt, extra) if x))))
    return out


def _fusion(moy: dict, niv: dict) -> dict:
    res = {}
    for src in (moy, niv):
        for code, d in src.items():
            cible = res.setdefault(code, {})
            for k, v in d.items():
                if k == "renvois":
                    if v and v not in cible.get("renvois", ""):
                        cible["renvois"] = (cible.get("renvois", "") + " / " + v).strip(" /") if cible.get("renvois") else v
                else:
                    cible[k] = v
    return res


def _cycle_tableur(dossier, annee, sous_nationaux):
    pref = str(annee)[2:]
    out = []
    for mat, m in (("maths", "m"), ("sciences", "s")):
        k_moy, k_niv = f"{pref}_{m}_moy", f"{pref}_{m}_niv"
        moy = _tableur_transversal(_lire_tableur(dossier / FICHIERS[k_moy][1])[0], "moy", sous_nationaux)
        niv = _tableur_transversal(_lire_tableur(dossier / FICHIERS[k_niv][1])[0], "niv", sous_nationaux)
        for code, d in _fusion(moy, niv).items():
            renv = d.get("renvois", "")
            out += _lignes_sortie(code, annee, mat, {k: v for k, v in d.items() if k.startswith("moy")},
                                  f"TIMSS {annee} International Results, {_ref(k_moy)}", renv)
            out += _lignes_sortie(code, annee, mat, {k: v for k, v in d.items() if not k.startswith("moy")},
                                  f"TIMSS {annee} International Results, {_ref(k_niv)}", renv)
    return out


def _cycle_pdf(dossier, annee, sous_nationaux):
    out = []
    for mat in MATIERES:
        for genre in ("moy", "niv"):
            cle, page, temoin, exhibit = PAGES_PDF[(annee, mat, genre)]
            lignes = _lignes_pdf(dossier / FICHIERS[cle][1], page, temoin)
            for code, d in _pdf_transversal(lignes, genre, sous_nationaux).items():
                src = f"TIMSS {annee} International Results in {'Mathematics' if mat == 'maths' else 'Science'}, " \
                      f"{exhibit}, p. {page + 1} du PDF – {FICHIERS[cle][0]}"
                out += _lignes_sortie(code, annee, mat, d, src, d.get("renvois", ""))
    return out


def _cycle_1995(dossier, sous_nationaux):
    """1995 : valeurs réétalonnées publiées dans les tableaux de tendance (2023, à défaut 2019,
    à défaut 2003 pour la Lettonie LSS), puis Banque mondiale pour les pays restants."""
    out, pris = [], set()
    for mat, m in (("maths", "m"), ("sciences", "s")):
        for cyc in ("23", "19"):
            k_moy, k_niv = f"{cyc}_{m}_moy_tend", f"{cyc}_{m}_niv_tend"
            moy = _tableur_tendance_moy(_lire_tableur(dossier / FICHIERS[k_moy][1]), sous_nationaux)
            niv = _tableur_tendance_niv(_lire_tableur(dossier / FICHIERS[k_niv][1]), sous_nationaux)
            rapport = f"TIMSS 20{cyc} International Results (tableau de tendance)"
            for (code, an), (v, renv) in moy.items():
                if an == 1995 and (code, mat, "moy") not in pris:
                    pris.add((code, mat, "moy"))
                    out += _lignes_sortie(code, 1995, mat, {"moy": v}, f"{rapport}, {_ref(k_moy)}", renv,
                                          "échelle 1995 réétalonnée pour les tendances")
            for (code, an), d in niv.items():
                if an == 1995 and (code, mat, "niv") not in pris:
                    pris.add((code, mat, "niv"))
                    out += _lignes_sortie(code, 1995, mat, d, f"{rapport}, {_ref(k_niv)}", "",
                                          "échelle 1995 réétalonnée pour les tendances")
        # Lettonie (écoles de langue lettone) : rapport 2003
        for genre in ("moy", "niv"):
            if ("LV", mat, genre) in pris:
                continue
            cle, page, temoin, exhibit = PAGES_PDF[(2003, mat, genre + "_tend")]
            d = _pdf_tendance_2003_lettonie(_lignes_pdf(dossier / FICHIERS[cle][1], page, temoin), genre)
            pris.add(("LV", mat, genre))
            src = (f"TIMSS 2003 International Results in {'Mathematics' if mat == 'maths' else 'Science'} "
                   f"(tendances 1995-2003), {exhibit}, p. {page + 1} du PDF – {FICHIERS[cle][0]}")
            out += _lignes_sortie("LV", 1995, mat, d, src, "", "échelle 1995 réétalonnée pour les tendances")
    # Pays de 1995 absents de tous les tableaux de tendance : Banque mondiale (Grèce)
    wb = _banque_mondiale(dossier)
    pays_1995 = {r[0] for r in out}
    for (code, ind, an), v in sorted(wb.items()):
        if an == 1995 and code not in pays_1995:
            src = f"Banque mondiale, EdStats, {_inv_wb(ind)} – https://api.worldbank.org/v2/indicator/{_inv_wb(ind)}"
            note = ("absent des tableaux publiés par l'ISC (pas de tendance) ; valeur calculée par la "
                    "Banque mondiale à partir des microdonnées IEA, cohérente avec l'échelle de tendance "
                    "pour les autres pays de 1995 (voir notes) ; à utiliser avec prudence")
            out.append((code, ind, 1995, round(v, 1), src, note))
    return out


def _inv_wb(ind):
    return next(k for k, v in _WB_IND.items() if v == ind)


def _banque_mondiale(dossier) -> dict:
    """{(code ISO2, indicateur, année): valeur} depuis les JSON EdStats téléchargés."""
    iso3 = dict(zip(_ISO3.split(";"), ["AT", "BE", "BG", "HR", "CY", "CZ", "DK", "EE", "FI", "FR", "DE",
                                       "EL", "HU", "IE", "IT", "LV", "LT", "LU", "MT", "NL", "PL", "PT",
                                       "RO", "SK", "SI", "ES", "SE"]))
    res = {}
    for ind_wb, ind in _WB_IND.items():
        f = Path(dossier) / FICHIERS["wb_" + ind_wb][1]
        if not f.exists():
            continue
        _, data = json.loads(f.read_text(encoding="utf-8"))
        for x in data:
            if x.get("value") is not None and x["countryiso3code"] in iso3:
                res[(iso3[x["countryiso3code"]], ind, int(x["date"]))] = float(x["value"])
    return res


def extraire(dossier_brut=DOSSIER_BRUT_DEFAUT, sous_nationaux: bool = False) -> pd.DataFrame:
    """Extrait les indicateurs TIMSS 4e année des fichiers de `dossier_brut`.

    sous_nationaux=True ajoute la Communauté française de Belgique (code BE_FR, 2023).
    """
    dossier = Path(dossier_brut)
    lignes = []
    for annee in (2023, 2019, 2015):
        lignes += _cycle_tableur(dossier, annee, sous_nationaux)
    for annee in (2011, 2007, 2003):
        lignes += _cycle_pdf(dossier, annee, sous_nationaux)
    lignes += _cycle_1995(dossier, sous_nationaux)
    df = pd.DataFrame(lignes, columns=COLONNES)
    df["annee"] = df["annee"].astype(int)
    if df.duplicated(["pays", "indicateur", "annee"]).any():
        raise ValueError("doublons pays/indicateur/année :\n"
                         + df[df.duplicated(["pays", "indicateur", "annee"], keep=False)].to_string())
    return df.sort_values(["pays", "indicateur", "annee"]).reset_index(drop=True)


# ============================================================================================
# Contrôles
# ============================================================================================
ATTENDUS = [  # (pays, indicateur, année, valeur attendue d'après la commande)
    ("FR", "timss4_maths", 2019, 485), ("FR", "timss4_sciences", 2019, 488),
    ("FR", "timss4_maths", 2023, 484),
]


def controles(df: pd.DataFrame, dossier_brut=DOSSIER_BRUT_DEFAUT) -> pd.DataFrame:
    """Compare la base aux valeurs attendues, aux tableaux de tendance 2019/2023 et à la Banque mondiale.

    Renvoie un DataFrame (controle, pays, indicateur, annee, base, reference, ecart).
    """
    dossier = Path(dossier_brut)
    base = df.set_index(["pays", "indicateur", "annee"])["valeur"]
    lignes = []
    for p, i, a, v in ATTENDUS:
        lignes.append(("valeur attendue", p, i, a, base.get((p, i, a)), v))
    # tableaux de tendance (valeurs republiées dans les rapports 2019 et 2023)
    for cyc in ("23", "19"):
        for mat, m in (("maths", "m"), ("sciences", "s")):
            moy = _tableur_tendance_moy(_lire_tableur(dossier / FICHIERS[f"{cyc}_{m}_moy_tend"][1]), False)
            niv = _tableur_tendance_niv(_lire_tableur(dossier / FICHIERS[f"{cyc}_{m}_niv_tend"][1]), False)
            for (p, a), (v, _) in moy.items():
                lignes.append((f"tendance 20{cyc}", p, f"timss4_{mat}", a, base.get((p, f"timss4_{mat}", a)), v))
            for (p, a), d in niv.items():
                if "avance" in d:
                    lignes.append((f"tendance 20{cyc}", p, f"timss4_avance_{mat}", a,
                                   base.get((p, f"timss4_avance_{mat}", a)), d["avance"]))
                if "bas_atteint" in d:
                    lignes.append((f"tendance 20{cyc}", p, f"timss4_bas_{mat}", a,
                                   base.get((p, f"timss4_bas_{mat}", a)), 100 - d["bas_atteint"]))
    src = df.set_index(["pays", "indicateur", "annee"])["source"]
    for (p, i, a), v in _banque_mondiale(dossier).items():
        if str(src.get((p, i, a), "")).startswith("Banque mondiale"):
            continue  # valeur reprise de la Banque mondiale : pas d'auto-contrôle
        lignes.append(("Banque mondiale", p, i, a, base.get((p, i, a)), v))
    c = pd.DataFrame(lignes, columns=["controle", "pays", "indicateur", "annee", "base", "reference"])
    c = c[c["pays"].isin(UE27)]
    c["ecart"] = c["base"] - c["reference"]
    return c


def _resume_controles(c: pd.DataFrame) -> str:
    out = []
    for nom, g in c.groupby("controle", sort=False):
        comp = g.dropna(subset=["base"])
        ecarts = comp[comp["ecart"].abs() >= 0.5]
        absents = g[g["base"].isna()]
        out.append(f"- {nom} : {len(comp)} valeurs comparées, {len(ecarts)} écarts >= 0,5 ; "
                   f"{len(absents)} valeurs de référence absentes de la base")
        if len(ecarts):
            out.append(ecarts.sort_values(["indicateur", "pays", "annee"]).to_string(index=False))
        if len(absents) and nom != "Banque mondiale":
            out.append("  absentes : " + ", ".join(f"{r.pays} {r.indicateur} {r.annee}"
                                                    for r in absents.itertuples()))
    return "\n".join(out)


if __name__ == "__main__":
    dossier = Path(sys.argv[1]) if len(sys.argv) > 1 else DOSSIER_BRUT_DEFAUT
    telecharger(dossier)
    df = extraire(dossier)
    df.to_csv(SORTIE_CSV, index=False, encoding="utf-8")
    print(f"{len(df)} lignes écrites dans {SORTIE_CSV}")
    print(df.pivot_table(index="pays", columns=["annee"], values="valeur",
                         aggfunc="count", fill_value=0).to_string())
    print(_resume_controles(controles(df, dossier)))
