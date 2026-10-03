# Refaire le système fiscal français : plan détaillé

Rapport d'environ 150 pages sur ce que serait le système fiscal français s'il était reconstruit
à partir de zéro. Format think tank : les responsables politiques en premier lecteur, les
économistes et les citoyens ensuite. L'exercice prend pour modèle la *Mirrlees Review*
(2010-2011), avec deux différences : le terrain est français, et le système à réformer comporte
un bloc de cotisations sociales qui n'a pas d'équivalent britannique.

**La consigne qui prime sur toutes les autres : le rapport doit être pédagogique.** Mieux vaut un
chapitre entièrement compris qu'un chapitre exhaustif abandonné en cours de route.

## Les règles du jeu, fixées au cadrage

Consignées dans `CADRAGE.md`, où les vingt-trois questions sont tranchées. Dix commandent la
lecture du plan.

1. **Rendement constant.** Le rapport demande comment lever 1 270 Md€ mieux, pas combien lever.
   Chaque proposition est gagée. Une variante chiffre ce que coûterait de lever un à deux points
   de PIB de plus, puisque le déficit est de 5,1 points en 2025.
2. **Toute cotisation est un impôt.** Convention assumée, dont la figure `p2` montre la portée.
3. **Tous les transferts monétaires sont dans le périmètre**, y compris les prestations
   universelles : sans eux, un taux marginal effectif ne veut rien dire.
4. **Les paramètres des retraites sont donnés.** Seul leur financement est discuté.
5. **Périmètre Eurostat** pour tous les chiffres, avec un encadré nommant ce qui en est exclu.
6. **Pas de fonction de bien-être imposée.** Les résultats sont présentés pour un éventail de
   préférences redistributives, et le rapport dit à partir de quelle préférence sa conclusion
   bascule.
7. **La mobilité des bases est une contrainte forte**, assumée comme telle : elle borne d'emblée
   les taux sur le capital et sur le sommet du barème. En contrepartie, chaque affirmation de
   mobilité dit sur quoi elle repose, et distingue les cas documentés des extrapolations.
8. **Ordres de grandeur.** Pas de simulation distributive sur microdonnées : aucun accès. Les
   distributions par décile déjà publiées sont utilisées ; aucun perdant n'est nommé.
9. **L'idéal d'abord, le faisable ensuite.** Le système est construit sans les bornes du droit
   de l'Union et du droit constitutionnel, qui font l'objet d'un chapitre à part.
10. **Traçabilité stricte.** Tout chiffre renvoie à un fichier de `donnees/`. Un chapitre n'est
    fini que sans marque **[à sourcer]** résiduelle.

L'équipe de rédaction penche du même côté sur la question de l'efficience. Conséquence pratique :
chaque fois qu'une réforme améliore l'efficience au détriment de la progressivité, le rapport dit
**par quoi** elle est compensée. Sans cela il sera lu comme une plaidoirie.

## La forme

Les chapitres thématiques suivent tous la même marche : **ce qui existe aujourd'hui**, **ce que
la théorie dit d'optimal**, **ce qu'on ferait en repartant de zéro**. Les deux premières parties
fournissent les matériaux communs pour ne pas répéter vingt fois les mêmes chiffres.

Quatre dispositifs pédagogiques, construits systématiquement et non au cas par cas.

- **Les encadrés « comment ça marche »** : une page détachable qui explique un mécanisme depuis
  zéro. Prévus à ce stade : la remontée de la TVA le long de la chaîne de production ; pourquoi la
  perte sèche croît avec le carré du taux ; ce qu'est un rendement normal ; comment un transfert
  dégressif fabrique un taux marginal ; ce que fait l'inflation à un impôt sur le rendement.
- **Un cas chiffré récurrent** : trois ménages suivis d'un chapitre à l'autre, dont on voit ce
  que chaque réforme change. Proposition — un couple au voisinage du salaire minimum avec deux
  enfants, locataire ; un célibataire au salaire moyen, accédant à la propriété ; un couple de
  retraités propriétaires sans emprunt, au niveau de vie médian. Ils couvrent les trois marges qui
  comptent : les transferts, le logement, et la frontière entre actifs et retraités.
- **Une idée par figure** : chaque figure porte une seule affirmation, et son titre énonce la
  conclusion plutôt que le contenu.
- **Définitions en marge**, plus un glossaire final.

---

# Partie I — Le cadre (≈ 28 pages)

