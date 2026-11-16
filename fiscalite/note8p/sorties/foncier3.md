# Bloc « fiscalité immobilière », version 3 : compte rendu pour l'assembleur

*Scripts : `note8p/calculs/foncier3_calculs.py` (→ `foncier3.json`, journal `foncier3_journal.txt`),
`foncier3_figures.py` (g4, g5, g6, g10 ; `--rec A_E15` pour changer le scénario figuré), `foncier3_annexe.py`
(→ `annexes/annexe_foncier.tex`). Le modèle communal (`foncier/simulation.py`) et le premier script du bloc
(`foncier_calculs.py`) sont importés sans modification. Md€ de 2025, assiettes 2025 non indexées, **années de caisse**.
Le calcul se paramètre en une ligne : `python3 note8p/calculs/foncier3_calculs.py --E 13.5 --archi B` affiche la table
annuelle de n'importe quelle enveloppe. Statuts : [E] empirique publié, [S] simulation, [H] hypothèse, [C] choix.*

## 1. Ce qui change

- **Enveloppe** : la baisse de l'IS étant abandonnée, rien ne justifie 15 Md€ par défaut. Cinq enveloppes de recette
  nationale nouvelle (9, 10, 12, 15, 18 Md€), deux architectures, toutes les tables annuelles dans `annuel_par_scenario`
  (clés `A_E9` … `B_E18`, plus `A_substitution` et `B_substitution`).
- **Architecture recommandée : B** (taxe communale à double taux + taxe nationale sur le seul sol, § 3).
- **Enveloppe recommandée : 12 Md€** si la réforme foncière finance seulement les droits et la transition (option a) ;
  **15 Md€** si le bouclage veut aussi financer une baisse de l'impôt sur le travail (option b, ≈ 2,7 Md€ de plus par an).
  18 Md€ n'est pas recommandé.
- **Capitalisation, nouvelle convention** [S] : la valeur des biens baisse de la valeur actuelle de l'impôt en plus,
  −(E − κ × 8,07)/r, et toute la baisse porte sur le sol (le bâti reste à son coût de remplacement, comme dans les
  comptes de patrimoine, où le sol est un résidu). La version précédente imputait aussi au sol le transfert communal du bâti
  vers le sol, sans contrepartie : ses taux étaient 5 % plus élevés.
- **Parcimonie** (consigne de l'auteur) : retirés le gain sur le nombre de ventes et la perte sèche évitée sur les ventes
  (réaction durable non établie en France), l'extrapolation de la mobilité des propriétaires (Pays-Bas → France), le
  triangle de Harberger sur le bâti (élasticité non calibrée), la variante de baisse unique en 2030. Restent la
  capitalisation (mécanisme standard, en ordre de grandeur) et trois paramètres de trajectoire signalés [H] (§ 5).

## 2. Les enveloppes (architecture B ; A entre parenthèses quand elle diffère)

| Recette nationale nouvelle (Md€) | 9 | 10 | **12** | 15 | 18 |
|---|---|---|---|---|---|
| Taux national sur le sol, après capitalisation | 0,142 % | 0,158 % | **0,192 %** | 0,244 % | 0,297 % |
| (A : taux sur sol + bâti/4) | (0,113 %) | (0,126 %) | (0,152 %) | (0,192 %) | (0,234 %) |
| Hausse moyenne par logement | +174 € | +193 € | **+232 €** (+240) | +290 € (+301) | +347 € (+361) |
| Médiane / 9e décile | +122 / +467 | +135 / +508 | **+162 / +592** (+189 / +542) | +201 / +718 | +241 / +846 |
| Logements à plus de +300 € / +600 € | 21 / 6 % | 24 / 7 % | **29 / 10 %** (30 / 8 %) | 38 / 14 % | 43 / 20 % |
| Logements dont la taxe baisse | 10 % | 10 % | **9 %** (6 %) | 8 % | 7 % |
| Paris : ensemble ; appartement médian | +111 % ; +611 € | +123 % ; +677 € | **+148 % ; +811 €** (+125 % ; +682 €) | +185 % ; +1 011 € | +222 % ; +1 211 € |
| Perte de valeur, tous biens (r = 3 % ; 4 %), Md€ | 300 ; 225 | 333 ; 250 | **400 ; 300** | 500 ; 375 | 600 ; 450 |
| dont logements des ménages (% de leur valeur) | 2,1 % | 2,3 % | **2,8 %** | 3,5 % | 4,2 % |
| Net 2029 / 2030 / 2031 | +0,2 / +0,1 / +0,3 | +0,5 / +0,7 / +1,2 | **+1,1 / +2,0 / +3,0** | +2,1 / +3,8 / +5,8 | +3,1 / +5,7 / +8,5 |
| Net en régime permanent (2040) | 0,0 | +0,9 | **+2,7** | +5,4 | +8,1 |

[S] Chaque milliard d'enveloppe rapporte 0,90 Md€ net (déductibilité). 9 Md€ ne fait que financer les droits et la
transition (net ≈ 0, −0,1 en 2032) ; la seule substitution aux droits (8,1 Md€) laisse un trou de 0,8 Md€ par an. Les
impôts périodiques sur l'immobilier passeraient de 1,9 % du PIB à environ 2,3 % avec 12 Md€ (2,4 % avec 15) (moyenne de l'OCDE 0,95 %,
Royaume-Uni 2,8 % ; OCDE, 2023, déjà cité dans la version précédente).

