"""Indicateurs de santé hors Eurostat (et dérivés d'Eurostat) pour 27 pays de l'UE.

Bulletin « efficience de la dépense de santé ». Ce module produit un DataFrame
long aux colonnes ``pays, indicateur, annee, valeur, source, note``.

Indicateurs produits
--------------------
- sante_ima30                    OCDE HCQI, mortalité à 30 j après IAM (45+, std âge-sexe),
                                 série chaînée si le pays en dispose, sinon non chaînée.
- sante_ima30_nonchaine          (complément) série non chaînée (même hôpital) pour tous les pays.
- sante_antibiotiques            OCDE Health Statistics, J01, DDD/1 000 hab./jour
                                 (ESAC-Net non accessible en données brutes, voir notes).
- sante_depenses_catastrophiques OMS Europe (UHCFP_4), % des ménages.
- sante_attente                  OCDE, délai moyen (jours) prothèse de hanche,
                                 de l'avis du spécialiste à l'opération.
- sante_attente_mediane          (complément) même chose, médiane.
- sante_attente_silc             (complément) EU-SILC hlth_silc_08, % des 16+ déclarant un
                                 besoin d'examen médical non satisfait pour cause de liste d'attente.
- sante_rd_pharma_ratio          BERD NACE C21 / dépense en produits pharmaceutiques HC.5.1 (%).
- sante_surmortalite_12m         Eurostat demo_mexrt, moyenne des 12 mois de l'année civile (%).
- sante_inegalite_densite        CV non pondéré de la densité médicale entre régions NUTS 2.
- sante_inegalite_densite_pond   CV pondéré par la population.

Usage
-----
    python -I sante_ext.py [--dossier DOSSIER_BRUT] [--sans-telechargement]

Les fichiers téléchargés sont traités comme des données (lecture CSV/JSON
uniquement) ; rien n'est exécuté depuis le dossier brut.
"""
from __future__ import annotations

import argparse
import http.client
import io
import json
import math
import os
import ssl
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

import pandas as pd

ICI = Path(__file__).resolve().parent
DOSSIER_BRUT_DEFAUT = Path(
    "/tmp/claude-0/-home-user-Projets-annexes/935fc156-45bd-500a-b52a-e7e4ee23abb6"
    "/scratchpad/efficience/sante_raw"
)
SORTIE_CSV = ICI / "sante_ext.csv"

PAYS = ["AT", "BE", "BG", "HR", "CY", "CZ", "DK", "EE", "FI", "FR", "DE", "EL", "HU", "IE",
        "IT", "LV", "LT", "LU", "MT", "NL", "PL", "PT", "RO", "SK", "SI", "ES", "SE"]
ISO3_VERS_ISO2 = {
    "AUT": "AT", "BEL": "BE", "BGR": "BG", "HRV": "HR", "CYP": "CY", "CZE": "CZ", "DNK": "DK",
    "EST": "EE", "FIN": "FI", "FRA": "FR", "DEU": "DE", "GRC": "EL", "HUN": "HU", "IRL": "IE",
    "ITA": "IT", "LVA": "LV", "LTU": "LT", "LUX": "LU", "MLT": "MT", "NLD": "NL", "POL": "PL",
    "PRT": "PT", "ROU": "RO", "SVK": "SK", "SVN": "SI", "ESP": "ES", "SWE": "SE",
}

UA = "efficience-sante/1.0 (python urllib; extraction statistique)"
EUROSTAT = "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/"
OECD = "https://sdmx.oecd.org/public/rest/data/"

