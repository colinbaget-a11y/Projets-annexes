"""Bloc « fiscalité immobilière », version 3 (note8p/CONSIGNES_V3.md : IS maintenu à 25 %, enveloppe à revoir).

Lancer depuis fiscalite/ :
  python3 note8p/calculs/foncier3_calculs.py                  -> sorties/foncier3.json + foncier3_journal.txt
  python3 note8p/calculs/foncier3_calculs.py --E 13.5 --archi B   (scénario libre : table annuelle à l'écran)

Paramétrable : scenario(E, archi, r, kappa, debut, paliers) renvoie taux, effets par logement, capitalisation et table
annuelle (années de caisse, Md€ de 2025, + = recette publique en plus par rapport au droit en vigueur).

Deux architectures [C] :
  A : base unique par bien b = sol + bâti/4 ; taux communal (recette communale inchangée à la bascule) + taux national
      uniforme sur la même base (version précédente, foncier_calculs.py) ;
  B : taxe communale à double taux (sol taxé 4 fois plus que le bâti, même part communale que A) + taxe nationale
      additionnelle sur la seule valeur du sol.
Capitalisation (convention nouvelle, « résiduelle » comme les comptes de patrimoine) : la valeur des biens baisse de la
valeur actuelle de l'impôt en plus, ΔV = −(E − κ·ΔDMTO)/r, et, le bâti restant à son coût de remplacement, toute la
baisse porte sur le sol ; le transfert communal du bâti vers le sol est à somme nulle entre biens. Le taux national est
calé avec κ = 0 (prudent : si la baisse des droits se capitalise, la base est plus grande et la recette aussi).
Réutilise (sans les modifier) foncier/simulation.py et note8p/calculs/foncier_calculs.py (importé : il réécrit
foncier.json à l'identique, ses entrées n'ayant pas changé). Lit note8p/sorties/is.json (lecture seule).
Statuts : [E] empirique publié, [S] simulation, [H] hypothèse, [C] choix de politique.
"""
import argparse
import contextlib
import io
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ICI = Path(__file__).resolve().parent
N8 = ICI.parent
RACINE = N8.parent
OUT = N8 / "sorties"
sys.path[:0] = [str(ICI), str(RACINE / "foncier")]
with contextlib.redirect_stdout(io.StringIO()):
    import foncier_calculs as fc  # noqa: E402  (modèle communal, droits, assiette, cas-types)

L, c, W, NLOG = fc.L, fc.c, fc.W, fc.NLOG
K, T, PART_CHAMP = fc.K, fc.T, fc.PART_CHAMP
DEMI, D_FR, D_LOG_FR = fc.DEMI, fc.D_FR, fc.D_LOG_FR
SOL, SOL_BATI, BATI, PRIV = fc.SOL, fc.SOL_BATI, fc.BATI, fc.PRIV
SOL_TOT, BATI_TOT, NU_TOT = fc.SOL_TOT, fc.BATI_TOT, fc.NU_TOT
TAU0, REC_COMM = fc.TAU0, fc.REC_COMM
B_I, COMM, TC_COM, PO, LOC = fc.B_I, fc.COMM, fc.TC_COM, fc.PO, fc.LOC
PARIS, PARIS_A = fc.PARIS, fc.PARIS_A
HLM_SOL, HLM_BATI = fc.HLM_SOL, fc.HLM_BATI
ANS = list(range(2027, 2041))
ENVS = [9.0, 10.0, 12.0, 15.0, 18.0]
ARCHIS = ["A", "B"]
R = 0.03

# Parts de la recette nationale par catégorie de biens, selon l'architecture (biens privés, Insee fin 2025)
BW = {s: SOL[s] + BATI[s] / K for s in PRIV}
BW_TOT = sum(BW.values())
PARTS = {
    "A": dict(men_log=(SOL_BATI["S14"] + BATI["S14"] / K) / BW_TOT,
              nus=NU_TOT / BW_TOT,
              societes=(BW["S11"] + BW["S12"]) / BW_TOT,
              entr_is=(BW["S11"] + BW["S12"] - (HLM_SOL + HLM_BATI / K)) / BW_TOT,
              bati=(BATI_TOT / K) / BW_TOT),
    "B": dict(men_log=SOL_BATI["S14"] / SOL_TOT,
              nus=NU_TOT / SOL_TOT,
              societes=(SOL["S11"] + SOL["S12"]) / SOL_TOT,
              entr_is=(SOL["S11"] + SOL["S12"] - HLM_SOL) / SOL_TOT,
              bati=0.0),
}
VS_MOD = L.v * L.lam                                    # valeur du sol de chaque logement (modèle)
SB_MOD = float((W * B_I).sum())
SS_MOD = float((W * VS_MOD).sum())
VAL_INSEE_MEN = float(fc.ter.loc["S14", "N2111"] + fc.ter.loc["S14", "N111"])
PART_DMTO_LOG = D_LOG_FR / D_FR

