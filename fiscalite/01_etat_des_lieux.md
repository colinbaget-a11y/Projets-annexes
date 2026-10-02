# État des lieux des prélèvements obligatoires français

Premier chapitre du projet. Objet : savoir ce que l'on taxe, pour combien, et où sont les
défauts de construction. Tous les chiffres de ce document sortent des fichiers de `donnees/`
et sont reproductibles par `panorama.py` ; les douze figures sont produites par
`graphiques.py` et décrites dans `figures/INDEX.md`. Les affirmations institutionnelles qui ne
s'appuient pas encore sur une source téléchargée sont marquées **[à sourcer]**.

## 1. Le socle de données

La source centrale est la *National Tax List* que la France transmet chaque année à Eurostat
avec la table 0900 du programme SEC 2010. C'est le seul fichier qui donne, impôt par impôt,
le rendement, le code SEC et la fonction économique, de 1995 à 2024. L'extrait français
compte 121 prélèvements distincts, dont la somme reproduit exactement l'agrégat comptable
des recettes fiscales (843 800 M€ en 2024), ce qui garantit qu'aucune ligne n'est oubliée ni
double-comptée.

Un piège mérite d'être signalé : la liste contient deux codages parallèles de l'impôt sur le
revenu (D51M reprend D51A, D51O reprend D51B). Les sommer double-compte 359 Md€.

Deux limites à retenir pour la suite. D'abord, les cotisations sociales n'y figurent que par
agrégats : 482 Md€ sans aucun détail par régime ni par assiette. Ensuite, la liste laisse des
postes non nommés, dont deux gros : 13,4 Md€ d'« autres taxes » sur les bénéfices des
sociétés et 8,6 Md€ d'« autres taxes sur des services spécifiques ». La CVAE et la taxe
d'habitation ont une ligne mais sans aucune valeur renseignée. Au total, nommer chaque
prélèvement demandera de passer par les sources françaises : *Voies et moyens* tome I, la
liste des taxes affectées, les annexes au PLFSS.

## 2. Combien, et sur quoi

| Bloc | 2024, M€ | % du PIB | % du total |
|---|---:|---:|---:|
| Cotisations sociales nettes | 482 281 | 16,4 | 38,0 |
| Impôts sur la production et les importations | 456 277 | 15,5 | 35,9 |
| Impôts courants sur le revenu et le patrimoine | 366 049 | 12,5 | 28,8 |
| Impôts en capital | 21 474 | 0,7 | 1,7 |
| **Total hors cotisations imputées** | **1 270 244** | **43,3** | 100 |
| Total y compris cotisations imputées | 1 321 460 | 45,0 | |

Le PIB 2024 est de 2 935 Md€. L'écart entre les deux totaux, 51 Md€, tient aux cotisations
imputées : les pensions de fonctionnaires que l'État se verse à lui-même, comptabilisées
comme une cotisation sans flux réel. Le périmètre français usuel des prélèvements
obligatoires correspond à la ligne en gras.

Deux traits structurels sortent de ce tableau. Le premier est la place des cotisations
sociales, qui restent le premier bloc à 38 % du total. Le second est le poids des impôts sur
la production et les importations, 15,5 points de PIB, dont un tiers n'est pas de la TVA mais
des taxes assises sur la production elle-même : 129 Md€ d'« autres impôts sur la production »,
c'est-à-dire des prélèvements dus indépendamment du résultat de l'entreprise.

La déformation depuis 1995 est plus instructive que le niveau.

| En % du PIB | 1995 | 2010 | 2024 | écart |
|---|---:|---:|---:|---:|
| Cotisations sociales | 19,87 | 18,05 | 16,43 | −3,44 |
| Impôts sur le revenu des ménages | 5,15 | 7,68 | 9,37 | +4,23 |
| Impôts sur les sociétés | 1,77 | 2,31 | 2,85 | +1,09 |
| TVA | 7,34 | 6,81 | 7,03 | −0,31 |
| Autres impôts sur la production | 4,12 | 4,13 | 4,40 | +0,28 |
| Autres impôts courants | 1,10 | 1,14 | 0,24 | −0,86 |
| Impôts en capital | 0,35 | 0,39 | 0,73 | +0,38 |
| **Total** | **42,15** | **42,28** | **43,28** | **+1,13** |

