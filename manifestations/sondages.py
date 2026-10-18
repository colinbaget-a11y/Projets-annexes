"""
Collecte des sondages d'intentions de vote : France, Italie, Royaume-Uni, Allemagne, Espagne.

Sources :
  - Wikipédia en anglais, pages « Opinion polling for the … election » : un tableau par année ou
    par période, avec dates de terrain, institut et intentions de vote par parti ;
  - Allemagne : wahlrecht.de, une page par institut (archives depuis 1998).

    python sondages.py               télécharge (si absent du cache) et écrit sondages.csv.gz
    python sondages.py --rafraichir  retélécharge tout

Sortie sondages.csv.gz (format long) : pays, page, institut, date (fin du terrain), parti, part (%),
echantillon, scenario (France, présidentielle : un sondage teste plusieurs listes de candidats ;
0 ailleurs). Les résultats d'élections présents dans les tableaux sont écartés.
"""
import hashlib
import io
import re
import urllib.parse
import sys
import time
import urllib.request
from datetime import date
from pathlib import Path

import pandas as pd
from lxml import html as lhtml

ICI = Path(__file__).resolve().parent
CACHE = Path("/tmp/claude-0/-home-user-Projets-annexes/935fc156-45bd-500a-b52a-e7e4ee23abb6"
             "/scratchpad/manifestations/brut")
UA = "recherche-sondages/1.0 (etude academique ; python urllib)"
WIKI = "https://en.wikipedia.org/wiki/"
PAGES = {
    "UK": ["Opinion_polling_for_the_2010_United_Kingdom_general_election",
           "Opinion_polling_for_the_2015_United_Kingdom_general_election",
           "Opinion_polling_for_the_2017_United_Kingdom_general_election",
           "Opinion_polling_for_the_2019_United_Kingdom_general_election",
           "Opinion_polling_for_the_2024_United_Kingdom_general_election",
           "Opinion_polling_for_the_next_United_Kingdom_general_election"],
    "ES": ["Opinion_polling_for_the_2008_Spanish_general_election",
           "Opinion_polling_for_the_2011_Spanish_general_election",
           "Opinion_polling_for_the_2015_Spanish_general_election",
           "Opinion_polling_for_the_2016_Spanish_general_election",
           "Opinion_polling_for_the_April_2019_Spanish_general_election",
           "Opinion_polling_for_the_November_2019_Spanish_general_election",
           "Opinion_polling_for_the_2023_Spanish_general_election",
           "Opinion_polling_for_the_next_Spanish_general_election"],
    "IT": ["Opinion_polling_for_the_2008_Italian_general_election",
           "Opinion_polling_for_the_2013_Italian_general_election",
           "Opinion_polling_for_the_2018_Italian_general_election",
           "Opinion_polling_for_the_2022_Italian_general_election",
           "Opinion_polling_for_the_next_Italian_general_election"],
    "FR": ["Opinion_polling_for_the_2007_French_presidential_election",
           "Opinion_polling_for_the_2019_European_Parliament_election_in_France",
           "2024_European_Parliament_election_in_France",            # sondages sur la page de l'élection
           "Opinion_polling_for_the_2024_French_legislative_election",
           "Next_French_legislative_election",
           "Opinion_polling_for_the_2027_French_presidential_election"],
}
# France : les pages de Wikipédia en français sont bien plus complètes entre deux élections
WIKI_FR = "https://fr.wikipedia.org/wiki/"
PAGES_FR = ["Liste_de_sondages_sur_l'élection_présidentielle_française_de_2007",
            "Liste_de_sondages_sur_l'élection_présidentielle_française_de_2012",
            "Liste_de_sondages_sur_l'élection_présidentielle_française_de_2022",
            "Liste_de_sondages_sur_l'élection_présidentielle_française_de_2027"]
MOIS_FR = {"janv": 1, "févr": 2, "fevr": 2, "mars": 3, "avr": 4, "mai": 5, "juin": 6, "juil": 7, "août": 8,
           "aout": 8, "sept": 9, "oct": 10, "nov": 11, "déc": 12, "dec": 12}
