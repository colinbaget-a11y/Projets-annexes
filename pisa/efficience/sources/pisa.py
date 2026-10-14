"""PISA 2000-2025 : indicateurs par pays (UE-27) calculés depuis les microdonnées OCDE.

Usage
-----
    python3 -I pisa.py --telecharger DOSSIER_BRUT   # télécharge les fichiers élèves
    python3 -I pisa.py DOSSIER_BRUT                 # calcule et écrit pisa.csv à côté du module

Fonctions publiques : ``telecharger(dossier_brut)`` et ``extraire(dossier_brut)``.
Voir ``pisa_notes.md`` pour les définitions, seuils, ruptures de série et contrôles.
"""
from __future__ import annotations

import concurrent.futures as cf
import os
import re
import shutil
import subprocess
import sys
import time
import urllib.request
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd

# --------------------------------------------------------------------------------------
# 1. Fichiers sources (URL officielles ; 2000-2012 via copies Internet Archive des .zip OCDE)
# --------------------------------------------------------------------------------------
OECD_OLD = "https://www.oecd.org/content/dam/oecd/en/data/datasets/pisa"
FICHIERS = {
    2025: {"stu": "https://webfs.oecd.org/pisa2022/2025/CY09_MS_STU_PUF.zip"},
    2022: {"stu": "https://webfs.oecd.org/pisa2022/STU_QQQ_SPSS.zip",
           "crt": "https://webfs.oecd.org/pisa2022/CRT_SPSS.zip"},
    2018: {"stu": "https://webfs.oecd.org/pisa2018/SPSS_STU_QQQ.zip"},
    2015: {"stu": "https://webfs.oecd.org/pisa/PUF_SPSS_COMBINED_CMB_STU_QQQ.zip"},
    2012: {"stu": "https://web.archive.org/web/2023id_/https://www.oecd.org/pisa/pisaproducts/INT_STU12_DEC03.zip",
           "syntaxe": OECD_OLD + "/pisa-2012-datasets/main-survey/sas-and-spss-control-files/"
                                 "SPSS%20syntax%20to%20read%20in%20student%20questionnaire%20data%20file.txt"},
    2009: {"stu": "https://web.archive.org/web/2023id_/https://www.oecd.org/pisa/pisaproducts/INT_STQ09_DEC11.zip",
           "syntaxe": OECD_OLD + "/pisa-2009-datasets/sas-and-spss-control-files/PISA2009_SPSS_student.txt"},
    2006: {"stu": "https://web.archive.org/web/2020id_/http://www.oecd.org/pisa/pisaproducts/INT_Stu06_Dec07.zip",
           "syntaxe": OECD_OLD + "/pisa-2006-datasets/sas-and-spss-control-files/PISA2006_SPSS_student.txt"},
    2003: {"stu": "https://web.archive.org/web/2025id_/https://www.oecd.org/content/dam/oecd/en/data/datasets/"
                  "pisa/pisa-2003-datasets/data-sets-in-txt-formats/INT_stui_2003_v2.zip",
           "syntaxe": OECD_OLD + "/pisa-2003-datasets/sas-and-spss-control-files/PISA2003_SPSS_student.txt"},
    2000: {"stu_math": "https://web.archive.org/web/2023id_/https://www.oecd.org/pisa/pisaproducts/intstud_math.zip",
           "stu_read": "https://web.archive.org/web/2023id_/https://www.oecd.org/pisa/pisaproducts/intstud_read.zip",
           "stu_scie": "https://web.archive.org/web/2023id_/https://www.oecd.org/pisa/pisaproducts/intstud_scie.zip",
           "syntaxe_math": OECD_OLD + "/pisa-2000-datasets/sas-and-spss-control-files/PISA2000_SPSS_student_mathematics.txt",
           "syntaxe_read": OECD_OLD + "/pisa-2000-datasets/sas-and-spss-control-files/PISA2000_SPSS_student_reading.txt",
           "syntaxe_scie": OECD_OLD + "/pisa-2000-datasets/sas-and-spss-control-files/PISA2000_SPSS_student_science.txt"},
}

UA = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
      "Chrome/126.0 Safari/537.36")
SEGMENT = 8 * 1024 * 1024   # taille d'une plage HTTP
NB_FILS = 12                # plages téléchargées en parallèle (le débit par connexion est faible)


def _nom_local(annee: int, cle: str, url: str) -> str:
    return f"{annee}_{cle}_{os.path.basename(url.split('?')[0])}"


def _requete(url: str, plage: str | None = None, methode: str = "GET"):
    req = urllib.request.Request(url, method=methode, headers={"User-Agent": UA})
    if plage:
        req.add_header("Range", f"bytes={plage}")
    return urllib.request.urlopen(req, timeout=120)  # TLS vérifié (contexte par défaut)


def _taille_et_plages(url: str) -> tuple[int | None, str]:
    """Renvoie (taille totale, url finale) si le serveur accepte les plages, sinon (None, url)."""
    with _requete(url, "0-0") as r:
        final = r.geturl()
        cr = r.headers.get("Content-Range")
        if r.status == 206 and cr and "/" in cr and cr.split("/")[-1].isdigit():
            return int(cr.split("/")[-1]), final
    return None, final


