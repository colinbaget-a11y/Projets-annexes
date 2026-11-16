"""Bouclage budgétaire de la note de 8 pages : neutralité approximative chaque année, sans dette de transition.

Entrées : sorties/{ircsg,foncier,is,pfu}.json (tables « annuel »). Unités : Md€ constants (niveau des prix et de
l'activité de 2027 ≈ 2025 + 2 ans) ; les séries IS, nominales (+3 %/an), sont déflatées par leur propre croissance.
Convention de caisse : l'IS d'un exercice est encaissé l'année suivante (is.json, annuel_caisse) ; la taxe foncière,
les droits et l'impôt sur les plus-values sont comptés l'année d'encaissement.

Règles (CADRE.md) : pas de déficit organisé ; les recettes de la fin de l'effacement des plus-values ne financent rien
tant qu'elles ne sont pas constatées (elles forment une réserve, affectée ensuite à une baisse supplémentaire du taux
d'IS) ; la fin de la contribution exceptionnelle sur l'IS et l'extinction de la CRDS (droit en vigueur) sont affichées
à part, non comptées.

Choix de calendrier [C] :
- taux réduit d'IS : 20 % pour l'exercice 2027, aligné sur le taux normal dès l'exercice 2028 ;
- déduction immédiate : 25 % pour l'exercice 2029, 50 % dès l'exercice 2030 (elle attend la taxe foncière, en
  recouvrement par tiers en 2029-2031, et les droits baissent au même rythme : foncier.json) ;
- taux normal : baisse par demi-points, la plus forte possible chaque année sans solde négatif au-delà de −0,3 Md€.
Sortie : sorties/bouclage.json, sorties/bouclage.txt.
"""
import json
from pathlib import Path

S = Path(__file__).resolve().parent.parent / "sorties"
ANS = list(range(2027, 2041))
G = 1.03                                     # croissance nominale des séries IS (is.json : point de taux 2,99 → 4,39)


def charge(nom):
    p = S / f"{nom}.json"
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else {}


IS, FON, PFU, IRC = charge("is"), charge("foncier"), charge("pfu"), charge("ircsg")
defl = {a: G ** (a - 2027) for a in ANS}


def is_exercice(cle, a):
    v = IS["annuel"].get(str(a), {}).get(cle, 0.0)
    return v / defl[a]


# Déduction : profil du calendrier B (25 % puis 50 %) décalé de deux exercices (début en 2029), en euros constants.
B = IS["deduction"]["calendriers"]["B"]["mix"]
B_const = {int(a): v / defl[int(a)] for a, v in B.items()}
DEC = 2


def deduction_exercice(a):
    b = a - DEC
    if b < 2027:
        return 0.0
    if b in B_const:
        return -B_const[b]
    return -B_const[max(B_const)]            # régime permanent (constant en euros constants)


def taux_reduit_exercice(a):
    return is_exercice("is_fin_taux_reduit", a)


def point_exercice(a):
    """Coût net d'un point de baisse du taux normal (base totale, taux réduit aligné), interaction avec la déduction."""
    base = is_exercice("is_point_taux_normal_base_totale", a)
    inter = IS["annuel"].get(str(a), {}).get("is_point_interaction_deduction", 0.0) / defl[a]
    # l'interaction est calculée pour le calendrier B non décalé : on la rapporte au coût de la déduction décalée
    ded_b = IS["annuel"].get(str(a), {}).get("is_deduction_50", 0.0) / defl[a]
    ratio = (deduction_exercice(a) / ded_b) if ded_b else 0.0
    return base + inter * ratio


def foncier(a):
    return FON["annuel"][str(a)]["net"]


def ircsg(a):
    an = IRC.get("annuel", {}).get(str(a), {})
    return an.get("net", 0.0) if an else 0.0


def pfu(a):
    return PFU["annuel"][str(a)]["fin_effacement_central"]


# Baisse du taux : par demi-points, jamais de retour en arrière ; un demi-point de plus n'est accordé à l'exercice a
# que si le solde de caisse reste ≥ −0,3 Md€ cette année-là ET toutes les années suivantes (à points constants).
def solde_ex(a, kk):
    caisse = min(a + 1, 2040)
    return (taux_reduit_exercice(a) + deduction_exercice(a) + kk * point_exercice(a)
            + foncier(caisse) + ircsg(caisse))


points = {}
k = 0.0
for a in ANS:
    while all(solde_ex(b, k + 0.5) >= -0.3 for b in ANS if b >= a):
        k += 0.5
    points[a] = k

lignes, res = [], {}
for c in ANS:                                 # c = année de caisse
    e = c - 1
    tr = taux_reduit_exercice(e) if e >= 2027 else 0.0
    dd = deduction_exercice(e) if e >= 2027 else 0.0
    pt = points.get(e, 0.0) * point_exercice(e) if e >= 2027 else 0.0
    fo, ir, pf = foncier(c), ircsg(c), pfu(c)
    tot = tr + dd + pt + fo + ir
    res[c] = {"ircsg": ir, "foncier_net": fo, "taux_reduit": tr, "deduction_50": dd, "baisse_taux": pt,
              "taux_normal": 25 - points.get(e, 0.0) if e >= 2027 else 25.0, "solde_sans_pfu": tot,
              "pfu_reserve": pf, "solde_avec_pfu": tot + pf,
              "foncier_detail": FON["annuel"][str(c)]}
    lignes.append(f"{c} | IR-CSG {ir:+.2f} | foncier {fo:+.2f} | taux réduit {tr:+.2f} | déduction {dd:+.2f} | "
                  f"taux {res[c]['taux_normal']:.1f} % ({pt:+.2f}) | solde {tot:+.2f} | réserve PV {pf:+.2f}")

dette = 0.0
for c in ANS:
    dette = dette * 1.0325 - res[c]["solde_sans_pfu"]
res_tot = {"annuel": res, "points_par_exercice": points, "dette_cumulee_2040_sans_pfu": dette,
           "notes": __doc__}
(S / "bouclage.json").write_text(json.dumps(res_tot, ensure_ascii=False, indent=1), encoding="utf-8")
(S / "bouclage.txt").write_text("\n".join(lignes) + f"\nDette cumulée 2040 (sans réserve PV) : {dette:.2f}\n",
                                encoding="utf-8")
print("\n".join(lignes))
print(f"dette cumulée 2040 sans la réserve des plus-values : {dette:.2f} Md€")
