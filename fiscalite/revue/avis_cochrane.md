# Avis de fond sur « Taxer mieux plutôt que davantage » : grille de John Cochrane

*Avis interne, non publié, 16 novembre 2026. Il porte sur la version actuelle de `synthese/note-reforme-fiscale.pdf`
(26 pages, compilée le 16/11 à 10 h 25), lue en entier, ainsi que sur `revue/methode_v2.md`, `synthese/modele_purs.py`,
`synthese/architectures_ircsg.py` et leurs sorties. La grille appliquée est celle que John Cochrane défend en public :
croissance par l'offre, assiette large et taux marginaux bas, préférence pour l'imposition de la consommation,
scepticisme sur l'imposition du capital et des sociétés, attention aux incitations marginales, aux effets d'équilibre et
à la crédibilité, méfiance envers la complexité et les dispositifs ciblés. Ce n'est pas son avis : aucune phrase ne lui
est attribuée.*

*Repères : **[N]** ce que dit la note ; **[M]** sortie des programmes de la note (`synthese/sorties/`) ; **[R]** calcul
de cette revue, fait avec les programmes de la note (méthode en fin de document).*

## Verdict

La note ne contient pas de grosse bêtise qui invaliderait le projet. Trois des quatre réformes vont dans le sens de cette
grille : assiette large et taux marginaux plus bas dans la moitié haute, impôt récurrent sur le sol à la place d'un impôt
sur les transactions, déduction immédiate financée par la suppression de dispositifs ciblés plutôt que par le taux.
Le défaut de fond est l'étalon de mesure. C'est une perte sèche statique, de court terme, limitée au travail, qui met à
zéro toutes les marges du capital et de l'épargne. Elle rend le bilan « modeste » par construction, sert à justifier le
maintien d'un impôt sur l'épargne parmi les plus lourds d'Europe et fait paraître bon marché chaque dispositif ciblé.
Ensuite, deux attributions sont contredites par les tableaux de la note elle-même. Les 15 Md€ demandés aux retraités ne
sont pas « le prix du gain d'efficacité ». La franchise « pour l'emploi » produit moins d'emploi dans la proposition finale que le
barème neutre sans franchise. Enfin, le calendrier de l'IS crée l'attentisme que la note évite ailleurs.

## Grosses erreurs de fond, de la plus grave à la moins grave

### 1. L'étalon ne mesure pas le critère annoncé, et il est asymétrique entre travail et capital

**Ce que dit la note.** Le critère est « quel système fiscal gêne le moins la croissance, c'est-à-dire décourage le moins
de travailler, d'investir, de déménager ou de produire » [N, introduction]. Le gain est mesuré par une perte sèche sur le
revenu d'activité, avec une élasticité intensive de 0,05 à 0,10 au centre et de 0,10 à 0,25 dans le jeu haut
[`methode_v2.md`], alors que la note cite 0,3 à long terme (Chetty, Guren, Manoli et Weber). Le PFU a un gain d'efficacité de 0 et
« ne rapporterait rien en activité » [N, tableau 5, § 4.3]. Le milliard levé coûte 0,07 Md€ de perte sèche (0,03 à
0,14) [N]. Conclusion : « Le gain total est modeste et robuste », environ 7 Md€, « 0,2 % du PIB » [N, § 5].

**Pourquoi c'est une erreur.**
- *Le jeu haut ne couvre pas l'élasticité de long terme que la note cite elle-même.* Les marges qui comptent pour la
  croissance n'y sont pas : carrière, formation, création d'entreprise, localisation des hauts revenus et des sièges,
  accumulation du capital. Le chiffre de 0,2 % du PIB n'est donc pas une mesure de l'effet sur la croissance. C'est
  un plancher construit sur les réactions observées d'une année sur l'autre. Il sera lu comme « la structure fiscale
  compte peu », ce que la méthode ne peut pas établir.