# Hypothèses de trajectoire (reprises de foncier_calculs.py)
PHI, I_REP, H_REP, ELIG, RECOURS = fc.PHI, fc.I_REP, fc.H_REP, fc.ELIG, fc.RECOURS
DED_IS, DED_BAIL = fc.DED_IS, fc.DED_BAIL


def qpond(x, q):
    o = x.sort_values()
    cw = W[o.index].cumsum() / NLOG
    return float(o[cw >= q].iloc[0])


def par_decile(s):
    return ((W * s).groupby(L.dec_prix).sum() / W.groupby(L.dec_prix).sum()).values


def ratio_decile(num, den):
    return ((W * num).groupby(L.dec_prix).sum() / (W * den).groupby(L.dec_prix).sum()).values


def taux(E, archi, r=R, kappa=0.0):
    """Taux national (sol ; bâti) une fois la valeur du sol ajustée ; ΔS = −(E − κ·ΔDMTO)/r."""
    s1 = SOL_TOT - (E - kappa * DEMI) / r
    base = s1 + (BATI_TOT / K if archi == "A" else 0.0)
    tn = E / base
    tc = REC_COMM / (s1 + BATI_TOT / K)                  # taux communal moyen sur le sol (bâti : /4)
    return dict(tn_sol=100 * tn, tn_bati=100 * tn / K if archi == "A" else 0.0, tc_sol=100 * tc,
                tc_bati=100 * tc / K, sol_apres=s1, baisse_sol_pct=100 * (1 - s1 / SOL_TOT), base=base,
                tn_statique=100 * E / (SOL_TOT + (BATI_TOT / K if archi == "A" else 0.0)))


def taxe_logements(E, archi):
    """Taxe de chaque logement du modèle après réforme (part communale + part nationale) et part nationale."""
    paye = E * 1e9 * PARTS[archi]["men_log"] * PART_CHAMP
    nat = paye / SB_MOD * B_I if archi == "A" else paye / SS_MOD * VS_MOD
    return COMM + nat, nat


def logements(E, archi):
    tf1, nat = taxe_logements(E, archi)
    dtf = tf1 - L.tf0
    r_ = dict(paye_logements_fr=E * PARTS[archi]["men_log"],
              moyenne=float((W * dtf).sum() / NLOG), moyenne_pct=float(100 * (W * dtf).sum() / fc.TF0),
              pctl={q: qpond(dtf, q / 100) for q in (10, 25, 50, 75, 90, 95, 99)},
              plus300=100 * float(W[dtf > 300].sum() / NLOG), plus600=100 * float(W[dtf > 600].sum() / NLOG),
              baisse=100 * float(W[dtf < 0].sum() / NLOG), double=100 * float(W[dtf > L.tf0].sum() / NLOG),
              paris_pct=float(100 * (W * dtf)[PARIS].sum() / (W * L.tf0)[PARIS].sum()),
              paris_a=float(dtf[PARIS_A].iloc[0]),
              dtf=[float(u) for u in par_decile(dtf)], dtf_pct=[float(u) for u in 100 * ratio_decile(dtf, L.tf0)],
              tfv=[float(u) for u in 100 * ratio_decile(tf1, L.v)],
              net_parc=[float(u) for u in par_decile(dtf - L.d0 / 2)])
    ty = L.assign(a=W * dtf, w=W).groupby("type").sum(numeric_only=True)
    r_["maisons"], r_["apparts"] = float(ty.a["m"] / ty.w["m"]), float(ty.a["a"] / ty.w["a"])
    r_["hausse_po_fr"] = float((W * dtf.clip(lower=0) * PO).sum() / 1e9 / PART_CHAMP)
    r_["hausse_bailleurs_fr"] = float((W * dtf * LOC).sum() / 1e9 / PART_CHAMP)
    # impôt sur le bâti des logements (champ, Md€) : part communale (bâti/4) + part nationale sur le bâti (A seulement)
    tn_b = (E * 1e9 * PARTS[archi]["men_log"] * PART_CHAMP / SB_MOD) if archi == "A" else 0.0
    r_["impot_bati"] = float((W * (L.codgeo.map(TC_COM) + tn_b) * L.v * (1 - L.lam) / K).sum() / 1e9)
    # rapport effectif taux du sol / taux du bâti, toutes parts confondues, par logement
    tc = L.codgeo.map(TC_COM)
    if archi == "A":
        rap = pd.Series(K, index=L.index)
    else:
        tnb = E * 1e9 * PARTS[archi]["men_log"] * PART_CHAMP / SS_MOD
        rap = K * (1 + tnb / tc)
    r_["rapport_sol_bati"] = dict(p10=qpond(rap, .10), p50=qpond(rap, .50), p90=qpond(rap, .90),
                                  paris=float(rap[PARIS_A].iloc[0]),
                                  moyenne=float((W * rap).sum() / NLOG))
    r_["perte_valeur_pct"] = dict(p5=100 * qpond(-dtf / R / L.v, 0.05),
                                  plus5=100 * float(W[(-dtf / R / L.v) < -0.05].sum() / NLOG),
                                  par_decile=[float(u) for u in 100 * ratio_decile(-dtf / R, L.v)])
    return r_, dtf


