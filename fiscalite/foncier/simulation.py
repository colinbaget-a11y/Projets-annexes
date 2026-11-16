"""Simulations de la note foncière : moins de droits de mutation, plus de taxe foncière, deux taux terrain/bâti.

Lancer depuis fiscalite/foncier/ après donnees_foncier.py : python3 simulation.py  ->  sorties/simulation.txt

Champ : logements des particuliers (parc du recensement 2022 moins les HLM), France métropolitaine hors
Alsace-Moselle (pas de DVF). Unité : la commune, avec deux types de logements (maison, appartement).

Hypothèses (toutes réglables en tête de fichier) :
- valeur d'un logement = prix médian au m² des ventes 2023-2024 (commune, sinon intercommunalité, sinon
  département) × surface médiane des logements vendus du même type ;
- part du terrain = 1 − coût de reconstruction du bâti / prix au m², bornée entre 10 et 90 % ; le coût de
  reconstruction est calé pour que la part du terrain de l'ensemble égale celle des comptes de patrimoine des
  ménages (Insee, 2024 : 3 993 Md€ de terrains pour 4 807 Md€ de logements) ;
- taxe foncière actuelle d'un logement = (taxe foncière / valeur des logements de la commune, Insee IA 91, 2017)
  × valeur 2024 × facteur national calé sur le total ;
- droits de mutation = taux × valeur des ventes de logements anciens de la commune (moyenne annuelle 2023-2024).
"""
import json
import os
import sys
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
OUT = HERE / "sorties"
OUT.mkdir(exist_ok=True)

LAMBDA_MENAGES = 3993 / (3993 + 4807)        # Insee, comptes de patrimoine 2024, ménages (S14)
LMIN, LMAX = 0.10, 0.90
RATIO_COUT_APPART = 1.25                     # coût de reconstruction au m² habitable : appartement / maison
TAUX_DMTO = 0.045 + 0.012 + 0.0237 * 0.045   # 2024 : département 4,5 %, commune 1,2 %, frais d'assiette de l'État
PART_DEP_DMTO = (0.045 + 0.0237 * 0.045) / TAUX_DMTO
TF_2017_MENAGES = 19.2e9                     # Insee IA 91 : TFPB nette sur les logements et dépendances des ménages
CROISS_COMMUNE = os.environ.get("CROISS_COMMUNE", "1") == "1"   # croissance de la TF par commune
CROISSANCE_TF = None                         # TFPB 2024 / 2017 (REI) : lu dans donnees/croissance_tf.json

c = pd.read_csv(HERE / "donnees/communes.csv.gz", dtype={"codgeo": str, "dep": str, "epci": str}).set_index("codgeo")
c = c[c.log.fillna(0) > 0].copy()

# ---------------------------------------------------------------- parc des particuliers, valeurs
hlm = c.rp_lochlmv.fillna(0)
tot = (c.maison + c.appart).replace(0, np.nan)
c["n_m"] = (c.maison - hlm * c.maison / tot).clip(lower=0).fillna(0)
c["n_a"] = (c.appart - hlm * c.appart / tot).clip(lower=0).fillna(0)
c["v_m"] = c.m_pm2 * c.m_surf
c["v_a"] = c.a_pm2 * c.a_surf