- *L'épargne n'a aucune élasticité dans le modèle.* Le 0 du PFU n'est pas un résultat. Il découle de cette hypothèse.
  Les études citées (Bach et al., France Stratégie, Yagan) mesurent l'investissement des sociétés existantes, pas la
  distorsion entre consommer aujourd'hui et demain, ni les fonds propres externes des jeunes entreprises. La note
  concède elle-même que le raisonnement « ne vaut pas pour une jeune entreprise qui lève des fonds propres à
  l'extérieur ». Pour le travail, la note retient des élasticités quasi expérimentales positives. Pour le capital,
  l'absence d'effet détecté à court terme vaut zéro. Les deux marges ne sont pas jugées avec la même exigence de preuve.
- *Conséquence directe sur la réforme : elle creuse l'écart entre l'imposition du travail et celle de l'épargne.* Vers
  50 000 € de salaire brut, le taux marginal de l'impôt fusionné tombe vers 24 % [R, barème de la proposition : 14 % puis
  montée à 30,3 % à 45 000 € imposés, franchise de 4 000 € ; même ordre que `revue_transversale.md` § 5.8]. Le bénéfice
  distribué reste à 48,6-49,1 % [N, figure 9]. L'intérêt reste taxé à 31,4 % sur son montant nominal, inflation comprise. Le dossier le
  dit pourtant (`07_ou_changer.md` § 7 : « le système taxe l'inflation sans que personne l'ait voté »).
  Une hiérarchie orientée vers la croissance irait dans l'autre sens.
- *Le prix d'un milliard est trop bas, ce qui fait paraître chaque dispositif ciblé bon marché.* 0,07 correspond à une
  élasticité d'environ 0,1. Avec la formule standard tε/(1−t−tε), un coin de 40 à 50 % et l'élasticité de 0,3 que la
  note cite donnent 0,25 à 0,43 [R]. À ce prix, la franchise par enfant ou l'exonération des petites pensions
  coûteraient trois à six fois plus que les « 0,1 à 0,9 Md€ » annoncés.

