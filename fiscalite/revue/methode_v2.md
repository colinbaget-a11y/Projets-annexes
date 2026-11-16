# Méthode de perte sèche, version 2 (16/11/2026)

Demande de l'auteur : ne pas laisser l'optimiseur décider ; coin total ; distinguer réactions réelles et
déclaratives ; marges intensive et extensive ; raisonner en écart à l'existant avec des hypothèses basses,
centrales, hautes et prudentes ; comparer quelques architectures simples et mesurer les rendements décroissants.
Les élasticités viennent de `cours/elasticites-france.tex` (chiffres relus dans les études).

## 1. Diagnostic de la version 1

| Point | Version 1 | Problème | Correction |
|---|---|---|---|
| Coin total | Oui : IR-CSG + cotisations non contributives + retrait de la prime d'activité ; marge extensive comprise | La quantité réagissait au taux net *total*. Or le salaire réagit au taux de l'IR et pas aux cotisations (Lehmann, Marical et Rioux, 2013), et trois fois moins au retrait des prestations (Sicsic, 2022). Cela gonflait la réaction là où les cotisations sont lourdes. | La quantité réagit au taux de l'impôt fusionné ; chaque euro perdu coûte le coin total non contributif. |
| Réel / déclaré | Une seule élasticité du revenu imposable : 0,15 dans la moitié du bas, 0,20 entre 50 et 90 %, 0,30 entre 90 et 99 %, 0,40 au 1 % ; 50 % de la réaction du haut supposée déplacée vers l'IS et le PFU | Le gain venait à plus de 90 % du dixième du haut, par une élasticité qui mesure surtout la forme, la date et la déclaration des revenus. | Élasticité du revenu réellement produit, faible et la même partout au-dessus de la médiane. La réaction déclarative du dixième du haut est comptée à part comme un effet sur la recette, net du déplacement vers l'IS et le PFU. Elle n'entre pas dans le gain d'efficacité. |
| Comportements | Élasticité intensive de 0,15 à 0,40, plus η = 0,25 sous 2 Smic | La marge intensive, trop forte en bas, absorbait ce qui relève de la participation (chez Lehmann et al., la réaction passe par les mois travaillés ; 0,03 pour les salariés modestes employés toute l'année). | Marge intensive faible (0,05 en bas, 0,10 au-dessus). La participation est modélisée par η sur le taux de prélèvement du premier salaire, sous 2 Smic. |
| Écart à l'existant | Oui (variation par rapport à aujourd'hui), avec trois jeux | Le jeu central n'était pas prudent. | Trois jeux, central prudent (tableau 2). |
| Optimiseur | La référence était le barème qui minimise la perte sèche | La référence était radicale (dernier décile −5 200 € par foyer, 54 % de perdants) et décidée par le modèle. | La référence devient le barème qui s'écarte le moins de ce que chacun paie aujourd'hui. L'optimum reste calculé, pour mémoire, comme mesure du gain atteignable. |

## 2. Calibrage (modele_purs.V2)

| | Bas | Central | Haut | Appui |
|---|---|---|---|---|
| Revenu réel, moitié du bas | 0,02 | 0,05 | 0,10 | LMR 2013 : 0,03 pour les salariés modestes employés toute l'année ; Cabannes et al. 2014 : non significatif des déciles 2 à 9 |
| Revenu réel, 50-90 % | 0,05 | 0,10 | 0,20 | Sicsic 2022 : 0,33 pour le revenu d'activité, réaction de court terme surtout par les mois travaillés |
| Revenu réel, 90-99 % et 1 % | 0,05 | 0,10 | 0,25 | aucune séparation mesurée du réel et du déclaratif ; même valeur qu'au milieu par prudence |
| Revenu déclaré, 90-99 % / 1 % | 0,10 / 0,15 | 0,20 / 0,30 | 0,30 / 0,45 | total réel + déclaré ≈ 0,30 au centre (Cabannes et al. : 0,31, de 0,15 à 0,45) ; 0,51 chez Sicsic pour le revenu d'activité |
| Participation η (sous 2 Smic) | 0,10 | 0,25 | 0,50 | Chetty, Guren, Manoli et Weber 2011 : 0,25 ; effets faibles du RSA sur l'emploi ; Carbonnier 2021 : 1 à 2 pour les femmes mariées (résumé seulement) |
| Déplacement du revenu déclaré | s = 0,5 vers 48,6 % | | | convention ; aucune estimation française |