**Option (a), hausse modérée : 12 Md€.** Elle couvre la baisse des droits (8,1), le report et la déductibilité, et laisse
1 à 3 Md€ par an pour la transition de l'IS. Or le calendrier ne colle pas : le coût net de l'IS (fin du taux réduit moins
déduction de 50 %, en caisse, `is.json`) vaut −2,4 Md€ en 2028 et −4,0 en 2029, quand la taxe n'a pas encore produit ou
n'en est qu'au premier tiers. Foncier + IS : 2028 −2,8 ; 2029 −2,9 ; 2030 −0,6 ; 2031 +1,7 ; 2035 +4,9 ; 2040 +5,6
(table `foncier_plus_is_caisse`). **Aucune enveloppe ne finance l'IS en 2028-2029** (même 18 Md€ laisse −0,9 en 2029) :
l'assembleur doit soit décaler la déduction d'un ou deux ans, soit la financer ailleurs. Le foncier ne peut pas avancer :
premier avis à l'automne 2029 au plus tôt.

**Option (b), hausse ambitieuse : 15 Md€.** ≈ +5,4 Md€ par an en régime permanent, dont ≈ 2,7 de plus que (a) pour le
travail ; Foncier + IS ≥ +1,3 dès 2030. 18 Md€ dégage +8,1 Md€, mais 20 % des logements prendraient plus de 600 € par an
et l'appartement parisien médian 1 200 € : le coût politique croît plus vite que la recette. **Recommandation : 12 Md€ ;
15 si le bloc IR-CSG a besoin de 2 à 3 Md€ pour les bas salaires ; pas 18.** Le choix est celui du bouclage : chaque
enveloppe a sa table annuelle.

## 3. Deux architectures : recommandation B

