"""Bloc « fiscalité du capital », révision v3 (CONSIGNES_V3.md, section Capital) : neutralité entre « vendre puis
transmettre » et « transmettre puis l'héritier vend ».

Reprend note8p/calculs/pfu_transmission.py (v2) sans le modifier : barème des droits, jeux d'hypothèses bas / central /
haut et profil des ventes sont recopiés à l'identique. Ce qui est nouveau :
  1. comparaison de règles de correction (i) taux moyen des droits ajouté au prix (v2, règle américaine § 1015(d)(6)) ;
     (ii) même correction au taux marginal ; (iii) impôt latent déduit de l'assiette des droits ; (iv) crédit à la vente
     des droits afférents à l'impôt latent (« correction à la marge », double calcul des droits) ; (v) majoration
     forfaitaire de 30 % de la plus-value ; (vi) réalisation au décès avec déduction (type Canada), pour mémoire ;
  2. cas-types : exemple 100 k€ -> 1 M€, petite plus-value, très grande plus-value, neveu, conjoint, pacte Dutreil ;
  3. profils de recettes 2027-2040 par règle ; scénario prudent de la règle recommandée.
Parcimonie (CONSIGNES_V3, ajout du 18/11/2026) : aucun modèle de migration ; la prudence sur les très grands patrimoines
est un scénario simple (jeu bas, encaissé avec deux ans de décalage), pas une élasticité appliquée.

Lancer depuis fiscalite/ : python3 note8p/calculs/pfu3_neutralite.py
Sorties : note8p/sorties/pfu3.json, pfu3_calculs.txt ; figure note8p/figures/g9_exemple_pv.{pdf,png}.
Conventions : Md€ au niveau du PIB de 2025, sans croissance ; + = recette en plus par rapport au droit de 2026.
"""
import json
import sys
from pathlib import Path

RACINE = Path(__file__).resolve().parents[2]
N8 = RACINE / "note8p"
L, J = [], {}
p = L.append


def fr(x, d=0):
    return f"{x:,.{d}f}".replace(",", " ").replace(".", ",").replace("-", "−")


# ---------------------------------------------------------------------------------------------------------------------
# 0. Droit de 2026 (identique à pfu_transmission.py)
# ---------------------------------------------------------------------------------------------------------------------
IR_PFU, PS = 0.128, 0.186
T = IR_PFU + PS                                       # PFU 31,4 % [V]
BAREMES = {                                           # CGI art. 777, 779, 788 [V/S, service-public F35794]
    "ligne directe": ([(8072, .05), (12109, .10), (15932, .15), (552324, .20), (902838, .30), (1805677, .40),
                       (float("inf"), .45)], 100_000),
    "frère ou sœur": ([(24430, .35), (float("inf"), .45)], 15_932),
    "neveu": ([(float("inf"), .55)], 7_967),
    "conjoint": ([(float("inf"), 0.0)], 0),           # exonéré (art. 796-0 bis)
}


def droits(part, lien="ligne directe", dutreil=False):
    """Droits d'un bénéficiaire sur sa part. Dutreil (art. 787 B) : 75 % de la valeur des titres exonérée."""
    bar, ab = BAREMES[lien]
    x = (0.25 * part if dutreil else part) - ab
    d, bas = 0.0, 0.0
    for haut, t in bar:
        if x > bas:
            d += (min(x, haut) - bas) * t
        bas = haut
    return max(d, 0.0)


def marg(part, lien="ligne directe", dutreil=False, h=1.0):
    return (droits(part + h, lien, dutreil) - droits(part, lien, dutreil)) / h


# ---------------------------------------------------------------------------------------------------------------------
# 1. Règles de correction et cas-types
# ---------------------------------------------------------------------------------------------------------------------
REGLES = {
    "i": "(i) droits au taux moyen ajoutés au prix (v2, § 1015(d)(6))",
    "ii": "(ii) même correction au taux marginal des droits",
    "iii": "(iii) impôt latent déduit de l'assiette des droits",
    "iv": "(iv) crédit à la vente des droits afférents à l'impôt latent",
    "v": "(v) prix majoré forfaitairement de 30 % de la plus-value",
    "vi": "(vi) réalisation au décès, impôt déduit des droits (pour mémoire)",
}
FORFAIT = 0.30