WAHLRECHT = "https://www.wahlrecht.de/umfragen/"
INSTITUTS_DE = ["allensbach", "verian", "forsa", "politbarometer", "gms", "dimap", "insa", "yougov"]
MOIS = {m: i + 1 for i, m in enumerate(["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep",
                                         "oct", "nov", "dec"])}
NON_PARTIS = re.compile(r"date|poll|firm|organi|sample|lead|turnout|undecided|don't|dk|margin|"
                        r"commission|client|source|fieldwork|area|scenario|abst|none|^n$", re.I)


def telecharger(url, fichier, rafraichir=False):
    f = CACHE / fichier
    if f.exists() and not rafraichir:
        return f.read_bytes()
    for essai in range(4):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=120) as r:
                contenu = r.read()
            f.write_bytes(contenu)
            time.sleep(1)
            return contenu
        except OSError as e:
            if getattr(e, "code", None) == 404:
                return b""
            time.sleep(5 * (essai + 1))
    raise RuntimeError(f"échec : {url}")


def nombre(x):
    """Premier nombre d'une cellule (« 28.7 122/125 » -> 28.7 ; « 37% » -> 37)."""
    m = re.search(r"\d+(?:[.,]\d+)?", str(x).replace("−", "-"))
    return float(m.group().replace(",", ".")) if m else None


def date_fin(texte):
    """Fin du terrain : (année explicite ou None, mois, jour). « 19–23 Dec », « 28 Nov – 2 Dec 2011 »."""
    t = re.sub(r"\[.*?\]", "", str(texte)).strip()
    fin = re.split(r"[–—-]", t)[-1].strip()
    an = re.search(r"(19|20)\d{2}", fin) or re.search(r"(19|20)\d{2}", t)
    mois = re.search(r"[A-Za-z]{3,}", fin) or re.search(r"[A-Za-z]{3,}", t)
    jour = re.search(r"\b\d{1,2}\b", re.sub(r"(19|20)\d{2}", "", fin))
    if not (mois and jour) or mois.group()[:3].lower() not in MOIS:
        return None
    return (int(an.group()) if an else None), MOIS[mois.group()[:3].lower()], int(jour.group())


def annotation(r, inst):
    """Ligne de commentaire fusionnée sur toute la largeur (« X annonce sa candidature (date) »)."""
    valeurs = {str(v) for v in r.values if str(v) not in ("nan", "")}
    return len(valeurs) <= 2 and len(inst) > 30


def lire_wikipedia(pays, page, contenu):
    doc = lhtml.fromstring(contenu)
    lignes = []
    an_page = re.search(r"(19|20)\d{2}", page)
    annee = int(an_page.group()) if an_page else None      # à défaut de titre de section daté
    mois_prec, k, hors_sujet = None, 0, False
    for el in doc.iter("h2", "h3", "h4", "table"):
        if el.tag != "table":
            titre = el.text_content()
            an = re.search(r"\b(19|20)\d{2}\b", titre)
            if an:
                annee, mois_prec = int(an.group()), None
            # tableaux qui ne sont pas des intentions de vote nationales
            hors_sujet = bool(re.search(r"preference|preferred|likelihood|coalition|leader|approv|seat|"
                                        r"sub-national|constituenc|region|hypothetical|second round|run-?off|"
                                        r"by nation|scotland|wales|london|northern ireland", titre, re.I))
            continue
        if hors_sujet or "wikitable" not in (el.get("class") or ""):
            continue
        # en-têtes de partis réduits à un logo ou à une couleur : on prend le titre du lien ou l'alt
        for th in el.xpath(".//tr[position()<=2]/th"):
            if not th.text_content().strip():
                nom = (th.xpath(".//a/@title") or th.xpath(".//img/@alt") or [""])[0]
                if nom:
                    for enfant in list(th):
                        th.remove(enfant)
                    th.text = nom
        try:
            t = pd.read_html(io.StringIO(lhtml.tostring(el, encoding="unicode")))[0]
        except (ValueError, IndexError):
            continue
        cols = [c[0] if isinstance(c, tuple) else c for c in t.columns]
        t.columns = [str(c) for c in cols]
        c_date = next((c for c in t.columns if re.search(r"date|fieldwork", c, re.I)), None)
        c_inst = next((c for c in t.columns if re.search(r"poll|firm|organi", c, re.I)), None)
        if c_date is None or c_inst is None:
            continue
        c_n = next((c for c in t.columns if re.search(r"sample", c, re.I)), None)
        k += 1
        partis = [c for c in dict.fromkeys(t.columns) if not NON_PARTIS.search(c) and c not in (c_date, c_inst)
                  and not c.startswith("Unnamed") and c.lower() != "others"]
        for i, r in t.iterrows():
            inst = str(r[c_inst])
            if re.search(r"election|result", inst, re.I) or inst == c_inst or annotation(r, inst):
                continue
            dd = date_fin(r[c_date])
            if dd is None:
                continue
            an, mois, jour = dd
            # tableaux du plus récent au plus ancien : un passage de janvier à décembre fait reculer l'année
            if an is not None:
                annee = an
            elif mois_prec is not None and annee is not None and mois > mois_prec + 6:
                annee -= 1
            mois_prec = mois
            if annee is None:
                continue
            try:
                d = date(annee, mois, jour)
            except ValueError:
                continue
            for p in partis:
                v = r[p]
                if isinstance(v, pd.Series):
                    v = v.iloc[0]
                x = nombre(v)
                if x is not None and 0 <= x <= 70:
                    lignes.append((pays, page, re.sub(r"\[.*?\]", "", inst).strip(), d, p, x,
                                   nombre(r[c_n]) if c_n else None, f"{k}.{i}"))
    return lignes


