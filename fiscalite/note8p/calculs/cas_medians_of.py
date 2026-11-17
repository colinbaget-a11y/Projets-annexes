"""Cinq ménages « médians » au droit actuel (OpenFisca-France 176.1, droit des revenus 2025), sans niche.
Lancer depuis fiscalite/ : python3.13 note8p/calculs/cas_medians_of.py -> note8p/sorties/cas_medians_of.csv
Hypothèses [H/E] : salaire net médian du secteur privé 2023, 2 183 € par mois en EQTP (Insee) ; le salaire brut est
calé pour donner ce net après cotisations, CSG et CRDS. Pension : 1 500 € brut par mois par retraité, ordre de grandeur
de la médiane (la DREES publie la moyenne de droit direct, 1 666 € brut fin 2023, pas la médiane) [H]. Smic 2025.
"""
import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import ircsg4_openfisca as OF  # noqa: E402

NET_MED = 2183.0 * 12
o0 = None
lo, hi = 25000.0, 45000.0
for _ in range(40):
    m = (lo + hi) / 2
    o = OF.simule([("sal", m, 1985)])
    net = o["bases"][0] - o["csg"] - o["crds"]
    lo, hi = (m, hi) if net < NET_MED else (lo, m)
BRUT_MED = (lo + hi) / 2
PENS = 1500.0 * 12
ENF = ("2016-03-01", "2019-03-01")
CAS = [
    ("ret_couple", "Couple de retraités, chacun la pension médiane", [("ret", PENS, 1955), ("ret", PENS, 1955)], ()),
    ("couple_2e", "Couple, deux enfants, chacun le salaire médian", [("sal", BRUT_MED, 1985), ("sal", BRUT_MED, 1985)], ENF),
    ("celib", "Célibataire au salaire médian", [("sal", BRUT_MED, 1985)], ()),
    ("smic_couple", "Couple de smicards sans enfant", [("sal", OF.SMIC, 1990), ("sal", OF.SMIC, 1990)], ()),
    ("mono_2e", "Couple, deux enfants, un seul salaire médian", [("sal", BRUT_MED, 1985), ("sal", 0.0, 1985)], ENF),
]
rows = []
for cle, lib, ad, enf in CAS:
    r = OF.calcule(ad, enf, {}, False)
    c = OF.charge(r)
    rows.append(dict(cle=cle, libelle=lib, enfants=len(enf), bruts=";".join(f"{a[1]:.2f}" for a in ad),
                     statuts=";".join(a[0] for a in ad), bases=";".join(f"{b:.2f}" for b in r["bases"]),
                     charge=round(c["total"], 2), ir=round(c["ir_net"], 2), csg_crds=round(c["csg_crds"], 2)))
    print(cle, rows[-1]["charge"], rows[-1]["bases"], flush=True)
out = Path(__file__).resolve().parent.parent / "sorties" / "cas_medians_of.csv"
with open(out, "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=rows[0].keys())
    w.writeheader()
    w.writerows(rows)
print("brut médian", round(BRUT_MED))
