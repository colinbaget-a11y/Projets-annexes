"""Fusion IR-CSG-CRDS, foyers purs : référence et arbitrages, perte sèche généralisée (revue/methode_perte_seche.md).

Version corrigée de perte_seche_ircsg.py : les foyers représentatifs sont séparés en foyers d'actifs et foyers de
retraités (modele_purs.py), ce qui corrige les défauts établis par revue/verif_ir_csg.md (franchise d'activité
accordée aux retraités, « qui paie » au prorata, recette non tenue, marge extensive des personnes seules, parents
isolés deux fois trop nombreux, quotient familial surévalué).

Référence (consigne de l'auteur) : assiette large, impôt individuel, même barème pour tous, ni franchise ni aide
familiale dans l'impôt. Barème à taux marginal en ligne droite (0, 20 000 €, z1, z2 ; 50 % au-delà de z2), choisi
dans la même grille que perte_seche_ircsg.py pour minimiser la perte sèche généralisée centrale (coin non
contributif, déplacement s = 0,5 vers 48,6 % pour le dixième le plus aisé, marge extensive η = 0,25), à recette
égale (220 Md€).

Chaque arbitrage modifie un seul paramètre ; la recette est rétablie par un même nombre de points ajouté à tous les
taux sous le taux supérieur (« points de taux pour tous »).

Lancer depuis fiscalite/ : python3 synthese/perte_seche_ircsg_purs.py
Sorties : synthese/sorties/perte_seche_ircsg_purs.txt et .json, synthese/sorties/controles_purs.txt
"""
import itertools
import json
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE)]
import modele_purs as M  # noqa: E402

ex, P = M.ex, M.P
OUT = HERE / "sorties"
OUT.mkdir(exist_ok=True)
GRILLE = dict(t0=[0.06, 0.09, 0.12, 0.15, 0.18], tb=[0.12, 0.15, 0.18, 0.21, 0.24],
              z1=[30e3, 45e3, 60e3, 90e3], z2=[250e3, 400e3, 600e3])        # grille de perte_seche_ircsg.py
CAS = (("retraité seul 17 000 €", "retraite_seul", 17e3), ("salarié seul au Smic (21 500 € brut)", "seul", 21.5e3),
       ("couple avec deux enfants 50 000 €", "couple_2enf", 50e3))


def bareme(b, d=0.0, top=0.50):
    t0, tb, z1, t1, z2 = b
    return ex.bareme_lineaire([0, 20e3, z1, z2], [t0 + d, tb + d, t1 + d, top])


def options(**k):
    o = dict(M.OPT0)
    o.update(k)
    return o


def cale_t1(t0, tb, z1, z2, o):
    """Taux en z1 qui donne la recette cible (référence)."""
    lo, hi = 0.0, 0.50
    for _ in range(32):
        t1 = (lo + hi) / 2
        lo, hi = (t1, hi) if M.recette(*bareme((t0, tb, z1, t1, z2)), o) < M.CIBLE else (lo, t1)
    return (lo + hi) / 2


def cale_d(b, o, top=0.50, cible=None):
    """Points de taux pour tous qui rétablissent la recette."""
    cible = M.CIBLE if cible is None else cible
    lo, hi = -0.15, 0.30
    for _ in range(36):
        d = (lo + hi) / 2
        lo, hi = (d, hi) if M.recette(*bareme(b, d, top), o) < cible else (lo, d)
    return (lo + hi) / 2


def reference(o):
    """Barème de la grille qui minimise la perte sèche centrale (nc_s50_486 + ext_nc), à recette égale."""
    rows = []
    for t0, tb, z1, z2 in itertools.product(*GRILLE.values()):
        if tb < t0 or z1 >= z2:
            continue
        t1 = cale_t1(t0, tb, z1, z2, o)
        if not tb <= t1 < 0.50 - 1e-3:
            continue
        b = (t0, tb, z1, t1, z2)
        rows.append((M.evalue("grille", *bareme(b), o, sorties=False)["cen"], b))
    rows.sort(key=lambda r: r[0])
    return rows


