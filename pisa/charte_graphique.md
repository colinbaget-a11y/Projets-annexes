# Charte graphique

Relevée sur les chapitres 5 et 16 du manuel (figures 5.1 à 5.6 et 16.1 à 16.6). À appliquer à toute
figure produite pour ce projet.

## Couleurs

Échantillonnées directement dans les PDF.

| Rôle | Hex | Usage observé |
|---|---|---|
| Bleu principal | `#003399` | série de référence, France, titres de section |
| Vert | `#1F7A4D` | deuxième famille (États-Unis ; actions calculées) |
| Or | `#C79100` | troisième famille (Japon ; technologies) |
| Grenat | `#A50020` | quatrième famille (Royaume-Uni) |
| Gris de série | `#808080` | série de contexte volontairement discrète (Allemagne) |
| Bleus secondaires | `#33619F`, `#6491C6`, `#98B8DD` | aplats, aires, empilements |
| Bande d'événement | `#E3E4E3` | guerres, récessions, périodes remarquables |
| Grille | `#EBECEB` | horizontale uniquement |
| Axe et ligne de zéro | `#1A1A1A` | trait fin plein |
| Annotation secondaire | `#AAAAAA` | écarts, repères, mentions |
| Fond d'encadré | `#FAEDF1` sur bordure `#D2C7CB` | encadrés « Débat », mises en garde |

**La couleur encode la nature de l'objet, pas seulement l'identité de la série.** Dans la figure 5.6, bleu,
or et vert distinguent trois familles d'estimations qui ne mesurent pas la même chose ; dans la figure 16.6,
le vert isole la mesure calibrée différemment des trois autres. C'est la convention la plus utile du manuel.

Contrôle de lisibilité : le couple grenat / vert n'est séparé que de 6,7 en deutéranopie, et l'or est à
2,8:1 sur fond blanc. Les deux sont acceptables **parce que** la charte étiquette chaque marque avec sa
valeur dans la couleur de la série ; ne jamais les faire voisiner sans étiquette.

## Typographie

Tout en serif, y compris les axes et les valeurs — le manuel est composé en Latin Modern. Sur écran,
Source Serif 4 en est l'équivalent le plus sobre. Chiffres en `tabular-nums` dès qu'ils s'alignent.
Écriture française : virgule décimale, espace fine avant `%`, signe moins typographique `−`.

## Anatomie d'une figure

**Titre au-dessus**, jamais dans le cadre : `Figure N.` en gras, puis la description en romain, l'unité
incluse dans la phrase. *« Figure 5.1. Dépense publique dans cinq grands pays, 1900-2024. En pourcentage
du PIB. »*

**Sources et note en dessous**, en corps réduit, label en italique : `Sources :` puis `Note :`. La note dit
ce que le graphique ne peut pas montrer — ruptures de série, changements de périmètre, ce que la barre
représente exactement.

**Dans le cadre :**

- grille horizontale seule, très pâle ; aucune grille verticale sauf repère explicite ;
- axes en trait fin ; ligne de zéro en trait plein noir quand l'échelle traverse zéro ;
- repère de référence en pointillé gris, avec son étiquette en gris au-dessus du cadre ;
- bandes grises pour les périodes remarquables, sans étiquette dans le cadre ;
- étiquettes de valeur à droite de la marque, **dans la couleur de la série** ; format `23,7` pour un point,
  `230 à 320` pour une fourchette ;
- annotations secondaires en gris, et seulement au-delà d'un seuil (dans la figure 5.2, l'écart à la zone
  euro n'est écrit que s'il dépasse un point de PIB) ;
- titre d'axe sous l'axe des abscisses, centré ; titre d'axe des ordonnées pivoté, coloré comme la série
  quand il n'y en a qu'une par axe ;
- aucun titre à l'intérieur du cadre.

**Légende** sans cadre : à l'intérieur en bas à droite pour les séries temporelles, sous le graphique et
centrée pour les barres et les plages. Traits pour les courbes, carrés pour les aplats.

**Proportions.** Mesurée sur les figures du manuel, l'aire de tracé des graphiques de séries longues fait
environ **1,5 de large pour 1 de haut** (figures 5.1 et 16.4), et les petits multiples 3:1 (figure 16.6).
Les graphiques en barres et en plages sont plats : leur hauteur suit le nombre de lignes, à raison de lignes
serrées (14 lignes tiennent dans la même hauteur qu'un demi-graphique de série). Une figure ne se compose
donc pas dans un cadre de format fixe : **le cadre suit le contenu**, sinon il se remplit de blanc.

**Formes retenues.** Séries longues : courbes de 1,5 à 2 points, sans marqueurs, interrompues là où la
source ne mesure rien. Comparaisons de catégories : barres horizontales triées, une seule couleur, valeur
en bout. Fourchettes d'estimations : segment horizontal avec un point rond, ou un point seul quand
l'estimation est unique. Comparaisons multi-dimensions : petits multiples côte à côte, un titre par volet.

**Ce que la charte s'autorise et que je n'aurais pas fait :** le double axe (figure 5.4), avec les deux
titres d'axe colorés comme leurs séries. À réserver aux cas où indexer les deux séries sur une base commune
détruirait l'information, et toujours avec les couleurs d'axe.