def date_fin_fr(texte):
    """« 25-29 septembre », « 28 septembre-1er octobre 2023 » -> (année ou None, mois, jour)."""
    t = re.sub(r"\[.*?\]", "", str(texte)).lower().replace("1er", "1").strip()
    fin = re.split(r"[–—-]", t)[-1].strip()
    an = re.search(r"(19|20)\d{2}", fin) or re.search(r"(19|20)\d{2}", t)
    mois = None
    for zone in (fin, t):
        for mot in re.findall(r"[a-zéû]{3,}", zone):
            mois = next((v for k, v in MOIS_FR.items() if mot.startswith(k)), None)
            if mois:
                break
        if mois:
            break
    jour = re.search(r"\b\d{1,2}\b", re.sub(r"(19|20)\d{2}", "", fin))
    if mois is None or jour is None:
        return None
    return (int(an.group()) if an else None), mois, int(jour.group())


def lire_wikipedia_fr(page, contenu):
    """Premier tour de la présidentielle : une ligne par scénario de candidats."""
    doc = lhtml.fromstring(contenu)
    lignes, annee, mois_prec, premier_tour = [], None, None, False
    an_page = re.search(r"(19|20)\d{2}", page)
    for el in doc.iter("h2", "h3", "h4", "table"):
        if el.tag != "table":
            titre = el.text_content().lower()
            if "premier tour" in titre:
                premier_tour = True
            elif "second tour" in titre or "notes" in titre:
                premier_tour = False
            an = re.search(r"\b(19|20)\d{2}\b", titre)
            if an:
                annee, mois_prec = int(an.group()), None
            continue
        if not premier_tour or "wikitable" not in (el.get("class") or ""):
            continue
        try:
            t = pd.read_html(io.StringIO(lhtml.tostring(el, encoding="unicode")), thousands=None)[0]
        except (ValueError, IndexError):
            continue
        cols = []
        for c in t.columns:
            c = c if isinstance(c, tuple) else (c, c)
            cols.append(str(c[1] if str(c[0]).startswith("Unnamed") else c[0]))
        cols = ["Date" if re.match(r"Dates?$", c) else c for c in cols]
        t.columns = cols
        if "Sondeur" not in t or "Date" not in t:
            continue
        candidats = [c for c in dict.fromkeys(cols) if c not in ("Sondeur", "Date", "Échantillon", "Autres")
                     and not c.startswith("Unnamed")]
        if annee is None and an_page:
            annee = int(an_page.group())
        for i, r in t.iterrows():
            inst = str(r["Sondeur"])
            if inst in ("Sondeur", "nan") or re.search(r"élection|résultat", inst, re.I) or annotation(r, inst):
                continue
            dd = date_fin_fr(r["Date"] if not isinstance(r["Date"], pd.Series) else r["Date"].iloc[0])
            if dd is None:
                continue
            an, mois, jour = dd
            if an is not None:
                annee = an
            elif mois_prec is not None and mois > mois_prec + 6:
                annee -= 1
            mois_prec = mois
            try:
                d = date(annee, mois, jour)
            except (ValueError, TypeError):
                continue
            for c in candidats:
                v = r[c]
                if isinstance(v, pd.Series):
                    v = v.iloc[0]
                x = nombre(v)
                if x is not None and 0 <= x <= 70:
                    lignes.append(("FR", "fr:" + page, re.sub(r"\[.*?\]", "", inst).strip(), d,
                                   re.sub(r"\[.*?\]", "", c).strip(), x, nombre(r.get("Échantillon")), i))
    return lignes