Le taux global a peu bougé en trente ans, mais sa composition a basculé. Les cotisations ont
reculé de 3,4 points de PIB, les impôts sur le revenu des ménages en ont gagné 4,2. Ce n'est
pas l'impôt sur le revenu qui a absorbé ce transfert : il passe de 3,49 % à 3,28 % du PIB sur
la période. C'est la CSG, qui passe de 1,18 % à 5,22 % du PIB. La chute des « autres impôts
courants » de 1,14 à 0,24 point entre 2010 et 2024 est la suppression de la taxe d'habitation
sur les résidences principales.

## 3. Trois impôts font la moitié du produit fiscal

| Rang | Prélèvement | 2024, M€ | % du PIB |
|---:|---|---:|---:|
| 1 | TVA | 206 332 | 7,03 |
| 2 | Contribution sociale généralisée | 153 131 | 5,22 |
| 3 | Impôt sur le revenu | 96 163 | 3,28 |
| 4 | Impôt sur les sociétés | 67 998 | 2,32 |
| 5 | Taxe foncière sur le bâti | 42 059 | 1,43 |
| 6 | Accise sur les produits énergétiques (TICPE) | 29 554 | 1,01 |
| 7 | Mutations à titre gratuit (DMTG) | 20 819 | 0,71 |
| 8 | Taxe sur les salaires | 17 315 | 0,59 |
| 9 | Droits d'enregistrement (DMTO) | 14 663 | 0,50 |
| 10 | Autres prélèvements sociaux sur les revenus du capital | 14 646 | 0,50 |
| 11 | Accise sur les tabacs | 13 606 | 0,46 |
| 12 | Autres impôts sur les bénéfices des sociétés | 13 387 | 0,46 |
| 13 | Versement mobilité | 12 231 | 0,42 |
| 14 | Contributions formation professionnelle et apprentissage | 11 359 | 0,39 |
| 15 | Taxe spéciale sur les conventions d'assurance | 10 031 | 0,34 |

Hors cotisations sociales, 3 prélèvements font 50 % du produit fiscal, 8 en font 75 %, 21 en
font 90 %. À l'autre bout, 34 prélèvements rapportent moins de 150 M€ chacun, pour 643 M€
cumulés, soit 0,08 % du produit fiscal. Vingt-deux d'entre eux ont un rendement nul ou non
renseigné : ce sont des impôts qui existent juridiquement sans produire de recette.

## 4. Les blocs, un par un

### 4.1 La TVA — 206 Md€, 7,0 % du PIB

Assiette : la consommation finale, avec quatre taux (20 %, 10 %, 5,5 %, 2,1 %) et un jeu
d'exonérations.

Les taux réduits sont un instrument redistributif très coûteux par euro effectivement
transféré. Le mécanisme est arithmétique : un ménage aisé dépense moins que les autres en
alimentation *en proportion* de son revenu, mais davantage *en valeur absolue*. Un point de
TVA en moins sur l'alimentation lui rapporte donc plus d'euros qu'à un ménage modeste. Pour
atteindre le ménage modeste, il faut consentir la dépense sur toute la distribution.

Les exonérations posent un problème différent, et moins visible. Un secteur exonéré — santé,
banque, assurance, enseignement — ne facture pas de TVA mais ne récupère pas celle qu'il a
payée sur ses consommations intermédiaires. Cette TVA reste donc incorporée dans son prix de
vente et se retrouve taxée une seconde fois en aval : une cascade. Deux conséquences
concrètes : le secteur exonéré est incité à internaliser ce qu'il achetait à l'extérieur
(produire soi-même sa comptabilité ou son informatique évite la TVA non déductible), et une
prestation identique est taxée différemment selon qu'elle est achetée ou produite en interne.
La taxe sur les salaires, 17,3 Md€, est le contrepoids administratif de cette exonération :
faute de pouvoir taxer la valeur ajoutée de ces secteurs, on taxe leur masse salariale.

### 4.2 Les prélèvements assis sur le travail