# Certificat intermédiaire public « Sectigo Public Server Authentication CA DV R36 »
# (émis par la racine « Sectigo Public Server Authentication Root R46 »).
# Le serveur dw.euro.who.int n'envoie pas cet intermédiaire, ce qui fait échouer la
# vérification TLS des clients qui ne vont pas le chercher eux-mêmes (navigateurs : AIA).
# On l'ajoute donc aux certificats connus ; la vérification reste complète
# (chaîne jusqu'à une racine de confiance du magasin système + nom d'hôte).
# Source : Mozilla CCADB, PublicAllIntermediateCertsWithPEMCSV.
# SHA-256 : 8C:54:C3:34:B6:6B:A4:E4:26:77:2A:F4:A3:F9:13:6C:19:A1:AE:C7:29:FD:B2:8C:53:5C:07:A5:A4:EF:22:E0
SECTIGO_DV_R36_PEM = """-----BEGIN CERTIFICATE-----
MIIGTDCCBDSgAwIBAgIQOXpmzCdWNi4NqofKbqvjsTANBgkqhkiG9w0BAQwFADBf
MQswCQYDVQQGEwJHQjEYMBYGA1UEChMPU2VjdGlnbyBMaW1pdGVkMTYwNAYDVQQD
Ey1TZWN0aWdvIFB1YmxpYyBTZXJ2ZXIgQXV0aGVudGljYXRpb24gUm9vdCBSNDYw
HhcNMjEwMzIyMDAwMDAwWhcNMzYwMzIxMjM1OTU5WjBgMQswCQYDVQQGEwJHQjEY
MBYGA1UEChMPU2VjdGlnbyBMaW1pdGVkMTcwNQYDVQQDEy5TZWN0aWdvIFB1Ymxp
YyBTZXJ2ZXIgQXV0aGVudGljYXRpb24gQ0EgRFYgUjM2MIIBojANBgkqhkiG9w0B
AQEFAAOCAY8AMIIBigKCAYEAljZf2HIz7+SPUPQCQObZYcrxLTHYdf1ZtMRe7Yeq
RPSwygz16qJ9cAWtWNTcuICc++p8Dct7zNGxCpqmEtqifO7NvuB5dEVexXn9RFFH
12Hm+NtPRQgXIFjx6MSJcNWuVO3XGE57L1mHlcQYj+g4hny90aFh2SCZCDEVkAja
EMMfYPKuCjHuuF+bzHFb/9gV8P9+ekcHENF2nR1efGWSKwnfG5RawlkaQDpRtZTm
M64TIsv/r7cyFO4nSjs1jLdXYdz5q3a4L0NoabZfbdxVb+CUEHfB0bpulZQtH1Rv
38e/lIdP7OTTIlZh6OYL6NhxP8So0/sht/4J9mqIGxRFc0/pC8suja+wcIUna0HB
pXKfXTKpzgis+zmXDL06ASJf5E4A2/m+Hp6b84sfPAwQ766rI65mh50S0Di9E3Pn
2WcaJc+PILsBmYpgtmgWTR9eV9otfKRUBfzHUHcVgarub/XluEpRlTtZudU5xbFN
xx/DgMrXLUAPaI60fZ6wA+PTAgMBAAGjggGBMIIBfTAfBgNVHSMEGDAWgBRWc1hk
lfmSGrASKgRieaFAFYghSTAdBgNVHQ4EFgQUaMASFhgOr872h6YyV6NGUV3LBycw
DgYDVR0PAQH/BAQDAgGGMBIGA1UdEwEB/wQIMAYBAf8CAQAwHQYDVR0lBBYwFAYI
KwYBBQUHAwEGCCsGAQUFBwMCMBsGA1UdIAQUMBIwBgYEVR0gADAIBgZngQwBAgEw
VAYDVR0fBE0wSzBJoEegRYZDaHR0cDovL2NybC5zZWN0aWdvLmNvbS9TZWN0aWdv
UHVibGljU2VydmVyQXV0aGVudGljYXRpb25Sb290UjQ2LmNybDCBhAYIKwYBBQUH
AQEEeDB2ME8GCCsGAQUFBzAChkNodHRwOi8vY3J0LnNlY3RpZ28uY29tL1NlY3Rp
Z29QdWJsaWNTZXJ2ZXJBdXRoZW50aWNhdGlvblJvb3RSNDYucDdjMCMGCCsGAQUF
BzABhhdodHRwOi8vb2NzcC5zZWN0aWdvLmNvbTANBgkqhkiG9w0BAQwFAAOCAgEA
YtOC9Fy+TqECFw40IospI92kLGgoSZGPOSQXMBqmsGWZUQ7rux7cj1du6d9rD6C8
ze1B2eQjkrGkIL/OF1s7vSmgYVafsRoZd/IHUrkoQvX8FZwUsmPu7amgBfaY3g+d
q1x0jNGKb6I6Bzdl6LgMD9qxp+3i7GQOnd9J8LFSietY6Z4jUBzVoOoz8iAU84OF
h2HhAuiPw1ai0VnY38RTI+8kepGWVfGxfBWzwH9uIjeooIeaosVFvE8cmYUB4TSH
5dUyD0jHct2+8ceKEtIoFU/FfHq/mDaVnvcDCZXtIgitdMFQdMZaVehmObyhRdDD
4NQCs0gaI9AAgFj4L9QtkARzhQLNyRf87Kln+YU0lgCGr9HLg3rGO8q+Y4ppLsOd
unQZ6ZxPNGIfOApbPVf5hCe58EZwiWdHIMn9lPP6+F404y8NNugbQixBber+x536
WrZhFZLjEkhp7fFXf9r32rNPfb74X/U90Bdy4lzp3+X1ukh1BuMxA/EEhDoTOS3l
7ABvc7BYSQubQ2490OcdkIzUh3ZwDrakMVrbaTxUM2p24N6dB+ns2zptWCva6jzW
r8IWKIMxzxLPv5Kt3ePKcUdvkBU/smqujSczTzzSjIoR5QqQA6lN1ZRSnuHIWCvh
JEltkYnTAH41QJ6SAWO66GrrUESwN/cgZzL4JLEqz1Y=
-----END CERTIFICATE-----
"""