def lire_wahlrecht(institut, contenu):
    t = None
    for tab in pd.read_html(io.StringIO(contenu.decode("utf-8", "replace"))):
        if tab.shape[0] > 5 and tab.shape[1] > 6:
            t = tab
            break
    if t is None:
        return []
    t.columns = [str(c[0] if isinstance(c, tuple) else c) for c in t.columns]
    c_date = t.columns[0]
    partis = [c for c in t.columns if re.match(r"(CDU|SPD|GR|FDP|LINKE|PDS|AfD|BSW|FW|PIRATEN|Sonstige)", c)]
    lignes = []
    for _, r in t.iterrows():
        m = re.match(r"(\d{2})\.(\d{2})\.(\d{4})", str(r[c_date]))
        if not m:
            continue
        d = date(int(m.group(3)), int(m.group(2)), int(m.group(1)))
        for p in partis:
            x = nombre(r[p])
            if x is not None and "%" in str(r[p]):
                lignes.append(("DE", "wahlrecht.de", institut, d, p.replace("Ü", "UE").replace("GRÜNE", "GRUENE"), x,
                               None, 0))
    return lignes


def main():
    rafraichir = "--rafraichir" in sys.argv
    CACHE.mkdir(parents=True, exist_ok=True)
    lignes = []
    for pays, pages in PAGES.items():
        for page in pages:
            contenu = telecharger(WIKI + page, f"wiki_{page}.html", rafraichir)
            if contenu:
                l = lire_wikipedia(pays, page, contenu)
                print(f"{pays} {page}: {len(l)} valeurs")
                lignes += l
    for page in PAGES_FR:
        nom = "frwiki_" + hashlib.md5(page.encode()).hexdigest()[:10] + ".html"
        contenu = telecharger(WIKI_FR + urllib.parse.quote(page), nom, rafraichir)
        if contenu:
            l = lire_wikipedia_fr(page, contenu)
            print(f"FR fr:{page}: {len(l)} valeurs")
            lignes += l
    for inst in INSTITUTS_DE:
        contenu = telecharger(f"{WAHLRECHT}{inst}.htm", f"de_{inst}.htm", rafraichir)
        pages = [(f"{inst}.htm", contenu)]
        for lien in sorted(set(re.findall(rf'href="({inst}/\d{{4}}\.htm)"', contenu.decode("utf-8", "replace")))):
            pages.append((lien, telecharger(WAHLRECHT + lien, "de_" + lien.replace("/", "_"), rafraichir)))
        n = 0
        for nom, c in pages:
            if c:
                l = lire_wahlrecht(inst, c)
                n += len(l)
                lignes += l
        print(f"DE {inst}: {n} valeurs ({len(pages)} pages)")
    s = pd.DataFrame(lignes, columns=["pays", "page", "institut", "date", "parti", "part", "echantillon",
                                      "scenario"])
    s = s.drop_duplicates(["pays", "page", "institut", "date", "parti", "part", "scenario"])
    s.to_csv(ICI / "sondages.csv.gz", index=False)
    print(s.groupby("pays").agg(debut=("date", "min"), fin=("date", "max"), sondages=("date", "size")))


if __name__ == "__main__":
    main()
