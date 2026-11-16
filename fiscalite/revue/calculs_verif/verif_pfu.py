"""Vérification indépendante des chiffres clés de la partie « Revenus du capital » (PFU, holdings, apport-cession,
CEHR/CDHR, perte sèche). Écrit sans réutiliser le code du dépôt ; les seuls chiffres repris sont ceux des sources
citées en commentaire. Sortie : verif_pfu_sortie.txt (même dossier).

Lancer : python3 verif_pfu.py
"""
from math import log
from pathlib import Path

OUT = Path(__file__).resolve().parent / "verif_pfu_sortie.txt"
L = []
p = L.append


def f(x, d=2):
    return f"{x:.{d}f}"


# ------------------------------------------------------------------ paramètres (droit 2026)
IR_PFU, PS_HAUT, PS_BAS = 0.128, 0.186, 0.172          # CGI 200 A ; LFSS 2026 art. 12
PFU = IR_PFU + PS_HAUT                                  # 31,4 %
IS, CSB = 0.25, 0.033                                   # IS normal ; contribution sociale (IS > 763 000 €)
IS_CSB = IS * (1 + CSB)                                 # 25,825 %
IS_CE = 0.36125                                         # IS + contribution exceptionnelle maximale (CA > 3 Md€)
QPFC = 0.05                                             # quote-part de frais et charges (mère-fille)

# ------------------------------------------------------------------ 1. taux cumulés
p("== 1. Taux cumulés sur 100 de bénéfice ==")
for nom, is_ in (("IS 25 %", IS), ("IS 25,825 %", IS_CSB), ("IS 36,125 %", IS_CE)):
    for perso, t in (("PFU", PFU), ("PFU+CEHR 4", PFU + 0.04), ("CDHR 20+18,6", 0.20 + PS_HAUT),
                     ("PFU 25", 0.25)):
        p(f"  {nom:12s} {perso:13s}: {100 * (is_ + (1 - is_) * t):.2f} %")
for nom, is_ in (("IS 25 %", IS), ("IS 25,825 %", IS_CSB)):
    h = is_ + (1 - is_) * QPFC * IS
    hi = is_ + (1 - is_) * 0.01 * IS
    p(f"  holding, {nom} : QPFC 5 % -> {100 * h:.2f} % ; intégration (1 %) -> {100 * hi:.2f} %")
sal = 0.097 + 0.49 * (1 - 0.068)
p(f"  salaire, TMS hors cotisations : 9,7 + 49 × (1 − 6,8 %) = {100 * sal:.2f} %")
p(f"  new view : 100 × (1 − PFU) = {100 * (1 - PFU):.1f} ; 105 × (1 − PFU) = {105 * (1 - PFU):.2f}")

# ------------------------------------------------------------------ 2. assiette
DIV, INT, AUTRES, PV, CRYPTO, MV = 50.136, 10.428, 1.349, 18.777, 0.368, 1.444   # 2042, revenus 2024 (Md€)
B = DIV + INT + AUTRES + PV + CRYPTO - MV
p("\n== 2. Assiette du PFU (totaux 2042, revenus 2024) ==")
p(f"  2DC {DIV} + 2TR {INT} + 2TS {AUTRES} + 3VG {PV} + 3AN {CRYPTO} − 3VH {MV} = {B:.2f} Md€")
p(f"  IR à 12,8 % : {IR_PFU * B:.2f} Md€ (majorant : 2,54 M de foyers optent pour le barème) ; "
  f"acompte 2CK 7,665 Md€ -> assiette {7.665 / 0.128:.1f} Md€")
p(f"  PS à 18,6 % sur cette assiette : {PS_HAUT * B:.2f} Md€")
# dividendes 2024 gonflés par l'anticipation de la CDHR : Insee (IP 2105) +13,9 Md€ en 2024, −10,5 Md€ en 2025 ;
# rapport AN n° 3056 : 61,0 -> 74,9 -> 64,3 Md€ (comptes nationaux, dividendes reçus par les ménages)
k25 = 64.3 / 74.9
B25 = B - DIV * (1 - k25)
p(f"  variante 2025 : dividendes × {k25:.3f} (64,3/74,9) -> assiette {B25:.1f} Md€")

# ------------------------------------------------------------------ 3. PFU à 25 % et hausses


def reaction(e, b, t0, t1, forme="log"):
    if forme == "log":
        return e * b * log((1 - t1) / (1 - t0))
    return e * b * ((1 - t1) - (1 - t0)) / (1 - t0)         # linéaire, relative au taux de départ


