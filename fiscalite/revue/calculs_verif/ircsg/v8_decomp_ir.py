"""Faisabilité : décomposer le passage de l'IR actuel (80 Md€ sur les revenus au barème) au barème de l'IR appliqué à
chaque adulte sur l'assiette large (197 Md€), sur les foyers purs du modèle. Règles 2024 (brochure 2025) ; niches
ignorées ; retraités : RFR approché (pension × 0,95 × 0,9, abattement de 10 % plafonné à 4 399 € par foyer (brochure 2025), chiffre
non vérifié ; abattement des plus de 65 ans). Lancer depuis fiscalite/."""
import sys
import numpy as np
sys.path[:0] = ["/home/user/Projets-annexes/fiscalite/synthese"]
import modele_purs as M
IRS, IRT = [0, 11497, 29315, 83823, 180294], [0, .11, .30, .41, .45]
def bar(q):
    return sum(t * np.clip(np.minimum(q, h) - s, 0, None) for s, h, t in zip(IRS, IRS[1:] + [np.inf], IRT))
def ir(r, couple, n, isole=False, decote=True, qf=True):
    p0 = 2.0 if couple else 1.0
    if not qf:
        n = 0
    if couple:
        p = 2 + 0.5 * min(n, 2) + max(n - 2, 0); cap = 1791 * 2 * (p - p0)
    elif isole and n >= 1:
        p = 2.0; cap = 4224.0
    else:
        p, cap = 1.0, 0.0
    i0 = p0 * bar(r / p0); i1 = np.maximum(p * bar(r / p), i0 - cap)
    if decote:
        i1 = i1 - np.clip((1470 if couple else 889) - 0.4525 * i1, 0, None)
    return np.clip(i1, 0, None)
def abat_age(r_pers):
    return np.where(r_pers <= 17510, 2796, np.where(r_pers <= 28170, 1398, 0))
def total(f):
    return sum((w * f(nom, g, parts, k)).sum() for nom, g, fam, w, parts, k in M.TYPES) / 1e9
ZN = M.ZN
def rfr(nom, g, parts):
    if g == "A":
        return M.RFR_A
    brut = ZN
    r = brut * 0.95 - np.minimum(0.10 * brut * 0.95, 4399)
    n = len(parts)
    return np.clip(r - n * abat_age(r / n), 0, None)
etapes = [
    ("a. règles actuelles sans niche, base RFR, imposition commune", lambda nom, g, parts, k: ir(rfr(nom, g, parts), len(parts) == 2, k, isole=(k > 0 and len(parts) == 1))),
    ("b. base large (revenu après cotisations)", lambda nom, g, parts, k: ir(ZN, len(parts) == 2, k, isole=(k > 0 and len(parts) == 1))),
    ("c. sans quotient familial des enfants", lambda nom, g, parts, k: ir(ZN, len(parts) == 2, k, qf=False)),
    ("d. sans décote", lambda nom, g, parts, k: ir(ZN, len(parts) == 2, k, qf=False, decote=False)),
    ("e. sans quotient conjugal (barème par adulte)", lambda nom, g, parts, k: sum(bar(sh * ZN) for sh in parts)),
]
print("IR des revenus au barème aujourd'hui (IRCOM moins IR imputé au PFU) : 80,2 Md€ (après niches)")
prev = None
for lab, f in etapes:
    t = total(f)
    print(f"{lab:<62} {t:6.1f} Md€" + (f"  ({t-prev:+.1f})" if prev is not None else ""))
    prev = t
