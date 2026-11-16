"""Bloc « fiscalité du capital » de la note de 8 pages (note8p/CADRE.md) : PFU inchangé, fin de l'effacement des
plus-values à la transmission, CEHR et CDHR sur les revenus du capital.

Reprend le travail de pfu/ sans le modifier : les données de base sont lues dans pfu/sorties/calculs_pfu.json (sortie de
pfu/calculs_pfu.py, recalée sur 2025) ; les jeux d'hypothèses bas / central / haut du chiffrage de l'effacement (JEUX)
et les fonctions de profil sont copiés de pfu/calculs_pfu.py (section 3). Ce qui change par rapport à pfu/ :
  1. calendrier budgétaire réaliste : transmissions soumises à la règle à partir de 2027 ; ventes des héritiers étalées ;
     impôt sur les plus-values encaissé l'année qui suit la vente (plus-values hors prélèvement à la source, payées au
     solde de l'impôt de N+1) ; table annuelle 2027-2040 ;
  2. règle de non-double imposition retenue : les droits de mutation afférents à la plus-value latente s'ajoutent au
     prix d'acquisition repris (règle américaine des donations, IRC § 1015(d)(6)) ; la recette est réduite d'autant ;
  3. deux options pour les plus-values acquises avant l'annonce : (1) prix d'acquisition historique pour tout (retenue) ;
     (2) valeur au jour de l'annonce comme prix de référence (« jour V ») ; reports d'apport-cession transmis sans
     effacement dans les deux cas ;
  4. exemple 100 000 € -> 1 000 000 € ; coin de verrouillage (rendement supplémentaire exigé pour vendre) ; coût d'un
     point de PFU ; CEHR et CDHR sur le capital ; indexation des plus-values (ordre de grandeur).

Lancer depuis fiscalite/ : python3 note8p/calculs/pfu_transmission.py
Sorties : note8p/sorties/pfu.json ; note8p/sorties/pfu_calculs.txt ; figure note8p/figures/g9_exemple_pv.{pdf,png}.
Conventions : Md€ au niveau du PIB de 2025 (pas de croissance ni d'inflation sur 2027-2040, comme les autres blocs de la
note fusionnée) ; + = recette publique en plus par rapport au droit de 2026. Statuts : [E] empirique publié ;
[S] simulation ou calcul ; [H] hypothèse ; [C] choix de politique ; [V] chiffre vérifié sur la source citée.
"""
import json
import sys
from math import log
from pathlib import Path

RACINE = Path(__file__).resolve().parents[2]          # fiscalite/
N8 = RACINE / "note8p"
SRC = json.loads((RACINE / "pfu/sorties/calculs_pfu.json").read_text(encoding="utf-8"))
L, J = [], {}
p = L.append


def fr(x, d=1):
    s = f"{x:,.{d}f}".replace(",", " ").replace(".", ",")
    return s.replace("-", "−")


# =====================================================================================================================
# 0. Paramètres : droit de 2026 et données de pfu/
# =====================================================================================================================
IR_PFU, PS_HAUT = 0.128, 0.186          # [V] CGI art. 200 A ; LFSS 2026 (loi 2025-1403) art. 12 : CSG du capital 10,6 %
PFU = IR_PFU + PS_HAUT                  # 31,4 % en 2026 (30 % de 2018 à 2025)
T_PV_REPORT = 0.30                      # [H] (pfu/calculs_pfu.py) : IR de l'année d'apport + PS ; non tranché
PIB25 = 2991.1                          # [V] Insee, PIB 2025
B25 = SRC["assiette"]["total_2025"]     # [S] assiette du PFU des revenus de 2025 (67,0 Md€ ; DGFiP n° 53 sur cases 2024)
B24 = SRC["assiette"]["total"]          # [V] revenus de 2024 (79,6 Md€), gonflés par l'anticipation de la CDHR
CEHR25 = SRC["recettes"]["cehr"]        # [V] 1,39 Md€, revenus 2025 (DGFiP n° 53, provisoire)
CDHR25 = SRC["recettes"]["cdhr"]        # [V] 0,62 Md€, revenus 2025 (DGFiP n° 53, provisoire)
STOCK_EP23, STOCK_8UT24 = 127.0, 173.268
STOCK_C = STOCK_EP23 / 152.869 * STOCK_8UT24          # ≈ 144 Md€ (pfu/calculs_pfu.py)

