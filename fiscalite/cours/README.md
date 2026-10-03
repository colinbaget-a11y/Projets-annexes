# Le cours

`refaire-l-impot.tex` est la version de référence : 52 pages, quinze modules en trois parties,
trente et une figures et deux tableaux.

La deuxième partie est une lecture guidée de trois textes, lus l'un après l'autre et pour ce que
chacun démontre :

| module | texte |
|---|---|
| 8 | Mankiw, Weinzierl et Yagan, « Optimal Taxation in Theory and Practice », *JEP* 23(4), 2009 |
| 9 | *Tax by Design*, Mirrlees Review, IFS et Oxford University Press, 2011 |
| 10 | Johansson, Heady, Arnold, Brys et Vartia, « Taxation and Economic Growth », OCDE WP 620, 2008 |

Les PDF de travail sont dans `sources/` (non versionné). Composition reprise de la charte du rapport :
Latin Modern, titres de section en bleu `#003399`, phrase d'ouverture en gras, légendes de figure
au-dessus, sources et note de lecture sous la figure.

```sh
cd fiscalite
FIG_NU=1 python graphiques.py && FIG_NU=1 python graphiques_cours.py   # etc. pour chaque script
cd cours && pdflatex refaire-l-impot.tex && pdflatex refaire-l-impot.tex
```

Les figures incluses sont les versions « nues » de `figures/nu/*.pdf` : le titre principal devient
la légende LaTeX et n'est donc pas dessiné dans l'image, mais le sous-titre, les sources et la
note de lecture y restent. La variable d'environnement `FIG_NU` commande ce mode, et réduit aussi
le format et les tailles de texte pour que la figure soit composée à la taille à laquelle elle
sera imprimée.

`refaire-l-impot.html` est l'ancienne version en dix modules, conservée pour la lecture en
ligne ; elle n'est plus tenue à jour.

## Points de méthode à ne pas perdre

Le texte n'a plus d'encadré « comment ça marche » : les deux qui portaient la distinction taux
marginal / taux moyen et la définition de la progressivité sont passés en prose au module 4,
celui sur l'abattement pour rendement normal au module 5. Les encadrés restants sont des mises en
garde, pas des définitions.

- La valeur publiée par l'OCDE pour le taux supérieur français en 2013 (122,8 %) est écartée du
  tracé de la figure 24 et signalée en note : point isolé, cause non documentée par la source.
- Les magnitudes du document de l'OCDE ne sont pas reprises comme chiffrage : ses auteurs écrivent
  eux-mêmes qu'elles sont « plus élevées que ce à quoi on pourrait raisonnablement s'attendre ».
  Seul l'ordre du classement est utilisé, et sous le statut d'une confirmation, pas d'une preuve.
- Le ratio de couverture de la TVA (figure 7) rapporte les recettes à la seule consommation des
  ménages. L'indicateur OCDE voisin inclut la consommation publique et donne un niveau plus bas :
  ne pas mélanger les deux.
- Le poste SEC D29 (« autres impôts sur la production ») ne contient pas la même chose partout :
  la Suède y classe une large part de ses cotisations employeur et affiche 10,2 points de PIB.
  La comparaison France-Allemagne reste utilisable, mais le diagnostic tient au détail des
  prélèvements français, pas au rang dans l'agrégat.
- Sur les prélèvements rapportés au PIB hors cotisations imputées, la France est **deuxième**
  (43,5 %), à égalité avec l'Autriche et derrière le Danemark (45,4 %) — et non première, comme
  une version antérieure l'écrivait.
- Détention contre transaction immobilière : 45,6 Md€ (taxes foncières et IFI) contre 14,7 Md€
  (droits d'enregistrement). Les 48 et 17 d'une version antérieure n'étaient pas reconstituables
  à partir de la National Tax List.
- Le taux effectif sur l'épargne dépasse 100 % à partir de 7 % d'inflation pour un rendement réel
  de 3 %, et de 4,7 % pour un rendement réel de 2 % — pas à partir de 4 %.
