# Bloc « fiscalité immobilière » : compte rendu pour l'assembleur

*16/11/2026. Scripts : `note8p/calculs/foncier_calculs.py` (chiffres → `foncier.json`, journal `foncier_journal.txt`) et
`foncier_figures.py` (g4, g5, g6), `foncier_annexe.py` (annexe LaTeX générée depuis le JSON). Le modèle communal de `foncier/simulation.py` est importé tel quel (logements des
particuliers, métropole hors Alsace-Moselle, DVF 2023-2024 pour les prix, REI 2025, comptes de patrimoine fin 2025).
Montants en Md€ de 2025, assiettes de 2025 non indexées. Statuts : [E] empirique publié, [S] simulation, [H] hypothèse,
[C] choix de politique.*

## 1. La proposition en cinq lignes

- **Droits de mutation divisés par deux** [C] : de 5,81 % à 2,90 % du prix (taux permanent ; 4,50 % département,
  1,20 % commune, frais d'assiette de l'État). Coût : **8,1 Md€** France entière sur les ventes de 2025 [S]. L'ancien
  chiffre de 7,6 Md€ portait sur le champ du modèle (métropole hors Alsace-Moselle, 94 % des droits) : il sous-estimait
  le coût. À terme, une suppression complète pourrait être envisagée selon le marché, les résultats et le financement. Elle
  ne fait pas partie du scénario central.
- **Une seule taxe foncière, une seule base, deux taux** [C] : base de chaque bien = valeur du sol + ¼ de la valeur du
  bâti. Le sol, bâti ou non, est donc taxé quatre fois plus que le bâti. Le montant dû est le taux communal voté
  (recette communale inchangée lors de la bascule) plus un **taux national uniforme**. Aucune exonération des terrains
  construits, aucune taxe sur les seuls terrains nus.
- **Hausse nette** [C] : recette nationale nouvelle de 10, 15 ou 20 Md€, à choisir au bouclage. **Recommandation :
  15 Md€**, soit environ 0,20 % de la valeur du sol (0,05 % du bâti) une fois la capitalisation passée. Après la baisse des
  droits, le report de paiement et la déductibilité, il reste **≈ 5,3 Md€ par an** pour d'autres baisses, dont celle de
  l'IS.
- **Synchronisation** [C] : loi en 2027, premier avis à l'automne 2029. La part nationale monte par tiers en 2029, 2030
  et 2031. Le taux des droits baisse le 1er janvier des mêmes années : 5,81 → 4,84 → 3,87 → 2,90 %. Une clause suspend
  chaque palier de baisse tant que le palier de taxe correspondant n'est pas mis en recouvrement.
- **Pertes patrimoniales assumées, liquidité traitée** [C] : pas de compensation. Les propriétaires occupants modestes
  peuvent reporter la hausse, avec intérêt au taux de l'État, garanti sur le bien et remboursé à la vente ou à la
  succession. Le besoin de financement du report est compté chaque année.

## 2. Pourquoi les droits sont un mauvais impôt, et ce qu'on peut attendre de leur baisse

Les droits ne frappent que ceux qui changent de logement. Un couple qui attend un enfant, une famille qui suit un emploi,
un retraité qui prendrait plus petit paient 5,8 % du prix à chaque achat, alors que le propriétaire qui ne bouge pas ne
paie rien. Sur un logement de 222 000 € (valeur moyenne du parc du modèle), cela fait **12 900 €** par achat, et
**6 400 €** après réforme : c'est l'indicateur « coût d'un déménagement » [S]. Le rendement suit en plus le cycle : les
droits sur les logements sont passés de 16,8 Md€ en 2022 à 11,2 Md€ en 2024 (Compte du logement).