# Jeux d'hypothèses de l'effacement, copiés de pfu/calculs_pfu.py, toutes [H] (annexe de pfu/) ; tau = taux moyen
# effectif des droits de mutation à titre gratuit sur les titres transmis (ajout : sert à la règle de non-double
# imposition). Repère : 21,2 Md€ de DMTG en 2025 (DGFiP n° 43) pour ≈ 300 Md€ de transmissions (CAE, 2021) ≈ 7 %.
JEUX = {
    "bas": dict(E=1200, b=0.017, lam=0.40, a=0.15, h=0.02, S=STOCK_EP23, T=35, tau=0.15),
    "central": dict(E=1450, b=0.023, lam=0.55, a=0.30, h=0.04, S=STOCK_C, T=25, tau=0.10),
    "haut": dict(E=1700, b=0.030, lam=0.70, a=0.45, h=0.06, S=STOCK_8UT24, T=15, tau=0.05),
}
A_REP = 0.10                            # [H] part des reports transmis réalisée la première année (pfu/)
G_PRIX = 0.04                           # [H] hausse annuelle des valeurs (option « jour V »)
AN0, AN1 = 2027, 2040                   # transmissions soumises à la règle à partir du 1er janvier 2027 (ou de l'annonce)
ANS = list(range(AN0, AN1 + 1))

p("=" * 110)
p("BLOC FISCALITÉ DU CAPITAL (note8p) — calculs de note8p/calculs/pfu_transmission.py")
p("=" * 110)

# =====================================================================================================================
# 1. Exemple : titres acquis 100 000 €, valant 1 000 000 € (un enfant, succession, droit de 2026)
# =====================================================================================================================
# Barème des droits en ligne directe (CGI art. 777) et abattement de 100 000 € (art. 779) [V service-public F35794 ;
# seuils lus sur sources secondaires concordantes, inchangés depuis 2011-2012]
BAREME_LD = [(8072, 0.05), (12109, 0.10), (15932, 0.15), (552324, 0.20), (902838, 0.30), (1805677, 0.40),
             (float("inf"), 0.45)]
ABATT_LD = 100_000


def droits_ld(part, abatt=ABATT_LD):
    x, d, bas = max(0.0, part - abatt), 0.0, 0.0
    for haut, t in BAREME_LD:
        if x > bas:
            d += (min(x, haut) - bas) * t
        bas = haut
    return d


def tmarg_ld(part, abatt=ABATT_LD):
    x, bas = max(0.0, part - abatt), 0.0
    for haut, t in BAREME_LD:
        if x <= haut:
            return t
        bas = haut


V, B = 1_000_000, 100_000
G = V - B
EX = {}
# (a) il vend aujourd'hui, puis transmet le produit net
imp_pv = PFU * G
EX["vend"] = dict(pv=imp_pv, droits=droits_ld(V - imp_pv))
# (a') dirigeant de PME partant à la retraite : abattement fixe de 500 000 € sur la part d'IR (CGI art. 150-0 D ter,
#      cessions jusqu'au 31/12/2031) ; prélèvements sociaux sur toute la plus-value [S]
imp_retr = IR_PFU * max(0, G - 500_000) + PS_HAUT * G
EX["vend_retraite"] = dict(pv=imp_retr, droits=droits_ld(V - imp_retr))
# (b) il transmet aujourd'hui : droits sur 1 M€ ; plus-value effacée, l'héritier revend 1 M€ sans impôt
EX["transmet_actuel"] = dict(pv=0.0, droits=droits_ld(V))
# (c) réforme sans correction : droits sur 1 M€, l'héritier reprend 100 000 € et paie la plus-value en vendant
EX["reforme_brute"] = dict(pv=imp_pv, droits=droits_ld(V))
# (d) réforme retenue : droits afférents à la plus-value (droits × G / V) ajoutés au prix d'acquisition repris
d_ = droits_ld(V)
ajout = d_ * G / V
EX["reforme"] = dict(pv=PFU * (G - ajout), droits=d_, ajout_prix=ajout)
# (e) variante neutre non retenue : impôt latent déduit de l'assiette des droits
EX["reforme_neutre"] = dict(pv=imp_pv, droits=droits_ld(V - imp_pv))
# (f) titres d'entreprise transmis sous pacte Dutreil (exonération de 75 %, CGI art. 787 B ; conservation 2 + 6 ans
#     depuis la LF 2026) : aujourd'hui et avec la réforme
d_dut = droits_ld(0.25 * V)
EX["dutreil_actuel"] = dict(pv=0.0, droits=d_dut)
EX["dutreil_reforme"] = dict(pv=PFU * (G - d_dut * G / V), droits=d_dut, ajout_prix=d_dut * G / V)
for k, v in EX.items():
    v["total"] = v["pv"] + v["droits"]
    v["net_heritier"] = V - v["total"]