# ---------------------------------------------------------------- part du terrain
# Maisons : mesure directe = prix au m² des terrains à bâtir (commune si au moins 5 ventes, sinon département)
# × surface de parcelle médiane des maisons vendues (plafonnée à PARCELLE_MAX), rapportée au prix de la maison.
# Appartements : résidu (1 − coût de reconstruction / prix au m²), le coût étant calé pour que la part du terrain
# de l'ensemble égale celle des comptes de patrimoine des ménages.
PARCELLE_MAX = 1500.0
# Communes sans assez de ventes de terrains : prix du terrain du département ajusté selon l'écart de prix des
# maisons entre la commune et son département, avec l'élasticité estimée sur les communes qui ont des ventes.
dep_m = (c.m_pm2 * c.n_m).groupby(c.dep).sum() / c.n_m.groupby(c.dep).sum()
x_ = np.log(c.m_pm2 / c.dep.map(dep_m))
y_ = np.log(c.pm2_tab_com / c.pm2_tab_dep)
ok_ = (c.n_tab_com.fillna(0) >= 5) & (c.m_n.fillna(0) >= 10) & x_.notna() & y_.notna()
ELAST_TERRAIN, CONST_TERRAIN = np.polyfit(x_[ok_], y_[ok_], 1)
N_REG_TERRAIN = int(ok_.sum())
pm2_tab = c.pm2_tab_com.where(c.n_tab_com.fillna(0) >= 5,
                              c.pm2_tab_dep * np.exp(CONST_TERRAIN + ELAST_TERRAIN * x_.fillna(0)))
c["l_m"] = (pm2_tab * c.m_terrain.clip(upper=PARCELLE_MAX) / c.v_m).clip(LMIN, LMAX)
c["l_m"] = c.l_m.fillna(c.dep.map(c.groupby("dep").l_m.median())).fillna(c.l_m.median())


def part_agregee(B):
    la = (1 - B / c.a_pm2).clip(LMIN, LMAX)
    V = c.n_m * c.v_m + c.n_a * c.v_a
    return (c.n_m * c.v_m * c.l_m + c.n_a * c.v_a * la).sum() / V.sum()


lo, hi = 100.0, 20000.0
for _ in range(60):
    B = (lo + hi) / 2
    lo, hi = (B, hi) if part_agregee(B) > LAMBDA_MENAGES else (lo, B)
B_APPART = (lo + hi) / 2
c["l_a"] = (1 - B_APPART / c.a_pm2).clip(LMIN, LMAX)


def parts_residu(B):
    """Variante de contrôle : résidu pour les maisons aussi (coût maison = coût appartement / RATIO_COUT_APPART)."""
    return (1 - B / RATIO_COUT_APPART / c.m_pm2).clip(LMIN, LMAX)


# ---------------------------------------------------------------- taxe foncière actuelle par logement
r = c.tf_valeur_2017 / 100
r = r.fillna(c.epci.map(r.groupby(c.epci).median())).fillna(c.dep.map(r.groupby(c.dep).median()))
c["r2017"] = r
cr = json.loads((HERE / "donnees/croissance_tf.json").read_text())
CROISSANCE_TF = cr["tfpb_2024"] / cr["tfpb_2017"]
part_champ = (c.n_m + c.n_a).sum() / cr["logements_metro_particuliers"]
CIBLE_TF = TF_2017_MENAGES * CROISSANCE_TF * part_champ
# croissance propre à chaque commune de la taxe foncière bâtie 2017-2024 (taux et bases, REI), relative à la
# croissance nationale : corrige par exemple la hausse du taux parisien de 13,5 à 20,5 % en 2023. Communes
# fusionnées ou absentes : croissance nationale ; bornée à [0,7 ; 2].
t17 = pd.read_csv(HERE / "donnees/tfpb2017_communes.csv", dtype={"codgeo": str}).set_index("codgeo").tfpb_2017
g = (c.tfpb / c.index.map(t17)) / CROISSANCE_TF
c["g_rel"] = g.where(np.isfinite(g) & (g > 0), 1.0).clip(0.7, 2.0) if CROISS_COMMUNE else 1.0
brut = (c.r2017 * c.g_rel * (c.n_m * c.v_m + c.n_a * c.v_a)).sum()
KAPPA = CIBLE_TF / brut
c["tf_m"], c["tf_a"] = KAPPA * c.r2017 * c.g_rel * c.v_m, KAPPA * c.r2017 * c.g_rel * c.v_a

