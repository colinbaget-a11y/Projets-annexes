"""Bloc IR-CSG v3, version finale « C2 financé 5,5 » (décision de l'assembleur, 18/11/2026).

Financement externe de 5,5 Md€ par an en régime de croisière (foncier, niches de l'IS), en caisse par paliers :
0 jusqu'en 2031, 1,0 (2032), 2,0 (2033), 3,0 (2034), 4,0 (2035), 5,0 (2036), 5,5 dès 2037. La fusion garde sa montée
en charge 2027-2030 à recette constante (barème C2 à recette constante pendant ces années) ; chaque palier de
financement abaisse le barème vers sa version finale.

Ciblage : baisse des taux aux points 0, 1, 1,5 et 2 Smic (poids 1 / 1 / 1 / 0,5), donc aucun taux marginal relevé entre
0,7 et 1,1 Smic ; plafond de 48 % et point haut (163 400 €) inchangés. Pour que le haut ne reçoive rien de ce
financement, le taux au point 3,5 Smic est relevé de δ tel que l'impôt au point haut (et au-delà) soit inchangé :
l'aire retirée sous la courbe des taux marginaux en bas est rendue entre 2 Smic et le point haut. Lancer après
ircsg3_proposition.py : python3 note8p/calculs/ircsg3_final.py
"""
import json

import numpy as np

import ircsg3_proposition as PR

N, R, B, C, M = PR.N, PR.R, PR.B, PR.C, PR.M
O, OUT, D = PR.O, PR.OUT, PR.D
FIN = 5.5
PALIERS = {2032: 1.0, 2033: 2.0, 2034: 3.0, 2035: 4.0, 2036: 5.0}
W_BAS = np.array([1.0, 1.0, 1.0, 0.5, 0.0, 0.0])
P0, T0 = PR.REC["points"], np.array(PR.REC["taux"])


def bareme_fin(e):
    tt = T0 - e * W_BAS
    s0 = N.continu(P0, T0)
    zp = P0[-1]
    # δ au point 3,5 Smic : impôt au point haut inchangé
    lost = s0[1](zp) - N.continu(P0, tt)[1](zp)
    gain_par_point = (P0[4] - P0[3]) / 2 + (P0[5] - P0[4]) / 2
    tt[4] += lost / gain_par_point
    return N.continu(P0, list(tt)), list(tt)


def cale(F):
    lo, hi = 0.0, 0.1
    for _ in range(45):
        m = (lo + hi) / 2
        lo, hi = (m, hi) if N.recette(bareme_fin(m)[0], O) > N.CIBLE - F else (lo, m)
    return (lo + hi) / 2


E = cale(FIN)
S, TT = bareme_fin(E)
L = []


def p(s):
    print(s, flush=True)
    L.append(s)


ind = B.indicateurs(S, O)
ind["efficacite"] = PR.efficacite(S)
ind["part_gains"] = PR.part_gains(S)
ev = N.evalue(S, O, repart=True)
ev0 = N.evalue(N.continu(P0, list(T0)), O, repart=True)
cas = {k: R.cas_type(S, O, k) for k in R.CAS.cle}
for v in cas.values():
    v["delta_mois"] = v["delta"] / 12
# retraités et familles
ret = {f"{int(q / 1e3)}k": float(N.impot_z(S, O, [q])[0]) - B.auj("retraite_seul", q)
       for q in (10e3, 12e3, 14e3, 16e3, 18e3, 20e3, 25e3, 30e3, 40e3, 60e3, 80e3, 100e3)}
fam = {}
for prof, kids in (("couple_2enf", 2), ("couple_2enf_mono", 2), ("couple_3enf", 3), ("couple_3enf_mono", 3),
                   ("parent_isole_2enf", 2), ("couple_0enf_mono", 0)):
    gg = PR.U.CTN[PR.U.CTN.profil == prof]
    rows = {}
    for bb in (20e3, 30e3, 40e3, 60e3, 80e3, 100e3, 150e3):
        r = gg.iloc[np.argmin(np.abs(gg.brut.values - bb))]
        zs = [r.base_a] + ([r.base_b] if prof.startswith("couple") else [])
        rows[f"{int(bb / 1e3)}k"] = (float(N.impot_z(S, O, zs, kids)[0]) - (r.ir + r.csg + r.crds)) / 12
    fam[prof] = rows
PR.S0 = S                                   # decompose() utilise le barème S0
niches = [PR.decompose(*a) for a in PR.NICH]
sc = {}
for cle0, cle1 in (("conj_0", "conj_mi"), ("conj2_0", "conj2_mi"), ("conj_0", "conj_1k")):
    c1 = R.CAS[R.CAS.cle == cle1].iloc[0]
    sal2 = float(str(c1.bruts).split(";")[1])
    sc[cle1] = dict(auj=PR.SC[cle1]["auj"], final=100 * (R.impot_cas(S, O, cle1) - R.impot_cas(S, O, cle0)) / sal2)
# qui reçoit les 5,5 Md€ (différence avec C2 à recette constante)
dec_f = [a - b for a, b in zip(ev["dec_eur"], ev0["dec_eur"])]
recu = dict(top10_Md=ev["top10_Md"] - ev0["top10_Md"], top1_Md=ev["top1_Md"] - ev0["top1_Md"],
            actifs_Md=ev["groupes"]["actifs"]["Md"] - ev0["groupes"]["actifs"]["Md"],
            retraites_Md=ev["groupes"]["retraites"]["Md"] - ev0["groupes"]["retraites"]["Md"], deciles_eur=dec_f)