p("1. Exemple : titres acquis 100 000 €, valant 1 000 000 €, un enfant (droit de 2026 ; hors CEHR et CDHR l'année de la vente)")
NOMS_EX = {"vend": "vend aujourd'hui (PFU 31,4 %), transmet le produit", "vend_retraite": "idem, dirigeant partant à la retraite (abattement 500 k€ sur l'IR)",
           "transmet_actuel": "transmet aujourd'hui (plus-value effacée)", "reforme_brute": "réforme sans correction",
           "reforme": "réforme retenue (droits afférents à la PV ajoutés au prix)", "reforme_neutre": "variante neutre (impôt latent déduit des droits)",
           "dutreil_actuel": "titres sous pacte Dutreil, aujourd'hui", "dutreil_reforme": "titres sous pacte Dutreil, réforme"}
for k, v in EX.items():
    p(f"   {NOMS_EX[k]:62s} : impôt PV {fr(v['pv'], 0):>9s} € ; droits {fr(v['droits'], 0):>9s} € ; total "
      f"{fr(v['total'], 0):>9s} € ({fr(100 * v['total'] / V, 1)} %) ; reste à l'héritier {fr(v['net_heritier'], 0)} €")
p(f"   taux marginal des droits sur 1 M€ : {fr(100 * tmarg_ld(V), 0)} % ; droits afférents à la PV ajoutés au prix : "
  f"{fr(EX['reforme']['ajout_prix'], 0)} € ; écart réforme retenue − vente avant décès : "
  f"{fr(EX['reforme']['total'] - EX['vend']['total'], 0)} €")
J["exemple"] = dict(valeur=V, prix=B, pfu=PFU, cas=EX)

# =====================================================================================================================
# 2. Coin de verrouillage : rendement supplémentaire qu'un autre placement doit offrir pour qu'il vaille la peine de
#    vendre (plus-value de 90 % de la valeur ; rendement 5 % ; impôt sur les plus-values seul, droits proportionnels)
# =====================================================================================================================


def seuil_x(gv, t, r, D, step_up):
    """x tel que vendre maintenant et placer à r + x donne la même richesse nette qu'au terme D. step_up=True : la
    plus-value s'efface au terme (décès, droit actuel) ; False : elle est imposée au terme (vente par l'héritier)."""
    def ecart(x):
        w0 = 1 - t * gv
        if step_up:
            garde, vend = (1 + r) ** D, w0 * (1 + r + x) ** D
        else:
            vD = (1 + r) ** D
            garde = vD - t * (vD - (1 - gv))
            wD = w0 * (1 + r + x) ** D
            vend = wD - t * (wD - w0)
        return vend - garde
    lo, hi = 0.0, 0.5
    for _ in range(100):
        m = (lo + hi) / 2
        lo, hi = (m, hi) if ecart(m) < 0 else (lo, m)
    return lo


VERR = {}
for gv in (0.9, 0.55):
    for D in (5, 10, 20):
        VERR[f"gv{gv}_D{D}"] = dict(actuel=seuil_x(gv, PFU, 0.05, D, True), reforme=seuil_x(gv, PFU, 0.05, D, False))
p("")
p("2. Verrouillage : rendement supplémentaire exigé pour vendre et réinvestir (points par an ; r = 5 %) [S]")
for k, v in VERR.items():
    p(f"   {k} : droit actuel (effacement au terme) {fr(100 * v['actuel'], 2)} pt ; réforme (imposé au terme) "
      f"{fr(100 * v['reforme'], 2)} pt")
p("   héritier aujourd'hui : prix d'acquisition = valeur reçue, plus-value nulle -> 0 pt ; avec la réforme : ligne « réforme »")
J["verrouillage"] = VERR

# =====================================================================================================================
# 3. Recette de la fin de l'effacement, 2027-2040
# =====================================================================================================================


