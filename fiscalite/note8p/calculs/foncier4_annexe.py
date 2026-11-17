"""Écrit note8p/annexes/annexe_foncier.tex (version 4), centrée sur le scénario central B_E10, à partir de
sorties/foncier3.json (taux, logements, trajectoire, cas-types, variantes), sorties/foncier4.json (capitalisation selon la
rotation, loyers et taux, IFI) et sorties/foncier.json (droits de mutation).

python3 note8p/calculs/foncier4_annexe.py   (après foncier3_calculs.py et foncier4_calculs.py)
"""
import json
from pathlib import Path

ICI = Path(__file__).resolve().parent
S_ = ICI.parent / "sorties"
J = json.loads((S_ / "foncier3.json").read_text(encoding="utf-8"))
K = json.loads((S_ / "foncier4.json").read_text(encoding="utf-8"))
J0 = json.loads((S_ / "foncier.json").read_text(encoding="utf-8"))
OUT = ICI.parent / "annexes/annexe_foncier.tex"
REC = "B_E10"


def f(x, d=0, signe=False):
    if x is None:
        return "--"
    if round(x, d) == 0:
        return "0"
    s = f"{x:+,.{d}f}" if signe else f"{x:,.{d}f}"
    return s.replace(",", "\\,").replace(".", ",").replace("-", "$-$")


S, TR, P, D = J["scenarios"], J["annuel_par_scenario"], J["parts_recette_nationale"], J0["dmto"]
s10 = S[REC]
lg, tx = s10["logements"], s10["taux"]
C3, C4 = K["capitalisation"]["r3"], K["capitalisation"]["r4"]
ROT, LP, IFI = K["rotation"], K["loyers_prix"], K["ifi"]
pb = P["B"]

# ------------------------------------------------------------------ tableau 1 : le scénario central par dixième de prix
rows_dec = []
for i in range(10):
    rows_dec.append(f"{i+1} & {f(J0['dec_pm2'][i] / 1000, 1)} & {f(lg['dtf'][i], signe=True)} & "
                    f"{f(J0['tfv_auj'][i], 2)} & {f(lg['tfv'][i], 2)} & {f(C3['perte_tf_decile'][i], 1)} & "
                    f"{f(C3['b']['net_decile'][i], 1, True)} & {f(C3['c']['net_decile'][i], 1, True)} \\\\")
rows_dec = "\n".join(rows_dec)

# ------------------------------------------------------------------ tableau 2 : capitalisation, logements des ménages
def ligne_cap(lib, k):
    a3 = 0.0 if k == "a" else C3[k]["gain_md"]
    a4 = 0.0 if k == "a" else C4[k]["gain_md"]
    return (f"{lib} & {f(a3, 0, True)} & {f(a3 - C3['perte_tf_md'], 0, True)} & "
            f"{f(100 * (a3 - C3['perte_tf_md']) / K['valeur_logements_menages'], 1, True)} & "
            f"{f(a4 - C4['perte_tf_md'], 0, True)} & {f(C3[k]['gagnants_pct'])} \\\\")


rows_cap = "\n".join([
    ligne_cap("(a) Prix rigides : l'acheteur garde l'économie", "a"),
    ligne_cap("(b) Le vendeur capte l'économie de son acheteur", "b"),
    ligne_cap("(c) Les prix intègrent toutes les ventes futures", "c")])

# ------------------------------------------------------------------ tableau 3 : trajectoire B_E10
sel = ["2027", "2028", "2029", "2030", "2031", "2032", "2033", "2035", "2040"]
postes = [("taxe_fonciere_nouvelle", "Taxe sur le sol"), ("dmto", "Droits de mutation"),
          ("calendrier_ventes", "Achats différés"), ("report_paiement", "Report de paiement"),
          ("deductibilite_is_ir", "Déductibilité"), ("net", "\\textbf{Net}")]
rows_tr = "\n".join(f"{lab} & " + " & ".join(f(TR[REC][a][k], 1, True) for a in sel) + " \\\\" for k, lab in postes)
rows_tr += "\n" + "Taux des droits (\\%) & " + " & ".join(
    f(J["indicateurs_annuels"][REC][a]["taux_dmto_pct"], 2) for a in sel) + " \\\\"