# --------------------------------------------------------------------------------------
# Fichiers à télécharger : nom local -> URL
# --------------------------------------------------------------------------------------
_geo = "&".join(f"geo={g}" for g in PAYS)
FICHIERS = {
    # OCDE
    "oecd_hcqo_ac.csv": OECD + "OECD.ELS.HD,DSD_HCQO@DF_AC,2.1/all?format=csvfilewithlabels",
    "oecd_phmc_consum.csv": OECD + "OECD.ELS.HD,HEALTH_PHMC@DF_PHMC_CONSUM,1.1/all?format=csvfilewithlabels",
    "oecd_waiting.csv": OECD + "OECD.ELS.HD,DSD_HEALTH_PROC@DF_WAITING,1.2/all?format=csvfilewithlabels",
    # Eurostat (JSON-stat 2.0)
    "es_demo_mexrt.json": EUROSTAT + f"demo_mexrt?unit=PC&{_geo}",
    "es_rd_e_berdindr2.json": EUROSTAT + f"rd_e_berdindr2?nace_r2=C21&unit=MIO_EUR&{_geo}",
    "es_hlth_sha11_hc.json": EUROSTAT + f"hlth_sha11_hc?icha11_hc=HC51&unit=MIO_EUR&{_geo}",
    "es_hlth_rs_physreg.json": EUROSTAT + "hlth_rs_physreg?unit=P_HTHAB&unit=NR&geoLevel=nuts2",
    "es_hlth_rs_prsrg.json": EUROSTAT + "hlth_rs_prsrg?isco08=OC221&unit=P_HTHAB&unit=NR&geoLevel=nuts2",
    "es_demo_r_pjanaggr3.json": EUROSTAT + "demo_r_pjanaggr3?sex=T&age=TOTAL&unit=NR&geoLevel=nuts2",
    "es_hlth_silc_08.json": EUROSTAT + (f"hlth_silc_08?reason=WLIST&age=Y_GE16&sex=T"
                                        f"&quant_inc=TOTAL&unit=PC&{_geo}"),
}
# Listes officielles des codes NUTS par version (GISCO), pour ne pas mélanger deux
# découpages régionaux dans un même calcul de dispersion.
VERSIONS_NUTS = [2024, 2021, 2016, 2013, 2010, 2006, 2003]
for _v in VERSIONS_NUTS:
    FICHIERS[f"gisco_nuts_{_v}.csv"] = (
        f"https://gisco-services.ec.europa.eu/distribution/v2/nuts/csv/NUTS_AT_{_v}.csv")
