"""Écrit note8p/annexes/annexe_foncier.tex à partir de note8p/sorties/foncier.json (lancer après foncier_calculs.py).

python3 note8p/calculs/foncier_annexe.py
"""
import json
from pathlib import Path

ICI = Path(__file__).resolve().parent
J = json.loads((ICI.parent / "sorties/foncier.json").read_text(encoding="utf-8"))
OUT = ICI.parent / "annexes/annexe_foncier.tex"
OUT.parent.mkdir(exist_ok=True)


def f(x, d=0, signe=False):
    if round(x, d) == 0:
        return "0"
    s = f"{x:+,.{d}f}" if signe else f"{x:,.{d}f}"
    s = s.replace(",", "\\,").replace(".", ",")
    return s.replace("-", "$-$")


D, A, T, LG = J["dmto"], J["assiette"], J["taux"], J["logements"]
CAP, TR, CAS, G = J["capitalisation"], J["annuel_par_scenario"], J["cas"], J["gains"]
H = J["hypotheses_trajectoire"]
ENVS = ["substitution", "E10", "E15", "E20"]
LAB = {"substitution": f"{f(D['demi'], 1)} (substitution)", "E10": "10", "E15": "15 (recommandée)", "E20": "20"}

# --- tableau par dixième
dec = J["dec_pm2"]
rows_dec = "\n".join(
    f"{k+1} & {f(dec[k])} & {f(J['tfv_auj'][k], 2)} & {f(LG['E10']['dtf'][k], signe=True)} & "
    f"{f(LG['E15']['dtf'][k], signe=True)} & {f(LG['E15']['dtf_pct'][k], signe=True)} & "
    f"{f(LG['E20']['dtf'][k], signe=True)} & {f(LG['E15']['net_parc'][k], signe=True)} & {f(LG['E15']['tfv'][k], 2)} & "
    f"{f(CAP['E15']['par_decile_pct'][k], 1, True)} \\\\" for k in range(10))

# --- tableau des enveloppes
rows_env = "\n".join(
    f"{LAB[e]} & {f(T[e]['tn_statique'], 3)} & {f(T[e]['tn'], 3)} & {f(T[e]['tn_r4'], 3)} & {f(T[e]['baisse_sol'], 1)} & "
    f"{f(T[e]['rendement_taux_statique'], 1)} & {f(LG[e]['paye_logements_fr'], 1)} & {f(CAP[e]['total_tous'])} & "
    f"{f(CAP[e]['logements_menages'])} & {f(TR[e]['2040']['net'], 1, True)} \\\\" for e in ENVS)

# --- trajectoire
ans = [str(a) for a in range(2027, 2041)]
postes = [("taxe_fonciere_nouvelle", "Taxe foncière nouvelle"), ("dmto", "Droits de mutation"),
          ("calendrier_ventes", "Achats différés"), ("report_paiement", "Report de paiement"),
          ("deductibilite_is_ir", "Déductibilité"), ("net", "\\textbf{Net, 15 Md€}")]
sel = ["2027", "2028", "2029", "2030", "2031", "2032", "2033", "2035", "2040"]
head_tr = " & ".join(sel)
rows_tr = "\n".join(f"{lab} & " + " & ".join(f(TR['E15'][a][k], 1, True) for a in sel) + " \\\\" for k, lab in postes)
for e, lab in (("E10", "Net, 10 Md€"), ("E20", "Net, 20 Md€"), ("substitution", "Net, substitution"),
               ("E15_baisse_unique_2030", "Net, 15 Md€, baisse unique 2030"),
               ("E15_glissement_un_an", "Net, 15 Md€, un an de retard")):
    rows_tr += "\n" + f"{lab} & " + " & ".join(f(TR[e][a]['net'], 1, True) for a in sel) + " \\\\"
stock = J["indicateurs_annuels"]["E15"]
rows_tr += "\n" + "Stock de report (15 Md€) & " + " & ".join(f(stock[a]['stock_report'], 1) for a in sel) + " \\\\"
rows_tr += "\n" + "Taux des droits (\\%) & " + " & ".join(f(stock[a]['taux_dmto_pct'], 2) for a in sel) + " \\\\"

# --- cas-types
COURT = {'orleans': 'Orléans, app. 65 m²', 'lyon': 'Lyon, app. 80 m²', 'massy': 'Massy, app. 65 m²',
         'sgdb': 'Ste-Geneviève, maison 100 m²'}
