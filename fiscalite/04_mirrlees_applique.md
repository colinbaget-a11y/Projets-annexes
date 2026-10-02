# La Mirrlees Review appliquée à la France

## 1. Où en est le Royaume-Uni

La Mirrlees Review est l'exercice de référence : deux volumes publiés par l'Institute for
Fiscal Studies, *Dimensions of Tax Design* (2010), qui rassemble les travaux commandés à des
spécialistes, et *Tax by Design* (2011), 548 pages en vingt chapitres, qui tire les
conclusions. Elle a été présidée par James Mirrlees, avec notamment Stuart Adam, Timothy
Besley, Richard Blundell et Stephen Bond.

Vérification faite, **elle n'a pas eu de successeur**. Ce qui s'en rapproche le plus au
Royaume-Uni est l'IFS Deaton Review of Inequalities, présidée par Angus Deaton, qui porte sur
les inégalités et non sur la refonte du système fiscal. Son volet le plus proche de notre sujet
est un commentaire de Robert Moffitt intitulé « Transfers, taxes, and tax credits for those on
low incomes: beyond Mirrlees », qui soutient que la conception des transferts doit aller
au-delà du cadre de Mirrlees en intégrant la conditionnalité et les politiques de formation.
C'est une inflexion, pas une nouvelle revue.

Autrement dit, si l'on veut un modèle pour un exercice français, c'est *Tax by Design* qu'il
faut prendre, en sachant que ses chiffrages datent de 2010 et son terrain du Royaume-Uni.

## 2. Ce qui rend la Review réplicable

Sa force n'est pas la liste de ses recommandations, c'est sa méthode. Chaque chapitre suit la
même marche : une proposition théorique, un diagnostic chiffré qui montre que le système
s'en écarte, une mesure de l'écart, puis une réforme chiffrée avec ses gagnants et ses
perdants. Le diagnostic chiffré est le pivot. C'est lui qu'on peut refaire pour la France.

Les diagnostics signature de la Review, avec leur numéro de figure :

| Chapitre | Diagnostic | Figures |
|---|---|---|
| 4 | Distribution des taux de participation et des taux marginaux effectifs parmi les travailleurs | 4.5 |
| 4 | Taux moyens de participation et taux marginaux effectifs le long de la distribution des salaires, par type de famille | 4.6 à 4.8 |
| 9 | Effet d'un élargissement de l'assiette de TVA par décile de revenu et de dépense | 9.1 à 9.6 |
| 11 | Hétérogénéité du prix implicite du carbone selon la source et l'utilisateur | chapitre 11 |
| 14 | Taux effectifs d'imposition sur différents supports d'épargne | 14.1 |
| 16 | Comparaison de la taxe locale britannique avec un impôt proportionnel à la valeur du bien | 16.1 à 16.4 |
| 17 | Taux effectifs d'imposition des sociétés et biais dette-fonds propres | 17.1, 17.2 |

## 3. Ce que l'on peut refaire pour la France, et avec quoi

Trois de ces diagnostics sont réplicables immédiatement avec des données publiques. Les
autres demandent soit des données individuelles, soit un calcul propre.

| Diagnostic | Donnée trouvée | État |
|---|---|---|
| Taux marginaux effectifs | OCDE, modèle TaxBEN, `DSD_TAXBEN_METR` | répliqué |
| Taux de participation | OCDE, modèle TaxBEN, `DSD_TAXBEN_PTR` | répliqué |
| Prix implicite du carbone | OCDE, Effective Carbon Rates, `DSD_ECR` | répliqué |
| Taux effectifs sur les sociétés | Commission européenne, base ETR méthodologie Devereux-Griffith, 1998-2024 | identifié, à télécharger |
| Élargissement de la TVA par décile | enquête Budget de famille de l'Insee | données individuelles, accès à demander |
| Taux effectifs sur l'épargne | aucun jeu publié ; calcul à faire à partir des paramètres | à construire |
| Fiscalité foncière et valeur des biens | valeurs locatives contre DVF | à construire |

## 4. Les trois répliques

### 4.1 Le prix du carbone : la dispersion plutôt que le niveau

Le reproche central du chapitre 11 n'est pas que le carbone soit insuffisamment taxé, c'est
que le prix implicite varie « considérablement selon la source de l'émission et selon
l'identité de l'utilisateur ». La Review note même que le taux réduit de TVA sur l'énergie
domestique agit comme une subvention aux émissions.

Les données de l'OCDE permettent de mesurer exactement cela pour la France. En 2021, pour
l'ensemble des secteurs utilisateurs d'énergie, un quart des émissions de CO₂ n'était soumis
à aucun prix, et 31 % l'était au-dessus de 120 € la tonne. Mais cette moyenne cache tout :

| Secteur | non tarifé | moins de 30 € | 30 à 60 € | plus de 60 € |
|---|---:|---:|---:|---:|
| Transport routier | 0 % | 0 % | 6 % | 94 % |
| Électricité | 19 % | 0 % | 81 % | 0 % |
| Bâtiments | 36 % | 3 % | 60 % | 0,5 % |
| Industrie | 41 % | 7 % | 45 % | 6 % |
| Transport hors route | 52 % | 0 % | 42 % | 6 % |
| Agriculture et pêche | 21 % | 78 % | 0,3 % | 0,5 % |