**Ce qu'il faudrait changer.**
- Nommer l'étalon pour ce qu'il est (« perte sèche statique sur l'activité, à court terme ») et retirer « croissance »
  et « 0,2 % du PIB » du bilan, ou les accompagner d'effets sur la production et l'emploi présentés à part, comme la
  section IS le fait déjà (production : +0,1 % du PIB ; bien-être : 0,05 à 0,16 Md€).
- Ajouter un jeu « long terme » qui croise les marges. Exemple calculé avec le modèle de la note [R] : élasticité
  intensive de 0,10 / 0,20 / 0,25 / 0,25 et participation de 0,10. La proposition gagne alors 8,8 Md€ au lieu de 4,9,
  presque entièrement par la marge intensive, et la franchise d'activité n'ajoute plus rien (−6,39 contre −6,33 Md€ pour le
  barème neutre).
- Pour le PFU, écrire que le maintien est un choix de stabilité, de budget et de répartition, pas l'absence d'effet
  réel. Ajouter au moins un bloc d'ordre de grandeur sur l'épargne, comme celui de la section IS. Traiter l'inflation sur les
  intérêts, pas seulement sur les plus-values.

### 2. Les 15 Md€ des retraités ne sont pas « le prix du gain d'efficacité »

**Ce que dit la note.** Taxer les pensions comme les salaires, « c'est le mécanisme même du gain » [N, § 1.4]. La hausse
de 15 Md€ « est le prix du gain d'efficacité » [N, § 5]. Le principe invoqué est de « taxer ce qui ne réagit pas »
[N, § 1.3].

**Pourquoi c'est une erreur.**
- *Le tableau 1 de la note dit autre chose.* Garder l'abattement de 10 % ramène la hausse des retraités de +7,0 à
  +0,9 Md€ et ne fait perdre que 0,6 Md€ de gain : 3,4 au lieu de 4,0, soit 85 % du gain du barème neutre conservé.
  La franchise par enfant reporte 6 Md€ de plus sur les retraités (+13,0) et *réduit* le gain (3,6). La franchise
  d'activité en reporte 7 de plus (+14,0) pour +0,6 Md€ de gain [N, tableau 1]. Dans la proposition elle-même, la
  franchise de 4 000 € achète 0,85 Md€ de gain par an contre 6,4 Md€ de plus payés par les retraités. Sans elle,
  avec les mêmes enfants, petites pensions et contrainte, le meilleur barème gagne 4,0 Md€ et les retraités paient
  +8,8 Md€. Avec elle, 4,9 et +15,2 [R]. L'essentiel des 15 Md€ finance donc la contrainte familiale et la franchise,
  pas l'efficacité. La note le dit d'ailleurs une fois correctement : « l'emploi et les familles se financent pour
  l'essentiel sur les pensions » [N, § 1.5].
- *« Taxer ce qui ne réagit pas » est un argument de prélèvement exceptionnel, valable pour le seul stock des pensions
  liquidées.* En régime permanent, la pension d'un système contributif est un salaire différé. Le modèle exclut les
  cotisations vieillesse du coin au motif qu'elles achètent des droits. Or la réforme réduit de 4,2 % la pension nette
  d'impôt : +15,2 Md€ sur 361 Md€ de pensions nettes d'impôt [M, `controles_purs.txt`]. Environ 1 point de salaire brut
  (4,2 % d'environ un quart du salaire brut en cotisations contributives) devient donc un prélèvement sans contrepartie pour les générations futures
  [R]. La note ne le compte pas.
- *Le raisonnement contredit la section IS.* La note condamne la contribution exceptionnelle parce qu'elle « fait payer
  les investissements passés et rend incertain le rendement des investissements futurs » [N, § 3]. Taxer davantage des
  pensions acquises sous d'autres règles, au motif qu'elles ne peuvent plus réagir, relève de la même logique. Un État
  qui l'assume apprend aux agents à réagir plus tôt.

**Ce qu'il faudrait changer.** Justifier l'alignement par la neutralité, et non par l'inélasticité. Même revenu, même
impôt : une pension est un salaire différé dont les cotisations ont été déduites, ce qui correspond au traitement d'un
impôt sur la consommation. Séparer dans les tableaux la part de la hausse qui sert l'efficacité de celle qui finance les
franchises. Corriger les deux phrases citées. Montrer la variante « barème neutre, abattement maintenu » comme celle qui
garde l'essentiel du gain sans charger les retraités. Voter l'alignement avec sa transition et une règle de stabilité.

### 3. La franchise « pour l'emploi » ne produit pas d'emploi dans la proposition finale

**Ce que dit la note.** Entre 1 et 1,5 Smic, « près de 60 % d'un euro de salaire en plus » est déjà prélevé [N, § 1.2].
La franchise de 4 000 € est retenue « pour l'emploi » ; c'est « le seul dispositif qui ajoute du gain » [N, § 1.3, 1.5].

**Pourquoi c'est une erreur.**
- Sous la contrainte de répartition, le barème retenu impose 14 % dès le premier euro au-delà de la franchise [M]. Le
  gain sur la participation tombe à 1,4 Md€, contre 1,8 pour le barème neutre sans franchise et 2,4 avec [M]. Un
  salarié au Smic paie 61 € de plus [M].
- 3,7 des 4,9 Md€ du gain viennent de la baisse des taux marginaux au-dessus de la médiane : −0,9 entre 50 et 90 %, −1,7
  entre 90 et 99 %, −1,1 pour le 1 % du haut [M]. Sous cette grille, c'est la bonne nouvelle de la note : le gain vient
  d'une assiette élargie et de taux marginaux plus bas là où se trouve le revenu. Mais la note raconte autre chose.
- Le coin de 60 % entre 1 et 1,5 Smic vient des cotisations non contributives et de la sortie de la prime d'activité.
  La fusion n'y touche pas. Le plus gros problème d'incitation que la note identifie reste entier.

**Ce qu'il faudrait changer.** Dire d'où vient le gain. Puis choisir : soit revenir à un taux d'entrée bas (le barème
neutre, à 2 % d'entrée et sans franchise, fait plus pour la participation que la proposition avec franchise), soit intégrer la prime d'activité au barème fusionné,
avec une seule pente de sortie. Le prélèvement à la source de l'impôt fusionné en est le véhicule naturel. Chiffrer
cette intégration.

### 4. L'IS : un calendrier qui pousse à attendre, des pertes mal traitées, un financement qui alourdit le reste du capital

**Ce que dit la note.** Déduction de 50 % de 2027 à 2032, puis 100 %, votée dès 2027 [N, § 3.3]. Les pertes ne sont
évoquées qu'en passant (« ce que le plafonnement de leur imputation empêche en partie ») [N, § 3.2]. La déduction porte
sur les seuls équipements. Elle est financée notamment par la fin du taux réduit de 15 %. Le gain de l'IS est de « 0,1
(0,05 à 0,16), moins 0 à 0,8 si fin du taux réduit » [N, tableau 5].

**Pourquoi c'est une erreur.**
- *Attentisme.* Avec 50 % de déduction immédiate et le reste amorti (z de 0,925 à 0,95), attendre 2033 fait gagner
  25 % × (1 − z), soit 1,2 à 1,9 % du prix de la machine [R]. C'est à peu près ce que coûte un mois de retard, pour un rendement brut
  de 15 à 20 % par an [R, hypothèse]. Les
  achats de fin 2032 glisseront donc sur 2033, et chaque budget sera tenté de rouvrir la date. La note applique
  pourtant la bonne règle aux droits de mutation : la baisse s'applique dès l'annonce, parce qu'annoncée pour plus tard
  elle gèlerait les ventes.
- *Pertes.* La déduction immédiate crée des déficits chez les entreprises qui investissent et croissent. Leur
  imputation est plafonnée (1 M€ plus 50 % du bénéfice au-delà, art. 209 I du CGI ; BOI-IS-DEF-10-30) et ils ne sont
  pas revalorisés. L'effet mesuré par Zwick et Mahon n'existe que chez les entreprises qui paient l'impôt, comme la
  note le rappelle. `revue_is.md` demandait de chiffrer un report hors plafond. Ce n'est pas fait.
- *Signe incertain.* Pour un équipement, la déduction immédiate à 25 % annule le coin sur le rendement normal, quel que
  soit le taux. Mais la hausse de 15 à 25 % touche aussi les bâtiments, l'immatériel acheté, les stocks et le besoin en
  fonds de roulement des petites sociétés. Le tableau 5 en tire honnêtement un gain net de signe incertain. La réforme
  censée rendre l'IS neutre pour l'investissement alourdit donc le coût d'une partie du capital.

**Ce qu'il faudrait changer.**
- Examiner l'amortissement neutre, dit « neutral cost recovery » : on revalorise chaque année la base restant à amortir
  au taux d'actualisation, si bien que la valeur actuelle des déductions égale celle d'une déduction immédiate. Le coût
  de première année est faible, ce qui traite précisément « la vraie difficulté » de la note (la transition). On peut
  l'appliquer dès 2027, à tout le capital amortissable, sans palier (voir les notes de la Tax Foundation en sources).
- Reporter les déficits nés de la déduction sans plafond et avec intérêts.
- Ensuite seulement, supprimer le taux réduit, dont le défaut (seuil, découpages, pic sous le plafond) est bien
  identifié. Montrer le taux marginal effectif d'une petite société avant et après.

### 5. La contrainte sur les plus grandes fortunes n'est pas démontrée, et le report d'apport-cession n'est pas tranché

**Ce que dit la note.** Dans la convention centrale du modèle, les 3 800 foyers au-delà de 3 M€ paieraient 2 à 16 points
de plus [N, § 1.5]. Le traitement du report d'apport-cession est laissé entre trois options, dont l'une (PLF 2027)
alourdirait de 90 à 100 M€ la facture de chacun des plus gros apporteurs [N, § 4.3].

**Pourquoi c'est un risque majeur.** C'est la première contrainte du cahier des charges, et la seule que la note ne
peut pas affirmer tenir (problème déjà classé premier par `revue_transversale.md`). Cette grille les présume aussi
les plus mobiles. L'estimation d'exil citée (Bach et al., 2025) ne porte que sur les revenus du capital.

**Ce qu'il faudrait changer.** Caler la part au PFU sur les données de la DGFiP, comme la note le prévoit. Si la
convention centrale se confirme, corriger par le haut du barème : un taux supérieur atteint plus tard ou plus bas, et non
le retour de niches. Pour le report, la seule option cohérente avec la logique de la note est la transmission du report
sans effacement. On impose quand le capital sort des sociétés, jamais sans liquidité, sans hausse de facture à la
transmission. Il faut la retenir et l'écrire.

## Choix contestables mais défendables

- **La troisième contrainte.** Aucun décile ne doit bouger de plus de 500 €. Le cahier des charges n'en fixe que deux.
  C'est elle qui coûte le dernier tiers du gain atteignable (4,9 contre 7,8 Md€). La prudence sur les élasticités la
  justifie, mais la note doit la présenter comme un choix de l'auteur. La note dit par ailleurs que « la redistribution
  n'est pas l'objectif ».
- **Impôt individuel et franchise par enfant plutôt que le quotient.** Sur l'étalon de la note, la variante « quotient
  conjugal et familial » fait mieux (3,9 contre 3,6 Md€). Elle allège le dixième du haut (−3,0 Md€), protège les couples
  à un revenu et écarte le risque constitutionnel de 2012 [N, tableau 1]. La note la refuse parce qu'elle « profite
  surtout aux couples aisés », objection de répartition. L'impôt individuel se défend sous cette grille : il baisse le
  taux du second apporteur, dont la participation réagit sans doute plus que l'η uniforme de 0,25 (Carbonnier, cité sur
  résumé, trouve 1 à 2). Il faut alors le dire et le tester avec une élasticité propre aux conjoints.
- **Droits de mutation divisés par deux plutôt que supprimés ; rapport terrain/bâti de 4 plutôt que le sol seul.**
  Le sol seul fait un peu mieux (−0,5 contre −0,4 Md€ de perte sèche sur le bâti) [N, tableau 3]. La transition et la
  répartition justifient le compromis.
- **PFU maintenu.** L'argument de stabilité est le meilleur de la section. La « nouvelle vue » du dividende est bien
  appliquée. Mais aligner la CSG du capital à 10,6 % (+1,3 Md€), présenté comme une simplification, alourdit l'impôt
  sur l'épargne. Sous cette grille, l'uniformité se ferait plutôt vers le bas.
- **Contribution exceptionnelle éteinte dans la référence.** C'est cohérent avec la critique de la rétroactivité. Mais la
  « recette constante » est mesurée par rapport à une référence inférieure de 5 à 7 Md€ à 2026 et au PLF 2027
  [N, tableau 4]. Le tableau 5 doit le dire.
- **Pensions exonérées de façon dégressive (taux de 28 % entre 12 500 et 25 000 €).** La note la dit « sans effet sur
  l'activité ». Ce n'est pas exact : le niveau de la pension dépend de l'âge de départ et de la surcote, ainsi que de
  l'épargne retraite. Environ un tiers des retraités du modèle ont une pension dans cette tranche (5,8 M d'adultes sur 18,3) [R].