rows_cas = "\n".join(
    f"{COURT[c['cle']]} & {f(c['prix'])} & {f(c['taux_2026'], 2)} & {f(c['dmto_2026'], -2 if False else 0)} & "
    f"{f(c['dmto_permanent'])} & {f(c['dmto_apres'])} & {f(c['tf_actuelle'])} & {f(c['dtf'], signe=True)} & "
    f"{f(c['dtf_10'], signe=True)} & {f(c['net_7ans'], signe=True)} & {f(c['perte_valeur_proprietaire'], signe=True)} \\\\"
    for c in CAS)

M = J["mobilite"]
g6 = J["g6"]
sig = D["cout_selon_sigma"]
tex = rf"""% Annexe du bloc « fiscalité immobilière » de la note de 8 pages (note8p/CADRE.md). Générée par
% note8p/calculs/foncier_annexe.py à partir de note8p/sorties/foncier.json (note8p/calculs/foncier_calculs.py, qui importe
% foncier/simulation.py). Compte rendu : note8p/sorties/foncier.md. Montants en Md€ de 2025, assiettes 2025 non indexées.

\subsection{{Données, champ et calibrage}}

Le modèle communal est celui de la note fusionnée (\texttt{{foncier/simulation.py}}, inchangé) : 30,5~millions de logements
des particuliers de métropole hors Alsace-Moselle ; valeur = prix médian au m² des ventes 2023-2024 de la commune × surface
médiane ; part du sol mesurée par les terrains à bâtir (maisons) ou par résidu (appartements), calée sur les comptes de
patrimoine des ménages (46,2~\% fin 2025) ; taxe foncière de 2025 (REI) répartie au prorata de la valeur dans chaque
commune. Les agrégats nationaux viennent des comptes de patrimoine de l'Insee (tableau 8.200, fin 2025) : biens privés
(sociétés non financières, sociétés financières, ménages, institutions sans but lucratif), hors terres agricoles et biens
publics. Sol : {f(A['sol'])}~Md€, dont {f(A['nu'])} de terrains non bâtis ; bâti (logements et bâtiments non résidentiels)
: {f(A['bati'])}~Md€.

\textbf{{Droits de mutation.}} Taux permanent de 5,807~\% : 4,50~\% pour le département (art.~1594~D CGI), 1,20~\% pour la
commune (art.~1584) et 2,37~\% de la part départementale de frais d'assiette (art.~1647~V). La majoration à 5~\% (loi
n°~2025-127, art.~116), dont les primo-accédants sont exclus, cesse le 31~mars 2028 ; la référence de la réforme est donc
le taux permanent. France entière, au taux permanent et sur les ventes de 2025, les droits valent {f(D['logements_fr'], 1)}~Md€
sur les logements et {f(D['autres_fr'], 1)}~Md€ sur les autres biens (différence OFGL moins Compte du logement, ramenée au
taux permanent), soit {f(D['total_fr'], 1)}~Md€ : la division par deux coûte \textbf{{{f(D['demi'], 2)}~Md€}}, contre
{f(D['ancien_calibrage'], 2)} dans l'ancien calibrage, limité au champ du modèle. Le coût suit le cycle :
{f(D['demi_2324'], 1)}~Md€ aux ventes moyennes de 2023-2024, 10,0~Md€ à celles de 2022. Un point de taux vaut
{f(D['cout_par_point'], 2)}~Md€.

\subsection{{Architecture et formules}}

Chaque bien $i$ a une base $b_i = S_i + B_i/4$ ($S$ : valeur du sol, bâti ou non ; $B$ : valeur du bâti). Il paie
$(t_c + t_n)\,b_i$ : le sol est taxé au taux $t$ et le bâti au taux $t/4$. Lors de la bascule, le taux communal
$t_c = \sum_{{i \in c}} \mathrm{{TF}}_i^0 / \sum_{{i \in c}} b_i$ garde la recette de chaque commune ; la commune le vote
ensuite librement, le rapport de 4 étant fixé par la loi. Le taux national uniforme $t_n$ lève l'enveloppe $E$ :
$t_n = E / \sum_i b_i$, la part des logements des ménages ({f(100*A['part_men_log'], 1)}~\% de la base) étant répartie
entre les logements du modèle au prorata de $b_i$.

\textbf{{Capitalisation.}} La valeur du sol est la rente nette capitalisée : $S = \rho/(r + \tau_S)$, où $\tau_S$ est
l'impôt sur le sol rapporté à sa valeur. Aujourd'hui, $\tau_S^0 = 0{{,}}358~\%$ (taxe / valeur des logements, appliquée à
tous les biens bâtis) et 0,08~\% pour les terrains non bâtis (hypothèse). Après la réforme, $\tau_S^1 = t_c + t_n$ ; le
taux communal monte pour garder la recette sur un sol moins cher. Le point fixe
$S^1 = S^0 (r+\tau_S^0)/(r+\tau_S^1)$, $t_n = E/(S^1 + B/4)$ est résolu numériquement avec $r = 3~\%$ (variante 4~\%), le
bâti restant à son coût. La perte de valeur des biens est la valeur actuelle de la hausse, $\Delta \mathrm{{TF}}_i / r$
(baisse des droits gardée par l'acheteur, cas central ; variante symétrique dans le tableau~\ref{{tab:fon8_env}}).

\begin{{table}}[!htbp]\centering\scriptsize
\caption{{Enveloppes de recette foncière nouvelle}}\label{{tab:fon8_env}}
\begin{{tabular}}{{@{{}}lrrrrrrrrr@{{}}}}
\toprule
Enveloppe & \multicolumn{{3}}{{c}}{{Taux national sur le sol (\%)}} & Baisse du & Recette au & Payé par & \multicolumn{{2}}{{c}}{{Perte de valeur (Md€)}} & Net \\
\cmidrule(lr){{2-4}}\cmidrule(lr){{8-9}}
(Md€) & statique & $r$ = 3 \% & $r$ = 4 \% & sol (\%) & taux statique & logements & tous & logements & 2040 \\
\midrule
{rows_env}
\bottomrule
\end{{tabular}}
\par\vspace{{2pt}}{{\raggedright\scriptsize Taux du bâti : un quart du taux du sol. « Recette au taux statique » : ce que
rapporterait le taux calculé sans capitalisation, une fois les valeurs ajustées. Perte de valeur à $r$ = 3~\% (4~\% : un
quart de moins). Si la baisse des droits se capitalise aussi, la perte nette de tous les propriétaires vaut
{f(CAP['E15']['symetrique'])}~Md€ pour 15~Md€. Sans les terrains non bâtis, tous les taux montent de {f(J['sens_sans_nus'])}~\%.\par}}
\end{{table}}

\subsection{{Résultats pour les logements}}

\begin{{table}}[!htbp]\centering\scriptsize
\caption{{Taxe foncière des logements par dixième de prix au m² de la commune}}\label{{tab:fon8_dec}}
\begin{{tabular}}{{@{{}}rrrrrrrrrr@{{}}}}
\toprule
 & Prix & Taxe/valeur & \multicolumn{{4}}{{c}}{{Variation de taxe (€/an ; \% pour 15)}} & Taxe $-$ droits & Taxe/valeur & Valeur \\
\cmidrule(lr){{4-7}}
Dixième & (€/m²) & 2025 (\%) & 10 & 15 & 15 (\%) & 20 & 15 (€/an) & 15 (\%) & 15 (\%) \\
\midrule
{rows_dec}
\bottomrule
\end{{tabular}}
\par\vspace{{2pt}}{{\raggedright\scriptsize Enveloppes de 10, 15 et 20~Md€ en régime permanent ; « taxe $-$ droits » :
hausse de taxe moins la baisse des droits rapportée à l'ensemble des logements de la commune ; valeur : perte de valeur
capitalisée ($r$ = 3~\%). Avec 15~Md€ : hausse médiane {f(LG['E15']['pctl']['50'], signe=True)}~€, 9\textsuperscript{{e}}
décile {f(LG['E15']['pctl']['90'], signe=True)}~€, 99\textsuperscript{{e}} centile {f(LG['E15']['pctl']['99'], signe=True)}~€ ;
{f(100*LG['E15']['plus300'])}~\% des logements au-delà de +300~€, {f(100*LG['E15']['plus600'])}~\% au-delà de +600~€ ;
baisse pour {f(100*LG['E15']['baisse'])}~\% ; Paris {f(LG['E15']['paris_pct'], signe=True)}~\% ; maisons
{f(LG['E15']['maisons'], signe=True)}~€, appartements {f(LG['E15']['apparts'], signe=True)}~€. Impôt sur le bâti des logements :
14,3~Md€ aujourd'hui, 7,3 avec la seule part communale à la nouvelle base, {f(LG['E15']['impot_bati'], 1)} avec 15~Md€.\par}}
\end{{table}}

\subsection{{Trajectoire 2027-2040}}

Calendrier (choix) : loi en 2027, valeurs de référence au 1\textsuperscript{{er}}~janvier 2028, premier avis à l'automne
2029 ; part nationale et passage de la part communale à la nouvelle base par tiers en 2029, 2030 et 2031 ; taux des droits
abaissé au 1\textsuperscript{{er}}~janvier des mêmes années. Une clause suspend chaque palier de baisse tant que le palier
de taxe n'est pas mis en recouvrement. Hypothèses : {f(100*H['phi'])}~\% des ventes annuelles décalées de décembre à
janvier par point de baisse annoncée (les +26~\% de ventes du mois précédant la hausse de 0,7~point de 2014 représentent
environ 2~\% des ventes de l'année, soit 3~\% par point) ; report ouvert aux propriétaires occupants modestes, qui doivent
{f(100*H['eligibles'])}~\% des hausses des occupants, utilisé par la moitié d'entre eux, avec un intérêt de 3~\% et un
remboursement de 1/15 du stock par an ; déductibilité l'année suivante au taux effectif de {f(100*H['deduction_is'])}~\% pour
la part des sociétés soumises à l'IS (hors HLM, {f(100*A['part_entr_is'], 1)}~\% de la base) et de
{f(100*H['deduction_bailleurs'])}~\% pour la hausse des bailleurs. Aucune reprise durable des ventes n'est comptée : à
6~\% de ventes par point, le coût des droits tomberait de {f(sig['0'], 1)} à {f(sig['6'], 1)}~Md€.

\begin{{table}}[!htbp]\centering\scriptsize
\caption{{Trajectoire budgétaire (Md€ ; + = recette publique)}}\label{{tab:fon8_traj}}
\begin{{tabular}}{{@{{}}l{'r' * len(sel)}@{{}}}}
\toprule
 & {head_tr} \\
\midrule
{rows_tr}
\bottomrule
\end{{tabular}}
\par\vspace{{2pt}}{{\raggedright\scriptsize Années 2034, 2036-2039 : voir \texttt{{note8p/sorties/foncier.json}}, table
\texttt{{annuel}} (15~Md€) et \texttt{{annuel\_par\_scenario}}. Le report est un prêt remboursable, compté ici en besoin de
financement net.\par}}
\end{{table}}

\subsection{{Cas-types}}

\begin{{table}}[!htbp]\centering\scriptsize
\caption{{Achats et taxe foncière (prix médian DVF au m² de la commune × surface)}}\label{{tab:fon8_cas}}
\setlength{{\tabcolsep}}{{3pt}}
\begin{{tabular}}{{@{{}}lrrrrrrrrrr@{{}}}}
\toprule
 & Prix & Taux & Droits & Droits & Droits & Taxe & \multicolumn{{2}}{{c}}{{Hausse (€/an)}} & Bilan & Perte du \\
\cmidrule(lr){{8-9}}
 & (€) & 2026 (\%) & 2026 & permanents & après & actuelle & 15 & 10 & 7 ans & vendeur \\
\midrule
{rows_cas}
\bottomrule
\end{{tabular}}
\par\vspace{{2pt}}{{\raggedright\scriptsize Orléans et Massy : primo-accédants (hors majoration) ; Lyon et
Sainte-Geneviève-des-Bois : autres acheteurs, à 6,32~\% jusqu'au 31~mars 2028 (tableau DGFiP au 1\textsuperscript{{er}}~juin
2026). Bilan à 7 ans : économie de droits moins valeur actuelle de sept ans de hausse, prix inchangés. Perte du vendeur :
hausse capitalisée à 3~\%, qui revient à l'acheteur sous forme d'un prix plus bas si la taxe se capitalise. Mobilité : une
famille qui quitte Orléans pour un poste en Essonne paie {f(M['droits_permanent'])}~€ de droits au taux permanent
({f(M['droits_2026'])} en 2026), {f(M['droits_apres'])}~€ après réforme, soit l'équivalent de {f(M['hausse_mensuelle_equiv_6ans_avant'])}~€
puis {f(M['hausse_mensuelle_equiv_6ans_apres'])}~€ d'augmentation nette par mois pendant six ans.\par}}
\end{{table}}

\subsection{{Gains, sensibilités et variantes écartées}}

\textbf{{Perte sèche}} (indicateur d'efficacité, triangle de Harberger, méthode de l'annexe de la note fusionnée). Ventes de
logements : {f(G['3']['perte_seche_ventes'], 2)}, {f(G['6']['perte_seche_ventes'], 2)} et {f(G['8']['perte_seche_ventes'], 2)}~Md€
pour 3, 6 et 8~\% de ventes en moins par point (soit +{f(G['3']['ventes_pct'])}, +{f(G['6']['ventes_pct'])} et
+{f(G['8']['ventes_pct'])}~\% de ventes durables) ; zéro si la réaction n'est que temporaire. Autres immeubles :
{f(G['autres_immeubles'], 2)}~Md€ (transposition). Bâti des logements (élasticité 1, coût d'usage 4,5~\%) :
{f(G['bati']['E10'], 2)}, {f(G['bati']['E15'], 2)} et {f(G['bati']['E20'], 2)}~Md€ pour 10, 15 et 20~Md€. Le sol ne crée
pas de perte sèche. Schéma g6 : un terrain de {f(g6['sol'])}~€ et un immeuble de {f(g6['bati'])}~€ ; au taux unique de
{f(g6['taux_unique'], 3)}~\%, construire ajoute {f(g6['unique_bati']-g6['unique_nu'])}~€ d'impôt par an ; avec
{f(g6['taux_sol'], 3)}~\% sur le sol et {f(g6['taux_bati'], 3)}~\% sur le bâti (même recette), {f(g6['double_bati']-g6['double_nu'])}~€,
et le terrain nu paie {f(g6['double_nu'])}~€ au lieu de {f(g6['unique_nu'])}.

\textbf{{Variantes écartées.}} \emph{{Substitution pure}} (8,1~Md€) : le solde est négatif ($-$0,8~Md€ par an) à cause de la
déductibilité, et rien ne finance l'IS. \emph{{Taux national sur le seul sol}} : il évite les 20~\% de la part nationale
qui portent sur le bâti, mais le rapport sol/bâti varierait alors entre communes et il faudrait deux bases dans l'avis.
\emph{{Baisse des droits en une fois}} (2030) : aucune année négative dans le calcul, mais une incitation à différer les
achats pendant plus de deux ans que l'hypothèse d'un mois de décalage ne capte pas. \emph{{Taux départemental}} : de 0,13
à 0,79~\% du sol selon le département (ancien calcul). \emph{{Suppression des droits}} : 16,2~Md€ ; orientation de long
terme seulement. \emph{{Baisse immédiate avant la taxe}} (ancienne trajectoire) : 8,1~Md€ de dette par année d'avance.

\textbf{{Expériences de référence.}} \emph{{Bade-Wurtemberg}} (Landesgrundsteuergesetz du 4/11/2020, modifié en 2023 et
le 18/11/2025) : valeur = surface × \emph{{Bodenrichtwert}} de la zone, fixé par les comités d'experts (§~38 al.~1-2) ;
preuve d'une valeur inférieure de plus de 30~\% par expertise (§~38 al.~4) ; taux légal de 1,30~pour mille, réduit de 30~\% pour
les terrains majoritairement résidentiels, de 25~\% pour le logement social, de 10~\% pour les monuments (§~40) ;
\emph{{Hebesatz}} unique par commune (§~50 al.~4), taux distinct possible sur les terrains constructibles non bâtis
(§~50a) ; valeurs au 1/1/2022, impôt dû en 2025 ; modèle validé par le Bundesfinanzhof (II~R~26/24 et II~R~27/24,
communiqué du 20/05/2026), recours constitutionnels pendants (source associative). \emph{{Pennsylvanie}} : rapports
municipaux sol/bâti de 1,4 à 17,5 dans 18 villes en 2000, dont Pittsburgh (1913-2001), Scranton (1913), Harrisburg (1975),
Allentown (1997) (Banzhaf et Lavery, 2010, tableau~2) ; comté et district scolaire taxent au taux unique. Oates et Schwab
(1997) : permis réels +70~\% à Pittsburgh entre 1960-79 et 1980-89 contre $-$14~\% en moyenne dans 15 villes, attribués
surtout à la pénurie de bureaux (comparaison avant-après, un seul traité). Plassmann et Tideman (2000) : effet positif
sur les permis dans 15 villes à deux taux contre 204 témoins, sensible à la spécification (résumé et thèse lus). Banzhaf
et Lavery (2010) : différences premières avec effets fixes par secteur de recensement ; +5 à 6 points de croissance
décennale du nombre de pièces, surtout par plus de logements ; environ +3 points (pièces) et +2 points (logements) pour un
rapport de 4 (version de travail de 2008). Pittsburgh a abandonné le double taux en 2001 après une réévaluation qui avait
relevé la valeur du sol de 81~\% (Hughes, 2006).

\textbf{{Limites.}} Taux uniforme de la valeur dans chaque commune (la dispersion réelle multiplie les perdants) ; valeurs
de l'Insee sans géographie pour les sociétés ; contenu des « autres terrains » ; droits sur les autres biens par
différence de deux sources ; paramètres du report et de la déductibilité supposés ; capitalisation complète supposée
(contestée par une étude danoise non publiée) ; premier avis en 2029 ambitieux (le Bade-Wurtemberg a mis plus de quatre
ans en partant de valeurs de zone existantes).
"""
OUT.write_text(tex, encoding="utf-8")
print("écrit", OUT)