Le mécanisme du gaspillage est direct. Un automobiliste renonce à un déplacement dont la
valeur pour lui est de 115 € par tonne évitée, pendant qu'un industriel conserve un procédé
dont la décarbonation ne lui coûterait que 40 € la tonne. On achète la tonne chère et on
laisse la tonne bon marché. À rendement identique, un prix uniforme achèterait davantage de
réduction.

Le cas de l'électricité est le plus perturbant. C'est l'énergie la moins carbonée du bouquet
français, et 81 % de ses émissions supportent un prix compris entre 30 et 60 € la tonne,
contre 0,5 % pour les bâtiments. Autrement dit, la fiscalité renchérit le vecteur dont la
décarbonation dépend.

En comparaison internationale, la France tarife 33 % de ses émissions au-dessus de 60 € la
tonne, derrière le Royaume-Uni (41 %), l'Italie, l'Espagne et les Pays-Bas (38 %), devant
l'Allemagne (23 %) et la Pologne (20 %).

### 4.2 Les taux marginaux effectifs

Le chapitre 4 construit, pour chaque niveau de salaire et chaque configuration familiale, le
taux effectif de prélèvement résultant de l'empilement complet : cotisations, impôt, et
retrait des prestations. Le modèle TaxBEN de l'OCDE produit l'équivalent pour la France.

Pour un passage d'un mi-temps à un temps plein, en 2025, avec demande du revenu minimum
garanti :

| Type de ménage | au salaire minimum | à 67 % du salaire moyen | au salaire moyen |
|---|---:|---:|---:|
| Célibataire sans enfant | 32 % | 51 % | 47 % |
| Célibataire, deux enfants | 32 % | 44 % | 41 % |
| Couple sans enfant | 32 % | 44 % | 49 % |
| Couple, deux enfants | 32 % | 44 % | 54 % |

Deux choses sautent aux yeux. D'abord le profil n'est pas monotone : pour un célibataire sans
enfant, le taux marginal est plus élevé à 67 % du salaire moyen qu'au salaire moyen. C'est
exactement le genre de creux et de bosse que la Review reproche au système britannique, et
qu'aucune décision n'a voulu : il résulte de la superposition d'instruments conçus séparément.

Ensuite, le niveau. À 67 % du salaire moyen, un célibataire sans enfant conserve 49 centimes
sur chaque euro supplémentaire en France, contre 73 au Royaume-Uni, 74 aux États-Unis et en
Suède, et 57 en Allemagne. Seule la Belgique fait plus (62 %).

### 4.3 Les taux de participation

Le taux de participation mesure ce qui reste d'un salaire quand on quitte le revenu minimum
pour un emploi. C'est la variable qui commande la décision de travailler ou non, distincte de
celle qui commande le nombre d'heures.

Pour un célibataire sans enfant français en 2025, la reprise d'emploi au salaire minimum
laisse 57 % du salaire, et 51 % à 67 % du salaire moyen. La France est proche de la moyenne de
l'OCDE, loin de la Belgique où il ne reste que 31 %, et loin aussi du Royaume-Uni et des
États-Unis où il reste plus des deux tiers.

Le point méthodologique mérite d'être noté : contrairement au taux marginal, le taux de
participation français est relativement plat entre le salaire minimum et le salaire moyen. Le
problème français n'est donc pas d'abord l'incitation à reprendre un emploi, c'est
l'incitation à augmenter son temps de travail une fois en emploi.

## 5. Ce que ces répliques ne disent pas

Trois limites, qui définissent le travail restant.

Le modèle TaxBEN raisonne sur des cas types, pas sur une population. Les figures 4.5 à 4.8 de
la Review sont construites sur l'ensemble des travailleurs britanniques, ce qui donne une
distribution et non quelques points. L'équivalent français demande une microsimulation sur
données d'enquête ou administratives.

Les transitions mesurées sont discrètes : du mi-temps au temps plein, de l'inactivité à
l'emploi. La courbe continue de taux marginal, celle qui révélerait les pics locaux aux
seuils de la prime d'activité ou des allègements de cotisations, n'y est pas.

Enfin, les données carbone s'arrêtent à 2021 et ne reflètent donc ni le gel de la composante
carbone ni les évolutions récentes du prix des quotas.

## 6. Ce que ces répliques disent déjà

Les trois diagnostics convergent vers la même conclusion de méthode. Dans les trois cas, le
problème français n'est pas le niveau du prélèvement mais sa dispersion : des prix du carbone
qui vont de zéro à plus de 120 € la tonne pour un dommage identique, et des taux marginaux qui
varient de 32 à 54 % selon la configuration familiale et le niveau de salaire, sans qu'aucune
décision n'ait voulu ce profil.

C'est précisément l'argument de neutralité du chapitre 2 : ce qui coûte, ce n'est pas tant de
prélever que de prélever différemment des situations semblables.