### 1. L'exercice, et pourquoi il est utile même si personne ne repart de zéro
Ce que veut dire « optimal » ici : au moins autant de redistribution, au moins autant de
recettes, moins de pertes. Les trois critères — efficience, équité, administrabilité — et ce
qu'ils arbitrent. Les règles du jeu ci-dessus, énoncées pour le lecteur. Pourquoi un système
existant ne peut pas se juger impôt par impôt.

### 2. Ce qu'un impôt coûte vraiment
Le mécanisme de la perte sèche expliqué sans courbe d'offre et de demande : l'impôt ne coûte
pas seulement ce qu'il prélève, il coûte aussi les échanges qui n'ont pas lieu parce qu'il
existe. Le résultat qui commande tout le reste : **le coût croît avec le carré du taux**.
Doubler un taux quadruple la perte, ce qui est l'argument décisif pour des assiettes larges
et des taux bas. Base rédigée dans `02_cadre_theorique.md`.

### 3. Les trois principes que l'on retient de Mirrlees
Juger le système comme un tout. Neutralité par défaut, écart justifié. Obtenir la
redistribution par l'instrument le moins distorsif. Chacun traduit en conséquence opératoire.
Base rédigée dans `02_cadre_theorique.md`. → `h4_lecture_par_principe.png`.

### 4. Quatre maquettes déjà construites
Ce qui a été essayé ailleurs, et ce que chaque solution résout : l'impôt dual nordique,
l'allocation pour rendement normal, le système par boîtes néerlandais, l'imposition des seuls
bénéfices distribués. Le problème commun qu'elles traitent — taxer le rendement, c'est taxer
l'attente, et d'autant plus que l'attente est longue. Où se situe la France, qui a fait la moitié
du chemin vers l'impôt dual sans le dire. Rédigé dans `05_maquettes_de_reference.md`.
→ `p4_impot_sur_l_attente.png`.

---

# Partie II — Ce que la France prélève aujourd'hui (≈ 25 pages)

### 5. Anatomie des 1 270 Md€
Combien, sur quoi, pour qui. Les trois impôts qui font la moitié du produit. La concentration :
dix prélèvements font 80 % des recettes, et la longue traîne compte des dizaines de taxes à
rendement négligeable. La déformation depuis 1995. Rédigé dans `01_etat_des_lieux.md`.
→ `g1`, `g2`, `g3`, `g4`, `g5`, `g9`, `g11`.

### 6. Découper les prélèvements selon ce qu'ils font
Quatre découpages qui ne sont dans aucune nomenclature officielle : ce qui est réellement taxé,
ce qui frappe un intrant de production, ce qui corrige une externalité, et ce que chaque bloc
devient à la lumière des trois principes. Le chiffre qui sert ensuite partout : 119 Md€ frappent
directement un facteur de production. Rédigé dans `03_decoupages.md`.
→ `h1`, `h2`, `h3`, `g6`, `g7`, `g10`.

### 7. Le coût de la complexité
Les dépenses fiscales et ce qu'elles coûtent. Les taxes à faible rendement dont le produit ne
couvre guère les frais de recouvrement. L'instabilité des règles, et pourquoi elle est en
elle-même un impôt : un investisseur qui ne sait pas quel sera le régime dans cinq ans exige une
prime, et cette prime est une perte sèche que personne n'encaisse.
→ `g8`, `g9`. **À construire** : coût de gestion rapporté au produit, par impôt.

---

# Partie III — Trois choses à comprendre avant de proposer (≈ 25 pages)

La partie pédagogique, demandée explicitement au cadrage. Ces trois sujets sont ceux où
l'intuition commune et l'arithmétique divergent le plus, et où le débat public se trompe le plus
souvent de grandeur.

### 8. Un taux marginal n'est pas un taux moyen
Ce que chaque mot veut dire, avec un exemple chiffré avant toute formule. Pourquoi un taux
marginal de 60 % sur une tranche ne signifie pas qu'on prend 60 % du revenu. Pourquoi, à
l'inverse, c'est bien le taux marginal qui décide des comportements : personne n'arbitre sur son
taux moyen. Où sont les pics français, et d'où ils viennent — la dégressivité des transferts, pas
le barème de l'impôt. Le résultat à emporter : un pic de taux marginal est toujours le prix d'un
ciblage, et un ciblage plus serré achète toujours un pic plus haut.
→ `m3_taux_marginaux_effectifs.png`, `m4_taux_participation.png`.
**À construire** : le profil continu du taux marginal effectif français du RSA au dernier décile,
par assemblage des barèmes, à défaut de microsimulation.