- **« Effacement » du report au décès.** La note le présente comme une exonération définitive. Les droits de succession
  portent pourtant sur la valeur, plus-value latente comprise, sauf pacte Dutreil. L'option du PLF 2027 empile deux impôts
  sur le même événement, sans liquidité.

## Ce qui manque

- **L'impôt sur la consommation.** C'est le substitut naturel au prélèvement sur les pensions. Il frappe aussi les
  revenus acquis, y compris la consommation financée par le patrimoine, mais sans viser une catégorie. Il ne taxe pas
  l'épargne. Le dossier traite des taux réduits de TVA (`07_ou_changer.md` § 6). La note n'en dit pas un mot,
  même pour l'écarter.
- **L'intégration de la prime d'activité et des allègements dégressifs** au barème fusionné (voir l'erreur 3).
- **La marge de l'âge de départ.** La réforme taxe moins le salaire et plus la pension : elle rend la poursuite
  d'activité plus payante. C'est probablement un gain non compté, en faveur de la réforme, affaibli dans la tranche de
  sortie à 28 %.
- **Le droit des sols.** Là où la taxe foncière monte le plus (Paris +122 %), c'est la constructibilité, et non l'impôt,
  qui limite la construction. Le gain de 0,4 Md€ sur le bâti suppose que l'offre puisse répondre.
- **Les arbitrages entre salaire, dividende et société après la fusion** (24 % contre 48,6 % vers 50 000 €). Les
  dirigeants se paieront davantage en salaire, ce qui réduit l'assiette de l'IS. Rien n'est chiffré
  (`revue_transversale.md` § 5.8).
- **L'IFI.** Un impôt étroit sur le patrimoine immobilier coexisterait avec un impôt national sur le sol. L'absorber
  dans la taxe foncière simplifierait sans alourdir les grandes fortunes.
- **Un engagement de stabilité pour l'ensemble.** La note fait de la stabilité le premier service à rendre pour le PFU
  et l'IS. Il manque un instrument qui l'engage sur les quatre réformes (loi pluriannuelle, règle de non-rétroactivité).

## Ce qui est bien vu

- Le **coin total** : cotisations sans contrepartie et retrait des prestations comptés dans le coût de chaque euro
  perdu. C'est exactement la bonne mesure des incitations à la marge.
- La **séparation du réel et du déclaratif**, prudente, avec l'effet sur la recette donné à part. Le refus de laisser
  l'optimiseur décider, et la courbe des rendements décroissants qui montre ce que coûte chaque pas vers l'optimum.
- La **fusion sur assiette large** (au moins 24 Md€ de niches supprimées) avec des taux marginaux plus bas dans la
  moitié haute, et le taux supérieur ramené d'environ 55 à 50 %.
- L'**immobilier** : un impôt récurrent sur le sol à la place d'un impôt sur les ventes. La baisse s'applique dès son
  annonce. Les valeurs sont révisées tous les trois ans, ce qui évite le verrou de la Proposition 13. Le report de
  paiement est prévu pour les propriétaires âgés. La note est honnête sur la capitalisation et sur la fragilité du
  partage entre maisons et appartements.
- L'**IS** : la déduction immédiate plutôt qu'une baisse de taux qui allège aussi les rentes et le capital installé,
  financée par la fin du taux réduit, des zones, d'une partie de la boîte à brevets et du CIR apprécié par société. La
  note refuse un IS progressif et un minimum national, et laisse s'éteindre une surtaxe rétroactive. Elle distingue
  clairement le gain de production du gain de bien-être.
- Le **PFU** : la stabilité comme premier service ; l'arithmétique de la nouvelle vue ; le refus de taxer les bénéfices
  non distribués des holdings ; l'indexation du prix d'acquisition préférée aux abattements pour durée de détention.

## Fond ou présentation

| Point | Nature | À corriger dans |
|---|---|---|
| Étalon statique ; PFU à 0 par hypothèse ; prix du milliard | **Fond** (modèle, jeu long terme, bloc épargne) | méthode, § 4, § 5 |
| « 0,2 % du PIB », « modeste et robuste », « croissance » | Présentation, mais trompeuse sur le fond | introduction, § 5 |
| « Mécanisme même du gain », « prix du gain d'efficacité » | **Fond** (attribution fausse d'après le tableau 1) | § 1.4, § 5 |
| Prélèvement exceptionnel sur les pensions et coût permanent via les cotisations | **Fond** | § 1.3, méthode |
| Franchise « pour l'emploi », taux d'entrée de 14 % | **Fond** (choix du barème) et récit | § 1.3, § 1.5 |
| Palier de 2033, pertes, actifs couverts | **Fond** (conception) | § 3.3 |
| 3 800 foyers, report non tranché | **Fond** (contrainte du cahier des charges) | § 1.5, § 4.3 |
| Contribution exceptionnelle dans la référence | Présentation (dire la référence) | tableau 5 |