# OMS Europe : export en deux temps (l'API renvoie un JSON avec l'URL de téléchargement)
WHO_EXPORT = "https://dw.euro.who.int/api/v5/export/UHCFP_4?lang=EN&format=csv"
WHO_FICHIER = "who_uhcfp_4.csv"


# --------------------------------------------------------------------------------------
# Téléchargement
# --------------------------------------------------------------------------------------
def _contexte_ssl(intermediaire_who: bool = False) -> ssl.SSLContext:
    ctx = ssl.create_default_context(cafile=os.environ.get("SSL_CERT_FILE") or None)
    if intermediaire_who:
        ctx.load_verify_locations(cadata=SECTIGO_DV_R36_PEM)
    return ctx


def _get(url: str, ctx: ssl.SSLContext | None = None, essais: int = 4) -> bytes:
    ctx = ctx or _contexte_ssl()
    derniere = None
    for k in range(essais):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "*/*"})
            with urllib.request.urlopen(req, context=ctx, timeout=300) as r:
                return r.read()
        except urllib.error.HTTPError as e:  # 429 / 5xx : on réessaie
            derniere = e
            if e.code not in (429, 500, 502, 503, 504):
                raise
        except (urllib.error.URLError, ConnectionError, OSError, http.client.HTTPException) as e:
            derniere = e  # coupure réseau transitoire : on réessaie
        time.sleep(10 * (k + 1))
    raise RuntimeError(f"Échec du téléchargement {url}: {derniere}")


def telecharger(dossier_brut=DOSSIER_BRUT_DEFAUT) -> dict:
    """Télécharge les fichiers bruts dans ``dossier_brut``. Renvoie {fichier: statut}."""
    d = Path(dossier_brut)
    d.mkdir(parents=True, exist_ok=True)
    statut = {}
    for nom, url in FICHIERS.items():
        try:
            contenu = _get(url)
            (d / nom).write_bytes(contenu)
            statut[nom] = f"ok ({len(contenu)} octets)"
        except Exception as e:  # on continue : les autres sources restent utilisables
            statut[nom] = f"ÉCHEC : {e}"
        time.sleep(1)
    # OMS Europe
    try:
        ctx = _contexte_ssl(intermediaire_who=True)
        meta = None
        for _ in range(6):
            meta = json.loads(_get(WHO_EXPORT, ctx))
            if meta.get("status") == "Generated" and meta.get("download_url"):
                break
            time.sleep(10)
        contenu = _get(meta["download_url"], ctx)
        (d / WHO_FICHIER).write_bytes(contenu)
        (d / (WHO_FICHIER + ".meta.json")).write_text(json.dumps(meta, indent=1))
        statut[WHO_FICHIER] = f"ok ({len(contenu)} octets, généré {meta.get('generated_time')})"
    except Exception as e:
        statut[WHO_FICHIER] = f"ÉCHEC : {e}"
    return statut


# --------------------------------------------------------------------------------------
# Lecture
# --------------------------------------------------------------------------------------
def lire_jsonstat(chemin) -> pd.DataFrame:
    """JSON-stat 2.0 (API Eurostat) -> DataFrame (une colonne par dimension + value, status)."""
    d = json.loads(Path(chemin).read_text(encoding="utf-8"))
    ids, tailles = d["id"], d["size"]
    cats = []
    for k in ids:
        idx = d["dimension"][k]["category"]["index"]
        if isinstance(idx, dict):
            codes = sorted(idx, key=idx.get)
        else:
            codes = list(idx)
        cats.append(codes)
    valeurs = d.get("value", {})
    statuts = d.get("status", {})
    if isinstance(valeurs, list):
        valeurs = {str(i): v for i, v in enumerate(valeurs) if v is not None}
    lignes = []
    for cle, v in valeurs.items():
        i = int(cle)
        pos = []
        for t in reversed(tailles):
            pos.append(i % t)
            i //= t
        pos.reverse()
        ligne = {k: cats[j][pos[j]] for j, k in enumerate(ids)}
        ligne["value"] = v
        ligne["status"] = statuts.get(cle) if isinstance(statuts, dict) else None
        lignes.append(ligne)
    return pd.DataFrame(lignes, columns=ids + ["value", "status"])