def cas(V, B, n=1, lien="ligne directe", dutreil=False):
    """Charge totale (tous bénéficiaires), en €. A : le parent vend puis transmet le produit (pas de Dutreil sur des
    liquidités). B : il transmet, chaque héritier vend sa part. 'garde' : charge si l'héritier ne vend jamais."""
    G = V - B
    v, g = V / n, G / n                               # part de chaque héritier
    tg = T * g
    dA = droits(v - tg, lien)                         # parent qui vend : droits sur le produit net, sans Dutreil
    dB = droits(v, lien, dutreil)
    dB_net = droits(v - tg, lien, dutreil)            # droits recalculés sur la part diminuée de l'impôt latent
    m = marg(v, lien, dutreil)
    out = {"A_vend_puis_transmet": n * (T * g + dA), "aujourdhui": n * dB, "sans_correction": n * (dB + tg)}
    adj = {"i": dB * g / v, "ii": m * g, "v": FORFAIT * g}
    for k, a in adj.items():
        out[k] = n * (dB + T * max(g - a, 0.0))
    out["iii"] = n * (dB_net + tg)
    out["iv"] = n * (dB + tg - (dB - dB_net))
    out["vi"] = out["iii"]
    garde = {"aujourdhui": n * dB, "i": n * dB, "ii": n * dB, "iv": n * dB, "v": n * dB, "iii": n * dB_net,
             "vi": n * (tg + dB_net)}
    return dict(V=V, B=B, n=n, lien=lien, dutreil=dutreil, charges=out, garde=garde, tmoy=dB / v if v else 0,
                tmarg=m, ecart={k: out[k] - out["A_vend_puis_transmet"] for k in out})


CAS = {
    "exemple": ("Exemple : 100 k€ devenus 1 M€, un enfant", cas(1e6, 1e5)),
    "petite": ("Petite plus-value : 250 k€ devenus 400 k€, un enfant", cas(4e5, 2.5e5)),
    "tres_grande": ("Très grande : 2 M€ devenus 40 M€, deux enfants", cas(4e7, 2e6, n=2)),
    "neveu": ("Autre lien : 100 k€ devenus 1 M€, un neveu", cas(1e6, 1e5, lien="neveu")),
    "frere": ("Autre lien : 100 k€ devenus 1 M€, un frère", cas(1e6, 1e5, lien="frère ou sœur")),
    "conjoint": ("Conjoint : 100 k€ devenus 1 M€ (exonéré)", cas(1e6, 1e5, lien="conjoint")),
    "dutreil_ex": ("Pacte Dutreil : 100 k€ devenus 1 M€, un enfant", cas(1e6, 1e5, dutreil=True)),
    "dutreil_pme": ("Pacte Dutreil : entreprise de 10 M€ (prix 0,5 M€), deux enfants", cas(1e7, 5e5, n=2, dutreil=True)),
}
p("=" * 110)
p("BLOC CAPITAL v3 — neutralité vendre/transmettre (note8p/calculs/pfu3_neutralite.py)")
p("=" * 110)
p("1. Charge totale (impôt sur la plus-value + droits), € ; écart B − A (transmettre puis vendre − vendre puis transmettre)")
for k, (lib, c) in CAS.items():
    p(f"\n   {lib} — taux moyen des droits {fr(100 * c['tmoy'], 1)} %, marginal {fr(100 * c['tmarg'], 1)} %")
    ch, A = c["charges"], c["charges"]["A_vend_puis_transmet"]
    p(f"     A vendre puis transmettre : {fr(A)} ({fr(100 * A / c['V'], 1)} %)")
    for r in ["aujourdhui", "sans_correction", "i", "ii", "iii", "iv", "v", "vi"]:
        nom = REGLES.get(r, r)
        p(f"     {nom:68s} {fr(ch[r]):>12s}  écart {fr(ch[r] - A):>11s} ({fr(100 * (ch[r] - A) / A, 1):>6s} %)"
          + (f" ; s'il ne vend jamais : {fr(c['garde'][r])}" if r in c["garde"] else ""))
J["cas"] = {k: dict(libelle=lib, **c) for k, (lib, c) in CAS.items()}

# Rapport taux marginal / taux moyen dans les cas-types en ligne directe (sert à calibrer m à partir de tau)
rat = {k: CAS[k][1]["tmarg"] / CAS[k][1]["tmoy"] for k in ("exemple", "petite", "tres_grande", "dutreil_ex", "dutreil_pme")}
p("\n   rapport taux marginal / taux moyen des droits : " + " ; ".join(f"{k} {fr(v, 2)}" for k, v in rat.items()))
J["rapport_marginal_moyen"] = rat

