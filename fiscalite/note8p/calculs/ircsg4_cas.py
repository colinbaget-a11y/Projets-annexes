"""Bloc IR-CSG v4 : cas-types nets des niches, Julie, second conjoint, minimum vieillesse (ASPA). Lancer après
ircsg4_modele.py et ircsg4_openfisca.py (python3.13) :  python3 note8p/calculs/ircsg4_cas.py
Complète note8p/sorties/ircsg4.json (cas_types_nets, julie, aspa) et écrit note8p/sorties/tab_cas_types.tex.

Conventions : barème final v4 (clé bareme de ircsg4.json) ; franchise de 6 000 € par enfant chez le parent qui gagne le
plus ; aucun frais réel déclaré (trajet court ou en transports en commun) [H] ; gain du nouveau système = nouvel impôt −
charge d'aujourd'hui sans niche ; perte des niches = valeur des niches supprimées (crédits restitués compris) ; net =
nouvel impôt − charge d'aujourd'hui avec niches. Les engagements Pinel en cours sont gardés (réduction imputée avant et
après), donc sans effet sur le net.
"""
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import ircsg3_modele as N  # noqa: E402

OUT = N.SORTIES
J = json.loads((OUT / "ircsg4.json").read_text(encoding="utf-8"))
S = N.continu(J["bareme"]["points"], J["bareme"]["taux"])
O = N.options()
CAS = pd.read_csv(OUT / "ircsg4_of_cas.csv")
L = []


def p(s):
    print(s, flush=True)
    L.append(s)


def nouveau(r):
    zs = [float(b) for b in str(r.bases).split(";")]
    return float(N.impot_z(S, O, zs, int(r.enfants))[0]) - float(r.pinel_garde)


NETS = {}
for r in CAS.itertuples():
    nv = nouveau(r)
    gain = nv - (r.charge_sans - r.pinel_garde)
    perte = (r.charge_sans - r.pinel_garde) - r.charge_avec
    NETS[r.cle] = dict(libelle=r.libelle, aujourdhui_avec_niches=r.charge_avec, aujourdhui_sans_niches=r.charge_sans - r.pinel_garde,
                       nouvel_impot=nv, gain_systeme=gain, perte_niches=perte, net=nv - r.charge_avec,
                       gain_systeme_mois=gain / 12, perte_niches_mois=perte / 12, net_mois=(nv - r.charge_avec) / 12,
                       credits_restitues=max(-r.ir_avec, 0.0))
    p(f"{r.cle:12s} {r.libelle[:70]:70s} aujourd'hui {r.charge_avec:8,.0f} (sans niche {r.charge_sans:8,.0f}) → {nv:8,.0f} :"
      f" système {gain:+7,.0f}, niches {perte:+7,.0f}, net {nv - r.charge_avec:+7,.0f} €/an ({(nv - r.charge_avec) / 12:+5.0f}/mois)")

# Julie : ce qu'elle garde de 200 € de salaire net en plus
a, b = CAS[CAS.cle == "julie"].iloc[0], CAS[CAS.cle == "julie_200"].iloc[0]
dz = float(b.bases) - float(a.bases)
garde_auj = 200.0 - ((b.ir_avec - a.ir_avec) / 12)
garde_dem = (dz - (nouveau(b) - nouveau(a))) / 12
JULIE = dict(brut_avant=float(a.bruts), brut_apres=float(b.bruts), hausse_revenu_apres_cotisations_mois=dz / 12,
             garde_aujourdhui_mois=garde_auj, garde_demain_mois=garde_dem,
             taux_prelevement_aujourdhui=100 * (1 - garde_auj / (dz / 12)), taux_prelevement_demain=100 * (1 - garde_dem / (dz / 12)),
             net_avant_ir_aujourdhui=float(a.bases) - float(a.csg_crds), impot_nouveau_avant=nouveau(a))
p(f"[JULIE] +200 € de salaire net par mois (+{dz / 12:.0f} € après cotisations) : elle garde aujourd'hui {garde_auj:.0f} €,"
  f" demain {garde_dem:.0f} € (prélèvement sur le supplément {JULIE['taux_prelevement_aujourdhui']:.0f} % → {JULIE['taux_prelevement_demain']:.0f} %)")

