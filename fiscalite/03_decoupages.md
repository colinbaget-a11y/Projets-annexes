# Découper les prélèvements français selon ce qu'ils font

La nomenclature comptable répond à une question d'enregistrement : à quel moment du circuit
l'argent est pris. Elle range la contribution sociale de solidarité des sociétés et la taxe
foncière dans la même case, « autres impôts sur la production », alors que la première est
une taxe en cascade sur le chiffre d'affaires et la seconde, pour partie, une taxe sur une
rente foncière. Pour juger un système, il faut découper autrement.

Les quatre découpages qui suivent reprennent les propositions du chapitre 2. Chaque
prélèvement de la liste française a été classé à la main au-delà de 50 M€, par règle en
dessous ; 99,9 % du produit est classé à la main. Le détail ligne par ligne, avec le motif de
chaque affectation, est dans `donnees/classification_prelevements.csv`. Les affectations sont
discutables et doivent l'être : c'est l'intérêt de les publier.

Le champ couvre 1 274,9 Md€ en 2024, soit les 121 impôts de la liste Eurostat plus les
cotisations sociales effectives, soit 43,4 % du PIB.

## Découpage 1 — Ce qui est réellement taxé

| Assiette économique | Md€ | % du PIB | part |
|---|---:|---:|---:|
| Travail (cotisations et taxes sur les salaires) | 490,3 | 16,70 | 38,5 % |
| Consommation des ménages | 261,0 | 8,89 | 20,5 % |
| Revenu global (impôt sur le revenu, CSG, CRDS) | 258,5 | 8,81 | 20,3 % |
| Bénéfice des sociétés | 90,0 | 3,06 | 7,1 % |
| Détention de patrimoine | 48,0 | 1,64 | 3,8 % |
| Énergie | 43,3 | 1,47 | 3,4 % |
| Intrants et facteurs de production | 28,4 | 0,97 | 2,2 % |
| Transmission | 20,8 | 0,71 | 1,6 % |
| Transaction | 17,2 | 0,59 | 1,3 % |
| Revenus du capital des ménages | 15,6 | 0,53 | 1,2 % |
| Rentes | 1,6 | 0,05 | 0,1 % |

Trois enseignements.

Le travail supporte 38,5 % du total, et ce chiffre ne dit encore rien de la distorsion, parce
qu'une cotisation qui ouvre un droit individuel proportionnel n'est pas un impôt à la marge.
Le point de passage obligé du rapport est donc la mesure de la contributivité : quelle part
des 490 Md€ achète un droit, quelle part finance une dépense universelle. Tant que cette part
n'est pas établie, le débat sur le coût du travail reste indécidable.

Le capital est taxé sous quatre formes qui s'ignorent : 90 Md€ sur le bénéfice des sociétés,
48 Md€ sur la détention, 20,8 Md€ sur la transmission, 15,6 Md€ sur les revenus. Aucune
cohérence ne relie les quatre. Un même euro de patrimoine peut être frappé zéro, une ou
quatre fois selon sa forme juridique et le moment considéré.

Les rentes, que la théorie désigne comme la meilleure assiette possible, rapportent 1,6 Md€,
soit 0,05 % du PIB. Les transactions, que la même théorie désigne comme la pire, rapportent
dix fois plus.

## Découpage 2 — L'efficience productive

Le critère est celui de Diamond et Mirrlees : un prélèvement qui frappe un facteur ou une
consommation intermédiaire pousse les entreprises à produire autrement qu'au moindre coût,
et fait perdre de la production sans rien acheter en échange, sauf s'il corrige un dommage.

| | Md€ | % du PIB |
|---|---:|---:|
| Frappe clairement un intrant | 119,3 | 4,06 |
| dont justifié par une externalité | 42,2 | 1,44 |
| **dont sans justification correctrice** | **77,0** | **2,62** |
| Frappe partiellement un intrant | 574,4 | 19,57 |
| Ne frappe pas d'intrant | 581,2 | 19,80 |

Les 77 Md€ sans justification correctrice sont le cœur du problème français. On y trouve la
taxe sur les salaires, le versement mobilité, les contributions formation et apprentissage,
la cotisation foncière des entreprises, la contribution sociale de solidarité des sociétés,
les taxes sur les surfaces et les bureaux, les impositions de chambres consulaires, et une
trentaine de taxes sectorielles sur le chiffre d'affaires.