# ---------------------------------------------------------------- droits de mutation annuels, par logement du parc
c["dmto"] = TAUX_DMTO * c.valeur_ventes_an
c["dmto_m"] = np.where(c.n_m > 0, TAUX_DMTO * c.valeur_ventes_m_an / c.n_m.replace(0, np.nan), 0)
c["dmto_a"] = np.where(c.n_a > 0, TAUX_DMTO * c.valeur_ventes_a_an / c.n_a.replace(0, np.nan), 0)
c[["dmto_m", "dmto_a"]] = c[["dmto_m", "dmto_a"]].fillna(0)

# table longue : une ligne par commune et type de logement
L = pd.concat([pd.DataFrame({"codgeo": c.index, "dep": c.dep, "type": t, "n": c[f"n_{t}"], "v": c[f"v_{t}"],
                             "lam": c[f"l_{t}"], "tf0": c[f"tf_{t}"], "d0": c[f"dmto_{t}"], "pm2": c[f"{t}_pm2"],
                             "pmen": c.pmen, "epci": c.epci}) for t in ("m", "a")], ignore_index=True)
L = L[L.n > 0].reset_index(drop=True)
L["dec_prix"] = pd.qcut(L.pm2.rank(method="first"), 10, labels=False)  # déciles de prix au m² (lignes)
# déciles pondérés par le nombre de logements
o = L.sort_values("pm2")
cum = o.n.cumsum() / o.n.sum()
L.loc[o.index, "dec_prix"] = np.minimum((cum * 10).astype(int), 9)
L["taille"] = pd.cut(L.pmen.fillna(0), [-1, 1000, 5000, 20000, 100000, 1e9],
                     labels=["< 1 000 hab.", "1 000-5 000", "5 000-20 000", "20 000-100 000", "> 100 000"])
TF0, D0 = (L.n * L.tf0).sum(), (L.n * L.d0).sum()
VAL, TERRE = (L.n * L.v).sum(), (L.n * L.v * L.lam).sum()


# ---------------------------------------------------------------- scénarios
def report_tf(s):
    """Baisse des DMTO de s, taxe foncière actuelle relevée du même pourcentage partout."""
    return L.tf0 * (1 + s * D0 / TF0), (1 - s) * L.d0


def valeur_unique(s):
    t = (TF0 + s * D0) / VAL
    return t * L.v, (1 - s) * L.d0


TAUX = {}


def deux_taux(s, k):
    """Taux sur le terrain = k × taux sur le bâti (k = inf : terrain seul), recette nationale constante."""
    base = L.v * (L.lam * (k if np.isfinite(k) else 1.0) + (1 - L.lam) * (1.0 if np.isfinite(k) else 0.0))
    t = (TF0 + s * D0) / (L.n * base).sum()
    TAUX[k] = (t * (k if np.isfinite(k) else 1.0), t if np.isfinite(k) else 0.0)
    return t * base, (1 - s) * L.d0


def deux_taux_local(s, k):
    """Chaque commune garde sa recette de taxe foncière, répartie selon la base à deux taux ; chaque département
    remplace ses droits de mutation perdus (part départementale, communale et frais) par un taux sur la valeur
    des terrains de son territoire."""
    base = L.v * (L.lam * k + (1 - L.lam))
    g = L.assign(b=L.n * base, t0=L.n * L.tf0, terre=L.n * L.v * L.lam, d=L.n * L.d0)
    tc = g.groupby("codgeo").t0.sum() / g.groupby("codgeo").b.sum()
    td = s * g.groupby("dep").d.sum() / g.groupby("dep").terre.sum()
    TAUX[f"dep{k}"] = td
    return L.codgeo.map(tc) * base + L.dep.map(td) * L.v * L.lam, (1 - s) * L.d0