def _ligne(pays, ind, annee, valeur, source, note=""):
    return {"pays": pays, "indicateur": ind, "annee": int(annee), "valeur": float(valeur),
            "source": source, "note": note}


STATUTS_OCDE = {"B": "rupture de série", "D": "définition différente", "E": "estimation",
                "P": "provisoire"}
STATUTS_ES = {"b": "rupture de série", "c": "confidentiel", "d": "définition différente",
              "e": "estimation", "p": "provisoire", "u": "faible fiabilité"}


def _statut_ocde(s):
    if isinstance(s, str) and s:
        return STATUTS_OCDE.get(s, s)
    return ""


def _statut_es(s):
    if isinstance(s, str) and s:
        return ", ".join(STATUTS_ES.get(c, c) for c in s)
    return ""


def _joindre(*parties):
    return "; ".join(p for p in parties if p)


# ---------------------------------------------------------------- sante_ima30
def _ima30(d: Path) -> list:
    src = "OCDE, Health Care Quality Indicators, flux OECD.ELS.HD:DSD_HCQO@DF_AC(2.1)"
    t = pd.read_csv(d / "oecd_hcqo_ac.csv", low_memory=False)
    t = t[t.MEASURE.isin(["MORTAMIO", "MORTAMII"]) & (t.SEX == "_T") & (t.AGE == "Y_GE45")
          & (t.STATISTICAL_OPERATION == "OBS") & (t.METHODOLOGY == "AGE_SEX_STANDARD")
          & t.REF_AREA.isin(ISO3_VERS_ISO2) & t.OBS_VALUE.notna()]
    out = []
    for iso3, g in t.groupby("REF_AREA"):
        pays = ISO3_VERS_ISO2[iso3]
        chaine = g[g.MEASURE == "MORTAMIO"]
        retenu, type_ = (chaine, "chaînée (linked, décès à l'hôpital et hors hôpital)") if len(chaine) \
            else (g[g.MEASURE == "MORTAMII"], "non chaînée (unlinked, décès dans le même séjour)")
        for _, r in retenu.iterrows():
            out.append(_ligne(pays, "sante_ima30", r.TIME_PERIOD, r.OBS_VALUE, src,
                              _joindre(f"série {type_}", "pour 100 patients" if r.MEASURE ==
                                       "MORTAMIO" else "pour 100 admissions",
                                       _statut_ocde(r.OBS_STATUS))))
        for _, r in g[g.MEASURE == "MORTAMII"].iterrows():
            out.append(_ligne(pays, "sante_ima30_nonchaine", r.TIME_PERIOD, r.OBS_VALUE, src,
                              _joindre("série non chaînée, pour 100 admissions",
                                       _statut_ocde(r.OBS_STATUS))))
    return out


# ---------------------------------------------------------------- sante_antibiotiques
def _antibiotiques(d: Path) -> list:
    src = "OCDE, Health Statistics, flux OECD.ELS.HD:HEALTH_PHMC@DF_PHMC_CONSUM(1.1), ATC J01"
    t = pd.read_csv(d / "oecd_phmc_consum.csv", low_memory=False)
    t = t[(t.PHARMACEUTICAL == "J01") & (t.UNIT_MEASURE == "DDD_10P3HB")
          & t.REF_AREA.isin(ISO3_VERS_ISO2) & t.OBS_VALUE.notna()]
    return [_ligne(ISO3_VERS_ISO2[r.REF_AREA], "sante_antibiotiques", r.TIME_PERIOD, r.OBS_VALUE, src,
                   _joindre("DDD/1 000 hab./jour; repli OCDE (ESAC-Net non téléchargeable)",
                            _statut_ocde(r.OBS_STATUS)))
            for _, r in t.iterrows()]