def capitalisation(E, archi):
    """Ordres de grandeur : baisse de valeur des biens (= du sol, le bâti restant à son coût), r × κ."""
    out = {}
    pm = PARTS[archi]["men_log"]
    for r in (0.03, 0.04):
        for kap in (0.0, 0.5, 1.0):
            tot = (E - kap * DEMI) / r
            men = (E * pm - kap * DEMI * PART_DMTO_LOG) / r
            out[f"r{int(100*r)}_k{int(100*kap)}"] = dict(
                tous=tot, pct_sol_prive=100 * tot / SOL_TOT, pct_immobilier_prive=100 * tot / (SOL_TOT + BATI_TOT),
                menages_logements=men, pct_logements_menages=100 * men / VAL_INSEE_MEN)
    return out


def trajectoire(E, archi, lg, debut=2029, n=3):
    """Table annuelle (caisse). Taxe émise et recouvrée à l'automne de l'année ; droits à la vente ; déductibilité N+1."""
    pas = {a: min(max(a - debut + 1, 0), n) / n for a in ANS}
    tx = {a: T * (1 - 0.5 * pas[a]) for a in ANS}
    tx[ANS[0] - 1] = T
    out, ind, stock = {}, {}, 0.0
    for a in ANS:
        f = pas[a]
        tf = E * f
        dm = -DEMI * f
        d_suiv = 100 * (tx[a] - tx[a + 1]) if a + 1 in tx else 0.0
        d_pts = 100 * (tx[a - 1] - tx[a])
        cal = -PHI * d_suiv * D_FR * tx[a] / T + PHI * d_pts * D_FR * tx[a] / T
        nouveau = ELIG * RECOURS * lg["hausse_po_fr"] * f
        remb = H_REP * stock * (1 + I_REP)
        stock = stock * (1 + I_REP) + nouveau - remb
        rep = -(nouveau - remb)
        fp = pas.get(a - 1, 0.0)
        ded = -fp * (DED_IS * E * PARTS[archi]["entr_is"] + DED_BAIL * max(lg["hausse_bailleurs_fr"], 0))
        net = tf + dm + cal + rep + ded
        out[a] = dict(taxe_fonciere_nouvelle=round(tf, 3), dmto=round(dm, 3), calendrier_ventes=round(cal, 3),
                      report_paiement=round(rep, 3), deductibilite_is_ir=round(ded, 3), net=round(net, 3))
        ind[a] = dict(stock_report=round(stock, 3), taux_dmto_pct=round(100 * tx[a], 2), part_taxe=round(f, 3))
    return out, ind


def scenario(E, archi, debut=2029, n=3):
    lg, dtf = logements(E, archi)
    tr, ind = trajectoire(E, archi, lg, debut, n)
    return dict(E=E, archi=archi, taux=taux(E, archi), taux_r4=taux(E, archi, r=0.04),
                taux_k100=taux(E, archi, kappa=1.0), logements=lg, capitalisation=capitalisation(E, archi),
                annuel=tr, indicateurs=ind), dtf