def deux_taux_local_national(s, k, cout=None):
    """Comme deux_taux_local, mais la perte de DMTO est remplacée par un taux national unique sur la valeur des
    terrains (reversé aux départements selon leurs pertes : péréquation) ; cout = perte de recette à compenser."""
    base = L.v * (L.lam * k + (1 - L.lam))
    g = L.assign(b=L.n * base, t0=L.n * L.tf0)
    tc = g.groupby("codgeo").t0.sum() / g.groupby("codgeo").b.sum()
    perte = s * D0 if cout is None else cout
    tn = perte / TERRE
    TAUX[f"nat{k}"] = tn
    return L.codgeo.map(tc) * base + tn * L.v * L.lam, (1 - s) * L.d0


def resume(nom, tf1, d1, p):
    dtf = tf1 - L.tf0
    dtot = dtf + (d1 - L.d0)
    n = L.n
    rec = ((n * tf1).sum() + (n * d1).sum()) / 1e9
    perd = n[dtf > 300].sum() / n.sum()
    perd50 = n[dtf > 0.5 * L.tf0].sum() / n.sum()
    gagne = n[dtf < -100].sum() / n.sum()
    perd100 = n[dtf > L.tf0].sum() / n.sum()
    p(f"{nom} : recette TF + DMTO {rec:.1f} Md€ (avant {(TF0 + D0)/1e9:.1f}) ; TF {(n*tf1).sum()/1e9:.1f} ;"
      f" logements dont la TF augmente de plus de 300 € {100*perd:.0f} %, de plus de 50 % {100*perd50:.0f} %,"
      f" de plus de 100 % {100*perd100:.1f} % ;"
      f" baisse de plus de 100 € {100*gagne:.0f} %")
    for cle, lab in (("dec_prix", "décile de prix au m²"), ("type", "type"), ("taille", "taille de commune")):
        g = L.assign(w=n, a=n * dtf, b=n * dtot, t0=n * L.tf0).groupby(cle, observed=True)
        t = pd.DataFrame({"dTF €": g.a.sum() / g.w.sum(), "dTF %": 100 * g.a.sum() / g.t0.sum(),
                          "dTF+DMTO €": g.b.sum() / g.w.sum()}).round(0)
        p(f"  par {lab} : " + " ; ".join(f"{i} {r['dTF €']:+.0f} € ({r['dTF %']:+.0f} %), total {r['dTF+DMTO €']:+.0f} €"
                                         for i, r in t.iterrows()))
    return dtf, dtot


CAS = [("75056", "a", "Paris, appartement"), ("69123", "a", "Lyon, appartement"), ("33063", "a", "Bordeaux, appartement"),
       ("74010", "m", "Annecy, maison"), ("44109", "m", "Nantes, maison"), ("87085", "m", "Limoges, maison"),
       ("42218", "a", "Saint-Étienne, appartement"), ("19272", "m", "Ussel (Corrèze), maison"),
       ("23096", "m", "Guéret (Creuse), maison"), ("33009", "m", "Arcachon, maison")]


def cas_types(scen, p):
    for code, t, lab in CAS:
        i = L[(L.codgeo == code) & (L.type == t)].index
        if len(i) == 0:
            p(f"  {lab} : absent")
            continue
        i = i[0]
        dm = TAUX_DMTO * L.v[i]
        txt = []
        for nom, (tf1, d1) in scen.items():
            dtf = tf1[i] - L.tf0[i]
            eco = dm * (1 - d1[i] / L.d0[i]) if L.d0[i] > 0 else 0
            txt.append(f"{nom} TF {tf1[i]:,.0f} € ({dtf:+,.0f}), DMTO à l'achat −{eco:,.0f} €"
                       + (f", amorti en {eco/dtf:.0f} ans" if dtf > 0 else ""))
        p(f"  {lab} : valeur {L.v[i]:,.0f} €, terrain {100*L.lam[i]:.0f} %, TF {L.tf0[i]:,.0f} €, DMTO à l'achat {dm:,.0f} € | "
          + " | ".join(txt))