# ------------------------------------------------------------------ tableau 4 : cas-types
COURT = {'orleans': 'Orléans, app. 65 m²', 'lyon': 'Lyon, app. 80 m²', 'massy': 'Massy, app. 65 m²',
         'sgdb': 'Ste-Geneviève, maison 100 m²'}
rows_cas = []
for r, k4 in zip(J["cas"][REC]["projets"], K["cas"]):
    rows_cas.append(f"{COURT[r['cle']]} & {f(r['prix'])} & {f(r['dmto_permanent'])} & {f(r['economie'])} & "
                    f"{f(r['tf_actuelle'])} & {f(r['dtf'], signe=True)} & {f(k4['point_mort'])} & "
                    f"{f(k4['intervalle'])} & {f(r['perte_valeur'], signe=True)} \\\\")
rows_cas = "\n".join(rows_cas)
M = J["cas"][REC]["mobilite"]
g6 = J["g6"]

# ------------------------------------------------------------------ tableau 5 : variantes (une ligne par scénario)
rows_var = []
for k in ("B_E9", "B_E10", "B_E12", "B_E15", "B_E18", "A_E10"):
    s, l_, tr = S[k], S[k]["logements"], TR[k]
    cp = s["capitalisation"]["r3_k0"]
    nom = ("\\textbf{B, 10 (central)}" if k == REC else
           (f"B, {k[3:]}" if k[0] == "B" else "A, 10 (base unique)"))
    rows_var.append(
        f"{nom} & {f(s['taux']['tn_sol'], 3)} & {f(l_['moyenne'], signe=True)} & {f(l_['pctl']['50'], signe=True)} & "
        f"{f(l_['pctl']['90'], signe=True)} & {f(l_['plus600'])} & {f(l_['paris_a'], signe=True)} & "
        f"{f(g6[k]['construire'])} & {f(cp['pct_logements_menages'], 1)} & {f(tr['2029']['net'], 1, True)} & "
        f"{f(tr['2031']['net'], 1, True)} & {f(tr['2040']['net'], 1, True)} \\\\")
rows_var = "\n".join(rows_var)

perte_men = C3["perte_tf_md"]
conso = {k: (0.007 * v, 0.014 * v) for k, v in (("a", perte_men), ("b", -C3["b"]["net_md"]))}