def _telecharger_fichier(url: str, dest: Path, essais: int = 6) -> None:
    if dest.exists() and dest.stat().st_size > 0:
        return
    part = dest.with_suffix(dest.suffix + ".part")
    for k in range(essais):
        try:
            taille, final = _taille_et_plages(url)
            break
        except Exception:                    # noqa: BLE001 - hôte instable : on réessaie
            if k == essais - 1:
                raise
            time.sleep(10 * (k + 1))
    if taille is None:                       # pas de plages : un seul flux
        for k in range(essais):
            try:
                with _requete(final) as r, open(part, "wb") as f:
                    shutil.copyfileobj(r, f, 1 << 20)
                break
            except Exception:                # noqa: BLE001 - on réessaie
                if k == essais - 1:
                    raise
                time.sleep(5 * (k + 1))
        part.rename(dest)
        return
    with open(part, "wb") as f:
        f.truncate(taille)
    plages = [(a, min(a + SEGMENT, taille) - 1) for a in range(0, taille, SEGMENT)]

    def un_segment(ab):
        a, b = ab
        for k in range(essais):
            try:
                with _requete(final, f"{a}-{b}") as r:
                    if r.status != 206:
                        raise IOError(f"statut {r.status}")
                    data = r.read()
                if len(data) != b - a + 1:
                    raise IOError("segment incomplet")
                fd = os.open(part, os.O_WRONLY)
                try:
                    os.pwrite(fd, data, a)
                finally:
                    os.close(fd)
                return
            except Exception:                # noqa: BLE001
                if k == essais - 1:
                    raise
                time.sleep(3 * (k + 1))

    with cf.ThreadPoolExecutor(NB_FILS) as ex:
        list(ex.map(un_segment, plages))
    if part.stat().st_size != taille:
        raise IOError(f"taille inattendue pour {dest}")
    part.rename(dest)


def _zip_valide(chemin: Path) -> bool:
    """Teste l'intégrité d'un zip (Deflate64, méthode 9, utilisé en 2025 : test via `unzip -t`)."""
    with zipfile.ZipFile(chemin) as z:
        if all(i.compress_type in (0, 8, 12, 14) for i in z.infolist()):
            return z.testzip() is None
    return subprocess.run(["unzip", "-tqq", str(chemin)], capture_output=True).returncode == 0


def _extraire_zip(chemin: Path, membre: str, dest_dir: Path) -> Path:
    """Extrait un membre d'un zip (repli sur `unzip` pour Deflate64)."""
    dest_dir.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(chemin) as z:
        info = z.getinfo(membre)
        if info.compress_type in (0, 8, 12, 14):
            return Path(z.extract(info, dest_dir))
    subprocess.run(["unzip", "-o", "-qq", str(chemin), membre, "-d", str(dest_dir)], check=True)
    return dest_dir / membre


def telecharger(dossier_brut, annees=None) -> list[Path]:
    """Télécharge les fichiers élèves (et syntaxes SPSS 2000-2012) dans ``dossier_brut``.

    Les fichiers déjà présents sont conservés. Les .zip sont vérifiés (testzip).
    """
    d = Path(dossier_brut)
    d.mkdir(parents=True, exist_ok=True)
    sortie = []
    for annee in (annees or FICHIERS):
        for cle, url in FICHIERS[annee].items():
            dest = d / _nom_local(annee, cle, url)
            print(f"[{annee}] {cle} <- {url}", flush=True)
            _telecharger_fichier(url, dest)
            if dest.suffix.lower() == ".zip" and not _zip_valide(dest):
                dest.unlink()
                raise IOError(f"zip corrompu : {dest}")
            sortie.append(dest)
    return sortie


# --------------------------------------------------------------------------------------
# 2. Pays, seuils, configuration par cycle
# --------------------------------------------------------------------------------------
# Code PISA (CNT, ISO 3166 alpha-3 ; QCY = Chypre dans certains fichiers) -> code Eurostat
PAYS = {"AUT": "AT", "BEL": "BE", "BGR": "BG", "HRV": "HR", "CYP": "CY", "QCY": "CY", "CZE": "CZ",
        "DNK": "DK", "EST": "EE", "FIN": "FI", "FRA": "FR", "DEU": "DE", "GRC": "EL", "HUN": "HU",
        "IRL": "IE", "ITA": "IT", "LVA": "LV", "LTU": "LT", "LUX": "LU", "MLT": "MT", "NLD": "NL",
        "POL": "PL", "PRT": "PT", "ROU": "RO", "SVK": "SK", "SVN": "SI", "ESP": "ES", "SWE": "SE"}
UE27 = sorted(set(PAYS.values()))

DOMAINES = {"maths": "MATH", "lecture": "READ", "sciences": "SCIE"}
# Bornes inférieures officielles des niveaux 2 et 5 (identiques dans tous les cycles où l'échelle
# a des niveaux : lecture depuis 2000, maths depuis 2003, sciences depuis 2006 ; vérifié pour 2025
# dans les notes techniques PISA 2025).
SEUILS = {"maths": (420.07, 606.99), "lecture": (407.47, 625.61), "sciences": (409.54, 633.33)}
# Premier cycle où l'échelle (et donc les niveaux et la tendance OCDE) existe pour chaque domaine
ECHELLE_DEPUIS = {"maths": 2003, "lecture": 2000, "sciences": 2006}

# Items de harcèlement (question ST038) : actes subis « au moins quelques fois par mois » (codes 3-4)
ITEMS_HARC = {
    2015: ["ST038Q03NA", "ST038Q04NA", "ST038Q05NA", "ST038Q06NA", "ST038Q07NA", "ST038Q08NA"],
    2018: ["ST038Q03NA", "ST038Q04NA", "ST038Q05NA", "ST038Q06NA", "ST038Q07NA", "ST038Q08NA"],
    2022: ["ST038Q03NA", "ST038Q04NA", "ST038Q05NA", "ST038Q06NA", "ST038Q07NA", "ST038Q08NA"],
    2025: ["ST038Q04NA", "ST038Q05NA", "ST038Q07NA", "ST038Q08NA", "ST038Q12DA"],
}
# Indices du questionnaire élève (WLE) : nom de variable par cycle (absent = non mesuré)
INDICES = {
    2025: {"appartenance": "BELONG", "securite": "FEELSAFE", "harcelement": "BULLIED"},
    2022: {"appartenance": "BELONG", "securite": "FEELSAFE", "harcelement": "BULLIED"},
    2018: {"appartenance": "BELONG", "harcelement": "BEINGBULLIED"},
    2015: {"appartenance": "BELONG"},
    2012: {"appartenance": "BELONG"},
    2003: {"appartenance": "BELONG"},
}

