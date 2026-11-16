"""Écrit note8p/annexes/annexe_foncier.tex (version 3) à partir de sorties/foncier3.json et foncier.json.

python3 note8p/calculs/foncier3_annexe.py   (après foncier3_calculs.py)
"""
import json
from pathlib import Path

ICI = Path(__file__).resolve().parent
J = json.loads((ICI.parent / "sorties/foncier3.json").read_text(encoding="utf-8"))
J0 = json.loads((ICI.parent / "sorties/foncier.json").read_text(encoding="utf-8"))
OUT = ICI.parent / "annexes/annexe_foncier.tex"
REC = "B_E12"


def f(x, d=0, signe=False):
    if x is None:
        return "--"
    if round(x, d) == 0:
        return "0"
    s = f"{x:+,.{d}f}" if signe else f"{x:,.{d}f}"
    return s.replace(",", "\\,").replace(".", ",").replace("-", "$-$")


S, TR, P, D = J["scenarios"], J["annuel_par_scenario"], J["parts_recette_nationale"], J0["dmto"]
ENVS = ["9", "10", "12", "15", "18"]

rows_env = []
for a in ("A", "B"):
    for e in ENVS:
        s = S[f"{a}_E{e}"]
        lg, tx, cp = s["logements"], s["taux"], s["capitalisation"]
        tr = TR[f"{a}_E{e}"]
        rows_env.append(
            f"{a} & {e} & {f(tx['tn_sol'], 3)} & {f(tx['tn_bati'], 3)} & {f(lg['moyenne'], signe=True)} & "
            f"{f(lg['pctl']['50'], signe=True)} & {f(lg['pctl']['90'], signe=True)} & {f(lg['plus300'])} & "
            f"{f(lg['plus600'])} & {f(lg['paris_a'], signe=True)} & {f(lg['impot_bati'], 1)} & "
            f"{f(lg['rapport_sol_bati']['p50'], 1)}/{f(lg['rapport_sol_bati']['p90'], 1)} & "
            f"{f(tr['2029']['net'], 1, True)} & {f(tr['2031']['net'], 1, True)} & {f(tr['2040']['net'], 1, True)} \\\\")
    if a == "A":
        rows_env.append("\\midrule")
rows_env = "\n".join(rows_env)

rows_cap = "\n".join(
    f"{e} & " + " & ".join(f(S[f'B_E{e}']['capitalisation'][k]['tous']) for k in
                           ("r3_k0", "r3_k50", "r3_k100", "r4_k0", "r4_k50", "r4_k100"))
    + f" & {f(S[f'B_E{e}']['capitalisation']['r3_k0']['pct_sol_prive'], 1)} & "
      f"{f(S[f'B_E{e}']['capitalisation']['r3_k0']['pct_logements_menages'], 1)} & "
      f"{f(S[f'B_E{e}']['capitalisation']['r3_k100']['pct_logements_menages'], 1)} \\\\" for e in ENVS)

sel = ["2027", "2028", "2029", "2030", "2031", "2032", "2033", "2035", "2040"]
postes = [("taxe_fonciere_nouvelle", "Taxe foncière nouvelle"), ("dmto", "Droits de mutation"),
          ("calendrier_ventes", "Achats différés"), ("report_paiement", "Report de paiement"),
          ("deductibilite_is_ir", "Déductibilité"), ("net", "\\textbf{Net B, 12}")]
rows_tr = "\n".join(f"{lab} & " + " & ".join(f(TR[REC][a][k], 1, True) for a in sel) + " \\\\" for k, lab in postes)
for a in ("B", "A"):
    for e in ENVS:
        k = f"{a}_E{e}"
        if k == REC:
            continue
        rows_tr += "\n" + f"Net {a}, {e} & " + " & ".join(f(TR[k][x]['net'], 1, True) for x in sel) + " \\\\"