## Calculs de la revue

- *Jeu croisé* : `modele_purs.evalue` avec `V2["croise"] = reel (0,10 ; 0,20 ; 0,25 ; 0,25), decl (0,20 ; 0,30),
  eta 0,10`, sur le barème neutre, le neutre avec franchise de 4 000 € (recalé à recette égale par
  `architectures_ircsg.cale_d`) et le barème de la proposition. Résultats : −6,33 / −6,39 / −8,82 Md€. Les jeux bas,
  central et haut de la note sont retrouvés à l'identique (−4,03 / −4,55 / −4,85 au centre).
- *Proposition sans franchise d'activité* : même recherche que `architectures_ircsg.py` (contrainte ±500 € par décile,
  1 % du haut sans hausse, enfants à 6 000 €, petites pensions), avec F = 0 et une grille de taux d'entrée étendue à
  2-16 %. Barème retenu : 8 % au premier euro, 14 % à 20 k€, 30 % à 45 k€, 50 % à 1 M€. Gain −4,01 Md€, dont
  participation −1,06 ; retraités +8,8 Md€. Avec F = 4 000 €, la même recherche retrouve la proposition de la note
  (−4,86 ; +15,2).
- *Attentisme sur l'IS* : z = 0,5 + 0,5 × (0,85 à 0,90) ; gain à attendre = 0,25 × (1 − z).
- *Tranche de sortie des pensions* : adultes des foyers de retraités de `modele_purs.TYPES` dont la pension (part de
  ZN) est comprise entre 12 500 et 25 000 € : 5,79 M sur 18,25 M.