# Nombre de valeurs plausibles par cycle (ordre de traitement : priorité aux cycles récents)
CYCLES = {2025: 10, 2022: 10, 2018: 10, 2015: 10, 2012: 5, 2009: 5, 2006: 5, 2003: 5, 2000: 5}


# --------------------------------------------------------------------------------------
# 3. Lecture des microdonnées (colonnes utiles seulement, UE-27 seulement), avec cache
# --------------------------------------------------------------------------------------
def _fichier(d: Path, annee: int, cle: str) -> Path:
    if cle not in FICHIERS[annee]:
        cle = cle.split("_")[0]          # « stu_qq2 » : membre du zip « stu »
    return d / _nom_local(annee, cle, FICHIERS[annee][cle])


def _membre_zip(chemin: Path, motif: str) -> str:
    with zipfile.ZipFile(chemin) as z:
        noms = [n for n in z.namelist() if re.search(motif, n, re.I)]
    if len(noms) != 1:
        raise ValueError(f"{chemin.name} : membre {motif!r} introuvable ou ambigu ({noms})")
    return noms[0]


def _lire_sav_ue(chemin_sav: Path, colonnes: list[str]) -> pd.DataFrame:
    """Lit un .sav par blocs avec usecols, garde les élèves des pays de l'UE-27."""
    import pyreadstat
    _, meta = pyreadstat.read_sav(str(chemin_sav), metadataonly=True)
    dispo = set(meta.column_names)
    cols = [c for c in colonnes if c in dispo]
    morceaux = []
    for bloc, _ in pyreadstat.read_file_in_chunks(pyreadstat.read_sav, str(chemin_sav),
                                                  chunksize=150_000, usecols=cols):
        morceaux.append(bloc[bloc["CNT"].isin(PAYS)])
    return pd.concat(morceaux, ignore_index=True)


def _colonnes_voulues(annee: int) -> list[str]:
    npv = CYCLES[annee]
    cols = ["CNT", "CNTSTUID", "W_FSTUWT", "ESCS", *INDICES.get(annee, {}).values()]
    cols += [f"PV{i}{d}" for d in DOMAINES.values() for i in range(1, npv + 1)]
    cols += ITEMS_HARC.get(annee, [])
    return cols


def _cache(d: Path, annee: int, nom: str) -> Path:
    return d / f"cache_{annee}_{nom}_ue27.csv.gz"


def _charger_sav(d: Path, annee: int, cle: str, membre_motif: str, colonnes: list[str],
                 nettoyer: bool) -> pd.DataFrame:
    cache = _cache(d, annee, cle)
    if cache.exists():
        return pd.read_csv(cache)
    zp = _fichier(d, annee, cle)
    membre = _membre_zip(zp, membre_motif)
    tmp = d / f"_x{annee}{cle}"
    sav = _extraire_zip(zp, membre, tmp)
    try:
        df = _lire_sav_ue(sav, colonnes)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    df.to_csv(cache, index=False, compression="gzip")
    if nettoyer:
        zp.unlink()
    return df


# --------------------------------------------------------------------------------------
# 4. Statistiques pondérées avec valeurs plausibles
# --------------------------------------------------------------------------------------
def _quantile_pondere(x: np.ndarray, w: np.ndarray, q: float) -> float:
    o = np.argsort(x, kind="mergesort")
    cw = np.cumsum(w[o])
    return float(x[o][np.searchsorted(cw, q * cw[-1])])


def _quarts_pondere(x: np.ndarray, w: np.ndarray) -> np.ndarray:
    """Quart national (1 à 4) de chaque élève, par cumul des poids (NaN si x manquant)."""
    out = np.full(len(x), np.nan)
    ok = ~np.isnan(x)
    xs, ws = x[ok], w[ok]
    o = np.argsort(xs, kind="mergesort")
    part = (np.cumsum(ws[o]) - ws[o] / 2) / ws.sum()     # position au milieu du poids de l'élève
    q = np.empty(len(xs))
    q[o] = np.minimum(np.floor(part * 4) + 1, 4)
    out[ok] = q
    return out


def _moy(x, w):
    ok = ~np.isnan(x)
    return float(np.sum(x[ok] * w[ok]) / np.sum(w[ok])) if ok.any() else np.nan


def _stats_domaine(pvs: np.ndarray, w: np.ndarray, domaine: str, annee: int) -> dict:
    """pvs : matrice élèves x valeurs plausibles. Chaque statistique est calculée sur chaque
    valeur plausible puis moyennée (règle de Rubin pour le point estimé)."""
    l2, l5 = SEUILS[domaine]
    res = {"moy": [], "faibles": [], "forts": [], "d9d1": []}
    for k in range(pvs.shape[1]):
        x = pvs[:, k]
        ok = ~np.isnan(x)
        x, ww = x[ok], w[ok]
        res["moy"].append(np.sum(x * ww) / ww.sum())
        res["faibles"].append(100 * ww[x < l2].sum() / ww.sum())
        res["forts"].append(100 * ww[x >= l5].sum() / ww.sum())
        res["d9d1"].append(_quantile_pondere(x, ww, 0.9) - _quantile_pondere(x, ww, 0.1))
    out = {k: float(np.mean(v)) for k, v in res.items()}
    if annee < ECHELLE_DEPUIS[domaine]:
        out.pop("faibles"), out.pop("forts")      # pas de niveaux de compétence définis
    return out


