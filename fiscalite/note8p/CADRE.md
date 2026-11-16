# Refonte « note de 8 pages » (17/11/2026) : cadre commun à tous les chantiers

Décisions de l'auteur (économiste, coauteur de la note). Elles remplacent synthese/DECISIONS.md et
synthese/CONSIGNES_COUPE.md partout où elles divergent. Le travail existant (fiscalite/synthese, ir_csg, foncier, is,
pfu, revue) reste la base : on le réutilise, on ne refait que ce que les nouveaux arbitrages imposent. Pas de nouveau
modèle complexe, pas d'exploration de toutes les variantes.

## Doctrine
Vision de centre droit, libérale : favorable au travail, à l'investissement, à l'entrepreneuriat, à l'accumulation du
capital et à la croissance. Prélèvements obligatoires globalement constants. Trois objectifs : plus de croissance (moins
pénaliser travail, progression salariale, risque, investissement, mobilité) ; moins de rentes (déplacer l'impôt vers les
assiettes peu distorsives, d'abord la rente foncière ; moins d'avantages qui orientent les décisions) ; plus de
simplicité et de neutralité. Tenir compte des charges de famille ; éviter que des catégories importantes de
travailleurs soient lourdement pénalisées.

**Plus aucune contrainte redistributive artificielle** : pas de contrainte par décile, pas de neutralité du dernier
centile. On regarde d'abord ce que donne une réforme efficace, puis les résultats distributifs (actifs, familles). Si
certaines catégories de travailleurs ou de familles sont fortement pénalisées, corriger avec un minimum de
modifications, sans réintroduire de contraintes numériques dans l'optimisation.

Pragmatisme : instruments simples, crédibles, si possible déjà expérimentés ailleurs ; rapport coût-efficacité
systématique. Une mesure théoriquement intéressante mais coûteuse pour un effet faible ou incertain peut être écartée
et seulement mentionnée comme orientation de long terme (neutralité dette / fonds propres, exonération du rendement
normal, indexation des plus-values, traitement des pertes, suppression intégrale des DMTO). Ambitieux sur les
objectifs, conservateurs sur les instruments.

## Contrainte budgétaire (changement majeur)
Aucune hausse de la dette : neutralité budgétaire approximative **chaque année** (écarts techniques mineurs tolérés,
pas d'années de déficit organisées). L'ancienne trajectoire faisait ~32 Md€ de dette de transition (baisse immédiate
des DMTO avant la taxe foncière ; amortissement accéléré avant les recettes compensatrices ; recettes des plus-values
encaissées tard ; baisses mal financées) : chaque chantier doit fournir des montants **année par année** (2027-2040)
pour permettre un bouclage sans dette. Les recettes des plus-values à la transmission ne sont réutilisées qu'une fois
constatées. Distinguer les mesures nouvelles des évolutions déjà inscrites dans le droit (extinction de la CRDS fin
2033, fin des contributions exceptionnelles) ; ne pas financer deux fois la même mesure ; pas de recettes de croissance.
Base de chiffrage : prélèvements obligatoires 2025 ; à défaut 2024, en le disant. Droit de 2026.

## Mesure des gains
1. D'abord, quand c'est crédible, des effets réels en ordres de grandeur à partir d'élasticités standard réellement
   applicables : offre de travail (heures, ETP), participation, investissement, stock de capital, allocation des
   facteurs ; éventuellement traduits en PIB potentiel de long terme par une fonction de production standard
   (Cobb-Douglas, part du capital ~1/3), réforme par réforme. **Pas de chiffre global de PIB pour l'ensemble.**
   Interdits : élasticité du revenu imposable → production réelle ; hausse des transactions → hausse du PIB ; hausse
   temporaire de l'investissement → hausse permanente du PIB ; confusion niveau / taux de croissance.
2. Sinon, garder la réduction de perte sèche (méthode : synthese/parties/annexe_methode.tex, revue/methode_v2.md), en
   disant que c'est un indicateur d'efficacité, pas un supplément de PIB. Vérifier formules, élasticités, coins
   préexistants, substitutions, doubles comptes.
3. Dans le corps de la note : des indicateurs concrets (ce que rapporte une augmentation de salaire, ce que coûte un
   déménagement, le taux marginal effectif d'un investissement…).

Chaque résultat porte son statut : **[E]** résultat empirique publié ; **[S]** simulation calibrée par nous ;
**[H]** hypothèse ; **[C]** choix de politique. Chaque chiffre important doit être reproductible par un script.

## Livrables de chaque chantier (dossier fiscalite/note8p)
- scripts : `calculs/<bloc>_*.py` (python3 ; OpenFisca : python3.13) ; ne pas modifier les scripts existants des
  autres dossiers (les importer ou les copier) ;
- `sorties/<bloc>.json` : tous les chiffres utilisés, avec, pour le bouclage, une table `annuel` {année: {poste: Md€}}
  de 2027 à 2040 (+ = recette publique en plus par rapport au droit en vigueur, − = coût) et les coûts par point de
  paramètre utiles au bouclage ;
- `sorties/<bloc>.md` : compte rendu de 2 à 4 pages pour l'assembleur : choix faits, chiffres clés, cas-types, statut
  [E]/[S]/[H]/[C], limites qui peuvent changer la conclusion, références vérifiées (auteur, année, revue, résultat et
  ordre de grandeur) ;
- figures : `figures/gN_<nom>.pdf` + `.png` + `_source.tex` via `charte.sauver` (charte.py : gris = actuel, bleu clair =
  naïve/variante, bleu foncé = proposition, ocre brique = hausse/arbitrage ; un message par graphique ; pas de titre
  dans l'image ; légendes courtes ; pas de décimales inutiles ; largeur 6,3 pouces pleine page ou 3,05 demi-page,
  hauteur ≤ 2,6) ; proposer dans le .md un titre-message pour chaque figure ;
- `annexes/annexe_<bloc>.tex` : annexe technique (LaTeX, sections \subsection, ≤ 5 pages) : données, hypothèses,
  formules, variantes non retenues, résultats détaillés (déciles, configurations familiales), sensibilités, trajectoire.

## Règles
- fiscalite/CLAUDE.md : vérifier le droit sur les textes (CGI, CSS, BOFiP, service-public.fr, lois de finances) ; dater
  le droit ; ne rien affirmer de mémoire ; dire ce qui n'a pas pu être vérifié. Sites inaccessibles : ccomptes.fr,
  budget.gouv.fr, economie.gouv.fr (passer par vie-publique.fr, assemblee-nationale.fr, senat.fr).
- Ne jamais inventer une référence ou un chiffre ; pour un papier qui porte un raisonnement : question, données,
  identification, résultat et ordre de grandeur, limites.
- Exemples honnêtes et représentatifs, pas systématiquement favorables ; montrer les perdants.
- Fichiers téléchargés : chacun dans un nouveau dossier, lus avec `python3 -I`, jamais exécutés.
- Ne pas committer ; ne pas toucher aux fichiers d'un autre chantier.