def profil_ventes(a, h, n=40):
    """Part de la plus-value latente d'une cohorte vendue l'année calendaire c + j (j = 0..n) : la part a vendue dans
    les douze mois est répartie pour moitié sur l'année de la transmission et l'année suivante ; ensuite (1−a)·h·(1−h)^(k−2)
    l'année c + k − 1 (k ≥ 2), comme dans pfu/calculs_pfu.py."""
    v = [0.0] * (n + 2)
    v[0] += a / 2
    v[1] += a / 2
    for k in range(2, n + 1):
        v[k - 1] += (1 - a) * h * (1 - h) ** (k - 2)
    return v


def recette(Lc, a, h, phi=lambda c: 1.0):
    """Recette encaissée l'année y : impôt sur les ventes de l'année y − 1 (solde de l'IR et prélèvements sociaux de N+1)."""
    pv = profil_ventes(a, h)
    out = {}
    for y in ANS:
        s = 0.0
        for c in range(AN0, y):          # cohortes transmises de 2027 à y − 1 (ventes au plus tard en y − 1)
            j = (y - 1) - c
            if 0 <= j < len(pv):
                s += Lc * phi(c) * pv[j]
        out[y] = s
    return out


def phi_jour_v(lam):
    """Option « jour V » : seule la plus-value acquise depuis l'annonce (fin 2026) est reprise."""
    return lambda c: min(1.0, (1 - (1 + G_PRIX) ** (-(c - AN0 + 1))) / lam)


EFF, ANNUEL_J = {}, {}
for nom, q in JEUX.items():
    G_aut = q["E"] * q["b"] * q["lam"]
    L_aut = PFU * G_aut * (1 - q["tau"])          # droits afférents à la plus-value ajoutés au prix d'acquisition
    L_rep = T_PV_REPORT * q["S"] / q["T"] * (1 - q["tau"])
    r_aut = recette(L_aut, q["a"], q["h"])
    r_rep = recette(L_rep, A_REP, q["h"])
    r_v = recette(L_aut, q["a"], q["h"], phi=phi_jour_v(q["lam"]))
    EFF[nom] = dict(q, G_aut=G_aut, L_aut=L_aut, L_rep=L_rep, L=L_aut + L_rep, L_brut=PFU * G_aut + T_PV_REPORT * q["S"] / q["T"],
                    hist={y: r_aut[y] + r_rep[y] for y in ANS}, rep={y: r_rep[y] for y in ANS},
                    jour_v={y: r_v[y] + r_rep[y] for y in ANS})
p("")
p("3. Fin de l'effacement : recette encaissée par année (Md€ au niveau du PIB 2025) [S sur hypothèses H]")
p("   transmissions soumises à la règle à partir de 2027 ; ventes : a dans les douze mois (moitié l'année même), puis h par an ;")
p("   impôt encaissé l'année qui suit la vente ; droits afférents à la plus-value ajoutés au prix (recette × (1 − τ))")
for nom, e in EFF.items():
    p(f"   {nom:8s} impôt latent transmis par an {fr(e['L_brut'], 2)} brut, {fr(e['L'], 2)} net de la correction "
      f"(τ = {fr(100 * e['tau'], 0)} %) ; dont reports {fr(e['L_rep'], 2)}")
p("   année   " + "  ".join(f"{y}" for y in ANS))
for nom, e in EFF.items():
    p(f"   {nom:8s}" + " ".join(f"{e['hist'][y]:5.2f}" for y in ANS) + "   (option 1 : prix historique pour tout)")
    p(f"   {'':8s}" + " ".join(f"{e['jour_v'][y]:5.2f}" for y in ANS) + "   (option 2 : valeur au jour de l'annonce)")
    p(f"   {'':8s}" + " ".join(f"{e['rep'][y]:5.2f}" for y in ANS) + "   (dont reports d'apport-cession)")
CUM = {nom: dict(hist=sum(e["hist"].values()), jour_v=sum(e["jour_v"].values()),
                 hist_2027_2031=sum(e["hist"][y] for y in range(2027, 2032)),
                 jour_v_2027_2031=sum(e["jour_v"][y] for y in range(2027, 2032))) for nom, e in EFF.items()}
for nom, c in CUM.items():
    p(f"   cumul 2027-2040 {nom:8s} : option 1 {fr(c['hist'], 1)} ; option 2 {fr(c['jour_v'], 1)} "
      f"({fr(100 * c['jour_v'] / c['hist'], 0)} %) ; coût de l'option 2 {fr(c['hist'] - c['jour_v'], 1)} Md€ ; "
      f"2027-2031 : {fr(c['hist_2027_2031'], 1)} contre {fr(c['jour_v_2027_2031'], 1)}")