### 9. Taxer un stock ou taxer un flux : l'arithmétique qui décide
Un impôt sur le patrimoine ne se compare pas à un impôt sur le revenu : il faut d'abord le
convertir. Un prélèvement de 2 % par an sur un capital qui rapporte 3 % en termes réels prend
les deux tiers du rendement ; avec le prélèvement forfaitaire unique qui s'applique déjà au
rendement nominal, il prend plus que la totalité du rendement réel. Deux conséquences développées
sans polémique : un impôt sur le stock frappe d'autant plus durement que le rendement est faible,
donc il est régressif par rapport à l'habileté du détenteur ; et l'impôt français existant sur les
revenus du capital taxe déjà l'inflation, donc prélève la moitié d'un rendement réel de 3 % sans
que personne l'ait voulu. Le cas de la proposition Zucman — 2 % sur les patrimoines supérieurs à
100 M€ — est traité ici, sur ce terrain : l'argument qui la motive est réel, l'instrument est le
problème. Le précédent néerlandais du rendement présumé, censuré par la Cour suprême en décembre
2021, sert de contre-épreuve.
→ `p3_stock_contre_flux.png`, `p4_impot_sur_l_attente.png`.
**À construire** : le même calcul pour un patrimoine professionnel non liquide, et le rendement
implicite exigé pour que l'impôt ne force pas la cession. **[à sourcer]** le parcours
parlementaire exact de la proposition et son rendement attendu.

### 10. Les retraités : ce qu'ils reçoivent, ce qu'ils paient
Le fait d'abord : le niveau de vie médian des 65 ans et plus atteint 94 % de celui de l'ensemble
de la population, contre 90 % dans l'Union, 83 % en Allemagne et 78 % au Danemark ; et la pauvreté
française frappe 21,4 % des moins de 18 ans contre 12,4 % des plus de 65 ans, soit l'inverse exact
du profil allemand. Les prélèvements ensuite : sur 100 € bruts, une pension au taux normal
supporte 9,1 € de prélèvements sociaux contre 20,8 € pour un salaire — mais 11,3 de ces 20,8
ouvrent des droits, de sorte que l'écart dépend entièrement de la convention comptable retenue.
Le chapitre montre les deux lectures plutôt que d'en imposer une : le débat public sur la
contribution des retraités porte en fait sur une question de classification, pas sur un fait.
→ `p1_retraites_niveau_vie.png`, `p2_salaire_pension.png`.
**À construire** : part des 65 ans et plus dans le patrimoine total, et taux de prélèvement global
par âge.

---

# Partie IV — Reconstruire, assiette par assiette (≈ 55 pages)

Sept chapitres, tous en trois temps, chacun refermé par une recommandation chiffrée et par ce
qu'elle coûte ou rapporte, à rendement constant.

### 11. La consommation
*Aujourd'hui* : 206 Md€ de TVA, trois taux, un champ d'exonérations hérité. Les accises.
*La théorie* : le résultat d'Atkinson-Stiglitz et sa condition — la séparabilité entre biens et
travail. Pourquoi différencier les taux est un très mauvais instrument de redistribution : le
taux réduit sur l'alimentation donne plus d'argent aux riches qu'aux pauvres en euros, parce
qu'ils consomment plus.
*From scratch* : taux unique, base élargie, compensation intégrale par le barème direct. Les deux
vrais problèmes techniques, qui ne sont pas idéologiques : les services financiers et le logement
occupé par son propriétaire. **Position tranchée.**

### 12. Le travail et les transferts
*Aujourd'hui* : deux impôts sur le revenu qui ne partagent ni assiette ni unité ni barème, un
bloc de cotisations, des allègements qui créent leurs propres pentes, et des transferts dégressifs
qui font les pics du barème effectif.
*La théorie* : la formule du taux marginal optimal et ses trois ingrédients — l'élasticité, la
forme de la distribution des revenus, le poids social. Pourquoi le taux optimal est en U et non
croissant.
*From scratch* : un seul prélèvement sur le revenu du travail, une seule assiette, un barème
effectif continu du RSA au dernier décile. **Une section**, sans recommandation autonome, sur
l'unité d'imposition : l'imposition jointe fait peser sur le second apporteur de revenu un taux
calé sur le revenu du premier, là où l'élasticité est la plus forte. **Position tranchée.**