# progression de carrière : ce que garde un salarié seul quand son salaire brut passe de 1,5 à 2 Smic, ou de 2 à 3 Smic
# (charge d'aujourd'hui : courbe OpenFisca de la v3, salarié seul sans niche ; revenu après cotisations de la même courbe)
SAL = json.loads((OUT / "ircsg3.json").read_text(encoding="utf-8"))["courbes"]["salarie"]
bm = np.array([r["brut_mensuel"] for r in SAL])
zz = np.array([r["z"] for r in SAL])
aa = np.array([r["auj"] for r in SAL])
SMIC_M = 21621.6 / 12
PROG = {}
for a1, a2 in ((1.5, 2.0), (2.0, 3.0)):
    b1, b2 = a1 * SMIC_M, a2 * SMIC_M
    z1, z2 = float(np.interp(b1, bm, zz)), float(np.interp(b2, bm, zz))
    t1, t2 = float(np.interp(b1, bm, aa)), float(np.interp(b2, bm, aa))
    n1, n2 = float(N.impot_z(S, O, [z1])[0]), float(N.impot_z(S, O, [z2])[0])
    dz = (z2 - z1) / 12
    PROG[f"{a1}_{a2}"] = dict(brut_mensuel=(b1, b2), hausse_apres_cotisations_mois=dz,
                              garde_aujourdhui_mois=dz - (t2 - t1) / 12, garde_demain_mois=dz - (n2 - n1) / 12,
                              prelevement_aujourdhui_pct=100 * (t2 - t1) / (z2 - z1), prelevement_demain_pct=100 * (n2 - n1) / (z2 - z1))
    v = PROG[f"{a1}_{a2}"]
    p(f"[PROGRESSION] {a1} → {a2} Smic ({b1:,.0f} → {b2:,.0f} € brut/mois, +{dz:.0f} € après cotisations) : garde"
      f" aujourd'hui {v['garde_aujourdhui_mois']:.0f} € ({v['prelevement_aujourdhui_pct']:.1f} % prélevés), demain"
      f" {v['garde_demain_mois']:.0f} € ({v['prelevement_demain_pct']:.1f} %)")
JULIE["progressions"] = PROG

# second conjoint : prélèvement sur le mi-temps repris
m0, m1 = CAS[CAS.cle == "mono"].iloc[0], CAS[CAS.cle == "mono_mi"].iloc[0]
sal2 = float(str(m1.bruts).split(";")[1])
SC = dict(salaire_brut=sal2, aujourdhui_pct=100 * (m1.charge_avec - m0.charge_avec) / sal2,
          demain_pct=100 * (nouveau(m1) - nouveau(m0)) / sal2)
p(f"[SECOND CONJOINT] mi-temps au Smic repris : prélèvement {SC['aujourdhui_pct']:.1f} % → {SC['demain_pct']:.1f} % du brut")

# ------------------------------------------------------------------ minimum vieillesse
# ASPA 2025 (personne seule) : plafond 12 411,44 € par an (OpenFisca, circulaire Cnav 2024-39) ; 12 523,14 € en 2026
# (service-public.gouv.fr, page vérifiée le 23/06/2026) ; ressources : pensions de retraite retenues en brut (OpenFisca :
# retraite_brute ; montants « bruts » sur service-public) ; ASPA exonérée d'IR (CGI art. 81, 9° ; BOFiP
# BOI-RSA-CHAMP-20-50-30) ; assujettissement à la CSG non vérifié sur le texte (OpenFisca ne la soumet pas).
ASPA = 12411.44
COURBE = json.loads((OUT / "ircsg3.json").read_text(encoding="utf-8"))["courbes"]["retraite"]
pe = np.array([r["pension"] for r in COURBE])
auj = np.array([r["auj"] for r in COURBE])
ROWS = []
for P_ in (6000.0, 8000.0, 10000.0, 12000.0, ASPA, 13000.0, 14000.0, 15000.0, 16000.0):
    t_auj = float(np.interp(P_, pe, auj))
    t_new = float(N.impot_z(S, O, [P_])[0])
    aspa = max(ASPA - P_, 0.0)
    rev_auj = P_ + aspa - t_auj
    rev_new = P_ + aspa - t_new                               # ASPA calculée sur la pension brute (droit actuel)
    aspa_net = max(ASPA - (P_ - t_new), 0.0)                  # variante : ASPA calculée sur la pension nette du nouvel impôt
    rev_var = P_ - t_new + aspa_net
    ROWS.append(dict(pension=P_, aspa=aspa, impot_auj=t_auj, impot_nouveau=t_new, revenu_auj=rev_auj, revenu_nouveau=rev_new,
                     perte=rev_auj - rev_new, aspa_variante=aspa_net, revenu_variante=rev_var, perte_variante=rev_auj - rev_var,
                     cout_public_variante=aspa_net - aspa))
