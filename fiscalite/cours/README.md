# Le cours

`refaire-l-impot.tex` est la version de référence. Composition reprise de la charte du rapport :
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

`refaire-l-impot.html` est l'ancienne version, conservée pour la lecture en ligne.