def recette(t0, t1, b, e, forme="log"):
    dq = reaction(e, b, t0, t1, forme)
    return t1 * (b + dq) - t0 * b, dq


p("\n== 3. PFU ramené à 25 % (baisse de 6,4 points, assiette b) ==")
for nb, b in (("2024 (79,6)", B), ("2025 (dividendes −14 %)", B25)):
    p(f"  assiette {nb} : coût mécanique {(PFU - 0.25) * b:.2f} Md€")
    for e in (0.65, 0.77, 1.0):
        r_log, dq = recette(PFU, 0.25, b, e)
        r_lin, _ = recette(PFU, 0.25, b, e, "lin")
        # régime permanent : seule la part pi de la réaction est une recette durable (le reste est un calendrier :
        # le bénéfice aurait été distribué plus tard et imposé ; avec un taux permanent, le moment de la
        # distribution ne change pas la valeur actualisée de l'impôt)
        perm = {pi: (PFU - 0.25) * b - pi * 0.25 * dq for pi in (0.0, 0.5, 1.0)}
        p(f"    e = {e} : réaction +{dq:.2f} ; coût premières années {-r_log:.2f} (log) / {-r_lin:.2f} (linéaire)"
          f" ; régime permanent π = 0 / 0,5 / 1 : {perm[0.0]:.2f} / {perm[0.5]:.2f} / {perm[1.0]:.2f}")

p("  hausses :")
for t1 in (0.33, 0.344):
    m = (t1 - PFU) * B
    for e in (0.65, 0.77, 1.0):
        r, _ = recette(PFU, t1, B, e)
        p(f"    {100 * PFU:.1f} -> {100 * t1:.1f} %, e = {e} : mécanique {m:.2f} ; net {r:.2f} ({100 * r / m:.0f} %)")
# reproduction CAE Focus 124 : 30 -> 33 %, assiette 57 Md€, e = 0,65 ; formule CAE ΔR = Δt B (1 − e t1/(1 − t1))
cae = 0.03 * 57 * (1 - 0.65 * 0.33 / 0.67)
r_cae, _ = recette(0.30, 0.33, 57, 0.65)
p(f"  CAE 124 reproduit : formule CAE {cae:.2f} ; formule log {r_cae:.2f} (publié : 1,2 ; brut 1,7)")
p(f"  CAE 147 : brut 0,9 Md€ pour 1,5 pt d'IR -> assiette implicite {0.9 / 0.015:.0f} Md€")
for e in (0.65, 0.77, 1.0):
    p(f"  e = {e} : taux maximisant la recette 1/(1+e) = {100 / (1 + e):.1f} % ; coût marginal d'un euro levé à 31,4 % "
      f"= {1 / (1 - e * PFU / (1 - PFU)):.2f}")

# ------------------------------------------------------------------ 4. interaction PFU / CDHR (réduction de la part IR)
p("\n== 4. Rentier (dividendes seuls, personne seule) : PFU, CEHR, CDHR ==")


def cehr(r, seul=True):
    s1, s2 = (250e3, 500e3) if seul else (500e3, 1e6)
    return 0.03 * max(0, min(r, s2) - s1) + 0.04 * max(0, r - s2)


def cdhr(r, impot, seul=True, pac=0):
    s = 250e3 if seul else 500e3
    if r <= s:
        return 0.0
    decote = max(0.0, 0.20 * r - 0.825 * (r - s))
    return max(0.0, 0.20 * r - decote - (impot + 1500 * pac + (0 if seul else 12500)))


for D in (200e3, 300e3, 600e3, 3e6):
    for nom, ir in (("PFU 31,4", IR_PFU), ("PFU 25 (IR 6,4)", 0.064)):
        i = ir * D
        c = cehr(D)
        d = cdhr(D, i + c)
        tot = i + c + d + PS_HAUT * D
        p(f"  {D / 1e3:6.0f} k€ {nom:16s}: IR {i / 1e3:7.1f} CEHR {c / 1e3:6.1f} CDHR {d / 1e3:6.1f} PS {PS_HAUT * D / 1e3:6.1f}"
          f" -> {tot / 1e3:7.1f} k€ ({100 * tot / D:.1f} %)")
    # PFU à 25 % par les prélèvements sociaux (12,2 %)
    i, c = IR_PFU * D, cehr(D)
    d = cdhr(D, i + c)
    p(f"  {D / 1e3:6.0f} k€ PFU 25 (PS 12,2)   : total {(i + c + d + 0.122 * D) / 1e3:7.1f} k€ ({100 * (i + c + d + 0.122 * D) / D:.1f} %)")