- **Transactions : une réaction temporaire certaine, une réaction durable incertaine.** [E] Les effets de calendrier sont
  massifs et établis : +26 % de ventes le mois qui précède la hausse française de 2014 (Bérard et Trannoy, 2018),
  +41 % puis −42 % en Allemagne (Fritzsche et Vandrei, 2019). Ce sont des déplacements, pas des gains. L'effet durable est
  disputé. En France, il est nul au-delà de trois mois selon Bérard et Trannoy, et d'environ −10 % dans les seuls marchés
  détendus selon Bachelet et Poulhès (2017). Il atteint −15 % en sept mois pour 1,1 point à Toronto (Dachis, Duranton et
  Turner, 2012) et −7 % par point en Allemagne. Dolls et al. (2025) ne trouvent en revanche aucun effet significatif sur
  le nombre de ventes allemandes. Avec 0, 3, 6 ou 8 % de ventes par point, la baisse de 2,9 points ajoute
  durablement 0, 9, 18 ou 25 % de ventes (jusqu'à environ 220 000 par an) [S]. **La trajectoire ne compte aucune
  reprise.** Celle-ci réduirait le coût des droits de 8,1 à 6,6 Md€ (σ = 6).
- **Mobilité : établie pour les déménagements résidentiels, pas pour l'emploi.** [E] En Finlande, +0,5 point réduit de
  5,6 % la mobilité des propriétaires, et surtout les agrandissements ; les réductions de taille ne bougent pas, et l'effet
  net sur les changements d'emploi n'est pas clair (Eerola et al., 2021, *JUE*). Au Royaume-Uni, +2 points réduisent la
  mobilité annuelle de 2,6 points, sans effet sur les déménagements liés à l'emploi ni sur les longues distances
  (Hilber et Lyytikäinen, 2017, *JUE*). Aux Pays-Bas, la mobilité de propriétaire à propriétaire baisse d'au moins 8 %
  par point de coûts de transaction (van Ommeren et van Leuvensteijn, 2005). **Aucune estimation causale française.**
  On ne chiffre donc ni emploi ni appariement. On peut dire que la baisse rend le changement de logement moins cher pour les
  familles, sans prétendre qu'elle améliore mesurablement l'emploi.
- **Construction : des canaux plausibles, pas de preuve.** Le neuf et les terrains à bâtir vendus sous TVA paient déjà un
  droit réduit (art. 1594 F quinquies A CGI, taux non relu ici) : la baisse ne touche donc pas directement la
  construction. Les canaux indirects sont plausibles : chaînes de ventes (vendre l'ancien pour acheter le neuf),
  acquisition d'immeubles anciens pour les diviser, rénover ou démolir-reconstruire, remembrement de parcelles. Aucune
  étude ne les chiffre. L'argument « construction » repose plutôt sur le double taux (§ 3).

## 3. L'architecture : une taxe, une base, deux taux

**Simplification** [C]. L'ancienne architecture superposait un taux national sur le seul sol et une part communale à deux
taux. On garde désormais une base unique par bien (sol + bâti/4), sur laquelle s'additionnent le taux communal et le taux
national, comme aujourd'hui les taux communal et intercommunal sur la même valeur locative. Il n'y a qu'une évaluation,
qu'un avis et qu'un rôle. Le rapport de 4 est le même partout.

- *Prix de la simplicité* : 20 % de la base pondérée est du bâti, donc 20 % de la part nationale porte sur les
  constructions. Avec 15 Md€, l'impôt sur le bâti des logements passe malgré tout de 14,3 à 9,4 Md€, et non à 7,3 avec
  la seule part communale [S]. Un taux national sur le seul sol éviterait ces 3 Md€ sur le bâti, mais le rapport entre sol
  et bâti varierait alors d'une commune à l'autre. Variante non retenue.
- *Pourquoi un taux national* : les pertes de droits sont surtout départementales, et les départements n'ont plus de taxe
  foncière depuis 2021. Un taux départemental devrait atteindre 0,79 % du sol dans la Creuse contre 0,13 % à Paris
  (ancien calcul). La part nationale compense d'abord départements et communes pour leurs droits perdus ; le reste va à
  l'État.
- *Évaluation* [C] : la DGFiP publie, par zone, une valeur du sol au m² tirée des ventes (DVF) et l'applique à la surface
  cadastrale, sur le modèle des *Bodenrichtwerte*. Une valeur de zone surévaluée de plus de 30 % peut être contestée par
  expertise. Le bâti est évalué forfaitairement : surface × barème national au m² par type, avec abattement d'ancienneté.
  Les valeurs sont révisées tous les trois ans, jamais à la vente. Les locaux professionnels suivent la même base (point
  administratif à instruire).
- **Bade-Wurtemberg** [E, textes lus]. Depuis 2025, l'impôt foncier (*Grundsteuer B*) y vaut surface du terrain ×
  *Bodenrichtwert* de la zone (§ 38 al. 1 LGrStG), sans regard au bâti. Les valeurs de zone sont fixées par les comités
  d'experts (§ 196 BauGB). Le contribuable peut prouver par expertise une valeur inférieure de plus de 30 % (§ 38 al. 4,
  exposé des motifs de la loi du 18/11/2025). Le taux légal de 1,30 ‰ est réduit de 30 % pour les terrains
  majoritairement résidentiels, de 25 % pour le logement social et de 10 % pour les monuments (§ 40). Le taux communal
  (*Hebesatz*) est unique par commune (§ 50 al. 4), sauf un taux distinct possible sur les terrains constructibles non
  bâtis (« Grundsteuer C », § 50a). Les valeurs ont été arrêtées au 1/1/2022 pour un impôt dû en 2025, soit plus de quatre
  ans après la loi de novembre 2020. Le Bundesfinanzhof a validé le modèle (II R 26/24 et II R 27/24, communiqué du
  20/05/2026). Des recours constitutionnels sont pendants selon le Bund der Steuerzahler (source associative). À
  Karlsruhe, à recette constante, les maisons individuelles paient 76 % de plus et les copropriétés 20 % de moins (calcul
  de la ville, 2024). C'est la référence pour **évaluer le sol en masse**. Ce n'est pas un double taux : le bâti n'y est
  pas taxé.
- **Pennsylvanie** [E]. C'est la référence pour le **double taux**. Pittsburgh l'a appliqué de 1913 à 2001, avec un
  rapport municipal de 2 à 5,8 ; Scranton depuis 1913, Harrisburg depuis 1975, Allentown depuis 1997 (Banzhaf et Lavery,
  tableau 2). Le comté et le district scolaire taxent sol et bâti au même taux : à Pittsburgh, le rapport tous niveaux
  confondus restait à peine supérieur à 2. Les résultats empiriques :
  - Oates et Schwab (1997, *NTJ* 50(1)) : les permis réels de Pittsburgh augmentent de 70 % de 1960-79 à 1980-89, contre
    −14 % en moyenne dans 15 villes de la Rust Belt. Les auteurs attribuent l'essor à la pénurie de bureaux et au
    programme Renaissance II ; l'impôt foncier a joué un « supporting role ». C'est une comparaison avant-après sur une
    seule ville, sans effet causal propre.
  - Plassmann et Tideman (2000, *JUE* 47(2)) : 15 villes à deux taux contre 204 à taux unique, 1972-1994. Effet positif
    significatif sur le nombre de permis, non significatif dans une autre spécification de la thèse (résumé seulement).
  - Banzhaf et Lavery (2010, *JUE* 67(2)) : secteurs de recensement, différences premières avec effets fixes. Le nombre
    de pièces croît de 5 à 6 points de plus par décennie, surtout par davantage de logements. Rapporté au rapport des taux,
    un rapport de 4 donne environ +3 points pour les pièces et +2 points pour les logements (version de travail 2008 lue ;
    l'article publié confirme le sens sans chiffre dans le résumé).
  - Limites : petites villes en déclin, taux municipaux seulement, évaluations souvent anciennes. Pittsburgh a abandonné
    le double taux en 2001 après une réévaluation brutale du sol (+81 %, Hughes, 2006).

## 4. Les enveloppes

| Enveloppe (recette nationale) | 8,1 (substitution) | 10 | **15** | 20 |
|---|---|---|---|---|
| Taux national sur le sol, après capitalisation (bâti = ¼) | 0,106 % | 0,132 % | **0,201 %** | 0,272 % |
| Idem sans capitalisation | 0,097 % | 0,121 % | 0,181 % | 0,241 % |
| Baisse de la valeur du sol (r = 3 %) | −9,8 % | −10,6 % | −12,4 % | −14,3 % |
| Payé par les logements des ménages (Md€) | 5,2 | 6,5 | **9,7** | 12,9 |
| Hausse moyenne de taxe par logement | +162 € (+20 %) | +200 € (+25 %) | **+301 € (+38 %)** | +401 € (+50 %) |
| Hausse médiane / 9e décile / 99e centile | +128 / +388 / +592 € | +158 / +461 / +707 € | **+237 / +655 / +975 €** | +315 / +858 / +1 278 € |
| Logements à plus de +300 €/an | 17 % | 23 % | **40 %** | 52 % |
| Paris (moyenne ; appartement médian) | +84 % ; +462 € | +104 % ; +570 € | **+156 % ; +850 €** | +208 % ; +1 130 € |
| Perte de valeur, tous propriétaires (r = 3 % ; 4 %) | 269 ; 202 Md€ | 333 ; 250 | **500 ; 375** | 667 ; 500 |
| dont logements des ménages (% de leur valeur) | 1,9 % | 2,4 % | **3,6 %** | 4,8 % |
| Net disponible en régime permanent (2040) | −0,8 | +1,0 | **+5,5** | +10,0 |

[S] Note de lecture : la capitalisation réduit l'assiette. Au taux calculé sans elle, la recette serait plus faible de 8 à
11 %. Le taux légal doit donc être calé après capitalisation. La simple substitution laisse un solde négatif (−0,8 Md€),
parce que la taxe des entreprises et des bailleurs est déductible. Chaque milliard d'enveloppe en plus rapporte
0,90 Md€ net. **Recommandation : 15 Md€.** C'est la plus petite enveloppe qui dégage un montant utile pour l'IS (≈ 5 Md€).
Les impôts périodiques sur l'immobilier passeraient de 1,9 % à environ 2,4 % du PIB, entre la moyenne de l'OCDE (0,95 %)
et le Royaume-Uni (2,8 %) (OCDE, 2023). 10 Md€ ne libère presque rien. 20 Md€ porte la hausse au-delà de 600 € pour 22 %
des logements.

## 5. Trajectoire recommandée (15 Md€, trois paliers ; Md€, + = recette) — table `annuel` du JSON

| | 2027 | 2028 | 2029 | 2030 | 2031 | 2032 | 2035 | 2040 |
|---|---|---|---|---|---|---|---|---|
| Taxe foncière nouvelle | 0 | 0 | +5,0 | +10,0 | +15,0 | +15,0 | +15,0 | +15,0 |
| Droits de mutation | 0 | 0 | −2,7 | −5,4 | −8,1 | −8,1 | −8,1 | −8,1 |
| Calendrier des ventes (achats différés au palier) | 0 | −0,5 | 0,0 | 0,0 | +0,2 | 0 | 0 | 0 |
| Report de paiement (besoin de financement net) | 0 | 0 | −0,2 | −0,4 | −0,6 | −0,5 | −0,4 | −0,3 |
| Déductibilité (IS, revenus fonciers ; N+1) | 0 | 0 | 0 | −0,4 | −0,8 | −1,2 | −1,2 | −1,2 |
| **Net disponible** | **0** | **−0,5** | **+2,1** | **+3,8** | **+5,8** | **+5,2** | **+5,3** | **+5,5** |

- Pour 10 Md€ : 0 ; −0,5 ; +0,5 ; +0,8 ; +1,2 ; puis ≈ +0,8 à +1,0. Pour 20 Md€ : 0 ; −0,5 ; +3,7 ; +6,9 ; +10,3 ; puis
  ≈ +9,6 à +10,0. Les tables complètes figurent dans `annuel_par_scenario`.
- **Achats différés** [H] : chaque palier d'un point décale environ 3 % des ventes annuelles de décembre à janvier
  (ordre de grandeur tiré des +26 % de Bérard et Trannoy pour 0,7 point). Le seul écart négatif (−0,5 Md€ en 2028) est
  un décalage de recette, récupéré en 2029. Une **baisse unique en 2030** (variante `E15_baisse_unique_2030`) n'a aucune
  année négative dans notre calcul (+3,4 Md€ en 2029). Mais elle incite à attendre plus de deux ans pour économiser
  2,9 % du prix, ce que notre hypothèse d'un mois de décalage ne capte pas. Nous recommandons les paliers. Si les valeurs
  prennent un an de retard, tout glisse d'un an (variante `E15_glissement_un_an`) sans coût budgétaire.
- **Report** [H] : 25 % des hausses des propriétaires occupants sont dues par des ménages éligibles (sous un plafond de
  revenu, par exemple celui de l'art. 1417 II du CGI, montant non relu). La moitié l'utilise. Intérêt de 3 %,
  remboursement de 1/15 du stock par an. Le stock atteint 5,6 Md€ en 2040.
- **Déductibilité** [H] : 20 % de la part payée par les entreprises soumises à l'IS (hors HLM) et 25 % de la hausse des
  bailleurs (taxe déductible des revenus fonciers au réel). À confirmer avec le bloc IS pour ne pas compter deux fois.

## 6. Perte patrimoniale et trésorerie

Une hausse durable d'impôt sur un bien immobile se reporte dans son prix. Le propriétaire actuel perd à l'annonce la
valeur actuelle des hausses futures. C'est une **perte de patrimoine**, définitive, que l'étalement ne change presque pas
(97 % de la perte est supportée à l'annonce pour une montée sur trois ans). À 15 Md€, elle vaut 500 Md€ pour l'ensemble des
propriétaires à r = 3 %, dont 322 Md€ (3,6 % de leur valeur) pour les logements des ménages. Elle atteint −7,5 % au 5e
centile, et 34 % des logements perdent plus de 5 % [S]. Elle est assumée [C]. Si la baisse des droits passe aussi dans les
prix, la perte nette tombe à environ 230 Md€ pour l'ensemble des propriétaires. L'acheteur futur, lui, paie le bien
moins cher d'autant : pour lui, la taxe capitalisée est neutre.

La **difficulté de trésorerie** est autre chose : un retraité modeste dans un bien qui a pris de la valeur peut ne pas
pouvoir payer 500 € de plus par an. Le report la règle sans rien donner. La dette, avec intérêt, est réglée sur le prix de
vente ou la succession. Le prêt reste remboursable, mais il crée un besoin de financement, compté dans la trajectoire
(≈ 0,3 à 0,6 Md€ par an). Les reports facultatifs sont très peu utilisés : moins de 1 % des ayants droit aux États-Unis
dans les années 1990 (Baer, 1998, cité par Shan, 2010, non relu). D'où un report proposé sur l'avis lui-même.

## 7. Cas-types (enveloppe de 15 Md€ ; prix = médiane DVF 2023-2024 au m² × surface)

**Le jeune couple à Massy (Essonne).** Un trois-pièces de 65 m² à 4 140 €/m² coûte **269 000 €** (DVF de Massy ; un
bien à 400 000 € correspondrait plutôt à 95 m²). Ces primo-accédants pour leur résidence principale échappent à la
majoration temporaire. Le tableau DGFiP au 1/6/2026 donne pour l'Essonne 5,00 % hors primo-accédants et 4,50 % sinon, et
aucune réduction au titre de l'art. 1594 F septies. Massy, plus de 5 000 habitants, perçoit la taxe communale de 1,20 %,
et l'État prélève 2,37 % de la part départementale. Les droits atteignent donc **15 620 € (5,81 %)** ; un acheteur non
primo-accédant paierait 17 000 € (6,32 %) jusqu'au 31/3/2028. Les « frais de notaire » ajoutent les émoluments et la
contribution de sécurité immobilière, non comptés ici. Après réforme, le couple paie **7 810 €** et économise **7 810 €**.
Sa taxe foncière (925 € estimés) augmente de **+475 €/an** en régime permanent, dont 448 € de part nationale, atteints par
paliers d'environ 160 €. Si les prix ne bougent pas, il reste gagnant de 4 850 € s'il revend au bout de sept ans. L'économie
vaut 16 ans de hausse. Si la hausse se capitalise, il achète environ 15 800 € moins cher et la taxe lui est neutre. Le
propriétaire qui lui vend, lui, perd cette somme.

**La famille qui suit un emploi.** Propriétaire d'une maison à Orléans (270 000 €), elle accepte un poste en Essonne et
achète une maison de 100 m² à Sainte-Geneviève-des-Bois (365 000 €). Elle paie 23 060 € de droits en 2026 (6,32 %),
21 190 € au taux permanent et **10 600 €** après réforme. Pour payer les seuls droits, il faut aujourd'hui une
augmentation nette de **294 € par mois pendant six ans** ; après réforme, 147 €. Sa taxe foncière augmente ensuite
de +560 €/an.

| Projet (g5) | Prix | Droits actuels (5,81 %) | Après (2,90 %) | Économie | Taxe foncière +€/an (15 ; 10 Md€) |
|---|---|---|---|---|---|
| Orléans, appartement 65 m² (ville moyenne) | 170 000 | 9 870 | 4 940 | 4 940 | +300 ; +220 |
| Lyon, appartement 80 m² (métropole) | 372 000 | 21 600 | 10 800 | 10 800 | +665 ; +450 |
| Massy, appartement 65 m² (couronne) | 269 000 | 15 620 | 7 810 | 7 810 | +475 ; +325 |
| Sainte-Geneviève-des-Bois, maison 100 m² (Île-de-France) | 365 000 | 21 190 | 10 600 | 10 600 | +560 ; +380 |

**Perdants** [S] : propriétaires qui ne vendent pas là où le sol est cher. À Paris, l'appartement médian prend +850 €/an
(+156 %) ; les maisons des communes de villégiature chères étaient déjà les plus touchées dans l’ancien calcul. Les terrains nus et les biens des sociétés
(HLM comprises) et associations paient 5,3 Md€ de part nationale, pour 1,5 Md€ de droits en moins. Rapportée à la valeur, la taxe passe de 0,54 à 0,61 % dans les communes les
moins chères et de 0,18 à 0,35 % dans les plus chères (g4) : l'écart se resserre, sans s'inverser.

## 8. Gains (indicateurs d'efficacité, pas de PIB)

[S] Perte sèche annuelle évitée, avec 15 Md€ : **1,7 Md€** sur les ventes de logements à σ = 6 % par point (0,9 à σ = 3 ;
2,3 à σ = 8 ; **0 si la réaction n'est que temporaire**), environ 0,4 Md€ sur les ventes d'autres immeubles (σ transposé)
et 0,4 Md€ sur le bâti des logements (impôt de 14,3 à 9,4 Md€). L'impôt sur le sol n'ajoute pas de perte sèche. La
réduction de l'IS financée par l'excédent est comptée dans le bloc IS. Mobilité des propriétaires : de 0 à +25 % si elle
réagit comme aux Pays-Bas (extrapolation non établie). Le double taux réduit le coût fiscal de construire : sur un terrain
de 200 000 €, un immeuble de 600 000 € ajoute 2 150 €/an d'impôt à taux unique, contre 980 € avec le double taux. Garder
le terrain nu coûte 1 300 € au lieu de 720 € (g6).

## 9. Figures : titres-messages proposés

- **g4_taxe_valeur** : « Rapportée à la valeur, la taxe foncière reste plus lourde dans les communes bon marché, mais
  le rapport avec les plus chères passe de 3 à 1,7 ».
- **g5_achats** : « Diviser les droits par deux fait économiser de 5 000 à 11 000 € à l'achat, contre 300 à 650 € de
  taxe foncière en plus par an ».
- **g6_sol_bati** : « Taxer le sol plutôt que le bâti divise par deux l'impôt dû pour avoir construit et renchérit la
  détention d'un terrain vide ».

## 10. Limites qui peuvent changer la conclusion

1. **Réaction des ventes** : si elle n'est que temporaire (lecture française de 2014), le gain sur les ventes disparaît.
   La réforme se défend alors par la base (sol, valeurs de marché), par la mobilité des familles et par le financement
   de l'IS.
2. **Capitalisation** : r = 3 % (Koster et Pinchbeck, 2022, trouvent 3 à 4 % en Angleterre ; capitalisation complète au
   Danemark, Høj et al., 2018). Une étude danoise non publiée ne trouve aucun effet sur les prix (Nielsson et al., 2024) :
   l'assiette ne baisserait pas, et la recette serait plus forte.
3. **Assiette** : valeurs Insee du sol par secteur, sans géographie pour les entreprises. Le contenu des « autres
   terrains » (565 Md€) est mal connu ; sans eux, les taux montent de 7 %. Les droits sur les autres biens (3,0 Md€) sont
   une différence entre deux sources.
4. **Dispersion** : un même taux de la valeur pour tous les logements d'une commune. Les perdants individuels seront plus
   nombreux que simulé.
5. **Administration** : le Bade-Wurtemberg, qui avait déjà ses valeurs de zone, a mis plus de quatre ans. Le premier avis
   en 2029 est ambitieux ; la clause de synchronisation protège le budget, pas le calendrier.
6. **Report et déductibilité** : paramètres supposés (éligibilité, recours, taux effectifs).
7. **Droit** : égalité devant l'impôt de valeurs de zone appliquées à toute la parcelle (jamais expertisé en France) ;
   découplage de la TEOM ; compensation des départements (aucune exigence d'une compensation à l'euro près, décision
   2019-796 DC).

## 11. Références vérifiées (lecture : textes, sauf mention)

- DGFiP, « Droits d'enregistrement et taxe de publicité foncière : taux… applicables au 1er juin 2026 » (impots.gouv.fr,
  lu le 16/11/2026) : Essonne, Métropole de Lyon et Loiret à 5,00 % hors primo-accédants, 4,50 % sinon ; Savoie seule à taux réduit
  pour les primo-accédants. Loi n° 2025-127, art. 116 (majoration du 1/4/2025 au 31/3/2028) ; art. 1584 et 1647 V CGI
  (BOFiP, via `foncier/notes/droits_mutation.md`).
- Landesgrundsteuergesetz BW du 4/11/2020 (§ 38, 40, 50 lus sur gesetze-im-internet.de) ; loi modificative du
  18/11/2025 (GBl. n° 113) et Drucksache 17/9480 (§ 38 al. 4, § 40 al. 8, § 50a) ; BFH II R 26/24 et II R 27/24
  (communiqué) ; Stadtkämmerei Karlsruhe (07/10/2024).
- Oates et Schwab (1997), *NTJ* 50(1), 1-21 ; Plassmann et Tideman (2000), *JUE* 47(2), 216-247 (résumé et thèse) ;
  Banzhaf et Lavery (2010), *JUE* 67(2), 169-179 (version de travail Lincoln 2008) ; Hughes (2006), Lincoln WP06ZK1.
- Bérard et Trannoy (2018), *Économie et Statistique* 500-502 ; Bachelet et Poulhès (2017), CGDD ; Dachis, Duranton et
  Turner (2012), *JEG* 12(2) ; Fritzsche et Vandrei (2019), *RSUE* 74 (résumé) ; Dolls, Fuest, Krolage et Neumeier
  (2025), *JUE* 145 ; Eerola, Harjunen, Lyytikäinen et Saarimaa (2021), *JUE* 124 ; Hilber et Lyytikäinen (2017),
  *JUE* 101 ; van Ommeren et van Leuvensteijn (2005), *JRS* 45(4) ; Koster et Pinchbeck (2022), *AEJ: Policy* 14(1) ;
  Høj, Jørgensen et Schou (2018), *Fiscal Studies* 39(2) ; Nielsson, Wroblewski et Yding (2024, document de travail).
  Contrôles détaillés : `revue/verif_litterature_foncier.md`, `foncier/notes/`.