La part communale est la même : base sol + bâti/4, taux voté par la commune (recette inchangée à la bascule). La
différence est la part nationale : **A** l'applique à la même base (un seul montant par bien) ; **B** l'applique au seul sol
(deux lignes sur l'avis).

| Critère (12 Md€) | A : base unique | **B : double taux + national sur le sol** |
|---|---|---|
| Part de la recette nationale qui porte sur le bâti | 20 % | **0** |
| Impôt sur le bâti des logements (champ ; 14,3 Md€ aujourd'hui) | 9,0 Md€ | **7,3 Md€** |
| Impôt dû pour avoir construit un immeuble de 600 000 € (g6) | 1 090 €/an | **860 €/an** (2 150 aujourd'hui) |
| Détention d'un terrain nu de 200 000 € | 1 450 €/an | 1 530 €/an (720 aujourd'hui) |
| Rapport effectif taux du sol / taux du bâti | 4 partout | 4,6 (P10), 5,2 (médiane), 6,8 (P90), 10 à Paris |
| Hausse dans le 1er / le 10e dixième de prix | +46 / +620 € | **+20 / +693 €** |
| 9e décile de la hausse ; > 600 € | +542 € ; 8 % | +592 € ; 10 % |
| Logements dont la taxe baisse | 6 % | 9 % |
| Perte de valeur : 5e centile ; logements > 5 % | −6,4 % ; 23 % | −6,9 % ; 25 % |
| Recette payée par les logements des ménages / terrains nus / sociétés | 64,5 / 6,8 / 29,3 % | 62,1 / 8,5 / 30,3 % |

**Pourquoi B** [C]. (1) La nouvelle fiscalité ne touche pas du tout le bâti : la hausse nette porte sur la rente, ce qui est
la doctrine du projet ; les bureaux, entrepôts et usines des entreprises ne paient rien de plus. (2) L'incitation à
construire est plus forte : l'immeuble ajoute 860 € d'impôt au lieu de 1 090 (A) et 2 150 aujourd'hui. (3) La simplicité
administrative est la même : l'administration doit séparer sol et bâti dans les deux cas, puisque la part communale porte
sur sol + bâti/4 ; deux lignes sur un avis ne coûtent rien. B a même un avantage : la part nationale ne dépend que des
valeurs du sol (comme au Bade-Wurtemberg) et peut être émise même si le barème du bâti prend du retard. (4) La hausse se
concentre là où le sol est cher : moins dans les communes bon marché (+20 € dans le premier dixième contre +46), plus à
Paris et dans le dixième le plus cher.

**Inconvénients de B, réels mais pas sérieux.** Les perdants sont un peu plus concentrés (9e décile +592 € contre +542 ;
Paris +811 € contre +682 € pour l'appartement médian) ; le rapport sol/bâti varie d'une commune à l'autre (5 en médiane,
10 à Paris, où le taux communal est bas), ce qui n'a pas d'inconvénient économique (plus le rapport est élevé, plus
l'impôt est neutre) ; les terrains nus (jardins, terrains à bâtir, espaces naturels, contenu mal connu) paient un peu plus.
Juridiquement, une taxe nationale sur la seule valeur du sol est un impôt distinct, à l'assiette homogène : pas d'obstacle
identifié, mais pas d'expertise constitutionnelle faite. **Recommandation : B.**

## 4. Capitalisation : ordres de grandeur, pas des prévisions

Mécanisme standard [S] : une hausse permanente d'impôt de E par an réduit la valeur des biens de E/r ; si la baisse des
droits (8,07 Md€ par an) se capitalise aussi pour une part κ, la perte nette est (E − κ × 8,07)/r. Hypothèses : r constant,
capitalisation complète de la taxe, aucune réaction de l'offre ni des loyers. La littérature trouve une capitalisation
forte (Høj, Jørgensen et Schou, 2018, Danemark ; Koster et Pinchbeck, 2022, r de 3 à 4 % en Angleterre) ; celle des droits
de mutation est moins documentée.

| Perte de valeur, tous biens privés (Md€) | κ = 0 | κ = 50 % | κ = 100 % |
|---|---|---|---|
| 12 Md€, r = 3 % ; r = 4 % | **400 ; 300** | 265 ; 199 | 131 ; 98 |
| 15 Md€, r = 3 % ; r = 4 % | 500 ; 375 | 365 ; 274 | 231 ; 173 |
| 9 Md€, r = 3 % | 300 | 165 | 31 |
| 18 Md€, r = 3 % | 600 | 465 | 331 |

À 12 Md€ (κ = 0, r = 3 %), la perte vaut 6,0 % du sol privé et 2,8 % de la valeur des logements des ménages (0,3 % si κ =
100 %). **Repère** : de fin 2022 à fin 2025, le sol bâti de toute l'économie a perdu 881 Md€ dans les comptes de patrimoine
(g10), sans tension bancaire visible (ACPR, 2026 : encours douteux de niveau 3 à 1,2 % fin 2025). Le propriétaire en place
perd à l'annonce ; l'acheteur suivant achète moins cher et la taxe lui est neutre.

**Conséquences possibles** (brèves ; [E] pour les estimations publiées, [S] pour nos produits) :
- *Consommation.* La propension marginale à consommer le patrimoine immobilier est faible en France : 0,7 centime par euro
  (1,4 en bas de la distribution du patrimoine, 0,8 en haut ; Arrondel, Lamarche et Savignac, 2015, Banque de France DT 552,
  Enquête Patrimoine 2010, coupe transversale, pas un effet causal). Appliquée à la perte des ménages à 12 Md€ (249 Md€,
  κ = 0) : **1,7 à 3,5 Md€ de consommation en moins par an**, 0,2 à 0,4 si κ = 100 %, avant recyclage de la recette (baisse
  des droits, de l'impôt sur le travail). Chauvin et Muellbauer (2018, *Économie et Statistique* 500-502, modèle
  macroéconomique 1981-2016) trouvent un effet de richesse immobilière agrégé faible en France, faute de crédit hypothécaire
  rechargeable, et des prix plus élevés relativement aux revenus qui *réduisent* la consommation (les locataires et futurs
  accédants épargnent davantage) : une baisse des prix n'est donc pas forcément récessive. Les 5 à 7 centimes estimés aux
  États-Unis (Mian, Rao et Sufi, 2013, *QJE* 128(4)) ne sont pas transposables.
- *Crédit immobilier.* L'octroi repose sur la solvabilité (taux d'effort plafonné par le HCSF) plutôt que sur la valeur du
  bien ; 99,6 % de la production est à taux fixe (ACPR, *Le financement de l'habitat en 2025*, AS n° 183, 2026). Des prix plus
  bas réduisent les montants empruntés ; la baisse des droits réduit l'apport à financer.
- *Garanties bancaires.* 97,4 % de l'encours est garanti, dont 66,9 % par caution et 26 % par hypothèque ; la LTV moyenne en
  cours de vie est de 67,5 % (ACPR, 2026). Une baisse de 3 à 6 % des prix la relève de 2 à 4 points : la perte en cas de
  défaut augmente un peu sur la minorité hypothécaire, pas la probabilité de défaut.
- *Fonds propres négatifs.* 17,5 % des prêts accordés en 2025 dépassent la valeur du bien (LTV > 100 %, droits financés à
  crédit ; ACPR, 2026) : ces ménages sont en fonds propres négatifs dès l'achat, et une baisse de 3 à 6 % prolonge cette
  situation d'un à deux ans d'amortissement [S, ordre de grandeur]. Cela ne pèse qu'en cas de revente forcée (mutation,
  séparation), sans appel de marge à taux fixe. Les acheteurs de 2027-2028, qui paient encore les droits pleins, sont les
  plus exposés : un argument pour ne pas retarder la synchronisation.

## 5. Trajectoire (B, 12 Md€ ; Md€ ; + = recette ; caisse) — `annuel_par_scenario["B_E12"]`

| | 2027 | 2028 | 2029 | 2030 | 2031 | 2032 | 2035 | 2040 |
|---|---|---|---|---|---|---|---|---|
| Taxe foncière nouvelle | 0 | 0 | +4,0 | +8,0 | +12,0 | +12,0 | +12,0 | +12,0 |
| Droits de mutation | 0 | 0 | −2,7 | −5,4 | −8,1 | −8,1 | −8,1 | −8,1 |
| Achats différés | 0 | −0,5 | 0 | 0 | +0,2 | 0 | 0 | 0 |
| Report de paiement | 0 | 0 | −0,2 | −0,3 | −0,4 | −0,4 | −0,3 | −0,2 |
| Déductibilité (N+1) | 0 | 0 | 0 | −0,3 | −0,7 | −1,0 | −1,0 | −1,0 |
| **Net** | **0** | **−0,5** | **+1,1** | **+2,0** | **+3,0** | **+2,5** | **+2,6** | **+2,7** |

- **Calendrier** [C] : loi 2027 ; premier avis à l'automne 2029 ; part nationale par tiers (2029, 2030, 2031) ; taux des
  droits 5,81 → 4,84 → 3,87 → 2,90 % au 1er janvier des mêmes années ; **clause de suspension** : chaque palier de baisse
  ne s'applique que si le palier de taxe correspondant est mis en recouvrement la même année. Un an de retard des valeurs
  décale tout d'un an, sans coût.
- **Trois paramètres [H]**, gardés parce qu'ils sont des coûts de caisse certains dans leur principe : achats différés de
  décembre 2028 à janvier 2029 (3 % des ventes par point de baisse annoncée, calé sur les +26 % de ventes le mois précédant
  la hausse de 2014, Bérard et Trannoy, 2018 ; décalage récupéré l'année suivante) ; report de paiement (25 % des hausses
  des propriétaires occupants dues par des éligibles, recours de moitié : provision prudente, les reports facultatifs étant
  très peu utilisés aux États-Unis) ; déductibilité (droit en vigueur ; 20 % pour les sociétés à l'IS hors HLM, 25 % pour la
  hausse des bailleurs). Ce sont les seules hypothèses non mécaniques de la table.

## 6. Cas-types (B, 12 Md€ ; A et B 15 entre parenthèses)

| Projet (g5) | Prix | Droits 5,81 % → 2,90 % | Économie | Taxe foncière, +€/an | Équivalent |
|---|---|---|---|---|---|
| Orléans, appartement 65 m² | 170 000 | 9 870 → 4 940 | 4 940 | **+243** (A 12 : +253 ; B 15 : +285) | 20 ans |
| Lyon, appartement 80 m² | 372 000 | 21 600 → 10 800 | 10 800 | **+595** (+536 ; +739) | 18 ans |
| Massy, appartement 65 m² | 269 000 | 15 620 → 7 810 | 7 810 | **+419** (+386 ; +518) | 19 ans |
| Ste-Geneviève-des-Bois, maison 100 m² | 365 000 | 21 190 → 10 600 | 10 600 | **+466** (+452 ; +579) | 23 ans |

**Le jeune couple à Massy.** Primo-accédants, 269 000 € pour 65 m² ; droits de 15 620 € (5,81 %, primo-accédants exonérés
de la majoration ; 17 000 € pour un autre acheteur jusqu'au 31/3/2028). Après réforme : 7 810 €. Leur taxe foncière (925 €)
augmente de **+419 €/an** en régime permanent, atteints par paliers de 140 €. S'ils revendent après sept ans, prix
inchangés, ils restent gagnants de 5 200 € ; l'économie vaut 19 ans de hausse. Si la hausse se capitalise, ils achètent
14 000 € moins cher et la taxe leur est neutre ; le vendeur supporte la perte.

**La famille qui suit un emploi.** Elle vend sa maison d'Orléans (270 000 €) pour un poste en Essonne et achète à
Sainte-Geneviève-des-Bois (365 000 €) : 23 060 € de droits en 2026 (6,32 %), 21 190 € au taux permanent, **10 600 €**
après réforme. Pour payer les seuls droits, il faut aujourd'hui une augmentation nette de 294 € par mois pendant six ans ;
après réforme, 147 €. Sa nouvelle taxe foncière augmente de +466 €/an.

**Perdants** [S] : les propriétaires qui ne vendent pas là où le sol est cher. Appartement parisien médian +811 €/an
(+148 % pour Paris) ; dixième le plus cher +693 €/an et −5,0 % de valeur. Rapportée à la valeur, la taxe passe de 0,54 à
0,56 % dans les communes les moins chères et de 0,18 à 0,33 % dans les plus chères (g4) : l'écart se resserre sans
s'inverser.

## 7. Figures : titres-messages proposés

- **g4_taxe_valeur** : « Rapportée à la valeur, la taxe foncière ne monte guère dans les communes bon marché et double
  presque dans les plus chères ».
- **g5_achats** : « Diviser les droits par deux fait économiser de 5 000 à 11 000 € à l'achat, contre 240 à 600 € de taxe
  foncière en plus par an ».
- **g6_sol_bati** : « Avec une part nationale sur le seul sol, construire un immeuble coûte 860 € d'impôt par an, contre
  2 150 € aujourd'hui ».
- **g10_foncier_pib** : « La valeur du sol bâti est passée d'environ la moitié du PIB à la fin des années 1990 à plus de
  deux fois le PIB » (53 % en 1998, 276 % en 2007, 298 % en 2022, 235 % en 2025 ; ménages 33 % → 138 %). Données Insee
  déjà dans le dépôt (`foncier/donnees/patrimoine_2025.csv`, comptes de patrimoine millésime 2026), figure refaite à la
  charte.

## 8. Limites qui peuvent changer la conclusion

1. **Gains économiques non chiffrés** : sans réaction durable établie des ventes en France (nulle au-delà de trois mois
   selon Bérard et Trannoy, 2018), la réforme se défend par la base (rente plutôt que bâti), par le coût d'un déménagement
   (12 900 € → 6 400 € pour un logement de 222 000 €) et par l'effet du double taux sur la construction (Banzhaf et Lavery,
   2010, *JUE* : +2 points de logements par décennie pour un rapport de 4, petites villes de Pennsylvanie).
2. **Capitalisation** : ordre de grandeur ; si les prix ne bougent pas (Nielsson et al., 2024, document de travail
   danois), la recette est plus forte et la perte patrimoniale plus faible.
3. **Assiette** : valeurs du sol des sociétés sans géographie ; terrains non bâtis mal connus (sans eux, taux +7 %).
4. **Dispersion** : même taux de la valeur pour tous les logements d'une commune ; les perdants réels seront plus nombreux.
5. **Calendrier** : un premier avis en 2029 est ambitieux ; la clause protège le budget, pas le calendrier. Le décalage
   avec la transition de l'IS (2028-2029) est à régler au bouclage.

## 9. Références vérifiées (nouvelles dans cette version)

- Arrondel, Lamarche et Savignac (2015), « Wealth Effects on Consumption across the Wealth Distribution: Empirical
  Evidence », Banque de France DT 552 (= BCE WP 1817), texte lu : PMC du patrimoine net ≈ 0,006 ; immobilier 1,4 → 0,8
  centime du bas au haut de la distribution ; 58,9 % des ménages endettés pour leur résidence principale sans hypothèque
  (2010).
- Chauvin et Muellbauer (2018), « Consumption, household portfolios and the housing market in France », *Économie et
  Statistique* 500-502, 157-178 (synthèse Insee lue).
- Mian, Rao et Sufi (2013), « Household Balance Sheets, Consumption, and the Economic Slump », *QJE* 128(4), 1687-1726
  (résumé : 5 à 7 centimes par dollar de patrimoine immobilier perdu).
- ACPR (2026), « Le financement de l'habitat en 2025 », Analyses et synthèses n° 183 (lu) : LTV moyenne à l'octroi 79,9 %,
  LTV > 100 % 17,5 %, LTV en cours de vie 67,5 %, encours garanti 97,4 % (caution 66,9 %, hypothèque 26 %), taux fixe 99,6 %
  de la production, encours de niveau 3 1,2 %.
- Insee, comptes de patrimoine base 2020, tableau 8.200, millésime 2026 (déjà dans le dépôt).
- Les autres références (droits de mutation, Bade-Wurtemberg, Pennsylvanie, transactions, mobilité, capitalisation) sont
  celles de `sorties/foncier.md`, § 11, inchangées.