def _stats_escs(pvs: np.ndarray, escs: np.ndarray, w: np.ndarray) -> dict:
    """Écart de score haut-bas quart ESCS et % de défavorisés résilients (domaine des pvs)."""
    quart = _quarts_pondere(escs, w)
    bas, haut = quart == 1, quart == 4
    ecarts, resil = [], []
    for k in range(pvs.shape[1]):
        x = pvs[:, k]
        ok = ~np.isnan(x)                              # élèves sans score dans ce domaine exclus
        ecarts.append(_moy(x[haut], w[haut]) - _moy(x[bas], w[bas]))
        seuil = _quantile_pondere(x[ok], w[ok], 0.75)  # quart supérieur national (tous élèves)
        resil.append(100 * w[bas & ok & (x >= seuil)].sum() / w[bas & ok].sum())
    return {"ecart_escs": float(np.mean(ecarts)), "resilients": float(np.mean(resil))}


# --------------------------------------------------------------------------------------
# 5. Indicateurs d'un cycle
# --------------------------------------------------------------------------------------
def _pvs(df: pd.DataFrame, code: str, npv: int) -> np.ndarray | None:
    cols = [f"PV{i}{code}" for i in range(1, npv + 1)]
    if not all(c in df.columns for c in cols):
        return None
    m = df[cols].to_numpy(float)
    return None if np.isnan(m).all() else m


def _ligne(pays, ind, annee, val, source, note=""):
    return {"pays": pays, "indicateur": ind, "annee": annee,
            "valeur": None if val is None or not np.isfinite(val) else round(float(val), 3),
            "source": source, "note": note}


def _indicateurs(df: pd.DataFrame, annee: int, npv: int, source: str,
                 domaines_df: dict | None = None) -> list[dict]:
    """df : élèves UE-27 (une ligne par élève). domaines_df : pour 2000, un DataFrame par domaine."""
    lignes = []
    df = df.assign(pays=df["CNT"].map(PAYS))
    for pays, g in df.groupby("pays"):
        w = g["W_FSTUWT"].to_numpy(float)
        lignes.append(_ligne(pays, "pisa_effectif_15ans", annee, w.sum(), source))
        for dom, code in DOMAINES.items():
            gd = g if domaines_df is None else domaines_df[dom][domaines_df[dom]["CNT"].map(PAYS) == pays]
            pv = _pvs(gd, code, npv)
            if pv is None:
                continue
            wd = gd["W_FSTUWT"].to_numpy(float)
            st = _stats_domaine(pv, wd, dom, annee)
            lignes.append(_ligne(pays, f"pisa_{dom}", annee, st["moy"], source))
            lignes.append(_ligne(pays, f"pisa_d9d1_{dom}", annee, st["d9d1"], source))
            if "faibles" in st:
                lignes.append(_ligne(pays, f"pisa_faibles_{dom}", annee, st["faibles"], source))
                lignes.append(_ligne(pays, f"pisa_forts_{dom}", annee, st["forts"], source))
            if dom == "maths" and "ESCS" in gd.columns and gd["ESCS"].notna().any():
                se = _stats_escs(pv, gd["ESCS"].to_numpy(float), wd)
                lignes.append(_ligne(pays, "pisa_ecart_escs_maths", annee, se["ecart_escs"], source))
                lignes.append(_ligne(pays, "pisa_resilients", annee, se["resilients"], source))
        # élèves faibles (sous le niveau 2) dans les trois domaines à la fois : la i-ème valeur
        # plausible de chaque domaine est appariée, puis on fait la moyenne sur les valeurs plausibles
        if domaines_df is None and annee >= 2006:
            pvs = {dom: _pvs(g, code, npv) for dom, code in DOMAINES.items()}
            if all(v is not None for v in pvs.values()):
                bas = np.ones_like(pvs["maths"], dtype=bool)
                for dom, v in pvs.items():
                    bas &= v < SEUILS[dom][0]
                part = [100 * w[bas[:, i]].sum() / w.sum() for i in range(bas.shape[1])]
                lignes.append(_ligne(pays, "pisa_faibles_3domaines", annee, float(np.mean(part)), source))
        for ind, var in INDICES.get(annee, {}).items():
            if var in g.columns and g[var].notna().sum() > 0:
                lignes.append(_ligne(pays, f"pisa_{ind}", annee, _moy(g[var].to_numpy(float), w), source))
        items = [c for c in ITEMS_HARC.get(annee, []) if c in g.columns]
        if items:
            it = g[items].to_numpy(float, copy=True)
            it[(it < 1) | (it > 4)] = np.nan
            rep = ~np.isnan(it).all(axis=1)
            if rep.any():
                freq = (np.nan_to_num(it, nan=0) >= 3).any(axis=1)
                lignes.append(_ligne(pays, "pisa_harcelement_freq", annee,
                                     100 * w[rep & freq].sum() / w[rep].sum(), source))
    return lignes


def _source(annee: int, fichier: str) -> str:
    return f"OCDE, base de données PISA {annee}, fichier {fichier} ; calcul sur microdonnées"