# ---------------------------------------------------------------------------------------------------- appel libre
if __name__ == "__main__" and len(sys.argv) > 1:
    ap = argparse.ArgumentParser()
    ap.add_argument("--E", type=float, default=12.0)
    ap.add_argument("--archi", default="B", choices=ARCHIS)
    ap.add_argument("--debut", type=int, default=2029)
    ap.add_argument("--paliers", type=int, default=3)
    a = ap.parse_args()
    s, _ = scenario(a.E, a.archi, a.debut, a.paliers)
    print(f"E = {a.E} Md€, architecture {a.archi} : taux national {s['taux']['tn_sol']:.3f} % du sol ;"
          f" hausse moyenne {s['logements']['moyenne']:+.0f} €/logement ; > 300 € : {s['logements']['plus300']:.0f} %")
    for an, v in s["annuel"].items():
        print(an, " ".join(f"{k} {x:+.2f}" for k, x in v.items()))
    sys.exit(0)

# ---------------------------------------------------------------------------------------------------- calcul complet
lignes = []


def p(s=""):
    print(s, flush=True)
    lignes.append(s)


J = {"conventions": "Md€ de 2025, assiettes 2025 non indexées ; années de caisse (taxe foncière recouvrée l'année de"
                    " l'avis, droits à la vente, déductibilité l'année suivante) ; + = recette publique en plus par"
                    " rapport au droit en vigueur (droits au taux permanent) ; − = coût",
     "architectures": {"A": "base unique sol + bâti/4 pour la part communale et la part nationale",
                       "B": "part communale à double taux (sol = 4 × bâti) + taxe nationale sur le seul sol"},
     "parts_recette_nationale": PARTS, "dmto_demi": DEMI, "dmto_total": D_FR,
     "assiette": dict(sol=SOL_TOT, nus=NU_TOT, bati=BATI_TOT, base_A=BW_TOT)}
p(f"[DMTO] division par deux : {DEMI:.2f} Md€ (France entière, taux permanent, ventes 2025) ; logements"
  f" {D_LOG_FR/2:.2f}")
for a in ARCHIS:
    pa = PARTS[a]
    p(f"[PARTS {a}] recette nationale payée par : logements des ménages {100*pa['men_log']:.1f} % ; terrains nus"
      f" {100*pa['nus']:.1f} % ; sociétés {100*pa['societes']:.1f} % (soumises à l'IS hors HLM {100*pa['entr_is']:.1f} %) ;"
      f" part qui porte sur le bâti {100*pa['bati']:.1f} %")

SC, DTF = {}, {}
for a in ARCHIS:
    for E in ENVS + [round(DEMI, 2)]:
        nom = f"{a}_E{E:g}" if E in ENVS else f"{a}_substitution"
        SC[nom], DTF[nom] = scenario(E, a)
        s, lg, tx = SC[nom], SC[nom]["logements"], SC[nom]["taux"]
        tr = s["annuel"]
        p(f"[{nom}] taux national {tx['tn_sol']:.3f} % du sol, {tx['tn_bati']:.3f} % du bâti (statique"
          f" {tx['tn_statique']:.3f} ; r = 4 % {s['taux_r4']['tn_sol']:.3f} ; si droits capitalisés"
          f" {s['taux_k100']['tn_sol']:.3f}) ; communal moyen {tx['tc_sol']:.2f} % sol / {tx['tc_bati']:.2f} % bâti")
        p(f"   logements : moyenne {lg['moyenne']:+.0f} € ({lg['moyenne_pct']:+.0f} %), médiane {lg['pctl'][50]:+.0f},"
          f" P90 {lg['pctl'][90]:+.0f}, P99 {lg['pctl'][99]:+.0f} ; > 300 € {lg['plus300']:.0f} %, > 600 €"
          f" {lg['plus600']:.0f} %, baisse {lg['baisse']:.0f} % ; Paris {lg['paris_pct']:+.0f} % (appartement médian"
          f" {lg['paris_a']:+.0f} €) ; maisons {lg['maisons']:+.0f}, appartements {lg['apparts']:+.0f} ; impôt sur le bâti"
          f" {lg['impot_bati']:.1f} Md€ ; rapport sol/bâti P10 {lg['rapport_sol_bati']['p10']:.1f} médiane"
          f" {lg['rapport_sol_bati']['p50']:.1f} P90 {lg['rapport_sol_bati']['p90']:.1f} Paris"
          f" {lg['rapport_sol_bati']['paris']:.1f}")
        cp = s["capitalisation"]
        p(f"   valeur : −{cp['r3_k0']['tous']:.0f} Md€ (r 3 %, κ 0) ; −{cp['r4_k0']['tous']:.0f} (r 4 %) ; κ 50 %"
          f" −{cp['r3_k50']['tous']:.0f} ; κ 100 % −{cp['r3_k100']['tous']:.0f} ; logements des ménages"
          f" −{cp['r3_k0']['pct_logements_menages']:.1f} % ; P5 {lg['perte_valeur_pct']['p5']:.1f} % ; > 5 %"
          f" {lg['perte_valeur_pct']['plus5']:.0f} %")
        p("   net : " + " ; ".join(f"{an} {tr[an]['net']:+.2f}" for an in (2028, 2029, 2030, 2031, 2032, 2035, 2040))
          + f" ; cumul {sum(v['net'] for v in tr.values()):+.1f}")