# régime de croisière (cohortes illimitées) pour situer 2040
q = JEUX["central"]
croisiere = EFF["central"]["L"]
p(f"   repère : recette de très long terme (toutes cohortes vendues) ≈ impôt latent net transmis par an = {fr(croisiere, 2)} Md€ (central)")

# Sensibilité : effet d'annonce mal géré (une année de transmissions anticipées avant la date d'effet)
p("   si la date d'effet suivait l'annonce d'un an : une cohorte avancée échappe à la règle, soit "
  + " ; ".join(f"{nom} {fr(EFF[nom]['L'], 1)} Md€ d'impôt latent perdu" for nom in EFF))
J["effacement"] = {nom: dict(hyp={k: e[k] for k in ("E", "b", "lam", "a", "h", "S", "T", "tau")}, impot_latent_brut=e["L_brut"],
                             impot_latent_net=e["L"], dont_reports=e["L_rep"], cumul=CUM[nom]) for nom, e in EFF.items()}

# Sensibilité de la correction des droits (τ = 0 : pas de correction)
p("   sans correction des droits (τ = 0), recette 2040 centrale : " + fr(EFF["central"]["hist"][2040] / (1 - JEUX["central"]["tau"]), 2)
  + f" au lieu de {fr(EFF['central']['hist'][2040], 2)}")

# PLF 2027, art. 5 (expiration des reports à la transmission), en discussion, non retenu dans la base
art5_c = T_PV_REPORT * JEUX["central"]["S"] / JEUX["central"]["T"]
p(f"   PLF 2027 art. 5 (version du Gouvernement, si adoptée) : ≈ {fr(art5_c, 1)} Md€ par an d'impôt exigible à la transmission"
  " (central, avant étalement) ; la ligne « reports » ci-dessus se retrancherait alors de notre recette")

# =====================================================================================================================
# 4. PFU : coût d'un point ; CEHR et CDHR sur le capital ; CRDS
# =====================================================================================================================


def changement(t1, b, e=0.77, t0=PFU):
    dq = e * b * log((1 - t1) / (1 - t0))
    return (t1 - t0) * b, t1 * (b + dq) - t0 * b, {pi: (t1 - t0) * b + pi * t1 * dq for pi in (0.0, 0.5, 1.0)}


PT = {}
for nb, b in (("2025", B25), ("2024", B24)):
    meca, prem, perm = changement(PFU - 0.01, b)
    prem_e = [changement(PFU - 0.01, b, e)[1] for e in (0.65, 0.77, 1.0)]
    PT[nb] = dict(meca=meca, prem_077=prem, prem_e=prem_e, perm=perm)
# reprise par la CDHR d'une baisse par la part d'IR (pfu/ : 0,66 à 1,10 Md€ pour 6,4 points, tant qu'elle existe)
rep_cdhr = [x / 6.4 for x in SRC["cdhr_reprise"]]
p("")
p("4. Coût d'un point de PFU (31,4 -> 30,4 %), Md€ par an [S ; élasticité e = 0,77 (Lefebvre, Lehmann et Sicsic, 2025) E]")
for nb, d in PT.items():
    p(f"   revenus {nb} : mécanique {fr(d['meca'], 2)} ; premières années (e = 0,65 / 0,77 / 1) "
      + " / ".join(fr(x, 2) for x in d["prem_e"]) + " ; régime permanent (π = 0 / 0,5 / 1) "
      + " / ".join(fr(d["perm"][pi], 2) for pi in (0.0, 0.5, 1.0)))
p(f"   baisse par la part d'IR : la CDHR en reprend {fr(rep_cdhr[0], 2)} à {fr(rep_cdhr[1], 2)} par point tant qu'elle existe")
p(f"   repères : baisse à 25 % (6,4 points) {fr(SRC['naif']['PFU 25 % 2025']['meca'], 2)} mécanique, "
  f"{fr(SRC['naif']['PFU 25 % 2025']['prem'][1], 2)} premières années (pfu/)")