- *Prix du milliard* : tε/(1 − t − tε) avec t = 0,4 à 0,5 et ε = 0,3, soit 0,25 à 0,43. Avec ε = 0,1, on obtient 0,07 à
  0,11 et l'on retrouve l'ordre de grandeur de la note.
- *Cotisations vieillesse* : 27,4 % de cotisations contributives sous le plafond dans `ps_ircsg_methode.coin`
  (vieillesse et chômage ; la part vieillesse seule est un peu plus faible) ; × 4,2 % de pension nette en moins ≈ 1
  point de salaire brut. C'est un ordre de
  grandeur : le lien entre salaire et pension n'est que partiel dans le régime de base.

Non vérifié ici : les chiffres de la note tirés de la littérature et du droit, revus par ailleurs (`revue/verif_*.md`).

## Sources consultées en ligne

- Tax Foundation, [How Neutral Cost Recovery Works in Practice](https://taxfoundation.org/blog/how-neutral-cost-recovery-works-in-practice/) et
  [Reduce the Front Cost of Full Expensing](https://taxfoundation.org/blog/reduce-front-cost-full-expensing/) :
  mécanisme de l'amortissement neutre.
- BOFiP, [BOI-IS-DEF-10-30](https://bofip.impots.gouv.fr/export/pdf/3384) : plafonnement de l'imputation des déficits
  (art. 209 I du CGI), confirmé aussi par `revue/revue_is.md`.