# ordre de grandeur de la reprise par la CDHR d'une baisse de la part IR : pour un rentier pur au-delà de 500 k€,
# l'écart au plancher est d'environ 20 − 12,8 − ~3,9 ≈ 3,3 points ; la baisse de 6,4 points est reprise en entier.
for y in (0.37, 0.6):
    p(f"  CDHR {y} Md€ (acompte 2025 / PLF 2027) ; si ses redevables étaient des rentiers purs (écart 3,3 pts) : assiette"
      f" PFU {y / 0.033:.0f} Md€ ; reprise d'une baisse de 6,4 pts : {0.064 * y / 0.033:.2f} Md€")

# ------------------------------------------------------------------ 5. apport-cession
p("\n== 5. Expiration du report de l'apport-cession à toute transmission ==")
ENTREES = {2020: 10.841, 2021: 16.358, 2022: 18.366, 2023: 33.636, 2024: 22.172}   # AN 3056, tableau DGFiP
EXPIRES = {2020: 0.313, 2021: 0.494, 2022: 0.635, 2023: 0.418, 2024: 1.514}
STOCK = {2020: 78.787, 2021: 96.640, 2022: 117.130, 2023: 152.869, 2024: 173.268}  # case 8UT (majorant, note 462)
for a in range(2021, 2025):
    ds = STOCK[a] - STOCK[a - 1]
    p(f"  {a} : Δstock {ds:6.2f} ; entrées − expirés {ENTREES[a] - EXPIRES[a]:6.2f} ; écart {ds - ENTREES[a] + EXPIRES[a]:+.2f}")
EP_2023 = 127.0     # PLF 2027, évaluation préalable de l'art. 5, § 1.1
r = EP_2023 / STOCK[2023]
p(f"  stock EP 2023 / 8UT 2023 = {r:.3f} -> stock 2024 corrigé ≈ {r * STOCK[2024]:.0f} Md€")
for S, nom in ((EP_2023, "EP 2023"), (STOCK[2023], "8UT 2023"), (r * STOCK[2024], "2024 corrigé"), (STOCK[2024], "8UT 2024")):
    row = []
    for T in (15, 25, 35):
        for tau in (0.30, PFU):
            row.append(f"T={T},τ={100 * tau:.1f}: {S / T * tau:.2f}")
    p(f"  {nom:12s} ({S:.0f}) : " + " ; ".join(row))
moy = sum(ENTREES[a] for a in (2022, 2023, 2024)) / 3
p(f"  entrées moyennes 2022-2024 : {moy:.1f} Md€ ; impôt potentiel à 30-31,4 % : {0.30 * moy:.1f}-{PFU * moy:.1f} Md€/an"
  f" (borne de très long terme, si tout est transmis et si les entrées restent à ce niveau)")
# lecture de l'évaluation préalable : 500 M€ en 2027 = 200 IR + 300 PS
p(f"  EP : 300 M€ de PS -> plus-values {0.3 / PS_HAUT:.2f} Md€ (à 18,6 %) ou {0.3 / PS_BAS:.2f} (17,2 %) ; IR implicite "
  f"{0.3 / PS_HAUT * IR_PFU * 1000:.0f} M€ (publié : 200)")
p("    lecture a) 500 M€ = 1/5 d'une année pleine (étalement appliqué à tout) -> année pleine "
  f"{0.5 * 5:.1f} Md€, soit {0.5 * 5 / PFU:.1f} Md€ de plus-values transmises par an")
p("    lecture b) 500 M€ = un trimestre de transmissions (1er oct.-31 déc. 2026), sans étalement -> année pleine "
  f"{0.5 * 4:.1f} Md€")
q = 0.5 / (PS_HAUT + IR_PFU / 5)
p(f"    lecture c) un trimestre, étalement de l'IR seul (texte de l'art. 1681 G) -> {q:.2f} Md€ de PV par trimestre,"
  f" année pleine {4 * q * PFU:.1f} Md€ (mais partage IR/PS {IR_PFU / 5 * q * 1000:.0f}/{PS_HAUT * q * 1000:.0f}"
  f", incompatible avec 200/300)")
pv84 = 23.5 / 84
p(f"  84 foyers : {pv84 * 1000:.0f} M€ de plus-value chacun ; × 30 / 31,4 / 35,4 % = {pv84 * 300:.0f} / {pv84 * 314:.0f} / "
  f"{pv84 * 354:.0f} M€")