# ---------------------------------------------------------------- sante_depenses_catastrophiques
def _catastrophiques(d: Path) -> list:
    src = "OMS Europe, European Health Information Gateway, indicateur UHCFP_4 (jeu UHCFP)"
    texte = (d / WHO_FICHIER).read_text(encoding="utf-8-sig")
    i = texte.find('"COUNTRY","YEAR","VALUE"')
    t = pd.read_csv(io.StringIO(texte[i:]))
    t = t[t.COUNTRY.isin(ISO3_VERS_ISO2) & t.VALUE.notna()]
    note = ("% des ménages; dépense catastrophique = reste à charge > 40 % de la capacité à payer "
            "(consommation moins un montant normatif pour alimentation, logement, charges)")
    return [_ligne(ISO3_VERS_ISO2[r.COUNTRY], "sante_depenses_catastrophiques", r.YEAR, r.VALUE,
                   src, note) for _, r in t.iterrows()]


# ---------------------------------------------------------------- sante_attente
def _attente(d: Path) -> list:
    src = "OCDE, Health Care Utilisation – Waiting times, flux OECD.ELS.HD:DSD_HEALTH_PROC@DF_WAITING(1.2)"
    t = pd.read_csv(d / "oecd_waiting.csv", low_memory=False)
    t = t[(t.MEDICAL_PROCEDURE == "CM8151_8153") & (t.WAITING_TIME == "WTSP")
          & t.REF_AREA.isin(ISO3_VERS_ISO2) & t.OBS_VALUE.notna()]
    out = []
    for mesure, ind, lib in [("WAIT_MEAN", "sante_attente", "moyenne"),
                             ("WAIT_MEDIAN", "sante_attente_mediane", "médiane")]:
        for _, r in t[t.MEASURE == mesure].iterrows():
            out.append(_ligne(ISO3_VERS_ISO2[r.REF_AREA], ind, r.TIME_PERIOD, r.OBS_VALUE, src,
                              _joindre(f"jours, {lib}, prothèse de hanche, de l'avis du spécialiste "
                                       "à l'intervention", _statut_ocde(r.OBS_STATUS))))
    # complément EU-SILC
    s = lire_jsonstat(d / "es_hlth_silc_08.json")
    s = s[s.geo.isin(PAYS) & s.value.notna()]
    for _, r in s.iterrows():
        out.append(_ligne(r.geo, "sante_attente_silc", r.time, r.value,
                          "Eurostat hlth_silc_08 (EU-SILC), reason=WLIST, 16 ans et plus",
                          _joindre("% de la population déclarant un besoin d'examen médical non "
                                   "satisfait pour cause de liste d'attente", _statut_es(r.status))))
    return out


# ---------------------------------------------------------------- sante_rd_pharma_ratio
def _rd_pharma(d: Path) -> list:
    b = lire_jsonstat(d / "es_rd_e_berdindr2.json")
    h = lire_jsonstat(d / "es_hlth_sha11_hc.json")
    b = b[b.value.notna()][["geo", "time", "value", "status"]].rename(
        columns={"value": "berd", "status": "st_b"})
    h = h[h.value.notna()][["geo", "time", "value", "status"]].rename(
        columns={"value": "hc51", "status": "st_h"})
    m = b.merge(h, on=["geo", "time"])
    m = m[m.geo.isin(PAYS) & (m.hc51 > 0)]
    src = ("Eurostat rd_e_berdindr2 (BERD, NACE C21, M EUR) / Eurostat hlth_sha11_hc "
           "(HC.5.1, M EUR)")
    out = []
    for _, r in m.iterrows():
        note = _joindre("%; BERD branche pharmaceutique / dépense courante en produits "
                        "pharmaceutiques et autres biens médicaux non durables (HC.5.1, tous financeurs)",
                        f"BERD {r.berd:.1f} M EUR, HC.5.1 {r.hc51:.1f} M EUR",
                        ("BERD: " + _statut_es(r.st_b)) if _statut_es(r.st_b) else "",
                        ("HC51: " + _statut_es(r.st_h)) if _statut_es(r.st_h) else "")
        out.append(_ligne(r.geo, "sante_rd_pharma_ratio", r.time, 100 * r.berd / r.hc51, src, note))
    return out