Cotisations sociales 482 Md€, CSG 153 Md€, impôt sur le revenu 96 Md€, taxe sur les salaires
17 Md€, versement mobilité 12 Md€, formation et apprentissage 11 Md€, forfait social 6 Md€.

Le premier défaut est structurel : **la France a deux impôts sur le revenu**. L'impôt sur le
revenu est familialisé, progressif, à assiette étroite ; la CSG est individuelle,
proportionnelle, à assiette large, et rapporte 1,6 fois plus. Ils ne partagent ni l'unité
d'imposition, ni la définition du revenu, ni les règles d'abattement, ni l'administration.
Toute réforme de la progressivité porte donc sur le plus petit des deux, ce qui en démultiplie
le coût pour un effet redistributif donné.

Le deuxième défaut tient à l'empilement. Ce qu'un employeur paie en plus pour augmenter un
salarié dépend de la superposition des cotisations, des allègements généraux dégressifs, de la
CSG, de l'impôt sur le revenu, et du retrait des prestations sous condition de ressources.
Comme les allègements se retirent à mesure que le salaire monte, le coût pour l'employeur
d'un euro net supplémentaire croît fortement entre le SMIC et environ 1,6 SMIC **[à sourcer :
profil exact des taux marginaux effectifs]**. Personne n'a décidé ce profil : il est le
sous-produit de dispositifs empilés indépendamment, chacun défendable isolément.

### 4.3 Le capital des ménages

Quatre assiettes distinctes, et des traitements sans cohérence entre elles.

- **Les revenus** : prélèvement forfaitaire unique à 30 % sur les revenus mobiliers, dont
  14,6 Md€ de prélèvements sociaux, avec option pour le barème.
- **Le stock** : impôt sur la fortune immobilière, 2,7 Md€, qui ne porte que sur l'immobilier
  depuis 2018. Deux patrimoines de même valeur sont imposés très différemment selon leur
  composition.
- **Les transmissions** : 20,8 Md€ de droits de mutation à titre gratuit. Les taux faciaux
  sont parmi les plus élevés de l'OCDE, l'assiette est l'une des plus étroites : abattements
  renouvelables, régime de l'assurance-vie, exonération partielle Dutreil, purge des
  plus-values latentes au décès **[à sourcer : chiffrage de chaque dispositif]**. Le seul
  pacte Dutreil est chiffré à 4,0 Md€ pour 2026, après une révision à la hausse de 4,2 Md€
  d'une année sur l'autre, ce qui dit l'incertitude sur son coût réel.
- **Les transactions** : 14,7 Md€ de droits d'enregistrement. Taxer la mutation plutôt que la
  détention décourage les réallocations : un ménage qui déménage pour un meilleur emploi paie
  plusieurs points du prix du logement, un ménage qui reste ne paie rien. C'est une taxe sur
  le fait de bouger, pas sur la richesse.

La taxe foncière, 42 Md€, mérite un point à part. Son assiette repose sur les valeurs
locatives cadastrales établies en 1970 pour les locaux d'habitation, actualisées depuis par
des coefficients forfaitaires. La révision des locaux professionnels a eu lieu, celle des
locaux d'habitation a été reportée **[à sourcer : état actuel du calendrier]**. L'assiette
n'a donc plus de rapport systématique avec la valeur des biens, et deux propriétaires de
patrimoine identique paient des montants différents selon la structure du parc en 1970.

### 4.4 Les entreprises

Impôt sur les sociétés 68 Md€, plus 13,4 Md€ d'autres impôts sur les bénéfices. À côté, les
impôts de production : cotisation foncière des entreprises 7,7 Md€, contribution sociale de
solidarité des sociétés 5,2 Md€, impositions forfaitaires sur les entreprises de réseaux
1,9 Md€, versement mobilité 12,2 Md€, et la part des 42 Md€ de taxe foncière acquittée par
les entreprises.

Ces prélèvements ont une propriété commune qui les sépare de l'impôt sur les sociétés : ils
sont assis sur le chiffre d'affaires, la valeur locative ou la masse salariale, donc dus même
lorsque l'entreprise perd de l'argent. Trois effets suivent. Ils frappent plus durement les
activités à faible marge et à forte intensité capitalistique. Ils se cumulent le long de la
chaîne de production, puisque chaque stade paie sur un chiffre d'affaires qui incorpore déjà
la taxe acquittée en amont — c'est le reproche classique fait à la C3S. Et ils pèsent sur la
décision d'investir en France indépendamment de sa rentabilité.