Formules :
- **Marge intensive.** ΔQ = e·g·Δln(1−t), où t est le taux marginal de l'impôt fusionné. La variation de perte sèche vaut −(coin moyen)·ΔQ. Le coin moyen est la moyenne, entre avant et après, de t + cotisations non contributives salariales et patronales + retrait de la prime d'activité.
- **Marge extensive.** Elle est inchangée : η sur le taux de prélèvement de la reprise d'emploi, sous 2 Smic.
- **Revenu déclaré.** L'effet sur la recette vaut (coin moyen − s·48,6 %)·ΔQ_déclaré. Il est présenté à part.
- **Prix d'un milliard.** C'est la perte sèche réelle d'un milliard levé par un point de taux pour tous : 0,03 / 0,07 / 0,14 autour du barème neutre, 0,04 / 0,08 / 0,17 avec franchise, enfants et petites pensions (`architectures_ircsg.txt`, [PRIX]). Il remplace 0,16 / 0,38 / 0,60 dans `perte_seche_autres.py`.

## 3. Résultats IR-CSG (`synthese/architectures_ircsg.py`, sorties `architectures_ircsg.txt`)

Toutes les architectures sont à recette constante (220 Md€). Perte sèche réelle en variation par rapport à aujourd'hui, en Md€ par an : centrale, avec la fourchette basse–haute entre parenthèses.

- **Gain atteignable** (meilleur barème simple, franchise d'activité de 4 000 € comprise) : −7,8 (−3,8 à −18,2).
  - Cet optimum aplatit le barème : 16 % jusqu'à 60 000 €, 50 % au-delà de 2 M€.
  - Le dernier décile y gagne 25 Md€, et 49 à 58 % des foyers perdent plus de 500 €.
- **Barème neutre** (2 % au premier euro, 14 % à 20 k€, 23 % à 30 k€, 50 % à 250 k€) : −4,0 (−1,9 à −9,2), soit la moitié du gain atteignable.
  - Aucun décile ne bouge de plus de 600 €. Les retraités paient 7 Md€ de plus. 25 % des foyers perdent plus de 500 €.
  - Le gain vient du dixième du haut, dont le taux marginal baisse alors que son taux moyen monte un peu (fin des niches), et de la participation des bas salaires (−1,8), grâce à un taux d'entrée de 2 % au lieu des 9,7 % de CSG-CRDS.
- **Franchise d'activité.** Avec 4 000 €, le neutre passe à −4,6 (59 %) ; avec 8 000 €, à −5,0 (64 %).
  - La franchise est le seul dispositif qui *augmente* le gain, par la marge extensive.
  - Elle reporte la charge sur les retraités : +14 et +21 Md€.
- **Ce qui coûte du gain.** Aide aux enfants, petites pensions, abattement sur les pensions, quotient : de 0,1 à 0,9 Md€ chacun.
- **Proposition.** Le barème est le plus efficace parmi ceux qui ne changent aucun décile de plus de 500 € et n'alourdissent pas le 1 % du haut, avec une franchise d'activité, 6 000 € par enfant et les petites pensions exonérées.
  - Franchise de 4 000 € : −4,9 (−2,3 à −11,1), soit 63 % du gain atteignable ; retraités +15 Md€ ; couples avec deux enfants −1 200 € par foyer.
  - Franchise de 8 000 € : −5,2 (67 %) ; retraités +23 Md€.
- **Rendements décroissants** (chemin du barème neutre vers l'optimum) :
  - 30 % du chemin portent la part de 52 à 69 %, alors que le dernier décile passe de +2,5 à −6 Md€.
  - Les derniers 30 % du gain demandent de rendre 20 à 25 Md€ au dernier décile, et la moitié des foyers perdent plus de 500 €.
- **Revenu déclaré.** Effet sur la recette de +3 à +4 Md€ pour le neutre et la proposition (+6,5 pour l'optimum), avec une fourchette de 1,5 à 6.
- **Très hauts revenus** (`controle_hauts_purs.txt`). Pour les 3 800 foyers au-delà de 3 M€, le résultat dépend de la part (non publiée) de leurs revenus au PFU.
  - Si leurs revenus du barème paient aujourd'hui ce que dit le barème légal (44 à 49 %), la proposition baisse leur impôt, sauf au-delà de 9 M€ (+1 point).
  - Dans la convention centrale, qui leur prête un taux actuel de 32 à 37 %, ils paieraient 2 à 16 points de plus.
  - La comparaison ne compte pas la CEHR, qui disparaîtrait sur les revenus du barème.

Réponse à la question des rendements décroissants : on obtient environ deux tiers du gain atteignable sans
bouleverser la répartition par décile, pas 80 %. Le dernier tiers demande une forte baisse d'impôt pour le dernier
décile. Le prix réel de la prudence est ailleurs : quelle que soit l'architecture, l'essentiel du gain est
financé par l'alignement des retraités, qui paient de 7 à 23 Md€ de plus.

## 4. Autres réformes

Elles respectaient déjà la séparation entre réel et déclaratif :
- **Foncier.** Mobilité et construction, deux réactions réelles.
- **IS.** Le triangle sur l'investissement est réel ; le transfert de bénéfices est compté à part, selon son coût réel κ.
- **PFU.** La réaction des dividendes est surtout un report.

Seul change le prix d'un milliard. PFU à 25 % : +0,3 Md€ (0,15 à 0,6) au lieu de +1,4, sans gain réel mesuré.