def _cycle_sav(d: Path, annee: int, nettoyer: bool) -> list[dict]:
    motif = {2025: r"STU_PUF\.sav$", 2022: r"STU_QQQ\.SAV$",
             2018: r"STU_QQQ\.sav$", 2015: r"STU_QQQ\.sav$"}[annee]
    df = _charger_sav(d, annee, "stu", motif, _colonnes_voulues(annee), nettoyer and annee != 2015)
    if annee == 2015:     # items de harcèlement publiés à part (fichier QQ2), appariés par CNTSTUID
        qq2 = _charger_sav(d, 2015, "stu_qq2", r"STU_QQ2\.sav$", ["CNT", "CNTSTUID"] + ITEMS_HARC[2015],
                           nettoyer)
        df = df.merge(qq2, on=["CNT", "CNTSTUID"], how="left", validate="one_to_one")
    nom = os.path.basename(FICHIERS[annee]["stu"])
    lignes = _indicateurs(df, annee, CYCLES[annee], _source(annee, nom))
    if annee == 2022:     # pensée créative : fichier CRT (sans poids) apparié au fichier élève
        crt = _charger_sav(d, 2022, "crt", r"CRT_COG\.SAV$",
                           ["CNT", "CNTSTUID"] + [f"PV{i}CRTH_NC" for i in range(1, 11)], nettoyer)
        m = crt.merge(df[["CNT", "CNTSTUID", "W_FSTUWT"]], on=["CNT", "CNTSTUID"], how="inner",
                      validate="one_to_one")
        src = _source(2022, "CRT_SPSS.zip (apparié à STU_QQQ pour W_FSTUWT)")
        for cnt, g in m.groupby("CNT"):
            pv = g[[f"PV{i}CRTH_NC" for i in range(1, 11)]].to_numpy(float)
            w = g["W_FSTUWT"].to_numpy(float)
            v = np.mean([_moy(pv[:, k], w) for k in range(10)])
            lignes.append(_ligne(PAYS[cnt], "pisa_pensee_creative", 2022, v, src,
                                 "échelle 0-60 points (score « number correct »)"))
    return lignes


# --------------------------------------------------------------------------------------
# 6. Repli : Banque mondiale EdStats (source 12), tableaux OCDE repris (LO.PISA.*)
# --------------------------------------------------------------------------------------
EDSTATS_URL = ("https://api.worldbank.org/v2/country/{pays}/indicator/{ind}"
               "?source=12&format=json&per_page=20000&date=2000:2025")
EDSTATS_IND = [f"LO.PISA.{d}{s}" for d in ("MAT", "REA", "SCI")
               for s in ("", ".P10", ".P90", ".2", ".3", ".4", ".5", ".6")] + \
              ["LO.PISA.REA.0.B1C", "LO.PISA.REA.1C", "LO.PISA.REA.1B", "LO.PISA.REA.1A"]
# Lecture : parts arrondies à l'unité ; la somme des catégories sous le niveau 2 (2 à 4 catégories,
# souvent nulles) est plus précise que 100 - (niveaux 2 à 6), cf. pisa_notes.md.
_REA_BAS = ["LO.PISA.REA.0.B1C", "LO.PISA.REA.1C", "LO.PISA.REA.1B", "LO.PISA.REA.1A"]
ISO3_EDSTATS = {"AT": "AUT", "BE": "BEL", "BG": "BGR", "HR": "HRV", "CY": "CYP", "CZ": "CZE", "DK": "DNK",
                "EE": "EST", "FI": "FIN", "FR": "FRA", "DE": "DEU", "EL": "GRC", "HU": "HUN", "IE": "IRL",
                "IT": "ITA", "LV": "LVA", "LT": "LTU", "LU": "LUX", "MT": "MLT", "NL": "NLD", "PL": "POL",
                "PT": "PRT", "RO": "ROU", "SK": "SVK", "SI": "SVN", "ES": "ESP", "SE": "SWE"}


def telecharger_edstats(dossier_brut) -> Path:
    """Télécharge les séries LO.PISA.* (UE-27) de l'API Banque mondiale ; JSON mis en cache."""
    import json
    dest = Path(dossier_brut) / "edstats_lo_pisa.json"
    if dest.exists():
        return dest
    pays = ";".join(ISO3_EDSTATS.values())
    lignes = []
    for i in range(0, len(EDSTATS_IND), 10):           # 10 indicateurs par requête
        url = EDSTATS_URL.format(pays=pays, ind=";".join(EDSTATS_IND[i:i + 10]))
        with _requete(url) as r:
            meta, data = json.loads(r.read().decode("utf-8"))
        if meta.get("pages", 1) > 1:
            raise IOError("pagination EdStats inattendue")
        lignes += [{"iso3": x["countryiso3code"], "ind": x["indicator"]["id"], "annee": int(x["date"]),
                    "valeur": x["value"]} for x in data if x["value"] is not None]
    dest.write_text(json.dumps(lignes))
    return dest


# --------------------------------------------------------------------------------------
# 7. Cycles 2000-2012 : fichiers texte à largeur fixe + syntaxe SPSS officielle
# --------------------------------------------------------------------------------------
INDICES.update({2000: {"appartenance": "BELONG"}})


def _positions_spss(syntaxe: Path) -> dict[str, tuple[int, int]]:
    """Lit les positions « NOM debut - fin » du bloc DATA LIST d'une syntaxe SPSS OCDE."""
    pos = {}
    motif = re.compile(r"^\s*/?\s*([A-Za-z_][A-Za-z0-9_]*)\s+(\d+)\s*-\s*(\d+)\b")
    for ligne in syntaxe.read_text(encoding="latin-1").splitlines():
        m = motif.match(ligne)
        if m and m.group(1).upper() not in pos:
            pos[m.group(1).upper()] = (int(m.group(2)) - 1, int(m.group(3)))
    return pos