def cas_types(b, d, top, o):
    tm, T = bareme(b, d, top)
    return {nom: M.cas_type(tm, T, o, prof, brut) for nom, prof, brut in CAS}


def fmt_groupes(g):
    return (f"actifs {g['actifs']['Md']:+.1f}, retraités {g['retraites']['Md']:+.1f} | personnes seules sans enfant"
            f" {g['seuls']['Md']:+.1f} (dont retraitées {g['seuls_retraites']['Md']:+.1f}), parents isolés"
            f" {g['parents_isoles']['Md']:+.1f}, couples sans enfant {g['couples0']['Md']:+.1f} (dont retraités"
            f" {g['couples0_retraites']['Md']:+.1f}), couples avec deux enfants {g['couples2']['Md']:+.1f}")


def fmt_euros(g):
    return " ; ".join(f"{lib} {g[k]['eur']:+,.0f}" for k, lib in (
        ("seuls_actifs", "seul actif"), ("seuls_retraites", "seul retraité"), ("parents_isoles", "parent isolé"),
        ("couples0_actifs", "couple actif sans enfant"), ("couples0_retraites", "couple retraité"),
        ("couples2", "couple avec deux enfants")))


if __name__ == "__main__":
    L, C = [], []

    def p(s):
        print(s, flush=True)
        L.append(s)

    o_ref = options()
    p("[NB] Md€ et € par an ; perte sèche : variation par rapport à aujourd'hui (négatif = gain d'efficacité) ;"
      " déciles : foyers classés par revenu fiscal du point représentatif, € par foyer ; « Md€ » : variation de la"
      " charge IR + CSG + CRDS de chaque groupe ; cas-types OpenFisca (revenus 2024).")
    p(f"[AUJ] recette à remplacer {M.CIBLE:.1f} Md€ ; perte sèche quadratique d'aujourd'hui (modèle des notes)"
      f" {M.QUAD0:.1f} Md€ ; foyers purs : {M.W_A.sum() / 1e6:.1f} M d'actifs, {M.W_R.sum() / 1e6:.1f} M de retraités,"
      f" {M.CASES_T / 1e6:.2f} M de parents isolés ; chèque {M.CHEQUE:,.0f} € par enfant (quotient familial des enfants"
      f" {M.QF_COUT:.1f} Md€)")
    grille = reference(o_ref)
    b = grille[0][1]
    p(f"[REF] barème de référence : {100*b[0]:.0f} % au premier euro, {100*b[1]:.0f} % à 20 k€, {100*b[3]:.1f} % à "
      f"{b[2]/1e3:.0f} k€, 50 % à {b[4]/1e3:.0f} k€ (perte sèche centrale {grille[0][0]:+.1f} Md€ ; {len(grille)} barèmes"
      f" de la grille tiennent la recette)")
    p("[REF] cinq meilleurs barèmes de la grille (t0, tb, z1, t1, z2 : perte centrale) : " + " | ".join(
        f"{100*u[0]:.0f}/{100*u[1]:.0f}/{u[2]/1e3:.0f}k/{100*u[3]:.1f}/{u[4]/1e3:.0f}k : {c:+.1f}" for c, u in grille[:5]))
    bords = [k for k, i in (("t0", 0), ("tb", 1), ("z1", 2), ("z2", 4)) if b[i] in (min(GRILLE[k]), max(GRILLE[k]))]
    if bords:
        p(f"[REF] attention : le barème retenu est au bord de la grille pour {', '.join(bords)}")
    res = []
    ref = {}

    def run(nom, recale=True, top=0.50, **k):
        o = options(**k)
        d = cale_d(b, o, top) if recale else 0.0
        tm, T = bareme(b, d, top)
        r = M.evalue(nom, tm, T, o)
        lo = M.evalue(nom, tm, T, o, jeu="bas", sorties=False)
        hi = M.evalue(nom, tm, T, o, jeu="haut", sorties=False)
        r.update(d=d, top=top, options=o, lo=lo["cen"], hi=hi["cen"], cas=cas_types(b, d, top, o))
        if not ref:
            ref.update(r)
        p(f"[{nom}] points de taux pour tous {100*d:+.2f} ; recette {r['recette']:.1f} Md€ ; perte sèche, variation"
          f" par rapport à aujourd'hui : centrale {r['cen']:+.1f} Md€ (élasticités basses à hautes {r['lo']:+.1f} à"
          f" {r['hi']:+.1f} ; écart à la référence {r['cen'] - ref['cen']:+.1f}) ; quadratique {r['quad']:+.1f} ; coin"
          f" IR-CSG seul {r['c0']:+.1f} ; coin non contributif {r['nc']:+.1f} ; toutes cotisations {r['tout']:+.1f} ;"
          f" déplacement s=0,5 {r['nc_s50_486'] - r['nc']:+.1f} ; marge extensive {r['ext_nc']:+.1f} (dont personnes"
          f" seules de 0,5 à 2 Smic {r['ext_nc_seuls_05_2']:+.1f}) ; perdants > 500 € {r['perdants500']:.0f} %")
        p("    déciles € " + " ".join(f"{u:+.0f}" for u in r["dec_eur"]) + f" ; 1 % du haut {r['top1_Md']:+.1f} Md€,"
          f" 10 % du haut {r['top10_Md']:+.1f} Md€")
        p("    Md€ : " + fmt_groupes(r["groupes"]))
        p("    € par foyer : " + fmt_euros(r["groupes"]))
        p("    cas-types € par an : " + " ; ".join(f"{n} {u:+,.0f}" for n, u in r["cas"].items()))
        res.append(r)
        return r

    run("Référence : assiette large, même barème pour tous", recale=False)
    run("Franchise d'activité 4 000 €", F=4000.0)
    run("Franchise d'activité 8 000 €", F=8000.0)
    run("Franchise de 8 000 € sur les seuls salaires", F=8000.0, sur="salaires")
    run("Franchise de 8 000 € sur tous les revenus", F=8000.0, sur="tout")
    run("Abattement de 10 % sur les pensions", abat_pens=0.10)
    run("Petites pensions exonérées (totalement jusqu'à 12 500 €, dégressif jusqu'à 25 000 €)", Fp=12500.0,
        Fp_degressif=True)
    run("Famille : franchise de 6 000 € par enfant", fam="franchise")
    run("Famille : chèque par enfant", fam="cheque")
    run("Imposition commune : quotient conjugal et familial", fam="quotient")
    run("Taux supérieur 45 %", top=0.45)
    run("Taux supérieur 55 %", top=0.55)
    run("Ancienne proposition : franchise d'activité 8 000 € + 6 000 € par enfant", F=8000.0, fam="franchise")
    (OUT / "perte_seche_ircsg_purs.txt").write_text("\n".join(L) + "\n", encoding="utf-8")

    # ------------------------------------------------------------------ contrôles d'ordre de grandeur
    def c(s):
        print(s, flush=True)
        C.append(s)

    alertes = []
    c("Contrôles du modèle à foyers purs (synthese/modele_purs.py, perte_seche_ircsg_purs.py)")
    c("")
    c("1. Construction")
    for s in M.controles():
        c(s)
    # quotient familial : sensibilité à la représentation des parents non isolés (comme la vérification)
    W_A, S, RFR_A = M.W_A, M.S, M.RFR_A

    def ir_concubin(r):
        i0 = P._bareme_ir(r)
        i = np.maximum(1.5 * P._bareme_ir(r / 1.5), i0 - P.PLAF)
        return np.clip(i - np.clip(P.DEC_S - P.DEC_T * i, 0, None), 0, None)
    g_conc = P.ir_actuel(RFR_A, False, 0) - ir_concubin(RFR_A)
    n_seul_enf = (P.W * (1 - P.S) * P.NS).sum()                   # 4,0 M dans le modèle d'origine
    ns_b, nc_b, part_t = n_seul_enf / (W_A * (1 - S)).sum(), (M.ENFANTS - n_seul_enf) / (W_A * S).sum(), M.CASES_T / n_seul_enf
    qf_b = ((W_A * (1 - S) * ns_b * (part_t * M.GAIN_S + (1 - part_t) * g_conc)).sum()
            + (W_A * S * nc_b / 2 * M.GAIN_C).sum()) / 1e9
    c(f"   sensibilité : en gardant {n_seul_enf / 1e6:.1f} M de personnes seules avec un enfant, dont 1,97 M avec la"
      f" case T et les autres à 1,5 part (représentation de la vérification), le quotient familial vaut {qf_b:.1f} Md€")
    c("")
    c("2. Recette et répartition")
    o8 = options(F=8000.0, fam="franchise")
    bar_p = json.loads((M.ROOT / "ir_csg/sorties/proposition_baremes.json").read_text())["proposition"]
    bp = (bar_p["t0"], bar_p["tb"], bar_p["z1"], bar_p["t1"], bar_p["z2"])
    rec_p = M.recette(*bareme(bp), o8)
    c(f"Barème de l'ancienne proposition (17 / 22 / 24,2 % à 45 k€ / 50 % à 600 k€, franchise d'activité 8 000 €,"
      f" 6 000 € par enfant) appliqué tel quel aux foyers purs : recette {rec_p:.1f} Md€ au lieu de {M.CIBLE:.1f}"
      f" (vérification, foyers spécialisés : 243,3)")
    tm_p, T_p = bareme(bp)
    rp = M.evalue("ancienne proposition, barème publié", tm_p, T_p, o8, sorties=True)
    c(f"   à ce barème, les retraités paient {rp['groupes']['retraites']['Md']:+.1f} Md€ de plus (vérification : au moins"
      f" +28 contre le prorata du modèle d'origine) et les actifs {rp['groupes']['actifs']['Md']:+.1f}")
    anc = res[-1]
    c(f"   recalé sur la recette ({100*anc['d']:+.2f} point pour tous dans la grille de référence) : retraités"
      f" {anc['groupes']['retraites']['Md']:+.1f} Md€, actifs {anc['groupes']['actifs']['Md']:+.1f} Md€ (sorties"
      f" actuelles : pensions +13,6, chômage +3,0, salaires −13,4, indépendants −3,2)")
    if anc["groupes"]["retraites"]["Md"] < 28:
        alertes.append("hausse des retraités sous la borne de +28 Md€ de la vérification (ancienne proposition)")
    # la franchise d'activité ne touche plus les retraités
    tm0, T0 = bareme(b)
    ecart = 0.0
    for nom, g, _, w, parts, kids in M.TYPES:
        if g == "R":
            i0 = M.impot_adultes(tm0, T0, options(), *M.adultes(g, parts, options()), kids)[0]
            i8 = M.impot_adultes(tm0, T0, options(F=8000.0), *M.adultes(g, parts, options(F=8000.0)), kids)[0]
            ecart += (w * (i0 - i8)).sum() / 1e9
    c(f"À barème inchangé, la franchise d'activité de 8 000 € allège l'impôt des retraités de {ecart:.2f} Md€ (modèle"
      f" d'origine : les retraités en profitaient)")
    # somme des déciles = total
    pire = 0.0
    for r in res:
        tot_dec = sum(e * n for e, n in zip(r["dec_eur"], r["dec_foyers"])) / 1e9
        grp = r["groupes"]
        tot_grp = grp["actifs"]["Md"] + grp["retraites"]["Md"]
        tot_fam = grp["seuls"]["Md"] + grp["parents_isoles"]["Md"] + grp["couples0"]["Md"] + grp["couples2"]["Md"]
        pire = max(pire, abs(tot_dec - r["total_Md"]), abs(tot_grp - r["total_Md"]), abs(tot_fam - r["total_Md"]),
                   abs(r["recette"] - M.CIBLE))
        c(f"   {r['nom']} : recette {r['recette']:.2f} ; somme des déciles {tot_dec:+.3f} Md€, actifs + retraités"
          f" {tot_grp:+.3f}, quatre types de foyers {tot_fam:+.3f}, total {r['total_Md']:+.3f}")
    c(f"Écart le plus grand entre ces sommes, ou entre la recette et la cible : {pire:.3f} Md€")
    if pire > 0.05:
        alertes.append("les sommes par décile ou par groupe ne redonnent pas le total, ou la recette n'est pas tenue")
    c("")
    c("3. Prix d'un milliard (coût marginal des fonds publics) du barème de référence")
    d1 = cale_d(b, o_ref, cible=M.CIBLE + 1.0)
    for jeu in ("bas", "central", "haut"):
        r0 = M.evalue("ref", *bareme(b), o_ref, jeu=jeu, sorties=False)
        r1 = M.evalue("ref + 1 Md€", *bareme(b, d1), o_ref, jeu=jeu, sorties=False)
        parts_ = {"quadratique": r1["modele"] - r0["modele"], "coin IR-CSG seul": r1["c0"] - r0["c0"],
                  "coin non contributif": r1["nc"] - r0["nc"], "toutes cotisations": r1["tout"] - r0["tout"],
                  "central (non contributif, s = 0,5, marge extensive)": r1["cen"] - r0["cen"]}
        c(f"   élasticités {jeu} : +1 Md€ de recette mécanique = {100*d1:+.3f} point pour tous ; perte sèche"
          " supplémentaire, μ = 1 + ΔPS, et coût marginal au sens de Kleven et Kreiner 1/(1 − ΔPS) : " + " ; ".join(
              f"{k} {u:.2f} Md€ (μ {1 + u:.2f} ; {1 / (1 - u):.2f})" for k, u in parts_.items()))
        if jeu == "central":
            mu_c = parts_["central (non contributif, s = 0,5, marge extensive)"]
    # même calcul quand le milliard vient du seul taux en z1 (instrument de revue/methode_perte_seche.md)
    t1a = cale_t1(b[0], b[1], b[2], b[4], o_ref)
    lo_, hi_ = t1a, 0.50
    for _ in range(36):
        t1b = (lo_ + hi_) / 2
        lo_, hi_ = (t1b, hi_) if M.recette(*bareme((b[0], b[1], b[2], t1b, b[4])), o_ref) < M.CIBLE + 1.0 else (lo_, t1b)
    ra = M.evalue("t1", *bareme((b[0], b[1], b[2], t1a, b[4])), o_ref, sorties=False)
    rb = M.evalue("t1 + 1 Md€", *bareme((b[0], b[1], b[2], (lo_ + hi_) / 2, b[4])), o_ref, sorties=False)
    c(f"   élasticités central, milliard levé par le seul taux en z1 ({100 * ((lo_ + hi_) / 2 - t1a):+.2f} point) :"
      f" coin IR-CSG seul {rb['c0'] - ra['c0']:.2f} ; non contributif {rb['nc'] - ra['nc']:.2f} ; toutes cotisations"
      f" {rb['tout'] - ra['tout']:.2f} ; central {rb['cen'] - ra['cen']:.2f} Md€ (note de méthode, ancienne proposition,"
      " foyers mélangés : 0,16 / 0,38 / 0,60)")
    c("   Repère : Kleven et Kreiner (2006, JPubE 90, tableau 3), France : 1,21 (heures seules) à 1,72 (avec la"
      " participation), coin fiscal complet. Le modèle ne contient que les cotisations non contributives et la prime"
      " d'activité dans le coin, pas la TVA ni les autres prestations, et le barème de référence a des taux marginaux"
      " bas (12 à 15 % jusqu'à 20 000 €) : un coût marginal plus faible est attendu.")
    if 1 / (1 - mu_c) < 1.21:
        alertes.append(f"à signaler, non absurde : coût marginal central {1 / (1 - mu_c):.2f}, sous la fourchette de"
                       " Kleven et Kreiner (1,21 à 1,72) ; voir le § 3")
    if 1 / (1 - mu_c) < 1.0 or 1 / (1 - mu_c) > 2.5:
        alertes.append(f"ABSURDE : coût marginal central {1 / (1 - mu_c):.2f}")
    c("")
    c("4. Marge extensive des personnes seules de 0,5 à 2 Smic (exclue du modèle d'origine comme artefact)")
    for r in res:
        c(f"   {r['nom']} : {r['ext_nc_seuls_05_2']:+.2f} Md€ ; salarié seul au Smic"
          f" {r['cas']['salarié seul au Smic (21 500 € brut)']:+,.0f} € par an")
    c("")
    c("5. Signes et ordres de grandeur")
    for r in res:
        cas = r["cas"]
        g = r["groupes"]
        if r["options"]["F"] == 0 and r["options"]["Fp"] == 0 and r["options"]["abat_pens"] == 0 and g["retraites"]["Md"] < 0:
            alertes.append(f"{r['nom']} : les retraités gagnent sans dispositif pour eux")
        if cas["retraité seul 17 000 €"] < -1:
            alertes.append(f"{r['nom']} : le retraité seul à 17 000 € gagne")
    cur_r = sum((w * M.CURT[nom]).sum() for nom, g, _, w, _, _ in M.TYPES if g == "R") / 1e9
    if abs(cur_r - 41.1) > 2:
        alertes.append(f"à signaler : charge actuelle des retraités {cur_r:.1f} Md€ contre 41,1 au prorata (§ 1 : à revenu"
                       " net égal, un retraité sans enfant paie presque autant qu'un actif sans enfant au-delà de 40 000 €,"
                       " et les enfants sont tous chez les actifs)")
    if abs(M.QF_COUT - 12.9) > 0.3:
        alertes.append(f"à signaler : quotient familial des enfants {M.QF_COUT:.1f} Md€ contre 12,9 dans la vérification"
                       " (§ 1 : les enfants ne sont plus que chez les actifs, donc moins dans les tranches basses où les"
                       " retraités sont nombreux ; 14,3 avec le RFR du foyer représentatif, 13,4 avec un RFR sans le"
                       " capital au PFU ; 13,2 avec la représentation des parents de la vérification)")
    x0 = M.x.iloc[0]                                             # tranche du bas (0 à 10 000 €)
    n_r_bas = x0.foyers * float(M.PEN_N.iloc[0] / x0.assiette3)
    if n_r_bas > 1.5 * x0.foyers_pensions:
        alertes.append(f"à signaler : tranche {x0.tranche} : {n_r_bas / 1e6:.1f} M de foyers de retraités dans le modèle"
                       f" (masse des pensions) contre {x0.foyers_pensions / 1e6:.1f} M de foyers déclarant des pensions"
                       f" dans l'IRCOM ; {(x0.foyers - x0.foyers_pensions - x0.foyers_salaires) / 1e6:.1f} M de foyers"
                       " n'y déclarent ni salaire ni pension. Effet faible sur les montants (revenus très bas)")
    if bords:
        alertes.append(f"à signaler : barème de référence au bord de la grille ({', '.join(bords)})")
    c("Points à signaler (contrôles automatiques) :" + (" aucun" if not alertes else "\n   - " + "\n   - ".join(alertes)))
    (OUT / "controles_purs.txt").write_text("\n".join(C) + "\n", encoding="utf-8")

    def propre(u):
        if isinstance(u, dict):
            return {k: propre(w) for k, w in u.items()}
        if isinstance(u, (list, tuple)):
            return [propre(w) for w in u]
        if isinstance(u, (np.floating, np.integer)):
            return float(u)
        return u
    (OUT / "perte_seche_ircsg_purs.json").write_text(json.dumps(propre(dict(
        ref=list(b), quad0=M.QUAD0, cible=M.CIBLE, qf_cout=M.QF_COUT, cheque=M.CHEQUE, res=res)), indent=1,
        ensure_ascii=False), encoding="utf-8")