### 13. L'épargne et le capital des ménages
*Aujourd'hui* : une mosaïque de régimes — assurance vie, PEA, livrets, PER, immobilier locatif —
dont les taux effectifs diffèrent pour des placements économiquement voisins. Un prélèvement
forfaitaire unique qui ne distingue ni le rendement normal de la rente, ni le réel du nominal.
*La théorie* : séparer le rendement normal de la rente. Taxer la rente ne décourage rien ; taxer
le rendement normal décourage d'attendre, c'est-à-dire taxe la patience. Les maquettes du
chapitre 4 et ce qui les distingue vraiment.
*From scratch* : cadre dual complété par une allocation pour rendement normal et par une règle de
partage pour les dirigeants, et un traitement explicite de l'inflation. **Position tranchée.**

### 14. Les entreprises
*Aujourd'hui* : impôt sur les sociétés à 25 %, intérêts déductibles et rien pour les fonds
propres, et 119 Md€ de prélèvements assis sur une base indépendante du résultat.
*La théorie* : le théorème d'efficience productive de Diamond et Mirrlees. Taxer un intrant fait
produire moins avec les mêmes moyens, donc réduit le gâteau avant tout partage. Le biais de
financement : le système subventionne l'endettement.
*From scratch* : supprimer d'abord les prélèvements sur intrants, parce que c'est le seul gain
certain qui ne dépend d'aucune hypothèse de comportement. Neutraliser ensuite le biais de
financement, avec la réserve sérieuse de l'imposition minimale mondiale à 15 %, qui peut rendre
une allocation pour fonds propres inopérante.
**À construire** : base de taux effectifs de la Commission, méthodologie Devereux-Griffith.

### 15. Le patrimoine et les transmissions
*Aujourd'hui* : 50 Md€ sur la détention, assis sur des valeurs locatives de 1970 ; des droits de
mutation parmi les plus élevés d'Europe ; des droits de succession au barème élevé mais à
l'assiette très étroite.
*La théorie* : pourquoi taxer la transaction est à peu près la pire façon de taxer l'immobilier —
elle décourage le déménagement, donc la mobilité du travail. Pourquoi la rente foncière pure est
l'assiette la plus efficiente qui existe : le terrain ne se déplace pas et son offre ne réagit
pas. Pourquoi la transmission est le point où la théorie et l'opinion s'écartent le plus.
*From scratch* : déplacer la charge de la transaction vers la détention, sur une base réévaluée ;
séparer le terrain du bâti ; reconstruire l'assiette des transmissions plutôt que monter les taux.
**Position tranchée.** **À construire** : partage terrain/bâti dans les 50 Md€.

### 16. L'énergie et le carbone
*Aujourd'hui* : un prix implicite du carbone qui varie du simple au quadruple selon l'usage. Le
transport routier a 94 % de ses émissions tarifées au-dessus de 120 € la tonne ; l'industrie en a
6 % au-dessus de 60 €, les bâtiments 0,5 %, l'agriculture presque rien.
*La théorie* : un prix unique n'est pas une préférence, c'est une condition d'efficacité. Tant que
deux tonnes identiques ont deux prix, on achète la tonne chère et on laisse la tonne bon marché,
donc on paie plus cher une réduction donnée.
*From scratch* : un prix unique, et ce qu'il implique pour les autres taxes énergétiques, qui
cessent alors d'avoir une justification environnementale.
→ `m1`, `m2`, `g12`. **Position tranchée.**

### 17. La fiscalité locale
*Aujourd'hui* : des assiettes supprimées sans être remplacées, une autonomie de taux résiduelle,
et un financement par transferts qui coupe le lien entre la décision de dépense et son coût.
*La théorie* : un échelon qui vote la dépense doit en supporter le coût visible, sinon la
contrainte budgétaire disparaît. L'assiette locale doit être immobile, sous peine de concurrence
entre collectivités.
*From scratch* : une assiette foncière réévaluée, un pouvoir de taux réel, une péréquation
explicite plutôt que dissimulée dans les dotations.

---

# Partie V — La maquette, le droit, le chemin (≈ 20 pages)

### 18. La maquette d'ensemble
Ce que lève chaque assiette dans le système reconstruit, à rendement constant : le tableau qui
doit boucler sur 1 270 Md€, et la variante à un ou deux points de plus. C'est le chapitre qui rend
le reste crédible ou non. **À construire** : la maquette elle-même.

### 19. Ce que le droit interdit, et ce que cela coûte
Le droit de l'Union sur la structure des taux de TVA. La jurisprudence constitutionnelle sur
l'égalité devant les charges publiques et sur les taux confiscatoires. L'autonomie financière des
collectivités. Pour chaque contrainte : ce qu'elle empêche, ce que cela coûte, et si elle mérite
d'être renégociée. **[à sourcer]** pour chacune.

