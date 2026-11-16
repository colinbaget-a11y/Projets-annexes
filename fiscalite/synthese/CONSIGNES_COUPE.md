# Consignes de la coupe (17/11/2026), décision de l'auteur

La note est trop longue et trop bavarde. Trois consignes, dans cet ordre.

## 1. Ne pas redire ce que dit déjà le rapport commun

La note s'insère dans le rapport commun du think tank (`fiscalite/rapport-commun-docx.js`). Sa première partie,
« Qu'est-ce qu'un bon impôt ? », et sa deuxième, « La France a progressivement perdu le fil de sa fiscalité »,
exposent déjà, et la note ne doit donc PAS réexpliquer :
- la Déclaration de 1789 (nécessité, facultés, consentement, contrôle de l'emploi), le triangle financer / orienter
  / corriger, Tinbergen, Musgrave, Mirrlees Review ;
- la perte sèche expliquée par un échange rendu impossible (y compris l'exemple de la vente d'appartement empêchée
  par les droits de mutation), le coût qui croît comme le carré du taux, « assiette large, taux bas », Ramsey, la
  neutralité (deux revenus comparables, même impôt), Pigou, le classement de l'OCDE, la courbe de Laffer ;
- l'incidence (qui paie vraiment l'impôt) ; la justice qui se juge à l'échelle du système ;
- le niveau des prélèvements français (43-45 % du PIB, rang OCDE), la dépense qui l'explique ;
- l'histoire par couches : CSG créée en 1991 à 1,1 %, CRDS créée en 1996 « pour treize ans », niches qui se
  multiplient, « l'exonération des uns est payée par les autres » ;
- en termes généraux : les droits de mutation taxent le fait de déménager, l'épargne est taxée différemment selon
  l'enveloppe, les impôts de production taxent avant le bénéfice.

La note peut s'appuyer sur ces principes en une incise (« le principe d'une assiette large et d'un taux bas »), au
besoin avec un renvoi bref à « la première partie du rapport », mais ne les démontre plus. Ce qui reste propre à la
note : les faits chiffrés propres à chaque impôt, les études empiriques qui mesurent les réactions, les chiffrages,
les choix de conception, les arbitrages, la transition.

## 2. Mettre beaucoup moins en avant les choix sur le 1 % et les familles

On ne change AUCUN chiffrage. Mais la neutralité du 1 % le plus aisé et le geste un peu favorable aux familles ne sont
plus présentés comme des objectifs ou des contraintes affichés (ni dans les titres, ni en tête de section, ni comme
« contrainte » numérotée).
- Le cadre affiché est la **neutralité distributive** : chaque réforme est calibrée pour rapporter autant et pour
  laisser la répartition de la charge à peu près inchangée, de façon à isoler le gain d'efficacité de tout choix de
  redistribution, qui relève d'un choix collectif (c'est la position de la première partie du rapport). Cette
  présentation est exacte : c'est bien ce que font les contraintes (déciles à ±500 € près, haut inchangé).
- Les résultats restent dans la note, sobrement, comme résultats (« qui paie ») : effets par décile, effet sur le
  1 % quand il est significatif, cas-types familiaux. Ne pas supprimer d'information distributive importante (en
  particulier les grands perdants, les retraités) ; la rendre plus brève, la placer avec les autres résultats.
- Supprimer les formules qui affichent l'intention : « sans alourdir la charge des plus grandes fortunes », « un peu
  plus favorable aux familles », « contrainte du 1 % », « neutralité du haut » en titre, « la charge du 1 % ne doit
  pas bouger », « pour épargner le haut ». Remplacer par la neutralité distributive d'ensemble ou rien.
- Le détail du bilan pour le 1 % (conventions, compensations, CEHR) va en annexe ; le corps en garde une ou deux
  phrases et le chiffre central avec sa fourchette.

## 3. Couper : efficacité de mots

Objectif de longueur (mots hors commentaires, mesurés par `sed 's/%.*//' f | wc -w`) :

| fichier | avant | cible |
|---|---|---|
| ircsg.tex / annexe_ircsg.tex | 5 078 / 2 387 | ≤ 3 300 / ≤ 1 800 |
| foncier.tex / annexe_foncier.tex | 5 414 / 4 436 | ≤ 3 300 / ≤ 3 000 |
| is.tex / annexe_is.tex | 4 057 / 3 211 | ≤ 2 600 / ≤ 2 200 |
| pfu.tex / annexe_pfu.tex | 5 553 / 3 726 | ≤ 3 300 / ≤ 2 600 |
| ensemble.tex / annexe_methode.tex | 5 169 / 2 357 | ≤ 2 800 / ≤ 1 800 |
| introduction.tex / essentiel.tex | 1 351 / 567 | ≈ 550 / ≈ 400 |

Comment couper, par ordre de rendement :
- chaque idée et chaque chiffre une seule fois dans la note ; une partie renvoie à une autre plutôt que de redire ;
  le corps ne recopie pas l'annexe, la note de figure ne recopie pas le texte ;
- supprimer les phrases d'annonce, de transition, de récapitulation, les « autrement dit », les reformulations, les
  précautions répétées (une réserve importante est dite une fois, au bon endroit) ;
- un exemple par mécanisme, pas trois ; un cas-type par message ;
- phrases plus courtes, sujets concrets, verbes précis ;
- figures : au plus 9 dans le corps IR-CSG, 8 foncier, 6 IS, 6 PFU, 3 ou 4 ensemble ; supprimer celles qui redisent
  le texte ou une autre figure (ou les passer en annexe si elles portent une information unique) ; notes de figure de
  deux ou trois phrases au plus plus la source.

Ce qui ne bouge pas :
- **aucun chiffre modifié** (on peut en supprimer, pas en changer ni en arrondir autrement) ; vérifier avec
  `python3 synthese/verif_chiffres.py <fichier>` qui liste les nombres présents après la coupe mais absents avant ;
- l'architecture en six temps de chaque partie (situation actuelle ; problème économique ; réforme naïve ; réforme
  plus intelligente ; vrais arbitrages ; transition), en plus court ; les titres disent le résultat ;
- les hypothèses fortes et les chiffres non vérifiés restent signalés (plus brièvement) ; les fragilités qui
  peuvent changer la conclusion restent dans le corps (saillance de la CSG notamment) ;
- prose en vrais paragraphes (pas de listes à puces systématiques), pas de jargon de consultant ;
- les étiquettes `\label` citées ailleurs (`grep -rn 'ref{<label>}' synthese/parties`) : ne pas les supprimer sans
  mettre à jour les renvois ; ne pas renommer les étiquettes de section ;
- les tableaux `tab_ircsg_*.tex` sont générés par `tables_ircsg.py` : modifier le script et le relancer, pas le
  fichier ; les autres `tab_*.tex` peuvent être édités directement ou retirés du corps ;
- ne pas toucher aux scripts de calcul ni aux sorties ; ne pas committer (l'assemblage committe).

Compilation de contrôle, sans gêner les autres rédacteurs : depuis `synthese/`,
`mkdir -p $SCRATCH/tex && pdflatex -interaction=nonstopmode -halt-on-error -output-directory=$SCRATCH/tex note-reforme-fiscale.tex`
(une erreur dans la partie d'un autre rédacteur peut apparaître transitoirement : ne corriger que la sienne).
