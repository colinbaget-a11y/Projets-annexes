# Avis interne : la note « Taxer mieux plutôt que davantage » relue avec la grille de la Tax Foundation

*16 novembre 2026. Avis interne, non publié. Il relit sur le fond `synthese/note-reforme-fiscale.pdf`, dans sa version du 16 novembre, avec la grille d'analyse publique de la Tax Foundation : neutralité, assiettes larges et taux bas, déduction immédiate de l'investissement, impôt foncier préféré aux droits sur les transactions, compétitivité internationale, critique de la double imposition du capital. L'avis ne parle pas au nom de la Tax Foundation : les seules phrases qu'il lui attribue sont tirées de ses publications, citées à la fin. Les points déjà relevés dans `revue/revue_*.md` ne sont repris que si cette grille change le diagnostic. Trois marques sont utilisées : **[vérifié]** pour un fait contrôlé sur une source citée à la fin ; **[calcul]** pour un calcul de l'avis, non refait dans les modèles du dossier ; **[supposé]** pour une hypothèse plausible que la littérature n'a pas établie.*

## Verdict

La note ne se trompe pas de direction : une assiette large avec des taux marginaux plus bas en haut, des droits de mutation remplacés par un impôt récurrent, un IS financé par l'assiette plutôt que par le taux et un PFU stable, c'est ce que demande la grille. Trois défauts de conception affaiblissent pourtant sa justification : la « taxe sur le sol » ne frappe que le sol des logements des particuliers, et taxe donc un usage plutôt que le sol ; le gain de la fusion suppose que les pensions ne réagissent pas, ce qui n'est vrai que pour les retraités actuels ; le calendrier de la déduction immédiate crée une falaise en 2033, et son financement renchérit le capital des PME. Les autres défauts (épargne retraite imposée deux fois, report d'apport-cession non tranché, CRDS rendue permanente sans le dire) se corrigent sans changer la thèse.

## Grosses erreurs de fond, de la plus grave à la moins grave

### 1. La « taxe sur le sol » ne taxe que le sol des logements des particuliers

**Ce que dit la note.**
- « Un impôt récurrent sur la valeur du sol ne décourage ni le travail ni la construction, puisque le terrain existe de toute façon. »
- Les droits perdus sont remplacés par « un taux national de 0,19 % sur la valeur des terrains ». Ce taux est calé sur le seul champ des 30,5 millions de logements des particuliers, HLM exclus, soit environ 3 070 Md€ de terrains (`perte_seche_autres.py`).
- La baisse des droits de mutation ne vise que les logements. Les locaux professionnels « ne sont pas traités ici » (`foncier/note-foncier.tex`) ; ils représentent environ 3 Md€ de droits (16,7 Md€ au total en 2025, dont 13,6 sur les logements, selon la note).
- « L'impôt qui porte sur les constructions passe d'environ 14 à 7 Md€ : c'est le principal effet économique. »

**Pourquoi c'est une erreur.**
- *Un impôt sur le sol n'est neutre que s'il ne dépend pas de l'usage du terrain.* Ici, le taux national ne s'applique que lorsque le terrain porte un logement de particulier. Y échappent le terrain à bâtir resté nu, le terrain d'une entreprise et celui d'un HLM.
  - À 3 % d'actualisation, 0,19 % par an représentent environ 6 % de la valeur du terrain **[calcul]**. Mettre une parcelle en logement privé coûte donc ce montant de plus que la laisser nue ou la céder à un usage d'entreprise.
  - L'impôt récompense ainsi l'attente sur les terrains constructibles, à l'inverse de l'effet que la note invoque. Le double taux de Pennsylvanie qu'elle cite (Banzhaf et Lavery) porte sur tous les terrains. L'ampleur de la réaction n'est pas mesurée **[supposé]**.
- *La réforme creuse l'écart entre le logement et le capital productif.* Elle allège de 7 Md€ l'impôt sur les constructions résidentielles. Les bâtiments d'entreprise gardent leur taxe foncière et la CFE, et les ventes de locaux professionnels leurs droits de mutation.
  - La note reconnaît que le logement occupé par son propriétaire est déjà avantagé : le loyer qu'il se verse n'est pas imposé.
  - Au regard de la neutralité, la réforme pousse donc l'épargne vers la brique plutôt que vers les machines.