### 20. Les perdants, et comment on les traite
Qui perd dans chaque réforme, par ordre de grandeur et par situation type — pas par simulation.
Les effets de capitalisation, en particulier pour l'immobilier, où une réforme annoncée se paie
dans les prix avant d'entrer en vigueur. Les compensations possibles, et celles qui tuent la
réforme en la vidant.

### 21. Les séquences
Ce que l'on sait des réformes fiscales qui ont tenu, en France et ailleurs. Dans quel ordre les
mesures de cette maquette peuvent s'enchaîner sans qu'une étape rende la suivante impossible.

---

## Méthode de travail

Chaque chiffre renvoie à un fichier de `donnees/` ou à une source téléchargée dans `sources/`.
Les affirmations non traçables portent la marque **[à sourcer]** et sont résolues avant qu'un
chapitre soit considéré comme fini. Il en reste huit dans `01_etat_des_lieux.md`.

La littérature empirique est mobilisée en résumé : les résultats sont cités sans examen détaillé
de la stratégie d'identification. Conséquence à accepter — un résultat cité peut être fragile, et
le rapport ne le verra pas. Je signale au cas par cas quand un résultat porte seul une
recommandation chiffrée, parce que c'est là que l'exposition est réelle.

Rédaction en Markdown tant que le volume le permet, avec une structure de fichiers convertible en
LaTeX sans réécriture. Je rédige les chapitres complets avec leurs figures ; tu arbitres et tu
réécris.

## Fichiers

| Fichier | Contenu |
|---|---|
| `CADRAGE.md` | les vingt-trois questions de cadrage et les réponses du 3 octobre 2026 |
| `extract_donnees.py` | télécharge et extrait les trois sources de base |
| `extract_mirrlees.py` | données OCDE TaxBEN et Effective Carbon Rates |
| `extract_pedagogie.py` | Eurostat sur la situation des retraités, taux sociaux statutaires 2026 |
| `panorama.py` | agrégats, classement, concentration, déformation depuis 1995 |
| `classification.py` | reclassement des 123 prélèvements sur quatre dimensions |
| `graphiques.py` | figures `g1` à `g12`, et la charte partagée |
| `graphiques_decoupages.py` | figures `h1` à `h4` |
| `graphiques_mirrlees.py` | figures `m1` à `m4` |
| `graphiques_pedagogie.py` | figures `p1` à `p4` |
| `donnees/ntl_france.csv` | 121 prélèvements, rendement 1995-2024, code SEC, fonction économique |
| `donnees/classification_prelevements.csv` | le classement ligne par ligne, avec le motif |
| `01_etat_des_lieux.md` | matériau du chapitre 5 |
| `02_cadre_theorique.md` | matériau des chapitres 2 et 3 |
| `03_decoupages.md` | matériau du chapitre 6 |
| `04_mirrlees_applique.md` | diagnostics de *Tax by Design* répliqués, matériau des chapitres 8 et 16 |
| `05_maquettes_de_reference.md` | chapitre 4 rédigé |

## Sources déjà mobilisées

- Eurostat, *National Tax Lists*, mise à jour du 21 juillet 2026, onglet FR, 1995-2024.
- Eurostat, `nama_10_gdp`, `gov_10a_taxag`, `gov_10dd_edpt1`, `ilc_pnp2`, `ilc_li02`.
- *Évaluation des voies et moyens*, tome II, annexe au projet de loi de finances pour 2026.
- OCDE, modèle TaxBEN et *Effective Carbon Rates*.
- Urssaf, taux de cotisations du secteur privé au 1er janvier 2026 ; service-public.gouv.fr,
  fiche F2971 pour les prélèvements sociaux sur les pensions.
- IFS, *Tax by Design* (2011), texte intégral.

## Sources à mobiliser ensuite

- *Voies et moyens* tome I et liste des taxes affectées, pour nommer les 27 Md€ laissés en
  « autres taxes ».
- Annexes au PLFSS et données Urssaf, pour le détail des cotisations.
- Conseil des prélèvements obligatoires, Cour des comptes, IGF sur les taxes à faible rendement.
- Commission européenne, base de taux effectifs d'imposition des sociétés.
- Insee, DREES et IPP, distributions par décile déjà publiées.
- OCDE, *Revenue Statistics* et *Taxing Wages*.