La catégorie intermédiaire mérite une explication, car elle est énorme. Elle contient d'abord
les cotisations patronales, 293 Md€, qui sont un prélèvement sur un facteur mais dont la
nature dépend de la contributivité. Elle contient ensuite la TVA, 206 Md€, qui est neutre tant
que la chaîne de déduction est complète, et qui ne l'est pas : les secteurs exonérés ne
récupèrent pas la taxe payée sur leurs achats, elle reste incorporée dans leurs prix et se
retrouve taxée en aval. Cette rémanence n'est pas isolable dans la source utilisée ; la
chiffrer est un des travaux à mener.

La contribution sociale de solidarité des sociétés mérite une mention particulière, parce
qu'elle illustre exactement le mécanisme. Assise sur le chiffre d'affaires, elle est acquittée
à chaque stade sur un montant qui contient déjà la taxe payée en amont. Deux économies
produisant la même chose supportent donc une charge différente selon le nombre d'entreprises
que traverse le produit, et la fiscalité devient une prime à l'intégration verticale.

## Découpage 3 — Les prélèvements correcteurs

| | Md€ | % du PIB |
|---|---:|---:|
| Correcteurs | 56,6 | 1,93 |
| Partiellement correcteurs | 19,9 | 0,68 |
| Non correcteurs | 1 198,4 | 40,83 |

Pour ces 56,6 Md€, le rendement n'est pas le critère. Un prélèvement correcteur est bien
calibré quand son taux égale le dommage et qu'il est le même pour tous ceux qui causent ce
dommage. Le travail à mener est donc de nature différente : il ne s'agit pas de mesurer un
rendement mais de reconstituer, pour chaque énergie et chaque usage, le prix implicite de la
tonne de CO₂, puis de mesurer sa dispersion. Une fiscalité carbone hétérogène achète moins de
tonnes évitées qu'une fiscalité uniforme de même rendement.

Un cas se signale déjà : l'accise sur l'électricité, 4,8 Md€, frappe l'énergie la moins
carbonée du bouquet français, donc décourage le report qui constitue le principal levier de
décarbonation.

## Découpage 4 — Lecture au regard des principes

Ce découpage est une lecture, pas une mesure. Il attribue à chaque prélèvement la conséquence
qu'aurait l'application des principes du chapitre 2. Il est présenté pour être contesté.

| Conséquence | Md€ | % du PIB |
|---|---:|---:|
| Fusionner dans un prélèvement unique sur le revenu du travail | 433,5 | 14,77 |
| Fusionner impôt sur le revenu, CSG et CRDS | 265,9 | 9,06 |
| Conserver tel quel, assiette large et taux unique | 206,3 | 7,03 |
| Refondre pour exonérer le rendement normal | 83,6 | 2,85 |
| Refondre la fiscalité foncière, séparer terrain et bâti | 50,3 | 1,71 |
| Supprimer | 48,4 | 1,65 |
| Refondre | 41,8 | 1,42 |
| Unifier le prix du carbone | 38,8 | 1,32 |
| Conserver comme correcteur | 31,1 | 1,06 |
| À identifier avant de juger | 27,3 | 0,93 |
| Refondre l'assiette des transmissions | 20,8 | 0,71 |
| Supprimer en même temps qu'on élargit la TVA | 17,3 | 0,59 |

Un seul prélèvement, la TVA, passe le test sans réserve, et encore à condition de supprimer
ses taux réduits et de traiter les exonérations. Le reste demande une refonte d'assiette, une
fusion ou une suppression. Et 27,3 Md€ ne peuvent pas être jugés parce que la source publique
ne les nomme pas.

## Ce que ces découpages commandent comme travaux

1. **Mesurer la contributivité des 490 Md€ assis sur le travail.** Sans cela, on ne sait pas
   quelle part est un impôt et quelle part est un prix.
2. **Chiffrer la TVA rémanente**, c'est-à-dire la taxe non déduite par les secteurs exonérés,
   et son effet de cascade.
3. **Séparer terrain et bâti** dans les 50 Md€ de fiscalité foncière.
4. **Reconstituer les prix implicites du carbone** par énergie et par usage.
5. **Nommer les 27 Md€** que la source laisse en « autres taxes ».
6. **Estimer la part du rendement normal** dans les assiettes de l'impôt sur les sociétés et
   des prélèvements sur les revenus du capital, puisque c'est elle que la théorie recommande
   d'exonérer.