def _lire_txt_ue(zp: Path, syntaxe: Path, colonnes: list[str]) -> pd.DataFrame:
    pos = _positions_spss(syntaxe)
    cols = [c for c in colonnes if c in pos]
    membre = _membre_zip(zp, r"\.txt$")
    morceaux = []
    with zipfile.ZipFile(zp) as z, z.open(membre) as f:
        lecteur = pd.read_fwf(f, colspecs=[pos[c] for c in cols], names=cols, header=None,
                              dtype={"CNT": str}, chunksize=100_000, encoding="latin-1")
        for bloc in lecteur:
            bloc["CNT"] = bloc["CNT"].str.strip()
            morceaux.append(bloc[bloc["CNT"].isin(PAYS)])
    df = pd.concat(morceaux, ignore_index=True)
    for c in cols:
        if c != "CNT":
            df[c] = pd.to_numeric(df[c], errors="coerce")
    for c in ("ESCS", "BELONG"):     # codes manquants 997-9999 dans les fichiers texte
        if c in df.columns:
            df.loc[df[c].abs() >= 900, c] = np.nan
    return df


def _charger_txt(d: Path, annee: int, cle: str, cle_syntaxe: str, colonnes: list[str],
                 nettoyer: bool) -> pd.DataFrame:
    cache = _cache(d, annee, cle)
    if cache.exists():
        return pd.read_csv(cache, dtype={"CNT": str})
    zp = _fichier(d, annee, cle)
    df = _lire_txt_ue(zp, _fichier(d, annee, cle_syntaxe), colonnes)
    df.to_csv(cache, index=False, compression="gzip")
    if nettoyer:
        zp.unlink()
    return df


def _cycle_txt(d: Path, annee: int, nettoyer: bool) -> list[dict]:
    cols = _colonnes_voulues(annee)
    if annee != 2000:
        df = _charger_txt(d, annee, "stu", "syntaxe", cols, nettoyer)
        nom = os.path.basename(FICHIERS[annee]["stu"])
        return _indicateurs(df, annee, 5, _source(annee, nom + " (Internet Archive)"))
    parts = {}
    for dom, suf in (("maths", "math"), ("lecture", "read"), ("sciences", "scie")):
        parts[dom] = _charger_txt(d, 2000, f"stu_{suf}", f"syntaxe_{suf}", cols, nettoyer)
    src = _source(2000, "intstud_read/math/scie.zip (Internet Archive)")
    return _indicateurs(parts["lecture"], 2000, 5, src, domaines_df=parts)


# --------------------------------------------------------------------------------------
# 8. Valeurs publiées par l'OCDE (Chypre, absente des fichiers publics 2015-2025 ; contrôles)
# --------------------------------------------------------------------------------------
# PISA 2022 Results (Vol. I), tableau I.1 ; PISA 2025 Results (Vol. I), tableaux I.1 et I.5.
PUBLIE_CHYPRE = {
    (2012, "pisa_maths"): 440,          # PISA 2012 Results (Vol. I) ; absent d'EdStats
    (2022, "pisa_maths"): 418, (2022, "pisa_lecture"): 381, (2022, "pisa_sciences"): 411,
    (2025, "pisa_maths"): 412, (2025, "pisa_lecture"): 379, (2025, "pisa_sciences"): 411,
    (2025, "pisa_appartenance"): -0.02,
}
SOURCE_OCDE_2022 = "OCDE, PISA 2022 Results (Volume I), tableau I.1 (valeur publiée)"
SOURCE_OCDE_2025 = "OCDE, PISA 2025 Results (Volume I), tableaux I.1 et I.5 (valeur publiée)"

# Moyennes publiées (maths, lecture, sciences) pour les contrôles : PISA 2022 et 2025, Vol. I,
# tableau I.1 (tous pays UE disponibles) ; cycles antérieurs : France et Allemagne (rapports OCDE).
REF_MOYENNES = {
    2025: {"EE": (508, 499, 527), "FI": (469, 474, 504), "IE": (480, 500, 500), "AT": (477, 467, 497),
           "PL": (484, 482, 495), "CZ": (477, 468, 490), "BE": (480, 466, 490), "LT": (470, 464, 488),
           "DE": (464, 465, 486), "NL": (483, 441, 485), "SE": (464, 466, 485), "SI": (460, 445, 484),
           "FR": (458, 456, 483), "IT": (468, 474, 483), "PT": (460, 462, 482), "HU": (459, 452, 480),
           "DK": (471, 460, 478), "ES": (457, 451, 477), "HR": (455, 453, 476), "SK": (469, 448, 475),
           "LU": (458, 443, 474), "LV": (460, 430, 468), "MT": (439, 415, 453), "EL": (424, 423, 434),
           "RO": (419, 413, 425), "BG": (405, 387, 421)},
    2022: {"EE": (510, 511, 526), "NL": (493, 459, 488), "IE": (492, 516, 504), "BE": (489, 479, 491),
           "DK": (489, 489, 494), "PL": (489, 489, 499), "AT": (487, 480, 491), "CZ": (487, 489, 498),
           "SI": (485, 469, 500), "FI": (484, 490, 511), "LV": (483, 475, 494), "SE": (482, 487, 494),
           "LT": (475, 472, 484), "DE": (475, 480, 492), "FR": (474, 474, 487), "ES": (473, 474, 485),
           "HU": (473, 473, 486), "PT": (472, 477, 484), "IT": (471, 482, 477), "MT": (466, 445, 466),
           "SK": (464, 447, 462), "HR": (463, 475, 483), "EL": (430, 438, 441), "RO": (428, 428, 428),
           "BG": (417, 404, 421)},
    2018: {"FR": (495, 493, 493), "DE": (500, 498, 503), "EE": (523, 523, 530), "PL": (516, 512, 511)},
    2015: {"FR": (493, 499, 495), "DE": (506, 509, 509), "EE": (520, 519, 534), "FI": (511, 526, 531)},
    2012: {"FR": (495, 505, 499), "DE": (514, 508, 524)},
    2009: {"FR": (497, 496, 498), "DE": (513, 497, 520)},
    2006: {"FR": (496, 488, 495), "DE": (504, 495, 516)},
    2003: {"FR": (511, 496, 511), "DE": (503, 491, 502)},
    2000: {"FR": (517, 505, 500), "DE": (490, 484, 487)},
}
# Part de défavorisés résilients (maths) et écart de score en maths haut-bas quart ESCS publiés
# (PISA 2022 Results, Vol. I, tableau I.2).
REF_ESCS_2022 = {"MT": (12.7, 83), "EL": (12.0, 76), "DK": (10.2, 74), "FI": (11.9, 83), "IE": (11.9, 74),
                 "HR": (10.7, 82), "LV": (11.7, 75), "EE": (10.3, 81), "IT": (11.3, 85), "ES": (11.7, 86),
                 "SE": (9.9, 99), "NL": (10.6, 106), "SI": (9.4, 91), "PL": (8.6, 96), "LT": (9.8, 92),
                 "BG": (7.4, 108), "PT": (9.4, 101), "DE": (9.5, 111), "AT": (8.2, 106), "FR": (7.4, 113),
                 "BE": (8.2, 117), "CZ": (7.3, 116), "HU": (8.2, 121), "SK": (6.1, 133), "RO": (6.6, 132)}