R_ACT = 0.03                                 # taux d'actualisation réel
# Réaction des volumes de ventes (revue droits_mutation.md) : +6 % de ventes par point de baisse du taux
# (fourchette 0 à +8 %), appliquée de façon multiplicative ; elle réduit le coût de la baisse des droits.
VOL_PAR_POINT = 0.06


def cout_baisse(s, vol=VOL_PAR_POINT):
    """Perte de recette de DMTO pour une baisse de s du taux, avec réaction des volumes (Md€)."""
    dpts = 100 * s * TAUX_DMTO
    return D0 * (1 - (1 - s) * (1 + vol) ** dpts) / 1e9, dpts


def primo(scen, p, horizons=(7, 15)):
    """Jeune ménage qui achète le logement médian de la commune : économie de DMTO à l'achat, hausse annuelle
    de taxe foncière, bilan actualisé s'il revend après H ans ; propriétaire installé : hausse perpétuelle."""
    rows = []
    for code, t, lab in CAS:
        i = L[(L.codgeo == code) & (L.type == t)].index
        if len(i) == 0:
            continue
        i = i[0]
        for nom, (tf1, d1) in scen.items():
            eco = TAUX_DMTO * L.v[i] * (1 - d1[i] / L.d0[i]) if L.d0[i] > 0 else 0.0
            dt = tf1[i] - L.tf0[i]
            va = {h: dt * (1 - (1 + R_ACT) ** -h) / R_ACT for h in horizons}
            rows.append(dict(cas=lab, scen=nom, valeur=L.v[i], dmto=TAUX_DMTO * L.v[i], eco=eco, dtf=dt,
                             **{f"net{h}": eco - va[h] for h in horizons}, installe=-dt / R_ACT))
    df = pd.DataFrame(rows)
    for _, r in df.iterrows():
        p(f"  {r.cas} [{r.scen}] : économie à l'achat {r.eco:,.0f} € ; TF {r.dtf:+,.0f} €/an ; gain net s'il revend après "
          + ", après ".join(f"{h} ans {r[f'net{h}']:+,.0f} €" for h in horizons)
          + f" ; propriétaire installé (valeur actuelle de la hausse) {r.installe:+,.0f} €")
    return df