crds_pfu = 0.005 * B25
p(f"   CRDS (0,5 point) comprise dans les 18,6 % : sur l'assiette du PFU {fr(crds_pfu, 2)} Md€ ; s'éteint fin 2033 (droit en vigueur)")
J["pfu"] = dict(taux=PFU, assiette_2025=B25, assiette_2024=B24, cout_point=PT, reprise_cdhr_par_point=rep_cdhr,
                crds_sur_assiette_pfu=crds_pfu)

CAP = dict(cehr_total=CEHR25, cehr_capital=[0.5 * CEHR25, 0.8 * CEHR25], cdhr_total=CDHR25,
           cdhr_capital=[0.8 * CDHR25, 1.0 * CDHR25])
p("")
p("5. CEHR et CDHR sur les revenus du capital (revenus 2025, DGFiP n° 53, provisoire) [V ; parts H]")
p(f"   CEHR {fr(CEHR25, 2)} Md€ tous revenus ; part sur le capital 50-80 % -> {fr(CAP['cehr_capital'][0], 2)} à {fr(CAP['cehr_capital'][1], 2)}")
p(f"   CDHR {fr(CDHR25, 2)} Md€ ; due par des foyers dont le taux moyen est < 20 %, surtout grâce au PFU -> 80-100 % -> "
  f"{fr(CAP['cdhr_capital'][0], 2)} à {fr(CAP['cdhr_capital'][1], 2)}")
p("   maintien sur le capital (majoration de 3/4 points du PFU au-delà des mêmes seuils de revenu) : 0 ; suppression de la")
p(f"   CEHR sur le capital : −{fr(CAP['cehr_capital'][0], 1)} à −{fr(CAP['cehr_capital'][1], 1)} avant la reprise par la CDHR des foyers à son plancher")
J["cehr_cdhr_capital"] = CAP

# =====================================================================================================================
# 5. Indexation des plus-values sur l'inflation : ordre de grandeur [H]
# =====================================================================================================================
# Plus-values imposées des revenus 2025 : 13,0 Md€ (pfu/) ; détention moyenne N ans ; inflation 2 % ; prix de revient
# égal à une fraction k du prix de cession
PV25 = SRC["assiette"]["pv_2025"]
IDX = {}
for N, k in ((5, 0.6), (10, 0.5), (15, 0.4)):
    infl = k * ((1.02) ** N - 1)          # part inflationniste du prix de vente
    gain = 1 - k                          # plus-value nominale (part du prix)
    IDX[f"N{N}"] = dict(part_gain=infl / gain, cout=PFU * PV25 * infl / gain)
p("")
p("6. Indexation du prix d'acquisition sur l'inflation (2 %/an) : coût sur les plus-values imposées de 2025 [H]")
for k_, v in IDX.items():
    p(f"   détention {k_} : {fr(100 * v['part_gain'], 0)} % de la plus-value imposée est inflationniste -> coût {fr(v['cout'], 2)} Md€ par an")
J["indexation"] = IDX

# =====================================================================================================================
# 6. Table annuelle pour le bouclage
# =====================================================================================================================
ANNUEL = {}
for y in ANS:
    ANNUEL[str(y)] = {
        "fin_effacement_central": round(EFF["central"]["hist"][y], 3),
        "fin_effacement_bas": round(EFF["bas"]["hist"][y], 3),
        "fin_effacement_haut": round(EFF["haut"]["hist"][y], 3),
        "dont_reports_apport_cession_central": round(EFF["central"]["rep"][y], 3),
        "variante_jour_v_central": round(EFF["central"]["jour_v"][y], 3),
        "variante_jour_v_bas": round(EFF["bas"]["jour_v"][y], 3),
        "variante_jour_v_haut": round(EFF["haut"]["jour_v"][y], 3),
        "taux_pfu_inchange": 0.0,
        "cehr_cdhr_capital_maintenues": 0.0,
    }
J["annuel"] = ANNUEL
J["unites"] = ("Md€ au niveau du PIB 2025 (pas de croissance) ; + = recette en plus par rapport au droit de 2026 ; "
               "la ligne fin_effacement ne doit être réutilisée qu'une fois constatée (CADRE.md)")
