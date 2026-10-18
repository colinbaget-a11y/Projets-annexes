"""
Collecte des sondages d'intentions de vote : France, Italie, Royaume-Uni, Allemagne, Espagne.

Sources :
  - Wikipédia en anglais, pages « Opinion polling for the … election » : un tableau par année ou
    par période, avec dates de terrain, institut et intentions de vote par parti ;
  - Allemagne : wahlrecht.de, une page par institut (archives depuis 1998).

    python sondages.py               télécharge (si absent du cache) et écrit sondages.csv.gz
    python sondages.py --rafraichir  retélécharge tout

Sortie sondages.csv.gz (format long) : pays, page, institut, date (fin du terrain), parti, part (%),
echantillon. Les résultats d'élections présents dans les tableaux sont écartés.
"""
import io
import re
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


def lire_wikipedia(pays, page, contenu):
    doc = lhtml.fromstring(contenu)
    lignes = []
    an_page = re.search(r"(19|20)\d{2}", page)
    annee = int(an_page.group()) if an_page else None      # à défaut de titre de section daté
    mois_prec = None
    for el in doc.iter("h2", "h3", "h4", "table"):
        if el.tag != "table":
            an = re.search(r"\b(19|20)\d{2}\b", el.text_content())
            if an:
                annee, mois_prec = int(an.group()), None
            continue
        if "wikitable" not in (el.get("class") or ""):
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
        partis = [c for c in dict.fromkeys(t.columns) if not NON_PARTIS.search(c) and c not in (c_date, c_inst)
                  and not c.startswith("Unnamed") and c.lower() != "others"]
        for _, r in t.iterrows():
            inst = str(r[c_inst])
            if re.search(r"election|result", inst, re.I) or inst == c_inst:
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
                                   nombre(r[c_n]) if c_n else None))
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
                               None))
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
    s = pd.DataFrame(lignes, columns=["pays", "page", "institut", "date", "parti", "part", "echantillon"])
    s = s.drop_duplicates(["pays", "institut", "date", "parti", "part"])
    s.to_csv(ICI / "sondages.csv.gz", index=False)
    print(s.groupby("pays").agg(debut=("date", "min"), fin=("date", "max"), sondages=("date", "size")))


if __name__ == "__main__":
    main()