# Table demandée : annuel_par_scenario (architecture × enveloppe)
J["annuel_par_scenario"] = {k: v["annuel"] for k, v in SC.items()}
J["indicateurs_annuels"] = {k: v["indicateurs"] for k, v in SC.items()}
J["scenarios"] = {k: {kk: vv for kk, vv in v.items() if kk not in ("annuel", "indicateurs")} for k, v in SC.items()}
J["hypotheses_trajectoire"] = dict(phi=PHI, interet_report=I_REP, remboursement=H_REP, eligibles=ELIG,
                                   recours=RECOURS, deduction_is=DED_IS, deduction_bailleurs=DED_BAIL,
                                   premier_avis=2029, paliers=3, r=R,
                                   clause="chaque palier de baisse des droits (1/1/2029, 2030, 2031) ne s'applique que si"
                                          " le palier de taxe correspondant est mis en recouvrement la même année")
J["par_point"] = dict(md_par_point_dmto=D_FR / (100 * T),
                      net_permanent_par_md_enveloppe={a: (SC[f"{a}_E18"]["annuel"][2040]["net"]
                                                          - SC[f"{a}_E9"]["annuel"][2040]["net"]) / 9 for a in ARCHIS})

# Interaction avec la transition de l'IS (lecture seule de is.json, années de caisse)
IS = json.loads((OUT / "is.json").read_text(encoding="utf-8"))["annuel_caisse"]
is_net = {int(a): v["is_fin_taux_reduit"] + v["is_deduction_50"] for a, v in IS.items()}
J["is_transition_caisse"] = is_net
cov = {}
for k, s in SC.items():
    cov[k] = {a: round(s["annuel"][a]["net"] + is_net.get(a, 0.0), 3) for a in ANS}
J["foncier_plus_is_caisse"] = cov
p("[IS] fin du taux réduit + déduction de 50 % (caisse, is.json) : "
  + " ; ".join(f"{a} {is_net[a]:+.2f}" for a in ANS if a <= 2036))
for k in ["B_E9", "B_E10", "B_E12", "B_E15", "B_E18", "A_E12"]:
    p(f"[FONCIER + IS {k}] " + " ; ".join(f"{a} {cov[k][a]:+.2f}" for a in ANS if a <= 2035)
      + f" ; 2040 {cov[k][2040]:+.2f} ; minimum 2029-2040 {min(cov[k][a] for a in ANS if a >= 2029):+.2f}")

# ---------------------------------------------------------------------------------------------------- cas-types
p()
EREC, AREC = 12.0, "B"
CAS = {}
PROJ = {r["cle"]: r for r in fc.CAS}
for a in ARCHIS:
    for E in ENVS:
        tf1, nat = taxe_logements(E, a)
        lst = []
        for r in fc.CAS:
            i = fc.idx(r["commune"], "a" if r["cle"] != "sgdb" else "m")
            k_ = r["prix"] / L.v[i]
            d = float((tf1[i] - L.tf0[i]) * k_)
            lst.append(dict(cle=r["cle"], prix=r["prix"], dmto_permanent=r["dmto_permanent"], dmto_2026=r["dmto_2026"],
                            dmto_apres=r["dmto_apres"], economie=r["economie"], tf_actuelle=r["tf_actuelle"],
                            dtf=d, dtf_nat=float(nat[i] * k_), annees_equivalentes=r["economie"] / d if d > 0 else None,
                            net_7ans=r["economie"] - d * (1 - (1 + R) ** -7) / R, perte_valeur=-d / R))
        i_o = fc.idx("45234", "m")
        k_o = fc.mob["vend"] / L.v[i_o]
        mob = dict(fc.mob, dtf_orleans_quittee=float((tf1[i_o] - L.tf0[i_o]) * k_o),
                   dtf_sgdb=lst[3]["dtf"])
        CAS[f"{a}_E{E:g}"] = dict(projets=lst, mobilite=mob)
