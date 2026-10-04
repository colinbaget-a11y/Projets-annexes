# Fiscalité : règles de travail

Ces règles valent pour tout le dossier `fiscalite/`, et d'abord pour le cours
`cours/refaire-l-impot.tex`.

## Vérifier en fiscaliste

Chaque fois que le cours explique comment fonctionne un impôt ou un prélèvement français, vérifier
que cela marche vraiment ainsi, sur les textes : assiette, taux, seuils, redevable, fait générateur,
exonérations, déductibilité, date d'effet. Sources de référence : CGI et code de la sécurité sociale
(Légifrance), BOFiP, brochure pratique de l'impôt sur le revenu de l'année, service-public.fr, lois
de finances et de financement de la sécurité sociale et leurs évaluations préalables.

- Dater le droit décrit quand il a changé (droit 2025 contre droit 2026) ; ne jamais présenter un
  régime exceptionnel comme le cas courant (exemple : l'IS à 36,1 % ne vise qu'environ 450
  entreprises).
- Ne rien affirmer de mémoire ; dire ce qui n'a pas pu être vérifié.
- Sites inaccessibles depuis l'environnement : ccomptes.fr, budget.gouv.fr, economie.gouv.fr ;
  passer par vie-publique.fr, assemblee-nationale.fr ou senat.fr.

## Distinguer le démontré du supposé

Mécanisme qu'on peut refaire au calcul, fait mesuré, effet causal identifié, hypothèse plausible :
le texte dit toujours de quoi il s'agit. Les hypothèses de l'auteur que la littérature n'a pas
établies restent dans le cours, formulées comme telles (« on peut supposer, sans que la littérature
l'ait prouvé, que… »).

## Style et figures

Prose dense et concrète ; pas de structures « A, et A' » répétées, ni de paragraphes d'annonce ou de
conclusions récapitulatives. Le cours ne doit pas s'allonger : une idée n'est exposée qu'une fois,
les chapitres suivants y renvoient ; la mécanique détaillée d'un impôt n'a sa place que si elle
illustre un point général ; une figure ne redit ni le texte ni une autre figure, et sa note ne
recopie pas le texte. Les sources et notes de lecture des figures sont écrites dans
`figures/nu/<figure>_note.tex` et composées en texte par `\figbloc`, jamais dans l'image.
