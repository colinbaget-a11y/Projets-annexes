# Revue : « Fusionner les impôts sur le revenu » (note IR-CSG)

## Verdict

La direction est juste : taxer les pensions, qui ne réagissent pas, et aplatir le haut réduit les distorsions. L'ampleur n'est pas établie : 94 % du gain de perte sèche vient du décile supérieur, mesuré sur le seul coin IR-CSG, sans marge extensive. C'est du revenu déclaré, pas de la croissance. La note tait un risque constitutionnel, change de convention pour les grandes fortunes et n'aide que certaines familles. Rien d'impossible ; les plus fortes hausses frappent les petites pensions (jusqu'à 19 %).

## Problèmes, du plus grave au moins grave

**1. Mauvais coin pour la perte sèche.**
- *Passage* : « elle croît avec le carré du taux marginal ».
- *Problème* : `proposition.py` prend pour τ le seul taux IR-CSG (32 % à 50 000 € brut). Le coin marginal total au salaire moyen est de 58 % (OCDE, `donnees/coin_marginal_par_niveau.csv`), et vos notes (`sorties/lit_haut_elasticites.md`) calibrent les élasticités sur ce coin total.
- *Pourquoi* : avec un coin préexistant τc, un point d'IR-CSG coûte au premier ordre environ e·z·(τc+τ)/(1−τc−τ)². Le niveau (18 Md€), les gains au milieu et les coûts en bas (retrait de la prime d'activité) sont sous-estimés ; le classement des barèmes peut changer.
- *Correction* : recalculer τ avec OpenFisca, cotisations non contributives et prime d'activité comprises.

**2. La « croissance » est du revenu déclaré en haut.**
- *Passage* : « La perte sèche est de 9 Md€ […], deux fois moins qu'aujourd'hui ».
- *Problème* : recalcul sur le modèle (jeu central) : 8,3 des 8,8 Md€ de gain viennent des 10 % du haut (90-99 % : 7,4 → 3,1 ; top 1 % : 7,0 → 3,0). Le revenu du travail déclaré augmente de 22 Md€, dont 97 % dans ce décile.
- *Pourquoi* : en haut, l'élasticité mesure surtout le calendrier, la forme de la rémunération et le passage vers l'IS et le PFU (Saez, Slemrod, Giertz 2012). Un revenu déplacé vers une autre assiette taxée n'est pas une perte sèche.
- *Correction* : publier la décomposition ; ajouter une variante avec report d'une partie de la réponse sur une assiette taxée à environ 50 % ; parler d'un effet de niveau (environ 0,3 % du PIB).

**3. Risque constitutionnel absent.**
- *Passages* : « L'impôt est individuel » ; franchise sur la seule activité.
- *Problème* : le Conseil constitutionnel a censuré la contribution à 75 %, assise « par personne physique sans prendre en considération l'existence du foyer fiscal » (2012-662 DC, cons. 73), et la ristourne de CSG, qui ignorait les autres revenus, le foyer et les charges de famille (2000-437 DC, cons. 9). La proposition réunit ces deux traits ; remplacer l'impôt de foyer distingue le cas de 2012, mais l'argument manque.
- *Correction* : ajouter un paragraphe juridique et chiffrer une option d'imposition commune.

**4. Grandes fortunes : la convention change en cours de route.**
- *Passage* : « Si, comme c'est vraisemblable, la part du capital […] croît […] autant qu'aujourd'hui ».
- *Problème* : tous les autres chiffres utilisent CAPITAL=mixte (défaut) ; cette phrase cite CAPITAL=haut. En mixte, `controle_hauts.txt` donne +2,8 points de RFR entre 3 et 9 M€ et +6,2 au-delà.
- C'est un artefact : au-delà de 9 M€, mixte prête aux revenus du barème un IR actuel de 23 % (35 % en « haut »), très en dessous de 45 % plus 4 %.
- *Correction* : caler la part du PFU par tranche sur le rapport IR/RFR et tout recalculer. En « haut », le reste bouge peu (t1 : 25,4 % au lieu de 24,2 ; déciles 1 à 7 : ±2 € ; perte sèche : 9,0 Md€).

**5. Marge extensive manquante.**
- *Passages* : « elle rend le premier emploi […] plus payant » ; « chaque millier d'euros de franchise […] coûte environ 0,5 Md€ ».
- *Problème* : le modèle compte le coût de la franchise, pas son bénéfice ; l'étape 3, l'ancre, relève le taux d'entrée sans coût de participation. Le mécanisme est plausible, pas démontré, et la prime d'activité est ignorée.
- La franchise couvre aussi les loyers (`LABN`). Cela contredit « la franchise récompense le travail » et exonère 16 000 € pour un couple de retraités bailleurs.
- *Correction* : calculer les taux de prélèvement à la participation à 0,5 et 1 Smic, prime d'activité comprise, avec une élasticité extensive (0,25 dans vos notes). Exclure les loyers de la franchise.

**6. Les retraités sont imposés *plus* que les actifs.**
- *Passage* : « l'imposition des retraités comme des actifs ».
- *Problème* : à 17 000 €, le retraité paie 3 250 €, l'actif 1 270 €. Défendable (Ramsey), mais à écrire.
- 17 000 € est proche du seuil d'exonération de CSG au-delà de 65 ans : c'est le pire cas.
- Une pension de 10 000 € paierait 1 825 €. Or l'ASPA garantit 12 523 € par an, calculés sur les ressources brutes : ses allocataires tomberaient sous le minimum.
- *Correction* : donner la hausse par niveau de pension, exonérer jusqu'au niveau de l'ASPA et traiter l'invalidité à part.