for k in (f"{AREC}_E{EREC:g}", "A_E12", "B_E15", "A_E15", "B_E10"):
    p(f"[CAS {k}] " + " ; ".join(f"{x['cle']} {x['prix']:.0f} € : droits −{x['economie']:.0f}, taxe {x['dtf']:+.0f}"
                                 f"/an ({x['annees_equivalentes'] or 0:.0f} ans)" for x in CAS[k]["projets"]))
J["cas"] = CAS
J["mobilite_base"] = fc.mob

# ---------------------------------------------------------------------------------------------------- g6 : construire
g6 = {"sol": 200_000, "bati": 600_000, "aujourdhui": dict(t_sol=100 * TAU0, t_bati=100 * TAU0)}
for a in ARCHIS:
    for E in ENVS:
        tx = SC[f"{a}_E{E:g}"]["taux"]
        g6[f"{a}_E{E:g}"] = dict(t_sol=tx["tc_sol"] + tx["tn_sol"], t_bati=tx["tc_bati"] + tx["tn_bati"])
for k, v in g6.items():
    if isinstance(v, dict):
        v["nu"] = v["t_sol"] / 100 * g6["sol"]
        v["construire"] = v["t_bati"] / 100 * g6["bati"]
        v["bati"] = v["nu"] + v["construire"]
p("[G6] terrain 200 000 €, immeuble 600 000 € : " + " ; ".join(
    f"{k} nu {v['nu']:.0f} €, construire +{v['construire']:.0f} €" for k, v in g6.items()
    if isinstance(v, dict) and k in ("aujourdhui", "A_E12", "B_E12", "A_E15", "B_E15")))
J["g6"] = g6

# ---------------------------------------------------------------------------------------------------- g10 : sol / PIB
pt = pd.read_csv(RACINE / "foncier/donnees/patrimoine_2025.csv", comment="#", index_col=0)
J["g10"] = dict(annees=[int(a) for a in pt.index], ensemble=[float(u) for u in 100 * pt.terrains_batis / pt.pib],
                menages=[float(u) for u in 100 * pt.terrains_batis_men / pt.pib],
                sol_2022=float(pt.terrains_batis[2022]), sol_2025=float(pt.terrains_batis[2025]))
s = 100 * pt.terrains_batis / pt.pib
p(f"[G10] sol sous les bâtiments / PIB : 1998 {s[1998]:.0f} % ; 2007 {s[2007]:.0f} % ; 2022 {s[2022]:.0f} % ; 2025"
  f" {s[2025]:.0f} % ; baisse 2022-2025 {pt.terrains_batis[2025]-pt.terrains_batis[2022]:.0f} Md€")

# ---------------------------------------------------------------------------------------------------- consommation
# [E] PMC du patrimoine immobilier : 0,7 centime par euro (Arrondel, Lamarche et Savignac, 2015, coupe 2010 ; 1,4 bas
# du patrimoine à 0,8 haut) ; 5 à 7 centimes aux États-Unis (Mian, Rao et Sufi, 2013). Produit = ordre de grandeur.
CONSO = {}
for k in (f"{AREC}_E{EREC:g}", "B_E15", "B_E18", "B_E9", "A_E12"):
    cp = SC[k]["capitalisation"]
    CONSO[k] = {kap: dict(perte_menages=cp[f"r3_k{kap}"]["menages_logements"],
                          conso_07=0.007 * cp[f"r3_k{kap}"]["menages_logements"],
                          conso_14=0.014 * cp[f"r3_k{kap}"]["menages_logements"],
                          conso_us_6=0.06 * cp[f"r3_k{kap}"]["menages_logements"]) for kap in (0, 50, 100)}
    p(f"[CONSO {k}] perte des ménages (r 3 %) κ 0/50/100 : " + " / ".join(
        f"{v['perte_menages']:.0f} Md€ → {v['conso_07']:.1f} à {v['conso_14']:.1f} Md€/an" for v in CONSO[k].values()))
J["consommation"] = CONSO

(OUT / "foncier3_journal.txt").write_text("\n".join(lignes) + "\n", encoding="utf-8")


def _js(o):
    if isinstance(o, dict):
        return {str(k): _js(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [_js(v) for v in o]
    if isinstance(o, (np.floating, np.integer)):
        return float(o)
    if isinstance(o, np.bool_):
        return bool(o)
    return o


(OUT / "foncier3.json").write_text(json.dumps(_js(J), ensure_ascii=False, indent=1), encoding="utf-8")