- *La grille et les références de la note vont toutes dans le même sens.*
  - L'International Tax Competitiveness Index (ITCI) 2026 ne donne la meilleure note qu'aux pays sans impôt foncier ou qui ne taxent que le sol (« or only tax land »), c'est-à-dire l'Australie et l'Estonie. Il pénalise les droits de mutation, présentés comme « a direct tax on capital », y compris sur l'immobilier d'entreprise. La France y est 32e sur 38 pour les impôts sur la propriété **[vérifié]**.
  - Le Bade-Wurtemberg, que la note cite comme modèle, applique sa valeur du sol à toutes les parcelles. Depuis une loi de 2021, ses communes peuvent aussi taxer plus lourdement les terrains constructibles laissés nus (« Grundsteuer C ») **[vérifié]**.

**Ce qu'il faudrait changer.**
- Asseoir le taux national sur la valeur de tous les terrains, bâtis ou non, quels que soient le propriétaire et l'usage, par valeur de zone multipliée par la surface (la méthode de la note). Le taux sera inférieur à 0,19 % ; il reste à calculer.
- Appliquer le même double taux à la taxe foncière des locaux professionnels.
- Programmer la baisse de moitié des droits de mutation sur l'immobilier d'entreprise (environ 1,5 Md€ **[calcul]**), ou dire pourquoi on y renonce.
- Imposer les terrains à bâtir à leur valeur de terrain constructible, avec une majoration communale facultative, sur le modèle de la « Grundsteuer C ».
- Traiter les HLM par un dégrèvement explicite plutôt qu'en les retirant de l'assiette.
- Refaire les tableaux de répartition : une partie de la charge prévue pour Paris (+122 %) passera sur les terrains d'entreprise et les terrains nus.

### 2. Le gain de la fusion compte comme permanent un gain qui vient en partie des retraités actuels

**Ce que dit la note.**
- « Taxer ce qui ne réagit pas pour alléger ce qui réagit. Les pensions déjà liquidées […] ne réagissent presque pas. »
- « C'est le mécanisme même du gain : leurs pensions sont taxées comme des salaires. » Les actifs paient 15 Md€ de moins, les retraités 15 Md€ de plus ; « l'emploi et les familles se financent pour l'essentiel sur les pensions ».
- Entre 12 500 et 25 000 € de pension, le taux marginal de 28 % est jugé « sans effet sur l'activité ».
- Le coin total ne compte que les « cotisations sans contrepartie de droits ». Dans le modèle, « les pensions et le chômage ne réagissent pas » (`synthese/modele_purs.py`).

**Pourquoi c'est un risque majeur.**
- *Le principe est bon.* Les cotisations sont déduites, puisque l'assiette est le revenu après cotisations, et les pensions sont taxées. C'est le traitement neutre de l'épargne retraite que préfère la grille : déduite à l'entrée, imposée à la sortie.
- *Le chiffrage confond le stock et le régime permanent.*
  - Pour les retraités actuels, la hausse frappe des décisions passées : elle ne fausse rien, mais son gain n'existe que pendant la transition.
  - Pour les futurs retraités, la pension est la contrepartie des cotisations contributives. Le modèle suppose que les salariés valorisent ces droits, puisqu'il ne met pas ces cotisations dans le coin.
  - S'ils les valorisent, une hausse permanente de l'impôt sur les pensions réduit la valeur de ces droits, donc taxe le travail qui les acquiert. En régime permanent, la baisse de 15 Md€ sur les actifs et la hausse de 15 Md€ sur les pensions touchent les mêmes personnes à deux âges de leur vie. Pour un salarié en carrière complète, si le rendement est proche de la croissance, le coin sur toute la vie bouge peu.
  - Le modèle retient la moitié favorable de chaque hypothèse. Si les droits sont valorisés, l'impôt sur la pension entre dans le coin ; s'ils ne le sont pas, les cotisations contributives y entrent et le coin de départ est plus élevé.
  - L'ampleur du biais dépend de la façon dont les salariés perçoivent ce lien. En France, le lien entre une cotisation de plus et la pension est faible pour beaucoup : minimum contributif, 25 meilleures années, six derniers mois dans la fonction publique. Cela réduit le problème, sans qu'on puisse le chiffrer ici **[supposé]**.
