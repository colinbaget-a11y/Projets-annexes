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
import numpy as np      # noqa: E402  (imports scientifiques après la partie téléchargement)
import pandas as pd     # noqa: E402

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

CYCLES = {   # nb de valeurs plausibles, fichier élève, membre du zip
    2025: dict(npv=10, cle="stu", membre="CY09_MS_STU_PUF.sav"),
    2022: dict(npv=10, cle="stu", membre="CY08MSP_STU_QQQ.SAV"),
    2018: dict(npv=10, cle="stu", membre=None),
    2015: dict(npv=10, cle="stu", membre=None),
    2012: dict(npv=5, cle="stu", membre=None),
    2009: dict(npv=5, cle="stu", membre=None),
    2006: dict(npv=5, cle="stu", membre=None),
    2003: dict(npv=5, cle="stu", membre=None),
    2000: dict(npv=5, cle=None, membre=None),
}


# --------------------------------------------------------------------------------------
# 3. Lecture des microdonnées (colonnes utiles seulement, UE-27 seulement), avec cache
# --------------------------------------------------------------------------------------
def _fichier(d: Path, annee: int, cle: str) -> Path:
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
    npv = CYCLES[annee]["npv"]
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
    zp = _fichier(d, annee, cle.split("_")[0])
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
        ecarts.append(_moy(x[haut], w[haut]) - _moy(x[bas], w[bas]))
        seuil = _quantile_pondere(x, w, 0.75)          # quart supérieur national (tous élèves)
        resil.append(100 * w[bas & (x >= seuil)].sum() / w[bas].sum())
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
    lignes = _indicateurs(df, annee, CYCLES[annee]["npv"], _source(annee, nom))
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