J["cout_par_point"] = {
    "pfu_1_point_revenus2025_mecanique": round(PT["2025"]["meca"], 3),
    "pfu_1_point_revenus2025_premieres_annees_e077": round(PT["2025"]["prem_077"], 3),
    "pfu_1_point_revenus2025_permanent_pi05": round(PT["2025"]["perm"][0.5], 3),
    "pfu_1_point_reprise_cdhr_si_baisse_part_ir": [round(x, 3) for x in rep_cdhr],
    "suppression_cehr_sur_capital": [-round(x, 2) for x in CAP["cehr_capital"]],
    "suppression_cdhr": -round(CDHR25, 2),
}
J["sources_cle"] = {
    "pfu_2026": "CGI art. 200 A ; LFSS 2026 art. 12 (CSG capital 10,6 %) [V, pfu/donnees/pfu_chiffres.csv]",
    "retraite_dirigeant": "CGI art. 150-0 D ter, abattement fixe 500 000 € prorogé au 31/12/2031 (LF 2025) [S]",
    "droits_succession": "CGI art. 777 et 779 ; service-public F35794 [V/S]",
    "dutreil_lf2026": "LF 2026 (loi 2026-103) : engagement individuel 4 -> 6 ans, biens somptuaires exclus [S]",
    "plf2027_art5": "Adopté en 1re lecture à l'AN le 16/10/2026 sous une forme amendée (successions exclues) ; première partie rejetée le 04/11/2026 (scrutin 9759) [S]",
    "exit_tax": "CGI art. 167 bis : dégrèvement après 2 ans (5 ans au-delà de 2,57 M€) [S] ; amendements AN du 30/10/2026 (15 ans) dans un texte rejeté [S]",
    "irc_1015d6": "26 U.S.C. § 1015(d)(6) [V]",
}

(N8 / "sorties").mkdir(exist_ok=True)
(N8 / "sorties" / "pfu.json").write_text(json.dumps(J, ensure_ascii=False, indent=1, default=float), encoding="utf-8")
(N8 / "sorties" / "pfu_calculs.txt").write_text("\n".join(L) + "\n", encoding="utf-8")
print("\n".join(L))

# =====================================================================================================================
# 7. Figure g9_exemple_pv (charte.py)
# =====================================================================================================================
if "--sans-figure" not in sys.argv:
    sys.path.insert(0, str(N8))
    from charte import plt, axes, sauver, AUJ, PROP, HAUSSE, ENCRE, ENCRE2, PLEINE, _fr  # noqa: E402

    cas = [("vend", "Il vend, puis\ntransmet le produit"), ("transmet_actuel", "Il transmet\n(droit actuel)"),
           ("reforme", "Il transmet ;\nl'héritier vend (réforme)")]
    fig, ax = plt.subplots(figsize=(PLEINE, 2.4))
    axes(ax, grille="x")
    for i, (k, lab) in enumerate(cas):
        d, pv = EX[k]["droits"] / 1e3, EX[k]["pv"] / 1e3
        y = len(cas) - 1 - i
        ax.barh(y, d, color=AUJ, height=0.55, zorder=2, label="Droits de succession" if i == 0 else None)
        ax.barh(y, pv, left=d, color=HAUSSE if k == "reforme" else PROP, height=0.55, zorder=2,
                label="Impôt sur la plus-value" if i == 0 else None)
        ax.text(d + pv + 6, y, f"{_fr(d + pv)} k€", va="center", fontsize=7.5, color=ENCRE)
    ax.set_yticks(range(len(cas)))
    ax.set_yticklabels([c[1] for c in cas][::-1])
    ax.set_xlim(0, 520)
    ax.xaxis.set_major_formatter(__import__("matplotlib.ticker", fromlist=["FuncFormatter"]).FuncFormatter(
        lambda v, _: _fr(v) + " k€"))
    from matplotlib.patches import Patch
    ax.legend(handles=[Patch(color=AUJ, label="Droits de succession"), Patch(color=PROP, label="Impôt sur la plus-value"),
                       Patch(color=HAUSSE, label="Impôt sur la plus-value, payé par l'héritier")],
              loc="lower center", bbox_to_anchor=(0.45, 1.0), ncol=3, fontsize=7, handlelength=1.2)
    ax.tick_params(axis="y", length=0)
    sauver(fig, "g9_exemple_pv",
           "calculs des auteurs (note8p/calculs/pfu_transmission.py), droit de 2026 : PFU de 31,4 %, barème des droits "
           "en ligne directe après abattement de 100 000 €.",
           "Titres acquis 100 000 €, valant 1 000 000 €, un seul enfant ; hors CEHR et CDHR l'année de la vente. "
           "Réforme : les droits afférents à la plus-value (191 666 €) s'ajoutent au prix d'acquisition repris.")
