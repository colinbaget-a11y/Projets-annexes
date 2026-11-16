# Fusion des quatre notes en une seule (demande du 16/11/2026)

Demande de l'auteur :
1. fusionner les notes IR-CSG, foncier, IS, PFU en une seule note ;
2. enlever les répétitions manifestes ;
3. vérifier chaque calcul, et qu'aucun résultat n'est absurde au regard des ordres de grandeur ;
4. pour chaque réforme, calculer simplement la perte sèche, avec une version à peine plus évoluée que la
   perte quadratique (s'inspirer de la littérature de fiscalité optimale).

Consigne ajoutée par l'auteur : aucune hypothèse implicite (du type « on sort les loyers de la franchise »,
« on exonère jusqu'au minimum vieillesse »). Point de départ : assiettes larges, même taux pour tout le monde.
La note doit montrer tous les endroits où il y a un arbitrage à faire, chacun chiffré comme une variante
(recette, perte sèche, qui paie), sans le trancher en douce. Les révisions précédentes qui recommandaient de
telles exclusions (IR-CSG : loyers, minimum vieillesse) doivent être réécrites en arbitrages.

Arbitrages à faire apparaître :
- IR-CSG : franchise (montant, revenus couverts : activité, loyers, pensions) ; petites pensions ; individuel
  ou commun ; famille (rien, franchise, chèque, quotient) ; taux supérieur.
- Foncier : rapport terrain/bâti ; taux national avec ou sans reprise des ventes ; baisse de 30 ou 50 % ;
  étalement ; report de paiement.
- IS : déduction de 50 ou 100 % ; taux réduit gardé ou non ; financement par le taux ou l'assiette ;
  contribution exceptionnelle.
- PFU : taux ; report de l'apport-cession (expiration à toute transmission, à la cession, transmis sans
  effacement) ; majoration CEHR ; alignement des prélèvements sociaux.

## Étapes
- [ ] Vérification des calculs, par agents : `revue/verif_ir_csg.md`, `revue/verif_foncier.md`,
      `revue/verif_is_pfu.md`.
- [ ] Méthode de perte sèche, par agent : `revue/methode_perte_seche.md`.
- [ ] Script unique `synthese/perte_seche.py` : même formule pour les quatre réformes (Harberger généralisé :
      variation de perte sèche = somme, sur chaque marge, du coin fiscal moyen × variation de la quantité taxée ;
      coin total, déplacements entre assiettes, marge extensive).
- [ ] Note fusionnée `synthese/note-reforme-fiscale.tex` (+ docx) : introduction commune (objectifs et
      contraintes) ; encadré méthode ; une section par réforme ; tableau de synthèse (recette, perte sèche,
      qui paie, grandes fortunes, familles, transition) ; bibliographie unique.

## Répétitions à supprimer
Objectifs et contraintes répétés dans chaque introduction ; taux cumulés IS + PFU (notes IS et PFU) ;
CEHR et majoration (IR-CSG et PFU) ; paragraphes « grandes fortunes » et « familles » de chaque note ;
« ce qu'on ne fait pas » ; listes de références.