- *L'âge de départ est une marge d'activité.* Entre 12 500 et 25 000 € de pension, une année de travail de plus relève la pension, et ce supplément est taxé à 28 %. « Sans effet sur l'activité » n'est vrai que pour les pensions déjà liquidées.
- *La note se contredit sur ce point.* Elle rejette la contribution exceptionnelle sur l'IS parce qu'elle « fait payer les investissements passés et rend incertain le rendement des investissements futurs ». Le levier principal de la fusion fait la même chose avec le travail et les cotisations passés.

**Ce qu'il faudrait changer.**
- Garder la mesure et changer sa justification.
- Séparer le gain de transition, qui vient du stock de retraités et baisse à mesure que les générations se renouvellent, du gain en régime permanent.
- Ajouter une variante où une part (0, ½ ou 1) de la hausse d'impôt sur les pensions, actualisée, entre dans le coin des actifs, symétriquement au traitement des cotisations contributives.
- Supprimer « sans effet sur l'activité ».
- Si le gain en régime permanent baisse nettement, réviser la phrase de l'ensemble selon laquelle « plus des deux tiers du gain » viennent de la fusion. Le modèle n'a pas été refait pour cet avis.

### 3. IS : une falaise en 2033, et un financement qui renchérit le capital des PME

**Ce que dit la note.**
- La déduction est fixée à 50 % jusqu'en 2032, puis à 100 %, par un calendrier voté dès 2027.
- Elle est financée par la fin du taux réduit (2,2 à 3,1 Md€), le CIR apprécié au niveau du groupe (0,6), la fin des zones (0,55) et la boîte à brevets réduite de moitié (0,2 à 0,6).
- L'excédent est « rendu par une baisse du taux normal de 0,6 à 1,2 point » une fois la dette de transition remboursée, en 4 à 25 ans.
- Gain d'efficacité : 0,1 Md€ (0,05 à 0,16), « moins 0 à 0,8 si fin du taux réduit » (tableau 5).

**Pourquoi c'est une erreur.**
- *Une falaise annoncée.*
  - Avec la valeur actuelle de déduction de la note (z = 0,85 à 0,90), un équipement déduit à 50 % vaut 0,925 à 0,95 de son prix en déductions ; à 100 %, il en vaut 1. Acheter le 2 janvier 2033 plutôt que le 31 décembre 2032 fait donc gagner 1,2 à 1,9 % du prix **[calcul]**.
  - On peut attendre un creux d'investissement fin 2032 et un pic en 2033. La note applique elle-même ce raisonnement aux droits de mutation : une baisse « annoncée pour plus tard […] gèlerait les ventes ».
  - Les réactions de calendrier à l'amortissement exceptionnel américain ont été fortes (House et Shapiro, 2008, cités de seconde main dans `is/notes/is_recherche.md`).