def controles(res: pd.DataFrame) -> pd.DataFrame:
    """Compare les résultats calculés sur microdonnées aux valeurs publiées par l'OCDE."""
    v = res.set_index(["pays", "indicateur", "annee"])["valeur"]
    typ = res.set_index(["pays", "indicateur", "annee"])["source"].str.contains("calcul sur microdonnées")
    lignes = []
    for annee, pays_ref in REF_MOYENNES.items():
        for pays, triple in pays_ref.items():
            for ind, ref in zip(("pisa_maths", "pisa_lecture", "pisa_sciences"), triple):
                calc = v.get((pays, ind, annee))
                lignes.append((annee, pays, ind, ref, calc))
    for pays, (resil, ecart) in REF_ESCS_2022.items():
        lignes.append((2022, pays, "pisa_resilients", resil, v.get((pays, "pisa_resilients", 2022))))
        lignes.append((2022, pays, "pisa_ecart_escs_maths", ecart, v.get((pays, "pisa_ecart_escs_maths", 2022))))
    out = pd.DataFrame(lignes, columns=["annee", "pays", "indicateur", "publie_ocde", "calcule"])
    out["ecart"] = out["calcule"] - out["publie_ocde"]
    out["origine"] = ["microdonnées" if typ.get((p, i, a), False) else "repli publié"
                      for p, i, a in zip(out["pays"], out["indicateur"], out["annee"])]
    return out


# --------------------------------------------------------------------------------------
# 9. Repli EdStats -> indicateurs
# --------------------------------------------------------------------------------------
SOURCE_EDSTATS = ("Banque mondiale, EdStats (API v2, source 12), séries LO.PISA.* reprises des "
                  "tableaux OCDE (valeur publiée, non recalculée)")


def _indicateurs_edstats(d: Path) -> list[dict]:
    import json
    chemin = Path(d) / "edstats_lo_pisa.json"
    if not chemin.exists():
        return []
    e = pd.DataFrame(json.loads(chemin.read_text()))
    inv = {v: k for k, v in ISO3_EDSTATS.items()}
    e["pays"] = e["iso3"].map(inv)
    s = e.set_index(["pays", "annee", "ind"])["valeur"]
    lignes = []
    for (pays, annee), _ in e.groupby(["pays", "annee"]):
        for dom, c in (("maths", "MAT"), ("lecture", "REA"), ("sciences", "SCI")):
            g = lambda i: s.get((pays, annee, i))        # noqa: E731
            moy = g(f"LO.PISA.{c}")
            if moy is not None:
                lignes.append(_ligne(pays, f"pisa_{dom}", annee, moy, SOURCE_EDSTATS))
            p10, p90 = g(f"LO.PISA.{c}.P10"), g(f"LO.PISA.{c}.P90")
            if p10 is not None and p90 is not None:
                lignes.append(_ligne(pays, f"pisa_d9d1_{dom}", annee, p90 - p10, SOURCE_EDSTATS))
            if annee < ECHELLE_DEPUIS[dom]:
                continue
            niv = {k: g(f"LO.PISA.{c}.{k}") for k in (2, 3, 4, 5, 6)}
            if None in niv.values():
                continue
            arr = " ; parts par niveau arrondies à l'unité par la source (± 1 à 2 points)" if c == "REA" else ""
            bas = [g(i) for i in _REA_BAS]
            if c == "REA" and None not in bas:
                lignes.append(_ligne(pays, f"pisa_faibles_{dom}", annee, sum(bas), SOURCE_EDSTATS,
                                     "somme des parts sous le niveau 2" + arr))
            else:
                lignes.append(_ligne(pays, f"pisa_faibles_{dom}", annee, 100 - sum(niv.values()),
                                     SOURCE_EDSTATS, "100 - somme des parts aux niveaux 2 à 6" + arr))
            lignes.append(_ligne(pays, f"pisa_forts_{dom}", annee, niv[5] + niv[6], SOURCE_EDSTATS,
                                 "somme des parts aux niveaux 5 et 6" + arr))
    return lignes


