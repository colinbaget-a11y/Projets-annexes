"""
Regroupement des partis (libellés des tableaux de sondages) en blocs comparables entre pays, et parti
du chef de gouvernement à chaque date.

Blocs : droite radicale, droite, centre, gauche, gauche radicale, autres (régionalistes,
inclassables comme le M5S, divers). Les libellés non reconnus vont dans « non classé » et sont listés
par analyse.py pour contrôle.
"""
import re

BLOCS = ["droite radicale", "droite", "centre", "gauche", "gauche radicale", "autres"]

REGLES = {
    "FR": [
        ("droite radicale", r"\b(FN|RN|REC|Reconq|Zemmour|Le ?Pen|Bardella|Villiers|MPF|DLF|Dupont|LP|UPR|"
                            r"Asselineau|Philippot|Patriotes|UDR|Ciotti)\b"),
        ("autres", r"\b(GE/MEI|UDMF|R!|DSV)"),
        ("droite", r"\b(UMP|LR|LC|Sarkozy|Fillon|P[ée]cresse|Wauquiez|Retailleau|Bertrand|DVD|Lisnard|NE)\b"),
        ("centre", r"\b(UDF|Bayrou|MoDem|LREM|LaREM|Ens|Renew|Renaissance|Macron|Horizons|Philippe|Attal|"
                   r"UDI|Hayer|Loiseau|ENS|Lepage|DVC|Villepin)\b"),
        ("gauche radicale", r"\b(LFI|FI|M[ée]lenchon|PCF|Buffet|Roussel|LO|Laguiller|Arthaud|LCR|NPA|"
                            r"Besancenot|Poutou|Bov[ée]|Aubry|EXG|Schivardi|Ruffin)\b"),
        ("gauche", r"\b(PS|Royal|Hollande|Hamon|Glucksmann|PP|EELV|LV|Voynet|Jadot|Tondelier|G\.s|PRG|"
                   r"NFP|NUPES|EAC|Les Verts|Hidalgo|Faure|ND|ECO)\b"),
        ("autres", r"\b(DIV|CPNT|Nihous|PA|Lassalle|AJ|GJ|AR|DVG|Others?)\b"),
    ],
    "UK": [
        ("droite radicale", r"^(UKIP|Brx|Ref|Reform|BNP)\b"),
        ("droite", r"^(Con)\b"),
        ("centre", r"^(LD|Chg)\b"),
        ("gauche", r"^(Lab|Grn|Green)\b"),
        ("autres", r"^(SNP|PC|SNP / PC|RB|DUP|UUP|SDLP|SF|All|GPNI|TUV|Others?)\b"),
    ],
    "DE": [
        ("droite radicale", r"^AfD"),
        ("droite", r"^(CDU|FW)"),
        ("centre", r"^FDP"),
        ("gauche", r"^(SPD|GRUENE|GR)"),
        ("gauche radicale", r"^(LINKE|PDS|BSW)"),
        ("autres", r"^(PIRATEN|Sonstige)"),
    ],
    "ES": [
        ("droite radicale", r"^(Vox|SALF)\b"),
        ("droite", r"^(PP\b|UPN\b|NA\+|PAR\b)"),
        ("centre", r"^(Cs|C's|CS|UPyD|UPYD)\b"),
        ("gauche", r"^(PSOE)\b"),
        ("gauche radicale", r"^(Podemos|Unidas Podemos|Unidos Podemos|IU|Sumar|M[áa]s Pa[íi]s|Comprom[íi]s|"
                            r"EQUO)"),
        ("autres", r"^(ERC|Junts|JxCat|CiU|PDeCAT|CDC|DiL|CUP|PNV|EH Bildu|Bildu|Amaiur|BNG|CC|CCa|PRC|"
                   r"Ger[oa] Bai|TE|PACMA|EV|FA|Adelante)"),
    ],
    "IT": [
        ("droite radicale", r"^(FdI|LN|Lega|Italexit|CPI|FN)\b"),
        ("droite radicale", r"^(LD|La Destra)\b"),
        ("droite", r"^(FI|PdL|CDX|NcI|PdL/ FI|Centre-right|C!|NM|AN)"),
        ("centre", r"^(UdC|UDC|NCD|AP|CP/ AP|SC|A|IV|\+E|\+E–A|FLI|With Monti|Az|IC|CI|CD)\b"),
        ("gauche", r"^(PD|CSX|IdV|Italy\. Common Good|Centre-left|Ulivo)"),
        ("gauche radicale", r"^(SEL|SI|LeU|MDP|Art\.1|RC|PRC|PaP|EV|AVS|SEL/ SI|Civil Revolution|SA|FdV|PdCI|UP)\b"),
        ("autres", r"^(M5S|Five Star|Oth|VTR)"),
    ],
}
EXCLUS = re.compile(r"approve|disapprove|not sure|majority|undecided|none|abst|^abs\.|corbyn|theresa may|"
                    r"farron|cameron|osborne|boris johnson|nuttall", re.I)

# parti du chef de gouvernement (France : parti du président), par période (début inclus)
GOUVERNEMENT = {
    "FR": [("1995-05-17", "droite"), ("2012-05-15", "gauche"), ("2017-05-14", "centre")],
    "UK": [("1997-05-02", "gauche"), ("2010-05-11", "droite"), ("2024-07-05", "gauche")],
    "DE": [("1998-10-27", "gauche"), ("2005-11-22", "droite"), ("2021-12-08", "gauche"), ("2025-05-06", "droite")],
    "ES": [("2004-04-17", "gauche"), ("2011-12-21", "droite"), ("2018-06-02", "gauche")],
    "IT": [("2006-05-17", "gauche"), ("2008-05-08", "droite"), ("2011-11-16", None), ("2013-04-28", "gauche"),
           ("2018-06-01", None), ("2022-10-22", "droite radicale")],   # None : technocrate ou coalition M5S
}


def bloc(pays, parti):
    if EXCLUS.search(parti):
        return None
    for nom, motif in REGLES[pays]:
        if re.search(motif, parti):
            return nom
    return "non classé"


def gouvernement(pays, jour):
    courant = None
    for debut, b in GOUVERNEMENT[pays]:
        if str(jour) >= debut:
            courant = b
    return courant
