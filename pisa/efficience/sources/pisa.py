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
    taille, final = _taille_et_plages(url)
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
            if dest.suffix.lower() == ".zip":
                with zipfile.ZipFile(dest) as z:
                    if z.testzip() is not None:
                        dest.unlink()
                        raise IOError(f"zip corrompu : {dest}")
            sortie.append(dest)
    return sortie