# --------------------------------------------------------------------------------------
# 10. Notes par indicateur et cycle (ruptures de série, définitions)
# --------------------------------------------------------------------------------------
def _note_auto(pays: str, ind: str, annee: int) -> str:
    n = []
    dom = next((k for k in DOMAINES if ind.endswith(k)), None)
    if dom and annee < ECHELLE_DEPUIS[dom]:
        n.append(f"échelle {dom} établie en {ECHELLE_DEPUIS[dom]} : valeur {annee} non comparable aux "
                 "cycles suivants (domaine mineur, échelle provisoire)")
    if dom == "lecture" and annee == 2009:
        n.append("nouveau cadre de lecture en 2009 (échelle 2000 maintenue, niveaux 1a/1b)")
    if dom == "lecture" and annee == 2018:
        n.append("lecture domaine majeur, nouveau cadre et test adaptatif en 2018")
    if dom == "maths" and annee == 2022:
        n.append("maths domaine majeur, cadre révisé en 2022")
    if dom == "sciences" and annee == 2025:
        n.append("sciences domaine majeur, nouveau cadre 2025 (test adaptatif multi-étapes)")
    if annee == 2015 and (dom or ind == "pisa_resilients"):
        n.append("passage à l'évaluation sur ordinateur et nouveau modèle d'échelonnement en 2015")
    if pays == "ES" and annee == 2018 and dom == "lecture":
        n.append("ATTENTION : lecture 2018 non publiée par l'OCDE pour l'Espagne (réponses "
                 "invraisemblables d'une partie des élèves) ; valeur calculée, à exclure des comparaisons")
    if pays == "AT" and annee == 2009:
        n.append("OCDE : comparabilité limitée (boycott d'une partie des élèves en 2009)")
    if pays == "NL" and annee == 2000:
        n.append("OCDE : taux de participation insuffisant, résultats non publiés en 2000")
    if pays == "LU" and annee == 2000:
        n.append("OCDE : conditions de passation différentes en 2000, comparabilité limitée")
    if ind == "pisa_resilients":
        n.append("défavorisés = quart inférieur national de l'ESCS ; résilients = quart supérieur national "
                 "en maths (définition OCDE de 2022 appliquée à tous les cycles)")
    if ind == "pisa_ecart_escs_maths":
        n.append("moyenne maths du quart supérieur national d'ESCS moins quart inférieur")
    if ind in ("pisa_appartenance", "pisa_securite", "pisa_harcelement"):
        n.append("indice WLE propre au cycle (moyenne OCDE ~0) : pas de comparaison de niveau entre cycles")
    if ind == "pisa_harcelement" and annee == 2018:
        n.append("variable BEINGBULLIED")
    if ind == "pisa_harcelement_freq":
        items = {2025: "5 actes dont la cyberintimidation (ST038 Q04, Q05, Q07, Q08, Q12)"}.get(
            annee, "6 actes (ST038 Q03 à Q08)")
        n.append(f"% d'élèves victimes d'au moins un acte au moins quelques fois par mois ; {items}")
    if ind == "pisa_effectif_15ans":
        n.append("somme des poids W_FSTUWT (population de 15 ans scolarisée représentée)")
    return " ; ".join(n)


# --------------------------------------------------------------------------------------
# 11. Fonction principale
# --------------------------------------------------------------------------------------
def extraire(dossier_brut, nettoyer: bool = False) -> pd.DataFrame:
    """Calcule les indicateurs PISA UE-27 pour tous les cycles dont les fichiers sont présents.

    Ordre de priorité : microdonnées OCDE (fichiers de ``telecharger``, ou caches
    ``cache_*_ue27.csv.gz`` créés au premier passage) ; à défaut valeurs publiées (EdStats pour
    2000-2018, tableaux OCDE pour Chypre 2022 et 2025). ``nettoyer=True`` supprime chaque zip
    dès que son cache UE-27 est écrit.
    """
    d = Path(dossier_brut)
    lignes = []
    for annee in CYCLES:
        try:
            if annee >= 2015:
                lignes += _cycle_sav(d, annee, nettoyer)
            else:
                lignes += _cycle_txt(d, annee, nettoyer)
            print(f"PISA {annee} : microdonnées traitées", file=sys.stderr)
        except (FileNotFoundError, KeyError) as e:
            print(f"PISA {annee} : microdonnées absentes ({e}) -> repli sur valeurs publiées",
                  file=sys.stderr)
    res = pd.DataFrame(lignes)
    deja = set(zip(res["pays"], res["indicateur"], res["annee"])) if len(res) else set()
    repli = [r for r in _indicateurs_edstats(d) if (r["pays"], r["indicateur"], r["annee"]) not in deja]
    for (annee, ind), val in PUBLIE_CHYPRE.items():
        if ("CY", ind, annee) not in deja:
            src = {2012: "OCDE, PISA 2012 Results (Volume I) (valeur publiée)",
                   2022: SOURCE_OCDE_2022}.get(annee, SOURCE_OCDE_2025)
            repli.append(_ligne("CY", ind, annee, val, src,
                                "Chypre : microdonnées non disponibles, valeur publiée par l'OCDE"))
    res = pd.concat([res, pd.DataFrame(repli)], ignore_index=True)
    auto = [_note_auto(p, i, a) for p, i, a in zip(res["pays"], res["indicateur"], res["annee"])]
    res["note"] = [" ; ".join(x for x in (n, a) if x) for n, a in zip(res["note"].fillna(""), auto)]
    res = res.sort_values(["indicateur", "pays", "annee"]).reset_index(drop=True)
    return res[["pays", "indicateur", "annee", "valeur", "source", "note"]]


if __name__ == "__main__":
    args = sys.argv[1:]
    if args and args[0] == "--telecharger":
        telecharger(args[1])
        telecharger_edstats(args[1])
        sys.exit(0)
    if not args:
        sys.exit("usage : python3 -I pisa.py [--telecharger] DOSSIER_BRUT")
    sortie = extraire(args[0])
    chemin = Path(__file__).resolve().parent / "pisa.csv"
    sortie.to_csv(chemin, index=False, encoding="utf-8")
    print(f"{len(sortie)} lignes -> {chemin}", file=sys.stderr)