# cascade (figure F)
res, _ = C.cascade(S, O)
D["cascade_final"] = [dict(etape=a, libelle=b, **c) for a, b, c in res]
# trajectoire : fusion 2027-2030 à recette constante (λ), puis paliers de financement
a0 = PR.VERS["F0"]["ind"]["agregats"]
ann = {}
for an in range(2027, 2041):
    lam = PR.MONTEE.get(an, 1.0)
    f = 0.0 if an < 2032 else PALIERS.get(an, FIN)
    k = f / FIN
    act = lam * ((1 - k) * a0["actifs"] + k * ind["agregats"]["actifs"])
    rt = lam * ((1 - k) * a0["retraites"] + k * ind["agregats"]["retraites"])
    row = dict(ircsg_retraites=rt, ircsg_actifs=act, ircsg_cehr_bareme_absorbee=-lam * R.CEHR_BAR,
               ircsg_invalidite_dependance_maintenus=-lam * sum(R.GARDES.values()), financement_externe_recu=f)
    row["ircsg_ecart_calage"] = -f - sum(v for kk, v in row.items() if kk != "financement_externe_recu")
    row["ircsg_total"] = sum(v for kk, v in row.items() if kk != "financement_externe_recu")
    ann[str(an)] = row
D["final"] = dict(
    description="C2 financé 5,5 Md€ : baisse ciblée aux points 0, 1, 1,5, 2 Smic (poids 1/1/1/0,5), taux au point 3,5 Smic"
                " relevé pour que l'impôt au point haut et au-delà soit inchangé ; plafond 48 % au point haut",
    points=P0, taux=TT, baisse_points=100 * E, financement=FIN, recette=N.recette(S, O),
    cas_types=cas, salaries={k: v for k, v in ind.items() if k.startswith("sal_")}, retraites_seuls=ret,
    retraites_couples={k: ind[k]["delta"] for k in ("retraite_couple_30k", "retraite_couple_60k")},
    familles_sans_niche_mois=fam, familles_niches=niches, second_conjoint=sc, deciles_eur=ev["dec_eur"],
    agregats=ind["agregats"], efficacite=ind["efficacite"], part_gains=ind["part_gains"], qui_recoit_les_5_5=recu)
D["annuel_final"] = ann
D["unites_final"] = ("Md€ niveau 2025 ; + = recette publique en plus ; ircsg_total = −financement externe de l'année ;"
                     " fusion λ = 0,25/0,5/0,75/1 en 2027-2030 ; financement en caisse 0 jusqu'en 2031 puis 1/2/3/4/5 et 5,5")
json.dump(D, open(OUT / "ircsg3.json", "w"), ensure_ascii=False, indent=1, default=float)

p(f"[FINAL] taux {[round(100 * x, 2) for x in TT]} aux points {[round(x) for x in P0]} ; baisse {100 * E:.2f} point ;"
  f" recette {N.recette(S, O):.2f}")
p("  salariés €/mois : " + " ; ".join(f"{k} {ind[k]['mois']:+.1f}" for k in ind if k.startswith("sal_")))
p("  retraités €/an : " + " ; ".join(f"{k} {v:+.0f}" for k, v in ret.items()))
p(f"  couples de retraités 30 k {ind['retraite_couple_30k']['delta']:+.0f}, 60 k {ind['retraite_couple_60k']['delta']:+.0f}")
p("  familles €/mois : " + " | ".join(f"{k} " + " ".join(f"{kk}:{v:+.0f}" for kk, v in r.items()) for k, r in fam.items()))
p("  niches : " + " | ".join(f"{r['libelle'][:40]} {r['net_mois']:+.0f}" for r in niches))
p("  second conjoint : " + " ; ".join(f"{k} {v['auj']:.1f} -> {v['final']:.1f} %" for k, v in sc.items()))
p("  cas : " + " ; ".join(f"{k} {v['delta']:+.0f} ({v['delta_mois']:+.0f}/m)" for k, v in cas.items()))
a, e = ind["agregats"], ind["efficacite"]
p(f"  déciles {[round(x) for x in ev['dec_eur']]} ; 10 % {a['top10']:+.2f} ; 1 % {a['top1']:+.2f} ; part des baisses D10"
  f" {100 * ind['part_gains']['part_d10']:.1f} %, 1 % {100 * ind['part_gains']['part_top1']:.1f} %")
p(f"  reçu des 5,5 : 10 % {recu['top10_Md']:+.2f}, 1 % {recu['top1_Md']:+.2f}, actifs {recu['actifs_Md']:+.2f}, retraités"
  f" {recu['retraites_Md']:+.2f} ; déciles {[round(x) for x in dec_f]}")
p(f"  efficacité : " + " ; ".join(f"{j} {e[j]['gain']:.2f} Md€, {e[j]['emplois_milliers']:.0f} k, ETP {e[j]['etp_milliers']:.0f} k,"
                                    f" travail {e[j]['travail_pct']:.2f} %" for j in e))
p("  annuel : " + " ; ".join(f"{k} {v['ircsg_total']:+.2f}" for k, v in ann.items()))
(OUT / "ircsg3_final.txt").write_text("\n".join(L) + "\n", encoding="utf-8")