tex = rf"""% Annexe du bloc « fiscalité immobilière » (version 4, note8p/CONSIGNES_V4.md). Générée par
% note8p/calculs/foncier4_annexe.py à partir de note8p/sorties/foncier3.json (foncier3_calculs.py), foncier4.json
% (foncier4_calculs.py) et foncier.json. Compte rendu : note8p/sorties/foncier4.md. Scénario central B_E10.
% Md€ de 2025, années de caisse.

\subsection{{Données, champ et droits de mutation}}

Modèle communal de \texttt{{foncier/simulation.py}} : 30,5~millions de logements des particuliers de métropole hors
Alsace-Moselle ; valeur = prix médian au m² des ventes 2023-2024 de la commune × surface médiane ; part du sol mesurée
par les terrains à bâtir (maisons) ou par résidu (appartements), calée sur les comptes de patrimoine des ménages ; taxe
foncière de 2025 (REI) répartie au prorata de la valeur dans chaque commune, donc identique en proportion pour tous les
logements d'une commune. Agrégats : comptes de patrimoine de l'Insee (tableau 8.200, fin 2025), biens privés (sociétés,
ménages, ISBLSM), hors terres agricoles et biens publics : sol {f(J['assiette']['sol'])}~Md€, dont
{f(J['assiette']['nus'])} de terrains non bâtis ; bâti {f(J['assiette']['bati'])}~Md€. Droits au taux permanent de
5,807~\% (4,50~\% département, art.~1594~D CGI ; 1,20~\% commune, art.~1584 ; frais d'assiette de 2,37~\% de la part
départementale, art.~1647~V) ; la majoration à 5~\% (loi n°~2025-127, art.~116) cesse le 31/3/2028. France entière,
ventes de 2025 : {f(D['total_fr'], 1)}~Md€, dont {f(D['logements_fr'], 1)} sur les logements ; la division par deux
coûte \textbf{{{f(D['demi'], 2)}~Md€}} (7,2 aux ventes de 2023-2024, 10,0 à celles de 2022) [S]. Aucune reprise durable
des ventes n'est comptée.

\subsection{{Le scénario central : double taux communal et 10~Md€ sur le seul sol}}

Chaque bien $i$ a un sol $S_i$ (bâti ou non) et un bâti $B_i$. Part communale [C] : base $S_i + B_i/4$, taux $t_c$ voté
par la commune et fixé à la bascule pour garder sa recette ($t_c = \sum_{{i\in c}}\mathrm{{TF}}_i^0/\sum_{{i\in c}}(S_i+B_i/4)$).
Part nationale [C] : $t_n = E/\sum_i S_i$ sur le seul sol, avec $E$ = 10~Md€ de recette nationale nouvelle. Le rapport
effectif entre le taux du sol et celui du bâti vaut $4\,(1 + t_n/t_c)$ : {f(lg['rapport_sol_bati']['p10'], 1)} (1\textsuperscript{{er}} décile
des logements), {f(lg['rapport_sol_bati']['p50'], 1)} (médiane), {f(lg['rapport_sol_bati']['p90'], 1)} (9\textsuperscript{{e}}
décile), {f(lg['rapport_sol_bati']['paris'], 1)} à Paris. Taux national après capitalisation de la taxe : \textbf{{{f(tx['tn_sol'], 3)}~\%}}
du sol ({f(tx['tn_statique'], 3)}~\% sur les valeurs actuelles ; {f(s10['taux_r4']['tn_sol'], 3)}~\% si $r$ = 4~\%).
Taux communal moyen : {f(tx['tc_sol'], 2)}~\% du sol et {f(tx['tc_bati'], 2)}~\% du bâti. La recette nationale est payée
à {f(100*pb['men_log'], 1)}~\% par les logements des ménages, {f(100*pb['nus'], 1)}~\% par les terrains non bâtis et
{f(100*pb['societes'], 1)}~\% par les sociétés ; rien ne porte sur le bâti, dont l'impôt (logements du champ) passe de
14,3 à {f(lg['impot_bati'], 1)}~Md€.

Par logement [S] : hausse moyenne {f(lg['moyenne'], signe=True)}~€ par an, médiane {f(lg['pctl']['50'], signe=True)}~€,
9\textsuperscript{{e}} décile {f(lg['pctl']['90'], signe=True)}~€ ; {f(lg['plus300'])}~\% des logements paient plus de
300~€ de plus, {f(lg['plus600'])}~\% plus de 600~€ ; la taxe baisse pour {f(lg['baisse'])}~\%. Maisons
{f(lg['maisons'], signe=True)}~€, appartements {f(lg['apparts'], signe=True)}~€ ; Paris {f(lg['paris_pct'], signe=True)}~\%
(appartement médian {f(lg['paris_a'], signe=True)}~€).

\begin{{table}}[!htbp]\centering\scriptsize
\caption{{Scénario central par dixième de logements classés selon le prix au m² de leur commune}}\label{{tab:fon4_dec}}
\setlength{{\tabcolsep}}{{4pt}}
\begin{{tabular}}{{@{{}}lrrrrrrr@{{}}}}
\toprule
 & Prix & Hausse & \multicolumn{{2}}{{c}}{{Taxe / valeur (\%)}} & \multicolumn{{3}}{{c}}{{Valeur du logement (\%, $r$ = 3~\%)}} \\
\cmidrule(lr){{4-5}}\cmidrule(l){{6-8}}
Dixième & (k€/m²) & (€/an) & avant & après & taxe seule & net (b) & net (c) \\
\midrule
{rows_dec}
\bottomrule
\end{{tabular}}
\par\vspace{{2pt}}{{\raggedright\scriptsize Prix : médiane du dixième. Taxe / valeur avant capitalisation (figure g4).
Valeur : effet de la seule taxe, puis effet net de la baisse des droits selon les hypothèses (b) et (c) de la
section suivante, en \% de la valeur du modèle (prix DVF).\par}}
\end{{table}}

\subsection{{Capitalisation : qui perd, qui gagne}}

\textbf{{Taxe annuelle.}} Valeur d'un bien = loyer net d'impôt actualisé au taux $r$ (3~\% ; variante 4~\%, dans la
fourchette de 3 à 4~\% estimée en Angleterre par Koster et Pinchbeck, 2022, et cohérente avec la capitalisation complète
mesurée au Danemark par Høj, Jørgensen et Schou, 2018) [E]. Une hausse permanente $\Delta T$ réduit la valeur de
$\Delta T/r$ ; le bâti restant à son coût de remplacement, la baisse porte sur le sol. Hypothèses [H] : $r$ constant,
taxe jugée permanente, aucune réaction de l'offre ni des loyers. Le propriétaire en place à l'annonce supporte toute la
perte ; l'acheteur suivant paie moins cher un bien plus taxé et n'y perd rien. Au total, la valeur des biens privés
baisse de {f(K['ensemble_biens']['r3']['perte_tf'])}~Md€ ({f(K['ensemble_biens']['r4']['perte_tf'])} si $r$ = 4~\%),
dont {f(perte_men)}~Md€ pour les logements des ménages ({f(C3['perte_tf_pct'], 1)}~\% de leur valeur).

\textbf{{Droits de mutation.}} Ils ne se capitalisent pas comme une taxe annuelle. Ils sont payés à la vente, à des
dates irrégulières, et l'économie d'un bien dépend de sa fréquence de revente. Si un bien est vendu au hasard au taux
$\rho$ par an (part de sa valeur vendue chaque année), la valeur actuelle de la baisse $\Delta\tau$ = 2,90 points vaut
$\Delta\tau\,P\,\rho/r$ quand les prix intègrent toutes les ventes futures ; c'est l'économie annuelle moyenne $\Delta\tau
P\rho$ divisée par $r$. Les droits se capitalisent donc « euro pour euro » \emph{{en moyenne}}, mais bien par bien en
proportion de la rotation, non de la valeur. Le propriétaire gagne si son bien change de main plus souvent que tous les
$H^* = \Delta\tau\,P/\Delta T$ ans (point mort indépendant de $r$) et perd sinon.

\textbf{{Rotation observée}} [S, DVF 2025] : la valeur des ventes de logements représente {f(100*ROT['agregee'], 1)}~\% de
la valeur du parc chaque année, soit un changement de main tous les {f(ROT['intervalle_moyen'])} ans en moyenne
(maisons {f(100*ROT['maisons'], 1)}~\%, appartements {f(100*ROT['apparts'], 1)}~\% ; de {f(100*ROT['p10'], 1)} à
{f(100*ROT['p90'], 1)}~\% du 1\textsuperscript{{er}} au 9\textsuperscript{{e}} décile des logements). La durée de détention
des biens revendus est bien plus courte : 13,7 ans pour les appartements et 15,8 ans pour les maisons en Île-de-France en
2024 (Notaires du Grand Paris) [E, pas de série nationale trouvée]. L'écart tient aux logements gardés jusqu'au décès et
transmis sans vente, qui ne paient pas de droits de mutation à titre onéreux. Appliquer une durée de 10 à 15 ans à tout
le parc surestimerait le gain d'un facteur 3 à 4 (de {f(K['gain_c_si_H_uniforme_pct']['15'], 1)} à
{f(K['gain_c_si_H_uniforme_pct']['10'], 1)}~\% de la valeur au lieu de {f(C3['c']['gain_pct'], 1)}~\%).

\textbf{{Trois hypothèses d'incidence}} [H, encadrées par la littérature]. (a) Prix rigides : lors de la hausse de 2014,
le prix hors droits n'a pas bougé et l'acheteur a tout supporté (Bachelet et Poulhès, 2017, CGDD) [E] ; symétriquement,
l'acheteur garderait l'économie et le propriétaire en place n'en tirerait rien, sauf comme acheteur de son logement
suivant. (b) Le vendeur capte l'économie de son seul acheteur (prix plus élevé de $\Delta\tau/(1+\tau_1)$, sans
anticipation des reventes suivantes) : gain $\approx \Delta\tau\,P\,\rho/(\rho + r)$. (c) Les prix intègrent toutes les
ventes futures : gain $\Delta\tau\,P\,\rho/r$. Dolls, Fuest, Krolage et Neumeier (2025, \emph{{JUE}}) trouvent en
Allemagne une baisse des prix demandés de 3~\% par point de droits, davantage pour les appartements qui tournent plus
vite, ce qui est de l'ordre de (c) [E]. Nous retenons (b) comme ordre de grandeur central, (a) et (c) comme bornes.

\begin{{table}}[!htbp]\centering\scriptsize
\caption{{Variation de la valeur des logements des ménages, scénario central (Md€)}}\label{{tab:fon4_cap}}
\setlength{{\tabcolsep}}{{4pt}}
\begin{{tabular}}{{@{{}}lrrrrr@{{}}}}
\toprule
 & Droits & \multicolumn{{2}}{{c}}{{Net, $r$ = 3~\%}} & Net & Logements \\
\cmidrule(lr){{3-4}}
 & ($r$ = 3~\%) & Md€ & \% & $r$ = 4~\% & gagnants (\%) \\
\midrule
Taxe sur le sol seule & -- & {f(-perte_men, 0, True)} & {f(-C3['perte_tf_pct'], 1, True)} & {f(-C4['perte_tf_md'], 0, True)} & -- \\
{rows_cap}
\bottomrule
\end{{tabular}}
\par\vspace{{2pt}}{{\raggedright\scriptsize Valeur des logements des ménages : {f(K['valeur_logements_menages'])}~Md€
(Insee, fin 2025). Calcul logement par logement avec la rotation de sa commune et de son type ; Md€ France entière.
Logements gagnants : dont la valeur nette monte. Pour l'ensemble des biens privés, (c) donne
{f(-K['ensemble_biens']['r3']['net_c'], 0, True)}~Md€ (taxe $-${f(K['ensemble_biens']['r3']['perte_tf'])}, droits
+{f(K['ensemble_biens']['r3']['gain_c'])}).\par}}
\end{{table}}

Lecture. La baisse des droits compense en moyenne une bonne part de la taxe, mais pas pour les mêmes propriétaires :
les communes bon marché, où la taxe monte peu et où l'on revend souvent, gagnent ; les dixièmes chers perdent 2 à
2,6~\% dans le cas (b). Le point mort médian du parc est de {f(K['point_mort']['p50'])} ans (quartiles
{f(K['point_mort']['p25'])} et {f(K['point_mort']['p75'])}) : un propriétaire qui ne vend presque jamais là où le sol
est cher porte l'essentiel de la perte. Effet sur la consommation, ordre de grandeur : avec une propension marginale de
0,7 à 1,4 centime par euro de patrimoine immobilier (Arrondel, Lamarche et Savignac, 2015, Enquête Patrimoine 2010,
coupe transversale) [E], la perte nette (b) réduirait la consommation de {f(conso['b'][0], 1)} à {f(conso['b'][1], 1)}~Md€
par an, {f(conso['a'][0], 1)} à {f(conso['a'][1], 1)} dans le cas (a), avant recyclage de la recette ; l'effet de
richesse immobilière agrégé est faible en France (Chauvin et Muellbauer, 2018).

\subsection{{Valeur du sol : rentes ou taux ?}}

\begin{{figure}}[!htbp]\centering
\includegraphics[width=\linewidth]{{figures/g10b_loyers_taux.pdf}}\par\vspace{{1pt}}
{{\raggedright\scriptsize\color{{gris}}\input{{figures/g10b_loyers_taux_source.tex}}\par}}
\caption{{Les prix ont doublé par rapport aux loyers pendant que les taux longs baissaient}}\label{{fig:g10b}}
\end{{figure}}

La hausse du sol bâti de {f(J['g10']['ensemble'][J['g10']['annees'].index(1998)])}~\% à
{f(J['g10']['ensemble'][J['g10']['annees'].index(2025)])}~\% du PIB entre 1998 et 2025 (g10) ne mesure pas la hausse des
rentes annuelles. De 1998 à 2025, les prix des logements anciens ont été multipliés par {f(LP['prix'], 1)} et les loyers
(IPC) par {f(LP['loyers'], 1)} : le rapport loyers / prix a été divisé par deux, pendant que le taux de l'emprunt d'État
à 10 ans passait de {f(LP['oat']['1998'], 1)}~\% à {f(LP['oat']['2020'], 1)}~\% (2020) puis {f(LP['oat']['2025'], 1)}~\%
(2025) [E]. Une grande part de la hausse reflète donc la baisse des taux d'actualisation et des anticipations de loyers,
et la baisse de 2022-2025 coïncide avec leur remontée. La part attribuable aux rentes courantes ne peut pas être isolée
avec ces seules séries (l'indice des loyers suit des baux de qualité constante et sous-estime les loyers de
relocation) ; l'argument pour taxer le sol tient à son offre fixe, pas à l'ampleur de sa revalorisation.

\subsection{{Trajectoire du scénario central}}

Calendrier [C] : loi en 2027, premier avis à l'automne 2029 ; part nationale par tiers en 2029, 2030 et 2031 ; taux des
droits baissé au 1\textsuperscript{{er}} janvier des mêmes années (5,81 → 4,84 → 3,87 → 2,90~\%) ; chaque palier de
baisse est suspendu tant que le palier de taxe correspondant n'est pas mis en recouvrement. Achats différés [H, calé sur
Bérard et Trannoy, 2018] : 3~\% des ventes annuelles décalées de décembre à janvier par point de baisse annoncée. Report
de paiement [C, provision H] : 25~\% des hausses des propriétaires occupants dues par des ménages éligibles, recours de
moitié, intérêt de 3~\%, remboursement de 1/15 du stock par an. Déductibilité [droit en vigueur, taux effectifs H] :
20~\% de la part des sociétés à l'IS hors HLM et 25~\% de la hausse des bailleurs, l'année suivante.

\begin{{table}}[!htbp]\centering\scriptsize
\caption{{Table annuelle, scénario central (Md€ de 2025, années de caisse ; + = recette)}}\label{{tab:fon4_traj}}
\setlength{{\tabcolsep}}{{3.5pt}}
\begin{{tabular}}{{@{{}}lrrrrrrrrr@{{}}}}
\toprule
 & {" & ".join(sel)} \\
\midrule
{rows_tr}
\bottomrule
\end{{tabular}}
\par\vspace{{2pt}}{{\raggedright\scriptsize Toutes les années : \texttt{{annuel\_par\_scenario["B\_E10"]}} de
foncier3.json. Chaque milliard de recette nationale en plus rapporte 0,90~Md€ net (déductibilité).\par}}
\end{{table}}

\subsection{{Cas-types et construction}}

\begin{{table}}[!htbp]\centering\scriptsize
\caption{{Achats types, scénario central (prix = médiane DVF 2023-2024 au m² × surface)}}\label{{tab:fon4_cas}}
\setlength{{\tabcolsep}}{{3.5pt}}
\begin{{tabular}}{{@{{}}lrrrrrrrr@{{}}}}
\toprule
 & Prix & Droits & Économie & Taxe & Hausse & Point & Intervalle & Perte de \\
 & (€) & 5,81~\% & (€) & actuelle & (€/an) & mort (ans) & commune (ans) & valeur (€) \\
\midrule
{rows_cas}
\bottomrule
\end{{tabular}}
\par\vspace{{2pt}}{{\raggedright\scriptsize Point mort : économie de droits / hausse annuelle ; un bien revendu plus
souvent y gagne dans le cas (c). Intervalle commune : inverse de la rotation des logements du même type dans la commune.
Perte de valeur : hausse de taxe capitalisée à 3~\%, avant prise en compte des droits.\par}}
\end{{table}}

Famille mutée d'Orléans (maison de {f(M['vend'])}~€) à Sainte-Geneviève-des-Bois (achat de {f(M['achete'])}~€) : droits de
{f(M['droits_2026'])}~€ en 2026 (6,32~\%), {f(M['droits_permanent'])}~€ au taux permanent, {f(M['droits_apres'])}~€ après
réforme ; taxe foncière de la nouvelle maison {f(M['dtf_sgdb'], signe=True)}~€/an. Construction (g6) : sur un terrain de
{f(g6['sol'])}~€, un immeuble de {f(g6['bati'])}~€ ajoute {f(g6['aujourdhui']['construire'])}~€ d'impôt par an aujourd'hui,
{f(g6[REC]['construire'])}~€ dans le scénario central et {f(g6['A_E10']['construire'])}~€ si la part nationale portait aussi
sur le bâti/4 ; garder le terrain nu coûte {f(g6['aujourdhui']['nu'])}~€, puis {f(g6[REC]['nu'])}~€.

\subsection{{Variantes d'enveloppe et d'architecture}}

\begin{{table}}[!htbp]\centering\scriptsize
\caption{{Variantes (taux après capitalisation, $r$ = 3~\%)}}\label{{tab:fon4_var}}
\setlength{{\tabcolsep}}{{3pt}}
\begin{{tabular}}{{@{{}}lrrrrrrrrrrr@{{}}}}
\toprule
 & Taux & \multicolumn{{3}}{{c}}{{Hausse par logement (€/an)}} & $>$600 € & Paris & Construire & Valeur & \multicolumn{{3}}{{c}}{{Net (Md€)}} \\
\cmidrule(lr){{3-5}}\cmidrule(l){{10-12}}
Architecture, $E$ & sol (\%) & moy. & méd. & P90 & (\%) & app. & (€/an) & logts (\%) & 2029 & 2031 & 2040 \\
\midrule
{rows_var}
\bottomrule
\end{{tabular}}
\par\vspace{{2pt}}{{\raggedright\scriptsize Valeur logts : baisse de la valeur des logements des ménages due à la seule
taxe. Construire : impôt dû à cause de l'immeuble de g6. A : part nationale sur la même base sol + bâti/4 (taux du bâti
= taux du sol / 4). Seule substitution aux droits ({f(D['demi'], 1)}~Md€) : net $-$0,8~Md€ par an. Tables annuelles de
toutes les variantes : \texttt{{annuel\_par\_scenario}} de foncier3.json ; toute enveloppe :
\texttt{{foncier3\_calculs.py --E <Md€> --archi B}}.\par}}
\end{{table}}

\subsection{{IFI : une substitution possible à terme}}

L'IFI a rapporté 2,2~Md€ en 2024 (186\,000 foyers, patrimoine immobilier net taxable de 467~Md€, soit
{f(IFI['taux_moyen_ifi'], 2)}~\% en moyenne) et 2,3~Md€ en 2025 (193\,600 foyers) [E, DGFiP, chiffres lus dans des
sources secondaires]. Il taxe le bâti comme le sol, net des dettes, au-dessus d'un seuil de 1,3~M€ : c'est un impôt sur
une fraction des propriétaires, qui pénalise la construction et se contourne par l'endettement et le démembrement. Une
taxe nationale sur le sol remplit mieux sa fonction de taxation de la rente : à terme, une fois les nouvelles valeurs
fiables, elle pourrait s'y substituer ; à recette égale, il faudrait environ {f(IFI['points_taux_sol_equivalents'], 2)}
point de plus sur le sol. Cette substitution déplace la charge des patrimoines élevés vers l'ensemble des propriétaires :
c'est un choix distinct, non compté dans le financement [C].

\subsection{{Hypothèses retirées et limites}}

Non chiffrés, faute de mécanisme établi en France ou de calibrage : la reprise durable du nombre de ventes, la perte
sèche évitée sur les ventes, la mobilité des propriétaires, le triangle de Harberger sur le bâti. Limites : valeurs du
sol des sociétés sans géographie ; contenu mal connu des terrains non bâtis (sans eux, taux +7~\%) ; même taux de la
valeur dans une commune (les perdants réels seront plus dispersés) ; rotation mesurée sur une seule année de ventes
(2025, basse) ; report et déductibilité paramétrés ; calendrier d'évaluation ambitieux (le Bade-Wurtemberg a mis plus
de quatre ans).
"""
OUT.write_text(tex, encoding="utf-8")
print("annexe écrite :", OUT)