if __name__ == "__main__":
    lignes = []

    def p(s):
        print(s, flush=True)
        lignes.append(s)
    p(f"champ : {L.n.sum()/1e6:.1f} M logements de particuliers, valeur {VAL/1e9:,.0f} Md€, terrain {TERRE/1e9:,.0f} Md€"
      f" ({100*TERRE/VAL:.1f} %) ; coût de reconstruction calé pour les appartements {B_APPART:,.0f} €/m²")
    p(f"taxe foncière des particuliers {TF0/1e9:.1f} Md€ (croissance TFPB 2017-2024 {CROISSANCE_TF:.3f}, part du champ"
      f" {part_champ:.3f}) ; DMTO sur les logements anciens {D0/1e9:.1f} Md€ (taux {100*TAUX_DMTO:.2f} %) ;"
      f" TF moyenne {TF0/L.n.sum():,.0f} € par logement ; TF / valeur {100*TF0/VAL:.3f} %")
    lm = (L.n * L.v * L.lam).groupby(L.type).sum() / (L.n * L.v).groupby(L.type).sum()
    p(f"prix des terrains imputé : élasticité au prix des maisons {ELAST_TERRAIN:.2f} (constante {CONST_TERRAIN:.2f},"
      f" {N_REG_TERRAIN} communes)")
    p("part du terrain par type : " + str(lm.round(3).to_dict()) + " ; par décile de prix : " + " ".join(
        f"{100*u:.0f}" for u in ((L.n * L.v * L.lam).groupby(L.dec_prix).sum() / (L.n * L.v).groupby(L.dec_prix).sum())))
    # validation : méthode des terrains à bâtir (maisons, par département)
    td = pd.read_csv(HERE / "donnees/terrains_dep.csv", dtype={"dep": str}).set_index("dep")
    lt = (td.pm2_tab * td.m_terrain / (td.m_pm2 * td.m_surf)).rename("tab")
    lr_ = parts_residu(B_APPART)
    lr = (c.n_m * c.v_m * lr_).groupby(c.dep).sum() / (c.n_m * c.v_m).groupby(c.dep).sum()
    j = pd.concat([lt, lr.rename("resid")], axis=1).dropna()
    p(f"contrôle maisons par département : part du terrain par résidu {100*j.resid.median():.0f} % (médiane), par prix"
      f" des terrains à bâtir {100*j.tab.median():.0f} % ; corrélation {j.corr().iloc[0,1]:.2f}")
    scen = {}
    for s in (0.3, 0.5):
        scen[f"R{int(100*s)}"] = report_tf(s)
        resume(f"[report sur la TF actuelle, DMTO −{int(100*s)} %]", *scen[f"R{int(100*s)}"], p)
    s = 0.5
    scen["V50"] = valeur_unique(s)
    resume("[valeur vénale, taux unique national, DMTO −50 %]", *scen["V50"], p)
    for k in (2, 4, np.inf):
        nom = f"K{k}" if np.isfinite(k) else "Kinf"
        scen[nom] = deux_taux(s, k)
        resume(f"[deux taux nationaux, terrain = {k} × bâti, DMTO −50 %]", *scen[nom], p)
    for k in (2, 4):
        scen[f"L{k}"] = deux_taux_local(s, k)
        resume(f"[deux taux, recette constante par commune, terrain = {k} × bâti ; DMTO −50 % remplacés par un taux"
               f" départemental sur le terrain]", *scen[f"L{k}"], p)
    for k in (2, 4, np.inf):
        tl, tb = TAUX[k]
        p(f"taux nationaux (terrain = {k} × bâti) : terrain {100*tl:.3f} %, bâti {100*tb:.3f} % de la valeur")
    td = TAUX["dep4"]
    p(f"taux départemental sur le terrain qui remplace 50 % des DMTO : médiane {100*td.median():.3f} %, de {100*td.min():.3f}"
      f" à {100*td.max():.3f} % ; Paris {100*td.get('75', np.nan):.3f} %, Creuse {100*td.get('23', np.nan):.3f} %")
    w = L.n * L.v
    for nom in ("R50", "K4", "L4"):
        tf1 = scen[nom][0]
        rr = (L.n * tf1).groupby(L.dec_prix).sum() / w.groupby(L.dec_prix).sum()
        p(f"TF / valeur par décile de prix, {nom} : " + " ".join(f"{100*u:.2f}" for u in rr))
    rr = (L.n * L.tf0).groupby(L.dec_prix).sum() / w.groupby(L.dec_prix).sum()
    p("TF / valeur par décile de prix, aujourd'hui : " + " ".join(f"{100*u:.2f}" for u in rr))
    p("prix au m² médian par décile : " + " ".join(f"{u:,.0f}" for u in L.groupby("dec_prix").pm2.median()))
    for s_ in (0.3, 0.5):
        for vol in (0.0, 0.03, VOL_PAR_POINT, 0.08):
            c_, dp = cout_baisse(s_, vol)
            p(f"baisse des DMTO de {int(100*s_)} % ({dp:.1f} points) : perte de recette {c_:.1f} Md€ avec +{100*vol:.0f} % de"
              f" ventes par point ; hausse de TF nécessaire {100*c_*1e9/TF0:.0f} %")
    scen["N4"] = deux_taux_local_national(0.5, 4)
    taux_n4 = TAUX["nat4"]
    resume("[deux taux, recette constante par commune, terrain = 4 × bâti ; DMTO −50 % remplacés par un taux national"
           " unique sur le terrain]", *scen["N4"], p)
    c_vol, _ = cout_baisse(0.5)
    tf_v, d_v = deux_taux_local_national(0.5, 4, cout=c_vol * 1e9)
    # droits payés sur les ventes supplémentaires (correction signalée par revue/verif_foncier.md)
    scen["N4v"] = (tf_v, d_v * (1 + VOL_PAR_POINT) ** (100 * 0.5 * TAUX_DMTO))
    resume(f"[idem, avec réaction des volumes : perte à compenser {c_vol:.1f} Md€]", *scen["N4v"], p)
    p(f"taux national sur le terrain : {100*taux_n4:.3f} % de la valeur des terrains sans réaction des ventes,"
      f" {100*TAUX['nat4']:.3f} % avec")
    w = L.n * L.v
    rr = (L.n * scen["N4"][0]).groupby(L.dec_prix).sum() / w.groupby(L.dec_prix).sum()
    p("TF / valeur par décile de prix, N4 : " + " ".join(f"{100*u:.2f}" for u in rr))
    # contrôles demandés par la revue (revue/revue_foncier.md)
    base4 = L.v * (L.lam * 4 + (1 - L.lam))
    g4 = L.assign(b=L.n * base4, t0=L.n * L.tf0)
    tc4 = L.codgeo.map(g4.groupby("codgeo").t0.sum() / g4.groupby("codgeo").b.sum())
    bati_av = (L.n * L.tf0 * (1 - L.lam)).sum() / 1e9
    bati_ap = (L.n * tc4 * L.v * (1 - L.lam)).sum() / 1e9
    p(f"[CONTROLE] part de la TF portant sur le bâti (TF actuelle répartie selon la valeur) : {bati_av:.1f} Md€ ;"
      f" après la proposition : {bati_ap:.1f} Md€")
    dtf = scen["N4"][0] - L.tf0
    paris = (L.codgeo == "75056") & (L.type == "a")
    p(f"[CONTROLE] Paris, appartement médian : TF {float(L.tf0[paris].iloc[0]):,.0f} € -> "
      f"{float(scen['N4'][0][paris].iloc[0]):,.0f} € ; hausse capitalisée à {100*R_ACT:.0f} % : "
      f"{float(dtf[paris].iloc[0])/R_ACT:,.0f} € ; nette de la baisse annuelle moyenne des DMTO du parc : "
      f"{float((dtf + scen['N4'][1] - L.d0)[paris].iloc[0])/R_ACT:,.0f} €")
    # variante : part du terrain des maisons par résidu, coût de reconstruction recalé sur 45 % au total
    lam0 = L.lam.copy()
    def part_tot(B):
        lm_ = (1 - B / RATIO_COUT_APPART / L.pm2).clip(LMIN, LMAX)
        la_ = (1 - B / L.pm2).clip(LMIN, LMAX)
        lam_ = np.where(L.type == "m", lm_, la_)
        return lam_, (L.n * L.v * lam_).sum() / (L.n * L.v).sum()
    lo, hi = 100.0, 6000.0
    for _ in range(40):
        Bv = (lo + hi) / 2
        lo, hi = (Bv, hi) if part_tot(Bv)[1] > LAMBDA_MENAGES else (lo, Bv)
    L["lam"] = part_tot(Bv)[0]
    TERRE_SAUVE = TERRE
    globals()["TERRE"] = (L.n * L.v * L.lam).sum()
    tfv, dv = deux_taux_local_national(0.5, 4)
    resume(f"[VARIANTE résidu pour les maisons aussi (coût recalé {Bv:,.0f} €/m²) : proposition]", tfv, dv, p)
    L["lam"] = lam0
    globals()["TERRE"] = TERRE_SAUVE
    p("cas-types (un logement médian de la commune) :")
    cas_types({k: scen[k] for k in ("R50", "K4", "N4")}, p)
    p(f"primo-accédant (taux d'actualisation {100*R_ACT:.0f} %) :")
    primo({k: scen[k] for k in ("R50", "N4")}, p).round(0).to_csv(OUT / "primo.csv", index=False)
    (OUT / "simulation.txt").write_text("\n".join(lignes) + "\n", encoding="utf-8")