p(f"  part des entrées 2023 au top 0,01 % : {18.810 / 33.636:.3f} ; 84 foyers : {23.5 / 33.636:.3f}")

# ------------------------------------------------------------------ 6. prélèvements sociaux
p("\n== 6. Alignement des prélèvements sociaux à 18,6 % ==")
p(f"  amendement sans exclusions 2,8 Md€ / 1,4 pt -> assiette {2.8 / 0.014:.0f} Md€ ; texte voté 1,5 -> {1.5 / 0.014:.0f} Md€")
p(f"  prélèvement de solidarité 2027 (PLF, état A, l. 1427) 15,305 / 7,5 % -> assiette {15.305 / 0.075:.0f} Md€")
p(f"  CRDS 2024 (0,37 + 0,58) / 0,5 % -> {(0.37 + 0.58) / 0.005:.0f} Md€")
p(f"  assiette restée à 17,2 % : {2.8 / 0.014 - 1.5 / 0.014:.0f} Md€ -> alignement {0.014 * (2.8 / 0.014 - 1.5 / 0.014):.2f} Md€ ;"
  f" avec l'assiette 204 Md€ − 107 : {0.014 * (204 - 107):.2f}")
fonc = 34.953 + 0.7 * 8.482
p(f"  repère : revenus fonciers 4BA + 70 % de 4BE = {fonc:.1f} Md€ (déficits non déduits)")

# ------------------------------------------------------------------ 7. perte sèche (formule du dépôt, puis corrigée)
p("\n== 7. Perte sèche d'un PFU à 25 % (Harberger, prix d'un milliard μ−1) ==")
MU1 = (0.04, 0.08, 0.17)
for e in (0.65, 0.77, 1.0):
    dq = reaction(e, B, PFU, 0.25)
    tbar = (PFU + 0.25) / 2
    for pi in (0.0, 0.5, 1.0):
        depot = [-pi * tbar * dq + m * ((PFU - 0.25) * B - 0.25 * dq) for m in MU1]
        perm = [-pi * tbar * dq + m * ((PFU - 0.25) * B - pi * 0.25 * dq) for m in MU1]
        p(f"  e = {e} π = {pi} : dépôt " + " / ".join(f"{x:+.2f}" for x in depot)
          + " ; corrigé (recette permanente) " + " / ".join(f"{x:+.2f}" for x in perm))

# ------------------------------------------------------------------ 8. exil
p("\n== 8. Exil (CAE Focus 118 : 0,02 à 0,23 % du top 1 % par point d'imposition effective, à long terme) ==")
base_top = 0.96 * DIV + 0.8 * PV + 0.3 * INT       # parts : 96 % des dividendes (FS 2021) ; PV et intérêts : hypothèses
for dpt in (0.0002, 0.0023):
    part = dpt * 6.4
    p(f"  {100 * dpt:.2f} %/pt × 6,4 pts = {100 * part:.2f} % du top 1 % retenu ; assiette PFU du top 1 % ≈ {base_top:.0f} Md€ ;"
      f" recette gardée ≈ {part * 0.25 * base_top:.3f} Md€ (PFU à 25 % seul)")

# ------------------------------------------------------------------ 9. cas types (droit 2026, barème des revenus 2024)
p("\n== 9. Cas types (personne seule, 1 part ; barème IR des revenus 2024 ; non indexé) ==")
SEUILS = [0, 11497, 29315, 83823, 180294]
TAUX = [0, 0.11, 0.30, 0.41, 0.45]


def bareme(x):
    t = 0.0
    for i, s in enumerate(SEUILS):
        h = SEUILS[i + 1] if i + 1 < len(SEUILS) else float("inf")
        t += TAUX[i] * max(0.0, min(x, h) - s)
    return t


def cas(nom, autre, div, interets, pv, seul=True):
    """autre : revenu net imposable au barème hors capital (salaire après abattement, pension…)."""
    cap = div + interets + pv
    base_ir = bareme(autre)
    # PFU
    ir_pfu = base_ir + IR_PFU * cap
    rfr = autre + cap
    c = cehr(rfr)
    d = cdhr(rfr, ir_pfu + c)
    pfu_tot = IR_PFU * cap + PS_HAUT * cap + (c - cehr(autre)) + d
    # option barème : abattement 40 % sur dividendes, CSG déductible 6,8 % ; RFR avec dividendes bruts (hypothèse)
    imp = autre + 0.6 * div + interets + pv - 0.068 * cap
    ir_b = bareme(imp)
    c_b = cehr(rfr)
    d_b = cdhr(rfr, ir_b + c_b)
    bar_tot = ir_b - base_ir + PS_HAUT * cap + (c_b - cehr(autre)) + d_b
    # PFU à 25 % par la part IR (6,4 %)
    ir_25 = base_ir + 0.064 * cap
    d_25 = cdhr(rfr, ir_25 + c)
    p25 = 0.064 * cap + PS_HAUT * cap + (c - cehr(autre)) + d_25
    p(f"  {nom} : capital {cap:,.0f} € ; impôt sur le capital PFU {pfu_tot:,.0f} ({100 * pfu_tot / cap:.1f} %) ; "
      f"barème {bar_tot:,.0f} ({100 * bar_tot / cap:.1f} %) ; PFU 25 (IR) {p25:,.0f} ({100 * p25 / cap:.1f} %)"
      .replace(",", " "))


