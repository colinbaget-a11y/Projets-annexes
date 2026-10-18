# Épisodes d'émeutes candidats (FR, IT, UK, DE, ES, 2005-2025) : notes

Fichier de données : `episodes_candidats.csv` (38 lignes ; 13 retenus, 9 limites, 16 écartés).
Une case vide signifie que l'information n'a pas été trouvée ou n'a pas pu être vérifiée : rien n'a été estimé.

## 1. Règle de sélection proposée

On évalue trois critères, chacun à partir de chiffres publiés :

- **C1, destruction.** Au moins une des conditions suivantes :
  - au moins 100 véhicules incendiés ;
  - au moins 20 bâtiments ou commerces incendiés, pillés ou saccagés ;
  - des dégâts estimés à au moins 1 M€ (ou l'équivalent en £).
- **C2, intensité.** Au moins 300 interpellations, ou au moins 100 membres des forces de l'ordre blessés.
- **C3, extension.** Des violences dans au moins 3 communes, sur au moins 2 jours ou nuits consécutifs.

**Classement :**

- **Retenu** : C1 est rempli, ainsi que C2 ou C3. La destruction est donc obligatoire, ce qui exclut les simples manifestations réprimées.
- **Limite** : au moins un critère est rempli, mais pas la combinaison exigée pour « retenu ».
- **Écarté** : aucun critère n'est rempli, ou aucun ne peut être vérifié.

**Pourquoi ces choix :**

- Les interpellations seules sont un mauvais indicateur, car elles dépendent de la doctrine policière. En France, les interpellations préventives sont massives (1 082 le 8 décembre 2018 à Paris, avec peu de dégâts). C'est pourquoi C1 est obligatoire.
- Le seuil de 1 M€ est bas. Il permet de garder les journées urbaines très médiatisées (Blockupy, Rome 2011, Milan 2015).
- **Variante stricte** (test de robustesse) : C1 exige au moins 10 M€ de dégâts ou au moins 500 véhicules incendiés.
  - Resteraient retenus : France 2005, Gilets jaunes (agrégat), Nahel 2023, Nouvelle-Calédonie 2024, Angleterre 2011, Royaume-Uni 2024 et G20 Hambourg 2017 (12 M€).
  - Passeraient en limite : Catalogne 2019 (≈9,8 M€, juste sous le seuil), PSG 2025 (264 véhicules), le 1er décembre 2018, Villiers-le-Bel, Blockupy et Ballymena.

## 2. Résultat (retenus)

| Pays | Épisode | Date du pic |
|---|---|---|
| FR | Banlieues 2005 | 06/11/2005 (nuit du 6 au 7) |
| FR | Villiers-le-Bel 2007 | 26/11/2007 |
| FR | Gilets jaunes, agrégat | 01/12/2018 |
| FR | Gilets jaunes, 1er décembre 2018 | 01/12/2018 |
| FR | Nahel | 30/06/2023 |
| FR (NC) | Nouvelle-Calédonie | 14/05/2024 |
| FR | PSG | 31/05/2025 |
| UK | Angleterre 2011 | 08/08/2011 |
| UK | Été 2024 (Southport) | 04/08/2024 |
| UK (NI) | Ballymena 2025 | 11/06/2025 |
| DE | G20 Hambourg | 07/07/2017 |
| DE | Blockupy Francfort | 18/03/2015 |
| ES | Catalogne 2019 | 18/10/2019 |

**L'Italie n'a aucun épisode retenu.** Rome (15 octobre 2011) et Milan (1er mai 2015) sont classés limites : ils remplissent C1 mais restent des journées dans une seule ville, avec peu d'interpellations.

## 3. Précautions pour l'usage économétrique

- **Proximité électorale (risque de confusion avec la campagne) :**
  - Catalogne : trois semaines avant les législatives du 10 novembre 2019.
  - Royaume-Uni 2024 : quatre semaines après l'élection du 4 juillet 2024, d'où un effet « lune de miel » de Starmer.
  - Corse : en pleine campagne présidentielle de 2022.
- **Hors du champ des sondages nationaux :**
  - Les sondages britanniques couvrent en général la Grande-Bretagne seule, pas l'Irlande du Nord (Ballymena 2025, Belfast 2005).
  - La Nouvelle-Calédonie et la Guadeloupe sont des territoires ultramarins : leur effet sur les intentions de vote en métropole est peut-être faible.
- **Mouvements politiques eux-mêmes :** les Gilets jaunes, la Catalogne et les retraites sont des mobilisations politiques en soi. L'émeute n'y est pas exogène à l'opinion, contrairement à 2005, Nahel, 2011 ou PSG. Il vaut mieux distinguer :
  1. les émeutes « apolitiques » de quartiers ou de supporters ;
  2. celles d'extrême gauche ou de black bloc (G20, Blockupy, Rome 2011, Milan 2015) ;
  3. celles d'extrême droite (Royaume-Uni 2024, Ballymena, Chemnitz, CGIL, Torre Pacheco) ;
  4. celles d'indépendantistes ou de nationalistes (Catalogne, Nouvelle-Calédonie, Corse).
- **Date du choc :** prendre `date_pic`. Pour les épisodes de plusieurs nuits, la date de début peut aussi servir de choc, car la couverture médiatique démarre souvent dès la première nuit.
- **Écartés mais très politisés :** Chemnitz 2018, l'assaut de la CGIL en 2021 et Torre Pacheco 2025 ont peu de destructions mais une très forte charge politique. Ils peuvent servir de groupe de contrôle (violence politique sans émeute destructrice) ou être testés séparément.

## 4. Points incertains et sources contradictoires

- **France 2005 :**
  - Date du pic : en.wikipedia (tableau) et la presse placent le maximum (1 408 véhicules, 274 communes) la nuit du 6 au 7 novembre. fr.wikipedia écrit « nuit du 7 au 8 novembre, 1 500 voitures ». J'ai retenu le 6 novembre.
  - Morts : 2, 3 ou 4 selon les sources.
  - Interpellations : 2 888 à 2 921 selon le bilan ministériel, 4 770 au 30 novembre, et L'Obs annonce 6 056.
  - Véhicules : de 8 973 à 10 346.
  - Coût : 200 M€ selon la FFSA en décembre 2005, révisé à 150-160 M€ en avril 2006.
- **Villiers-le-Bel :**
  - Policiers blessés : 81 selon la DDSP, contre 119 dont 81 par arme à feu dans l'infobox de fr.wikipedia.
  - Total de véhicules incendiés non trouvé (63 pour la seule nuit du 26 au 27).
  - fr.wikipedia date la fin au 9 décembre ; j'ai retenu le 27 novembre (fin des trois nuits de violences).
- **1er décembre 2018 :**
  - Blessés : 133 selon la préfecture de police via AP, contre 110 dans un bilan antérieur.
  - Véhicules : « près de 55 voitures », chiffre d'une source secondaire, sans chiffre officiel trouvé.
  - Les « 6 immeubles incendiés » viennent de Public Sénat ; une dépêche anglophone dit n'avoir pas trouvé de bâtiments incendiés.
  - C1 repose surtout sur l'Arc de Triomphe (≈1 M€, CMN). Le classement « retenu » est donc proche du seuil.
- **16 mars 2019 :** 91 commerces touchés selon la CCI, contre environ 80 enseignes dont une vingtaine pillées ou incendiées selon d'autres sources. Aucun montant trouvé.
- **Gilets jaunes, agrégat :**
  - Montant FFA : 170 M€ à la mi-mars 2019 (hors acte 18), 200 M€ au 16 mars, 217 M€ fin mai.
  - Totaux d'interpellations et de blessés non recherchés de façon fiable : cases laissées vides.
- **Retraites 2023 :**
  - 455 ou 457 interpellations le 23 mars.
  - Aucun chiffrage des dégâts trouvé.
  - Date de fin (28 mars) conventionnelle.
- **Nahel 2023 :**
  - Véhicules : 12 031 selon le rapport du Sénat (avril 2024), contre 5 662 à 5 892 selon les décomptes nuit par nuit. Le chiffre du Sénat inclut probablement les véhicules touchés par propagation : à vérifier dans le rapport.
  - Coût : 650 M€ (1re estimation des assureurs), puis 793 M€ assurés, et environ 1 Md€ au total.
  - Pic : 1 311 interpellations la nuit du 30 juin au 1er juillet, mais le nombre maximal de véhicules (≈1 990) a pu être atteint la nuit du 29 au 30.
- **Nouvelle-Calédonie :**
  - Morts : 14 dans l'infobox, 13 dans une partie du texte de fr.wikipedia.
  - Date de fin conventionnelle (≈15 juin). Les violences sporadiques et le couvre-feu durent jusqu'à décembre 2024.
- **PSG 2025 :**
  - 559 interpellations (ministère), puis 563.
  - 264 véhicules incendiés : chiffre provisoire du ministère, repris par Tuniscope. Je ne l'ai pas trouvé dans une source de presse française de premier rang : à recouper (AFP, Le Monde).
- **Angleterre 2011 :**
  - Interpellations : 4 105 selon le Home Office, contre « 3 000+ » au 10 août et 3 103 personnes passées en justice un an plus tard.
  - Nombre de véhicules incendiés non trouvé.
  - Coût : 200 M£ assurés (ABI) et 500 M£ au total. Ce dernier chiffre vient du rapport intérimaire du Riots Panel, cité via la presse et non lu directement.
- **Royaume-Uni 2024 :**
  - Policiers blessés : 361+ selon en.wikipedia, non recoupé.
  - Coût : estimations d'assureurs seulement (au moins 20 M£ ; moins de 250 M£). Une grande partie relève du Riot Compensation Act (à la charge de la police), sans total public trouvé.
- **Ballymena 2025 :**
  - Coût : « plusieurs millions de livres », formule vague tirée d'un témoignage au tribunal. C1 n'est donc rempli que faiblement.
  - Policiers blessés : 59, 63 ou 107 selon la date du bilan.
- **G20 Hambourg :**
  - Policiers blessés : 231 à 592 selon le mode de calcul (Dudde parle de 592 blessés « intentionnellement »).
  - Les 12 M€ du GDV ne couvrent ni la voirie, ni les bâtiments publics, ni les véhicules de police.
- **Blockupy :** 1,6 M€ selon un député cité par le Wiesbadener Kurier ; la police parlait d'un montant « de l'ordre du million ».
- **Catalogne 2019 :**
  - Pas de total d'interpellations sur l'ensemble de l'épisode (194 du 14 au 19 octobre).
  - Pas de total de conteneurs ou de véhicules brûlés.
  - Les 2,5 M€ de la mairie de Barcelone ne couvrent que la première semaine.
- **Hasél 2021 :**
  - Les 70 000 € ne concernent que la 1re nuit à Barcelone.
  - Aucun bilan des pillages de commerces trouvé.
  - Date de fin incertaine : des manifestations ont continué en mars.
- **Italie :**
  - Bilans des dégâts presque introuvables (14 décembre 2010, CGIL 2021, Sandri 2007).
  - Rome 2011 : blessés de 70 (jour même) à environ 200 selon des sources non vérifiées.
  - Milan 2015 : 1,5 M€ correspond à un fonds régional d'indemnisation, pas à une estimation des dégâts.
- **Allemagne, Berlin 2022-2023 :** 103 interpellations, chiffre tiré d'une source secondaire (Tichys Einblick) qui cite les autorités. Le chiffre de 145 circulant ailleurs n'a pas été confirmé.
- **Torre Pacheco 2025 :** dates exactes de début et de fin incertaines (les violences commencent vers le 11 ou 12 juillet).

## 5. Épisodes non inclus ou écartés sans fiche détaillée

- **Gilets jaunes, 8 décembre 2018 :** 1 082 interpellations à Paris (cité par L'Avenir/Belga), mais peu de destructions : illustre la limite du critère des interpellations.
- **Autres épisodes non examinés,** faute de temps et parce qu'ils sont a priori d'une ampleur moindre :
  - France : Grenoble-Villeneuve 2010, Amiens-Nord 2012, Sainte-Soline 2023, Martinique 2024 ;
  - Espagne : Ferraz (Madrid) novembre 2023, Linares 2021 ;
  - Italie : Catane 2007 (mort de l'inspecteur Raciti).
  Martinique 2024 mériterait d'être vérifié si les territoires ultramarins sont conservés.