p("[ASPA] pension brute / ASPA / impôt aujourd'hui → nouvel impôt / perte annuelle si l'ASPA restait calculée sur la"
  " pension brute / perte avec la règle retenue (ASPA calculée sur la pension nette du nouvel impôt)")
for r in ROWS:
    p(f"  {r['pension']:8,.0f} : ASPA {r['aspa']:6,.0f} ; impôt {r['impot_auj']:5,.0f} → {r['impot_nouveau']:5,.0f} ;"
      f" perte {r['perte']:5,.0f} €/an ({r['perte'] / 12:.0f}/mois) ; variante {r['perte_variante']:5,.0f}")
J["cas_types_nets"] = NETS
J["julie"] = JULIE
J["second_conjoint"] = SC
J["aspa"] = dict(plafond_2025=ASPA, ressources_droit_actuel="pensions brutes", regle_retenue="ASPA calculée sur la pension"
                " nette du nouvel impôt", exoneration_ir="CGI art. 81, 9°", lignes=ROWS, cout_Md=J["final"]["aspa_cout_Md"],
                allocataires_fin_2024=752800, source="DREES, Minima sociaux et prestations sociales, édition 2025, fiche 28",
                nature="dépense sociale (fonds de solidarité vieillesse), hors périmètre fiscal, financée sur l'enveloppe du bloc")
json.dump(J, open(OUT / "ircsg4.json", "w"), ensure_ascii=False, indent=1, default=float)
with open(OUT / "ircsg4_calculs.txt", "a", encoding="utf-8") as fh:
    fh.write("\n[CAS-TYPES]\n" + "\n".join(L) + "\n")


# ------------------------------------------------------------------ tableau LaTeX des cas-types
def fr(v, signe=True):
    s = f"{abs(v):,.0f}".replace(",", "\\,")
    if not signe:
        return s
    return ("$-$" if v < -0.5 else "$+$" if v > 0.5 else "") + s


ORDRE = [("smic_hs", "Salarié au Smic, 10\\,\\% d'heures supplémentaires"),
         ("milieu", "Salarié seul, 40\\,000~€ brut, sans niche"),
         ("julie", "Julie, 2\\,000~€ net par mois"),
         ("garde", "Couple biactif 36\\,+\\,24~k€, deux jeunes enfants gardés"),
         ("garde_dom", "Le même, avec une aide à domicile (3\\,000~€)"),
         ("garde_sans", "Le même, sans niche"),
         ("pi_garde", "Parent isolé au Smic, un enfant gardé"),
         ("nombreuse", "Famille nombreuse 40\\,+\\,25~k€, trois enfants"),
         ("mono", "Couple mono-actif, 45~k€, deux enfants"),
         ("mono_mi", "Le même, le conjoint reprend un mi-temps au Smic"),
         ("ret_modeste", "Retraité seul, pension de 14\\,000~€"),
         ("ret_dom", "Retraitée, 30\\,000~€, aide à domicile (4\\,000~€)"),
         ("cadres", "Cadres 90\\,+\\,60~k€, dons, emploi à domicile, Pinel")]
lig = []
for k, lib in ORDRE:
    v = NETS[k]
    lig.append(f"{lib} & {fr(v['aujourdhui_avec_niches'], False)} & {fr(v['gain_systeme_mois'])} & {fr(v['perte_niches_mois'])}"
               f" & \\textbf{{{fr(v['net_mois'])}}} \\\\")
TEX = ("% Produit par note8p/calculs/ircsg4_cas.py (ne pas éditer à la main).\n"
       "\\begin{tabular}{lrrrr}\\hline\n"
       "Situation & Payé aujourd'hui & Nouveau système & Perte des niches & Variation nette \\\\\n"
       " & (€/an) & (€/mois) & (€/mois) & (€/mois) \\\\ \\hline\n" + "\n".join(lig) + "\n\\hline\\end{tabular}\n")
(OUT / "tab_cas_types.tex").write_text(TEX, encoding="utf-8")
print("tab_cas_types.tex écrit")