# ---------------------------------------------------------------- sante_surmortalite_12m
def _surmortalite(d: Path) -> list:
    t = lire_jsonstat(d / "es_demo_mexrt.json")
    t = t[t.geo.isin(PAYS) & t.value.notna()].copy()
    t["annee"] = t.time.str[:4].astype(int)
    out = []
    for (geo, an), g in t.groupby(["geo", "annee"]):
        if len(g) != 12:
            continue  # année civile incomplète : non calculée
        st = sorted({s for s in g.status.dropna() if s})
        out.append(_ligne(geo, "sante_surmortalite_12m", an, g.value.mean(),
                          "Eurostat demo_mexrt (surmortalité mensuelle, % vs moyenne 2016-2019)",
                          _joindre("moyenne arithmétique des 12 taux mensuels de l'année civile, en %",
                                   ("statuts mensuels: " + _statut_es("".join(st))) if st else "")))
    return out


# ---------------------------------------------------------------- sante_inegalite_densite
def _cv(x, w=None):
    if w is None:
        w = [1.0] * len(x)
    sw = sum(w)
    m = sum(wi * xi for wi, xi in zip(w, x)) / sw
    var = sum(wi * (xi - m) ** 2 for wi, xi in zip(w, x)) / sw
    return math.sqrt(var) / m


def _codes_nuts(d: Path) -> dict:
    """{version: {pays: ensemble des codes NUTS 2 (hors extra-regio ZZ)}} d'après GISCO."""
    res = {}
    for v in VERSIONS_NUTS:
        f = d / f"gisco_nuts_{v}.csv"
        if not f.exists():
            continue
        t = pd.read_csv(f, dtype=str, keep_default_na=False)
        codes = t.NUTS_ID[(t.NUTS_ID.str.len() == 4) & ~t.NUTS_ID.str.endswith("ZZ")]
        par_pays = {}
        for c in codes:
            par_pays.setdefault(c[:2], set()).add(c)
        res[v] = par_pays
    return res


def _densites_regionales(d: Path) -> pd.DataFrame:
    """Densité (P_HTHAB) et effectif (NR) de médecins par région NUTS 2 et année.

    hlth_rs_physreg (série courante, prioritaire) complétée par hlth_rs_prsrg
    (série historique 1993-2021, ISCO08 OC221 = médecins) pour les couples
    (région, année) absents de la première.
    """
    morceaux = []
    for fichier, lib in [("es_hlth_rs_physreg.json", "physreg"), ("es_hlth_rs_prsrg.json", "prsrg")]:
        if not (d / fichier).exists():
            continue
        t = lire_jsonstat(d / fichier)
        t = t[t.value.notna() & (t.geo.str.len() == 4) & ~t.geo.str.endswith("ZZ")]
        dens = t[t.unit == "P_HTHAB"][["geo", "time", "value", "status"]].rename(
            columns={"value": "dens"})
        nr = t[t.unit == "NR"][["geo", "time", "value"]].rename(columns={"value": "nr"})
        x = dens.merge(nr, on=["geo", "time"], how="left")
        x["jeu"] = lib
        morceaux.append(x)
    x = pd.concat(morceaux, ignore_index=True)
    x = x.drop_duplicates(["geo", "time"], keep="first")  # physreg d'abord
    x["pays"] = x.geo.str[:2]
    return x[x.pays.isin(PAYS)]