- *Le financement renchérit le capital des PME.*
  - Sous le plafond du taux réduit, la fin de ce taux porte le taux marginal de 15 à 25 %. La hausse frappe tout le capital de ces sociétés : stocks, besoin en fonds de roulement, locaux, incorporels. L'allègement, lui, ne porte que sur les équipements, et seulement à moitié jusqu'en 2032.
  - D'après les chiffres de la note, le bilan de l'IS en bien-être est de signe incertain (+0,05 à +0,16 contre jusqu'à −0,8 Md€).
  - La grille approuve un taux unique : l'ITCI pénalise les taux multiples, les boîtes à brevets et les subventions à la R&D, et la France a la troisième subvention implicite à la R&D la plus généreuse de l'OCDE, 34,3 % contre 16,4 % en moyenne **[vérifié]**. Elle l'approuve à condition que la recette revienne aussitôt par le taux normal ou par la déduction de tous les actifs. La rendre « une fois la dette remboursée » transforme la mesure en hausse durable de l'impôt des petites sociétés.
- *Les déficits.* La déduction immédiate multiplie les déficits fiscaux des entreprises qui investissent. Leur imputation est plafonnée à 1 M€ plus 50 % du bénéfice au-delà, et le report se fait sans intérêt. La note le signale en une phrase sans en tirer de conséquence ; l'ITCI 2026 relève ce plafond **[vérifié]**.

**Ce qu'il faudrait changer.**
- Monter de 50 à 100 % par paliers annuels de 10 points, de 2028 à 2032, au lieu d'un saut de 50 points au 1er janvier 2033. Chaque palier ne fait plus gagner qu'environ 0,3 % du prix par an d'attente **[calcul]**, moins que ce que coûte une année de retard.
- Ouvrir dès 2027 une déduction de 100 % sous un plafond annuel à toutes les sociétés à l'IS, sur le modèle de l'« Annual Investment Allowance » britannique (1 M£, permanente) **[vérifié]**. Les PME, chez qui l'effet mesuré passe par la trésorerie (Zwick et Mahon), en profitent tout de suite. Celles qui investissent sont ainsi compensées de la fin du taux réduit.
- Inscrire dans la loi le calendrier de baisse du taux normal financée par l'élargissement de l'assiette, au lieu de la subordonner au remboursement de la dette.
- Sortir du plafond les déficits nés des nouvelles déductions, ou les reporter avec intérêt.

### 4. L'assiette sans déduction impose deux fois l'épargne retraite

**Ce que dit la note.**
- L'assiette est « sans réduction, abattement ni taux réduit ». Le dossier précise que la réforme « n'admet ni déduction, ni réduction, ni crédit » (`ir_csg/sorties/niches_crds.md`).
- Les versements d'épargne retraite déduits du revenu (PER et anciens contrats) représentent environ 9,6 Md€ en revenus 2024, plus 0,9 Md€ pour les indépendants. La note n'en dit rien.

**Pourquoi c'est une erreur.**
- Aujourd'hui, les versements volontaires sur un PER sont déduits, et la sortie est imposée : rente comme une pension, capital au barème pour la part des versements **[vérifié]**.
- Supprimer la déduction sans exonérer la sortie fait payer l'impôt deux fois sur la même épargne. Les cotisations obligatoires, elles, restent déduites (revenu après cotisations).
- C'est précisément la double imposition de l'épargne que la grille combat. Élargir l'assiette consiste à supprimer des faveurs, pas le traitement neutre de l'épargne.
- L'enjeu est de 2 à 4 Md€ d'impôt **[calcul grossier : taux marginal moyen de 20 à 40 % supposé pour ceux qui déduisent]**, sur des foyers surtout aisés.
- Les tableaux par décile en tiennent déjà compte en moyenne, puisque le modèle part d'une assiette sans déduction. C'est le traitement de l'épargne qui pose problème, pas la recette.

**Ce qu'il faudrait changer.**
- Écrire que les versements d'épargne retraite restent déductibles, dans les plafonds actuels, ce qui est cohérent avec les cotisations obligatoires.
- À défaut, exonérer à la sortie la part issue de versements non déduits.
- Remettre le coût dans le barème.

### 5. Le report d'apport-cession n'est pas tranché, et l'option du PLF 2027 impose deux fois la même valeur

**Ce que dit la note.**
- Elle décrit trois traitements : l'expiration à toute transmission (PLF 2027, art. 5), l'expiration à la vente par la holding, et la transmission du report aux héritiers sans effacement.
- Elle n'en choisit aucun. Le tableau 5 renvoie au « traitement du report » pour la recette comme pour « qui paie plus ».

**Pourquoi c'est une erreur.**
- Le respect de la contrainte sur les grandes fortunes en dépend. L'expiration à toute transmission alourdit de 90 à 100 M€ la facture de chacun des plus gros apporteurs, selon la note.
- Pour la grille, l'effacement au décès (le « step-up » américain) évite que la même valeur paie à la fois l'impôt successoral et l'impôt sur la plus-value **[vérifié]**.
  - L'option du PLF 2027 empile les deux : plus-value imposée à la transmission, puis droits de succession, sans liquidité pour une holding familiale sous pacte Dutreil.
  - La Tax Foundation chiffre deux options sur ce point : supprimer l'effacement, ce qui alourdit selon elle l'imposition de l'épargne, et remplacer l'impôt successoral par une imposition des plus-values au décès **[vérifié]**. Elle ne propose pas d'ajouter la seconde au premier, ce que fait le PLF 2027.
- La transmission du report aux héritiers garde un seul impôt à la transmission et taxe la plus-value quand le capital sort réellement des sociétés.
  - Les États-Unis avaient abandonné en 1979 ce régime (le « carryover basis »), notamment parce que les héritiers ne connaissaient pas toujours le prix d'acquisition **[vérifié]**.
  - L'objection ne vaut pas ici. La plus-value en report est déclarée chaque année (état de suivi 2074-I, ligne 8UT) **[vérifié]**.

**Ce qu'il faudrait changer.**
- Retenir la transmission du report sans effacement et l'écrire.
- Si le gouvernement maintient l'expiration à toute transmission, demander que l'impôt sur la plus-value s'impute sur les droits de succession.

### 6. La CRDS devient permanente sans que la note le dise

**Ce que dit la note.**
- La fusion garde une recette de 220 Md€, dont 7 Md€ de CRDS.
- Ailleurs, la note prend pour référence le droit en vigueur : la contribution exceptionnelle sur l'IS « s'éteint ».

**Pourquoi c'est une erreur.**
- La CRDS n'est due que jusqu'à l'extinction des missions de la CADES (ordonnance de 1996, modifiée en 2004). La loi organique du 7 août 2020 fixe cette extinction au 31 décembre 2033 **[vérifié]**.
- Par rapport au droit en vigueur, la fusion rend donc permanents environ 7 Md€ par an à partir de 2034, près d'un quart de point de PIB **[calcul]**. La note traite ainsi les deux prélèvements temporaires de façon opposée.
- La dette de l'ACOSS, qui pourrait atteindre 82 Md€ fin 2026 selon le Sénat, rend probable une prolongation **[vérifié]**. C'est alors un choix à écrire, pas un acquis.

**Ce qu'il faudrait changer.**
- Dire quelle référence est retenue.
- Prévoir soit une baisse des taux de l'impôt fusionné à l'extinction de la CADES, soit, explicitement, que l'impôt fusionné reprend le financement de la dette sociale.

## Choix contestables mais défendables

1. **Le PFU maintenu à 31,4 %, avec une majoration de 3 puis 4 points qui remplace la CEHR.**
   - Le bénéfice distribué supporte 49,1 % au total, 52,1 % avec la majoration. Après la fusion, le taux marginal supérieur sur un salaire tombe à 50 %, hors cotisations : la hiérarchie s'inverse au sommet.
   - La grille irait vers un taux intégré plus bas, voire vers l'impôt sur la seule distribution. L'Estonie taxe à 22 % les seuls bénéfices distribués et n'impose pas le dividende chez l'actionnaire ; elle est première de l'ITCI pour la 13e année **[vérifié]**.
   - Le choix est défendable : après la baisse de 2018, aucun effet n'a été détecté sur l'investissement ni sur les salaires (France Stratégie, 2023), la réaction des dividendes porte sur leur date, et la contrainte budgétaire s'impose.
   - L'argument de stabilité vaut toutefois dans les deux sens : le taux de référence est celui que la LFSS pour 2026 vient de relever. Il faudrait au moins montrer la comparaison après fusion et chiffrer le retour à 30 % comme variante.
2. **Les droits de mutation seulement divisés par deux.**
   - Le triangle de la note décroît vite : les 2,9 % restants ne coûtent qu'environ 0,5 Md€ de perte sèche (6 × 196 / 2 × 0,029²) **[calcul]**. S'arrêter à mi-chemin se défend.
   - La grille viserait zéro à terme, en commençant par l'immobilier d'entreprise (erreur 1).
3. **Un rapport de quatre entre le terrain et le bâti plutôt que le sol seul.**
   - L'ITCI ne récompense que le sol seul. D'après le tableau 3 de la note, le sol seul ne gagne que 0,1 Md€ de plus.
   - Le choix est défendable pour la répartition : avec deux taux nationaux, le dernier décile paie +215 % de taxe foncière, contre +266 % avec le sol seul. Il faudrait toutefois annoncer le sol seul comme point d'arrivée.
4. **Mesurer le bien-être alors que l'objectif affiché est la croissance.**
   - Le bien-être est le bon critère. Mais, pour un coin petit, l'effet sur le PIB est sans commune mesure avec la perte sèche évitée : pour l'IS, +0,1 % de PIB à long terme, près de 3 Md€ **[calcul]**, contre 0,1 Md€ de perte sèche.
   - La phrase « L'IS et le PFU servent surtout à ne pas aggraver les choses » dépend donc de l'indicateur choisi. Il faudrait ajouter au tableau 5 une colonne de PIB, de capital et d'emploi à long terme, comme le fait un chiffrage dynamique.
5. **Des élasticités de court terme et aucune mobilité au sommet.**
   - Les hypothèses hautes (0,20 à 0,25 pour le revenu réel au-dessus de la médiane) restent sous la valeur de long terme que la note cite elle-même : environ 0,3 selon Chetty, Guren, Manoli et Weber.
   - Aucune réaction migratoire des hauts salaires n'est comptée. La littérature en trouve pourtant de fortes : Kleven, Landais, Saez et Schultz (QJE, 2014), sur le régime danois des étrangers **[vérifié]**.
   - De plus, la liste des exonérations que l'assiette supprime « si elle suit celle de la CSG » comprend le régime des impatriés (0,4 Md€, `niches_crds.md`). La note n'en parle pas.
   - La prudence se défend. Elle biaise toutefois contre l'aplatissement du barème, et les hypothèses hautes devraient être présentées comme « de court terme ».
6. **Une franchise d'activité qui couvre les loyers.** Elle avantage les loyers par rapport aux revenus au PFU et ne rend aucun travail plus payant ; la note le reconnaît. Le modèle ne sait pas séparer ces revenus, mais la loi peut réserver la franchise aux salaires et à la part travail des bénéfices des indépendants.

## Ce qui manque

- **Les impôts de production.**
  - L'ITCI 2026 relève que la France tire 13 % de ses recettes fiscales sur les entreprises d'impôts assis sur le chiffre d'affaires ; la Grèce suit avec 3,4 % **[vérifié]**. Il juge la déduction des investissements en France supérieure à la moyenne, mais « compromised by the French production taxes ».
  - Selon la grille, un euro gagné sur l'assiette de l'IS doit être comparé à une baisse de la C3S ou de la CVAE. La note doit montrer pourquoi la déduction des équipements, où la France est déjà au-dessus de la moyenne (88 % contre 86 %), passe avant.
- **L'immobilier d'entreprise.** Droits de mutation sur les locaux professionnels, taxe foncière sur les bâtiments d'entreprise, CFE (erreur 1).
- **L'IFI à côté du taux national sur le sol.**
  - Le même terrain parisien paierait la taxe foncière (+122 %), le taux national et l'IFI. Le profil du « rentier » de la note omet l'IFI.
  - L'ITCI donne une note moyenne aux impôts sur la fortune qui ne visent que certains actifs ; la meilleure note revient aux pays qui n'en ont pas **[vérifié]**. Fondre l'IFI dans l'impôt sur le sol irait dans le sens de la grille. Il faut au moins montrer le cumul.
- **L'inflation.** Le PFU frappe à 31,4 % les intérêts et les plus-values nominaux. L'indexation du prix d'acquisition est présentée comme « la correction de principe », sans être proposée ni chiffrée. Elle rendrait aussi au sommet une partie de ce que coûterait la fin de l'effacement du report.
- **Le biais en faveur de la dette.**
  - Sous 3 M€ de charges financières nettes, la déduction immédiate s'ajoute à des intérêts entièrement déductibles. L'équipement financé par emprunt est alors subventionné : son taux marginal effectif devient négatif (`is/notes/is_recherche.md`).
  - L'ITCI récompense la déduction pour fonds propres **[vérifié]**. Il faut au moins le dire.
- **L'amortissement neutre, à comparer.**
  - La Tax Foundation le propose pour réduire le coût initial de la déduction immédiate : on garde les durées d'amortissement et on majore chaque année les annuités restantes pour que leur valeur actuelle égale 100 % **[vérifié]**. Il supprime la bosse de 14 à 15,5 Md€ la première année et peut s'étendre aux bâtiments, dont les déductions valent 54,8 % du prix en France selon l'ITCI 2026 **[vérifié]**.
  - Il coûte toutefois plus cher à l'État en valeur actuelle si la majoration est calée sur le taux des entreprises, puisque l'État paie alors leur taux au lieu du sien. La dette de transition de la note est un prêt aux entreprises au taux de l'État ; ce n'est pas une perte.
  - Calée sur le taux de l'État, la majoration comble environ 60 % de l'écart avec la déduction immédiate, pour une entreprise qui actualise à 5 %, sans coût actuariel supplémentaire pour l'État **[calcul : amortissement linéaire sur sept ans, majoration de 3,25 %]**.
- **Les locataires.** En théorie, la part de l'impôt qui porte sur le sol ne se reporte pas sur les loyers ; la part qui porte sur le bâti, si. Rien n'est chiffré.
- **Les comparaisons internationales.**
  - *Australie, territoire de la capitale (Canberra).* Depuis 2012, il remplace en vingt ans les droits de mutation par une taxe annuelle assise sur la valeur des terrains. C'est le précédent le plus proche de la bascule. Le gouvernement a délibérément ralenti le transfert, et une commission de l'assemblée territoriale a mis en garde contre des taxes annuelles « insoutenables » en fin de parcours **[vérifié, presse et organismes militants]**. La leçon politique, absente de la note : les perdants paient chaque année, les gagnants profitent d'une baisse diffuse.
  - *Estonie et Lettonie.* Elles n'imposent les bénéfices des sociétés qu'à leur distribution. Le circuit des holdings françaises en est une version privée, réservée à ceux qui peuvent en créer une. C'est la bonne comparaison pour la section 4.
  - *Royaume-Uni et États-Unis.* Le Royaume-Uni a rendu permanente la déduction immédiate des équipements en novembre 2023 ; les États-Unis ont rendu permanent l'amortissement de 100 % en juillet 2025, pour les biens acquis depuis le 19 janvier 2025 **[vérifié]**. Les deux sont passés à 100 % d'un coup. Avec 50 % pendant six ans, la France resterait en retrait de ses concurrents, ce qui pèse dans l'argument du taux moyen effectif.

## Ce qui est bien vu et à garder

- **Fusion IR-CSG-CRDS.**
  - Un impôt au lieu de trois, sur une seule assiette, individuel, sans au moins 24 Md€ de niches.
  - Le taux marginal supérieur sur le travail passe de 55 à 50 %, alors que l'ITCI classe le coin sur le travail français (47 %) parmi les plus lourds **[vérifié]**.
  - L'assiette « après cotisations » met fin à une double imposition. La CSG frappe aujourd'hui 98,25 % du salaire brut, cotisations salariales de retraite comprises, puis de nouveau la pension **[vérifié]**. La fusion revient au traitement neutre : cotisations déduites, pension imposée.
  - Autres acquis : une franchise ciblée sur la reprise d'emploi, une collecte inchangée par le prélèvement à la source, une variante de repli contre le risque constitutionnel, aucun gain fondé sur une réaction déclarative.
- **Immobilier.**
  - Passer des droits de mutation à un impôt récurrent plus lourd sur le sol est la direction exacte de la grille.
  - La baisse s'applique dès son annonce. Les valeurs sont révisées tous les trois ans. La note refuse tout plafond attaché au propriétaire (Proposition 13, Ferreira) et toute révision à chaque vente. Elle prévoit un report de paiement pour les propriétaires âgés et garde le pouvoir de taux des communes.
- **IS.**
  - Le taux de 25 % est gardé, et la contribution exceptionnelle, en partie rétroactive, s'éteint.
  - Le financement par l'assiette (taux réduit, CIR, zones, boîte à brevets) correspond exactement à ce que l'ITCI pénalise **[vérifié]**.
  - La note écarte un IS progressif et un impôt minimum national.
  - L'argument de fond est juste : la déduction immédiate exonère le rendement normal, la baisse du taux allège aussi les rentes et le capital déjà installé (Chodorow-Reich, Smith, Zidar et Zwick).
  - Voter tout le calendrier d'un coup, pour la stabilité, est un bon principe : c'est le profil du calendrier qu'il faut changer (erreur 3).
- **PFU.**
  - La stabilité comme objectif.
  - La lecture de 2013 et 2018 comme un seul épisode de calendrier.
  - Le principe d'imposer le bénéfice quand il sort des sociétés, qui est la logique estonienne.
  - Le refus d'un impôt de 25 % sur les revenus non distribués des holdings, qui taxerait le capital avant sa sortie.
  - Le diagnostic que la fuite tient à l'effacement au décès.
  - L'indexation préférée aux abattements pour durée de détention.
- **Méthode.** Le coin total, les fourchettes, la séparation entre réactions réelles et déclaratives, l'optimum gardé comme étalon et le « prix d'un milliard » rendent les arbitrages lisibles.

## Hors champ : présentation

Ces points relèvent de la réécriture et ne changent pas le fond :
- « principal effet économique » (constructions de 14 à 7 Md€), alors que la perte sèche évitée vient surtout des ventes (1,5 contre 0,4 Md€) ;
- la cellule IS du tableau 5 (« moins 0 à 0,8 si fin du taux réduit »), illisible ;
- le profil du « rentier », qui omet l'IFI.

## Vérifications

**Vérifié sur les sources citées ci-dessous.**
- ITCI 2026 : rangs de la France, notation des impôts fonciers, des droits de mutation, des impôts sur la fortune et des incitations, part des impôts sur le chiffre d'affaires, déductions par type d'actif.
- Positions de la Tax Foundation sur l'amortissement neutre, l'effacement au décès et le régime abandonné en 1979.
- Échéance de la CADES et durée de la CRDS.
- Assiette de la CSG sur les salaires et fiscalité du PER.
- Suivi déclaratif du report (2074-I).
- Bade-Wurtemberg ; réforme de Canberra ; déduction immédiate au Royaume-Uni et aux États-Unis ; Kleven et al. (2014).

**Non vérifié ou non calculé.**
- Valeur des terrains hors logements des particuliers, et taux national sur une assiette complète.
- Effet de la perception des impôts sur les pensions sur le gain de la fusion : le modèle n'a pas été refait.
- Coût exact d'un amortissement neutre : seul un calcul grossier a été fait, sur 63 Md€ d'investissement éligible par an, amortis linéairement sur sept ans.
- Montant d'impôt en jeu sur l'épargne retraite.
- Contenu des aménagements du report par la loi du 19 février 2026, signalés par le BOFiP.

**Sources.**
- Tax Foundation, *International Tax Competitiveness Index 2026* : https://taxfoundation.org/wp-content/uploads/2026/10/ITCI_26_book_v1.pdf
- Tax Foundation, amortissement neutre : https://taxfoundation.org/neutral-cost-recovery-full-expensing-faq/ ; https://taxfoundation.org/tax-reform-guide/option/adopt-a-neutral-cost-recovery-system-for-all-structures/
- Tax Foundation, effacement au décès : https://taxfoundation.org/tax-reform-guide/option/replace-the-estate-tax-with-capital-gains-taxation-at-death/ ; https://taxfoundation.org/tax-reform-guide/option/eliminate-step-up-in-basis-on-capital-gains-at-death/
- CADES et CRDS :
  - https://www.vie-publique.fr/loi/274394-lois-7-aout-2020-dette-sociale-et-autonomie-5e-risque-dependance
  - https://conseil-etat.fr/avis-consultatifs/derniers-avis-rendus/au-gouvernement/avis-relatif-a-l-interpretation-des-regles-organiques-encadrant-le-transfert-de-deficits-a-la-caisse-d-amortissement-de-la-dette-sociale-cades
  - https://www.legifrance.gouv.fr/jorf/article_jo/JORFARTI000001670850
  - https://www.senat.fr/rap/a25-747/a25-747_mono.html
- Assiette de la CSG (source secondaire) : https://payfit.com/fr/fiches-pratiques/csg/
- PER : https://www.service-public.gouv.fr/particuliers/vosdroits/F36526
- Report d'apport-cession : https://bofip.impots.gouv.fr/bofip/12041-PGP.html/identifiant=BOI-RPPM-PVBMI-30-10-60-40-20260810
- Bade-Wurtemberg : https://www.ihk.de/rhein-neckar/recht/steuerrecht/grundsteuer-gewerbesteuer/landesgrundsteuergesetz-bw-5149072 ; https://www.landtag-bw.de/resource/blob/254816/2edb5831417c5a99a828a2ace10ee534/17_1076_D.pdf
- Canberra :
  - https://www.prosper.org.au/2020/10/the-second-interval-the-evaluation-in-brief/
  - https://www.canberratimes.com.au/story/9303822/act-stamp-duty-phase-not-on-track-to-meet-timetable-review-says/
  - https://www.canberratimes.com.au/story/9339303/inquiry-warns-against-unsustainable-rates-bills-for-canberrans/
  - https://the-riotact.com/?p=788886
- Royaume-Uni : https://www.gov.uk/government/publications/capital-allowances-permanent-full-expensing/capital-allowances-permanent-full-expensing-for-companies-investing-in-plant-and-machinery
- États-Unis : https://rsmus.com/insights/services/business-tax/obba-tax-bonus-depreciation.html
- Kleven, Landais, Saez et Schultz (2014) : https://eml.berkeley.edu/~saez/kleven-landais-saez-schultzQJE14danishscheme.pdf