# ---------------------------------------------------------------------------------------------------------------------
# 2. Recettes 2027-2040 par règle (méthode et jeux de pfu_transmission.py ; tau = taux moyen [H] ; m = 1,4 tau [H])
# ---------------------------------------------------------------------------------------------------------------------
STOCK_C = 127.0 / 152.869 * 173.268
JEUX = {
    "bas": dict(E=1200, b=0.017, lam=0.40, a=0.15, h=0.02, S=127.0, T=35, tau=0.15),
    "central": dict(E=1450, b=0.023, lam=0.55, a=0.30, h=0.04, S=STOCK_C, T=25, tau=0.10),
    "haut": dict(E=1700, b=0.030, lam=0.70, a=0.45, h=0.06, S=173.268, T=15, tau=0.05),
}
K_MARG = 1.4          # [H] m = 1,4 τ : rapport observé dans les cas-types en ligne directe (1,2 à 1,6), plafonné à 45 %
T_REP, A_REP = 0.30, 0.10
ANS = list(range(2027, 2041))


def profil(a, h, n=40):
    v = [0.0] * (n + 2)
    v[0] += a / 2
    v[1] += a / 2
    for k in range(2, n + 1):
        v[k - 1] += (1 - a) * h * (1 - h) ** (k - 2)
    return v


def recette(Lc, a, h):
    pv = profil(a, h)
    return {y: sum(Lc * pv[(y - 1) - c] for c in range(2027, y) if 0 <= (y - 1) - c < len(pv)) for y in ANS}


REC = {}
for nom, q in JEUX.items():
    Lpv = T * q["E"] * q["b"] * q["lam"]
    Lrep = T_REP * q["S"] / q["T"]
    m = min(K_MARG * q["tau"], 0.45)
    brut = {y: recette(Lpv, q["a"], q["h"])[y] + recette(Lrep, A_REP, q["h"])[y] for y in ANS}
    perte_droits = m * (Lpv + Lrep)               # (iii) : droits réduits dès la transmission, chaque année
    R = {
        "sans_correction": brut,
        "i": {y: brut[y] * (1 - q["tau"]) for y in ANS},
        "ii": {y: brut[y] * (1 - m) for y in ANS},
        "iv": {y: brut[y] * (1 - m) for y in ANS},
        "v": {y: brut[y] * (1 - FORFAIT) for y in ANS},
        "iii": {y: brut[y] - perte_droits for y in ANS},
        "vi": {y: (0.0 if y == 2027 else (Lpv + Lrep) * (1 - m)) for y in ANS},   # IR payé en N+1 de la transmission
    }
    REC[nom] = dict(m=m, L_brut=Lpv + Lrep, perte_droits_iii=perte_droits, R=R)
# Scénario prudent de la règle recommandée (iv) : jeu bas, encaissé deux ans plus tard (recette constatée en N+1,
# réutilisée en N+2) — aucune élasticité de départ appliquée (pas de modèle de migration, CONSIGNES_V3).
PRUD = {y: (REC["bas"]["R"]["iv"][y - 2] if y - 2 >= 2027 else 0.0) for y in ANS}

p("\n2. Recettes par règle, Md€ (impôt encaissé l'année qui suit la vente) [S sur hypothèses H]")
for nom, e in REC.items():
    p(f"   jeu {nom} : impôt latent transmis par an {fr(e['L_brut'], 2)} ; τ = {fr(100 * JEUX[nom]['tau'])} % ; "
      f"m = {fr(100 * e['m'])} % ; (iii) perte de droits {fr(e['perte_droits_iii'], 2)} par an dès 2027")
p("   année      " + " ".join(f"{y:>5d}" for y in ANS) + "   cumul")
for nom in ("central", "bas", "haut"):
    for r in ("sans_correction", "i", "iv", "v", "iii", "vi"):
        s = REC[nom]["R"][r]
        p(f"   {nom[:4]} {r:15s}" + " ".join(f"{s[y]:5.2f}" for y in ANS) + f"  {sum(s.values()):6.1f}")
p("   prudent (iv)        " + " ".join(f"{PRUD[y]:5.2f}" for y in ANS) + f"  {sum(PRUD.values()):6.1f}")
cout_iv_vs_i = {nom: sum(REC[nom]["R"]["i"].values()) - sum(REC[nom]["R"]["iv"].values()) for nom in REC}
p("   coût cumulé 2027-2040 de (iv) par rapport à (i) : " + " ; ".join(f"{k} {fr(v, 1)}" for k, v in cout_iv_vs_i.items()))
p("   coût annuel en régime de croisière de (iv) par rapport à (i) : " + " ; ".join(
    f"{k} {fr(e['L_brut'] * (e['m'] - JEUX[k]['tau']), 2)}" for k, e in REC.items()))

J["recettes"] = {nom: dict(m=e["m"], tau=JEUX[nom]["tau"], impot_latent_brut=e["L_brut"],
                           perte_droits_iii=e["perte_droits_iii"],
                           par_regle={r: {str(y): round(v, 3) for y, v in s.items()} for r, s in e["R"].items()},
                           cumul={r: round(sum(s.values()), 2) for r, s in e["R"].items()})
                 for nom, e in REC.items()}