is_ = J["is_transition_caisse"]
rows_tr += "\n\\midrule\nIS : taux réduit + déduction & " + " & ".join(f(is_[a], 1, True) for a in sel) + " \\\\"
rows_tr += "\n" + "Taux des droits (\\%) & " + " & ".join(
    f(J["indicateurs_annuels"][REC][a]["taux_dmto_pct"], 2) for a in sel) + " \\\\"

COURT = {'orleans': 'Orléans, app. 65 m²', 'lyon': 'Lyon, app. 80 m²', 'massy': 'Massy, app. 65 m²',
         'sgdb': 'Ste-Geneviève, maison 100 m²'}
rows_cas = []
for i, r in enumerate(J["cas"][REC]["projets"]):
    ca = J["cas"]["A_E12"]["projets"][i]
    b15 = J["cas"]["B_E15"]["projets"][i]
    rows_cas.append(f"{COURT[r['cle']]} & {f(r['prix'])} & {f(r['dmto_permanent'])} & {f(r['economie'])} & "
                    f"{f(r['tf_actuelle'])} & {f(r['dtf'], signe=True)} & {f(ca['dtf'], signe=True)} & "
                    f"{f(b15['dtf'], signe=True)} & {f(r['annees_equivalentes'])} & {f(r['perte_valeur'], signe=True)} \\\\")
rows_cas = "\n".join(rows_cas)
M = J["cas"][REC]["mobilite"]
g6 = J["g6"]
pa, pb = P["A"], P["B"]
b12, a12 = S["B_E12"], S["A_E12"]

