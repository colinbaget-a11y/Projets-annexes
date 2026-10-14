"""
Dépense de santé de l'OCDE (System of Health Accounts, base « Health Statistics »), UE-27, 2000 à la
dernière année publiée.

    python sources/ocde_sha.py        télécharge puis écrit sources/ocde_sha.csv

Indicateurs :
  sante_dep_hab_ocde_ppa       dépense courante de santé par habitant, toutes sources de financement,
                               EUR à parités de pouvoir d'achat, prix courants (EUR_PPP_PS, V)
  sante_dep_hab_ocde_ppa_cst   idem, prix constants (EUR_PPP_PS, Q)
  sante_reste_a_charge_ocde    paiements directs des ménages (HF3), % de la dépense courante de santé

Les chiffres de la note (dépense de 4 250 EUR par habitant pour la France ; reste à charge de 9,3 %
contre 14,9 % dans l'UE) ne se retrouvent exactement dans aucune de ces séries, quelle que soit l'année
(voir le README).
"""
import io
import os
import ssl
import sys
import time
import urllib.request
from pathlib import Path

import pandas as pd

ICI = Path(__file__).resolve().parent
SORTIE_CSV = ICI / "ocde_sha.csv"
ISO3 = {
    "AUT": "AT", "BEL": "BE", "BGR": "BG", "HRV": "HR", "CYP": "CY", "CZE": "CZ", "DNK": "DK",
    "EST": "EE", "FIN": "FI", "FRA": "FR", "DEU": "DE", "GRC": "EL", "HUN": "HU", "IRL": "IE",
    "ITA": "IT", "LVA": "LV", "LTU": "LT", "LUX": "LU", "MLT": "MT", "NLD": "NL", "POL": "PL",
    "PRT": "PT", "ROU": "RO", "SVK": "SK", "SVN": "SI", "ESP": "ES", "SWE": "SE",
}
# clé : pays.fréquence.mesure.unité.régime de financement.recettes.fonction.mode.prestataire.facteur.actif.prix
URL = ("https://sdmx.oecd.org/public/rest/data/OECD.ELS.HD,DSD_SHA@DF_SHA,1.1/"
       + "+".join(ISO3) + ".A.EXP_HEALTH.EUR_PPP_PS+PT_EXP_HLTH.HF3+_T.._T._T._T..."
       "?startPeriod=2000&format=csvfilewithlabels")
FICHIER = "sha.csv"
SOURCE = "OCDE, Health Statistics (SHA), DF_SHA"
STATUTS = {"B": "rupture de série", "D": "définition différente", "E": "estimation", "P": "provisoire"}


def telecharger(dossier_brut):
    d = Path(dossier_brut)
    d.mkdir(parents=True, exist_ok=True)
    ctx = ssl.create_default_context(cafile=os.environ.get("SSL_CERT_FILE") or None)
    for k in range(4):
        try:
            req = urllib.request.Request(URL, headers={"User-Agent": "efficience/1.0"})
            with urllib.request.urlopen(req, context=ctx, timeout=300) as r:
                (d / FICHIER).write_bytes(r.read())
            return
        except OSError as e:
            print(f"OCDE indisponible ({e}), nouvel essai")
            time.sleep(10 * (k + 1))
    raise RuntimeError("Échec du téléchargement OCDE SHA")


def extraire(dossier_brut):
    t = pd.read_csv(Path(dossier_brut) / FICHIER, dtype=str)
    t["OBS_VALUE"] = pd.to_numeric(t.OBS_VALUE, errors="coerce")
    t = t[t.REF_AREA.isin(ISO3) & t.OBS_VALUE.notna()]
    choix = {
        ("EUR_PPP_PS", "_T", "V"): "sante_dep_hab_ocde_ppa",
        ("EUR_PPP_PS", "_T", "Q"): "sante_dep_hab_ocde_ppa_cst",
        ("PT_EXP_HLTH", "HF3", "_Z"): "sante_reste_a_charge_ocde",
    }
    cle = list(zip(t.UNIT_MEASURE, t.FINANCING_SCHEME, t.PRICE_BASE))
    t = t.assign(indicateur=[choix.get(c) for c in cle]).dropna(subset=["indicateur"])
    return pd.DataFrame({
        "pays": t.REF_AREA.map(ISO3),
        "indicateur": t.indicateur,
        "annee": t.TIME_PERIOD.astype(int),
        "valeur": t.OBS_VALUE,
        "source": SOURCE,
        "note": t.OBS_STATUS.map(STATUTS).fillna("") if "OBS_STATUS" in t else "",
    }).sort_values(["indicateur", "pays", "annee"]).reset_index(drop=True)


if __name__ == "__main__":
    brut = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("/tmp/efficience_brut/ocde_sha")
    telecharger(brut)
    df = extraire(brut)
    df.to_csv(SORTIE_CSV, index=False, float_format="%.6g")
    print(df.groupby("indicateur").agg(pays=("pays", "nunique"), debut=("annee", "min"),
                                       fin=("annee", "max")).to_string())