def _inegalite(d: Path) -> list:
    x = _densites_regionales(d)
    nuts = _codes_nuts(d)
    pop = lire_jsonstat(d / "es_demo_r_pjanaggr3.json")
    pop = pop[pop.value.notna()][["geo", "time", "value"]].rename(columns={"value": "pop"})
    pop = pop.set_index(["geo", "time"])["pop"]
    out = []
    for (pays, an), g in x.groupby(["pays", "time"]):
        dispo = set(g.geo)
        choix = None
        for v in VERSIONS_NUTS:  # du plus récent au plus ancien
            k = nuts.get(v, {}).get(pays, set())
            if len(k) < 2:
                continue
            cov = len(dispo & k) / len(k)
            if choix is None or cov > choix[1] + 1e-12:
                choix = (v, cov, k)
            if cov == 1:
                break
        if choix is None or choix[1] < 0.9:
            continue  # couverture insuffisante d'un découpage NUTS cohérent
        v, cov, k = choix
        sel = g[g.geo.isin(k)]
        n = len(sel)
        if n < 2:
            continue
        dens = sel.dens.tolist()
        manquants = sorted(k - dispo)
        jeux = "+".join(sorted(set(sel.jeu)))
        base = _joindre(f"NUTS {v}, {n}/{len(k)} régions"
                        + (f" (manquantes: {' '.join(manquants)})" if manquants else ""),
                        f"jeu {jeux}")
        st = sorted({c for s in sel.status.dropna() for c in s})
        stn = ("statuts: " + _statut_es("".join(st))) if st else ""
        src = (f"Eurostat hlth_rs_{'physreg' if jeux == 'physreg' else jeux.replace('+', '/')}"
               " (médecins pour 100 000 hab., NUTS 2)")
        out.append(_ligne(pays, "sante_inegalite_densite", an, _cv(dens), src,
                          _joindre("CV non pondéré (écart-type de population / moyenne simple)",
                                   base, stn)))
        # pondération : population demo_r_pjanaggr3 si toutes les régions y figurent,
        # sinon population implicite NR x 100 000 / densité tirée du même jeu
        cles = list(zip(sel.geo, sel.time))
        if all(c in pop.index for c in cles):
            w = [float(pop[c]) for c in cles]
            wlib = "poids: population au 1er janvier (demo_r_pjanaggr3)"
        elif sel.nr.notna().all():
            w = (sel.nr * 1e5 / sel.dens).tolist()
            wlib = "poids: population implicite = effectif / densité x 100 000 (codes NUTS absents de demo_r_pjanaggr3)"
        else:
            continue
        out.append(_ligne(pays, "sante_inegalite_densite_pond", an, _cv(dens, w),
                          src + " et demo_r_pjanaggr3",
                          _joindre("CV pondéré par la population", wlib, base, stn)))
    return out


EXTRACTEURS = {
    "sante_ima30": _ima30,
    "sante_antibiotiques": _antibiotiques,
    "sante_depenses_catastrophiques": _catastrophiques,
    "sante_attente": _attente,
    "sante_rd_pharma_ratio": _rd_pharma,
    "sante_surmortalite_12m": _surmortalite,
    "sante_inegalite_densite": _inegalite,
}


def extraire(dossier_brut=DOSSIER_BRUT_DEFAUT) -> pd.DataFrame:
    """Lit les fichiers bruts et renvoie le DataFrame long (pays, indicateur, annee, valeur, source, note)."""
    d = Path(dossier_brut)
    lignes = []
    for nom, f in EXTRACTEURS.items():
        try:
            lignes += f(d)
        except FileNotFoundError as e:
            print(f"[{nom}] fichier brut absent, indicateur ignoré : {e}")
    df = pd.DataFrame(lignes, columns=["pays", "indicateur", "annee", "valeur", "source", "note"])
    df = df[df.pays.isin(PAYS)]
    df = df.sort_values(["indicateur", "pays", "annee"]).reset_index(drop=True)
    return df


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--dossier", default=str(DOSSIER_BRUT_DEFAUT))
    ap.add_argument("--sans-telechargement", action="store_true")
    ap.add_argument("--sortie", default=str(SORTIE_CSV))
    a = ap.parse_args()
    if not a.sans_telechargement:
        for k, v in telecharger(a.dossier).items():
            print(f"{k}: {v}")
    df = extraire(a.dossier)
    df.to_csv(a.sortie, index=False, float_format="%.6g")
    print(f"{len(df)} lignes écrites dans {a.sortie}")
    print(df.groupby("indicateur").agg(pays=("pays", "nunique"), debut=("annee", "min"),
                                       fin=("annee", "max"), n=("valeur", "size")).to_string())


if __name__ == "__main__":
    main()