tex = rf"""% Annexe du bloc « fiscalité immobilière » (version 3, note8p/CONSIGNES_V3.md). Générée par
% note8p/calculs/foncier3_annexe.py à partir de note8p/sorties/foncier3.json (foncier3_calculs.py, qui importe
% foncier_calculs.py et foncier/simulation.py). Compte rendu : note8p/sorties/foncier3.md. Md€ de 2025, années de caisse.

\subsection{{Données, champ et droits de mutation}}

Modèle communal de \texttt{{foncier/simulation.py}} (inchangé) : 30,5~millions de logements des particuliers de métropole
hors Alsace-Moselle ; valeur = prix médian au m² des ventes 2023-2024 de la commune × surface médiane ; part du sol
mesurée par les terrains à bâtir (maisons) ou par résidu (appartements), calée sur les comptes de patrimoine des ménages ;
taxe foncière de 2025 (REI) répartie au prorata de la valeur dans chaque commune, donc identique en proportion pour tous
les logements d'une commune. Agrégats : comptes de patrimoine de l'Insee (tableau 8.200, fin 2025), biens privés (sociétés,
ménages, ISBLSM), hors terres agricoles et biens publics : sol {f(J['assiette']['sol'])}~Md€, dont {f(J['assiette']['nus'])}
de terrains non bâtis ; bâti {f(J['assiette']['bati'])}~Md€.
Droits au taux permanent de 5,807~\% (4,50~\% département, art.~1594~D CGI ; 1,20~\% commune, art.~1584 ; frais d'assiette
de 2,37~\% de la part départementale, art.~1647~V) ; la majoration à 5~\% (loi n°~2025-127, art.~116) cesse le 31/3/2028.
France entière, ventes de 2025 : {f(D['total_fr'], 1)}~Md€, dont {f(D['logements_fr'], 1)} sur les logements ; la division
par deux coûte \textbf{{{f(D['demi'], 2)}~Md€}} (7,2 aux ventes de 2023-2024, 10,0 à celles de 2022) ; un point de taux vaut
{f(D['cout_par_point'], 2)}~Md€. Aucune reprise durable des ventes n'est comptée.

\subsection{{Deux architectures}}

Chaque bien $i$ a un sol $S_i$ (bâti ou non) et un bâti $B_i$. La part communale est la même dans les deux
architectures : base $S_i + B_i/4$, taux $t_c$ voté par la commune, fixé à la bascule pour garder sa recette
($t_c = \sum_{{i\in c}}\mathrm{{TF}}_i^0/\sum_{{i\in c}}(S_i+B_i/4)$) ; le rapport de 4 est fixé par la loi.
\textbf{{A}} ajoute un taux national uniforme $t_n^A = E/\sum_i (S_i + B_i/4)$ sur la même base : un seul montant par bien.
\textbf{{B}} ajoute une taxe nationale sur le seul sol, $t_n^B = E/\sum_i S_i$ : deux lignes sur l'avis, l'une sur
$S+B/4$, l'autre sur $S$. Le rapport effectif entre le taux du sol et celui du bâti vaut 4 partout dans A et
$4\,(1 + t_n^B/t_c)$ dans B. Répartition de la recette nationale : logements des ménages {f(100*pa['men_log'], 1)}~\% (A) et
{f(100*pb['men_log'], 1)}~\% (B) ; terrains non bâtis {f(100*pa['nus'], 1)} et {f(100*pb['nus'], 1)}~\% ; sociétés
{f(100*pa['societes'], 1)} et {f(100*pb['societes'], 1)}~\% ; part portant sur le bâti {f(100*pa['bati'], 1)}~\% et 0.
Dans le modèle, la part des logements est répartie au prorata de $S_i + B_i/4$ (A) ou de $S_i$ (B).

\textbf{{Capitalisation.}} Valeur d'un bien = loyer net d'impôt capitalisé au taux $r$ (3~\% ; variante 4~\%) : une hausse
permanente d'impôt $\Delta T$ réduit la valeur de $\Delta T/r$. Le bâti restant à son coût de remplacement, la baisse porte
sur le sol, comme dans les comptes de patrimoine où le sol est un résidu. Pour l'ensemble, $\Delta V = -(E - \kappa\,
\Delta D)/r$, où $\Delta D = {f(D['demi'], 2)}$~Md€ est la baisse des droits et $\kappa$ la part capitalisée dans les prix
(0, 50 ou 100~\%) ; le transfert communal du bâti vers le sol est à somme nulle entre biens. Le taux national est calé sur
la base après baisse, avec $\kappa = 0$ (prudent : si les droits se capitalisent, la base et la recette sont plus
grandes). La version précédente faisait aussi porter sur le sol le transfert communal, sans contrepartie : taux 5~\%
plus élevés. Chiffres présentés comme ordres de grandeur, pas comme prévisions : $r$ constant, capitalisation complète,
aucune réaction de l'offre.

\begin{{table}}[!htbp]\centering\scriptsize
\caption{{Enveloppes et architectures : taux, logements, trajectoire}}\label{{tab:fon3_env}}
\setlength{{\tabcolsep}}{{3pt}}
\begin{{tabular}}{{@{{}}llrrrrrrrrrrrrr@{{}}}}
\toprule
 & $E$ & \multicolumn{{2}}{{c}}{{Taux national (\%)}} & \multicolumn{{3}}{{c}}{{Hausse par logement (€/an)}} & \multicolumn{{2}}{{c}}{{Logements (\%)}} & Paris & Bâti & Sol/bâti & \multicolumn{{3}}{{c}}{{Net (Md€)}} \\
\cmidrule(lr){{3-4}}\cmidrule(lr){{5-7}}\cmidrule(lr){{8-9}}\cmidrule(lr){{13-15}}
 & (Md€) & sol & bâti & moy. & méd. & P90 & $>$300 € & $>$600 € & app. & (Md€) & méd./P90 & 2029 & 2031 & 2040 \\
\midrule
{rows_env}
\bottomrule
\end{{tabular}}
\par\vspace{{2pt}}{{\raggedright\scriptsize Taux après capitalisation ($r$ = 3~\%). Paris app. : appartement parisien médian
(€/an). Bâti : impôt sur le bâti des logements du champ, 14,3~Md€
aujourd'hui. Sol/bâti : rapport effectif des taux, médiane et 9\textsuperscript{{e}} décile des logements. Net : table
annuelle (taxe, droits, achats différés, report, déductibilité). Pour la seule substitution aux droits
({f(D['demi'], 1)}~Md€), le net reste négatif ($-$0,8~Md€ en 2040).\par}}
\end{{table}}

\subsection{{Capitalisation : ordres de grandeur}}

\begin{{table}}[!htbp]\centering\scriptsize
\caption{{Baisse de la valeur des biens (et donc du sol), architecture B}}\label{{tab:fon3_cap}}
\begin{{tabular}}{{@{{}}lrrrrrrrrr@{{}}}}
\toprule
 & \multicolumn{{3}}{{c}}{{$r$ = 3~\% (Md€)}} & \multicolumn{{3}}{{c}}{{$r$ = 4~\% (Md€)}} & Sol privé & \multicolumn{{2}}{{c}}{{Logements des ménages}} \\
\cmidrule(lr){{2-4}}\cmidrule(lr){{5-7}}\cmidrule(lr){{9-10}}
$E$ (Md€) & $\kappa$ = 0 & 50~\% & 100~\% & 0 & 50~\% & 100~\% & (\%, $\kappa$ = 0) & $\kappa$ = 0 (\%) & 100~\% (\%) \\
\midrule
{rows_cap}
\bottomrule
\end{{tabular}}
\par\vspace{{2pt}}{{\raggedright\scriptsize $\kappa$ : part de la baisse des droits capitalisée dans les prix. Totaux
identiques dans A ; pour les logements des ménages, A donne 0,1 point de plus. Repère : de fin 2022 à fin 2025, la valeur du
sol bâti de toute l'économie a baissé de {f(J['g10']['sol_2022'] - J['g10']['sol_2025'])}~Md€ (Insee, g10).\par}}
\end{{table}}

Dispersion (B, 12~Md€, $\kappa$ = 0) : 5\textsuperscript{{e}} centile des logements {f(b12['logements']['perte_valeur_pct']['p5'], 1)}~\% ;
{f(b12['logements']['perte_valeur_pct']['plus5'])}~\% des logements perdent plus de 5~\% (A :
{f(a12['logements']['perte_valeur_pct']['p5'], 1)}~\% et {f(a12['logements']['perte_valeur_pct']['plus5'])}~\%). Effet sur la
consommation, ordre de grandeur : propension marginale à consommer le patrimoine immobilier de 0,7 centime par euro en
France (Arrondel, Lamarche et Savignac, 2015, Enquête Patrimoine 2010, coupe transversale ; 1,4 centime en bas de la
distribution, 0,8 en haut), soit, pour une perte des ménages de {f(J['consommation'][REC]['0']['perte_menages'])}~Md€
($\kappa$ = 0), {f(J['consommation'][REC]['0']['conso_07'], 1)} à {f(J['consommation'][REC]['0']['conso_14'], 1)}~Md€ de
consommation annuelle en moins, avant tout recyclage de la recette ; {f(J['consommation'][REC]['100']['conso_07'], 1)}
à {f(J['consommation'][REC]['100']['conso_14'], 1)}~Md€ si $\kappa$ = 100~\%. Les 5 à 7 centimes estimés aux États-Unis
(Mian, Rao et Sufi, 2013) reposent sur le crédit hypothécaire rechargeable, absent en France (Chauvin et Muellbauer, 2018).

\subsection{{Trajectoire}}

Calendrier [C] : loi en 2027, premier avis à l'automne 2029 ; part nationale par tiers en 2029, 2030 et 2031 ; taux des
droits baissé au 1\textsuperscript{{er}} janvier des mêmes années (5,81 → 4,84 → 3,87 → 2,90~\%) ; chaque palier de baisse
est suspendu tant que le palier de taxe correspondant n'est pas mis en recouvrement. Achats différés [H, calé sur Bérard et
Trannoy, 2018] : 3~\% des ventes annuelles décalées de décembre à janvier par point de baisse annoncée. Report de paiement
[C, provision H] : 25~\% des hausses des propriétaires occupants dues par des ménages éligibles, recours de moitié,
intérêt de 3~\%, remboursement de 1/15 du stock par an. Déductibilité [droit en vigueur, taux effectifs H] : 20~\% de la
part des sociétés à l'IS hors HLM et 25~\% de la hausse des bailleurs, l'année suivante.

\begin{{table}}[!htbp]\centering\scriptsize
\caption{{Table annuelle (Md€ de 2025, années de caisse ; + = recette)}}\label{{tab:fon3_traj}}
\setlength{{\tabcolsep}}{{3.5pt}}
\begin{{tabular}}{{@{{}}lrrrrrrrrr@{{}}}}
\toprule
 & {" & ".join(sel)} \\
\midrule
{rows_tr}
\bottomrule
\end{{tabular}}
\par\vspace{{2pt}}{{\raggedright\scriptsize Toutes les années : \texttt{{annuel\_par\_scenario}} de foncier3.json. Ligne IS :
fin du taux réduit et déduction de 50~\% (bloc IS, en caisse), pour comparaison ; elle n'est pas comprise dans le net.\par}}
\end{{table}}

\subsection{{Cas-types et construction}}

\begin{{table}}[!htbp]\centering\scriptsize
\caption{{Achats types (prix = médiane DVF 2023-2024 au m² × surface)}}\label{{tab:fon3_cas}}
\setlength{{\tabcolsep}}{{3.5pt}}
\begin{{tabular}}{{@{{}}lrrrrrrrrr@{{}}}}
\toprule
 & Prix & Droits & Économie & Taxe & \multicolumn{{3}}{{c}}{{Hausse de taxe (€/an)}} & Années & Perte de \\
\cmidrule(lr){{6-8}}
 & (€) & 5,81~\% & (€) & actuelle & B, 12 & A, 12 & B, 15 & équiv. & valeur (€) \\
\midrule
{rows_cas}
\bottomrule
\end{{tabular}}
\par\vspace{{2pt}}{{\raggedright\scriptsize Années équiv. : économie de droits / hausse annuelle (B, 12). Perte de valeur :
hausse capitalisée à 3~\%, supportée par le propriétaire en place au moment de l'annonce.\par}}
\end{{table}}

Famille mutée d'Orléans (maison de {f(M['vend'])}~€) à Sainte-Geneviève-des-Bois (achat de {f(M['achete'])}~€) : droits de
{f(M['droits_2026'])}~€ en 2026 (6,32~\%), {f(M['droits_permanent'])}~€ au taux permanent, {f(M['droits_apres'])}~€ après
réforme ; taxe foncière de la nouvelle maison {f(M['dtf_sgdb'], signe=True)}~€/an (B, 12). Construction (g6) : terrain de
{f(g6['sol'])}~€ et immeuble de {f(g6['bati'])}~€ ; l'impôt dû à cause de l'immeuble vaut {f(g6['aujourdhui']['construire'])}~€
aujourd'hui, {f(g6['A_E12']['construire'])}~€ avec A et {f(g6['B_E12']['construire'])}~€ avec B (12~Md€) ; garder le terrain
nu coûte {f(g6['aujourdhui']['nu'])}, {f(g6['A_E12']['nu'])} et {f(g6['B_E12']['nu'])}~€.

\subsection{{Hypothèses retirées et limites}}

Retirés de cette version, faute de mécanisme établi ou de calibrage : le gain sur le nombre de ventes et la perte sèche
évitée sur les ventes (la réaction durable n'est pas établie en France), l'extrapolation de la mobilité des propriétaires,
le triangle de Harberger sur le bâti, la variante de baisse unique des droits en 2030. Limites : valeurs du sol par
secteur sans géographie pour les sociétés ; contenu mal connu des terrains non bâtis (sans eux, taux +7~\%) ; même taux de
la valeur dans une commune (les perdants réels seront plus dispersés) ; report et déductibilité paramétrés ; calendrier
d'évaluation ambitieux (le Bade-Wurtemberg a mis plus de quatre ans).
"""
OUT.write_text(tex, encoding="utf-8")
print("annexe écrite :", OUT)