**7. Aide aux familles surestimée.**
- *Passages* : « un peu moins pour les plus aisées » ; « 20,6 Md€ au lieu de 13,9 ».
- *Problème* : la valeur de la franchise suit le taux marginal : 1 880 € à 200 000 € de revenu net, 2 990 € à 600 000 €. Elle dépasse donc le plafond de 1 791 € dès environ 170 000 €.
- Les familles de trois enfants ne sont pas modélisées. Au troisième enfant, le quotient donne 1 840 € à 60 000 € de RFR et 3 010 € à 80 000 € (`ir_actuel`) ; la franchise, environ 1 500 €.
- Le comparateur omet la garde d'enfants (1,8 Md€) et la scolarité (0,45 Md€), supprimées : il faut comparer à au moins 16,2 Md€.
- *Correction* : modéliser trois enfants ; corriger la phrase.

**8. Erreurs ponctuelles.**
- Les optimums butent sur les bornes de la grille (étape 3 : 120 et 600 k€ ; proposition : 45 et 600 k€), avec un taux du haut fixé à 50 %. Sans contrainte, le minimum serait un impôt forfaitaire : écrire « le meilleur des barèmes essayés ».
- « Au-delà de 8 000 €, […] les pensions doivent alors financer davantage » : le modèle dit l'inverse (+13,0 → +12,6 Md€). La hausse vient du taux d'entrée, qui passe de 17 à 20 %.
- L'article 3 du PLF 2027 a été supprimé en commission, puis en séance le 15 octobre (presse) : dater.
- Chetty et al. (2011) ne montrent pas que les heures bougent peu, mais que les frictions masquent une élasticité de long terme d'au moins 0,34.
- Sauts de CSG : citer la règle des deux années.

## Questions

**1. Économiste mainstream.** Il approuverait l'élargissement de l'assiette, la taxation des bases inélastiques et l'individualisation, qui augmenterait les heures des épouses de 3,7 % (Kabátek et al., 2014) : la note n'exploite pas ce gain. Il contesterait les points 1, 2, 5 et 8, et ajouterait la saillance : les salariés réagissent à l'IR, pas aux cotisations (Lehmann, Marical et Rioux, 2013) ; une CSG fondue dans un impôt visible peut accroître les réponses.

**2. Centre droit.** Il approuverait la baisse des taux sur le travail (personne seule à 150 000 € : −13 170 €). Il objecterait à la fin des quotients, à la suppression des réductions pour dons et emploi à domicile (7 Md€), et à un effort plus lourd sur les petites pensions (+19 %) que sur les aisées (+9 % à 30 000 €).

**3. Croissance.** Le mécanisme tient ; 4 à 15 Md€ est crédible comme borne haute d'un effet de niveau sur le revenu déclaré. Le coût du travail ne change pas ; la recette induite (+5 Md€) n'est pas nette des reports vers le PFU. Non chiffrés : seconds apporteurs, seniors, chômeurs.

**4. Système et perdants.** Rien d'impossible, mais trois chantiers manquent : les seuils des aides fondés sur le RFR, qui augmente d'environ 10 % sans les abattements ; la base de la prime d'activité ; l'affectation de la CSG et de la CRDS.

Paieraient aussi nettement plus : pensions d'invalidité, chômeurs (+3 Md€), parents isolés (+340 €), couples sans enfant (+360 €), couples mono-actifs (+1 080 €), gros utilisateurs de niches. Les 33 % de perdants sont un plancher.

**5. Familles.** La réforme favorise les couples avec deux enfants (−970 €), pas les parents isolés, les familles nombreuses ni les couples mono-actifs. L'aide croît avec le revenu, alors que les transferts jouent peu sur la natalité en haut (Cohen et al., 2013) et que les crèches ont un effet plus durable (Bergsvik et al., 2021). Supprimer le crédit pour garde va contre l'objectif.

**6. Grandes fortunes.** Aucune hausse n'est démontrée : capital inchangé, barème du haut plus bas. Restent des pertes individuelles (dons, outre-mer, monuments historiques) et la CDHR à redéfinir.

## Vérifié, non vérifié

Vérifiés : décisions [2012-662](https://www.conseil-constitutionnel.fr/decision/2012/2012662DC.htm) et [2000-437](https://www.conseil-constitutionnel.fr/decision/2000/2000437DC.htm) ; PLF 2027 ([AN](https://www.assemblee-nationale.fr/dyn/17/comptes-rendus/cion_fin/l17cion_fin2627005_compte-rendu.pdf), [presse](https://selectra.info/finance/actualites/marche/impot-retraites-abattement-supprime-15-octobre)) ; [ASPA](https://www.service-public.gouv.fr/particuliers/vosdroits/F16871) ; [CSG des pensions](https://www.service-public.gouv.fr/particuliers/vosdroits/F2971) ; rapport Blin de 1977. Non vérifiés : page du rapport Blin, imposition de l'ASPA, suite au Sénat, 153 Md€ de CSG.