### 4.5 Énergie et environnement

Douze prélèvements identifiés comme environnementaux dans la liste Eurostat, 43,6 Md€, soit
1,49 % du PIB. La TICPE en représente les deux tiers.

Le défaut central n'est pas le niveau mais la dispersion. Le prix implicite de la tonne de CO₂
varie fortement selon l'énergie et selon l'usage, du fait des tarifs réduits et exonérations
sectorielles, et la composante carbone de la TICPE est gelée depuis 2018 **[à sourcer :
chiffrage des prix implicites par usage, travaux du CPO et de France Stratégie]**. Une
fiscalité carbone hétérogène achète moins de tonnes évitées qu'une fiscalité uniforme de même
rendement, puisque les abattements les moins chers ne sont pas ceux qui sont déclenchés.
L'électricité, peu carbonée en France, supporte 4,8 Md€ d'accise, ce qui décourage
l'électrification au moment où elle est l'instrument principal de décarbonation.

### 4.6 La fiscalité locale

Après la suppression de la taxe d'habitation sur les résidences principales et la réduction
de la CVAE, les ressources fiscales locales se concentrent sur la taxe foncière et sur des
fractions de TVA transférées. Le lien entre la base taxable et le territoire s'est distendu :
une collectivité qui accueille de l'activité ou des habitants n'en retire plus
mécaniquement de recette propre **[à sourcer : part des recettes locales encore assises sur
une base locale]**.

## 5. Les défauts transversaux

**Les dépenses fiscales.** 89,4 Md€ en 2024 (montant définitif), 91,8 Md€ attendus en 2025,
88,3 Md€ en 2026, selon le tome II des *Voies et moyens* annexé au PLF 2026. Quinze
dispositifs font plus de la moitié du coût. Les premiers sont le crédit d'impôt recherche
(8,0 Md€ en 2026), le crédit d'impôt pour l'emploi d'un salarié à domicile (7,2 Md€),
l'abattement de 10 % sur les pensions (4,7 Md€) et le pacte Dutreil (4,0 Md€). Rapporté au
produit, l'ordre de grandeur est parlant : les niches représentent environ 11 % des recettes
fiscales de l'État **[à sourcer : recettes fiscales nettes de l'État dans le PLF 2026]**.

**La longue traîne.** 34 prélèvements sous 150 M€ pour 643 M€ au total. Chacun a son assiette,
ses règles, ses obligations déclaratives et son coût de recouvrement. La question n'est pas
leur rendement mais le rapport entre ce rendement et le coût administratif et de conformité
qu'ils imposent **[à sourcer : rapport IGF sur les taxes à faible rendement]**.

**L'opacité résiduelle.** 22 Md€ de prélèvements ne sont pas nommés dans la liste publiée par
Eurostat. On ne peut pas discuter de la réforme d'un impôt qu'on ne sait pas désigner.

## 6. Ce qu'il reste à construire

1. **Nommer les 22 Md€ manquants** et réconcilier la liste Eurostat avec *Voies et moyens*
   tome I et la liste des taxes affectées.
2. **Détailler les 482 Md€ de cotisations sociales** par régime, par assiette et par taux,
   à partir des annexes au PLFSS et des données de l'URSSAF.
3. **Construire le barème effectif sur le travail**, c'est-à-dire le taux marginal de
   prélèvement tenant compte des cotisations, des allègements, de la CSG, de l'impôt sur le
   revenu et du retrait des prestations, du RSA à cinq fois le SMIC.
4. **Chiffrer les prix implicites du carbone** par énergie et par usage.
5. **Comparer** la structure française à celles de l'Allemagne, du Danemark, du Royaume-Uni
   et de la Suède, à partir des mêmes listes Eurostat déjà téléchargées pour les 27 pays.
6. **Mesurer la dispersion des valeurs locatives** par rapport aux valeurs de marché.