cas("Petit épargnant (pension 22 000 €, 800 € de dividendes, 300 € d'intérêts)", 19800, 800, 300, 0)
cas("Cadre (95 000 € nets imposables, 6 000 € de dividendes, 4 000 € de plus-values)", 95000, 6000, 0, 4000)
cas("Rentier (3 M€ de dividendes)", 0, 3e6, 0, 0)
cas("Rentier moyen (400 000 € de dividendes)", 0, 4e5, 0, 0)
p("  petit épargnant : PS sur 60 000 € d'assurance-vie à 2,5 % : 17,2 % -> 18,6 % = "
  f"{0.014 * 1500:.0f} € de plus par an")
# dirigeant de PME : bénéfice 400 000 € avant IS
BEN = 400e3
is_pme = 0.15 * 42500 + 0.25 * (BEN - 42500)
dist = BEN - is_pme
ir = IR_PFU * dist
c = cehr(dist)
d = cdhr(dist, ir + c)
tot_d = is_pme + ir + c + d + PS_HAUT * dist
tot_h = is_pme + QPFC * IS * dist
p(f"  Dirigeant de PME (bénéfice 400 000 €, IS {is_pme:,.0f} €) : tout distribué -> {tot_d:,.0f} € ({100 * tot_d / BEN:.1f} %,"
  f" dont CDHR {d:,.0f}) ; gardé dans la holding -> {tot_h:,.0f} € ({100 * tot_h / BEN:.1f} %)".replace(",", " "))
PVC = 7.5e6
p(f"  Cession (plus-value 7,5 M€) : directe ≥ {PFU * PVC / 1e6:.2f} M€ (31,4 %), {0.354 * PVC / 1e6:.2f} M€ avec CEHR 4 % ;"
  f" apport-cession : 0 à la cession ; à la transmission : 0 (droit actuel) / {PFU * PVC / 1e6:.2f} M€ (art. 5, IR"
  f" {IR_PFU * PVC / 1e6:.2f} M€ étalable sur 5 ans) / 0 tant que les héritiers ne vendent pas (report transmis)")

# ------------------------------------------------------------------ 10. retour au barème : ordre de grandeur statique
p("\n== 10. Retour au barème : ordre de grandeur statique (hypothèses fortes, voir registre) ==")
# dividendes : 96 % au top 1 % supposé au TMI 45 % ; 4 % au TMI 30 % ; intérêts au TMI moyen 30 % ; PV au TMI 45 %
gain = 0.96 * DIV * (0.45 * (0.6 - 0.068) - IR_PFU) + 0.04 * DIV * (0.30 * (0.6 - 0.068) - IR_PFU) \
    + INT * (0.30 * (1 - 0.068) - IR_PFU) + PV * (0.45 * (1 - 0.068) - IR_PFU)
p(f"  gain statique brut ≈ {gain:.1f} Md€ (avant : optants déjà au barème, CDHR perdue 0,4-0,6, foyers aux TMI 41 %)")
for e in (0.65, 0.77, 1.0):
    # taux moyen pondéré avant/après pour la réaction
    t_apres = PFU + gain / B
    r, dq = recette(PFU, t_apres, B, e)
    p(f"  e = {e} : taux moyen {100 * PFU:.1f} -> {100 * t_apres:.1f} % ; recette nette {r:.1f} Md€ (réaction {dq:.1f})")
p(f"  2013 : −40 % de dividendes déclarés -> si l'assiette des dividendes baissait de 40 % : "
  f"{gain - 0.40 * DIV * (PFU + 0.96 * (0.45 * 0.532 - IR_PFU)):.1f} Md€")

OUT.write_text("\n".join(L) + "\n", encoding="utf-8")
print("\n".join(L))