J["cout_iv_par_rapport_a_i_cumul"] = cout_iv_vs_i

# ---------------------------------------------------------------------------------------------------------------------
# 3. Table annuelle pour le bouclage
# ---------------------------------------------------------------------------------------------------------------------
J["regle_recommandee"] = ("(iv) correction à la marge : prix repris = prix historique + (droits payés − droits recalculés "
                          "sur la part diminuée de l'impôt latent) / PFU ; équivalent à un crédit à la vente")
J["annuel"] = {str(y): {
    "fin_effacement_central": round(REC["central"]["R"]["iv"][y], 3),
    "fin_effacement_bas": round(REC["bas"]["R"]["iv"][y], 3),
    "fin_effacement_haut": round(REC["haut"]["R"]["iv"][y], 3),
    "fin_effacement_prudent": round(PRUD[y], 3),
    "regle_v2_taux_moyen_central": round(REC["central"]["R"]["i"][y], 3),
    "taux_pfu_inchange": 0.0,
    "cehr_cdhr_capital_maintenues": 0.0,
} for y in ANS}
J["unites"] = ("Md€ au niveau du PIB 2025 (pas de croissance) ; + = recette en plus par rapport au droit de 2026. "
               "Les lignes fin_effacement ne se réutilisent qu'une fois constatées ; pour le bouclage, ligne prudente.")
(N8 / "sorties" / "pfu3.json").write_text(json.dumps(J, ensure_ascii=False, indent=1, default=float), encoding="utf-8")
(N8 / "sorties" / "pfu3_calculs.txt").write_text("\n".join(L) + "\n", encoding="utf-8")
print("\n".join(L))

# ---------------------------------------------------------------------------------------------------------------------
# 4. Figure g9 (charte.py)
# ---------------------------------------------------------------------------------------------------------------------
if "--sans-figure" not in sys.argv:
    sys.path.insert(0, str(N8))
    from charte import plt, axes, sauver, AUJ, NAIF, PROP, HAUSSE, ENCRE, PLEINE, _fr  # noqa: E402
    from matplotlib.patches import Patch
    from matplotlib.ticker import FuncFormatter
    c = CAS["exemple"][1]
    V, B, G = c["V"], c["B"], c["V"] - c["B"]
    d_full, d_net = droits(V), droits(V - T * G)
    barres = [  # (libellé, droits, impôt PV, couleur PV)
        ("Elle vend, puis transmet\nle produit de la vente", d_net, T * G, PROP),
        ("Elle garde ses titres jusqu'au\ndécès : aujourd'hui", d_full, 0.0, PROP),
        ("Elle garde ses titres jusqu'au\ndécès : avec la réforme", d_full, c["charges"]["iv"] - d_full, HAUSSE),
    ]
    fig, ax = plt.subplots(figsize=(PLEINE, 2.1))
    axes(ax, grille="x")
    for i, (lab, d, pv, col) in enumerate(barres):
        y = len(barres) - 1 - i
        ax.barh(y, d / 1e3, color=AUJ, height=0.58, zorder=2)
        ax.barh(y, pv / 1e3, left=d / 1e3, color=col, height=0.58, zorder=2)
        ax.text((d + pv) / 1e3 + 6, y, f"{_fr((d + pv) / 1e3)} k€", va="center", fontsize=7.5, color=ENCRE)
    ax.set_yticks(range(len(barres)))
    ax.set_yticklabels([b[0] for b in barres][::-1])
    ax.set_xlim(0, 500)
    ax.xaxis.set_major_formatter(FuncFormatter(lambda v, _: _fr(v) + " k€"))
    ax.tick_params(axis="y", length=0)
    ax.legend(handles=[Patch(color=AUJ, label="Droits de succession"),
                       Patch(color=PROP, label="Impôt sur la plus-value payé par la fondatrice"),
                       Patch(color=HAUSSE, label="Impôt sur la plus-value payé par l'héritier qui revend")],
              loc="lower center", bbox_to_anchor=(0.42, 1.0), ncol=3, fontsize=6.8, handlelength=1.1, columnspacing=1.0)
    sauver(fig, "g9_exemple_pv",
           "calculs des auteurs (note8p/calculs/pfu3_neutralite.py), droit de 2026 : PFU de 31,4 %, barème des droits "
           "en ligne directe après abattement de 100 000 €.",
           f"Titres acquis 100 000 €, valant 1 000 000 €, un seul enfant ; hors CEHR et CDHR. Correction à la marge : "
           f"le prix repris est majoré des droits afférents à l'impôt latent ({_fr(d_full - d_net)} € de droits, "
           f"soit {_fr((d_full - d_net) / T)} € ajoutés au prix).")
